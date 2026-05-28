/* ============================================
   StudyVault — Simplify Language
   On-demand plain-English rewriting of lesson prose.

   Purely additive: it never alters canonical content. The original paragraph
   is hidden (not destroyed) and a simplified sibling block is shown beside it,
   so reverting is instant and glossary tooltips / narration mapping on the
   original are untouched.

   Article lessons only — practice-first subjects have no [data-narration-id]
   prose segments, so this module no-ops there.

   Talks to:
     POST /api/simplify     — generate + cache (returns simplified text)
     POST /api/simplify-qa  — fire-and-forget async QA of a fresh cache entry
   Couples with the narration player via window.SimplifyNarration (main.js).
   ============================================ */

(function () {
  'use strict';

  var PREF_KEY = 'studyvault-simplify';     // { on: bool }
  var LEVEL = 'simple';                      // v1: single level
  var MIN_LEN = 40;                          // skip trivially short segments

  // Per-session client cache: narration id -> simplified text (avoids
  // re-hitting the endpoint when a student toggles a paragraph off then on).
  var clientCache = {};
  // narration id -> the original paragraph element
  var segments = [];
  // narration id -> pristine text captured before any controls were injected
  var pristineText = {};
  var globalOn = false;
  var toggleBtn = null;

  // ---- Preference storage ----
  // localStorage for everyone (anonymous + logged-in). An accessibility
  // preference is inherently per-device; profile sync is a documented v2
  // follow-up (no profiles settings column to write to yet).
  function getPref() {
    try { return JSON.parse(localStorage.getItem(PREF_KEY)) || {}; }
    catch (e) { return {}; }
  }
  function setPref(p) {
    try { localStorage.setItem(PREF_KEY, JSON.stringify(p)); } catch (e) {}
  }

  // ---- Text extraction ----
  // Clone the paragraph, strip glossary popups and our own controls, and read
  // the plain text. Captured once at init, before we inject the Simplify pill.
  function extractText(el) {
    var clone = el.cloneNode(true);
    clone.querySelectorAll('.term-popup, .sv-simplify-pill, .sv-simplified').forEach(function (n) {
      n.parentNode && n.parentNode.removeChild(n);
    });
    return (clone.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function glossaryTerms() {
    var g = window._lessonGlossary || [];
    return g.map(function (t) { return t && t.term ? t.term : ''; }).filter(Boolean);
  }

  // ---- API ----
  function callSimplify(id, text) {
    return fetch('/api/simplify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        level: LEVEL,
        lessonId: window._lessonId || null,
        paragraphIndex: id,
        subjectSlug: window._subjectSlug || null,
        glossaryTerms: glossaryTerms()
      })
    }).then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); });
  }

  function triggerQa(hash) {
    if (!hash) return;
    try {
      fetch('/api/simplify-qa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ hash: hash, level: LEVEL }),
        keepalive: true
      }).catch(function () {});
    } catch (e) {}
  }

  // ---- Render / revert a single paragraph ----
  function isSimplified(el) {
    return el.classList.contains('sv-orig-hidden');
  }

  function showSimplified(el, id, simplifiedText) {
    if (isSimplified(el)) return;
    var block = document.createElement('div');
    block.className = 'sv-simplified';
    block.setAttribute('data-for', id);

    var p = document.createElement('p');
    p.className = 'sv-simplified-text';
    p.textContent = simplifiedText;

    var foot = document.createElement('div');
    foot.className = 'sv-simplified-foot';
    var label = document.createElement('span');
    label.className = 'sv-simplified-label';
    label.textContent = 'Simplified — check key terms against the original.';
    var revert = document.createElement('button');
    revert.type = 'button';
    revert.className = 'sv-show-original';
    revert.textContent = 'Show original';
    revert.addEventListener('click', function (e) {
      e.stopPropagation();
      revertParagraph(el, id);
      // Reverting one paragraph means the lesson is no longer fully simplified.
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

  function revertParagraph(el, id) {
    var block = el.nextSibling;
    if (block && block.classList && block.classList.contains('sv-simplified')) {
      block.parentNode.removeChild(block);
    } else {
      // Defensive: find by data-for if DOM shifted.
      var stray = document.querySelector('.sv-simplified[data-for="' + cssEscape(id) + '"]');
      if (stray) stray.parentNode.removeChild(stray);
    }
    el.classList.remove('sv-orig-hidden');
    if (window.SimplifyNarration) window.SimplifyNarration.setParagraph(id, false);
  }

  function cssEscape(s) {
    return String(s).replace(/["\\]/g, '\\$&');
  }

  // ---- Simplify a paragraph (cache-aware) ----
  function setBusy(el, busy) {
    el.classList.toggle('sv-simplifying', busy);
    var pill = el.querySelector('.sv-simplify-pill');
    if (pill) pill.disabled = busy;
  }

  function simplifyParagraph(el, id) {
    if (isSimplified(el)) return Promise.resolve();
    if (clientCache[id]) { showSimplified(el, id, clientCache[id]); return Promise.resolve(); }

    setBusy(el, true);
    return callSimplify(id, pristineText[id]).then(function (data) {
      if (data.useOriginal || !data.simplified) {
        // Known-bad or empty — leave the original showing.
        return;
      }
      clientCache[id] = data.simplified;
      showSimplified(el, id, data.simplified);
      if (data.needsQa) triggerQa(data.hash);
    }).catch(function () {
      // Network/rate-limit — silently keep the original.
    }).then(function () {
      setBusy(el, false);
    });
  }

  // ---- Global toggle ----
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
      segments.forEach(function (s) { if (isSimplified(s.el)) revertParagraph(s.el, s.id); });
    }
  }

  // ---- Per-paragraph pill ----
  function addPill(el, id) {
    var pill = document.createElement('button');
    pill.type = 'button';
    pill.className = 'sv-simplify-pill';
    pill.setAttribute('aria-label', 'Simplify this paragraph');
    pill.textContent = 'Simplify';
    pill.addEventListener('click', function (e) {
      e.stopPropagation(); // don't trigger narration click-to-jump
      simplifyParagraph(el, id);
    });
    el.appendChild(pill);
    el.classList.add('sv-has-pill');
  }

  // ---- Init ----
  function init() {
    var notes = document.getElementById('study-notes');
    if (!notes) return;

    var els = notes.querySelectorAll('[data-narration-id]');
    segments = [];
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.classList.contains('sv-has-pill')) continue; // already initialised
      var id = el.getAttribute('data-narration-id');
      if (!id) continue;
      var text = extractText(el);
      if (text.length < MIN_LEN) continue; // skip headings / tiny fragments
      pristineText[id] = text;
      segments.push({ el: el, id: id });
      addPill(el, id);
    }
    if (!segments.length) return; // not an article lesson with prose — no-op

    // Wire the toolbar toggle (added in lesson.html).
    toggleBtn = document.querySelector('.a11y-simplify-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function () {
        setGlobalState(!globalOn);
      });
    }

    // Restore saved preference.
    var pref = getPref();
    if (pref.on) {
      // Reflect state immediately; paragraphs fill in as the (mostly cached)
      // requests resolve.
      setGlobalState(true);
    }
  }

  window.initSimplify = init;
})();
