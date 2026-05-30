# Issue feature planner digest — 2026-05-30T13:13Z

**Run:** issue-feature-planner (org scan; **benchmarks** repo scope for planning)  
**Briefing:** 2026-05-30T12:07Z · **north_star_fit:** HPC/scientific computing — PH-5b (catalog honesty), PH-IO (agent signals), PH-7e (tier-1 perf); proof → easy → fast

---

## Executive summary

- Scanned **6 repos** via `issue-feature-triage.py`: **42** issues in `needs_plan`, **3** feature candidates (all **lic** studio-ui).
- **Benchmarks** repo: **11** `needs_plan`; **all 11** now have plan comments or duplicate routing — **no new plan PRs** required this pass.
- **New work this run:** posted duplicate cross-links on **#25**, **#28**, **#29** → umbrella **#20** / PR **#135**.
- **No implementation** — zero issues carry **`plan-approved`**; harness/kernel code remains blocked.
- **proof_gap_researcher handoff:** 13 **G-*** partial + 4 missing; lic **#527** (G-math-syn), **#472** (P-linalg), **#387** (G-par) are highest-signal targets.
- **Catalog debt unchanged:** 117 `catalog_gaps` (PH-5b); draft PR **#183** awaits maintainer **`plan-approved`**.
- **lic backlog:** 31 `plan-needed` master-plan-gap issues — defer to lic-scoped planner pass (out of benchmarks scope).
- **FFT vendor rubrics merged:** PR **#198** on `main`; **#51**/**#52** await **`plan-approved`** only.

---

## Deliverable / findings

### Issues scanned

| Repo | needs_plan | candidates | notes |
|------|------------|------------|-------|
| **lic** | 31 | 3 | studio-ui #394–399; 31 master-plan-gap / explorer |
| **benchmarks** | 11 | 0 | All planned or duplicate-routed |
| lip, lit | 0 | 0 | — |
| lis, roadmap | — | — | `gh` scan error / no issues |

### Plans drafted (this run)

| Issue | Action | Plan / PR |
|-------|--------|-----------|
| **#25**, **#28**, **#29** | Duplicate cross-link posted | Umbrella **#20** · [PR #135](https://github.com/li-langverse/benchmarks/pull/135) |

### Already planned (no duplicate work)

| Issue | Existing plan / PR |
|-------|-------------------|
| #18 | `2026-05-18-tier1-fft-microbench.md` · PR **#136** |
| #19 | `2026-05-18-tier2-catalog-lic-sync.md` (on `main`; partial defer 2026-05-29) |
| #20, #54 | `2026-05-29-lic-root-agent-preflight.md` · PR **#135** |
| #51, #52 | `2026-05-30-fft-vendor-rubrics-ph5b.md` · PR **#198** (**merged**) |
| #53 | `2026-05-29-ph-io-7-summary-parity-gate.md` · PR **#137** |
| #179 | `2026-05-30-catalog-path-reconciliation-ph5b.md` · PR **#183** |
| #181 | swarm-gap-actions sync · PR **#182** |

### Issues blocked

| Item | Reason |
|------|--------|
| All `needs_plan` without **`plan-approved`** | Implementation agents must wait for maintainer label |
| **lic#473** | `swarm-gap-ingest.py` missing on main — blocks #181 refresh |
| **lic#436** | registry.yaml merge conflict — blocks gap ingest |
| lic candidates #394–399 | Wrong repo scope (studio-ui → **lic** planner) |
| lic #463/#424 (tier-1 red rows) | Perf work → `bench_improver` / `numerics_researcher`; **no threshold weakening** |
| 6 tier-1 **red** rows | matmul_blocked, matmul_naive, ml_*, num_gmres — PH-5b/PH-7e |

### proof_gap_researcher handoff (provability_holes, priority 9)

Research goal eligible — cite on handoff:

| Signal | Source | Suggested focus |
|--------|--------|-----------------|
| **G-math-syn** partial — `for`/`range` | provability-gaps.md | lic **#527** — parse+typecheck Done gate (PH-2h) |
| **G-lean** partial — `sqrt_open_bound`, `mat2_at2_eval` | provability-gaps.md | lic **#472** P-linalg loop ≡ ensures gate |
| **G-par** / **G-dec** partial | master plan PH-7d | lic **#387** MIR proc tags + Lean disjoint |
| **G-math** partial — 6 tier-1 red rows | ecosystem-audit | lic **#463**, **#424** (implementation, not catalog-only) |
| **G-ann**, **G-gpu**, **G-meta**, **G-authz** missing | provability-gaps.md | Do not plan-close without PH track |
| NumPy broadcast defer | lic **#526** | PH-2i reject gate + defer criteria |

**north_star_fit:** Mathematical provability pillar; PH-2h, PH-2i, PH-7d, PH-7e.

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

### lic backlog — next planner pass (top 3)

| Issue | Title | PH / G |
|-------|-------|--------|
| [lic#527](https://github.com/li-langverse/lic/issues/527) | for/range surface Done gate | PH-2h, G-math-syn |
| [lic#526](https://github.com/li-langverse/lic/issues/526) | NumPy-rank broadcast reject gate | PH-2i, G-math |
| [lic#525](https://github.com/li-langverse/lic/issues/525) | `lic build --jobs=N` not wired | PH-8p-c |

### Implementation queue (after approval)

| Issue | Repo | Agent |
|-------|------|-------|
| #179 catalog 117 gaps | benchmarks + lic | code_implementer + lic harness routing |
| #181 swarm-gap sync | benchmarks + lic | agent_kit / plan_verifier |
| lic #472 P-linalg gate | lic | proof_gap_researcher |

---

## Deferred

- **lic studio-ui #394–399** — defer to lic-scoped issue planner.
- **Explorer rubrics** PETSc/Kokkos/OpenMP (lic #116–#129) — research rubrics; batch in lic explorer pass.
- **Sim runners idle** (lic #521–#523, #478) — supervisor/research debt; not benchmarks catalog work.
- **Weakening `threshold_ratio_cpp`** for red tier-1 rows — rejected per vision filter.
- **Self-merge** governance/roadmap PRs — not attempted.

---

<!-- li-agent-issue-feature-planner-digest-v1 -->
