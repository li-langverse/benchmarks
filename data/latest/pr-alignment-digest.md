# PR alignment agent digest — 2026-05-20 (19:20Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`, `issue-feature-triage.py` (refreshed 19:17–19:19Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight at **19:19Z**: **6** PRs in merge-order queue; **0** `merge-approved` / **0** in `merge_sequence`; **20** open org-wide (`pr-program`).
- **0 PRs closed** this pass — `prs_safe_close_now: 0`; all hygiene candidates are draft or dependency-blocked.
- **Earlier today (19:03Z pass):** **5** horner duplicates closed (lic#80/#82/#91/#94/#98); canonical **lic#85** retained.
- **8 alignment comments** from 19:03Z pass still current; **1 follow-up** posted on **lic#85** — GHA `build-and-test` regressed to **FAIL**.
- **benchmarks#32** remains OPEN — close **after [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34)** merges (`safe_now: false`).
- **CI-green merge candidates:** [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47), [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) only (lic#85 dropped from green set).
- **23** issues `plan-needed`; **horner_pure_li** still red (~88× vs cpp) — docs on #47, harness fix blocked on lic#85 CI.
- **64** orphan branches without PR — route to `pr_branch_opener`.
- **local_ci_results:** null — benchmarks#32/#34/#39 have GHA `none` on branch; run `local-ci-sweep` if gate requires.

## Deliverable / findings

### Close hygiene (max 5) — **0 closed this pass**

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges — in `merge_order` rank 1; never close while redundant pair pending |
| [lic#101/#87/#84/#81](https://github.com/li-langverse/lic/pull/101) | **Deferred** | Draft — updated 2026-05-20; confirm abandon before close |
| [benchmarks#42–#50](https://github.com/li-langverse/benchmarks/pull/50) | **Deferred** | Draft cluster; #49 has `plan-needed` |

### Prior-pass closes (19:03Z — recorded for audit)

| PR | Action | Reason |
|----|--------|--------|
| [lic#98](https://github.com/li-langverse/lic/pull/98) | **Closed** | Superseded by lic#85 |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **Closed** | Superseded by lic#85 |
| [lic#91](https://github.com/li-langverse/lic/pull/91) | **Closed** | Superseded by lic#85 |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **Closed** | Duplicate of lic#85 |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | **Closed** | Duplicate of lic#85 |

### Per-PR alignment (8 reviewed — comments at 19:03Z + lic#85 follow-up 19:20Z)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | **aligned** | PH-5b/PH-7e numerics docs; CI pass |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | **aligned** | Security CWE preflight; supersedes #32; GHA `none` on branch |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | **aligned** | Org sweep exclude li-cursor-agents; GHA `none` |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **wait for dependency** | Close after #34 merges |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | **wait for dependency** | Canonical horner fix; **CI FAIL** (build-and-test, macos, registry-and-tier0) — bug_fixer |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | **aligned** | Governance — human merge only |
| [lic#101](https://github.com/li-langverse/lic/pull/101) | **needs plan** | Draft feature; `plan-needed`; updated 17:16Z |
| [lic#87](https://github.com/li-langverse/lic/pull/87) | **needs plan** | Draft PH-H httpd; `plan-needed`; updated 16:51Z |

### Labels

- Did **not** add `merge-approved` (pr-review-agent only).
- Retained **`plan-needed`** on lic#101, lic#87, benchmarks#49; no new labels added.

### Local CI

- Briefing `local_ci_results`: null — recommend `python3 scripts/local-ci-sweep.py --repo benchmarks --pr 34` (and 32, 39) when `LI_LOCAL_CI_POST_PR_COMMENTS=1`.

### Merge queue snapshot

Vision order: package CI / mirrors → benchmarks → lic → lip/lit/lis → roadmap.

Top CI-green (awaiting `merge-approved`): **benchmarks#47** → **roadmap#12**.

Redundant: benchmarks#34 ⊃ #32 (close #32 after #34).

Horner stack: lic#85 canonical (duplicates closed).

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
- Close draft PRs (lic#81/#84/#87/#101, benchmarks#42–#50) until human confirms abandoned.
- **roadmap#12** — no agent merge (`ALLOW_GOVERNANCE_MERGE` unset).
- **li-demo** maintainer PRs — automation sandbox (skip unless user asks).
- **56→64** orphan branches — `pr_branch_opener` agent.
- **merge-approved** labeling — deferred to `pr_reviewer` after alignment + CI green.
