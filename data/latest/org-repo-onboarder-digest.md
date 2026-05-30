# Org repo onboarder digest — 2026-05-30T14:06Z

**Agent:** `org_repo_onboarder` · **Source:** proactive · discovery `2026-05-30T14:06Z` · CI audit `2026-05-30T14:02Z` · agent-kit audit `2026-05-30T14:05Z` · briefing `2026-05-30T14:02Z`

## Executive summary

- **Discovery (refreshed):** `github=35` · audit-known `known=13` · **`new=22`** · **`stale=0`** (`gh_api_orgs_repos`).
- **“New” = not in CI/agent-kit audit known set** — all 22 repos already exist on GitHub with `main` default and **`ci.yml` present** (verified via `gh api`); bootstrap CI is not the blocker.
- **Agent-kit is the primary gap:** 22/22 new repos have `.cursor/rules` locally (where cloned) but **no canonical stamp** (`1.3.5+6018e18bf2ed91f4`); `lic-docs` has **no local clone**.
- **Highest-risk unclassified (placement + security):** `lidb`, `store.realtime`, `net.httpd`, `lic-docs` — data/realtime/http surface before catalog registration.
- **Product P0 (routing overrides → core_tooling):** `studio`, `studio.ai`, `ui`, `sim`, `render`, `world`, `proof-library` — PH-GD / PH-SIM / provable pillars.
- **Stale catalog:** none — no `stale_known_repos`; do not archive/delete without human approval.
- **North star fit:** platform hygiene unblocks **provable** (`proof-library`, `lit` path), **easy** (`studio`, `ui`, `lic-docs`), **secure** (`lidb`, `net.httpd`, `store.realtime`).
- **Briefing gap:** `agent-briefing.json` still omits `org_new_repos_discovery` — consume `data/latest/org-new-repos-discovery.json` directly.

## Deliverable / findings

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 35 |
| Known (CI + agent-kit audits + core list) | 13 |
| **New (not in known set)** | **22** |
| **Stale known (catalog ⊄ GitHub)** | **0** |

Preflight: `data/latest/org-new-repos-discovery.json`, `org-repo-ci-audit.json`, `org-agent-kit-audit.json`

### New repos (classification + handoffs)

Confirmed classifications apply **routing overrides** from `explore-li-ecosystem` where `classify_new_repo()` under-labels product repos.

| Repo | Auto class | **Confirmed** | CI on `main` | Agent-kit | Recommended handoffs |
|------|------------|---------------|:------------:|:---------:|----------------------|
| `li-gui` | candidate_official | candidate_official | ✓ | partial | `agent_kit_maintainer` → `package_architect` → `code_implementer` |
| `li-local-ci` | candidate_official | **core_tooling** | ✓ | partial | `agent_kit_maintainer` → `code_implementer` |
| `lic-docs` | unclassified | **candidate_official** | ✓ | no clone | clone → `agent_kit_maintainer` → `docs_maintainer` → `package_architect` |
| `lidb` | unclassified | **candidate_official** | ✓ | partial | `agent_kit_maintainer` → `package_architect` → `code_implementer` |
| `mmo` | unclassified | unclassified | ✓ | partial | `agent_kit_maintainer` → `package_architect` |
| `net.httpd` | unclassified | **official_mirror** | ✓ | partial | `agent_kit_maintainer` → `ci_maintainer` (audit only) |
| `physics.custom` | unclassified | unclassified | ✓ | partial | `agent_kit_maintainer` → `package_architect` |
| `physics.runtime` | unclassified | unclassified | ✓ | partial | `agent_kit_maintainer` → `package_architect` |
| `proof-library` | unclassified | **core_tooling** | ✓ | partial | `agent_kit_maintainer` → `code_implementer` |
| `render` | unclassified | **core_tooling** | ✓ | partial | `agent_kit_maintainer` → `code_implementer` |
| `research-findings` | unclassified | unclassified | ✓ | partial | `agent_kit_maintainer` (research exempt docs policy) |
| `sim` | unclassified | **core_tooling** | ✓ | partial | `agent_kit_maintainer` → `code_implementer` |
| `sim.additive` | unclassified | unclassified (vertical) | ✓ | partial | `agent_kit_maintainer` → `package_architect` |
| `sim.automotive` | unclassified | unclassified (vertical) | ✓ | partial | `agent_kit_maintainer` → `package_architect` |
| `sim.drug_design` | unclassified | unclassified (vertical) | ✓ | partial | `agent_kit_maintainer` → `package_architect` |
| `sim.robotics` | unclassified | unclassified (vertical) | ✓ | partial | `agent_kit_maintainer` → `package_architect` |
| `sim.scientific` | unclassified | unclassified (vertical) | ✓ | partial | `agent_kit_maintainer` → `package_architect` |
| `store.realtime` | unclassified | unclassified | ✓ | partial | `agent_kit_maintainer` → **`package_architect` (P0)** |
| `studio` | unclassified | **core_tooling** | ✓ | partial | `agent_kit_maintainer` → `docs_maintainer` → `code_implementer` |
| `studio.ai` | unclassified | **core_tooling** | ✓ | partial | `agent_kit_maintainer` → `code_implementer` |
| `ui` | unclassified | **core_tooling** | ✓ | partial | `agent_kit_maintainer` → `code_implementer` |
| `world` | unclassified | **core_tooling** | ✓ | partial | `agent_kit_maintainer` → `code_implementer` |

**Onboarding plan (per repo — downstream agents only):**

| Step | Agent | Action | When |
|------|-------|--------|------|
| 1 | `ci_maintainer` | `expand_audit_coverage` | CI already on GitHub — add repo to `org-repo-ci-audit` known set after smoke |
| 2 | `agent_kit_maintainer` | `sync_agent_kit` | **Now** — canonical `1.3.5+6018e18bf2ed91f4` |
| 3 | `docs_maintainer` | `live_docs_smoke` | After kit PR (most have `pages.yml`) |
| 4 | `package_architect` | `placement_review` | `unclassified` + `candidate_official` only |
| 5 | `code_implementer` | `register_in_catalog` | **After** steps 1–2 green — do not catalog early |

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
| `ci_maintainer` | `*` (22 new) | `expand_audit_coverage` | add to `org-repo-ci-audit` after verify |

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

**After kit + audit — catalog (blocked until CI audit lists repo):**

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

## Deferred

- **Catalog registration** for all 22 — blocked until agent-kit stamp + CI audit known-set expansion.
- **`ci_maintainer` `add_ci_yml`** — skipped; GitHub already has `ci.yml` on `main` for every new repo.
- **Stale catalog pruning** — none.
- **Bulk `sim.*` / `physics.*` placement** — defer `package_architect` until P0 product repos kit-complete.
- **Merge program / PR opener** — out of scope (`--skip-slow` briefing).
- **Self-merge / sibling-tree edits** — explicitly out of scope.
