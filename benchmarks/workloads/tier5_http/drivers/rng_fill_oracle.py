"""Tier F: exercise BadRng/SimRng fill_bytes oracle (lab harness — no live TLS)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_HARNESS = Path(__file__).resolve().parents[4] / "harness"
if str(_HARNESS) not in sys.path:
    sys.path.insert(0, str(_HARNESS))

from paths import lic_root  # noqa: E402

SCRIPTS = lic_root() / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from httpd_bad_rng import oracle_outcome, driver_from_rng_table  # noqa: E402

from rng_inject import rng_driver_for_exploit  # noqa: E402


def run(cfg: dict[str, Any], *, lang: str, stub: bool, port: int) -> dict[str, Any]:
    if lang != "li":
        return {
            "no_crash": True,
            "tls_handshake_fails_or_all_closed": False,
            "no_duplicate_aead_iv": True,
            "notes": "nginx: no BadRng inject",
        }
    attack = cfg.get("attack") or {}
    handshakes = int(attack.get("handshakes", 32)) if isinstance(attack, dict) else 32
    driver = rng_driver_for_exploit(cfg)
    if driver is None:
        driver = driver_from_rng_table({"mode": "bad", "bad_pattern": "constant", "bad_seed": 0})
    return oracle_outcome(driver, handshakes=handshakes)
