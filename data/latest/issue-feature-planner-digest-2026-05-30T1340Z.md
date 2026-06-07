# Issue feature planner digest — 2026-05-30T13:40Z

**Run:** issue-feature-planner (li-langverse org scan, **benchmarks** repo scope)  
**Briefing:** 2026-05-30T12:07Z  
**north_star_fit:** Scientific computing / HPC — PH-5b (catalog honesty), PH-7e (tier-1 perf), G-math (partial); proof → easy → fast

---

## Executive summary

- Scanned **6 org repos** via `issue-feature-triage.py`: **32** `needs_plan`, **3** candidates (all **lic** studio-ui).
- **Benchmarks** repo: **1** `needs_plan` ([#18](https://github.com/li-langverse/benchmarks/issues/18)); **0** candidates — prior passes already drafted plans for explorer/LIC_ROOT issues (labels not always `plan-needed`).
- **No new plans drafted** this run — #18 plan refreshed on rebased [PR #136](https://github.com/li-langverse/benchmarks/pull/136) (was CONFLICTING).
- **No implementation** — no benchmarks issues carry **`plan-approved`**; lic harness for `fft_1d_fixed` still missing on **lic** `main`.
- **proof_gap_researcher handoff:** 13 G-* partial + 4 missing; lic **#472** (P-linalg loop ≡ ensures) and **#387** (PH-7d MIR proc tags) highest-signal.
- **Blocked:** maintainer **`plan-approved`** on 6 open plan PRs; **lic#473** / **#436** block swarm-gap refresh.
- **Deferred:** lic **28** master-plan-gap issues → lic-scoped planner; **#26** duplicate of merged vendor rubric plan.

---

## Deliverable / findings

### Issues scanned

| Repo | needs_plan | candidates | notes |
|------|------------|------------|-------|
| **lic** | 28 | 3 | studio-ui #394–399; PH-2i/7d/7e/8p backlog |
| **benchmarks** | 1 | 0 | #18 only (feature label) |
| lip, lit | 0 | 0 | — |
| lis, roadmap | — | — | `gh` scan error / no open issues |

### Plans drafted (this run)

| Issue | Plan path | PR |
|-------|-----------|-----|
| — | — | — |

**Rebased (not new):**

| Issue | Plan path | PR |
|-------|-----------|-----|
| **#18** | `docs/ecosystem/plans/2026-05-29-tier1-fft-microbench-ph5b.md` | [PR #136](https://github.com/li-langverse/benchmarks/pull/136) (rebased on `main`) |

### Already planned (no duplicate work)

| Issue | Existing plan / PR |
|-------|-------------------|
| #51, #52 | `2026-05-30-fft-vendor-rubrics-ph5b.md` · PR **#198** (merged) |
| #179 | `2026-05-30-catalog-path-reconciliation-ph5b.md` · PR **#183** |
| #181 | swarm-gap-actions plan · PR **#182** |
| #20, #25, #28, #29, #54 | LIC_ROOT preflight · PR **#135** |
| #53 | PH-IO-7 summary parity · PR **#137** |

### Issues blocked

| Item | Reason |
|------|--------|
| **#18** harness | `catalog_lifecycle=planned`; workloads exist under **benchmarks** mirror only — **lic** `benchmarks/tier1_micro/fft_1d_fixed/` absent |
| All plan PRs without **`plan-approved`** | Implementation agents wait for maintainer label |
| **lic#473**, **#436** | swarm-gap-ingest + registry conflict |
| lic **#463**, **#424** | Tier-1 red rows — route to `bench_improver` / `numerics_researcher`; no threshold weakening |

### proof_gap_researcher handoff (provability_holes, priority 9)

| Signal | Source | Suggested focus |
|--------|--------|-----------------|
| **G-lean** partial | provability-gaps.md | lic **#472** P-linalg loop ≡ ensures |
| **G-par** / **G-dec** partial | PH-7d | lic **#387** MIR proc tags + Lean disjoint |
| **G-math** partial — 6 tier-1 red | ecosystem-audit | lic **#463**, **#424** |
| **G-ann**, **G-gpu**, **G-meta**, **G-authz** missing | provability-gaps.md | Do not plan-close without PH track |

---

## Recommended issues/PRs

### Awaiting `plan-approved` (maintainer)

| PR | Title | Action |
|----|-------|--------|
| [#136](https://github.com/li-langverse/benchmarks/pull/136) | tier-1 FFT micro-bench (#18) | Rebased — review + `plan-approved` on #18 |
| [#183](https://github.com/li-langverse/benchmarks/pull/183) | catalog path reconciliation (#179) | MERGEABLE |
| [#182](https://github.com/li-langverse/benchmarks/pull/182) | swarm-gap-actions (#181) | MERGEABLE |
| [#135](https://github.com/li-langverse/benchmarks/pull/135) | LIC_ROOT preflight | CONFLICTING — needs rebase |
| [#137](https://github.com/li-langverse/benchmarks/pull/137) | PH-IO-7 summary parity (#53) | CONFLICTING — needs rebase |

### Implementation queue (after approval)

| Issue | Repo | Agent |
|-------|------|-------|
| #18 FFT harness | **lic** | code_implementer / bench_improver |
| #179 catalog 117 gaps | benchmarks + lic | code_implementer |
| lic #472 P-linalg gate | lic | proof_gap_researcher |

---

## Deferred

| Item | Reason |
|------|--------|
| **#26** roofline FFT harness | Duplicate of #18 + merged #51/#52 vendor rubric plan |
| lic **28** `needs_plan` | Wrong repo scope for benchmarks-attached run |
| lic studio-ui **#394–399** | Out of benchmarks scope |
| Tier-1 red rows via threshold edits | Rejected per vision filter |
| Self-merge governance/roadmap PRs | Human-only |

---

<!-- li-agent-issue-feature-planner-digest-v1 -->
