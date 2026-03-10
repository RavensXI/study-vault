/**
 * Teacher setup — runs after auth-gate on teacher-accessible pages.
 * 1. Hides admin-only nav links for teacher role
 * 2. Shows a welcome modal if teacher hasn't set their name/subject yet
 *
 * Include after auth-gate.js:
 *   <script src="/js/teacher-setup.js" defer></script>
 */
(function () {
  var SESSION_KEY = 'studyvault-auth';
  var TEACHER_KEY = 'studyvault-teacher';

  function getAuth() {
    try { return JSON.parse(sessionStorage.getItem(SESSION_KEY)); } catch (e) { return null; }
  }

  function getTeacher() {
    try { return JSON.parse(sessionStorage.getItem(TEACHER_KEY)); } catch (e) { return null; }
  }

  var auth = getAuth();
  if (!auth) return;

  // ---- Hide admin-only nav links for teachers ----
  if (auth.role === 'teacher') {
    document.querySelectorAll('[data-admin-only]').forEach(function (el) {
      el.style.display = 'none';
    });
  }

  // ---- Admin users skip the welcome modal ----
  if (auth.role === 'admin') return;

  // ---- Teacher welcome modal ----
  var teacher = getTeacher();
  if (teacher && teacher.name && teacher.subject) {
    // Already set up — auto-select subject if on editor page
    applyTeacherSubject(teacher.subject);
    return;
  }

  // Subjects list
  var subjects = [
    { slug: 'history', name: 'History' },
    { slug: 'business', name: 'Business' },
    { slug: 'geography', name: 'Geography' },
    { slug: 'sport-science', name: 'Sport Science' },
    { slug: 'drama', name: 'Drama' },
    { slug: 'food-technology', name: 'Food Preparation & Nutrition' },
    { slug: 'religious-education', name: 'Religious Studies' },
    { slug: 'gcse-music', name: 'Music' }
  ];

  // Build modal
  var overlay = document.createElement('div');
  overlay.className = 'teacher-welcome-overlay';

  var optionsHtml = '<option value="">Select your subject...</option>';
  subjects.forEach(function (s) {
    optionsHtml += '<option value="' + s.slug + '">' + s.name + '</option>';
  });

  overlay.innerHTML =
    '<div class="teacher-welcome-box">' +
      '<h2>Welcome to StudyVault</h2>' +
      '<p>Let\u2019s get you set up. This only takes a moment.</p>' +
      '<form class="teacher-welcome-form">' +
        '<label>Your name</label>' +
        '<input type="text" class="teacher-welcome-input" placeholder="e.g. Mr Smith" required>' +
        '<label>Which subject do you teach?</label>' +
        '<select class="teacher-welcome-select" required>' + optionsHtml + '</select>' +
        '<div class="teacher-welcome-actions">' +
          '<button type="submit" class="teacher-welcome-btn" disabled>Continue to Editor</button>' +
          '<a href="/admin/images" class="teacher-welcome-link" style="display:none">or go to Image QA \u2192</a>' +
        '</div>' +
      '</form>' +
    '</div>';

  document.body.appendChild(overlay);

  var form = overlay.querySelector('form');
  var nameInput = overlay.querySelector('input');
  var subjectSelect = overlay.querySelector('select');
  var btn = overlay.querySelector('button');
  var altLink = overlay.querySelector('.teacher-welcome-link');

  function updateBtn() {
    var valid = nameInput.value.trim() && subjectSelect.value;
    btn.disabled = !valid;
    if (valid) {
      // Show the right button text based on current page
      var onImages = location.pathname.indexOf('/images') !== -1;
      btn.textContent = onImages ? 'Continue to Image QA' : 'Continue to Editor';
      altLink.style.display = '';
      altLink.href = onImages
        ? '/admin/editor?subject=' + subjectSelect.value
        : '/admin/images';
      altLink.textContent = onImages
        ? 'or go to Editor \u2192'
        : 'or go to Image QA \u2192';
    }
  }

  nameInput.addEventListener('input', updateBtn);
  subjectSelect.addEventListener('change', updateBtn);

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var data = { name: nameInput.value.trim(), subject: subjectSelect.value };
    sessionStorage.setItem(TEACHER_KEY, JSON.stringify(data));
    overlay.remove();
    applyTeacherSubject(data.subject);
  });

  function applyTeacherSubject(slug) {
    // If on editor page, set the subject dropdown
    var pickSubject = document.getElementById('pick-subject');
    if (pickSubject && !new URLSearchParams(window.location.search).get('subject')) {
      // Wait for subjects to load, then auto-select
      var observer = new MutationObserver(function () {
        if (pickSubject.options.length > 1) {
          observer.disconnect();
          pickSubject.value = slug;
          pickSubject.dispatchEvent(new Event('change'));
        }
      });
      observer.observe(pickSubject, { childList: true });
    }
  }

  // ---- Inline styles for the modal ----
  var style = document.createElement('style');
  style.textContent = [
    '.teacher-welcome-overlay { position: fixed; inset: 0; z-index: 9999; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; padding: 1.5rem; font-family: Inter, system-ui, sans-serif; }',
    '.teacher-welcome-box { background: white; border-radius: 16px; padding: 2rem 2rem 1.75rem; max-width: 400px; width: 100%; box-shadow: 0 8px 32px rgba(0,0,0,0.15); }',
    '.teacher-welcome-box h2 { font-family: "Source Serif 4", Georgia, serif; font-size: 1.3rem; margin: 0 0 0.35rem; color: #2d2a26; }',
    '.teacher-welcome-box p { font-size: 0.88rem; color: #6b6560; margin: 0 0 1.25rem; }',
    '.teacher-welcome-form label { display: block; font-size: 0.82rem; font-weight: 600; color: #2d2a26; margin-bottom: 0.3rem; }',
    '.teacher-welcome-input, .teacher-welcome-select { width: 100%; padding: 0.6rem 0.8rem; border: 1px solid #ddd; border-radius: 10px; font-size: 0.88rem; font-family: inherit; margin-bottom: 1rem; background: white; }',
    '.teacher-welcome-input:focus, .teacher-welcome-select:focus { outline: none; border-color: #7c3aed; box-shadow: 0 0 0 2px rgba(124,58,237,0.15); }',
    '.teacher-welcome-actions { text-align: center; }',
    '.teacher-welcome-btn { width: 100%; padding: 0.7rem; background: #7c3aed; color: white; border: none; border-radius: 10px; font-size: 0.9rem; font-weight: 600; cursor: pointer; font-family: inherit; }',
    '.teacher-welcome-btn:hover:not(:disabled) { background: #6d28d9; }',
    '.teacher-welcome-btn:disabled { opacity: 0.5; cursor: not-allowed; }',
    '.teacher-welcome-link { display: block; margin-top: 0.75rem; font-size: 0.82rem; color: #6b6560; text-decoration: none; }',
    '.teacher-welcome-link:hover { color: #7c3aed; }'
  ].join('\n');
  document.head.appendChild(style);
})();
