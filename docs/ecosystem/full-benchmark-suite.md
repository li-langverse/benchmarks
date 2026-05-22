# Full benchmark suite (mandatory after implementation)

Run from the **benchmarks** repo when `lic` (and optionally `lis`) are checked out beside it.

## One command

```bash
cd benchmarks
LIC_ROOT=/workspace/lic ./scripts/run-full-benchmark-suite.sh
./scripts/benchmark-failures-report.sh
cat data/latest/benchmark-matrix.md
```

## Tier ladder

| Tier | What | Default in full suite |
|------|------|------------------------|
| **0** | Correctness (`li-tests`, verify, stability) | yes |
| **1** | Micro vs **cpp** | yes |
| **2** | Physics vs **cpp** | yes |
| **3** | HTTP oracles (nginx, apache, node, li-httpd, …) | yes |
| **4** | HTTP exploits | yes (`SKIP_EXPLOITS=1` to skip) |
| **5** | Ecosystem (compile, security, lip/lit) | **no** — `RUN_TIER5_ECOSYSTEM=1` |

Script paths still use `tier5_http` / `run-tier5-http-bench.sh` on disk; log labels say **tier 3/4**.

## Full matrix (always)

`benchmark-matrix-report.py` writes:

- `data/latest/benchmark-matrix.json` — machine-readable sections + `http_performance` + `http_exploits` grids
- `data/latest/benchmark-matrix.md` — human tables (all catalog rows, HTTP RPS by oracle, exploit pass/fail)

Included automatically at the end of `run-full-benchmark-suite.sh`.

## HTTP exploits (tier 4)

`run-tier5-http-exploits.sh` — `vendor/lis-tier5` harness, profile `pr` by default (`TIER5_EXPLOIT_PROFILE`, `TIER5_EXPLOIT_LANGS`).

Skip only for fast iteration: `SKIP_EXPLOITS=1`. Growth policy: [http-server-benchmark-growth.md](./http-server-benchmark-growth.md).

## What runs

| Step | Source | Output |
|------|--------|--------|
| Build | `setup-lic-for-bench.sh` | `lic/build/compiler/lic/lic`, `lic/build/li-httpd` |
| Tier 0 | `lic/benchmarks/harness/bench.py --tier 0` | `stability.csv`, verify |
| Tier 1+2 | inline tier-1/2 specs | `lic/benchmarks/results/latest.csv` |
| Tier 3 | `run-tier5-http-bench.sh` + `tier5-http-bench.py` | HTTP rows → merged into `latest.csv` |
| Tier 4 | `run-tier5-http-exploits.sh` | `exploit_report.csv` |
| Tier 5 | `bench_ecosystem.py` | optional (`RUN_TIER5_ECOSYSTEM=1`) |
| Ingest | `ingest-lic.sh` | `data/latest/summary.json` |
| Report | `benchmark-failures-report.sh` | RED/YELLOW/GREEN summary |

## HTTP scenarios (tier 3)

**Multi-oracle** (`run-tier5-http-bench.sh` → `vendor/lis-tier5/` harness): compares **nginx**, **apache**, **lighttpd**, **node**, **bun**, and **li-httpd** on each scenario (skips oracles not installed).

| Scenario | What it measures | Oracles compared |
|----------|------------------|------------------|
| `static_small` | 1 KiB static file | nginx, apache, lighttpd, node, bun, li |
| `static_large` | large static payload | same (all static oracles) |
| `keepalive_pipelining` | HTTP/1.1 pipelined keep-alive | same |
| `proxy_loopback` | single-backend reverse proxy loopback | **nginx + li** (+ supplemental `li/li_epoll`, `li/c_epoll`) |
| `lb_round_robin` | 3-backend proxy, round-robin | **nginx + li** only |
| `lb_least_conn` | 3-backend proxy, least-conn | **nginx + li** only |
| `lb_peer_down` | LB with one backend killed mid-run | **nginx + li** only |

Apache/lighttpd/node/bun are **not** wired for proxy/LB yet (`PROXY_ORACLES` in `http_oracles.py`).

Env: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li` · `BENCH_HTTP_PROFILE=nightly` (wrk timing; `ci` is TOML-only)

## Faster iteration

```bash
SKIP_BUILD=1 SKIP_TIER0=1 SKIP_EXPLOITS=1 BENCH_RUNS=1 ./scripts/run-full-benchmark-suite.sh
```

## Ecosystem (tier 5, later)

When compile benches use the same flags as `li-tests` (`--allow-open-vc` where needed):

```bash
RUN_TIER5_ECOSYSTEM=1 ./scripts/run-full-benchmark-suite.sh
```
