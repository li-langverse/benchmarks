"""build_summary — multi-platform skip charts and OS normalization."""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INGEST = ROOT / "scripts/ingest"
sys.path.insert(0, str(INGEST))

from build_summary import (  # noqa: E402
    PLATFORM_ORDER,
    build_platform_skip_chart,
    catalog_platforms,
    effective_size_meta,
    load_catalog_defaults,
    main,
    normalize_os,
)


class BuildSummaryPlatformTests(unittest.TestCase):
    def test_normalize_os_maps_darwin_to_macos(self):
        self.assertEqual(normalize_os("darwin"), "macos")
        self.assertEqual(normalize_os("Darwin"), "macos")
        self.assertEqual(normalize_os("linux"), "linux")

    def test_catalog_platforms_defaults(self):
        defaults = {"platforms": ["linux", "macos", "windows"]}
        self.assertEqual(catalog_platforms({}, defaults), list(PLATFORM_ORDER))

    def test_load_catalog_defaults_merges_reporting_section(self):
        defaults = load_catalog_defaults()
        self.assertEqual(defaults.get("platforms"), ["linux", "macos", "windows"])
        self.assertEqual(defaults.get("sota_policy"), "best_competitor_lang_excludes_li")

    def test_effective_size_meta_algo_registry_stub(self):
        cfg = {"size_label": "harness pending", "variant": "algo_registry"}
        meta = effective_size_meta(cfg, has_csv=False)
        self.assertEqual(meta["size_label"], "algo registry stub")

    def test_platform_skip_chart_has_skip_status(self):
        cfg = {
            "category": "micro",
            "metric": "wall_time",
            "repo": "lic",
            "path": "benchmarks/tier2_physics/foo",
            "size_label": "harness pending",
            "variant": "algo_registry",
            "tier": 1,
        }
        chart = build_platform_skip_chart("foo", cfg, "macos", multi=True)
        self.assertEqual(chart["os"], "macos")
        self.assertEqual(chart["status"], "skip")
        self.assertEqual(chart["validity_status"], "skip")
        self.assertEqual(chart["size_label"], "algo registry stub")
        self.assertEqual(chart["base_id"], "foo")

    def test_fixture_ingest_emits_three_os_charts_for_simd_dot(self):
        fixture_csv = INGEST / "fixtures/summary/lic.csv"
        summary_path = ROOT / "data/latest/summary.json"
        backup = summary_path.read_text(encoding="utf-8") if summary_path.is_file() else None
        prev = os.environ.get("BENCHMARKS_CSV")
        os.environ["BENCHMARKS_CSV"] = str(fixture_csv)
        try:
            lic_root = ROOT.parent / "lic"
            if not lic_root.is_dir():
                self.skipTest("lic sibling clone not present")
            rc = main()
            self.assertEqual(rc, 0)
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            charts = [
                ch
                for cat in summary.get("categories", {}).values()
                for ch in cat.get("charts", [])
                if (ch.get("base_id") or ch.get("id")) == "simd_dot"
                or ch.get("id", "").startswith("simd_dot")
            ]
            oss = {ch.get("os") for ch in charts}
            self.assertIn("linux", oss)
            self.assertIn("macos", oss)
            self.assertIn("windows", oss)
            linux = next(c for c in charts if c.get("os") == "linux")
            self.assertTrue(linux.get("series"))
            macos = next(c for c in charts if c.get("os") == "macos")
            self.assertEqual(macos.get("status"), "skip")
        finally:
            if backup is not None:
                summary_path.write_text(backup, encoding="utf-8")
            if prev is None:
                os.environ.pop("BENCHMARKS_CSV", None)
            else:
                os.environ["BENCHMARKS_CSV"] = prev


if __name__ == "__main__":
    unittest.main()
