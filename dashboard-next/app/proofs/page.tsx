import Link from "next/link";

const PROVABILITY_GAPS_URL =
  "https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md";

export default function ProofsPage() {
  return (
    <main>
      <section className="placeholder">
        <h2>Proofs vs benchmarks</h2>
        <p>
          Dashboard status colors report <strong>wall-clock ratios</strong> against
          catalog thresholds (usually C++). They are not Lean proof certificates or
          G-* closure evidence.
        </p>
        <ul style={{ marginTop: "1rem", paddingLeft: "1.25rem", color: "var(--muted)" }}>
          <li>
            <strong style={{ color: "var(--text)" }}>Green</strong> — ratio within
            threshold; does not mean the kernel is formally verified.
          </li>
          <li>
            <strong style={{ color: "var(--text)" }}>Red pure_li</strong> — PH-7e
            codegen performance debt, not a missing proof row.
          </li>
          <li>
            <strong style={{ color: "var(--text)" }}>shared_c_kernel</strong> — shared
            C numerics; not pure-Li competitiveness proof.
          </li>
        </ul>
        <p style={{ marginTop: "1.25rem" }}>
          Proof wiring and G-* gaps:{" "}
          <a href={PROVABILITY_GAPS_URL} target="_blank" rel="noopener noreferrer">
            lic/docs/verification/provability-gaps.md
          </a>
        </p>
        <p style={{ marginTop: "1.25rem" }}>
          <Link href="/pillar/proofs/">Pillar: proofs</Link>
          {" · "}
          <Link href="/">← Overview</Link>
        </p>
      </section>
    </main>
  );
}
