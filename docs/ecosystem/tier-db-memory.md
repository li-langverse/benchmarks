# tier_db_memory — RSS idle and peak under load

Benchmark tier for **lidb** memory audit: resident set size at idle and peak under sustained read/write load vs **PostgreSQL 15+**.

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_memory/` | Suite config, scenarios |
| `scripts/run-db-memory-bench.sh` | Entry stub |
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
```

Env: `BENCH_DB_MEMORY_PROFILE`, `BENCH_DB_MEMORY_RUN_HARNESS`, `POSTGRES_URL`, `LIDB_URL`.

Target: lidb RSS ≤ `1.1×` postgres (`threshold_ratio_vs_postgres` in `defaults.toml`).

## Plan linkage

**WP-N4** · **PH-DB-MEM**
