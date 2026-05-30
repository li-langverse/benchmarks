# Ecosystem grader digest — `ecosystem_grader-1780152735271`

**Date:** 2026-05-30T14:56Z  
**Agent:** `ecosystem_grader`  
**Source:** proactive  
**Scorecard:** `data/latest/ecosystem-quality-report.json` (refreshed 2026-05-30T14:56:21Z)  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-30T14:02Z)  
**North star fit:** ecosystem orchestration · PH-2i (linalg), PH-7e (tier-1 perf), provability_holes research goal

---

## Executive summary

- **Grade C** — overall score **75.8 / 100** (`ecosystem-quality-report.json`: `grade`, `overall_score`).
- **Unattended-safe: no** — `unattended_safe: false`; goal loops starved and swarm execution degraded.
- **Weakest lanes:** `swarm_execution` **60.0** and `gap_pressure` **60.0** — dispatch meta agents before implementers.
- **Strong lanes:** `ecosystem_posture` **100.0** (0 red benchmarks, 0 repos missing CI on main); `briefing_health` **85.0**.
- **Goal-directed health:** 6/8 runners stopped; **25/97** plan todos pending; `agents_live: 0` (`goal_directed_health.signals`).
- **Swarm drift:** 45% incomplete rate on 11 terminal runs sampled; **109** runs still `running`; CP last 2h: **826 error**, **23 running** (`swarm_execution.signals`, Supabase `agent_runs`).
- **Gap backlog:** **64** open registry rows (31 `plan_debt`, 30 `competitor_feature`, 3 `missing_package`) — blocks unattended closure.
- **Briefing P0 intact:** `proof_gap_researcher`, `workspace_sweeper`, `plan_verifier` remain ahead of `code_implementer` / `bench_improver`.

---

## Dimension drill-down

### briefing_health (85.0)

Preflight core path is green: `preflight_failed: 0`, briefing present, **10** recommended agents. Eight slow preflights remain skipped (`--skip-slow`: plan_audit, issue_hygiene, explorer, pr_program, ci_bug_triage, security_cwe_audit, agent_deliverable_gate, pr_branch_hygiene), which suppresses live plan-completion and PR-program signals. The scorecard flags only `preflight-skipped` (medium). Refreshing slow preflights on the next full briefing cycle would lift governance confidence without contradicting current P0 ordering.

### ecosystem_posture (100.0)

Ecosystem audit and org CI gate both pass: `benchmark_red_count: 0`, `repos_missing_ci_main: 0`, `open_prs: 0`, `failed_prs: 0` in scorecard signals (briefing snapshot). Tier-1 bench rows are yellow not red (`matmul_blocked`, `matmul_naive` near 1.2× in briefing `ecosystem_audit.benchmarks.yellow`). No coordinator lane degradation on CI or red-benchmark gates this cycle — perf work stays P2 behind swarm meta and provability research.

### goal_directed_health (70.0)

Snapshot at `lic/data/goal-directed-agents/snapshot.json` shows **8** runners, **6** not running (`runners_stopped: 6`), **25** pending todos across active backlogs. `httpd` and `swarm-observer` report `running: true` but supervisor idle (logs 28k–30k s stale); last httpd iterations exited **124** on `gap-phase2-perf-wrk-soak` and `gap-phase2-streaming-wrk`. Completed loops (compiler-studio 47/47, sim 5/5) remain off. Starved lanes: studio-ui-ux (2 pending UX todos), sim-md-research, sim-chem-research, security-research. Re-enable supervisors after fixing httpd timeout gates — do not bypass proof-before-perf.

### swarm_execution (60.0)

Local sample: 120 runs, 11 terminal, **45% incomplete**, **9% error** (1× `autoresearch` SDK error). **109** runs stuck `running` in filesystem sample. Control-plane last 2h: **826** `error`, **67** `incomplete`, **23** `running`, **1** `finished` — mass preemption / status-reconciliation drift, not repo merge conflicts. Observer @ 14:55Z: `retry_counts: {}`, `swarm_health.healthy: true` despite `goal_mismatch` finding (proof_gap_researcher, workspace_sweeper, plan_verifier under-dispatched). Delegate to `swarm_observer` for terminalization TTL and error vs incomplete reconciliation in `li-cursor-agents`.

