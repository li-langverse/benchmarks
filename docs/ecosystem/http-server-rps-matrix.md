# HTTP webserver RPS matrix (tier 5)

Generated: 2026-06-03T05:06:04.925840+00:00

**Mandatory after every li-httpd change:**
`LIC_ROOT=… ./scripts/run-tier5-http-bench.sh` → `./scripts/benchmark-matrix-report.py`

Source CSV: `/mnt/c/Users/Julian/Documents/Programming/li/benchmarks/vendor/lis-tier5/results/latest.csv`

Oracles: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li`. Proxy/LB scenarios bench **nginx + li**; static scenarios bench all oracles.

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | caddy | traefik | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|---|---|
| static_small | 6,191 | 122 | 643 | 6,440 | — | — | 2,689 | — | 50.60× |
| keepalive_pipelining | 6,503 | 124 | 1,714 | 6,715 | — | — | 3,034 | — | 52.27× |
| static_large | FAIL | 94 | 515 | 185 | — | — | 287 | — | — |
| proxy_loopback | 33,683 | 125 | 126 | 105 | — | — | — | — | 268.94× |
| lb_round_robin | 32,033 | 2,099 | 2,073 | 1,856 | — | — | — | — | 15.26× |
| lb_least_conn | 32,790 | 2,056 | 1,920 | 1,853 | — | — | — | — | 15.95× |
| lb_peer_down | 30,555 | 2,002 | 2,095 | 1,918 | — | — | — | — | 15.26× |

**Li notes:** `lb_least_conn`: verify_fail_caddy:/; `lb_peer_down`: verify_fail_caddy:/; `lb_round_robin`: verify_fail_caddy:/; `static_large`: wrk_parse_fail_li

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | pass | other oracles N/A |
| https_static | — | li=5,993; nginx=114; apache=1,049; lighttpd=6,074; caddy=2,064; traefik=120 |
| https_tls_matrix | — | li=5,677; nginx=312; apache=1,780; lighttpd=5,541; caddy=2,484; traefik=515 |

See also: [http-server-benchmark-growth.md](http-server-benchmark-growth.md), [lic-httpd-bench-compat.md](lic-httpd-bench-compat.md).
