import { nextChipTabIndex } from "./gpu-chip-picker-a11y.ts";

let failed = 0;

function assertEqual(actual, expected, label) {
  if (actual !== expected) {
    console.error(`${label}: expected ${expected}, got ${actual}`);
    failed += 1;
  }
}

assertEqual(nextChipTabIndex("ArrowRight", 0, 3), 1, "ArrowRight from first");
assertEqual(nextChipTabIndex("ArrowRight", 2, 3), 0, "ArrowRight wraps");
assertEqual(nextChipTabIndex("ArrowLeft", 0, 3), 2, "ArrowLeft wraps");
assertEqual(nextChipTabIndex("ArrowUp", 1, 3), 0, "ArrowUp moves back");
assertEqual(nextChipTabIndex("ArrowDown", 1, 3), 2, "ArrowDown moves forward");
assertEqual(nextChipTabIndex("Home", 2, 3), 0, "Home to first");
assertEqual(nextChipTabIndex("End", 0, 3), 2, "End to last");
assertEqual(nextChipTabIndex("Enter", 0, 3), null, "Enter ignored");
assertEqual(nextChipTabIndex("ArrowRight", 0, 0), null, "empty list");

console.log(failed === 0 ? "gpu-chip-picker-a11y.test: OK" : "FAILED");
process.exit(failed === 0 ? 0 : 1);
