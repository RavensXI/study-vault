/* ============================================
   StudyVault — Simplify / Explain / Tutor chunk menu
   On-demand help for any lesson paragraph (narration chunk).

   Two entry points:
     1. Global "Simplify language" toggle (a11y toolbar) — levels the whole
        lesson into plainer wording.
     2. Per-chunk menu (click a paragraph) — Simplify wording, Explain it
        differently (analogy/reframe), or Ask the tutor about this part.

   Purely additive. For "simplify" the original paragraph is hidden (not
   destroyed) and a plainer sibling shown; for "explain" a supplementary card
   is added below and the original is left untouched. Canonical content and
   narration are never modified.

   Article lessons only — no-op where there are no [data-narration-id] prose
   segments (practice-first subjects).

   Endpoints:
     POST /api/simplify     { text, level: 'simple'|'explain', ... }
     POST /api/simplify-qa  { hash, level }   (fire-and-forget async QA)
   Couples with the narration player via window.SimplifyNarration (main.js)
   and the lesson tutor via window.LessonTutor (lesson-tutor.js).
   ============================================ */

(function () {
  'use strict';

  var PREF_KEY = 'studyvault-simplify';   // { on: bool } — global leveling toggle
  var MIN_LEN = 60;                        // skip headings / short fragments

  var clientCache = {};      // `${level}:${id}` -> generated text
  var segments = [];         // [{ el, id }]
  var pristineText = {};     // id -> text captured before controls injected
  var globalOn = false;
  var toggleBtn = null;
  var menuEl = null;         // single reusable popover
  var menuForId = null;

  // ---- Preference storage (localStorage for everyone; profile sync = v2) ----
  function getPref() {
    try { return JSON.parse(localStorage.getItem(PREF_KEY)) || {}; }
    catch (e) { return {}; }
  }
  function setPref(p) {
    try { localStorage.setItem(PREF_KEY, JSON.stringify(p)); } catch (e) {}
  }

  // ---- Helpers ----
  // Extract the prose to simplify. Strip glossary popups, our own controls, the
  // "Key Fact" label, and the revision-tip widgets (lightbulb + task popup) —
  // the revision task is a separate activity and must NOT be simplified, but
  // the Key Fact's actual content should be.
  function extractText(el) {
    var clone = el.cloneNode(true);
    clone.querySelectorAll('.term-popup, .sv-chunk-icon, .sv-simplified, .sv-explained, .revision-tip-btn, .revision-tip-popup, .key-fact-label').forEach(function (n) {
      n.parentNode && n.parentNode.removeChild(n);
    });
    return (clone.textContent || '').replace(/\s+/g, ' ').trim();
  }

  // Blocks that carry a data-narration-id but aren't prose to simplify.
  function isExcludedChunk(el) {
    return /^H[1-6]$/.test(el.tagName);
  }

  function isKeyFact(el) {
    return el.classList.contains('key-fact') || !!(el.closest && el.closest('.key-fact'));
  }
  function glossaryTerms() {
    var g = window._lessonGlossary || [];
    return g.map(function (t) { return t && t.term ? t.term : ''; }).filter(Boolean);
  }
  function cssEscape(s) { return String(s).replace(/["\\]/g, '\\$&'); }
  function elById(id) {
    var s = segmentFor(id);
    return s ? s.el : null;
  }
  function segmentFor(id) {
    for (var i = 0; i < segments.length; i++) if (segments[i].id === id) return segments[i];
    return null;
  }

  // ---- API ----
  function callGenerate(id, level) {
    return fetch('/api/simplify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: pristineText[id],
        level: level,
        lessonId: window._lessonId || null,
        paragraphIndex: id,
        subjectSlug: window._subjectSlug || null,
        glossaryTerms: glossaryTerms()
      })
    }).then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); });
  }
  function triggerQa(hash, level) {
    if (!hash) return;
    try {
      fetch('/api/simplify-qa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ hash: hash, level: level }),
        keepalive: true
      }).catch(function () {});
    } catch (e) {}
  }

  // ---- Shimmer + type-out (shared) ----
  function shimmer() {
    var s = document.createElement('div');
    s.className = 'sv-shimmer';
    s.innerHTML = '<span></span><span></span><span></span>';
    return s;
  }

  // Reveal text word by word, fast — feels like it's being written out.
  function typeOut(pEl, text) {
    var tokens = text.split(/(\s+)/); // [word, space, word, ...]
    var i = 0, acc = '';
    pEl.textContent = '';
    (function step() {
      if (i >= tokens.length) { pEl.textContent = text; return; }
      var tok = tokens[i++];
      acc += tok;
      pEl.textContent = acc;
      setTimeout(step, tok.trim() === '' ? 0 : 22);
    })();
  }

  function fill(parts, text) {
    if (parts.shimmer && parts.shimmer.parentNode) parts.shimmer.parentNode.removeChild(parts.shimmer);
    typeOut(parts.p, text);
  }

  var SPARKLE_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/></svg>';

  // ---- SIMPLE (leveling): hide original, show plainer sibling ----
  // Indicator is the left stripe + the global toggle state — no tagline.
  // Click the simplified block to re-open the bubbles ("Show original").
  function isSimplified(el) { return el.classList.contains('sv-orig-hidden'); }

  function createSimplifiedBlock(el, id) {
    var keyFact = isKeyFact(el);
    var block = document.createElement('div');
    block.className = 'sv-simplified' + (keyFact ? ' sv-simplified--keyfact' : '');
    block.setAttribute('data-for', id);
    if (keyFact) {
      var kfLabel = document.createElement('div');
      kfLabel.className = 'key-fact-label';
      kfLabel.textContent = 'Key Fact';
      block.appendChild(kfLabel);
    }
    var p = document.createElement('p');
    p.className = 'sv-simplified-text';
    block.appendChild(p);
    var sh = shimmer();
    block.appendChild(sh);
    block.addEventListener('click', function (e) {
      if (e.target.closest('a, button')) return;
      if (document.body.classList.contains('sv-hl-mode')) return;
      var sel = window.getSelection && window.getSelection();
      if (sel && !sel.isCollapsed) return;
      e.stopPropagation();
      openBubbles(el, id, e.clientX, e.clientY);
    });
    el.classList.add('sv-orig-hidden');
    el.parentNode.insertBefore(block, el.nextSibling);
    if (window.SimplifyNarration) window.SimplifyNarration.setParagraph(id, true);
    return { block: block, p: p, shimmer: sh };
  }

  function revertSimplified(el, id) {
    var block = document.querySelector('.sv-simplified[data-for="' + cssEscape(id) + '"]');
    if (block) block.parentNode.removeChild(block);
    el.classList.remove('sv-orig-hidden');
    if (window.SimplifyNarration) window.SimplifyNarration.setParagraph(id, false);
  }

  function simplifyParagraph(el, id) {
    if (isSimplified(el)) return Promise.resolve();
    var parts = createSimplifiedBlock(el, id); // shimmer shows immediately
    var ck = 'simple:' + id;
    if (clientCache[ck]) { fill(parts, clientCache[ck]); return Promise.resolve(); }
    return callGenerate(id, 'simple').then(function (data) {
      if (data.useOriginal || !data.simplified) { revertSimplified(el, id); return; }
      clientCache[ck] = data.simplified;
      fill(parts, data.simplified);
      if (data.needsQa) triggerQa(data.hash, 'simple');
    }).catch(function () { revertSimplified(el, id); });
  }

  // ---- EXPLAIN (analogy/reframe): supplementary card, original untouched ----
  function explainBlockFor(id) {
    return document.querySelector('.sv-explained[data-for="' + cssEscape(id) + '"]');
  }

  function createExplainCard(el, id) {
    var card = document.createElement('div');
    card.className = 'sv-explained';
    card.setAttribute('data-for', id);
    card.innerHTML =
      '<div class="sv-explained-head">' +
        SPARKLE_ICON +
        '<span>Explained another way</span>' +
        '<button type="button" class="sv-explained-hide" aria-label="Hide">Hide</button>' +
      '</div>' +
      '<p class="sv-explained-text"></p>' +
      '<div class="sv-aside-foot"><span class="sv-aside-label">A different explanation to help it click — the original above is what the exam expects.</span></div>';
    card.querySelector('.sv-explained-hide').addEventListener('click', function (e) {
      e.stopPropagation();
      removeExplain(id);
    });
    var p = card.querySelector('.sv-explained-text');
    var sh = shimmer();
    p.parentNode.insertBefore(sh, p.nextSibling);
    var anchor = document.querySelector('.sv-simplified[data-for="' + cssEscape(id) + '"]') || el;
    anchor.parentNode.insertBefore(card, anchor.nextSibling);
    return { card: card, p: p, shimmer: sh };
  }

  function removeExplain(id) {
    var card = explainBlockFor(id);
    if (card) card.parentNode.removeChild(card);
  }

  function explainParagraph(el, id) {
    if (explainBlockFor(id)) return; // already shown
    var parts = createExplainCard(el, id); // shimmer shows immediately
    var ck = 'explain:' + id;
    if (clientCache[ck]) { fill(parts, clientCache[ck]); return; }
    callGenerate(id, 'explain').then(function (data) {
      if (data.useOriginal || !data.simplified) { removeExplain(id); return; }
      clientCache[ck] = data.simplified;
      fill(parts, data.simplified);
      if (data.needsQa) triggerQa(data.hash, 'explain');
    }).catch(function () { removeExplain(id); });
  }

  // ---- Ask the tutor ----
  function askTutor(id) {
    if (window.LessonTutor && typeof window.LessonTutor.askAbout === 'function') {
      window.LessonTutor.askAbout(pristineText[id]);
    }
  }

  // ---- Chunk bubbles (icon cluster popped over the click point) ----
  function buildBubbles() {
    if (menuEl) return;
    menuEl = document.createElement('div');
    menuEl.className = 'sv-bubbles';
    document.body.appendChild(menuEl);
    document.addEventListener('click', function (e) {
      if (menuEl.classList.contains('open') && !e.target.closest('.sv-bubbles')) closeBubbles();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeBubbles();
    });
    window.addEventListener('scroll', closeBubbles, { passive: true });
  }

  function bubble(label, iconPath, handler) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'sv-bubble';
    b.setAttribute('aria-label', label);
    b.setAttribute('data-label', label);
    b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + iconPath + '</svg>';
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      closeBubbles();
      handler();
    });
    return b;
  }

  function openBubbles(el, id, clientX, clientY) {
    buildBubbles();
    menuForId = id;
    menuEl.innerHTML = '';

    // 1. Simplify wording (toggles to "Show original" once simplified)
    if (isSimplified(el)) {
      menuEl.appendChild(bubble('Show original', '<path d="M3 12a9 9 0 1 0 18 0 9 9 0 0 0-18 0z"/><path d="M9 12h6"/>', function () {
        revertSimplified(el, id);
        if (globalOn) setGlobalState(false, { skipRevertAll: true });
      }));
    } else {
      menuEl.appendChild(bubble('Simplify wording', '<path d="M4 7h16"/><path d="M4 12h10"/><path d="M4 17h7"/>', function () {
        simplifyParagraph(el, id);
      }));
    }

    // 2. Explain it differently (toggles to "Hide explanation" when shown)
    if (explainBlockFor(id)) {
      menuEl.appendChild(bubble('Hide explanation', '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>', function () {
        removeExplain(id);
      }));
    } else {
      menuEl.appendChild(bubble('Explain it differently', '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/>', function () {
        explainParagraph(el, id);
      }));
    }

    // 3. Ask the tutor
    menuEl.appendChild(bubble('Ask the tutor', '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>', function () {
      askTutor(id);
    }));

    // Pop the cluster centred on the click point, sitting just above the cursor.
    menuEl.classList.add('open');
    var mw = menuEl.offsetWidth || 150;
    var mh = menuEl.offsetHeight || 44;
    var left = Math.max(8, Math.min(clientX - mw / 2, window.innerWidth - mw - 8));
    var top = clientY - mh - 12;
    if (top < 8) top = clientY + 16; // not enough room above — drop below the cursor
    menuEl.style.left = (left + window.scrollX) + 'px';
    menuEl.style.top = (top + window.scrollY) + 'px';
  }

  function closeBubbles() {
    if (menuEl) menuEl.classList.remove('open');
    menuForId = null;
  }

  // ---- Per-chunk click wiring ----
  // Click anywhere on a paragraph (outside highlight mode / text selection) to
  // pop the bubbles over the click point. No persistent icon.
  function wireChunk(el, id) {
    el.classList.add('sv-chunk');
    el.addEventListener('click', function (e) {
      if (e.target.closest('.sv-simplified, .sv-explained, .sv-bubbles')) return;
      if (e.target.closest('dfn, .term, .glossary-popup, a, button, .revision-tip-btn, .revision-tip-popup')) return;
      if (document.body.classList.contains('sv-hl-mode')) return; // highlighting
      var sel = window.getSelection && window.getSelection();
      if (sel && !sel.isCollapsed) return; // user is selecting text
      e.stopPropagation(); // don't let the document close-handler swallow this click
      openBubbles(el, id, e.clientX, e.clientY);
    });
  }

  // ---- Global toggle (simplify whole lesson into plainer wording) ----
  function setGlobalState(on, opts) {
    opts = opts || {};
    globalOn = !!on;
    setPref({ on: globalOn });
    if (toggleBtn) toggleBtn.setAttribute('aria-pressed', globalOn ? 'true' : 'false');
    document.body.classList.toggle('sv-simplify-global', globalOn);
    if (window.SimplifyNarration) window.SimplifyNarration.setGlobal(globalOn);
    if (globalOn) {
      segments.forEach(function (s) { simplifyParagraph(s.el, s.id); });
    } else if (!opts.skipRevertAll) {
      segments.forEach(function (s) { if (isSimplified(s.el)) revertSimplified(s.el, s.id); });
    }
  }

  // ---- Init ----
  function init() {
    var notes = document.getElementById('study-notes');
    if (!notes) return;

    var els = notes.querySelectorAll('[data-narration-id]');
    segments = [];
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.classList.contains('sv-chunk')) continue; // already wired
      if (isExcludedChunk(el)) continue;                // headings, key-fact widgets, etc.
      var id = el.getAttribute('data-narration-id');
      if (!id) continue;
      var text = extractText(el);
      if (text.length < MIN_LEN) continue;
      pristineText[id] = text;
      segments.push({ el: el, id: id });
      wireChunk(el, id);
    }
    if (!segments.length) return; // not an article lesson with prose — no-op

    toggleBtn = document.querySelector('.a11y-simplify-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function () { setGlobalState(!globalOn); });
    }

    var pref = getPref();
    if (pref.on) setGlobalState(true);
  }

  window.initSimplify = init;
})();
