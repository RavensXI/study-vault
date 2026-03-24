/* ============================================
   StudyVault v2 — main.js
   Scroll progress, collapsibles, visited tracking, mobile nav

   Phase 1: Runs on DOMContentLoaded — static elements always present
   Phase 2: initLessonFeatures() — called after dynamic content injection
            (by lesson-loader.js) OR immediately for static lesson pages
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
  // Phase 1 — always runs (static elements)
  initScrollProgress();
  initMobileNav();
  initAccessibility();
  initPageTransitions();
  initRevealAnimations();

  // Phase 2 — runs immediately if content is already in the page (static pages)
  // For dynamic pages, lesson-loader.js calls window.initLessonFeatures() after inject
  if (!document.getElementById('lesson-loading')) {
    initLessonFeatures();
  }
});

/**
 * Phase 2 init — call this after dynamic content has been injected into the DOM.
 * Safe to call on static pages too (all functions guard with early returns).
 */
function initLessonFeatures() {
  initCollapsibles();
  initVisitedTracking();
  initPracticeQuestions();
  initNarration();
  initGlossary();
  initLightbox();
  initHeroEdit();
  initKnowledgeCheck();
  initLessonNavBackSlot();
  initNavIcons();
  initRevisionTips();
  initLogoLink();
  initLessonPill();
  initLessonProgress();
  initFlashcardModal();
  initSidebarPanel();
}

// Expose globally for lesson-loader.js and guide-loader.js
window.initLessonFeatures = initLessonFeatures;
window.initNavIcons = initNavIcons;

/* --- Scroll Progress Bar + Header Elevation --- */
function initScrollProgress() {
  const bar = document.querySelector('.scroll-progress');
  const header = document.querySelector('.page-header');

  function updateProgress() {
    const scrollTop = window.scrollY;
    if (bar) {
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      bar.style.width = Math.min(pct, 100) + '%';
    }
    if (header) {
      header.classList.toggle('scrolled', scrollTop > 8);
    }
  }

  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();
}

/* --- Collapsible Sections --- */
function initCollapsibles() {
  var hintsKnown = !!localStorage.getItem('sv_collapsible_hint');

  document.querySelectorAll('.collapsible-toggle').forEach(btn => {
    // Inject hint + wrapper around icon if not already present
    var icon = btn.querySelector('.collapsible-icon');
    if (icon && !btn.querySelector('.collapsible-toggle-right')) {
      var wrapper = document.createElement('span');
      wrapper.className = 'collapsible-toggle-right';
      if (!hintsKnown) {
        var hint = document.createElement('span');
        hint.className = 'collapsible-hint';
        hint.textContent = 'Tap to expand';
        wrapper.appendChild(hint);
      }
      icon.parentNode.insertBefore(wrapper, icon);
      wrapper.appendChild(icon);
    }

    btn.addEventListener('click', () => {
      const section = btn.closest('.collapsible');
      const content = section.querySelector('.collapsible-content');
      const isOpen = section.classList.contains('open');

      if (isOpen) {
        // Collapse: set explicit height first for smooth animation
        content.style.maxHeight = content.scrollHeight + 'px';
        content.offsetHeight; // force reflow
        content.style.maxHeight = '0';
        section.classList.remove('open');
      } else {
        // Expand
        section.classList.add('open');
        content.style.maxHeight = content.scrollHeight + 'px';
        // After transition, allow dynamic height
        const onEnd = () => {
          if (section.classList.contains('open')) {
            content.style.maxHeight = 'none';
          }
          content.removeEventListener('transitionend', onEnd);
        };
        content.addEventListener('transitionend', onEnd);

        // After first expand, hide all hints and remember
        if (!localStorage.getItem('sv_collapsible_hint')) {
          localStorage.setItem('sv_collapsible_hint', '1');
          document.querySelectorAll('.collapsible-hint').forEach(h => {
            h.classList.add('sv-hint-hidden');
          });
        }
      }

      // Update aria
      const expanded = section.classList.contains('open');
      btn.setAttribute('aria-expanded', expanded);
    });
  });

  // Sidebar collapsibles (Related Media)
  document.querySelectorAll('.sidebar-collapsible-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const section = btn.closest('.sidebar-collapsible');
      const content = section.querySelector('.sidebar-collapsible-content');
      const isOpen = section.classList.contains('open');

      if (isOpen) {
        content.style.maxHeight = content.scrollHeight + 'px';
        content.offsetHeight;
        content.style.maxHeight = '0';
        section.classList.remove('open');
      } else {
        section.classList.add('open');
        content.style.maxHeight = content.scrollHeight + 'px';
        const onEnd = () => {
          if (section.classList.contains('open')) {
            content.style.maxHeight = 'none';
            const sidebar = section.closest('.lesson-sidebar');
            if (sidebar) {
              const sidebarRect = sidebar.getBoundingClientRect();
              const sectionRect = section.getBoundingClientRect();
              const sectionBottomInScroll = sectionRect.bottom - sidebarRect.top + sidebar.scrollTop;
              const visibleBottom = sidebar.scrollTop + sidebar.clientHeight;
              if (sectionBottomInScroll > visibleBottom - 16) {
                sidebar.scrollTo({ top: sectionBottomInScroll - sidebar.clientHeight + 16, behavior: 'smooth' });
              }
            }
          }
          content.removeEventListener('transitionend', onEnd);
        };
        content.addEventListener('transitionend', onEnd);
      }

      btn.setAttribute('aria-expanded', section.classList.contains('open'));
    });
  });
}

/* --- Visited Lesson Tracking (localStorage) --- */
function initVisitedTracking() {
  const unitSlug = document.body.dataset.unit;
  const lessonSlug = document.body.dataset.lesson;

  // If we're on a lesson page, mark it visited
  if (unitSlug && lessonSlug) {
    markVisited(unitSlug, lessonSlug);
  }

  // If we're on a unit contents page, highlight visited lessons
  if (document.querySelector('.lesson-grid')) {
    updateVisitedCards();
  }

  // If we're on the homepage, update progress bars
  if (document.querySelector('.unit-grid')) {
    updateHomepageProgress();
  }
}

function getVisited() {
  return JSON.parse(localStorage.getItem('studyvault-visited') || '{}');
}

function markVisited(unit, lesson) {
  const visited = getVisited();
  if (!visited[unit]) visited[unit] = [];
  if (!visited[unit].includes(lesson)) {
    visited[unit].push(lesson);
    localStorage.setItem('studyvault-visited', JSON.stringify(visited));
  }
}

function updateVisitedCards() {
  const visited = getVisited();
  const unitSlug = document.body.dataset.unit;
  if (!unitSlug) return;

  const unitVisited = visited[unitSlug] || [];

  document.querySelectorAll('.lesson-card[data-lesson]').forEach(card => {
    if (unitVisited.includes(card.dataset.lesson)) {
      card.classList.add('visited');
    }
  });

  // Update unit progress bar
  const totalCards = document.querySelectorAll('.lesson-card:not(.coming-soon)').length;
  const visitedCount = unitVisited.length;
  const progressLabel = document.querySelector('.unit-progress-label');
  const progressFill = document.querySelector('.progress-bar-fill');

  if (progressLabel) {
    progressLabel.textContent = visitedCount + ' of ' + totalCards + ' lessons visited';
  }
  if (progressFill && totalCards > 0) {
    progressFill.style.width = Math.round((visitedCount / totalCards) * 100) + '%';
  }
}

function updateHomepageProgress() {
  const visited = getVisited();

  document.querySelectorAll('.unit-card[data-unit]').forEach(card => {
    const unit = card.dataset.unit;
    const total = parseInt(card.dataset.totalLessons, 10) || 0;
    const unitVisited = (visited[unit] || []).length;
    const pct = total > 0 ? Math.round((unitVisited / total) * 100) : 0;

    const fill = card.querySelector('.progress-bar-fill');
    const meta = card.querySelector('.unit-meta');

    if (fill) fill.style.width = pct + '%';
    if (meta) meta.textContent = unitVisited + ' of ' + total + ' lessons visited';
  });
}

