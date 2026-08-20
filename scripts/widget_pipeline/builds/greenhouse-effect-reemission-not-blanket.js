/* ===========================================================================
   Where does the infrared go?

   Twelve packets of infrared leave the warm surface. Some meet a greenhouse
   gas molecule on the way up. The student commits to a prediction — how many
   come BACK DOWN, and how many STAY TRAPPED in the air — then runs it.

   A task frame under the title states the scenario and the ask; the three
   control groups are numbered 1-2-3 so the setting, the prediction and the
   commit do not read as equal siblings; and every dot in the picture is
   named by a legend, so nothing on the stage is decoration.

   The "trapped" row is the blanket picture written as a number. It comes out
   zero every single time, because a molecule that absorbs infrared re-emits
   it within a fraction of a second, in a direction it cannot choose. Half of
   what it absorbs therefore heads back towards the ground.

   Every tally is read off the simulated packet array, never hand-authored.
   =========================================================================== */
(function () {
  'use strict';

  var SVGNS = 'http://www.w3.org/2000/svg';
  var PACKETS = 12;
  var TARGET_STREAK = 3;
  var MAX_CHIP = 6;
  var DUR = 1300;      /* ms per packet flight */
  var STAGGER = 45;

  var SKIES = {
    less:  { key: 'less',  label: 'Less CO₂',  molecules: 9,  absorbed: [2, 4],  note: 'Less carbon dioxide' },
    today: { key: 'today', label: 'Today’s air', molecules: 20, absorbed: [6, 8],  note: 'Today’s air' },
    more:  { key: 'more',  label: 'More CO₂',  molecules: 36, absorbed: [10],    note: 'More carbon dioxide and methane' }
  };

  var CSS = [
    '.svw-ghg{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
    '.svw-ghg *{box-sizing:border-box}',
    '.svw-ghg .ghg-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--ghg-accent);margin:0 0 .16rem}',
    '.svw-ghg .ghg-ttl{font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;font-weight:600;line-height:1.2;margin:0 0 .3rem;color:#2d2a26}',
    '.svw-ghg .ghg-frame{font-size:.82rem;line-height:1.45;color:#5b564e;margin:0 0 .55rem}',
    '.svw-ghg .ghg-frame b{font-weight:600;color:#2d2a26}',
    '.svw-ghg .ghg-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;overflow:hidden;margin:0 0 .5rem}',
    '.svw-ghg .ghg-stage svg{display:block;width:100%}',
    '.svw-ghg .ghg-ctl{display:grid;grid-template-columns:1fr;gap:.5rem}',
    '.svw-ghg.ghg-wide .ghg-ctl{grid-template-columns:minmax(150px,.8fr) 1.6fr;gap:.9rem;align-items:start}',
    '.svw-ghg .ghg-lab{display:flex;align-items:center;gap:.4rem;font-size:.72rem;font-weight:600;color:#5b564e;margin:0 0 .26rem;line-height:1.35}',
    '.svw-ghg .ghg-sub{padding-left:calc(17px + .4rem)}',
    '.svw-ghg .ghg-step{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;width:17px;height:17px;border-radius:6px;background:var(--ghg-soft);color:var(--ghg-accent);font-size:.66rem;font-weight:700;line-height:1}',
    '.svw-ghg .ghg-row{display:flex;flex-wrap:wrap;gap:.28rem}',
    '.svw-ghg .ghg-row+.ghg-lab{margin-top:.4rem}',
    '.svw-ghg button{font-family:inherit;cursor:pointer;color:#2d2a26}',
    '.svw-ghg .ghg-opt{font-size:.78rem;font-weight:600;padding:.42rem .6rem;border-radius:9px;border:1px solid #ddd7cd;background:#faf8f5;line-height:1.15}',
    '.svw-ghg .ghg-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-ghg .ghg-chip{flex:1 1 0;min-width:32px;text-align:center;padding:.42rem .1rem;font-variant-numeric:tabular-nums}',
    '.svw-ghg .ghg-need{border-color:var(--ghg-accent);box-shadow:0 0 0 2px var(--ghg-soft)}',
    '.svw-ghg .ghg-derived{font-size:.74rem;color:#8d8880;margin:.3rem 0 0;font-variant-numeric:tabular-nums}',
    '.svw-ghg .ghg-foot{display:flex;align-items:center;gap:.5rem;margin:.55rem 0 0}',
    '.svw-ghg .ghg-go{font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5}',
    '.svw-ghg .ghg-go.ghg-primary{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-ghg .ghg-streak{font-size:.74rem;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svw-ghg .ghg-streak.ghg-done{color:#4f7d63;font-weight:600}',
    '.svw-ghg .ghg-cap{font-size:.84rem;line-height:1.5;margin:.45rem 0 0;min-height:3.1em;color:#2d2a26}',
    '.svw-ghg .ghg-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;border:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
  ].join('\n');

  /* --- small helpers ----------------------------------------------------- */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function svg(tag, attrs) {
    var n = document.createElementNS(SVGNS, tag);
    for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
    return n;
  }
  function rng(seed) {
    var s = (seed >>> 0) || 1;
    return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  }
  function shuffle(arr, r) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(r() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }
  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }
  /* a numbered chip carries the ORDER of the three control groups, so the
     setting, the prediction and the commit do not read as equal siblings */
  function stepChip(n) {
    var s = el('span', 'ghg-step', String(n));
    s.setAttribute('aria-hidden', 'true');
    return s;
  }
  function labelWith(step, text, extra) {
    var d = el('div', 'ghg-lab' + (extra ? ' ' + extra : ''));
    if (step) d.appendChild(stepChip(step));
    d.words = el('span', '', text);
    d.appendChild(d.words);
    return d;
  }

  window.SVWidget = {
    meta: {
      id: 'greenhouse-effect-reemission-not-blanket',
      title: 'Where does the infrared go?',
      teaches: 'Greenhouse gas molecules absorb outgoing infrared and re-emit it in random directions, so about half returns to the surface. Nothing is trapped.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var uid = 'g' + Math.floor(Math.random() * 1e9).toString(36);
      var reduced = !!ctx.reducedMotion;

      root.classList.add('svw-ghg');
      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
                   ctx.accent || '#8a6a4f';
      root.style.setProperty('--ghg-accent', accent);
      root.style.setProperty('--ghg-soft', accent + '33');

      var style = el('style');
      style.textContent = CSS;
      root.appendChild(style);

      /* --- state ---------------------------------------------------------- */
      var S = {
        skyKey: 'today',
        round: null,        /* {absorbed, packets:[{absorbed,dir}], id} */
        truth: null,
        down: null,         /* predicted */
        stuck: null,        /* predicted */
        phase: 'setup',     /* setup | revealed */
        correct: null,
        streak: 0,
        attempted: 0,
        mastered: false,
        roundId: 0
      };
      var animToken = 0;
      var flights = [];

      /* --- shell ---------------------------------------------------------- */
      root.appendChild(el('div', 'ghg-kick', 'Greenhouse effect'));
      root.appendChild(el('h3', 'ghg-ttl', 'Where does the infrared go?'));

      /* task frame: the scenario, then the ask. Not a how-to. */
      var frame = el('p', 'ghg-frame');
      frame.appendChild(document.createTextNode('The warm ground gives out '));
      frame.appendChild(el('b', '', '12 packets of infrared radiation'));
      frame.appendChild(document.createTextNode(
        ', heading up towards space. Predict how many escape, how many come back down, ' +
        'and how many stay trapped — then run it.'));
      root.appendChild(frame);

      var stageBox = el('div', 'ghg-stage');
      root.appendChild(stageBox);

      var ctl = el('div', 'ghg-ctl');
      root.appendChild(ctl);

      var gSky = el('div', 'ghg-grp');
      gSky.appendChild(labelWith(1, 'Greenhouse gas in the air'));
      var skyRow = el('div', 'ghg-row');
      gSky.appendChild(skyRow);
      ctl.appendChild(gSky);

      var gPred = el('div', 'ghg-grp');
      var labDown = labelWith(2, 'How many come back down?');
      var rowDown = el('div', 'ghg-row');
      var labStuck = labelWith(0, 'How many stay trapped in the air?', 'ghg-sub');
      var rowStuck = el('div', 'ghg-row');
      var derived = el('div', 'ghg-derived', '');
      gPred.appendChild(labDown); gPred.appendChild(rowDown);
      gPred.appendChild(labStuck); gPred.appendChild(rowStuck);
      gPred.appendChild(derived);
      ctl.appendChild(gPred);

      var foot = el('div', 'ghg-foot');
      var goBtn = el('button', 'ghg-go', 'Run it');
      goBtn.type = 'button';
      var streakOut = el('span', 'ghg-streak', '');
      foot.appendChild(stepChip(3));
      foot.appendChild(goBtn); foot.appendChild(streakOut);
      root.appendChild(foot);

      var cap = el('p', 'ghg-cap', '');
      root.appendChild(cap);

      var sr = el('p', 'ghg-sr', '');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* --- sky buttons ---------------------------------------------------- */
      var skyBtns = {};
      ['less', 'today', 'more'].forEach(function (k) {
        var b = el('button', 'ghg-opt', SKIES[k].label);
        b.type = 'button';
        b.setAttribute('aria-pressed', k === S.skyKey ? 'true' : 'false');
        b.addEventListener('click', function () {
          S.skyKey = k;
          newRound();
        });
        skyRow.appendChild(b);
        skyBtns[k] = b;
      });

      /* --- number chips --------------------------------------------------- */
      function chipRow(row, field, aria) {
        var btns = [];
        for (var v = 0; v <= MAX_CHIP; v++) {
          (function (val) {
            var b = el('button', 'ghg-opt ghg-chip', String(val));
            b.type = 'button';
            b.setAttribute('aria-pressed', 'false');
            b.setAttribute('aria-label', val + ' ' + aria);
            b.addEventListener('click', function () {
              if (S.phase === 'revealed') newRound();
              S[field] = val;
              paintChips();
              paintDerived();
              paintGo();
              pushState();
            });
            row.appendChild(b);
            btns.push(b);
          }(v));
        }
        return btns;
      }
      var downBtns = chipRow(rowDown, 'down', 'back down to the surface');
      var stuckBtns = chipRow(rowStuck, 'stuck', 'trapped in the air');

      /* --- stage ---------------------------------------------------------- */
      var geo = null;
      var svgRoot = null;
      var legend = null;

      function stageWidth() {
        var w = Math.round(stageBox.clientWidth || stageBox.getBoundingClientRect().width);
        return Math.max(240, w || 300);
      }
      function isWide() {
        var w = root.clientWidth || root.getBoundingClientRect().width;
        return w >= 520;
      }

      function buildGeometry() {
        var W = stageWidth();
        var H = isWide() ? 164 : 144;
        var padX = 12;
        var toaY = 30;
        var groundTop = H - 22;
        var bandTop = toaY + 12;
        var bandBot = groundTop - 24;
        var sky = SKIES[S.skyKey];
        var r = rng(S.roundId * 7919 + 13);

        /* greenhouse gas molecules on a jittered grid */
        var n = sky.molecules;
        var rows = n <= 10 ? 2 : (n <= 22 ? 3 : 4);
        var cols = Math.ceil(n / rows);
        var cw = (W - 2 * padX) / cols;
        var rh = (bandBot - bandTop) / rows;
        var mol = [];
        for (var i = 0; i < n; i++) {
          var rw = Math.floor(i / cols), cl = i % cols;
          mol.push({
            x: clamp(padX + (cl + 0.5) * cw + (r() - 0.5) * cw * 0.6, padX + 4, W - padX - 4),
            y: clamp(bandTop + (rw + 0.5) * rh + (r() - 0.5) * rh * 0.55, bandTop, bandBot),
            used: false
          });
        }

        /* packets leave the surface, evenly spread */
        var span = (W - 2 * padX) / PACKETS;
        var flightsOut = [];
        for (var p = 0; p < PACKETS; p++) {
          var px = padX + (p + 0.5) * span;
          var rec = S.round.packets[p];
          var f = { x0: px, y0: groundTop - 5, absorbed: rec.absorbed, dir: rec.dir, mol: null, pts: [] };
          if (!rec.absorbed) {
            f.pts = [[px, groundTop - 5], [clamp(px + (r() - 0.5) * 90, 8, W - 8), 7]];
          } else {
            /* nearest unused molecule above this packet */
            var best = -1, bestD = 1e9;
            for (var m = 0; m < mol.length; m++) {
              if (mol[m].used) continue;
              var d = Math.abs(mol[m].x - px) + Math.abs(mol[m].y - bandTop) * 0.25;
              if (d < bestD) { bestD = d; best = m; }
            }
            if (best < 0) best = 0;
            mol[best].used = true;
            f.mol = mol[best];
            var mx = mol[best].x, my = mol[best].y;
            var ex, ey;
            if (rec.dir === 'up') {
              ey = 7;
              var spread = (my - ey) * 0.85;
              ex = clamp(mx + (r() - 0.5) * 2 * spread, 6, W - 6);
              if (Math.abs(ex - mx) < 10) ex = mx + (ex >= mx ? 12 : -12);
            } else {
              ey = groundTop - 3;
              var spreadD = (ey - my) * 0.85;
              ex = clamp(mx + (r() - 0.5) * 2 * spreadD, 6, W - 6);
              if (Math.abs(ex - mx) < 10) ex = mx + (ex >= mx ? 12 : -12);
            }
            ex = clamp(ex, 6, W - 6);
            f.pts = [[px, groundTop - 5], [mx, my], [ex, ey]];
          }
          flightsOut.push(f);
        }
        return { W: W, H: H, padX: padX, toaY: toaY, groundTop: groundTop, mol: mol, flights: flightsOut };
      }

      function drawStage() {
        geo = buildGeometry();
        var W = geo.W, H = geo.H;
        stageBox.innerHTML = '';
        svgRoot = svg('svg', {
          viewBox: '0 0 ' + W + ' ' + H,
          width: W, height: H,
          role: 'img',
          'aria-label': 'Side view of the atmosphere: the surface below, greenhouse gas molecules above it, and space at the top.'
        });

        var defs = svg('defs', {});
        var mkOut = svg('marker', { id: uid + '-out', markerWidth: '6', markerHeight: '6', refX: '3.4', refY: '2', orient: 'auto' });
        mkOut.appendChild(svg('path', { d: 'M0,0 L4,2 L0,4 z', fill: '#9c948a' }));
        var mkBack = svg('marker', { id: uid + '-back', markerWidth: '6', markerHeight: '6', refX: '3.4', refY: '2', orient: 'auto' });
        mkBack.appendChild(svg('path', { d: 'M0,0 L4,2 L0,4 z', fill: accent }));
        defs.appendChild(mkOut); defs.appendChild(mkBack);
        svgRoot.appendChild(defs);

        /* bands */
        svgRoot.appendChild(svg('rect', { x: 0, y: 0, width: W, height: H, fill: '#faf8f5' }));
        svgRoot.appendChild(svg('rect', { x: 0, y: geo.toaY, width: W, height: geo.groundTop - geo.toaY, fill: '#f2ede4' }));
        svgRoot.appendChild(svg('line', {
          x1: 0, y1: geo.toaY, x2: W, y2: geo.toaY,
          stroke: '#ddd5c8', 'stroke-width': 1, 'stroke-dasharray': '4 4'
        }));
        svgRoot.appendChild(svg('rect', { x: 0, y: geo.groundTop, width: W, height: H - geo.groundTop, fill: '#c9bfae' }));
        svgRoot.appendChild(svg('line', { x1: 0, y1: geo.groundTop, x2: W, y2: geo.groundTop, stroke: '#b0a693', 'stroke-width': 1 }));

        var tSpace = svg('text', { x: 10, y: 19, fill: '#8d8880', 'font-size': '11', 'letter-spacing': '.08em', 'font-family': 'Inter,system-ui,sans-serif' });
        tSpace.textContent = 'SPACE';
        svgRoot.appendChild(tSpace);
        var tSurf = svg('text', { x: 10, y: H - 7, fill: '#584f42', 'font-size': '11', 'letter-spacing': '.08em', 'font-family': 'Inter,system-ui,sans-serif' });
        tSurf.textContent = 'SURFACE';
        svgRoot.appendChild(tSurf);

        /* molecules */
        var gMol = svg('g', {});
        geo.mol.forEach(function (m) {
          m.node = svg('circle', { cx: m.x, cy: m.y, r: 3, fill: '#b8afa1' });
          gMol.appendChild(m.node);
        });
        svgRoot.appendChild(gMol);

        /* legend: name both kinds of dot, so nothing in the picture is
           decoration. Both are replaced by the tallies after a run. */
        legend = svg('g', {});
        function key(x, y, text, fill, anchor, haloFill) {
          var t = svg('text', {
            x: x, y: y, fill: fill, 'font-size': '11', 'text-anchor': anchor,
            'font-family': 'Inter,system-ui,sans-serif',
            stroke: haloFill, 'stroke-width': '3', 'paint-order': 'stroke',
            'stroke-linejoin': 'round'
          });
          t.textContent = text;
          legend.appendChild(t);
          return t;
        }
        var kGas = key(W - 10, geo.toaY + 13, 'greenhouse gas molecules', '#6f685d', 'end', '#f2ede4');
        var kPk = key(W - 10, H - 7, '12 infrared packets', '#584f42', 'end', '#c9bfae');
        svgRoot.appendChild(legend);
        [[kGas, '#b8afa1', geo.toaY + 9], [kPk, '#2d2a26', H - 11]].forEach(function (pair) {
          var wid = 130;
          try { wid = pair[0].getComputedTextLength() || wid; } catch (e) { /* estimate */ }
          legend.insertBefore(svg('circle', {
            cx: clamp(W - 14 - wid - 4, 8, W - 8), cy: pair[2], r: 3, fill: pair[1]
          }), pair[0]);
        });

        /* flight paths, hidden until the run */
        flights = [];
        var gPath = svg('g', {});
        geo.flights.forEach(function (f, i) {
          var d = 'M' + f.pts[0][0] + ',' + f.pts[0][1];
          for (var k = 1; k < f.pts.length; k++) d += ' L' + f.pts[k][0] + ',' + f.pts[k][1];
          var back = f.absorbed && f.dir === 'down';
          var path = svg('path', {
            d: d, fill: 'none',
            stroke: back ? accent : '#9c948a',
            'stroke-width': back ? 1.9 : 1.3,
            'stroke-linecap': 'round',
            opacity: back ? 0.95 : 0.6
          });
          gPath.appendChild(path);
          var len = 0;
          try { len = path.getTotalLength(); } catch (e) { len = 0; }
          path.setAttribute('stroke-dasharray', len || 1);
          path.setAttribute('stroke-dashoffset', len || 1);
          flights.push({ path: path, len: len || 1, f: f, back: back, delay: i * STAGGER });
        });
        svgRoot.appendChild(gPath);

        /* packets waiting on the ground */
        var gDot = svg('g', {});
        geo.flights.forEach(function (f, i) {
          var c = svg('circle', { cx: f.x0, cy: f.y0, r: 3.4, fill: '#2d2a26' });
          gDot.appendChild(c);
          flights[i].dot = c;
        });
        svgRoot.appendChild(gDot);

        /* tallies live in the picture, added only after a run */
        var gTal = svg('g', {});
        svgRoot.appendChild(gTal);
        svgRoot.tallyGroup = gTal;

        stageBox.appendChild(svgRoot);
      }

      function showTallies() {
        if (!svgRoot || !svgRoot.tallyGroup) return;
        var g = svgRoot.tallyGroup;
        while (g.firstChild) g.removeChild(g.firstChild);
        if (legend) legend.setAttribute('opacity', 0);
        var W = geo.W, H = geo.H;
        function tag(x, y, text, fill, halo, weight, anchor) {
          var t = svg('text', {
            x: x, y: y, fill: fill, 'font-size': '11.5', 'text-anchor': anchor || 'end',
            'font-weight': weight || '600', 'font-family': 'Inter,system-ui,sans-serif',
            stroke: halo, 'stroke-width': '3.5', 'paint-order': 'stroke',
            'stroke-linejoin': 'round'
          });
          t.textContent = text;
          g.appendChild(t);
        }
        /* each tally is haloed in the colour of the band it sits in */
        tag(W - 10, 19, S.truth.space + ' escaped to space', '#5b564e', '#faf8f5');
        tag(10, geo.toaY + 19, S.truth.stuck + ' trapped in the air', '#7a736a', '#f2ede4', '600', 'start');
        tag(W - 10, H - 7, S.truth.down + ' back to the surface', accent, '#c9bfae', '700');
      }

      /* --- the round ------------------------------------------------------ */
      function newRound() {
        animToken++;
        S.roundId++;
        var sky = SKIES[S.skyKey];
        var r = rng(Math.floor(Math.random() * 1e9));
        var absorbed = sky.absorbed[Math.floor(r() * sky.absorbed.length)];

        var idx = [];
        for (var i = 0; i < PACKETS; i++) idx.push(i);
        shuffle(idx, r);
        var absorbedSet = {};
        for (var a = 0; a < absorbed; a++) absorbedSet[idx[a]] = true;

        /* re-emission direction: random, and over many packets half go down */
        var dirs = [];
        for (var d = 0; d < absorbed; d++) dirs.push(d < absorbed / 2 ? 'down' : 'up');
        shuffle(dirs, r);

        var packets = [], di = 0, downCount = 0;
        for (var p = 0; p < PACKETS; p++) {
          if (absorbedSet[p]) {
            var dir = dirs[di++];
            if (dir === 'down') downCount++;
            packets.push({ absorbed: true, dir: dir });
          } else {
            packets.push({ absorbed: false, dir: 'up' });
          }
        }

        S.round = { absorbed: absorbed, packets: packets };
        /* read the answer off the model, never hand-author it */
        S.truth = { down: downCount, space: PACKETS - downCount, stuck: 0 };
        S.phase = 'setup';
        S.correct = null;

        drawStage();
        paintSky();
        paintAsk();
        paintChips();
        paintDerived();
        paintGo();
        setCaption();
        pushState();
      }

      /* --- painting -------------------------------------------------------- */
      function paintSky() {
        for (var k in skyBtns) if (Object.prototype.hasOwnProperty.call(skyBtns, k)) {
          skyBtns[k].setAttribute('aria-pressed', k === S.skyKey ? 'true' : 'false');
        }
      }
      function paintChips() {
        downBtns.forEach(function (b, v) {
          b.setAttribute('aria-pressed', S.down === v ? 'true' : 'false');
          b.classList.remove('ghg-need');
        });
        stuckBtns.forEach(function (b, v) {
          b.setAttribute('aria-pressed', S.stuck === v ? 'true' : 'false');
          b.classList.remove('ghg-need');
        });
      }
      /* the round's one hidden fact — how many were absorbed — belongs where
         the prediction is made, not in a line below the button */
      function paintAsk() {
        labDown.words.textContent = S.round.absorbed +
          ' of the 12 are absorbed. How many come back down?';
      }
      function paintDerived() {
        if (S.down == null || S.stuck == null) {
          derived.textContent = 'The rest of the 12 escape to space.';
        } else {
          derived.textContent = 'Your prediction lets ' + (PACKETS - S.down - S.stuck) +
            ' of the 12 escape to space.';
        }
      }
      function paintGo() {
        var ready = S.down != null && S.stuck != null;
        goBtn.classList.toggle('ghg-primary', ready && S.phase === 'setup');
        if (S.phase === 'revealed') {
          goBtn.textContent = S.mastered ? 'Another anyway' : 'Go again';
          goBtn.classList.add('ghg-primary');
        } else {
          goBtn.textContent = 'Run it';
        }
      }
      function paintStreak() {
        if (S.mastered) {
          streakOut.textContent = 'You have it';
          streakOut.className = 'ghg-streak ghg-done';
        } else if (S.streak > 0) {
          streakOut.textContent = S.streak + ' in a row';
          streakOut.className = 'ghg-streak';
        } else {
          streakOut.textContent = S.attempted ? 'Streak reset' : '';
          streakOut.className = 'ghg-streak';
        }
      }

      function setCaption(text) {
        if (text) { cap.textContent = text; sr.textContent = text; return; }
        var sky = SKIES[S.skyKey], A = S.round.absorbed;
        cap.textContent = 'The other ' + (PACKETS - A) + ' packets meet nothing on the way up: ' +
          'they pass straight through and escape.';
        sr.textContent = sky.note + '. ' + A + ' of the 12 packets are absorbed. ' + cap.textContent;
      }

      /* --- commit ---------------------------------------------------------- */
      function commit() {
        if (S.phase === 'revealed') { newRound(); return; }
        if (S.down == null || S.stuck == null) {
          (S.down == null ? downBtns : stuckBtns).forEach(function (b) { b.classList.add('ghg-need'); });
          setCaption('The prediction needs both numbers — how many come back down, and how many stay trapped.');
          return;
        }
        var A = S.round.absorbed, D = S.truth.down, up = A - D;
        S.attempted++;
        S.correct = (S.down === D && S.stuck === 0);
        if (S.correct) {
          S.streak++;
          if (S.streak >= TARGET_STREAK) S.mastered = true;
        } else {
          S.streak = 0;
        }
        S.phase = 'revealed';

        var msg;
        if (S.correct && S.mastered && S.streak === TARGET_STREAK) {
          msg = 'Three in a row — you have it. Absorbed infrared is re-emitted at once in a random ' +
                'direction, so about half returns and the surface settles warmer.';
        } else if (S.correct && S.skyKey === 'more') {
          msg = 'Right — ' + D + ' back down, ' + up + ' onwards, none trapped. More greenhouse gas means ' +
                'more absorb-and-re-emit events, so more infrared returns to the ground.';
        } else if (S.correct) {
          msg = 'Right — ' + D + ' back down, ' + up + ' onwards, none trapped. A molecule cannot aim its ' +
                're-emission, so roughly half of what it absorbs heads back down.';
        } else if (S.stuck > 0) {
          msg = 'Nothing stays trapped. A molecule re-emits absorbed infrared in a fraction of a second — ' +
                'it cannot hold it like a blanket. ' + D + ' of the ' + A + ' came back down.';
        } else if (S.down === 0) {
          msg = 'You had it all escaping. A molecule cannot aim its re-emission, so ' + D + ' of the ' + A +
                ' absorbed came back down to the surface.';
        } else if (S.down === A) {
          msg = 'That is the mirror picture — all of it sent straight back. Re-emission is random, so only ' +
                'about half returns: ' + D + ' down, ' + up + ' onwards.';
        } else {
          msg = 'Re-emission is random, so about half of the absorbed infrared comes back down: ' + D +
                ' of the ' + A + ', not ' + S.down + '. None stays trapped.';
        }

        paintGo();
        paintStreak();
        setCaption(msg);
        pushState();
        run();
      }

      /* --- the run --------------------------------------------------------- */
      function markAbsorbers() {
        geo.flights.forEach(function (f) {
          if (f.absorbed && f.mol && f.mol.node) {
            f.mol.node.setAttribute('r', 4.6);
            f.mol.node.setAttribute('fill', accent);
          }
        });
      }
      function settle(fl) {
        fl.path.setAttribute('stroke-dashoffset', 0);
        fl.path.setAttribute('marker-end', 'url(#' + uid + (fl.back ? '-back' : '-out') + ')');
        var end = fl.f.pts[fl.f.pts.length - 1];
        if (end[1] <= 6) {
          fl.dot.setAttribute('opacity', 0);           /* gone into space */
        } else {
          fl.dot.setAttribute('cx', end[0]);
          fl.dot.setAttribute('cy', end[1]);
          fl.dot.setAttribute('fill', accent);
        }
      }
      function run() {
        markAbsorbers();
        if (reduced || !window.requestAnimationFrame) {
          flights.forEach(settle);
          showTallies();
          return;
        }
        var token = ++animToken, t0 = 0;
        flights.forEach(function (fl) { fl.dot.setAttribute('opacity', 1); });
        function step(ts) {
          if (token !== animToken) return;
          if (!t0) t0 = ts;
          var t = ts - t0, done = true;
          for (var i = 0; i < flights.length; i++) {
            var fl = flights[i];
            var u = clamp((t - fl.delay) / DUR, 0, 1);
            fl.path.setAttribute('stroke-dashoffset', fl.len * (1 - u));
            var pt = null;
            try { pt = fl.path.getPointAtLength(fl.len * u); } catch (e) { pt = null; }
            if (pt) { fl.dot.setAttribute('cx', pt.x); fl.dot.setAttribute('cy', pt.y); }
            if (u >= 1) settle(fl); else done = false;
          }
          if (done) { showTallies(); return; }
          window.requestAnimationFrame(step);
        }
        window.requestAnimationFrame(step);
      }

      /* --- state for the gate ---------------------------------------------- */
      function pushState() {
        var out = {
          sky: S.skyKey,
          absorbed: S.round ? S.round.absorbed : null,
          predictedDown: S.down,
          predictedStuck: S.stuck,
          phase: S.phase,
          correct: S.correct,
          streak: S.streak,
          mastered: S.mastered,
          attempted: S.attempted,
          round: S.roundId
        };
        if (S.phase === 'revealed' && S.truth) {
          out.backDown = S.truth.down;
          out.outToSpace = S.truth.space;
          out.stuck = S.truth.stuck;
        }
        root.dataset.svState = JSON.stringify(out);
      }

      goBtn.addEventListener('click', commit);

      /* keep the layout honest if the modal is resized */
      function fitWidth() {
        root.classList.toggle('ghg-wide', isWide());
      }
      fitWidth();
      newRound();

      if (window.ResizeObserver) {
        var ro = new window.ResizeObserver(function () {
          var was = root.classList.contains('ghg-wide');
          fitWidth();
          if (was !== root.classList.contains('ghg-wide') && S.phase === 'setup') {
            animToken++;
            drawStage();
          }
        });
        try { ro.observe(root); } catch (e) { /* no observer, no harm */ }
      }
    }
  };
}());
