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
    var subjectResult = await sb
      .from('subjects')
      .select('id, slug, name, exam_board, spec_code, color, image_url')
      .eq('slug', subjectSlug)
      .single();

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
      '<a href="/' + subjectSlug + '/exam-technique/index.html">Exam Technique</a>' +
      '<a href="/' + subjectSlug + '/revision-technique/index.html">Revision Techniques</a>';

    // Build HTML matching static landing page structure
    var html = '';

    // Hero
    html += '<section class="hero"><h1>' + esc(subject.name) + '</h1></section>';

    // Unit grid — uses same .unit-card structure as static pages
    html += '<div class="unit-grid">';

    units.forEach(function (unit) {
      html += '<a href="/browse/' + subjectSlug + '/' + unit.slug + '" class="unit-card" data-unit="' + esc(unit.slug) + '" data-total-lessons="' + unit.lesson_count + '" style="--card-accent: ' + unit.accent + ';">';
      html += '<div class="unit-card-image">';
      if (unit.image_url) {
        html += '<img src="' + esc(unit.image_url) + '" alt="' + esc(unit.name) + '">';
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
  }

  // ---- Render unit index page (lesson cards) ----
  async function renderUnitIndex(subjectSlug, unitSlug) {
    var unitResult = await sb
      .from('units')
      .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name)')
      .eq('slug', unitSlug)
      .eq('subjects.slug', subjectSlug)
      .single();

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
      '<a href="/' + subjectSlug + '/exam-technique/index.html">Exam Technique</a>' +
      '<a href="/' + subjectSlug + '/revision-technique/index.html">Revision Techniques</a>';

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
    html += '<div class="lesson-grid">';

    lessons.forEach(function (lesson) {
      var url = '/lesson/' + subjectSlug + '/' + unitSlug + '/' + lesson.lesson_number;
      html += '<a href="' + url + '" class="lesson-card" data-lesson="' + esc(lesson.slug) + '">';
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

    // Update visited cards from localStorage
    if (typeof updateVisitedCards === 'function') {
      updateVisitedCards();
    }
  }

  // ---- Main ----
  async function init() {
    var params = parseUrl();
    if (!params) {
      showError('Invalid URL', 'Browse URL format: /browse/{subject} or /browse/{subject}/{unit}');
      return;
    }

    var authed = await checkAuth();
    if (!authed) {
      var redirect = encodeURIComponent(window.location.pathname);
      window.location.href = '/?redirect=' + redirect;
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
