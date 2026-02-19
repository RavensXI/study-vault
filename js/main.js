/* ============================================
   StudyVault v2 — main.js
   Scroll progress, collapsibles, visited tracking, mobile nav
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
  initScrollProgress();
  initCollapsibles();
  initVisitedTracking();
  initMobileNav();
  initPracticeQuestions();
  initNarration();
  initAccessibility();
  initGlossary();
  initLightbox();
  initHeroEdit();
  initPageTransitions();
  initKnowledgeCheck();
  initLessonNavBackSlot();
  initNavIcons();
  initRevisionTips();
  initLogoLink();
});

/* --- Scroll Progress Bar --- */
function initScrollProgress() {
  const bar = document.querySelector('.scroll-progress');
  if (!bar) return;

  function updateProgress() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    bar.style.width = Math.min(pct, 100) + '%';
  }

  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();
}

/* --- Collapsible Sections --- */
function initCollapsibles() {
  document.querySelectorAll('.collapsible-toggle').forEach(btn => {
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
      ['Describe two', 'describe-two.html'],
      ['Write an account', 'write-an-account.html'],
      ['Explain the significance', 'explain-significance.html'],
      ['Explain what was important', 'explain-significance.html'],
      ['Explain two similarities', 'explain-similarities.html'],
      ['In what ways', 'in-what-ways.html'],
      ['Which had more impact', 'which-had-more-impact.html'],
      ['How far do you agree', 'factor-essay.html'],
      ['Has ', 'factor-essay.html'],
      ['Define', 'define.html'],
      ['Outline', 'outline.html'],
      ['Explain one way', 'explain-one-way.html'],
      ['Calculate', 'calculate.html'],
      ['Discuss', 'discuss.html'],
      ['Justify', 'justify-evaluate.html'],
      ['Evaluate', 'justify-evaluate.html']
    ];
    for (var i = 0; i < guides.length; i++) {
      if (type.indexOf(guides[i][0]) !== -1) return '../exam-technique/' + guides[i][1];
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

  function toggleMenu() {
    const isOpen = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', isOpen);
    if (overlay) overlay.classList.toggle('open', isOpen);
  }

  function closeMenu() {
    nav.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
    if (overlay) overlay.classList.remove('open');
  }

  btn.addEventListener('click', toggleMenu);

  if (overlay) {
    overlay.addEventListener('click', closeMenu);
  }

  // Close when clicking a nav link
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  // Close on Escape key
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && nav.classList.contains('open')) {
      closeMenu();
    }
  });
}

/* --- Narration Player --- */
function initNarration() {
  var playerEl = document.querySelector('.narration-player');
  if (!playerEl) return;

  var audio = playerEl.querySelector('.narration-audio');
  var playBtn = playerEl.querySelector('.narration-play');
  var progressFill = playerEl.querySelector('.narration-progress-fill');
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
    if (audio.paused) { startPlayback(); } else { audio.pause(); }
  });

  fabPlay.addEventListener('click', function() {
    if (audio.paused) { startPlayback(); } else { audio.pause(); }
  });

  audio.addEventListener('play', function() {
    isPlaying = true;
    audioStarted = true;
    playBtn.classList.add('playing');
    playBtn.setAttribute('aria-label', 'Pause narration');
    fabPlay.classList.add('playing');
    fab.classList.toggle('visible', !mainPlayerVisible);
    if (currentIndex >= 0) setHighlight(manifest[currentIndex].id);
  });

  audio.addEventListener('pause', function() {
    isPlaying = false;
    playBtn.classList.remove('playing');
    playBtn.setAttribute('aria-label', 'Play narration');
    fabPlay.classList.remove('playing');
  });

  // --- Progress ---

  audio.addEventListener('timeupdate', function() {
    var gt = globalTime();
    var pct = (gt / totalDuration * 100) + '%';
    progressFill.style.width = pct;
    timeEl.textContent = fmtTime(gt) + ' / ' + fmtTime(totalDuration);
    fabFill.style.width = pct;
    fabTime.textContent = fmtTime(gt);
  });

  // --- Clip ended — advance or finish ---

  audio.addEventListener('ended', function() {
    if (currentIndex + 1 < manifest.length) {
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

  // --- Speed toggle ---

  speedBtn.addEventListener('click', function() {
    speedIndex = (speedIndex + 1) % speeds.length;
    audio.playbackRate = speeds[speedIndex];
    speedBtn.textContent = speeds[speedIndex] + 'x';
  });

  // --- Click paragraph to jump to that clip ---

  document.querySelectorAll('[data-narration-id]').forEach(function(el) {
    el.addEventListener('click', function() {
      var id = el.dataset.narrationId;
      for (var i = 0; i < manifest.length; i++) {
        if (manifest[i].id === id) { loadClip(i); audio.play(); break; }
      }
    });
  });

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

    // Check if popup would go off the top of the viewport — flip below if so
    const rect = term.getBoundingClientRect();
    term.classList.toggle('term-flip', rect.top < 100);

    term.classList.add('term-visible');
    activeTerm = term;
  }

  function hideTerm(term) {
    term.classList.remove('term-visible', 'term-flip');
    if (activeTerm === term) activeTerm = null;
  }

  terms.forEach(term => {
    // Desktop: hover
    term.addEventListener('mouseenter', () => showTerm(term));
    term.addEventListener('mouseleave', () => hideTerm(term));

    // Mobile: tap to toggle
    term.addEventListener('click', (e) => {
      e.preventDefault();
      if (term.classList.contains('term-visible')) {
        hideTerm(term);
      } else {
        showTerm(term);
      }
    });
  });

  // Close on tap elsewhere (mobile)
  document.addEventListener('click', (e) => {
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
        '<span class="kc-title">Knowledge Check</span>' +
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
  // Pages with data-unit are 2 levels deep (subject/unit-folder/).
  // Update logo href to go to the root dashboard.
  if (document.body.dataset.unit) {
    brand.setAttribute('href', '../../index.html');
  }
}

/* --- Revision Technique Tips (lightbulbs) --- */
function initRevisionTips() {
  const article = document.querySelector('article.study-notes');
  if (!article) return;

  const basePath = (function () {
    const parts = location.pathname.split('/');
    parts.pop();
    return parts.join('/') + '/../revision-technique/';
  })();

  const lightbulbSVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/></svg>';

  const tips = [
    {
      selector: '.key-fact',
      text: 'Cover this box and try to recall every detail from memory.',
      link: 'retrieval-practice.html',
      label: 'Retrieval Practice'
    },
    {
      selector: '.timeline',
      text: 'Draw this timeline from memory on a blank page \u2014 then check your gaps.',
      link: 'dual-coding.html',
      label: 'Dual Coding'
    },
    {
      selector: '.collapsible',
      text: 'After reading, ask \u201cwhy?\u201d and \u201chow?\u201d for each key fact inside.',
      link: 'elaborative-interrogation.html',
      label: 'Elaborative Interrogation',
      maxPerPage: 1
    }
  ];

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
      popup.innerHTML = '<p>' + tip.text + '</p><a href="' + basePath + tip.link + '">' + tip.label + ' \u2192</a>';

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
