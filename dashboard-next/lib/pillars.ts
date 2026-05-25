/** Dashboard navigation pillars (WP1 plan). */
export type PillarId =
  | "numerics"
  | "compiler"
  | "server"
  | "physics"
  | "proofs"
  | "security"
  | "database"
  | "graphics"
  | "tooling";

export type Pillar = {
  id: PillarId;
  label: string;
  description: string;
};

export const PILLARS: readonly Pillar[] = [
  {
    id: "numerics",
    label: "Numerics",
    description: "Micro kernels, SIMD, linear algebra, and core math performance.",
  },
  {
    id: "compiler",
    label: "Compiler",
    description: "Codegen, LLVM, compile-time, and toolchain benchmarks.",
  },
  {
    id: "server",
    label: "Server",
    description: "HTTP, webserver, and request-path throughput (li-httpd, lis).",
  },
  {
    id: "physics",
    label: "Physics",
    description: "Tier-2 simulations, rigid body, and physics module benches.",
  },
  {
    id: "proofs",
    label: "Proofs",
    description: "Proof database, verification gates, and provability evidence.",
  },
  {
    id: "security",
    label: "Security",
    description: "CVE tiers, exploit harnesses, and security registry rows.",
  },
  {
    id: "database",
    label: "Database",
    description: "Storage, query, and proof-db / persistence performance.",
  },
  {
    id: "graphics",
    label: "Graphics",
    description: "Rendering, GPU paths, and visualization workloads.",
  },
  {
    id: "tooling",
    label: "Tooling",
    description: "lip, lit, lic compile, and ecosystem tooling benches.",
  },
] as const;

export const PILLAR_IDS: PillarId[] = PILLARS.map((p) => p.id);

export function getPillar(id: string): Pillar | undefined {
  return PILLARS.find((p) => p.id === id);
}

/** Map summary.json categories to pillar ids for future filtering. */
export const CATEGORY_TO_PILLAR: Partial<Record<string, PillarId>> = {
  micro: "numerics",
  physics: "physics",
  http: "server",
  tooling: "tooling",
  security: "security",
  correctness: "proofs",
};
