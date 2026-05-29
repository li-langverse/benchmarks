#!/usr/bin/env python3
"""Validate a data/gpu-contributions/<slug>/ folder before PR."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRIB_ROOT = ROOT / "data" / "gpu-contributions"
SCHEMA = "benchmarks/gpu-chip-contribution/v1"
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_MANIFEST_KEYS = (
    "schema",
    "chip_slug",
    "label",
    "vendor",
    "host_os",
    "primary_backend",
    "artifacts",
    "submitted_at",
)
ALLOWED_VENDORS = frozenset({"nvidia", "amd", "apple", "intel", "other"})
ALLOWED_BACKENDS = frozenset({"cuda", "hip", "metal", "vulkan"})


def validate_dir(contrib_dir: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = contrib_dir / "contribution.json"
    if not manifest_path.is_file():
        return [f"{contrib_dir.name}: missing contribution.json"]

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{contrib_dir.name}: invalid JSON in contribution.json: {exc}"]

    if manifest.get("schema") != SCHEMA:
        errors.append(f"{contrib_dir.name}: schema must be {SCHEMA}")

    slug = manifest.get("chip_slug")
    if slug != contrib_dir.name:
        errors.append(
            f"{contrib_dir.name}: chip_slug {slug!r} must match directory name"
        )
    if not slug or not SLUG_RE.match(str(slug)):
        errors.append(f"{contrib_dir.name}: chip_slug must match {SLUG_RE.pattern}")

    for key in REQUIRED_MANIFEST_KEYS:
        if key not in manifest:
            errors.append(f"{contrib_dir.name}: missing manifest key {key}")

    vendor = manifest.get("vendor")
    if vendor not in ALLOWED_VENDORS:
        errors.append(f"{contrib_dir.name}: vendor must be one of {sorted(ALLOWED_VENDORS)}")

    backend = manifest.get("primary_backend")
    if backend not in ALLOWED_BACKENDS:
        errors.append(
            f"{contrib_dir.name}: primary_backend must be one of {sorted(ALLOWED_BACKENDS)}"
        )

    artifacts = manifest.get("artifacts") or {}
    suite_name = artifacts.get("lig_gpu_suite")
    if not suite_name:
        errors.append(f"{contrib_dir.name}: artifacts.lig_gpu_suite required")
    else:
        suite_path = contrib_dir / str(suite_name)
        if not suite_path.is_file():
            errors.append(f"{contrib_dir.name}: missing artifact {suite_name}")
        else:
            try:
                suite = json.loads(suite_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{contrib_dir.name}: invalid suite JSON: {exc}")
            else:
                if suite.get("schema") != "ph-hw/lig-full-gpu-suite/v1":
                    errors.append(
                        f"{contrib_dir.name}: suite schema must be ph-hw/lig-full-gpu-suite/v1"
                    )
                if not suite.get("matrix"):
                    errors.append(f"{contrib_dir.name}: suite matrix is empty")

    honest_name = artifacts.get("lig_gpu_honest")
    if honest_name:
        honest_path = contrib_dir / str(honest_name)
        if not honest_path.is_file():
            errors.append(f"{contrib_dir.name}: missing optional artifact {honest_name}")

    contrib = manifest.get("contributor") or {}
    if not contrib.get("github") and not contrib.get("anonymous_ok"):
        errors.append(
            f"{contrib_dir.name}: set contributor.github or contributor.anonymous_ok"
        )

    return errors


def main() -> int:
    targets: list[Path]
    if len(sys.argv) > 1:
        targets = [CONTRIB_ROOT / sys.argv[1]]
    else:
        if not CONTRIB_ROOT.is_dir():
            print("No gpu-contributions directory — skipping")
            return 0
        targets = sorted(p for p in CONTRIB_ROOT.iterdir() if p.is_dir())

    all_errors: list[str] = []
    for d in targets:
        if d.name.startswith("_") or d.name.startswith("."):
            continue
        all_errors.extend(validate_dir(d))

    if all_errors:
        for e in all_errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"Validated {len(targets)} GPU contribution(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
