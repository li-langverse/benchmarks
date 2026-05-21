# Vendored lis tier-5 HTTP harness (temporary)

Mirrors **`li-langverse/lis`** `benchmarks/tier5_http/` until the upstream PR with **nginx + wrk** CSV lands on **lis** `main`.

## Sync from a lis checkout

```bash
LIS_ROOT=../lis ./scripts/sync-lis-tier5-vendor.sh
```

## Run (benchmarks CI / local)

```bash
sudo apt-get install -y nginx wrk
export LIS_ROOT="$PWD/vendor/lis-tier5"
python3 "$LIS_ROOT/benchmarks/tier5_http/harness/bench_http.py" --profile ci
python3 scripts/ingest/merge_lis_http_into_summary.py "$LIS_ROOT/results/latest.csv"
```

## Li vs nginx

- **`lang=nginx`** **`rps`** rows: **ready** on Linux with nginx + wrk.
- **`lang=li`** **`rps`**: requires **`lic`** `li-net-httpd` / **`LI_HTTPD_BIN`** wiring (not shipped yet).

Remove this vendor tree after **lis** `main` includes the harness and benchmarks CI checks out **lis** only.
