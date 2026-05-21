# Issue hygiene live pass (2026-05-21)

**Agent:** `issue_hygiene` · **Preflight:** `issue-backlog-hygiene.py` + `issue-feature-triage.py`  
**Live SDK:** blocked (Cursor API 401 — key rotate needed)  
**Actions:** 7 `gh issue comment` on duplicate numerics/explorer issues

## Executive summary

- Scanned **93** open issues (4 repos); **4** duplicate clusters (**13** dup issues); **2** repos with explorer-finding bursts.
- **37** issues route to **issue_planner** (`plan-needed` / `ecosystem-gap`); **0** `plan-approved` implementer queue.
- Posted duplicate-link comments on **lic#126, #118, #114, #106** and **benchmarks#107, #105, #31** pointing at canonical keep issues (#39, #79, #47, #31).
- **Deferred:** bulk close (policy: human or explicit thread request); live LLM digest until API key valid.

## Duplicate clusters (keep → close candidates)

| Repo | Keep | Duplicates commented |
|------|------|----------------------|
| lic | #39 numerics SOTA pack | #126, #118 |
| lic | #79 horner_pure_li map | #114, #106 |
| benchmarks | #47 (cluster) | #107, #105 |
| benchmarks | #31 | #31 dup set (see JSON) |

Full machine list: `data/latest/issue-backlog-hygiene.json`

## Routing

- **issue_planner:** 37 issues need plans before implementation.
- **code_implementer:** 0 with `plan-approved` on this scan.

## Next

1. Human: close duplicates after confirming #39 / #79 are canonical numerics trackers.
2. Run **issue_planner** on top `needs_plan` (26 from triage).
3. Rotate **CURSOR_API_KEY** and re-run `LI_CONTROL_PLANE_STORE=disk ./scripts/cursor-agent-run.sh --agent issue_hygiene` for full LLM pass.
