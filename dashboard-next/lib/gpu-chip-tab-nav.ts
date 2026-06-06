/** Shared ids/helpers for GPU chip picker ARIA tabs (WCAG tab pattern). */

export const GPU_CHIP_TAB_PANEL_ID = "gpu-selected-chip-panel";

export function gpuChipTabId(slug: string): string {
  return `gpu-chip-tab-${slug}`;
}

/** Returns the next tab index for arrow/home/end keys, or null if unhandled. */
export function nextGpuChipTabIndex(key: string, current: number, count: number): number | null {
  if (count <= 0) return null;
  switch (key) {
    case "ArrowRight":
    case "ArrowDown":
      return (current + 1) % count;
    case "ArrowLeft":
    case "ArrowUp":
      return (current - 1 + count) % count;
    case "Home":
      return 0;
    case "End":
      return count - 1;
    default:
      return null;
  }
}
