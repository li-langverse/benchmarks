"""Completion gate — branch resolution for BN5 pre-merge polling."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE_SCRIPT = ROOT / "scripts/benchmark-nightly-green-gate.sh"


class BenchmarkNightlyGreenGateTests(unittest.TestCase):
    def test_gate_script_resolves_workflow_branch(self):
        text = GATE_SCRIPT.read_text(encoding="utf-8")
        self.assertIn("_resolve_gate_branch", text)
        self.assertIn("LI_REPO_WORKFLOW_BRANCH", text)
        self.assertIn('BENCHMARK_NIGHTLY_GATE_BRANCH:-', text)

    def test_gate_script_polls_merge_jobs_off_main(self):
        text = GATE_SCRIPT.read_text(encoding="utf-8")
        self.assertIn('bench-(linux|macos|windows)-merge', text)
        self.assertIn("publish-dashboard runs on main only", text)


if __name__ == "__main__":
    unittest.main()
