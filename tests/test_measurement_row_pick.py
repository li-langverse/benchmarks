"""Measurement row pick + CSV dedupe for build_summary."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/ingest"))

from build_summary import (  # noqa: E402
    dedupe_csv_rows,
    measurement_row_score,
    parse_sample_runs,
    pick_best_measurement_row,
)


class MeasurementRowPickTests(unittest.TestCase):
    def test_parse_sample_runs_rejects_git_sha(self):
        self.assertIsNone(parse_sample_runs({"sample_runs": "0c313cf0"}))
        self.assertEqual(parse_sample_runs({"sample_runs": "20"}), 20)

    def test_pick_best_prefers_valid_timing_row(self):
        legacy = {
            "benchmark": "foo",
            "lang": "li",
            "metric": "wall_time",
            "value": "0.42",
            "sample_runs": "0c313cf0",
            "os": "linux",
        }
        fresh = {
            "benchmark": "foo",
            "lang": "li",
            "metric": "wall_time",
            "value": "0.18",
            "sample_runs": "20",
            "stddev": "0.001",
            "git_sha": "abc123",
            "os": "linux",
        }
        picked = pick_best_measurement_row([legacy, fresh])
        self.assertEqual(picked["sample_runs"], "20")
        self.assertGreater(measurement_row_score(fresh), measurement_row_score(legacy))

    def test_dedupe_keeps_best_per_key(self):
        rows = [
            {
                "benchmark": "foo",
                "lang": "li",
                "variant": "",
                "metric": "wall_time",
                "value": "1",
                "sample_runs": "deadbeef",
                "os": "linux",
                "threads": "",
            },
            {
                "benchmark": "foo",
                "lang": "li",
                "variant": "",
                "metric": "wall_time",
                "value": "2",
                "sample_runs": "20",
                "stddev": "0.01",
                "os": "linux",
                "threads": "",
            },
        ]
        out = dedupe_csv_rows(rows)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["sample_runs"], "20")


if __name__ == "__main__":
    unittest.main()
