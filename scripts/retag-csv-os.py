#!/usr/bin/env python3
"""Rewrite os column on a benchmark CSV (nightly per-OS merge shards)."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("csv", type=Path)
    p.add_argument("--os", required=True)
    args = p.parse_args()
    rows = list(csv.DictReader(args.csv.open(encoding="utf-8")))
    if not rows:
        print(f"retag-csv-os: empty {args.csv}", file=sys.stderr)
        return 1
    fieldnames = list(rows[0].keys())
    if "os" not in fieldnames:
        print("retag-csv-os: no os column", file=sys.stderr)
        return 1
    for row in rows:
        row["os"] = args.os
    with args.csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"retag-csv-os: {args.csv} ({len(rows)} rows -> os={args.os})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
