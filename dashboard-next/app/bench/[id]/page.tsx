import Link from "next/link";
import { notFound } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { findRow, loadSummary } from "@/lib/summary";

type PageProps = {
  params: Promise<{ id: string }>;
};

export function generateStaticParams() {
  const summary = loadSummary();
  return summary.rows.map((row) => ({ id: row.benchmark }));
}

export default async function BenchPage({ params }: PageProps) {
  const { id } = await params;
  const summary = loadSummary();
  const row = findRow(summary, id);
  if (!row) notFound();

  return (
    <main>
      <section className="placeholder">
        <h2>
          {row.benchmark} <Badge status={row.status} />
        </h2>
        <p>
          Stub benchmark detail — tier {row.tier}, repo {row.repo}, metric{" "}
          {row.metric}.
        </p>
        <dl
          className="mono"
          style={{
            marginTop: "1rem",
            display: "grid",
            gridTemplateColumns: "auto 1fr",
            gap: "0.35rem 1rem",
          }}
        >
          <dt>Path</dt>
          <dd>{row.path}</dd>
          <dt>Category</dt>
          <dd>{row.category ?? "—"}</dd>
          <dt>Li / C++</dt>
          <dd>
            {row.li_value ?? "—"} / {row.cpp_value ?? "—"}{" "}
            {row.unit ? row.unit : ""}
          </dd>
          <dt>Ratio vs C++</dt>
          <dd>{row.ratio_vs_cpp != null ? `${row.ratio_vs_cpp.toFixed(4)}×` : "—"}</dd>
          <dt>PH ids</dt>
          <dd>{row.ph_ids.join(", ") || "—"}</dd>
        </dl>
        <p style={{ marginTop: "1.25rem" }}>
          <Link href="/">← Overview</Link>
        </p>
      </section>
    </main>
  );
}
