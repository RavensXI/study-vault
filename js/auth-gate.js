/**
 * Auth gate for staff pages.
 *
 *   <script src="/js/auth-gate.js" data-role="admin"></script>           admin only
 *   <script src="/js/auth-gate.js" data-role="admin,teacher"></script>   admin or teacher
 *   (data-auth="teacher" is still accepted and means the same thing.)
 *
 * Load it AFTER supabase-js (and after js/content-reads.js) so the gate can use the library.
 *
 * Every staff page signs in the same way (Tom, 29 Sep 2026): a Supabase account at
 * /teacher/login. Admin is Tom's account (profiles.role = platform_admin) AND a session that
 * passed the two-factor step (aal2, a code from Microsoft Authenticator; js/staff-mfa.js). The
 * shared ADMIN_PASSWORD is retired, and any copy of it left in browser storage is erased here.
 *
 * The page's own calls to /api/ get the signed-in user's token added (Authorization: Bearer),
 * which is what the server checks (api/_lib/admin-auth.js, api/pipeline/_lib/auth.js). The
 * cached 'studyvault-auth' entry only decides what the page shows; it grants nothing.
 */
(function () {
  var script = document.currentScript;
  var allowedRoles = (script.getAttribute('data-role') || 'admin').split(',').map(function (r) { return r.trim(); });
  var SESSION_KEY = 'studyvault-auth';
  var SB_URL = 'https://baipckgywpnwapobwtsy.supabase.co';
  var SB_KEY = 'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2';
  var TOKEN_KEY = 'sb-baipckgywpnwapobwtsy-auth-token';

  function readJSON(store) { try { return JSON.parse(store.getItem(SESSION_KEY)); } catch (e) { return null; } }

  // The retired shared password: erase any stored copy (sessions saved before 29 Sep 2026).
  [sessionStorage, localStorage].forEach(function (st) {
    var s = readJSON(st);
    if (s && s.pw) { try { st.removeItem(SESSION_KEY); } catch (e) {} }
  });

  function getSession() {
    var s = readJSON(sessionStorage);
    if (s) return s;
    var l = readJSON(localStorage);
    if (l && (l.role === 'admin' || l.role === 'teacher')) {
      try { sessionStorage.setItem(SESSION_KEY, JSON.stringify(l)); } catch (e) {}
      return l;
    }
    return null;
  }

  function saveSession(data) {
    var json = JSON.stringify(data);
    try { sessionStorage.setItem(SESSION_KEY, json); localStorage.setItem(SESSION_KEY, json); } catch (e) {}
  }

  function clearSession() {
    try { sessionStorage.removeItem(SESSION_KEY); localStorage.removeItem(SESSION_KEY); } catch (e) {}
  }

  // One Supabase client for the gate; it also keeps the stored token fresh.
  var sb = null;
  function client() {
    if (!sb && window.supabase) sb = window.supabase.createClient(SB_URL, SB_KEY);
    return sb;
  }
  function ensureSupabase() {
    return new Promise(function (resolve, reject) {
      if (window.supabase) return resolve(client());
      var s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js';
      s.onload = function () { resolve(client()); };
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  // The current access token (refreshed by supabase-js when it has expired), or null.
  function accessToken() {
    return ensureSupabase().then(function (c) {
      return c.auth.getSession().then(function (r) { return (r.data && r.data.session && r.data.session.access_token) || null; });
    }).catch(function () {
      try { return (JSON.parse(localStorage.getItem(TOKEN_KEY)) || {}).access_token || null; } catch (e) { return null; }
    });
  }

  /* Same-origin /api/ calls: add the user's token when the page did not set one, and drop the
     retired X-Admin-Password header. Installed before the page's scripts run. */
  if (window.fetch && !window.__svStaffFetch) {
    window.__svStaffFetch = true;
    var nativeFetch = window.fetch.bind(window);
    window.fetch = function (input, init) {
      var url = typeof input === 'string' ? input : (input && input.url) || '';
      var path = url.indexOf(location.origin) === 0 ? url.slice(location.origin.length) : url;
      if (typeof input !== 'string' || path.indexOf('/api/') !== 0) return nativeFetch(input, init);
      var h = new Headers((init && init.headers) || {});
      h.delete('x-admin-password');
      if (h.has('authorization')) return nativeFetch(input, Object.assign({}, init, { headers: h }));
      return accessToken().then(function (tok) {
        if (tok) h.set('Authorization', 'Bearer ' + tok);
        return nativeFetch(input, Object.assign({}, init, { headers: h }));
      });
    };
  }

  function addLogoutButton() {
    function inject() {
      // Admin pages use .admin-nav, the student shell uses .header-nav.
      var nav = document.querySelector('.header-nav') || document.querySelector('.admin-nav');
      if (!nav || nav.querySelector('.auth-logout-btn')) return;
      var btn = document.createElement('a');
      btn.href = '#';
      btn.textContent = 'Sign out';
      btn.className = 'auth-logout-btn';
      btn.style.cssText = 'color:#dc2626;font-weight:600;';
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        clearSession();
        ensureSupabase().then(function (c) { return c.auth.signOut(); }).catch(function () {})
          .then(function () { location.href = '/teacher/login'; });
      });
      nav.appendChild(btn);
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject);
    else inject();
  }

  function toSignIn() {
    clearSession();
    location.replace('/teacher/login?next=' + encodeURIComponent(location.pathname + location.search));
  }

  // Hide the page until the sign-in is confirmed, unless a cached staff session already allows it.
  var cached = getSession();
  var admitted = !!(cached && allowedRoles.indexOf(cached.role) !== -1);
  if (!admitted) {
    var hide = document.createElement('style');
    hide.id = 'auth-gate-loading';
    hide.textContent = 'body { visibility: hidden !important; }';
    document.head.appendChild(hide);
  } else {
    addLogoutButton();
  }

  function admit(data) {
    saveSession(data);
    var h = document.getElementById('auth-gate-loading');
    if (h) h.remove();
    if (!admitted) { admitted = true; addLogoutButton(); }
  }

  function refuse() {
    var h = document.getElementById('auth-gate-loading');
    if (h) h.remove();
    function show() {
      var css = document.createElement('style');
      css.textContent = 'body > *:not(.auth-gate-overlay){display:none!important}' +
        '.auth-gate-overlay{display:flex;min-height:100vh;align-items:center;justify-content:center;background:#faf8f5;font-family:Inter,system-ui,sans-serif;padding:1.5rem}' +
        '.auth-gate-box{background:#fff;border-radius:16px;padding:2.5rem 2rem;max-width:400px;width:100%;box-shadow:0 2px 12px rgba(0,0,0,.07);text-align:center;color:#2d2a26}' +
        '.auth-gate-box a{display:inline-block;margin-top:1rem;color:#6b6560}';
      document.head.appendChild(css);
      var o = document.createElement('div');
      o.className = 'auth-gate-overlay';
      o.innerHTML = '<div class="auth-gate-box"><p>This page is for StudyVault admin only.</p>' +
        '<a href="/teacher/login?signout=1">Sign in with a different account</a></div>';
      document.body.insertBefore(o, document.body.firstChild);
    }
    if (document.body) show(); else document.addEventListener('DOMContentLoaded', show);
  }

  // Confirm with Supabase: the account, its role, and whether the two-factor step is done.
  ensureSupabase().then(function (c) {
    return c.auth.getSession().then(function (r) {
      var session = r.data && r.data.session;
      if (!session) return toSignIn();
      var uid = session.user.id;
      return Promise.all([
        c.from('profiles').select('role, school_id, full_name').eq('id', uid).single(),
        c.auth.mfa.getAuthenticatorAssuranceLevel()
      ]).then(function (res) {
        var profile = res[0].data, aal = res[1].data || {};
        if (!profile) return toSignIn();
        // An account with a code set up that has not entered it this session: back for the code.
        if (aal.currentLevel !== 'aal2' && aal.nextLevel === 'aal2') return toSignIn();
        var role = profile.role === 'platform_admin'
          ? (aal.currentLevel === 'aal2' ? 'admin' : null)
          : (profile.role === 'teacher' || profile.role === 'school_admin') ? 'teacher' : null;
        if (profile.role === 'platform_admin' && !role) return toSignIn();   // admin must pass the code step
        // Admin may open every staff page; a teacher only the pages that allow teachers.
        if (role === 'admin' || (role && allowedRoles.indexOf(role) !== -1)) {
          return admit({ role: role, teacher_id: uid, school_id: profile.school_id, full_name: profile.full_name });
        }
        if (!role) return toSignIn();
        clearSession();
        refuse();
      });
    });
  }).catch(function () {
    if (!admitted) toSignIn();
  });
})();
