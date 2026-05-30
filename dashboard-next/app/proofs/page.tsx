import Link from "next/link";

const PROOF_LIBRARY_URL = "https://li-langverse.github.io/proof-library/";

export default function ProofsPage() {
  return (
    <main>
      <section className="placeholder">
        <h2>Proof library moved</h2>
        <p>
          The proof corpus dashboard (catalog vs Lean, divergence, human votes) lives in
          the dedicated{" "}
          <a href={PROOF_LIBRARY_URL}>proof-library</a> repository — separate from
          benchmark wall-clock performance.
        </p>
        <p style={{ marginTop: "1.25rem" }}>
          <a href={PROOF_LIBRARY_URL}>Open proof library →</a>
        </p>
        <p style={{ marginTop: "1.25rem" }}>
          <Link href="/pillar/proofs/">Pillar: proofs (perf rows)</Link>
          {" · "}
          <Link href="/">← Overview</Link>
        </p>
      </section>
    </main>
  );
}
