# GitHub Actions budget (benchmarks repo)

**Policy:** Use Actions for **CI gates** and **publishing** only. Recurring audits, merge-queue refresh, and bench improvement sweeps use **[Cursor Automations](../../.cursor/automations/README.md)**.

## Free tier (reference)

| Repo visibility | Actions minutes |
|-----------------|-----------------|
| **Public** | Unlimited (standard GitHub fair use) |
| **Private** (Free plan) | **2,000 min/month** per account |

`li-langverse/*` repos are public → Actions minutes are typically **not billed**, but we still avoid cron noise, duplicate work, and org-wide runner load.

## Workflows in this repo

| Workflow | Trigger | ~Minutes/run | Est. monthly (assumption) |
|----------|---------|--------------|---------------------------|
| **Benchmarks CI** | PR + push `main` | 1–2 (2 jobs) | ~30 PRs → **30–60 min** |
| **Deploy dashboard** | push `main` (paths) | 2–3 | ~10 data publishes → **20–30 min** |
| **Ingest benchmarks** | `repository_dispatch` / manual | 1–2 | ~20 lic bench events → **20–40 min** |
| ~~Ecosystem audit cron~~ | **Removed** — use Cursor | — | — |

**Rough total (event-driven only):** ~70–130 min/month if private; **$0 marginal** if public.

### Avoid (was planned, do not merge on cron)

| Pattern | Why |
|---------|-----|
| `cron: */15` queue refresh | 96×/day × 1 min ≈ **2,880 min/month** on one workflow alone |
| `cron: 0 */6` ecosystem audit | 4×/day × 1 min ≈ **120 min/month** + duplicate of Cursor agent |

## Critical path (keep in Actions)

1. **PR CI** — `ci.yml`: ingest smoke + dashboard build (must pass before merge).
2. **Pages** — `pages.yml`: publish https://li-langverse.github.io/benchmarks/
3. **Ingest** — `ingest.yml`: update `data/latest/summary.json` when lic finishes benches (dispatch only).

## Optional manual Actions

`workflow_dispatch` on ingest is fine for ad-hoc refresh without burning cron budget.

## Roadmap repo (sibling)

[roadmap PR #2](https://github.com/li-langverse/roadmap/pull/2) includes `refresh-development-overview.yml` on a **15-minute cron** — **drop the schedule** before merge; use Cursor [merge-queue-digest.md](../../.cursor/automations/merge-queue-digest.md) instead. Keep `pages.yml` on push to `main` only.
