/* StudyVault lesson widget — photosynthesis-limiting-factor-plateau
   Self-contained. No imports, no network, no storage outside root. */
(function () {
  'use strict';

  /* ---------------------------------------------------------------
     ONE MODEL. Every curve, every verdict and every caption number
     comes from here, so the reveal cannot contradict the marking.
     Law of limiting factors: the rate is set by whichever factor is
     in shortest supply.
     Rate is in arbitrary units.
  ----------------------------------------------------------------*/
  function pLight(L) { return L; }              /* L in arbitrary units 0-10 */
  function pCO2(c) { return c * 100; }          /* c in % by volume          */
  function pTemp(T) {                           /* enzyme curve, T in °C     */
    return 12 * Math.pow(2, (T - 25) / 10) / (1 + Math.exp((T - 32) / 2.2));
  }
  function rateOf(s) { return Math.min(pLight(s.light), pCO2(s.co2), pTemp(s.temp)); }
  function limiterOf(s) {
    var best = 'light', bv = pLight(s.light), cv = pCO2(s.co2), tv = pTemp(s.temp);
    if (cv < bv) { bv = cv; best = 'co2'; }
    if (tv < bv) { bv = tv; best = 'temp'; }
    return best;
  }

  var NAME = { light: 'light intensity', co2: 'carbon dioxide', temp: 'temperature' };
  var NOUN = { light: 'light', co2: 'CO₂', temp: 'warmth' };
  var EPS = 0.15;

  function fmt(v) { return v.toFixed(1); }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function levelText(f, s) {
    return f === 'light' ? (fmt(s.light) + ' units')
      : f === 'co2' ? (s.co2.toFixed(2) + '%')
        : (s.temp + ' °C');
  }
  function clone(s) { return { light: s.light, co2: s.co2, temp: s.temp }; }
  function applyOpt(s, o) { var n = clone(s); n[o.factor] = o.to; return n; }

  /* Option labels are DERIVED from the model values, never authored,
     so a label can never disagree with what the option does. */
  function optLabel(s, o) {
    if (o.factor === 'light') return 'Turn the lamp up · ' + fmt(s.light) + ' → ' + fmt(o.to) + ' units';
    if (o.factor === 'co2') return 'Inject CO₂ · ' + s.co2.toFixed(2) + '% → ' + o.to.toFixed(2) + '%';
    return (o.to >= 34 ? 'Turn the heat up · ' : 'Warm the greenhouse · ')
      + s.temp + ' → ' + o.to + ' °C';
  }
  function optEcho(s, o) {
    if (o.factor === 'light') return 'turn the lamp up';
    if (o.factor === 'co2') return 'inject CO₂';
    return o.to >= 34 ? 'turn the heat up' : 'warm the greenhouse';
  }

  /* ---------------------------------------------------------------
     ROUND BANK — which factor is limiting rotates, and one round
     (r4) sits on the RISING limb so "more of the plotted factor"
     is sometimes the right call.
  ----------------------------------------------------------------*/
  var ROUNDS = [
    { id: 'r1', plot: 'light', state: { light: 8, co2: 0.04, temp: 20 },
      opts: [{ factor: 'light', to: 10 }, { factor: 'co2', to: 0.10 }, { factor: 'temp', to: 28 }] },
    { id: 'r2', plot: 'co2', state: { light: 3, co2: 0.10, temp: 20 },
      opts: [{ factor: 'co2', to: 0.14 }, { factor: 'light', to: 8 }, { factor: 'temp', to: 28 }] },
    { id: 'r3', plot: 'light', state: { light: 8, co2: 0.10, temp: 12 },
      opts: [{ factor: 'light', to: 10 }, { factor: 'temp', to: 25 }, { factor: 'co2', to: 0.14 }] },
    { id: 'r4', plot: 'light', state: { light: 3, co2: 0.07, temp: 25 },
      opts: [{ factor: 'light', to: 6 }, { factor: 'co2', to: 0.12 }, { factor: 'temp', to: 28 }] },
    { id: 'r5', plot: 'light', state: { light: 8, co2: 0.06, temp: 25 },
      opts: [{ factor: 'temp', to: 38 }, { factor: 'co2', to: 0.12 }, { factor: 'light', to: 10 }] },
    { id: 'r6', plot: 'co2', state: { light: 8, co2: 0.12, temp: 14 },
      opts: [{ factor: 'temp', to: 26 }, { factor: 'co2', to: 0.16 }, { factor: 'light', to: 10 }] }
  ];

  var PREDS = [
    { id: 'up', label: 'Rate rises', echo: 'rate rises' },
    { id: 'same', label: 'No change', echo: 'no change' },
    { id: 'down', label: 'Rate falls', echo: 'rate falls' }
  ];

  function outcomeOf(before, after) {
    var d = rateOf(after) - rateOf(before);
    return d > EPS ? 'up' : d < -EPS ? 'down' : 'same';
  }

  var AXIS = {
    light: { max: 10, ticks: [0, 2, 4, 6, 8, 10], fmt: function (v) { return String(v); },
      title: 'Light intensity (arbitrary units)' },
    co2: { max: 0.16, ticks: [0, 0.04, 0.08, 0.12, 0.16], fmt: function (v) { return v ? v.toFixed(2) : '0'; },
      title: 'Carbon dioxide concentration (%)' }
  };

  var CSS = [
    '.SVWROOT{background:#fff;border:1px solid #e8e3db;border-radius:16px;padding:.8rem .9rem .85rem;',
    'font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;',
    '-webkit-font-smoothing:antialiased;box-sizing:border-box;}',
    '.SVWROOT *{box-sizing:border-box;}',
    '.SVWROOT .p-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0;line-height:1.3;}',
    '.SVWROOT .p-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.16;margin:.05rem 0 0;}',
    '.SVWROOT .p-task{font-size:.82rem;line-height:1.38;color:#5b564e;margin:.2rem 0 .4rem;}',
    '.SVWROOT .p-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.35rem .45rem .25rem;}',
    '.SVWROOT .p-cond{font-size:.72rem;font-weight:600;letter-spacing:.02em;color:#8d8880;margin:0;line-height:1.3;',
    'font-variant-numeric:tabular-nums;}',
    '.SVWROOT .p-svg{display:block;width:100%;}',
    '.SVWROOT .p-step{display:flex;align-items:center;gap:.35rem;font-size:.74rem;font-weight:600;color:#5b564e;',
    'margin:.4rem 0 .2rem;line-height:1.3;}',
    '.SVWROOT .p-row2{display:flex;align-items:center;gap:.35rem;margin:.35rem 0 0;font-size:.74rem;',
    'font-weight:600;color:#5b564e;line-height:1.3;}',
    '.SVWROOT .p-num{display:inline-flex;align-items:center;justify-content:center;width:1rem;height:1rem;',
    'border-radius:50%;font-size:.64rem;font-weight:700;color:#2d2a26;flex:none;}',
    '.SVWROOT .p-opts{display:grid;grid-template-columns:1fr;gap:.26rem;}',
    '.SVWROOT.is-wide .p-opts{grid-template-columns:repeat(3,1fr);gap:.35rem;}',
    '.SVWROOT .p-preds{flex:1 1 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:.26rem;}',
    '.SVWROOT .p-btn{font:inherit;font-size:.8rem;font-weight:600;line-height:1.22;text-align:left;color:#2d2a26;',
    'background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.34rem .55rem;cursor:pointer;',
    'font-variant-numeric:tabular-nums;}',
    '.SVWROOT .p-preds .p-btn{text-align:center;padding:.34rem .2rem;font-size:.78rem;}',
    '.SVWROOT .p-btn[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
    '.SVWROOT .p-btn:disabled{cursor:default;opacity:.45;}',
    '.SVWROOT .p-btn[aria-pressed="true"]:disabled{opacity:1;}',
    '.SVWROOT .p-go{display:flex;align-items:center;gap:.55rem;margin-top:.45rem;}',
    '.SVWROOT .p-check{font:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;',
    'border-radius:10px;padding:.42rem .9rem;cursor:pointer;flex:none;}',
    '.SVWROOT .p-run{font-size:.74rem;color:#8d8880;line-height:1.3;}',
    '.SVWROOT .p-cap{font-size:.8rem;line-height:1.45;color:#2d2a26;margin:.45rem 0 0;min-height:4.5em;}',
    '.SVWROOT.is-wide .p-cap{min-height:3.5em;}',
    '.SVWROOT .p-verd{font-weight:700;}',
    '.SVWROOT .p-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;',
    'clip:rect(0 0 0 0);white-space:nowrap;border:0;}'
  ].join('');

  window.SVWidget = {
    meta: {
      id: 'photosynthesis-limiting-factor-plateau',
      title: 'What sets the rate?',
      teaches: 'A plateau means one factor has become limiting while the plotted factor keeps rising; raise the limiting factor and the whole plateau lifts.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var CLS = 'svw-plfp';
      root.className = (root.className ? root.className + ' ' : '') + CLS;

      var accent = (ctx.accent && String(ctx.accent).trim())
        || (getComputedStyle(root).getPropertyValue('--accent') || '').trim()
        || '#4f7d63';

      var style = document.createElement('style');
      style.textContent = CSS.replace(/SVWROOT/g, CLS);
      root.appendChild(style);

      /* ---------- markup, built once ---------- */
      function el(tag, cls, txt) {
        var n = document.createElement(tag);
        if (cls) n.className = cls;
        if (txt != null) n.textContent = txt;
        return n;
      }
      var kick = el('p', 'p-kick', 'Photosynthesis');
      kick.style.color = accent;
      var title = el('h3', 'p-title', 'What sets the rate?');
      var task = el('p', 'p-task', '');

      var stage = el('div', 'p-stage');
      var cond = el('p', 'p-cond', '');
      var SVGNS = 'http://www.w3.org/2000/svg';
      var svg = document.createElementNS(SVGNS, 'svg');
      svg.setAttribute('class', 'p-svg');
      svg.setAttribute('role', 'img');
      stage.appendChild(cond); stage.appendChild(svg);

      var step1 = el('div', 'p-step');
      var n1 = el('span', 'p-num', '1'); n1.style.background = accent + '33';
      step1.appendChild(n1); step1.appendChild(el('span', null, 'Change one thing in the greenhouse'));
      var opts = el('div', 'p-opts');

      var step2 = el('div', 'p-row2');
      var n2 = el('span', 'p-num', '2'); n2.style.background = accent + '33';
      var preds = el('div', 'p-preds');
      step2.appendChild(n2); step2.appendChild(el('span', null, 'Predict'));
      step2.appendChild(preds);

      var go = el('div', 'p-go');
      var check = el('button', 'p-check', 'Check');
      check.type = 'button';
      var run = el('p', 'p-run', '');
      go.appendChild(check); go.appendChild(run);

      var capEl = el('p', 'p-cap', '');
      var sr = el('p', 'p-sr', '');
      sr.setAttribute('aria-live', 'polite');

      [kick, title, task, stage, step1, opts, step2, go, capEl, sr]
        .forEach(function (n) { root.appendChild(n); });

      var optBtns = [], predBtns = [];
      var i;
      for (i = 0; i < 3; i++) {
        var ob = el('button', 'p-btn', '');
        ob.type = 'button'; ob.setAttribute('aria-pressed', 'false');
        ob.dataset.i = String(i);
        ob.addEventListener('click', onOpt);
        opts.appendChild(ob); optBtns.push(ob);
      }
      for (i = 0; i < PREDS.length; i++) {
        var pb = el('button', 'p-btn', PREDS[i].label);
        pb.type = 'button'; pb.setAttribute('aria-pressed', 'false');
        pb.dataset.i = String(i);
        pb.addEventListener('click', onPred);
        preds.appendChild(pb); predBtns.push(pb);
      }
      check.addEventListener('click', onCheck);
      root.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !S.revealed) { S.choice = null; S.pred = null; paint(); }
      });

      /* ---------- svg furniture, built once ---------- */
      function mk(tag, attrs) {
        var n = document.createElementNS(SVGNS, tag), k;
        for (k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
        return n;
      }
      var gGrid = mk('g', {}), gCurve = mk('g', {}), gMark = mk('g', {});
      svg.appendChild(gGrid); svg.appendChild(gCurve); svg.appendChild(gMark);

      var yLab = mk('text', { x: 0, y: 0, 'font-size': 10.5, fill: '#8d8880' });
      yLab.textContent = 'Rate of photosynthesis (arbitrary units)';
      yLab.setAttribute('font-size', 10);
      var xLab = mk('text', { x: 0, y: 0, 'font-size': 10.5, fill: '#8d8880', 'text-anchor': 'middle' });
      var axisX = mk('line', { stroke: '#c9c1b4', 'stroke-width': 1 });
      var axisY = mk('line', { stroke: '#c9c1b4', 'stroke-width': 1 });
      gGrid.appendChild(yLab); gGrid.appendChild(xLab);
      gGrid.appendChild(axisX); gGrid.appendChild(axisY);

      var curveOld = mk('polyline', { fill: 'none', stroke: '#b4ada1', 'stroke-width': 2, 'stroke-linejoin': 'round' });
      var curveNew = mk('polyline', { fill: 'none', stroke: accent, 'stroke-width': 2.6, 'stroke-linejoin': 'round' });
      gCurve.appendChild(curveOld); gCurve.appendChild(curveNew);

      var guideH = mk('line', { stroke: '#c9c1b4', 'stroke-width': 1, 'stroke-dasharray': '3 3' });
      var hop = mk('line', { stroke: accent, 'stroke-width': 1.4, 'stroke-dasharray': '4 3' });
      var ptOld = mk('circle', { r: 4, fill: '#2d2a26' });
      var ptNew = mk('circle', { r: 4.6, fill: accent });
      var valOld = mk('text', { 'font-size': 11, 'font-weight': 700, fill: '#2d2a26' });
      var valNew = mk('text', { 'font-size': 11, 'font-weight': 700, fill: accent });
      var nowLab = mk('text', { 'font-size': 9.5, fill: '#8d8880' });
      nowLab.textContent = 'now';
      gMark.appendChild(guideH); gMark.appendChild(hop);
      gMark.appendChild(ptOld); gMark.appendChild(ptNew);
      gMark.appendChild(valOld); gMark.appendChild(valNew); gMark.appendChild(nowLab);

      var tickPool = [];
      function tick(k) {
        while (tickPool.length <= k) {
          var g = mk('g', {});
          var ln = mk('line', { stroke: '#c9c1b4', 'stroke-width': 1 });
          var tx = mk('text', { 'font-size': 10, fill: '#8d8880', 'text-anchor': 'middle' });
          g.appendChild(ln); g.appendChild(tx);
          gGrid.appendChild(g);
          tickPool.push({ g: g, ln: ln, tx: tx });
        }
        return tickPool[k];
      }
      var yPool = [];
      function ytick(k) {
        while (yPool.length <= k) {
          var g = mk('g', {});
          var ln = mk('line', { stroke: '#efe9e0', 'stroke-width': 1 });
          var tx = mk('text', { 'font-size': 10, fill: '#8d8880', 'text-anchor': 'end' });
          g.appendChild(ln); g.appendChild(tx);
          gGrid.appendChild(g);
          yPool.push({ g: g, ln: ln, tx: tx });
        }
        return yPool[k];
      }

      /* ---------- state ---------- */
      var order = shuffle([0, 1, 2, 3, 4, 5]);
      var S = { qi: 0, choice: null, pred: null, revealed: false, correct: false,
        streak: 0, attempted: 0, mastered: false, wide: false };

      function shuffle(a) {
        var i, j, t;
        for (i = a.length - 1; i > 0; i--) { j = Math.floor(Math.random() * (i + 1)); t = a[i]; a[i] = a[j]; a[j] = t; }
        return a;
      }
      function round() { return ROUNDS[order[S.qi % order.length]]; }

      /* ---------- geometry + drawing ---------- */
      function draw() {
        var R = round(), ax = AXIS[R.plot];
        var w = Math.max(240, Math.round(root.clientWidth - 32));
        var h = S.wide ? 150 : 122;
        svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
        svg.setAttribute('width', w); svg.setAttribute('height', h);
        svg.style.height = h + 'px';

        var padL = 24, padR = 14, padT = 14, padB = 25;
        var x0 = padL, x1 = w - padR, y0 = padT, y1 = h - padB;
        var YMAX = 10;
        function X(v) { return x0 + (v / ax.max) * (x1 - x0); }
        function Y(v) { return y1 - (v / YMAX) * (y1 - y0); }

        yLab.setAttribute('x', 1); yLab.setAttribute('y', padT - 5);
        xLab.setAttribute('x', (x0 + x1) / 2); xLab.setAttribute('y', h - 4);
        xLab.textContent = ax.title;
        axisX.setAttribute('x1', x0); axisX.setAttribute('x2', x1);
        axisX.setAttribute('y1', y1); axisX.setAttribute('y2', y1);
        axisY.setAttribute('x1', x0); axisY.setAttribute('x2', x0);
        axisY.setAttribute('y1', y0); axisY.setAttribute('y2', y1);

        var k;
        for (k = 0; k < tickPool.length; k++) tickPool[k].g.setAttribute('display', 'none');
        for (k = 0; k < ax.ticks.length; k++) {
          var t = tick(k), tv = ax.ticks[k], tx = X(tv);
          t.g.removeAttribute('display');
          t.ln.setAttribute('x1', tx); t.ln.setAttribute('x2', tx);
          t.ln.setAttribute('y1', y1); t.ln.setAttribute('y2', y1 + 4);
          t.tx.setAttribute('x', tx); t.tx.setAttribute('y', y1 + 14);
          t.tx.textContent = ax.fmt(tv);
        }
        var yts = [0, 5, 10];
        for (k = 0; k < yts.length; k++) {
          var yt = ytick(k), yv = yts[k], yy = Y(yv);
          yt.ln.setAttribute('x1', x0); yt.ln.setAttribute('x2', x1);
          yt.ln.setAttribute('y1', yy); yt.ln.setAttribute('y2', yy);
          yt.tx.setAttribute('x', x0 - 5); yt.tx.setAttribute('y', yy + 3.5);
          yt.tx.textContent = String(yv);
        }

        function series(state) {
          var pts = [], n = 60, j, xv, st;
          for (j = 0; j <= n; j++) {
            xv = ax.max * j / n;
            st = clone(state); st[R.plot] = xv;
            pts.push(X(xv).toFixed(1) + ',' + Y(rateOf(st)).toFixed(1));
          }
          return pts.join(' ');
        }

        var before = R.state;
        curveOld.setAttribute('points', series(before));
        var bx = X(before[R.plot]), by = Y(rateOf(before));
        ptOld.setAttribute('cx', bx); ptOld.setAttribute('cy', by);
        guideH.setAttribute('x1', x0); guideH.setAttribute('x2', bx);
        guideH.setAttribute('y1', by); guideH.setAttribute('y2', by);
        valOld.setAttribute('x', Math.min(bx + 7, x1 - 24)); valOld.setAttribute('y', by - 7);
        valOld.textContent = fmt(rateOf(before));
        nowLab.setAttribute('x', Math.min(bx + 7, x1 - 24)); nowLab.setAttribute('y', by + 14);

        if (S.revealed) {
          var o = R.opts[S.choice], after = applyOpt(before, o);
          var oldPts = curveOld.getAttribute('points'), newPts = series(after);
          var nx = X(after[R.plot]), ny = Y(rateOf(after));
          var moved = Math.abs(nx - bx) > 1 || Math.abs(ny - by) > 1;
          /* A curve identical to the grey one is not news: when the point has
             slid along it, leave the single grey curve so the slide reads. */
          if (newPts !== oldPts || !moved) {
            curveNew.setAttribute('points', newPts);
            curveNew.removeAttribute('display');
          } else {
            curveNew.setAttribute('display', 'none');
          }
          ptNew.setAttribute('cx', nx); ptNew.setAttribute('cy', ny);
          ptNew.removeAttribute('display');
          hop.setAttribute('x1', bx); hop.setAttribute('y1', by);
          hop.setAttribute('x2', nx); hop.setAttribute('y2', ny);
          hop.removeAttribute('display');
          ptOld.setAttribute('fill', '#fff');
          ptOld.setAttribute('stroke', '#8d8880');
          ptOld.setAttribute('stroke-width', 1.4);
          valOld.setAttribute('fill', '#8d8880');
          var sameSpot = Math.abs(nx - bx) < 3 && Math.abs(ny - by) < 3;
          valNew.setAttribute('x', Math.min(nx + 7, x1 - 24));
          valNew.setAttribute('y', sameSpot ? ny + 18 : ny - 7);
          valNew.textContent = fmt(rateOf(after));
          valNew.removeAttribute('display');
          nowLab.setAttribute('display', 'none');
        } else {
          curveNew.setAttribute('display', 'none');
          ptNew.setAttribute('display', 'none');
          hop.setAttribute('display', 'none');
          valNew.setAttribute('display', 'none');
          nowLab.removeAttribute('display');
          ptOld.setAttribute('fill', '#2d2a26');
          ptOld.removeAttribute('stroke');
          valOld.setAttribute('fill', '#2d2a26');
        }
      }

      /* ---------- prose, all derived ---------- */
      function taskText(R) {
        return R.plot === 'light'
          ? 'A grower records the rate of photosynthesis as the lamp is turned up. Choose one change to the greenhouse and predict its effect.'
          : 'A grower records the rate of photosynthesis as CO₂ is added to the air. Choose one change to the greenhouse and predict its effect.';
      }
      function condText(R) {
        return R.plot === 'light'
          ? 'Graph plotted at CO₂ ' + R.state.co2.toFixed(2) + '% and ' + R.state.temp + ' °C'
          : 'Graph plotted at light ' + fmt(R.state.light) + ' units and ' + R.state.temp + ' °C';
      }
      function feedback(R, o, predId) {
        var before = R.state, after = applyOpt(before, o);
        var r0 = rateOf(before), r1 = rateOf(after);
        var out = outcomeOf(before, after);
        var lim = limiterOf(before), newLim = limiterOf(after);
        var right = out === predId;

        var verdict = right ? 'Right' : 'Not quite';
        var echo = ' you said ' + optEcho(before, o) + ', '
          + PREDS[predId === 'up' ? 0 : predId === 'same' ? 1 : 2].echo + '. ';
        var body;
        if (out === 'down') {
          body = 'It drops from ' + fmt(r0) + ' to ' + fmt(r1) + '. Past about 28 °C the enzymes denature, so the ceiling itself collapses — that is damage, not a shortage, and no extra light or CO₂ can undo it.';
        } else if (out === 'up') {
          body = 'It climbs from ' + fmt(r0) + ' to ' + fmt(r1) + '. ';
          if (newLim === o.factor) {
            body += cap(NAME[lim]) + ' was the shortage and still is — you have moved further up the rising part of the curve.';
          } else {
            body += cap(NAME[lim]) + ' was in shortest supply, so raising it lifts the whole plateau. '
              + cap(NAME[newLim]) + ' sets the ceiling now.';
          }
        } else {
          body = 'It stays at ' + fmt(r0) + '. ' + cap(NAME[lim]) + ' at ' + levelText(lim, before)
            + ' is the limiting factor, so the extra ' + NOUN[o.factor] + ' cannot be used. ';
          body += (o.factor === R.plot)
            ? cap(NOUN[o.factor]) + ' has not stopped working — lower down the curve it still sets the rate.'
            : 'Raise that instead and the whole plateau lifts.';
        }
        return { right: right, verdict: verdict, echo: echo, body: body, out: out };
      }

      /* ---------- painting ---------- */
      function paint() {
        var R = round(), i;
        task.textContent = taskText(R);
        cond.textContent = condText(R);
        for (i = 0; i < 3; i++) {
          optBtns[i].textContent = optLabel(R.state, R.opts[i]);
          optBtns[i].setAttribute('aria-pressed', S.choice === i ? 'true' : 'false');
          optBtns[i].disabled = S.revealed;
        }
        for (i = 0; i < PREDS.length; i++) {
          predBtns[i].setAttribute('aria-pressed', S.pred === PREDS[i].id ? 'true' : 'false');
          predBtns[i].disabled = S.revealed;
        }
        n1.style.background = S.choice == null ? accent + '33' : '#e8e2d9';
        n2.style.background = S.pred == null ? accent + '33' : '#e8e2d9';
        check.textContent = S.revealed ? (S.mastered ? 'Another anyway' : 'Next') : 'Check';
        run.textContent = S.mastered ? 'You have it.'
          : S.attempted === 0 ? ''
            : S.streak === 0 ? 'Run reset — three in a row ends it.'
              : S.streak === 1 ? '1 right in a row — two more.'
                : '2 right in a row — one more and you have it.';
        draw();
      }

      function setCap(html) { capEl.innerHTML = html; }

      function openingCap() {
        setCap('Rate is in arbitrary units. Whichever factor is in shortest supply is the '
          + '<strong>limiting factor</strong> — it fixes the ceiling the rate cannot pass.');
      }

      function state(extra) {
        var o = { round: round().id, streak: S.streak, mastered: S.mastered, attempted: S.attempted };
        if (extra) for (var k in extra) if (Object.prototype.hasOwnProperty.call(extra, k)) o[k] = extra[k];
        root.dataset.svState = JSON.stringify(o);
      }

      function onOpt(e) {
        if (S.revealed) return;
        S.choice = parseInt(e.currentTarget.dataset.i, 10);
        paint();
        state({ choice: S.choice, prediction: S.pred });
      }
      function onPred(e) {
        if (S.revealed) return;
        S.pred = PREDS[parseInt(e.currentTarget.dataset.i, 10)].id;
        paint();
        state({ choice: S.choice, prediction: S.pred });
      }

      function onCheck() {
        var R = round();
        if (S.revealed) { next(); return; }
        if (S.choice == null || S.pred == null) {
          setCap('Pick a change (1) and a prediction (2), then press Check.');
          n1.style.background = S.choice == null ? accent + '77' : '#e8e2d9';
          n2.style.background = S.pred == null ? accent + '77' : '#e8e2d9';
          sr.textContent = 'A change and a prediction are both needed.';
          return;
        }
        var o = R.opts[S.choice];
        var fb = feedback(R, o, S.pred);
        S.revealed = true; S.correct = fb.right; S.attempted++;
        S.streak = fb.right ? S.streak + 1 : 0;
        var justMastered = false;
        if (S.streak >= 3 && !S.mastered) { S.mastered = true; justMastered = true; }
        var tail = justMastered
          ? ' <strong>Three in a row — you have it:</strong> a plateau marks a limiting factor, not a maximum.'
          : '';
        setCap('<span class="p-verd" style="color:' + (fb.right ? '#4f7d63' : '#2d2a26') + '">'
          + fb.verdict + ' —</span>' + fb.echo + fb.body + tail);
        sr.textContent = (fb.right ? 'Correct. ' : 'Incorrect. ') + fb.body;
        paint();
        state({ choice: S.choice, prediction: S.pred, correct: fb.right,
          rateBefore: +fmt(rateOf(R.state)), rateAfter: +fmt(rateOf(applyOpt(R.state, o))) });
      }

      function next() {
        S.qi++;
        if (S.qi % order.length === 0) {
          var last = order[order.length - 1];
          shuffle(order);
          if (order[0] === last) { order.push(order.shift()); }
        }
        S.choice = null; S.pred = null; S.revealed = false;
        openingCap();
        paint();
        state({});
      }

      /* ---------- size ---------- */
      function measure() {
        var w = root.clientWidth || 360;
        var wide = w >= 560;
        if (wide !== S.wide) { S.wide = wide; root.classList.toggle('is-wide', wide); }
        draw();
      }
      if (typeof ResizeObserver === 'function') {
        var ro = new ResizeObserver(measure);
        ro.observe(root);
      } else if (window.addEventListener) {
        window.addEventListener('resize', measure);
      }
      /* ctx.reducedMotion needs no branch: nothing here animates or transitions. */

      openingCap();
      measure();
      paint();
      state({});
    }
  };
}());
