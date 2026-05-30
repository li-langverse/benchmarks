# PR reviewer digest — 2026-05-30T09:56Z

**Agent:** `pr_reviewer` · **Source:** proactive ecosystem sweep · **North star:** proof → easy → fast (PH-5b, PH-7e, Phase 2i/7e)

## Executive summary

- **Preflight refreshed:** `pr-merge-queue-plan.json` and `pr-program-run.json` at 09:56Z — both report **`open_prs=0`** because org `gh pr list` uses **GraphQL (0 remaining)**; REST search still shows **50+ open PRs** (audit undercount).
- **No `merge-approved` added** this run (mandate: reviewer adds only after full standards + human APPROVED).
- **P0 queue (already labeled):** [lip#32](https://github.com/li-langverse/lip/pull/32), [lit#18](https://github.com/li-langverse/lit/pull/18), [li-net#12](https://github.com/li-langverse/li-net/pull/12) — CI green via REST, **`merge-approved` present**, **no GitHub APPROVED review** → **pr_merger** blocked on `review_approved`.
- **Best new CI-green candidate:** [lic#524](https://github.com/li-langverse/lic/pull/524) — tier-1 `matmul_blocked` harness + release notes; **defer label** until [lic#499](https://github.com/li-langverse/lic/pull/499) MIR restore merges (stack order).
- **Numerics canonical blocked:** lic#499 — `build-and-test` / macOS **failure**; lic#520 merge conflicts; do not weaken `catalog.toml` (yellow: `matmul_blocked`, `matmul_naive`).
- **Platform hygiene:** [benchmarks#215](https://github.com/li-langverse/benchmarks/pull/215) CI green but **mergeable=false**; [benchmarks#216](https://github.com/li-langverse/benchmarks/pull/216) agent-kit digest — conflicts, no label.
- **Feature gates:** [lic#517](https://github.com/li-langverse/lic/pull/517) GPU decorators, [lic#495](https://github.com/li-langverse/lic/pull/495) CAD — `plan-needed` without `plan-approved` → not merge-ready.
- **Error (non-fatal):** GraphQL quota exhausted during `pr-merge-gate.py` / `run-pr-program.py` enumeration → `pr_not_found` false negatives; use REST until reset (~09:68Z epoch).

## Deliverable / findings

### Preflight artifacts

| Artifact | `generated_at` | Signal |
|----------|----------------|--------|
| `pr-merge-queue-plan.json` | 2026-05-30T09:56Z | Empty `merge_sequence`; stale `open_prs=0` |
| `pr-program-run.json` | 2026-05-30T09:56Z | `all_open=[]`, `ci_green=0` (GraphQL starvation) |
| `pr-branch-hygiene.json` | 2026-05-30T09:35Z | 11 draft PRs → close candidates, **`safe_now=0`** |
| `ecosystem-audit.json` | 2026-05-30T09:46Z | Bench yellow: `matmul_blocked`, `matmul_naive`; 20 green |
| `local-ci-results.json` | 2026-05-30T09:23Z | **lic#439** failed (`li-tests` 2 failed) |

### Standards checklist (sampled CI-green / merge-approved)

| PR | Vision / PH | Strict / proof | Security | Performance | Release notes | Verdict |
|----|-------------|----------------|----------|-------------|---------------|---------|
| lip#32 | Platform LLVM pin | N/A chore | N/A | N/A | N/A chore | **gate-ready*** — needs APPROVED |
| lit#18 | Platform LLVM pin | N/A chore | N/A | N/A | N/A chore | **gate-ready*** — needs APPROVED |
| li-net#12 | Agent-kit sync | N/A chore | N/A | N/A | N/A | **gate-ready*** — needs APPROVED |
| lic#524 | PH-5b, PH-7e | Harness only | N/A | Evidence ≤1.2× local | ✅ release-notes | **aligned, defer** (after #499) |
| lic#499 | PH-5b, PH-7e | MIR restore | N/A | Bench evidence | ✅ study doc | **aligned, CI red** |
| lic#517 | PH-7d | Feature | TBD | TBD | TBD | **needs plan** |
| lic#495 | PH-CAD | Feature | TBD | TBD | TBD | **needs plan** |
| benchmarks#215 | Ecosystem CI | Audit fix | N/A | N/A | Digest only | **aligned, conflicts** |
| lic#439 | — | — | — | — | — | **block** local-ci fail |

\* `merge-approved` label already on lip#32, lit#18, li-net#12.

### Gate script (REST-verified; GraphQL gate unreliable)

```text
lip#32:   merge-approved ✓  CI success ✓  mergeable true  review: none
lit#18:  merge-approved ✓  CI success ✓  mergeable true  review: none
li-net#12: merge-approved ✓  CI success ✓  mergeable true  review: none
lic#524:  no label  CI success ✓  mergeable true  review: none
lic#499:  numerics-research  CI fail (build-and-test)
```

### north_star_fit

- **Domain:** Scientific numerics + platform CI (tier-1 codegen, package mirrors).
- **PH ids:** PH-5b (benchmark catalog), PH-7e (math→SIMD lowering), Phase 2i partial (linalg).
- **Proof-before-perf:** No `merge-approved` on feature stacks (#517, #495); numerics stack ordered #499 → #524.

### Actions taken

| Action | Target |
|--------|--------|
| Review comment | [lic#524](https://github.com/li-langverse/lic/pull/524#issuecomment) — defer until #499 |
| Review comment | [lip#32](https://github.com/li-langverse/lip/pull/32#issuecomment) — needs APPROVED |
| Label `merge-approved` | **none** (stack / review blockers) |

## Recommended issues/PRs

| Priority | Repo | Item | Labels / next step |
|----------|------|------|-------------------|
| P0 | lip | [#32](https://github.com/li-langverse/lip/pull/32) fix(ci) LLVM 22 | `merge-approved` → **human APPROVED** → pr_merger |
| P0 | lit | [#18](https://github.com/li-langverse/lit/pull/18) fix(ci) LLVM 22 | same |
| P0 | li-net | [#12](https://github.com/li-langverse/li-net/pull/12) agent-kit sync | same |
| P1 | lic | [#499](https://github.com/li-langverse/lic/pull/499) matmul MIR restore | Fix `build-and-test`, then pr-review-agent |
| P1 | lic | [#524](https://github.com/li-langverse/lic/pull/524) matmul_blocked harness | After #499; then `merge-approved` |
| P2 | benchmarks | [#215](https://github.com/li-langverse/benchmarks/pull/215) ecosystem-audit GraphQL fallback | Resolve conflicts, then review |
| P2 | lic | [#439](https://github.com/li-langverse/lic/pull/439) | Fix local-ci / GHA before review |
| P2 | lic | [#517](https://github.com/li-langverse/lic/pull/517) GPU decorators | `plan-approved` required |
| P2 | lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | `plan-needed` |
| Hygiene | org | 11 draft PRs (lic#430–432, benchmarks#128–209, roadmap#26) | Human confirm abandoned → close |
| Governance | roadmap | Open PRs #43–45 | **Human merge only** — never auto-merge |

## Deferred

- Full `run-pr-program.py` org enumeration until **GraphQL resets** (~1780135734).
- Adding `merge-approved` to lic#524 until lic#499 lands and human review completes.
- **Merge execution** — **pr_merger** only after `reviewDecision: APPROVED`.
- **roadmap** / governance repos — human merge per policy.
- **benchmarks#216** (current workspace branch) — resolve conflicts with main before review.
- Re-run `pr-merge-gate.py --json` on P0 trio after GraphQL recovery for authoritative `ready: true`.

## Error

**GitHub GraphQL rate limit exhausted** (`used: 5000/5000`) during proactive sweep. Symptom: `pr-merge-gate.py` returned `pr_not_found` for valid PRs; `ecosystem-audit.json` / `pr-program-run.json` report `open_prs=0`. **Mitigation:** REST `gh api` used for this digest; re-run gate scripts after reset. **Stack trace:** N/A (API 403 on GraphQL, not Python exception).
