# lic ↔ benchmarks httpd compatibility

**Full RPS table (all scenarios, `li` every row):** [http-server-rps-matrix.md](http-server-rps-matrix.md) — refresh via `./scripts/benchmark-matrix-report.py` after tier-5 benches.

## macOS (darwin arm64) — li-httpd blocker

Tier-5 harness exports **`no_li_httpd_bin`** or **`no_li`** on proxy/LB/static rows when `LI_HTTPD_BIN` is unset or the binary is not built for the host OS.

| Host | `li-httpd` | Dashboard ingest | Honest row color |
|------|------------|------------------|------------------|
| **macOS arm64** (local dev) | Epoll-linked binary not shipped for darwin | `validity_status=pass`, `validity_source=latest.csv:no_li_httpd_bin` (or `no_li`) | **yellow** — nginx/node RPS only (`latest.csv:oracle_only`) |
| **Linux x86_64/aarch64** | Build via `lic` `./scripts/build-li-httpd.sh`, set `LI_HTTPD_BIN` | `lang=li` **rps** rows in `lis` `benchmarks/results/latest.csv` | green/yellow/red vs nginx |

Reproduce oracle-only rows: `BENCH_HTTP_ORACLES=nginx,node ./scripts/run-tier5-http-bench.sh` on macOS (see **lis** `feat/tier5-csv-full` / PR #12).

## Which `lic` checkout for tier-5 HTTP?

| `lic` branch / `main` | `build/li-httpd` | Tier-5 wrk RPS | Routing tests |
|----------------------|------------------|----------------|---------------|
| **`origin/main`** (2026-05-21) | Stub `tcp_*` + `li_rt_httpd` oracle | **Not representative** — do not tune RPS gates on main alone |
| **`cursor/httpd-masterplan-54aa`** / linux `li-net-httpd` | Full epoll proxy/static (`runtime/li_rt_net.c`) | **Use for** `run-full-benchmark-suite.sh`, `httpd-masterplan-step.sh` on **Linux** |

Another agent may advance **`lic` `main`** (routing loader, `lic httpd validate-config`, math-linalg). Rebase the httpd perf branch before claiming bench regressions.

## Commands

```bash
# Full HTTP perf + exploits (canonical today)
LIC_ROOT=/path/to/lic  # checkout cursor/httpd-masterplan-54aa
cd benchmarks
SKIP_BUILD=0 ./scripts/run-full-benchmark-suite.sh
python3 scripts/benchmark-matrix-report.py
```

```bash
# Config-only on latest main
cd lic && ./build/compiler/lic/lic httpd validate-config packages/li-httpd/examples/rate_limit.toml
```

## Merge gate

When epoll `li-httpd` lands on `lic` `main`, re-run step-0 baseline and drop the branch pin in agent notes.
