# Ecosystem grader digest — 2026-05-30 (proactive sweep)

**Agent:** `ecosystem_grader` · **Run:** `ecosystem_grader-1780104301830` · **Source:** proactive  
**Scorecard:** `data/latest/ecosystem-quality-report.json` @ 2026-05-30T01:28:19Z (regenerated this pass)  
**Briefing:** `data/latest/agent-briefing.json` @ 2026-05-30T01:07Z · hash `6594b2a691c9db00`  
**north_star_fit:** provable → easy → fast (PH-2i, PH-7e, PH-5b); meta-orchestration only — no product code edits

## Executive summary

- **Grade C · overall score 72.2 / 100 · unattended-safe: no** — down from stale B/83.2 after scorecard refresh on current briefing.
- **Primary degradation:** `swarm_execution` (60) — 107 runs stuck `running`, 23% incomplete rate on 13 terminal samples; delegate to **`swarm_observer`** first per scorecard.
- **Goal-directed loops starved:** `goal_directed_health` (70) — 3/4 runners stopped (`compiler-studio`, `sim`, `studio-ui-ux`); `httpd` process alive but log ~6.2h stale with 3 pending phase-2 todos.
- **Ecosystem posture mixed:** PR lane clear (`open_prs=0`, `failed_prs=0`) but **6 red benchmark rows** (PH-5b/7e) and **17-item CI bug queue** (`ci-bug-triage.json`).
- **Briefing preflight:** 2 scripts failed (`org_agent_kit_audit`, `security_cwe_audit` JSONDecodeError); `agent_deliverable_gate` skipped (`LI_CURSOR_AGENTS_ENABLED` unset).
- **Governance pressure:** 166 master-plan findings, 27 swarm-gap backlog (5 missing packages, 22 plan_debt); **`plan_verifier`** + **`implementation_gaps`** remain briefing P0.
- **Workspace hygiene:** 1 dirty sibling (`lic` on `chore/agent-docs_maintainer-20260530`, 3 files) — **`workspace_sweeper`** before implementers touch `lic`.
- **Control-plane signal:** 15+ concurrent SDK runs with `briefing_hash=null`; 7-day error counts dominated by workflow agents (288 `implementation_gaps`, 261 `bug_fixer` errors) — orchestration drift, not product regressions.

## Dimension drill-down

**briefing_health (84.0, weight 0.15)** — Briefing present with 13 recommended agents. Two preflight failures (`org_agent_kit_audit` exit 1: 9 repos missing/drifted agent-kit; `security_cwe_audit` exit 1: empty JSON input). One skip (`agent_deliverable_gate`). Preflight otherwise green (ecosystem audit, plan audit 166 findings, CI org audit 0 missing). Scorecard finding: `preflight-failures` (high).

**ecosystem_posture (67.0, weight 0.25)** — PR merge lane is empty (`open_prs=0`, `failed_prs=0`, `repos_missing_ci_main=0`) — improvement vs stale scorecard. Numerics lane degraded: **6 red rows** (`matmul_blocked`, `matmul_naive`, three `ml_*` stubs, `num_gmres`). Docs gap: 8 repos without live Pages. Scorecard recommends **`ci_maintainer`** for weak posture despite clean PR metrics; numerics work routes via heap `coord_numerics`.

**goal_directed_health (70.0, weight 0.2)** — Snapshot present: 4 runners, 17/75 plan todos pending, **0 agents_live**. Stopped: `compiler-studio` (supervisor off, plan complete), `sim` (1 pending `sim-p2-qm-dft-scf`, log 5.4d stale), `studio-ui-ux` (supervisor off). `httpd` marked running but supervisor idle (log 22291s stale; pending: perf wrk soak, mitigation exploits, streaming wrk). Finding: `goal-runners-stopped` (high).

**swarm_execution (60.0, weight 0.25)** — Sampled 120 runs from `li-cursor-agents/data/runs`: 13 terminal, 107 still `running`, 1 error, 3 incomplete (23% incomplete rate, 7.7% error rate). Top error agent: `bug_fixer` (1 in sample). Likely SDK status reconciliation failure — many runs show `status: running` in JSON while control-plane marks prior tick as `error`. Findings: `swarm-incomplete-rate` (medium), `swarm-many-running` (medium). **Do not dispatch more implementers until `swarm_observer` triages.**

**gap_pressure (92.0, weight 0.15)** — 27 open gaps in `swarm-gap-actions.json` (5 `missing_package`: std.io/csv/summary/plot, line-profiler; 22 `plan_debt`). Low severity finding; apply pipeline owned by **`gap_explorer`** + **`swarm_observer`**.

## Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|----------------------|
| `preflight-failures` | high | `agent-briefing.json` → `preflight_runs.org_agent_kit_audit`, `security_cwe_audit` | `agent_kit_maintainer`, `security_auditor` |
| `benchmark-red-rows` | high | `ecosystem-audit.json` → `benchmarks.red` (6 rows) | `numerics_researcher`, `bench_improver` |
| `goal-runners-stopped` | high | `lic/data/goal-directed-agents/snapshot.json` | `plan_verifier` + restart httpd/sim/studio loops |
| `swarm-incomplete-rate` | medium | `li-cursor-agents/data/runs/*.json` | **`swarm_observer`** |
| `swarm-many-running` | medium | `li-cursor-agents/data/runs/*.json` + control-plane `agent_runs` | **`swarm_observer`** |
| `repos-missing-live-docs` | low | `ecosystem-audit.json` → `metrics.repos_without_live_pages=8` | `docs_maintainer` |
| `swarm-gap-backlog` | low | `data/latest/swarm-gap-actions.json` | `gap_explorer` |

## Recommended dispatch order

Align scorecard `recommended_agents` with briefing heap (`coord_*` priority) and P0 governance. **Gate implementers behind meta fixes.**

| Order | Agent | Coordinator / lane | Reason |
|------:|-------|---------------------|--------|
| 1 | **`swarm_observer`** | meta | Scorecard P0 — `swarm_execution` 60; reconcile 107 stuck runs, incomplete rate |
| 2 | **`workspace_sweeper`** | platform | Briefing P0 — dirty `lic` workspace before numerics/CI agents |
| 3 | **`pr_alignment`** | `coord_pull_requests` (p10) | 1 PR flagged close/supersede (`pr-branch-hygiene.json`) |
| 4 | **`plan_verifier`** | `coord_governance` (p30) | 166 plan-completion findings; restart stopped goal loops |
| 5 | **`implementation_gaps`** | `coord_governance` (p30) | Cross-check plan vs implementation |
| 6 | **`numerics_researcher`** → **`bench_improver`** | `coord_numerics` (p20) | 6 red rows; defer until swarm_observer clears run backlog |
| 7 | **`gap_explorer`** | `coord_ecosystem` (p40) | 2 missing std modules + gap registry |
| 8 | **`agent_kit_maintainer`** | `coord_platform` (p50) | 9 repos missing/drifted kit |
| 9 | **`docs_maintainer`** | `coord_ecosystem` (p40) | 8 repos without live docs |
| 10 | **`bug_fixer`** → **`code_implementer`** | implementation | 17 CI queue items — **after** swarm_observer + workspace_sweeper |
| 11 | **`ci_maintainer`** | platform | Scorecard posture signal; org CI audit currently 0 missing |
| 12 | **`security_auditor`** | security | CWE audit script broken; Top25 missing_in_catalog=19 |
| 13 | **`pr_branch_opener`** | PR hygiene | 133 branches pushed without open PR (low urgency vs empty merge queue) |

**Handoffs (meta-agents):**

| Signal | Delegate |
|--------|----------|
| 23% incomplete + 107 running | `swarm_observer` — control-plane status reconciliation, prompt/runner fixes |
| 27 gap backlog / plan_debt | `gap_explorer` + `swarm_observer` apply pipeline |
| 6 red benchmarks | `numerics_researcher`, `bench_improver` via `coord_numerics` |
| 3 stopped runners + 17 pending todos | Restart `httpd-plan-until-deadline.sh`; `sim`/`studio-ui-ux` supervisors; `plan_verifier` |

## Human-only blockers

- **`security_cwe_audit.py`** — `JSONDecodeError: Expecting value: line 1 column 1` on empty input; fix script input path or feed file before `security_auditor` can pass preflight.
- **`LI_CURSOR_AGENTS_ENABLED=1`** — required to enable `agent_deliverable_gate` scan; currently skipped.
- **Merge queue empty** — `open_prs=0`; no auto-merge candidates; human `merge-approved` labels blocked until PRs exist.
- **133 orphan branches** — `pr_branch_opener` can draft PRs but human review needed for close/supersede decisions (`pr_alignment`).
- **Governance PRs** — `roadmap` agent-kit canonical stamp `1.3.5+6018e18bf2ed91f4`; human merge for cross-repo kit rollouts.
- **Provability gates** — do not disable Lean policy or edit `trusted.lean` without human-approved issues.

## Deliverable / findings

### Scorecard delta (stale → refreshed)

