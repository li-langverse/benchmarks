"""Read/write catalog.toml preserving [reporting] and trailing sections."""
from __future__ import annotations

import re
import tomllib
from pathlib import Path

REPORTING_MARKER = re.compile(r"\n\[reporting\]\s*\n", re.MULTILINE)


def split_catalog_text(text: str) -> tuple[str, str, str]:
    """Return (header, benchmarks_body, footer) where body holds [[benchmark]] blocks only."""
    m = REPORTING_MARKER.search(text)
    if m:
        footer = text[m.start() + 1 :]
        prefix = text[: m.start() + 1]
    else:
        footer = ""
        prefix = text
    idx = prefix.find("[[benchmark]]")
    if idx < 0:
        raise ValueError("catalog.toml: no [[benchmark]] sections")
    header = prefix[:idx].rstrip() + "\n\n"
    body = prefix[idx:].rstrip() + "\n"
    return header, body, footer


def load_benchmarks(catalog_path: Path) -> tuple[str, list[dict], str]:
    text = catalog_path.read_text(encoding="utf-8")
    header, _body, footer = split_catalog_text(text)
    data = tomllib.loads(text)
    return header, [dict(b) for b in data.get("benchmark", [])], footer


def write_catalog(
    catalog_path: Path,
    *,
    header: str,
    benchmarks: list[dict],
    footer: str,
    format_benchmark,
) -> None:
    parts = [header.rstrip(), ""]
    parts.append("\n\n".join(format_benchmark(b) for b in benchmarks))
    if footer.strip():
        parts.append("")
        parts.append(footer.rstrip())
    catalog_path.write_text("\n".join(parts) + "\n", encoding="utf-8")
