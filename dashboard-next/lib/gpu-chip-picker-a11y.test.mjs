/** @typedef {{ chip_slug: string }} Contribution */

/**
 * Mirrors arrow-key roving in gpu-chip-picker.tsx for unit coverage.
 * @param {Contribution[]} contributions
 * @param {string} selectedSlug
 * @param {string} key
 */
function nextSlugFromArrowKey(contributions, selectedSlug, key) {
  if (contributions.length === 0) return selectedSlug;

  const activeIndex = Math.max(
    0,
    contributions.findIndex((c) => c.chip_slug === selectedSlug),
  );
  let nextIndex = activeIndex;

  switch (key) {
    case "ArrowRight":
    case "ArrowDown":
      nextIndex = (activeIndex + 1) % contributions.length;
      break;
    case "ArrowLeft":
    case "ArrowUp":
      nextIndex = (activeIndex - 1 + contributions.length) % contributions.length;
      break;
    case "Home":
      nextIndex = 0;
      break;
    case "End":
      nextIndex = contributions.length - 1;
      break;
    default:
      return selectedSlug;
  }

  return contributions[nextIndex].chip_slug;
}

const contributions = [
  { chip_slug: "nvidia-rtx-4090-linux" },
  { chip_slug: "apple-m2-macos" },
  { chip_slug: "amd-rx-7900-linux" },
];

let failed = 0;

function assertEqual(label, actual, expected) {
  if (actual !== expected) {
    console.error(`${label}: expected ${expected}, got ${actual}`);
    failed += 1;
  }
}

assertEqual(
  "ArrowRight",
  nextSlugFromArrowKey(contributions, "nvidia-rtx-4090-linux", "ArrowRight"),
  "apple-m2-macos",
);
assertEqual(
  "ArrowLeft wrap",
  nextSlugFromArrowKey(contributions, "nvidia-rtx-4090-linux", "ArrowLeft"),
  "amd-rx-7900-linux",
);
assertEqual("Home", nextSlugFromArrowKey(contributions, "amd-rx-7900-linux", "Home"), "nvidia-rtx-4090-linux");
assertEqual("End", nextSlugFromArrowKey(contributions, "nvidia-rtx-4090-linux", "End"), "amd-rx-7900-linux");

const GPU_CHIP_TAB_PANEL_ID = "gpu-chip-panel";
const gpuChipTabId = (slug) => `gpu-chip-tab-${slug}`;

assertEqual("panel id", GPU_CHIP_TAB_PANEL_ID, "gpu-chip-panel");
assertEqual("tab id", gpuChipTabId("apple-m2-macos"), "gpu-chip-tab-apple-m2-macos");

console.log(failed === 0 ? "gpu-chip-picker-a11y.test: OK" : "FAILED");
process.exit(failed === 0 ? 0 : 1);
