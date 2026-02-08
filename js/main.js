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

  // Highlight logic
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

    // Add new highlight
    if (newEl) {
      if (newCollapsible && !newCollapsible.classList.contains('open')) {
        // Content is collapsed — shimmer the collapsible toggle
        if (!newCollapsible.classList.contains('narration-reading')) {
          newCollapsible.classList.add('narration-reading');
        }
        const toggle = newCollapsible.querySelector('.collapsible-toggle');
        if (toggle) {
          const rect = toggle.getBoundingClientRect();
          if (rect.top < 80 || rect.bottom > window.innerHeight - 80) {
            toggle.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }
      } else {
        // Content is visible — highlight normally
        newEl.classList.add('narration-active');
        const rect = newEl.getBoundingClientRect();
        if (rect.top < 80 || rect.bottom > window.innerHeight - 80) {
          newEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
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
