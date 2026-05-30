# Issue feature planner digest — 2026-05-30 (pass 2)

**Run:** issue-feature-planner · benchmarks repo scope  
**Triage:** `2026-05-30T11:10Z` · briefing `2026-05-30T10:59Z`  
**north_star_fit:** HPC / scientific computing — PH-5b (catalog honesty), PH-IO (agent signals), PH-7e (tier-1 perf); **proof → easy → fast**  
**Research handoff:** `provability_holes` priority 9 → **proof_gap_researcher**

---

## Executive summary

- Scanned **6 repos** (`issue-feature-triage.py`): **42** `needs_plan`, **3** candidates (all **lic** studio-ui).
- **Benchmarks:** **11** `needs_plan` — **all** have `li-agent-plan-v2` comments and on-repo or merged plan docs; **no new plans** this pass (duplicate avoidance).
- **Merged since last digest:** [PR #198](https://github.com/li-langverse/benchmarks/pull/198) — FFT vendor rubrics (#51, #52) on `main`.
- **No implementation** — zero issues carry **`plan-approved`**; catalog/harness work blocked on maintainer labels.
- **Ecosystem benches:** 22 green, 5 **near_threshold** (≤1.08× cpp); **no** threshold weakening proposed.
- **proof_gap_researcher:** 13 **G-*** partial + 4 missing; top lic targets **#472**, **#387**, **#527**/**#526** (newest PH-2h/2i gates).
- **Lic backlog:** **31** master-plan-gap issues; **#525**, **#461** lack planner v2 comments — next **lic-scoped** planner pass.
- **Human-only:** approve **5 open** plan PRs (#135–#137, #182, #183); resolve **lic#436** registry conflict and **lic#473** ingest script on `main`.

---

## Deliverable / findings

### Issues scanned

| Repo | needs_plan | candidates | notes |
|------|------------|------------|-------|
| **lic** | 31 | 3 | #394–399 studio-ui; #525/#461 unplanned |
| **benchmarks** | 11 | 0 | fully planned |
| lip, lit | 0 | 0 | — |
| lis, roadmap | — | — | `gh` scan error / no issues |

### Plans drafted (this run)

| Issue | Plan | PR |
|-------|------|-----|
| — | *None — benchmarks queue complete* | — |

### Already planned (benchmarks)

| Issue | Plan / PR |
|-------|-----------|
| #18 | `2026-05-18-tier1-fft-microbench.md` · [#136](https://github.com/li-langverse/benchmarks/pull/136) |
| #19 | `2026-05-18-tier2-catalog-lic-sync.md` |
| #20, #25, #28, #29, #54 | LIC_ROOT preflight · [#135](https://github.com/li-langverse/benchmarks/pull/135) |
| #51, #52 | `2026-05-30-fft-vendor-rubrics-ph5b.md` · [#198](https://github.com/li-langverse/benchmarks/pull/198) **merged** |
| #53 | PH-IO-7 parity · [#137](https://github.com/li-langverse/benchmarks/pull/137) |
| #179 | catalog path reconciliation · [#183](https://github.com/li-langverse/benchmarks/pull/183) |
| #181 | swarm-gap-actions sync · [#182](https://github.com/li-langverse/benchmarks/pull/182) |

### Issues blocked

| Item | Reason |
|------|--------|
| All `needs_plan` without **`plan-approved`** | Implementation agents wait for maintainer |
| Open plan PRs #135–137, #182, #183 | Draft docs not merged; need review + label |
| **lic#473** | `swarm-gap-ingest.py` not on `main` — blocks #181 pipeline |
| **lic#436** | `registry.yaml` merge conflict |
| lic #463/#424 | Tier-1 perf reds — **bench_improver** / **lic** kernels, not catalog-only |
| lic #525, #461 | No `li-agent-plan-v2` yet — lic-scoped planner |

### proof_gap_researcher handoff (provability_holes)

| Priority | Issue / signal | PH / G-* | Action |
|----------|----------------|----------|--------|
| P0 | lic **#472** P-linalg loop ≡ `ensures` | PH-2i, PH-2f, **G-lean**, **G-math** | Lean corpus + `lic build`; split open obligations in math-linalg sub-plan |
| P0 | lic **#387** MIR proc tags + disjoint | PH-7d, **G-par**, **G-dec** | Plan in **lic** `docs/superpowers/plans/` (has plan-needed, verify v2) |
| P1 | lic **#527** for/range parse+typecheck gate | PH-2h, **G-math-syn** | v2 posted — await `plan-approved` |
| P1 | lic **#526** NumPy-rank broadcast reject gate | PH-2i, **G-math** | v2 posted — await `plan-approved` |
| P2 | lic **#461** provability-gaps doc hygiene | honesty | Quick doc PR; no G-* closure claim |
| Defer | **G-ann**, **G-gpu**, **G-meta**, **G-authz** missing | — | No PH track → defer per vision filter |

**Catalog honesty (benchmarks only):** 117 `catalog_gaps` ([#179](https://github.com/li-langverse/benchmarks/issues/179)) — triage paths / `status=planned`; harness stays in **lic**.

**Near-threshold tier-1 (monitor, do not weaken gates):** `num_integ_rk4`, `matmul_naive`, `simd_dot`, `matmul_blocked`, `fft_1d_fixed`.

---

## Recommended issues/PRs

### Awaiting `plan-approved` (maintainer)

| PR | Issues | State |
|----|--------|-------|
| [#183](https://github.com/li-langverse/benchmarks/pull/183) | #179 | OPEN |
| [#182](https://github.com/li-langverse/benchmarks/pull/182) | #181 | OPEN |
| [#135](https://github.com/li-langverse/benchmarks/pull/135) | #20, #25, #28, #29, #54 | OPEN |
| [#136](https://github.com/li-langverse/benchmarks/pull/136) | #18 | OPEN |
| [#137](https://github.com/li-langverse/benchmarks/pull/137) | #53 | OPEN |
| [#198](https://github.com/li-langverse/benchmarks/pull/198) | #51, #52 | **MERGED** — add `plan-approved` on issues |

### After approval — agent routing

| Issue | Repo | Agent |
|-------|------|-------|
| #179 (117 catalog gaps) | benchmarks + lic | code_implementer |
| #18 FFT harness | lic | bench_improver / numerics |
| #181 swarm-gap sync | benchmarks + lic | plan_verifier |
| #472 P-linalg Lean gate | lic | **proof_gap_researcher** |
| #525 `--jobs` wiring | lic | code_implementer (after plan) |

---

## Deferred

- **Benchmarks new plans** — queue complete until maintainer approves open PRs.
- **lic studio-ui #394–399** — lic-scoped planner.
- **lic #525, #461** — draft plans on next lic pass (max 3/issue cap).
- **Explorer rubrics** (#124–#129, PETSc/Kokkos) — batch research; not blocking P0 gates.
- **`threshold_ratio_cpp` weakening** — rejected.
- **Self-merge** roadmap/governance PRs — not attempted.
- **Actions `schedule:` cron** — not added.

---

<!-- li-agent-issue-feature-planner-digest-v2 -->
