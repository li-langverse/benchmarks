# Tier-5 Apache/lighttpd proxy oracle launch fix

## Summary

Fixes `apache_proxy_start_fail` and lighttpd proxy `start_fail` in tier-5 HTTP harness so proxy/LB rows can include apache and lighttpd RPS alongside nginx and li.

## Agent continuation

1. **Read:** `vendor/lis-tier5/benchmarks/tier5_http/harness/http_oracles.py` (`apache_proxy_lb_conf`, `lighttpd_proxy_lb_conf`, `start_*_proxy_bench`).
2. **Run:** `BENCH_PROXY_ORACLES=nginx,apache,lighttpd,li LIC_ROOT=… ./scripts/run-tier5-http-bench.sh` then `./scripts/benchmark-matrix-report.py`.
3. **Then:** merge **lic** PR #153 (epoll proxy) before trusting **li** proxy rows on dashboard ingest.
4. **Blocked on:** **li** `https_static` RPS until `li-tls` terminates TLS in-process.

## Changed

- `vendor/lis-tier5/benchmarks/tier5_http/harness/http_oracles.py` — Apache balancer config; lighttpd `proxy.server` tuple syntax + `htdocs/` mkdir in `start_lighttpd_proxy_bench`.

## Not changed

- **lic** runtime / `li-httpd` proxy implementation (separate PR #153).
- nginx/caddy proxy paths (already worked or optional).
- HTTPS `openssl s_time` oracle wiring.

## Breaking

N/A.

## Security

N/A — bench-only prefix configs under `/tmp`.

## Performance

Enables apache/lighttpd columns on `proxy_loopback` / `lb_*` when backends are up.

## Downstream

- Refresh `docs/ecosystem/http-server-rps-matrix.md` after nightly bench.
