import type { SummaryRow } from "@/lib/summary";

type NumericValidity = NonNullable<SummaryRow["numeric_validity"]>;

type NumericValidityPanelProps = {
  row: SummaryRow;
};

function fmtNum(value: number | null | undefined): string {
  if (value == null || Number.isNaN(value)) return "—";
  if (Math.abs(value) >= 1e6 || (Math.abs(value) > 0 && Math.abs(value) < 1e-4)) {
    return value.toExponential(4);
  }
  return value.toPrecision(10);
}

export function NumericValidityPanel({ row }: NumericValidityPanelProps) {
  const nv = row.numeric_validity as NumericValidity | undefined;
  if (!nv) {
    return (
      <section className="validity-panel" aria-label="Numeric oracle">
        <h3 style={{ fontSize: "1rem", margin: "1.5rem 0 0.5rem" }}>
          Numeric oracle
        </h3>
        <p style={{ color: "var(--muted)", fontSize: "0.9rem" }}>
          No analytical verify rows in ingest yet. Run tier-1 with{" "}
          <code>--verify</code> so <code>latest.csv</code> exports{" "}
          <code>verify_ulps</code> / <code>verify_within_1ulp</code>.
        </p>
      </section>
    );
  }

  const epsLabel = nv.within_1ulp
    ? "yes — within 1 ULP of analytical reference"
    : "no — exceeds 1 ULP (float64)";

  return (
    <section className="validity-panel" aria-label="Numeric oracle">
      <h3 style={{ fontSize: "1rem", margin: "1.5rem 0 0.5rem" }}>
        Analytical oracle (Li vs closed form)
      </h3>
      <p style={{ color: "var(--muted)", fontSize: "0.9rem" }}>
        Correctness is checked against an analytical reference when available (
        <code>horner_pure_li</code>, <code>reduce_sum</code>). Dot/matmul use
        iterative spec; small sizes are cross-checked with high-precision decimal
        in the harness.
      </p>
      <dl
        className="mono"
        style={{
          marginTop: "0.75rem",
          display: "grid",
          gridTemplateColumns: "auto 1fr",
          gap: "0.35rem 1rem",
        }}
      >
        <dt>Oracle kind</dt>
        <dd>{nv.oracle}</dd>
        <dt>Analytical reference</dt>
        <dd>{fmtNum(nv.analytical_value)}</dd>
        <dt>Measured checksum</dt>
        <dd>{fmtNum(nv.checksum_value)}</dd>
        <dt>Absolute error</dt>
        <dd>{fmtNum(nv.abs_error)}</dd>
        <dt>Relative error</dt>
        <dd>{fmtNum(nv.rel_error)}</dd>
        <dt>ULP distance</dt>
        <dd>{fmtNum(nv.ulps)}</dd>
        <dt>Within 1 ULP</dt>
        <dd>{epsLabel}</dd>
      </dl>
    </section>
  );
}
