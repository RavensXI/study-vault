/* ============================================
   StudyVault — Browse Loader
   Renders subject landing pages and unit index pages from Supabase.
   Routes: /browse/{subject}        → subject landing (shows unit cards)
           /browse/{subject}/{unit}  → unit index (shows lesson cards)
   ============================================ */

(function () {
  'use strict';

  var sb = window.supabase.createClient(
    'https://baipckgywpnwapobwtsy.supabase.co',
    'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
  );

  var loadingEl = document.getElementById('browse-loading');
  var errorEl = document.getElementById('browse-error');
  var contentEl = document.getElementById('browse-content');

  // ---- Parse URL ----
  function parseUrl() {
    var path = window.location.pathname;
    var match = path.match(/^\/browse\/([^/]+)(?:\/([^/]+))?\/?$/);
    if (!match) return null;
    return {
      subjectSlug: match[1],
      unitSlug: match[2] || null
    };
  }

  // ---- Auth check ----
  async function checkAuth() {
    var result = await sb.auth.getSession();
    if (result.data.session) return true;
    var raw = localStorage.getItem('studyvault-user');
    if (raw) return true;
    return false;
  }

  // ---- Show error ----
  function showError(title, message) {
    loadingEl.style.display = 'none';
    document.getElementById('error-title').textContent = title;
    document.getElementById('error-message').textContent = message;
    errorEl.style.display = '';
  }

  // ---- Escape HTML ----
  function esc(str) {
    var div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
  }

  // ---- Render subject landing page (unit cards) ----
  async function renderSubjectLanding(subjectSlug) {
    var schoolId = (typeof SchoolSession !== 'undefined' && SchoolSession.isActive())
      ? SchoolSession.getSchoolId()
      : null;

    var subjectQuery = sb
      .from('subjects')
      .select('id, slug, name, exam_board, spec_code, color, image_url, settings')
      .eq('slug', subjectSlug);

    if (schoolId) {
      subjectQuery = subjectQuery.eq('school_id', schoolId);
    } else {
      subjectQuery = subjectQuery.is('school_id', null);
    }

    var subjectResult = await subjectQuery.single();

    if (subjectResult.error || !subjectResult.data) {
      showError('Subject not found', 'No subject found with slug "' + subjectSlug + '"');
      return;
    }

    var subject = subjectResult.data;

    var unitsResult = await sb
      .from('units')
      .select('id, slug, name, subtitle, body_class, accent, image_url, lesson_count, sort_order')
      .eq('subject_id', subject.id)
      .order('sort_order');

    var units = unitsResult.data || [];

    document.title = subject.name + ' - StudyVault';
    document.getElementById('header-unit-label').textContent = subject.name;

    // Add nav links
    var nav = document.getElementById('header-nav');
    nav.innerHTML = '<a href="/">Home</a>' +
      '<a href="/guide/' + subjectSlug + '/exam-technique">Exam Technique</a>' +
      '<a href="/guide/' + subjectSlug + '/revision-technique">Revision Techniques</a>';

    // Apply colour theme from first unit's body class
    if (units.length > 0 && units[0].body_class) {
      document.body.classList.add(units[0].body_class);
    }

    // Build HTML matching static landing page structure
    var html = '';

    // Hero
    html += '<section class="hero"><h1>' + esc(subject.name) + '</h1></section>';

    // Quote ticker — between title and unit cards
    if (subject.settings && subject.settings.quote_ticker_html) {
      html += subject.settings.quote_ticker_html;
    }

    // Unit grid — uses same .unit-card structure as static pages
    html += '<div class="unit-grid' + (units.length === 1 ? ' single-unit' : '') + '">';

    // Get image positions from subject settings
    var imgPositions = (subject.settings && subject.settings.unit_image_positions) || {};

    units.forEach(function (unit) {
      html += '<a href="/browse/' + subjectSlug + '/' + unit.slug + '" class="unit-card" data-unit="' + esc(unit.slug) + '" data-total-lessons="' + unit.lesson_count + '" style="--card-accent: ' + unit.accent + ';">';
      html += '<div class="unit-card-image">';
      if (unit.image_url) {
        var imgStyle = imgPositions[unit.slug] ? ' style="object-position: ' + imgPositions[unit.slug] + '"' : '';
        html += '<img src="' + esc(unit.image_url) + '" alt="' + esc(unit.name) + '"' + imgStyle + '>';
      }
      html += '</div>';
      html += '<div class="unit-card-body">';
      html += '<h2>' + esc(unit.name) + '</h2>';
      if (unit.subtitle) {
        html += '<p class="unit-subtitle">' + esc(unit.subtitle) + '</p>';
      }
      html += '<span class="unit-meta">0 of ' + unit.lesson_count + ' lessons visited</span>';
      html += '<div class="progress-bar-track"><div class="progress-bar-fill"></div></div>';
      html += '</div></a>';
    });

    html += '</div>';

    loadingEl.style.display = 'none';
    contentEl.innerHTML = html;
    contentEl.style.display = '';

    // Add nav icons (pencil/lightbulb) to Exam Technique / Revision Techniques links
    if (typeof initNavIcons === 'function') initNavIcons();
    if (typeof initRevealAnimations === 'function') initRevealAnimations();
  }

  // ---- Render unit index page (lesson cards) ----
  async function renderUnitIndex(subjectSlug, unitSlug) {
    var schoolId = (typeof SchoolSession !== 'undefined' && SchoolSession.isActive())
      ? SchoolSession.getSchoolId()
      : null;

    var unitQuery = sb
      .from('units')
      .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, school_id)')
      .eq('slug', unitSlug)
      .eq('subjects.slug', subjectSlug);

    if (schoolId) {
      unitQuery = unitQuery.eq('subjects.school_id', schoolId);
    } else {
      unitQuery = unitQuery.is('subjects.school_id', null);
    }

    var unitResult = await unitQuery.single();

    if (unitResult.error || !unitResult.data) {
      showError('Unit not found', 'No unit found.');
      return;
    }

    var unit = unitResult.data;
    var subject = unit.subjects;

    var lessonsResult = await sb
      .from('lessons')
      .select('id, lesson_number, slug, title, description, status')
      .eq('unit_id', unit.id)
      .eq('status', 'live')
      .order('lesson_number');

    var lessons = lessonsResult.data || [];

    document.title = unit.name + ' - StudyVault';
    document.body.classList.add(unit.body_class);
    document.body.dataset.unit = unit.slug;
    document.getElementById('header-unit-label').textContent = unit.name;

    // Nav links
    var nav = document.getElementById('header-nav');
    nav.innerHTML = '<a href="/">Home</a>' +
      '<a href="/browse/' + subjectSlug + '">Subject Home</a>' +
      '<a href="/guide/' + subjectSlug + '/exam-technique">Exam Technique</a>' +
      '<a href="/guide/' + subjectSlug + '/revision-technique">Revision Techniques</a>';

    var html = '';

    // Unit page header — coloured strip with title and description
    html += '<div class="unit-page-header">';
    html += '<div class="unit-page-header-inner">';
    html += '<h1>' + esc(unit.name) + '</h1>';
    if (unit.subtitle) {
      html += '<p>' + esc(unit.subtitle) + '</p>';
    }
    html += '</div></div>';

    // Progress bar
    html += '<div class="unit-progress">';
    html += '<div class="unit-progress-label">0 of ' + unit.lesson_count + ' lessons visited</div>';
    html += '<div class="progress-bar-track"><div class="progress-bar-fill"></div></div>';
    html += '</div>';

    // Lesson grid
    html += '<div class="lesson-grid sv-stagger">';

    lessons.forEach(function (lesson) {
      var url = '/lesson/' + subjectSlug + '/' + unitSlug + '/' + lesson.lesson_number;
      html += '<a href="' + url + '" class="lesson-card sv-reveal" data-lesson="' + esc(lesson.slug) + '">';
      html += '<span class="lesson-card-number">Lesson ' + lesson.lesson_number + '</span>';
      html += '<h3>' + esc(lesson.title) + '</h3>';
      if (lesson.description) {
        html += '<p>' + esc(lesson.description) + '</p>';
      }
      html += '</a>';
    });

    html += '</div>';

    // Back link — wrapped in container to match static page padding
    html += '<div style="max-width: var(--page-max); margin: 0 auto; padding: 0 1.5rem 3rem;">';
    html += '<a href="/browse/' + subjectSlug + '" class="back-link">&larr; Back to ' + esc(subject.name) + '</a>';
    html += '</div>';

    loadingEl.style.display = 'none';
    contentEl.innerHTML = html;
    contentEl.style.display = '';

    // Add nav icons, update visited cards, trigger reveal animations
    if (typeof initNavIcons === 'function') initNavIcons();
    if (typeof updateVisitedCards === 'function') updateVisitedCards();
    if (typeof initRevealAnimations === 'function') initRevealAnimations();
  }

  // ---- Main ----
  async function init() {
    var params = parseUrl();
    if (!params) {
      showError('Invalid URL', 'Browse URL format: /browse/{subject} or /browse/{subject}/{unit}');
      return;
    }

    try {
      if (params.unitSlug) {
        await renderUnitIndex(params.subjectSlug, params.unitSlug);
      } else {
        await renderSubjectLanding(params.subjectSlug);
      }
    } catch (err) {
      console.error('Browse loader error:', err);
      showError('Something went wrong', 'Could not load the page. Please try again.');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
