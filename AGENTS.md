# Agent instructions (benchmarks)

1. **PR-only** — branch + PR; CI green; reviewer merges; do not self-merge.
2. **Do not** copy `lic/benchmarks/harness` into this repo.
3. Update `catalog.toml` via PR when adding index entries.
4. `data/latest/summary.json` is produced by **ingest CI** — do not hand-edit unless fixing ingest.
5. After perf work in `lic`, check the [dashboard](https://li-langverse.github.io/benchmarks/).
