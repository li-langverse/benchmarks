# PR alignment agent digest — 2026-05-20 (19:34Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py` (refreshed 19:31–19:33Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight refreshed **19:33Z**: **6** PRs in `merge_order`; **0** `merge-approved` / **0** in `merge_sequence`; **20** open org-wide (`pr-program`).
- **0 PRs closed** this pass — `prs_safe_close_now: 0`; all 13 hygiene close candidates are draft or dependency-blocked.
- **benchmarks#34** still **OPEN** — [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) remains open; close #32 **after #34 merges** only.
- **CI-green merge candidates:** [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47), [roadmap#12](https://github.com/li-langverse/roadmap/pull/12); lic#85 **not** green (GHA fail on 3 jobs).
- **Horner stack:** lic#85 canonical; duplicates #80/#82/#91/#94/#98 closed in earlier pass (19:03Z).
- **Draft PRs** (lic#81/#84/#87/#101, benchmarks#42–#50) updated today — **not** abandoned; defer close until human confirms.
- **benchmarks#32/#34/#39:** GHA checks `none` on branch — consider `local-ci-sweep` when gate requires green.
- **64** orphan branches without PR — route to `pr_branch_opener`.
- Control-plane: prior `pr_alignment` runs **finished** (latest `pr_alignment-1779304639396` at 19:17Z).

## Deliverable / findings

### Close hygiene (max 5) — **0 closed this pass**

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | `safe_now: false`; #34 not merged; in `merge_order` rank 1 |
| [lic#101/#87/#84/#81](https://github.com/li-langverse/lic/pull/101) | **Deferred** | Draft — updated 2026-05-20 (15:11–17:16Z); active work |
| [benchmarks#42–#50](https://github.com/li-langverse/benchmarks/pull/50) | **Deferred** | Draft cluster; #49 has `plan-needed`; #50 updated 18:24Z |

### Prior-pass closes (19:03Z — audit trail)

| PR | Action | Reason |
|----|--------|--------|
| lic#98, #94, #91, #80, #82 | **Closed** | Superseded by lic#85 (horner DCE fix) |

### Per-PR alignment (8 reviewed)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | **aligned** | PH-5b/PH-7e numerics docs; CI pass (`dashboard-build`, `ingest-smoke`) |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | **aligned** | Security CWE preflight; supersedes #32; GHA `none` |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | **aligned** | Org sweep exclude li-cursor-agents; GHA `none` |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **wait for dependency** | Close after #34 merges; pass comment 19:34Z |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | **wait for dependency** | Canonical horner fix; CI **FAIL** — pass comment 19:34Z |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | **aligned** | Governance docs; CI pass; human merge only |
| [lic#101](https://github.com/li-langverse/lic/pull/101) | **needs plan** | Draft GUI/studio; `plan-needed`; 74 commits |
| [lic#87](https://github.com/li-langverse/lic/pull/87) | **needs plan** | Draft PH-H httpd M1; `plan-needed`; depends #84 |

### Labels

- Did **not** add `merge-approved` (pr-review-agent only).
- Retained **`plan-needed`** on lic#101, lic#87, benchmarks#49.

### Local CI

- Briefing `local_ci_results`: null — run `python3 scripts/local-ci-sweep.py --repo benchmarks --pr 34` (and 32, 39) when `LI_LOCAL_CI_POST_PR_COMMENTS=1`.

### Merge queue snapshot

Vision order: package CI / mirrors → benchmarks → lic → lip/lit/lis → roadmap.

Top CI-green (awaiting `merge-approved`): **benchmarks#47** → **roadmap#12**.

Redundant: benchmarks#34 ⊃ #32 (close #32 after #34).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human review **benchmarks#47** → `merge-approved` | benchmarks | — |
| Fix CI on **lic#85** then review → `merge-approved` | lic | — |
| Merge **benchmarks#34** then close **#32** | benchmarks | — |
| Human merge **roadmap#12** (governance) | roadmap | — |
| Confirm abandon or promote **lic#101/#87** drafts | lic | `plan-needed` |
| Run **local-ci-sweep** for benchmarks#32/#34/#39 | benchmarks | — |
| Route **bug_fixer** to lic#85 CI failures | lic | — |

## Deferred

- Close **benchmarks#32** until **benchmarks#34** merges.
- Close draft PRs until human confirms abandoned (all touched today).
- **roadmap#12** — no agent merge (`ALLOW_GOVERNANCE_MERGE` unset).
- **64** orphan branches — `pr_branch_opener`.
- **merge-approved** labeling — `pr_reviewer` after alignment + CI green.
