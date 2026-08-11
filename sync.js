/* svSync — progress lives on the ACCOUNT (user_metadata.sv_progress), same
   place the wizard setup already syncs. Signed in: dashboards pull-merge on
   load and push after; lesson pages push after each completion; sign-in
   restores everything onto a fresh device. Signed out (guest): everything
   just stays local, exactly as before.

   Merge rules are additive so no device can erase another's work:
   completions are unioned, task ticks OR together, newest daily stamps win.

   Self-contained (home-study loads it without dash-data.js). */

var SVSYNC_URL = 'https://baipckgywpnwapobwtsy.supabase.co';
var SVSYNC_KEY = 'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2';
var SVSYNC_TOKKEY = 'sb-baipckgywpnwapobwtsy-auth-token';

function svTok() {
  try { var s = JSON.parse(localStorage.getItem(SVSYNC_TOKKEY)); return (s && s.access_token) || null; }
  catch (e) { return null; }
}

/* everything progress-shaped this device knows */
function svProgressGather() {
  var g = function (k, d) { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } };
  var tasks = {};
  try {
    Object.keys(localStorage).forEach(function (k) {
      if (k.indexOf('sv_progress_') === 0) {
        try { tasks[k.slice(12)] = JSON.parse(localStorage.getItem(k)); } catch (e) {}
      }
    });
  } catch (e) {}
  return { done: g('sv-lessons-done', {}), when: g('sv-lessons-when', {}),
           plan: g('sv-plan-prefs', null), warmup: g('sv-warmup', null),
           warmlog: g('sv-warmup-log', {}), kc: g('sv-kc-log', {}),
           practice: g('sv-practice-log', []), shortschecks: g('sv-shorts-checks', []),
           flashlog: g('sv-flash-log', []),
           miscon: g('sv-misconception-log', []),
           flashsr: g('sv-flashcard-progress', null),
           flashday: localStorage.getItem('sv-flash-day') || null, tasks: tasks };
}

/* fold the account copy into this device (additive), write back to
   localStorage, return the merged object */
function svProgressMerge(remote) {
  var L = svProgressGather();
  if (remote) {
    Object.keys(remote.done || {}).forEach(function (k) {
      var a = L.done[k] || [];
      (remote.done[k] || []).forEach(function (n) { if (a.indexOf(n) < 0) a.push(n); });
      L.done[k] = a;
    });
    L.when = Object.assign({}, remote.when || {}, L.when);
    Object.keys(remote.tasks || {}).forEach(function (k) {
      var loc = L.tasks[k], rem = remote.tasks[k] || {};
      if (!loc) { L.tasks[k] = rem; return; }
      Object.keys(rem).forEach(function (t) { if (rem[t] === true) loc[t] = true; });
    });
    if (!L.plan && remote.plan) L.plan = remote.plan;
    if (remote.warmup && (!L.warmup || remote.warmup.date > L.warmup.date)) L.warmup = remote.warmup;
    L.warmlog = Object.assign({}, remote.warmlog || {}, L.warmlog || {});
    L.kc = Object.assign({}, remote.kc || {}, L.kc || {});
    /* answer logs: union by identity, newest first, capped */
    var seen = {};
    L.practice = (L.practice || []).concat(remote.practice || []).filter(function (e) {
      var k = e.d + '|' + e.k + '|' + (e.q || '').slice(0, 40);
      if (seen[k]) return false; seen[k] = 1; return true;
    }).slice(0, 60);
    var seen2 = {};
    L.shortschecks = (L.shortschecks || []).concat(remote.shortschecks || []).filter(function (e) {
      var k = e.d + '|' + e.lid + '|' + e.ti;
      if (seen2[k]) return false; seen2[k] = 1; return true;
    }).slice(0, 300);
    var seen3 = {};
    L.flashlog = (L.flashlog || []).concat(remote.flashlog || []).filter(function (e) {
      var k = e.t || JSON.stringify(e);
      if (seen3[k]) return false; seen3[k] = 1; return true;
    }).sort(function (a, b) { return (b.t || 0) - (a.t || 0); }).slice(0, 400);
    if (remote.flashday && (!L.flashday || remote.flashday > L.flashday)) L.flashday = remote.flashday;
    var seen4 = {};
    L.miscon = (L.miscon || []).concat(remote.miscon || []).filter(function (e) {
      var k = e.d + '|' + e.sub + '|' + e.unit + '|' + e.n + '|' + (e.tag || '').slice(0, 40);
      if (seen4[k]) return false; seen4[k] = 1; return true;
    }).slice(0, 200);
    /* Leitner boxes: per card, the copy with more attempts is the truer one */
    if (remote.flashsr && remote.flashsr.cards) {
      L.flashsr = L.flashsr || { cards: {}, streak: 0 };
      L.flashsr.cards = L.flashsr.cards || {};
      Object.keys(remote.flashsr.cards).forEach(function (k) {
        var loc = L.flashsr.cards[k], rem = remote.flashsr.cards[k];
        if (!loc || (rem.attempts || 0) > (loc.attempts || 0)) L.flashsr.cards[k] = rem;
      });
      L.flashsr.streak = Math.max(L.flashsr.streak || 0, remote.flashsr.streak || 0);
    }
  }
  try {
    localStorage.setItem('sv-lessons-done', JSON.stringify(L.done));
    localStorage.setItem('sv-lessons-when', JSON.stringify(L.when));
    if (L.plan) localStorage.setItem('sv-plan-prefs', JSON.stringify(L.plan));
    if (L.warmup) localStorage.setItem('sv-warmup', JSON.stringify(L.warmup));
    if (L.warmlog) localStorage.setItem('sv-warmup-log', JSON.stringify(L.warmlog));
    if (L.kc) localStorage.setItem('sv-kc-log', JSON.stringify(L.kc));
    if (L.practice) localStorage.setItem('sv-practice-log', JSON.stringify(L.practice));
    if (L.shortschecks) localStorage.setItem('sv-shorts-checks', JSON.stringify(L.shortschecks));
    if (L.flashlog) localStorage.setItem('sv-flash-log', JSON.stringify(L.flashlog));
    if (L.miscon) localStorage.setItem('sv-misconception-log', JSON.stringify(L.miscon));
    if (L.flashsr) localStorage.setItem('sv-flashcard-progress', JSON.stringify(L.flashsr));
    if (L.flashday) localStorage.setItem('sv-flash-day', L.flashday);
    Object.keys(L.tasks).forEach(function (k) {
      localStorage.setItem('sv_progress_' + k, JSON.stringify(L.tasks[k]));
    });
  } catch (e) {}
  return L;
}

