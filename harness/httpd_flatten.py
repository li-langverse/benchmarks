"""Resolve httpd config flatten pipeline (Li default; Python deprecated rollback)."""

from __future__ import annotations

import os
import subprocess
import sys
import warnings
from pathlib import Path

from paths import BENCH_REPO, lic_root


def httpd_config_pipeline() -> str:
    v = str(os.environ.get("LI_HTTPD_CONFIG_PIPELINE", "li")).strip().lower()
    return v if v in ("python", "li") else "li"


def li_httpd_root() -> Path | None:
    raw = os.environ.get("LI_HTTPD_ROOT", "").strip()
    if raw:
        p = Path(raw).resolve()
        return p if (p / "li-httpd").is_file() or (p / "scripts/flatten-httpd-config-li.sh").is_file() else None
    for cand in (
        BENCH_REPO.parent / "li-httpd",
        lic_root().parent / "li-httpd",
    ):
        if (cand / "scripts/flatten-httpd-config-li.sh").is_file():
            return cand.resolve()
    # Isolated agent workspace: .../li-httpd/<run>/repo
    parent = BENCH_REPO.parent
    if parent.name == "li-httpd":
        runs = sorted(parent.glob("*/repo"), key=lambda p: p.stat().st_mtime, reverse=True)
        for r in runs:
            if (r / "scripts/flatten-httpd-config-li.sh").is_file():
                return r.resolve()
    return None


def flatten_httpd_config(toml_path: Path, out_conf: Path, *, cwd: Path | None = None) -> None:
    """Flatten server.toml → runtime.conf using the active pipeline."""
    pipeline = httpd_config_pipeline()
    if pipeline == "li":
        root = li_httpd_root()
        if root is None:
            raise RuntimeError(
                "LI_HTTPD_CONFIG_PIPELINE=li but LI_HTTPD_ROOT / sibling li-httpd not found"
            )
        wrapper = root / "li-httpd"
        if wrapper.is_file():
            cmd = [str(wrapper), "config", "flatten", str(toml_path.resolve()), "-o", str(out_conf)]
            run_cwd = root
        else:
            script = root / "scripts" / "flatten-httpd-config-li.sh"
            cmd = ["bash", str(script), str(toml_path.resolve()), "-o", str(out_conf)]
            run_cwd = root
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=run_cwd)
        if proc.returncode != 0:
            raise RuntimeError((proc.stderr or proc.stdout or "Li flatten failed").strip())
        return

    warnings.warn(
        "LI_HTTPD_CONFIG_PIPELINE=python is deprecated; use li (see li-httpd/docs/config-pipeline.md)",
        DeprecationWarning,
        stacklevel=2,
    )
    script = lic_root() / "scripts" / "flatten-httpd-config.py"
    if not script.is_file():
        raise RuntimeError(f"missing python flatten script: {script}")
    proc = subprocess.run(
        [sys.executable, str(script), str(toml_path.resolve()), "-o", str(out_conf)],
        capture_output=True,
        text=True,
        cwd=cwd or lic_root(),
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "python flatten failed").strip())
