# Org repo onboarder digest — 2026-05-30T0735Z

**Agent:** `org_repo_onboarder` · **Source:** proactive · discovery `2026-05-30T07:35Z` (reconciled) · CI audit `2026-05-30T07:32Z` · agent-kit audit `2026-05-30T07:31Z` · briefing `2026-05-30T07:06Z`

## Executive summary

- **Discovery (reconciled):** `github=35` `known=35` **`new=0`** **`stale=0`** — full org list via `gh api orgs/li-langverse/repos`; matches catalog/briefing known set from prior cycle.
- **Error (preflight):** `python3 scripts/discover-new-org-repos.py` initially returned **`new=22`** because `gh repo list` hit **GraphQL rate limit** → `fallback_core_list` (13 repos) and **incomplete** `org-repo-ci-audit.json` / `org-agent-kit-audit.json` (local-only 12-repo sweep). Do not enqueue `org_repo_onboarding` from that raw output.
- **No net-new repos** — empty `new_repo_entries`; do not add catalog rows without CI + agent-kit path.
- **Highest platform risk (existing):** `lidb` non-`main` default (WP-H0); **`lic-docs`** handbook repo (docs workflow; verify `ci.yml` gate); **9** repos missing/drifted agent-kit in briefing vs **12** in local audit scope.
- **Highest-risk unclassified (if ever in `new_repos`):** `lidb`, `lic-docs`, `net.httpd`, `store.realtime` — placement/CI ambiguity before catalog registration.
- **CI audit this run:** incomplete (`repos_ok` empty — rate limit); policy still gates `lidb` default branch.
- **Agent-kit:** **3** OK locally (`benchmarks`, `lip`, `lit`); **9** needing sync in briefing (`lic`, `lis`, `roadmap` drift + 6 `missing_kit`); remote repos need `ensure-org-agent-kit.py` without `--local-only` when quota resets.
- **North star:** platform hygiene → **provable** (`lic`, `lit`, `proof-library`), **easy** (`lic-docs`, `studio`), **secure** (`li-httpd`, `li-net`, `lidb`) — no perf/catalog work ahead of proof gates.

## Deliverable / findings

### Error

```
python3 scripts/discover-new-org-repos.py
→ github_source=fallback_core_list, github_count=13, new_count=22 (FALSE POSITIVE)

gh repo list li-langverse
→ GraphQL: API rate limit already exceeded for user ID …
```

**Mitigation used:** `gh api orgs/li-langverse/repos --paginate` (REST) + reconcile `known_repos` against prior discovery (`24ca4b4`, 35 repos). Wrote reconciled `data/latest/org-new-repos-discovery.json`.

Restored `scripts/discover-new-org-repos.py` from git `1b947b6` (was missing on current branch).

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 35 |
| Known (catalog + audits) | 35 |
| **New** | **0** |
| **Stale known** | **0** |

Preflight: `data/latest/org-new-repos-discovery.json`, `org-repo-ci-audit.json`, `org-agent-kit-audit.json`

Briefing `agent-briefing.json` does **not** embed `org_new_repos_discovery` yet — read discovery JSON directly.

### New repos (classification + handoffs)

*None this cycle.*

| Repo | Classification | Recommended handoffs |
|------|----------------|----------------------|
| — | — | — |

### Stale catalog entries

*None.* No archive/delete without human approval.

### Catalog sync — reference classification (all 35 GitHub repos)

| Bucket | Repos |
|--------|-------|
| **core_tooling** | `lic`, `li-language`, `lip`, `lit`, `lis`, `benchmarks`, `roadmap`, `li-cursor-agents`, `li-local-ci`, `lic-docs` |
| **official_mirror** | `li-net`, `li-httpd`, `li-std-core`, `li-std-math`, `li-demo`, `net.httpd` |
| **candidate_official** | `li-gui`, `lidb` |
| **unclassified** (domain / product) | `studio`, `studio.ai`, `ui`, `render`, `sim`, `sim.*`, `physics.*`, `world`, `mmo`, `proof-library`, `store.realtime`, `research-findings` |

