# Benchmarks — https_static tier5 stub (M1 wave 8)

## Summary

Added nightly `https_static` tier-5 HTTP scenario with `verify_skip` / `tls_m15_pending` until `li-tls` terminates HTTPS on li-httpd.

## Agent continuation

1. **Read** `vendor/lis-tier5/benchmarks/tier5_http/scenarios/https_static/bench.toml` and `catalog.toml` row `https_static`.
2. **Run** `LIC_ROOT=/workspace/lic ./scripts/httpd-masterplan-step.sh step-8-wave8-tls-headers "M1 wave 8"` after lic wave 8 merges.
3. **Then** flip catalog `verify_skip` off when `LI_HTTPD_TLS=1` ships in lic.
4. **Blocked on** lic `packages/li-tls` record layer (PH-H / M1.5).

## Changed

- `vendor/lis-tier5/benchmarks/tier5_http/scenarios/https_static/bench.toml` — TLS verify stub.
- `vendor/lis-tier5/benchmarks/tier5_http/harness/bench_http.py` — `bench_tls_scenario`.
- `vendor/lis-tier5/benchmarks/tier5_http/suite.toml` — nightly includes `https_static`.
- `catalog.toml` — `https_static` row (`verify_skip`).

## Not changed

- lic TLS terminate implementation (separate PR on `cursor/httpd-masterplan-54aa`).
- Exploit matrix thresholds.
- Dashboard Vite build.

## Breaking

N/A — scenario skipped in verify gate.

## Security

N/A — stub only; no TLS listener in bench yet.

## Performance

N/A — `load.tool = none`.

## Downstream

- **lic:** enable HTTPS bench when M1.5 TLS lands.
