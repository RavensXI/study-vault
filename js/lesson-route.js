/* The lesson route (Tom, 3 Oct 2026; preview branch lesson-route).

   The side column stops being a menu of features and becomes the lesson's route:
     Read  ->  Quick quiz  ->  Flashcards  ->  Exam question
   one vertical line with a node per stage. The order is a SUGGESTION: every stage can be tapped at any
   time, a finished stage ticks wherever it sits, and the percentage counts weight, not position, so any
   mix that reaches 50% finishes the lesson (exam question + flashcards = 55%). The next unfinished
   stage opens out with one clear button. Podcast, video, the lightbulb task and an interactive sit
   below as "Also counts". Under that, the lesson's contents: the section you are in is highlighted
   and sections you have read get a tick; reading every section ticks Read.

   Nothing here keeps its own copy of progress: it reads the existing Lesson Progress items (main.js)
   and clicks the existing buttons (quiz, flashcards, exam question), which stay in the page, hidden.
   The only new state is which sections were read: 'sv-read-<path>', account-synced (js/account-sync.js). */
(function () {
  'use strict';
  if (!/^\/lesson\//.test(location.pathname)) return;
  var READ_KEY = 'sv-read-' + location.pathname;

  var ICON = {
    read: '<path d="M2 4.5h7a3 3 0 0 1 3 3V20a2.5 2.5 0 0 0-2.5-2.5H2z"/><path d="M22 4.5h-7a3 3 0 0 0-3 3V20a2.5 2.5 0 0 1 2.5-2.5H22z"/>',
    'knowledge-check': '<circle cx="12" cy="12" r="9.5"/><path d="M9.3 9.2a2.8 2.8 0 0 1 5.4 1c0 1.9-2.7 2.5-2.7 3.6"/><path d="M12 17.2h.01"/>',
    flashcards: '<rect x="3" y="7" width="13" height="11" rx="2"/><rect x="8" y="3.5" width="13" height="11" rx="2"/>',
    'practice-question': '<path d="M14 2.5H6.5a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V8z"/><path d="M14 2.5V8h5.5"/><path d="M8.5 13h7M8.5 17h4.5"/>',
    podcast: '<path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/>',
    video: '<polygon points="7,4.5 19.5,12 7,19.5"/>',
    'revision-task': '<path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>',
    interactive: '<path d="M8 13V5.5a1.5 1.5 0 0 1 3 0V12"/><path d="M11 11.5a1.5 1.5 0 0 1 3 0V13"/><path d="M14 12.5a1.5 1.5 0 0 1 3 0V14a7 7 0 0 1-7 7h-.5a6 6 0 0 1-4.6-2.2L3.5 16.6a1.5 1.5 0 0 1 2.3-1.9L8 17"/>',
    tick: '<polyline points="20 6 9 17 4 12"/>'
  };
  function svg(name, cls) {
    return '<svg class="' + (cls || '') + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON[name] + '</svg>';
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  // the route's four stages, then the extras; only those this lesson has are shown
  var MAIN = [
    { id: 'read', name: 'Read', verb: 'Read the lesson' },
    { id: 'knowledge-check', name: 'Quiz', verb: 'Take the quick quiz' },
    { id: 'flashcards', name: 'Flashcards', verb: 'Practise the flashcards' },
    { id: 'practice-question', name: 'Exam Q', verb: 'Answer an exam question' }
  ];
  var EXTRA = [
    { id: 'podcast', name: 'Podcast' }, { id: 'video', name: 'Video' },
    { id: 'revision-task', name: 'Lightbulb task' }, { id: 'interactive', name: 'Interactive' }
  ];

  function q(s) { return document.querySelector(s); }
  function click(sel) { var b = q(sel); if (b) b.click(); return !!b; }
  function scrollTo(el) { if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }

  var ACT = {
    read: function () { var h = firstUnreadHeading(); scrollTo(h || q('article.study-notes')); },
    'knowledge-check': function () { click('#knowledge-check-btn'); },
    flashcards: function () { click('#sidebar-flashcard-btn'); },
    'practice-question': function () { click('.sv-practice-btn') || scrollTo(q('#practice-section, .practice-section')); },
    podcast: function () {
      click('.audio-tab[data-mode="podcast"]');
      var w = q('.audio-player-wrapper'); scrollTo(w);
      setTimeout(function () { var p = q('.narration-play'); if (p && !p.classList.contains('playing')) p.click(); }, 500);
    },
    video: function () { click('.sidebar-video-play') || click('.sidebar-video'); },
    'revision-task': function () {
      var b = q('article.study-notes .revision-tip-btn'); if (!b) return;
      b.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(function () { b.click(); }, 450);
    },
    interactive: function () { var s = q('.sv-embed-strip'); if (s) { s.scrollIntoView({ behavior: 'smooth', block: 'center' }); } }
  };

  /* ---------- reading: which sections have been read ---------- */
  var headings = [], readSet = {};
  function loadRead() { try { (JSON.parse(localStorage.getItem(READ_KEY) || '[]') || []).forEach(function (i) { readSet[i] = true; }); } catch (e) {} }
  function saveRead() { try { localStorage.setItem(READ_KEY, JSON.stringify(Object.keys(readSet).map(Number))); } catch (e) {} }
  function readCount() { var n = 0; for (var i = 0; i < headings.length; i++) if (readSet[i]) n++; return n; }
  function firstUnreadHeading() { for (var i = 0; i < headings.length; i++) if (!readSet[i]) return headings[i]; return null; }

  function waitFor(cb) {
    var tries = 0;
    (function poll() {
      var sec = q('.sidebar-progress-section');
      var ready = sec && sec.querySelector('.lesson-progress-item') && sec.dataset.svPct !== undefined &&
                  q('#knowledge-check-btn') && q('article.study-notes h2');
      if (ready) return cb(sec);
      if (++tries < 80) setTimeout(poll, 250);
    })();
  }

  waitFor(function (section) {
    var sidebar = q('.lesson-sidebar');
    var panel = q('.sv-panel');
    if (!sidebar || q('.svr')) return;
    headings = [].slice.call(document.querySelectorAll('article.study-notes h2'));
    loadRead();

    function has(id) { return id === 'read' || !!section.querySelector('.lesson-progress-item[data-task="' + id + '"]'); }
    function done(id) {
      if (id === 'read') return headings.length > 0 && readCount() === headings.length;
      var it = section.querySelector('.lesson-progress-item[data-task="' + id + '"]');
      return !!(it && it.classList.contains('completed'));
    }
    var W = window.svTaskWeights || {};
    var main = MAIN.filter(function (s) { return has(s.id); });
    var extra = EXTRA.filter(function (s) { return has(s.id); });

    var root = document.createElement('section');
    root.className = 'svr';
    root.setAttribute('aria-label', 'Lesson route');
    root.innerHTML =
      '<div class="svr-sec">' +
        '<header class="svr-head"><span class="svr-title">Lesson progress</span><span class="svr-pct" aria-live="polite"></span></header>' +
        '<div class="svr-bar"><i></i></div>' +
        '<ol class="svr-route" style="--n:' + main.length + '">' + main.map(function (s) {
          return '<li class="svr-stage" data-id="' + s.id + '"><button type="button" class="svr-step" aria-label="' + esc(s.verb) + '">' +
            '<span class="svr-node">' + svg(s.id, 'svr-ic') + svg('tick', 'svr-tick') + '</span>' +
            '<span class="svr-name">' + esc(s.name) + '</span><span class="svr-meta"></span></button></li>';
        }).join('') + '</ol>' +
        '<button type="button" class="svr-next"></button>' +
      '</div>' +
      (extra.length ? '<div class="svr-sec"><span class="svr-label">Also counts</span><div class="svr-extras" style="--m:' + extra.length + '">' + extra.map(function (s) {
        return '<button type="button" class="svr-chip" data-id="' + s.id + '">' + svg(s.id, 'svr-ic') + svg('tick', 'svr-tick') +
          '<span>' + esc(s.name) + '</span><b>' + (W[s.id] || 0) + '%</b></button>';
      }).join('') + '</div></div>' : '') +
      (headings.length ? '<nav class="svr-sec svr-contents" aria-label="In this lesson"><span class="svr-label">In this lesson</span><ol>' + headings.map(function (h, i) {
        return '<li><a href="#" data-i="' + i + '">' + esc(h.textContent.replace(/\s+/g, ' ').trim()) + '</a></li>';
      }).join('') + '</ol></nav>' : '') +
      '<footer class="svr-foot"></footer>';

    // Related media and the tutor keep their own buttons (and behaviour), moved into the route's foot
    var foot = root.querySelector('.svr-foot');
    var rm = q('.rm-launcher'), tutor = q('.tile-tutor .sv-tool-btn');
    if (rm) foot.appendChild(rm);
    if (tutor) foot.appendChild(tutor);
    if (!foot.children.length) foot.remove();

    sidebar.insertBefore(root, panel || sidebar.firstChild);
    if (panel) panel.classList.add('svr-hidden');
    document.body.classList.add('has-svr');

    /* ---- render state ---- */
    var pctEl = root.querySelector('.svr-pct'), bar = root.querySelector('.svr-bar i');
    function render() {
      var p = +section.dataset.svPct || 0;
      pctEl.innerHTML = '<b>' + p + '%</b> · ' + (p >= 50 ? 'lesson done' : 'done at 50%');
      bar.style.width = p + '%';
      root.classList.toggle('is-complete', p >= 50);
      var next = null;
      main.forEach(function (s) {
        var li = root.querySelector('.svr-stage[data-id="' + s.id + '"]');
        var d = done(s.id);
        li.classList.toggle('is-done', d);
        if (!d && !next) next = s;
        li.classList.toggle('is-next', !d && next === s);
        li.querySelector('.svr-meta').textContent = s.id === 'read'
          ? readCount() + ' of ' + headings.length
          : (d ? 'Done' : (W[s.id] || 0) + '%');
      });
      var nb = root.querySelector('.svr-next');
      if (next) {
        nb.hidden = false; nb.dataset.id = next.id;
        nb.innerHTML = '<span>' + esc(next.verb) + '</span>' + (next.id !== 'read' ? '<small>\u00b7 ' + (W[next.id] || 0) + '%</small>' : '') + '<span class="svr-arrow">\u2192</span>';
      } else nb.hidden = true;
      extra.forEach(function (s) {
        var c = root.querySelector('.svr-chip[data-id="' + s.id + '"]');
        if (c) c.classList.toggle('is-done', done(s.id));
      });
      root.querySelectorAll('.svr-contents a').forEach(function (a) { a.classList.toggle('is-read', !!readSet[+a.dataset.i]); });
    }
    new MutationObserver(render).observe(section, { subtree: true, attributes: true, attributeFilter: ['class', 'data-sv-pct'] });
    render();

    /* ---- actions: every stage, any time, in any order ---- */
    root.addEventListener('click', function (e) {
      var row = e.target.closest('.svr-step, .svr-chip, .svr-next');
      if (row) { var id = (row.closest('[data-id]') || row).dataset.id; if (ACT[id]) ACT[id](); return; }
      var a = e.target.closest('.svr-contents a');
      if (a) { e.preventDefault(); scrollTo(headings[+a.dataset.i]); }
    });

    /* ---- contents: where you are, and what you have read ---- */
    var links = root.querySelectorAll('.svr-contents a');
    function onScroll() {
      var cur = 0, vh = window.innerHeight;
      headings.forEach(function (h, i) { if (h.getBoundingClientRect().top < vh * 0.35) cur = i; });
      links.forEach(function (a, i) { a.classList.toggle('is-here', i === cur); });
      // a section counts as read once the next heading (or the end of the lesson) has come up the screen
      var changed = false;
      headings.forEach(function (h, i) {
        if (readSet[i]) return;
        var endEl = headings[i + 1] || q('article.study-notes').lastElementChild;
        if (endEl && endEl.getBoundingClientRect().top < vh * 0.6) { readSet[i] = true; changed = true; }
      });
      if (changed) { saveRead(); render(); }
    }
    // the live behaviour: the column scrolls with the page until its foot is in view, then stays there;
    // its sticking point comes from its own height, so it is never cut off and never scrolls inside
    function stickPoint() {
      var h = sidebar.getBoundingClientRect().height, top = 80;
      var t = Math.min(top, window.innerHeight - h - 16);
      document.body.style.setProperty('--svr-top', t + 'px');
    }
    stickPoint();
    window.addEventListener('resize', stickPoint);
    if (window.ResizeObserver) new ResizeObserver(stickPoint).observe(sidebar);
    var ticking = false;
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; onScroll(); }); } }, { passive: true });
    onScroll();
  });
})();
