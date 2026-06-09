"""plan-completion-audit catalog gap split (PH-5b / #266)."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_audit_module():
    path = ROOT / "scripts/plan-completion-audit.py"
    spec = importlib.util.spec_from_file_location("plan_completion_audit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class PlanCompletionAuditCatalogTests(unittest.TestCase):
    def test_audit_json_has_catalog_gap_split(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/plan-completion-audit.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)
        report = json.loads((ROOT / "data/latest/plan-completion-audit.json").read_text())
        summary = report["summary"]
        self.assertIn("catalog_gaps_actionable", summary)
        self.assertIn("catalog_gaps_repo_mismatch", summary)
        self.assertIn("lic_present", report["roots"])
        self.assertIn("benchmarks_root", report["roots"])
        self.assertEqual(summary["catalog_gaps_actionable"], 0)
        self.assertEqual(summary["catalog_gaps_repo_mismatch"], 0)

    def test_repo_mismatch_detected_when_lic_repo_points_at_benchmarks_path(self):
        mod = load_audit_module()
        with tempfile.TemporaryDirectory() as tmp:
            bench_root = Path(tmp) / "bench"
            workloads = bench_root / "benchmarks/workloads/tier1_micro/demo_gap"
            workloads.mkdir(parents=True)
            catalog = bench_root / "catalog.toml"
            catalog.write_text(
                '\n'.join(
                    [
                        '[[benchmark]]',
                        'id = "demo_gap"',
                        'repo = "lic"',
                        'path = "benchmarks/workloads/tier1_micro/demo_gap"',
                        'tier = 1',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            old_root = mod.ROOT
            old_lic = mod.LIC
            try:
                mod.ROOT = bench_root
                mod.LIC = bench_root.parent / "missing-lic"
                _, actionable, repo_mismatch = mod.catalog_gap_analysis()
                self.assertEqual(len(actionable), 0)
                self.assertEqual(len(repo_mismatch), 1)
                self.assertIn("repo=lic but path exists under benchmarks", repo_mismatch[0]["item"])
            finally:
                mod.ROOT = old_root
                mod.LIC = old_lic


if __name__ == "__main__":
    unittest.main()
