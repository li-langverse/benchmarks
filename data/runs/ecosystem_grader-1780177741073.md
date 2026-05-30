# Ecosystem grader digest — `ecosystem_grader-1780177741073`

**Date:** 2026-05-30T21:49Z  
**Agent:** `ecosystem_grader`  
**Source:** proactive  
**Scorecard:** `data/latest/ecosystem-quality-report.json` (refreshed 2026-05-30T21:48:56Z)  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-30T21:46Z)  
**North star fit:** ecosystem orchestration · PH-2i (linalg partial), PH-7e (tier-1 perf advisory), PH-DB (native persist partial), provability + swarm_coverage research goals

---

## Executive summary

- **Grade C** — overall score **77.0 / 100** (`ecosystem-quality-report.json`: `grade`, `overall_score`).
- **Unattended-safe: yes** — scorecard `unattended_safe: true`; meta lanes still degraded despite programmatic green on CI/bench posture.
- **Weakest lanes:** `gap_pressure` **60.0** and tied **70.0** on `goal_directed_health` + `swarm_execution` — gap/orchestration agents before implementers.
- **Strong lane:** `ecosystem_posture` **100.0** (0 red benchmarks, 0 repos missing CI on main, 0 failed PRs).
- **Goal-directed health:** 6/9 runners stopped; **34/110** plan todos pending; `agents_live: 0` — httpd/swarm-observer/ph-db supervisors up but idle between agent runs.
- **Swarm drift:** 23% error rate on 13 terminal runs (local sample); **107** runs still `running` in filesystem sample; CP last 24h: **12,496 error**, **23 running**, **132 incomplete**, **372 finished**.
- **Gap backlog:** **64** open registry rows (31 `plan_debt`, 30 `competitor_feature`, 3 `missing_package`) — apply pipeline not draining.
- **Briefing P0 aligned:** scorecard `recommended_agents` matches briefing heap — `swarm_observer`, `workspace_sweeper`, `plan_verifier`, `gap_explorer` ahead of `code_implementer`; no contradiction.

---

## Dimension drill-down

### briefing_health (77.0)

Briefing present with **11** recommended agents. Core fast preflights pass (`ecosystem_audit`, `workspace_dirty_sweep`). One failure: `org_agent_kit_audit` exit **1** — **21** org repos missing or drifted agent-kit (canonical 1.3.5+6018e18bf2ed91f4). Eight slow scripts remain skipped (`--skip-slow`: plan_audit, issue_hygiene, explorer, pr_program, ci_bug_triage, security_cwe_audit, agent_deliverable_gate, pr_branch_hygiene), suppressing live plan-completion depth and PR-program hygiene. Scorecard flags `preflight-failures` (medium) and `preflight-skipped` (medium). Agent-kit rollout is the actionable delta this cycle; slow-preflight refresh remains human env toggle.

### ecosystem_posture (100.0)

Ecosystem audit clean: `benchmark_red_count: 0`, `repos_missing_ci_main: 0`, `failed_prs: 0`, `open_prs: 0` in scorecard signals. Tier-1 bench rows are yellow not red (`matmul_blocked` yellow; `matmul_naive`, `simd_dot`, `fft_1d_fixed` near 1.0× in briefing). No coordinator lane degradation on CI or red-benchmark gates — perf work stays P2 behind swarm meta and provability research. Proof-before-perf order holds.

### goal_directed_health (70.0)

Snapshot at `lic/data/goal-directed-agents/snapshot.json`: **9** runners, **6** not running (`runners_stopped: 6`), **34** pending todos across **110** total. `httpd`, `swarm-observer`, and `ph-db` report `running: true` but supervisor idle (httpd log ~4961s stale; last iterations exit **124** on `gap-phase2-perf-wrk-soak` and `gap-phase2-streaming-wrk`). Completed loops (compiler-studio 47/47, sim 5/5) remain off. Starved lanes: studio-ui-ux (2 pending UX todos), sim-md-research (`md-r3-oracle-plan`), sim-chem-research (2 pending), security-research (3 pending), ph-db (9 merge/governance todos including cross-repo PH-DB wave). Re-enable supervisors after fixing httpd timeout gates — do not bypass proof-before-perf.

### swarm_execution (70.0)

Local sample: 120 runs, 13 terminal, **23% error rate** (3 errors: `docs_maintainer`, `gui_ui_tester`, `bench_improver` @ ~21:47Z), **0% incomplete** on terminal sample. **107** runs stuck `running` in filesystem sample. Control-plane last 24h: **12,496** `error`, **132** `incomplete`, **23** `running`, **372** `finished`. Recent mass preemption @ 21:42Z (10+ agents simultaneous `error`, `briefing_hash: null`). Terminal errors are SDK backend failures after substantive work (not repo conflicts) — e.g. `docs_maintainer-1780177405649` completed doc edits but SDK returned error; `gui_ui_tester-1780177405633` produced audit artifacts then SDK error. Delegate terminalization TTL and error vs incomplete reconciliation to `swarm_observer` on `li-cursor-agents`.

### gap_pressure (60.0)

