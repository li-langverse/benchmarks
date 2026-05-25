# Org repo CI policy

Every repository under **`li-langverse`** must have **`.github/workflows/ci.yml`** on its default branch before:

- Listing in [official-packages.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/official-packages.md)
- Enabling Dependabot merges
- Applying required status checks in [org-branch-protection.json](https://github.com/li-langverse/roadmap/blob/main/scripts/org-branch-protection.json)

## Audit

```bash
python3 scripts/ensure-org-repo-ci.py
cat data/latest/org-repo-ci-audit.json
```

Exit code **1** if any repo is missing CI — suitable for `workflow_dispatch` or agent pre-flight.

## Official package mirrors

Template: [`lic/scripts/templates/github-repo/ci.yml`](https://github.com/li-langverse/lic/blob/main/scripts/templates/github-repo/ci.yml)

Monorepo path: `lic/packages/<name>/.github/workflows/ci.yml`

```bash
cd lic
./scripts/ensure-package-ci.sh
./scripts/push-official-package-repo.sh <name>
```

## New repos

1. `./scripts/li-new-package <name> --official` (includes `ci.yml`)
2. `gh repo create li-langverse/<name> …`
3. `./scripts/push-official-package-repo.sh <name> --create`
4. `cd roadmap && ./scripts/apply-org-branch-protection.sh <name>`

**Agents:** do not create empty org repos. **Cursor rule:** `li-repo-ci-required` (lic + benchmarks).

## Required check names (branch protection)

| Repo | Context |
|------|---------|
| `lic`, `li-language` | `build-and-test` |
| `benchmarks` | `ingest-smoke` (+ `dashboard-static` optional) |
| `lip` | `bootstrap` |
| `lit` | `test` |
| `roadmap` | `verify-kit` |
| Package mirrors | `check` |

**Default branch:** workflows are read from each repo's **current default branch** (`gh repo view --json defaultBranchRef`), not from a local sibling checkout. Use `--allow-local-fallback` only for offline dev.

**Non-main default (WP-H0):** `lidb` is listed in `repos_gated_non_main_default` until its default branch is `main`; it must not appear in `repos_ok` because a local clone has `ci.yml`.
