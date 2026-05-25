# tier_db_registry benchmark skeleton (PH-DB-5 prep)

## Agent continuation

1. **Read:** `benchmarks/tier_db_registry/README.md`, `docs/ecosystem/tier-db-registry-benchmark.md`, `schema/tier-db-registry-ingest.json`.
2. **Run:** `./scripts/run-db-registry-bench.sh` — expect stub manifest at `data/latest/tier-db-registry.json`.
3. **Then:** When **lidb** + **lis** registry-min land, implement harness → `results/latest.csv` → wire ingest into `build_summary.py` (`category = database`, oracle `postgres`).

## Summary

Adds **tier_db_registry** skeleton: OLTP scenarios (publish, read-by-name, read-latest), shared `registry-v1.sql`, catalog rows (tier 6), CI manifest JSON, and `run-db-registry-bench.sh` stub. P95 vs Postgres 15+ documented; nightly timing optional.

## Changed

| Area | Path |
|------|------|
| Tier config | `benchmarks/tier_db_registry/` |
| Run stub | `scripts/run-db-registry-bench.sh` |
| Manifest writer | `scripts/ingest/write-tier-db-registry-manifest.py` |
| Ingest schema | `schema/tier-db-registry-ingest.json` |
| CI artifact | `data/latest/tier-db-registry.json` |
| Catalog | `catalog.toml` (3 rows) |
| Docs | `docs/ecosystem/tier-db-registry-benchmark.md` |

## Not changed

- `build_summary.py` merge (manifest-only until CSV producer exists).
- `run-full-benchmark-suite.sh` (explicit follow-up).

## Test plan

- [ ] `./scripts/run-db-registry-bench.sh` exits 0 and refreshes manifest.
- [ ] `catalog.toml` parses; three `registry_*` ids present.
- [ ] Benchmarks CI green (no harness dependency).
