# Release notes: 2026-05-25 — tier-db-token-efficiency

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** feat/tier-db-token-efficiency  
**PH / REQ:** PH-DB-2, PH-DB-5, WP-N4

---

## Summary

Adds **tier_db_token_efficiency** — reproducible 18-scenario corpus comparing SQL, liq, Prisma, Drizzle, Supabase JS, PostgREST, and GraphQL token counts with CI manifest ingest.

## Agent continuation

1. **Read:** `docs/ecosystem/tier-db-token-efficiency.md`, `benchmarks/tier_db_token_efficiency/scenarios.json`, `../lidb/docs/liq-token-efficiency-audit.md`
2. **Run:** `./scripts/run-db-token-efficiency-bench.sh` → `data/latest/tier-db-token-efficiency.json`
3. **Then:** Optional `catalog.toml` dashboard row; re-run after lidb liq grammar changes
4. **Blocked on:** none

## Changed

| Area | What | Evidence |
|------|------|----------|
| Tier suite | `benchmarks/tier_db_token_efficiency/` scenarios + `compute_tokens.py` | Manifest `encoder=tiktoken_cl100k_base`, n=18 |
| Scripts | `run-db-token-efficiency-bench.sh`, `write-tier-db-token-efficiency-manifest.py` | `./scripts/run-db-token-efficiency-bench.sh` exit 0 |
| Docs | `docs/ecosystem/tier-db-token-efficiency.md` | Master matrix + methodology |
| Ingest | `data/latest/tier-db-token-efficiency.json`, `schema/tier-db-token-efficiency-ingest.json` | `liq_vs_sql_delta_pct_total=-35.6` |

## Not changed

- `tier_db_registry` latency harness — **not** in this PR
- Dashboard `catalog.toml` row — follow-up
- `run-full-benchmark-suite.sh` wiring — optional later

## Breaking changes

None.

## Security

N/A — static string corpus; no live DB or credentials.

## Performance

N/A — token metric only; not latency. liq total **405** vs SQL **629** tokens (authoring surface).

## Downstream

| Repo | Action |
|------|--------|
| lidb | `docs/liq-token-efficiency-audit.md` (sibling PR) |
| roadmap | Appendix cross-link in `lidb-native-li-matrices.md` |

## CHANGELOG entry

- **tier_db_token_efficiency:** token audit tier, manifest, ecosystem doc — [2026-05-25-tier-db-token-efficiency.md](2026-05-25-tier-db-token-efficiency.md).
