#!/usr/bin/env python3
"""Audit li-langverse repos for roadmap agent-kit (Cursor rules, hooks, version stamp).

Writes data/latest/org-agent-kit-audit.json

Usage:
  python3 scripts/ensure-org-agent-kit.py
  python3 scripts/ensure-org-agent-kit.py --repo lip
  python3 scripts/ensure-org-agent-kit.py --local-only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/org-agent-kit-audit.json"
ORG = "li-langverse"
ROADMAP = Path(os.environ.get("ROADMAP_ROOT", ROOT.parent / "roadmap"))
KIT = ROADMAP / "agent-kit"

REQUIRED_RULES = [
    ".cursor/rules/li-pr-only.mdc",
    ".cursor/rules/li-ecosystem-gates.mdc",
    ".cursor/rules/li-release-notes.mdc",
]

# Org repos that must carry synced agent-kit (code + agent runners).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from org_repos import CORE_AGENT_KIT_REPOS  # noqa: E402

LOCAL_DIR_ALIASES: dict[str, list[str]] = {
    "lic": ["lic", "li"],
}


def hash_kit_cursor() -> str:
    root = KIT / ".cursor"
    h = hashlib.sha256()
    for dirpath, _, files in os.walk(root):
        for f in sorted(files):
            p = Path(dirpath) / f
            rel = p.relative_to(root)
            h.update(str(rel).encode())
            h.update(p.read_bytes())
    return h.hexdigest()[:16]


def canonical_stamp() -> str:
    manifest = tomllib.load(open(KIT / "manifest.toml", "rb"))
    version = manifest.get("version", "unknown")
    return f"{version}+{hash_kit_cursor()}"


def gh_json(args: list[str]):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def list_org_repos() -> list[str]:
    rows = gh_json(["repo", "list", ORG, "--limit", "100", "--json", "name,isArchived"])
    if not rows:
        return CORE_AGENT_KIT_REPOS
    return sorted(r["name"] for r in rows if not r.get("isArchived"))


def resolve_local_dir(repo: str) -> Path | None:
    for name in LOCAL_DIR_ALIASES.get(repo, [repo]):
        candidate = ROOT.parent / name
        if candidate.is_dir():
            return candidate
    return None


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8").strip()


def audit_local(repo: str, stamp: str) -> dict:
    root = resolve_local_dir(repo)
    if root is None:
        return {
            "repo": repo,
            "present_locally": False,
            "status": "missing_local_clone",
        }

    cursor_stamp = read_text(root / ".cursor" / "agent-kit-version")
    expected_stamp = read_text(root / "scripts" / "expected-agent-kit-version")
    sync_script = root / "scripts" / "sync-agent-kit.sh"
    missing_rules = [r for r in REQUIRED_RULES if not (root / r).is_file()]
    agents_md = (root / "AGENTS.md").is_file()

    drift = cursor_stamp != stamp or expected_stamp != stamp
    missing_kit = cursor_stamp is None

    if missing_kit:
        status = "missing_kit"
    elif drift:
        status = "drift"
    elif missing_rules:
        status = "missing_rules"
    elif not sync_script.is_file():
        status = "missing_sync_script"
    else:
        status = "ok"

    return {
        "repo": repo,
        "present_locally": True,
        "local_path": str(root),
        "status": status,
        "cursor_stamp": cursor_stamp,
        "expected_stamp": expected_stamp,
        "canonical_stamp": stamp,
        "missing_rules": missing_rules,
        "has_sync_script": sync_script.is_file(),
        "has_agents_md": agents_md,
        "fix": (
            f"cd {root} && ../roadmap/scripts/install-agent-kit.sh {repo}"
            if status != "ok"
            else None
        ),
    }


def gh_has_file(repo: str, path: str) -> bool:
    proc = subprocess.run(
        ["gh", "api", f"repos/{ORG}/{repo}/contents/{path}", "-q", ".sha"],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0 and bool(proc.stdout.strip())


def audit_remote(repo: str, stamp: str) -> dict:
    cursor_raw = None
    proc = subprocess.run(
        ["gh", "api", f"repos/{ORG}/{repo}/contents/.cursor/agent-kit-version", "-q", ".content"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0 and proc.stdout.strip():
        import base64

        cursor_raw = base64.b64decode(proc.stdout.strip()).decode("utf-8").strip()

    missing_rules = [r for r in REQUIRED_RULES if not gh_has_file(repo, r)]
    has_sync = gh_has_file(repo, "scripts/sync-agent-kit.sh")

    if cursor_raw is None:
        status = "missing_kit"
    elif cursor_raw != stamp:
        status = "drift"
    elif missing_rules:
        status = "missing_rules"
    elif not has_sync:
        status = "missing_sync_script"
    else:
        status = "ok"

    return {
        "repo": repo,
        "status": status,
        "cursor_stamp": cursor_raw,
        "canonical_stamp": stamp,
        "missing_rules": missing_rules,
        "has_sync_script": has_sync,
        "fix": f"../roadmap/scripts/install-agent-kit.sh {repo}" if status != "ok" else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit org repos for agent-kit compliance")
    parser.add_argument("--repo", action="append", dest="repos", help="limit to repo(s)")
    parser.add_argument("--local-only", action="store_true", help="only audit sibling clones")
    parser.add_argument("--json-out", type=Path, default=OUT)
    args = parser.parse_args()

    if not KIT.is_dir():
        print(f"roadmap agent-kit not found: {KIT}", file=sys.stderr)
        return 1

    stamp = canonical_stamp()
    repos = args.repos if args.repos else sorted(set(CORE_AGENT_KIT_REPOS) | set(list_org_repos()))

    entries: list[dict] = []
    for repo in repos:
        local = audit_local(repo, stamp)
        if args.local_only:
            entries.append(local)
        elif local.get("present_locally"):
            entries.append(local)
        else:
            if subprocess.run(["which", "gh"], capture_output=True).returncode == 0:
                entries.append(audit_remote(repo, stamp))
            else:
                entries.append(local)

    needing = [e for e in entries if e.get("status") not in ("ok", "missing_local_clone")]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

    report = {
        "generated_at": now,
        "org": ORG,
        "canonical_stamp": stamp,
        "roadmap_kit": str(KIT),
        "required_rules": REQUIRED_RULES,
        "policy": "docs/ecosystem/ADOPTION.md",
        "repos_ok": [e["repo"] for e in entries if e.get("status") == "ok"],
        "repos_needing_sync": needing,
        "entries": entries,
    }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.json_out}")
    print(f"canonical: {stamp}")
    print(f"OK: {len(report['repos_ok'])}  needing sync: {len(needing)}")
    for e in needing[:12]:
        print(f"  - {e['repo']}: {e.get('status')}")
    return 1 if needing else 0


if __name__ == "__main__":
    raise SystemExit(main())
