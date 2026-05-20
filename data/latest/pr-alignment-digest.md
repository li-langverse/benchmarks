# PR alignment agent digest — 2026-05-20 (18:42Z pass)

**Agent:** `pr_alignment`  
**Preflight:** `pr-merge-queue-plan.py`, `pr-branch-hygiene.py` (refreshed), `run-pr-program.py` (refreshed), `issue-feature-triage.py`  
**Org:** li-langverse  
**Vision:** proof → easy → fast ([vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md))  
**Merges performed:** 0 (agent does not merge)

## Executive summary

- Preflight refreshed at **18:39–18:42Z**: **14** PRs in merge-order queue; **28** open org-wide (`pr-program`); **0** `merge-approved` / **0** in `merge_sequence`.
- **0 PRs closed** — `prs_safe_close_now: 0`; all **13** hygiene close candidates remain `safe_now: false`.
- **4 alignment comments** this pass: [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34#issuecomment-4501553165), [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39#issuecomment-4501553335), [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32#issuecomment-4501553717) (wait for #34), [lic#94](https://github.com/li-langverse/lic/pull/94#issuecomment-4501553497) (superseded).
- **Horner cluster** (#80/#82/#85/#91/#94/#98): **lic#85** canonical (CI pass); **lic#91** alternative (broader numerics, CI fail); **#94/#98** superseded + CI fail; human pick one then close siblings.
- **benchmarks#32** ⊂ **#34** — defer close #32 until #34 merges.
- **Draft PRs** (lic#81/#84/#87/#101, benchmarks#42–#50): **active today** (8–74 commits) — not abandoned; do not close.
- **56** orphan branches without PR — route to `pr_branch_opener`.
- **local_ci_results:** null — run `local-ci-sweep` for GHA `none` on benchmarks#32/#34/#39.
- **22** issues still `plan-needed` across lic/benchmarks.

## Deliverable / findings

### Close hygiene (max 5)

| PR | Action | Reason |
|----|--------|--------|
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **Deferred** | Close after #34 merges; comment 18:42Z |
| [lic#94](https://github.com/li-langverse/lic/pull/94) | **Deferred** | Superseded by #85; CI fail — comment 18:42Z |
| [lic#98](https://github.com/li-langverse/lic/pull/98) | **Deferred** | Superseded by #85 (prior pass comment) |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **Deferred** | Superseded by #85 (prior pass) |
| [lic#82](https://github.com/li-langverse/lic/pull/82) | **Deferred** | Superseded by #85 (prior pass) |
| [lic#81/#84/#87/#101](https://github.com/li-langverse/lic/pull/101) | **Deferred** | Draft — updated 2026-05-20 (not abandoned) |
| [benchmarks#42–#50](https://github.com/li-langverse/benchmarks/pull/50) | **Deferred** | Draft cluster — #49/#50 have `plan-needed` or CI fail |

**Closes this run:** 0

### Per-PR alignment (8 reviewed — merge-plan ranks 1–8)

| PR | Verdict | Notes |
|----|---------|-------|
| [li-demo#7](https://github.com/li-langverse/li-demo/pull/7) | **aligned** (sandbox) | Agent smoke; CI pass — skip merge unless user asks |
| [li-demo#8](https://github.com/li-langverse/li-demo/pull/8) | **aligned** (sandbox) | 100% overlap with #7/#9 — human pick one |
| [li-demo#9](https://github.com/li-langverse/li-demo/pull/9) | **aligned** (sandbox) | Docs maintainer automation |
| [benchmarks#32](https://github.com/li-langverse/benchmarks/pull/32) | **wait for dependency** | Close after #34 merges — comment 18:42Z |
| [benchmarks#34](https://github.com/li-langverse/benchmarks/pull/34) | **aligned** | Security CWE preflight; supersedes #32; GHA `none` — comment 18:42Z |
| [benchmarks#39](https://github.com/li-langverse/benchmarks/pull/39) | **aligned** | Org sweep exclude li-cursor-agents; GHA `none` — comment 18:42Z |
| [benchmarks#47](https://github.com/li-langverse/benchmarks/pull/47) | **aligned** | PH-5b/PH-7e numerics docs; CI pass |
| [lic#80](https://github.com/li-langverse/lic/pull/80) | **close as superseded** | Duplicate horner fix; prefer **lic#85** |

**Extended queue (ranks 9–14):** lic#82/#85/#91/#94/#98 (horner duplicates), roadmap#12 (governance — human merge).

### Labels

- Did **not** add `merge-approved` (pr-review-agent only).
- **`plan-needed`** on lic#101, lic#87, benchmarks#49 — retained; no new labels added.

### Local CI

- Briefing `local_ci_results`: null — run `python3 scripts/local-ci-sweep.py` for benchmarks#32/#34/#39 when gate needs local-ci for GHA `none`.

### Merge queue snapshot

Vision order: package CI / mirrors → benchmarks → lic → lip/lit/lis → roadmap.

Top CI-green (awaiting `merge-approved`): benchmarks#47 → lic#85 → lic#82 → lic#80 → roadmap#12.

Redundant warnings: 15 lic horner pairs + benchmarks#34⊃#32 + 3 li-demo overlaps.

### Control plane

- Prior `pr_alignment` runs today: finished (17:11Z, 17:33Z, 17:53Z); one `error` at 18:15Z.
- This run: comments + digest only; no DB writes.

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Human: keep **lic#85**, close **#80/#82/#94/#98** after pick | lic | — |
| Or merge **lic#91** once (broader pass), close other horner PRs | lic | — |
| Human review **benchmarks#47** for `merge-approved` | benchmarks | — |
| Merge **benchmarks#34** then close **#32** | benchmarks | — |
| Human review **roadmap#12** (governance merge) | roadmap | — |
| Human: pick one **li-demo** PR among #7/#8/#9 | li-demo | — |
| Plan **lic#101** before undraft | lic | `plan-needed` |
| Plan **lic#87** / **benchmarks#49** before promoting drafts | lic, benchmarks | `plan-needed` |
| Add **ci.yml** on **li-local-ci** main | li-local-ci | `ci` |
| Run **issue-feature-planner** on 22 `plan-needed` issues | lic, benchmarks | `plan-needed` |

## Deferred

- All **13** `prs_recommended_close` rows (`safe_now: false`).
- Draft PR closes until human confirms abandon (drafts updated 2026-05-20).
- **benchmarks#32** close until **#34** merges.
- **roadmap#12** merge (governance gate).
- **li-demo#7–#9** (automation sandbox).
- **local-ci-sweep** for GHA-missing PRs (benchmarks#32/#34/#39).
- **56** branches without PRs (`pr_branch_opener`).
- Horner **#98** human close (superseded comment exists; not `safe_now`).
