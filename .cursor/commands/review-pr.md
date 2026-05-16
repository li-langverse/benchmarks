# /review-pr

**PR review agent** — standards + gate (agent judgment, not script-only).

**Skills:** `merge-approved-pr`, `review-pr-alignment`  
**Prompt:** [.cursor/automations/pr-review-agent.md](../automations/pr-review-agent.md)

```bash
python3 scripts/pr-merge-gate.py --repo li-langverse/<repo> --pr <N> --json
gh pr diff <N> --repo li-langverse/<repo>
```

Approve + `merge-approved` only when all gates pass. Merge via **pr-auto-merge** automation separately.
