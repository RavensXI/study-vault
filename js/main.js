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

  function showQuestion() {
    // Pick a random question different from current
    let idx;
    do {
      idx = Math.floor(Math.random() * questions.length);
    } while (idx === currentIndex && questions.length > 1);
    currentIndex = idx;

    const q = questions[currentIndex];
    typeEl.textContent = q.type;
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
  marksEl.parentNode.insertBefore(showMarksLink, marksEl.nextSibling);
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
  const playerEl = document.querySelector('.narration-player');
  if (!playerEl) return;

  const audio = playerEl.querySelector('.narration-audio');
  const playBtn = playerEl.querySelector('.narration-play');
  const progress = playerEl.querySelector('.narration-progress');
  const progressFill = playerEl.querySelector('.narration-progress-fill');
  const timeEl = playerEl.querySelector('.narration-time');
  const speedBtn = playerEl.querySelector('.narration-speed');

  if (!audio) return;

  let manifest = window.narrationManifest || [];
  let activeChunk = null;
  const speeds = [1, 1.25, 1.5, 0.75];
  let speedIndex = 0;

  // Format time as m:ss
  function fmtTime(s) {
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return m + ':' + (sec < 10 ? '0' : '') + sec;
  }

  // Play / Pause
  playBtn.addEventListener('click', () => {
    if (audio.paused) {
      audio.play();
    } else {
      audio.pause();
    }
  });

  audio.addEventListener('play', () => {
    playBtn.classList.add('playing');
    playBtn.setAttribute('aria-label', 'Pause narration');
  });

  audio.addEventListener('pause', () => {
    playBtn.classList.remove('playing');
    playBtn.setAttribute('aria-label', 'Play narration');
  });

  // Progress bar update
  audio.addEventListener('timeupdate', () => {
    if (!audio.duration) return;
    const pct = (audio.currentTime / audio.duration) * 100;
    progressFill.style.width = pct + '%';
    timeEl.textContent = fmtTime(audio.currentTime) + ' / ' + fmtTime(audio.duration);

    // Highlight current chunk
    updateHighlight(audio.currentTime);
  });

  // Click to seek on progress bar
  progress.addEventListener('click', (e) => {
    const rect = progress.getBoundingClientRect();
    const pct = (e.clientX - rect.left) / rect.width;
    audio.currentTime = pct * audio.duration;
  });

  // Speed toggle
  speedBtn.addEventListener('click', () => {
    speedIndex = (speedIndex + 1) % speeds.length;
    audio.playbackRate = speeds[speedIndex];
    speedBtn.textContent = speeds[speedIndex] + 'x';
  });

  // Click on narrated element to jump to that point
  document.querySelectorAll('[data-narration-id]').forEach(el => {
    el.addEventListener('click', () => {
      const id = el.dataset.narrationId;
      const entry = manifest.find(m => m.id === id);
      if (entry) {
        audio.currentTime = entry.start;
        if (audio.paused) audio.play();
      }
    });
  });

  // When a collapsible opens, re-apply highlight if narration is inside it
  document.querySelectorAll('.collapsible-toggle').forEach(toggle => {
    toggle.addEventListener('click', () => {
      if (activeChunk && !audio.paused) {
        // Force re-evaluation by clearing activeChunk
        const current = activeChunk;
        activeChunk = null;
        updateHighlight(audio.currentTime);
      }
    });
  });

  // Auto-scroll tracking — disable when user manually scrolls away
  let autoScrollEnabled = true;
  let lastProgrammaticScroll = 0;

  function isInViewport(el) {
    const rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight && rect.bottom > 0;
  }

  function doAutoScroll(el) {
    lastProgrammaticScroll = Date.now();
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  // Listen for manual scrolls to detect when the user leaves the narration area
  window.addEventListener('scroll', () => {
    if (audio.paused) return;
    // Ignore scroll events caused by our own scrollIntoView
    if (Date.now() - lastProgrammaticScroll < 1000) return;
    // User is manually scrolling — check if active element is still visible
    if (activeChunk) {
      const el = document.querySelector('[data-narration-id="' + activeChunk + '"]');
      if (el) autoScrollEnabled = isInViewport(el);
    }
  }, { passive: true });

  function updateHighlight(time) {
    let newChunk = null;

    for (let i = manifest.length - 1; i >= 0; i--) {
      if (time >= manifest[i].start && time < manifest[i].end) {
        newChunk = manifest[i].id;
        break;
      }
    }

    if (newChunk === activeChunk) return;

    // Remove old highlight
    if (activeChunk) {
      const oldEl = document.querySelector('[data-narration-id="' + activeChunk + '"]');
      if (oldEl) oldEl.classList.remove('narration-active');
    }

    // Work out where the new chunk lives
    let newCollapsible = null;
    let newEl = null;
    if (newChunk) {
      newEl = document.querySelector('[data-narration-id="' + newChunk + '"]');
      if (newEl) newCollapsible = newEl.closest('.collapsible');
    }

    // Remove shimmer from any collapsible that isn't the current one
    document.querySelectorAll('.collapsible.narration-reading').forEach(el => {
      if (el !== newCollapsible) el.classList.remove('narration-reading');
    });

    // Add new highlight (always), but only auto-scroll if user hasn't scrolled away
    if (newEl) {
      if (newCollapsible && !newCollapsible.classList.contains('open')) {
        // Content is collapsed — shimmer the collapsible toggle
        if (!newCollapsible.classList.contains('narration-reading')) {
          newCollapsible.classList.add('narration-reading');
        }
        if (autoScrollEnabled) {
          const toggle = newCollapsible.querySelector('.collapsible-toggle');
          if (toggle) {
            const rect = toggle.getBoundingClientRect();
            if (rect.top < 80 || rect.bottom > window.innerHeight - 80) {
              doAutoScroll(toggle);
            }
          }
        }
      } else {
        // Content is visible — highlight normally
        newEl.classList.add('narration-active');
        if (autoScrollEnabled) {
          const rect = newEl.getBoundingClientRect();
          if (rect.top < 80 || rect.bottom > window.innerHeight - 80) {
            doAutoScroll(newEl);
          }
        }
      }
    }

    activeChunk = newChunk;
  }

  // Clear highlight when audio ends
  audio.addEventListener('ended', () => {
    if (activeChunk) {
      const el = document.querySelector('[data-narration-id="' + activeChunk + '"]');
      if (el) el.classList.remove('narration-active');
      activeChunk = null;
    }
    // Clear any collapsible pulse
    document.querySelectorAll('.collapsible.narration-reading').forEach(el => {
      el.classList.remove('narration-reading');
    });
  });

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    // Don't capture when typing in inputs
    const tag = e.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || e.target.isContentEditable) return;

    if (e.code === 'Space') {
      e.preventDefault();
      if (audio.paused) audio.play();
      else audio.pause();
    } else if (e.code === 'ArrowLeft') {
      e.preventDefault();
      audio.currentTime = Math.max(0, audio.currentTime - 5);
    } else if (e.code === 'ArrowRight') {
      e.preventDefault();
      audio.currentTime = Math.min(audio.duration || 0, audio.currentTime + 5);
    }
  });

  // --- Floating mini-player ---
  const fab = document.createElement('div');
  fab.className = 'narration-fab';
  fab.innerHTML =
    '<button class="narration-fab-play" aria-label="Pause narration">' +
      '<svg class="narration-icon-play" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>' +
      '<svg class="narration-icon-pause" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>' +
    '</button>' +
    '<div class="narration-fab-progress"><div class="narration-fab-progress-fill"></div></div>' +
    '<span class="narration-fab-time">0:00</span>';
  document.body.appendChild(fab);

  const fabPlay = fab.querySelector('.narration-fab-play');
  const fabFill = fab.querySelector('.narration-fab-progress-fill');
  const fabTime = fab.querySelector('.narration-fab-time');

  fabPlay.addEventListener('click', () => {
    if (audio.paused) audio.play();
    else audio.pause();
  });

  // Sync fab state with audio
  audio.addEventListener('play', () => fabPlay.classList.add('playing'));
  audio.addEventListener('pause', () => fabPlay.classList.remove('playing'));
  audio.addEventListener('timeupdate', () => {
    if (!audio.duration) return;
    fabFill.style.width = (audio.currentTime / audio.duration * 100) + '%';
    fabTime.textContent = fmtTime(audio.currentTime);
  });

  // Show fab when main player is out of view AND audio has been used
  let mainPlayerVisible = true;
  let audioStarted = false;
  const observer = new IntersectionObserver(([entry]) => {
    mainPlayerVisible = entry.isIntersecting;
    fab.classList.toggle('visible', !mainPlayerVisible && audioStarted);
  }, { threshold: 0 });
  observer.observe(playerEl);

  audio.addEventListener('play', () => {
    audioStarted = true;
    fab.classList.toggle('visible', !mainPlayerVisible);
  });
  audio.addEventListener('ended', () => {
    audioStarted = false;
    fab.classList.remove('visible');
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
