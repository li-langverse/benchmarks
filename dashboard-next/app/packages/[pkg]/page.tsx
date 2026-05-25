import Link from "next/link";
import { notFound } from "next/navigation";
import { BenchRowList } from "@/components/drilldown/bench-row-list";
import {
  findPackage,
  loadEcosystemPackages,
} from "@/lib/ecosystem-packages";
import { githubTreeUrl } from "@/lib/github";
import { loadSummary } from "@/lib/summary";

type PageProps = {
  params: Promise<{ pkg: string }>;
};

export function generateStaticParams() {
  return loadEcosystemPackages().map((p) => ({ pkg: p.id }));
}

export default async function PackagePage({ params }: PageProps) {
  const { pkg } = await params;
  const packages = loadEcosystemPackages();
  const meta = findPackage(packages, pkg);
  if (!meta) notFound();

  const summary = loadSummary();
  const rows = summary.rows.filter((r) => r.package === pkg);
  const repoUrl = githubTreeUrl(meta.repo, "");

  return (
    <main>
      <section className="placeholder">
        <h2>{meta.id}</h2>
        <p>
          Ecosystem package <span className="mono">{meta.repo}</span>
          {meta.bench_required === false ? " · bench not gate-blocking" : ""}
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
          <dt>Repo</dt>
          <dd>
            <a href={repoUrl} target="_blank" rel="noopener noreferrer">
              github.com/li-langverse/{meta.repo}
            </a>
          </dd>
          <dt>Default pillars</dt>
          <dd>
            {meta.pillar_defaults.length > 0
              ? meta.pillar_defaults.join(", ")
              : "—"}
          </dd>
          <dt>CSV ingest paths</dt>
          <dd>
            {meta.csv_paths.length > 0 ? meta.csv_paths.join("; ") : "—"}
          </dd>
        </dl>

        <h3 style={{ fontSize: "1rem", marginTop: "1.5rem", color: "var(--text)" }}>
          Catalog rows ({rows.length})
        </h3>
        <BenchRowList
          rows={rows}
          emptyMessage={`No summary rows tagged package="${pkg}".`}
        />

        <p style={{ marginTop: "1.25rem" }}>
          <Link href="/">← Overview</Link>
        </p>
      </section>
    </main>
  );
}
