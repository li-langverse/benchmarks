# Issue feature planner digest — 2026-05-30

**Run:** issue-feature-planner (benchmarks repo scope)  
**Briefing hash era:** 2026-05-30T04:06Z  
**north_star_fit:** Scientific computing / HPC — PH-5b (catalog honesty), PH-IO (agent signals), PH-7e (tier-1 perf); proof → easy → fast

---

## Executive summary

- Scanned **6 repos** via `issue-feature-triage.py`: **40** issues in `needs_plan`, **3** feature candidates (all **lic** studio-ui).
- **Benchmarks** repo: **12** `needs_plan`; **10** already had `li-agent-plan-v2` comments and draft/open plan PRs from prior passes.
- **New work this run:** drafted unified FFT vendor rubric plan for **#51** + **#52** → draft PR (pending push).
- **No implementation** — no issues carry **`plan-approved`**; harness/kernel code deferred.
- **proof_gap_researcher handoff:** 13 **G-*** partial + 4 missing rows; lic **#472** (P-linalg loop ≡ ensures) and **#461** (provability-gaps doc hygiene) are highest-signal planning targets.
- **Blocked / human-only:** `plan-approved` labels on 6 draft plan PRs (#135, #136, #137, #182, #183, + this run); **lic#473** blocks swarm-gap refresh.
- **Deferred:** lic studio-ui candidates (#394, #398, #399) — out of benchmarks scope; lic master-plan-gap backlog (28 issues) for lic-scoped planner pass.

---

## Deliverable / findings

### Issues scanned

| Repo | needs_plan | candidates | notes |
|------|------------|------------|-------|
| **lic** | 28 | 3 | studio-ui feats; 28 master-plan-gap / explorer |
| **benchmarks** | 12 | 0 | 10 pre-planned; **2 new** (#51, #52) |
| lip, lit | 0 | 0 | — |
| lis, roadmap | — | — | `gh` scan error / no issues |

### Plans drafted (this run)

| Issue | Plan path | PR |
|-------|-----------|-----|
| **benchmarks#51** | `docs/ecosystem/plans/2026-05-30-fft-vendor-rubrics-ph5b.md` | [PR #198](https://github.com/li-langverse/benchmarks/pull/198) |
| **benchmarks#52** | same (combined rubric) | [PR #198](https://github.com/li-langverse/benchmarks/pull/198) |

### Already planned (no duplicate work)

| Issue | Existing plan / PR |
|-------|-------------------|
| #18 | `2026-05-18-tier1-fft-microbench.md` · PR **#136** |
| #19 | `2026-05-18-tier2-catalog-lic-sync.md` |
| #20, #25, #28, #29, #54 | `2026-05-29-lic-root-agent-preflight.md` · PR **#135** |
| #53 | `2026-05-29-ph-io-7-summary-parity-gate.md` · PR **#137** |
| #179 | `2026-05-30-catalog-path-reconciliation-ph5b.md` · PR **#183** |
| #181 | `2026-05-30-swarm-gap-actions-sync.md` · PR **#182** |

### Issues blocked

| Item | Reason |
|------|--------|
| All `needs_plan` without **`plan-approved`** | Implementation agents must wait for maintainer label |
| **lic#473** | `swarm-gap-ingest.py` missing on main — blocks #181 refresh pipeline |
| **lic#436** | registry.yaml merge conflict — blocks gap ingest |
| lic candidates #394–399 | Wrong repo scope (studio-ui → **lic** planner) |
| lic #463/#424 (tier-1 red rows) | Perf work, not planning-only; route to `bench_improver` / `numerics_researcher` — **no threshold weakening** |

### proof_gap_researcher handoff (provability_holes, priority 9)

Research goal eligible — cite on handoff:

| Signal | Source | Suggested focus |
|--------|--------|-----------------|
| **G-lean** partial — `sqrt_open_bound`, `mat2_at2_eval` | provability-gaps.md | lic **#472** P-linalg loop ≡ ensures gate |
| **G-par** / **G-dec** partial | master plan PH-7d | lic **#387** MIR proc tags + Lean disjoint |
| **G-math** partial — 6 tier-1 red rows | ecosystem-audit | lic **#463**, **#424** (implementation, not catalog-only) |
| **G-ann**, **G-gpu**, **G-meta**, **G-authz** missing | provability-gaps.md | Do not plan-close without PH track |
| Doc hygiene | lic **#461** | Duplicate Proof-db appendix — quick win for honesty |

**north_star_fit:** Mathematical provability pillar; PH-2i, PH-7d, PH-7e, Phase 2f Lean gate.

---

## Recommended issues/PRs

### Awaiting `plan-approved` (maintainer)

| PR | Title | Labels to add after review |
|----|-------|------------------------------|
| [#183](https://github.com/li-langverse/benchmarks/pull/183) | catalog path reconciliation PH-5b (#179) | `plan-approved` on #179 |
| [#182](https://github.com/li-langverse/benchmarks/pull/182) | swarm-gap-actions refresh (#181) | `plan-approved` on #181 |
| [#135](https://github.com/li-langverse/benchmarks/pull/135) | LIC_ROOT agent preflight (#20–#29, #54) | `plan-approved` on linked issues |
| [#136](https://github.com/li-langverse/benchmarks/pull/136) | tier-1 FFT micro-bench (#18) | `plan-approved` on #18 |
| [#137](https://github.com/li-langverse/benchmarks/pull/137) | PH-IO-7 summary parity (#53) | `plan-approved` on #53 |
| [#198](https://github.com/li-langverse/benchmarks/pull/198) | FFT vendor rubrics (#51, #52) | `plan-approved` on #51, #52 |

### Implementation queue (after approval)

| Issue | Repo | Agent |
|-------|------|-------|
| #179 catalog 117 gaps | benchmarks | code_implementer + lic harness routing |
| #181 swarm-gap sync | benchmarks + lic | agent_kit / plan_verifier |
| lic #472 P-linalg gate | lic | proof_gap_researcher |

---

## Deferred

- **#51/#52 pure-Li FFT** — numerics study + parent #18 harness first; no catalog-only closure.
- **lic studio-ui #394–399** — defer to lic-scoped issue planner.
- **Explorer rubrics** PETSc/Kokkos/OpenMP (#116–#129) — research rubrics; batch in lic explorer pass.
- **Weakening `threshold_ratio_cpp`** for red tier-1 rows — rejected per vision filter.
- **Self-merge** governance/roadmap PRs — not attempted.

---

<!-- li-agent-issue-feature-planner-digest-v1 -->
