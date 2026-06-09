export const GPU_CHIP_TAB_PANEL_ID = "gpu-chip-panel";

export function gpuChipTabId(slug: string): string {
  return `gpu-chip-tab-${slug}`;
}

/** Roving tabindex target for WAI-ARIA tabs (automatic activation). */
export function nextChipTabIndex(
  key: string,
  currentIndex: number,
  count: number,
): number | null {
  if (count <= 0) return null;
  switch (key) {
    case "ArrowLeft":
    case "ArrowUp":
      return currentIndex === 0 ? count - 1 : currentIndex - 1;
    case "ArrowRight":
    case "ArrowDown":
      return currentIndex === count - 1 ? 0 : currentIndex + 1;
    case "Home":
      return 0;
    case "End":
      return count - 1;
    default:
      return null;
  }
}
