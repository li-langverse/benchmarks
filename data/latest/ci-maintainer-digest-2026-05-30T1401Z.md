# ci_maintainer proactive digest — 2026-05-30T14:01Z

Run: `ci_maintainer-1780149652563` · Agent: `ci_maintainer` · Source: proactive

## Executive summary

- **Org CI gate:** 0 repos missing `ci.yml` on default branch (REST full-org sweep: 33/33 non-exempt OK).
- **`ensure-org-repo-ci.py`** exit 0 — OK: **12** (script scope via `ORG_REPOS` / partial GraphQL list), missing: **0**.
- **Full REST audit (35 active repos):** 33 OK, 2 exempt (`li-cursor-agents`, `research-findings`), 0 missing, 0 incomplete.
- **`ecosystem-audit.json` aligned:** `repos_missing_ci_main: 0`, `missing_ci_on_main: []`.
- **No CI template PRs** opened — functionality gate satisfied; no isolated-clone `ci.yml` rollouts required.
- **`lidb` default branch is `main`** with `ci.yml` present — WP-H0 gate cleared (stale note in audit config remains).
- **GraphQL quota exhausted** (0/5000); REST core ~2700 remaining — script `gh repo list` under-scopes to 12 repos until GraphQL resets or audit uses REST paginate.
- **Branch protection rulesets** not org-wide — workflow job ids match `roadmap/scripts/org-branch-protection.json` locally.

## Deliverable / findings

| Check | Result |
|-------|--------|
| `ensure-org-repo-ci.py` | exit **0** — OK: **12**, missing: **0**, gated: **0**, incomplete: **0** |
| REST full-org `ci.yml` audit | **33** OK, **0** missing, **2** exempt, **0** incomplete |
| `ecosystem-audit.json` | `repos_missing_ci_main`: **0**, `missing_ci_on_main`: **[]** |
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
| fix(audit): REST paginate fallback when GraphQL rate-limited in ensure-org-repo-ci | benchmarks | `ecosystem-ci`, `agent:ci_maintainer` |
| Apply org branch protection rulesets (required check: `check`) | org settings / roadmap | `ecosystem-governance` |
| Remove `continue-on-error` from lic windows CI matrix job | lic | `ecosystem-ci`, `ci-hygiene` |

## Deferred

- **Audit scope expansion** — add 22 onboarded repos to `org_repos.py` / `ensure-org-repo-ci.py` REST fallback (onboarder handoff).
- **Branch protection rollout** for package mirrors — human `roadmap/scripts/apply-org-branch-protection.sh`.
- **lic windows `continue-on-error`** — separate hygiene pass (out of scope for add-CI mandate).
- **GraphQL quota recovery** — defer `gh repo list` full-org sweep until rate limit resets (~2026-05-30T14:09Z).
