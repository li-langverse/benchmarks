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
npm run build
```

Output: `out/`. Copy `../data/latest/summary.json` to `out/latest/` before deploy (see `pages.yml` WP8).

## Data

Build reads `../data/latest/summary.json` at compile time.
