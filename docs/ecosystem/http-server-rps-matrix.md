# HTTP webserver RPS matrix (tier 5)

Generated: 2026-06-07T07:34:38.685658+00:00

**Mandatory after every li-httpd change:**
`LIC_ROOT=… ./scripts/run-tier5-http-bench.sh` → `./scripts/benchmark-matrix-report.py`

Source CSV: `/mnt/c/Users/Julian/Documents/Programming/li/benchmarks/vendor/lis-tier5/results/latest.csv`

Oracles: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li`. Proxy/LB scenarios bench **nginx + li**; static scenarios bench all oracles.

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | caddy | traefik | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|---|---|
| static_small | 4,030 | 109 | 660 | 5,171 | — | — | 1,759 | — | 37.00× |
| keepalive_pipelining | 5,457 | 149 | 1,426 | 6,528 | — | — | 2,845 | — | 36.58× |
| static_large | FAIL | 71 | 448 | 171 | — | — | 265 | — | — |
| proxy_loopback | 32,327 | 120 | 120 | 120 | — | — | — | — | 268.83× |
| proxy_post_json | — | — | — | — | — | — | — | — | — |
| lb_round_robin | 32,750 | 2,040 | 2,071 | 1,914 | — | — | — | — | 16.05× |
| lb_least_conn | 30,280 | 2,010 | 1,958 | 1,804 | — | — | — | — | 15.07× |
| lb_sticky_cookie | — | — | — | — | — | — | — | — | — |
| lb_peer_down | 32,265 | 1,940 | 1,884 | 1,827 | — | — | — | — | 16.63× |
| tls_dhe_handshake | — | — | — | — | — | — | — | — | — |

**Li notes:** `lb_least_conn`: verify_fail_caddy:/; `lb_peer_down`: verify_fail_caddy:/; `lb_round_robin`: verify_fail_caddy:/; `proxy_loopback`: verify_fail_caddy:/; `static_large`: wrk_parse_fail_li

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | pass | other oracles N/A |
| https_static | — | li=5,868; nginx=112; apache=1,041; lighttpd=5,706; caddy=1,706; traefik=120 |
| https_tls_matrix | — | li=5,688; nginx=119; apache=1,530; lighttpd=5,907; caddy=2,467; traefik=116 |

See also: [http-server-benchmark-growth.md](http-server-benchmark-growth.md), [lic-httpd-bench-compat.md](lic-httpd-bench-compat.md).
