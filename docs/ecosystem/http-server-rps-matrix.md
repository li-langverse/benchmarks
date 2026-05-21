# HTTP webserver RPS matrix (tier 5)

Generated: 2026-05-21T14:23:39.671407+00:00

**Mandatory after every li-httpd change:**
`LIC_ROOT=… ./scripts/run-tier5-http-bench.sh` → `./scripts/benchmark-matrix-report.py`

Source CSV: `/workspace/vendor/lis-tier5/results/latest.csv`

Oracles: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li`. Proxy/LB scenarios bench **nginx + li**; static scenarios bench all oracles.

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|
| static_small | 106,609 | 68,611 | 45,209 | 155,758 | 24,351 | — | 1.55× |
| keepalive_pipelining | 226,251 | 71,244 | 52,984 | 197,438 | 22,541 | — | 3.18× |
| static_large | 7,586 | 9,046 | 6,863 | 8,125 | 2,427 | — | 0.84× |
| proxy_loopback | 133,784 | 77,971 | — | — | — | — | 1.72× |
| lb_round_robin | 129,995 | 43,829 | — | — | — | — | 2.97× |
| lb_least_conn | 134,988 | 52,017 | — | — | — | — | 2.60× |
| lb_peer_down | 126,265 | 62,964 | — | — | — | — | 2.01× |

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | pass | N/A (li-only or pending) |
| https_static | skip | N/A (li-only or pending) |

See also: [http-server-benchmark-growth.md](http-server-benchmark-growth.md), [lic-httpd-bench-compat.md](lic-httpd-bench-compat.md).
