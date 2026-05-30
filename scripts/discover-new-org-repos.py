#!/usr/bin/env python3
"""Discover GitHub org repos not yet in the ecosystem catalog / briefing known set.

Writes data/latest/org-new-repos-discovery.json

Usage:
  python3 scripts/discover-new-org-repos.py
  python3 scripts/discover-new-org-repos.py --fixture-github /path/github.json --fixture-known /path/known.json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/org-new-repos-discovery.json"
ORG = os.environ.get("GH_ORG", "li-langverse")

CORE_AGENT_KIT_REPOS = [
    "lic",
    "li-language",
    "lip",
    "lit",
    "lis",
    "benchmarks",
    "roadmap",
    "li-cursor-agents",
    "li-net",
    "li-httpd",
    "li-std-core",
    "li-std-math",
    "li-demo",
]

ORG_MIRROR_REPOS = [
    "li-net",
    "li-httpd",
    "li-std-core",
    "li-std-math",
    "li-demo",
]


def gh_json(args: list[str]) -> list[dict] | dict | None:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def list_github_repos() -> tuple[list[str], str]:
    rows = gh_json(["repo", "list", ORG, "--limit", "100", "--json", "name,isArchived"])
    if not rows:
        return CORE_AGENT_KIT_REPOS, "fallback_core_list"
    names = sorted(r["name"] for r in rows if not r.get("isArchived"))
    return names, "gh_repo_list"


def load_json(path: Path) -> dict | list | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def repo_names_from_audit(audit: dict | None, ok_key: str, missing_key: str) -> set[str]:
    out: set[str] = set()
    if not isinstance(audit, dict):
        return out
    for r in audit.get(ok_key) or []:
        if isinstance(r, str) and r:
            out.add(r)
    for row in audit.get(missing_key) or []:
        if isinstance(row, str) and row:
            out.add(row)
        elif isinstance(row, dict):
            name = row.get("repo")
            if isinstance(name, str) and name:
                out.add(name)
    return out


def collect_known_repos(
    *,
    org_ci_audit: dict | None,
    org_agent_kit_audit: dict | None,
    ecosystem_audit: dict | None,
    org_packages: dict | None,
    extra: list[str] | None = None,
) -> set[str]:
    known: set[str] = set(CORE_AGENT_KIT_REPOS)
    known |= repo_names_from_audit(org_ci_audit, "repos_ok", "repos_missing_ci")
    kit = org_agent_kit_audit or {}
    for row in kit.get("repos_needing_sync") or []:
        if isinstance(row, str) and row:
            known.add(row)
        elif isinstance(row, dict) and row.get("repo"):
            known.add(str(row["repo"]))
    for r in kit.get("repos_ok") or []:
        if isinstance(r, str) and r:
            known.add(r)
    eco = ecosystem_audit or {}
    for key in ("repos_without_live_docs", "missing_ci_on_main", "repos_audited"):
        for r in eco.get(key) or []:
            if isinstance(r, str) and r:
                known.add(r)
    if isinstance(org_packages, dict):
        known |= set(org_packages.keys())
    if extra:
        known |= {r for r in extra if r}
    return known


def classify_new_repo(name: str) -> str:
    if name in ORG_MIRROR_REPOS or name.startswith("li-std-") or name in ("li-net", "li-httpd", "li-demo"):
        return "official_mirror"
    if name in ("lic", "li-language", "lip", "lit", "lis", "benchmarks", "roadmap", "li-cursor-agents"):
        return "core_tooling"
    if name.startswith("li-"):
        return "candidate_official"
    return "unclassified"


def onboarding_steps_for_repo(repo: str, classification: str) -> list[dict[str, str]]:
    steps = [
        {"agent": "ci_maintainer", "action": "add_ci_yml", "reason": f"Bootstrap ci.yml on new repo {repo}"},
        {"agent": "agent_kit_maintainer", "action": "sync_agent_kit", "reason": f"Install roadmap agent-kit on {repo}"},
        {"agent": "docs_maintainer", "action": "live_docs_smoke", "reason": f"Verify handbook / live docs for {repo}"},
    ]
    if classification in ("unclassified", "candidate_official"):
        steps.append(
            {
                "agent": "package_architect",
                "action": "placement_review",
                "reason": f"Classify {repo} — official PKG vs experimental vs archive",
            }
        )
    steps.append(
        {
            "agent": "code_implementer",
            "action": "register_in_catalog",
            "reason": f"After CI + agent-kit, add {repo} to org catalog / work-queue targets",
        }
    )
    return steps


def diff_org_repos(github_repos: list[str], known: set[str]) -> dict[str, Any]:
    gh = set(github_repos)
    new_repos = sorted(gh - known)
    stale_known = sorted(known - gh)
    entries = [
        {
            "repo": name,
            "classification": classify_new_repo(name),
            "onboarding_steps": onboarding_steps_for_repo(name, classify_new_repo(name)),
        }
        for name in new_repos
    ]
    return {
        "github_repos": sorted(gh),
        "known_repos": sorted(known),
        "new_repos": new_repos,
        "stale_known_repos": stale_known,
        "new_repo_entries": entries,
        "summary": {
            "github_count": len(gh),
            "known_count": len(known),
            "new_count": len(new_repos),
            "stale_count": len(stale_known),
        },
    }


def build_discovery_payload(
  github_repos: list[str],
  known: set[str],
  *,
  github_source: str,
) -> dict[str, Any]:
    diff = diff_org_repos(github_repos, known)
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "org": ORG,
        "github_source": github_source,
        **diff,
        "downstream_agent": "org_repo_onboarder",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover new li-langverse org repos")
    parser.add_argument("--fixture-github", type=Path, help="JSON list of repo names (tests)")
    parser.add_argument("--fixture-known", type=Path, help="JSON list of known repo names (tests)")
    parser.add_argument("--json-out", type=Path, default=OUT)
    args = parser.parse_args()

    if args.fixture_github:
        gh_raw = load_json(args.fixture_github)
        github_repos = sorted(gh_raw) if isinstance(gh_raw, list) else []
        github_source = "fixture"
    else:
        github_repos, github_source = list_github_repos()

    if args.fixture_known:
        known_raw = load_json(args.fixture_known)
        known = set(known_raw) if isinstance(known_raw, list) else set()
    else:
        known = collect_known_repos(
            org_ci_audit=load_json(ROOT / "data/latest/org-repo-ci-audit.json"),
            org_agent_kit_audit=load_json(ROOT / "data/latest/org-agent-kit-audit.json"),
            ecosystem_audit=load_json(ROOT / "data/latest/ecosystem-audit.json"),
            org_packages=None,
        )
        explorer = load_json(ROOT / "data/latest/ecosystem-explorer.json")
        if isinstance(explorer, dict):
            for r in explorer.get("org_mirror_repos") or []:
                if isinstance(r, str):
                    known.add(r)

    payload = build_discovery_payload(github_repos, known, github_source=github_source)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.json_out}")
    print(
        f"github={payload['summary']['github_count']} known={payload['summary']['known_count']} "
        f"new={payload['summary']['new_count']} stale={payload['summary']['stale_count']}"
    )
    if payload["new_repos"]:
        print("new:", ", ".join(payload["new_repos"][:12]))
    return 0 if payload["summary"]["new_count"] == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
