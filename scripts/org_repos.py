"""Canonical li-langverse org repo lists.

Policy:
- **li-cursor-agents** — excluded from org sweeps until re-enabled.
- **li-demo** — automation sandbox; no automated merges unless user asks.
"""
from __future__ import annotations

# Local SDK / automation runner — not part of core product org loop.
IGNORE_REPOS = frozenset({"li-cursor-agents"})

# No required ci.yml on default branch (research archive). See repo-ci-required.md.
CI_EXEMPT_REPOS = IGNORE_REPOS | frozenset({"research-findings"})

# Automation/testing repo (workflows, gate experiments) — not product merge queue.
AUTOMATION_SANDBOX_REPOS = frozenset({"li-demo"})

# Skip in run-pr-program --execute and auto-merge sweeps.
MERGE_IGNORE_REPOS = IGNORE_REPOS | AUTOMATION_SANDBOX_REPOS

# Primary repos for merge queue, triage, hygiene, security sweep.
ORG_REPOS = [
    "lic",
    "lip",
    "lit",
    "lis",
    "benchmarks",
    "roadmap",
    "li-net",
    "li-httpd",
    "li-std-core",
    "li-std-math",
    "li-demo",
    "li-language",
]

# Package mirrors + core (agent-kit sync targets).
CORE_AGENT_KIT_REPOS = [r for r in ORG_REPOS if r not in IGNORE_REPOS]


def filter_repos(names: list[str]) -> list[str]:
    return [n for n in names if n not in IGNORE_REPOS]


def filter_merge_repos(names: list[str]) -> list[str]:
    return [n for n in names if n not in MERGE_IGNORE_REPOS]


def without_ignored(*extra: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for r in list(ORG_REPOS) + list(extra):
        if r in IGNORE_REPOS or r in seen:
            continue
        seen.add(r)
        out.append(r)
    return out
