# Benchmark dashboard ship integration

## Summary

Consolidates dashboard ship PRs (#79–#82), expands catalog to **169** algo_registry rows with **problem_size** / **size_label**, implements Algorithm×Facet matrix + five-panel bench drill-down, and pins lic CI until `resource_options_invalid` lands on lic main.

## Agent continuation

1. **Read:** `docs/dashboard/coverage-gap-analysis.md`, `docs/dashboard/diagram-layout.md`, integration PR checklist.
2. **Run:** `cd dashboard-next && npm run build`; on PR CI confirm `ingest-smoke` + `dashboard-build` green.
3. **Next:** Human merge `feat/benchmark-ship-integration`; after Pages deploy verify live row count ≥169 and Size column on `/matrix`.
4. **Blocked:** 109 catalog rows still `path=unknown` until lic harness + CSV; memory facet ratios until RSS ingest.

## Changed

| Area | Paths / evidence |
|------|------------------|
| Integration branch | `feat/benchmark-ship-integration` — merges #79 board, #80 tier filter, #81 SOTA/validity/OS, #82 diagram IA, expand-catalog |
| Catalog | `catalog.toml` — 169 rows; removed `lig_viewport_stub`, `li_math_gemm_stub`; `lig` 7× `viz_*`, `li-math` 3× `ml_*` |
| Problem sizes | `scripts/catalog/enrich-catalog-metadata.py`; tier1 `params.toml`; HTTP `size_label` on lis scenarios |
| Ingest | `scripts/ingest/build_summary_fixture.py` uses root `catalog.toml` → `data/latest/summary.json` (169 rows, 140 with size labels) |
| Dashboard | `dashboard-next/components/bench/algorithm-facet-grid.tsx`, `app/matrix/page.tsx`, `app/bench/[id]/page.tsx` facet panels |
| Gap analysis | `docs/dashboard/coverage-gap-analysis.md` |
| CI | `.github/workflows/ci.yml` — lic `ref: c0977131` |

## Not changed

- lic/lis live CSV refresh on every PR (fixture ingest for dashboard artifact).
- Closing superseded PRs #79–#82 individually (integration supersedes; close with pointer after merge).
- Demo video PR #78 (docs-only; merge separately).

## Breaking

N/A — dashboard additive.

## Security

N/A — honesty UI only; no trusted creep.

## Performance

N/A — static export; facet matrix uses client windowing above 80 rows (no new bench runs).

## Downstream

Pages workflow copies `data/latest/*.json` to `out/latest/` on deploy from `main`.
