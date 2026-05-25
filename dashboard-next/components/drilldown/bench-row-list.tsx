import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import type { SummaryRow } from "@/lib/summary";

type BenchRowListProps = {
  rows: SummaryRow[];
  emptyMessage?: string;
};

export function BenchRowList({
  rows,
  emptyMessage = "No benchmark rows for this filter.",
}: BenchRowListProps) {
  if (rows.length === 0) {
    return (
      <p className="mono" style={{ marginTop: "1rem", color: "var(--muted)" }}>
        {emptyMessage}
      </p>
    );
  }

  const sorted = [...rows].sort((a, b) => a.benchmark.localeCompare(b.benchmark));

  return (
    <table className="data-table" style={{ marginTop: "1rem" }}>
      <thead>
        <tr>
          <th scope="col">Benchmark</th>
          <th scope="col">Tier</th>
          <th scope="col">Status</th>
          <th scope="col">Ratio</th>
        </tr>
      </thead>
      <tbody>
        {sorted.map((row) => (
          <tr key={row.benchmark}>
            <td>
              <Link href={`/bench/${row.benchmark}/`}>{row.benchmark}</Link>
            </td>
            <td className="mono">{row.tier}</td>
            <td>
              <Badge status={row.status} />
            </td>
            <td className="mono">
              {row.ratio_vs_cpp != null ? `${row.ratio_vs_cpp.toFixed(3)}×` : "—"}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
