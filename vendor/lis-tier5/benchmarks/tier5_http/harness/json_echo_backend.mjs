#!/usr/bin/env node
/** Minimal JSON REST backend for tier5 proxy_post_json (no external deps). */
import http from "node:http";

const port = Number(process.env.BACKEND_PORT || "39231");
const host = process.env.BACKEND_HOST || "127.0.0.1";
const users = new Map();

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://${host}`);
  if (url.pathname === "/health" && req.method === "GET") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ ok: true }));
    return;
  }
  if (url.pathname === "/api/rest/users" && req.method === "POST") {
    let body = "";
    try {
      body = await readBody(req);
    } catch {
      res.writeHead(413);
      res.end();
      return;
    }
    let parsed;
    try {
      parsed = JSON.parse(body || "{}");
    } catch {
      res.writeHead(400, { "content-type": "application/json" });
      res.end(JSON.stringify({ error: "invalid json" }));
      return;
    }
    const id = String(users.size + 1);
    const row = { id, name: parsed.name || "", email: parsed.email || "" };
    users.set(id, row);
    res.writeHead(201, { "content-type": "application/json" });
    res.end(JSON.stringify(row));
    return;
  }
  res.writeHead(404);
  res.end();
});

server.listen(port, host, () => {
  console.log(`json_echo_backend on ${host}:${port}`);
});
