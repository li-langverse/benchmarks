# Tier-5 HTTP benchmarks (`li-httpd` · nginx oracle)

## What runs today

`harness/bench_http.py` validates each scenario’s `bench.toml`, then — when `nginx` and `wrk` are on `PATH` — starts **stock nginx** in a private prefix serving `fixtures/static/`, runs **wrk**, and writes **`results/latest.csv`** (same column schema as `lic` bench exports).

Profiles come from `suite.toml`:

| Profile   | Timing | wrk duration (typical) |
|-----------|--------|-------------------------|
| `ci`      | off    | capped (default 3s via `BENCH_HTTP_QUICK_SEC`) |
| `nightly` | on     | uses `[load].duration_sec` from each scenario |

Scenarios in `suite.toml` **ci** / **nightly**: `static_small`, `keepalive_pipelining`, `static_large` (GET `/file.bin`, 1 MiB fixture auto-generated).

`lang=li` throughput rows are **not** emitted until a `li-httpd` binary is wired in; set `LI_HTTPD_BIN` only as a placeholder hook for future work.

## Quick commands (from lis repo root)

```bash
# TOML-only / harness rows (no nginx)
python3 benchmarks/tier5_http/harness/bench_http.py --profile ci --no-bench

# Full nginx + wrk (install deps first, Linux example)
sudo apt-get install -y nginx wrk
python3 benchmarks/tier5_http/harness/bench_http.py --profile ci
cat results/latest.csv
```

Single scenario:

```bash
python3 benchmarks/tier5_http/harness/bench_http.py static_small --profile nightly
```

## Downstream ingest

The **benchmarks** repo merges `lis/results/latest.csv` when building `data/latest/summary.json` (`compare_oracle = "nginx"` for tier-5 HTTP rows in `catalog.toml`).
