#!/usr/bin/env python3
"""Triage catalog.toml lic path gaps — classify and optionally apply planned-row honesty.

Writes data/latest/catalog-gap-triage.json.

Usage:
  LIC_ROOT=../lic python3 scripts/catalog/catalog-gap-triage.py
  LIC_ROOT=../lic python3 scripts/catalog/catalog-gap-triage.py --write
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
OUT = ROOT / "data/latest/catalog-gap-triage.json"

if str(ROOT / "scripts/catalog") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts/catalog"))

import importlib.util

from gap_policy import (  # noqa: E402
    classify_catalog_row,
    remediation_for,
)

_sync_path = ROOT / "scripts/catalog/sync-paths-from-lic-tree.py"
_spec = importlib.util.spec_from_file_location("sync_paths_from_lic_tree", _sync_path)
if _spec is None or _spec.loader is None:
    raise SystemExit(f"cannot load {_sync_path}")
_sync_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sync_mod)
format_benchmark = _sync_mod.format_benchmark
load_header = _sync_mod.load_header


def resolve_lic_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).resolve()
    return Path(os.environ.get("LIC_ROOT", ROOT.parent / "lic")).resolve()


def triage_rows(benchmarks: list[dict], lic_root: Path) -> list[dict]:
    rows: list[dict] = []
    for row in benchmarks:
        action = classify_catalog_row(row, lic_root=lic_root, bench_root=ROOT)
        rel = str(row.get("path", "")).strip()
        rows.append(
            {
                "id": row["id"],
                "repo": row.get("repo", "lic"),
                "path": rel or "unknown",
                "tier": row.get("tier"),
                "catalog_lifecycle": row.get("catalog_lifecycle"),
                "action": action,
                "remediation": remediation_for(action),
            }
        )
    return rows


def apply_remediations(benchmarks: list[dict], triage: list[dict]) -> list[str]:
    by_id = {t["id"]: t for t in triage}
    changed: list[str] = []
    for row in benchmarks:
        t = by_id.get(row["id"])
        if not t:
            continue
        fix = t.get("remediation")
        if fix == "planned_unknown":
            if row.get("path") != "unknown" or row.get("catalog_lifecycle") != "planned":
                row["path"] = "unknown"
                row["catalog_lifecycle"] = "planned"
                if not row.get("ph_ids"):
                    row["ph_ids"] = ["PH-5b"]
                changed.append(row["id"])
        elif fix == "planned_keep_path":
            if row.get("catalog_lifecycle") != "planned":
                row["catalog_lifecycle"] = "planned"
                if not row.get("ph_ids"):
                    row["ph_ids"] = ["PH-5b"]
                changed.append(row["id"])
    return changed


def load_footer(text: str) -> str:
    """Preserve [reporting] and trailing sections after the last [[benchmark]] block."""
    marker = "[[benchmark]]"
    idx = text.rfind(marker)
    if idx < 0:
        return ""
    tail = text[idx:]
    end = tail.find("\n\n[", 1)
    if end < 0:
        return ""
    return tail[end + 2 :].rstrip() + "\n"


def write_catalog(benchmarks: list[dict]) -> None:
    original = CATALOG.read_text(encoding="utf-8")
    header = load_header(original)
    footer = load_footer(original)
    body = "\n\n".join(format_benchmark(b) for b in benchmarks)
    out = header + body + "\n"
    if footer:
        out += "\n" + footer
    CATALOG.write_text(out, encoding="utf-8")


def main() -> int:
    import tomllib

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lic-root", type=Path, default=None)
    parser.add_argument("--write", action="store_true", help="apply planned/unknown remediations to catalog.toml")
    args = parser.parse_args()

    lic_root = resolve_lic_root(str(args.lic_root) if args.lic_root else None)
    text = CATALOG.read_text(encoding="utf-8")
    benchmarks = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    triage = triage_rows(benchmarks, lic_root)

    counts = Counter(r["action"] for r in triage)
    remediations = Counter(r["remediation"] for r in triage if r["remediation"])

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "lic_root": str(lic_root),
        "lic_present": lic_root.is_dir(),
        "summary": {
            "catalog_rows": len(benchmarks),
            "by_action": dict(sorted(counts.items())),
            "remediations": dict(sorted(remediations.items())),
            "bogus_remap": [r["id"] for r in triage if r["action"] == "bogus_remap"],
            "defer_planned": [r["id"] for r in triage if r["action"] == "defer_planned"],
            "lic_impl": [r["id"] for r in triage if r["action"] == "lic_impl"],
        },
        "rows": triage,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(json.dumps(report["summary"], indent=2))

    if args.write:
        changed = apply_remediations(benchmarks, triage)
        if not changed:
            print("catalog.toml: no remediations to apply")
            return 0
        write_catalog(benchmarks)
        print(f"catalog.toml: applied {len(changed)} remediations")
        for bench_id in changed[:15]:
            print(f"  - {bench_id}")
        if len(changed) > 15:
            print(f"  ... and {len(changed) - 15} more")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
