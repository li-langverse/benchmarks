#!/usr/bin/env python3
"""Compare Li vs Python summary.json outputs (PH-IO-7 gate)."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def bench_ids(summary: dict) -> set[str]:
    return {r["benchmark"] for r in summary.get("rows", [])}


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: compare_summary_outputs.py <li.json> <py.json>", file=sys.stderr)
        return 2
    li_path = Path(sys.argv[1])
    py_path = Path(sys.argv[2])
    if not li_path.is_file() or not py_path.is_file():
        print("compare_summary: missing input file", file=sys.stderr)
        return 2
    li = load(li_path)
    py = load(py_path)
    li_ids = bench_ids(li)
    py_ids = bench_ids(py)
    missing = py_ids - li_ids
    extra = li_ids - py_ids
    if missing or extra:
        print(f"compare_summary: benchmark id mismatch missing={sorted(missing)} extra={sorted(extra)}")
        return 1
    mismatches = 0
    py_by = {r["benchmark"]: r for r in py.get("rows", [])}
    for row in li.get("rows", []):
        bid = row["benchmark"]
        other = py_by.get(bid)
        if other is None:
            continue
        if row.get("status") != other.get("status"):
            print(f"compare_summary: {bid} status li={row.get('status')} py={other.get('status')}")
            mismatches += 1
    if mismatches:
        print(f"compare_summary: {mismatches} status mismatch(es)")
        return 1
    print(f"compare_summary: ok ({len(li_ids)} benchmarks, statuses match)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
