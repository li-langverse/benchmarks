# PR alignment agent digest — 2026-05-20 (16:15Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`, `issue-feature-triage.py` (refreshed 16:08–16:12Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight refreshed: **13** PRs in merge-order queue; **25** open org-wide (`pr-program`); **0** `merge-approved` / **0** in `merge_sequence`.
- **0 PRs closed** — `prs_safe_close_now: 0`; hygiene lists **11** draft/duplicate candidates (all `safe_now: false`).
- **11 alignment comments posted** this pass on queue + duplicate + draft targets (see Deliverable).
- **Horner quad** ([lic#80](https://github.com/li-langverse/lic/pull/80) / [#82](https://github.com/li-langverse/lic/pull/82) / [#85](https://github.com/li-langverse/lic/pull/85) / [#94](https://github.com/li-langverse/lic/pull/94)): 100% overlap — **#85** recommended canonical (CI green); **#94** failing CI.
- **Redundant:** [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) ⊂ [#34](https://github.com/li-langverse/benchmarks/pull/34) — defer close until #34 merges; comment posted on #32.
- **lic#91** numerics docs: aligned PH-5b/PH-7e but **GHA fail** — merge after #85; route CI to `bug_fixer`.
- **roadmap#12**: aligned docs; governance repo — human merge only.
- **56** branches without open PR — route to `pr_branch_opener`.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges (`safe_now: false`); [comment](https://github.com/li-langverse/benchmarks/pull/32#issuecomment-4500358031) |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **Deferred** | Superseded by #85 — human close; [comment](https://github.com/li-langverse/lic/pull/80#issuecomment-4500360934) |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | **Deferred** | Superseded by #85; [comment](https://github.com/li-langverse/lic/pull/82#issuecomment-4500361196) |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **Deferred** | Superseded + CI fail; [comment](https://github.com/li-langverse/lic/pull/94#issuecomment-4500361385) |
| [lic#81](https://github.com/li-langverse/lic/pull/81) | **Deferred** | Draft World Studio — confirm abandoned |
| [lic#84](https://github.com/li-langverse/lic/pull/84) | **Deferred** | Draft httpd perf — confirm abandoned |
| [lic#87](https://github.com/li-langverse/lic/pull/87) | **Deferred** | Draft M1 wave 1 — confirm abandoned |
| [lic#92](https://github.com/li-langverse/lic/pull/92) | **Deferred** | Draft TOML loader — [comment](https://github.com/li-langverse/lic/pull/92#issuecomment-4500363386) |
| [benchmarks#42–#48](https://github.com/li-langverse/benchmarks/pull/48) | **Deferred** | Draft cluster — [#48 comment](https://github.com/li-langverse/benchmarks/pull/48#issuecomment-4500363526) |

**Closes this run:** 0

### Per-PR alignment (primary queue + duplicates)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | **aligned** | PH-5b/PH-7e numerics docs; CI pass; [comment](https://github.com/li-langverse/benchmarks/pull/47#issuecomment-4500359401) |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | **aligned** | Security CWE preflight; supersedes #32; GHA `none`; [comment](https://github.com/li-langverse/benchmarks/pull/34#issuecomment-4500359642) |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **wait for dependency** | Close after #34; [comment](https://github.com/li-langverse/benchmarks/pull/32#issuecomment-4500358031) |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | **aligned** | Canonical horner DCE fix; CI green; [comment](https://github.com/li-langverse/lic/pull/85#issuecomment-4500360022) |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **close as superseded** | Pick #85 |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | **close as superseded** | Pick #85 |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **close as superseded** | Pick #85; CI fail |
| [lic#91](https://github.com/li-langverse/lic/pull/91) | **wait for dependency** | Docs + test; CI fail; after #85; [comment](https://github.com/li-langverse/lic/pull/91#issuecomment-4500361605) |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | **aligned** | Ecosystem stats; human merge; [comment](https://github.com/li-langverse/roadmap/pull/12#issuecomment-4500361745) |
| [lic#92](https://github.com/li-langverse/lic/pull/92) | **defer** | Draft httpd; needs plan-approved if promoted |
| [benchmarks#48](https://github.com/li-langverse/benchmarks/pull/48) | **defer** | Draft world_engine ingest |

### Labels

- Did not add `merge-approved` (pr-review-agent only).
- No `plan-needed` labels added (reviewed items are bench/docs/CI infra).

### Local CI

- Briefing `local_ci_results`: null — run `local-ci-sweep` for benchmarks#32/#34/#39 when gate needs local-ci for GHA `none`.

### Control plane

- Prior `pr_alignment` run `pr_alignment-1779292109234` (15:48Z) **error**; finished runs at 15:27Z / 15:06Z.

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human: keep **lic#85**, close **#80/#82/#94** (horner DCE guard) | lic | — |
| Human review **benchmarks#47** for `merge-approved` | benchmarks | — |
| Human review **roadmap#12** (governance merge) | roadmap | — |
| Human: pick one **li-demo** PR among #7/#8/#9; close others | li-demo | — |
| Merge **benchmarks#34** then close **#32** | benchmarks | — |
| Fix CI on **lic#91** and **li-language#6** | lic, li-language | `bug` |
| Confirm draft intent: **lic#81/#84/#87/#92**, **benchmarks#42–#48** | lic, benchmarks | — |
| Add **ci.yml** on **li-local-ci** main | li-local-ci | `ci` |

## Deferred

- Close **benchmarks#32** until **#34** merges.
- Close draft **lic#81/#84/#87/#92** and **benchmarks#42–#48** until human confirms abandoned (`safe_now: false`).
- **li-demo#7/#8/#9** triplet — no comment this pass (prior pass covered); human pick one.
- **lic#91** / **li-language#6** CI — route to `bug_fixer`.
- **56** branches without open PR — `pr_branch_opener` queue.
- Adding `merge-approved` — **pr_reviewer** agent only.
