# tier_db_registry — registry OLTP benchmarks

Compare **lidb** (`lidb_embed` + `001_registry.sql`) against **PostgreSQL 15+** (`registry-v1.sql`) on package-registry hot paths.

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
| `nightly` | on (reduced iters when profile=ci inside harness) | Scheduled / manual |

## Schema

| File | Engine |
|------|--------|
| [`schema/registry-v1.sql`](schema/registry-v1.sql) | Postgres 15+ oracle (canonical for ratio) |
| `lidb/migrations/001_registry.sql` | lidb_embed migrate (UUID schema; workload-equivalent paths) |
| [`schema/registry-sqlite-v1.sql`](schema/registry-sqlite-v1.sql) | CI plumbing stub only |

## Run

```bash
cd benchmarks

# CI (default): validate layout + stub manifest — no engines
./scripts/run-db-registry-bench.sh

# SQLite stub plumbing (status unknown — not PH-DB-5 evidence)
BENCH_DB_REGISTRY_RUN_HARNESS=1 BENCH_DB_REGISTRY_ALLOW_SQLITE_STUB=1 \
  BENCH_DB_REGISTRY_ENGINE=sqlite_stub ./scripts/run-db-registry-bench.sh

# lidb timings only (no Postgres yet)
export LIDB_ROOT=../lidb
BENCH_DB_REGISTRY_RUN_HARNESS=1 BENCH_DB_REGISTRY_ENGINE=lidb_only ./scripts/run-db-registry-bench.sh

# Real PH-DB-5 compare (lidb P95 / Postgres P95 ≤ threshold)
pip install -r benchmarks/tier_db_registry/harness/requirements-registry.txt
export POSTGRES_URL='postgresql://localhost/registry_bench'
export LIDB_ROOT=../lidb
BENCH_DB_REGISTRY_RUN_HARNESS=1 BENCH_DB_REGISTRY_PROFILE=nightly \
  BENCH_DB_REGISTRY_ENGINE=compare ./scripts/run-db-registry-bench.sh

cat data/latest/tier-db-registry.json
```

From **lidb** repo (builds embed, delegates to benchmarks harness):

```bash
cd lidb
export BENCHMARKS_ROOT=../benchmarks
export POSTGRES_URL=...   # optional for compare
bash scripts/bench/registry_oltp.sh
```

| Path | Role |
|------|------|
| `harness/registry_oltp.py` | Real lidb + Postgres / postgres_only / lidb_only |
| `harness/registry_oltp_stub.py` | Validate + SQLite stub (`--run-timing`) |
| `harness/requirements-registry.txt` | Optional `psycopg` for Postgres oracle |
| `fixtures/seed.toml` | Reproducible publisher/package seed |
| `results/latest.csv` | Emitted when harness timing runs |

### Env

| Variable | Default | Notes |
|----------|---------|-------|
| `BENCH_DB_REGISTRY_PROFILE` | `ci` | `nightly` for full measure_iters |
| `BENCH_DB_REGISTRY_RUN_HARNESS` | `0` | `1` to run timings |
| `BENCH_DB_REGISTRY_ENGINE` | `auto` | `compare`, `postgres_only`, `lidb_only`, `sqlite_stub` |
| `BENCH_DB_REGISTRY_THRESHOLD` | `1.2` | Max lidb/postgres P95 ratio for **pass** |
| `POSTGRES_URL` | — | Postgres 15+ (psycopg required for real bench) |
| `LIDB_ROOT` / `LIDB_EMBED` | auto `../lidb` | Native embed binary |
| `LIDB_DATA_DIR` | temp | Persistent lidb data dir (optional) |

## PH-DB-5 exit gate

Manifest `status: pass` only when **all three** scenarios have measured `ratio_vs_postgres` ≤ `BENCH_DB_REGISTRY_THRESHOLD`. Otherwise manifest is `unknown` (partial engines) or `fail` (over threshold) — never fake green.

## CI

| Workflow | Trigger | Harness | Manifest `status` |
|----------|---------|---------|-------------------|
| [`ci.yml`](../../.github/workflows/ci.yml) | PR / push `main` | validate-only stub | `stub` |
| [`tier-db-registry-nightly.yml`](../../.github/workflows/tier-db-registry-nightly.yml) | `workflow_dispatch` + weekly cron (Mon 06:00 UTC) | Postgres 16 service + `compare` | `pass` / `fail` / `unknown` |

**PR path:** unchanged — `./scripts/run-db-registry-bench.sh` with default env (no `POSTGRES_URL`, no lidb build).

**Nightly path (WP-K):** GHA job `registry-compare` provisions `postgres:16`, checks out sibling **lidb**, builds `lidb_embed`, sets:

```bash
POSTGRES_URL=postgresql://postgres:postgres@localhost:5432/registry_bench
BENCH_DB_REGISTRY_RUN_HARNESS=1
BENCH_DB_REGISTRY_PROFILE=nightly
BENCH_DB_REGISTRY_ENGINE=compare   # or postgres_only via workflow_dispatch input
```

Uploads artifact `tier-db-registry-nightly` (`tier-db-registry.json`, harness JSON, CSV). **Fail closed:** when `engine=compare`, job fails if Postgres is up but any scenario lacks numeric `ratio_vs_postgres` or engine P95 timings.

Manual dispatch accepts `engine=postgres_only` for oracle-only smoke (manifest stays `unknown` — honest, not green).

## CI ingest

Manifest: `data/latest/tier-db-registry.json` (schema: [`schema/tier-db-registry-ingest.json`](../../schema/tier-db-registry-ingest.json)).

See [tier-db-registry-benchmark.md](../../docs/ecosystem/tier-db-registry-benchmark.md) · [ph-db-ci-hosting-plan WP-K](https://github.com/li-langverse/lic/blob/cursor/ph-db-ci-hosting-plan/docs/superpowers/plans/ph-db-ci-hosting-plan.md).
