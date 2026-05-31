# Zero-missing benchmark dashboard data

Goal: every row in `data/latest/summary.json` has real measurements (no `status: skip`), every catalog entry has a harness and workload on disk, and competitive `lig` GPU data is published.

## Gates

```bash
python3 scripts/audit/zero-missing-data-report.py   # writes data/latest/zero-missing-data-report.json
python3 scripts/check-zero-missing-data.py          # exit 1 until all blocking counts are 0
```

Blocking counts:

| Key | Meaning |
|-----|---------|
| `summary_skip_rows` | Matrix rows with no ingested series |
| `catalog_without_csv` | Catalog ids with no matching `results/latest.csv` benchmark |
| `harness_pending` | Catalog `size_label = harness pending` |
| `workload_dir_missing` | `path` does not resolve under `benchmarks/workloads/` |

Nightly `publish-dashboard` runs `check-zero-missing-data.py` before committing; the push only lands when the merged multi-OS CSV fills the matrix.

## How to get to zero

1. **Green nightly** — parallel tier jobs → `merge-benchmark-tier-csvs.sh` → `ingest-lic.sh` → `build_summary.py`.
2. **Catalog paths** — `python3 scripts/catalog/fix-catalog-workload-paths.py` (paths use `benchmarks/workloads/tier*`, not legacy `benchmarks/tier*`).
3. **Harness backlog** — clear `harness_pending` entries in `catalog.toml` (implement bench or mark `catalog_lifecycle = planned` and exclude from matrix).
4. **lig competitive** — run `bench-lig-gpu-suite.sh` in lic, `submit-gpu-contribution.sh`, ensure `lig-gpu-matrix.json` is regenerated on ingest.
5. **Local full run** — `./scripts/run-full-benchmark-suite.sh` then ingest; commit only after `check-zero-missing-data.py` passes.

## Current baseline (pre-full nightly)

Committed `summary.json` is mostly skip until the first successful `publish-dashboard` after nightly #280+.
