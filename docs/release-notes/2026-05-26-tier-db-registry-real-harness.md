# tier_db_registry — real lidb vs Postgres harness (WP-C / PH-DB-5 prep)

## Summary

Replaces stub-only path with `registry_oltp.py`: lidb_embed timings vs Postgres 15+ on `registry-v1.sql`, honest manifest (`stub` / `unknown` / `pass` / `fail`), CI unchanged (validate + stub).

## Run locally

```bash
cd benchmarks
# CI path (no engines)
./scripts/run-db-registry-bench.sh

# Real compare (needs cmake lidb + Postgres 15+)
export LIDB_ROOT=../lidb
export POSTGRES_URL='postgresql://user:pass@localhost:5432/bench'
pip install -r benchmarks/tier_db_registry/harness/requirements-registry.txt
BENCH_DB_REGISTRY_RUN_HARNESS=1 BENCH_DB_REGISTRY_PROFILE=nightly \
  BENCH_DB_REGISTRY_ENGINE=compare ./scripts/run-db-registry-bench.sh
```

Postgres-only oracle (lidb ratio pending):

```bash
BENCH_DB_REGISTRY_RUN_HARNESS=1 BENCH_DB_REGISTRY_ENGINE=postgres_only \
  POSTGRES_URL=... ./scripts/run-db-registry-bench.sh
```

## PH-DB-5 gate

Exit when all three scenarios have `ratio_vs_postgres` ≤ `BENCH_DB_REGISTRY_THRESHOLD` (default **1.2**) and manifest `status: pass`. Until then dashboard stays **unknown** / **fail** — never fake green.

## Checklist

- [x] `./scripts/run-db-registry-bench.sh` — CI stub
- [x] `python3 -m unittest tests.test_tier_db_registry`
- [ ] Nightly: compare with lidb + Postgres (org runners)
