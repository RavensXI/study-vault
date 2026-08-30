/* ============================================================
   demand-curve-movement-vs-shift

   One demand diagram, one rotating event, four committable answers:
   move up the curve, move down the curve, shift left, shift right.

   The idea it exists to break: "any change shifts the curve".
   The trap it deliberately sets: a RIVAL bar's price change is still a
   price change - but it is not THIS good's price, so it shifts.

   Everything the feedback says is derived from the same model that
   draws the diagram: Q = 800 - 400P, shift = +/- 150 bars.
   ============================================================ */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';

  /* ---------- the model ------------------------------------------------
     Demand schedule for one chocolate bar in one corner shop.
     Q = 800 - 400P  ->  at £1.00, 400 a week; £1.20, 320; 80p, 480.
     A non-price factor moves the whole schedule by 150 bars a week.
     Every figure printed anywhere in this widget comes from qAt().      */
  var P_NOW = 1.00;
  var SHIFT = 150;
  var PMIN = 0.40, PMAX = 1.60, QMAX = 800;
  /* the drawn segment stops short of the axis range so that a shifted
     curve and its label still fit inside the plot */
  var CMIN = 0.50, CMAX = 1.55;

  function qAt(p, shift) { return 800 - 400 * p + (shift || 0); }

  /* plot box inside the 340 x 168 viewBox */
  var X0 = 46, X1 = 322, Y0 = 12, Y1 = 132;
  function X(q) { return X0 + (q / QMAX) * (X1 - X0); }
  function Y(p) { return Y1 - ((p - PMIN) / (PMAX - PMIN)) * (Y1 - Y0); }

  function money(p) {
    return p < 1 ? Math.round(p * 100) + 'p' : '£' + p.toFixed(2);
  }

  /* ---------- the events ----------------------------------------------
     kind 'own'   : the good's OWN price changed -> movement along
     kind 'other' : something else changed       -> the curve shifts     */
  var EVENTS = {
    'own-up': {
      kind: 'own', ans: 'up', price: 1.20,
      text: 'The shop puts the bar up from £1.00 to £1.20.',
      truth: 'The point slides up the same curve — 400 bars a week become 320.',
      why: 'Only the position on the curve changed; the curve is still D1.'
    },
    'own-down': {
      kind: 'own', ans: 'down', price: 0.80,
      text: 'A weekend offer cuts the bar from £1.00 to 80p.',
      truth: 'The point slides down the same curve — 400 bars a week become 480.',
      why: 'More is bought because the bar is cheaper, not because demand itself grew.'
    },
    'rival-cut': {
      kind: 'other', ans: 'left',
      text: 'A rival bar on the next shelf is cut from £1.00 to 60p.',
      truth: 'At the same £1.00 the shop now sells 250, not 400 — the curve moves left to D2.',
      why: 'The price that fell belongs to a substitute, not to this bar.'
    },
    'rival-up': {
      kind: 'other', ans: 'right',
      text: 'The rival bar on the next shelf goes up to £1.40.',
      truth: 'At the same £1.00 the shop now sells 550, not 400 — the curve moves right to D2.',
      why: 'Shoppers switch across from the dearer substitute; this bar’s price never moved.'
    },
    'health': {
      kind: 'other', ans: 'left',
      text: 'A national health campaign turns shoppers against chocolate.',
      truth: 'Fewer are wanted at every price — 250 at £1.00 — so the curve moves left to D2.',
      why: 'Tastes are a non-price factor, so the whole schedule falls.'
    },
    'advert': {
      kind: 'other', ans: 'right',
      text: 'The maker starts a television advertising campaign for the bar.',
      truth: 'More are wanted at every price — 550 at £1.00 — so the curve moves right to D2.',
      why: 'Advertising changes tastes, not the price on the shelf.'
    },
    'income': {
      kind: 'other', ans: 'right',
      text: 'A pay rise leaves shoppers in the town with more to spend.',
      truth: 'At the same £1.00 the shop sells 550, not 400 — the curve moves right to D2.',
      why: 'Higher income lifts demand at every price; the bar still costs £1.00.'
    },
    'recession': {
      kind: 'other', ans: 'left',
      text: 'A large local employer closes and household incomes fall.',
      truth: 'At the same £1.00 the shop sells 250, not 400 — the curve moves left to D2.',
      why: 'Lower income cuts demand at every price; the bar still costs £1.00.'
    }
  };

  /* Deck order guarantees the tempting reversal (a DIFFERENT good's
     price) lands in round two, before mastery can be reached. */
  var PATTERN = ['own', 'rival', 'other', 'other', 'own', 'rival', 'other', 'other'];
  var GROUPS = {
    own: ['own-up', 'own-down'],
    rival: ['rival-cut', 'rival-up'],
    other: ['health', 'advert', 'income', 'recession']
  };

  var ANSWERS = [
    { key: 'up', main: 'Move up the curve', sub: 'fewer bought, same curve', echo: 'movement along, up the curve' },
    { key: 'down', main: 'Move down the curve', sub: 'more bought, same curve', echo: 'movement along, down the curve' },
    { key: 'left', main: 'Whole curve shifts left', sub: 'fewer at every price', echo: 'the whole curve shifts left' },
    { key: 'right', main: 'Whole curve shifts right', sub: 'more at every price', echo: 'the whole curve shifts right' }
  ];

  var TEST = {
    own: 'The bar’s own price changed — that is always a movement along.',
    other: 'The bar’s own price did not change, so the curve itself had to move.'
  };

  var CSS = [
    '.svw-dcms{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45}',
    '.svw-dcms *{box-sizing:border-box}',
    '.svw-dcms .dcms-kicker{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .15rem}',
    '.svw-dcms .dcms-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.15rem;line-height:1.2;margin:0 0 .3rem}',
    '.svw-dcms .dcms-ctx{font-size:.8rem;line-height:1.45;color:#5b564e;margin:0 0 .2rem}',
    '.svw-dcms .dcms-ev{font-size:.92rem;line-height:1.42;font-weight:600;margin:0 0 .5rem}',
    '.svw-dcms .dcms-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.3rem .25rem .05rem;margin:0 0 .5rem}',
    '.svw-dcms .dcms-svg{display:block;width:100%;height:148px}',
    '.svw-dcms .dcms-answers{display:grid;grid-template-columns:repeat(2,1fr);gap:.38rem;margin:0 0 .45rem;padding:0}',
    '.svw-dcms .dcms-ans{display:block;width:100%;text-align:left;font-family:inherit;color:#2d2a26;',
    'background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.4rem .5rem;cursor:pointer}',
    '.svw-dcms .dcms-ans:focus-visible{outline:2px solid #2d2a26;outline-offset:2px}',
    '.svw-dcms .dcms-ans-main{display:block;font-size:.79rem;font-weight:600;line-height:1.25}',
    '.svw-dcms .dcms-ans-sub{display:block;font-size:.7rem;color:#8d8880;line-height:1.25;margin-top:.05rem}',
    '.svw-dcms .dcms-ans[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-dcms .dcms-ans[aria-pressed="true"] .dcms-ans-sub{color:#cfc9bf}',
    '.svw-dcms .dcms-ans[data-mark="right"]{background:#fff;border-color:#4f7d63;border-width:2px;color:#3f6650}',
    '.svw-dcms .dcms-ans[data-mark="right"] .dcms-ans-sub{color:#4f7d63}',
    '.svw-dcms .dcms-ans[data-mark="picked"]{background:#fff;border-style:dashed;border-color:#b3aa9c;color:#7a736a}',
    '.svw-dcms .dcms-ans[data-mark="picked"] .dcms-ans-sub{color:#a39b8f}',
    '.svw-dcms .dcms-ans[disabled]{cursor:default}',
    '.svw-dcms .dcms-go{display:flex;align-items:center;gap:.5rem;margin:0 0 .4rem}',
    '.svw-dcms .dcms-streak{flex:1 1 auto;min-width:0;font-size:.74rem;color:#8d8880}',
    '.svw-dcms .dcms-btn{flex:0 0 auto;font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;',
    'border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-dcms .dcms-btn[disabled]{background:#faf8f5;border-color:#ddd7cd;color:#a39b8f;cursor:default}',
    '.svw-dcms .dcms-btn:focus-visible{outline:2px solid #2d2a26;outline-offset:2px}',
    '.svw-dcms .dcms-cap{font-size:.84rem;line-height:1.5;margin:0;min-height:76px;color:#2d2a26}',
    '.svw-dcms .dcms-verdict{font-weight:700}',
    '.svw-dcms .dcms-verdict[data-v="right"]{color:#4f7d63}',
    '.svw-dcms .dcms-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;',
    'clip:rect(0 0 0 0);white-space:nowrap;border:0}'
  ].join('');

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function svg(tag, attrs) {
    var n = document.createElementNS(NS, tag), k;
    for (k in attrs) { if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]); }
    return n;
  }

  function shuffled(list) {
    var a = list.slice(), i, j, t;
    for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1));
      t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function buildDeck() {
    var pools = { own: shuffled(GROUPS.own), rival: shuffled(GROUPS.rival), other: shuffled(GROUPS.other) };
    var deck = [], i;
    for (i = 0; i < PATTERN.length; i++) deck.push(pools[PATTERN[i]].shift());
    return deck;
  }

  window.SVWidget = {
    meta: {
      id: 'demand-curve-movement-vs-shift',
      title: 'Movement or shift?',
      teaches: 'A change in the good’s own price moves the point along the demand curve; only non-price factors shift the whole curve.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;

      var wrap = el('div', 'svw-dcms');
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
      var kicker = el('p', 'dcms-kicker', 'Demand');
      kicker.style.color = accent;
      wrap.appendChild(kicker);
      wrap.appendChild(el('h3', 'dcms-title', 'Movement or shift?'));
      wrap.appendChild(el('p', 'dcms-ctx', 'A corner shop sells 400 of one chocolate bar a week at £1.00.'));
      var evLine = el('p', 'dcms-ev', '');
      wrap.appendChild(evLine);

      /* ---------- zone 2: the stage ---------- */
      var stage = el('div', 'dcms-stage');
      var s = svg('svg', {
        'class': 'dcms-svg', viewBox: '0 0 340 168',
        preserveAspectRatio: 'xMidYMid meet', role: 'img',
        'aria-label': 'Demand diagram: price against quantity demanded per week.'
      });
      stage.appendChild(s);
      wrap.appendChild(stage);

      /* axes */
      s.appendChild(svg('line', { x1: X0, y1: Y0 - 4, x2: X0, y2: Y1, stroke: '#b3aa9c', 'stroke-width': 1 }));
      s.appendChild(svg('line', { x1: X0, y1: Y1, x2: X1 + 6, y2: Y1, stroke: '#b3aa9c', 'stroke-width': 1 }));

      function tick(text, x, y, anchor) {
        var t = svg('text', {
          x: x, y: y, 'text-anchor': anchor, fill: '#8d8880',
          'font-size': '10', 'font-family': 'Inter, system-ui, sans-serif'
        });
        t.textContent = text;
        return t;
      }
      [0.60, 1.00, 1.40].forEach(function (p) {
        s.appendChild(tick(p.toFixed(2), X0 - 5, Y(p) + 3, 'end'));
        s.appendChild(svg('line', { x1: X0 - 3, y1: Y(p), x2: X0, y2: Y(p), stroke: '#c9c2b6', 'stroke-width': 1 }));
      });
      [200, 400, 600].forEach(function (q) {
        s.appendChild(tick(String(q), X(q), Y1 + 11, 'middle'));
        s.appendChild(svg('line', { x1: X(q), y1: Y1, x2: X(q), y2: Y1 + 3, stroke: '#c9c2b6', 'stroke-width': 1 }));
      });
      var qTitle = tick('Quantity demanded (bars per week)', (X0 + X1) / 2, 164, 'middle');
      s.appendChild(qTitle);
      var pTitle = svg('text', {
        x: 11, y: (Y0 + Y1) / 2, fill: '#8d8880', 'font-size': '10',
        'text-anchor': 'middle', 'font-family': 'Inter, system-ui, sans-serif',
        transform: 'rotate(-90 11 ' + ((Y0 + Y1) / 2) + ')'
      });
      pTitle.textContent = 'Price (£)';
      s.appendChild(pTitle);

      /* guides, curves, point */
      var guideH = svg('line', { x1: X0, y1: Y(P_NOW), x2: X(qAt(P_NOW, 0)), y2: Y(P_NOW), stroke: '#c9c2b6', 'stroke-width': 1, 'stroke-dasharray': '3 3' });
      var guideV = svg('line', { x1: X(qAt(P_NOW, 0)), y1: Y(P_NOW), x2: X(qAt(P_NOW, 0)), y2: Y1, stroke: '#c9c2b6', 'stroke-width': 1, 'stroke-dasharray': '3 3' });
      s.appendChild(guideH); s.appendChild(guideV);

      function curveLine(shift) {
        return { x1: X(qAt(CMAX, shift)), y1: Y(CMAX), x2: X(qAt(CMIN, shift)), y2: Y(CMIN) };
      }
      var c1 = curveLine(0);
      var d1 = svg('line', { x1: c1.x1, y1: c1.y1, x2: c1.x2, y2: c1.y2, stroke: '#2d2a26', 'stroke-width': 2, 'stroke-linecap': 'round' });
      var d2 = svg('line', { x1: c1.x1, y1: c1.y1, x2: c1.x2, y2: c1.y2, stroke: accent, 'stroke-width': 2, 'stroke-linecap': 'round', opacity: '0' });
      s.appendChild(d1); s.appendChild(d2);

      function curveLabel(txt, x, fill) {
        var t = svg('text', { x: x, y: Y(CMIN) - 4, 'text-anchor': 'start', fill: fill, 'font-size': '10.5', 'font-weight': '700', 'font-family': 'Inter, system-ui, sans-serif' });
        t.textContent = txt;
        return t;
      }
      var lab1 = curveLabel('D1', c1.x2 + 4, '#2d2a26');
      var lab2 = curveLabel('D2', c1.x2 + 4, accent);
      lab2.setAttribute('opacity', '0');
      s.appendChild(lab1); s.appendChild(lab2);

      var ghost = svg('circle', { cx: X(qAt(P_NOW, 0)), cy: Y(P_NOW), r: 3.4, fill: 'none', stroke: '#b3aa9c', 'stroke-width': 1.2, opacity: '0' });
      var trail = svg('line', { x1: X(qAt(P_NOW, 0)), y1: Y(P_NOW), x2: X(qAt(P_NOW, 0)), y2: Y(P_NOW), stroke: '#b3aa9c', 'stroke-width': 1, 'stroke-dasharray': '2 3', opacity: '0' });
      var dot = svg('circle', { cx: X(qAt(P_NOW, 0)), cy: Y(P_NOW), r: 4.2, fill: accent });
      var dotLab = svg('text', { x: X(qAt(P_NOW, 0)) + 9, y: Y(P_NOW) - 6, fill: '#2d2a26', 'font-size': '10.5', 'font-weight': '600', 'text-anchor': 'start', 'font-family': 'Inter, system-ui, sans-serif' });
      dotLab.textContent = '£1.00, 400';
      s.appendChild(trail); s.appendChild(ghost); s.appendChild(dot); s.appendChild(dotLab);

      /* ---------- zone 3: answers + commit ---------- */
      var answers = el('div', 'dcms-answers');
      var btns = {};
      ANSWERS.forEach(function (a) {
        var b = el('button', 'dcms-ans');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        b.appendChild(el('span', 'dcms-ans-main', a.main));
        b.appendChild(el('span', 'dcms-ans-sub', a.sub));
        b.addEventListener('click', function () { pick(a.key); });
        answers.appendChild(b);
        btns[a.key] = b;
      });
      wrap.appendChild(answers);

      var go = el('div', 'dcms-go');
      var streak = el('span', 'dcms-streak', '');
      var commit = el('button', 'dcms-btn', 'Check');
      commit.type = 'button';
      commit.disabled = true;
      go.appendChild(streak); go.appendChild(commit);
      wrap.appendChild(go);

      /* ---------- zone 4: the caption ---------- */
      var cap = el('p', 'dcms-cap');
      cap.setAttribute('aria-live', 'polite');
      wrap.appendChild(cap);
      var sr = el('p', 'dcms-sr');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      /* ---------- state ---------- */
      var st = {
        deck: buildDeck(), i: 0, id: null, choice: null,
        committed: false, streak: 0, attempted: 0, mastered: false
      };
      var raf = null;
      /* which side of the moving point its price/quantity readout sits on,
         so it never runs into the old position marker */
      var labelSide = 'right';

      function publish(correct) {
        root.dataset.svState = JSON.stringify({
          streak: st.streak, mastered: st.mastered, attempted: st.attempted,
          event: st.id, choice: st.choice,
          correct: (correct === undefined ? null : correct)
        });
      }

      function stop() { if (raf) { cancelAnimationFrame(raf); raf = null; } }

      function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

      function setPoint(p, q) {
        var x = X(q), y = Y(p);
        dot.setAttribute('cx', x); dot.setAttribute('cy', y);
        guideH.setAttribute('y1', y); guideH.setAttribute('y2', y); guideH.setAttribute('x2', x);
        guideV.setAttribute('x1', x); guideV.setAttribute('x2', x); guideV.setAttribute('y1', y);
        trail.setAttribute('x2', x); trail.setAttribute('y2', y);
        if (labelSide === 'left') {
          /* below-left: clear of both the shifted curve and the old marker */
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

      function setD2(shift) {
        var c = curveLine(shift);
        d2.setAttribute('x1', c.x1); d2.setAttribute('y1', c.y1);
        d2.setAttribute('x2', c.x2); d2.setAttribute('y2', c.y2);
        lab2.setAttribute('x', c.x2 + 4);
      }

      function resetStage() {
        stop();
        labelSide = 'right';
        d1.setAttribute('stroke', '#2d2a26');
        d2.setAttribute('opacity', '0');
        lab2.setAttribute('opacity', '0');
        ghost.setAttribute('opacity', '0');
        trail.setAttribute('opacity', '0');
        setD2(0);
        setPoint(P_NOW, qAt(P_NOW, 0));
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

      function animate(ev) {
        ghost.setAttribute('opacity', '1');
        trail.setAttribute('opacity', '1');
        if (ev.kind === 'own') {
          var p1 = ev.price;
          play(function (e) {
            var p = P_NOW + (p1 - P_NOW) * e;
            setPoint(p, qAt(p, 0));
          });
        } else {
          var target = (ev.ans === 'right') ? SHIFT : -SHIFT;
          labelSide = (ev.ans === 'right') ? 'right' : 'left';
          d2.setAttribute('opacity', '1');
          lab2.setAttribute('opacity', '1');
          d1.setAttribute('stroke', '#c9c2b6');
          play(function (e) {
            var sh = target * e;
            setD2(sh);
            setPoint(P_NOW, qAt(P_NOW, sh));
          });
        }
      }

      function say(verdict, vkind, body) {
        cap.textContent = '';
        var v = el('span', 'dcms-verdict', verdict);
        v.setAttribute('data-v', vkind);
        cap.appendChild(v);
        cap.appendChild(document.createTextNode(' ' + body));
        sr.textContent = verdict + ' ' + body;
      }

      function showStreak() {
        if (st.mastered) { streak.textContent = ''; return; }
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

      function labelOf(key) {
        var found = null;
        ANSWERS.forEach(function (a) { if (a.key === key) found = a.echo; });
        return found;
      }

      function check() {
        var ev = EVENTS[st.id];
        var right = (st.choice === ev.ans);
        st.committed = true;
        st.attempted += 1;
        st.streak = right ? st.streak + 1 : 0;
        if (right && st.streak >= 3) st.mastered = true;

        ANSWERS.forEach(function (a) {
          var b = btns[a.key];
          b.disabled = true;
          b.setAttribute('aria-pressed', 'false');
          if (a.key === ev.ans) b.setAttribute('data-mark', 'right');
          else if (a.key === st.choice) b.setAttribute('data-mark', 'picked');
        });

        animate(ev);

        if (right && st.mastered && st.streak === 3) {
          say('Three in a row — you have it.', 'right',
            'A change in the bar’s own price moves the point along the curve; income, tastes, advertising or another good’s price move the whole curve.');
        } else if (right) {
          say('Right —', 'right', labelOf(st.choice) + '. ' + ev.truth + ' ' + ev.why);
        } else {
          say('Not quite —', 'wrong', 'you chose ' + labelOf(st.choice) + '. ' + ev.truth + ' ' + TEST[ev.kind]);
        }

        showStreak();
        commit.textContent = st.mastered ? 'Another anyway' : 'Next event';
        publish(right);
      }

      function nextRound() {
        if (st.i >= st.deck.length) { st.deck = buildDeck(); st.i = 0; }
        st.id = st.deck[st.i]; st.i += 1;
        st.choice = null;
        st.committed = false;
        evLine.textContent = EVENTS[st.id].text + ' Predict what happens on the demand diagram.';
        ANSWERS.forEach(function (a) {
          var b = btns[a.key];
          b.disabled = false;
          b.removeAttribute('data-mark');
          b.setAttribute('aria-pressed', 'false');
        });
        resetStage();
        commit.textContent = 'Check';
        commit.disabled = true;
        cap.textContent = 'The marked point sits on demand curve D1: 400 bars a week at £1.00. '
          + 'Every point on D1 pairs a price with the quantity wanted at that price.';
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
