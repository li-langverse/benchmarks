# PR alignment agent digest — 2026-05-20 (17:15Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`, `issue-feature-triage.py` (refreshed 17:11–17:14Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight refreshed: **14** PRs in merge-order queue; **27** open org-wide (`pr-program`); **0** `merge-approved` / **0** in `merge_sequence`.
- **0 PRs closed** — `prs_safe_close_now: 0`; hygiene lists **12** draft/duplicate candidates (all `safe_now: false`).
- **3 new alignment comments** this pass: [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32#issuecomment-4500810815), [lic#94](https://github.com/li-langverse/lic/pull/94#issuecomment-4500810945), [lic#101](https://github.com/li-langverse/lic/pull/101#issuecomment-4500811075); added `plan-needed` on **lic#101**.
- **Horner sextet** (#80/#82/#85/#91/#94/#98): 100% overlap — **#85** canonical (CI pass); **#94** and **#98** superseded; **#91** broader numerics pass if single merge preferred.
- **Redundant:** [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) ⊂ [#34](https://github.com/li-langverse/benchmarks/pull/34) — defer close until #34 merges (both still open).
- **New draft:** [lic#101](https://github.com/li-langverse/lic/pull/101) (agent-first GUI) — needs plan before promotion.
- **56** branches without open PR — route to `pr_branch_opener`.
- Control plane: latest `pr_alignment` run `pr_alignment-1779295721441` finished 16:54Z.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges (`safe_now: false`); comment posted |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **Deferred** | Superseded by #85 — prior pass comment |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | **Deferred** | Superseded by #85 |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **Deferred** | Superseded by #85; comment posted |
| [lic#98](https://github.com/li-langverse/lic/pull/98) | **Deferred** | Duplicate; CI fail; prior pass comment |
| [lic#81](https://github.com/li-langverse/lic/pull/81) | **Deferred** | Draft World Studio — confirm abandoned |
| [lic#84](https://github.com/li-langverse/lic/pull/84) | **Deferred** | Draft httpd perf — confirm abandoned |
| [lic#87](https://github.com/li-langverse/lic/pull/87) | **Deferred** | Draft M1 wave 1 — has `plan-needed` |
| [lic#101](https://github.com/li-langverse/lic/pull/101) | **Deferred** | Draft GUI — `plan-needed` added; confirm intent |
| [benchmarks#42–#49](https://github.com/li-langverse/benchmarks/pull/48) | **Deferred** | Draft cluster — confirm intent |

**Closes this run:** 0

### Per-PR alignment (8 reviewed)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | **aligned** | PH-5b/PH-7e numerics docs; CI pass; ready for `pr-review-agent` |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | **aligned** | Security CWE preflight; supersedes #32; GHA `none` |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **wait for dependency** | Close after #34 merges |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | **aligned** | Org sweep exclude li-cursor-agents; GHA `none` |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | **aligned** | **Canonical** horner DCE fix; CI pass |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **close as superseded** | 100% overlap; use #85 or #91 |
| [lic#98](https://github.com/li-langverse/lic/pull/98) | **close as superseded** | 100% overlap; CI fail on build-and-test |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | **aligned** | Ecosystem stats docs; governance — human merge only |

**Also noted (prior pass):** lic#91 (broader numerics), lic#80/#82 (superseded), li-demo#7–#9 (sandbox), benchmarks#49 (`plan-needed`).

### Labels

- Did **not** add `merge-approved` (pr-review-agent only).
- Added **`plan-needed`** on [lic#101](https://github.com/li-langverse/lic/pull/101) (feature draft without plan).

### Local CI

- Briefing `local_ci_results`: null — run `local-ci-sweep` for benchmarks#32/#34/#39 and lic#91 when gate needs local-ci for GHA `none`.

### Control plane

- Recent `pr_alignment` runs: `pr_alignment-1779295721441` (16:48Z **finished**), `pr_alignment-1779294589420` (16:29Z **finished**).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human: keep **lic#85**, close **#80/#82/#94/#98** (horner DCE guard) | lic | — |
| Human review **benchmarks#47** for `merge-approved` | benchmarks | — |
| Human review **roadmap#12** (governance merge) | roadmap | — |
| Human: pick one **li-demo** PR among #7/#8/#9; close others | li-demo | — |
| Merge **benchmarks#34** then close **#32** | benchmarks | — |
| Plan **lic#101** (agent-first GUI) before undraft | lic | `plan-needed` |
| Plan **lic#87** / **benchmarks#49** before promoting drafts | lic, benchmarks | `plan-needed` |
| Confirm draft intent: **lic#81/#84**, **benchmarks#42–#48** | lic, benchmarks | — |
| Add **ci.yml** on **li-local-ci** main | li-local-ci | `ci` |

## Deferred

- All **12** `prs_recommended_close` rows (`safe_now: false`).
- **lic#98** CI fix vs close-as-superseded (human pick).
- **li-language#6** failing GHA (ci_bug_triage queue).
- **19** redundant horner/li-demo pairs — human pick-one.
- **56** orphan branches → `pr_branch_opener`.
- **22** issues still `plan-needed` (issue-feature-triage).
