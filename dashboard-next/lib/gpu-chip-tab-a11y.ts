/** Shared ids/helpers for GPU chip picker tabs (WCAG tab pattern). */

export const GPU_CHIP_TAB_PANEL_ID = "gpu-chip-tabpanel";

export function gpuChipTabId(slug: string): string {
  return `gpu-chip-tab-${slug}`;
}

export type GpuChipTabKey =
  | "ArrowRight"
  | "ArrowDown"
  | "ArrowLeft"
  | "ArrowUp"
  | "Home"
  | "End";

/** Next tab index after arrow/home/end; null when key is not handled. */
export function nextGpuChipTabIndex(
  key: string,
  currentIndex: number,
  tabCount: number,
): number | null {
  if (tabCount <= 0 || currentIndex < 0) return null;

  switch (key as GpuChipTabKey) {
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
