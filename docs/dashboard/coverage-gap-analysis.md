# Benchmark dashboard coverage gap analysis

**Date:** 2026-05-26 · **Branch:** `feat/benchmark-ship-integration` → `main` after PR #85  
**Live target:** https://li-langverse.github.io/benchmarks/  
**Regression gates:** [INVARIANTS.md](./INVARIANTS.md) · `scripts/check-dashboard-invariants.py`

## Current vs target

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Catalog rows | **170** | ≥126 registry + HTTP/DB + sizes | ✅ |
| `summary.json` rows | **169–170** | Match catalog | ✅ fixture ingest |
| Package `*_stub` rows | **0** | 0 | ✅ removed |
| Rows with `problem_size` / `size_label` | **31+** harness + **140** pending labels | All tier1 + HTTP measured | Partial |
| Size variant rows (`base_id`) | **2** (`matmul_*_N1024`) | Multi-size sweeps per family | Started |
| Facet matrix `/matrix` | Implemented | 5 facet columns + size filter | ✅ |
| `path=unknown` | ~109 | OK until harness wired | Documented |

## Package rows (real ids, not package stubs)

| Package | Rows | Example ids |
|---------|------|-------------|
| lic | 139+ | `matmul_naive`, `md_lennard_jones`, `num_cg`, … |
| lis | 8 | `static_small` (payload_1k), `proxy_loopback`, … |
| lidb | 10 | `registry_publish`, tier_db scenarios |
| lig | 7 | `viz_colormap`, `viz_marching_cubes`, … |
| li-math | 3 | `ml_mlp_forward`, `ml_conv2d_forward`, … |
| lip / lit | 1 each | `lip_smoke`, `lit_smoke` (CI harness paths) |

## Missing sizes (next ingest)

- tier1: only 5 harness dirs today — enrich reads `params.toml` (N=256, 512, …).
- tier2 physics: need grid/cell count in harness metadata → `problem_size=tier2_*`.
- HTTP: payload labels on `static_small` / `static_large` done; wrk concurrency variants TBD.

## CI enforcement (2026-05-26)

| Check | Script | Threshold |
|-------|--------|-------------|
| Summary/catalog parity | `check-dashboard-invariants.py` | rows ≥ 150, ids 1:1 |
| No package stubs | same | ban `*_stub`, `lig_viewport_stub` |
| Static routes | `check-dashboard-static-routes.sh` | index + matrix + ≥145 bench pages |

## Agent continuation

1. Read [ARCHITECTURE.md](./ARCHITECTURE.md), [INVARIANTS.md](./INVARIANTS.md), [SHIP-STATUS.md](./SHIP-STATUS.md).
2. Run `python3 scripts/check-dashboard-invariants.py` after catalog edits; `build_summary_fixture.py` to refresh `summary.json`.
3. Verify live `/matrix` row count ≥169 and Size column after Pages deploy from `main`.
4. **Blocked:** ~109 `path=unknown` until **lic** harness + CSV; memory facet ratios until RSS ingest.
