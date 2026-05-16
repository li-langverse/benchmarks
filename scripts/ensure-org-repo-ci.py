#!/usr/bin/env python3
"""Verify every li-langverse repo has .github/workflows/ci.yml on default branch.

Writes data/latest/org-repo-ci-audit.json
Exit 1 if any repo missing CI (use in CI or pre-merge checks).

Usage:
  python3 scripts/ensure-org-repo-ci.py
  python3 scripts/ensure-org-repo-ci.py --repo lic
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/org-repo-ci-audit.json"
ORG = "li-langverse"
REQUIRED_WORKFLOW = "ci.yml"
# Repos exempt from single-job ci.yml (multi-workflow compiler mirrors)
EXEMPT_REPOS: set[str] = set()  # li-language uses ci.yml — keep in audit


def gh_json(args: list[str]):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def list_org_repos() -> list[str]:
    rows = gh_json(["repo", "list", ORG, "--limit", "100", "--json", "name,isArchived"])
    if not rows:
        return []
    return sorted(r["name"] for r in rows if not r.get("isArchived"))


def workflow_names(repo: str) -> list[str]:
    proc = subprocess.run(
        ["gh", "api", f"repos/{ORG}/{repo}/contents/.github/workflows", "-q", ".[].name"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]


def has_ci(repo: str) -> bool:
    names = workflow_names(repo)
    return REQUIRED_WORKFLOW in names or "ci.yaml" in names


def latest_check_job(repo: str) -> str | None:
    """Return primary CI job name for branch protection hints."""
    if repo in ("lic", "li-language"):
        return "build-and-test"
    if repo == "benchmarks":
        return "ingest-smoke"
    if repo == "roadmap":
        return "verify-kit"
    if repo == "lip":
        return "bootstrap"
    if repo == "lit":
        return "test"
    if repo == "lis":
        return None  # matrix jobs — ruleset uses empty or repo-specific
    # Official package mirrors
    return "check"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit org repos for ci.yml")
    parser.add_argument("--repo", action="append", dest="repos", help="limit to repo(s)")
    parser.add_argument("--json-out", type=Path, default=OUT)
    args = parser.parse_args()

    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("gh required", file=sys.stderr)
        return 1

    repos = args.repos if args.repos else list_org_repos()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    ok: list[str] = []
    missing: list[dict] = []
    workflows: dict[str, list[str]] = {}

    for repo in repos:
        if repo in EXEMPT_REPOS:
            ok.append(repo)
            continue
        names = workflow_names(repo)
        workflows[repo] = names
        if has_ci(repo):
            ok.append(repo)
        else:
            missing.append(
                {
                    "repo": repo,
                    "workflows": names,
                    "fix": f"Add .github/workflows/{REQUIRED_WORKFLOW} (see lic/scripts/templates/github-repo/ci.yml)",
                    "suggested_required_check": latest_check_job(repo),
                }
            )

    report = {
        "generated_at": now,
        "org": ORG,
        "required_workflow": REQUIRED_WORKFLOW,
        "repos_ok": ok,
        "repos_missing_ci": missing,
        "workflows": workflows,
        "policy": "docs/ecosystem/repo-ci-required.md",
        "lic_monorepo_hint": "Run lic/scripts/ensure-package-ci.sh before push-official-package-repo.sh",
    }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.json_out}")
    print(f"OK: {len(ok)}  missing: {len(missing)}")
    for m in missing:
        print(f"  MISSING {m['repo']}: {m['workflows']}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
