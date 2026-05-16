# Agent automations & skills (li-langverse)

**Policy:** Recurring monitoring uses **[Cursor Automations](https://cursor.com/automations)** — not GitHub Actions `cron:` — see [actions-budget.md](./actions-budget.md).

Prompt files live in **`.cursor/automations/`**. Shared skills in **`.cursor/skills/`**.

After changing shared templates, bump **`roadmap`** `agent-kit/manifest.toml` and run `./scripts/sync-agent-kit.sh` in each code repo.

---

## Automations catalog

| Automation | Schedule | Prompt | Purpose |
|------------|----------|--------|---------|
| **Issue feature planner** | 2×/week | [issue-feature-planner.md](../../.cursor/automations/issue-feature-planner.md) | New feature issues → vision-aligned plan (no code until `plan-approved`) |
| **Plan completion audit** | Weekly | [plan-completion-audit.md](../../.cursor/automations/plan-completion-audit.md) | Unchecked PH phases, plan boxes, G-* gaps, catalog drift |
| Ecosystem health | Daily / 12h | [ecosystem-health.md](../../.cursor/automations/ecosystem-health.md) | CI, docs, benchmark reds |
| Failed benchmarks | Weekly | [failed-benchmarks-maintainer.md](../../.cursor/automations/failed-benchmarks-maintainer.md) | Dashboard regression fixes in lic |
| Benchmark visuals | Weekly | [benchmark-visual-validation.md](../../.cursor/automations/benchmark-visual-validation.md) | PNG/GIF validation |
| Merge queue digest | Daily | [merge-queue-digest.md](../../.cursor/automations/merge-queue-digest.md) | Ready PRs for humans |

### Per-repo planner scope

When creating **one automation per repo**, paste the parent prompt plus:

- [repos/lic.md](../../.cursor/automations/repos/lic.md)
- [repos/benchmarks.md](../../.cursor/automations/repos/benchmarks.md)
- [repos/lip.md](../../.cursor/automations/repos/lip.md)
- [repos/lit.md](../../.cursor/automations/repos/lit.md)
- [repos/lis.md](../../.cursor/automations/repos/lis.md)
- [repos/roadmap.md](../../.cursor/automations/repos/roadmap.md)

---

## Skills

| Skill | Use when |
|-------|----------|
| [plan-feature-from-issue](../../.cursor/skills/plan-feature-from-issue/SKILL.md) | Drafting a plan from a GitHub issue |
| [audit-plan-completion](../../.cursor/skills/audit-plan-completion/SKILL.md) | Interpreting plan audit JSON |
| [li-ecosystem-discipline](../../.cursor/skills/li-ecosystem-discipline/SKILL.md) | Any cross-repo PR |
| [write-li-release-notes](../../.cursor/skills/write-li-release-notes/SKILL.md) | Before merge |
| [research-li-numerics](../../.cursor/skills/research-li-numerics/SKILL.md) | Physics/numerics kernels |

---

## Scripts (run locally or in automations)

```bash
# Feature issues needing plans
python3 scripts/issue-feature-triage.py
# → data/latest/issue-feature-triage.json

# Incomplete plans / implementation drift
export LIC_ROOT=../lic
python3 scripts/plan-completion-audit.py
# → data/latest/plan-completion-audit.json

# Org health + benchmarks
python3 scripts/ecosystem-audit.py
# → data/latest/ecosystem-audit.json
```

---

## GitHub issue labels (recommended org-wide)

| Label | Meaning |
|-------|---------|
| `plan-needed` | Feature accepted; planner automation should draft plan |
| `plan-approved` | Plan linked; implementation agents may code |
| `feature` / `enhancement` | Eligible for feature planner |

---

## What is already automated (no Cursor UI required)

| Mechanism | What it does |
|-----------|----------------|
| **GitHub Actions** `issue-feature-planning.yml` | On new/labeled feature issues → posts planning checklist comment |
| **GitHub Actions** `plan-completion-audit.yml` | `workflow_dispatch` → runs audit scripts, uploads JSON artifacts |
| **Org labels** | `plan-needed`, `plan-approved`, `feature` (via `scripts/setup-org-labels.sh`) |
| **Slash commands** | `/plan-feature`, `/audit-plans` in `.cursor/commands/` |
| **agent-kit 1.3.0** | Skills + automation prompts synced via `roadmap` → `install-agent-kit.sh` |

## Cursor UI setup (optional — for full agent runs on a schedule)

1. [cursor.com/automations](https://cursor.com/automations) → **New automation**
2. **Trigger:** Schedule (or "Issues opened" when available for your org)
3. **Repository:** `li-langverse/<repo>` or multi-repo cloud workspace
4. **Instructions:** paste full markdown from the prompt file
5. **Model:** default; enable PR creation only for `plan-approved` implementation runs

If you skip Cursor UI, use **Actions → Run workflow → Plan completion audit** weekly and rely on issue comments for new features.

---

## Propagate to agent-kit (roadmap)

Add to `roadmap/agent-kit/overlays/benchmarks/` (and other repos):

- `skills/plan-feature-from-issue/`
- `skills/audit-plan-completion/`
- `automations/issue-feature-planner.md`
- `automations/plan-completion-audit.md`

Bump `agent-kit/manifest.toml` version; notify repos via sync script.
