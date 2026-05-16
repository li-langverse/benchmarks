# Cursor Automations (not GitHub Actions cron)

Heavy recurring ops run as **[Cursor Automations](https://cursor.com/automations)** (cloud agents) so we stay inside the GitHub Actions free budget. Create each automation in the Cursor UI and paste the prompt from the matching file below.

| Automation | Trigger (suggested) | Prompt file | Primary repo |
|------------|---------------------|-------------|--------------|
| **Issue feature planner** | 2×/week per repo (or org sweep) | [issue-feature-planner.md](./issue-feature-planner.md) + [repos/](./repos/) | all · skills: `plan-feature-from-issue` |
| **Plan completion audit** | Weekly | [plan-completion-audit.md](./plan-completion-audit.md) | `benchmarks` + `lic` · skill: `audit-plan-completion` |
| **Benchmark visuals** | Weekly or after lic bench / manual | [benchmark-visual-validation.md](./benchmark-visual-validation.md) | `lic` + `benchmarks` |
| **Failed benchmarks** | Schedule: weekly, or webhook after lic bench | [failed-benchmarks-maintainer.md](./failed-benchmarks-maintainer.md) | `lic` (+ `benchmarks` ingest) |
| **Numerics research** | Weekly or `numerics-research` issues | [numerics-research-cycle.md](./numerics-research-cycle.md) | `lic` · skills: `research-li-numerics`, `numerics-autoresearch` |
| **Ecosystem explorer** | Weekly / biweekly | [ecosystem-explorer.md](./ecosystem-explorer.md) | `benchmarks` + `lic` · skill: `explore-li-ecosystem` · Reddit/HPC web search |
| Ecosystem health | Schedule: daily or every 12h | [ecosystem-health.md](./ecosystem-health.md) | `benchmarks` (+ `roadmap` read) |
| Benchmark improvement | Same as failed benchmarks (alias) | [benchmark-improvement.md](./benchmark-improvement.md) | `lic` |
| Merge queue digest | Schedule: daily | [merge-queue-digest.md](./merge-queue-digest.md) | `roadmap` |
| **PR auto-merge** | 12h or after review | [pr-auto-merge.md](./pr-auto-merge.md) | plan: **`plan-merge-queue`** · review: `merge-approved-pr` |

**Philosophy:** [ecosystem-first.md](../docs/ecosystem/ecosystem-first.md) · catalog: [tooling-catalog.md](../docs/ecosystem/tooling-catalog.md) · gaps → `file-ecosystem-gap-issue.py`

**Setup guide:** [docs/ecosystem/agent-automations.md](../docs/ecosystem/agent-automations.md)

**Dashboard:** https://li-langverse.github.io/benchmarks/ — local report: `./scripts/benchmark-failures-report.sh`

**Do not** add `schedule:` cron to `.github/workflows/` for audits or queue refresh — use Cursor instead.

## GitHub Actions we keep (critical path)

See [docs/ecosystem/actions-budget.md](../docs/ecosystem/actions-budget.md) for minute estimates.
