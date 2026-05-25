import type { SummaryRow } from "@/lib/summary";
import { formatRatioVsSota, rowValidityStatus } from "@/lib/validity";
import { Badge } from "@/components/ui/badge";

type ValidityPanelProps = {
  row: SummaryRow;
};

const VALIDITY_LABEL: Record<string, string> = {
  pass: "pass — perf claims allowed when ratio is green",
  fail: "fail — perf not claimable",
  unknown: "unknown — no stability/harness pass signal",
};

export function ValidityPanel({ row }: ValidityPanelProps) {
  const validity = rowValidityStatus(row);
  const badgeStatus =
    validity === "pass" ? "green" : validity === "fail" ? "red" : "unknown";

  return (
    <section className="validity-panel" aria-label="Validity gate">
      <h3 style={{ fontSize: "1rem", margin: "1.5rem 0 0.5rem" }}>Validity gate</h3>
      <p>
        <Badge status={badgeStatus}>{validity}</Badge>
        <span className="mono" style={{ marginLeft: "0.5rem", color: "var(--muted)" }}>
          {VALIDITY_LABEL[validity]}
        </span>
      </p>
      {row.validity_source ? (
        <p className="mono" style={{ fontSize: "0.85rem", color: "var(--muted)" }}>
          Source: {row.validity_source}
        </p>
      ) : null}
      <dl
        className="mono"
        style={{
          marginTop: "0.75rem",
          display: "grid",
          gridTemplateColumns: "auto 1fr",
          gap: "0.35rem 1rem",
        }}
      >
        <dt>Ratio vs best competitor</dt>
        <dd>
          {formatRatioVsSota(row)}
          {row.sota_lang ? (
            <span style={{ color: "var(--muted)" }}>
              {" "}
              (best in series: <code>{row.sota_lang}</code> — Li is never labeled best)
            </span>
          ) : null}
        </dd>
        {row.sota_value != null ? (
          <>
            <dt>Best competitor value</dt>
            <dd>
              {row.sota_value} {row.unit ?? ""}
            </dd>
          </>
        ) : null}
      </dl>
    </section>
  );
}
