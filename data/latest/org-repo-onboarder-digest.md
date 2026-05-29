# Org repo onboarder digest — 2026-05-29

**Source:** proactive sweep · briefing `2026-05-29T07:45Z` · discovery refreshed `2026-05-29T08:36Z`

## Executive summary

- **Discovery refreshed** via `scripts/discover-new-org-repos.py` (restored on branch; was missing from `chore/fix-nightly-macos-core`).
- **0 new** GitHub repos vs ecosystem known set; **0 stale** catalog entries (ghost repos).
- **33 / 33** non-archived org repos aligned between `gh repo list` and audit-derived `known_repos`.
- **No net-new onboarding handoffs** — all repos already in CI/kit/ecosystem audits; do not add catalog rows without CI + agent-kit path.
- **Highest platform risk (existing repos):** `lidb` gated on non-`main` default (`feat/ph-db-2-liorm-liq`); **28** repos missing/drifted agent-kit; **10** without live docs.
- **CI audit:** 31 repos OK on default branch; `lidb` WP-H0 gated; `research-findings` CI-exempt by policy.
- **Control plane:** `queued_agent_tasks` empty for this briefing hash — heap already routes `agent_kit_maintainer`, `ci_maintainer`, `docs_maintainer`.
- **North star:** No unclassified *new* repos; focus remains proof-first platform hygiene (kit → CI → docs → catalog).

## Deliverable / findings

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 33 |
| Known (audits + core list) | 33 |
| **New** | **0** |
| **Stale known** | **0** |

Preflight: `data/latest/org-new-repos-discovery.json`

### New repos (classification + handoffs)

*None this cycle.*

| Repo | Classification | Recommended handoffs |
|------|----------------|----------------------|
| — | — | — |

### Stale catalog entries

*None this cycle.* No archive/delete candidates without human approval.

### Catalog sync (all GitHub repos — reference)

| Bucket | Repos |
|--------|-------|
| **core_tooling** | `lic`, `li-language`, `lip`, `lit`, `lis`, `benchmarks`, `roadmap`, `li-cursor-agents` |
| **official_mirror** | `li-net`, `li-httpd`, `li-std-core`, `li-std-math`, `li-demo`, `net.httpd` |
| **candidate_official** | `li-gui`, `li-local-ci`, `lidb` |
| **unclassified** (domain packages) | `sim*`, `physics.*`, `render`, `studio`, `studio.ai`, `ui`, `world`, `mmo`, `store.realtime`, `research-findings` |

### Onboarding plan (existing repos — hygiene, not “new repo”)

Downstream agents own isolated clone PRs; onboarder does not open PRs.

| Repo | Agent | Action | Notes |
|------|-------|--------|-------|
| *28 repos* | `agent_kit_maintainer` | `sync_agent_kit` | See `org-agent-kit-audit.json` (`missing_kit` / `drift`) |
| `lidb` | `ci_maintainer` | `wp_h0_main_default` | Set default branch `main` before enforcing `ci.yml` on default |
| 10 repos | `docs_maintainer` | `live_docs_smoke` | `lic`, `lip`, `lit`, `lis`, `li-demo`, `li-httpd`, `li-net`, `li-std-*`, `roadmap` |
| `research-findings` | — | — | CI-exempt; optional docs only |

### Handoff queue (control plane)

**New-repo onboarding (`org_repo_onboarding`):** *empty* — `new_repo_entries` is `[]`.

**Related platform queue (existing heap / briefing — not onboarder-created):**

| agent_id | repo / scope | action |
|----------|--------------|--------|
| `agent_kit_maintainer` | 28 repos | `sync_agent_kit` |
| `ci_maintainer` | `lidb` | `wp_h0_main_default` |
| `docs_maintainer` | 10 repos | `live_docs_smoke` |
| `workspace_sweeper` | `lic` | dirty sibling sweep (4 safe files) |

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-----------------|--------|
| `lidb` | WP-H0: set default branch to `main` before org CI gate | `platform`, `ci` |
| `li-demo` | chore(agent-kit): sync roadmap cursor policy | `agent-kit`, `chore` |
| `li-httpd` | chore(agent-kit): sync roadmap cursor policy | `agent-kit`, `chore` |
| `li-std-core` | chore(agent-kit): sync roadmap cursor policy | `agent-kit`, `chore` |
| `li-std-math` | chore(agent-kit): sync roadmap cursor policy | `agent-kit`, `chore` |
| `lic` | chore(agent-kit): align cursor stamp to canonical | `agent-kit`, `drift` |
| `roadmap` | docs: enable GitHub Pages / live handbook smoke | `docs`, `platform` |

*(Several agent-kit PRs already open with failing CI — fix via `bug_fixer` / `ci_maintainer`, not onboarder self-merge.)*

## Deferred

- **Catalog pruning:** no stale entries; no archive/delete without human sign-off.
- **New repo catalog registration:** blocked until a repo appears in `new_repos` with CI + kit path complete.
- **Explorer / plan_audit / ci_bug_triage:** skipped in preflight (`--skip-slow`).
- **Merge program:** 74 open PRs — out of onboarder scope; merge coordinator owns sequence.

## Error (preflight)

Initial run failed: `scripts/discover-new-org-repos.py` absent on branch `chore/fix-nightly-macos-core` (present in commit `7393560`). **Recovered** by restoring script + briefing wiring; discovery re-run succeeded.
