/**
 * Inline waveform player for practice-format lessons.
 *
 * Why this exists separately from the Guided Listening dock in main.js:
 * practice.html does not load main.js, and the two components want opposite
 * things. The dock is fixed to the viewport, carries pinned annotations and a
 * staff "adjust pins" bar, and is right for walking a student THROUGH a set
 * work. A drill needs none of that — Section A is unfamiliar listening, so
 * annotating the excerpt would delete the skill being tested. This is just a
 * transport and a waveform, sitting in the flow of the passage.
 *
 * Markup (written into passage HTML by scripts/music-practice/apply_inline_player.py):
 *
 *   <figure class="sv-ap-inline" data-audio="https://.../clip.mp3">
 *     <div class="sv-api-bar">
 *       <button type="button" class="sv-api-play" aria-label="Play">&#9654;</button>
 *       <span class="sv-api-tick">0:00 / 0:00</span>
 *     </div>
 *     <div class="sv-api-wrap"><canvas class="sv-api-canvas"></canvas></div>
 *     <script type="application/json" class="sv-api-peaks">{"peaks":[...],"duration":12.6}<\/script>
 *   </figure>
 *
 * Peaks travel inline because R2 sends no Access-Control-Allow-Origin header,
 * so a cross-origin fetch of a .peaks.json is blocked in the browser.
 *
 * A <script> injected via innerHTML never executes, which is exactly what we
 * want — it is inert data we read with .textContent.
 */
