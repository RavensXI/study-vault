/* moon-synchronous-rotation — StudyVault lesson widget
   The Moon spins once per orbit. That exact match is why the same face
   stays towards Earth. Everything on screen is computed from one model:
   an orbit angle and a rotation angle. */
(function () {
  'use strict';

  var META = {
    id: 'moon-synchronous-rotation',
    title: 'Spin, orbit and the face we see',
    teaches: 'The Moon rotates once per orbit (both about 27.3 days), so the same face stays towards Earth; a Moon that did not spin at all would turn every side towards us.'
  };

  /* ---------- the model ---------------------------------------------
     Angles are integer degrees, anticlockwise, measured at Earth.
     theta = where the Moon is on its orbit.
     phi   = the direction the marked crater points, in space:
     phi = (start + 180) + spin * (theta - start), so the crater begins
     pointing back at Earth. Every view and every answer comes from here. */

  function cosD(d) {
    var m = ((d % 360) + 360) % 360;
    if (m === 90 || m === 270) return 0;
    if (m === 0) return 1;
    if (m === 180) return -1;
    return Math.cos(m * Math.PI / 180);
  }
  function sinD(d) {
    var m = ((d % 360) + 360) % 360;
    if (m === 0 || m === 180) return 0;
    if (m === 90) return 1;
    if (m === 270) return -1;
    return Math.sin(m * Math.PI / 180);
  }
  function craterAngle(r, theta) { return (r.start + 180) + r.spin * (theta - r.start); }

  /* Which way the crater faces, relative to the Moon-to-Earth line. Every
     round uses multiples of 90 degrees, so this stays exact integer work. */
  function faceAt(r, theta) {
    var rel = ((Math.round(craterAngle(r, theta) - (theta + 180)) % 360) + 360) % 360;
    if (rel === 0) return 'at';
    if (rel === 180) return 'away';
    return 'side';
  }
  /* How much of the Earth-facing half is sunlit. Sunlight arrives from the
     left, so this depends only on where the Moon is, never on its spin. */
  function litAt(theta) {
    var t = ((Math.round(theta) % 360) + 360) % 360;
    if (t === 0) return 'all';
    if (t === 180) return 'none';
    return 'half';
  }

  var FACE_SAID = { at: 'facing Earth', away: 'facing away', side: 'side-on' };
  var FACE_IS = { at: 'facing Earth', away: 'facing away from Earth', side: 'side-on to Earth' };
  var LIT_SAID = { all: 'fully lit', half: 'half lit', none: 'not lit' };
  var SPIN_WORD = ['not spinning at all', 'spinning once per orbit', 'spinning twice per orbit'];
  var TRAVEL_WORD = { 90: 'a quarter of the way round', 180: 'half way round', 270: 'three quarters of the way round' };

  var MECH_FACE = [
    'With no spin the crater keeps pointing one way in space, so Earth sees every side in one orbit.',
    'One spin per orbit turns the Moon by exactly the angle the orbit carries it, so the same face stays towards us.',
    'Two spins per orbit is one turn too many, so the face pointed at us keeps sliding round.'
  ];
  var MECH_LIT = {
    all: 'Earth is between the Sun and the Moon, so the face we see is fully sunlit.',
    half: 'The Moon is off to one side of the Sun, so half the face we see is lit.',
    none: 'All the sunlight is on the side turned away — the far side is not a dark side.'
  };

  window.SVWidget = {
    meta: META,
    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || ctx.accent || '#8a6a4f';
      var calm = !!ctx.reducedMotion;

      /* ---------- style (every selector scoped to .svw-moon) ---------- */
      var css = [
        '.svw-moon{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45}',
        '.svw-moon *{box-sizing:border-box}',
        '.svw-moon .m-head{display:flex;align-items:baseline;justify-content:space-between;gap:.6rem}',
        '.svw-moon .m-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + '}',
        '.svw-moon .m-run{font-size:.7rem;color:#8d8880;font-variant-numeric:tabular-nums;white-space:nowrap}',
        '.svw-moon .m-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.18rem;margin:.1rem 0 .28rem;line-height:1.2}',
        '.svw-moon .m-frame{font-size:.82rem;color:#5b564e;margin:0 0 .45rem}',
        '.svw-moon .m-frame b{color:#2d2a26;font-weight:600}',
        '.svw-moon .m-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.35rem}',
        '.svw-moon .m-svgwrap{max-width:320px;margin:0 auto}',
        '.svw-moon .m-svgwrap svg{display:block;width:100%;height:auto}',
        '.svw-moon .m-grp{margin-top:.45rem}',
        '.svw-moon .m-lab{display:flex;align-items:center;gap:.35rem;font-size:.75rem;font-weight:600;color:#5b564e;margin:0 0 .28rem}',
        '.svw-moon .m-num{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;border-radius:50%;background:' + accent + '22;color:' + accent + ';font-size:.64rem;font-weight:700;flex:none}',
        '.svw-moon .m-opts{display:grid;grid-template-columns:repeat(3,1fr);gap:.32rem}',
        '.svw-moon .m-opt{font-family:inherit;font-size:.76rem;font-weight:600;line-height:1.2;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.4rem .28rem;min-height:38px;cursor:pointer}',
        '.svw-moon .m-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
        '.svw-moon .m-opt[data-key="1"]{box-shadow:inset 0 0 0 2px #4f7d63;border-color:#4f7d63}',
        '.svw-moon .m-opt:disabled{cursor:default;opacity:1}',
        '.svw-moon .m-go{margin-top:.5rem;font-family:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.5rem .95rem;cursor:pointer}',
        '.svw-moon .m-go:disabled{background:#efe9e0;border-color:#e0d9cd;color:#a49d93;cursor:default}',
        '.svw-moon .m-cap{margin:.5rem 0 0;font-size:.8rem;line-height:1.55;color:#5b564e;min-height:66px}',
        '.svw-moon .m-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}'
      ].join('');

      /* ---------- build the DOM once, then mutate it ---------- */
      root.textContent = '';
      var st = document.createElement('style');
      st.textContent = css;
      root.appendChild(st);

      var wrap = mk('div', 'svw-moon');
      root.appendChild(wrap);

      var head = mk('div', 'm-head');
      var kick = mk('span', 'm-kick'); kick.textContent = 'The Moon';
      var run = mk('span', 'm-run');
      head.appendChild(kick); head.appendChild(run);
      wrap.appendChild(head);

      var h = mk('div', 'm-title'); h.textContent = META.title;
      wrap.appendChild(h);

      var frame = mk('p', 'm-frame');
      wrap.appendChild(frame);

      var stage = mk('div', 'm-stage');
      var svgwrap = mk('div', 'm-svgwrap');
      stage.appendChild(svgwrap);
      wrap.appendChild(stage);

      var g1 = group('1', 'When it arrives, which way does the crater face?',
        [['at', 'Towards Earth'], ['away', 'Away from Earth'], ['side', 'Side-on']]);
      var g2 = group('2', 'How much of the Earth-facing side is sunlit then?',
        [['all', 'All of it'], ['half', 'Half of it'], ['none', 'None of it']]);
      wrap.appendChild(g1.box); wrap.appendChild(g2.box);

      var go = mk('button', 'm-go'); go.type = 'button'; go.textContent = 'Check';
      wrap.appendChild(go);

      var cap = mk('p', 'm-cap');
      wrap.appendChild(cap);

      var sr = mk('p', 'm-sr'); sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      /* ---------- the one stage ---------- */
      var CX = 176, CY = 65, R = 48, MR = 11, VW = 300, VH = 130;
      var svg = svgel('svg', { viewBox: '0 0 ' + VW + ' ' + VH, role: 'img' });
      svgwrap.appendChild(svg);

      svg.appendChild(svgel('circle', {
        cx: CX, cy: CY, r: R, fill: 'none', stroke: '#d8d1c5',
        'stroke-width': 1, 'stroke-dasharray': '3 4'
      }));

      /* the Sun, far to the left, with parallel rays */
      [47, 65, 83].forEach(function (y) {
        svg.appendChild(svgel('line', { x1: 31, y1: y, x2: 45, y2: y, stroke: accent + '99', 'stroke-width': 1.6 }));
        svg.appendChild(svgel('path', { d: 'M45 ' + (y - 3) + 'L51 ' + y + 'L45 ' + (y + 3) + 'Z', fill: accent + '99' }));
      });
      svg.appendChild(svgel('circle', { cx: 16, cy: 65, r: 11, fill: accent + '2e', stroke: accent + '88', 'stroke-width': 1.2 }));
      svg.appendChild(svglabel(16, 88, 'Sun', 'middle'));

      bodyDisc(svg, CX, CY, 11, '#6f6a62', '#ded8cc', '#5b564e');
      svg.appendChild(svglabel(CX, 86, 'Earth', 'middle'));

      /* a key, so the coloured dot is never a mystery */
      svg.appendChild(svgel('circle', { cx: 250, cy: 14, r: 3.4, fill: accent }));
      svg.appendChild(svglabel(258, 18, 'crater', 'start'));

      var dest = svgel('circle', {
        cx: CX, cy: CY, r: MR, fill: 'none', stroke: '#b3aa9c',
        'stroke-width': 1.2, 'stroke-dasharray': '3 3'
      });
      svg.appendChild(dest);

      var ghosts = [];
      for (var gi = 0; gi < 7; gi++) {
        var gg = svgel('g', { opacity: '0' });
        gg.appendChild(svgel('circle', { r: 7.5, fill: '#b9b1a4', stroke: '#c9c1b4', 'stroke-width': .8 }));
        gg.appendChild(svgel('path', { fill: '#fff', stroke: '#c9c1b4', 'stroke-width': .8 }));
        gg.appendChild(svgel('circle', { r: 2.3, fill: accent }));
        svg.appendChild(gg);
        ghosts.push(gg);
      }

      var moonG = svgel('g', {});
      var moonDark = svgel('circle', { r: MR, fill: '#b9b1a4', stroke: '#9c9488', 'stroke-width': 1 });
      var moonLit = svgel('path', { fill: '#fff', stroke: '#9c9488', 'stroke-width': 1 });
      var craterTick = svgel('line', { stroke: accent, 'stroke-width': 1.6 });
      var craterDot = svgel('circle', { r: 3.4, fill: accent, stroke: '#fff', 'stroke-width': .8 });
      moonG.appendChild(moonDark); moonG.appendChild(moonLit);
      moonG.appendChild(craterTick); moonG.appendChild(craterDot);
      svg.appendChild(moonG);

      /* ---------- state ---------- */
      var round = { spin: 0, start: 0, travel: 180 };
      var deck = [], lastSpin = -1, first = true;
      var pickFace = null, pickLit = null;
      var phase = 'answer';            /* answer | revealed */
      var streak = 0, attempted = 0, mastered = false;
      var raf = 0, trailTo = -1;

      newRound();

      /* ---------- interaction ---------- */
      g1.buttons.forEach(function (b) {
        b.addEventListener('click', function () {
          if (phase !== 'answer') return;
          pickFace = b.dataset.val; paint(); publish();
        });
      });
      g2.buttons.forEach(function (b) {
        b.addEventListener('click', function () {
          if (phase !== 'answer') return;
          pickLit = b.dataset.val; paint(); publish();
        });
      });
      go.addEventListener('click', function () {
        if (phase === 'answer') { commit(); } else { newRound(); }
      });

      function commit() {
        if (!pickFace || !pickLit) return;
        var end = round.start + round.travel;
        var ansFace = faceAt(round, end), ansLit = litAt(end);
        var okFace = pickFace === ansFace, okLit = pickLit === ansLit;
        var right = okFace && okLit;
        attempted++;
        streak = right ? streak + 1 : 0;
        if (streak >= 3) mastered = true;
        phase = 'revealed';

        var msg;
        if (right) {
          msg = 'Right — crater ' + FACE_IS[ansFace] + '; Earth-facing side ' + LIT_SAID[ansLit] + '. ' + MECH_FACE[round.spin];
          if (ansLit === 'none') msg += ' ' + MECH_LIT.none;
        } else if (!okFace && !okLit) {
          msg = 'Not quite — you said crater ' + FACE_SAID[pickFace] + ', Earth-facing side ' + LIT_SAID[pickLit] +
            '. In fact: crater ' + FACE_IS[ansFace] + '; Earth-facing side ' + LIT_SAID[ansLit] + '. ' +
            MECH_FACE[round.spin] + ' ' + MECH_LIT[ansLit];
        } else if (!okFace) {
          msg = 'Not quite — you said the crater ' + FACE_SAID[pickFace] + '. It ends up ' + FACE_IS[ansFace] +
            '. The sunlit half you had right. ' + MECH_FACE[round.spin];
        } else {
          msg = 'Not quite — the crater you had right, but you said the Earth-facing side ' + LIT_SAID[pickLit] +
            '. It is ' + LIT_SAID[ansLit] + '. ' + MECH_LIT[ansLit];
        }
        if (streak === 3) {
          msg = 'Three in a row — you have it. The Moon does spin: one turn takes 27.3 days, exactly the time it takes to orbit Earth. ' +
            'That match is called synchronous rotation, and Earth’s tidal pull is what locked it in — tidal locking.';
        }
        say(msg);
        paint();
        publish();
        play();
        try { go.focus(); } catch (e) {}
      }

      function newRound() {
        cancel();
        if (first) { round = { spin: 0, start: 0, travel: 180 }; first = false; }
        else { round = dealt(); }
        lastSpin = round.spin;
        pickFace = null; pickLit = null; phase = 'answer'; trailTo = -1;
        frame.innerHTML = 'Looking down on the Earth–Moon system. The marked crater starts facing Earth. ' +
          'It now travels <b>' + TRAVEL_WORD[round.travel] + '</b> to the dashed circle, <b>' +
          SPIN_WORD[round.spin] + '</b>. Predict what Earth sees when it arrives.';
        say('The Moon takes 27.3 days to travel once round Earth.');
        drawAt(round.start);
        paint();
        publish();
      }

      function dealt() {
        if (!deck.length) {
          [0, 1, 2].forEach(function (sp) {
            [0, 90, 180, 270].forEach(function (s) {
              [90, 180, 270].forEach(function (tv) { deck.push({ spin: sp, start: s, travel: tv }); });
            });
          });
          for (var i = deck.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1)), t = deck[i]; deck[i] = deck[j]; deck[j] = t;
          }
        }
        var at = -1;
        for (var k = 0; k < deck.length; k++) { if (deck[k].spin !== lastSpin) { at = k; break; } }
        if (at < 0) at = 0;
        return deck.splice(at, 1)[0];
      }

      /* ---------- drawing: one model, every view ---------- */
      function drawAt(theta) {
        var x = CX + R * cosD(theta), y = CY - R * sinD(theta);
        var phi = craterAngle(round, theta);
        moonDark.setAttribute('cx', x); moonDark.setAttribute('cy', y);
        moonLit.setAttribute('d', leftHalf(x, y, MR));
        var dx = x + MR * cosD(phi), dy = y - MR * sinD(phi);
        craterTick.setAttribute('x1', x); craterTick.setAttribute('y1', y);
        craterTick.setAttribute('x2', dx); craterTick.setAttribute('y2', dy);
        craterDot.setAttribute('cx', dx); craterDot.setAttribute('cy', dy);

        var e = round.start + round.travel;
        dest.setAttribute('cx', CX + R * cosD(e));
        dest.setAttribute('cy', CY - R * sinD(e));
        dest.setAttribute('opacity', phase === 'answer' ? '1' : '0');

        var steps = round.travel / 45;
        for (var i = 0; i < ghosts.length; i++) {
          var on = i <= steps && i <= trailTo;
          ghosts[i].setAttribute('opacity', on ? '.55' : '0');
          if (!on) continue;
          var gt = round.start + 45 * i;
          var gx = CX + R * cosD(gt), gy = CY - R * sinD(gt);
          var gp = craterAngle(round, gt);
          ghosts[i].childNodes[0].setAttribute('cx', gx);
          ghosts[i].childNodes[0].setAttribute('cy', gy);
          ghosts[i].childNodes[1].setAttribute('d', leftHalf(gx, gy, 7.5));
          ghosts[i].childNodes[2].setAttribute('cx', gx + 7.5 * cosD(gp));
          ghosts[i].childNodes[2].setAttribute('cy', gy - 7.5 * sinD(gp));
        }
        svg.setAttribute('aria-label', 'A view down onto Earth and the Moon, with sunlight coming from the left. ' +
          'The Moon is ' + Math.round(((theta % 360) + 360) % 360) + ' degrees round its orbit, and the marked crater is ' +
          FACE_IS[faceAt(round, Math.round(theta))] + '.');
      }

      function play() {
        var from = round.start, to = round.start + round.travel;
        if (calm) { trailTo = 9; drawAt(to); return; }
        var t0 = 0;
        cancel();
        raf = requestAnimationFrame(function step(ts) {
          if (!root.isConnected) { raf = 0; return; }
          if (!t0) t0 = ts;
          var p = Math.min(1, (ts - t0) / 1150);
          var e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
          var th = from + (to - from) * e;
          trailTo = Math.floor((th - from) / 45);
          drawAt(th);
          if (p < 1) { raf = requestAnimationFrame(step); }
          else { raf = 0; trailTo = 9; drawAt(to); }
        });
      }
      function cancel() { if (raf) { cancelAnimationFrame(raf); raf = 0; } }

      function leftHalf(cx, cy, r) {
        return 'M' + cx + ' ' + (cy - r) + 'A' + r + ' ' + r + ' 0 0 0 ' + cx + ' ' + (cy + r) + 'Z';
      }

      /* ---------- controls and caption ---------- */
      function paint() {
        var end = round.start + round.travel;
        var ansFace = faceAt(round, end), ansLit = litAt(end);
        mark(g1.buttons, pickFace, phase === 'revealed' ? ansFace : null);
        mark(g2.buttons, pickLit, phase === 'revealed' ? ansLit : null);
        if (phase === 'answer') {
          go.textContent = 'Check';
          go.disabled = !(pickFace && pickLit);
          if (pickFace && pickLit) {
            say('Your prediction: crater ' + FACE_SAID[pickFace] + ', Earth-facing side ' + LIT_SAID[pickLit] + '.');
          } else if (pickFace || pickLit) {
            say('Your prediction so far: ' + (pickFace ? 'crater ' + FACE_SAID[pickFace] : 'Earth-facing side ' + LIT_SAID[pickLit]) + '.');
          }
        } else {
          go.textContent = mastered ? 'Another anyway' : 'Next';
          go.disabled = false;
        }
        run.textContent = mastered ? 'You have it'
          : streak === 0 ? ''
            : streak + ' in a row — ' + (3 - streak) + ' more';
      }
      function mark(btns, picked, key) {
        btns.forEach(function (b) {
          b.setAttribute('aria-pressed', b.dataset.val === picked ? 'true' : 'false');
          if (key && b.dataset.val === key) { b.dataset.key = '1'; } else { delete b.dataset.key; }
          b.disabled = phase !== 'answer';
        });
      }
      function say(msg) { cap.textContent = msg; sr.textContent = msg; }

      function publish() {
        var end = round.start + round.travel;
        root.dataset.svState = JSON.stringify({
          spinPerOrbit: round.spin,
          travelDegrees: round.travel,
          faceAnswer: faceAt(round, end),
          litAnswer: litAt(end),
          pickFace: pickFace,
          pickLit: pickLit,
          phase: phase,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      /* ---------- small helpers ---------- */
      function mk(tag, cls) { var n = document.createElement(tag); if (cls) { n.className = cls; } return n; }
      function svgel(tag, attrs) {
        var n = document.createElementNS('http://www.w3.org/2000/svg', tag);
        for (var k in attrs) { if (Object.prototype.hasOwnProperty.call(attrs, k)) { n.setAttribute(k, attrs[k]); } }
        return n;
      }
      function svglabel(x, y, txt, anchor) {
        var n = svgel('text', {
          x: x, y: y, 'text-anchor': anchor, 'font-size': 11, fill: '#8d8880',
          'font-family': 'Inter,system-ui,sans-serif'
        });
        n.textContent = txt;
        return n;
      }
      function bodyDisc(target, cx, cy, r, dark, lit, stroke) {
        target.appendChild(svgel('circle', { cx: cx, cy: cy, r: r, fill: dark, stroke: stroke, 'stroke-width': 1 }));
        target.appendChild(svgel('path', { d: leftHalf(cx, cy, r), fill: lit, stroke: stroke, 'stroke-width': 1 }));
      }
      function group(num, question, opts) {
        var box = mk('div', 'm-grp');
        var lab = mk('div', 'm-lab');
        var chip = mk('span', 'm-num'); chip.textContent = num;
        var q = mk('span'); q.textContent = question;
        lab.appendChild(chip); lab.appendChild(q);
        var row = mk('div', 'm-opts');
        var buttons = opts.map(function (o) {
          var b = mk('button', 'm-opt');
          b.type = 'button';
          b.dataset.val = o[0];
          b.textContent = o[1];
          b.setAttribute('aria-pressed', 'false');
          row.appendChild(b);
          return b;
        });
        box.appendChild(lab); box.appendChild(row);
        return { box: box, buttons: buttons };
      }
    }
  };
})();
