# Ingest — checkout lis + dashboard honesty for HTTP

## Summary

Benchmark ingest workflows now check out **lis** and call `ingest-lic.sh` with explicit `LIC_ROOT` / `LIS_ROOT`, fixing a bug where `build_summary.py` received a CSV file as the second positional argument (mis-parsed as the `lis` tree).

## Agent continuation

1. **Read:** `.github/workflows/ingest.yml`, `.github/workflows/ci.yml`, `.github/workflows/ecosystem-audit.yml`, `docs/honesty/benchmark-dashboard.md`, `scripts/ingest/build_summary.py` (`sys.argv` contract).
2. **Run:** On a PR, confirm **Benchmarks CI** `ingest-smoke` still passes; manually dispatch **Ingest benchmarks** after a `lic-bench-complete` dispatch if you need to validate artifact copy + ingest.
3. **Then:** When **lis** ships `results/latest.csv` with `rps` rows for `li` and `nginx`, re-run ingest and confirm `data/latest/summary.json` HTTP charts gain non-empty `series` and `ratio_vs_reference`.
4. **Blocked on:** **lis** tier-5 harness still stub-only for perf (`bench_http.py`); no CSV writer on `main` yet per `lis/docs/plan.md`.

## Changed

| Area | Path | Evidence |
|------|------|----------|
| Manual ingest | `.github/workflows/ingest.yml` | `lis` checkout; artifact → `lic/benchmarks/results/latest.csv`; `ingest-lic.sh` |
| PR CI | `.github/workflows/ci.yml` | `lis` checkout; `LIS_ROOT` on ingest step |
| Manual audit | `.github/workflows/ecosystem-audit.yml` | `lis` checkout; `LIS_ROOT`; Python fallback `build_summary.py lic lis` |
| Docs | `docs/honesty/benchmark-dashboard.md` | HTTP vs nginx honesty; local vs CI; `li-local-ci` vs dashboard |
| Changelog | `CHANGELOG.md` | Unreleased Fixed row |

## Not changed

- `catalog.toml` HTTP benchmark IDs or thresholds.
- `scripts/ingest/build_summary.py` ratio logic.
- `li-local-ci` behavior or `local-ci-sweep.py` contract.
- **lis** harness implementation (still stub for throughput).

## Breaking

N/A — workflow and doc corrections only.

## Security

N/A — read-only checkout of public org repos; same `GITHUB_TOKEN` scope as existing `lic` checkout.

## Performance

N/A — shallow `lis` checkout adds small clone time to affected workflows.

## Downstream

Org automation that assumed ingest used only `lic` should note **`lis` is now a sibling checkout** under `GITHUB_WORKSPACE/lis` for these jobs.
