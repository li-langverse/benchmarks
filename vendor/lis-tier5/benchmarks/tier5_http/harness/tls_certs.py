"""Generate TLS certificate material for tier-5 HTTPS benchmarks.

Supports key algorithms (RSA/EC/Ed25519), chain depth, and long subject DNs for
fair cross-oracle comparison (nginx, caddy, traefik, apache, lighttpd, li-httpd).
"""
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TlsCertSpec:
    id: str
    key_type: str = "rsa"  # rsa | ec | ed25519
    key_bits: int = 2048
    curve: str = "P-256"  # P-256 | P-384 for ec
    chain_depth: int = 1  # 1=leaf only, 2=leaf+intermediate, 3=leaf+inter+root in chain PEM
    subject_cn: str = "127.0.0.1"
    long_subject: bool = False

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> TlsCertSpec:
        return cls(
            id=str(raw.get("id") or "rsa2048-leaf"),
            key_type=str(raw.get("key_type") or raw.get("key") or "rsa").lower(),
            key_bits=int(raw.get("key_bits") or raw.get("bits") or 2048),
            curve=str(raw.get("curve") or "P-256"),
            chain_depth=max(1, min(3, int(raw.get("chain_depth") or 1))),
            subject_cn=str(raw.get("subject_cn") or "127.0.0.1"),
            long_subject=bool(raw.get("long_subject")),
        )


@dataclass
class TlsCertMaterial:
    cert: Path
    key: Path
    spec: TlsCertSpec
    chain_pem: Path | None = None


def default_tls_specs(*, quick: bool = False) -> list[TlsCertSpec]:
    """Default cert matrix for nightly HTTPS benches."""
    core = [
        TlsCertSpec(id="rsa2048-leaf", key_type="rsa", key_bits=2048, chain_depth=1),
        TlsCertSpec(id="rsa4096-leaf", key_type="rsa", key_bits=4096, chain_depth=1),
        TlsCertSpec(id="ecdsa-p256-leaf", key_type="ec", curve="P-256", chain_depth=1),
        TlsCertSpec(id="ecdsa-p384-leaf", key_type="ec", curve="P-384", chain_depth=1),
        TlsCertSpec(id="ed25519-leaf", key_type="ed25519", chain_depth=1),
        TlsCertSpec(id="rsa2048-chain3", key_type="rsa", key_bits=2048, chain_depth=3),
        TlsCertSpec(
            id="rsa2048-long-subject",
            key_type="rsa",
            key_bits=2048,
            chain_depth=1,
            long_subject=True,
        ),
    ]
    if quick:
        return [core[0], core[2]]
    return core


def parse_tls_specs(cfg: dict[str, Any], *, quick: bool) -> list[TlsCertSpec]:
    tls = cfg.get("tls") or {}
    raw_variants = tls.get("variants")
    if raw_variants:
        return [TlsCertSpec.from_dict(v) for v in raw_variants if isinstance(v, dict)]
    if tls.get("matrix"):
        return default_tls_specs(quick=quick)
    return [TlsCertSpec(id="rsa2048-leaf")]


def _subject_dn(spec: TlsCertSpec) -> str:
    if spec.long_subject:
        pad = "x" * 512
        return f"/CN={spec.subject_cn}/OU={pad}/O=li-tier5-bench/C=US"
    return f"/CN={spec.subject_cn}/O=li-tier5-bench/C=US"


