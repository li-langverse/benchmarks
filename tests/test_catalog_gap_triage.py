"""catalog-gap-triage — PH-5b competitive vertical stub honesty."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/catalog"


def _load_gap_policy():
    path = SCRIPTS / "gap_policy.py"
    spec = importlib.util.spec_from_file_location("gap_policy", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class CatalogGapPolicyTests(unittest.TestCase):
    def setUp(self):
        self.gap_policy = _load_gap_policy()

    def test_bogus_bio_remap_detected(self):
        self.assertTrue(
            self.gap_policy.is_bogus_competitive_remap(
                "bio_proteinmpnn",
                "benchmarks/workloads/tier1_micro/num_sparse_mv",
            )
        )

    def test_honest_tier2_path_not_bogus(self):
        self.assertFalse(
            self.gap_policy.is_bogus_competitive_remap(
                "qm_dft_scf_energy",
                "benchmarks/workloads/tier2_physics/qm_dft_scf_energy",
            )
        )

    def test_triage_script_writes_json(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "catalog-gap-triage.py"), "--lic-root", "/tmp"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        out = ROOT / "data/latest/catalog-gap-triage.json"
        self.assertTrue(out.is_file())
        data = json.loads(out.read_text())
        self.assertIn("bogus_remap", data["summary"])
        self.assertIsInstance(data["summary"]["bogus_remap"], list)
        self.assertIn("lic_impl", data["summary"])


class CatalogHonestyAppliedTests(unittest.TestCase):
    def test_bio_stub_rows_use_unknown_path(self):
        import tomllib

        catalog = tomllib.loads((ROOT / "catalog.toml").read_text())
        by_id = {b["id"]: b for b in catalog["benchmark"]}
        row = by_id["bio_proteinmpnn"]
        self.assertEqual(row.get("path"), "unknown")
        self.assertEqual(row.get("catalog_lifecycle"), "planned")

    def test_matmul_blocked_stays_active(self):
        import tomllib

        catalog = tomllib.loads((ROOT / "catalog.toml").read_text())
        by_id = {b["id"]: b for b in catalog["benchmark"]}
        row = by_id["matmul_blocked"]
        self.assertNotEqual(row.get("catalog_lifecycle"), "planned")
        self.assertIn("matmul_blocked", row.get("path", ""))


if __name__ == "__main__":
    unittest.main()
