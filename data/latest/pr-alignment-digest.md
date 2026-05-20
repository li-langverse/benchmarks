# PR alignment agent digest — 2026-05-20 (19:00Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`, `issue-feature-triage.py` (refreshed 18:58–19:02Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight at **19:00Z**: **14** PRs in merge-order queue; **0** `merge-approved` / **0** in `merge_sequence`; **28** open org-wide (`pr-program`).
- **5 PRs closed** as superseded horner duplicates — canonical **[lic#85](https://github.com/li-langverse/lic/pull/85)** (CI green, PH-5b/PH-7e).
- **8 alignment comments** posted: benchmarks#47/#34/#39/#32, lic#85, li-demo#9, roadmap#12.
- **benchmarks#32** still OPEN — **wait for [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34)** before close (`safe_now: false`).
- **13** hygiene close candidates remain draft/deferred; **0** `prs_safe_close_now`.
- **22** issues `plan-needed`; **horner_pure_li** still red (~88× vs cpp) — compiler path via lic#85 + [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) docs.
- **local_ci_results:** null — GHA `none` on benchmarks#32/#34/#39; run `local-ci-sweep` if gate requires.
- **56** orphan branches without PR — route to `pr_branch_opener`.

## Deliverable / findings

### Close hygiene (max 5) — **5 closed**

| PR | Action | Reason |
|----|--------|--------|
| [lic#98](https://github.com/li-langverse/lic/pull/98) | **Closed** | Superseded by lic#85; CI fail; identical 8-file horner diff |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **Closed** | Superseded by lic#85; CI fail |
| [lic#91](https://github.com/li-langverse/lic/pull/91) | **Closed** | Superseded by lic#85; CI fail; numerics docs on benchmarks#47 |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **Closed** | CI-green duplicate of lic#85 |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | **Closed** | CI-green duplicate of lic#85 |

**Canonical horner PR:** [lic#85](https://github.com/li-langverse/lic/pull/85) — aligned; route to `pr-review-agent` (no `merge-approved` added here).

### Deferred closes

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close **after #34 merges** — branch fully contained in #34 |
| [lic#101/#87/#84/#81](https://github.com/li-langverse/lic/pull/101) | **Deferred** | Draft — updated 2026-05-20; confirm abandon before close |
| [benchmarks#42–#50](https://github.com/li-langverse/benchmarks/pull/50) | **Deferred** | Draft cluster; #49 has `plan-needed` |

### Per-PR alignment (8 reviewed)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | **aligned** | PH-5b/PH-7e numerics docs; CI pass |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | **aligned** | Security CWE preflight; supersedes #32; GHA `none` |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | **aligned** | Org sweep exclude li-cursor-agents; GHA `none` |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **wait for dependency** | Close after #34 merges |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | **aligned** | Canonical horner fix; CI green |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | **aligned** | Governance — human merge only |
| [li-demo#9](https://github.com/li-langverse/li-demo/pull/9) | **aligned** (sandbox) | Overlap with #7/#8 — human pick one |
| [li-demo#7/#8](https://github.com/li-langverse/li-demo/pull/7) | **aligned** (sandbox) | Prior pass; skip merge unless user asks |

### Labels

- Did **not** add `merge-approved` (pr-review-agent only).
- Retained existing **`plan-needed`** on lic#101, lic#87, benchmarks#49; no new labels.

### Local CI

- Briefing `local_ci_results`: null — recommend `python3 scripts/local-ci-sweep.py --repo benchmarks --pr 32` (and 34, 39) when `LI_LOCAL_CI_POST_PR_COMMENTS=1`.

### Merge queue snapshot

Vision order: package CI / mirrors → benchmarks → lic → lip/lit/lis → roadmap.

Top CI-green (awaiting `merge-approved`): benchmarks#47 → **lic#85** → roadmap#12.

Redundant: benchmarks#34⊃#32; li-demo#7/#8/#9 overlap.

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human review **lic#85** → `merge-approved` | lic | — |
| Human review **benchmarks#47** → `merge-approved` | benchmarks | — |
| Merge **benchmarks#34** then close **#32** | benchmarks | — |
| Human merge **roadmap#12** (governance) | roadmap | — |
| Human: pick one **li-demo** among #7/#8/#9 | li-demo | — |
| Plan before undraft: **lic#101**, **lic#87** | lic | `plan-needed` |
| Plan before undraft: **benchmarks#49** | benchmarks | `plan-needed` |
| Add **ci.yml** on **li-local-ci** main | li-local-ci | — |
| Run **issue-feature-planner** on 22 `plan-needed` issues | lic, benchmarks | `plan-needed` |

## Deferred

- **benchmarks#32** close until **#34** merges.
- All draft PR closes (lic#81/#84/#87/#101, benchmarks#42–#50) until human confirms abandoned.
- **roadmap#12** merge (governance gate).
- **local-ci-sweep** for GHA-missing benchmarks PRs.
- **56** branches without PRs (`pr_branch_opener`).
- **li-language#6** failing CI (outside merge-plan top 14).
