/* Content reads under the school privacy rules (24 Sep 2026).

   Lessons, units, subjects, guide pages and school lesson edits are private to each school,
   and unpublished lessons to staff (supabase/migrations/20260924210000_school_content_private.sql).
   Many pages read these tables with plain fetches that carry only the public key, which the
   database now treats as a signed-out visitor. This puts the right identity on those reads:

   * an admin session (shared admin password, which the database cannot see): content reads go
     to /api/staff/rest, where the password is checked on the server;
   * a signed-in user: a content read that carries no sign-in gets the user's token, so a pupil
     sees their school's lessons; if the token has expired the read is retried as a visitor,
     which still returns the free tier.

   Load it BEFORE the Supabase library and before any page script that fetches content: the
   library keeps the fetch it finds when a client is created. For visitors it does nothing. */
(function () {
  'use strict';
  if (!window.fetch) return;
  var BASE = 'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/';
  var CONTENT = /^(lessons|units|subjects|guide_pages|lesson_overrides)(\?|$)/;
  var PASS = ['accept', 'prefer', 'range', 'range-unit'];
  var TOKEN_KEY = 'sb-baipckgywpnwapobwtsy-auth-token';
  var nativeFetch = window.fetch.bind(window);

  var adminPw = null;
  try {
    var s = JSON.parse(sessionStorage.getItem('studyvault-auth')) || JSON.parse(localStorage.getItem('studyvault-auth'));
    if (s && s.pw && s.role === 'admin') adminPw = s.pw;
  } catch (e) {}

  function userToken() {
    try { var raw = localStorage.getItem(TOKEN_KEY); return raw ? (JSON.parse(raw) || {}).access_token || null : null; }
    catch (e) { return null; }
  }

  window.fetch = function (input, init) {
    try {
      var url = typeof input === 'string' ? input : (input && input.url) || String(input);
      var method = ((init && init.method) || (input && input.method) || 'GET').toUpperCase();
      if (url.indexOf(BASE) !== 0 || (method !== 'GET' && method !== 'HEAD') || !CONTENT.test(url.slice(BASE.length))) {
        return nativeFetch(input, init);
      }
      var from = new Headers((init && init.headers) || (input && input.headers) || {});

      if (adminPw) {
        var h = { 'X-Admin-Password': adminPw };
        PASS.forEach(function (k) { var v = from.get(k); if (v) h[k] = v; });
        return nativeFetch('/api/staff/rest?p=' + encodeURIComponent(url.slice(BASE.length)),
          { method: method, headers: h, signal: init && init.signal });
      }

      // Supabase clients already sign their requests; plain fetches carry only the apikey.
      var tok = userToken();
      if (tok && !from.has('authorization')) {
        var signed = new Headers(from);
        signed.set('Authorization', 'Bearer ' + tok);
        var opts = Object.assign({}, init || {}, { method: method, headers: signed });
        return nativeFetch(url, opts).then(function (r) {
          return r.status === 401 ? nativeFetch(input, init) : r;
        });
      }
    } catch (e) {}
    return nativeFetch(input, init);
  };
})();
