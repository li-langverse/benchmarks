#!/usr/bin/env python3
"""Evaluate whether an open PR satisfies li-langverse merge gates (CI, review, labels)."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MERGE_APPROVED = "merge-approved"
PLAN_APPROVED = "plan-approved"
PLAN_NEEDED = "plan-needed"
BLOCK_LABELS = frozenset({"do-not-merge", "blocked", "wontfix"})
GOVERNANCE_REPOS = frozenset({"roadmap"})
ORG_REPOS = (
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
)


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


@dataclass
class GateResult:
    repo: str
    number: int
    url: str
    ready: bool
    checks: list[dict] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "repo": self.repo,
            "number": self.number,
            "url": self.url,
            "ready": self.ready,
            "checks": self.checks,
            "blockers": self.blockers,
        }


def _check(name: str, ok: bool, detail: str, blockers: list[str], checks: list[dict]) -> None:
    checks.append({"name": name, "ok": ok, "detail": detail})
    if not ok:
        blockers.append(f"{name}: {detail}")


def evaluate_pr(
    repo: str,
    number: int,
    *,
    require_approval: bool = True,
    require_release_notes: bool = True,
    allow_governance: bool = False,
) -> GateResult:
    full = f"li-langverse/{repo}" if "/" not in repo else repo
    repo_name = full.split("/", 1)[-1]

    pr = gh_json(
        [
            "pr",
            "view",
            str(number),
            "--repo",
            full,
            "--json",
            "number,url,isDraft,labels,statusCheckRollup,reviewDecision,author,"
            "files,headRefName,baseRefName,title",
        ]
    )
    if not pr:
        return GateResult(repo_name, number, "", False, blockers=["pr_not_found"])

    url = pr.get("url", "")
    blockers: list[str] = []
    checks: list[dict] = []
    label_names = {lb["name"] for lb in pr.get("labels") or []}

    _check(
        "not_draft",
        not pr.get("isDraft"),
        "PR is still a draft",
        blockers,
        checks,
    )

    _check(
        "merge_approved_label",
        MERGE_APPROVED in label_names,
        f"missing label `{MERGE_APPROVED}` (reviewer adds after standards pass)",
        blockers,
        checks,
    )

    blocked = label_names & BLOCK_LABELS
    _check(
        "no_block_labels",
        not blocked,
        f"blocked by labels: {', '.join(sorted(blocked))}",
        blockers,
        checks,
    )

    if PLAN_NEEDED in label_names and PLAN_APPROVED not in label_names:
        _check(
            "plan_approved",
            False,
            f"has `{PLAN_NEEDED}` without `{PLAN_APPROVED}`",
            blockers,
            checks,
        )
    else:
        _check(
            "plan_approved",
            True,
            "plan gate ok",
            blockers,
            checks,
        )

    ci = classify_ci(pr.get("statusCheckRollup"))
    _check(
        "ci_green",
        ci == "pass",
        f"CI status is `{ci}` (all required checks must pass)",
        blockers,
        checks,
    )

    decision = (pr.get("reviewDecision") or "").upper()
    if require_approval:
        _check(
            "review_approved",
            decision == "APPROVED",
            f"reviewDecision is `{decision or 'none'}` (need APPROVED)",
            blockers,
            checks,
        )
    else:
        _check(
            "review_approved",
            decision in ("APPROVED", "REVIEW_REQUIRED", ""),
            f"reviewDecision `{decision}`",
            blockers,
            checks,
        )

    if repo_name in GOVERNANCE_REPOS and not allow_governance:
        _check(
            "governance_repo",
            False,
            f"`{repo_name}` requires human merge unless ALLOW_GOVERNANCE_MERGE=1",
            blockers,
            checks,
        )
    else:
        _check(
            "governance_repo",
            True,
            "not a blocked governance auto-merge repo",
            blockers,
            checks,
        )

    if require_release_notes and repo_name in ("lic", "lip", "lit", "lis", "benchmarks"):
        files = [f.get("path", "") for f in pr.get("files") or []]
        has_rn = any(
            p.startswith("docs/release-notes/") or p == "CHANGELOG.md" for p in files
        )
        chore = label_names & {"chore", "dependencies", "dependabot"}
        _check(
            "release_notes",
            has_rn or bool(chore),
            "no CHANGELOG.md or docs/release-notes/* in PR (required unless chore/deps)",
            blockers,
            checks,
        )

    ready = len(blockers) == 0
    return GateResult(repo_name, number, url, ready, checks, blockers)


def list_merge_candidates(repo: str | None = None) -> list[GateResult]:
    repos = [repo] if repo else list(ORG_REPOS)
    out: list[GateResult] = []
    for r in repos:
        rows = gh_json(
            [
                "pr",
                "list",
                "--repo",
                f"li-langverse/{r}",
                "--state",
                "open",
                "--label",
                MERGE_APPROVED,
                "--json",
                "number",
                "--limit",
                "20",
            ]
        )
        if not rows:
            continue
        for row in rows:
            out.append(evaluate_pr(r, row["number"]))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="PR merge gate for li-langverse")
    parser.add_argument("--repo", help="repo name or org/repo")
    parser.add_argument("--pr", type=int, help="PR number")
    parser.add_argument("--sweep", action="store_true", help="all open PRs with merge-approved")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-approval", action="store_true")
    parser.add_argument("--no-release-notes", action="store_true")
    parser.add_argument(
        "--allow-governance",
        action="store_true",
        help="allow roadmap governance merges",
    )
    args = parser.parse_args()

    if not subprocess.run(["which", "gh"], capture_output=True).returncode == 0:
        print("gh CLI required", file=sys.stderr)
        return 1

    if args.sweep:
        results = list_merge_candidates(args.repo)
    elif args.repo and args.pr:
        results = [
            evaluate_pr(
                args.repo,
                args.pr,
                require_approval=not args.no_approval,
                require_release_notes=not args.no_release_notes,
                allow_governance=args.allow_governance,
            )
        ]
    else:
        parser.error("use --repo + --pr or --sweep")

    payload = {
        "results": [r.to_dict() for r in results],
        "ready": [r.to_dict() for r in results if r.ready],
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for r in results:
            status = "READY" if r.ready else "BLOCKED"
            print(f"{status} {r.repo}#{r.number} {r.url}")
            for b in r.blockers:
                print(f"  - {b}")

    return 0 if all(r.ready for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
