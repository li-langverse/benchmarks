import Link from "next/link";
import { notFound } from "next/navigation";
import { Header } from "@/components/shell/header";
import { StatusBadge } from "@/components/ui/badge";
import { loadSummary } from "@/lib/summary";
import { PILLAR_IDS, getPillar } from "@/lib/pillars";

export function generateStaticParams() {
  return PILLAR_IDS.map((id) => ({ id }));
}

export default async function PillarPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const pillar = getPillar(id);
  if (!pillar) notFound();
  const summary = loadSummary();
  const rows = summary.rows;

  return (
    <>
      <Header subtitle={pillar.label} />
      <main className="mx-auto max-w-6xl px-6 py-8">
        <p className="text-[var(--muted)]">{pillar.description}</p>
        <ul className="mt-6 space-y-2">
          {rows.map((r) => (
            <li
              key={r.benchmark}
              className="flex flex-wrap items-center justify-between gap-2 rounded border border-[var(--border)] bg-[var(--surface)] px-3 py-2"
            >
              <Link href={`/bench/${r.benchmark}/`}>{r.benchmark}</Link>
              <StatusBadge status={r.status}>{r.status}</StatusBadge>
            </li>
          ))}
        </ul>
        <p className="mt-8">
          <Link href="/">← Overview</Link>
        </p>
      </main>
    </>
  );
}
