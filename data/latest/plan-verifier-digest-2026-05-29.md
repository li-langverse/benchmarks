# Plan verifier digest — 2026-05-29

**Agent:** `plan_verifier` · **Queued:** `heap:coord_governance:plan_verifier` · **North star:** proof → easy → fast · **Audit:** `plan-completion-audit.json` @ 2026-05-29T17:53Z · **Ingest:** `lic/scripts/swarm-gap-ingest.py` confirmed (84 registry gaps, +0 delta)

## Executive summary

- **166 total findings** — 5 open master-plan tracker rows, 26 open sub-plan gates, 117 catalog path gaps; 31 tracker phases marked complete.
- **Active PH partial rows:** 2i, 7d, 7e, 8p, Vision-LLM — all remain `[ ]` at `lic/docs/superpowers/plans/2026-05-14-li-master-plan.md:444–473`; none closable without new Lean/tests or perf evidence.
- **Provability:** 13 **Partial** + 4 **Missing** G-* rows in `provability-gaps.md`; zero G-* at **Done** (honest register holds).
- **Ecosystem P0:** 34 failing PRs block new feature work (`ecosystem-audit.json`); plan debt is P1 behind CI.
- **Goal-directed runners:** 11 `plan_pending` todos across httpd (2), sim (3), sim-md-research (1), sim-chem-research (2), security-research (3); compiler-studio loop idle with `wave-d-gui-scaffold` in_progress but empty `plan_pending`.
- **Registry drift:** httpd `gap-phase2-perf-wrk-soak` / `gap-phase2-streaming-wrk` still pending in snapshot but dedupe-closed in `registry.yaml` — swarm_observer should reopen canonical rows on next ingest fix.
- **Swarm ingest:** ran clean; no new `plan_debt_snapshot` rows (mapping already present).
- **Issues filed this pass:** 0 (existing #385–387, #19, #27, #387 cover master-plan gaps; httpd/sim/security loops own runner debt).

## Tracker review

| PH | Status | Evidence (file / test) | Close gate |
|----|--------|------------------------|------------|
| **2i** | **partial — open** | Length-1 broadcast: `li-tests/math_linalg/broadcast_len1_mul_int4.li`, `broadcast_len1_add_float4.li`; lowering `compiler/mir/lower.cpp:413–434`, `emit.cpp:995–1030`. Sub-plan 2i-b `[x]` at `plans/2026-05-16-li-math-linalg-surface.md:170`. | **Open:** full NumPy-rank broadcast; master tracker still lists length-1 as open → reconcile via lic#386 |
| **7d** | **partial — open** | `@vectorized` on `for` → `ArraySimdScope` (#150). Gap tests: `li-tests/tooling/parallel_decorator_policy_capture_gap.sh`, `parallel_decorator_for_elaboration_gap.sh` (G-par/G-dec). | **Open:** MIR proc tags + Lean **G-par** proofs; lic#387 |
| **7e** | **partial — open** | Closed slices: `matmul_naive`, `horner_pure_li` ≤1.2× via `scripts/check-tier1-li-vs-cpp.sh`; `li-tests/math_linalg/` corpus. **Yellow:** `matmul_blocked` (ecosystem audit). | **Open:** remaining tier-1 strict rows + float Lean Props; lic#27, lic#49 |
| **8p** | **partial — open** | Ninja `-j` for C++ only. `--jobs=N` sets `LI_COMPILE_JOBS` env (`compiler/lic/main.cpp:161–163`) but frontend still sequential. | **Open:** 8p-b workspace pool + 8p-d wall-time SLO; lic#385 |
| **Vision-LLM** | **partial — open** | v0 shipped: `lic check --format=json`, `lic diagnose`, `diagnostic-v1` schema, `li-tests/tooling/diagnose_json_smoke.sh`. | **Open:** compact test manifest export, `lic-fix-suggest.sh` beyond stub; lic#19 |

**Sub-plan gates (26 open, sample):** P-linalg Lean loop≡closed-form still `[ ]` at `plans/2026-05-16-li-math-linalg-surface.md` (**G-lean**); tier-1 perf gate `[ ]` same file; phase-07 HPC decorator/fuzz/tier-1 rows at `plans/2026-05-14-phase-07-native-hpc.md`.

**Snapshot → registry `plan_debt` map:**

| Runner | `plan_pending` | Registry id |
|--------|----------------|-------------|
| httpd | `gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk` | `gap-plan-pending-httpd-gap-phase2-*` (deduped; **closed** in registry — drift) |
| sim | `sim-p1-num-dot-axpy`, `sim-p1-md-neighbor-cell`, `sim-p2-qm-dft-scf` | `gap-plan-pending-sim-sim-p1-*`, `gap-plan-pending-sim-sim-p2-qm-dft-scf` (**open**) |
| sim-md-research | `md-r3-oracle-plan` | `gap-plan-pending-sim-md-research-md-r3-oracle-plan` (**open**) |
| sim-chem-research | `chem-r2-dft-scf-gap`, `chem-r3-package-placement` | `gap-plan-pending-sim-chem-research-chem-r2-*`, `chem-r3-*` (**open**) |
| security-research | `sec-r1-httpd-fuzz-smoke`, `sec-r2-tier5-gap-exploit`, `sec-r3-runtime-surface` | `gap-plan-pending-security-research-sec-r1-*` … `sec-r3-*` (**open**) |

## Provability / G-*

From `lic/docs/verification/provability-gaps.md` (last updated 2026-05-21):

| Tier | IDs | Master-plan tie-in |
|------|-----|-------------------|
| **Partial (13)** | G-lean, G-vc, G-par, G-dec, G-math, G-bnd, G-def, G-oop, G-math-syn, G-async, G-net, G-trust, G-narrow | PH-2i/7d/7e/2f; P-linalg, P-float, P-par open |
| **Missing (4)** | G-ann, G-gpu, G-meta, G-authz | Deferred / research / OS phase |
| **Key blockers** | **G-par:** `@parallel` on plain `for` bypasses capture policy (`parallel_decorator_policy_capture_gap.sh`). **G-math:** `matmul_blocked` tier-1 yellow; full NumPy broadcast open. **G-lean:** `sqrt_open_bound` intentional open (`sqrt_open_bound_contract_tier.sh`). |

Audit `recommended_actions` aligns: P1 close/update 5 tracker rows + sync provability-gaps; P2 catalog 117 rows; P3 archive 9 stale normative checklists in phase-02 typechecker plan.

## Recommended issues

No new issues filed — duplicates of today's tracker coverage. Route via existing issues + orchestrator loops:

| Priority | Repo | Issue | Labels | PH / G-* |
|----------|------|-------|--------|----------|
| P1 | lic | [#386](https://github.com/li-langverse/lic/issues/386) | `plan-needed`, `master-plan-gap` | PH-2i — reconcile length-1 broadcast closed vs tracker |
| P1 | lic | [#387](https://github.com/li-langverse/lic/issues/387) | `plan-needed`, `master-plan-gap` | PH-7d / **G-par** — MIR proc tags + Lean disjoint proofs |
| P1 | lic | [#385](https://github.com/li-langverse/lic/issues/385) | `plan-needed`, `master-plan-gap` | PH-8p — parallel workspace pool + wall-time SLO |
| P1 | lic | [#27](https://github.com/li-langverse/lic/issues/27) | `master-plan-gap` | PH-7e / **G-math** — tier-1 Done criteria (`matmul_blocked`) |
| P2 | lic | [#19](https://github.com/li-langverse/lic/issues/19) | `plan-needed`, `master-plan-gap` | Vision-LLM — manifest CI + compact test export |
| P2 | lic | [#49](https://github.com/li-langverse/lic/issues/49) | `plan-needed`, `master-plan-gap` | **G-math** summary table drift vs register |

**Runner handoffs (orchestrator loops apply — do not duplicate as master-plan issues):** httpd loop → 2 pending perf gates; sim / sim-md-research / sim-chem-research → algo registry; security-research → tier5 fuzz/exploit surface.

## Deferred

- No plan checkbox edits or gate weakening (evidence-required policy).
- No implementation (`plan-approved` agents only).
- Catalog 117-row P2 sweep deferred to `gap_explorer` / `implementation_gaps`.
- Stale phase-02 normative checklists (9 rows) — doc hygiene, not release blockers.
- Filing net-new GitHub issues skipped where #385–387 and runner loops already cover debt.
- `lic` registry.yaml ingest delta committed in lic repo separately if needed (benchmarks pass is digest-only).

**north_star_fit:** domain=governance/plan-honesty · PH=2i,7d,7e,8p,Vision-LLM · pillar=provable (G-* register must not overclaim)
