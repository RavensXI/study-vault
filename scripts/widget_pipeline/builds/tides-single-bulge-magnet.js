/* tides-single-bulge-magnet — StudyVault lesson widget
   The Moon does not drag the sea to it like a magnet. Its pull is
   DIFFERENT at different parts of Earth: hardest on the near side, less at
   the centre, least on the far side. So the water stands high at both ends
   of the Earth–Moon line, and a coast turning through both of them meets a
   high tide about every 12 hours 25 minutes.

   One geometry drives everything: a Moon slot, a town slot and the ellipse
   the sea is drawn as. The marking answer, the timing answer, the picture
   and the closing sweep all read from that one model, so the reveal can
   never disagree with the question. */
(function () {
  'use strict';

  var META = {
    id: 'tides-single-bulge-magnet',
    title: 'High tide at Whitby',
    teaches: 'Tidal force is the difference in the Moon’s pull across Earth: the near side is pulled hardest, the centre less, the far side least. Water stands high at both ends, so a coast meets a high tide about every 12 hours 25 minutes.'
  };

  /* ---------- the model -------------------------------------------------
     Angles are degrees, anticlockwise on screen, measured at Earth's centre.
     Coast points sit in 8 slots, 45 degrees apart. The Moon sits in one of
     them. High water is at the Moon's slot and the slot opposite. Earth
     turns anticlockwise, so a coast's angle past the Moon grows with time. */

  var LUNAR_DAY = 24 + 50 / 60;      /* 24 h 50 min: a coast back under the Moon */
  var MOON_SLOTS = [0, 1, 3, 4, 5, 7];   /* keeps the stage wide, never tall */
  var OFFSETS = [0, 2, 4];               /* where Whitby starts, in slots */

  function highSlots(m) { return [m % 8, (m + 4) % 8]; }

  function hoursToNextHigh(offSlots) {
    var rel = (offSlots * 45) % 360;
    var next = rel < 180 ? 180 : 360;
    return LUNAR_DAY * (next - rel) / 360;
  }
  /* the verdict turns on an integer key, never on a float comparison */
  function timeKey(hours) { return hours > 9 ? '12' : '6'; }

  var TIME_OPTS = [
    ['6', 'About 6 hours'],
    ['12', 'About 12½ hours'],
    ['25', 'About 25 hours']
  ];
  /* The pull arrows are a GIVEN, on stage from the opening state: the student
     predicts the water from a shown mechanism instead of recalling it. One
     signed perpendicular offset per Moon slot keeps the three words clear of
     the coast markers, the Moon and the key at every deal. */
  var PULL_WORD = ['hardest', 'less', 'least'];
  var PULL_OFF = { 0: -11, 1: -11, 3: 11, 4: 11, 5: -16.5, 7: 16.5 };
  var GIVEN = 'The arrows are the Moon’s pull: hardest on the near side, less at the centre, ' +
    'least on the far side. A coast comes back round to the Moon every 24 hours 50 minutes.';
  var MECH = 'The far side is pulled least, so it gets left behind. That leaves the water ' +
    'high at both ends of the Moon’s line.';
  var TIME_SAID = { '6': 'about 6 hours', '12': 'about 12½ hours', '25': 'about 25 hours' };
  var NUMWORD = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight'];
  var REL_SAID = [
    'on the side facing the Moon',
    'an eighth of a turn past the Moon',
    'a quarter turn past the Moon',
    'three eighths of a turn past the Moon',
    'on the side facing away from the Moon',
    'five eighths of a turn past the Moon',
    'three quarters of a turn past the Moon',
    'seven eighths of a turn past the Moon'
  ];

  /* ---------- geometry of the one stage ---------- */
  var VW = 220, VH = 172, CX = 110, CY = 74;
  var ER = 38;                       /* Earth, and the ring the coast points sit on */
  var SEA_FLAT = 50;                 /* before the commit: an even sea all round */
  var SEA_RX = 62, SEA_RY = 44;      /* after: two bulges */
  var MOON_ORBIT = 84, MOON_R = 10;
  var MK = 26;                       /* marker hit area, px (the ring drawn is smaller) */

  var INK = '#2d2a26', MUT = '#8d8880', GREEN = '#4f7d63';

  function rad(d) { return d * Math.PI / 180; }
  function px(d) { return CX + ER * Math.cos(rad(d)); }
  function py(d) { return CY - ER * Math.sin(rad(d)); }
  function seaR(relDeg, rx, ry) {
    var c = Math.cos(rad(relDeg)), s = Math.sin(rad(relDeg));
    return 1 / Math.sqrt((c / rx) * (c / rx) + (s / ry) * (s / ry));
  }

  window.SVWidget = {
    meta: META,
    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || ctx.accent || '#8a6a4f';
      var calm = !!ctx.reducedMotion;

      /* ---------- style: every selector under .svw-tide ---------- */
      var css = [
        '.svw-tide{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:' + INK + ';line-height:1.45}',
        '.svw-tide *{box-sizing:border-box}',
        '.svw-tide .t-head{display:flex;align-items:baseline;justify-content:space-between;gap:.6rem}',
        '.svw-tide .t-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + '}',
        '.svw-tide .t-run{font-size:.7rem;color:' + MUT + ';font-variant-numeric:tabular-nums;white-space:nowrap}',
        '.svw-tide .t-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.16rem;margin:.08rem 0 .24rem;line-height:1.2}',
        '.svw-tide .t-frame{font-size:.82rem;color:#5b564e;margin:0 0 .4rem}',
        '.svw-tide .t-lab{display:flex;align-items:flex-start;gap:.35rem;font-size:.75rem;font-weight:600;color:#5b564e;line-height:1.3;margin:0 0 .26rem}',
        '.svw-tide .t-num{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;border-radius:50%;background:' + accent + '22;color:' + accent + ';font-size:.64rem;font-weight:700;flex:none;margin-top:1px}',
        '.svw-tide .t-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.3rem}',
        '.svw-tide .t-ring{position:relative;width:100%;max-width:244px;margin:0 auto}',
        '.svw-tide .t-base{display:block;width:100%;height:auto}',
        '.svw-tide .t-over,.svw-tide .t-top{position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none}',
        /* the coast buttons sit at z-index 1, so the pull arrows pass UNDER
           them while Whitby and the sweep dot ride above and stay findable */
        '.svw-tide .t-top{z-index:2}',
        '.svw-tide .t-mk{position:absolute;width:' + MK + 'px;height:' + MK + 'px;transform:translate(-50%,-50%);border:0;background:none;padding:0;margin:0;cursor:pointer;z-index:1;display:flex;align-items:center;justify-content:center}',
        '.svw-tide .t-mk i{display:block;width:16px;height:16px;border-radius:50%;border:1.5px solid #8f8778;background:rgba(255,255,255,.62)}',
        '.svw-tide .t-mk[aria-pressed="true"] i{border-width:2.5px;border-color:' + INK + ';background:rgba(45,42,38,.28)}',
        '.svw-tide .t-mk[data-key="1"] i{border-width:2.5px;border-color:' + GREEN + ';background:rgba(255,255,255,.62)}',
        '.svw-tide .t-mk[data-key="1"][aria-pressed="true"] i{background:rgba(79,125,99,.38)}',
        '.svw-tide .t-mk:focus-visible{outline:none}',
        '.svw-tide .t-mk:focus-visible i{box-shadow:0 0 0 3px ' + accent + '66}',
        '.svw-tide .t-mk:disabled{cursor:default}',
        '.svw-tide .t-grp{margin-top:.45rem}',
        '.svw-tide .t-grp[data-wake="0"]{opacity:.42}',
        '.svw-tide .t-opts{display:grid;grid-template-columns:repeat(3,1fr);gap:.32rem}',
        '.svw-tide .t-opt{font-family:inherit;font-size:.76rem;font-weight:600;line-height:1.2;color:' + INK + ';background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.4rem .24rem;min-height:36px;cursor:pointer}',
        '.svw-tide .t-opt[aria-pressed="true"]{background:' + INK + ';border-color:' + INK + ';color:#fff}',
        '.svw-tide .t-opt[data-key="1"]{box-shadow:inset 0 0 0 2px ' + GREEN + ';border-color:' + GREEN + '}',
        '.svw-tide .t-opt:disabled{cursor:default;opacity:1}',
        '.svw-tide .t-go{margin-top:.45rem;font-family:inherit;font-size:.82rem;font-weight:600;color:#fff;background:' + INK + ';border:1px solid ' + INK + ';border-radius:10px;padding:.46rem .95rem;cursor:pointer}',
        '.svw-tide .t-go:disabled{background:#efe9e0;border-color:#e0d9cd;color:#a49d93;cursor:default}',
        '.svw-tide .t-cap{margin:.42rem 0 0;font-size:.8rem;line-height:1.5;color:#5b564e;min-height:56px}',
        '.svw-tide .t-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}'
      ].join('');

      /* ---------- DOM, built once, then mutated ---------- */
      root.textContent = '';
      var styleTag = document.createElement('style');
      styleTag.textContent = css;
      root.appendChild(styleTag);

      var wrap = mk('div', 'svw-tide');
      root.appendChild(wrap);

      var head = mk('div', 't-head');
      var kick = mk('span', 't-kick'); kick.textContent = 'Tides';
      var run = mk('span', 't-run');
      head.appendChild(kick); head.appendChild(run);
      wrap.appendChild(head);

      var h = mk('div', 't-title'); h.textContent = META.title;
      wrap.appendChild(h);

      var frame = mk('p', 't-frame');
      frame.textContent = 'The Moon pulls on the Earth’s water. Where does that water stand high, and how long does Whitby wait for its next high tide?';
      wrap.appendChild(frame);

      wrap.appendChild(label('1', 'Predict where the sea stands highest — mark every coast point.'));

      var stage = mk('div', 't-stage');
      var ring = mk('div', 't-ring');
      stage.appendChild(ring);
      wrap.appendChild(stage);

      var g2 = mk('div', 't-grp');
      g2.appendChild(label('2', 'How long until Whitby’s next high tide?'));
      var opts2 = mk('div', 't-opts');
      var timeBtns = TIME_OPTS.map(function (o) {
        var b = mk('button', 't-opt');
        b.type = 'button'; b.dataset.val = o[0]; b.textContent = o[1];
        b.setAttribute('aria-pressed', 'false');
        opts2.appendChild(b);
        return b;
      });
      g2.appendChild(opts2);
      wrap.appendChild(g2);

      var go = mk('button', 't-go'); go.type = 'button'; go.textContent = 'Check';
      wrap.appendChild(go);

      var cap = mk('p', 't-cap');
      wrap.appendChild(cap);

      var sr = mk('p', 't-sr'); sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      /* ---------- the one stage: picture, coast markers, overlay ---------- */
      var base = svgel('svg', { viewBox: '0 0 ' + VW + ' ' + VH, role: 'img' });
      base.setAttribute('class', 't-base');
      ring.appendChild(base);

      /* the sea: one ellipse. A circle before the commit, two bulges after. */
      var sea = svgel('ellipse', {
        cx: CX, cy: CY, rx: SEA_FLAT, ry: SEA_FLAT,
        fill: accent + '2e', stroke: accent, 'stroke-width': 1.7
      });
      base.appendChild(sea);

      base.appendChild(svgel('circle', { cx: CX, cy: CY, r: ER, fill: '#d5cdbd', stroke: '#a49b8a', 'stroke-width': 1 }));

      /* which way Earth turns: the student needs it to time the next high tide */
      base.appendChild(svgel('path', {
        d: arcPath(CX, CY, 25, 188, 292), fill: 'none', stroke: '#8f8778',
        'stroke-width': 1.7, 'stroke-linecap': 'round'
      }));
      base.appendChild(svgel('path', { d: tangentHead(CX, CY, 25, 292), fill: '#8f8778' }));

      /* the Moon. The three pull arrows draw the Earth–Moon line, so there is
         no separate dashed line to double it. */
      var moonG = svgel('g', {});
      moonG.appendChild(svgel('circle', { r: MOON_R, fill: '#cfc8bc', stroke: '#a49d93', 'stroke-width': 1 }));
      moonG.appendChild(svgel('circle', { cx: -2.6, cy: -2.4, r: 2.4, fill: '#b6ada0' }));
      moonG.appendChild(svgel('circle', { cx: 3.2, cy: 2.6, r: 1.5, fill: '#b6ada0' }));
      base.appendChild(moonG);

      /* key, so no symbol is ever a mystery. It sits bottom left, and moves
         to the top left on the one round where the Moon would crowd it. */
      var keyG = svgel('g', {});
      keyG.appendChild(svgel('circle', { cx: 10, cy: 151, r: 4.2, fill: INK }));
      keyG.appendChild(svgtext(18, 154.5, 'Whitby', 'start', 9.5, MUT));
      keyG.appendChild(svgel('circle', { cx: 10, cy: 164, r: 4.8, fill: '#cfc8bc', stroke: '#a49d93', 'stroke-width': 1 }));
      keyG.appendChild(svgtext(18, 167.5, 'Moon', 'start', 9.5, MUT));
      base.appendChild(keyG);

      /* eight coast points, real buttons over the picture */
      var markers = [];
      for (var s = 0; s < 8; s++) {
        var b = mk('button', 't-mk');
        b.type = 'button';
        b.dataset.slot = String(s);
        b.setAttribute('aria-pressed', 'false');
        b.appendChild(document.createElement('i'));
        b.style.left = (px(s * 45) / VW * 100) + '%';
        b.style.top = (py(s * 45) / VH * 100) + '%';
        ring.appendChild(b);
        markers.push(b);
      }

      /* two overlays. The arrows go UNDER the coast buttons so a marked point
         is never cut by a shaft; Whitby, the sweep and the readout go OVER
         them so the town the timing question asks about is always findable. */
      var over = svgel('svg', { viewBox: '0 0 ' + VW + ' ' + VH, 'aria-hidden': 'true' });
      over.setAttribute('class', 't-over');
      ring.appendChild(over);
      var topLayer = svgel('svg', { viewBox: '0 0 ' + VW + ' ' + VH, 'aria-hidden': 'true' });
      topLayer.setAttribute('class', 't-top');
      ring.appendChild(topLayer);

      var arrows = [];
      for (var a = 0; a < 3; a++) {
        var g = svgel('g', {});
        var halo = svgel('line', { stroke: '#faf8f5', 'stroke-width': 4.4, 'stroke-linecap': 'round' });
        var shaft = svgel('line', { stroke: INK, 'stroke-width': 2, 'stroke-linecap': 'round' });
        var headP = svgel('path', { fill: INK, stroke: '#faf8f5', 'stroke-width': .7 });
        var lab = svgtext(0, 0, PULL_WORD[a], 'middle', 9, '#5b564e');
        lab.setAttribute('font-weight', '600');
        lab.setAttribute('stroke', '#faf8f5');
        lab.setAttribute('stroke-width', '2.4');
        lab.setAttribute('paint-order', 'stroke');
        g.appendChild(halo); g.appendChild(shaft); g.appendChild(headP); g.appendChild(lab);
        over.appendChild(g);
        arrows.push({ g: g, halo: halo, shaft: shaft, head: headP, lab: lab });
      }
      var townDot = svgel('circle', { r: 4.2, fill: INK, stroke: '#faf8f5', 'stroke-width': 1 });
      topLayer.appendChild(townDot);
      var sweepDot = svgel('circle', { r: 4.6, fill: accent, stroke: '#faf8f5', 'stroke-width': 1.3, opacity: '0' });
      topLayer.appendChild(sweepDot);
      var readout = svgtext(VW - 8, 167.5, '', 'end', 9.5, '#5b564e');
      topLayer.appendChild(readout);

      /* ---------- state ---------- */
      var round = { moon: 0, off: 0 };
      var deck = [], lastOff = -1, first = true;
      var picks = {}, pickTime = null;
      var phase = 'answer';
      var streak = 0, attempted = 0, mastered = false;
      var raf = 0;

      newRound();

      /* ---------- interaction ---------- */
      markers.forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (phase !== 'answer') { return; }
          var k = btn.dataset.slot;
          if (picks[k]) { delete picks[k]; } else { picks[k] = 1; }
          paint(); publish();
        });
      });
      timeBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (phase !== 'answer' || btn.disabled) { return; }
          pickTime = btn.dataset.val;
          paint(); publish();
        });
      });
      go.addEventListener('click', function () {
        if (phase === 'answer') { commit(); } else { newRound(); }
      });

      /* ---------- commit: the only place a verdict appears ---------- */
      function commit() {
        var chosen = pickList();
        if (!chosen.length || !pickTime) { return; }
        var hs = highSlots(round.moon);
        var okMark = chosen.length === 2 && chosen.indexOf(hs[0]) >= 0 && chosen.indexOf(hs[1]) >= 0;
        var ansKey = timeKey(hoursToNextHigh(round.off));
        var okTime = pickTime === ansKey;
        var right = okMark && okTime;

        attempted++;
        streak = right ? streak + 1 : 0;
        if (streak >= 3) { mastered = true; }
        phase = 'revealed';

        var ansSaid = TIME_SAID[ansKey];
        var me = markEcho(chosen, hs);
        var msg;
        if (streak === 3) {
          msg = 'Three in a row — you have it. The near side is pulled hardest and the far side least, ' +
            'so the water heaps up at both ends. A coast meets a high tide about every 12 hours 25 minutes.';
        } else if (right) {
          msg = 'Right — ' + me + ', and ' + ansSaid + '. ' + MECH;
        } else if (okTime) {
          msg = 'Not quite — the timing was right, but ' + me + '. ' + MECH;
        } else if (okMark) {
          msg = 'Not quite — you found both high-tide places, but you said ' + TIME_SAID[pickTime] +
            '. Whitby passes a high about every 12 hours 25 minutes, so its next one is ' + ansSaid + '.';
        } else {
          msg = 'Not quite — ' + me + ', and you said ' + TIME_SAID[pickTime] + '. ' + MECH +
            ' Whitby’s next high tide is ' + ansSaid + '.';
        }
        say(msg);
        paint();
        publish();
        reveal();
        try { go.focus(); } catch (e) { /* focus is a nicety, not a requirement */ }
      }

      function markEcho(chosen, hs) {
        var n = chosen.length;
        if (n === 1) {
          var rel = ((chosen[0] - round.moon) % 8 + 8) % 8;
          if (rel === 0) { return 'you marked the near side only'; }
          if (rel === 4) { return 'you marked the far side only'; }
          return 'you marked one point, off the line';
        }
        if (n === 2 && chosen.indexOf(hs[0]) >= 0 && chosen.indexOf(hs[1]) >= 0) {
          return 'you marked both ends of the line';
        }
        if (n === 2) { return 'you marked two wrong points'; }
        return 'you marked ' + NUMWORD[Math.min(n, 8)] + ' points';
      }

      /* ---------- rounds ---------- */
      function newRound() {
        cancel();
        if (first) { round = { moon: 0, off: 0 }; first = false; }
        else { round = dealt(); }
        lastOff = round.off;
        picks = {}; pickTime = null; phase = 'answer';
        drawRound();
        paint();
        publish();
      }

      function dealt() {
        if (!deck.length) {
          MOON_SLOTS.forEach(function (m) {
            OFFSETS.forEach(function (o) { deck.push({ moon: m, off: o }); });
          });
          for (var i = deck.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1)), t = deck[i]; deck[i] = deck[j]; deck[j] = t;
          }
        }
        var at = -1;
        for (var k = 0; k < deck.length; k++) { if (deck[k].off !== lastOff) { at = k; break; } }
        if (at < 0) { at = 0; }
        return deck.splice(at, 1)[0];
      }

      /* ---------- drawing: one model, every view ---------- */
      function drawRound() {
        var md = round.moon * 45;
        var ux = Math.cos(rad(md)), uy = -Math.sin(rad(md));
        var mx = CX + MOON_ORBIT * ux, my = CY + MOON_ORBIT * uy;
        moonG.setAttribute('transform', 'translate(' + r2(mx) + ' ' + r2(my) + ')');

        keyG.setAttribute('transform', round.moon === 5 ? 'translate(0 -139)' : 'translate(0 0)');

        var td = ((round.moon + round.off) % 8) * 45;
        townDot.setAttribute('cx', r2(px(td)));
        townDot.setAttribute('cy', r2(py(td)));

        sea.setAttribute('rx', SEA_FLAT);
        sea.setAttribute('ry', SEA_FLAT);
        sea.setAttribute('transform', 'rotate(' + (-md) + ' ' + CX + ' ' + CY + ')');

        showArrows();
        sweepDot.setAttribute('opacity', '0');
        readout.textContent = '';

        var townSlot = (round.moon + round.off) % 8;
        markers.forEach(function (btn, i) {
          var rel = ((i - round.moon) % 8 + 8) % 8;
          var isTown = i === townSlot;
          btn.setAttribute('aria-label', (isTown ? 'Whitby, ' : 'Coast point ') + REL_SAID[rel]);
          btn.title = isTown ? 'Whitby' : 'Coast point';
        });

        base.setAttribute('aria-label', 'A view down onto Earth from above the North Pole. Earth turns anticlockwise, ' +
          'the Moon lies out to one side, and eight coast points are marked round the shore. Whitby is the solid dot. ' +
          'Three arrows on the Earth–Moon line show the Moon’s pull: hardest on the near side, less at the centre, least on the far side.');
      }

      function setArrow(ar, a0, a1, ux, uy, off) {
        var x0 = CX + a0 * ux, y0 = CY + a0 * uy;
        var x1 = CX + a1 * ux, y1 = CY + a1 * uy;
        var hx = x1 - 5 * ux, hy = y1 - 5 * uy;
        var nx = -uy, ny = ux;
        ar.halo.setAttribute('x1', r2(x0)); ar.halo.setAttribute('y1', r2(y0));
        ar.halo.setAttribute('x2', r2(hx)); ar.halo.setAttribute('y2', r2(hy));
        ar.shaft.setAttribute('x1', r2(x0)); ar.shaft.setAttribute('y1', r2(y0));
        ar.shaft.setAttribute('x2', r2(hx)); ar.shaft.setAttribute('y2', r2(hy));
        ar.head.setAttribute('d', 'M' + r2(x1) + ' ' + r2(y1) +
          'L' + r2(hx + 3.2 * nx) + ' ' + r2(hy + 3.2 * ny) +
          'L' + r2(hx - 3.2 * nx) + ' ' + r2(hy - 3.2 * ny) + 'Z');
        var mid = (a0 + a1) / 2;
        ar.lab.setAttribute('x', r2(CX + mid * ux + off * nx));
        ar.lab.setAttribute('y', r2(CY + mid * uy + off * ny));
      }

      function setSweep(absDeg, rx, ry) {
        var r = seaR(absDeg - round.moon * 45, rx, ry);
        sweepDot.setAttribute('cx', r2(CX + r * Math.cos(rad(absDeg))));
        sweepDot.setAttribute('cy', r2(CY - r * Math.sin(rad(absDeg))));
      }

      function paintSea(p) {
        var rx = SEA_FLAT + (SEA_RX - SEA_FLAT) * p;
        var ry = SEA_FLAT + (SEA_RY - SEA_FLAT) * p;
        sea.setAttribute('rx', r2(rx));
        sea.setAttribute('ry', r2(ry));
        return { rx: rx, ry: ry };
      }

      /* the three-arrow picture: hardest at the near side, least at the far
         side. Drawn from the opening state, so the marking question is a
         prediction from a shown mechanism, not a memory test. */
      function showArrows() {
        var md = round.moon * 45;
        var ux = Math.cos(rad(md)), uy = -Math.sin(rad(md));
        var off = PULL_OFF[round.moon] || -11;
        setArrow(arrows[0], ER, ER + 27, ux, uy, off);
        setArrow(arrows[1], 0, 19, ux, uy, off);
        setArrow(arrows[2], -ER, -ER + 11, ux, uy, off);
      }

      /* The reveal is a demonstration, not a question. The even sea pulls out
         into two bulges under the arrows the student has been reading all
         along, then Whitby is carried once round so both of its high tides
         are seen happening. */
      function reveal() {
        var td = ((round.moon + round.off) % 8) * 45;
        if (calm) {
          var d0 = paintSea(1);
          sweepDot.setAttribute('opacity', '1');
          setSweep(td, d0.rx, d0.ry);
          readout.textContent = '12½ h between high tides';
          return;
        }
        var t0 = 0;
        cancel();
        sweepDot.setAttribute('opacity', '1');
        raf = requestAnimationFrame(function step(ts) {
          if (!root.isConnected) { raf = 0; return; }
          if (!t0) { t0 = ts; }
          var t = ts - t0;
          var mp = Math.min(1, t / 620);
          var e = mp < .5 ? 2 * mp * mp : 1 - Math.pow(-2 * mp + 2, 2) / 2;
          var d = paintSea(e);
          var sp = Math.max(0, Math.min(1, (t - 900) / 3000));
          var ang = td + 360 * sp;
          setSweep(ang, d.rx, d.ry);
          if (t > 900) {
            var relPos = ((ang - round.moon * 45) % 360 + 360) % 360;
            var word = (relPos < 24 || relPos > 336 || Math.abs(relPos - 180) < 24) ? 'high tide'
              : (Math.abs(relPos - 90) < 24 || Math.abs(relPos - 270) < 24) ? 'low tide' : 'in between';
            readout.textContent = '+' + (LUNAR_DAY * sp).toFixed(1) + ' h · ' + word;
          }
          if (t < 3960) { raf = requestAnimationFrame(step); }
          else {
            raf = 0;
            var d1 = paintSea(1);
            setSweep(td, d1.rx, d1.ry);
            readout.textContent = '12½ h between high tides';
          }
        });
      }
      function cancel() { if (raf) { cancelAnimationFrame(raf); raf = 0; } }

      /* ---------- controls and caption ---------- */
      function pickList() {
        var out = [];
        for (var k in picks) { if (Object.prototype.hasOwnProperty.call(picks, k)) { out.push(+k); } }
        return out.sort(function (x, y) { return x - y; });
      }

      function paint() {
        var hs = highSlots(round.moon);
        var chosen = pickList();
        var ansKey = timeKey(hoursToNextHigh(round.off));

        markers.forEach(function (btn, i) {
          btn.setAttribute('aria-pressed', picks[i] ? 'true' : 'false');
          if (phase === 'revealed' && (i === hs[0] || i === hs[1])) { btn.dataset.key = '1'; }
          else { delete btn.dataset.key; }
          btn.disabled = phase !== 'answer';
        });
        timeBtns.forEach(function (btn) {
          btn.setAttribute('aria-pressed', btn.dataset.val === pickTime ? 'true' : 'false');
          if (phase === 'revealed' && btn.dataset.val === ansKey) { btn.dataset.key = '1'; }
          else { delete btn.dataset.key; }
          btn.disabled = phase !== 'answer' || !chosen.length;
        });
        g2.dataset.wake = chosen.length ? '1' : '0';

        if (phase === 'answer') {
          go.textContent = 'Check';
          go.disabled = !(chosen.length && pickTime);
          /* the model facts stay put while the student reasons from them; the
             pressed markers and the filled time button carry the live values */
          say(GIVEN);
        } else {
          go.textContent = mastered ? 'Another anyway' : 'Next';
          go.disabled = false;
        }
        run.textContent = mastered ? 'You have it'
          : streak === 0 ? ''
            : streak + ' in a row — ' + (3 - streak) + ' more';
      }

      /* the live region only speaks when the words actually change, so
         marking a coast point does not re-read the standing model facts */
      function say(msg) { cap.textContent = msg; if (sr.textContent !== msg) { sr.textContent = msg; } }

      function publish() {
        var hours = hoursToNextHigh(round.off);
        root.dataset.svState = JSON.stringify({
          moonSlot: round.moon,
          townSlot: (round.moon + round.off) % 8,
          offsetSlots: round.off,
          highSlots: highSlots(round.moon),
          hoursToNextHigh: Math.round(hours * 100) / 100,
          timeAnswer: timeKey(hours),
          marked: pickList(),
          pickTime: pickTime,
          phase: phase,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      /* ---------- small helpers ---------- */
      function mk(tag, cls) { var n = document.createElement(tag); if (cls) { n.className = cls; } return n; }
      function r2(v) { return Math.round(v * 100) / 100; }
      function svgel(tag, attrs) {
        var n = document.createElementNS('http://www.w3.org/2000/svg', tag);
        for (var k in attrs) { if (Object.prototype.hasOwnProperty.call(attrs, k)) { n.setAttribute(k, attrs[k]); } }
        return n;
      }
      function svgtext(x, y, txt, anchor, size, fill) {
        var n = svgel('text', {
          x: x, y: y, 'text-anchor': anchor, 'font-size': size, fill: fill,
          'font-family': 'Inter,system-ui,sans-serif'
        });
        n.textContent = txt;
        return n;
      }
      function arcPath(cx, cy, r, d0, d1) {
        var x0 = cx + r * Math.cos(rad(d0)), y0 = cy - r * Math.sin(rad(d0));
        var x1 = cx + r * Math.cos(rad(d1)), y1 = cy - r * Math.sin(rad(d1));
        return 'M' + r2(x0) + ' ' + r2(y0) + 'A' + r + ' ' + r + ' 0 0 0 ' + r2(x1) + ' ' + r2(y1);
      }
      function tangentHead(cx, cy, r, d) {
        var x = cx + r * Math.cos(rad(d)), y = cy - r * Math.sin(rad(d));
        var tx = -Math.sin(rad(d)), ty = -Math.cos(rad(d));
        var nx = -ty, ny = tx;
        return 'M' + r2(x + 5.5 * tx) + ' ' + r2(y + 5.5 * ty) +
          'L' + r2(x + 3.1 * nx) + ' ' + r2(y + 3.1 * ny) +
          'L' + r2(x - 3.1 * nx) + ' ' + r2(y - 3.1 * ny) + 'Z';
      }
      function label(num, question) {
        var box = mk('div', 't-lab');
        var chip = mk('span', 't-num'); chip.textContent = num;
        var q = mk('span'); q.textContent = question;
        box.appendChild(chip); box.appendChild(q);
        return box;
      }
    }
  };
})();
