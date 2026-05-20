# PR alignment agent digest — 2026-05-20 (16:55Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`, `issue-feature-triage.py` (refreshed 16:51–16:52Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight refreshed: **14** PRs in merge-order queue; **26** open org-wide (`pr-program`); **0** `merge-approved` / **0** in `merge_sequence`.
- **0 PRs closed** — `prs_safe_close_now: 0`; hygiene lists **11** draft/duplicate candidates (all `safe_now: false`).
- **1 new alignment comment** this pass: [lic#98](https://github.com/li-langverse/lic/pull/98#issuecomment-4500652687) (new horner duplicate, CI fail → superseded by #85).
- **Horner sextet** (#80/#82/#85/#91/#94/#98): 100% overlap — **#85** recommended canonical (CI pass); **#98** and **#94** superseded + CI fail on #98.
- **Redundant:** [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) ⊂ [#34](https://github.com/li-langverse/benchmarks/pull/34) — defer close until #34 merges (both still open).
- **lic#92** already **merged** (16:49Z) — removed from hygiene close list; no action.
- **56** branches without open PR — route to `pr_branch_opener`.
- Control plane: `pr_alignment-1779294589420` finished 16:29Z; this pass records digest only.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges (`safe_now: false`) |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **Deferred** | Superseded by #85 — human close |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | **Deferred** | Superseded by #85 |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **Deferred** | Superseded by #85; CI fail |
| [lic#98](https://github.com/li-langverse/lic/pull/98) | **Deferred** | New duplicate; CI fail; comment posted |
| [lic#81](https://github.com/li-langverse/lic/pull/81) | **Deferred** | Draft World Studio — confirm abandoned |
| [lic#84](https://github.com/li-langverse/lic/pull/84) | **Deferred** | Draft httpd perf — confirm abandoned |
| [lic#87](https://github.com/li-langverse/lic/pull/87) | **Deferred** | Draft M1 wave 1 — has `plan-needed` |
| [benchmarks#42–#49](https://github.com/li-langverse/benchmarks/pull/48) | **Deferred** | Draft cluster — confirm intent |

**Closes this run:** 0

### Per-PR alignment (8 reviewed — merge-order ranks 7–14 + lic#98)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | **aligned** | PH-5b/PH-7e numerics docs; CI pass; ready for `pr-review-agent` |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | **aligned** | Security CWE preflight; supersedes #32; GHA `none` |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **wait for dependency** | Close after #34 merges |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | **aligned** | Org sweep exclude li-cursor-agents; GHA `none` |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | **aligned** | **Canonical** horner DCE fix; CI pass; pick over siblings |
| [lic#98](https://github.com/li-langverse/lic/pull/98) | **close as superseded** | 100% overlap; CI fail; use #85 |
| [lic#91](https://github.com/li-langverse/lic/pull/91) | **aligned** (pick one) | Broader numerics + bench; overlaps horner set; GHA `none` |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | **aligned** | Ecosystem stats docs; governance — human merge only |

**Prior pass coverage (unchanged):** li-demo#7–#9, lic#80/#82/#94, benchmarks#49, lic#87.

### Labels

- Did **not** add `merge-approved` (pr-review-agent only).
- No new labels this pass (`plan-needed` already on lic#87, benchmarks#49 from prior pass).

### Local CI

- Briefing `local_ci_results`: null — run `local-ci-sweep` for benchmarks#32/#34/#39 and lic#91 when gate needs local-ci for GHA `none`.

### Control plane

- Recent `pr_alignment` runs: `pr_alignment-1779294589420` (16:29Z **finished**), `pr_alignment-1779293372481` (16:09Z **finished**).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human: keep **lic#85**, close **#80/#82/#94/#98** (horner DCE guard) | lic | — |
| Human review **benchmarks#47** for `merge-approved` | benchmarks | — |
| Human review **roadmap#12** (governance merge) | roadmap | — |
| Human: pick one **li-demo** PR among #7/#8/#9; close others | li-demo | — |
| Merge **benchmarks#34** then close **#32** | benchmarks | — |
| Fix CI on **lic#98** or close; fix **li-language#6** | lic, li-language | `bug` |
| Plan **lic#87** / **benchmarks#49** before promoting drafts | lic, benchmarks | `plan-needed` |
| Confirm draft intent: **lic#81/#84**, **benchmarks#42–#48** | lic, benchmarks | — |
| Add **ci.yml** on **li-local-ci** main | li-local-ci | `ci` |

## Deferred

- All `safe_now: false` hygiene closes (11 PRs).
- benchmarks#32 close until #34 merges.
- Horner duplicate human pick (#85 vs #98 author claim).
- 56 orphan branches → `pr_branch_opener`.
- 22 issues with `plan-needed` → `issue-feature-planner`.
- `merge-approved` labeling → `pr-review-agent` only.
