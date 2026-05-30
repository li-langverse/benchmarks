# Ecosystem grader digest — `ecosystem_grader-1780144535416`

**Date:** 2026-05-30T12:35Z  
**Agent:** ecosystem_grader (proactive sweep)  
**Scorecard:** `data/latest/ecosystem-quality-report.json` (2026-05-30T12:20:21Z)  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-30T12:07Z)  
**north_star_fit:** provable → easy → fast — PH-5b / PH-7e tier-1 numerics; PH-2f provability_holes research; no gate weakening

---

## Executive summary

- **Grade C** · **overall score 70.8 / 100** · **unattended-safe: no** (`ecosystem-quality-report.json`: `grade`, `overall_score`, `unattended_safe`).
- **Stable vs 07:37Z pass** (70.8 / C): `gap_pressure` slipped to **60** (64 open gaps); `ecosystem_posture` improved to **75** (1 repo without live docs vs 10); briefing preflights regressed (**8 skipped**, plan_audit off).
- **Meta lanes degraded:** `swarm_execution` **70** (36% incomplete rate on 22 terminal runs in local sample; **98** runs still `running`), `gap_pressure` **60** (64 open gaps: 31 plan_debt, 30 competitor_feature, 3 missing_package).
- **Briefing P0:** `proof_gap_researcher` (provability_holes priority 9) → `workspace_sweeper` (2 dirty sibling repos) — scorecard agrees; do not skip for numerics-only heap work.
- **Scorecard meta-first dispatch:** `swarm_observer` → `gap_explorer` → `plan_verifier` before implementers; aligns with `swarm-incomplete-rate` + `swarm-gap-backlog` findings.
- **Goal-directed loops starved:** 6/8 runners stopped, **25** plan todos pending of 97, `agents_live: 0`; httpd last todos exited **124** (wrk soak timeout).
- **6 red benchmark rows** unchanged (`matmul_blocked`, `matmul_naive`, ML forwards, `num_gmres`) — `coord_numerics` P20 after meta reconciliation.
- **12:30Z orchestrator wave:** 10+ agents `error` in parallel (null `briefing_hash`) — SDK slot contention, not auth; delegate `swarm_observer`.

---

## Dimension drill-down

### briefing_health (77.0)

Briefing is present with **12 recommended agents** and core fast preflights green (`ecosystem_audit`, `org_ci_audit`, `workspace_dirty_sweep` exit 0). Weakness: **8 scripts skipped** (`--skip-slow`: plan_audit, explorer, pr_program, pr_branch_hygiene, ci_bug_triage, security_cwe_audit, issue_hygiene) plus **1 failure** — `org_agent_kit_audit` exit 1 (`li-language: missing_kit` vs canonical `1.3.5+6018e18bf2ed91f4`). `agent_deliverable_gate` skipped (`LI_CURSOR_AGENTS_ENABLED` unset). Findings `preflight-skipped` (medium), `preflight-failures` (medium). Run full preflight before unattended cycles; dispatch **plan_verifier** (plan audit skipped) and **agent_kit_maintainer**.

### ecosystem_posture (75.0)

Org CI posture is clean: **0** repos missing CI on main, **0** open/failed PRs in ecosystem audit, **11** repos with live pages. Dimension held below 80 by **six red benchmark rows** (ingest @ 2026-05-29T18:47Z, ratios 1.33–1.55× vs cpp) and **1 repo without live docs**. Finding `benchmark-red-rows` (high). Route **bench_improver** + **numerics_researcher** under `coord_numerics` (heap P20) after `swarm_observer` clears execution drift; lic PR #499 (matmul MIR) blocked on CI — human review before ingest refresh.

### goal_directed_health (70.0)