Registry apply pipeline holds **64** open gaps (`swarm-gap-actions.json`): **31** `plan_debt` (master-plan phases 2i, 7d, 7e, 8p, Vision-LLM without runner mapping), **30** `competitor_feature`, **3** `missing_package` (`std.summary`, `std.plot`, `li-line-profiler`). Swarm-observer orchestrator plan complete (5/5) but apply pipeline not draining. `gap_explorer` + `swarm_observer` apply pass should run before `implementation_gaps` / `code_implementer` on new std modules.

---

## Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|----------------------|
| `goal-runners-stopped` | high | `lic/data/goal-directed-agents/snapshot.json` | `swarm_observer` + httpd plan loop human restart |
| `swarm-error-rate` | high | `li-cursor-agents/data/runs/` (23% on 13 terminal runs) | `swarm_observer` |
| `swarm-gap-backlog` | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| `preflight-failures` | medium | `agent-briefing.preflight_runs.org_agent_kit_audit` (exit 1, 21 repos) | `agent_kit_maintainer` |
| `preflight-skipped` | medium | `agent-briefing.preflight_runs` (8 × `--skip-slow`) | briefing maintainer / supervisor env |
| `swarm-many-running` | medium | `li-cursor-agents/data/runs/` (107 running) | `swarm_observer` |
| `plan-debt-gaps` | medium | `swarm-gap-actions.by_kind.plan_debt` (31 rows) | `plan_verifier`, `gap_explorer` |

---

## Recommended dispatch order

Aligns with `ecosystem-quality-report.json` → `recommended_agents`, merged with briefing P0 and heap coordinators (no contradiction):

| Order | Agent | Reason | Coordinator lane |
|------:|-------|--------|------------------|
| 1 | `swarm_observer` | `swarm_execution` 70 (below 75); briefing P0 research goal `swarm_coverage` (priority 10); 107 stuck `running`; 12.5k CP errors/24h | meta / control-plane |
| 2 | `workspace_sweeper` | Briefing P0 + scorecard: 2 dirty siblings (`lic`, `benchmarks`) | hygiene |
| 3 | `plan_verifier` | Briefing P0 + heap P30: 65 master-plan open items; plan audit skipped | `coord_governance` |
| 4 | `gap_explorer` | `gap_pressure` 60 (below 80); 2 missing std modules; 64 registry rows | `coord_ecosystem` |
| 5 | `agent_kit_maintainer` | `org_agent_kit_audit` exit 1 — 21 repos missing/drifted kit | ecosystem hygiene |
| 6 | `pr_alignment` | Heap P10: 16 PRs flagged close/supersede | `coord_pull_requests` |
| 7 | `implementation_gaps` | Heap P30: plan vs code drift (after plan_verifier) | `coord_governance` |
| 8 | `issue_hygiene` | dup_clusters=4, explorer_spam_repos=2 | `coord_governance` |
| 9 | `bug_fixer` → `code_implementer` | 2 CI/bug queue items — after meta lanes stable | implementer |
| 10 | `security_auditor` | CWE Top25 missing_in_catalog=19 | security |
| — | `bench_improver` / `ci_maintainer` | **Deferred** — ecosystem_posture 100; yellow matmul only | perf / CI |

**Handoff signals (north_star_fit):**

| Signal | Delegate to |
|--------|-------------|
| 23% terminal error rate + 107 stuck `running` + 12.5k CP errors/24h | `swarm_observer` |
| 64 open gaps / 31 plan_debt | `gap_explorer` + `swarm_observer` apply pipeline |
| 6 stopped goal runners / httpd exit 124 | httpd plan loop + `plan_verifier` |
| 21 repos missing agent-kit | `agent_kit_maintainer` |
| PH-DB cross-repo merge wave (wp-g through wp-prod) | human governance + ph-db plan loop |

---

## Human-only blockers

