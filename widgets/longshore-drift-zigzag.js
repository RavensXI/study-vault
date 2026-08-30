/* longshore-drift-zigzag
   Predict a pebble's path along an angled-wave beach, then watch the real
   saw-tooth play out. Swash runs up the beach on the wave bearing; backwash
   drains straight down the slope under gravity; the net is drift along the
   coast in the direction the waves are travelling.

   Everything quantitative is derived: the drift direction comes from a
   compass model (sea bearing + wind bearing), and the per-wave gain comes
   from the swash run and the measured approach angle. Nothing is authored
   twice. */
(function () {
  'use strict';

  var BEARING = {
    'north': 0, 'north-east': 45, 'east': 90, 'south-east': 135,
    'south': 180, 'south-west': 225, 'west': 270, 'north-west': 315
  };
  var CARDINAL = { 0: 'North', 90: 'East', 180: 'South', 270: 'West' };

  /* Five beaches. `sea` is the compass direction the open water lies in,
     `wind` is the prevailing wind it blows FROM. `angle` is the measured
     wave approach angle at the shore (waves refract in the shallows, so
     this is smaller than the offshore bearing implies). `order` fixes the
     option order so the widget is reproducible under test. */
  var ROUNDS = [
    { sea: 'north', wind: 'north-west', angle: 30, swash: 6, waves: 8, order: [0, 1, 2, 3] },
    { sea: 'north', wind: 'north-east', angle: 35, swash: 7, waves: 6, order: [2, 0, 3, 1] },
    { sea: 'west', wind: 'south-west', angle: 20, swash: 7, waves: 10, order: [3, 2, 1, 0] },
    { sea: 'east', wind: 'south-east', angle: 45, swash: 6, waves: 6, order: [1, 3, 0, 2] },
    { sea: 'south', wind: 'south-west', angle: 25, swash: 7, waves: 8, order: [2, 3, 1, 0] }
  ];

  var KEYS = ['zig-right', 'zig-left', 'straight', 'inout'];

  /* stage geometry, in viewBox units */
  var VW = 360, VH = 118, SEA = 36, BACK = 100, U = 8; /* U = units per metre */

  function solve(r) {
    var seaB = BEARING[r.sea];
    var travel = (BEARING[r.wind] + 180) % 360;      /* waves travel TOWARDS this */
    var rel = ((travel - seaB) % 360 + 360) % 360;   /* 0 = straight out to sea */
    var along = Math.sin(rel * Math.PI / 180);       /* + => screen right */
    var dir = along > 0 ? 1 : -1;
    var th = r.angle * Math.PI / 180;
    var stepM = r.swash * Math.sin(th);              /* metres along shore per wave */
    var climbM = r.swash * Math.cos(th);             /* metres up the beach */
    return {
      dir: dir,
      seaName: r.sea,
      wind: r.wind,
      angle: r.angle,
      swash: r.swash,
      waves: r.waves,
      order: r.order,
      leftName: CARDINAL[(seaB + 270) % 360],
      rightName: CARDINAL[(seaB + 90) % 360],
      driftName: CARDINAL[(seaB + (dir > 0 ? 90 : 270)) % 360],
      otherName: CARDINAL[(seaB + (dir > 0 ? 270 : 90)) % 360],
      stepM: stepM,
      climbM: climbM,
      totalM: stepM * r.waves,
      correct: dir > 0 ? 'zig-right' : 'zig-left'
    };
  }

  function lower(s) { return s.toLowerCase(); }

  window.SVWidget = {
    meta: {
      id: 'longshore-drift-zigzag',
      title: 'Longshore drift: the pebble’s path',
      teaches: 'Swash carries sediment up the beach on the wave bearing, backwash drains straight back down under gravity, so each wave shifts the sediment along the coast in a zigzag.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var reduced = !!ctx.reducedMotion;

      var wrap = document.createElement('div');
      wrap.className = 'svw-lsd';
      root.innerHTML = '';
      root.appendChild(wrap);

      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
        ctx.accent || '#8a6a4f';

      var style = document.createElement('style');
      style.textContent = [
        '.svw-lsd{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
        '.svw-lsd *{box-sizing:border-box}',
        '.svw-lsd .lsd-col{max-width:560px;margin:0 auto}',
        '.svw-lsd .lsd-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px}',
        '.svw-lsd .lsd-kicker{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + '}',
        '.svw-lsd .lsd-streak{font-size:.7rem;color:#8d8880;font-variant-numeric:tabular-nums;text-align:right}',
        '.svw-lsd .lsd-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.18rem;font-weight:600;margin:.16rem 0 .28rem;line-height:1.25}',
        '.svw-lsd .lsd-frame{font-size:.84rem;line-height:1.45;color:#5b564e;margin:0 0 .68rem}',
        '.svw-lsd .lsd-stage{display:block;width:100%;max-width:440px;margin:0 auto .68rem;border:1px solid #e8e2d9;border-radius:12px}',
        '.svw-lsd .lsd-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:6px;margin:0 0 .68rem}',
        '.svw-lsd .lsd-opt{display:grid;grid-template-columns:44px 1fr 14px;align-items:center;gap:8px;',
        '  min-height:44px;padding:6px 8px;text-align:left;font:inherit;color:inherit;cursor:pointer;',
        '  background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px}',
        '.svw-lsd .lsd-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
        '.svw-lsd .lsd-opt.is-right{border-color:#4f7d63;box-shadow:inset 0 0 0 1px #4f7d63}',
        '.svw-lsd .lsd-opt:disabled{cursor:default}',
        '.svw-lsd .lsd-glyph{display:block;width:44px;height:auto}',
        '.svw-lsd .lsd-lab{font-size:.82rem;font-weight:600;line-height:1.3}',
        '.svw-lsd .lsd-mark{font-size:.82rem;font-weight:700;text-align:right;color:#8d8880}',
        '.svw-lsd .lsd-mark.ok{color:#4f7d63}',
        '.svw-lsd .lsd-opt[aria-pressed="true"] .lsd-mark{color:#fff}',
        '.svw-lsd .lsd-go{font:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;',
        '  background:#2d2a26;color:#fff;border:1px solid #2d2a26;cursor:pointer;margin:0 0 .68rem}',
        '.svw-lsd .lsd-go:disabled{background:#f0ece5;color:#8d8880;border-color:#e4ded3;cursor:default}',
        '.svw-lsd .lsd-cap{margin:0;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;',
        '  padding:10px;font-size:.82rem;line-height:1.45;min-height:98px}',
        '.svw-lsd .lsd-v{font-weight:700}',
        '.svw-lsd .lsd-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
      ].join('');
      wrap.appendChild(style);

      var col = document.createElement('div');
      col.className = 'lsd-col';
      wrap.appendChild(col);

      /* ---- header ---------------------------------------------------- */
      var head = document.createElement('div');
      head.className = 'lsd-head';
      var kicker = document.createElement('span');
      kicker.className = 'lsd-kicker';
      kicker.textContent = 'Coasts';
      var streakEl = document.createElement('span');
      streakEl.className = 'lsd-streak';
      head.appendChild(kicker);
      head.appendChild(streakEl);
      col.appendChild(head);

      var title = document.createElement('h3');
      title.className = 'lsd-title';
      title.textContent = 'Where does the pebble end up?';
      col.appendChild(title);

      var frame = document.createElement('p');
      frame.className = 'lsd-frame';
      col.appendChild(frame);

      /* ---- stage ------------------------------------------------------ */
      var NS = 'http://www.w3.org/2000/svg';
      function el(tag, attrs) {
        var n = document.createElementNS(NS, tag);
        for (var k in attrs) if (attrs.hasOwnProperty(k)) n.setAttribute(k, attrs[k]);
        return n;
      }
      var svg = el('svg', {
        'class': 'lsd-stage', viewBox: '0 0 ' + VW + ' ' + VH,
        role: 'img', preserveAspectRatio: 'xMidYMid meet'
      });
      var svgTitle = el('title', {});
      svg.appendChild(svgTitle);
      col.appendChild(svg);

      var defs = el('defs', {});
      var clip = el('clipPath', { id: 'lsd-seaclip' });
      clip.appendChild(el('rect', { x: 0, y: 0, width: VW, height: SEA }));
      defs.appendChild(clip);
      svg.appendChild(defs);

      svg.appendChild(el('rect', { x: 0, y: 0, width: VW, height: SEA, fill: '#dbe5e8' }));
      svg.appendChild(el('rect', { x: 0, y: SEA, width: VW, height: BACK - SEA, fill: '#f2e7d3' }));
      svg.appendChild(el('rect', { x: 0, y: BACK, width: VW, height: VH - BACK, fill: '#e8e6dd' }));

      var crests = el('g', { 'clip-path': 'url(#lsd-seaclip)', stroke: '#a7bfc4', 'stroke-width': 1.1, fill: 'none', opacity: .7 });
      svg.appendChild(crests);

      var arrow = el('g', { stroke: '#3f5559', 'stroke-width': 2.2, fill: '#3f5559' });
      svg.appendChild(arrow);

      svg.appendChild(el('line', { x1: 0, y1: SEA, x2: VW, y2: SEA, stroke: '#8fa7ac', 'stroke-width': 1.4 }));
      svg.appendChild(el('line', { x1: 0, y1: BACK, x2: VW, y2: BACK, stroke: '#d9d2c5', 'stroke-width': 1 }));

      var HALO = { 'paint-order': 'stroke', stroke: '#dbe5e8', 'stroke-width': 3.5, 'stroke-linejoin': 'round' };
      var seaLabel = el('text', { 'font-size': 12.5, fill: '#5b6f74', 'font-family': 'Inter,system-ui,sans-serif',
        'paint-order': HALO['paint-order'], stroke: HALO.stroke, 'stroke-width': HALO['stroke-width'], 'stroke-linejoin': HALO['stroke-linejoin'] });
      svg.appendChild(seaLabel);
      var waveLabel = el('text', { 'font-size': 12.5, fill: '#3f5559', 'font-weight': 600, 'font-family': 'Inter,system-ui,sans-serif',
        'paint-order': HALO['paint-order'], stroke: HALO.stroke, 'stroke-width': HALO['stroke-width'], 'stroke-linejoin': HALO['stroke-linejoin'] });
      svg.appendChild(waveLabel);
      var leftLabel = el('text', { x: 8, y: VH - 5, 'font-size': 13, fill: '#7d766c', 'text-anchor': 'start', 'font-family': 'Inter,system-ui,sans-serif' });
      var rightLabel = el('text', { x: VW - 8, y: VH - 5, 'font-size': 13, fill: '#7d766c', 'text-anchor': 'end', 'font-family': 'Inter,system-ui,sans-serif' });
      svg.appendChild(leftLabel);
      svg.appendChild(rightLabel);

      var ghost = el('path', { fill: 'none', stroke: '#a9a29a', 'stroke-width': 1.6, 'stroke-dasharray': '5 4', 'stroke-linejoin': 'round' });
      var ghostLabel = el('text', { 'font-size': 12.5, fill: '#8d8880', 'font-family': 'Inter,system-ui,sans-serif' });
      svg.appendChild(ghost);
      svg.appendChild(ghostLabel);

      var real = el('path', { fill: 'none', stroke: accent, 'stroke-width': 2.2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' });
      svg.appendChild(real);
      var heads = el('g', { fill: accent });
      svg.appendChild(heads);

      var measure = el('g', {});
      var mLine = el('line', { stroke: '#8d8880', 'stroke-width': 1 });
      var mA = el('line', { stroke: '#8d8880', 'stroke-width': 1 });
      var mB = el('line', { stroke: '#8d8880', 'stroke-width': 1 });
      var mText = el('text', { 'font-size': 12.5, fill: '#5b564e', 'text-anchor': 'middle', 'font-family': 'Inter,system-ui,sans-serif' });
      measure.appendChild(mLine); measure.appendChild(mA); measure.appendChild(mB); measure.appendChild(mText);
      svg.appendChild(measure);

      var pebbleLabel = el('text', { 'font-size': 12.5, fill: '#5b564e', 'text-anchor': 'middle', 'font-family': 'Inter,system-ui,sans-serif',
        'paint-order': 'stroke', stroke: '#dbe5e8', 'stroke-width': 3.5, 'stroke-linejoin': 'round' });
      pebbleLabel.textContent = 'pebble';
      svg.appendChild(pebbleLabel);
      var startDot = el('circle', { r: 3.4, fill: 'none', stroke: '#8d8880', 'stroke-width': 1.2 });
      var pebble = el('circle', { r: 4, fill: accent, stroke: '#fff', 'stroke-width': 1.2 });
      svg.appendChild(startDot);
      svg.appendChild(pebble);

      /* ---- options ---------------------------------------------------- */
      var opts = document.createElement('div');
      opts.className = 'lsd-opts';
      opts.setAttribute('role', 'group');
      opts.setAttribute('aria-label', 'Possible paths for the pebble');
      col.appendChild(opts);

      function glyphFor(key) {
        var g = el('svg', { 'class': 'lsd-glyph', viewBox: '0 0 52 30', 'aria-hidden': 'true' });
        g.appendChild(el('line', { x1: 2, y1: 8, x2: 50, y2: 8, stroke: 'currentColor', 'stroke-width': 1, opacity: .35 }));
        var d, i, x;
        if (key === 'zig-right' || key === 'zig-left') {
          d = '';
          for (i = 0; i < 3; i++) {
            x = key === 'zig-right' ? 8 + i * 11 : 44 - i * 11;
            var nx = key === 'zig-right' ? x + 11 : x - 11;
            d += (i === 0 ? 'M' + x + ' 8' : '') + 'L' + nx + ' 24L' + nx + ' 8';
          }
          g.appendChild(el('path', { d: d, fill: 'none', stroke: 'currentColor', 'stroke-width': 1.7, 'stroke-linejoin': 'round' }));
          g.appendChild(el('polygon', {
            points: key === 'zig-right' ? '42,3 50,8 42,13' : '10,3 2,8 10,13',
            fill: 'currentColor'
          }));
          g.appendChild(el('circle', {
            cx: key === 'zig-right' ? 8 : 44, cy: 8, r: 2.2, fill: 'currentColor'
          }));
        } else if (key === 'straight') {
          g.appendChild(el('line', { x1: 8, y1: 16, x2: 44, y2: 16, stroke: 'currentColor', 'stroke-width': 1.7 }));
          g.appendChild(el('polygon', { points: '44,16 37,12 37,20', fill: 'currentColor' }));
          g.appendChild(el('polygon', { points: '8,16 15,12 15,20', fill: 'currentColor' }));
        } else {
          g.appendChild(el('line', { x1: 26, y1: 6, x2: 26, y2: 26, stroke: 'currentColor', 'stroke-width': 1.7 }));
          g.appendChild(el('polygon', { points: '26,4 22,11 30,11', fill: 'currentColor' }));
          g.appendChild(el('polygon', { points: '26,28 22,21 30,21', fill: 'currentColor' }));
        }
        return g;
      }

      var optBtns = [];
      KEYS.forEach(function (key) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'lsd-opt';
        b.dataset.key = key;
        b.setAttribute('aria-pressed', 'false');
        b.appendChild(glyphFor(key));
        var lab = document.createElement('span');
        lab.className = 'lsd-lab';
        var mark = document.createElement('span');
        mark.className = 'lsd-mark';
        b.appendChild(lab);
        b.appendChild(mark);
        b._lab = lab; b._mark = mark;
        b.addEventListener('click', function () { pick(key); });
        optBtns.push(b);
      });

      var go = document.createElement('button');
      go.type = 'button';
      go.className = 'lsd-go';
      go.textContent = 'Check the path';
      go.disabled = true;
      col.appendChild(go);

      var cap = document.createElement('p');
      cap.className = 'lsd-cap';
      col.appendChild(cap);

      var sr = document.createElement('p');
      sr.className = 'lsd-sr';
      sr.setAttribute('aria-live', 'polite');
      col.appendChild(sr);

      /* ---- state ------------------------------------------------------- */
      var idx = 0, S = null, choice = null, revealed = false;
      var streak = 0, mastered = false, attempted = 0;
      var raf = 0;

      function say(verdict, rest) {
        cap.textContent = '';
        if (verdict) {
          var b = document.createElement('b');
          b.className = 'lsd-v';
          b.textContent = verdict + ' ';
          cap.appendChild(b);
        }
        cap.appendChild(document.createTextNode(rest));
        sr.textContent = (verdict ? verdict + ' ' : '') + rest;
      }

      function publish() {
        root.dataset.svState = JSON.stringify({
          round: idx + 1, choice: choice, revealed: revealed,
          streak: streak, mastered: mastered, attempted: attempted
        });
      }

      function pathFrom(x0, dir, waves) {
        var pts = [[x0, SEA]], x = x0, i;
        for (i = 0; i < waves; i++) {
          var nx = x + dir * S.stepM * U;
          if (nx < 14 || nx > VW - 14) break;
          pts.push([nx, SEA + S.climbM * U]);
          pts.push([nx, SEA]);
          x = nx;
        }
        return pts;
      }
      function dOf(pts) {
        return pts.map(function (p, i) {
          return (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1);
        }).join('');
      }

      function layout() {
        var dir = S.dir;
        var x0 = dir > 0 ? 78 : VW - 78;
        S.x0 = x0;

        svgTitle.textContent = 'A beach with the sea to the ' + S.seaName + '. Waves reach the shore at ' +
          S.angle + ' degrees, travelling towards the ' + lower(S.driftName) + '. A pebble rests on the waterline.';

        /* wave crests and the travel arrow, both at the measured approach angle */
        var th = S.angle * Math.PI / 180;
        var tx = dir * Math.sin(th), ty = Math.cos(th);       /* travel, screen */
        var cx = dir * Math.cos(th), cy = -Math.sin(th);      /* crest line, screen */
        crests.innerHTML = '';
        for (var i = -8; i <= 8; i++) {
          var px = VW / 2 + tx * 15 * i, py = SEA / 2 + ty * 15 * i;
          crests.appendChild(el('line', {
            x1: (px - cx * 300).toFixed(1), y1: (py - cy * 300).toFixed(1),
            x2: (px + cx * 300).toFixed(1), y2: (py + cy * 300).toFixed(1)
          }));
        }
        arrow.innerHTML = '';
        var hx = x0 - dir * 34, hy = SEA - 3;
        var ax = hx - tx * 24, ay = hy - ty * 24;
        arrow.appendChild(el('line', { x1: ax.toFixed(1), y1: ay.toFixed(1), x2: hx.toFixed(1), y2: hy.toFixed(1) }));
        arrow.appendChild(el('polygon', {
          points: [hx + ',' + hy,
            (hx - tx * 8 + cx * 3.6).toFixed(1) + ',' + (hy - ty * 8 + cy * 3.6).toFixed(1),
            (hx - tx * 8 - cx * 3.6).toFixed(1) + ',' + (hy - ty * 8 - cy * 3.6).toFixed(1)].join(' '),
          stroke: 'none'
        }));
        waveLabel.textContent = 'waves';
        waveLabel.setAttribute('x', Math.max(24, Math.min(VW - 24, ax + dir * 2)).toFixed(1));
        waveLabel.setAttribute('y', (ay - 5).toFixed(1));
        waveLabel.setAttribute('text-anchor', 'middle');

        seaLabel.textContent = 'Sea · to the ' + S.seaName;
        seaLabel.setAttribute('x', dir > 0 ? VW - 8 : 8);
        seaLabel.setAttribute('y', 14);
        seaLabel.setAttribute('text-anchor', dir > 0 ? 'end' : 'start');

        leftLabel.textContent = '◀ ' + S.leftName;
        rightLabel.textContent = S.rightName + ' ▶';

        pebbleLabel.setAttribute('x', x0); pebbleLabel.setAttribute('y', SEA - 7);
        startDot.setAttribute('cx', x0); startDot.setAttribute('cy', SEA);
        pebble.setAttribute('cx', x0); pebble.setAttribute('cy', SEA);

        real.setAttribute('d', ''); real.removeAttribute('stroke-dasharray'); real.removeAttribute('stroke-dashoffset');
        ghost.setAttribute('d', ''); ghostLabel.textContent = '';
        heads.innerHTML = '';
        measure.setAttribute('opacity', '0');
      }

      function newRound() {
        if (raf) { cancelAnimationFrame(raf); raf = 0; }
        S = solve(ROUNDS[idx % ROUNDS.length]);
        choice = null; revealed = false;
        frame.textContent = 'A ' + S.wind + ' wind drives waves onto this beach at an angle. Predict the path of one pebble over ' + S.waves + ' waves.';
        S.order.forEach(function (k, position) {
          var b = optBtns[k];
          opts.appendChild(b);
          b.disabled = false;
          b.setAttribute('aria-pressed', 'false');
          b._mark.textContent = '';
          b._mark.className = 'lsd-mark';
          b.classList.remove('is-right');
          b._lab.textContent =
            b.dataset.key === 'zig-right' ? 'Zigzag, drifting ' + lower(S.rightName) :
              b.dataset.key === 'zig-left' ? 'Zigzag, drifting ' + lower(S.leftName) :
                b.dataset.key === 'straight' ? 'Straight line along the beach' :
                  'Up and back to the same spot';
          void position;
        });
        layout();
        go.textContent = 'Check the path';
        go.disabled = true;
        streakEl.textContent = streak > 0 ? streak + ' right in a row' : (mastered ? 'you have it' : '');
        say('', 'Wave approach angle ' + S.angle + '° to the shoreline. Each wave washes about ' +
          S.swash + ' m up the beach before draining back.');
        publish();
      }

      function pick(key) {
        if (revealed) return;
        choice = key;
        optBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.key === key ? 'true' : 'false'); });
        go.disabled = false;
        var lab = optBtns.filter(function (b) { return b.dataset.key === key; })[0]._lab.textContent;
        say('', 'Chosen: ' + lower(lab.charAt(0)) + lab.slice(1) + '. Wave approach angle ' + S.angle +
          '°; each wave washes about ' + S.swash + ' m up the beach.');
        publish();
      }

      function drawGhost() {
        var pts;
        if (choice === 'straight') {
          var end = S.x0 + S.dir * Math.min(S.totalM * U, VW - 80);
          pts = [[S.x0, SEA + 7], [end, SEA + 7]];
        } else if (choice === 'inout') {
          pts = [[S.x0, SEA], [S.x0, SEA + S.climbM * U], [S.x0, SEA]];
        } else {
          pts = pathFrom(S.x0, -S.dir, S.waves);
        }
        ghost.setAttribute('d', dOf(pts));
        var last = pts[pts.length - 1];
        ghostLabel.textContent = 'your path';
        ghostLabel.setAttribute('x', choice === 'inout' ? (S.x0 - S.dir * 6).toFixed(1) : (last[0] + (last[0] > S.x0 ? 5 : -5)).toFixed(1));
        ghostLabel.setAttribute('y', choice === 'inout' ? (SEA + S.climbM * U * 0.55).toFixed(1) : (SEA + 20).toFixed(1));
        ghostLabel.setAttribute('text-anchor', choice === 'inout' ? (S.dir > 0 ? 'end' : 'start') : (last[0] > S.x0 ? 'start' : 'end'));
      }

      function drawHeads(pts) {
        heads.innerHTML = '';
        if (pts.length < 3) return;
        var th = S.angle * Math.PI / 180;
        var tx = S.dir * Math.sin(th), ty = Math.cos(th);
        var a = pts[1];
        heads.appendChild(el('polygon', {
          points: [a[0] + ',' + a[1],
            (a[0] - tx * 8 + ty * 3.4).toFixed(1) + ',' + (a[1] - ty * 8 - tx * 3.4).toFixed(1),
            (a[0] - tx * 8 - ty * 3.4).toFixed(1) + ',' + (a[1] - ty * 8 + tx * 3.4).toFixed(1)].join(' ')
        }));
        var b = pts[2];
        heads.appendChild(el('polygon', {
          points: [b[0] + ',' + b[1], (b[0] - 3.4) + ',' + (b[1] + 8), (b[0] + 3.4) + ',' + (b[1] + 8)].join(' ')
        }));
      }

      function commit() {
        if (revealed) { idx++; newRound(); return; }
        if (!choice) return;
        revealed = true;
        attempted++;
        var right = choice === S.correct;
        if (right) { streak++; if (streak >= 3) mastered = true; } else { streak = 0; }

        optBtns.forEach(function (b) {
          b.disabled = true;
          if (b.dataset.key === S.correct) {
            b.classList.add('is-right');
            b._mark.textContent = '✓';
            b._mark.className = 'lsd-mark ok';
          } else if (b.dataset.key === choice) {
            b._mark.textContent = '✕';
          }
        });

        var pts = pathFrom(S.x0, S.dir, S.waves);
        var step = S.stepM.toFixed(1), total = Math.round(S.totalM);
        var drift = lower(S.driftName), other = lower(S.otherName);

        if (right) {
          say('Right —', 'a zigzag drifting ' + drift + 'wards. Swash climbs the beach at the wave angle, backwash drains straight down, netting ' +
            step + ' m ' + drift + ' per wave: ' + total + ' m after ' + S.waves + ' waves.');
        } else if (choice === 'straight') {
          say('Not quite —', 'you chose a straight line. No current runs along the shore; water only rushes up the beach and drains back. The drift is the sum of angled trips.');
          drawGhost();
        } else if (choice === 'inout') {
          say('Not quite —', 'you chose up and back to one spot. That needs waves head-on. These arrive at ' + S.angle +
            '°, so every swash lands the pebble ' + step + ' m further ' + drift + '.');
          drawGhost();
        } else {
          say('Not quite —', 'you chose a zigzag drifting ' + other + 'wards. The saw-tooth is right, but swash follows the waves in, and these run in towards the ' + drift + '.');
          drawGhost();
        }
        if (mastered && right) {
          say('Three in a row —', 'you have it. Swash runs up the beach at the wave angle; backwash drains straight back under gravity. Groynes are built to interrupt that drift.');
        }

        streakEl.textContent = mastered ? 'you have it' : (streak > 0 ? streak + ' right in a row' : '');
        go.textContent = mastered ? 'Another anyway' : 'Next beach';
        go.disabled = false;

        var endX = pts[pts.length - 1][0];
        mLine.setAttribute('x1', S.x0); mLine.setAttribute('y1', BACK + 5);
        mLine.setAttribute('x2', endX); mLine.setAttribute('y2', BACK + 5);
        mA.setAttribute('x1', S.x0); mA.setAttribute('y1', BACK + 2); mA.setAttribute('x2', S.x0); mA.setAttribute('y2', BACK + 8);
        mB.setAttribute('x1', endX); mB.setAttribute('y1', BACK + 2); mB.setAttribute('x2', endX); mB.setAttribute('y2', BACK + 8);
        mText.setAttribute('x', ((S.x0 + endX) / 2).toFixed(1));
        mText.setAttribute('y', VH - 4);
        mText.textContent = total + ' m ' + drift;

        real.setAttribute('d', dOf(pts));
        publish();

        var len = real.getTotalLength ? real.getTotalLength() : 0;
        function finish() {
          real.removeAttribute('stroke-dasharray');
          real.removeAttribute('stroke-dashoffset');
          pebble.setAttribute('cx', endX); pebble.setAttribute('cy', SEA);
          drawHeads(pts);
          measure.setAttribute('opacity', '1');
        }
        if (reduced || !len) { finish(); return; }
        real.setAttribute('stroke-dasharray', len);
        real.setAttribute('stroke-dashoffset', len);
        var dur = Math.min(2200, S.waves * 240), t0 = 0;
        raf = requestAnimationFrame(function tick(now) {
          if (!wrap.isConnected) { raf = 0; return; }
          if (!t0) t0 = now;
          var t = Math.min(1, (now - t0) / dur);
          real.setAttribute('stroke-dashoffset', (len * (1 - t)).toFixed(1));
          var p = real.getPointAtLength(len * t);
          pebble.setAttribute('cx', p.x.toFixed(1)); pebble.setAttribute('cy', p.y.toFixed(1));
          if (t < 1) { raf = requestAnimationFrame(tick); } else { raf = 0; finish(); }
        });
      }

      go.addEventListener('click', commit);
      newRound();
    }
  };
})();
