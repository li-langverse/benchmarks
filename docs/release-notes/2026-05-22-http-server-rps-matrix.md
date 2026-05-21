# HTTP webserver full RPS comparison matrix

## Summary

Adds a canonical multi-oracle RPS table (all tier-5 HTTP scenarios, **`li` on every row**) plus Cursor rule **li-httpd-bench-matrix.mdc** so agents refresh performance after each httpd step.

## Agent continuation

1. **Read:** `docs/ecosystem/http-server-rps-matrix.md`, `.cursor/rules/li-httpd-bench-matrix.mdc`, `scripts/benchmark-matrix-report.py`.
2. **Run:** `LIC_ROOT=../lic BENCH_HTTP_PROFILE=nightly ./scripts/run-tier5-http-bench.sh && ./scripts/benchmark-matrix-report.py`.
3. **Then:** fix `proxy_loopback` / LB `wrk_parse_fail_li` on epoll `li-httpd`; paste updated table into next **lic** httpd PR.
4. **Blocked on:** `lic` `main` stub — static RPS only until epoll rebases onto `main`.

## Changed

- `scripts/benchmark-matrix-report.py` — fixed scenario order from `suite.toml`; columns `li|nginx|apache|lighttpd|node|bun|li/nginx`; verify table for `rate_limit_429`, `https_static`; writes `docs/ecosystem/http-server-rps-matrix.md`.
- `.cursor/rules/li-httpd-bench-matrix.mdc` — mandatory matrix refresh after httpd edits.
- `docs/ecosystem/http-server-benchmark-growth.md` — link to RPS matrix doc.
- `docs/ecosystem/http-server-rps-matrix.md` — generated snapshot (epoll `LIC_ROOT`, 2026-05-21).

## Not changed

- `vendor/lis-tier5/benchmarks/tier5_http/harness/bench_http.py` proxy hot path (Li still **FAIL** on proxy/LB).
- **lic** runtime merge to `main`.
- Dashboard ingest thresholds.

## Breaking

N/A — reporting only.

## Security

N/A — throughput table; exploits remain in `benchmark-matrix.md` exploit section.

## Performance

Example RPS (epoll branch, loopback wrk): `static_small` li **135,343** vs nginx **85,276** (1.59×); `keepalive_pipelining` li **233,938** vs nginx **95,637** (2.45×); proxy/LB li **FAIL** pending fix.

## Downstream

- **lic** httpd PRs must paste `http-server-rps-matrix.md` table in description.
