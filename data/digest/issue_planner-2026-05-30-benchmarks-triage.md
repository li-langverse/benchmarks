# Issue feature planner — benchmarks triage (2026-05-30)

**Run:** `issue_planner-2026-05-30-benchmarks-triage` · **Date:** 2026-05-30  
**Scope:** li-langverse org (6 repos scanned); **plans acted:** benchmarks **#181**, **#179**, **#20** (verify + handoff)  
**north_star_fit:** Scientific/HPC · **PH-5b**, **PH-7e**, **PH-IO** · proof → easy → fast (no implementation without `plan-approved`)

## Executive summary

- **Scanned 6 repos** via `scripts/issue-feature-triage.py`: **40** `needs_plan`, **3** lic `candidates`; **benchmarks** has **11** open planning issues.
- **Three benchmarks issues** already have vision-aligned plans + **draft PRs** from 2026-05-30 early pass — this run **did not** open duplicate PRs or implement code.
- **Local audit** with `LIC_ROOT=../lic`: **`catalog_gaps: 0`** (65 total findings); issue **#179** triage policy (117 historical gaps / `status=planned`) remains valid for dashboard honesty.
- **`swarm-gap-actions.json`** refreshed locally (`2026-05-30T09:16Z`, **65** open); wiring into preflight per **#181** still blocked on **lic#473** (ingest script on main).
- **Six tier-1 red** rows unchanged (**PH-5b**, **PH-7e**); catalog-only work cannot close them — route to **bench_improver** / **lic** harness.
- **proof_gap_researcher** handoff: **G-hw** / **G-meta** Horner `FmaFloatF64` vs `--numerically-stable`; **lic#472** P-linalg loop ≡ ensures; **lic#461** duplicate Proof-db appendix in `provability-gaps.md`.
- **Human-only:** add **`plan-approved`** on **#181**, **#179**, **#20** (and related) before implementation agents; do not self-merge draft plan PRs.

## Deliverable / findings

### 1. Issues scanned

| Repo | `needs_plan` | `candidates` | Notes |
|------|--------------|--------------|-------|
| **lic** | 28 | 3 | Master-plan-gap, explorer-finding; plans live in **lic** `docs/superpowers/plans/` |
| **benchmarks** | 11 | 0 | This workspace; 3 prioritized below |
| **lip**, **lit** | 0 | 0 | — |
| **lis**, **roadmap** | — | — | `gh` empty / failed in triage script |

**Triage artifact:** `data/latest/issue-feature-triage.json` (`generated_at`: 2026-05-30T09:16Z)

### 2. Plans drafted (this repo, max 3)

