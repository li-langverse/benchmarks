# Expand catalog from lic algo_registry + tier-2 harness gaps

## Summary

Syncs **124** new `catalog.toml` rows from `lic/benchmarks/competitive/algo_registry.json` (126 algorithms minus seven harness aliases) plus five missing `tier2_physics` harness dirs; regenerates `data/latest/summary.json` with **169** rows (one per catalog id, mostly `unknown` until measured).

## Agent continuation

1. **Read:** `scripts/catalog/sync-from-algo-registry.py`, `catalog.toml` algo_registry sync section, `docs/honesty/benchmark-dashboard.md`.
2. **Run:** `LIC_ROOT=../lic python3 scripts/catalog/sync-from-algo-registry.py --dry-run`; `python3 scripts/ingest/build_summary.py ../lic ../lis`; `cd dashboard-next && npm ci && npm run build`.
3. **Then:** Wire harness CSV for high-priority registry ids (matmul/simd already measured); merge `feat/sota-validity-os-reporting` if validity fields needed on drill-down; deploy via ingest/Pages workflow so live dashboard matches `summary.json`.
4. **Blocked on:** Per-algorithm lic harness + `latest.csv` rows — stubs intentionally `path = "unknown"` and `status = unknown`.

## Changed

| Area | Paths / evidence |
|------|------------------|
| Catalog sync | `scripts/catalog/sync-from-algo-registry.py` — family → pillar/tier; aliases for `matmul_*`, `simd_dot`, `md_lennard_jones`, etc. |
| Catalog | `catalog.toml` — **45 → 169** `[[benchmark]]` entries; tier-2 gaps: `three_body_pure`, `schrodinger_1d_barrier`, `ragdoll_chain`, `orbit_two_body`, `fdtd_waveguide_2d` with real paths |
| Ingest | `data/latest/summary.json` — **35 → 169** `rows` via `scripts/ingest/build_summary.py` (pending rows for `path=unknown`) |
| Dashboard | `dashboard-next/app/page.tsx` — `TIER_ORDER` includes tier **6** (registry OLTP) |

## Not changed

- `threshold_ratio_cpp` and compare-oracle policy (no threshold weakening).
- lic/lis harness execution or `latest.csv` schema.
- Vite `dashboard/` cutover (still `dashboard-next` static export path).
- SOTA/validity ingest fields (stack on `feat/sota-validity-os-reporting` when merging).

## Breaking

N/A — additive catalog/summary rows; search and matrix show more `unknown` benchmarks.

## Security

N/A — catalog metadata only; no trusted creep.

## Performance

N/A — no new measurements; dashboard perf claims stay `unknown` for new registry stubs until CSV ingest.

## Downstream

- **li-cursor-agents** `agent-briefing.py` will list more catalog ids after ingest on Pages.
- **lic** sim workbench `algo_registry.json` remains source of truth; re-run sync after registry bumps.
