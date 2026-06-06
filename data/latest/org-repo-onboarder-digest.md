# Org repo onboarder digest — 2026-05-30T20:22Z

**Agent:** `org_repo_onboarder` · **Source:** proactive · discovery `2026-05-30T20:22Z` · CI audit `2026-05-30T19:56Z` · agent-kit audit `2026-05-30T20:21Z` · briefing `2026-05-30T19:57Z`

## Executive summary

- **Discovery (refreshed):** `github=35` · `known=35` · **`new=0`** · **`stale=0`** — GitHub org and briefing known set are fully aligned.
- **No net-new repos** this cycle; prior P0 **`lic-docs`** graduated into the known set (CI + agent-kit audit coverage) but **onboarding is incomplete**.
- **Highest-risk gap:** **`lic-docs`** — handbook repo with CI on `main`, no agent-kit stamp, no local sibling clone; **`agent_kit_maintainer`** remains P0 before catalog registration.
- **Agent-kit backlog (known repos):** **21** repos with `missing_kit` (canonical stamp `1.3.5+6018e18bf2ed91f4` absent); **13** repos OK.
- **CI gate:** all audited repos have `ci.yml` on `main` (`repos_missing_ci: []`); `research-findings` exempt; no `ci_maintainer` bootstrap needed.
- **Stale catalog entries:** none — no archive/delete candidates.
- **Unclassified verticals** (`sim.*`, `physics.*`, `mmo`, `store.realtime`, `research-findings`) remain placement-deferred until P0 product repos are kit-complete.
- **Briefing gap:** `agent-briefing.json` omits `org_new_repos_discovery` — consume `data/latest/org-new-repos-discovery.json` directly.

## Deliverable / findings

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 35 |
| Known (CI + agent-kit audits + core list) | 35 |
| **New (not in known set)** | **0** |
| **Stale known (catalog ⊄ GitHub)** | **0** |

Preflight: `data/latest/org-new-repos-discovery.json`, `org-repo-ci-audit.json`, `org-agent-kit-audit.json`

### New repos (classification + handoffs)

*None.* `new_repos: []` · `new_repo_entries: []`

### In-flight onboarding (recently graduated — not net-new)

| Repo | Auto class | **Confirmed** | CI | Agent-kit | Recommended handoffs |
|------|------------|---------------|-----|-----------|----------------------|
| `lic-docs` | unclassified | **candidate_official** | ✓ `ci.yml` + `docs.yml` on `main` | `missing_local_clone` · no `.cursor/rules` on GitHub | `agent_kit_maintainer` → `docs_maintainer` → `package_architect` → `code_implementer` |

**`lic-docs` detail (GitHub):**

- Description: *Li language handbook (MkDocs)*
- Default branch: `main` · pushed `2026-05-30T09:56Z`
- Workflows: `ci.yml`, `docs.yml` (CI audit: `status: ok`)
- No agent-kit stamp; no sibling clone under `../lic-docs`

**Onboarding plan (`lic-docs` — downstream agents only):**

| Step | Agent | Action | Notes |
|------|-------|--------|-------|
| 1 | `ci_maintainer` | `verify_ci_yml` | Already on `main` — confirm audit row, no new PR |
| 2 | `agent_kit_maintainer` | `sync_agent_kit` | Isolated clone; install `1.3.5+6018e18bf2ed91f4` |
| 3 | `docs_maintainer` | `live_docs_smoke` | MkDocs + Pages deploy |
| 4 | `package_architect` | `placement_review` | Official handbook PKG vs `lic/docs` overlap |
| 5 | `code_implementer` | `register_in_catalog` | **After** kit + placement — do not catalog early |

### Agent-kit backlog (known repos — primary handoff surface)

| Repo | Confirmed class | Agent-kit status | Recommended handoffs |
|------|-----------------|------------------|----------------------|
| `studio` | core_tooling | `missing_kit` | `agent_kit_maintainer` → `docs_maintainer` → `code_implementer` |
| `studio.ai` | core_tooling | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `ui` | core_tooling | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `sim` | core_tooling | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `render` | core_tooling | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `world` | core_tooling | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `proof-library` | core_tooling | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `li-local-ci` | core_tooling | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `lidb` | candidate_official | `missing_kit` | `agent_kit_maintainer` → `package_architect` → `code_implementer` |
| `net.httpd` | official_mirror | `missing_kit` | `agent_kit_maintainer` → `ci_maintainer` (verify) |
| `li-gui` | candidate_official | `missing_kit` | `agent_kit_maintainer` → `package_architect` |
| `store.realtime` | unclassified | `missing_kit` | `agent_kit_maintainer` → **`package_architect` (P0)** |
| `sim.*` / `physics.*` / `mmo` / `research-findings` | unclassified (vertical) | `missing_kit` | `agent_kit_maintainer` → `package_architect` |

