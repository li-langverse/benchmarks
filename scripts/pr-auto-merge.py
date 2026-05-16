#!/usr/bin/env python3
"""Merge a PR when pr-merge-gate.py passes. Default: dry-run."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts" / "pr-merge-gate.py"


def run_gate(repo: str, pr: int, allow_governance: bool) -> dict:
    args = [
        sys.executable,
        str(GATE),
        "--repo",
        repo,
        "--pr",
        str(pr),
        "--json",
    ]
    if allow_governance:
        args.append("--allow-governance")
    proc = subprocess.run(args, capture_output=True, text=True, check=False)
    if proc.returncode != 0 and not proc.stdout.strip():
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(proc.returncode)
    data = json.loads(proc.stdout)
    results = data.get("results") or []
    if not results:
        raise SystemExit("no gate result")
    return results[0]


def merge_pr(repo: str, pr: int, method: str, delete_branch: bool) -> None:
    full = f"li-langverse/{repo}" if "/" not in repo else repo
    args = ["gh", "pr", "merge", str(pr), "--repo", full, f"--{method}"]
    if delete_branch:
        args.append("--delete-branch")
    subprocess.check_call(args)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="actually merge (default is dry-run)",
    )
    parser.add_argument(
        "--method",
        choices=("squash", "merge", "rebase"),
        default="squash",
    )
    parser.add_argument("--no-delete-branch", action="store_true")
    parser.add_argument("--allow-governance", action="store_true")
    args = parser.parse_args()

    result = run_gate(args.repo, args.pr, args.allow_governance)
    if not result.get("ready"):
        print(json.dumps(result, indent=2), file=sys.stderr)
        print("merge gate failed", file=sys.stderr)
        return 1

    if not args.execute:
        print(f"DRY-RUN: would merge {args.repo}#{args.pr} ({args.method})")
        print(json.dumps(result, indent=2))
        return 0

    merge_pr(args.repo, args.pr, args.method, delete_branch=not args.no_delete_branch)
    print(f"merged {args.repo}#{args.pr}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
