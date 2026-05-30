# Ecosystem grader digest — `ecosystem_grader-1780146986899`

**Date:** 2026-05-30T13:20Z  
**Agent:** `ecosystem_grader`  
**Source:** proactive ecosystem sweep  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-30T12:07Z)  
**Scorecard:** `data/latest/ecosystem-quality-report.json` (70.8, grade **C**)  
**North star fit:** ecosystem orchestration — proof → easy → fast (Phase 2i partial, PH-5b/7e numerics debt)

---

## Executive summary

- **Grade C (70.8/100)** — improved from prior D (69.0) but still below unattended threshold; `unattended_safe: false`.
- **Unattended operation: not safe** — goal-directed loops starved (6/8 runners stopped, 25 plan todos pending), 64 open swarm gaps, and 89% incomplete rate in sampled agent runs.
- **Weakest dimension: `gap_pressure` (60.0)** — 64 registry rows (31 plan_debt, 30 competitor_feature, 3 missing_package); `gap_explorer` + `swarm_observer` apply pipeline required before implementers.
- **Swarm execution drift (70.0)** — 111/120 sampled runs still `running`, 8 `incomplete`; CP DB shows mass concurrent `running` at 13:16–13:19Z with `briefing_hash: null` (SDK terminalization gap, not repo errors).
- **Ecosystem posture (75.0)** — 6 red benchmark rows (matmul_*, ml_*, num_gmres); 137 green, 0 open/failed PRs, CI on main complete across org.
- **Briefing health (77.0)** — 1 preflight failure (`org_agent_kit_audit` exit 1: `li-language` missing agent-kit); 8 slow preflights skipped.
- **Goal-directed health (70.0)** — `httpd` and `swarm-observer` supervisors idle/stale; research runners (md/chem/security) and `studio-ui-ux` stopped with pending todos.
- **P0 briefing preserved** — `proof_gap_researcher` (provability_holes) and `workspace_sweeper` (2 dirty sibling repos) remain in dispatch queue alongside scorecard meta-agents.

---

## Dimension drill-down

### briefing_health (77.0 / weight 0.15)

Briefing snapshot is present with 12 recommended agents and a valid heap plan (`coord_numerics` P20 → `bench_improver`/`numerics_researcher`; governance P30 → `plan_verifier`/`implementation_gaps`). Preflight coverage is partial: `ecosystem_audit` and `workspace_dirty_sweep` passed, but `org_agent_kit_audit` exited 1 because `li-language` lacks the canonical agent-kit stamp and required `.cursor/rules/*` files. Eight slow preflights were skipped (`--skip-slow`), leaving plan audit, explorer, PR program, and security CWE signals stale. Refresh via full preflight (drop `--skip-slow`) and `plan_verifier` before trusting governance lane scores.

### ecosystem_posture (75.0 / weight 0.25)

Org-wide audit is healthy on merge/CI axes: 0 open PRs, 0 failed PRs, 0 repos missing CI on main, 11/12 repos with live pages. Performance debt dominates: six red benchmark rows at 1.33–1.55× vs C++ (`matmul_blocked`, `matmul_naive`, `ml_conv2d_forward`, `ml_mlp_forward`, `ml_mlp_train_step`, `num_gmres`), all tagged PH-5b/7e. Two yellow MD thermostats and five near-threshold rows (num_cholesky, cloth_swing, robo_*) warrant watch-list only. Master plan shows 166 open items; current PH focus is Phase 2i linalg partial. Numerics lane (`numerics_researcher`, `bench_improver`) should run after meta-orchestration stabilizes swarm dispatch.

### goal_directed_health (70.0 / weight 0.20)

Snapshot present with 8 runners, 0 agents live. Six runners report `running: false` or supervisor idle: `compiler-studio` (plan complete, supervisor off 409k s), `sim` (complete), `studio-ui-ux` (2 pending: palette latency, GPU fail recovery), `sim-md-research` (1 pending: oracle plan), `sim-chem-research` (2 pending), `security-research` (3 pending). `httpd` shows supervisor idle with log 24k s stale — last todos `gap-phase2-perf-wrk-soak` and `gap-phase2-streaming-wrk` failed with agent exit 124 (timeout). `swarm-observer` orchestrator plan complete but supervisor idle 22k s. Aggregate: 25/97 plan todos pending across runners; goal-directed loops are starved and need human or supervisor restart after fixing httpd timeout root cause.

### swarm_execution (70.0 / weight 0.25)

Local sample of 120 runs under `li-cursor-agents/data/runs/`: 111 `running`, 8 `incomplete`, 1 `finished`, 0 `error` — incomplete rate 88.9%. CP DB lifetime status skews heavily `error` (400–709 per agent) from historical mislabeling; current tick (13:16–13:19Z) shows ~15 agents concurrently `running` with null `briefing_hash`, indicating wave dispatch without terminal reconciliation. Latest `control_plane_reports.swarm_health.healthy: true` is stale (2026-05-25). Delegate to `swarm_observer` for control-plane prompt fixes: terminalize stuck runs after SDK TTL, attach briefing_hash on run start, refresh dashboard swarm_health.

