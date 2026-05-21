# HTTP webserver RPS matrix (tier 5)

Generated: 2026-05-21T15:13:50.015067+00:00

**Mandatory after every li-httpd change:**
`LIC_ROOT=… ./scripts/run-tier5-http-bench.sh` → `./scripts/benchmark-matrix-report.py`

Source CSV: `/workspace/vendor/lis-tier5/results/latest.csv`

Oracles: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li`. Proxy/LB scenarios bench **nginx + li**; static scenarios bench all oracles.

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|
| static_small | 104,305 | 84,019 | 53,408 | 135,400 | — | — | 1.24× |
| keepalive_pipelining | 146,792 | 78,313 | 59,730 | 245,283 | — | — | 1.87× |
| static_large | — | 9,115 | 6,843 | 8,236 | — | — | — |
| proxy_loopback | — | 58,666 | 42,460 | 22,475 | — | — | — |
| lb_round_robin | — | 40,145 | 41,075 | 20,543 | — | — | — |
| lb_least_conn | — | 53,067 | 41,041 | 24,175 | — | — | — |
| lb_peer_down | — | 52,824 | 41,257 | 19,655 | — | — | — |

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | — | other oracles N/A |
| https_static | skip | apache=811; lighttpd=866 |

See also: [http-server-benchmark-growth.md](http-server-benchmark-growth.md), [lic-httpd-bench-compat.md](lic-httpd-bench-compat.md).
