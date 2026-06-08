# Ecosystem explorer

**Purpose:** Periodically discover **missing implementations**, **stdlib/package gaps**, **benchmark catalog holes**, and **language-design opportunities** by combining:

1. **Local static scan** — `scripts/ecosystem-explorer.py` → `data/latest/ecosystem-explorer.json`
2. **HPC rubric** — compare Li to Eigen, Kokkos, PETSc, FFTW, OpenMP, SUNDIALS, … — normative **release pins** and bump cadence: [reference-baseline-versions.md](../honesty/reference-baseline-versions.md)
3. **External signals** — Cursor agent **web search** (Reddit, papers, GitHub discussions); the script does **not** scrape Reddit (ToS / rate limits).

**Not a substitute for:** [ecosystem-health](../../.cursor/automations/ecosystem-health.md) (CI/PR reds) or [numerics-research-cycle](../../.cursor/automations/numerics-research-cycle.md) (kernel-level SOTA).

---

## Run locally

```bash
cd benchmarks
LIC_ROOT=../lic python3 scripts/ecosystem-explorer.py
cat data/latest/ecosystem-explorer.json | python3 -m json.tool | head -80

# Optional markdown digest for PR/issue attachment
LIC_ROOT=../lic python3 scripts/ecosystem-explorer.py \
  --write-digest docs/ecosystem/explorer-digests/latest.md
```

**GitHub Actions:** `workflow_dispatch` → **Ecosystem explorer** (uploads JSON artifact; no `schedule:`).

---

## Cursor automation

1. [cursor.com/automations](https://cursor.com/automations) → **New automation**
2. **Schedule:** weekly (e.g. Monday) or biweekly
3. **Repo:** `li-langverse/benchmarks` (multi-repo workspace with `lic` sibling)
4. **Instructions:** paste [.cursor/automations/ecosystem-explorer.md](../../.cursor/automations/ecosystem-explorer.md)
5. **Skill:** `explore-li-ecosystem`

Slash command: `/explore-ecosystem`

---

## Agent workflow (summary)

| Step | Action |
|------|--------|
| 1 | Run `ecosystem-explorer.py` + `ecosystem-audit.py` |
| 2 | Execute 3–5 `web_search_queries` from JSON (Reddit + web) |
| 3 | Map findings → **ecosystem-gap** or **feature** issue (label `explorer-finding`) |
| 4 | Link to PH ids / `catalog.toml` row when proposing benches |
| 5 | Do **not** implement until `plan-approved` |

---

## Output fields (`ecosystem-explorer.json`)

| Field | Meaning |
|-------|---------|
| `missing_std_modules` | `std.io`, `std.csv`, … expected by benchmarks ingest |
| `hpc_libraries` | Static rubric vs Li status (`missing` / `partial` / …) |
| `catalog.suggested_catalog_gaps` | New bench categories (FFT, pure_li, …) |
| `web_search_queries` | Ready-made queries for Cursor web search |
| `open_ecosystem_gap_issues` | Open org issues labeled `ecosystem-gap` |
| `recommended_actions` | Prioritized next steps |

---

## Filing issues

```bash
python3 scripts/file-ecosystem-gap-issue.py \
  --repo lic \
  --title "std/csv: PH-IO-4 CSV ingest for benchmarks" \
  --what-tried "ecosystem-explorer: std.csv missing on main" \
  --expected "import std.csv in ingest smoke" \
  --blocked "module not found at compile time"
```

Add label **`explorer-finding`** for triage. Planner automation picks up `ecosystem-gap` + `plan-needed`.

---

## Reddit / community sources (manual agent search)

| Source | Use for |
|--------|---------|
| r/ProgrammingLanguages, r/Compilers | Language design, ownership, verification |
| r/HPC, r/scientificcomputing | Libraries, Kokkos/OpenMP, solver stacks |
| r/cpp, r/rust | Performance comparisons, interop expectations |
| HN / Lobsters | “New language” threads, tooling gaps |

**Policy:** Summarize publicly; do not paste private messages. Cite URLs in issues.

---

## HPC rubric refresh

When explorer passes cite new Eigen/Kokkos/PETSc/Chapel releases:

1. Diff upstream release pages against [reference-baseline-versions.md](../honesty/reference-baseline-versions.md).
2. If major/minor changed, open a **benchmarks** docs PR updating the pin table (`last_reviewed`, release URLs) within **30 days**.
3. Do **not** duplicate pin tables in digests — link the normative doc; digests remain ephemeral evidence.

---

## Related

- [reference-baseline-versions.md](../honesty/reference-baseline-versions.md) — SOTA pin table + agent tooling parity
- [tooling-catalog.md](./tooling-catalog.md)
- [ecosystem-first.md](./ecosystem-first.md)
- [agent-automations.md](./agent-automations.md)
- Skill: [explore-li-ecosystem](../../.cursor/skills/explore-li-ecosystem/SKILL.md)
