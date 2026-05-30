# Plan verifier — li-langverse pass (2026-05-30T14:21Z)

**Run:** `heap:coord_governance:plan_verifier:fed3b4b19bafa90f6e8d` · **Preflight:** `plan-completion-audit.py` → `data/latest/plan-completion-audit.json` (166 findings)  
**north_star_fit:** scientific computing / HPC · **PH-2i**, **PH-7d**, **PH-7e**, **PH-8p**, **Vision-LLM** · **G-lean**, **G-par**, **G-dec**, **G-math**, **G-math-syn** · proof → easy → fast

## Executive summary

- **Preflight OK:** `plan-completion-audit.json` regenerated at **2026-05-30T14:21Z** — **5** open master-plan tracker rows, **166** total findings (**117** catalog path gaps, **26** open sub-plan gates, **31** tracker phases complete).
- **Ecosystem P0 active:** `ecosystem-audit.json` (**2026-05-30T14:12Z**) lists **34** failed PRs across org — precedes new plan work; briefing snapshot showed **0** failed (stale metrics path).
- **Tier-1 perf:** **2** yellow rows (`matmul_blocked`, `matmul_naive`) — **PH-7e** / **G-math** remain **partial**; advisory ≤1.2× not met on blocked path.
- **Provability:** **13** partial + **4** missing **G-*** per audit; register at `lic/docs/verification/provability-gaps.md` (no **Done** rows yet).
- **Swarm ingest:** `lic/scripts/swarm-gap-ingest.py` ran OK — registry **90** gaps (**55** `plan_debt`); **0** new rows this pass (snapshot + audit already ingested).
- **plan_pending:** **12** todos across **5** runners with active supervisors idle; registry still lists **completed** sim/swarm/httpd-mitigation rows as open `plan_debt` — reconcile via [#471](https://github.com/li-langverse/lic/issues/471).
- **GitHub issues:** **not filed** (coverage exists — see § Recommended issues); **3** highest-signal open issues cited for heap handoff.
- **No implementation** — verification-only; master-plan `[x]` unchanged without evidence PRs.

## Tracker review

Open PH / master-plan rows (`lic/docs/superpowers/plans/2026-05-14-li-master-plan.md` lines **444–473**). **Done** only with cited tests/Lean/scripts.

| Phase | Status | Evidence (file / gate) | Blocker to `[x]` |
|-------|--------|------------------------|------------------|
| **PH-2i** | **partial — open** | `li-tests/math_linalg/` (22 specs): `broadcast_len1_*.li`, `norm_*.li`, `axpy_float4.li`, `reductions/`; `li-tests/tooling/broadcast_len1_codegen_lean_gap.sh` documents Lean gap | Full NumPy-rank broadcast ([#526](https://github.com/li-langverse/lic/issues/526)); **P-linalg** loop ≡ `ensures` gate open in `plans/2026-05-16-li-math-linalg-surface.md` |
| **PH-7d** | **partial — open** | `li-tests/decorators/`; `compiler/mir/lower.cpp` `ArraySimdScope` (#150 7d-c); `parallel_disjoint_lean_opaque_gap.sh` | Full MIR proc tags; Lean **G-par** / **G-dec** ([#387](https://github.com/li-langverse/lic/issues/387)) |
| **PH-7e** | **partial — open** | `scripts/check-tier1-li-vs-cpp.sh`; `CHANGELOG.md` PH-7e slice; ecosystem yellow `matmul_naive` / `matmul_blocked` | Remaining tier-1 slices ([#463](https://github.com/li-langverse/lic/issues/463), [#424](https://github.com/li-langverse/lic/issues/424)) |
| **PH-8p** | **partial — open** | Ninja `-j` on C++ build only; `compiler/lic/main.cpp:161–163` sets `LI_COMPILE_JOBS` from `--jobs=` — **no** `compiler/` consumer | Wire parallel MIR/LLVM; parallel `run_all.sh` ([#525](https://github.com/li-langverse/lic/issues/525)) |
| **Vision-LLM** | **partial — open** | `li-tests/tooling/diagnose_json_smoke.sh`; `docs/schemas/diagnostic-v1.json`; `gen-li-agent-manifest.sh` stub | Manifest + CI export Done gate ([#425](https://github.com/li-langverse/lic/issues/425), [#464](https://github.com/li-langverse/lic/issues/464)) |

**Sub-plan gates (26 open, sample):** phase-02 typechecker (`fib.li`, `bad_*.li`, borrow double-mut); phase-07 HPC tier-1 perf + decorator fuzz; governance/scaffold/package rows — full list in audit `plan_files_open`. **20** checkboxes suppressed where tracker phase complete (e.g. **PH-5b**).

### goal-directed-agents `plan_pending` → registry `plan_debt`

| Runner | `plan_pending` (snapshot) | Registry id | Notes |
|--------|---------------------------|-------------|-------|
| **httpd** | `gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk` | `gap-plan-pending-httpd-gap-phase2-*` | Agent exit **124**, gates failed; [#477](https://github.com/li-langverse/lic/issues/477) |
| **studio-ui-ux** | `studio-ux-16-palette-search-latency`, `studio-ux-17-gpu-fail-recovery` | `gap-plan-pending-studio-ui-ux-studio-ux-16/17-*` | Ingested **2026-05-30**; ux-04…15 **completed** in snapshot but still **open** in registry — **stale** |
| **sim-md-research** | `md-r3-oracle-plan` | `gap-plan-pending-sim-md-research-md-r3-oracle-plan` | [#523](https://github.com/li-langverse/lic/issues/523) |
| **sim-chem-research** | `chem-r2-dft-scf-gap`, `chem-r3-package-placement` | `gap-plan-pending-sim-chem-research-chem-r2/3-*` | [#522](https://github.com/li-langverse/lic/issues/522) |
| **security-research** | `sec-r1-httpd-fuzz-smoke`, `sec-r2-tier5-gap-exploit`, `sec-r3-runtime-surface` | `gap-plan-pending-security-research-sec-r*` | [#521](https://github.com/li-langverse/lic/issues/521) |
| **sim** | *(none)* | `gap-plan-pending-sim-sim-p1-*`, `sim-p2-*` still **open** | Snapshot **completed** — close via [#471](https://github.com/li-langverse/lic/issues/471) |
| **compiler-studio** | *(none)* | — | Loop backlog clear |
| **swarm-observer** | *(none)* | `orch-r0`…`orch-r4` still **open** | All **completed** in snapshot — **stale** |
| **ph-db** | *(not in snapshot)* | `gap-plan-pending-ph-db-wp-*` (9 rows) | Registry drift — runner absent from snapshot; [#423](https://github.com/li-langverse/lic/issues/423) |

### `recommended_actions` cross-check (audit ≡ ecosystem)

| Priority | Action | Plan debt alignment |
|----------|--------|---------------------|
| **P0** (ecosystem only) | Fix **34** failing PR CIs | Blocks feature work per skill; not in plan audit JSON |
| **P1** | Close/update **5** master-plan tracker rows | Maps open PH rows above |
| **P1** | Update **provability-gaps.md** with compiler closes | **13** partial + **4** missing **G-*** |
| **P2** | **117** catalog paths missing under `lic/benchmarks/` | **PH-5b** catalog honesty — aspirational rows |
| **P3** | Archive **9** stale normative checklists (`phase-02-typechecker.md`) | Doc hygiene only |

## Provability / G-*

From `lic/docs/verification/provability-gaps.md` (audit mirror **2026-05-30T14:21Z**):

| Bucket | IDs | Tied PH |
|--------|-----|---------|
| **Partial (13)** | **G-lean**, **G-vc**, **G-par**, **G-stdlib**, **G-dec**, **G-math**, **G-bnd**, **G-oop**, **G-math-syn**, **G-async**, **G-net**, **G-trust**, **G-narrow** | **2f**, **7d**, **7e**, **2i**, **2j**, **H** |
| **Missing (4)** | **G-ann**, **G-gpu**, **G-meta**, **G-authz** | Phase **4+**, OS, research |
| **Axiomatic / social** | **G-hw**, **G-wrong-spec** | Documented limits |

**Active session hotspots:** **G-par** + **G-dec** block **PH-7d**; **G-math** + **G-lean** (`sqrt_open_bound`, loop ≡ closed form — [#17](https://github.com/li-langverse/lic/issues/17)) block **PH-2i** / **PH-7e**; **G-math-syn** (`for`/`range`) — [#527](https://github.com/li-langverse/lic/issues/527).

## Recommended issues

**No new issues filed** — existing `plan-needed` / `master-plan-gap` coverage is sufficient. Handoff to heap / `swarm_observer`:

1. **[#477](https://github.com/li-langverse/lic/issues/477)** — `[master-plan-gap] PH-H httpd: gap-phase2-perf-wrk-soak + gap-phase2-streaming-wrk pending` — labels: `master-plan-gap`, `PH-H` — supervisor stale, exit **124**.
2. **[#471](https://github.com/li-langverse/lic/issues/471)** — `[master-plan-gap] swarm-gap-ingest: close plan_debt when todo.status=completed` — labels: `master-plan-gap`, `plan-needed` — registry drift (sim, swarm-observer, studio-ux-04…15).
3. **[#463](https://github.com/li-langverse/lic/issues/463)** — `[master-plan-gap] PH-7e: tier-1 red/yellow benchmarks vs 1.2× advisory` — labels: `PH-7e`, `G-math` — evidence: ecosystem yellow `matmul_*`, `docs/numerics/studies/2026-05-30-matmul-blocked-7e.md`.

## Deferred

- **Implementing** PH slices or weakening tier-1 gates (`plan-approved` required).
- **Filing duplicate issues** for PH-7d, PH-8p, Vision-LLM, G-lean (issues **387**, **525**, **425**, **17** already open).
- **Bulk catalog implementation** (**117** paths) or checking master-plan `[x]` without evidence PRs.
- **Closing stale registry rows** programmatically — needs `swarm_observer` + [#471](https://github.com/li-langverse/lic/issues/471) ingest rule.
- **Git commit/push** of audit JSON / this digest (operational artifacts).
