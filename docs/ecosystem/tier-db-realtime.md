# tier_db_realtime — WebSocket publish→client latency

Benchmark tier for **lidb** realtime: P95 latency from server publish to WebSocket client delivery vs **PostgreSQL 15+** (logical replication / listen-notify baseline).

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_realtime/` | Suite config, scenarios |
| `scripts/run-db-realtime-bench.sh` | Entry stub |
| `data/latest/tier-db-realtime.json` | CI ingest artifact |

## Scenarios

| `id` | Measures | Metric |
|------|----------|--------|
| `ws_publish_latency` | Publish event → client WS frame | `latency_p95` (ms) |

## Run

```bash
./scripts/run-db-realtime-bench.sh
```

Env: `BENCH_DB_REALTIME_PROFILE`, `BENCH_DB_REALTIME_RUN_HARNESS`, `LIDB_WS_URL`, `POSTGRES_URL`.

Target: lidb P95 ≤ `1.2×` postgres (`threshold_ratio_vs_postgres`).

## Plan linkage

**WP-N4** · **PH-DB-RT**
