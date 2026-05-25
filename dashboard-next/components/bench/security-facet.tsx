import Link from "next/link";
import type { SummaryRow } from "@/lib/summary";
import { Badge } from "@/components/ui/badge";

export function SecurityFacet({ row }: { row: SummaryRow }) {
  return (
    <section className="facet-panel" aria-label="Security facet">
      <h3 style={{ fontSize: "1rem", margin: "1.5rem 0 0.5rem" }}>⑤ Security</h3>
      {row.category === "security" ? (
        <p>
          <Badge status={row.status} /> {row.metric}
        </p>
      ) : (
        <p className="mono" style={{ color: "var(--muted)" }}>
          Row-level gates N/A — <Link href="/matrix#security">security matrix</Link>.
        </p>
      )}
    </section>
  );
}
