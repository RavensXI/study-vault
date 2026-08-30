/* Negative feedback as a continuous, oscillating cycle.
 *
 * The student is dropped part-way through a real control story (glucose after
 * a meal, core temperature after a run, blood water content after a salty
 * meal) and must predict what happens NEXT: which response is acting, which
 * way the level moves, and what happens once it crosses the set point.
 *
 * Everything the widget draws, marks and says comes from ONE simulation:
 *
 *     effort  +=  -k * deviation      correction is proportional to deviation
 *     effort  *=  damp                what is already acting keeps acting
 *     level   +=  effort + load       cells keep using glucose, heat keeps leaking
 *
 * so the correction always carries the level a little past the set point, the
 * deviation flips sides, the opposite response starts, and the level swings
 * gently either side instead of stopping on the line.
 */
(function () {
  'use strict';

  /* ---------------------------------------------------------------- model */

  var K = 0.0625;      /* how hard the response works per unit of deviation */
  var DAMP = 0.84;     /* the response already acting does not stop at once */
  var LOAD = 0.006;    /* continuous background load - the level is never still */
  var STEPS = 62;      /* samples of "next" that fit on the graph */
  var PAST = 22;       /* samples of the story so far */

  function lcg(seed) {
    var s = seed >>> 0;
    return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  }

  /* Normalised: the level starts exactly one deviation away from the set
     point, and the set point is zero. Sign and size are applied on display. */
  function simulate(seed) {
    var r = lcg(seed), d = 1, v = 0, n = 0, out = [d], i;
    for (i = 0; i < STEPS; i++) {
      v += -K * d;
      v *= DAMP;
      n = n * 0.86 + (r() - 0.5) * LOAD;
      d += v + n;
      out.push(d);
    }
    return out;
  }

  function analyse(a) {
    var cross = [], prev = Math.sign(a[0]), i, s;
    for (i = 1; i < a.length; i++) {
      s = Math.sign(a[i]);
      if (s !== 0 && s !== prev) { cross.push(i); prev = s; }
    }
    var ext = [], c, st, en, m, mi;
    for (c = 0; c < cross.length; c++) {
      st = cross[c];
      en = (cross[c + 1] !== undefined) ? cross[c + 1] : a.length;
      m = 0; mi = st;
      for (i = st; i < en; i++) { if (Math.abs(a[i]) > Math.abs(m)) { m = a[i]; mi = i; } }
      ext.push({ v: m, i: mi });
    }
    return { cross: cross, ext: ext };
  }

  /* A run is only usable if the drawn curve actually shows what the captions
     claim: a modest overshoot, visibly smaller swings after it, and a level
     still crossing the line at the right-hand edge. ~56% of seeds qualify. */
  function usable(a) {
    var r = analyse(a);
    if (r.cross.length < 4 || r.ext.length < 3) return false;
    var e0 = Math.abs(r.ext[0].v), e1 = Math.abs(r.ext[1].v), e2 = Math.abs(r.ext[2].v);
    if (e0 < 0.24 || e0 > 0.30) return false;
    if (e1 < 0.06 || e1 > 0.13) return false;
    if (!(e0 > e1 && e1 > e2)) return false;
    var tail = Math.floor(a.length * 0.72), i;
    for (i = 0; i < r.cross.length; i++) { if (r.cross[i] >= tail) break; }
    if (i === r.cross.length) return false;
    for (i = 1; i < a.length; i++) { if (a[i] > 1.001) return false; }
    return true;
  }

  function runFor(seed) {
    var s = seed >>> 0, a = simulate(s), guard = 0;
    while (!usable(a) && guard < 60) {
      s = (s * 1103515245 + 12345) >>> 0;
      a = simulate(s);
      guard++;
    }
    return { level: a, marks: analyse(a) };
  }

  /* ------------------------------------------------------------ scenarios */

  var GLUCOSE = {
    quantity: 'blood glucose',
    subject: 'glucose',
    centre: 'pancreas',
    high: {
      name: 'Insulin', lower: 'insulin', full: 'insulin',
      mech: 'glucose moves into cells and is stored as glycogen in the liver'
    },
    low: {
      name: 'Glucagon', lower: 'glucagon', full: 'glucagon',
      mech: 'the liver converts stored glycogen back into glucose'
    }
  };

  var TEMPERATURE = {
    quantity: 'core body temperature',
    subject: 'temperature',
    centre: 'thermoregulatory centre',
    high: {
      name: 'Sweating', lower: 'sweating', full: 'sweating and vasodilation', plural: true,
      mech: 'sweat evaporates and the skin arterioles widen, so more heat is lost'
    },
    low: {
      name: 'Shivering', lower: 'shivering', full: 'shivering and vasoconstriction', plural: true,
      mech: 'muscles contract rapidly to release heat and the skin arterioles narrow'
    }
  };

  var WATER = {
    quantity: 'the water content of the blood',
    subject: 'the level',
    centre: 'brain',
    high: {
      name: 'Less ADH', lower: 'less ADH', full: 'less ADH',
      mech: 'the kidney reabsorbs less water, so a large volume of dilute urine is made'
    },
    low: {
      name: 'More ADH', lower: 'more ADH', full: 'more ADH',
      mech: 'the kidney reabsorbs more water, so only a little concentrated urine is made'
    }
  };

  var SCENARIOS = [
    {
      id: 'glucose-high', sys: GLUCOSE, setPoint: 5, start: 8, dp: 1, unit: ' mmol/dm³',
      spShort: '5.0', spWord: '5.0',
      frame: 'Twenty minutes after a meal, blood glucose has climbed to 8.0 mmol/dm³ — well above the set point of 5.0. Predict what happens over the next hour.'
    },
    {
      id: 'glucose-low', sys: GLUCOSE, setPoint: 5, start: 3.7, dp: 1, unit: ' mmol/dm³',
      spShort: '5.0', spWord: '5.0',
      frame: 'It is five hours since the last meal and blood glucose has fallen to 3.7 mmol/dm³, below the set point of 5.0. Predict what happens over the next hour.'
    },
    {
      id: 'temperature-high', sys: TEMPERATURE, setPoint: 37, start: 38, dp: 1, unit: '°C',
      spShort: '37.0', spWord: '37.0',
      frame: 'Twenty minutes into a hard run, core body temperature has reached 38.0°C — above the set point of 37.0°C. Predict what happens over the next half hour.'
    },
    {
      id: 'temperature-low', sys: TEMPERATURE, setPoint: 37, start: 36.3, dp: 1, unit: '°C',
      spShort: '37.0', spWord: '37.0',
      frame: 'Ten minutes waiting in cold rain has taken core body temperature down to 36.3°C, below the set point of 37.0°C. Predict the next half hour.'
    },
    {
      id: 'water-high', sys: WATER, setPoint: 0, start: 1, dp: 0, unit: '', qualitative: true,
      spShort: 'set point', spWord: 'the set point',
      frame: 'A litre of water drunk in one go has pushed the water content of the blood above its set point. Predict what happens over the next few hours.'
    },
    {
      id: 'water-low', sys: WATER, setPoint: 0, start: -1, dp: 0, unit: '', qualitative: true,
      spShort: 'set point', spWord: 'the set point',
      frame: 'A salty meal has left the blood too concentrated: the water content is below its set point. Predict what happens over the next few hours.'
    }
  ];

  /* --------------------------------------------------------- round wiring */

  function buildRound(sc, seed) {
    var above = sc.start > sc.setPoint;
    var first = above ? sc.sys.high : sc.sys.low;   /* acts on the starting side */
    var other = above ? sc.sys.low : sc.sys.high;   /* takes over once it crosses */
    var run = runFor(seed);
    var d0 = sc.start - sc.setPoint;                 /* signed display deviation */

    var value = function (dNorm) { return sc.setPoint + dNorm * d0; };
    var overshoot = run.marks.ext[0].v;              /* normalised, opposite sign */

    var subj = sc.sys.subject;
    var moveDown = above;
    var goes = moveDown ? 'falls' : 'rises';
    var comesBack = moveDown ? 'lifts it back' : 'brings it down';
    var carriesOn = moveDown ? 'keeps on falling' : 'keeps on rising';
    var nothing = moveDown ? 'Nothing lifts it back.' : 'Nothing brings it down.';
    var sp = sc.spWord;

    var cap = function (t) { return t.charAt(0).toUpperCase() + t.slice(1); };
    var eases = first.plural ? ' ease off' : ' eases off';
    var acts = other.plural ? ' act on the other side' : ' acts on the other side';

    var options = [
      {
        key: 'cycle',
        text: first.name + ' — ' + subj + ' ' + goes + ' past ' + sp + ', then ' +
              other.lower + ' ' + comesBack + '. It keeps swinging.'
      },
      {
        key: 'swap',
        text: other.name + ' — ' + subj + ' ' + goes + ' past ' + sp + ', then ' +
              first.lower + ' ' + comesBack + '. It keeps swinging.'
      },
      {
        key: 'stops',
        text: first.name + ' — ' + subj + ' ' + goes + ' to ' + sp +
              ', the response switches off, and it holds exactly there.'
      },
      {
        key: 'runaway',
        text: first.name + ' — ' + subj + ' ' + goes + ' past ' + sp + ' and ' +
              carriesOn + '. ' + nothing
      }
    ];

    /* deterministic shuffle from the same seed, so the right card moves about */
    var rnd = lcg(seed ^ 0x9e3779b9), i, j, t;
    for (i = options.length - 1; i > 0; i--) {
      j = Math.floor(rnd() * (i + 1));
      t = options[i]; options[i] = options[j]; options[j] = t;
    }

    var fmt = function (dNorm) {
      if (sc.qualitative) return null;
      return value(dNorm).toFixed(sc.dp) + sc.unit;
    };
    var overStr = fmt(overshoot);
    var pastLine = sc.qualitative
      ? 'past ' + sp
      : 'past ' + sp + ' to ' + overStr;
    var reached = sc.qualitative
      ? 'carried on a little way past the set point'
      : 'reached ' + overStr;
    var sideWord = above ? 'above' : 'below';

    var crossings = run.marks.cross.length;

    var feedback = {
      cycle:
        'Right — you said ' + first.lower + ', then ' + other.lower + ' ' +
        (moveDown ? 'lifting it back' : 'bringing it down') + '. ' + cap(subj) + ' ' +
        goes + ' ' + pastLine + ', then ' + other.lower + ' takes over on the other ' +
        'side. ' + cap(first.full) + eases + ' as the level returns, but what is ' +
        'already acting carries it past — so the deviation swaps sides, and the level ' +
        'is still crossing ' + sp + ' at the edge of the graph.',
      stops:
        'Not quite — you said ' + subj + ' ' + goes + ' to ' + sp +
        ' and holds exactly there. It went ' + pastLine + ', and ' + other.lower + ' ' +
        comesBack + '. ' + cap(first.full) + eases + ' as the level returns, but ' +
        'what is already acting carries it past the line; past it, the deviation is ' +
        'on the other side, so the opposite response starts.',
      swap:
        'Not quite — you said ' + other.lower + ' acts first. ' + cap(subj) + ' was ' +
        sideWord + ' ' + sp + ', and on that side it is ' + first.lower + ' that acts: ' +
        first.mech + '. ' + cap(other.full) + acts + ' — that is what ' +
        'brought the level back after it ' + reached + '.',
      runaway:
        'Not quite — you said ' + subj + ' ' + goes + ' past ' + sp + ' and ' +
        carriesOn + '. It ' + reached + ', then turned and came back: on the other ' +
        'side of the set point the level is deviating again, the other way, so ' +
        other.lower + ' starts and ' + comesBack + '. The loop answers the deviation ' +
        'whichever side of the line it is on.',
      short:
        'Right — ' + first.lower + ', then ' + other.lower + ' ' +
        (moveDown ? 'lifting it back' : 'bringing it down') + '. ' + cap(subj) + ' went ' +
        pastLine + ' and swung back, crossing ' + sp + ' ' + crossings + ' times.'
    };

    var srText = sc.qualitative
      ? 'The level ' + goes + ' past the set point, turns, and crosses back. It crosses the set point ' +
        crossings + ' times and is still moving at the end.'
      : 'The level ' + goes + ' past ' + sp + ' to ' + overStr +
        ', turns, and crosses back. It crosses the set point ' + crossings +
        ' times and is still moving at the end.';

    return {
      sc: sc, run: run, above: above, first: first, other: other,
      options: options, feedback: feedback, value: value, fmt: fmt,
      d0: d0, srText: srText, crossings: crossings,
      overIndex: run.marks.ext[0].i
    };
  }

  /* -------------------------------------------------------------- drawing */

  function hexToRgb(hex) {
    var h = String(hex || '').trim().replace('#', '');
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    if (!/^[0-9a-fA-F]{6}$/.test(h)) h = '8a6a4f';
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
  }

  function draw(cv, round, accentRgb, revealed, progress) {
    var css = cv.getBoundingClientRect();
    var w = Math.max(200, Math.round(css.width));
    var h = Math.round(css.height);
    var dpr = Math.min(3, window.devicePixelRatio || 1);
    if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) {
      cv.width = Math.round(w * dpr);
      cv.height = Math.round(h * dpr);
    }
    var g = cv.getContext('2d');
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, w, h);

    var A = function (a) { return 'rgba(' + accentRgb[0] + ',' + accentRgb[1] + ',' + accentRgb[2] + ',' + a + ')'; };
    var MUTED = '#8d8880', HAIR = '#e0d9cd';
    var sansFont = 'Inter, system-ui, -apple-system, "Segoe UI", sans-serif';

    /* Labels sit over the trace and the dashed line, so give each one a small
       patch of the stage's own paper to stand on - otherwise the curve runs
       straight through the words. */
    function label(txt, x, y, align, baseline) {
      g.font = '600 10.5px ' + sansFont;
      g.textAlign = align;
      g.textBaseline = baseline;
      var tw = g.measureText(txt).width, th = 11;
      var rx = align === 'right' ? x - tw : (align === 'center' ? x - tw / 2 : x);
      var ry = baseline === 'top' ? y : (baseline === 'middle' ? y - th / 2 : y - th + 2);
      g.fillStyle = '#faf8f5';
      g.fillRect(rx - 2, ry - 1.5, tw + 4, th + 3);
      g.fillStyle = MUTED;
      g.fillText(txt, x, y);
    }

    var padL = 9, padR = 9, padT = 9, band = 26;
    var plotT = padT, plotB = h - band - 6, plotH = plotB - plotT;
    var plotL = padL, plotR = w - padR, plotW = plotR - plotL;

    var sc = round.sc, d0 = round.d0;
    var span = Math.abs(d0);
    var vTop = round.above ? sc.setPoint + span * 1.12 : sc.setPoint + span * 0.42;
    var vBot = round.above ? sc.setPoint - span * 0.42 : sc.setPoint - span * 1.12;
    var yOf = function (val) { return plotT + (vTop - val) / (vTop - vBot) * plotH; };
    var total = PAST + STEPS;
    var xOf = function (i) { return plotL + (i / total) * plotW; };

    /* the story so far: a smooth approach to where the student joins it */
    var pastAt = function (i) {
      var u = i / PAST;
      return round.value(u * u * (3 - 2 * u));
    };
    var futureAt = function (i) { return round.value(round.run.level[i]); };

    var spY = yOf(sc.setPoint);
    var nowX = xOf(PAST);

    /* ---- the response band: how hard the loop is working, and which way */
    if (revealed) {
      var shown = PAST + Math.round(STEPS * progress);
      var bandT = h - band, bandH = band - 8;
      var i, dv, strength, x;
      for (i = 0; i <= shown; i++) {
        dv = (i <= PAST) ? (pastAt(i) - sc.setPoint) : (futureAt(i - PAST) - sc.setPoint);
        strength = Math.min(1, Math.abs(dv) / span);
        x = xOf(i);
        g.fillStyle = A(0.06 + 0.5 * strength);
        g.fillRect(x, bandT, (plotW / total) + 1.2, bandH);
      }
      /* handover lines where the level crosses and the other response takes over */
      var cr = round.run.marks.cross;
      for (i = 0; i < cr.length; i++) {
        if (PAST + cr[i] > shown) break;
        x = xOf(PAST + cr[i]);
        g.strokeStyle = HAIR; g.lineWidth = 1;
        g.beginPath(); g.moveTo(x, bandT); g.lineTo(x, bandT + bandH); g.stroke();
      }
      /* name the response in each stretch wide enough to hold a word */
      g.font = '600 10.5px ' + sansFont;
      g.textBaseline = 'middle';
      var bounds = [0].concat(cr.map(function (c) { return PAST + c; })).concat([total]);
      var side = round.above ? 1 : -1;
      for (i = 0; i < bounds.length - 1; i++) {
        var s0 = bounds[i], s1 = Math.min(bounds[i + 1], shown);
        if (s1 - s0 <= 0) continue;
        var x0 = xOf(s0), x1 = xOf(s1);
        if (x1 - x0 < 46) continue;
        var isFirstSide = (i % 2 === 0);
        var resp = ((isFirstSide ? side : -side) > 0) ? sc.sys.high : sc.sys.low;
        g.fillStyle = MUTED;
        g.textAlign = 'center';
        g.fillText(resp.name, (x0 + x1) / 2, bandT + bandH / 2);
      }
    }

    /* ---- the set point */
    g.strokeStyle = HAIR;
    g.lineWidth = 1;
    g.setLineDash([4, 4]);
    g.beginPath(); g.moveTo(plotL, spY); g.lineTo(plotR, spY); g.stroke();
    g.setLineDash([]);

    /* The trace leaves the set point at the left edge, so put the label on
       whichever side of the line the curve is not using. */
    label('set point' + (sc.qualitative ? '' : ' ' + sc.spShort + sc.unit),
          plotL + 1, spY + (round.above ? 11 : -10), 'left', 'middle');

    /* ---- "now" */
    g.strokeStyle = HAIR;
    g.beginPath(); g.moveTo(nowX, plotT); g.lineTo(nowX, plotB); g.stroke();

    /* ---- the trace */
    g.lineWidth = 2;
    g.lineJoin = 'round';
    g.strokeStyle = A(1);
    g.beginPath();
    for (var p = 0; p <= PAST; p++) {
      var yy = yOf(pastAt(p));
      if (p === 0) g.moveTo(xOf(p), yy); else g.lineTo(xOf(p), yy);
    }
    g.stroke();

    if (revealed) {
      var upTo = Math.round(STEPS * progress);
      g.beginPath();
      g.moveTo(nowX, yOf(pastAt(PAST)));
      for (var f = 1; f <= upTo; f++) g.lineTo(xOf(PAST + f), yOf(futureAt(f)));
      g.stroke();

      /* the dip the feedback quotes, marked where it happens */
      if (upTo >= round.overIndex && !sc.qualitative) {
        var ox = xOf(PAST + round.overIndex), oy = yOf(futureAt(round.overIndex));
        g.fillStyle = A(1);
        g.beginPath(); g.arc(ox, oy, 2.6, 0, 6.2832); g.fill();
        /* to the side of the turning point, not under it - below the dip is
           where the response band starts */
        var txt = round.fmt(round.run.level[round.overIndex]);
        g.font = '600 10.5px ' + sansFont;
        var fits = ox + 7 + g.measureText(txt).width < plotR;
        label(txt, ox + (fits ? 7 : -7), oy, fits ? 'left' : 'right', 'middle');
      }
    } else {
      /* where the student joins the story */
      g.fillStyle = A(1);
      g.beginPath(); g.arc(nowX, yOf(pastAt(PAST)), 3.4, 0, 6.2832); g.fill();
      label('now', nowX + 5, plotT + 6, 'left', 'middle');
      if (!sc.qualitative) {
        label(sc.start.toFixed(sc.dp) + sc.unit, nowX - 6,
              yOf(pastAt(PAST)) + (round.above ? -9 : 11), 'right', 'middle');
      }
    }
    g.textBaseline = 'alphabetic';
  }

  /* ----------------------------------------------------------------- CSS */

  var CSS =
    '.svw-nfcc{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45}' +
    '.svw-nfcc *{box-sizing:border-box}' +
    '.svw-nfcc .nf-k{margin:0 0 2px;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase}' +
    '.svw-nfcc .nf-t{margin:0 0 6px;font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;font-weight:600;line-height:1.15}' +
    '.svw-nfcc .nf-frame{margin:0 0 10px;font-size:.84rem;line-height:1.45;color:#5b564e}' +
    '.svw-nfcc .nf-stage{margin:0 0 12px;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:5px}' +
    '.svw-nfcc .nf-cv{display:block;width:100%;height:118px}' +
    '.svw-nfcc .nf-opts{display:flex;flex-direction:column;gap:6px;margin:0 0 12px}' +
    '.svw-nfcc .nf-opt{display:block;width:100%;text-align:left;font:inherit;font-size:.8rem;line-height:1.35;' +
      'padding:.42rem .6rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;cursor:pointer}' +
    '.svw-nfcc .nf-opt:hover{border-color:#c9c1b3}' +
    '.svw-nfcc .nf-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}' +
    '.svw-nfcc .nf-opt:focus-visible{outline:2px solid #2d2a26;outline-offset:2px}' +
    '.svw-nfcc .nf-opt.nf-chosen{background:#faf8f5;border-color:#c9c1b3;color:#2d2a26}' +
    '.svw-nfcc .nf-fb{margin:0 0 12px;font-size:.84rem;line-height:1.5;color:#2d2a26}' +
        '.svw-nfcc .nf-fb b{font-weight:700}' +
    '.svw-nfcc .nf-done{margin:.5rem 0 0;color:#4f7d63;font-weight:600}' +
    '.svw-nfcc .nf-bar{display:flex;align-items:center;gap:.7rem;flex-wrap:wrap}' +
    '.svw-nfcc .nf-go{font:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;' +
      'border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}' +
    '.svw-nfcc .nf-go:disabled{background:#faf8f5;border-color:#ddd7cd;color:#9a948a;cursor:default}' +
    '.svw-nfcc .nf-go:focus-visible{outline:2px solid #2d2a26;outline-offset:2px}' +
    '.svw-nfcc .nf-run{font-size:.74rem;color:#8d8880;font-variant-numeric:tabular-nums}' +
    '.svw-nfcc .nf-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;' +
      'clip:rect(0 0 0 0);white-space:nowrap;border:0}' +
    /* last, and doubled, so it outranks .nf-opt{display:block} on both
       specificity and source order - the earlier single-class version lost
       the cascade and left "hidden" cards on screen after a commit. */
    '.svw-nfcc .nf-hide.nf-hide{display:none}';

  /* --------------------------------------------------------------- mount */

  window.SVWidget = {
    meta: {
      id: 'negative-feedback-continuous-cycle',
      title: 'Negative feedback: predict what happens next',
      teaches: 'Negative feedback corrects continuously around a set point, overshoots slightly, and never switches off for good.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      root.className = 'svw-nfcc';
      root.innerHTML = '';

      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      var accentHex = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
                      ctx.accent || '#8a6a4f';
      var accentRgb = hexToRgb(accentHex);
      var reduced = !!ctx.reducedMotion;

      var el = function (tag, cls, txt) {
        var n = document.createElement(tag);
        if (cls) n.className = cls;
        if (txt !== undefined) n.textContent = txt;
        return n;
      };

      var kicker = el('p', 'nf-k', 'Negative feedback');
      kicker.style.color = accentHex;
      var title = el('h3', 'nf-t', 'What happens next?');
      var frame = el('p', 'nf-frame', '');

      var stage = el('div', 'nf-stage');
      var cv = document.createElement('canvas');
      cv.className = 'nf-cv';
      cv.setAttribute('role', 'img');
      stage.appendChild(cv);

      var opts = el('div', 'nf-opts');
      var optBtns = [], i;
      for (i = 0; i < 4; i++) {
        var b = el('button', 'nf-opt');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        opts.appendChild(b);
        optBtns.push(b);
      }

      var fb = el('div', 'nf-fb nf-hide');
      var fbP = el('p', null, '');
      fbP.style.margin = '0';
      var fbDone = el('p', 'nf-done nf-hide', '');
      fb.appendChild(fbP);
      fb.appendChild(fbDone);

      var bar = el('div', 'nf-bar');
      var go = el('button', 'nf-go', 'Check');
      go.type = 'button';
      go.disabled = true;
      var runTxt = el('span', 'nf-run', '');
      bar.appendChild(go);
      bar.appendChild(runTxt);

      var sr = el('p', 'nf-sr', '');
      sr.setAttribute('aria-live', 'polite');

      root.appendChild(kicker);
      root.appendChild(title);
      root.appendChild(frame);
      root.appendChild(stage);
      root.appendChild(opts);
      root.appendChild(fb);
      root.appendChild(bar);
      root.appendChild(sr);

      /* ------------------------------------------------------------ state */

      var S = {
        round: null, picked: null, phase: 'ask',
        streak: 0, mastered: false, attempted: 0,
        lastScenario: -1, seed: (Date.now() ^ 0x5f3759df) >>> 0,
        progress: 0, raf: 0
      };

      function publish(extra) {
        var st = {
          streak: S.streak,
          mastered: S.mastered,
          attempted: S.attempted,
          scenario: S.round ? S.round.sc.id : null,
          picked: S.picked,
          phase: S.phase
        };
        if (extra) for (var k in extra) if (extra.hasOwnProperty(k)) st[k] = extra[k];
        root.dataset.svState = JSON.stringify(st);
      }

      function redraw() {
        if (!root.isConnected) return;
        draw(cv, S.round, accentRgb, S.phase === 'told', S.progress);
      }

      function animate() {
        if (S.raf) { cancelAnimationFrame(S.raf); S.raf = 0; }
        if (reduced) { S.progress = 1; redraw(); return; }
        var t0 = 0;
        var step = function (t) {
          if (!root.isConnected) { S.raf = 0; return; }
          if (!t0) t0 = t;
          S.progress = Math.min(1, (t - t0) / 620);
          redraw();
          if (S.progress < 1) S.raf = requestAnimationFrame(step);
          else S.raf = 0;
        };
        S.progress = 0;
        S.raf = requestAnimationFrame(step);
      }

      /* An LCG's low bits have a very short period, so `seed % 6` walked only
         the even scenarios and every below-set-point story was unreachable.
         Mix the whole word down before taking the remainder. */
      function mix32(x) {
        x = (x ^ (x >>> 16)) >>> 0;
        x = Math.imul(x, 0x7feb352d) >>> 0;
        x = (x ^ (x >>> 15)) >>> 0;
        x = Math.imul(x, 0x846ca68b) >>> 0;
        return (x ^ (x >>> 16)) >>> 0;
      }

      function nextScenario() {
        var n = SCENARIOS.length, idx, guard = 0;
        do {
          S.seed = (S.seed * 1103515245 + 12345) >>> 0;
          idx = mix32(S.seed) % n;
          guard++;
        } while (idx === S.lastScenario && guard < 12);
        S.lastScenario = idx;
        return SCENARIOS[idx];
      }

      function newRound() {
        var sc = nextScenario();
        S.seed = (S.seed * 1103515245 + 12345) >>> 0;
        S.round = buildRound(sc, S.seed);
        S.picked = null;
        S.phase = 'ask';
        S.progress = 0;

        frame.textContent = sc.frame;
        for (var i = 0; i < 4; i++) {
          optBtns[i].textContent = S.round.options[i].text;
          optBtns[i].dataset.key = S.round.options[i].key;
          optBtns[i].setAttribute('aria-pressed', 'false');
          optBtns[i].className = 'nf-opt';
          optBtns[i].disabled = false;
        }
        fb.classList.add('nf-hide');
        fbDone.classList.add('nf-hide');
        go.textContent = 'Check';
        go.disabled = true;
        cv.setAttribute('aria-label', sc.frame);
        sr.textContent = sc.frame;
        redraw();
        publish();
      }

      function pick(idx) {
        if (S.phase !== 'ask') return;
        S.picked = S.round.options[idx].key;
        for (var i = 0; i < 4; i++) {
          optBtns[i].setAttribute('aria-pressed', i === idx ? 'true' : 'false');
        }
        go.disabled = false;
        publish();
      }

      function commit() {
        if (!S.picked) return;
        S.phase = 'told';
        S.attempted += 1;
        var right = S.picked === 'cycle';
        if (right) S.streak += 1; else S.streak = 0;
        var justMastered = right && S.streak >= 3 && !S.mastered;
        if (right && S.streak >= 3) S.mastered = true;

        for (var i = 0; i < 4; i++) {
          if (optBtns[i].dataset.key === S.picked) {
            optBtns[i].className = 'nf-opt nf-chosen';
            optBtns[i].setAttribute('aria-pressed', 'false');
          } else {
            optBtns[i].className = 'nf-opt nf-hide';
          }
          optBtns[i].disabled = true;
        }

        /* Once they have it, the full explanation a third time is noise: give
           the short echo and say what they now know. */
        var useShort = right && S.mastered;
        fbP.textContent = useShort ? S.round.feedback.short : S.round.feedback[S.picked];
        fb.classList.remove('nf-hide');
        if (right && S.mastered) {
          fbDone.textContent = justMastered
            ? 'Three in a row — you have it. The loop never switches off for good: each correction carries the level a little past the set point, the opposite response takes over, and it swings gently either side.'
            : 'Still got it.';
          fbDone.classList.remove('nf-hide');
        } else {
          fbDone.classList.add('nf-hide');
        }

        go.textContent = S.mastered ? 'Another anyway' : 'Next situation';
        go.disabled = false;
        runTxt.textContent = S.mastered ? ''
          : (S.streak === 0
              ? 'Run reset — back to none in a row.'
              : (S.streak === 2 ? '2 right in a row — one more and you have it.'
                                : S.streak + ' right in a row.'));
        sr.textContent = fbP.textContent + ' ' + S.round.srText;
        animate();
        publish({ correct: right });
      }

      for (i = 0; i < 4; i++) {
        (function (n) {
          optBtns[n].addEventListener('click', function () { pick(n); });
        })(i);
      }
      go.addEventListener('click', function () {
        if (S.phase === 'ask') commit(); else newRound();
      });

      if (window.ResizeObserver) {
        var ro = new ResizeObserver(function () {
          if (!root.isConnected) { ro.disconnect(); return; }
          redraw();
        });
        ro.observe(stage);
      }

      newRound();
    }
  };
})();
