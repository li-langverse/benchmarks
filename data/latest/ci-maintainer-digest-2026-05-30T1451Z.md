# ci_maintainer proactive digest — 2026-05-30T14:51Z

Run: `ci_maintainer-1780152649781` · Agent: `ci_maintainer` · Source: proactive

## Executive summary

- **Org CI gate:** 0 repos missing `ci.yml` on default branch (`ensure-org-repo-ci.py` exit 0).
- **34 org repos OK** — all non-exempt repos have `ci.yml` on `main` (GitHub API audit, no local fallback).
- **ecosystem-audit.json** refreshed and aligned: `repos_missing_ci_main: 0`, `missing_ci_on_main: []`.
- **Preflight rate-limit noise cleared** — prior audit at 14:32Z hit HTTP 403 on all repos; re-run succeeded.
- **No new CI PRs** opened — functionality gate satisfied; no template rollouts required.
- **research-findings** remains CI-exempt (archive repo); only exempt repo in org sweep.
- **Branch protection rulesets** not yet org-wide — workflow job ids match `org-branch-protection.json` locally.
- **34 failing PRs** in ecosystem audit are CI-red on existing PRs, not missing-workflow gaps.

## Deliverable / findings

| Check | Result |
|-------|--------|
| `ensure-org-repo-ci.py` | exit **0** — OK: **34**, missing: **0**, gated: **0**, incomplete: **0** |
| `ecosystem-audit.py` | refreshed `ecosystem-audit.json` — `repos_missing_ci_main`: **0** |
| CI PRs opened this run | **0** |
| Isolated clone edits | **0** (no missing repos) |
| `continue-on-error` on OS matrix | **lic** `build-and-test-windows` — pre-existing, not introduced |

### Branch protection vs required checks (local spot-check)

| Repo | Required check (ruleset config) | Workflow job | Match |
|------|--------------------------------|--------------|-------|
| `lic` | `version`, `build-and-test` | `version`, `build-and-test` | ✓ |
| `lip` | `bootstrap` | `bootstrap` | ✓ |
| `lit` | `test` | `test` | ✓ |
| `benchmarks` | `ingest-smoke`, `dashboard-build` | `ingest-smoke`, `dashboard-build` | ✓ |
| `roadmap` | `verify-kit` | `verify-kit` | ✓ |
| Package mirrors (default) | `check` | `check` | ✓ (rulesets TBD) |

## Recommended issues/PRs

None required for missing CI. Optional follow-ups:

| Title | Repo | Labels |
|-------|------|--------|
| Apply org branch protection rulesets (required check: `check`) | org settings / roadmap | `ecosystem-governance` |
| Remove `continue-on-error` from lic windows CI matrix job | lic | `ecosystem-ci`, `ci-hygiene` |
| Fix failing agent-kit sync PR CI (34 red PRs in ecosystem audit) | package mirrors | `ecosystem-ci`, `bug` |

## Deferred

- **Branch protection rollout** for package mirrors — human `roadmap/scripts/apply-org-branch-protection.sh`.
- **lic windows `continue-on-error`** — separate hygiene pass (out of scope for add-CI mandate).
- **Per-repo CI red on open PRs** — bug_fixer / pr_alignment scope, not ci_maintainer add-workflow mandate.