/* --- Practice Questions --- */
function initPracticeQuestions() {
  const questions = window.practiceQuestions;
  if (!questions || questions.length === 0) return;

  const textEl = document.getElementById('practice-text');
  const typeEl = document.getElementById('practice-type');
  const marksEl = document.getElementById('practice-marks');
  const newBtn = document.getElementById('practice-new');
  const answerEl = document.getElementById('practice-answer');
  const aiBtn = document.getElementById('practice-ai-mark');
  const sendBtn = document.getElementById('practice-send');
  const toast = document.getElementById('practice-toast');

  if (!textEl) return;

  let currentIndex = -1;

  function getGuideUrl(type) {
    if (!type) return null;
    var guides = [
      // History (AQA) — subject-specific, matched first
      ['Describe two', 'describe-two.html'],
      ['Write an account', 'write-an-account.html'],
      ['Explain the significance', 'explain-significance.html'],
      ['Explain what was important', 'explain-significance.html'],
      ['Explain two similarities', 'explain-similarities.html'],
      ['In what ways', 'in-what-ways.html'],
      ['Which had more impact', 'which-had-more-impact.html'],
      ['How far do you agree', 'factor-essay.html'],
      ['Has ', 'factor-essay.html'],
      // Drama (OCR) — subject-specific
      ['Costume', 'costume-design.html'],
      ['Voice', 'voice-skills.html'],
      ['Physicality', 'physicality.html'],
      ['Movement', 'physicality.html'],
      ['Staging', 'staging.html'],
      ['Lighting', 'design.html'],
      ['Sound', 'design.html'],
      ['Director', 'director.html'],
      ['Set Design', 'set-design.html'],
      ['Section B', 'section-b-essay.html'],
      // Food Technology (AQA 8585)
      ['1 mark \u2014 Define', 'define-1-mark.html'],
      ['2 marks \u2014 Name', 'name-identify-2-marks.html'],
      ['2 marks \u2014 Identify', 'name-identify-2-marks.html'],
      ['4 marks \u2014 Explain', 'explain-4-marks.html'],
      ['6 marks \u2014 Explain', 'explain-6-marks.html'],
      ['8 marks \u2014 Discuss', 'discuss-8-marks.html'],
      // Religious Education (AQA 8062) — 2026 exam types
      ['1 mark \u2014 Multiple Choice', 'multiple-choice-1-mark.html'],
      ['1 mark \u2014 Give/Name', 'give-name-1-mark.html'],
      ['4 marks \u2014 Explain Influence', 'explain-influence-4-marks.html'],
      ['4 marks \u2014 Explain Similarities & Differences', 'explain-similarities-differences-4-marks.html'],
      ['6 marks \u2014 Explain with Sources', 'explain-sources-6-marks.html'],
      ['12 marks \u2014 Evaluate a Statement', 'evaluate-statement-12-marks.html'],
      // English Literature (AQA 8702)
      ['Quote Analysis', 'quote-analysis.html'],
      ['Extract Analysis', 'extract-analysis.html'],
      ['Extended Response', 'extended-response.html'],
      ['Essay with SPaG', 'essay-response.html'],
      ['Anthology Comparison', 'anthology-comparison.html'],
      ['Unseen Poetry Analysis', 'unseen-poetry-analysis.html'],
      ['Unseen Poetry Comparison', 'unseen-poetry-comparison.html'],
      // English Language (AQA 8700)
      ['4 marks — Retrieval', 'retrieval.html'],
      ['8 marks — Language Analysis', 'language-analysis.html'],
      ['8 marks — Structure Analysis', 'structure-analysis.html'],
      ['8 marks — Summary', 'summary.html'],
      ['16 marks — Comparison', 'comparison.html'],
      ['20 marks — Evaluation', 'evaluation.html'],
      ['40 marks — Creative Writing', 'creative-writing.html'],
      ['40 marks — Transactional Writing', 'transactional-writing.html'],
      // Music (Eduqas C660U)
      ['Multiple Choice', 'multiple-choice.html'],
      ['Identification', 'identification.html'],
      ['Short Feature Identification', 'short-feature-identification.html'],
      ['Extended Listening Response', 'extended-listening-response.html'],
      ['Prepared Extract', 'prepared-extract.html'],
      // AQA Science (Combined + Separate)
      ['1 mark \u2014 Recall', 'recall-1-mark.html'],
      ['2 marks \u2014 Describe', 'describe-2-marks.html'],
      ['2 marks \u2014 Calculate', 'calculate-2-marks.html'],
      ['3 marks \u2014 Explain', 'explain-3-marks.html'],
      ['4 marks \u2014 Compare', 'compare-and-explain-4-marks.html'],
      ['6 marks \u2014 Extended', 'extended-response-6-marks.html'],
      // Generic — matched last
      ['Define', 'define.html'],
      ['Outline', 'outline.html'],
      ['Explain one way', 'explain.html'],
      ['Calculate', 'calculate.html'],
      ['Analyse', 'analyse.html'],
      ['Discuss', 'discuss.html'],
      ['Justify', 'justify-evaluate.html'],
      ['Evaluate', 'justify-evaluate.html'],
      ['Identify', 'identify-state.html'],
      ['State', 'identify-state.html'],
      ['Extended response', 'extended-response.html'],
      ['Extended Explanation', 'director.html'],
      ['Describe', 'describe.html'],
      ['Explain', 'explain.html']
    ];

    // Detect if running on dynamic route (/lesson/...) or static (subject/unit/lesson-NN.html)
    var isDynamic = /^\/lesson\//.test(location.pathname);
    var subjectSlug = '';
    if (isDynamic) {
      var parts = location.pathname.split('/');
      subjectSlug = parts[2] || ''; // /lesson/{subject}/...
    }

    for (var i = 0; i < guides.length; i++) {
      if (type.indexOf(guides[i][0]) !== -1) {
        var slug = guides[i][1].replace('.html', '');
        if (isDynamic) {
          return '/guide/' + subjectSlug + '/exam-technique/' + slug;
        }
        return '../exam-technique/' + guides[i][1];
      }
    }
    return null;
  }

  function showQuestion() {
    // Pick a random question different from current
    let idx;
    do {
      idx = Math.floor(Math.random() * questions.length);
    } while (idx === currentIndex && questions.length > 1);
    currentIndex = idx;

    const q = questions[currentIndex];
    typeEl.textContent = q.type;
    var existingTag = typeEl.parentNode.querySelector('.practice-past-paper-tag');
    if (existingTag) existingTag.remove();
    var existingGuide = typeEl.parentNode.querySelector('.practice-guide-link');
    if (existingGuide) existingGuide.remove();
    if (q.pastPaper) {
      var tag = document.createElement('span');
      tag.className = 'practice-past-paper-tag';
      tag.textContent = 'Past paper';
      typeEl.after(tag);
    }
    var guideUrl = getGuideUrl(q.type);
    if (guideUrl) {
      var guideLink = document.createElement('a');
      guideLink.className = 'practice-guide-link';
      guideLink.href = guideUrl;
      guideLink.target = '_blank';
      guideLink.rel = 'noopener noreferrer';
      guideLink.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>How do I answer this?';
      var insertAfter = typeEl.parentNode.querySelector('.practice-past-paper-tag') || typeEl;
      insertAfter.after(guideLink);
    }
    textEl.textContent = q.text;
    marksEl.innerHTML = formatMarkScheme(q.marks);
    marksEl.style.display = 'none'; // hide mark scheme initially
    answerEl.value = '';
  }

  function formatMarkScheme(raw) {
    // Escape HTML
    const esc = raw.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // Split into paragraphs on double newline
    const blocks = esc.split(/\n\n+/);

    let html = '';
    blocks.forEach(block => {
      block = block.trim();
      if (!block) return;

      // Level headings
      if (/^Level\s+\d/i.test(block)) {
        // Split into heading line and the rest
        const lines = block.split('\n');
        const heading = lines[0];
        const rest = lines.slice(1).join('\n');

        // Extract level number and marks
        const match = heading.match(/^(Level\s+\d)\s*\(([^)]+)\):\s*(.*)/i);
        if (match) {
          html += '<div class="ms-level">';
          html += '<div class="ms-level-header"><span class="ms-level-num">' + match[1] + '</span><span class="ms-level-marks">' + match[2] + '</span></div>';
          html += '<p class="ms-level-desc">' + match[3] + '</p>';
        } else {
          html += '<div class="ms-level">';
          html += '<p class="ms-level-desc">' + heading + '</p>';
        }

        // Handle example lines
        if (rest) {
          const examples = rest.split(/\n(?=Example)/);
          examples.forEach(ex => {
            ex = ex.trim();
            if (ex.startsWith('Example')) {
              const colonIdx = ex.indexOf(':');
              if (colonIdx > -1) {
                const label = ex.substring(0, colonIdx + 1);
                const content = ex.substring(colonIdx + 1).trim();
                html += '<div class="ms-example"><span class="ms-example-label">' + label + '</span> ' + content + '</div>';
              } else {
                html += '<div class="ms-example">' + ex + '</div>';
              }
            } else {
              html += '<p class="ms-level-desc">' + ex + '</p>';
            }
          });
        }

        html += '</div>';
      } else if (/^0\s+marks/i.test(block)) {
        html += '<div class="ms-zero">' + block + '</div>';
      } else if (/^SPaG/i.test(block)) {
        html += '<div class="ms-spag"><strong>SPaG:</strong> ' + block.replace(/^SPaG:\s*/i, '') + '</div>';
      } else if (/^All historically/i.test(block)) {
        html += '<div class="ms-preamble">' + block + '</div>';
      } else {
        html += '<p>' + block + '</p>';
      }
    });

    return html;
  }

  function showToast(message, duration) {
    toast.textContent = message;
    toast.classList.add('visible');
    setTimeout(() => toast.classList.remove('visible'), duration || 3000);
  }

  // Load first question
  showQuestion();

  // New question button
  newBtn.addEventListener('click', showQuestion);

  // AI Mark — copies prompt to clipboard
  aiBtn.addEventListener('click', () => {
    const answer = answerEl.value.trim();
    if (!answer) {
      showToast('Write an answer first!');
      return;
    }

    const q = questions[currentIndex];
    const lessonTitle = document.querySelector('.lesson-header h1');
    const prompt =
      'You are an AQA GCSE History examiner. Mark the following student answer.\n\n' +
      'TOPIC: ' + (lessonTitle ? lessonTitle.textContent : 'Conflict & Tension') + '\n\n' +
      'QUESTION (' + q.type + '):\n' + q.text + '\n\n' +
      'MARK SCHEME GUIDANCE:\n' + q.marks + '\n\n' +
      'STUDENT ANSWER:\n' + answer + '\n\n' +
      'Please provide:\n' +
      '1. A mark out of ' + q.type.match(/\d+/)[0] + (q.type.includes('SPaG') ? ' (plus SPaG out of 4)' : '') + '\n' +
      '2. What the student did well (with specific quotes from their answer)\n' +
      '3. What could be improved (with specific suggestions)\n' +
      '4. A model paragraph showing how to improve the weakest part of their answer';

    navigator.clipboard.writeText(prompt).then(() => {
      showToast('Copied! Paste into ChatGPT or Claude to get your mark.');
    }).catch(() => {
      // Fallback: select a hidden textarea
      const ta = document.createElement('textarea');
      ta.value = prompt;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      showToast('Copied! Paste into ChatGPT or Claude to get your mark.');
    });
  });

  // Send to teacher — try mailto, fallback to clipboard
  sendBtn.addEventListener('click', () => {
    const answer = answerEl.value.trim();
    if (!answer) {
      showToast('Write an answer first!');
      return;
    }

    const q = questions[currentIndex];
    const lessonTitle = document.querySelector('.lesson-header h1');
    const teacherEmail = 't.shaun@unity.lancs.sch.uk';
    const subjectText = 'StudyVault Answer: ' + (lessonTitle ? lessonTitle.textContent : 'Practice Question');
    const bodyText = 'Question (' + q.type + '):\n' + q.text + '\n\nMy Answer:\n' + answer;

    // Copy to clipboard first (always works)
    const clipboardText = 'To: ' + teacherEmail + '\nSubject: ' + subjectText + '\n\n' + bodyText;
    navigator.clipboard.writeText(clipboardText).catch(() => {
      const ta = document.createElement('textarea');
      ta.value = clipboardText;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    });

    // Try opening mailto
    const mailtoUrl = 'mailto:' + teacherEmail +
      '?subject=' + encodeURIComponent(subjectText) +
      '&body=' + encodeURIComponent(bodyText);
    window.location.href = mailtoUrl;

    // Show toast with fallback instructions
    showToast('Answer copied! If email didn\u2019t open, paste it into an email to ' + teacherEmail, 5000);
  });

  // Toggle mark scheme on click
  marksEl.addEventListener('click', () => {
    marksEl.style.display = 'none';
  });

  // Show/hide mark scheme
  const showMarksLink = document.createElement('button');
  showMarksLink.className = 'practice-show-marks';
  showMarksLink.textContent = 'Show mark scheme';
  showMarksLink.addEventListener('click', () => {
    const visible = marksEl.style.display !== 'none';
    marksEl.style.display = visible ? 'none' : 'block';
    showMarksLink.textContent = visible ? 'Show mark scheme' : 'Hide mark scheme';
  });
  marksEl.parentNode.insertBefore(showMarksLink, marksEl);
}

/* --- Mobile Navigation --- */
function initMobileNav() {
  const btn = document.querySelector('.mobile-menu-btn');
  const nav = document.querySelector('.header-nav');
  const overlay = document.querySelector('.mobile-overlay');
  if (!btn || !nav) return;

  // --- Default (non-lesson) mobile nav ---
  function toggleMenu() {
    // If sidebar panel mode is active, skip default nav toggle
    if (document.body.classList.contains('sidebar-panel-mode')) return;
    const isOpen = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', isOpen);
    if (overlay) overlay.classList.toggle('open', isOpen);
  }

  function closeMenu() {
    if (document.body.classList.contains('sidebar-panel-mode')) return;
    nav.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
    if (overlay) overlay.classList.remove('open');
  }

  btn.addEventListener('click', toggleMenu);

  if (overlay) {
    overlay.addEventListener('click', closeMenu);
  }

  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && nav.classList.contains('open')) {
      closeMenu();
    }
  });
}

/* --- Sidebar Panel (mobile lesson pages) --- */
function initSidebarPanel() {
  var sidebar = document.querySelector('.lesson-sidebar');
  if (!sidebar) return; // Not a lesson page

  var btn = document.querySelector('.mobile-menu-btn');
  var overlay = document.querySelector('.mobile-overlay');
  var nav = document.querySelector('.header-nav');
  if (!btn) return;

  // Check if we are at mobile breakpoint
  var mql = window.matchMedia('(max-width: 768px)');
  var panelReady = false;

  function setupPanel() {
    if (panelReady) return;
    panelReady = true;

    // Add panel-mode class to body
    document.body.classList.add('sidebar-panel-mode');

    // Create close button + title at top of sidebar
    var closeRow = document.createElement('div');
    closeRow.className = 'sidebar-panel-close';
    closeRow.innerHTML =
      '<span class="sidebar-panel-close-title">Lesson Tools</span>' +
      '<button class="sidebar-panel-close-btn" aria-label="Close panel">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
          '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>' +
        '</svg>' +
      '</button>';
    sidebar.insertBefore(closeRow, sidebar.firstChild);

    // Create nav links section from the header nav
    var panelNav = document.createElement('div');
    panelNav.className = 'sidebar-panel-nav';
    var headerLinks = nav ? nav.querySelectorAll('a') : [];
    var navIcons = {
      'Home': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
      'Unit Overview': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
      'Exam Technique': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
      'Revision Techniques': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/></svg>'
    };
    headerLinks.forEach(function (a) {
      // Skip hidden prev/next lesson links and lesson pill
      if (a.style.display === 'none' || a.classList.contains('nav-lesson-pill')) return;
      var clone = document.createElement('a');
      clone.href = a.href;
      clone.textContent = a.textContent.trim();
      var icon = navIcons[clone.textContent] || '';
      if (icon) clone.innerHTML = icon + '<span>' + clone.textContent + '</span>';
      clone.addEventListener('click', function () { closeSidebar(); });
      panelNav.appendChild(clone);
    });
    // Insert nav after close button
    sidebar.insertBefore(panelNav, closeRow.nextSibling);

    // Close button handler
    closeRow.querySelector('.sidebar-panel-close-btn').addEventListener('click', closeSidebar);

    // Swipe-to-close support
    var touchStartX = 0;
    var touchStartY = 0;
    var swiping = false;

    sidebar.addEventListener('touchstart', function (e) {
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
      swiping = true;
    }, { passive: true });

    sidebar.addEventListener('touchmove', function (e) {
      if (!swiping) return;
      var dx = e.touches[0].clientX - touchStartX;
      var dy = Math.abs(e.touches[0].clientY - touchStartY);
      // If mostly horizontal swipe to the right (> 60px, angle < 30deg)
      if (dx > 60 && dy < dx * 0.6) {
        closeSidebar();
        swiping = false;
      }
    }, { passive: true });

    sidebar.addEventListener('touchend', function () {
      swiping = false;
    }, { passive: true });
  }

  function teardownPanel() {
    if (!panelReady) return;
    panelReady = false;
    document.body.classList.remove('sidebar-panel-mode', 'sidebar-open');
    var closeRow = sidebar.querySelector('.sidebar-panel-close');
    if (closeRow) closeRow.remove();
    var panelNav = sidebar.querySelector('.sidebar-panel-nav');
    if (panelNav) panelNav.remove();
  }

  function openSidebar() {
    document.body.classList.add('sidebar-open');
    btn.setAttribute('aria-expanded', 'true');
    if (overlay) overlay.classList.add('open');
  }

  function closeSidebar() {
    document.body.classList.remove('sidebar-open');
    btn.setAttribute('aria-expanded', 'false');
    if (overlay) overlay.classList.remove('open');
    // Also close the header nav in case it was open
    if (nav) nav.classList.remove('open');
  }

  function handleToggle() {
    if (!panelReady) return; // Let default nav handler run
    if (document.body.classList.contains('sidebar-open')) {
      closeSidebar();
    } else {
      openSidebar();
    }
  }

  // Override the hamburger click on lesson pages at mobile breakpoint
  btn.addEventListener('click', function () {
    if (panelReady) {
      handleToggle();
    }
  });

  // Overlay closes panel
  if (overlay) {
    overlay.addEventListener('click', function () {
      if (panelReady) closeSidebar();
    });
  }

  // Escape key closes panel
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panelReady && document.body.classList.contains('sidebar-open')) {
      closeSidebar();
    }
  });

  // React to breakpoint changes
  function onBreakpoint(e) {
    if (e.matches) {
      setupPanel();
    } else {
      teardownPanel();
    }
  }

  if (mql.matches) setupPanel();
  if (mql.addEventListener) {
    mql.addEventListener('change', onBreakpoint);
  } else if (mql.addListener) {
    mql.addListener(onBreakpoint);
  }

  // Expose close for other code
  window._closeSidebarPanel = closeSidebar;
}

