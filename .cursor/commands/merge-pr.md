# /merge-pr

Review merge gates and optionally merge a PR labeled `merge-approved`.

## Usage

```
/merge-pr lic 4
/merge-pr benchmarks 7 --execute
```

## Steps

1. Run `python3 scripts/pr-merge-gate.py --repo <repo> --pr <n> --json`
2. If not ready, list blockers and stop
3. If ready and user asked to merge: `python3 scripts/pr-auto-merge.py --repo <repo> --pr <n> --execute`
4. Otherwise remind: add label `merge-approved` and let GitHub Action merge on push

Do not add `merge-approved` on PRs you authored without another reviewer's approval.
