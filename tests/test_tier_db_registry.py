"""tier_db_registry — layout validation and harness smoke."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIER_ROOT = ROOT / "benchmarks/tier_db_registry"
HARNESS = TIER_ROOT / "harness/registry_oltp.py"
HARNESS_STUB = TIER_ROOT / "harness/registry_oltp_stub.py"
RUN_SCRIPT = ROOT / "scripts/run-db-registry-bench.sh"
MANIFEST = ROOT / "data/latest/tier-db-registry.json"


class TierDbRegistryTests(unittest.TestCase):
    def test_registry_oltp_validate_only(self):
        proc = subprocess.run(
            [sys.executable, str(HARNESS), "--validate-only"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)

    def test_registry_oltp_stub_validate_only(self):
        proc = subprocess.run(
            [sys.executable, str(HARNESS_STUB), "--validate-only"],
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
            env={**os.environ, "BENCH_DB_REGISTRY_PROFILE": "ci"},
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        self.assertTrue(MANIFEST.is_file())
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(data["tier"], "tier_db_registry")
        self.assertEqual(data["status"], "stub")
        self.assertIn("PH-DB-5", data["ph_plan"])
        self.assertEqual(len(data["scenarios"]), 3)
        self.assertIn("registry_oltp.py", data["sources"]["harness_py"])

    def test_registry_oltp_stub_timing_writes_csv(self):
        proc = subprocess.run(
            [sys.executable, str(HARNESS_STUB), "--profile", "ci", "--run-timing"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        csv_path = TIER_ROOT / "results/latest.csv"
        self.assertTrue(csv_path.is_file())
        lines = csv_path.read_text(encoding="utf-8").strip().splitlines()
        self.assertGreaterEqual(len(lines), 4)

    def test_lidb_only_when_embed_available(self):
        lidb_root = ROOT.parent / "lidb"
        if not (lidb_root / "scripts" / "smoke.sh").is_file():
            self.skipTest("lidb repo not present")
        proc = subprocess.run(
            [
                sys.executable,
                str(HARNESS),
                "--profile",
                "ci",
                "--engine",
                "lidb_only",
                "--json-out",
                str(ROOT / "data/latest/tier-db-registry-harness-test.json"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            env={**os.environ, "LIDB_ROOT": str(lidb_root)},
            check=False,
        )
        if proc.returncode != 0 and "lidb_embed" in (proc.stderr + proc.stdout):
            self.skipTest("lidb_embed not built")
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        harness_path = ROOT / "data/latest/tier-db-registry-harness-test.json"
        self.assertTrue(harness_path.is_file())
        harness = json.loads(harness_path.read_text(encoding="utf-8"))
        self.assertEqual(harness["engine_mode"], "lidb_only")
        self.assertIn(harness["status"], ("unknown", "pass", "fail"))
        for sc in harness["scenarios"]:
            self.assertIsNotNone(sc["engines"].get("lidb"))


if __name__ == "__main__":
    unittest.main()
