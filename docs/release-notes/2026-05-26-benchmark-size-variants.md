# Benchmark problem size variants

## Summary

Catalog, ingest, and dashboard-next now carry optional `problem_size` / `size_label` (and `base_id` for suffixed ids) so multiple problem scales per algorithm can appear as separate dashboard rows.

## Agent continuation

1. **Read** `docs/ecosystem/benchmark-size-survey.md`, `catalog.toml` header, `scripts/ingest/build_summary.py` (`row_matches_catalog`).
2. **Run** `python3 scripts/ingest/build_summary.py ../lic ../lis` then `python3 scripts/benchmark-matrix-report.py`; `cd dashboard-next && npm run build`.
3. **Next** When lic exports sized sweeps, add CSV `problem_size` or suffixed `benchmark` ids; register rows in `catalog.toml` (see `matmul_naive_N1024` pending stub).
4. **Blocked** `feat/benchmark-ship-integration` branch not on remote — PR targets `main`; merge into `feat/benchmark-board-ship` locally if needed.

## Changed

| Path | Notes |
|------|--------|
| `catalog.toml` | Schema comments; sizes on tier-1 micro + sample physics/http; `matmul_naive_N1024` pending variant |
| `scripts/ingest/build_summary.py` | Size-aware CSV match; `summary.json` `problem_size` / `size_label` / `base_id`; `reporting.size_labels` |
| `schema/bench-result.json` | Optional `problem_size` CSV column |
| `scripts/benchmark-matrix-report.py` | Matrix rows include size fields |
| `dashboard-next/` | Size column + filters on overview/matrix; bench drill-down |
| `docs/ecosystem/benchmark-size-survey.md` | lic/lis size survey |

## Not changed

- `lic` harness CSV header (no `problem_size` column yet — backward compatible)
- `feat/expand-catalog-algorithms` catalog expansion (separate branch)
- Bench thresholds / tier gates

## Breaking / Security / Performance / Downstream

- **Breaking:** N/A — additive JSON fields; extra catalog row `matmul_naive_N1024` is pending-only.
- **Security:** N/A
- **Performance:** N/A
- **Downstream:** Agents filtering by benchmark id should also check `size_label` when multiple rows share a family (`base_id`).
