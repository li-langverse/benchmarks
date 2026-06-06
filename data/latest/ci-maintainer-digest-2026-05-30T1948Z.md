# ci_maintainer proactive digest — 2026-05-30T19:48Z

Run: `ci_maintainer-1780170449021` · Agent: `ci_maintainer` · Source: proactive

## Executive summary

- **Org CI gate green:** 34 repos OK, **0 missing** `ci.yml` on default branch; **0 gated**, **0 audit_incomplete**.
- **Ecosystem audit aligned:** `repos_missing_ci_main: 0`, `missing_ci_on_main: []` — prior REST rate-limit false positives cleared.
- **GitHub REST healthy:** core **4891/5000**; full org scan succeeded without `--allow-local-fallback`.
- **No CI PRs opened** — functionality gate satisfied; no `lic/scripts/templates/github-repo/ci.yml` rollouts needed.
- **`research-findings`** remains CI-exempt (archive repo) in org-repo-ci audit.
- **Branch protection:** direct API returns 404 on `lic`/`lip`; org rulesets not readable with current token — human `apply-org-branch-protection.sh` still deferred.
- **Pre-existing hygiene:** `lic` `build-and-test-windows` uses `continue-on-error: true` (OS matrix) — out of scope for add-CI pass.
- **North star:** ecosystem platform hygiene — proof-before-perf CI gate on package mirrors (secure + provable pillar).

## Deliverable / findings

| Check | Result |
|-------|--------|
| `ensure-org-repo-ci.py` | exit **0** — OK: **34**, missing: **0**, gated: **0**, incomplete: **0** |
| `ecosystem-audit.py` | exit **0** — `missing_ci_on_main`: **[]** |
| CI PRs opened this run | **0** |
| Isolated clone `ci.yml` edits | **0** |
| Required check vs workflow (template hints) | `lic` → `build-and-test`; `lip` → `bootstrap`; package mirrors → `check` |

### Branch protection vs required checks (spot-check)

| Repo | Template job | Workflow present | Direct protection API |
|------|--------------|------------------|-------------------------|
| `lic` | `build-and-test` | ✓ (`ci.yml`) | 404 (rulesets or unprotected) |
| `lip` | `bootstrap` | ✓ (`ci.yml`) | 404 (rulesets or unprotected) |
| Package mirrors | `check` | ✓ (`ci.yml` on all 34 OK repos) | rulesets TBD (token 403) |

## Recommended issues/PRs

None required for missing CI.

| Title | Repo | Labels |
|-------|------|--------|
| Apply org branch protection rulesets (required check: `check`) | org settings / roadmap | `ecosystem-governance` |
| Remove `continue-on-error` from lic windows CI matrix job | lic | `ecosystem-ci`, `ci-hygiene` |
| fix(workspace): skip broken paths in workspace-prune stat | li-cursor-agents | `agent-infra` |

## Deferred

- **Branch protection rollout** for package mirrors — human `roadmap/scripts/apply-org-branch-protection.sh`.
- **lic windows `continue-on-error`** — separate hygiene pass (do not weaken OS matrix gates on new CI rollouts).
- **Org rulesets visibility** — token lacks org rulesets scope; verify protection alignment after human rollout.
- **Per-repo CI red on open PRs** — `bug_fixer` / `pr_alignment` scope (ecosystem audit: 0 open/failed PRs this cycle).
