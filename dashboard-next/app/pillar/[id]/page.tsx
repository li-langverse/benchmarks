import Link from "next/link";
import { notFound } from "next/navigation";
import { CATEGORY_TO_PILLAR, getPillar, PILLAR_IDS } from "@/lib/pillars";
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
  const categories = Object.entries(CATEGORY_TO_PILLAR)
    .filter(([, pillarId]) => pillarId === pillar.id)
    .map(([cat]) => cat);

  const rowCount = summary.rows.filter(
    (r) => r.category && categories.includes(r.category),
  ).length;

  return (
    <main>
      <section className="placeholder">
        <h2>{pillar.label}</h2>
        <p>{pillar.description}</p>
        <p style={{ marginTop: "1rem" }}>
          Stub pillar view — charts and tables land in a later work package.
        </p>
        {categories.length > 0 ? (
          <p className="mono" style={{ marginTop: "0.75rem" }}>
            Categories: {categories.join(", ")} · ~{rowCount} rows
          </p>
        ) : (
          <p className="mono" style={{ marginTop: "0.75rem" }}>
            Category mapping TBD for this pillar.
          </p>
        )}
        <p style={{ marginTop: "1.25rem" }}>
          <Link href="/">← Overview</Link>
        </p>
      </section>
    </main>
  );
}