/* --- Narration Player --- */
function initNarration() {
  var playerEl = document.querySelector('.narration-player');
  if (!playerEl) return;

  var audio = playerEl.querySelector('.narration-audio');
  var playBtn = playerEl.querySelector('.narration-play');
  var progressFill = playerEl.querySelector('.narration-progress-fill');
  var progressBar = playerEl.querySelector('.narration-progress');
  var timeEl = playerEl.querySelector('.narration-time');
  var speedBtn = playerEl.querySelector('.narration-speed');

  if (!audio) return;

  // Manifest: [{ id: "n1", src: "narration_n1.wav", duration: 14.2 }, ...]
  var manifest = window.narrationManifest || [];
  if (!manifest.length || !manifest[0].src) return;

  // Calculate total duration and cumulative start offsets
  var totalDuration = 0;
  var offsets = [];
  for (var i = 0; i < manifest.length; i++) {
    offsets.push(totalDuration);
    totalDuration += manifest[i].duration;
  }
  if (totalDuration === 0) return;

  var currentIndex = -1;
  var activeChunk = null;
  var speeds = [1, 1.25, 1.5, 0.75];
  var speedIndex = 0;
  var isPlaying = false;
  var autoScrollEnabled = true;
  var lastProgrammaticScroll = 0;

  // --- Podcast tab support ---
  var podcastUrl = window.podcastUrl || null;
  var playerMode = 'narration'; // 'narration' or 'podcast'
  var tabBar = document.querySelector('.audio-player-tabs');
  var podcastDuration = 0;

  if (podcastUrl && tabBar) {
    tabBar.style.display = '';
    var tabs = tabBar.querySelectorAll('.audio-tab');
    var tabTrack = tabBar.querySelector('.audio-tab-track');
    tabs.forEach(function(tab) {
      tab.addEventListener('click', function() {
        var mode = tab.dataset.mode;
        if (mode === playerMode) return;

        // Stop current playback
        audio.pause();
        clearHighlight();
        isPlaying = false;
        playBtn.classList.remove('playing');
        playBtn.setAttribute('aria-label', 'Play ' + mode);

        // Switch active tab + slide indicator
        tabs.forEach(function(t) { t.classList.remove('active'); });
        tab.classList.add('active');
        tabTrack.classList.toggle('podcast-active', mode === 'podcast');
        playerMode = mode;

        if (mode === 'podcast') {
          // Switch to single-file podcast mode
          audio.src = podcastUrl;
          audio.load();
          currentIndex = -1;
          progressFill.style.width = '0%';
          timeEl.textContent = '0:00 / 0:00';
          speedBtn.textContent = speeds[speedIndex] + 'x';
        } else {
          // Switch back to narration mode
          audio.src = '';
          currentIndex = -1;
          progressFill.style.width = '0%';
          timeEl.textContent = '0:00 / ' + fmtTime(totalDuration);
        }
      });
    });
  }

  // --- Floating mini-player ---
  var fab = document.createElement('div');
  fab.className = 'narration-fab';
  fab.innerHTML =
    '<button class="narration-fab-play" aria-label="Pause narration">' +
      '<svg class="narration-icon-play" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>' +
      '<svg class="narration-icon-pause" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>' +
    '</button>' +
    '<div class="narration-fab-progress"><div class="narration-fab-progress-fill"></div></div>' +
    '<span class="narration-fab-time">0:00</span>';
  document.body.appendChild(fab);

  var fabPlay = fab.querySelector('.narration-fab-play');
  var fabFill = fab.querySelector('.narration-fab-progress-fill');
  var fabTime = fab.querySelector('.narration-fab-time');
  var mainPlayerVisible = true;
  var audioStarted = false;

  var observer = new IntersectionObserver(function(entries) {
    mainPlayerVisible = entries[0].isIntersecting;
    fab.classList.toggle('visible', !mainPlayerVisible && audioStarted);
  }, { threshold: 0 });
  observer.observe(playerEl);

  // --- Helpers ---

  function fmtTime(s) {
    var m = Math.floor(s / 60);
    var sec = Math.floor(s % 60);
    return m + ':' + (sec < 10 ? '0' : '') + sec;
  }

  function globalTime() {
    if (currentIndex < 0) return 0;
    return offsets[currentIndex] + (audio.currentTime || 0);
  }

  function loadClip(index) {
    if (index < 0 || index >= manifest.length) return false;
    currentIndex = index;
    audio.src = manifest[index].src;
    audio.playbackRate = speeds[speedIndex];
    // Preload next clip for gapless transition
    if (index + 1 < manifest.length) {
      var preload = new Audio();
      preload.src = manifest[index + 1].src;
      preload.preload = 'auto';
    }
    return true;
  }

  function startPlayback() {
    if (currentIndex < 0) loadClip(0);
    audio.play();
  }

  function isInViewport(el) {
    var rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight && rect.bottom > 0;
  }

  function doAutoScroll(el) {
    lastProgrammaticScroll = Date.now();
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function setHighlight(chunkId) {
    if (chunkId === activeChunk) return;

    // Remove old highlight
    if (activeChunk) {
      var oldEl = document.querySelector('[data-narration-id="' + activeChunk + '"]');
      if (oldEl) oldEl.classList.remove('narration-active');
    }

    var newEl = null;
    var newCollapsible = null;
    if (chunkId) {
      newEl = document.querySelector('[data-narration-id="' + chunkId + '"]');
      if (newEl) newCollapsible = newEl.closest('.collapsible');
    }

    // Remove shimmer from any collapsible that isn't the current one
    document.querySelectorAll('.collapsible.narration-reading').forEach(function(el) {
      if (el !== newCollapsible) el.classList.remove('narration-reading');
    });

    if (newEl) {
      if (newCollapsible && !newCollapsible.classList.contains('open')) {
        // Content is collapsed — shimmer the collapsible toggle
        if (!newCollapsible.classList.contains('narration-reading')) {
          newCollapsible.classList.add('narration-reading');
        }
        if (autoScrollEnabled) {
          var toggle = newCollapsible.querySelector('.collapsible-toggle');
          if (toggle) {
            var rect = toggle.getBoundingClientRect();
            if (rect.top < 80 || rect.bottom > window.innerHeight - 80) {
              doAutoScroll(toggle);
            }
          }
        }
      } else {
        newEl.classList.add('narration-active');
        if (autoScrollEnabled) {
          var rect = newEl.getBoundingClientRect();
          if (rect.top < 80 || rect.bottom > window.innerHeight - 80) {
            doAutoScroll(newEl);
          }
        }
      }
    }

    activeChunk = chunkId;
  }

  function clearHighlight() {
    if (activeChunk) {
      var el = document.querySelector('[data-narration-id="' + activeChunk + '"]');
      if (el) el.classList.remove('narration-active');
      activeChunk = null;
    }
    document.querySelectorAll('.collapsible.narration-reading').forEach(function(el) {
      el.classList.remove('narration-reading');
    });
  }

  // --- Play / Pause ---

  playBtn.addEventListener('click', function() {
    if (playerMode === 'podcast') {
      if (audio.paused) { audio.play(); } else { audio.pause(); }
    } else {
      if (audio.paused) { startPlayback(); } else { audio.pause(); }
    }
  });

  fabPlay.addEventListener('click', function() {
    if (playerMode === 'podcast') {
      if (audio.paused) { audio.play(); } else { audio.pause(); }
    } else {
      if (audio.paused) { startPlayback(); } else { audio.pause(); }
    }
  });

  audio.addEventListener('play', function() {
    isPlaying = true;
    audioStarted = true;
    playBtn.classList.add('playing');
    playBtn.setAttribute('aria-label', 'Pause ' + playerMode);
    fabPlay.classList.add('playing');
    fab.classList.toggle('visible', !mainPlayerVisible);
    if (playerMode === 'narration' && currentIndex >= 0) setHighlight(manifest[currentIndex].id);
  });

  audio.addEventListener('pause', function() {
    isPlaying = false;
    playBtn.classList.remove('playing');
    playBtn.setAttribute('aria-label', 'Play narration');
    fabPlay.classList.remove('playing');
  });

  // --- Progress ---

  audio.addEventListener('timeupdate', function() {
    if (playerMode === 'podcast') {
      var dur = audio.duration || 0;
      var cur = audio.currentTime || 0;
      var pct = dur > 0 ? (cur / dur * 100) + '%' : '0%';
      progressFill.style.width = pct;
      if (progressBar) progressBar.style.setProperty('--progress-pct', pct);
      timeEl.textContent = fmtTime(cur) + ' / ' + fmtTime(dur);
      fabFill.style.width = pct;
      fabTime.textContent = fmtTime(cur);
    } else {
      var gt = globalTime();
      var pct = (gt / totalDuration * 100) + '%';
      progressFill.style.width = pct;
      if (progressBar) progressBar.style.setProperty('--progress-pct', pct);
      timeEl.textContent = fmtTime(gt) + ' / ' + fmtTime(totalDuration);
      fabFill.style.width = pct;
      fabTime.textContent = fmtTime(gt);
    }
  });

  // --- Clip ended — advance or finish ---

  audio.addEventListener('ended', function() {
    if (playerMode === 'podcast') {
      // Podcast is a single file — just reset
      isPlaying = false;
      progressFill.style.width = '100%';
      playBtn.classList.remove('playing');
      playBtn.setAttribute('aria-label', 'Play podcast');
      fabPlay.classList.remove('playing');
      fab.classList.remove('visible');
    } else if (currentIndex + 1 < manifest.length) {
      loadClip(currentIndex + 1);
      audio.play();
    } else {
      isPlaying = false;
      audioStarted = false;
      currentIndex = -1;
      clearHighlight();
      progressFill.style.width = '100%';
      playBtn.classList.remove('playing');
      playBtn.setAttribute('aria-label', 'Play narration');
      fabPlay.classList.remove('playing');
      fab.classList.remove('visible');
    }
  });

  // --- Progress bar seek (podcast mode) ---

  progressBar.addEventListener('click', function(e) {
    if (playerMode !== 'podcast') return;
    var rect = progressBar.getBoundingClientRect();
    var pct = (e.clientX - rect.left) / rect.width;
    if (audio.duration) {
      audio.currentTime = pct * audio.duration;
    }
  });
  progressBar.style.cursor = 'pointer';

  // --- Speed toggle ---

  speedBtn.addEventListener('click', function() {
    speedIndex = (speedIndex + 1) % speeds.length;
    audio.playbackRate = speeds[speedIndex];
    speedBtn.textContent = speeds[speedIndex] + 'x';
  });

  // --- Click paragraph to jump to that clip (desktop only) ---

  var isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  if (!isTouchDevice) {
    document.querySelectorAll('[data-narration-id]').forEach(function(el) {
      el.addEventListener('click', function(e) {
        // Don't hijack glossary term clicks or work in podcast mode
        if (e.target.closest('dfn, .glossary-popup')) return;
        if (playerMode === 'podcast') return;
        var id = el.dataset.narrationId;
        for (var i = 0; i < manifest.length; i++) {
          if (manifest[i].id === id) { loadClip(i); audio.play(); break; }
        }
      });
    });
  }

  // --- Collapsible re-highlight ---

  document.querySelectorAll('.collapsible-toggle').forEach(function(toggle) {
    toggle.addEventListener('click', function() {
      if (activeChunk && isPlaying) {
        var current = activeChunk;
        activeChunk = null;
        setHighlight(current);
      }
    });
  });

  // --- Auto-scroll suppression ---

  window.addEventListener('scroll', function() {
    if (!isPlaying) return;
    if (Date.now() - lastProgrammaticScroll < 1000) return;
    if (activeChunk) {
      var el = document.querySelector('[data-narration-id="' + activeChunk + '"]');
      if (el) autoScrollEnabled = isInViewport(el);
    }
  }, { passive: true });

  // --- Keyboard: Space to play/pause ---

  document.addEventListener('keydown', function(e) {
    var tag = e.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || e.target.isContentEditable) return;
    if (e.code === 'Space') {
      e.preventDefault();
      if (audio.paused) { startPlayback(); } else { audio.pause(); }
    }
  });
}