(function () {
  'use strict';

  var registry = [];      // every figure we have wired, so we can stop orphans
  var playing = null;     // at most one drill clip audible at a time

  function fmt(t) {
    t = Math.max(0, Math.floor(t || 0));
    return Math.floor(t / 60) + ':' + ('0' + (t % 60)).slice(-2);
  }

  function stopOrphans() {
    for (var i = registry.length - 1; i >= 0; i--) {
      var e = registry[i];
      if (!document.contains(e.fig)) {
        try { e.audio.pause(); } catch (err) {}
        if (playing === e) playing = null;
        registry.splice(i, 1);
      }
    }
  }

  function setup(fig) {
    if (fig.getAttribute('data-api-init')) return;
    fig.setAttribute('data-api-init', '1');

    var src = fig.getAttribute('data-audio');
    var cv = fig.querySelector('.sv-api-canvas');
    var playB = fig.querySelector('.sv-api-play');
    var tick = fig.querySelector('.sv-api-tick');
    var wrap = fig.querySelector('.sv-api-wrap');
    if (!src || !cv || !playB || !tick || !wrap) return;

    var peaks = null, dur = 0;
    var holder = fig.querySelector('.sv-api-peaks');
    if (holder) {
      try {
        var d = JSON.parse(holder.textContent);
        peaks = d.peaks;
        dur = d.duration || 0;
      } catch (e) {}
    }

    var audio = new Audio();
    audio.preload = 'metadata';
    audio.src = src;

    var entry = { fig: fig, audio: audio };
    registry.push(entry);

    var ctx = cv.getContext('2d');
    var raf = null;

    function draw() {
      var w = cv.clientWidth, h = cv.clientHeight;
      if (!w || !h) return;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      if (cv.width !== Math.round(w * dpr)) {
        cv.width = Math.round(w * dpr);
        cv.height = Math.round(h * dpr);
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, w, h);
      if (!peaks || !peaks.length) return;
      var played = dur ? audio.currentTime / dur : 0;
      var bw = w / peaks.length;
      for (var i = 0; i < peaks.length; i++) {
        var bh = Math.max(2, peaks[i] * (h - 4));
        ctx.fillStyle = (i / peaks.length) < played
          ? 'rgba(45,42,38,0.85)'
          : 'rgba(45,42,38,0.22)';
        ctx.fillRect(i * bw, (h - bh) / 2, Math.max(1, bw - 1), bh);
      }
    }

    function tickText() {
      tick.textContent = fmt(audio.currentTime) + ' / ' + fmt(dur || audio.duration);
    }

    function loop() {
      tickText();
      draw();
      raf = requestAnimationFrame(loop);
    }
    function startLoop() { if (raf === null) loop(); }
    function stopLoop() {
      if (raf !== null) { cancelAnimationFrame(raf); raf = null; }
      tickText(); draw();
    }

    audio.addEventListener('loadedmetadata', function () {
      // trust the real file over the manifest if they disagree
      if (audio.duration && isFinite(audio.duration)) {
        if (!dur || Math.abs(audio.duration - dur) > 0.5) dur = audio.duration;
      }
      tickText(); draw();
    });

    playB.addEventListener('click', function () {
      if (audio.paused) {
        if (playing && playing !== entry) {
          try { playing.audio.pause(); } catch (e) {}
        }
        playing = entry;
        audio.play();
      } else {
        audio.pause();
      }
    });

    audio.addEventListener('play', function () {
      playB.innerHTML = '&#10074;&#10074;';
      playB.setAttribute('aria-label', 'Pause');
      fig.classList.add('is-playing');
      startLoop();
    });
    function onStop() {
      playB.innerHTML = '&#9654;';
      playB.setAttribute('aria-label', 'Play');
      fig.classList.remove('is-playing');
      stopLoop();
    }
    audio.addEventListener('pause', onStop);
    audio.addEventListener('ended', function () { audio.currentTime = 0; onStop(); });

    function seekToClientX(clientX) {
      var r = cv.getBoundingClientRect();
      var d = dur || audio.duration;
      if (!d || !isFinite(d)) return;
      audio.currentTime = Math.max(0, Math.min(d, d * (clientX - r.left) / r.width));
      tickText(); draw();
    }
    cv.addEventListener('click', function (e) { seekToClientX(e.clientX); });

    // keyboard: the wrap is focusable so a clip is usable without a mouse
    wrap.setAttribute('tabindex', '0');
    wrap.setAttribute('role', 'slider');
    wrap.setAttribute('aria-label', 'Seek within the extract');
    wrap.addEventListener('keydown', function (e) {
      var d = dur || audio.duration;
      if (!d || !isFinite(d)) return;
      if (e.key === 'ArrowRight') { audio.currentTime = Math.min(d, audio.currentTime + 2); }
      else if (e.key === 'ArrowLeft') { audio.currentTime = Math.max(0, audio.currentTime - 2); }
      else if (e.key === 'Home') { audio.currentTime = 0; }
      else if (e.key === ' ' || e.key === 'Enter') { playB.click(); }
      else { return; }
      e.preventDefault();
      tickText(); draw();
    });

    window.addEventListener('resize', draw);
    tickText();
    // canvas has no width until it is laid out; one frame later it does
    requestAnimationFrame(draw);
    setTimeout(draw, 120);
  }

  function initAll() {
    stopOrphans();
    var list = document.querySelectorAll('.sv-ap-inline');
    for (var i = 0; i < list.length; i++) setup(list[i]);
  }
  window.initPracticeAudio = initAll;

  // Passage panels, worked examples and the method-card modal each inject their
  // own HTML at different moments. Watching the tree is one hook instead of
  // three, and it picks up any injection site added later.
  function watch() {
    initAll();
    if (window._svPracticeAudioWatcher || !window.MutationObserver) return;
    var queued = false;
    var obs = new MutationObserver(function (muts) {
      if (queued) return;
      for (var i = 0; i < muts.length; i++) {
        var added = muts[i].addedNodes;
        for (var j = 0; j < added.length; j++) {
          var n = added[j];
          if (n.nodeType !== 1) continue;
          if ((n.classList && n.classList.contains('sv-ap-inline')) ||
              (n.querySelector && n.querySelector('.sv-ap-inline'))) {
            queued = true;
            requestAnimationFrame(function () { queued = false; initAll(); });
            return;
          }
        }
      }
    });
    obs.observe(document.body, { childList: true, subtree: true });
    window._svPracticeAudioWatcher = obs;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', watch);
  } else {
    watch();
  }
})();
