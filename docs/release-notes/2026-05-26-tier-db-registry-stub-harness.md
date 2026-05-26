# tier_db_registry — runnable local stub harness

## Summary

Adds SQLite validation/timing stub, `fixtures/seed.toml`, `registry_oltp_stub.py`, and `lidb-bench-stub/registry_oltp.sh`. CI default path validates tier layout without lidb/Postgres; `BENCH_DB_REGISTRY_RUN_HARNESS=1` exercises harness plumbing only.

## Test plan

- [x] `./scripts/run-db-registry-bench.sh` — validate + stub manifest
- [x] `python3 -m unittest tests.test_tier_db_registry`
- [x] `BENCH_DB_REGISTRY_RUN_HARNESS=1` — SQLite CSV + manifest `status: unknown`

## Still blocked

- Real **lidb** vs **Postgres 15+** P95 parity (`PH-DB-5` gate)
- `build_summary.py` merge until lidb/postgres CSV rows exist
