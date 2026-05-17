#!/usr/bin/env python3
"""Plan merge order and detect redundant PRs before auto-merge.

Writes data/latest/pr-merge-queue-plan.json

Requires: gh auth with repo read access.
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
OUT = ROOT / "data/latest/pr-merge-queue-plan.json"

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
]

# Lower = merge earlier (vision: package CI → benchmarks → lic → tooling → governance)
REPO_PRIORITY: dict[str, int] = {
    "li-httpd": 10,
    "li-net": 10,
    "li-std-core": 12,
    "li-std-math": 12,
    "li-demo": 12,
    "benchmarks": 20,
    "lic": 30,
    "lip": 40,
    "lit": 40,
    "lis": 45,
    "roadmap": 90,
}

TITLE_PRIORITY_HINTS: list[tuple[int, re.Pattern[str]]] = [
    (0, re.compile(r"\bci\.yml\b|workflow|github actions", re.I)),
    (5, re.compile(r"fix\(types\)|compile|build.?fix|blocker", re.I)),
    (10, re.compile(r"agent-kit|sync", re.I)),
    (15, re.compile(r"benchmark|catalog|ingest", re.I)),
]


def gh_json(args: list[str]) -> dict | list | None:
    proc = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def gate_ready(repo: str, number: int) -> tuple[bool, list[str]]:
    gate = ROOT / "scripts" / "pr-merge-gate.py"
    proc = subprocess.run(
        [sys.executable, str(gate), "--repo", repo, "--pr", str(number), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        return False, ["gate script failed"]
    try:
        data = json.loads(proc.stdout)
        row = data["results"][0]
        return bool(row.get("ready")), list(row.get("blockers") or [])
    except (json.JSONDecodeError, KeyError, IndexError):
        return False, ["invalid gate output"]


def title_priority_boost(title: str) -> int:
    for boost, pat in TITLE_PRIORITY_HINTS:
        if pat.search(title):
            return boost
    return 50


def fetch_open_prs(repos: list[str]) -> list[dict]:
    rows: list[dict] = []
    for repo in repos:
        prs = gh_json(
            [
                "pr",
                "list",
                "--repo",
                f"li-langverse/{repo}",
                "--state",
                "open",
                "--json",
                "number,title,url,labels,baseRefName,headRefName,isDraft,createdAt",
                "--limit",
                "40",
            ]
        )
        if not prs:
            continue
        for pr in prs:
            if pr.get("isDraft"):
                continue
            labels = {lb["name"] for lb in pr.get("labels") or []}
            rows.append(
                {
                    "repo": repo,
                    "number": pr["number"],
                    "title": pr["title"],
                    "url": pr["url"],
                    "base": pr.get("baseRefName", "main"),
                    "head": pr.get("headRefName", ""),
                    "labels": sorted(labels),
                    "merge_approved": "merge-approved" in labels,
                    "created_at": pr.get("createdAt"),
                }
            )
    return rows


def enrich_pr(row: dict) -> dict:
    detail = gh_json(
        [
            "pr",
            "view",
            str(row["number"]),
            "--repo",
            f"li-langverse/{row['repo']}",
            "--json",
            "files,commits",
        ]
    )
    files: list[str] = []
    commits = 0
    if isinstance(detail, dict):
        files = [f.get("path", "") for f in detail.get("files") or [] if f.get("path")]
        commits = len(detail.get("commits") or [])
    ready, blockers = gate_ready(row["repo"], row["number"])
    priority = REPO_PRIORITY.get(row["repo"], 60) + title_priority_boost(row["title"])
    if not ready:
        priority += 200
    if row["merge_approved"] and ready:
        priority -= 30
    return {
        **row,
        "files": files,
        "commit_count": commits,
        "gate_ready": ready,
        "gate_blockers": blockers,
        "priority_score": priority,
    }


def file_overlap(a: list[str], b: list[str]) -> float:
    if not a or not b:
        return 0.0
    sa, sb = set(a), set(b)
    inter = len(sa & sb)
    denom = min(len(sa), len(sb))
    return inter / denom if denom else 0.0


def branch_included_in(repo: str, base: str, ancestor_head: str, descendant_head: str) -> bool:
    """True if ancestor_head commits are reachable from descendant_head vs base."""
    if not ancestor_head or not descendant_head or ancestor_head == descendant_head:
        return ancestor_head == descendant_head
    cmp = gh_json(
        [
            "api",
            f"repos/li-langverse/{repo}/compare/{base}...{descendant_head}",
        ]
    )
    if not isinstance(cmp, dict):
        return False
    status = cmp.get("status", "")
    if status == "identical":
        return True
    # ahead_by on descendant compare includes ancestor if merged in line
    ahead = cmp.get("ahead_by", 0) or 0
    behind = cmp.get("behind_by", 0) or 0
    if ahead == 0 and behind == 0:
        return True
    # compare ancestor...descendant: if status ahead and behind 0, descendant contains ancestor
    inner = gh_json(
        [
            "api",
            f"repos/li-langverse/{repo}/compare/{ancestor_head}...{descendant_head}",
        ]
    )
    if isinstance(inner, dict):
        return inner.get("status") in ("ahead", "identical") and (inner.get("behind_by") or 0) == 0
    return False


def detect_stacks(prs: list[dict]) -> list[dict]:
    """PR B based on PR A's head branch in same repo."""
    by_repo: dict[str, list[dict]] = {}
    for p in prs:
        by_repo.setdefault(p["repo"], []).append(p)
    stacks: list[dict] = []
    for repo, group in by_repo.items():
        heads = {p["head"]: p for p in group if p.get("head")}
        for p in group:
            base = p.get("base", "")
            if base in heads and base != p.get("head"):
                parent = heads[base]
                stacks.append(
                    {
                        "repo": repo,
                        "merge_first": f"{parent['repo']}#{parent['number']}",
                        "then": f"{p['repo']}#{p['number']}",
                        "reason": f"{p['url']} is stacked on branch `{base}` from #{parent['number']}",
                    }
                )
    return stacks


