#!/usr/bin/env python3
"""Mark tier-5 HTTP catalog rows planned when scenario harness dir is absent."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"

MISSING_SCENARIO_IDS = (
    "https_static",
    "lb_least_conn",
    "lb_peer_down",
    "lb_round_robin",
)


def load_header(text: str) -> str:
    idx = text.find("[[benchmark]]")
    return text[:idx].rstrip() + "\n\n" if idx != -1 else ""


def format_benchmark(b: dict) -> str:
    lines = ["[[benchmark]]", f'id = "{b["id"]}"']
    skip = {"id", "ph_ids"}
    for key, val in b.items():
        if key in skip:
            continue
        if val is None:
            continue
        if isinstance(val, bool):
            lines.append(f"{key} = {'true' if val else 'false'}")
        elif isinstance(val, (int, float)):
            lines.append(f"{key} = {val}")
        else:
            lines.append(f'{key} = "{val}"')
    ph = b.get("ph_ids") or []
    if ph:
        lines.append("ph_ids = [" + ", ".join(f'"{p}"' for p in ph) + "]")
    return "\n".join(lines)


def main() -> int:
    import tomllib

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.write:
        parser.error("pass --dry-run or --write")

    text = CATALOG.read_text(encoding="utf-8")
    benches = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    fixes: list[str] = []
    for b in benches:
        bid = b.get("id")
        if bid not in MISSING_SCENARIO_IDS:
            continue
        rel = str(b.get("path") or "")
        if rel and (ROOT / rel).is_dir():
            continue
        fixes.append(str(bid))
        if args.write:
            b["path"] = "unknown"
            b["catalog_lifecycle"] = "planned"
            b["variant"] = "vertical_stub"

    print(f"planned tier5 stubs: {len(fixes)}", fixes)
    if not args.write:
        return 0

    header = load_header(text)
    CATALOG.write_text(header + "\n\n".join(format_benchmark(b) for b in benches) + "\n")
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
