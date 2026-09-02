import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'
import { defineConfig } from 'vite'

const here = dirname(fileURLToPath(import.meta.url))

// Figures live in ../figs (produced by the marimo notebook at the repo root),
// which is outside Slidev's Vite root. Allow reading from the repo root so
// slides can reference them relatively without duplicating the files.
export default defineConfig({
  server: {
    fs: {
      allow: [resolve(here, '..')],
    },
  },
})
