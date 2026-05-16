# Release notes: 2026-05-16 — numerics research methodology

**Date:** 2026-05-16  
**Repo:** benchmarks  
**PH / REQ:** PH-5b, PH-7e  

## Summary

Canonical numerics research workflow for agents and humans: **SOTA survey** of reference implementations and numerical recipes, optional **autoresearch** for novel algorithms, mandatory **evidence packs** (stability, performance, accuracy, plots, animations) aligned with org vision and ecosystem-first policy.

## Added

| Item | Path |
|------|------|
| Methodology | `docs/numerics/research-methodology.md` |
| Algorithm template | `docs/numerics/algorithm-note-template.md` |
| Study location | `docs/numerics/studies/README.md` |
| Skill | `.cursor/skills/research-li-numerics/SKILL.md` |
| Skill | `.cursor/skills/numerics-autoresearch/SKILL.md` |
| Checklist script | `scripts/numerics-evidence-checklist.py` |
| Command | `.cursor/commands/numerics-research.md` |
| Automation | `.cursor/automations/numerics-research-cycle.md` |

## Usage

```bash
python3 scripts/numerics-evidence-checklist.py --study docs/numerics/studies/YYYY-MM-DD-slug.md
LIC_ROOT=../lic ./scripts/render-benchmark-visuals.sh
```

## Propagate

Sync via `roadmap/agent-kit` to **lic** (primary implementation repo) and bump manifest.

## Benchmark impact

N/A — documentation and agent policy only.
