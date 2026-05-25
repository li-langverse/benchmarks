# HTTP webserver RPS matrix (tier 5)

Generated: 2026-05-25T17:47:38.843477+00:00

**Mandatory after every li-httpd change:**
`LIC_ROOT=… ./scripts/run-tier5-http-bench.sh` → `./scripts/benchmark-matrix-report.py`

Source CSV: `/Users/julian/Documents/coding-projects/benchmarks/vendor/lis-tier5/results/latest.csv`

Oracles: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li`. Proxy/LB scenarios bench **nginx + li**; static scenarios bench all oracles.

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|
| static_small | — | 17,365 | — | — | 7,592 | — | — |
| keepalive_pipelining | — | 25,032 | — | — | 15,010 | — | — |
| static_large | — | 4,057 | — | — | 1,107 | — | — |
| proxy_loopback | no bin | 12,373 | — | — | — | — | — |
| lb_round_robin | no bin | 20,458 | — | — | — | — | — |
| lb_least_conn | no bin | 11,998 | — | — | — | — | — |
| lb_peer_down | no bin | 25,578 | — | — | — | — | — |

**Li notes:** `lb_least_conn`: no_li_httpd_bin; `lb_peer_down`: no_li_httpd_bin; `lb_round_robin`: no_li_httpd_bin; `proxy_loopback`: no_li_httpd_bin

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | no_li_httpd_bin | other oracles N/A |
| https_static | — | nginx=362 |

See also: [http-server-benchmark-growth.md](http-server-benchmark-growth.md), [lic-httpd-bench-compat.md](lic-httpd-bench-compat.md).
