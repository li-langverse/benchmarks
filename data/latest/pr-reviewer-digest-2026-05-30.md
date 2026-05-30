# PR reviewer digest — 2026-05-30

**Agent:** `pr_reviewer` · **Source:** proactive ecosystem sweep · **Run:** `pr_reviewer-1780124463739` · **Pass:** 2026-05-30T07:01Z · **North star:** proof → easy → fast

## Executive summary

- **GraphQL exhausted** (0/5000, reset ~07:08Z) — `pr-merge-queue-plan.py`, `run-pr-program.py`, and `pr-merge-gate.py` report **0 open PRs** (false negative); **REST** used for live review.
- **7 PRs carry `merge-approved`** (lip#32, lit#18, li-net#12, li-httpd#13, li-std-core#8, li-std-math#9) — all **CI green**; **sole org blocker:** zero human `APPROVED` reviews (`cap-jmk-real` author on all).
- **P0 merge order** (vision tier): lip#32 → lit#18 → agent-kit wave — LLVM 22 CI pin unblocks mirror/toolchain builds.
- **Feature PRs need plan:** lic#494 (PH-HW LKIR), lic#495 (CAD v1) — CI green; **`plan-needed` added** this pass; defer `merge-approved`.
- **benchmarks#201** — CI green but **`mergeable: dirty`** + missing release notes; reviewer comment posted; not `merge-approved`.
- **Red / defer:** lic#496 (CI fail), li-httpd#10 (CI fail + dirty), lic#492 (no checks); **roadmap** PRs — human merge only.
- **Preflight scripts refreshed** at 07:01Z; merge queue empty until GraphQL resets and gates re-run.
- **No merge executed**; no new `merge-approved` labels (prior pass already labeled P0/P1 wave).

## Deliverable / findings

### Preflight (degraded)

| Script | Result | Notes |
|--------|--------|-------|
| `pr-merge-queue-plan.py` | `open_prs=0` | GraphQL — unreliable |
| `run-pr-program.py` | `open_prs=0 ci_green=0` | Same |
| `pr-merge-gate.py --repo lip --pr 32` | `pr_not_found` | Gate script uses GraphQL |
| REST `gh api pulls` | 50+ open across org | Source of truth this pass |

**Error:** `GraphQL: API rate limit already exceeded for user ID 207167228` (reset `2026-05-30T07:08:35Z`).

### P0 — lip#32 · lit#18 — **aligned** (awaiting human approve)

| Gate | Evidence |
|------|----------|
| CI | lip bootstrap SUCCESS; lit test SUCCESS |
| Plan | Chore CI — no `plan-approved` required |
| Vision / PH | P0 package CI — LLVM 22 matches `lic` CMake pin |
| Label | `merge-approved` present |
| Blocker | `mergeable_state: blocked` — branch protection + **0 reviews** |

### P1 — agent-kit wave — **aligned** (awaiting human approve)

| Repo | PR | CI | Label |
|------|-----|-----|-------|
| li-net | [#12](https://github.com/li-langverse/li-net/pull/12) | green | merge-approved |
| li-httpd | [#13](https://github.com/li-langverse/li-httpd/pull/13) | green | merge-approved |
| li-std-core | [#8](https://github.com/li-langverse/li-std-core/pull/8) | green | merge-approved |
| li-std-math | [#9](https://github.com/li-langverse/li-std-math/pull/9) | green | merge-approved |

### lic#494 · lic#495 — **needs plan**

| PR | CI | Action this pass |
|----|-----|------------------|
| [#494 PH-HW LKIR](https://github.com/li-langverse/lic/pull/494) | 7/7 SUCCESS | `plan-needed` label added |
| [#495 CAD fundamentals](https://github.com/li-langverse/lic/pull/495) | 6/6 SUCCESS | `plan-needed` label added |

Release notes present on both; bench evidence on #494. Prior reviewer comments stand — defer `merge-approved` until `plan-approved`.

### benchmarks#201 — **blockers**

| Gate | Status |
|------|--------|
| CI | ✓ SUCCESS |
| Release notes | ✗ missing in diff |
| Mergeable | ✗ dirty (conflicts with `main`) |
| Label | none |

Comment: [benchmarks#201#issuecomment-4582027662](https://github.com/li-langverse/benchmarks/pull/201#issuecomment-4582027662)

**north_star_fit:** domain=ecosystem/governance · PH-5b

### Control-plane

| Agent | Status | Error |
|-------|--------|-------|
| `pr_reviewer-1780124463739` | running | — |
| `pr_merger-1780124441153` | error | `unregistered_running_reconciled` |
| `pr_alignment-1780124441163` | error | `unregistered_running_reconciled` |

Sibling merge agents likely blocked by same GraphQL exhaustion cascade.

### Ecosystem context (briefing 06:58Z)

- **Open PRs (scripts):** 0 — stale due to GraphQL
- **Red benchmarks:** 6 rows (matmul_*, ml_*, num_gmres) — numerics backlog, not PR blockers
- **Dirty workspace:** `lic` on `cursor/httpd-plan-continue` (5 files) — unrelated to merge queue

## Recommended issues/PRs

| Priority | Repo | Item | Labels / action |
|----------|------|------|-----------------|
| P0 | lip | [#32](https://github.com/li-langverse/lip/pull/32) fix(ci): LLVM 22 | `merge-approved` → human **Approve** |
| P0 | lit | [#18](https://github.com/li-langverse/lit/pull/18) fix(ci): LLVM 22 | `merge-approved` → human **Approve** |
| P1 | li-net | [#12](https://github.com/li-langverse/li-net/pull/12) agent-kit sync | `merge-approved` → human **Approve** |
| P1 | li-httpd | [#13](https://github.com/li-langverse/li-httpd/pull/13) agent-kit sync | `merge-approved` → human **Approve** |
| P1 | li-std-core | [#8](https://github.com/li-langverse/li-std-core/pull/8) agent-kit sync | `merge-approved` → human **Approve** |
| P1 | li-std-math | [#9](https://github.com/li-langverse/li-std-math/pull/9) agent-kit sync | `merge-approved` → human **Approve** |
| P2 | lic | [#494](https://github.com/li-langverse/lic/pull/494) PH-HW LKIR | `plan-needed` → add `plan-approved` |
| P2 | lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | `plan-needed` → add `plan-approved` |
| P2 | benchmarks | [#201](https://github.com/li-langverse/benchmarks/pull/201) repo boundaries | release notes + rebase → standards pass |
| hygiene | benchmarks/lic | workspace sweep fallback PRs | close redundant stack (`pr_branch_opener`) |

## Deferred

- Re-run `run-pr-program.py` + `pr-merge-gate.py` after GraphQL reset (~07:08Z).
- **`pr_merger`** until non-author `APPROVED` on P0/P1 wave (7 labeled, 0 gate-ready per scripts).
- **lic#492**, **lic#496**, **li-httpd#10** — not CI-green merge candidates.
- **roadmap** merges — human only per policy.
- **132+ branches** without open PR — `pr_branch_opener` backlog; do not merge stale sweep fallbacks.
- Stagger org GraphQL sweeps to avoid exhausting quota and blocking gate scripts.
