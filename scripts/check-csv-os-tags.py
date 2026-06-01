#!/usr/bin/env python3
"""CI gate: per-OS benchmark CSV must tag rows with the runner OS (not stale linux)."""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

ALIASES = {
    "darwin": "macos",
    "osx": "macos",
    "macos": "macos",
    "linux": "linux",
    "windows": "windows",
    "win32": "windows",
}


def normalize_os(raw: str | None) -> str:
    if not raw:
        return "unknown"
    return ALIASES.get(raw.strip().lower(), raw.strip().lower())


def fail(msg: str) -> None:
    print(f"check-csv-os-tags: FAIL {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("csv", type=Path)
    p.add_argument("--expect-os", required=True)
    p.add_argument("--min-rows", type=int, default=20)
    args = p.parse_args()

    expect = normalize_os(args.expect_os)
    if expect == "unknown":
        fail(f"unsupported --expect-os {args.expect_os!r}")

    if not args.csv.is_file():
        fail(f"missing {args.csv}")

    rows = list(csv.DictReader(args.csv.open(encoding="utf-8")))
    if len(rows) < args.min_rows:
        fail(f"{len(rows)} rows < min_rows {args.min_rows}")

    tags = Counter(normalize_os(r.get("os")) for r in rows)
    wrong = {os: n for os, n in tags.items() if os != expect and os != "unknown"}
    if wrong:
        fail(f"expected all rows os={expect}, got distribution {dict(tags)}")

    print(
        f"PASS check-csv-os-tags ({args.csv.name}: {len(rows)} rows, os={expect})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
