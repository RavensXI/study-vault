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
    // Redirect /browse/separate-sciences → /browse/science (units merge into science)
    if (subjectSlug === 'separate-sciences') {
      window.location.replace('/browse/science');
      return;
    }

    // Determine content source: bespoke (school-specific) or generic (school_id NULL)
    var hasBespoke = (typeof SchoolSession !== 'undefined' && SchoolSession.hasBespoke(subjectSlug));

    // School students can only access subscribed or bespoke subjects
    if (typeof SchoolSession !== 'undefined' && SchoolSession.isActive() && !hasBespoke && !SchoolSession.isSubscribed(subjectSlug)) {
      showError('Subject not available', 'Your school does not currently subscribe to this subject.');
      return;
    }

    var subjectQuery = sb
      .from('subjects')
      .select('id, slug, name, exam_board, spec_code, color, image_url, settings')
      .eq('slug', subjectSlug);

    if (hasBespoke) {
      subjectQuery = subjectQuery.eq('school_id', SchoolSession.getSchoolId());
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

    // Merge Separate Sciences units into Science when student takes triple
    var isScienceSubject = subjectSlug === 'science' || subjectSlug.indexOf('science-') === 0;
    var hasSepSci = false;
    if (isScienceSubject) {
      try {
        var picks = JSON.parse(localStorage.getItem('studyvault-subjects') || '[]');
        hasSepSci = picks.indexOf('separate-sciences') !== -1;
      } catch(e) {}
      // Also check free user prefs
      if (!hasSepSci && typeof FreeUser !== 'undefined' && FreeUser.isActive()) {
        hasSepSci = FreeUser.getSubjectSlugs().indexOf('separate-sciences') !== -1;
      }
      if (hasSepSci) {
        // Fetch the separate-sciences subject and merge its units
        var sepQuery = sb.from('subjects').select('id').eq('slug', 'separate-sciences');
        if (hasBespoke) {
          sepQuery = sepQuery.eq('school_id', SchoolSession.getSchoolId());
        } else {
          sepQuery = sepQuery.is('school_id', null);
        }
        var sepResult = await sepQuery.maybeSingle();
        if (sepResult.data) {
          var sepUnitsResult = await sb.from('units')
            .select('id, slug, name, subtitle, body_class, accent, image_url, lesson_count, sort_order')
            .eq('subject_id', sepResult.data.id)
            .order('sort_order');
          var sepUnits = sepUnitsResult.data || [];
          // Only add units that aren't already in the combined list (by slug)
          var existingSlugs = units.map(function(u) { return u.slug; });
          sepUnits.forEach(function(su) {
            if (existingSlugs.indexOf(su.slug) === -1) {
              su.sort_order = (units.length ? units[units.length - 1].sort_order : 0) + su.sort_order + 1;
              su._isSeparateScience = true;
              units.push(su);
            }
          });
          // Also merge practice_units from sep sci settings
          if (subject.settings && sepResult.data) {
            var sepSubjResult = await sb.from('subjects').select('settings').eq('id', sepResult.data.id).single();
            if (sepSubjResult.data && sepSubjResult.data.settings && sepSubjResult.data.settings.practice_units) {
              subject.settings.practice_units = (subject.settings.practice_units || []).concat(sepSubjResult.data.settings.practice_units);
            }
          }
        }
      }
    }


    // Tier filtering for subject overview — get actual filtered counts per unit
    var TIERED_OVERVIEW = ['maths', 'maths-aqa', 'maths-ocr', 'maths-eduqas', 'science', 'science-edexcel', 'science-ocr', 'separate-sciences'];
    var savedTiersOverview = {};
    try { savedTiersOverview = JSON.parse(localStorage.getItem('studyvault-tiers') || '{}'); } catch(e) {}
    var overviewTier = savedTiersOverview[subjectSlug] || 'higher';
    if (TIERED_OVERVIEW.indexOf(subjectSlug) !== -1 && overviewTier === 'foundation') {
      // Fetch filtered lesson counts per unit
      for (var i = 0; i < units.length; i++) {
        var countResult = await sb.from('lessons').select('id', { count: 'exact', head: true })
          .eq('unit_id', units[i].id).eq('status', 'live').neq('tier', 'higher');
        units[i]._filteredCount = countResult.count || 0;
      }
    }

    // Free user English Lit: filter to only selected texts + compulsory units
    if (subjectSlug.indexOf('english-literature') === 0 && typeof FreeUser !== 'undefined' && FreeUser.isActive()) {
      var freeSubj = FreeUser.getSubject(subjectSlug);
      if (freeSubj && freeSubj.texts && Object.keys(freeSubj.texts).length > 0) {
        var selectedSlugs = Object.values(freeSubj.texts);
        // Compulsory poetry/unseen units (slug varies by board)
        var compulsory = ['power-and-conflict', 'unseen-poetry', 'love-and-relationships',
          'poetry-relationships', 'poetry-conflict', 'poetry-time-and-place', 'poetry-belonging',
          'poetry-love-and-relationships', 'poetry-youth-and-age'];
        units = units.filter(function (u) {
          return selectedSlugs.indexOf(u.slug) !== -1 || compulsory.indexOf(u.slug) !== -1;
        });
      }
    }

    document.title = subject.name + ' - StudyVault';
    document.getElementById('header-unit-label').textContent = subject.name;

    // Add nav links
    var nav = document.getElementById('header-nav');
    var isPracticeSubject = subject.settings && subject.settings.format === 'practice';
    var navHtml = '<a href="/">Home</a>';
    if (!isPracticeSubject) {
      navHtml += '<a href="/guide/' + subjectSlug + '/exam-technique">Exam Technique</a>';
      navHtml += '<a href="/guide/' + subjectSlug + '/revision-technique">Revision Techniques</a>';
    }
    nav.innerHTML = navHtml;

    // Apply colour theme from first unit
    if (units.length > 0) {
      if (units[0].body_class) document.body.classList.add(units[0].body_class);
      if (units[0].accent) document.documentElement.style.setProperty('--accent', units[0].accent);
    }

    // Build HTML matching static landing page structure
    var html = '';

    // Hero
    var displayName = hasSepSci ? 'Science (Triple)' : subject.name;
    html += '<section class="hero"><h1>' + esc(displayName) + '</h1>';
    if (TIERED_OVERVIEW.indexOf(subjectSlug) !== -1) {
      var tierBadgeLabel = overviewTier === 'foundation' ? 'Foundation' : 'Higher';
      html += '<p style="font-family:Inter,sans-serif;font-size:0.8rem;font-weight:600;color:var(--text-secondary);margin:0.5rem 0 0;letter-spacing:0.03em">' + tierBadgeLabel + ' tier</p>';
    }
    html += '</section>';

    // Quote ticker — between title and unit cards
    if (subject.settings && subject.settings.quote_ticker_html) {
      html += subject.settings.quote_ticker_html;
    }

    // Unit grid — uses same .unit-card structure as static pages
    html += '<div class="unit-grid' + (units.length === 1 ? ' single-unit' : '') + '">';

    // Get image positions from subject settings
    var imgPositions = (subject.settings && subject.settings.unit_image_positions) || {};

    units.forEach(function (unit) {
      var unitLessonCount = unit._filteredCount != null ? unit._filteredCount : unit.lesson_count;
      html += '<a href="/browse/' + subjectSlug + '/' + unit.slug + '" class="unit-card" data-unit="' + esc(unit.slug) + '" data-total-lessons="' + unitLessonCount + '" style="--card-accent: ' + unit.accent + ';">';
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
      html += '<span class="unit-meta">0 of ' + unitLessonCount + ' lessons visited</span>';
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
    var hasBespoke = (typeof SchoolSession !== 'undefined' && SchoolSession.hasBespoke(subjectSlug));

    var unitQuery = sb
      .from('units')
      .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, school_id, settings)')
      .eq('slug', unitSlug)
      .eq('subjects.slug', subjectSlug);

    if (hasBespoke) {
      unitQuery = unitQuery.eq('subjects.school_id', SchoolSession.getSchoolId());
    } else {
      unitQuery = unitQuery.is('subjects.school_id', null);
    }

    var unitResult = await unitQuery.maybeSingle();

    // Fallback: if viewing science and unit not found, try separate-sciences
    if (!unitResult.data && (subjectSlug === 'science' || subjectSlug.indexOf('science-') === 0)) {
      var sepQuery = sb.from('units')
        .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, school_id, settings)')
        .eq('slug', unitSlug)
        .eq('subjects.slug', 'separate-sciences');
      if (hasBespoke) {
        sepQuery = sepQuery.eq('subjects.school_id', SchoolSession.getSchoolId());
      } else {
        sepQuery = sepQuery.is('subjects.school_id', null);
      }
      unitResult = await sepQuery.maybeSingle();
    }

    if (!unitResult.data) {
      showError('Unit not found', 'No unit found.');
      return;
    }

    var unit = unitResult.data;
    var subject = unit.subjects;

    var lessonsResult = await sb
      .from('lessons')
      .select('id, lesson_number, slug, title, description, status, tier')
      .eq('unit_id', unit.id)
      .eq('status', 'live')
      .order('lesson_number');

    var lessons = lessonsResult.data || [];

    // Filter by tier if student has a Foundation preference for this subject
    var savedTiers = {};
    try { savedTiers = JSON.parse(localStorage.getItem('studyvault-tiers') || '{}'); } catch(e) {}
    var subjectTier = savedTiers[subjectSlug] || 'higher';
    if (subjectTier === 'foundation') {
      lessons = lessons.filter(function(l) { return l.tier !== 'higher'; });
    }

    document.title = unit.name + ' - StudyVault';
    if (unit.body_class) document.body.classList.add(unit.body_class);
    if (unit.accent) document.documentElement.style.setProperty('--accent', unit.accent);
    if (unit.accent_light) document.documentElement.style.setProperty('--accent-light', unit.accent_light);
    if (unit.accent_badge) document.documentElement.style.setProperty('--accent-badge', unit.accent_badge);
    document.body.dataset.unit = unit.slug;
    document.getElementById('header-unit-label').textContent = unit.name;

    // Nav links
    var nav = document.getElementById('header-nav');
    var isPracticeUnit = (subject.settings && subject.settings.format === 'practice') ||
      (subject.settings && subject.settings.practice_units && subject.settings.practice_units.indexOf(unitSlug) !== -1);
    var unitNavHtml = '<a href="/">Home</a>' +
      '<a href="/browse/' + subjectSlug + '">Subject Home</a>';
    if (!isPracticeUnit) {
      unitNavHtml += '<a href="/guide/' + subjectSlug + '/exam-technique">Exam Technique</a>';
      unitNavHtml += '<a href="/guide/' + subjectSlug + '/revision-technique">Revision Techniques</a>';
    }
    nav.innerHTML = unitNavHtml;

    var html = '';

    // Unit page header — coloured strip with title and description
    html += '<div class="unit-page-header">';
    html += '<div class="unit-page-header-inner">';
    html += '<h1>' + esc(unit.name) + '</h1>';
    if (unit.subtitle) {
      html += '<p>' + esc(unit.subtitle) + '</p>';
    }
    // Tier indicator for tiered subjects
    var TIERED = ['maths', 'maths-aqa', 'maths-ocr', 'maths-eduqas', 'science', 'science-edexcel', 'science-ocr', 'separate-sciences'];
    if (TIERED.indexOf(subjectSlug) !== -1) {
      var tierLabel = subjectTier === 'foundation' ? 'Foundation' : 'Higher';
      html += '<div class="unit-tier-badge" style="margin-top:0.5rem">';
      html += '<span style="font-family:Inter,sans-serif;font-size:0.75rem;font-weight:600;color:rgba(255,255,255,0.85);background:rgba(255,255,255,0.15);padding:0.25rem 0.75rem;border-radius:6px;display:inline-block">';
      html += tierLabel + ' tier</span></div>';
    }
    html += '</div></div>';

    // Progress bar — use filtered count so Foundation students see correct total
    var displayCount = lessons.length;
    html += '<div class="unit-progress">';
    html += '<div class="unit-progress-label">0 of ' + displayCount + ' lessons visited</div>';
    html += '<div class="progress-bar-track"><div class="progress-bar-fill"></div></div>';
    html += '</div>';

    // Lesson grid
    html += '<div class="lesson-grid sv-stagger">';

    var isPractice = (subject.settings && subject.settings.format === 'practice') ||
      (subject.settings && subject.settings.practice_units && subject.settings.practice_units.indexOf(unitSlug) !== -1);
    var lessonPrefix = isPractice ? '/practice/' : '/lesson/';

    lessons.forEach(function (lesson) {
      var url = lessonPrefix + subjectSlug + '/' + unitSlug + '/' + lesson.lesson_number;
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
