# PR alignment agent digest — 2026-05-20 (17:37Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py` (refreshed 17:33–17:37Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight refreshed: **14** PRs in merge-order queue; **27** open org-wide (`pr-program`); **0** `merge-approved` / **0** in `merge_sequence`.
- **0 PRs closed** — `prs_safe_close_now: 0`; all **12** hygiene close candidates remain `safe_now: false`.
- **4 new alignment comments** this pass: [lic#80](https://github.com/li-langverse/lic/pull/80#issuecomment-4500969352), [lic#82](https://github.com/li-langverse/lic/pull/82#issuecomment-4500969487), [lic#91](https://github.com/li-langverse/lic/pull/91#issuecomment-4500969625), [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32#issuecomment-4500969775).
- **Horner sextet** (#80/#82/#85/#91/#94/#98): **#85** canonical (CI pass); **#91** alternative if broader numerics pass preferred; **#94/#98** superseded; **#80/#82** close-as-superseded comments added.
- **benchmarks#32** ⊂ **#34** — both still open; defer close until #34 merges.
- **56** orphan branches without PR — route to `pr_branch_opener`.
- **local_ci_results:** null — sweep needed for GHA `none` PRs (#32/#34/#39, lic#91).
- Control plane: prior `pr_alignment-1779297066959` finished 17:11Z.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges; comment refreshed |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **Deferred** | Superseded by #85 — close comment posted |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | **Deferred** | Superseded by #85 — close comment posted |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **Deferred** | Superseded by #85 (prior pass comment) |
| [lic#98](https://github.com/li-langverse/lic/pull/98) | **Deferred** | Duplicate + CI fail (prior pass comment) |
| [lic#81/#84/#87/#101](https://github.com/li-langverse/lic/pull/101) | **Deferred** | Draft — confirm abandoned |
| [benchmarks#42–#49](https://github.com/li-langverse/benchmarks/pull/49) | **Deferred** | Draft cluster — #49 has `plan-needed` |

**Closes this run:** 0

### Per-PR alignment (8 reviewed)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | **aligned** | PH-5b/PH-7e numerics docs; CI pass; prior comment stands |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | **aligned** | Security CWE preflight; supersedes #32; GHA `none` |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **wait for dependency** | Close after #34 merges — comment refreshed |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | **aligned** | Org sweep exclude li-cursor-agents; GHA `none` |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | **aligned** | **Canonical** horner DCE fix; CI pass |
| [lic#91](https://github.com/li-langverse/lic/pull/91) | **aligned** or **superseded** | Broader numerics pass; human pick vs #85 — comment refreshed |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **close as superseded** | 100% overlap; CI fail |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | **aligned** | Ecosystem stats; governance — human merge only |

**Also noted:** lic#80/#82 (superseded comments this pass), lic#98 (superseded), li-demo#7–#9 (sandbox skip), benchmarks#49 (`plan-needed` draft).

### Labels

- Did **not** add `merge-approved` (pr-review-agent only).
- **`plan-needed`** already on lic#101, benchmarks#49, lic#87 (no changes this pass).

### Local CI

- Briefing `local_ci_results`: null — run `python3 scripts/local-ci-sweep.py` for benchmarks#32/#34/#39 and lic#91 when gate needs local-ci for GHA `none`.

### Control plane

- Recent `pr_alignment` runs: `pr_alignment-1779297066959` (17:11Z **finished**), `pr_alignment-1779295721441` (16:48Z **finished**).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human: keep **lic#85**, close **#80/#82/#94/#98** (horner DCE guard) | lic | — |
| Or merge **lic#91** once for docs+fix, close other horner PRs | lic | — |
| Human review **benchmarks#47** for `merge-approved` | benchmarks | — |
| Human review **roadmap#12** (governance merge) | roadmap | — |
| Merge **benchmarks#34** then close **#32** | benchmarks | — |
| Human: pick one **li-demo** PR among #7/#8/#9 | li-demo | — |
| Plan **lic#101** before undraft | lic | `plan-needed` |
| Plan **lic#87** / **benchmarks#49** before promoting drafts | lic, benchmarks | `plan-needed` |
| Add **ci.yml** on **li-local-ci** main | li-local-ci | `ci` |

## Deferred

- All **12** `prs_recommended_close` rows (`safe_now: false`).
- **lic#98** CI fix vs close-as-superseded (human pick).
- **li-language#6** failing GHA.
- **19** redundant horner/li-demo pairs.
- **56** orphan branches → `pr_branch_opener`.
- **22** issues still `plan-needed` (issue-feature-triage).
