// news-image-20261126: copy-only entrypoint for the Thursday front page.
//
// The artwork is the committed entry.png, drawn on the build machine
// with fixed content (no clock, no network, no randomness). This file
// NEVER runs any other program or subprocess at grade time: it only
// copies the exact committed bytes to the output directory, after
// checking the PNG signature and the 1024x1024 header. Node 22,
// standard library only.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const LOCAL_PNG = join(HERE, "entry.png");
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const OUTPUT_PNG = join(OUTPUT_DIR, "entry.png");

function sha256Of(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function checkPng(path) {
  const data = readFileSync(path);
  const signature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (data.length < 33 || !data.subarray(0, 8).equals(signature)) {
    throw new Error(path + " is not a PNG file");
  }
  const w = data.readUInt32BE(16);
  const h = data.readUInt32BE(20);
  if (w !== 1024 || h !== 1024) {
    throw new Error(`${path} is ${w}x${h}, expected 1024x1024`);
  }
  return data.length;
}

if (!existsSync(LOCAL_PNG)) {
  throw new Error("missing committed artwork: " + LOCAL_PNG);
}
const before = sha256Of(LOCAL_PNG);
const size = checkPng(LOCAL_PNG);
mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(LOCAL_PNG, OUTPUT_PNG);
const after = sha256Of(OUTPUT_PNG);
if (before !== after) {
  throw new Error("copy mismatch: " + before + " vs " + after);
}
console.log(`copied entry.png (${size} bytes, sha256 ${before}) to ${OUTPUT_PNG}`);
