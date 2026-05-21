# HTTP webserver RPS matrix (tier 5)

Generated: 2026-05-21T18:19:12.251367+00:00

**Mandatory after every li-httpd change:**
`LIC_ROOT=… ./scripts/run-tier5-http-bench.sh` → `./scripts/benchmark-matrix-report.py`

Source CSV: `/workspace/vendor/lis-tier5/results/latest.csv`

Oracles: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li`. Proxy/LB scenarios bench **nginx + li**; static scenarios bench all oracles.

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|
| static_small | 135,466 | 130,456 | — | — | — | — | 1.04× |
| keepalive_pipelining | 235,097 | 144,627 | — | — | — | — | 1.63× |
| static_large | FAIL | — | — | — | — | — | — |
| proxy_loopback | 9,121 | 52,620 | — | — | — | — | 0.17× |
| lb_round_robin | 9,141 | — | — | — | — | — | — |
| lb_least_conn | 11,405 | — | — | — | — | — | — |
| lb_peer_down | 18,455 | — | — | — | — | — | — |

**Li notes:** `static_large`: wrk_parse_fail_li

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | pass | other oracles N/A |
| https_static | skip | other oracles N/A |

See also: [http-server-benchmark-growth.md](http-server-benchmark-growth.md), [lic-httpd-bench-compat.md](lic-httpd-bench-compat.md).