Snapshot present (`lic/data/goal-directed-agents/snapshot.json`, 2026-05-30T12:35Z): **8 runners**, **6 not running** (supervisor off or idle with stale logs), **25 pending todos** of 97, **`agents_live: 0`**. **httpd**, **studio-ui-ux**, **swarm-observer** show `running: true` (fixture/gh-compare processes) but `agent_live: false`; httpd todos `gap-phase2-perf-wrk-soak` / `gap-phase2-streaming-wrk` exited **124**. **studio-ui-ux** active todo `studio-ux-16-palette-search-latency` (2 wave-2 pending). Research loops (**sim-md**, **sim-chem**, **security-research**) idle since 2026-05-25. Finding `goal-runners-stopped` (high). Restart plan loops or hand pending todos to **plan_verifier** / vertical owners.

### swarm_execution (70.0)

Local sample (n=120): **98 running**, **22 terminal**, **1 error**, **8 incomplete** → `error_rate` **0.0455**, `incomplete_rate` **0.3636**. Findings `swarm-incomplete-rate` (medium), `swarm-many-running` (medium). Control-plane DB (full history): **10,082 error**, 475 finished, 42 incomplete, 23 running — historical error volume dominates; **12:30Z batch** shows 10+ concurrent `error` runs (`proof_gap_researcher`, `workspace_sweeper`, `plan_verifier`, `ecosystem_grader`, …) with `briefing_hash: null` — orchestrator preemption. Top error agent in sample: `code_implementer` (1). Delegate **swarm_observer** for terminalization, stale-run sweeper, and parallel-pool slot policy on **li-cursor-agents**.

### gap_pressure (60.0)

`swarm-gap-actions.json` (2026-05-30T12:20Z): **64 open gaps** — `plan_debt: 31`, `competitor_feature: 30`, `missing_package: 3` (`std.plot`, `std.summary`, line-profiler seed). Finding `swarm-gap-backlog` (high), `plan-debt-gaps` (medium). Briefing lists **2 missing std modules** for **gap_explorer**; registry is broader. **gap_explorer** + **swarm_observer** apply pipeline before **code_implementer** / **implementation_gaps** flood implementers.

---

## Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|------------------------|
| benchmark-red-rows | high | `data/latest/ecosystem-audit.json` → `benchmarks.red` | `bench_improver`, `numerics_researcher` |
| goal-runners-stopped | high | `lic/data/goal-directed-agents/snapshot.json` | plan loop owners / `plan_verifier` |
| swarm-gap-backlog | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| preflight-failures | medium | `data/latest/agent-briefing.json` → `preflight_runs.org_agent_kit_audit` | `agent_kit_maintainer` |
| preflight-skipped | medium | `data/latest/agent-briefing.json` → `preflight_runs` (--skip-slow) | orchestrator / full preflight run |
| swarm-incomplete-rate | medium | `li-cursor-agents/data/runs` | `swarm_observer` |
| swarm-many-running | medium | `li-cursor-agents/data/runs` | `swarm_observer` |
| plan-debt-gaps | medium | `data/latest/swarm-gap-actions.json` → `by_kind.plan_debt` | `gap_explorer`, `plan_verifier` |

---

## Recommended dispatch order

Merged **scorecard** `recommended_agents` with **briefing** `recommended_agents` (briefing P0 wins on ties):

1. **proof_gap_researcher** — briefing P0: research goal `provability_holes` eligible (priority 9); retry after 12:30Z wave error.
2. **workspace_sweeper** — briefing P0: lic dirty on `cursor/swarm-observer-plan-loop` (6 safe files: snapshot, registry, nginx submodule, logs); benchmarks dirty on digest branch.
3. **swarm_observer** — scorecard: `swarm_execution` < 75; 36% incomplete rate + 98 “running” stubs; 12:30Z parallel pool errors.
4. **gap_explorer** — scorecard: `gap_pressure` < 80; 64 registry gaps vs briefing’s 2 std modules.
5. **plan_verifier** — scorecard + briefing: plan-completion-audit (166 findings); plan_audit skipped this cycle.
6. **implementation_gaps** — briefing: cross-check plan vs implementation (after verifier).
7. **agent_kit_maintainer** — preflight exit 1: `li-language` missing_kit.
8. **bench_improver** / **numerics_researcher** — heap `coord_numerics` P20 + 6 red rows (after meta + workspace).
9. **code_implementer** — briefing: implement missing std modules from explorer (after gap_explorer).
10. **docs_maintainer**, **pr_branch_opener**, **security_auditor** — 1 repo without live pages; 147 orphan branches; Top25 catalog gaps (19).

