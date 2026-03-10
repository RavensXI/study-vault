/**
 * Teacher setup — runs after auth-gate on teacher-accessible pages.
 * 1. Hides admin-only nav links for teacher role
 * 2. Shows a welcome screen if teacher hasn't set their name/subject yet
 *    — picks subject once, then chooses Editor or Images
 * 3. Auto-selects their subject on the editor page
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

  // ---- Admin users skip the welcome ----
  if (auth.role === 'admin') return;

  // ---- Teacher already set up — just auto-select subject ----
  var teacher = getTeacher();
  if (teacher && teacher.name && teacher.subject) {
    applyTeacherSubject(teacher.subject);
    return;
  }

  // ---- First visit: show full-page welcome (not a modal) ----

  // Hide ALL page content
  var hideStyle = document.createElement('style');
  hideStyle.id = 'teacher-welcome-hide';
  hideStyle.textContent = 'body > *:not(.teacher-welcome-page) { display: none !important; }';
  document.head.appendChild(hideStyle);

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

  var optionsHtml = '<option value="">Select your subject...</option>';
  subjects.forEach(function (s) {
    optionsHtml += '<option value="' + s.slug + '">' + s.name + '</option>';
  });

  var page = document.createElement('div');
  page.className = 'teacher-welcome-page';
  page.innerHTML =
    '<div class="tw-card">' +
      '<div class="tw-brand">StudyVault</div>' +
      '<h1>Teacher Tools</h1>' +
      '<p>Set up your account to get started.</p>' +
      '<div class="tw-form">' +
        '<label for="tw-name">Your name</label>' +
        '<input type="text" id="tw-name" placeholder="e.g. Mr Smith">' +
        '<label for="tw-subject">Your subject</label>' +
        '<select id="tw-subject">' + optionsHtml + '</select>' +
      '</div>' +
      '<div class="tw-actions" id="tw-actions" style="display:none">' +
        '<p class="tw-choose">What would you like to do?</p>' +
        '<a class="tw-action-btn tw-action-primary" id="tw-go-editor" href="/admin/editor">' +
          '<span class="tw-action-title">Edit Lessons</span>' +
          '<span class="tw-action-desc">Review and edit lesson content for your subject</span>' +
        '</a>' +
        '<a class="tw-action-btn" id="tw-go-images" href="/admin/images">' +
          '<span class="tw-action-title">Manage Images</span>' +
          '<span class="tw-action-desc">Check hero images and diagram positioning</span>' +
        '</a>' +
      '</div>' +
      '<a href="/" class="tw-back">\u2190 Back to StudyVault</a>' +
    '</div>';

  document.body.appendChild(page);

  var nameInput = document.getElementById('tw-name');
  var subjectSelect = document.getElementById('tw-subject');
  var actionsDiv = document.getElementById('tw-actions');
  var editorLink = document.getElementById('tw-go-editor');
  var imagesLink = document.getElementById('tw-go-images');

  function checkReady() {
    if (nameInput.value.trim() && subjectSelect.value) {
      actionsDiv.style.display = '';
      editorLink.href = '/admin/editor?subject=' + subjectSelect.value;
    } else {
      actionsDiv.style.display = 'none';
    }
  }

  nameInput.addEventListener('input', checkReady);
  subjectSelect.addEventListener('change', checkReady);

  function saveAndGo(e) {
    var data = { name: nameInput.value.trim(), subject: subjectSelect.value };
    if (!data.name || !data.subject) {
      e.preventDefault();
      return;
    }
    sessionStorage.setItem(TEACHER_KEY, JSON.stringify(data));
    // Navigation happens via the <a> href
  }

  editorLink.addEventListener('click', saveAndGo);
  imagesLink.addEventListener('click', saveAndGo);

  function applyTeacherSubject(slug) {
    var pickSubject = document.getElementById('pick-subject');
    if (pickSubject && !new URLSearchParams(window.location.search).get('subject')) {
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

  // ---- Inline styles ----
  var style = document.createElement('style');
  style.textContent = [
    '.teacher-welcome-page { display: flex; min-height: 100vh; align-items: center; justify-content: center; background: #faf8f5; padding: 2rem 1.5rem; font-family: Inter, system-ui, sans-serif; }',
    '.tw-card { max-width: 420px; width: 100%; }',
    '.tw-brand { font-family: "Source Serif 4", Georgia, serif; font-size: 1rem; font-weight: 700; color: #9a938c; margin-bottom: 1.5rem; letter-spacing: -0.01em; }',
    '.tw-card h1 { font-family: "Source Serif 4", Georgia, serif; font-size: 1.8rem; font-weight: 700; color: #2d2a26; margin: 0 0 0.4rem; }',
    '.tw-card > p { font-size: 0.92rem; color: #6b6560; margin: 0 0 2rem; line-height: 1.5; }',
    '.tw-form label { display: block; font-size: 0.78rem; font-weight: 600; color: #2d2a26; margin-bottom: 0.35rem; }',
    '.tw-form input, .tw-form select { width: 100%; padding: 0.7rem 0.9rem; border: 1px solid #e0ddd8; border-radius: 10px; font-size: 0.9rem; font-family: inherit; background: white; color: #2d2a26; margin-bottom: 1.1rem; }',
    '.tw-form input:focus, .tw-form select:focus { outline: none; border-color: #2d2a26; box-shadow: 0 0 0 2px rgba(45,42,38,0.08); }',
    '.tw-form input::placeholder { color: #b5b0aa; }',
    '.tw-choose { font-size: 0.82rem; font-weight: 600; color: #2d2a26; margin: 0.5rem 0 0.75rem; }',
    '.tw-action-btn { display: block; padding: 1rem 1.15rem; border-radius: 12px; text-decoration: none; color: #2d2a26; border: 1px solid #e0ddd8; background: white; margin-bottom: 0.65rem; transition: border-color 0.15s, box-shadow 0.15s; }',
    '.tw-action-btn:hover { border-color: #2d2a26; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }',
    '.tw-action-primary { border-color: #2d2a26; }',
    '.tw-action-title { display: block; font-weight: 600; font-size: 0.92rem; margin-bottom: 0.15rem; }',
    '.tw-action-desc { display: block; font-size: 0.78rem; color: #6b6560; }',
    '.tw-back { display: inline-block; margin-top: 1.5rem; font-size: 0.82rem; color: #9a938c; text-decoration: none; transition: color 0.15s; }',
    '.tw-back:hover { color: #2d2a26; }'
  ].join('\n');
  document.head.appendChild(style);
})();
