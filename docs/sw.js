/* ================================
   🚀 ARKALIA-LUNA SERVICE WORKER v3.0-phase1
   Performance & Cache Optimisé
   ================================ */

const CACHE_NAME = 'arkalia-luna-v3.0-phase1';
const CACHE_VERSION = '3.0.1';

// 📦 Ressources critiques à mettre en cache
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/assets/arkalia-luna-theme.css',
    '/assets/js/arkalia-assistant.js',
    '/assets/logo.svg',
    '/assets/favicon.svg',
    '/quick-start/',
    '/style-demo/',
    '/modules/',
];

// 🎯 Installation du Service Worker
self.addEventListener('install', (event) => {
    console.log('🔧 Service Worker installing...');

    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('📦 Caching static assets...');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('✅ Service Worker installed successfully');
                return self.skipWaiting();
            })
            .catch((error) => {
                console.error('❌ Service Worker installation failed:', error);
            })
    );
});

// 🔄 Activation du Service Worker
self.addEventListener('activate', (event) => {
    console.log('🚀 Service Worker activating...');

    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName !== CACHE_NAME) {
                            console.log('🗑️ Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('✅ Service Worker activated');
                return self.clients.claim();
            })
    );
});

// 🌐 Interception des requêtes réseau
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // 🎯 Stratégie Cache First pour les assets statiques
    if (isStaticAsset(request)) {
        event.respondWith(cacheFirst(request));
        return;
    }

    // 🌐 Stratégie Network First pour les pages
    if (isNavigationRequest(request)) {
        event.respondWith(networkFirst(request));
        return;
    }

    // 📊 Stratégie Stale While Revalidate pour les autres ressources
    event.respondWith(staleWhileRevalidate(request));
});

// 🎯 Cache First Strategy (Assets statiques)
async function cacheFirst(request) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }

        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;

    } catch (error) {
        console.warn('🚨 Cache First failed:', error);
        return new Response('Ressource non disponible', {
            status: 503,
            statusText: 'Service Unavailable'
        });
    }
}

// 🌐 Network First Strategy (Pages)
async function networkFirst(request) {
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;

    } catch (error) {
        console.warn('🌐 Network failed, trying cache:', error);
        const cachedResponse = await caches.match(request);

        if (cachedResponse) {
            return cachedResponse;
        }

        // Page de fallback si pas de cache
        return new Response(`
            <!DOCTYPE html>
            <html>
            <head>
                <title>Arkalia-LUNA - Hors ligne</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body { 
                        font-family: Inter, Arial, sans-serif; 
                        text-align: center; 
                        padding: 50px;
                        background: linear-gradient(135deg, #6366f1, #8b5cf6);
                        color: white;
                        margin: 0;
                    }
                    .container {
                        background: rgba(255, 255, 255, 0.1);
                        backdrop-filter: blur(20px);
                        border-radius: 20px;
                        padding: 40px;
                        max-width: 500px;
                        margin: 0 auto;
                    }
                    h1 { font-size: 2.5rem; margin-bottom: 20px; }
                    p { font-size: 1.2rem; opacity: 0.9; }
                    .retry-btn {
                        background: white;
                        color: #6366f1;
                        border: none;
                        padding: 15px 30px;
                        border-radius: 50px;
                        font-weight: 600;
                        cursor: pointer;
                        margin-top: 20px;
                        font-size: 1rem;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🌙 Arkalia-LUNA</h1>
                    <p>Vous êtes actuellement hors ligne.</p>
                    <p>Vérifiez votre connexion internet et réessayez.</p>
                    <button class="retry-btn" onclick="window.location.reload()">
                        🔄 Réessayer
                    </button>
                </div>
            </body>
            </html>
        `, {
            status: 200,
            headers: { 'Content-Type': 'text/html' }
        });
    }
}

// 📊 Stale While Revalidate Strategy
async function staleWhileRevalidate(request) {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);

    const fetchPromise = fetch(request).then((networkResponse) => {
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    }).catch(() => cachedResponse);

    return cachedResponse || fetchPromise;
}

// 🔍 Utilitaires de détection
function isStaticAsset(request) {
    const url = new URL(request.url);
    return url.pathname.match(/\.(css|js|svg|png|jpg|jpeg|webp|ico|woff2?)$/);
}

function isNavigationRequest(request) {
    return request.mode === 'navigate' ||
        (request.method === 'GET' && request.headers.get('accept').includes('text/html'));
}

// 📊 Messages pour les clients
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }

    if (event.data && event.data.type === 'GET_VERSION') {
        event.ports[0].postMessage({
            version: CACHE_VERSION,
            cacheName: CACHE_NAME
        });
    }
});

// 🧹 Nettoyage automatique du cache (limite de taille)
async function cleanupCache() {
    const cache = await caches.open(CACHE_NAME);
    const requests = await cache.keys();

    if (requests.length > 100) { // Limite de 100 entrées
        const oldestRequests = requests.slice(0, requests.length - 80);
        await Promise.all(oldestRequests.map(request => cache.delete(request)));
        console.log('🧹 Cache cleanup completed');
    }
}

// Nettoyage périodique
setInterval(cleanupCache, 30 * 60 * 1000); // Toutes les 30 minutes 