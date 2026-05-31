#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
rows = json.loads((ROOT / "data/latest/summary.json").read_text())["rows"]
sk = [r for r in rows if r.get("status") == "skip"]
print("skip by os", Counter(r.get("os") for r in sk))
print("skip by tier", Counter(r.get("tier") for r in sk))
print("skip by package", Counter(r.get("package") for r in sk))
print("status totals", Counter(r.get("status") for r in rows))
