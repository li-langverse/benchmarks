# Wire tier_db_memory / tier_db_parallel lidb harness runners

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** feat/bench-memory-parallel-wire  
**PH / REQ:** WP-N4, PH-DB-MEM, PH-DB-PAR  
**Author:** agent

---

## Summary (one sentence)

`run-db-memory-bench.sh` and `run-db-parallel-bench.sh` now delegate to **lidb** `memory_footprint.sh` / `parallel_load.sh` when `BENCH_DB_*_RUN_HARNESS=1`, with benchmarks-local fallbacks that still exit 0.

## Agent continuation (required)

1. Read: `docs/ecosystem/tier-db-memory.md`, `tier-db-parallel.md`, `lidb/README.md` harness table.
2. Run: `chmod +x scripts/run-db-*-bench.sh scripts/lidb-bench-stub/*.sh && ./scripts/run-db-memory-bench.sh && BENCH_DB_MEMORY_RUN_HARNESS=1 LIDB_ROOT=/nonexistent ./scripts/run-db-memory-bench.sh` (expect stub manifest).
3. Then: With sibling **lidb** built (`cmake` target `lidb_embed`), run `BENCH_DB_MEMORY_RUN_HARNESS=1` and confirm `data/latest/tier-db-memory.json` has `status: pass` and measured `rss_mb` rows.
4. Blocked on: Postgres compare oracle for nightly ratio rows — **not** in this PR.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Runners | Harness dispatch + `BENCH_HARNESS_JSON` → `data/latest/tier-db-*.json` | `scripts/run-db-memory-bench.sh`, `scripts/run-db-parallel-bench.sh` |
| Fallback | `scripts/lidb-bench-stub/{memory_footprint,parallel_load}.sh` | Exit 0 + stub manifest when lidb scripts absent |
| Docs | Tier tables + env vars | `docs/ecosystem/tier-db-memory.md`, `tier-db-parallel.md` |

## Not changed (scope fence)

- **lidb** harness implementation (`scripts/bench/*.sh` bodies) — lives in **lidb** repo.
- **tier_db_security** / audit / realtime runners — still stub-only on `RUN_HARNESS=1` except security partial wire.
- CI GHA — still runs default stub mode (`BENCH_DB_*_RUN_HARNESS` unset).

## Breaking changes

None.

## Security

N/A — benchmark orchestration only; no new probes.

## Performance

N/A for CI stub path. Local harness: `BENCH_DB_MEMORY_RUN_HARNESS=1` builds `lidb_embed` and samples RSS (Darwin `time -l` or Linux `time -v`).

## Downstream

| Repo | Action |
|------|--------|
| lidb | Ensure `scripts/bench/memory_footprint.sh` and `parallel_load.sh` on default branch for measured runs |
| benchmarks dashboard | Ingest `data/latest/tier-db-memory.json` / `tier-db-parallel.json` when manifests refreshed |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Added
- **tier_db_memory / tier_db_parallel harness wire:** lidb `memory_footprint.sh` / `parallel_load.sh` when `BENCH_DB_*_RUN_HARNESS=1` (WP-N4).
```
