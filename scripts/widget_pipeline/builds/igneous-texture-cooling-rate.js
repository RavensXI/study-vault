/* igneous-texture-cooling-rate — StudyVault lesson widget
   The rock is a thermometer you can read backwards. One cooling model
   turns a cooling time into a crystal size in millimetres, and the SAME
   number drives the drawing, the classification and the marking — so the
   picture can never disagree with the verdict.

   Model: sizeMm(days) = 10^((log10 days - 4.2) / 3)
     3 days      (thin lava flow)      -> 0.057 mm   fine
     70 days     (thick lava flow)     -> 0.16 mm    fine
     2,000 y     (6 km, phenocrysts)   -> 3.6 mm     coarse (then quenched)
     10,000 y    (chamber 8 km down)   -> 6.1 mm     coarse
     100,000 y   (pluton 15 km down)   -> 13 mm      coarse
     30 seconds  (chilled in seawater) -> 0.0028 mm  glassy (no crystals)
   Every value sits clear of the 1 mm coarse/fine boundary by 6x or more, and
   the verdict itself compares ids, never floats. Every setting is also
   unambiguously at the surface or unambiguously deep, so one application of
   "slow cooling grows large crystals" settles every round. */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';
  var CLS = 'svw-igntex';
  var UID = 0;

  /* --------------------------------------------------------------- model */

  var DAY = 1;
  var YEAR = 365.25;

  function sizeMm(days) { return Math.pow(10, (Math.log10(days) - 4.2) / 3); }

  /* thresholds: glassy below 0.005 mm (nearest real value 0.057, 10x clear);
     coarse at or above 1 mm (nearest values 0.41 and 6.1, 2.4x clear) */
  function classify(mm) {
    if (mm < 0.005) return 'glassy';
    return mm >= 1 ? 'coarse' : 'fine';
  }

  function fmtMm(mm) {
    if (mm >= 10) return String(Math.round(mm));
    if (mm >= 1) return (Math.round(mm * 10) / 10).toFixed(1);
    if (mm >= 0.1) return (Math.round(mm * 100) / 100).toFixed(2);
    return (Math.round(mm * 1000) / 1000).toFixed(3);
  }

  /* Every cooling setting the widget can talk about. `days` is the time the
     melt takes to solidify; the crystal size comes from the model, never
     from a hand-typed number. */
  function setting(o) {
    o.mm = sizeMm(o.days);
    if (o.thenDays) { o.groundMm = sizeMm(o.thenDays); o.texture = 'porph'; }
    else { o.texture = classify(o.mm); }
    return o;
  }

  /* The dyke setting (1 km down, fine-grained) was removed after a field
     test: it is underground, so the lesson's own rule — "coarse means slow
     cooling deep underground" — gives the WRONG answer unless you already
     know that 1 km is not deep and three years is not slow. Every setting
     here is now unambiguous on the one dimension being tested: clearly at
     the surface, or clearly deep. */
  var S = {
    flow: setting({
      id: 'flow', depthKm: 0, days: 3 * DAY, rock: 'basalt',
      opt: 'At the surface — 3 days',
      frame: 'At the surface, basaltic magma spreads as a thin lava flow and is solid in three days.',
      when: 'three days at the surface'
    }),
    thick: setting({
      id: 'thick', depthKm: 0, days: 70 * DAY, rock: 'rhyolite',
      opt: 'At the surface — 10 weeks',
      frame: 'At the surface, a thick rhyolitic lava flow stays hot for about ten weeks.',
      when: 'ten weeks at the surface'
    }),
    quench: setting({
      id: 'quench', depthKm: 0, sea: true, days: 30 / 86400, rock: 'obsidian',
      opt: 'At the surface — under a minute',
      frame: 'At the surface, rhyolitic lava pours into the sea and chills solid in under a minute.',
      when: 'seconds in seawater'
    }),
    pluton8: setting({
      id: 'pluton8', depthKm: 8, days: 10000 * YEAR, rock: 'granite',
      opt: '8 km down — 10,000 years',
      frame: 'Eight kilometres down, granitic magma sits in a chamber for about 10,000 years.',
      when: '10,000 years 8 km down'
    }),
    pluton15: setting({
      id: 'pluton15', depthKm: 15, days: 100000 * YEAR, rock: 'gabbro',
      opt: '15 km down — 100,000 years',
      frame: 'Fifteen kilometres down, basaltic magma cools for about 100,000 years.',
      when: '100,000 years 15 km down'
    }),
    two: setting({
      id: 'two', depthKm: 6, days: 2000 * YEAR, thenDays: 3 * DAY, rock: 'porphyritic andesite',
      opt: '6 km down 2,000 years, then erupted',
      frame: 'Six kilometres down, andesitic magma grows crystals for 2,000 years — then it erupts and sets in three days.',
      when: '2,000 years at 6 km, then erupted'
    })
  };

  var TEXTURES = {
    coarse: { id: 'coarse', label: 'Coarse — crystals over 1 mm', short: 'coarse-grained', mm: 6, ground: 0 },
    fine: { id: 'fine', label: 'Fine — crystals under 1 mm', short: 'fine-grained', mm: 0.3, ground: 0 },
    porph: { id: 'porph', label: 'Porphyritic — two crystal sizes', short: 'porphyritic', mm: 3.5, ground: 0.06 },
    glassy: { id: 'glassy', label: 'Glassy — no crystals at all', short: 'glassy', mm: 0.002, ground: 0 }
  };
  var TEX_ORDER = ['coarse', 'fine', 'porph', 'glassy'];

  /* ---------------------------------------------------------------- deck */

  /* PREDICT: given the cooling setting, what texture forms?
     READ: given the texture, where did it cool? Every read round offers
     exactly one option in the right texture class, and at least one that
     is the misconception — a long time in the wrong place, or a single
     stage for a two-size rock. */
  function byDays(a, b) { return S[a].days - S[b].days; }

  /* The rule rides on every ask, so a student who half-remembers the lesson
     still has the one thing they need in front of them. */
  var RULE = 'Slow cooling grows large crystals. ';

  function readRound(ansId, optIds, frame) {
    return {
      dir: 'read', answer: ansId, spec: S[ansId],
      options: optIds.slice().sort(byDays),
      frame: frame, ask: RULE + 'Where did this rock cool?'
    };
  }

  function buildDeck() {
    var deck = [];
    ['flow', 'thick', 'quench', 'pluton8', 'pluton15', 'two'].forEach(function (id) {
      deck.push({
        dir: 'predict', answer: S[id].texture, spec: S[id], options: TEX_ORDER.slice(),
        frame: S[id].frame, ask: RULE + 'What texture forms?'
      });
    });
    /* Read rounds describe the specimen in the lesson's own words - seen by
       eye, needs a lens, no crystals - never in millimetres the lesson never
       taught. Every distractor is wrong on PLACE or on the number of cooling
       stages, so one clean application of the rule settles it. */
    deck.push(readRound('pluton8', ['flow', 'thick', 'quench', 'pluton8'],
      'A hand specimen. Interlocking crystals, all much the same size, easily seen by eye.'));
    deck.push(readRound('pluton15', ['thick', 'quench', 'two', 'pluton15'],
      'A hand specimen. Crystals all much the same size, some as wide as a fingernail.'));
    deck.push(readRound('quench', ['quench', 'flow', 'pluton8', 'two'],
      'A hand specimen. It is smooth and glassy, with no crystals at all.'));
    deck.push(readRound('flow', ['flow', 'two', 'pluton8', 'pluton15'],
      'A hand specimen. All the crystals are far too small to see without a lens.'));
    deck.push(readRound('two', ['flow', 'thick', 'two', 'pluton8'],
      'A hand specimen. Large crystals sit in a groundmass too fine to see.'));
    for (var i = deck.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = deck[i];
      deck[i] = deck[j]; deck[j] = t;
    }
    return deck;
  }

  /* ------------------------------------------------------------ geometry */

  var VBW = 300, VBH = 104;
  var SX = 18, SW = 98;              /* crust section panel */
  var AIR = 8, SURF = 20, HB = 96;   /* sky top, ground level, section base */
  /* The section runs to 18 km although the deepest body sits at 15, so a
     15 km pluton is drawn at its true depth and still clears the axis
     caption underneath. Ticks are labelled to 15 only. */
  var KM = (HB - SURF) / 18;         /* px per km */
  var CX = 236, CY = 48, R = 40;     /* specimen circle */
  var AX1 = 126, AX2 = 186, AY = 48; /* arrow between the two panels */

  function yKm(k) { return SURF + k * KM; }

  function el(name, attrs) {
    var e = document.createElementNS(NS, name), k;
    for (k in attrs) if (attrs.hasOwnProperty(k)) e.setAttribute(k, attrs[k]);
    return e;
  }
  function txt(x, y, s, size, fill, anchor) {
    var e = el('text', { x: x, y: y, 'font-size': size, fill: fill, 'text-anchor': anchor || 'middle' });
    e.textContent = s;
    return e;
  }
  function clear(g) { while (g.firstChild) g.removeChild(g.firstChild); }

  /* seeded so a redraw of the same round gives the same mosaic */
  function rng(seed) {
    var s = (seed >>> 0) || 1;
    return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  }

  var TONES = ['#d6ccb9', '#c1b6a0', '#e2d9c8', '#ab9f89', '#cdc2ad'];

  /* Field of view across the specimen, in mm. Chosen so the crystals are
     actually visible; the scale bar under the circle then tells the truth
     about how big they are. */
  function fieldMm(mm, phenoMm) {
    if (phenoMm) return Math.min(30, Math.max(6, phenoMm * 3.4));
    if (mm < 0.005) return 25;
    return Math.min(30, Math.max(1.2, mm * 18));
  }
  var BARS = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20];
  function barMm(fov) {
    var best = BARS[0];
    for (var i = 0; i < BARS.length; i++) if (BARS[i] <= fov * 0.45) best = BARS[i];
    return best;
  }

  /* ----------------------------------------------------------------- css */

  function css(accent, reduced) {
    var p = '.' + CLS + ' ';
    return '.' + CLS + '{background:#fff;border:1px solid #e8e3db;border-radius:16px;' +
      'padding:1rem;font-family:Inter,system-ui,-apple-system,sans-serif;color:#2d2a26;' +
      'box-sizing:border-box;max-width:100%;}' +
      p + '*{box-sizing:border-box;}' +
      p + '.k{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;' +
      'text-transform:uppercase;color:' + accent + ';}' +
      p + '.t{margin:.18rem 0 .4rem;font-family:"Source Serif 4",Georgia,serif;' +
      'font-weight:600;font-size:1.2rem;line-height:1.18;}' +
      p + '.frame{margin:0 0 .3rem;font-size:.84rem;line-height:1.42;color:#5b564e;}' +
      p + '.ask{margin:0 0 .45rem;font-size:.88rem;line-height:1.35;font-weight:600;}' +
      p + '.stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;' +
      'max-width:366px;margin:0 auto .45rem;overflow:hidden;}' +
      p + '.stage svg{display:block;width:100%;height:auto;}' +
      p + '.opts{display:grid;grid-template-columns:1fr;gap:.3rem;margin:0 0 .42rem;}' +
      p + '.o{font:600 .82rem/1.3 Inter,system-ui,sans-serif;color:#2d2a26;background:#faf8f5;' +
      'border:1px solid #ddd7cd;border-radius:10px;padding:.34rem .6rem;min-height:30px;' +
      'cursor:pointer;text-align:left;' +
      (reduced ? '' : 'transition:background .12s,border-color .12s;') + '}' +
      p + '.o[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}' +
      p + '.o.is-ans{border-color:' + accent + ';box-shadow:inset 0 0 0 1px ' + accent + ';}' +
      p + '.o[disabled]{cursor:default;opacity:.94;}' +
      p + '.act{display:flex;align-items:center;gap:.55rem;flex-wrap:wrap;margin:0 0 .4rem;}' +
      p + '.go{font:600 .82rem Inter,system-ui,sans-serif;background:#2d2a26;color:#fff;' +
      'border:1px solid #2d2a26;border-radius:10px;padding:.44rem .95rem;cursor:pointer;}' +
      p + '.go[disabled]{background:#faf8f5;color:#a8a29a;border-color:#e0d9cd;cursor:default;}' +
      p + '.run{font-size:.78rem;color:#8d8880;font-variant-numeric:tabular-nums;}' +
      p + '.cap{margin:0;font-size:.84rem;line-height:1.45;color:#2d2a26;min-height:44px;}' +
      p + '.cap .v{font-weight:700;}' +
      p + '.cap .rt{color:#4f7d63;}' +
      p + '.cap.rest{color:#8d8880;}' +
      p + '.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);' +
      'white-space:nowrap;margin:-1px;padding:0;border:0;}';
  }

  /* --------------------------------------------------------------- mount */

  window.SVWidget = {
    meta: {
      id: 'igneous-texture-cooling-rate',
      title: 'Read the rock backwards',
      teaches: 'Crystal size records cooling rate: slow cooling deep underground grows large crystals, fast cooling at the surface freezes tiny ones, and two crystal sizes mean two cooling stages.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;
      var uid = 'igt' + (++UID) + '-' + Math.floor(Math.random() * 100000);

      var wrap = document.createElement('div');
      wrap.className = CLS;
      var style = document.createElement('style');
      style.textContent = css(accent, reduced);
      wrap.appendChild(style);

      var kick = document.createElement('p'); kick.className = 'k';
      kick.textContent = 'Igneous texture';
      var ttl = document.createElement('h3'); ttl.className = 't';
      ttl.textContent = 'Read the rock backwards';
      var frame = document.createElement('p'); frame.className = 'frame';
      var ask = document.createElement('p'); ask.className = 'ask';
      wrap.appendChild(kick); wrap.appendChild(ttl); wrap.appendChild(frame); wrap.appendChild(ask);

      /* ------------------------------------------------------------ stage */
      var stage = document.createElement('div'); stage.className = 'stage';
      var svg = el('svg', {
        viewBox: '0 0 ' + VBW + ' ' + VBH, role: 'img',
        'aria-label': 'A crust cross-section beside a rock specimen'
      });
      stage.appendChild(svg); wrap.appendChild(stage);

      var defs = el('defs', {});
      var clip = el('clipPath', { id: uid + '-c' });
      clip.appendChild(el('circle', { cx: CX, cy: CY, r: R }));
      var pat = el('pattern', { id: uid + '-p', patternUnits: 'userSpaceOnUse', width: 4, height: 4 });
      var patG = el('g', { transform: 'scale(4)' });
      patG.appendChild(el('rect', { x: 0, y: 0, width: 1.02, height: 1.02, fill: TONES[0] }));
      [[0, 0, 0.55, 0.48, 1], [0.55, 0, 0.45, 0.52, 2], [0, 0.48, 0.5, 0.52, 3], [0.5, 0.52, 0.5, 0.48, 4]]
        .forEach(function (q) {
          patG.appendChild(el('rect', {
            x: q[0], y: q[1], width: q[2], height: q[3], fill: TONES[q[4]],
            stroke: '#9c927f', 'stroke-width': 0.05
          }));
        });
      pat.appendChild(patG);
      defs.appendChild(clip); defs.appendChild(pat);
      svg.appendChild(defs);

      /* section: sky, crust, depth grid */
      svg.appendChild(el('rect', { x: SX, y: AIR, width: SW, height: SURF - AIR, fill: '#f3efe8' }));
      var sea = el('rect', { x: SX, y: AIR, width: SW, height: SURF - AIR, fill: '#dce6ea' });
      sea.style.display = 'none';
      svg.appendChild(sea);
      svg.appendChild(el('rect', { x: SX, y: SURF, width: SW, height: HB - SURF, fill: '#e6dfd2' }));
      [5, 10].forEach(function (k) {
        svg.appendChild(el('line', {
          x1: SX, y1: yKm(k), x2: SX + SW, y2: yKm(k),
          stroke: '#cfc4b2', 'stroke-width': 0.6, 'stroke-dasharray': '2 4'
        }));
      });
      [0, 5, 10, 15].forEach(function (k) {
        svg.appendChild(txt(SX - 3, yKm(k) + 3, String(k), 9, '#8d8880', 'end'));
      });
      svg.appendChild(el('line', { x1: SX, y1: SURF, x2: SX + SW, y2: SURF, stroke: '#8d8880', 'stroke-width': 1 }));
      svg.appendChild(el('rect', {
        x: SX, y: AIR, width: SW, height: HB - AIR, fill: 'none',
        stroke: '#ddd5c7', 'stroke-width': 0.8
      }));
      svg.appendChild(txt(SX + SW / 2, 103, 'depth (km)', 9, '#8d8880'));

      /* rate axis: deeper is slower. Sits clear of the magma bodies, which
         never reach past x = 92. */
      var RAX = SX + SW - 17;
      svg.appendChild(el('path', {
        d: 'M ' + RAX + ' ' + (SURF + 7) + ' L ' + RAX + ' ' + (HB - 9) +
          ' M ' + (RAX - 2.8) + ' ' + (HB - 14) + ' L ' + RAX + ' ' + (HB - 9) + ' L ' + (RAX + 2.8) + ' ' + (HB - 14),
        fill: 'none', stroke: '#c4b9a6', 'stroke-width': 1,
        'stroke-linecap': 'round', 'stroke-linejoin': 'round'
      }));
      [[SURF + 21, 'fast'], [HB - 24, 'slow']].forEach(function (q) {
        var lx = SX + SW - 8, t = txt(lx, q[0], q[1], 8.5, '#9a938a');
        t.setAttribute('transform', 'rotate(-90 ' + lx + ' ' + q[0] + ')');
        svg.appendChild(t);
      });

      var bodies = el('g', {});
      svg.appendChild(bodies);

      /* arrow between the panels */
      var arrow = el('path', {
        d: '', stroke: '#a49b8c', 'stroke-width': 1.4, fill: 'none',
        'stroke-linecap': 'round', 'stroke-linejoin': 'round'
      });
      var arrowLbl = txt((AX1 + AX2) / 2, AY - 7, '', 8.5, '#8d8880');
      svg.appendChild(arrow); svg.appendChild(arrowLbl);

      /* specimen */
      svg.appendChild(el('circle', { cx: CX, cy: CY, r: R, fill: '#f1ebe1' }));
      var rockG = el('g', { 'clip-path': 'url(#' + uid + '-c)' });
      svg.appendChild(rockG);
      svg.appendChild(el('circle', { cx: CX, cy: CY, r: R, fill: 'none', stroke: '#8d8880', 'stroke-width': 1.2 }));
      var scaleG = el('g', {});
      svg.appendChild(scaleG);

      /* --------------------------------------------------------- controls */
      var opts = document.createElement('div'); opts.className = 'opts';
      opts.setAttribute('role', 'group');
      opts.setAttribute('aria-label', 'Choose your answer');
      var btns = [], i;
      for (i = 0; i < 4; i++) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'o'; b.setAttribute('aria-pressed', 'false');
        opts.appendChild(b); btns.push(b);
      }
      wrap.appendChild(opts);

      var act = document.createElement('div'); act.className = 'act';
      var go = document.createElement('button');
      go.type = 'button'; go.className = 'go'; go.textContent = 'Check';
      go.disabled = true;
      var run = document.createElement('span'); run.className = 'run';
      act.appendChild(go); act.appendChild(run); wrap.appendChild(act);

      var cap = document.createElement('p'); cap.className = 'cap rest';
      var sr = document.createElement('p'); sr.className = 'sr';
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(cap); wrap.appendChild(sr);
      root.appendChild(wrap);

      /* ------------------------------------------------------------ state */
      var deck = buildDeck(), deckAt = 0;
      var round = null, picked = null, locked = false, seed = 1;
      var streak = 0, attempted = 0, mastered = false;

      function pushState(extra) {
        var s = { streak: streak, mastered: mastered, attempted: attempted };
        if (round) {
          s.direction = round.dir;
          s.answer = round.answer;
          s.crystalMm = Math.round(round.spec.mm * 1000) / 1000;
          if (round.spec.groundMm) s.groundMm = Math.round(round.spec.groundMm * 1000) / 1000;
        }
        if (extra) for (var k in extra) if (extra.hasOwnProperty(k)) s[k] = extra[k];
        root.dataset.svState = JSON.stringify(s);
      }

      /* ---------------------------------------------------------- drawing */

      function setPattern(t) {
        pat.setAttribute('width', t);
        pat.setAttribute('height', t);
        patG.setAttribute('transform', 'scale(' + t + ')');
      }

      function drawScale(fov) {
        clear(scaleG);
        var bm = barMm(fov), w = bm * (2 * R / fov), y = 94;
        var x1 = CX - w / 2, x2 = CX + w / 2;
        scaleG.appendChild(el('line', { x1: x1, y1: y, x2: x2, y2: y, stroke: '#8d8880', 'stroke-width': 1 }));
        scaleG.appendChild(el('line', { x1: x1, y1: y - 2.4, x2: x1, y2: y + 2.4, stroke: '#8d8880', 'stroke-width': 1 }));
        scaleG.appendChild(el('line', { x1: x2, y1: y - 2.4, x2: x2, y2: y + 2.4, stroke: '#8d8880', 'stroke-width': 1 }));
        scaleG.appendChild(txt(CX, 103, String(bm) + ' mm', 9, '#8d8880'));
      }

      function poly(pts, fill, stroke, w) {
        return el('polygon', { points: pts.join(' '), fill: fill, stroke: stroke, 'stroke-width': w });
      }

      /* interlocking mosaic: neighbouring crystals share jittered vertices,
         so the grains lock together the way they do in a real coarse rock */
      function mosaic(cell) {
        var rand = rng(seed * 7919 + 13);
        var n = Math.ceil((2 * R) / cell) + 2;
        var x0 = CX - R - cell, y0 = CY - R - cell;
        var jx = [], jy = [], a, c;
        for (a = 0; a <= n; a++) {
          jx.push([]); jy.push([]);
          for (c = 0; c <= n; c++) {
            jx[a].push((rand() - 0.5) * cell * 0.46);
            jy[a].push((rand() - 0.5) * cell * 0.46);
          }
        }
        var k = 0;
        for (a = 0; a < n; a++) for (c = 0; c < n; c++) {
          var ax = x0 + c * cell, ay = y0 + a * cell;
          var dx = ax + cell / 2 - CX, dy = ay + cell / 2 - CY;
          if (Math.sqrt(dx * dx + dy * dy) > R + cell) continue;
          var pts = [
            (ax + jx[a][c]).toFixed(1) + ',' + (ay + jy[a][c]).toFixed(1),
            (ax + cell + jx[a][c + 1]).toFixed(1) + ',' + (ay + jy[a][c + 1]).toFixed(1),
            (ax + cell + jx[a + 1][c + 1]).toFixed(1) + ',' + (ay + cell + jy[a + 1][c + 1]).toFixed(1),
            (ax + jx[a + 1][c]).toFixed(1) + ',' + (ay + cell + jy[a + 1][c]).toFixed(1)
          ];
          rockG.appendChild(poly(pts, TONES[k++ % TONES.length], '#8d8880', 0.7));
        }
      }

      function phenocrysts(size) {
        var rand = rng(seed * 104729 + 71);
        var spots = [[-0.44, -0.32], [0.30, -0.44], [-0.06, 0.16], [0.46, 0.26], [-0.46, 0.46]];
        spots.forEach(function (s, k) {
          var px = CX + s[0] * R, py = CY + s[1] * R, pts = [], m, ang, rr;
          for (m = 0; m < 5; m++) {
            ang = (m / 5) * Math.PI * 2 + rand() * 0.55;
            rr = size * 0.5 * (0.74 + rand() * 0.46);
            pts.push((px + Math.cos(ang) * rr).toFixed(1) + ',' + (py + Math.sin(ang) * rr).toFixed(1));
          }
          rockG.appendChild(poly(pts, TONES[(k + 1) % TONES.length], '#6f6a61', 0.9));
        });
      }

      function glass() {
        rockG.appendChild(el('rect', { x: CX - R, y: CY - R, width: 2 * R, height: 2 * R, fill: '#4b463f' }));
        [[-20, 34], [-2, 44], [18, 30]].forEach(function (q) {
          rockG.appendChild(el('path', {
            d: 'M ' + (CX + q[0]) + ' ' + (CY - q[1]) + ' A ' + q[1] + ' ' + q[1] + ' 0 0 1 ' +
              (CX + q[0]) + ' ' + (CY + q[1]),
            fill: 'none', stroke: '#7d766c', 'stroke-width': 0.9
          }));
        });
        rockG.appendChild(el('ellipse', { cx: CX - 12, cy: CY - 14, rx: 15, ry: 8, fill: '#ffffff', opacity: 0.13 }));
      }

      /* one entry point: the millimetre figures come from the model, so the
         picture and the marking can never disagree */
      function drawSpecimen(mm, ground) {
        clear(rockG);
        var fov = fieldMm(mm, ground ? mm : 0);
        drawScale(fov);
        var upp = (2 * R) / fov, cell = mm * upp;
        if (!ground && mm < 0.005) { glass(); return; }
        if (ground) {
          setPattern(Math.max(ground * upp, 1.7));
          rockG.appendChild(el('rect', { x: CX - R, y: CY - R, width: 2 * R, height: 2 * R, fill: 'url(#' + uid + '-p)' }));
          phenocrysts(cell);
        } else if (cell >= 9) {
          mosaic(cell);
        } else {
          setPattern(Math.max(cell, 1.7));
          rockG.appendChild(el('rect', { x: CX - R, y: CY - R, width: 2 * R, height: 2 * R, fill: 'url(#' + uid + '-p)' }));
        }
      }

      function blankSpecimen() {
        clear(rockG); clear(scaleG);
      }

      function magmaBody(s, fill, stroke, dashed) {
        var g = el('g', {}), mid = SX + SW / 2;
        var dash = dashed ? '3 2' : '';
        if (s.depthKm > 0.05) {
          g.appendChild(el('ellipse', {
            cx: mid, cy: yKm(s.depthKm), rx: 25, ry: Math.min(8, 3.2 + s.depthKm * 0.42),
            fill: fill, stroke: stroke, 'stroke-width': 1.1, 'stroke-dasharray': dash
          }));
        }
        if (s.depthKm <= 0.05 || s.thenDays) {
          g.appendChild(el('rect', {
            x: mid - 27, y: SURF - 4.4, width: 54, height: 4.4, rx: 1.6,
            fill: fill, stroke: stroke, 'stroke-width': 1.1, 'stroke-dasharray': dash
          }));
        }
        if (s.thenDays) {
          g.appendChild(el('path', {
            d: 'M ' + mid + ' ' + (yKm(s.depthKm) - 6) + ' L ' + mid + ' ' + (SURF + 1) +
              ' M ' + (mid - 3) + ' ' + (SURF + 6) + ' L ' + mid + ' ' + (SURF + 1) + ' L ' + (mid + 3) + ' ' + (SURF + 6),
            fill: 'none', stroke: stroke, 'stroke-width': 1.1, 'stroke-linecap': 'round', 'stroke-linejoin': 'round'
          }));
        }
        return g;
      }

      function setArrow(dir) {
        var y = AY;
        if (dir === 'predict') {
          arrow.setAttribute('d', 'M ' + AX1 + ' ' + y + ' L ' + AX2 + ' ' + y +
            ' M ' + (AX2 - 6) + ' ' + (y - 4) + ' L ' + AX2 + ' ' + y + ' L ' + (AX2 - 6) + ' ' + (y + 4));
          arrowLbl.textContent = 'grows';
        } else {
          arrow.setAttribute('d', 'M ' + AX2 + ' ' + y + ' L ' + AX1 + ' ' + y +
            ' M ' + (AX1 + 6) + ' ' + (y - 4) + ' L ' + AX1 + ' ' + y + ' L ' + (AX1 + 6) + ' ' + (y + 4));
          arrowLbl.textContent = 'records';
        }
      }

      /* --------------------------------------------------------- feedback */

      var WHERE = {
        flow: 'at the surface', thick: 'at the surface', quench: 'at the surface',
        pluton8: '8 km down', pluton15: '15 km down', two: '6 km down'
      };
      var DUR = {
        flow: 'three days', thick: 'ten weeks', quench: 'under a minute',
        pluton8: '10,000 years', pluton15: '100,000 years', two: '2,000 years'
      };
      /* a faithful echo of what the button said, in prose */
      var ECHO = {
        flow: 'the surface, three days', thick: 'the surface, ten weeks',
        quench: 'the surface, under a minute', pluton8: '8 km down, 10,000 years',
        pluton15: '15 km down, 100,000 years', two: '6 km down for 2,000 years, then erupted'
      };
      var WHY = {
        flow: 'At the surface the heat pours straight into the air, so it sets in three days and atoms freeze where they stand.',
        thick: 'Ten weeks sounds long, but surface heat escapes fast — nowhere near slow enough to grow anything over 1 mm.',
        quench: 'Chilled in seawater in under a minute, the atoms had no time at all to line up into a crystal.',
        pluton8: 'Wrapped in hot rock 8 km down, the melt takes 10,000 years to set — time for atoms to travel to a growing crystal.',
        pluton15: '15 km down the melt cools for 100,000 years, the slowest setting here, so the crystals grow the biggest.',
        two: 'The 2,000 years at 6 km grew the big crystals; the eruption then froze the rest in three days.'
      };
      function cap1(t) { return t.charAt(0).toUpperCase() + t.slice(1); }
      function sizePhrase(s) {
        if (s.texture === 'glassy') return 'no crystals at all';
        return 'crystals about ' + fmtMm(s.mm) + ' mm';
      }

      function predictMsg(ok, pick) {
        var s = round.spec, ans = round.answer, mm = fmtMm(s.mm);
        if (ok) {
          if (ans === 'porph') {
            return 'porphyritic: two sizes at once. The 2,000 years at 6 km grew crystals about ' +
              fmtMm(s.mm) + ' mm; the eruption then froze the rest at ' + fmtMm(s.groundMm) +
              ' mm. That is ' + s.rock + '.';
          }
          return TEXTURES[ans].short + ', ' + sizePhrase(s) + '. ' + WHY[s.id] +
            (s.rock ? ' That is ' + s.rock + '.' : '');
        }
        var said = 'you said ' + TEXTURES[pick].short + '. ';
        if (pick === 'coarse') {
          if (ans === 'fine') {
            return said + cap1(DUR[s.id]) + ' sounds long, but ' + WHERE[s.id] +
              ' the heat escapes almost at once, so crystals stop at about ' + mm +
              ' mm. Large crystals need depth.';
          }
          if (ans === 'glassy') {
            return said + 'This lava was solid in under a minute. Atoms need time to travel to a growing crystal; here they had none, so it froze as glass.';
          }
          return said + 'One size cannot record two stages: 2,000 years at 6 km grew crystals about ' +
            fmtMm(s.mm) + ' mm, then the eruption froze the rest at ' + fmtMm(s.groundMm) + ' mm.';
        }
        if (pick === 'fine') {
          if (ans === 'coarse') {
            return said + cap1(WHERE[s.id]) + ' the melt is wrapped in hot rock, a poor conductor, so it takes ' +
              DUR[s.id] + ' to set — and the crystals reach about ' + mm + ' mm, well over the 1 mm line.';
          }
          if (ans === 'glassy') {
            return said + 'Fine still means crystals, only small ones. Under a minute is too fast for any crystal to start, so this froze as a glass.';
          }
          return said + 'The groundmass is fine, about ' + fmtMm(s.groundMm) + ' mm, but the ' +
            fmtMm(s.mm) + ' mm crystals grew first, 2,000 years down at 6 km. Two sizes, two stages.';
        }
        if (pick === 'porph') {
          if (ans === 'glassy') {
            return said + 'Porphyritic needs two stages and two crystal sizes. This lava froze in under a minute, so it grew no crystals at all.';
          }
          return said + 'Two crystal sizes need two cooling stages. This magma cooled in one place at one rate, so every crystal came out about the same size — ' + mm + ' mm.';
        }
        if (ans === 'porph') {
          return said + 'Glass needs a freeze in seconds. This melt had 2,000 years at 6 km first, so it grew crystals about ' +
            fmtMm(s.mm) + ' mm before the eruption froze the rest.';
        }
        return said + 'Glass needs a freeze in seconds. This melt had ' + DUR[s.id] +
          ', enough to grow crystals about ' + mm + ' mm across.';
      }

      var READ_OK = {
        pluton8: 'crystals you can see by eye mean slow. Only depth is that slow: 8 km down, wrapped in hot rock, the melt took 10,000 years. That is granite.',
        pluton15: 'crystals that big mean very slow indeed. 15 km down the melt cooled for 100,000 years, so the grains grew to about ' + fmtMm(S.pluton15.mm) + ' mm. That is gabbro.',
        quench: 'no crystals at all means instant. Lava dropped into seawater loses its heat in seconds, and atoms freeze before a crystal can start. That is obsidian.',
        flow: 'crystals too small to see mean fast. A thin flow gives its heat to the air and is solid in three days, so nothing grows big. That is basalt.',
        two: 'two crystal sizes mean two stages. The big crystals grew slowly 6 km down; the groundmass froze in days after the eruption. That is porphyritic andesite.'
      };

      function readMsg(ok, pick) {
        var s = round.spec, p = S[pick];
        if (ok) return READ_OK[s.id];
        var said = 'you chose ' + ECHO[pick] + '. ';
        if (s.groundMm) {
          return said + 'One place at one rate gives one crystal size. This rock has two, so it cooled in two stages: slowly at 6 km, then fast after erupting.';
        }
        if (p.groundMm) {
          return said + 'That gives two crystal sizes. These are all one size, so one place and one rate — ' + s.when + '.';
        }
        if (p.texture === 'glassy') {
          return said + 'A freeze that fast leaves glass, not crystals. These reached ' + fmtMm(s.mm) +
            ' mm, so this melt cooled much more slowly — ' + s.when + '.';
        }
        if (p.depthKm === 0 && s.depthKm > 0) {
          return said + 'Surface heat escapes into the air, so even ' + DUR[p.id] + ' only reaches ' +
            fmtMm(p.mm) + ' mm. Crystals this big need ' + DUR[s.id] + ' deep down.';
        }
        if (p.mm > s.mm) {
          return said + 'That grows crystals about ' + fmtMm(p.mm) +
            ' mm. These are far smaller, so this melt lost its heat much faster — ' + s.when + '.';
        }
        return said + 'That only reaches about ' + fmtMm(p.mm) +
          ' mm. These crystals are far bigger, so the melt cooled much more slowly — ' + s.when + '.';
      }

      function verdict(ok, body) {
        cap.className = 'cap';
        cap.innerHTML = '';
        var v = document.createElement('span');
        v.className = 'v' + (ok ? ' rt' : '');
        v.textContent = ok ? 'Right — ' : 'Not quite — ';
        cap.appendChild(v);
        cap.appendChild(document.createTextNode(body));
        sr.textContent = (ok ? 'Right. ' : 'Not quite. ') + body;
      }

      /* ----------------------------------------------------------- rounds */

      function newRound() {
        if (deckAt >= deck.length) { deck = buildDeck(); deckAt = 0; }
        round = deck[deckAt++];
        seed = deckAt * 31 + 7;
        picked = null; locked = false;

        frame.textContent = round.frame;
        ask.textContent = round.ask;
        setArrow(round.dir);
        clear(bodies);
        sea.style.display = 'none';

        if (round.dir === 'predict') {
          if (round.spec.sea) sea.style.display = '';
          bodies.appendChild(magmaBody(round.spec, accent + '44', accent, false));
          blankSpecimen();
          btns.forEach(function (b, n) {
            var t = TEXTURES[round.options[n]];
            b.value = t.id;
            b.textContent = t.label;
            b.setAttribute('aria-label', t.label);
          });
        } else {
          drawSpecimen(round.spec.mm, round.spec.groundMm || 0);
          btns.forEach(function (b, n) {
            var id = round.options[n];
            b.value = id;
            b.textContent = S[id].opt;
            b.setAttribute('aria-label', S[id].opt);
          });
        }

        btns.forEach(function (b) {
          b.disabled = false;
          b.setAttribute('aria-pressed', 'false');
          b.classList.remove('is-ans');
        });
        go.textContent = 'Check';
        go.disabled = true;
        cap.className = 'cap rest';
        cap.textContent = round.dir === 'predict'
          ? 'The section shows where this melt sat, and how fast it lost its heat there.'
          : 'Work back from the crystals: how fast did this melt have to lose its heat?';
        pushState();
      }

      function commit() {
        if (picked === null || locked) return;
        locked = true;
        attempted++;
        var ok = picked === round.answer;
        streak = ok ? streak + 1 : 0;
        var justMastered = ok && streak >= 3 && !mastered;
        if (streak >= 3) mastered = true;

        if (round.dir === 'predict') {
          drawSpecimen(round.spec.mm, round.spec.groundMm || 0);
        } else {
          clear(bodies);
          sea.style.display = round.spec.sea ? '' : 'none';
          if (!ok) bodies.appendChild(magmaBody(S[picked], '#d8cfbe', '#2d2a26', true));
          bodies.appendChild(magmaBody(round.spec, accent + '44', accent, false));
        }

        var body = round.dir === 'predict' ? predictMsg(ok, picked) : readMsg(ok, picked);
        if (justMastered) {
          body = 'three in a row, and you have it. Crystal size records cooling rate: deep and slow grows big crystals, fast at the surface freezes tiny ones, and two sizes mean two stages.';
        }
        verdict(ok, body);

        btns.forEach(function (b) {
          b.disabled = true;
          if (b.value === round.answer) b.classList.add('is-ans');
        });
        run.textContent = mastered
          ? (streak === 0 ? 'You have it — that one caught you out.' : 'You have it — keep going if you like.')
          : (streak === 0
            ? (attempted > 1 ? 'Run reset — three in a row to finish.' : '')
            : streak + ' right in a row — ' + (3 - streak) + ' more to go.');
        go.textContent = mastered ? 'Another anyway' : 'Next';
        go.disabled = false;
        pushState({ picked: picked, right: ok });
      }

      /* ---------------------------------------------------------- wiring */

      btns.forEach(function (b) {
        b.addEventListener('click', function () {
          if (locked) return;
          picked = b.value;
          btns.forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
          if (round.dir === 'predict') {
            var t = TEXTURES[picked];
            drawSpecimen(t.mm, t.ground);
            cap.textContent = 'Drawn: ' + t.short + '. Check it against where the melt cooled.';
          } else {
            clear(bodies);
            sea.style.display = S[picked].sea ? '' : 'none';
            bodies.appendChild(magmaBody(S[picked], '#d8cfbe', '#2d2a26', true));
            cap.textContent = 'Marked: ' + WHERE[picked] + ', ' + DUR[picked] + '.';
          }
          cap.className = 'cap rest';
          sr.textContent = cap.textContent;
          go.disabled = false;
          pushState({ picked: picked });
        });
      });

      go.addEventListener('click', function () {
        if (locked) { newRound(); btns[0].focus(); } else { commit(); }
      });

      newRound();
      pushState();
    }
  };
})();
