#!/usr/bin/env python3
"""Merge per-OS benchmark CSV artifacts into lic benchmarks/results/latest.csv."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

# Later paths win on duplicate (benchmark, lang, variant, metric, os) keys.
DEFAULT_ORDER = ("linux", "macos", "windows")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return [], []
        return list(reader.fieldnames), list(reader)


def merge_into(
    header: list[str],
    rows: list[dict[str, str]],
    new_header: list[str],
    new_rows: list[dict[str, str]],
) -> None:
    if not new_rows:
        return
    for col in new_header:
        if col not in header:
            header.append(col)
    key_cols = [c for c in ("benchmark", "lang", "variant", "metric", "os") if c in header]
    index = {
        tuple(row.get(c, "") for c in key_cols): i
        for i, row in enumerate(rows)
    }
    for row in new_rows:
        key = tuple(row.get(c, "") for c in key_cols)
        normalized = {c: row.get(c, "") for c in header}
        if key in index:
            rows[index[key]] = normalized
        else:
            rows.append(normalized)


def main() -> int:
    if len(sys.argv) < 3:
        print(
            "usage: merge_bench_csv_artifacts.py <out.csv> <linux.csv> [macos.csv] [windows.csv]",
            file=sys.stderr,
        )
        return 2
    out = Path(sys.argv[1])
    inputs = [Path(p) for p in sys.argv[2:] if Path(p).is_file()]
    if not inputs:
        print("no input CSV files", file=sys.stderr)
        return 1

    header: list[str] = []
    rows: list[dict[str, str]] = []
    for path in inputs:
        h, r = read_csv(path)
        merge_into(header, rows, h, r)
        print(f"merged {path.name}: +{len(r)} rows", file=sys.stderr)

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out} ({len(rows)} rows)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
