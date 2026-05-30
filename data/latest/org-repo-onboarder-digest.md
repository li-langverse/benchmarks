# Org repo onboarder digest — 2026-05-30T0907Z

**Agent:** `org_repo_onboarder` · **Source:** proactive · discovery `2026-05-30T09:07Z` · CI audit `2026-05-30T09:03Z` · agent-kit audit `2026-05-30T09:03Z` · briefing `2026-05-30T08:04Z`

## Executive summary

- **Discovery (reconciled):** `github=35` `known=35` **`new=0`** **`stale=0`** via `gh_api_orgs_repos` (REST fallback after GraphQL `gh repo list` rate limit).
- **Script fix:** `discover-new-org-repos.py` now falls back to `gh api orgs/li-langverse/repos --paginate` before `fallback_core_list` — avoids false **`stale=22`** / **`new=0`** skew from 13-repo core list.
- **No net-new repos** — `new_repo_entries` is empty; do not add catalog rows without CI + agent-kit path.
- **Highest platform risk (existing):** **`lic-docs`** missing required `ci.yml` (docs-only workflow); **`lidb`** WP-H0 default-branch gate; **29** repos missing/drifted agent-kit (4 OK: `benchmarks`, `li-cursor-agents`, `lip`, `lit`).
- **Highest-risk unclassified (if they appear in `new_repos` next cycle):** `lidb`, `lic-docs`, `net.httpd`, `store.realtime` — placement/CI ambiguity before catalog registration.
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
| 29 repos (`repos_needing_sync`) | `agent_kit_maintainer` | `sync_agent_kit` | canonical `1.3.5+6018e18bf2ed91f4`; `lic`/`lis`/`roadmap` **drift**, rest **missing_kit** |
| `lic-docs` | `ci_maintainer` | `add_ci_yml` | only `docs.yml` today; template `lic/scripts/templates/github-repo/ci.yml` |
| `lidb` | `ci_maintainer` | `wp_h0_main_default` | WP-H0: default branch `main` before org CI gate on default |
| `lic-docs`, `li-gui` | `agent_kit_maintainer` | `sync_agent_kit` | `lic-docs` missing local clone in audit |
| 8 repos (briefing) | `docs_maintainer` | `live_docs_smoke` | `repos_without_live_docs` in ecosystem audit |
| All 35 | `org_repo_onboarder` | `refresh_discovery` | wire `org_new_repos_discovery` into `agent-briefing.py` |

Downstream agents own isolated-clone PRs — onboarder does **not** open PRs or edit sibling trees.

### Handoff queue (control plane)

**`org_repo_onboarding` (new repos):** *empty* — `new_repo_entries` is `[]`.

**Enqueue (platform hygiene — priority order):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `ci_maintainer` | `lic-docs` | `add_ci_yml` | platform / easy — handbook CI gate |
| `ci_maintainer` | `lidb` | `wp_h0_main_default` | platform / secure — PH-DB-0 default branch |
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
| `docs_maintainer` | `li-demo` | `live_docs_smoke` | 8 repos without live Pages (heap) |
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
| `lic-docs` | chore(ci): add required `ci.yml` for org CI policy | `platform`, `ci`, `docs` |
| `lidb` | WP-H0: set default branch to `main` before org CI gate | `platform`, `ci`, `PH-DB-0` |
| `lic` | chore(agent-kit): align cursor stamp to canonical `1.3.5` | `agent-kit`, `drift`, `provable` |
| `roadmap` | chore(agent-kit): sync canonical cursor rules | `agent-kit`, `governance` |
| `studio` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `PH-GD` |
| `proof-library` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `provable` |
| `benchmarks` | chore(preflight): embed `org_new_repos_discovery` in agent briefing | `platform`, `agent-kit` |

## Deferred

- **Catalog registration** for any repo — blocked until it appears in `new_repos` with CI + agent-kit complete.
- **Stale catalog pruning** — none identified; no archive/delete without human sign-off.
- **Bulk agent-kit wave** — remaining `missing_kit` mirrors (`sim.*`, `physics.*`, `mmo`, `store.realtime`, etc.) after P0 drift + platform repos.
- **`docs_maintainer`** live Pages — separate heap task (8 repos); not onboarder-owned.
- **Merge program / pr_branch_opener** — out of scope (`--skip-slow` briefing).
- **False discovery from `fallback_core_list`** — mitigated by REST fallback; do not enqueue stale=22 handoffs from old runs.
