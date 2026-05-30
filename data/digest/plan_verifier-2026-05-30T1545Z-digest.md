# Plan verifier — li-langverse pass (2026-05-30T15:45Z)

**Run:** `heap:coord_governance:plan_verifier:fed3b4b19bafa90f6e8d` · **Preflight:** `plan-completion-audit.py` → `data/latest/plan-completion-audit.json` (166 findings)  
**north_star_fit:** scientific computing / HPC · **PH-2i**, **PH-7d**, **PH-7e**, **PH-8p**, **Vision-LLM** · **G-lean**, **G-par**, **G-dec**, **G-math**, **G-math-syn** · proof → easy → fast

## Executive summary

- **Preflight OK:** `plan-completion-audit.json` at **2026-05-30T15:45Z** — **5** open master-plan tracker rows, **166** total findings (**117** catalog path gaps, **26** open sub-plan gates, **31** tracker phases complete).
- **Org CI P0 clear:** `ecosystem-audit.json` (**2026-05-30T15:43Z**) reports **0** failed PRs, **0** repos missing CI on main — no P0 block before plan work.
- **Tier-1 perf:** **1** yellow row (`matmul_blocked`); **3** near-threshold (`matmul_naive` 1.11×, `simd_dot` 1.04×, `fft_1d_fixed` 1.01× vs cpp) — **PH-7e** / **G-math** remain **partial**.
- **Provability:** **13** partial + **4** missing **G-***; no **Done** rows in `provability-gaps.md` (last updated 2026-05-21).
- **Swarm ingest:** `lic/scripts/swarm-gap-ingest.py` OK — **90** registry gaps (**55** `plan_debt`, **30** `competitor_feature`, **5** `missing_package`); **0** new rows this pass.
- **Registry drift:** `httpd` `plan_pending` (2 todos, exit **124**) but canonical `gap-plan-pending-httpd-gap-phase2-*` rows **closed**; `sim` / `swarm-observer` completed todos still **open** `plan_debt` — handoff **#471**.
- **GitHub issues:** **not filed** (API rate limit exceeded); cite existing issues below.
- **No implementation** — verification-only; master-plan `[x]` unchanged.

## Tracker review

Open PH / master-plan rows (`lic/docs/superpowers/plans/2026-05-14-li-master-plan.md` **444–473**). **Done** only with cited tests/Lean/scripts.

