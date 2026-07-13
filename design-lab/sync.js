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
           warmlog: g('sv-warmup-log', {}),
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
    if (remote.flashday && (!L.flashday || remote.flashday > L.flashday)) L.flashday = remote.flashday;
  }
  try {
    localStorage.setItem('sv-lessons-done', JSON.stringify(L.done));
    localStorage.setItem('sv-lessons-when', JSON.stringify(L.when));
    if (L.plan) localStorage.setItem('sv-plan-prefs', JSON.stringify(L.plan));
    if (L.warmup) localStorage.setItem('sv-warmup', JSON.stringify(L.warmup));
    if (L.warmlog) localStorage.setItem('sv-warmup-log', JSON.stringify(L.warmlog));
    if (L.flashday) localStorage.setItem('sv-flash-day', L.flashday);
    Object.keys(L.tasks).forEach(function (k) {
      localStorage.setItem('sv_progress_' + k, JSON.stringify(L.tasks[k]));
    });
  } catch (e) {}
  return L;
}

function svProgressPush(payload, tok) {
  tok = tok || svTok();
  if (!tok) return Promise.resolve(false);
  return fetch(SVSYNC_URL + '/auth/v1/user', {
    method: 'PUT',
    headers: { apikey: SVSYNC_KEY, 'Content-Type': 'application/json', Authorization: 'Bearer ' + tok },
    body: JSON.stringify({ data: { sv_progress: Object.assign({}, payload || svProgressGather(),
      { updated: new Date().toISOString() }) } })
  }).then(function (r) { return r.ok; }).catch(function () { return false; });
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
  fetch(SVSYNC_URL + '/auth/v1/user', { headers: { apikey: SVSYNC_KEY, Authorization: 'Bearer ' + tok } })
    .then(function (r) { if (!r.ok) throw 0; return r.json(); })
    .then(function (u) {
      var M = svProgressMerge(u.user_metadata && u.user_metadata.sv_progress);
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
