/* The lesson timeline (Tom, 3 Oct 2026; preview branch podcast-transcripts).

   The Lesson Progress row becomes the controls: the big Quick Quiz / Flashcards / Exam question tiles
   go, and each step on the timeline takes you there. Steps sit in equal columns joined by one line
   that fills as steps are done: Quiz, Cards, Exam Q (the core three, on a heavier line), then Task,
   Interactive, Podcast, Video where the lesson has them. Under each: its name and what it is worth.
   One full-width "Next" button names the heaviest step not yet done (the quickest road to 50%); any
   step can still be tapped at any time, in any order.

   Nothing here keeps its own progress: it reads the Lesson Progress items (main.js) and clicks the
   existing buttons, which stay in the page, hidden. The only new state is 'sv-timeline-hint' (the
   one-time "Tap any step" on phones), account-synced. */
(function () {
  'use strict';
  if (!/^\/lesson\//.test(location.pathname)) return;
  var HINT_KEY = 'sv-timeline-hint';   // + 'sv-lesson-done-seen' below

  var STEPS = [
    { id: 'knowledge-check', name: 'Quiz', verb: 'Take the quick quiz', core: true },
    { id: 'flashcards', name: 'Cards', verb: 'Practise the flashcards', core: true },
    { id: 'practice-question', name: 'Exam Q', verb: 'Answer an exam question', core: true },
    { id: 'revision-task', name: 'Task', verb: 'Try a lightbulb task' },
    { id: 'interactive', name: 'Interactive', verb: 'Master the interactive' },
    { id: 'podcast', name: 'Podcast', verb: 'Listen to the podcast' },
    { id: 'video', name: 'Video', verb: 'Watch the video' }
  ];
  var ICON = {
    'knowledge-check': '<circle cx="12" cy="12" r="9.5"/><path d="M9.3 9.2a2.8 2.8 0 0 1 5.4 1c0 1.9-2.7 2.5-2.7 3.6"/><path d="M12 17.2h.01"/>',
    flashcards: '<rect x="3" y="7" width="13" height="11" rx="2"/><rect x="8" y="3.5" width="13" height="11" rx="2"/>',
    'practice-question': '<path d="M14 2.5H6.5a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V8z"/><path d="M14 2.5V8h5.5"/><path d="M8.5 13h7M8.5 17h4.5"/>',
    'revision-task': '<path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>',
    interactive: '<path d="M8 13V5.5a1.5 1.5 0 0 1 3 0V12"/><path d="M11 11.5a1.5 1.5 0 0 1 3 0V13"/><path d="M14 12.5a1.5 1.5 0 0 1 3 0V14a7 7 0 0 1-7 7h-.5a6 6 0 0 1-4.6-2.2L3.5 16.6a1.5 1.5 0 0 1 2.3-1.9L8 17"/>',
    podcast: '<path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/>',
    video: '<polygon points="7,4.5 19.5,12 7,19.5"/>',
    tick: '<polyline points="20 6 9 17 4 12"/>'
  };
  function svg(name, cls) {
    return '<svg class="' + cls + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON[name] + '</svg>';
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function q(s) { return document.querySelector(s); }
  function click(sel) { var b = q(sel); if (b) b.click(); return !!b; }

  var ACT = {
    'knowledge-check': function () { click('#knowledge-check-btn'); },
    flashcards: function () { click('#sidebar-flashcard-btn'); },
    'practice-question': function () { click('.sv-practice-btn') || (q('#practice-section, .practice-section') || {}).scrollIntoView && q('#practice-section, .practice-section').scrollIntoView({ behavior: 'smooth' }); },
    'revision-task': function () {
      var bs = [].slice.call(document.querySelectorAll('article.study-notes .revision-tip-btn')); if (!bs.length) return;
      // the nearest lightbulb below the top of the screen, else the first
      var b = bs.filter(function (x) { return x.getBoundingClientRect().top > 80; })[0] || bs[0];
      b.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(function () { b.click(); }, 450);
    },
    interactive: function () { var s = q('.sv-embed-strip'); if (s) { s.scrollIntoView({ behavior: 'smooth', block: 'center' }); var b = s.querySelector('button'); if (b) setTimeout(function () { b.click(); }, 450); } },
    podcast: function () {
      click('.audio-tab[data-mode="podcast"]');
      var w = q('.audio-player-wrapper'); if (w) w.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setTimeout(function () { var p = q('.narration-play'); if (p && !p.classList.contains('playing')) p.click(); }, 500);
    },
    video: function () { click('.sidebar-video-play') || click('.sidebar-video'); }
  };

  function waitFor(cb) {
    var tries = 0;
    (function poll() {
      var sec = q('.sidebar-progress-section');
      if (sec && sec.querySelector('.lesson-progress-item') && sec.dataset.svPct !== undefined && q('.sv-panel')) return cb(sec);
      if (++tries < 80) setTimeout(poll, 250);
    })();
  }

  waitFor(function (section) {
    if (section.querySelector('.svtl')) return;
    var ul = q('.header-unit-label'); if (ul && ul.textContent) ul.title = ul.textContent.trim();   // the full unit name on hover when it is truncated
    var W = window.svTaskWeights || {};
    function item(id) { return section.querySelector('.lesson-progress-item[data-task="' + id + '"]'); }
    var steps = STEPS.filter(function (s) { return item(s.id); });
    if (!steps.length) return;

    var root = document.createElement('div');
    root.className = 'svtl';
    root.innerHTML =
      '<ol class="svtl-row" style="--n:' + steps.length + '">' + steps.map(function (s) {
        return '<li class="svtl-step' + (s.core ? ' is-core' : '') + '" data-id="' + s.id + '">' +
          '<button type="button" class="svtl-btn" data-tip="' + esc(s.verb) + '" aria-label="' + esc(s.verb) + ', worth ' + (W[s.id] || 0) + '%">' +
            '<span class="svtl-node">' + svg(s.id, 'svtl-ic') + svg('tick', 'svtl-tick') + '</span>' +
            '<span class="svtl-name">' + esc(s.name) + '</span><span class="svtl-worth">' + (W[s.id] || 0) + '%</span>' +
          '</button></li>';
      }).join('') + '</ol>' +
      '<button type="button" class="svtl-next"></button>' +
      '<button type="button" class="svtl-further" hidden></button>';
    var card = section.querySelector('.lesson-progress-card');
    (card && card.parentNode === section ? card : section.lastChild).after(root);
    document.body.classList.add('has-svtl');

    function done(id) { var it = item(id); return !!(it && it.classList.contains('completed')); }
    var nextBtn = root.querySelector('.svtl-next');
    function render() {
      var next = null;
      steps.forEach(function (s) {
        var li = root.querySelector('.svtl-step[data-id="' + s.id + '"]');
        var d = done(s.id);
        li.classList.toggle('is-done', d);
        li.querySelector('.svtl-worth').textContent = d ? 'Done' : (W[s.id] || 0) + '%';
        if (!d && (!next || (W[s.id] || 0) > (W[next.id] || 0))) next = s;   // heaviest not done = quickest road to 50%
      });
      root.querySelectorAll('.svtl-step').forEach(function (li) { li.classList.toggle('is-next', !!next && li.dataset.id === next.id); });
      var p = +section.dataset.svPct || 0, left = steps.filter(function (s) { return !done(s.id); }).length;
      var further = root.querySelector('.svtl-further');
      if (p >= 50) {
        // done: the button's job becomes moving on; going further is the quiet second choice
        var nl = q('#nav-next-lesson'), hasNext = nl && nl.getAttribute('href') && nl.getAttribute('href') !== '#' && nl.style.display !== 'none';
        nextBtn.hidden = false; nextBtn.dataset.id = 'next-lesson'; nextBtn.dataset.href = hasNext ? nl.getAttribute('href') : '/';
        nextBtn.innerHTML = '<span>' + (hasNext ? 'Next lesson' : 'Back to your dashboard') + '</span><span class="svtl-arrow">\u2192</span>';
        if (left && next) {
          further.hidden = false; further.dataset.id = next.id;
          further.textContent = 'Or go further: ' + left + ' step' + (left > 1 ? 's' : '') + ' left';
        } else further.hidden = true;
      } else if (next) {
        further.hidden = true;
        nextBtn.hidden = false; nextBtn.dataset.id = next.id; delete nextBtn.dataset.href;
        nextBtn.innerHTML = '<span>Next: ' + esc(next.verb.charAt(0).toLowerCase() + next.verb.slice(1)) + '</span><small>\u00b7 ' + (W[next.id] || 0) + '%</small><span class="svtl-arrow">\u2192</span>';
      } else nextBtn.hidden = true;
      celebrate(p);
    }

    /* the moment, once per lesson: when this visit takes the lesson past 50% (and again, smaller, at 100%)
       the header pulses and, on phones where the panel is in a closed drawer, a bar slides up.
       'sv-lesson-done-seen' ({path: 1 | 2}, account-synced) keeps it from repeating on later visits. */
    var SEEN_KEY = 'sv-lesson-done-seen', startPct = null;
    function seenAll() { try { return JSON.parse(localStorage.getItem(SEEN_KEY) || '{}') || {}; } catch (e) { return {}; } }
    function celebrate(p) {
      if (startPct === null) { startPct = p; return; }        // the state on arrival is not news
      var level = p >= 100 ? 2 : p >= 50 ? 1 : 0, all = seenAll(), had = all[location.pathname] || 0;
      if (level <= had || level === 0 || startPct >= (level === 2 ? 100 : 50)) return;
      all[location.pathname] = level; try { localStorage.setItem(SEEN_KEY, JSON.stringify(all)); } catch (e) {}
      section.classList.remove('svtl-pulse'); void section.offsetWidth; section.classList.add('svtl-pulse');
      if (window.svSound) svSound.play(level === 2 ? 'explored' : 'done');
      var drawerMode = window.matchMedia && window.matchMedia('(max-width: 900px)').matches;
      if (drawerMode) toast(level);
    }
    function toast(level) {
      var old = q('.svtl-toast'); if (old) old.remove();
      var nl = q('#nav-next-lesson'), href = nl && nl.getAttribute('href') && nl.getAttribute('href') !== '#' ? nl.getAttribute('href') : null;
      var t = document.createElement('div');
      t.className = 'svtl-toast'; t.setAttribute('role', 'status');
      t.innerHTML = '<span class="svtl-toast-tick">\u2713</span><span class="svtl-toast-text">' + (level === 2 ? 'Fully explored' : 'Lesson done') + '</span>' +
        (href ? '<a class="svtl-toast-go" href="' + esc(href) + '">Next lesson \u2192</a>' : '') +
        '<button type="button" class="svtl-toast-x" aria-label="Close">\u00d7</button>';
      document.body.appendChild(t);
      requestAnimationFrame(function () { t.classList.add('is-in'); });
      function close() { t.classList.remove('is-in'); setTimeout(function () { t.remove(); }, 400); }
      t.querySelector('.svtl-toast-x').addEventListener('click', close);
      setTimeout(close, 9000);
    }
    new MutationObserver(render).observe(section, { subtree: true, attributes: true, attributeFilter: ['class'] });
    render();

    root.addEventListener('click', function (e) {
      var b = e.target.closest('.svtl-btn, .svtl-next, .svtl-further'); if (!b) return;
      if (b.dataset.href) { location.href = b.dataset.href; return; }
      var id = (b.closest('[data-id]') || b).dataset.id;
      if (ACT[id]) ACT[id]();
      dismissHint();
    });

    // phones have no hover: the first time, say once that the steps can be tapped
    var hinted = false;
    try { hinted = !!localStorage.getItem(HINT_KEY); } catch (e) {}
    function dismissHint() { if (!root.classList.contains('show-hint')) return; root.classList.remove('show-hint'); try { localStorage.setItem(HINT_KEY, '1'); } catch (e) {} }
    if (!hinted && window.matchMedia && window.matchMedia('(hover: none)').matches) root.classList.add('show-hint');
  });
})();
