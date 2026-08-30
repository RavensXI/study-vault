/* ===========================================================================
   Where does the infrared go?

   A step-through DEMONSTRATION, not a question. Tom's field ruling (20 Aug):
   the old predict-and-check version asked "how many stay trapped?", whose
   answer is 0 in every round, and "how many come back down?", whose answer is
   about half with a tolerance — so after round one the student was re-typing a
   constant. Where no fair, variable question exists, BUILD_GUIDE 0b says build
   the demonstration instead: no verdict, no streak, no marking.

   Five steps follow twelve packets of infrared from the warm ground to
   wherever they end up. The ledger under the picture always totals 12, and its
   TRAPPED column reads 0 at every step, in every sky — that is the blanket
   misconception, named on screen and killed by the arithmetic.

   The one real variable stays explorable: the CO2 buttons change how many
   packets meet a molecule, and so how many are sent back down. Step 5 asks for
   exactly that comparison.

   Every number is counted off the simulated packet array, never hand-authored.
   =========================================================================== */
(function () {
  'use strict';

  var SVGNS = 'http://www.w3.org/2000/svg';
  var PACKETS = 12;
  var DUR = 850;       /* ms for one packet's move between steps */
  var STAGGER = 38;    /* ms between packets, so they do not move as a block */

  /* Absorbed counts are deliberately never half of 12: the absorbed group and
     the group that meets nothing must differ in size (4/8, 7/5, 10/2), so no
     sentence can ever say a bare "the 6" and leave the student guessing which
     six it means. */
  var SKIES = {
    less:  { key: 'less',  label: 'Less CO₂',  molecules: 9,  absorbed: 4,  note: 'Less carbon dioxide' },
    today: { key: 'today', label: 'Today’s air', molecules: 20, absorbed: 7,  note: 'Today’s air' },
    more:  { key: 'more',  label: 'More CO₂',  molecules: 36, absorbed: 10, note: 'More carbon dioxide' }
  };
  var SKY_ORDER = ['less', 'today', 'more'];

  /* pa/pb are how far along its first and second leg each packet has flown at
     that step; mol says whether the absorbing molecules are lit. */
  var STEPS = [
    {
      pa: 0.28, pb: 0, mol: false,
      text: function () {
        return 'Twelve packets of infrared leave the warm ground and head up towards space.';
      }
    },
    {
      pa: 1, pb: 0, mol: false,
      text: function (m) {
        return m.free + ' of the 12 meet nothing on the way up and sail straight out to space. ' +
               'The other ' + m.absorbed + ' are absorbed by a greenhouse gas molecule.';
      }
    },
    {
      pa: 1, pb: 0, mol: true,
      text: function () {
        return 'Each molecule re-emits its packet within a fraction of a second, in a direction ' +
               'it cannot choose. Nothing is held — the trapped column stays 0.';
      }
    },
    {
      pa: 1, pb: 1, mol: true,
      text: function (m) {
        return 'Re-emission is random, so about half of the absorbed packets are flung back down: ' +
               m.down + ' reach the surface, ' + m.space + ' carry on out.';
      }
    },
    {
      pa: 1, pb: 1, mol: true,
      text: function (m) {
        return m.note + ': ' + m.down + ' of the 12 come back down. Try ' + m.others +
               ' — more greenhouse gas, more absorb-and-re-emit events, more infrared returned.';
      }
    }
  ];

  var LEDGER = [
    { key: 'air',     label: 'In the air' },
    { key: 'down',    label: 'Back down' },
    { key: 'space',   label: 'Out to space' },
    { key: 'trapped', label: 'Trapped' }
  ];

  var CSS = [
    '.svw-ghg{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
    '.svw-ghg *{box-sizing:border-box}',
    '.svw-ghg .ghg-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--ghg-accent);margin:0 0 .16rem}',
    '.svw-ghg .ghg-ttl{font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;font-weight:600;line-height:1.2;margin:0 0 .3rem;color:#2d2a26}',
    '.svw-ghg .ghg-frame{font-size:.82rem;line-height:1.45;color:#5b564e;margin:0 0 .55rem}',
    '.svw-ghg .ghg-frame b{font-weight:600;color:#2d2a26}',
    '.svw-ghg .ghg-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;overflow:hidden;margin:0 0 .5rem}',
    '.svw-ghg .ghg-stage svg{display:block;width:100%}',
    '.svw-ghg .ghg-ledger{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid #e8e2d9}',
    '.svw-ghg .ghg-cell{padding:.4rem .25rem .45rem;text-align:center;border-left:1px solid #efe9e0}',
    '.svw-ghg .ghg-cell:first-child{border-left:0}',
    '.svw-ghg .ghg-cl{font-size:.66rem;font-weight:600;color:#8d8880;line-height:1.2}',
    '.svw-ghg .ghg-cv{font-size:.98rem;font-weight:600;line-height:1.25;font-variant-numeric:tabular-nums}',
    '.svw-ghg .ghg-cell.ghg-live .ghg-cv{color:var(--ghg-accent)}',
    '.svw-ghg .ghg-cap{font-size:.84rem;line-height:1.45;margin:0 0 .55rem;min-height:4.4em;color:#2d2a26}',
    '.svw-ghg .ghg-ctl{display:grid;grid-template-columns:1fr;gap:.5rem}',
    '.svw-ghg.ghg-wide .ghg-ctl{grid-template-columns:1.15fr 1fr;gap:.9rem;align-items:end}',
    '.svw-ghg .ghg-lab{font-size:.72rem;font-weight:600;color:#5b564e;margin:0 0 .26rem;line-height:1.35}',
    '.svw-ghg .ghg-row{display:flex;flex-wrap:wrap;gap:.28rem}',
    '.svw-ghg button{font-family:inherit;cursor:pointer;color:#2d2a26}',
    '.svw-ghg .ghg-opt{font-size:.78rem;font-weight:600;padding:.4rem .6rem;border-radius:9px;border:1px solid #ddd7cd;background:#faf8f5;line-height:1.15}',
    '.svw-ghg .ghg-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-ghg .ghg-nav{display:flex;align-items:center;gap:.4rem}',
    '.svw-ghg .ghg-btn{font-size:.82rem;font-weight:600;padding:.5rem .9rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5}',
    '.svw-ghg .ghg-btn.ghg-primary{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-ghg .ghg-btn[disabled]{opacity:.45;cursor:default}',
    '.svw-ghg .ghg-count{font-size:.74rem;color:#8d8880;margin-left:auto;font-variant-numeric:tabular-nums}',
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
  function ease(u) { return u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2; }

  window.SVWidget = {
    meta: {
      id: 'greenhouse-effect-reemission-not-blanket',
      title: 'Where does the infrared go?',
      teaches: 'Greenhouse gas molecules absorb outgoing infrared and re-emit it in random directions within a fraction of a second, so about half returns to the surface. Nothing is trapped.'
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
        step: 0,                 /* index into STEPS */
        maxStep: 0,
        seen: { today: true },
        round: null,             /* {absorbed, free, down, space, packets} */
        sceneId: 0
      };
      var animToken = 0;
      var flights = [];
      var geo = null;
      var svgRoot = null;
      var cur = { a: 0, b: 0 };  /* how far the packets have flown right now */

      /* --- shell ---------------------------------------------------------- */
      root.appendChild(el('div', 'ghg-kick', 'Greenhouse effect'));
      root.appendChild(el('h3', 'ghg-ttl', 'Where does the infrared go?'));

      /* task frame: what you will watch, and what to watch for */
      var frame = el('p', 'ghg-frame');
      frame.appendChild(document.createTextNode('The warm ground gives out '));
      frame.appendChild(el('b', '', '12 packets of infrared radiation'));
      frame.appendChild(document.createTextNode(
        '. Step through what happens to them — and watch what changes when there is more CO₂ in the air.'));
      root.appendChild(frame);

      var stageBox = el('div', 'ghg-stage');
      var svgWrap = el('div', 'ghg-svgwrap');
      stageBox.appendChild(svgWrap);

      /* the running ledger: it totals 12 at every step, and TRAPPED never moves */
      var ledgerBox = el('div', 'ghg-ledger');
      var cells = {};
      LEDGER.forEach(function (c) {
        var cell = el('div', 'ghg-cell' + (c.key === 'down' ? ' ghg-live' : ''));
        var v = el('div', 'ghg-cv', '0');
        cell.appendChild(v);
        cell.appendChild(el('div', 'ghg-cl', c.label));
        ledgerBox.appendChild(cell);
        cells[c.key] = v;
      });
      stageBox.appendChild(ledgerBox);
      root.appendChild(stageBox);

      var cap = el('p', 'ghg-cap', '');
      root.appendChild(cap);

      var ctl = el('div', 'ghg-ctl');
      root.appendChild(ctl);

      var gSky = el('div', 'ghg-grp');
      gSky.appendChild(el('div', 'ghg-lab', 'Greenhouse gas in the air'));
      var skyRow = el('div', 'ghg-row');
      gSky.appendChild(skyRow);
      ctl.appendChild(gSky);

      var nav = el('div', 'ghg-nav');
      var backBtn = el('button', 'ghg-btn', 'Back');
      backBtn.type = 'button';
      var nextBtn = el('button', 'ghg-btn ghg-primary', 'Next');
      nextBtn.type = 'button';
      var stepOut = el('span', 'ghg-count', '');
      nav.appendChild(backBtn);
      nav.appendChild(nextBtn);
      nav.appendChild(stepOut);
      ctl.appendChild(nav);

      var sr = el('p', 'ghg-sr', '');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* --- sky buttons: the one real variable ----------------------------- */
      var skyBtns = {};
      SKY_ORDER.forEach(function (k) {
        var b = el('button', 'ghg-opt', SKIES[k].label);
        b.type = 'button';
        b.setAttribute('aria-pressed', k === S.skyKey ? 'true' : 'false');
        b.addEventListener('click', function () {
          if (S.skyKey === k) return;
          S.skyKey = k;
          S.seen[k] = true;
          buildRound();
          paintSky();
          /* rebuild at the step we are on; replay the return leg so the
             change in the number coming back down is something you SEE */
          var t = STEPS[S.step];
          if (t.pb > 0 && !reduced) {
            applyAll(t.pa, 0);
            cur = { a: t.pa, b: 0 };
            animateTo(t.pa, t.pb, false);
          } else {
            applyAll(t.pa, t.pb);
            cur = { a: t.pa, b: t.pb };
          }
          paintStep();
        });
        skyRow.appendChild(b);
        skyBtns[k] = b;
      });

      /* --- the model: build one round of twelve packets -------------------- */
      function buildRound() {
        var sky = SKIES[S.skyKey];
        var r = rng(Math.floor(Math.random() * 1e9));
        var absorbed = sky.absorbed;

        var idx = [];
        for (var i = 0; i < PACKETS; i++) idx.push(i);
        shuffle(idx, r);
        var absorbedSet = {};
        for (var a = 0; a < absorbed; a++) absorbedSet[idx[a]] = true;

        /* re-emission direction: a molecule cannot choose, and over the whole
           set about half of what is absorbed heads back down */
        var dirs = [];
        for (var d = 0; d < absorbed; d++) dirs.push(d < absorbed / 2 ? 'down' : 'up');
        shuffle(dirs, r);

        var packets = [], di = 0;
        for (var p = 0; p < PACKETS; p++) {
          if (absorbedSet[p]) packets.push({ absorbed: true, dir: dirs[di++] });
          else packets.push({ absorbed: false, dir: 'up' });
        }

        /* counted off the array, never authored */
        var nAbs = 0, nDown = 0;
        packets.forEach(function (q) {
          if (q.absorbed) nAbs++;
          if (q.absorbed && q.dir === 'down') nDown++;
        });
        S.round = {
          absorbed: nAbs, free: PACKETS - nAbs, down: nDown, space: PACKETS - nDown,
          note: sky.note, packets: packets
        };
        S.sceneId++;
        drawStage();
      }

      /* --- stage ----------------------------------------------------------- */
      function stageWidth() {
        var w = Math.round(svgWrap.clientWidth || svgWrap.getBoundingClientRect().width);
        return Math.max(240, w || 300);
      }
      function isWide() {
        var w = root.clientWidth || root.getBoundingClientRect().width;
        return w >= 520;
      }

      function buildGeometry() {
        var W = stageWidth();
        var H = isWide() ? 176 : 156;
        var padX = 12;
        var toaY = 30;
        var groundTop = H - 22;
        var bandTop = toaY + 12;
        var bandBot = groundTop - 24;
        var sky = SKIES[S.skyKey];
        var r = rng(S.sceneId * 7919 + 13);

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

        var span = (W - 2 * padX) / PACKETS;
        var out = [];
        for (var p = 0; p < PACKETS; p++) {
          var px = padX + (p + 0.5) * span;
          var rec = S.round.packets[p];
          var f = { x0: px, y0: groundTop - 5, absorbed: rec.absorbed, dir: rec.dir, mol: null };
          if (!rec.absorbed) {
            /* one leg: straight out through the atmosphere */
            f.ptsA = [[px, groundTop - 5], [clamp(px + (r() - 0.5) * 90, 8, W - 8), 7]];
            f.ptsB = null;
          } else {
            var best = -1, bestD = 1e9;
            for (var m = 0; m < mol.length; m++) {
              if (mol[m].used) continue;
              var dd = Math.abs(mol[m].x - px) + Math.abs(mol[m].y - bandTop) * 0.25;
              if (dd < bestD) { bestD = dd; best = m; }
            }
            if (best < 0) best = 0;
            mol[best].used = true;
            f.mol = mol[best];
            var mx = mol[best].x, my = mol[best].y;
            var ex, ey, spread;
            if (rec.dir === 'up') {
              ey = 7;
              spread = (my - ey) * 0.85;
            } else {
              ey = groundTop - 3;
              spread = (ey - my) * 0.85;
            }
            ex = clamp(mx + (r() - 0.5) * 2 * spread, 6, W - 6);
            if (Math.abs(ex - mx) < 10) ex = clamp(mx + (ex >= mx ? 12 : -12), 6, W - 6);
            /* leg A up to the molecule, leg B away from it */
            f.ptsA = [[px, groundTop - 5], [mx, my]];
            f.ptsB = [[mx, my], [ex, ey]];
          }
          out.push(f);
        }
        return { W: W, H: H, padX: padX, toaY: toaY, groundTop: groundTop, mol: mol, flights: out };
      }

      function pathFor(pts, colour, width) {
        var d = 'M' + pts[0][0] + ',' + pts[0][1];
        for (var k = 1; k < pts.length; k++) d += ' L' + pts[k][0] + ',' + pts[k][1];
        var path = svg('path', {
          d: d, fill: 'none', stroke: colour, 'stroke-width': width,
          'stroke-linecap': 'round', opacity: colour === accent ? 0.95 : 0.6
        });
        var len = 0;
        try { len = path.getTotalLength(); } catch (e) { len = 0; }
        len = len || 1;
        path.setAttribute('stroke-dasharray', len);
        path.setAttribute('stroke-dashoffset', len);
        return { path: path, len: len };
      }

      function drawStage() {
        geo = buildGeometry();
        var W = geo.W, H = geo.H;
        svgWrap.innerHTML = '';
        svgRoot = svg('svg', {
          viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, role: 'img',
          'aria-label': 'Side view of the atmosphere: the warm surface below, greenhouse gas molecules above it, space at the top.'
        });

        var defs = svg('defs', {});
        var mkOut = svg('marker', { id: uid + '-out', markerWidth: '6', markerHeight: '6', refX: '3.4', refY: '2', orient: 'auto' });
        mkOut.appendChild(svg('path', { d: 'M0,0 L4,2 L0,4 z', fill: '#9c948a' }));
        var mkBack = svg('marker', { id: uid + '-back', markerWidth: '6', markerHeight: '6', refX: '3.4', refY: '2', orient: 'auto' });
        mkBack.appendChild(svg('path', { d: 'M0,0 L4,2 L0,4 z', fill: accent }));
        defs.appendChild(mkOut); defs.appendChild(mkBack);
        svgRoot.appendChild(defs);

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

        var gMol = svg('g', {});
        geo.mol.forEach(function (m) {
          m.node = svg('circle', { cx: m.x, cy: m.y, r: 3, fill: '#b8afa1' });
          gMol.appendChild(m.node);
        });
        svgRoot.appendChild(gMol);

        /* legend: both kinds of dot are named, at every step */
        var legend = svg('g', {});
        function key(x, y, text, fill, halo) {
          var t = svg('text', {
            x: x, y: y, fill: fill, 'font-size': '11', 'text-anchor': 'end',
            'font-family': 'Inter,system-ui,sans-serif',
            stroke: halo, 'stroke-width': '3', 'paint-order': 'stroke', 'stroke-linejoin': 'round'
          });
          t.textContent = text;
          legend.appendChild(t);
          return t;
        }
        var kGas = key(W - 10, geo.toaY + 13, 'greenhouse gas molecules', '#6f685d', '#f2ede4');
        var kPk = key(W - 10, H - 7, '12 infrared packets', '#584f42', '#c9bfae');
        svgRoot.appendChild(legend);
        [[kGas, '#b8afa1', geo.toaY + 9], [kPk, '#2d2a26', H - 11]].forEach(function (pair) {
          var wid = 130;
          try { wid = pair[0].getComputedTextLength() || wid; } catch (e) { /* estimate */ }
          legend.insertBefore(svg('circle', {
            cx: clamp(W - 14 - wid - 4, 8, W - 8), cy: pair[2], r: 3, fill: pair[1]
          }), pair[0]);
        });

        /* flight paths, drawn on as the packets fly */
        flights = [];
        var gPath = svg('g', {});
        var gDot = svg('g', {});
        geo.flights.forEach(function (f) {
          var back = f.absorbed && f.dir === 'down';
          var legA = pathFor(f.ptsA, '#9c948a', 1.3);
          legA.back = false;
          gPath.appendChild(legA.path);
          var legB = null;
          if (f.ptsB) {
            legB = pathFor(f.ptsB, back ? accent : '#9c948a', back ? 1.9 : 1.3);
            legB.back = back;
            gPath.appendChild(legB.path);
          }
          var dot = svg('circle', { cx: f.x0, cy: f.y0, r: 3.4, fill: '#2d2a26' });
          gDot.appendChild(dot);
          flights.push({ a: legA, b: legB, dot: dot, absorbed: f.absorbed, dir: f.dir, mol: f.mol });
        });
        svgRoot.appendChild(gPath);
        svgRoot.appendChild(gDot);
        svgWrap.appendChild(svgRoot);
      }

      /* --- moving the packets ---------------------------------------------- */
      function setLeg(leg, u) {
        if (!leg) return;
        leg.path.setAttribute('stroke-dashoffset', leg.len * (1 - u));
        if (u > 0.995) leg.path.setAttribute('marker-end', 'url(#' + uid + (leg.back ? '-back' : '-out') + ')');
        else leg.path.removeAttribute('marker-end');
      }
      function setDot(fl, a, b) {
        var onB = fl.b && b > 0;
        var leg = onB ? fl.b : fl.a;
        var u = onB ? b : a;
        var pt = null;
        try { pt = leg.path.getPointAtLength(leg.len * u); } catch (e) { pt = null; }
        if (!pt) return;
        fl.dot.setAttribute('cx', pt.x);
        fl.dot.setAttribute('cy', pt.y);
        fl.dot.setAttribute('fill', (onB && fl.dir === 'down') ? accent : '#2d2a26');
        /* a packet that has left the top of the frame is gone into space */
        fl.dot.setAttribute('opacity', (pt.y <= 8 && u > 0.98) ? 0 : 1);
      }
      function setMolecules(lit, pulse) {
        if (!geo) return;
        geo.flights.forEach(function (f, i) {
          if (!f.absorbed || !f.mol || !f.mol.node) return;
          var r = lit ? 4.6 + (pulse || 0) * 2.6 : 3;
          f.mol.node.setAttribute('r', r);
          f.mol.node.setAttribute('fill', lit ? accent : '#b8afa1');
        });
      }
      function applyAll(a, b, pulse, lit) {
        flights.forEach(function (fl) {
          setLeg(fl.a, a);
          setLeg(fl.b, fl.b ? b : 0);
          setDot(fl, a, b);
        });
        setMolecules(lit == null ? STEPS[S.step].mol : lit, pulse || 0);
      }
      function animateTo(toA, toB, pulse) {
        var fromA = cur.a, fromB = cur.b;
        var token = ++animToken, t0 = 0;
        var total = DUR + STAGGER * (flights.length - 1);
        function frame(ts) {
          if (token !== animToken) return;
          if (!t0) t0 = ts;
          var t = ts - t0;
          flights.forEach(function (fl, i) {
            var u = ease(clamp((t - i * STAGGER) / DUR, 0, 1));
            var a = fromA + (toA - fromA) * u;
            var b = fromB + (toB - fromB) * u;
            setLeg(fl.a, a);
            setLeg(fl.b, fl.b ? b : 0);
            setDot(fl, a, b);
          });
          if (pulse) setMolecules(true, Math.sin(Math.PI * clamp(t / total, 0, 1)));
          if (t < total) { window.requestAnimationFrame(frame); return; }
          cur = { a: toA, b: toB };
          applyAll(toA, toB, 0);          /* land exactly on the target */
        }
        window.requestAnimationFrame(frame);
      }

      /* --- the ledger, counted off the model ------------------------------- */
      function tally() {
        var R = S.round;
        if (S.step <= 0) return { air: PACKETS, down: 0, space: 0, trapped: 0 };
        if (S.step <= 2) return { air: R.absorbed, down: 0, space: R.free, trapped: 0 };
        return { air: 0, down: R.down, space: R.space, trapped: 0 };
      }

      /* --- painting --------------------------------------------------------- */
      function paintSky() {
        SKY_ORDER.forEach(function (k) {
          skyBtns[k].setAttribute('aria-pressed', k === S.skyKey ? 'true' : 'false');
        });
      }
      function paintStep() {
        var R = S.round, t = tally();
        LEDGER.forEach(function (c) { cells[c.key].textContent = t[c.key]; });
        var others = [];
        SKY_ORDER.forEach(function (k) { if (k !== S.skyKey) others.push(SKIES[k].label); });
        cap.textContent = STEPS[S.step].text({
          absorbed: R.absorbed, free: R.free, down: R.down, space: R.space, note: R.note,
          others: others.join(' and ')
        });
        stepOut.textContent = 'Step ' + (S.step + 1) + ' of ' + STEPS.length;
        backBtn.disabled = S.step === 0;
        nextBtn.textContent = S.step === STEPS.length - 1 ? 'Start again' : 'Next';
        sr.textContent = 'Step ' + (S.step + 1) + ' of ' + STEPS.length + '. ' + cap.textContent +
          ' In the air ' + t.air + ', back down ' + t.down + ', out to space ' + t.space +
          ', trapped ' + t.trapped + '.';
        pushState();
      }

      function goToStep(i, animateIt) {
        var wrapped = false;
        if (i >= STEPS.length) { i = 0; wrapped = true; }
        i = clamp(i, 0, STEPS.length - 1);
        var wasMol = STEPS[S.step].mol;
        S.step = i;
        if (i > S.maxStep) S.maxStep = i;
        var t = STEPS[i];
        if (wrapped) buildRound();            /* a fresh scatter for the replay */
        if (reduced || !window.requestAnimationFrame || wrapped) {
          applyAll(t.pa, t.pb, 0);
          cur = { a: t.pa, b: t.pb };
        } else {
          animateTo(t.pa, t.pb, t.mol && !wasMol);
        }
        paintStep();
      }

      /* --- state for the gate ----------------------------------------------- */
      function pushState() {
        var t = tally(), seen = 0;
        SKY_ORDER.forEach(function (k) { if (S.seen[k]) seen++; });
        root.dataset.svState = JSON.stringify({
          step: S.step + 1,
          totalSteps: STEPS.length,
          skiesViewed: seen,
          completed: S.maxStep >= STEPS.length - 1,
          sky: S.skyKey,
          backDown: t.down,
          outToSpace: t.space,
          trapped: t.trapped
        });
      }

      nextBtn.addEventListener('click', function () { goToStep(S.step + 1, true); });
      backBtn.addEventListener('click', function () { goToStep(S.step - 1, true); });
      root.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') { goToStep(S.step + 1, true); e.preventDefault(); }
        else if (e.key === 'ArrowLeft') { goToStep(S.step - 1, true); e.preventDefault(); }
      });

      function fitWidth() { root.classList.toggle('ghg-wide', isWide()); }
      fitWidth();
      buildRound();
      paintSky();
      goToStep(0, false);

      if (window.ResizeObserver) {
        var ro = new window.ResizeObserver(function () {
          var was = root.classList.contains('ghg-wide');
          fitWidth();
          if (was !== root.classList.contains('ghg-wide')) {
            animToken++;
            drawStage();
            var t = STEPS[S.step];
            applyAll(t.pa, t.pb, 0);
            cur = { a: t.pa, b: t.pb };
          }
        });
        try { ro.observe(root); } catch (e) { /* no observer, no harm */ }
      }
    }
  };
}());