### gap_pressure (60.0)

Registry apply pipeline holds **64** open gaps (`swarm-gap-actions.json`): **31** `plan_debt` (mostly master-plan phases without runner mapping), **30** `competitor_feature`, **3** `missing_package` (`std.summary`, `std.plot`, `li-line-profiler` patched pending in backlog). Swarm-observer orchestrator plan complete (5/5) but apply pipeline not draining. `gap_explorer` + `swarm_observer` apply pass should run before `implementation_gaps` / `code_implementer` on new std modules.

---

## Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|----------------------|
| `goal-runners-stopped` | high | `lic/data/goal-directed-agents/snapshot.json` | `swarm_observer` + httpd plan loop human restart |
| `swarm-gap-backlog` | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| `swarm-incomplete-rate` | medium | `li-cursor-agents/data/runs/` (45% incomplete) | `swarm_observer` |
| `swarm-many-running` | medium | `li-cursor-agents/data/runs/` (109 running) | `swarm_observer` |
| `preflight-skipped` | medium | `agent-briefing.preflight_runs` | briefing maintainer / supervisor env |
| `plan-debt-gaps` | medium | `swarm-gap-actions.by_kind.plan_debt` | `plan_verifier`, `gap_explorer` |

---

## Recommended dispatch order

Aligns with `ecosystem-quality-report.json` → `recommended_agents`, merged with briefing P0 and heap coordinators (no contradiction):

| Order | Agent | Reason | Coordinator lane |
|------:|-------|--------|------------------|
| 1 | `swarm_observer` | `swarm_execution` 60 (below 75) — terminalize stuck runs, refresh CP swarm_health | meta / control-plane |
| 2 | `proof_gap_researcher` | Briefing P0: provability_holes research goal (priority 9) | research |
| 3 | `workspace_sweeper` | Briefing P0: 1 dirty sibling (`lic` on `cursor/swarm-observer-plan-loop`, 5 files) | hygiene |
| 4 | `plan_verifier` | Briefing P0 + heap P30: 166 master-plan open items, plan audit skipped | `coord_governance` |
| 5 | `gap_explorer` | `gap_pressure` 60 (below 80); 2 missing std modules; 64 registry rows | `coord_ecosystem` |
| 6 | `pr_alignment` | Heap P10: 14 PRs flagged close/supersede | `coord_pull_requests` |
| 7 | `implementation_gaps` | Heap P30: plan vs code drift (after plan_verifier) | `coord_governance` |
| 8 | `issue_hygiene` | dup_clusters=4, explorer_spam_repos=2 | `coord_governance` |
| 9 | `bug_fixer` → `code_implementer` | 1 CI/bug queue item — after meta lanes stable | implementer |
| 10 | `security_auditor` | CWE Top25 missing_in_catalog=19 | security |
| — | `bench_improver` / `ci_maintainer` | **Deferred** — ecosystem_posture 100; yellow matmul only | perf / CI |

**Handoff signals (north_star_fit):**

| Signal | Delegate to |
|--------|-------------|
| 45% incomplete + 109 stuck `running` | `swarm_observer` |
| 64 open gaps / 31 plan_debt | `gap_explorer` + `swarm_observer` apply pipeline |
| 6 stopped goal runners / httpd exit 124 | httpd plan loop + `plan_verifier` |
| provability_holes eligible | `proof_gap_researcher` |

---

## Human-only blockers

- **Governance / trusted.lean** — never auto-merge; human-approved issues only.
- **httpd wrk soak timeouts** — exit 124 on tier5 perf gates needs human tuning (`HTTPD_BENCH_SKIP_TIMING`, fixture soak duration) before plan loop restart.
- **Branch protection rollout** — org rulesets for package mirrors (`roadmap/scripts/apply-org-branch-protection.sh`).
- **lic dirty workspace** — 5 changed files on `cursor/swarm-observer-plan-loop`; human decides commit vs revert before sweeper lands.
- **Slow preflight enablement** — drop `--skip-slow` requires supervisor env change (not agent-implementable in benchmarks alone).
- **LI_CURSOR_AGENTS_ENABLED=1** — agent deliverable gate disabled; obscures incomplete-run scan.

