/**
 * Make the shared admin pages feel like the teacher platform.
 *
 * /teacher/review and /teacher/editor are the SAME FILES as /admin/review and
 * /admin/editor. That is fine for the tables underneath — a teacher reviewing
 * their department's lessons needs the same list Tom does — but it means a
 * teacher currently arrives at a console with Build, QA and Manage menus
 * pointing at pipeline runs, image QA and school administration. None of it is
 * theirs, and it tells them this is a machine they are expected to operate.
 *
 * So: when the signed-in person is a teacher and NOT an admin, swap the admin
 * nav for the teacher masthead and let css/teacher-shell.css restyle the page
 * onto the same tokens as /teacher/classes.
 *
 * The .admin-nav element is REUSED rather than replaced, because js/auth-gate.js
 * injects its Sign out control into exactly that class name. Replacing the node
 * would silently remove the only way to sign out — which is the bug we spent
 * this evening fixing on the classes page.
 */
(function () {
  var SESSION_KEY = 'studyvault-auth';

  function session() {
    try {
      return JSON.parse(sessionStorage.getItem(SESSION_KEY) ||
                        localStorage.getItem(SESSION_KEY) || 'null');
    } catch (e) { return null; }
  }

  function apply() {
    var s = session();
    if (!s) return;

    /* Admins keep the console. Only narrow it for people who are teachers and
       nothing more — getting this backwards would take Tom's own tools away. */
    var role = s.role || '';
    if (role !== 'teacher' && role !== 'school_admin') return;

    document.body.setAttribute('data-staff', 'teacher');

    var nav = document.querySelector('.admin-nav');
    if (!nav) return;

    /* Keep anything auth-gate has already injected (Sign out), drop the rest. */
    var keep = [];
    Array.prototype.forEach.call(nav.querySelectorAll('.auth-logout-btn'), function (el) {
      keep.push(el);
    });
    nav.innerHTML = '';

    var here = location.pathname;
    [
      ['Classes',        '/teacher/classes'],
      ['Review content', '/teacher/review'],
      ['Edit lessons',   '/teacher/editor']
    ].forEach(function (item) {
      var a = document.createElement('a');
      a.href = item[1];
      a.textContent = item[0];
      /* /teacher/review and /admin/review are the same page, so match on the
         last segment rather than the whole path. */
      if (here.split('/').pop() === item[1].split('/').pop()) {
        a.setAttribute('aria-current', 'page');
      }
      nav.appendChild(a);
    });

    keep.forEach(function (el) { nav.appendChild(el); });

    /* The brand should go somewhere a teacher wants to be. */
    var home = document.querySelector('.admin-nav-home');
    if (home) { home.href = '/teacher/classes'; home.textContent = 'My classes'; }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', apply);
  } else {
    apply();
  }

  /* auth-gate signs people in AFTER load and reloads, but on the shared-password
     path it can admit without a reload — so re-apply once shortly after, rather
     than leaving a teacher looking at the admin console until they navigate. */
  setTimeout(apply, 600);
})();
