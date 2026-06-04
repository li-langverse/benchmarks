# Catalog path reconciliation — honest planned rows (PH-5b / REQ-BENCH-CATALOG-1)

> **Issue:** [benchmarks#179](https://github.com/li-langverse/benchmarks/issues/179)  
> **Related:** [#20](https://github.com/li-langverse/benchmarks/issues/20)–[#29](https://github.com/li-langverse/benchmarks/issues/29), [LIC_ROOT plan](./2026-05-18-lic-root-audit-layout.md), [tier-2 sync plan](./2026-05-18-tier2-catalog-lic-sync.md)  
> **Repo:** li-langverse/benchmarks + li-langverse/lic  
> **Vision:** **Provable** (honest catalog), **Fast** (measurement surface for PH-5b/PH-7e)  
> **Learned from:** [vision-and-roadmap.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md), [provability-gaps.md](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md), `plan-completion-audit.json` (2026-05-31: **0** actionable `catalog_gaps` with LIC_ROOT), [benchmark-dashboard honesty](../honesty/benchmark-dashboard.md)

## Goal

Maintain an **honest** `catalog.toml` index: when harness paths are missing under **lic**, rows must be explicitly `catalog_lifecycle = "planned"` (or corrected) so dashboard and audit do not overclaim coverage. The original 117-gap spike is **resolved** when `LIC_ROOT=../lic` is present; this plan covers ongoing policy and tier-2 stub reconciliation.

## Non-goals

- Copying `lic/benchmarks/harness` into **benchmarks** (ingest-only per AGENTS.md).
- Weakening benchmark thresholds to green incomplete kernels.
- Claiming **G-math** / **G-par** closure from catalog edits alone.
- Bulk-removing catalog rows without master-plan / PH-5b alignment.

## Dependencies

- **PH-5b** — harness ownership in **lic**; catalog is dashboard index only.
- **PH-7e** — tier-1 yellow/red rows need **lic** perf work, not catalog-only fixes.
- [PR #135](https://github.com/li-langverse/benchmarks/pull/135) — LIC_ROOT resolver (merged).
- **lic** stacked PRs for missing tier-2 physics dirs ([tier-2 sync plan](./2026-05-18-tier2-catalog-lic-sync.md)).
- Human: **`plan-approved`** before implementation PRs.

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | **Triage script** `scripts/catalog-gap-triage.py` — classify gaps: `fix_path`, `planned`, `lic_impl` | JSON in `data/latest/catalog-gap-triage.json` |
| B | **Planned-row policy** — all rows without lic path use `catalog_lifecycle=planned` + `ph_ids` | Audit `catalog_gaps_actionable` stays ≤20 |
| C | **Path fixes** — correct mis-mapped bio/drug/am rows where harness exists elsewhere | Scoped PR ≤30 rows |
| D | **lic** issues — one per missing tier-2 kernel cluster (CFD, MD, QM stubs) | Linked from catalog |
| E | **Audit split** — `plan-completion-audit.py` reports `actionable` vs `planned` gaps | Dashboard badge for planned rows |

## Current status (2026-06-04)

- `catalog-gap-triage.py` + `apply-catalog-honesty-ph5b.py` land honest `repo=benchmarks` mirrors and fix competitive vertical remaps ([#266](https://github.com/li-langverse/benchmarks/issues/266)).
- `plan-completion-audit.json`: **`catalog_gaps`: 0** with sibling `../lic` checkout and post-PH-5b catalog.
- Tier-1 posture: 0 red, 1 yellow (`matmul_blocked`), 3 near-threshold greens.
- Remaining debt: aspirational tier-2 catalog rows ahead of lic dev tree ([#19](https://github.com/li-langverse/benchmarks/issues/19)).

## Tests / benches

- `python3 scripts/plan-completion-audit.py` with `LIC_ROOT=../lic` — actionable gaps documented.
- `python3 scripts/check-dashboard-invariants.py` — row count stable.
- Ingest smoke: `./scripts/ingest/ingest-lic.sh` for fixed-path rows.

## Provability

- **G-math** — stays **Partial** until proofs + green tier-1 where claimed.
- **G-par** — unchanged; no perf claims from path mapping.

## Rollout

1. **benchmarks** draft PR: this plan (refresh of closed #183).
2. Scoped PR: triage script + planned-row schema (post **`plan-approved`**).
3. **lic** PR(s): missing harness directories (separate repo).
4. Close #179 when policy landed and actionable gaps ≤20 on CI with LIC_ROOT.

## Human-only

- Approve `catalog_lifecycle=planned` dashboard UX.
- Prioritize tier-2 physics clusters on **lic** `main` vs contributor branches.
