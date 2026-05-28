# Release notes: 2026-05-28 — bench mean ± σ in dashboard

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks (+ lic harness PR)  
**PR:** branch `cursor/bench-mean-std-dashboard-5599`  

---

## Summary

Dashboard and ingest show **mean ± sample stddev** and **run count** from harness CSV (`value` = mean; requires lic `timing_stats` harness).

## Agent continuation

1. Merge **lic** PR `cursor/bench-mean-std-runs-5599` first.
2. Re-run tier 1+2 → `ingest-lic.sh` so `summary.json` rows include `li_stddev` / `sample_runs`.
3. Verify `/bench/horner_pure_li` shows `n≥20` for sub-second kernels.

## Changed

| Area | What |
|------|------|
| Ingest | `timing_fields_from_row`, `value_stat: mean` in reporting |
| Dashboard | `formatMeanStd`, langs table Mean ± σ / Runs columns |
| Suite | `BENCH_RUNS=6`, `BENCH_MIN_RUNS=6`, `BENCH_SUBSEC_MIN_RUNS=20` |

## Not changed

- HTTP tier-5 harness (still separate median path in lis-tier5 until follow-up).

## CHANGELOG

### Changed

- Dashboard displays harness **mean ± σ** and **sample_runs** when lic CSV includes new columns — [2026-05-28-bench-mean-std-dashboard.md](docs/release-notes/2026-05-28-bench-mean-std-dashboard.md).
