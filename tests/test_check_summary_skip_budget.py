"""check-summary-skip-budget.py — block hundreds of skip rows on committed summary."""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check-summary-skip-budget.py"


def load_gate():
    spec = importlib.util.spec_from_file_location("check_summary_skip_budget", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


class CheckSummarySkipBudgetTests(unittest.TestCase):
    def test_committed_summary_within_skip_budget(self):
        summary_path = ROOT / "data/latest/summary.json"
        if not summary_path.is_file():
            self.skipTest("summary.json missing")
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        rows = summary.get("rows") or []
        skip = sum(1 for r in rows if r.get("status") == "skip")
        linux_skip = sum(
            1 for r in rows if r.get("os") == "linux" and r.get("status") == "skip"
        )
        self.assertLessEqual(skip, 100)
        self.assertEqual(linux_skip, 0)


if __name__ == "__main__":
    unittest.main()
