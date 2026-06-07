# Tier-2 gaming-physics catalog sync with lic dev tree (PH-5b)

> **Superseded (2026-06-07):** Harness ownership moved to **benchmarks** per [ADR](../benchmarks-single-repo-layout.md). Active reconcile plan: [2026-06-07-tier2-gaming-physics-catalog-reconcile.md](./2026-06-07-tier2-gaming-physics-catalog-reconcile.md).

> **Issue:** [benchmarks#19](https://github.com/li-langverse/benchmarks/issues/19)  
> **Related:** [lic#24](https://github.com/li-langverse/lic/issues/24) (`tier0_stability` path)  
> **Repo:** li-langverse/benchmarks + li-langverse/lic  
> **Vision:** **Provable** (honest catalog), **Fast** (tier-2 physics proof surface)  
> **Learned from:** [li-language PR #6](https://github.com/li-langverse/li-language/pull/6) (tier-2 suite intent), [master plan phase-07](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-phase-07-native-hpc.md), `catalog.toml`, local `LIC_ROOT` path audit (2026-05-18)

## Goal

Reconcile **benchmarks** `catalog.toml` tier-2 rows with directories that exist on **lic** `main` (or feature branch), so plan-completion-audit and ingest do not report false gaps for gaming-physics kernels that are catalog-only.

## Current drift (2026-05-18, `LIC_ROOT=../li`)

**Missing under lic tree** (catalog ahead of harness):

- `advection_diffusion_2d`, `wave_equation_2d`, `sph_dam_break_2d`, `euler_fluid_2d`, `combustion_passive`, `wind_field_bc`, `rigid_body_stack`, `cloth_swing`
- `tier0_stability` → `benchmarks/tier0_correctness` (tier 0)

**Present** on `../li`: core tier-2 set (`nbody_gravity`, `double_pendulum`, `md_lennard_jones`, …).

## Non-goals

- Implementing physics solvers only in **benchmarks** (kernels live in **lic**).
- Dropping `threshold_ratio_cpp` to green incomplete kernels.
- Merging **li-language** fork PRs without **lic** org review.

## Dependencies

- **PH-5b** — physics tier-2 harness ownership.
- **lic** feature branch or stacked PRs for missing 8 kernels (may align with cap-jmk-real/li-language work — track in **lic**, not benchmarks-only).

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | Inventory: catalog id → path exists on `lic` main | Markdown table in plan or lic issue |
| B | **Policy:** catalog rows require `path` on **lic** `main` before merge OR `status = "planned"` field in catalog.toml | No silent missing dirs |
| C | **lic** PR(s): land 8 tier-2 dirs + `tier0_correctness` OR remove/defer catalog rows | `plan-completion-audit` catalog_gaps = 0 for those ids |
| D | **benchmarks** PR: catalog.toml sync (drop, defer, or point to shipped paths) | Ingest smoke green |
| E | Close **lic#24** when tier0 harness path resolved | Single owner: lic |

## Tests / benches

- `python3 scripts/plan-completion-audit.py` — zero missing-path rows for `repo = "lic"`.
- `LIC_ROOT=… ./scripts/ingest/ingest-lic.sh` — tier-2 ids produce CSV or explicit skip reason.
- **li-tests** / `bench.py --tier 2` on **lic** after harness lands.

## Provability

- **G-math** / physics modules — remain **Partial** until proofs exist; catalog sync is measurement honesty only.

## Rollout

1. **benchmarks** draft PR: this plan + optional `catalog.toml` `status` schema (after `plan-approved`).
2. **lic** implementation PR(s) for missing harness dirs (separate repo).
3. Remove `master-plan-gap` when audit clean.

## Human-only

- Decide whether gaming-physics expansion lands on **lic** `main` or stays on contributor fork until org CI green.
