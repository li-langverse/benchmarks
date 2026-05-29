"""Smoke test for dashboard gap audit on committed summary.json."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_audit_dashboard_gaps_p0_zero() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/audit-dashboard-gaps.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = json.loads((ROOT / "data/latest/dashboard-gap-report.json").read_text())
    assert report["p0_count"] == 0
