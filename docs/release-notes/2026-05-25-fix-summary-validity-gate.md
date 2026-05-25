# Fix summary ingest validity gate blanking tier colors

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (feat/fix-summary-statuses)  
**PH / REQ:** PH-IO-7 (dashboard honesty)  
**Author:** agent

---

## Summary (one sentence)

`validity_for_benchmark` no longer forces every CSV-backed row to `unknown` when `latest.csv` lacks a `passed` column or catalog `variant` differs from export tags, so perf colors appear for harness rows that already have measurements.

## Agent continuation (required)

1. Read: `scripts/ingest/build_summary.py` (`li_rows_for_validity`, `latest.csv:perf_present`), `docs/honesty/benchmark-dashboard.md`.
2. Run: `python3 scripts/ingest/build_summary.py ../lic ../lis`; `python3 scripts/ingest/build_summary_fixture.py`; `python3 -m py_compile scripts/ingest/build_summary.py`.
3. Then: Extend **lic**/**lis** CSV writers with explicit `passed` + `os` on all exports; re-run ingest in CI so Pages picks up full green/yellow/red coverage.
4. Blocked on: Full tier-2/5 harness CSV coverage — most catalog rows remain `pending` / no series until benches land.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Ingest | `li_rows_for_validity()` variant fallback (matches `lang_series`); implicit pass `latest.csv:perf_present` when Li has numeric rows and no `passed` column | Local ingest: 8 `green` rows; tier 1 `green: 1`, tier 2 `green: 5`, tier 5 `green: 2` |
| Artifact | `data/latest/summary.json` regenerated from sibling `../lic` CSV | 179 rows; 171 `unknown`, 8 `green` |

## Not changed (scope fence)

- **lic**/**lis** harness measurement code and CSV `passed`/`os` column producers.
- Dashboard-next UI components — consume existing `status` field.
- Catalog `validity_required` defaults (still `true`).
- Agent control plane (**li-cursor-agents**).

## Breaking changes

None — `validity_source` may show `latest.csv:perf_present`; `status` may change from `unknown` to perf color where CSV data exists.

## Security

N/A — ingest-only.

## Performance

N/A — ingest CPU only.

## Downstream

| Repo | Action |
|------|--------|
| **lic** / **lis** | Add `passed` and `os` to `benchmarks/results/latest.csv` exports |
