import Link from "next/link";
import { ProofLibraryBoard } from "@/components/proof-library-board";
import { loadProofLibrary } from "@/lib/proof-library";
import { loadProofPosture } from "@/lib/proof-posture";

const PROVABILITY_GAPS_URL =
  "https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md";

export default function ProofsPage() {
  const library = loadProofLibrary();
  const posture = loadProofPosture();

  return (
    <main>
      <section className="placeholder">
        <h2>Proof library</h2>
        <p>
          Lemma and axiom catalog from <code>lic/proof-db</code> — separate from benchmark
          wall-clock ratios. Compare <strong>scientific catalog opinion</strong> vs{" "}
          <strong>Lean scan</strong>, then record what you believe (browser-local votes + GitHub
          discussion).
        </p>
        <ul style={{ marginTop: "1rem", paddingLeft: "1.25rem", color: "var(--muted)" }}>
          <li>
            <strong style={{ color: "var(--text)" }}>Catalog</strong> — TOML / index{" "}
            <code>proof_status</code> (proved, open, axiomatic, discrepancy).
          </li>
          <li>
            <strong style={{ color: "var(--text)" }}>Lean</strong> — static scan of theorem
            bodies (sorry → open; trusted axiom → axiomatic).
          </li>
          <li>
            <strong style={{ color: "var(--text)" }}>Red row</strong> — catalog and Lean disagree.
          </li>
          <li>
            Bench greens on the overview are still <em>not</em> proof certificates — see{" "}
            <Link href="/pillar/proofs/">pillar: proofs</Link>.
          </li>
        </ul>
        <p style={{ marginTop: "1.25rem" }}>
          Compiler G-* gaps:{" "}
          <a href={PROVABILITY_GAPS_URL} target="_blank" rel="noopener noreferrer">
            provability-gaps.md
          </a>
        </p>
      </section>

      {posture && posture.rows.length > 0 ? (
        <section className="proof-posture-strip">
          <h3>G-* compiler gaps (from provability-gaps.md)</h3>
          <div className="proof-posture-chips">
            {posture.rows.slice(0, 12).map((row) => (
              <span key={row.id} className="mono proof-posture-chip">
                {row.id}: {row.status}
              </span>
            ))}
            {posture.rows.length > 12 ? (
              <span className="mono proof-posture-chip">+{posture.rows.length - 12} more</span>
            ) : null}
          </div>
        </section>
      ) : null}

      {library ? (
        <ProofLibraryBoard
          generatedAt={library.generated_at}
          licCommit={library.lic_commit}
          summary={library.summary}
          entries={library.entries}
          voteNote={library.vote_policy.note}
        />
      ) : (
        <section className="placeholder">
          <p>
            <code>proof-library.json</code> missing. From benchmarks repo run:{" "}
            <code className="mono">LIC_ROOT=../lic python3 scripts/build-proof-library.py</code>
          </p>
        </section>
      )}
    </main>
  );
}
