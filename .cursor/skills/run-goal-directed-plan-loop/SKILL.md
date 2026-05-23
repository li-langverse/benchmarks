---
name: run-goal-directed-plan-loop
description: >-
  Pointer to goal-directed plan loop skill (overnight agents, plan-loop.py).
  Use when running httpd/ecosystem plan loops from the benchmarks sibling repo.
---

# Goal-directed plan loop

See **`lic/.cursor/skills/run-goal-directed-plan-loop/SKILL.md`** (httpd commands) and  
**`li-cursor-agents/.cursor/skills/run-goal-directed-plan-loop/SKILL.md`** (full pattern).

Preflight from benchmarks:

```bash
./scripts/agent-preflight.sh
```

Pages after agent work:

```bash
LIC_ROOT=../lic ./scripts/refresh-live-sites.sh
```
