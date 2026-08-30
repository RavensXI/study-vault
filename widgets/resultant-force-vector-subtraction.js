/* Resultant force: combining forces on one line.
   Self-contained lesson widget. No imports, no network, no storage. */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';
  var CLS = 'svw-rfvs';

  /* ---------------------------------------------------------------- data
     sign: +1 is right (h) or up (v).  Every resultant is computed from
     these figures, never hand-authored.                                */
  var ROUNDS = [
    {
      key: 'tug',
      axis: 'h',
      pos: 'to the right', neg: 'to the left', posS: 'right', negS: 'left',
      frame: 'Two teams pull a rope opposite ways. State the resultant force and the motion.',
      body: { label: 'Marker', state: 'at rest', moving: false, dirSign: 1 },
      forces: [
        { label: 'Red team', n: 500, sign: 1 },
        { label: 'Blue team', n: 300, sign: -1 }
      ],
      extraSizes: [300, 500],
      motions: [
        { k: 'accel-pos', text: 'Accelerates to the right', verb: 'accelerates to the right' },
        { k: 'accel-neg', text: 'Accelerates to the left', verb: 'accelerates to the left' },
        { k: 'still', text: 'Stays still — the pulls cancel', verb: 'stays still' },
        { k: 'steady', text: 'Moves right at a steady speed', verb: 'moves right at a steady speed' }
      ]
    },
    {
      key: 'skydiver',
      axis: 'v',
      pos: 'upwards', neg: 'downwards', posS: 'up', negS: 'down',
      frame: 'A skydiver falls with her parachute open. State the resultant force and her motion.',
      body: { label: 'Skydiver', state: 'falling ↓', moving: true, dirSign: -1 },
      forces: [
        { label: 'Air resistance', n: 700, sign: 1 },
        { label: 'Weight', n: 700, sign: -1 }
      ],
      extraSizes: [700],
      motions: [
        { k: 'faster', text: 'Speeds up as she falls', verb: 'speeds up as she falls' },
        { k: 'slower', text: 'Slows down but keeps falling', verb: 'slows down but keeps falling' },
        { k: 'steady', text: 'Falls at a steady speed', verb: 'falls at a steady speed' },
        { k: 'stop', text: 'Slows down and stops', verb: 'slows down and stops' }
      ]
    },
    {
      key: 'trolley',
      axis: 'h',
      pos: 'to the right', neg: 'to the left', posS: 'right', negS: 'left',
      frame: 'Two students push a trolley the same way. State the resultant force and the motion.',
      body: { label: 'Trolley', state: 'at rest · smooth floor', moving: false, dirSign: 1 },
      forces: [
        { label: 'Ravi', n: 60, sign: 1 },
        { label: 'Mia', n: 40, sign: 1 }
      ],
      extraSizes: [20, 40, 60],
      motions: [
        { k: 'accel-pos', text: 'Accelerates to the right', verb: 'accelerates to the right' },
        { k: 'accel-neg', text: 'Accelerates to the left', verb: 'accelerates to the left' },
        { k: 'still', text: 'Stays still — the pushes cancel', verb: 'stays still' },
        { k: 'steady', text: 'Moves right at a steady speed', verb: 'moves right at a steady speed' }
      ]
    },
    {
      key: 'car',
      axis: 'h',
      pos: 'forwards', neg: 'backwards', posS: 'forwards', negS: 'backwards',
      frame: 'A car drives along a level road. State the resultant force and describe the motion.',
      body: { label: 'Car', state: 'moving →', moving: true, dirSign: 1 },
      forces: [
        { label: 'Driving force', n: 4000, sign: 1 },
        { label: 'Air resistance', n: 1500, sign: -1 },
        { label: 'Friction', n: 500, sign: -1 }
      ],
      extraSizes: [2500, 4000],
      motions: [
        { k: 'faster', text: 'Speeds up', verb: 'speeds up' },
        { k: 'slower', text: 'Slows down', verb: 'slows down' },
        { k: 'steady', text: 'Keeps moving at a steady speed', verb: 'keeps moving at a steady speed' },
        { k: 'stop', text: 'Slows down and stops', verb: 'slows down and stops' }
      ]
    },
    {
      key: 'sledge',
      axis: 'h',
      pos: 'forwards', neg: 'backwards', posS: 'forwards', negS: 'backwards',
      frame: 'Dogs pull a moving sledge across snow. State the resultant force and the motion.',
      body: { label: 'Sledge', state: 'moving →', moving: true, dirSign: 1 },
      forces: [
        { label: 'Dogs', n: 400, sign: 1 },
        { label: 'Friction', n: 250, sign: -1 },
        { label: 'Air resistance', n: 150, sign: -1 }
      ],
      extraSizes: [150, 400],
      motions: [
        { k: 'faster', text: 'Speeds up', verb: 'speeds up' },
        { k: 'slower', text: 'Slows down', verb: 'slows down' },
        { k: 'steady', text: 'Keeps moving at a steady speed', verb: 'keeps moving at a steady speed' },
        { k: 'stop', text: 'Slows down and stops', verb: 'slows down and stops' }
      ]
    },
    {
      key: 'rocket',
      axis: 'v',
      pos: 'upwards', neg: 'downwards', posS: 'up', negS: 'down',
      frame: 'A rocket climbs with its engine firing. State the resultant force and the motion.',
      body: { label: 'Rocket', state: 'climbing ↑', moving: true, dirSign: 1 },
      forces: [
        { label: 'Thrust', n: 3000, sign: 1 },
        { label: 'Weight', n: 2500, sign: -1 }
      ],
      extraSizes: [2500, 3000],
      motions: [
        { k: 'faster', text: 'Speeds up as it climbs', verb: 'speeds up as it climbs' },
        { k: 'slower', text: 'Slows down', verb: 'slows down' },
        { k: 'steady', text: 'Climbs at a steady speed', verb: 'climbs at a steady speed' },
        { k: 'stop', text: 'Slows down and stops', verb: 'slows down and stops' }
      ]
    }
  ];

  /* ------------------------------------------------------------- physics */
  function resultantOf(r) {
    var t = 0;
    for (var i = 0; i < r.forces.length; i++) t += r.forces[i].sign * r.forces[i].n;
    return t;                                   // integer newtons, signed
  }
  function sumOfMagnitudes(r) {
    var t = 0;
    for (var i = 0; i < r.forces.length; i++) t += r.forces[i].n;
    return t;
  }
  function sideTotal(r, sign) {
    var t = 0;
    for (var i = 0; i < r.forces.length; i++) if (r.forces[i].sign === sign) t += r.forces[i].n;
    return t;
  }
  function biggestForce(r) {
    var m = 0;
    for (var i = 0; i < r.forces.length; i++) m = Math.max(m, r.forces[i].n);
    return m;
  }
  function correctMotionKey(r) {
    var res = resultantOf(r);
    if (r.body.moving) {
      var along = res * r.body.dirSign;
      return along > 0 ? 'faster' : (along < 0 ? 'slower' : 'steady');
    }
    return res > 0 ? 'accel-pos' : (res < 0 ? 'accel-neg' : 'still');
  }
  function sizeOptions(r) {
    var out = [];
    [Math.abs(resultantOf(r)), sumOfMagnitudes(r)].forEach(function (v) {
      if (out.indexOf(v) === -1) out.push(v);
    });
    for (var i = 0; i < r.extraSizes.length && out.length < 4; i++) {
      if (out.indexOf(r.extraSizes[i]) === -1) out.push(r.extraSizes[i]);
    }
    out.sort(function (a, b) { return a - b; });
    return out;
  }
  function dirWord(r, res) {
    return res > 0 ? r.pos : (res < 0 ? r.neg : '');
  }

  /* ------------------------------------------------------------- helpers */
  function mk(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function svg(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
    return n;
  }
  function drawArrow(g, x1, y1, x2, y2, colour, w) {
    var dx = x2 - x1, dy = y2 - y1, L = Math.sqrt(dx * dx + dy * dy) || 1;
    var ux = dx / L, uy = dy / L;
    var head = Math.min(9, L * 0.6), hw = 4.6;
    var bx = x2 - ux * head, by = y2 - uy * head;
    g.appendChild(svg('line', {
      x1: x1, y1: y1, x2: bx, y2: by,
      stroke: colour, 'stroke-width': w, 'stroke-linecap': 'round'
    }));
    g.appendChild(svg('polygon', {
      points: [x2, y2, bx - uy * hw, by + ux * hw, bx + uy * hw, by - ux * hw]
        .map(function (v) { return Math.round(v * 10) / 10; }).join(' '),
      fill: colour
    }));
  }
  function label(g, x, y, s, size, fill, weight, anchor) {
    var t = svg('text', {
      x: x, y: y, 'font-size': size, fill: fill,
      'font-family': 'Inter, system-ui, sans-serif',
      'font-weight': weight || 400,
      'text-anchor': anchor || 'middle'
    });
    t.textContent = s;
    g.appendChild(t);
    return t;
  }

  var INK = '#2d2a26', MUTED = '#8d8880', LINE = '#d9d2c6', PAPER = '#faf8f5';

  /* --------------------------------------------------------------- mount */
  window.SVWidget = {
    meta: {
      id: 'resultant-force-vector-subtraction',
      title: 'Combining forces on one line',
      teaches: 'Forces are vectors: forces in opposite directions subtract and forces in the same direction add, and only a non-zero resultant changes the motion.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a3f';
      var reduced = !!ctx.reducedMotion;

      /* ---- style (every selector scoped to the root class) ---- */
      var css = [
        '.' + CLS + '{background:#fff;border:1px solid #e8e3db;border-radius:16px;container-type:inline-size;',
        'padding:clamp(.95rem,3.2vw,1.25rem);color:' + INK + ';box-sizing:border-box;max-width:100%;',
        'font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;}',
        '.' + CLS + ' *{box-sizing:border-box;}',
        '.' + CLS + ' .rf-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--rf-a);}',
        '.' + CLS + ' .rf-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.15rem;line-height:1.2;margin:.16rem 0 .3rem;}',
        '.' + CLS + ' .rf-frame{font-size:.84rem;line-height:1.45;color:#5b564e;margin:0 0 .5rem;}',
        '.' + CLS + ' .rf-stage{background:' + PAPER + ';border:1px solid #efe9e0;border-radius:12px;padding:.3rem .4rem;margin:0 0 .5rem;}',
        '.' + CLS + ' .rf-stage svg{display:block;width:100%;height:auto;max-height:112px;}',
        '.' + CLS + ' .rf-lab{font-size:.72rem;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:' + MUTED + ';margin:0 0 .22rem;}',
        '.' + CLS + ' .rf-sizes{display:flex;flex-wrap:wrap;gap:.34rem;margin:0 0 .45rem;}',
        '.' + CLS + ' .rf-motions{display:grid;grid-template-columns:repeat(auto-fit,minmax(238px,1fr));gap:.26rem;margin:0 0 .45rem;}',
        '.' + CLS + ' .rf-chip{font-family:inherit;font-size:.82rem;font-weight:600;line-height:1.28;color:' + INK + ';',
        'background:' + PAPER + ';border:1px solid #ddd7cd;border-radius:10px;padding:.3rem .64rem;text-align:left;',
        'cursor:pointer;font-variant-numeric:tabular-nums;}',
        '.' + CLS + ' .rf-chip[aria-pressed="true"]{background:' + INK + ';border-color:' + INK + ';color:#fff;}',
        '.' + CLS + ' .rf-chip[disabled]{cursor:default;opacity:.72;}',
        '.' + CLS + ' .rf-chip.rf-key{border-color:var(--rf-a);box-shadow:inset 0 0 0 1px var(--rf-a);}',
        '.' + CLS + ' .rf-row{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;margin:0 0 .4rem;}',
        '.' + CLS + ' .rf-go{font-family:inherit;font-size:.85rem;font-weight:600;background:' + INK + ';color:#fff;',
        'border:1px solid ' + INK + ';border-radius:10px;padding:.48rem 1rem;cursor:pointer;}',
        '.' + CLS + ' .rf-streak{font-size:.78rem;color:' + MUTED + ';}',
        '.' + CLS + ' .rf-cap{font-size:.84rem;line-height:1.45;color:' + INK + ';margin:0;min-height:3.4rem;}',
        '.' + CLS + ' .rf-cap b{font-weight:600;}',
        '@container (min-width:440px){.' + CLS + ' .rf-motions{grid-template-columns:1fr 1fr;}}',
        '.' + CLS + ' .rf-sr{margin:0;position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}',
        '.' + CLS + ' .rf-chip:focus-visible,.' + CLS + ' .rf-go:focus-visible{outline:2px solid var(--rf-a);outline-offset:2px;}'
      ].join('');

      root.className = (root.className ? root.className + ' ' : '') + CLS;
      root.style.setProperty('--rf-a', accent);
      var st = document.createElement('style');
      st.textContent = css;
      root.appendChild(st);

      /* ---- skeleton, built once ---- */
      var kick = mk('div', 'rf-kick', 'Predict');
      var title = mk('h3', 'rf-title', 'Combining forces on one line');
      var frame = mk('p', 'rf-frame', '');
      var stage = mk('div', 'rf-stage');
      var svgEl = svg('svg', { viewBox: '0 0 340 122', preserveAspectRatio: 'xMidYMid meet', role: 'img' });
      stage.appendChild(svgEl);

      var labA = mk('p', 'rf-lab', '1 · Resultant force');
      var sizes = mk('div', 'rf-sizes');
      var labB = mk('p', 'rf-lab', '2 · What the object does');
      var motions = mk('div', 'rf-motions');
      var row = mk('div', 'rf-row');
      var go = mk('button', 'rf-go', 'Check the resultant');
      go.type = 'button';
      var streak = mk('span', 'rf-streak', '');
      row.appendChild(go); row.appendChild(streak);
      var cap = mk('p', 'rf-cap', '');
      var sr = mk('p', 'rf-sr');
      sr.setAttribute('aria-live', 'polite');

      [kick, title, frame, stage, labA, sizes, labB, motions, row, cap, sr]
        .forEach(function (n) { root.appendChild(n); });

      /* ---- state ---- */
      var idx = 0, pickedSize = null, pickedMotion = null, revealed = false;
      var streakN = 0, attempted = 0, mastered = false, lastCorrect = null;

      function r() { return ROUNDS[idx % ROUNDS.length]; }

      function publish() {
        root.dataset.svState = JSON.stringify({
          round: r().key,
          resultant: resultantOf(r()),
          size: pickedSize,
          motion: pickedMotion,
          correct: lastCorrect,
          streak: streakN,
          mastered: mastered,
          attempted: attempted
        });
      }

      /* ---- stage painting ---- */
      function paintStage() {
        while (svgEl.firstChild) svgEl.removeChild(svgEl.firstChild);
        var d = r(), res = resultantOf(d);
        var maxN = Math.max(biggestForce(d), Math.abs(res));
        var g = svg('g', {});
        svgEl.appendChild(g);

        var alt = d.forces.map(function (f) {
          return f.label + ' ' + f.n + ' newtons ' + (f.sign > 0 ? d.pos : d.neg);
        }).join(', ');
        svgEl.setAttribute('aria-label',
          d.body.label + ', ' + d.body.state + '. Forces: ' + alt + '.');

        if (d.axis === 'h') {
          g.appendChild(svg('rect', { x: 142, y: 26, width: 56, height: 46, rx: 10, fill: '#fff', stroke: LINE }));
          label(g, 170, 48, d.body.label, 13, INK, 600);
          label(g, 170, 62, d.body.state, 11, MUTED, 400);

          [1, -1].forEach(function (sign) {
            var list = d.forces.filter(function (f) { return f.sign === sign; });
            var ys = list.length > 1 ? [38, 62] : [49];
            list.forEach(function (f, i) {
              var len = Math.max(16, Math.round(108 * f.n / maxN));
              var y = ys[i];
              var x0 = sign > 0 ? 198 : 142;
              drawArrow(g, x0, y, x0 + sign * len, y, INK, 2.4);
              label(g, sign > 0 ? 336 : 4, y - 8, f.label + ' ' + f.n + ' N', 12, INK, 500,
                sign > 0 ? 'end' : 'start');
            });
          });

          if (revealed) {
            var rg = svg('g', {});
            g.appendChild(rg);
            if (res === 0) {
              rg.appendChild(svg('line', {
                x1: 152, y1: 90, x2: 188, y2: 90, stroke: accent,
                'stroke-width': 3.4, 'stroke-linecap': 'round'
              }));
            } else {
              var rl = Math.max(16, Math.round(108 * Math.abs(res) / maxN));
              drawArrow(rg, 170, 90, 170 + (res > 0 ? rl : -rl), 90, accent, 3.4);
            }
            label(rg, 170, 104, 'Resultant', 11, MUTED, 500);
            label(rg, 170, 118, res === 0 ? '0 N (balanced)' : Math.abs(res) + ' N ' + dirWord(d, res), 12.5, accent, 700);
            if (!reduced) { rg.setAttribute('opacity', '0'); fade(rg); }
          }
        } else {
          g.appendChild(svg('rect', { x: 164, y: 46, width: 72, height: 36, rx: 10, fill: '#fff', stroke: LINE }));
          label(g, 200, 63, d.body.label, 13, INK, 600);
          label(g, 200, 76, d.body.state, 11, MUTED, 400);

          d.forces.forEach(function (f) {
            var len = Math.max(12, Math.round(34 * f.n / maxN));
            var up = f.sign > 0;
            var y0 = up ? 44 : 84;
            drawArrow(g, 200, y0, 200, y0 + (up ? -len : len), INK, 2.4);
            label(g, 216, up ? 22 : 98, f.label, 12, INK, 500, 'start');
            label(g, 216, up ? 35 : 111, f.n + ' N', 12, INK, 500, 'start');
          });

          if (revealed) {
            var vg = svg('g', {});
            g.appendChild(vg);
            if (res === 0) {
              vg.appendChild(svg('line', {
                x1: 52, y1: 66, x2: 88, y2: 66, stroke: accent,
                'stroke-width': 3.4, 'stroke-linecap': 'round'
              }));
            } else {
              var vl = Math.max(12, Math.round(40 * Math.abs(res) / maxN));
              if (res > 0) drawArrow(vg, 70, 88, 70, 88 - vl, accent, 3.4);
              else drawArrow(vg, 70, 44, 70, 44 + vl, accent, 3.4);
            }
            label(vg, 70, 104, 'Resultant', 11, MUTED, 500);
            label(vg, 70, 118, res === 0 ? '0 N (balanced)' : Math.abs(res) + ' N ' + dirWord(d, res), 12.5, accent, 700);
            if (!reduced) { vg.setAttribute('opacity', '0'); fade(vg); }
          }
        }
      }

      var fadeTimer = null;
      function fade(node) {                       // one short reveal, then idle
        if (fadeTimer) { clearTimeout(fadeTimer); fadeTimer = null; }
        node.style.transition = 'opacity .32s ease';
        fadeTimer = setTimeout(function () {
          node.setAttribute('opacity', '1');
          fadeTimer = null;
        }, 20);
      }

      /* ---- controls ---- */
      function buildChoices() {
        while (sizes.firstChild) sizes.removeChild(sizes.firstChild);
        while (motions.firstChild) motions.removeChild(motions.firstChild);
        var d = r();

        sizeOptions(d).forEach(function (n) {
          var b = mk('button', 'rf-chip', n + ' N');
          b.type = 'button';
          b.setAttribute('aria-pressed', 'false');
          b.addEventListener('click', function () {
            if (revealed) return;
            pickedSize = n;
            Array.prototype.forEach.call(sizes.children, function (c) {
              c.setAttribute('aria-pressed', c === b ? 'true' : 'false');
            });
            echo(); publish();
          });
          sizes.appendChild(b);
        });

        d.motions.forEach(function (m) {
          var b = mk('button', 'rf-chip', m.text);
          b.type = 'button';
          b.setAttribute('aria-pressed', 'false');
          b.dataset.k = m.k;
          b.addEventListener('click', function () {
            if (revealed) return;
            pickedMotion = m.k;
            Array.prototype.forEach.call(motions.children, function (c) {
              c.setAttribute('aria-pressed', c === b ? 'true' : 'false');
            });
            echo(); publish();
          });
          motions.appendChild(b);
        });
      }

      function motionByKey(d, k) {
        for (var i = 0; i < d.motions.length; i++) if (d.motions[i].k === k) return d.motions[i];
        return null;
      }
      function setChips(disabled) {
        Array.prototype.forEach.call(sizes.children, function (c) { c.disabled = disabled; });
        Array.prototype.forEach.call(motions.children, function (c) { c.disabled = disabled; });
      }

      function html(s) { cap.innerHTML = s; }

      function echo() {
        var d = r();
        if (pickedSize != null && pickedMotion != null) {
          var m = motionByKey(d, pickedMotion);
          html('Your answer: <b>' + pickedSize + ' N</b>, and the ' +
            d.body.label.toLowerCase() + ' ' + m.verb + '.');
        } else if (pickedSize != null) {
          html('Your answer so far: <b>' + pickedSize + ' N</b>.');
        } else if (pickedMotion != null) {
          html('Your answer so far: the ' + d.body.label.toLowerCase() + ' ' +
            motionByKey(d, pickedMotion).verb + '.');
        }
      }

      /* ---- the working, derived from the figures on the diagram ---- */
      function arith(d) {
        var res = resultantOf(d), out = '';
        d.forces.forEach(function (f) {
          if (f.sign > 0) out += (out ? ' + ' : '') + f.n;
        });
        if (!out) {
          d.forces.forEach(function (f) { out += (out ? ' + ' : '') + f.n; });
          return out + ' = ' + Math.abs(res) + ' N.';
        }
        d.forces.forEach(function (f) { if (f.sign < 0) out += ' − ' + f.n; });
        return out + ' = ' + Math.abs(res) + ' N.';
      }

      function diagnosis(d, sizeOK, motionOK) {
        var res = resultantOf(d), sum = sumOfMagnitudes(d);
        if (!motionOK && pickedMotion === 'stop' && res === 0) {
          return '<b>Zero resultant is not stopping.</b> Nothing is left over to slow it, so it keeps the speed it had.';
        }
        if (!sizeOK && pickedSize === sum && sum !== Math.abs(res)) {
          return 'Adding every number gives ' + sum + ' N — right only when the forces point the same way.';
        }
        if (!sizeOK && sideTotal(d, -1) === 0 &&
          pickedSize === Math.abs(d.forces[0].n - d.forces[1].n)) {
          return 'Subtracting is only right when forces oppose. These both point ' + d.pos + ', so they add.';
        }
        if (!sizeOK && (sideTotal(d, -1) === 0 || sideTotal(d, 1) === 0)) {
          return 'Both act ' + (sideTotal(d, -1) === 0 ? d.posS : d.negS) +
            ', so they <b>add</b> — neither force alone is the resultant.';
        }
        if (!sizeOK && pickedSize === biggestForce(d)) {
          return 'The biggest single force is not the resultant — the forces acting the other way still count.';
        }
        if (!motionOK && (pickedMotion === 'steady' || pickedMotion === 'still') && res !== 0) {
          return 'A resultant force <b>changes</b> the motion. Steady speed needs zero, and ' +
            Math.abs(res) + ' N is left over.';
        }
        if (!motionOK && res === 0) {
          return 'With balanced forces there is nothing left to change the motion.';
        }
        if (!motionOK) {
          return 'The motion always follows the resultant, and here the resultant points ' + dirWord(d, res) + '.';
        }
        if (!sizeOK) {
          return 'Add up each direction separately, then take the difference.';
        }
        return '';
      }

      function principle(d) {
        var res = resultantOf(d);
        if (res === 0 && d.body.moving) {
          return 'Zero resultant means <b>no change in motion</b>: it keeps the speed it already had.';
        }
        if (res === 0) return 'Balanced forces leave it exactly as it was.';
        if (sideTotal(d, -1) === 0 || sideTotal(d, 1) === 0) {
          return 'Same direction, so they <b>add</b> — bigger than either force alone.';
        }
        if (d.forces.length > 2) {
          return 'Three forces, yet the resultant is smaller than the biggest one alone.';
        }
        return 'Opposite directions <b>subtract</b>: the resultant is the difference, not the total.';
      }

      /* ---- commit ---- */
      function check() {
        var d = r(), res = resultantOf(d);
        if (pickedSize == null || pickedMotion == null) {
          html('Pick a size in newtons and what the object does, then check.');
          return;
        }
        var ck = correctMotionKey(d);
        var sizeOK = pickedSize === Math.abs(res);
        var motionOK = pickedMotion === ck;
        var allOK = sizeOK && motionOK;

        revealed = true;
        attempted++;
        lastCorrect = allOK;
        if (allOK) { streakN++; if (streakN >= 3) mastered = true; }
        else streakN = 0;

        var chosen = motionByKey(d, pickedMotion), right = motionByKey(d, ck);
        var who = 'the ' + d.body.label.toLowerCase();
        var out;
        if (allOK) {
          out = '<b>Right —</b> ' + pickedSize + ' N' +
            (res === 0 ? '' : ' ' + dirWord(d, res)) + ', and ' + who + ' ' + right.verb + '. ' +
            arith(d) + ' ' + principle(d);
        } else if (sizeOK) {
          out = '<b>Not quite —</b> your ' + pickedSize + ' N is right, but you said “' +
            chosen.text + '”. It ' + right.verb + '. ' + diagnosis(d, sizeOK, motionOK);
        } else if (motionOK) {
          out = '<b>Not quite —</b> the motion is right, but you said <b>' + pickedSize + ' N</b>. It is ' +
            Math.abs(res) + ' N' + (res === 0 ? '' : ' ' + dirWord(d, res)) + ': ' + arith(d) + ' ' +
            diagnosis(d, sizeOK, motionOK);
        } else {
          out = '<b>Not quite —</b> you said <b>' + pickedSize + ' N</b> and “' + chosen.text +
            '”. It is ' + Math.abs(res) + ' N' + (res === 0 ? '' : ' ' + dirWord(d, res)) +
            ', and it ' + right.verb + '. ' + arith(d) + ' ' + diagnosis(d, sizeOK, motionOK);
        }
        if (mastered && allOK && streakN === 3) {
          out = '<b>Right —</b> three in a row, you have it. Forces on one line: opposite directions subtract, ' +
            'the same direction adds, and a resultant of zero means the motion does not change.';
        }
        html(out);
        sr.textContent = (allOK ? 'Correct. ' : 'Not correct. ') + 'Resultant ' + Math.abs(res) + ' newtons ' +
          (res === 0 ? 'balanced' : dirWord(d, res)) + '.';

        setChips(true);
        Array.prototype.forEach.call(motions.children, function (c) {
          if (c.dataset.k === ck) c.classList.add('rf-key');
        });
        Array.prototype.forEach.call(sizes.children, function (c) {
          if (c.textContent === Math.abs(res) + ' N') c.classList.add('rf-key');
        });
        go.textContent = mastered ? 'Another anyway' : 'Next force diagram';
        paintStage();
        paintStreak();
        publish();
      }

      function paintStreak() {
        if (mastered) streak.textContent = 'Mastered · three in a row';
        else if (streakN === 2) streak.textContent = '2 right in a row — one more and you have it';
        else if (streakN === 1) streak.textContent = '1 right in a row';
        else streak.textContent = '';
      }

      function nextRound() {
        idx++;
        pickedSize = null; pickedMotion = null; revealed = false;
        frame.textContent = r().frame;
        buildChoices();
        paintStage();
        html('A resultant force is the single force with the same effect as all the forces acting together.');
        go.textContent = 'Check the resultant';
        publish();
      }

      go.addEventListener('click', function () {
        if (revealed) nextRound(); else check();
      });

      /* ---- first paint ---- */
      frame.textContent = r().frame;
      buildChoices();
      paintStage();
      html('A resultant force is the single force with the same effect as all the forces acting together.');
      publish();
    }
  };
})();
