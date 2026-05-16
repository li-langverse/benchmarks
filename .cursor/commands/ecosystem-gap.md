# /ecosystem-gap

File a standardized **ecosystem-gap** issue when catalog tooling is missing or fails.

## Steps

1. Confirm [tooling-catalog.md](../../docs/ecosystem/tooling-catalog.md) has no fit
2. Run:

```bash
python3 scripts/file-ecosystem-gap-issue.py \
  --repo <repo> \
  --title "<short title>" \
  --what-tried "<command or path tried>" \
  --expected "<what catalog should do>" \
  --blocked "<error or gap>"
```

3. Stop — do not add ad-hoc scripts in the feature PR without that issue
4. **issue-feature-planner** will draft a plan after `plan-needed`; implement after `plan-approved`
