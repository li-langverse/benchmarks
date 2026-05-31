#!/usr/bin/env python3
"""Audit catalog.toml vs workloads on disk; emit data/latest/catalog-audit.json."""
from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
WORKLOADS = ROOT / "benchmarks" / "workloads"
OUT = ROOT / "data" / "latest" / "catalog-audit.json"


def resolve_catalog_path(path: str, bid: str) -> Path:
    """Map catalog path strings to on-disk workload directories."""
    if not path or path in ("unknown",):
        return Path()
    p = path.replace("\\", "/")
    candidates: list[Path] = []
    if p.startswith("benchmarks/"):
        candidates.append(ROOT / p)
    if p.startswith("benchmarks/tier"):
        candidates.append(ROOT / p.replace("benchmarks/tier", "benchmarks/workloads/tier", 1))
    if p.startswith("benchmarks/viewport/"):
        tail = p.split("/", 2)[-1]
        candidates.append(WORKLOADS / "tier1_micro" / tail)
    for tier in (
        "tier0_correctness", "tier1_micro", "tier1_stdlib", "tier2_physics",
        "tier3_ecosystem", "tier5_http", "tier6_db", "tier7_compiler",
    ):
        candidates.append(WORKLOADS / tier / bid)
    for c in candidates:
        if c.is_dir():
            return c
    return candidates[0] if candidates else Path()

def main() -> int:
    doc = tomllib.loads(CATALOG.read_text(encoding="utf-8"))
    rows = doc.get("benchmark", [])
    missing_size: list[str] = []
    harness_pending: list[str] = []
    path_missing: list[str] = []
    path_ok: list[str] = []
    for b in rows:
        bid = b.get("id", "")
        sl = b.get("size_label", "")
        path = b.get("path", "")
        if sl == "harness pending":
            harness_pending.append(bid)
        if not b.get("problem_size") and sl != "harness pending" and b.get("catalog_lifecycle") != "planned":
            if not sl:
                missing_size.append(bid)
        if path in ("unknown", "", None):
            continue
        full = ROOT / path if not str(path).startswith("benchmarks/workloads") else ROOT / path
        if str(path).startswith("benchmarks/"):
            full = ROOT / path
        elif (WORKLOADS / path.split("/")[-1]).exists() and "tier" in path:
            full = ROOT / path
        else:
            # try workloads mirror
            alt = WORKLOADS
            for part in ("tier1_micro", "tier2_physics"):
                if (WORKLOADS / part / bid).is_dir():
                    full = WORKLOADS / part / bid
                    break
        if full.is_dir() or (ROOT / path).is_dir():
            path_ok.append(bid)
        elif path.startswith("benchmarks/workloads") and (ROOT / path).is_dir():
            path_ok.append(bid)
        elif (WORKLOADS / "tier1_micro" / bid).is_dir() or (WORKLOADS / "tier2_physics" / bid).is_dir():
            path_ok.append(bid)
        else:
            if path not in ("unknown", "li-tests/benchmarks/tier0_correctness"):
                path_missing.append({"id": bid, "path": path})

    report = {
        "schema": "benchmarks/catalog-audit/v1",
        "catalog_rows": len(rows),
        "harness_pending_count": len(harness_pending),
        "harness_pending_sample": harness_pending[:20],
        "missing_problem_size_count": len(missing_size),
        "missing_problem_size_sample": missing_size[:20],
        "workload_dir_present_count": len(path_ok),
        "workload_dir_missing_count": len(path_missing),
        "workload_dir_missing_sample": path_missing[:30],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(OUT)
    print(json.dumps({k: report[k] for k in report if k.endswith("_count")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
