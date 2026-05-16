import { defineConfig } from "vite";

export default defineConfig({
  base: "/benchmarks/",
  publicDir: "../data",
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
});
