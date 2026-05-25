# Dashboard diagram layout — Algorithm × Facet IA

## Summary

Documents compact portal IA (minimal mermaid subgraphs), Algorithm×Facet overview matrix, single-route five-facet bench detail, JSON field mapping, and facet-grid types stub for dashboard-next.

## Agent continuation

1. **Read:** `docs/dashboard/diagram-layout.md`, `docs/dashboard/design-system.md` (Diagram layout section), `dashboard-next/components/bench/algorithm-facet-grid.tsx`.
2. **Run:** `cd dashboard-next && npm run build` before implementing virtualized matrix.
3. **Next:** WP2 — `/matrix` facet columns + virtualized rows; reorder `/bench/[id]` panels to facet order; memory ingest when CSV exports RSS.
4. **Blocked:** Memory facet data until lic/lis export `peak_rss` (or equivalent) into ingest.

## Changed

| Path | What |
|------|------|
| `docs/dashboard/diagram-layout.md` | Portal IA + drill-down mermaid, matrix wireframe, JSON mapping, UX scale notes |
| `docs/dashboard/design-system.md` | Diagram layout section linking to diagram-layout.md |
| `dashboard-next/components/bench/algorithm-facet-grid.tsx` | `FacetId`, `FacetCell`, `facetCellsFromSummaryRow` types/helpers (no UI) |

## Not changed

- Ingest `build_summary.py`, live `summary.json` schema, Pages deploy workflow.
- Existing bench components behavior (`validity-panel`, `os-table`, etc.) — reorder only in follow-up.

## Breaking

N/A — documentation and types stub only.

## Security

N/A — no trust boundary changes.

## Performance

N/A — design doc; virtualization specified for 200+ rows in WP2.

## Downstream

None until matrix UI lands on `dashboard-next`.