def detect_redundant_pairs(prs: list[dict]) -> list[dict]:
    redundant: list[dict] = []
    by_repo: dict[str, list[dict]] = {}
    for p in prs:
        by_repo.setdefault(p["repo"], []).append(p)

    for repo, group in by_repo.items():
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                overlap = file_overlap(a["files"], b["files"])
                reasons: list[str] = []
                action = None

                # stacked: handled separately
                if a.get("head") == b.get("base") or b.get("head") == a.get("base"):
                    continue

                base = a.get("base") if a.get("base") == b.get("base") else "main"
                a_in_b = branch_included_in(repo, base, a["head"], b["head"])
                b_in_a = branch_included_in(repo, base, b["head"], a["head"])

                if a_in_b and not b_in_a:
                    reasons.append(f"#{b['number']} branch includes all commits from #{a['number']}")
                    action = f"close #{a['number']} after #{b['number']} merges"
                elif b_in_a and not a_in_b:
                    reasons.append(f"#{a['number']} branch includes all commits from #{b['number']}")
                    action = f"close #{b['number']} after #{a['number']} merges"

                if overlap >= 0.85 and a["files"] and b["files"]:
                    reasons.append(f"{overlap:.0%} file overlap")
                    if not action:
                        action = "human: pick one PR or rebase the other"

                if "supersed" in (a["title"] + b["title"]).lower():
                    reasons.append("title mentions supersede")

                if reasons and action:
                    redundant.append(
                        {
                            "repo": repo,
                            "pr_a": f"{repo}#{a['number']}",
                            "pr_b": f"{repo}#{b['number']}",
                            "url_a": a["url"],
                            "url_b": b["url"],
                            "overlap": round(overlap, 3),
                            "reasons": reasons,
                            "suggested_action": action,
                        }
                    )
    return redundant


def pr_key(p: dict) -> str:
    return f"{p['repo']}#{p['number']}"


def stack_blocked_ids(prs: list[dict], stacks: list[dict]) -> dict[str, str]:
    """Child PRs blocked until stack parent is merge-approved + gate-ready."""
    by_id = {pr_key(p): p for p in prs}
    blocked: dict[str, str] = {}
    for s in stacks:
        parent_id = s["merge_first"]
        child_id = s["then"]
        parent = by_id.get(parent_id)
        child = by_id.get(child_id)
        if not parent or not child:
            continue
        if not (parent["merge_approved"] and parent["gate_ready"]):
            blocked[child_id] = (
                f"stacked on #{parent['number']}; merge parent {parent_id} first "
                f"({parent['url']})"
            )
    return blocked


def enforce_stack_order(ordered: list[dict], stacks: list[dict]) -> list[dict]:
    """Ensure stacked children never rank above their parent branch PR."""
    ids = [pr_key(p) for p in ordered]
    by_id = {pr_key(p): p for p in ordered}
    for s in stacks:
        parent_id = s["merge_first"]
        child_id = s["then"]
        if parent_id not in ids or child_id not in ids:
            continue
        pi, ci = ids.index(parent_id), ids.index(child_id)
        if ci < pi:
            ids.pop(ci)
            ids.insert(pi + 1, child_id)
    return [by_id[i] for i in ids]


