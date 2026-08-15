/**
 * Play-along notation for Score Reading.
 *
 * The exam is a LISTENING paper: when notation appears it appears with music
 * playing, and the questions join what you hear to what you see. A student who
 * cannot read music has no way into a silent picture, but can follow a
 * highlight that moves across the notes as they sound. That is the whole idea.
 *
 * Audio is synthesised in the browser rather than streamed: no files, no R2, no
 * licensing, and the highlight can never drift out of sync with a recording.
 * A plain tone is also clearer than a performance when the point is "which note
 * is longer".
 *
 * Markup (written by scripts/music-practice/notation.py::playable):
 *   <figure class="sv-scoreplay">
 *     <script type="application/json" class="sv-sp-map">
 *       {"tempo":100,"notes":[{"id":"abc123","midi":60,"beats":1}, ...]}
 *     </script>
 *     ...engraved svg...
 *     <div class="sv-sp-bar"><button class="sv-sp-play">Play</button>
 *          <span class="sv-sp-hint">Watch the notes light up</span></div>
 *   </figure>
 *
 * Optional per-note fields (Tom's review, 15 Aug — dynamics and articulation
 * were printed but not performed, which teaches students that markings are
 * decoration):
 *   vel   0..1  loudness multiplier (p ≈ 0.45, mf ≈ 0.75, f ≈ 1.0)
 *   art   "stac" sounds ~45% of the beat then silence; "leg" sounds the full
 *         beat with a soft release so notes join up. Default keeps the old 92%.
 * The clock ALWAYS advances by the full printed beats — articulation changes
 * how long a note SOUNDS, never how long it LASTS. (Staccato was previously
 * faked by shortening beats, which made staccato bars rush.)
 */
(function () {
  'use strict';

  var AC = null;
  function ctx() {
    if (!AC) AC = new (window.AudioContext || window.webkitAudioContext)();
    return AC;
  }
  var current = null;   // only one example sounds at a time

  function hz(midi) { return 440 * Math.pow(2, (midi - 69) / 12); }

  function setup(fig) {
    if (fig.getAttribute('data-sp-init')) return;
    fig.setAttribute('data-sp-init', '1');

    var holder = fig.querySelector('.sv-sp-map');
    var btn = fig.querySelector('.sv-sp-play');
    if (!holder || !btn) return;
    var map;
    try { map = JSON.parse(holder.textContent); } catch (e) { return; }
    var notes = map.notes || [];
    var beatMs = 60000 / (map.tempo || 100);

    var timers = [];
    function clearAll() {
      timers.forEach(clearTimeout);
      timers = [];
      notes.forEach(function (n) {
        if (!n.id) return;          // rests carry no element
        var g = fig.querySelector('#' + CSS.escape(n.id));
        if (g) g.classList.remove('sv-sp-on');
      });
    }

    function stop() {
      clearAll();
      fig.classList.remove('is-playing');
      btn.textContent = 'Play';
      if (current === fig) current = null;
    }

    function play() {
      if (current && current !== fig) {
        var other = current;
        current = null;
        other.dispatchEvent(new CustomEvent('sv-sp-stop'));
      }
      clearAll();
      var c = ctx();
      if (c.state === 'suspended') c.resume();
      current = fig;
      fig.classList.add('is-playing');
      btn.textContent = 'Stop';

      var t = 0;
      notes.forEach(function (n) {
        var dur = n.beats * beatMs;
        // schedule the sound on the audio clock (accurate) ...
        if (n.midi) {
          var o = c.createOscillator(), g = c.createGain();
          o.type = 'triangle';
          o.frequency.value = hz(n.midi);
          var t0 = c.currentTime + t / 1000;
          // articulation: how much of the beat SOUNDS (the clock is untouched)
          var frac = n.art === 'stac' ? 0.45 : (n.art === 'leg' ? 1.0 : 0.92);
          var t1 = t0 + Math.max(0.09, dur / 1000 * frac);
          var peak = 0.22 * (typeof n.vel === 'number' ? n.vel : 1);
          g.gain.setValueAtTime(0.0001, t0);
          g.gain.exponentialRampToValueAtTime(Math.max(peak, 0.0002), t0 + 0.015);
          if (n.art === 'leg') {
            // hold, then a short release INTO the next note — joined, not gapped
            g.gain.setValueAtTime(Math.max(peak, 0.0002), t1 - 0.03);
            g.gain.exponentialRampToValueAtTime(0.0001, t1 + 0.02);
          } else {
            g.gain.exponentialRampToValueAtTime(0.0001, t1);
          }
          o.connect(g); g.connect(c.destination);
          o.start(t0); o.stop(t1 + 0.04);
        }
        // ...and the highlight on a timer (accurate enough for the eye)
        if (n.id) (function (id, at, len) {
          timers.push(setTimeout(function () {
            var el = fig.querySelector('#' + CSS.escape(id));
            if (el) el.classList.add('sv-sp-on');
          }, at));
          timers.push(setTimeout(function () {
            var el = fig.querySelector('#' + CSS.escape(id));
            if (el) el.classList.remove('sv-sp-on');
          }, at + len));
        })(n.id, t, dur);
        t += dur;
      });
      timers.push(setTimeout(stop, t + 120));
    }

    fig.addEventListener('sv-sp-stop', stop);
    btn.addEventListener('click', function () {
      if (fig.classList.contains('is-playing')) stop(); else play();
    });
  }

  function initAll() {
    document.querySelectorAll('.sv-scoreplay').forEach(setup);
  }
  window.initScorePlayers = initAll;

  function watch() {
    initAll();
    if (window._svScoreWatcher || !window.MutationObserver) return;
    var queued = false;
    var obs = new MutationObserver(function () {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () { queued = false; initAll(); });
    });
    obs.observe(document.body, { childList: true, subtree: true });
    window._svScoreWatcher = obs;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', watch);
  } else {
    watch();
  }
})();
