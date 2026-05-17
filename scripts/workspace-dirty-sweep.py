#!/usr/bin/env python3
"""Detect uncommitted work in sibling Li ecosystem clones (preflight for workspace_sweeper).

Writes data/latest/workspace-dirty-sweep.json — used by agent-briefing recommend_agents.

Usage:
  python3 scripts/workspace-dirty-sweep.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/workspace-dirty-sweep.json"
SECRET = re.compile(
    r"(?:^|/)(?:\.env(?:\.|$)|\.env\.github|credentials\.json|\.pem$|id_rsa$|node_modules/)",
    re.I,
)


def git(*args: str, cwd: Path) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip() if proc.returncode == 0 else ""


def test_commands(repo: Path) -> list[str]:
    cmds: list[str] = []
    pkg = repo / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            scripts = data.get("scripts") or {}
            if scripts.get("test") and "no test specified" not in str(scripts.get("test", "")).lower():
                cmds.append("npm test")
        except json.JSONDecodeError:
            pass
    if (repo / "li-tests" / "run_all.sh").is_file():
        cmds.append("./li-tests/run_all.sh")
    return cmds


def scan_repo(path: Path) -> dict | None:
    if not (path / ".git").is_dir():
        return None
    porcelain = git("status", "--porcelain", cwd=path)
    if not porcelain:
        return None
    files = [ln[3:].strip() for ln in porcelain.splitlines() if ln[3:].strip()]
    safe = [f for f in files if not SECRET.search(f)]
    if not safe:
        return None
    remote = git("remote", "get-url", "origin", cwd=path)
    repo_name = path.name
    org = os.environ.get("GH_ORG", "li-langverse")
    m = re.search(r"github\.com[:/]([^/]+)/([^/.]+)", remote)
    if m:
        org, repo_name = m.group(1), m.group(2).replace(".git", "")
    return {
        "path": str(path.resolve()),
        "repo": repo_name,
        "org": org,
        "branch": git("branch", "--show-current", cwd=path) or "HEAD",
        "changed_files": len(safe),
        "safe_files": safe[:40],
        "test_commands": test_commands(path),
    }


def main() -> int:
    anchor = Path(os.environ.get("LI_ECOSYSTEM_ROOT", ROOT.parent))
    names = os.environ.get(
        "LI_WORKSPACE_SWEEP_REPO_NAMES", "lic,benchmarks,roadmap,li-cursor-agents,li"
    ).split(",")
    dirty: list[dict] = []
    for name in names:
        name = name.strip()
        if not name:
            continue
        row = scan_repo(anchor / name)
        if row:
            dirty.append(row)
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "ecosystem_root": str(anchor),
        "dirty_count": len(dirty),
        "dirty_repos": dirty,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} dirty_count={len(dirty)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
