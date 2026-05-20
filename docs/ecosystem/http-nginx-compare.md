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

## Next: Li vs nginx

1. **lic** — P0 net/http + real `httpd_serve` ([httpd-prerequisites](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/httpd-prerequisites.md)).
2. **lis** — wire `LI_HTTPD_BIN` in `bench_http.py` (second wrk pass, `lang=li` row).
3. Remove **vendor/lis-tier5** after **lis** harness is on `main`.
