#!/usr/bin/env python3
"""CI gate: dashboard must report linux, macos, and windows (never linux-only)."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.toml"
SUMMARY = ROOT / "data/latest/summary.json"

REQUIRED_PLATFORMS = ("linux", "macos", "windows")


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


def chart_os_set(summary: dict) -> set[str]:
    oss: set[str] = set()
    for cat in summary.get("categories", {}).values():
        for ch in cat.get("charts", []):
            os_tag = ch.get("os")
            if os_tag:
                oss.add(str(os_tag).lower())
    return oss


def main() -> int:
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
    row_os = Counter(str(r.get("os", "")).lower() for r in rows if r.get("os"))

    for plat in REQUIRED_PLATFORMS:
        if row_os.get(plat, 0) < 1:
            fail(f"summary.rows has no rows for os={plat!r}")

    tier01 = [
        r
        for r in rows
        if isinstance(r, dict) and r.get("tier") in (0, 1, "0", "1")
    ]
    tier01_os = {str(r.get("os", "")).lower() for r in tier01 if r.get("os")}
    for plat in ("macos", "windows"):
        if plat not in tier01_os:
            fail(f"tier 0/1 summary rows missing os={plat!r}")

    chart_oss = chart_os_set(summary)
    for plat in REQUIRED_PLATFORMS:
        if plat not in chart_oss:
            fail(f"summary charts missing os={plat!r}")

    os_values = summary.get("reporting", {}).get("os_values") or []
    normalized = [str(v).lower() for v in os_values]
    for plat in REQUIRED_PLATFORMS:
        if plat not in normalized and plat not in chart_oss:
            fail(f"reporting.os_values missing {plat!r}")

    print(
        "PASS check-reporting-platforms "
        f"(catalog platforms={list(platforms)}, "
        f"row_os={dict(row_os)}, tier01_os={sorted(tier01_os)}, chart_os={sorted(chart_oss)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
