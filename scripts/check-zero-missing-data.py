#!/usr/bin/env python3
"""Fail CI when dashboard data has skips, CSV gaps, or catalog harness holes."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data/latest/zero-missing-data-report.json"
AUDIT_SCRIPT = ROOT / "scripts/catalog/audit-catalog-coverage.py"
REPORT_SCRIPT = ROOT / "scripts/audit/zero-missing-data-report.py"


def fail(msg: str) -> None:
    print(f"check-zero-missing-data: FAIL {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    if AUDIT_SCRIPT.is_file():
        subprocess.run([sys.executable, str(AUDIT_SCRIPT)], check=True, cwd=ROOT)

    subprocess.run([sys.executable, str(REPORT_SCRIPT)], cwd=ROOT)
    if not REPORT.is_file():
        fail(f"missing {REPORT}")

    report = json.loads(REPORT.read_text(encoding="utf-8"))
    blocking = report.get("blocking_counts") or {}
    bad = {k: v for k, v in blocking.items() if v}
    if bad:
        fail(
            "dashboard not zero-missing: "
            + ", ".join(f"{k}={v}" for k, v in bad.items())
            + f"; see {REPORT.relative_to(ROOT)}"
        )

    print("PASS check-zero-missing-data (0 blocking gaps)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