**Agent-kit OK (13):** `benchmarks`, `li-cursor-agents`, `li-demo`, `li-httpd`, `li-language`, `li-net`, `li-std-core`, `li-std-math`, `lic`, `lip`, `lis`, `lit`, `roadmap`

### Stale catalog entries

*None.* `stale_known_repos: []`. No archive/delete candidates this cycle — do not remove catalog rows without human approval.

### Handoff queue (control plane)

**`org_repo_onboarding` — P0 (in-flight `lic-docs`, enqueue first):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `lic-docs` | `sync_agent_kit` | easy — **isolated clone first** |
| `ci_maintainer` | `lic-docs` | `verify_ci_yml` | platform — confirm audit row only |
| `docs_maintainer` | `lic-docs` | `live_docs_smoke` | easy — MkDocs handbook |
| `package_architect` | `lic-docs` | `placement_review` | easy / provable — docs vs `lic` monorepo split |
| `code_implementer` | `lic-docs` | `register_in_catalog` | easy — **blocked until kit + placement** |

**P0 — product / platform hygiene (known repos):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `studio` | `sync_agent_kit` | easy / PH-GD |
| `agent_kit_maintainer` | `studio.ai` | `sync_agent_kit` | ai-first / PH-GD |
| `agent_kit_maintainer` | `ui` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `sim` | `sync_agent_kit` | scientific computing / PH-SIM |
| `agent_kit_maintainer` | `render` | `sync_agent_kit` | graphics / PH-GD |
| `agent_kit_maintainer` | `proof-library` | `sync_agent_kit` | provable |
| `agent_kit_maintainer` | `lidb` | `sync_agent_kit` | secure / PH-DB |
| `agent_kit_maintainer` | `net.httpd` | `sync_agent_kit` | secure / server mirror |
| `agent_kit_maintainer` | `li-local-ci` | `sync_agent_kit` | platform / CI tooling |
| `package_architect` | `lidb` | `placement_review` | secure — official PKG vs experimental |
| `package_architect` | `store.realtime` | `placement_review` | secure — realtime data plane |

**P1 — domain verticals + GUI:**

| agent_id | repo | action |
|----------|------|--------|
| `agent_kit_maintainer` | `world` | `sync_agent_kit` |
| `agent_kit_maintainer` | `li-gui` | `sync_agent_kit` |
| `agent_kit_maintainer` | `sim.robotics` | `sync_agent_kit` |
| `agent_kit_maintainer` | `sim.scientific` | `sync_agent_kit` |
| `agent_kit_maintainer` | `sim.additive` | `sync_agent_kit` |
| `agent_kit_maintainer` | `sim.automotive` | `sync_agent_kit` |
| `agent_kit_maintainer` | `sim.drug_design` | `sync_agent_kit` |
| `agent_kit_maintainer` | `physics.runtime` | `sync_agent_kit` |
| `agent_kit_maintainer` | `physics.custom` | `sync_agent_kit` |
| `agent_kit_maintainer` | `mmo` | `sync_agent_kit` |
| `agent_kit_maintainer` | `store.realtime` | `sync_agent_kit` |
| `agent_kit_maintainer` | `research-findings` | `sync_agent_kit` |

**Platform meta:**

| agent_id | repo | action |
|----------|------|--------|
| `org_repo_onboarder` | `benchmarks` | `embed_discovery_in_briefing` |

Downstream agents own isolated-clone PRs — onboarder does **not** open PRs or edit sibling trees.

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-------------------|--------|
| `lic-docs` | chore(agent-kit): sync canonical cursor rules (initial onboarding) | `agent-kit`, `docs`, `org-onboarding` |
| `lic-docs` | chore(docs): confirm Pages deploy + live docs smoke | `docs`, `surface:docs` |
| `studio` | chore(agent-kit): sync canonical cursor rules `1.3.5` | `agent-kit`, `PH-GD` |
| `studio.ai` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `ai-first` |
| `ui` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `platform` |
| `sim` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `PH-SIM` |
| `lidb` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `secure` |
| `proof-library` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `provable` |
| `li-gui` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `org-onboarding` |
| `benchmarks` | chore(preflight): embed `org_new_repos_discovery` in agent briefing | `platform` |
| `roadmap` | docs(ecosystem): record `lic-docs` placement decision | `platform`, `docs` |

## Deferred

- **`code_implementer` catalog registration** for `lic-docs` — blocked until agent-kit PR merged + `package_architect` placement recorded.
- **`ci_maintainer` `add_ci_yml`** for any repo — not needed; all audited repos have CI on `main`.
- **Catalog registration** for hygiene repos — blocked until agent-kit stamp green.
- **Stale catalog pruning** — none (`stale_count=0`).
- **Bulk `sim.*` / `physics.*` placement** — defer `package_architect` until P0 product repos kit-complete.
- **Merge program / PR opener** — out of scope (`--skip-slow` briefing).
- **Self-merge / sibling-tree edits** — explicitly out of scope.
