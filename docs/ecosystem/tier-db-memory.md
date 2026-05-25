# tier_db_memory — RSS idle and peak under load

Benchmark tier for **lidb** memory audit: resident set size at idle and peak under sustained read/write load vs **PostgreSQL 15+**.

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_memory/` | Suite config, scenarios |
| `scripts/run-db-memory-bench.sh` | Entry (stub manifest or lidb harness) |
| `../lidb/scripts/bench/memory_footprint.sh` | Measured harness when `BENCH_DB_MEMORY_RUN_HARNESS=1` |
| `scripts/lidb-bench-stub/memory_footprint.sh` | Fallback stub (exit 0) if lidb script missing |
| `data/latest/tier-db-memory.json` | CI ingest artifact |
| `schema/tier-db-memory-ingest.json` | Manifest JSON Schema |

## Scenarios

| `id` | Measures | Metric |
|------|----------|--------|
| `rss_idle` | Process RSS after cold start | `rss_mb` |
| `rss_peak_load` | Peak RSS under concurrent load | `rss_mb` |

## Run

```bash
./scripts/run-db-memory-bench.sh
# Measured lidb_embed RSS (sibling lidb checkout or benchmarks fallback stub):
BENCH_DB_MEMORY_RUN_HARNESS=1 ./scripts/run-db-memory-bench.sh
```

| Variable | Default | Notes |
|----------|---------|-------|
| `BENCH_DB_MEMORY_PROFILE` | `ci` | `ci` or `nightly` |
| `BENCH_DB_MEMORY_RUN_HARNESS` | `0` | `1` → `lidb/scripts/bench/memory_footprint.sh` or `scripts/lidb-bench-stub/` |
| `LIDB_ROOT` | `../lidb` | Override when lidb is not a sibling |
| `POSTGRES_URL` / `LIDB_URL` | — | Postgres compare oracle (future nightly) |

Target: lidb RSS ≤ `1.1×` postgres (`threshold_ratio_vs_postgres` in `defaults.toml`).

## Plan linkage

**WP-N4** · **PH-DB-MEM**
