# Ingest CSV smoke (PH-IO-4)

## Summary

`ingest-lic.sh` runs Li `csv_ingest_smoke.li` (std/io + std/csv from `lic`) before Python `build_summary.py`.

## Agent continuation

1. **Read:** `scripts/ingest/csv_ingest_smoke.li`, `scripts/ingest/ingest-csv-smoke.sh`, `lic` release note `2026-05-16-std-csv-ph-io-4.md`.
2. **Run:** `LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh` (needs built `lic` with PH-IO-4).
3. **Then:** replace `parse_csv` in `build_summary.py` with optional Li helper output.
4. **Blocked on:** human merge; `lic` tag pin in benchmarks workflow.

## Changed

| Area | Path | Evidence |
|------|------|----------|
| Ingest | `scripts/ingest/csv_ingest_smoke.li` | parses `fixtures/lic_sample.csv` |
| Ingest | `scripts/ingest/ingest-csv-smoke.sh` | PASS/FAIL gate |
| Ingest | `scripts/ingest/ingest-lic.sh` | calls smoke first |

## Not changed

- `build_summary.py` logic and `data/latest/summary.json` shape.
- `catalog.toml` still loaded via Python `tomllib`.
- Dashboard Vite bundle.

## Breaking

N/A

## Security

N/A — fixture-only smoke; production CSV paths still validated in `lic` via `std/io` when used.

## Performance

N/A

## Downstream

Pin `lic` commit with `std/csv` before requiring smoke in CI.
