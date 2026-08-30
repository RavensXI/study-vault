/* ============================================================
   curve-movement-vs-shift

   One diagram model, two markets. Demand (a corner shop's chocolate
   bars) and supply (a town's bakeries) are DATA for the same mechanism,
   so the widget is built once and reused.

   The idea it exists to break: "price falls, so demand increases".
   A change in the good's OWN price slides the point along the existing
   curve. Only a non-price factor moves the whole curve to a new place.

   The trap it deliberately sets: a price that is not this good's price
   (a rival bar's price, the price of flour) still shifts the curve.

   Every figure printed anywhere comes from qAt(), the same function that
   draws the lines, so the reveal cannot contradict the marking.
   ============================================================ */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';

  /* plot box inside the 340 x 168 viewBox */
  var X0 = 46, X1 = 322, Y0 = 12, Y1 = 132;

  /* ---------- the two markets --------------------------------------
     Q = a + b*P.  A non-price factor moves the whole schedule by
     `shift` units.  cmin/cmax are the prices the drawn segment spans,
     kept inside the axis range so a shifted curve still fits.        */
  var MARKETS = {
    d: {
      key: 'd', kicker: 'Demand', name: 'demand', tag: 'D', up: false,
      good: 'bar', unit: 'bars a week', seller: 'shop', verb: 'sells',
      wants: 'wanted',
      ctx: 'A corner shop sells 400 chocolate bars a week at £1.00. Predict what each change does to the diagram.',
      axisQ: 'Quantity demanded (bars per week)',
      aria: 'Demand diagram: price against quantity demanded per week.',
      a: 800, b: -400, shift: 150,
      pNow: 1.00, pUp: 1.20, pDown: 0.80,
      pmin: 0.40, pmax: 1.60, qmax: 800,
      cmin: 0.50, cmax: 1.55,
      pticks: [0.60, 1.00, 1.40], qticks: [200, 400, 600],
      legendEnd: true
    },
    s: {
      key: 's', kicker: 'Supply', name: 'supply', tag: 'S', up: true,
      good: 'loaf', unit: 'loaves a week', seller: 'bakeries', verb: 'supply',
      wants: 'offered',
      ctx: 'A town’s bakeries supply 300 loaves a week at £3.00. Predict what each change does to the diagram.',
      axisQ: 'Quantity supplied (loaves per week)',
      aria: 'Supply diagram: price against quantity supplied per week.',
      a: -300, b: 200, shift: 120,
      pNow: 3.00, pUp: 3.50, pDown: 2.50,
      pmin: 2.20, pmax: 3.90, qmax: 640,
      cmin: 2.30, cmax: 3.80,
      pticks: [2.50, 3.00, 3.50], qticks: [200, 400, 600],
      legendEnd: false
    }
  };

  /* ---------- the events -------------------------------------------
     kind 'own'   : the good's OWN price changed   -> movement along
     kind 'trap'  : a price changed, but not this good's -> shift
     kind 'other' : a non-price factor changed     -> shift          */
  var EVENTS = {
    'd:own-up': {
      m: 'd', kind: 'own', ans: 'up', price: 1.20,
      text: 'The shop puts the bar up from £1.00 to £1.20.',
      why: 'Only the position on D1 changed. The curve itself has not moved.'
    },
    'd:own-down': {
      m: 'd', kind: 'own', ans: 'down', price: 0.80,
      text: 'A weekend offer cuts the bar from £1.00 to 80p.',
      why: 'More is bought because the bar is cheaper, not because demand itself grew.'
    },
    'd:rival-cut': {
      m: 'd', kind: 'trap', ans: 'left',
      text: 'A rival bar on the next shelf is cut to 60p.',
      why: 'The price that fell belongs to a substitute, not to this bar.'
    },
    'd:rival-up': {
      m: 'd', kind: 'trap', ans: 'right',
      text: 'The rival bar on the next shelf goes up to £1.40.',
      why: 'Shoppers switch across from the dearer rival. This bar’s price never moved.'
    },
    'd:health': {
      m: 'd', kind: 'other', ans: 'left',
      text: 'A health campaign turns shoppers against chocolate.',
      why: 'Tastes are a non-price factor, so the whole schedule falls.'
    },
    'd:advert': {
      m: 'd', kind: 'other', ans: 'right',
      text: 'The maker starts a TV advertising campaign for the bar.',
      why: 'Advertising changes tastes, not the price on the shelf.'
    },
    'd:income': {
      m: 'd', kind: 'other', ans: 'right',
      text: 'A pay rise leaves shoppers in the town with more to spend.',
      why: 'Higher income lifts demand at every price. The bar still costs £1.00.'
    },
    'd:slump': {
      m: 'd', kind: 'other', ans: 'left',
      text: 'A large local employer closes and household incomes fall.',
      why: 'Lower income cuts demand at every price. The bar still costs £1.00.'
    },
    's:own-up': {
      m: 's', kind: 'own', ans: 'up', price: 3.50,
      text: 'The price of a loaf rises from £3.00 to £3.50.',
      why: 'Baking more is worth it at £3.50, so the point climbs S1. The curve stays put.'
    },
    's:own-down': {
      m: 's', kind: 'own', ans: 'down', price: 2.50,
      text: 'The price of a loaf falls from £3.00 to £2.50.',
      why: 'Fewer loaves are worth baking at £2.50, but S1 itself is unchanged.'
    },
    's:flour-up': {
      m: 's', kind: 'trap', ans: 'left',
      text: 'The price of flour jumps by a third.',
      why: 'Flour is an input cost. The price that rose is not the loaf’s own price.'
    },
    's:flour-down': {
      m: 's', kind: 'trap', ans: 'right',
      text: 'A good harvest sends the price of flour down.',
      why: 'Cheaper flour makes every loaf more profitable, whatever the loaf sells for.'
    },
    's:ovens': {
      m: 's', kind: 'other', ans: 'right',
      text: 'The bakeries fit faster ovens that bake more in a shift.',
      why: 'Better technology lifts output without the loaf’s price changing.'
    },
    's:entry': {
      m: 's', kind: 'other', ans: 'right',
      text: 'Two more bakeries open in the town.',
      why: 'More firms means more loaves offered at every price.'
    },
    's:exit': {
      m: 's', kind: 'other', ans: 'left',
      text: 'The town’s largest bakery shuts down.',
      why: 'Fewer firms means fewer loaves offered at every price.'
    },
    's:rules': {
      m: 's', kind: 'other', ans: 'left',
      text: 'New hygiene rules add an extra check to every batch.',
      why: 'The check costs time on each batch, so output falls at any price.'
    }
  };

  var GROUPS = {
    d: {
      own: ['own-up', 'own-down'],
      trap: ['rival-cut', 'rival-up'],
      other: ['health', 'advert', 'income', 'slump']
    },
    s: {
      own: ['own-up', 'own-down'],
      trap: ['flour-up', 'flour-down'],
      other: ['ovens', 'entry', 'exit', 'rules']
    }
  };

  /* Markets alternate; the price-that-is-not-this-price trap lands in
     round three, before three in a row can be reached. */
  var PLAN = [
    { m: 'd', g: 'own' }, { m: 's', g: 'other' },
    { m: 'd', g: 'trap' }, { m: 's', g: 'own' },
    { m: 'd', g: 'other' }, { m: 's', g: 'trap' },
    { m: 'd', g: 'own' }, { m: 's', g: 'other' }
  ];

  var ANSWERS = [
    { key: 'up', main: 'Move up the curve', echo: 'movement along, up the curve' },
    { key: 'down', main: 'Move down the curve', echo: 'movement along, down the curve' },
    { key: 'left', main: 'Whole curve shifts left', echo: 'the whole curve shifts left' },
    { key: 'right', main: 'Whole curve shifts right', echo: 'the whole curve shifts right' }
  ];

  /* sub-labels are market data: the same four moves, different consequence */
  var SUBS = {
    d: { up: 'same curve, fewer bars', down: 'same curve, more bars',
         left: 'fewer at every price', right: 'more at every price' },
    s: { up: 'same curve, more loaves', down: 'same curve, fewer loaves',
         left: 'fewer at every price', right: 'more at every price' }
  };

  var MASTERY = 'A change in the good’s own price moves the point along the curve. '
    + 'Everything else — incomes, tastes, input costs, technology, the number of firms — moves the whole curve.';

  var CSS = [
    '.svw-cms{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45;max-width:640px;margin:0 auto}',
    '.svw-cms *{box-sizing:border-box}',
    '.svw-cms .cms-kicker{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .15rem}',
    '.svw-cms .cms-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.15rem;line-height:1.2;margin:0 0 .28rem}',
    '.svw-cms .cms-ctx{font-size:.8rem;line-height:1.45;color:#5b564e;margin:0 0 .22rem}',
    '.svw-cms .cms-ev{font-size:.92rem;line-height:1.42;font-weight:600;margin:0 0 .48rem}',
    '.svw-cms .cms-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.3rem .25rem .05rem;margin:0 0 .5rem}',
    '.svw-cms .cms-svg{display:block;width:100%;height:148px}',
    '.svw-cms .cms-answers{display:grid;grid-template-columns:repeat(2,1fr);gap:.38rem;margin:0 0 .45rem;padding:0}',
    '.svw-cms .cms-ans{display:block;width:100%;text-align:left;font-family:inherit;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.4rem .5rem;cursor:pointer}',
    '.svw-cms .cms-ans:focus-visible{outline:2px solid #2d2a26;outline-offset:2px}',
    '.svw-cms .cms-ans-main{display:block;font-size:.79rem;font-weight:600;line-height:1.25}',
    '.svw-cms .cms-ans-sub{display:block;font-size:.7rem;color:#8d8880;line-height:1.25;margin-top:.05rem}',
    '.svw-cms .cms-ans[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-cms .cms-ans[aria-pressed="true"] .cms-ans-sub{color:#cfc9bf}',
    '.svw-cms .cms-ans[data-mark="right"]{background:#fff;border-color:#4f7d63;border-width:2px;color:#3f6650}',
    '.svw-cms .cms-ans[data-mark="right"] .cms-ans-sub{color:#4f7d63}',
    '.svw-cms .cms-ans[data-mark="picked"]{background:#fff;border-style:dashed;border-color:#b3aa9c;color:#7a736a}',
    '.svw-cms .cms-ans[data-mark="picked"] .cms-ans-sub{color:#a39b8f}',
    '.svw-cms .cms-ans[disabled]{cursor:default}',
    '.svw-cms .cms-go{display:flex;align-items:center;gap:.5rem;margin:0 0 .4rem}',
    '.svw-cms .cms-streak{flex:1 1 auto;min-width:0;font-size:.74rem;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svw-cms .cms-btn{flex:0 0 auto;font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-cms .cms-btn[disabled]{background:#faf8f5;border-color:#ddd7cd;color:#a39b8f;cursor:default}',
    '.svw-cms .cms-btn:focus-visible{outline:2px solid #2d2a26;outline-offset:2px}',
    '.svw-cms .cms-cap{font-size:.84rem;line-height:1.5;margin:0;min-height:76px;color:#2d2a26}',
    '.svw-cms .cms-verdict{font-weight:700}',
    '.svw-cms .cms-verdict[data-v="right"]{color:#4f7d63}',
    '.svw-cms .cms-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}'
  ].join('');

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function svg(tag, attrs) {
    var n = document.createElementNS(NS, tag), k;
    for (k in attrs) {
      if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
    }
    return n;
  }

  function qAt(m, p, shift) { return m.a + m.b * p + (shift || 0); }
  function X(m, q) { return X0 + (q / m.qmax) * (X1 - X0); }
  function Y(m, p) { return Y1 - ((p - m.pmin) / (m.pmax - m.pmin)) * (Y1 - Y0); }
  function money(p) { return p < 1 ? Math.round(p * 100) + 'p' : '£' + p.toFixed(2); }
  function qs(m, p, shift) { return Math.round(qAt(m, p, shift)); }

  function shuffled(list) {
    var a = list.slice(), i, j, t;
    for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1));
      t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /* Every sentence about a number is generated from the model above. */
  function truthOf(ev) {
    var m = MARKETS[ev.m];
    var q0 = qs(m, m.pNow, 0);
    if (ev.kind === 'own') {
      return 'The point slides ' + (ev.ans === 'up' ? 'up' : 'down') + ' the same curve — '
        + q0 + ' ' + m.unit + ' become ' + qs(m, ev.price, 0) + '.';
    }
    var sh = (ev.ans === 'right') ? m.shift : -m.shift;
    return 'At the same ' + money(m.pNow) + ' the ' + m.seller + ' now ' + m.verb + ' '
      + qs(m, m.pNow, sh) + ', not ' + q0 + ' — the whole curve moves ' + ev.ans
      + ' to ' + m.tag + '2.';
  }

  function testOf(ev) {
    var m = MARKETS[ev.m];
    if (ev.kind === 'own') {
      return 'The ' + m.good + '’s own price changed, and that always moves the point along the curve.';
    }
    if (ev.kind === 'trap') {
      return 'A price did change — but not the ' + m.good + '’s own price, so the whole curve moves.';
    }
    return 'The ' + m.good + '’s own price never changed, so the curve itself had to move.';
  }

  function openingOf(m) {
    return 'The marked point sits on ' + m.name + ' curve ' + m.tag + '1: ' + qs(m, m.pNow, 0)
      + ' ' + m.unit + ' at ' + money(m.pNow) + '. Every point on ' + m.tag
      + '1 pairs a price with the quantity ' + m.wants + ' at that price.';
  }

  window.SVWidget = {
    meta: {
      id: 'curve-movement-vs-shift',
      title: 'Movement or shift?',
      teaches: 'A change in the good’s own price moves the point along the demand or supply curve; only a non-price factor shifts the whole curve.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;
      var GREY = '#a39b8f';

      var wrap = el('div', 'svw-cms');
      var style = document.createElement('style');
      style.textContent = CSS;
      wrap.appendChild(style);
      root.appendChild(wrap);

      /* accent read from our own node, per the house rule */
      try {
        var own = getComputedStyle(wrap).getPropertyValue('--accent');
        if (own && own.trim()) accent = own.trim();
      } catch (e) { /* keep ctx.accent */ }

      /* ---------- zone 1: title + task frame ---------- */
      var kicker = el('p', 'cms-kicker', 'Demand');
      kicker.style.color = accent;
      wrap.appendChild(kicker);
      wrap.appendChild(el('h3', 'cms-title', 'Movement or shift?'));
      var ctxLine = el('p', 'cms-ctx', MARKETS.d.ctx);
      wrap.appendChild(ctxLine);
      var evLine = el('p', 'cms-ev', '');
      wrap.appendChild(evLine);

      /* ---------- zone 2: the stage ---------- */
      var stage = el('div', 'cms-stage');
      var s = svg('svg', {
        'class': 'cms-svg', viewBox: '0 0 340 168',
        preserveAspectRatio: 'xMidYMid meet', role: 'img',
        'aria-label': MARKETS.d.aria
      });
      stage.appendChild(s);
      wrap.appendChild(stage);

      s.appendChild(svg('line', { x1: X0, y1: Y0 - 4, x2: X0, y2: Y1, stroke: '#b3aa9c', 'stroke-width': 1 }));
      s.appendChild(svg('line', { x1: X0, y1: Y1, x2: X1 + 6, y2: Y1, stroke: '#b3aa9c', 'stroke-width': 1 }));

      function tick(anchor) {
        return svg('text', {
          x: 0, y: 0, 'text-anchor': anchor, fill: '#8d8880',
          'font-size': '10', 'font-family': 'Inter, system-ui, sans-serif'
        });
      }
      var pTickT = [], pTickL = [], qTickT = [], qTickL = [], i;
      for (i = 0; i < 3; i++) {
        pTickT.push(tick('end'));
        pTickL.push(svg('line', { stroke: '#c9c2b6', 'stroke-width': 1 }));
        qTickT.push(tick('middle'));
        qTickL.push(svg('line', { stroke: '#c9c2b6', 'stroke-width': 1 }));
        s.appendChild(pTickL[i]); s.appendChild(pTickT[i]);
        s.appendChild(qTickL[i]); s.appendChild(qTickT[i]);
      }
      var qTitle = tick('middle');
      qTitle.setAttribute('x', (X0 + X1) / 2);
      qTitle.setAttribute('y', 164);
      s.appendChild(qTitle);
      var pTitle = svg('text', {
        x: 11, y: (Y0 + Y1) / 2, fill: '#8d8880', 'font-size': '10',
        'text-anchor': 'middle', 'font-family': 'Inter, system-ui, sans-serif',
        transform: 'rotate(-90 11 ' + ((Y0 + Y1) / 2) + ')'
      });
      pTitle.textContent = 'Price (£)';
      s.appendChild(pTitle);

      var guideH = svg('line', { stroke: '#c9c2b6', 'stroke-width': 1, 'stroke-dasharray': '3 3' });
      var guideV = svg('line', { stroke: '#c9c2b6', 'stroke-width': 1, 'stroke-dasharray': '3 3' });
      s.appendChild(guideH); s.appendChild(guideV);

      /* the curve the student's wrong answer would have produced */
      var wrongCurve = svg('line', {
        stroke: GREY, 'stroke-width': 1.6, 'stroke-dasharray': '5 4',
        'stroke-linecap': 'round', opacity: '0'
      });
      s.appendChild(wrongCurve);

      var c1 = svg('line', { stroke: '#2d2a26', 'stroke-width': 2, 'stroke-linecap': 'round' });
      var c2 = svg('line', { stroke: accent, 'stroke-width': 2, 'stroke-linecap': 'round', opacity: '0' });
      s.appendChild(c1); s.appendChild(c2);

      /* a paper-coloured halo so a label stays readable where a dashed
         line runs behind it */
      var HALO = { stroke: '#faf8f5', 'stroke-width': '3', 'paint-order': 'stroke', 'stroke-linejoin': 'round' };
      function halo(node) {
        var k; for (k in HALO) { if (Object.prototype.hasOwnProperty.call(HALO, k)) node.setAttribute(k, HALO[k]); }
        return node;
      }
      function curveLabel(fill) {
        return halo(svg('text', {
          x: 0, y: 0, 'text-anchor': 'start', fill: fill, 'font-size': '10.5',
          'font-weight': '700', 'font-family': 'Inter, system-ui, sans-serif'
        }));
      }
      var lab1 = curveLabel('#2d2a26');
      var lab2 = curveLabel(accent);
      lab2.setAttribute('opacity', '0');
      s.appendChild(lab1); s.appendChild(lab2);

      /* legend, shown only when a wrong answer is marked on the diagram */
      var legend = svg('g', { opacity: '0' });
      var legLine = svg('line', { stroke: GREY, 'stroke-width': 1.6, 'stroke-dasharray': '5 4' });
      var legDot = svg('circle', { r: 3.8, fill: 'none', stroke: GREY, 'stroke-width': 1.6, 'stroke-dasharray': '3 2.4', opacity: '0' });
      var legText = svg('text', {
        y: 21, fill: '#8d8880', 'font-size': '9.5',
        'font-family': 'Inter, system-ui, sans-serif'
      });
      legText.textContent = 'your answer';
      legend.appendChild(legLine); legend.appendChild(legDot); legend.appendChild(legText);
      s.appendChild(legend);

      /* the point the student's wrong answer would have produced */
      var wrongDot = svg('circle', { r: 4.2, fill: 'none', stroke: GREY, 'stroke-width': 1.6, 'stroke-dasharray': '3 2.4', opacity: '0' });

      var ghost = svg('circle', { r: 3.4, fill: 'none', stroke: '#b3aa9c', 'stroke-width': 1.2, opacity: '0' });
      var trail = svg('line', { stroke: '#b3aa9c', 'stroke-width': 1, 'stroke-dasharray': '2 3', opacity: '0' });
      var dot = svg('circle', { r: 4.2, fill: accent });
      var dotLab = halo(svg('text', {
        fill: '#2d2a26', 'font-size': '10.5', 'font-weight': '600',
        'text-anchor': 'start', 'font-family': 'Inter, system-ui, sans-serif',
        style: 'font-variant-numeric:tabular-nums'
      }));
      s.appendChild(trail); s.appendChild(ghost); s.appendChild(wrongDot);
      s.appendChild(dot); s.appendChild(dotLab);

      /* ---------- zone 3: answers + commit ---------- */
      var answers = el('div', 'cms-answers');
      var btns = {}, subs = {};
      ANSWERS.forEach(function (a) {
        var b = el('button', 'cms-ans');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        b.appendChild(el('span', 'cms-ans-main', a.main));
        var sub = el('span', 'cms-ans-sub', '');
        b.appendChild(sub);
        b.addEventListener('click', function () { pick(a.key); });
        answers.appendChild(b);
        btns[a.key] = b;
        subs[a.key] = sub;
      });
      wrap.appendChild(answers);

      var go = el('div', 'cms-go');
      var streak = el('span', 'cms-streak', '');
      var commit = el('button', 'cms-btn', 'Check');
      commit.type = 'button';
      commit.disabled = true;
      go.appendChild(streak); go.appendChild(commit);
      wrap.appendChild(go);

      /* ---------- zone 4: the caption ---------- */
      var cap = el('p', 'cms-cap');
      cap.setAttribute('aria-live', 'polite');
      wrap.appendChild(cap);
      var sr = el('p', 'cms-sr');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      /* ---------- state ---------- */
      var st = {
        deck: buildDeck(true), i: 0, id: null, m: MARKETS.d,
        choice: null, committed: false,
        streak: 0, attempted: 0, mastered: false
      };
      var raf = null;
      var labelSide = 'right';

      function buildDeck(first) {
        var pools = {
          d: { own: shuffled(GROUPS.d.own), trap: shuffled(GROUPS.d.trap), other: shuffled(GROUPS.d.other) },
          s: { own: shuffled(GROUPS.s.own), trap: shuffled(GROUPS.s.trap), other: shuffled(GROUPS.s.other) }
        };
        /* the very first round is the headline misconception: the shop
           drops the price, so does "demand" rise? */
        if (first) pools.d.own = ['own-down', 'own-up'];
        var deck = [], k;
        for (k = 0; k < PLAN.length; k++) {
          deck.push(PLAN[k].m + ':' + pools[PLAN[k].m][PLAN[k].g].shift());
        }
        return deck;
      }

      function publish(correct) {
        var ev = EVENTS[st.id] || {};
        root.dataset.svState = JSON.stringify({
          streak: st.streak, mastered: st.mastered, attempted: st.attempted,
          market: st.m.key, event: st.id, kind: ev.kind || null,
          choice: st.choice,
          correct: (correct === undefined ? null : correct)
        });
      }

      function stop() { if (raf) { cancelAnimationFrame(raf); raf = null; } }
      function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

      function curvePts(m, shift) {
        return {
          xa: X(m, qAt(m, m.cmax, shift)), ya: Y(m, m.cmax),
          xb: X(m, qAt(m, m.cmin, shift)), yb: Y(m, m.cmin)
        };
      }

      function setCurve(line, label, m, shift) {
        var p = curvePts(m, shift);
        line.setAttribute('x1', p.xa); line.setAttribute('y1', p.ya);
        line.setAttribute('x2', p.xb); line.setAttribute('y2', p.yb);
        if (label) {
          var rx = (p.xa > p.xb) ? p.xa : p.xb;
          var ry = (p.xa > p.xb) ? p.ya : p.yb;
          label.setAttribute('x', rx + 5);
          label.setAttribute('y', ry + 3.5);
        }
      }

      function setPoint(m, p, q) {
        var x = X(m, q), y = Y(m, p);
        dot.setAttribute('cx', x); dot.setAttribute('cy', y);
        guideH.setAttribute('x1', X0); guideH.setAttribute('x2', x);
        guideH.setAttribute('y1', y); guideH.setAttribute('y2', y);
        guideV.setAttribute('x1', x); guideV.setAttribute('x2', x);
        guideV.setAttribute('y1', y); guideV.setAttribute('y2', Y1);
        trail.setAttribute('x2', x); trail.setAttribute('y2', y);
        if (m.up) {
          /* below-right of an upward-sloping curve is always empty */
          dotLab.setAttribute('text-anchor', 'start');
          dotLab.setAttribute('x', Math.min(x + 9, X1 - 56));
          dotLab.setAttribute('y', y + 13);
        } else if (labelSide === 'left') {
          dotLab.setAttribute('text-anchor', 'end');
          dotLab.setAttribute('x', Math.max(x - 9, X0 + 48));
          dotLab.setAttribute('y', y + 13);
        } else {
          dotLab.setAttribute('text-anchor', 'start');
          dotLab.setAttribute('x', Math.min(x + 9, X1 - 52));
          dotLab.setAttribute('y', y - 6);
        }
        dotLab.textContent = money(p) + ', ' + Math.round(q);
      }

      function renderMarket(m) {
        s.setAttribute('aria-label', m.aria);
        qTitle.textContent = m.axisQ;
        m.pticks.forEach(function (p, k) {
          pTickT[k].setAttribute('x', X0 - 5);
          pTickT[k].setAttribute('y', Y(m, p) + 3);
          pTickT[k].textContent = p.toFixed(2);
          pTickL[k].setAttribute('x1', X0 - 3); pTickL[k].setAttribute('x2', X0);
          pTickL[k].setAttribute('y1', Y(m, p)); pTickL[k].setAttribute('y2', Y(m, p));
        });
        m.qticks.forEach(function (q, k) {
          qTickT[k].setAttribute('x', X(m, q));
          qTickT[k].setAttribute('y', Y1 + 11);
          qTickT[k].textContent = String(q);
          qTickL[k].setAttribute('x1', X(m, q)); qTickL[k].setAttribute('x2', X(m, q));
          qTickL[k].setAttribute('y1', Y1); qTickL[k].setAttribute('y2', Y1 + 3);
        });
        lab1.textContent = m.tag + '1';
        lab2.textContent = m.tag + '2';
        var lx = m.legendEnd ? X1 : X0 + 22;
        legText.setAttribute('x', lx);
        legText.setAttribute('text-anchor', m.legendEnd ? 'end' : 'start');
        var ll = m.legendEnd ? X1 - 71 : X0 + 4;
        legLine.setAttribute('x1', ll); legLine.setAttribute('x2', ll + 14);
        legLine.setAttribute('y1', 17.5); legLine.setAttribute('y2', 17.5);
        legDot.setAttribute('cx', ll + 7); legDot.setAttribute('cy', 17.5);
      }

      function resetStage(m) {
        stop();
        labelSide = 'right';
        c1.setAttribute('stroke', '#2d2a26');
        c2.setAttribute('opacity', '0');
        lab2.setAttribute('opacity', '0');
        ghost.setAttribute('opacity', '0');
        trail.setAttribute('opacity', '0');
        wrongCurve.setAttribute('opacity', '0');
        wrongDot.setAttribute('opacity', '0');
        legend.setAttribute('opacity', '0');
        setCurve(c1, lab1, m, 0);
        setCurve(c2, lab2, m, 0);
        ghost.setAttribute('cx', X(m, qAt(m, m.pNow, 0)));
        ghost.setAttribute('cy', Y(m, m.pNow));
        trail.setAttribute('x1', X(m, qAt(m, m.pNow, 0)));
        trail.setAttribute('y1', Y(m, m.pNow));
        setPoint(m, m.pNow, qAt(m, m.pNow, 0));
      }

      function play(apply) {
        if (reduced) { apply(1); return; }
        var t0 = null, DUR = 750;
        stop();
        raf = requestAnimationFrame(function step(now) {
          if (t0 === null) t0 = now;
          var t = Math.min(1, (now - t0) / DUR);
          apply(ease(t));
          if (t < 1) { raf = requestAnimationFrame(step); } else { raf = null; }
        });
      }

      /* Draws what the student said, in grey, beside what actually
         happens. One model, so the two pictures cannot disagree. */
      function markWrong(m, ev, choice) {
        if (choice === 'left' || choice === 'right') {
          setCurve(wrongCurve, null, m, choice === 'right' ? m.shift : -m.shift);
          wrongCurve.setAttribute('opacity', '1');
          legLine.setAttribute('opacity', '1');
          legDot.setAttribute('opacity', '0');
        } else {
          var p = (choice === 'up') ? m.pUp : m.pDown;
          wrongDot.setAttribute('cx', X(m, qAt(m, p, 0)));
          wrongDot.setAttribute('cy', Y(m, p));
          wrongDot.setAttribute('opacity', '1');
          legLine.setAttribute('opacity', '0');
          legDot.setAttribute('opacity', '1');
        }
        legend.setAttribute('opacity', '1');
      }

      function animate(m, ev) {
        ghost.setAttribute('opacity', '1');
        trail.setAttribute('opacity', '1');
        if (ev.kind === 'own') {
          var p1 = ev.price;
          play(function (e) {
            var p = m.pNow + (p1 - m.pNow) * e;
            setPoint(m, p, qAt(m, p, 0));
          });
        } else {
          var target = (ev.ans === 'right') ? m.shift : -m.shift;
          labelSide = (ev.ans === 'left') ? 'left' : 'right';
          c2.setAttribute('opacity', '1');
          lab2.setAttribute('opacity', '1');
          c1.setAttribute('stroke', '#c9c2b6');
          play(function (e) {
            var sh = target * e;
            setCurve(c2, lab2, m, sh);
            setPoint(m, m.pNow, qAt(m, m.pNow, sh));
          });
        }
      }

      function say(verdict, vkind, body) {
        cap.textContent = '';
        var v = el('span', 'cms-verdict', verdict);
        v.setAttribute('data-v', vkind);
        cap.appendChild(v);
        cap.appendChild(document.createTextNode(' ' + body));
        sr.textContent = verdict + ' ' + body;
      }

      function showStreak() {
        if (st.mastered) { streak.textContent = 'You have it — keep going if you like.'; return; }
        if (st.streak === 1) { streak.textContent = '1 right in a row — two more to go.'; }
        else if (st.streak === 2) { streak.textContent = '2 right in a row — one more to go.'; }
        else { streak.textContent = ''; }
      }

      function pick(key) {
        if (st.committed) return;
        st.choice = key;
        ANSWERS.forEach(function (a) {
          btns[a.key].setAttribute('aria-pressed', a.key === key ? 'true' : 'false');
        });
        commit.disabled = false;
        publish();
      }

      function echoOf(key) {
        var found = null;
        ANSWERS.forEach(function (a) { if (a.key === key) found = a.echo; });
        return found;
      }

      function check() {
        var ev = EVENTS[st.id], m = st.m;
        var right = (st.choice === ev.ans);
        st.committed = true;
        st.attempted += 1;
        st.streak = right ? st.streak + 1 : 0;
        var justMastered = false;
        if (right && st.streak >= 3 && !st.mastered) { st.mastered = true; justMastered = true; }

        ANSWERS.forEach(function (a) {
          var b = btns[a.key];
          b.disabled = true;
          b.setAttribute('aria-pressed', 'false');
          if (a.key === ev.ans) b.setAttribute('data-mark', 'right');
          else if (a.key === st.choice) b.setAttribute('data-mark', 'picked');
        });

        if (!right) markWrong(m, ev, st.choice);
        animate(m, ev);

        if (justMastered) {
          say('Three in a row — you have it.', 'right', MASTERY);
        } else if (right) {
          say('Right —', 'right', echoOf(st.choice) + '. ' + truthOf(ev) + ' ' + ev.why);
        } else {
          say('Not quite —', 'wrong', 'you chose ' + echoOf(st.choice) + '. '
            + truthOf(ev) + ' ' + testOf(ev));
        }

        showStreak();
        commit.textContent = st.mastered ? 'Another anyway' : 'Next change';
        publish(right);
      }

      function nextRound() {
        if (st.i >= st.deck.length) { st.deck = buildDeck(false); st.i = 0; }
        st.id = st.deck[st.i]; st.i += 1;
        var ev = EVENTS[st.id];
        var m = MARKETS[ev.m];
        st.m = m;
        st.choice = null;
        st.committed = false;

        kicker.textContent = m.kicker;
        ctxLine.textContent = m.ctx;
        evLine.textContent = ev.text;
        renderMarket(m);
        resetStage(m);

        ANSWERS.forEach(function (a) {
          var b = btns[a.key];
          b.disabled = false;
          b.removeAttribute('data-mark');
          b.setAttribute('aria-pressed', 'false');
          subs[a.key].textContent = SUBS[m.key][a.key];
        });

        commit.textContent = 'Check';
        commit.disabled = true;
        cap.textContent = openingOf(m);
        sr.textContent = '';
        showStreak();
        publish();
      }

      commit.addEventListener('click', function () {
        if (st.committed) { nextRound(); commit.focus(); }
        else if (st.choice) { check(); }
      });

      wrap.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !st.committed && st.choice) {
          st.choice = null;
          ANSWERS.forEach(function (a) { btns[a.key].setAttribute('aria-pressed', 'false'); });
          commit.disabled = true;
          publish();
        }
      });

      nextRound();
    }
  };
})();
