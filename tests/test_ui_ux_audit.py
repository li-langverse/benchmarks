"""ui-ux-audit preflight — lic-docs + benchmarks-dashboard rows."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class UiUxAuditTests(unittest.TestCase):
    def test_preflight_writes_ui_audit_with_benchmarks_dashboard(self) -> None:
        agents = Path(os.environ.get("LI_CURSOR_AGENTS_ROOT", ROOT.parent / "li-cursor-agents"))
        if not (agents / "ux-harness" / "run_audit.py").is_file():
            self.skipTest("li-cursor-agents sibling clone not present")

        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/ui-ux-audit.py"), "--preflight"],
            cwd=ROOT,
            env={**os.environ, "LI_CURSOR_AGENTS_ROOT": str(agents)},
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, (proc.stdout or "") + (proc.stderr or ""))

        audit_path = ROOT / "data/latest/ui-audit.json"
        self.assertTrue(audit_path.is_file(), msg=proc.stderr)
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        ids = {t.get("target_id") for t in payload.get("targets") or []}
        self.assertIn("lic-docs", ids)
        self.assertIn("benchmarks-dashboard", ids)
        bench = next(t for t in payload["targets"] if t["target_id"] == "benchmarks-dashboard")
        self.assertEqual(bench.get("status"), "pass")


if __name__ == "__main__":
    unittest.main()
