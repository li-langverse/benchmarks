# ci_maintainer proactive digest — 2026-05-30T15:27Z

Run: `ci_maintainer-1780154600116` · Agent: `ci_maintainer` · Source: proactive

## Executive summary

- **Org CI gate:** 0 repos missing `ci.yml` on default branch — **32 OK** via `--allow-local-fallback`, **0 missing**, **2 incomplete** (no sibling clone).
- **Incomplete repos verified:** GraphQL confirms `li-local-ci` and `lic-docs` both have `ci.yml` on `main` (REST rate limit only).
- **GitHub REST exhausted:** core **0/5000**; org CI audit and `ecosystem-audit.py` `has_ci_on_main` return false positives until reset (~15:52Z).
- **ecosystem-audit.json stale:** `repos_missing_ci_main: 35`, `missing_ci_on_main` lists all org repos — **not actionable** this cycle.
- **No new CI PRs** — functionality gate satisfied; no `lic/scripts/templates/github-repo/ci.yml` rollouts.
- **research-findings** remains CI-exempt (archive repo).
- **138 open PRs / 39 failing** in ecosystem audit are CI-red on existing PRs, not missing-workflow gaps.
- **North star:** ecosystem platform hygiene — proof-before-perf CI gate on package mirrors (secure + provable pillar).

## Deliverable / findings

| Check | Result |
|-------|--------|
| `ensure-org-repo-ci.py` (REST) | exit **1** — 33 `audit_incomplete` (rate limit) |
| `ensure-org-repo-ci.py --allow-local-fallback` | OK: **32**, missing: **0**, incomplete: **2** |
| GraphQL spot-check (`li-local-ci`, `lic-docs`) | both have `ci.yml` on `main` ✓ |
| `ecosystem-audit.py` | exit **0** — `missing_ci_on_main` **stale** (35 false positives) |
| CI PRs opened this run | **0** |
| Isolated clone `ci.yml` edits | **0** |

### Error

```
ensure-org-repo-ci.py: gh: API rate limit exceeded for user ID 207167228 (HTTP 403)
gh api rate_limit: core 0/5000, reset ~2026-05-30T15:52Z
ecosystem-audit.py: missing_ci_on_main unreliable while REST core exhausted
```

Re-run both audits after REST reset before treating `missing_ci_on_main` as real gaps.

### Branch protection vs required checks (local spot-check, unchanged)

| Repo | Required check | Workflow job | Match |
|------|----------------|--------------|-------|
| `lic` | `version`, `build-and-test` | same | ✓ |
| `lip` | `bootstrap` | `bootstrap` | ✓ |
| Package mirrors (default) | `check` | `check` | ✓ (rulesets TBD) |

## Recommended issues/PRs

None required for missing CI.

| Title | Repo | Labels |
|-------|------|--------|
| Re-run org-repo-ci-audit after GitHub REST rate limit reset | benchmarks | `ecosystem-ci`, `agent:ci_maintainer` |
| fix(audit): GraphQL fallback for has_ci_on_main when REST rate-limited | benchmarks | `ecosystem-ci`, `agent:ci_maintainer` |
| Apply org branch protection rulesets (required check: `check`) | org settings / roadmap | `ecosystem-governance` |
| Remove `continue-on-error` from lic windows CI matrix job | lic | `ecosystem-ci`, `ci-hygiene` |

## Deferred

- **Org-repo-ci + ecosystem-audit re-audit** — wait for REST core reset (~15:52Z).
- **ecosystem-audit GraphQL fallback** — reduce false `missing_ci_on_main` during rate limits.
- **Branch protection rollout** for package mirrors — human `roadmap/scripts/apply-org-branch-protection.sh`.
- **lic windows `continue-on-error`** — separate hygiene pass.
- **Per-repo CI red on open PRs** — `bug_fixer` / `pr_alignment` scope.
