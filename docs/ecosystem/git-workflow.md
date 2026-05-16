# Git workflow (li-langverse)

Agents and humans follow **PR-only** + **no force push by default**. Hooks enforce this (`agent-kit/hooks/guard-destructive-git.sh`).

---

## Push policy

| Do | Don't |
|----|--------|
| `git push -u origin HEAD` on **your feature branch** | `git push origin main` / `dev` |
| `git fetch` + `git rebase origin/main` then normal `git push` | `git push --force` / `git push -f` |
| Extra **commits** on the branch for review fixes | `git commit --amend` + force after branch is shared |
| `git pull --rebase` to update local branch | Force-push to update PR (unless rare exception below) |

**Default:** if the remote rejects a push, **rebase or merge** the default branch, then push again — do not reach for `--force`.

---

## When the remote rejects your push

```bash
git fetch origin
git rebase origin/main    # or origin/dev per repo default
# resolve conflicts, then:
git push origin HEAD
```

If you already have open commits and need to incorporate review feedback, prefer **new commits** (`git commit`) over rewriting history on a branch that already has a PR.

---

## Rare exception (feature branch only)

Force push is **discouraged** even on feature branches. Use only when:

1. A **human** explicitly asked to rewrite history (e.g. squash before merge done via GitHub UI instead), and
2. Branch is **yours alone** / open PR only you work on, and
3. You use **`git push --force-with-lease`** (never bare `--force`), and
4. Shell hook: `LI_HOOK_ALLOW=1` for that single command.

Never force-push **`main`**, **`dev`**, **`master`**, or org-wide shared long-lived branches.

---

## Merge / close

- Prefer **`merge-approved`** + `pr-auto-merge.py` over manual `gh pr merge` by agents.
- Do not force-push after merge to “fix” main — open a new PR.

---

## Related

- Rule **li-pr-only.mdc**, **li-git-hygiene.mdc**
- [ecosystem-first.md](./ecosystem-first.md)
