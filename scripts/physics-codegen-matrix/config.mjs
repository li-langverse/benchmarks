/** Pilot + full physics codegen matrix configuration. */
export const PILOT_BENCHES = [
  "wave_equation_1d",
  "heat_equation_2d",
  "schrodinger_1d_barrier",
];

export const FULL_BENCHES = [
  "wave_equation_1d",
  "heat_equation_2d",
  "advection_diffusion_2d",
  "wave_equation_2d",
  "sph_dam_break_2d",
  "wind_field_bc",
  "combustion_passive",
  "fdtd_waveguide_2d",
  "schrodinger_1d_barrier",
  "euler_fluid_2d",
];

export const LANGS = ["cpp", "rust", "julia", "li"];

export function pilotMode() {
  const raw = process.env.PHYSICS_CODEGEN_PILOT?.trim().toLowerCase();
  return raw === "1" || raw === "true" || raw === "yes";
}

export function modelsForArmA() {
  const raw = process.env.PHYSICS_CODEGEN_MODELS?.trim();
  if (raw) return raw.split(",").map((s) => s.trim()).filter(Boolean);
  return ["default", "qwen-3.5-9b", "qwen-3.5-20b"];
}

export function fixedModelArmB() {
  const explicit = process.env.PHYSICS_CODEGEN_ARM_B_MODEL?.trim();
  if (explicit) return explicit;
  const models = modelsForArmA();
  return models.find((m) => m === "default") || models[0] || "default";
}

export function benches() {
  return pilotMode() ? PILOT_BENCHES : FULL_BENCHES;
}

export function expectedRowCount() {
  const n = benches().length;
  const models = modelsForArmA();
  if (pilotMode()) return models.length * n + n * LANGS.length;
  return models.length * n + n * LANGS.length;
}
