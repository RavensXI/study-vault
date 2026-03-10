const CACHE_VERSION = 'sv-v3';
const SHELL_CACHE = CACHE_VERSION + '-shell';
const RUNTIME_CACHE = CACHE_VERSION + '-runtime';

// App shell — pre-cached on install for offline support
const SHELL_ASSETS = [
  '/',
  '/css/style.css',
  '/js/main.js',
  '/js/lesson-loader.js',
  '/js/browse-loader.js',
  '/js/guide-loader.js',
  '/lesson.html',
  '/browse.html',
  '/guide.html',
  '/images/padlock.svg',
  '/images/icon-192.png',
  '/manifest.json'
];

// Install — pre-cache app shell (for offline), activate immediately
self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(SHELL_CACHE).then(function (cache) {
      return cache.addAll(SHELL_ASSETS);
    }).then(function () {
      return self.skipWaiting();
    })
  );
});

// Activate — clear old caches, claim clients immediately
self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (key) {
          return key !== SHELL_CACHE && key !== RUNTIME_CACHE;
        }).map(function (key) {
          return caches.delete(key);
        })
      );
    }).then(function () {
      return self.clients.claim();
    })
  );
});

// Fetch strategies
self.addEventListener('fetch', function (event) {
  var url = new URL(event.request.url);

  // Skip non-GET requests and Supabase API calls
  if (event.request.method !== 'GET') return;
  if (url.hostname.includes('supabase')) return;

  // Local images — cache first (rarely change, used on home page)
  if (url.origin === self.location.origin && url.pathname.startsWith('/images/')) {
    event.respondWith(
      caches.open(RUNTIME_CACHE).then(function (cache) {
        return cache.match(event.request).then(function (cached) {
          if (cached) return cached;
          return fetch(event.request).then(function (response) {
            if (response.ok) cache.put(event.request, response.clone());
            return response;
          });
        });
      })
    );
    return;
  }

  // R2 assets (audio, images) — cache first (large, rarely change)
  if (url.hostname.includes('r2.dev')) {
    event.respondWith(
      caches.open(RUNTIME_CACHE).then(function (cache) {
        return cache.match(event.request).then(function (cached) {
          if (cached) return cached;
          return fetch(event.request).then(function (response) {
            if (response.ok) cache.put(event.request, response.clone());
            return response;
          });
        });
      })
    );
    return;
  }

  // Google Fonts — cache first (versioned by Google, stable)
  if (url.hostname.includes('fonts.googleapis.com') || url.hostname.includes('fonts.gstatic.com')) {
    event.respondWith(
      caches.open(RUNTIME_CACHE).then(function (cache) {
        return cache.match(event.request).then(function (cached) {
          if (cached) return cached;
          return fetch(event.request).then(function (response) {
            if (response.ok) cache.put(event.request, response.clone());
            return response;
          });
        });
      })
    );
    return;
  }

  // Everything else (shell assets, pages, API routes) — network first, cache fallback
  event.respondWith(
    fetch(event.request).then(function (response) {
      if (response.ok) {
        var cacheName = SHELL_ASSETS.indexOf(url.pathname) !== -1 ? SHELL_CACHE : RUNTIME_CACHE;
        var clone = response.clone();
        caches.open(cacheName).then(function (cache) {
          cache.put(event.request, clone);
        });
      }
      return response;
    }).catch(function () {
      return caches.match(event.request);
    })
  );
});
