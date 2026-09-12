/* Revision timer that follows the student from page to page (Tom, 12 Sep 2026).
   The countdown is a timestamp in localStorage (sv-timer: {end, total}), so every
   page carries on from the wall clock — lessons, practice, the planner, refreshes.
   Per device, never synced (a timer is not progress); never pauses when hidden.
   The cosy desk's wristwatch reads and writes the same store; every other page
   mounts a small dial in its header: tap for 15 / 25 / 45 minutes or stop. */
(function () {
  'use strict';
  var KEY = 'sv-timer';
  function read() { try { var t = JSON.parse(localStorage.getItem(KEY) || 'null'); if (t && t.end > Date.now()) return t; } catch (e) {} return null; }
  function set(min) { var t = { end: Date.now() + min * 60000, total: min * 60000 }; try { localStorage.setItem(KEY, JSON.stringify(t)); } catch (e) {} unlock(); return t; }
  function stop() { try { localStorage.removeItem(KEY); } catch (e) {} }
  /* a soft two-note chime; the AudioContext is unlocked on the start tap so it may sound minutes later */
  var actx = null;
  function unlock() { try { if (!actx) actx = new (window.AudioContext || window.webkitAudioContext)(); if (actx.state === 'suspended') actx.resume(); } catch (e) {} }
  function chime() {
    if (!actx) return;
    var t0 = actx.currentTime;
    [587.33, 783.99].forEach(function (freq, i) {
      var o = actx.createOscillator(), g = actx.createGain(), off = i * 0.22;
      o.type = 'sine'; o.frequency.value = freq; o.connect(g); g.connect(actx.destination);
      g.gain.setValueAtTime(0.0001, t0 + off); g.gain.exponentialRampToValueAtTime(0.16, t0 + off + 0.03); g.gain.exponentialRampToValueAtTime(0.0001, t0 + off + 1.0);
      o.start(t0 + off); o.stop(t0 + off + 1.05);
    });
  }
  function mmss(ms) { var s = Math.max(0, Math.round(ms / 1000)), m = Math.floor(s / 60); s = s % 60; return m + ':' + (s < 10 ? '0' : '') + s; }

  var CSS = '.svtimer{position:relative;display:inline-flex;align-items:center;gap:6px;border:0;background:none;padding:2px 4px;cursor:pointer;font:600 .82rem Inter,system-ui,sans-serif;color:#4a4239;flex:none}'
    + '.svtimer .dial{width:28px;height:28px;display:block}'
    + '.svtimer .dial .ring{fill:#fffdf8;stroke:#3a2615;stroke-width:1.5}'
    + '.svtimer .dial .arc{fill:none;stroke:#c06325;stroke-width:2.2;stroke-linecap:round;transform:rotate(-90deg);transform-origin:50% 50%;transition:stroke-dashoffset .9s linear}'
    + '.svtimer .dial .tick{stroke:#3a2615;stroke-width:1.1;stroke-linecap:round}'
    + '.svtimer .dial .hand{stroke:#3a2615;stroke-width:1.7;stroke-linecap:round}'
    + '.svtimer .dial .pin{fill:#3a2615}'
    + '.svtimer .left{font-variant-numeric:tabular-nums;min-width:0}.svtimer .left:empty{display:none}'
    + '.svtimer.flash .dial{animation:svtflash .35s ease-in-out 5}@keyframes svtflash{50%{transform:scale(1.25)}}'
    + '.svtimer-pop{position:absolute;top:calc(100% + 8px);right:0;z-index:1000;background:#fff;border:1px solid #d5c9b3;border-radius:6px;padding:.4rem;display:none;gap:.3rem;box-shadow:0 10px 26px rgba(40,28,12,.16)}'
    + '.svtimer-pop.open{display:flex}'
    + '.svtimer-pop button{font:600 .82rem Inter,system-ui,sans-serif;color:#2d2a26;background:#faf8f5;border:1px solid #e4dfd2;border-radius:4px;padding:.4rem .7rem;cursor:pointer;white-space:nowrap}'
    + '.svtimer-pop button:hover{border-color:#c06325;color:#c06325}.svtimer-pop button.stop{color:#9a3a25}'
    + '@media (max-width:700px){.svtimer .left{font-size:.76rem}}';

  function mount(where) {
    if (!where || document.querySelector('.svtimer')) return null;
    if (!document.getElementById('svtimer-css')) { var st = document.createElement('style'); st.id = 'svtimer-css'; st.textContent = CSS; document.head.appendChild(st); }
    var wrap = document.createElement('span'); wrap.style.position = 'relative'; wrap.style.display = 'inline-flex'; wrap.className = 'svtimer-wrap';
    var b = document.createElement('button'); b.type = 'button'; b.className = 'svtimer'; b.setAttribute('aria-label', 'Revision timer');
    /* a small clock: face, four ticks, hands at ten past ten, a pin; the rust arc runs round the outside */
    var R = 12.6, C = 2 * Math.PI * R;
    b.innerHTML = '<svg class="dial" viewBox="0 0 28 28" aria-hidden="true"><circle class="ring" cx="14" cy="14" r="10.3"/>'
      + [0, 90, 180, 270].map(function (a) { return '<line class="tick" x1="14" y1="5" x2="14" y2="6.8" transform="rotate(' + a + ' 14 14)"/>'; }).join('')
      + '<line class="hand" x1="14" y1="14" x2="10.6" y2="11"/><line class="hand" x1="14" y1="14" x2="18.6" y2="9.4"/><circle class="pin" cx="14" cy="14" r="1.2"/>'
      + '<circle class="arc" cx="14" cy="14" r="' + R + '" stroke-dasharray="' + C.toFixed(2) + '" stroke-dashoffset="' + C.toFixed(2) + '"/></svg><span class="left"></span>';
    var pop = document.createElement('span'); pop.className = 'svtimer-pop';
    pop.innerHTML = '<button data-min="15">15 min</button><button data-min="25">25 min</button><button data-min="45">45 min</button><button class="stop" data-min="0">Stop</button>';
    wrap.appendChild(b); wrap.appendChild(pop);
    where.parentNode ? where.parentNode.insertBefore(wrap, where) : document.body.appendChild(wrap);
    var arc = b.querySelector('.arc'), left = b.querySelector('.left'), fired = false;
    function tick() {
      var t = read();
      if (!t) { arc.style.strokeDashoffset = C; left.textContent = ''; pop.querySelector('.stop').style.display = 'none';
        try { if (localStorage.getItem(KEY) && !fired) { fired = true; b.classList.add('flash'); chime(); stop(); setTimeout(function () { b.classList.remove('flash'); }, 2000); } } catch (e) {}
        return; }
      fired = false; pop.querySelector('.stop').style.display = '';
      var frac = (t.end - Date.now()) / t.total; arc.style.strokeDashoffset = (C * (1 - Math.max(0, Math.min(1, frac)))).toFixed(2);
      left.textContent = mmss(t.end - Date.now());
    }
    b.addEventListener('click', function (e) { e.stopPropagation(); pop.classList.toggle('open'); });
    pop.querySelectorAll('button').forEach(function (x) { x.addEventListener('click', function (e) { e.stopPropagation(); var m = +x.dataset.min; if (m) set(m); else stop(); pop.classList.remove('open'); tick(); }); });
    document.addEventListener('click', function () { pop.classList.remove('open'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') pop.classList.remove('open'); });
    tick(); setInterval(tick, 1000);
    return b;
  }
  window.svTimer = { read: read, set: set, stop: stop, chime: chime, unlock: unlock, mount: mount };
  /* mount points: the classic top bar (before the podcast player); lesson and practice headers (before Next Lesson).
     The desk has its own wristwatch and mounts nothing. */
  function auto() {
    if (document.getElementById('watch')) return;
    var at = document.querySelector('.top .podbar') || document.getElementById('nav-next-lesson');
    if (at) mount(at);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', auto); else auto();
})();
