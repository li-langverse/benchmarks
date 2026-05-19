"""Canonical li-langverse org repo lists.

Policy: **li-cursor-agents** is excluded from org sweeps, CI audit, PR program,
and agent-kit enforcement until re-enabled explicitly.
"""
from __future__ import annotations

# Local SDK / automation runner — not part of core product org loop.
IGNORE_REPOS = frozenset({"li-cursor-agents"})

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


def without_ignored(*extra: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for r in list(ORG_REPOS) + list(extra):
        if r in IGNORE_REPOS or r in seen:
            continue
        seen.add(r)
        out.append(r)
    return out
