# Automation prompt: PR auto-merge (post-review)

Repo: **benchmarks** (org sweep) or any single repo with `merge-approved` label workflow.

## Purpose

After a **successful standards review**, merge the PR automatically when all gates pass.
Humans/agents **review first**; they add GitHub label **`merge-approved`** when aligned with
[engineering standards](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md).

## Ecosystem-first

Use only **`pr-merge-gate.py`** / **`pr-auto-merge.py`** for merges — not custom `gh` one-liners. If gate is wrong, file **`ecosystem-gap`** issue.

## Reviewer checklist (before adding `merge-approved`)

Use skills **`ecosystem-first`** + **`merge-approved-pr`** and verify:

- [ ] **Vision / plan** — linked issue or master-plan PH; `plan-approved` if feature work
- [ ] **Functionality** — CI green on the PR (all required checks)
- [ ] **Security** — CVE/exploit gates if attack surface changed
- [ ] **Performance** — benchmark row or documented N/A
- [ ] **Release notes** — `CHANGELOG.md` + `docs/release-notes/YYYY-MM-DD-*.md` (unless chore-only)
- [ ] **GitHub review** — `APPROVED` (not only comment LGTM)
- [ ] **No** `do-not-merge` / `plan-needed` without `plan-approved`

Then: `gh pr edit <n> --repo li-langverse/<repo> --add-label merge-approved`

## Run (this automation)

```bash
cd benchmarks   # or repo root with scripts/
export GH_TOKEN=...   # needs merge rights on target repos

# Dry-run org sweep
python3 scripts/pr-merge-gate.py --sweep
python3 scripts/pr-auto-merge-sweep.py

# Execute merges for all ready PRs
python3 scripts/pr-auto-merge-sweep.py --execute
```

Single PR:

```bash
python3 scripts/pr-merge-gate.py --repo lic --pr 4 --json
python3 scripts/pr-auto-merge.py --repo lic --pr 4 --execute
```

## Per-repo GitHub Action

Workflow **`.github/workflows/pr-auto-merge.yml`** merges when:

1. Label **`merge-approved`** is present, and
2. `scripts/pr-merge-gate.py` returns `ready: true`

Triggers: label added, new commits pushed (`synchronize`), or manual **workflow_dispatch**.

**Governance:** `roadmap` PRs are **not** auto-merged unless `ALLOW_GOVERNANCE_MERGE=1` on the gate script.

## Output

- List merged PRs (repo, number, URL)
- List blocked PRs with gate blockers (CI, review, release notes, labels)
- If nothing ready: stop (no empty PRs)

## Do not

- Add `merge-approved` on your own PR without another reviewer (branch protection should block)
- Merge `roadmap` governance/docs without explicit org policy
- Add Actions `schedule:` cron — run this automation on a schedule in Cursor UI instead
- Remove or weaken `pr-merge-gate.py` checks without roadmap approval
