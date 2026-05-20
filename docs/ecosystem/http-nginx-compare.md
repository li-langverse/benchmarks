# HTTP benchmarks vs nginx (tier-5)

## Oracle

[`catalog.toml`](../../catalog.toml) rows `static_small` and `keepalive_pipelining` use `compare_oracle = "nginx"` and metric **`rps`**. The dashboard shows **`ratio_vs_reference`** only when both **`lang=nginx`** and **`lang=li`** RPS rows exist (threshold `1.0` = match or beat nginx on throughput).

## Repos

| Repo | Role |
|------|------|
| **lis** | `benchmarks/tier5_http/harness/bench_http.py` — stock nginx + wrk → `results/latest.csv` |
| **benchmarks** | Ingest (`ingest-lic.sh`, `merge_lis_http_into_summary.py`), plots (`plot_http_benchmarks.py`), dashboard |
| **lic** | `packages/li-net-httpd` — **`httpd_serve`** still stub; blocks **`lang=li`** rows |

Until **lis** `main` ships the harness, **benchmarks** vendors a copy under [`vendor/lis-tier5/`](../../vendor/lis-tier5/README.md). Sync with `./scripts/sync-lis-tier5-vendor.sh`.

## Local run

```bash
sudo apt-get install -y nginx wrk
pip install matplotlib  # optional plots

# Bench (vendor or lis checkout)
python3 vendor/lis-tier5/benchmarks/tier5_http/harness/bench_http.py --profile ci

# Merge HTTP into dashboard data without wiping lic rows (when lic CSV absent)
python3 scripts/ingest/merge_lis_http_into_summary.py vendor/lis-tier5/results/latest.csv

# Plots
LIS_ROOT=$PWD/vendor/lis-tier5 ./scripts/run-http-benchmark-report.sh
```

Full ingest when **lic** `benchmarks/results/latest.csv` exists:

```bash
LIC_ROOT=../lic LIS_ROOT=../lis ./scripts/ingest/ingest-lic.sh
```

## CI

- **Benchmarks CI** runs vendored `bench_http.py`, then `ingest-lic.sh` (HTTP merge if no lic CSV).
- **Ingest workflow** accepts `repository_dispatch` types `lic-bench-complete` and `lis-bench-complete`.

## Li vs nginx (M0 static server, local ci profile)

Example measured rows (`bench_http.py --profile ci`, Linux):

| Scenario | nginx RPS | li RPS (`build/li-httpd`) | nginx/li (dashboard `ratio_vs_reference`) |
|----------|-----------|---------------------------|-------------------------------------------|
| `static_small` | ~66k | ~13k | ~5.25 (red until ≤1.0 threshold) |
| `keepalive_pipelining` | ~76k | ~12k | ~6.21 |

M0 **li-httpd** uses trusted POSIX seam [`runtime/li_rt_net.c`](https://github.com/li-langverse/lic/blob/main/runtime/li_rt_net.c) (fork-per-connection, minimal HTTP/1.1). Not yet a proved Li parser/router.

## Next steps

1. Merge **lic** branch `cursor/httpd-serve-m0-54aa` (human push — bot 403).
2. Merge **benchmarks** #45 and **lis** harness PR; drop **vendor/lis-tier5** when upstream has harness.
3. Parser proofs, keep-alive in Li server, async reactor — close gap vs nginx.