### gap_pressure (60.0 / weight 0.15)

`swarm-gap-actions.json` reports 64 open gaps: 31 plan_debt (master-plan partial phases), 30 competitor_feature (verticals/intel stubs), 3 missing_package (`line_profiler`, `std.summary`, `std.plot` patched to backlog pending). Plan-completion audit adds 117 catalog gaps and 166 total findings. Gap registry apply pipeline ran 2026-05-30T09:28Z but most plan_debt rows deferred (“no runner backlog mapping”). `gap_explorer` should reconcile explorer catalog (2 missing std modules in briefing) with registry; `swarm_observer` should map plan_debt rows to active goal-directed backlogs (`studio-ui-ux`, research loops).

---

## Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|----------------------|
| benchmark-red-rows | high | `agent-briefing.json` → `ecosystem_audit.benchmarks.red` | `numerics_researcher`, `bench_improver` |
| goal-runners-stopped | high | `lic/data/goal-directed-agents/snapshot.json` | human supervisor + relevant plan loops |
| swarm-gap-backlog | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| preflight-failures | medium | `agent-briefing.preflight_runs.org_agent_kit_audit` | `agent_kit_maintainer` |
| preflight-skipped | medium | `agent-briefing.preflight_runs` (8× `--skip-slow`) | briefing maintainer / full preflight run |
| swarm-incomplete-rate | medium | `li-cursor-agents/data/runs/` (89% incomplete) | `swarm_observer` |
| swarm-many-running | medium | `li-cursor-agents/data/runs/` (111 running) | `swarm_observer` |
| plan-debt-gaps | medium | `swarm-gap-actions.by_kind.plan_debt` (31 rows) | `plan_verifier`, `implementation_gaps` |

---

## Recommended dispatch order

Align scorecard `recommended_agents` with briefing P0 and heap priority; do not skip P0 items.

| Order | Agent | Reason | Lane |
|-------|-------|--------|------|
| 1 | `swarm_observer` | `swarm_execution` 70.0 &lt; 75 — terminalize runs, refresh CP swarm_health | meta / control-plane |
| 2 | `gap_explorer` | `gap_pressure` 60.0 &lt; 80 — reconcile 64 open gaps + 2 missing std modules | coord_ecosystem P40 |
| 3 | `plan_verifier` | briefing_health weak + plan-completion-audit (166 findings) | coord_governance P30 |
| 4 | `proof_gap_researcher` | **Briefing P0:** provability_holes research goal (priority 9) | research |
| 5 | `workspace_sweeper` | **Briefing P0:** lic + benchmarks dirty sibling repos | hygiene |
| 6 | `implementation_gaps` | cross-check plan vs implementation (heap P30) | coord_governance |
| 7 | `agent_kit_maintainer` | `li-language` missing kit (preflight exit 1) | coord_platform P50 |
| 8 | `bench_improver` → `numerics_researcher` | 6 red rows (heap P20) — **after** meta lanes stabilize | coord_numerics |
| 9 | `code_implementer` | missing std modules from explorer | post-explorer |
| 10 | `docs_maintainer`, `pr_branch_opener`, `security_auditor` | backlog hygiene (147 branch-only pushes; 1 repo without live docs) | lower priority |

**Defer implementers** (`code_implementer`, `bench_improver`) until `swarm_observer` clears stuck `running` wave and `gap_explorer` updates registry — otherwise implementer runs compete with unreconciled heap state.

---

## Human-only blockers

| Blocker | Detail | Action |
|---------|--------|--------|
| Goal-directed supervisor restart | `httpd` exit 124 on wrk soak todos; 6/8 runners stopped | Human: inspect `lic/data/httpd-plan-loop/until-deadline-*.log`, fix timeout, restart supervisor |
| `li-language` agent-kit | Preflight exit 1; missing rules + no `install-agent-kit.sh` run | `cd li-language && ../roadmap/scripts/install-agent-kit.sh li-language` then PR |
| Skipped preflights | plan_audit, explorer, pr_program, security_cwe, ci_bug_triage skipped | Run full briefing preflight without `--skip-slow` on maintainer host |
| `LI_CURSOR_AGENTS_ENABLED` | `agent_deliverable_gate` skipped | Set env var to enable deliverable scan |
| Stale CP dashboard report | `control_plane_reports.swarm_health.healthy: true` @ 2026-05-25 | `swarm_observer` PR on `li-cursor-agents` (no human merge) |
| 147 branches without PR | `pr_branch_opener` backlog | Human triage for abandoned vs intentional draft branches |
| Merge queue | 0 open PRs — no merge-queue conflict today | — |

