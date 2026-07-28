#!/usr/bin/env node
/**
 * Vercel Node entry — Framework Preset: Node (detects server.js).
 * Starts the @taskmark/ui standalone server bound to this board root.
 *
 * Locally you can also: npm start  →  taskmark serve
 *
 * Note: use a literal require.resolve so Vercel NFT can see the entry;
 * vercel.json also includeFiles the full @taskmark/ui tree + board markdown.
 */
import { createRequire } from "node:module"
import fs from "node:fs"
import { pathToFileURL } from "node:url"
import { fileURLToPath } from "node:url"
import path from "node:path"

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const require = createRequire(import.meta.url)

if (!process.env.TASKMARK_BOARD?.trim()) {
  process.env.TASKMARK_BOARD = __dirname
}
process.env.HOSTNAME ??= "0.0.0.0"
if (!process.env.PORT && !process.env.TASKMARK_PORT) {
  // Local default matches CLI; Vercel injects PORT.
  process.env.PORT = "8275"
}

let serverJs
try {
  // Literal path — helps Node File Trace include the standalone entry.
  serverJs = require.resolve("@taskmark/ui/dist/standalone/server.js")
} catch {
  serverJs = null
}

if (!serverJs || !fs.existsSync(serverJs)) {
  console.error(
    `@taskmark/ui standalone server missing` +
      (serverJs ? ` at ${serverJs}` : " (package not installed or incomplete)")
  )
  console.error("Reinstall: npm install @taskmark/ui --save")
  console.error(
    "On Vercel, ensure @taskmark/ui is under dependencies (not devDependencies)"
  )
  process.exit(1)
}

console.log(`Taskmark UI (Vercel/Node)`)
console.log(`  board:  ${process.env.TASKMARK_BOARD}`)
console.log(`  listen: ${process.env.HOSTNAME}:${process.env.PORT}`)

await import(pathToFileURL(serverJs).href)
