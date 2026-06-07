"""PH-5b catalog honesty — triage and audit actionable gap counts."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CatalogHonestyPh5bTests(unittest.TestCase):
    def test_gap_triage_writes_json(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/catalog-gap-triage.py")],
            cwd=ROOT,
            env={**__import__("os").environ, "LIC_ROOT": str(ROOT.parent / "lic")},
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        out = ROOT / "data/latest/catalog-gap-triage.json"
        self.assertTrue(out.is_file())
        data = json.loads(out.read_text())
        self.assertEqual(data["schema"], "benchmarks/catalog-gap-triage/v1")
        self.assertIn("summary", data)

    def test_plan_audit_includes_ph5b_summary_keys(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/plan-completion-audit.py")],
            cwd=ROOT,
            env={**__import__("os").environ, "LIC_ROOT": str(ROOT.parent / "lic")},
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        audit = json.loads((ROOT / "data/latest/plan-completion-audit.json").read_text())
        summary = audit["summary"]
        self.assertIn("catalog_gaps_actionable", summary)


if __name__ == "__main__":
    unittest.main()
