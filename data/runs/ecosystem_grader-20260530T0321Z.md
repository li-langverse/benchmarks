# Ecosystem grader digest — 2026-05-30 (proactive sweep)

**Agent:** `ecosystem_grader` · **Run:** `ecosystem_grader-20260530T0321Z` · **Source:** proactive  
**Scorecard:** `data/latest/ecosystem-quality-report.json` @ 2026-05-30T03:21:16Z (regenerated this pass)  
**Briefing:** `data/latest/agent-briefing.json` @ 2026-05-30T02:05Z  
**north_star_fit:** provable → easy → fast (PH-2i, PH-7e, PH-5b); meta-orchestration only — no product code edits

---

## Executive summary

- **Grade C · overall score 78.6 / 100 · unattended-safe: yes** — up from prior C/72.2; `swarm_execution` recovered to 90 while numerics and goal loops remain degraded.
- **Primary degradation:** `ecosystem_posture` (67) — **6 red benchmark rows** (PH-5b/7e: `matmul_blocked`, `matmul_naive`, three `ml_*`, `num_gmres`); PR lane clear (`open_prs=0`, `failed_prs=0`).
- **Goal-directed loops starved:** `goal_directed_health` (70) — 3/4 runners stopped (`compiler-studio`, `sim`, `studio-ui-ux`); `httpd` process alive but log ~8.1h stale with **2 pending** phase-2 perf/soak todos.
- **Briefing preflight:** 1 script failed (`org_agent_kit_audit` exit 1 — 9 repos missing/drifted agent-kit); **8 scripts skipped** (`--skip-slow`); `agent_deliverable_gate` skipped (`LI_CURSOR_AGENTS_ENABLED` unset).
- **Governance pressure:** 166 master-plan findings, 27 swarm-gap backlog (5 missing packages, 22 plan_debt); briefing P0: **`workspace_sweeper`**, **`plan_verifier`**, **`implementation_gaps`**.
- **Swarm execution improved:** sampled 120 local run JSONs — 0% error/incomplete rate; **113 still marked `running`** in files (SDK reconciliation drift); control-plane DB shows 22 `running`, 5534 historical `error`.
- **Workspace hygiene:** 1 dirty sibling (`lic` on `cursor/httpd-plan-continue`, 5 safe files) — sweep before numerics agents touch `lic`.
- **Merge queue empty** — no open PRs; 164 orphan branches queued for `pr_branch_opener` (deferred vs meta fixes).

---

## Dimension drill-down

**briefing_health (77.0, weight 0.15)** — Briefing present with 12 recommended agents. One preflight failure: `org_agent_kit_audit` exit 1 (9 repos missing or drifted agent-kit; canonical `1.3.5+6018e18bf2ed91f4`). Eight slow preflights skipped (`plan_audit`, `issue_hygiene`, `explorer`, `pr_program`, `pr_branch_hygiene`, `ci_bug_triage`, `security_cwe_audit`, `agent_deliverable_gate`). Ecosystem audit and workspace dirty sweep green. Scorecard findings: `preflight-failures` (medium), `preflight-skipped` (medium).

**ecosystem_posture (67.0, weight 0.25)** — PR merge lane is empty and org CI audit reports 0 repos missing CI on main. Numerics lane is the drag: **6 red rows** at 1.33–1.55× cpp (`ecosystem-audit.json` → `benchmarks.red`). Docs gap persists: 8 repos without live GitHub Pages. Scorecard recommends **`ci_maintainer`** for weak posture signal despite clean PR metrics; numerics work routes via heap `coord_numerics` (`numerics_researcher` → `bench_improver`).

**goal_directed_health (70.0, weight 0.2)** — Snapshot present: 4 runners, 16/75 plan todos pending, **0 agents_live**. Stopped: `compiler-studio` (supervisor off, 47/47 complete), `sim` (1 pending `sim-p2-qm-dft-scf`, log ~5.4d stale), `studio-ui-ux` (supervisor off, 13/13 complete). `httpd` marked running but supervisor idle (`log_age_sec` ~29084; pending: `gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk`). Finding: `goal-runners-stopped` (high).

**swarm_execution (90.0, weight 0.25)** — Sampled 120 runs from `li-cursor-agents/data/runs`: 7 terminal, **113 still `running`**, 0 error, 0 incomplete in the sample (0% error/incomplete rates). Control-plane corroboration: 22 DB rows `running` (started ~03:18Z this tick, `briefing_hash=null`); 5534 historical `error` statuses dominated by workflow agents. Finding: `swarm-many-running` (medium) — likely SDK status reconciliation, not product regressions. Prior `swarm-incomplete-rate` finding cleared this pass.

**gap_pressure (92.0, weight 0.15)** — 27 open gaps in `swarm-gap-actions.json` (5 `missing_package`: std.io/csv/summary/plot, line-profiler; 22 `plan_debt`). Low severity finding `swarm-gap-backlog`; apply pipeline owned by **`gap_explorer`** + **`swarm_observer`**.

---

## Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|----------------------|
| `benchmark-red-rows` | high | `ecosystem-audit.json` → `benchmarks.red` (6 rows) | `numerics_researcher`, `bench_improver` |
| `goal-runners-stopped` | high | `lic/data/goal-directed-agents/snapshot.json` | `plan_verifier` + restart httpd/sim loops |
| `preflight-failures` | medium | `agent-briefing.json` → `preflight_runs.org_agent_kit_audit` | `agent_kit_maintainer` |
| `preflight-skipped` | medium | `agent-briefing.json` → `preflight_runs` (8 × `--skip-slow`) | human: run full preflight cycle |
| `swarm-many-running` | medium | `li-cursor-agents/data/runs/*.json` (113 running in sample) | `swarm_observer` |
| `repos-missing-live-docs` | low | `ecosystem-audit.json` → `metrics.repos_without_live_pages=8` | `docs_maintainer` |
| `swarm-gap-backlog` | low | `data/latest/swarm-gap-actions.json` | `gap_explorer` |

---

## Recommended dispatch order

Align scorecard `recommended_agents` with briefing heap (`coord_*` priority). Briefing P0 (`workspace_sweeper`, `plan_verifier`, `implementation_gaps`) takes precedence over scorecard-only picks unless cited below.

| Order | Agent | Coordinator / lane | Reason |
|------:|-------|---------------------|--------|
| 1 | **`workspace_sweeper`** | platform | Briefing P0 + scorecard P0 — dirty `lic` on `cursor/httpd-plan-continue` |
| 2 | **`plan_verifier`** | `coord_governance` (p30) | Scorecard + briefing P0 — 166 plan-completion findings; refresh skipped `plan_audit` |
| 3 | **`implementation_gaps`** | `coord_governance` (p30) | Briefing P0 — cross-check plan vs implementation |
| 4 | **`swarm_observer`** | meta | 113 file-JSON runs stuck `running`; reconcile status + `briefing_hash` linkage |
| 5 | **`numerics_researcher`** → **`bench_improver`** | `coord_numerics` (p20) | 6 red rows (PH-5b/7e); after workspace sweep |
| 6 | **`gap_explorer`** | `coord_ecosystem` (p40) | 2 missing std modules + 27 gap registry |
| 7 | **`agent_kit_maintainer`** | `coord_platform` (p50) | 9 repos missing/drifted kit (preflight exit 1) |
| 8 | **`docs_maintainer`** | `coord_ecosystem` (p40) | 8 repos without live docs |
| 9 | **`bug_fixer`** → **`code_implementer`** | implementation | 1 CI/bug item in work queue (skipped triage this pass) |
| 10 | **`security_auditor`** | security | Top25 missing_in_catalog=19 (`cwe_feed_sync` green; full audit skipped) |
| 11 | **`ci_maintainer`** | platform | Scorecard posture signal |
| 12 | **`pr_branch_opener`** | PR hygiene | 164 branches without open PR — low urgency vs empty merge queue |

**Handoffs (meta-agents):**

| Signal | Delegate |
|--------|----------|
| 113 runs stuck `running` in file sample | `swarm_observer` — control-plane status reconciliation |
| 27 gap backlog / plan_debt | `gap_explorer` + `swarm_observer` apply pipeline |
| 6 red benchmarks | `numerics_researcher`, `bench_improver` via `coord_numerics` |
| 3 stopped runners + 16 pending todos | Restart `httpd-plan-until-deadline.sh`; `sim` supervisor; `plan_verifier` |

---

## Human-only blockers

- **`LI_CURSOR_AGENTS_ENABLED=1`** — required to enable `agent_deliverable_gate` scan; currently skipped.
- **Full preflight cycle** — 8 scripts skipped with `--skip-slow` (`plan_audit`, `ci_bug_triage`, `security_cwe_audit`, etc.); run without skip before unattended dispatch escalates.
- **Merge queue empty** — `open_prs=0`; no auto-merge candidates; human `merge-approved` labels blocked until PRs exist.
- **164 orphan branches** — `pr_branch_opener` can draft PRs but human review needed for close/supersede decisions.
- **Governance PRs** — agent-kit canonical stamp `1.3.5+6018e18bf2ed91f4`; human merge for cross-repo kit rollouts.
- **Provability gates** — do not disable Lean policy or edit `trusted.lean` without human-approved issues.
- **httpd plan loop** — supervisor idle ~8h; human may restart `./scripts/httpd-plan-until-deadline.sh` for phase-2 perf/soak todos.

---

## Deliverable / findings

### Scorecard delta (prior pass → refreshed)

| Field | Prior (2026-05-30T01:28Z) | Fresh (2026-05-30T03:21Z) |
|-------|---------------------------|---------------------------|
| overall_score | 72.2 | **78.6** |
| grade | C | **C** |
| unattended_safe | false | **true** |
| briefing_health | 84.0 | **77.0** (more skips surfaced) |
| swarm_execution | 60.0 | **90.0** (0% error/incomplete in sample) |
| ecosystem_posture | 67.0 | **67.0** (6 red benches unchanged) |
| goal_directed_health | 70.0 | **70.0** (3 stopped runners) |

