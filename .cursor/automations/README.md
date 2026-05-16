# Cursor Automations (agents — not GitHub Actions cron)

**Architecture:** [cursor-agent-architecture.md](../docs/ecosystem/cursor-agent-architecture.md)  
**Preflight:** `./scripts/agent-preflight.sh` → `data/latest/agent-briefing.json`

Heavy **reasoning** work runs here. **GitHub Actions** = CI + Pages only ([actions-budget.md](../docs/ecosystem/actions-budget.md)).

## Agent roster (create at cursor.com/automations)

| Agent | Prompt | Web? |
|-------|--------|------|
| **Orchestrator** | [agent-orchestrator.md](./agent-orchestrator.md) | Optional |
| **Ecosystem explorer** | [ecosystem-explorer.md](./ecosystem-explorer.md) | **Yes** |
| **Implementation gaps** | [implementation-gaps-agent.md](./implementation-gaps-agent.md) | **Yes** |
| **Plan completion** | [plan-completion-audit.md](./plan-completion-audit.md) | No |
| **Issue planner** | [issue-feature-planner.md](./issue-feature-planner.md) | Optional |
| **PR alignment** | [pr-alignment-agent.md](./pr-alignment-agent.md) | No |
| **PR review** | [pr-review-agent.md](./pr-review-agent.md) | Optional |
| **Numerics research** | [numerics-research-cycle.md](./numerics-research-cycle.md) | **Yes** |
| Ecosystem health | [ecosystem-health.md](./ecosystem-health.md) | No |
| Merge queue / auto-merge | [merge-queue-digest.md](./merge-queue-digest.md), [pr-auto-merge.md](./pr-auto-merge.md) | No |
| Failed benchmarks | [failed-benchmarks-maintainer.md](./failed-benchmarks-maintainer.md) | Optional |

Per-repo scope: [repos/](./repos/) — append to planner/health automations.

## Slash commands (local Agent)

| Command | Agent |
|---------|--------|
| `/agent-briefing` | Preflight + route |
| `/explore-ecosystem` | Explorer |
| `/audit-plans` | Plan completion |
| `/review-pr` | PR review |
| `/pr-alignment` | PR alignment |
| `/numerics-research` | Numerics |
| `/merge-queue` | Merge plan |

## Scripts = preflight only

| Script | Feeds agent |
|--------|-------------|
| `agent-briefing.py` | All agents |
| `ecosystem-explorer.py` | Explorer, implementation-gaps |
| `plan-completion-audit.py` | Plan, implementation-gaps |
| `run-pr-program.py` | PR alignment, PR review, merge |

**Do not** add `schedule:` cron to `.github/workflows/` for these concerns.
