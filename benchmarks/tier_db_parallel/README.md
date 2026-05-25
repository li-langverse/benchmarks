# tier_db_parallel — Parallel

Full-spectrum **lidb** audit benchmark tier (WP-N4 stub). Harness compares **lidb** vs **PostgreSQL 15+** where applicable.

## Scenarios

| Scenario | Measures | Primary metric |
|----------|----------|----------------|
| `concurrent_readers` | Scalable concurrent SELECT throughput | `ops_per_sec` (ops) |
| `concurrent_writers` | Scalable concurrent INSERT/UPDATE throughput | `ops_per_sec` (ops) |

## Run

```bash
cd benchmarks
./scripts/run-db-parallel-bench.sh
BENCH_DB_PARALLEL_RUN_HARNESS=1 ./scripts/run-db-parallel-bench.sh
cat data/latest/tier-db-parallel.json
```

Env: `BENCH_DB_PARALLEL_PROFILE=ci|nightly`, `BENCH_DB_PARALLEL_RUN_HARNESS`, `LIDB_ROOT`, `POSTGRES_URL`, `LIDB_URL`.

## CI ingest

Manifest: `data/latest/tier-db-parallel.json` — see [`schema/tier-db-parallel-ingest.json`](../../schema/tier-db-parallel-ingest.json).

Doc: [tier-db-parallel.md](../../docs/ecosystem/tier-db-parallel.md).