- **Governance / trusted.lean** — never auto-merge; human-approved issues only.
- **httpd wrk soak timeouts** — exit 124 on tier5 perf gates needs human tuning (`HTTPD_BENCH_SKIP_TIMING`, fixture soak duration) before plan loop restart.
- **PH-DB merge wave** — four feat/ph-db-* branches across lidb/lis/benchmarks/li-cursor-agents require human merge-queue review; branches currently on digest/chore branches not expected feat branches.
- **Branch protection rollout** — org rulesets for package mirrors (`roadmap/scripts/apply-org-branch-protection.sh`).
- **Dirty workspaces** — `lic` (4 files on `chore/workspace-sweep-1780171200`) and `benchmarks` (6 files on digest branch); human decides commit vs revert before sweeper lands.
- **Slow preflight enablement** — drop `--skip-slow` requires supervisor env change (not agent-implementable in benchmarks alone).
- **LI_CURSOR_AGENTS_ENABLED=1** — agent deliverable gate disabled; obscures incomplete-run scan.
- **Agent-kit canonical pin** — 21-repo rollout may need org-wide PR review before bulk merge.
- **Native SDL capture regression** — `gui_ui_tester` reports `SDL_RenderReadPixels` 0 frames (li-cursor-agents #47); blocks honest native UX gates.

---

## Agent deliverable checklist

- [x] Cited `ecosystem-quality-report.json` (77.0, grade C @ 21:48Z) — no manual re-score
- [x] Read `agent-briefing.json` + `goal-directed-agents/snapshot.json`
- [x] Queried control-plane DB (`agent_runs` status aggregates, recent errors, 24h window)
- [x] Sampled failing runs (`docs_maintainer-1780177405649`, `gui_ui_tester-1780177405633`, `bench_improver-1780177395064`)
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
| Governance (`coord_governance`) | 77 briefing | degraded visibility | plan_audit skipped; 65 open plan items |
| Ecosystem (`coord_ecosystem`) | 60 gap | **degraded** | 64 open swarm gaps |
| Swarm meta | 70 execution | **degraded** | stuck `running`, mass CP errors, SDK terminal errors |
| Goal-directed | 70 | **starved** | 6/9 supervisors off or idle |
| Agent-kit | — | **failure** | 21 repos missing kit |

### Execution drift sample

| Run | Status | Pattern |
|-----|--------|---------|
| `docs_maintainer-1780177405649` | error | SDK error after 240s / 45 tools — doc edits completed, no deliverable section |
| `gui_ui_tester-1780177405633` | error | SDK error after 249s — audit artifacts written, native SDL regression (#47) |
| `bench_improver-1780177395064` | error | SDK error — tier-1 bench work interrupted |
| `swarm_observer-1780177378947` | error | @ 21:42Z mass tick — `briefing_hash: null` |
| `plan_verifier-1780172416618` | incomplete | prior cycle — plan audit depth missing |

CP last 24h confirms systemic error volume (12,496 rows) dominated by historical/preemption noise; local terminal sample shows **actionable** 23% error on recent UX/docs/bench agents. Grader confirms **swarm_observer first**, then hygiene/governance, then implementers.

### Score delta vs prior pass (`ecosystem_grader-1780171057813`)

| Metric | Prior (19:53Z) | Current (21:48Z) | Trend |
|--------|---------------:|-----------------:|-------|
| Overall | 77.0 | **77.0** | ↔ |
| Unattended-safe | yes | **yes** | ↔ |
| swarm_execution | 70.0 | **70.0** | ↔ (error rate 0%→23% on terminal sample) |
| goal_directed_health | 70.0 | **70.0** | ↔ (34 pending vs 25 prior — snapshot refresh) |
| briefing_health | 77.0 | **77.0** | ↔ |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Terminalize stuck `running` agent runs after SDK TTL | li-cursor-agents | `ecosystem-meta`, `swarm_observer` |
| Reconcile CP `error` vs `incomplete`/`finished` persistence | li-cursor-agents | `ecosystem-meta` |
| Fix SDK terminal error on completed agent work (deliverable section gate) | li-cursor-agents | `ecosystem-meta`, `cursor-sdk` |
| Roll out agent-kit 1.3.5 to 21 missing/drifted org repos | li-cursor-agents / org | `agent-kit`, `agent_kit_maintainer` |
| Restart httpd plan loop — fix tier5 wrk soak exit 124 | lic | `httpd`, `tier5`, `perf` |
| Map master-plan plan_debt gaps to goal-directed runner backlogs | lic | `swarm-gap`, `plan-debt` |
| Close/supersede 16 flagged PRs (pr_alignment backlog) | org | `pr-hygiene` |
| PH-DB cross-repo merge wave (wp-g through wp-n5) | lidb, lis, benchmarks, li-cursor-agents | `ph-db`, `governance` |
| Fix native SDL capture regression (`SDL_RenderReadPixels` 0 frames) | li-cursor-agents | `ux`, `gui_ui_tester` |

No new implementer PRs recommended until meta lanes (`swarm_observer`, `gap_explorer`) complete.

---

## Deferred

- **bench_improver / numerics_researcher** — tier-1 yellow matmul only; ecosystem_posture 100; proof-before-perf order holds.
- **ci_maintainer add-workflow** — 0 repos missing CI; red PR fixes → `bug_fixer`.
- **Full `--skip-slow` preflight drop** — next scheduled full briefing or human supervisor toggle.
- **Goal runner restarts** (compiler-studio, sim, research loops) — plans complete or idle; restart only when new todos land.
- **Control-plane PR** — file from `swarm_observer` after observer pass, not this grader run.
- **proof_gap_researcher** — parallel research lane (provability_holes); not blocking meta sweep.
- **studio-ui-ux palette/gpu todos** — blocked on gap orchestrator mapping; defer to studio plan loop restart.

---

## References

- Scorecard: `benchmarks/data/latest/ecosystem-quality-report.json`
- Briefing: `benchmarks/data/latest/agent-briefing.json`
- Goal snapshot: `lic/data/goal-directed-agents/snapshot.json`
- Gap registry: `benchmarks/data/latest/swarm-gap-actions.json`
- Prior pass: `benchmarks/data/runs/ecosystem_grader-1780171057813.md`
- Vision: [vision-and-roadmap.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md)
- Master plan: [2026-05-14-li-master-plan.md](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md)
