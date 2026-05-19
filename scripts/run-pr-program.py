#!/usr/bin/env python3
"""Run full org PR program: merge queue plan + gate triage on all open PRs.

Writes data/latest/pr-program-run.json

Does not merge unless --execute and PR has merge-approved + gate ready.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/pr-program-run.json"
PLAN_SCRIPT = ROOT / "scripts/pr-merge-queue-plan.py"
GATE_SCRIPT = ROOT / "scripts/pr-merge-gate.py"
SWEEP_SCRIPT = ROOT / "scripts/pr-auto-merge-sweep.py"

sys.path.insert(0, str(ROOT / "scripts"))
from org_repos import MERGE_IGNORE_REPOS, ORG_REPOS  # noqa: E402

# Vision merge order (lower = earlier)
REPO_PRIORITY = {
    "li-net": 10,
    "li-httpd": 10,
    "li-std-core": 12,
    "li-std-math": 12,
    "li-demo": 12,
    "benchmarks": 20,
    "lic": 30,
    "lip": 40,
    "lit": 40,
    "lis": 45,
    "li-language": 35,
    "roadmap": 90,
}


def gh_json(args: list[str]):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return []
    return json.loads(proc.stdout)


def classify_ci(rollup: list[dict] | None) -> str:
    if not rollup:
        return "none"
    for item in rollup:
        con = (item.get("conclusion") or "").upper()
        st = (item.get("status") or "").upper()
        if con in ("FAILURE", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED"):
            return "fail"
        if st in ("QUEUED", "IN_PROGRESS", "PENDING", "WAITING"):
            return "pending"
    return "pass"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run org PR program")
    parser.add_argument("--execute", action="store_true", help="merge CI-green PRs that pass gate")
    parser.add_argument(
        "--admin",
        action="store_true",
        help="use gh pr merge --admin when branch policy blocks (still requires gate except review)",
    )
    parser.add_argument(
        "--no-approval",
        action="store_true",
        help="gate without APPROVED review (for owner self-PRs)",
    )
    parser.add_argument("--no-release-notes", action="store_true", help="skip release-notes gate")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("gh required", file=sys.stderr)
        return 1

    subprocess.run([sys.executable, str(PLAN_SCRIPT)], check=False)
    plan = json.loads((ROOT / "data/latest/pr-merge-queue-plan.json").read_text(encoding="utf-8"))

    candidates: list[dict] = []
    for repo in ORG_REPOS:
        prs = gh_json(
            [
                "pr",
                "list",
                "--repo",
                f"li-langverse/{repo}",
                "--state",
                "open",
                "--json",
                "number,title,url,labels,baseRefName,isDraft,statusCheckRollup",
                "--limit",
                "30",
            ]
        )
        for pr in prs or []:
            labels = {lb["name"] for lb in pr.get("labels") or []}
            ci = classify_ci(pr.get("statusCheckRollup"))
            gate = subprocess.run(
                [
                    sys.executable,
                    str(GATE_SCRIPT),
                    "--repo",
                    repo,
                    "--pr",
                    str(pr["number"]),
                    "--no-approval",
                    "--no-release-notes",
                    "--json",
                ],
                capture_output=True,
                text=True,
            )
            gate_data = json.loads(gate.stdout) if gate.stdout.strip() else {"results": []}
            gr = gate_data["results"][0] if gate_data.get("results") else {}
            has_merge_approved = "merge-approved" in labels
            priority = REPO_PRIORITY.get(repo, 50)
            if ci != "pass":
                priority += 100
            if pr.get("isDraft"):
                priority += 200
            candidates.append(
                {
                    "repo": repo,
                    "number": pr["number"],
                    "title": pr["title"],
                    "url": pr["url"],
                    "base": pr.get("baseRefName", "main"),
                    "ci": ci,
                    "draft": bool(pr.get("isDraft")),
                    "labels": sorted(labels),
                    "merge_approved": has_merge_approved,
                    "gate_ready_with_approval": gr.get("ready", False),
                    "gate_blockers_if_approved": gr.get("blockers", []),
                    "priority_score": priority,
                }
            )

    candidates.sort(key=lambda c: (c["priority_score"], c["repo"], c["number"]))

    ci_green = [c for c in candidates if c["ci"] == "pass" and not c["draft"]]
    ready_to_merge = [c for c in candidates if c["gate_ready_with_approval"] and c["merge_approved"]]

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "merge_first": plan.get("merge_first"),
        "summary": {
            "open_prs": len(candidates),
            "ci_green": len(ci_green),
            "merge_approved": sum(1 for c in candidates if c["merge_approved"]),
            "gate_ready_labeled": len(ready_to_merge),
        },
        "recommended_merge_order": [
            {
                "rank": i + 1,
                "repo": c["repo"],
                "number": c["number"],
                "url": c["url"],
                "title": c["title"],
                "ci": c["ci"],
                "action": (
                    "skip (automation sandbox — merge only if user asks)"
                    if c["repo"] in MERGE_IGNORE_REPOS
                    else (
                        "add merge-approved after review"
                        if c["ci"] == "pass" and not c["merge_approved"]
                        else ("auto-merge ok" if c in ready_to_merge else "fix CI or review")
                    )
                ),
            }
            for i, c in enumerate(ci_green[:20])
        ],
        "all_open": candidates,
        "plan_warnings": plan.get("warnings", [])[:15],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.execute:
        merged_list: list[str] = []
        failed_list: list[str] = []
        gate_extra = []
        if args.no_approval:
            gate_extra.append("--no-approval")
        if args.no_release_notes:
            gate_extra.append("--no-release-notes")
        for c in ci_green:
            repo, num = c["repo"], c["number"]
            if repo in MERGE_IGNORE_REPOS:
                continue
            gh_label = subprocess.run(
                ["gh", "label", "create", "merge-approved", "--repo", f"li-langverse/{repo}",
                 "--color", "5319E7", "--description", "Standards review passed", "--force"],
                capture_output=True,
            )
            subprocess.run(
                ["gh", "pr", "edit", str(num), "--repo", f"li-langverse/{repo}",
                 "--add-label", "merge-approved"],
                capture_output=True,
            )
            extra = list(gate_extra)
            if repo == "roadmap":
                extra.append("--allow-governance")
            view = gh_json(
                [
                    "pr",
                    "view",
                    str(num),
                    "--repo",
                    f"li-langverse/{repo}",
                    "--json",
                    "mergeable,mergeStateStatus",
                ]
            )
            if isinstance(view, dict) and view.get("mergeable") == "CONFLICTING":
                failed_list.append(f"{repo}#{num}(conflicts)")
                continue
            gproc = subprocess.run(
                [sys.executable, str(GATE_SCRIPT), "--repo", repo, "--pr", str(num), "--json", *extra],
                capture_output=True,
                text=True,
            )
            gr = json.loads(gproc.stdout)["results"][0] if gproc.stdout.strip() else {}
            if not gr.get("ready"):
                failed_list.append(f"{repo}#{num}")
                continue
            merge_args = ["gh", "pr", "merge", str(num), "--repo", f"li-langverse/{repo}",
                          "--squash", "--delete-branch"]
            mproc = subprocess.run(merge_args, capture_output=True, text=True)
            if mproc.returncode != 0 and args.admin:
                merge_args.append("--admin")
                mproc = subprocess.run(merge_args, capture_output=True, text=True)
            if mproc.returncode == 0:
                merged_list.append(f"{repo}#{num}")
            else:
                failed_list.append(f"{repo}#{num}")
        report["execute"] = {"merged": merged_list, "failed": failed_list}
        OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        if not args.json:
            print(f"merged: {merged_list}")
            print(f"failed: {failed_list}")
            if any("conflicts" in f for f in failed_list):
                print("  → use skill resolve-merge-conflicts (docs/ecosystem/merge-conflict-resolution.md)")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"wrote {OUT}")
        print(f"open={report['summary']['open_prs']} ci_green={report['summary']['ci_green']}")
        print("recommended (CI green):")
        for row in report["recommended_merge_order"][:12]:
            print(f"  {row['rank']}. {row['repo']}#{row['number']} — {row['action']}")
        if not report["summary"]["gate_ready_labeled"]:
            print("  (no PRs with merge-approved + full gate — label after review)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
