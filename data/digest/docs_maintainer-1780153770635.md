# docs_maintainer digest — 2026-05-30

**Agent:** `docs_maintainer` · **Run:** `1780153770635` · **Heap:** `coord_ecosystem`  
**north_star_fit:** easy · ai-first — `ui_ux_quality` handoff for `gui_ux_tester`; proof status unchanged (**G-*** not edited).

---

## Executive summary

- Preflight `ecosystem-audit.json`: **`repos_without_live_docs: []`**, **`live_docs_down: []`** — 12 org repos with live Pages; no broken handbook URLs this pass.
- Shipped **`docs/ecosystem/gui-ux-quality-handoff.md`** on **lic** (cherry-pick #549 + delta): targets, swarm gaps, workflow-repo routing, studio-ux-12 **Partial** honesty.
- Extended **plan cross-links** (lic + benchmarks mirror): PH-8p, PH-UX, Pkg, **G-*** hints; **Doc-c** lines on six open phase plans.
- Linked GUI UX handoff from **lic Pages hub** (`site/index.html`) and **handbook index**.
- Open **lic#549** superseded by this branch — same scope + nav/routing delta; human should close #549 as duplicate after merge.
- Plan-completion debt (166 findings) unchanged — `plan_verifier` / `implementation_gaps`, not docs.
- Tier-1 **yellow** benches (`matmul_blocked`, `matmul_naive`) — `bench_improver`, not docs.

---

## Deliverable / findings

| Item | Detail |
|------|--------|
| **Repo (primary)** | `li-langverse/lic` — isolated clone `1780153988956` |
| **Repo (digest)** | `li-langverse/benchmarks` — this file |
| **PR (lic)** | `chore/agent-docs_maintainer-1780153770635-digest` |
| **Files (lic)** | `gui-ux-quality-handoff.md`, `plan-cross-links.md`, `site/index.html`, `docs/handbook/README.md`, 6 phase plans, CHANGELOG, release notes |
| **Preflight** | `ecosystem-audit.json` @ 2026-05-30T15:11Z — metrics: 0 repos without live docs, 0 live docs down |
| **ui_ux handoff** | Routes `gui_ux_tester` → `ux-targets.json`, proactive `data/latest-gui-ui-run/`, companion [2026-05-30-gui-ui.md](../docs/ecosystem/ux-digests/2026-05-30-gui-ui.md) |

### Cross-links (master plan ↔ provability-gaps ↔ phases)

- [Master plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md) ↔ [provability-gaps](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) via [plan-cross-links](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/plan-cross-links.md)
- **Doc-c** proof-gap anchors added on: math-linalg, httpd, package-scaffold, ecosystem-governance, parallel-compile-ci, studio-ui-ux plan
- Benchmarks mirror updated with **UI/UX quality** section pointing at lic handoff

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| docs(ecosystem): GUI UX handoff + plan cross-links (run 1780153770635) | `lic` | `li-swarm`, `agent:docs_maintainer` |
| docs(digest): docs_maintainer pass 1780153770635 | `benchmarks` | `li-swarm`, `agent:docs_maintainer` |
| Close duplicate docs(ecosystem): GUI UX handoff (#549) | `lic` | after merge of 1780153770635 branch |
| Human review merge queue — lic#482, #481, #495 ready | multi | `merge-approved` (human) |
| gap: gui_ux_tester full ux-targets Linux CI audit | `li-cursor-agents` | `studio-ui`, `agent:gui_ux_tester` |

---

## Deferred

- **lis** handbook Pages PRs with red CI ([#16](https://github.com/li-langverse/lis/pull/16), [#23](https://github.com/li-langverse/lis/pull/23)) — separate docs pass after CI fix.
- **li-language** / **lic-docs** mkdocs nav drift — `docs_ui_tester` ([#403](https://github.com/li-langverse/lic/issues/403)).
- Playwright/axe adapter for `web_gui` ([#32](https://github.com/li-langverse/li-cursor-agents/issues/32)) — `gui_ui_tester` / harness, not handbook.
- Plan-completion P1 (166 findings) and catalog path gaps (117) — governance / implementer agents.
- Roadmap self-merge — PRs only, human review.
