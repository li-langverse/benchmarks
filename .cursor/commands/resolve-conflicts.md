# /resolve-conflicts

Resolve PR merge conflicts **without reverting** main or branch progress.

```bash
gh pr view <N> --repo li-langverse/<repo> --json mergeable,headRefName,baseRefName
git fetch origin && git checkout <headRefName>
git merge origin/main
git diff --name-only --diff-filter=U
# edit each file — skill: resolve-merge-conflicts
git commit -m "merge: integrate main (preserve both sides)"
git push origin HEAD
```

Policy: [merge-conflict-resolution.md](../../docs/ecosystem/merge-conflict-resolution.md)
