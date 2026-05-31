# Swarm observer digest — `swarm_observer-1780189200`

**Date:** 2026-05-31T01:00Z  
**Agent:** `swarm_observer`  
**Research goal:** `swarm_coverage` (north_star_fit: ecosystem + ai — registry, backlog apply, handoffs)  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-31T00:53Z)  
**Scorecard:** `data/latest/ecosystem-quality-report.json` (82.0, grade **B**, `unattended_safe: true`)  
**Orchestrator note:** `lic/docs/ecosystem/orchestrator-notes/2026-05-31-orch-r4-ui-ux-signals.md`

---

## Executive summary

- **Posture: degraded (recoverable)** — grade **B** (82.0); ecosystem posture strong (100) vs gap pressure (60) and goal-directed health (70).
- **Unattended: marginal** — scorecard `unattended_safe: true`, but 64 open registry gaps, 6/9 plan runners stopped, and async-swarm wave-kill churn need periodic meta audits.
- **`orch-r3` done** — 3 `missing_package` gaps patched to `ecosystem-package-backlog.md`; this pass advances **`orch-r4-ui-ux-signals`** (studio UX todos linked).
- **SDK wave-kill spike @ 00:50Z** — supervisor restart killed ~24 agents (20 errors/agent today); root cause is control-plane restart + global SDK lock, not missing `CURSOR_API_KEY`.
- **Programmatic observer healthy** — `retry_counts: {}`, `stopped_agents: []`; no auto-heal budget exhausted; `swarm_degraded` not surfaced.
- **Goal-directed drift** — `agents_live: 0` in scorecard but 3 runners active (`httpd`, `swarm-observer`, `ph-db`); 6 stopped (compiler-studio, sim, studio-ui, md/chem/security research).
- **Briefing alignment OK** — heap governance stack + `gap_explorer` match recent dispatch; `agent_kit_maintainer` finishing (591 finished) despite audit exit 1.
- **CP report stale** — Supabase `control_plane_reports.is_latest` @ 2026-05-25; live state in `control_plane_state` @ 00:59Z.

---

## Deliverable / findings

### Findings

| Agent / area | Symptom | Evidence path | Severity |
|--------------|---------|---------------|----------|
| Async swarm | Wave-kill batch @ 00:50Z — 20 errors/agent across 15+ agents | MCP `agent_runs` WHERE `started_at > 2026-05-31`; `li-cursor-agents/data/runs/*-1780188519*.json` | high |
| `swarm_observer` | SDK error, 0 tool calls, 125s | `li-cursor-agents/data/runs/swarm_observer-1780188930904.json` | high |
| `gui_ui_tester` | SDK error, 0 tool calls, 252s | `li-cursor-agents/data/runs/gui_ui_tester-1780188668577.json` | medium |
| Gap registry | 64 open gaps (30 competitor, 31 plan_debt, 3 missing_package) | `benchmarks/data/latest/swarm-gap-actions.json`, `lic/data/swarm-gap-registry/registry.yaml` | high |
| Goal-directed | 6/9 runners stopped; scorecard `agents_live: 0` | `lic/data/goal-directed-agents/snapshot.json` | high |
| Agent-kit audit | `org_agent_kit_audit` exit 1 (21 repos drift) | `agent-briefing.preflight_runs` | medium |
| Workspace sweep | Push rejected on `chore/studio-ux-12-harness-sota` (non-FF) | `workspace_sweeper` sweep digest @ 00:50Z | medium |
| Preflight | 8 scripts skipped (`--skip-slow`); 1 failed (agent-kit) | `agent-briefing.preflight_runs` | medium |
| CP dashboard | Latest report 6 days stale | MCP `control_plane_reports` | low |
| Benchmarks | 0 red; `matmul_blocked` yellow; 3 near tier-1 | `agent-briefing.json` → `ecosystem_audit` | low |

### Error sample classification

| Pattern | Example run | Root cause |
|---------|-------------|------------|
| SDK zero-tool error | `swarm_observer-1780188930904` | **Cursor SDK session error** — global lock + wave restart; `tools=0`, premature |
| SDK zero-tool error | `gui_ui_tester-1780188668577` | **SDK error** during proactive sweep; no harness output |
| Wave-kill batch | 20× `bug_fixer`, `plan_verifier`, … @ 00:50Z | **Supervisor restart** after workspace sweep — runs marked `error`, `completion: null` |
| Historical volume | 17,767 all-time `error` rows in CP | Mix of wave-kill, SDK errors, retries (not current degradation) |
| httpd plan | `gap-phase2-perf-wrk-soak` exit 124 | **Plan loop timeout** — long wrk soak |
| Repo conflict | `li-cursor-agents` push rejected | **Remote ahead** — needs pull/rebase before sweep push |

**Error (representative — wave-kill):**

```
Error: SDK run status: error; run_id=run-38ea1ab4-7d5b-456c-8aac-53e8b2d034f6; model=default; attempt=1; tools=0; duration_ms=125610
```

Evidence: `li-cursor-agents/data/runs/swarm_observer-1780188930904.json`

### Self-heal actions taken (programmatic observer)

