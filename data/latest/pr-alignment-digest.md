# PR alignment agent digest — 2026-05-20

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`, `issue-feature-triage.py`  
**Org:** li-langverse  
**Merges performed:** 0 (blocked by policy)

## Executive summary

- Preflight refreshed: **11 open PRs** org-wide; merge queue tracks **4** (benchmarks#32, #34, #39; roadmap#12).
- **0 PRs closed** — all 6 hygiene close candidates have `safe_now: false`; no abandoned drafts confirmed.
- **8 alignment comments** posted (benchmarks#32, #34, #39, #42, #43; roadmap#12; li-language#6, #8).
- **benchmarks#32** superseded by **#34** (100% overlap) — defer close until #34 merges; commented on both.
- **roadmap#12** only CI-green PR — aligned; awaits human review + `merge-approved` (governance repo).
- **li-language#6** CI fail (Windows) + feature scope — verdict **needs plan**; `plan-needed` label unavailable in repo.
- **li-language#8** title/body mismatch (workspace sweep + unrelated docs) — needs split or rebase.
- Draft benchmarks PRs **#42–#46** active today — **not closed**; #42–#43 reviewed in this pass.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| benchmarks#32 | **Deferred** | Close after #34 merges (`safe_now: false`) |
| benchmarks#42–#46 | **Deferred** | Draft PRs updated 2026-05-20 — not abandoned |

**Closes this run:** none

### Per-PR alignment (8 reviewed)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | aligned | Security CWE audit fix; supersedes #32 |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | aligned | CI pass; human merge required |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | aligned | Org sweep exclusion chore |
| [benchmarks#42](https://github.com/li-langverse/benchmarks/pull/42) | aligned (draft) | ingest-lis CI fix; mark ready when green |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | wait for dependency | Superseded by #34 |
| [benchmarks#43](https://github.com/li-langverse/benchmarks/pull/43) | wait for dependency | Blocked on lic#13 (PH-IO std modules) |
| [li-language#6](https://github.com/li-langverse/li-language/pull/6) | needs plan | CI fail; tier-2 feature without plan |
| [li-language#8](https://github.com/li-langverse/li-language/pull/8) | needs plan | Title/body mismatch; mixed commits |

### Labels

- Attempted `plan-needed` on li-language#6 — label not defined in repo (create label or use issue linkage).

### Local CI

- `local_ci_results`: null — no local-ci pass to reference for GHA `none` PRs.

### Control plane

- Prior `pr_alignment` runs today: 5 rows, all `status: error` (this run completes digest + comments).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Create `plan-needed` label in li-language | li-language | chore |
| plan-needed: tier-2 gaming physics in correct repo tier | benchmarks or lic | plan-needed, feature |
| plan-needed: PH-IO std modules before sample merge | lic | plan-needed, feature (lic#13) |
| Run local-ci-sweep for benchmarks#32, #34, #39 | benchmarks | — |
| Fix Windows CI on li-language#6 | li-language | bug |
| Human review roadmap#12 for merge-approved | roadmap | — |

## Deferred

- Close **benchmarks#32** after **#34** merges.
- Review draft **benchmarks#44–#46** (not in 8-PR cap this run): #44 language docs sketch, #45 HTTP tier-5 plots, #46 li-httpd vs nginx RCA — all active drafts.
- **63 branches** without open PRs (`pr_branch_hygiene.branches_needing_pr`) — pr_branch_opener agent.
- **22 issues** with `plan-needed` — issue_planner agent.
- **li-language#6** Windows CI fix — bug_fixer agent.
