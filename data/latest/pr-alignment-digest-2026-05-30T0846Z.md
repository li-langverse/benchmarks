# PR alignment digest — 2026-05-30T08:46Z

**Agent:** `pr_alignment` · **Source:** proactive ecosystem sweep · **North star:** proof → easy → fast (PH-5b, PH-7e, Phase 2i)

## Executive summary

- **166 open org PRs** (`ecosystem-audit.json`); merge-queue scripts report **stale `open_prs=0`** until slow `pr-merge-gate` enrichment finishes (re-run killed >3m).
- **Vision merge order:** mirrors / lip / lit / agent-kit → benchmarks → lic → roadmap (roadmap never auto-close).
- **P0 aligned (no merge this run):** [lip#32](https://github.com/li-langverse/lip/pull/32), [lit#18](https://github.com/li-langverse/lit/pull/18) — `merge-approved`, CI green, human `review_approved` only; alignment comments posted.
- **Numerics canonical:** [lic#499](https://github.com/li-langverse/lic/pull/499) focused matmul MIR restore (PH-5b/7e) — **aligned**, **defer** until `build-and-test` green; supersedes bench_improver stub stack.
- **Feature blocked:** [lic#495](https://github.com/li-langverse/lic/pull/495) CAD v1 — `plan-needed` without `plan-approved`; alignment comment posted.
- **Closed 5 superseded PRs:** lic#504–#508 (agent bench_improver deliverable stubs) with alignment comments → pointer to lic#499.
- **Hygiene backlog:** 133 branches without PR; `prs_recommended_close=0` in `pr-branch-hygiene.json` — manual duplicate scan still required for workspace-sweep PR wave on benchmarks.
- **Issue triage:** 40 `plan-needed` issues on lic, 9 on benchmarks — route to `issue-feature-planner` / `plan_verifier`.
- **No `merge-approved` labels added**; **no merges** (alignment agent mandate).

## Deliverable / findings

### Preflight

| Artifact | `generated_at` | Key signal |
|----------|----------------|------------|
| `pr-merge-queue-plan.json` | 2026-05-30T08:07Z | `merge_sequence=[]`, `open_prs=0` (stale vs REST) |
| `pr-program-run.json` | 2026-05-30T07:59Z | `merge_first=null` |
| `pr-branch-hygiene.json` | 2026-05-30T07:51Z | `branches_needing_pr=133`, `prs_safe_close_now=0` |
| `issue-feature-triage.json` | 2026-05-30T08:38Z | `needs_plan=40` (lic), `candidates=3` |
| `ecosystem-audit.json` | 2026-05-30T08:38Z | `open_prs=166`, `ready_prs=70`, `failed_prs=47` |

`pr-merge-queue-plan.py` + `pr-branch-hygiene.py` + `run-pr-program.py` started; merge-plan refresh **still running** at digest time (>3m).

### Per-PR alignment (sampled 8)

| PR | Plan | PH / PKG | Merge order | Verdict | Action taken |
|----|------|----------|-------------|---------|--------------|
| [lip#32](https://github.com/li-langverse/lip/pull/32) | CI chore | Platform | **First** (before lic) | aligned | Comment |
| [lit#18](https://github.com/li-langverse/lit/pull/18) | CI chore | Platform | **First** | aligned | Comment |
| [lic#499](https://github.com/li-langverse/lic/pull/499) | Bench regression fix | PH-5b, PH-7e | After package wave | aligned, **defer** (CI) | Comment |
| [lic#495](https://github.com/li-langverse/lic/pull/495) | **needs plan** | PH-CAD / AL-4 | After plan gate | needs plan | Comment; keep `plan-needed` |
| [lic#503](https://github.com/li-langverse/lic/pull/503) | Bench improver stack | PH-5b, PH-7e | — | superseded / defer | Prefer #499; 100 commits, **CONFLICTING** |
| [lic#500](https://github.com/li-langverse/lic/pull/500) | Feature | PH-ML | After lic core | defer | CI fail; no comment (digest only) |
| [benchmarks#207](https://github.com/li-langverse/benchmarks/pull/207) | Agent digest | CI maintainer | After mirrors | wait | Large diff; not redundant with #206 sweep |
| [lic#504–508](https://github.com/li-langverse/lic/pull/504) | N/A stubs | PH-5b/7e | — | superseded | **Closed** (5/5 cap) |

### Red bench rows (unchanged)

`matmul_blocked` 1.55×, `matmul_naive` 1.33×, ML forwards 1.33×, `num_gmres` 1.4× vs cpp — do not relax `catalog.toml` thresholds.

### north_star_fit

Numerics PH-5b/PH-7e (tier-1 matmul restoration); ecosystem CI ordering (lip/lit before lic); governance (`plan-needed` on CAD feature).

## Recommended issues/PRs

| Priority | Repo | Item | Labels / notes |
|----------|------|------|----------------|
| P0 | lip | [#32](https://github.com/li-langverse/lip/pull/32) fix(ci) LLVM 22 | `merge-approved` — human approve |
| P0 | lit | [#18](https://github.com/li-langverse/lit/pull/18) fix(ci) LLVM 22 | `merge-approved` — human approve |
| P1 | lic | [#499](https://github.com/li-langverse/lic/pull/499) matmul MIR restore | `numerics-research` — fix `build-and-test`, then pr-review-agent |
| P1 | lic | [#437](https://github.com/li-langverse/lic/pull/437) perf matmul (if still open) | Reconcile with #499 before merge |
| P2 | lic | [#463](https://github.com/li-langverse/lic/issues/463) tier-1 red benchmarks | `plan-needed` / master-plan-gap |
| P2 | lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | `plan-needed` → plan-approved |
| Hygiene | lic | #509–#516 bench_improver runs | Close after #499 lands (next alignment pass) |
| Hygiene | benchmarks | #205–#206 workspace sweeps | Dedupe vs #207; close redundant sweeps |
| Governance | lic | [#476](https://github.com/li-langverse/lic/issues/476) PH-Pkg governance | `plan-needed` |

## Deferred

- Full `pr-merge-queue-plan.py` + `run-pr-program.py` completion (org-scale gate enrichment).
- `plan_audit`, `pr_branch_hygiene` refresh (`--skip-slow` in briefing preflight).
- **roadmap** repo PRs — human merge only; never auto-close.
- **lic#503**, **lic#516** large matmul stacks — conflict resolution vs #499.
- **benchmarks** workspace-sweep PR wave (~18 duplicates per pr_reviewer) — next pass after `safe_now` or explicit duplicate map.
- Adding `merge-approved` — **pr-review-agent** only.
- **Merge execution** — **pr_merger** after human APPROVED.

## Actions log

| Action | PRs |
|--------|-----|
| Alignment comment | lip#32, lit#18, lic#499, lic#495 |
| Closed (superseded) | lic#504, #505, #506, #507, #508 → canonical lic#499 |
