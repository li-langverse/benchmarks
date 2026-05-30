# Issue feature planner digest — 2026-05-30T15:24Z

**Run:** issue-feature-planner (li-langverse org scan, **benchmarks** repo scope)  
**Briefing:** 2026-05-30T14:02Z  
**north_star_fit:** Scientific computing / HPC — PH-5b (catalog honesty), PH-7e (tier-1 perf), G-math (partial); proof → easy → fast

---

## Executive summary

- Scanned **6 org repos** via `issue-feature-triage.py`: **32** `needs_plan`, **3** candidates (all **lic** studio-ui).
- **Benchmarks** repo: **1** `needs_plan` ([#18](https://github.com/li-langverse/benchmarks/issues/18)); **0** candidates.
- **No new plans drafted** — #18 plan current on [PR #136](https://github.com/li-langverse/benchmarks/pull/136) (`MERGEABLE`); issue comment refreshed 2026-05-30T13:41Z.
- **No implementation** — #18 lacks **`plan-approved`**; **lic** `benchmarks/tier1_micro/fft_1d_fixed/` absent on `main`; catalog row `catalog_lifecycle=planned`.
- **proof_gap_researcher handoff:** `provability_holes` priority 9 — active runs in control plane; lic **#472** (P-linalg loop ≡ ensures), **#527** (G-math-syn for/range gate), **#387** (PH-7d MIR proc tags) highest-signal for planner ↔ research coordination.
- **Blocked:** maintainer **`plan-approved`** on open plan PRs; **lic#473** / **#436** block swarm-gap refresh.
- **Deferred:** lic **28** master-plan-gap issues → lic-scoped planner; **#26** duplicate of #18 + merged vendor rubric plan.

---

## Deliverable / findings

### Issues scanned

| Repo | needs_plan | candidates | notes |
|------|------------|------------|-------|
| **lic** | 28 | 3 | studio-ui #394–399; PH-2i/7d/7e/8p backlog |
| **benchmarks** | 1 | 0 | #18 only (`feature` label; no `plan-needed`) |
| lip, lit | 0 | 0 | — |
| lis, roadmap | — | — | `gh` scan error / no open issues |

### Plans drafted (this run)

| Issue | Plan path | PR |
|-------|-----------|-----|
| — | — | — |

**Already planned (no duplicate work):**

| Issue | Plan path | PR |
|-------|-----------|-----|
| **#18** | `docs/ecosystem/plans/2026-05-29-tier1-fft-microbench-ph5b.md` (branch) · `2026-05-18-tier1-fft-microbench.md` (main) | [PR #136](https://github.com/li-langverse/benchmarks/pull/136) |
| #51, #52 | `2026-05-30-fft-vendor-rubrics-ph5b.md` | PR **#198** (merged) |
| #179 | `2026-05-30-catalog-path-reconciliation-ph5b.md` | PR **#183** |
| #181 | swarm-gap-actions plan | PR **#182** |
| #53 | PH-IO-7 summary parity | PR **#137** |

### Issues blocked

| Item | Reason |
|------|--------|
| **#18** harness | `fft_1d_fixed` catalog row planned; harness must land in **lic** (not copied to benchmarks) |
| All plan PRs without **`plan-approved`** | Implementation agents wait for maintainer label |
| **lic#473**, **#436** | swarm-gap-ingest + registry merge conflict |
| **lic#463**, **#424** | Tier-1 red rows — route to `bench_improver` / `numerics_researcher`; no threshold weakening |
| **gh API rate limit** | Transient 403 on `gh pr diff` — did not block triage or PR status checks |

### proof_gap_researcher handoff (provability_holes, priority 9)

Control plane (2026-05-30T15:24Z): **2** `proof_gap_researcher` runs `running`; recent cycles cover vec3_dot opaque ensures, mat2_at2 MIR, parallel disjoint Lean, method_call requires.

| Signal | lic issue | G-* / PH | Planner note |
|--------|-----------|----------|--------------|
| P-linalg loop ≡ ensures gate open | **#472** | G-lean, G-math, PH-2i | Sub-plan gate; pair with proof_gap_researcher cycle 33+ |
| for/range parse+typecheck Done gate | **#527** | G-math-syn, PH-2h | Language surface — plan home **lic** |
| MIR proc tags + Lean disjoint | **#387** | G-par, G-dec, PH-7d | Decorator lowering; blocks PH-7e tier-2 MD bench (#429) |
| NumPy-rank broadcast reject criteria | **#526** | G-math, PH-2i | Defer full rank until 2i-b closed |
| 6 tier-1 red benchmark rows | **#463**, **#424** | G-math, PH-7e | Perf evidence, not proof closure — bench_improver first |
| **G-ann**, **G-gpu**, **G-meta**, **G-authz** missing | — | provability-gaps.md | Do not plan-close without PH track |

**Recent proof_gap digests:** `data/digest/proof_gap_researcher-2026-05-30-*.md` (vec3_dot, mat2_at2, parallel_disjoint, method_call, horner_fma, sum_dot).

---

## Recommended issues/PRs

### Awaiting `plan-approved` (maintainer)

| PR | Title | Action |
|----|-------|--------|
| [#136](https://github.com/li-langverse/benchmarks/pull/136) | tier-1 FFT micro-bench (#18) | MERGEABLE — review + `plan-approved` on #18 |
| [#183](https://github.com/li-langverse/benchmarks/pull/183) | catalog path reconciliation (#179) | MERGEABLE |
| [#182](https://github.com/li-langverse/benchmarks/pull/182) | swarm-gap-actions (#181) | MERGEABLE |
| [#137](https://github.com/li-langverse/benchmarks/pull/137) | PH-IO-7 summary parity (#53) | Check mergeable (may need rebase) |
| [#135](https://github.com/li-langverse/benchmarks/pull/135) | LIC_ROOT preflight | Check mergeable (may need rebase) |

### Implementation queue (after approval)

| Issue | Repo | Agent |
|-------|------|-------|
| #18 FFT harness | **lic** | code_implementer / bench_improver |
| #179 catalog gaps | benchmarks + lic | code_implementer |
| lic #472 P-linalg gate | lic | proof_gap_researcher |
| lic #527 for/range gate | lic | issue_planner (lic scope) + proof_gap_researcher |

### lic candidates (out of benchmarks scope)

| Issue | Title | Labels |
|-------|-------|--------|
| [#399](https://github.com/li-langverse/lic/issues/399) | studio-ux-16 CI capture deps | — |
| [#398](https://github.com/li-langverse/lic/issues/398) | studio-ux-13 agentic_ai SOTA refs | — |
| [#394](https://github.com/li-langverse/lic/issues/394) | studio-ui-ux-capture-native.sh | — |

---

## Deferred

| Item | Reason |
|------|--------|
| **#26** roofline FFT harness | Duplicate of #18 + merged #51/#52 vendor rubric plan |
| lic **28** `needs_plan` | Wrong repo scope for benchmarks-attached run |
| lic studio-ui **#394–399** | Out of benchmarks scope; no vision pillar without PH track |
| Tier-1 red rows via threshold edits | Rejected per vision filter |
| Self-merge governance/roadmap PRs | Human-only |
| **fft_1d_fixed** near-threshold (1.007×) | Already green in audit — monitor only; no catalog-only closure |

---

<!-- li-agent-issue-feature-planner-digest-v1 -->
