/* ============================================
   StudyVault — Practice Lesson Loader
   Fetches practice lesson data from Supabase
   and populates the practice.html template.
   ============================================ */

(function () {
  'use strict';

  // ---- Supabase client ----
  var sb = window.supabase.createClient(
    'https://baipckgywpnwapobwtsy.supabase.co',
    'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
  );

  // ---- DOM refs ----
  var loadingEl = document.getElementById('practice-loading');
  var errorEl = document.getElementById('practice-error');
  var pageEl = document.getElementById('practice-page');

  // ---- Parse URL ----
  // Expects: /practice/{subject}/{unit}/{number}
  function parseUrl() {
    var path = window.location.pathname;
    var match = path.match(/^\/practice\/([^/]+)\/([^/]+)\/(\d+)\/?$/);
    if (!match) return null;
    var urlParams = new URLSearchParams(window.location.search);
    return {
      subjectSlug: match[1],
      unitSlug: match[2],
      lessonNumber: parseInt(match[3], 10),
      subjectId: urlParams.get('sid') || null
    };
  }

  // ---- Fetch lesson data ----
  async function fetchLesson(params) {
    // Determine staff status
    var isStaff = false;
    try {
      var _a = JSON.parse(sessionStorage.getItem('studyvault-auth')) || JSON.parse(localStorage.getItem('studyvault-auth'));
      isStaff = _a && (_a.role === 'admin' || _a.role === 'teacher');
    } catch(e) {}

    var hasBespoke = (typeof SchoolSession !== 'undefined' && SchoolSession.hasBespoke(params.subjectSlug));

    // Build unit query
    var unitQuery = sb
      .from('units')
      .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, exam_board, school_id)')
      .eq('slug', params.unitSlug)
      .eq('subjects.slug', params.subjectSlug);

    if (params.subjectId) {
      unitQuery = unitQuery.eq('subject_id', params.subjectId);
    } else if (isStaff) {
      unitQuery = unitQuery.not('subjects.school_id', 'is', null);
    } else if (hasBespoke) {
      unitQuery = unitQuery.eq('subjects.school_id', SchoolSession.getSchoolId());
    } else {
      unitQuery = unitQuery.is('subjects.school_id', null);
    }

    var unitResult = await unitQuery.maybeSingle();

    // Staff fallback: if no bespoke found, try generic
    if (isStaff && (!unitResult.data)) {
      unitResult = await sb
        .from('units')
        .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, exam_board, school_id)')
        .eq('slug', params.unitSlug)
        .eq('subjects.slug', params.subjectSlug)
        .is('subjects.school_id', null)
        .maybeSingle();
    }

    if (unitResult.error || !unitResult.data) {
      return { error: 'Unit not found' };
    }

    var unit = unitResult.data;

    // Fetch the lesson — select practice-specific fields
    var lessonResult = await sb
      .from('lessons')
      .select('id, lesson_number, slug, title, description, tier, status, practice_data, hero_image_url, hero_image_alt, hero_image_caption, hero_image_position, narration_manifest')
      .eq('unit_id', unit.id)
      .eq('lesson_number', params.lessonNumber)
      .single();

    if (lessonResult.error || !lessonResult.data) {
      return { error: 'Lesson not found' };
    }

    // Block non-live lessons for students
    if (lessonResult.data.status !== 'live') {
      var isStaffCheck = false;
      try {
        var authSession = JSON.parse(sessionStorage.getItem('studyvault-auth')) || JSON.parse(localStorage.getItem('studyvault-auth'));
        if (authSession && ['admin', 'platform_admin', 'teacher', 'school_admin'].indexOf(authSession.role) !== -1) {
          isStaffCheck = true;
        }
      } catch (e) {}
      if (!isStaffCheck) {
        return { error: 'This lesson is not yet available' };
      }
      lessonResult.data._isPreview = true;
    }

    // Get prev/next lessons for navigation
    var siblingsResult = await sb
      .from('lessons')
      .select('lesson_number, title, slug')
      .eq('unit_id', unit.id)
      .eq('status', 'live')
      .order('lesson_number');

    var siblings = siblingsResult.data || [];
    var currentIdx = siblings.findIndex(function (s) {
      return s.lesson_number === params.lessonNumber;
    });

    return {
      lesson: lessonResult.data,
      unit: unit,
      subject: unit.subjects,
      prevLesson: currentIdx > 0 ? siblings[currentIdx - 1] : null,
      nextLesson: currentIdx < siblings.length - 1 ? siblings[currentIdx + 1] : null,
      totalLessons: unit.lesson_count
    };
  }

  // ---- URL builders ----
  function practiceUrl(subjectSlug, unitSlug, lessonNumber) {
    return '/practice/' + subjectSlug + '/' + unitSlug + '/' + lessonNumber;
  }

  function browseUrl(subjectSlug, unitSlug) {
    if (unitSlug) return '/browse/' + subjectSlug + '/' + unitSlug;
    return '/browse/' + subjectSlug;
  }

  // ---- Render lesson ----
  function renderLesson(data, params) {
    var lesson = data.lesson;
    var unit = data.unit;
    var subject = data.subject || {};
    var pd = lesson.practice_data || {};
    if (typeof pd === 'string') { try { pd = JSON.parse(pd); } catch(e) { pd = {}; } }

    // Set page title
    document.title = 'Practice ' + lesson.lesson_number + ': ' + lesson.title + ' - StudyVault';

    // Set body class for unit theming
    if (unit.body_class) document.body.classList.add(unit.body_class);
    document.body.dataset.unit = unit.slug;
    document.body.dataset.lesson = lesson.slug;

    // Set accent CSS variables from DB
    if (unit.accent) document.documentElement.style.setProperty('--accent', unit.accent);
    if (unit.accent_light) document.documentElement.style.setProperty('--accent-light', unit.accent_light);
    if (unit.accent_badge) document.documentElement.style.setProperty('--accent-badge', unit.accent_badge);

    // Header unit label
    var headerLabel = document.getElementById('header-unit-label');
    headerLabel.textContent = unit.name + ' Practice';
    if (unit.accent) headerLabel.style.color = unit.accent;
    if (unit.accent_badge) headerLabel.style.background = unit.accent_badge;

    // Navigation links
    var subjectSlug = params.subjectSlug;
    var unitSlug = params.unitSlug;
    document.getElementById('nav-unit-overview').href = browseUrl(subjectSlug, unitSlug);
    document.getElementById('nav-exam-technique').href = '/guide/' + subjectSlug + '/exam-technique';
    document.getElementById('nav-revision-technique').href = '/guide/' + subjectSlug + '/revision-technique';

    if (data.prevLesson) {
      var prevLink = document.getElementById('nav-prev-lesson');
      prevLink.href = practiceUrl(subjectSlug, unitSlug, data.prevLesson.lesson_number);
      prevLink.style.display = '';
    }

    if (data.nextLesson) {
      var nextLink = document.getElementById('nav-next-lesson');
      nextLink.href = practiceUrl(subjectSlug, unitSlug, data.nextLesson.lesson_number);
      nextLink.style.display = '';
    }

    // Lesson header
    document.getElementById('lesson-number').textContent =
      unit.name + ' \u2014 Lesson ' + lesson.lesson_number + ' of ' + data.totalLessons;

    // Insert title text before the format badge
    var titleEl = document.getElementById('lesson-title');
    var badge = titleEl.querySelector('.format-badge');
    titleEl.insertBefore(document.createTextNode(lesson.title + ' '), badge);

    // Subtitle
    if (lesson.description) {
      document.getElementById('lesson-subtitle').textContent = lesson.description;
    }

    // ===== A. METHOD CARD =====
    var mc = pd.method_card;
    if (mc) {
      var methodCard = document.getElementById('method-card');
      methodCard.style.display = '';

      document.getElementById('method-title').textContent = mc.title || '';

      // Content paragraphs
      var contentEl = document.getElementById('method-content');
      if (mc.content) {
        contentEl.innerHTML = mc.content; // HTML with KaTeX
      }

      // Steps
      var stepsContainer = document.getElementById('method-steps-container');
      if (mc.steps && mc.steps.length) {
        var ol = document.createElement('ol');
        ol.className = 'method-steps';
        for (var si = 0; si < mc.steps.length; si++) {
          var li = document.createElement('li');
          li.innerHTML = mc.steps[si];
          ol.appendChild(li);
        }
        stepsContainer.appendChild(ol);
      }

      // Example
      var exContainer = document.getElementById('method-example-container');
      if (mc.example) {
        var exDiv = document.createElement('div');
        exDiv.className = 'method-example';
        exDiv.innerHTML = '<div class="method-example-label">Worked Example</div>' + mc.example;
        exContainer.appendChild(exDiv);
      }
    }

    // ===== B. WORKED EXAMPLES =====
    var we = pd.worked_examples;
    if (we && we.length) {
      var weSection = document.getElementById('worked-section');
      weSection.style.display = '';

      var weContainer = document.getElementById('worked-examples-container');
      for (var wi = 0; wi < we.length; wi++) {
        var example = we[wi];
        var weId = 'we-' + (wi + 1);
        var diffClass = example.difficulty ? 'difficulty-' + example.difficulty.toLowerCase() : '';

        var weHtml = '<div class="worked-example" id="' + weId + '">';
        weHtml += '<div class="worked-example-header" onclick="toggleWorkedExample(\'' + weId + '\')">';
        weHtml += '<span class="worked-example-number">' + (wi + 1) + '</span>';
        weHtml += '<span class="worked-example-question">' + escapeHtml(example.question || '') + '</span>';
        if (example.difficulty) {
          weHtml += '<span class="worked-example-difficulty ' + diffClass + '">' + escapeHtml(example.difficulty) + '</span>';
        }
        weHtml += '<svg class="worked-example-toggle" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>';
        weHtml += '</div>';
        weHtml += '<div class="worked-example-body"><div class="worked-steps">';

        var steps = example.steps || [];
        for (var si2 = 0; si2 < steps.length; si2++) {
          var step = steps[si2];
          var isLast = si2 === steps.length - 1;
          var stepClass = isLast ? 'step-content step-hidden step-answer' : 'step-content step-hidden';
          var btnLabel = isLast ? 'Show answer' : 'Show step';

          weHtml += '<div class="worked-step">';
          weHtml += '<div class="step-label">' + escapeHtml(step.label || ('Step ' + (si2 + 1))) + '</div>';
          weHtml += '<div class="' + stepClass + '" data-step="' + (si2 + 1) + '">';
          if (isLast) weHtml += '<div class="step-label">Answer</div>';
          weHtml += step.content || '';
          weHtml += '</div>';
          weHtml += '<button class="step-reveal-btn" onclick="revealStep(this)">';
          weHtml += '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';
          weHtml += ' ' + btnLabel;
          weHtml += '</button>';
          weHtml += '</div>';
        }

        weHtml += '</div></div></div>';
        weContainer.innerHTML += weHtml;
      }
    }

    // ===== C. PROBLEM BANK =====
    var pb = pd.problem_bank;
    if (pb) {
      // Store in window for the interactivity script
      window._problemBank = {
        bronze: pb.bronze || [],
        silver: pb.silver || [],
        gold: pb.gold || []
      };

      var problemsSection = document.getElementById('practice-problems');
      problemsSection.style.display = '';

      // Set tier descriptions
      if (pb.bronze_description) document.getElementById('bronze-description').textContent = pb.bronze_description;
      if (pb.silver_description) document.getElementById('silver-description').textContent = pb.silver_description;
      if (pb.gold_description) document.getElementById('gold-description').textContent = pb.gold_description;

      // Set initial score labels with correct counts
      var bCount = (pb.bronze || []).length;
      var sCount = (pb.silver || []).length;
      var gCount = (pb.gold || []).length;
      var totalCount = bCount + sCount + gCount;

      document.getElementById('score-total').textContent = '0/' + totalCount;
      document.getElementById('score-bronze').textContent = '0/' + bCount;
      document.getElementById('score-silver').textContent = '0/' + sCount;
      document.getElementById('score-gold').textContent = '0/' + gCount;
      document.getElementById('bronze-score').textContent = '0/' + bCount + ' correct';
      document.getElementById('silver-score').textContent = '0/' + sCount + ' correct';
      document.getElementById('gold-score').textContent = '0/' + gCount + ' correct';
      document.getElementById('progress-score-display').textContent = '0/' + totalCount;
      document.getElementById('progress-bronze-count').textContent = '0/' + bCount;
      document.getElementById('progress-silver-count').textContent = '0/' + sCount;
      document.getElementById('progress-gold-count').textContent = '0/' + gCount;
    }

    // ===== NARRATION =====
    window.narrationManifest = lesson.narration_manifest || [];

    // ===== PREV/NEXT NAV =====
    renderLessonNav(data, subjectSlug, unitSlug);

    // Back link
    var backLink = document.getElementById('back-link');
    backLink.href = browseUrl(subjectSlug, unitSlug);
    backLink.innerHTML = '&larr; Back to ' + escapeHtml(unit.name);

    // Show the page
    loadingEl.style.display = 'none';
    pageEl.style.display = '';

    // Show preview banner for non-live lessons (staff only)
    if (lesson._isPreview) {
      var statusLabel = lesson.status === 'pending_review' ? 'Pending Review'
        : lesson.status === 'ready_for_teacher' ? 'Ready for Teacher'
        : lesson.status === 'publishing' ? 'Publishing (Assets Generating)'
        : lesson.status === 'awaiting_qa' ? 'Awaiting QA'
        : lesson.status || 'Draft';
      var banner = document.createElement('div');
      banner.style.cssText = 'position:sticky;top:56px;z-index:999;background:#fef3c7;color:#92400e;padding:0.6rem 1.25rem;font-size:0.85rem;font-weight:600;text-align:center;border-bottom:2px solid #f59e0b;box-shadow:0 2px 8px rgba(0,0,0,0.08);';
      banner.textContent = 'Preview Mode \u2014 Status: ' + statusLabel + ' (not visible to students)';
      pageEl.insertBefore(banner, pageEl.firstChild);
    }

    // Init the practice interactivity (problems, narration, etc.)
    if (typeof window.initPracticeFeatures === 'function') {
      try {
        window.initPracticeFeatures();
      } catch (featureErr) {
        console.warn('Practice feature init error (non-fatal):', featureErr);
      }
    }

    // Render LaTeX equations via KaTeX (if loaded)
    if (typeof renderMathInElement === 'function') {
      renderMathInElement(pageEl, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '\\[', right: '\\]', display: true },
          { left: '\\(', right: '\\)', display: false },
        ],
        throwOnError: false
      });
    }
  }

  // ---- Render prev/next navigation ----
  function renderLessonNav(data, subjectSlug, unitSlug) {
    var nav = document.getElementById('practice-nav');
    var html = '';

    if (data.prevLesson) {
      html += '<a href="' + practiceUrl(subjectSlug, unitSlug, data.prevLesson.lesson_number) + '">';
      html += '<span class="practice-nav-direction">&larr; Previous Lesson</span>';
      html += '<span class="practice-nav-title">' + escapeHtml(data.prevLesson.title) + '</span>';
      html += '</a>';
    }

    if (data.nextLesson) {
      html += '<a href="' + practiceUrl(subjectSlug, unitSlug, data.nextLesson.lesson_number) + '" class="nav-next">';
      html += '<span class="practice-nav-direction">Next Lesson &rarr;</span>';
      html += '<span class="practice-nav-title">' + escapeHtml(data.nextLesson.title) + '</span>';
      html += '</a>';
    }

    nav.innerHTML = html;
  }

  // ---- Show error ----
  function showError(title, message) {
    loadingEl.style.display = 'none';
    document.getElementById('error-title').textContent = title;
    document.getElementById('error-message').textContent = message;
    errorEl.style.display = '';
  }

  // ---- Utility ----
  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ---- Main ----
  async function init() {
    var params = parseUrl();
    if (!params) {
      showError('Invalid URL', 'The practice URL format should be /practice/{subject}/{unit}/{number}');
      return;
    }

    try {
      var data = await fetchLesson(params);

      if (data.error) {
        showError('Lesson not found', data.error);
        return;
      }

      renderLesson(data, params);
    } catch (err) {
      console.error('Practice loader error:', err);
      showError('Something went wrong', 'Could not load the practice lesson. Please try again.');
    }
  }

  // Wait for DOM before init
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
