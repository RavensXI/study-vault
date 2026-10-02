/* Podcast transcript and extras on the lesson page (Tom, 1 Oct 2026; preview branch).

   Everything here hangs off files shipped in /transcripts/<subject>/<unit>/lNN.*:
     lNN.json            the transcript, turn by turn (MAI-Transcribe-2): required — no file, no feature
     lNN.study.json      chapters, lesson-section matches, "Check you listened" quiz
     lNN.factcheck.json  moments the hosts get wrong (shown to staff only)
     lNN.video.vtt       captions for the explainer video
   The podcast plays through the page's own player (js/main.js, one <audio> shared with
   narration), so this file only switches it to the podcast tab, seeks and reads its time. */
(function () {
  'use strict';
  var m = location.pathname.match(/^\/lesson\/([^/]+)\/([^/]+)\/(\d+)\/?$/);
  if (!m) return;
  var base = '/transcripts/' + m[1] + '/' + m[2] + '/l' + ('0' + m[3]).slice(-2);
  var qs = new URLSearchParams(location.search);

  function getJSON(url) {
    return fetch(url, { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fmt(s) { s = Math.max(0, Math.floor(s)); return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2); }
  function isStaff() {
    try {
      var a = JSON.parse(localStorage.getItem('studyvault-auth') || 'null');
      return !!(a && (a.role === 'admin' || a.role === 'teacher'));
    } catch (e) { return false; }
  }

  // Captions file: the video modal (lesson-loader.js) attaches it as a <track> when this is set.
  fetch(base + '.video.vtt', { method: 'HEAD' }).then(function (r) { if (r.ok) window._svCaptionsUrl = base + '.video.vtt'; }).catch(function () {});

  getJSON(base + '.json').then(function (tr) {
    if (!tr || !tr.turns || !tr.turns.length) return;
    Promise.all([getJSON(base + '.study.json'), isStaff() ? getJSON(base + '.factcheck.json') : Promise.resolve(null)])
      .then(function (r) { waitForPlayer(function () { build(tr, r[0] || {}, r[1] || []); }); });
  });

  function waitForPlayer(cb) {
    var tries = 0;
    (function poll() {
      var tabs = document.querySelector('.audio-player-tabs');
      var ready = window.podcastUrl && tabs && tabs.style.display !== 'none' && document.querySelector('.study-notes h2, .study-notes p');
      if (ready) return cb();
      if (++tries < 120) setTimeout(poll, 250);
    })();
  }

  function build(tr, study, flags) {
    var audio = document.querySelector('.narration-audio');
    var podTab = document.querySelector('.audio-tab[data-mode="podcast"]');
    var wrapper = document.querySelector('.audio-player-wrapper');
    if (!audio || !podTab || !wrapper) return;
    var names = tr.speakers || { 1: 'Host A', 2: 'Host B' };
    var turns = tr.turns;
    var chapters = study.chapters || [];
    var quiz = study.quiz || [];

    function inPodcast() { return !!(audio.currentSrc || audio.src) && (audio.currentSrc || audio.src).indexOf(window.podcastUrl) !== -1; }

    /* play the podcast from a moment: switch tabs if needed, then seek once the file is ready */
    /* A "Hear this explained" clip plays start -> end, fades out over the last 1.5 s, pauses,
       and offers "Keep listening". Any other way of playing (main button, chapter, paragraph)
       clears the clip, so only the Hear buttons ever stop early. */
    var clip = null, ownSeek = false, raf = 0, FADE = 1.5, keepTimer = 0;
    /* "Keep listening" lives in the floating player at the bottom (Tom, 2 Oct 2026): a pupil who
       starts a clip from a heading has usually scrolled away from the main player. When the main
       player is on screen instead, it sits in that player's control row. It goes after 10 s;
       the ordinary play button carries on from the same place anyway. */
    var keep = document.createElement('button');
    keep.type = 'button'; keep.className = 'svt-keep'; keep.hidden = true; keep.textContent = 'Keep listening';
    var fab = document.querySelector('.narration-fab');
    var fabTime = fab && fab.querySelector('.narration-fab-time');
    var meta = wrapper.querySelector('.narration-meta');
    function hideKeep() { clearTimeout(keepTimer); keep.hidden = true; if (fab) fab.classList.remove('svt-keeping'); }
    function showKeep() {
      var inFab = fab && fab.classList.contains('visible');
      if (inFab) { fab.insertBefore(keep, fab.querySelector('.narration-fab-progress')); fab.classList.add('svt-keeping'); }
      else meta.insertBefore(keep, meta.firstChild);
      keep.hidden = false;
      keep.focus({ preventScroll: true });
      clearTimeout(keepTimer);
      keepTimer = setTimeout(hideKeep, 10000);
    }
    function endClip(restore) {
      if (!clip) return;
      cancelAnimationFrame(raf);
      if (restore) audio.volume = clip.vol;
      clip = null;
      if (fab) fab.classList.remove('svt-in-clip');
    }
    function watchClip() {
      if (!clip) return;
      var left = clip.end - audio.currentTime;
      if (left <= FADE) audio.volume = Math.max(0, clip.vol * Math.max(0, left) / FADE);
      if (left <= 0.05) {
        var v = clip.vol;
        audio.pause();
        endClip(false);
        audio.volume = v;
        showKeep();
        return;
      }
      raf = requestAnimationFrame(watchClip);
    }
    /* while a clip plays, the floating player says how long is left of it */
    audio.addEventListener('timeupdate', function () {
      if (clip && fabTime) fabTime.textContent = fmt(Math.max(0, clip.end - audio.currentTime)) + ' left';
    });
    audio.addEventListener('seeking', function () { if (!ownSeek) endClip(true); });
    audio.addEventListener('seeked', function () { ownSeek = false; });
    audio.addEventListener('play', function () {
      hideKeep();
      if (clip) { cancelAnimationFrame(raf); raf = requestAnimationFrame(watchClip); }
    });
    audio.addEventListener('emptied', function () { endClip(true); hideKeep(); });
    keep.addEventListener('click', function () {
      hideKeep();
      var p = audio.play(); if (p && p.catch) p.catch(function () {});
    });

    function playAt(t, opts) {
      opts = opts || {};
      endClip(true);
      hideKeep();
      function go() {
        ownSeek = true;           /* cleared on 'seeked': our own jump must not cancel the clip */
        try { audio.currentTime = t; } catch (e) { ownSeek = false; }
        if (opts.end && opts.end > t) { clip = { end: opts.end, vol: audio.volume || 1 }; if (fab) fab.classList.add('svt-in-clip'); }
        if (!opts.cueOnly) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); }
      }
      if (!inPodcast()) podTab.click();
      if (audio.readyState >= 1 && inPodcast()) go();
      else audio.addEventListener('loadedmetadata', function once() { audio.removeEventListener('loadedmetadata', once); go(); });
    }
    window.svPodcastPlayAt = playAt;

    /* ---- the Transcript button: an icon in the player's control row, beside the speed.
       Shown in both modes so a pupil who cannot hear finds it without trying the podcast first. ---- */
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'svt-open svt-tipped';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', 'svt-panel');
    btn.setAttribute('aria-label', 'Podcast transcript');
    btn.dataset.tip = 'Podcast transcript';
    btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="4" width="17" height="16" rx="2.5"/><path d="M7.5 9h9M7.5 12.5h9M7.5 16h5.5"/></svg>';
    var speed = meta.querySelector('.narration-speed');
    meta.insertBefore(btn, speed ? speed.nextSibling : null);

    /* ---- the panel ---- */
    var panel = document.createElement('section');
    panel.id = 'svt-panel';
    panel.className = 'svt-panel';
    panel.hidden = true;
    panel.setAttribute('aria-label', 'Podcast transcript');
    var flagByTurn = {};
    (flags || []).forEach(function (f) {
      for (var i = 0; i < turns.length; i++) {
        if (f.start < turns[i].end + 1 || i === turns.length - 1) { (flagByTurn[i] = flagByTurn[i] || []).push(f); break; }
      }
    });
    var html = '<div class="svt-head"><h2 class="svt-title">Podcast transcript</h2>' +
      '<div class="svt-search"><label class="svt-sr" for="svt-q">Search the transcript</label>' +
      '<input id="svt-q" type="search" placeholder="Search the transcript" autocomplete="off">' +
      '<span class="svt-count" aria-live="polite"></span>' +
      '<button type="button" class="svt-next" aria-label="Next match">Next</button></div>' +
      '<button type="button" class="svt-close" aria-label="Close transcript">&times;</button></div>';
    if (flags && flags.length) {
      html += '<div class="svt-staff" role="note"><b>Staff only:</b> ' + flags.length + ' moment' + (flags.length > 1 ? 's' : '') +
        ' where the hosts may be wrong. Marked <span class="svt-flag-dot" aria-hidden="true">!</span> below.</div>';
    }
    if (chapters.length) {
      html += '<nav class="svt-chapters" aria-label="Podcast chapters"><h3>Chapters</h3><ol>' + chapters.map(function (c, i) {
        return '<li><button type="button" data-t="' + c.start + '"><span class="svt-ct">' + fmt(c.start) + '</span>' + esc(c.title) + '</button></li>';
      }).join('') + '</ol></nav>';
    }
    html += '<div class="svt-turns">' + turns.map(function (t, i) {
      var f = flagByTurn[i];
      return '<p class="svt-turn svt-s' + t.speaker + '" data-i="' + i + '" data-t="' + t.start + '" tabindex="0" role="button" aria-label="' +
        esc((names[t.speaker] || 'Host') + ' at ' + fmt(t.start) + '. Play from here.') + '">' +
        '<span class="svt-who">' + esc(names[t.speaker] || 'Host') + ' <span class="svt-time">' + fmt(t.start) + '</span></span>' +
        '<span class="svt-text">' + esc(t.text) + '</span>' +
        (f ? f.map(function (x) {
          return '<span class="svt-flag" role="note"><span class="svt-flag-dot" aria-hidden="true">!</span> ' +
            esc(x.problem) + (x.lesson_says ? ' <i>Lesson: ' + esc(x.lesson_says) + '</i>' : '') + '</span>';
        }).join('') : '') + '</p>';
    }).join('') + '</div>';
    if (quiz.length) {
      html += '<div class="svt-quiz"><h3>Check you listened</h3><ol>' + quiz.map(function (q, qi) {
        return '<li class="svt-q" data-q="' + qi + '"><p class="svt-qtext">' + esc(q.q) + '</p><div class="svt-opts" role="group" aria-label="Answers">' +
          q.options.map(function (o, oi) { return '<button type="button" class="svt-opt" data-o="' + oi + '">' + esc(o) + '</button>'; }).join('') +
          '</div><div class="svt-fb" aria-live="polite"></div></li>';
      }).join('') + '</ol><p class="svt-score" aria-live="polite"></p></div>';
    }
    panel.innerHTML = html;
    wrapper.parentNode.insertBefore(panel, wrapper.nextSibling);

    var turnEls = panel.querySelectorAll('.svt-turn');
    function open(focusSearch) {
      panel.hidden = false; btn.setAttribute('aria-expanded', 'true'); btn.classList.add('on');
      if (focusSearch) panel.querySelector('#svt-q').focus();
    }
    function close() { panel.hidden = true; btn.setAttribute('aria-expanded', 'false'); btn.classList.remove('on'); btn.focus(); }
    btn.addEventListener('click', function () { if (panel.hidden) open(); else close(); });
    panel.querySelector('.svt-close').addEventListener('click', close);

    /* click or Enter on a paragraph (or a chapter) plays from there */
    panel.addEventListener('click', function (e) {
      var el = e.target.closest('[data-t]');
      if (el && panel.contains(el) && !e.target.closest('.svt-opt')) playAt(parseFloat(el.dataset.t));
    });
    panel.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.key === ' ') && e.target.classList.contains('svt-turn')) { e.preventDefault(); playAt(parseFloat(e.target.dataset.t)); }
    });

    /* follow playback: the paragraph being spoken is highlighted and kept in view */
    var cur = -1, userScrolledAt = 0;
    var list = panel.querySelector('.svt-turns');
    list.addEventListener('wheel', function () { userScrolledAt = Date.now(); }, { passive: true });
    list.addEventListener('touchmove', function () { userScrolledAt = Date.now(); }, { passive: true });
    audio.addEventListener('timeupdate', function () {
      if (!inPodcast()) return;
      var t = audio.currentTime, i = cur;
      if (i < 0 || t < turns[i].start || (turns[i + 1] && t >= turns[i + 1].start)) {
        i = -1;
        for (var k = 0; k < turns.length; k++) { if (turns[k].start <= t + 0.05) i = k; else break; }
      }
      if (i === cur) return;
      if (cur >= 0 && turnEls[cur]) turnEls[cur].classList.remove('svt-now');
      cur = i;
      if (i >= 0 && turnEls[i]) {
        turnEls[i].classList.add('svt-now');
        if (!panel.hidden && Date.now() - userScrolledAt > 4000) {
          var top = turnEls[i].offsetTop - list.offsetTop - list.clientHeight / 3;
          list.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
        }
      }
      var chs = panel.querySelectorAll('.svt-chapters button');
      for (var c = 0; c < chs.length; c++) {
        var a = chapters[c].start, b = chapters[c + 1] ? chapters[c + 1].start : 1e9;
        chs[c].classList.toggle('svt-here', t >= a && t < b);
      }
    });

    /* search: highlight matches, Next jumps through them */
    var q = panel.querySelector('#svt-q'), countEl = panel.querySelector('.svt-count'), hits = [], hi = -1;
    function runSearch() {
      var term = q.value.trim().toLowerCase();
      hits = []; hi = -1;
      turnEls.forEach(function (el, i) {
        var txt = turns[i].text, span = el.querySelector('.svt-text');
        if (!term || term.length < 2) { span.textContent = txt; el.classList.remove('svt-hit'); return; }
        var low = txt.toLowerCase(), at = low.indexOf(term);
        if (at < 0) { span.textContent = txt; el.classList.remove('svt-hit'); return; }
        var out = '', from = 0;
        while (at >= 0) { out += esc(txt.slice(from, at)) + '<mark>' + esc(txt.slice(at, at + term.length)) + '</mark>'; from = at + term.length; at = low.indexOf(term, from); }
        span.innerHTML = out + esc(txt.slice(from));
        el.classList.add('svt-hit'); hits.push(el);
      });
      countEl.textContent = term.length < 2 ? '' : (hits.length ? hits.length + ' found' : 'Not found');
      if (hits.length) jump(0);
    }
    function jump(k) {
      if (!hits.length) return;
      hi = (k + hits.length) % hits.length;
      var el = hits[hi];
      list.scrollTo({ top: Math.max(0, el.offsetTop - list.offsetTop - 40), behavior: 'smooth' });
      userScrolledAt = Date.now();
    }
    var tmr;
    q.addEventListener('input', function () { clearTimeout(tmr); tmr = setTimeout(runSearch, 200); });
    q.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); jump(hi + 1); } });
    panel.querySelector('.svt-next').addEventListener('click', function () { jump(hi + 1); });

    /* chapter marks on the player's progress bar, shown while the podcast is the source */
    var bar = document.querySelector('.narration-progress');
    function marks() {
      if (!bar || !chapters.length) return;
      var old = bar.querySelectorAll('.svt-mark'); old.forEach(function (x) { x.remove(); });
      if (!inPodcast() || !(audio.duration > 0)) return;
      chapters.forEach(function (c) {
        if (c.start <= 0) return;
        var mk = document.createElement('span');
        mk.className = 'svt-mark'; mk.style.left = (c.start / audio.duration * 100) + '%'; mk.title = c.title;
        bar.appendChild(mk);
      });
    }
    audio.addEventListener('loadedmetadata', marks);
    audio.addEventListener('emptied', marks);
    marks();

    /* what the marks mean: pointing at the bar (or touching it) shows the chapter there and its
       time. (The chapter now playing was named beside the clock too; Tom took it out, 2 Oct 2026:
       a chapter title alone in the player read as nonsense.) */
    function chapterAt(t) {
      var k = -1;
      for (var i = 0; i < chapters.length; i++) if (chapters[i].start <= t + 0.5) k = i;
      return k;
    }
    var player = wrapper.querySelector('.narration-player');
    var tip = document.createElement('div');
    tip.className = 'svt-bartip'; tip.hidden = true; tip.setAttribute('aria-hidden', 'true');
    player.appendChild(tip);
    var tipTimer = 0;
    function showTip(clientX) {
      if (!bar || !chapters.length || !inPodcast() || !(audio.duration > 0)) { tip.hidden = true; return; }
      var r = bar.getBoundingClientRect(), pr = player.getBoundingClientRect();
      var f = Math.min(1, Math.max(0, (clientX - r.left) / r.width)), t = f * audio.duration, k = chapterAt(t);
      tip.innerHTML = (k >= 0 ? '<b>' + esc(chapters[k].title) + '</b>' : '') + '<span>' + fmt(t) + '</span>';
      tip.hidden = false;
      var w = tip.offsetWidth, x = clientX - pr.left;
      tip.style.left = Math.min(pr.width - w / 2 - 4, Math.max(w / 2 + 4, x)) + 'px';
      tip.style.top = (r.top - pr.top) + 'px';
    }
    if (bar && chapters.length) {
      bar.addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse') showTip(e.clientX); });
      bar.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') tip.hidden = true; });
      /* a touch has no hover: show it under the finger, and while it slides */
      bar.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') { clearTimeout(tipTimer); showTip(e.clientX); } });
      bar.addEventListener('touchmove', function (e) { if (e.touches[0]) showTip(e.touches[0].clientX); }, { passive: true });
      bar.addEventListener('pointerup', function (e) {
        if (e.pointerType !== 'mouse') { clearTimeout(tipTimer); tipTimer = setTimeout(function () { tip.hidden = true; }, 1500); }
      });
    }

    /* quiz: client-side marking; a wrong answer offers the moment it was said */
    var score = 0, answered = 0;
    panel.querySelectorAll('.svt-q').forEach(function (li) {
      var item = quiz[+li.dataset.q];
      li.querySelectorAll('.svt-opt').forEach(function (b) {
        b.addEventListener('click', function () {
          if (li.classList.contains('done')) return;
          li.classList.add('done'); answered++;
          var ok = +b.dataset.o === item.answer;
          if (ok) score++;
          li.querySelectorAll('.svt-opt').forEach(function (x) {
            x.disabled = true;
            if (+x.dataset.o === item.answer) x.classList.add('right');
          });
          if (!ok) b.classList.add('wrong');
          var fb = li.querySelector('.svt-fb');
          fb.innerHTML = (ok ? 'Right. ' : 'Not quite. ') + esc(item.why || '') +
            (ok ? '' : ' <button type="button" class="svt-again" data-t="' + item.start + '">Hear that part again (' + fmt(item.start) + ')</button>');
          if (answered === quiz.length) panel.querySelector('.svt-score').textContent = 'You got ' + score + ' out of ' + quiz.length + '.';
        });
      });
    });

    /* "Hear this explained" beside lesson headings the podcast clearly covers: a small round badge
       (a speech bubble, so it is not mistaken for the podcast's headphones). Hover or focus names
       it with the clip's length. Until a pupil has used one, the first badge also carries the
       words, since a phone has no hover; 'sv-hear-used' (account-synced) records that. */
    var hearUsed = false;
    try { hearUsed = localStorage.getItem('sv-hear-used') === '1'; } catch (e) {}
    var HEAR_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5H10l-4.5 4v-4h0A2.5 2.5 0 0 1 4 13.5z"/><path d="M10.2 6.9v5.2l4.3-2.6z" fill="currentColor" stroke="none"/></svg>';
    var firstHear = true;
    (study.sections || []).forEach(function (s) {
      if (!(s.confidence >= 0.75)) return;
      var hs = document.querySelectorAll('.study-notes h2, .study-notes h3'), h = null;
      for (var i = 0; i < hs.length; i++) {
        if ((s.id && hs[i].id === s.id) || hs[i].textContent.trim() === s.heading) { h = hs[i]; break; }
      }
      if (!h || h.querySelector('.svt-hear')) return;
      var b = document.createElement('button');
      var len = s.end > s.start ? ' · ' + fmt(s.end - s.start) : '';
      b.type = 'button'; b.className = 'svt-hear svt-tipped' + (!hearUsed && firstHear ? ' svt-hear-labelled' : '');
      firstHear = false;
      b.setAttribute('aria-label', 'Hear this explained in the podcast' + (len ? ', ' + fmt(s.end - s.start) + ' long' : ''));
      b.dataset.tip = 'Hear this explained' + len;
      b.innerHTML = HEAR_ICON + '<span class="svt-hear-words">Hear this explained</span>';
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        try { localStorage.setItem('sv-hear-used', '1'); } catch (x) {}
        document.querySelectorAll('.svt-hear-labelled').forEach(function (x) { x.classList.remove('svt-hear-labelled'); });
        playAt(s.start, { end: s.end });
      });
      h.appendChild(b);
    });

    /* deep link from the dashboard search: ?t=400&play=podcast cues the podcast there */
    if (qs.get('play') === 'podcast' && qs.get('t')) {
      var t0 = parseFloat(qs.get('t')) || 0;
      open();
      playAt(t0, { cueOnly: true });
      var near = 0; for (var k = 0; k < turns.length; k++) if (turns[k].start <= t0 + 0.5) near = k;
      setTimeout(function () {
        turnEls[near].classList.add('svt-now', 'svt-cued');
        list.scrollTo({ top: Math.max(0, turnEls[near].offsetTop - list.offsetTop - 40) });
        wrapper.scrollIntoView({ block: 'start', behavior: 'smooth' });
        var p = audio.play(); if (p && p.catch) p.catch(function () {});
      }, 400);
    }
  }
})();
