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
  // Expose for tier-attempt tracking in practice.html
  window._practiceSupabaseClient = sb;

  // ---- DOM refs ----
  var loadingEl = document.getElementById('practice-loading');
  var errorEl = document.getElementById('practice-error');
  var pageEl = document.getElementById('practice-page');

  // ---- Method card: wrap vocab tables in a <details> so they don't overwhelm
  //      the left panel. MFL method cards ship a 10-15 row vocab table which
  //      fits better hidden behind a click.
  function collapseVocabTables(container, openByDefault) {
    if (!container) return;
    var tables = container.querySelectorAll('table');
    for (var i = 0; i < tables.length; i++) {
      var t = tables[i];
      if (t.closest('details')) continue; // already wrapped
      var details = document.createElement('details');
      details.className = 'method-card-vocab';
      if (openByDefault) details.open = true;
      var summary = document.createElement('summary');
      var rowCount = t.querySelectorAll('tr').length;
      summary.textContent = 'Vocabulary (' + Math.max(rowCount - 1, 0) + ' items)';
      details.appendChild(summary);
      t.parentNode.insertBefore(details, t);
      details.appendChild(t);
    }
  }

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

    // Fallback: if viewing science and unit not found, try separate-sciences
    if (!unitResult.data && (params.subjectSlug === 'science' || params.subjectSlug.indexOf('science-') === 0)) {
      var sepQuery2 = sb.from('units')
        .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, exam_board, school_id)')
        .eq('slug', params.unitSlug)
        .eq('subjects.slug', 'separate-sciences');
      if (hasBespoke) {
        sepQuery2 = sepQuery2.eq('subjects.school_id', SchoolSession.getSchoolId());
      } else {
        sepQuery2 = sepQuery2.is('subjects.school_id', null);
      }
      unitResult = await sepQuery2.maybeSingle();
    }

    if (unitResult.error || !unitResult.data) {
      return { error: 'Unit not found' };
    }

    var unit = unitResult.data;

    // Fetch the lesson — select practice-specific fields
    var lessonResult = await sb
      .from('lessons')
      .select('id, lesson_number, slug, title, description, tier, status, practice_data, related_media, hero_image_url, hero_image_alt, hero_image_caption, hero_image_position, narration_manifest')
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

  function lessonUrl(subjectSlug, unitSlug, lessonNumber) {
    return '/lesson/' + subjectSlug + '/' + unitSlug + '/' + lessonNumber;
  }

  function browseUrl(subjectSlug, unitSlug) {
    if (unitSlug) return '/browse/' + subjectSlug + '/' + unitSlug;
    return '/browse/' + subjectSlug;
  }

  function guideUrl(subjectSlug, type) {
    return '/guide/' + subjectSlug + '/' + type;
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

    // ===== STANDARD HEADER =====
    // Lesson number + unit pill in header
    var headerUnitLabel = document.getElementById('header-unit-label');
    if (headerUnitLabel) {
      headerUnitLabel.textContent = 'Lesson ' + lesson.lesson_number + ' of ' + data.totalLessons;
      if (unit.accent) {
        headerUnitLabel.style.color = unit.accent;
        headerUnitLabel.style.background = unit.accent_badge || '';
        headerUnitLabel.style.padding = '0.15rem 0.6rem';
        headerUnitLabel.style.borderRadius = '6px';
        headerUnitLabel.style.fontSize = '0.75rem';
        headerUnitLabel.style.fontWeight = '600';
      }
    }

    // Nav: Unit Overview
    var navUnitOverview = document.getElementById('nav-unit-overview');
    if (navUnitOverview) {
      navUnitOverview.href = browseUrl(subjectSlug, unitSlug);
      navUnitOverview.textContent = 'Unit Overview';
    }

    // Nav: Prev lesson
    var navPrevLesson = document.getElementById('nav-prev-lesson');
    if (navPrevLesson) {
      if (data.prevLesson) {
        navPrevLesson.href = practiceUrl(subjectSlug, unitSlug, data.prevLesson.lesson_number);
        navPrevLesson.classList.add('nav-lesson-pill');
        navPrevLesson.style.display = '';
      } else {
        navPrevLesson.style.display = 'none';
      }
    }

    // Nav: Next lesson
    var navNextLesson = document.getElementById('nav-next-lesson');
    if (navNextLesson) {
      if (data.nextLesson) {
        navNextLesson.href = practiceUrl(subjectSlug, unitSlug, data.nextLesson.lesson_number);
        navNextLesson.classList.add('nav-lesson-pill');
        navNextLesson.style.display = '';
      } else {
        navNextLesson.style.display = 'none';
      }
    }

    // Legacy hidden elements (for compatibility)
    var lessonNumberEl = document.getElementById('lesson-number');
    if (lessonNumberEl) lessonNumberEl.textContent = 'Lesson ' + lesson.lesson_number + ' of ' + data.totalLessons;

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

      var panelMethodContent = document.getElementById('panel-method-content');
      if (panelMethodContent && mc.content) {
        panelMethodContent.innerHTML = mc.content;
        collapseVocabTables(panelMethodContent, false); // left panel: collapsed by default
      }

      var panelSteps = document.getElementById('panel-method-steps');
      if (mc.steps && mc.steps.length && panelSteps) {
        panelSteps.innerHTML = '';
        for (var si = 0; si < mc.steps.length; si++) {
          var li = document.createElement('li');
          li.innerHTML = mc.steps[si];
          panelSteps.appendChild(li);
        }
      }

      // ===== METHOD MODAL =====
      // Store method card data for initPracticeFeatures
      window._practiceMethodCard = mc;
      window._practiceLoadLessonId = lesson.id;

      var modalTitle = document.getElementById('method-modal-title');
      if (modalTitle) modalTitle.textContent = mc.title || '';

      var modalContent = document.getElementById('method-modal-content');
      if (modalContent) {
        modalContent.innerHTML = mc.content || mc.explanation || '';
        collapseVocabTables(modalContent, true); // modal: expanded by default (user actively opened it)
      }

      var modalSteps = document.getElementById('method-modal-steps');
      if (mc.steps && mc.steps.length && modalSteps) {
        modalSteps.innerHTML = '';
        for (var msi = 0; msi < mc.steps.length; msi++) {
          var mli = document.createElement('li');
          mli.innerHTML = mc.steps[msi];
          modalSteps.appendChild(mli);
        }
      }

      // (Worked example removed from modal — students see it in Learn mode instead)
    } else {
      // No method card — hide modal elements
      window._practiceMethodCard = null;
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
    var we2 = pd.worked_examples;
    if (we2 && we2.length) {
      window._workedExamples = we2;
    } else {
      window._workedExamples = [];
    }

    // ===== PROBLEM BANK =====
    var pb = pd.problem_bank;
    if (pb) {
      // Filter out higher_only problems for Foundation students
      var isFoundation = false;
      try {
        var tiers = JSON.parse(localStorage.getItem('studyvault-tiers') || '{}');
        var subjectBase = params.subjectSlug.replace(/-(?:aqa|edexcel|ocr|eduqas)$/, '');
        var studentTier = tiers[params.subjectSlug] || tiers[subjectBase] || 'higher';
        isFoundation = studentTier === 'foundation';
      } catch(e) {}

      function filterTier(problems) {
        if (!isFoundation) return problems;
        return problems.filter(function(p) { return !p.higher_only; });
      }

      // Same-day sessions keep one order (a mid-session refresh isn't jarring),
      // but tomorrow deals the bank fresh — a returning student shouldn't meet
      // the identical run of questions in the identical order every visit.
      function daySeed(salt) {
        var str = new Date().toISOString().slice(0, 10) + '|' + location.pathname + '|' + salt;
        var h = 2166136261;
        for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
        return h >>> 0;
      }
      function seededShuffle(arr, seed) {
        var a = arr.slice(), s = seed;
        for (var i = a.length - 1; i > 0; i--) {
          s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
          var j = s % (i + 1); var t = a[i]; a[i] = a[j]; a[j] = t;
        }
        return a;
      }
      window._problemBank = {
        bronze: seededShuffle(filterTier(pb.bronze || []), daySeed('b')),
        silver: seededShuffle(filterTier(pb.silver || []), daySeed('s')),
        gold: seededShuffle(filterTier(pb.gold || []), daySeed('g'))
      };
      window._tierDescriptions = {
        bronze: pb.bronze_description || '',
        silver: pb.silver_description || '',
        gold: pb.gold_description || ''
      };
      window._examBoard = subject.exam_board || '';
    }

    // ===== PASSAGES + AI MARKING (from practice_data) =====
    if (pd.passages && pd.passages.length) {
      window._practicePassages = pd.passages;
    }
    if (pd.ai_marking_prompts) {
      window._aiMarkingPrompts = pd.ai_marking_prompts;
    }

    // ===== RELATED MEDIA (from lesson row, fallback to practice_data.related_videos) =====
    // ===== RELATED MEDIA (from lesson row, fallback to practice_data.related_videos) =====
    var relatedMedia = lesson.related_media;
    var mediaSection = document.getElementById('panel-related-videos');
    if (relatedMedia && relatedMedia.length && mediaSection) {
      var rmhtml = '';
      for (var ci = 0; ci < relatedMedia.length; ci++) {
        var cat = relatedMedia[ci];
        if (!cat.items || !cat.items.length) continue;
        rmhtml += '<div class="sidebar-collapsible">';
        rmhtml += '<button class="sidebar-collapsible-toggle" aria-expanded="false" onclick="this.parentElement.classList.toggle(\'open\')">';
        rmhtml += '<span>' + (cat.emoji || '') + ' ' + escapeHtml(cat.category || '') + '</span>';
        rmhtml += '<svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>';
        rmhtml += '</button><div class="sidebar-collapsible-content">';
        for (var ii = 0; ii < cat.items.length; ii++) {
          var item = cat.items[ii];
          rmhtml += '<a href="' + escapeHtml(item.url || '#') + '" target="_blank" rel="noopener noreferrer" class="sidebar-media-item">';
          rmhtml += '<strong>' + escapeHtml(item.title || '') + '</strong>';
          if (item.description) rmhtml += '<span>' + escapeHtml(item.description) + '</span>';
          rmhtml += '</a>';
        }
        rmhtml += '</div></div>';
      }
      mediaSection.innerHTML = rmhtml;
      mediaSection.style.display = '';
    } else if (pd.related_videos && pd.related_videos.length && mediaSection) {
      var vhtml = '<div class="sidebar-collapsible"><button class="sidebar-collapsible-toggle" aria-expanded="false" onclick="this.parentElement.classList.toggle(\'open\')"><span>&#127909; Related Videos</span><svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button><div class="sidebar-collapsible-content">';
      for (var vi = 0; vi < pd.related_videos.length; vi++) {
        var v = pd.related_videos[vi];
        vhtml += '<a href="' + escapeHtml(v.url || '#') + '" target="_blank" rel="noopener noreferrer" class="sidebar-media-item">';
        vhtml += '<strong>' + escapeHtml(v.title || '') + '</strong>';
        if (v.channel) vhtml += '<span>' + escapeHtml(v.channel) + '</span>';
        vhtml += '</a>';
      }
      vhtml += '</div></div>';
      mediaSection.innerHTML = vhtml;
      mediaSection.style.display = '';
    }

    // ===== TOPIC LINKS / PREREQUISITES (from practice_data) =====
    var topicLinks = pd.topic_links;
    if (topicLinks && topicLinks.prerequisites && topicLinks.prerequisites.length) {
      var topicSection = document.getElementById('panel-topic-links');
      var topicPills = document.getElementById('panel-topic-pills');
      if (topicSection && topicPills) {
        var thtml = '';
        for (var ti = 0; ti < topicLinks.prerequisites.length; ti++) {
          var tl = topicLinks.prerequisites[ti];
          var href = tl.slug ? ('/practice/' + subjectSlug + '/' + tl.slug) : '#';
          thtml += '<a href="' + href + '" class="topic-pill">' + escapeHtml(tl.title || '') + '</a>';
        }
        topicPills.innerHTML = thtml;
        topicSection.style.display = '';
      }
    }

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
      banner.style.cssText = 'position:fixed;top:' + 'var(--header-height)' + ';left:0;right:0;z-index:999;background:#fef3c7;color:#92400e;padding:0.5rem 1.25rem;font-size:0.82rem;font-weight:600;text-align:center;border-bottom:2px solid #f59e0b;';
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
