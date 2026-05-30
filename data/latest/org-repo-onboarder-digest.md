# Org repo onboarder digest — 2026-05-30T1015Z

**Agent:** `org_repo_onboarder` · **Source:** proactive · discovery `2026-05-30T10:15Z` · CI audit `2026-05-30T10:14Z` · agent-kit audit `2026-05-30T10:15Z` · briefing `2026-05-30T10:03Z`

## Executive summary

- **Discovery (refreshed):** `github=35` `known=35` **`new=0`** **`stale=0`** via `gh_repo_list` — GitHub org and catalog/audit known set are in sync.
- **No net-new repos** — `new_repo_entries` is empty; do not add catalog rows without CI + agent-kit path.
- **CI audit complete:** **0** repos missing `ci.yml` on default branch (`repos_missing_ci: []`); `research-findings` exempt; `li-cursor-agents` excluded per `org_repos.IGNORE_REPOS`.
- **Agent-kit hygiene:** **30** repos missing or drifted (**3 drift:** `lic`, `lis`, `roadmap`; **27 missing_kit**); **4 OK:** `benchmarks`, `li-cursor-agents`, `lip`, `lit`; `lic-docs` = `missing_local_clone` (no sibling checkout).
- **Highest-risk unclassified (next `new_repos` cycle):** `lidb`, `lic-docs`, `net.httpd`, `store.realtime` — placement/CI ambiguity before catalog registration.
- **Live docs gap:** **8** repos without live Pages (`li-demo`, `li-httpd`, `li-net`, `li-std-core`, `li-std-math`, `lip`, `lis`, `lit`) — `docs_maintainer` heap, not onboarder-owned.
- **North star:** platform hygiene → **provable** (`lic`, `lit`, `proof-library`), **easy** (`lic-docs`, `studio`), **secure** (`li-httpd`, `li-net`, `lidb`) — no perf/catalog work ahead of proof gates.
- **Briefing gap:** `agent-briefing.json` does not embed `org_new_repos_discovery` — read `data/latest/org-new-repos-discovery.json` directly.

## Deliverable / findings

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 35 |
| Known (catalog + audits) | 35 |
| **New** | **0** |
| **Stale known** | **0** |

Preflight: `data/latest/org-new-repos-discovery.json`, `org-repo-ci-audit.json`, `org-agent-kit-audit.json`

### New repos (classification + handoffs)

*None this cycle.*

| Repo | Classification | Recommended handoffs |
|------|----------------|----------------------|
| — | — | — |

### Stale catalog entries

*None.* All 35 catalog-known repos exist on GitHub. No archive/delete without human approval.

### Catalog sync — reference classification (all 35 GitHub repos)

| Bucket | Repos |
|--------|-------|
| **core_tooling** | `lic`, `li-language`, `lip`, `lit`, `lis`, `benchmarks`, `roadmap`, `li-cursor-agents`, `li-local-ci` |
| **official_mirror** | `li-net`, `li-httpd`, `li-std-core`, `li-std-math`, `li-demo`, `net.httpd` |
| **candidate_official** | `li-gui`, `lidb`, `lic-docs` |
| **unclassified** (domain / product) | `studio`, `studio.ai`, `ui`, `render`, `sim`, `sim.*`, `physics.*`, `world`, `mmo`, `proof-library`, `store.realtime`, `research-findings` |

**Routing overrides:** `studio`, `studio.ai`, `ui`, `render`, `sim` are first-class product repos (PH-GD / PH-SIM) — treat as **core_tooling** for agent handoffs even though `classify_new_repo()` labels them `unclassified` when they appear in `new_repos`.

### Onboarding plan (existing repos — hygiene, no new-repo fan-out)

| Repo / scope | Agent | Action | Notes |
|--------------|-------|--------|-------|
| 30 repos (`repos_needing_sync`) | `agent_kit_maintainer` | `sync_agent_kit` | canonical `1.3.5+6018e18bf2ed91f4`; **drift:** `lic`/`lis`/`roadmap`, rest **missing_kit** |
| `lic-docs` | `agent_kit_maintainer` | `sync_agent_kit` | CI OK on GitHub; audit has no local clone |
| `lidb` | `ci_maintainer` | `wp_h0_main_default` | policy note WP-H0 — confirm default branch gate |
| 8 repos (ecosystem audit) | `docs_maintainer` | `live_docs_smoke` | `repos_without_live_docs` |
| All 35 | `org_repo_onboarder` | `refresh_discovery` | wire `org_new_repos_discovery` into `agent-briefing.py` |

