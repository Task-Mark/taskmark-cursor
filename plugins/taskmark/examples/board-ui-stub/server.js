#!/usr/bin/env node
/**
 * Vercel Node entry — Framework Preset: Node (detects server.js).
 * Starts the @taskmark/ui standalone server bound to this board root.
 *
 * Locally you can also: npm start  →  taskmark serve
 */
import { createRequire } from "node:module"
import fs from "node:fs"
import path from "node:path"
import { pathToFileURL } from "node:url"
import { fileURLToPath } from "node:url"

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const require = createRequire(import.meta.url)

if (!process.env.TASKMARK_BOARD?.trim()) {
  process.env.TASKMARK_BOARD = __dirname
}
process.env.HOSTNAME ??= "0.0.0.0"
if (!process.env.PORT && !process.env.TASKMARK_PORT) {
  process.env.PORT = "8275"
}

const uiPkgJson = require.resolve("@taskmark/ui/package.json")
const uiRoot = path.dirname(uiPkgJson)
const serverJs = path.join(uiRoot, "dist", "standalone", "server.js")

if (!fs.existsSync(serverJs)) {
  console.error(`@taskmark/ui standalone server missing at ${serverJs}`)
  console.error("Reinstall: npm install @taskmark/ui")
  process.exit(1)
}

console.log(`Taskmark UI (Vercel/Node)`)
console.log(`  board:  ${process.env.TASKMARK_BOARD}`)
console.log(`  listen: ${process.env.HOSTNAME}:${process.env.PORT}`)

await import(pathToFileURL(serverJs).href)
