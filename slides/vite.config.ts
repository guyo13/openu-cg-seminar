import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'
import { createReadStream, existsSync, statSync } from 'node:fs'
import { defineConfig } from 'vite'

const here = dirname(fileURLToPath(import.meta.url))
const repoRoot = resolve(here, '..')
const figsRoot = resolve(repoRoot, 'figs')

const MIME: Record<string, string> = {
  '.png': 'image/png',
  '.gif': 'image/gif',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
}

// Dev-only. Slides reference figures as "../figs/...", which the production
// build turns into a hashed asset import (works). The dev server instead
// leaves the URL literal and base-prefixes it to "/../figs/...", which the
// browser normalises to "/figs/..." — not a dev route, so Vite's SPA fallback
// answers with index.html and every image renders broken. Serve those
// requests from the repo-root figs/ directory instead.
function serveRepoFigs() {
  return {
    name: 'serve-repo-figs',
    apply: 'serve' as const,
    configureServer(server: any) {
      server.middlewares.use('/figs', (req: any, res: any, next: any) => {
        const rel = decodeURIComponent((req.url || '/').split('?')[0])
        const file = resolve(figsRoot, '.' + rel)
        if (!file.startsWith(figsRoot + '/') || !existsSync(file) || !statSync(file).isFile())
          return next()
        res.setHeader('Content-Type', MIME[file.slice(file.lastIndexOf('.')).toLowerCase()]
          ?? 'application/octet-stream')
        createReadStream(file).pipe(res)
      })
    },
  }
}

export default defineConfig({
  plugins: [serveRepoFigs()],
  // figures live outside the Slidev root, so allow reading from the repo root
  server: { fs: { allow: [repoRoot] } },
})