Downstream agents own isolated-clone PRs — onboarder does **not** open PRs or edit sibling trees.

### Handoff queue (control plane)

**`org_repo_onboarding` (new repos):** *empty* — `new_repo_entries` is `[]`.

**Enqueue (platform hygiene — priority order):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `lic` | `sync_agent_kit` | provable — drift `1.3.3` → `1.3.5` |
| `agent_kit_maintainer` | `lis` | `sync_agent_kit` | provable — drift |
| `agent_kit_maintainer` | `roadmap` | `sync_agent_kit` | governance — drift |
| `agent_kit_maintainer` | `studio` | `sync_agent_kit` | easy / PH-GD |
| `agent_kit_maintainer` | `studio.ai` | `sync_agent_kit` | ai-first / PH-GD |
| `agent_kit_maintainer` | `ui` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `sim` | `sync_agent_kit` | scientific computing / PH-SIM |
| `agent_kit_maintainer` | `proof-library` | `sync_agent_kit` | provable |
| `agent_kit_maintainer` | `li-httpd` | `sync_agent_kit` | secure / server |
| `agent_kit_maintainer` | `li-net` | `sync_agent_kit` | secure |
| `agent_kit_maintainer` | `li-demo` | `sync_agent_kit` | platform templates |
| `agent_kit_maintainer` | `li-language` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `li-std-core` | `sync_agent_kit` | provable / std |
| `agent_kit_maintainer` | `li-std-math` | `sync_agent_kit` | provable / PH-2i |
| `agent_kit_maintainer` | `render` | `sync_agent_kit` | graphics / PH-GD |
| `agent_kit_maintainer` | `world` | `sync_agent_kit` | gaming / PH-GD |
| `agent_kit_maintainer` | `lic-docs` | `sync_agent_kit` | easy — handbook; clone + kit PR |
| `ci_maintainer` | `lidb` | `wp_h0_main_default` | platform / secure — PH-DB-0 default branch |
| `docs_maintainer` | `li-demo` | `live_docs_smoke` | easy — Pages handbook |
| `docs_maintainer` | `lip` | `live_docs_smoke` | ecosystem audit gap |
| `org_repo_onboarder` | `*` | `refresh_discovery` | embed discovery in briefing each preflight |

**If `new_repos` non-empty next cycle**, per-repo fan-out:

| agent_id | action |
|----------|--------|
| `ci_maintainer` | `add_ci_yml` |
| `agent_kit_maintainer` | `sync_agent_kit` |
| `docs_maintainer` | `live_docs_smoke` |
| `package_architect` | `placement_review` (unclassified / candidate_official) |
| `code_implementer` | `register_in_catalog` (after CI + kit) |

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-------------------|--------|
| `lidb` | WP-H0: set default branch to `main` before org CI gate | `platform`, `ci`, `PH-DB-0` |
| `lic` | chore(agent-kit): align cursor stamp to canonical `1.3.5` | `agent-kit`, `drift`, `provable` |
| `roadmap` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `governance` |
| `studio` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `PH-GD` |
| `proof-library` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `provable` |
| `lic-docs` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `docs` |
| `benchmarks` | chore(preflight): embed `org_new_repos_discovery` in agent briefing | `platform`, `agent-kit` |

## Deferred

- **Catalog registration** for any repo — blocked until it appears in `new_repos` with CI + agent-kit complete.
- **Stale catalog pruning** — none identified; no archive/delete without human sign-off.
- **Bulk agent-kit wave** — remaining `missing_kit` mirrors (`sim.*`, `physics.*`, `mmo`, `store.realtime`, `net.httpd`, etc.) after P0 drift + platform repos.
- **`docs_maintainer`** live Pages — separate heap task (8 repos); not onboarder-owned.
- **`li-cursor-agents`** — excluded from org CI sweep; kit already at canonical stamp.
- **Merge program / pr_branch_opener** — out of scope (`--skip-slow` briefing).
