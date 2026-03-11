/**
 * Teacher setup — runs after auth-gate on teacher-accessible pages.
 * 1. Hides admin-only nav links for teacher role
 * 2. Shows a welcome screen if teacher hasn't set their name/subject yet
 *    — picks subject once, then chooses Editor or Images
 * 3. Shows a unit picker on return visits (before showing raw dropdowns)
 * 4. Passes ?subject=X&unit=Y so the page auto-selects dropdowns
 *
 * Include after auth-gate.js:
 *   <script src="/js/teacher-setup.js" defer></script>
 */
(function () {
  var SESSION_KEY = 'studyvault-auth';
  var TEACHER_KEY = 'studyvault-teacher';
  var SB_URL = 'https://baipckgywpnwapobwtsy.supabase.co';
  var SB_KEY = 'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2';

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

  // ---- Teacher already set up ----
  var teacher = getTeacher();
  if (teacher && teacher.name && teacher.subject) {
    var params = new URLSearchParams(window.location.search);
    // If URL already has unit param, let the page load normally
    if (params.get('unit')) return;
    // Show unit picker
    showUnitPicker(teacher);
    return;
  }

  // ---- First visit: show full-page welcome ----
  showWelcome();

  // ==================================================================

  function injectStyles() {
    if (document.getElementById('teacher-setup-styles')) return;
    var style = document.createElement('style');
    style.id = 'teacher-setup-styles';
    style.textContent = [
      '.teacher-setup-page { display: flex; min-height: 100vh; align-items: center; justify-content: center; background: #faf8f5; padding: 2rem 1.5rem; font-family: Inter, system-ui, sans-serif; }',
      '.tw-card { max-width: 480px; width: 100%; }',
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
      '.tw-back:hover { color: #2d2a26; }',
      /* Unit picker cards */
      '.tw-unit-grid { display: grid; gap: 0.65rem; }',
      '.tw-unit-card { padding: 1rem 1.15rem; border-radius: 12px; border: 1px solid #e0ddd8; background: white; transition: border-color 0.15s, box-shadow 0.15s; }',
      '.tw-unit-card:hover { border-color: #2d2a26; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }',
      '.tw-unit-name { font-weight: 600; font-size: 0.92rem; color: #2d2a26; margin: 0 0 0.5rem; }',
      '.tw-unit-accent { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 0.4rem; vertical-align: -1px; }',
      '.tw-unit-links { display: flex; gap: 0.5rem; }',
      '.tw-unit-link { font-size: 0.78rem; font-weight: 600; color: #6b6560; text-decoration: none; padding: 0.3rem 0.7rem; border-radius: 8px; border: 1px solid #e0ddd8; transition: all 0.15s; }',
      '.tw-unit-link:hover { color: #2d2a26; border-color: #2d2a26; background: #f9f7f4; }',
      '.tw-unit-link-primary { color: #2d2a26; border-color: #2d2a26; }',
      '.tw-loading { text-align: center; padding: 2rem; color: #9a938c; font-size: 0.88rem; }',
      '.tw-change { font-size: 0.78rem; color: #9a938c; text-decoration: none; margin-left: 0.5rem; transition: color 0.15s; }',
      '.tw-change:hover { color: #2d2a26; }'
    ].join('\n');
    document.head.appendChild(style);
  }

  function hidePageContent() {
    var hideStyle = document.createElement('style');
    hideStyle.id = 'teacher-setup-hide';
    hideStyle.textContent = 'body > *:not(.teacher-setup-page) { display: none !important; }';
    document.head.appendChild(hideStyle);
  }

  // ==================================================================
  //  WELCOME (first visit)
  // ==================================================================

  function showWelcome() {
    injectStyles();
    hidePageContent();

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
    page.className = 'teacher-setup-page';
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
          '<a class="tw-action-btn" id="tw-go-guides" href="/admin/editor-guide">' +
            '<span class="tw-action-title">Edit Guides</span>' +
            '<span class="tw-action-desc">Edit exam technique and revision technique guides</span>' +
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
    var guidesLink = document.getElementById('tw-go-guides');
    var imagesLink = document.getElementById('tw-go-images');

    function checkReady() {
      if (nameInput.value.trim() && subjectSelect.value) {
        actionsDiv.style.display = '';
        editorLink.href = '/admin/editor?subject=' + subjectSelect.value;
        guidesLink.href = '/admin/editor-guide?subject=' + subjectSelect.value;
        imagesLink.href = '/admin/images?subject=' + subjectSelect.value;
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
    guidesLink.addEventListener('click', saveAndGo);
    imagesLink.addEventListener('click', saveAndGo);
  }

  // ==================================================================
  //  UNIT PICKER (return visits)
  // ==================================================================

  function showUnitPicker(teacher) {
    injectStyles();
    hidePageContent();

    var subjectNames = {
      'history': 'History',
      'business': 'Business',
      'geography': 'Geography',
      'sport-science': 'Sport Science',
      'drama': 'Drama',
      'food-technology': 'Food Preparation & Nutrition',
      'religious-education': 'Religious Studies',
      'gcse-music': 'Music'
    };

    var page = document.createElement('div');
    page.className = 'teacher-setup-page';
    page.innerHTML =
      '<div class="tw-card">' +
        '<div class="tw-brand">StudyVault</div>' +
        '<h1>Welcome back, ' + escHtml(teacher.name) + '</h1>' +
        '<p>' + escHtml(subjectNames[teacher.subject] || teacher.subject) +
          '<a href="#" class="tw-change" id="tw-change-subject">Change</a></p>' +
        '<div id="tw-units"><div class="tw-loading">Loading units\u2026</div></div>' +
        '<a href="/" class="tw-back">\u2190 Back to StudyVault</a>' +
      '</div>';

    document.body.appendChild(page);

    // Change subject link
    document.getElementById('tw-change-subject').addEventListener('click', function (e) {
      e.preventDefault();
      sessionStorage.removeItem(TEACHER_KEY);
      location.reload();
    });

    // Fetch units from Supabase
    fetchUnits(teacher.subject);
  }

  function fetchUnits(subjectSlug) {
    var sb = window.supabase.createClient(SB_URL, SB_KEY);
    var container = document.getElementById('tw-units');

    sb.from('subjects').select('id').eq('slug', subjectSlug).single()
      .then(function (subjectResult) {
        if (!subjectResult.data) {
          container.innerHTML = '<div class="tw-loading">Subject not found.</div>';
          return;
        }
        return sb.from('units').select('id, slug, name, accent, sort_order')
          .eq('subject_id', subjectResult.data.id)
          .order('sort_order');
      })
      .then(function (unitsResult) {
        if (!unitsResult) return;
        var units = unitsResult.data || [];
        if (!units.length) {
          container.innerHTML = '<div class="tw-loading">No units found.</div>';
          return;
        }
        renderUnitCards(units, subjectSlug);
      })
      .catch(function () {
        container.innerHTML = '<div class="tw-loading">Failed to load units.</div>';
      });
  }

  function renderUnitCards(units, subjectSlug) {
    var container = document.getElementById('tw-units');

    // Subject-level guides link (guides are per-subject, not per-unit)
    var html =
      '<div class="tw-unit-card" style="margin-bottom: 0.75rem;">' +
        '<div class="tw-unit-name">Guides</div>' +
        '<div class="tw-unit-links">' +
          '<a href="/admin/editor-guide?subject=' + subjectSlug + '&type=exam-technique" class="tw-unit-link tw-unit-link-primary">Exam Technique</a>' +
          '<a href="/admin/editor-guide?subject=' + subjectSlug + '&type=revision-technique" class="tw-unit-link">Revision Technique</a>' +
        '</div>' +
      '</div>';

    html += '<div class="tw-unit-grid">';

    units.forEach(function (u) {
      var editorUrl = '/admin/editor?subject=' + subjectSlug + '&unit=' + u.slug;
      var imagesUrl = '/admin/images?subject=' + subjectSlug + '&unit=' + u.slug;
      var accentDot = u.accent
        ? '<span class="tw-unit-accent" style="background:' + u.accent + '"></span>'
        : '';

      html +=
        '<div class="tw-unit-card">' +
          '<div class="tw-unit-name">' + accentDot + escHtml(u.name) + '</div>' +
          '<div class="tw-unit-links">' +
            '<a href="' + editorUrl + '" class="tw-unit-link tw-unit-link-primary">Edit Lessons</a>' +
            '<a href="' + imagesUrl + '" class="tw-unit-link">Manage Images</a>' +
          '</div>' +
        '</div>';
    });

    html += '</div>';
    container.innerHTML = html;
  }

  function escHtml(str) {
    var d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }
})();
