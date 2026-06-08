# Plan verifier digest — 2026-05-30T13:31Z

**Preflight:** `benchmarks/data/latest/plan-completion-audit.json` at `2026-05-30T13:31Z` (166 findings).  
**Swarm ingest:** `lic/scripts/swarm-gap-ingest.py` exit 0 — registry **90** gaps (55 `plan_debt`, 30 `competitor_feature`, 5 `missing_package`); 0 rows added this pass.  
**north_star_fit:** governance · PH-2i, PH-7d, PH-7e, PH-8p, Vision-LLM · G-math, G-par, G-dec, G-math-syn

## Executive summary

- **5** master-plan tracker rows remain unchecked (2i, 7d, 7e, 8p, Vision-LLM); **31** phases complete; audit **166** findings (`open_tracker_items: 5`, `open_plan_checkboxes: 26`).
- **PH-2i:** length-1 broadcast has `li-tests` evidence (`broadcast_len1_*`, `norm_float4` in `manifest.toml`); full NumPy-rank broadcast and P-linalg loop≡ensures gate still open.
- **PH-7e / G-math:** six tier-1 benchmarks red vs C++ (>1.2×): `matmul_blocked`, `matmul_naive`, `ml_conv2d_forward`, `ml_mlp_*`, `num_gmres` — blocks perf sub-plan gate (#463).
- **PH-7d / G-par / G-dec:** `@vectorized` → `ArraySimdScope` in MIR (`compiler/mir/lower.cpp`); policy tests green; MIR proc tags + Lean disjoint proofs open (#387).
- **PH-8p:** `--jobs=N` only `setenv("LI_COMPILE_JOBS")` in `compiler/lic/main.cpp`; no compiler consumer — #525.
- **Provability:** 13 Partial + 4 Missing **G-***; register dated 2026-05-21; none marked **Done**.
- **Goal-directed agents:** **10** `plan_pending` todos across **5** runners; registry ids `gap-plan-pending-<runner>-<todo>` aligned; httpd wrk-soak rows **closed** in registry but still **pending** in snapshot (supervisor stale, exit 124).
- **Ecosystem P0:** 33 failed PRs (ecosystem-audit) precede new plan work; plan audit `recommended_actions` P1/P2 align with master-plan debt.

## Tracker review

| Phase | Master plan cite | Verdict | Evidence |
|-------|------------------|---------|----------|
| **2i** | `lic/docs/superpowers/plans/2026-05-14-li-master-plan.md:444` | **Open (partial)** | **Slice done:** `math_linalg/norm_float4.li`, `reductions/`, `broadcast_len1_add_float4.li`, `broadcast_len1_mul_int4.li` (`li-tests/manifest.toml:825-830,868`). **Open:** NumPy-rank broadcast (#526); sub-plan gate **P-linalg** loop≡ensures (#472). |
| **7d** | `:454` | **Open (partial)** | **Slice done:** `decorators/vectorized_for_scope_ok.li`, `parallel_def_disjoint_inherit.li` (#150 7d-c). **Open:** full MIR proc tags, **G-par** Lean (#387); phase-07 gate “Tier 2 MD `@` on `def`” unchecked. |
| **7e** | `:455` | **Open (partial)** | **Slice done:** loop matmul + FMA horner; `horner_pure_li` advisory green per register. **Open:** 6 red tier-1 rows (ecosystem audit); strict `LI_TIER1_PERF_STRICT` optional (#463). |
| **8p** | `:467` | **Open (partial)** | Ninja `-j` for C++ only. **Open:** `run_all.sh` sequential (#428); `--jobs` parse-only (#525). |
| **Vision-LLM** | `:473` | **Open (partial)** | **Slice done:** `li-tests/tooling/diagnose_json_smoke.sh`, `lic check --format=json`. **Open:** manifest stub ship gate (#464). |

**Sub-plan exit gates (26 open, not PH tracker):** phase-02 typechecker (3); phase-07 HPC (3); plots-and-social (4); ecosystem-governance (7); math-linalg P-linalg (#472); package-scaffold (7).

**Mark `[x]` only with tests/Lean cite:** none of the five tracker rows qualify for full closure.

### `plan_pending` → registry `plan_debt`

| Runner | `plan_pending` | Registry id | Status |
|--------|----------------|-------------|--------|
| httpd | `gap-phase2-perf-wrk-soak` | `gap-plan-pending-httpd-gap-phase2-perf-wrk-soak` | registry **closed** (deduped); snapshot still **pending** |
| httpd | `gap-phase2-streaming-wrk` | `gap-plan-pending-httpd-gap-phase2-streaming-wrk` | registry **closed** (deduped); snapshot still **pending** |
| studio-ui-ux | `studio-ux-16-palette-search-latency` | `gap-plan-pending-studio-ui-ux-studio-ux-16-palette-search-latency` | **open** |
| studio-ui-ux | `studio-ux-17-gpu-fail-recovery` | `gap-plan-pending-studio-ui-ux-studio-ux-17-gpu-fail-recovery` | **open** |
| sim-md-research | `md-r3-oracle-plan` | `gap-plan-pending-sim-md-research-md-r3-oracle-plan` | **open** (#523) |
| sim-chem-research | `chem-r2-dft-scf-gap`, `chem-r3-package-placement` | `gap-plan-pending-sim-chem-research-chem-r2-*`, `chem-r3-*` | **open** (#522) |
| security-research | `sec-r1-httpd-fuzz-smoke`, `sec-r2-tier5-gap-exploit`, `sec-r3-runtime-surface` | `gap-plan-pending-security-research-sec-r*` | **open** (#521) |

**Runners with empty `plan_pending`:** `compiler-studio` (47/47), `sim` (5/5), `swarm-observer` (5/5).

## Provability / G-*

From `lic/docs/verification/provability-gaps.md` (2026-05-21):

| Status | Count | IDs |
|--------|-------|-----|
| Partial | 13 | G-lean, G-vc, G-par, G-dec, G-math, G-bnd, G-stdlib, G-math-syn, G-async, G-net, G-trust, G-narrow, G-oop |
| Missing | 4 | G-ann, G-gpu, G-meta, G-authz |

**PH alignment:** 2i/7e → **G-math** (closed slices: dot/norm/axpy/broadcast_len1; open: tier-1 reds, full matmul float Props). 7d → **G-dec** + **G-par**. 2f tracker marked done but **G-lean** / **G-vc** remain Partial (`sqrt_open_bound` intentional open).

### `recommended_actions` cross-check (audit vs ecosystem)

| Action | Priority | Plan debt overlap |
|--------|----------|-------------------|
| Fix failing PR CI | P0 (ecosystem) | 33 failed PRs — precedes new plan work |
| Close/update master plan tracker rows | P1 (audit) | 5 open PH rows above |
| Update `provability-gaps.md` on compiler close | P1 (audit) | Register stale vs broadcast_len1 / tier-1 red reality |
| Archive normative spec checklists | P3 (audit) | 9 stale rows in `phase-02-typechecker.md` |
| Catalog path gaps (117) | P2 (audit) | `competitor_feature` registry rows — not PH blockers |

## Recommended issues

No new issues filed this pass (existing coverage sufficient).

| # | Title | Repo | Labels | PH-/G- ids |
|---|-------|------|--------|------------|
| [#525](https://github.com/li-langverse/lic/issues/525) | PH-8p-c: `--jobs` sets `LI_COMPILE_JOBS` but compiler never reads it | lic | plan-needed, master-plan-gap | PH-8p-c |
| [#526](https://github.com/li-langverse/lic/issues/526) | PH-2i: full NumPy-rank broadcast — defer gate + compile_fail corpus | lic | plan-needed, master-plan-gap | PH-2i-b, G-math |
| [#527](https://github.com/li-langverse/lic/issues/527) | PH-2h / G-math-syn: for/range Done gate | lic | plan-needed, master-plan-gap | PH-2h, G-math-syn |

**Also tracked (no duplicate):** #463 (PH-7e reds), #387 (G-par MIR), #464 (Vision-LLM), #428/#460 (8p-a), #472 (P-linalg), #477 (httpd wrk), #521–523 (research runners idle).

## Deferred

- No plan checkbox edits or implementation (requires `plan-approved`).
- Runner-owned todos (httpd, studio-ui-ux, sim-*, security-research) — swarm_observer / existing #477, #521–523.
- Catalog-only gaps (117) and 9 stale normative spec checklists — docs hygiene, not PH closure.
- Filing duplicate GitHub issues for PH rows already covered by #463, #387, #464, #525–527.
