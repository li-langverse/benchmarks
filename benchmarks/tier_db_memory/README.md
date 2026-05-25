# tier_db_memory — Memory

Full-spectrum **lidb** audit benchmark tier (WP-N4 stub). Harness compares **lidb** vs **PostgreSQL 15+** where applicable.

## Scenarios

| Scenario | Measures | Primary metric |
|----------|----------|----------------|
| `rss_idle` | Process RSS after cold start (idle) | `rss_mb` (mb) |
| `rss_peak_load` | Peak RSS under sustained read/write load | `rss_mb` (mb) |

## Run (stub)

```bash
cd benchmarks
./scripts/run-db-memory-bench.sh
cat data/latest/tier-db-memory.json
```

Env: `BENCH_DB_MEMORY_PROFILE=ci|nightly`, `POSTGRES_URL`, `LIDB_URL`.

## CI ingest

Manifest: `data/latest/tier-db-memory.json` — see [`schema/tier-db-memory-ingest.json`](../../schema/tier-db-memory-ingest.json).

Doc: [tier-db-memory.md](../../docs/ecosystem/tier-db-memory.md).
