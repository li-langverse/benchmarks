# Ecosystem explorer automation

## Summary

Adds a **discovery** loop for the Li org: static scans of `lic` std/packages, benchmarks ingest expectations, catalog gaps, and an HPC-library rubric — plus ready-made **Reddit/web search queries** for Cursor agents.

## Agent continuation

1. **Cursor UI:** New automation from `.cursor/automations/ecosystem-explorer.md` (weekly).
2. **Run:** `LIC_ROOT=../lic python3 scripts/ecosystem-explorer.py`
3. **Web:** Execute `web_search_queries` from `data/latest/ecosystem-explorer.json`
4. **File:** `explorer-finding` + `ecosystem-gap` / `feature` issues; planner picks up `plan-needed`

## Changed

| Area | Path |
|------|------|
| Script | `scripts/ecosystem-explorer.py` |
| Skill | `.cursor/skills/explore-li-ecosystem/SKILL.md` |
| Automation | `.cursor/automations/ecosystem-explorer.md` |
| Command | `.cursor/commands/explore-ecosystem.md` |
| Workflow | `.github/workflows/ecosystem-explorer.yml` (dispatch only) |
| Docs | `docs/ecosystem/ecosystem-explorer.md` |

## Not changed

- No Reddit API integration (agents use web search manually)
- No `schedule:` cron on GitHub Actions

## Breaking

N/A
