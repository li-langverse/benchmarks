# PR alignment agent digest — 2026-05-20 (20:02Z)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`, `issue-feature-triage.py` (refreshed 20:02Z)  
**Org:** li-langverse · vision: proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (policy)

## Executive summary

- Preflight refreshed: **23 open PRs** org-wide (`run-pr-program`); merge queue ranks **8** active PRs (benchmarks#32, #34, #39, #47; lic#85, #122, #123; roadmap#12).
- **0 PRs closed** — `prs_safe_close_now: 0`; all 14 hygiene close candidates are drafts or dependency-blocked (`safe_now: false`).
- **8 alignment comments** posted this pass (merge-queue set); none had prior `PR alignment (agent)` comments.
- **2 CI-green** non-draft PRs per program: **benchmarks#47**, **roadmap#12** — await human review + `merge-approved` (not added by this agent).
- **benchmarks#34** supersedes **#32** — #32 verdict **wait for dependency**; close #32 only after #34 merges.
- **lic horner triplet** (#85, #122, #123): 100% file overlap — human must pick one fix PR; #123 noted **close as superseded** after pick.
- **14 draft PRs** flagged for close review — deferred (not abandoned; tier-5/httpd/studio work in flight).
- **63 branches** without open PR — defer to `pr_branch_opener`.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | `safe_now: false`; in `merge_order` rank 1; close after [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) merges |
| [benchmarks#42](https://github.com/li-langverse/benchmarks/pull/42)–[#50](https://github.com/li-langverse/benchmarks/pull/50) (drafts) | **Deferred** | Confirm abandoned before close — active tier-5/CI/httpd stack |
| [lic#81](https://github.com/li-langverse/lic/pull/81), [#84](https://github.com/li-langverse/lic/pull/84), [#87](https://github.com/li-langverse/lic/pull/87), [#101](https://github.com/li-langverse/lic/pull/101) | **Deferred** | Draft PRs — World Studio / httpd / GUI; not superseded without human sign-off |

**Closes this run:** none (0/5 cap used)

### Per-PR alignment (8 reviewed)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | **aligned** | PH-5b numerics docs; CI green; top review candidate |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | **aligned** | Ecosystem stats; CI green; governance human merge only |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | **aligned** | Security CWE preflight; supersedes #32 |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | **aligned** | Exclude li-cursor-agents from org sweeps |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **wait for dependency** | Superseded by #34 — do not merge |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | **aligned** (dedup pending) | Horner DCE fix; CI fail; overlaps #122/#123 |
| [lic#122](https://github.com/li-langverse/lic/pull/122) | **wait for dependency** | Docs + test fix; overlap with #85/#123 |
| [lic#123](https://github.com/li-langverse/lic/pull/123) | **close as superseded** (after human pick) | Newest duplicate of #85 fix path |

### Labels

- Did **not** add `merge-approved` (pr-review-agent only).
- No new `plan-needed` labels on merge-queue set (chore/docs/security scope).

### Local CI

- `local_ci_results`: null in briefing — PRs with GHA `none`/`fail` need `python3 scripts/local-ci-sweep.py` or supervisor with `LI_LOCAL_CI_POST_PR_COMMENTS`.

### Control plane

- Recent `pr_alignment` runs: **finished** (19:17Z–19:44Z). This pass: digest + 8 GitHub comments.

### Comment log

| PR | Comment URL |
|----|-------------|
| benchmarks#32 | https://github.com/li-langverse/benchmarks/pull/32#issuecomment-4502182183 |
| benchmarks#34 | https://github.com/li-langverse/benchmarks/pull/34#issuecomment-4502182386 |
| benchmarks#39 | https://github.com/li-langverse/benchmarks/pull/39#issuecomment-4502182535 |
| benchmarks#47 | https://github.com/li-langverse/benchmarks/pull/47#issuecomment-4502182722 |
| lic#85 | https://github.com/li-langverse/lic/pull/85#issuecomment-4502182950 |
| lic#122 | https://github.com/li-langverse/lic/pull/122#issuecomment-4502183198 |
| lic#123 | https://github.com/li-langverse/lic/pull/123#issuecomment-4502183398 |
| roadmap#12 | https://github.com/li-langverse/roadmap/pull/12#issuecomment-4502183569 |

## Recommended issues/PRs

| Title | Repo | Labels / action |
|-------|------|-----------------|
| Human review + `merge-approved` for numerics docs | benchmarks | — ([PR #47](https://github.com/li-langverse/benchmarks/pull/47)) |
| Human review roadmap ecosystem stats | roadmap | governance merge ([PR #12](https://github.com/li-langverse/roadmap/pull/12)) |
| Pick canonical lic horner PR (#85 vs #122 vs #123) | lic | close superseded two after merge |
| Merge benchmarks#34 then close #32 | benchmarks | supersede hygiene |
| Run local-ci-sweep for benchmarks#32, #34, #39 | benchmarks | CI `none` |
| Fix CI on chosen lic horner PR | lic | bug / bench |
| plan-needed: tier-2 gaming physics → lic catalog | lic | plan-needed ([issue triage](https://github.com/li-langverse/lic/issues)) |
| plan-needed: tier-5 HTTP oracle harness | benchmarks | plan-needed (#49 has label) |

## Deferred

- Close **benchmarks#32** after **#34** merges.
- Resolve **lic#85 / #122 / #123** duplicate stack before any merge-approved.
- **14 draft PRs** (benchmarks tier-5, lic httpd/studio) — confirm abandoned with author before close.
- **63 branches** without PRs — `pr_branch_opener`.
- **22 issues** `plan-needed` — `issue_planner` automation.
- **li-language#6** CI fail — `bug_fixer` (outside 8-PR cap this pass).
