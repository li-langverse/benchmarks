"""check-reporting-platforms.py — catalog must list linux, macos, windows."""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check-reporting-platforms.py"


def load_gate():
    spec = importlib.util.spec_from_file_location("check_reporting_platforms", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


class CheckReportingPlatformsTests(unittest.TestCase):
    def test_catalog_lists_three_platforms(self):
        mod = load_gate()
        self.assertEqual(
            mod.load_reporting_platforms(),
            ["linux", "macos", "windows"],
        )

    def test_committed_summary_has_macos_windows_rows(self):
        summary_path = ROOT / "data/latest/summary.json"
        if not summary_path.is_file():
            self.skipTest("summary.json missing")
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        rows = summary.get("rows") or []
        os_seen = {str(r.get("os", "")).lower() for r in rows}
        for need in ("linux", "macos", "windows"):
            self.assertIn(need, os_seen, msg=f"missing summary row for os={need}")


if __name__ == "__main__":
    unittest.main()
