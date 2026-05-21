# Tier-5 rate_limit_429 + master-plan progress runner

## Summary

Added `rate_limit_429` HTTP scenario (li-httpd verify-only) to vendor harness and catalog; `httpd-masterplan-step.sh` appends full-suite matrix after each master-plan milestone.

## Agent continuation

1. **Read** `data/latest/httpd-masterplan-progress.md` and `data/latest/benchmark-matrix.md` after each lic change.
2. **Run** `LIC_ROOT=/workspace/lic ./scripts/httpd-masterplan-step.sh step-N-<slug> "note"` (8–15 min full suite; use `SKIP_TIER0=1 BENCH_RUNS=1` defaults).
3. **Then** merge PRs #58/#59 when CI green; refresh Pages ingest for new catalog row `rate_limit_429`.
4. **Blocked on** `https_*` tier5 scenarios until `li-tls` package lands in lic.

## Changed

- `vendor/lis-tier5/benchmarks/tier5_http/scenarios/rate_limit_429/bench.toml`; `suite.toml` includes scenario in ci/nightly.
- `vendor/lis-tier5/benchmarks/tier5_http/harness/bench_http.py` — `bench_rate_limit_scenario`, runtime `.conf` writer.
- `catalog.toml` — `rate_limit_429` row (`verify_pass`, oracle `li`).
- `scripts/httpd-masterplan-step.sh` — progress log + matrix excerpt.

## Not changed

- Tier-1 `matmul_blocked` RED thresholds.
- Exploit harness TOML set (still separate `tier5_http_exploits`).
- lic compiler / stdlib proofs.
- Dashboard Vite build (PH-IO-5).

## Breaking

N/A — additive catalog and harness path.

## Security

N/A — reuses existing rate-limit behavior; no new attack surface in harness.

## Performance

N/A — verify-only row (no wrk RPS for `rate_limit_429`).

## Downstream

- **lic** `cursor/httpd-masterplan-54aa` — routing tests + `li-log` stub; rebuild `build/li-httpd` before bench.
