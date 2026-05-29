import fs from "fs";
import path from "path";

export type CatalogAudit = {
  schema: string;
  catalog_rows: number;
  harness_pending_count: number;
  workload_dir_present_count: number;
  workload_dir_missing_count: number;
};

export function loadCatalogAudit(): CatalogAudit | null {
  const p = path.join(process.cwd(), "data/latest/catalog-audit.json");
  if (!fs.existsSync(p)) return null;
  return JSON.parse(fs.readFileSync(p, "utf8")) as CatalogAudit;
}
