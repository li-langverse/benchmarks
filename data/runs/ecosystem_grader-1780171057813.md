# Ecosystem grader digest — `ecosystem_grader-1780171057813`

**Date:** 2026-05-30T19:57Z  
**Agent:** `ecosystem_grader`  
**Source:** proactive  
**Scorecard:** `data/latest/ecosystem-quality-report.json` (refreshed 2026-05-30T19:53:48Z)  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-30T19:50Z)  
**North star fit:** ecosystem orchestration · PH-2i (linalg partial), PH-7e (tier-1 perf advisory), provability_holes + swarm_coverage research goals

---

## Executive summary

- **Grade C** — overall score **77.0 / 100** (`ecosystem-quality-report.json`: `grade`, `overall_score`).
- **Unattended-safe: yes** — scorecard `unattended_safe: true`; meta lanes still degraded despite programmatic green.
- **Weakest lanes:** `gap_pressure` **60.0** and `goal_directed_health` **70.0** — gap/orchestration agents before implementers.
- **Strong lanes:** `ecosystem_posture` **100.0** (0 red benchmarks, 0 repos missing CI on main); `briefing_health` **77.0** (core preflights mostly green).
- **Goal-directed health:** 6/8 runners stopped; **25/97** plan todos pending; `agents_live: 0` — httpd + swarm-observer supervisors idle with stale logs.
- **Swarm drift:** 50% incomplete rate on 8 terminal runs sampled locally; **112** runs still `running` in filesystem sample; CP last 2h: **1822 error**, **24 running**, **10 incomplete**, **14 finished**.
- **Gap backlog:** **64** open registry rows (31 `plan_debt`, 30 `competitor_feature`, 3 `missing_package`) — apply pipeline not draining.
- **New preflight failure:** `org_agent_kit_audit` exit **1** — 21 org repos missing or drifted agent-kit (canonical 1.3.5+6018e18bf2ed91f4); dispatch `agent_kit_maintainer` after meta sweep.
- **Briefing P0 aligned:** `swarm_observer`, `workspace_sweeper`, `plan_verifier` ahead of `code_implementer`; no contradiction with scorecard `recommended_agents`.

---

## Dimension drill-down

### briefing_health (77.0)

Briefing present with **11** recommended agents. Core fast preflights pass (`issue_triage`, `ecosystem_audit`, `org_ci_audit`, `merge_plan`, `cwe_feed_sync`, `workspace_dirty_sweep`). One new failure: `org_agent_kit_audit` exit **1** (21 repos needing kit sync — li-gui, lidb, render, sim, proof-library, etc.). Eight slow scripts remain skipped (`--skip-slow`: plan_audit, issue_hygiene, explorer, pr_program, ci_bug_triage, security_cwe_audit, agent_deliverable_gate, pr_branch_hygiene), suppressing live plan-completion and PR-program depth. Scorecard flags `preflight-failures` (medium) and `preflight-skipped` (medium). Agent-kit rollout is the actionable delta this cycle; slow-preflight refresh remains human env toggle.

### ecosystem_posture (100.0)

Ecosystem audit and org CI gate both pass: `benchmark_red_count: 0`, `repos_missing_ci_main: 0`, `failed_prs: 0`. Scorecard signals show `open_prs: 1` (briefing merge_plan still reports 0 open — hygiene flags 16 PRs for close/supersede review via `pr_alignment`, not live open merge queue). Tier-1 bench rows are yellow not red (`matmul_blocked` yellow; `matmul_naive`, `simd_dot`, `fft_1d_fixed` near 1.0× in briefing). No coordinator lane degradation on CI or red-benchmark gates — perf work stays P2 behind swarm meta and provability research.

### goal_directed_health (70.0)

Snapshot at `lic/data/goal-directed-agents/snapshot.json`: **8** runners, **6** not running (`runners_stopped: 6`), **25** pending todos. `httpd` and `swarm-observer` report `running: true` but supervisor idle (logs 46k–48k s stale); last httpd iterations exited **124** on `gap-phase2-perf-wrk-soak` and `gap-phase2-streaming-wrk` (wrk soak timeout). Completed loops (compiler-studio 47/47, sim 5/5) remain off. Starved lanes: studio-ui-ux (2 pending UX todos: palette-search-latency, gpu-fail-recovery), sim-md-research (md-r3-oracle-plan), sim-chem-research (2 pending), security-research (3 pending). Re-enable supervisors after fixing httpd timeout gates — do not bypass proof-before-perf.

### swarm_execution (70.0)

Local sample: 120 runs, 8 terminal, **50% incomplete**, **0% error** on terminal sample (errors concentrated in non-terminal / historical CP rows). **112** runs stuck `running` in filesystem sample. Control-plane last 2h: **1822** `error`, **10** `incomplete`, **24** `running`, **14** `finished` — mass preemption wave @ 19:46–19:47Z (15+ agents simultaneous `run_started`-only errors). Observer @ 19:54Z (`swarm_observer-1780170744552`): programmatic `healthy: true`, retried `swarm_observer`, dispatched `implementation_gaps`; `gap_explorer`, `issue_hygiene`, `security_auditor` still under-dispatched vs briefing heap. Delegate terminalization TTL and error vs incomplete reconciliation to `swarm_observer` on `li-cursor-agents`.

