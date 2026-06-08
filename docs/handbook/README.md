# Benchmarks handbook

This repo is the **org performance dashboard** — catalog, ingest, static Pages site, and agent preflight JSON. Harness sources stay in **`lic`** (and tier-5 HTTP in **`lis`**).

## Live site vs in-repo docs

| Surface | URL / path |
|---------|------------|
| **Dashboard (GitHub Pages)** | https://li-langverse.github.io/benchmarks/ |
| **Handbook (this tree)** | [`docs/handbook/README.md`](README.md) |
| **Ecosystem ops** | [`docs/ecosystem/`](../ecosystem/) |
| **Numerics research** | [`docs/numerics/`](../numerics/) |

If Pages returns **404**, enable **Settings → Pages → GitHub Actions** and run `pages.yml` on `main` — see [SETUP_GITHUB.md](../../SETUP_GITHUB.md).

**Local preview (no Pages):**

```bash
LIC_ROOT=../li ./scripts/dashboard/render-static.sh
open static-dashboard/index.html
```

## Vision & plan cross-links

| Doc | Role |
|-----|------|
| [Org vision & roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md) | Pillars, where visions live |
| [Engineering standards](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md) | Security, perf, PR discipline |
| [**Li master plan**](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md) | **PH-*** phase tracker (normative order) |
| [**Provability gaps**](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) | Honest **G-*** register — do not overclaim proof |
| [Phase plans (lic)](https://github.com/li-langverse/lic/tree/main/docs/superpowers/plans) | Per-phase checklists (`2026-05-14-phase-*.md`, product plans) |
| [Development overview](https://li-langverse.github.io/roadmap/development-overview/) | PR queue, branch CI, docs/bench snapshot |

Detailed map: [plan-cross-links.md](../ecosystem/plan-cross-links.md).

## Benchmark honesty

Dashboard rows are **measurements**, not proof certificates. Labels and thresholds: [benchmark-dashboard.md](../honesty/benchmark-dashboard.md).

Reference C++ / HPC **SOTA version pins** and bump cadence (Eigen, Kokkos, PETSc, Chapel): [reference-baseline-versions.md](../honesty/reference-baseline-versions.md).

## Agents

[AGENTS.md](../../AGENTS.md) · [Release notes policy](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/release-notes.md) · Preflight: `./scripts/agent-preflight.sh`

## Li language (style + shareables)

Short guides and **syntax-highlighted code PNGs** for posts: [`docs/language/README.md`](../language/README.md) — regenerate via `scripts/render-li-code-image.py --all`.
