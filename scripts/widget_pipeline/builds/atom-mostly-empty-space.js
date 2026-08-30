/* ============================================================
   atom-mostly-empty-space

   Three benches, one beam. The student is handed a model of the atom and
   must predict what the detector records when 20 000 alpha particles are
   fired at gold foil. The solid-ball prediction ("nearly all stopped") is
   committable on every bench, including the nuclear one - which is the
   whole point. The scale lie is named on the diagram at the reveal.

   Self-contained: no imports, no network, no storage.
   ============================================================ */
(function () {
  'use strict';

  var FIRED = 20000;
  var BACK_IN = 10000;    /* about 1 in 10 000 come straight back */
  var DEFLECT_IN = 2000;  /* about 1 in 2 000 are deflected sharply */
  var RATIO = 10000;      /* atom radius : nucleus radius */
  var NUC_DRAW = 0.13;    /* nucleus dot radius, as a fraction of the drawn atom */

  var BENCHES = [
    { key: 'solid', name: 'Solid spheres',
      desc: 'Atoms packed solid, with no gaps: the everyday picture.' },
    { key: 'pudding', name: 'Plum pudding',
      desc: 'Positive charge spread evenly through the whole atom.' },
    { key: 'nuclear', name: 'Nuclear',
      desc: 'Positive charge and nearly all the mass in a tiny centre.' }
  ];

  var OPTIONS = [
    { id: 'A', label: 'Nearly all stopped by the foil' },
    { id: 'B', label: 'All pass through, bending only slightly' },
    { id: 'C', label: 'Nearly all pass through; a few bounce back' },
    { id: 'D', label: 'About half pass through, half bounce back' }
  ];

  /* --- the model. Everything the widget claims is computed from here. --- */

  function outcome(key) {
    if (key === 'solid') return { stopped: FIRED, through: 0, deflected: 0, back: 0 };
    if (key === 'pudding') return { stopped: 0, through: FIRED, deflected: 0, back: 0 };
    var back = Math.round(FIRED / BACK_IN);
    var defl = Math.round(FIRED / DEFLECT_IN);
    return { stopped: 0, through: FIRED - back - defl, deflected: defl, back: back };
  }

  /* The right answer is read off the outcome, never hand-typed beside it. */
  function keyFor(o) {
    if (o.stopped > o.through) return 'A';
    if (o.back === 0) return 'B';
    if (o.back * 10 < o.through) return 'C';
    return 'D';
  }

  function grouped(v) {
    return String(v).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  }

  function readoutFor(o) {
    if (o.stopped > 0) {
      return grouped(o.through) + ' through · ' + grouped(o.deflected) +
             ' deflected · ' + grouped(o.stopped) + ' stopped';
    }
    return grouped(o.through) + ' through · ' + grouped(o.deflected) +
           ' deflected · ' + grouped(o.back) + ' came back';
  }

  var FEEDBACK = {
    solid: {
      A: 'Right — a solid, gapless foil would stop them. The real beam did the opposite: almost every particle went straight through.',
      B: 'Not quite — you said all would pass through. Solid, gapless matter has no gaps: the beam would stop at the surface.',
      C: 'Not quite — you said nearly all would pass through. Solid, gapless matter leaves nothing for them to pass through.',
      D: 'Not quite — you said half would pass through. Solid, gapless matter has no gaps at all, so none would get through.'
    },
    pudding: {
      A: 'Not quite — you said the foil would stop them. Charge spread thinly pushes only weakly, so every alpha gets through.',
      B: 'Right — charge spread through the whole atom is far too weak to turn an alpha round. Yet a few really did come back.',
      C: 'Not quite — you said a few would bounce back. Spread-out charge is far too weak for that, so this model predicts none.',
      D: 'Not quite — you said half would bounce back. Spread-out charge deflects nothing sharply; the whole beam gets through.'
    },
    nuclear: {
      A: 'Not quite — you said the foil would stop them. It stopped none: a nuclear atom is almost all empty space.',
      B: 'Not quite — you said none would come back. 2 did, and only positive charge packed into a tiny nucleus could do that.',
      C: 'Right — 2 in 20 000 came back. Only a tiny, dense, positive nucleus can turn an alpha round; the rest is empty space.',
      D: 'Not quite — you said half would bounce back. Only 2 in 20 000 did: the nucleus is far too small to be hit often.'
    }
  };

  var OPENER = 'Alpha particles are positive and fast. Anything that turns one round must be positive and concentrated.';
  var MASTERED = 'Three in a row — you have it. An atom is mostly empty space, and only a nucleus 10 000 times smaller can send an alpha back.';

  var CSS = [
    '.svw-ae{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;position:relative}',
    '.svw-ae *{box-sizing:border-box}',
    '.svw-ae-kicker{margin:0 0 .16rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase}',
    '.svw-ae-title{margin:0 0 .3rem;font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.18}',
    '.svw-ae-frame{margin:0 0 .6rem;font-size:.84rem;line-height:1.42;color:#5b564e}',
    '.svw-ae-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem .6rem}',
    '.svw-ae-bench{margin:0 0 .3rem;font-size:.78rem;line-height:1.35;color:#5b564e}',
    '.svw-ae-bench b{color:#2d2a26;font-weight:700}',
    '.svw-ae-svg{display:block;width:100%}',
    '.svw-ae-read{margin:.3rem 0 0;font-size:.78rem;line-height:1.3;color:#5b564e;font-variant-numeric:tabular-nums;min-height:1.35em}',
    '.svw-ae-opts{display:grid;gap:.35rem;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));max-width:640px;margin:.6rem 0 0}',
    '.svw-ae-opt{display:flex;align-items:center;justify-content:space-between;gap:.4rem;width:100%;text-align:left;',
    'font-family:inherit;font-size:.82rem;font-weight:600;line-height:1.3;color:#2d2a26;background:#faf8f5;',
    'border:1px solid #ddd7cd;border-radius:10px;padding:.42rem .55rem;cursor:pointer}',
    '.svw-ae-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-ae-tag{font-size:.7rem;font-weight:600;color:#8d8880;white-space:nowrap}',
    '.svw-ae-opt[aria-pressed="true"] .svw-ae-tag{color:#cfc8bd}',
    '.svw-ae-opts.is-done .svw-ae-opt{background:#faf8f5;border-color:#e4ded4;color:#8d8880;cursor:default}',
    '.svw-ae-opts.is-done .svw-ae-opt .svw-ae-tag{color:#8d8880}',
    '.svw-ae-opts.is-done .svw-ae-opt.is-pick{color:#2d2a26;border-color:#2d2a26}',
    '.svw-ae-opts.is-done .svw-ae-opt.is-key{color:#2d2a26;border-color:#4f7d63;background:rgba(79,125,99,.10)}',
    '.svw-ae-commit{display:flex;align-items:center;gap:.55rem;margin:.55rem 0 0}',
    '.svw-ae-go{font-family:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;',
    'border-radius:10px;padding:.5rem .95rem;cursor:pointer}',
    '.svw-ae-go[disabled]{opacity:.38;cursor:default}',
    '.svw-ae-cap{margin:.55rem 0 0;font-size:.84rem;line-height:1.5;color:#2d2a26;min-height:4.5em}',
    '.svw-ae-run{display:block;margin-top:.22rem;font-size:.78rem;color:#8d8880}',
    '.svw-ae-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svw-ae-track{fill:none;stroke-linecap:round;stroke-linejoin:round}'
  ].join('');

  var SVGNS = 'http://www.w3.org/2000/svg';
  function svgEl(name, attrs) {
    var e = document.createElementNS(SVGNS, name);
    for (var k in attrs) if (attrs.hasOwnProperty(k)) e.setAttribute(k, attrs[k]);
    return e;
  }

  window.SVWidget = {
    meta: {
      id: 'atom-mostly-empty-space',
      title: 'The gold foil experiment',
      teaches: 'An atom is mostly empty space: a tiny, dense nucleus about 10 000 times smaller than the atom carries nearly all the mass.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var reduced = !!ctx.reducedMotion;

      var wrap = document.createElement('div');
      wrap.className = 'svw-ae';
      var style = document.createElement('style');
      style.textContent = CSS;
      wrap.appendChild(style);
      root.appendChild(wrap);

      var accent = (getComputedStyle(wrap).getPropertyValue('--accent') || '').trim() ||
                   ctx.accent || '#8a6a4f';

      /* ---------------- markup, built once ---------------- */

      var kicker = document.createElement('p');
      kicker.className = 'svw-ae-kicker';
      kicker.style.color = accent;
      kicker.textContent = 'Models of the atom';
      wrap.appendChild(kicker);

      var title = document.createElement('h3');
      title.className = 'svw-ae-title';
      title.textContent = 'The gold foil experiment';
      wrap.appendChild(title);

      var frame = document.createElement('p');
      frame.className = 'svw-ae-frame';
      frame.textContent = 'A beam of 20 000 alpha particles is fired at gold foil a few atoms thick. ' +
                          'Predict what the detector records for the model on the bench.';
      wrap.appendChild(frame);

      var stage = document.createElement('div');
      stage.className = 'svw-ae-stage';
      wrap.appendChild(stage);

      var bench = document.createElement('p');
      bench.className = 'svw-ae-bench';
      var benchName = document.createElement('b');
      var benchDesc = document.createTextNode('');
      bench.appendChild(benchName);
      bench.appendChild(benchDesc);
      stage.appendChild(bench);

      var svg = svgEl('svg', { 'class': 'svw-ae-svg', role: 'img' });
      var svgTitle = svgEl('title', {});
      svg.appendChild(svgTitle);
      stage.appendChild(svg);

      var gFoil = svgEl('g', {});
      var gAtoms = svgEl('g', {});
      var gTracks = svgEl('g', {});
      var gFurniture = svgEl('g', {});
      svg.appendChild(gFurniture);
      svg.appendChild(gFoil);
      svg.appendChild(gTracks);
      svg.appendChild(gAtoms);

      /* fixed pools, created once and mutated */
      var TRACK_MAX = 16;
      var trackEls = [];
      for (var t = 0; t < TRACK_MAX; t++) {
        var p = svgEl('path', { 'class': 'svw-ae-track', d: 'M0,0', opacity: '0' });
        gTracks.appendChild(p);
        trackEls.push(p);
      }

      var foilBand = svgEl('rect', { rx: '3' });
      gFoil.appendChild(foilBand);

      var atomEls = [];
      for (var a = 0; a < 3; a++) {
        var g = svgEl('g', {});
        var ring = svgEl('circle', {});
        var nuc = svgEl('circle', {});
        g.appendChild(ring);
        g.appendChild(nuc);
        var dots = [];
        for (var d = 0; d < 4; d++) {
          var dot = svgEl('circle', { r: '1.7' });
          g.appendChild(dot);
          dots.push(dot);
        }
        gAtoms.appendChild(g);
        atomEls.push({ ring: ring, nuc: nuc, dots: dots });
      }

      var srcBox = svgEl('rect', { rx: '2' });
      var detBar = svgEl('rect', { rx: '2.5' });
      var lblSrc = svgEl('text', { 'text-anchor': 'start' });
      var lblFoil = svgEl('text', { 'text-anchor': 'middle' });
      var lblDet = svgEl('text', { 'text-anchor': 'end' });
      var lblScale = svgEl('text', { 'text-anchor': 'middle', opacity: '0' });
      [srcBox, detBar, lblSrc, lblFoil, lblDet, lblScale].forEach(function (e) { gFurniture.appendChild(e); });
      lblSrc.textContent = 'α source';
      lblFoil.textContent = 'gold foil';
      lblDet.textContent = 'detector';

      var readout = document.createElement('p');
      readout.className = 'svw-ae-read';
      stage.appendChild(readout);

      var opts = document.createElement('div');
      opts.className = 'svw-ae-opts';
      opts.setAttribute('role', 'group');
      opts.setAttribute('aria-label', 'Predict the detector result');
      wrap.appendChild(opts);

      var optEls = OPTIONS.map(function (o) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'svw-ae-opt';
        b.setAttribute('aria-pressed', 'false');
        var lab = document.createElement('span');
        lab.textContent = o.label;
        var tag = document.createElement('span');
        tag.className = 'svw-ae-tag';
        b.appendChild(lab);
        b.appendChild(tag);
        b.addEventListener('click', function () { pick(o.id); });
        opts.appendChild(b);
        return { id: o.id, el: b, tag: tag };
      });

      var commit = document.createElement('div');
      commit.className = 'svw-ae-commit';
      var goBtn = document.createElement('button');
      goBtn.type = 'button';
      goBtn.className = 'svw-ae-go';
      goBtn.textContent = 'Run the experiment';
      goBtn.disabled = true;
      goBtn.addEventListener('click', onGo);
      commit.appendChild(goBtn);
      wrap.appendChild(commit);

      var cap = document.createElement('p');
      cap.className = 'svw-ae-cap';
      var capMsg = document.createElement('span');
      var capRun = document.createElement('span');
      capRun.className = 'svw-ae-run';
      cap.appendChild(capMsg);
      cap.appendChild(capRun);
      wrap.appendChild(cap);

      var sr = document.createElement('p');
      sr.className = 'svw-ae-sr';
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      /* ---------------- state ---------------- */

      var st = {
        benchIndex: 0,
        picked: null,
        revealed: false,
        streak: 0,
        mastered: false,
        attempted: 0
      };
      var geo = null;

      function currentBench() { return BENCHES[st.benchIndex]; }

      /* ---------------- geometry + drawing ---------------- */

      function measure() {
        var W = Math.round(svg.getBoundingClientRect().width) || 300;
        var H = Math.round(Math.max(106, Math.min(130, W * 0.30)));
        var r = Math.max(10, Math.min(17, (H - 38) / 6.2));
        var labelY = H - 19;
        var cy0 = (H - 26) / 2 + 2;
        return {
          W: W, H: H, r: r, labelY: labelY, cy0: cy0,
          srcX: 24, foilX: Math.round(W * 0.45), detX: W - 20,
          font: Math.max(10.6, Math.min(12, W / 26))
        };
      }

      function beamYs(g) {
        var span = g.r * 2.6, ys = [];
        for (var i = 0; i < 11; i++) ys.push(g.cy0 - span + (2 * span) * (i / 10));
        return ys;
      }

      function trackPaths(key, g) {
        var ys = beamYs(g), out = [];
        var x0 = g.srcX + 6, face = g.foilX - g.r - 4;
        var top = 6, bot = g.labelY - 16;
        if (key === 'solid') {
          ys.forEach(function (y) {
            out.push({ d: 'M' + x0 + ',' + y.toFixed(1) + 'L' + face + ',' + y.toFixed(1), kind: 'through' });
          });
          [1, 5, 9].forEach(function (i) {
            out.push({ d: 'M' + face + ',' + ys[i].toFixed(1) + 'L' + (x0 + 28) + ',' + (ys[i] - 13).toFixed(1), kind: 'back' });
          });
        } else if (key === 'pudding') {
          ys.forEach(function (y, i) {
            var kink = (i % 2 ? 1.8 : -1.8);
            out.push({
              d: 'M' + x0 + ',' + y.toFixed(1) + 'L' + g.foilX + ',' + y.toFixed(1) +
                 'L' + g.detX + ',' + (y + kink).toFixed(1), kind: 'through'
            });
          });
        } else {
          ys.forEach(function (y, i) {
            if (i === 4 || i === 5 || i === 6) return;
            out.push({ d: 'M' + x0 + ',' + y.toFixed(1) + 'L' + g.detX + ',' + y.toFixed(1), kind: 'through' });
          });
          out.push({
            d: 'M' + x0 + ',' + ys[4].toFixed(1) + 'L' + g.foilX + ',' + ys[4].toFixed(1) +
               'L' + g.detX + ',' + top.toFixed(1), kind: 'defl'
          });
          out.push({
            d: 'M' + x0 + ',' + ys[6].toFixed(1) + 'L' + g.foilX + ',' + ys[6].toFixed(1) +
               'L' + g.detX + ',' + bot.toFixed(1), kind: 'defl'
          });
          out.push({
            d: 'M' + x0 + ',' + ys[5].toFixed(1) + 'L' + (g.foilX - 1) + ',' + ys[5].toFixed(1) +
               'L' + (x0 + 22) + ',' + (ys[5] - g.r * 2.5).toFixed(1), kind: 'back'
          });
        }
        return out;
      }

      function draw() {
        geo = measure();
        var g = geo, key = currentBench().key;
        svg.setAttribute('viewBox', '0 0 ' + g.W + ' ' + g.H);
        svg.style.height = g.H + 'px';
        svgTitle.textContent = currentBench().name + ' model: alpha beam, gold foil and detector.';

        /* furniture */
        srcBox.setAttribute('x', g.srcX - 15); srcBox.setAttribute('y', g.cy0 - 11);
        srcBox.setAttribute('width', 17); srcBox.setAttribute('height', 22);
        srcBox.setAttribute('fill', '#2d2a26');
        detBar.setAttribute('x', g.detX); detBar.setAttribute('y', 6);
        detBar.setAttribute('width', 5); detBar.setAttribute('height', Math.max(20, g.labelY - 14));
        detBar.setAttribute('fill', '#ddd7cd');
        [lblSrc, lblFoil, lblDet].forEach(function (l) {
          l.setAttribute('y', g.labelY);
          l.setAttribute('font-size', g.font);
          l.setAttribute('fill', '#8d8880');
          l.setAttribute('font-family', 'Inter,system-ui,sans-serif');
        });
        lblSrc.setAttribute('x', 1);
        lblFoil.setAttribute('x', g.foilX);
        lblDet.setAttribute('x', g.W - 1);
        lblScale.setAttribute('x', g.W / 2);
        lblScale.setAttribute('y', g.H - 4);
        lblScale.setAttribute('font-size', Math.max(10.6, g.font - 0.6));
        lblScale.setAttribute('fill', accent);
        lblScale.setAttribute('font-family', 'Inter,system-ui,sans-serif');
        lblScale.textContent = 'nucleus drawn ' + grouped(Math.round(NUC_DRAW * RATIO)) +
                               '× too big — to scale it vanishes';
        lblScale.setAttribute('opacity',
          (key === 'nuclear' && st.revealed) ? '1' : '0');

        /* foil */
        var bandHalf = 3 * g.r + 2;
        foilBand.setAttribute('x', g.foilX - g.r - 4);
        foilBand.setAttribute('width', g.r * 2 + 8);
        foilBand.setAttribute('y', (g.cy0 - bandHalf).toFixed(1));
        foilBand.setAttribute('height', (2 * bandHalf).toFixed(1));
        foilBand.setAttribute('fill', key === 'solid' ? 'rgba(45,42,38,.10)' : accent + '12');
        foilBand.setAttribute('stroke', accent + '33');

        /* atoms */
        var cys = [g.cy0 - 2 * g.r, g.cy0, g.cy0 + 2 * g.r];
        atomEls.forEach(function (A, i) {
          var cy = cys[i];
          A.ring.setAttribute('cx', g.foilX); A.ring.setAttribute('cy', cy);
          A.ring.setAttribute('r', g.r);
          if (key === 'solid') {
            A.ring.setAttribute('fill', 'rgba(45,42,38,.72)');
            A.ring.setAttribute('stroke', '#2d2a26');
            A.ring.setAttribute('stroke-dasharray', 'none');
          } else if (key === 'pudding') {
            A.ring.setAttribute('fill', accent + '3d');
            A.ring.setAttribute('stroke', accent);
            A.ring.setAttribute('stroke-dasharray', 'none');
          } else {
            A.ring.setAttribute('fill', 'rgba(255,255,255,.55)');
            A.ring.setAttribute('stroke', '#c9c2b6');
            A.ring.setAttribute('stroke-dasharray', '2 2.6');
          }
          A.ring.setAttribute('stroke-width', '1');

          A.nuc.setAttribute('cx', g.foilX); A.nuc.setAttribute('cy', cy);
          A.nuc.setAttribute('r', (g.r * NUC_DRAW).toFixed(2));
          A.nuc.setAttribute('fill', accent);
          A.nuc.setAttribute('opacity', key === 'nuclear' ? '1' : '0');

          A.dots.forEach(function (dot, j) {
            var ang = (Math.PI / 2) * j + (i * 0.4) + 0.6;
            var rad = key === 'pudding' ? g.r * 0.52 : g.r;
            dot.setAttribute('cx', (g.foilX + Math.cos(ang) * rad).toFixed(1));
            dot.setAttribute('cy', (cy + Math.sin(ang) * rad).toFixed(1));
            dot.setAttribute('r', key === 'nuclear' ? '1.2' : '1.7');
            dot.setAttribute('fill', key === 'nuclear' ? '#a39c92' : '#5b564e');
            dot.setAttribute('opacity', key === 'solid' ? '0' : '1');
          });
        });

        drawTracks();
      }

      function drawTracks() {
        var g = geo, key = currentBench().key;
        var paths = trackPaths(key, g);
        trackEls.forEach(function (el, i) {
          var spec = paths[i];
          if (!spec || !st.revealed) {
            el.setAttribute('opacity', '0');
            el.style.transition = 'none';
            el.setAttribute('stroke-dashoffset', '620');
            if (spec) el.setAttribute('d', spec.d);
            return;
          }
          el.setAttribute('d', spec.d);
          el.setAttribute('stroke', spec.kind === 'through' ? '#8d8880' : accent);
          el.setAttribute('stroke-width', spec.kind === 'through' ? '1.1' : '1.8');
          el.setAttribute('opacity', spec.kind === 'through' ? '0.6' : '1');
          el.setAttribute('stroke-dasharray', '620');
          if (reduced) {
            el.style.transition = 'none';
            el.setAttribute('stroke-dashoffset', '0');
          } else {
            el.style.transition = 'none';
            el.setAttribute('stroke-dashoffset', '620');
            /* force a style flush so the transition actually runs */
            void el.getBoundingClientRect().width;
            el.style.transition = 'stroke-dashoffset .55s linear ' + (i * 28) + 'ms';
            el.setAttribute('stroke-dashoffset', '0');
          }
        });
      }

      /* ---------------- interaction ---------------- */

      function pick(id) {
        if (st.revealed) return;
        st.picked = id;
        optEls.forEach(function (o) {
          o.el.setAttribute('aria-pressed', o.id === id ? 'true' : 'false');
        });
        goBtn.disabled = false;
        sync();
      }

      function onGo() {
        if (!st.revealed) {
          if (!st.picked) return;
          reveal();
        } else {
          nextBench();
        }
      }

      function reveal() {
        var b = currentBench();
        var o = outcome(b.key);
        var key = keyFor(o);
        var right = st.picked === key;

        var wasMastered = st.mastered;
        st.revealed = true;
        st.attempted += 1;
        st.streak = right ? st.streak + 1 : 0;
        if (st.streak >= 3) st.mastered = true;
        /* the mastery line is said once, on the round that earns it; every
           later round still gets its own diagnosis */
        var justMastered = st.mastered && !wasMastered;

        opts.classList.add('is-done');
        optEls.forEach(function (op) {
          op.el.setAttribute('aria-pressed', 'false');
          op.el.classList.toggle('is-pick', op.id === st.picked);
          op.el.classList.toggle('is-key', op.id === key);
          op.el.disabled = true;
          op.tag.textContent = op.id === st.picked ? 'yours'
                              : (op.id === key ? 'actual' : '');
        });

        readout.textContent = readoutFor(o);
        capMsg.textContent = justMastered ? MASTERED : FEEDBACK[b.key][st.picked];
        capRun.textContent = runNote(right);
        goBtn.textContent = st.mastered ? 'Another anyway' : 'Next model';
        sr.textContent = (right ? 'Correct. ' : 'Not correct. ') + readoutFor(o);

        draw();
        sync();
      }

      function runNote(right) {
        if (st.mastered) return '';
        if (!right) return 'Run back to 0 — three in a row finishes it.';
        if (st.streak === 1) return '1 right in a row — two more and you have it.';
        return '2 right in a row — one more and you have it.';
      }

      function nextBench() {
        st.benchIndex = (st.benchIndex + 1) % BENCHES.length;
        st.picked = null;
        st.revealed = false;
        opts.classList.remove('is-done');
        optEls.forEach(function (op) {
          op.el.disabled = false;
          op.el.classList.remove('is-pick', 'is-key');
          op.el.setAttribute('aria-pressed', 'false');
          op.tag.textContent = '';
        });
        goBtn.textContent = 'Run the experiment';
        goBtn.disabled = true;
        capMsg.textContent = OPENER;
        capRun.textContent = st.streak > 0 && !st.mastered
          ? (st.streak === 1 ? '1 right in a row — two more and you have it.'
                             : '2 right in a row — one more and you have it.')
          : '';
        setBenchText();
        draw();
        sync();
      }

      function setBenchText() {
        var b = currentBench();
        benchName.textContent = 'On the bench: ' + b.name + ' — ';
        bench.lastChild.nodeValue = b.desc;
      }

      function sync() {
        root.dataset.svState = JSON.stringify({
          bench: currentBench().key,
          picked: st.picked,
          revealed: st.revealed,
          streak: st.streak,
          mastered: st.mastered,
          attempted: st.attempted
        });
      }

      /* ---------------- first paint ---------------- */

      setBenchText();
      readout.textContent = 'Beam ready: 20 000 α · detector clear';
      capMsg.textContent = OPENER;
      capRun.textContent = '';
      draw();
      sync();

      if (typeof ResizeObserver === 'function') {
        var ro = new ResizeObserver(function () {
          var w = Math.round(svg.getBoundingClientRect().width);
          if (!geo || Math.abs(w - geo.W) > 1) draw();
        });
        ro.observe(stage);
      }
    }
  };
})();
