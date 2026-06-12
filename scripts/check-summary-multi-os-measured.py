#!/usr/bin/env python3
"""CI gate: summary must include measured macOS/Windows charts, not only skip placeholders."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/latest/summary.json"
MIN_OS_CHARTS_WITH_SERIES = 10


def fail(msg: str) -> None:
    print(f"check-summary-multi-os-measured: FAIL {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    if not SUMMARY.is_file():
        fail(f"missing {SUMMARY}")

    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    charts = [
        ch
        for cat in summary.get("categories", {}).values()
        for ch in cat.get("charts", [])
    ]

    def count_series(os_name: str) -> int:
        return sum(
            1
            for ch in charts
            if ch.get("os") == os_name and ch.get("series")
        )

    linux_n = count_series("linux")
    macos_n = count_series("macos")
    windows_n = count_series("windows")

    linux_only = os.environ.get("MULTI_OS_LINUX_ONLY", "").strip() in ("1", "true", "yes")
    skip_windows = linux_only or os.environ.get("MULTI_OS_SKIP_WINDOWS", "").strip() in (
        "1",
        "true",
        "yes",
    )
    skip_macos = linux_only or os.environ.get("MULTI_OS_SKIP_MACOS", "").strip() in (
        "1",
        "true",
        "yes",
    )

    if not skip_macos and macos_n < MIN_OS_CHARTS_WITH_SERIES:
        fail(f"macos charts with series={macos_n} < {MIN_OS_CHARTS_WITH_SERIES}")
    if not skip_windows and windows_n < MIN_OS_CHARTS_WITH_SERIES:
        fail(f"windows charts with series={windows_n} < {MIN_OS_CHARTS_WITH_SERIES}")
    if linux_only:
        print("check-summary-multi-os-measured: linux-only nightly (MULTI_OS_LINUX_ONLY=1)")
    elif skip_windows:
        print("check-summary-multi-os-measured: skip windows requirement (MULTI_OS_SKIP_WINDOWS=1)")

    print(
        "PASS check-summary-multi-os-measured "
        f"(linux={linux_n}, macos={macos_n}, windows={windows_n})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
