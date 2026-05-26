# tier_db_registry — registry OLTP benchmarks

Compare **lidb** (via **lis** `registry-min` profile) against **PostgreSQL 15+** on the same schema for package-registry hot paths.

## Scenarios

| Scenario | OLTP path | Primary metric |
|----------|-----------|----------------|
| `registry_publish` | Insert package + version + attestation | P95 latency (ms) |
| `registry_read_by_name` | Lookup package by name | P95 latency (ms) |
| `registry_read_latest` | Latest version for package name | P95 latency (ms) |

## Profiles

| Profile | Timing | When |
|---------|--------|------|
| `ci` | off (config validation only) | PR smoke |
| `nightly` | on (P95 vs Postgres) | Scheduled / manual |

## Schema

Shared DDL: [`schema/registry-v1.sql`](schema/registry-v1.sql) — aligned with **lip** `registry/schema/registry-v1.sql` and **lidb** `migrations/001_registry.sql` (WP1).

## Run

```bash
cd benchmarks
# CI dry-run: validate suite/scenarios/schema + stub manifest (default)
./scripts/run-db-registry-bench.sh

# SQLite stub timing (plumbing only — not lidb/postgres P95 evidence)
BENCH_DB_REGISTRY_RUN_HARNESS=1 BENCH_DB_REGISTRY_PROFILE=nightly ./scripts/run-db-registry-bench.sh

# Validate harness only
python3 benchmarks/tier_db_registry/harness/registry_oltp_stub.py --validate-only

cat data/latest/tier-db-registry.json
```

| Path | Role |
|------|------|
| `fixtures/seed.toml` | Reproducible publisher/package seed |
| `schema/registry-sqlite-v1.sql` | SQLite subset for local stub |
| `harness/registry_oltp_stub.py` | Validate + optional `--run-timing` |
| `results/latest.csv` | Emitted when harness timing runs |

Env: `BENCH_DB_REGISTRY_PROFILE=ci|nightly`, `BENCH_DB_REGISTRY_RUN_HARNESS=1`, `POSTGRES_URL`, `LIDB_URL` / `lis db start` (real P95 runs).

## CI ingest

Manifest: `data/latest/tier-db-registry.json` (schema: [`schema/tier-db-registry-ingest.json`](../../schema/tier-db-registry-ingest.json)).

CSV rows (future): `benchmarks/tier_db_registry/results/latest.csv` with columns `benchmark,lang,metric,value,unit,variant`.

## Plan

**PH-DB-5** — document P95 vs Postgres; dashboard **unknown** until harness produces CSV. See [tier-db-registry-benchmark.md](../../docs/ecosystem/tier-db-registry-benchmark.md).
