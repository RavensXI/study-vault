/* bending-tension-compression
   One load. Two opposite stresses. At the same moment.

   The student marks BOTH faces of a loaded part — top face and
   underside — before any verdict appears. One structural model decides
   the support reactions, the bending moment, the deflected shape that
   gets drawn, and therefore which face is stretched and which squashed,
   so the picture and the marking can never disagree. Rotating the
   geometry moves the answer: a shelf held at both ends stretches
   underneath, a bracket held at one end stretches on TOP. Two axial
   rounds (a prop pushed end to end, a tie pulled end to end) are the
   contrast: those really are a single force.

   The two marks are sequenced, not offered as a panel. Step 2 sleeps
   until step 1 is set, and the face being asked about is named on the
   drawing itself — a numbered chip on a leader line, plus its edge lit
   in the accent — so "which face is this question about" is answered by
   the stage, not by the label alone. */
(function () {
  'use strict';

  /* ---------------------------------------------------------------
     1. The model
     --------------------------------------------------------------- */

  var N = 96;               /* stations along the member, x = 0..1 */

  /* every load becomes a list of point loads, so one moment routine
     serves both books spread along a shelf and an oven on one spot */
  function pointsFrom(sc) {
    var out = [];
    (sc.loads || []).forEach(function (ld) {
      if (ld.kind === 'point') { out.push({ x: ld.x, P: ld.P }); return; }
      var n = 32, w = (ld.to - ld.from) / n, i;
      for (i = 0; i < n; i++) { out.push({ x: ld.from + w * (i + 0.5), P: ld.w * w }); }
    });
    return out;
  }

  function interp(arr, f) {
    var t = f * N, i0 = Math.floor(t);
    if (i0 >= N) { return arr[N]; }
    if (i0 < 0) { return arr[0]; }
    var k = t - i0;
    return arr[i0] * (1 - k) + arr[i0 + 1] * k;
  }

  function analyse(sc) {
    var xs = [], M = [], i, j, x, m;
    for (i = 0; i <= N; i++) { xs.push(i / N); }

    /* the load runs straight down the member's own line: no curve, so
       both faces do the same thing */
    if (sc.axial) {
      var flat = [];
      for (i = 0; i <= N; i++) { flat.push(0); }
      return { top: sc.axial, bottom: sc.axial, shape: flat, bending: false };
    }

    var P = pointsFrom(sc), W = 0, Ma = 0;
    for (j = 0; j < P.length; j++) { W += P[j].P; }

    if (sc.geom === 'cant') {
      /* built in at x = 0: a vertical reaction plus a fixing moment */
      for (j = 0; j < P.length; j++) { Ma += P[j].P * P[j].x; }
      for (i = 0; i <= N; i++) {
        x = xs[i]; m = -Ma + W * x;
        for (j = 0; j < P.length; j++) { if (P[j].x < x) { m -= P[j].P * (x - P[j].x); } }
        M.push(m);
      }
    } else {
      /* two supports, with or without an overhang past the outer one */
      var a = sc.sup[0], b = sc.sup[1];
      for (j = 0; j < P.length; j++) { Ma += P[j].P * (P[j].x - a); }
      var Rb = Ma / (b - a), Ra = W - Rb;
      for (i = 0; i <= N; i++) {
        x = xs[i]; m = 0;
        if (a < x) { m += Ra * (x - a); }
        if (b < x) { m += Rb * (x - b); }
        for (j = 0; j < P.length; j++) { if (P[j].x < x) { m -= P[j].P * (x - P[j].x); } }
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
    if (sc.geom !== 'cant') {
      var va = interp(v, sc.sup[0]), vb = interp(v, sc.sup[1]);
      var beta = -(vb - va) / (sc.sup[1] - sc.sup[0]);
      var alpha = -va - beta * sc.sup[0];
      for (i = 0; i <= N; i++) { v[i] += alpha + beta * xs[i]; }
    }

    var peak = 0;
    for (i = 0; i <= N; i++) { if (Math.abs(M[i]) > Math.abs(peak)) { peak = M[i]; } }

    /* sagging (positive) stretches the underside and squashes the top;
       hogging does the reverse. Explicit epsilon scaled to the load,
       never a bare float comparison. */
    var eps = 1e-6 * Math.max(W, 1e-6);
    var sag = peak > eps;

    var big = 0;
    for (i = 0; i <= N; i++) { big = Math.max(big, Math.abs(v[i])); }
    var shape = [];
    for (i = 0; i <= N; i++) { shape.push(big > 0 ? v[i] / big : 0); }

    return {
      top: sag ? 'squash' : 'stretch',
      bottom: sag ? 'stretch' : 'squash',
      shape: shape,
      bending: true
    };
  }

  /* ---------------------------------------------------------------
     2. The rounds
     --------------------------------------------------------------- */

  var ROUNDS = [
    { id: 'shelf', geom: 'simple', sup: [0, 1],
      loads: [{ kind: 'udl', from: 0, to: 1, w: 1 }],
      scenario: 'A pine shelf is fixed to brackets at both ends, with a row of heavy books along it.',
      mech: 'Held at both ends, the shelf sags: the underside is pulled longer, the top squashed shorter.',
      win: 'Both at once — so it splits from underneath, and a batten glued along the bottom edge stiffens it most.' },

    { id: 'bracket', geom: 'cant',
      loads: [{ kind: 'point', x: 1, P: 1 }],
      scenario: 'A steel bracket is bolted to a wall at one end only. A loaded basket hangs from its tip.',
      mech: 'Held at one end only, the bracket hogs: the top is pulled longer, the underside squashed.',
      win: 'The opposite way round to a shelf — so a cantilever tears at the top, where extra depth or a rib belongs.' },

    { id: 'prop', geom: 'axial', axial: 'squash',
      scenario: 'A prop is wedged horizontally between two walls that lean in, pushing on both its ends.',
      mech: 'The push runs straight along the prop’s own line, so the whole section is squashed at once.',
      win: 'This one really is a single force. Bending is the one that does two opposite things at the same time.' },

    { id: 'bench', geom: 'over', sup: [0, 0.62],
      loads: [{ kind: 'point', x: 1, P: 1 }],
      scenario: 'A softwood bench top rests on two legs and reaches past the outer one. Someone sits on that far end.',
      mech: 'The far end drops and levers the top over the outer leg: the top is pulled longer, the underside squashed.',
      win: 'The pull is worst right over that leg — where softwood splits, and where a deeper rail belongs.' },

    { id: 'footrest', geom: 'simple', sup: [0, 1],
      loads: [{ kind: 'point', x: 0.5, P: 1 }],
      scenario: 'A steel footrest rail runs between the legs of a stool. Someone stands on the middle of it.',
      mech: 'Held at both ends, the rail sags: the underside is pulled longer, the top squashed shorter.',
      win: 'Both faces work at once, which is why a hollow tube does so well — the metal sits out at those two faces.' },

    { id: 'tie', geom: 'axial', axial: 'stretch',
      scenario: 'A steel tie bar runs between two walls that are being pushed apart. Each wall pulls on its end.',
      mech: 'The pull runs straight along the bar’s own line, so the whole section is stretched at once.',
      win: 'One force, one effect, no curve at all. That is tension — not bending.' },

    { id: 'worktop', geom: 'simple', sup: [0, 1],
      loads: [{ kind: 'point', x: 0.34, P: 1 }],
      scenario: 'An MDF worktop spans two base units. A heavy oven sits on it, a third of the way along.',
      mech: 'Held at both ends, the worktop sags: the underside is pulled longer, the top squashed shorter.',
      win: 'MDF gives way where it is pulled, so a steel strip along the bottom edge helps; one on top barely does.' },

    { id: 'canopy', geom: 'cant',
      loads: [{ kind: 'udl', from: 0, to: 1, w: 1 }],
      scenario: 'An acrylic canopy is bolted to the wall along one edge only. Wet snow lies evenly over it.',
      mech: 'Fixed along one edge only, the canopy hogs: the top is pulled longer, the underside squashed.',
      win: 'So acrylic crazes on the top surface at the wall — not underneath, where you would look first.' }
  ];

  var ASK = 'Mark what each face is doing while the load is on.';

  var OPTS = [
    { key: 'stretch', word: 'Stretched' },
    { key: 'squash', word: 'Squashed' },
    { key: 'none', word: 'No change' }
  ];

  var FACES = [
    { slot: 'top', num: '1', label: 'The top face', tag: 'top face' },
    { slot: 'bot', num: '2', label: 'The underside', tag: 'underside' }
  ];

  var WORD = { stretch: 'stretched', squash: 'squashed', none: 'unchanged' };
  var MARK = { stretch: 'stretched', squash: 'squashed', none: 'no change' };
  var BIG = { stretch: 'TENSION', squash: 'COMPRESSION' };

  function echoOf(t, b) {
    if (t === 'none' && b === 'none') {
      return 'you said neither face changes length; the part just bends.';
    }
    if (t === b) { return 'you marked both faces ' + WORD[t] + '.'; }
    return 'you marked the top face ' + WORD[t] + ' and the underside ' + WORD[b] + '.';
  }

  var DIAG = {
    bothNone: 'Bending is not a force of its own: a curve makes its outside face longer and its inside face shorter, always both.',
    oneNone: 'A face cannot change length on its own — if one is doing something, the opposite face is doing the reverse.',
    swapped: 'You have the right pair, the wrong way round: the face on the outside of the bend is the stretched one.',
    sameFaces: 'Both faces cannot do the same thing here — the part curves, and a curve has a longer side and a shorter one.',
    axialPair: 'Nothing curves here: the load runs straight along the member, so both faces do the same thing.',
    axialPush: 'Look at the load arrows — those ends are being pushed towards each other, so the material is squashed.',
    axialPull: 'Look at the load arrows — those ends are being pulled apart, so the material is stretched.'
  };

  function diagnose(t, b, sc) {
    if (t === 'none' && b === 'none') { return DIAG.bothNone; }
    if (t === 'none' || b === 'none') { return DIAG.oneNone; }
    if (sc.axial) {
      if (t !== b) { return DIAG.axialPair; }
      return sc.axial === 'squash' ? DIAG.axialPush : DIAG.axialPull;
    }
    if (t === b) { return DIAG.sameFaces; }
    return DIAG.swapped;
  }

  var OPENER = 'Tension pulls a material longer. Compression squashes it shorter. Work out what each face of this part is doing.';
  var OPENER2 = 'The outside of a bend has further to travel than the inside. Mark each face, then check it.';
  var MASTER = 'Three in a row — you have it. Find the outside of the bend and you have found the stretched face.';

  /* ---------------------------------------------------------------
     3. Drawing
     --------------------------------------------------------------- */

  var VB_W = 320, VB_H = 106;
  var MID_Y = 62, DEPTH = 42, EXAG = 10;
  var CHIP_X = 256, CHIP_R = 7;        /* the face chips live in a right-hand gutter */
  var BASE = '#eee9df', SQUASH = '#dbd8d2', LINE = '#b7ae9e', FURN = '#6f6a62';
  var INK_C = '#5b564e';    /* compression: neutral, on the grey band */
  var NS = 'http://www.w3.org/2000/svg';

  function blend(hex, base, t) {
    function parts(h) {
      h = String(h).replace('#', '');
      if (h.length === 3) { h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2]; }
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
    }
    var a, b, out = '#', i, v;
    try { a = parts(hex); b = parts(base); } catch (e) { return base; }
    if (!a || isNaN(a[0])) { return base; }
    for (i = 0; i < 3; i++) {
      v = Math.round(b[i] + (a[i] - b[i]) * t);
      out += ('0' + Math.max(0, Math.min(255, v)).toString(16)).slice(-2);
    }
    return out;
  }

  function svgEl(tag, attrs) {
    var e = document.createElementNS(NS, tag), k;
    for (k in attrs) { if (Object.prototype.hasOwnProperty.call(attrs, k)) { e.setAttribute(k, attrs[k]); } }
    return e;
  }

  /* the member stops short of the gutter so the face chips have room */
  function span(sc) {
    if (sc.geom === 'cant') { return [20, 234]; }
    if (sc.geom === 'axial') { return [14, 218]; }
    return [16, 232];
  }

  function vArrow(x, y1, y2) {
    var a = x.toFixed(1), b = y2.toFixed(1);
    return 'M' + a + ' ' + y1.toFixed(1) + 'L' + a + ' ' + b +
           'M' + (x - 3.2).toFixed(1) + ' ' + (y2 - 4.8).toFixed(1) + 'L' + a + ' ' + b +
           'L' + (x + 3.2).toFixed(1) + ' ' + (y2 - 4.8).toFixed(1);
  }

  function hArrow(x1, x2, y) {
    var d = x2 > x1 ? -1 : 1;
    return 'M' + x1 + ' ' + y + 'L' + x2 + ' ' + y +
           'M' + (x2 + d * 5.2) + ' ' + (y - 3.4) + 'L' + x2 + ' ' + y + 'L' + (x2 + d * 5.2) + ' ' + (y + 3.4);
  }

  /* ---------------------------------------------------------------
     4. The widget
     --------------------------------------------------------------- */

  var CSS = [
    '.svw-btc{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26}',
    '.svw-btc *{box-sizing:border-box}',
    '.svw-btc .btc-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--btc-a);margin:0 0 .2rem}',
    '.svw-btc .btc-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.16rem;line-height:1.2;margin:0 0 .28rem}',
    '.svw-btc .btc-frame{font-size:.85rem;line-height:1.4;margin:0 0 .5rem;color:#3d3a35}',
    '.svw-btc .btc-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.45rem;margin:0 0 .55rem}',
    '.svw-btc .btc-stage svg{display:block;width:100%;max-width:360px;height:auto;margin:0 auto}',
    '.svw-btc .btc-groups{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:.5rem;margin:0 0 .5rem}',
    '.svw-btc .btc-grp[data-state="dormant"]{opacity:.38}',
    '.svw-btc .btc-lab{display:flex;align-items:center;gap:.4rem;font-size:.75rem;font-weight:600;color:#8d8880;margin:0 0 .3rem}',
    '.svw-btc .btc-grp[data-state="live"] .btc-lab,.svw-btc .btc-grp[data-state="done"] .btc-lab{color:#2d2a26}',
    '.svw-btc .btc-num{display:inline-flex;align-items:center;justify-content:center;width:1.24rem;height:1.24rem;border-radius:50%;border:1.5px solid #c9c2b6;background:#fff;color:#8d8880;font-size:.72rem;font-weight:700;line-height:1;flex:0 0 auto}',
    '.svw-btc .btc-grp[data-state="live"] .btc-num{background:var(--btc-a);border-color:var(--btc-a);color:#fff}',
    '.svw-btc .btc-grp[data-state="done"] .btc-num{background:var(--btc-t);border-color:var(--btc-a);color:var(--btc-a)}',
    '.svw-btc .btc-row{display:grid;grid-template-columns:repeat(3,1fr);gap:.35rem}',
    '.svw-btc .btc-opt{appearance:none;font-family:inherit;font-size:.78rem;font-weight:600;line-height:1.2;text-align:center;background:#faf8f5;border:1px solid #ddd7cd;border-radius:9px;padding:.42rem .2rem;cursor:pointer;color:#2d2a26}',
    '.svw-btc .btc-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-btc .btc-opt[data-ans="1"]{box-shadow:0 0 0 2px var(--btc-a);border-color:var(--btc-a)}',
    '.svw-btc .btc-opt:disabled{cursor:default}',
    '.svw-btc .btc-go{appearance:none;font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-btc .btc-go:disabled{background:#faf8f5;border-color:#e0d9cd;color:#b3aca1;cursor:default}',
    '.svw-btc .btc-run{font-size:.76rem;color:#8d8880;min-height:1.05rem;margin:.35rem 0 .1rem;font-variant-numeric:tabular-nums}',
    '.svw-btc .btc-cap{font-size:.84rem;line-height:1.48;margin:0;padding:.5rem 0 0;border-top:1px solid #efe9e0;min-height:4.6rem;color:#3d3a35}',
    '.svw-btc .btc-cap b{font-weight:600}',
    '.svw-btc .btc-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
  ].join('');

  window.SVWidget = {
    meta: {
      id: 'bending-tension-compression',
      title: 'Inside a bending part',
      teaches: 'Bending is not one force: the part curves, so one face is pulled longer (tension) while the opposite face is squashed shorter (compression), at the same moment — and which face is which flips with the supports.'
    },

    mount: function (root, ctx) {
      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
                   ((ctx && ctx.accent) || '#8a6a4f');
      var reduced = !!(ctx && ctx.reducedMotion);
      /* the two faces must be told apart at a glance: the stretched face
         carries the accent, the squashed face stays neutral grey */
      var STRETCH = blend(accent, BASE, 0.44);
      var INK_T = blend(accent, '#2d2a26', 0.5);

      root.classList.add('svw-btc');
      root.innerHTML = '';
      root.style.setProperty('--btc-a', accent);
      root.style.setProperty('--btc-t', accent + '22');
      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      /* the sagging shelf, then the bracket that flips the answer, then
         the prop that really is one force; the rest shuffled behind */
      var order = [0, 1, 2], tail = [3, 4, 5, 6, 7], i, j, t;
      for (i = tail.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1)); t = tail[i]; tail[i] = tail[j]; tail[j] = t;
      }
      order = order.concat(tail);

      var pos = 0, sc = ROUNDS[order[0]], model = analyse(sc);
      var pick2 = { top: null, bot: null };
      var revealed = false, streak = 0, attempted = 0, mastered = false;
      var bend = 0, raf = 0;

      /* ---- markup, built once and then mutated ---- */
      var head = document.createElement('div');
      head.innerHTML = '<p class="btc-kick"></p><h3 class="btc-title"></h3><p class="btc-frame"></p>';
      root.appendChild(head);
      head.querySelector('.btc-kick').textContent = 'Forces and stresses';
      head.querySelector('.btc-title').textContent = 'Inside a bending part';
      var frame = head.querySelector('.btc-frame');

      var stage = document.createElement('div');
      stage.className = 'btc-stage';
      root.appendChild(stage);

      var svg = svgEl('svg', { viewBox: '0 0 ' + VB_W + ' ' + VB_H, role: 'img' });
      var gFurn = svgEl('g', {});
      var pLoad = svgEl('path', { fill: 'none', stroke: FURN, 'stroke-width': '1.5', 'stroke-linecap': 'round' });
      var pFill = svgEl('path', { fill: BASE, stroke: 'none' });
      var pTopBand = svgEl('path', { fill: BASE, stroke: 'none', opacity: '0' });
      var pBotBand = svgEl('path', { fill: BASE, stroke: 'none', opacity: '0' });
      var pEdge = svgEl('path', { fill: 'none', stroke: LINE, 'stroke-width': '1.2', 'stroke-linejoin': 'round' });
      var pLive = svgEl('path', { fill: 'none', stroke: accent, 'stroke-width': '2.6', 'stroke-linecap': 'round', opacity: '0' });
      var pTopArr = svgEl('path', { fill: 'none', stroke: FURN, 'stroke-width': '1.5', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', opacity: '0' });
      var pBotArr = svgEl('path', { fill: 'none', stroke: FURN, 'stroke-width': '1.5', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', opacity: '0' });
      var tTop = svgEl('text', { 'text-anchor': 'middle', 'paint-order': 'stroke', 'stroke-width': '4', 'stroke-linejoin': 'round', opacity: '0' });
      var tBot = svgEl('text', { 'text-anchor': 'middle', 'paint-order': 'stroke', 'stroke-width': '4', 'stroke-linejoin': 'round', opacity: '0' });

      /* the gutter chips: the same numeral as the control group, sitting
         at the height of the face that group is asking about */
      var gChips = svgEl('g', {});
      var pLead = svgEl('path', { fill: 'none', stroke: '#c4bcac', 'stroke-width': '1', 'stroke-dasharray': '3 2.6' });
      gChips.appendChild(pLead);
      var chips = FACES.map(function (fc, k) {
        var cy = MID_Y + (k === 0 ? -DEPTH / 2 : DEPTH / 2);
        var g = svgEl('g', {});
        var circ = svgEl('circle', { cx: CHIP_X, cy: cy, r: CHIP_R, fill: '#fff', stroke: '#c9c2b6', 'stroke-width': '1.5' });
        var num = svgEl('text', {
          x: CHIP_X, y: cy + 3.2, 'text-anchor': 'middle', 'font-size': '9.2',
          'font-weight': '700', fill: '#8d8880'
        });
        num.textContent = fc.num;
        var word = svgEl('text', {
          x: CHIP_X + CHIP_R + 4, y: cy + 3.1, 'font-size': '9.4', 'font-weight': '600', fill: '#8d8880'
        });
        word.textContent = fc.tag;
        g.appendChild(circ); g.appendChild(num); g.appendChild(word);
        gChips.appendChild(g);
        return { circ: circ, num: num, word: word, cy: cy };
      });

      svg.appendChild(gFurn); svg.appendChild(pLoad);
      svg.appendChild(pFill); svg.appendChild(pTopBand); svg.appendChild(pBotBand);
      svg.appendChild(pEdge); svg.appendChild(pLive);
      svg.appendChild(pTopArr); svg.appendChild(pBotArr);
      svg.appendChild(tTop); svg.appendChild(tBot);
      svg.appendChild(gChips);
      stage.appendChild(svg);

      var groups = document.createElement('div');
      groups.className = 'btc-groups';
      root.appendChild(groups);

      function buildGroup(fc) {
        var wrap = document.createElement('div');
        wrap.className = 'btc-grp';
        wrap.setAttribute('data-state', 'dormant');
        var lab = document.createElement('p');
        lab.className = 'btc-lab';
        var chip = document.createElement('span');
        chip.className = 'btc-num'; chip.textContent = fc.num; chip.setAttribute('aria-hidden', 'true');
        lab.appendChild(chip);
        lab.appendChild(document.createTextNode(fc.label));
        wrap.appendChild(lab);
        var row = document.createElement('div');
        row.className = 'btc-row';
        var made = OPTS.map(function (o) {
          var b = document.createElement('button');
          b.type = 'button'; b.className = 'btc-opt';
          b.setAttribute('aria-pressed', 'false');
          b.setAttribute('aria-label', fc.label + ': ' + o.word);
          b.textContent = o.word;
          b.addEventListener('click', function () { pick(fc.slot, o.key); });
          row.appendChild(b);
          return b;
        });
        wrap.appendChild(row);
        groups.appendChild(wrap);
        return { wrap: wrap, btns: made };
      }

      var grp = { top: buildGroup(FACES[0]), bot: buildGroup(FACES[1]) };

      var go = document.createElement('button');
      go.type = 'button'; go.className = 'btc-go'; go.textContent = 'Check it'; go.disabled = true;
      root.appendChild(go);

      var run = document.createElement('p'); run.className = 'btc-run'; root.appendChild(run);
      var cap = document.createElement('p'); cap.className = 'btc-cap'; root.appendChild(cap);
      var capMark = document.createElement('b');
      var capText = document.createTextNode('');
      var sr = document.createElement('p'); sr.className = 'btc-sr';
      sr.setAttribute('aria-live', 'polite'); root.appendChild(sr);

      go.addEventListener('click', function () { if (revealed) { next(); } else { commit(); } });
      root.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !revealed && (pick2.top || pick2.bot)) {
          pick2.bot = null; pick('top', null);
        }
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
        for (k = 0; k < pts.length; k++) { d += (k ? 'L' : 'M') + pts[k].x.toFixed(1) + ' ' + (pts[k].y + off).toFixed(1); }
        return d;
      }
      function band(pts, o1, o2) {
        var d = edge(pts, o1), k;
        for (k = pts.length - 1; k >= 0; k--) { d += 'L' + pts[k].x.toFixed(1) + ' ' + (pts[k].y + o2).toFixed(1); }
        return d + 'Z';
      }
      /* a short arrow lying along the face, pointing out (stretched) or
         in (squashed), rotated with the local slope of the curve */
      function faceArrows(pts, off, out) {
        var d = '', spots = [[7, -1], [33, 1]], q;
        for (q = 0; q < spots.length; q++) {
          var idx = spots[q][0], s = spots[q][1] * (out ? 1 : -1);
          var a = pts[Math.max(0, idx - 2)], b2 = pts[Math.min(pts.length - 1, idx + 2)];
          var dx = b2.x - a.x, dy = b2.y - a.y, L = Math.sqrt(dx * dx + dy * dy) || 1;
          var tx = dx / L, ty = dy / L, nx = -ty, ny = tx;
          var px = pts[idx].x, py = pts[idx].y + off;
          var hx = px + s * 8 * tx, hy = py + s * 8 * ty;
          var bx = px - s * 8 * tx, by = py - s * 8 * ty;
          d += 'M' + bx.toFixed(1) + ' ' + by.toFixed(1) + 'L' + hx.toFixed(1) + ' ' + hy.toFixed(1);
          d += 'M' + (hx - s * 4.4 * tx + 2.8 * nx).toFixed(1) + ' ' + (hy - s * 4.4 * ty + 2.8 * ny).toFixed(1) +
               'L' + hx.toFixed(1) + ' ' + hy.toFixed(1) +
               'L' + (hx - s * 4.4 * tx - 2.8 * nx).toFixed(1) + ' ' + (hy - s * 4.4 * ty - 2.8 * ny).toFixed(1);
        }
        return d;
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

      /* walls and supports change only when the round does */
      function drawFurniture() {
        gFurn.textContent = '';
        var s = span(sc), x0 = s[0], x1 = s[1], k;

        if (sc.geom === 'axial') {
          [[2, 14], [218, 230]].forEach(function (w) {
            gFurn.appendChild(svgEl('rect', {
              x: w[0], y: 22, width: w[1] - w[0], height: 78,
              fill: '#ede7dd', stroke: '#c4bcac', 'stroke-width': '1'
            }));
          });
          var out = sc.axial === 'stretch';
          gFurn.appendChild(svgEl('path', {
            d: hArrow(out ? 88 : 42, out ? 42 : 88, 34), fill: 'none', stroke: FURN,
            'stroke-width': '1.8', 'stroke-linecap': 'round'
          }));
          gFurn.appendChild(svgEl('path', {
            d: hArrow(out ? 146 : 192, out ? 192 : 146, 34), fill: 'none', stroke: FURN,
            'stroke-width': '1.8', 'stroke-linecap': 'round'
          }));
          return;
        }

        if (sc.geom === 'cant') {
          gFurn.appendChild(svgEl('rect', { x: 2, y: 18, width: 20, height: 84, fill: '#ede7dd', stroke: '#c4bcac', 'stroke-width': '1' }));
          for (k = 0; k < 6; k++) {
            gFurn.appendChild(svgEl('line', { x1: 2, y1: 26 + k * 13, x2: 22, y2: 18 + k * 13, stroke: '#cfc7b8', 'stroke-width': '1' }));
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
      }

      /* the load arrows land on the surface they are pressing on, so they
         follow the member down as it bends */
      function drawLoads(pts) {
        if (sc.geom === 'axial') { pLoad.setAttribute('d', ''); return; }
        var h = DEPTH / 2, s = span(sc), x0 = s[0], x1 = s[1], d = '';
        (sc.loads || []).forEach(function (ld) {
          var idx, p, q, f2;
          if (ld.kind === 'point') {
            idx = Math.round(ld.x * 40); p = pts[idx];
            d += vArrow(ld.x >= 1 ? p.x - 5 : p.x, 10, p.y - h - 4);
          } else {
            for (q = 0; q < 7; q++) {
              f2 = ld.from + (ld.to - ld.from) * (q / 6);
              idx = Math.round(f2 * 40); p = pts[idx];
              d += vArrow(Math.min(Math.max(p.x, x0 + 5), x1 - 5), 20, p.y - h - 4);
            }
            d += 'M' + (x0 + 4) + ' 20L' + (x1 - 4) + ' 20';
          }
        });
        pLoad.setAttribute('d', d);
      }

      /* the member itself at bend fraction t2 (0 straight, 1 fully bent) */
      function drawMember(t2) {
        var pts = centreLine(t2), h = DEPTH / 2;
        pFill.setAttribute('d', band(pts, -h, h));
        pEdge.setAttribute('d', band(pts, -h, h));
        pTopBand.setAttribute('d', band(pts, -h, 0));
        pBotBand.setAttribute('d', band(pts, 0, h));

        var mid = pts[20], solo = revealed && !model.bending;
        tTop.setAttribute('x', mid.x.toFixed(1));
        tTop.setAttribute('y', (mid.y + (solo ? 4 : -7)).toFixed(1));
        tBot.setAttribute('x', mid.x.toFixed(1));
        tBot.setAttribute('y', (mid.y + 15).toFixed(1));

        /* the arrows sit on the same line as their own face word */
        pTopArr.setAttribute('d', faceArrows(pts, -(h - 9.5), revealed ? model.top === 'stretch' : pick2.top === 'stretch'));
        pBotArr.setAttribute('d', faceArrows(pts, (h - 9.5), revealed ? model.bottom === 'stretch' : pick2.bot === 'stretch'));

        /* the face the live control group is asking about, lit along its
           own edge so the question has a place on the drawing */
        var live = liveSlot();
        pLive.setAttribute('d', live ? edge(pts, live === 'top' ? -h : h) : '');
        pLive.setAttribute('opacity', live ? '1' : '0');

        /* leaders from each face's end across to its numbered chip */
        var endX = sc.geom === 'axial' ? 233 : pts[40].x + 3;
        var endTop = sc.geom === 'axial' ? MID_Y - h : pts[40].y - h;
        var endBot = sc.geom === 'axial' ? MID_Y + h : pts[40].y + h;
        pLead.setAttribute('d',
          'M' + endX.toFixed(1) + ' ' + endTop.toFixed(1) + 'L' + (CHIP_X - CHIP_R - 2) + ' ' + chips[0].cy +
          'M' + endX.toFixed(1) + ' ' + endBot.toFixed(1) + 'L' + (CHIP_X - CHIP_R - 2) + ' ' + chips[1].cy);

        drawLoads(pts);
      }

      function tintFor(k) { return k === 'stretch' ? STRETCH : k === 'squash' ? SQUASH : BASE; }

      /* which group is being asked for right now: step 2 sleeps until
         step 1 is set, and neither is live once both are marked */
      function liveSlot() {
        if (revealed) { return null; }
        if (!pick2.top) { return 'top'; }
        if (!pick2.bot) { return 'bot'; }
        return null;
      }

      function groupStates() {
        var live = liveSlot();
        ['top', 'bot'].forEach(function (slot, k) {
          var st = revealed ? 'done'
            : slot === live ? 'live'
              : pick2[slot] ? 'done'
                : slot === 'bot' && !pick2.top ? 'dormant' : 'done';
          grp[slot].wrap.setAttribute('data-state', st);
          grp[slot].btns.forEach(function (b) {
            b.disabled = revealed || (slot === 'bot' && !pick2.top);
          });
          /* the chip on the drawing mirrors the chip on the control group */
          var on = st === 'live', marked = !!pick2[slot];
          chips[k].circ.setAttribute('fill', on ? accent : marked ? accent + '22' : '#fff');
          chips[k].circ.setAttribute('stroke', on || marked ? accent : '#c9c2b6');
          chips[k].num.setAttribute('fill', on ? '#fff' : marked ? accent : '#8d8880');
          chips[k].word.setAttribute('fill', on || marked ? INK_C : '#8d8880');
          chips[k].word.setAttribute('font-weight', on ? '700' : '600');
        });
      }

      /* the student's own marking, shown lightly and without a verdict */
      function showMarks() {
        [[pTopBand, tTop, pTopArr, pick2.top], [pBotBand, tBot, pBotArr, pick2.bot]].forEach(function (r) {
          var k = r[3];
          r[0].setAttribute('fill', tintFor(k));
          r[0].setAttribute('opacity', k && k !== 'none' ? '0.6' : '0');
          r[1].setAttribute('opacity', k ? '1' : '0');
          r[1].setAttribute('font-size', '8.5');
          r[1].setAttribute('font-weight', '400');
          r[1].setAttribute('letter-spacing', '0');
          r[1].setAttribute('fill', INK_C);
          r[1].setAttribute('stroke', k === 'squash' ? SQUASH : k === 'stretch' ? STRETCH : BASE);
          r[1].textContent = k ? MARK[k] : '';
          r[2].setAttribute('stroke', FURN);
          r[2].setAttribute('opacity', k === 'stretch' || k === 'squash' ? '0.5' : '0');
        });
        groupStates();
        drawMember(bend);
      }

      /* what is really happening, once they have committed */
      function showTruth() {
        [[pTopBand, tTop, pTopArr, model.top], [pBotBand, tBot, pBotArr, model.bottom]].forEach(function (r) {
          var k = r[3];
          r[0].setAttribute('fill', tintFor(k));
          r[0].setAttribute('opacity', '1');
          r[1].setAttribute('opacity', '1');
          r[1].setAttribute('font-size', '9.5');
          r[1].setAttribute('font-weight', '700');
          r[1].setAttribute('letter-spacing', '.4');
          r[1].setAttribute('fill', k === 'stretch' ? INK_T : INK_C);
          r[1].setAttribute('stroke', tintFor(k));
          r[1].textContent = BIG[k];
          r[2].setAttribute('opacity', '1');
          r[2].setAttribute('stroke', k === 'stretch' ? INK_T : INK_C);
        });
        /* no curve, so both faces do the same thing: say it once, across
           the whole section, rather than printing the word twice */
        if (!model.bending) { tBot.setAttribute('opacity', '0'); }
        groupStates();
        drawMember(bend);
      }

      function bendTo(target) {
        if (reduced) { bend = target; drawMember(bend); return; }
        if (raf) { cancelAnimationFrame(raf); }
        var from = bend, t0 = null;
        function step(ts) {
          if (!root.isConnected) { raf = 0; return; }
          if (t0 === null) { t0 = ts; }
          var k = Math.min(1, (ts - t0) / 420), e = 1 - Math.pow(1 - k, 3);
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
          step: revealed ? 'checked' : liveSlot() === 'top' ? 1 : liveSlot() === 'bot' ? 2 : 'ready',
          top: pick2.top,
          bottom: pick2.bot,
          answerTop: revealed ? model.top : null,
          answerBottom: revealed ? model.bottom : null,
          correct: revealed ? (pick2.top === model.top && pick2.bot === model.bottom) : null,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      function pick(which, key) {
        if (revealed) { return; }
        pick2[which] = key;
        if (which === 'top' && !key) { pick2.bot = null; }
        ['top', 'bot'].forEach(function (slot) {
          grp[slot].btns.forEach(function (b, k) {
            b.setAttribute('aria-pressed', OPTS[k].key === pick2[slot] ? 'true' : 'false');
          });
        });
        go.disabled = !(pick2.top && pick2.bot);
        showMarks();
        state();
      }

      function setCap(marker, body, green) {
        capMark.textContent = marker;
        capMark.style.color = green ? '#4f7d63' : '#2d2a26';
        capText.nodeValue = marker ? ' ' + body : body;
        cap.textContent = '';
        if (marker) { cap.appendChild(capMark); }
        cap.appendChild(capText);
        sr.textContent = (marker ? marker + ' ' : '') + body;
      }

      function commit() {
        if (!pick2.top || !pick2.bot || revealed) { return; }
        revealed = true; attempted++;
        var right = pick2.top === model.top && pick2.bot === model.bottom;
        streak = right ? streak + 1 : 0;
        var justMastered = false;
        if (right && streak >= 3 && !mastered) { mastered = true; justMastered = true; }

        grp.top.btns.forEach(function (b, k) { if (OPTS[k].key === model.top) { b.setAttribute('data-ans', '1'); } });
        grp.bot.btns.forEach(function (b, k) { if (OPTS[k].key === model.bottom) { b.setAttribute('data-ans', '1'); } });

        showTruth();
        bendTo(model.bending ? 1 : 0);

        var body = echoOf(pick2.top, pick2.bot) + ' ' +
          (right ? sc.win + (justMastered ? ' ' + MASTER : '')
            : sc.mech + ' ' + diagnose(pick2.top, pick2.bot, sc));
        setCap(right ? 'Right —' : 'Not quite —', body, right);
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
        pick2.top = null; pick2.bot = null; revealed = false; bend = 0;
        grp.top.btns.concat(grp.bot.btns).forEach(function (b) {
          b.removeAttribute('data-ans'); b.setAttribute('aria-pressed', 'false');
        });
        go.textContent = 'Check it'; go.disabled = true;
        render();
        state();
      }

      function render() {
        frame.textContent = sc.scenario + ' ' + ASK;
        drawFurniture();
        showMarks();
        if (!revealed) { setCap('', attempted ? OPENER2 : OPENER, false); }
        runLine();
      }

      render();
      state();
    }
  };
})();
