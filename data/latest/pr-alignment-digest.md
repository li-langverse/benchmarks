# PR alignment agent digest — 2026-05-20 (17:57Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`, `issue-feature-triage.py` (refreshed 17:53–17:57Z)  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight refreshed: **14** PRs in merge-order queue; **27** open org-wide (`pr-program`); **0** `merge-approved` / **0** in `merge_sequence`.
- **0 PRs closed** — `prs_safe_close_now: 0`; all **12** hygiene close candidates remain `safe_now: false`.
- **2 alignment comments** this pass: [lic#98](https://github.com/li-langverse/lic/pull/98#issuecomment-4501133167) (close as superseded), [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32#issuecomment-4501133312) (wait for #34).
- **Horner cluster** (#80/#82/#85/#91/#94/#98): **lic#85** canonical (CI pass); **lic#91** alternative for broader numerics; **#94/#98** superseded; **#80/#82** prior pass comments recommend close after human pick.
- **benchmarks#32** ⊂ **#34** — both open; **#34 not merged** — defer close #32.
- **56** orphan branches without PR — route to `pr_branch_opener`.
- **local_ci_results:** null — run `local-ci-sweep` for GHA `none` on benchmarks#32/#34/#39 and lic#91.
- **22** issues still `plan-needed` across lic/benchmarks (issue-feature-triage).

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges; comment refreshed 17:57Z |
| [lic#98](https://github.com/li-langverse/lic/pull/98) | **Deferred** | Superseded by #85 — close comment posted (human close) |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **Deferred** | Superseded by #85 (prior pass) |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **Deferred** | Superseded by #85 (prior pass) |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | **Deferred** | Superseded by #85 (prior pass) |
| [lic#81/#84/#87/#101](https://github.com/li-langverse/lic/pull/101) | **Deferred** | Draft — **active** (8–74 commits, updated today); not abandoned |
| [benchmarks#42–#49](https://github.com/li-langverse/benchmarks/pull/49) | **Deferred** | Draft cluster — #49 has `plan-needed` |

**Closes this run:** 0

### Per-PR alignment (8 reviewed)

| PR | Verdict | Notes |
|----|---------|-------|
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | **aligned** | PH-5b/PH-7e numerics docs; CI pass; ready for `pr-review-agent` |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | **aligned** | Security CWE preflight; supersedes #32; GHA `none` |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **wait for dependency** | Close after #34 merges — comment refreshed |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | **aligned** | Org sweep exclude li-cursor-agents; GHA `none` |
| [lic#85](https://github.com/li-langverse/lic/pull/85) | **aligned** | **Canonical** horner DCE fix; CI pass |
| [lic#91](https://github.com/li-langverse/lic/pull/91) | **aligned** (pick one) | Broader numerics pass vs #85 — human choice |
| [lic#98](https://github.com/li-langverse/lic/pull/98) | **close as superseded** | 100% overlap; CI fail — comment this pass |
| [roadmap#12](https://github.com/li-langverse/roadmap/pull/12) | **aligned** | Ecosystem stats; governance — human merge only |

**Also noted:** lic#94 (superseded, CI fail), lic#80/#82 (superseded), li-demo#7–#9 (sandbox skip), benchmarks#49 / lic#87 / lic#101 (`plan-needed` drafts).

### Labels

- Did **not** add `merge-approved` (pr-review-agent only).
- **`plan-needed`** already on lic#101, lic#87, benchmarks#49 — no changes.

### Local CI

- Briefing `local_ci_results`: null — run `python3 scripts/local-ci-sweep.py` for benchmarks#32/#34/#39 and lic#91 when gate needs local-ci for GHA `none`.

### Merge queue snapshot

Vision order: package CI / mirrors → benchmarks → lic → lip/lit/lis → roadmap.

Top non-sandbox CI-green (awaiting `merge-approved`): benchmarks#47 → lic#85 → lic#82 → lic#80 → roadmap#12.

Redundant warnings: 15 lic horner pairs + benchmarks#34⊃#32 + 3 li-demo overlaps.

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
| Run **issue-feature-planner** on 22 `plan-needed` issues | lic, benchmarks | `plan-needed` |

## Deferred

- All **12** `prs_recommended_close` rows (`safe_now: false`).
- Draft PR closes until human confirms abandon (drafts show recent activity).
- **benchmarks#32** close until **#34** merges.
- **roadmap#12** merge (governance gate).
- **li-demo#7–#9** (automation sandbox).
- **local-ci-sweep** for GHA-missing PRs.
- **56** branches without PRs (`pr_branch_opener`).
