# PR alignment agent digest — 2026-05-20 (16:35Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py` (refreshed 16:31Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight refreshed: **13** PRs in merge-order queue; **26** open org-wide (`pr-program`); **0** `merge-approved` / **0** in `merge_sequence`.
- **0 PRs closed** — `prs_safe_close_now: 0`; hygiene lists **12** draft/duplicate candidates (all `safe_now: false`).
- **6 new alignment comments** this pass: [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39#issuecomment-4500501968), [#49](https://github.com/li-langverse/benchmarks/pull/49#issuecomment-4500502149), [li-demo#7–#9](https://github.com/li-langverse/li-demo/pull/7#issuecomment-4500502340), [lic#87](https://github.com/li-langverse/lic/pull/87#issuecomment-4500502796); prior pass already covered horner quad + benchmarks#32/#34/#47 + roadmap#12.
- **Horner quad** ([lic#80](https://github.com/li-langverse/lic/pull/80) / [#82](https://github.com/li-langverse/lic/pull/82) / [#85](https://github.com/li-langverse/lic/pull/85) / [#94](https://github.com/li-langverse/lic/pull/94)): 100% overlap — **#85** recommended canonical; **#94** superseded + CI fail.
- **Redundant:** [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) ⊂ [#34](https://github.com/li-langverse/benchmarks/pull/34) — defer close until #34 merges.
- **Labels added:** `plan-needed` on [lic#87](https://github.com/li-langverse/lic/pull/87), [benchmarks#49](https://github.com/li-langverse/benchmarks/pull/49) (draft feature work).
- **56** branches without open PR — route to `pr_branch_opener`.
- Control plane: prior `pr_alignment` runs today **finished** (16:09Z); no new run recorded for this pass.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges (`safe_now: false`) |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **Deferred** | Superseded by #85 — human close |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | **Deferred** | Superseded by #85 |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **Deferred** | Superseded by #85; CI fail |
| [lic#81](https://github.com/li-langverse/lic/pull/81) | **Deferred** | Draft World Studio — confirm abandoned |
| [lic#84](https://github.com/li-langverse/lic/pull/84) | **Deferred** | Draft httpd perf — confirm abandoned |
| [lic#87](https://github.com/li-langverse/lic/pull/87) | **Deferred** | Draft M1 wave 1 — comment + `plan-needed` added |
| [lic#92](https://github.com/li-langverse/lic/pull/92) | **Deferred** | Draft TOML loader — confirm abandoned |
| [benchmarks#42–#49](https://github.com/li-langverse/benchmarks/pull/48) | **Deferred** | Draft cluster — #49 new in hygiene |

**Closes this run:** 0

### Per-PR alignment (8 reviewed)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | **aligned** | PH-5b/PH-7e numerics docs; CI pass in program; ready for `pr-review-agent` |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | **aligned** | Security CWE preflight; supersedes #32; GHA `none` |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **wait for dependency** | Close after #34 merges |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | **aligned** | Canonical horner DCE fix; pick over #80/#82/#94 |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **close as superseded** | Pick #85 |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | **close as superseded** | Pick #85 |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **close as superseded** | Pick #85; CI fail |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | **aligned** | Ecosystem stats docs; governance — human merge only |

**Also commented this pass:** [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) (**aligned**), [benchmarks#49](https://github.com/li-langverse/benchmarks/pull/49) (**defer**), [li-demo#7–#9](https://github.com/li-langverse/li-demo/pull/7) (**aligned** / pick one duplicate).

### Labels

- Did **not** add `merge-approved` (pr-review-agent only).
- Added `plan-needed`: **lic#87**, **benchmarks#49**.

### Local CI

- Briefing `local_ci_results`: null — run `local-ci-sweep` for benchmarks#32/#34/#39 when gate needs local-ci for GHA `none`.

### Control plane

- Recent `pr_alignment` runs: `pr_alignment-1779293372481` (16:09Z **finished**), `pr_alignment-1779292109234` (15:48Z **error**).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human: keep **lic#85**, close **#80/#82/#94** (horner DCE guard) | lic | — |
| Human review **benchmarks#47** for `merge-approved` | benchmarks | — |
| Human review **roadmap#12** (governance merge) | roadmap | — |
| Human: pick one **li-demo** PR among #7/#8/#9; close others | li-demo | — |
| Merge **benchmarks#34** then close **#32** | benchmarks | — |
| Fix CI on **lic#91** and **li-language#6** | lic, li-language | `bug` |
| Plan **lic#87** / **benchmarks#49** before promoting drafts | lic, benchmarks | `plan-needed` |
| Confirm draft intent: **lic#81/#84/#92**, **benchmarks#42–#48** | lic, benchmarks | — |
| Add **ci.yml** on **li-local-ci** main | li-local-ci | `ci` |

## Deferred

- All `prs_recommended_close` rows (`safe_now: false`) — no agent closes without dependency merge or human abandon confirmation.
- **benchmarks#32** until **#34** merges.
- **roadmap#12** — governance human merge.
- **li-demo#7/#8/#9** — human picks canonical duplicate.
- Draft httpd/world_engine cluster until owners confirm abandon vs promote.
- **56** orphan branches — `pr_branch_opener` automation.
