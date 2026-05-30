# ci_maintainer digest — 2026-05-30

**Run:** `ci_maintainer-1780133512165` (proactive)  
**North star fit:** Ecosystem platform gate — org repos must expose `ci.yml` on `main` before Dependabot and merge-queue automation (proof → easy → fast; PH-8p CI throughput).

## Executive summary

- Refreshed `org-repo-ci-audit.json` via `ensure-org-repo-ci.py` (REST exhausted; `--allow-local-fallback` → **0 missing**, 2 incomplete without sibling clones).
- GraphQL batch audit (35 org repos): **33 have `ci.yml` on `main`**; only **`lic-docs`** lacks it; **`research-findings`** is exempt.
- `ecosystem-audit.json` reported **35 missing CI** — false positive from GitHub REST rate limit (`5000/5000`); patched `has_ci_on_main` to GraphQL-fallback on 403.
- Closed duplicate **lic-docs#3**; **lic-docs#1** remains open with green `check`, labels `ecosystem-ci`, `merge-approved` — human merge only.
- No new CI PRs opened this run (no repos missing `ci.yml` besides in-flight lic-docs).
- **Error (non-blocking):** REST `gh api` rate-limited for full org sweep; GraphQL quota remained available.

## Deliverable / findings

| Signal | Result |
|--------|--------|
| `org-repo-ci-audit.json` | OK: 32 (local fallback), missing: 0, incomplete: `li-local-ci`, `lic-docs` (no local `.github/workflows`) |
| GraphQL `ci.yml` on `main` | 33/35 present; missing: `lic-docs` only |
| `ecosystem-audit` `missing_ci_on_main` | Stale/false until rate-limit fix re-run |
| Branch protection vs `check` job | `lic-docs`: no rulesets; PR CI job `check` matches template |
| `li-local-ci` | `ci.yml` already on **remote** `main`; sibling clone outdated (no local workflows dir) |

**Actions taken**

1. `python3 scripts/ensure-org-repo-ci.py` (+ `--allow-local-fallback`)
2. GraphQL verification of all non-archived org repos
3. Closed [lic-docs#3](https://github.com/li-langverse/lic-docs/pull/3) as duplicate of [#1](https://github.com/li-langverse/lic-docs/pull/1)
4. `ecosystem-audit.py`: GraphQL fallback when REST hits rate limit

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| Merge `chore(ci): add org-required ci.yml for lic-docs` | `lic-docs` | `ecosystem-ci`, `merge-approved` — [PR #1](https://github.com/li-langverse/lic-docs/pull/1) |
| Re-run `ecosystem-audit.py` after REST quota reset | `benchmarks` | — (validates rate-limit fix) |
| Optional: sync local `li-local-ci` clone (`git pull`) | dev env | — |

## Deferred

- **Self-merge** `lic-docs#1` — governance: human review despite `merge-approved`.
- **research-findings** — exempt from org `ci.yml` policy (`IGNORE_REPOS` / audit exempt).
- **lidb** — gated non-main default (WP-H0) until default branch is `main`.
- **Full REST re-audit** — retry `ensure-org-repo-ci.py` without `--allow-local-fallback` when `gh api rate_limit` core resets (~1h).
