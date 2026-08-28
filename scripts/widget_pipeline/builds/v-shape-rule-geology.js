/* v-shape-rule-geology — StudyVault lesson widget
   Why a geological boundary bends into a V where it crosses a valley.

   ONE 3D model drives the map, the section, the reveal and the marking, so
   the drawing can never contradict the verdict. All lengths are map units;
   1 unit = 20 m on the ground. The map is true to scale. The section
   exaggerates height 3x so a 4 degree bed reads clearly against a 1-in-40
   stream, and it says so on the panel.

     ground   Z(u, v) = Z0 - S*u + K*|v|     u = distance downstream
                                             v = offset from the stream
     bed      Zb(u)   = Zb0 + P*u            P = -D dips downstream
                                                 +D dips upstream
                                                  0 horizontal
     outcrop  K*|v| = (Zb0 - Z0) + M*u       M = S + P

   M > 0  the arms open downstream, so the V points upstream
   M < 0  the arms open upstream,   so the V points downstream
   Every dip used here is at least 3x the stream gradient, so no round sits
   near the M = 0 boundary, and the verdict compares id strings, not floats. */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';
  var CLS = 'svw-vshape';
  var UID = 0;

  /* ------------------------------------------------------------------ model */

  var S = 0.025;    /* the stream falls 1 in 40 downstream */
  var K = 0.05;     /* the valley sides rise 1 in 20 away from the stream */
  var Z0 = 15;      /* elevation on the stream at the left edge, = 300 m */
  var MPU = 20;     /* metres per map unit */

  function bedP(att, D) { return att === 'down' ? -D : att === 'up' ? D : 0; }
  function groundZ(u) { return Z0 - S * u; }

  /* the whole rule, in three lines */
  function traceOf(att, D) {
    if (att === 'vertical') return { straight: true, slope: 0, dir: 0, v: 'none' };
    var M = S + bedP(att, D);
    var slope = M / K;
    return {
      straight: false,
      slope: Math.abs(slope),
      dir: slope > 0 ? 1 : -1,
      v: slope > 0 ? 'upstream' : 'downstream'
    };
  }

  /* ---------------------------------------------------------------- rounds */

  /* Round 1 is fixed and teaches dip itself before dip is ever used: the bed
     slopes down one way while the valley floor slopes the other, so a student
     has to read the bed line rather than the ground. */
  var PRIMER = { dir: 'dip', att: 'up', D: 0.055, u: 150 };

  var DECK = [
    { dir: 'dip', att: 'down', D: 0.135, u: 150 },
    { dir: 'dip', att: 'horizontal', D: 0, u: 150 },
    { dir: 'predict', att: 'horizontal', D: 0, u: 120 },
    { dir: 'predict', att: 'down', D: 0.075, u: 200 },
    { dir: 'predict', att: 'up', D: 0.075, u: 150 },
    { dir: 'predict', att: 'vertical', D: 0, u: 150 },
    { dir: 'predict', att: 'down', D: 0.135, u: 120 },
    { dir: 'predict', att: 'up', D: 0.025, u: 90 },
    { dir: 'read', att: 'horizontal', D: 0, u: 80 },
    { dir: 'read', att: 'down', D: 0.115, u: 230 },
    { dir: 'read', att: 'up', D: 0.055, u: 60 },
    { dir: 'read', att: 'vertical', D: 0, u: 110 },
    { dir: 'read', att: 'down', D: 0.075, u: 190 },
    { dir: 'read', att: 'up', D: 0.075, u: 150 },
    { dir: 'read', att: 'vertical', D: 0, u: 190 }
  ];

  function dipKey(att) {
    return att === 'horizontal' ? 'level' : att === 'vertical' ? 'vertical' : att;
  }

  function makeRound(r) {
    var t = traceOf(r.att, r.D);
    return {
      dir: r.dir, att: r.att, D: r.D, uStar: r.u, trace: t,
      answer: r.dir === 'predict' ? t.v : r.dir === 'dip' ? dipKey(r.att) : r.att
    };
  }

  function buildDeck() {
    var d = DECK.map(makeRound);
    for (var i = d.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = d[i];
      d[i] = d[j]; d[j] = t;
    }
    return d;
  }

  /* -------------------------------------------------------------- geometry */

  var VBW = 300, VBH = 150;
  var MAP_L = 8, MAP_R = 292, MAP_T = 5, MAP_B = 88, MAP_CY = 46, VMAX = 40;
  var SEC_T = 102, SEC_B = 146, CY0 = 163, VE = 3;
  var ULEN = MAP_R - MAP_L;

  function gx(u) { return MAP_L + u; }
  function gy(v) { return MAP_CY + v; }
  function sy(z) { return CY0 - VE * z; }

  /* the drawn trace, straight from the model */
  function tracePts(r) {
    var t = r.trace, u = r.uStar;
    if (t.straight) {
      return [[gx(u), gy(-VMAX)], [gx(u), gy(VMAX)]];
    }
    var du = VMAX / t.slope;
    return [
      [gx(u + t.dir * du), gy(-VMAX)],
      [gx(u), gy(0)],
      [gx(u + t.dir * du), gy(VMAX)]
    ];
  }

  /* the same shape for a prediction the student has not committed yet */
  function ghostPts(r, choice) {
    var u = r.uStar;
    if (choice === 'none') return [[gx(u), gy(-VMAX)], [gx(u), gy(VMAX)]];
    var slope = r.trace.straight ? 1.5 : r.trace.slope;
    var dir = choice === 'upstream' ? 1 : -1;
    var du = VMAX / slope;
    return [
      [gx(u + dir * du), gy(-VMAX)],
      [gx(u), gy(0)],
      [gx(u + dir * du), gy(VMAX)]
    ];
  }

  function bedLine(r, att, D) {
    var u = r.uStar;
    if (att === 'vertical') return [[gx(u), SEC_T], [gx(u), SEC_B]];
    var P = bedP(att, D);
    var Zb0 = groundZ(u) - P * u;
    return [[gx(0), sy(Zb0)], [gx(ULEN), sy(Zb0 + P * ULEN)]];
  }

  function pts(a) {
    return a.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' ');
  }

  /* ------------------------------------------------------------------ view */

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

  /* ------------------------------------------------------------------- css */

  function css(accent, reduced) {
    var p = '.' + CLS + ' ';
    return '.' + CLS + '{background:#fff;border:1px solid #e8e3db;border-radius:16px;' +
      'padding:1rem;font-family:Inter,system-ui,-apple-system,sans-serif;color:#2d2a26;' +
      'box-sizing:border-box;max-width:100%;}' +
      p + '*{box-sizing:border-box;}' +
      p + '.k{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;' +
      'text-transform:uppercase;color:' + accent + ';}' +
      p + '.t{margin:.18rem 0 .38rem;font-family:"Source Serif 4",Georgia,serif;' +
      'font-weight:600;font-size:1.2rem;line-height:1.18;}' +
      p + '.frame{margin:0 0 .28rem;font-size:.84rem;line-height:1.4;color:#5b564e;}' +
      p + '.ask{margin:0 0 .4rem;font-size:.88rem;line-height:1.32;font-weight:600;}' +
      p + '.stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;' +
      'max-width:366px;margin:0 auto .42rem;overflow:hidden;}' +
      p + '.stage svg{display:block;width:100%;height:auto;}' +
      p + '.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));' +
      'gap:.26rem;margin:0 0 .38rem;}' +
      p + '.o{font:600 .82rem/1.3 Inter,system-ui,sans-serif;color:#2d2a26;background:#faf8f5;' +
      'border:1px solid #ddd7cd;border-radius:10px;padding:.3rem .58rem;min-height:30px;' +
      'cursor:pointer;text-align:left;' +
      (reduced ? '' : 'transition:background .12s,border-color .12s;') + '}' +
      p + '.o[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}' +
      p + '.o.is-ans{border-color:' + accent + ';box-shadow:inset 0 0 0 1px ' + accent + ';}' +
      p + '.o[disabled]{cursor:default;opacity:.94;}' +
      p + '.act{display:flex;align-items:center;gap:.55rem;flex-wrap:wrap;margin:0 0 .38rem;}' +
      p + '.go{font:600 .82rem Inter,system-ui,sans-serif;background:#2d2a26;color:#fff;' +
      'border:1px solid #2d2a26;border-radius:10px;padding:.42rem .95rem;cursor:pointer;}' +
      p + '.go[disabled]{background:#faf8f5;color:#a8a29a;border-color:#e0d9cd;cursor:default;}' +
      p + '.run{font-size:.78rem;color:#8d8880;font-variant-numeric:tabular-nums;}' +
      p + '.cap{margin:0;font-size:.84rem;line-height:1.42;color:#2d2a26;min-height:52px;}' +
      p + '.cap .v{font-weight:700;}' +
      p + '.cap .rt{color:#4f7d63;}' +
      p + '.cap.rest{color:#8d8880;}' +
      p + '.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);' +
      'white-space:nowrap;margin:-1px;padding:0;border:0;}';
  }

  /* ------------------------------------------------------------------ copy */

  var PRED_LABEL = {
    upstream: 'V points upstream (to the left)',
    downstream: 'V points downstream (to the right)',
    none: 'No V — a straight line across'
  };
  var PRED_ECHO = {
    upstream: 'the V points upstream',
    downstream: 'the V points downstream',
    none: 'there is no V'
  };
  var PRED_ORDER = ['upstream', 'downstream', 'none'];

  var ATT_LABEL = {
    horizontal: 'Horizontal — level, follows a contour',
    down: 'Dips downstream — down to the right',
    up: 'Dips upstream — down to the left',
    vertical: 'Vertical — crosses in a straight line'
  };

  var DIP_LABEL = {
    down: 'Down to the right (downstream)',
    up: 'Down to the left (upstream)',
    level: 'Level — it does not slope'
  };
  var DIP_ECHO = {
    down: 'it slopes down to the right',
    up: 'it slopes down to the left',
    level: 'it is level'
  };
  var DIP_ORDER = ['down', 'up', 'level'];

  /* the words that sit on the bed in the section, in every round */
  var SLOPE_PHRASE = {
    down: 'slopes down', up: 'slopes down',
    level: 'stays level', vertical: 'straight down'
  };
  var ATT_ECHO = {
    horizontal: 'it is horizontal',
    down: 'it dips downstream',
    up: 'it dips upstream',
    vertical: 'it is vertical'
  };
  var ATT_ORDER = ['horizontal', 'down', 'up', 'vertical'];

  var FRAME = {
    horizontal: 'A bed crosses this valley. It is horizontal — all at one height.',
    down: 'A bed crosses this valley. It dips downstream — sloping down to the right.',
    up: 'A bed crosses this valley. It dips upstream — sloping down to the left.',
    vertical: 'A bed crosses this valley. It is vertical — it goes straight down.'
  };

  /* --------------------------------------------------------------- mount */

  window.SVWidget = {
    meta: {
      id: 'v-shape-rule-geology',
      title: 'Where the boundary Vs',
      teaches: 'A boundary crops out where the height of the bed matches the height of the ground, so its V in a valley points the way the bed dips; horizontal beds follow the contours and vertical beds cross straight.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;
      var uid = 'vsh' + (++UID) + '-' + Math.floor(Math.random() * 100000);

      var wrap = document.createElement('div');
      wrap.className = CLS;
      var style = document.createElement('style');
      style.textContent = css(accent, reduced);
      wrap.appendChild(style);

      var kick = document.createElement('p'); kick.className = 'k';
      kick.textContent = 'Map reading';
      var ttl = document.createElement('h3'); ttl.className = 't';
      ttl.textContent = 'Where the boundary Vs';
      var frame = document.createElement('p'); frame.className = 'frame';
      var ask = document.createElement('p'); ask.className = 'ask';
      wrap.appendChild(kick); wrap.appendChild(ttl); wrap.appendChild(frame); wrap.appendChild(ask);

      /* ----------------------------------------------------------- stage */
      var stage = document.createElement('div'); stage.className = 'stage';
      var svg = el('svg', {
        viewBox: '0 0 ' + VBW + ' ' + VBH, role: 'img',
        'aria-label': 'A contoured map of a valley above a section drawn along the stream'
      });
      stage.appendChild(svg); wrap.appendChild(stage);

      var defs = el('defs', {});
      var mclip = el('clipPath', { id: uid + '-m' });
      mclip.appendChild(el('rect', { x: MAP_L, y: MAP_T, width: ULEN, height: MAP_B - MAP_T }));
      var sclip = el('clipPath', { id: uid + '-s' });
      sclip.appendChild(el('rect', { x: MAP_L, y: SEC_T, width: ULEN, height: SEC_B - SEC_T }));
      var gclip = el('clipPath', { id: uid + '-g' });
      gclip.appendChild(el('polygon', {
        points: pts([[gx(0), sy(groundZ(0))], [gx(ULEN), sy(groundZ(ULEN))],
          [gx(ULEN), SEC_B], [gx(0), SEC_B]])
      }));
      defs.appendChild(mclip); defs.appendChild(sclip); defs.appendChild(gclip);
      svg.appendChild(defs);

      /* map: paper, contours, stream */
      svg.appendChild(el('rect', {
        x: MAP_L, y: MAP_T, width: ULEN, height: MAP_B - MAP_T,
        fill: '#f3efe8', stroke: '#e0d9cd', 'stroke-width': 0.8
      }));
      var mapG = el('g', { 'clip-path': 'url(#' + uid + '-m)' });
      svg.appendChild(mapG);

      /* Ground below a contour lies inside a wedge opening downstream. Painting
         those wedges from the highest contour down tints the low ground darkest,
         so the valley reads as a valley. Both the wedges and the contour lines
         come from the same Z(u, v), so they cannot disagree. */
      var BANDS = ['#ece6dc', '#e9e2d6', '#e6ded0', '#e3daca', '#e0d6c4',
        '#ddd2be', '#dacfb9', '#d7cbb4'];
      var labels = [];
      var LABEL_AT = { 15: 1, 13: 1, 11: 1 };
      var reach = VMAX / (S / K);
      for (var zc = 15, bi = 0; zc >= 8; zc--, bi++) {
        var uc = (Z0 - zc) / S;
        mapG.appendChild(el('polygon', {
          points: pts([[gx(uc), gy(0)], [gx(uc + 400), gy(-200)], [gx(uc + 1300), gy(-200)],
            [gx(uc + 1300), gy(200)], [gx(uc + 400), gy(200)]]),
          fill: BANDS[bi]
        }));
      }
      for (var zl = 15; zl >= 8; zl--) {
        var ul = (Z0 - zl) / S;
        mapG.appendChild(el('polyline', {
          points: pts([[gx(ul + reach), gy(-VMAX)], [gx(ul), gy(0)], [gx(ul + reach), gy(VMAX)]]),
          fill: 'none', stroke: '#c3b8a3', 'stroke-width': 0.7, 'stroke-linejoin': 'round'
        }));
        if (LABEL_AT[zl] && ul + reach <= ULEN - 12) {
          var lab = txt(gx(ul + reach), MAP_T + 9, (zl * MPU) + ' m', 8.5, '#7a736a');
          lab.setAttribute('stroke', '#e9e2d6');
          lab.setAttribute('stroke-width', '2.6');
          lab.setAttribute('paint-order', 'stroke');
          labels.push(lab);
        }
      }

      mapG.appendChild(el('line', {
        x1: gx(0), y1: gy(0), x2: gx(ULEN), y2: gy(0),
        stroke: '#7f99a3', 'stroke-width': 1.6
      }));
      mapG.appendChild(el('path', {
        d: 'M ' + gx(ULEN - 13) + ' ' + (gy(0) - 3.6) + ' L ' + gx(ULEN - 3) + ' ' + gy(0) +
          ' L ' + gx(ULEN - 13) + ' ' + (gy(0) + 3.6),
        fill: 'none', stroke: '#7f99a3', 'stroke-width': 1.6,
        'stroke-linecap': 'round', 'stroke-linejoin': 'round'
      }));

      var dipG = el('g', {});
      mapG.appendChild(dipG);

      var ghostG = el('g', { 'clip-path': 'url(#' + uid + '-m)' });
      var traceG = el('g', { 'clip-path': 'url(#' + uid + '-m)' });
      svg.appendChild(ghostG); svg.appendChild(traceG);
      var labG = el('g', { 'clip-path': 'url(#' + uid + '-m)' });
      var viewLbl = txt(MAP_L + 4, MAP_T + 9, 'from above', 8.5, '#7a736a', 'start');
      viewLbl.setAttribute('stroke', '#e9e2d6');
      viewLbl.setAttribute('stroke-width', '2.6');
      viewLbl.setAttribute('paint-order', 'stroke');
      labG.appendChild(viewLbl);
      labels.forEach(function (n) { labG.appendChild(n); });
      svg.appendChild(labG);

      /* the strip between the panels names the two ends of the valley */
      svg.appendChild(txt(MAP_L + 1, 97, '◂ upstream', 9, '#8d8880', 'start'));
      svg.appendChild(txt(MAP_R - 1, 97, 'downstream ▸', 9, '#8d8880', 'end'));

      /* section along the stream */
      svg.appendChild(el('rect', {
        x: MAP_L, y: SEC_T, width: ULEN, height: SEC_B - SEC_T,
        fill: '#f3efe8', stroke: '#e0d9cd', 'stroke-width': 0.8
      }));
      var secG = el('g', { 'clip-path': 'url(#' + uid + '-s)' });
      svg.appendChild(secG);
      secG.appendChild(el('polygon', {
        points: pts([[gx(0), sy(groundZ(0))], [gx(ULEN), sy(groundZ(ULEN))],
          [gx(ULEN), SEC_B], [gx(0), SEC_B]]),
        fill: '#dacfba'
      }));
      secG.appendChild(el('line', {
        x1: gx(0), y1: sy(groundZ(0)), x2: gx(ULEN), y2: sy(groundZ(ULEN)),
        stroke: '#7f99a3', 'stroke-width': 1.6
      }));
      secG.appendChild(txt(MAP_L + 4, SEC_T + 9, 'section along the stream · vertical scale ×3', 8.5, '#8d8880', 'start'));

      /* the bed twice: faint where erosion has removed it, solid underground */
      var sghostG = el('g', { 'clip-path': 'url(#' + uid + '-s)' });
      var sghostS = el('g', { 'clip-path': 'url(#' + uid + '-g)' });
      var sbedG = el('g', { 'clip-path': 'url(#' + uid + '-s)' });
      var sbedS = el('g', { 'clip-path': 'url(#' + uid + '-g)' });
      var sannG = el('g', { 'clip-path': 'url(#' + uid + '-s)' });
      svg.appendChild(sghostG); svg.appendChild(sghostS);
      svg.appendChild(sbedG); svg.appendChild(sbedS); svg.appendChild(sannG);

      var linkG = el('g', {});
      svg.appendChild(linkG);

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
      var deck = [makeRound(PRIMER)].concat(buildDeck()), deckAt = 0;
      var round = null, picked = null, locked = false;
      var streak = 0, attempted = 0, mastered = false;

      function pushState(extra) {
        var s = { streak: streak, mastered: mastered, attempted: attempted };
        if (round) {
          s.ask = round.dir;
          s.attitude = round.att;
          s.vPoints = round.trace.v;
          s.answer = round.answer;
        }
        if (extra) for (var k in extra) if (extra.hasOwnProperty(k)) s[k] = extra[k];
        root.dataset.svState = JSON.stringify(s);
      }

      /* ---------------------------------------------------------- drawing */

      var DIP_WORD = { horizontal: 'horizontal', vertical: 'vertical', down: 'dip', up: 'dip' };

      function drawDipSymbol() {
        clear(dipG);
        if (round.dir !== 'predict') return;
        var x = gx(40), y = gy(18), ink = '#3a352e';
        if (round.att === 'horizontal') {
          dipG.appendChild(el('circle', { cx: x, cy: y, r: 5.4, fill: 'none', stroke: ink, 'stroke-width': 1.5 }));
          dipG.appendChild(el('line', { x1: x - 9, y1: y, x2: x + 9, y2: y, stroke: ink, 'stroke-width': 1.5 }));
          dipG.appendChild(el('line', { x1: x, y1: y - 9, x2: x, y2: y + 9, stroke: ink, 'stroke-width': 1.5 }));
        } else if (round.att === 'vertical') {
          dipG.appendChild(el('line', { x1: x, y1: y - 10, x2: x, y2: y + 10, stroke: ink, 'stroke-width': 1.8 }));
          dipG.appendChild(el('line', { x1: x - 7, y1: y, x2: x + 7, y2: y, stroke: ink, 'stroke-width': 1.5 }));
        } else {
          var d = round.att === 'down' ? 1 : -1;
          dipG.appendChild(el('line', { x1: x, y1: y - 10, x2: x, y2: y + 10, stroke: ink, 'stroke-width': 1.8 }));
          dipG.appendChild(el('path', {
            d: 'M ' + x + ' ' + y + ' L ' + (x + d * 12) + ' ' + y +
              ' M ' + (x + d * 7.5) + ' ' + (y - 3.4) + ' L ' + (x + d * 12) + ' ' + y +
              ' L ' + (x + d * 7.5) + ' ' + (y + 3.4),
            fill: 'none', stroke: ink, 'stroke-width': 1.5,
            'stroke-linecap': 'round', 'stroke-linejoin': 'round'
          }));
        }
        dipG.appendChild(txt(x, y + 18, DIP_WORD[round.att], 8.5, '#5f5a51'));
      }

      function drawTrace() {
        clear(traceG);
        traceG.appendChild(el('polyline', {
          points: pts(tracePts(round)), fill: 'none', stroke: accent,
          'stroke-width': 2.2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round'
        }));
      }

      function drawGhostTrace(choice) {
        clear(ghostG);
        if (!choice) return;
        ghostG.appendChild(el('polyline', {
          points: pts(ghostPts(round, choice)), fill: 'none', stroke: '#2d2a26',
          'stroke-width': 1.5, 'stroke-dasharray': '4 3',
          'stroke-linejoin': 'round', 'stroke-linecap': 'round'
        }));
      }

      function drawBed(faint, solid, att, D, colour, dash, width) {
        var line = bedLine(round, att, D);
        function seg(op) {
          var a = { x1: line[0][0], y1: line[0][1], x2: line[1][0], y2: line[1][1],
            stroke: colour, 'stroke-width': width, 'stroke-linecap': 'round', opacity: op };
          if (dash) a['stroke-dasharray'] = dash;
          return el('line', a);
        }
        clear(faint); clear(solid);
        faint.appendChild(seg(0.38));
        solid.appendChild(seg(1));
      }

      /* where the bed line is actually inside the section panel */
      function bedRange(att, D) {
        if (att === 'vertical') return null;
        var P = bedP(att, D);
        var Zb0 = groundZ(round.uStar) - P * round.uStar;
        if (P === 0) {
          var y = sy(Zb0);
          return (y > SEC_T + 4 && y < SEC_B - 4) ? [12, ULEN - 12] : null;
        }
        var uA = ((CY0 - SEC_T) / VE - Zb0) / P;
        var uB = ((CY0 - SEC_B) / VE - Zb0) / P;
        var lo = Math.max(6, Math.min(uA, uB));
        var hi = Math.min(ULEN - 6, Math.max(uA, uB));
        return hi - lo > 26 ? [lo, hi] : null;
      }

      function arrowTo(g, x1, y1, x2, y2, colour, dashed, w) {
        var a = { x1: x1, y1: y1, x2: x2, y2: y2, stroke: colour,
          'stroke-width': w, 'stroke-linecap': 'round' };
        if (dashed) a['stroke-dasharray'] = '4 3';
        g.appendChild(el('line', a));
        var dx = x2 - x1, dy = y2 - y1, L = Math.sqrt(dx * dx + dy * dy) || 1;
        var ux = dx / L, uy = dy / L, h = 5;
        g.appendChild(el('path', {
          d: 'M ' + (x2 - ux * h - uy * h * 0.6) + ' ' + (y2 - uy * h + ux * h * 0.6) +
            ' L ' + x2 + ' ' + y2 +
            ' L ' + (x2 - ux * h + uy * h * 0.6) + ' ' + (y2 - uy * h - ux * h * 0.6),
          fill: 'none', stroke: colour, 'stroke-width': w,
          'stroke-linecap': 'round', 'stroke-linejoin': 'round'
        }));
      }

      /* An arrow ON the bed pointing the way it slopes down, with the words
         next to it. This is what makes "dip" mean something before a student
         is asked to use it. `which` is the direction being claimed, so a
         wrong guess draws its own arrow. */
      function drawBedArrow(att, D, which, colour, dashed) {
        clear(sannG);
        var lx, ly, w = dashed ? 1.6 : 1.9;
        if (att === 'vertical') {
          var xv = gx(round.uStar);
          arrowTo(sannG, xv, SEC_T + 10, xv, SEC_T + 26, colour, dashed, w);
          lx = xv; ly = SEC_T + 34;
        } else {
          var P = bedP(att, D);
          var Zb0 = groundZ(round.uStar) - P * round.uStar;
          var r = bedRange(att, D);
          if (!r) return;
          if (which === 'level') {
            lx = gx((r[0] + r[1]) / 2); ly = sy(Zb0 + P * (r[0] + r[1]) / 2) - 6;
          } else {
            var fwd = which === 'down' ? 1 : -1;
            var from = fwd > 0 ? r[0] : r[1];
            var span = fwd > 0 ? r[1] - r[0] : r[0] - r[1];
            var u1 = from + 0.38 * span, u2 = from + 0.76 * span;
            arrowTo(sannG, gx(u1), sy(Zb0 + P * u1), gx(u2), sy(Zb0 + P * u2), colour, dashed, w);
            var midY = sy(Zb0 + P * (u1 + u2) / 2);
            lx = gx((u1 + u2) / 2);
            ly = midY - 6.5 < SEC_T + 21 ? midY + 11 : midY - 6.5;
          }
        }
        lx = Math.max(MAP_L + 32, Math.min(MAP_R - 32, lx));
        ly = Math.max(SEC_T + 21, Math.min(SEC_B - 4, ly));
        var t = txt(lx, ly, SLOPE_PHRASE[which], 8.5, colour);
        t.setAttribute('stroke', '#e6ddce');
        t.setAttribute('stroke-width', '2.6');
        t.setAttribute('paint-order', 'stroke');
        sannG.appendChild(t);
      }

      function ghostDip(choice) {
        if (choice === 'horizontal' || choice === 'vertical') return 0;
        return round.att === 'down' || round.att === 'up' ? round.D : 0.1;
      }

      function drawLink() {
        clear(linkG);
        var x = gx(round.uStar);
        linkG.appendChild(el('line', {
          x1: x, y1: gy(0), x2: x, y2: sy(groundZ(round.uStar)),
          stroke: accent, 'stroke-width': 1, 'stroke-dasharray': '3 3'
        }));
        linkG.appendChild(el('circle', { cx: x, cy: gy(0), r: 2.2, fill: accent }));
        linkG.appendChild(el('circle', { cx: x, cy: sy(groundZ(round.uStar)), r: 2.2, fill: accent }));
      }

      /* --------------------------------------------------------- feedback */

      function contourM() { return Math.round(groundZ(round.uStar) * MPU); }

      function dipRight() {
        if (round.att === 'up') {
          return 'it slopes down to the left, upstream. That is what dip means — the way a bed tilts down into the ground. The valley floor slopes the other way.';
        }
        if (round.att === 'down') {
          return 'it slopes down to the right, downstream. That is what dip means — the way a bed tilts down into the ground. It drops faster than the valley floor.';
        }
        return 'it is level. The bed line is flat, so the bed stays at one height all the way. A level bed has no dip direction at all.';
      }

      function dipWrong(pick) {
        var said = 'you said ' + DIP_ECHO[pick] + '. ';
        if (round.att === 'up') {
          return said + 'Follow the bed itself, not the ground. The bed is higher on the right and lower on the left, so it slopes down to the left.';
        }
        if (round.att === 'down') {
          return said + 'Follow the bed itself. It starts high on the left and drops as it goes right, so it slopes down to the right.';
        }
        return said + 'The bed line is flat all the way across, so the bed stays at one height. It does not slope either way.';
      }

      function predictRight() {
        if (round.att === 'horizontal') {
          return 'the V points upstream. A bed that stays at one height follows a contour line, and contour lines bend upstream in a valley.';
        }
        if (round.att === 'vertical') {
          return 'there is no V. A vertical bed goes straight down, so it is at every height at once and the valley cannot bend it.';
        }
        if (round.att === 'down') {
          return 'the V points downstream. Going upstream, this bed rises faster than the valley floor, so you meet it high up the sides. The point of the V is left downstream.';
        }
        return 'the V points upstream. Going downstream, this bed rises while the valley floor drops, so you meet it up on the higher ground. The point of the V is left upstream.';
      }

      function predictWrong(pick) {
        var said = 'you said ' + PRED_ECHO[pick] + '. ';
        if (round.att === 'vertical') {
          return said + 'A vertical bed goes straight down, so it is at every height at once. The valley cannot bend it, and the boundary runs dead straight.';
        }
        if (pick === 'none') {
          return said + 'Only a vertical bed runs dead straight. This bed is ' +
            (round.att === 'horizontal' ? 'level' : 'tilted') +
            ', so the place where it meets the surface moves along the valley — the V points ' + round.trace.v + '.';
        }
        if (round.att === 'down') {
          return said + 'Going upstream, this bed rises faster than the valley floor, so you meet it high up the valley sides. That leaves the point of the V downstream.';
        }
        if (round.att === 'up') {
          return said + 'Going downstream, this bed rises while the valley floor drops, so you meet it up on the higher ground. That leaves the point of the V upstream.';
        }
        return said + 'A bed at one height follows a contour line, and contour lines bend upstream in a valley. So this boundary points upstream too.';
      }

      function readRight() {
        if (round.att === 'horizontal') {
          return 'horizontal. The boundary stays on the ' + contourM() +
            ' m contour the whole way, so the bed is all at one height. It points upstream because contour lines do.';
        }
        if (round.att === 'vertical') {
          return 'vertical. The boundary runs dead straight across the contours, so the valley makes no difference to it. Only a bed on end does that.';
        }
        if (round.att === 'down') {
          return 'it dips downstream. The V points downstream and its arms run back upstream, up the valley sides — so the bed rises upstream and slopes down to the right.';
        }
        return 'it dips upstream. The V points upstream and its arms run downstream, up the valley sides — so the bed rises downstream and slopes down to the left.';
      }

      function readWrong(pick) {
        var said = 'you said ' + ATT_ECHO[pick] + '. ';
        var v = round.trace.v;
        if (round.att === 'horizontal') {
          return said + 'Follow the boundary: it stays on the ' + contourM() +
            ' m contour the whole way, so the bed is all at one height — horizontal.';
        }
        if (round.att === 'vertical') {
          return said + 'A tilted or level bed follows the shape of the valley. This boundary runs dead straight across the contours, so the bed is vertical.';
        }
        if (pick === 'up') {
          return said + 'A bed dipping upstream rises downstream, so its V would point upstream. This V points downstream.';
        }
        if (pick === 'down') {
          return said + 'A bed dipping downstream rises upstream, so its V would point downstream. This V points upstream.';
        }
        if (pick === 'horizontal') {
          return said + 'A level bed stays on one contour. This boundary crosses the contours, and its V points ' +
            v + ' — so the bed dips ' + v + '.';
        }
        return said + 'A vertical bed runs dead straight. This boundary bends into a V pointing ' +
          v + ', so the bed dips ' + v + '.';
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
        picked = null; locked = false;

        clear(traceG); clear(ghostG); clear(sbedG); clear(sbedS);
        clear(sghostG); clear(sghostS); clear(linkG); clear(sannG);
        drawDipSymbol();

        var ids;
        if (round.dir === 'dip') {
          frame.textContent = 'Dip is the way a bed slopes down into the ground. The section shows one bed.';
          ask.textContent = 'Which way does this bed slope down?';
          drawBed(sbedG, sbedS, round.att, round.D, '#3a352e', '', 2.4);
          ids = DIP_ORDER;
        } else if (round.dir === 'predict') {
          frame.textContent = FRAME[round.att];
          ask.textContent = 'Which way does the boundary V across the valley?';
          drawBed(sbedG, sbedS, round.att, round.D, '#3a352e', '', 2.2);
          drawBedArrow(round.att, round.D, dipKey(round.att), '#3a352e', false);
          ids = PRED_ORDER;
        } else {
          frame.textContent = 'A boundary crosses this valley. Contours are in metres.';
          ask.textContent = 'Which way is this bed dipping — if at all?';
          drawTrace();
          ids = ATT_ORDER;
        }

        btns.forEach(function (b, n) {
          if (n >= ids.length) { b.style.display = 'none'; return; }
          b.style.display = '';
          b.value = ids[n];
          b.textContent = round.dir === 'predict' ? PRED_LABEL[ids[n]]
            : round.dir === 'dip' ? DIP_LABEL[ids[n]] : ATT_LABEL[ids[n]];
          b.setAttribute('aria-label', b.textContent);
          b.disabled = false;
          b.setAttribute('aria-pressed', 'false');
          b.classList.remove('is-ans');
        });

        go.textContent = 'Check';
        go.disabled = true;
        cap.className = 'cap rest';
        cap.textContent = round.dir === 'dip'
          ? 'The dark line is the bed. The blue-grey line is the valley floor.'
          : round.dir === 'predict'
            ? 'The section shows this bed under the valley floor.'
            : 'The boundary is drawn on the map; the contours give the heights.';
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

        if (round.dir === 'dip') {
          drawBedArrow(round.att, round.D, round.answer, accent, false);
        } else if (round.dir === 'predict') {
          drawTrace();
          if (ok) clear(ghostG);
        } else {
          drawBed(sbedG, sbedS, round.att, round.D, accent, '', 2.2);
          drawBedArrow(round.att, round.D, dipKey(round.att), accent, false);
          if (ok) { clear(sghostG); clear(sghostS); }
        }
        if (round.dir !== 'dip') drawLink();

        var body = round.dir === 'dip'
          ? (ok ? dipRight() : dipWrong(picked))
          : round.dir === 'predict'
            ? (ok ? predictRight() : predictWrong(picked))
            : (ok ? readRight() : readWrong(picked));
        if (justMastered) {
          body = 'that is three in a row, and you have it. A boundary follows the line where bed and ground are at the same height, so its V points the way the bed dips.';
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
          if (round.dir === 'dip') {
            drawBedArrow(round.att, round.D, picked, '#2d2a26', true);
            cap.textContent = 'Marked on the bed: ' + DIP_ECHO[picked] + '.';
          } else if (round.dir === 'predict') {
            drawGhostTrace(picked);
            cap.textContent = 'Drawn on the map: ' + PRED_ECHO[picked] + '.';
          } else {
            drawBed(sghostG, sghostS, picked, ghostDip(picked), '#2d2a26', '4 3', 1.8);
            drawBedArrow(picked, ghostDip(picked), dipKey(picked), '#2d2a26', true);
            cap.textContent = 'Drawn in the section: ' + ATT_ECHO[picked] + '.';
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
