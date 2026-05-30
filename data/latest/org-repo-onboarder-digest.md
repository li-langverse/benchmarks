# Org repo onboarder digest — 2026-05-30T14:51Z

**Agent:** `org_repo_onboarder` · **Source:** proactive · discovery `2026-05-30T14:51Z` · CI audit `2026-05-30T14:32Z` · agent-kit audit `2026-05-30T14:46Z` · briefing `2026-05-30T14:02Z`

## Executive summary

- **Discovery (refreshed):** `github=35` · `known=35` · **`new=0`** · **`stale=0`** (`gh_repo_list`) — org catalog / audit known set matches GitHub.
- **No net-new repos** this cycle; onboarding focus shifts to **agent-kit hygiene** on repos already in the known set.
- **Agent-kit gap:** **21** repos with `missing_kit` (no canonical stamp `1.3.5+6018e18bf2ed91f4`); **`lic-docs`** has no local clone (`missing_local_clone`).
- **CI audit blocked:** `org-repo-ci-audit.json` hit **GitHub API rate limit** — **33** repos `audit_incomplete`; only `research-findings` verified (`exempt`). Do not treat empty workflow lists as missing CI.
- **Ecosystem audit (briefing):** `repos_missing_ci_main=0` — prior green signal still holds; re-run CI audit after rate limit reset.
- **Highest-risk hygiene (placement + security):** `lidb`, `store.realtime`, `net.httpd`, `lic-docs` — data/realtime/http/docs surface.
- **Product P0 (routing → core_tooling):** `studio`, `studio.ai`, `ui`, `sim`, `render`, `world`, `proof-library`.
- **North star fit:** platform hygiene unblocks **provable** (`proof-library`), **easy** (`studio`, `ui`, `lic-docs`), **secure** (`lidb`, `net.httpd`, `store.realtime`).
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

*None.* `new_repos: []`, `new_repo_entries: []`.

All 35 GitHub repos are in `known_repos`. Remaining work is **onboarding hygiene** (agent-kit, CI audit refresh, placement) — not discovery.

### Agent-kit backlog (known repos — primary handoff surface)

| Repo | Auto class | **Confirmed** | Agent-kit status | Recommended handoffs |
|------|------------|---------------|------------------|----------------------|
| `studio` | unclassified | **core_tooling** | `missing_kit` | `agent_kit_maintainer` → `docs_maintainer` → `code_implementer` |
| `studio.ai` | unclassified | **core_tooling** | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `ui` | unclassified | **core_tooling** | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `sim` | unclassified | **core_tooling** | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `render` | unclassified | **core_tooling** | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `world` | unclassified | **core_tooling** | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `proof-library` | unclassified | **core_tooling** | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `li-local-ci` | candidate_official | **core_tooling** | `missing_kit` | `agent_kit_maintainer` → `code_implementer` |
| `lidb` | unclassified | **candidate_official** | `missing_kit` | `agent_kit_maintainer` → `package_architect` → `code_implementer` |
| `lic-docs` | unclassified | **candidate_official** | `missing_local_clone` | clone → `agent_kit_maintainer` → `docs_maintainer` → `package_architect` |
| `net.httpd` | unclassified | **official_mirror** | `missing_kit` | `agent_kit_maintainer` → `ci_maintainer` (verify only) |
| `li-gui` | candidate_official | candidate_official | `missing_kit` | `agent_kit_maintainer` → `package_architect` |
| `store.realtime` | unclassified | unclassified | `missing_kit` | `agent_kit_maintainer` → **`package_architect` (P0)** |
| `sim.additive` | unclassified | unclassified (vertical) | `missing_kit` | `agent_kit_maintainer` → `package_architect` |
| `sim.automotive` | unclassified | unclassified (vertical) | `missing_kit` | `agent_kit_maintainer` → `package_architect` |
| `sim.drug_design` | unclassified | unclassified (vertical) | `missing_kit` | `agent_kit_maintainer` → `package_architect` |
| `sim.robotics` | unclassified | unclassified (vertical) | `missing_kit` | `agent_kit_maintainer` → `package_architect` |
| `sim.scientific` | unclassified | unclassified (vertical) | `missing_kit` | `agent_kit_maintainer` → `package_architect` |
| `physics.custom` | unclassified | unclassified | `missing_kit` | `agent_kit_maintainer` → `package_architect` |
| `physics.runtime` | unclassified | unclassified | `missing_kit` | `agent_kit_maintainer` → `package_architect` |
| `mmo` | unclassified | unclassified | `missing_kit` | `agent_kit_maintainer` → `package_architect` |
| `research-findings` | unclassified | unclassified | `missing_kit` | `agent_kit_maintainer` (research exempt CI policy) |

