/**
 * Auth gate for protected pages.
 *
 * Shared password mode (default):
 *   <script src="/js/auth-gate.js" data-role="admin"></script>
 *   <script src="/js/auth-gate.js" data-role="admin,teacher"></script>
 *
 * Teacher email+password mode (Supabase Auth):
 *   <script src="/js/auth-gate.js" data-role="teacher" data-auth="teacher"></script>
 *
 * When data-auth="teacher" is set, renders an email + password form that
 * authenticates via Supabase Auth, verifies the user has a teacher or
 * platform_admin role in the profiles table, stores session info, and
 * reloads the page. Falls back to the shared password gate when data-auth
 * is not set.
 */
(function () {
  var script = document.currentScript;
  var allowedRoles = (script.getAttribute('data-role') || 'admin').split(',').map(function (r) { return r.trim(); });
  var authMode = script.getAttribute('data-auth') || '';
  var SESSION_KEY = 'studyvault-auth';

  function getSession() {
    try {
      var s = sessionStorage.getItem(SESSION_KEY);
      if (s) return JSON.parse(s);
      // Also check localStorage (persists across tabs for staff)
      var l = localStorage.getItem(SESSION_KEY);
      if (l) {
        var parsed = JSON.parse(l);
        // Only restore staff sessions, not student ones
        if (parsed.role === 'admin' || parsed.role === 'teacher') {
          sessionStorage.setItem(SESSION_KEY, l);
          return parsed;
        }
      }
      return null;
    } catch (e) { return null; }
  }

  function saveSession(data) {
    var json = JSON.stringify(data);
    sessionStorage.setItem(SESSION_KEY, json);
    // Staff sessions also persist to localStorage for cross-tab access
    if (data.role === 'admin' || data.role === 'teacher') {
      localStorage.setItem(SESSION_KEY, json);
    }
  }

  var isTeacherAuth = authMode === 'teacher';

  function addLogoutButton() {
    function inject() {
      // Admin pages use .admin-nav, the student shell uses .header-nav. Only the
      // latter was checked, so no admin page has ever shown a Sign out — a stale
      // staff session in localStorage auto-admits forever with no way to clear it.
      var nav = document.querySelector('.header-nav') || document.querySelector('.admin-nav');
      if (!nav) return;
      if (nav.querySelector('.auth-logout-btn')) return;
    var btn = document.createElement('a');
    btn.href = '#';
    btn.textContent = 'Sign out';
    btn.className = 'auth-logout-btn';
    btn.style.cssText = 'color:#dc2626;font-weight:600;';
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      sessionStorage.removeItem(SESSION_KEY);
      localStorage.removeItem(SESSION_KEY);
      // Clear Supabase Auth session too
      if (window.supabase) {
        var sb = window.supabase.createClient(
          'https://baipckgywpnwapobwtsy.supabase.co',
          'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
        );
        sb.auth.signOut().finally(function () { location.reload(); });
      } else {
        location.reload();
      }
    });
    nav.appendChild(btn);
    }
    // Run now if DOM ready, otherwise wait
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', inject);
    } else {
      inject();
    }
  }

  var session = getSession();
  if (session && allowedRoles.indexOf(session.role) !== -1) {
    addLogoutButton();
    return; // Valid session — page renders normally
  }

  // For teacher auth mode, check for existing Supabase session before showing gate
  if (isTeacherAuth && window.supabase) {
    // Check localStorage for Supabase token synchronously — if present, hide page
    // and verify async. This prevents flashing the login form unnecessarily.
    var sbKey = 'sb-baipckgywpnwapobwtsy-auth-token';
    var sbRaw = localStorage.getItem(sbKey);
    if (sbRaw) {
      // There's a Supabase token — hide page while we verify
      var hideStyle = document.createElement('style');
      hideStyle.id = 'auth-gate-loading';
      hideStyle.textContent = 'body { visibility: hidden !important; }';
      document.head.appendChild(hideStyle);

      var sb = window.supabase.createClient(
        'https://baipckgywpnwapobwtsy.supabase.co',
        'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
      );
      sb.auth.getSession().then(function (result) {
        if (result.data.session) {
          var userId = result.data.session.user.id;
          return sb.from('profiles').select('role, school_id, full_name').eq('id', userId).single()
            .then(function (profileResult) {
              var profile = profileResult.data;
              if (profile && allowedRoles.indexOf(profile.role) !== -1) {
                saveSession({
                  role: profile.role,
                  teacher_id: userId,
                  school_id: profile.school_id,
                  full_name: profile.full_name
                });
                // Remove hide style and admit
                var ls = document.getElementById('auth-gate-loading');
                if (ls) ls.remove();
                var cs = document.getElementById('auth-gate-css');
                if (cs) cs.remove();
                var ov = document.querySelector('.auth-gate-overlay');
                if (ov) ov.remove();
                addLogoutButton();
                return; // Admitted
              }
            });
        }
      }).catch(function () {}).finally(function () {
        // If we get here without being admitted, show the gate
        var ls = document.getElementById('auth-gate-loading');
        if (ls) ls.remove();
      });
    }
  }

  // ---- Not authenticated — hide page and show login ----

  // Inject CSS immediately (before body parses)
  var gateCSS = document.createElement('style');
  gateCSS.id = 'auth-gate-css';
  gateCSS.textContent = [
    'body > *:not(.auth-gate-overlay) { display: none !important; }',
    '.auth-gate-overlay { display: flex !important; min-height: 100vh; align-items: center; justify-content: center; background: #faf8f5; font-family: Inter, system-ui, sans-serif; padding: 1.5rem; }',
    '.auth-gate-box { background: white; border-radius: 16px; padding: 2.5rem 2rem; max-width: 400px; width: 100%; box-shadow: 0 2px 12px rgba(0,0,0,0.07); text-align: center; }',
    '.auth-gate-brand { font-family: "Source Serif 4", Georgia, serif; font-size: 1.5rem; font-weight: 700; color: #2d2a26; margin-bottom: 0.25rem; }',
    '.auth-gate-brand svg { width: 1em; height: 1em; vertical-align: -0.1em; margin-left: 0.1em; }',
    '.auth-gate-title { font-size: 0.95rem; color: #6b6560; font-weight: 500; margin-bottom: 1.5rem; }',
    '.auth-gate-input { width: 100%; padding: 0.65rem 0.85rem; border: 1px solid #ddd; border-radius: 10px; font-size: 0.9rem; font-family: inherit; text-align: center; margin-bottom: 0.75rem; }',
    '.auth-gate-input:focus { outline: none; border-color: #7c3aed; box-shadow: 0 0 0 2px rgba(124,58,237,0.15); }',
    '.auth-gate-label { display: block; font-size: 0.78rem; font-weight: 600; color: #6b6560; text-align: left; margin-bottom: 0.3rem; }',
    '.auth-gate-group { margin-bottom: 0.75rem; }',
    '.auth-gate-group .auth-gate-input { margin-bottom: 0; text-align: left; }',
    '.auth-gate-error { color: #dc2626; font-size: 0.82rem; margin-bottom: 0.5rem; }',
    '.auth-gate-btn { width: 100%; padding: 0.65rem; background: #2d2a26; color: white; border: none; border-radius: 10px; font-size: 0.9rem; font-weight: 600; cursor: pointer; font-family: inherit; }',
    '.auth-gate-btn:hover { background: #1a1816; }',
    '.auth-gate-btn:disabled { opacity: 0.6; cursor: wait; }',
    '.auth-gate-back { display: inline-block; margin-top: 1.25rem; font-size: 0.82rem; color: #6b6560; text-decoration: none; }',
    '.auth-gate-back:hover { color: #2d2a26; }',
    '.auth-gate-login-link { display: block; margin-top: 1rem; font-size: 0.82rem; color: #7c3aed; text-decoration: none; font-weight: 600; }',
    '.auth-gate-login-link:hover { text-decoration: underline; }'
  ].join('\n');
  document.head.appendChild(gateCSS);

  var lockSVG = '<svg class="logo-lock" viewBox="0 0 2048 2048" aria-hidden="true" style="width:1em;height:1em;vertical-align:-0.1em;margin-left:0.1em"><path fill="currentColor" d="M 1006.55 384.5 C 1012.26 384.032 1017.96 384.019 1023.69 384.03 C 1126.34 383.508 1224.86 424.385 1296.99 497.419 C 1360.21 560.738 1398.86 644.469 1406.04 733.658 C 1408.66 765.139 1407.27 812.813 1407.19 845.206 C 1408.84 845.067 1410.49 844.96 1412.14 844.887 C 1429.72 844.275 1447.74 845.081 1465.32 844.677 C 1495.06 843.994 1535.25 840.392 1535.47 882.388 L 1535.36 1317.69 L 1535.32 1438.19 C 1535.26 1507.75 1538.75 1557.74 1484.85 1611.82 C 1460.86 1635.66 1430.61 1652.23 1397.59 1659.62 C 1375.13 1664.65 1350.12 1663.97 1327.09 1663.93 L 1262.44 1663.83 L 1039.75 1663.73 L 791.843 1663.77 C 753.977 1663.77 680.267 1666.52 646.687 1658.7 C 616.228 1651.35 588.323 1635.91 565.929 1614 C 532.163 1581.54 512.105 1536.9 512.157 1490.19 C 512.202 1449.42 512.422 1408.59 512.416 1367.82 L 512.46 1090.95 L 512.437 949.482 C 512.426 925.408 512.016 901.145 513.113 877.152 C 513.68 864.772 526.116 849.163 538.208 846.652 C 551.022 843.991 567.128 844.956 580.366 844.959 C 600.487 844.856 620.61 844.943 640.73 845.219 C 639.551 827.347 640.432 805.755 640.372 787.686 C 640.3 766.215 640.741 742.607 643.073 721.312 C 651.702 644.63 683.654 572.444 734.615 514.5 C 806.373 432.129 899.065 391.821 1006.55 384.5 z M 716.467 845.223 C 818.381 844.143 921.774 845.464 1023.95 845.099 L 1331.64 844.834 L 1331.54 843.821 C 1330.34 831.289 1331.21 811.921 1331.49 799.241 C 1331.8 783.652 1331.59 768.058 1330.86 752.483 C 1326.9 666.541 1286.96 586.231 1220.82 531.214 C 1176.33 494.282 1122.33 470.636 1065.02 462.987 C 1056.45 461.791 1035.74 459.773 1026.64 460.477 C 938.331 462.331 863.078 491.197 801.283 555.598 C 753.658 605.045 724.17 669.155 717.618 737.494 C 714.147 772.586 716.753 809.897 716.467 845.223 z"/><path class="logo-lock-keyhole" d="M 1010.92 1075.34 C 1032.39 1072.69 1058.68 1077.88 1078.25 1086.82 C 1108.74 1101.11 1132.38 1126.83 1144.05 1158.4 C 1155.23 1188.63 1153.67 1227.84 1139.51 1256.66 C 1122.21 1291.9 1098.3 1312.15 1062.02 1325.22 C 1061.91 1344.15 1065.34 1395.94 1058.79 1410.84 C 1054.1 1421.5 1045.86 1427.24 1035.49 1431.54 C 1022.09 1434.04 1009.85 1433.55 998.968 1424.13 C 993.361 1419.21 989.346 1412.74 987.435 1405.53 C 984.458 1394.29 986.554 1342.42 985.404 1325.3 C 972.138 1319.93 962.284 1316.02 950.395 1307.56 C 923.012 1288.07 903.201 1257.64 897.872 1224.34 C 892.21 1190.1 900.488 1155.02 920.859 1126.93 C 943.784 1095.82 973.572 1081.06 1010.92 1075.34 z"/></svg>';

  document.addEventListener('DOMContentLoaded', function () {
    var overlay = document.createElement('div');
    overlay.className = 'auth-gate-overlay';

    if (isTeacherAuth) {
      // ---- Teacher email + password mode (Supabase Auth) ----
      overlay.innerHTML =
        '<div class="auth-gate-box">' +
          '<div class="auth-gate-brand">StudyVault' + lockSVG + '</div>' +
          '<div class="auth-gate-title">Sign in with your teacher account</div>' +
          '<form class="auth-gate-form">' +
            '<div class="auth-gate-group">' +
              '<label class="auth-gate-label" for="ag-email">Email address</label>' +
              '<input type="email" id="ag-email" class="auth-gate-input" placeholder="you@school.ac.uk" autocomplete="email" autofocus required>' +
            '</div>' +
            '<div class="auth-gate-group">' +
              '<label class="auth-gate-label" for="ag-password">Password</label>' +
              '<input type="password" id="ag-password" class="auth-gate-input" placeholder="Your password" autocomplete="current-password" required>' +
            '</div>' +
            '<div class="auth-gate-error" style="display:none"></div>' +
            '<button type="submit" class="auth-gate-btn">Sign in</button>' +
          '</form>' +
          '<a href="/teacher/login" class="auth-gate-login-link">Use the full sign-in page</a>' +
          '<a href="/" class="auth-gate-back">\u2190 Back to StudyVault</a>' +
        '</div>';
      document.body.insertBefore(overlay, document.body.firstChild);

      var form = overlay.querySelector('form');
      var emailInput = overlay.querySelector('#ag-email');
      var passInput = overlay.querySelector('#ag-password');
      var error = overlay.querySelector('.auth-gate-error');
      var btn = overlay.querySelector('button');

      // Load Supabase JS if not already present
      function ensureSupabase(cb) {
        if (window.supabase) { cb(); return; }
        var s = document.createElement('script');
        s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js';
        s.onload = cb;
        s.onerror = function () {
          error.textContent = 'Failed to load authentication library.';
          error.style.display = '';
        };
        document.head.appendChild(s);
      }

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        btn.disabled = true;
        btn.textContent = 'Signing in\u2026';
        error.style.display = 'none';

        var email = emailInput.value.trim();
        var password = passInput.value;

        ensureSupabase(function () {
          var SB_URL = 'https://baipckgywpnwapobwtsy.supabase.co';
          var SB_KEY = 'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2';
          var sb = window.supabase.createClient(SB_URL, SB_KEY);

          sb.auth.signInWithPassword({ email: email, password: password })
            .then(function (result) {
              if (result.error) {
                error.textContent = result.error.message;
                error.style.display = '';
                btn.disabled = false;
                btn.textContent = 'Sign in';
                passInput.select();
                return;
              }

              // Verify teacher/admin role
              sb.from('profiles').select('role, school_id, full_name').eq('id', result.data.user.id).single()
                .then(function (profileResult) {
                  var profile = profileResult.data;
                  if (!profile || (profile.role !== 'teacher' && profile.role !== 'platform_admin')) {
                    error.textContent = 'This account is not a teacher account.';
                    error.style.display = '';
                    sb.auth.signOut();
                    btn.disabled = false;
                    btn.textContent = 'Sign in';
                    return;
                  }

                  if (allowedRoles.indexOf(profile.role) === -1) {
                    error.textContent = 'You don\u2019t have access to this page.';
                    error.style.display = '';
                    btn.disabled = false;
                    btn.textContent = 'Sign in';
                    return;
                  }

                  // Store session
                  saveSession({
                    role: profile.role,
                    teacher_id: result.data.user.id,
                    school_id: profile.school_id,
                    full_name: profile.full_name
                  });
                  location.reload();
                });
            })
            .catch(function () {
              error.textContent = 'Connection error. Try again.';
              error.style.display = '';
              btn.disabled = false;
              btn.textContent = 'Sign in';
            });
        });
      });

    } else {
      // ---- Original shared password mode ----
      overlay.innerHTML =
        '<div class="auth-gate-box">' +
          '<div class="auth-gate-brand">StudyVault' + lockSVG + '</div>' +
          '<div class="auth-gate-title">Enter password to continue</div>' +
          '<form class="auth-gate-form">' +
            '<input type="password" class="auth-gate-input" placeholder="Password" autofocus required>' +
            '<div class="auth-gate-error" style="display:none"></div>' +
            '<button type="submit" class="auth-gate-btn">Sign in</button>' +
          '</form>' +
          '<a href="/" class="auth-gate-back">\u2190 Back to StudyVault</a>' +
        '</div>';
      document.body.insertBefore(overlay, document.body.firstChild);

      var form = overlay.querySelector('form');
      var input = overlay.querySelector('input');
      var error = overlay.querySelector('.auth-gate-error');
      var btn = overlay.querySelector('button');

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        btn.disabled = true;
        btn.textContent = 'Signing in\u2026';
        error.style.display = 'none';

        fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ password: input.value })
        })
        .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); })
        .then(function (res) {
          if (res.ok && res.data.role) {
            if (allowedRoles.indexOf(res.data.role) !== -1) {
              var sessionData = { role: res.data.role, pw: input.value };
              if (res.data.school_id) sessionData.school_id = res.data.school_id;
              saveSession(sessionData);
              location.reload();
            } else {
              error.textContent = 'You don\u2019t have access to this page.';
              error.style.display = '';
              btn.disabled = false;
              btn.textContent = 'Sign in';
            }
          } else {
            error.textContent = res.data.error || 'Incorrect password';
            error.style.display = '';
            btn.disabled = false;
            btn.textContent = 'Sign in';
            input.select();
          }
        })
        .catch(function () {
          error.textContent = 'Connection error. Try again.';
          error.style.display = '';
          btn.disabled = false;
          btn.textContent = 'Sign in';
        });
      });
    }
  });
})();
