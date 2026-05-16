# Cursor agent architecture (li-langverse)

**Rule:** Work that needs **judgment, web research, or cross-repo reasoning** runs as **Cursor Agents** (cloud automations or local Agent chat). **GitHub Actions** run **CI and Pages only**.

The stack is:

| Layer | What | When |
|-------|------|------|
| **1. Cursor Automations** | Scheduled cloud agents at [cursor.com/automations](https://cursor.com/automations) | Production schedules |
| **2. [li-cursor-agents](https://github.com/li-langverse/li-cursor-agents)** | Local `@cursor/sdk` + **mock backend for CI** | Dev + automated agent tests |
| **3. Local Agent (IDE)** | Same prompts + `/agent-briefing` | Ad-hoc |
| **4. Preflight scripts** (benchmarks) | `agent-briefing.py` → JSON | **Input only** — no LLM |
| **5. GitHub Actions** | `ci.yml`, `pages.yml` | Compile/test/publish only — **never** call real SDK in CI |

### Local SDK runner (li-cursor-agents)

```bash
git clone https://github.com/li-langverse/li-cursor-agents ../li-cursor-agents
cd benchmarks
./scripts/cursor-agent-run.sh --agent ecosystem_explorer --mock   # CI-safe
export CURSOR_API_KEY=... 
./scripts/cursor-agent-run.sh --agent pr_review                   # real SDK
```

`CURSOR_MOCK=1` or `CI=true` without API key → **mock backend** (deterministic markdown, no LLM).

Preflight does **not** replace explorer/review/research agents — it **feeds** them.

---

## Agent catalog (Cursor Automations)

Create one automation per row; paste the linked prompt file.

| Agent | Schedule | Prompt | Skill(s) | Needs web |
|-------|----------|--------|----------|-----------|
| **Orchestrator** | Weekly | [agent-orchestrator.md](../../.cursor/automations/agent-orchestrator.md) | — | Optional |
| **Ecosystem explorer** | Biweekly | [ecosystem-explorer.md](../../.cursor/automations/ecosystem-explorer.md) | `explore-li-ecosystem` | **Yes** (Reddit, HPC, papers) |
| **Implementation gaps** | Weekly | [implementation-gaps-agent.md](../../.cursor/automations/implementation-gaps-agent.md) | `explore-li-ecosystem`, `audit-plan-completion` | **Yes** |
| **Plan completion** | Weekly | [plan-completion-audit.md](../../.cursor/automations/plan-completion-audit.md) | `audit-plan-completion` | No |
| **Issue planner** | 2×/week | [issue-feature-planner.md](../../.cursor/automations/issue-feature-planner.md) | `plan-feature-from-issue` | Optional |
| **PR alignment** | Daily | [pr-alignment-agent.md](../../.cursor/automations/pr-alignment-agent.md) | `review-pr-alignment` | No |
| **PR review** | On open PR / daily | [pr-review-agent.md](../../.cursor/automations/pr-review-agent.md) | `merge-approved-pr`, `review-pr-alignment` | Optional |
| **Numerics research** | Weekly + `numerics-research` issues | [numerics-research-cycle.md](../../.cursor/automations/numerics-research-cycle.md) | `research-li-numerics`, `numerics-autoresearch` | **Yes** |
| **Ecosystem health** | Daily | [ecosystem-health.md](../../.cursor/automations/ecosystem-health.md) | `ecosystem-first` | No |
| **Merge queue / auto-merge** | 12h | [merge-queue-digest.md](../../.cursor/automations/merge-queue-digest.md) + [pr-auto-merge.md](../../.cursor/automations/pr-auto-merge.md) | `plan-merge-queue`, `merge-approved-pr` | No |
| Failed benchmarks | Weekly | [failed-benchmarks-maintainer.md](../../.cursor/automations/failed-benchmarks-maintainer.md) | `research-li-numerics` | Optional |

---

## Local preflight (before any agent run)

```bash
cd benchmarks
./scripts/agent-preflight.sh
# → data/latest/agent-briefing.json (aggregates triage, plans, explorer, PR queue)
```

Then open **Cursor Agent** (or start the matching Automation) and say:

> Read `data/latest/agent-briefing.json` and run the **PR alignment** agent tasks.

Slash: `/agent-briefing`, `/review-pr`, `/pr-alignment`, `/explore-ecosystem`, `/numerics-research`

---

## What must **not** be an Action cron

| Anti-pattern | Use instead |
|--------------|-------------|
| Scheduled ecosystem audit | Cursor **ecosystem-health** + **explorer** |
| Scheduled numerics SOTA | Cursor **numerics-research-cycle** + web search |
| Scheduled PR review comments | Cursor **pr-review-agent** |
| Scheduled plan gap scan | Cursor **plan-completion-audit** + **implementation-gaps-agent** |
| `workflow_dispatch` for thinking | OK only to **refresh JSON artifacts** for agents |

`workflow_dispatch` workflows (`plan-completion-audit.yml`, `ecosystem-explorer.yml`, `org-repo-ci-audit.yml`) are **optional artifact publishers** — run them if you want CI-stored JSON; agents still do interpretation.

---

## Agent run contract

Every automation prompt follows:

1. **Preflight** — run scripts listed in prompt (or read latest `data/latest/*.json`)
2. **Reason** — web search / read plans / diff PRs (agent brain)
3. **Act** — issues, comments, draft PRs, labels (`plan-needed`, `explorer-finding`, `merge-approved` only when gates pass)
4. **Do not** — self-merge without `merge-approved` + gate; no `schedule:` in new workflows

---

## Multi-repo workspace

Cloud automations should use a workspace with **benchmarks + lic + roadmap** siblings so `LIC_ROOT=../lic` and preflight scripts resolve.

---

## Related

- [agent-automations.md](./agent-automations.md) — setup checklist
- [actions-budget.md](./actions-budget.md) — CI-only Actions policy
- [tooling-catalog.md](./tooling-catalog.md) — script index