**Agent-kit OK (13):** `benchmarks`, `li-cursor-agents`, `li-demo`, `li-httpd`, `li-language`, `li-net`, `li-std-core`, `li-std-math`, `lic`, `lip`, `lis`, `lit`, `roadmap`

**Onboarding plan (hygiene repos — downstream agents only):**

| Step | Agent | Action | When |
|------|-------|--------|------|
| 1 | `agent_kit_maintainer` | `sync_agent_kit` | **Now** — canonical `1.3.5+6018e18bf2ed91f4` |
| 2 | `ci_maintainer` | `refresh_ci_audit` | After GitHub rate limit reset — do not infer CI gaps from incomplete audit |
| 3 | `docs_maintainer` | `live_docs_smoke` | After kit PR (where `pages.yml` exists) |
| 4 | `package_architect` | `placement_review` | `unclassified` + `candidate_official` only |
| 5 | `code_implementer` | `register_in_catalog` | **After** kit + CI audit green — do not catalog early |

### Stale catalog entries

*None.* `stale_known_repos: []`. No archive/delete candidates this cycle.

### Handoff queue (control plane)

**`org_repo_onboarding` — P0 (enqueue first):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `studio` | `sync_agent_kit` | easy / PH-GD |
| `agent_kit_maintainer` | `studio.ai` | `sync_agent_kit` | ai-first / PH-GD |
| `agent_kit_maintainer` | `ui` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `sim` | `sync_agent_kit` | scientific computing / PH-SIM |
| `agent_kit_maintainer` | `render` | `sync_agent_kit` | graphics / PH-GD |
| `agent_kit_maintainer` | `proof-library` | `sync_agent_kit` | provable |
| `agent_kit_maintainer` | `lidb` | `sync_agent_kit` | secure / PH-DB |
| `agent_kit_maintainer` | `lic-docs` | `sync_agent_kit` | easy — **clone first** |
| `agent_kit_maintainer` | `net.httpd` | `sync_agent_kit` | secure / server mirror |
| `agent_kit_maintainer` | `li-local-ci` | `sync_agent_kit` | platform / CI tooling |
| `package_architect` | `lidb` | `placement_review` | secure — official PKG vs experimental |
| `package_architect` | `store.realtime` | `placement_review` | secure — realtime data plane |
| `package_architect` | `lic-docs` | `placement_review` | easy — docs vs lic monorepo split |
| `ci_maintainer` | `benchmarks` | `refresh_ci_audit` | re-run `org-repo-ci-audit` after rate limit |

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

**After kit + CI audit — catalog (blocked until gates green):**

| agent_id | repo | action |
|----------|------|--------|
| `code_implementer` | `studio` | `register_in_catalog` |
| `code_implementer` | `ui` | `register_in_catalog` |
| `code_implementer` | `sim` | `register_in_catalog` |
| `code_implementer` | `render` | `register_in_catalog` |
| `code_implementer` | `proof-library` | `register_in_catalog` |
| `docs_maintainer` | `studio` | `live_docs_smoke` |

| agent_id | repo | action |
|----------|------|--------|
| `org_repo_onboarder` | `benchmarks` | `embed_discovery_in_briefing` |

Downstream agents own isolated-clone PRs — onboarder does **not** open PRs or edit sibling trees.

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-------------------|--------|
| `studio` | chore(agent-kit): sync canonical cursor rules `1.3.5` | `agent-kit`, `PH-GD` |
| `studio.ai` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `ai-first` |
| `ui` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `platform` |
| `sim` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `PH-SIM` |
| `lidb` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `secure` |
| `lic-docs` | chore(agent-kit): sync canonical cursor rules (initial clone) | `agent-kit`, `docs` |
| `net.httpd` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `server` |
| `proof-library` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `provable` |
| `benchmarks` | chore(preflight): embed `org_new_repos_discovery` in agent briefing | `platform` |
| `benchmarks` | chore(ci-audit): re-run org-repo-ci-audit after GH rate limit | `platform`, `ci` |

## Deferred

- **Net-new repo onboarding** — none (`new_count=0`).
- **Catalog registration** for hygiene repos — blocked until agent-kit stamp + CI audit refresh.
- **`ci_maintainer` `add_ci_yml`** — not indicated; ecosystem audit reports `repos_missing_ci_main=0`.
- **Stale catalog pruning** — none.
- **Bulk `sim.*` / `physics.*` placement** — defer `package_architect` until P0 product repos kit-complete.
- **CI audit conclusions** while rate-limited — defer until `org-repo-ci-audit` re-run succeeds.
- **Merge program / PR opener** — out of scope (`--skip-slow` briefing).
- **Self-merge / sibling-tree edits** — explicitly out of scope.
