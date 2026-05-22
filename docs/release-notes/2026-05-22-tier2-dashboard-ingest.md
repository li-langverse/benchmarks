# Dashboard ingest: tier-2 physics CSV (post rigid_body_stack fix)

## Summary

Refreshed `data/latest/summary.json` and history index from `lic` `benchmarks/results/latest.csv` after tier-1+2 harness sweep (includes `rigid_body_stack` Li timings).

## Agent continuation

1. **Read:** `data/latest/summary.json` physics category; `catalog.toml` `rigid_body_stack` row.
2. **Run:** After **lic#169** merges, `LIC_ROOT=<lic> ./scripts/ingest/ingest-lic.sh` on `main` for CI-aligned SHA.
3. **Then:** Pages deploy from `main`; verify https://li-langverse.github.io/benchmarks/ physics charts.
4. **Blocked on:** lic merge for permanent bench driver contracts on `main`.

## Changed

| Path | Evidence |
|------|----------|
| `data/latest/summary.json` | 33 benchmark rows; `rigid_body_stack` Li/cpp ratio |
| `data/history/index.json` | `latest_deltas` from `record-benchmark-history.py` |
| `data/history/2026-05-22T084152Z.json` | snapshot |

## Not changed

- `catalog.toml` (rows already present).
- `scripts/ingest/*` ingest pipeline.
- Tier-5 HTTP vendor CSV.

## Breaking / Security / Performance / Downstream

| Topic | Status |
|-------|--------|
| **Breaking** | N/A |
| **Security** | N/A |
| **Performance** | Display-only refresh from lic harness at `229ecc7` + local tier-2 contract branch CSV |
| **Downstream** | N/A |
