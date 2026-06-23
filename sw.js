/* Service worker for offline study.
 *
 * Conservative strategy to avoid stale content:
 *   • Navigations (HTML pages) → network-first, fall back to cache offline.
 *   • Same-origin assets (css/js/json) → cache-first, then network.
 *   • Cross-origin (e.g. the Pyodide CDN, highlight.js) → not intercepted.
 * Bump VERSION to invalidate old caches on deploy. */
var VERSION = "v1";
var CACHE = "dssp-" + VERSION;
var CORE = [
  "./",
  "index.html",
  "overview.html",
  "manifest.webmanifest",
  "styles/glass.css",
  "styles/effects.js",
  "styles/nav-ux.js",
  "styles/search.js",
  "styles/hands-on.js",
  "styles/icon.svg",
  "search_index.json",
];

self.addEventListener("install", function (e) {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return c.addAll(CORE).catch(function () {});
    })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches
      .keys()
      .then(function (keys) {
        return Promise.all(
          keys.filter(function (k) { return k !== CACHE; }).map(function (k) {
            return caches.delete(k);
          })
        );
      })
      .then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  if (new URL(req.url).origin !== self.location.origin) return; // leave CDNs alone

  var isPage =
    req.mode === "navigate" ||
    (req.headers.get("accept") || "").indexOf("text/html") !== -1;

  if (isPage) {
    e.respondWith(
      fetch(req)
        .then(function (res) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); });
          return res;
        })
        .catch(function () {
          return caches.match(req).then(function (r) {
            return r || caches.match("index.html");
          });
        })
    );
  } else {
    e.respondWith(
      caches.match(req).then(function (cached) {
        return (
          cached ||
          fetch(req).then(function (res) {
            var copy = res.clone();
            caches.open(CACHE).then(function (c) { c.put(req, copy); });
            return res;
          })
        );
      })
    );
  }
});
