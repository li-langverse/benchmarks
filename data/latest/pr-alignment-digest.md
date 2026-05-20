# PR alignment agent digest — 2026-05-20 (15:10Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`, `issue-feature-triage.py` (refreshed 15:09–15:10Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight refreshed: **11** PRs in merge queue order; **23** open org-wide (`pr-program-run`); **0** `merge-approved` / **0** in `merge_sequence`.
- **0 PRs closed** — `prs_safe_close_now: 0`; hygiene lists **10** draft/duplicate candidates (all `safe_now: false`).
- **[lic#83](https://github.com/li-langverse/lic/pull/83) merged** (2026-05-20T15:02Z); draft **[lic#77](https://github.com/li-langverse/lic/pull/77)** / **[lic#78](https://github.com/li-langverse/lic/pull/78)** already **CLOSED** (superseded path).
- **4 alignment comments posted** this pass: [lic#84](https://github.com/li-langverse/lic/pull/84#issuecomment-4499784226), [lic#81](https://github.com/li-langverse/lic/pull/81#issuecomment-4499784566), [li-demo#8](https://github.com/li-langverse/li-demo/pull/8#issuecomment-4499785045), [lic#82](https://github.com/li-langverse/lic/pull/82#issuecomment-4499785785).
- **Horner triplet:** [lic#80](https://github.com/li-langverse/lic/pull/80) / [#82](https://github.com/li-langverse/lic/pull/82) / [#85](https://github.com/li-langverse/lic/pull/85) — human must pick one; suggest #85 if CI fully green.
- **Redundant:** [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) ⊂ [#34](https://github.com/li-langverse/benchmarks/pull/34) — defer close until #34 merges.
- **CI-green for review:** benchmarks#47, lic#80/#82/#85, roadmap#12; benchmarks#32/#34/#39 GHA empty on branch heads.
- **li-demo triplet** (#7/#8/#9): 100% overlap — sandbox; merge only if human asks.
- **57** branches without open PR — route to `pr_branch_opener`.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges (`safe_now: false`) |
| [lic#81](https://github.com/li-langverse/lic/pull/81) | **Deferred** | Draft World Studio — CI fail; [comment](https://github.com/li-langverse/lic/pull/81#issuecomment-4499784566) |
| [lic#84](https://github.com/li-langverse/lic/pull/84) | **Deferred** | Draft httpd perf — overlaps #87; [comment](https://github.com/li-langverse/lic/pull/84#issuecomment-4499784226) |
| [lic#77](https://github.com/li-langverse/lic/pull/77), [lic#78](https://github.com/li-langverse/lic/pull/78) | **Already closed** | Superseded by merged #83 |
| [benchmarks#42–#48](https://github.com/li-langverse/benchmarks/pull/42) | **Deferred** | Draft PH-IO/HTTP/world_engine — not `safe_now` |
| [lic#87](https://github.com/li-langverse/lic/pull/87), [lic#89](https://github.com/li-langverse/lic/pull/89) | **Deferred** | New drafts in hygiene list — confirm intent |

**Closes this run:** 0

### Per-PR alignment (merge-order queue, max 8 reviewed)

| PR | Verdict | Notes |
|----|---------|-------|
| [li-demo#7](https://github.com/li-langverse/li-demo/pull/7) | aligned (sandbox) | Agent smoke; pr-program skip unless human asks |
| [li-demo#8](https://github.com/li-langverse/li-demo/pull/8) | close as superseded | Duplicate triplet — **comment posted** |
| [li-demo#9](https://github.com/li-langverse/li-demo/pull/9) | close as superseded | Pick one with #7/#8 |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | wait for dependency | Superseded by #34; GHA `none` |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | aligned | Security CWE audit preflight; merge before closing #32 |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | aligned | Org sweep excludes li-cursor-agents; GHA `none` |
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | aligned | PH-5b/PH-7e numerics docs; CI pass |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | aligned | Honest horner_pure_li; pick vs #82/#85 |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | aligned | **comment posted** — close after #85 picked |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | aligned | Newest horner branch; CI mostly pass |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | aligned | Ecosystem stats; governance — human merge only |

### Additional reviewed (drafts + hygiene)

| PR | Verdict | Notes |
|----|---------|-------|
| [lic#83](https://github.com/li-langverse/lic/pull/83) | **merged** | 2e/2f/H canonical — unblocks draft cleanup |
| [lic#81](https://github.com/li-langverse/lic/pull/81) | wait for dependency | World Studio merge; draft; CI fail — **comment posted** |
| [lic#84](https://github.com/li-langverse/lic/pull/84) | wait for dependency | Draft httpd — **comment posted** |
| [lic#87](https://github.com/li-langverse/lic/pull/87), [lic#89](https://github.com/li-langverse/lic/pull/89) | wait for dependency | New httpd/docs drafts — confirm vs abandoned |
| [benchmarks#42–#48](https://github.com/li-langverse/benchmarks/pull/42) | aligned / wait (draft) | PH-IO ingest, language docs, HTTP plots |
| [li-language#6](https://github.com/li-langverse/li-language/pull/6) | needs CI fix | Tier-2 gaming physics; GHA fail — `bug_fixer` queue |

### Labels

- Did not add `merge-approved` (pr-review-agent only).
- No `plan-needed` label changes (queue items are CI/docs/bench fixes).

### Local CI

- Briefing `local_ci_results`: null — run `python3 scripts/local-ci-sweep.py --repo benchmarks --pr 32|34|39` when gate needs local-ci for GHA `none`.

### Control plane

- Latest finished `pr_alignment` runs: `pr_alignment-1779288368092` (14:46Z), `pr_alignment-1779287314681` (14:28Z).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human: pick **one** of lic#80 / #82 / #85 (horner DCE guard) | lic | — |
| Human review **benchmarks#47** for `merge-approved` | benchmarks | — |
| Human review **roadmap#12** (governance merge) | roadmap | — |
| Human: pick one **li-demo** PR among #7/#8/#9; close others | li-demo | — |
| Merge **benchmarks#34** then close **#32** | benchmarks | — |
| Confirm **lic#81** / **#84** / **#87** intent or close drafts | lic | — |
| Fix CI on **li-language#6** | li-language | `bug` |

## Deferred

- Close **benchmarks#32** until **#34** merges.
- Close draft **lic#81/#84/#87/#89** and **benchmarks#42–#48** until human confirms abandoned.
- **li-language#6** CI — route to `bug_fixer`.
- **57** branches without open PR — `pr_branch_opener` queue.
- Adding `merge-approved` — **pr_reviewer** agent only.
