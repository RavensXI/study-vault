const CACHE_VERSION = 'sv-v9';
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
  '/js/free-user-filters.js',
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

  // Page navigations — network first. The cached copy is served ONLY when the
  // browser reports it is offline. A failed navigation fetch while online is
  // NOT offline (a preview deployment's SSO redirect, a proxy error) — serving
  // cache there used to wedge an origin on a stale page indefinitely with no
  // error in the console. Fail visibly instead so the cause can be seen.
  if (event.request.mode === 'navigate') {
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
        if (self.navigator && self.navigator.onLine === false) {
          return caches.match(event.request).then(function (cached) {
            return cached || errorPage('You are offline',
              'This page is not saved for offline use. Reconnect and try again.');
          });
        }
        return errorPage('Connection problem',
          'StudyVault could not reach the server. This is a network or server issue, not your connection being offline.');
      })
    );
    return;
  }

  // Everything else (shell assets, API routes, subresources) — network first,
  // cache fallback. A stale stylesheet or script cannot wedge navigation, and
  // offline use of previously visited pages needs it.
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

// A visible, never-cached failure page (503) with a retry button.
function errorPage(title, message) {
  var html = '<!doctype html><html><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1">' +
    '<title>' + title + ' — StudyVault</title></head>' +
    '<body style="margin:0;display:flex;align-items:center;justify-content:center;min-height:100vh;background:#faf8f5;color:#2d2a26;font-family:Inter,system-ui,sans-serif;text-align:center;padding:2rem;">' +
    '<div style="max-width:26rem;"><h1 style="font-size:1.4rem;margin:0 0 0.75rem;">' + title + '</h1>' +
    '<p style="margin:0 0 1.5rem;line-height:1.5;">' + message + '</p>' +
    '<button onclick="location.reload()" style="background:#2d2a26;color:#faf8f5;border:0;border-radius:16px;padding:0.75rem 1.75rem;font-size:1rem;font-family:inherit;cursor:pointer;">Try again</button>' +
    '</div></body></html>';
  return new Response(html, {
    status: 503,
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' }
  });
}
