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
    try { var _a = JSON.parse(sessionStorage.getItem('studyvault-auth')) || JSON.parse(localStorage.getItem('studyvault-auth')); isStaff = _a && (_a.role === 'admin' || _a.role === 'teacher'); } catch(e) {}
    var hasBespoke = (typeof SchoolSession !== 'undefined' && SchoolSession.hasBespoke(params.subjectSlug));

    var unitQuery = sb
      .from('units')
      .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, exam_board, school_id)')
      .eq('slug', params.unitSlug)
      .eq('subjects.slug', params.subjectSlug);

    if (params.subjectId) {
      // Explicit subject ID from review dashboard — use it directly
      unitQuery = unitQuery.eq('subject_id', params.subjectId);
    } else if (isStaff) {
      // Staff: don't filter by school_id — try bespoke first, fall back to generic
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

    // Get prev/next lessons
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
    document.getElementById('nav-exam-technique').href = '/guide/' + subjectSlug + '/exam-technique';
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
    window._subjectSlug = params.subjectSlug;
    window._examBoard = subject.exam_board || '';

    // Extract podcast URL from related_media (if present)
    window.podcastUrl = null;
    var relMedia = lesson.related_media || [];
    for (var mi = 0; mi < relMedia.length; mi++) {
      if ((relMedia[mi].category || '').toLowerCase() === 'podcasts') {
        var items = relMedia[mi].items || [];
        for (var mj = 0; mj < items.length; mj++) {
          if (items[mj].title === 'Lesson Podcast' && items[mj].url && items[mj].url !== '#') {
            window.podcastUrl = items[mj].url;
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
      var subjectBase = params.subjectSlug.replace(/-(?:aqa|edexcel|ocr|eduqas)$/, '');
      var tier = tiers[params.subjectSlug] || tiers[subjectBase] || 'higher';
      if (tier === 'foundation') {
        document.body.classList.add('tier-foundation');
      }
    } catch(e) {}

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

    // Beta banner + report button for generic content (school_id NULL)
    if (!subject.school_id) {
      // Beta banner below the progress bar
      var progressBar = document.querySelector('.lesson-progress-inline-wrap') || document.querySelector('.lesson-progress-inline');
      var betaBanner = document.createElement('div');
      betaBanner.className = 'beta-banner';
      betaBanner.innerHTML = '<span class="beta-badge">BETA</span> This content is AI-generated from the exam specification. It has been verified against the spec but may contain errors.';
      var insertAfter = progressBar || document.querySelector('.lesson-header');
      if (insertAfter && insertAfter.parentNode) {
        insertAfter.parentNode.insertBefore(betaBanner, insertAfter.nextSibling);
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
      var categoryName = cat.category;
      var items = cat.items;

      // If lesson podcast is in the player tabs, rename category and filter it out
      if (hasPodcastTab && (categoryName || '').toLowerCase() === 'podcasts') {
        items = items.filter(function(item) { return item.title !== 'Lesson Podcast'; });
        if (items.length === 0) return; // skip empty category entirely
        categoryName = 'Other Podcasts';
      }

      html += '<div class="sidebar-collapsible">';
      html += '<button class="sidebar-collapsible-toggle" aria-expanded="false">';
      html += '<span>' + (cat.emoji ? cat.emoji + ' ' : '') + escapeHtml(categoryName) + '</span>';
      html += '<svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>';
      html += '</button>';
      html += '<div class="sidebar-collapsible-content">';

      items.forEach(function (item) {
        html += '<a href="' + escapeAttr(item.url) + '" target="_blank" rel="noopener noreferrer" class="sidebar-media-item">';
        html += '<strong>' + escapeHtml(item.title) + '</strong>';
        if (item.description) {
          html += '<span>' + escapeHtml(item.description) + '</span>';
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

  function escapeAttr(str) {
    return str.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
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
