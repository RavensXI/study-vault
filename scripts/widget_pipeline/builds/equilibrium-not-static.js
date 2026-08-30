/* equilibrium-not-static — a sealed flask, ten seconds on.
   The student reads a count-vs-time graph, commits to what the amounts do
   next AND what the two rates are doing, then watches the particles.
   Every number comes from one kinetic model: dA/dt = -kf*A + kr*B. */
(function () {
  'use strict';

  var N = 24;                      /* particles in the flask, fixed */
  var SETS = [                     /* rate constants per second */
    { kf: 0.08, kr: 0.04 },        /* settles at  8 A, 16 B */
    { kf: 0.02, kr: 0.06 },        /* settles at 18 A,  6 B */
    { kf: 0.04, kr: 0.08 },        /* settles at 16 A,  8 B */
    { kf: 0.09, kr: 0.03 }         /* settles at  6 A, 18 B */
  ];
  var WINDOW = 10;                 /* seconds the student predicts */
  var TCAND = [4, 5, 6, 7, 8, 9, 10, 12, 14, 16];

  /* ---------- the model ---------------------------------------------- */

  function build(set, A0, tNow) {
    var K = set.kf + set.kr, Aeq = N * set.kr / K;
    function A(t) { return Aeq + (A0 - Aeq) * Math.exp(-K * t); }
    function intA(a, b) {
      return Aeq * (b - a) + (A0 - Aeq) / K * (Math.exp(-K * a) - Math.exp(-K * b));
    }
    var tEnd = tNow + WINDOW;
    var ia = intA(tNow, tEnd), ib = WINDOW * N - ia;
    var nowA = Math.round(A(tNow));
    var fwd = Math.round(set.kf * ia), rev = Math.round(set.kr * ib);
    var nextA = nowA - fwd + rev;                    /* what the dots will show */
    var Rf = set.kf * A(tNow), Rr = set.kr * (N - A(tNow));
    var rel = Math.abs(Rf - Rr) / Math.max(Rf, Rr);
    return {
      A: A, K: K, Aeq: Aeq, A0: A0, tNow: tNow, tEnd: tEnd,
      nowA: nowA, nextA: nextA, fwd: fwd, rev: rev, rel: rel,
      rates: rel < 0.06 ? 'eq' : (Rf > Rr ? 'fwd' : 'rev'),
      trend: nextA < nowA ? 'fall' : (nextA > nowA ? 'rise' : 'stay')
    };
  }

  function ok(r, shape) {
    if (r.nowA === N / 2 || r.nextA === N / 2) return false;   /* the 12/12 trap must stay wrong */
    if (r.fwd > r.nowA || r.rev > N - r.nowA) return false;    /* can only flip what is there */
    if (r.nextA < 0 || r.nextA > N) return false;
    if (shape === 'settled') {
      return r.rates === 'eq' && r.trend === 'stay' &&
             r.fwd === r.rev && r.fwd >= 3 && r.rel < 0.02;
    }
    if (Math.abs(r.nextA - r.nowA) < 3) return false;
    if (Math.abs(r.fwd - r.rev) < 3) return false;
    if (r.rel < 0.25) return false;
    return shape === 'falling' ? (r.rates === 'fwd' && r.trend === 'fall')
                               : (r.rates === 'rev' && r.trend === 'rise');
  }

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function pick(shape, avoid) {
    var order = shuffle([0, 1, 2, 3]), i, s, r, hits = [];
    for (i = 0; i < order.length; i++) {
      s = SETS[order[i]];
      if (shape === 'settled') {
        var A0 = Math.random() < 0.5 ? 0 : N;
        r = build(s, A0, Math.ceil(6 / (s.kf + s.kr) / 5) * 5);
        if (ok(r, shape) && order[i] !== avoid) { r.set = order[i]; r.shape = shape; return r; }
      } else {
        var start = shape === 'falling' ? N : 0;
        for (var k = 0; k < TCAND.length; k++) {
          r = build(s, start, TCAND[k]);
          if (ok(r, shape)) { r.set = order[i]; r.shape = shape; hits.push(r); }
        }
        if (hits.length && order[i] !== avoid) return hits[Math.floor(Math.random() * hits.length)];
        hits = [];
      }
    }
    /* nothing rejected on the avoid rule alone: take the first that works */
    for (i = 0; i < SETS.length; i++) {
      s = SETS[i];
      if (shape === 'settled') {
        r = build(s, N, Math.ceil(6 / (s.kf + s.kr) / 5) * 5);
        if (ok(r, shape)) { r.set = i; r.shape = shape; return r; }
      } else {
        for (var m = 0; m < TCAND.length; m++) {
          r = build(s, shape === 'falling' ? N : 0, TCAND[m]);
          if (ok(r, shape)) { r.set = i; r.shape = shape; return r; }
        }
      }
    }
    r = build(SETS[0], N, 50); r.set = 0; r.shape = 'settled'; return r;
  }

  /* ---------- markup helpers ------------------------------------------ */

  var NS = 'http://www.w3.org/2000/svg';
  function sv(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) if (attrs.hasOwnProperty(k)) n.setAttribute(k, attrs[k]);
    return n;
  }
  function h(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }

  var CSS = [
    '.svw-eqns{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
    '.svw-eqns *{box-sizing:border-box}',
    '.svw-eqns .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--svw-a);margin:0 0 .15rem}',
    '.svw-eqns .t{font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;font-weight:600;line-height:1.2;margin:0 0 .3rem}',
    '.svw-eqns .frame{font-size:.84rem;line-height:1.45;color:#4a453e;margin:0 0 .48rem}',
    '.svw-eqns .stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.45rem .5rem;margin:0 0 .48rem}',
    '.svw-eqns .stage svg{display:block;width:100%;max-width:390px;height:auto;margin:0 auto}',
    '.svw-eqns .grp{margin:0 0 .42rem}',
    '.svw-eqns .lab{display:flex;align-items:center;gap:.4rem;font-size:.78rem;font-weight:600;color:#5b564e;margin:0 0 .32rem}',
    '.svw-eqns .chip{flex:none;width:1.05rem;height:1.05rem;border-radius:50%;background:var(--svw-a);color:#fff;font-size:.62rem;font-weight:700;display:flex;align-items:center;justify-content:center}',
    '.svw-eqns .opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(126px,1fr));gap:.35rem}',
    '.svw-eqns .opt{font:inherit;font-size:.78rem;font-weight:600;line-height:1.25;text-align:left;padding:.42rem .55rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;cursor:pointer}',
    '.svw-eqns .opt:hover{border-color:#c9c1b4}',
    '.svw-eqns .opt.on{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-eqns .opt[disabled]{cursor:default;opacity:.62}',
    '.svw-eqns .opt.on[disabled]{opacity:1}',
    '.svw-eqns .row{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin:0 0 .4rem}',
    '.svw-eqns .go{font:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-eqns .go.quiet{background:#faf8f5;color:#2d2a26;border-color:#ddd7cd}',
    '.svw-eqns .run{font-size:.76rem;color:#8d8880}',
    '.svw-eqns .cap{font-size:.84rem;line-height:1.5;margin:0;min-height:3.6rem;color:#2d2a26}',
    '.svw-eqns .cap b{font-weight:600}',
    '.svw-eqns .cap .v{font-weight:700}',
    '.svw-eqns .cap .v.no{color:#2d2a26}',
    '.svw-eqns .cap .v.yes{color:#4f7d63}',
    '.svw-eqns .sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}'
  ].join('');

  /* ---------- the widget ---------------------------------------------- */

  window.SVWidget = {
    meta: {
      id: 'equilibrium-not-static',
      title: 'Sealed flask: the next ten seconds',
      teaches: 'At equilibrium both reactions carry on at equal rates, so the amounts hold steady — steady, not equal.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;

      root.className = 'svw-eqns';
      root.style.setProperty('--svw-a', accent);
      root.appendChild(h('style', null, CSS));

      root.appendChild(h('p', 'k', 'Reversible reactions'));
      root.appendChild(h('h3', 't', 'The next ten seconds'));
      root.appendChild(h('p', 'frame',
        'A sealed flask holds the reversible reaction A ⇌ B; nothing enters or leaves. ' +
        'From the graph, predict the next 10 seconds.'));

      /* --- stage: one scene, flask on the left, count graph on the right --- */
      var stage = h('div', 'stage');
      var svg = sv('svg', { viewBox: '0 0 320 110', role: 'img' });
      svg.appendChild(sv('title', {})).textContent = 'A sealed flask of particles and a graph of how many of each there are over time';

      var PX = 134, PY = 14, PW = 182, PH = 70, BASE = PY + PH;

      svg.appendChild(sv('rect', { x: 46, y: 3, width: 16, height: 10, rx: 3,
        fill: '#efe9e0', stroke: '#b7ae9f', 'stroke-width': 1.2 }));
      svg.appendChild(sv('rect', { x: 12, y: 13, width: 84, height: 80, rx: 10,
        fill: '#fff', stroke: '#b7ae9f', 'stroke-width': 1.4 }));

      var dots = [], i, j;
      for (j = 0; j < 4; j++) {
        for (i = 0; i < 6; i++) {
          var c = sv('circle', { cx: (21 + i * 12.6).toFixed(1), cy: 27 + j * 17, r: 4.4,
            'stroke-width': 1.4 });
          dots.push(c); svg.appendChild(c);
        }
      }
      var flaskLab = sv('text', { x: 54, y: 106, 'text-anchor': 'middle', 'font-size': 12,
        'font-family': 'Inter,system-ui,sans-serif', fill: '#5b564e' });
      svg.appendChild(flaskLab);

      var band = sv('rect', { x: PX, y: PY, width: 0, height: PH, fill: '#2d2a26', opacity: 0.05 });
      svg.appendChild(band);
      svg.appendChild(sv('line', { x1: PX, y1: PY, x2: PX, y2: BASE, stroke: '#d8d1c5', 'stroke-width': 1 }));
      svg.appendChild(sv('line', { x1: PX, y1: BASE, x2: PX + PW, y2: BASE, stroke: '#d8d1c5', 'stroke-width': 1 }));

      function txt(x, y, s, opt) {
        var a = { x: x, y: y, 'text-anchor': (opt && opt.anchor) || 'start',
          'font-size': (opt && opt.size) || 12, 'font-family': 'Inter,system-ui,sans-serif',
          fill: (opt && opt.fill) || '#8d8880' };
        if (opt && opt.weight) a['font-weight'] = opt.weight;
        var n = sv('text', a); n.textContent = s; svg.appendChild(n); return n;
      }
      txt(131, PY + 4, String(N), { anchor: 'end' });
      var ylab = txt(110, PY + PH / 2, 'particles', { anchor: 'middle', size: 11.5 });
      ylab.setAttribute('transform', 'rotate(-90 110 ' + (PY + PH / 2) + ')');
      txt(PX, BASE + 15, '0', { anchor: 'middle' });
      var nowLab = txt(PX, BASE + 15, '', { anchor: 'middle' });
      var tally = txt(PX + PW, 11, '', { anchor: 'end', fill: '#5b564e' });

      var pathA = sv('path', { fill: 'none', stroke: accent, 'stroke-width': 2.2, 'stroke-linejoin': 'round' });
      var pathB = sv('path', { fill: 'none', stroke: '#5b564e', 'stroke-width': 2, 'stroke-dasharray': '5 3', 'stroke-linejoin': 'round' });
      var futA = sv('path', { fill: 'none', stroke: accent, 'stroke-width': 2.2, 'stroke-linejoin': 'round' });
      var futB = sv('path', { fill: 'none', stroke: '#5b564e', 'stroke-width': 2, 'stroke-dasharray': '5 3', 'stroke-linejoin': 'round' });
      svg.appendChild(pathA); svg.appendChild(pathB); svg.appendChild(futA); svg.appendChild(futB);
      var nowLine = sv('line', { y1: PY, y2: BASE, stroke: '#2d2a26', 'stroke-width': 1,
        'stroke-dasharray': '3 3', opacity: 0.55 });
      svg.appendChild(nowLine);
      var tagA = txt(PX + 8, 0, 'A', { weight: 700, fill: accent });
      var tagB = txt(PX + 8, 0, 'B', { weight: 700, fill: '#5b564e' });

      stage.appendChild(svg);
      root.appendChild(stage);

      /* --- controls: two sequenced groups, one commit ------------------ */
      function group(no, text) {
        var g = h('div', 'grp'), lab = h('div', 'lab');
        lab.appendChild(h('span', 'chip', no));
        lab.appendChild(h('span', null, text));
        g.appendChild(lab);
        var o = h('div', 'opts'); g.appendChild(o);
        root.appendChild(g);
        return o;
      }
      var TRENDS = ['fall', 'stay', 'rise', 'even'];
      var RATES = ['stop', 'fwd', 'rev', 'eq'];

      var box1 = group('1', 'In the next 10 s the number of A will…');
      var box2 = group('2', '…and the two reaction rates are…');

      var btn1 = [], btn2 = [], k;
      for (k = 0; k < 4; k++) {
        var b1 = h('button', 'opt'); b1.type = 'button'; b1.dataset.v = TRENDS[k];
        box1.appendChild(b1); btn1.push(b1);
        var b2 = h('button', 'opt'); b2.type = 'button'; b2.dataset.v = RATES[k];
        box2.appendChild(b2); btn2.push(b2);
      }
      btn2[0].textContent = 'Both have stopped';
      btn2[1].textContent = 'Forward faster';
      btn2[2].textContent = 'Reverse faster';
      btn2[3].textContent = 'Equal — both still going';

      var row = h('div', 'row');
      var go = h('button', 'go', 'Check'); go.type = 'button';
      var run = h('span', 'run', '');
      row.appendChild(go); row.appendChild(run);
      root.appendChild(row);

      var cap = h('p', 'cap');
      root.appendChild(cap);
      var sr = h('p', 'sr'); sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* --- state -------------------------------------------------------- */
      var R = null, ident = [], flipF = [], flipR = [];
      var pickedT = null, pickedR = null, phase = 'ask';
      var streak = 0, attempted = 0, mastered = false, lastSet = -1;
      var shapes = shuffle(['settled', 'falling', 'rising']), shapeAt = 0;
      var timer = null;

      function xFor(t) { return PX + (t / R.tEnd) * PW; }
      function yFor(n) { return BASE - (n / N) * PH; }

      function curve(from, to, forB) {
        var d = '', steps = Math.max(2, Math.round((to - from) * 4)), s, t, a;
        for (s = 0; s <= steps; s++) {
          t = from + (to - from) * s / steps;
          a = R.A(t);
          d += (s ? 'L' : 'M') + xFor(t).toFixed(1) + ' ' + yFor(forB ? N - a : a).toFixed(1) + ' ';
        }
        return d;
      }

      function paintDots() {
        var nA = 0;
        for (var q = 0; q < N; q++) {
          var isA = ident[q] === 'A';
          if (isA) nA++;
          dots[q].setAttribute('fill', isA ? accent : '#fff');
          dots[q].setAttribute('stroke', isA ? accent : '#8d8880');
        }
        flaskLab.textContent = nA + ' A · ' + (N - nA) + ' B';
        return nA;
      }

      function newRound() {
        var shape = shapes[shapeAt % 3];
        shapeAt++;
        if (shapeAt % 3 === 0) shuffle(shapes);
        R = pick(shape, lastSet);
        lastSet = R.set;

        ident = [];
        for (var q = 0; q < N; q++) ident.push(q < R.nowA ? 'A' : 'B');
        shuffle(ident);
        var as = [], bs = [];
        for (q = 0; q < N; q++) (ident[q] === 'A' ? as : bs).push(q);
        flipF = shuffle(as).slice(0, R.fwd);
        flipR = shuffle(bs).slice(0, R.rev);

        pathA.setAttribute('d', curve(0, R.tNow, false));
        pathB.setAttribute('d', curve(0, R.tNow, true));
        futA.setAttribute('d', ''); futB.setAttribute('d', '');
        band.setAttribute('x', xFor(R.tNow)); band.setAttribute('width', (PW - (xFor(R.tNow) - PX)).toFixed(1));
        nowLine.setAttribute('x1', xFor(R.tNow)); nowLine.setAttribute('x2', xFor(R.tNow));
        nowLab.setAttribute('x', xFor(R.tNow)); nowLab.textContent = 'now, ' + R.tNow + ' s';
        tagA.setAttribute('y', (yFor(R.A(0)) + (R.A0 === N ? 12 : -5)).toFixed(1));
        tagB.setAttribute('y', (yFor(N - R.A(0)) + (R.A0 === N ? -5 : 12)).toFixed(1));
        tally.textContent = '';
        paintDots();

        pickedT = null; pickedR = null; phase = 'ask';
        for (var b = 0; b < 4; b++) {
          btn1[b].classList.remove('on'); btn2[b].classList.remove('on');
          btn1[b].disabled = false; btn2[b].disabled = false;
        }
        btn1[0].textContent = 'Fall';
        btn1[1].textContent = 'Stay at ' + R.nowA;
        btn1[2].textContent = 'Rise';
        btn1[3].textContent = 'Even out at ' + (N / 2) + ' A, ' + (N / 2) + ' B';
        go.textContent = 'Check'; go.classList.remove('quiet');
        cap.textContent = '';
        showRun();
        state();
      }

      function showRun() {
        if (mastered) { run.textContent = 'You have it.'; return; }
        if (streak === 1) { run.textContent = '1 right in a row — two to go.'; return; }
        if (streak === 2) { run.textContent = '2 right in a row — one to go.'; return; }
        run.textContent = '';
      }

      function state(extra) {
        var s = {
          streak: streak, mastered: mastered, attempted: attempted,
          shape: R ? R.shape : null, nowA: R ? R.nowA : null, nextA: R ? R.nextA : null,
          fwd: R ? R.fwd : null, rev: R ? R.rev : null,
          answer: R ? { trend: R.trend, rates: R.rates } : null,
          picked: { trend: pickedT, rates: pickedR }, phase: phase
        };
        if (extra) for (var q in extra) if (extra.hasOwnProperty(q)) s[q] = extra[q];
        root.dataset.svState = JSON.stringify(s);
      }

      function choose(list, which, v) {
        return function () {
          if (phase !== 'ask') return;
          for (var q = 0; q < 4; q++) list[q].classList.toggle('on', list[q].dataset.v === v);
          if (which === 't') pickedT = v; else pickedR = v;
          state();
        };
      }
      for (k = 0; k < 4; k++) {
        btn1[k].addEventListener('click', choose(btn1, 't', TRENDS[k]));
        btn2[k].addEventListener('click', choose(btn2, 'r', RATES[k]));
      }

      /* --- feedback, built from the model ------------------------------ */
      var TE = {
        fall: 'A would fall',
        stay: function () { return 'A would hold at ' + R.nowA; },
        rise: 'A would rise',
        even: function () { return 'A and B would even out at ' + (N / 2) + ' each'; }
      };
      var RE = {
        stop: 'both reactions had stopped',
        fwd: 'the forward reaction was faster',
        rev: 'the reverse reaction was faster',
        eq: 'the two rates were equal'
      };
      function echo(map, key) { var v = map[key]; return typeof v === 'function' ? v() : v; }

      function happened() {
        return 'A went ' + R.nowA + ' → ' + R.nextA + ': ' +
               R.fwd + ' A→B and ' + R.rev + ' B→A.';
      }

      function verdictText(right, justMastered) {
        var lead = (right ? 'Right' : 'Not quite') + ' — you said ' +
          echo(TE, pickedT) + ' and ' + echo(RE, pickedR) + '. ';
        if (right) {
          if (justMastered) {
            return lead + 'Three in a row: you have it. Both reactions keep running at equal ' +
              'rates, so the amounts hold steady without being equal.';
          }
          if (R.shape === 'settled') {
            return lead + 'It did: ' + R.fwd + ' A→B and ' + R.rev + ' B→A in those 10 s. ' +
              'Equal rates hold the flask at ' + R.nowA + ' A and ' + (N - R.nowA) + ' B — steady, not equal.';
          }
          return lead + happened() + ' Both run; ' +
            (R.trend === 'fall' ? 'forward' : 'reverse') + ' is ahead, so the counts move on ' +
            'until the rates level at ' + Math.round(R.Aeq) + ' A.';
        }
        var fix;
        if (pickedR === 'stop') {
          fix = R.shape === 'settled'
            ? 'A flat line means the two rates are equal, not zero — the flask never goes quiet.'
            : 'The count is still moving, so nothing has stopped — nor will it once the line flattens.';
        } else if (pickedT === 'even') {
          fix = 'Equilibrium settles where the rates balance — ' + Math.round(R.Aeq) +
            ' A and ' + (N - Math.round(R.Aeq)) + ' B here, not ' + (N / 2) + ' each.';
        } else if (R.shape === 'settled') {
          fix = 'The counts have stopped changing, so neither direction can be ahead any more.';
        } else if (pickedR === 'eq' || pickedT === 'stay') {
          fix = 'While the counts are still moving, the two rates cannot be equal yet.';
        } else {
          fix = 'The graph is still ' + (R.trend === 'fall' ? 'falling, so the forward reaction is ahead.'
                                                           : 'rising, so the reverse reaction is ahead.');
        }
        return lead + happened() + ' ' + fix;
      }

      function say(right, text) {
        cap.textContent = '';
        var v = h('span', 'v ' + (right ? 'yes' : 'no'), text.slice(0, text.indexOf('—') + 1));
        cap.appendChild(v);
        cap.appendChild(document.createTextNode(text.slice(text.indexOf('—') + 1)));
        sr.textContent = text;
      }

      /* --- the reveal ---------------------------------------------------- */
      function apply(p) {
        var fF = Math.round(R.fwd * p), fR = Math.round(R.rev * p), q;
        for (q = 0; q < R.fwd; q++) ident[flipF[q]] = q < fF ? 'B' : 'A';
        for (q = 0; q < R.rev; q++) ident[flipR[q]] = q < fR ? 'A' : 'B';
        paintDots();
        tally.textContent = '10 s: ' + fF + ' A→B · ' + fR + ' B→A';
        futA.setAttribute('d', curve(R.tNow, R.tNow + WINDOW * p, false));
        futB.setAttribute('d', curve(R.tNow, R.tNow + WINDOW * p, true));
      }

      function play(done) {
        if (reduced) { apply(1); done(); return; }
        var s = 0;
        (function step() {
          if (!root.isConnected) { timer = null; return; }
          s++;
          apply(s / 10);
          if (s < 10) { timer = setTimeout(step, 105); }
          else { timer = null; done(); }
        })();
      }

      function commit() {
        if (phase === 'run') return;
        if (phase === 'done') { newRound(); return; }
        if (!pickedT || !pickedR) {
          cap.textContent = 'Choose what the number of A does next, and what the two rates are doing.';
          sr.textContent = cap.textContent;
          state({ incomplete: true });
          return;
        }
        var right = (pickedT === R.trend) && (pickedR === R.rates);
        phase = 'run';
        for (var b = 0; b < 4; b++) { btn1[b].disabled = true; btn2[b].disabled = true; }
        go.textContent = 'Watching…';
        attempted++;
        if (right) { streak++; if (streak >= 3) mastered = true; } else { streak = 0; }
        state();
        var justMastered = right && streak === 3;
        play(function () {
          phase = 'done';
          say(right, verdictText(right, justMastered));
          go.textContent = mastered ? 'Another anyway' : 'Next flask';
          go.classList.add('quiet');
          showRun();
          state({ correct: right });
        });
      }
      go.addEventListener('click', commit);

      newRound();
    }
  };
})();
