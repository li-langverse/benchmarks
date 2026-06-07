# PR alignment digest — 2026-05-30T09:30Z

**Agent:** `pr_alignment` · **Source:** proactive ecosystem sweep · **North star:** proof → easy → fast (PH-5b, PH-7e, Phase 2i)

## Executive summary

- **172 open org PRs** (`ecosystem-audit.json`); merge-queue JSON still reports **`open_prs=0`** / empty `merge_sequence` until `pr-merge-gate` enrichment completes (slow org sweep; `run-pr-program.py` >5m in flight).
- **Vision merge order:** mirrors / lip / lit / agent-kit → benchmarks → lic → roadmap (roadmap never auto-close).
- **Numerics canonical:** [lic#499](https://github.com/li-langverse/lic/pull/499) — tier-1 matmul MIR restore (PH-5b/7e); **aligned**, **defer** until `build-and-test` green; supersedes bench_improver stub stack.
- **Closed 5 superseded PRs:** lic#509–#513 (agent bench_improver deliverable stubs) → pointer to lic#499 (follows prior close of #504–#508).
- **Feature blocked:** [lic#517](https://github.com/li-langverse/lic/pull/517) Studio GPU decorators — **needs plan** (alignment comment posted); [lic#495](https://github.com/li-langverse/lic/pull/495) CAD v1 still `plan-needed`.
- **P0 merge-approved (no merge this run):** [lip#32](https://github.com/li-langverse/lip/pull/32), [lit#18](https://github.com/li-langverse/lit/pull/18), [li-net#12](https://github.com/li-langverse/li-net/pull/12) — human `review_approved` / pr_merger only.
- **Digest aligned:** [benchmarks#208](https://github.com/li-langverse/benchmarks/pull/208) matmul tier-1 greens evidence — pairs with lic#499, not a substitute.
- **Hygiene:** `pr-branch-hygiene.json` — 39 branches without PR, 12 draft PRs flagged `prs_recommended_close` but **`prs_safe_close_now=0`** (no auto-close).
- **No `merge-approved` added**; **no merges** (alignment agent mandate).

## Deliverable / findings

### Preflight

| Artifact | `generated_at` | Key signal |
|----------|----------------|------------|
| `pr-merge-queue-plan.json` | 2026-05-30T09:08Z | `merge_sequence=[]`, `open_prs=0` (stale vs REST) |
| `pr-program-run.json` | 2026-05-30T09:05Z | `all_open=[]` (stale; re-run in progress) |
| `pr-branch-hygiene.json` | 2026-05-30T08:46Z | `branches_needing_pr=39`, `prs_safe_close_now=0`, 12 draft close candidates |
| `issue-feature-triage.json` | 2026-05-30T09:16Z | `needs_plan=40` (lic), 11 (benchmarks) |
| `ecosystem-audit.json` | 2026-05-30T09:19Z | `open_prs=172`, `ready_prs=70`, `failed_prs=48` |

`pr-merge-queue-plan.py` refreshed; `pr-branch-hygiene.py` + full `run-pr-program.py` started at 09:16Z — gate enrichment still running at digest time.

### Per-PR alignment (sampled 8)

| PR | Plan | PH / PKG | Merge order | Verdict | Action taken |
|----|------|----------|-------------|---------|--------------|
| [lic#499](https://github.com/li-langverse/lic/pull/499) | Bench regression fix | PH-5b, PH-7e | After package wave | aligned, **defer** (CI red) | Prior alignment comments stand |
| [lic#503](https://github.com/li-langverse/lic/pull/503) | Bench improver stack | PH-5b, PH-7e | — | superseded / defer | Prefer #499; no checks on branch yet |
| [lic#437](https://github.com/li-langverse/lic/pull/437) | Perf matmul | PH-5b, PH-7e | After #499 | defer | `merge-approved` + **CONFLICTING** — reconcile with #499 |
| [lic#517](https://github.com/li-langverse/lic/pull/517) | **needs plan** | PH-7d, G-par | After lic core | needs plan | Comment |
| [lic#495](https://github.com/li-langverse/lic/pull/495) | **needs plan** | PH-CAD / AL-4 | After plan gate | needs plan | Keep `plan-needed` (prior comment) |
| [benchmarks#208](https://github.com/li-langverse/benchmarks/pull/208) | Agent digest | PH-5b, PH-7e | After mirrors | aligned (digest) | Comment |
| [lip#32](https://github.com/li-langverse/lip/pull/32) | CI chore | Platform | **First** | aligned | No action (prior pass) |
| [lit#18](https://github.com/li-langverse/lit/pull/18) | CI chore | Platform | **First** | aligned | No action (prior pass) |

### Red bench rows (unchanged)

`matmul_blocked` 1.55×, `matmul_naive` 1.33×, ML forwards 1.33×, `num_gmres` 1.4× vs cpp — do not relax `catalog.toml` thresholds until lic#499 lands green.

### north_star_fit

- **Domain:** Scientific numerics / tier-1 codegen (PH-5b, PH-7e).
- **PH ids:** PH-5b (benchmark catalog), PH-7e (math→SIMD lowering), Phase 2i partial (linalg surface).
- **Proof-before-perf:** lic#517 blocked on plan; no merge-approved on feature stacks.

## Recommended issues/PRs

| Priority | Repo | Item | Labels / notes |
|----------|------|------|----------------|
| P0 | lip | [#32](https://github.com/li-langverse/lip/pull/32) fix(ci) LLVM 22 | `merge-approved` — human approve → pr_merger |
| P0 | lit | [#18](https://github.com/li-langverse/lit/pull/18) fix(ci) LLVM 22 | `merge-approved` — human approve |
| P0 | li-net | [#12](https://github.com/li-langverse/li-net/pull/12) agent-kit sync | `merge-approved` |
| P1 | lic | [#499](https://github.com/li-langverse/lic/pull/499) matmul MIR restore | `numerics-research` — fix `build-and-test`, then pr-review-agent |
| P1 | lic | [#437](https://github.com/li-langverse/lic/pull/437) perf matmul | Reconcile with #499 before merge |
| P2 | lic | [#463](https://github.com/li-langverse/lic/issues/463) tier-1 red benchmarks | `plan-needed` / master-plan-gap |
| P2 | lic | [#517](https://github.com/li-langverse/lic/pull/517) GPU decorators | needs `plan-approved` |
| P2 | lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | `plan-needed` |
| Hygiene | lic | #514, #516 bench_improver / sweep | Close after #499 lands (next pass) |
| Hygiene | benchmarks | Draft #123–#183, agent digest wave | `safe_now=0` — human confirm abandoned drafts |
| Governance | lic | [#476](https://github.com/li-langverse/lic/issues/476) PH-Pkg governance | `plan-needed` |

## Deferred

- Full `run-pr-program.py` completion (org-scale gate enrichment; prior JSON stale).
- `plan_audit`, slow `pr_branch_hygiene` refresh (`--skip-slow` in briefing preflight).
- **roadmap** PRs with `merge-approved` (#19–#21) — human merge only; never auto-close.
- **lic#503**, **lic#514**, **lic#516** — supersede or merge after #499 CI green.
- **benchmarks** workspace-sweep / digest PR backlog — dedupe after numerics unblocked.
- Adding `merge-approved` — **pr-review-agent** only.
- **Merge execution** — **pr_merger** after human APPROVED.

## Actions log

| Action | PRs |
|--------|-----|
| Alignment comment | lic#517, benchmarks#208 |
| Closed (superseded) | lic#509, #510, #511, #512, #513 → canonical lic#499 |
