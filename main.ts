// Entry for make.fun's news-image-20261121: "Sum up 21 November's world news in one image".
// entry.png is rendered ahead of time from src/front.html (tools/render.ps1); at grading time
// this program only copies those exact bytes to the output folder, so every run gives the same file.
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const png = readFileSync(new URL('./entry.png', import.meta.url));
// The contest takes a PNG or JPEG of at most 1 MiB and 1024 x 1024 pixels: refuse to write anything else.
const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (!signature.every((b, i) => png[i] === b)) throw new Error('entry.png is not a PNG');
if (png.length > 1048576) throw new Error(`entry.png is ${png.length} bytes, over 1 MiB`);
const width = png.readUInt32BE(16), height = png.readUInt32BE(20);
if (width > 1024 || height > 1024) throw new Error(`entry.png is ${width}x${height}, over 1024x1024`);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), png);
