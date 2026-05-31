"""table_sota_display — table shows li when Li beats best competitor."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INGEST = ROOT / "scripts/ingest"
sys.path.insert(0, str(INGEST))

spec = importlib.util.spec_from_file_location("build_summary", INGEST / "build_summary.py")
bs = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(bs)


class TableSotaDisplayTests(unittest.TestCase):
    def test_li_wins_lower_is_better(self):
        lang, val = bs.table_sota_display(1.0, "cpp", 2.0, lower_is_better=True)
        self.assertEqual(lang, "li")
        self.assertEqual(val, 1.0)

    def test_competitor_wins_lower_is_better(self):
        lang, val = bs.table_sota_display(3.0, "cpp", 2.0, lower_is_better=True)
        self.assertEqual(lang, "cpp")
        self.assertEqual(val, 2.0)

    def test_li_wins_higher_is_better(self):
        lang, val = bs.table_sota_display(200.0, "rust", 100.0, lower_is_better=False)
        self.assertEqual(lang, "li")
        self.assertEqual(val, 200.0)

    def test_tie_stays_competitor(self):
        lang, val = bs.table_sota_display(2.0, "cpp", 2.0, lower_is_better=True)
        self.assertEqual(lang, "cpp")
        self.assertEqual(val, 2.0)


if __name__ == "__main__":
    unittest.main()
