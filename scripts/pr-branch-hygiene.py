#!/usr/bin/env python3
"""Find remote branches without open PRs and PRs recommended for close.

Writes data/latest/pr-branch-hygiene.json (consumed by agent-briefing.py).

Requires: gh CLI, GH_TOKEN for private repos.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/pr-branch-hygiene.json"
ORG = "li-langverse"

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
    "li-cursor-agents",
]

SKIP_BRANCH_PREFIXES = (
    "dependabot/",
    "renovate/",
    "github-actions/",
    "release/",
)
SKIP_BRANCH_NAMES = {"main", "dev", "master", "gh-pages"}


def gh_json(args: list[str]) -> list | dict | None:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def default_branch(repo: str) -> str:
    data = gh_json(["repo", "view", f"{ORG}/{repo}", "--json", "defaultBranchRef"])
    if isinstance(data, dict):
        ref = data.get("defaultBranchRef") or {}
        name = ref.get("name")
        if name:
            return name
    return "main"


def open_pr_heads(repo: str) -> tuple[set[str], list[dict]]:
    prs = gh_json(
        [
            "pr",
            "list",
            "--repo",
            f"{ORG}/{repo}",
            "--state",
            "open",
            "--json",
            "headRefName,isDraft,number,url,updatedAt,labels",
            "--limit",
            "50",
        ]
    )
    heads: set[str] = set()
    pr_list = prs if isinstance(prs, list) else []
    for pr in pr_list:
        if not isinstance(pr, dict):
            continue
        head = pr.get("headRefName")
        if head:
            heads.add(head)
    return heads, pr_list


def branch_ahead(repo: str, base: str, head: str) -> int:
    cmp = gh_json(
        [
            "api",
            f"repos/{ORG}/{repo}/compare/{base}...{head}",
            "--jq",
            ".ahead_by",
        ]
    )
    if cmp is None:
        return 0
    if isinstance(cmp, int):
        return cmp
    return 0


def list_remote_branches(repo: str, limit: int) -> list[str]:
    data = gh_json(
        [
            "api",
            f"repos/{ORG}/{repo}/branches",
            "--paginate",
            "--jq",
            ".[].name",
        ]
    )
    if not isinstance(data, list):
        return []
    names: list[str] = []
    for name in data:
        if not isinstance(name, str):
            continue
        if name in SKIP_BRANCH_NAMES:
            continue
        if any(name.startswith(p) for p in SKIP_BRANCH_PREFIXES):
            continue
        names.append(name)
        if len(names) >= limit:
            break
    return names


def parse_close_number(action: str) -> int | None:
    m = re.search(r"close #(\d+)", action, re.I)
    return int(m.group(1)) if m else None


def redundant_closes(merge_plan: dict) -> list[dict]:
    out: list[dict] = []
    for row in merge_plan.get("redundant") or []:
        action = str(row.get("suggested_action") or "")
        num = parse_close_number(action)
        if num is None:
            continue
        repo = str(row.get("repo") or "")
        url_a = row.get("url_a") or ""
        url_b = row.get("url_b") or ""
        pr_a = str(row.get("pr_a") or "")
        pr_b = str(row.get("pr_b") or "")
        close_url = url_a if pr_a.endswith(f"#{num}") else url_b if pr_b.endswith(f"#{num}") else ""
        safe_now = "after" not in action.lower()
        out.append(
            {
                "repo": repo,
                "number": num,
                "url": close_url,
                "reason": "; ".join(row.get("reasons") or []),
                "action": "close",
                "safe_now": safe_now,
                "source": "merge_plan.redundant",
                "suggested_action": action,
            }
        )
    return out


def stale_pr_candidates(repo: str, prs: list[dict], base: str) -> list[dict]:
    out: list[dict] = []
    for pr in prs:
        labels = {lb.get("name") for lb in pr.get("labels") or [] if isinstance(lb, dict)}
        if "superseded" in labels or "stale-pr" in labels:
            out.append(
                {
                    "repo": repo,
                    "number": pr["number"],
                    "url": pr.get("url"),
                    "reason": f"labels: {', '.join(sorted(labels & {'superseded', 'stale-pr'}))}",
                    "action": "close",
                    "safe_now": True,
                    "source": "label",
                }
            )
            continue
        if pr.get("isDraft"):
            out.append(
                {
                    "repo": repo,
                    "number": pr["number"],
                    "url": pr.get("url"),
                    "reason": "draft PR — confirm abandoned before close",
                    "action": "close",
                    "safe_now": False,
                    "source": "draft",
                }
            )
    return out


def scan_branches(repo: str, max_branches: int) -> list[dict]:
    base = default_branch(repo)
    heads, open_prs = open_pr_heads(repo)
    needing: list[dict] = []
    for branch in list_remote_branches(repo, max_branches):
        if branch in heads:
            continue
        ahead = branch_ahead(repo, base, branch)
        if ahead < 1:
            continue
        needing.append(
            {
                "repo": repo,
                "branch": branch,
                "base": base,
                "ahead_by": ahead,
                "reason": f"branch `{branch}` is {ahead} commit(s) ahead of `{base}` with no open PR",
                "suggested_title": f"chore({repo}): sync branch {branch}",
            }
        )
    return needing, stale_pr_candidates(repo, open_prs, base)


def main() -> int:
    parser = argparse.ArgumentParser(description="Branch / PR hygiene scan for agents")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--repo", help="limit to one repo")
    parser.add_argument("--max-branches", type=int, default=40, help="max branches per repo")
    args = parser.parse_args()

    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("gh required", file=sys.stderr)
        return 1

    repos = [args.repo] if args.repo else ORG_REPOS
    merge_plan_path = ROOT / "data/latest/pr-merge-queue-plan.json"
    merge_plan: dict = {}
    if merge_plan_path.is_file():
        merge_plan = json.loads(merge_plan_path.read_text(encoding="utf-8"))

    branches_needing_pr: list[dict] = []
    prs_recommended_close: list[dict] = []
    seen_close: set[tuple[str, int]] = set()

    for row in redundant_closes(merge_plan):
        key = (row["repo"], row["number"])
        if key in seen_close:
            continue
        seen_close.add(key)
        prs_recommended_close.append(row)

    for repo in repos:
        needing, stale = scan_branches(repo, args.max_branches)
        branches_needing_pr.extend(needing)
        for row in stale:
            key = (row["repo"], row["number"])
            if key in seen_close:
                continue
            seen_close.add(key)
            prs_recommended_close.append(row)

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "org": ORG,
        "summary": {
            "repos_scanned": len(repos),
            "branches_needing_pr": len(branches_needing_pr),
            "prs_recommended_close": len(prs_recommended_close),
            "prs_safe_close_now": sum(1 for p in prs_recommended_close if p.get("safe_now")),
        },
        "branches_needing_pr": branches_needing_pr,
        "prs_recommended_close": prs_recommended_close,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"wrote {OUT}")
        print(
            f"  branches needing PR: {report['summary']['branches_needing_pr']}, "
            f"PRs to review for close: {report['summary']['prs_recommended_close']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
