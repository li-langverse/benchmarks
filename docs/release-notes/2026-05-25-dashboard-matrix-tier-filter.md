# Dashboard matrix tier filter + mobile padding

## Summary

Overview tier-strip links to `/matrix/?tier=N` now filter the catalog table client-side; mobile header/main padding tightened on narrow viewports.

## Agent continuation

1. Read `dashboard-next/components/matrix-catalog-table.tsx` and `app/matrix/page.tsx`.
2. Run `cd dashboard-next && npm run build`; open `/benchmarks/matrix/?tier=2` on Pages after merge.
3. Next: merge `feat/sota-validity-os-reporting` for SOTA/validity columns on live ingest; refresh `benchmark-matrix.json` generated_at in ingest.
4. Blocked: none for this slice.

## Changed

- `dashboard-next/components/matrix-catalog-table.tsx` — new client table; `useSearchParams` tier filter.
- `dashboard-next/app/matrix/page.tsx` — Suspense wrapper for static export.
- `dashboard-next/app/globals.css` — `.matrix-filter-meta`; mobile `1rem` horizontal padding.

## Not changed

- `pages.yml` artifact copy list (unchanged).
- Ingest `build_summary.py` SOTA/validity fields (separate branch).
- Category bento chart tiles on overview (design-system future work).

## Breaking

N/A — dashboard-only UX fix.

## Security

N/A — no auth or trust boundary changes.

## Performance

N/A — client-side filter over prebuilt matrix rows (&lt;100 rows).

## Downstream

GitHub Pages redeploy on merge to `main` touching `dashboard-next/**`.
