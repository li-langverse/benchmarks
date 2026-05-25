import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import type { SummaryRow } from "@/lib/summary";

type BenchRowListProps = {
  rows: SummaryRow[];
  emptyMessage: string;
};

export function BenchRowList({ rows, emptyMessage }: BenchRowListProps) {
  if (rows.length === 0) {
    return <p style={{ color: "var(--muted)" }}>{emptyMessage}</p>;
  }
  return (
    <div className="table-wrap" style={{ marginTop: "1rem" }}>
      <table className="data-table">
        <thead>
          <tr>
            <th>Benchmark</th>
            <th>Tier</th>
            <th>Package</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.benchmark}>
              <td>
                <Link href={`/bench/${row.benchmark}/`}>{row.benchmark}</Link>
              </td>
              <td>{row.tier}</td>
              <td>{row.package ?? "—"}</td>
              <td>
                <Badge status={row.status} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