**Confirmed overrides (routing table):** `studio`, `ui`, `render`, `sim`, `studio.ai` are first-class product repos (PH-GD / PH-SIM) — treat as **core_tooling** for handoffs even though `classify_new_repo()` labels them `unclassified` when they appear in `new_repos`.

### Onboarding plan (existing repos — hygiene)

| Repo / scope | Agent | Action | Notes |
|--------------|-------|--------|-------|
| 9 repos (briefing) | `agent_kit_maintainer` | `sync_agent_kit` | `lic`, `lis`, `roadmap` drift; mirrors `missing_kit` |
| `lidb` | `ci_maintainer` | `wp_h0_main_default` | WP-H0: default branch `main` before `ci.yml` on default |
| `lic-docs` | `ci_maintainer` | `add_ci_yml` | MkDocs handbook; verify org CI gate |
| `lic-docs`, `li-gui` | `agent_kit_maintainer` | `sync_agent_kit` | clone workspace if `missing_local_clone` |
| All 35 (when quota OK) | `agent_kit_maintainer` | `sync_agent_kit` | Re-run `ensure-org-agent-kit.py` (remote audit) |
| `research-findings` | — | optional kit/docs | CI-exempt per policy |

Downstream agents own isolated-clone PRs — onboarder does **not** open PRs or edit sibling trees.

### Handoff queue (control plane)

**`org_repo_onboarding` (new repos):** *empty* — `new_repo_entries` is `[]`.

**Enqueue (platform hygiene):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `ci_maintainer` | `lidb` | `wp_h0_main_default` | platform / secure — PH-DB-0 default branch |
| `ci_maintainer` | `lic-docs` | `add_ci_yml` | platform / easy — handbook CI gate |
| `agent_kit_maintainer` | `lic` | `sync_agent_kit` | provable — drift vs canonical `1.3.5+6018e18bf2ed91f4` |
| `agent_kit_maintainer` | `lis` | `sync_agent_kit` | provable — drift |
| `agent_kit_maintainer` | `roadmap` | `sync_agent_kit` | governance — drift |
| `agent_kit_maintainer` | `li-demo` | `sync_agent_kit` | platform |
| `agent_kit_maintainer` | `li-httpd` | `sync_agent_kit` | secure / server |
| `agent_kit_maintainer` | `li-language` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `li-net` | `sync_agent_kit` | secure |
| `agent_kit_maintainer` | `li-std-core` | `sync_agent_kit` | provable / std |
| `agent_kit_maintainer` | `li-std-math` | `sync_agent_kit` | provable / PH-2i |
| `agent_kit_maintainer` | `proof-library` | `sync_agent_kit` | provable |
| `agent_kit_maintainer` | `studio` | `sync_agent_kit` | easy / PH-GD |
| `agent_kit_maintainer` | `ui` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `sim` | `sync_agent_kit` | scientific computing |
| `org_repo_onboarder` | `*` | `refresh_discovery` | Re-run discovery when `gh` quota resets; wire into `agent-briefing.py` |

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
| `lic-docs` | chore(ci): add required `ci.yml` for org CI policy | `platform`, `ci`, `docs` |
| `lic` | chore(agent-kit): align cursor stamp to canonical | `agent-kit`, `drift`, `provable` |
| `proof-library` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `provable` |
| `studio` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `PH-GD` |
| `benchmarks` | chore(preflight): wire `discover-new-org-repos.py` into `agent-briefing.py` | `platform`, `agent-kit` |

## Deferred

- **Catalog registration** for any repo — blocked until it appears in `new_repos` with CI + agent-kit complete.
- **Stale catalog pruning** — none identified; no archive/delete without human sign-off.
- **False `new=22` handoffs** — do not enqueue from rate-limited discovery run.
- **Full org CI / agent-kit remote audit** — retry when GitHub API quota resets.
- **`docs_maintainer`** — 10 repos without live Pages (heap); separate from onboarder.
- **Merge program / pr_branch_opener** — out of scope (132 branches per briefing; `--skip-slow`).
