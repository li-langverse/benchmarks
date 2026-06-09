"""plan-completion-audit catalog gap split (PH-5b / #266)."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PlanCompletionCatalogGapsTests(unittest.TestCase):
    def test_audit_emits_actionable_and_repo_mismatch_fields(self):
        script = ROOT / "scripts/plan-completion-audit.py"
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "LIC_ROOT": str(ROOT.parent / "lic")},
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)
        audit_path = ROOT / "data/latest/plan-completion-audit.json"
        data = json.loads(audit_path.read_text())
        summary = data["summary"]
        for key in (
            "catalog_gaps",
            "catalog_gaps_actionable",
            "catalog_gaps_repo_mismatch",
        ):
            self.assertIn(key, summary, msg=f"missing summary.{key}")
        self.assertIn("catalog_gaps_actionable", data)
        self.assertIn("lic_present", data)
        self.assertIn("benchmarks_root", data)

    def test_catalog_no_bogus_bio_proteinmpnn_remap(self):
        import tomllib

        catalog = tomllib.loads((ROOT / "catalog.toml").read_text())
        by_id = {b["id"]: b for b in catalog.get("benchmark", [])}
        row = by_id["bio_proteinmpnn"]
        self.assertEqual(row.get("repo"), "benchmarks")
        self.assertIn("bio_proteinmpnn", row.get("path", ""))
        self.assertNotIn("num_sparse_mv", row.get("path", ""))


if __name__ == "__main__":
    unittest.main()
