#!/usr/bin/env python3
"""Write manifest.json + visuals.zip for benchmark shareables (download links for PRs)."""
from __future__ import annotations

import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data/visuals/latest"


def main() -> int:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    if not out_dir.is_dir():
        print(f"missing {out_dir}", file=sys.stderr)
        return 1

    files: list[dict] = []
    for p in sorted(out_dir.iterdir()):
        if p.suffix.lower() not in (".png", ".gif", ".zip", ".json"):
            continue
        if p.name == "manifest.json":
            continue
        files.append(
            {
                "name": p.name,
                "bytes": p.stat().st_size,
                "kind": "animation" if p.suffix.lower() == ".gif" else "plot",
            }
        )

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%MZ")
    zip_path = out_dir / f"benchmark-visuals-{ts}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out_dir.iterdir()):
            if p.suffix.lower() in (".png", ".gif") and p.is_file():
                zf.write(p, arcname=p.name)

    branch = "BRANCH"  # agent replaces after push
    repo = "li-langverse/benchmarks"
    base_raw = f"https://raw.githubusercontent.com/{repo}/{branch}/data/visuals/latest"

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dashboard": "https://li-langverse.github.io/benchmarks/",
        "source_lic_share": "lic/benchmarks/results/share/",
        "zip": zip_path.name,
        "zip_bytes": zip_path.stat().st_size if zip_path.is_file() else 0,
        "files": files,
        "download_links_template": {
            "note": "Replace BRANCH with your PR branch after push",
            "zip": f"{base_raw}/{zip_path.name}",
            "example_png": f"{base_raw}/bench_speed_tier2.png",
        },
        "physics_priority": [
            "md_lennard_jones_energy_overlay.png",
            "md_lennard_jones_energy_by_lang.png",
            "md_lennard_jones_li.gif",
            "md_lennard_jones_cpp.gif",
            "bench_speed_tier2.png",
            "speedup_vs_cpp.png",
        ],
    }

    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_dir / 'manifest.json'} ({len(files)} assets, zip {zip_path.name})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
