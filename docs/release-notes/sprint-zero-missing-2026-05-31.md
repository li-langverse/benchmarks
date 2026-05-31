# Sprint run 2026-05-31

## Results

- Ran full Linux tier suite via `scripts/sprint-run-all-tiers.sh` (WSL).
- **summary.json:** 54 green, 2 yellow, 243 skip (was 21 green / 277 skip).
- **latest.csv:** 305 rows merged from tier0/1/2 shards + tier5 HTTP oracles.
- **Zero-missing gate:** still failing — see `data/latest/zero-missing-data-report.json`.

## Skip breakdown

| Cause | ~count |
|-------|--------|
| macOS / Windows matrix rows (no local CSV) | 112 |
| Linux rows without harness or CSV | 131 |
| harness pending catalog entries | 114 |
| workload dirs missing on disk | 27 |

## Fixes in this branch

- `scripts/tier5-http-bench.py` — fall back to `benchmarks/harness/timing_stats.py`.
- `scripts/sprint-run-all-tiers.sh` — repeatable sprint driver.
- `scripts/audit/analyze-skips.py` — skip attribution helper.

## Next

1. Green GHA nightly + 3-OS CSV merge (clears macOS/Windows skips).
2. Implement or mark `harness pending` catalog entries (114).
3. Add tier6 / tier5 supplemental fixtures for 27 missing paths.
4. Re-run gate: `BENCHMARK_NIGHTLY_GATE_NATIVE=1 bash scripts/benchmark-nightly-gate.sh`.
