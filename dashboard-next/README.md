# Li benchmarks dashboard (Next.js)

Static export for GitHub Pages at `/benchmarks`.

## Dev

```bash
npm install
npm run dev
```

Open http://localhost:3000/benchmarks (basePath).

## Build

```bash
npm ci
npm run build
```

Output: `out/`. Build reads `../data/latest/summary.json` at compile time (`lib/summary.ts`).

## GitHub Pages deploy (WP8)

CI and Pages deploy **dashboard-next** (see [`.github/workflows/pages.yml`](../.github/workflows/pages.yml)). The legacy Vite app in `../dashboard/` is unchanged and not deployed.

After `npm run build`, copy latest ingest artifacts into the static export (skip missing files):

```bash
mkdir -p out/latest
for f in summary.json release-index.json benchmark-matrix.json; do
  if [ -f "../data/latest/$f" ]; then
    cp "../data/latest/$f" out/latest/
  fi
done
```

Upload path for GitHub Pages: `dashboard-next/out` (requires `index.html` at the artifact root). Runtime fetch URL for client-side data: `/benchmarks/latest/summary.json`.
