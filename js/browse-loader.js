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
    // /browse/{subject}/{unit?}
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
    // Fetch subject with its units
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

    var html = '<div class="subject-landing" style="max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem;">';
    html += '<h1 style="font-family: \'Source Serif 4\', serif; margin-bottom: 0.5rem;">' + esc(subject.name) + '</h1>';
    html += '<p style="color: var(--text-muted); margin-bottom: 2rem;">' + esc(subject.exam_board + (subject.spec_code ? ' ' + subject.spec_code : '')) + '</p>';

    html += '<div class="unit-cards" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem;">';

    units.forEach(function (unit) {
      html += '<a href="/browse/' + subjectSlug + '/' + unit.slug + '" class="unit-card" data-unit="' + esc(unit.slug) + '" ' +
        'style="display: block; border-radius: 16px; overflow: hidden; background: white; box-shadow: 0 2px 12px rgba(0,0,0,0.08); text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s;">';

      if (unit.image_url) {
        html += '<div style="height: 160px; overflow: hidden;"><img src="' + esc(unit.image_url) + '" alt="" style="width: 100%; height: 100%; object-fit: cover;"></div>';
      } else {
        html += '<div style="height: 160px; background: ' + unit.accent + '; opacity: 0.15;"></div>';
      }

      html += '<div style="padding: 1.25rem;">';
      html += '<h3 style="font-family: \'Source Serif 4\', serif; font-size: 1.15rem; margin: 0 0 0.25rem;">' + esc(unit.name) + '</h3>';
      if (unit.subtitle) {
        html += '<p style="color: var(--text-muted); font-size: 0.875rem; margin: 0 0 0.5rem;">' + esc(unit.subtitle) + '</p>';
      }
      html += '<span style="font-size: 0.82rem; color: ' + unit.accent + '; font-weight: 600;">' + unit.lesson_count + ' lessons</span>';

      // Progress bar placeholder
      html += '<div class="unit-progress" style="margin-top: 0.75rem; height: 4px; background: #eee; border-radius: 2px;">';
      html += '<div class="unit-progress-fill" style="height: 100%; border-radius: 2px; background: ' + unit.accent + '; width: 0; transition: width 0.3s;"></div>';
      html += '</div>';

      html += '</div></a>';
    });

    html += '</div></div>';

    loadingEl.style.display = 'none';
    contentEl.innerHTML = html;
    contentEl.style.display = '';
  }

  // ---- Render unit index page (lesson cards) ----
  async function renderUnitIndex(subjectSlug, unitSlug) {
    // Fetch unit with subject
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

    // Fetch lessons
    var lessonsResult = await sb
      .from('lessons')
      .select('id, lesson_number, slug, title, hero_image_url, status')
      .eq('unit_id', unit.id)
      .eq('status', 'live')
      .order('lesson_number');

    var lessons = lessonsResult.data || [];

    document.title = unit.name + ' - StudyVault';
    document.body.classList.add(unit.body_class);
    document.getElementById('header-unit-label').textContent = unit.name;

    // Nav links
    var nav = document.getElementById('header-nav');
    nav.innerHTML = '<a href="/">Home</a>' +
      '<a href="/browse/' + subjectSlug + '">Subject Home</a>' +
      '<a href="/' + subjectSlug + '/exam-technique/index.html">Exam Technique</a>' +
      '<a href="/' + subjectSlug + '/revision-technique/index.html">Revision Techniques</a>';

    var html = '<div class="unit-index" style="max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem;">';
    html += '<h1 style="font-family: \'Source Serif 4\', serif; margin-bottom: 0.25rem;">' + esc(unit.name) + '</h1>';
    if (unit.subtitle) {
      html += '<p style="color: var(--text-muted); margin-bottom: 2rem;">' + esc(unit.subtitle) + '</p>';
    }

    html += '<div class="lesson-cards" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1.25rem;">';

    lessons.forEach(function (lesson) {
      var url = '/lesson/' + subjectSlug + '/' + unitSlug + '/' + lesson.lesson_number;
      html += '<a href="' + url + '" class="lesson-card" data-lesson="' + esc(lesson.slug) + '" ' +
        'style="display: block; border-radius: 12px; overflow: hidden; background: white; box-shadow: 0 1px 8px rgba(0,0,0,0.06); text-decoration: none; color: inherit; transition: transform 0.15s, box-shadow 0.15s; border-left: 4px solid ' + unit.accent + ';">';

      html += '<div style="padding: 1rem 1.25rem;">';
      html += '<span style="font-size: 0.75rem; font-weight: 600; color: ' + unit.accent + '; text-transform: uppercase;">Lesson ' + lesson.lesson_number + '</span>';
      html += '<h3 style="font-family: \'Source Serif 4\', serif; font-size: 1rem; margin: 0.25rem 0 0; line-height: 1.4;">' + esc(lesson.title) + '</h3>';
      html += '</div></a>';
    });

    html += '</div>';

    // Back link
    html += '<a href="/browse/' + subjectSlug + '" class="back-link" style="display: inline-block; margin-top: 2rem;">&larr; Back to ' + esc(subject.name) + '</a>';
    html += '</div>';

    loadingEl.style.display = 'none';
    contentEl.innerHTML = html;
    contentEl.style.display = '';
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
