"""Tier-1 FFT micro-bench catalog + workload mirror (benchmarks#6 / #18)."""

from __future__ import annotations

import os
import shutil
import subprocess
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

  def test_native_oracle_builds(self):
    cc = os.environ.get("CC") or shutil.which("clang") or shutil.which("gcc") or shutil.which("cc")
    if not cc:
      self.skipTest("no C compiler (clang/gcc/cc) on PATH")
    build_dir = ROOT / "build" / "test-fft-oracle"
    build_dir.mkdir(parents=True, exist_ok=True)
    bin_path = build_dir / "fft_1d_fixed_cpp"
    main_c = self.workload / "cpp" / "main.c"
    core_c = self.workload / "common" / "fft_1d_fixed_core.c"
    cmd = [cc, "-O3", "-march=native", "-ffast-math", str(main_c), str(core_c), "-lm"]
    try:
      proc = subprocess.run(["pkg-config", "--exists", "fftw3"], capture_output=True, check=False)
      if proc.returncode == 0:
        cflags = subprocess.check_output(["pkg-config", "--cflags", "fftw3"], text=True).split()
        libs = subprocess.check_output(["pkg-config", "--libs", "fftw3"], text=True).split()
        cmd = [*cmd, "-DLI_BENCH_FFTW", *cflags, *libs]
    except (FileNotFoundError, subprocess.CalledProcessError):
      pass
    cmd.extend(["-o", str(bin_path)])
    subprocess.check_call(cmd, cwd=ROOT)
    out = subprocess.check_output([str(bin_path), "--verify"], text=True).strip()
    checksum = float(out)
    self.assertNotEqual(checksum, 0.0)


if __name__ == "__main__":
  unittest.main()