| Action | Source | Result |
|--------|--------|--------|
| Observer scan | MCP `control_plane_state` @ 00:59:42Z | `retry_counts: {}`, `stopped_agents: []` |
| Gap ingest/apply | `swarm-gap-actions.json` @ 00:54Z | 64 open; 23 backlog patches (idempotent) |
| Scorecard | `ecosystem-quality-report.json` @ 00:54Z | 82.0 grade B, `unattended_safe: true` |
| Workspace sweep | Deterministic sweep @ 00:50Z | 2 repos swept; CP restarted (pid 1408555) |
| Agent-kit rollout | `agent_kit_maintainer-1780189120548` finished | 21 repos: no changes after install |
| Async dispatch | 30 runs `running` in CP (latest tick) | Normal parallel pool; no stuck >30m |

### Recommended control-plane fixes

| Fix | Repo / path |
|-----|-------------|
| Classify wave-kill / zero-tool SDK errors as `incomplete` not `error` | `li-cursor-agents/src/control-plane/finalize-run.ts` |
| Stagger async-swarm restart vs research-lane dispatch after workspace sweep | `li-cursor-agents/scripts/keep-agents-running.sh`, `src/async-swarm/` |
| Refresh Supabase `control_plane_reports` each supervisor tick | `li-cursor-agents/src/control-plane/build-report.ts` |
| Reconcile `agents_live: 0` vs active httpd/swarm-observer/ph-db runners | `lic/scripts/goal-directed-agents-snapshot.py`, `benchmarks/scripts/ecosystem-quality-grade.py` |
| Dedupe concurrent `swarm_observer` research-lane workers | `li-cursor-agents/src/lanes/research-lane.ts` |
| Nightly full preflight (no `--skip-slow`) for plan/security/ci triage | supervisor env |
| Auto `git pull --rebase` on sweep branches before push | `li-cursor-agents/src/observer/workspace-sweep.ts` (or equivalent) |

### Human-only blockers

| Blocker | Why human |
|---------|-----------|
| `std.plot` / `std.summary` implementation | Product modules — provability + API review |
| `li-line-profiler` package seed | New package placement — `package_architect` |
| 21 repos agent-kit drift (audit exit 1) | Per-repo PR review when install produces diffs |
| `verticals.toml` on benchmarks main | Blocks vertical ingest (`gap-infra-verticals-toml-missing-benchmarks-main`) |
| Master-plan / `trusted.lean` | Governance — no auto-merge |
| lic#439 local-ci failure | Product fix — `bug_fixer` / `code_implementer` queue |

### Agent deliverable checklist

- [x] Read ecosystem quality report + briefing + gap registry/actions
- [x] Queried control-plane DB (`agent_runs`, `control_plane_state`, `control_plane_reports`, `interventions_snapshots`)
- [x] Confirmed gap ingest/apply fresh (registry @ 00:59Z)
- [x] Completed `orch-r4-ui-ux-signals` orchestrator note
- [x] Sampled error runs + classified root causes
- [x] Wrote digest to `benchmarks/data/runs/`
- [ ] PR on `li-cursor-agents` for observer/finalize-run fixes (deferred — recommend after 2+ ticks of classification data)

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| [Ecosystem gap] PH-IO-7: ship `std.summary` for agent summary.json | `lic` | `master-plan-gap`, `ecosystem` |
| [Ecosystem gap] PH-IO-5: ship `std.plot` for static dashboard | `lic` | `master-plan-gap`, `ecosystem` |
| [Package seed] `li-line-profiler` — line-level profiling (WP-B) | `lic` or new `li-line-profiler` | `ecosystem`, `plan-needed` |
| fix(control-plane): classify SDK wave-kill as incomplete + dedupe swarm_observer | `li-cursor-agents` | `swarm`, `bug` |
| chore: merge `benchmarks/competitive/verticals.toml` to main | `benchmarks` | `ecosystem`, `swarm-gap` |
| fix(workspace-sweep): rebase before push on conflict branches | `li-cursor-agents` | `swarm`, `bug` |
| fix(local-ci): lic#439 — reproduce and gate | `lic` | `bug`, `ci` |

---

## Deferred

- **`orch-r3-missing-package-sweep`** — close on next ingest (orchestrator note + backlog patches are completion evidence).
- **ph-db plan_debt (9 todos)** — apply deferred (no runner backlog mapping); route via agents control plane, not systemd loops.
- **Master-plan plan_debt rows (8)** — deferred in gap apply; human/plan_verifier scope.
- **Observer prompt / `src/observer/` PR** — ship after wave-kill vs SDK-error classification metrics stabilize.
- **Full preflight without `--skip-slow`** — schedule off-peak supervisor tick.

---

## Gap orchestration summary (`swarm_coverage`)

| `gap_kind` | Open | Primary action this pass |
|------------|-----:|--------------------------|
| `missing_package` | 3 | Backlog todos pending; handoff `issue_planner` |
| `plan_debt` | 31 | 12 runner todos patched; studio-ux-16/17 linked (`orch-r4`) |
| `competitor_feature` | 30 | Vertical stubs patched to sim-md-research backlog |

**north_star_fit:** Ecosystem orchestration for proof-before-perf backlog — UI/UX signals routed to studio plan loop; no product code in `lic` (orchestration-only pass).
