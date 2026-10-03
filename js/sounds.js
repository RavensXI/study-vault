/* StudyVault sounds (Tom, 3 Oct 2026; preview branch). A few quiet sounds that mark RESULTS, never
   navigation: a right answer, a wrong one, "partly", a lesson done (50%), fully explored (100%), an
   interactive mastered, and the revision timer. Generated in the browser (Web Audio, a soft
   marimba-like tone), so there is nothing to download.

   Rules: never on clicks, opening or closing; silent while narration, the podcast or a video is playing
   (the timer excepted); every sound sits beside something visible on screen; one switch, Sounds on/off
   in "Read your way" ('sv-sounds' = 'on' | 'off', account-synced), on by default and quiet.

   Browsers only allow sound after the page has been touched, so the first tap or key press on ANY page
   unlocks it. That is why the timer chime was rarely heard: a timer set on one page usually ends on
   another, where nothing had unlocked the sound yet. */
(function () {
  'use strict';
  var KEY = 'sv-sounds', ctx = null, master = null;

  function enabled() { try { return localStorage.getItem(KEY) !== 'off'; } catch (e) { return true; } }
  function setEnabled(on) { try { localStorage.setItem(KEY, on ? 'on' : 'off'); } catch (e) {} }

  function unlock() {
    try {
      if (!ctx) {
        var AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
        ctx = new AC(); master = ctx.createGain(); master.gain.value = 0.5; master.connect(ctx.destination);
      }
      if (ctx.state === 'suspended') ctx.resume();
    } catch (e) {}
  }
  ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) { document.addEventListener(ev, unlock, { capture: true, passive: true }); });

  function mediaPlaying() {
    var all = document.querySelectorAll('audio, video');
    for (var i = 0; i < all.length; i++) if (!all[i].paused && !all[i].muted) return true;
    return false;
  }

  /* one soft mallet note: a sine with a touch of its octave, quick attack, exponential decay */
  function note(freq, at, len, vol) {
    var t = ctx.currentTime + at;
    [[1, 1], [2, 0.18], [3, 0.05]].forEach(function (h) {
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.type = 'sine'; o.frequency.value = freq * h[0];
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(vol * h[1], t + 0.012);
      g.gain.exponentialRampToValueAtTime(0.0001, t + len);
      o.connect(g); g.connect(master); o.start(t); o.stop(t + len + 0.05);
    });
  }

  // the palette: C major, gentle, short
  var SOUNDS = {
    right:    function () { note(659.3, 0, 0.35, 0.22); note(987.8, 0.09, 0.5, 0.2); },               // E5 -> B5, a small lift
    partly:   function () { note(587.3, 0, 0.4, 0.18); },                                                // D5, neutral
    wrong:    function () { note(220.0, 0, 0.32, 0.2); note(207.7, 0.07, 0.38, 0.14); },               // A3 -> G#3, a low muted tap
    done:     function () { [523.3, 659.3, 784.0].forEach(function (f, i) { note(f, i * 0.09, 0.7, 0.2); }); note(1046.5, 0.3, 1.1, 0.12); },
    explored: function () { [523.3, 659.3, 784.0, 1046.5].forEach(function (f, i) { note(f, i * 0.085, 0.9, 0.2); }); note(1318.5, 0.38, 1.4, 0.12); note(784.0, 0.38, 1.4, 0.1); },
    mastery:  function () { [784.0, 987.8, 1174.7].forEach(function (f, i) { note(f, i * 0.07, 0.6, 0.18); }); },
    timer:    function () { for (var r = 0; r < 3; r++) { note(587.3, r * 0.75, 0.6, 0.32); note(784.0, r * 0.75 + 0.18, 0.8, 0.32); } }
  };

  function play(name, opts) {
    opts = opts || {};
    if (!SOUNDS[name] || !enabled()) return false;
    if (!opts.force && mediaPlaying()) return false;       // never over narration, the podcast or a video
    unlock();
    if (!ctx || ctx.state !== 'running') return false;
    try { SOUNDS[name](); return true; } catch (e) { return false; }
  }

  window.svSound = { play: play, enabled: enabled, setEnabled: setEnabled, unlock: unlock };

  // an interactive mastered (js/widget-embed.js announces it)
  document.addEventListener('sv-widget-mastered', function () { play('mastery'); });
})();