/* --- Accessibility Toolbar --- */
function initAccessibility() {
  const toolbar = document.querySelector('.a11y-toolbar');
  if (!toolbar) return;

  const dyslexiaBtn = toolbar.querySelector('.a11y-dyslexia-toggle');
  const overlayBtns = toolbar.querySelectorAll('.a11y-overlay');
  const STORAGE_KEY = 'studyvault-a11y';

  // Load saved preferences
  function loadPrefs() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch (e) {
      return {};
    }
  }

  function savePrefs(prefs) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
  }

  // Apply dyslexia font
  function setDyslexia(on) {
    document.body.classList.toggle('dyslexia-font', on);
    if (dyslexiaBtn) dyslexiaBtn.setAttribute('aria-pressed', on);
    const prefs = loadPrefs();
    prefs.dyslexia = on;
    savePrefs(prefs);
  }

  // Apply overlay colour
  function setOverlay(colour) {
    // Remove any existing overlay class
    document.body.className = document.body.className
      .replace(/\boverlay-\S+/g, '')
      .trim();

    if (colour) {
      document.body.classList.add('overlay-' + colour);
    }

    // Update active state on buttons
    overlayBtns.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.overlay === colour);
    });

    const prefs = loadPrefs();
    prefs.overlay = colour;
    savePrefs(prefs);
  }

  // Dark mode
  const darkBtn = toolbar.querySelector('.a11y-dark-toggle');

  function setDarkMode(on) {
    document.body.classList.toggle('dark-mode', on);
    if (darkBtn) darkBtn.setAttribute('aria-pressed', on);
    const prefs = loadPrefs();
    prefs.darkMode = on;
    savePrefs(prefs);
  }

  // Font size
  const fontDownBtn = toolbar.querySelector('.a11y-font-down');
  const fontUpBtn = toolbar.querySelector('.a11y-font-up');
  const fontSizes = [-1, 0, 1, 2]; // step indices
  let fontSizeStep = 0;

  function setFontSize(step) {
    // Remove existing font-size classes
    document.body.className = document.body.className
      .replace(/\bfont-size-\S+/g, '')
      .trim();

    fontSizeStep = Math.max(-1, Math.min(2, step));
    if (fontSizeStep === -1) document.body.classList.add('font-size-down-1');
    else if (fontSizeStep === 1) document.body.classList.add('font-size-up-1');
    else if (fontSizeStep === 2) document.body.classList.add('font-size-up-2');

    const prefs = loadPrefs();
    prefs.fontSize = fontSizeStep;
    savePrefs(prefs);
  }

  // Event listeners
  if (dyslexiaBtn) {
    dyslexiaBtn.addEventListener('click', () => {
      const isOn = document.body.classList.contains('dyslexia-font');
      setDyslexia(!isOn);
    });
  }

  if (darkBtn) {
    darkBtn.addEventListener('click', () => {
      const isOn = document.body.classList.contains('dark-mode');
      setDarkMode(!isOn);
    });
  }

  if (fontDownBtn) {
    fontDownBtn.addEventListener('click', () => setFontSize(fontSizeStep - 1));
  }

  if (fontUpBtn) {
    fontUpBtn.addEventListener('click', () => setFontSize(fontSizeStep + 1));
  }

  overlayBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      setOverlay(btn.dataset.overlay);
    });
  });

  // Restore saved preferences on page load
  const prefs = loadPrefs();
  if (prefs.dyslexia) setDyslexia(true);
  if (prefs.darkMode) setDarkMode(true);
  if (typeof prefs.fontSize === 'number') setFontSize(prefs.fontSize);
  if (prefs.overlay) setOverlay(prefs.overlay);
  else setOverlay(''); // mark "none" as active
}

/* --- Glossary Tooltips --- */
function initGlossary() {
  const terms = document.querySelectorAll('.term');
  if (!terms.length) return;

  // Build popup elements
  terms.forEach(term => {
    const popup = document.createElement('span');
    popup.className = 'term-popup';
    popup.textContent = term.dataset.def;
    term.appendChild(popup);
  });

  let activeTerm = null;

  function showTerm(term) {
    if (activeTerm && activeTerm !== term) hideTerm(activeTerm);

    const rects = term.getClientRects();
    const rect = term.getBoundingClientRect();
    const popup = term.querySelector('.term-popup');
    // For wrapped inline elements, absolute positioning is relative to the
    // first line fragment, not the bounding box — use that as our reference
    const refLeft = rects.length > 1 ? rects[0].left : rect.left;

    // Vertical: flip below if near top of viewport
    term.classList.toggle('term-flip', rect.top < 100);

    // Horizontal: position popup within content area
    if (popup) {
      // Reset to default positioning first so we can measure natural width
      popup.style.left = '';
      popup.style.transform = '';

      // Temporarily make visible to measure, then position
      popup.style.visibility = 'hidden';
      popup.style.opacity = '1';
      popup.style.pointerEvents = 'none';
      const popupWidth = popup.offsetWidth;
      popup.style.visibility = '';
      popup.style.opacity = '';
      popup.style.pointerEvents = '';

      // Centre over the term (or first fragment if wrapped), clamp to content area
      const contentEl = term.closest('.lesson-content') || term.closest('main') || document.body;
      const contentRight = contentEl.getBoundingClientRect().right;
      const anchorRect = rects.length > 1 ? rects[0] : rect;
      const termCentre = anchorRect.left + anchorRect.width / 2;
      let popupLeft = termCentre - popupWidth / 2;
      popupLeft = Math.max(8, Math.min(popupLeft, contentRight - popupWidth - 8));

      popup.style.left = (popupLeft - refLeft) + 'px';
      popup.style.transform = 'none';
      term.classList.add('term-visible');
    } else {
      term.classList.add('term-visible');
    }

    activeTerm = term;
  }

  function hideTerm(term) {
    term.classList.remove('term-visible', 'term-flip');
    const popup = term.querySelector('.term-popup');
    if (popup) {
      popup.style.left = '';
      popup.style.right = '';
      popup.style.transform = '';
    }
    if (activeTerm === term) activeTerm = null;
  }

  terms.forEach(term => {
    // Touch: tap to toggle (for phones, tablets, touchscreen laptops)
    var touchMoved = false;
    term.addEventListener('touchstart', () => { touchMoved = false; }, { passive: true });
    term.addEventListener('touchmove', () => { touchMoved = true; }, { passive: true });
    term.addEventListener('touchend', (e) => {
      if (touchMoved) return; // was a scroll, not a tap
      e.preventDefault();
      if (term.classList.contains('term-visible')) {
        hideTerm(term);
      } else {
        showTerm(term);
      }
    });

    // Mouse: hover to show, click to toggle (always bind — touchscreen laptops have mice too)
    term.addEventListener('mouseenter', () => showTerm(term));
    term.addEventListener('mouseleave', () => hideTerm(term));
    term.addEventListener('click', (e) => {
      e.preventDefault();
      if (term.classList.contains('term-visible')) {
        hideTerm(term);
      } else {
        showTerm(term);
      }
    });
  });

  // Close on tap elsewhere
  var isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  document.addEventListener(isTouch ? 'touchend' : 'click', (e) => {
    if (activeTerm && !e.target.closest('.term')) {
      hideTerm(activeTerm);
    }
  });
}

/* --- Image Lightbox --- */
function initLightbox() {
  const imgs = document.querySelectorAll('.diagram img, .lesson-hero-image img');
  if (!imgs.length) return;

  // Create overlay once
  const overlay = document.createElement('div');
  overlay.className = 'lightbox-overlay';
  overlay.innerHTML = '<button class="lightbox-close" aria-label="Close">&times;</button><img src="" alt="">';
  document.body.appendChild(overlay);

  const lbImg = overlay.querySelector('img');

  function open(src, alt) {
    lbImg.src = src;
    lbImg.alt = alt;
    requestAnimationFrame(() => overlay.classList.add('active'));
  }

  function close() {
    overlay.classList.remove('active');
  }

  imgs.forEach(img => {
    img.addEventListener('click', () => open(img.src, img.alt));
  });

  overlay.addEventListener('click', (e) => {
    if (e.target !== lbImg) close();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay.classList.contains('active')) close();
  });
}

/* --- Hero Image Position Editor (add ?hero-edit to URL) --- */
function initHeroEdit() {
  if (!new URLSearchParams(window.location.search).has('hero-edit')) return;

  const imgs = document.querySelectorAll('.lesson-hero-image img');
  if (!imgs.length) return;

  // Inject styles
  const style = document.createElement('style');
  style.textContent = `
    .hero-edit-active .lesson-hero-image { position: relative; cursor: grab; }
    .hero-edit-active .lesson-hero-image:active { cursor: grabbing; }
    .hero-edit-label {
      position: absolute; top: 0.5rem; left: 0.5rem; z-index: 100;
      background: rgba(0,0,0,0.75); color: #fff; font: 600 14px/1 monospace;
      padding: 0.35rem 0.6rem; border-radius: 6px; pointer-events: none;
      user-select: none;
    }
    .hero-edit-panel {
      position: fixed; bottom: 1rem; right: 1rem; z-index: 9999;
      background: #1a1a1a; color: #eee; font: 13px/1.5 monospace;
      padding: 1rem 1.25rem; border-radius: 12px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.3); max-width: 380px;
    }
    .hero-edit-panel h4 { margin: 0 0 0.5rem; font-size: 14px; color: #fff; }
    .hero-edit-panel p { margin: 0.2rem 0; font-size: 12px; color: #aaa; }
    .hero-edit-panel button {
      margin-top: 0.75rem; padding: 0.4rem 0.8rem; border: none;
      background: var(--accent, #2563eb); color: #fff; border-radius: 6px;
      font: 600 13px/1 system-ui; cursor: pointer;
    }
    .hero-edit-panel button:hover { filter: brightness(1.15); }
    .hero-edit-panel .hero-edit-output {
      margin-top: 0.5rem; padding: 0.5rem; background: #111; border-radius: 6px;
      font-size: 11px; white-space: pre; max-height: 200px; overflow-y: auto;
      user-select: all;
    }
  `;
  document.head.appendChild(style);
  document.body.classList.add('hero-edit-active');

  // Panel
  const panel = document.createElement('div');
  panel.className = 'hero-edit-panel';
  panel.innerHTML = '<h4>Hero Position Editor</h4>' +
    '<p>Drag images up/down to reposition.</p>' +
    '<button class="hero-edit-copy">Copy values</button>' +
    '<div class="hero-edit-output" style="display:none"></div>';
  document.body.appendChild(panel);

  const output = panel.querySelector('.hero-edit-output');
  const copyBtn = panel.querySelector('.hero-edit-copy');

  // Get current Y% from an img's object-position
  function getYPct(img) {
    const pos = img.style.objectPosition || getComputedStyle(img).objectPosition || 'center center';
    const parts = pos.trim().split(/\s+/);
    const yStr = parts.length > 1 ? parts[1] : parts[0];
    const val = parseFloat(yStr);
    return isNaN(val) ? 50 : val;
  }

  imgs.forEach(img => {
    const figure = img.closest('.lesson-hero-image');

    // Label
    const label = document.createElement('div');
    label.className = 'hero-edit-label';
    label.textContent = 'Y: ' + getYPct(img).toFixed(0) + '%';
    figure.appendChild(label);

    let dragging = false;
    let startY = 0;
    let startPct = 0;

    function onStart(e) {
      e.preventDefault();
      dragging = true;
      startY = e.type.startsWith('touch') ? e.touches[0].clientY : e.clientY;
      startPct = getYPct(img);
    }

    function onMove(e) {
      if (!dragging) return;
      const clientY = e.type.startsWith('touch') ? e.touches[0].clientY : e.clientY;
      const delta = clientY - startY;
      // Dragging down → image shifts up (lower %) ; dragging up → image shifts down (higher %)
      // Sensitivity: ~0.3% per pixel
      const newPct = Math.max(0, Math.min(100, startPct - delta * 0.3));
      img.style.objectPosition = 'center ' + newPct.toFixed(1) + '%';
      label.textContent = 'Y: ' + newPct.toFixed(0) + '%';
    }

    function onEnd() {
      dragging = false;
    }

    figure.addEventListener('mousedown', onStart);
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onEnd);
    figure.addEventListener('touchstart', onStart, { passive: false });
    window.addEventListener('touchmove', onMove, { passive: true });
    window.addEventListener('touchend', onEnd);
  });

  copyBtn.addEventListener('click', () => {
    let text = '';
    imgs.forEach(img => {
      const src = img.getAttribute('src') || '';
      const lesson = src.replace('-hero.jpg', '').replace('lesson-', 'Lesson ');
      text += lesson + ': center ' + getYPct(img).toFixed(0) + '%\n';
    });
    output.textContent = text.trim();
    output.style.display = 'block';
    navigator.clipboard.writeText(text.trim()).catch(() => {});
  });
}

