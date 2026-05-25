# Refresh benchmark CSV ingest — measured tier 1/2 rows

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** feat/refresh-bench-csv  
**PH / REQ:** WP-B5 (benchmark dashboard honesty)

---

## Summary (one sentence)

Regenerated `data/latest/summary.json` from a fresh **lic** tier 1+2 harness run (81 CSV rows) plus tier-5 vendor merge, restoring green/yellow/red perf status for harness-backed catalog ids while leaving unmeasured registry rows honestly `unknown`.

## Agent continuation (required)

1. **Read:** `../lic/benchmarks/results/latest.csv`, `scripts/ingest/build_summary.py`, `docs/honesty/benchmark-dashboard.md`.
2. **Run:** `LIC_ROOT=../lic LIS_ROOT=../lis ./scripts/ingest/ingest-lic.sh`; `python3 scripts/check-dashboard-invariants.py`.
3. **Then:** Fix **lic** build failures for skipped benches (`horner_pure_li`, `rigid_body_stack`, …) and re-run tier 1+2 harness.
4. **Blocked on:** ~163 catalog rows without harness CSV; tier-6 DB stubs.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Data | `data/latest/summary.json` | Ingest: **163** `unknown`, **14** `green`, **1** `yellow`, **1** `red` (179 rows) |
| Ingest | `li_rows_for_validity`, `latest.csv:perf_present`, `merge-tier5-into-lic-csv.py` | `./scripts/ingest/ingest-lic.sh` |
| Harness (local) | **lic** tier 1+2 timing; 11 Li builds skipped | Sibling `latest.csv` 81 rows (not committed in **lic** here) |

## Not changed (scope fence)

- `catalog.toml` thresholds — **not** weakened.
- **lic** compiler fixes for skipped kernels — follow-up **lic** PR.
- `dashboard-next` UI — **not** in this PR.

## Breaking changes

None.

## Security

N/A — reads existing CSV only.

## Performance

| Tier | Green | Yellow | Red | Unknown |
|------|-------|--------|-----|---------|
| 1 | 3 | 0 | 1 | 43 |
| 2 | 9 | 1 | 0 | 80 |
| 5 | 2 | 0 | 0 | 8 |

## Downstream

| Repo | Action |
|------|--------|
| **lic** | Optional: commit `benchmarks/results/latest.csv` on agent branch if policy allows |

## CHANGELOG entry (paste into Unreleased)

### Fixed

- **Harness-backed dashboard rows:** Refresh `data/latest/summary.json` from **lic** tier 1+2 CSV + ingest validity — [2026-05-25-refresh-bench-csv.md](docs/release-notes/2026-05-25-refresh-bench-csv.md).
