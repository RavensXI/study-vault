/* Field lines are a MAP, not a set of rails.
   Every direction, every strength and every distractor in this widget is
   computed from the actual charge configuration at mount time - the field
   lines themselves are traced by integrating the same field function - so
   the reveal cannot drift from the marking. */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';
  var VW = 240, VH = 150, EDGE = 5;

  /* ---------------------------------------------------------------
     1. The physics. E = sum of q*d/|d|^3 (Coulomb, 3-D), or a constant
     vector for the uniform field between parallel plates.
     --------------------------------------------------------------- */
  function fieldAt(p, cfg) {
    if (cfg.uniform) return { x: cfg.uniform.x, y: cfg.uniform.y };
    var ex = 0, ey = 0;
    for (var i = 0; i < cfg.charges.length; i++) {
      var c = cfg.charges[i], dx = p.x - c.x, dy = p.y - c.y;
      var r2 = dx * dx + dy * dy;
      if (r2 < 0.6) r2 = 0.6;
      var k = c.q / (r2 * Math.sqrt(r2));
      ex += k * dx; ey += k * dy;
    }
    return { x: ex, y: ey };
  }
  function magOf(e) { return Math.sqrt(e.x * e.x + e.y * e.y); }
  function unitOf(e) { var m = magOf(e); return m ? { x: e.x / m, y: e.y / m } : null; }

  /* Midpoint-method streamline. dir = +1 follows the field, -1 runs back
     against it (used to draw the lines that end on a lone negative charge). */
  function traceLine(cfg, start, dir) {
    var h = 1.4, pts = [[start.x, start.y]], p = { x: start.x, y: start.y };
    for (var i = 0; i < 900; i++) {
      var n1 = unitOf(fieldAt(p, cfg)); if (!n1) break;
      var mid = { x: p.x + dir * h * 0.5 * n1.x, y: p.y + dir * h * 0.5 * n1.y };
      var n2 = unitOf(fieldAt(mid, cfg)); if (!n2) break;
      p = { x: p.x + dir * h * n2.x, y: p.y + dir * h * n2.y };
      pts.push([p.x, p.y]);
      if (p.x < EDGE || p.x > VW - EDGE || p.y < EDGE || p.y > VH - EDGE) break;
      var hit = false;
      for (var j = 0; j < cfg.charges.length; j++) {
        var c = cfg.charges[j];
        if (Math.sqrt((p.x - c.x) * (p.x - c.x) + (p.y - c.y) * (p.y - c.y)) < 7.5) { hit = true; break; }
      }
      if (hit) break;
    }
    return dir > 0 ? pts : pts.reverse();   /* always stored in field-flow order */
  }

  var LINECACHE = {};
  function linesFor(key) {
    if (LINECACHE[key]) return LINECACHE[key];
    var cfg = CONFIGS[key], out = [], i, k;
    if (cfg.uniform) {
      for (i = 0; i < cfg.plateX.length; i++) {
        var col = [], y0 = cfg.plateTop + 3, y1 = cfg.plateBot - 3;
        for (k = 0; k <= 12; k++) col.push([cfg.plateX[i], y0 + k * (y1 - y0) / 12]);
        out.push(col);
      }
    } else {
      var allNeg = true;
      for (i = 0; i < cfg.charges.length; i++) if (cfg.charges[i].q > 0) allNeg = false;
      for (i = 0; i < cfg.charges.length; i++) {
        var c = cfg.charges[i];
        if (c.q < 0 && !allNeg) continue;           /* lines already arrive from the + charge */
        for (k = 0; k < cfg.seeds; k++) {
          var a = ((cfg.seedOffset || 0) + k * 360 / cfg.seeds) * Math.PI / 180;
          var s = { x: c.x + 11 * Math.cos(a), y: c.y + 11 * Math.sin(a) };
          out.push(traceLine(cfg, s, c.q > 0 ? 1 : -1));
        }
      }
    }
    LINECACHE[key] = out;
    return out;
  }

  function nearestOnLines(P, ls) {
    var best = 1e9, bp = null;
    for (var i = 0; i < ls.length; i++) {
      var l = ls[i];
      for (var j = 0; j < l.length; j++) {
        var dx = l[j][0] - P.x, dy = l[j][1] - P.y, d = Math.sqrt(dx * dx + dy * dy);
        if (d < best) { best = d; bp = l[j]; }
      }
    }
    return { d: best, p: bp };
  }

  /* ---------------------------------------------------------------
     2. Directions in words. Screen coordinates: y grows downwards.
     --------------------------------------------------------------- */
  var WORDS = ['Right', 'Up & right', 'Up', 'Up & left', 'Left', 'Down & left', 'Down', 'Down & right'];
  var PHRASE = ['to the right', 'up and to the right', 'straight up', 'up and to the left',
                'to the left', 'down and to the left', 'straight down', 'down and to the right'];
  function compassIndex(v) {
    var a = Math.atan2(-v.y, v.x) * 180 / Math.PI;
    if (a < 0) a += 360;
    return Math.round(a / 45) % 8;
  }

  /* ---------------------------------------------------------------
     3. The configurations and the round pool.
     --------------------------------------------------------------- */
  var CONFIGS = {
    pos: { charges: [{ x: 120, y: 75, q: 1 }], seeds: 12, seedOffset: 0,
           scene: 'a positive charged sphere' },
    neg: { charges: [{ x: 120, y: 75, q: -1 }], seeds: 12, seedOffset: 0,
           scene: 'a negative charged sphere' },
    dip: { charges: [{ x: 74, y: 75, q: 1 }, { x: 166, y: 75, q: -1 }], seeds: 10, seedOffset: 0,
           scene: 'two opposite charges' },
    pla: { uniform: { x: 0, y: 1 }, charges: [], plateX: [42, 74, 106, 138, 170, 202],
           plateTop: 32, plateBot: 120, scene: 'two parallel charged plates' }
  };

  /* The mechanism sentence, keyed by configuration and the sign of the test charge. */
  var WHY = {
    'pos+': 'Field lines point away from a positive charge, and P sits in a gap where the field is every bit as real as on a line.',
    'pos-': 'The arrows point away from the positive sphere, and a negative charge is pushed the opposite way to the arrow — back towards it.',
    'neg+': 'Field lines point in towards a negative charge, so a positive test charge is pulled the same way the arrow points.',
    'neg-': 'The arrows point in towards the negative sphere, and a negative charge is pushed the opposite way to the arrow, so outwards.',
    'dip+': 'Between the spheres the field runs from the positive charge to the negative one, gaps between the lines included.',
    'dip-': 'The field runs from the positive sphere to the negative one, and a negative charge is pushed against the arrows.',
    'pla+': 'Between parallel plates the field is uniform: one direction and one strength everywhere, gaps included.',
    'pla-': 'The field runs from the positive plate to the negative one, and a negative charge is pushed against the arrows.'
  };

  var P45 = 45 / Math.SQRT2;   /* 45 degrees out, at radius 45 - exactly mid-gap */
  var P42 = 42 / Math.SQRT2;
  var D2R = Math.PI / 180;

  var ROUNDS = [
    { t: 'dir', c: 'pos', p: { x: 120 + P45, y: 75 - P45 }, q: 1 },
    { t: 'dir', c: 'pos', p: { x: 120 - P45, y: 75 - P45 }, q: -1 },
    { t: 'dir', c: 'neg', p: { x: 120 + P45, y: 75 + P45 }, q: 1 },
    { t: 'dir', c: 'neg', p: { x: 120 - P45, y: 75 - P45 }, q: -1 },
    { t: 'dir', c: 'dip', p: { x: 120, y: 42 }, q: 1 },
    { t: 'dir', c: 'dip', p: { x: 120, y: 108 }, q: -1 },
    { t: 'dir', c: 'pla', p: { x: 88, y: 75 }, q: 1 },
    { t: 'dir', c: 'pla', p: { x: 148, y: 60 }, q: -1 },
    { t: 'str', c: 'pos', pts: [{ x: 120 + 30 / Math.SQRT2, y: 75 - 30 / Math.SQRT2 },
                                { x: 120 - 62 * Math.cos(15 * D2R), y: 75 + 62 * Math.sin(15 * D2R) },
                                { x: 120 + 45 * Math.cos(105 * D2R), y: 75 - 45 * Math.sin(105 * D2R) }] },
    { t: 'str', c: 'pos', pts: [{ x: 120 + 42 * Math.cos(30 * D2R), y: 75 - 42 * Math.sin(30 * D2R) },
                                { x: 120 + P42, y: 75 + P42 },
                                { x: 120 - 42 * Math.cos(15 * D2R), y: 75 + 42 * Math.sin(15 * D2R) }] },
    { t: 'str', c: 'pla', pts: [{ x: 58, y: 46 }, { x: 88, y: 75 }, { x: 186, y: 104 }] },
    { t: 'str', c: 'dip', pts: [{ x: 178, y: 64 }, { x: 120, y: 42 }, { x: 214, y: 24 }] }
  ];

  function shuffled(n) {
    var a = [], i, j, t;
    for (i = 0; i < n; i++) a.push(i);
    for (i = n - 1; i > 0; i--) { j = Math.floor(Math.random() * (i + 1)); t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  /* ---------------------------------------------------------------
     4. Build one round. Everything derived, nothing hand-authored.
     --------------------------------------------------------------- */
  function buildRound(def) {
    var cfg = CONFIGS[def.c], ls = linesFor(def.c);
    var R = { def: def, cfg: cfg, lines: ls, kind: def.t }, i;

    if (def.t === 'dir') {
      var u = unitOf(fieldAt(def.p, cfg));
      var f = { x: u.x * def.q, y: u.y * def.q };            /* force on the test charge */
      var opp = { x: -f.x, y: -f.y };
      var pA = { x: -f.y, y: f.x }, pB = { x: f.y, y: -f.x };
      var nl = nearestOnLines(def.p, ls);
      var tox = { x: nl.p[0] - def.p.x, y: nl.p[1] - def.p.y };
      var perp = (pA.x * tox.x + pA.y * tox.y) >= (pB.x * tox.x + pB.y * tox.y) ? pA : pB;

      R.point = def.p; R.force = f; R.gap = nl.d;
      R.answer = 'right';
      var pool = [{ key: 'right', vec: f }, { key: 'opposite', vec: opp },
                  { key: 'onto', vec: perp }, { key: 'none' }];
      var order = shuffled(4);
      R.options = [];
      for (i = 0; i < 4; i++) R.options.push(pool[order[i]]);
      for (i = 0; i < R.options.length; i++) {
        var o = R.options[i];
        if (o.vec) {
          var ix = compassIndex(o.vec);
          o.label = WORDS[ix]; o.phrase = PHRASE[ix]; o.glyph = 'arrow';
        } else {
          o.label = 'Nothing pushes it'; o.phrase = 'nothing pushes it'; o.glyph = 'dot';
        }
      }
      var sign = def.q > 0 ? 'positive' : 'negative';
      R.ask = def.c === 'pla'
        ? 'The map shows the field between two charged plates. A tiny ' + sign + ' charge is placed at P. Which way is it pushed?'
        : 'The map shows the electric field around ' + cfg.scene + '. A tiny ' + sign + ' charge is placed at P. Which way is it pushed?';
      R.why = WHY[def.c + (def.q > 0 ? '+' : '-')];
    } else {
      var labels = ['A', 'B', 'C'], ord = shuffled(3), marks = [];
      for (i = 0; i < 3; i++) {
        var pt = def.pts[ord[i]];
        marks.push({ p: pt, label: labels[i], m: magOf(fieldAt(pt, cfg)),
                     onLine: nearestOnLines(pt, ls).d < 3 });
      }
      var hi = marks[0], lo = marks[0];
      for (i = 1; i < 3; i++) { if (marks[i].m > hi.m) hi = marks[i]; if (marks[i].m < lo.m) lo = marks[i]; }
      R.marks = marks;
      R.same = (hi.m - lo.m) / hi.m < 1e-9;   /* equal by construction, not by luck */
      R.best = hi;
      R.answer = R.same ? 'same' : hi.label;
      R.options = [];
      var byLabel = marks.slice().sort(function (a, b) { return a.label < b.label ? -1 : 1; });
      for (i = 0; i < 3; i++) {
        R.options.push({ key: byLabel[i].label, label: 'Point ' + byLabel[i].label,
                         phrase: 'point ' + byLabel[i].label, glyph: byLabel[i].label });
      }
      R.options.push({ key: 'same', label: 'Just the same', phrase: 'just the same', glyph: '=' });
      R.ask = def.c === 'pla'
        ? 'Three points are marked between two charged plates. Where is the field strongest?'
        : def.c === 'dip'
          ? 'Three points are marked on the field map of two opposite charges. Where is the field strongest?'
          : 'Three points are marked on the field map around ' + cfg.scene + '. Where is the field strongest?';
    }
    return R;
  }

  /* ---------------------------------------------------------------
     5. Feedback: verdict first, the student's own answer echoed back.
     --------------------------------------------------------------- */
  var MASTERY = 'Three in a row, so you have it: the arrow gives the push on a positive charge, the spacing gives the strength, and the field fills the gaps too.';

  function strengthWhy(R) {
    if (R.same) {
      if (R.def.c === 'pla') return 'The lines stay parallel and evenly spaced between the plates, so the field is uniform — the same strength everywhere.';
      return 'All three sit the same distance from the sphere, so the field is identical. One of them happens to lie on a drawn line, which changes nothing.';
    }
    return 'The lines are closest together there, and closer lines mean a stronger field.';
  }

  function feedback(R, chosenKey, mastered) {
    var i, chosen = null, correct = null;
    for (i = 0; i < R.options.length; i++) {
      if (R.options[i].key === chosenKey) chosen = R.options[i];
      if (R.options[i].key === R.answer) correct = R.options[i];
    }
    var ok = chosenKey === R.answer;
    var head = '<b>' + (ok ? 'Right' : 'Not quite') + '</b> — ';

    if (ok) {
      return head + chosen.phrase + '. ' +
        (mastered ? MASTERY : (R.kind === 'dir' ? R.why : strengthWhy(R)));
    }

    if (R.kind === 'dir') {
      if (chosenKey === 'none') {
        return head + 'you said nothing pushes it. The drawn lines are only a sample — the field fills the gaps between them just as strongly. At P the push is ' + correct.phrase + '.';
      }
      if (chosenKey === 'onto') {
        return head + 'you said ' + chosen.phrase + ', which points straight at the nearest line. A field line is not a rail and nothing slides onto it. The push at P is ' + correct.phrase + '.';
      }
      if (R.def.q < 0) {
        return head + 'you said ' + chosen.phrase + ', the way the arrows point. An arrow gives the push on a <b>positive</b> charge, so a negative one goes the opposite way, ' + correct.phrase + '.';
      }
      return head + 'you said ' + chosen.phrase + ', straight against the arrows. The arrow at a point <b>is</b> the push on a positive charge, so it is ' + correct.phrase + '.';
    }

    if (R.same) {
      var picked = null;
      for (i = 0; i < R.marks.length; i++) if (R.marks[i].label === chosenKey) picked = R.marks[i];
      if (R.def.c === 'pla') {
        return head + 'you said ' + chosen.phrase + '. The lines stay parallel and evenly spaced between the plates, so the field is uniform. Being nearer a plate changes nothing.';
      }
      if (picked && picked.onLine) {
        return head + 'you said ' + chosen.phrase + ', the one sitting on a drawn line. All three are the same distance from the sphere, so the field is the same at each. A line is only where we chose to draw.';
      }
      return head + 'you said ' + chosen.phrase + '. All three sit the same distance from the sphere, so the spacing around them matches and the field is the same at each.';
    }
    if (chosenKey === 'same') {
      return head + 'you said just the same. Look at the spacing: the lines bunch together at ' + R.best.label +
             ' and spread apart elsewhere, and that spacing <b>is</b> the strength.';
    }
    return head + 'you said ' + chosen.phrase + ', where the lines have spread apart. Closer lines mean a stronger field, so it is strongest at ' + R.best.label + '.';
  }

  /* ---------------------------------------------------------------
     6. Drawing.
     --------------------------------------------------------------- */
  function mk(tag, attrs) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) e.setAttribute(k, attrs[k]);
    return e;
  }
  function polyPoint(pts, frac) {
    var total = 0, i, seg = [];
    for (i = 1; i < pts.length; i++) {
      var dx = pts[i][0] - pts[i - 1][0], dy = pts[i][1] - pts[i - 1][1];
      var d = Math.sqrt(dx * dx + dy * dy);
      seg.push(d); total += d;
    }
    if (!total) return null;
    var want = total * frac, run = 0;
    for (i = 0; i < seg.length; i++) {
      if (run + seg[i] >= want) {
        var t = seg[i] ? (want - run) / seg[i] : 0;
        return {
          x: pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t,
          y: pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t,
          tx: (pts[i + 1][0] - pts[i][0]) / (seg[i] || 1),
          ty: (pts[i + 1][1] - pts[i][1]) / (seg[i] || 1),
          len: total
        };
      }
      run += seg[i];
    }
    return null;
  }
  function arrowHead(x, y, tx, ty, size, fill) {
    var nx = -ty, ny = tx, w = size * 0.55;
    return mk('polygon', {
      points: (x + tx * size) + ',' + (y + ty * size) + ' ' +
              (x - tx * size * 0.35 + nx * w) + ',' + (y - ty * size * 0.35 + ny * w) + ' ' +
              (x - tx * size * 0.35 - nx * w) + ',' + (y - ty * size * 0.35 - ny * w),
      fill: fill
    });
  }
  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

  function drawScene(scene, R, accent) {
    clear(scene);
    var cfg = R.cfg, i, k;

    if (cfg.uniform) {
      scene.appendChild(mk('rect', { x: 28, y: cfg.plateTop - 6, width: 184, height: 6,
                                     fill: '#e3ddd1', stroke: '#c8bfae', 'stroke-width': 1 }));
      scene.appendChild(mk('rect', { x: 28, y: cfg.plateBot, width: 184, height: 6,
                                     fill: '#e3ddd1', stroke: '#c8bfae', 'stroke-width': 1 }));
      for (k = 0; k < 5; k++) {
        var px = 48 + k * 36;
        var tp = mk('text', { x: px, y: cfg.plateTop - 1.4, 'text-anchor': 'middle',
                              'font-size': 9, 'font-weight': 700, fill: '#5b564e' });
        tp.textContent = '+'; scene.appendChild(tp);
        var tn = mk('text', { x: px, y: cfg.plateBot + 4.8, 'text-anchor': 'middle',
                              'font-size': 9, 'font-weight': 700, fill: '#5b564e' });
        tn.textContent = '−'; scene.appendChild(tn);
      }
    }

    for (i = 0; i < R.lines.length; i++) {
      var pts = R.lines[i], d = 'M' + pts[0][0].toFixed(1) + ' ' + pts[0][1].toFixed(1);
      for (k = 1; k < pts.length; k++) d += 'L' + pts[k][0].toFixed(1) + ' ' + pts[k][1].toFixed(1);
      scene.appendChild(mk('path', { d: d, fill: 'none', stroke: '#b3aa9c',
                                     'stroke-width': 1.1, 'stroke-linecap': 'round' }));
      var probe = polyPoint(pts, 0.5);
      var fracs = (probe && probe.len > 70) ? [0.32, 0.72] : [0.5];
      for (k = 0; k < fracs.length; k++) {
        var a = polyPoint(pts, fracs[k]);
        if (a) scene.appendChild(arrowHead(a.x, a.y, a.tx, a.ty, 4.6, '#b3aa9c'));
      }
    }

    for (i = 0; i < cfg.charges.length; i++) {
      var c = cfg.charges[i];
      scene.appendChild(mk('circle', { cx: c.x, cy: c.y, r: 11, fill: '#fff',
                                       stroke: '#2d2a26', 'stroke-width': 1.6 }));
      var s = mk('text', { x: c.x, y: c.y, dy: '0.36em', 'text-anchor': 'middle',
                           'font-size': 15, 'font-weight': 700, fill: '#2d2a26' });
      s.textContent = c.q > 0 ? '+' : '−';
      scene.appendChild(s);
    }

    var marks = R.kind === 'dir' ? [{ p: R.point, label: 'P' }] : R.marks;
    for (i = 0; i < marks.length; i++) {
      var m = marks[i];
      scene.appendChild(mk('circle', { cx: m.p.x, cy: m.p.y, r: 4.4, fill: '#fff',
                                       stroke: accent, 'stroke-width': 2.2 }));
      var lx = m.p.x + (m.p.x > VW - 26 ? -10 : 9);
      var ly = m.p.y + (m.p.y < 20 ? 14 : -7);
      var lt = mk('text', { x: lx, y: ly, 'text-anchor': 'middle', 'font-size': 11,
                            'font-weight': 700, fill: '#2d2a26', stroke: '#faf8f5',
                            'stroke-width': 2.6, 'paint-order': 'stroke' });
      lt.textContent = m.label;
      scene.appendChild(lt);
      if (R.kind === 'dir') R.labelEl = lt;
    }
  }

  function drawReveal(layer, R, accent) {
    clear(layer);
    if (R.kind === 'dir') {
      var f = R.force, P = R.point;
      /* start clear of the marker so the arrow reads as a push on the charge */
      var x0 = P.x + f.x * 6.5, y0 = P.y + f.y * 6.5, x1 = P.x + f.x * 30, y1 = P.y + f.y * 30;
      layer.appendChild(mk('line', { x1: x0, y1: y0, x2: x1, y2: y1,
                                     stroke: accent, 'stroke-width': 2.6, 'stroke-linecap': 'round' }));
      layer.appendChild(arrowHead(x1, y1, f.x, f.y, 6, accent));
      /* only now - moving it earlier would hint at the answer */
      if (R.labelEl) {
        R.labelEl.setAttribute('x', P.x - f.x * 12);
        R.labelEl.setAttribute('y', P.y - f.y * 12 + 3.6);
      }
    } else {
      for (var i = 0; i < R.marks.length; i++) {
        var m = R.marks[i];
        if (R.same || m === R.best) {
          layer.appendChild(mk('circle', { cx: m.p.x, cy: m.p.y, r: 9.5, fill: 'none',
                                           stroke: accent, 'stroke-width': 2 }));
        }
      }
    }
  }

  function glyph(box, kind, vec) {
    clear(box);
    if (kind === 'arrow') {
      var rot = Math.atan2(vec.y, vec.x) * 180 / Math.PI;
      var g = mk('g', { transform: 'rotate(' + rot.toFixed(1) + ' 11 11)' });
      g.appendChild(mk('line', { x1: 3.5, y1: 11, x2: 14.5, y2: 11, stroke: 'currentColor',
                                 'stroke-width': 2, 'stroke-linecap': 'round' }));
      g.appendChild(mk('polygon', { points: '19.5,11 13.5,7.6 13.5,14.4', fill: 'currentColor' }));
      box.appendChild(g);
    } else if (kind === 'dot') {
      box.appendChild(mk('circle', { cx: 11, cy: 11, r: 3.6, fill: 'currentColor' }));
    } else {
      box.appendChild(mk('circle', { cx: 11, cy: 11, r: 8.2, fill: 'none',
                                     stroke: 'currentColor', 'stroke-width': 1.5 }));
      var t = mk('text', { x: 11, y: 11, dy: '0.36em', 'text-anchor': 'middle',
                           'font-size': 10.5, 'font-weight': 700, fill: 'currentColor' });
      t.textContent = kind;
      box.appendChild(t);
    }
  }

  /* ---------------------------------------------------------------
     7. Style. Every selector scoped to .svw-flm.
     --------------------------------------------------------------- */
  var CSS = [
    '.svw-flm{position:relative;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;padding:0}',
    '.svw-flm *{box-sizing:border-box}',
    '.svw-flm .kick{margin:0 0 .16rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:ACCENT}',
    '.svw-flm .ttl{margin:0 0 .3rem;font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.2}',
    '.svw-flm .ask{margin:0 0 .55rem;font-size:.86rem;line-height:1.45;color:#3c3831}',
    '.svw-flm .stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:5px;max-width:330px;margin:0 auto .6rem}',
    '.svw-flm .stage svg{display:block;width:100%;height:184px}',
    '.svw-flm .opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:7px;margin:0 0 .55rem}',
    '.svw-flm .opt{display:flex;align-items:center;gap:.5rem;min-height:42px;padding:.42rem .6rem;font-family:inherit;font-size:.8rem;font-weight:600;line-height:1.25;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;cursor:pointer;text-align:left}',
    '.svw-flm .opt svg{flex:0 0 auto;color:inherit}',
    '.svw-flm .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-flm .opt[disabled]{cursor:default}',
    '.svw-flm .opt:focus-visible{outline:2px solid ACCENT;outline-offset:2px}',
    '.svw-flm.anim .opt{transition:background-color .14s ease,color .14s ease}',
    '.svw-flm .bar{display:flex;align-items:center;gap:.6rem;margin:0 0 .55rem}',
    '.svw-flm .run{flex:1 1 auto;font-size:.76rem;line-height:1.3;color:#5b564e;font-variant-numeric:tabular-nums}',
    '.svw-flm .run.done{color:#4f7d63;font-weight:600}',
    '.svw-flm .go{flex:0 0 auto;font-family:inherit;font-size:.82rem;font-weight:600;line-height:1;padding:.55rem 1rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-flm .go[disabled]{opacity:.38;cursor:default}',
    '.svw-flm .go:focus-visible{outline:2px solid ACCENT;outline-offset:2px}',
    '.svw-flm .cap{margin:0;min-height:2.4rem;font-size:.82rem;line-height:1.5;color:#3c3831;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.55rem .7rem}',
    '.svw-flm .cap.empty{background:transparent;border-color:transparent}',
    '.svw-flm .sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}'
  ].join('');

  /* ---------------------------------------------------------------
     8. Mount.
     --------------------------------------------------------------- */
  window.SVWidget = {
    meta: {
      id: 'field-lines-as-maps-not-paths',
      title: 'Reading a field map',
      teaches: 'Field lines map the direction of the force on a positive charge, and their spacing maps the strength. They are not rails, and the space between them is not empty.'
    },
    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;

      root.className = 'svw-flm' + (reduced ? '' : ' anim');
      clear(root);

      var style = document.createElement('style');
      style.textContent = CSS.replace(/ACCENT/g, accent);
      root.appendChild(style);

      function div(cls, tag) { var e = document.createElement(tag || 'div'); e.className = cls; return e; }

      var kick = div('kick', 'p'); kick.textContent = 'Electric fields';
      var ttl = div('ttl', 'h3'); ttl.textContent = 'Reading a field map';
      var ask = div('ask', 'p');
      root.appendChild(kick); root.appendChild(ttl); root.appendChild(ask);

      var stage = div('stage');
      var svg = mk('svg', { viewBox: '0 0 ' + VW + ' ' + VH,
                            preserveAspectRatio: 'xMidYMid meet', role: 'img' });
      var svgTitle = mk('title', {});
      var scene = mk('g', {}), layer = mk('g', {});
      svg.appendChild(svgTitle); svg.appendChild(scene); svg.appendChild(layer);
      stage.appendChild(svg); root.appendChild(stage);

      var opts = div('opts');
      var buttons = [];
      for (var b = 0; b < 4; b++) {
        var btn = document.createElement('button');
        btn.className = 'opt'; btn.type = 'button'; btn.setAttribute('aria-pressed', 'false');
        var gbox = mk('svg', { viewBox: '0 0 22 22', width: 22, height: 22, 'aria-hidden': 'true' });
        var lab = document.createElement('span');
        btn.appendChild(gbox); btn.appendChild(lab);
        btn._g = gbox; btn._l = lab;
        opts.appendChild(btn); buttons.push(btn);
      }
      root.appendChild(opts);

      var bar = div('bar');
      var run = div('run', 'span');
      var go = document.createElement('button');
      go.className = 'go'; go.type = 'button'; go.textContent = 'Check';
      bar.appendChild(run); bar.appendChild(go); root.appendChild(bar);

      var cap = div('cap empty', 'p');
      var sr = div('sr', 'p'); sr.setAttribute('aria-live', 'polite');
      root.appendChild(cap); root.appendChild(sr);

      /* ---- state ---- */
      var queue = [], lastIdx = -1, R = null, chosen = null, phase = 'ask';
      var streak = 0, attempted = 0, mastered = false;

      function nextDef() {
        if (!queue.length) {
          queue = shuffled(ROUNDS.length);
          if (queue[0] === lastIdx && queue.length > 1) {
            var t = queue[0]; queue[0] = queue[1]; queue[1] = t;
          }
        }
        lastIdx = queue.shift();
        return ROUNDS[lastIdx];
      }

      function publish() {
        root.dataset.svState = JSON.stringify({
          round: R ? (R.kind + ':' + R.def.c + (R.kind === 'dir' ? (R.def.q > 0 ? ':+' : ':-') : '')) : null,
          phase: phase,
          chosen: chosen,
          answer: R ? R.answer : null,
          correct: phase === 'done' ? (chosen === R.answer) : null,
          streak: streak, mastered: mastered, attempted: attempted
        });
      }

      function describe() {
        if (!R) return '';
        if (R.kind === 'dir') {
          var rel;
          if (R.cfg.uniform) {
            rel = 'in the space between two lines, midway between the plates';
          } else {
            var c = R.cfg.charges[0];
            rel = 'in the gap between two lines, ' +
                  PHRASE[compassIndex({ x: R.point.x - c.x, y: R.point.y - c.y })] + ' of the charge';
          }
          return 'Diagram: field lines around ' + R.cfg.scene + '. Point P lies ' + rel + '.';
        }
        var s = 'Diagram: field lines around ' + R.cfg.scene + '. ';
        for (var i = 0; i < R.marks.length; i++) {
          s += 'Point ' + R.marks[i].label +
               (R.marks[i].onLine ? ' sits on a drawn line. ' : ' sits in a gap between lines. ');
        }
        return s;
      }

      function runLine() {
        if (mastered) return 'Mastered — another if you like.';
        if (streak === 1) return '1 right in a row — two more to go.';
        if (streak === 2) return '2 in a row — one more and you have it.';
        return '';
      }

      function setRound() {
        R = buildRound(nextDef());
        chosen = null; phase = 'ask';
        ask.textContent = R.ask;
        svgTitle.textContent = describe();
        drawScene(scene, R, accent);
        clear(layer);
        for (var i = 0; i < buttons.length; i++) {
          var o = R.options[i], bt = buttons[i];
          bt._l.textContent = o.label;
          bt.setAttribute('aria-pressed', 'false');
          bt.dataset.key = o.key;
          bt.disabled = false;
          glyph(bt._g, o.glyph, o.vec);
        }
        cap.className = 'cap empty'; cap.textContent = '';
        go.textContent = 'Check';
        go.disabled = true;
        run.className = 'run' + (mastered ? ' done' : '');
        run.textContent = runLine();
        sr.textContent = R.ask + ' ' + describe();
        publish();
      }

      function pick(key) {
        if (phase === 'done') return;
        chosen = key;
        for (var i = 0; i < buttons.length; i++) {
          buttons[i].setAttribute('aria-pressed', buttons[i].dataset.key === key ? 'true' : 'false');
        }
        go.disabled = false;
        publish();
      }

      function commit() {
        if (!chosen) return;
        var ok = chosen === R.answer;
        var hadRun = streak > 0;
        attempted++;
        streak = ok ? streak + 1 : 0;
        var hitThree = ok && streak >= 3;
        if (hitThree) mastered = true;
        phase = 'done';
        drawReveal(layer, R, accent);
        cap.className = 'cap';
        cap.innerHTML = feedback(R, chosen, hitThree);
        var onOption = false;
        for (var i = 0; i < buttons.length; i++) {
          if (document.activeElement === buttons[i]) onOption = true;
          buttons[i].disabled = true;
        }
        if (onOption) go.focus();     /* never strand focus on a disabled button */
        run.className = 'run' + (mastered ? ' done' : '');
        run.textContent = mastered ? 'Mastered — another if you like.'
          : (streak ? runLine() : (hadRun ? 'Run reset — three in a row ends it.' : ''));
        go.textContent = mastered ? 'Another anyway' : 'Next';
        go.disabled = false;
        sr.textContent = cap.textContent;
        publish();
      }

      for (var q = 0; q < buttons.length; q++) {
        (function (bt) {
          bt.addEventListener('click', function () { pick(bt.dataset.key); });
        })(buttons[q]);
      }
      go.addEventListener('click', function () {
        if (phase === 'done') { setRound(); go.focus(); } else { commit(); }
      });
      root.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && phase === 'ask' && chosen) {
          chosen = null;
          for (var i = 0; i < buttons.length; i++) buttons[i].setAttribute('aria-pressed', 'false');
          go.disabled = true;
          publish();
        }
      });

      setRound();
    }
  };
})();