### Coordinator lane health

| Coordinator | Status | Evidence |
|-------------|--------|----------|
| `coord_pull_requests` | **Green** | 0 open PRs, 0 failed PRs |
| `coord_numerics` | **Red** | 6 dashboard red rows; heap p20 |
| `coord_governance` | **Yellow** | 166 plan findings; goal loops stalled |
| `coord_ecosystem` | **Yellow** | 8 docs gaps, 2 missing std modules, 27 swarm gaps |
| `coord_platform` | **Yellow** | 9 agent-kit drifts; workspace dirty |

### Goal-directed runner snapshot

| Runner | Running | Pending todos | Note |
|--------|---------|---------------|------|
| `httpd` | yes (stale) | 2 | `gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk` |
| `compiler-studio` | no | 0 | supervisor off — 47/47 complete |
| `sim` | no | 1 | `sim-p2-qm-dft-scf`; log ~5.4d old |
| `studio-ui-ux` | no | 0 | supervisor off — 13/13 complete |

### Swarm execution (control-plane corroboration)

```text
agent_runs status counts: error=5534, finished=283, incomplete=22, running=22
```

Current tick: 10+ agents `running` with `briefing_hash=null` (SDK runs not linked to briefing snapshot). Top historical `error` agents: `implementation_gaps` (339), `workspace_sweeper` (334), `bug_fixer` (307) — orchestration churn, not product regressions.

### Red benchmark rows (PH-5b / PH-7e)

| id | ratio_vs_cpp | ph_ids |
|----|--------------|--------|
| `matmul_blocked` | 1.549 | PH-5b |
| `matmul_naive` | 1.3333 | PH-5b, PH-7e |
| `ml_conv2d_forward` | 1.3333 | PH-5b |
| `ml_mlp_forward` | 1.3333 | PH-5b |
| `ml_mlp_train_step` | 1.3333 | PH-5b |
| `num_gmres` | 1.4 | PH-5b |

137 green rows; 2 yellow; 5 near-threshold; 42 unknown (tier0/5/6 smoke not ingested).

---

## Recommended issues/PRs

| Title | Repo | Labels / notes |
|-------|------|----------------|
| fix(control-plane): reconcile stuck `running` agent_runs + briefing_hash linkage | **li-cursor-agents** | `swarm`, `agent:swarm_observer`; run `npm test` |
| chore(agent-kit): sync canonical stamp to 9 drifted repos | **li-demo**, **li-httpd**, **li-language**, **li-net**, **li-std-***, **lic**, **lis**, **roadmap** | `agent:agent_kit_maintainer`; separate PRs per repo |
| perf(7e): matmul_blocked emit — blocked IKJ + FMA/SIMD | **lic** | `PH-7e`, `numerics`; largest red (1.55×) |
| perf(7e): matmul_naive + ml_* stub kernels — honest tier-1 parity | **lic** | `PH-5b`, `PH-7e`; coordinate `bench_improver` |
| chore: full preflight without `--skip-slow` | **benchmarks** | unblocks `plan_audit`, `ci_bug_triage`, `security_cwe_audit` |
| docs: enable GitHub Pages for 8 repos without live docs | various | `agent:docs_maintainer` |
| restart: httpd plan loop phase-2 perf/soak todos | **lic** | human supervisor or `./scripts/httpd-plan-until-deadline.sh` |
| sim: resume `sim-p2-qm-dft-scf` goal loop | **lic** (sim worktree) | `agent:plan_verifier` handoff |

*Do **not** self-merge PRs.*

---

## Deferred

- **`pr_branch_opener`** for 164 orphan branches — low priority while merge queue empty; risk of PR noise.
- **`ml_*` stub benchmarks** — measurement artifacts until real kernels land.
- **22 plan_debt gaps** in swarm registry — no runner backlog mapping; defer to master-plan phases.
- **42 unknown harness rows** — tier 0/5/6 smoke not ingested; separate hygiene pass.
- **Full CI ingest cycle** — do not hand-edit `summary.json`; wait for lic CI + `ingest-lic.sh`.
- **Control-plane prompt edits** — deferred to `swarm_observer` PR on `li-cursor-agents`.
- **Self-merge / protected branches** — out of scope for all agents.

---

## Agent deliverable checklist

- [x] Regenerated scorecard (`python3 scripts/ecosystem-quality-grade.py`)
- [x] Cited fields from `ecosystem-quality-report.json` (no manual rescoring)
- [x] Dimension drill-down, top findings table, dispatch order, human blockers
- [x] Digest written to `data/runs/ecosystem_grader-20260530T0321Z.md`
- [x] Control-plane DB queried (read-only) for run status corroboration
- [ ] Control-plane prompt edits — **deferred** to `swarm_observer` PR on `li-cursor-agents`
- [ ] No PRs opened, no merges, no protected-branch pushes
