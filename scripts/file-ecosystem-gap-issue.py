#!/usr/bin/env python3
"""File a standardized ecosystem-gap issue for planner automations to pick up."""
from __future__ import annotations

import argparse
import subprocess
import sys
import textwrap


def build_body(
    what_tried: str,
    expected: str,
    blocked: str,
    catalog_path: str,
    parent: int | None,
) -> str:
    parent_line = f"\nParent / related issue: #{parent}\n" if parent else ""
    return textwrap.dedent(
        f"""\
        ## Ecosystem gap

        Shared tooling should have covered this work ([ecosystem-first](https://github.com/li-langverse/benchmarks/blob/main/docs/ecosystem/ecosystem-first.md)).

        ### What I tried
        {what_tried.strip()}

        ### Expected (catalog behavior)
        {expected.strip()}

        ### Blocked / error
        {blocked.strip()}

        ### Catalog checked
        - [{catalog_path}](https://github.com/li-langverse/benchmarks/blob/main/{catalog_path})
        {parent_line}
        ## Agent instructions

        - [ ] **issue-feature-planner** (or human) drafts plan: extend catalog vs new script in `roadmap/agent-kit`
        - [ ] Label **`plan-approved`** before implementation PR
        - [ ] Update **tooling-catalog.md** in the same PR as the fix

        /cc automation — `ecosystem-gap` + `plan-needed`
        """
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="File ecosystem-gap GitHub issue")
    parser.add_argument("--repo", required=True, help="repo name or org/repo")
    parser.add_argument("--title", required=True, help="short title (prefix added if missing)")
    parser.add_argument("--what-tried", required=True)
    parser.add_argument("--expected", required=True)
    parser.add_argument("--blocked", required=True)
    parser.add_argument("--parent", type=int, default=None, help="related issue number")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    full = args.repo if "/" in args.repo else f"li-langverse/{args.repo}"
    title = args.title
    if not title.lower().startswith("[ecosystem gap]"):
        title = f"[Ecosystem gap] {title}"

    body = build_body(
        args.what_tried,
        args.expected,
        args.blocked,
        "docs/ecosystem/tooling-catalog.md",
        args.parent,
    )

    if args.dry_run:
        print(f"repo: {full}\ntitle: {title}\n\n{body}")
        return 0

    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("gh CLI required", file=sys.stderr)
        return 1

    cmd = [
        "gh",
        "issue",
        "create",
        "--repo",
        full,
        "--title",
        title,
        "--body",
        body,
        "--label",
        "ecosystem-gap",
        "--label",
        "plan-needed",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return proc.returncode
    print(proc.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
