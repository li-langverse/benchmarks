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

- `static_small` — 1 KiB file, li-httpd epoll vs nginx
- `keepalive_pipelining` — wrk Lua pipeline depth 8 (Debian wrk lacks `--pipeline`)
- `proxy_loopback` — Li epoll (default), `LI_HTTPD_PROXY_C=1`, nginx oracle

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
