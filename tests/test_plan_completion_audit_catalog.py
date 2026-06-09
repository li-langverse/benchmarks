#!/usr/bin/env python3
"""Tests for plan-completion-audit catalog gap classification."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts" / "plan-completion-audit.py"


def load_audit_module():
    spec = importlib.util.spec_from_file_location("plan_completion_audit", AUDIT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["plan_completion_audit"] = mod
    spec.loader.exec_module(mod)
    return mod


class CatalogGapScanTests(unittest.TestCase):
    def test_repo_mismatch_when_path_under_benchmarks(self) -> None:
        mod = load_audit_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workloads = root / "benchmarks" / "workloads" / "tier1_micro" / "foo"
            workloads.mkdir(parents=True)
            catalog = root / "catalog.toml"
            catalog.write_text(
                '[[benchmark]]\n'
                'id = "foo"\n'
                'repo = "lic"\n'
                'path = "benchmarks/workloads/tier1_micro/foo"\n',
                encoding="utf-8",
            )
            old_root = mod.ROOT
            old_lic = mod.LIC
            try:
                mod.ROOT = root
                mod.LIC = root / "missing-lic"
                all_gaps, actionable, mismatch = mod.catalog_gap_scan()
                self.assertEqual(len(mismatch), 1)
                self.assertEqual(mismatch[0]["kind"], "repo_mismatch")
                self.assertEqual(len(actionable), 0)
                self.assertEqual(len(all_gaps), 1)
            finally:
                mod.ROOT = old_root
                mod.LIC = old_lic


if __name__ == "__main__":
    unittest.main()
