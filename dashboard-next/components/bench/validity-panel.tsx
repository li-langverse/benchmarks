import type { SummaryRow } from "@/lib/summary";
import { plainValiditySource } from "@/lib/validity-labels";
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

  const headingId = "validity-gate-heading";

  return (
    <section className="validity-panel" aria-labelledby={headingId}>
      <h3 id={headingId} className="bench-panel-heading">
        Validity gate
      </h3>
      <p>
        <Badge status={badgeStatus}>{validity}</Badge>
        <span className="validity-panel-hint mono">{VALIDITY_LABEL[validity]}</span>
      </p>
      {row.validity_source ? (
        <>
          <p className="mono validity-panel-source-code">
            Source: <code>{row.validity_source}</code>
          </p>
          <p className="validity-panel-plain">{plainValiditySource(row.validity_source)}</p>
        </>
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
