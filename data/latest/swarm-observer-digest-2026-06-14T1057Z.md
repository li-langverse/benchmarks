# Swarm observer digest — Performance (`733bd20d`)

**Generated:** 2026-06-14T10:57Z · **Run:** `1781433380358` · **Goal:** `swarm_coverage` @ performance

## Summary

- Grade **B (81.1)**, `unattended_safe: true`; orchestration degraded, execution clean
- **62** open gaps; PyYAML blocks live ingest (last apply 2026-06-11)
- **0 red / 2 yellow / 5 near-threshold** numerics; perf agents not heap-dispatched
- Briefing heap: `docs_maintainer` + `ci_maintainer`; scorecard adds `gap_explorer` + `plan_verifier`
- CP `state.json` / `latest-report.json` absent; GH 403 → false CI missing signal

**Report:** `/app/data/runs/swarm_observer-1781433380358.md`  
**Orchestrator note:** `/workspace/lic/docs/ecosystem/orchestrator-notes/2026-06-14-orch-performance-733bd20d.md`  
**Whitepaper:** `/workspace/lic/docs/research/swarm_coverage/performance/2026-06-14-whitepaper-733bd20d.md`
