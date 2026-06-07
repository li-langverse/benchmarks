#!/usr/bin/env python3
"""Tests for locked CSV merge and sample-run parity resume gates."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

HARNESS = Path(__file__).resolve().parent
sys.path.insert(0, str(HARNESS))

from csv_bench_io import benchmark_sample_runs_parity_ok, wall_time_sample_runs  # noqa: E402


def _row(benchmark: str, lang: str, sample_runs: int) -> dict[str, str]:
    return {
        "benchmark": benchmark,
        "lang": lang,
        "metric": "wall_time",
        "sample_runs": str(sample_runs),
    }


class CsvBenchIoTests(unittest.TestCase):
    def test_wall_time_sample_runs_groups_langs(self) -> None:
        rows = [_row("matmul_naive", "li", 30), _row("matmul_naive", "cpp", 30)]
        self.assertEqual(wall_time_sample_runs(rows, "matmul_naive"), {"li": 30, "cpp": 30})

    def test_parity_ok_when_equal(self) -> None:
        rows = [_row("matmul_naive", "li", 102), _row("matmul_naive", "cpp", 102)]
        self.assertTrue(benchmark_sample_runs_parity_ok(rows, "matmul_naive", equalize=True))

    def test_parity_fails_when_li_runs_short(self) -> None:
        rows = [_row("matmul_naive", "li", 73), _row("matmul_naive", "cpp", 102)]
        self.assertFalse(benchmark_sample_runs_parity_ok(rows, "matmul_naive", equalize=True))

    def test_parity_skipped_when_equalize_off(self) -> None:
        rows = [_row("matmul_naive", "li", 73), _row("matmul_naive", "cpp", 102)]
        self.assertTrue(benchmark_sample_runs_parity_ok(rows, "matmul_naive", equalize=False))

    def test_missing_li_not_complete(self) -> None:
        rows = [_row("matmul_naive", "cpp", 102)]
        self.assertFalse(benchmark_sample_runs_parity_ok(rows, "matmul_naive", equalize=True))


if __name__ == "__main__":
    unittest.main()
