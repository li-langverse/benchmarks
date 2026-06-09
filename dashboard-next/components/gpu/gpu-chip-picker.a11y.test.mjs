import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const pickerSrc = readFileSync(join(root, "components/gpu/gpu-chip-picker.tsx"), "utf8");
const clientSrc = readFileSync(join(root, "components/gpu/gpu-matrix-client.tsx"), "utf8");

const required = [
  [pickerSrc, 'role="tablist"'],
  [pickerSrc, "aria-controls={GPU_CHIP_PANEL_ID}"],
  [pickerSrc, "tabIndex={active ? 0 : -1}"],
  [pickerSrc, "handleTabKeyDown"],
  [pickerSrc, "ArrowRight"],
  [clientSrc, 'role="tabpanel"'],
  [clientSrc, "GPU_CHIP_PANEL_ID"],
  [clientSrc, "gpuChipTabId(selected.chip_slug)"],
];

let failed = 0;
for (const [src, needle] of required) {
  if (!src.includes(needle)) {
    console.error(`gpu-chip-picker.a11y.test: missing ${needle}`);
    failed += 1;
  }
}

console.log(failed === 0 ? "gpu-chip-picker.a11y.test: OK" : "FAILED");
process.exit(failed === 0 ? 0 : 1);
