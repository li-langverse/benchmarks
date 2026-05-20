# PR alignment agent digest — 2026-05-20 (15:32Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py` (refreshed 15:27–15:31Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight refreshed: **12** PRs in merge-order queue; **24** open org-wide; **0** `merge-approved` / **0** in `merge_sequence`.
- **0 PRs closed** — `prs_safe_close_now: 0`; hygiene lists **11** draft/duplicate candidates (all `safe_now: false`).
- **4 alignment comments posted** this pass: [lic#91](https://github.com/li-langverse/lic/pull/91#issuecomment-4499978974), [lic#87](https://github.com/li-langverse/lic/pull/87#issuecomment-4499979180), [lic#92](https://github.com/li-langverse/lic/pull/92#issuecomment-4499979357), [benchmarks#48](https://github.com/li-langverse/benchmarks/pull/48#issuecomment-4499979569).
- **Horner triplet** ([lic#80](https://github.com/li-langverse/lic/pull/80) / [#82](https://github.com/li-langverse/lic/pull/82) / [#85](https://github.com/li-langverse/lic/pull/85)): 100% overlap — human must pick one; all CI-green on Linux rollup.
- **Redundant:** [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) ⊂ [#34](https://github.com/li-langverse/benchmarks/pull/34) — defer close until #34 merges.
- **lic#91** numerics docs: aligned with PH-5b/PH-7e but **GHA fail** on `build-and-test` / macOS — route to `bug_fixer`.
- **Httpd drafts** (#84/#87/#92): active M1 work; [#89](https://github.com/li-langverse/lic/pull/89) already **CLOSED** (superseded by #92).
- **56** branches without open PR — route to `pr_branch_opener`.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges (`safe_now: false`) |
| [lic#81](https://github.com/li-langverse/lic/pull/81) | **Deferred** | Draft World Studio — CI fail; prior alignment comment |
| [lic#84](https://github.com/li-langverse/lic/pull/84) | **Deferred** | Draft httpd perf — prior alignment comment |
| [lic#87](https://github.com/li-langverse/lic/pull/87) | **Deferred** | Draft M1 wave 1 — **comment posted** this pass |
| [lic#92](https://github.com/li-langverse/lic/pull/92) | **Deferred** | Draft TOML loader — **comment posted**; supersedes #89 |
| [lic#89](https://github.com/li-langverse/lic/pull/89) | **Already closed** | Superseded by #92 |
| [benchmarks#42–#48](https://github.com/li-langverse/benchmarks/pull/48) | **Deferred** | Draft PH-IO/HTTP/world_engine — #48 **comment posted** |

**Closes this run:** 0

### Per-PR alignment (merge-order queue, max 8 reviewed)

| PR | Verdict | Notes |
|----|---------|-------|
| [li-demo#7](https://github.com/li-langverse/li-demo/pull/7) | aligned (sandbox) | Agent smoke; pr-program skip unless human asks |
| [li-demo#8](https://github.com/li-langverse/li-demo/pull/8) | close as superseded | Duplicate triplet — pick one with #7/#9 |
| [li-demo#9](https://github.com/li-langverse/li-demo/pull/9) | close as superseded | 100% overlap with #7/#8 |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | wait for dependency | Superseded by #34; GHA `none` |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | aligned | Security CWE audit preflight; merge before closing #32 |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | aligned | Org sweep excludes li-cursor-agents; GHA `none` |
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | aligned | PH-5b/PH-7e numerics docs; CI pass |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | aligned | Honest horner_pure_li; pick vs #82/#85 |

### Additional reviewed (beyond queue cap)

| PR | Verdict | Notes |
|----|---------|-------|
| [lic#82](https://github.com/li-langverse/lic/pull/82) | aligned | Duplicate horner — close after #85 picked |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | aligned | Newest horner branch; suggest canonical pick |
| [lic#91](https://github.com/li-langverse/lic/pull/91) | aligned (CI fail) | Numerics researcher; **comment posted** |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | aligned | Ecosystem stats; governance — human merge only |
| [lic#87](https://github.com/li-langverse/lic/pull/87) | wait for dependency | Draft httpd M1 — **comment posted** |
| [lic#92](https://github.com/li-langverse/lic/pull/92) | aligned (draft) | TOML route loader — **comment posted** |
| [benchmarks#48](https://github.com/li-langverse/benchmarks/pull/48) | wait for dependency | World engine ingest — **comment posted** |
| [li-language#6](https://github.com/li-langverse/li-language/pull/6) | needs CI fix | Tier-2 gaming physics; GHA fail |

### Labels

- Did not add `merge-approved` (pr-review-agent only).
- No `plan-needed` label changes (queue items are CI/docs/bench fixes).

### Local CI

- Briefing `local_ci_results`: null — run `local-ci-sweep` for benchmarks#32/#34/#39 when gate needs local-ci for GHA `none`.

### Control plane

- Latest finished `pr_alignment` runs: `pr_alignment-1779289600412` (15:06Z), prior passes 14:46Z / 14:28Z.

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human: pick **one** of lic#80 / #82 / #85 (horner DCE guard) | lic | — |
| Human review **benchmarks#47** for `merge-approved` | benchmarks | — |
| Human review **roadmap#12** (governance merge) | roadmap | — |
| Human: pick one **li-demo** PR among #7/#8/#9; close others | li-demo | — |
| Merge **benchmarks#34** then close **#32** | benchmarks | — |
| Fix CI on **lic#91** and **li-language#6** | lic, li-language | `bug` |
| Confirm **lic#81** / **#84** / **#87** / **#92** / **benchmarks#48** draft intent | lic, benchmarks | — |

## Deferred

- Close **benchmarks#32** until **#34** merges.
- Close draft **lic#81/#84/#87/#92** and **benchmarks#42–#48** until human confirms abandoned (`safe_now: false`).
- **lic#91** / **li-language#6** CI — route to `bug_fixer`.
- **56** branches without open PR — `pr_branch_opener` queue.
- Adding `merge-approved` — **pr_reviewer** agent only.
