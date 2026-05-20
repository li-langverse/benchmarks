# PR alignment agent digest — 2026-05-20 (13:34Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py` (refreshed 13:34Z)  
**Org:** li-langverse  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight: **17 open PRs** org-wide; merge queue ranks **8** PRs (li-demo#7 → roadmap#12); **0** in `merge_sequence` / **0** `merge-approved`.
- **0 PRs closed** — hygiene lists **8** close candidates; **`prs_safe_close_now: 0`**; no duplicate-bot exceptions.
- **4 alignment comments posted:** [li-demo#8](https://github.com/li-langverse/li-demo/pull/8), [li-demo#9](https://github.com/li-langverse/li-demo/pull/9), [lic#77](https://github.com/li-langverse/lic/pull/77), [lic#78](https://github.com/li-langverse/lic/pull/78).
- **Merged since last pass:** [lic#73](https://github.com/li-langverse/lic/pull/73) (MIR object fields), [lic#72](https://github.com/li-langverse/lic/pull/72) (Phase H li-http) — removed from active queue.
- **Redundant pair:** benchmarks#32 ⊂ #34 — defer close until #34 merges (both in merge_order).
- **li-demo triplet:** #7/#8/#9 — 100% overlap; human pick one before `merge-approved` (sandbox: merge only if asked).
- **CI-green (GHA):** benchmarks#47, roadmap#12, li-demo#7–9; benchmarks#32/#34/#39 GHA `none` on branch heads.
- **local_ci_results:** null — run `local-ci-sweep` for benchmarks#32, #34, #39 when gate needs local-ci.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges (`safe_now: false`; in merge_order) |
| [benchmarks#42–#46](https://github.com/li-langverse/benchmarks/pull/42) | **Deferred** | Draft PRs — CI pass on several; not abandoned |
| [lic#77](https://github.com/li-langverse/lic/pull/77), [lic#78](https://github.com/li-langverse/lic/pull/78) | **Deferred** | New drafts — alignment comment posted; confirm not abandoned |
| [lic#72](https://github.com/li-langverse/lic/pull/72), [lic#73](https://github.com/li-langverse/lic/pull/73) | **Merged** | No longer open |

**Closes this run:** 0

### Per-PR alignment (8 open merge-order PRs)

| PR | Verdict | Notes |
|----|---------|-------|
| [li-demo#7](https://github.com/li-langverse/li-demo/pull/7) | aligned (sandbox) | Agent smoke; pr-program skip unless human asks |
| [li-demo#8](https://github.com/li-langverse/li-demo/pull/8) | aligned (sandbox) | Duplicate triplet — **comment posted** |
| [li-demo#9](https://github.com/li-langverse/li-demo/pull/9) | aligned (sandbox) | Duplicate triplet — **comment posted** |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | wait for dependency | Superseded by #34; GHA `none` |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | aligned | Security CWE audit preflight; merge before closing #32 |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | aligned | Org sweep excludes li-cursor-agents; GHA `none` |
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | aligned | PH-5b/PH-7e numerics docs; CI pass (dashboard-build, ingest-smoke) |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | aligned | Ecosystem stats docs; governance — human merge |

### Additional reviewed (outside merge_order top 8)

| PR | Verdict | Notes |
|----|---------|-------|
| [lic#73](https://github.com/li-langverse/lic/pull/73) | aligned (merged) | MIR object fields |
| [lic#72](https://github.com/li-langverse/lic/pull/72) | aligned (merged) | Phase H li-http; had plan-approved |
| [lic#77](https://github.com/li-langverse/lic/pull/77) | wait for dependency | Draft 2e/2f VC — **comment posted** |
| [lic#78](https://github.com/li-langverse/lic/pull/78) | wait for dependency | Draft 2e/2f E0304; CI fail — **comment posted** |
| [benchmarks#42–#46](https://github.com/li-langverse/benchmarks/pull/42) | aligned / wait (draft) | PH-IO ingest, language docs, HTTP plots — active drafts |
| [li-language#6](https://github.com/li-langverse/li-language/pull/6) | needs CI fix | Tier-2 gaming physics; GHA fail — bug_fixer queue |

### Labels

- Did not add `merge-approved` (pr-review-agent only).
- No `plan-needed` label changes this run (no unplanned feature PRs in top 8).

### Local CI

- No briefing `local_ci_results` — use `python3 scripts/local-ci-sweep.py --repo benchmarks --pr 32|34|39` when GHA stays `none`.

### Control plane

- Latest finished `pr_alignment` run before this pass: `pr_alignment-1779279665084` (12:21Z).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human review benchmarks#47 for `merge-approved` | benchmarks | — |
| Human review roadmap#12 (governance merge) | roadmap | — |
| Human: pick one li-demo PR among #7/#8/#9 | li-demo | — |
| Run local-ci-sweep for benchmarks#32, #34, #39 | benchmarks | — |
| Close benchmarks#32 after benchmarks#34 merges | benchmarks | superseded |
| Mark ready + plan-approved on lic#77/#78 when 2f work is active | lic | plan-approved, plan-needed |
| Fix CI on li-language#6 | li-language | — |
| Human merge li-demo#7 if smoke test intended on main | li-demo | — |

## Deferred

- Close **benchmarks#32** after **#34** merges.
- **5 benchmarks draft PRs** (#42–#46) + **2 lic drafts** (#77–#78) — confirm abandoned before close.
- **58 branches** without open PRs — `pr_branch_opener` agent.
- **22 issues** with `plan-needed` — `issue_planner` agent.
- **li-language#6** (CI fail) — bug_fixer; outside merge_order top 8.
