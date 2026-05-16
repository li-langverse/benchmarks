# /explore-ecosystem

Ecosystem discovery: missing std/libs, HPC parity, Reddit/web signals.

**Skill:** `explore-li-ecosystem` · **Doc:** [ecosystem-explorer.md](../../docs/ecosystem/ecosystem-explorer.md)

```bash
cd benchmarks
LIC_ROOT=../lic python3 scripts/ecosystem-explorer.py \
  --write-digest docs/ecosystem/explorer-digests/latest.md
cat data/latest/ecosystem-explorer.json
```

Then run **web search** on `web_search_queries` from the JSON (Reddit + HPC libs). File issues with label `explorer-finding` — no code until `plan-approved`.
