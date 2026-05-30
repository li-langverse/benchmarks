# Plan verifier digest — 2026-05-30T14:55Z

**Preflight:** `benchmarks/data/latest/plan-completion-audit.json` at `2026-05-30T14:55Z` (166 findings).  
**Swarm ingest:** `lic/scripts/swarm-gap-ingest.py` exit 0 — registry **90** gaps (55 `plan_debt`, 30 `competitor_feature`, 5 `missing_package`); 0 rows added this pass.  
**north_star_fit:** governance · PH-2i, PH-7d, PH-7e, PH-8p, Vision-LLM · G-math, G-par, G-dec, G-lean

## Executive summary

- **5** master-plan tracker rows remain unchecked (2i, 7d, 7e, 8p, Vision-LLM); **31** phases complete; audit totals **166** findings (`open_tracker_items: 5`, `open_plan_checkboxes: 26`, `catalog_gaps: 117`).
- **PH-2i:** length-1 broadcast lowers in MIR/codegen (`broadcast_len1_*` compile_ok in `manifest.toml`); Lean semantics intentionally absent (`broadcast_len1_codegen_lean_gap.sh`); full NumPy-rank broadcast still open — tracker correctly **partial**.
- **PH-7e / G-math:** ecosystem audit flags **yellow** tier-1 rows `matmul_blocked`, `matmul_naive` (>1.2× C++); `horner_pure_li` near threshold (1.0066×); strict gate optional via `LI_TIER1_PERF_STRICT`.
- **PH-7d / G-par / G-dec:** `@vectorized` → `ArraySimdScope` done (#150); **G-par** Lean disjoint proofs still opaque stubs (`parallel_disjoint_lean_opaque_gap.sh`); full MIR proc tags open.
- **PH-8p:** `--jobs=N` parses to `LI_COMPILE_JOBS` only (`compiler/lic/main.cpp:161-163`); no compiler consumer; `run_all.sh` / workspace remain sequential.
- **Provability:** **13 Partial + 4 Missing G-*** per audit; register last updated 2026-05-21 — none marked **Done**; handbook must not overclaim.
- **Goal-directed agents:** **10** `plan_pending` todos across **5** runners; registry drift: **3** stale `sim` rows still **open** though snapshot `plan_pending=[]`; httpd wrk-soak rows **closed** in registry but still **pending** in snapshot (exit 124, supervisor stale).
- **Ecosystem P0:** `ecosystem-audit.json` (`2026-05-30T14:52Z`) reports **39** failed PRs — precedes new master-plan closure work per audit priority table.

## Tracker review

| Phase | Master plan cite | Verdict | Evidence |
|-------|------------------|---------|----------|
| **2i** | `lic/docs/superpowers/plans/2026-05-14-li-master-plan.md:444` | **Open (partial)** | **Slice done:** `math_linalg/norm_float4.li`, `reductions/`, `broadcast_len1_add_float4.li`, `broadcast_len1_mul_int4.li` (`li-tests/manifest.toml:825-830,868`); sub-plan 2i-b checked. **Open:** NumPy-rank broadcast; P-linalg loop≡ensures gate (`2026-05-16-li-math-linalg-surface.md` unchecked **G-lean** row). |
| **7d** | `:454` | **Open (partial)** | **Slice done:** `decorators/vectorized_for_scope_ok.li`, `parallel_def_disjoint_inherit.li` (#150 7d-c). **Open:** MIR proc tags, **G-par** Lean proofs (`parallel_disjoint_lean_opaque_gap.sh`); phase-07 gate “Tier 2 MD `@` on `def`” unchecked. |
| **7e** | `:455` | **Open (partial)** | **Slice done:** loop matmul + FMA horner; `check-tier1-li-vs-cpp.sh` advisory. **Open:** `matmul_naive` / `matmul_blocked` yellow in ecosystem audit; full float Lean Props (`sqrt_open_bound`, matmul Props). |
| **8p** | `:467` | **Open (partial)** | Ninja `-j` for C++ (`scripts/build.sh` reads `LI_BUILD_JOBS`). **Open:** parallel `run_all.sh`, workspace batching, `lic --jobs` consumer. |
| **Vision-LLM** | `:473` | **Open (partial)** | **Slice done:** `lic check --format=json`, `lic diagnose` (`main.cpp:479-496`), `diagnose_json_smoke.sh`, `diagnostic-v1` schema stub. **Open:** manifest ship gate, full agent-handover completion. |

**Sub-plan exit gates (26 open, not PH tracker):** phase-02 typechecker (3 gates — no `fib.li` / `bad_*` manifest rows found); phase-07 HPC (3); plots-and-social (4); ecosystem-governance (7); math-linalg **P-linalg** (**G-lean**); package-scaffold (7).

**Mark `[x]` only with tests/Lean cite:** none of the five tracker rows qualify for full closure.

### `plan_pending` → registry `plan_debt`

| Runner | `plan_pending` | Registry id | Registry status | Notes |
|--------|----------------|-------------|-----------------|-------|
| httpd | `gap-phase2-perf-wrk-soak` | `gap-plan-pending-httpd-gap-httpd-gap-httpd-gap-phase2-perf-wrk-soak` | **closed** | Snapshot still **pending**; agent exit **124** @ 2026-05-30T05:51Z — orchestrator loop applies |
| httpd | `gap-phase2-streaming-wrk` | `gap-plan-pending-httpd-gap-httpd-gap-httpd-gap-phase2-streaming-wrk` | **closed** | Snapshot still **pending**; exit **124** @ 06:38Z |
| studio-ui-ux | `studio-ux-16-palette-search-latency` | `gap-plan-pending-studio-ui-ux-studio-ux-16-palette-search-latency` | **open** | Supervisor off; `active_todo_id` set |
| studio-ui-ux | `studio-ux-17-gpu-fail-recovery` | `gap-plan-pending-studio-ui-ux-studio-ux-17-gpu-fail-recovery` | **open** | Supervisor off |
| sim-md-research | `md-r3-oracle-plan` | `gap-plan-pending-sim-md-research-md-r3-oracle-plan` | **open** | Supervisor off |
| sim-chem-research | `chem-r2-dft-scf-gap` | `gap-plan-pending-sim-chem-research-chem-r2-dft-scf-gap` | **open** | Last run gates_ok=false |
| sim-chem-research | `chem-r3-package-placement` | `gap-plan-pending-sim-chem-research-chem-r3-package-placement` | **open** | Supervisor off |
| security-research | `sec-r1-httpd-fuzz-smoke` | `gap-plan-pending-security-research-sec-r1-httpd-fuzz-smoke` | **open** | Agent exit 1 on last attempt |
| security-research | `sec-r2-tier5-gap-exploit` | `gap-plan-pending-security-research-sec-r2-tier5-gap-exploit` | **open** | — |
| security-research | `sec-r3-runtime-surface` | `gap-plan-pending-security-research-sec-r3-runtime-surface` | **open** | — |

**Stale registry (snapshot `plan_pending=[]` but registry still open):**

| Runner | Stale open ids | Should be |
|--------|----------------|-----------|
| sim | `gap-plan-pending-sim-sim-p1-num-dot-axpy`, `…-md-neighbor-cell`, `…-p2-qm-dft-scf` | **closed** (5/5 todos completed) |

**Runners with empty `plan_pending`:** `compiler-studio` (47/47), `sim` (5/5), `swarm-observer` (5/5).

## Provability / G-*

From `lic/docs/verification/provability-gaps.md` (2026-05-21):

| Status | Count | IDs |
|--------|-------|-----|
| Partial | 13 | G-lean, G-vc, G-par, G-dec, G-math, G-bnd, G-stdlib, G-math-syn, G-async, G-net, G-trust, G-narrow, G-oop |
| Missing | 4 | G-ann, G-gpu, G-meta, G-authz |

**PH alignment:**

- **2i / 7e → G-math:** closed slices (dot/norm/axpy, length-1 broadcast codegen, tier-1 horner); open: yellow matmul rows, float `@` Props, broadcast Lean witness.
- **7d → G-dec + G-par:** parse/policy/`@vectorized` MIR done; decorator MIR proc tags + Lean disjoint semantics open.
- **2f tracker [x] vs G-lean Partial:** intentional — `sqrt_open_bound`, kernel-not-default-gate remain open per register.

### `recommended_actions` cross-check (audit vs plan debt)

| Audit action | Priority | Plan / registry overlap |
|--------------|----------|-------------------------|
| Fix failing org CI | **P0** (ecosystem) | 39 failed PRs — blocks new PH closure |
| Close/update master plan tracker rows | **P1** (audit) | 5 open PH rows; registry `gap-plan-debt-lic-master-plan-*` mirrors same debt |
| Update `provability-gaps.md` on compiler close | **P1** (audit) | Register stale vs broadcast_len1 codegen + tier-1 yellow reality |
| Catalog path gaps (117) | **P2** (audit) | `competitor_feature` rows — aspirational catalog, not PH blockers |
| Archive normative spec checklists | **P3** (audit) | 9 stale rows in `phase-02-typechecker.md` |

## Recommended issues

**GitHub API rate limit exceeded** — no new issues filed this pass. Existing issues cover the three highest master-plan gaps without an active orchestrator loop:

| # | Title | Repo | Labels | PH-/G- ids |
|---|-------|------|--------|------------|
| [#525](https://github.com/li-langverse/lic/issues/525) | PH-8p-c: `--jobs` sets `LI_COMPILE_JOBS` but compiler never reads it | lic | plan-needed, master-plan-gap | PH-8p, PH-8p-c |
| [#526](https://github.com/li-langverse/lic/issues/526) | PH-2i: full NumPy-rank broadcast — defer gate + compile_fail corpus | lic | plan-needed, master-plan-gap | PH-2i, G-math |
| [#387](https://github.com/li-langverse/lic/issues/387) | G-par: Lean disjoint proofs for `@parallel(disjoint=)` | lic | plan-needed, master-plan-gap | PH-7d, G-par |

**Orchestrator loops (do not duplicate with issues):** httpd wrk-soak (#477 area), studio-ui-ux wave-2 (#182), sim-md/chem/security research runners (#521–523).

## Deferred

- No master-plan checkbox edits — no `[x]` without test/Lean evidence in same PR.
- No implementation (`plan-approved` required for code agents).
- No new GitHub Actions `schedule:` cron.
- Did not re-run full `ecosystem-audit.py` or `issue-feature-triage.py` (briefing used cached ecosystem audit).
- Registry stale-row cleanup (`sim` completed todos; httpd dedupe reopen) left to `swarm_observer` — ingest added 0 snapshot reconciliation rows this pass.
- Issue filing deferred until GitHub API rate limit resets.
