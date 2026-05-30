# PR reviewer digest — 2026-05-30

**Agent:** `pr_reviewer` · **Source:** proactive ecosystem sweep · **Run:** `pr_reviewer-1780127006850` · **Pass:** 2026-05-30T07:44Z · **North star:** proof → easy → fast

## Executive summary

- **GraphQL still exhausted** (0/5000) — `pr-merge-queue-plan.py` / `run-pr-program.py` / `pr-merge-gate.py` report **0 open PRs** (false negative); **REST** used for live review.
- **P0 merge queue:** [lip#32](https://github.com/li-langverse/lip/pull/32) + [lit#18](https://github.com/li-langverse/lit/pull/18) — CI green, `merge-approved` present; **blocker:** zero human `APPROVED` reviews.
- **New `merge-approved` this pass:** [lic-docs#1](https://github.com/li-langverse/lic-docs/pull/1) — org `ci.yml` rollout; CI green; awaits human approve.
- **Numerics hot path:** [lic#499](https://github.com/li-langverse/lic/pull/499) PH-5b/7e matmul restore — release notes ✓, **CI red** (`build-and-test`, macOS); defer merge.
- **Feature plan gate:** [lic#495](https://github.com/li-langverse/lic/pull/495) — CI green but **`plan-needed` without `plan-approved`** + merge conflicts.
- **Ecosystem hygiene:** [benchmarks#201](https://github.com/li-langverse/benchmarks/pull/201) — CI green, **`mergeable: dirty`**; reviewer comment posted.
- **~30 redundant** `workspace sweep fallback` PRs across lic/benchmarks — close stack, do not merge.
- **No merge executed**; roadmap PRs remain human-only.

## Deliverable / findings

### Preflight (degraded)

| Script | Result | Notes |
|--------|--------|-------|
| `pr-merge-queue-plan.py` | `open_prs=0` | GraphQL — unreliable |
| `run-pr-program.py` | `open_prs=0 ci_green=0` | Same |
| `pr-merge-gate.py` | `pr_not_found` on all probes | Gate script uses GraphQL `gh pr view` |
| REST `gh api pulls` / `check-runs` | 50+ open org-wide | Source of truth this pass |

**Error:** `GraphQL: API rate limit already exceeded for user ID 207167228` (core REST ~4648/5000 OK).

### CI-green + aligned (awaiting human approve)

| Repo | PR | CI | Label | Blocker |
|------|-----|-----|-------|---------|
| lip | [#32](https://github.com/li-langverse/lip/pull/32) LLVM 22 CI | 1/1 ✓ | merge-approved | No APPROVED review |
| lit | [#18](https://github.com/li-langverse/lit/pull/18) LLVM 22 CI | 1/1 ✓ | merge-approved | No APPROVED review |
| lic-docs | [#1](https://github.com/li-langverse/lic-docs/pull/1) org ci.yml | 1/1 ✓ | **merge-approved added** | No APPROVED review |

Reviewer comments: [lip#32](https://github.com/li-langverse/lip/pull/32#issuecomment-4582141596), [lit#18](https://github.com/li-langverse/lit/pull/18#issuecomment-4582141630), [lic-docs#1](https://github.com/li-langverse/lic-docs/pull/1#issuecomment-4582141699).

### Defer — blockers posted

| Repo | PR | Verdict | Blocker |
|------|-----|---------|---------|
| lic | [#499](https://github.com/li-langverse/lic/pull/499) matmul PH-5b/7e | defer | CI fail (5/7 pass) |
| lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | needs plan | `plan-needed`, dirty merge |
| lic | [#496](https://github.com/li-langverse/lic/pull/496) PH-CAD types | defer | CI fail |
| benchmarks | [#201](https://github.com/li-langverse/benchmarks/pull/201) repo boundaries | defer | merge conflicts (dirty) |

Comments: [#499](https://github.com/li-langverse/lic/pull/499#issuecomment-4582141919), [#495](https://github.com/li-langverse/lic/pull/495#issuecomment-4582141944), [#496](https://github.com/li-langverse/lic/pull/496#issuecomment-4582141971), [#201](https://github.com/li-langverse/benchmarks/pull/201#issuecomment-4582142000).

### Checklist notes (org-wide)

| Gate | Status |
|------|--------|
| Vision / PH | P0 LLVM pin = ecosystem CI (easy); #499/#495 trace PH-5b/7e, AL-4 CAD |
| Strict by default | No `trusted.lean` creep in reviewed PRs |
| Security | N/A on CI/chore PRs; #489 httpd surface not reviewed (0 checks) |
| Performance | #499 targets red matmul rows — must not merge on red CI |
| Release notes | #499, #495, #496 have `docs/release-notes/*`; #201 missing (prior pass) |
| Ecosystem-first | Gate scripts blocked — used REST + org `pr-merge-gate.py` policy manually |

### Redundant / hygiene

- **30** open PRs titled `workspace sweep fallback` (lic + benchmarks) — superseded stack; `pr_branch_opener` should close after newest sweep lands.
- **roadmap#38**, **roadmap#39** — governance repo; **human merge only**; no `merge-approved`.

### Control-plane

| Agent | Status |
|-------|--------|
| `pr_reviewer-1780127006850` | running (this pass) |
| Prior `pr_reviewer` / `pr_merger` runs | error cascade (`unregistered_running_reconciled`) — likely GraphQL exhaustion |

**north_star_fit:** domain=ecosystem/platform · PH=CI infra (P0), PH-5b/7e (#499), AL-4 (#495)

## Recommended issues/PRs

| Priority | Repo | Item | Labels / action |
|----------|------|------|-----------------|
| P0 | lip | [#32](https://github.com/li-langverse/lip/pull/32) fix(ci): LLVM 22 | `merge-approved` → human **Approve** |
| P0 | lit | [#18](https://github.com/li-langverse/lit/pull/18) fix(ci): LLVM 22 | `merge-approved` → human **Approve** |
| P1 | lic-docs | [#1](https://github.com/li-langverse/lic-docs/pull/1) org ci.yml | `merge-approved` (new) → human **Approve** |
| P2 | lic | [#499](https://github.com/li-langverse/lic/pull/499) matmul tier-1 | `numerics-research` → fix CI, then review |
| P2 | lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | `plan-needed` → add `plan-approved`, rebase |
| P2 | benchmarks | [#201](https://github.com/li-langverse/benchmarks/pull/201) repo boundaries | resolve conflicts + release notes |
| hygiene | lic/benchmarks | workspace sweep fallback ×30 | close redundant stack |
| backlog | lic | [#488](https://github.com/li-langverse/lic/pull/488) provability mat2 VC | 0 CI checks — trigger workflows |

## Deferred

- Re-run `run-pr-program.py` + `pr-merge-gate.py` after GraphQL reset.
- **`pr_merger`** until non-author `APPROVED` on P0/P1 wave (lip, lit, lic-docs, prior agent-kit wave).
- **lic#499**, **lic#496** — not merge candidates until CI green.
- **roadmap** merges — human only per policy.
- **P1 agent-kit wave** (li-net#12, li-httpd#13, li-std-core#8, li-std-math#9) — still `merge-approved` from prior pass; unchanged this sweep.
- Stagger org GraphQL sweeps to avoid blocking gate automation.
