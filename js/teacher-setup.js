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
    '.teacher-welcome-overlay { position: fixed; inset: 0; z-index: 9999; background: rgba(45,42,38,0.65); backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; padding: 1.5rem; font-family: Inter, system-ui, sans-serif; }',
    '.teacher-welcome-box { background: #faf8f5; border-radius: 20px; padding: 2.5rem 2.25rem 2rem; max-width: 380px; width: 100%; box-shadow: 0 12px 40px rgba(0,0,0,0.2); }',
    '.teacher-welcome-box h2 { font-family: "Source Serif 4", Georgia, serif; font-size: 1.4rem; font-weight: 700; margin: 0 0 0.3rem; color: #2d2a26; }',
    '.teacher-welcome-box p { font-size: 0.85rem; color: #6b6560; margin: 0 0 1.5rem; line-height: 1.5; }',
    '.teacher-welcome-form label { display: block; font-size: 0.78rem; font-weight: 600; color: #2d2a26; margin-bottom: 0.35rem; letter-spacing: 0.01em; }',
    '.teacher-welcome-input, .teacher-welcome-select { width: 100%; padding: 0.65rem 0.85rem; border: 1px solid #ddd; border-radius: 10px; font-size: 0.88rem; font-family: inherit; margin-bottom: 1.15rem; background: white; color: #2d2a26; }',
    '.teacher-welcome-input:focus, .teacher-welcome-select:focus { outline: none; border-color: #2d2a26; box-shadow: 0 0 0 2px rgba(45,42,38,0.1); }',
    '.teacher-welcome-actions { margin-top: 0.25rem; text-align: center; }',
    '.teacher-welcome-btn { width: 100%; padding: 0.75rem; background: #2d2a26; color: #faf8f5; border: none; border-radius: 10px; font-size: 0.9rem; font-weight: 600; cursor: pointer; font-family: inherit; transition: background 0.15s; }',
    '.teacher-welcome-btn:hover:not(:disabled) { background: #1a1816; }',
    '.teacher-welcome-btn:disabled { opacity: 0.35; cursor: not-allowed; }',
    '.teacher-welcome-link { display: block; margin-top: 0.85rem; font-size: 0.82rem; color: #6b6560; text-decoration: none; transition: color 0.15s; }',
    '.teacher-welcome-link:hover { color: #2d2a26; }'
  ].join('\n');
  document.head.appendChild(style);
})();
