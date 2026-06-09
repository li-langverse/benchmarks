#!/usr/bin/env python3
"""Classify catalog.toml path gaps: fix_path, planned, bogus_remap, lic_impl.

Writes data/latest/catalog-gap-triage.json. Use --write-planned to mark competitive
vertical stub rows honest (catalog_lifecycle=planned, path=unknown).

Env: LIC_ROOT (default ../lic), same roots as plan-completion-audit.py.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import os as _os

LIC = Path(_os.environ.get("LIC_ROOT", ROOT.parent / "lic"))
OUT = ROOT / "data/latest/catalog-gap-triage.json"
CATALOG = ROOT / "catalog.toml"
VENDOR_LIS = ROOT / "vendor/lis-tier5"

# Competitive vertical catalog ids ahead of lic harness (PH-5b honesty policy).
VERTICAL_STUB_PREFIXES = (
    "bio_",
    "drug_",
    "robo_",
    "am_",
    "pde_cfl_",
    "pde_heat_implicit",
)

INTENTIONAL_ID_PATH = {
    "tier0_stability": "tier0_correctness",
}


def _catalog_path_candidates(repo: str, rel: str) -> list[Path]:
    rel = rel.replace("\\", "/")
    out: list[Path] = []
    if repo == "lic":
        out.extend([LIC / rel, ROOT / rel])
        if "/workloads/" in rel:
            out.append(LIC / rel.replace("/workloads/", "/", 1))
    elif repo == "lis":
        if VENDOR_LIS.is_dir():
            out.append(VENDOR_LIS / rel)
            if "/workloads/" in rel:
                out.append(VENDOR_LIS / rel.replace("/workloads/", "/", 1))
    elif repo == "benchmarks":
        out.append(ROOT / rel)
    elif repo == "li-math":
        tail = rel.rsplit("/", 1)[-1]
        out.append(ROOT / "benchmarks/workloads/tier1_micro" / tail)
    elif repo in ("lig", "lip", "lit"):
        out.append(ROOT / rel)
    else:
        root = ROOT if repo == "benchmarks" else None
        if root:
            out.append(root / rel)
    return out


def path_exists(repo: str, rel: str) -> bool:
    return any(p.is_dir() or p.is_file() for p in _catalog_path_candidates(repo, rel))


def is_bogus_remap(row: dict) -> bool:
    bid = str(row.get("id", ""))
    rel = str(row.get("path", "")).strip()
    if not bid or not rel or rel == "unknown":
        return False
    if row.get("catalog_lifecycle") == "planned":
        return False
    intentional = INTENTIONAL_ID_PATH.get(bid)
    if intentional and intentional in rel:
        return False
    tail = rel.rsplit("/", 1)[-1]
    if bid == tail or bid.startswith(tail + "_"):
        return False
    return True


def is_vertical_stub_id(bid: str) -> bool:
    return any(bid.startswith(p) for p in VERTICAL_STUB_PREFIXES)


def classify_row(row: dict) -> str | None:
    bid = str(row.get("id", ""))
    rel = str(row.get("path", "")).strip()
    repo = str(row.get("repo", "lic"))
    if row.get("catalog_lifecycle") == "planned" or rel in ("", "unknown"):
        return None
    if is_vertical_stub_id(bid) or is_bogus_remap(row):
        return "bogus_remap"
    if not path_exists(repo, rel):
        if is_vertical_stub_id(bid):
            return "planned"
        return "lic_impl"
    return None


def triage_catalog() -> dict:
    import tomllib

    data = tomllib.loads(CATALOG.read_text(encoding="utf-8"))
    buckets: dict[str, list[dict]] = {
        "bogus_remap": [],
        "planned": [],
        "lic_impl": [],
        "fix_path": [],
    }
    for row in data.get("benchmark", []):
        kind = classify_row(row)
        if not kind:
            continue
        entry = {
            "id": row.get("id"),
            "repo": row.get("repo", "lic"),
            "path": row.get("path"),
            "tier": row.get("tier"),
        }
        buckets[kind].append(entry)
    return buckets


EXTRA_PLANNED_IDS = frozenset(
    {
        "proxy_loopback",
        "viz_colormap",
        "viz_decimate",
        "viz_inspector_panels",
        "viz_linked_views",
        "viz_marching_cubes",
        "viz_pipeline_graph",
        "viz_resample",
    }
)

ML_PATH_FIXES = {
    "ml_conv2d_forward": "benchmarks/workloads/tier1_micro/ml_conv2d_forward",
    "ml_mlp_forward": "benchmarks/workloads/tier1_micro/ml_mlp_forward",
    "ml_mlp_train_step": "benchmarks/workloads/tier1_micro/ml_mlp_train_step",
}


def _load_format_benchmark():
    import importlib.util

    path = ROOT / "scripts/catalog/sync-paths-from-lic-tree.py"
    spec = importlib.util.spec_from_file_location("sync_paths", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.format_benchmark, mod.load_header


def apply_planned_stubs() -> int:
    """Mark competitive vertical stubs and bogus remaps as planned; fix ml paths."""
    import tomllib

    format_benchmark, load_header = _load_format_benchmark()
    text = CATALOG.read_text(encoding="utf-8")
    data = tomllib.loads(text)
    changed = 0
    rows: list[dict] = []
    for row in data.get("benchmark", []):
        bid = str(row.get("id", ""))
        if bid in ML_PATH_FIXES:
            row = dict(row)
            row["path"] = ML_PATH_FIXES[bid]
            changed += 1
        if row.get("catalog_lifecycle") != "planned" and (
            is_vertical_stub_id(bid) or is_bogus_remap(row) or bid in EXTRA_PLANNED_IDS
        ):
            row = dict(row)
            row["catalog_lifecycle"] = "planned"
            row["path"] = "unknown"
            changed += 1
        rows.append(row)
    if changed:
        header = load_header(text)
        body = "\n\n".join(format_benchmark(b) for b in rows) + "\n"
        CATALOG.write_text(header + body, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-planned",
        action="store_true",
        help="Mark competitive vertical stub / bogus-remap rows planned in catalog.toml",
    )
    args = parser.parse_args()
    if args.write_planned:
        n = apply_planned_stubs()
        print(f"catalog.toml: marked {n} rows planned (path=unknown)")

    buckets = triage_catalog()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    report = {
        "generated_at": now,
        "roots": {"lic": str(LIC), "benchmarks": str(ROOT)},
        "summary": {k: len(v) for k, v in buckets.items()},
        "buckets": buckets,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
