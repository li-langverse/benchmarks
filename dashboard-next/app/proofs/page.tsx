const PROOF_LIBRARY_URL = "https://li-langverse.github.io/proof-library/";

export default function ProofsMovedPage() {
  return (
    <main className="placeholder">
      <h2>Proof library moved</h2>
      <p>
        The proof corpus UI now lives in the dedicated{" "}
        <a href={PROOF_LIBRARY_URL}>proof-library</a> repository — separate from benchmark
        performance ratios.
      </p>
      <p>
        <a href={PROOF_LIBRARY_URL}>Continue to proof library →</a>
      </p>
      <meta httpEquiv="refresh" content={`2;url=${PROOF_LIBRARY_URL}`} />
    </main>
  );
}
