#!/usr/bin/env python3
"""Merge release manifests into data/latest/release-index.json.

Reads data/incoming/manifests/*.json (see schema/release-manifest.json).
Does not fabricate benchmark CSV rows or summary.json entries.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INCOMING_DIR = ROOT / "data" / "incoming" / "manifests"
INDEX_PATH = ROOT / "data" / "latest" / "release-index.json"

ALLOWED_PACKAGES = frozenset(
    {"lic", "lis", "lip", "lit", "lidb", "lig", "li-math"}
)
ARTIFACT_KINDS = frozenset({"csv", "manifest", "other"})


class ManifestError(Exception):
    pass


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def validate_manifest(raw: dict, *, source: str) -> dict:
    if not isinstance(raw, dict):
        raise ManifestError(f"{source}: manifest must be a JSON object")

    required = (
        "package",
        "version",
        "git_sha",
        "published_at",
        "bench_required",
        "artifacts",
    )
    missing = [k for k in required if k not in raw]
    if missing:
        raise ManifestError(f"{source}: missing fields: {', '.join(missing)}")

    package = raw["package"]
    if package not in ALLOWED_PACKAGES:
        raise ManifestError(
            f"{source}: unknown package {package!r} "
            f"(allowed: {', '.join(sorted(ALLOWED_PACKAGES))})"
        )

    if not isinstance(raw["version"], str) or not raw["version"].strip():
        raise ManifestError(f"{source}: version must be a non-empty string")
    if not isinstance(raw["git_sha"], str) or len(raw["git_sha"].strip()) < 7:
        raise ManifestError(f"{source}: git_sha must be at least 7 characters")
    if not isinstance(raw["published_at"], str) or not raw["published_at"].strip():
        raise ManifestError(f"{source}: published_at must be a non-empty ISO-8601 string")
    if not isinstance(raw["bench_required"], bool):
        raise ManifestError(f"{source}: bench_required must be boolean")

    artifacts = raw["artifacts"]
    if not isinstance(artifacts, list):
        raise ManifestError(f"{source}: artifacts must be an array")

    normalized_artifacts: list[dict] = []
    for i, item in enumerate(artifacts):
        if not isinstance(item, dict):
            raise ManifestError(f"{source}: artifacts[{i}] must be an object")
        if "path" not in item or "kind" not in item:
            raise ManifestError(f"{source}: artifacts[{i}] requires path and kind")
        kind = item["kind"]
        if kind not in ARTIFACT_KINDS:
            raise ManifestError(
                f"{source}: artifacts[{i}].kind must be one of "
                f"{', '.join(sorted(ARTIFACT_KINDS))}"
            )
        path = item["path"]
        if not isinstance(path, str) or not path.strip():
            raise ManifestError(f"{source}: artifacts[{i}].path must be a non-empty string")
        normalized_artifacts.append({"path": path, "kind": kind})

    return {
        "package": package,
        "version": raw["version"].strip(),
        "git_sha": raw["git_sha"].strip(),
        "published_at": raw["published_at"].strip(),
        "bench_required": raw["bench_required"],
        "artifacts": normalized_artifacts,
    }


def load_index() -> dict:
    if INDEX_PATH.is_file():
        data = json.loads(INDEX_PATH.read_text())
        if not isinstance(data, dict):
            raise ManifestError(f"{INDEX_PATH}: root must be an object")
        packages = data.get("packages")
        if packages is None:
            packages = {}
        if not isinstance(packages, dict):
            raise ManifestError(f"{INDEX_PATH}: packages must be an object")
        return {"updated_at": data.get("updated_at"), "packages": packages}
    return {"updated_at": None, "packages": {}}


def package_entry(manifest: dict, *, source: str) -> dict:
    entry = {
        "version": manifest["version"],
        "git_sha": manifest["git_sha"],
        "published_at": manifest["published_at"],
        "bench_required": manifest["bench_required"],
        "artifacts": manifest["artifacts"],
        "manifest_source": source,
    }

    csv_paths = [
        a["path"]
        for a in manifest["artifacts"]
        if a["kind"] == "csv"
    ]
    if manifest["bench_required"] and csv_paths:
        existing = [p for p in csv_paths if (ROOT / p).is_file()]
        if existing:
            entry["csv_refresh_needed"] = True
            entry["csv_artifact_paths"] = existing

    return entry


def collect_manifest_paths() -> list[Path]:
    if not INCOMING_DIR.is_dir():
        return []
    return sorted(
        p
        for p in INCOMING_DIR.glob("*.json")
        if p.is_file() and not p.name.startswith(".")
    )


def ingest(*, write_index: bool = True) -> dict:
    index = load_index()
    notes: list[str] = []
    merged = 0

    for path in collect_manifest_paths():
        source = str(path.relative_to(ROOT))
        try:
            raw = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            raise ManifestError(f"{source}: invalid JSON: {exc}") from exc

        manifest = validate_manifest(raw, source=source)
        pkg = manifest["package"]
        entry = package_entry(manifest, source=source)
        index["packages"][pkg] = entry
        merged += 1

        if entry.get("csv_refresh_needed"):
            notes.append(
                f"{pkg}: csv refresh needed (bench_required, artifact on disk; "
                "run ingest-lic after copying CSV — no fabricated bench rows)"
            )

    index["updated_at"] = _iso_now()
    if notes:
        index["notes"] = notes

    if write_index:
        INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        INDEX_PATH.write_text(json.dumps(index, indent=2) + "\n")

    return {"merged": merged, "packages": len(index["packages"]), "notes": notes}


def main() -> int:
    try:
        result = ingest()
    except ManifestError as exc:
        print(f"ingest-release-manifests: error: {exc}", file=sys.stderr)
        return 1

    print(
        f"ingest-release-manifests: merged {result['merged']} manifest(s), "
        f"{result['packages']} package(s) in index"
    )
    for note in result["notes"]:
        print(f"  note: {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
