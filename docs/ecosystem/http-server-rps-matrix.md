# HTTP webserver RPS matrix (tier 5)

Generated: 2026-05-21T13:50:17.090999+00:00

**Mandatory after every li-httpd change:**
`LIC_ROOT=… ./scripts/run-tier5-http-bench.sh` → `./scripts/benchmark-matrix-report.py`

Source CSV: `/workspace/vendor/lis-tier5/results/latest.csv`

Oracles: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li`. Proxy/LB scenarios bench **nginx + li**; static scenarios bench all oracles.

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|
| static_small | 135,343 | 85,276 | 52,230 | 177,456 | 29,382 | — | 1.59× |
| keepalive_pipelining | 233,938 | 95,637 | 64,981 | 235,147 | 29,975 | — | 2.45× |
| static_large | 9,226 | 8,857 | 8,820 | 9,084 | 3,141 | — | 1.04× |
| proxy_loopback | FAIL | 77,204 | — | — | — | — | — |
| lb_round_robin | FAIL | 68,477 | — | — | — | — | — |
| lb_least_conn | FAIL | 71,359 | — | — | — | — | — |
| lb_peer_down | FAIL | 72,199 | — | — | — | — | — |

**Li notes:** `lb_least_conn`: wrk_parse_fail_li; `lb_peer_down`: wrk_parse_fail_li; `lb_round_robin`: wrk_parse_fail_li; `proxy_loopback`: wrk_parse_fail_li

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | pass | N/A (li-only or pending) |
| https_static | skip | N/A (li-only or pending) |

See also: [http-server-benchmark-growth.md](http-server-benchmark-growth.md), [lic-httpd-bench-compat.md](lic-httpd-bench-compat.md).
