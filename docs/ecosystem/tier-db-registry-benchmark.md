# tier_db_registry — registry OLTP vs PostgreSQL

Benchmark tier for **package registry** hot paths: **lidb** (embedded via **lis** `registry-min`) vs **PostgreSQL 15+** on identical DDL.

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_registry/` | Suite config, scenarios, shared schema |
| `scripts/run-db-registry-bench.sh` | Entry stub (writes CI manifest) |
| `data/latest/tier-db-registry.json` | CI ingest artifact |
| `schema/tier-db-registry-ingest.json` | Manifest JSON Schema |
| [`catalog.toml`](../../catalog.toml) | Dashboard rows (`category = database`, `tier = 6`) |

## Scenarios

| `id` | Workload | Metric |
|------|----------|--------|
| `registry_publish` | Insert publisher, package, version, attestation | P95 latency (ms) |
| `registry_read_by_name` | `SELECT` package by name | P95 latency (ms) |
| `registry_read_latest` | Latest version for package | P95 latency (ms) |

DDL: `benchmarks/tier_db_registry/schema/registry-v1.sql` — keep in sync with **lip** / **lidb** registry migrations.

## Run

```bash
cd benchmarks
./scripts/run-db-registry-bench.sh
# Optional timed run (when harness exists):
# BENCH_DB_REGISTRY_PROFILE=nightly BENCH_DB_REGISTRY_RUN_HARNESS=1 ./scripts/run-db-registry-bench.sh
```

Env:

| Variable | Default | Notes |
|----------|---------|-------|
| `BENCH_DB_REGISTRY_PROFILE` | `ci` | `ci` = config-only; `nightly` = P95 timing |
| `POSTGRES_URL` | — | Postgres 15+ with `registry-v1` schema applied |
| `LIDB_URL` / `lis db start` | — | **lis** registry-min profile (WP5) |
| `BENCH_DB_REGISTRY_THRESHOLD` | `1.2` | Max lidb/postgres P95 ratio for green |

## CI ingest

1. `run-db-registry-bench.sh` calls `scripts/ingest/write-tier-db-registry-manifest.py`.
2. Artifact: `data/latest/tier-db-registry.json` (see schema).
3. Future: `benchmarks/tier_db_registry/results/latest.csv` merged into `summary.json` like HTTP CSV rows.

**Honesty:** Until CSV exists, dashboard shows **unknown** for tier-6 database rows — not “lidb slower than Postgres.”

## Plan linkage

| PH | Deliverable |
|----|-------------|
| **PH-DB-1** | `lidb` + `001_registry.sql` |
| **PH-DB-4** | lip registry API + schema |
| **PH-DB-5** | This tier — P95 parity evidence for registry release |

Nightly runs are **optional** (org schedule); PR **ci** profile validates TOML + schema paths only.

## Full suite

Not yet in `run-full-benchmark-suite.sh`. Add when `BENCH_DB_REGISTRY_RUN_HARNESS=1` is stable.
