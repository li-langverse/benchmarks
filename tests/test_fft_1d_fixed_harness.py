"""Tier-1 FFT micro-bench catalog + workload mirror (benchmarks#6 / #18)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness"))

from bench import TIER1_BENCHES  # noqa: E402


class Fft1dFixedHarnessTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    import tomllib

    cls.catalog = tomllib.loads((ROOT / "catalog.toml").read_text(encoding="utf-8"))
    cls.workload = ROOT / "benchmarks" / "workloads" / "tier1_micro" / "fft_1d_fixed"

  def _row(self, bench_id: str) -> dict:
    for row in self.catalog.get("benchmark", []):
      if row.get("id") == bench_id:
        return row
    self.fail(f"missing catalog row {bench_id}")

  def test_catalog_rows_active(self):
    for bench_id in ("fft_1d_fixed", "fft_1d_fixed_pure_li"):
      row = self._row(bench_id)
      self.assertNotEqual(row.get("catalog_lifecycle"), "planned")
      self.assertEqual(row.get("variant"), "fftw_reference" if bench_id == "fft_1d_fixed" else "pure_li")

  def test_workload_mirror_complete(self):
    required = (
      "common/fft_1d_fixed_core.c",
      "common/fft_1d_fixed_core.h",
      "cpp/main.c",
      "li/main.li",
      "li/main_pure.li",
      "harness.toml",
      "params.toml",
    )
    for rel in required:
      self.assertTrue((self.workload / rel).is_file(), rel)

  def test_bench_specs_registered(self):
    names = {s.name for s in TIER1_BENCHES}
    self.assertIn("fft_1d_fixed", names)
    self.assertIn("fft_1d_fixed_pure_li", names)
    pure = next(s for s in TIER1_BENCHES if s.name == "fft_1d_fixed_pure_li")
    self.assertTrue(pure.li_pure)


if __name__ == "__main__":
  unittest.main()
