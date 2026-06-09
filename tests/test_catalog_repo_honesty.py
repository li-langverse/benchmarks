"""catalog repo honesty — triage script and audit path resolution."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIAGE = ROOT / "scripts/catalog/triage-catalog-repo-honesty.py"


def load_triage():
    spec = importlib.util.spec_from_file_location("triage_catalog", TRIAGE)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class CatalogRepoHonestyTests(unittest.TestCase):
    def test_should_defer_competitive_stub_remap(self):
        mod = load_triage()
        self.assertTrue(
            mod.should_defer_stub("bio_proteinmpnn", "benchmarks/workloads/tier1_micro/num_sparse_mv")
        )
        self.assertFalse(
            mod.should_defer_stub("num_sparse_mv", "benchmarks/workloads/tier1_micro/num_sparse_mv")
        )
        self.assertFalse(
            mod.should_defer_stub(
                "matmul_naive_N1024", "benchmarks/workloads/tier1_micro/matmul_naive"
            )
        )

    def test_triage_dry_run_exits_zero(self):
        proc = subprocess.run(
            [sys.executable, str(TRIAGE), "--dry-run"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)


if __name__ == "__main__":
    unittest.main()
