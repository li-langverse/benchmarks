# HTTP webserver RPS matrix (tier 5)

Generated: 2026-05-29T07:25:29.778537+00:00

**Mandatory after every li-httpd change:**
`LIC_ROOT=… ./scripts/run-tier5-http-bench.sh` → `./scripts/benchmark-matrix-report.py`

Source CSV: `/home/s4il0r/Documents/Cursor/li-langverse/benchmarks/vendor/lis-tier5/results/latest.csv`

Oracles: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li`. Proxy/LB scenarios bench **nginx + li**; static scenarios bench all oracles.

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|
| static_small | — | 12,087 | — | — | 4,626 | — | — |
| keepalive_pipelining | — | 22,604 | — | — | 15,817 | — | — |
| static_large | — | 4,149 | — | — | 1,805 | — | — |
| proxy_loopback | no bin | 21,415 | — | — | — | — | — |
| lb_round_robin | no bin | 24,167 | — | — | — | — | — |
| lb_least_conn | no bin | 24,309 | — | — | — | — | — |
| lb_peer_down | no bin | 25,179 | — | — | — | — | — |

**Li notes:** `lb_least_conn`: no_li_httpd_bin; `lb_peer_down`: no_li_httpd_bin; `lb_round_robin`: no_li_httpd_bin; `proxy_loopback`: no_li_httpd_bin

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | no_li_httpd_bin | other oracles N/A |
| https_static | skip | nginx=583 |

See also: [http-server-benchmark-growth.md](http-server-benchmark-growth.md), [lic-httpd-bench-compat.md](lic-httpd-bench-compat.md).
