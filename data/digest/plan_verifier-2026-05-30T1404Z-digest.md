# Plan verifier — li-langverse pass (2026-05-30T14:04Z)

**Run:** `heap:coord_governance:plan_verifier:fed3b4b19bafa90f6e8d` · **Preflight:** `plan-completion-audit.py` → `data/latest/plan-completion-audit.json` (166 findings)  
**north_star_fit:** scientific computing / HPC · **PH-2i**, **PH-7d**, **PH-7e**, **PH-8p**, **Vision-LLM** · **G-lean**, **G-par**, **G-dec**, **G-math**, **G-math-syn** · proof → easy → fast

## Executive summary

- **Preflight OK:** `plan-completion-audit.json` regenerated at **2026-05-30T14:04Z** — **5** open master-plan tracker rows, **166** total findings (**117** catalog path gaps, **26** open sub-plan gates).
- **Org CI green:** ecosystem audit **2026-05-30T14:01Z** — **0** failed PRs, **0** repos missing CI on main; **P0** not blocking plan work.
- **Tier-1 perf:** **2** yellow rows (`matmul_blocked`, `matmul_naive`) — **PH-7e** / **G-math** remain **partial**; not red but above 1.2× advisory without strict gate.
- **Provability:** **13** partial + **4** missing **G-*** rows per audit; register unchanged in substance ([provability-gaps.md](../lic/docs/verification/provability-gaps.md)).
- **Swarm ingest:** `lic/scripts/swarm-gap-ingest.py` ran OK — registry **90** gaps (**55** `plan_debt`); **0** new snapshot rows (registry already ingested).
- **plan_pending drift:** snapshot shows **12** pending todos across **5** runners; registry still lists **completed** sim/studio/swarm todos as open `plan_debt` — orchestrator should reconcile statuses, not re-open loops.
- **GitHub issues:** **not filed** — `gh` GraphQL rate limit exceeded; three draft issues below for human or retry.
- **No implementation** — verification-only pass; master-plan checkboxes stay open until evidence PRs land.

## Tracker review

Open PH / master-plan rows (`lic/docs/superpowers/plans/2026-05-14-li-master-plan.md` lines **444–473**). **Done** only with cited tests/Lean/scripts.

| Phase | Status | Evidence (file / gate) | Blocker to `[x]` |
|-------|--------|------------------------|------------------|
| **PH-2i** | **partial — open** | `li-tests/math_linalg/` (24 specs): `broadcast_len1_*.li`, `norm_*.li`, `axpy_float4.li`, `reductions/`, `matmul_*.li`; plan gate **P-linalg loop ≡ ensures** still `- [ ]` in `plans/2026-05-16-li-math-linalg-surface.md` | Full NumPy-rank broadcast; float `@` trusted vs MIR per **G-math** |
| **PH-7d** | **partial — open** | `li-tests/decorators/` + `manifest.toml` suites; `vectorized_for_parse_ok.li`; `parallel_disjoint_lean_opaque_gap.sh` documents **G-par** stubs | Full MIR proc tags; Lean **G-par** / **G-dec** proofs |
| **PH-7e** | **partial — open** | `scripts/check-tier1-li-vs-cpp.sh`; `CHANGELOG.md` PH-7e slice; ecosystem **yellow** `matmul_naive` / `matmul_blocked` | Remaining tier-1 slices; strict optional gate not default green |
| **PH-8p** | **partial — open** | `compiler/lic/main.cpp:161–163` sets `LI_COMPILE_JOBS` from `--jobs=`; **no** `compiler/` consumer of env var | Wire jobs to parallel MIR/LLVM; parallel `run_all.sh` / workspace |
| **Vision-LLM** | **partial — open** | `li-tests/tooling/diagnose_json_smoke.sh`; `docs/schemas/diagnostic-v1.json`; `gen-li-agent-manifest.sh` | Full manifest + agent-handover completion per spec |

**Sub-plan gates (26 open, sample):** phase-02 typechecker (`fib.li`, `bad_*.li`), phase-07 HPC tier-1 perf, governance/scaffold/package rows — see audit `plan_files_open`. **20** checkboxes suppressed where tracker phase marked complete (e.g. **PH-5b** benchmark plan).

### goal-directed-agents `plan_pending` → registry `plan_debt`

