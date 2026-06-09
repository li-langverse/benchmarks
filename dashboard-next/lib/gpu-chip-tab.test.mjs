import { chipPanelId, chipTabId, nextChipTabIndex } from "./gpu-chip-tab-ids.ts";

let failed = 0;

function assert(cond, msg) {
  if (!cond) {
    console.error("FAIL:", msg);
    failed += 1;
  }
}

assert(chipTabId("nvidia-rtx-3060-linux") === "gpu-chip-tab-nvidia-rtx-3060-linux", "tab id");
assert(chipPanelId("apple-m1-macos") === "gpu-chip-panel-apple-m1-macos", "panel id");

assert(nextChipTabIndex(0, 3, "ArrowRight") === 1, "arrow right");
assert(nextChipTabIndex(2, 3, "ArrowRight") === 0, "arrow right wrap");
assert(nextChipTabIndex(0, 3, "ArrowLeft") === 2, "arrow left wrap");
assert(nextChipTabIndex(1, 3, "ArrowUp") === 0, "arrow up");
assert(nextChipTabIndex(0, 3, "Home") === 0, "home");
assert(nextChipTabIndex(0, 3, "End") === 2, "end");
assert(nextChipTabIndex(0, 0, "ArrowRight") === null, "empty list");
assert(nextChipTabIndex(0, 3, "Enter") === null, "ignored key");

console.log(failed === 0 ? "gpu-chip-tab.test: OK" : "gpu-chip-tab.test: FAILED");
process.exit(failed === 0 ? 0 : 1);
