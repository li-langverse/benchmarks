# Cursor Automations (not GitHub Actions cron)

Heavy recurring ops run as **[Cursor Automations](https://cursor.com/automations)** (cloud agents) so we stay inside the GitHub Actions free budget. Create each automation in the Cursor UI and paste the prompt from the matching file below.

| Automation | Trigger (suggested) | Prompt file | Repo |
|------------|---------------------|-------------|------|
| Ecosystem health | Schedule: daily or every 12h | [ecosystem-health.md](./ecosystem-health.md) | `benchmarks` (+ read `roadmap` via multi-repo env) |
| Benchmark improvement | Schedule: weekly, or after lic bench dispatch | [benchmark-improvement.md](./benchmark-improvement.md) | `lic` (primary), `benchmarks` for ingest |
| Merge queue digest | Schedule: daily | [merge-queue-digest.md](./merge-queue-digest.md) | `roadmap` |

**Do not** add `schedule:` cron to `.github/workflows/` for audits or queue refresh — use Cursor instead.

## GitHub Actions we keep (critical path)

See [docs/ecosystem/actions-budget.md](../docs/ecosystem/actions-budget.md) for minute estimates.
