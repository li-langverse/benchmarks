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
  return raw !== "0" && raw !== "false";
}

export function modelsForArmA() {
  const raw = process.env.PHYSICS_CODEGEN_MODELS?.trim();
  if (raw) return raw.split(",").map((s) => s.trim()).filter(Boolean);
  return ["composer-2.5-fast", "cursor-auto", "qwen-3.5-9b"];
}

export function fixedModelArmB() {
  const models = modelsForArmA();
  return process.env.PHYSICS_CODEGEN_ARM_B_MODEL?.trim() || models[0] || "composer-2.5-fast";
}

export function benches() {
  return pilotMode() ? PILOT_BENCHES : FULL_BENCHES;
}
