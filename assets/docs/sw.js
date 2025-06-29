// 🚀 Arkalia Service Worker - Ultra Simple & Rapide
const CACHE_NAME = "arkalia-v3.1";
const CACHE_FILES = [
    "/",
    "/assets/arkalia-luna-theme.css",
    "/assets/js/arkalia-assistant.js",
    "/assets/logo.svg",
    "/assets/favicon.svg"
];

// 📦 Installation
self.addEventListener("install", (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(CACHE_FILES))
            .then(() => self.skipWaiting())
    );
});

// 🔄 Activation
self.addEventListener("activate", (e) => {
    e.waitUntil(
        caches.keys().then(names =>
            Promise.all(
                names.filter(name => name !== CACHE_NAME)
                     .map(name => caches.delete(name))
            )
        ).then(() => self.clients.claim())
    );
});

// 🌐 Fetch
self.addEventListener("fetch", (e) => {
    e.respondWith(
        caches.match(e.request)
            .then(response => response || fetch(e.request))
            .catch(() => caches.match("/"))
    );
});
