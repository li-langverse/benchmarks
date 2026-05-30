# PR reviewer digest — 2026-05-30

**Agent:** `pr_reviewer` · **Source:** proactive ecosystem sweep · **North star:** proof → easy → fast · **Pass:** 2026-05-30T06:40Z

## Executive summary

- **GraphQL rate limit exhausted** (5000/5000, reset ~07:08Z) — `pr-merge-gate.py`, `run-pr-program.py`, and `gh pr list` returned **0 open PRs** (false negative); used **REST API** for live review.
- **New merge-approved:** [lip#32](https://github.com/li-langverse/lip/pull/32), [lit#18](https://github.com/li-langverse/lit/pull/18) — P0 LLVM 22 CI pin; CI green, standards aligned.
- **Agent-kit wave (5 PRs)** already labeled `merge-approved` — CI green; **sole blocker:** no human `APPROVED` review on any (`cap-jmk-real` author).
- **Feature PRs blocked on plan:** [lic#494](https://github.com/li-langverse/lic/pull/494) (PH-HW), [lic#495](https://github.com/li-langverse/lic/pull/495) (CAD/AL-4) — CI green but missing `plan-approved`.
- **[benchmarks#201](https://github.com/li-langverse/benchmarks/pull/201)** — CI green repo-boundary cleanup; needs full standards pass + release-notes check before `merge-approved`.
- **Redundant stacks:** 10+ `workspace sweep fallback` PRs on benchmarks/lic — defer/close via `pr_branch_opener` hygiene, not merge queue.
- **No merge executed**; roadmap/governance repos untouched per policy.
- **Control-plane:** sibling agents (`pr_merger`, `pr_alignment`) errored same tick — likely GraphQL cascade.

## Deliverable / findings

### Preflight (degraded)

| Script | Result | Notes |
|--------|--------|-------|
| `pr-merge-queue-plan.py` | `open_prs=0` | GraphQL blocked — unreliable |
| `run-pr-program.py` | `open_prs=0 ci_green=0` | Same |
| `pr-merge-gate.py` | `pr_not_found` | Gate script uses GraphQL |
| REST `gh api pulls` | 50+ open across org | Source of truth this pass |

**Error:** `GraphQL: API rate limit already exceeded for user ID 207167228` (core REST remaining: 4953/5000).

### lip#32 · lit#18 — **aligned** ✓

| Gate | Evidence |
|------|----------|
| CI | lip bootstrap SUCCESS; lit test SUCCESS |
| Plan | Chore CI fix — no `plan-approved` required |
| Vision / PH | P0 package CI — LLVM 22 matches `lic` CMake pin |
| Strict by default | `.github/workflows/ci.yml`, `scripts/ci-install-llvm.sh` only |
| Security | N/A |
| Performance | N/A |
| Release notes | N/A (chore) |
| Ecosystem-first | Same pattern as lic org CI |

**Actions taken:** `merge-approved` label added; review comment posted.

**Blocker:** `reviewDecision: REVIEW_REQUIRED` — human Approve → `pr_merger`.

**Merge order:** lip#32 → lit#18 → agent-kit wave (vision: mirrors before lic).

### Agent-kit wave — **aligned, awaiting human approve**

| Repo | PR | CI | Label |
|------|-----|-----|-------|
| li-net | [#12](https://github.com/li-langverse/li-net/pull/12) | green | merge-approved |
| li-httpd | [#13](https://github.com/li-langverse/li-httpd/pull/13) | green | merge-approved |
| li-std-core | [#8](https://github.com/li-langverse/li-std-core/pull/8) | green | merge-approved |
| li-std-math | [#9](https://github.com/li-langverse/li-std-math/pull/9) | green | merge-approved |
| li-std-math | [#7](https://github.com/li-langverse/li-std-math/pull/7) | green | merge-approved (deps) |

**Blocker:** 0 PR reviews org-wide on this wave. Comment refreshed on li-httpd#13.

### lic#494 · lic#495 — **needs plan**

| PR | CI | Blocker |
|----|-----|---------|
| [#494 PH-HW LKIR](https://github.com/li-langverse/lic/pull/494) | 7/7 SUCCESS | missing `plan-approved` |
| [#495 CAD fundamentals](https://github.com/li-langverse/lic/pull/495) | 6/6 SUCCESS | missing `plan-approved` |

Release notes present; bench evidence on #494. Comments posted — defer `merge-approved` until planner adds label.

### lic#492 · lic#496 · li-httpd#10 — **defer**

| PR | Status |
|----|--------|
| lic#492 PH-ML Wave 1 | 0 CI checks — not CI-green |
| lic#496 PH-CAD types | CI fail (build-and-test) |
| li-httpd#10 feature | CI fail; needs `plan-approved` |

### benchmarks#201 — **pending review**

CI green (dashboard-build, ingest-smoke). Cross-cutting repo-boundary + proof-posture removal. Needs CHANGELOG/release-notes verification and scope review before label.

**north_star_fit:** domain=ecosystem/governance · PH-5b (catalog boundaries)

## Recommended issues/PRs

| Priority | Repo | Item | Labels / action |
|----------|------|------|-----------------|
| P0 | lip | [#32](https://github.com/li-langverse/lip/pull/32) fix(ci): LLVM 22 | `merge-approved` → human **Approve** |
| P0 | lit | [#18](https://github.com/li-langverse/lit/pull/18) fix(ci): LLVM 22 | `merge-approved` → human **Approve** |
| P1 | li-net | [#12](https://github.com/li-langverse/li-net/pull/12) agent-kit sync | `merge-approved` → human **Approve** |
| P1 | li-httpd | [#13](https://github.com/li-langverse/li-httpd/pull/13) agent-kit sync | `merge-approved` → human **Approve** |
| P1 | li-std-core | [#8](https://github.com/li-langverse/li-std-core/pull/8) agent-kit sync | `merge-approved` → human **Approve** |
| P1 | li-std-math | [#9](https://github.com/li-langverse/li-std-math/pull/9) agent-kit sync | `merge-approved` → human **Approve** |
| P2 | lic | [#494](https://github.com/li-langverse/lic/pull/494) PH-HW LKIR | add `plan-approved` |
| P2 | lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | add `plan-approved` |
| P2 | benchmarks | [#201](https://github.com/li-langverse/benchmarks/pull/201) repo boundaries | standards pass pending |
| hygiene | benchmarks/lic | workspace sweep fallback PRs | close redundant stack |

## Deferred

- Re-run `run-pr-program.py` + `pr-merge-gate.py` after GraphQL reset (~07:08Z).
- Auto-merge until non-author `APPROVED` on P0/P1 wave (7 PRs with `merge-approved`, 0 gate-ready).
- **lic#492**, **lic#496**, **li-httpd#10** — CI red or pending; not merge candidates.
- **roadmap** merges — human only per policy.
- **167 branches** without open PR — `pr_branch_opener` backlog; do not merge stale sweep fallbacks.
- Rate-limit guard: stagger org sweeps to avoid GraphQL exhaustion blocking gate scripts.
