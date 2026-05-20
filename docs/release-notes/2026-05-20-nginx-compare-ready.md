# nginx compare ready — vendored tier-5 + safe HTTP ingest

## Summary

Benchmarks can run **stock nginx + wrk** baselines, merge **`lang=nginx`** RPS into `summary.json` without clearing physics rows when **lic** CSV is absent, and plot HTTP charts; **Li vs nginx ratio** activates when **lic** ships **li-httpd** and the harness emits **`lang=li`** rows.

## Agent continuation

1. **Read:** `docs/ecosystem/http-nginx-compare.md`, `vendor/lis-tier5/README.md`, `scripts/ingest/merge_lis_http_into_summary.py`.
2. **Run:** `python3 vendor/lis-tier5/benchmarks/tier5_http/harness/bench_http.py --profile ci` then `merge_lis_http_into_summary.py` on `vendor/lis-tier5/results/latest.csv`.
3. **Then:** merge **lis** PR (`bench_http.py` + `bench-export.yml`); remove vendor after **lis** `main` sync; wire **lic** `httpd_serve` + `LI_HTTPD_BIN`.
4. **Blocked on:** `cursor[bot]` cannot push **lis** (403) — human push required for upstream harness.

## Changed

| Area | Path |
|------|------|
| Vendor harness | `vendor/lis-tier5/benchmarks/tier5_http/**` |
| Ingest | `scripts/ingest/ingest-lic.sh`, `ingest-lis.sh`, `merge_lis_http_into_summary.py` |
| CI / ingest WF | `.github/workflows/ci.yml`, `ingest.yml` |
| Docs | `docs/ecosystem/http-nginx-compare.md` |
| Dashboard data | `data/latest/summary.json` http nginx series |

## Not changed

- `dashboard/` Vite sources (other agent).
- **lic** `httpd_serve` implementation.
- Full **lic** bench CSV generation in CI (still optional).

## Breaking

N/A

## Security

nginx bench binds loopback only; private `-p` prefix.

## Performance

CI adds ~10s wrk per scenario on Ubuntu.

## Downstream

**lis** `bench-export.yml` + `BENCHMARKS_INGEST_DISPATCH` for automated ingest when token configured.
