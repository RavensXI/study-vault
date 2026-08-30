/* reinforced-concrete-embedding
   Where the steel has to be, and why the answer flips.

   One structural model decides everything on screen: the support
   reactions, the bending moment along the member, the deflected shape
   that gets drawn, which face is in tension, and therefore the correct
   answer. No round hard-codes "low" or "high". */
(function () {
  'use strict';

  /* ---------------------------------------------------------------
     1. The model
     --------------------------------------------------------------- */

  var N = 96;               /* stations along the member, x = 0..1 */

  /* every load becomes a list of point loads, so one moment routine
     serves both a slab pressing down evenly and a tank sitting on a spot */
  function pointsFrom(sc) {
    var out = [];
    (sc.loads || []).forEach(function (ld) {
      if (ld.kind === 'point') { out.push({ x: ld.x, P: ld.P }); return; }
      var n = 32, w = (ld.to - ld.from) / n, i;
      for (i = 0; i < n; i++) out.push({ x: ld.from + w * (i + 0.5), P: ld.w * w });
    });
    return out;
  }

  function interp(arr, f) {
    var t = f * N, i0 = Math.floor(t);
    if (i0 >= N) return arr[N];
    if (i0 < 0) return arr[0];
    var k = t - i0;
    return arr[i0] * (1 - k) + arr[i0 + 1] * k;
  }

  function analyse(sc) {
    var xs = [], M = [], i, j, x, m;
    for (i = 0; i <= N; i++) xs.push(i / N);

    var P = pointsFrom(sc), W = 0, Ma = 0;
    for (j = 0; j < P.length; j++) W += P[j].P;

    if (sc.axial) {
      /* the load runs straight down the member's own line: no bending */
      for (i = 0; i <= N; i++) M.push(0);
    } else if (sc.geom === 'cant') {
      /* built in at x = 0: a vertical reaction plus a fixing moment */
      for (j = 0; j < P.length; j++) Ma += P[j].P * P[j].x;
      for (i = 0; i <= N; i++) {
        x = xs[i]; m = -Ma + W * x;
        for (j = 0; j < P.length; j++) if (P[j].x < x) m -= P[j].P * (x - P[j].x);
        M.push(m);
      }
    } else {
      /* two simple supports, with or without an overhang past one of them */
      var a = sc.sup[0], b = sc.sup[1];
      for (j = 0; j < P.length; j++) Ma += P[j].P * (P[j].x - a);
      var Rb = Ma / (b - a), Ra = W - Rb;
      for (i = 0; i <= N; i++) {
        x = xs[i]; m = 0;
        if (a < x) m += Ra * (x - a);
        if (b < x) m += Rb * (x - b);
        for (j = 0; j < P.length; j++) if (P[j].x < x) m -= P[j].P * (x - P[j].x);
        M.push(m);
      }
    }

    /* deflected shape: curvature follows the bending moment, integrated
       twice, then pinned back onto the supports. v is measured downward. */
    var dx = 1 / N, th = [0], v = [0];
    for (i = 1; i <= N; i++) {
      th.push(th[i - 1] + (-(M[i] + M[i - 1]) / 2) * dx);
      v.push(v[i - 1] + (th[i] + th[i - 1]) / 2 * dx);
    }
    if (!sc.axial && sc.geom !== 'cant') {
      var va = interp(v, sc.sup[0]), vb = interp(v, sc.sup[1]);
      var beta = -(vb - va) / (sc.sup[1] - sc.sup[0]);
      var alpha = -va - beta * sc.sup[0];
      for (i = 0; i <= N; i++) v[i] += alpha + beta * xs[i];
    }

    var peak = 0, pi = 0;
    for (i = 0; i <= N; i++) if (Math.abs(M[i]) > Math.abs(peak)) { peak = M[i]; pi = i; }

    /* sagging (positive) stretches the underside; hogging stretches the
       top; no bending stretches neither face. Explicit epsilon scaled to
       the load, never a bare float comparison. */
    var eps = 1e-6 * Math.max(W, 1e-6);
    var face = Math.abs(peak) < eps ? 'none' : (peak > 0 ? 'low' : 'high');

    var big = 0;
    for (i = 0; i <= N; i++) big = Math.max(big, Math.abs(v[i]));
    var shape = [];
    for (i = 0; i <= N; i++) shape.push(big > 0 ? v[i] / big : 0);

    return { face: face, shape: shape, peakX: xs[pi] };
  }

  /* ---------------------------------------------------------------
     2. The rounds
     --------------------------------------------------------------- */

  var ROUNDS = [
    { id: 'floor-beam', mode: 'bars', geom: 'beam', sup: [0, 1],
      loads: [{ kind: 'udl', from: 0, to: 1, w: 1 }],
      scenario: 'A concrete floor beam spans between two walls, with the floor above pressing down along its length.',
      mech: 'The beam sags between its two supports: the underside is pulled longer, the top squashed shorter.',
      win: 'Concrete splits where it is pulled, so the main bars belong low — buried just inside the stretched face.' },

    { id: 'balcony', mode: 'bars', geom: 'cant',
      loads: [{ kind: 'point', x: 1, P: 1 }],
      scenario: 'A balcony slab is built into the wall at one end only. People stand at its free outer edge.',
      mech: 'Held at one end only, the slab hogs: the top is pulled longer while the underside is squashed.',
      win: 'So the bars sit high here, near the top — the opposite of a beam held up at both ends.' },

    { id: 'crack-lintel', mode: 'crack', geom: 'beam', sup: [0, 1],
      loads: [{ kind: 'udl', from: 0, to: 1, w: 1 }],
      scenario: 'A plain concrete lintel rests on brickwork each side of a window. The wall above presses down on it.',
      mech: 'The lintel sags between the walls it rests on: the underside is pulled longer, the top squashed.',
      win: 'Plain concrete splits from the stretched face upward. Bars buried low would have held that crack shut.' },

    { id: 'column', mode: 'bars', geom: 'column', axial: true,
      loads: [{ kind: 'point', x: 0.5, P: 1 }],
      scenario: 'A column carries the beams of the floor above. The load presses straight down the column line.',
      mech: 'The load runs down the column’s own line, so the whole cross-section is squashed at once.',
      win: 'Columns still get steel — vertical bars and links stop a tall one bowing — but no face is stretched.' },

    { id: 'canopy', mode: 'bars', geom: 'cant',
      loads: [{ kind: 'udl', from: 0, to: 1, w: 1 }],
      scenario: 'A concrete canopy over the doors is built into the wall at one end only. Wet snow lies evenly on it.',
      mech: 'Held at one end only, the canopy hogs: the top is pulled longer, the underside squashed shorter.',
      win: 'So the bars run high, near the top, and carry on into the wall — that is where the pull is worst.' },

    { id: 'plant-beam', mode: 'bars', geom: 'beam', sup: [0, 1],
      loads: [{ kind: 'point', x: 0.35, P: 1 }],
      scenario: 'A concrete beam spans between two columns. A heavy water tank sits on it a third of the way along.',
      mech: 'The beam sags under the tank: the underside is pulled longer and the top is squashed shorter.',
      win: 'So the main bars stay low, near the underside, right through the length that sags.' },

    { id: 'walkway', mode: 'bars', geom: 'over', sup: [0, 0.6],
      loads: [{ kind: 'udl', from: 0, to: 1, w: 1 }, { kind: 'point', x: 1, P: 0.15 }],
      scenario: 'A walkway slab rests on two columns and reaches past the outer one. People stand on that far tip.',
      mech: 'The loaded tip drops and levers the slab over the outer column, so the slab hogs across that support.',
      win: 'The top is pulled longest there, so the main bars run high over that column, not low.' },

    { id: 'crack-canopy', mode: 'crack', geom: 'cant',
      loads: [{ kind: 'point', x: 1, P: 1 }],
      scenario: 'A plain concrete canopy is built into the wall at one end only, with a heavy sign hung at its tip.',
      mech: 'Held at one end only, the canopy hogs: the top is pulled longer, the underside squashed shorter.',
      win: 'Plain concrete splits from the stretched face, so it opens on top at the wall — where rebar should be.' }
  ];

  var ASK = {
    bars: 'Which face gets stretched — and where must the main steel bars (rebar) sit?',
    crack: 'There is no rebar in it at all — where does the first crack open?'
  };

  var OPTS = [
    { key: 'high', word: 'High', bars: 'near the top face', crack: 'from the top face' },
    { key: 'mid', word: 'Mid-depth', bars: 'in the middle', crack: 'from the middle' },
    { key: 'low', word: 'Low', bars: 'near the bottom face', crack: 'from the bottom face' },
    { key: 'none', word: 'Neither', bars: 'nothing is stretched', crack: 'it does not crack' }
  ];

  var ECHO = {
    bars: {
      high: 'you put the bars high, near the top.',
      mid: 'you put the bars at mid-depth.',
      low: 'you put the bars low, near the bottom.',
      none: 'you said neither face is stretched.'
    },
    crack: {
      high: 'you said it cracks from the top face.',
      mid: 'you said it cracks from mid-depth.',
      low: 'you said it cracks from the bottom face.',
      none: 'you said it does not crack.'
    }
  };

  function diagnose(chosen, face, mode) {
    if (face === 'none') {
      return 'Nothing here is pulled longer: the load runs straight down the column’s own line.';
    }
    if (chosen === 'none') {
      return 'Anything held up and then loaded bends, and bending always stretches one face.';
    }
    if (chosen === 'mid') {
      return mode === 'crack'
        ? 'At mid-depth the concrete hardly changes length, so nothing there is pulled far enough to split.'
        : 'At mid-depth the concrete hardly changes length, so bars there have almost nothing to hold together.';
    }
    return mode === 'crack'
      ? 'That face is being squashed shorter, and squashing is the job concrete is already good at.'
      : 'That face is being squashed, and concrete is strong in compression — it needs no help there.';
  }

  var OPENER = 'Concrete is strong in compression — being squashed — but weak in tension, being pulled longer. Steel is strong in tension. That is why the two are used together; the question is always where the steel has to be.';
  var OPENER2 = 'Concrete is weak in tension — being pulled longer — and steel is strong in it. So find the face that gets stretched.';
  var MASTER = 'Three in a row: you have it. Steel goes where the concrete is stretched — low where a member sags, high where it hogs over a support — and it is buried inside, not bolted on, so the cover keeps fire and rust off it.';

  /* ---------------------------------------------------------------
     3. Drawing constants
     --------------------------------------------------------------- */

  var VB_W = 320, VB_H = 116;
  var MID_Y = 70, DEPTH = 44, COVER = 7, EXAG = 11;
  var CONCRETE = '#eee9df', SQUASHED = '#e0dad0';
  var NS = 'http://www.w3.org/2000/svg';

  /* the face labels sit on an opaque plate of their own band colour, so a
     bar or a crack passing behind a word never cuts through the letters */
  function blend(hex, base, t) {
    function parts(h) {
      h = h.replace('#', '');
      if (h.length === 3) { h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2]; }
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
    }
    var a, b, out = '#', i, v;
    try { a = parts(hex); b = parts(base); } catch (e) { return base; }
    for (i = 0; i < 3; i++) {
      v = Math.round(b[i] + (a[i] - b[i]) * t);
      v = Math.max(0, Math.min(255, v));
      out += ('0' + v.toString(16)).slice(-2);
    }
    return out;
  }

  function svgEl(tag, attrs) {
    var e = document.createElementNS(NS, tag), k;
    for (k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) e.setAttribute(k, attrs[k]);
    return e;
  }

  function span(sc) {
    return sc.geom === 'cant' ? [30, 292] : [26, 294];
  }

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  var CSS = [
    '.svw-rce{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26}',
    '.svw-rce *{box-sizing:border-box}',
    '.svw-rce .rce-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--rce-a);margin:0 0 .2rem}',
    '.svw-rce .rce-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.2;margin:0 0 .3rem}',
    '.svw-rce .rce-frame{font-size:.85rem;line-height:1.42;margin:0 0 .55rem;color:#3d3a35}',
    '.svw-rce .rce-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem;margin:0 0 .6rem}',
    '.svw-rce .rce-stage svg{display:block;width:100%;max-width:400px;height:auto;margin:0 auto}',
    '.svw-rce .rce-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(138px,1fr));gap:.4rem;margin:0 0 .5rem}',
    '.svw-rce .rce-opt{appearance:none;text-align:left;font-family:inherit;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.4rem .55rem;cursor:pointer;color:#2d2a26}',
    '.svw-rce .rce-opt b{display:block;font-size:.82rem;font-weight:600;line-height:1.25}',
    '.svw-rce .rce-opt i{display:block;font-style:normal;font-size:.72rem;line-height:1.25;color:#8d8880}',
    '.svw-rce .rce-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-rce .rce-opt[aria-pressed="true"] i{color:#d8d2c8}',
    '.svw-rce .rce-opt[data-ans="1"]{box-shadow:0 0 0 2px var(--rce-a);border-color:var(--rce-a)}',
    '.svw-rce .rce-opt:disabled{cursor:default}',
    '.svw-rce .rce-go{appearance:none;font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-rce .rce-go:disabled{background:#faf8f5;border-color:#e0d9cd;color:#b3aca1;cursor:default}',
    '.svw-rce .rce-run{font-size:.76rem;color:#8d8880;min-height:1.05rem;margin:.35rem 0 .1rem;font-variant-numeric:tabular-nums}',
    '.svw-rce .rce-cap{font-size:.84rem;line-height:1.48;margin:0;padding:.5rem 0 0;border-top:1px solid #efe9e0;min-height:5rem;color:#3d3a35}',
    '.svw-rce .rce-cap b{font-weight:600}',
    '.svw-rce .rce-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
  ].join('');

  /* ---------------------------------------------------------------
     4. The widget
     --------------------------------------------------------------- */

  window.SVWidget = {
    meta: {
      id: 'reinforced-concrete-embedding',
      title: 'Where does the steel go?',
      teaches: 'Steel sits where the concrete is being stretched — low in a sagging beam, high over a cantilever support — and it is buried inside the concrete, not fixed to its surface.'
    },

    mount: function (root, ctx) {
      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
                   ((ctx && ctx.accent) || '#8a6a4f');
      var reduced = !!(ctx && ctx.reducedMotion);

      root.classList.add('svw-rce');
      root.innerHTML = '';
      root.style.setProperty('--rce-a', accent);
      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      /* the sagging beam, then the cantilever that flips the answer, then
         a crack round; everything else shuffled behind them */
      var order = [0, 1, 2], tail = [3, 4, 5, 6, 7], i, j, t;
      for (i = tail.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1)); t = tail[i]; tail[i] = tail[j]; tail[j] = t;
      }
      order = order.concat(tail);

      var pos = 0, sc = ROUNDS[order[0]], model = analyse(sc);
      var chosen = null, revealed = false, streak = 0, attempted = 0, mastered = false;
      var bend = 0, raf = 0;

      /* ---- markup, built once and then mutated ---- */
      var head = document.createElement('div');
      head.innerHTML = '<p class="rce-kick"></p><h3 class="rce-title"></h3><p class="rce-frame"></p>';
      root.appendChild(head);
      head.querySelector('.rce-kick').textContent = 'Reinforced concrete';
      head.querySelector('.rce-title').textContent = 'Where does the steel go?';
      var frame = head.querySelector('.rce-frame');

      var stage = document.createElement('div');
      stage.className = 'rce-stage';
      root.appendChild(stage);

      var STRETCHED = blend(accent, CONCRETE, 0.26);

      var svg = svgEl('svg', { viewBox: '0 0 ' + VB_W + ' ' + VB_H, role: 'img' });
      var gFurn = svgEl('g', {});
      var pMember = svgEl('path', { fill: CONCRETE, stroke: '#b7ae9e', 'stroke-width': '1.2', 'stroke-linejoin': 'round' });
      var pComp = svgEl('path', { fill: SQUASHED, stroke: 'none', opacity: '0' });
      var pTens = svgEl('path', { fill: STRETCHED, stroke: 'none', opacity: '0' });
      var pGhost = svgEl('path', { fill: 'none', stroke: '#9b948a', 'stroke-width': '1.6', 'stroke-dasharray': '5 4', 'stroke-linecap': 'round', opacity: '0' });
      var pBar = svgEl('path', { fill: 'none', stroke: accent, 'stroke-width': '3', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', opacity: '0' });
      var pCrack = svgEl('path', { fill: 'none', stroke: '#2d2a26', 'stroke-width': '2.2', 'stroke-linejoin': 'round', 'stroke-linecap': 'round', opacity: '0' });
      var tTop = svgEl('text', { 'text-anchor': 'middle', 'font-size': '11', 'font-weight': '700', 'letter-spacing': '.5', 'paint-order': 'stroke', 'stroke-width': '4', 'stroke-linejoin': 'round', opacity: '0' });
      var tBot = svgEl('text', { 'text-anchor': 'middle', 'font-size': '11', 'font-weight': '700', 'letter-spacing': '.5', 'paint-order': 'stroke', 'stroke-width': '4', 'stroke-linejoin': 'round', opacity: '0' });
      svg.appendChild(gFurn);
      svg.appendChild(pMember); svg.appendChild(pComp); svg.appendChild(pTens);
      svg.appendChild(pGhost); svg.appendChild(pBar); svg.appendChild(pCrack);
      svg.appendChild(tTop); svg.appendChild(tBot);
      stage.appendChild(svg);

      var opts = document.createElement('div');
      opts.className = 'rce-opts';
      root.appendChild(opts);
      var btns = OPTS.map(function (o) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'rce-opt'; b.setAttribute('aria-pressed', 'false');
        b.innerHTML = '<b></b><i></i>';
        b.addEventListener('click', function () { pick(o.key); });
        opts.appendChild(b);
        return b;
      });

      var go = document.createElement('button');
      go.type = 'button'; go.className = 'rce-go'; go.textContent = 'Check it'; go.disabled = true;
      root.appendChild(go);

      var run = document.createElement('p'); run.className = 'rce-run'; root.appendChild(run);
      var cap = document.createElement('p'); cap.className = 'rce-cap'; root.appendChild(cap);
      var sr = document.createElement('p'); sr.className = 'rce-sr';
      sr.setAttribute('aria-live', 'polite'); root.appendChild(sr);

      go.addEventListener('click', function () { if (revealed) { next(); } else { commit(); } });
      root.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !revealed && chosen) { pick(null); }
      });

      /* ---- geometry, driven by the model ---- */
      function centreLine(t2) {
        var pts = [], s = span(sc), x0 = s[0], x1 = s[1], k, f;
        for (k = 0; k <= 40; k++) {
          f = k / 40;
          pts.push({ x: x0 + (x1 - x0) * f, y: MID_Y + interp(model.shape, f) * EXAG * t2 });
        }
        return pts;
      }
      function edge(pts, off) {
        var d = '', k;
        for (k = 0; k < pts.length; k++) d += (k ? 'L' : 'M') + pts[k].x.toFixed(1) + ' ' + (pts[k].y + off).toFixed(1);
        return d;
      }
      function band(pts, o1, o2) {
        var d = edge(pts, o1), k;
        for (k = pts.length - 1; k >= 0; k--) d += 'L' + pts[k].x.toFixed(1) + ' ' + (pts[k].y + o2).toFixed(1);
        return d + 'Z';
      }
      /* main bars, hooked back into the member at each end the way rebar is */
      function barPath(pts, off) {
        var hook = off > 0 ? -5 : 5, a = pts[0], z = pts[pts.length - 1], k, d;
        d = 'M' + a.x.toFixed(1) + ' ' + (a.y + off + hook).toFixed(1);
        for (k = 0; k < pts.length; k++) d += 'L' + pts[k].x.toFixed(1) + ' ' + (pts[k].y + off).toFixed(1);
        return d + 'L' + z.x.toFixed(1) + ' ' + (z.y + off + hook).toFixed(1);
      }
      function arrowPath(x, y1, y2) {
        return 'M' + x + ' ' + y1 + 'L' + x + ' ' + y2 +
               'M' + (x - 3.2) + ' ' + (y2 - 4.8) + 'L' + x + ' ' + y2 + 'L' + (x + 3.2) + ' ' + (y2 - 4.8);
      }
      function hatch(g, x0, y0, x1, y1, n) {
        for (var k = 0; k < n; k++) {
          var f = (k + 0.5) / n;
          g.appendChild(svgEl('line', {
            x1: x0 + (x1 - x0) * f, y1: y0, x2: x0 + (x1 - x0) * f - 5, y2: y1,
            stroke: '#b9b1a4', 'stroke-width': '1'
          }));
        }
      }

      /* walls, supports and load arrows change only when the round does */
      function drawFurniture() {
        gFurn.textContent = '';
        var s = span(sc), x0 = s[0], x1 = s[1], k;

        if (sc.geom === 'column') {
          gFurn.appendChild(svgEl('rect', { x: 128, y: 96, width: 64, height: 10, fill: '#e2ddd2', stroke: '#b9b1a4', 'stroke-width': '1' }));
          hatch(gFurn, 128, 106, 192, 112, 6);
          gFurn.appendChild(svgEl('line', { x1: 134, y1: 26, x2: 186, y2: 26, stroke: '#b9b1a4', 'stroke-width': '2' }));
          for (k = 0; k < 3; k++) {
            gFurn.appendChild(svgEl('path', {
              d: arrowPath(146 + k * 14, 6, 23), fill: 'none', stroke: '#6f6a62',
              'stroke-width': '1.5', 'stroke-linecap': 'round'
            }));
          }
          return;
        }

        if (sc.geom === 'cant') {
          gFurn.appendChild(svgEl('rect', { x: 6, y: 24, width: 24, height: 84, fill: '#ede7dd', stroke: '#c4bcac', 'stroke-width': '1' }));
          for (k = 0; k < 6; k++) {
            gFurn.appendChild(svgEl('line', { x1: 6, y1: 30 + k * 13, x2: 30, y2: 24 + k * 13, stroke: '#cfc7b8', 'stroke-width': '1' }));
          }
        } else {
          sc.sup.forEach(function (f) {
            var sx = x0 + (x1 - x0) * f, sy = MID_Y + DEPTH / 2;
            gFurn.appendChild(svgEl('path', {
              d: 'M' + sx + ' ' + sy + 'L' + (sx - 8) + ' ' + (sy + 13) + 'L' + (sx + 8) + ' ' + (sy + 13) + 'Z',
              fill: '#e2ddd2', stroke: '#b9b1a4', 'stroke-width': '1'
            }));
            hatch(gFurn, sx - 11, sy + 13, sx + 11, sy + 19, 4);
          });
        }

        (sc.loads || []).forEach(function (ld) {
          if (ld.kind === 'point') {
            var px = x0 + (x1 - x0) * ld.x;
            if (ld.x >= 1) px -= 5;
            gFurn.appendChild(svgEl('path', {
              d: arrowPath(px, 16, MID_Y - DEPTH / 2 - 4), fill: 'none', stroke: '#6f6a62',
              'stroke-width': '1.8', 'stroke-linecap': 'round'
            }));
          } else {
            var n = 7, q, f2, ax;
            for (q = 0; q < n; q++) {
              f2 = ld.from + (ld.to - ld.from) * (q / (n - 1));
              ax = x0 + (x1 - x0) * f2;
              ax = Math.min(Math.max(ax, x0 + 5), x1 - 5);
              gFurn.appendChild(svgEl('path', {
                d: arrowPath(ax, 24, MID_Y - DEPTH / 2 - 4), fill: 'none', stroke: '#6f6a62',
                'stroke-width': '1.3', 'stroke-linecap': 'round'
              }));
            }
            gFurn.appendChild(svgEl('line', {
              x1: x0 + 4, y1: 24, x2: x1 - 4, y2: 24, stroke: '#6f6a62', 'stroke-width': '1.3'
            }));
          }
        });
      }

      /* the member itself at bend fraction t2 (0 straight, 1 fully bent) */
      function drawMember(t2) {
        if (sc.geom === 'column') {
          pMember.setAttribute('d', 'M143 26L177 26L177 96L143 96Z');
          pComp.setAttribute('d', 'M143 26L177 26L177 96L143 96Z');
          pTens.setAttribute('d', '');
          return;
        }
        var pts = centreLine(t2), h = DEPTH / 2, top = model.face === 'high';
        pMember.setAttribute('d', band(pts, -h, h));
        pTens.setAttribute('d', top ? band(pts, -h, 0) : band(pts, 0, h));
        pComp.setAttribute('d', top ? band(pts, 0, h) : band(pts, -h, 0));

        /* keep the words clear of the crack, which must stay at the section
           of largest bending moment wherever the model puts it */
        var s = span(sc);
        var lf = sc.mode !== 'crack' ? 0.5 : (model.peakX < 0.35 ? 0.62 : 0.22);
        var cx = s[0] + (s[1] - s[0]) * lf, dy = interp(model.shape, lf) * EXAG * t2;
        tTop.setAttribute('x', cx.toFixed(1)); tTop.setAttribute('y', (MID_Y + dy - 3).toFixed(1));
        tBot.setAttribute('x', cx.toFixed(1)); tBot.setAttribute('y', (MID_Y + dy + 11).toFixed(1));

        pBar.setAttribute('d', barPath(pts, top ? -(h - COVER) : (h - COVER)));
        if (chosen && chosen !== 'none' && chosen !== model.face) {
          pGhost.setAttribute('d', edge(pts, chosen === 'high' ? -(h - COVER) : chosen === 'low' ? (h - COVER) : 0));
        }

        var px = Math.min(Math.max(model.peakX, 0.06), 0.94);
        var cxp = s[0] + (s[1] - s[0]) * px;
        var cy = MID_Y + interp(model.shape, px) * EXAG * t2 + (top ? -h : h);
        var dir = top ? 1 : -1;
        pCrack.setAttribute('d', 'M' + cxp.toFixed(1) + ' ' + cy.toFixed(1) +
          'l4 ' + (7 * dir) + 'l-5 ' + (7 * dir) + 'l5 ' + (6 * dir) + 'l-3 ' + (4 * dir));
      }

      function bendTo(target) {
        if (reduced) { bend = target; drawMember(bend); return; }
        if (raf) { cancelAnimationFrame(raf); }
        var from = bend, t0 = null;
        function step(ts) {
          if (!root.isConnected) { raf = 0; return; }
          if (t0 === null) { t0 = ts; }
          var k = Math.min(1, (ts - t0) / 380), e = 1 - Math.pow(1 - k, 3);
          bend = from + (target - from) * e;
          drawMember(bend);
          if (k < 1) { raf = requestAnimationFrame(step); } else { raf = 0; }
        }
        raf = requestAnimationFrame(step);
      }

      /* ---- state and flow ---- */
      function state() {
        root.dataset.svState = JSON.stringify({
          round: sc.id,
          selected: chosen,
          correct: revealed ? (chosen === model.face) : null,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      function labelOpts() {
        OPTS.forEach(function (o, k) {
          btns[k].querySelector('b').textContent = o.word;
          btns[k].querySelector('i').textContent = o[sc.mode];
        });
      }

      function pick(key) {
        if (revealed) { return; }
        chosen = key;
        OPTS.forEach(function (o, k) {
          btns[k].setAttribute('aria-pressed', o.key === key ? 'true' : 'false');
        });
        go.disabled = !key;
        state();
      }

      function commit() {
        if (!chosen || revealed) { return; }
        revealed = true; attempted++;
        var right = chosen === model.face;
        streak = right ? streak + 1 : 0;
        var justMastered = false;
        if (right && streak >= 3 && !mastered) { mastered = true; justMastered = true; }

        btns.forEach(function (b, k) {
          b.disabled = true;
          if (OPTS[k].key === model.face) { b.setAttribute('data-ans', '1'); }
        });

        var top = model.face === 'high';
        if (sc.geom === 'column') {
          pComp.setAttribute('opacity', '1');
          tTop.setAttribute('text-anchor', 'start'); tBot.setAttribute('text-anchor', 'start');
          tTop.setAttribute('x', 196); tTop.setAttribute('y', 58);
          tBot.setAttribute('x', 196); tBot.setAttribute('y', 71);
          tTop.textContent = 'COMPRESSION'; tBot.textContent = 'squashed all through';
          tTop.setAttribute('fill', '#6f6a62'); tTop.setAttribute('stroke', '#faf8f5');
          tBot.setAttribute('fill', '#6f6a62'); tBot.setAttribute('stroke', '#faf8f5');
          tBot.setAttribute('font-size', '9.5'); tBot.setAttribute('font-weight', '400');
          tTop.setAttribute('opacity', '1'); tBot.setAttribute('opacity', '1');
          pBar.setAttribute('d', 'M150 32L150 90M170 32L170 90');
          pCrack.setAttribute('d', 'M147 40L173 40M147 61L173 61M147 82L173 82');
          pCrack.setAttribute('stroke', accent); pCrack.setAttribute('stroke-width', '1.4');
          pBar.setAttribute('opacity', '1'); pCrack.setAttribute('opacity', '1');
        } else {
          pComp.setAttribute('opacity', '1'); pTens.setAttribute('opacity', '1');
          tTop.textContent = top ? 'TENSION' : 'COMPRESSION';
          tBot.textContent = top ? 'COMPRESSION' : 'TENSION';
          tTop.setAttribute('fill', top ? accent : '#6f6a62');
          tTop.setAttribute('stroke', top ? STRETCHED : SQUASHED);
          tBot.setAttribute('fill', top ? '#6f6a62' : accent);
          tBot.setAttribute('stroke', top ? SQUASHED : STRETCHED);
          tTop.setAttribute('opacity', '1'); tBot.setAttribute('opacity', '1');
          if (sc.mode === 'crack') {
            pCrack.setAttribute('opacity', '1');
          } else {
            pBar.setAttribute('opacity', '1');
            if (chosen !== 'none' && chosen !== model.face) { pGhost.setAttribute('opacity', '1'); }
          }
        }
        drawMember(bend);
        bendTo(1);

        var marker = right ? 'Right —' : 'Not quite —';
        var body = ECHO[sc.mode][chosen] + ' ' +
                   (justMastered ? MASTER : sc.mech + ' ' + (right ? sc.win : diagnose(chosen, model.face, sc.mode)));
        cap.innerHTML = '<b style="color:' + (right ? '#4f7d63' : '#2d2a26') + '">' + marker + '</b> ' + esc(body);
        sr.textContent = marker + ' ' + body;
        runLine();
        go.textContent = mastered ? 'Another anyway' : 'Next one';
        state();
      }

      function runLine() {
        if (!attempted) { run.textContent = ''; return; }
        if (mastered) { run.textContent = 'Mastered — keep going if you want.'; return; }
        if (streak === 0) { run.textContent = 'Run reset — back to nought in a row.'; return; }
        if (streak === 1) { run.textContent = '1 right in a row — two more to go.'; return; }
        run.textContent = '2 right in a row — one more and you have it.';
      }

      function next() {
        pos = (pos + 1) % order.length;
        sc = ROUNDS[order[pos]];
        model = analyse(sc);
        chosen = null; revealed = false; bend = 0;
        btns.forEach(function (b) {
          b.disabled = false; b.removeAttribute('data-ans'); b.setAttribute('aria-pressed', 'false');
        });
        [pComp, pTens, pBar, pGhost, pCrack, tTop, tBot].forEach(function (e) { e.setAttribute('opacity', '0'); });
        pCrack.setAttribute('stroke', '#2d2a26'); pCrack.setAttribute('stroke-width', '2.2');
        tTop.setAttribute('text-anchor', 'middle'); tBot.setAttribute('text-anchor', 'middle');
        tBot.setAttribute('font-size', '11'); tBot.setAttribute('font-weight', '700');
        go.textContent = 'Check it'; go.disabled = true;
        render();
        state();
      }

      function render() {
        frame.textContent = sc.scenario + ' ' + ASK[sc.mode];
        labelOpts();
        drawFurniture();
        drawMember(bend);
        if (!revealed) { cap.textContent = attempted ? OPENER2 : OPENER; }
        runLine();
      }

      render();
      state();
    }
  };
})();
