#!/usr/bin/env python3
"""Run li-cursor-agents ux-harness; write ui-audit.json and ux-audit.json."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / "data" / "latest"
AGENTS_ROOT = Path(
    os.environ.get("LI_CURSOR_AGENTS_ROOT", ROOT.parent / "li-cursor-agents")
).resolve()
HARNESS = AGENTS_ROOT / "ux-harness" / "run_audit.py"
MANIFEST = AGENTS_ROOT / "config" / "ux-targets.json"


def maybe_build_lic_docs(build_lic: bool, mock: bool) -> int:
    if mock or not build_lic:
        return 0
    build_script = ROOT / "scripts" / "build-lic-docs.py"
    if not build_script.is_file():
        print(f"missing {build_script}", file=sys.stderr)
        return 1
    proc = subprocess.run(
        [sys.executable, str(build_script)],
        cwd=str(ROOT),
        check=False,
    )
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Use harness mock mode (CI default)")
    parser.add_argument("--quick", action="store_true", help="Alias for --mock")
    parser.add_argument(
        "--build-lic",
        action="store_true",
        help="Build lic MkDocs site before audit (non-mock extended CI)",
    )
    args = parser.parse_args()
    mock = args.mock or args.quick

    LATEST.mkdir(parents=True, exist_ok=True)

    code = maybe_build_lic_docs(args.build_lic, mock)
    if code != 0:
        return code

    if not HARNESS.is_file():
        print(f"ux-harness missing: {HARNESS}", file=sys.stderr)
        return 1

    cmd = [
        sys.executable,
        str(HARNESS),
        "--all",
        "--manifest",
        str(MANIFEST),
        "--out-dir",
        str(LATEST),
    ]
    if mock:
        cmd.append("--mock")

    proc = subprocess.run(cmd, cwd=str(AGENTS_ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return proc.returncode

    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mock": mock,
        "agents_root": str(AGENTS_ROOT),
    }
    (LATEST / "ui-ux-audit-meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    for name in ("ui-audit.json", "ux-audit.json"):
        if not (LATEST / name).is_file():
            print(f"missing output {name}", file=sys.stderr)
            return 1

    print(json.dumps({"ok": True, "mock": mock, "latest": str(LATEST)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
