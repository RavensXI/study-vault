/* collision-theory-energy-distribution
   One model, one stage. The curve drawn on screen IS the model: every
   percentage and every multiplier in the feedback is read off the same
   sampled distribution that is painted, so the reveal counts rather than
   asserts.

   Energy is carried in units of RT for the starting mixture, so the axis
   is deliberately unnumbered - the exam claim is about shape and share,
   not about kilojoules. */
(function () {
  'use strict';

  var SVGNS = 'http://www.w3.org/2000/svg';
  var XMAX = 8;        /* right-hand edge of the drawn energy axis */
  var NP = 161;        /* samples used for BOTH the path and the areas */
  var EA0 = 3.6;       /* activation energy of the uncatalysed reaction */

  /* ---- the model -------------------------------------------------- */

  /* number of particles at energy E, for temperature t (x starting T)
     and particle count N. Shape sqrt(E) * exp(-E/t), normalised so the
     area under the whole curve is N. */
  function curve(t, N) {
    var k = N * (2 / Math.sqrt(Math.PI)) * Math.pow(t, -1.5);
    var pts = [], i, E;
    for (i = 0; i < NP; i++) {
      E = XMAX * i / (NP - 1);
      pts.push([E, k * Math.sqrt(E) * Math.exp(-E / t)]);
    }
    return pts;
  }

  /* area under the sampled curve to the right of x0 (trapezium) */
  function areaFrom(pts, x0) {
    var a = 0, i, xA, xB, yA, yB, xs, ys;
    for (i = 1; i < pts.length; i++) {
      xA = pts[i - 1][0]; xB = pts[i][0];
      if (xB <= x0) continue;
      yA = pts[i - 1][1]; yB = pts[i][1];
      xs = xA > x0 ? xA : x0;
      ys = yA + (yB - yA) * (xs - xA) / (xB - xA);
      a += (ys + yB) / 2 * (xB - xs);
    }
    return a;
  }

  function yAt(pts, x0) {
    var i;
    for (i = 1; i < pts.length; i++) {
      if (pts[i][0] >= x0) {
        return pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) *
          (x0 - pts[i - 1][0]) / (pts[i][0] - pts[i - 1][0]);
      }
    }
    return 0;
  }

  function peakOf(pts) {
    var m = 0, i;
    for (i = 0; i < pts.length; i++) { if (pts[i][1] > m) m = pts[i][1]; }
    return m;
  }

  /* Bands. Integer-exact cases (a catalyst leaves the collision count at
     exactly 1, doubling leaves the share at exactly 1) land dead centre
     of 'same'; every other round sits at least 0.15 clear of a boundary. */
  function band(m) {
    if (Math.abs(m - 1) <= 0.01) return 'same';
    if (m < 1) return 'down';
    return m < 1.5 ? 'up-small' : 'up-big';
  }

  var ROUNDS = [
    { key: 'warm',   change: 'You now warm it.',
      t: 1.35, N: 1,   ea: 1,    type: 'temp' },
    { key: 'conc2',  change: 'You now double the concentration of one reactant.',
      t: 1,    N: 2,   ea: 1,    type: 'conc' },
    { key: 'cat',    change: 'You now stir in a catalyst.',
      t: 1,    N: 1,   ea: 0.65, type: 'cat' },
    { key: 'hot',    change: 'You now warm it strongly.',
      t: 1.45, N: 1,   ea: 1,    type: 'temp' },
    { key: 'cool',   change: 'You now cool it in an ice bath.',
      t: 0.85, N: 1,   ea: 1,    type: 'temp' },
    { key: 'dilute', change: 'You now dilute one reactant to half strength.',
      t: 1,    N: 0.5, ea: 1,    type: 'conc' }
  ];

  function model(r) {
    var before = curve(1, 1), after = curve(r.t, r.N);
    var eaA = EA0 * r.ea;
    var fB = areaFrom(before, EA0) / areaFrom(before, 0);
    var fA = areaFrom(after, eaA) / areaFrom(after, 0);
    /* collision frequency: how many particles there are, times how fast
       they move (mean speed goes with the square root of temperature) */
    var coll = r.N * Math.sqrt(r.t);
    var share = fA / fB;
    return {
      before: before, after: after, eaB: EA0, eaA: eaA,
      fB: fB, fA: fA, coll: coll, share: share, rate: coll * share,
      cBand: band(coll), sBand: band(share),
      peakB: peakOf(before), peakA: peakOf(after),
      sameCurve: (r.t === 1 && r.N === 1)
    };
  }

  var OPTS = [
    { k: 'down',     label: 'Falls' },
    { k: 'same',     label: 'No change' },
    { k: 'up-small', label: 'Rises a little' },
    { k: 'up-big',   label: 'Rises a lot' }
  ];
  var SAY = {
    'down': 'falls', 'same': 'stays the same',
    'up-small': 'rises a little', 'up-big': 'rises a lot'
  };

  function fmtX(m) { return '×' + m.toFixed(2).replace(/\.?0+$/, ''); }
  function pct(f) { return (f * 100).toFixed(1) + '%'; }

  /* ---- markup ----------------------------------------------------- */

  var CSS = [
    '.svw-cte{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;',
    'color:#2d2a26;line-height:1.45;text-align:left}',
    '.svw-cte *{box-sizing:border-box}',
    '.svw-cte .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;',
    'text-transform:uppercase;color:var(--cte-a);margin:0 0 .18rem}',
    '.svw-cte .t{font-family:"Source Serif 4",Georgia,serif;font-weight:600;',
    'font-size:1.22rem;line-height:1.2;margin:0 0 .3rem}',
    '.svw-cte .frame{font-size:.84rem;margin:0 0 .5rem;color:#3c3831}',
    '.svw-cte .frame b{font-weight:600}',
    '.svw-cte .stagewrap{background:#faf8f5;border:1px solid #efe9e0;',
    'border-radius:12px;padding:.3rem .25rem .05rem;margin:0 0 .5rem}',
    '.svw-cte .stagewrap svg{display:block;width:100%;max-width:430px;',
    'height:auto;margin:0 auto}',
    '.svw-cte .after{opacity:0}',
    '.svw-cte.is-live .after{opacity:1}',
    '.svw-cte.anim .after{transition:opacity .32s cubic-bezier(.16,1,.3,1)}',
    '.svw-cte .stats{display:none;gap:1.05rem;flex-wrap:wrap;margin:0 0 .45rem}',
    '.svw-cte.is-live .stats{display:flex}',
    '.svw-cte .stat span{display:block;font-size:.7rem;font-weight:600;color:#8d8880}',
    '.svw-cte .stat strong{display:block;font-size:.82rem;font-weight:600;',
    'font-variant-numeric:tabular-nums}',
    '.svw-cte .groups{display:grid;gap:.45rem .9rem;margin:0 0 .45rem;',
    'grid-template-columns:repeat(auto-fit,minmax(232px,1fr))}',
    '.svw-cte .glab{font-size:.78rem;font-weight:600;margin:0 0 .28rem;',
    'display:flex;align-items:center;gap:.35rem}',
    '.svw-cte .chip{display:inline-flex;align-items:center;justify-content:center;',
    'width:1.05rem;height:1.05rem;border-radius:50%;background:var(--cte-c);',
    'font-size:.66rem;font-weight:700;flex:none}',
    '.svw-cte .opts{display:grid;grid-template-columns:repeat(4,1fr);gap:.28rem}',
    '.svw-cte .opt{font:600 .74rem/1.25 inherit;font-family:inherit;color:#2d2a26;',
    'background:#faf8f5;border:1px solid #ddd7cd;border-radius:9px;',
    'padding:.36rem .18rem;min-height:2.05rem;cursor:pointer;text-align:center}',
    '.svw-cte .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-cte .opt.was{border-color:#4f7d63;box-shadow:inset 0 0 0 1px #4f7d63}',
    '.svw-cte .opt[disabled]{cursor:default}',
    '.svw-cte .row{display:flex;align-items:center;gap:.6rem;margin:0 0 .4rem}',
    '.svw-cte .go{font:600 .82rem/1.2 inherit;font-family:inherit;',
    'background:#2d2a26;color:#fff;border:1px solid #2d2a26;border-radius:10px;',
    'padding:.5rem .95rem;cursor:pointer;flex:none}',
    '.svw-cte .go[disabled]{opacity:.42;cursor:default}',
    '.svw-cte .run{font-size:.74rem;color:#8d8880;flex:1;text-align:right}',
    '.svw-cte .cap{font-size:.83rem;line-height:1.45;margin:0;color:#3c3831;',
    'min-height:4.4em}',
    '.svw-cte .cap b{font-weight:600}',
    '.svw-cte .sr{position:absolute;width:1px;height:1px;overflow:hidden;',
    'clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap}'
  ].join('');

  /* plot box inside the 320x132 viewBox */
  var PX0 = 32, PX1 = 312, PY0 = 22, PY1 = 104;

  function xp(E) { return PX0 + (E / XMAX) * (PX1 - PX0); }

  function svgEl(tag, attrs) {
    var n = document.createElementNS(SVGNS, tag), k;
    for (k in attrs) { if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]); }
    return n;
  }

  window.SVWidget = {
    meta: {
      id: 'collision-theory-energy-distribution',
      title: 'Collisions that count',
      teaches: 'Warming a reaction shifts the whole spread of particle energies, so the share of collisions above the activation energy rises far more than the collision count does; a catalyst lowers the barrier instead, and concentration only adds collisions.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;

      var idx = 0, picked = { c: null, s: null };
      var streak = 0, attempted = 0, mastered = false, committed = false, lastCorrect = null;
      var m = model(ROUNDS[0]);

      var w = document.createElement('div');
      w.className = 'svw-cte' + (reduced ? '' : ' anim');
      w.style.setProperty('--cte-a', accent);
      w.style.setProperty('--cte-c', accent + '33');
      var st = document.createElement('style');
      st.textContent = CSS;
      w.appendChild(st);

      var head = document.createElement('div');
      head.innerHTML =
        '<p class="k">Rates of reaction</p>' +
        '<p class="t">Collisions that count</p>' +
        '<p class="frame"></p>';
      w.appendChild(head);
      var frame = head.querySelector('.frame');

      /* ---- stage ---- */
      var wrap = document.createElement('div');
      wrap.className = 'stagewrap';
      var svg = svgEl('svg', {
        viewBox: '0 0 320 126', preserveAspectRatio: 'xMidYMid meet', role: 'img'
      });
      var fillB = svgEl('path', { fill: 'rgba(45,42,38,.22)', stroke: 'none' });
      var gAfter = svgEl('g', { 'class': 'after' });
      var fillA = svgEl('path', { fill: accent + '7a', stroke: 'none' });
      var lineA = svgEl('path', { fill: 'none', stroke: accent, 'stroke-width': '2', 'stroke-linejoin': 'round' });
      var eaLineA = svgEl('line', { stroke: accent, 'stroke-width': '1.4', 'stroke-dasharray': '4 3' });
      var pctA = svgEl('text', {
        x: '0', y: '0', fill: accent, 'font-size': '11',
        'font-family': 'Inter,system-ui,sans-serif', 'font-weight': '700'
      });
      var eaTextA = svgEl('text', {
        x: '232', y: '13', fill: accent,
        'font-size': '11', 'font-family': 'Inter,system-ui,sans-serif', 'font-weight': '600'
      });
      eaTextA.textContent = 'with catalyst';
      var eaSwatch = svgEl('line', {
        x1: '214', y1: '9.5', x2: '228', y2: '9.5', stroke: accent,
        'stroke-width': '1.4', 'stroke-dasharray': '4 3'
      });
      gAfter.appendChild(fillA); gAfter.appendChild(lineA); gAfter.appendChild(pctA);
      gAfter.appendChild(eaLineA); gAfter.appendChild(eaSwatch); gAfter.appendChild(eaTextA);

      var lineB = svgEl('path', { fill: 'none', stroke: '#8d8880', 'stroke-width': '1.6', 'stroke-linejoin': 'round' });
      var axisX = svgEl('line', { x1: PX0, y1: PY1, x2: PX1, y2: PY1, stroke: '#c9c2b6', 'stroke-width': '1' });
      var axisY = svgEl('line', { x1: PX0, y1: PY0, x2: PX0, y2: PY1, stroke: '#c9c2b6', 'stroke-width': '1' });
      var eaLineB = svgEl('line', {
        x1: xp(EA0), y1: PY0 - 2, x2: xp(EA0), y2: PY1,
        stroke: '#2d2a26', 'stroke-width': '1.4', 'stroke-dasharray': '4 3'
      });

      function txt(x, y, s, opts) {
        var a = { x: x, y: y, 'font-size': (opts && opts.size) || '11',
          'font-family': 'Inter,system-ui,sans-serif', fill: (opts && opts.fill) || '#8d8880',
          'font-weight': (opts && opts.weight) || '500' };
        if (opts && opts.anchor) a['text-anchor'] = opts.anchor;
        var n = svgEl('text', a);
        n.textContent = s;
        return n;
      }

      var pctB = txt(0, 0, '', { fill: '#6f6a62', weight: '700' });
      var yLab = txt(PX0, 13, 'number of particles');
      var eaLab = txt(xp(EA0) + 5, 34, 'activation energy', { fill: '#2d2a26', weight: '600' });
      var xLab = txt(PX0, 122, 'particle energy →');
      var brLine = svgEl('path', { fill: 'none', stroke: '#c9c2b6', 'stroke-width': '1' });
      var brLab = txt(0, 122, 'enough energy to react', { anchor: 'middle' });

      var legend = svgEl('g', { 'class': 'after' });
      legend.appendChild(svgEl('line', { x1: 196, y1: 9.5, x2: 209, y2: 9.5, stroke: '#8d8880', 'stroke-width': '1.6' }));
      legend.appendChild(txt(213, 13, 'before'));
      legend.appendChild(svgEl('line', { x1: 252, y1: 9.5, x2: 265, y2: 9.5, stroke: accent, 'stroke-width': '2' }));
      legend.appendChild(txt(269, 13, 'after', { fill: accent, weight: '600' }));

      [fillB, gAfter, pctB, lineB, axisX, axisY, eaLineB, yLab, eaLab, xLab, brLine, brLab, legend]
        .forEach(function (n) { svg.appendChild(n); });
      wrap.appendChild(svg);
      w.appendChild(wrap);

      /* ---- stats (revealed with the answer) ---- */
      var stats = document.createElement('div');
      stats.className = 'stats';
      stats.innerHTML =
        '<div class="stat"><span>Collisions</span><strong id="s1"></strong></div>' +
        '<div class="stat"><span>Enough energy</span><strong id="s2"></strong></div>' +
        '<div class="stat"><span>Overall rate</span><strong id="s3"></strong></div>';
      var s1 = stats.querySelector('#s1'), s2 = stats.querySelector('#s2'), s3 = stats.querySelector('#s3');
      s1.removeAttribute('id'); s2.removeAttribute('id'); s3.removeAttribute('id');
      w.appendChild(stats);

      /* ---- prediction groups ---- */
      var groups = document.createElement('div');
      groups.className = 'groups';
      var btnC = [], btnS = [];

      function makeGroup(n, label, store, sink) {
        var g = document.createElement('div');
        var lab = document.createElement('p');
        lab.className = 'glab';
        lab.innerHTML = '<span class="chip">' + n + '</span>';
        lab.appendChild(document.createTextNode(label));
        g.appendChild(lab);
        var o = document.createElement('div');
        o.className = 'opts';
        OPTS.forEach(function (opt) {
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'opt';
          b.textContent = opt.label;
          b.setAttribute('aria-pressed', 'false');
          b.setAttribute('aria-label', label + ': ' + opt.label);
          b.addEventListener('click', function () {
            if (committed) return;
            picked[store] = opt.k;
            sink.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
            go.disabled = !(picked.c && picked.s);
            say(label + ': ' + opt.label + ' selected.');
            paint();
          });
          sink.push(b);
          o.appendChild(b);
        });
        g.appendChild(o);
        groups.appendChild(g);
      }
      makeGroup('1', 'Collisions each second', 'c', btnC);
      makeGroup('2', 'Share of collisions with enough energy', 's', btnS);
      w.appendChild(groups);

      /* ---- commit ---- */
      var row = document.createElement('div');
      row.className = 'row';
      var go = document.createElement('button');
      go.type = 'button';
      go.className = 'go';
      go.textContent = 'Check';
      go.disabled = true;
      var run = document.createElement('span');
      run.className = 'run';
      row.appendChild(go); row.appendChild(run);
      w.appendChild(row);

      var cap = document.createElement('p');
      cap.className = 'cap';
      w.appendChild(cap);

      var sr = document.createElement('p');
      sr.className = 'sr';
      sr.setAttribute('aria-live', 'polite');
      w.appendChild(sr);
      function say(s) { sr.textContent = s; }

      root.appendChild(w);

      /* ---- drawing ---- */
      function yScale() {
        var p = m.peakB;
        if (committed && m.peakA > p) p = m.peakA;
        return p * 1.12;
      }
      function yp(y, s) { return PY1 - (y / s) * (PY1 - PY0); }

      function pathOf(pts, s) {
        var d = '', i;
        for (i = 0; i < pts.length; i++) {
          d += (i ? 'L' : 'M') + xp(pts[i][0]).toFixed(1) + ' ' + yp(pts[i][1], s).toFixed(1);
        }
        return d;
      }
      function tailOf(pts, ea, s) {
        var d = 'M' + xp(ea).toFixed(1) + ' ' + yp(yAt(pts, ea), s).toFixed(1), i;
        for (i = 0; i < pts.length; i++) {
          if (pts[i][0] > ea) d += 'L' + xp(pts[i][0]).toFixed(1) + ' ' + yp(pts[i][1], s).toFixed(1);
        }
        return d + 'L' + xp(XMAX).toFixed(1) + ' ' + PY1 + 'L' + xp(ea).toFixed(1) + ' ' + PY1 + 'Z';
      }

      function draw() {
        var s = yScale();
        lineB.setAttribute('d', pathOf(m.before, s));
        fillB.setAttribute('d', tailOf(m.before, m.eaB, s));
        lineA.setAttribute('d', m.sameCurve ? '' : pathOf(m.after, s));
        fillA.setAttribute('d', tailOf(m.after, m.eaA, s));
        var moved = Math.abs(m.eaA - m.eaB) > 1e-9;
        eaLineA.setAttribute('x1', xp(m.eaA)); eaLineA.setAttribute('x2', xp(m.eaA));
        eaLineA.setAttribute('y1', PY0 - 2); eaLineA.setAttribute('y2', PY1);
        eaLineA.setAttribute('opacity', moved ? '1' : '0');
        eaTextA.setAttribute('opacity', moved ? '1' : '0');
        eaSwatch.setAttribute('opacity', moved ? '1' : '0');
        var bx2 = committed ? m.eaB + 1.6 : m.eaB;
        pctB.setAttribute('x', (xp(bx2) + (committed ? 0 : 5)).toFixed(1));
        pctB.setAttribute('y', (yp(yAt(m.before, bx2), s) - 4).toFixed(1));
        pctB.textContent = pct(m.fB);
        pctA.setAttribute('x', (xp(m.eaA) + 5).toFixed(1));
        pctA.setAttribute('y', (yp(yAt(m.after, m.eaA), s) - 4).toFixed(1));
        pctA.textContent = pct(m.fA);
        legend.style.display = m.sameCurve ? 'none' : '';
        var bx = committed ? Math.min(m.eaA, m.eaB) : m.eaB;
        brLine.setAttribute('d', 'M' + xp(bx).toFixed(1) + ' 108L' + xp(bx).toFixed(1) +
          ' 111L' + PX1 + ' 111L' + PX1 + ' 108');
        brLab.setAttribute('x', ((xp(bx) + PX1) / 2).toFixed(1));
        svg.setAttribute('aria-label',
          'Graph of number of particles against particle energy, with a dashed activation energy line. ' +
          (committed
            ? 'Before the change ' + pct(m.fB) + ' of particles are beyond the line; after it ' + pct(m.fA) + ' are.'
            : pct(m.fB) + ' of the particles are beyond the line.'));
      }

      /* ---- text ---- */
      function openLine() {
        return 'The curve shows how the energy of the particles is spread out. Only the ' +
          'shaded slice — ' + pct(m.fB) + ' of them — is past the dashed line with enough ' +
          'energy to react; the rest just bounce apart.';
      }

      function mechanism(r) {
        if (r.type === 'temp') {
          if (picked.s === 'same' && r.t > 1) {
            return 'Warming is not just more collisions: it shifts the whole spread of ' +
              'particle energies to the right, so a far larger share clears the activation energy line.';
          }
          if (picked.s === 'same') {
            return 'Cooling is not just fewer collisions: it drags the whole spread of ' +
              'particle energies down, so a far smaller share still clears the activation energy line.';
          }
          return 'Temperature shifts the whole spread of particle energies, so the share ' +
            'above the activation energy line changes far more than the collision count does.';
        }
        if (r.type === 'cat') {
          if (picked.c !== 'same') {
            return 'A catalyst does not make particles move faster, so the collision count is ' +
              'untouched. It lowers the activation energy, and it is not used up.';
          }
          return 'A catalyst leaves the spread of energies alone and lowers the activation ' +
            'energy instead, so more of the same collisions clear it. It is not used up.';
        }
        if (picked.s !== 'same') {
          return 'Concentration changes how many collisions there are, never how energetic ' +
            'they are — the same small share still clears the barrier.';
        }
        return (r.N > 1 ? 'Twice as many particles in the same space give about twice as many collisions'
          : 'Half as many particles in the same space give about half as many collisions') +
          ', but the spread of energies is unchanged — the same small share still clears the barrier.';
      }

      function feedback(r, ok, instead) {
        var real = 'the collision count <b>' + SAY[m.cBand] + '</b> (' + fmtX(m.coll) +
          ') and the share with enough energy <b>' + SAY[m.sBand] + '</b> (' + fmtX(m.share) + ')';
        var tail = instead || mechanism(r);
        if (ok) {
          return '<b>Right —</b> ' + real + '. ' + tail;
        }
        return '<b>Not quite —</b> you said the collision count <b>' + SAY[picked.c] +
          '</b> and the share <b>' + SAY[picked.s] + '</b>. In fact ' + real + '. ' + tail;
      }

      function paint() {
        var r = ROUNDS[idx];
        frame.innerHTML = 'Two solutions react in a flask. <b>' + r.change +
          '</b> Predict the effect on both.';
        run.textContent = mastered
          ? 'You have it — carry on if you like.'
          : (streak === 1 ? '1 in a row.'
            : streak === 2 ? '2 in a row — one more and you have it.' : '');
        root.dataset.svState = JSON.stringify({
          round: idx, change: r.key,
          picked: { collisions: picked.c, share: picked.s },
          actual: { collisions: m.cBand, share: m.sBand },
          multiplier: {
            collisions: +m.coll.toFixed(3), share: +m.share.toFixed(3), rate: +m.rate.toFixed(3)
          },
          shareBefore: +(m.fB * 100).toFixed(2), shareAfter: +(m.fA * 100).toFixed(2),
          committed: committed, correct: lastCorrect,
          streak: streak, mastered: mastered, attempted: attempted
        });
      }

      function commit() {
        var r = ROUNDS[idx];
        var ok = (picked.c === m.cBand && picked.s === m.sBand);
        committed = true;
        lastCorrect = ok;
        attempted += 1;
        streak = ok ? streak + 1 : 0;
        if (streak >= 3) { mastered = true; }

        w.classList.add('is-live');
        draw();
        s1.textContent = fmtX(m.coll);
        s2.textContent = pct(m.fB) + ' → ' + pct(m.fA);
        s3.textContent = fmtX(m.rate);
        cap.innerHTML = feedback(r, ok, (ok && mastered && streak === 3)
          ? '<b>Three in a row — you have it:</b> heat shifts the whole spread of energies, ' +
            'concentration only adds collisions, a catalyst lowers the barrier.'
          : null);
        btnC.concat(btnS).forEach(function (b) { b.disabled = true; });
        btnC[OPTS.map(function (o) { return o.k; }).indexOf(m.cBand)].classList.add('was');
        btnS[OPTS.map(function (o) { return o.k; }).indexOf(m.sBand)].classList.add('was');
        go.textContent = mastered ? 'Another anyway' : 'Next change';
        go.disabled = false;
        say(cap.textContent);
        paint();
      }

      function next() {
        idx = (idx + 1) % ROUNDS.length;
        m = model(ROUNDS[idx]);
        committed = false;
        lastCorrect = null;
        picked.c = null; picked.s = null;
        w.classList.remove('is-live');
        btnC.concat(btnS).forEach(function (b) {
          b.disabled = false;
          b.classList.remove('was');
          b.setAttribute('aria-pressed', 'false');
        });
        go.textContent = 'Check';
        go.disabled = true;
        cap.textContent = openLine();
        draw();
        paint();
        say('New change: ' + ROUNDS[idx].change);
      }

      go.addEventListener('click', function () {
        if (committed) { next(); } else if (picked.c && picked.s) { commit(); }
      });

      cap.textContent = openLine();
      draw();
      paint();
    }
  };
}());
