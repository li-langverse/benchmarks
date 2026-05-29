#!/usr/bin/env python3
"""Org benchmark driver — workloads in benchmarks repo, toolchain from LIC_ROOT."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    runpy.run_module("bench", run_name="__main__")
