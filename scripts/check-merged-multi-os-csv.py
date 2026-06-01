#!/usr/bin/env python3
"""CI gate: merged latest.csv must include measured rows for linux, macos, and windows."""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REQUIRED = ("linux", "macos", "windows")
MIN_ROWS_PER_OS = 20
MIN_BENCHMARKS_PER_OS = 10


def fail(msg: str) -> None:
    print(f"check-merged-multi-os-csv: FAIL {msg}", file=sys.stderr)
    sys.exit(1)


def normalize_os(raw: str | None) -> str:
    if not raw:
        return "unknown"
    os = raw.strip().lower()
    if os in ("darwin", "osx"):
        return "macos"
    return os


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "results/latest.csv")
    if not path.is_file():
        fail(f"missing {path}")

    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    if not rows:
        fail("CSV is empty")

    by_os: dict[str, list[dict[str, str]]] = {os: [] for os in REQUIRED}
    for row in rows:
        os = normalize_os(row.get("os"))
        if os in by_os:
            by_os[os].append(row)

    for os in REQUIRED:
        subset = by_os[os]
        if len(subset) < MIN_ROWS_PER_OS:
            fail(f"os={os}: {len(subset)} rows < {MIN_ROWS_PER_OS}")
        benches = {r["benchmark"] for r in subset if r.get("benchmark")}
        if len(benches) < MIN_BENCHMARKS_PER_OS:
            fail(f"os={os}: {len(benches)} benchmarks < {MIN_BENCHMARKS_PER_OS}")

    dist = Counter(normalize_os(r.get("os")) for r in rows)
    print(
        "PASS check-merged-multi-os-csv "
        f"({len(rows)} rows, per_os={{{', '.join(f'{k}={dist[k]}' for k in REQUIRED)}}})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
