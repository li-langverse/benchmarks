# PR reviewer digest — 2026-05-30T07:56Z

**Agent:** `pr_reviewer` · **Source:** proactive ecosystem sweep · **Run:** `pr_reviewer-1780127816950` · **North star:** proof → easy → fast

## Executive summary

- **GraphQL exhausted** (0/5000 remaining) — org gate scripts report **0 open PRs** (false negative); **REST API** used as source of truth this pass.
- **241 open org PRs** sampled; **13** carry `merge-approved`; **42** redundant `workspace sweep fallback` stacks (lic×19, benchmarks×18).
- **P0 merge queue (CI green + `merge-approved`):** [lip#32](https://github.com/li-langverse/lip/pull/32), [lit#18](https://github.com/li-langverse/lit/pull/18), [lic-docs#1](https://github.com/li-langverse/lic-docs/pull/1) — **sole blocker:** no human `APPROVED` review.
- **P1 agent-kit wave:** [li-net#12](https://github.com/li-langverse/li-net/pull/12), [li-httpd#13](https://github.com/li-langverse/li-httpd/pull/13), [li-std-core#8](https://github.com/li-langverse/li-std-core/pull/8), [li-std-math#9](https://github.com/li-langverse/li-std-math/pull/9) — CI green, `merge-approved`, blocked on human approve.
- **Numerics hot path:** [lic#499](https://github.com/li-langverse/lic/pull/499) PH-5b/7e — release notes present, **CI red** (`build-and-test`, macOS); do not merge.
- **Feature plan gate:** [lic#495](https://github.com/li-langverse/lic/pull/495) — CI green but **`plan-needed` without `plan-approved`** + merge conflicts.
- **Roadmap PRs** (#19–#21) have `merge-approved` + CI green — **human merge only** per governance policy; `pr_merger` must skip.
- **No new `merge-approved` labels** added this pass (aligned PRs already labeled; blockers on feature/numerics PRs).

## Deliverable / findings

### Error — degraded preflight

```
GraphQL: API rate limit already exceeded for user ID 207167228
```

| Resource | Remaining | Reset (unix) |
|----------|-----------|--------------|
| GraphQL | 0 / 5000 | 1780128522 |
| REST core | ~4097 / 5000 | 1780130167 |

| Script | Result | Notes |
|--------|--------|-------|
| `pr-merge-queue-plan.py` | `open_prs=0` | GraphQL `gh pr list` returns empty |
| `run-pr-program.py` | `open_prs=0 ci_green=0` | Same |
| `pr-merge-gate.py` | `pr_not_found` on all probes | Uses GraphQL `gh pr view` |

### CI-green + aligned (awaiting human approve)

| Repo | PR | CI | Label | Blocker |
|------|-----|-----|-------|---------|
| lip | [#32](https://github.com/li-langverse/lip/pull/32) LLVM 22 CI | 1/1 ✓ | merge-approved | No APPROVED review |
| lit | [#18](https://github.com/li-langverse/lit/pull/18) LLVM 22 CI | 1/1 ✓ | merge-approved | No APPROVED review |
| lic-docs | [#1](https://github.com/li-langverse/lic-docs/pull/1) org ci.yml | 1/1 ✓ | merge-approved | No APPROVED review |
| li-net | [#12](https://github.com/li-langverse/li-net/pull/12) agent-kit sync | 3/3 ✓ | merge-approved | No APPROVED review |
| li-httpd | [#13](https://github.com/li-langverse/li-httpd/pull/13) agent-kit sync | 3/3 ✓ | merge-approved | No APPROVED review |
| li-std-core | [#8](https://github.com/li-langverse/li-std-core/pull/8) agent-kit sync | 3/3 ✓ | merge-approved | No APPROVED review |
| li-std-math | [#9](https://github.com/li-langverse/li-std-math/pull/9) agent-kit sync | 3/3 ✓ | merge-approved | No APPROVED review |
| lic | [#437](https://github.com/li-langverse/lic/pull/437) tier-1 matmul perf | 7/7 ✓ | merge-approved | No APPROVED review; verify not superseded by #499 |
| benchmarks | [#132](https://github.com/li-langverse/benchmarks/pull/132) macOS tier profile | ✓ | merge-approved | No APPROVED review |

Reviewer comments posted in prior pass (`pr_reviewer-1780127006850`, 07:44Z); status unchanged — no duplicate comments this tick.

### Defer — blockers

| Repo | PR | Verdict | Blocker |
|------|-----|---------|---------|
| lic | [#499](https://github.com/li-langverse/lic/pull/499) matmul PH-5b/7e | defer | CI fail (5/7 pass) |
| lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | needs plan | `plan-needed`, dirty merge |
| lic | [#496](https://github.com/li-langverse/lic/pull/496) PH-CAD types | defer | CI fail, dirty merge |
| lic | [#488](https://github.com/li-langverse/lic/pull/488) provability mat2 VC | defer | 0 CI checks, dirty merge |
| lic | [#503](https://github.com/li-langverse/lic/pull/503) matmul improver | defer | 0 CI checks, dirty merge |
| benchmarks | [#201](https://github.com/li-langverse/benchmarks/pull/201) repo boundaries | defer | merge conflicts (dirty) |

### Checklist (reviewed subset)

| Gate | Status |
|------|--------|
| Vision / PH | LLVM pin = ecosystem CI (easy); #499/#437/#503 trace PH-5b/7e; #495/#496 trace AL-4 CAD |
| Strict by default | No `trusted.lean` creep in reviewed PRs |
| Security | N/A on CI/chore PRs reviewed |
| Performance | #499/#437 target red matmul rows — must not merge on red CI or without bench evidence |
| Release notes | #499 has `docs/release-notes/*`; #201 cross-cutting — missing release notes |
| Ecosystem-first | Gate scripts blocked; REST + manual checklist applied |

### Redundant / hygiene

- **42** open PRs titled `workspace sweep fallback` — superseded stack; close after newest sweep lands (`pr_branch_opener` / `pr_alignment`).
- **133** branches pushed without open PR (`pr-branch-hygiene.json`).
- **roadmap#19–#21** — governance repo; `merge-approved` present but **human merge only**.

### Control-plane

| Run | Status |
|-----|--------|
| `pr_reviewer-1780127816950` | running (this pass) |
| Prior `pr_reviewer` / `pr_merger` runs | error cascade — GraphQL exhaustion |

**north_star_fit:** domain=ecosystem/platform · PH=CI infra (P0), PH-5b/7e (#499, #437), AL-4 (#495)

## Recommended issues/PRs

| Priority | Repo | Item | Labels / action |
|----------|------|------|-----------------|
| P0 | lip | [#32](https://github.com/li-langverse/lip/pull/32) fix(ci): LLVM 22 | `merge-approved` → human **Approve** → `pr_merger` |
| P0 | lit | [#18](https://github.com/li-langverse/lit/pull/18) fix(ci): LLVM 22 | same |
| P1 | lic-docs | [#1](https://github.com/li-langverse/lic-docs/pull/1) org ci.yml | same |
| P1 | li-net / li-httpd / li-std-core / li-std-math | agent-kit sync #12–#13, #8–#9 | human **Approve** |
| P2 | lic | [#499](https://github.com/li-langverse/lic/pull/499) matmul tier-1 | fix CI, reconcile vs #437 stack |
| P2 | lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | add `plan-approved`, resolve conflicts |
| P2 | benchmarks | [#201](https://github.com/li-langverse/benchmarks/pull/201) repo boundaries | resolve conflicts + release notes |
| hygiene | lic/benchmarks | workspace sweep fallback ×42 | close redundant stack |
| governance | roadmap | [#19–#21](https://github.com/li-langverse/roadmap/pulls) | human review + merge only |

## Deferred

- Re-run `run-pr-program.py` + `pr-merge-gate.py` after GraphQL reset (~1780128522).
- **`pr_merger`** until non-author `APPROVED` on P0/P1 wave.
- **lic#499**, **lic#496**, **lic#488**, **lic#503** — not merge candidates until CI green + conflicts resolved.
- **roadmap** merges — human only per policy (even with `merge-approved`).
- Stagger org GraphQL sweeps (`bench_improver` + gate scripts) to avoid blocking automation.
- **lic#437 vs #499** — `pr_alignment` should confirm which matmul PR is canonical before merge.
