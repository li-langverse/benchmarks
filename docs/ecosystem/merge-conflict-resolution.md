# Merge conflict resolution (org policy)

**Goal:** Integrate **`main`** and the **PR branch** so **nothing advanced is lost** on either side.

**Skill:** `.cursor/skills/resolve-merge-conflicts/SKILL.md`

---

## Core rule

> **Never revert progress.** Do not pick “all main” or “all branch” to finish fast.  
> Conflicts mean **both lines moved forward** — produce a **third state** that keeps both intents.

| Forbidden | Required |
|-----------|----------|
| `git checkout --ours .` / `--theirs .` on the whole tree | Read each conflicted hunk |
| Dropping the PR’s feature because main “looks newer” | Keep PR commits’ behavior |
| Dropping main’s fixes because the PR “owns” the file | Keep main’s security/CI/docs fixes |
| Force-push to “clean up” after a bad resolution | Normal `git push` after correct merge |

---

## Workflow

```bash
git fetch origin
git checkout <feature-branch>
git merge origin/main   # or: git rebase origin/main (repo policy; see git-workflow.md)
```

For each conflicted file:

1. **Identify sides** — `<<<<<<< HEAD` (current branch) vs `>>>>>>> origin/main` (incoming).
2. **Classify** — independent edits vs same-line semantic clash.
3. **Integrate** — union of additions; merge semantics on overlaps (see skill).
4. **Verify** — file must build; no duplicate imports, labels, or workflow keys.
5. **Stage** — `git add <file>` only when both sides’ intent is preserved.

```bash
git status
# run repo CI locally when possible
git commit -m "merge: integrate main into <branch> (preserve both sides)"
git push origin HEAD
```

---

## Conflict patterns

| Pattern | Resolution |
|---------|------------|
| Both added different lines | Keep **both** blocks (order: main infra first, then feature). |
| Both edited same function | Merge logic: main’s fix + branch’s feature (re-run tests). |
| Main deleted / branch modified | Usually **keep branch content** if still needed; confirm main deletion wasn’t intentional removal. |
| Branch deleted / main modified | Usually **keep main**; re-apply branch intent as new commits if still required. |
| Lockfiles / generated | Regenerate from merged manifests, don’t hand-pick one lockfile. |
| `status.json` / audit JSON | Merge keys or regenerate script; don’t wipe live metrics from either side. |

---

## PR hygiene

- Comment on the PR: files touched, what was kept from **main** vs **branch**.
- Re-run **CI** before `merge-approved`.
- If conflicts are governance/docs only, still preserve **automation + snapshot** updates from both sides.

---

## Related

- [git-workflow.md](./git-workflow.md) — no force push
- Skills: `resolve-merge-conflicts`, `plan-merge-queue`, `merge-approved-pr`
- `python3 scripts/run-pr-program.py` — don’t admin-merge `CONFLICTING` PRs; fix first
