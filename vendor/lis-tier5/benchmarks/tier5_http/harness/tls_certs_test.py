#!/usr/bin/env python3
"""Unit tests for tls_certs (skip when openssl missing)."""
from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from tls_certs import TlsCertSpec, default_tls_specs, generate_tls_material, parse_tls_specs


@unittest.skipUnless(shutil.which("openssl"), "openssl required")
class TlsCertsTest(unittest.TestCase):
    def test_rsa2048_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mat = generate_tls_material(Path(tmp), TlsCertSpec(id="rsa2048-leaf"))
            self.assertIsNotNone(mat)
            assert mat is not None
            self.assertTrue(mat.cert.is_file())
            self.assertTrue(mat.key.is_file())

    def test_chain3(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mat = generate_tls_material(Path(tmp), TlsCertSpec(id="rsa2048-chain3", chain_depth=3))
            self.assertIsNotNone(mat)
            assert mat is not None
            blob = mat.cert.read_text(encoding="utf-8")
            self.assertGreaterEqual(blob.count("BEGIN CERTIFICATE"), 2)

    def test_parse_matrix(self) -> None:
        specs = parse_tls_specs({"tls": {"matrix": True}}, quick=True)
        self.assertEqual(2, len(specs))
        self.assertEqual(7, len(default_tls_specs(quick=False)))


if __name__ == "__main__":
    unittest.main()
