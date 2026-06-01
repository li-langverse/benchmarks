/** Build SDK prompt for one matrix cell. */
export function buildCellPrompt({ arm, bench_id: benchId, lang, model }) {
  const langDir =
    lang === "cpp"
      ? "cpp"
      : lang === "rust"
        ? "rust"
        : lang === "julia"
          ? "julia"
          : "li";
  const mainHint =
    lang === "cpp"
      ? "cpp/main.c or cpp/main.cpp"
      : lang === "rust"
        ? "rust/main.rs (create rust/ if missing)"
        : lang === "julia"
          ? "julia/*.jl (create julia/ if missing)"
          : "li/main.li";

  return `## Physics codegen matrix — live cell

| Field | Value |
|-------|-------|
| Arm | ${arm} |
| Model label | ${model} |
| Benchmark | ${benchId} |
| Language | ${lang} |

Implement or fix the tier-2 PDE kernel under:

\`benchmarks/workloads/tier2_physics/${benchId}/${langDir}/\`

Reference oracle: \`common/\` + \`cpp/main.c\` (do **not** edit \`common/\` or \`params.toml\`).

Target entrypoint: \`${mainHint}\`

Libraries are allowed (Eigen, ndarray, DifferentialEquations.jl, Li stdlib, etc.).

**Done when** this passes from the benchmarks repo root:

\`\`\`bash
LIC_ROOT="\${LIC_ROOT:-/workspace/lic}" python3 harness/bench.py --tier 2 --verify-results --only ${benchId}
\`\`\`

Use skill **agent-self-unblock** if IDE hooks block Read/StrReplace.

Keep changes minimal and scoped to this benchmark's ${lang} tree.`;
}
