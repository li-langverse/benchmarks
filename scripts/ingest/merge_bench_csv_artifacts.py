#!/usr/bin/env python3
"""Merge per-OS benchmark CSV artifacts into lic benchmarks/results/latest.csv."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

# Later paths win on duplicate (benchmark, lang, variant, metric, os) keys.
DEFAULT_ORDER = ("linux", "macos", "windows")


def read_csv(path: Path, *, force_os: str | None = None) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return [], []
        rows = list(reader)
        if force_os:
            for row in rows:
                row["os"] = force_os
        return list(reader.fieldnames), rows


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
            "usage: merge_bench_csv_artifacts.py <out.csv> [linux.csv|linux:path] [macos:path] ...",
            file=sys.stderr,
        )
        return 2
    out = Path(sys.argv[1])
    raw_inputs = sys.argv[2:]
    if not raw_inputs:
        print("no input CSV files", file=sys.stderr)
        return 1

    header: list[str] = []
    rows: list[dict[str, str]] = []
    for spec in raw_inputs:
        force_os: str | None = None
        path_s = spec
        if ":" in spec and not spec.endswith(".csv"):
            force_os, path_s = spec.split(":", 1)
        elif spec.count(":") == 1 and ".csv" in spec:
            force_os, path_s = spec.rsplit(":", 1)
        path = Path(path_s)
        if not path.is_file():
            print(f"skip missing {path_s}", file=sys.stderr)
            continue
        h, r = read_csv(path, force_os=force_os)
        merge_into(header, rows, h, r)
        tag = f" (os={force_os})" if force_os else ""
        print(f"merged {path.name}: +{len(r)} rows{tag}", file=sys.stderr)

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out} ({len(rows)} rows)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
