#!/usr/bin/env python3
"""Tests for per-benchmark run-count equalization across languages."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

HARNESS = Path(__file__).resolve().parent
sys.path.insert(0, str(HARNESS))

from timing_stats import (  # noqa: E402
    TimingStats,
    equalize_runs_enabled,
    probe_command,
    time_command,
    time_commands_with_equal_runs,
)


class TimingEqualizeTests(unittest.TestCase):
    def test_equalize_runs_default_on(self) -> None:
        with mock.patch.dict("os.environ", {}, clear=True):
            self.assertTrue(equalize_runs_enabled())

    def test_equalize_runs_can_disable(self) -> None:
        with mock.patch.dict("os.environ", {"BENCH_EQUALIZE_RUNS": "0"}):
            self.assertFalse(equalize_runs_enabled())

    def test_time_commands_with_equal_runs_uses_max(self) -> None:
        planned = iter([10, 30, 20])

        def fake_probe(cmd, *, cwd=None, runs=6):  # noqa: ARG001
            return [0.1, 0.1, 0.1], next(planned)

        def fake_time(cmd, *, cwd=None, runs=6, total_runs=None, initial_samples=None):  # noqa: ARG001
            n = total_runs if total_runs is not None else len(initial_samples or [])
            return TimingStats(mean=0.1, stddev=0.0, sample_runs=n)

        with (
            mock.patch.dict("os.environ", {"BENCH_EQUALIZE_RUNS": "1"}),
            mock.patch("timing_stats.probe_command", side_effect=fake_probe),
            mock.patch("timing_stats.time_command", side_effect=fake_time),
        ):
            stats = time_commands_with_equal_runs([["a"], ["b"], ["c"]], runs=6)

        self.assertEqual([s.sample_runs for s in stats], [30, 30, 30])

    def test_time_command_honors_total_runs_with_initial_samples(self) -> None:
        with mock.patch("timing_stats.run_timed_once", return_value=0.05):
            stats = time_command(
                ["echo"],
                runs=6,
                total_runs=12,
                initial_samples=[0.05, 0.05, 0.05],
            )
        self.assertEqual(stats.sample_runs, 12)

    def test_probe_command_returns_planned_runs(self) -> None:
        with mock.patch("timing_stats.run_timed_once", return_value=0.01):
            with mock.patch("timing_stats.subprocess.run") as run_mock:
                run_mock.return_value = mock.Mock(returncode=0)
                samples, planned = probe_command(["echo"], runs=6)
        self.assertEqual(len(samples), 3)
        self.assertGreaterEqual(planned, 20)


if __name__ == "__main__":
    unittest.main()
