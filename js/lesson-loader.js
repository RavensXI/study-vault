/* ============================================
   StudyVault — Lesson Loader
   Fetches lesson data from Supabase and populates the template.
   ============================================ */

(function () {
  'use strict';

  // ---- Supabase client ----
  var sb = window.supabase.createClient(
    'https://baipckgywpnwapobwtsy.supabase.co',
    'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
  );

  // ---- DOM refs ----
  var loadingEl = document.getElementById('lesson-loading');
  var errorEl = document.getElementById('lesson-error');
  var pageEl = document.getElementById('lesson-page');

  // ---- Parse URL ----
  // Expects: /lesson/{subject}/{unit}/{number}
  function parseUrl() {
    var path = window.location.pathname;
    var match = path.match(/^\/lesson\/([^/]+)\/([^/]+)\/(\d+)\/?$/);
    if (!match) return null;
    var urlParams = new URLSearchParams(window.location.search);
    return {
      subjectSlug: match[1],
      unitSlug: match[2],
      lessonNumber: parseInt(match[3], 10),
      subjectId: urlParams.get('sid') || null
    };
  }

  // ---- One-time slug migration ----
  // Free-tier History split: Edexcel renamed `history` → `history-edexcel`,
  // AQA build now at `history-aqa`. Unity students still use `history`.
  // Free-tier users with a saved Edexcel pref go to `history-edexcel`;
  // anonymous and AQA-pref users default to `history-aqa`.
  function chooseHistoryTargetSlug() {
    if (typeof FreeUser !== 'undefined' && FreeUser.isActive && FreeUser.isActive()) {
      var pref = FreeUser.getSubject('history') || FreeUser.getSubject('history-edexcel') || FreeUser.getSubject('history-aqa');
      if (pref && pref.slug) return pref.slug;
    }
    return 'history-aqa';
  }
  function maybeRedirectOldHistorySlug(slug) {
    if (slug !== 'history') return false;
    var isUnity = (typeof SchoolSession !== 'undefined' && SchoolSession.isActive && SchoolSession.isActive());
    if (isUnity) return false;
    var target = chooseHistoryTargetSlug();
    var newPath = window.location.pathname.replace(/^\/lesson\/history\//, '/lesson/' + target + '/');
    if (newPath !== window.location.pathname) {
      window.location.replace(newPath + (window.location.search || '') + (window.location.hash || ''));
      return true;
    }
    return false;
  }

  // ---- Auth check ----
  async function checkAuth() {
    // Try Supabase session first
    var result = await sb.auth.getSession();
    if (result.data.session) {
      return {
        id: result.data.session.user.id,
        name: result.data.session.user.user_metadata.full_name || result.data.session.user.user_metadata.name || '',
        email: result.data.session.user.email,
        isDemo: false
      };
    }

    // Fallback: demo user in localStorage
    var raw = localStorage.getItem('studyvault-user');
    if (raw) {
      try {
        var parsed = JSON.parse(raw);
        // Handle legacy format
        if (parsed.username && !parsed.id) {
          parsed.id = parsed.username;
          parsed.isDemo = true;
        }
        return parsed;
      } catch (e) { /* ignore */ }
    }

    return null;
  }

  // ---- Fetch lesson data ----
  async function fetchLesson(params) {
    // Join through units -> subjects to get the lesson
    // Determine content source: bespoke (school-specific) or generic (school_id NULL)
    // Staff with teacher/admin session can view any lesson — no school_id filter
    var isStaff = false;
    var staffSchoolId = null;
    try {
      var _a = JSON.parse(sessionStorage.getItem('studyvault-auth')) || JSON.parse(localStorage.getItem('studyvault-auth'));
      isStaff = _a && (_a.role === 'admin' || _a.role === 'teacher');
      if (isStaff && _a && _a.school_id) staffSchoolId = _a.school_id;
    } catch(e) {}
    var hasBespoke = (typeof SchoolSession !== 'undefined' && SchoolSession.hasBespoke(params.subjectSlug));
    // School hint for staff: prefer the teacher-login school_id, then any active
    // school session (admin "browsing as Unity"). Without this hint, the staff
    // wildcard query .not('subjects.school_id', 'is', null) returns >1 row when
    // multiple schools share a subject slug (e.g. both Unity and Severn Vale
    // have a 'science' subject), and .maybeSingle() bails with no data.
    var schoolHint = staffSchoolId
      || (typeof SchoolSession !== 'undefined' && SchoolSession.isActive() ? SchoolSession.getSchoolId() : null);

    var unitQuery = sb
      .from('units')
      .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, exam_board, school_id, settings)')
      .eq('slug', params.unitSlug)
      .eq('subjects.slug', params.subjectSlug);

    if (params.subjectId) {
      // Explicit subject ID from review dashboard — use it directly
      unitQuery = unitQuery.eq('subject_id', params.subjectId);
    } else if (isStaff && schoolHint) {
      // Staff with a school hint (teacher login or active school session) —
      // scope to that school first
      unitQuery = unitQuery.eq('subjects.school_id', schoolHint);
    } else if (isStaff) {
      // True admin with no school hint — any bespoke version; .limit(1) keeps
      // maybeSingle happy when multiple schools share a subject slug. Falls
      // back to generic below if nothing returns.
      unitQuery = unitQuery.not('subjects.school_id', 'is', null).limit(1);
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
        .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, exam_board, school_id, settings)')
        .eq('slug', params.unitSlug)
        .eq('subjects.slug', params.subjectSlug)
        .is('subjects.school_id', null)
        .maybeSingle();
    }

    // Fallback: if viewing science and unit not found, try separate-sciences
    if (!unitResult.data && (params.subjectSlug === 'science' || params.subjectSlug.indexOf('science-') === 0)) {
      var sepQuery = sb.from('units')
        .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, exam_board, school_id, settings)')
        .eq('slug', params.unitSlug)
        .eq('subjects.slug', 'separate-sciences');
      if (hasBespoke) {
        sepQuery = sepQuery.eq('subjects.school_id', SchoolSession.getSchoolId());
      } else {
        sepQuery = sepQuery.is('subjects.school_id', null);
      }
      unitResult = await sepQuery.maybeSingle();
    }

    if (unitResult.error || !unitResult.data) {
      return { error: 'Unit not found' };
    }

    var unit = unitResult.data;

    // Now get the lesson
    var lessonResult = await sb
      .from('lessons')
      .select('*')
      .eq('unit_id', unit.id)
      .eq('lesson_number', params.lessonNumber)
      .single();

    if (lessonResult.error || !lessonResult.data) {
      return { error: 'Lesson not found' };
    }

    // Block tier='higher' lessons for Foundation users on tiered subjects.
    // The browse-loader already filters them from lists, but a direct URL
    // (bookmark, search result) would otherwise render an empty page since
    // every paragraph is inside .higher-only.
    if (lessonResult.data.tier === 'higher') {
      var TIERED_DIRECT = ['maths','maths-edexcel','maths-aqa','maths-ocr','maths-eduqas',
        'science','science-aqa','science-edexcel','science-ocr','science-ocr-b',
        'separate-sciences','separate-sciences-edexcel','separate-sciences-ocr','separate-sciences-ocr-b'];
      if (TIERED_DIRECT.indexOf(params.subjectSlug) !== -1) {
        try {
          var directTiers = JSON.parse(localStorage.getItem('studyvault-tiers') || '{}');
          var directBase = params.subjectSlug.replace(/-(?:aqa|edexcel|ocr-b|ocr|eduqas)$/, '');
          var directTier = directTiers[params.subjectSlug] || directTiers[directBase] || 'higher';
          if (directTier === 'foundation') {
            return { error: 'This lesson is Higher Tier only. Switch to Higher in your subject settings to view it.' };
          }
        } catch (e) {}
      }
    }

    // Block non-live lessons for students (admins/teachers can preview)
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
      // Mark as preview for staff
      lessonResult.data._isPreview = true;
    }

    // Get prev/next lessons. Foundation users on tiered subjects skip
    // tier='higher' lessons so navigation doesn't dead-end at hidden lessons.
    var TIERED_FOR_NAV = ['maths','maths-edexcel','maths-aqa','maths-ocr','maths-eduqas',
      'science','science-aqa','science-edexcel','science-ocr','science-ocr-b',
      'separate-sciences','separate-sciences-edexcel','separate-sciences-ocr','separate-sciences-ocr-b'];
    var navFoundationFilter = false;
    if (TIERED_FOR_NAV.indexOf(params.subjectSlug) !== -1) {
      try {
        var navTiers = JSON.parse(localStorage.getItem('studyvault-tiers') || '{}');
        var navBase = params.subjectSlug.replace(/-(?:aqa|edexcel|ocr-b|ocr|eduqas)$/, '');
        var navTier = navTiers[params.subjectSlug] || navTiers[navBase] || 'higher';
        navFoundationFilter = (navTier === 'foundation');
      } catch (e) {}
    }
    var siblingsQuery = sb
      .from('lessons')
      .select('lesson_number, title, slug, tier')
      .eq('unit_id', unit.id)
      .eq('status', 'live')
      .order('lesson_number');
    if (navFoundationFilter) siblingsQuery = siblingsQuery.neq('tier', 'higher');
    var siblingsResult = await siblingsQuery;

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
      totalLessons: siblings.length,
      unitLessons: siblings.map(function (s) { return { number: s.lesson_number, title: s.title }; })
    };
  }

  // ---- Build lesson URL ----
  function lessonUrl(subjectSlug, unitSlug, lessonNumber) {
    return '/lesson/' + subjectSlug + '/' + unitSlug + '/' + lessonNumber;
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

    // Set page title
    document.title = 'Lesson ' + lesson.lesson_number + ': ' + lesson.title + ' - StudyVault';

    // Set body class for unit theming (preserve existing classes like a11y)
    if (unit.body_class) document.body.classList.add(unit.body_class);
    document.body.dataset.unit = unit.slug;
    document.body.dataset.lesson = lesson.slug;
    // Set accent CSS variables directly from DB (works for all units, no CSS class needed)
    if (unit.accent) document.documentElement.style.setProperty('--accent', unit.accent);
    if (unit.accent_light) document.documentElement.style.setProperty('--accent-light', unit.accent_light);
    if (unit.accent_badge) document.documentElement.style.setProperty('--accent-badge', unit.accent_badge);

    // Header unit label
    document.getElementById('header-unit-label').textContent = unit.name;

    // Navigation links — use params from URL (always reliable) over DB join
    var subjectSlug = params.subjectSlug;
    var unitSlug = params.unitSlug;
    document.getElementById('nav-unit-overview').href = browseUrl(subjectSlug, unitSlug);
    var examNav = document.getElementById('nav-exam-technique');
    if (examNav) {
      if (window._hasExamGuides) {
        examNav.href = '/guide/' + subjectSlug + '/exam-technique';
        examNav.style.display = '';
      } else {
        examNav.style.display = 'none';
      }
    }
    document.getElementById('nav-revision-technique').href = '/guide/' + subjectSlug + '/revision-technique';

    if (data.prevLesson) {
      var prevLink = document.getElementById('nav-prev-lesson');
      prevLink.href = lessonUrl(subjectSlug, unitSlug, data.prevLesson.lesson_number);
      prevLink.style.display = '';
    }

    if (data.nextLesson) {
      var nextLink = document.getElementById('nav-next-lesson');
      nextLink.href = lessonUrl(subjectSlug, unitSlug, data.nextLesson.lesson_number);
      nextLink.style.display = '';
    }

    // Lesson header
    document.getElementById('lesson-number').textContent =
      'Lesson ' + lesson.lesson_number + ' of ' + data.totalLessons;
    // Put "Lesson X of Y" in the header pill instead of the inline label
    window._lessonOfTotal = { num: lesson.lesson_number, total: data.totalLessons };
    document.getElementById('lesson-title').textContent = lesson.title;

    // Hero image
    if (lesson.hero_image_url) {
      var heroFig = document.getElementById('hero-figure');
      var heroImg = document.getElementById('hero-image');
      heroImg.src = lesson.hero_image_url;
      heroImg.alt = lesson.hero_image_alt || '';
      if (lesson.hero_image_position) {
        heroImg.style.objectPosition = lesson.hero_image_position;
      }
      if (lesson.hero_image_caption) {
        document.getElementById('hero-caption').textContent = lesson.hero_image_caption;
      }
      heroFig.style.display = '';
    }

    // Content HTML
    var studyNotes = document.getElementById('study-notes');
    studyNotes.innerHTML = lesson.content_html || '';

    // Lesson notice modal — extract any <div class="lesson-notice"> from content
    // and show as a load-time modal the student must dismiss.
    var noticeEls = studyNotes.querySelectorAll('.lesson-notice');
    if (noticeEls.length > 0) {
      var noticeBodies = [];
      var noticeTitle = '';
      noticeEls.forEach(function (n) {
        if (!noticeTitle && n.dataset.noticeTitle) noticeTitle = n.dataset.noticeTitle;
        noticeBodies.push(n.innerHTML);
        n.parentNode.removeChild(n);
      });
      showLessonNoticeModal(noticeTitle || 'Heads up', noticeBodies.join(''), lesson.id);
    }

    // Render Chart.js diagrams embedded in content
    // Charts are stored as JSON in data-chart attribute on canvas elements
    var chartCanvases = studyNotes.querySelectorAll('canvas[data-chart]');
    if (chartCanvases.length > 0) {
      // Delay slightly to ensure canvas is laid out in the DOM
      setTimeout(function() {
        if (typeof Chart === 'undefined') {
          console.warn('Chart.js not loaded — diagrams will not render');
          return;
        }
        chartCanvases.forEach(function(canvas) {
          try {
            // Ensure canvas has dimensions
            if (!canvas.style.width) canvas.style.width = '100%';
            if (!canvas.style.height) canvas.style.height = '300px';
            var config = JSON.parse(canvas.getAttribute('data-chart'));
            config.options = config.options || {};
            config.options.responsive = true;
            config.options.maintainAspectRatio = false;
            new Chart(canvas, config);
          } catch(e) {
            console.warn('Chart render error:', e);
          }
        });
      }, 100);
    }

    // Exam tip
    if (lesson.exam_tip_html) {
      var examTip = document.getElementById('exam-tip');
      examTip.innerHTML = lesson.exam_tip_html;
      examTip.style.display = '';
    }

    // Conclusion
    if (lesson.conclusion_html) {
      var conclusion = document.getElementById('conclusion');
      conclusion.innerHTML = lesson.conclusion_html;
      conclusion.style.display = '';
    }

    // Set window globals for main.js init functions
    window.narrationManifest = lesson.narration_manifest || [];
    window.practiceQuestions = lesson.practice_questions || [];
    window.knowledgeCheck = lesson.knowledge_checks || [];
    window._lessonGlossary = lesson.glossary_terms || [];
    window._lessonFlashcardQuestions = lesson.flashcard_questions || [];
    window._lessonId = lesson.id;
    window._lessonUnitId = unit.id;
    window._subjectSlug = params.subjectSlug;
    window._subjectName = subject.name || '';
    window._unitSlug = unit.slug || params.unitSlug || '';
    window._unitLessons = data.unitLessons || [];
    window._unitName = unit.name || '';
    window._examBoard = subject.exam_board || '';
    // Exam technique guides are legacy — only Unity-bespoke subjects have them.
    // Opt in via subjects.settings.has_exam_guides = true. Default false for new subjects.
    window._hasExamGuides = !!(subject.settings && subject.settings.has_exam_guides);

    // Extract podcast URL from related_media (if present)
    window.podcastUrl = null;
    var relMedia = lesson.related_media || [];
    for (var mi = 0; mi < relMedia.length; mi++) {
      var rmCat = relMedia[mi];
      if (!rmCat) continue;
      if ((rmCat.category || '').toLowerCase() === 'podcasts') {
        var items = Array.isArray(rmCat.items) ? rmCat.items : [];
        for (var mj = 0; mj < items.length; mj++) {
          var it = items[mj];
          if (it && it.title === 'Lesson Podcast' && it.url && it.url !== '#') {
            window.podcastUrl = it.url;
            break;
          }
        }
      }
    }

    // Video overview (YouTube ID, Google Drive URL, or direct MP4 URL)
    if (lesson.youtube_video_id && lesson.youtube_video_id !== 'practice-only') {
      var videoSection = document.getElementById('sidebar-video-section');
      var iframe = document.getElementById('sidebar-video-iframe');
      var videoId = lesson.youtube_video_id;
      var isGDrive = videoId.indexOf('drive.google.com') !== -1;
      var isDirectVideo = /\.(mp4|webm)(\?|$)/i.test(videoId) || videoId.indexOf('r2.dev/') !== -1;
      var embedSrc = videoId.startsWith('http')
        ? videoId
        : 'https://www.youtube.com/embed/' + videoId;

      if (isGDrive || isDirectVideo) {
        // Google Drive or direct video: show thumbnail with play button, open modal on click
        var container = iframe.closest('.sidebar-video');
        container.classList.add('sidebar-video--gdrive');
        iframe.remove();

        // Thumbnail: Google Drive has its own, direct video uses a generic play card
        var thumbHtml = '';
        if (isGDrive) {
          var fileIdMatch = videoId.match(/\/d\/([^/]+)/);
          var thumbUrl = fileIdMatch
            ? 'https://drive.google.com/thumbnail?id=' + fileIdMatch[1] + '&sz=w600'
            : '';
          thumbHtml = '<img class="sidebar-video-thumb" src="' + thumbUrl + '" alt="Video overview">';
        } else {
          thumbHtml = '<div class="sidebar-video-thumb sidebar-video-thumb--generic"><span class="sv-video-label">StudyVault</span><span class="sv-video-sublabel">Video Overview</span></div>';
        }

        container.innerHTML =
          thumbHtml +
          '<button class="sidebar-video-play" aria-label="Play video overview">' +
            '<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="5,3 19,12 5,21"/></svg>' +
          '</button>';

        container.addEventListener('click', function () {
          openVideoModal(embedSrc, lesson.title, isDirectVideo);
        });

        // AI-generated video disclosure — StudyVault's own overview videos are
        // AI-made (NotebookLM); curated YouTube documentaries (the else branch)
        // are third-party and get no such note.
        if (!videoSection.querySelector('.sidebar-video-ai-note')) {
          var vnote = document.createElement('div');
          vnote.className = 'sidebar-video-ai-note';
          vnote.textContent = 'This video was generated using AI. Voices are synthetic.';
          vnote.style.cssText = 'font-size:0.68rem;line-height:1.3;color:var(--text-muted,#8a8580);margin-top:0.4rem;text-align:center';
          videoSection.appendChild(vnote);
        }
      } else {
        iframe.src = embedSrc;
        iframe.title = lesson.title;
      }
      videoSection.style.display = '';
    }

    // Flashcard revision button in sidebar (opens modal overlay)
    (function () {
      var kcSection = document.querySelector('.sidebar-knowledge-check');
      if (kcSection) {
        var flashcardSection = document.createElement('div');
        flashcardSection.className = 'sidebar-section sidebar-flashcard-section';
        flashcardSection.innerHTML =
          '<button type="button" class="sidebar-flashcard-link" id="sidebar-flashcard-btn">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;flex-shrink:0">' +
              '<rect x="2" y="4" width="14" height="12" rx="2"/>' +
              '<rect x="8" y="8" width="14" height="12" rx="2"/>' +
            '</svg>' +
            '<span>Flashcards</span>' +
          '</button>';
        kcSection.parentElement.insertBefore(flashcardSection, kcSection.nextSibling);
      }
    })();

    // Related media
    renderRelatedMedia(lesson.related_media || []);

    // Prev/next navigation
    renderLessonNav(data, subjectSlug, unitSlug);

    // Back link
    var backLink = document.getElementById('back-link');
    backLink.href = browseUrl(subjectSlug, unitSlug);
    backLink.innerHTML = '&larr; Back to ' + unit.name;

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
      banner.style.cssText = 'position:sticky;top:56px;z-index:999;background:#fef3c7;color:#92400e;padding:0.6rem 1.25rem;font-size:0.85rem;font-weight:600;text-align:center;border-bottom:2px solid #f59e0b;box-shadow:0 2px 8px rgba(0,0,0,0.08);grid-column:1/-1;';
      banner.textContent = 'Preview Mode \u2014 Status: ' + statusLabel + ' (not visible to students)';
      pageEl.insertBefore(banner, pageEl.firstChild);
    }

    // Ad placeholders disabled — no ads on free tier for now
    // Re-enable when ad strategy is decided (see docs/DPIA_SCREENING.md)

    // Apply Foundation tier body class if student selected Foundation
    // Hides .higher-only content via CSS
    try {
      var tiers = JSON.parse(localStorage.getItem('studyvault-tiers') || '{}');
      var subjectBase = params.subjectSlug.replace(/-(?:aqa|edexcel|ocr-b|ocr|eduqas)$/, '');
      var tier = tiers[params.subjectSlug] || tiers[subjectBase] || 'higher';
      if (tier === 'foundation') {
        document.body.classList.add('tier-foundation');
      }
    } catch(e) {}

    // First-time tutorial — runs once per device on first article-lesson visit
    if (!lesson._isPreview) {
      try {
        var __td = localStorage.getItem('sv-lesson-tutorial-done');
        var __htd = localStorage.getItem('sv-highlight-tutorial-done');
        var __hon = localStorage.getItem('sv-hl-enabled') === '1';
        // Run if first-time, OR returning student with highlight feature on
        // who hasn't seen the highlight coachmark yet.
        if (!__td || (__hon && !__htd)) {
          // Defer until layout settles + main.js's initLessonFeatures has wired up DOM
          setTimeout(maybeStartLessonTutorial, 1500);
        }
      } catch (e) {}
    }

    // Init lesson features from main.js (Phase 2 functions)
    // Wrapped in its own try/catch so a feature init failure doesn't
    // block visit tracking or show a misleading "could not load" error
    if (typeof window.initLessonFeatures === 'function') {
      try {
        window.initLessonFeatures();
      } catch (featureErr) {
        console.warn('Feature init error (non-fatal):', featureErr);
      }
    }

    // "Show tour" button — must run AFTER initLessonFeatures so the gutter
    // and sidebar lesson-progress section are in the DOM
    addSidebarTourButton();
    wireReplayTourButton();

    // Exam-countdown pill — explicit call after dynamic .lesson-header is
    // rendered. The script's own DOMContentLoaded timer can race with
    // the Supabase fetch on first visit; this guarantees the pill lands.
    // Idempotent — duplicate from the timer is suppressed inside init().
    if (typeof window.initExamCountdown === 'function') window.initExamCountdown();

    // Beta banner + report button for generic content (school_id NULL)
    if (!subject.school_id) {
      // Beta banner below the progress bar
      var progressBar = document.querySelector('.lesson-progress-inline-wrap') || document.querySelector('.lesson-progress-inline');
      var betaBanner = document.createElement('div');
      betaBanner.className = 'beta-banner';
      betaBanner.innerHTML = '<span class="beta-badge">BETA</span> This content is AI-generated from the exam specification. It has been verified against the spec but may contain errors.';
      var mainCol = document.querySelector('.lesson-content');
      if (mainCol) {
        mainCol.insertBefore(betaBanner, mainCol.firstChild);
      } else {
        var insertAfter = progressBar || document.querySelector('.lesson-header');
        if (insertAfter && insertAfter.parentNode) {
          insertAfter.parentNode.insertBefore(betaBanner, insertAfter.nextSibling);
        }
      }

      // Report error button at the bottom of the lesson content
      var studyNotes = document.getElementById('study-notes');
      if (studyNotes) {
        var reportBtn = document.createElement('div');
        reportBtn.className = 'report-error-section';
        var reportSubject = encodeURIComponent(subject.name + ' - L' + lesson.lesson_number + ': ' + lesson.title);
        var reportBody = encodeURIComponent('I found an error in this lesson:\n\nSubject: ' + subject.name + ' (' + (subject.exam_board || '') + ')\nLesson: ' + lesson.lesson_number + ' - ' + lesson.title + '\nURL: ' + window.location.href + '\n\nError description:\n');
        reportBtn.innerHTML = '<a href="mailto:studyvault.info@gmail.com?subject=Error%20Report%3A%20' + reportSubject + '&body=' + reportBody + '" class="report-error-btn">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>' +
          ' Spotted an error? Let us know</a>';
        studyNotes.appendChild(reportBtn);
      }
    }

    // Trigger scroll reveal animations on lesson content
    if (typeof window.initRevealAnimations === 'function') {
      window.initRevealAnimations();
    }

    // Render LaTeX equations via KaTeX (if loaded)
    if (typeof renderMathInElement === 'function') {
      var katexOpts = {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '\\[', right: '\\]', display: true },
          { left: '\\(', right: '\\)', display: false },
        ],
        throwOnError: false
      };
      ['study-notes', 'conclusion', 'exam-tip'].forEach(function(id) {
        var el = document.getElementById(id);
        if (el) renderMathInElement(el, katexOpts);
      });
    }
  }

  // ---- Render related media sidebar ----
  function renderRelatedMedia(categories) {
    var container = document.getElementById('sidebar-media');
    if (!categories.length) {
      container.style.display = 'none';
      return;
    }

    var html = '<div class="sidebar-section-title">Related Media</div>';

    var hasPodcastTab = !!window.podcastUrl;

    categories.forEach(function (cat) {
      if (!cat || typeof cat !== 'object') return;
      var categoryName = cat.category || '';
      // Defensive: items may be null/undefined/non-array on some legacy lessons
      var items = Array.isArray(cat.items) ? cat.items : [];

      // If lesson podcast is in the player tabs, rename category and filter it out
      if (hasPodcastTab && categoryName.toLowerCase() === 'podcasts') {
        items = items.filter(function(item) { return item && item.title !== 'Lesson Podcast'; });
        if (items.length === 0) return; // skip empty category entirely
        categoryName = 'Other Podcasts';
      }

      // Skip categories that ended up empty (null items, all filtered out, etc.)
      if (items.length === 0) return;

      html += '<div class="sidebar-collapsible">';
      html += '<button class="sidebar-collapsible-toggle" aria-expanded="false">';
      html += '<span>' + (cat.emoji ? cat.emoji + ' ' : '') + cleanText(categoryName) + '</span>';
      html += '<svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>';
      html += '</button>';
      html += '<div class="sidebar-collapsible-content">';

      items.forEach(function (item) {
        if (!item || !item.url) return;
        html += '<a href="' + escapeAttr(item.url) + '" target="_blank" rel="noopener noreferrer" class="sidebar-media-item">';
        html += '<strong>' + cleanText(item.title || '') + '</strong>';
        if (item.description) {
          html += '<span>' + cleanText(item.description) + '</span>';
        }
        html += '</a>';
      });

      html += '</div></div>';
    });

    // Add podcast feed subscribe button if this subject has a podcast
    if (hasPodcastTab) {
      var feedUrl = window.location.origin + '/api/podcast/feed?subject=' + (window._subjectSlug || '');
      if (typeof SchoolSession !== 'undefined' && SchoolSession.isActive()) {
        var sess = SchoolSession.get();
        if (sess && sess.school_id) feedUrl += '&school=' + sess.school_id;
      }
      window._podcastFeedUrl = feedUrl;
      html += '<div class="sidebar-podcast-feed">';
      html += '<button type="button" class="sidebar-podcast-feed-btn" onclick="window._showPodcastModal()">';
      html += '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/></svg>';
      html += ' Subscribe in podcast app';
      html += '</button>';
      html += '</div>';
    }

    container.innerHTML = html;
  }

  // ---- Podcast subscribe modal ----
  window._showPodcastModal = function () {
    var url = window._podcastFeedUrl;
    if (!url) return;

    // Remove existing modal if any
    var old = document.getElementById('podcast-feed-modal');
    if (old) old.remove();

    var overlay = document.createElement('div');
    overlay.id = 'podcast-feed-modal';
    overlay.className = 'podcast-feed-overlay';
    overlay.innerHTML =
      '<div class="podcast-feed-modal">' +
        '<button class="podcast-feed-close" aria-label="Close">&times;</button>' +
        '<h3>Listen on your podcast app</h3>' +
        '<p class="podcast-feed-intro">Take these revision podcasts with you. Listen on the bus, walking to school, or anywhere.</p>' +
        '<div class="podcast-feed-steps">' +
          '<div class="podcast-feed-step"><span class="podcast-feed-step-num">1</span><div>Open your podcast app<br><span class="podcast-feed-step-hint">Apple Podcasts, Pocket Casts, Overcast, Castro, etc.</span></div></div>' +
          '<div class="podcast-feed-step"><span class="podcast-feed-step-num">2</span><div>Find "Add by URL" or "Subscribe by RSS"<br><span class="podcast-feed-step-hint">Usually in Search or Settings</span></div></div>' +
          '<div class="podcast-feed-step"><span class="podcast-feed-step-num">3</span><div>Paste the link you copied below</div></div>' +
        '</div>' +
        '<div class="podcast-feed-url-row">' +
          '<input type="text" class="podcast-feed-url" value="' + url.replace(/"/g, '&quot;') + '" readonly onclick="this.select()">' +
          '<button type="button" class="podcast-feed-copy-btn">Copy link</button>' +
        '</div>' +
        '<p class="podcast-feed-note">All episodes will appear in order. New lessons are added automatically.</p>' +
      '</div>';

    document.body.appendChild(overlay);

    // Close handlers
    overlay.querySelector('.podcast-feed-close').addEventListener('click', function () { overlay.remove(); });
    overlay.addEventListener('click', function (e) { if (e.target === overlay) overlay.remove(); });

    // Copy handler
    overlay.querySelector('.podcast-feed-copy-btn').addEventListener('click', function () {
      var input = overlay.querySelector('.podcast-feed-url');
      navigator.clipboard.writeText(input.value).then(function () {
        var btn = overlay.querySelector('.podcast-feed-copy-btn');
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(function () { btn.textContent = 'Copy link'; btn.classList.remove('copied'); }, 2000);
      });
    });
  };

  // ---- Render prev/next navigation ----
  function renderLessonNav(data, subjectSlug, unitSlug) {
    var nav = document.getElementById('lesson-nav');
    var html = '';

    if (data.prevLesson) {
      html += '<a href="' + lessonUrl(subjectSlug, unitSlug, data.prevLesson.lesson_number) + '" class="lesson-nav-link lesson-nav-link--prev">';
      html += '<span class="lesson-nav-direction">&larr; Previous Lesson</span>';
      html += '<span class="lesson-nav-title">' + escapeHtml(data.prevLesson.title) + '</span>';
      html += '</a>';
    }

    if (data.nextLesson) {
      html += '<a href="' + lessonUrl(subjectSlug, unitSlug, data.nextLesson.lesson_number) + '" class="lesson-nav-link lesson-nav-link--next">';
      html += '<span class="lesson-nav-direction">Next Lesson &rarr;</span>';
      html += '<span class="lesson-nav-title">' + escapeHtml(data.nextLesson.title) + '</span>';
      html += '</a>';
    }

    nav.innerHTML = html;
  }

  // ---- Record lesson visit (fire and forget) ----
  function recordVisit(user, lessonId) {
    if (!user || user.isDemo) {
      // For demo users, still use localStorage
      var unit = document.body.dataset.unit;
      var lesson = document.body.dataset.lesson;
      if (unit && lesson) {
        var visited = JSON.parse(localStorage.getItem('studyvault-visited') || '{}');
        if (!visited[unit]) visited[unit] = [];
        if (visited[unit].indexOf(lesson) === -1) visited[unit].push(lesson);
        localStorage.setItem('studyvault-visited', JSON.stringify(visited));
      }
      return;
    }

    // Supabase upsert for authenticated users
    sb.from('lesson_visits').upsert(
      {
        user_id: user.id,
        lesson_id: lessonId,
        last_visit: new Date().toISOString(),
        visit_count: 1
      },
      { onConflict: 'user_id,lesson_id' }
    ).then(function () {
      // Also increment visit_count via RPC or update
      sb.rpc('increment_visit_count', {
        p_user_id: user.id,
        p_lesson_id: lessonId
      }).then(function () {}).catch(function () {});
    }).catch(function () {});
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

  // Some related_media titles carry literal HTML entities (e.g. "&mdash;") that
  // would otherwise render as text once escaped. Decode to the real character
  // first, then escapeHtml re-escapes safely for insertion.
  function decodeEntities(str) {
    if (!str || str.indexOf('&') === -1) return str || '';
    var t = document.createElement('textarea');
    t.innerHTML = str;
    return t.value;
  }
  function cleanText(str) { return escapeHtml(decodeEntities(str || '')); }

  function escapeAttr(str) {
    return str.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // ---- First-time lesson tutorial ----
  function maybeStartLessonTutorial() {
    var fullTutorialDone = false;
    var highlightTutorialDone = false;
    // Feature is GA — default ON; only false if the student explicitly opted out.
    var highlightFeatureOn = true;
    try {
      fullTutorialDone = localStorage.getItem('sv-lesson-tutorial-done') === '1';
      highlightTutorialDone = localStorage.getItem('sv-highlight-tutorial-done') === '1';
      if (localStorage.getItem('sv-hl-enabled') === '0') highlightFeatureOn = false;
    } catch (e) {}
    if (fullTutorialDone && (highlightTutorialDone || !highlightFeatureOn)) return;
    // Returning students with the highlight feature on get a one-step mini-tour
    var highlightOnlyMode = fullTutorialDone && highlightFeatureOn && !highlightTutorialDone;

    var isMobile = window.innerWidth <= 768;

    // Helper: is this element actually rendered? offsetParent unreliable —
    // returns null for position:fixed elements (broke the gutter target).
    function isVisible(el) {
      if (!el) return false;
      var s = window.getComputedStyle(el);
      if (s.display === 'none' || s.visibility === 'hidden') return false;
      var r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    }

    // Resolve targets that actually exist on this rendered page.
    // Steps with no target are auto-dropped.
    var studyNotes = document.getElementById('study-notes');
    var firstTerm = studyNotes ? studyNotes.querySelector('dfn.term') : null;
    var firstTip = studyNotes ? studyNotes.querySelector('.revision-tip-btn, .key-fact[data-revision-tip]') : null;
    var audioPlayer = document.querySelector('.audio-player-wrapper');
    var podcastTab = document.querySelector('.audio-tab[data-mode="podcast"]');
    var practiceSection = document.getElementById('practice');
    var kcBtn = document.getElementById('knowledge-check-btn');
    var flashcardBtn = document.querySelector('.sidebar-flashcard-section, .sidebar-flashcard-link');
    // Lesson progress checklist has TWO renderings — the sidebar card on
    // narrow viewports and the gutter rail on ≥1400px. Pick whichever is
    // currently visible.
    var lessonProgress = null;
    var gutter = document.querySelector('.gutter-progress');
    var sidebarProgress = document.querySelector('.sidebar-progress-section');
    if (isVisible(gutter)) lessonProgress = gutter;
    else if (isVisible(sidebarProgress)) lessonProgress = sidebarProgress;
    var sidebarMedia = document.getElementById('sidebar-media');
    var hasMedia = sidebarMedia && sidebarMedia.children.length > 0 && isVisible(sidebarMedia);
    var podcastSubBtn = document.querySelector('.sidebar-podcast-feed-btn');
    // Cinematic video sidebar — Unity only on the free tier (display:none
    // when no youtube_video_id, so isVisible naturally drops the step there)
    var videoSection = document.getElementById('sidebar-video-section');
    var revisionNav = document.getElementById('nav-revision-technique');
    var revisionNavVisible = isVisible(revisionNav);
    var hamburger = document.querySelector('.mobile-menu-btn');
    var bugFab = document.querySelector('.bugr-fab');

    // Header step — on mobile the link is hidden behind the hamburger,
    // so we anchor to the hamburger and rephrase.
    var revisionNavStep = revisionNavVisible
      ? {
          target: revisionNav,
          text: 'How to revise — proven techniques like retrieval, spacing, and dual coding, with examples for this subject.',
          side: 'bottom'
        }
      : (hamburger ? {
          target: hamburger,
          text: 'Open this menu to find the Revision Techniques guide — proven techniques like retrieval and spacing, with examples for this subject.',
          side: 'bottom'
        } : null);

    var rawSteps = [
      revisionNavStep,
      audioPlayer && isVisible(audioPlayer) && {
        target: audioPlayer,
        text: 'Listen to the lesson read aloud while you follow along. Tap to play, drag to scrub, or change speed.',
        side: 'bottom'
      },
      isVisible(podcastTab) && {
        target: podcastTab,
        text: 'Switch to the lesson podcast — a short audio summary you can listen to on the go.',
        side: 'bottom'
      },
      isVisible(videoSection) && {
        target: videoSection,
        text: 'A short cinematic video overview of the lesson — perfect if you want to grasp the big picture before reading.',
        side: 'left'
      },
      firstTerm && isVisible(firstTerm) && {
        target: firstTerm,
        text: 'Tap or hover any underlined word to see what it means without leaving the lesson.',
        side: 'bottom',
        _id: 'glossary'
      },
      highlightFeatureOn && document.querySelector('.sv-hl-fab--enter') && {
        target: document.querySelector('.sv-hl-fab--enter'),
        text: (window.innerWidth <= 768
          ? 'Tap Highlight Mode to start. Then tap a word to mark where the highlight starts, and tap another word to finish it. You can add a colour and a note. Everything you save lives in this same corner.'
          : 'Click Highlight Mode to start. Then drag across any text in the lesson to highlight it — pick a colour and add a note if you like. Everything you save lives in this same corner.'),
        side: 'top',
        _id: 'highlight'
      },
      firstTip && isVisible(firstTip) && {
        target: firstTip,
        text: 'Click any lightbulb to reveal a short revision task linked to that part of the lesson. Different prompts for different ideas — list, define, recall, apply.',
        side: 'right'
      },
      lessonProgress && {
        target: lessonProgress,
        text: 'Your lesson checklist. There\'s no required order — work through it however you like. Completing the quick quiz and flashcards ticks them off automatically.',
        side: 'left'
      },
      kcBtn && isVisible(kcBtn) && {
        target: kcBtn,
        text: 'A quick five-question quiz to check what stuck.',
        side: 'left'
      },
      flashcardBtn && isVisible(flashcardBtn) && {
        target: flashcardBtn,
        text: 'Revise key ideas with flashcards — flip, mark right or wrong, repeat.',
        side: 'left'
      },
      hasMedia && {
        target: sidebarMedia,
        text: 'Genuinely good external content — podcasts, videos, films and study tools — for when you want to step away from revision but stay in the topic.',
        side: 'left'
      },
      podcastSubBtn && isVisible(podcastSubBtn) && {
        target: podcastSubBtn,
        text: 'Subscribe to the subject\'s lesson podcasts in your usual app — Apple Podcasts, Pocket Casts, Overcast, or any other podcast app that supports adding a feed by URL.',
        side: 'left'
      },
      practiceSection && {
        target: practiceSection.querySelector('.practice-card') || practiceSection,
        text: 'Have a go at exam-style questions. You can mark your own answer or get AI feedback to compare.',
        side: 'top'
      },
      bugFab && {
        target: bugFab,
        text: 'Spotted a mistake or something that doesn\'t work? Tap this to send a quick report — it includes a screenshot so we can see exactly what you saw.',
        side: 'left',
        pinLast: true
      }
    ];
    var steps = rawSteps.filter(Boolean);

    // Returning students who've already seen the full tour only see the new
    // highlight coachmark — narrow the steps array to just that one.
    if (highlightOnlyMode) {
      steps = steps.filter(function (s) { return s._id === 'highlight'; });
    }

    // Sort by visual document position (top-to-bottom) so the tour flows
    // naturally without zig-zagging up and down. Pin bug FAB to the end
    // since it's position:fixed (its rect.top is viewport-relative).
    steps.forEach(function (s) {
      if (s.pinLast) { s._sortKey = Number.MAX_VALUE; return; }
      var r = s.target.getBoundingClientRect();
      s._sortKey = r.top + window.scrollY;
    });
    steps.sort(function (a, b) { return a._sortKey - b._sortKey; });

    if (steps.length === 0) {
      try {
        localStorage.setItem('sv-lesson-tutorial-done', '1');
        if (highlightFeatureOn) localStorage.setItem('sv-highlight-tutorial-done', '1');
      } catch (e) {}
      return;
    }

    // ----- Build DOM -----
    var backdropTop = document.createElement('div');
    var backdropRight = document.createElement('div');
    var backdropBottom = document.createElement('div');
    var backdropLeft = document.createElement('div');
    [backdropTop, backdropRight, backdropBottom, backdropLeft].forEach(function (el) {
      el.className = 'sv-tutorial-backdrop';
      document.body.appendChild(el);
    });

    var tooltipEl = document.createElement('div');
    tooltipEl.className = 'sv-tutorial-tooltip';
    var dotsHtml = steps.map(function () { return '<span></span>'; }).join('');
    tooltipEl.innerHTML =
      '<div class="sv-tutorial-tooltip-arrow"></div>' +
      '<div class="sv-tutorial-tooltip-text"></div>' +
      '<div class="sv-tutorial-tooltip-actions">' +
        '<div class="sv-tutorial-tooltip-progress">' + dotsHtml + '</div>' +
        '<div class="sv-tutorial-tooltip-buttons">' +
          '<button type="button" class="sv-tutorial-tooltip-skip">Skip tour</button>' +
          '<button type="button" class="sv-tutorial-tooltip-btn"></button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(tooltipEl);

    var textEl = tooltipEl.querySelector('.sv-tutorial-tooltip-text');
    var btnEl = tooltipEl.querySelector('.sv-tutorial-tooltip-btn');
    var skipEl = tooltipEl.querySelector('.sv-tutorial-tooltip-skip');
    var arrowEl = tooltipEl.querySelector('.sv-tutorial-tooltip-arrow');
    var dotEls = tooltipEl.querySelectorAll('.sv-tutorial-tooltip-progress span');

    var spotlightedEl = null;
    function clearSpotlight() {
      if (spotlightedEl) {
        spotlightedEl.classList.remove('sv-tutorial-spotlight');
        spotlightedEl = null;
      }
    }
    function setSpotlight(el) {
      clearSpotlight();
      if (el && el.classList) {
        el.classList.add('sv-tutorial-spotlight');
        spotlightedEl = el;
      }
    }

    // ----- Backdrop frame around target rect -----
    function paintBackdrop(target) {
      var rect = target.getBoundingClientRect();
      var pad = 8;
      var x1 = Math.max(0, rect.left - pad);
      var y1 = Math.max(0, rect.top - pad);
      var x2 = Math.min(window.innerWidth, rect.right + pad);
      var y2 = Math.min(window.innerHeight, rect.bottom + pad);

      backdropTop.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:' + y1 + 'px;background:rgba(20,18,15,0.55);z-index:1099;pointer-events:none;';
      backdropBottom.style.cssText = 'position:fixed;top:' + y2 + 'px;left:0;width:100vw;height:' + Math.max(0, window.innerHeight - y2) + 'px;background:rgba(20,18,15,0.55);z-index:1099;pointer-events:none;';
      backdropLeft.style.cssText = 'position:fixed;top:' + y1 + 'px;left:0;width:' + x1 + 'px;height:' + (y2 - y1) + 'px;background:rgba(20,18,15,0.55);z-index:1099;pointer-events:none;';
      backdropRight.style.cssText = 'position:fixed;top:' + y1 + 'px;left:' + x2 + 'px;width:' + Math.max(0, window.innerWidth - x2) + 'px;height:' + (y2 - y1) + 'px;background:rgba(20,18,15,0.55);z-index:1099;pointer-events:none;';
      [backdropTop, backdropRight, backdropBottom, backdropLeft].forEach(function (el) { el.classList.add('active'); });
    }

    function positionTooltip(target, preferSide) {
      var rect = target.getBoundingClientRect();
      var tw = tooltipEl.offsetWidth || 300;
      var th = tooltipEl.offsetHeight || 130;
      arrowEl.className = 'sv-tutorial-tooltip-arrow';

      var spaceR = window.innerWidth - rect.right;
      var spaceL = rect.left;
      var spaceB = window.innerHeight - rect.bottom;
      var spaceT = rect.top;

      function placeRight() {
        tooltipEl.style.left = Math.min(rect.right + 16, window.innerWidth - tw - 8) + 'px';
        tooltipEl.style.top = Math.max(8, Math.min(rect.top + rect.height / 2 - th / 2, window.innerHeight - th - 8)) + 'px';
        arrowEl.classList.add('arrow-left');
      }
      function placeBottom() {
        tooltipEl.style.left = Math.max(8, Math.min(rect.left + rect.width / 2 - tw / 2, window.innerWidth - tw - 8)) + 'px';
        tooltipEl.style.top = Math.min(rect.bottom + 16, window.innerHeight - th - 8) + 'px';
        arrowEl.classList.add('arrow-top');
      }
      function placeTop() {
        tooltipEl.style.left = Math.max(8, Math.min(rect.left + rect.width / 2 - tw / 2, window.innerWidth - tw - 8)) + 'px';
        tooltipEl.style.top = Math.max(8, rect.top - th - 16) + 'px';
        arrowEl.classList.add('arrow-bottom');
      }
      function placeLeft() {
        tooltipEl.style.left = Math.max(8, rect.left - tw - 16) + 'px';
        tooltipEl.style.top = Math.max(8, Math.min(rect.top + rect.height / 2 - th / 2, window.innerHeight - th - 8)) + 'px';
        arrowEl.classList.add('arrow-right');
      }

      // Mobile: prefer bottom/top placement (sides are usually too narrow)
      var order;
      if (isMobile) {
        order = ['bottom', 'top'];
      } else {
        var byRoom = [['right', spaceR], ['bottom', spaceB], ['top', spaceT], ['left', spaceL]];
        byRoom.sort(function (a, b) { return b[1] - a[1]; });
        order = [preferSide];
        byRoom.forEach(function (p) { if (order.indexOf(p[0]) === -1) order.push(p[0]); });
      }

      for (var i = 0; i < order.length; i++) {
        var side = order[i];
        if (side === 'right' && spaceR >= tw + 24) { placeRight(); return; }
        if (side === 'bottom' && spaceB >= th + 24) { placeBottom(); return; }
        if (side === 'top' && spaceT >= th + 24) { placeTop(); return; }
        if (side === 'left' && spaceL >= tw + 24) { placeLeft(); return; }
      }
      // Best-effort fallback: place on whichever side has most space and let it sit close
      var bestSide = isMobile
        ? (spaceB >= spaceT ? 'bottom' : 'top')
        : (Math.max(spaceR, spaceB, spaceT, spaceL) === spaceB ? 'bottom'
            : Math.max(spaceR, spaceB, spaceT, spaceL) === spaceT ? 'top'
            : Math.max(spaceR, spaceB, spaceT, spaceL) === spaceR ? 'right' : 'left');
      if (bestSide === 'right') placeRight();
      else if (bestSide === 'top') placeTop();
      else if (bestSide === 'left') placeLeft();
      else placeBottom();
    }

    function paintDots(i) {
      for (var d = 0; d < dotEls.length; d++) {
        dotEls[d].className = '';
        if (d < i) dotEls[d].classList.add('done');
        else if (d === i) dotEls[d].classList.add('current');
      }
    }

    // ----- Mobile drawer sync -----
    // On mobile (≤768px), the lesson sidebar is a slide-in drawer hidden
    // off-screen by default and only revealed when body has 'sidebar-open'.
    // The header nav is similarly hidden behind the hamburger button. The
    // tour highlights elements inside both — auto-manage the drawer state
    // so the target is actually visible when we paint the backdrop.
    function isInSidebar(el) { return !!(el && el.closest && el.closest('.lesson-sidebar')); }
    function isInHeaderNav(el) { return !!(el && el.closest && el.closest('.header-nav')); }
    function syncDrawerForTarget(target) {
      if (!isMobile) return;
      var inSidebar = isInSidebar(target);
      var inHeaderNav = isInHeaderNav(target);
      // Sidebar drawer
      var overlay = document.querySelector('.mobile-overlay');
      if (inSidebar) {
        document.body.classList.add('sidebar-open');
        if (overlay) overlay.classList.add('open');
      } else {
        document.body.classList.remove('sidebar-open');
        if (overlay) overlay.classList.remove('open');
      }
      // Header nav drawer
      var nav = document.querySelector('.header-nav');
      if (nav) {
        if (inHeaderNav) nav.classList.add('open');
        else nav.classList.remove('open');
      }
    }
    function closeAllDrawers() {
      if (!isMobile) return;
      document.body.classList.remove('sidebar-open');
      var overlay = document.querySelector('.mobile-overlay');
      if (overlay) overlay.classList.remove('open');
      var nav = document.querySelector('.header-nav');
      if (nav) nav.classList.remove('open');
    }

    var idx = 0;
    function finish(opts) {
      var skipToast = opts && opts.skipToast;
      tooltipEl.classList.remove('active');
      [backdropTop, backdropRight, backdropBottom, backdropLeft].forEach(function (el) { el.classList.remove('active'); });
      clearSpotlight();
      closeAllDrawers();
      try {
        localStorage.setItem('sv-lesson-tutorial-done', '1');
        if (highlightFeatureOn) localStorage.setItem('sv-highlight-tutorial-done', '1');
      } catch (e) {}
      setTimeout(function () {
        if (tooltipEl.parentNode) tooltipEl.parentNode.removeChild(tooltipEl);
        [backdropTop, backdropRight, backdropBottom, backdropLeft].forEach(function (el) {
          if (el.parentNode) el.parentNode.removeChild(el);
        });
      }, 350);
      window.removeEventListener('resize', repositionCurrent);
      window.removeEventListener('scroll', repositionCurrent, true);
      document.removeEventListener('keydown', onKey);
      // Scroll back to the top of the lesson so the student starts where
      // they would naturally read from. Smooth so it doesn't feel like a jump.
      try {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } catch (e) {
        window.scrollTo(0, 0);
      }
      // Toast — only when the student completes the tour, not when skipping
      if (!skipToast) {
        showTutorialToast('You\'re all set. Happy revising!');
      }
    }
    function repositionCurrent() {
      if (idx >= steps.length || !spotlightedEl) return;
      paintBackdrop(steps[idx].target);
      positionTooltip(steps[idx].target, steps[idx].side);
    }
    function onKey(e) {
      if (e.key === 'Escape') finish();
      else if (e.key === 'Enter' || e.key === 'ArrowRight') { e.preventDefault(); showStep(idx + 1); }
      else if (e.key === 'ArrowLeft' && idx > 0) { e.preventDefault(); showStep(idx - 1); }
    }
    function showStep(i) {
      idx = i;
      if (i >= steps.length) { finish(); return; }
      var step = steps[i];
      textEl.textContent = step.text;
      btnEl.textContent = (i === steps.length - 1) ? 'Got it' : 'Next';
      paintDots(i);
      tooltipEl.classList.remove('active');

      // Open / close mobile drawers so the target is actually on-screen
      // before we measure its rect. Drawer transitions take ~350ms (matches
      // the 380ms paint delay below).
      syncDrawerForTarget(step.target);

      // Scroll target into view (mobile especially benefits from `start` block)
      try {
        step.target.scrollIntoView({
          behavior: 'smooth',
          block: isMobile ? 'center' : 'center',
          inline: 'nearest'
        });
      } catch (e) {}

      setTimeout(function () {
        setSpotlight(step.target);
        paintBackdrop(step.target);
        positionTooltip(step.target, step.side);
        tooltipEl.classList.add('active');
      }, 380);
    }

    btnEl.addEventListener('click', function () { showStep(idx + 1); });
    skipEl.addEventListener('click', function () { finish({ skipToast: true }); });
    window.addEventListener('resize', repositionCurrent);
    window.addEventListener('scroll', repositionCurrent, true);
    document.addEventListener('keydown', onKey);

    showStep(0);
  }

  // ---- Tutorial completion toast ----
  function showTutorialToast(message) {
    // Remove any prior toast still hanging around
    var existing = document.getElementById('sv-tutorial-toast');
    if (existing) existing.remove();
    var toast = document.createElement('div');
    toast.id = 'sv-tutorial-toast';
    toast.textContent = message;
    toast.style.cssText =
      'position:fixed;bottom:2.5rem;left:50%;transform:translateX(-50%) translateY(8px);' +
      'background:#2d2a26;color:#fff;font-family:Inter,sans-serif;font-size:0.92rem;' +
      'font-weight:600;padding:0.85rem 1.4rem;border-radius:12px;' +
      'box-shadow:0 8px 32px rgba(45,42,38,0.22);z-index:9999;' +
      'opacity:0;transition:opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1),' +
      'transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);pointer-events:none;' +
      'max-width:calc(100vw - 2rem);text-align:center;';
    document.body.appendChild(toast);
    requestAnimationFrame(function () {
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
    });
    setTimeout(function () {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(-50%) translateY(8px)';
      setTimeout(function () { if (toast.parentNode) toast.remove(); }, 350);
    }, 3200);
  }

  // ---- Tour-replay button ----
  // Placed under the lesson checklist wherever it lives. On wide desktops
  // (≥1400px) the checklist is the fixed-position gutter on the left, so the
  // button goes inside the gutter as a small icon-only circle. On narrower
  // viewports the checklist is in the right sidebar — the button becomes a
  // full pill labelled "Show tour" right beneath that sidebar section.
  function isElVisible(el) {
    if (!el) return false;
    var s = window.getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') return false;
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }

  function addSidebarTourButton() {
    var gutter = document.querySelector('.gutter-progress');
    var sidebarProgress = document.querySelector('.sidebar-progress-section');
    var headerNav = document.getElementById('header-nav');

    // Clean any previous injection (could exist from a prior render)
    document.querySelectorAll('.sidebar-tour-section, .gutter-tour-btn, .header-tour-btn').forEach(function (el) { el.remove(); });

    if (isElVisible(gutter) && headerNav) {
      // Wide desktop — small icon button in the page header, alongside the
      // nav links. Keeps the gutter clean and the tour control discoverable.
      var btn = document.createElement('button');
      btn.id = 'replay-tour-btn';
      btn.type = 'button';
      btn.className = 'header-tour-btn';
      btn.title = 'Show the lesson tour again';
      btn.setAttribute('aria-label', 'Show the lesson tour again');
      btn.innerHTML =
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16">' +
          '<circle cx="12" cy="12" r="10"/><polyline points="10 8 16 12 10 16 10 8"/>' +
        '</svg>';
      headerNav.insertBefore(btn, headerNav.firstChild);
    } else if (sidebarProgress) {
      // Narrow — a full pill under the sidebar lesson-progress card
      var section = document.createElement('div');
      section.className = 'sidebar-section sidebar-tour-section';
      section.innerHTML =
        '<button type="button" class="sidebar-flashcard-link" id="replay-tour-btn">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;flex-shrink:0">' +
            '<circle cx="12" cy="12" r="10"/><polyline points="10 8 16 12 10 16 10 8"/>' +
          '</svg>' +
          '<span>Show tour</span>' +
        '</button>';
      sidebarProgress.parentNode.insertBefore(section, sidebarProgress.nextSibling);
    }
  }

  function wireReplayTourButton() {
    var btn = document.getElementById('replay-tour-btn');
    if (!btn || btn._wired) return;
    btn._wired = true;
    btn.addEventListener('click', function () {
      try { localStorage.removeItem('sv-lesson-tutorial-done'); } catch (e) {}
      maybeStartLessonTutorial();
    });
  }

  // ---- Lesson notice modal ----
  function showLessonNoticeModal(title, bodyHtml, lessonId) {
    var key = 'studyvault-lesson-notice-' + lessonId;
    try { if (sessionStorage.getItem(key) === 'dismissed') return; } catch (e) {}

    var overlay = document.createElement('div');
    overlay.className = 'lesson-notice-overlay';
    overlay.innerHTML =
      '<div class="lesson-notice-modal" role="dialog" aria-modal="true" aria-labelledby="lesson-notice-title">' +
        '<div class="lesson-notice-icon" aria-hidden="true">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
            '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>' +
          '</svg>' +
        '</div>' +
        '<h2 id="lesson-notice-title" class="lesson-notice-title">' + title + '</h2>' +
        '<div class="lesson-notice-body">' + bodyHtml + '</div>' +
        '<button type="button" class="lesson-notice-dismiss">Got it</button>' +
      '</div>';
    document.body.appendChild(overlay);

    function close() {
      overlay.classList.remove('active');
      try { sessionStorage.setItem(key, 'dismissed'); } catch (e) {}
      setTimeout(function () { if (overlay.parentNode) overlay.parentNode.removeChild(overlay); }, 250);
      document.removeEventListener('keydown', onKey);
    }
    function onKey(e) {
      if (e.key === 'Escape' || e.key === 'Enter') { e.preventDefault(); close(); }
    }
    overlay.querySelector('.lesson-notice-dismiss').addEventListener('click', close);
    document.addEventListener('keydown', onKey);

    requestAnimationFrame(function () {
      overlay.classList.add('active');
      var btn = overlay.querySelector('.lesson-notice-dismiss');
      if (btn) {
        try { btn.focus({ preventScroll: true }); }
        catch (e) { btn.focus(); }
      }
    });
  }

  // ---- Video modal (Google Drive) ----
  function openVideoModal(src, title, isDirectVideo) {
    // Create overlay if it doesn't exist yet
    var overlay = document.getElementById('video-modal-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'video-modal-overlay';
      overlay.className = 'video-modal-overlay';
      overlay.innerHTML =
        '<button class="video-modal-close" aria-label="Close">&times;</button>' +
        '<div class="video-modal-container"></div>';
      document.body.appendChild(overlay);

      overlay.querySelector('.video-modal-close').addEventListener('click', closeVideoModal);
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeVideoModal();
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && overlay.classList.contains('active')) closeVideoModal();
      });
    }

    var container = overlay.querySelector('.video-modal-container');

    if (isDirectVideo) {
      // Direct MP4/video: use native <video> element
      container.innerHTML =
        '<video class="video-modal-player" controls preload="metadata">' +
          '<source src="' + src + '" type="video/mp4">' +
          'Your browser does not support video playback.' +
        '</video>';
    } else {
      // Google Drive / YouTube: use iframe
      container.innerHTML =
        '<iframe class="video-modal-iframe" src="' + src + '" title="' + (title || 'Video overview') + '" allow="autoplay; fullscreen" allowfullscreen></iframe>';
    }

    requestAnimationFrame(function () {
      overlay.classList.add('active');
    });
  }

  function closeVideoModal() {
    var overlay = document.getElementById('video-modal-overlay');
    if (!overlay) return;
    overlay.classList.remove('active');
    // Stop playback after transition
    setTimeout(function () {
      var container = overlay.querySelector('.video-modal-container');
      container.innerHTML = '';
    }, 300);
  }

  // ---- Main ----
  async function init() {
    var params = parseUrl();
    if (!params) {
      showError('Invalid URL', 'The lesson URL format should be /lesson/{subject}/{unit}/{number}');
      return;
    }
    if (maybeRedirectOldHistorySlug(params.subjectSlug)) return;

    // Auth check (optional — for tracking, not gating)
    var user = await checkAuth();

    // Fetch lesson
    try {
      var data = await fetchLesson(params);

      if (data.error) {
        showError('Lesson not found', data.error);
        return;
      }

      renderLesson(data, params);
      recordVisit(user, data.lesson.id);
    } catch (err) {
      console.error('Lesson loader error:', err);
      showError('Something went wrong', 'Could not load the lesson. Please try again.');
    }
  }

  // Wait for DOM before init
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