/* progress lives in its OWN TABLE (public.progress, own-row RLS) — never in
   user_metadata: Supabase embeds metadata in every access token, and a term
   of history once bloated student JWTs past Cloudflare's header limits,
   520-ing all their content requests. */
function svUid(tok) {
  try { return JSON.parse(atob(tok.split('.')[1].replace(/-/g, '+').replace(/_/g, '/'))).sub || null; }
  catch (e) { return null; }
}

function svProgressPush(payload, tok) {
  tok = tok || svTok();
  var uid = tok && svUid(tok);
  if (!uid) return Promise.resolve(false);
  return fetch(SVSYNC_URL + '/rest/v1/progress', {
    method: 'POST',
    headers: { apikey: SVSYNC_KEY, 'Content-Type': 'application/json',
               Authorization: 'Bearer ' + tok, Prefer: 'resolution=merge-duplicates' },
    body: JSON.stringify({ person_id: uid,
      blob: Object.assign({}, payload || svProgressGather(), { updated: new Date().toISOString() }),
      updated_at: new Date().toISOString() })
  }).then(function (r) { return r.ok; }).catch(function () { return false; });
}

/* the account's copy: RLS returns only the caller's own row */
function svProgressFetch(tok) {
  tok = tok || svTok();
  if (!tok) return Promise.resolve(null);
  return fetch(SVSYNC_URL + '/rest/v1/progress?select=blob&limit=1', {
    headers: { apikey: SVSYNC_KEY, Authorization: 'Bearer ' + tok }
  }).then(function (r) { return r.ok ? r.json() : []; })
    .then(function (rows) { return (rows[0] && rows[0].blob) || null; })
    .catch(function () { return null; });
}

var _svPushT = null;
function svProgressPushSoon() {
  clearTimeout(_svPushT);
  _svPushT = setTimeout(function () { svProgressPush(); }, 1500);
}

/* dashboards call this on load: pull the account copy, merge, push the
   union back. If the account knew things this device didn't, one reload
   (per session) repaints everything from the merged state. */
function svProgressSync() {
  var tok = svTok(); if (!tok) return;
  var before = JSON.stringify(svProgressGather());
  svProgressFetch(tok)
    .then(function (remote) {
      var M = svProgressMerge(remote);
      var changed = JSON.stringify({ done: M.done, when: M.when, plan: M.plan, warmup: M.warmup,
        flashday: M.flashday, tasks: M.tasks }) !== before;
      return svProgressPush(M, tok).then(function () {
        if (changed && !sessionStorage.getItem('sv-sync-reloaded')) {
          sessionStorage.setItem('sv-sync-reloaded', '1');
          location.reload();
        }
      });
    })
    .catch(function () {});
}

/* sign out = push what we have, then clean the device. Safe now the account
   holds it all — sign back in anywhere and it comes home. */
function svSignOut() {
  var wipe = function () {
    try {
      ['sv-user', 'sv-welcome', 'sv-lessons-done', 'sv-lessons-when', 'sv-warmup',
       'sv-flash-day', 'sv-plan-prefs'].forEach(function (k) { localStorage.removeItem(k); });
      Object.keys(localStorage).forEach(function (k) {
        if (k.indexOf('sv_progress_') === 0 || /^sb-.*-auth-token/.test(k)) localStorage.removeItem(k);
      });
      sessionStorage.removeItem('sv-sync-reloaded');
    } catch (e) {}
    location.href = 'home-study.html';
  };
  svProgressPush().then(wipe, wipe);
}
