# Plan verifier digest — 2026-05-30

**Preflight:** `data/latest/plan-completion-audit.json` at `2026-05-30T10:26Z` (166 findings).  
**Swarm ingest:** `lic/scripts/swarm-gap-ingest.py` exit 0 — registry 83 gaps (48 `plan_debt`, 30 `competitor_feature`, 5 `missing_package`); 0 rows added this pass.  
**north_star_fit:** governance · PH-2i, PH-7d, PH-7e, PH-8p, Vision-LLM · G-math, G-par, G-dec, G-math-syn

## Executive summary

- **5** master-plan tracker rows remain unchecked (2i, 7d, 7e, 8p, Vision-LLM); **31** phases marked complete; audit totals **166** findings (`open_tracker_items: 5`, `open_plan_checkboxes: 26`, `catalog_gaps: 117`).
- **PH-2i (partial):** `norm`, `sum`/`dot`, `reductions/`, length-1 broadcast, and scalar×array have `li-tests/math_linalg/` + `manifest.toml` rows; full NumPy-rank broadcast and **P-linalg** loop≡`ensures` gate stay open.
- **PH-7e (partial):** tier-1 dashboard has **0 red** / **5 near-threshold** (`matmul_naive` 1.06×, `simd_dot` 1.05×, `matmul_blocked` 1.02×); advisory ≤1.2× holds — reconcile stale **#463** (still titles “red benchmarks”).
- **PH-7d (partial):** `@vectorized` on `for` → `ArraySimdScope` has decorator tests; **G-par** MIR proc tags + Lean disjoint proofs open (**#387**).
- **PH-8p (partial):** C++ Ninja `-j` only; `run_all.sh` sequential; `lic build --jobs=N` sets `LI_COMPILE_JOBS` without compiler consumer (**#525**).
- **Provability:** **13** Partial + **4** Missing **G-*** per audit; register last updated **2026-05-21** — no row marked **Done**.
- **Goal-directed agents:** **10** `plan_pending` todos across **5** runners; registry `gap-plan-pending-<runner>-<todo>` ids aligned after ingest; httpd wrk/streaming todos supervisor-stale (exit 124, **#477**).
- **Issues this pass:** no new duplicates — cite **#525–527** (filed earlier today), **#477**, **#521–523**, **#387**, **#464**, **#49** (register drift).

## Tracker review

| Phase | Master plan cite | Verdict | Evidence |
|-------|------------------|---------|----------|
| **2i** | `lic/docs/superpowers/plans/2026-05-14-li-master-plan.md:444` | **Open (partial)** | **Done slices:** `math_linalg/norm_float4.li`, `reductions/sum_float4.li`, `broadcast_len1_add_float4.li`, `broadcast_len1_mul_int4.li` (`li-tests/manifest.toml:825-830,868`). **Open:** NumPy-rank broadcast (**#526**); sub-plan gate **P-linalg** loop≡ensures (`docs/superpowers/plans/2026-05-16-li-math-linalg-surface.md:171`, **#472**). |
| **7d** | `:454` | **Open (partial)** | **Done slices:** `decorators/vectorized_for_scope_ok.li`, `parallel_def_disjoint_inherit.li` (#150 7d-c). **Open:** full MIR proc tags, **G-par** Lean (**#387**); phase-07 plan gate “Tier 2 MD `@` on `def`” still unchecked. |
| **7e** | `:455` | **Open (partial)** | **Done slices:** `scripts/check-tier1-li-vs-cpp.sh`, `horner_pure_li` / `matmul_naive` in advisory set; ecosystem audit **green_count: 22**, near-threshold only. **Open:** strict `LI_TIER1_PERF_STRICT`, remaining float Lean Props; **#463** title stale vs dashboard. |
| **8p** | `:467` | **Open (partial)** | **Done:** Ninja `-j` in `scripts/build.sh`. **Open:** `li-tests/run_all.sh` has no `LI_TEST_JOBS` pool (**#428**); `--jobs` parse-only in `compiler/lic/main.cpp:161-163` (**#525**). |
| **Vision-LLM** | `:473` | **Open (partial)** | **Done slices:** `li-tests/tooling/diagnose_json_smoke.sh`, `lic check --format=json`, `docs/schemas/diagnostic-v1.json`. **Open:** manifest ship gate (**#464**, **#425**). |

**Sub-plan exit gates (26 open):** phase-02 typechecker (3 gates), phase-07 HPC (3), plots-and-social (4), ecosystem-governance (7), math-linalg **P-linalg** + tier-1 perf (2), package-scaffold (7). **9** normative spec checklist rows flagged stale (not PH blockers).

**Mark `[x]` only with tests/Lean cite:** none of the five tracker rows qualify for full closure.

### `plan_pending` → registry `plan_debt`

| Runner | `plan_pending` | Registry id | Notes |
|--------|----------------|-------------|-------|
| httpd | `gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk` | `gap-plan-pending-httpd-gap-phase2-*` | snapshot **pending**; agent exit **124**; **#477** |
| studio-ui-ux | `studio-ux-16-palette-search-latency`, `studio-ux-17-gpu-fail-recovery` | `gap-plan-pending-studio-ui-ux-studio-ux-16-*`, `…-17-*` | supervisor idle |
| sim-md-research | `md-r3-oracle-plan` | `gap-plan-pending-sim-md-research-md-r3-oracle-plan` | **#523** |
| sim-chem-research | `chem-r2-dft-scf-gap`, `chem-r3-package-placement` | `gap-plan-pending-sim-chem-research-chem-r2-*`, `chem-r3-*` | **#522** |
| security-research | `sec-r1-httpd-fuzz-smoke`, `sec-r2-tier5-gap-exploit`, `sec-r3-runtime-surface` | `gap-plan-pending-security-research-sec-r*` | **#521** |

**Empty `plan_pending`:** `compiler-studio` (47/47), `sim` (5/5), `swarm-observer` (5/5).

## Provability / G-*

From `lic/docs/verification/provability-gaps.md` (2026-05-21):

| Status | Count | IDs |
|--------|-------|-----|
| Partial | 13 | G-lean, G-vc, G-par, G-dec, G-math, G-bnd, G-stdlib, G-math-syn, G-async, G-net, G-trust, G-narrow, G-oop |
| Missing | 4 | G-ann, G-gpu, G-meta, G-authz |

**PH alignment:** 2i/7e → **G-math** (closed slices documented in register; open: P-linalg loop witness, full float matmul Props). 7d → **G-dec** + **G-par**. Phase **2f** tracker `[x]` but **G-lean** / **G-vc** remain Partial (`sqrt_open_bound` intentional open per register).

**`recommended_actions` cross-check (ecosystem audit `2026-05-30T10:20Z`):**

| Action | Priority | Plan overlap |
|--------|----------|--------------|
| Fix failing PR CI | **P0** | 44 failed PRs — precedes new PH work |
| Close/update master plan tracker rows | **P1** | 5 open PH rows above |
| Update `provability-gaps.md` on compiler close | **P1** | Register stale vs broadcast_len1 / tier-1 greens (**#49**) |
| Catalog path gaps (117) | **P2** | `competitor_feature` registry — not PH blockers |
| Archive normative spec checklists | **P3** | 9 stale rows in `phase-02-typechecker.md` |

## Recommended issues

No new issues filed this pass (orchestrator loops + morning batch cover debt). Track existing:

| # | Title | Labels | PH-/G- ids |
|---|-------|--------|------------|
| [#525](https://github.com/li-langverse/lic/issues/525) | PH-8p-c: `--jobs` sets `LI_COMPILE_JOBS` but compiler never reads it | plan-needed, master-plan-gap | PH-8p-c |
| [#526](https://github.com/li-langverse/lic/issues/526) | PH-2i: full NumPy-rank broadcast defer gate | plan-needed, master-plan-gap | PH-2i-b, G-math |
| [#527](https://github.com/li-langverse/lic/issues/527) | PH-2h / G-math-syn: for/range Done gate | plan-needed, master-plan-gap | PH-2h, G-math-syn |
| [#477](https://github.com/li-langverse/lic/issues/477) | PH-H httpd: wrk-soak + streaming-wrk pending | plan-needed, master-plan-gap | PH-H |
| [#521–523](https://github.com/li-langverse/lic/issues/521) | security / chem / md research runners idle | plan-needed, master-plan-gap | — |
| [#387](https://github.com/li-langverse/lic/issues/387) | PH-7d / G-par: MIR proc tags + Lean proofs | plan-needed, master-plan-gap | PH-7d, G-par |
| [#464](https://github.com/li-langverse/lic/issues/464) | Vision-LLM manifest ship gate | plan-needed, master-plan-gap | Vision-LLM |
| [#463](https://github.com/li-langverse/lic/issues/463) | PH-7e tier-1 reds — **stale** vs 2026-05-30 dashboard (0 red) | master-plan-gap | PH-7e, G-math |

## Deferred

- No plan checkbox edits or implementation (`plan-approved` required for code agents).
- Runner-owned todos — `swarm_observer` / goal-directed loops (**#477**, **#521–523**).
- **117** catalog path gaps — P2 competitor backlog, not master-plan PH closure.
- **P0** org CI on 44 failed PRs — `ecosystem-audit.json` `recommended_actions`; out of plan_verifier scope.
- Re-run full `ecosystem-audit.py` in CI preflight (briefing used `--skip-slow` for plan_audit).