| Field | Stale (2026-05-27) | Fresh (2026-05-30) |
|-------|--------------------|--------------------|
| overall_score | 83.2 | **72.2** |
| grade | B | **C** |
| unattended_safe | true | **false** |
| ecosystem_posture | 47 (87 open PRs, 54 failed) | **67** (0 open, 0 failed, 6 red benches) |
| goal_directed_health | 100 | **70** (3 stopped runners) |
| swarm_execution | 100 | **60** (107 running) |

### Coordinator lane health

| Coordinator | Status | Evidence |
|-------------|--------|----------|
| `coord_pull_requests` | **Green** | 0 open PRs; 1 supersede review pending |
| `coord_numerics` | **Red** | 6 dashboard red rows; `bench_improver` pass notes `matmul_naive` fixed locally, ingest stale |
| `coord_governance` | **Yellow** | 166 plan findings; goal loops stalled |
| `coord_ecosystem` | **Yellow** | 8 docs gaps, 2 missing std modules, 27 swarm gaps |
| `coord_platform` | **Yellow** | 9 agent-kit drifts; swarm execution degraded |

### Goal-directed runner snapshot

| Runner | Running | Pending todos | Note |
|--------|---------|---------------|------|
| `httpd` | yes (stale) | 3 | `gap-phase2-perf-wrk-soak`, mitigation exploits, streaming wrk |
| `compiler-studio` | no | 0 | supervisor off — wave complete |
| `sim` | no | 1 | `sim-p2-qm-dft-scf`; log 5.4d old |
| `studio-ui-ux` | no | 0 | supervisor off |

### Swarm execution drift (sample)

Control-plane (7d): top `error` statuses — `implementation_gaps` 288, `workspace_sweeper` 284, `bug_fixer` 261. Current tick: 15 agents `running` with `briefing_hash=null` (SDK runs not linked to briefing snapshot). Prior `ecosystem_grader-1780104224223` marked `error` in DB while JSON still `running` — status reconciliation bug.

### CI / bug queue (17 items)

- 1 `local_ci`: **lic#439** (`ci-bug-triage.json`)
- 16 `pr_ci`: lip (4), lit (3), others — GHA checks failing
- **`bug_fixer`** queued on lic#439 this tick

## Recommended issues/PRs

| Title | Repo | Labels / notes |
|-------|------|----------------|
| fix(control-plane): reconcile stuck `running` agent_runs + briefing_hash linkage | **li-cursor-agents** | `swarm`, `agent:swarm_observer`; run `npm test` |
| fix(scripts): security-cwe-audit empty JSON input | **benchmarks** | unblocks preflight; `security_auditor` |
| chore(agent-kit): sync canonical stamp to 9 drifted repos | **li-demo**, **li-httpd**, **li-language**, **li-net**, **li-std-***, **lic**, **lis**, **roadmap** | `agent:agent_kit_maintainer`; separate PRs per repo |
| perf(7e): matmul_blocked emit — FMA/SIMD on blocked IKJ | **lic** | `PH-7e`, `numerics`; largest red (1.55×) |
| chore: CI re-ingest after matmul_naive `@` merge | **benchmarks** | refresh dashboard oracle |
| fix: lic#439 local-ci failure | **lic** | `agent:bug_fixer`; queued this tick |
| docs: enable GitHub Pages for 8 repos without live docs | various | `agent:docs_maintainer` |
| governance: review 1 PR for close/supersede | per `pr-branch-hygiene.json` | `agent:pr_alignment` |
| restart: httpd plan loop phase-2 perf/soak todos | **lic** | human supervisor or `./scripts/httpd-plan-until-deadline.sh` |

## Deferred

- **`pr_branch_opener`** for 133 orphan branches — low priority while merge queue empty; risk of PR noise.
- **`ml_*` stub benchmarks** — measurement artifacts until real kernels (`bench_improver` digest).
- **22 plan_debt gaps** in swarm registry — no runner backlog mapping; defer to master-plan phases.
- **42 unknown harness rows** — tier 0/5/6 smoke not ingested.
- **Full CI ingest cycle** — do not hand-edit `summary.json`; wait for lic CI + `ingest-lic.sh`.
- **Self-merge / protected branches** — out of scope for all agents.

## Agent deliverable checklist

- [x] Regenerated scorecard (`python3 scripts/ecosystem-quality-grade.py`)
- [x] Cited fields from `ecosystem-quality-report.json` (no manual rescoring)
- [x] Dimension drill-down, top findings table, dispatch order, human blockers
- [x] Digest written to `data/runs/ecosystem_grader-1780104301830.md`
- [x] Control-plane DB queried (read-only) for run status corroboration
- [ ] Control-plane prompt edits — **deferred** to `swarm_observer` PR on `li-cursor-agents`
- [ ] No PRs opened, no merges, no protected-branch pushes