**Do not contradict briefing P0:** numerics remain important but follow provability research + workspace + meta reconciliation first.

---

## Human-only blockers

| Blocker | Detail |
|---------|--------|
| Agent deliverable gate off | `LI_CURSOR_AGENTS_ENABLED` unset — no agent PR completion scan |
| lic PR #499 | Matmul MIR fast paths — CI red on build-and-test; merge blocked until green |
| Agent-kit sync | `li-language` missing kit `1.3.5+6018e18bf2ed91f4` |
| Goal loop timeouts | httpd `gap-phase2-perf-wrk-soak` / `gap-phase2-streaming-wrk` exit 124 — longer budget or human gate |
| Full preflight skipped | plan_audit, explorer, pr_program, security_cwe_audit off (`--skip-slow`) |
| No open merge queue | 0 open PRs — merge automation idle; 147 pushed branches without PRs |
| 12:30Z wave failures | 10+ agents errored simultaneously — orchestrator slot limit; not missing API keys |

No missing `CURSOR_API_KEY` surfaced in this cycle.

---

## Agent deliverable checklist

<!-- li-agent -->
## Agent deliverable

- [x] Read `ecosystem-quality-report.json` (scorecard fresh @ 12:20Z; no manual re-score)
- [x] Dimension narratives + findings table + dispatch order
- [x] Control-plane SQL spot-check (`agent_runs` status histogram + recent errors)
- [x] Goal-directed snapshot reviewed (`lic/data/goal-directed-agents/snapshot.json`)
- [x] Sample error runs cited (12:30Z wave, `ecosystem_grader-1780144197422.json`)
- [x] Digest written to `data/runs/ecosystem_grader-1780144535416.md`
- [ ] **swarm_observer** PR on `li-cursor-agents` (stale-run sweeper / parallel pool limits)
- [ ] **gap_explorer** reconcile 64 open gaps in `swarm-gap-actions.json`
- [ ] Full preflight (drop `--skip-slow`) before next unattended cycle
- [ ] Enable `LI_CURSOR_AGENTS_ENABLED=1` for deliverable gate
<!-- /li-agent -->

---

## Deliverable / findings (agent-specific)

### Handoff matrix

| Signal | Delegate to |
|--------|-------------|
| 36% incomplete rate + 98 running stubs | `swarm_observer` |
| 64 open gaps (31 plan_debt, 30 competitor_feature) | `gap_explorer` + `swarm_observer` apply pipeline |
| 6 red benchmarks | `bench_improver`, `numerics_researcher` |
| 6 stopped goal runners + 25 pending todos | Plan loops / `plan_verifier` |
| lic + benchmarks dirty workspaces | `workspace_sweeper` |
| provability_holes research eligible | `proof_gap_researcher` |

### Control-plane evidence

```text
agent_runs status histogram (full DB):
  error: 10082 | finished: 475 | incomplete: 42 | running: 23
Recent errors @ 2026-05-30T12:30Z: proof_gap_researcher, workspace_sweeper, plan_verifier,
  ecosystem_grader, code_implementer, ci_maintainer, pr_merger, … (briefing_hash null)
Scorecard local sample (n=120 JSON): error_rate=0.0455, incomplete_rate=0.3636, running_count=98
```

### Goal-directed runners (stopped / idle)

