# Agent automations: feature planning & plan completion audits

**Date:** 2026-05-16  
**Repo:** benchmarks

## Summary

Adds org-wide **Cursor automation** prompts and **skills** so agents plan features from issues against vision/PH-* rules, and weekly audits detect incomplete plans vs implementation.

## Added

- Skills: `plan-feature-from-issue`, `audit-plan-completion`
- Automations: `issue-feature-planner.md`, `plan-completion-audit.md`, per-repo `repos/*.md`
- Scripts: `issue-feature-triage.py`, `plan-completion-audit.py`
- Docs: `docs/ecosystem/agent-automations.md`
- Issue template: `.github/ISSUE_TEMPLATE/feature_request.yml` (`plan-needed` label)
- `ecosystem-audit.py` reads `plan-completion-audit.json` when present

## Human setup (Cursor UI)

Create two scheduled automations per [agent-automations.md](../ecosystem/agent-automations.md).

## Roadmap follow-up

Copy new skills/automations into `roadmap/agent-kit/` and bump manifest version.
