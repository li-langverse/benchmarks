# Org repo onboarder digest — 2026-05-29

**Source:** proactive sweep · briefing `2026-05-29T12:27Z` · discovery refreshed `2026-05-29T12:45Z`

## Executive summary

- **Discovery refreshed** via `scripts/discover-new-org-repos.py` → `github=33 known=33 new=0 stale=0`.
- **0 new** GitHub repos vs ecosystem known set; **0 stale** catalog entries (no ghost/archive candidates).
- **33 / 33** non-archived org repos aligned between `gh repo list` and audit-derived `known_repos`.
- **No net-new onboarding handoffs** — do not add catalog rows without CI + agent-kit path.
- **Highest platform risk (existing repos):** `lidb` gated on non-`main` default (`feat/ph-db-2-liorm-liq`); **28** repos missing/drifted agent-kit (canonical `1.3.5+6018e18bf2ed91f4`); **10** without live docs.
- **CI audit:** 31 repos OK on default branch; `lidb` WP-H0 gated; `research-findings` CI-exempt (ecosystem-audit still lists it under `missing_ci_on_main` — policy mismatch only).
- **No unclassified *new* repos** — highest-risk bucket is dormant only if a repo appears in `new_repos` without `package_architect` placement.
- **Control plane:** heap already enqueues `agent_kit_maintainer`, `ci_maintainer`, `docs_maintainer` for briefing `e5fad788e09b81ca`; **no** `org_repo_onboarding` rows (empty `new_repo_entries`).

## Deliverable / findings

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 33 |
| Known (audits + core list) | 33 |
| **New** | **0** |
| **Stale known** | **0** |

Preflight: `data/latest/org-new-repos-discovery.json`, `org-repo-ci-audit.json`, `org-agent-kit-audit.json`

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
| *28 repos* | `agent_kit_maintainer` | `sync_agent_kit` | 25 `missing_kit`, 3 `drift` (`lic`, `lis`, `roadmap`); see `org-agent-kit-audit.json` |
| `lidb` | `ci_maintainer` | `wp_h0_main_default` | Set default branch `main` before enforcing `ci.yml` on default |
| 10 repos | `docs_maintainer` | `live_docs_smoke` | `lic`, `lip`, `lit`, `lis`, `li-demo`, `li-httpd`, `li-net`, `li-std-*`, `roadmap` |
| `li-gui` | `agent_kit_maintainer` | `sync_agent_kit` | No local clone in audit workspace — clone before kit PR |
| `research-findings` | — | — | CI-exempt; optional docs / kit only |

### Handoff queue (control plane)

**New-repo onboarding (`org_repo_onboarding`):** *empty* — `new_repo_entries` is `[]`.

**Related platform queue (briefing `e5fad788e09b81ca` — not onboarder-created):**

| agent_id | repo / scope | action |
|----------|--------------|--------|
| `agent_kit_maintainer` | 28 repos (heap + per-repo fingerprints) | `sync_agent_kit` |
| `agent_kit_maintainer` | `lic` | `sync_agent_kit` (drift) |
| `ci_maintainer` | `lidb` | `wp_h0_main_default` |
| `docs_maintainer` | 10 repos | `live_docs_smoke` |
| `workspace_sweeper` | `lic`, `benchmarks` | dirty sibling sweep |

**If a repo appears in `new_repos` next cycle**, enqueue per `onboarding_steps_for_repo`:

| agent_id | action |
|----------|--------|
| `ci_maintainer` | `add_ci_yml` |
| `agent_kit_maintainer` | `sync_agent_kit` |
| `docs_maintainer` | `live_docs_smoke` |
| `package_architect` | `placement_review` (if `unclassified` or `candidate_official`) |
| `code_implementer` | `register_in_catalog` (after CI + kit) |

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-----------------|--------|
| `lidb` | WP-H0: set default branch to `main` before org CI gate | `platform`, `ci` |
| `li-demo` | chore(agent-kit): sync roadmap cursor policy | `agent-kit`, `chore` |
| `li-httpd` | chore(agent-kit): sync roadmap cursor policy | `agent-kit`, `chore` |
| `studio` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `chore` |
| `sim` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `chore` |
| `lic` | chore(agent-kit): align cursor stamp to canonical | `agent-kit`, `drift` |
| `roadmap` | docs: enable GitHub Pages / live handbook smoke | `docs`, `platform` |

*(Several agent-kit PRs already open with failing CI — fix via `bug_fixer` / `ci_maintainer`, not onboarder self-merge.)*

## Deferred

- **Catalog pruning:** no stale entries; no archive/delete without human sign-off.
- **New repo catalog registration:** blocked until a repo appears in `new_repos` with CI + kit path complete.
- **Explorer / plan_audit / ci_bug_triage:** skipped in preflight (`--skip-slow`).
- **Merge program:** 95 open PRs / 36 failed CI — out of onboarder scope.
- **`li-gui`:** audit incomplete locally (`missing_local_clone`); kit sync deferred until workspace clone exists.

## Error

None this cycle. Preflight `org_agent_kit_audit` exited non-zero (28 repos needing sync) — expected signal, not a discovery failure.
