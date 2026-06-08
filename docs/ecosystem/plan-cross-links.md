# Plan cross-links (master plan ↔ gaps ↔ phases)

Agents use this map so **vision**, **PH trackers**, and **honest proof status** stay aligned across repos.

## Canonical documents

| Layer | Repository | Path |
|-------|------------|------|
| **Master plan** (PH order, repo policy) | `lic` | [`docs/superpowers/plans/2026-05-14-li-master-plan.md`](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md) · [plan-cross-links (lic)](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/plan-cross-links.md) |
| **Provability gaps (G-*)** | `lic` | [`docs/verification/provability-gaps.md`](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) |
| **Phase plans** | `lic` | [`docs/superpowers/plans/`](https://github.com/li-langverse/lic/tree/main/docs/superpowers/plans) (`2026-05-14-phase-*.md`, lip/lip/httpd/math plans) |
| **Ecosystem governance** | `roadmap` | [`docs/ecosystem/vision-and-roadmap.md`](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md) |
| **Milestones (themes)** | `roadmap` | [`docs/roadmap/milestones.md`](https://github.com/li-langverse/roadmap/blob/main/docs/roadmap/milestones.md) |
| **Benchmark catalog & dashboard** | `benchmarks` | [`catalog.toml`](../../catalog.toml) · [handbook](../handbook/README.md) · [HPC reference cadence](./hpc-reference-library-cadence.md) |

## Edit rules

1. **Cross-repo or pillar change** → update **master plan** + open **roadmap** proposal (human merge on governance paths).
2. **Close a G-* row** → same PR as the implementation; update **provability-gaps.md** (Partial → Done only with evidence cited in the table).
3. **Close a PH phase checkbox** → same PR as the deliverable; link bench rows or `li-tests` where applicable.
4. **Perf claim** → `catalog.toml` row + ingest; cite dashboard URL; do not mark proof **Done** from bench green alone.

## Phase plan index (lic)

| Plan | PH / topic |
|------|------------|
| `2026-05-14-phase-00-bootstrap.md` | Bootstrap |
| `2026-05-14-phase-01-lexer-parser.md` | Parser |
| `2026-05-14-phase-02-typechecker.md` | Types |
| `2026-05-14-phase-03-mir-codegen.md` | MIR / LLVM |
| `2026-05-14-phase-04-runtime-stdlib.md` | Runtime / std |
| `2026-05-14-phase-05-tetris.md` | Demo game |
| `2026-05-14-phase-06-self-host.md` | Self-host |
| `2026-05-14-phase-07-native-hpc.md` | **PH-5b**, SIMD / tier-1 |
| `2026-05-14-benchmarks-and-simulations.md` | Bench harness |
| `2026-05-16-li-package-manager-lip.md` | **lip** |
| `2026-05-16-li-httpd-plan.md` | **lis** / httpd |
| `2026-05-16-li-math-linalg-surface.md` | Math / **PH-7e** · **G-math**, **G-math-syn** |
| `2026-05-24-studio-ui-ux-plan-loop.md` | **PH-UX** / Studio (UX honesty, not Lean) |
| `2026-05-22-parallel-compile-ci.md` | **PH-8p** — parallel compile / CI throughput |
| **lidb / registry DB** (proposal) | **PH-DB-*** · [tier-db-registry-benchmark.md](./tier-db-registry-benchmark.md) |
| **lidb graph / vector / GPU** (PH-DB-G0) | [tier-db-graph-registry.md](./tier-db-graph-registry.md) · [tier-db-vector-ann.md](./tier-db-vector-ann.md) · [tier-db-gpu-speedup.md](./tier-db-gpu-speedup.md) |
| **lidb full-spectrum audit** (WP-N4) | [tier-db-security.md](./tier-db-security.md) · [tier-db-memory.md](./tier-db-memory.md) · [tier-db-parallel.md](./tier-db-parallel.md) · [tier-db-audit.md](./tier-db-audit.md) · [tier-db-realtime.md](./tier-db-realtime.md) |

## Open master-plan tracker rows (2026-05-30)

Preflight: `data/latest/ecosystem-audit.json` · `plan_completion_audit.summary.open_tracker_items: 5`. Do not mark **Done** without cited evidence.

| PH | Gap ID(s) | Phase plan (lic) |
|----|-----------|------------------|
| **2i** — Math / linalg | **G-math**, **G-math-syn** | [`2026-05-16-li-math-linalg-surface.md`](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-math-linalg-surface.md) |
| **7d** — Execution decorators | **G-dec**, **G-par** | [`2026-05-16-li-execution-decorators.md`](https://github.com/li-langverse/lic/blob/main/docs/superpowers/specs/2026-05-16-li-execution-decorators.md) · [`phase-07-native-hpc`](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-phase-07-native-hpc.md) |
| **7e** — Math → SIMD lowering | **G-math** | [`2026-05-16-li-math-linalg-surface.md`](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-math-linalg-surface.md) · [`benchmarks-and-simulations`](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-benchmarks-and-simulations.md) |
| **8p** — Parallel compile / CI | — | [`2026-05-22-parallel-compile-ci.md`](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-22-parallel-compile-ci.md) |
| **Vision-LLM** — Agent JSON diagnostics | — | [`2026-05-16-li-llm-first-design.md`](https://github.com/li-langverse/lic/blob/main/docs/superpowers/specs/2026-05-16-li-llm-first-design.md) |

## UI / UX audit handoff (`ui_ux_quality` research goal)

Surface quality is **not** proof — keep separate from **G-*** rows. Supports **`gui_ux_tester`**, **`docs_ui_tester`**, **`studio_ui_ux_builder`**.

| Agent | Surface | Latest digest |
|-------|---------|---------------|
| `gui_ux_tester` | GUI apps, fixtures, native SDL | [2026-05-30-gui-ui.md](./ux-digests/2026-05-30-gui-ui.md) · `data/latest-gui-ui-run/ui-audit.json` |
| `docs_ui_tester` | MkDocs / handbook Pages | [2026-05-31-docs-ui.md](./ux-digests/2026-05-31-docs-ui.md) · `data/latest-docs-ui-run/ui-audit.json` |
| `studio_ui_ux_builder` | PH-UX plan loop, bench gates | [`data/latest/studio-ui-ux-builder-digest.md`](../../data/latest/studio-ui-ux-builder-digest.md) |

Remediation: `data/latest/remediation_manifest.json` (P1 issues + acceptance checklists). Workflow repo routing: **`lic`** for studio-ui-ux harness; **`li-cursor-agents`** for ux-harness adapters.

## Automation

`python3 scripts/plan-completion-audit.py` reads **LIC_ROOT** (default `../lic` sibling checkout; CI `lic`. Skips path=unknown and catalog_lifecycle=planned.) Output: `data/latest/plan-completion-audit.json` (`master_plan_open` = tracker only; `stale_spec_checklists` = normative task bullets, not gates).
