# tier_db_registry — registry OLTP vs PostgreSQL

Benchmark tier for **package registry** hot paths: **lidb** (`lidb_embed`) vs **PostgreSQL 15+** on registry OLTP workloads.

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_registry/` | Suite config, scenarios, shared schema, harness |
| `benchmarks/tier_db_registry/harness/registry_oltp.py` | Real lidb + Postgres compare |
| `benchmarks/tier_db_registry/harness/registry_oltp_stub.py` | Validate + SQLite stub |
| `scripts/run-db-registry-bench.sh` | CI validate + optional harness |
| `lidb/scripts/bench/registry_oltp.sh` | Build embed + invoke benchmarks harness |
| `data/latest/tier-db-registry.json` | CI ingest artifact |
| [`catalog.toml`](../../catalog.toml) | Dashboard rows (`category = database`, `tier = 6`) |

## Scenarios

| `id` | Workload | Metric |
|------|----------|--------|
| `registry_publish` | Insert publisher, package, version, attestation | P95 latency (ms) |
| `registry_read_by_name` | `SELECT` package by name | P95 latency (ms) |
| `registry_read_latest` | Latest version for package | P95 latency (ms) |

DDL: `benchmarks/tier_db_registry/schema/registry-v1.sql` (Postgres oracle). **lidb** uses `migrations/001_registry.sql` (UUID schema; equivalent hot paths).

## Run

```bash
cd benchmarks
# Default (CI): validate tier layout + stub manifest — no lidb/postgres
./scripts/run-db-registry-bench.sh

# Real compare (local / nightly)
export LIDB_ROOT=../lidb POSTGRES_URL='postgresql://...'
pip install -r benchmarks/tier_db_registry/harness/requirements-registry.txt
BENCH_DB_REGISTRY_RUN_HARNESS=1 BENCH_DB_REGISTRY_PROFILE=nightly \
  BENCH_DB_REGISTRY_ENGINE=compare ./scripts/run-db-registry-bench.sh
```

Env:

| Variable | Default | Notes |
|----------|---------|-------|
| `BENCH_DB_REGISTRY_PROFILE` | `ci` | `ci` = validate-only in PR; `nightly` = full measure_iters |
| `BENCH_DB_REGISTRY_RUN_HARNESS` | `0` | `1` enables timing harness |
| `BENCH_DB_REGISTRY_ENGINE` | `auto` | `compare` \| `postgres_only` \| `lidb_only` \| `sqlite_stub` |
| `POSTGRES_URL` | — | Postgres 15+ (`psycopg` for real bench) |
| `LIDB_ROOT` / `LIDB_EMBED` | — | **lidb** native embed |
| `BENCH_DB_REGISTRY_THRESHOLD` | `1.2` | PH-DB-5 pass: lidb P95 / postgres P95 ≤ threshold |

## CI behavior

| Job | `RUN_HARNESS` | Engines | Manifest `status` |
|-----|---------------|---------|-------------------|
| PR `ci.yml` | `0` | none | `stub` |
| Nightly (optional) | `1` | `postgres_only` or `compare` | `unknown` / `pass` / `fail` |

**Honesty:** `pass` only with measured lidb vs Postgres ratios on all three scenarios. SQLite stub → `unknown`. No fake green P95.

## CI ingest

1. `run-db-registry-bench.sh` → `write-tier-db-registry-manifest.py`
2. Artifact: `data/latest/tier-db-registry.json`
3. CSV: `benchmarks/tier_db_registry/results/latest.csv` when harness runs

## Plan linkage

| PH | Deliverable |
|----|-------------|
| **PH-DB-1** | `lidb` + `001_registry.sql` |
| **PH-DB-4** | lip registry API + schema |
| **PH-DB-5** | This tier — P95 parity evidence |

## Blockers

- **Postgres in CI:** not provisioned on default PR runners — use `postgres_only` / `compare` on nightly with service container or skip (`stub`).
- **Schema drift:** lip `registry-v1` vs lidb `001_registry` — workloads aligned; DDL differs (BIGSERIAL vs UUID).
- **PH-DB-5 exit:** requires green ratios on all scenarios; until then dashboard stays `unknown`/`fail`.
