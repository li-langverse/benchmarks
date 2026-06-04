# Issue feature planner digest — 2026-05-31T01:00Z

**Agent:** issue_planner · **Repo focus:** benchmarks (+ org triage)  
**Skill:** `plan-feature-from-issue` · **Vision:** [vision-and-roadmap.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md)

## Executive summary

- Scanned **6 org repos** via `issue-feature-triage.py`: **33** `needs_plan` (lic), **1** benchmarks `needs_plan` (#18), **3** lic candidates (studio-ui).
- **benchmarks#18** — plan on `main` (`2026-05-18-tier1-fft-microbench.md`); **lic** harness landed (`fft_1d_fixed` **1.006×** green); blocked on human **`plan-approved`** and `catalog_lifecycle` promotion.
- **benchmarks#179** — refreshed plan (117-gap spike **resolved** with LIC_ROOT; policy for `planned` rows remains).
- **benchmarks#41** — new plan for **pure_li** variant expansion (PH-7e codegen surface).
- **No implementation** — no issue carries **`plan-approved`**.
- **lic backlog:** 32 master-plan-gap issues deferred this run (compiler/PH-* scope → lic repo).
- **Swarm handoff:** `swarm_coverage` — catalog honesty + pure-Li proof surface supports `swarm_observer` tier-1 monitoring.

## Deliverable / findings

### Issues scanned

| Repo | needs_plan | candidates | planned |
|------|------------|------------|---------|
| lic | 33 | 3 | 0 |
| benchmarks | 1 (#18) | 0 | 0 |
| lip, lit | 0 | 0 | 0 |
| lis, roadmap | gh empty/error | — | — |
| **Total** | **34** | **3** | **0** |

### Plans drafted (this run)

| Issue | Plan path | PR |
|-------|-----------|-----|
| **benchmarks#41** | `docs/ecosystem/plans/2026-05-31-pure-li-variant-expansion-ph7e.md` | [PR #262](https://github.com/li-langverse/benchmarks/pull/262) |
| **benchmarks#179** | `docs/ecosystem/plans/2026-05-31-catalog-path-reconciliation-ph5b.md` | [PR #263](https://github.com/li-langverse/benchmarks/pull/263) |
| **benchmarks#18** | `docs/ecosystem/plans/2026-05-18-tier1-fft-microbench.md` (existing on main) | status refresh comment only |

### PH / REQ mapping

| Issue | PH-* | REQ-* | G-* |
|-------|------|-------|-----|
| #18 | PH-5b, PH-7e | REQ-BENCH-FFT-1 | G-math Partial (perf only) |
| #41 | PH-7e, PH-5b | REQ-BENCH-PURELI-1 | G-math Partial |
| #179 | PH-5b, PH-7e | REQ-BENCH-CATALOG-1 | honesty gate only |

### Issues blocked (human-only)

| Issue | Blocker |
|-------|---------|
| #18, #41, #179 | Maintainer **`plan-approved`** before catalog/harness PRs |
| #18 | Promote `catalog_lifecycle` from `planned` → active after review |
| lic #574, #526, #387 | Compiler/Lean scope — lic planner pass; not benchmarks |

### Deferred

| Item | Reason |
|------|--------|
| lic 32× `master-plan-gap` | Language/compiler PH-* — plan home is **lic** `docs/superpowers/plans/` |
| lic #399, #398, #394 (candidates) | Studio-ui UX; out of benchmarks scope |
| #26 roofline FFT | Duplicate of #18 + merged vendor rubrics (#51/#52, PR #198) |
| Threshold weakening | Vision filter — rejected |

## Recommended issues/PRs

| Target | Repo | Labels needed |
|--------|------|---------------|
| [Pure-Li variant expansion (#41)](https://github.com/li-langverse/benchmarks/issues/41) | benchmarks | `plan-approved` |
| [Catalog path reconciliation (#179)](https://github.com/li-langverse/benchmarks/issues/179) | benchmarks | `plan-approved` |
| [Tier-1 FFT micro-bench (#18)](https://github.com/li-langverse/benchmarks/issues/18) | benchmarks | `plan-approved` |
| lic#424 / lic#463 tier-1 red/yellow | lic | plan-approved on parent bench issues |

## Errors

None this run.
