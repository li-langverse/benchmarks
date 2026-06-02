"""Shared helpers for tier5_http exploit stub drivers."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Repo root: …/benchmarks/benchmarks/workloads/tier5_http/drivers → parents[4]
_REPO = Path(__file__).resolve().parents[4]
if str(_REPO / "harness") not in sys.path:
    sys.path.insert(0, str(_REPO / "harness"))

from httpd_flatten import flatten_httpd_config, httpd_config_pipeline  # noqa: E402
from paths import lic_root  # noqa: E402

REPO = lic_root()
SCRIPTS = REPO / "scripts"


def flatten_config(server_config: Path) -> str:
    tmp = Path("/tmp") / f"li_exploit_flatten_{server_config.stem}.conf"
    flatten_httpd_config(server_config, tmp, cwd=REPO)
    return tmp.read_text(encoding="utf-8")


def leak_censor_enabled_in_flatten(server_config: Path) -> bool:
    text = flatten_config(server_config)
    for line in text.splitlines():
        if line.startswith("leak_censor_enabled="):
            val = line.split("=", 1)[1].strip()
            return val not in ("0", "false")
    return False


def run_oracle(name: str) -> bool:
    import subprocess

    path = REPO / "build" / name
    if not path.is_file():
        path = Path(f"/tmp/{name}")
    if not path.is_file() or not path.stat().st_mode & 0o111:
        return False
    proc = subprocess.run([str(path)], cwd=REPO, capture_output=True)
    return proc.returncode == 0


def resolve_server_config(cfg: dict[str, Any]) -> Path:
    from http_exploit_toml import resolve_server_config as _resolve

    return _resolve(cfg)
