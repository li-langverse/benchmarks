# PR alignment digest — 2026-05-30T15:15Z

**Agent:** `pr_alignment` · **Source:** heap `coord_pull_requests` · **Run:** `pr_alignment-1780153762510`  
**north_star_fit:** Scientific numerics + governance (PH-5b, PH-7e, Phase 2i, PH-7d, PH-DB-4) — proof → easy → fast  
**Vision:** [vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md) · **Master plan:** [2026-05-14-li-master-plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md)

## Executive summary

- **~242 open org PRs** (GraphQL search); gate scripts report **`open_prs: 0`** — **REST core exhausted** (0/5000); GraphQL still usable for `gh pr view` / search.
- **Vision merge order:** package CI / mirrors → benchmarks → lic → lip/lit/lis → roadmap (roadmap never auto-close).
- **11 draft PRs** in `prs_recommended_close` (lic#430–#432, #530–#540); **`prs_safe_close_now: 0`** — **0 closes** (confirm abandoned first).
- **Canonical tier-1 matmul:** [lic#437](https://github.com/li-langverse/lic/pull/437) — `merge-approved`, **aligned**, **defer** (`mergeable: CONFLICTING`).
- **Bench hotfix:** [lic#550](https://github.com/li-langverse/lic/pull/550) — **aligned**, **defer** (coordinate rebase with #437); alignment comment posted this run.
- **Feature blocked (needs plan):** [lic#489](https://github.com/li-langverse/lic/pull/489), [#517](https://github.com/li-langverse/lic/pull/517) — `plan-needed` without `plan-approved`; prior comments stand.
- **Draft + `merge-approved`:** lic#530–#532 — content aligned; **defer** until undraft (prior comments 14:03Z).
- **New opener PRs:** lip#46–48, roadmap#48, li-language#20–21 — **`plan-needed` added** this run; not merge-ready.
- **No merges, no `merge-approved` added** (alignment agent mandate).

## Deliverable / findings

### Preflight

| Artifact | `generated_at` | Key signal |
|----------|----------------|------------|
| `pr-merge-queue-plan.json` | 2026-05-30T15:09Z | `open_prs=0`, `merge_sequence=[]` — **false negative** (REST/GraphQL path in scripts) |
| `pr-program-run.json` | 2026-05-30T15:07Z | Stale snapshot; `run-pr-program.py` still running in background (>5m) |
| `pr-branch-hygiene.json` | 2026-05-30T14:56Z | 11 draft close candidates, `prs_safe_close_now=0`, 139 branches needing PR |
| `issue-feature-triage.json` | 2026-05-30T15:11Z | `needs_plan=32`, `candidates=3` (lic issues #521–#527, etc.) |
| `agent-briefing.json` | 2026-05-30T14:02Z | Heap queued 14 PR close/supersede review |

### Per-PR alignment (sampled 8)

| PR | Plan | PH / PKG | Merge order | Verdict | Action |
|----|------|----------|-------------|---------|--------|
| [lic#437](https://github.com/li-langverse/lic/pull/437) | Bench perf fix | PH-5b, PH-7e | After package wave | aligned, **defer** (conflicts) | Rebase → pr-review-agent |
| [lic#550](https://github.com/li-langverse/lic/pull/550) | Bench verify fix | PH-5b, PH-7e | With / after #437 | aligned, **defer** | Comment posted 15:15Z |
| [lic#489](https://github.com/li-langverse/lic/pull/489) | **needs plan** | httpd gap-phase2 | After `plan-approved` | needs plan | Prior comment; keep `plan-needed` |
| [lic#517](https://github.com/li-langverse/lic/pull/517) | **needs plan** | PH-7d, G-par | After lic core | needs plan | Prior comment 09:27Z |
| [lic#530](https://github.com/li-langverse/lic/pull/530) | Plan doc (#472) | PH-2i/2f | Parallel governance | aligned, **defer** (draft) | Do not close — `merge-approved` |
| [roadmap#19](https://github.com/li-langverse/roadmap/pull/19) | Governance WP-A5 | ecosystem | **Last** (roadmap) | aligned, human merge | Never auto-close |
| [roadmap#21](https://github.com/li-langverse/roadmap/pull/21) | Governance WP-B4 | httpd canonical | **Last** | aligned, human merge | Never auto-close |
| [lip#43](https://github.com/li-langverse/lip/pull/43) | CI fix | PH-DB-4 | **First** (package) | aligned, **defer** | Prior comment 14:03Z; rebase |

### Newly opened (opener 14:58Z) — labels applied

| PR | Verdict | Action |
|----|---------|--------|
| [lip#46](https://github.com/li-langverse/lip/pull/46)–[#48](https://github.com/li-langverse/lip/pull/48) | needs plan | `plan-needed` added |
| [roadmap#48](https://github.com/li-langverse/roadmap/pull/48) | needs plan | `plan-needed` added (PH-DB-0) |
| [li-language#20](https://github.com/li-langverse/li-language/pull/20) | needs plan | `plan-needed` added (HPC) |
| [li-language#21](https://github.com/li-langverse/li-language/pull/21) | needs plan | `plan-needed` added (Phase 2f) |

### Draft close candidates (11) — deferred

lic#430, #431, #432, #530, #531, #532, #536, #537, #538, #539, #540 — hygiene `safe_now: false`. **#530–#532** carry `merge-approved` — **never close** without explicit supersede. **#536–#540** are plan-doc drafts; confirm abandoned vs active plan work before close.

### Actions log

- **Comments:** [lic#550](https://github.com/li-langverse/lic/pull/550#issuecomment-4583226272) alignment template.
- **Labels:** `plan-needed` on lip#46–48, roadmap#48, li-language#20–21.
- **Closes:** 0 (`prs_safe_close_now=0`).
- **Merges:** 0.

### Error

```
REST API rate limit exhausted (core 0/5000; reset ~2026-05-30T15:18Z UTC per gh api rate_limit).
Scripts pr-merge-queue-plan.py / run-pr-program.py report open_prs=0 while GraphQL search shows ~242 open.
run-pr-program.py background job still running after >5m at digest time — terminate/re-run after REST reset.
Workaround used: gh search prs + gh pr view (GraphQL).
```

## Recommended issues/PRs

| Priority | Repo | Item | Labels / notes |
|----------|------|------|----------------|
| P0 | lip | [#43](https://github.com/li-langverse/lip/pull/43) fix(ci) lis main checkout | Rebase → human APPROVED |
| P0 | roadmap | [#19](https://github.com/li-langverse/roadmap/pull/19), [#21](https://github.com/li-langverse/roadmap/pull/21) | `merge-approved` — **human** merge only |
| P1 | lic | [#437](https://github.com/li-langverse/lic/pull/437) tier-1 matmul | Rebase → pr-review-agent / pr_merger |
| P1 | lic | [#550](https://github.com/li-langverse/lic/pull/550) matmul_blocked verify | Merge after/with #437 |
| P1 | lic | [#530](https://github.com/li-langverse/lic/pull/530)–[#532](https://github.com/li-langverse/lic/pull/532) plan docs | Undraft + APPROVED |
| P2 | lic | [#489](https://github.com/li-langverse/lic/pull/489) httpd perf | Add `plan-approved` |
| P2 | lic | [#517](https://github.com/li-langverse/lic/pull/517) GPU decorators | Add `plan-approved` |
| P2 | lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | `plan-needed` |
| P2 | lip | [#46](https://github.com/li-langverse/lip/pull/46)–[#48](https://github.com/li-langverse/lip/pull/48) | `plan-needed` — plan before merge |
| P2 | roadmap | [#48](https://github.com/li-langverse/roadmap/pull/48) lidb proposal | `plan-needed`, PH-DB-0 |
| P2 | li-language | [#20](https://github.com/li-langverse/li-language/pull/20), [#21](https://github.com/li-langverse/li-language/pull/21) | Large stacks — plan + CI |
| Hygiene | benchmarks | Agent digest cluster (#236–#246) | Dedupe after lic#437 lands |
| Infra | benchmarks | REST fallback in merge-queue scripts | Prevent false `open_prs: 0` |

## Deferred

- Full `run-pr-program.py` / hygiene refresh after REST core reset (~15:18Z UTC).
- **11 draft PRs** — human confirm abandoned; do not batch-close #530–#532 (`merge-approved`).
- **benchmarks** digest wave — dedupe redundant agent PRs after numerics merge.
- **lit#21–#23** dependabot — low priority; merge after package CI stable.
- **lic#551**, **benchmarks#245–#246** — newest agent digests; alignment only if promoted to feature.
- Adding `merge-approved` — **pr-review-agent** only.
- **Merge execution** — **pr_merger** after human APPROVED.
