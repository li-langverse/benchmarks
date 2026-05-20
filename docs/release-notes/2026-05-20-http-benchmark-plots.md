# HTTP tier-5 benchmark plots (lis nginx baseline)

## Summary

Adds matplotlib PNG generation for tier-5 HTTP rows in **benchmarks** (`plot_http_benchmarks.py`) and a local runner that does **not** mutate `data/latest/summary.json`, so it can run alongside ingest work on other branches.

## Agent continuation

1. **Read:** `scripts/plot_http_benchmarks.py`, `scripts/run-http-benchmark-report.sh`, `scripts/render-benchmark-visuals.sh`.
2. **Run:** `LIS_ROOT=../lis ./scripts/run-http-benchmark-report.sh` (requires `nginx` + `wrk` on Linux; `pip install matplotlib`).
3. **Then:** merge **lis** harness PR (`bench_http.py` CSV) first; use `ingest-lic.sh` on **main** only when **lic** `latest.csv` is present so physics rows are not cleared to `unknown`.
4. **Blocked on:** `lang=li` RPS rows until **li-httpd** is wired; dashboard `ratio_vs_reference` stays null with nginx-only series.

## Changed

| Area | Path | Evidence |
|------|------|----------|
| Plot script | `scripts/plot_http_benchmarks.py` | PNG per scenario + overview |
| Runner | `scripts/run-http-benchmark-report.sh` | lis bench + plot, no summary ingest |
| Visuals | `scripts/render-benchmark-visuals.sh` | lis CSV path; lic plot non-fatal |
| Manifest | `scripts/visual-manifest.py` | `http_priority` list |

## Not changed

- `.github/workflows/*` (leave to `cursor/ingest-lis-checkout-54aa` / other agents).
- `dashboard/` Vite sources (`cursor/li-plot-ph-io-5-c9a5` territory).
- `catalog.toml` or `scripts/ingest/build_summary.py`.
- Committed `data/latest/summary.json` on this PR (local runs only).

## Breaking

N/A — additive scripts; `render-benchmark-visuals.sh` exits 0 when lis HTTP plots succeed even if lic venv plot fails.

## Security

N/A — reads local CSV/JSON; plots written under `data/visuals/latest/` (gitignored PNGs).

## Performance

Local **wrk** load (~3s per scenario in `ci` profile); matplotlib render &lt;1s.

## Downstream

After **lis** `results/latest.csv` lands in CI artifacts, wire optional upload + `ingest-lic.sh` on a coordinated PR; do not parallel-edit `summary.json` without **lic** bench CSV.
