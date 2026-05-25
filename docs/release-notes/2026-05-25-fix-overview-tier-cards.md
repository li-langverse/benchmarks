# Release notes: 2026-05-25 — fix-overview-tier-cards

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** feat/fix-overview-tier-cards  
**PH / REQ:** PH-5b  
**Author:** agent

---

## Summary (one sentence)

Overview tier and pillar cards count measured green/yellow/red from `summary.rows` and label unmeasured rows **pending**, fixing the “0 ok, only ?” strip when ingest `tier_counts.unknown` held placeholders.

## Agent continuation (required)

1. Read: `docs/dashboard/fix-unknowns-and-overview-plan.md`
2. Run: `cd dashboard-next && npm run test:overview && npm run build`
3. Then: merge when CI green; redeploy Pages
4. Blocked on: tier5 Li RPS in **lis** (not this PR)

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| `dashboard-next/lib/overview.ts` | `splitTierCounts`, `countPillarOverview` | `npm run test:overview` |
| `dashboard-next/lib/coverage.ts` | `hasWallClock`, fixed `rowCoverageKind` | test script |
| `dashboard-next/app/page.tsx` | Measured / Pending tier sections | Manual `/` |
| `docs/dashboard/fix-unknowns-and-overview-plan.md` | Wave plan | — |

## Not changed

- `scripts/ingest/build_summary.py` — **not** this PR
- `data/latest/summary.json` regeneration — **not** this PR

## Breaking / Security / Performance

N/A — display-only.

## Downstream

Rebuild benchmarks Pages after merge.
