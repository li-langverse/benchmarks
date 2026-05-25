# tier_db_parallel — concurrent readers and writers

Benchmark tier for **lidb** parallel scalability: concurrent reader and writer throughput vs **PostgreSQL 15+**.

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_parallel/` | Suite config, scenarios |
| `scripts/run-db-parallel-bench.sh` | Entry stub |
| `data/latest/tier-db-parallel.json` | CI ingest artifact |

## Scenarios

| `id` | Measures | Metric |
|------|----------|--------|
| `concurrent_readers` | `SELECT` throughput at N clients | `ops_per_sec` |
| `concurrent_writers` | `INSERT`/`UPDATE` throughput at N clients | `ops_per_sec` |

## Run

```bash
./scripts/run-db-parallel-bench.sh
```

Env: `BENCH_DB_PARALLEL_PROFILE`, `BENCH_DB_PARALLEL_RUN_HARNESS`, `POSTGRES_URL`, `LIDB_URL`.

Green when lidb `ops_per_sec` ≥ postgres (ratio threshold `1.0`).

## Plan linkage

**WP-N4** · **PH-DB-PAR**
