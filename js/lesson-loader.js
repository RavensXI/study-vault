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
    return {
      subjectSlug: match[1],
      unitSlug: match[2],
      lessonNumber: parseInt(match[3], 10)
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
    // First, get the unit
    // Determine school scope: school students see their school's content, free users see generic
    var schoolId = (typeof SchoolSession !== 'undefined' && SchoolSession.isActive())
      ? SchoolSession.getSchoolId()
      : null;

    var unitQuery = sb
      .from('units')
      .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, exam_board, school_id)')
      .eq('slug', params.unitSlug)
      .eq('subjects.slug', params.subjectSlug);

    if (schoolId) {
      unitQuery = unitQuery.eq('subjects.school_id', schoolId);
    } else {
      unitQuery = unitQuery.is('subjects.school_id', null);
    }

    var unitResult = await unitQuery.single();

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
    document.body.classList.add(unit.body_class);
    document.body.dataset.unit = unit.slug;
    document.body.dataset.lesson = lesson.slug;

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
    document.getElementById('lesson-title').textContent = lesson.title;

    // Hero image
    if (lesson.hero_image_url) {
      var heroFig = document.getElementById('hero-figure');
      var heroImg = document.getElementById('hero-image');
      heroImg.src = lesson.hero_image_url;
      heroImg.alt = lesson.hero_image_alt || '';
      if (lesson.hero_image_position && lesson.hero_image_position !== 'center 50%') {
        heroImg.style.objectPosition = lesson.hero_image_position;
      }
      if (lesson.hero_image_caption) {
        document.getElementById('hero-caption').textContent = lesson.hero_image_caption;
      }
      heroFig.style.display = '';
    }

    // Content HTML
    document.getElementById('study-notes').innerHTML = lesson.content_html || '';

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
    if (lesson.youtube_video_id) {
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
          thumbHtml = '<div class="sidebar-video-thumb sidebar-video-thumb--generic"></div>';
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

    // Inject ad placeholders for free users only
    if (typeof FreeUser !== 'undefined' && FreeUser.isActive() && !SchoolSession.isActive()) {
      // Sidebar ad — below knowledge check, above video/media
      var sidebar = document.querySelector('.lesson-sidebar');
      var knowledgeCheck = document.querySelector('.sidebar-knowledge-check');
      if (sidebar && knowledgeCheck) {
        var sidebarAd = document.createElement('div');
        sidebarAd.className = 'ad-placeholder ad-placeholder--sidebar';
        sidebarAd.innerHTML = '<img src="/images/sample-ad-300x250.png" alt="Ad" style="width:100%;height:auto;border-radius:inherit;">';
        knowledgeCheck.insertAdjacentElement('afterend', sidebarAd);
      }
      // Inline ad — before the conclusion (inside study-notes content)
      var conclusion = document.querySelector('#study-notes .conclusion');
      if (conclusion) {
        var inlineAd = document.createElement('div');
        inlineAd.className = 'ad-placeholder ad-placeholder--inline';
        inlineAd.innerHTML = '<img src="/images/sample-ad-728x90.png" alt="Ad" style="width:100%;height:auto;border-radius:inherit;">';
        conclusion.parentElement.insertBefore(inlineAd, conclusion);
      }
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

    // Trigger scroll reveal animations on lesson content
    if (typeof window.initRevealAnimations === 'function') {
      window.initRevealAnimations();
    }

    // Render LaTeX equations via KaTeX (if loaded)
    if (typeof renderMathInElement === 'function') {
      renderMathInElement(document.getElementById('study-notes'), {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '\\[', right: '\\]', display: true },
          { left: '\\(', right: '\\)', display: false },
        ],
        throwOnError: false
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

    container.innerHTML = html;
  }

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