### gap_pressure (60.0)

Registry apply pipeline holds **64** open gaps (`swarm-gap-actions.json`): **31** `plan_debt` (master-plan phases without runner mapping — 2i, 7d, 7e, Vision-LLM, etc.), **30** `competitor_feature`, **3** `missing_package` (`std.summary`, `std.plot`, `li-line-profiler` patched pending in backlog). Swarm-observer orchestrator plan complete (5/5) but apply pipeline not draining. `gap_explorer` + `swarm_observer` apply pass should run before `implementation_gaps` / `code_implementer` on new std modules.

---

## Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|----------------------|
| `goal-runners-stopped` | high | `lic/data/goal-directed-agents/snapshot.json` | `swarm_observer` + httpd plan loop human restart |
| `swarm-gap-backlog` | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| `swarm-incomplete-rate` | medium | `li-cursor-agents/data/runs/` (50% incomplete on terminal sample) | `swarm_observer` |
| `swarm-many-running` | medium | `li-cursor-agents/data/runs/` (112 running) | `swarm_observer` |
| `preflight-failures` | medium | `agent-briefing.preflight_runs.org_agent_kit_audit` (exit 1, 21 repos) | `agent_kit_maintainer` |
| `preflight-skipped` | medium | `agent-briefing.preflight_runs` (8 × `--skip-slow`) | briefing maintainer / supervisor env |
| `plan-debt-gaps` | medium | `swarm-gap-actions.by_kind.plan_debt` (31 rows) | `plan_verifier`, `gap_explorer` |

---

## Recommended dispatch order

Aligns with `ecosystem-quality-report.json` → `recommended_agents`, merged with briefing P0 and heap coordinators (no contradiction):

| Order | Agent | Reason | Coordinator lane |
|------:|-------|--------|------------------|
| 1 | `swarm_observer` | `swarm_execution` 70 (below 75); briefing P0 research goal `swarm_coverage` (priority 10); 112 stuck `running` | meta / control-plane |
| 2 | `workspace_sweeper` | Briefing P0 + scorecard: 2 dirty siblings (`lic`, `benchmarks`) | hygiene |
| 3 | `plan_verifier` | Briefing P0 + heap P30: 166 master-plan open items; plan audit skipped | `coord_governance` |
| 4 | `gap_explorer` | `gap_pressure` 60 (below 80); 2 missing std modules; 64 registry rows | `coord_ecosystem` |
| 5 | `agent_kit_maintainer` | **New:** `org_agent_kit_audit` exit 1 — 21 repos missing/drifted kit | ecosystem hygiene |
| 6 | `pr_alignment` | Heap P10: 16 PRs flagged close/supersede | `coord_pull_requests` |
| 7 | `implementation_gaps` | Heap P30: plan vs code drift (after plan_verifier) | `coord_governance` |
| 8 | `issue_hygiene` | dup_clusters=4, explorer_spam_repos=2 | `coord_governance` |
| 9 | `bug_fixer` → `code_implementer` | 1 CI/bug queue item — after meta lanes stable | implementer |
| 10 | `security_auditor` | CWE Top25 missing_in_catalog=19 | security |
| — | `bench_improver` / `ci_maintainer` | **Deferred** — ecosystem_posture 100; yellow matmul only | perf / CI |

**Handoff signals (north_star_fit):**

| Signal | Delegate to |
|--------|-------------|
| 50% incomplete + 112 stuck `running` + 1822 CP errors/2h | `swarm_observer` |
| 64 open gaps / 31 plan_debt | `gap_explorer` + `swarm_observer` apply pipeline |
| 6 stopped goal runners / httpd exit 124 | httpd plan loop + `plan_verifier` |
| 21 repos missing agent-kit | `agent_kit_maintainer` |
| provability_holes + swarm_coverage eligible | `proof_gap_researcher` (parallel research lane) |

---

## Human-only blockers

- **Governance / trusted.lean** — never auto-merge; human-approved issues only.
- **httpd wrk soak timeouts** — exit 124 on tier5 perf gates needs human tuning (`HTTPD_BENCH_SKIP_TIMING`, fixture soak duration) before plan loop restart.
- **Branch protection rollout** — org rulesets for package mirrors (`roadmap/scripts/apply-org-branch-protection.sh`).
- **Dirty workspaces** — `lic` (5 files on `cursor/swarm-observer-plan-loop`) and `benchmarks` (2 files on digest branch); human decides commit vs revert before sweeper lands.
- **Slow preflight enablement** — drop `--skip-slow` requires supervisor env change (not agent-implementable in benchmarks alone).
- **LI_CURSOR_AGENTS_ENABLED=1** — agent deliverable gate disabled; obscures incomplete-run scan.
- **Agent-kit canonical pin** — 21-repo rollout may need org-wide PR review before bulk merge.

---

