# Issue feature planner — org-wide pass (2026-05-30T14:03Z)

**Run:** `issue_planner-1780149277711` · **Date:** 2026-05-30  
**Scope:** li-langverse org (6 repos) · **Workspace:** benchmarks  
**north_star_fit:** HPC/scientific computing · **PH-2i**, **PH-5b**, **PH-7e**, **G-lean**, **G-hw** · proof → easy → fast

## Error

**GitHub API rate limit exceeded** — live `gh issue list` failed for all 6 org repos:

```
GraphQL: API rate limit already exceeded for user ID 207167228.
```

Additionally, `GH_TOKEN` env token is invalid (inactive account `cap-jmk-real` in `~/.config/gh/hosts.yml` is valid but not active for this shell).

**Impact this run:**

- `scripts/issue-feature-triage.py` wrote `needs_plan=0`, `candidates=0` with `"error": "no issues or gh failed"` per repo.
- **No issue comments posted**, **no draft PRs opened**, **no label changes** (`plan-needed` removal blocked).
- Fallback: cached `issue_backlog_hygiene` from briefing (`2026-05-30T13:31Z`, `live_scan: true`) + local plan branches in sibling **lic** checkout.

## Executive summary

- **Scanned 6 repos** (lic, lip, lit, lis, benchmarks, roadmap) — live triage **blocked** by GitHub rate limit; cached hygiene shows **119** open issues, **50** routed to planner (mostly **lic** `master-plan-gap`).
- **Zero new plans drafted** this run — top **benchmarks** issues (#181, #179, #20) and top **lic** issues (#527, #526, #472, #425, #476) already have vision-aligned plan docs on local draft branches from earlier passes.
- **No code implementation** — none of the above issues carry `plan-approved`; vision filter holds.
- **Six tier-1 red** benchmark rows unchanged (**PH-5b**, **PH-7e**); lic#463/#424 are **bench_improver** scope, not new planner work (defer threshold weakening).
- **proof_gap_researcher handoff** refreshed: Horner `FmaFloatF64` ignores `--numerically-stable` (**G-hw**, **G-meta**); lic#472 P-linalg loop ≡ plan ready on branch `docs/plan-p-linalg-loop-ensures-472`.
- **Human-only:** add **`plan-approved`** on benchmarks #181/#179/#20 and lic #527/#526/#472 before implementation agents; retry planner after rate limit resets (~1h).
- **Maintainer:** activate valid `gh` token or wait for rate-limit reset; consider consolidating 14 duplicate lic issues per hygiene P0.

## Deliverable / findings

### 1. Issues scanned

| Repo | Live triage | Cached hygiene (`13:31Z`) | Notes |
|------|-------------|---------------------------|-------|
| **lic** | gh failed | **~28** `plan-needed` / **50** routed | Plan branches exist for top items |
| **benchmarks** | gh failed | **11** planning issues (prior pass) | #181, #179, #20 covered |
| **lip**, **lit** | gh failed | 0 routed | — |
| **lis**, **roadmap** | gh failed | empty in triage | — |

**Triage artifact:** `data/latest/issue-feature-triage.json` (`generated_at`: 2026-05-30T14:03Z, all repos errored)

### 2. Plans drafted (this run)

| Issue | Plan path (existing) | Draft PR / branch | Status |
|-------|---------------------|-------------------|--------|
| — | — | — | **No new plans** — rate limit blocked gh verify/post |

**Existing plans verified locally (no duplicates opened):**

| Issue | Plan path | Branch / PR |
|-------|-----------|-------------|
| [benchmarks#181](https://github.com/li-langverse/benchmarks/issues/181) | `docs/ecosystem/plans/2026-05-30-swarm-gap-actions-sync.md` | [PR #182](https://github.com/li-langverse/benchmarks/pull/182) / `docs/plan-swarm-gap-sync-181` |
| [benchmarks#179](https://github.com/li-langverse/benchmarks/issues/179) | `docs/ecosystem/plans/2026-05-30-catalog-path-reconciliation-ph5b.md` | [PR #183](https://github.com/li-langverse/benchmarks/pull/183) / `docs/plan-catalog-reconciliation-179` |
| [benchmarks#20](https://github.com/li-langverse/benchmarks/issues/20) | `docs/ecosystem/plans/2026-05-29-lic-root-agent-preflight.md` | [PR #135](https://github.com/li-langverse/benchmarks/pull/135) |
| [lic#527](https://github.com/li-langverse/lic/issues/527) | `docs/superpowers/plans/2026-05-30-for-range-ph2h-g-math-syn.md` | `docs/plan-for-range-ph2h-527` |
| [lic#526](https://github.com/li-langverse/lic/issues/526) | `docs/superpowers/plans/2026-05-30-numpy-broadcast-defer-ph2i.md` | `docs/plan-numpy-broadcast-defer-526` |
| [lic#472](https://github.com/li-langverse/lic/issues/472) | `docs/superpowers/plans/2026-05-30-p-linalg-loop-ensures-ph2i.md` | `docs/plan-p-linalg-loop-ensures-472` |
| [lic#425](https://github.com/li-langverse/lic/issues/425) | (Vision-LLM manifest gate) | `docs/plan-vision-llm-425` |
| [lic#476](https://github.com/li-langverse/lic/issues/476) | (PH-Pkg governance) | `docs/plan-ph-pkg-governance-476` |

### 3. Issues blocked / deferred

| Item | Reason |
|------|--------|
| All gh mutations | **API rate limit** — comments, PRs, labels deferred |
| **lic#463**, **lic#424** | Tier-1 red benches → **bench_improver** / harness in **lic**, not planner-only |
| **lic#473**, **lic#471**, **lic#436** | Block **benchmarks#181** implementation until ingest on main |
| Threshold weakening | **Rejected** — no `threshold_ratio_cpp` edits |
| **roadmap** / governance PRs | Do not self-merge |
| **lic#521–#523**, **#477–#478** | Sim/security/httpd supervisor idle — defer until runner loop (PH-Pkg #476) |

### 4. proof_gap_researcher handoff (`provability_holes`, priority 9)

Align with [proof_gap_researcher-2026-05-30-horner-fma-numerically-stable.md](./proof_gap_researcher-2026-05-30-horner-fma-numerically-stable.md) and briefing provability counts (**13** partial, **4** missing).

| Priority | Target | PH / G-* | Action |
|----------|--------|----------|--------|
| P0 | Horner `FmaFloatF64` / `HornerFmaUnroll` ignore `fp_numerically_stable` | **PH-7e**, **G-hw**, **G-meta** | Gate codegen like matmul (`emit.cpp:232-247` vs `764-800`); evidence: `horner_fma_numerically_stable_gap.sh` |
| P0 | Tier-1 `horner_pure_li` closed slice vs FMA trust hole | **PH-5b**, **G-math** | Do not claim G-math Done until policy + bench evidence align |
| P1 | [lic#472](https://github.com/li-langverse/lic/issues/472) P-linalg loop ≡ ensures | **PH-2i**, **G-lean** | Plan on `docs/plan-p-linalg-loop-ensures-472`; await `plan-approved` |
| P1 | [lic#461](https://github.com/li-langverse/lic/issues/461) Duplicate Proof-db appendix | **G-proof-db** | Docs-only; no `trusted.lean` |
| P2 | [lic#462](https://github.com/li-langverse/lic/issues/462) length-1 broadcast test gap | **PH-2i-b**, **G-math** | Link to [broadcast-len1 digest](./proof_gap_researcher-2026-05-30-broadcast-len1-codegen-lean.md) |

**north_star_fit for handoff:** Mathematical provability before tier-1 perf claims; no new trusted axioms for FMA drift.

## Recommended issues/PRs

### Maintainer (plan approval — blocked on gh this run)

| Title | Repo | Labels / action |
|-------|------|-----------------|
| docs(plan): swarm-gap-actions refresh (#181) | benchmarks | [PR #182](https://github.com/li-langverse/benchmarks/pull/182) — **`plan-approved`** |
| docs(plan): catalog path reconciliation PH-5b (#179) | benchmarks | [PR #183](https://github.com/li-langverse/benchmarks/pull/183) — **`plan-approved`** |
| docs(plan): LIC_ROOT agent preflight (#20) | benchmarks | [PR #135](https://github.com/li-langverse/benchmarks/pull/135) — review vs merged CI |
| PH-2h for/range Done gate (#527) | lic | `docs/plan-for-range-ph2h-527` — **`plan-approved`** |
| NumPy-rank broadcast defer (#526) | lic | `docs/plan-numpy-broadcast-defer-526` — **`plan-approved`** |
| P-linalg loop ≡ ensures (#472) | lic | `docs/plan-p-linalg-loop-ensures-472` — **`plan-approved`** |
| [G-hw/G-meta] Gate Horner FMA on `--numerically-stable` | lic | `provability`, **PH-7e** — after proof research cycle 27 |

### Implementation agents (after `plan-approved` only)

| Agent | Issue / PR | Reason |
|-------|------------|--------|
| **bench_improver** | lic tier-1 reds (`matmul_blocked`, `ml_*`, `num_gmres`) | **PH-5b**, **PH-7e** |
| **proof_gap_researcher** | Horner FMA + lic#472 float pilot | `provability_holes` goal |
| **plan_verifier** | Merge draft plan PRs after approval | Close plan_debt drift |
| **issue_hygiene** | 14 duplicate lic clusters | P0 hygiene from briefing |

## Deferred

- New planning until GitHub rate limit resets or valid token active for automation shell.
- Duplicate planning PRs for issues already covered (#25, #28, #29 → fold into #20 / #135).
- **lic#463** as planner item — route to **bench_improver** (perf harness, not exit-gate doc).
- Org-wide sim/security/httpd supervisor issues (#521–#523, #477–#478) — blocked on PH-Pkg runner loop.
- Self-merge of roadmap/governance docs; new Actions `schedule:` cron entries.