| Issue | Plan path | Draft PR | Status |
|-------|-----------|----------|--------|
| [#181](https://github.com/li-langverse/benchmarks/issues/181) Swarm-gap-actions sync | [2026-05-30-swarm-gap-actions-sync.md](https://github.com/li-langverse/benchmarks/blob/docs/plan-swarm-gap-sync-181/docs/ecosystem/plans/2026-05-30-swarm-gap-actions-sync.md) | [PR #182](https://github.com/li-langverse/benchmarks/pull/182) | Plan comment posted; **DRAFT** |
| [#179](https://github.com/li-langverse/benchmarks/issues/179) PH-5b catalog paths (117) | [2026-05-30-catalog-path-reconciliation-ph5b.md](https://github.com/li-langverse/benchmarks/blob/docs/plan-catalog-reconciliation-179/docs/ecosystem/plans/2026-05-30-catalog-path-reconciliation-ph5b.md) | [PR #183](https://github.com/li-langverse/benchmarks/pull/183) | Plan comment posted; **DRAFT** |
| [#20](https://github.com/li-langverse/benchmarks/issues/20) LIC_ROOT CI checkout | [2026-05-29-lic-root-agent-preflight.md](https://github.com/li-langverse/benchmarks/blob/docs/plan-lic-root-preflight-2026-05-29/docs/ecosystem/plans/2026-05-29-lic-root-agent-preflight.md) | [PR #135](https://github.com/li-langverse/benchmarks/pull/135) | Plan comment notes partial merge on `main`; **DRAFT** |

**Legacy plans on `main`:** `docs/ecosystem/plans/2026-05-18-*.md` (FFT #18, tier-2 #19, LIC_ROOT layout) — superseded or complemented by 2026-05-29/30 PR-branch plans.

**No code implementation** in this run (no `plan-approved` on any of the above).

### 3. Issues blocked / deferred

| Item | Reason |
|------|--------|
| **#181** implementation | Blocked on **lic#473** (`swarm-gap-ingest.py` on main), **lic#471**, **lic#436** |
| **#179** implementation | Needs **`plan-approved`** + triage script; tier-2 harness in **lic**, not benchmarks-only |
| **#20** close | Sub-phases B–E in [2026-05-18-lic-root-audit-layout.md](../ecosystem/plans/2026-05-18-lic-root-audit-layout.md) may remain open despite CI checkout |
| **#18** FFT tier-1 | Plan on [PR #136](https://github.com/li-langverse/benchmarks/pull/136); harness must land in **lic** first |
| **#51–#54** explorer rubrics | [PR #198](https://github.com/li-langverse/benchmarks/pull/198) merged for FFT vendors; **#53** PH-IO-7 on [PR #137](https://github.com/li-langverse/benchmarks/pull/137) |
| **lic** 28× `needs_plan` | Out of benchmarks repo scope this run; numerics reds (**#424**, **#463**) → **bench_improver**, not planner |
| Threshold weakening | **Rejected** per vision filter — no `threshold_ratio_cpp` edits |
| **roadmap** / **lis** governance PRs | Do not self-merge |

### 4. proof_gap_researcher handoff (`provability_holes`, priority 9)

Align with [proof_gap_researcher-2026-05-30-horner-fma-literal-drift.md](./proof_gap_researcher-2026-05-30-horner-fma-literal-drift.md) and briefing **G-*** counts (**16** partial, **3** missing).

| Priority | Target | PH / G-* | Action |
|----------|--------|----------|--------|
| P0 | Horner `FmaFloatF64` / `HornerFmaUnroll` ignore `fp_numerically_stable` | **PH-7e**, **G-hw**, **G-meta** | Gate codegen like matmul; literal-addend witness in `horner_fma_literal_lean_drift.sh` |
| P0 | Tier-1 `horner_pure_li` closed slice vs FMA trust hole | **PH-5b**, **G-math** | Do not claim G-math Done until policy + bench evidence align |
| P1 | [lic#472](https://github.com/li-langverse/lic/issues/472) P-linalg loop ≡ ensures sub-plan gate | **PH-2i**, **G-lean** | Plan-only until `plan-approved`; links master plan 2i-b |
| P2 | [lic#461](https://github.com/li-langverse/lic/issues/461) Duplicate Proof-db appendix (`provability-gaps.md` L70–76) | **G-proof-db** | Docs-only fix; no `trusted.lean` |
| Defer | `publish_subdir` whitepaper | — | Auxiliary goal not injected |

**north_star_fit for handoff:** Mathematical provability before tier-1 perf claims; no new trusted axioms for FMA drift.

## Recommended issues/PRs

### Maintainer (plan approval)

| Title | Repo | Labels / action |
|-------|------|-----------------|
| docs(plan): swarm-gap-actions refresh pipeline (#181) | benchmarks | [PR #182](https://github.com/li-langverse/benchmarks/pull/182) — **`plan-approved`** on #181 |
| docs(plan): catalog path reconciliation PH-5b (#179) | benchmarks | [PR #183](https://github.com/li-langverse/benchmarks/pull/183) — **`plan-approved`** on #179 |
| docs(plan): LIC_ROOT agent preflight honesty (#20, …) | benchmarks | [PR #135](https://github.com/li-langverse/benchmarks/pull/135) — review vs merged CI |
| [G-hw/G-meta] Gate FmaFloatF64 / HornerFmaUnroll on fp_numerically_stable | lic | `provability`, `PH-7e` — after proof research cycle 18 |
| Ship swarm-gap-ingest.py on main | lic | [lic#473](https://github.com/li-langverse/lic/issues/473) — unblocks #181 |

### Implementation agents (after `plan-approved` only)

| Agent | Issue / PR | Reason |
|-------|------------|--------|
| **bench_improver** | lic tier-1 reds (`matmul_blocked`, `ml_*`, `num_gmres`) | **PH-5b**, **PH-7e** — harness in **lic** |
| **proof_gap_researcher** | Horner FMA + lic#472 | `provability_holes` goal |
| **plan_verifier** | Merge #182/#183 after approval | Close plan_debt drift |
| **gap_explorer** | std.summary / std.plot | PH-IO-5/7 — blocks Li-native ingest |

## Deferred

- Duplicate planning PRs for issues already covered (#25, #28, #29 → fold into #20 / #135).
- **lic** studio-ui candidates (#394, #398, #399) — lower priority than numerics/proof backlog.
- Org-wide **28** lic `needs_plan` items — next planner pass should pick **lic#472**, **lic#463**, **lic#464** (Vision-LLM).
- Self-merge of roadmap/governance docs.
- GitHub Actions new `schedule:` cron entries.
