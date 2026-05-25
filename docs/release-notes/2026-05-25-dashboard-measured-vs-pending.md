# Release notes: 2026-05-25 — dashboard-measured-vs-pending

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** feat/dashboard-measured-vs-pending  
**PH / REQ:** PH-5b (benchmark catalog honesty)  
**Author:** agent

---

## Summary (one sentence)

Dashboard-next splits tier overview counts into measured perf vs catalog-pending placeholders and links coverage-gap docs so 169 unknown rows are not read as “no benchmarks.”

## Agent continuation (required)

1. Read: `dashboard-next/lib/coverage.ts`, `docs/dashboard/coverage-gap-analysis.md`
2. Run: `cd dashboard-next && npm run build`
3. Then: Merge after green CI; coordinate ingest PR if it adds `pending` on `summary.json` rows (optional field already typed)
4. Blocked on: ~109 harness paths in **lic** for wall-clock CSV — not this PR

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| `dashboard-next/lib/coverage.ts` | Client-side `isCatalogPending`, `splitTierCounts`, `coverageHonesty` (no ingest schema change) | `npm run build` — 202 static routes |
| `dashboard-next/app/page.tsx` | Coverage honesty banner; tier cards show Measured vs Catalog pending | Manual `/` |
| `dashboard-next/app/matrix/page.tsx` | Matrix honesty + validity column via `summaryById` | Manual `/matrix/` |
| `dashboard-next/components/coverage-status-badge.tsx` | Distinct pending / validity-fail / validity-unknown badges | Matrix + search table |
| `dashboard-next/components/bench/algorithm-facet-grid.tsx` | Facet tones `pending` / `validity_fail` | Types for WP2 matrix |
| `dashboard-next/lib/summary.ts` | Optional `SummaryRow.pending` for forward-compatible ingest | Typecheck green |

## Not changed (scope fence)

- `scripts/ingest/build_summary.py` tier_counts aggregation — **not** in this PR (ingest fix PR can add row-level `pending` without conflict)
- `data/latest/summary.json` committed fixture — **not** regenerated in this PR
- Harness wiring in **lic** / CSV production — **not** in this PR

## Breaking changes

None — additive optional `pending` on `SummaryRow`; UI derives pending from existing row fields when absent.

## Security

N/A — read-only dashboard classification.

## Performance

N/A — static export build only; no bench thresholds changed.

## Downstream

| Repo | Action |
|------|--------|
| benchmarks Pages deploy | Rebuild `dashboard-next` after merge to refresh GitHub Pages |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Fixed
- **Dashboard measured vs pending:** tier strip splits wall-clock counts from catalog placeholders; coverage honesty banner links [coverage-gap-analysis.md](docs/dashboard/coverage-gap-analysis.md) — [2026-05-25-dashboard-measured-vs-pending.md](docs/release-notes/2026-05-25-dashboard-measured-vs-pending.md).
```
