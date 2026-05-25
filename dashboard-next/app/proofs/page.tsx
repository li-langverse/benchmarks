import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import {
  loadProofPosture,
  postureStatusClass,
} from "@/lib/proof-posture";

const PROVABILITY_GAPS_URL =
  "https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md";

export default function ProofsPage() {
  const posture = loadProofPosture();

  if (!posture || posture.rows.length === 0) {
    return (
      <main>
        <section className="placeholder">
          <h2>Proofs vs benchmarks</h2>
          <p>
            No <span className="mono">data/latest/proof-posture.json</span> at
            build time. Run{" "}
            <span className="mono">python3 scripts/build-proof-posture.py</span>{" "}
            with <span className="mono">LIC_ROOT</span> pointing at a lic
            checkout (or ingest via <span className="mono">ingest-lic.sh</span>
            ).
          </p>
          <p style={{ marginTop: "1.25rem" }}>
            Source of truth:{" "}
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

  return (
    <main>
      <section className="placeholder" style={{ marginBottom: "1.5rem" }}>
        <h2>Proof posture (G-*)</h2>
        <p>
          Rows parsed from{" "}
          <a href={PROVABILITY_GAPS_URL} target="_blank" rel="noopener noreferrer">
            provability-gaps.md
          </a>
          . Status colors are <strong>compiler maturity</strong>, not benchmark
          wall-clock ratios.
        </p>
        <p className="mono" style={{ marginTop: "0.75rem" }}>
          Generated: {posture.generated_at}
        </p>
      </section>
      <section>
        <h3 className="section-heading">Gap register</h3>
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Status</th>
                <th>Phase</th>
              </tr>
            </thead>
            <tbody>
              {posture.rows.map((row) => (
                <tr key={row.id}>
                  <td className="mono">{row.id}</td>
                  <td>
                    <Badge status={postureStatusClass(row.status)}>
                      {row.status}
                    </Badge>
                  </td>
                  <td className="mono">{row.phase || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      <section className="placeholder" style={{ marginTop: "2rem" }}>
        <h3 className="section-heading">Benchmark honesty</h3>
        <p style={{ color: "var(--muted)" }}>
          Dashboard bench colors report ratios against catalog thresholds. They
          are not Lean proof certificates.
        </p>
        <ul
          style={{
            marginTop: "1rem",
            paddingLeft: "1.25rem",
            color: "var(--muted)",
          }}
        >
          <li>
            <strong style={{ color: "var(--text)" }}>Green</strong> — ratio
            within threshold; not formal verification.
          </li>
          <li>
            <strong style={{ color: "var(--text)" }}>Red pure_li</strong> —
            PH-7e codegen debt, not a missing G-* row.
          </li>
        </ul>
      </section>
      <p style={{ marginTop: "1.5rem" }}>
        <Link href="/pillar/proofs/">Pillar: proofs</Link>
        {" · "}
        <Link href="/">← Overview</Link>
      </p>
    </main>
  );
}
