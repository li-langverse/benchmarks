---
name: run-local-pages-benchmarks
description: >-
  Refresh benchmarks Pages and roadmap development overview without GitHub
  Actions. Relative cpp ratios + hardware banner. Use when sites are stale or
  GHA quota is exhausted.
---

# Local Pages (benchmarks repo)

See canonical skill: **`lic/.cursor/skills/run-local-pages-benchmarks/SKILL.md`**.

```bash
LIC_ROOT=../lic ./scripts/refresh-live-sites.sh
./scripts/deploy-pages-local.sh --build
```
