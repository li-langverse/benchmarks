"""tier-7 registry alias sharding for parallel nightly CI."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness"))

from bench_registry import registry_alias_specs, shard_registry_alias_specs  # noqa: E402


class TestBenchRegistryShard(unittest.TestCase):
    def test_registry_alias_count(self):
        specs = registry_alias_specs()
        self.assertEqual(len(specs), 96)

    def test_round_robin_covers_all_without_duplicates(self):
        specs = registry_alias_specs()
        shard_count = 3
        seen: list[str] = []
        for shard in range(shard_count):
            part = shard_registry_alias_specs(specs, shard=shard, shard_count=shard_count)
            names = [s.name for s in part]
            self.assertEqual(len(names), len(set(names)))
            seen.extend(names)
        self.assertEqual(len(seen), len(specs))
        self.assertEqual(sorted(seen), sorted(s.name for s in specs))

    def test_shards_are_balanced(self):
        specs = registry_alias_specs()
        sizes = [
            len(shard_registry_alias_specs(specs, shard=i, shard_count=3))
            for i in range(3)
        ]
        self.assertEqual(sum(sizes), len(specs))
        self.assertLessEqual(max(sizes) - min(sizes), 1)


if __name__ == "__main__":
    unittest.main()
