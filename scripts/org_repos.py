"""Canonical li-langverse org repo lists (dynamic via `gh`).

All preflight / agent scripts should import from here — do not duplicate repo names.

Policy:
- **li-cursor-agents** — excluded from org sweeps (`IGNORE_REPOS`).
- **li-demo** — automation sandbox; no automated merges (`MERGE_IGNORE_REPOS`).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

ORG = os.environ.get("GH_ORG", "li-langverse")

# Local SDK / automation runner — not part of core product org loop.
IGNORE_REPOS = frozenset({"li-cursor-agents"})

# Automation/testing repo — no automated merge execution.
AUTOMATION_SANDBOX_REPOS = frozenset({"li-demo"})

MERGE_IGNORE_REPOS = IGNORE_REPOS | AUTOMATION_SANDBOX_REPOS

# Used when `gh` is missing or fails (keep in sync with org; last verified 2026-05-21).
FALLBACK_ORG_REPOS = [
    "benchmarks",
    "lic",
    "li-cursor-agents",
    "li-demo",
    "li-httpd",
    "li-language",
    "li-local-ci",
    "li-net",
    "lip",
    "lis",
    "li-std-core",
    "li-std-math",
    "lit",
    "roadmap",
]

# Populated by refresh_org_repos() / org_repos_for_*(); do not append in other modules.
ORG_REPOS: list[str] = []


def _gh_json(args: list[str]):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def list_org_repos() -> list[str]:
    """All non-archived repos in the org (includes li-cursor-agents, li-demo, li-local-ci)."""
    rows = _gh_json(["repo", "list", ORG, "--limit", "100", "--json", "name,isArchived"])
    if not rows:
        return list(FALLBACK_ORG_REPOS)
    return sorted(r["name"] for r in rows if not r.get("isArchived"))


def filter_repos(names: list[str]) -> list[str]:
    """Drop IGNORE_REPOS (e.g. li-cursor-agents)."""
    return [n for n in names if n not in IGNORE_REPOS]


def filter_merge_repos(names: list[str]) -> list[str]:
    """Drop repos that must not enter automated merge queue."""
    return [n for n in names if n not in MERGE_IGNORE_REPOS]


def org_repos_for_sweep() -> list[str]:
    """Product + infra repos agents should scan (issues, PRs, CI audits)."""
    return filter_repos(list_org_repos())


def org_repos_for_merge() -> list[str]:
    """Repos eligible for merge queue / run-pr-program execute."""
    return filter_merge_repos(list_org_repos())


def refresh_org_repos() -> list[str]:
    """Refresh module-level ORG_REPOS for legacy `from org_repos import ORG_REPOS`."""
    global ORG_REPOS
    ORG_REPOS = org_repos_for_sweep()
    return ORG_REPOS


def build_org_repos_catalog() -> dict:
    """Metadata for agent briefing — full org vs sweep vs merge subsets."""
    all_repos = list_org_repos()
    sweep = filter_repos(all_repos)
    merge_q = filter_merge_repos(all_repos)
    source = "gh" if _gh_json(["repo", "list", ORG, "--limit", "1", "--json", "name"]) else "fallback"
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "org": ORG,
        "source": source,
        "all_repos": all_repos,
        "sweep_repos": sweep,
        "merge_queue_repos": merge_q,
        "ignored_repos": sorted(IGNORE_REPOS),
        "merge_ignored_repos": sorted(MERGE_IGNORE_REPOS),
        "counts": {
            "all": len(all_repos),
            "sweep": len(sweep),
            "merge_queue": len(merge_q),
        },
    }


def without_ignored(*extra: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for r in list_org_repos() + list(extra):
        if r in IGNORE_REPOS or r in seen:
            continue
        seen.add(r)
        out.append(r)
    return out


def agent_kit_target_repos() -> list[str]:
    """Repos that should carry roadmap agent-kit (dynamic sweep set)."""
    return org_repos_for_sweep()


def core_agent_kit_repos() -> list[str]:
    """Alias for agent-kit audit targets."""
    return agent_kit_target_repos()


def run_self_test() -> int:
    all_repos = list_org_repos()
    sweep = org_repos_for_sweep()
    merge_q = org_repos_for_merge()
    assert "li-local-ci" in all_repos or "li-local-ci" in FALLBACK_ORG_REPOS, all_repos
    assert "li-cursor-agents" in all_repos
    assert "li-cursor-agents" not in sweep
    assert "li-demo" not in merge_q
    assert "lic" in sweep
    refresh_org_repos()
    assert ORG_REPOS == sweep
    cat = build_org_repos_catalog()
    assert cat["counts"]["sweep"] == len(sweep)
    print(f"org_repos self-test OK (all={len(all_repos)} sweep={len(sweep)} merge={len(merge_q)})")
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(run_self_test())
    cat = build_org_repos_catalog()
    print(json.dumps(cat, indent=2))
