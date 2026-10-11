// Minimal static server for dist/ (used by Railway via `npm start`). No dependencies.
// Sends X-Robots-Tag: noindex until the site is ready for launch (set INDEXING=on to allow).
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { dirname, extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const dist = join(dirname(fileURLToPath(import.meta.url)), "dist");
const port = Number(process.env.PORT) || 8080;
const noindex = process.env.INDEXING !== "on";

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".ico": "image/x-icon",
  ".txt": "text/plain; charset=utf-8",
};

async function resolve(urlPath) {
  let path = decodeURIComponent(urlPath.split("?")[0]);
  if (path.endsWith("/")) path += "index.html";
  if (!extname(path)) path += ".html"; // clean URLs: /programm -> programm.html
  const file = normalize(join(dist, path));
  if (!file.startsWith(dist)) return null;
  try {
    return { file, body: await readFile(file) };
  } catch {
    return null;
  }
}

createServer(async (req, res) => {
  const headers = { "X-Content-Type-Options": "nosniff" };
  if (noindex) headers["X-Robots-Tag"] = "noindex, nofollow";
  if (req.url === "/robots.txt" && noindex) {
    res.writeHead(200, { ...headers, "Content-Type": TYPES[".txt"] });
    return res.end("User-agent: *\nDisallow: /\n");
  }
  let found = null;
  try {
    found = await resolve(req.url ?? "/");
  } catch {
    found = null; // malformed URL encoding
  }
  if (!found) {
    const notFound = await readFile(join(dist, "404.html")).catch(() => "Not found");
    res.writeHead(404, { ...headers, "Content-Type": TYPES[".html"] });
    return res.end(notFound);
  }
  const type = TYPES[extname(found.file)] ?? "application/octet-stream";
  const cache = type.startsWith("text/html") ? "no-cache" : "public, max-age=3600";
  res.writeHead(200, { ...headers, "Content-Type": type, "Cache-Control": cache });
  res.end(found.body);
}).listen(port, () => console.log(`Lotta Health site on :${port}`));
