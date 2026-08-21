/* StudyVault lesson widget — sampling-repeated-measurement
   Self-contained. No imports, no network, no storage outside root. */
(function () {
  'use strict';

  var WIN = 0.006;            /* seconds of the clip drawn on the stage */
  var CD_RATE = 44100, CD_BITS = 16, CD_SECS = 60;

  /* ---- waves: parts are [amplitude, harmonic, phase] over `cycles` in WIN ---- */
  var WAVES = [
    { cycles: 3, parts: [[1, 1, 0]] },
    { cycles: 2, parts: [[1, 1, 0], [0.35, 3, 0]] },
    { cycles: 4, parts: [[1, 1, 0], [0.30, 2, 1.1]] },
    { cycles: 3, parts: [[1, 1, 0], [0.40, 3, 0.6]] }
  ];

  var ROUNDS = [
    { wave: 0, rate: 2000, bits: 8,  secs: 3 },
    { wave: 1, rate: 1000, bits: 16, secs: 4 },
    { wave: 2, rate: 4000, bits: 4,  secs: 5 },
    { wave: 3, rate: 2000, bits: 16, secs: 2 },
    { wave: 0, rate: 4000, bits: 8,  secs: 2 },
    { wave: 1, rate: 1000, bits: 8,  secs: 5 },
    { wave: 2, rate: 2000, bits: 4,  secs: 4 },
    { wave: 3, rate: 4000, bits: 16, secs: 3 }
  ];

  /* ---------------- model ---------------- */

  function rawWave(w, u) {                 /* u = fraction of the window */
    var v = 0, i, p;
    for (i = 0; i < w.parts.length; i++) {
      p = w.parts[i];
      v += p[0] * Math.sin(2 * Math.PI * p[1] * w.cycles * u + p[2]);
    }
    return v;
  }
  function peakOf(w) {
    if (w._peak) return w._peak;
    var m = 0, i, v;
    for (i = 0; i <= 2000; i++) { v = Math.abs(rawWave(w, i / 2000)); if (v > m) m = v; }
    w._peak = m || 1;
    return w._peak;
  }
  function waveAt(w, u) { return rawWave(w, u) / peakOf(w); }

  function quantise(v, bits) {             /* v in [-1,1] -> nearest stored level */
    var levels = Math.pow(2, bits) - 1;
    var k = Math.round((v + 1) / 2 * levels);
    if (k < 0) k = 0; if (k > levels) k = levels;
    return (k / levels) * 2 - 1;
  }

  function sampleSet(r) {                  /* the measured points inside the window */
    var w = WAVES[r.wave];
    var n = Math.round(WIN * r.rate), i, u, pts = [];
    for (i = 0; i <= n; i++) {
      u = i / n;
      pts.push({ u: u, v: quantise(waveAt(w, u), r.bits) });
    }
    return pts;
  }

  function reconstructAt(pts, u) {         /* join the stored points back up */
    if (u <= pts[0].u) return pts[0].v;
    var i;
    for (i = 1; i < pts.length; i++) {
      if (u <= pts[i].u) {
        var a = pts[i - 1], b = pts[i];
        var f = (u - a.u) / (b.u - a.u);
        return a.v + (b.v - a.v) * f;
      }
    }
    return pts[pts.length - 1].v;
  }

  function worstError(r) {                 /* biggest gap, as % of the wave's height */
    var w = WAVES[r.wave], pts = sampleSet(r), m = 0, i, u, d;
    for (i = 0; i <= 900; i++) {
      u = i / 900;
      d = Math.abs(waveAt(w, u) - reconstructAt(pts, u));
      if (d > m) m = d;
    }
    return Math.round(m * 100);
  }

  function facts(r) {
    var samples = r.rate * r.secs;
    var totalBits = r.rate * r.bits * r.secs;
    var bytes = totalBits / 8;
    return {
      samples: samples, totalBits: totalBits, bytes: bytes, kb: bytes / 1000,
      spc: r.rate / (WAVES[r.wave].cycles / WIN)
    };
  }

  /* ---------------- answer options (derived, never hand-authored) ---------------- */

  function countOptions(r) {
    var f = facts(r);
    var opts = [
      { key: 'right',    n: f.samples,   label: fmt(f.samples) },
      { key: 'rateOnly', n: r.rate,      label: fmt(r.rate) },
      { key: 'bitTotal', n: f.totalBits, label: fmt(f.totalBits) },
      { key: 'whole',    n: -1,          label: 'The whole wave' }
    ];
    return opts;
  }

  function sizeOptions(r) {
    var f = facts(r), C = f.kb;
    var cands = [
      { key: 'noDiv8',    v: C * 8 },
      { key: 'noSecs',    v: C / r.secs },
      { key: 'byteEach',  v: r.rate * r.secs / 1000 },
      { key: 'div8twice', v: C / 8 },
      { key: 'timesSecs', v: C * r.secs },
      { key: 'halved',    v: C / 2 },
      { key: 'doubled',   v: C * 2 }
    ];
    var out = [{ key: 'right', v: C, label: fmt(C) + ' kB' }];
    var seen = {}; seen[C] = 1;
    for (var i = 0; i < cands.length && out.length < 4; i++) {
      var v = cands[i].v;
      if (v > 0 && v === Math.floor(v) && !seen[v]) {
        seen[v] = 1;
        out.push({ key: cands[i].key, v: v, label: fmt(v) + ' kB' });
      }
    }
    var mult = 3;
    while (out.length < 4) {                 /* guarantee four distinct whole-number options */
      var extra = C * mult;
      if (!seen[extra]) { seen[extra] = 1; out.push({ key: 'timesSecs', v: extra, label: fmt(extra) + ' kB' }); }
      mult++;
    }
    return out;
  }

  var COUNT_WHY = {
    rateOnly: function (r) { return fmt(r.rate) + ' is the rate — measurements in one second. The clip runs for ' + r.secs + ' s.'; },
    bitTotal: function (r) { return fmt(facts(r).totalBits) + ' is the number of bits, not the number of measurements — each measurement is ' + r.bits + ' bits wide.'; },
    whole:    function ()  { return 'The whole wave is never kept: the ADC only ever stores the readings taken at the dotted lines.'; }
  };
  var SIZE_WHY = {
    noDiv8:    function (r) { return fmt(facts(r).totalBits / 1000) + ' kB is the bit total read as bytes — divide the bits by 8 first.'; },
    noSecs:    function (r) { return 'That is one second’s worth; the clip lasts ' + r.secs + ' s.'; },
    byteEach:  function (r) { return 'That treats every measurement as one byte, but each one is ' + r.bits + ' bits — ' + (r.bits / 8) + ' bytes.'; },
    div8twice: function ()  { return 'That divides by 8 one time too many.'; },
    timesSecs: function (r) { return 'That counts the ' + r.secs + ' seconds in twice.'; },
    halved:    function ()  { return 'That is half of it — check the bit depth.'; },
    doubled:   function ()  { return 'That is double — check the bit depth.'; }
  };

  function fmt(n) {
    var s = (Math.round(n * 100) / 100).toString();
    var parts = s.split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return parts.join('.');
  }
  function tidy(n) { return fmt(Math.round(n * 10) / 10); }
  function art(n) { return (n === 8 || n === 11 || n === 18) ? 'an ' : 'a '; }
  function phrase(a) { return a.key === 'whole' ? 'the whole wave is stored' : a.label + ' measurements'; }

  /* ---------------- widget ---------------- */

  window.SVWidget = {
    meta: {
      id: 'sampling-repeated-measurement',
      title: 'Sampling a sound wave',
      teaches: 'Sampling is repeated measurement at fixed intervals: the stored file is rate × bit depth × seconds, and the wave between the measurements is lost.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var nodeAccent = '';
      try { nodeAccent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim(); } catch (e) {}
      var accent = ctx.accent || nodeAccent || '#4f7d63';
      var still = !!ctx.reducedMotion;

      root.className = (root.className ? root.className + ' ' : '') + 'svw-samp';
      if (still) root.className += ' svw-samp--still';
      root.style.setProperty('--svw-a', accent);

      root.innerHTML = [
        '<p class="svw-samp__kicker">Digital sound</p>',
        '<h3 class="svw-samp__title">Sampling a sound wave</h3>',
        '<p class="svw-samp__frame" data-r="frame"></p>',
        '<div class="svw-samp__stage">',
        '  <canvas class="svw-samp__canvas" data-r="canvas" role="img"></canvas>',
        '  <p class="svw-samp__params" data-r="params"></p>',
        '</div>',
        '<div class="svw-samp__step" data-r="step1">',
        '  <p class="svw-samp__lab"><span class="svw-samp__num">1</span> Measurements stored in the clip</p>',
        '  <div class="svw-samp__opts" data-r="opts1" role="group" aria-label="Measurements stored in the clip"></div>',
        '  <button type="button" class="svw-samp__done" data-r="done1" disabled hidden></button>',
        '</div>',
        '<div class="svw-samp__step" data-r="step2" hidden>',
        '  <p class="svw-samp__lab"><span class="svw-samp__num">2</span> Size of the file</p>',
        '  <div class="svw-samp__opts" data-r="opts2" role="group" aria-label="Size of the file"></div>',
        '  <button type="button" class="svw-samp__done" data-r="done2" disabled hidden></button>',
        '</div>',
        '<div class="svw-samp__actions">',
        '  <button type="button" class="svw-samp__primary" data-r="check">Check</button>',
        '  <button type="button" class="svw-samp__ghost" data-r="next" disabled hidden>Next wave</button>',
        '  <span class="svw-samp__run" data-r="run"></span>',
        '</div>',
        '<p class="svw-samp__caption" data-r="caption"></p>',
        '<p class="svw-samp__sr" data-r="sr" aria-live="polite"></p>'
      ].join('');

      var style = document.createElement('style');
      style.textContent = CSS;
      root.insertBefore(style, root.firstChild);

      var el = {};
      var nodes = root.querySelectorAll('[data-r]');
      for (var i = 0; i < nodes.length; i++) el[nodes[i].getAttribute('data-r')] = nodes[i];

      var g = el.canvas.getContext('2d');

      /* build the option buttons once, then mutate them */
      var btn1 = [], btn2 = [], k;
      for (k = 0; k < 4; k++) {
        btn1.push(mkOpt(el.opts1, 1, k));
        btn2.push(mkOpt(el.opts2, 2, k));
      }
      function mkOpt(host, which, idx) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'svw-samp__opt';
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', function () { pick(which, idx); });
        host.appendChild(b);
        return b;
      }

      var S = {
        round: 0, streak: 0, attempted: 0, mastered: false,
        pick1: -1, pick2: -1, revealed: false, opts1: [], opts2: []
      };

      el.check.addEventListener('click', commit);
      el.next.addEventListener('click', function () { S.round = (S.round + 1) % ROUNDS.length; newRound(); });
      el.done1.addEventListener('click', function () { if (!S.revealed) reopen(1); });
      el.done2.addEventListener('click', function () { if (!S.revealed) reopen(2); });

      /* ---- rendering ---- */

      function newRound() {
        var r = ROUNDS[S.round], f = facts(r);
        S.pick1 = -1; S.pick2 = -1; S.revealed = false;
        S.opts1 = shuffle(countOptions(r), S.round);
        S.opts2 = shuffle(sizeOptions(r), S.round + 1);

        el.frame.textContent = 'An ADC measures this wave’s height ' + fmt(r.rate) +
          ' times a second and stores each reading as ' + art(r.bits) + r.bits + '-bit number, for ' + r.secs +
          ' seconds. Predict how many measurements it keeps, and how big the file is.';
        el.params.textContent = fmt(r.rate) + ' samples/s · ' + r.bits + ' bits · ' +
          r.secs + ' s mono clip — first 6 ms shown';

        for (k = 0; k < 4; k++) {
          btn1[k].textContent = S.opts1[k].label;
          btn2[k].textContent = S.opts2[k].label;
          btn1[k].setAttribute('aria-pressed', 'false');
          btn2[k].setAttribute('aria-pressed', 'false');
          btn1[k].disabled = false;
          btn2[k].disabled = true;
        }
        show(el.step1, true); show(el.opts1, true); show(el.done1, false); el.done1.disabled = true;
        show(el.step2, false); show(el.opts2, true); show(el.done2, false); el.done2.disabled = true;
        show(el.check, true); el.check.disabled = false;
        show(el.next, false); el.next.disabled = true;

        el.caption.textContent = 'The ADC — the analogue-to-digital converter — takes one fresh measurement at every dotted line, about ' +
          tidy(f.spc) + ' per cycle of this wave. Nothing between the lines is stored.';
        runLine();
        draw();
        state();
      }

      function pick(which, idx) {
        if (S.revealed) return;
        if (which === 1) {
          S.pick1 = idx;
          for (k = 0; k < 4; k++) btn1[k].setAttribute('aria-pressed', k === idx ? 'true' : 'false');
          collapse(1);
          show(el.step2, true);
          for (k = 0; k < 4; k++) btn2[k].disabled = false;
          if (S.pick2 < 0) btn2[0].focus();
        } else {
          S.pick2 = idx;
          for (k = 0; k < 4; k++) btn2[k].setAttribute('aria-pressed', k === idx ? 'true' : 'false');
          collapse(2);
          el.check.focus();
        }
        state();
      }

      function collapse(which) {
        var lab = which === 1 ? 'Measurements' : 'File size';
        var txt = which === 1 ? S.opts1[S.pick1].label : S.opts2[S.pick2].label;
        var b = which === 1 ? el.done1 : el.done2;
        var opts = which === 1 ? el.opts1 : el.opts2;
        b.textContent = lab + ': ' + txt + '  ·  change';
        b.setAttribute('aria-label', lab + ' — you chose ' + txt + '. Change it.');
        b.disabled = false;
        show(b, true); show(opts, false);
        for (k = 0; k < 4; k++) (which === 1 ? btn1 : btn2)[k].disabled = true;
      }

      function reopen(which) {
        var b = which === 1 ? el.done1 : el.done2;
        var opts = which === 1 ? el.opts1 : el.opts2;
        show(b, false); b.disabled = true; show(opts, true);
        for (k = 0; k < 4; k++) (which === 1 ? btn1 : btn2)[k].disabled = false;
        (which === 1 ? btn1 : btn2)[0].focus();
        state();
      }

      function commit() {
        if (S.revealed) return;
        if (S.pick1 < 0 || S.pick2 < 0) {
          el.caption.textContent = S.pick1 < 0
            ? 'Both parts first — start with how many measurements the clip keeps.'
            : 'Both parts first — now choose the size of the file.';
          state();
          return;
        }
        var r = ROUNDS[S.round], f = facts(r);
        var a1 = S.opts1[S.pick1], a2 = S.opts2[S.pick2];
        var ok1 = a1.key === 'right', ok2 = a2.key === 'right', ok = ok1 && ok2;

        S.revealed = true;
        S.attempted++;
        S.streak = ok ? S.streak + 1 : 0;
        if (S.streak >= 3) S.mastered = true;

        el.done1.disabled = true; el.done2.disabled = true;
        show(el.step1, false); show(el.step2, false);   /* the answer is echoed in the feedback */
        show(el.check, false);
        show(el.next, true); el.next.disabled = false;
        el.next.textContent = S.mastered ? 'Another anyway' : 'Next wave';

        var countSum = fmt(r.rate) + ' × ' + r.secs + ' = ' + fmt(f.samples) + ' readings';
        var sizeSum = fmt(r.rate) + ' × ' + r.bits + ' × ' + r.secs + ' = ' + fmt(f.totalBits) +
          ' bits ÷ 8 = ' + fmt(f.bytes) + ' bytes = ' + fmt(f.kb) + ' kB';
        var msg;

        if (ok) {
          msg = 'Right — ' + fmt(f.samples) + ' measurements and ' + fmt(f.kb) + ' kB. It measures ' +
            fmt(r.rate) + ' times a second for ' + r.secs + ' s, so ' + countSum + ', and ' + sizeSum +
            '. The dots are all that survive: played back, the wave misses the original by up to ' +
            worstError(r) + '% of its height.';
          if (S.mastered) {
            var cdBytes = CD_RATE * CD_BITS * CD_SECS / 8;
            msg = 'Three in a row — you have it. Sampling is repeated measurement: the ADC keeps rate × seconds separate numbers, each one a fixed number of bits, and whatever the wave did in between is gone for good. That is what 44,100 Hz and 16-bit mean — CD audio measures ' +
              fmt(CD_RATE) + ' times a second at ' + CD_BITS + ' bits, so one minute is ' + fmt(CD_RATE) +
              ' × ' + CD_BITS + ' × 60 ÷ 8 = ' + fmt(cdBytes) + ' bytes per channel, about ' +
              tidy(cdBytes / 1000000) + ' MB.';
          }
        } else if (ok1) {
          msg = 'Not quite — you had the ' + a1.label + ' measurements right, but you said ' + a2.label +
            ' for the file. Size is rate × bit depth × seconds: ' + sizeSum + '. ' + SIZE_WHY[a2.key](r);
        } else if (ok2) {
          msg = 'Not quite — ' + a2.label + ' is the right size, but you said ' + phrase(a1) +
            ' for the measurements. The ADC measures ' + fmt(r.rate) + ' times a second for ' + r.secs +
            ' s, so ' + countSum + '. ' + COUNT_WHY[a1.key](r);
        } else {
          msg = 'Not quite — you said ' + phrase(a1) + ' and ' + a2.label + '. ' + COUNT_WHY[a1.key](r) +
            ' In fact ' + countSum + ', and ' + sizeSum + '. ' + SIZE_WHY[a2.key](r);
        }
        el.caption.textContent = msg;
        runLine();
        draw();
        state();
        el.next.focus();
      }

      function runLine() {
        if (S.mastered) { el.run.textContent = 'You have it'; return; }
        el.run.textContent = S.streak === 0 ? '' :
          S.streak === 1 ? '1 right in a row' : '2 right in a row — one more and you have it';
      }

      function show(node, on) { if (on) node.removeAttribute('hidden'); else node.setAttribute('hidden', ''); }

      function shuffle(arr, seed) {          /* deterministic, so the answer moves about */
        var a = arr.slice(), i, j, t, s = (seed * 2654435761) % 2147483647;
        for (i = a.length - 1; i > 0; i--) {
          s = (s * 1103515245 + 12345) % 2147483647;
          j = Math.abs(s) % (i + 1);
          t = a[i]; a[i] = a[j]; a[j] = t;
        }
        return a;
      }

      /* ---- the stage ---- */

      function draw() {
        var wrap = el.canvas.parentNode;
        var w = Math.max(180, wrap.clientWidth - 14);
        var h = el.canvas.clientHeight || 104;
        var dpr = window.devicePixelRatio || 1;
        el.canvas.width = Math.round(w * dpr);
        el.canvas.height = Math.round(h * dpr);
        el.canvas.style.width = w + 'px';
        g.setTransform(dpr, 0, 0, dpr, 0, 0);
        g.clearRect(0, 0, w, h);

        var r = ROUNDS[S.round], wv = WAVES[r.wave], pts = sampleSet(r);
        var padX = 8, padY = 9;
        var A = (h - padY * 2) / 2;
        var mid = h / 2;
        var X = function (u) { return padX + u * (w - padX * 2); };
        var Y = function (v) { return mid - v * A; };
        var i, u;

        /* quantisation levels, drawn only when they are big enough to see */
        var levels = Math.pow(2, r.bits);
        if (levels <= 16) {
          g.strokeStyle = '#ece5d9'; g.lineWidth = 1;
          for (i = 0; i < levels; i++) {
            var yy = Math.round(Y((i / (levels - 1)) * 2 - 1)) + 0.5;
            g.beginPath(); g.moveTo(padX, yy); g.lineTo(w - padX, yy); g.stroke();
          }
        }

        /* the real, continuous wave */
        var origin = [];
        for (i = 0; i <= 300; i++) { u = i / 300; origin.push([X(u), Y(waveAt(wv, u))]); }

        if (S.revealed) {
          /* what was lost: between the real wave and the joined-up samples */
          g.beginPath();
          g.moveTo(origin[0][0], origin[0][1]);
          for (i = 1; i < origin.length; i++) g.lineTo(origin[i][0], origin[i][1]);
          for (i = 300; i >= 0; i--) { u = i / 300; g.lineTo(X(u), Y(reconstructAt(pts, u))); }
          g.closePath();
          g.fillStyle = hexA(accent, 0.26);
          g.fill();
        }

        g.lineJoin = 'round'; g.lineCap = 'round';
        g.strokeStyle = S.revealed ? '#c9c2b6' : '#2d2a26';
        g.lineWidth = S.revealed ? 1.2 : 1.7;
        g.beginPath();
        g.moveTo(origin[0][0], origin[0][1]);
        for (i = 1; i < origin.length; i++) g.lineTo(origin[i][0], origin[i][1]);
        g.stroke();

        /* the measuring instants */
        g.strokeStyle = '#ddd5c8'; g.lineWidth = 1;
        if (g.setLineDash) g.setLineDash([2, 3]);
        for (i = 0; i < pts.length; i++) {
          var px = Math.round(X(pts[i].u)) + 0.5;
          g.beginPath(); g.moveTo(px, padY - 3); g.lineTo(px, h - padY + 3); g.stroke();
        }
        if (g.setLineDash) g.setLineDash([]);

        /* the reconstruction, computed from the stored points */
        if (S.revealed) {
          g.strokeStyle = '#2d2a26'; g.lineWidth = 1.9;
          g.beginPath();
          g.moveTo(X(pts[0].u), Y(pts[0].v));
          for (i = 1; i < pts.length; i++) g.lineTo(X(pts[i].u), Y(pts[i].v));
          g.stroke();
        }

        /* the measured points themselves */
        for (i = 0; i < pts.length; i++) {
          g.beginPath();
          g.arc(X(pts[i].u), Y(pts[i].v), 3.2, 0, Math.PI * 2);
          g.fillStyle = accent; g.fill();
          g.lineWidth = 1.5; g.strokeStyle = '#fff'; g.stroke();
        }

        el.canvas.setAttribute('aria-label',
          'A sound wave with ' + pts.length + ' measured points marked on it, ' +
          (S.revealed ? 'and the wave rebuilt by joining those points up.' : 'one at each measuring instant.'));
      }

      function hexA(hex, a) {
        var m = /^#?([0-9a-f]{6})$/i.exec(hex.trim());
        if (!m) return 'rgba(79,125,99,' + a + ')';
        var n = parseInt(m[1], 16);
        return 'rgba(' + ((n >> 16) & 255) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',' + a + ')';
      }

      function sr() {
        el.sr.textContent = el.caption.textContent + ' ' + (el.canvas.getAttribute('aria-label') || '');
      }

      function state() {
        var r = ROUNDS[S.round], f = facts(r);
        sr();
        root.dataset.svState = JSON.stringify({
          streak: S.streak, mastered: S.mastered, attempted: S.attempted,
          round: S.round, rate: r.rate, bits: r.bits, seconds: r.secs,
          samples: f.samples, sizeKb: f.kb,
          answered: (S.pick1 >= 0 ? 1 : 0) + (S.pick2 >= 0 ? 1 : 0),
          revealed: S.revealed,
          correct: S.revealed ? (S.opts1[S.pick1].key === 'right' && S.opts2[S.pick2].key === 'right') : null
        });
      }

      /* layout follows the container, not the viewport: the modal is narrower than the page */
      var wide = null;
      function layout() {
        var w = root.getBoundingClientRect().width;
        var next = w >= 470;
        if (next !== wide) { wide = next; root.classList.toggle('svw-samp--wide', next); }
        draw();
      }

      var ro = null;
      if (window.ResizeObserver) {
        ro = new ResizeObserver(function () { layout(); });
        ro.observe(root);
      } else {
        window.addEventListener('resize', layout);
      }

      layout();
      newRound();
      return function () { if (ro) ro.disconnect(); else window.removeEventListener('resize', draw); };
    }
  };

  /* ---------------- scoped styles ---------------- */

  var CSS = [
    '.svw-samp{box-sizing:border-box;background:#fff;border:1px solid #e8e3db;border-radius:16px;',
    'padding:1rem 1rem .85rem;color:#2d2a26;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;',
    'font-size:16px;line-height:1.4;max-width:100%;}',
    '.svw-samp *{box-sizing:border-box;}',
    '.svw-samp__kicker{margin:0 0 .15rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;',
    'text-transform:uppercase;color:var(--svw-a);}',
    '.svw-samp__title{margin:0 0 .3rem;font-family:"Source Serif 4",Georgia,serif;font-size:1.22rem;',
    'font-weight:600;line-height:1.18;}',
    '.svw-samp__frame{margin:0 0 .55rem;font-size:.84rem;line-height:1.45;color:#3c3833;}',
    '.svw-samp__stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.35rem .45rem .3rem;margin:0 0 .55rem;}',
    '.svw-samp__canvas{display:block;width:100%;height:100px;}',
    '.svw-samp__params{margin:.2rem 0 0;font-size:.72rem;line-height:1.3;color:#8d8880;font-variant-numeric:tabular-nums;}',
    '.svw-samp__step{margin:0 0 .45rem;}',
    '.svw-samp__lab{margin:0 0 .3rem;font-size:.78rem;font-weight:600;color:#2d2a26;}',
    '.svw-samp__num{display:inline-block;min-width:1.15em;margin-right:.3rem;padding:0 .3em;border-radius:5px;',
    'background:var(--svw-a);color:#fff;font-size:.68rem;text-align:center;}',
    '.svw-samp__opts{display:grid;grid-template-columns:1fr 1fr;gap:.35rem;}',
    '.svw-samp__opts[hidden]{display:none;}',
    '.svw-samp__opt,.svw-samp__done,.svw-samp__primary,.svw-samp__ghost{font-family:inherit;cursor:pointer;}',
    '.svw-samp__opt{padding:.42rem .3rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;',
    'color:#2d2a26;font-size:.8rem;font-weight:600;font-variant-numeric:tabular-nums;}',
    '.svw-samp__opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
    '.svw-samp__opt:disabled{cursor:default;opacity:1;}',
    '.svw-samp__done{display:inline-block;max-width:100%;text-align:left;padding:.35rem .6rem;border:1px dashed #ddd7cd;',
    'border-radius:10px;background:#fff;color:#5b564e;font-size:.78rem;font-weight:600;font-variant-numeric:tabular-nums;}',
    '.svw-samp__done:disabled{cursor:default;}',
    '.svw-samp__done[hidden],.svw-samp__step[hidden]{display:none;}',
    '.svw-samp__actions{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;margin:.15rem 0 .5rem;}',
    '.svw-samp__primary{padding:.45rem .95rem;border:1px solid #2d2a26;border-radius:10px;background:#2d2a26;',
    'color:#fff;font-size:.82rem;font-weight:600;}',
    '.svw-samp__ghost{padding:.45rem .95rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;',
    'color:#2d2a26;font-size:.82rem;font-weight:600;}',
    '.svw-samp__run{font-size:.74rem;color:#8d8880;}',
    '.svw-samp__caption{margin:0;font-size:.84rem;line-height:1.5;color:#3c3833;min-height:3.3em;}',
    '.svw-samp__sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;',
    'clip:rect(0 0 0 0);white-space:nowrap;border:0;}',
    '.svw-samp__opt:focus-visible,.svw-samp__done:focus-visible,.svw-samp__primary:focus-visible,',
    '.svw-samp__ghost:focus-visible{outline:2px solid var(--svw-a);outline-offset:2px;}',
    '.svw-samp--wide{padding:1.35rem 1.35rem 1.1rem;}',
    '.svw-samp--wide .svw-samp__canvas{height:128px;}',
    '.svw-samp--wide .svw-samp__opts{grid-template-columns:repeat(4,1fr);}',
    '.svw-samp--wide .svw-samp__caption{min-height:3em;}'
  ].join('');
})();
