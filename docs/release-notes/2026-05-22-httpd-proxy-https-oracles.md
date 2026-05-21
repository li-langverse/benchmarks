# HTTP proxy/LB + HTTPS multi-oracle benchmarks

## Summary

Extends tier-5 harness with `BENCH_PROXY_ORACLES` (nginx, apache, lighttpd, caddy, li), fixes matrix merge when supplemental `http_tier5.csv` has li=0, and adds `https_static` RPS via `openssl s_time` for TLS-capable oracles.

## Agent continuation

1. **Read:** `vendor/lis-tier5/benchmarks/tier5_http/harness/http_oracles.py`, `bench_http.py`; `docs/ecosystem/http-server-rps-matrix.md`.
2. **Run:** `LIC_ROOT=../lic BENCH_HTTP_PROFILE=nightly ./scripts/run-tier5-http-bench.sh && ./scripts/benchmark-matrix-report.py`.
3. **Then:** fix apache/lighttpd proxy start (module paths); wire **li-tls** for li `https_static` RPS.
4. **Blocked on:** `caddy` optional on CI; apache proxy needs `mod_proxy_balancer` tuning on some images.

## Changed

- `vendor/lis-tier5/benchmarks/tier5_http/harness/http_oracles.py` — proxy + TLS configs and hooks.
- `vendor/lis-tier5/benchmarks/tier5_http/harness/bench_http.py` — multi-oracle proxy/LB; `openssl_https_rps` + `bench_tls_scenario`.
- `scripts/benchmark-matrix-report.py` — supplemental merge fix; https row shows oracle RPS.
- `scripts/run-tier5-http-bench.sh` — `BENCH_PROXY_ORACLES`.
- `catalog.toml` — `https_static` metric `rps`.
- `docs/ecosystem/http-server-benchmark-growth.md`.

## Not changed

- **lic** runtime (separate PR/branch `cursor/httpd-proxy-bench-fix-54aa`).
- Dashboard ingest thresholds.

## Breaking

N/A.

## Security

HTTPS benches use generated self-signed certs (loopback only).

## Performance

Example after lic proxy fix: `proxy_loopback` li ~134k vs nginx ~78k; `lb_round_robin` li ~130k vs nginx ~44k.

## Downstream

- Paste `http-server-rps-matrix.md` into httpd PRs after each milestone.
