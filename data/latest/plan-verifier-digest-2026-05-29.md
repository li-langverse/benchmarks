# Plan verifier digest — 2026-05-29

**Agent:** `plan_verifier` · **Queued:** `heap:coord_governance:plan_verifier:fed3b4b19bafa90f6e8d` · **North star:** proof → easy → fast · **Audit:** `plan-completion-audit.json` @ 2026-05-29T17:58Z · **Ingest:** `lic/scripts/swarm-gap-ingest.py` (84 registry gaps, +0 delta)

## Executive summary

- **166 total findings** — 5 open master-plan tracker rows (`2i`, `7d`, `7e`, `8p`, `Vision-LLM`), 26 open sub-plan gates, 117 catalog path gaps; 31 tracker phases complete.
- **None of the 5 PH rows are closable** without new Lean proofs, tier-1 perf evidence, or doc reconciliation in the same PR as implementation.
- **Provability register:** 13 **Partial** + 4 **Missing** G-* IDs; zero G-* at **Done** (`provability-gaps.md` honest posture holds).
- **Ecosystem P0:** 34 failing PRs (`ecosystem-audit.json`); plan debt is P1 behind CI — aligns with audit `recommended_actions`.
- **Tier-1 perf:** `matmul_blocked` red at 1.55× cpp; `matmul_naive` red at 1.33× — blocks PH-7e “closed slice” claims until `check-tier1-li-vs-cpp.sh` strict passes.
- **Goal-directed:** 11 `plan_pending` todos across httpd (2), sim (3), sim-md-research (1), sim-chem-research (2), security-research (3); compiler-studio idle with empty `plan_pending`.
- **Registry drift:** httpd `gap-phase2-perf-wrk-soak` / `gap-phase2-streaming-wrk` still **pending** in snapshot but **closed** (deduped) in `registry.yaml` — swarm_observer / ingest dedupe bug; not a new master-plan issue.
- **Swarm ingest:** ran clean; no new `plan_debt_snapshot` rows this pass.

## Tracker review

Open PH / master-plan rows (`lic/docs/superpowers/plans/2026-05-14-li-master-plan.md:444–473`). Mark **done** only with tests/Lean cite in same PR.

