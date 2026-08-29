/* ============================================
   StudyVault — Account sync
   Everything a student does on a device belongs to their ACCOUNT.

   Before this module, only lesson_visits reached the server: a cleared
   browser or a new phone silently lost subjects, scores, streaks — all
   of it (audit 19 Aug). Now every syncable localStorage key is mirrored
   to the user_state table (one row per key, RLS-scoped to the user):

   - On sign-in the device and account MERGE: dict-like values deep-merge
     (arrays union, newer side wins conflicting leaves), scalars take the
     newer side by timestamp. First sign-in simply uploads the device.
   - After that, every localStorage write to a syncable key is pushed,
     debounced, via an intercepted Storage.setItem — no call site in any
     page needed changing, which is the point: pages keep writing
     localStorage exactly as they always have.
   - A different account signing in on the same device does NOT inherit
     the previous owner's progress: local state is replaced, not merged
     (sv-sync-owner stamps who the device's data belongs to).

   Anonymous visitors are untouched — no session, no sync, site works
   exactly as before. This file must load on every student-facing page.
   ============================================ */
(function () {
  'use strict';

  var SB_URL = 'https://baipckgywpnwapobwtsy.supabase.co';
  var SB_KEY = 'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2';

  /* Exact keys that sync. Deliberately a whitelist: auth tokens, sync
     bookkeeping and anything unknown NEVER leave the device. */
  var KEYS = [
    // identity of the student's course
    'studyvault-subjects', 'studyvault-free-prefs', 'sv-welcome',
    'studyvault-exam-year', 'studyvault-tiers',
    // progress and logs (dict-like: deep-merged)
    'studyvault-visited', 'sv-lessons-done', 'sv-lessons-when',
    'sv-kc-log', 'sv-practice-log', 'sv-flash-log', 'sv-flash-day',
    'sv-warmup-log', 'sv-misconception-log', 'sv-flashcard-progress',
    'sv-ko-data', 'sv-widget-done',
    // shorts
    'sv_shorts_watched', 'sv_shorts_saved', 'sv_shorts_day',
    'sv_shorts_streak', 'sv-shorts-checks',
    // preferences
    'studyvault-a11y', 'sv-focus-mode', 'sv-hl-enabled', 'sv-dash-view',
    // one-time hints (so a new device doesn't replay every tutorial)
    'sv-reader-tour-v1', 'sv-lesson-tutorial-done',
    'sv-flashcard-tutorial-done', 'sv-highlight-tutorial-done',
    'sv_collapsible_hint'
  ];
  var PREFIXES = ['sv-podcast-pos-'];
  var META_KEY = 'sv-sync-meta';    // {key: localWriteTsMs} — never synced
  var OWNER_KEY = 'sv-sync-owner';  // user id the device's data belongs to

  function syncable(k) {
    if (KEYS.indexOf(k) >= 0) return true;
    for (var i = 0; i < PREFIXES.length; i++) {
      if (k.indexOf(PREFIXES[i]) === 0) return true;
    }
    return false;
  }

  // ---- meta (local write timestamps for newer-wins merging) ----
  function meta() {
    try { return JSON.parse(localStorage.getItem(META_KEY)) || {}; }
    catch (e) { return {}; }
  }
  function setMeta(m) {
    applying = true;
    try { localStorage.setItem(META_KEY, JSON.stringify(m)); } catch (e) {}
    applying = false;
  }

  // ---- write interception ----
  var applying = false;          // true while we apply server state locally
  var dirty = {};                // keys changed locally, awaiting push
  var pushTimer = null;
  var session = null;            // current supabase session (or null)

  var origSet = Storage.prototype.setItem;
  var origRemove = Storage.prototype.removeItem;
  Storage.prototype.setItem = function (k, v) {
    origSet.call(this, k, v);
    if (this === window.localStorage && !applying && syncable(k)) noteWrite(k);
  };
  Storage.prototype.removeItem = function (k) {
    origRemove.call(this, k);
    if (this === window.localStorage && !applying && syncable(k)) noteWrite(k);
  };
  function noteWrite(k) {
    var m = meta(); m[k] = Date.now(); setMeta(m);
    if (!session) return;
    dirty[k] = true;
    clearTimeout(pushTimer);
    pushTimer = setTimeout(push, 1500);
  }

  // ---- REST helpers (plain fetch: keepalive works on page hide, and we
  // avoid coupling to whichever supabase-js client the page may have) ----
  function headers() {
    return {
      'apikey': SB_KEY,
      'Authorization': 'Bearer ' + session.access_token,
      'Content-Type': 'application/json'
    };
  }
  function rowsForPush(keys) {
    var rows = [];
    keys.forEach(function (k) {
      var raw = localStorage.getItem(k);
      rows.push({
        user_id: session.user.id, key: k,
        value: { raw: raw },      // verbatim string (or null = deleted)
        updated_at: new Date().toISOString()
      });
    });
    return rows;
  }
  function push(useBeacon) {
    var keys = Object.keys(dirty);
    if (!keys.length || !session) return;
    dirty = {};
    var body = JSON.stringify(rowsForPush(keys));
    fetch(SB_URL + '/rest/v1/user_state?on_conflict=user_id,key', {
      method: 'POST', body: body, keepalive: !!useBeacon,
      headers: Object.assign(headers(), { 'Prefer': 'resolution=merge-duplicates' })
    }).catch(function () {
      // network blip: re-mark so the next write (or unload flush) retries
      keys.forEach(function (k) { dirty[k] = true; });
    });
  }
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') { clearTimeout(pushTimer); push(true); }
  });

  // ---- merging ----
  function parse(raw) {
    if (raw == null) return undefined;
    try { return JSON.parse(raw); } catch (e) { return raw; }
  }
  function isObj(x) { return x && typeof x === 'object' && !Array.isArray(x); }
  function unionArr(a, b) {
    var seen = {}, out = [];
    a.concat(b).forEach(function (x) {
      var id = typeof x === 'string' ? x : JSON.stringify(x);
      if (!seen[id]) { seen[id] = 1; out.push(x); }
    });
    return out;
  }
  /* winner's leaves beat loser's on conflict; dicts merge, arrays union */
  function deepMerge(loser, winner) {
    if (Array.isArray(loser) && Array.isArray(winner)) return unionArr(loser, winner);
    if (isObj(loser) && isObj(winner)) {
      var out = {};
      Object.keys(loser).forEach(function (k) { out[k] = loser[k]; });
      Object.keys(winner).forEach(function (k) {
        out[k] = (k in out) ? deepMerge(out[k], winner[k]) : winner[k];
      });
      return out;
    }
    return winner === undefined ? loser : winner;
  }
  function mergeValues(localRaw, serverRaw, localNewer) {
    var l = parse(localRaw), s = parse(serverRaw);
    if (l === undefined) return serverRaw;
    if (s === undefined) return localRaw;
    if ((isObj(l) && isObj(s)) || (Array.isArray(l) && Array.isArray(s))) {
      var merged = localNewer ? deepMerge(s, l) : deepMerge(l, s);
      return JSON.stringify(merged);
    }
    return localNewer ? localRaw : serverRaw;
  }

  function applyLocal(k, raw) {
    applying = true;
    try {
      if (raw == null) origRemove.call(localStorage, k);
      else origSet.call(localStorage, k, raw);
    } catch (e) {}
    applying = false;
  }

  // ---- the sign-in sync ----
  function fullSync() {
    fetch(SB_URL + '/rest/v1/user_state?select=key,value,updated_at', { headers: headers() })
      .then(function (r) { return r.json(); })
      .then(function (rows) {
        if (!Array.isArray(rows)) return;
        var owner = localStorage.getItem(OWNER_KEY);
        var foreign = owner && owner !== session.user.id;
        var m = meta();
        var serverKeys = {};

        rows.forEach(function (row) {
          if (!syncable(row.key)) return;
          serverKeys[row.key] = true;
          var serverRaw = row.value ? row.value.raw : null;
          if (foreign) {
            // different account on this device: replace, never merge
            applyLocal(row.key, serverRaw);
            m[row.key] = Date.now();
            return;
          }
          var localTs = m[row.key] || 0;
          var serverTs = Date.parse(row.updated_at) || 0;
          var mergedRaw = mergeValues(localStorage.getItem(row.key), serverRaw, localTs > serverTs);
          applyLocal(row.key, mergedRaw);
          m[row.key] = Date.now();
          // if the merge produced something richer than the server copy, push it
          if (mergedRaw !== serverRaw) dirty[row.key] = true;
        });

        // device keys the server has never seen
        var candidates = KEYS.slice();
        for (var i = 0; i < localStorage.length; i++) {
          var k = localStorage.key(i);
          if (syncable(k) && candidates.indexOf(k) < 0) candidates.push(k);
        }
        candidates.forEach(function (k) {
          if (serverKeys[k]) return;
          if (foreign) { applyLocal(k, null); delete m[k]; return; }
          if (localStorage.getItem(k) != null) dirty[k] = true;
        });

        applying = true;
        try { localStorage.setItem(OWNER_KEY, session.user.id); } catch (e) {}
        applying = false;
        setMeta(m);
        if (Object.keys(dirty).length) push();
        try {
          document.dispatchEvent(new CustomEvent('sv-account-synced'));
        } catch (e) {}
      })
      .catch(function () {});
  }

  // ---- session discovery (supabase-js session lives in localStorage) ----
  function readSession() {
    try {
      var raw = localStorage.getItem('sb-baipckgywpnwapobwtsy-auth-token');
      if (!raw) return null;
      var tok = JSON.parse(raw);
      if (!tok || !tok.access_token || !tok.user) return null;
      if (tok.expires_at && tok.expires_at * 1000 < Date.now() + 30000) return null;
      return tok;
    } catch (e) { return null; }
  }

  function boot() {
    session = readSession();
    if (session) fullSync();
    // sign-in happening on THIS page (welcome/join): sync when the token lands
    var poll = setInterval(function () {
      var s = readSession();
      if (s && (!session || s.user.id !== session.user.id)) {
        session = s; fullSync();
      } else if (s) {
        session = s; // refreshed token
      }
    }, 3000);
    // storage events from other tabs signing in/out
    window.addEventListener('storage', function (e) {
      if (e.key === 'sb-baipckgywpnwapobwtsy-auth-token') {
        var s = readSession();
        if (s && (!session || s.user.id !== session.user.id)) { session = s; fullSync(); }
        if (!s) session = null;
      }
    });
    void poll;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
