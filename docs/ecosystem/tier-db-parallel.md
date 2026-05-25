# tier_db_parallel — concurrent readers and writers

Benchmark tier for **lidb** parallel scalability: concurrent reader and writer throughput vs **PostgreSQL 15+**.

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_parallel/` | Suite config, scenarios |
| `scripts/run-db-parallel-bench.sh` | Entry (stub manifest or lidb harness) |
| `../lidb/scripts/bench/parallel_load.sh` | Measured harness when `BENCH_DB_PARALLEL_RUN_HARNESS=1` |
| `scripts/lidb-bench-stub/parallel_load.sh` | Fallback stub (exit 0) if lidb script missing |
| `data/latest/tier-db-parallel.json` | CI ingest artifact |

## Scenarios

| `id` | Measures | Metric |
|------|----------|--------|
| `concurrent_readers` | `SELECT` throughput at N clients | `ops_per_sec` |
| `concurrent_writers` | `INSERT`/`UPDATE` throughput at N clients | `ops_per_sec` |

## Run

```bash
./scripts/run-db-parallel-bench.sh
# Measured concurrent reader ops (lidb_embed); writers scenario may stay stub in harness:
BENCH_DB_PARALLEL_RUN_HARNESS=1 ./scripts/run-db-parallel-bench.sh
```

| Variable | Default | Notes |
|----------|---------|-------|
| `BENCH_DB_PARALLEL_PROFILE` | `ci` | `ci` or `nightly` |
| `BENCH_DB_PARALLEL_RUN_HARNESS` | `0` | `1` → `lidb/scripts/bench/parallel_load.sh` or `scripts/lidb-bench-stub/` |
| `LIDB_ROOT` | `../lidb` | Override when lidb is not a sibling |
| `POSTGRES_URL` / `LIDB_URL` | — | Postgres compare oracle (future nightly) |

Green when lidb `ops_per_sec` ≥ postgres (ratio threshold `1.0`).

## Plan linkage

**WP-N4** · **PH-DB-PAR**
