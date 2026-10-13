// Builds the static Lotta Health site: src/pages/*.html + partials -> dist/.
// No dependencies. Run: npm run build
import { cpSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const src = join(root, "src");
const out = join(root, "dist");

// Content hash per asset so browsers never keep a stale stylesheet or script.
const version = (asset) => createHash("sha1").update(readFileSync(join(src, "assets", asset))).digest("hex").slice(0, 8);
const cssV = version("styles.css");
const jsV = version("main.js");

const partial = (name) => readFileSync(join(src, "partials", `${name}.html`), "utf8");
const head = partial("head").replace("assets/styles.css", `assets/styles.css?v=${cssV}`);
const header = partial("header");
const footer = partial("footer");

// Pages can pull in shared sections with <!-- include: name -->.
const includes = (html) => html.replace(/<!--\s*include:\s*([\w-]+)\s*-->/g, (m, name) => partial(name).trim());

// Each page starts with a meta comment:
// <!-- title: ... | description: ... | nav: home -->
const META = /^<!--\s*(.*?)\s*-->\s*/s;

function parseMeta(html, file) {
  const match = html.match(META);
  if (!match) throw new Error(`${file}: missing meta comment`);
  const meta = {};
  for (const part of match[1].split("|")) {
    const i = part.indexOf(":");
    meta[part.slice(0, i).trim()] = part.slice(i + 1).trim();
  }
  if (!meta.title || !meta.description) throw new Error(`${file}: title and description required`);
  return { meta, body: html.slice(match[0].length) };
}

rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
cpSync(join(src, "assets"), join(out, "assets"), { recursive: true });

const pages = readdirSync(join(src, "pages")).filter((f) => f.endsWith(".html"));
for (const file of pages) {
  const { meta, body } = parseMeta(readFileSync(join(src, "pages", file), "utf8"), file);
  const nav = meta.nav ?? "";
  const navHeader = header.replace(/data-nav="([^"]+)"/g, (m, key) =>
    key === nav ? `${m} aria-current="page"` : m,
  );
  const page = `<!doctype html>
<html lang="de">
<head>
${head.replaceAll("{{title}}", meta.title).replaceAll("{{description}}", meta.description).replaceAll("{{path}}", file === "index.html" ? "" : file)}
</head>
<body>
${navHeader}
<main id="inhalt">
${includes(body.trim())}
</main>
${footer.replaceAll("{{year}}", String(new Date().getFullYear()))}
<script src="assets/main.js?v=${jsV}" defer></script>
</body>
</html>
`;
  writeFileSync(join(out, file), page);
}

console.log(`Built ${pages.length} pages into ${out}`);
