#!/usr/bin/env python3
"""CI gate: multi-OS nightly ingest must include measured charts per platform."""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.toml"
SUMMARY = ROOT / "data/latest/summary.json"

REQUIRED_PLATFORMS = ("linux", "macos", "windows")
MIN_MEASURED_CHARTS_PER_OS = 10


def fail(msg: str) -> None:
    print(f"check-reporting-platforms: FAIL {msg}", file=sys.stderr)
    sys.exit(1)


def load_reporting_platforms() -> list[str]:
    import tomllib

    if not CATALOG.is_file():
        fail(f"missing {CATALOG}")
    catalog = tomllib.loads(CATALOG.read_text(encoding="utf-8"))
    raw = catalog.get("reporting", {}).get("platforms")
    if not raw:
        fail("[reporting].platforms missing in catalog.toml")
    return [str(p).strip().lower() for p in raw]


def charts_with_series(summary: dict) -> list[dict]:
    return [
        ch
        for cat in summary.get("categories", {}).values()
        for ch in cat.get("charts", [])
        if ch.get("series")
    ]


def main() -> int:
    strict = os.environ.get("MULTI_OS_STRICT", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )
    platforms = load_reporting_platforms()
    if platforms != list(REQUIRED_PLATFORMS):
        fail(
            f"[reporting].platforms must be {list(REQUIRED_PLATFORMS)!r}, "
            f"got {platforms!r} (do not collapse to linux-only)"
        )

    if not SUMMARY.is_file():
        fail(f"missing {SUMMARY} (run ingest after changing platforms)")

    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    rows = summary.get("rows") or []
    measured = charts_with_series(summary)
    measured_by_os = Counter(str(ch.get("os", "")).lower() for ch in measured)
    row_os = Counter(str(r.get("os", "")).lower() for r in rows if r.get("os"))

    skip_platform = [
        r
        for r in rows
        if r.get("status") == "skip"
        and r.get("validity_source") == "platform_not_measured"
    ]
    if skip_platform:
        fail(
            f"{len(skip_platform)} platform_not_measured skip rows remain "
            f"(merge linux+macos+windows CSV before ingest; do not emit skip placeholders)"
        )

    os_values = summary.get("reporting", {}).get("os_values") or []
    normalized = [str(v).lower() for v in os_values]

    if strict:
        for plat in REQUIRED_PLATFORMS:
            n = measured_by_os.get(plat, 0)
            if n < MIN_MEASURED_CHARTS_PER_OS:
                fail(
                    f"measured charts for os={plat!r}: {n} < {MIN_MEASURED_CHARTS_PER_OS}"
                )
            if row_os.get(plat, 0) < 1:
                fail(f"summary.rows has no rows for os={plat!r}")
            if plat not in normalized and plat not in measured_by_os:
                fail(f"reporting.os_values missing {plat!r}")

    print(
        "PASS check-reporting-platforms "
        f"(strict={strict}, catalog platforms={list(platforms)}, "
        f"measured_by_os={dict(measured_by_os)}, row_os={dict(row_os)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
