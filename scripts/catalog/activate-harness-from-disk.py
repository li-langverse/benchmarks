#!/usr/bin/env python3
"""Clear harness pending in catalog.toml when workload harness.toml exists."""
from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
WORKLOADS = ROOT / "benchmarks" / "workloads"


def resolve_workload_dir(bid: str, path: str) -> Path | None:
    if path and path not in ("unknown", ""):
        p = path.replace("\\", "/")
        for cand in (
            ROOT / p,
            ROOT / p.replace("benchmarks/tier", "benchmarks/workloads/tier", 1),
        ):
            if cand.is_dir():
                return cand
    if WORKLOADS.is_dir():
        for tier in WORKLOADS.iterdir():
            d = tier / bid
            if d.is_dir():
                return d
    return None


def problem_size_from_params(wdir: Path) -> str | None:
    params = wdir / "params.toml"
    if not params.is_file():
        return None
    doc = tomllib.loads(params.read_text(encoding="utf-8"))
    parts: list[str] = []
    for key in ("N", "nx", "ny", "steps", "n", "size"):
        if key in doc:
            parts.append(f"{key}={doc[key]}")
    return ",".join(parts[:4]) if parts else wdir.name


def patch_block(block: str, bid: str, wdir: Path) -> tuple[str, bool]:
    if 'size_label = "harness pending"' not in block:
        return block, False
    if not (wdir / "harness.toml").is_file():
        return block, False
    out = re.sub(r'\nsize_label = "harness pending"\s*\n', "\n", block, count=1)
    ps = problem_size_from_params(wdir)
    if ps and "problem_size" not in out:
        out = out.replace(f'id = "{bid}"\n', f'id = "{bid}"\nproblem_size = "{ps}"\n', 1)
    return out, out != block


def main() -> int:
    doc = tomllib.loads(CATALOG.read_text(encoding="utf-8"))
    text = CATALOG.read_text(encoding="utf-8")
    blocks = re.split(r"(?=^\[\[benchmark\]\])", text, flags=re.MULTILINE)
    updated = 0
    new_blocks: list[str] = []
    for block in blocks:
        if not block.strip():
            new_blocks.append(block)
            continue
        m = re.search(r'^id = "([^"]+)"', block, re.MULTILINE)
        if not m:
            new_blocks.append(block)
            continue
        bid = m.group(1)
        cfg = next((b for b in doc["benchmark"] if b["id"] == bid), {})
        wdir = resolve_workload_dir(bid, str(cfg.get("path", "")))
        if wdir:
            block, changed = patch_block(block, bid, wdir)
            if changed:
                updated += 1
        new_blocks.append(block)
    out = "".join(new_blocks)
    if updated:
        CATALOG.write_text(out, encoding="utf-8")
    pending = sum(
        1 for b in tomllib.loads(out)["benchmark"] if b.get("size_label") == "harness pending"
    )
    print(f"activated {updated} harness-pending entries")
    print(f"harness pending remaining: {pending}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