| Runner | `plan_pending` (snapshot) | Registry id pattern | Notes |
|--------|---------------------------|---------------------|-------|
| **httpd** | `gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk` | `gap-plan-pending-httpd-gap-phase2-*` | Agent exit **124**, gates failed; supervisor idle |
| **studio-ui-ux** | `studio-ux-16-palette-search-latency`, `studio-ux-17-gpu-fail-recovery` | `gap-plan-pending-studio-ui-ux-studio-ux-16/17-*` | Ingest added **2026-05-30**; prior ux-04…15 still **open** in registry but **completed** in snapshot — **stale** |
| **sim-md-research** | `md-r3-oracle-plan` | `gap-plan-pending-sim-md-research-md-r3-oracle-plan` | Research doc handoff |
| **sim-chem-research** | `chem-r2-dft-scf-gap`, `chem-r3-package-placement` | `gap-plan-pending-sim-chem-research-chem-r2/3-*` | chem-r2 gates failed once |
| **security-research** | `sec-r1`…`sec-r3` | `gap-plan-pending-security-research-sec-r*` | Supervisors off |
| **sim** | *(none)* | Registry still has `sim-p1-*`, `sim-p2-*` | Snapshot **completed** — close registry rows |
| **compiler-studio** | *(none)* | — | Loop backlog clear |
| **swarm-observer** | *(none)* | Registry has `orch-r0`…`orch-r4` open | All **completed** in snapshot — **stale** |

### recommended_actions cross-check (audit ≡ ecosystem)

| Priority | Action | Plan debt alignment |
|----------|--------|---------------------|
| **P1** | Close/update **5** master-plan tracker rows | Directly maps open PH rows above |
| **P1** | Update **provability-gaps.md** with compiler closes | **G-*** partial/missing counts |
| **P2** | **117** catalog paths missing under `lic/benchmarks/` | **PH-5b** catalog honesty — not tracker-complete |
| **P3** | Archive **9** stale normative checklists (`phase-02-typechecker.md`) | Doc hygiene only |

## Provability / G-*

From `lic/docs/verification/provability-gaps.md` (audit mirror **2026-05-30T14:04Z**):

| Bucket | IDs | Tied PH |
|--------|-----|---------|
| **Partial (13)** | **G-lean**, **G-vc**, **G-par**, **G-stdlib**, **G-dec**, **G-math**, **G-bnd**, **G-oop**, **G-math-syn**, **G-async**, **G-net**, **G-trust**, **G-narrow** | **2f**, **7d**, **7e**, **2i**, **2j**, **H** |
| **Missing (4)** | **G-ann**, **G-gpu**, **G-meta**, **G-authz** | Phase **4+**, OS, research |
| **Axiomatic / social** | **G-hw**, **G-wrong-spec** | Documented limits |

**Active session hotspots:** **G-par** + **G-dec** block **PH-7d**; **G-math** + **G-lean** (**sqrt_open_bound**, loop ≡ closed form) block **PH-2i** / **PH-7e**; **G-math-syn** (`for`/`range`) linked to deferred **PH-2h** work.

## Recommended issues

**GitHub filing skipped** (rate limit). Draft for `li-langverse/lic`:

1. **`[master-plan-gap] PH-7e: tier-1 matmul yellow — loop SIMD / blocked tile plan`** — labels: `master-plan-gap`, `PH-7e`, `G-math` — scope: `bench_improver` + `numerics_researcher`; evidence: ecosystem yellow rows, `docs/numerics/studies/2026-05-30-matmul-blocked-7e.md`.
2. **`[plan-needed] PH-8p-c: wire LI_COMPILE_JOBS to parallel compile passes`** — labels: `plan-needed`, `PH-8p` — scope: `code_implementer` after plan PR; evidence: `main.cpp` sets env only; `plans/2026-05-22-parallel-compile-ci.md`.
3. **`[master-plan-gap] PH-7d: decorator MIR tags + G-par Lean discharge`** — labels: `master-plan-gap`, `PH-7d`, `G-par`, `G-dec` — scope: `proof_gap_researcher` + compiler; evidence: `parallel_disjoint_lean_opaque_gap.sh`, open tracker row line **454**.

## Deferred

- **Implementing** PH slices or weakening tier-1 gates (`plan-approved` required).
- **Filing >3 issues** or bulk catalog row implementation (**117** paths).
- **Checking off** master-plan `[x]` without same-PR evidence.
- **Closing stale registry `plan_debt`** rows programmatically (needs `swarm_observer` apply-actions or ingest rule for `snapshot_completed`).
- **Git commit/push** of audit JSON from this pass (operational artifact; user can batch with next agent digest PR).
