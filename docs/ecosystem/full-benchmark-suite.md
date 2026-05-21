# Full benchmark suite (mandatory after implementation)

Run from the **benchmarks** repo when `lic` (and optionally `lis`) are checked out beside it.

## One command

```bash
cd benchmarks
LIC_ROOT=/workspace/lic ./scripts/run-full-benchmark-suite.sh
./scripts/benchmark-failures-report.sh
```

## What runs

| Step | Source | Output |
|------|--------|--------|
| Build | `setup-lic-for-bench.sh` | `lic/build/compiler/lic/lic`, `lic/build/li-httpd` |
| Tier 0 | `lic/benchmarks/harness/bench.py --tier 0` | `stability.csv`, verify |
| Tier 1+2 | `bench.py --tier 12 --runs 3` | `lic/benchmarks/results/latest.csv` |
| Tier 3 | `bench_ecosystem.py` | compile + security rows |
| Tier 5 HTTP | `tier5-http-bench.py` | `http_tier5.csv` → merged into `latest.csv` |
| Ingest | `ingest-lic.sh` | `data/latest/summary.json` |
| Report | `benchmark-failures-report.sh` | RED/YELLOW/GREEN summary |

## HTTP scenarios (tier 5)

**Multi-oracle** (`run-tier5-http-bench.sh` → `vendor/lis-tier5/` harness): compares **nginx**, **apache**, **lighttpd**, **node**, **bun**, and **li-httpd** on each scenario (skips oracles not installed).

- `static_small` — 1 KiB static file
- `keepalive_pipelining` — wrk pipelined keep-alive
- `proxy_loopback` — reverse proxy loopback (nginx + li; supplemental script adds `li/c_epoll`)
- Plus load-balancer scenarios in the vendor suite (`lb_*`, `static_large`) when present in CSV

Env: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li` · `BENCH_HTTP_PROFILE=nightly` (wrk timing; `ci` is TOML-only)

## Faster iteration

```bash
SKIP_BUILD=1 SKIP_TIER0=1 BENCH_RUNS=1 ./scripts/run-full-benchmark-suite.sh
```

## Env

| Variable | Default |
|----------|---------|
| `LIC_ROOT` | `./lic` or `/workspace/lic` |
| `BENCH_RUNS` | `3` (tier 1/2/3) |
| `HTTP_BENCH_RUNS` | `5` (tier 5) |
