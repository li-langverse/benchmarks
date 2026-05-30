# Ecosystem grader digest — `ecosystem_grader-1780149516754`

**Date:** 2026-05-30T13:58Z  
**Agent:** `ecosystem_grader`  
**Source:** proactive sweep  
**north_star_fit:** ecosystem orchestration; provable pillar (PH-2i, PH-2f, `provability_holes`)  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-30T13:56Z, hash `97f384a14707ebf4`)  
**Scorecard:** `data/latest/ecosystem-quality-report.json` (refreshed 2026-05-30T13:58:27Z)

---

## Executive summary

- **Grade C — 78.2/100** (`overall_score`, `grade`); **`unattended_safe: true`** — improved from prior D/69 after benchmark reds cleared and preflight failures dropped to 0.
- **Degraded lanes:** `swarm_execution` **70.0**, `gap_pressure` **60.0**, `goal_directed_health` **70.0** — meta agents should run before broad implementer waves.
- **Strong lanes:** `ecosystem_posture` **100.0** (0 red benchmarks, 0 failed PRs, 0 repos missing CI); `briefing_health` **85.0** (0 preflight failures, 8 skipped slow scripts).
- **Goal-directed loops starved:** 6/8 runners stopped; `agents_live: 0`; httpd loop idle after **exit 124** (timeout) on wrk-soak todos.
- **Gap backlog:** 64 open registry rows (31 `plan_debt`, 30 `competitor_feature`, 3 `missing_package`) — `gap_explorer` + `swarm_observer` apply pipeline.
- **Swarm execution drift:** 84% incomplete rate in terminal sample (27/32), 88 runs still `running`; CP shows mass `error` status (SDK wave kills, not product regressions).
- **Briefing P0 preserved:** `proof_gap_researcher` (provability_holes priority 9) → `workspace_sweeper` → governance heap — scorecard does not contradict.
- **Control-plane report stale:** latest `control_plane_reports` @ 2026-05-25 — dashboard under-reports current briefing hash.

---

## Dimension drill-down

### briefing_health (85.0)

Briefing is present with 10 `recommended_agents` and zero preflight failures (`preflight_failed: 0`). Eight slow scripts remain skipped (`plan_audit`, `explorer`, `ci_bug_triage`, `pr_program`, etc.), which limits PR-program and plan-audit freshness but does not block unattended operation per scorecard. Org CI and agent-kit audits now pass (exit 0). The medium finding `preflight-skipped` is informational — full preflight requires dropping `--skip-slow` on the briefing generator.

### ecosystem_posture (100.0)

Ecosystem audit shows **0 red** benchmark rows (yellow: `matmul_blocked`, `matmul_naive`; near-threshold: `num_integ_rk4`, `simd_dot`, `fft_1d_fixed`). Org metrics: 0 open/failed PRs in audit snapshot, 0 repos missing CI on main, 12 repos with live docs pages. No scorecard findings in this dimension — `ci_maintainer` / `bench_improver` are briefing-secondary (yellow tier-1 advisory), not scorecard-mandated this cycle.

### goal_directed_health (70.0)

Snapshot present (`lic/data/goal-directed-agents/snapshot.json`, 2026-05-30T13:58Z): 8 runners, **6 stopped**, 25/97 plan todos pending, `agents_live: 0`. Stopped: `compiler-studio`, `sim-algo`, `studio-ui-ux`, `sim-md-research`, `sim-chem-research`, `security-research`. Active supervisor: `httpd` (process alive) but **agent idle** — last batch exit **124** on `gap-phase2-perf-wrk-soak` and `gap-phase2-streaming-wrk` (~7h stale log). `swarm-observer` runner also idle. High finding `goal-runners-stopped` → restart plan loops or delegate `plan_verifier` + domain implementers per runner backlog.

### swarm_execution (70.0)

