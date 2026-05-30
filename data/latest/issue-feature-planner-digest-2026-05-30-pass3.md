# Issue feature planner digest — 2026-05-30 (pass 3)

**Run:** issue-feature-planner · org-wide (lic focus)  
**Triage:** `issue-feature-triage.py` @ 2026-05-30T12:03Z — **`gh` GraphQL rate-limited**; rescanned via GitHub REST API  
**north_star_fit:** platform throughput (**PH-8p-c**), ecosystem governance (**PH-Pkg**), proof honesty handoff → **proof_gap_researcher**  
**Research handoff:** `provability_holes` priority 9

---

## Executive summary

- **Error:** `gh issue list` failed (GraphQL rate limit exceeded); triage JSON reported **0** needs_plan — **undercount**. REST API rescan: **benchmarks 10**, **lic 10+** `plan-needed` (paginated cap).
- **Benchmarks queue:** all 11 issues already have `li-agent-plan-v2` comments; **no new plans** (duplicate avoidance).
- **This pass drafted 2 lic plans:** [#525](https://github.com/li-langverse/lic/issues/525) → [PR #536](https://github.com/li-langverse/lic/pull/536); [#476](https://github.com/li-langverse/lic/issues/476) → [PR #537](https://github.com/li-langverse/lic/pull/537).
- **#461 resolved:** merged [lic#519](https://github.com/li-langverse/lic/pull/519); posted status comment — await maintainer **`plan-approved`** / close.
- **No implementation** — zero issues carry **`plan-approved`** in scanned set.
- **proof_gap_researcher:** prioritize lic **#472**, **#387**, **#527**, **#526** (plans posted; await labels).
- **Ecosystem benches:** 137 green, 6 red tier-1 ML/num rows; **no** threshold weakening proposed.
- **Human-only:** review open plan PRs (benchmarks #135–137, #182–183; lic **#536**, **#537**); restore `gh` quota before next triage run.

---

## Deliverable / findings

### Issues scanned

| Repo | plan-needed (REST) | needs_plan (this pass) | notes |
|------|-------------------:|-----------------------:|-------|
| **benchmarks** | 10 | 0 | all planned |
| **lic** | 10+ | 2 drafted (#525, #476) | #527/#526/#387 have v2 |
| **lis** | 1 | 0 | #20 PH-DB — defer lic-scoped pass |
| lip, lit, roadmap | 0 | 0 | — |

### Plans drafted (this run)

| Issue | Plan path | Draft PR |
|-------|-----------|----------|
| lic **#525** | `lic/docs/superpowers/plans/2026-05-30-lic-build-jobs-ph8p-c.md` | [lic#536](https://github.com/li-langverse/lic/pull/536) |
| lic **#476** | `lic/docs/superpowers/plans/2026-05-30-ph-pkg-governance-exit-gates.md` | [lic#537](https://github.com/li-langverse/lic/pull/537) |
| lic **#461** | *N/A — fixed by merged #519* | status comment only |

### Issues blocked

| Item | Reason |
|------|--------|
| **`gh` GraphQL rate limit** | Triage script under-reported; use REST fallback or wait for quota reset |
| All `needs_plan` without **`plan-approved`** | Implementation agents blocked |
| Open plan PRs (benchmarks + lic) | Draft docs need maintainer review |
| lic **#463/#424** tier-1 reds | **bench_improver** / harness — not catalog-only |
| lis **#20** PH-DB hosting | Cross-repo; human org checklist if new infra |

### proof_gap_researcher handoff (provability_holes)

| Priority | Issue | PH / G-* | Action |
|----------|-------|----------|--------|
| P0 | lic **#472** P-linalg loop ≡ `ensures` | PH-2i, **G-lean**, **G-math** | Lean corpus; split open obligations |
| P0 | lic **#387** MIR proc tags + disjoint | PH-7d, **G-par**, **G-dec** | Verify v2 plan + `plan-approved` |
| P1 | lic **#527** for/range gate | PH-2h, **G-math-syn** | v2 posted — await label |
| P1 | lic **#526** NumPy broadcast defer | PH-2i, **G-math** | v2 posted — await label |
| Defer | **G-ann**, **G-gpu**, **G-meta**, **G-authz** missing | — | No PH track |

---

## Recommended issues/PRs

### Awaiting `plan-approved` (maintainer)

| PR | Repo | Issues |
|----|------|--------|
| [#536](https://github.com/li-langverse/lic/pull/536) | lic | #525 PH-8p-c |
| [#537](https://github.com/li-langverse/lic/pull/537) | lic | #476 PH-Pkg |
| [#183](https://github.com/li-langverse/benchmarks/pull/183) | benchmarks | #179 catalog gaps |
| [#182](https://github.com/li-langverse/benchmarks/pull/182) | benchmarks | #181 swarm-gap |
| [#135](https://github.com/li-langverse/benchmarks/pull/135) | benchmarks | #20, #25, #28, #29, #54 |
| [#136](https://github.com/li-langverse/benchmarks/pull/136) | benchmarks | #18 FFT |
| [#137](https://github.com/li-langverse/benchmarks/pull/137) | benchmarks | #53 PH-IO-7 |

### After approval — agent routing

| Issue | Agent |
|-------|-------|
| #525 `--jobs` wiring | code_implementer (lic) |
| #476 governance gates | docs_maintainer + plan_verifier |
| #179 (117 catalog gaps) | code_implementer (benchmarks + lic harness) |
| #472 P-linalg Lean | **proof_gap_researcher** |

---

## Deferred

- **Benchmarks new plans** — queue complete until maintainer approves open PRs.
- **lis #20** PH-DB control-plane hosting — governance checklist; separate pass.
- **lic studio-ui #394–399** — lic-scoped planner (max 3 cap next run).
- **`threshold_ratio_cpp` weakening** — rejected.
- **Self-merge** roadmap/governance PRs — not attempted.
- **Actions `schedule:` cron** — not added.

---

## Error

```
GraphQL: API rate limit already exceeded for user ID 207167228.
```

**Impact:** `scripts/issue-feature-triage.py` returned `needs_plan=0` for all 6 repos. Rescanned with unauthenticated/authenticated REST API for this digest. **Remediation:** wait for GitHub API quota reset or add REST fallback to triage script.

<!-- li-agent-issue-feature-planner-digest-v2 -->