---

## Agent deliverable checklist

- [x] Regenerated `ecosystem-quality-report.json` (75.8, grade C @ 14:56Z)
- [x] Cited all dimension scores and findings from scorecard (no manual re-score)
- [x] Read `agent-briefing.json` + `goal-directed-agents/snapshot.json`
- [x] Queried control-plane DB (`agent_runs` status aggregates, `control_plane_state`)
- [x] Sampled execution drift (`autoresearch-1780151421916.json` SDK error; incomplete plan_verifier rows)
- [x] Dispatch order aligned with `recommended_agents` + briefing P0
- [ ] Control-plane prompt edits — **deferred** to `swarm_observer` PR on `li-cursor-agents` (terminalization TTL)
- [ ] Full slow preflight briefing — **deferred** (human env)

---

## Deliverable / findings (agent-specific)

### Coordinator lane status

| Lane | Score | Status | Primary blocker |
|------|------:|--------|-----------------|
| PR (`coord_pull_requests`) | — | idle (0 open in briefing merge_plan) | pr_alignment backlog from hygiene flags |
| Governance (`coord_governance`) | 85 briefing | degraded visibility | plan_audit skipped |
| Ecosystem (`coord_ecosystem`) | 60 gap | **degraded** | 64 open swarm gaps |
| Swarm meta | 60 execution | **degraded** | stuck `running`, mass CP errors |
| Goal-directed | 70 | **starved** | 6/8 supervisors off or idle |

### Execution drift sample

| Run | Status | Pattern |
|-----|--------|---------|
| `autoresearch-1780151421916` | error | SDK `run-178f2223…` after 561s; premature — no numerics evidence |
| `plan_verifier-1780152735234` | incomplete | `run_started` only — wave preemption |
| `ci_maintainer-1780152649781` | incomplete | proactive digest incomplete at kickoff |

CP observer remediations queued @ 14:55Z: retry `proof_gap_researcher`, dispatch `implementation_gaps` — grader confirms **swarm_observer first**, then P0 research/hygiene, then governance implementers.

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Terminalize stuck `running` agent runs after SDK TTL | li-cursor-agents | `ecosystem-meta`, `swarm_observer` |
| Reconcile CP `error` vs `incomplete`/`finished` persistence | li-cursor-agents | `ecosystem-meta` |
| Restart httpd plan loop — fix tier5 wrk soak exit 124 | lic | `httpd`, `tier5`, `perf` |
| Close duplicate Studio UI/UX tracker issues (#181–#182 → keep #178) | lic | `issue-hygiene` |
| Map master-plan plan_debt gaps to goal-directed runner backlogs | lic | `swarm-gap`, `plan-debt` |
| Apply org branch protection rulesets | roadmap / org settings | `ecosystem-governance` |

No new implementer PRs recommended until meta lanes (`swarm_observer`, `gap_explorer`) complete.

---

## Deferred

- **bench_improver / numerics_researcher** — tier-1 yellow matmul only; ecosystem_posture 100; proof-before-perf order holds.
- **ci_maintainer add-workflow** — 0 repos missing CI; red PR fixes → `bug_fixer`.
- **Full `--skip-slow` preflight drop** — next scheduled full briefing or human supervisor toggle.
- **Goal runner restarts** (compiler-studio, sim, research loops) — plans complete or idle; restart only when new todos land.
- **Control-plane PR** — file from `swarm_observer` after observer pass, not this grader run.

---

## References

- Scorecard: `benchmarks/data/latest/ecosystem-quality-report.json`
- Briefing: `benchmarks/data/latest/agent-briefing.json`
- Goal snapshot: `lic/data/goal-directed-agents/snapshot.json`
- Gap registry: `benchmarks/data/latest/swarm-gap-actions.json`
- Vision: [vision-and-roadmap.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md)
- Master plan: [2026-05-14-li-master-plan.md](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md)