Sampled 120 local runs: 32 terminal, 27 incomplete (84%), 1 error (`gui_ui_tester`), 88 still `running`. CP DB corroborates high `error` counts per agent (historical mislabeling + SDK preemption). Recent tick @ 13:54Z shows simultaneous `error` on 10+ agents — supervisor wave kill pattern, not repo merge conflicts. Delegate **`swarm_observer`**: terminalize stuck `running` after TTL, reconcile status labels, refresh `control_plane_reports.swarm_health`.

### gap_pressure (60.0)

`swarm-gap-actions.json`: **64 open** gaps. Kinds: 31 `plan_debt`, 30 `competitor_feature`, 3 `missing_package` (`std.summary`, `std.plot`, `li-line-profiler` — patched pending in backlog). Medium finding `plan-debt-gaps` ties to master-plan partial phases (2i, 7d, 7e, Vision-LLM). **`gap_explorer`** reconciles registry; **`swarm_observer`** runs ingest/apply; implementers defer until meta lane clears highest plan_debt rows mapped to runners.

---

## Deliverable / findings

### Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|----------------------|
| `goal-runners-stopped` | high | `lic/data/goal-directed-agents/snapshot.json` | `plan_verifier` + domain plan loops (`httpd`, `compiler-studio`, research loops) |
| `swarm-gap-backlog` | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| `swarm-incomplete-rate` | medium | `li-cursor-agents/data/runs` | `swarm_observer` |
| `swarm-many-running` | medium | `li-cursor-agents/data/runs` | `swarm_observer` |
| `preflight-skipped` | medium | `agent-briefing.preflight_runs` | human / briefing cron (drop `--skip-slow`) |
| `plan-debt-gaps` | medium | `swarm-gap-actions.by_kind.plan_debt` | `plan_verifier`, `implementation_gaps` |

### Recommended dispatch order

Aligned with scorecard `recommended_agents` + briefing P0 + heap `flat_tasks` (do not skip P0):

| Order | agent | reason (source) |
|-------|-------|-----------------|
| 1 | `proof_gap_researcher` | Briefing P0 + scorecard — `provability_holes` priority 9 |
| 2 | `workspace_sweeper` | Briefing P0 + scorecard — 1 dirty `lic` sibling (safe runtime files) |
| 3 | `swarm_observer` | Scorecard — `swarm_execution` 70.0; stuck `running` / incomplete drift |
| 4 | `gap_explorer` | Scorecard — `gap_pressure` 60.0; 2 missing std modules in briefing |
| 5 | `plan_verifier` | Scorecard + briefing P0 — 166 plan findings, 26 open checkboxes |
| 6 | `pr_alignment` | Heap P10 — 14 draft PRs flagged close/supersede (`pr-branch-hygiene.json`) |
| 7 | `implementation_gaps` | Heap P30 — plan vs implementation cross-check |
| 8 | `issue_hygiene` | Heap P30 — dup_clusters=4, explorer_spam_repos=2 |
| 9 | `bug_fixer` → `code_implementer` | Briefing — `lic#439` local-ci failed (2 li-tests failures) |
| 10 | `security_auditor` | Briefing — 19 CWE Top-25 missing in catalog (no workflow gaps) |

**Deferred from scorecard this cycle:** `ci_maintainer`, `bench_improver` (ecosystem_posture 100; yellow-only benchmarks). Run if full `ecosystem_audit` refresh shows new reds.

### Human-only blockers

