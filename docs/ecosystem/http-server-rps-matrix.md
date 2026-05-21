# HTTP webserver RPS matrix (tier 5)

Generated: 2026-05-21T15:36:04.164886+00:00

**Mandatory after every li-httpd change:**
`LIC_ROOT=… ./scripts/run-tier5-http-bench.sh` → `./scripts/benchmark-matrix-report.py`

Source CSV: `/workspace/vendor/lis-tier5/results/latest.csv`

Oracles: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li`. Proxy/LB scenarios bench **nginx + li**; static scenarios bench all oracles.

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|
| static_small | 138,187 | 75,738 | 50,221 | 174,234 | — | — | 1.82× |
| keepalive_pipelining | 224,312 | 89,075 | 64,828 | 246,989 | — | — | 2.52× |
| static_large | 9,170 | 8,919 | 8,955 | 9,171 | — | — | 1.03× |
| proxy_loopback | FAIL | 58,205 | 40,708 | 24,620 | — | — | — |
| lb_round_robin | FAIL | 44,099 | 39,429 | 27,498 | — | — | — |
| lb_least_conn | FAIL | 67,105 | 39,648 | 23,680 | — | — | — |
| lb_peer_down | FAIL | 56,543 | 48,268 | 20,694 | — | — | — |

**Li notes:** `lb_least_conn`: verify_fail_li:/; `lb_peer_down`: verify_fail_li:/; `lb_round_robin`: verify_fail_li:/; `proxy_loopback`: verify_fail_li:/

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | pass | other oracles N/A |
| https_static | skip | apache=817; lighttpd=899 |

See also: [http-server-benchmark-growth.md](http-server-benchmark-growth.md), [lic-httpd-bench-compat.md](lic-httpd-bench-compat.md).