No missing API key signal in this sweep; CURSOR/GH tokens assumed present (agents dispatching).

---

## Agent deliverable checklist

- [x] Regenerated `data/latest/ecosystem-quality-report.json` (70.8, C)
- [x] Read `data/latest/agent-briefing.json` + `lic/data/goal-directed-agents/snapshot.json`
- [x] CP DB queried (`agent_runs` status aggregates, stuck `running` sample, stale `control_plane_reports`)
- [x] Sampled `li-cursor-agents/data/runs/` (120 files — 111 running, 8 incomplete)
- [x] Dimension drill-down + findings table from scorecard fields (no manual re-score)
- [x] Dispatch order aligned with scorecard + briefing P0
- [ ] Control-plane prompt PR (`li-cursor-agents`) — delegate `swarm_observer`
- [ ] Full preflight without `--skip-slow` — human/maintainer host

---

## Deliverable / findings

### Swarm execution evidence

Recent local run files (same tick as this grader):

| run_id | status | note |
|--------|--------|------|
| `ecosystem_grader-1780146986899` | running | this pass |
| `plan_verifier-1780147157338` | incomplete | no terminal completion |
| `proof_gap_researcher-1780147043795` | running | P0 research |
| `bench_improver-1780146968205` | running | numerics lane |

CP DB confirms wave dispatch at 13:16–13:19Z with null `briefing_hash` on all sampled rows — orchestration metadata not wired, not application test failures.

### Goal-directed runner summary

| runner | running | pending todos | last failure |
|--------|---------|---------------|--------------|
| httpd | idle (stale log) | 2 (wrk soak, streaming wrk) | exit 124 ×2 |
| studio-ui-ux | off | 2 (palette latency, GPU recovery) | — |
| sim-md-research | off | 1 (oracle plan) | — |
| sim-chem-research | off | 2 (dft scf, package placement) | gates_ok false |
| security-research | off | 3 (fuzz, exploit, runtime) | exit 1 on fuzz |
| swarm-observer | idle | 0 (plan complete) | — |
| compiler-studio, sim | off | 0 (complete) | — |

### Ecosystem audit highlights

- Red benchmarks: 6 (PH-5b numerics/ML matmul conv MLP gmres)
- Plan debt: 166 master-plan open items; 26 open checkboxes; 13 provability_partial, 4 provability_missing
- Workspace dirty: `lic` (6 files, swarm-observer branch), `benchmarks` (3 files, pr_reviewer digest branch)
- Open PRs: 0 — merge lane idle

---

## Recommended issues/PRs

| Title | Repo | Labels (suggested) |
|-------|------|-------------------|
| Terminalize stuck SDK runs + attach briefing_hash on dispatch | `li-cursor-agents` | `meta`, `swarm`, `control-plane` |
| Install canonical agent-kit on li-language | `li-language` | `agent-kit`, `ecosystem-gates` |
| Phase 7e tier-1: matmul_blocked / matmul_naive ≤1.2× C++ | `lic` | `benchmarks`, `PH-7e`, `numerics` |
| ML forward/train red rows — SIMD lowering follow-up | `lic` | `PH-5b`, `bench` |
| Restart httpd plan loop — wrk soak timeout (exit 124) | `lic` / `li-httpd` | `httpd`, `tier5`, `plan-loop` |
| Map plan_debt gaps → goal-directed runner backlogs | `lic` | `swarm-gap`, `orchestration` |
| Studio UX wave-2: palette search latency + GPU fail recovery | `lic-studio-ui` | `PH-UX`, `studio` |
| Open PRs for 147 orphan branches (triage batch) | org-wide | `hygiene`, `pr-branch` |

---

## Deferred

- **`code_implementer` / `bench_improver`** until `swarm_observer` + `gap_explorer` complete (avoid heap contention).
- **Full preflight suite** (plan_audit, explorer, pr_program, security_cwe) — run on next maintainer window without `--skip-slow`.
- **`pr_branch_opener` mass dispatch** (147 branches) — batch after workspace_sweeper clears dirty trees.
- **`docs_maintainer`** (1 repo without live pages) — P40 after gap_explorer.
- **`security_auditor` CWE Top25 catalog** (19 missing) — deferred; preflight skipped.
- **Human merge / protected-branch push** — out of scope for grader; no merges performed.
- **Control-plane PR implementation** — handoff to `swarm_observer` with `npm test` gate on `li-cursor-agents`.

---

## Handoff matrix

| Signal | Delegate to |
|--------|-------------|
| 89% incomplete / 111 stuck running | `swarm_observer` |
| 64 open gaps / 31 plan_debt | `gap_explorer` + `swarm_observer` apply pipeline |
| 6 red benchmarks | `ci_maintainer`, `bench_improver`, `numerics_researcher` |
| Runners stopped / plan_pending | Relevant plan loop or `plan_verifier`; human restart for httpd |
| Provability holes P0 | `proof_gap_researcher` |
