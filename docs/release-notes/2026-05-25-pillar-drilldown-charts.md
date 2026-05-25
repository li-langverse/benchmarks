# Release notes: 2026-05-25 — Pillar and drilldown charts

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** `feat/pillar-drilldown-charts` (builds on `feat/sota-relative-charts` / cdc0d58)  
**PH / REQ:** PH-DB-5, benchmark dashboard honesty  
**Author:** agent

---

## Summary (one sentence)

Adds **visible SOTA-relative bar charts** on `/pillar/[id]` (aggregate top/bottom benches) and completes **five-facet bench drill-down** on `/bench/[id]` with shared chart components, facet matrix snippet, and memory/security panels.

## Agent continuation (required)

1. **Read:** `docs/dashboard/diagram-layout.md`, `dashboard-next/components/charts/relative-bar-list.tsx`, `dashboard-next/components/bench/bench-facet-composition.tsx`, `dashboard-next/lib/pillar-charts.ts`
2. **Run:** `cd dashboard-next && npm run build`; `python3 scripts/check-dashboard-invariants.py`
3. **Next:** WP2 virtualized facet matrix on `/matrix`; history sparklines in matrix perf column
4. **Blocked:** Human merge (PR-only); do not weaken `check-dashboard-invariants.py`

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Shared charts | `RelativeBarList`, `BenchmarkRelativeBars` | `dashboard-next/components/charts/` |
| Pillar page | `PillarSummaryStrip` + top-12 / bottom-6 `ratio_vs_sota` bars + table | `app/pillar/[id]/page.tsx` |
| Bench drill-down | `BenchFacetComposition`: facet rail ①–⑤, `PerfRelativeBars`, `FacetMatrixSnippet` | `app/bench/[id]/page.tsx` |
| Helpers | `lib/pillar-charts.ts` | Pillar aggregate chart data |
| Scripts | `scripts/patch-dashboard-pages.py` | Page wiring helper |

## Not changed (scope fence)

- **Ingest** `build_summary.py` / `data/latest/summary.json` — unchanged on this PR (uses cdc0d58 data)
- **Legacy Vite** `dashboard/` — unchanged
- **Matrix virtualization** — still WP2 stub
- **li-cursor-agents** supervisor UI — separate repo

## Breaking changes

None.

## Security

N/A — static dashboard UI only.

## Performance

N/A — static export; pillar page renders ≤18 bar rows from prebuilt JSON.

## Downstream

| Repo | Action |
|------|--------|
| Pages deploy | Re-run `dashboard-next` build on merge |
| Agents | Pillar URLs now show charts — cite `ratio_vs_sota` |

## CHANGELOG entry (paste into Unreleased)

- **Dashboard pillar/drilldown charts:** Aggregate SOTA-relative bars on `/pillar/[id]`; five-facet composition on `/bench/[id]` — [2026-05-25-pillar-drilldown-charts.md](docs/release-notes/2026-05-25-pillar-drilldown-charts.md).
