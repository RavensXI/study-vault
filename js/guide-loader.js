/* ============================================
   StudyVault — Guide Loader
   Renders exam technique and revision technique pages from Supabase.
   Routes:
     /guide/{subject}/exam-technique           → hub index
     /guide/{subject}/exam-technique/{slug}     → individual guide
     /guide/{subject}/revision-technique        → hub index
     /guide/{subject}/revision-technique/{slug} → individual guide
   ============================================ */

(function () {
  'use strict';

  var sb = window.supabase.createClient(
    'https://baipckgywpnwapobwtsy.supabase.co',
    'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
  );

  var loadingEl = document.getElementById('guide-loading');
  var errorEl = document.getElementById('guide-error');
  var contentEl = document.getElementById('guide-content');

  // ---- Parse URL ----
  // /guide/{subject}/{guideType}
  // /guide/{subject}/{guideType}/{slug}
  function parseUrl() {
    var path = window.location.pathname;
    var match = path.match(/^\/guide\/([^/]+)\/(exam-technique|revision-technique)(?:\/([^/]+))?\/?$/);
    if (!match) return null;
    return {
      subjectSlug: match[1],
      guideType: match[2],
      slug: match[3] || null
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

  function showError(title, message) {
    loadingEl.style.display = 'none';
    document.getElementById('error-title').textContent = title;
    document.getElementById('error-message').textContent = message;
    errorEl.style.display = '';
  }

  function esc(str) {
    var div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
  }

  // ---- Build URLs ----
  function guideUrl(subjectSlug, guideType, slug) {
    if (slug) return '/guide/' + subjectSlug + '/' + guideType + '/' + slug;
    return '/guide/' + subjectSlug + '/' + guideType;
  }

  // ---- Render hub index page ----
  async function renderHub(params) {
    var subjectSlug = params.subjectSlug;
    var guideType = params.guideType;

    // Get the hub index page (slug = 'index')
    var subjectResult = await sb
      .from('subjects')
      .select('id, name')
      .eq('slug', subjectSlug)
      .single();

    if (subjectResult.error || !subjectResult.data) {
      showError('Subject not found', 'No subject "' + subjectSlug + '"');
      return;
    }

    var subject = subjectResult.data;

    var hubResult = await sb
      .from('guide_pages')
      .select('content_html, title')
      .eq('subject_id', subject.id)
      .eq('guide_type', guideType)
      .eq('slug', 'index')
      .single();

    if (hubResult.error || !hubResult.data) {
      showError('Hub not found', 'No ' + guideType + ' hub page found for ' + subjectSlug);
      return;
    }

    var isExam = guideType === 'exam-technique';
    var bodyClass = isExam ? 'unit-exam-technique' : 'unit-revision-technique';
    var label = isExam ? 'Exam Technique' : 'Revision Techniques';
    var otherType = isExam ? 'revision-technique' : 'exam-technique';
    var otherLabel = isExam ? 'Revision Techniques' : 'Exam Technique';

    document.title = label + ' - ' + subject.name + ' - StudyVault';
    document.body.classList.add(bodyClass);
    document.body.dataset.unit = guideType;
    document.getElementById('header-unit-label').textContent = label;

    // Nav
    var nav = document.getElementById('header-nav');
    nav.innerHTML = '<a href="/">Home</a>' +
      '<a href="/browse/' + subjectSlug + '">Unit Overview</a>' +
      '<a href="' + guideUrl(subjectSlug, otherType) + '">' + otherLabel + '</a>';

    // The hub content_html includes the unit-page-header, guide-hub, etc.
    contentEl.innerHTML = hubResult.data.content_html;
    loadingEl.style.display = 'none';
    contentEl.style.display = '';

    // Init nav icons on hub page
    if (typeof window.initNavIcons === 'function') window.initNavIcons();
    if (typeof window.initRevealAnimations === 'function') window.initRevealAnimations();

    // Rewrite any relative guide links to dynamic routes
    contentEl.querySelectorAll('a[href]').forEach(function (link) {
      var href = link.getAttribute('href');
      // Match relative links like "write-an-account.html" or "../revision-technique/retrieval-practice.html"
      if (href && !href.startsWith('http') && !href.startsWith('/') && !href.startsWith('#')) {
        if (href.endsWith('.html')) {
          var slug = href.replace('.html', '');
          // Check if it's a cross-reference to the other guide type
          if (slug.startsWith('../revision-technique/')) {
            slug = slug.replace('../revision-technique/', '');
            link.setAttribute('href', guideUrl(subjectSlug, 'revision-technique', slug));
          } else if (slug.startsWith('../exam-technique/')) {
            slug = slug.replace('../exam-technique/', '');
            link.setAttribute('href', guideUrl(subjectSlug, 'exam-technique', slug));
          } else {
            link.setAttribute('href', guideUrl(subjectSlug, guideType, slug));
          }
        }
      }
    });
  }

  // ---- Render individual guide page ----
  async function renderGuide(params) {
    var subjectSlug = params.subjectSlug;
    var guideType = params.guideType;
    var slug = params.slug;

    var subjectResult = await sb
      .from('subjects')
      .select('id, name')
      .eq('slug', subjectSlug)
      .single();

    if (subjectResult.error || !subjectResult.data) {
      showError('Subject not found', 'No subject "' + subjectSlug + '"');
      return;
    }

    var subject = subjectResult.data;

    var guideResult = await sb
      .from('guide_pages')
      .select('title, content_html')
      .eq('subject_id', subject.id)
      .eq('guide_type', guideType)
      .eq('slug', slug)
      .single();

    if (guideResult.error || !guideResult.data) {
      showError('Guide not found', 'No guide page "' + slug + '"');
      return;
    }

    var guide = guideResult.data;
    var isExam = guideType === 'exam-technique';
    var bodyClass = isExam ? 'unit-exam-technique' : 'unit-revision-technique';
    var label = isExam ? 'Exam Technique' : 'Revision Techniques';
    var otherType = isExam ? 'revision-technique' : 'exam-technique';
    var otherLabel = isExam ? 'Revision Techniques' : 'Exam Technique';

    document.title = guide.title + ' - ' + label + ' - StudyVault';
    document.body.classList.add(bodyClass);
    document.getElementById('header-unit-label').textContent = label;

    // Nav
    var nav = document.getElementById('header-nav');
    nav.innerHTML = '<a href="/">Home</a>' +
      '<a href="' + guideUrl(subjectSlug, guideType) + '">All Guides</a>' +
      '<a href="' + guideUrl(subjectSlug, otherType) + '">' + otherLabel + '</a>';

    // Init nav icons immediately after setting nav HTML
    if (typeof window.initNavIcons === 'function') window.initNavIcons();

    // Content already includes <main> + <aside> from the original .lesson-page
    var html = '<div class="lesson-page">';
    html += guide.content_html;
    html += '</div>';

    contentEl.innerHTML = html;
    loadingEl.style.display = 'none';
    contentEl.style.display = '';

    // Rewrite relative links
    contentEl.querySelectorAll('a[href]').forEach(function (link) {
      var href = link.getAttribute('href');
      if (href && !href.startsWith('http') && !href.startsWith('/') && !href.startsWith('#') && href.endsWith('.html')) {
        var target = href.replace('.html', '');
        if (target.startsWith('../revision-technique/')) {
          target = target.replace('../revision-technique/', '');
          link.setAttribute('href', guideUrl(subjectSlug, 'revision-technique', target));
        } else if (target.startsWith('../exam-technique/')) {
          target = target.replace('../exam-technique/', '');
          link.setAttribute('href', guideUrl(subjectSlug, 'exam-technique', target));
        } else {
          link.setAttribute('href', guideUrl(subjectSlug, guideType, target));
        }
      }
    });

    // Init collapsibles if any exist in the guide content
    if (typeof window.initLessonFeatures === 'function') {
      window.initLessonFeatures();
    }
    if (typeof window.initRevealAnimations === 'function') {
      window.initRevealAnimations();
    }
  }

  // ---- Main ----
  async function init() {
    var params = parseUrl();
    if (!params) {
      showError('Invalid URL', 'Guide URL format: /guide/{subject}/exam-technique/{slug}');
      return;
    }

    try {
      if (params.slug) {
        await renderGuide(params);
      } else {
        await renderHub(params);
      }
    } catch (err) {
      console.error('Guide loader error:', err);
      showError('Something went wrong', 'Could not load the guide. Please try again.');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
