# Tier-2 gaming-physics catalog sync with lic dev tree (PH-5b)

> **Issue:** [benchmarks#19](https://github.com/li-langverse/benchmarks/issues/19)  
> **Related:** [lic#24](https://github.com/li-langverse/lic/issues/24) (`tier0_stability` path)  
> **Repo:** li-langverse/benchmarks + li-langverse/lic  
> **Vision:** **Provable** (honest catalog), **Fast** (tier-2 physics proof surface)  
> **Learned from:** [li-language PR #6](https://github.com/li-langverse/li-language/pull/6) (tier-2 suite intent), [master plan phase-07](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-phase-07-native-hpc.md), `catalog.toml`, local `LIC_ROOT` path audit (2026-05-18)

## Goal

Reconcile **benchmarks** `catalog.toml` tier-2 rows with directories that exist on **lic** `main` (or feature branch), so plan-completion-audit and ingest do not report false gaps for gaming-physics kernels that are catalog-only.

## Current drift (updated 2026-05-20)

**Tier-2 (`benchmarks/tier2_physics/*`):** Verified against **`lic`** checkout (e.g. `feat/world-studio-impl-1` / nested `lic/`): all **`catalog.toml`** tier-2 rows resolve to existing harness directories.

**Tier-0 (`tier0_stability`):** Sources and **`li-tests`** entries live under **`li-tests/benchmarks/tier0_correctness/`** on **lic** (see `lic/benchmarks/harness/verify.py` → `tier0_sources()`). The org catalog previously pointed at **`benchmarks/tier0_correctness`**, which does not exist as a directory — **fixed in benchmarks** by setting `path = "li-tests/benchmarks/tier0_correctness"` so `plan-completion-audit` catalog_gaps = **0** when `LIC_ROOT` includes those files.

### Historical snapshot (2026-05-18)

Previously missing under some **lic** trees: eight tier-2 dirs + wrong tier-0 path — now addressed on current **lic** branch + catalog path correction above.

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
| C | **lic** PR(s): land tier-2 dirs on default branch; tier-0 stays under `li-tests/benchmarks/tier0_correctness` | `plan-completion-audit` catalog_gaps = 0 |
| D | **benchmarks** PR: catalog.toml sync (drop, defer, or point to shipped paths) | Ingest smoke green |
| E | Close **lic#24** when **benchmarks** `catalog.toml` tier0 path matches **lic** layout (done here) | Human verifies on `main` after merge |

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