def order_reason(p: dict, rank: int, blocked: dict[str, str]) -> str:
    if pr_key(p) in blocked:
        return blocked[pr_key(p)]
    parts = [f"rank {rank}", f"priority_score={p['priority_score']}"]
    if p["merge_approved"] and p["gate_ready"]:
        parts.append("merge-approved + gate ready")
    elif not p["merge_approved"]:
        parts.append("awaiting merge-approved label")
    elif not p["gate_ready"]:
        parts.append(f"gate blocked: {', '.join(p.get('gate_blockers') or [])}")
    return "; ".join(parts)


def build_merge_order(prs: list[dict], stacks: list[dict]) -> list[dict]:
    """Sort by repo/title priority; topological stack order; annotate blockers."""
    blocked = stack_blocked_ids(prs, stacks)

    def sort_key(p: dict) -> tuple:
        blocked_boost = 1 if pr_key(p) in blocked else 0
        return (blocked_boost, p["priority_score"], p["created_at"] or "")

    ordered = enforce_stack_order(sorted(prs, key=sort_key), stacks)
    plan: list[dict] = []
    for rank, p in enumerate(ordered, start=1):
        key = pr_key(p)
        auto = p["merge_approved"] and p["gate_ready"] and key not in blocked
        plan.append(
            {
                "rank": rank,
                "repo": p["repo"],
                "number": p["number"],
                "url": p["url"],
                "title": p["title"],
                "merge_approved": p["merge_approved"],
                "gate_ready": p["gate_ready"],
                "priority_score": p["priority_score"],
                "auto_merge_ok": auto,
                "blocked_reason": blocked.get(key),
                "order_reason": order_reason(p, rank, blocked),
            }
        )
    return plan


def build_merge_sequence(merge_order: list[dict]) -> list[dict]:
    """PRs safe to merge now, in rank order (one per supervisor tick)."""
    return [p for p in merge_order if p["auto_merge_ok"]]


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan merge queue order and redundancy")
    parser.add_argument("--json", action="store_true", help="print JSON to stdout")
    parser.add_argument("--repo", help="limit to one repo")
    args = parser.parse_args()

    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("gh required", file=sys.stderr)
        return 1

    repos = [args.repo] if args.repo else ORG_REPOS
    raw = fetch_open_prs(repos)
    prs = [enrich_pr(r) for r in raw]
    stacks = detect_stacks(prs)
    redundant = detect_redundant_pairs(prs)
    merge_order = build_merge_order(prs, stacks)
    merge_sequence = build_merge_sequence(merge_order)
    next_merge = merge_sequence[0] if merge_sequence else None

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "vision_order": "package CI / mirrors → benchmarks → lic → lip/lit/lis → roadmap",
        "ordering_rules": [
            "Repo tier: mirrors/httpd → benchmarks → lic → lip/lit/lis → roadmap (roadmap last)",
            "Title hints: ci.yml / blocker fixes before agent-kit / bench / feature work",
            "Stacks: parent branch PR must merge before child PR targeting parent head",
            "Redundant pairs: close superseded PR after the including PR merges (human if unclear)",
            "Only merge-approved + gate-ready PRs enter merge_sequence",
            "Supervisor: one merge per tick; re-run pr-merge-queue-plan.py after each merge",
        ],
        "summary": {
            "open_prs": len(prs),
            "merge_approved": sum(1 for p in prs if p["merge_approved"]),
            "gate_ready": sum(1 for p in prs if p["gate_ready"]),
            "auto_merge_candidates": len(merge_sequence),
            "redundant_pairs": len(redundant),
            "stacks": len(stacks),
        },
        "merge_first": next_merge,
        "next_merge": next_merge,
        "merge_sequence": merge_sequence,
        "merge_order": merge_order,
        "stacks": stacks,
        "redundant": redundant,
        "warnings": [],
    }

    for r in redundant:
        report["warnings"].append(
            f"{r['pr_a']} vs {r['pr_b']}: {r['suggested_action']}"
        )
    for s in stacks:
        report["warnings"].append(s["reason"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"wrote {OUT}")
        if next_merge:
            print(
                f"next merge: {next_merge['repo']}#{next_merge['number']} {next_merge['url']}"
            )
            print(f"  reason: {next_merge.get('order_reason', '')}")
        if len(merge_sequence) > 1:
            print(f"  then: {merge_sequence[1]['repo']}#{merge_sequence[1]['number']} …")
        for w in report["warnings"][:10]:
            print(f"  warn: {w}")
        if len(report["warnings"]) > 10:
            print(f"  ... +{len(report['warnings']) - 10} warnings")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
