// Checks the built site in dist/: every internal link and #anchor resolves,
// and no page contains en or em dashes. Run: npm run check
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const dist = join(dirname(fileURLToPath(import.meta.url)), "dist");
if (!existsSync(dist)) {
  console.error("dist/ missing. Run npm run build first.");
  process.exit(1);
}

const pages = readdirSync(dist).filter((f) => f.endsWith(".html"));
const html = Object.fromEntries(pages.map((p) => [p, readFileSync(join(dist, p), "utf8")]));
const ids = Object.fromEntries(
  pages.map((p) => [p, new Set([...html[p].matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]))]),
);

const problems = [];
for (const page of pages) {
  for (const [, ref] of html[page].matchAll(/\s(?:href|src)="([^"]+)"/g)) {
    if (/^(https?:|mailto:|tel:|data:)/.test(ref)) continue;
    const [file, anchor] = ref.replace(/\?[^#]*/, "").split("#");
    const target = file || page;
    if (!existsSync(join(dist, target))) problems.push(`${page}: broken link ${ref}`);
    else if (anchor && target.endsWith(".html") && !ids[target]?.has(anchor))
      problems.push(`${page}: missing anchor ${ref}`);
  }
  if (/[–—]/.test(html[page])) problems.push(`${page}: contains an en or em dash`);
}

if (problems.length) {
  console.error(problems.join("\n"));
  process.exit(1);
}
console.log(`OK: ${pages.length} pages, all internal links resolve.`);
