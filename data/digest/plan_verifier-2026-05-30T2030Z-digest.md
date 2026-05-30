# Plan verifier — li-langverse pass (2026-05-30T20:30Z)

**Run:** `heap:coord_governance:plan_verifier:fed3b4b19bafa90f6e8d` · **Preflight:** `plan-completion-audit.py` → `data/latest/plan-completion-audit.json` (65 findings)  
**north_star_fit:** scientific computing / HPC · **PH-2i**, **PH-7d**, **PH-7e**, **PH-8p**, **Vision-LLM**, **PH-DB** · **G-lean**, **G-par**, **G-dec**, **G-math** · proof → easy → fast

## Executive summary

- **Preflight OK:** `plan-completion-audit.json` at **2026-05-30T20:30Z** — **5** open master-plan tracker rows, **65** total findings (**40** open sub-plan gates, **0** catalog gaps, **31** tracker phases complete).
- **Org CI P0 clear:** `ecosystem-audit.json` (**2026-05-30T20:29Z**) — **0** failed PRs, **0** repos missing CI on main; tier-1 **1** yellow (`matmul_blocked`), **3** near-threshold rows.
- **Provability:** **16** partial + **3** missing **G-*** per audit mirror; `provability-gaps.md` last updated **2026-05-30** — no universal **Done** rows.
- **Swarm ingest:** `lic/scripts/swarm-gap-ingest.py` OK — **90** registry gaps (**55** `plan_debt`, **30** `competitor_feature`, **5** `missing_package`); **0** new rows this pass.
- **Registry drift:** `sim` / `swarm-observer` completed todos still **open** `plan_debt`; `httpd` pending todos map to duplicate deduped rows — handoff **#471**.
- **Issues filed (3):** [#574](https://github.com/li-langverse/lic/issues/574) PH-2i broadcast Lean gap · [#575](https://github.com/li-langverse/lic/issues/575) studio-ux-16/17 · [#576](https://github.com/li-langverse/lic/issues/576) PH-DB runner wp-* backlog.
- **No implementation** — verification-only; master-plan `[x]` unchanged.

## Tracker review

Open PH / master-plan rows (`lic/docs/superpowers/plans/2026-05-14-li-master-plan.md` **447–476**). **Done** only with cited tests/Lean/scripts.

| Phase | Status | Evidence (file / gate) | Blocker to `[x]` |
|-------|--------|------------------------|------------------|
| **PH-2i** | **partial — open** | `li-tests/math_linalg/broadcast_len1_*.li`, `norm_*.li`, `axpy_float4.li`, `reductions/` (manifest **447–1075**); `contracts_verify/linalg_norm4_int_closed.li`, `linalg_axpy4_int_closed.li` | Full NumPy-rank broadcast; length-1 **Lean** witness open — [#526](https://github.com/li-langverse/lic/issues/526), [#574](https://github.com/li-langverse/lic/issues/574) |
| **PH-7d** | **partial — open** | `decorators/vectorized_for_scope_ok.li`; `parallel_with_disjoint.li`, `parallel_def_disjoint_inherit.li`; `decorator_exploits/` compile_fail suite | MIR proc tags; Lean **G-par** / **G-dec** proofs — [#387](https://github.com/li-langverse/lic/issues/387), [#22](https://github.com/li-langverse/lic/issues/22) |
| **PH-7e** | **partial — open** | `scripts/check-tier1-li-vs-cpp.sh`; `math_linalg/matmul_*.li`; yellow `matmul_blocked`, near-threshold `matmul_naive` (1.11×) | Remaining tier-1 strict slices — [#463](https://github.com/li-langverse/lic/issues/463) |
| **PH-8p** | **partial — open** | **8p-a wired:** `li-tests/run_all.sh` `LI_TEST_JOBS` + `run_all_parallel_smoke.sh`; **8p-c reserved:** `resource_flags_smoke.sh` sets `LI_COMPILE_JOBS=99` with warn-only | **8p-b** workspace pool; **8p-c** compiler reads jobs — [#525](https://github.com/li-langverse/lic/issues/525), [#385](https://github.com/li-langverse/lic/issues/385) |
| **Vision-LLM** | **partial — open** | `li-tests/tooling/diagnose_json_smoke.sh`; `docs/schemas/diagnostic-v1.json` | Manifest + CI export Done gate — [#464](https://github.com/li-langverse/lic/issues/464) |

**Sub-plan gates (40 open):** dominated by `ph-db-battle-plan.md` (**28** rows); phase-07 HPC tier-1 + PH-7e honesty plan; plots/governance rows — see audit `plan_files_open`. **10** suppressed where tracker phase complete.

### goal-directed-agents `plan_pending` → registry `plan_debt`

| Runner | `plan_pending` | Registry id | Notes |
|--------|----------------|-------------|-------|
| **httpd** | `gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk` | `gap-plan-pending-httpd-gap-phase2-*` (+ deduped variants) | Exit **124**; gates exist — [#477](https://github.com/li-langverse/lic/issues/477) |
| **studio-ui-ux** | `studio-ux-16-palette-search-latency`, `studio-ux-17-gpu-fail-recovery` | `gap-plan-pending-studio-ui-ux-studio-ux-16/17-*` | Supervisor stopped — [#575](https://github.com/li-langverse/lic/issues/575) |
| **sim-md-research** | `md-r3-oracle-plan` | `gap-plan-pending-sim-md-research-md-r3-oracle-plan` | [#523](https://github.com/li-langverse/lic/issues/523) |
| **sim-chem-research** | `chem-r2-dft-scf-gap`, `chem-r3-package-placement` | `gap-plan-pending-sim-chem-research-chem-r2/3-*` | [#522](https://github.com/li-langverse/lic/issues/522) |
| **security-research** | `sec-r1/2/3-*` | `gap-plan-pending-security-research-sec-r*` | [#521](https://github.com/li-langverse/lic/issues/521) |
| **ph-db** | 9× `wp-*` todos | `gap-plan-pending-ph-db-wp-*` (9 rows) | No YAML plan-loop — [#576](https://github.com/li-langverse/lic/issues/576), [#423](https://github.com/li-langverse/lic/issues/423) |
| **compiler-studio** | *(none)* | — | **18/18** completed |
| **sim** / **swarm-observer** | *(none)* | stale `plan_debt` rows | [#471](https://github.com/li-langverse/lic/issues/471) |

### `recommended_actions` cross-check (audit ≡ ecosystem)

| Priority | Action | Plan debt alignment |
|----------|--------|---------------------|
| **P1** | Close/update **5** master-plan tracker rows | Open PH table above |
| **P1** | Update **provability-gaps.md** when closing compiler work | **16** partial + **3** missing **G-*** |
| **P0** | Org CI | **Clear** — 0 failed PRs |

## Provability / G-*

From `lic/docs/verification/provability-gaps.md` (audit mirror **2026-05-30T20:30Z**):

| Bucket | IDs | Tied PH |
|--------|-----|---------|
| **Partial (16)** | **G-lean**, **G-vc**, **G-par**, **G-dec**, **G-math**, **G-bnd**, **G-oop**, **G-math-syn**, **G-gpu**, **G-async**, **G-net**, **G-narrow**, **G-proof-db**, **G-physics**, **G-erdos**, **G-stdlib** | **2f**, **7d**, **7e**, **2i**, **2j**, **Doc** |
| **Missing (3)** | **G-ann**, **G-meta**, **G-authz** | Phase **4+**, OS, research |
| **Done** | **G-test-verify** | manifest `prove_lean_ok` |

**Hotspots:** **G-par** + **G-dec** → **PH-7d**; **G-math** (broadcast Lean gap, tier-1 yellow) → **PH-2i** / **PH-7e**; **G-math-syn** → [#527](https://github.com/li-langverse/lic/issues/527).

## Recommended issues

1. **[#574](https://github.com/li-langverse/lic/issues/574)** — `[master-plan-gap] PH-2i / G-math: length-1 broadcast — MIR codegen without Lean witness` — labels: `master-plan-gap`, `plan-needed`, **PH-2i**, **G-math**.
2. **[#575](https://github.com/li-langverse/lic/issues/575)** — `[master-plan-gap] studio-ui-ux: studio-ux-16/17 pending — palette latency + GPU fail recovery` — labels: `master-plan-gap`, `plan-needed`.
3. **[#576](https://github.com/li-langverse/lic/issues/576)** — `[master-plan-gap] PH-DB: ph-db runner — 9 wp-* todos pending, no plan-loop YAML` — labels: `master-plan-gap`, `plan-needed`, **PH-DB**.

## Deferred

- Implementing PH slices or weakening tier-1 gates (`plan-approved` required).
- Filing duplicate issues for PH-7d, PH-8p, Vision-LLM, httpd soak (**387**, **525**, **464**, **477** already open).
- Bulk `ph-db-battle-plan.md` gate implementation or master-plan `[x]` without evidence PRs.
- Programmatic registry reconcile for stale `plan_debt` — needs `swarm_observer` + [#471](https://github.com/li-langverse/lic/issues/471).
- GitHub Actions `schedule:` cron (forbidden).