| Phase | Status | Evidence (file / gate) | Blocker to `[x]` |
|-------|--------|------------------------|------------------|
| **PH-2i** | **partial — open** | `li-tests/math_linalg/` (25 specs): `broadcast_len1_*.li`, `norm_*.li`, `axpy_float4.li`, `reductions/`; `mat2_at2_codegen_probe.li` | Full NumPy-rank broadcast; **P-linalg** loop ≡ `ensures` (**G-lean** / **G-math**) — [#526](https://github.com/li-langverse/lic/issues/526) |
| **PH-7d** | **partial — open** | `li-tests/decorators/vectorized_for_scope_ok.li`; `ArraySimdScope` in `compiler/mir/lower.cpp:2043`; `parallel_disjoint_lean_opaque_gap.sh` | MIR proc tags; Lean **G-par** / **G-dec** — [#387](https://github.com/li-langverse/lic/issues/387) |
| **PH-7e** | **partial — open** | `scripts/check-tier1-li-vs-cpp.sh`; `li-tests/math_linalg/matmul_*.li`; yellow `matmul_blocked`, near-threshold `matmul_naive` | Remaining tier-1 slices — [#463](https://github.com/li-langverse/lic/issues/463), [#424](https://github.com/li-langverse/lic/issues/424) |
| **PH-8p** | **partial — open** | Ninja `-j` on C++ only; `compiler/lic/main.cpp:161–163` sets `LI_COMPILE_JOBS` — **no** `compiler/` consumer; `li-tests/run_all.sh` has **no** `LI_TEST_JOBS` / `-j` | **8p-a** parallel `run_all` + isolated builds; wire `--jobs` — [#525](https://github.com/li-langverse/lic/issues/525) |
| **Vision-LLM** | **partial — open** | `li-tests/tooling/diagnose_json_smoke.sh`; `docs/schemas/diagnostic-v1.json`; `gen-li-agent-manifest.sh` stub | Manifest + CI export Done gate — [#425](https://github.com/li-langverse/lic/issues/425), [#464](https://github.com/li-langverse/lic/issues/464) |

**Sub-plan gates (26 open):** phase-02 typechecker (`fib.li`, `bad_*.li`, borrow); phase-07 HPC tier-1 + decorator fuzz; governance/scaffold/package rows — see audit `plan_files_open`. **20** suppressed where tracker phase complete.

### goal-directed-agents `plan_pending` → registry `plan_debt`

| Runner | `plan_pending` (snapshot) | Registry id | Notes |
|--------|---------------------------|-------------|-------|
| **httpd** | `gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk` | `gap-plan-pending-httpd-gap-phase2-*` (**closed**) | Exit **124**, gates failed; scripts exist (`check-tier5-perf-wrk-soak.sh`, `check-tier5-streaming-soak.sh`); **reopen** ingest gap — [#477](https://github.com/li-langverse/lic/issues/477) |
| **studio-ui-ux** | `studio-ux-16-palette-search-latency`, `studio-ux-17-gpu-fail-recovery` | `gap-plan-pending-studio-ui-ux-studio-ux-16/17-*` (**open**) | ux-04…15 completed in snapshot; older ux rows **stale open** |
| **sim-md-research** | `md-r3-oracle-plan` | `gap-plan-pending-sim-md-research-md-r3-oracle-plan` (**open**) | [#523](https://github.com/li-langverse/lic/issues/523) |
| **sim-chem-research** | `chem-r2-dft-scf-gap`, `chem-r3-package-placement` | `gap-plan-pending-sim-chem-research-chem-r2/3-*` (**open**) | [#522](https://github.com/li-langverse/lic/issues/522) |
| **security-research** | `sec-r1-httpd-fuzz-smoke`, `sec-r2-tier5-gap-exploit`, `sec-r3-runtime-surface` | `gap-plan-pending-security-research-sec-r*` (**open**) | [#521](https://github.com/li-langverse/lic/issues/521) |
| **sim** | *(none)* | `gap-plan-pending-sim-sim-p1-*`, `sim-p2-*` (**open**) | All todos **completed** — stale |
| **swarm-observer** | *(none)* | `orch-r3`, `orch-r4` (**open**) | Todos **completed** — stale |
| **ph-db** | *(absent from snapshot)* | `gap-plan-pending-ph-db-wp-*` (9 rows) | Orphan registry — [#423](https://github.com/li-langverse/lic/issues/423) |

### `recommended_actions` cross-check (audit ≡ ecosystem)

| Priority | Action | Plan debt alignment |
|----------|--------|---------------------|
| **P1** | Close/update **5** master-plan tracker rows | Open PH table above |
| **P1** | Update **provability-gaps.md** with compiler closes | **13** partial + **4** missing **G-*** |
| **P2** | **117** catalog paths missing under `lic/benchmarks/` | Catalog honesty — aspirational rows |
| **P3** | Archive **9** stale normative checklists (`phase-02-typechecker.md`) | Doc hygiene only |

## Provability / G-*

From `lic/docs/verification/provability-gaps.md` (audit mirror **2026-05-30T15:45Z**):

| Bucket | IDs | Tied PH |
|--------|-----|---------|
| **Partial (13)** | **G-lean**, **G-vc**, **G-par**, **G-stdlib**, **G-dec**, **G-math**, **G-bnd**, **G-oop**, **G-math-syn**, **G-async**, **G-net**, **G-trust**, **G-narrow** | **2f**, **7d**, **7e**, **2i**, **2j**, **H** |
| **Missing (4)** | **G-ann**, **G-gpu**, **G-meta**, **G-authz** | Phase **4+**, OS, research |
| **Axiomatic / social** | **G-hw**, **G-wrong-spec** | Documented limits |

**Hotspots:** **G-par** + **G-dec** → **PH-7d**; **G-math** + **G-lean** (`sqrt_open_bound`, P-linalg loop witness) → **PH-2i** / **PH-7e**; **G-math-syn** (`for`/`range`) → [#527](https://github.com/li-langverse/lic/issues/527).

## Recommended issues

**No new issues filed** — `gh` API rate limit exceeded. Existing coverage for heap / `swarm_observer`:

1. **[#477](https://github.com/li-langverse/lic/issues/477)** — `[master-plan-gap] PH-H httpd: gap-phase2-perf-wrk-soak + gap-phase2-streaming-wrk pending` — labels: `master-plan-gap`, `PH-H`.
2. **[#471](https://github.com/li-langverse/lic/issues/471)** — `[master-plan-gap] swarm-gap-ingest: close plan_debt when todo.status=completed; reopen when plan_pending` — labels: `master-plan-gap`, `plan-needed`.
3. **[#463](https://github.com/li-langverse/lic/issues/463)** — `[master-plan-gap] PH-7e: tier-1 yellow matmul_* vs 1.2× advisory` — labels: `PH-7e`, `G-math`.

## Deferred

- Implementing PH slices or weakening tier-1 gates (`plan-approved` required).
- Filing duplicate issues for PH-7d, PH-8p, Vision-LLM, G-lean (**387**, **525**, **425**, **17** already open).
- Bulk catalog implementation (**117** paths) or master-plan `[x]` without evidence PRs.
- Programmatic registry reconcile — needs `swarm_observer` + [#471](https://github.com/li-langverse/lic/issues/471).
- GitHub Actions `schedule:` cron (forbidden).
