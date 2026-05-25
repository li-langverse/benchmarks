# tier_db_realtime — Realtime

Full-spectrum **lidb** audit benchmark tier (WP-N4 stub). Harness compares **lidb** vs **PostgreSQL 15+** where applicable.

## Scenarios

| Scenario | Measures | Primary metric |
|----------|----------|----------------|
| `ws_publish_latency` | WebSocket publish→client delivery P95 | `latency_p95` (ms) |

## Run (stub)

```bash
cd benchmarks
./scripts/run-db-realtime-bench.sh
cat data/latest/tier-db-realtime.json
```

Env: `BENCH_DB_REALTIME_PROFILE=ci|nightly`, `POSTGRES_URL`, `LIDB_URL`.

## CI ingest

Manifest: `data/latest/tier-db-realtime.json` — see [`schema/tier-db-realtime-ingest.json`](../../schema/tier-db-realtime-ingest.json).

Doc: [tier-db-realtime.md](../../docs/ecosystem/tier-db-realtime.md).
