# CI maintainer digest — 2026-05-30T08:41Z

**Agent:** `ci_maintainer` · **Run:** `ci_maintainer-1780130208258` · **Source:** proactive · **North star fit:** platform / **easy** (docs handbook CI gate; PH-8p CI throughput hygiene)

## Executive summary

- Refreshed **`org-repo-ci-audit.json`** via `python3 scripts/ensure-org-repo-ci.py`: **33 OK**, **1 missing** (`lic-docs`), **0 gated**, **0 incomplete**.
- Sole gap: **`lic-docs`** lacks `.github/workflows/ci.yml` on `main` (has `docs.yml` only); suggested required check name **`check`**.
- **Existing PR covers the gap:** [lic-docs#1](https://github.com/li-langverse/lic-docs/pull/1) (prior run `ci_maintainer-1780115437465`) — CI **green**, labels `ecosystem-ci`, `li-swarm`, `agent:ci_maintainer`, `merge-approved`; **no duplicate PR opened this run**.
- Adapted workflow: docs smoke via `scripts/build-docs.sh` (not lic package template verbatim); job name **`check`** matches org policy.
- **`main` branch protection** on `lic-docs`: **not configured** (HTTP 404) — enable after merge with required status check **`check`**.
- **`lidb`**: non-`main` default — **gated** (WP-H0); do not require `ci.yml` on default until default branch is `main`.
- **`research-findings`**: **exempt** in org CI audit; `ecosystem-audit.json` `missing_ci_on_main` lists it due to coarse “any workflow” heuristic — not actionable for `ci_maintainer`.
- **Ecosystem metrics:** `repos_missing_ci_main: 1` (refreshed audit aligns with org-repo-ci-audit, not stale briefing `0`).

## Deliverable / findings

### Preflight (`org-repo-ci-audit.json`, `ecosystem-audit.json`)

| Audit | Generated | Missing CI on main |
|-------|-----------|-------------------|
| `org-repo-ci-audit.json` | 2026-05-30T08:41Z | `lic-docs` (needs `ci.yml`) |
| `ecosystem-audit.json` | 2026-05-30T08:38Z | `research-findings` (exempt); metrics count **1** |

### lic-docs — org CI rollout (verified, not re-opened)

| Field | Value |
|-------|-------|
| PR | [#1](https://github.com/li-langverse/lic-docs/pull/1) |
| Branch | `chore/agent-ci_maintainer-1780115437465-ci` |
| Required check | `check` ✓ (pass on PR) |
| Workflow | `.github/workflows/ci.yml` — MkDocs smoke, preserves `docs.yml` Pages deploy |
| Branch protection | **None** on `main` — human should add `check` after merge |
| Self-merge | **Not performed** (governance) |

### Branch protection vs required checks

Org policy (`docs/ecosystem/repo-ci-required.md`): every non-exempt repo must expose a **`check`** job in `ci.yml`. For repos with protection enabled, the required context must match that job name. **`lic-docs`** has no protection yet; first merge of PR #1 unblocks enabling protection with context **`check`**.

### Isolated workspace

No new isolated clone edits this run — deliverable already on branch from run `ci_maintainer-1780115437465`. Re-running `prepare` → `commit-pr` would duplicate PR #1.

## Recommended issues/PRs

| Priority | Repo | Title / action | Labels |
|----------|------|----------------|--------|
| P0 | lic-docs | **Merge** [PR #1](https://github.com/li-langverse/lic-docs/pull/1) — org `ci.yml` for docs smoke gate | `ecosystem-ci`, `merge-approved` |
| P1 | lic-docs | Enable `main` branch protection — required status check **`check`** | `platform`, `ci` |
| P2 | lidb | WP-H0: migrate default branch to `main`, then run `ci_maintainer` for `ci.yml` gate | `platform`, `governance` |
| P2 | benchmarks | Align `ecosystem-audit.py` `has_ci_on_main` with org policy (`ci.yml` required, honor exempt set) | `ci`, `tech-debt` |

## Deferred

- **`lidb` WP-H0** — non-`main` default; gated in `org-repo-ci-audit.json`.
- **`research-findings`** — exempt archive-style repo; no `ci.yml` required.
- **Self-merge** of lic-docs PR — human review required despite `merge-approved`.
- **New PR branches** for lic-docs — superseded by open PR #1.
- **GitHub Actions cron** — not added (per agent rules).
