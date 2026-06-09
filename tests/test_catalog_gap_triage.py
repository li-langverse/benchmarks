"""catalog-gap-triage and plan-completion-audit catalog path resolution."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CatalogGapTriageTests(unittest.TestCase):
    def test_triage_script_writes_json(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/catalog-gap-triage.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        out = ROOT / "data/latest/catalog-gap-triage.json"
        self.assertTrue(out.is_file())
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertIn("summary", data)
        self.assertIn("buckets", data)

    def test_plan_audit_catalog_gaps_actionable_field(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/plan-completion-audit.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            env={
                **__import__("os").environ,
                "LIC_ROOT": str(ROOT.parent / "lic"),
            },
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        audit = json.loads((ROOT / "data/latest/plan-completion-audit.json").read_text())
        summary = audit["summary"]
        self.assertIn("catalog_gaps_actionable", summary)
        self.assertIn("catalog_gaps_path_missing", summary)
        self.assertLessEqual(
            summary["catalog_gaps_actionable"],
            summary.get("catalog_gaps", summary["catalog_gaps_actionable"]) + 1,
        )


if __name__ == "__main__":
    unittest.main()
