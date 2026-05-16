# Agent automations & skills (li-langverse)

**Architecture:** [cursor-agent-architecture.md](./cursor-agent-architecture.md) — **agents first**, scripts preflight, Actions CI-only.

**Policy:** Recurring **intelligence** uses **[Cursor Automations](https://cursor.com/automations)** — not GitHub Actions `cron:` — see [actions-budget.md](./actions-budget.md).

Prompt files: **`.cursor/automations/`** · Skills: **`.cursor/skills/`** · Local entry: **`./scripts/agent-preflight.sh`**

---

## Three layers

| Layer | Examples | Role |
|-------|----------|------|
| **Cursor Agents** | explorer, PR review, numerics SOTA, plan gaps | Web search, judgment, issues/PRs |
| **Preflight scripts** | `agent-briefing.py`, `ecosystem-explorer.py`, `pr-merge-queue-plan.py` | JSON for agents |
| **GitHub Actions** | `ci.yml`, `pages.yml`, `pr-auto-merge.yml` | Build, test, publish, gated merge |

There is no separate org “Cursor SDK” — use **Automations UI** + **local Agent** with the same prompts.

---

## Quick start

```bash
cd benchmarks
./scripts/agent-preflight.sh
cat data/latest/agent-briefing.json   # → recommended_agents
```

1. Open [cursor.com/automations](https://cursor.com/automations) → **New automation**
2. Paste prompt from `recommended_agents` (e.g. `ecosystem-explorer.md`)
3. Enable **web search** for explorer, numerics, implementation-gaps
4. Multi-repo workspace: **benchmarks**, **lic**, **roadmap**

---

## Agent catalog

| Agent | Schedule | Prompt | Skills |
|-------|----------|--------|--------|
| Orchestrator | Weekly | [agent-orchestrator.md](../../.cursor/automations/agent-orchestrator.md) | — |
| **Ecosystem explorer** | Biweekly | [ecosystem-explorer.md](../../.cursor/automations/ecosystem-explorer.md) | `explore-li-ecosystem` |
| **Implementation gaps** | Weekly | [implementation-gaps-agent.md](../../.cursor/automations/implementation-gaps-agent.md) | `explore-li-ecosystem`, `audit-plan-completion` |
| Plan completion | Weekly | [plan-completion-audit.md](../../.cursor/automations/plan-completion-audit.md) | `audit-plan-completion` |
| Issue planner | 2×/week | [issue-feature-planner.md](../../.cursor/automations/issue-feature-planner.md) | `plan-feature-from-issue` |
| **PR alignment** | Daily | [pr-alignment-agent.md](../../.cursor/automations/pr-alignment-agent.md) | `review-pr-alignment` |
| **PR review** | Daily / on PR | [pr-review-agent.md](../../.cursor/automations/pr-review-agent.md) | `merge-approved-pr`, `review-pr-alignment` |
| **Numerics research** | Weekly | [numerics-research-cycle.md](../../.cursor/automations/numerics-research-cycle.md) | `research-li-numerics`, `numerics-autoresearch` |
| Ecosystem health | Daily | [ecosystem-health.md](../../.cursor/automations/ecosystem-health.md) | `ecosystem-first` |
| Merge / auto-merge | 12h | [merge-queue-digest.md](../../.cursor/automations/merge-queue-digest.md), [pr-auto-merge.md](../../.cursor/automations/pr-auto-merge.md) | `plan-merge-queue`, `merge-approved-pr` |

### Per-repo overlays

[repos/lic.md](../../.cursor/automations/repos/lic.md) · [benchmarks](../../.cursor/automations/repos/benchmarks.md) · [lip](../../.cursor/automations/repos/lip.md) · [lit](../../.cursor/automations/repos/lit.md) · [lis](../../.cursor/automations/repos/lis.md) · [roadmap](../../.cursor/automations/repos/roadmap.md)

---

## Preflight scripts (not agents)

```bash
./scripts/agent-preflight.sh          # all-in-one briefing
python3 scripts/ecosystem-explorer.py # explorer input
python3 scripts/plan-completion-audit.py
python3 scripts/run-pr-program.py     # PR alignment / review
python3 scripts/pr-merge-gate.py --repo lic --pr N --json
```

---

## GitHub Actions (limited)

| Keep | Purpose |
|------|---------|
| `ci.yml` | PR CI |
| `pages.yml` | Dashboard |
| `pr-auto-merge.yml` | Merge when `merge-approved` + gate |
| `workflow_dispatch` audits | Optional JSON artifacts only |

**Do not** cron: explorer, plan audit, PR review, numerics research.

---

## Labels

| Label | Agent |
|-------|--------|
| `plan-needed` | Issue planner |
| `plan-approved` | Implementation agents |
| `merge-approved` | PR review → auto-merge |
| `explorer-finding` | Explorer / implementation-gaps |
| `ecosystem-gap` | Planner + catalog |
| `numerics-research` | Numerics agent |

`scripts/setup-org-labels.sh`

---

## Propagate (roadmap agent-kit)

Bump `agent-kit/manifest.toml`; sync `cursor-agent-architecture.md`, `li-agent-automations.mdc`, new automations + skills.