| id | branch | plan_pending | note |
|----|--------|--------------|------|
| httpd | cursor/httpd-plan-continue | 2 | agent_exit 124 on wrk soak; log 21314s stale |
| studio-ui-ux | cursor/studio-ui-ux-plan-loop | 2 | active: `studio-ux-16-palette-search-latency` |
| swarm-observer | cursor/swarm-observer-plan-loop | 0 | orch plan complete; supervisor idle |
| compiler-studio | cursor/compiler-studio-plan-loop | 0 | supervisor off; plan complete |
| sim | cursor/sim-algo-plan-loop | 0 | supervisor off |
| sim-md-research | cursor/sim-md-research-loop | 1 | `md-r3-oracle-plan` |
| sim-chem-research | cursor/sim-chem-research-loop | 2 | DFT handoff todos |
| security-research | cursor/security-research-loop | 3 | fuzz/exploit todos |

### Execution drift samples

- `ecosystem_grader-1780144197422.json` — started 12:30:23Z, status `error`, `briefing_hash: null` (parallel wave)
- `proof_gap_researcher-1780144231263.json` — same wave; briefing P0 blocked
- `workspace_sweeper-1780144178060.json` — same wave; dirty lic/benchmarks sweep not completed

### Coordinator lane health

| Coordinator | Priority | Agents | Lane status |
|-------------|----------|--------|-------------|
| coord_numerics | 20 | numerics_researcher, bench_improver | **degraded** — 6 red rows; blocked on lic codegen |
| coord_governance | 30 | plan_verifier, implementation_gaps | **weak** — plan_audit skipped; 166 open plan items |
| coord_ecosystem | 40 | gap_explorer, docs_maintainer | **degraded** — 64 gap backlog; 1 repo no live docs |
| coord_platform | 50 | agent_kit_maintainer | **weak** — li-language missing kit |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| **observer: stale SDK run sweeper** — mark `running` > 2h incomplete; parallel pool slot cap | `li-cursor-agents` | `control-plane`, `agent:swarm_observer` |
| **gap-apply: reconcile 64 open registry rows** — plan_debt runner mapping | `lic` | `orchestration`, `agent:gap_explorer` |
| **bench: tier-1 green matmul_naive + num_gmres** — review PR #499 | `lic` | `PH-7e`, `agent:bench_improver` |
| **org: agent-kit sync li-language** | `li-language` | `agent:agent_kit_maintainer` |
| **feat(httpd): gap-phase2 perf wrk soak** — extend timeout or split todos | `lic` | `li-swarm`, `agent:code_implementer` |
| **preflight: drop --skip-slow for plan_audit + security_cwe_audit** | `benchmarks` | `orchestration`, `agent:ecosystem_grader` |
| **docs: live pages for 1 repo without GitHub Pages** | org-wide | `agent:docs_maintainer` |
| **branch hygiene: 147 pushed branches without open PR** | org-wide | `agent:pr_branch_opener` |

---

## Deferred

- **Merge automation** — 0 open PRs; merge queue idle until PRs land.
- **ML tier-1 reds** (`ml_conv2d_forward`, `ml_mlp_forward`, `ml_mlp_train_step`) — li-math stub scope; defer until lic tier-1 codegen green.
- **Yellow thermostats** (`md_thermostat_berendsen`, `md_thermostat_nose_hoover`) — tier-2 MD micro-opt after tier-1 crisis.
- **147 orphan branches** — `pr_branch_opener` backlog; not blocking meta lane.
- **Research loop todos** (sim-md, sim-chem, security-research) — idle since 2026-05-25; restart when goal-directed supervisor budget available.
- **Full security_cwe_audit** — skipped this cycle; defer to next full preflight.
- **Control-plane prompt edits** — any SDK/orchestrator fixes → PR on `li-cursor-agents` with `npm test` (not in this digest-only pass).

---

**Evidence paths:** `benchmarks/data/latest/ecosystem-quality-report.json`, `benchmarks/data/latest/agent-briefing.json`, `benchmarks/data/latest/swarm-gap-actions.json`, `lic/data/goal-directed-agents/snapshot.json`, `li-cursor-agents/data/runs/`
