# Repo scope: **benchmarks** (issue feature planner)

Parent: [issue-feature-planner.md](../issue-feature-planner.md)

## This repo

- **In scope:** `catalog.toml`, ingest, dashboard, `scripts/*audit*`, docs/ecosystem
- **Out of scope:** physics/compiler kernels — file **lic** issue instead

## Feature examples

| Issue | Plan location |
|-------|----------------|
| New catalog row | `catalog.toml` + release notes; lic bench must exist first |
| Dashboard chart | `dashboard-next/app/`, `dashboard-next/components/` — routes `/`, `/bench/[id]`, `/pillar/[id]`, `/matrix`, `/history` (Pages base `/benchmarks/`) |
| New automation | `.cursor/automations/` + `docs/ecosystem/agent-automations.md` |

**Dashboard (deployed):** https://li-langverse.github.io/benchmarks/ — sitemap: `docs/dashboard/sitemap.md`

## Completion audit

```bash
python3 scripts/plan-completion-audit.py
python3 scripts/ecosystem-audit.py
```

Commit JSON to `data/latest/` only on dedicated bot branch if org allows.
