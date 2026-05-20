# PR alignment agent digest — 2026-05-20 (19:47Z)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`, `issue-feature-triage.py` (refreshed)  
**Org:** li-langverse · vision: proof → easy → fast  
**Merges performed:** 0 (policy)

## Executive summary

- Preflight refreshed: **20 open PRs** org-wide; merge queue ranks **6** (benchmarks#32, #34, #39, #47; lic#85; roadmap#12).
- **0 PRs closed** — `prs_safe_close_now: 0`; **benchmarks#32** deferred until **#34** merges (100% overlap, still open).
- **1 new alignment comment** this pass (**benchmarks#50**); prior pass already commented **#32, #34, #39, #42, #43, #47, #12, li-language#6/#8**.
- **2 CI-green** non-draft PRs: **benchmarks#47** (numerics docs), **roadmap#12** (ecosystem stats) — await human review + `merge-approved`; roadmap requires governance merge.
- **benchmarks#34** supersedes **#32** — verdict **wait for dependency** on #32; **aligned** on #34 (security CWE preflight).
- **lic#85** horner DCE fix — aligned with PH-5b/PH-7e; CI red; no local-ci pass in briefing.
- **13 PRs** flagged `prs_recommended_close` (drafts + redundant #32); all `safe_now: false`.
- **65 branches** without open PR — defer to `pr_branch_opener`.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) merges (`safe_now: false`, in merge_order) |
| benchmarks#42–#46, #48–#50 | **Deferred** | Draft PRs updated 2026-05-20 — active tier-5/CI work, not abandoned |
| lic#81, #84, #87, #101 | **Deferred** | Draft PRs — confirm abandoned before close |

**Closes this run:** none

### Per-PR alignment (8 reviewed)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | aligned | Numerics researcher pass (PH-5b); CI green; docs-only |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | aligned | Ecosystem stats on dev overview; CI green; human merge |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | aligned | Security CWE audit script; supersedes #32 |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | wait for dependency | Superseded by #34 — close after #34 merges |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | aligned | Exclude li-cursor-agents from org sweeps (chore) |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | aligned | Horner pure-Li DCE guard (PH-5b); fix CI before review |
| [li-language#6](https://github.com/li-langverse/li-language/pull/6) | needs plan | Tier-2 gaming physics in wrong repo tier; CI fail |
| [benchmarks#50](https://github.com/li-langverse/benchmarks/pull/50) | needs plan | Tier-5 multi-oracle draft; CI fail; coordinate with #46/#49 |

### Labels

- Did **not** add `merge-approved` (pr-review-agent only).
- `plan-needed` already on benchmarks#49, lic#87, lic#101; li-language repo lacks label for #6 (noted prior run).

### Local CI

- `local_ci_results`: null — GHA `none`/`fail` PRs need `local-ci-sweep` or supervisor with `LI_LOCAL_CI_POST_PR_COMMENTS`.

### Control plane

- Recent `pr_alignment` runs: mostly `finished`; one `error` at 18:15Z (SDK). This run completes digest + #50 comment.

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human review + `merge-approved` for numerics docs | benchmarks | — ([PR #47](https://github.com/li-langverse/benchmarks/pull/47)) |
| Human review roadmap ecosystem stats | roadmap | — ([PR #12](https://github.com/li-langverse/roadmap/pull/12)) |
| plan-needed: tier-2 gaming physics → lic/benchmarks catalog | lic or benchmarks | plan-needed, feature |
| plan-needed: tier-5 HTTP oracle + exploit harness | benchmarks | plan-needed, feature |
| Run local-ci-sweep for benchmarks#32, #34, #39 | benchmarks | — |
| Fix CI on lic#85 horner bench PR | lic | bug |
| Close benchmarks#32 after #34 merges | benchmarks | — (supersede) |

## Deferred

- Close **benchmarks#32** after **#34** merges.
- Draft tier-5 stack **#46, #48, #49** and lic httpd drafts **#81, #84, #87, #101** — not abandoned.
- **li-language#8** workspace sweep — title aligned but verify diff before merge.
- **65 branches** without PRs — `pr_branch_opener`.
- **23 issues** `plan-needed` — `issue_planner`.