| Blocker | detail |
|---------|--------|
| Draft PR closure | 14 draft PRs (`lic` #530–540, #432; `benchmarks` #182–230; `roadmap` #26) — all `safe_now: false`; human confirm abandoned before `pr_alignment` closes |
| `lic#439` CI | local-ci: 2 failed / 253 passed in `lic-host` profile — needs human triage or `bug_fixer` with log access |
| Full preflight | 8 scripts skipped `--skip-slow`; `agent_deliverable_gate` disabled (`LI_CURSOR_AGENTS_ENABLED` unset) |
| Provability governance | `trusted.lean` changes require human-approved issues — no agent bypass |
| CP dashboard staleness | `control_plane_reports` latest @ 2026-05-25 vs briefing `97f384a…` @ 2026-05-30 |
| Goal loop timeouts | httpd todos exit **124** — extend deadline or fix wrk-soak harness before unattended httpd loop |

### Agent deliverable checklist

- [x] Regenerated `ecosystem-quality-report.json` (78.2, grade C, `unattended_safe: true`)
- [x] Read `agent-briefing.json`, goal-directed snapshot, swarm-gap-actions
- [x] CP DB sampled (`agent_runs` status histogram, recent errors)
- [x] Dispatch order reconciled (scorecard + briefing P0 + heap)
- [x] Narrative filed under `data/runs/`
- [ ] `swarm_observer` PR for observer terminalization (li-cursor-agents, `npm test`)
- [ ] Full briefing without `--skip-slow` (human/cron)

### Handoff to meta-agents

| Signal | Delegate to |
|--------|-------------|
| 84% incomplete / 88 `running` | `swarm_observer` — CP prompt + status reconciliation |
| 64 open gaps / 31 plan_debt | `gap_explorer` + `swarm_observer` apply pipeline |
| 6 runners stopped / httpd exit 124 | `plan_verifier` + restart relevant plan loop |
| Yellow matmul (tier-1 advisory) | `bench_improver`, `numerics_researcher` when numerics coord active |

---

## Recommended issues/PRs

| Title | Repo | Labels / action |
|-------|------|-----------------|
| [plan-needed] PH-2i: full NumPy-rank broadcast — define reject gate + defer criteria (G-math) | `lic` #526 | `master-plan-gap`, `plan-needed` |
| [plan-needed] PH-2h / G-math-syn: for/range surface — define parse+typecheck Done gate | `lic` #527 | `master-plan-gap`, `plan-needed` |
| [master-plan-gap] PH-8p-c: lic build --jobs=N sets LI_COMPILE_JOBS but compiler never reads it | `lic` #525 | `master-plan-gap`, `plan-needed` |
| [master-plan-gap] sim-md-research: md-r3-oracle-plan pending | `lic` #523 | `master-plan-gap`, `plan-needed` |
| **Fix local-ci failures on PR 439** | `lic` PR [#439](https://github.com/li-langverse/lic/pull/439) | `bug_fixer` / `code_implementer` |
| **Review 14 abandoned draft PRs for close** | `lic`, `benchmarks`, `roadmap` | `pr_alignment`; see `data/latest/pr-branch-hygiene.json` |
| CWE Top-25 catalog coverage (19 missing) | `lic` cve-catalog | `security_auditor` |
| Missing std: `std.summary`, `std.plot` | `lic` | `gap_explorer` → `code_implementer` |

---

## Deferred

- **`bench_improver` / `numerics_researcher`** — no red rows; yellow `matmul_*` only (PH-5b/7e advisory).
- **`ci_maintainer`** — `repos_missing_ci_main: 0`.
- **`docs_maintainer`** — `repos_without_live_pages: 0` in current audit.
- **`agent_kit_maintainer`** — org agent-kit audit OK (12/12).
- **Full `plan_audit` / `explorer` / `ci_bug_triage`** — blocked on `--skip-slow` until next full briefing run.
- **`ecosystem_grader` self-dispatch** — removed from scorecard recommended list (overall ≥70); this run is proactive narrative only.
- **Merge queue** — `next_merge: null`, 0 gate-ready PRs.

---

## Paths (dashboard)

| Artifact | Path |
|----------|------|
| Scorecard | `benchmarks/data/latest/ecosystem-quality-report.json` |
| Briefing | `benchmarks/data/latest/agent-briefing.json` |
| Gap actions | `benchmarks/data/latest/swarm-gap-actions.json` |
| Goal runners | `lic/data/goal-directed-agents/snapshot.json` |
| PR hygiene | `benchmarks/data/latest/pr-branch-hygiene.json` |
| This digest | `benchmarks/data/runs/ecosystem_grader-1780149516754.md` |
