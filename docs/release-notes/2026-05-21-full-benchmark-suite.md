# Full benchmark suite — agent workflow

## Summary

Adds `run-full-benchmark-suite.sh` so agents run tier-0 through tier-5 HTTP (multi-oracle webservers + supplemental proxy variants), ingest, and `benchmark-failures-report.sh` after every perf/httpd/compiler/physics change.

## Agent continuation

1. **Read:** `docs/ecosystem/full-benchmark-suite.md`, `AGENTS.md` standing ops #1, `scripts/run-full-benchmark-suite.sh`.
2. **Run:** `LIC_ROOT=../lic ./scripts/setup-lic-for-bench.sh` once; then `./scripts/run-full-benchmark-suite.sh` (fast: `SKIP_BUILD=1 SKIP_TIER0=1 BENCH_RUNS=1 HTTP_BENCH_RUNS=2`).
3. **Then:** Read `./scripts/benchmark-failures-report.sh` and `data/latest/summary.json`; fix RED tier-1/2 in **lic** harness, not dashboard thresholds.
4. **Blocked on:** tier-0 `li-tests` reds (`import_httpd_lib.li`, `import_parse.li`); 10 tier-2 physics specs that fail to build until harness fixes land in **lic**.

## Changed

| Area | Path | Evidence |
|------|------|----------|
| Full suite | `scripts/run-full-benchmark-suite.sh` | tier0 warn-continue; resilient tier1/2 loop; merge `http_tier5.csv` |
| Bench env | `scripts/setup-lic-for-bench.sh` | LLVM 18, clang, libomp, wrk, nginx |
| Multi-oracle HTTP | `vendor/lis-tier5/`, `run-tier5-http-bench.sh` | nginx, apache, lighttpd, node, bun, li per scenario |
| Supplemental proxy | `scripts/tier5-http-bench.py` | `li_epoll` + `c_epoll` vs nginx on `proxy_loopback` |
| Ingest | `scripts/ingest/build_summary.py` | `variant` filter for `li` rows (`proxy_loopback` → `li_epoll`) |
| Catalog | `catalog.toml` | `proxy_loopback` row (`compare_oracle=nginx`) |
| Docs | `docs/ecosystem/full-benchmark-suite.md`, `tooling-catalog.md`, `AGENTS.md` | mandatory post-implementation run |

## Not changed

- `lic` harness kernels (RED: `matmul_*`, `harmonic_oscillator_chain` unchanged by this PR).
- GitHub Actions cron (still no scheduled full-suite; agents run locally).
- **lis** `bench_http.py` stub (tier-5 rows produced from **benchmarks** `tier5-http-bench.py` into `lic` CSV for ingest).

## Breaking

N/A — additive scripts and ingest behavior for HTTP rows with data.

## Security

N/A — local wrk/nginx loopback only; no new trusted surface.

## Performance

N/A — measurement tooling only. Sample run (this env): `static_small` li≈102k vs nginx≈97k RPS; `proxy_loopback` li≈145k vs nginx≈68k RPS.

## Downstream

Agents on **lic** PRs should set `LIC_ROOT` to sibling checkout and run full suite before claiming perf gates; commit `data/latest/summary.json` only when intentionally refreshing dashboard artifacts on **benchmarks** PRs.
