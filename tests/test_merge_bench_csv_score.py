#!/usr/bin/env python3
"""Tier shard merge must not let later registry aliases clobber equalized tier1 rows."""
from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MERGE = ROOT / "scripts" / "ingest" / "merge_bench_csv_artifacts.py"


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "benchmark",
        "lang",
        "variant",
        "metric",
        "value",
        "stddev",
        "sample_runs",
        "unit",
        "os",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})


class MergeBenchCsvScoreTests(unittest.TestCase):
    def test_keeps_higher_sample_runs_on_duplicate_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            tier1 = tmp_p / "tier-1.csv"
            tier7 = tmp_p / "tier-7.csv"
            out = tmp_p / "latest.csv"
            base = {
                "benchmark": "matmul_naive",
                "variant": "release",
                "metric": "wall_time",
                "value": "1.0",
                "stddev": "0.01",
                "unit": "s",
                "os": "linux",
            }
            _write_csv(
                tier1,
                [
                    {**base, "lang": "li", "sample_runs": "102"},
                    {**base, "lang": "cpp", "sample_runs": "102"},
                ],
            )
            _write_csv(
                tier7,
                [
                    {**base, "lang": "li", "sample_runs": "73"},
                    {**base, "lang": "cpp", "sample_runs": "73"},
                ],
            )
            proc = subprocess.run(
                [sys.executable, str(MERGE), str(out), str(tier1), str(tier7)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with out.open(encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            li = next(r for r in rows if r["lang"] == "li")
            self.assertEqual(li["sample_runs"], "102")


if __name__ == "__main__":
    unittest.main()
