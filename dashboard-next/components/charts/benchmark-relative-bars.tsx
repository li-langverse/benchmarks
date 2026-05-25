import type { BenchmarkRelativeItem } from "@/lib/pillar-charts";
import { RelativeBarList, type RelativeBarItem } from "@/components/charts/relative-bar-list";

type BenchmarkRelativeBarsProps = {
  items: BenchmarkRelativeItem[];
  title: string;
  benchHref?: (id: string) => string;
};

export function BenchmarkRelativeBars({
  items,
  title,
  benchHref = (id) => `/bench/${id}/`,
}: BenchmarkRelativeBarsProps) {
  const barItems: RelativeBarItem[] = items.map((item) => ({
    key: item.benchmark,
    label: item.benchmark,
    relative: item.relative,
    highlight: item.claimable && item.relative >= 1,
    dimmed: !item.claimable,
    href: benchHref(item.benchmark),
  }));

  return (
    <RelativeBarList
      items={barItems}
      ariaLabel={title}
      caption={
        <>
          {title} — Li relative speed vs best competitor (<code>ratio_vs_sota</code>), higher is
          better.
        </>
      }
      referenceNote="1.0 = best competitor in series; Li is never labeled SOTA."
    />
  );
}
