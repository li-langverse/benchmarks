import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const picker = readFileSync(join(root, "components/gpu/gpu-chip-picker.tsx"), "utf8");
const client = readFileSync(join(root, "components/gpu/gpu-matrix-client.tsx"), "utf8");

const checks = [
  ["GPU_CHIP_TAB_PANEL_ID export", () => picker.includes("export const GPU_CHIP_TAB_PANEL_ID")],
  ["gpuChipTabId export", () => picker.includes("export function gpuChipTabId")],
  ["aria-controls on tabs", () => picker.includes("aria-controls={GPU_CHIP_TAB_PANEL_ID}")],
  ["roving tabIndex", () => picker.includes("tabIndex={active ? 0 : -1}")],
  [
    "arrow key handler",
    () => picker.includes("ArrowRight") && picker.includes("onKeyDown={handleTabKeyDown}"),
  ],
  ["tabpanel role in client", () => client.includes('role="tabpanel"')],
  ["tabpanel id wired", () => client.includes("GPU_CHIP_TAB_PANEL_ID")],
  ["open slots not tabs", () => !/openSlots\.map[\s\S]*?role="tab"/.test(picker)],
];

let failed = 0;
for (const [name, fn] of checks) {
  if (!fn()) {
    console.error(`FAIL: ${name}`);
    failed += 1;
  }
}

console.log(failed === 0 ? "gpu-chip-picker-a11y.test: OK" : "FAILED");
process.exit(failed === 0 ? 0 : 1);
