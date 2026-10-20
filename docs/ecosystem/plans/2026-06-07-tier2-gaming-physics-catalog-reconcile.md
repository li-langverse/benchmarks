# Tier-2 gaming-physics catalog reconcile — benchmarks repo ownership (PH-5b)

> **Issue:** [benchmarks#19](https://github.com/li-langverse/benchmarks/issues/19)  
> **Related:** [benchmarks#266](https://github.com/li-langverse/benchmarks/issues/266) (catalog path honesty), [benchmarks#15](https://github.com/li-langverse/benchmarks/issues/15) (tier-2 suite, merged), [ADR benchmarks-single-repo-layout](../benchmarks-single-repo-layout.md)  
> **Repo:** li-langverse/benchmarks (catalog + workloads); li-langverse/lic (toolchain only)  
> **Vision:** **Provable** (honest catalog), **Fast** (tier-2 gaming/fluids measurement surface)  
> **Learned from:** [vision-and-roadmap.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md), [benchmarks-single-repo-layout ADR](../benchmarks-single-repo-layout.md), [2026-05-18 tier-2 sync plan](./2026-05-18-tier2-catalog-lic-sync.md) (superseded scope), `plan-completion-audit.py` with `LIC_ROOT=../lic` (2026-06-07)

## Goal

Close the **false catalog_gaps** for five tier-2 gaming/fluids benchmarks (`euler_fluid_2d`, `combustion_passive`, `wind_field_bc`, `rigid_body_stack`, `cloth_swing`) without re-landing harness trees under **lic**. Workloads already exist under `benchmarks/workloads/tier2_physics/`; audit failures are caused by stale `repo = "lic"` on paths that resolve in the **benchmarks** checkout per the 2026-05-30 ADR.

## Decision (issue #19 options)

| Option | Verdict |
|--------|---------|
| 1. Land harness dirs in **lic** `dev` first | **Reject** — contradicts ADR; duplicates workloads already in **benchmarks** |
| 2. Hold catalog rows / `catalog_lifecycle = planned` | **Defer** — workloads exist and some rows are measured; honesty fix is `repo` field, not planned stub |
| 3. Split: catalog points at repo that owns the path | **Accept** — set `repo = "benchmarks"` for the five ids |

## Non-goals

- Copying `benchmarks/workloads/` back into `lic/benchmarks/tier2_physics/`.
- Weakening `threshold_ratio_cpp` to green incomplete Li builds.
- Bulk `catalog_lifecycle = planned` for rows with on-disk workloads and ingest history.
- Implementing physics kernels in this planning PR (separate **lic** perf issues if Li compile fails).

## Dependencies

- **PH-5b** — tier-2 physics harness + catalog honesty.
- **REQ-BENCH-CATALOG-1** — catalog `repo`/`path` must match checkout root ([#266](https://github.com/li-langverse/benchmarks/issues/266)).
- [ADR: benchmarks-single-repo-layout](../benchmarks-single-repo-layout.md) — workloads canonical in **benchmarks**.
- Human: **`plan-approved`** before `catalog.toml` implementation PR merges.

## Current drift (2026-06-07)

| Catalog `id` | `repo` (stale) | `path` | On **benchmarks** `main` | On **lic** `dev` |
|---|---|---|---|---|
| `euler_fluid_2d` | `lic` | `benchmarks/workloads/tier2_physics/euler_fluid_2d` | **present** | missing (expected) |
| `combustion_passive` | `lic` | `benchmarks/workloads/tier2_physics/combustion_passive` | **present** | missing |
| `wind_field_bc` | `lic` | `benchmarks/workloads/tier2_physics/wind_field_bc` | **present** | missing |
| `rigid_body_stack` | `lic` | `benchmarks/workloads/tier2_physics/rigid_body_stack` | **present** | missing |
| `cloth_swing` | `lic` | `benchmarks/workloads/tier2_physics/cloth_swing` | **present** | missing |

`plan-completion-audit.py` reports these as `catalog_gaps` because it resolves `repo = "lic"` against `LIC_ROOT`, not the benchmarks tree where paths actually live.

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | **Plan** (this doc) + issue comment on [#19](https://github.com/li-langverse/benchmarks/issues/19) | Maintainer adds `plan-approved` |
| B | **catalog.toml** PR: `repo = "benchmarks"` for the five ids; keep `path` unchanged | Audit: 0 gaps for these ids with `LIC_ROOT=../lic` |
| C | **Ingest smoke**: `./scripts/ingest/ingest-lic.sh` + `check-dashboard-invariants.py` | Row count stable; no new `unknown` for fixed ids |
| D | **Reconcile #266**: fold five-id fix into broader catalog honesty PR or land first as scoped slice | [#266](https://github.com/li-langverse/benchmarks/issues/266) actionable gap count drops |
| E | **Close #19** when B–C green; remove `master-plan-gap` | Linked PR merged |

## Tests / benches

- `LIC_ROOT=../lic python3 scripts/plan-completion-audit.py` — five ids absent from `catalog_gaps`.
- `python3 scripts/check-dashboard-invariants.py` — catalog row count unchanged.
- `./scripts/run-bench.sh --tier 2` (subset: five ids) — document Li build failures separately; catalog honesty does not require green perf.
- **li-tests** — unchanged; tier-0 correctness tracked in [#17](https://github.com/li-langverse/benchmarks/issues/17).

## Provability

- **G-math** — remains **Partial**; catalog reconcile is measurement honesty only.
- **G-par** — unchanged; no perf claims from `repo` field correction.
- Do not mark proof **Done** from dashboard greens alone ([engineering-standards](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md)).

## Rollout

1. Merge this plan PR (draft until `plan-approved`).
2. Implementation PR: `catalog.toml` `repo` field for five ids (≤10-line diff).
3. Regenerate `data/latest/plan-completion-audit.json` in CI or ingest follow-up.
4. Close **#19**; keep **#266** open for remaining `repo`/`path` debt (~140 rows).

## Human-only

- Approve **`plan-approved`** on [#19](https://github.com/li-langverse/benchmarks/issues/19).
- Decide whether five-id fix lands before or inside [#266](https://github.com/li-langverse/benchmarks/issues/266) mega-PR.
- Prioritize **lic** Li compile fixes for benches that fail `run-bench.sh` (separate from catalog gap).

## north_star_fit

**Domain:** HPC / gaming physics tier-2 benchmarks · **PH-5b** · proof → easy → fast (honest catalog before perf claims).