/* --- Page Transitions --- */
function initPageTransitions() {
  // Clear the page-enter animation after it finishes so that
  // transform: translateY(0) doesn't persist on <body>.
  // Any transform on body breaks position:fixed descendants (lightbox, mini-player, etc.)
  document.body.addEventListener('animationend', (e) => {
    if (e.animationName === 'page-enter') {
      document.body.style.opacity = '1';
      document.body.style.animation = 'none';
    }
  });

  document.addEventListener('click', (e) => {
    const link = e.target.closest('a[href]');
    if (!link) return;

    const href = link.getAttribute('href');

    // Skip external links, anchors, new-tab links, and special protocols
    if (!href || href.startsWith('#') || href.startsWith('http') ||
        href.startsWith('mailto:') || href.startsWith('tel:') ||
        link.target === '_blank' || e.ctrlKey || e.metaKey || e.shiftKey) return;

    e.preventDefault();
    document.body.classList.add('page-exit');

    // Navigate after exit animation completes
    setTimeout(() => { window.location.href = href; }, 200);
  });
}

/* --- Scroll Reveal Animations --- */
function initRevealAnimations() {
  // Collect all elements that need reveal animation
  var els = Array.prototype.slice.call(document.querySelectorAll('.sv-reveal'));

  // Lesson page elements (content blocks, sidebar, hero, sections)
  var lessonSelectors = [
    '.lesson-header .lesson-number',
    '.lesson-header h1',
    '.lesson-hero-image',
    '.study-notes > h2',
    '.study-notes > p',
    '.study-notes > .key-fact',
    '.study-notes > .collapsible',
    '.study-notes > .timeline',
    '.study-notes > figure.diagram',
    '.study-notes > blockquote',
    '.study-notes > ul',
    '.study-notes > ol',
    '.lesson-sidebar',
    '.exam-tip',
    '.conclusion',
    '.practice-section',
    '.lesson-nav',
    '.narration-player',
    '.guide-hub .guide-card'
  ];

  lessonSelectors.forEach(function (sel) {
    var matches = document.querySelectorAll(sel);
    matches.forEach(function (el) {
      // Only add if not already visible (avoid re-animating on re-init)
      if (!el.classList.contains('sv-visible')) els.push(el);
    });
  });

  if (!els.length) return;

  // If user prefers reduced motion, show everything immediately
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    els.forEach(function (el) { el.classList.add('sv-visible'); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('sv-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

  els.forEach(function (el) { observer.observe(el); });
}
// Expose globally so loaders can call after injecting content
window.initRevealAnimations = initRevealAnimations;

/* --- Knowledge Check Quiz --- */
function initKnowledgeCheck() {
  const btn = document.getElementById('knowledge-check-btn');
  const questions = window.knowledgeCheck;
  if (!btn || !questions || !questions.length) return;

  const unit = document.body.dataset.unit || 'unknown';
  const lesson = document.body.dataset.lesson || 'unknown';
  const storageKey = 'studyvault-kc-' + unit + '/' + lesson;

  // Show saved score on button
  const scoreEl = document.getElementById('knowledge-check-score');
  const saved = localStorage.getItem(storageKey);
  if (saved && scoreEl) scoreEl.textContent = saved;

  btn.addEventListener('click', () => openKnowledgeCheck(questions, storageKey, scoreEl));
}

function openKnowledgeCheck(questions, storageKey, scoreEl) {
  let current = 0;
  let score = 0;

  const overlay = document.createElement('div');
  overlay.className = 'kc-overlay';
  overlay.innerHTML =
    '<div class="kc-modal">' +
      '<div class="kc-header">' +
        '<span class="kc-title">Quick Quiz</span>' +
        '<span class="kc-step" id="kc-step"></span>' +
      '</div>' +
      '<div class="kc-body" id="kc-body"></div>' +
      '<div class="kc-footer" id="kc-footer"></div>' +
    '</div>';

  document.body.appendChild(overlay);

  overlay.addEventListener('click', (e) => { if (e.target === overlay) closeKC(); });
  const onKey = (e) => { if (e.key === 'Escape') closeKC(); };
  document.addEventListener('keydown', onKey);

  function closeKC() {
    document.removeEventListener('keydown', onKey);
    overlay.remove();
  }

  function getBody() { return overlay.querySelector('#kc-body'); }
  function getFooter() { return overlay.querySelector('#kc-footer'); }

  function addNextBtn(isCorrect) {
    const isLast = current === questions.length - 1;
    const footer = getFooter();
    footer.querySelector('.kc-btn-primary').style.display = 'none';
    const nextBtn = document.createElement('button');
    nextBtn.className = 'kc-btn kc-btn-primary';
    nextBtn.textContent = isLast ? 'See results' : 'Next';
    nextBtn.addEventListener('click', () => {
      current++;
      current < questions.length ? showQuestion() : showResult();
    });
    footer.appendChild(nextBtn);
    // Delay focus to prevent Enter key bleed-through
    setTimeout(() => nextBtn.focus(), 50);
  }

  function showQuestion() {
    const q = questions[current];
    overlay.querySelector('#kc-step').textContent = (current + 1) + ' / ' + questions.length;

    switch (q.type) {
      case 'mcq': renderMCQ(q); break;
      case 'fill': renderFill(q); break;
      case 'match': renderMatch(q); break;
    }
  }

  // --- Multiple Choice ---
  function renderMCQ(q) {
    const body = getBody();
    const footer = getFooter();
    let selected = -1;

    body.innerHTML = '<p class="kc-question">' + q.q + '</p><div class="kc-options" id="kc-options"></div>';
    footer.innerHTML = '<button class="kc-btn kc-btn-primary" id="kc-check" disabled>Check</button>';

    const grid = body.querySelector('#kc-options');
    q.options.forEach((opt, i) => {
      const btn = document.createElement('button');
      btn.className = 'kc-option';
      btn.textContent = opt;
      btn.addEventListener('click', () => {
        if (btn.classList.contains('locked')) return;
        grid.querySelectorAll('.kc-option').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selected = i;
        footer.querySelector('#kc-check').disabled = false;
      });
      grid.appendChild(btn);
    });

    footer.querySelector('#kc-check').addEventListener('click', () => {
      if (selected < 0) return;
      grid.querySelectorAll('.kc-option').forEach(b => b.classList.add('locked'));
      const correct = selected === q.correct;
      grid.children[selected].classList.add(correct ? 'correct' : 'incorrect');
      if (!correct) grid.children[q.correct].classList.add('correct');
      if (correct) score++;
      addNextBtn(correct);
    });
  }

  // --- Fill in the Blank ---
  function renderFill(q) {
    const body = getBody();
    const footer = getFooter();
    let selected = -1;

    const sentence = q.q.replace('_____', '<span class="kc-blank" id="kc-blank">?</span>');
    body.innerHTML = '<p class="kc-question kc-fill-sentence">' + sentence + '</p><div class="kc-fill-options" id="kc-fill-opts"></div>';
    footer.innerHTML = '<button class="kc-btn kc-btn-primary" id="kc-check" disabled>Check</button>';

    const opts = body.querySelector('#kc-fill-opts');
    // Shuffle option order for display
    const indices = q.options.map((_, i) => i);
    for (let i = indices.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const t = indices[i]; indices[i] = indices[j]; indices[j] = t;
    }

    indices.forEach(i => {
      const btn = document.createElement('button');
      btn.className = 'kc-fill-btn';
      btn.textContent = q.options[i];
      btn.addEventListener('click', () => {
        if (btn.classList.contains('locked')) return;
        opts.querySelectorAll('.kc-fill-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selected = i;
        body.querySelector('#kc-blank').textContent = q.options[i];
        body.querySelector('#kc-blank').classList.add('filled');
        footer.querySelector('#kc-check').disabled = false;
      });
      opts.appendChild(btn);
    });

    footer.querySelector('#kc-check').addEventListener('click', () => {
      if (selected < 0) return;
      opts.querySelectorAll('.kc-fill-btn').forEach(b => b.classList.add('locked'));
      const correct = selected === q.correct;
      const blank = body.querySelector('#kc-blank');
      blank.classList.add(correct ? 'correct' : 'incorrect');
      opts.querySelectorAll('.kc-fill-btn').forEach(b => {
        const idx = q.options.indexOf(b.textContent);
        if (idx === q.correct) b.classList.add('correct');
        else if (b.classList.contains('selected') && !correct) b.classList.add('incorrect');
      });
      if (correct) score++;
      addNextBtn(correct);
    });
  }

  // --- Match Up ---
  function renderMatch(q) {
    const body = getBody();
    const footer = getFooter();

    body.innerHTML = '<p class="kc-question">' + q.q + '</p><div class="kc-match" id="kc-match"></div>';
    footer.innerHTML = '<button class="kc-btn kc-btn-primary" id="kc-check" disabled>Check</button>';

    const container = body.querySelector('#kc-match');

    // Shuffle right-side options
    const shuffled = q.right.map((r, i) => ({ text: r, idx: i }));
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const t = shuffled[i]; shuffled[i] = shuffled[j]; shuffled[j] = t;
    }

    q.left.forEach((left, i) => {
      const row = document.createElement('div');
      row.className = 'kc-match-row';
      const label = document.createElement('span');
      label.className = 'kc-match-left';
      label.textContent = left;
      const sel = document.createElement('select');
      sel.className = 'kc-match-select';
      sel.innerHTML = '<option value="">Select\u2026</option>';
      shuffled.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.idx;
        opt.textContent = s.text;
        sel.appendChild(opt);
      });
      sel.addEventListener('change', checkAllSelected);
      row.appendChild(label);
      row.appendChild(sel);
      container.appendChild(row);
    });

    function checkAllSelected() {
      const selects = container.querySelectorAll('.kc-match-select');
      const allFilled = Array.from(selects).every(s => s.value !== '');
      footer.querySelector('#kc-check').disabled = !allFilled;
    }

    footer.querySelector('#kc-check').addEventListener('click', () => {
      const selects = container.querySelectorAll('.kc-match-select');
      let allCorrect = true;
      selects.forEach((sel, i) => {
        sel.disabled = true;
        const row = sel.closest('.kc-match-row');
        if (parseInt(sel.value) === q.order[i]) {
          row.classList.add('correct');
        } else {
          row.classList.add('incorrect');
          allCorrect = false;
        }
      });
      if (allCorrect) score++;
      addNextBtn(allCorrect);
    });
  }

  function showResult() {
    const body = getBody();
    const footer = getFooter();
    overlay.querySelector('#kc-step').textContent = 'Done';

    const total = questions.length;
    const pct = Math.round(score / total * 100);
    let msg = '';
    if (pct === 100) msg = 'Perfect recall. You know this topic.';
    else if (pct >= 60) msg = 'Solid effort. Review what you missed and try again.';
    else msg = 'Read through the lesson and give it another go.';

    body.innerHTML =
      '<div class="kc-result">' +
        '<div class="kc-result-score">' + score + '/' + total + '</div>' +
        '<div class="kc-result-label">' + pct + '% correct</div>' +
        '<p class="kc-result-msg">' + msg + '</p>' +
      '</div>';
    footer.innerHTML =
      '<button class="kc-btn kc-btn-secondary" id="kc-retry">Try again</button>' +
      '<button class="kc-btn kc-btn-primary" id="kc-close">Close</button>';

    const scoreStr = score + '/' + total;
    const prev = localStorage.getItem(storageKey);
    const prevScore = prev ? parseInt(prev) : 0;
    if (score >= prevScore) {
      localStorage.setItem(storageKey, scoreStr);
      if (scoreEl) scoreEl.textContent = scoreStr;
    }

    overlay.querySelector('#kc-close').addEventListener('click', closeKC);
    overlay.querySelector('#kc-retry').addEventListener('click', () => {
      current = 0;
      score = 0;
      showQuestion();
    });
  }

  showQuestion();
}

/* --- Lesson Nav: move back-link into empty grid slot --- */
function initLessonNavBackSlot() {
  var lessonNav = document.querySelector('.lesson-nav');
  if (!lessonNav) return;
  var prev = lessonNav.querySelector('.lesson-nav-link--prev');
  var next = lessonNav.querySelector('.lesson-nav-link--next');
  var backLink = lessonNav.nextElementSibling;
  if (!backLink || !backLink.classList.contains('back-link')) return;
  if (!prev && next) {
    backLink.style.gridColumn = '1';
    backLink.style.alignSelf = 'center';
    backLink.style.marginTop = '0';
    lessonNav.prepend(backLink);
  } else if (prev && !next) {
    backLink.style.gridColumn = '2';
    backLink.style.justifySelf = 'end';
    backLink.style.alignSelf = 'center';
    backLink.style.marginTop = '0';
    lessonNav.appendChild(backLink);
  }
}

/* --- Nav Icons --- */
function initNavIcons() {
  var navLinks = document.querySelectorAll('.header-nav a');
  var icons = {
    'Exam Technique': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
    'Revision Techniques': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/></svg>'
  };
  var classes = {
    'Exam Technique': 'nav-exam-technique',
    'Revision Techniques': 'nav-revision-techniques'
  };
  navLinks.forEach(function (link) {
    if (link.querySelector('.nav-icon')) return; // already initialised
    var text = link.textContent.trim();
    if (icons[text]) {
      var span = document.createElement('span');
      span.className = 'nav-icon';
      span.innerHTML = icons[text];
      link.prepend(span);
    }
    if (classes[text]) {
      link.classList.add(classes[text]);
    }
    if (/Previous Lesson|Next Lesson/.test(text)) {
      link.classList.add('nav-lesson-pill');
    }
  });
}

/* --- Logo Link → Root Dashboard --- */
function initLogoLink() {
  var brand = document.querySelector('.header-brand');
  if (!brand) return;
  // Dynamic routes already have href="/" in the template.
  // Static pages with data-unit are 2 levels deep — update to root.
  if (document.body.dataset.unit && !location.pathname.startsWith('/lesson/')) {
    brand.setAttribute('href', '../../index.html');
  }
}

/* --- Lesson Pill (header) --- */
function initLessonPill() {
  // Support both static (lesson-01.html) and dynamic (/lesson/.../1) URLs
  var match = location.pathname.match(/lesson-0*(\d+)\.html/) ||
              location.pathname.match(/\/lesson\/[^/]+\/[^/]+\/(\d+)/);
  if (!match) return;
  // Skip if pill already exists (e.g. added by lesson-loader.js)
  if (document.querySelector('.header-lesson-label')) return;
  var unitLabel = document.querySelector('.header-unit-label');
  if (!unitLabel) return;
  var pill = document.createElement('span');
  pill.className = 'header-lesson-label';
  var num = parseInt(match[1], 10);
  var total = window._lessonOfTotal ? window._lessonOfTotal.total : null;
  pill.textContent = total ? 'Lesson ' + num + ' of ' + total : 'Lesson ' + num;
  unitLabel.parentNode.insertBefore(pill, unitLabel.nextSibling);
}

/* --- Revision Technique Tips (lightbulbs) --- */
function initRevisionTips() {
  const article = document.querySelector('article.study-notes');
  if (!article) return;

  // Detect subject from URL
  var dynamicMatch = location.pathname.match(/^\/lesson\/([^/]+)\//);
  var subject = dynamicMatch ? dynamicMatch[1] : null;

  const basePath = (function () {
    if (dynamicMatch) {
      return '/guide/' + dynamicMatch[1] + '/revision-technique/';
    }
    // Static route: {subject}/{unit}/lesson-NN.html
    const parts = location.pathname.split('/');
    parts.pop();
    return parts.join('/') + '/../revision-technique/';
  })();

  const lightbulbSVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/></svg>';

  // Default tips (universal fallback)
  var defaultTips = [
    { selector: '.key-fact', text: 'Cover this box and try to recall every detail from memory.', link: 'retrieval-practice.html', label: 'Retrieval Practice' },
    { selector: '.timeline', text: 'Draw this timeline from memory on a blank page \u2014 then check your gaps.', link: 'dual-coding.html', label: 'Dual Coding' },
    { selector: '.collapsible', text: 'After reading, ask \u201cwhy?\u201d and \u201chow?\u201d for each key fact inside.', link: 'elaborative-interrogation.html', label: 'Elaborative Interrogation', maxPerPage: 1 }
  ];

  // Subject-specific tips — each links to that subject's revision technique guides
  var subjectTips = {
    'history': [
      { selector: '.key-fact', text: 'Cover this box and try to recall every detail from memory.', link: 'retrieval-practice.html', label: 'Retrieval Practice' },
      { selector: '.timeline', text: 'Draw this timeline from memory on a blank page \u2014 then check your gaps.', link: 'dual-coding.html', label: 'Dual Coding' },
      { selector: '.collapsible', text: 'After reading, ask \u201cwhy?\u201d and \u201chow?\u201d for each key fact inside.', link: 'elaborative-interrogation.html', label: 'Elaborative Interrogation', maxPerPage: 1 },
      { selector: 'figure.diagram', text: 'Recreate this diagram as a knowledge organiser \u2014 connect the concepts in your own layout.', link: 'knowledge-organisers.html', label: 'Knowledge Organisers', maxPerPage: 1 }
    ],
    'business': [
      { selector: '.key-fact', text: 'Cover this box and write down everything you remember.', link: 'retrieval-practice.html', label: 'Retrieval Practice' },
      { selector: 'figure.diagram', text: 'Use this diagram as the start of a mind map \u2014 add your own examples and connections.', link: 'mind-mapping.html', label: 'Mind Mapping', maxPerPage: 1 },
      { selector: '.collapsible', text: 'Summarise the key points inside in your own words before moving on.', link: 'active-reading.html', label: 'Active Reading', maxPerPage: 1 }
    ],
    'geography': [
      { selector: '.key-fact', text: 'Cover this box and try to recall every detail from memory.', link: 'retrieval-practice.html', label: 'Retrieval Practice' },
      { selector: 'figure.diagram', text: 'Sketch a simplified version of this diagram from memory, adding your own labels.', link: 'sketch-maps.html', label: 'Sketch Maps', maxPerPage: 1 },
      { selector: '.collapsible', text: 'Turn the key details inside into a case study revision card.', link: 'case-study-cards.html', label: 'Case Study Cards', maxPerPage: 1 }
    ],
    'sport-science': [
      { selector: '.key-fact', text: 'Cover this box and try to recall every detail from memory.', link: 'retrieval-practice.html', label: 'Retrieval Practice' },
      { selector: 'figure.diagram', text: 'Redraw this diagram from memory and label each component.', link: 'dual-coding.html', label: 'Dual Coding', maxPerPage: 1 },
      { selector: '.collapsible', text: 'Create a sports scenario that applies the concepts described inside.', link: 'scenario-practice.html', label: 'Scenario Practice', maxPerPage: 1 }
    ],
    'food-technology': [
      { selector: '.key-fact', text: 'Cover this box and try to recall every detail from memory.', link: 'retrieval-practice.html', label: 'Retrieval Practice' },
      { selector: 'figure.diagram', text: 'Redraw this diagram from memory, labelling each nutritional concept.', link: 'dual-coding.html', label: 'Dual Coding', maxPerPage: 1 },
      { selector: '.collapsible', text: 'Explain the content inside to someone else in your own words.', link: 'teach-back.html', label: 'Teach Back', maxPerPage: 1 }
    ],
    'religious-education': [
      { selector: '.key-fact', text: 'Turn this into a flashcard \u2014 the key teaching on one side, its source and meaning on the other.', link: 'quote-flashcards.html', label: 'Quote Flashcards' },
      { selector: 'figure.diagram', text: 'Create a comparison table from this diagram showing similarities and differences.', link: 'comparison-tables.html', label: 'Comparison Tables', maxPerPage: 1 },
      { selector: '.collapsible', text: 'Use the points inside to plan both sides of a 12-mark evaluation answer.', link: 'argument-planning.html', label: 'Argument Planning', maxPerPage: 1 }
    ],
    'gcse-music': [
      { selector: '.key-fact', text: 'Cover this box and try to recall every detail from memory.', link: 'retrieval-practice.html', label: 'Retrieval Practice' },
      { selector: 'figure.diagram', text: 'Redraw this diagram from memory, labelling each musical element.', link: 'dual-coding.html', label: 'Dual Coding', maxPerPage: 1 },
      { selector: '.collapsible', text: 'Listen to an example piece and try to identify each element discussed inside.', link: 'active-listening.html', label: 'Active Listening', maxPerPage: 1 }
    ],
    'english-literature': [
      { selector: '.key-fact', text: 'Turn this into a quote flashcard \u2014 the quote on one side, analysis and context on the other.', link: 'quote-flashcards.html', label: 'Quote Flashcards' },
      { selector: 'figure.diagram', text: 'Recreate this as a character or theme map from memory, adding your own textual evidence.', link: 'dual-coding.html', label: 'Dual Coding', maxPerPage: 1 },
      { selector: '.collapsible', text: 'Use the points inside to write a timed practice paragraph \u2014 aim for 10 minutes.', link: 'timed-exam-practice.html', label: 'Timed Exam Practice', maxPerPage: 1 }
    ],
    'english-language': [
      { selector: '.key-fact', text: 'Use retrieval practice to memorise key terminology and mark scheme criteria', link: 'retrieval-practice.html', label: 'Retrieval Practice' },
      { selector: '.timeline', text: 'Try dual coding to visualise language and structure techniques', link: 'dual-coding.html', label: 'Dual Coding' },
      { selector: '.collapsible', text: 'Use elaborative interrogation to deepen your analysis of writer\u2019s methods', link: 'elaborative-interrogation.html', label: 'Elaborative Interrogation', maxPerPage: 1 }
    ],
    'science': [
      { selector: '.key-fact', text: 'Cover this box and try to recall every detail from memory.', link: 'retrieval-practice.html', label: 'Retrieval Practice' },
      { selector: 'figure.diagram', text: 'Redraw this diagram from memory, labelling each part and adding the key equations.', link: 'mind-maps-diagrams.html', label: 'Mind Maps & Diagrams', maxPerPage: 1 },
      { selector: '.collapsible', text: 'Turn the facts inside into a set of flashcards \u2014 question on one side, answer on the other.', link: 'active-recall-flashcards.html', label: 'Active Recall', maxPerPage: 1 }
    ],
    'separate-sciences': [
      { selector: '.key-fact', text: 'Cover this box and try to recall every detail from memory.', link: 'retrieval-practice.html', label: 'Retrieval Practice' },
      { selector: 'figure.diagram', text: 'Redraw this diagram from memory, labelling each part and adding the key equations.', link: 'mind-maps-diagrams.html', label: 'Mind Maps & Diagrams', maxPerPage: 1 },
      { selector: '.collapsible', text: 'Turn the facts inside into a set of flashcards \u2014 question on one side, answer on the other.', link: 'active-recall-flashcards.html', label: 'Active Recall', maxPerPage: 1 }
    ]
  };

  const tips = subjectTips[subject] || defaultTips;

  let openPopup = null;

  tips.forEach(function (tip) {
    const els = article.querySelectorAll(tip.selector);
    const limit = tip.maxPerPage || Infinity;
    let count = 0;

    els.forEach(function (el) {
      if (count >= limit) return;
      count++;

      el.classList.add('revision-tip-anchor');

      const btn = document.createElement('button');
      btn.className = 'revision-tip-btn';
      btn.setAttribute('aria-label', 'Revision tip');
      btn.innerHTML = lightbulbSVG;

      const popup = document.createElement('div');
      popup.className = 'revision-tip-popup';
      var tipHref = basePath + (basePath.startsWith('/guide/') ? tip.link.replace('.html', '') : tip.link);
      // Use content-specific tip if present, otherwise fall back to generic
      var tipText = el.getAttribute('data-revision-tip') || tip.text;
      popup.innerHTML = '<p>' + tipText + '</p><a href="' + tipHref + '">' + tip.label + ' \u2192</a>';

      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        if (openPopup && openPopup !== popup) {
          openPopup.classList.remove('is-open');
        }
        popup.classList.toggle('is-open');
        openPopup = popup.classList.contains('is-open') ? popup : null;
      });

      el.appendChild(btn);
      el.appendChild(popup);
    });
  });

  // Close on outside click
  document.addEventListener('click', function () {
    if (openPopup) {
      openPopup.classList.remove('is-open');
      openPopup = null;
    }
  });
}

