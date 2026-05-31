#!/usr/bin/env python3
"""Fail CI when dashboard summary rows are skip."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data/latest/zero-missing-data-report.json"
REPORT_SCRIPT = ROOT / "scripts/audit/zero-missing-data-report.py"

def fail(msg: str) -> None:
    print(f"check-zero-missing-data: FAIL {msg}", file=sys.stderr)
    sys.exit(1)

def main() -> int:
    subprocess.run([sys.executable, str(REPORT_SCRIPT)], cwd=ROOT)
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    skip_rows = int(report.get("skip_row_count") or 0)
    if skip_rows:
        fail(f"{skip_rows} summary row(s) still skip")
    print("PASS check-zero-missing-data (0 skip rows in summary.json)")
    return 0

if __name__ == "__main__":
    sys.exit(main())