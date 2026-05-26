"""tier_db_registry — layout validation and SQLite stub harness smoke."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIER_ROOT = ROOT / "benchmarks/tier_db_registry"
HARNESS = TIER_ROOT / "harness/registry_oltp_stub.py"
RUN_SCRIPT = ROOT / "scripts/run-db-registry-bench.sh"
MANIFEST = ROOT / "data/latest/tier-db-registry.json"


class TierDbRegistryTests(unittest.TestCase):
    def test_registry_oltp_stub_validate_only(self):
        proc = subprocess.run(
            [sys.executable, str(HARNESS), "--validate-only"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)

    def test_run_db_registry_bench_ci_stub(self):
        proc = subprocess.run(
            ["bash", str(RUN_SCRIPT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "BENCH_DB_REGISTRY_PROFILE": "ci"},
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        self.assertTrue(MANIFEST.is_file())
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(data["tier"], "tier_db_registry")
        self.assertEqual(data["status"], "stub")
        self.assertIn("PH-DB-5", data["ph_plan"])
        self.assertEqual(len(data["scenarios"]), 3)

    def test_registry_oltp_stub_timing_writes_csv(self):
        proc = subprocess.run(
            [sys.executable, str(HARNESS), "--profile", "ci", "--run-timing"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        csv_path = TIER_ROOT / "results/latest.csv"
        self.assertTrue(csv_path.is_file())
        lines = csv_path.read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(lines), 4)


if __name__ == "__main__":
    unittest.main()