## Agent deliverable checklist

- [x] Cited `ecosystem-quality-report.json` (77.0, grade C @ 19:53Z) — no manual re-score
- [x] Read `agent-briefing.json` + `goal-directed-agents/snapshot.json`
- [x] Queried control-plane DB (`agent_runs` status aggregates, recent 15 runs, 2h window)
- [x] Cross-referenced `swarm_observer-1780170744552.md` observer pass (19:54Z)
- [x] Dispatch order aligned with scorecard `recommended_agents` + briefing P0
- [ ] Control-plane prompt edits — **deferred** to `swarm_observer` PR on `li-cursor-agents` (terminalization TTL)
- [ ] Full slow preflight briefing — **deferred** (human env)
- [ ] Agent-kit org rollout — **delegated** to `agent_kit_maintainer`

---

## Deliverable / findings (agent-specific)

### Coordinator lane status

| Lane | Score | Status | Primary blocker |
|------|------:|--------|-----------------|
| PR (`coord_pull_requests`) | — | idle (0 open in merge_plan) | 16 PRs flagged for hygiene review |
| Governance (`coord_governance`) | 77 briefing | degraded visibility | plan_audit skipped; 166 open plan items |
| Ecosystem (`coord_ecosystem`) | 60 gap | **degraded** | 64 open swarm gaps |
| Swarm meta | 70 execution | **degraded** | stuck `running`, mass CP errors |
| Goal-directed | 70 | **starved** | 6/8 supervisors off or idle |
| Agent-kit | — | **new failure** | 21 repos missing kit |

### Execution drift sample

| Run | Status | Pattern |
|-----|--------|---------|
| `autoresearch-1780170457809` | incomplete | `run_started` only — wave preemption @ 19:47Z |
| `docs_maintainer-1780170457780` | incomplete | proactive digest incomplete at kickoff |
| `ci_maintainer-1780170449021` | incomplete | same preemption wave |
| `gui_ui_tester-1780170449025` | error | simultaneous tick kill @ 19:47Z |
| `bench_improver-1780170439327` | error | SDK preemption, not repo conflict |

CP observer @ 19:52–19:57Z: dual `swarm_observer` runs active; `agent_kit_maintainer` finishing (3× finished in last 15 runs). Grader confirms **swarm_observer first**, then hygiene/governance, then implementers.

### Score delta vs prior pass (`ecosystem_grader-1780152735271`)

| Metric | Prior (14:56Z) | Current (19:53Z) | Trend |
|--------|---------------:|-----------------:|-------|
| Overall | 75.8 | **77.0** | ↑ |
| Unattended-safe | no | **yes** | ↑ |
| swarm_execution | 60.0 | **70.0** | ↑ (error rate 9%→0% on terminal sample) |
| briefing_health | 85.0 | **77.0** | ↓ (org_agent_kit_audit failure) |
| Incomplete rate (local terminal) | 45% | **50%** | ↔ degraded |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Terminalize stuck `running` agent runs after SDK TTL | li-cursor-agents | `ecosystem-meta`, `swarm_observer` |
| Reconcile CP `error` vs `incomplete`/`finished` persistence | li-cursor-agents | `ecosystem-meta` |
| Roll out agent-kit 1.3.5 to 21 missing/drifted org repos | li-cursor-agents / org | `agent-kit`, `agent_kit_maintainer` |
| Restart httpd plan loop — fix tier5 wrk soak exit 124 | lic | `httpd`, `tier5`, `perf` |
| Map master-plan plan_debt gaps to goal-directed runner backlogs | lic | `swarm-gap`, `plan-debt` |
| Close/supersede 16 flagged PRs (pr_alignment backlog) | org | `pr-hygiene` |
| Apply org branch protection rulesets | roadmap / org settings | `ecosystem-governance` |

No new implementer PRs recommended until meta lanes (`swarm_observer`, `gap_explorer`) complete.

---

## Deferred

- **bench_improver / numerics_researcher** — tier-1 yellow matmul only; ecosystem_posture 100; proof-before-perf order holds.
- **ci_maintainer add-workflow** — 0 repos missing CI; red PR fixes → `bug_fixer`.
- **Full `--skip-slow` preflight drop** — next scheduled full briefing or human supervisor toggle.
- **Goal runner restarts** (compiler-studio, sim, research loops) — plans complete or idle; restart only when new todos land.
- **Control-plane PR** — file from `swarm_observer` after observer pass, not this grader run.
- **proof_gap_researcher** — parallel research lane (provability_holes); not blocking meta sweep.

---

## References

- Scorecard: `benchmarks/data/latest/ecosystem-quality-report.json`
- Briefing: `benchmarks/data/latest/agent-briefing.json`
- Goal snapshot: `lic/data/goal-directed-agents/snapshot.json`
- Gap registry: `benchmarks/data/latest/swarm-gap-actions.json`
- Observer peer: `benchmarks/data/runs/swarm_observer-1780170744552.md`
- Vision: [vision-and-roadmap.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md)
- Master plan: [2026-05-14-li-master-plan.md](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md)