def _run_openssl(args: list[str], *, cwd: Path | None = None) -> bool:
    openssl = shutil.which("openssl")
    if not openssl:
        return False
    proc = subprocess.run(
        [openssl, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0


def _gen_key(key_path: Path, spec: TlsCertSpec) -> bool:
    if spec.key_type == "ed25519":
        return _run_openssl(["genpkey", "-algorithm", "ED25519", "-out", str(key_path)])
    if spec.key_type == "ec":
        curve = spec.curve.replace("P-", "prime256v1" if spec.curve == "P-256" else "secp384r1")
        if spec.curve == "P-384":
            curve = "secp384r1"
        elif spec.curve == "P-256":
            curve = "prime256v1"
        return _run_openssl(["genpkey", "-algorithm", "EC", "-pkeyopt", f"ec_paramgen_curve:{curve}", "-out", str(key_path)])
    bits = max(2048, spec.key_bits)
    return _run_openssl(["genpkey", "-algorithm", "RSA", "-pkeyopt", f"rsa_keygen_bits:{bits}", "-out", str(key_path)])


def _self_signed(cert_path: Path, key_path: Path, subject: str, days: int = 1) -> bool:
    return _run_openssl(
        [
            "req",
            "-x509",
            "-key",
            str(key_path),
            "-out",
            str(cert_path),
            "-days",
            str(days),
            "-subj",
            subject,
        ]
    )


def _signed_cert(
    cert_path: Path,
    key_path: Path,
    ca_cert: Path,
    ca_key: Path,
    subject: str,
    days: int = 1,
) -> bool:
    csr = cert_path.with_suffix(".csr")
    if not _run_openssl(["req", "-new", "-key", str(key_path), "-out", str(csr), "-subj", subject]):
        return False
    ok = _run_openssl(
        [
            "x509",
            "-req",
            "-in",
            str(csr),
            "-CA",
            str(ca_cert),
            "-CAkey",
            str(ca_key),
            "-CAcreateserial",
            "-out",
            str(cert_path),
            "-days",
            str(days),
        ]
    )
    if csr.is_file():
        csr.unlink()
    return ok


def generate_tls_material(tmp: Path, spec: TlsCertSpec) -> TlsCertMaterial | None:
    """Generate leaf cert + key under tmp; server cert PEM may include intermediate chain."""
    tmp.mkdir(parents=True, exist_ok=True)
    leaf_key = tmp / "leaf-key.pem"
    leaf_cert = tmp / "leaf.pem"
    subject = _subject_dn(spec)

    if spec.chain_depth <= 1:
        if spec.key_type == "rsa" and spec.key_bits == 2048 and not spec.long_subject:
            # Fast path matching legacy ensure_tls_cert.
            if not _run_openssl(
                [
                    "req",
                    "-x509",
                    "-newkey",
                    "rsa:2048",
                    "-keyout",
                    str(leaf_key),
                    "-out",
                    str(leaf_cert),
                    "-days",
                    "1",
                    "-nodes",
                    "-subj",
                    subject,
                ]
            ):
                return None
        else:
            if not _gen_key(leaf_key, spec):
                return None
            if not _self_signed(leaf_cert, leaf_key, subject):
                return None
        return TlsCertMaterial(cert=leaf_cert, key=leaf_key, spec=spec)

    root_key = tmp / "root-key.pem"
    root_cert = tmp / "root.pem"
    if not _gen_key(root_key, TlsCertSpec(id="root", key_type="rsa", key_bits=2048)):
        return None
    if not _self_signed(root_cert, root_key, "/CN=Tier5 Test Root CA/O=li-tier5-bench/C=US"):
        return None

    if spec.chain_depth == 2:
        signer_cert, signer_key = root_cert, root_key
        inter_cert = None
    else:
        inter_key = tmp / "inter-key.pem"
        inter_cert = tmp / "inter.pem"
        if not _gen_key(inter_key, TlsCertSpec(id="inter", key_type="rsa", key_bits=2048)):
            return None
        if not _signed_cert(
            inter_cert,
            inter_key,
            root_cert,
            root_key,
            "/CN=Tier5 Test Intermediate/O=li-tier5-bench/C=US",
        ):
            return None
        signer_cert, signer_key = inter_cert, inter_key

    if not _gen_key(leaf_key, spec):
        return None
    if not _signed_cert(leaf_cert, leaf_key, signer_cert, signer_key, subject):
        return None

    server_pem = tmp / "server.pem"
    parts = [leaf_cert.read_text(encoding="utf-8")]
    if inter_cert is not None and inter_cert.is_file():
        parts.append(inter_cert.read_text(encoding="utf-8"))
    elif spec.chain_depth == 2:
        parts.append(root_cert.read_text(encoding="utf-8"))
    server_pem.write_text("".join(parts), encoding="utf-8")
    chain_pem = tmp / "chain.pem"
    chain_pem.write_text("".join(parts[1:]), encoding="utf-8") if len(parts) > 1 else None
    return TlsCertMaterial(cert=server_pem, key=leaf_key, spec=spec, chain_pem=chain_pem if chain_pem.is_file() else None)


def ensure_tls_cert(tmp: Path) -> tuple[Path, Path] | None:
    """Backward-compatible single cert (RSA-2048 leaf) for legacy callers."""
    mat = generate_tls_material(tmp, TlsCertSpec(id="rsa2048-leaf"))
    if mat is None:
        return None
    return mat.cert, mat.key
