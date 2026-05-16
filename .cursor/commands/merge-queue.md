# /merge-queue

Plan merge order and find redundant PRs before auto-merge.

```bash
python3 scripts/pr-merge-queue-plan.py
```

Read `data/latest/pr-merge-queue-plan.json` — merge `merge_first` before others; resolve `redundant` and `stacks` before `pr-auto-merge-sweep --use-plan --execute`.

Skill: **plan-merge-queue**
