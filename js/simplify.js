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
  var MIN_LEN = 40;                        // skip trivially short segments

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
  function extractText(el) {
    var clone = el.cloneNode(true);
    clone.querySelectorAll('.term-popup, .sv-chunk-icon, .sv-simplified, .sv-explained').forEach(function (n) {
      n.parentNode && n.parentNode.removeChild(n);
    });
    return (clone.textContent || '').replace(/\s+/g, ' ').trim();
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

  // ---- SIMPLE (leveling): hide original, show plainer sibling ----
  function isSimplified(el) { return el.classList.contains('sv-orig-hidden'); }

  function showSimplified(el, id, text) {
    if (isSimplified(el)) return;
    var block = document.createElement('div');
    block.className = 'sv-simplified';
    block.setAttribute('data-for', id);
    var p = document.createElement('p');
    p.className = 'sv-simplified-text';
    p.textContent = text;
    var foot = document.createElement('div');
    foot.className = 'sv-aside-foot';
    var label = document.createElement('span');
    label.className = 'sv-aside-label';
    label.textContent = 'Simplified — check key terms against the original.';
    var revert = document.createElement('button');
    revert.type = 'button';
    revert.className = 'sv-aside-action';
    revert.textContent = 'Show original';
    revert.addEventListener('click', function (e) {
      e.stopPropagation();
      revertSimplified(el, id);
      if (globalOn) setGlobalState(false, { skipRevertAll: true });
    });
    foot.appendChild(label);
    foot.appendChild(revert);
    block.appendChild(p);
    block.appendChild(foot);

    el.classList.add('sv-orig-hidden');
    el.parentNode.insertBefore(block, el.nextSibling);
    if (window.SimplifyNarration) window.SimplifyNarration.setParagraph(id, true);
  }

  function revertSimplified(el, id) {
    var block = document.querySelector('.sv-simplified[data-for="' + cssEscape(id) + '"]');
    if (block) block.parentNode.removeChild(block);
    el.classList.remove('sv-orig-hidden');
    if (window.SimplifyNarration) window.SimplifyNarration.setParagraph(id, false);
  }

  function simplifyParagraph(el, id) {
    if (isSimplified(el)) return Promise.resolve();
    var ck = 'simple:' + id;
    if (clientCache[ck]) { showSimplified(el, id, clientCache[ck]); return Promise.resolve(); }
    el.classList.add('sv-busy');
    return callGenerate(id, 'simple').then(function (data) {
      if (data.useOriginal || !data.simplified) return;
      clientCache[ck] = data.simplified;
      showSimplified(el, id, data.simplified);
      if (data.needsQa) triggerQa(data.hash, 'simple');
    }).catch(function () {}).then(function () { el.classList.remove('sv-busy'); });
  }

  // ---- EXPLAIN (analogy/reframe): supplementary card, original untouched ----
  function explainBlockFor(id) {
    return document.querySelector('.sv-explained[data-for="' + cssEscape(id) + '"]');
  }

  function showExplainCard(el, id, text, loading) {
    var existing = explainBlockFor(id);
    if (existing) {
      if (!loading) {
        existing.querySelector('.sv-explained-text').textContent = text;
        existing.classList.remove('sv-busy');
      }
      return;
    }
    var card = document.createElement('div');
    card.className = 'sv-explained' + (loading ? ' sv-busy' : '');
    card.setAttribute('data-for', id);
    card.innerHTML =
      '<div class="sv-explained-head">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1h6c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/></svg>' +
        '<span>Explained another way</span>' +
        '<button type="button" class="sv-explained-hide" aria-label="Hide">Hide</button>' +
      '</div>' +
      '<p class="sv-explained-text"></p>' +
      '<div class="sv-aside-foot"><span class="sv-aside-label">A different explanation to help it click — the original above is what the exam expects.</span></div>';
    card.querySelector('.sv-explained-text').textContent = loading ? 'Thinking of another way to explain this…' : text;
    card.querySelector('.sv-explained-hide').addEventListener('click', function (e) {
      e.stopPropagation();
      removeExplain(id);
    });
    // Insert after the simplified block if present, else right after the chunk.
    var anchor = document.querySelector('.sv-simplified[data-for="' + cssEscape(id) + '"]') || el;
    anchor.parentNode.insertBefore(card, anchor.nextSibling);
  }

  function removeExplain(id) {
    var card = explainBlockFor(id);
    if (card) card.parentNode.removeChild(card);
  }

  function explainParagraph(el, id) {
    if (explainBlockFor(id)) return; // already shown
    var ck = 'explain:' + id;
    if (clientCache[ck]) { showExplainCard(el, id, clientCache[ck], false); return; }
    showExplainCard(el, id, '', true); // loading card
    callGenerate(id, 'explain').then(function (data) {
      if (data.useOriginal || !data.simplified) { removeExplain(id); return; }
      clientCache[ck] = data.simplified;
      showExplainCard(el, id, data.simplified, false);
      if (data.needsQa) triggerQa(data.hash, 'explain');
    }).catch(function () { removeExplain(id); });
  }

  // ---- Ask the tutor ----
  function askTutor(id) {
    if (window.LessonTutor && typeof window.LessonTutor.askAbout === 'function') {
      window.LessonTutor.askAbout(pristineText[id]);
    }
  }

  // ---- Chunk menu (popover) ----
  function buildMenu() {
    if (menuEl) return;
    menuEl = document.createElement('div');
    menuEl.className = 'sv-menu';
    menuEl.setAttribute('role', 'menu');
    document.body.appendChild(menuEl);
    document.addEventListener('click', function (e) {
      if (menuEl.classList.contains('open') && !e.target.closest('.sv-menu') && !e.target.closest('.sv-chunk-icon')) {
        closeMenu();
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
    window.addEventListener('scroll', closeMenu, { passive: true });
  }

  function menuItem(label, iconPath, handler) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'sv-menu-item';
    b.setAttribute('role', 'menuitem');
    b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + iconPath + '</svg><span>' + label + '</span>';
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      closeMenu();
      handler();
    });
    return b;
  }

  function openMenu(el, id, anchorRect) {
    buildMenu();
    menuForId = id;
    menuEl.innerHTML = '';

    // 1. Simplify wording  (toggles to "Show original" when already simplified)
    if (isSimplified(el)) {
      menuEl.appendChild(menuItem('Show original', '<path d="M3 12a9 9 0 1 0 18 0 9 9 0 0 0-18 0z"/><path d="M9 12h6"/>', function () {
        revertSimplified(el, id);
        if (globalOn) setGlobalState(false, { skipRevertAll: true });
      }));
    } else {
      menuEl.appendChild(menuItem('Simplify wording', '<path d="M4 7h16"/><path d="M4 12h10"/><path d="M4 17h7"/>', function () {
        simplifyParagraph(el, id);
      }));
    }

    // 2. Explain it differently (toggles to "Hide explanation" when shown)
    if (explainBlockFor(id)) {
      menuEl.appendChild(menuItem('Hide explanation', '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>', function () {
        removeExplain(id);
      }));
    } else {
      menuEl.appendChild(menuItem('Explain it differently', '<path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1h6c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/><path d="M9 18h6"/><path d="M10 22h4"/>', function () {
        explainParagraph(el, id);
      }));
    }

    // 3. Ask the tutor
    menuEl.appendChild(menuItem('Ask the tutor', '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>', function () {
      askTutor(id);
    }));

    // Position: below-left of the anchor, clamped to the viewport.
    menuEl.classList.add('open');
    var mw = menuEl.offsetWidth || 220;
    var mh = menuEl.offsetHeight || 140;
    var top = anchorRect.bottom + 6;
    if (top + mh > window.innerHeight - 8) top = Math.max(8, anchorRect.top - mh - 6);
    var left = Math.min(anchorRect.left, window.innerWidth - mw - 8);
    left = Math.max(8, left);
    menuEl.style.top = (top + window.scrollY) + 'px';
    menuEl.style.left = (left + window.scrollX) + 'px';
  }

  function closeMenu() {
    if (menuEl) menuEl.classList.remove('open');
    menuForId = null;
  }

  // ---- Per-chunk affordance + click wiring ----
  function wireChunk(el, id) {
    el.classList.add('sv-chunk');

    var icon = document.createElement('button');
    icon.type = 'button';
    icon.className = 'sv-chunk-icon';
    icon.setAttribute('aria-label', 'Help with this paragraph');
    icon.setAttribute('tabindex', '0');
    icon.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/><circle cx="12" cy="12" r="10"/></svg>';
    icon.addEventListener('click', function (e) {
      e.stopPropagation();
      if (menuForId === id && menuEl && menuEl.classList.contains('open')) { closeMenu(); return; }
      openMenu(el, id, icon.getBoundingClientRect());
    });
    el.appendChild(icon);

    // Whole-chunk click also opens the menu, but only when it won't fight text
    // selection or the highlight tool.
    el.addEventListener('click', function (e) {
      if (e.target.closest('.sv-chunk-icon, .sv-simplified, .sv-explained')) return;
      if (e.target.closest('dfn, .term, .glossary-popup, a, button')) return;
      if (document.body.classList.contains('sv-hl-mode')) return; // highlighting
      var sel = window.getSelection && window.getSelection();
      if (sel && !sel.isCollapsed) return; // user is selecting text
      openMenu(el, id, icon.getBoundingClientRect());
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
