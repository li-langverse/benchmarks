# Release notes: 2026-05-25 — ensure-org-repo-ci lidb gate

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (WP-A2)  
**PH / REQ:** org hygiene WP-A2  
**Author:** agent

---

## Summary (one sentence)

Hardens `ensure-org-repo-ci.py` so repos are not marked OK from local clone fallbacks when GitHub's default branch lacks `ci.yml`, and gates `lidb` until WP-H0 sets default branch to `main`.

## Agent continuation (required)

1. **Read:** `scripts/ensure-org-repo-ci.py`, `docs/ecosystem/repo-ci-required.md`, li-cursor-agents `docs/plans/2026-05-25-org-hygiene-multi-agent-plan.md` WP-H0 / WP-B1
2. **Run:** `python3 tests/test_ensure_org_repo_ci.py -q`; `python3 scripts/ensure-org-repo-ci.py --repo lidb`
3. **Then:** After human WP-H0 (`lidb` default → `main`), remove `lidb` from `NON_MAIN_DEFAULT_GATES` and land `ci.yml` via WP-B1
4. **Blocked on:** WP-H0 human default-branch rename for `lidb` — **none** for this benchmarks-only PR

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Audit script | Default-branch `gh api` required; `repos_gated_non_main_default`; `repos_audit_incomplete`; `--allow-local-fallback` dev flag | `tests/test_ensure_org_repo_ci.py` (6 tests) |
| Docs | `docs/ecosystem/repo-ci-required.md` — default branch + lidb gate | — |
| CI | `org-repo-ci-audit.yml` runs unittest | workflow_dispatch / PR paths |

## Not changed (scope fence)

- `lidb` repo CI workflow / agent-kit — **WP-B1** after WP-H0
- `ecosystem-audit.py` `has_ci_on_main` — separate follow-up if needed
- Committed `data/latest/org-repo-ci-audit.json` — regenerated in GHA with token

## Breaking changes

None — stricter audit may surface `repos_audit_incomplete` when `gh` rate-limits; re-run or use org token.

## Security

N/A — read-only GitHub API audit; no new secrets.

## Performance

N/A — one extra `gh repo view` per repo in audit.

## Downstream

| Repo | Action |
|------|--------|
| li-cursor-agents | WP-A2 deliverable |
| lidb | WP-H0 then WP-B1 |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Fixed
- **Org CI audit:** `ensure-org-repo-ci.py` requires GitHub API on default branch; gates `lidb` until WP-H0; drops silent local fallback — [2026-05-25-ensure-org-repo-ci-lidb-gate.md](docs/release-notes/2026-05-25-ensure-org-repo-ci-lidb-gate.md).
```
