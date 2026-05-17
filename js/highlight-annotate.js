/* StudyVault — Highlight & Annotate (prototype)
 *
 * Lets a student select text in #study-notes, choose a colour, add an optional note,
 * and revisit everything they've marked on a per-lesson modal or the cross-lesson
 * /highlights page. Storage is localStorage only; this is intentionally a prototype
 * that will be migrated server-side once student accounts ship.
 *
 * Activation: feature is gated behind ?highlights=1 in the URL (or
 * localStorage flag sv-hl-enabled=1, set automatically the first time the user
 * arrives with the query string). Once enabled, it stays enabled on this device.
 *
 * Public entry point: window.initHighlightAnnotate() — safe to call multiple times.
 */
(function () {
  'use strict';

  // ---------- PREVIEW: hardcoded per-lesson category definitions ----------
  // Stop-gap until the per-lesson generation pipeline runs (next session).
  // The mechanism (window._lessonCategoryDefinitions) is the same one the
  // real pipeline will populate from Supabase — once that's wired up, this
  // block goes away and lesson-loader.js sets the global instead.
  (function previewPerLessonDefinitions() {
    var path = window.location.pathname || '';
    // AQA English Literature — Julius Caesar — Lesson 5 (Characters)
    if (path.indexOf('julius-caesar') !== -1 && /\/0?5\/?$/.test(path)) {
      window._lessonCategoryDefinitions = {
        fact: "Character names, relationships, traits, and the lines that establish who someone is. Direct quotations that show what kind of person they are.",
        why: "What drives a character to act this way — and what Shakespeare wants the audience to feel about them.",
        'so-what': "How a character's actions shape the plot or carry a theme. The effect they have on other characters or on the play's argument.",
        question: "What the play leaves unclear about a character — their motives, contradictions, or things that stay unsaid. Worth asking your teacher."
      };
      return;
    }
    // AQA Science — any Biology lesson (subject-level framing)
    if (/\/biology/i.test(path)) {
      window._lessonCategoryDefinitions = {
        fact: "Scientific terms, definitions, equations, units, names of organs, tissues, cells and organelles, and any numbers worth memorising.",
        why: "How a biological process actually works — the mechanism, the cause of a condition, the reason behind an experimental result.",
        'so-what': "Real-world applications — health, disease, agriculture, ecology. Links to required practicals or to 6-mark exam questions.",
        question: "Something the lesson glosses over or that didn't click — a step in a mechanism, a confusing graph, a definition that contradicts another one. Worth asking your teacher."
      };
      return;
    }
  })();

  // ---------- feature gating ----------
  function isEnabled() {
    try {
      var url = new URL(window.location.href);
      if (url.searchParams.get('highlights') === '1') {
        try { localStorage.setItem('sv-hl-enabled', '1'); } catch (e) {}
        return true;
      }
      if (url.searchParams.get('highlights') === '0') {
        try { localStorage.removeItem('sv-hl-enabled'); } catch (e) {}
        return false;
      }
      return localStorage.getItem('sv-hl-enabled') === '1';
    } catch (e) {
      return false;
    }
  }

  // ---------- constants ----------
  // Categories drive both the cognitive choice ("what kind of thing is this?")
  // and the visual colour. Forcing this single choice is the highest-value
  // moment in the feature — even a basic Year 11 student is pulled into
  // metacognition. Categories are cross-curricular by design.
  var CATEGORIES = [
    { id: 'fact',     label: 'Key fact', short: 'Fact',    color: 'yellow', bg: '#fef08a', mark: '#fef9c3', hint: 'Dates, names, terms, formulas, quotes — facts to memorise.' },
    { id: 'why',      label: 'Why',      short: 'Why',     color: 'green',  bg: '#bbf7d0', mark: '#dcfce7', hint: "Causes, reasons, mechanisms, derivations, the writer's intent." },
    { id: 'so-what',  label: 'So what',  short: 'So what', color: 'pink',   bg: '#fbcfe8', mark: '#fce7f3', hint: 'Consequences, applications, exam relevance, links to themes.' },
    { id: 'question', label: 'Question', short: 'Q',       color: 'blue',   bg: '#bfdbfe', mark: '#dbeafe', hint: "Something I don't understand or want to follow up." }
  ];
  var DEFAULT_CATEGORY = 'fact';
  var CONTEXT_LEN = 30;
  var STORAGE_PREFIX = 'sv-hl:';
  var INDEX_KEY = 'sv-hl-index';

  function categoryFor(id) {
    for (var i = 0; i < CATEGORIES.length; i++) if (CATEGORIES[i].id === id) return CATEGORIES[i];
    return CATEGORIES[0];
  }

  // Legacy highlights only have `color`. Map back so they render & group
  // correctly under the new system.
  function categoryFromColor(color) {
    if (color === 'green') return 'why';
    if (color === 'pink') return 'so-what';
    if (color === 'blue') return 'question';
    return 'fact';
  }

  function getCategoryId(hl) {
    return hl && hl.category ? hl.category : categoryFromColor(hl && hl.color);
  }

  // Per-lesson bespoke definitions when present, generic hint otherwise.
  // Real pipeline will populate window._lessonCategoryDefinitions via
  // lesson-loader.js from a settings.category_definitions JSONB column.
  function getHintFor(catId) {
    var defs = window._lessonCategoryDefinitions;
    if (defs && defs[catId]) return defs[catId];
    return categoryFor(catId).hint;
  }

  // Back-compat: callers passing a legacy colour id still resolve to a category.
  function colorFor(id) { return categoryFor(id); }

  // ---------- KO Mode (lesson-task scaffolding) ----------
  // Optional mode the student opts into from the lesson checklist. Renders
  // a small floating card in the top-right showing the current focus
  // category (in colour), four clickable progress dots, and View all /
  // Exit actions. Highlighter cursor + yellow ::selection on the article.
  // Mode is global (persists across lesson navigation until exited).
  var KO_MODE_KEY = 'sv-hl-ko-mode';
  var KO_TUTORIAL_KEY = 'sv-ko-tutorial-done';
  var koCardEl = null;
  var koTutorialEl = null;
  var koExplicitFocus = null;  // set when user clicks a dot to override default

  function isKoModeActive() {
    try { return localStorage.getItem(KO_MODE_KEY) === '1'; } catch (e) { return false; }
  }

  function getCategoryCountsForLesson(lessonId) {
    var counts = { fact: 0, why: 0, 'so-what': 0, question: 0 };
    var list = getHighlights(lessonId);
    for (var i = 0; i < list.length; i++) {
      var c = getCategoryId(list[i]);
      if (counts.hasOwnProperty(c)) counts[c]++;
    }
    return counts;
  }

  function isLessonOrganised(lessonId) {
    lessonId = lessonId || window._lessonId;
    if (!lessonId) return false;
    var c = getCategoryCountsForLesson(lessonId);
    return c.fact >= 1 && c.why >= 1 && c['so-what'] >= 1 && c.question >= 1;
  }

  // Resolve the currently-focused category: explicit user pick if set,
  // otherwise the first category that's still empty on this lesson.
  function getKoFocus() {
    if (koExplicitFocus) return koExplicitFocus;
    if (!window._lessonId) return 'fact';
    var counts = getCategoryCountsForLesson(window._lessonId);
    for (var i = 0; i < CATEGORIES.length; i++) {
      if (counts[CATEGORIES[i].id] === 0) return CATEGORIES[i].id;
    }
    return 'fact';  // all full — default to fact for adding more
  }

  function setKoFocus(catId) {
    koExplicitFocus = catId;
    refreshKoCard();
  }

  function buildKoCard() {
    if (koCardEl) return koCardEl;
    koCardEl = document.createElement('div');
    koCardEl.className = 'sv-ko-card';
    koCardEl.innerHTML =
      '<div class="sv-ko-card-header">' +
        '<div class="sv-ko-card-title">' +
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>' +
          '<span>Knowledge organiser</span>' +
        '</div>' +
        '<button class="sv-ko-card-exit" type="button" aria-label="Exit mode" title="Exit mode">' +
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' +
        '</button>' +
      '</div>' +
      '<div class="sv-ko-card-focus-label">Next up</div>' +
      '<div class="sv-ko-card-focus" data-focus-chip>' +
        '<span class="sv-ko-card-focus-dot"></span>' +
        '<div class="sv-ko-card-focus-text">' +
          '<div class="sv-ko-card-focus-name">Key fact</div>' +
          '<div class="sv-ko-card-focus-hint">Dates, names, terms, formulas, quotes — facts to memorise.</div>' +
        '</div>' +
      '</div>' +
      '<div class="sv-ko-card-switch-label">Or pick another:</div>' +
      '<div class="sv-ko-card-dots">' +
        CATEGORIES.map(function (c) {
          return '<button class="sv-ko-dot sv-ko-dot--' + c.id + '" type="button" data-cat-dot="' + c.id + '" title="' + c.label + '" aria-label="Focus on ' + c.label + '">' +
                   '<span class="sv-ko-dot-swatch"></span>' +
                   '<span class="sv-ko-dot-name">' + c.label + '</span>' +
                   '<span class="sv-ko-dot-count">0</span>' +
                 '</button>';
        }).join('') +
      '</div>' +
      '<div class="sv-ko-card-actions">' +
        '<button class="sv-ko-card-link sv-ko-card-view-lesson" type="button">View these</button>' +
        '<a class="sv-ko-card-link" href="/highlights.html">All lessons →</a>' +
      '</div>' +
      '<div class="sv-ko-card-complete-banner">' +
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>' +
        'Lesson organised — well done.' +
      '</div>';
    document.body.appendChild(koCardEl);
    koCardEl.querySelector('.sv-ko-card-exit').addEventListener('click', exitKoMode);
    koCardEl.querySelector('.sv-ko-card-view-lesson').addEventListener('click', function () {
      if (typeof openModal === 'function') openModal();
    });
    koCardEl.querySelectorAll('.sv-ko-dot').forEach(function (dot) {
      dot.addEventListener('click', function () {
        setKoFocus(dot.getAttribute('data-cat-dot'));
      });
    });
    // Drag-to-move via the header (desktop only — mobile uses CSS bottom snap)
    koCardEl.querySelector('.sv-ko-card-header').addEventListener('mousedown', startKoDrag);
    applyKoPos();
    return koCardEl;
  }

  // ---------- KO card drag-to-move ----------
  var KO_POS_KEY = 'sv-ko-card-pos';
  var koDragState = null;

  function loadKoPos() {
    try { return JSON.parse(localStorage.getItem(KO_POS_KEY)) || null; } catch (e) { return null; }
  }
  function saveKoPos(pos) {
    try { localStorage.setItem(KO_POS_KEY, JSON.stringify(pos)); } catch (e) {}
  }

  // Clamp x/y so the card stays fully on-screen (8px margin on every side).
  function clampKoPos(x, y) {
    if (!koCardEl) return { x: x, y: y };
    var maxX = window.innerWidth - koCardEl.offsetWidth - 8;
    var maxY = window.innerHeight - koCardEl.offsetHeight - 8;
    return {
      x: Math.max(8, Math.min(x, maxX)),
      y: Math.max(8, Math.min(y, maxY))
    };
  }

  function applyKoPos() {
    if (!koCardEl) return;
    if (window.innerWidth <= 768) return;  // mobile: CSS handles positioning
    var pos = loadKoPos();
    if (!pos) return;
    var c = clampKoPos(pos.x, pos.y);
    koCardEl.style.left = c.x + 'px';
    koCardEl.style.top = c.y + 'px';
    koCardEl.style.right = 'auto';
  }

  function startKoDrag(evt) {
    if (window.innerWidth <= 768) return;
    // Don't start drag on the exit button or any other interactive child
    if (evt.target.closest('button, a')) return;
    evt.preventDefault();
    var rect = koCardEl.getBoundingClientRect();
    koDragState = {
      offsetX: evt.clientX - rect.left,
      offsetY: evt.clientY - rect.top
    };
    // Snap from right-anchored to left-anchored so we can drive position via left/top
    koCardEl.style.left = rect.left + 'px';
    koCardEl.style.top = rect.top + 'px';
    koCardEl.style.right = 'auto';
    koCardEl.classList.add('sv-ko-card--dragging');
    document.addEventListener('mousemove', onKoDrag);
    document.addEventListener('mouseup', endKoDrag);
  }

  function onKoDrag(evt) {
    if (!koDragState) return;
    var c = clampKoPos(
      evt.clientX - koDragState.offsetX,
      evt.clientY - koDragState.offsetY
    );
    koCardEl.style.left = c.x + 'px';
    koCardEl.style.top = c.y + 'px';
  }

  function endKoDrag() {
    if (!koDragState) return;
    document.removeEventListener('mousemove', onKoDrag);
    document.removeEventListener('mouseup', endKoDrag);
    koCardEl.classList.remove('sv-ko-card--dragging');
    saveKoPos({
      x: parseFloat(koCardEl.style.left) || 0,
      y: parseFloat(koCardEl.style.top) || 0
    });
    koDragState = null;
  }

  function setKoFocusBodyClass(focusId) {
    var b = document.body;
    ['fact', 'why', 'so-what', 'question'].forEach(function (c) {
      b.classList.toggle('sv-hl-ko-focus-' + c, c === focusId);
    });
  }

  function refreshKoCard() {
    if (!koCardEl) return;
    if (!window._lessonId) return;
    var counts = getCategoryCountsForLesson(window._lessonId);
    var focusId = getKoFocus();
    var focusCat = categoryFor(focusId);
    setKoFocusBodyClass(focusId);
    // Update dots
    for (var i = 0; i < CATEGORIES.length; i++) {
      var c = CATEGORIES[i];
      var dot = koCardEl.querySelector('[data-cat-dot="' + c.id + '"]');
      if (!dot) continue;
      var count = counts[c.id];
      dot.querySelector('.sv-ko-dot-count').textContent = count;
      dot.classList.toggle('sv-ko-dot--done', count >= 1);
      dot.classList.toggle('sv-ko-dot--focus', c.id === focusId);
    }
    // Update focus chip
    koCardEl.querySelector('.sv-ko-card-focus-name').textContent = focusCat.label;
    koCardEl.querySelector('.sv-ko-card-focus-hint').textContent = getHintFor(focusCat.id);
    var focusEl = koCardEl.querySelector('[data-focus-chip]');
    focusEl.className = 'sv-ko-card-focus sv-ko-card-focus--' + focusId;
    koCardEl.classList.toggle('sv-ko-card--complete', isLessonOrganised());
  }

  // ---------- KO Mode tutorial ----------
  // Two related triggers, same modal:
  //   1. First time ever (any subject) — gates on KO_TUTORIAL_KEY
  //   2. First time on each NEW subject thereafter — gates on a per-subject
  //      sv-ko-subject-seen-{slug} flag. Shows subject-specific framing.
  // The modal's heading + intro change depending on which trigger fired; the
  // four category cards always render with the current lesson's bespoke
  // definitions (via getHintFor) so they're subject-appropriate either way.
  function subjectOrientationKey() {
    var slug = window._subjectSlug;
    if (!slug) return null;
    return 'sv-ko-subject-seen-' + slug;
  }

  function buildKoTutorial() {
    if (koTutorialEl) return koTutorialEl;
    koTutorialEl = document.createElement('div');
    koTutorialEl.className = 'sv-ko-tutorial';
    koTutorialEl.innerHTML =
      '<div class="sv-ko-tutorial-backdrop"></div>' +
      '<div class="sv-ko-tutorial-panel" role="dialog" aria-modal="true" aria-labelledby="sv-ko-tutorial-title">' +
        '<h2 id="sv-ko-tutorial-title" class="sv-ko-tutorial-heading">Building a knowledge organiser</h2>' +
        '<p class="sv-ko-tutorial-intro">As you read this lesson, find at least one highlight for each of the four categories. The colour you pick is the cognitive move — what kind of thinking the highlight represents.</p>' +
        '<div class="sv-ko-tutorial-cards"></div>' +
        '<p class="sv-ko-tutorial-tip"><strong>Tip:</strong> when you select text in this mode, the highlight is created in the focused colour straight away and the note box pops up. Your notes are what make this a revision aid you can actually study from.</p>' +
        '<div class="sv-ko-tutorial-actions">' +
          '<button class="sv-ko-tutorial-go" type="button">Got it — let me start</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(koTutorialEl);
    koTutorialEl.querySelector('.sv-ko-tutorial-backdrop').addEventListener('click', hideKoTutorial);
    koTutorialEl.querySelector('.sv-ko-tutorial-go').addEventListener('click', function () {
      try {
        localStorage.setItem(KO_TUTORIAL_KEY, '1');
        var sk = subjectOrientationKey();
        if (sk) localStorage.setItem(sk, '1');
      } catch (e) {}
      hideKoTutorial();
    });
    return koTutorialEl;
  }

  // Re-render the four category cards with whatever definitions are current
  // for this lesson (subject-specific if available, generic otherwise).
  function refreshTutorialCards() {
    if (!koTutorialEl) return;
    var cards = koTutorialEl.querySelector('.sv-ko-tutorial-cards');
    cards.innerHTML = CATEGORIES.map(function (c) {
      return '<div class="sv-ko-tutorial-card sv-ko-tutorial-card--' + c.id + '">' +
               '<div class="sv-ko-tutorial-card-header">' +
                 '<span class="sv-ko-tutorial-card-dot"></span>' +
                 '<span class="sv-ko-tutorial-card-name">' + c.label + '</span>' +
               '</div>' +
               '<p class="sv-ko-tutorial-card-hint">' + getHintFor(c.id) + '</p>' +
             '</div>';
    }).join('');
  }

  function showKoTutorial() {
    buildKoTutorial();
    // Heading + intro vary by trigger: first-time vs new-subject orientation
    var firstTimeDone = false;
    try { firstTimeDone = localStorage.getItem(KO_TUTORIAL_KEY) === '1'; } catch (e) {}
    var subjectName = window._subjectName || '';
    var headingEl = koTutorialEl.querySelector('.sv-ko-tutorial-heading');
    var introEl = koTutorialEl.querySelector('.sv-ko-tutorial-intro');
    if (firstTimeDone && subjectName) {
      // Per-subject orientation
      headingEl.textContent = subjectName + ' — knowledge organiser';
      introEl.textContent = 'This is your first knowledge organiser for ' + subjectName + '. The four categories work a little differently in each subject — here\'s what each one means here:';
    } else {
      // First-time platform intro
      headingEl.textContent = 'Building a knowledge organiser';
      introEl.textContent = 'As you read this lesson, find at least one highlight for each of the four categories. The colour you pick is the cognitive move — what kind of thinking the highlight represents.';
    }
    refreshTutorialCards();
    koTutorialEl.classList.add('sv-ko-tutorial--open');
  }

  function hideKoTutorial() {
    if (koTutorialEl) koTutorialEl.classList.remove('sv-ko-tutorial--open');
  }

  function maybeShowKoTutorialOnFirstEntry() {
    var firstTimeDone = false;
    var subjectKey = null;
    var subjectSeen = false;
    try {
      firstTimeDone = localStorage.getItem(KO_TUTORIAL_KEY) === '1';
      subjectKey = subjectOrientationKey();
      if (subjectKey) subjectSeen = localStorage.getItem(subjectKey) === '1';
    } catch (e) { return; }
    // Nothing to show if both flags satisfied (or first-time done and we
    // can't determine subject for per-subject tracking)
    if (firstTimeDone && (subjectSeen || !subjectKey)) return;
    setTimeout(showKoTutorial, 200);  // small defer so the card paints first
  }

  function enterKoMode() {
    try { localStorage.setItem(KO_MODE_KEY, '1'); } catch (e) {}
    try { localStorage.setItem('sv-hl-enabled', '1'); } catch (e) {}
    document.body.classList.add('sv-hl-ko-mode');
    // Make sure the rest of the feature is wired up
    if (!bootstrapped) bootstrap();
    buildKoCard();
    koCardEl.style.display = 'block';
    koExplicitFocus = null;  // fresh entry — use auto-advancing default
    refreshKoCard();
    maybeShowKoTutorialOnFirstEntry();
  }

  function exitKoMode() {
    try { localStorage.removeItem(KO_MODE_KEY); } catch (e) {}
    document.body.classList.remove('sv-hl-ko-mode');
    ['fact', 'why', 'so-what', 'question'].forEach(function (c) {
      document.body.classList.remove('sv-hl-ko-focus-' + c);
    });
    if (koCardEl) koCardEl.style.display = 'none';
  }

  // Fired after any change to highlights. The lesson-progress checklist
  // listens for this to auto-tick the "Build a knowledge organiser" task.
  function notifyHighlightsChanged() {
    refreshKoCard();
    try {
      document.dispatchEvent(new CustomEvent('sv-hl-changed', {
        detail: { lessonId: window._lessonId, isOrganised: isLessonOrganised() }
      }));
    } catch (e) {}
  }

  // Expose for the checklist & external triggers
  window.svEnterKoMode = enterKoMode;
  window.svExitKoMode = exitKoMode;
  window.svIsLessonOrganised = isLessonOrganised;
  window.svIsKoModeActive = isKoModeActive;

  // ---------- storage ----------
  function lessonKey(lessonId) { return STORAGE_PREFIX + lessonId; }

  function getHighlights(lessonId) {
    try {
      var raw = localStorage.getItem(lessonKey(lessonId));
      return raw ? JSON.parse(raw) : [];
    } catch (e) { return []; }
  }

  function saveHighlights(lessonId, list) {
    try {
      if (list && list.length) {
        localStorage.setItem(lessonKey(lessonId), JSON.stringify(list));
      } else {
        localStorage.removeItem(lessonKey(lessonId));
      }
      updateIndex(lessonId, list ? list.length : 0);
    } catch (e) {
      console.warn('[highlights] save failed', e);
    }
    // Notify listeners (lesson checklist, KO banner). Defined later in the file.
    if (typeof notifyHighlightsChanged === 'function') notifyHighlightsChanged();
  }

  function readIndex() {
    try {
      var raw = localStorage.getItem(INDEX_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) { return []; }
  }

  function updateIndex(lessonId, count) {
    var idx = readIndex();
    var existing = -1;
    for (var i = 0; i < idx.length; i++) {
      if (idx[i].lesson_id === lessonId) { existing = i; break; }
    }
    if (count === 0) {
      if (existing >= 0) idx.splice(existing, 1);
    } else {
      var entry = {
        lesson_id: lessonId,
        lesson_title: document.getElementById('lesson-title')
          ? (document.getElementById('lesson-title').textContent || '').trim()
          : '',
        subject_name: window._subjectName || '',
        subject_slug: window._subjectSlug || '',
        unit_name: window._unitName || '',
        unit_slug: window._unitSlug || '',
        lesson_url: window.location.pathname,
        count: count,
        last_updated: new Date().toISOString()
      };
      if (existing >= 0) idx[existing] = entry;
      else idx.push(entry);
    }
    try { localStorage.setItem(INDEX_KEY, JSON.stringify(idx)); } catch (e) {}
  }

  // ---------- text normalization & anchoring ----------
  // Glossary popups (.term-popup) are children of .term elements and contain
  // the definition text. They're invisible (opacity:0) but live in the DOM,
  // so range.toString() and container.textContent both include them. We must
  // exclude them everywhere — otherwise selections leak the definition into
  // the highlight, and marks end up wrapping text inside the popup (which
  // gives an unreadable yellow-on-white when the popup pops up).
  var EXCLUDED_FROM_HIGHLIGHT = '.term-popup';

  function normalize(s) {
    return (s || '').replace(/\s+/g, ' ').trim();
  }

  function isExcludedTextNode(node) {
    return !!(node.parentElement && node.parentElement.closest(EXCLUDED_FROM_HIGHLIGHT));
  }

  // Like Element.textContent, but skips text inside EXCLUDED_FROM_HIGHLIGHT
  // selectors so the offsets we compute match what the user actually sees.
  function cleanTextContent(container) {
    if (!container) return '';
    var parts = [];
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return isExcludedTextNode(n) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = walker.nextNode())) parts.push(n.nodeValue);
    return parts.join('');
  }

  function getContainerText() {
    var c = document.getElementById('study-notes');
    return c ? cleanTextContent(c) : '';
  }

  // Like range.toString(), but skips text inside excluded popups. Range.toString()
  // is pure DOM concatenation and ignores user-select:none, so cross-element
  // selections (e.g. a keyword + adjacent words) would otherwise glue the popup's
  // definition into the middle of the snippet.
  function cleanRangeText(range) {
    if (!range || range.collapsed) return '';
    var container = document.getElementById('study-notes');
    if (!container) return range.toString();
    var startNode = range.startContainer;
    var endNode = range.endContainer;
    var parts = [];
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!range.intersectsNode(n)) return NodeFilter.FILTER_REJECT;
        if (isExcludedTextNode(n)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = walker.nextNode())) {
      var text = n.nodeValue;
      var s = (n === startNode) ? range.startOffset : 0;
      var e = (n === endNode) ? range.endOffset : text.length;
      if (e > s) parts.push(text.substring(s, e));
    }
    return parts.join('');
  }

  // Build context anchor for a freshly-made selection
  function buildAnchor(range) {
    var container = document.getElementById('study-notes');
    if (!container || !container.contains(range.commonAncestorContainer)) return null;
    var fullText = cleanTextContent(container);
    var selected = cleanRangeText(range);
    // Locate offset by walking text nodes and accumulating
    var offset = textOffsetOfRangeStart(container, range);
    if (offset < 0) return null;
    var prefix = fullText.substring(Math.max(0, offset - CONTEXT_LEN), offset);
    var suffix = fullText.substring(offset + selected.length, offset + selected.length + CONTEXT_LEN);
    return {
      text: normalize(selected),
      prefix: normalize(prefix),
      suffix: normalize(suffix)
    };
  }

  function textOffsetOfRangeStart(container, range) {
    // Walk text nodes (skipping excluded popup content) accumulating length
    // until we reach the range's start node
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return isExcludedTextNode(n) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var total = 0;
    var n;
    while ((n = walker.nextNode())) {
      if (n === range.startContainer) return total + range.startOffset;
      total += n.nodeValue.length;
    }
    // Fallback: search by clean text content
    var snippet = cleanRangeText(range);
    var idx = cleanTextContent(container).indexOf(snippet);
    return idx;
  }

  // Find a range in the live DOM matching a stored anchor
  function findRangeForAnchor(anchor) {
    var container = document.getElementById('study-notes');
    if (!container) return null;
    var normalizedFull = cleanTextContent(container);
    var needle = anchor.text;
    if (!needle) return null;
    // Find candidate occurrences and disambiguate by prefix/suffix when possible
    var candidates = [];
    var lower = normalizedFull;
    var from = 0;
    while (true) {
      var idx = lower.indexOf(needle, from);
      if (idx < 0) break;
      candidates.push(idx);
      from = idx + 1;
    }
    if (!candidates.length) {
      // Fallback: try whitespace-collapsed match
      var collapsed = normalize(normalizedFull);
      var pos = collapsed.indexOf(needle);
      if (pos < 0) return null;
      return rangeFromCollapsedOffset(container, pos, needle.length);
    }
    var best = candidates[0];
    var bestScore = -1;
    for (var i = 0; i < candidates.length; i++) {
      var o = candidates[i];
      var pre = normalize(normalizedFull.substring(Math.max(0, o - CONTEXT_LEN), o));
      var suf = normalize(normalizedFull.substring(o + needle.length, o + needle.length + CONTEXT_LEN));
      var score = 0;
      if (anchor.prefix && pre.indexOf(anchor.prefix.substr(-15)) >= 0) score += 2;
      if (anchor.suffix && suf.indexOf(anchor.suffix.substr(0, 15)) >= 0) score += 2;
      if (score > bestScore) { bestScore = score; best = o; }
    }
    return rangeFromOffset(container, best, needle.length);
  }

  // Build a Range from a character offset measured against textContent
  function rangeFromOffset(container, charOffset, length) {
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return isExcludedTextNode(n) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var consumed = 0;
    var startNode = null, startNodeOffset = 0;
    var endNode = null, endNodeOffset = 0;
    var n;
    while ((n = walker.nextNode())) {
      var len = n.nodeValue.length;
      if (!startNode && consumed + len > charOffset) {
        startNode = n;
        startNodeOffset = charOffset - consumed;
      }
      if (consumed + len >= charOffset + length) {
        endNode = n;
        endNodeOffset = (charOffset + length) - consumed;
        break;
      }
      consumed += len;
    }
    if (!startNode || !endNode) return null;
    var range = document.createRange();
    range.setStart(startNode, startNodeOffset);
    range.setEnd(endNode, endNodeOffset);
    return range;
  }

  function rangeFromCollapsedOffset(container, collapsedOffset, length) {
    // Walk text nodes, tracking BOTH the raw offset and the collapsed offset, so
    // we can re-anchor when DOM whitespace has changed since the highlight was made.
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return isExcludedTextNode(n) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var raw = 0, collapsed = 0;
    var startNode = null, startNodeOffset = 0;
    var endNode = null, endNodeOffset = 0;
    var n;
    while ((n = walker.nextNode())) {
      var text = n.nodeValue;
      for (var i = 0; i < text.length; i++) {
        var ch = text[i];
        var isWs = /\s/.test(ch);
        // skip leading whitespace runs in collapsed form (approximation)
        var advance = isWs ? (i === 0 || /\s/.test(text[i - 1]) ? 0 : 1) : 1;
        if (!startNode && collapsed >= collapsedOffset) {
          startNode = n;
          startNodeOffset = i;
        }
        if (startNode && collapsed >= collapsedOffset + length) {
          endNode = n;
          endNodeOffset = i;
          break;
        }
        collapsed += advance;
        raw++;
      }
      if (endNode) break;
    }
    if (!startNode || !endNode) return null;
    var range = document.createRange();
    range.setStart(startNode, startNodeOffset);
    range.setEnd(endNode, endNodeOffset);
    return range;
  }

  // ---------- mark wrapping (handles cross-element ranges) ----------
  function wrapRangeInMarks(range, hl) {
    if (!range || range.collapsed) return [];
    var marks = [];
    var startNode = range.startContainer;
    var endNode = range.endContainer;
    var startOff = range.startOffset;
    var endOff = range.endOffset;
    // Collect text nodes intersecting the range
    var nodes = [];
    var container = document.getElementById('study-notes');
    if (!container) return [];
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!range.intersectsNode(node)) return NodeFilter.FILTER_REJECT;
        if (isExcludedTextNode(node)) return NodeFilter.FILTER_REJECT;
        // Don't re-wrap text already inside another sv-hl mark
        var p = node.parentNode;
        while (p && p !== container) {
          if (p.classList && p.classList.contains('sv-hl')) return NodeFilter.FILTER_REJECT;
          p = p.parentNode;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = walker.nextNode())) nodes.push(n);
    if (!nodes.length) return [];

    for (var i = 0; i < nodes.length; i++) {
      var node = nodes[i];
      var text = node.nodeValue;
      var s = (node === startNode) ? startOff : 0;
      var e = (node === endNode) ? endOff : text.length;
      if (e <= s) continue;
      // Split out the highlighted segment
      var middle = node.splitText(s);
      // splitText returns the part AFTER s, so we then split at (e - s)
      if (e - s < middle.nodeValue.length) middle.splitText(e - s);
      var mark = document.createElement('mark');
      var catId = getCategoryId(hl);
      var catColor = hl.color || categoryFor(catId).color;
      mark.className = 'sv-hl sv-hl--' + catColor;
      mark.setAttribute('data-hl-id', hl.id);
      mark.setAttribute('data-hl-color', catColor);
      mark.setAttribute('data-hl-category', catId);
      if (hl.note) mark.setAttribute('data-hl-has-note', '1');
      middle.parentNode.insertBefore(mark, middle);
      mark.appendChild(middle);
      marks.push(mark);
    }
    return marks;
  }

  function unwrapMark(mark) {
    var parent = mark.parentNode;
    while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
    parent.removeChild(mark);
    if (parent.normalize) parent.normalize();
  }

  function unwrapHighlightById(hlId) {
    var marks = document.querySelectorAll('mark.sv-hl[data-hl-id="' + cssEscape(hlId) + '"]');
    marks.forEach(unwrapMark);
  }

  function cssEscape(s) {
    return String(s).replace(/["\\]/g, '\\$&');
  }

  // ---------- popover UI ----------
  var popoverEl = null;
  var activeHighlight = null; // when editing an existing one
  var pendingRange = null;    // when creating a new one
  var pendingAnchor = null;

  function buildPopover() {
    if (popoverEl) return popoverEl;
    popoverEl = document.createElement('div');
    popoverEl.className = 'sv-hl-popover';
    popoverEl.setAttribute('role', 'dialog');
    popoverEl.setAttribute('aria-label', 'Highlight options');
    popoverEl.innerHTML =
      '<div class="sv-hl-popover-prompt">What kind of highlight is this?</div>' +
      '<div class="sv-hl-popover-cats">' +
        CATEGORIES.map(function (c) {
          return '<button class="sv-hl-cat sv-hl-cat--' + c.id + '" type="button" data-cat="' + c.id + '" aria-pressed="false" title="' + c.hint + '">' +
            '<span class="sv-hl-cat-dot"></span>' +
            '<span class="sv-hl-cat-label">' + c.label + '</span>' +
          '</button>';
        }).join('') +
      '</div>' +
      '<div class="sv-hl-popover-quick-header">' +
        '<span class="sv-hl-popover-quick-dot"></span>' +
        '<span class="sv-hl-popover-quick-text">Marked as <strong class="sv-hl-popover-quick-name">Key fact</strong> — add a note (optional)</span>' +
      '</div>' +
      '<div class="sv-hl-note-row" hidden>' +
        '<textarea class="sv-hl-note" rows="3" maxlength="1000" placeholder="Add a note (optional)…"></textarea>' +
        '<div class="sv-hl-note-actions">' +
          '<button class="sv-hl-icon-btn sv-hl-delete" type="button" title="Delete highlight" hidden>' +
            '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-2 14a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/></svg>' +
          '</button>' +
          '<button class="sv-hl-btn sv-hl-cancel" type="button">Done</button>' +
          '<button class="sv-hl-btn sv-hl-save sv-hl-btn--primary" type="button">Save note</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(popoverEl);

    // Category button click — create/update highlight + reveal note row
    popoverEl.querySelectorAll('.sv-hl-cat').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var catId = btn.getAttribute('data-cat');
        applyOrUpdateCategory(catId);
        popoverEl.querySelectorAll('.sv-hl-cat').forEach(function (b) {
          b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
        });
        var prompt = popoverEl.querySelector('.sv-hl-popover-prompt');
        if (prompt) prompt.style.display = 'none';
        var row = popoverEl.querySelector('.sv-hl-note-row');
        row.hidden = false;
        popoverEl.querySelector('.sv-hl-note').focus();
      });
    });
    // Save note
    popoverEl.querySelector('.sv-hl-save').addEventListener('click', function () {
      var note = popoverEl.querySelector('.sv-hl-note').value;
      saveNote(note);
      hidePopover();
    });
    popoverEl.querySelector('.sv-hl-cancel').addEventListener('click', function () {
      hidePopover();
    });
    // Delete
    popoverEl.querySelector('.sv-hl-delete').addEventListener('click', function () {
      if (activeHighlight) deleteHighlight(activeHighlight.id);
      hidePopover();
    });
    return popoverEl;
  }

  function showPopoverAt(rect, opts) {
    buildPopover();
    var deleteBtn = popoverEl.querySelector('.sv-hl-delete');
    deleteBtn.hidden = !opts.canDelete;
    var noteRow = popoverEl.querySelector('.sv-hl-note-row');
    var noteEl = popoverEl.querySelector('.sv-hl-note');
    noteEl.value = opts.note || '';
    var activeCat = opts.category || '';
    popoverEl.querySelectorAll('.sv-hl-cat').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-cat') === activeCat ? 'true' : 'false');
    });
    var prompt = popoverEl.querySelector('.sv-hl-popover-prompt');
    if (prompt) prompt.style.display = activeCat ? 'none' : '';
    // KO-quick mode: skip the category picker entirely, jump straight to note.
    // CSS hides the prompt + cat picker, shows a small "Marked as X" header.
    var koQuick = !!opts.koQuickMode;
    popoverEl.classList.toggle('sv-hl-popover--ko-quick', koQuick);
    if (koQuick) {
      var qc = categoryFor(activeCat);
      popoverEl.querySelector('.sv-hl-popover-quick-dot').setAttribute('data-cat', qc.id);
      popoverEl.querySelector('.sv-hl-popover-quick-name').textContent = qc.label;
      noteRow.hidden = false;
    } else {
      noteRow.hidden = !(opts.note && opts.note.length);
    }
    popoverEl.classList.remove('sv-hl-hidden');
    // Position above the selection if there's room, else below
    popoverEl.style.visibility = 'hidden';
    popoverEl.style.display = 'block';
    var ph = popoverEl.offsetHeight;
    var pw = popoverEl.offsetWidth;
    var spaceAbove = rect.top;
    var top, left;
    if (spaceAbove > ph + 12) {
      top = window.scrollY + rect.top - ph - 8;
    } else {
      top = window.scrollY + rect.bottom + 8;
    }
    left = window.scrollX + rect.left + (rect.width / 2) - (pw / 2);
    // Clamp horizontally to viewport
    var maxLeft = window.scrollX + document.documentElement.clientWidth - pw - 12;
    var minLeft = window.scrollX + 12;
    if (left > maxLeft) left = maxLeft;
    if (left < minLeft) left = minLeft;
    popoverEl.style.top = top + 'px';
    popoverEl.style.left = left + 'px';
    popoverEl.style.visibility = 'visible';
    if (koQuick) {
      // Focus the note textarea so students can just start typing
      setTimeout(function () { noteEl.focus(); }, 0);
    }
  }

  function hidePopover() {
    if (popoverEl) {
      popoverEl.style.display = 'none';
      popoverEl.classList.add('sv-hl-hidden');
    }
    activeHighlight = null;
    pendingRange = null;
    pendingAnchor = null;
  }

  // ---------- create / update / delete flow ----------
  function applyOrUpdateCategory(catId) {
    var lessonId = window._lessonId;
    if (!lessonId) return;
    var cat = categoryFor(catId);
    if (activeHighlight) {
      // Update existing — change category + matching colour
      var list = getHighlights(lessonId);
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === activeHighlight.id) {
          list[i].category = cat.id;
          list[i].color = cat.color;
          list[i].updatedAt = new Date().toISOString();
          activeHighlight = list[i];
          break;
        }
      }
      saveHighlights(lessonId, list);
      // Re-render marks: rotate the colour class
      var marks = document.querySelectorAll('mark.sv-hl[data-hl-id="' + cssEscape(activeHighlight.id) + '"]');
      marks.forEach(function (m) {
        CATEGORIES.forEach(function (c) { m.classList.remove('sv-hl--' + c.color); });
        m.classList.add('sv-hl--' + cat.color);
        m.setAttribute('data-hl-color', cat.color);
        m.setAttribute('data-hl-category', cat.id);
      });
      refreshFab();
    } else if (pendingRange && pendingAnchor) {
      // Create new
      var hl = {
        id: 'hl-' + Math.random().toString(36).slice(2, 10) + Date.now().toString(36),
        text: pendingAnchor.text,
        prefix: pendingAnchor.prefix,
        suffix: pendingAnchor.suffix,
        category: cat.id,
        color: cat.color,
        note: '',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
      var marks2 = wrapRangeInMarks(pendingRange, hl);
      if (!marks2.length) {
        console.warn('[highlights] could not wrap range');
        hidePopover();
        return;
      }
      var list2 = getHighlights(lessonId);
      list2.push(hl);
      saveHighlights(lessonId, list2);
      activeHighlight = hl;
      pendingRange = null;
      pendingAnchor = null;
      window.getSelection().removeAllRanges();
      refreshFab();
    }
  }

  function saveNote(note) {
    if (!activeHighlight) return;
    var lessonId = window._lessonId;
    var list = getHighlights(lessonId);
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === activeHighlight.id) {
        list[i].note = (note || '').trim();
        list[i].updatedAt = new Date().toISOString();
        break;
      }
    }
    saveHighlights(lessonId, list);
    // Update mark data attribute
    var marks = document.querySelectorAll('mark.sv-hl[data-hl-id="' + cssEscape(activeHighlight.id) + '"]');
    marks.forEach(function (m) {
      if (note && note.trim()) m.setAttribute('data-hl-has-note', '1');
      else m.removeAttribute('data-hl-has-note');
    });
    refreshFab();
  }

  function deleteHighlight(hlId) {
    var lessonId = window._lessonId;
    var list = getHighlights(lessonId).filter(function (h) { return h.id !== hlId; });
    saveHighlights(lessonId, list);
    unwrapHighlightById(hlId);
    refreshFab();
  }

  // ---------- floating pill (selection affordance) ----------
  // Two-step flow: drag-select shows a small "Highlight" pill → click it →
  // colour/note popover opens. Stops the popover from ambushing students on
  // every selection (read-aloud, copy-paste, screen reader) and gives a clear,
  // discoverable affordance.
  var pillEl = null;
  var pillRect = null;

  function buildPill() {
    if (pillEl) return pillEl;
    pillEl = document.createElement('button');
    pillEl.type = 'button';
    pillEl.className = 'sv-hl-pill';
    pillEl.setAttribute('aria-label', 'Highlight selection');
    pillEl.innerHTML =
      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>' +
      '<span>Highlight</span>';
    pillEl.addEventListener('mousedown', function (e) { e.preventDefault(); });
    pillEl.addEventListener('click', function (e) {
      e.stopPropagation();
      if (!pendingRange || !pendingAnchor) { hidePill(); return; }
      var rect = pillRect || pendingRange.getBoundingClientRect();
      hidePill();
      showPopoverAt(rect, { canDelete: false, note: '' });
    });
    document.body.appendChild(pillEl);
    return pillEl;
  }

  function showPillAt(rect, cursorPoint) {
    buildPill();
    pillRect = rect;
    pillEl.style.visibility = 'hidden';
    pillEl.style.display = 'inline-flex';
    var ph = pillEl.offsetHeight;
    var pw = pillEl.offsetWidth;
    var top, left;
    if (cursorPoint) {
      var belowOverflows = (cursorPoint.y + ph + 24) > window.innerHeight;
      top = belowOverflows
        ? window.scrollY + cursorPoint.y - ph - 12
        : window.scrollY + cursorPoint.y + 12;
      left = window.scrollX + cursorPoint.x - (pw / 2);
    } else {
      var spaceAbove = rect.top;
      top = (spaceAbove > ph + 12)
        ? window.scrollY + rect.top - ph - 8
        : window.scrollY + rect.bottom + 8;
      left = window.scrollX + rect.left + (rect.width / 2) - (pw / 2);
    }
    var maxLeft = window.scrollX + document.documentElement.clientWidth - pw - 12;
    var minLeft = window.scrollX + 12;
    if (left > maxLeft) left = maxLeft;
    if (left < minLeft) left = minLeft;
    pillEl.style.top = top + 'px';
    pillEl.style.left = left + 'px';
    pillEl.style.visibility = 'visible';
    pillEl.classList.add('sv-hl-pill--visible');
  }

  function hidePill() {
    if (pillEl) {
      pillEl.style.display = 'none';
      pillEl.classList.remove('sv-hl-pill--visible');
    }
    pillRect = null;
  }

  // ---------- selection handling ----------
  function onMouseUp(evt) {
    if (evt.target.closest && evt.target.closest('.sv-hl-popover')) return;
    if (evt.target.closest && evt.target.closest('.sv-hl-pill')) return;
    var cursorX, cursorY;
    if (evt.changedTouches && evt.changedTouches[0]) {
      cursorX = evt.changedTouches[0].clientX;
      cursorY = evt.changedTouches[0].clientY;
    } else if (typeof evt.clientX === 'number') {
      cursorX = evt.clientX;
      cursorY = evt.clientY;
    }
    setTimeout(function () {
      var sel = window.getSelection();
      if (!sel || sel.isCollapsed) { hidePill(); return; }
      var range = sel.getRangeAt(0);
      var container = document.getElementById('study-notes');
      if (!container || !container.contains(range.commonAncestorContainer)) { hidePill(); return; }
      var text = range.toString();
      if (!text || !text.trim()) { hidePill(); return; }
      // Generous cap — paragraphs at GCSE 15/16 reading level often run
      // 800-1200 chars, and selections spanning two paragraphs are a
      // perfectly reasonable study highlight. Cap is just to stop a stray
      // Ctrl+A from wrapping the entire lesson in one mark.
      if (text.length > 5000) { hidePill(); return; }
      var anchor = buildAnchor(range);
      if (!anchor) { hidePill(); return; }
      pendingRange = range.cloneRange();
      pendingAnchor = anchor;
      activeHighlight = null;
      // In KO mode, skip the pill + category picker entirely. The focus IS
      // the choice — create the highlight in the focused colour immediately
      // and pop the note textarea so the student just types.
      if (isKoModeActive()) {
        var rect = range.getBoundingClientRect();  // capture before pendingRange is cleared
        var focusId = getKoFocus();
        applyOrUpdateCategory(focusId);
        hidePill();
        showPopoverAt(rect, {
          canDelete: true,
          note: '',
          category: focusId,
          koQuickMode: true
        });
        return;
      }
      var cursorPoint = (typeof cursorX === 'number') ? { x: cursorX, y: cursorY } : null;
      showPillAt(range.getBoundingClientRect(), cursorPoint);
    }, 10);
  }

  // Capture-phase click handler runs BEFORE the narration jump-to-clip listener
  // that main.js attaches to [data-narration-id] paragraphs. Two responsibilities:
  // (1) open the popover when an existing highlight is clicked
  // (2) suppress the click that follows a drag-selection so narration doesn't fire
  function onMarkClick(evt) {
    var mark = evt.target.closest('mark.sv-hl');
    if (mark) {
      evt.preventDefault();
      evt.stopPropagation();
      var hlId = mark.getAttribute('data-hl-id');
      var lessonId = window._lessonId;
      var list = getHighlights(lessonId);
      var hl = null;
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === hlId) { hl = list[i]; break; }
      }
      if (!hl) return;
      activeHighlight = hl;
      pendingRange = null;
      pendingAnchor = null;
      showPopoverAt(mark.getBoundingClientRect(), { canDelete: true, note: hl.note || '', category: getCategoryId(hl) });
      return;
    }
    if (justDragged) {
      var sel = window.getSelection();
      if (sel && !sel.isCollapsed && sel.toString().trim().length > 0) {
        evt.stopPropagation();
      }
      justDragged = false;
    }
  }

  // Drag-detection: only suppress narration on real selections, not bare clicks
  var justDragged = false;
  var mouseDownX = 0;
  var mouseDownY = 0;
  function onMouseDownTracker(evt) {
    mouseDownX = evt.clientX;
    mouseDownY = evt.clientY;
    justDragged = false;
  }
  function onMouseMoveTracker(evt) {
    if (Math.abs(evt.clientX - mouseDownX) > 3 || Math.abs(evt.clientY - mouseDownY) > 3) {
      justDragged = true;
    }
  }

  function onDocClick(evt) {
    if (pillEl && pillEl.style.display !== 'none' && !pillEl.contains(evt.target)) {
      hidePill();
    }
    if (!popoverEl || popoverEl.style.display === 'none') return;
    if (popoverEl.contains(evt.target)) return;
    if (evt.target.closest && evt.target.closest('mark.sv-hl')) return;
    hidePopover();
  }

  function onKeyDown(evt) {
    if (evt.key === 'Escape') { hidePill(); hidePopover(); }
  }

  // ---------- rehydrate marks on load ----------
  function rehydrate() {
    var lessonId = window._lessonId;
    if (!lessonId) return;
    var list = getHighlights(lessonId);
    var rehydrated = 0;
    for (var i = 0; i < list.length; i++) {
      var hl = list[i];
      try {
        var range = findRangeForAnchor(hl);
        if (range) {
          var marks = wrapRangeInMarks(range, hl);
          if (marks.length) rehydrated++;
        }
      } catch (e) {
        console.warn('[highlights] could not rehydrate', hl.id, e);
      }
    }
    return rehydrated;
  }

  // ---------- floating action button + per-lesson modal ----------
  var fabEl = null;
  var modalEl = null;

  function refreshFab() {
    if (!fabEl) return;
    var n = getHighlights(window._lessonId).length;
    fabEl.querySelector('.sv-hl-fab-count').textContent = n;
    fabEl.style.display = 'inline-flex';
    fabEl.classList.toggle('sv-hl-fab--empty', n === 0);
  }

  function buildFab() {
    if (fabEl) return fabEl;
    var stack = document.createElement('div');
    stack.className = 'sv-hl-fab-stack';

    var allBtn = document.createElement('a');
    allBtn.className = 'sv-hl-fab sv-hl-fab--all';
    allBtn.href = '/highlights.html';
    allBtn.setAttribute('aria-label', 'All highlights across lessons');
    allBtn.innerHTML =
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h10"/></svg>' +
      '<span class="sv-hl-fab-label">All Highlights</span>';
    stack.appendChild(allBtn);

    fabEl = document.createElement('button');
    fabEl.className = 'sv-hl-fab sv-hl-fab--lesson';
    fabEl.type = 'button';
    fabEl.setAttribute('aria-label', 'Lesson highlights');
    fabEl.innerHTML =
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>' +
      '<span class="sv-hl-fab-label">Lesson Highlights</span>' +
      '<span class="sv-hl-fab-count">0</span>';
    fabEl.addEventListener('click', openModal);
    stack.appendChild(fabEl);

    document.body.appendChild(stack);
    return fabEl;
  }

  function openModal() {
    if (!modalEl) {
      modalEl = document.createElement('div');
      modalEl.className = 'sv-hl-modal';
      modalEl.innerHTML =
        '<div class="sv-hl-modal-backdrop"></div>' +
        '<div class="sv-hl-modal-panel" role="dialog" aria-modal="true" aria-label="My highlights">' +
          '<header class="sv-hl-modal-header">' +
            '<h2>My highlights</h2>' +
            '<a class="sv-hl-modal-allpages" href="/highlights.html">All lessons →</a>' +
            '<button class="sv-hl-modal-close" aria-label="Close">×</button>' +
          '</header>' +
          '<div class="sv-hl-modal-body"></div>' +
        '</div>';
      document.body.appendChild(modalEl);
      modalEl.querySelector('.sv-hl-modal-backdrop').addEventListener('click', closeModal);
      modalEl.querySelector('.sv-hl-modal-close').addEventListener('click', closeModal);
    }
    renderModalBody();
    modalEl.classList.add('sv-hl-modal--open');
  }

  function closeModal() {
    if (modalEl) modalEl.classList.remove('sv-hl-modal--open');
  }

  function renderModalBody() {
    var body = modalEl.querySelector('.sv-hl-modal-body');
    var list = getHighlights(window._lessonId);
    if (!list.length) {
      body.innerHTML =
        '<div class="sv-hl-modal-empty">' +
          '<p>No highlights on this lesson yet.</p>' +
          '<p class="sv-hl-modal-hint">Select any text in the lesson, pick a category (Key fact, Why, So what, or Question), and optionally write a note.</p>' +
        '</div>';
      return;
    }
    // Newest first
    list.sort(function (a, b) { return (b.createdAt || '').localeCompare(a.createdAt || ''); });
    body.innerHTML = list.map(function (h) {
      var cat = categoryFor(getCategoryId(h));
      var noteHtml = h.note
        ? '<p class="sv-hl-modal-note">' + escapeHtml(h.note) + '</p>'
        : '';
      return '<article class="sv-hl-modal-item" data-hl-id="' + escapeHtml(h.id) + '">' +
          '<div class="sv-hl-modal-cat-row">' +
            '<span class="sv-hl-modal-cat sv-hl-modal-cat--' + cat.id + '">' + escapeHtml(cat.label) + '</span>' +
          '</div>' +
          '<div class="sv-hl-modal-snippet" style="background:' + cat.mark + '">' +
            '<span class="sv-hl-modal-bar" style="background:' + cat.bg + '"></span>' +
            '<span class="sv-hl-modal-text">' + escapeHtml(h.text) + '</span>' +
          '</div>' +
          noteHtml +
          '<div class="sv-hl-modal-actions">' +
            '<button class="sv-hl-modal-jump" type="button">Jump to</button>' +
            '<button class="sv-hl-modal-delete" type="button">Delete</button>' +
          '</div>' +
        '</article>';
    }).join('');
    body.querySelectorAll('.sv-hl-modal-item').forEach(function (item) {
      var hlId = item.getAttribute('data-hl-id');
      item.querySelector('.sv-hl-modal-jump').addEventListener('click', function () {
        var firstMark = document.querySelector('mark.sv-hl[data-hl-id="' + cssEscape(hlId) + '"]');
        if (firstMark) {
          closeModal();
          firstMark.scrollIntoView({ behavior: 'smooth', block: 'center' });
          firstMark.classList.add('sv-hl--flash');
          setTimeout(function () { firstMark.classList.remove('sv-hl--flash'); }, 1500);
        }
      });
      item.querySelector('.sv-hl-modal-delete').addEventListener('click', function () {
        deleteHighlight(hlId);
        renderModalBody();
      });
    });
  }

  function escapeHtml(s) {
    return String(s || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // ---------- styles ----------
  function injectStyles() {
    if (document.getElementById('sv-hl-styles')) return;
    var s = document.createElement('style');
    s.id = 'sv-hl-styles';
    s.textContent =
      // Belt-and-braces: also tell the browser not to select glossary popups,
      // so even if our JS misses, the native selection won't pick them up.
      '.term-popup{user-select:none;-webkit-user-select:none}' +
      'mark.sv-hl{padding:0.05em 0;border-radius:3px;cursor:pointer;transition:filter .15s ease;color:#2d2a26}' +
      'mark.sv-hl:hover{filter:brightness(.96)}' +
      'mark.sv-hl--yellow{background:#fef9c3}' +
      'mark.sv-hl--green{background:#dcfce7}' +
      'mark.sv-hl--pink{background:#fce7f3}' +
      'mark.sv-hl--blue{background:#dbeafe}' +
      'body.dark-mode mark.sv-hl{color:#f5f1ec}' +
      'body.dark-mode mark.sv-hl--yellow{background:rgba(234,179,8,.55)}' +
      'body.dark-mode mark.sv-hl--green{background:rgba(34,197,94,.45)}' +
      'body.dark-mode mark.sv-hl--pink{background:rgba(236,72,153,.45)}' +
      'body.dark-mode mark.sv-hl--blue{background:rgba(59,130,246,.5)}' +
      'mark.sv-hl[data-hl-has-note]::after{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:currentColor;vertical-align:super;margin-left:2px;opacity:.5}' +
      'mark.sv-hl--flash{animation:sv-hl-flash 1.4s ease}' +
      '@keyframes sv-hl-flash{0%,100%{box-shadow:0 0 0 0 rgba(45,42,38,0)}30%{box-shadow:0 0 0 6px rgba(45,42,38,.25)}}' +
      // Popover (category picker)
      '.sv-hl-popover{position:absolute;z-index:9000;background:#fff;border:1px solid rgba(45,42,38,.12);border-radius:14px;box-shadow:0 12px 30px rgba(20,18,15,.18);padding:10px;font-family:Inter,system-ui,sans-serif;color:#2d2a26;min-width:260px;max-width:320px}' +
      'body.dark-mode .sv-hl-popover{background:#3a3631;color:#f5f1ec;border-color:rgba(245,241,236,.12)}' +
      '.sv-hl-popover-prompt{font-size:.72rem;color:#7a7367;text-align:center;margin-bottom:7px;letter-spacing:.04em;text-transform:uppercase;font-weight:600}' +
      'body.dark-mode .sv-hl-popover-prompt{color:#a59f95}' +
      '.sv-hl-popover-cats{display:grid;grid-template-columns:1fr 1fr;gap:5px}' +
      '.sv-hl-cat{display:flex;align-items:center;gap:7px;padding:7px 9px;border:1px solid rgba(45,42,38,.14);background:#fff;border-radius:9px;font-family:inherit;font-size:.84rem;font-weight:500;color:#2d2a26;cursor:pointer;text-align:left;transition:transform .1s ease,border-color .1s ease,background .1s ease}' +
      '.sv-hl-cat:hover{transform:translateY(-1px);border-color:#2d2a26}' +
      '.sv-hl-cat[aria-pressed="true"]{border-color:#2d2a26;background:#faf8f5;box-shadow:0 0 0 1px #2d2a26 inset}' +
      'body.dark-mode .sv-hl-cat{background:#2a2826;color:#f5f1ec;border-color:rgba(245,241,236,.18)}' +
      'body.dark-mode .sv-hl-cat:hover{border-color:#f5f1ec}' +
      'body.dark-mode .sv-hl-cat[aria-pressed="true"]{background:#1f1c19;border-color:#f5f1ec;box-shadow:0 0 0 1px #f5f1ec inset}' +
      '.sv-hl-cat-dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;border:1px solid rgba(0,0,0,.06)}' +
      '.sv-hl-cat--fact .sv-hl-cat-dot{background:#fef08a}' +
      '.sv-hl-cat--why .sv-hl-cat-dot{background:#86efac}' +
      '.sv-hl-cat--so-what .sv-hl-cat-dot{background:#f9a8d4}' +
      '.sv-hl-cat--question .sv-hl-cat-dot{background:#93c5fd}' +
      // KO-quick popover: hide the category picker entirely, show a tiny
      // "Marked as X" header instead, and force the note textarea visible.
      '.sv-hl-popover-quick-header{display:none;align-items:center;gap:7px;padding:2px 4px 6px;font-size:.8rem;color:#5d564b}' +
      '.sv-hl-popover-quick-header strong{font-weight:600;color:#2d2a26}' +
      '.sv-hl-popover-quick-dot{width:9px;height:9px;border-radius:50%;background:#ccc;flex-shrink:0}' +
      '.sv-hl-popover-quick-dot[data-cat="fact"]{background:#eab308}' +
      '.sv-hl-popover-quick-dot[data-cat="why"]{background:#22c55e}' +
      '.sv-hl-popover-quick-dot[data-cat="so-what"]{background:#ec4899}' +
      '.sv-hl-popover-quick-dot[data-cat="question"]{background:#3b82f6}' +
      'body.dark-mode .sv-hl-popover-quick-header{color:#c8c2ba}' +
      'body.dark-mode .sv-hl-popover-quick-header strong{color:#f5f1ec}' +
      '.sv-hl-popover--ko-quick .sv-hl-popover-prompt,.sv-hl-popover--ko-quick .sv-hl-popover-cats{display:none}' +
      '.sv-hl-popover--ko-quick .sv-hl-popover-quick-header{display:flex}' +
      '.sv-hl-divider{width:1px;height:22px;background:rgba(45,42,38,.12);margin:0 2px}' +
      '.sv-hl-icon-btn{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;background:transparent;border:none;border-radius:8px;color:#a14242;cursor:pointer}' +
      '.sv-hl-icon-btn:hover{background:rgba(161,66,66,.1)}' +
      '.sv-hl-note-row{margin-top:10px;display:flex;flex-direction:column;gap:6px}' +
      '.sv-hl-note{width:100%;border:1px solid rgba(45,42,38,.15);border-radius:10px;padding:8px 10px;font-family:inherit;font-size:.92rem;color:inherit;resize:vertical;min-height:64px}' +
      '.sv-hl-note:focus{outline:none;border-color:#2d2a26}' +
      '.sv-hl-note-actions{display:flex;align-items:center;justify-content:flex-end;gap:6px}' +
      '.sv-hl-note-actions .sv-hl-icon-btn{margin-right:auto}' +
      '.sv-hl-btn{padding:6px 12px;border-radius:10px;border:1px solid rgba(45,42,38,.15);background:#fff;font-family:inherit;font-size:.86rem;color:#2d2a26;cursor:pointer}' +
      '.sv-hl-btn:hover{background:#faf8f5}' +
      '.sv-hl-btn--primary{background:#2d2a26;color:#faf8f5;border-color:#2d2a26}' +
      '.sv-hl-btn--primary:hover{background:#1f1c19}' +
      // Selection pill (the discoverable affordance)
      '.sv-hl-pill{position:absolute;z-index:9100;display:none;align-items:center;gap:6px;padding:6px 12px;border-radius:999px;background:#2d2a26;color:#faf8f5;border:none;cursor:pointer;font-family:Inter,system-ui,sans-serif;font-size:.82rem;font-weight:500;box-shadow:0 8px 20px rgba(20,18,15,.28);opacity:0;transform:translateY(4px);transition:opacity .14s ease,transform .14s ease}' +
      '.sv-hl-pill--visible{opacity:1;transform:translateY(0)}' +
      '.sv-hl-pill:hover{background:#1f1c19}' +
      '.sv-hl-pill svg{flex-shrink:0}' +
      // FAB stack — bottom-left so it doesn't collide with the bug-reporter FAB
      '.sv-hl-fab-stack{position:fixed;left:18px;bottom:18px;z-index:8000;display:flex;flex-direction:column;gap:8px;align-items:flex-start}' +
      '.sv-hl-fab{display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border-radius:999px;background:#2d2a26;color:#faf8f5;border:none;cursor:pointer;text-decoration:none;box-shadow:0 10px 24px rgba(20,18,15,.25);font-family:Inter,system-ui,sans-serif;font-size:.9rem;font-weight:500}' +
      '.sv-hl-fab:hover{background:#1f1c19}' +
      '.sv-hl-fab--all{padding:7px 12px;font-size:.82rem;background:#4a463f}' +
      '.sv-hl-fab--all:hover{background:#3a3631}' +
      '.sv-hl-fab-count{display:inline-flex;align-items:center;justify-content:center;min-width:22px;height:22px;padding:0 6px;border-radius:11px;background:#faf8f5;color:#2d2a26;font-size:.78rem;font-weight:600}' +
      '.sv-hl-fab--empty .sv-hl-fab-count{background:rgba(250,248,245,.22);color:#faf8f5}' +
      'body.dark-mode .sv-hl-fab{background:#3a3631;color:#f5f1ec}' +
      'body.dark-mode .sv-hl-fab:hover{background:#4a463f}' +
      'body.dark-mode .sv-hl-fab--all{background:#2a2826}' +
      'body.dark-mode .sv-hl-fab-count{background:#f5f1ec;color:#2d2a26}' +
      '@media (max-width:640px){.sv-hl-fab-label{display:none}.sv-hl-fab{padding:10px}.sv-hl-fab--all{padding:8px}}' +
      // Modal
      '.sv-hl-modal{position:fixed;inset:0;z-index:9500;display:none;align-items:flex-end;justify-content:center}' +
      '.sv-hl-modal--open{display:flex}' +
      '.sv-hl-modal-backdrop{position:absolute;inset:0;background:rgba(20,18,15,.32);backdrop-filter:blur(2px)}' +
      '.sv-hl-modal-panel{position:relative;background:#faf8f5;width:min(640px,100%);max-height:80vh;border-radius:16px 16px 0 0;display:flex;flex-direction:column;box-shadow:0 -20px 48px rgba(20,18,15,.18);font-family:Inter,system-ui,sans-serif;color:#2d2a26}' +
      '@media (min-width:720px){.sv-hl-modal{align-items:center}.sv-hl-modal-panel{border-radius:16px}}' +
      '.sv-hl-modal-header{display:flex;align-items:center;gap:14px;padding:18px 22px;border-bottom:1px solid rgba(45,42,38,.08)}' +
      '.sv-hl-modal-header h2{margin:0;font-size:1.1rem;font-weight:600;flex:1}' +
      '.sv-hl-modal-allpages{font-size:.85rem;color:#5d564b;text-decoration:none}' +
      '.sv-hl-modal-allpages:hover{color:#2d2a26;text-decoration:underline}' +
      '.sv-hl-modal-close{background:transparent;border:none;font-size:1.5rem;line-height:1;color:#5d564b;cursor:pointer;padding:4px 8px;border-radius:8px}' +
      '.sv-hl-modal-close:hover{background:rgba(45,42,38,.06);color:#2d2a26}' +
      '.sv-hl-modal-body{padding:14px 22px 22px;overflow-y:auto;display:flex;flex-direction:column;gap:14px}' +
      '.sv-hl-modal-empty{text-align:center;padding:32px 8px;color:#5d564b}' +
      '.sv-hl-modal-empty p{margin:0 0 6px}' +
      '.sv-hl-modal-hint{font-size:.88rem;color:#7a7367}' +
      '.sv-hl-modal-item{display:flex;flex-direction:column;gap:8px;padding:14px;background:#fff;border-radius:12px;border:1px solid rgba(45,42,38,.06)}' +
      '.sv-hl-modal-snippet{position:relative;padding:10px 12px 10px 16px;border-radius:10px;font-size:.95rem;line-height:1.5;color:#2d2a26}' +
      '.sv-hl-modal-cat-row{display:flex;gap:6px;margin-bottom:2px}' +
      '.sv-hl-modal-cat{display:inline-flex;align-items:center;gap:5px;font-size:.7rem;font-weight:700;padding:2px 9px;border-radius:999px;letter-spacing:.05em;text-transform:uppercase}' +
      '.sv-hl-modal-cat::before{content:"";width:7px;height:7px;border-radius:50%}' +
      '.sv-hl-modal-cat--fact{background:#fef9c3;color:#854d0e}' +
      '.sv-hl-modal-cat--fact::before{background:#eab308}' +
      '.sv-hl-modal-cat--why{background:#dcfce7;color:#166534}' +
      '.sv-hl-modal-cat--why::before{background:#22c55e}' +
      '.sv-hl-modal-cat--so-what{background:#fce7f3;color:#9d174d}' +
      '.sv-hl-modal-cat--so-what::before{background:#ec4899}' +
      '.sv-hl-modal-cat--question{background:#dbeafe;color:#1e40af}' +
      '.sv-hl-modal-cat--question::before{background:#3b82f6}' +
      // KO Mode — cursor varies by focused category so students get visual
      // feedback about what they're currently highlighting AS. Applied to
      // all descendants of #study-notes (the user-agent text-cursor on
      // selectable text overrides cursor inheritance, so we have to be
      // explicit). Each category has its own SVG cursor with matching fill
      // and stroke colours.
      'body.sv-hl-ko-focus-fact #study-notes,body.sv-hl-ko-focus-fact #study-notes *{cursor:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="28" viewBox="0 0 24 28"><path d="M5 22h14v3H5z" fill="%232d2a26"/><path d="M5 22l1-7 6-12h0a3 3 0 0 1 5 0l1 7-6 12H5z" fill="%23fef08a" stroke="%23854d0e" stroke-width="1.2"/><path d="M11 4l5 3" stroke="%23854d0e" stroke-width="1.2" fill="none"/></svg>\') 2 26, text}' +
      'body.sv-hl-ko-focus-why #study-notes,body.sv-hl-ko-focus-why #study-notes *{cursor:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="28" viewBox="0 0 24 28"><path d="M5 22h14v3H5z" fill="%232d2a26"/><path d="M5 22l1-7 6-12h0a3 3 0 0 1 5 0l1 7-6 12H5z" fill="%2386efac" stroke="%23166534" stroke-width="1.2"/><path d="M11 4l5 3" stroke="%23166534" stroke-width="1.2" fill="none"/></svg>\') 2 26, text}' +
      'body.sv-hl-ko-focus-so-what #study-notes,body.sv-hl-ko-focus-so-what #study-notes *{cursor:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="28" viewBox="0 0 24 28"><path d="M5 22h14v3H5z" fill="%232d2a26"/><path d="M5 22l1-7 6-12h0a3 3 0 0 1 5 0l1 7-6 12H5z" fill="%23f9a8d4" stroke="%239d174d" stroke-width="1.2"/><path d="M11 4l5 3" stroke="%239d174d" stroke-width="1.2" fill="none"/></svg>\') 2 26, text}' +
      'body.sv-hl-ko-focus-question #study-notes,body.sv-hl-ko-focus-question #study-notes *{cursor:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="28" viewBox="0 0 24 28"><path d="M5 22h14v3H5z" fill="%232d2a26"/><path d="M5 22l1-7 6-12h0a3 3 0 0 1 5 0l1 7-6 12H5z" fill="%2393c5fd" stroke="%231e40af" stroke-width="1.2"/><path d="M11 4l5 3" stroke="%231e40af" stroke-width="1.2" fill="none"/></svg>\') 2 26, text}' +
      'body.sv-hl-ko-mode #study-notes mark.sv-hl{cursor:pointer}' +
      // Live selection (during drag, before release) recolours to the focused
      // category so the highlight looks correct from the very first pixel —
      // not just after the popover opens.
      'body.sv-hl-ko-focus-fact #study-notes ::selection{background:#fef9c3;color:#2d2a26}' +
      'body.sv-hl-ko-focus-fact #study-notes ::-moz-selection{background:#fef9c3;color:#2d2a26}' +
      'body.sv-hl-ko-focus-why #study-notes ::selection{background:#dcfce7;color:#2d2a26}' +
      'body.sv-hl-ko-focus-why #study-notes ::-moz-selection{background:#dcfce7;color:#2d2a26}' +
      'body.sv-hl-ko-focus-so-what #study-notes ::selection{background:#fce7f3;color:#2d2a26}' +
      'body.sv-hl-ko-focus-so-what #study-notes ::-moz-selection{background:#fce7f3;color:#2d2a26}' +
      'body.sv-hl-ko-focus-question #study-notes ::selection{background:#dbeafe;color:#2d2a26}' +
      'body.sv-hl-ko-focus-question #study-notes ::-moz-selection{background:#dbeafe;color:#2d2a26}' +
      // Hide the bottom-left FAB stack while in KO mode — the card duplicates those actions
      'body.sv-hl-ko-mode .sv-hl-fab-stack{display:none}' +
      // Floating KO card — top-right, fixed, follows scroll
      '.sv-ko-card{position:fixed;top:84px;right:18px;z-index:7600;width:280px;background:#fff;border:1px solid rgba(45,42,38,.1);border-radius:14px;box-shadow:0 12px 30px rgba(20,18,15,.16);padding:14px 14px 12px;font-family:Inter,system-ui,sans-serif;color:#2d2a26;display:none}' +
      'body.dark-mode .sv-ko-card{background:#2a2826;color:#f5f1ec;border-color:rgba(245,241,236,.1)}' +
      '@media (max-width:768px){.sv-ko-card{top:auto;bottom:80px;right:12px;left:12px;width:auto}}' +
      '.sv-ko-card-header{display:flex;align-items:center;gap:8px;margin-bottom:10px;cursor:grab;user-select:none;-webkit-user-select:none}' +
      '.sv-ko-card-header button{cursor:pointer}' +
      '.sv-ko-card--dragging,.sv-ko-card--dragging .sv-ko-card-header{cursor:grabbing}' +
      '.sv-ko-card--dragging{box-shadow:0 24px 56px rgba(20,18,15,.32);transition:none}' +
      '@media (max-width:768px){.sv-ko-card-header{cursor:default}}' +
      '.sv-ko-card-title{display:inline-flex;align-items:center;gap:6px;font-size:.78rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#5d564b;flex:1}' +
      'body.dark-mode .sv-ko-card-title{color:#a59f95}' +
      '.sv-ko-card-exit{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border:none;background:transparent;color:#7a7367;cursor:pointer;border-radius:6px}' +
      '.sv-ko-card-exit:hover{background:rgba(45,42,38,.08);color:#2d2a26}' +
      'body.dark-mode .sv-ko-card-exit:hover{background:rgba(245,241,236,.1);color:#f5f1ec}' +
      '.sv-ko-card-focus-label{font-size:.7rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#7a7367;margin-bottom:5px}' +
      '.sv-ko-card-focus{display:flex;align-items:flex-start;gap:10px;padding:10px 12px;border-radius:10px;background:#fef9c3;color:#2d2a26;transition:background .2s ease}' +
      '.sv-ko-card-focus--fact{background:#fef9c3}' +
      '.sv-ko-card-focus--why{background:#dcfce7}' +
      '.sv-ko-card-focus--so-what{background:#fce7f3}' +
      '.sv-ko-card-focus--question{background:#dbeafe}' +
      'body.dark-mode .sv-ko-card-focus--fact{background:rgba(234,179,8,.35);color:#fef9c3}' +
      'body.dark-mode .sv-ko-card-focus--why{background:rgba(34,197,94,.3);color:#dcfce7}' +
      'body.dark-mode .sv-ko-card-focus--so-what{background:rgba(236,72,153,.3);color:#fce7f3}' +
      'body.dark-mode .sv-ko-card-focus--question{background:rgba(59,130,246,.35);color:#dbeafe}' +
      '.sv-ko-card-focus-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0;margin-top:5px;background:rgba(0,0,0,.35)}' +
      '.sv-ko-card-focus--fact .sv-ko-card-focus-dot{background:#854d0e}' +
      '.sv-ko-card-focus--why .sv-ko-card-focus-dot{background:#166534}' +
      '.sv-ko-card-focus--so-what .sv-ko-card-focus-dot{background:#9d174d}' +
      '.sv-ko-card-focus--question .sv-ko-card-focus-dot{background:#1e40af}' +
      '.sv-ko-card-focus-text{flex:1;min-width:0}' +
      '.sv-ko-card-focus-name{font-size:.95rem;font-weight:700;line-height:1.2;margin-bottom:3px}' +
      '.sv-ko-card-focus-hint{font-size:.78rem;line-height:1.4;opacity:.85}' +
      '.sv-ko-card-switch-label{font-size:.7rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#7a7367;margin:10px 0 5px}' +
      '.sv-ko-card-dots{display:grid;grid-template-columns:1fr 1fr;gap:4px}' +
      '.sv-ko-dot{display:inline-flex;align-items:center;gap:6px;padding:5px 8px;border-radius:8px;background:transparent;border:1px solid rgba(45,42,38,.1);font-family:inherit;font-size:.78rem;color:#5d564b;cursor:pointer;text-align:left;transition:background .12s ease,border-color .12s ease}' +
      '.sv-ko-dot:hover{background:#faf8f5;border-color:rgba(45,42,38,.2)}' +
      '.sv-ko-dot--focus{background:#faf8f5;border-color:#2d2a26;color:#2d2a26;font-weight:600}' +
      'body.dark-mode .sv-ko-dot{border-color:rgba(245,241,236,.15);color:#c8c2ba}' +
      'body.dark-mode .sv-ko-dot:hover{background:#3a3631}' +
      'body.dark-mode .sv-ko-dot--focus{background:#1f1c19;border-color:#f5f1ec;color:#f5f1ec}' +
      '.sv-ko-dot-swatch{width:9px;height:9px;border-radius:50%;flex-shrink:0}' +
      '.sv-ko-dot--fact .sv-ko-dot-swatch{background:#fef08a}' +
      '.sv-ko-dot--why .sv-ko-dot-swatch{background:#86efac}' +
      '.sv-ko-dot--so-what .sv-ko-dot-swatch{background:#f9a8d4}' +
      '.sv-ko-dot--question .sv-ko-dot-swatch{background:#93c5fd}' +
      '.sv-ko-dot-name{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}' +
      '.sv-ko-dot-count{font-size:.7rem;font-weight:700;color:inherit;padding:1px 5px;border-radius:8px;background:rgba(45,42,38,.08)}' +
      '.sv-ko-dot--done .sv-ko-dot-count{background:rgba(34,197,94,.25);color:#166534}' +
      'body.dark-mode .sv-ko-dot--done .sv-ko-dot-count{background:rgba(34,197,94,.35);color:#bbf7d0}' +
      '.sv-ko-card-actions{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:10px;padding-top:10px;border-top:1px solid rgba(45,42,38,.08)}' +
      'body.dark-mode .sv-ko-card-actions{border-top-color:rgba(245,241,236,.1)}' +
      '.sv-ko-card-link{font-size:.8rem;color:#5d564b;text-decoration:none;background:transparent;border:none;font-family:inherit;cursor:pointer;padding:0}' +
      '.sv-ko-card-link:hover{color:#2d2a26;text-decoration:underline}' +
      'body.dark-mode .sv-ko-card-link{color:#c8c2ba}' +
      'body.dark-mode .sv-ko-card-link:hover{color:#f5f1ec}' +
      '.sv-ko-card-complete-banner{display:none;align-items:center;gap:6px;margin-top:10px;padding:7px 10px;background:#166534;color:#bbf7d0;border-radius:8px;font-size:.78rem;font-weight:600}' +
      '.sv-ko-card--complete .sv-ko-card-complete-banner{display:flex}' +
      // First-time tutorial modal
      '.sv-ko-tutorial{position:fixed;inset:0;z-index:9700;display:none;align-items:center;justify-content:center;padding:20px}' +
      '.sv-ko-tutorial--open{display:flex}' +
      '.sv-ko-tutorial-backdrop{position:absolute;inset:0;background:rgba(20,18,15,.55);backdrop-filter:blur(3px)}' +
      '.sv-ko-tutorial-panel{position:relative;background:#faf8f5;width:min(560px,100%);max-height:88vh;overflow-y:auto;border-radius:16px;padding:24px 26px;box-shadow:0 20px 50px rgba(20,18,15,.4);font-family:Inter,system-ui,sans-serif;color:#2d2a26}' +
      'body.dark-mode .sv-ko-tutorial-panel{background:#2a2826;color:#f5f1ec}' +
      '.sv-ko-tutorial-heading{font-family:"Source Serif 4",Georgia,serif;font-weight:700;font-size:1.5rem;margin:0 0 10px;color:inherit}' +
      '.sv-ko-tutorial-intro{margin:0 0 18px;font-size:.95rem;line-height:1.55;color:inherit}' +
      '.sv-ko-tutorial-cards{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:18px}' +
      '@media (max-width:520px){.sv-ko-tutorial-cards{grid-template-columns:1fr}}' +
      '.sv-ko-tutorial-card{padding:12px 14px;border-radius:12px}' +
      '.sv-ko-tutorial-card--fact{background:#fef9c3;color:#2d2a26}' +
      '.sv-ko-tutorial-card--why{background:#dcfce7;color:#2d2a26}' +
      '.sv-ko-tutorial-card--so-what{background:#fce7f3;color:#2d2a26}' +
      '.sv-ko-tutorial-card--question{background:#dbeafe;color:#2d2a26}' +
      'body.dark-mode .sv-ko-tutorial-card--fact{background:rgba(234,179,8,.4);color:#fef9c3}' +
      'body.dark-mode .sv-ko-tutorial-card--why{background:rgba(34,197,94,.35);color:#dcfce7}' +
      'body.dark-mode .sv-ko-tutorial-card--so-what{background:rgba(236,72,153,.35);color:#fce7f3}' +
      'body.dark-mode .sv-ko-tutorial-card--question{background:rgba(59,130,246,.4);color:#dbeafe}' +
      '.sv-ko-tutorial-card-header{display:flex;align-items:center;gap:7px;margin-bottom:5px}' +
      '.sv-ko-tutorial-card-dot{width:10px;height:10px;border-radius:50%;background:rgba(0,0,0,.4)}' +
      '.sv-ko-tutorial-card--fact .sv-ko-tutorial-card-dot{background:#854d0e}' +
      '.sv-ko-tutorial-card--why .sv-ko-tutorial-card-dot{background:#166534}' +
      '.sv-ko-tutorial-card--so-what .sv-ko-tutorial-card-dot{background:#9d174d}' +
      '.sv-ko-tutorial-card--question .sv-ko-tutorial-card-dot{background:#1e40af}' +
      '.sv-ko-tutorial-card-name{font-size:.92rem;font-weight:700}' +
      '.sv-ko-tutorial-card-hint{margin:0;font-size:.84rem;line-height:1.45}' +
      '.sv-ko-tutorial-tip{margin:0 0 18px;padding:10px 12px;background:rgba(45,42,38,.04);border-radius:10px;font-size:.86rem;line-height:1.5}' +
      'body.dark-mode .sv-ko-tutorial-tip{background:rgba(245,241,236,.06)}' +
      '.sv-ko-tutorial-tip strong{font-weight:700}' +
      '.sv-ko-tutorial-actions{display:flex;justify-content:flex-end}' +
      '.sv-ko-tutorial-go{padding:10px 20px;border-radius:10px;background:#2d2a26;color:#faf8f5;border:none;font-family:inherit;font-size:.92rem;font-weight:600;cursor:pointer}' +
      '.sv-ko-tutorial-go:hover{background:#1f1c19}' +
      'body.dark-mode .sv-ko-tutorial-go{background:#f5f1ec;color:#2d2a26}' +
      'body.dark-mode .sv-ko-tutorial-go:hover{background:#fff}' +
      '.sv-hl-modal-bar{position:absolute;left:0;top:6px;bottom:6px;width:4px;border-radius:2px}' +
      '.sv-hl-modal-note{margin:0;padding:8px 12px;background:#faf8f5;border-radius:10px;font-size:.92rem;color:#3d3a35;border-left:3px solid rgba(45,42,38,.25)}' +
      '.sv-hl-modal-actions{display:flex;gap:8px;justify-content:flex-end}' +
      '.sv-hl-modal-jump,.sv-hl-modal-delete{padding:6px 12px;border-radius:8px;border:1px solid rgba(45,42,38,.15);background:#fff;font-family:inherit;font-size:.82rem;color:#2d2a26;cursor:pointer}' +
      '.sv-hl-modal-jump:hover{background:#faf8f5}' +
      '.sv-hl-modal-delete{color:#a14242;border-color:rgba(161,66,66,.25)}' +
      '.sv-hl-modal-delete:hover{background:#fbecec}';
    document.head.appendChild(s);
  }

  // ---------- entry point ----------
  function init() {
    if (!isEnabled()) return;
    if (!document.getElementById('study-notes')) return; // not on a lesson page
    if (!window._lessonId) {
      // Loader hasn't finished yet — retry a few times
      var tries = 0;
      var retry = setInterval(function () {
        tries++;
        if (window._lessonId) {
          clearInterval(retry);
          bootstrap();
        } else if (tries > 20) {
          clearInterval(retry);
        }
      }, 200);
      return;
    }
    bootstrap();
  }

  var bootstrapped = false;
  function bootstrap() {
    if (bootstrapped) { refreshFab(); refreshKoCard(); return; }
    bootstrapped = true;
    injectStyles();
    buildFab();
    refreshFab();
    rehydrate();
    // Restore KO mode if it was active when the student last navigated
    if (isKoModeActive()) {
      document.body.classList.add('sv-hl-ko-mode');
      buildKoCard();
      koCardEl.style.display = 'block';
      refreshKoCard();
    }
    var container = document.getElementById('study-notes');
    container.addEventListener('mousedown', onMouseDownTracker, true);
    container.addEventListener('mousemove', onMouseMoveTracker);
    container.addEventListener('mouseup', onMouseUp);
    // Touch support: long-press handled via native selection, then trigger on selectionchange
    container.addEventListener('touchend', onMouseUp);
    container.addEventListener('click', onMarkClick, true);
    document.addEventListener('mousedown', onDocClick);
    document.addEventListener('keydown', onKeyDown);
    // If URL hash points at a specific highlight, scroll & flash it
    var hash = window.location.hash || '';
    if (hash.indexOf('#hl-') === 0) {
      var targetId = hash.slice(1);
      setTimeout(function () {
        var m = document.querySelector('mark.sv-hl[data-hl-id="' + cssEscape(targetId) + '"]');
        if (m) {
          m.scrollIntoView({ behavior: 'smooth', block: 'center' });
          m.classList.add('sv-hl--flash');
          setTimeout(function () { m.classList.remove('sv-hl--flash'); }, 1500);
        }
      }, 250);
    }
  }

  window.initHighlightAnnotate = init;

  // Also self-init on DOMContentLoaded for static pages (defensive — main.js calls us too)
  if (document.readyState !== 'loading') {
    setTimeout(init, 50);
  } else {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(init, 50); });
  }
})();
