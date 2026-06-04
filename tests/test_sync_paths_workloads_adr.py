"""sync-paths-from-lic-tree benchmarks/workloads ADR (PH-5b / #266 sub-phase E)."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_sync_module():
    path = ROOT / "scripts/catalog/sync-paths-from-lic-tree.py"
    spec = importlib.util.spec_from_file_location("sync_paths", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class SyncPathsWorkloadsAdrTests(unittest.TestCase):
    def test_scan_prefers_benchmarks_workloads_without_lic(self):
        mod = load_sync_module()
        with tempfile.TemporaryDirectory() as tmp:
            bench = Path(tmp) / "bench"
            harness = bench / "benchmarks/workloads/tier1_micro/demo_sync"
            harness.mkdir(parents=True)
            index = mod.scan_harness_index(None, bench_root=bench, include_legacy_lic=False)
            self.assertIn("demo_sync", index)
            self.assertTrue(index["demo_sync"].startswith("benchmarks/workloads/"))

    def test_path_exists_under_bench_root_only(self):
        mod = load_sync_module()
        with tempfile.TemporaryDirectory() as tmp:
            bench = Path(tmp) / "bench"
            rel = "benchmarks/workloads/tier1_micro/demo_exists"
            (bench / rel).mkdir(parents=True)
            self.assertTrue(
                mod.path_exists(rel, bench_root=bench, lic_root=bench.parent / "no-lic")
            )


if __name__ == "__main__":
    unittest.main()
