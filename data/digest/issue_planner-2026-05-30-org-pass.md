# Issue feature planner — org pass (2026-05-30)

**Run:** `issue_planner-2026-05-30-org-pass` · **Date:** 2026-05-30  
**Scope:** 6 repos scanned; **3 new plans** on **lic** (language/compiler); **benchmarks** plans verified (no duplicates)  
**north_star_fit:** Scientific/HPC · **PH-2i**, **PH-2h**, **PH-2f**, **G-lean**, **G-math-syn** · proof → easy → fast

## Executive summary

- **Scanned 6 repos** via `scripts/issue-feature-triage.py`: **42** `needs_plan`, **3** lic `candidates`; **benchmarks** 11 planning issues all already have plan comments + draft PRs from prior passes.
- **Three new lic plans** drafted this run (**#472**, **#527**, **#526**) — one draft PR each; issue comments posted; **no code implementation**.
- **proof_gap_researcher handoff:** **lic#472** plan scopes P-linalg loop≡ensures slices; links cycle 21 Horner FMA drift digest (**G-hw**, **G-meta**, **G-vc**).
- **Benchmarks catalog debt (#179):** draft [PR #183](https://github.com/li-langverse/benchmarks/pull/183) unchanged; local `LIC_ROOT=../lic` audit shows **catalog_gaps: 0** — triage policy for 117 historical rows remains valid.
- **Six tier-1 near-threshold** rows in ecosystem audit (not red); perf work stays in **lic** harness — no threshold weakening.
- **39 lic `needs_plan`** items remain for future planner passes (**#387** PH-7d, **#463** tier-1 reds, Vision-LLM **#464**).
- **Human-only:** add **`plan-approved`** on **lic#472**, **#527**, **#526** (and pending benchmarks **#179**, **#181**, **#20**) before implementation agents.

## Deliverable / findings

### 1. Issues scanned

| Repo | `needs_plan` | `candidates` | Action this run |
|------|--------------|--------------|-----------------|
| **lic** | 31 | 3 | **3 plans** drafted (#472, #527, #526) |
| **benchmarks** | 11 | 0 | Verified existing plans; no duplicate PRs |
| **lip**, **lit** | 0 | 0 | — |
| **lis**, **roadmap** | — | — | `gh` empty / failed in triage |

**Triage artifact:** `data/latest/issue-feature-triage.json` (`generated_at`: 2026-05-30T10:26Z)

### 2. Plans drafted (max 3)

| Issue | Plan path | Draft PR | Status |
|-------|-----------|----------|--------|
| [lic#472](https://github.com/li-langverse/lic/issues/472) P-linalg loop ≡ ensures | [2026-05-30-p-linalg-loop-ensures-ph2i.md](https://github.com/li-langverse/lic/blob/docs/plan-p-linalg-loop-ensures-472/docs/superpowers/plans/2026-05-30-p-linalg-loop-ensures-ph2i.md) | [lic PR #530](https://github.com/li-langverse/lic/pull/530) | Comment posted; **DRAFT** |
| [lic#527](https://github.com/li-langverse/lic/issues/527) for/range PH-2h | [2026-05-30-for-range-ph2h-g-math-syn.md](https://github.com/li-langverse/lic/blob/docs/plan-for-range-ph2h-527/docs/superpowers/plans/2026-05-30-for-range-ph2h-g-math-syn.md) | [lic PR #531](https://github.com/li-langverse/lic/pull/531) | Comment posted; **DRAFT** |
| [lic#526](https://github.com/li-langverse/lic/issues/526) NumPy broadcast defer | [2026-05-30-numpy-broadcast-defer-ph2i.md](https://github.com/li-langverse/lic/blob/docs/plan-numpy-broadcast-defer-526/docs/superpowers/plans/2026-05-30-numpy-broadcast-defer-ph2i.md) | [lic PR #532](https://github.com/li-langverse/lic/pull/532) | Comment posted; **DRAFT** |

**Benchmarks (prior pass, verified):** #179 → [PR #183](https://github.com/li-langverse/benchmarks/pull/183); #20/#54 → [PR #135](https://github.com/li-langverse/benchmarks/pull/135); #53 → [PR #137](https://github.com/li-langverse/benchmarks/pull/137); #51/#52 → FFT rubrics on `main`.

### 3. Issues blocked / deferred

| Item | Reason |
|------|--------|
| **lic#472** implementation | Needs **`plan-approved`**; P-float / Horner slices human-scoped |
| **lic#527**, **#526** implementation | Needs **`plan-approved`** |
| **benchmarks** duplicate plans | All 11 `needs_plan` already have plan comments — skipped |
| **lic#463**, **#424** tier-1 reds | **bench_improver** / harness — not planner (no threshold weakening) |
| **lic#473**, **#471**, **#436** | Swarm-gap ingest blocked — unblocks benchmarks **#181** |
| **lic** studio-ui **#394–#399** | Lower priority vs proof/math backlog |
| **roadmap** / governance PRs | Do not self-merge |

### 4. proof_gap_researcher handoff (`provability_holes`, priority 9)

| Priority | Target | PH / G-* | Planner action |
|----------|--------|----------|----------------|
| P0 | P-linalg loop≡ensures backlog | **PH-2i**, **G-lean**, **G-vc** | **lic#472** plan + [PR #530](https://github.com/li-langverse/lic/pull/530) |
| P0 | Horner FMA vs `--numerically-stable` | **PH-7e**, **G-hw**, **G-meta** | Scoped as **sub E** in #472 plan; cycle 21 digest linked |
| P1 | for/range syntax gate | **PH-2h**, **G-math-syn** | **lic#527** plan |
| P1 | Broadcast reject honesty | **PH-2i-b**, **G-math** | **lic#526** plan |
| Defer | matmul IKJ full witness | **G-lean** | **sub D** in #472 — after int pilot |
| Defer | `publish_subdir` whitepaper | — | Auxiliary goal |

## Recommended issues/PRs

### Maintainer (plan approval)

| Title | Repo | Action |
|-------|------|--------|
| docs(plan): P-linalg loop ≡ ensures PH-2i/2f (#472) | lic | [PR #530](https://github.com/li-langverse/lic/pull/530) — **`plan-approved`** on #472 |
| docs(plan): for/range surface PH-2h (#527) | lic | [PR #531](https://github.com/li-langverse/lic/pull/531) — **`plan-approved`** on #527 |
| docs(plan): NumPy broadcast defer PH-2i-b (#526) | lic | [PR #532](https://github.com/li-langverse/lic/pull/532) — **`plan-approved`** on #526 |
| docs(plan): catalog path reconciliation PH-5b (#179) | benchmarks | [PR #183](https://github.com/li-langverse/benchmarks/pull/183) — pending from prior pass |

### Implementation agents (after `plan-approved` only)

| Agent | Target | Reason |
|-------|--------|--------|
| **proof_gap_researcher** | lic#472 sub B–E | `provability_holes` — loop witnesses |
| **code_implementer** | lic#527 parser/typecheck | **G-math-syn** syntax slice |
| **code_implementer** | lic#526 compile_fail corpus | **G-math** reject policy |
| **bench_improver** | tier-1 near-threshold (`matmul_*`, `simd_dot`) | **PH-5b**, **PH-7e** — lic harness |

## Deferred

- Next lic planner pass: **#387** (PH-7d MIR proc tags), **#464** (Vision-LLM manifest), **#525** (PH-8p `--jobs`).
- Self-merge of roadmap/governance docs.
- GitHub Actions new `schedule:` cron entries.
- Threshold ratio weakening on any benchmark row.
