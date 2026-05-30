import Link from "next/link";
import { notFound } from "next/navigation";
import { BenchRowList } from "@/components/drilldown/bench-row-list";
import { getPillar, PILLAR_IDS } from "@/lib/pillars";
import { loadSummary } from "@/lib/summary";

type PageProps = {
  params: Promise<{ id: string }>;
};

export function generateStaticParams() {
  return PILLAR_IDS.map((id) => ({ id }));
}

export default async function PillarPage({ params }: PageProps) {
  const { id } = await params;
  const pillar = getPillar(id);
  if (!pillar) notFound();

  const summary = loadSummary();
  const rows = summary.rows.filter((r) => r.pillar === id);

  return (
    <main>
      <section className="placeholder">
        <h2>{pillar.label}</h2>
        <p>{pillar.description}</p>
        <p className="mono" style={{ marginTop: "0.75rem", color: "var(--muted)" }}>
          {rows.length} benchmark row{rows.length === 1 ? "" : "s"} with pillar={id}
          {id === "graphics" ? (
            <>
              {" "}
              ·{" "}
              <Link href="/gpu-matrix/">GPU chip matrix (donate your hardware)</Link>
            </>
          ) : null}
        </p>

        <BenchRowList
          rows={rows}
          emptyMessage={`No rows tagged pillar="${id}" in summary.json.`}
        />

        <p style={{ marginTop: "1.25rem" }}>
          <Link href="/">← Overview</Link>
        </p>
      </section>
    </main>
  );
}
