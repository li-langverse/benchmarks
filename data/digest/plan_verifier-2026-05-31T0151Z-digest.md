# Plan verifier — li-langverse pass (2026-05-31T01:51Z)

**Run:** `heap:coord_governance:plan_verifier:fed3b4b19bafa90f6e8d` · **Preflight:** `plan-completion-audit.py` → `data/latest/plan-completion-audit.json` (166 findings)  
**north_star_fit:** scientific computing / HPC · **PH-2i**, **PH-7d**, **PH-7e**, **PH-8p**, **Vision-LLM** · **G-lean**, **G-par**, **G-dec**, **G-math** · proof → easy → fast

## Executive summary

- **Preflight OK:** `plan-completion-audit.json` at **2026-05-31T01:51Z** — **5** open master-plan tracker rows, **166** total findings (**26** open sub-plan gates, **117** catalog gaps, **31** tracker phases complete).
- **Org CI P1:** `ecosystem-audit.json` (**2026-05-31T01:51Z**) — **1** failed PR (`lic#617` workspace sweep); tier-1 **1** yellow (`matmul_blocked`), **3** near-threshold (`matmul_naive` 1.11×, `simd_dot`, `fft_1d_fixed`).
- **Provability:** **13** partial + **4** missing **G-*** per audit; `provability-gaps.md` **Last updated 2026-05-21** — drift vs broadcast_len1 tests and audit mirror.
- **Swarm ingest:** `lic/scripts/swarm-gap-ingest.py` **not on lic main** (#436); confirmed via `lic-studio-ui/scripts/swarm-gap-ingest.py` — **92** registry gaps, **0** new snapshot rows this pass.
- **Snapshot drift:** **httpd** 10/10 todos completed but **#477** + `plan_debt` rows still open; **studio-ui-ux** pending **studio-ux-21/24** (orchestrator loop); **#575** stale (16/17 done).
- **Issues filed (3):** [#618](https://github.com/li-langverse/lic/issues/618) close stale #462 · [#619](https://github.com/li-langverse/lic/issues/619) httpd reconcile · [benchmarks#266](https://github.com/li-langverse/benchmarks/issues/266) catalog 117 gaps.
- **No implementation** — verification-only; master-plan `[x]` unchanged.

## Tracker review

Open PH / master-plan rows (`lic/docs/superpowers/plans/2026-05-14-li-master-plan.md` **444–473**). **Done** only with cited tests/Lean/scripts.

| Phase | Status | Evidence (file / gate) | Blocker to `[x]` |
|-------|--------|------------------------|------------------|
| **PH-2i** | **partial — open** | `li-tests/math_linalg/broadcast_len1_*.li`, `norm_*.li`, `axpy_float4.li`, `reductions/`; `contracts_verify/linalg_*_closed.li` | Lean witness for length-1 broadcast (#574); full NumPy-rank (#526); close stale #462 ([#618](https://github.com/li-langverse/lic/issues/618)) |
| **PH-7d** | **partial — open** | `decorators/vectorized_for_scope_ok.li`; `parallel_with_disjoint.li`, `parallel_def_disjoint_inherit.li`; `decorator_exploits/` | MIR proc tags; Lean **G-par** / **G-dec** — [#387](https://github.com/li-langverse/lic/issues/387), [#22](https://github.com/li-langverse/lic/issues/22) |
| **PH-7e** | **partial — open** | `scripts/check-tier1-li-vs-cpp.sh`; `math_linalg/matmul_*.li`; yellow `matmul_blocked`, near-threshold `matmul_naive` | Tier-1 strict slices — [#463](https://github.com/li-langverse/lic/issues/463) |
| **PH-8p** | **partial — open** | Ninja `-j` in `scripts/build.sh`; **`LI_TEST_JOBS` not in `run_all.sh`** (8p-a not shipped) | 8p-a parallel `run_all`, 8p-b workspace pool, 8p-c `--jobs` read — [#460](https://github.com/li-langverse/lic/issues/460), [#525](https://github.com/li-langverse/lic/issues/525), [#385](https://github.com/li-langverse/lic/issues/385) |
| **Vision-LLM** | **partial — open** | `li-tests/tooling/diagnose_json_smoke.sh`; `docs/schemas/diagnostic-v1.json`; `scripts/gen-li-agent-manifest.sh` | Manifest + CI export Done gate — [#464](https://github.com/li-langverse/lic/issues/464), [#425](https://github.com/li-langverse/lic/issues/425) |

**Sub-plan gates (26 open):** phase-02 typechecker stale normative rows (9 suppressed as stale_spec); phase-07 HPC tier-1; PH-7e honesty plan; plots/governance. **20** suppressed where tracker phase complete.

### goal-directed-agents `plan_pending` → registry `plan_debt`

| Runner | `plan_pending` | Registry id | Notes |
|--------|----------------|-------------|-------|
| **studio-ui-ux** | `studio-ux-21-wgpu-swapchain-gpu-runner`, `studio-ux-24-gpu-runner-deps` | `gap-plan-pending-studio-ui-ux-studio-ux-21/24-*` | Orchestrator loop active; **#575 stale** (16/17 done) |
| **httpd** | *(none — 10/10 completed)* | stale `gap-plan-pending-httpd-gap-phase2-*` | Reconcile — [#619](https://github.com/li-langverse/lic/issues/619), [#477](https://github.com/li-langverse/lic/issues/477) |
| **compiler-studio** | *(none)* | — | **47/47** completed |
| **sim** | *(none)* | stale sim `plan_debt` rows | [#471](https://github.com/li-langverse/lic/issues/471) ingest reconcile |

### `recommended_actions` cross-check (audit ≡ ecosystem)

| Priority | Action | Plan debt alignment |
|----------|--------|---------------------|
| **P1** | Close/update **5** master-plan tracker rows | Open PH table above |
| **P1** | Update **provability-gaps.md** | **13** partial + **4** missing **G-*** |
| **P2** | **117** catalog path gaps | [benchmarks#266](https://github.com/li-langverse/benchmarks/issues/266), [#179](https://github.com/li-langverse/benchmarks/issues/179) |
| **P3** | Archive stale phase-02 normative checklists | 9 `stale_spec_checklists` |
| **P0** | Org CI | **1** failed PR (`lic#617`) — fix before new plan work |

## Provability / G-*

From `lic/docs/verification/provability-gaps.md` (audit mirror **2026-05-31T01:51Z**):

| Bucket | IDs | Tied PH |
|--------|-----|---------|
| **Partial (13)** | **G-lean**, **G-vc**, **G-par**, **G-dec**, **G-math**, **G-bnd**, **G-oop**, **G-math-syn**, **G-async**, **G-net**, **G-trust**, **G-narrow**, **G-stdlib** | **2f**, **7d**, **7e**, **2i**, **2j** |
| **Missing (4)** | **G-ann**, **G-gpu**, **G-meta**, **G-authz** | Phase **4+**, OS, research |
| **Done** | *(none universal)* | Closed slices inside Partial rows only |

**Hotspots:** **G-par** + **G-dec** → **PH-7d**; **G-math** (broadcast Lean gap, `matmul_blocked` yellow) → **PH-2i** / **PH-7e**; **G-math-syn** (`for`/`range`) → [#527](https://github.com/li-langverse/lic/issues/527).

**Register drift:** doc **Last updated 2026-05-21**; length-1 broadcast compile tests (`broadcast_len1_*.li`) not cited in **G-math** closed slice — [#49](https://github.com/li-langverse/lic/issues/49), [#618](https://github.com/li-langverse/lic/issues/618).

## Recommended issues

1. **[#618](https://github.com/li-langverse/lic/issues/618)** — `[master-plan-gap] PH-2i: close stale #462 — broadcast_len1 compile tests landed (G-math Lean witness still open)` — labels: `master-plan-gap`, `plan-needed`, **PH-2i**, **G-math**.
2. **[#619](https://github.com/li-langverse/lic/issues/619)** — `[master-plan-gap] PH-H httpd: snapshot 10/10 todos completed — reconcile #477 + stale plan_debt rows` — labels: `master-plan-gap`, `plan-needed`, **PH-H**.
3. **[benchmarks#266](https://github.com/li-langverse/benchmarks/issues/266)** — `[master-plan-gap] PH-5b: catalog.toml 117 missing lic paths` — labels: `master-plan-gap`, `plan-needed`, **PH-5b**.

## Deferred

- Implementing PH slices or weakening tier-1 gates (`plan-approved` required).
- Filing duplicate issues for PH-7d, PH-8p, Vision-LLM, studio-ux-21/24 (**387**, **525**, **464**, orchestrator loop already owns GPU runner todos).
- Bulk `ph-db-battle-plan.md` gate implementation or master-plan `[x]` without evidence PRs.
- Restoring `lic/scripts/swarm-gap-ingest.py` on main — tracked **#436**; ran mirror from lic-studio-ui only.
- GitHub Actions `schedule:` cron (forbidden).
