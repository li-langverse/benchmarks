#!/usr/bin/env python3
"""Regression: tier-0 stability resolves tier2 via harness.paths (post-split layout)."""

from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "harness"
WORKLOADS = ROOT / "benchmarks" / "workloads"


class HarnessPathsTest(unittest.TestCase):
    def test_tier_dirs_prefers_benchmarks_workloads(self) -> None:
        sys.path.insert(0, str(HARNESS))
        try:
            import paths as paths_mod  # noqa: PLC0415
        finally:
            sys.path.pop(0)
        t1, t1s, t2 = paths_mod.tier_dirs()
        self.assertTrue((WORKLOADS / "tier1_micro").is_dir())
        self.assertEqual(t1, WORKLOADS / "tier1_micro")
        self.assertEqual(t1s, WORKLOADS / "tier1_stdlib")
        self.assertEqual(t2, WORKLOADS / "tier2_physics")

    def test_stability_md_dir_uses_tier_dirs(self) -> None:
        stability = (HARNESS / "stability.py").read_text()
        self.assertIn("tier_dirs()", stability)
        self.assertNotIn("lic/benchmarks/tier2_physics", stability)
        tree = ast.parse(stability)
        assigns = {
            node.targets[0].id: node
            for node in tree.body
            if isinstance(node, ast.Assign)
            and isinstance(node.targets[0], ast.Name)
        }
        md_assign = assigns.get("MD_DIR")
        self.assertIsNotNone(md_assign)
        src = ast.get_source_segment(stability, md_assign) or ""
        self.assertIn("TIER2", src)
        self.assertIn("md_lennard_jones", src)


if __name__ == "__main__":
    unittest.main()
