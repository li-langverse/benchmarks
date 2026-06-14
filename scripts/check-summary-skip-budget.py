#!/usr/bin/env python3
"""Fail CI when summary.json has too many skip rows (empty benchmark pages)."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/latest/summary.json"

# No synthetic platform skip rows — only measured OS from merged nightly CSV.
MAX_TOTAL_SKIP_ROWS = 0
MAX_LINUX_SKIP_ROWS = 0
MIN_LINUX_GREEN_ROWS = 130
MAX_LINUX_UNKNOWN_ROWS = 15


def fail(msg: str) -> None:
    print(f"check-summary-skip-budget: FAIL {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    if not SUMMARY.is_file():
        fail(f"missing {SUMMARY}")

    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    rows = summary.get("rows") or []
    if not rows:
        fail("summary.rows is empty")

    by_os: dict[str, list[dict]] = {}
    for row in rows:
        by_os.setdefault(str(row.get("os") or "unknown"), []).append(row)

    skip_total = sum(1 for r in rows if r.get("status") == "skip")
    linux = by_os.get("linux", [])
    linux_skip = sum(1 for r in linux if r.get("status") == "skip")
    linux_green = sum(1 for r in linux if r.get("status") == "green")
    # Tier 6+ catalog stubs (db/gpu/registry) may stay unknown until harness runs.
    linux_unknown = sum(
        1
        for r in linux
        if r.get("status") == "unknown" and int(r.get("tier") or 99) <= 5
    )

    if skip_total > MAX_TOTAL_SKIP_ROWS:
        fail(
            f"{skip_total} skip rows > budget {MAX_TOTAL_SKIP_ROWS} "
            f"(by_os skip={ {os: sum(1 for r in rs if r.get('status')=='skip') for os, rs in by_os.items()} })"
        )
    if linux_skip > MAX_LINUX_SKIP_ROWS:
        fail(f"{linux_skip} linux skip rows > {MAX_LINUX_SKIP_ROWS}")
    if linux_green < MIN_LINUX_GREEN_ROWS:
        fail(f"{linux_green} linux green rows < {MIN_LINUX_GREEN_ROWS}")
    if linux_unknown > MAX_LINUX_UNKNOWN_ROWS:
        fail(f"{linux_unknown} linux unknown rows > {MAX_LINUX_UNKNOWN_ROWS}")

    charts = [
        ch
        for cat in summary.get("categories", {}).values()
        for ch in cat.get("charts", [])
    ]
    linux_charts = [
        ch
        for ch in charts
        if ch.get("os") in (None, "linux") or str(ch.get("id", "")).endswith("@linux")
    ]
    with_series = sum(1 for ch in linux_charts if ch.get("series"))
    if with_series < MIN_LINUX_GREEN_ROWS:
        fail(f"only {with_series} linux charts have series (need >= {MIN_LINUX_GREEN_ROWS})")

    print(
        "PASS check-summary-skip-budget "
        f"(skip_total={skip_total}, linux_green={linux_green}, "
        f"linux_unknown={linux_unknown}, linux_charts_with_series={with_series})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
