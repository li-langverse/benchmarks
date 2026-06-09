/** Stable id helpers for GPU chip tab / tabpanel ARIA wiring. */
export function chipTabId(slug: string): string {
  return `gpu-chip-tab-${slug}`;
}

export function chipPanelId(slug: string): string {
  return `gpu-chip-panel-${slug}`;
}

/** Roving-tab index for arrow/home/end keys (enabled tabs only). */
export function nextChipTabIndex(
  current: number,
  count: number,
  key: string,
): number | null {
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
