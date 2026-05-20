# PR alignment agent digest — 2026-05-20 (11:50Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`  
**Org:** li-langverse  
**Merges performed:** 0 (blocked by policy)

## Executive summary

- Preflight refreshed: **19 open PRs** org-wide; merge queue tracks **9** ranked PRs (li-demo#7 → roadmap#12).
- **0 PRs closed** — all **9** hygiene close candidates have `safe_now: false`; no abandoned drafts confirmed.
- **11 alignment comments** posted this pass (benchmarks#44–#47; lic#68–#73; li-demo#7); **4** from earlier today retained (#32, #34, #39, #42–#43, roadmap#12).
- **benchmarks#32** superseded by **#34** (100% overlap) — defer close until #34 merges; both commented.
- **4 CI-green PRs** ready for human review: benchmarks#47, lic#69, roadmap#12 (+ li-demo#7 sandbox skip).
- **lic#70** (#73 rank 8) strict contracts **E0303** — aligned, provable pillar; Windows CI may still be running.
- **3 lic drafts** (#68–#72) and **benchmarks drafts #44–#46** active today — not closed.
- **local_ci_results:** null — no local-ci substitute for GHA `none` on benchmarks#32/#34/#39.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| benchmarks#32 | **Deferred** | Close after #34 merges (`safe_now: false`; in merge_order) |
| benchmarks#42–#46 | **Deferred** | Draft PRs active 2026-05-20 — not abandoned |
| lic#68 | **Deferred** | Superseded by lic#69 — close after #69 merges |
| lic#71, #72 | **Deferred** | Active drafts — needs plan, not abandoned |

**Closes this run:** none

### Per-PR alignment (8 merge-order PRs)

| PR | Verdict | Notes |
|----|---------|-------|
| [li-demo#7](https://github.com/li-langverse/li-demo/pull/7) | aligned (sandbox) | Agent smoke; pr-program skip unless human asks |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | wait for dependency | Superseded by #34; GHA `none` |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | aligned | Security CWE audit fix; merge before closing #32 |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | aligned | Org sweep exclusion chore |
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | aligned | PH-5b/PH-7e numerics study; CI pass |
| [lic#69](https://github.com/li-langverse/lic/pull/69) | aligned | Workspace import + multiline def; CI pass |
| [lic#70](https://github.com/li-langverse/lic/pull/70) | aligned | E0303 strict ensures; G-lean pillar |
| [lic#73](https://github.com/li-langverse/lic/pull/73) | aligned | MIR object field access; CI pass |

**Additional reviewed (outside 8-cap or drafts):**

| PR | Verdict | Notes |
|----|---------|-------|
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | aligned | CI pass; governance repo — human merge |
| [benchmarks#42–#43](https://github.com/li-langverse/benchmarks/pull/42) | aligned (draft) | CI ingest / PH-IO samples — #43 blocked on lic#13 |
| [benchmarks#44–#46](https://github.com/li-langverse/benchmarks/pull/44) | wait for dependency | Language docs / HTTP visuals / RCA — active drafts |
| [lic#68](https://github.com/li-langverse/lic/pull/68) | close as superseded (defer) | After #69 merges |
| [lic#71](https://github.com/li-langverse/lic/pull/71) | needs plan | Scalar precision types without plan-approved |
| [lic#72](https://github.com/li-langverse/lic/pull/72) | needs plan | Phase H feature; CI fail; link lic#18/#30 |

### Labels

- Did not add `merge-approved` (pr-review-agent only).
- `plan-needed` on lic#71/#72: label exists in lic — add via issue planner if authors mark ready.

### Local CI

- No `local_ci_results` in briefing — benchmarks#32/#34/#39 still need GHA or `local-ci-sweep`.

### Control plane

- Prior `pr_alignment` runs today: 4 error + 1 finished before this pass; this run completes comments + digest.

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human review benchmarks#47 for merge-approved | benchmarks | — |
| Human review lic#69, #70, #73 for merge-approved | lic | — |
| Human review roadmap#12 (governance merge) | roadmap | — |
| Add `plan-approved` + issue link for lic#71 scalar types | lic | plan-needed, feature |
| Link lic#18/#30 on lic#72 before ready-for-review | lic | plan-needed, master-plan-gap |
| Run local-ci-sweep for benchmarks#32, #34, #39 | benchmarks | — |
| Close lic#68 after lic#69 merges | lic | superseded |
| Close benchmarks#32 after benchmarks#34 merges | benchmarks | superseded |

## Deferred

- Close **benchmarks#32** after **#34** merges.
- Close **lic#68** after **lic#69** merges.
- **59 branches** without open PRs — pr_branch_opener agent.
- **22 issues** with `plan-needed` — issue_planner agent.
- **li-language#6** (CI fail, needs plan) — prior pass; not in merge_order top 9.
- **li-demo#7** merge — operator confirmation only (automation sandbox).