| PH | Status | Evidence (file / test) | Close gate |
|----|--------|------------------------|------------|
| **2i** | **partial — open** | **Closed slices:** `li-tests/math_linalg/norm_*.li`, `reductions/`, `axpy_float4.li`, `dot_float_arrays.li`; length-1 broadcast tests `broadcast_len1_mul_int4.li`, `broadcast_len1_add_float4.li`. Sub-plan **2i-b** `[x]` at `plans/2026-05-16-li-math-linalg-surface.md:170`. | **Open:** full NumPy-rank broadcast; master tracker still lists length-1 as open → reconcile via [lic#386](https://github.com/li-langverse/lic/issues/386) |
| **7d** | **partial — open** | `@vectorized` on `for` → `ArraySimdScope` (#150). Gap harness: `li-tests/tooling/parallel_decorator_policy_capture_gap.sh`, `parallel_decorator_for_elaboration_gap.sh`. Policy skip: `policy_module.cpp:171–203`. | **Open:** MIR proc tags + Lean **G-par** proofs → [lic#387](https://github.com/li-langverse/lic/issues/387) |
| **7e** | **partial — open** | Advisory green: `horner_pure_li`; tests under `li-tests/math_linalg/`. **Red:** `matmul_blocked` 1.55×, `matmul_naive` 1.33× (`ecosystem-audit.json`). | **Open:** tier-1 strict + float Lean Props → [lic#27](https://github.com/li-langverse/lic/issues/27), [lic#49](https://github.com/li-langverse/lic/issues/49) |
| **8p** | **partial — open** | Ninja `-j` C++ only. `--jobs=N` sets `LI_COMPILE_JOBS` (`compiler/lic/main.cpp:161–163`) but frontend/workspace still sequential. | **Open:** 8p-b workspace pool + 8p-d wall-time SLO → [lic#385](https://github.com/li-langverse/lic/issues/385) |
| **Vision-LLM** | **partial — open** | v0: `lic check --format=json`, `lic diagnose`, `diagnostic-v1`, `li-tests/tooling/diagnose_json_smoke.sh`. | **Open:** compact test manifest export, fix-suggest beyond stub → [lic#19](https://github.com/li-langverse/lic/issues/19) |

**Sub-plan gates (sample of 26 open):** P-linalg Lean loop≡closed-form `[ ]` at `plans/2026-05-16-li-math-linalg-surface.md:171` (**G-lean**); tier-1 perf gate `[ ]` line 172; phase-07 HPC decorator/fuzz/tier-1 at `plans/2026-05-14-phase-07-native-hpc.md`.

**Snapshot → registry `plan_debt` map:**

| Runner | `plan_pending` | Registry id | Registry status |
|--------|----------------|-------------|-----------------|
| httpd | `gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk` | `gap-plan-pending-httpd-gap-phase2-*` → deduped canonical rows | **closed** (drift vs snapshot) |
| sim | `sim-p1-num-dot-axpy`, `sim-p1-md-neighbor-cell`, `sim-p2-qm-dft-scf` | `gap-plan-pending-sim-sim-p1-*`, `sim-p2-qm-dft-scf` | **open** |
| sim-md-research | `md-r3-oracle-plan` | `gap-plan-pending-sim-md-research-md-r3-oracle-plan` | **open** |
| sim-chem-research | `chem-r2-dft-scf-gap`, `chem-r3-package-placement` | `gap-plan-pending-sim-chem-research-chem-r2-*`, `chem-r3-*` | **open** |
| security-research | `sec-r1-httpd-fuzz-smoke`, `sec-r2-tier5-gap-exploit`, `sec-r3-runtime-surface` | `gap-plan-pending-security-research-sec-r1-*` … `sec-r3-*` | **open** |

## Provability / G-*

From `lic/docs/verification/provability-gaps.md` (audit: 13 partial, 4 missing):

| Tier | IDs | Master-plan tie-in |
|------|-----|-------------------|
| **Partial (13)** | G-lean, G-vc, G-par, G-dec, G-math, G-bnd, G-def, G-oop, G-math-syn, G-async, G-net, G-trust, G-narrow | PH-2i/7d/7e/2f; P-linalg, P-float, P-par open |
| **Missing (4)** | G-ann, G-gpu, G-meta, G-authz | Deferred / research / OS phase |
| **Blockers** | **G-par:** `@parallel` on plain `for` bypasses capture policy (`parallel_decorator_policy_capture_gap.sh`). **G-math:** tier-1 reds on matmul rows. **G-lean:** `sqrt_open_bound` intentional open (`sqrt_open_bound_contract_tier.sh`). |

**Cross-check `recommended_actions`:** plan audit P1 = close/update 5 tracker rows + sync provability-gaps; ecosystem P0 = fix 34 failing PRs first; P2 = 117 catalog rows without lic paths; P3 = archive 9 stale normative checklists in `phase-02-typechecker.md`.

## Recommended issues

No new issues filed (≤3 cap; existing coverage sufficient). Route through open issues + orchestrator loops:

| Priority | Repo | Issue | Labels | PH / G-* |
|----------|------|-------|--------|----------|
| P1 | lic | [#386](https://github.com/li-langverse/lic/issues/386) | `plan-needed`, `master-plan-gap` | PH-2i — reconcile length-1 broadcast vs tracker/sub-plan |
| P1 | lic | [#387](https://github.com/li-langverse/lic/issues/387) | `plan-needed`, `master-plan-gap` | PH-7d / **G-par** — MIR proc tags + Lean disjoint proofs |
| P1 | lic | [#385](https://github.com/li-langverse/lic/issues/385) | `plan-needed`, `master-plan-gap` | PH-8p — parallel workspace pool + wall-time SLO |

**Runner handoffs (orchestrator loops — not master-plan issues):** httpd → 2 perf gates; sim / sim-md-research / sim-chem-research → algo registry; security-research → tier5 fuzz/exploit surface.

## Deferred

- No plan checkbox edits or gate weakening (evidence-required policy).
- No implementation (`plan-approved` agents only).
- Catalog 117-row P2 sweep → `gap_explorer` / `implementation_gaps`.
- Stale phase-02 normative checklists (9 rows) — doc hygiene only.
- Net-new GitHub issues skipped where #385–387 and runner loops already cover debt.
- Fixing httpd registry dedupe-closed-vs-snapshot-pending → `swarm_observer` ingest logic, not this pass.

**north_star_fit:** domain=governance/plan-honesty · PH=2i,7d,7e,8p,Vision-LLM · pillar=provable (G-* register must not overclaim)
