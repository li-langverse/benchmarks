# Tier-5 HTTP — multi-oracle performance + security (nginx, Apache, lighttpd, li)

## Summary

`bench_http.py` and `exploit_http.py` share `harness/http_oracles.py` so tier-5 HTTP benchmarks compare **nginx, Apache httpd, lighttpd, Node.js, Bun, and li-httpd** (optional **caddy**) on the same wrk scenarios and exploit drivers.

## Agent continuation

1. **Read:** `vendor/lis-tier5/benchmarks/tier5_http/harness/http_oracles.py`, `BENCH_HTTP_ORACLES`, `TIER5_EXPLOIT_LANGS`.
2. **Run:** `sudo apt-get install -y nginx wrk apache2 lighttpd` then `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,li ./scripts/run-tier5-http-bench.sh` and `TIER5_EXPLOIT_LANGS=nginx,apache,lighttpd,li ./scripts/run-tier5-http-exploits.sh`.
3. **Then:** ingest `merge_lis_http_into_summary.py` for dashboard multi-bar charts; proxy scenarios still **nginx+li** only.
4. **Blocked on:** **caddy** not in CI apt (enable locally with `BENCH_HTTP_ORACLES=...,caddy`); Apache mod_proxy front for `proxy_loopback` not wired.

## Changed

| Path | Detail |
|------|--------|
| `vendor/lis-tier5/benchmarks/tier5_http/harness/http_oracles.py` | New shared launch/stop for nginx, apache, lighttpd, caddy, li |
| `harness/bench_http.py` | `BENCH_HTTP_ORACLES` loop; static scenarios bench all oracles |
| `harness/exploit_http.py` | Uses `http_oracles`; lighttpd/caddy optional |
| `scripts/run-tier5-http-bench.sh` | New wrapper |
| `scripts/ingest/merge_lis_http_into_summary.py` | Series includes apache, lighttpd, caddy |
| `scripts/plot_http_benchmarks.py` | Colors for apache/lighttpd/caddy |
| `.github/workflows/ci.yml` | `lighttpd` apt; bench+exploit after lic build |

## Not changed

- `catalog.toml` `compare_oracle` still **nginx** (li ratio baseline unchanged)
- Proxy/LB scenarios: still **nginx + li** only (no apache/lighttpd front)
- Exploit attack drivers (same TOMLs; more oracle columns in CSV)

## Breaking

N/A — additive CSV `lang` rows.

## Security

Exploit harness runs same tiers against each available oracle; CI `TIER5_EXPLOIT_LANGS=nginx,apache,lighttpd,li` when packages installed.

## Performance

Example local `static_small` ci (3s wrk): nginx ~84k, apache ~40–50k, lighttpd ~35–45k, li ~128k RPS (host-dependent). Use `results/latest.csv` for exact rows.

## Downstream

Dashboard http charts show all oracle series when ingest merges vendored CSV.
