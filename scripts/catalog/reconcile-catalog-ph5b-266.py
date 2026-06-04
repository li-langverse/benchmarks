#!/usr/bin/env python3
"""PH-5b catalog honesty for benchmarks#266 — repo field, vertical stubs, path fixes.

Sub-phases A–C from docs/ecosystem/plans/2026-06-01-catalog-audit-honesty-ph5b-266.md:
  A) repo=benchmarks when workload exists under benchmarks/
  B) bio_/drug_/am_ vertical stubs: path=unknown, catalog_lifecycle=planned, variant=vertical_stub
  C) ml_* path -> benchmarks/workloads/tier1_micro/<id>; tier5 lis paths -> vendor layout

Usage:
  python3 scripts/catalog/reconcile-catalog-ph5b-266.py --dry-run
  python3 scripts/catalog/reconcile-catalog-ph5b-266.py --write
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
VENDOR_LIS = ROOT / "vendor/lis-tier5"

VERTICAL_PREFIXES = ("bio_", "drug_", "am_")

TIER5_LIS_PATH_FIX = {
    "https_static": "benchmarks/tier5_http/scenarios/https_static",
    "lb_least_conn": "benchmarks/tier5_http/scenarios/lb_least_conn",
    "lb_peer_down": "benchmarks/tier5_http/scenarios/lb_peer_down",
    "lb_round_robin": "benchmarks/tier5_http/scenarios/lb_round_robin",
    "proxy_loopback": "benchmarks/tier5_http/scenarios/proxy_loopback",
}


def load_format_helpers():
    path = Path(__file__).parent / "sync-paths-from-lic-tree.py"
    spec = importlib.util.spec_from_file_location("sync_paths", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.load_header, mod.format_benchmark


def path_exists_for_row(row: dict) -> bool:
    rel = str(row.get("path", "")).strip()
    if not rel or rel == "unknown":
        return False
    repo = str(row.get("repo", "lic"))
    if repo == "benchmarks":
        root = ROOT
    elif repo == "lis":
        root = VENDOR_LIS if VENDOR_LIS.is_dir() else None
    else:
        root = None
    if root is None:
        return False
    p = root / rel
    return p.is_dir() or p.is_file()


def reconcile(rows: list[dict]) -> dict[str, list[str]]:
    changes: dict[str, list[str]] = {
        "repo_benchmarks": [],
        "vertical_planned": [],
        "ml_paths": [],
        "tier5_lis_paths": [],
    }

    for row in rows:
        bid = str(row.get("id", ""))
        if not bid:
            continue

        rel = str(row.get("path", "")).strip()

        # C) ml workloads live under tier1_micro
        if bid.startswith("ml_") and rel.startswith("benchmarks/ml/"):
            alt = f"benchmarks/workloads/tier1_micro/{bid}"
            if (ROOT / alt).is_dir():
                row["path"] = alt
                row["repo"] = "benchmarks"
                changes["ml_paths"].append(bid)

        # C) tier5 lis vendor layout (no workloads/ prefix)
        if bid in TIER5_LIS_PATH_FIX:
            new_path = TIER5_LIS_PATH_FIX[bid]
            if (VENDOR_LIS / new_path).is_dir():
                row["path"] = new_path
                row["repo"] = "lis"
                changes["tier5_lis_paths"].append(bid)

        rel = str(row.get("path", "")).strip()

        # B) vertical competitive stubs with bogus remaps
        if bid.startswith(VERTICAL_PREFIXES) and row.get("catalog_lifecycle") != "planned":
            tail = Path(rel).name if rel else ""
            if not rel or tail != bid:
                row["path"] = "unknown"
                row["catalog_lifecycle"] = "planned"
                row["variant"] = "vertical_stub"
                row["repo"] = "benchmarks"
                changes["vertical_planned"].append(bid)
                continue

        if row.get("catalog_lifecycle") == "planned":
            continue

        # A) repo field when path is under benchmarks checkout
        if rel.startswith("benchmarks/") and (ROOT / rel).is_dir():
            if str(row.get("repo", "lic")) != "benchmarks":
                row["repo"] = "benchmarks"
                changes["repo_benchmarks"].append(bid)

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.write:
        parser.error("pass --dry-run or --write")

    load_header, format_benchmark = load_format_helpers()
    text = CATALOG.read_text(encoding="utf-8")
    rows = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    changes = reconcile(rows)

    total = sum(len(v) for v in changes.values())
    for kind, ids in changes.items():
        print(f"{kind}: {len(ids)}")
        for bid in ids[:8]:
            print(f"  {bid}")
        if len(ids) > 8:
            print(f"  ... +{len(ids) - 8}")

    if args.dry_run or total == 0:
        return 0

    header = load_header(text)
    CATALOG.write_text(header + "\n\n".join(format_benchmark(b) for b in rows) + "\n")
    print(f"wrote {CATALOG} ({total} row updates)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
