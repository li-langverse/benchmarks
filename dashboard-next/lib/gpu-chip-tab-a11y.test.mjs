let failed = 0;

function assert(cond, msg) {
  if (!cond) {
    console.error("FAIL:", msg);
    failed += 1;
  }
}

function gpuChipTabId(slug) {
  return `gpu-chip-tab-${slug}`;
}

function nextGpuChipTabIndex(key, currentIndex, tabCount) {
  if (tabCount <= 0 || currentIndex < 0) return null;
  switch (key) {
    case "ArrowRight":
    case "ArrowDown":
      return (currentIndex + 1) % tabCount;
    case "ArrowLeft":
    case "ArrowUp":
      return (currentIndex - 1 + tabCount) % tabCount;
    case "Home":
      return 0;
    case "End":
      return tabCount - 1;
    default:
      return null;
  }
}

assert(gpuChipTabId("rtx-3090") === "gpu-chip-tab-rtx-3090", "tab id slug");

assert(nextGpuChipTabIndex("ArrowRight", 0, 3) === 1, "arrow right");
assert(nextGpuChipTabIndex("ArrowDown", 2, 3) === 0, "arrow down wraps");
assert(nextGpuChipTabIndex("ArrowLeft", 0, 3) === 2, "arrow left wraps");
assert(nextGpuChipTabIndex("ArrowUp", 1, 3) === 0, "arrow up");
assert(nextGpuChipTabIndex("Home", 2, 3) === 0, "home");
assert(nextGpuChipTabIndex("End", 0, 3) === 2, "end");
assert(nextGpuChipTabIndex("Enter", 0, 3) === null, "unhandled key");
assert(nextGpuChipTabIndex("ArrowRight", -1, 3) === null, "invalid index");

console.log(failed === 0 ? "gpu-chip-tab-a11y.test: OK" : `gpu-chip-tab-a11y.test: ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
