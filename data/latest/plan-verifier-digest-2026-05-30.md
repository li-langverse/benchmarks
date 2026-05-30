# Plan verifier digest — 2026-05-30

**Preflight:** `plan-completion-audit.json` regenerated at `2026-05-30T09:35Z` (166 findings).  
**Swarm ingest:** `lic/scripts/swarm-gap-ingest.py` exit 0 — registry 83 gaps (48 plan_debt, 30 competitor, 5 missing_package); no new rows this pass.

## Executive summary

- **5** master-plan tracker rows remain unchecked (2i, 7d, 7e, 8p, Vision-LLM); **31** phases marked complete; **166** total audit findings.
- **PH-2i-b length-1 broadcast** has compile evidence (`broadcast_len1_add_float4.li`, `broadcast_len1_mul_int4.li`); tracker still lists it open — reconcile needed (#386, #462 stale).
- **PH-7e / G-math:** 6 tier-1 benchmarks red vs C++ (>1.2×): `matmul_blocked`, `matmul_naive`, `ml_*`, `num_gmres` — blocks perf sub-plan gate (#463).
- **PH-7d / G-par:** `@vectorized` + `@parallel` parse/policy tests green; **MIR proc tags + Lean disjoint proofs** still open (#387).
- **PH-8p:** `run_all.sh` sequential (no `LI_TEST_JOBS`); `lic --jobs` sets env only — no compiler consumer (#428, **#525** new).
- **Provability:** 13 Partial + 4 Missing **G-*** rows; none **Done**; register last updated 2026-05-21.
- **Goal-directed agents:** 8 runners with **plan_pending** (10 todos); registry cross-links via `gap-plan-pending-<runner>-<todo>`; httpd wrk-soak items blocked (exit 124).
- **3 new issues filed** for non-orchestrator gaps: #525 (8p-c), #526 (2i NumPy-rank defer), #527 (G-math-syn for/range).

## Tracker review

| Phase | Tracker cite | Status | Test / Lean evidence |
|-------|--------------|--------|----------------------|
| **2i** | `lic/docs/superpowers/plans/2026-05-14-li-master-plan.md:444` | **Open (partial)** | **Done slice:** `norm_float4.li`, `axpy_float4.li`, `reductions/`, `broadcast_len1_*.li` (`manifest.toml:825-830`). **Open:** full NumPy-rank broadcast; P-linalg loop≡ensures sub-plan gate (#472). |
| **7d** | `:454` | **Open (partial)** | **Done slice:** `decorators/vectorized_for_scope_ok.li`, `parallel_def_disjoint_inherit.li` (#150 7d-c). **Open:** MIR proc tags, **G-par** Lean (#387); Tier-2 MD `@` on `def` gate (#429). |
| **7e** | `:455` | **Open (partial)** | **Done slice:** loop matmul + FMA horner advisory; `horner_pure_li` green. **Open:** 6 red tier-1 rows (ecosystem audit); `LI_TIER1_PERF_STRICT` optional (#463). |
| **8p** | `:467` | **Open (partial)** | Ninja `-j` for C++ only. **Open:** `LI_TEST_JOBS` in `run_all.sh` (#428); `--jobs` parse-only in `main.cpp:161-163` (#525). |
| **Vision-LLM** | `:473` | **Open (partial)** | **Done slice:** `li-tests/tooling/diagnose_json_smoke.sh`, `lic check --format=json`. **Open:** manifest stub ship gate (#464, #425). |

**Sub-plan exit gates (26 open, not tracker):** notable clusters — phase-02 typechecker (3 gates; li-tests evidence likely exists, #470), phase-07 HPC tier-1 perf + decorator fuzz (3), plots-and-social (4, #459), ecosystem-governance (7, #476), math-linalg P-linalg Lean gate (#472), package-scaffold (7).

**Mark done only with evidence:** None of the 5 tracker rows meet full closure; partial slices documented above.

### plan_pending → registry `plan_debt` map

| Runner | plan_pending todo | Registry id | Registry status |
|--------|-------------------|-------------|-----------------|
| httpd | `gap-phase2-perf-wrk-soak` | `gap-plan-pending-httpd-gap-phase2-perf-wrk-soak` | closed (deduped; snapshot still pending) |
| httpd | `gap-phase2-streaming-wrk` | `gap-plan-pending-httpd-gap-phase2-streaming-wrk` | closed (deduped; snapshot still pending) |
| studio-ui-ux | `studio-ux-16-palette-search-latency` | `gap-plan-pending-studio-ui-ux-studio-ux-16-palette-search-latency` | open |
| studio-ui-ux | `studio-ux-17-gpu-fail-recovery` | `gap-plan-pending-studio-ui-ux-studio-ux-17-gpu-fail-recovery` | open |
| sim-md-research | `md-r3-oracle-plan` | `gap-plan-pending-sim-md-research-md-r3-oracle-plan` | open |
| sim-chem-research | `chem-r2-dft-scf-gap`, `chem-r3-package-placement` | `gap-plan-pending-sim-chem-research-chem-r2-*`, `chem-r3-*` | open |
| security-research | `sec-r1/2/3-*` | `gap-plan-pending-security-research-sec-r*` | open |

Orchestrator loops apply to httpd, studio-ui-ux, sim-*, security-research — issues #477, #521–523 cover supervisor idle; swarm_observer ingest ran clean.

## Provability / G-*

From `lic/docs/verification/provability-gaps.md` (updated 2026-05-21):

| Status | Count | IDs |
|--------|-------|-----|
| Partial | 13 | G-lean, G-vc, G-par, G-dec, G-math, G-bnd, G-stdlib, G-math-syn, G-async, G-net, G-trust, G-narrow, G-oop (+ G-def Partial+ in register) |
| Missing | 4 | G-ann, G-gpu, G-meta, G-authz |

**Active-phase alignment:** PH-2i/7e → **G-math** (closed slices: dot/norm/axpy/broadcast_len1; open: full matmul float Props, tier-1 reds). PH-7d → **G-dec** + **G-par**. PH-2f → **G-lean** + **G-vc** (`sqrt_open_bound` intentional open).

**recommended_actions cross-check (audit vs plan debt):**

| Audit action | Priority | Plan debt overlap |
|--------------|----------|-------------------|
| Close/update master plan tracker rows | P1 | 5 open rows above |
| Update provability-gaps on compiler close | P1 | Register stale 9d; broadcast slice not reflected |
| Archive stale normative checklists | P3 | 9 in phase-02 typechecker plan |
| Catalog gaps (117) | P2 | Registry competitor_feature rows; not master-plan blockers |

## Recommended issues

| # | Title | Repo | Labels | PH-/G- ids |
|---|-------|------|--------|------------|
| [#525](https://github.com/li-langverse/lic/issues/525) | PH-8p-c: `--jobs` sets env but compiler never reads `LI_COMPILE_JOBS` | lic | plan-needed, master-plan-gap | PH-8p-c |
| [#526](https://github.com/li-langverse/lic/issues/526) | PH-2i: full NumPy-rank broadcast — defer gate + compile_fail corpus | lic | plan-needed, master-plan-gap | PH-2i-b, G-math |
| [#527](https://github.com/li-langverse/lic/issues/527) | PH-2h / G-math-syn: for/range Done gate | lic | plan-needed, master-plan-gap | PH-2h, G-math-syn |

**Existing issues (no duplicate filed):** #463 (PH-7e reds), #387 (G-par MIR), #428/#460 (8p-a), #386/#462 (2i broadcast reconcile — commented #462), #477 (httpd wrk soak), #472 (P-linalg Lean gate).

## Deferred

- No plan checkbox edits or code implementation (plan-approved required).
- Did not file issues for runner-owned todos (httpd, studio-ui-ux, sim-*, security-research) — swarm_observer backlog.
- 117 catalog path gaps (P2) — bench_improver / gap_explorer scope.
- 45 failed org PRs (ecosystem audit) — P0 CI before new plan work; not expanded here.
- provability-gaps.md typo/duplicate appendix (#461) — docs-only, out of verifier scope.
- Self-merge, gate weakening, GitHub Actions `schedule:` cron — not attempted.
