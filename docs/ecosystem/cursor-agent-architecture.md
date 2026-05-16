# Cursor agent architecture (li-langverse)

**Rule:** Work that needs **judgment, web research, or cross-repo reasoning** runs as **Cursor Agents** (cloud automations or local Agent chat). **GitHub Actions** run **CI and Pages only**.

There is no separate “agent SDK” in this org — the stack is:

| Layer | What | When |
|-------|------|------|
| **1. Cursor Automations** | Scheduled/triggered cloud agents at [cursor.com/automations](https://cursor.com/automations) | Explorer, numerics SOTA, PR review, plan gaps, merge queue |
| **2. Local Agent (IDE / CLI)** | Same prompts + skills; you or `cursor agent` with repo context | Ad-hoc, debugging, single PR |
| **3. Preflight scripts** | Deterministic JSON under `data/latest/` | **Input** to agents — not a substitute for agents |
| **4. GitHub Actions** | `ci.yml`, `pages.yml`, label-triggered merge gate | Compile/test/publish only |

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