/* --- Lesson Progress Tracker --- */
function initLessonProgress() {
  var sidebar = document.querySelector('.lesson-sidebar');
  if (!sidebar) return;

  var pathMatch = location.pathname.match(/^\/lesson\/([^/]+)\/([^/]+)\/(\d+)/);
  if (!pathMatch) return;

  var storageKey = 'sv_progress_' + pathMatch[1] + '_' + pathMatch[2] + '_' + pathMatch[3];

  function getState() {
    try { return JSON.parse(localStorage.getItem(storageKey)) || {}; } catch(e) { return {}; }
  }
  function saveState(s) { localStorage.setItem(storageKey, JSON.stringify(s)); }

  var tasks = [];

  var icons = {
    podcast: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>',
    video: '<svg viewBox="0 0 24 24" fill="currentColor" width="15" height="15"><polygon points="5,3 19,12 5,21"/></svg>',
    kc: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    revision: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/></svg>',
  };

  // Check for podcast — either in the tabbed player or in sidebar media
  if (window.podcastUrl || sidebar.innerHTML.toLowerCase().indexOf('podcast') !== -1) {
    tasks.push({ id: 'podcast', label: 'Listen to podcast', icon: icons.podcast, iconClass: 'lesson-progress-icon--podcast', auto: false });
  }

  // Check for video
  var videoSection = document.getElementById('sidebar-video-section');
  if (videoSection && videoSection.style.display !== 'none') {
    tasks.push({ id: 'video', label: 'Watch the video', icon: icons.video, iconClass: 'lesson-progress-icon--video', auto: false });
  }

  // Knowledge check
  tasks.push({ id: 'knowledge-check', label: 'Complete quick quiz', icon: icons.kc, iconClass: 'lesson-progress-icon--kc', auto: true });

  // Flashcards
  tasks.push({ id: 'flashcards', label: 'Revise with flashcards', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="2" y="4" width="16" height="14" rx="2"/><rect x="6" y="6" width="16" height="14" rx="2"/></svg>', iconClass: 'lesson-progress-icon--flashcards', auto: true });

  // Revision task
  tasks.push({ id: 'revision-task', label: 'Complete a revision task', icon: icons.revision, iconClass: 'lesson-progress-icon--revision', auto: false });

  if (tasks.length === 0) return;

  var state = getState();
  var checkSVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';

  // ---- Build sidebar version (shown on narrow screens / mobile panel) ----
  var section = document.createElement('div');
  section.className = 'sidebar-section sidebar-progress-section';
  var html = '<div class="sidebar-section-title">Lesson Progress</div><div class="lesson-progress-card">';

  tasks.forEach(function(task) {
    var done = state[task.id] ? ' completed' : '';
    html += '<div class="lesson-progress-item' + done + '" data-task="' + task.id + '"' + (task.auto ? ' data-auto="1"' : '') + '>';
    html += '<div class="lesson-progress-icon ' + (task.iconClass || '') + '">' + (task.icon || '') + '</div>';
    html += '<div class="lesson-progress-check">' + checkSVG + '</div>';
    html += '<span class="lesson-progress-label">' + task.label + '</span></div>';
  });

  var completed = tasks.filter(function(t) { return state[t.id]; }).length;
  var pct = Math.round((completed / tasks.length) * 100);
  html += '<div class="lesson-progress-bar"><div class="lesson-progress-bar-fill" style="width:' + pct + '%"></div></div>';
  html += '<div class="lesson-progress-summary">' + completed + ' of ' + tasks.length + ' complete</div></div>';
  section.innerHTML = html;

  var firstSection = sidebar.querySelector('.sidebar-section');
  sidebar.insertBefore(section, firstSection);

  // ---- Build gutter version (fixed left rail on wide desktops) ----
  var gutter = document.createElement('div');
  gutter.className = 'gutter-progress';
  var gutterHtml = '<div class="gutter-progress-title">Lesson Checklist</div>';

  tasks.forEach(function(task) {
    var done = state[task.id] ? ' completed' : '';
    gutterHtml += '<div class="gutter-progress-item' + done + '" data-task="' + task.id + '"' + (task.auto ? ' data-auto="1"' : '') + ' data-label="' + task.label + '">';
    gutterHtml += '<div class="gutter-progress-icon ' + (task.iconClass || '') + '">' + (task.icon || '') + '</div>';
    gutterHtml += '<div class="gutter-progress-check">' + checkSVG + '</div>';
    gutterHtml += '</div>';
  });

  gutter.innerHTML = gutterHtml;
  document.body.appendChild(gutter);

  // ---- Build inline progress bar (between title and hero) ----
  var lessonHeader = document.querySelector('.lesson-header');
  var heroFigure = document.getElementById('hero-figure');
  if (lessonHeader) {
    // Add % counter next to the title
    var titleEl = document.getElementById('lesson-title');
    if (titleEl) {
      var pctBadge = document.createElement('span');
      pctBadge.className = 'lesson-progress-pct';
      pctBadge.id = 'lesson-progress-pct';
      pctBadge.textContent = pct + '%';
      lessonHeader.appendChild(pctBadge);
    }

    // Add horizontal progress bar after the header
    var inlineBar = document.createElement('div');
    inlineBar.className = 'lesson-progress-inline';
    inlineBar.innerHTML = '<div class="lesson-progress-inline-fill" id="lesson-progress-inline-fill" style="width:' + pct + '%"></div>';
    lessonHeader.parentNode.insertBefore(inlineBar, lessonHeader.nextSibling);
  }

  // ---- Toast for auto-tick items ----
  function showAutoTickToast(label) {
    var existing = document.getElementById('progress-toast');
    if (existing) existing.remove();
    var toast = document.createElement('div');
    toast.id = 'progress-toast';
    toast.style.cssText = 'position:fixed;bottom:2rem;left:50%;transform:translateX(-50%);background:#2d2a26;color:#fff;font-family:Inter,sans-serif;font-size:0.82rem;padding:0.6rem 1.2rem;border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,0.15);z-index:9999;opacity:0;transition:opacity 0.3s ease;pointer-events:none;text-align:center;max-width:320px;';
    toast.textContent = 'This ticks automatically when you ' + label.toLowerCase() + '.';
    document.body.appendChild(toast);
    requestAnimationFrame(function () { toast.style.opacity = '1'; });
    setTimeout(function () {
      toast.style.opacity = '0';
      setTimeout(function () { toast.remove(); }, 300);
    }, 2500);
  }

  // ---- Shared click handlers ----
  function bindClicks(container, itemClass) {
    // Manual tasks: toggle on click
    container.querySelectorAll(itemClass + ':not([data-auto])').forEach(function(item) {
      item.addEventListener('click', function() {
        var taskId = item.dataset.task;
        state[taskId] = !state[taskId];
        saveState(state);
        syncAll();
      });
    });
    // Auto tasks: show toast on click
    container.querySelectorAll(itemClass + '[data-auto]').forEach(function(item) {
      item.addEventListener('click', function() {
        if (!state[item.dataset.task]) {
          var label = item.getAttribute('data-label') || item.querySelector('.lesson-progress-label');
          label = typeof label === 'string' ? label : (label ? label.textContent : 'complete this task');
          showAutoTickToast(label);
        }
      });
    });
  }

  bindClicks(section, '.lesson-progress-item');
  bindClicks(gutter, '.gutter-progress-item');

  // ---- Sync both widgets after any state change ----
  function syncAll() {
    var done = tasks.filter(function(t) { return state[t.id]; }).length;
    var p = Math.round((done / tasks.length) * 100);

    // Sidebar version
    tasks.forEach(function(t) {
      var el = section.querySelector('.lesson-progress-item[data-task="' + t.id + '"]');
      if (el) el.classList.toggle('completed', !!state[t.id]);
    });
    section.querySelector('.lesson-progress-bar-fill').style.width = p + '%';
    section.querySelector('.lesson-progress-summary').textContent = done + ' of ' + tasks.length + ' complete';

    // Gutter version
    tasks.forEach(function(t) {
      var el = gutter.querySelector('.gutter-progress-item[data-task="' + t.id + '"]');
      if (el) el.classList.toggle('completed', !!state[t.id]);
    });

    // Inline bar + title badge
    var inlineFill = document.getElementById('lesson-progress-inline-fill');
    if (inlineFill) inlineFill.style.width = p + '%';
    var pctEl = document.getElementById('lesson-progress-pct');
    if (pctEl) pctEl.textContent = p + '%';
  }

  // Auto-tick knowledge check on completion — watch document.body for the kc-result
  new MutationObserver(function(muts) {
    muts.forEach(function(m) {
      m.addedNodes.forEach(function(n) {
        if (n.nodeType !== 1) return;
        if (n.classList.contains('kc-result') || (n.querySelector && n.querySelector('.kc-result'))) {
          state['knowledge-check'] = true;
          saveState(state);
          syncAll();
        }
      });
    });
  }).observe(document.body, { childList: true, subtree: true });

  // Auto-tick flashcards on completion
  document.addEventListener('flashcards-completed', function () {
    state['flashcards'] = true;
    saveState(state);
    syncAll();
  });
}

/* --- Flashcard Modal (inline revision overlay on lesson page) --- */
function initFlashcardModal() {
  var btn = document.getElementById('sidebar-flashcard-btn');
  if (!btn) return;

  btn.addEventListener('click', function () {
    openFlashcardModal();
  });
}

function openFlashcardModal() {
  // Blur any focused element (prevents Space from triggering narration play button)
  if (document.activeElement) document.activeElement.blur();

  // Pause narration if playing
  var narrationAudio = document.querySelector('.narration-audio');
  if (narrationAudio && !narrationAudio.paused) narrationAudio.pause();

  var lessonId = window._lessonId;
  var glossary = window._lessonGlossary || [];
  var kc = window.knowledgeCheck || [];

  // ---- Build cards ----
  var allCards = [];

  glossary.forEach(function (t, i) {
    allCards.push({
      lessonId: lessonId,
      index: 'g' + i,
      front: t.term,
      back: t.definition,
      type: 'glossary',
      badgeLabel: 'Term'
    });
  });

  // Flashcard-specific questions (separate from knowledge checks)
  var fcQuestions = window._lessonFlashcardQuestions || [];
  fcQuestions.forEach(function (item, i) {
    allCards.push({
      lessonId: lessonId,
      index: 'q' + i,
      front: item.q || item.question,
      back: item.a || item.answer,
      type: 'question',
      badgeLabel: 'Question'
    });
  });

  if (allCards.length === 0) return;

  // ---- Leitner storage (shared with /revise page) ----
  var STORAGE_KEY = 'sv-flashcard-progress';
  var BOX_INTERVALS = [0, 1, 2, 4, 7, 14];

  function loadProgress() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch (e) {}
    return { cards: {}, streak: { current: 0, lastStudy: null } };
  }

  function saveProgress(data) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  }

  function getCardKey(lid, idx) {
    return lid + ':' + idx;
  }

  function todayStr() {
    return new Date().toISOString().slice(0, 10);
  }

  function computeNextReview(box) {
    var d = new Date();
    d.setDate(d.getDate() + BOX_INTERVALS[box]);
    return d.toISOString().slice(0, 10);
  }

  function updateStreak() {
    var prog = loadProgress();
    var today = todayStr();
    var yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    yesterday = yesterday.toISOString().slice(0, 10);

    if (prog.streak.lastStudy === today) {
      // Already studied today
    } else if (prog.streak.lastStudy === yesterday) {
      prog.streak.current++;
      prog.streak.lastStudy = today;
    } else {
      prog.streak.current = 1;
      prog.streak.lastStudy = today;
    }
    saveProgress(prog);
    return prog.streak;
  }

  // ---- Shuffle ----
  function fisherYatesShuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }
    return arr;
  }

  // ---- Escape ----
  function esc(str) {
    var d = document.createElement('div');
    d.textContent = str || '';
    return d.innerHTML;
  }

  // ---- Reading duration (for underline animation) ----
  function getReadDuration(text) {
    var words = (text || '').trim().split(/\s+/).length;
    var seconds = Math.max(1.5, Math.min(words / 4, 6));
    return Math.round(seconds * 100) / 100;
  }

  // ---- TTS ----
  function speakText(text) {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      var utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-GB';
      utterance.rate = 0.9;
      var btns = overlay.querySelectorAll('.fc-modal-speak');
      btns.forEach(function (b) { b.classList.add('speaking'); });
      utterance.onend = function () {
        btns.forEach(function (b) { b.classList.remove('speaking'); });
      };
      utterance.onerror = function () {
        btns.forEach(function (b) { b.classList.remove('speaking'); });
      };
      window.speechSynthesis.speak(utterance);
    }
  }

  function cancelSpeech() {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  }

  // ---- Session state ----
  var sessionCards = fisherYatesShuffle(allCards.slice());
  var currentIdx = 0;
  var results = { correct: 0, wrong: 0, skipped: 0 };
  var answersEnabled = false;
  var answerUnlockTimer = null;

  // ---- Build modal DOM ----
  var overlay = document.createElement('div');
  overlay.className = 'fc-modal-overlay';
  overlay.innerHTML =
    '<div class="fc-modal">' +
      '<div class="fc-modal-header">' +
        '<span class="fc-modal-title">Flashcard Revision</span>' +
        '<span class="fc-modal-count" id="fc-counter">' + allCards.length + ' cards</span>' +
        '<button class="fc-modal-close" aria-label="Close flashcard revision">&times;</button>' +
      '</div>' +
      '<div class="fc-modal-progress"><div class="fc-modal-progress-fill" id="fc-progress-fill"></div></div>' +
      '<div class="fc-modal-body" id="fc-modal-body">' +
        /* Session view */
        '<div class="fc-session" id="fc-session">' +
          '<div class="fc-session-topbar">' +
            '<span class="fc-session-counter" id="fc-session-counter"></span>' +
            '<button class="fc-session-skip" id="fc-skip">Skip</button>' +
          '</div>' +
          '<div class="fc-card-container">' +
            '<div class="fc-card" id="fc-card">' +
              '<div class="fc-card-face fc-card-front">' +
                '<span class="fc-card-badge" id="fc-badge-front"></span>' +
                '<button class="fc-modal-speak" id="fc-speak-front" aria-label="Read aloud" title="Read aloud">' +
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>' +
                '</button>' +
                '<div class="fc-card-text" id="fc-front-text"></div>' +
                '<span class="fc-card-hint">Tap to reveal</span>' +
              '</div>' +
              '<div class="fc-card-face fc-card-back">' +
                '<span class="fc-card-badge" id="fc-badge-back"></span>' +
                '<button class="fc-modal-speak" id="fc-speak-back" aria-label="Read aloud" title="Read aloud">' +
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>' +
                '</button>' +
                '<div class="fc-card-text" id="fc-back-text"></div>' +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div class="fc-answer-buttons" id="fc-answer-buttons">' +
            '<button class="fc-answer-btn fc-answer-btn--wrong" id="fc-btn-wrong">Got it wrong</button>' +
            '<button class="fc-answer-btn fc-answer-btn--right" id="fc-btn-right">Got it right</button>' +
          '</div>' +
        '</div>' +
        /* End screen */
        '<div class="fc-end" id="fc-end" style="display:none">' +
          '<div class="fc-end-card">' +
            '<h2 class="fc-end-title">Session Complete</h2>' +
            '<div class="fc-end-accuracy" id="fc-end-accuracy">0%</div>' +
            '<div class="fc-end-accuracy-label">accuracy</div>' +
            '<div class="fc-end-breakdown">' +
              '<div class="fc-end-stat fc-end-stat--correct"><span class="fc-end-stat-value" id="fc-end-correct">0</span><span class="fc-end-stat-label">correct</span></div>' +
              '<div class="fc-end-stat fc-end-stat--wrong"><span class="fc-end-stat-value" id="fc-end-wrong">0</span><span class="fc-end-stat-label">incorrect</span></div>' +
              '<div class="fc-end-stat fc-end-stat--skipped"><span class="fc-end-stat-value" id="fc-end-skipped">0</span><span class="fc-end-stat-label">skipped</span></div>' +
            '</div>' +
            '<div class="fc-end-streak" id="fc-end-streak" style="display:none"></div>' +
            '<div class="fc-end-actions">' +
              '<button class="fc-end-btn fc-end-btn--primary" id="fc-end-again">Study Again</button>' +
              '<button class="fc-end-btn fc-end-btn--secondary" id="fc-end-close">Back to Lesson</button>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</div>';

  document.body.appendChild(overlay);

  // Prevent body scroll while modal open
  document.body.style.overflow = 'hidden';

  // ---- Animate in ----
  requestAnimationFrame(function () {
    overlay.classList.add('active');
  });

  // ---- DOM refs inside modal ----
  var progressFill = overlay.querySelector('#fc-progress-fill');
  var sessionCounter = overlay.querySelector('#fc-session-counter');
  var cardEl = overlay.querySelector('#fc-card');
  var frontText = overlay.querySelector('#fc-front-text');
  var backText = overlay.querySelector('#fc-back-text');
  var frontBadge = overlay.querySelector('#fc-badge-front');
  var backBadge = overlay.querySelector('#fc-badge-back');
  var answerBtns = overlay.querySelector('#fc-answer-buttons');
  var sessionEl = overlay.querySelector('#fc-session');
  var endEl = overlay.querySelector('#fc-end');

  // ---- Show card ----
  function showCard() {
    if (currentIdx >= sessionCards.length) {
      endSession();
      return;
    }

    var card = sessionCards[currentIdx];
    var total = sessionCards.length;

    sessionCounter.textContent = 'Card ' + (currentIdx + 1) + ' of ' + total;
    progressFill.style.width = ((currentIdx / total) * 100) + '%';

    frontText.textContent = card.front;
    backText.textContent = card.back;
    frontBadge.textContent = card.badgeLabel;
    backBadge.textContent = card.badgeLabel;

    cardEl.classList.remove('flipped');
    cardEl.style.transform = '';
    answerBtns.classList.remove('visible', 'enabled');
    answersEnabled = false;
    if (answerUnlockTimer) { clearTimeout(answerUnlockTimer); answerUnlockTimer = null; }

    setCardHeight();
  }

  function setCardHeight() {
    var faces = cardEl.querySelectorAll('.fc-card-face');
    var maxH = 240;
    faces.forEach(function (f) {
      f.style.position = 'relative';
      var h = f.scrollHeight;
      if (h > maxH) maxH = h;
    });
    faces.forEach(function (f) {
      f.style.position = '';
    });
    cardEl.style.height = maxH + 'px';
  }

  // ---- Flip ----
  function flipCard() {
    if (cardEl.classList.contains('flipped')) return;

    var answerText = backText.textContent || '';
    var duration = getReadDuration(answerText);
    cardEl.style.setProperty('--read-duration', duration + 's');
    cardEl.classList.add('flipped');
    answerBtns.classList.add('visible');
    answerBtns.classList.remove('enabled');
    answersEnabled = false;
    answerBtns.querySelectorAll('.fc-answer-btn').forEach(function (b) { b.classList.add('waiting'); });

    answerUnlockTimer = setTimeout(function () {
      answerBtns.classList.add('enabled');
      answersEnabled = true;
      answerBtns.querySelectorAll('.fc-answer-btn').forEach(function (b) { b.classList.remove('waiting'); });
    }, duration * 1000);
  }

  cardEl.addEventListener('click', function (e) {
    if (e.target.closest('.fc-modal-speak')) return;
    flipCard();
  });

  // ---- Mark card ----
  function markCard(correct) {
    var card = sessionCards[currentIdx];
    var key = getCardKey(card.lessonId, card.index);
    var prog = loadProgress();

    if (!prog.cards[key]) {
      prog.cards[key] = { box: 1, nextReview: todayStr(), attempts: 0, correct: 0 };
    }

    var cp = prog.cards[key];
    cp.attempts++;

    if (correct) {
      cp.correct++;
      cp.box = Math.min(cp.box + 1, 5);
      results.correct++;
    } else {
      cp.box = 1;
      results.wrong++;
    }

    cp.nextReview = computeNextReview(cp.box);
    saveProgress(prog);

    currentIdx++;
    showCard();
  }

  overlay.querySelector('#fc-btn-wrong').addEventListener('click', function () { if (answersEnabled) markCard(false); });
  overlay.querySelector('#fc-btn-right').addEventListener('click', function () { if (answersEnabled) markCard(true); });

  // ---- Skip ----
  function skipCard() {
    results.skipped++;
    currentIdx++;
    showCard();
  }

  overlay.querySelector('#fc-skip').addEventListener('click', skipCard);

  // ---- End session ----
  function endSession() {
    cancelSpeech();
    sessionEl.style.display = 'none';

    var streak = updateStreak();
    var answered = results.correct + results.wrong;
    var accuracy = answered > 0 ? Math.round((results.correct / answered) * 100) : 0;

    overlay.querySelector('#fc-end-accuracy').textContent = accuracy + '%';
    overlay.querySelector('#fc-end-correct').textContent = results.correct;
    overlay.querySelector('#fc-end-wrong').textContent = results.wrong;
    overlay.querySelector('#fc-end-skipped').textContent = results.skipped;

    var streakEl = overlay.querySelector('#fc-end-streak');
    if (streak.current > 1) {
      streakEl.innerHTML = 'You\'re on a <strong>' + streak.current + '-day</strong> study streak!';
      streakEl.style.display = '';
    } else if (streak.current === 1) {
      streakEl.innerHTML = 'Day 1 of your study streak. Come back tomorrow!';
      streakEl.style.display = '';
    } else {
      streakEl.style.display = 'none';
    }

    progressFill.style.width = '100%';
    endEl.style.display = '';

    // Dispatch event for lesson progress tracker auto-tick
    document.dispatchEvent(new CustomEvent('flashcards-completed'));
  }

  // ---- End screen actions ----
  overlay.querySelector('#fc-end-again').addEventListener('click', function () {
    sessionCards = fisherYatesShuffle(allCards.slice());
    currentIdx = 0;
    results = { correct: 0, wrong: 0, skipped: 0 };
    endEl.style.display = 'none';
    sessionEl.style.display = '';
    cancelSpeech();
    showCard();
  });

  overlay.querySelector('#fc-end-close').addEventListener('click', closeModal);

  // ---- TTS buttons ----
  overlay.querySelector('#fc-speak-front').addEventListener('click', function (e) {
    e.stopPropagation();
    speakText(frontText.textContent);
  });
  overlay.querySelector('#fc-speak-back').addEventListener('click', function (e) {
    e.stopPropagation();
    speakText(backText.textContent);
  });

  // ---- Keyboard ----
  function handleKey(e) {
    if (e.key === 'Escape') {
      closeModal();
      return;
    }
    // Only handle keys when session is visible
    if (sessionEl.style.display === 'none') return;

    if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault();
      e.stopImmediatePropagation();
      flipCard();
    } else if (e.key === 'ArrowLeft' || e.key === '1') {
      e.stopImmediatePropagation();
      if (cardEl.classList.contains('flipped') && answersEnabled) markCard(false);
    } else if (e.key === 'ArrowRight' || e.key === '2') {
      e.stopImmediatePropagation();
      if (cardEl.classList.contains('flipped') && answersEnabled) markCard(true);
    } else if (e.key === 's' || e.key === 'S') {
      e.stopImmediatePropagation();
      skipCard();
    }
  }

  document.addEventListener('keydown', handleKey);

  // ---- Close ----
  function closeModal() {
    cancelSpeech();
    if (answerUnlockTimer) clearTimeout(answerUnlockTimer);
    document.removeEventListener('keydown', handleKey);
    overlay.classList.remove('active');
    document.body.style.overflow = '';
    setTimeout(function () {
      if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
    }, 300);
  }

  overlay.querySelector('.fc-modal-close').addEventListener('click', closeModal);
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeModal();
  });

  // ---- Touch swipe gestures (Tinder-style fling) ----
  // Apply swipe to the container, not the card (avoids rotateY inversion)
  var swipeTarget = cardEl.parentElement; // .fc-card-container
  var touchStartX = 0;
  var touchStartY = 0;

  cardEl.addEventListener('touchstart', function (e) {
    touchStartX = e.changedTouches[0].screenX;
    touchStartY = e.changedTouches[0].screenY;
    swipeTarget.style.transition = 'none';
  }, { passive: true });

  cardEl.addEventListener('touchmove', function (e) {
    if (!cardEl.classList.contains('flipped') || !answersEnabled) return;
    var dx = e.changedTouches[0].screenX - touchStartX;
    var rotation = dx / 20;
    var opacity = Math.max(0.3, 1 - Math.abs(dx) / 400);
    swipeTarget.style.transform = 'translateX(' + dx + 'px) rotate(' + rotation + 'deg)';
    swipeTarget.style.opacity = opacity;
    // Colour glow: green for right, red for left
    var intensity = Math.min(0.35, Math.abs(dx) / 300);
    if (dx > 10) {
      cardEl.style.boxShadow = '0 0 ' + Math.round(intensity * 60) + 'px rgba(22,163,74,' + intensity + ')';
    } else if (dx < -10) {
      cardEl.style.boxShadow = '0 0 ' + Math.round(intensity * 60) + 'px rgba(220,38,38,' + intensity + ')';
    } else {
      cardEl.style.boxShadow = '';
    }
  }, { passive: true });

  cardEl.addEventListener('touchend', function (e) {
    cardEl.style.boxShadow = '';
    swipeTarget.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
    var dx = e.changedTouches[0].screenX - touchStartX;
    var dy = e.changedTouches[0].screenY - touchStartY;

    if (cardEl.classList.contains('flipped') && answersEnabled && Math.abs(dx) > 80 && Math.abs(dx) > Math.abs(dy)) {
      var direction = dx > 0 ? 1 : -1;
      swipeTarget.style.transform = 'translateX(' + (direction * 600) + 'px) rotate(' + (direction * 30) + 'deg)';
      swipeTarget.style.opacity = '0';
      setTimeout(function () {
        swipeTarget.style.transition = 'none';
        swipeTarget.style.transform = '';
        swipeTarget.style.opacity = '';
        if (dx > 0) markCard(true);
        else markCard(false);
      }, 250);
    } else {
      swipeTarget.style.transform = '';
      swipeTarget.style.opacity = '';
    }
  }, { passive: true });

  // ---- First-time tutorial ----
  function showTutorialIfNeeded() {
    if (localStorage.getItem('sv-flashcard-tutorial-done')) return;

    var container = overlay.querySelector('.fc-card-container');
    if (!container) return;
    container.style.position = 'relative';

    var tut = document.createElement('div');
    tut.className = 'fc-tutorial-overlay';
    tut.innerHTML =
      '<div class="fc-tutorial-card">' +
        '<h3>How to use Flashcards</h3>' +
        '<ul>' +
          '<li>Tap the card or press <kbd>Enter</kbd> to flip it</li>' +
          '<li>Swipe left or press <kbd>&larr;</kbd> if you got it wrong</li>' +
          '<li>Swipe right or press <kbd>&rarr;</kbd> if you got it right</li>' +
          '<li>Tap the speaker icon to hear it read aloud</li>' +
        '</ul>' +
        '<button class="fc-tutorial-btn">Got it</button>' +
      '</div>';

    container.appendChild(tut);

    tut.querySelector('.fc-tutorial-btn').addEventListener('click', function (e) {
      e.stopPropagation();
      localStorage.setItem('sv-flashcard-tutorial-done', '1');
      tut.remove();
    });
  }

  // ---- Start session ----
  showCard();
  showTutorialIfNeeded();
}

// Expose globally so lesson-loader can call it
window.openFlashcardModal = openFlashcardModal;
