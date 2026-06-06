import { nextGpuChipTabIndex, gpuChipTabId, GPU_CHIP_TAB_PANEL_ID } from "./gpu-chip-tab-nav.ts";

let failed = 0;
function assert(cond, msg) {
  if (!cond) {
    console.error("FAIL:", msg);
    failed += 1;
  }
}

assert(GPU_CHIP_TAB_PANEL_ID === "gpu-selected-chip-panel", "panel id constant");
assert(gpuChipTabId("nvidia-rtx-3060-linux") === "gpu-chip-tab-nvidia-rtx-3060-linux", "tab id");

assert(nextGpuChipTabIndex("ArrowRight", 0, 3) === 1, "arrow right");
assert(nextGpuChipTabIndex("ArrowRight", 2, 3) === 0, "arrow right wrap");
assert(nextGpuChipTabIndex("ArrowLeft", 0, 3) === 2, "arrow left wrap");
assert(nextGpuChipTabIndex("ArrowDown", 1, 3) === 2, "arrow down");
assert(nextGpuChipTabIndex("ArrowUp", 0, 3) === 2, "arrow up wrap");
assert(nextGpuChipTabIndex("Home", 2, 3) === 0, "home");
assert(nextGpuChipTabIndex("End", 0, 3) === 2, "end");
assert(nextGpuChipTabIndex("Enter", 0, 3) === null, "unhandled key");
assert(nextGpuChipTabIndex("ArrowRight", 0, 0) === null, "empty list");

console.log(failed === 0 ? "gpu-chip-tab-nav.test: OK" : "gpu-chip-tab-nav.test: FAILED");
process.exit(failed === 0 ? 0 : 1);
