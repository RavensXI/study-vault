/* series-voltage-split — Combined Science, Series and Parallel Circuits (L4)

   Attacks two beliefs at once:
     1. "current gets used up as it goes round"   -> three ammeters on one
        loop always read the SAME number, and evenly spaced dots keep their
        spacing and their speed all the way round, through both resistors.
     2. "the supply splits 50/50, or the first resistor uses it up first"
        -> the student must COMMIT a split before anything is revealed.

   Commit before feedback: the widget opens in Predict. The bar is blank,
   the ammeters read "?", and the two resistor blocks are drawn the SAME
   width so the picture cannot leak the answer. Only on Check do the blocks
   snap to proportional width, the bar fills, and the ammeters agree.

   Arithmetic: every challenge is stored as integer half-volts and is
   verified at load time by two integer identities —
       v1h + v2h === 2*v          (p.d.s add to the supply)
       v1h * r2  === v2h * r1     (one current: V1/R1 === V2/R2)
   Success is an integer comparison on half-volts, never a float compare.
   The explore mode displays V2 as (supply - displayed V1) so the two
   printed numbers always add to the printed supply.
*/
(function () {
  'use strict';

  /* ---------- geometry (SVG user units, viewBox 320 x 182) ---------- */
  var X0 = 70, SPAN = 200, GAPW = 18, BLOCKW = SPAN - GAPW; /* 182 */
  var MINBLOCK = 24;
  var BAR_Y = 138, BAR_H = 28;

  /* ---------- challenge pool: integer half-volts, no floats ---------- */
  var POOL = [
    { r1: 9,  r2: 3,  v: 12, v1h: 18, v2h: 6  },
    { r1: 2,  r2: 6,  v: 12, v1h: 6,  v2h: 18 },
    { r1: 6,  r2: 2,  v: 16, v1h: 24, v2h: 8  },
    { r1: 10, r2: 5,  v: 15, v1h: 20, v2h: 10 },
    { r1: 3,  r2: 12, v: 15, v1h: 6,  v2h: 24 },
    { r1: 8,  r2: 8,  v: 24, v1h: 24, v2h: 24 },
    { r1: 12, r2: 4,  v: 8,  v1h: 12, v2h: 4  },
    { r1: 5,  r2: 15, v: 10, v1h: 5,  v2h: 15 },
    { r1: 7,  r2: 14, v: 21, v1h: 14, v2h: 28 },
    { r1: 2,  r2: 10, v: 18, v1h: 6,  v2h: 30 }
  ].filter(function (c) {
    /* self-check the data rather than trusting it */
    return c.v1h + c.v2h === 2 * c.v && c.v1h * c.r2 === c.v2h * c.r1 &&
           c.v1h > 0 && c.v2h > 0;
  });

  var CSS = [
    '.svsvs{background:#fff;border:1px solid #e8e3db;border-radius:16px;padding:1.15rem;',
    'box-shadow:0 1px 2px rgba(45,42,38,.04),0 14px 34px -24px rgba(45,42,38,.25);',
    'font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;',
    'color:#2d2a26;line-height:1.4;box-sizing:border-box}',
    '.svsvs *,.svsvs *::before,.svsvs *::after{box-sizing:border-box}',
    '.svsvs.narrow{padding:.9rem}',

    '.svsvs .s-head{display:flex;align-items:center;justify-content:space-between;gap:.6rem;flex-wrap:wrap}',
    '.svsvs .s-kicker{font-size:.68rem;font-weight:700;letter-spacing:.11em;',
    'text-transform:uppercase;color:var(--svsvs-acc)}',
    '.svsvs .s-modes{display:inline-flex;border:1px solid #ddd7cd;border-radius:10px;overflow:hidden}',
    '.svsvs .s-modes button{font:inherit;font-size:.78rem;font-weight:600;padding:.4rem .85rem;',
    'background:#faf8f5;color:#5b564e;border:0;cursor:pointer}',
    '.svsvs .s-modes button+button{border-left:1px solid #ddd7cd}',
    '.svsvs .s-modes button.on{background:#2d2a26;color:#fff}',
    '.svsvs .s-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.22rem;font-weight:600;',
    'line-height:1.25;margin:.3rem 0 .5rem;color:#2d2a26}',

    '.svsvs .s-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.35rem}',
    '.svsvs .s-svgwrap{position:relative;max-width:404px;margin:0 auto}',
    '.svsvs .s-stage svg{display:block;width:100%;height:auto;overflow:visible}',
    /* a real range input, invisible, sitting exactly over the voltage bar: the
       divider is drawn in SVG but the CONTROL is HTML, so keyboard, touch and
       screen readers all work (SVG elements do not fire focus events) */
    '.svsvs .s-split{position:absolute;left:20.625%;width:65%;top:71.4%;height:24.2%;',
    'margin:0;padding:0;opacity:0;cursor:ew-resize;touch-action:none}',
    '.svsvs .s-split:disabled{cursor:default}',
    '.svsvs .s-ring{position:absolute;left:20.625%;width:65%;top:71.4%;height:24.2%;',
    'border:2px solid var(--svsvs-acc);border-radius:8px;pointer-events:none;opacity:0}',
    '.svsvs .s-split:focus-visible+.s-ring{opacity:1}',

    '.svsvs .s-wire{fill:none;stroke:#8d8880;stroke-width:2;stroke-linecap:square}',
    '.svsvs .s-plate{stroke:#2d2a26;stroke-linecap:butt}',
    '.svsvs .s-block{stroke:#2d2a26;stroke-width:1.2}',
    '.svsvs .s-lbl{font-size:11px;font-weight:600;fill:#2d2a26;font-variant-numeric:tabular-nums}',
    '.svsvs .s-in{font-size:10px;font-weight:600;fill:#2d2a26}',
    '.svsvs .s-tiny{font-size:9px;fill:#8d8880}',
    '.svsvs .s-val{font-size:10px;fill:#2d2a26;font-variant-numeric:tabular-nums}',
    '.svsvs .s-amc{fill:#fff;stroke:#2d2a26;stroke-width:1.3}',
    '.svsvs .s-amt{font-size:9px;font-weight:700;fill:#2d2a26}',
    '.svsvs .s-dot{stroke:none}',
    '.svsvs .s-bar{fill:#fff;stroke:#ddd7cd;stroke-width:1}',
    '.svsvs .s-true{stroke:#2d2a26;stroke-width:2}',
    '.svsvs .s-segv{font-size:11px;font-weight:600;fill:#2d2a26;font-variant-numeric:tabular-nums}',
    '.svsvs .s-pline{stroke:#2d2a26;stroke-width:2.4}',
    '.svsvs .s-pred.done .s-pline{stroke:#8d8880;stroke-width:2;stroke-dasharray:4 3}',
    '.svsvs .s-pred.done .s-grip,.svsvs .s-pred.done .s-gt{display:none}',
    '.svsvs .s-grip{fill:#fff;stroke:#2d2a26;stroke-width:1.4}',
    '.svsvs .s-gt{stroke:#8d8880;stroke-width:1}',
    '.svsvs .s-you{font-size:9px;fill:#8d8880}',

    '.svsvs .s-sliders{display:grid;grid-template-columns:repeat(3,1fr);gap:.35rem .9rem;margin-top:.7rem}',
    '.svsvs.narrow .s-sliders{grid-template-columns:1fr 1fr}',
    '.svsvs.narrow .s-ctl.wide{grid-column:1/-1}',
    '.svsvs .s-ctl{display:block}',
    '.svsvs .s-ctl .top{display:flex;justify-content:space-between;align-items:baseline;',
    'font-size:.76rem;font-weight:600;color:#5b564e}',
    '.svsvs .s-ctl .top b{color:#2d2a26;font-weight:600;font-variant-numeric:tabular-nums}',
    '.svsvs .s-ctl input[type=range]{display:block;width:100%;height:22px;margin:.05rem 0 0;',
    'accent-color:var(--svsvs-acc)}',
    '.svsvs .s-ends{display:flex;justify-content:space-between;font-size:.62rem;color:#8d8880}',

    '.svsvs .s-actions{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.75rem}',
    '.svsvs .s-btn{font:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;',
    'background:#faf8f5;color:#2d2a26;border:1px solid #ddd7cd;border-radius:10px;cursor:pointer}',
    '.svsvs .s-btn:hover{border-color:#b9b0a2}',
    '.svsvs .s-btn.primary{background:#2d2a26;color:#fff;border-color:#2d2a26}',

    '.svsvs .s-stats{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.7rem}',
    '.svsvs .s-pill{background:var(--accent-badge,#f4f0ea);border-radius:9px;padding:.34rem .6rem;',
    'font-size:.76rem;color:#5b564e}',
    '.svsvs .s-pill b{color:#2d2a26;margin-left:.32rem;font-variant-numeric:tabular-nums}',
    '.svsvs .s-pill.good b{color:#4f7d63}',

    '.svsvs .s-caption{font-size:.88rem;line-height:1.5;color:#5b564e;margin:.7rem 0 0;min-height:3em}',
    '.svsvs .s-caption b{color:#2d2a26}',
    '.svsvs .s-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;',
    'clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svsvs button:focus-visible,.svsvs input:focus-visible{outline:2px solid var(--svsvs-acc);outline-offset:2px}'
  ].join('');

  window.SVWidget = {
    meta: {
      id: 'series-voltage-split',
      title: 'Where Do the Volts Go?',
      teaches: 'In series the current is identical everywhere, and the supply voltage divides between components in proportion to their resistance'
    },

    mount: function (root, ctx) {
      var reduced = !!(ctx && ctx.reducedMotion);
      var acc = (ctx && ctx.accent) ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var uid = 's' + Math.random().toString(36).slice(2, 8);

      /* ---------- colour helpers ---------- */
      function rgb(hex) {
        var h = String(hex).replace('#', '');
        if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
        if (h.length !== 6 || /[^0-9a-fA-F]/.test(h)) h = '8a6a4f';
        return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
      }
      function tint(a) { var c = rgb(acc); return 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + a + ')'; }
      var T1 = tint(0.55), T2 = tint(0.17);

      /* ---------- state (single source of truth) ---------- */
      var state = {
        mode: 'challenge',           /* 'challenge' (Predict) | 'explore' */
        r1: 4, r2: 8, voltage: 12,   /* explore: the lesson's own worked example */
        challenge: null
      };
      var order = [], orderAt = 0;
      /* Mastery exit: three right in a row and the student has it — stop
         asking. A wrong answer resets the run, so the cost of guessing is
         having to show it twice more. Nobody is made to grind ten. */
      var STREAK_TARGET = 3;
      var streak = 0, mastered = false, seen = 0;

      function reshuffle() {
        var rest = [];
        for (var i = 1; i < POOL.length; i++) rest.push(i);
        for (var j = rest.length - 1; j > 0; j--) {
          var k = Math.floor(Math.random() * (j + 1)), t = rest[j]; rest[j] = rest[k]; rest[k] = t;
        }
        order = [0].concat(rest);
        orderAt = 0;
      }
      reshuffle();

      function newChallenge() {
        if (orderAt >= order.length) {
          /* keep cycling, never repeat the one just seen */
          var last = order[order.length - 1];
          reshuffle();
          order = order.filter(function (n) { return n !== last; }).concat([last]);
        }
        var c = POOL[order[orderAt++]];
        state.challenge = {
          r1: c.r1, r2: c.r2, voltage: c.v,
          v1h: c.v1h, v2h: c.v2h, hv: 2 * c.v,
          predH: c.v,                /* half of the supply, in half-volts */
          committed: false
        };
      }
      newChallenge();

      /* ---------- physics ---------- */
      function deriveExplore() {
        var rt = state.r1 + state.r2;
        var i = state.voltage / rt;
        var v1 = i * state.r1;
        return { rt: rt, i: i, v1: v1, v2: state.voltage - v1, frac: state.r1 / rt };
      }
      function deriveChallenge() {
        var c = state.challenge;
        return {
          i: c.v1h / (2 * c.r1),     /* === v2h/(2*r2), proven by the load-time check */
          v1: c.v1h / 2, v2: c.v2h / 2,
          frac: c.v1h / c.hv,
          predV1: c.predH / 2, predV2: (c.hv - c.predH) / 2,
          predFrac: c.predH / c.hv,
          errH: Math.abs(c.predH - c.v1h)
        };
      }

      /* ---------- number formatting ---------- */
      function f2(x) { return (Math.round(x * 100) / 100).toFixed(2); }
      function f1(x) { return (Math.round(x * 10) / 10).toFixed(1); }

      /* ---------- markup, built once ---------- */
      root.classList.add('svsvs');
      root.style.setProperty('--svsvs-acc', acc);
      root.innerHTML = [
        '<style>', CSS, '</style>',
        '<div class="s-head"><span class="s-kicker">Interactive</span>',
        '<div class="s-modes" role="group" aria-label="Mode">',
        '<button type="button" class="on" data-mode="challenge" aria-pressed="true">Predict</button>',
        '<button type="button" data-mode="explore" aria-pressed="false">Explore</button>',
        '</div></div>',
        '<h3 class="s-title">Where do the volts go?</h3>',

        '<div class="s-stage"><div class="s-svgwrap"><svg viewBox="0 0 320 182">',
        '<defs><clipPath id="', uid, '-c">',
        '<rect x="', X0, '" y="', BAR_Y, '" width="', SPAN, '" height="', BAR_H, '" rx="5"/>',
        '</clipPath></defs>',
        /* wire loop, broken at the cell */
        '<path class="s-wire" d="M26,33 H294 V108 H26 V80"/>',
        '<path class="s-wire" d="M26,64 V33"/>',
        '<path class="s-track" d="M26,33 H294 V108 H26 Z" fill="none" stroke="none"/>',
        /* resistors */
        '<rect class="s-block s-b1" x="70" y="22" width="91" height="22" rx="4"/>',
        '<rect class="s-block s-b2" x="179" y="22" width="91" height="22" rx="4"/>',
        '<text class="s-in s-i1" x="115" y="37" text-anchor="middle">R₁</text>',
        '<text class="s-in s-i2" x="224" y="37" text-anchor="middle">R₂</text>',
        '<text class="s-lbl s-o1" x="115" y="14" text-anchor="middle">4 Ω</text>',
        '<text class="s-lbl s-o2" x="224" y="14" text-anchor="middle">8 Ω</text>',
        '<g class="s-dots"></g>',
        /* ammeters */
        '<circle class="s-amc s-c1" cx="48" cy="33" r="8"/>',
        '<text class="s-amt" x="48" y="36.5" text-anchor="middle">A</text>',
        '<text class="s-val s-a1" x="48" y="52" text-anchor="middle">? A</text>',
        '<circle class="s-amc s-c2" cx="170" cy="33" r="8"/>',
        '<text class="s-amt s-t2" x="170" y="36.5" text-anchor="middle">A</text>',
        '<text class="s-val s-a2" x="170" y="52" text-anchor="middle">? A</text>',
        '<circle class="s-amc" cx="160" cy="108" r="8"/>',
        '<text class="s-amt" x="160" y="111.5" text-anchor="middle">A</text>',
        '<text class="s-val s-a3" x="174" y="104">? A</text>',
        /* cell */
        '<line class="s-plate" x1="13" y1="66" x2="39" y2="66" stroke-width="2"/>',
        '<line class="s-plate" x1="20" y1="78" x2="32" y2="78" stroke-width="3.4"/>',
        '<text class="s-tiny" x="8" y="62" text-anchor="middle">+</text>',
        '<text class="s-tiny" x="8" y="90" text-anchor="middle">−</text>',
        '<text class="s-lbl s-sup" x="46" y="70">12 V</text>',
        '<text class="s-tiny" x="46" y="82">supply</text>',
        /* voltage bar */
        '<text class="s-tiny" x="70" y="132">potential difference</text>',
        '<text class="s-tiny s-tot" x="270" y="132" text-anchor="end">supply 12 V</text>',
        '<rect class="s-bar" x="', X0, '" y="', BAR_Y, '" width="', SPAN, '" height="', BAR_H, '" rx="5"/>',
        '<g clip-path="url(#', uid, '-c)">',
        '<rect class="s-s1" x="', X0, '" y="', BAR_Y, '" width="0" height="', BAR_H, '"/>',
        '<rect class="s-s2" x="', X0, '" y="', BAR_Y, '" width="0" height="', BAR_H, '"/>',
        '</g>',
        '<text class="s-tiny s-e1" x="76" y="157">R₁</text>',
        '<text class="s-tiny s-e2" x="264" y="157" text-anchor="end">R₂</text>',
        '<line class="s-true" x1="170" y1="136" x2="170" y2="168"/>',
        '<text class="s-segv s-v1" x="115" y="156" text-anchor="middle"></text>',
        '<text class="s-segv s-v2" x="224" y="156" text-anchor="middle"></text>',
        '<g class="s-pred" transform="translate(170,0)" style="pointer-events:none">',
        '<line class="s-pline" x1="0" y1="136" x2="0" y2="168"/>',
        '<rect class="s-grip" x="-6" y="145" width="12" height="16" rx="3"/>',
        '<line class="s-gt" x1="-2.5" y1="149" x2="-2.5" y2="157"/>',
        '<line class="s-gt" x1="2.5" y1="149" x2="2.5" y2="157"/>',
        '<text class="s-you" x="0" y="178" text-anchor="middle">you</text>',
        '</g>',
        '</svg>',
        '<input type="range" class="s-split" min="0" max="24" step="1" value="12">',
        '<div class="s-ring"></div>',
        '</div></div>',

        '<div class="s-sliders">',
        ctl('r1', 'Resistor R₁', 1, 20, 4, '1 Ω', '20 Ω', ''),
        ctl('r2', 'Resistor R₂', 1, 20, 8, '1 Ω', '20 Ω', ''),
        ctl('voltage', 'Supply', 1, 24, 12, '1 V', '24 V', ' wide'),
        '</div>',

        '<div class="s-actions">',
        '<button type="button" class="s-btn primary s-go" data-act="check">Check</button>',
        '<button type="button" class="s-btn s-new">New numbers</button>',
        '</div>',

        '<div class="s-stats">',
        '<span class="s-pill" data-p="0"><i></i><b></b></span>',
        '<span class="s-pill" data-p="1"><i></i><b></b></span>',
        '<span class="s-pill" data-p="2"><i></i><b></b></span>',
        '<span class="s-pill" data-p="3"><i></i><b></b></span>',
        '</div>',
        '<p class="s-caption"></p>',
        '<p class="s-sr" aria-live="polite"></p>'
      ].join('');

      function ctl(key, label, min, max, val, lo, hi, extra) {
        return '<label class="s-ctl' + extra + '"><span class="top"><span>' + label +
          '</span><b data-out="' + key + '"></b></span>' +
          '<input type="range" min="' + min + '" max="' + max + '" step="1" value="' + val +
          '" data-key="' + key + '" aria-label="' + label.replace(/[₁]/, ' 1').replace(/[₂]/, ' 2') + '">' +
          '<span class="s-ends"><span>' + lo + '</span><span>' + hi + '</span></span></label>';
      }

      var q = function (s) { return root.querySelector(s); };
      var svg = q('svg');
      var el = {
        b1: q('.s-b1'), b2: q('.s-b2'), i1: q('.s-i1'), i2: q('.s-i2'),
        o1: q('.s-o1'), o2: q('.s-o2'),
        c2: q('.s-c2'), t2: q('.s-t2'),
        a1: q('.s-a1'), a2: q('.s-a2'), a3: q('.s-a3'),
        sup: q('.s-sup'), tot: q('.s-tot'),
        s1: q('.s-s1'), s2: q('.s-s2'), trueLine: q('.s-true'),
        e1: q('.s-e1'), e2: q('.s-e2'), you: null,
        v1: q('.s-v1'), v2: q('.s-v2'),
        pred: q('.s-pred'), split: q('.s-split'), ring: q('.s-ring'),
        track: q('.s-track'), dots: q('.s-dots'),
        sliders: q('.s-sliders'), actions: q('.s-actions'),
        go: q('.s-go'), fresh: q('.s-new'),
        caption: q('.s-caption'), sr: q('.s-sr'),
        modes: root.querySelectorAll('.s-modes button'),
        pills: root.querySelectorAll('.s-pill')
      };
      el.b1.setAttribute('fill', T1); el.b2.setAttribute('fill', T2);
      el.s1.setAttribute('fill', T1); el.s2.setAttribute('fill', T2);

      function show(n, on) { n.style.display = on ? '' : 'none'; }

      /* ---------- current dots: one path, uniform spacing, uniform speed ---------- */
      var NDOTS = 12, dots = [], pathLen = 0, offset = 0, lastT = 0, raf = 0, visible = true;
      for (var d = 0; d < NDOTS; d++) {
        var c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        c.setAttribute('class', 's-dot'); c.setAttribute('r', '2.8'); c.setAttribute('fill', acc);
        el.dots.appendChild(c); dots.push(c);
      }
      function placeDots() {
        if (!pathLen) { try { pathLen = el.track.getTotalLength(); } catch (e) { pathLen = 0; } }
        if (!pathLen) return;
        for (var i = 0; i < NDOTS; i++) {
          var p = el.track.getPointAtLength((offset + i * pathLen / NDOTS) % pathLen);
          dots[i].setAttribute('cx', p.x); dots[i].setAttribute('cy', p.y);
        }
      }
      function dotSpeed() {
        /* px/s. Neutral while the answer is still hidden, so speed leaks nothing. */
        if (state.mode === 'challenge' && !state.challenge.committed) return 60;
        var i = state.mode === 'explore' ? deriveExplore().i : deriveChallenge().i;
        return Math.max(26, Math.min(130, 30 + 30 * i));
      }
      function frame(t) {
        raf = 0;
        if (reduced || !visible) return;
        if (!lastT) lastT = t;
        var dt = Math.min(0.05, (t - lastT) / 1000); lastT = t;
        if (!pathLen) { try { pathLen = el.track.getTotalLength(); } catch (e) {} }
        if (pathLen) { offset = (offset + dotSpeed() * dt) % pathLen; placeDots(); }
        raf = requestAnimationFrame(frame);
      }
      function startLoop() {
        if (reduced || !visible || raf) return;
        lastT = 0; raf = requestAnimationFrame(frame);
      }
      if (window.IntersectionObserver) {
        new IntersectionObserver(function (es) {
          visible = es[0].isIntersecting;
          if (visible) startLoop(); else if (raf) { cancelAnimationFrame(raf); raf = 0; }
        }, { threshold: 0 }).observe(root);
      }

      /* ---------- render ---------- */
      function blockWidths(r1, r2, proportional) {
        if (!proportional) return [BLOCKW / 2, BLOCKW / 2];
        var w1 = BLOCKW * r1 / (r1 + r2);
        if (w1 < MINBLOCK) w1 = MINBLOCK;
        else if (BLOCKW - w1 < MINBLOCK) w1 = BLOCKW - MINBLOCK;
        return [w1, BLOCKW - w1];
      }
      function setSegLabel(node, text, cx, w) {
        var size = w >= 44 ? 11 : 9;
        var need = text.length * size * 0.58 + 6;
        if (w < need) { show(node, false); return; }
        show(node, true);
        node.setAttribute('x', cx); node.setAttribute('font-size', size);
        node.textContent = text;
      }
      function pill(n, label, value, good) {
        var p = el.pills[n];
        if (label == null) { show(p, false); return; }
        show(p, true);
        p.firstChild.textContent = label;
        p.lastChild.textContent = value;
        p.classList.toggle('good', !!good);
      }

      function render() {
        var explore = state.mode === 'explore';
        var c = state.challenge, dC = deriveChallenge(), dE = deriveExplore();
        var r1 = explore ? state.r1 : c.r1;
        var r2 = explore ? state.r2 : c.r2;
        var V = explore ? state.voltage : c.voltage;
        var revealed = explore || c.committed;

        /* circuit */
        var ws = blockWidths(r1, r2, revealed);
        el.b1.setAttribute('width', ws[0]);
        el.b2.setAttribute('x', X0 + ws[0] + GAPW); el.b2.setAttribute('width', ws[1]);
        var cx1 = X0 + ws[0] / 2, cx2 = X0 + ws[0] + GAPW + ws[1] / 2, cAm = X0 + ws[0] + GAPW / 2;
        el.i1.setAttribute('x', cx1); el.o1.setAttribute('x', cx1);
        el.i2.setAttribute('x', cx2); el.o2.setAttribute('x', cx2);
        el.o1.textContent = r1 + ' Ω'; el.o2.textContent = r2 + ' Ω';
        show(el.i1, ws[0] >= 26); show(el.i2, ws[1] >= 26);
        el.c2.setAttribute('cx', cAm); el.t2.setAttribute('x', cAm); el.a2.setAttribute('x', cAm);
        el.sup.textContent = V + ' V';
        el.tot.textContent = 'supply ' + V + ' V';

        var amp = revealed ? (explore ? f2(dE.i) : f1(dC.i)) + ' A' : '? A';
        el.a1.textContent = amp; el.a2.textContent = amp; el.a3.textContent = amp;

        /* bar */
        var frac = explore ? dE.frac : dC.frac;
        var w1b = SPAN * frac;
        show(el.s1, revealed); show(el.s2, revealed); show(el.trueLine, revealed);
        show(el.e1, !revealed); show(el.e2, !revealed);
        el.s1.setAttribute('width', w1b);
        el.s2.setAttribute('x', X0 + w1b); el.s2.setAttribute('width', SPAN - w1b);
        el.trueLine.setAttribute('x1', X0 + w1b); el.trueLine.setAttribute('x2', X0 + w1b);

        var d1 = explore ? f2(dE.v1) : f1(dC.v1);
        var d2 = explore ? f2(V - Math.round(dE.v1 * 100) / 100) : f1(dC.v2);
        if (revealed) {
          setSegLabel(el.v1, d1 + ' V', X0 + w1b / 2, w1b);
          setSegLabel(el.v2, d2 + ' V', X0 + w1b + (SPAN - w1b) / 2, SPAN - w1b);
        } else { show(el.v1, false); show(el.v2, false); }

        /* prediction marker */
        show(el.pred, !explore);
        show(el.split, !explore); show(el.ring, !explore);
        if (!explore) {
          var px = X0 + SPAN * dC.predFrac;
          el.pred.setAttribute('transform', 'translate(' + px + ',0)');
          el.pred.classList.toggle('done', c.committed);
          if (!el.you) el.you = el.pred.querySelector('.s-you');
          show(el.you, c.committed);
          el.split.max = String(c.hv);
          if (el.split.value !== String(c.predH)) el.split.value = String(c.predH);
          el.split.disabled = c.committed;
          el.split.setAttribute('aria-label',
            'Predicted split of the ' + c.voltage + ' volt supply, in volts across R1');
          el.split.setAttribute('aria-valuetext',
            f1(dC.predV1) + ' volts across R1, ' + f1(dC.predV2) + ' volts across R2');
        }

        /* controls */
        show(el.sliders, explore);
        show(el.actions, !explore);
        if (!explore) {
          el.go.textContent = c.committed
            ? (mastered ? 'Another anyway' : 'Next challenge') : 'Check';
          el.go.dataset.act = c.committed ? 'next' : 'check';
          show(el.fresh, !c.committed);
        }

        /* stats + caption */
        if (explore) {
          pill(0, 'Current I everywhere', f2(dE.i) + ' A');
          pill(1, 'V₁ across ' + r1 + ' Ω', d1 + ' V');
          pill(2, 'V₂ across ' + r2 + ' Ω', d2 + ' V');
          pill(3, 'R total', dE.rt + ' Ω');
          el.caption.innerHTML = r1 === r2
            ? 'Two identical ' + r1 + ' Ω resistors, so each drops half the supply: <b>' +
              d1 + ' V</b>. Same current everywhere — <b>' + f2(dE.i) +
              ' A</b> at all three ammeters.'
            : 'Same current everywhere — <b>' + f2(dE.i) + ' A</b> at all three ammeters. ' +
              'V = I × R, so ' + r1 + ' Ω drops <b>' + d1 + ' V</b> and ' + r2 +
              ' Ω drops <b>' + d2 + ' V</b> — together the ' + V + ' V supply.';
        } else if (!c.committed) {
          pill(0, 'Your V₁', f1(dC.predV1) + ' V');
          pill(1, 'Your V₂', f1(dC.predV2) + ' V');
          pill(2, null); pill(3, null);
          el.caption.innerHTML = 'How does <b>' + V + ' V</b> divide between a ' + r1 +
            ' Ω and a ' + r2 + ' Ω resistor in one series loop?' +
            (streak > 0 && !mastered
              ? ' <span style="color:#8d8880">' + streak + ' right in a row — ' +
                (STREAK_TARGET - streak) + ' more and you have it.</span>' : '');
        } else {
          var close = dC.errH <= 1;               /* integer half-volts, never a float compare */
          pill(0, 'Current I everywhere', f1(dC.i) + ' A');
          pill(1, 'V₁ across ' + r1 + ' Ω', d1 + ' V');
          pill(2, 'V₂ across ' + r2 + ' Ω', d2 + ' V');
          pill(3, 'Your split', f1(dC.predV1) + ' / ' + f1(dC.predV2) + ' V', close);
          el.caption.innerHTML = verdict(c, dC, close) +
            (mastered && close
              ? ' <b>Three in a row — you have it.</b> The current is the same everywhere, ' +
                'and V = I × R gives the bigger resistor the bigger share.'
              : (close && streak > 0
                  ? ' <span style="color:#8d8880">' + streak + ' in a row.</span>' : ''));
        }

        /* explore slider read-outs */
        root.querySelector('[data-out="r1"]').textContent = state.r1 + ' Ω';
        root.querySelector('[data-out="r2"]').textContent = state.r2 + ' Ω';
        root.querySelector('[data-out="voltage"]').textContent = state.voltage + ' V';

        placeDots();
        pushState();
      }

      function verdict(c, d, close) {
        var big = c.r1 > c.r2 ? c.r1 : c.r2, small = c.r1 > c.r2 ? c.r2 : c.r1;
        var vBig = f1(c.r1 > c.r2 ? d.v1 : d.v2), amp = f1(d.i);
        var v1 = f1(d.v1), v2 = f1(d.v2);
        if (close) {
          return 'Right. One current — <b>' + amp + ' A</b> — through both, so V = I × R: ' +
            c.r1 + ' Ω drops <b>' + v1 + ' V</b> and ' + c.r2 + ' Ω drops <b>' + v2 +
            ' V</b>. Together they make the ' + c.voltage + ' V supply.';
        }
        if (c.r1 === c.r2) {
          return 'Two identical ' + c.r1 + ' Ω resistors share the supply equally — <b>' +
            v1 + ' V</b> each — because the same <b>' + amp + ' A</b> flows through both.';
        }
        var half = c.hv / 2;
        if (Math.abs(c.predH - half) <= 1) {
          return 'A 50/50 split only happens with equal resistors. The same <b>' + amp +
            ' A</b> flows through both, so V = I × R gives the ' + c.r1 + ' Ω <b>' + v1 +
            ' V</b> and the ' + c.r2 + ' Ω <b>' + v2 + ' V</b>.';
        }
        var wrongWay = (c.r1 > c.r2 && c.predH < half) || (c.r1 < c.r2 && c.predH > half);
        if (wrongWay) {
          return 'You gave the bigger share to the ' + small + ' Ω. Current is not used up — ' +
            'the same <b>' + amp + ' A</b> passes through both — so V = I × R makes the ' +
            big + ' Ω drop the most: <b>' + vBig + ' V</b>.';
        }
        return 'Right direction, out by <b>' + f1(d.errH / 2) + ' V</b>. The shares copy the ' +
          'resistances exactly (' + c.r1 + ':' + c.r2 + '), so <b>' + v1 + ' V</b> and <b>' + v2 +
          ' V</b> — one current, ' + amp + ' A, through both.';
      }

      function pushState() {
        var dE = deriveExplore(), c = state.challenge, dC = deriveChallenge();
        var r3 = function (x) { return Math.round(x * 1000) / 1000; };
        root.dataset.svState = JSON.stringify({
          mode: state.mode === 'explore' ? 'explore' : 'challenge',
          r1: state.r1, r2: state.r2, voltage: state.voltage,
          totalR: dE.rt, current: r3(dE.i), v1: r3(dE.v1), v2: r3(dE.v2),
          challenge: {
            r1: c.r1, r2: c.r2, voltage: c.voltage,
            splitFrac: r3(dC.predFrac), committed: c.committed,
            predictedV1: dC.predV1, actualV1: dC.v1, actualV2: dC.v2,
            current: dC.i, actualFrac: r3(dC.frac),
            errorVolts: c.committed ? dC.errH / 2 : null,
            isClose: c.committed ? dC.errH <= 1 : null,
            streak: streak, mastered: mastered, attempted: seen
          }
        });
      }

      /* ---------- prediction input ---------- */
      function setPred(h) {
        var c = state.challenge;
        if (c.committed) return;                 /* dragSplit is a no-op once committed */
        h = Math.max(0, Math.min(c.hv, Math.round(h)));
        if (h === c.predH) return;
        c.predH = h; render();
      }
      el.split.addEventListener('input', function () {
        setPred(parseInt(el.split.value, 10));
      });

      /* ---------- buttons ---------- */
      el.go.addEventListener('click', function () {
        var c = state.challenge;
        if (!c.committed) {
          c.committed = true;
          var d = deriveChallenge();
          seen++;
          if (d.errH <= 1) { streak++; if (streak >= STREAK_TARGET) mastered = true; }
          else { streak = 0; }
          el.sr.textContent = 'Checked. You predicted ' + f1(d.predV1) + ' volts and ' +
            f1(d.predV2) + ' volts. The true split is ' + f1(d.v1) + ' volts across ' + c.r1 +
            ' ohms and ' + f1(d.v2) + ' volts across ' + c.r2 + ' ohms, with ' + f1(d.i) +
            ' amps at every point of the loop.';
        } else {
          newChallenge();
          el.sr.textContent = 'New challenge: ' + state.challenge.voltage + ' volt supply, ' +
            state.challenge.r1 + ' ohms and ' + state.challenge.r2 + ' ohms.';
        }
        render();
      });
      el.fresh.addEventListener('click', function () {
        newChallenge();
        el.sr.textContent = 'New challenge: ' + state.challenge.voltage + ' volt supply, ' +
          state.challenge.r1 + ' ohms and ' + state.challenge.r2 + ' ohms.';
        render();
      });
      el.sliders.addEventListener('input', function (e) {
        var k = e.target.getAttribute('data-key');
        if (!k) return;
        state[k] = parseInt(e.target.value, 10);
        render();
      });
      Array.prototype.forEach.call(el.modes, function (b) {
        b.addEventListener('click', function () {
          state.mode = b.getAttribute('data-mode');
          Array.prototype.forEach.call(el.modes, function (x) {
            var on = x === b;
            x.classList.toggle('on', on);
            x.setAttribute('aria-pressed', on ? 'true' : 'false');
          });
          render();
        });
      });

      /* ---------- width-driven layout (container, not viewport) ---------- */
      function applyWidth() {
        root.classList.toggle('narrow', root.getBoundingClientRect().width < 560);
      }
      if (window.ResizeObserver) new ResizeObserver(applyWidth).observe(root);
      applyWidth();

      render();
      placeDots();
      startLoop();
      /* the track may not be measurable until layout settles */
      requestAnimationFrame(function () { placeDots(); });
    }
  };
})();
