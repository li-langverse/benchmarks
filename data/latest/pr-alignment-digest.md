# PR alignment agent digest — 2026-05-20 (14:50Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py` (refreshed 14:49Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight refreshed: **12** PRs in merge queue order; **24** open org-wide (`pr-program-run`); **0** `merge-approved` / **0** in `merge_sequence`.
- **0 PRs closed** — `prs_safe_close_now: 0`; all **11** hygiene close candidates require human confirmation or dependency merge.
- **4 alignment comments posted** this pass: [lic#85](https://github.com/li-langverse/lic/pull/85#issuecomment-4499597359) (horner triplet), [lic#83](https://github.com/li-langverse/lic/pull/83#issuecomment-4499598341) (undrafted + CI fail), [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32#issuecomment-4499597683) (defer until #34 merges).
- **Triple horner bench:** [lic#85](https://github.com/li-langverse/lic/pull/85) vs [lic#82](https://github.com/li-langverse/lic/pull/82) vs [lic#80](https://github.com/li-langverse/lic/pull/80) — 100% overlap; human must pick one; #85 CI mostly green.
- **Redundant:** [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) ⊂ [#34](https://github.com/li-langverse/benchmarks/pull/34) — defer close until #34 merges (#34 still OPEN).
- **lic#83** no longer draft — `build-and-test` failing; consolidates #77/#78 when ready.
- **CI-green for review:** benchmarks#47, lic#80/#82/#85, roadmap#12; benchmarks#32/#34/#39 GHA empty on branch heads.
- **li-demo triplet** (#7/#8/#9): 100% file overlap — sandbox: merge only if human asks.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges (`safe_now: false`; in merge_order) — [comment](https://github.com/li-langverse/benchmarks/pull/32#issuecomment-4499597683) |
| [lic#81](https://github.com/li-langverse/lic/pull/81) | **Deferred** | Draft World Studio — CI fail; confirm not abandoned |
| [lic#84](https://github.com/li-langverse/lic/pull/84) | **Deferred** | New draft (hygiene) — confirm abandoned before close |
| [lic#77](https://github.com/li-langverse/lic/pull/77), [lic#78](https://github.com/li-langverse/lic/pull/78) | **Deferred** | Draft 2e/2f — close only after #83 lands or human abandon confirm |
| [benchmarks#42–#48](https://github.com/li-langverse/benchmarks/pull/42) | **Deferred** | Draft PH-IO/HTTP/world_engine work — not `safe_now` |

**Closes this run:** 0

### Per-PR alignment (12 merge-order PRs)

| PR | Verdict | Notes |
|----|---------|-------|
| [li-demo#7](https://github.com/li-langverse/li-demo/pull/7) | aligned (sandbox) | Agent smoke marker; pr-program skip unless human asks |
| [li-demo#8](https://github.com/li-langverse/li-demo/pull/8) | aligned (sandbox) | Duplicate triplet — pick one with #7/#9 |
| [li-demo#9](https://github.com/li-langverse/li-demo/pull/9) | aligned (sandbox) | Duplicate triplet — pick one with #7/#8 |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | wait for dependency | Superseded by #34; GHA `none` |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | aligned | Security CWE audit preflight; merge before closing #32 |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | aligned | Org sweep excludes li-cursor-agents; GHA `none` |
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | aligned | PH-5b/PH-7e numerics docs; CI pass |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | aligned | Honest horner_pure_li; CI pass — pick vs #82/#85 |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | aligned | Same scope as #80/#85; CI pass |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | aligned | Newest horner branch; CI mostly pass — **comment posted** |
| [lic#83](https://github.com/li-langverse/lic/pull/83) | needs plan + CI fix | Undrafted; GHA fail — **comment posted** |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | aligned | Ecosystem stats docs; governance — human merge only |

### Additional reviewed (drafts + failing)

| PR | Verdict | Notes |
|----|---------|-------|
| [lic#81](https://github.com/li-langverse/lic/pull/81) | wait for dependency | World Studio merge; draft; CI fail |
| [lic#77](https://github.com/li-langverse/lic/pull/77) | wait for dependency | Draft 2e/2f VC — supersede when #83 lands |
| [lic#78](https://github.com/li-langverse/lic/pull/78) | wait for dependency | Draft 2e/2f E0304; CI fail |
| [lic#84](https://github.com/li-langverse/lic/pull/84) | wait for dependency | Draft — hygiene flags; confirm intent |
| [benchmarks#42–#46](https://github.com/li-langverse/benchmarks/pull/42) | aligned / wait (draft) | PH-IO ingest, language docs, HTTP plots |
| [li-language#6](https://github.com/li-langverse/li-language/pull/6) | needs CI fix | Tier-2 gaming physics; GHA fail — bug_fixer queue |

### Labels

- Did not add `merge-approved` (pr-review-agent only).
- No `plan-needed` label changes (top queue are CI/docs/bench fixes, not unplanned feature PRs).

### Local CI

- Briefing `local_ci_results`: null — run `python3 scripts/local-ci-sweep.py --repo benchmarks --pr 32|34|39` when gate needs local-ci for GHA `none`.

### Control plane

- Latest finished `pr_alignment` runs: `pr_alignment-1779287314681` (14:28Z), `pr_alignment-1779286098374` (14:08Z).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human: pick **one** of lic#80 / #82 / #85 (horner DCE guard) | lic | — |
| Human review **benchmarks#47** for `merge-approved` | benchmarks | — |
| Human review **roadmap#12** (governance merge) | roadmap | — |
| Human: pick one **li-demo** PR among #7/#8/#9 | li-demo | — |
| Fix CI on **lic#83** before merge-approved | lic | `plan-needed` (if no plan link) |
| Merge **benchmarks#34** then close **#32** | benchmarks | — |

## Deferred

- Close **benchmarks#32** until **#34** merges.
- Close draft **lic#77/#78/#81/#84** and **benchmarks#42–#48** until human confirms abandoned or canonical PR (#83) lands.
- **li-language#6** CI — route to `bug_fixer`.
- **56** branches without open PR — `pr_branch_opener` queue.
- Adding `merge-approved` — **pr_reviewer** agent only.
