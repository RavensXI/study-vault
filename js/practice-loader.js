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

    var subjectSlug = params.subjectSlug;
    var unitSlug = params.unitSlug;

    // ===== TOP BAR =====
    var topbarTitle = document.getElementById('topbar-lesson-title');
    if (topbarTitle) topbarTitle.textContent = lesson.title;

    var topbarUnit = document.getElementById('topbar-unit-name');
    if (topbarUnit) topbarUnit.textContent = '\u2014 ' + unit.name;

    // Legacy hidden elements (for compatibility)
    var lessonNumberEl = document.getElementById('lesson-number');
    if (lessonNumberEl) lessonNumberEl.textContent = unit.name + ' \u2014 Lesson ' + lesson.lesson_number + ' of ' + data.totalLessons;

    var titleEl = document.getElementById('lesson-title');
    if (titleEl) {
      var badge = titleEl.querySelector('.format-badge');
      if (badge) titleEl.insertBefore(document.createTextNode(lesson.title + ' '), badge);
    }

    var subtitleEl = document.getElementById('lesson-subtitle');
    if (subtitleEl && lesson.description) subtitleEl.textContent = lesson.description;

    // ===== LEFT PANEL: METHOD CARD =====
    var mc = pd.method_card;
    if (mc) {
      var panelMethod = document.getElementById('panel-method');
      panelMethod.style.display = '';

      var panelMethodTitle = document.getElementById('panel-method-title');
      if (panelMethodTitle) panelMethodTitle.textContent = mc.title || '';

      var panelSteps = document.getElementById('panel-method-steps');
      if (mc.steps && mc.steps.length && panelSteps) {
        panelSteps.innerHTML = '';
        for (var si = 0; si < mc.steps.length; si++) {
          var li = document.createElement('li');
          // Strip HTML for compact panel view
          var tempDiv = document.createElement('div');
          tempDiv.innerHTML = mc.steps[si];
          li.textContent = tempDiv.textContent;
          panelSteps.appendChild(li);
        }
      }
    }

    // ===== LEFT PANEL: EXAM CONTEXT =====
    var examCtx = pd.exam_context;
    if (examCtx) {
      if (examCtx.paper) {
        var paperEl = document.getElementById('exam-context-paper');
        if (paperEl) paperEl.textContent = examCtx.paper;
      }
      if (examCtx.marks) {
        var marksEl = document.getElementById('exam-context-marks');
        if (marksEl) marksEl.textContent = examCtx.marks;
      }
      if (examCtx.frequency) {
        var freqEl = document.getElementById('exam-context-frequency');
        if (freqEl) freqEl.textContent = examCtx.frequency;
      }
    }

    // ===== WORKED EXAMPLES (stored for learn mode) =====
    var we = pd.worked_examples;
    if (we && we.length) {
      window._workedExamples = we;
    } else {
      window._workedExamples = [];
    }

    // ===== PROBLEM BANK =====
    var pb = pd.problem_bank;
    if (pb) {
      window._problemBank = {
        bronze: pb.bronze || [],
        silver: pb.silver || [],
        gold: pb.gold || []
      };
    }

    // ===== NARRATION =====
    window.narrationManifest = lesson.narration_manifest || [];

    // ===== NEXT TOPIC LINK (for summary overlay) =====
    var nextLink = document.getElementById('summary-next-link');
    if (nextLink) {
      if (data.nextLesson) {
        nextLink.href = practiceUrl(subjectSlug, unitSlug, data.nextLesson.lesson_number);
        nextLink.textContent = 'Next: ' + escapeHtml(data.nextLesson.title) + ' \u2192';
      } else {
        nextLink.href = browseUrl(subjectSlug, unitSlug);
        nextLink.textContent = 'Back to ' + escapeHtml(unit.name) + ' \u2192';
      }
    }

    // Show the page, hide loading
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
      banner.style.cssText = 'position:fixed;top:52px;left:0;right:0;z-index:999;background:#fef3c7;color:#92400e;padding:0.5rem 1.25rem;font-size:0.82rem;font-weight:600;text-align:center;border-bottom:2px solid #f59e0b;';
      banner.textContent = 'Preview Mode \u2014 Status: ' + statusLabel + ' (not visible to students)';
      pageEl.appendChild(banner);
    }

    // Init the practice interactivity
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
