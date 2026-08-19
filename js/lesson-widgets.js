/* ============================================
   Lesson widgets — pilot (branch: lesson-widgets)

   Three hand-built interactive teaching components, injected at render
   time into three live lessons. The Supabase content is untouched: this
   file owns a map of lesson id -> widget + anchor, and inserts the
   widget after the section that teaches the concept. Built once,
   verified once, instantiated with data — the annotated-player model,
   not per-lesson generated code (the Gemini-diagram lesson).

   Physics correctness notes are inline with each model. Terminology
   mirrors each lesson's own prose (flashy hydrograph, rising limb,
   v = f lambda, pass/swap) so the widget and the text teach in the
   same voice.
   ============================================ */
(function () {
  'use strict';

  var REDUCED = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- shared scaffolding ---------- */

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function widgetShell(title) {
    var root = el('div', 'sv-widget');
    root.appendChild(el('div', 'svw-kicker', 'Interactive'));
    root.appendChild(el('h3', 'svw-title', title));
    var controls = el('div', 'svw-controls');
    var wrap = el('div', 'svw-canvaswrap');
    var canvas = document.createElement('canvas');
    wrap.appendChild(canvas);
    var stats = el('div', 'svw-stats');
    var caption = el('div', 'svw-caption');
    root.appendChild(controls);
    root.appendChild(wrap);
    root.appendChild(stats);
    root.appendChild(caption);
    return { root: root, controls: controls, canvas: canvas, stats: stats, caption: caption };
  }

  function slider(labelText, min, max, step, value, endLeft, endRight) {
    var f = el('div', 'svw-field');
    var lab = el('label', null, labelText);
    var input = document.createElement('input');
    input.type = 'range'; input.min = min; input.max = max; input.step = step; input.value = value;
    f.appendChild(lab); f.appendChild(input);
    if (endLeft) {
      f.appendChild(el('div', 'svw-ends', '<span>' + endLeft + '</span><span>' + endRight + '</span>'));
    }
    return { field: f, input: input };
  }

  function seg(options, onPick) {
    var s = el('div', 'svw-seg');
    var btns = options.map(function (o, i) {
      var b = el('button', i === 0 ? 'on' : '', o);
      b.addEventListener('click', function () {
        btns.forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on');
        onPick(i);
      });
      s.appendChild(b);
      return b;
    });
    return s;
  }

  function stat(label) {
    var s = el('div', 'svw-stat', label + ' <b>—</b>');
    return { el: s, set: function (v) { s.querySelector('b').textContent = v; } };
  }

  /* HiDPI canvas sized to its container; returns a ctx getter + redraw hook */
  function fitCanvas(canvas, height, redraw) {
    function resize() {
      var w = canvas.parentElement.clientWidth - 8;
      if (w < 50) return;
      var dpr = window.devicePixelRatio || 1;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(height * dpr);
      canvas.style.height = height + 'px';
      var ctx = canvas.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      redraw();
    }
    if (window.ResizeObserver) new ResizeObserver(resize).observe(canvas.parentElement);
    setTimeout(resize, 0);
    return resize;
  }

  var INK = '#2d2a26', MUT = '#8d8880', GRID = '#e8e2d9';

  /* Canvas can't use CSS variables, so read the accent at draw time —
     FROM THE WIDGET ITSELF, not documentElement. Two layers set --accent
     and they disagree: lesson-loader.js writes the unit's DB colour onto
     documentElement, while style.css sets one on body.unit-*, which is
     closer and therefore wins for everything a student sees. Resolving
     against the widget guarantees the canvas matches its own card
     whichever layer won. (The DB/CSS disagreement is a pre-existing site
     inconsistency — geography paper-1 is indigo in the DB, green in the
     CSS — worth reconciling separately.) */
  function accOf(node) {
    var v = getComputedStyle(node || document.documentElement)
      .getPropertyValue('--accent').trim();
    return v || '#8a6a4f';
  }
  /* a soft tint of the accent for secondary fills (bars, runs) */
  function accTintOf(node, alpha) {
    var c = accOf(node);
    if (c.charAt(0) === '#' && c.length === 7) {
      return 'rgba(' + parseInt(c.substr(1, 2), 16) + ',' +
        parseInt(c.substr(3, 2), 16) + ',' + parseInt(c.substr(5, 2), 16) +
        ',' + alpha + ')';
    }
    return 'rgba(138,106,79,' + alpha + ')';
  }

  /* ================= 1. WAVES (physics) =================
     Model: a wave on a rope with FIXED wave speed v = 6 m/s (speed is a
     property of the medium). y(x,t) = A sin(2pi (x/lambda - f t)), with
     lambda = v / f — so turning frequency up visibly shortens the
     wavelength while the equation v = f x lambda stays balanced. */
  function buildWaves() {
    var V = 6; // m/s, fixed by the "medium"
    var state = { f: 1.0, ampPct: 60, mode: 0, playing: !REDUCED, t: 0 };
    var ui = widgetShell('Make a wave: frequency, wavelength and amplitude');

    var modeSeg = seg(['Transverse', 'Longitudinal'], function (i) { state.mode = i; draw(); });
    var segField = el('div', 'svw-field svw-field--fixed'); segField.appendChild(el('label', null, 'Wave type')); segField.appendChild(modeSeg);
    var fS = slider('Frequency', 0.5, 3, 0.1, state.f, '0.5 Hz', '3 Hz');
    var aS = slider('Amplitude', 20, 90, 1, state.ampPct, 'small', 'large');
    var play = el('button', 'svw-btn primary', REDUCED ? 'Play' : 'Pause');
    var playField = el('div', 'svw-field svw-field--fixed'); playField.appendChild(el('label', null, '&nbsp;')); playField.appendChild(play);
    ui.controls.appendChild(segField);
    ui.controls.appendChild(fS.field);
    ui.controls.appendChild(aS.field);
    ui.controls.appendChild(playField);

    var stLambda = stat('Wavelength λ'), stT = stat('Period T'), stV = stat('Wave speed v');
    ui.stats.appendChild(stLambda.el); ui.stats.appendChild(stT.el); ui.stats.appendChild(stV.el);
    stV.set(V + ' m/s (fixed)');

    var H = 240;
    function draw() {
      var ctx = ui.canvas.getContext('2d');
      var w = ui.canvas.clientWidth || (ui.canvas.width / (window.devicePixelRatio || 1));
      ctx.clearRect(0, 0, w, H);
      var metres = 10;                      // canvas shows 10 m of rope
      var px = w / metres;
      var lambda = V / state.f;             // physics: lambda = v / f
      var mid = H / 2;
      var A = (state.ampPct / 100) * (H / 2 - 34);

      // rest position
      ctx.strokeStyle = GRID; ctx.setLineDash([5, 5]);
      ctx.beginPath(); ctx.moveTo(0, mid); ctx.lineTo(w, mid); ctx.stroke();
      ctx.setLineDash([]);

      if (state.mode === 0) {
        // transverse sine, moving right
        ctx.strokeStyle = accOf(ui.root); ctx.lineWidth = 2.5;
        ctx.beginPath();
        for (var x = 0; x <= w; x += 2) {
          var m = x / px;
          var y = mid - A * Math.sin(2 * Math.PI * (m / lambda - state.f * state.t));
          x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.stroke();
        // crest-to-crest wavelength bracket: first crest at phase pi/2
        var phase0 = (0.25 + state.f * state.t) * lambda; // metres of first crest >= 0
        var c1 = ((phase0 % lambda) + lambda) % lambda;
        if (c1 + lambda < metres) {
          var bx1 = c1 * px, bx2 = (c1 + lambda) * px, by = mid - A - 12;
          ctx.strokeStyle = INK; ctx.lineWidth = 1.2;
          ctx.beginPath();
          ctx.moveTo(bx1, by); ctx.lineTo(bx2, by);
          ctx.moveTo(bx1, by - 4); ctx.lineTo(bx1, by + 4);
          ctx.moveTo(bx2, by - 4); ctx.lineTo(bx2, by + 4);
          ctx.stroke();
          ctx.fillStyle = INK; ctx.font = '600 12px Inter, sans-serif'; ctx.textAlign = 'center';
          ctx.fillText('wavelength λ', (bx1 + bx2) / 2, by - 8);
        }
        // amplitude arrow at a crest
        var ax = (c1 % metres) * px;
        ctx.strokeStyle = MUT;
        ctx.beginPath(); ctx.moveTo(ax, mid); ctx.lineTo(ax, mid - A); ctx.stroke();
        ctx.fillStyle = MUT; ctx.font = '12px Inter, sans-serif'; ctx.textAlign = 'left';
        ctx.fillText('amplitude', ax + 6, mid - A / 2);
      } else {
        // longitudinal: particles displaced along the direction of travel
        var n = Math.floor(w / 9);
        var maxDense = -1, maxX = 0, minDense = 2, minX = 0;
        for (var i = 0; i < n; i++) {
          var xm = (i / n) * metres;
          var disp = (state.ampPct / 100) * 0.42 * (lambda / 4) *
                     Math.sin(2 * Math.PI * (xm / lambda - state.f * state.t));
          var xpx = (xm + disp) * px;
          ctx.strokeStyle = accOf(ui.root); ctx.lineWidth = 2;
          ctx.beginPath(); ctx.moveTo(xpx, mid - 46); ctx.lineTo(xpx, mid + 46); ctx.stroke();
          // local density ~ -d(disp)/dx: cos term
          var dens = -Math.cos(2 * Math.PI * (xm / lambda - state.f * state.t));
          if (dens > maxDense) { maxDense = dens; maxX = xpx; }
          if (dens < minDense) { minDense = dens; minX = xpx; }
        }
        ctx.fillStyle = INK; ctx.font = '600 12px Inter, sans-serif'; ctx.textAlign = 'center';
        ctx.fillText('compression', maxX, mid - 58);
        ctx.fillStyle = MUT;
        ctx.fillText('rarefaction', minX, mid + 70);
      }
    }

    /* rAF runs ONLY while playing — a paused widget costs nothing */
    function loop() {
      if (!state.playing) return;
      state.t += 1 / 60; draw();
      state.raf = requestAnimationFrame(loop);
    }
    play.addEventListener('click', function () {
      state.playing = !state.playing;
      play.textContent = state.playing ? 'Pause' : 'Play';
      if (state.playing) loop(); else cancelAnimationFrame(state.raf);
    });
    function sync() {
      state.f = parseFloat(fS.input.value);
      state.ampPct = parseFloat(aS.input.value);
      var lambda = V / state.f;
      stLambda.set(lambda.toFixed(1) + ' m');
      stT.set((1 / state.f).toFixed(2) + ' s');
      ui.caption.innerHTML = 'Turn <b>frequency</b> up and the <b>wavelength shrinks</b> — the ' +
        'wave speed is set by the rope, so <b>v = f×λ</b> stays at ' + V + ' m/s ' +
        '(' + state.f.toFixed(1) + ' Hz × ' + lambda.toFixed(1) + ' m). ' +
        'Amplitude changes the <b>energy</b> the wave carries — not its speed.';
      draw();
    }
    fS.input.addEventListener('input', sync);
    aS.input.addEventListener('input', sync);
    fitCanvas(ui.canvas, 240, draw);
    sync();
    if (state.playing) loop();
    return ui.root;
  }

  /* ================= 2. HYDROGRAPH (geography) =================
     Same storm, different drainage basin. The three factors the lesson
     teaches (relief, geology, urbanisation) all push the same way:
     more runoff -> shorter lag time, higher peak, steeper rising limb.
     The response curve is an asymmetric pulse (falling limb gentler
     than rising, as on every exam hydrograph). Numbers are indicative,
     not from a real gauging station. */
  function buildHydro() {
    var ui = widgetShell('Build a storm hydrograph: same rain, different basin');
    var rS = slider('Relief', 0, 100, 1, 30, 'flat', 'steep');
    var gS = slider('Geology', 0, 100, 1, 30, 'permeable (chalk)', 'impermeable (clay)');
    var uS = slider('Land use', 0, 100, 1, 20, 'rural', 'built-up');
    ui.controls.appendChild(rS.field); ui.controls.appendChild(gS.field); ui.controls.appendChild(uS.field);
    var stLag = stat('Lag time'), stPeak = stat('Peak discharge');
    ui.stats.appendChild(stLag.el); ui.stats.appendChild(stPeak.el);

    var RAIN = [3, 8, 13, 10, 5, 2];   // mm per hour, fixed storm, peak at hour 2
    var H = 260, HOURS = 40;

    function model() {
      var s = 0.35 * (rS.input.value / 100) + 0.35 * (gS.input.value / 100) + 0.30 * (uS.input.value / 100);
      var lag = 16 - 13 * s;              // hours from peak rain to peak discharge
      var peak = 8 + 42 * s;              // m3/s
      return { s: s, lag: lag, peak: peak };
    }
    function discharge(t, m) {
      var tp = 2.5 + m.lag;               // peak rain lands mid hour 2
      var rise = m.lag * 0.42, fall = rise * 2.3;
      var d = t < tp ? Math.exp(-Math.pow(t - tp, 2) / (2 * rise * rise))
                     : Math.exp(-Math.pow(t - tp, 2) / (2 * fall * fall));
      return 3 + (m.peak - 3) * d;        // 3 m3/s baseflow
    }

    function draw() {
      var ctx = ui.canvas.getContext('2d');
      var w = ui.canvas.clientWidth || 600;
      ctx.clearRect(0, 0, w, H);
      var m = model();
      var L = 44, R = 14, T = 12, B = 34;
      var pw = w - L - R, ph = H - T - B;
      var xOf = function (t) { return L + (t / HOURS) * pw; };
      var maxQ = 56;
      var yOf = function (q) { return T + ph - (q / maxQ) * ph; };

      // axes
      ctx.strokeStyle = GRID; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(L, T); ctx.lineTo(L, T + ph); ctx.lineTo(L + pw, T + ph); ctx.stroke();
      ctx.fillStyle = MUT; ctx.font = '11px Inter, sans-serif'; ctx.textAlign = 'center';
      for (var h = 0; h <= HOURS; h += 8) ctx.fillText(h + 'h', xOf(h), H - 16);
      ctx.fillText('time after storm begins', L + pw / 2, H - 3);
      ctx.save(); ctx.translate(11, T + ph / 2); ctx.rotate(-Math.PI / 2);
      ctx.fillText('discharge (m³/s)  ·  rainfall', 0, 0); ctx.restore();

      // rainfall bars
      ctx.fillStyle = accTintOf(ui.root, 0.22);
      RAIN.forEach(function (mm, i) {
        var bh = (mm / 14) * (ph * 0.42);
        ctx.fillRect(xOf(i) + 1, T + ph - bh, (pw / HOURS) - 2, bh);
      });

      // discharge curve
      ctx.strokeStyle = accOf(ui.root); ctx.lineWidth = 2.5;
      ctx.beginPath();
      for (var t = 0; t <= HOURS; t += 0.25) {
        var y = yOf(discharge(t, m));
        t === 0 ? ctx.moveTo(xOf(t), y) : ctx.lineTo(xOf(t), y);
      }
      ctx.stroke();

      // lag time annotation: peak rain (hour 2.5) to peak discharge
      var tPeakQ = 2.5 + m.lag;
      var yAnno = yOf(m.peak) - 8 < T + 12 ? T + 12 : yOf(m.peak) - 8;
      ctx.strokeStyle = INK; ctx.setLineDash([4, 4]); ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(xOf(2.5), T + ph); ctx.moveTo(xOf(2.5), yAnno); ctx.lineTo(xOf(tPeakQ), yAnno);
      ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = INK; ctx.font = '600 12px Inter, sans-serif'; ctx.textAlign = 'center';
      ctx.fillText('lag time ' + m.lag.toFixed(0) + 'h', xOf(2.5 + (tPeakQ - 2.5) / 2), yAnno - 6);

      // limb labels
      ctx.fillStyle = MUT; ctx.font = '12px Inter, sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText('rising limb', xOf(tPeakQ) - 8, yOf(m.peak * 0.6));
      ctx.textAlign = 'left';
      ctx.fillText('falling limb', xOf(tPeakQ + m.lag * 1.1), yOf(m.peak * 0.55));
    }

    function sync() {
      var m = model();
      stLag.set(m.lag.toFixed(0) + ' hours');
      stPeak.set(m.peak.toFixed(0) + ' m³/s');
      ui.caption.innerHTML =
        m.s > 0.62 ? 'Short lag time, steep rising limb, high peak — a <b>flashy hydrograph</b>. ' +
                     'Water is racing over steep, impermeable, built-up ground straight into the river. <b>High flood risk.</b>'
        : m.s < 0.35 ? 'Long lag time, gentle limbs, low peak — rain is <b>soaking into permeable ground</b> ' +
                       'and arriving slowly. Much lower flood risk.'
        : 'Somewhere in between — drag each slider to its extreme and watch which one changes the ' +
          '<b>lag time</b> and <b>peak discharge</b> most.';
      draw();
    }
    [rS, gS, uS].forEach(function (s) { s.input.addEventListener('input', sync); });
    fitCanvas(ui.canvas, H, draw);
    sync();
    return ui.root;
  }

  /* ================= 3. SORTING (computer science) =================
     Steps are precomputed by running the real algorithm, then replayed
     one comparison/move at a time — the widget can't drift from the
     algorithm because the algorithm generates the script. */
  function buildSort() {
    var ui = widgetShell('Watch the three sorts race: every comparison, every swap');
    var state = { alg: 0, vals: [], steps: [], pos: 0, playing: false, timer: null };

    var algSeg = seg(['Bubble', 'Insertion', 'Merge'], function (i) { state.alg = i; rebuild(); });
    var segField = el('div', 'svw-field svw-field--fixed'); segField.appendChild(el('label', null, 'Algorithm')); segField.appendChild(algSeg);
    var stepBtn = el('button', 'svw-btn primary', 'Step');
    var playBtn = el('button', 'svw-btn', 'Play');
    var shufBtn = el('button', 'svw-btn', 'Shuffle');
    var bField = el('div', 'svw-field svw-field--fixed'); bField.appendChild(el('label', null, '&nbsp;'));
    var bRow = el('div', null); bRow.style.display = 'flex'; bRow.style.gap = '.5rem';
    bRow.appendChild(stepBtn); bRow.appendChild(playBtn); bRow.appendChild(shufBtn);
    bField.appendChild(bRow);
    ui.controls.appendChild(segField); ui.controls.appendChild(bField);

    var stCmp = stat('Comparisons'), stMov = stat('Swaps / moves');
    ui.stats.appendChild(stCmp.el); ui.stats.appendChild(stMov.el);

    function shuffled() {
      var a = [2, 3, 4, 5, 6, 7, 8, 9];
      for (var i = a.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
      }
      return a;
    }

    /* run the real algorithm, recording steps */
    function script(alg, start) {
      var a = start.slice(), steps = [];
      if (alg === 0) { // bubble — repeated passes, swap adjacent pairs
        var passN = 0, swapped = true;
        while (swapped) {
          swapped = false; passN++;
          for (var i = 0; i < a.length - passN; i++) {
            steps.push({ type: 'cmp', i: i, j: i + 1, a: a.slice(),
              cap: 'Pass ' + passN + ': compare <b>' + a[i] + '</b> and <b>' + a[i + 1] + '</b>' +
                   (a[i] > a[i + 1] ? ' — wrong order, swap.' : ' — already in order.') });
            if (a[i] > a[i + 1]) {
              var t = a[i]; a[i] = a[i + 1]; a[i + 1] = t; swapped = true;
              steps.push({ type: 'swap', i: i, j: i + 1, a: a.slice(), cap: 'Swapped. The bigger value bubbles right.' });
            }
          }
        }
        steps.push({ type: 'done', a: a.slice(), cap: 'A full pass with <b>no swaps</b> — the list is sorted, so bubble sort stops.' });
      } else if (alg === 1) { // insertion — grow a sorted left-hand side
        /* The lifted value is HELD (hold) and its slot shown as a GAP, the
           way every exam diagram draws it — not as a duplicated bar. The
           comparison that ENDS a run counts too: a student comparing
           algorithms by comparison count must see the real total. */
        for (var k = 1; k < a.length; k++) {
          var v = a[k], j2 = k - 1, moved = false;
          steps.push({ type: 'pick', i: k, hold: v, gap: k, a: a.slice(),
            cap: 'Lift the next unsorted value, <b>' + v + '</b>, out of the list.' });
          while (j2 >= 0) {
            steps.push({ type: 'cmp', i: j2, j: j2 + 1, hold: v, gap: j2 + 1, a: a.slice(),
              cap: a[j2] > v
                ? '<b>' + a[j2] + '</b> &gt; ' + v + ' — shift it one place right.'
                : '<b>' + a[j2] + '</b> &le; ' + v + ' — stop here, this is where ' + v + ' belongs.' });
            if (a[j2] <= v) break;
            a[j2 + 1] = a[j2]; j2--; moved = true;
            steps.push({ type: 'shift', i: j2 + 1, hold: v, gap: j2 + 1, a: a.slice(), cap: 'Shifted right.' });
          }
          a[j2 + 1] = v;
          steps.push({ type: 'ins', i: j2 + 1, a: a.slice(),
            cap: moved ? 'Drop <b>' + v + '</b> into the gap — everything left of it is sorted.'
                       : '<b>' + v + '</b> was already in the right place.' });
        }
        steps.push({ type: 'done', a: a.slice(), cap: 'Every value inserted — the list is sorted.' });
      } else { // merge — bottom-up: merge runs of 1, then 2, then 4
        var width = 1;
        while (width < a.length) {
          for (var lo = 0; lo < a.length; lo += width * 2) {
            var midX = Math.min(lo + width, a.length), hi = Math.min(lo + width * 2, a.length);
            var left = a.slice(lo, midX), right = a.slice(midX, hi), out = [], li = 0, ri = 0;
            if (!right.length) continue;
            steps.push({ type: 'runs', lo: lo, mid: midX, hi: hi, a: a.slice(),
              cap: 'Merge the sorted lists [' + left.join(' ') + '] and [' + right.join(' ') + '].' });
            while (li < left.length && ri < right.length) {
              steps.push({ type: 'cmp', i: lo + li, j: midX + ri, a: a.slice(),
                cap: 'Compare the front of each list: <b>' + left[li] + '</b> vs <b>' + right[ri] + '</b> — take the smaller.' });
              out.push(left[li] <= right[ri] ? left[li++] : right[ri++]);
            }
            while (li < left.length) out.push(left[li++]);
            while (ri < right.length) out.push(right[ri++]);
            for (var w2 = 0; w2 < out.length; w2++) a[lo + w2] = out[w2];
            steps.push({ type: 'wrote', lo: lo, hi: hi, a: a.slice(),
              cap: 'Merged into [' + out.join(' ') + '].' });
          }
          width *= 2;
        }
        steps.push({ type: 'done', a: a.slice(), cap: 'All runs merged — the list is sorted. Merge sort does this reliably fast, even on big lists.' });
      }
      return steps;
    }

    var H = 210;
    function draw() {
      var ctx = ui.canvas.getContext('2d');
      var w = ui.canvas.clientWidth || 600;
      ctx.clearRect(0, 0, w, H);
      var s = state.steps[state.pos] || { a: state.vals };
      var a = s.a;
      var n = a.length, gap = 10, bw = (w - gap * (n + 1)) / n;
      var scale = function (v) { return (v / 9) * (H - 62); };
      for (var i = 0; i < n; i++) {
        var x = gap + i * (bw + gap);
        var bh = scale(a[i]);
        /* the slot the held value came out of renders EMPTY (dashed) —
           insertion sort's gap, not a duplicated bar */
        if (s.gap === i) {
          ctx.strokeStyle = '#c9c1b4'; ctx.lineWidth = 1.4; ctx.setLineDash([4, 4]);
          ctx.beginPath(); ctx.roundRect(x, H - 28 - scale(s.hold), bw, scale(s.hold), 6);
          ctx.stroke(); ctx.setLineDash([]);
          continue;
        }
        var hot = (s.type === 'cmp' && (i === s.i || i === s.j)) ||
                  (s.type === 'swap' && (i === s.i || i === s.j)) ||
                  ((s.type === 'ins' || s.type === 'shift' || s.type === 'pick') && i === s.i);
        var inRun = s.type === 'runs' && i >= s.lo && i < s.hi;
        ctx.fillStyle = s.type === 'done' ? '#4f7d63' : hot ? accOf(ui.root)
          : inRun ? accTintOf(ui.root, 0.34) : '#d8d0c3';
        ctx.beginPath();
        ctx.roundRect(x, H - 28 - bh, bw, bh, 6);
        ctx.fill();
        ctx.fillStyle = INK; ctx.font = '600 13px Inter, sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(a[i], x + bw / 2, H - 10);
      }
      // the value currently "in the hand", floating above its gap
      if (s.gap != null && s.hold != null) {
        var hx = gap + s.gap * (bw + gap);
        ctx.fillStyle = accOf(ui.root);
        ctx.beginPath(); ctx.roundRect(hx, 4, bw, 24, 6); ctx.fill();
        ctx.fillStyle = '#fff'; ctx.font = '700 13px Inter, sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(s.hold, hx + bw / 2, 21);
      }
    }

    function counts() {
      var c = 0, mv = 0;
      for (var i = 0; i <= state.pos && i < state.steps.length; i++) {
        var t = state.steps[i].type;
        if (t === 'cmp') c++;
        if (t === 'swap' || t === 'shift' || t === 'ins' || t === 'wrote') mv++;
      }
      stCmp.set(c); stMov.set(mv);
    }

    /* the bars live on a canvas, which is invisible to a screen reader —
       mirror the list as live text so the widget is followable without
       sight (and so its state is inspectable) */
    var sr = el('p', 'svw-sr');
    sr.setAttribute('aria-live', 'polite');
    ui.root.appendChild(sr);

    function show() {
      var s = state.steps[state.pos];
      ui.caption.innerHTML = s ? s.cap : '';
      if (s) {
        var shown = s.a.slice();
        if (s.gap != null) shown[s.gap] = 'gap';
        sr.textContent = 'List: ' + shown.join(', ') + '.' +
          (s.hold != null ? ' Holding ' + s.hold + '.' : '');
      }
      counts(); draw();
    }
    function step() {
      if (state.pos < state.steps.length - 1) { state.pos++; show(); }
      else stopPlay();
    }
    function stopPlay() {
      state.playing = false; playBtn.textContent = 'Play';
      if (state.timer) { clearInterval(state.timer); state.timer = null; }
    }
    function rebuild(fresh) {
      stopPlay();
      if (fresh || !state.vals.length) state.vals = shuffled();
      state.steps = [{ type: 'start', a: state.vals.slice(),
        cap: 'An unordered list. Press <b>Step</b> to watch every comparison, or <b>Play</b> to run it.' }]
        .concat(script(state.alg, state.vals));
      state.pos = 0; show();
    }
    stepBtn.addEventListener('click', step);
    playBtn.addEventListener('click', function () {
      if (state.playing) { stopPlay(); return; }
      if (state.pos >= state.steps.length - 1) state.pos = 0;
      state.playing = true; playBtn.textContent = 'Pause';
      state.timer = setInterval(step, REDUCED ? 1100 : 650);
    });
    shufBtn.addEventListener('click', function () { rebuild(true); });
    fitCanvas(ui.canvas, H, draw);
    rebuild(true);
    return ui.root;
  }

  /* ---------- injection map: /lesson/ URL -> widget + anchor ---------- */
  var MAP = {
    'science-aqa/physics-paper-2/6':
      { build: buildWaves, beforeHeading: 'Reflection, Refraction and Absorption' },
    'geography-aqa/paper-1/19':
      { build: buildHydro, beforeHeading: 'Physical Factors That Increase Flood Risk' },
    'computer-science/computational-thinking/4':
      { build: buildSort, beforeHeading: 'Comparing the algorithms' }
  };

  function inject() {
    var m = location.pathname.match(/\/lesson\/([^/]+)\/([^/]+)\/(\d+)/);
    var cfg = m && MAP[m[1] + '/' + m[2] + '/' + m[3]];
    if (!cfg || document.querySelector('.sv-widget')) return;
    var heads = document.querySelectorAll('#lesson-content h2, #lesson-content h3, .lesson-content h2, .lesson-content h3, article h2, article h3');
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].textContent.trim().indexOf(cfg.beforeHeading) === 0) {
        heads[i].parentNode.insertBefore(cfg.build(), heads[i]);
        return;
      }
    }
  }

  /* the loader injects content then calls window.initLessonFeatures —
     ride that hook so we run exactly once, after the prose exists */
  var orig = null;
  function arm() {
    if (typeof window.initLessonFeatures === 'function' && !window.initLessonFeatures.__svw) {
      orig = window.initLessonFeatures;
      window.initLessonFeatures = function () {
        var r = orig.apply(this, arguments);
        try { inject(); } catch (e) {}
        return r;
      };
      window.initLessonFeatures.__svw = true;
    }
  }
  arm();
  document.addEventListener('DOMContentLoaded', arm);

  /* review harness hook (widgets-test.html) — inert on lesson pages */
  window.__svWidgets = { waves: buildWaves, hydro: buildHydro, sort: buildSort };
})();
