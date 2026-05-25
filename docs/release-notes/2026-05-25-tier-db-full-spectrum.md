# Release notes: 2026-05-25 — tier-db-full-spectrum

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** branch `feat/tier-db-full-spectrum`  
**PH / REQ:** WP-N4  
**Author:** agent

---

## Summary (one sentence)

Adds five **lidb** full-spectrum audit benchmark tiers (security, memory, parallel, audit, realtime) as runnable stubs that exit 0 and write CI ingest JSON under `data/latest/`.

## Agent continuation (required)

1. Read: `docs/ecosystem/tier-db-security.md` … `tier-db-realtime.md`; `benchmarks/tier_db_*/README.md`.
2. Run: `./scripts/run-db-full-spectrum-bench.sh` — expect five new `data/latest/tier-db-*.json` with `"status": "stub"`.
3. Then: implement harnesses in **lidb**; set `BENCH_DB_*_RUN_HARNESS=1`; emit `benchmarks/tier_db_*/results/latest.csv`; merge into `summary.json` when stable.
4. Blocked on: **lidb** audit probe + WS harness (PH-DB-SEC/MEM/PAR/AUD/RT) — **none** for catalog/CI stub merge.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Tiers | Five suites under `benchmarks/tier_db_{security,memory,parallel,audit,realtime}/` | `suite.toml`, scenarios, stub schema SQL |
| Run | `scripts/run-db-{security,memory,parallel,audit,realtime}-bench.sh`, `run-db-full-spectrum-bench.sh` | exit 0 locally |
| Ingest | Manifest writers + `schema/tier-db-*-ingest.json` | `data/latest/tier-db-*.json` |
| Catalog | 9 new `[[benchmark]]` rows (tier 6) | `catalog.toml` |
| CI | GHA step runs full-spectrum + asserts manifests | `.github/workflows/ci.yml` |
| Docs | `docs/ecosystem/tier-db-*.md`, README table | — |

## Not changed (scope fence)

- **lidb** / **lis** harness implementation — stubs only
- `tier_db_registry`, graph/vector/GPU tiers — unchanged
- Dashboard merge of stub manifests into `summary.json` — still `merge_into_summary: false`
- Nightly Postgres/lidb timing — optional until harness lands

## Breaking changes

None.

## Security

N/A for stub manifests. Tier `tier_db_security` documents injection/RLS probes; no exploit execution in CI until harness exists.

## Performance

N/A — no measured rows; honesty `status: stub`.

## Downstream

| Repo | Action |
|------|--------|
| lidb | Add audit harnesses; wire `BENCH_DB_*_RUN_HARNESS=1` |
| benchmarks | N/A until CSV ingest |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Added
- **WP-N4 lidb full-spectrum audit tiers:** security, memory, parallel, audit, realtime stubs + CI manifests.
```
