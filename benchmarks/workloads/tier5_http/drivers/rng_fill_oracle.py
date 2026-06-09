"""Tier F: exercise BadRng/SimRng fill_bytes oracle (lab harness — no live TLS)."""

from __future__ import annotations

import sys
from typing import Any

from _driver_common import HARNESS, SCRIPTS

for p in (str(SCRIPTS), str(HARNESS)):
    if p not in sys.path:
        sys.path.insert(0, p)

from httpd_bad_rng import driver_from_rng_table, oracle_outcome  # noqa: E402
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
