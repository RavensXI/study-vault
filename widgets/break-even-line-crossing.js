/* StudyVault lesson widget — break-even-line-crossing
   Break-even is where the total revenue line crosses the total cost line.
   Everything on screen is derived from {fixed costs, price, variable cost}. */
(function () {
  'use strict';

  /* ---------------------------------------------------------------- data ---
     Every business is chosen so fixed costs divide exactly by contribution,
     before AND after each change, so every answer is a clean integer.        */

  var BIZ = [
    {
      name: 'Bela', pn: 'she',
      trade: 'candles from a market stall',
      unit: 'candle', units: 'candles',
      fc: 1800, p: 14, vc: 8,                       /* contribution 6, BE 300 */
      outs: [300, 420, 180],
      changes: [
        { kind: 'fc', text: "Bela's stall rent rises by £600 a month.", fc: 2400 },
        { kind: 'price', text: 'Bela raises the price to £17 a candle.', p: 17 },
        { kind: 'vc', text: 'Wax costs Bela £2 more for every candle.', vc: 10 },
        { kind: 'vol', text: 'Bela sells 380 candles this month, up from 320.', from: 320, to: 380 }
      ]
    },
    {
      name: 'Rafi', pn: 'he',
      trade: 'printed phone cases online',
      unit: 'case', units: 'cases',
      fc: 2400, p: 15, vc: 7,                       /* contribution 8, BE 300 */
      outs: [375, 300, 225],
      changes: [
        { kind: 'fc', text: "Rafi's workshop rent falls by £600 a month.", fc: 1800 },
        { kind: 'price', text: 'Rafi cuts the price to £12 a case.', p: 12 },
        { kind: 'vc', text: 'Blank cases cost Rafi £2 more each.', vc: 9 },
        { kind: 'vol', text: 'A review lifts Rafi to 460 cases this month, up from 340.', from: 340, to: 460 }
      ]
    },
    {
      name: 'Dee', pn: 'she',
      trade: 'a dog-walking round',
      unit: 'walk', units: 'walks',
      fc: 900, p: 12, vc: 3,                        /* contribution 9, BE 100 */
      outs: [140, 100, 60],
      changes: [
        { kind: 'fc', text: "Dee's insurance rises by £450 a month.", fc: 1350 },
        { kind: 'price', text: 'Dee raises the price to £15 a walk.', p: 15 },
        { kind: 'vc', text: "Fuel adds £3 to the cost of each of Dee's walks.", vc: 6 },
        { kind: 'vol', text: 'Dee books 170 walks this month, up from 120.', from: 120, to: 170 }
      ]
    },
    {
      name: 'Marcus', pn: 'he',
      trade: 'printed T-shirts at events',
      unit: 'shirt', units: 'shirts',
      fc: 1200, p: 16, vc: 6,                      /* contribution 10, BE 120 */
      outs: [200, 120, 90],
      changes: [
        { kind: 'fc', text: "Marcus's pitch fee rises by £300 a month.", fc: 1500 },
        { kind: 'price', text: 'Marcus raises the price to £18 a shirt.', p: 18 },
        { kind: 'vc', text: 'Blank shirts cost Marcus £2 more each.', vc: 8 },
        { kind: 'vol', text: 'Marcus sells 210 shirts this month, up from 150.', from: 150, to: 210 }
      ]
    },
    {
      name: 'Noor', pn: 'she',
      trade: 'smoothies from a kiosk',
      unit: 'cup', units: 'cups',
      fc: 2100, p: 5, vc: 2,                        /* contribution 3, BE 700 */
      outs: [900, 700, 500],
      changes: [
        { kind: 'fc', text: "Noor's kiosk rent falls by £600 a month.", fc: 1500 },
        { kind: 'price', text: 'Noor raises the price to £7 a cup.', p: 7 },
        { kind: 'vc', text: 'Fruit costs Noor £1 more for every cup.', vc: 3 },
        { kind: 'vol', text: 'Noor sells 780 cups this month, up from 650.', from: 650, to: 780 }
      ]
    }
  ];

  var TYPES = ['be', 'pl', 'move'];

  /* ------------------------------------------------------------- helpers --- */

  function contrib(s) { return s.p - s.vc; }
  function breakEven(s) { return s.fc / (s.p - s.vc); }
  function money(n) {
    var neg = n < 0;
    var v = Math.abs(Math.round(n));
    return (neg ? '-£' : '£') + v.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }
  function shortMoney(v) {
    if (v >= 1000) {
      var k = v / 1000;
      return '£' + (k === Math.round(k) ? k : k.toFixed(1)) + 'k';
    }
    return '£' + v;
  }
  function niceUp(v) {
    var m = Math.pow(10, Math.floor(Math.log(v) / Math.LN10));
    var steps = [1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10];
    for (var i = 0; i < steps.length; i++) {
      if (steps[i] * m >= v - 1e-9) return steps[i] * m;
    }
    return 10 * m;
  }
  function shuffle(a) {
    var out = a.slice();
    for (var i = out.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = out[i]; out[i] = out[j]; out[j] = t;
    }
    return out;
  }

  /* ================================================================ mount === */

  window.SVWidget = {
    meta: {
      id: 'break-even-line-crossing',
      title: 'Where the lines cross',
      teaches: 'Break-even is the crossing of the total revenue and total cost lines; contribution sets the gap, and costs or price move the crossing.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
        ctx.accent || '#8a5a2b';
      /* ctx.reducedMotion needs nothing here: this widget never animates —
         the chart is redrawn only when the student commits or the modal resizes. */

      /* ------------------------------------------------------------ CSS --- */
      var css = [
        '.svw-bex{background:#fff;border:1px solid #e8e3db;border-radius:16px;padding:1rem;',
        'color:#2d2a26;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;box-sizing:border-box}',
        '.svw-bex *,.svw-bex *:before,.svw-bex *:after{box-sizing:border-box}',
        '@media (min-width:560px){.svw-bex{padding:1.3rem}}',
        '.svw-bex .bx-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;',
        'color:' + accent + ';margin:0 0 .12rem}',
        '.svw-bex .bx-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;',
        'line-height:1.15;margin:0 0 .3rem}',
        '.svw-bex .bx-frame{font-size:.84rem;line-height:1.45;margin:0;color:#3c3833}',
        '.svw-bex .bx-stage{margin:.55rem 0 0;background:#faf8f5;border:1px solid #efe9e0;',
        'border-radius:12px;padding:.45rem .5rem .3rem}',
        '.svw-bex .bx-figs{display:flex;gap:.3rem;margin:0 0 .25rem}',
        '.svw-bex .bx-fig{flex:1 1 0;min-width:0;text-align:center;padding:.2rem .1rem;',
        'background:#fff;border:1px solid #efe9e0;border-radius:8px}',
        '.svw-bex .bx-fig b{display:block;font-size:.92rem;font-weight:700;font-variant-numeric:tabular-nums;line-height:1.25}',
        '.svw-bex .bx-fig span{display:block;font-size:.68rem;color:#8d8880;line-height:1.2}',
        '.svw-bex .bx-plot{display:block;line-height:0}',
        '.svw-bex .bx-plot svg{display:block;width:100%;height:auto}',
        '.svw-bex .bx-ans{margin:.55rem 0 0}',
        '.svw-bex .bx-choices{display:flex;gap:.35rem}',
        '.svw-bex .bx-btn{flex:1 1 0;min-width:0;font-family:inherit;font-size:.82rem;font-weight:600;',
        'padding:.45rem .3rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;',
        'cursor:pointer;text-align:center;line-height:1.2}',
        '.svw-bex .bx-btn small{display:block;font-size:.68rem;font-weight:500;color:#8d8880;margin-top:.1rem}',
        '.svw-bex .bx-btn[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
        '.svw-bex .bx-btn[aria-pressed="true"] small{color:#e6e0d6}',
        '.svw-bex .bx-numrow{display:flex;align-items:center;gap:.4rem;font-size:.82rem;color:#5b564e;margin-top:.4rem}',
        '.svw-bex .bx-num{width:6.5rem;font-family:inherit;font-size:.95rem;font-weight:700;',
        'font-variant-numeric:tabular-nums;padding:.4rem .55rem;border:1px solid #ddd7cd;border-radius:10px;',
        'background:#fff;color:#2d2a26}',
        '.svw-bex .bx-num:focus-visible,.svw-bex .bx-btn:focus-visible,.svw-bex .bx-go:focus-visible{',
        'outline:2px solid ' + accent + ';outline-offset:2px}',
        '.svw-bex .bx-act{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin-top:.5rem}',
        '.svw-bex .bx-go{font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem 1.05rem;',
        'border:1px solid #2d2a26;border-radius:10px;background:#2d2a26;color:#fff;cursor:pointer}',
        '.svw-bex .bx-run{font-size:.76rem;color:#8d8880}',
        '.svw-bex .bx-cap{font-size:.86rem;line-height:1.5;margin:.5rem 0 0;color:#3c3833;min-height:3.1em}',
        '.svw-bex .bx-cap b{font-weight:700;color:#2d2a26}',
        '.svw-bex .bx-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);',
        'clip-path:inset(50%);white-space:nowrap}'
      ].join('');

      root.className = (root.className ? root.className + ' ' : '') + 'svw-bex';
      var style = document.createElement('style');
      style.textContent = css;
      root.appendChild(style);

      /* ------------------------------------------------------------ DOM --- */
      function el(tag, cls, html) {
        var n = document.createElement(tag);
        if (cls) n.className = cls;
        if (html != null) n.innerHTML = html;
        return n;
      }

      var head = el('div');
      head.appendChild(el('p', 'bx-kick', 'Break-even'));
      head.appendChild(el('h3', 'bx-title', 'Where the lines cross'));
      var frame = el('p', 'bx-frame', '');
      head.appendChild(frame);
      root.appendChild(head);

      var stage = el('div', 'bx-stage');
      var figs = el('div', 'bx-figs');
      var figFC = el('div', 'bx-fig', '<b></b><span>Fixed costs / month</span>');
      var figP = el('div', 'bx-fig', '<b></b><span>Selling price</span>');
      var figVC = el('div', 'bx-fig', '<b></b><span>Variable cost</span>');
      figs.appendChild(figFC); figs.appendChild(figP); figs.appendChild(figVC);
      stage.appendChild(figs);
      var plot = el('div', 'bx-plot');
      stage.appendChild(plot);
      root.appendChild(stage);

      var ans = el('div', 'bx-ans');

      /* answer shape 1 — a quantity */
      var qtyRow = el('div', 'bx-numrow');
      var qtyInput = el('input', 'bx-num');
      qtyInput.type = 'number'; qtyInput.min = '0'; qtyInput.step = '1';
      qtyInput.setAttribute('inputmode', 'numeric');
      qtyInput.setAttribute('aria-label', 'Break-even quantity in units');
      var qtyUnit = el('span', null, 'units');
      qtyRow.appendChild(qtyInput); qtyRow.appendChild(qtyUnit);
      ans.appendChild(qtyRow);

      /* answer shape 2 — profit / loss / neither, then an amount */
      var plWrap = el('div');
      var plRow = el('div', 'bx-choices');
      var plBtns = [
        { key: 'profit', label: 'Profit' },
        { key: 'loss', label: 'Loss' },
        { key: 'neither', label: 'Neither' }
      ].map(function (o) {
        var b = el('button', 'bx-btn', o.label);
        b.type = 'button'; b.setAttribute('aria-pressed', 'false'); b.dataset.key = o.key;
        plRow.appendChild(b);
        return b;
      });
      plWrap.appendChild(plRow);
      var amtRow = el('div', 'bx-numrow');
      var amtLabel = el('span', null, 'How much?  £');
      var amtInput = el('input', 'bx-num');
      amtInput.type = 'number'; amtInput.min = '0'; amtInput.step = '1';
      amtInput.setAttribute('inputmode', 'numeric');
      amtInput.setAttribute('aria-label', 'Amount of profit or loss in pounds');
      amtRow.appendChild(amtLabel); amtRow.appendChild(amtInput);
      plWrap.appendChild(amtRow);
      ans.appendChild(plWrap);

      /* answer shape 3 — which way does it move */
      var mvRow = el('div', 'bx-choices');
      var mvBtns = [
        { key: 'left', label: 'Left', sub: 'fewer units' },
        { key: 'same', label: 'Stays put', sub: 'same units' },
        { key: 'right', label: 'Right', sub: 'more units' }
      ].map(function (o) {
        var b = el('button', 'bx-btn', o.label + '<small>' + o.sub + '</small>');
        b.type = 'button'; b.setAttribute('aria-pressed', 'false'); b.dataset.key = o.key;
        mvRow.appendChild(b);
        return b;
      });
      ans.appendChild(mvRow);
      root.appendChild(ans);

      var act = el('div', 'bx-act');
      var go = el('button', 'bx-go', 'Check');
      go.type = 'button';
      var run = el('p', 'bx-run', '');
      act.appendChild(go); act.appendChild(run);
      root.appendChild(act);

      var cap = el('p', 'bx-cap', '');
      root.appendChild(cap);
      var sr = el('p', 'bx-sr');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* ----------------------------------------------------------- state --- */
      var order = shuffle(BIZ);
      var idx = 0, plSeen = 0, mvSeen = 0;
      var streak = 0, attempted = 0, mastered = false;
      var round = null, committed = false, phase = 'answering', lastCorrect = null;
      var pick = null;                       /* chosen choice-button key      */
      var stageW = 0;

      /* per-business variant orders: keep the "no profit, no loss" output and
         the "nothing moves" change inside the first two of their kind, so the
         two hardest misconceptions are reachable before mastery. */
      var outOrder = {}, chOrder = {};
      BIZ.forEach(function (b) {
        var rest = shuffle(b.outs.slice(1));           /* outs[0] is exactly BE */
        rest.splice(Math.random() < 0.5 ? 0 : 1, 0, b.outs[0]);
        outOrder[b.name] = rest;
        var ch = shuffle(b.changes.filter(function (c) { return c.kind !== 'vol'; }));
        var vol = b.changes.filter(function (c) { return c.kind === 'vol'; })[0];
        ch.splice(Math.random() < 0.5 ? 0 : 1, 0, vol);
        chOrder[b.name] = ch;
      });

      function scenarioAfter(base, ch) {
        return {
          fc: ch.fc != null ? ch.fc : base.fc,
          p: ch.p != null ? ch.p : base.p,
          vc: ch.vc != null ? ch.vc : base.vc
        };
      }

      function newRound() {
        var biz = order[idx % order.length];
        var type = TYPES[idx % TYPES.length];
        idx++;
        var base = { fc: biz.fc, p: biz.p, vc: biz.vc };
        var r = { biz: biz, type: type, base: base, after: base, c: contrib(base), be: breakEven(base) };

        if (type === 'pl') {
          var outs = outOrder[biz.name];
          r.q = outs[plSeen % outs.length]; plSeen++;
          r.profit = r.c * r.q - base.fc;      /* integer by construction */
        } else if (type === 'move') {
          var chs = chOrder[biz.name];
          r.change = chs[mvSeen % chs.length]; mvSeen++;
          r.after = scenarioAfter(base, r.change);
          r.c2 = contrib(r.after);
          r.be2 = breakEven(r.after);
          r.dir = r.be2 > r.be ? 'right' : (r.be2 < r.be ? 'left' : 'same');
        }

        /* one set of axes for the whole round, so nothing rescales on commit */
        var qs = [r.be, r.be2 || 0, r.q || 0];
        if (r.change && r.change.to) qs.push(r.change.to);
        r.xMax = niceUp(Math.max.apply(null, qs) * 1.3);
        var ys = [
          base.p * r.xMax, r.after.p * r.xMax,
          base.fc + base.vc * r.xMax, r.after.fc + r.after.vc * r.xMax
        ];
        r.yMax = niceUp(Math.max.apply(null, ys));
        return r;
      }

      /* ----------------------------------------------------------- chart --- */
      function chartHeight(w) { return w >= 520 ? 180 : (w >= 400 ? 164 : 148); }

      function drawChart() {
        var w = stageW || 440, h = chartHeight(w);
        var L = 34, R = 10, T = 12, B = 22;
        var pw = Math.max(60, w - L - R), ph = h - T - B;
        var r = round;
        var sc = (r.type === 'move' && committed) ? r.after : r.base;
        var xMax = r.xMax, yMax = r.yMax;
        function X(u) { return (L + (u / xMax) * pw).toFixed(1); }
        function Y(v) { return (T + ph - (v / yMax) * ph).toFixed(1); }
        var s = [];
        s.push('<svg width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h +
          '" role="img" aria-label="' + chartAria() + '">');

        /* gridlines and £ scale */
        [0.5, 1].forEach(function (k) {
          s.push('<line x1="' + L + '" y1="' + Y(yMax * k) + '" x2="' + (L + pw) + '" y2="' + Y(yMax * k) +
            '" stroke="#efe9e0"/>');
          s.push('<text x="' + (L - 5) + '" y="' + (+Y(yMax * k) + 4) + '" text-anchor="end" font-size="11" ' +
            'fill="#8d8880" font-family="Inter,sans-serif">' + shortMoney(yMax * k) + '</text>');
        });
        s.push('<line x1="' + L + '" y1="' + Y(0) + '" x2="' + (L + pw) + '" y2="' + Y(0) + '" stroke="#ddd7cd"/>');
        s.push('<line x1="' + L + '" y1="' + T + '" x2="' + L + '" y2="' + Y(0) + '" stroke="#ddd7cd"/>');
        s.push('<text x="' + L + '" y="' + (T + ph + 15) + '" font-size="11" fill="#8d8880" ' +
          'font-family="Inter,sans-serif">0</text>');
        s.push('<text x="' + (L + pw / 2) + '" y="' + (T + ph + 15) + '" text-anchor="middle" font-size="11" ' +
          'fill="#8d8880" font-family="Inter,sans-serif">units sold</text>');
        s.push('<text x="' + (L + pw) + '" y="' + (T + ph + 15) + '" text-anchor="end" font-size="11" ' +
          'fill="#8d8880" font-family="Inter,sans-serif">' + xMax + '</text>');

        /* fixed-cost floor: the cost line does not start at zero */
        s.push('<line x1="' + L + '" y1="' + Y(sc.fc) + '" x2="' + (L + pw) + '" y2="' + Y(sc.fc) +
          '" stroke="#c9c1b4" stroke-width="1" stroke-dasharray="3 3"/>');
        s.push(lbl(L + 4, +Y(sc.fc) + 13, 'fixed costs', '#8d8880', 'start', 500));

        /* ghost of whichever line moved */
        var costMoved = committed && r.type === 'move' && (r.base.fc !== r.after.fc || r.base.vc !== r.after.vc);
        var priceMoved = committed && r.type === 'move' && r.base.p !== r.after.p;
        if (costMoved) {
          s.push('<line x1="' + X(0) + '" y1="' + Y(r.base.fc) + '" x2="' + X(xMax) + '" y2="' +
            Y(r.base.fc + r.base.vc * xMax) + '" stroke="#c9c1b4" stroke-width="2" stroke-dasharray="5 4"/>');
        }
        if (priceMoved) {
          s.push('<line x1="' + X(0) + '" y1="' + Y(0) + '" x2="' + X(xMax) + '" y2="' + Y(r.base.p * xMax) +
            '" stroke="#c9c1b4" stroke-width="2" stroke-dasharray="5 4"/>');
        }

        /* the two lines that matter */
        var costEnd = sc.fc + sc.vc * xMax, revEnd = sc.p * xMax;
        s.push('<line x1="' + X(0) + '" y1="' + Y(sc.fc) + '" x2="' + X(xMax) + '" y2="' + Y(costEnd) +
          '" stroke="#8d8880" stroke-width="2.2"/>');
        s.push('<line x1="' + X(0) + '" y1="' + Y(0) + '" x2="' + X(xMax) + '" y2="' + Y(revEnd) +
          '" stroke="' + accent + '" stroke-width="2.2"/>');
        s.push(lbl(L + pw - 2, Math.max(T + 9, +Y(revEnd) - 5), 'Total revenue', accent, 'end'));
        s.push(lbl(L + pw - 2, Math.min(T + ph - 5, +Y(costEnd) + 13), 'Total costs', '#6f6a62', 'end'));

        if (committed) {
          var be = r.type === 'move' ? breakEven(sc) : r.be;
          /* the crossing */
          s.push('<line x1="' + X(be) + '" y1="' + Y(sc.p * be) + '" x2="' + X(be) + '" y2="' + Y(0) +
            '" stroke="#8d8880" stroke-width="1" stroke-dasharray="3 3"/>');
          s.push('<circle cx="' + X(be) + '" cy="' + Y(sc.p * be) + '" r="4.5" fill="' + accent +
            '" stroke="#fff" stroke-width="1.5"/>');
          var moved = r.type === 'move' && r.dir !== 'same';
          var side = moved && r.be2 < r.be ? -1 : 1;      /* new label points away from the old */
          s.push(lbl(+X(be) + 5 * side, +Y(0) - 6, be + ' ' + r.biz.units, '#2d2a26',
            side < 0 ? 'end' : 'start', 700));

          if (moved) {
            s.push('<circle cx="' + X(r.be) + '" cy="' + Y(r.base.p * r.be) + '" r="4" fill="#faf8f5" ' +
              'stroke="#a9a29a" stroke-width="1.5"/>');
            s.push(lbl(+X(r.be) - 5 * side, +Y(0) - 6, 'was ' + r.be, '#8d8880',
              side < 0 ? 'start' : 'end', 500));
            s.push(arrow(+X(r.be), +X(be), +Y(0) - 22));
          }
          if (r.type === 'move' && r.change.kind === 'vol') {
            s.push(arrow(+X(r.change.from), +X(r.change.to), +Y(0) - 22));
            s.push(lbl(+X(r.change.to) + 5, +Y(0) - 19, 'sales', '#6f6a62', 'start'));
          }
          if (r.type === 'pl') {
            var yTop = Math.min(+Y(sc.p * r.q), +Y(sc.fc + sc.vc * r.q));
            var yBot = Math.max(+Y(sc.p * r.q), +Y(sc.fc + sc.vc * r.q));
            s.push('<line x1="' + X(r.q) + '" y1="' + yTop + '" x2="' + X(r.q) + '" y2="' + yBot +
              '" stroke="' + (r.profit >= 0 ? accent : '#8d8880') + '" stroke-width="6" stroke-opacity=".28"/>');
            s.push('<line x1="' + X(r.q) + '" y1="' + yBot + '" x2="' + X(r.q) + '" y2="' + Y(0) +
              '" stroke="#c9c1b4" stroke-width="1" stroke-dasharray="2 3"/>');
            var anch = (+X(r.q) > L + pw * 0.7) ? 'end' : 'start';
            var dx = anch === 'end' ? -6 : 6;
            s.push(lbl(+X(r.q) + dx, (yTop + yBot) / 2 + 4,
              (r.profit === 0 ? 'no gap' : money(Math.abs(r.profit)) + (r.profit > 0 ? ' profit' : ' loss')),
              '#2d2a26', anch, 700));
          }
        }
        s.push('</svg>');
        plot.innerHTML = s.join('');

        function lbl(x, y, text, fill, anchor, weight) {
          return '<text x="' + x + '" y="' + y + '" text-anchor="' + (anchor || 'start') + '" font-size="11.5" ' +
            'font-weight="' + (weight || 600) + '" fill="' + fill + '" font-family="Inter,sans-serif" ' +
            'paint-order="stroke" stroke="#faf8f5" stroke-width="3">' + text + '</text>';
        }
        function arrow(x1, x2, y) {
          var d = x2 > x1 ? 1 : -1;
          return '<line x1="' + x1 + '" y1="' + y + '" x2="' + (x2 - 5 * d) + '" y2="' + y +
            '" stroke="#a9a29a" stroke-width="1.5"/><path d="M' + x2 + ' ' + y + 'L' + (x2 - 6 * d) + ' ' +
            (y - 3.5) + 'L' + (x2 - 6 * d) + ' ' + (y + 3.5) + 'Z" fill="#a9a29a"/>';
        }
      }

      function chartAria() {
        var r = round, sc = (r.type === 'move' && committed) ? r.after : r.base;
        var t = 'Graph of total revenue at ' + money(sc.p) + ' a unit against total costs of ' +
          money(sc.fc) + ' plus ' + money(sc.vc) + ' a unit.';
        if (committed) t += ' The lines cross at ' + breakEven(sc) + ' units.';
        return t;
      }

      /* -------------------------------------------------------- rendering --- */
      function show(node, on) { node.style.display = on ? '' : 'none'; }

      function renderRound() {
        var r = round, b = r.biz;
        figFC.querySelector('b').textContent = money(r.base.fc);
        figP.querySelector('b').textContent = money(r.base.p);
        figVC.querySelector('b').textContent = money(r.base.vc);

        if (r.type === 'be') {
          frame.textContent = b.name + ' sells ' + b.trade + '. How many ' + b.units +
            ' must ' + b.pn + ' sell in a month to break even?';
          qtyUnit.textContent = b.units;
          qtyInput.value = '';
          qtyInput.setAttribute('aria-label', 'Break-even quantity in ' + b.units);
        } else if (r.type === 'pl') {
          frame.textContent = b.name + ' sells ' + b.trade + '. This month ' + b.pn + ' sells ' + r.q +
            ' ' + b.units + '. Profit or loss — and how much?';
          amtInput.value = '';
        } else {
          frame.textContent = r.change.text + ' Which way does the break-even point move?';
        }

        show(qtyRow, r.type === 'be');
        show(plWrap, r.type === 'pl');
        show(amtRow, false);
        show(mvRow, r.type === 'move');
        plBtns.concat(mvBtns).forEach(function (b2) { b2.setAttribute('aria-pressed', 'false'); });
        pick = null;
        committed = false;
        phase = 'answering';
        lastCorrect = null;
        go.textContent = 'Check';
        cap.innerHTML = r.type === 'be'
          ? 'Read the two lines: the revenue line starts at nothing, the cost line starts at the fixed costs.'
          : (r.type === 'pl'
            ? 'The gap between the two lines at that output is the profit or the loss.'
            : 'The figures above are the starting point. Picture what the change does to a line.');
        showRun();
        drawChart();
        setState();
      }

      function showRun() {
        if (mastered) { run.textContent = 'You have it.'; return; }
        if (streak === 0) { run.textContent = ''; return; }
        run.textContent = streak + ' right in a row — ' + (streak === 2 ? 'one more' : (3 - streak) + ' more') + '.';
      }

      function currentAnswer() {
        if (round.type === 'be') {
          var v = parseInt(qtyInput.value, 10);
          return isNaN(v) ? null : v;
        }
        if (round.type === 'pl') {
          if (!pick) return null;
          var a = parseInt(amtInput.value, 10);
          return pick === 'neither' ? 'neither' : (isNaN(a) ? pick : pick + ':' + a);
        }
        return pick;
      }
      function setState() {
        var st = {
          phase: phase, type: round.type, answer: currentAnswer(),
          streak: streak, mastered: mastered, attempted: attempted
        };
        if (phase === 'checked') {
          st.correct = lastCorrect;
          st.expected = expectedOf(round);               /* never before the commit */
        }
        root.dataset.svState = JSON.stringify(st);
      }
      function expectedOf(r) {
        if (r.type === 'be') return r.be;
        if (r.type === 'pl') return r.profit;
        return r.dir;
      }

      /* --------------------------------------------------------- feedback --- */
      function say(html) {
        cap.innerHTML = html;
        sr.textContent = cap.textContent;
      }
      function nudge(html) {                 /* Check pressed with nothing to check */
        say(html);
        phase = 'incomplete';
        setState();
      }
      var MASTERY = ' <b>Three in a row — you have it.</b> Break-even is fixed costs ÷ contribution; ' +
        'costs or price move it, sales do not.';

      function commit() {
        var r = round, b = r.biz, ok, head, tail, brief;

        if (r.type === 'be') {
          var g = parseInt(qtyInput.value, 10);
          if (isNaN(g)) { nudge('Type the number of ' + b.units + ' first, then check it.'); return; }
          ok = g === r.be;
          if (ok) {
            head = '<b>Right — ' + r.be + '.</b> Contribution is ' + money(b.p) + ' − ' + money(b.vc) + ' = ' +
              money(r.c) + ', and ' + money(b.fc) + ' ÷ ' + money(r.c) + ' = ' + r.be + '.';
            tail = ' That is the crossing: ' + b.unit + ' ' + (r.be + 1) + ' is the first to earn ' +
              money(r.c) + ' of profit.';
            brief = '<b>Right — ' + r.be + '.</b> ' + money(b.fc) + ' ÷ ' + money(r.c) + ' = ' + r.be + '.';
          } else {
            var why = '';
            if (g === Math.round(b.fc / b.p)) {
              why = ' Dividing by the price ignores the ' + money(b.vc) + ' every ' + b.unit + ' costs to make.';
            } else if (g === Math.round(b.fc / b.vc)) {
              why = ' You divided by the variable cost — the fixed costs are covered by contribution, not by it.';
            } else if (g < r.be) {
              why = ' At ' + g + ' the cost line is still above the revenue line: ' +
                money((r.be - g) * r.c) + ' of fixed costs is uncovered.';
            } else {
              why = ' By ' + g + ' the lines have already crossed and ' + b.pn + ' is ' +
                money((g - r.be) * r.c) + ' in profit.';
            }
            head = '<b>Not quite — you said ' + g + '.</b> Each ' + b.unit + ' contributes ' + money(b.p) +
              ' − ' + money(b.vc) + ' = ' + money(r.c) + ', so ' + money(b.fc) + ' ÷ ' + money(r.c) + ' = ' +
              r.be + '.';
            tail = why;
          }
        } else if (r.type === 'pl') {
          if (!pick) { nudge('Choose profit, loss or neither first, then check it.'); return; }
          var amt = parseInt(amtInput.value, 10);
          if (pick !== 'neither' && isNaN(amt)) { nudge('Add the amount in pounds, then check it.'); return; }
          var trueDir = r.profit > 0 ? 'profit' : (r.profit < 0 ? 'loss' : 'neither');
          ok = pick === trueDir && (pick === 'neither' || amt === Math.abs(r.profit));
          var said = pick === 'neither' ? 'neither profit nor loss' : money(amt) + ' ' + pick;
          var gap = Math.abs(r.q - r.be);
          if (ok && trueDir === 'neither') {
            head = '<b>Right — neither.</b> At ' + r.be + ' revenue ' + money(b.p * r.be) + ' exactly meets ' +
              money(b.fc) + ' fixed plus ' + money(b.vc * r.be) + ' variable costs.';
            tail = ' Covering everything is not the end of it — ' + b.unit + ' ' + (r.be + 1) +
              ' earns ' + money(r.c) + ' of clear profit.';
            brief = '<b>Right — neither.</b> ' + r.q + ' is exactly break-even.';
          } else if (ok && trueDir === 'profit') {
            head = '<b>Right — ' + money(r.profit) + ' profit.</b> ' + r.q + ' is ' + gap +
              ' past break-even, and each of those contributes ' + money(r.c) + ': ' + gap + ' × ' +
              money(r.c) + ' = ' + money(r.profit) + '.';
            tail = ' The revenue line is above the cost line, and the margin of safety is ' + gap + ' ' +
              b.units + '.';
            brief = '<b>Right — ' + money(r.profit) + ' profit.</b> ' + gap + ' × ' + money(r.c) + ' = ' +
              money(r.profit) + '.';
          } else if (ok) {
            head = '<b>Right — ' + money(-r.profit) + ' loss.</b> ' + r.q + ' is ' + gap +
              ' short of break-even, so ' + gap + ' × ' + money(r.c) + ' = ' + money(-r.profit) +
              ' of fixed costs is still uncovered.';
            tail = ' The cost line sits above the revenue line all the way to ' + r.be + '.';
            brief = '<b>Right — ' + money(-r.profit) + ' loss.</b> ' + gap + ' × ' + money(r.c) + ' = ' +
              money(-r.profit) + ' uncovered.';
          } else {
            head = '<b>Not quite — you said ' + said + '.</b> ' + r.q + ' is ' +
              (r.profit === 0 ? 'exactly break-even' : gap + ' ' + (r.profit > 0 ? 'past' : 'short of') +
                ' break-even (' + r.be + ')') + ', so ' +
              (r.profit === 0
                ? 'revenue ' + money(b.p * r.q) + ' equals total costs — £0 either way.'
                : gap + ' × ' + money(r.c) + ' = ' + money(Math.abs(r.profit)) +
                (r.profit > 0 ? ' profit.' : ' loss.'));
            tail = r.profit === 0
              ? ' Break-even is the one output where the gap between the lines is nothing.'
              : ' Read the gap between the lines at ' + r.q + ': the revenue line is ' +
              (r.profit > 0 ? 'above' : 'below') + ' the cost line there.';
          }
        } else {
          if (!pick) { nudge('Choose left, stays put or right first, then check it.'); return; }
          ok = pick === r.dir;
          var saidDir = pick === 'same' ? 'it stays put' : 'it moves ' + pick;
          var truth = r.dir === 'same'
            ? 'it stays at ' + r.be + '.'
            : 'it moves ' + r.dir + ', from ' + r.be + ' to ' + r.be2 + '.';
          var mech;
          if (r.change.kind === 'vol') {
            mech = ' Selling more moves ' + b.name + ' along the lines. The crossing only shifts if fixed ' +
              'costs, price or variable cost change.';
          } else if (r.change.kind === 'fc') {
            mech = ' The cost line ' + (r.after.fc > b.fc ? 'lifts' : 'drops') + ' without tilting, so ' +
              money(r.after.fc) + ' ÷ ' + money(r.c) + ' = ' + r.be2 + '.';
          } else if (r.change.kind === 'vc') {
            mech = ' A dearer ' + b.unit + ' tilts the cost line steeper and cuts contribution to ' +
              money(r.c2) + ': ' + money(b.fc) + ' ÷ ' + money(r.c2) + ' = ' + r.be2 + '.';
          } else {
            mech = ' The price tilts the revenue line ' + (r.after.p > b.p ? 'steeper' : 'flatter') +
              ', so it meets the cost line ' + (r.after.p > b.p ? 'sooner' : 'later') + ': ' + money(b.fc) +
              ' ÷ ' + money(r.c2) + ' = ' + r.be2 + '.';
          }
          head = ok ? '<b>Right — ' + truth + '</b>' : '<b>Not quite — you said ' + saidDir + '.</b> In fact ' + truth;
          tail = mech;
          brief = '<b>Right — ' + truth + '</b>';
        }

        /* commit is final for this round */
        committed = true;
        phase = 'checked';
        lastCorrect = ok;
        attempted++;
        if (ok) { streak++; } else { streak = 0; }
        var justMastered = ok && streak === 3 && !mastered;
        if (streak >= 3) mastered = true;
        say(justMastered ? (brief || head) + MASTERY : head + tail);
        go.textContent = mastered ? 'Another anyway' : 'Next business';
        showRun();
        drawChart();
        setState();
      }

      /* ----------------------------------------------------------- wiring --- */
      function choose(btns, btn) {
        if (committed) return;
        pick = btn.dataset.key;
        btns.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
        phase = 'answering';
        setState();
      }
      plBtns.forEach(function (b) {
        b.addEventListener('click', function () {
          choose(plBtns, b);
          show(amtRow, pick !== 'neither');
          say(pick === 'neither'
            ? 'You are saying the two lines meet exactly at this output.'
            : 'Now the size of the gap between the lines, in pounds.');
          if (pick !== 'neither') amtInput.focus();
        });
      });
      mvBtns.forEach(function (b) {
        b.addEventListener('click', function () {
          choose(mvBtns, b);
          say(pick === 'same'
            ? 'You are saying the crossing does not move at all.'
            : 'You are saying the lines meet at a ' + (pick === 'left' ? 'lower' : 'higher') + ' number of units.');
        });
      });
      go.addEventListener('click', function () {
        if (!committed) { commit(); return; }
        round = newRound();
        renderRound();
        (round.type === 'be' ? qtyInput : (round.type === 'pl' ? plBtns[0] : mvBtns[0])).focus();
      });
      [qtyInput, amtInput].forEach(function (i) {
        i.addEventListener('keydown', function (e) {
          if (e.key === 'Enter') { e.preventDefault(); go.click(); }
        });
        i.addEventListener('input', function () {
          if (committed) return;
          phase = 'answering';
          setState();
        });
      });
      root.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !committed && pick) {
          pick = null;
          plBtns.concat(mvBtns).forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
          show(amtRow, false);
          say('Cleared — choose again.');
          phase = 'answering';
          setState();
        }
      });

      /* keep the chart crisp at whatever width the modal gives us */
      function measure() {
        var w = Math.round(plot.getBoundingClientRect().width);
        if (w > 0 && Math.abs(w - stageW) > 6) { stageW = w; return true; }
        return false;
      }
      round = newRound();
      renderRound();
      measure(); drawChart(); setState();
      if (typeof ResizeObserver === 'function') {
        var ro = new ResizeObserver(function () { if (measure()) drawChart(); });
        ro.observe(plot);
      } else {
        window.addEventListener('resize', function () { if (measure()) drawChart(); });
      }
    }
  };
})();
