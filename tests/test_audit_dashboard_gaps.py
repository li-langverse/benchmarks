"""audit-dashboard-gaps — P0 gate on committed summary.json."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AuditDashboardGapsTests(unittest.TestCase):
    def test_committed_summary_has_zero_p0_gaps(self):
        script = ROOT / "scripts/audit-dashboard-gaps.py"
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            proc.returncode,
            0,
            msg=(proc.stdout or "") + (proc.stderr or ""),
        )


if __name__ == "__main__":
    unittest.main()
