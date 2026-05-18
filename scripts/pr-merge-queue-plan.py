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
    repo = row["repo"]
    num = row["number"]
    detail = gh_json(
        [
            "pr",
            "view",
            str(num),
            "--repo",
            f"li-langverse/{repo}",
            "--json",
            "files,commits,mergeable,mergeStateStatus,baseRefName,headRefName",
        ]
    )
    files: list[str] = []
    commits = 0
    mergeable = None
    merge_state = None
    if isinstance(detail, dict):
        files = [f.get("path", "") for f in detail.get("files") or [] if f.get("path")]
        commits = len(detail.get("commits") or [])
        mergeable = detail.get("mergeable")
        merge_state = detail.get("mergeStateStatus")
    ready, blockers = gate_ready(repo, num)
    priority = REPO_PRIORITY.get(repo, 60) + title_priority_boost(row["title"])
    if not ready:
        priority += 200
    if mergeable == "CONFLICTING":
        priority += 150
        blockers = list(blockers) + ["merge_conflicts_with_base"]
    if row["merge_approved"] and ready and mergeable != "CONFLICTING":
        priority -= 30
    return {
        **row,
        "files": files,
        "commit_count": commits,
        "gate_ready": ready,
        "gate_blockers": blockers,
        "mergeable": mergeable,
        "merge_state": merge_state,
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


def detect_pair_risks(group: list[dict]) -> list[dict]:
    """Same-base PRs that touch overlapping files — merge order matters for main + branch progress."""
    risks: list[dict] = []
    for i, a in enumerate(group):
        for b in group[i + 1 :]:
            if a.get("head") == b.get("base") or b.get("head") == a.get("base"):
                continue
            overlap = file_overlap(a["files"], b["files"])
            if overlap < 0.35:
                continue
            # Prefer merging smaller / CI-ready PR first so the other can rebase onto updated main.
            first, second = (a, b)
            if (b["commit_count"], b["number"]) < (a["commit_count"], a["number"]):
                first, second = b, a
            risks.append(
                {
                    "repo": a["repo"],
                    "base": a.get("base", "main"),
                    "merge_first": pr_key(first),
                    "then_rebase_and_merge": pr_key(second),
                    "url_first": first["url"],
                    "url_second": second["url"],
                    "file_overlap": round(overlap, 3),
                    "reason": (
                        f"~{overlap:.0%} file overlap on `{a.get('base', 'main')}`; "
                        f"merge #{first['number']} first, then merge `origin/{a.get('base', 'main')}` "
                        f"into #{second['number']} (preserve both sides) before merging #{second['number']}"
                    ),
                    "resolution": "benchmarks/docs/ecosystem/merge-conflict-resolution.md",
                }
            )
    return risks


def apply_pair_risk_order(group: list[dict], risks: list[dict]) -> list[dict]:
    """Topological order: merge_first before then_rebase_and_merge."""
    by_id = {pr_key(p): p for p in group}
    ids = [pr_key(p) for p in group]
    edges: list[tuple[str, str]] = []
    for r in risks:
        a, b = r["merge_first"], r["then_rebase_and_merge"]
        if a in by_id and b in by_id:
            edges.append((a, b))
    for parent, child in edges:
        if parent not in ids or child not in ids:
            continue
        pi, ci = ids.index(parent), ids.index(child)
        if ci < pi:
            ids.pop(ci)
            ids.insert(pi + 1, child)
    return [by_id[i] for i in ids]


def build_repo_merge_plans(
    prs: list[dict], stacks: list[dict], redundant: list[dict]
) -> list[dict]:
    """Per-repo (+ base branch) merge order, conflicts with main, and overlap risks."""
    by_key: dict[tuple[str, str], list[dict]] = {}
    for p in prs:
        by_key.setdefault((p["repo"], p.get("base", "main")), []).append(p)

    plans: list[dict] = []
    for (repo, base), group in sorted(by_key.items()):
        repo_stacks = [s for s in stacks if s.get("repo") == repo or repo in s.get("merge_first", "")]
        risks = detect_pair_risks(group)
        ordered = apply_pair_risk_order(group, risks)
        ordered = enforce_stack_order(ordered, repo_stacks)

        conflicting_main = [
            {
                "number": p["number"],
                "url": p["url"],
                "title": p["title"],
                "merge_state": p.get("merge_state"),
                "action": (
                    "Do not merge until rebased: `git fetch origin && git checkout <head> && "
                    "git merge origin/"
                    f"{base}` — resolve conflicts preserving main + PR progress "
                    "(see merge-conflict-resolution.md)"
                ),
            }
            for p in group
            if p.get("mergeable") == "CONFLICTING"
        ]

        safe_keys: list[str] = []
        for p in ordered:
            key = pr_key(p)
            blocked_stack = any(
                s["then"] == key and s["merge_first"] in {pr_key(x) for x in group}
                for s in repo_stacks
            )
            parent_not_ready = False
            for s in repo_stacks:
                if s["then"] != key:
                    continue
                pid = s["merge_first"]
                parent = next((x for x in group if pr_key(x) == pid), None)
                if parent and not (parent["merge_approved"] and parent["gate_ready"]):
                    parent_not_ready = True
            if (
                p.get("mergeable") != "CONFLICTING"
                and p["merge_approved"]
                and p["gate_ready"]
                and not parent_not_ready
            ):
                safe_keys.append(key)

        plans.append(
            {
                "repo": repo,
                "base": base,
                "open_prs": len(group),
                "local_merge_order": [pr_key(p) for p in ordered],
                "safe_merge_order": safe_keys,
                "safe_next": safe_keys[0] if safe_keys else None,
                "conflicting_with_main": conflicting_main,
                "pair_risks": risks,
                "stacks": [s for s in repo_stacks if s.get("merge_first", "").startswith(f"{repo}#")],
                "progress_rule": (
                    "After each merge to "
                    f"{base}, remaining PRs must integrate latest {base} "
                    "(merge or rebase) before merge — never discard main or open PR commits"
                ),
            }
        )
    return plans


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
        if parent.get("mergeable") == "CONFLICTING":
            blocked[child_id] = (
                f"stack parent {parent_id} conflicts with base — resolve parent first"
            )
        elif not (parent["merge_approved"] and parent["gate_ready"]):
            blocked[child_id] = (
                f"stacked on #{parent['number']}; merge parent {parent_id} first "
                f"({parent['url']})"
            )
    return blocked


def conflict_blocked_ids(prs: list[dict], pair_risks: list[dict]) -> dict[str, str]:
    """Later PR in a high-overlap pair blocked until earlier PR merges (rebase required)."""
    by_id = {pr_key(p): p for p in prs}
    blocked: dict[str, str] = {}
    for r in pair_risks:
        first_id = r["merge_first"]
        second_id = r["then_rebase_and_merge"]
        first = by_id.get(first_id)
        second = by_id.get(second_id)
        if not first or not second:
            continue
        if first.get("mergeable") == "CONFLICTING":
            blocked[second_id] = (
                f"merge {first_id} blocked (conflicts with base); fix before #{second['number']}"
            )
        elif second.get("mergeable") == "CONFLICTING":
            continue
        elif first_id not in blocked and not (
            first["merge_approved"] and first["gate_ready"]
        ):
            blocked[second_id] = (
                f"overlap with {first_id} ({r['file_overlap']:.0%} files); "
                f"merge {first_id} first, then rebase {second_id} onto main"
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


def build_merge_order(
    prs: list[dict],
    stacks: list[dict],
    repo_plans: list[dict],
    pair_risks: list[dict],
) -> list[dict]:
    """Sort by repo/title priority; per-repo overlap order; stacks; annotate blockers."""
    blocked = stack_blocked_ids(prs, stacks)
    blocked.update(conflict_blocked_ids(prs, pair_risks))

    local_rank: dict[str, int] = {}
    for plan in repo_plans:
        for i, key in enumerate(plan.get("local_merge_order") or []):
            local_rank[key] = i

    def sort_key(p: dict) -> tuple:
        key = pr_key(p)
        blocked_boost = 1 if key in blocked else 0
        conflict_boost = 1 if p.get("mergeable") == "CONFLICTING" else 0
        return (
            blocked_boost,
            conflict_boost,
            local_rank.get(key, 50),
            p["priority_score"],
            p["created_at"] or "",
        )

    ordered = enforce_stack_order(sorted(prs, key=sort_key), stacks)
    plan: list[dict] = []
    for rank, p in enumerate(ordered, start=1):
        key = pr_key(p)
        auto = (
            p["merge_approved"]
            and p["gate_ready"]
            and p.get("mergeable") != "CONFLICTING"
            and key not in blocked
        )
        block_parts: list[str] = []
        if blocked.get(key):
            block_parts.append(blocked[key])
        if p.get("mergeable") == "CONFLICTING":
            block_parts.append("conflicts with base — rebase onto main before merge")
        plan.append(
            {
                "rank": rank,
                "repo": p["repo"],
                "number": p["number"],
                "url": p["url"],
                "title": p["title"],
                "merge_approved": p["merge_approved"],
                "gate_ready": p["gate_ready"],
                "mergeable": p.get("mergeable"),
                "merge_state": p.get("merge_state"),
                "priority_score": p["priority_score"],
                "auto_merge_ok": auto,
                "blocked_reason": "; ".join(block_parts) if block_parts else None,
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
    all_pair_risks: list[dict] = []
    by_key: dict[tuple[str, str], list[dict]] = {}
    for p in prs:
        by_key.setdefault((p["repo"], p.get("base", "main")), []).append(p)
    for group in by_key.values():
        all_pair_risks.extend(detect_pair_risks(group))
    repo_merge_plans = build_repo_merge_plans(prs, stacks, redundant)
    merge_order = build_merge_order(prs, stacks, repo_merge_plans, all_pair_risks)
    merge_sequence = build_merge_sequence(merge_order)
    next_merge = merge_sequence[0] if merge_sequence else None

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "vision_order": "package CI / mirrors → benchmarks → lic → lip/lit/lis → roadmap",
        "ordering_rules": [
            "Repo tier: mirrors/httpd → benchmarks → lic → lip/lit/lis → roadmap (roadmap last)",
            "Title hints: ci.yml / blocker fixes before agent-kit / bench / feature work",
            "Stacks: parent branch PR must merge before child PR targeting parent head",
            "Same-repo overlap: merge lower-risk PR first; rebase others onto main (never drop commits)",
            "CONFLICTING with base: excluded from merge_sequence until integrated with main",
            "Redundant pairs: close superseded PR after the including PR merges (human if unclear)",
            "Only merge-approved + gate-ready + mergeable PRs enter merge_sequence",
            "Supervisor: one merge per tick; re-run pr-merge-queue-plan.py after each merge",
            "Progress: after every merge, remaining PRs must absorb latest main before their merge",
        ],
        "summary": {
            "open_prs": len(prs),
            "merge_approved": sum(1 for p in prs if p["merge_approved"]),
            "gate_ready": sum(1 for p in prs if p["gate_ready"]),
            "conflicting_with_main": sum(1 for p in prs if p.get("mergeable") == "CONFLICTING"),
            "auto_merge_candidates": len(merge_sequence),
            "redundant_pairs": len(redundant),
            "stacks": len(stacks),
            "pair_risk_count": len(all_pair_risks),
            "repos_with_plans": len(repo_merge_plans),
        },
        "repo_merge_plans": repo_merge_plans,
        "pair_risks": all_pair_risks,
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
    for risk in all_pair_risks:
        report["warnings"].append(risk["reason"])
    for plan in repo_merge_plans:
        for c in plan.get("conflicting_with_main") or []:
            report["warnings"].append(
                f"{plan['repo']}#{c['number']} CONFLICTING with {plan['base']}: rebase before merge"
            )

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
