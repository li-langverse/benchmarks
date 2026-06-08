# PR alignment digest — 2026-05-30T14:03Z

**Agent:** `pr_alignment` · **Source:** proactive ecosystem sweep · **Run:** `pr_alignment-1780149270160`  
**north_star_fit:** Scientific numerics + governance (PH-5b, PH-7e, Phase 2i, PH-7d) — proof → easy → fast

## Executive summary

- **≥200 open org PRs** (`gh search prs` REST); gate JSON falsely reports **`open_prs: 0`** while **GraphQL quota exhausted** (5000/5000).
- **Vision merge order:** package CI / mirrors → benchmarks → lic → lip/lit/lis → roadmap (roadmap never auto-close).
- **Canonical tier-1 matmul:** [lic#437](https://github.com/li-langverse/lic/pull/437) — `merge-approved`, **aligned**, **defer** (`mergeable_state: dirty`); superseded stack [#541](https://github.com/li-langverse/lic/pull/541) / [#542](https://github.com/li-langverse/lic/pull/542) / [#544](https://github.com/li-langverse/lic/pull/544) **closed**.
- **Feature blocked (needs plan):** [lic#489](https://github.com/li-langverse/lic/pull/489), [#517](https://github.com/li-langverse/lic/pull/517), [#495](https://github.com/li-langverse/lic/pull/495) — `plan-needed` without `plan-approved` (prior alignment comments stand).
- **Draft + `merge-approved`:** lic#530–#532 — content aligned; **defer** until undraft (comments posted this run via REST).
- **Package CI:** [lip#43](https://github.com/li-langverse/lip/pull/43) — **aligned**, blocked mergeable; alignment comment posted.
- **Hygiene:** 14 draft PRs in `prs_recommended_close`; **`prs_safe_close_now: 0`** — **0 closes** this run.
- **No merges, no `merge-approved` added** (alignment agent mandate).

## Deliverable / findings

### Preflight

| Artifact | `generated_at` | Key signal |
|----------|----------------|------------|
| `pr-merge-queue-plan.json` | 2026-05-30T13:56Z | `open_prs=0`, `merge_sequence=[]` — **false negative** (GraphQL) |
| `pr-program-run.json` | 2026-05-30T12:52Z | Stale; `run-pr-program.py` killed after >7m (GraphQL path) |
| `pr-branch-hygiene.json` | 2026-05-30T13:37Z | 14 draft close candidates, `prs_safe_close_now=0` |
| `issue-feature-triage.json` | 2026-05-30T14:01Z | **gh failed** at tail of sweep (`needs_plan=0` erroneous) |
| `ecosystem-audit.json` | 2026-05-30T13:56Z | `open_prs=0` (same GraphQL gap); bench yellow: `matmul_*` |

Prior reliable snapshot: `pr_reviewer-1780148640861` (13:44Z) — 93 open, 82 redundant pairs, 0 gate-ready.

### Per-PR alignment (sampled 8)

| PR | Plan | PH / PKG | Merge order | Verdict | Action |
|----|------|----------|-------------|---------|--------|
| [lic#437](https://github.com/li-langverse/lic/pull/437) | Bench perf fix | PH-5b, PH-7e | After package wave | aligned, **defer** (dirty) | Prior comments; no close |
| [lic#489](https://github.com/li-langverse/lic/pull/489) | **needs plan** | httpd gap-phase2 | After `plan-approved` | needs plan | Prior comment 12:50Z |
| [lic#517](https://github.com/li-langverse/lic/pull/517) | **needs plan** | PH-7d, G-par | After lic core | needs plan | Prior comment 09:27Z |
| [lic#530](https://github.com/li-langverse/lic/pull/530) | Plan doc (#472) | PH-2i/2f | Parallel governance | aligned, **defer** (draft) | REST comment 14:03Z |
| [roadmap#19](https://github.com/li-langverse/roadmap/pull/19) | Governance WP-A5 | ecosystem | **Last** (roadmap) | aligned, human merge | Never auto-close |
| [roadmap#21](https://github.com/li-langverse/roadmap/pull/21) | Governance WP-B4 | httpd canonical | **Last** | aligned, human merge | dirty — rebase |
| [lip#43](https://github.com/li-langverse/lip/pull/43) | CI fix | PH-DB-4 | **First** (package) | aligned, **defer** (blocked) | REST comment 14:03Z |
| [benchmarks#204](https://github.com/li-langverse/benchmarks/pull/204) | Agent digest | agent-kit | After mirrors | aligned (digest) | Dedupe vs #236–#239 cluster |

### Red bench signal (catalog)

`matmul_blocked`, `matmul_naive` **yellow** in fresh `ecosystem-audit.json` (09:25Z harness) — do not relax thresholds until lic#437 lands green after rebase.

### Actions log

- **Comments (REST):** lip#43; lic#530, #531, #532.
- **Closes:** 0 (`safe_now=0`; no redundant bot duplicates with clear survivor).
- **Labels:** 0 added (`merge-approved` is pr-review-agent).

### Error

```
GraphQL API rate limit exhausted (used 5000/5000). Scripts using `gh pr list` /
GraphQL return open_prs=0. Workaround: `gh search prs` + `gh api repos/.../pulls/N`
(REST). run-pr-program.py exceeded 7m — terminated. Re-run merge-queue-plan after
GraphQL reset (~2026-05-30T14:29Z per rate_limit.reset).
```

## Recommended issues/PRs

| Priority | Repo | Item | Labels / notes |
|----------|------|------|----------------|
| P0 | lip | [#43](https://github.com/li-langverse/lip/pull/43) fix(ci) lis main checkout | Rebase → human APPROVED |
| P0 | roadmap | [#19](https://github.com/li-langverse/roadmap/pull/19), [#21](https://github.com/li-langverse/roadmap/pull/21) | `merge-approved` — **human** merge only |
| P1 | lic | [#437](https://github.com/li-langverse/lic/pull/437) tier-1 matmul | Rebase → pr-review-agent / pr_merger |
| P1 | lic | [#530](https://github.com/li-langverse/lic/pull/530)–[#532](https://github.com/li-langverse/lic/pull/532) plan docs | Undraft + APPROVED |
| P2 | lic | [#489](https://github.com/li-langverse/lic/pull/489) httpd perf | Add `plan-approved` |
| P2 | lic | [#517](https://github.com/li-langverse/lic/pull/517) GPU decorators | Add `plan-approved` |
| P2 | lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | `plan-needed` |
| Hygiene | benchmarks | ~40 open agent digest PRs | Batch-close redundant pairs after numerics |
| Governance | lic | [#476](https://github.com/li-langverse/lic/issues/476) PH-Pkg governance | `plan-needed` (when triage REST recovers) |
| Infra | benchmarks | REST fallback in `pr-merge-queue-plan.py` | Prevent false `open_prs: 0` |

## Deferred

- Full `run-pr-program.py` / GraphQL merge-queue refresh after quota reset.
- **82 redundant pairs** from 13:37Z plan — human batch-close (no `safe_now`).
- **14 draft PRs** in hygiene JSON — confirm abandoned before close.
- **benchmarks** workspace-sweep / digest wave (#204–#239) — dedupe after lic#437.
- **lis#20**, **li-httpd#10** — `plan-needed` feature stacks.
- Adding `merge-approved` — **pr-review-agent** only.
- **Merge execution** — **pr_merger** after human APPROVED.
