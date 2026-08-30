/* StudyVault lesson widget — time-series-trend-vs-noise
 * Self-contained. No imports, no network, no storage outside root.
 *
 * Every plotted point comes from one model:
 *     value(t) = base + step*t + season[quarter(t)] + noise[t]
 * with the four seasonal effects summing to zero, so a 4-point moving
 * average of a quarterly series recovers the trend. Every verdict, every
 * number in the feedback and every mark drawn on the reveal is read back
 * out of that model — nothing about the answers is hand-authored.
 */
(function () {
  'use strict';

  var CLS = 'svw-tstn';
  var GREEN = '#4f7d63';
  var INK = '#2d2a26';
  var MUTED = '#8d8880';
  var TARGET_RUN = 3;

  /* ---------------------------------------------------------------- data */

  var ROUNDS = [
    {
      id: 'icecream', type: 'trend',
      what: 'Quarterly ice-cream sales at a seaside kiosk, in thousands of tubs.',
      ask: 'Ignoring the seasonal swing, which way is the underlying trend going?',
      startQ: 2, startYear: 2023, base: 30, step: 2,
      season: { 1: -12, 2: 2, 3: 14, 4: -4 },
      noise: [0, 2, 0, -2, 2, 0, 0, -2]
    },
    {
      id: 'garden', type: 'peak',
      what: 'Quarterly sales at a garden centre, in thousands of pounds.',
      ask: 'The seasonal pattern repeats each year. In which quarter will the next peak fall?',
      startQ: 2, startYear: 2023, base: 30, step: 7,
      season: { 1: -4, 2: 14, 3: 0, 4: -10 },
      noise: [0, 2, -2, 0, 0, 2, -2, 0]
    },
    {
      id: 'hotel', type: 'value',
      what: 'Quarterly bookings at a seaside hotel, in hundreds of rooms.',
      ask: 'Predict next quarter’s figure. Which band will it fall in?',
      startQ: 2, startYear: 2023, base: 44, step: 3,
      season: { 1: -15, 2: 5, 3: 16, 4: -6 },
      noise: [0, 2, -2, 0, 2, 0, -2, 0],
      bands: [
        { c: 46, why: 'that is the fall from the last two quarters carried on' },
        { c: 53, why: 'that is roughly the latest figure again' },
        { c: 63, why: 'that repeats last year’s Q2 and leaves the trend out' }
      ]
    },
    {
      id: 'oil', type: 'ma',
      what: 'Quarterly heating-oil deliveries, in thousands of litres.',
      ask: 'A 4-point moving average is worked out for this series. Predict the shape it will plot as.',
      startQ: 1, startYear: 2024, base: 80, step: 0,
      season: { 1: 16, 2: -4, 3: -20, 4: 8 },
      noise: [0, 2, -2, 0, 2, -2, 0, 2]
    },
    {
      id: 'umbrella', type: 'trend',
      what: 'Quarterly umbrella sales at a department store, in hundreds sold.',
      ask: 'Ignoring the seasonal swing, which way is the underlying trend going?',
      startQ: 1, startYear: 2024, base: 60, step: -3,
      season: { 1: 6, 2: -4, 3: -14, 4: 12 },
      noise: [0, 2, -2, 0, -2, 0, 2, 0]
    },
    {
      id: 'gym', type: 'peak',
      what: 'New gym memberships taken out each quarter.',
      ask: 'The seasonal pattern repeats each year. In which quarter will the next peak fall?',
      startQ: 2, startYear: 2023, base: 60, step: 2,
      season: { 1: 18, 2: -2, 3: -10, 4: -6 },
      noise: [0, 2, -2, 0, 2, 0, -2, 0]
    },
    {
      id: 'furniture', type: 'value',
      what: 'Quarterly garden-furniture sales at a retailer, in thousands of pounds.',
      ask: 'Predict next quarter’s figure. Which band will it fall in?',
      startQ: 2, startYear: 2023, base: 90, step: -4,
      season: { 1: -12, 2: 16, 3: 4, 4: -8 },
      noise: [0, -2, 2, 0, 2, 0, -2, 0],
      bands: [
        { c: 44, why: 'that is the recent fall carried straight on' },
        { c: 52, why: 'that is roughly the latest figure again' },
        { c: 92, why: 'that repeats last year’s Q2 and leaves the trend out' }
      ]
    },
    {
      id: 'delivery', type: 'ma',
      what: 'Quarterly food-delivery orders for one city, in thousands.',
      ask: 'A 4-point moving average is worked out for this series. Predict the shape it will plot as.',
      startQ: 1, startYear: 2024, base: 50, step: 4,
      season: { 1: 6, 2: -12, 3: -4, 4: 10 },
      noise: [0, 2, -2, 0, 2, 0, -2, 0]
    },
    {
      id: 'cinema', type: 'trend',
      what: 'Quarterly cinema admissions at a multiplex, in thousands.',
      ask: 'Ignoring the seasonal swing, which way is the underlying trend going?',
      startQ: 3, startYear: 2023, base: 46, step: 0,
      season: { 1: 4, 2: -16, 3: 2, 4: 10 },
      noise: [2, 0, -2, 0, 0, 2, -2, 2]
    }
  ];

  /* ------------------------------------------------------------- model */

  var N = 8;              // observed quarters
  var SLOTS = 12;         // 8 observed + 4 ahead

  function quarterAt(r, t) { return ((r.startQ - 1 + t) % 4) + 1; }
  function yearAt(r, t) { return r.startYear + Math.floor((r.startQ - 1 + t) / 4); }
  function trendAt(r, t) { return r.base + r.step * t; }
  function modelAt(r, t) { return trendAt(r, t) + r.season[quarterAt(r, t)]; }

  function pointsOf(r) {
    var out = [], t;
    for (t = 0; t < N; t++) {
      out.push({
        t: t, q: quarterAt(r, t), year: yearAt(r, t),
        trend: trendAt(r, t), value: modelAt(r, t) + r.noise[t]
      });
    }
    return out;
  }

  /* 4-point moving average, each point plotted at the midpoint of its four
     quarters (t = 1.5, 2.5, ...). Five points from eight quarters. */
  function movingAverage(pts) {
    var out = [], i, j, s;
    for (i = 0; i + 3 < pts.length; i++) {
      s = 0;
      for (j = 0; j < 4; j++) s += pts[i + j].value;
      out.push({ t: i + 1.5, value: s / 4 });
    }
    return out;
  }

  function peakQuarter(r) {
    var best = 1, q;
    for (q = 2; q <= 4; q++) if (r.season[q] > r.season[best]) best = q;
    return best;
  }

  function direction(r) { return r.step > 0 ? 'up' : (r.step < 0 ? 'down' : 'flat'); }

  /* next occurrence of quarter q strictly after the last observed point */
  function nextIndexOfQuarter(r, q) {
    var t;
    for (t = N; t < N + 4; t++) if (quarterAt(r, t) === q) return t;
    return N;
  }

  function bandsOf(r) {
    var next = modelAt(r, N);
    var list = r.bands.map(function (b) { return { c: b.c, why: b.why, key: false }; });
    list.push({ c: next, why: '', key: true });
    list.sort(function (a, b) { return a.c - b.c; });
    return list.map(function (b) { return { lo: b.c - 2, hi: b.c + 2, c: b.c, why: b.why, key: b.key }; });
  }

  function answerOf(r) {
    if (r.type === 'trend' || r.type === 'ma') return direction(r);
    if (r.type === 'peak') return 'Q' + peakQuarter(r);
    var bs = bandsOf(r), i;
    for (i = 0; i < bs.length; i++) if (bs[i].key) return 'b' + i;
    return 'b0';
  }

  function optionsOf(r) {
    if (r.type === 'trend') {
      return [{ k: 'up', label: 'Rising' }, { k: 'down', label: 'Falling' }, { k: 'flat', label: 'Roughly flat' }];
    }
    if (r.type === 'ma') {
      return [{ k: 'up', label: 'A steady rise' }, { k: 'flat', label: 'Roughly flat' },
        { k: 'down', label: 'A steady fall' }, { k: 'zigzag', label: 'The same zig-zag' }];
    }
    if (r.type === 'peak') {
      return [1, 2, 3, 4].map(function (q) { return { k: 'Q' + q, label: 'Q' + q }; });
    }
    return bandsOf(r).map(function (b, i) {
      return { k: 'b' + i, label: b.lo + '–' + b.hi };
    });
  }

  /* ------------------------------------------------------------- words */

  function n1(v) { return (Math.round(v * 10) / 10).toFixed(1); }
  function abs(v) { return Math.abs(v); }

  var DIRWORD = { up: 'rising', down: 'falling', flat: 'roughly flat' };
  var MAWORD = { up: 'a steady rise', down: 'a steady fall', flat: 'roughly flat', zigzag: 'the same zig-zag' };

  function sameQuarterPair(pts, q) {
    return pts.filter(function (p) { return p.q === q; });
  }

  function trendTail(r, pts) {
    var pair = sameQuarterPair(pts, pts[N - 1].q);
    var a = pair[0], b = pair[pair.length - 1];
    var cmp = 'Compare Q' + a.q + ' with Q' + a.q + ' — ' + a.value + ' in ' + a.year +
      ', ' + b.value + ' in ' + b.year + ' — ';
    if (r.step === 0) {
      var lo = Math.min.apply(null, pts.map(function (p) { return p.value; }));
      var hi = Math.max.apply(null, pts.map(function (p) { return p.value; }));
      return cmp + 'so the level is going nowhere. The series swings ' + (hi - lo) +
        ' across the year and ends where it started.';
    }
    return cmp + 'so the trend is ' + DIRWORD[direction(r)] + ' about ' + abs(r.step) + ' a quarter.';
  }

  function feedback(r, pts, picked, right) {
    var last = pts[N - 1], prev = pts[N - 2];
    var lastQ = 'Q' + last.q;
    var sOff = r.season[last.q];
    var side = sOff >= 0 ? 'above' : 'below';
    var legWord = last.value > prev.value ? 'climbs' : 'drops';
    var leg = 'The last leg ' + legWord + ' from ' + prev.value + ' to ' + last.value;
    var seasonBit = 'a quarter that sits about ' + abs(sOff) + ' ' + side + ' the trend every year';

    if (r.type === 'trend') {
      if (right) {
        return 'Right — ' + DIRWORD[picked] + '. ' + leg + ', but that is ' + lastQ +
          ', ' + seasonBit + '. ' + trendTail(r, pts);
      }
      return 'Not quite — you said ' + DIRWORD[picked] + '. ' + leg +
        ', and that is ' + lastQ + ', ' + seasonBit + '. ' + trendTail(r, pts);
    }

    if (r.type === 'ma') {
      var ma = movingAverage(pts);
      var vals = pts.map(function (p) { return p.value; });
      var swing = Math.max.apply(null, vals) - Math.min.apply(null, vals);
      var maVals = ma.map(function (m) { return m.value; });
      var maSwing = Math.max.apply(null, maVals) - Math.min.apply(null, maVals);
      var list = ma.map(function (m) { return n1(m.value); }).join(', ');
      var head = right ? 'Right — ' + MAWORD[picked] + '. ' : 'Not quite — you said ' + MAWORD[picked] + '. ';
      var tail = r.step === 0
        ? 'The raw figures swing ' + swing + '; the moving average moves ' + n1(maSwing) + '. That is what it is for.'
        : 'The raw figures swing ' + swing + ', but the average ' + (r.step > 0 ? 'climbs' : 'falls') +
          ' steadily by ' + abs(r.step) + ' a quarter — the trend itself.';
      return head + 'Each point is the mean of four quarters — one whole year — so the ' +
        'four seasonal effects cancel: ' + list + '. ' + tail;
    }

    if (r.type === 'peak') {
      var pq = peakQuarter(r);
      var pk = sameQuarterPair(pts, pq);
      var nt = nextIndexOfQuarter(r, pq);
      var when = 'Q' + pq + ' ' + yearAt(r, nt);
      var vals2 = pts.map(function (p) { return p.value; });
      var maxV = Math.max.apply(null, vals2);
      var maxP = pts.filter(function (p) { return p.value === maxV; })[0];
      var pkBit = 'Q' + pq + ' runs about ' + abs(r.season[pq]) + ' above the trend — ' +
        pk[0].value + ' in ' + pk[0].year + ', ' + pk[pk.length - 1].value + ' in ' + pk[pk.length - 1].year;
      if (right) {
        var tail;
        if (maxP.q !== pq) {
          tail = 'The tallest point plotted is ' + maxV + ' in Q' + maxP.q + ' ' + maxP.year +
            ', but height on the page is trend plus season — the peak is set by the calendar, ' +
            'not by which point is tallest. Next one: ' + when + '.';
        } else if (last.q === pq) {
          tail = 'The series ends on a peak, so the next one is a full year later: ' + when + '.';
        } else {
          tail = 'Next one: ' + when + ', ' + (nt - (N - 1)) + ' quarters ahead.';
        }
        return 'Right — Q' + pq + '. ' + pkBit + '. ' + tail;
      }
      var pickedQ = Number(picked.slice(1));
      var why;
      if (pickedQ === maxP.q && maxP.q !== pq) {
        why = 'Q' + pickedQ + ' holds the highest point on the graph (' + maxV +
          '), but that is the trend lifting the whole series, not the season: Q' + pickedQ +
          ' sits ' + abs(r.season[pickedQ]) + ' ' + (r.season[pickedQ] >= 0 ? 'above' : 'below') + ' the trend.';
      } else if (pickedQ === quarterAt(r, N)) {
        why = 'Q' + pickedQ + ' is simply the quarter that comes next, and the series is ' +
          (last.value > prev.value ? 'rising' : 'falling') + ' as it ends — but the peak is fixed to the calendar, not to the last leg.';
      } else {
        why = 'Q' + pickedQ + ' sits ' + abs(r.season[pickedQ]) + ' ' +
          (r.season[pickedQ] >= 0 ? 'above' : 'below') + ' the trend, so it is never the year’s high point.';
      }
      return 'Not quite — you said Q' + pickedQ + '. ' + why + ' ' + pkBit + '. Next peak: ' + when + '.';
    }

    // value
    var bs = bandsOf(r);
    var idx = Number(picked.slice(1));
    var key = bs.filter(function (b) { return b.key; })[0];
    var q8 = quarterAt(r, N), s8 = r.season[q8];
    var maths = 'The trend reaches about ' + trendAt(r, N) + ' next quarter and Q' + q8 +
      ' runs ' + abs(s8) + ' ' + (s8 >= 0 ? 'above' : 'below') + ' it, giving about ' + modelAt(r, N) + '.';
    if (right) {
      return 'Right — ' + key.lo + '–' + key.hi + '. ' + maths +
        ' One quarter ahead is a fair extrapolation; a year ahead assumes both the trend and the season hold, which is far less safe.';
    }
    return 'Not quite — you said ' + bs[idx].lo + '–' + bs[idx].hi + ': ' + bs[idx].why +
      '. ' + maths + ' That is the ' + key.lo + '–' + key.hi + ' band.';
  }

  function readout(pts) {
    var vals = pts.map(function (p) { return p.value; });
    var hi = Math.max.apply(null, vals), lo = Math.min.apply(null, vals);
    var hp = pts.filter(function (p) { return p.value === hi; })[0];
    var lp = pts.filter(function (p) { return p.value === lo; })[0];
    var last = pts[N - 1];
    return 'Highest ' + hi + ' (Q' + hp.q + ' ' + hp.year + ') · lowest ' + lo +
      ' (Q' + lp.q + ' ' + lp.year + ') · latest ' + last.value + ' (Q' + last.q + ' ' + last.year + ').';
  }

  /* --------------------------------------------------------------- svg */

  var SVGNS = 'http://www.w3.org/2000/svg';
  var W = 340, H = 164, PADL = 30, PADR = 8, PADT = 10, BASEY = 122;
  var QY = 136, YRY = 150;
  var SLOTW = (W - PADL - PADR) / SLOTS;

  function sx(t) { return PADL + SLOTW * (t + 0.5); }

  function niceMax(v) {
    var steps = [5, 10, 20, 25, 50, 100, 200], i, k;
    for (i = 0; i < steps.length; i++) {
      k = Math.ceil(v / steps[i]);
      if (k >= 3 && k <= 6) return { max: k * steps[i], step: steps[i], divs: k };
    }
    return { max: Math.ceil(v / 100) * 100, step: Math.ceil(v / 400) * 100, divs: 4 };
  }

  function s(tag, attrs) {
    var e = document.createElementNS(SVGNS, tag), k;
    for (k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) e.setAttribute(k, attrs[k]);
    return e;
  }
  function stext(x, y, str, attrs) {
    var e = s('text', attrs || {});
    e.setAttribute('x', x); e.setAttribute('y', y);
    e.textContent = str;
    return e;
  }

  function buildChart(r, accent, revealed, picked) {
    var pts = pointsOf(r);
    var need = [], t;
    pts.forEach(function (p) { need.push(p.value); });
    if (r.type === 'trend') {
      var topS = Math.max(r.season[1], r.season[2], r.season[3], r.season[4]);
      for (t = 0; t < N; t++) need.push(trendAt(r, t) + topS);
      need.push(trendAt(r, SLOTS - 1));
    } else if (r.type === 'value') {
      bandsOf(r).forEach(function (b) { need.push(b.hi); });
      need.push(trendAt(r, N));
    } else if (r.type === 'ma') {
      movingAverage(pts).forEach(function (m) { need.push(m.value); });
    }
    var top = niceMax(Math.max.apply(null, need) * 1.04);
    var yMax = top.max;

    function sy(v) { return BASEY - (v / yMax) * (BASEY - PADT); }

    var svg = s('svg', {
      viewBox: '0 0 ' + W + ' ' + H,
      role: 'img',
      'aria-label': 'Quarterly time series, ' + pts[0].value + ' to ' + pts[N - 1].value +
        ', eight quarters plotted with four quarters of empty axis ahead.'
    });

    /* ahead zone */
    svg.appendChild(s('rect', {
      x: sx(7.5), y: PADT - 4, width: (W - PADR) - sx(7.5), height: BASEY - PADT + 4,
      fill: INK, opacity: '.035'
    }));
    svg.appendChild(s('line', {
      x1: sx(7.5), y1: PADT - 4, x2: sx(7.5), y2: BASEY,
      stroke: '#c9c2b6', 'stroke-width': '1', 'stroke-dasharray': '3 3'
    }));

    /* gridlines + y labels */
    var i, v;
    for (i = 0; i <= top.divs; i++) {
      v = top.step * i;
      if (v > yMax) break;
      svg.appendChild(s('line', {
        x1: PADL, y1: sy(v), x2: W - PADR, y2: sy(v),
        stroke: i === 0 ? '#c9c2b6' : '#e8e2d9', 'stroke-width': '1'
      }));
      svg.appendChild(stext(PADL - 5, sy(v) + 3.4, String(v), {
        'text-anchor': 'end', 'font-size': '9.5', fill: MUTED, 'font-family': 'Inter, sans-serif'
      }));
    }

    /* x labels: quarter digits, then years */
    svg.appendChild(stext(PADL - 5, QY, 'Q', {
      'text-anchor': 'end', 'font-size': '9.5', fill: MUTED, 'font-family': 'Inter, sans-serif'
    }));
    var years = {};
    for (i = 0; i < SLOTS; i++) {
      var q = quarterAt(r, i), yr = yearAt(r, i);
      svg.appendChild(stext(sx(i), QY, String(q), {
        'text-anchor': 'middle', 'font-size': '9.5',
        fill: i < N ? '#6b655c' : '#a9a29a', 'font-family': 'Inter, sans-serif'
      }));
      if (!years[yr]) years[yr] = { a: i, b: i, future: i >= N };
      years[yr].b = i;
      if (i < N) years[yr].future = false;
    }
    for (var yk in years) if (Object.prototype.hasOwnProperty.call(years, yk)) {
      var g = years[yk];
      svg.appendChild(stext((sx(g.a) + sx(g.b)) / 2, YRY, yk, {
        'text-anchor': 'middle', 'font-size': '9.5',
        fill: g.future ? '#a9a29a' : MUTED, 'font-family': 'Inter, sans-serif'
      }));
    }

    /* reveal marks that sit UNDER the data */
    if (revealed && (r.type === 'trend')) {
      var hiS = Math.max(r.season[1], r.season[2], r.season[3], r.season[4]);
      var loS = Math.min(r.season[1], r.season[2], r.season[3], r.season[4]);
      var dTop = [], dBot = [];
      for (i = 0; i < N; i++) { dTop.push(sx(i) + ',' + sy(trendAt(r, i) + hiS)); dBot.unshift(sx(i) + ',' + sy(trendAt(r, i) + loS)); }
      svg.appendChild(s('polygon', {
        points: dTop.concat(dBot).join(' '), fill: accent, opacity: '.12'
      }));
    }

    /* data */
    var pl = pts.map(function (p) { return sx(p.t) + ',' + sy(p.value); }).join(' ');
    svg.appendChild(s('polyline', { points: pl, fill: 'none', stroke: INK, 'stroke-width': '1.6', 'stroke-linejoin': 'round' }));
    pts.forEach(function (p) {
      svg.appendChild(s('circle', { cx: sx(p.t), cy: sy(p.value), r: '2.6', fill: '#fff', stroke: INK, 'stroke-width': '1.3' }));
    });

    if (!revealed) return svg;

    /* reveal marks that sit OVER the data */
    if (r.type === 'trend') {
      svg.appendChild(s('line', {
        x1: sx(0), y1: sy(trendAt(r, 0)), x2: sx(N - 1), y2: sy(trendAt(r, N - 1)),
        stroke: accent, 'stroke-width': '2'
      }));
      svg.appendChild(s('line', {
        x1: sx(N - 1), y1: sy(trendAt(r, N - 1)), x2: sx(SLOTS - 1), y2: sy(trendAt(r, SLOTS - 1)),
        stroke: accent, 'stroke-width': '2', 'stroke-dasharray': '4 3'
      }));
      svg.appendChild(stext(sx(SLOTS - 1), sy(trendAt(r, SLOTS - 1)) - 5, 'trend', {
        'text-anchor': 'end', 'font-size': '10', fill: accent, 'font-weight': '600', 'font-family': 'Inter, sans-serif'
      }));
      svg.appendChild(stext(sx(0) - 8, Math.min(BASEY - 2,
        sy(trendAt(r, 0) + Math.min(r.season[1], r.season[2], r.season[3], r.season[4])) + 11),
        'seasonal band', { 'text-anchor': 'start', 'font-size': '9.5', fill: MUTED, 'font-family': 'Inter, sans-serif' }));
    }

    if (r.type === 'ma') {
      var ma = movingAverage(pts);
      svg.appendChild(s('polyline', {
        points: ma.map(function (m) { return sx(m.t) + ',' + sy(m.value); }).join(' '),
        fill: 'none', stroke: accent, 'stroke-width': '2.2', 'stroke-linejoin': 'round'
      }));
      ma.forEach(function (m) {
        svg.appendChild(s('circle', { cx: sx(m.t), cy: sy(m.value), r: '2.4', fill: accent }));
      });
      svg.appendChild(stext(W - PADR, sy(ma[ma.length - 1].value) + 3, '4-point moving average', {
        'text-anchor': 'end', 'font-size': '10', fill: accent, 'font-weight': '600', 'font-family': 'Inter, sans-serif'
      }));
    }

    if (r.type === 'peak') {
      var pq = peakQuarter(r);
      pts.forEach(function (p) {
        if (p.q === pq) svg.appendChild(s('circle', { cx: sx(p.t), cy: sy(p.value), r: '5.4', fill: 'none', stroke: accent, 'stroke-width': '1.6' }));
      });
      var nt = nextIndexOfQuarter(r, pq);
      svg.appendChild(s('line', { x1: sx(nt), y1: BASEY, x2: sx(nt), y2: PADT + 2, stroke: accent, 'stroke-width': '1.6', 'stroke-dasharray': '4 3' }));
      svg.appendChild(stext(sx(nt), PADT - 1, 'next peak', {
        'text-anchor': 'middle', 'font-size': '10', fill: accent, 'font-weight': '600', 'font-family': 'Inter, sans-serif'
      }));
      if (picked && picked !== 'Q' + pq) {
        var pt2 = nextIndexOfQuarter(r, Number(picked.slice(1)));
        svg.appendChild(s('line', { x1: sx(pt2), y1: BASEY, x2: sx(pt2), y2: PADT + 12, stroke: MUTED, 'stroke-width': '1.4', 'stroke-dasharray': '2 3' }));
        svg.appendChild(stext(sx(pt2), PADT + 9, 'yours', {
          'text-anchor': 'middle', 'font-size': '9.5', fill: MUTED, 'font-family': 'Inter, sans-serif'
        }));
      }
    }

    if (r.type === 'value') {
      var bs = bandsOf(r), key = null, idx = picked ? Number(picked.slice(1)) : -1;
      bs.forEach(function (b, k) { if (b.key) key = b; });
      svg.appendChild(s('line', {
        x1: sx(N - 1), y1: sy(trendAt(r, N - 1)), x2: sx(N), y2: sy(trendAt(r, N)),
        stroke: accent, 'stroke-width': '1.6', 'stroke-dasharray': '4 3'
      }));
      var keyLabY = sy(key.hi) - 5;
      if (idx >= 0 && !bs[idx].key) {
        svg.appendChild(s('rect', {
          x: sx(N) - 9, y: sy(bs[idx].hi), width: 18, height: Math.max(4, sy(bs[idx].lo) - sy(bs[idx].hi)),
          fill: 'none', stroke: MUTED, 'stroke-width': '1.2', 'stroke-dasharray': '3 2', rx: '2'
        }));
        var yourY = sy(bs[idx].c) + 3;
        if (Math.abs(yourY - keyLabY) < 12) yourY = keyLabY + (bs[idx].c < key.c ? 13 : -13);
        svg.appendChild(stext(W - PADR, yourY, 'yours', {
          'text-anchor': 'end', 'font-size': '9.5', fill: MUTED, 'font-family': 'Inter, sans-serif'
        }));
      }
      svg.appendChild(s('rect', {
        x: sx(N) - 9, y: sy(key.hi), width: 18, height: Math.max(4, sy(key.lo) - sy(key.hi)),
        fill: accent, opacity: '.22', rx: '2'
      }));
      svg.appendChild(s('rect', {
        x: sx(N) - 9, y: sy(key.hi), width: 18, height: Math.max(4, sy(key.lo) - sy(key.hi)),
        fill: 'none', stroke: accent, 'stroke-width': '1.4', rx: '2'
      }));
      svg.appendChild(stext(W - PADR, keyLabY, 'trend + season', {
        'text-anchor': 'end', 'font-size': '10', fill: accent, 'font-weight': '600', 'font-family': 'Inter, sans-serif'
      }));
    }

    return svg;
  }

  /* --------------------------------------------------------------- css */

  function css(accent) {
    return [
      '.' + CLS + '{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:' + INK + ';',
      'background:#fff;border:1px solid #e8e3db;border-radius:16px;padding:1.2rem 1.25rem 1.25rem;',
      'box-sizing:border-box;max-width:900px;-webkit-text-size-adjust:100%;}',
      '.' + CLS + ' *{box-sizing:border-box;}',
      '.' + CLS + ' .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + ';margin:0 0 .2rem;}',
      '.' + CLS + ' .t{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.2;margin:0 0 .35rem;}',
      '.' + CLS + ' .frame{font-size:.87rem;line-height:1.45;margin:0 0 .55rem;color:#3b3730;min-height:3.7em;}',
      '.' + CLS + ' .frame b{font-weight:600;}',
      '.' + CLS + ' .stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;',
      'padding:.35rem .3rem .15rem;margin:0 auto .55rem;max-width:430px;}',
      '.' + CLS + ' .stage svg{display:block;width:100%;height:auto;}',
      '.' + CLS + ' .opts{display:flex;flex-wrap:wrap;gap:.4rem;margin:0 0 .55rem;}',
      '.' + CLS + ' .opt{flex:1 1 4.2rem;min-width:4.2rem;font-family:inherit;font-size:.82rem;font-weight:600;',
      'line-height:1.15;padding:.5rem .55rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;',
      'color:' + INK + ';cursor:pointer;font-variant-numeric:tabular-nums;}',
      '.' + CLS + ' .opt:hover:not(:disabled){border-color:#c9c2b6;}',
      '.' + CLS + ' .opt.on{background:' + INK + ';border-color:' + INK + ';color:#fff;}',
      '.' + CLS + ' .opt.key{border-color:' + GREEN + ';box-shadow:0 0 0 1px ' + GREEN + ';}',
      '.' + CLS + ' .opt:disabled{opacity:1;cursor:default;}',
      '.' + CLS + ' .go{display:flex;align-items:center;gap:.6rem;margin:0 0 .5rem;}',
      '.' + CLS + ' .btn{font-family:inherit;font-size:.84rem;font-weight:600;padding:.55rem 1rem;border-radius:10px;',
      'border:1px solid ' + INK + ';background:' + INK + ';color:#fff;cursor:pointer;}',
      '.' + CLS + ' .btn:disabled{background:#faf8f5;border-color:#ddd7cd;color:#a9a29a;cursor:default;}',
      '.' + CLS + ' .run{font-size:.76rem;color:' + MUTED + ';font-variant-numeric:tabular-nums;}',
      '.' + CLS + ' .run.done{color:' + GREEN + ';font-weight:600;}',
      '.' + CLS + ' .cap{font-size:.86rem;line-height:1.5;color:#3b3730;margin:0;min-height:4.5em;}',
      '.' + CLS + ' .cap b{font-weight:600;}',
      '.' + CLS + ' .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}',
      '@media (min-width:620px){.' + CLS + ' .frame{min-height:2.9em;}.' + CLS + ' .cap{min-height:3.5em;}}'
    ].join('');
  }

  /* ------------------------------------------------------------- mount */

  function mount(root, ctx) {
    ctx = ctx || {};
    var cs = window.getComputedStyle ? window.getComputedStyle(root) : null;
    var accent = (cs && cs.getPropertyValue('--accent') || '').trim() || ctx.accent || '#3f6f5f';

    root.className = (root.className ? root.className + ' ' : '') + CLS;

    var style = document.createElement('style');
    style.textContent = css(accent);
    root.appendChild(style);

    function div(cls, html) {
      var d = document.createElement('div');
      d.className = cls;
      if (html !== undefined) d.innerHTML = html;
      return d;
    }

    var kicker = div('k'); kicker.textContent = 'Time series';
    var title = div('t'); title.textContent = 'Trend, season or noise?';
    var frame = document.createElement('p'); frame.className = 'frame';
    var stage = div('stage');
    var opts = div('opts');
    var goRow = div('go');
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'btn';
    var run = document.createElement('span'); run.className = 'run';
    goRow.appendChild(btn); goRow.appendChild(run);
    var cap = document.createElement('p'); cap.className = 'cap';
    var sr = document.createElement('p'); sr.className = 'sr';
    sr.setAttribute('aria-live', 'polite');

    root.appendChild(kicker);
    root.appendChild(title);
    root.appendChild(frame);
    root.appendChild(stage);
    root.appendChild(opts);
    root.appendChild(goRow);
    root.appendChild(cap);
    root.appendChild(sr);

    var state = { i: 0, streak: 0, mastered: false, attempted: 0, picked: null, revealed: false, brokeFrom: 0 };
    var round, pts, optButtons;

    function publish(extra) {
      var o = {
        streak: state.streak, mastered: state.mastered, attempted: state.attempted,
        series: round.id, task: round.type
      };
      if (extra) for (var k in extra) if (Object.prototype.hasOwnProperty.call(extra, k)) o[k] = extra[k];
      root.dataset.svState = JSON.stringify(o);
    }

    function renderChart() {
      var svg = buildChart(round, accent, state.revealed, state.picked);
      if (stage.firstChild) stage.replaceChild(svg, stage.firstChild);
      else stage.appendChild(svg);
    }

    function runLine() {
      if (state.mastered) {
        run.className = 'run done';
        run.textContent = 'Mastered — ' + TARGET_RUN + ' in a row.';
      } else if (state.streak === 0) {
        run.className = 'run';
        run.textContent = state.brokeFrom > 0 ? 'Run reset — back to 0.' : '';
      } else {
        run.className = 'run';
        run.textContent = state.streak + ' right in a row — ' +
          (TARGET_RUN - state.streak) + ' more and you have it.';
      }
    }

    function loadRound(focus) {
      round = ROUNDS[state.i % ROUNDS.length];
      pts = pointsOf(round);
      state.picked = null;
      state.revealed = false;

      frame.innerHTML = '';
      var b = document.createElement('b'); b.textContent = round.what;
      frame.appendChild(b);
      frame.appendChild(document.createTextNode(' ' + round.ask));

      opts.innerHTML = '';
      optButtons = optionsOf(round).map(function (o) {
        var el = document.createElement('button');
        el.type = 'button'; el.className = 'opt'; el.textContent = o.label;
        el.setAttribute('aria-pressed', 'false');
        el.addEventListener('click', function () { pick(o.k); });
        opts.appendChild(el);
        return { k: o.k, el: el };
      });

      btn.textContent = 'Check';
      btn.disabled = true;
      btn.onclick = commit;

      cap.textContent = readout(pts);
      runLine();
      renderChart();
      publish({ picked: null, correct: null });
      if (focus && optButtons.length) optButtons[0].el.focus();
    }

    function pick(k) {
      if (state.revealed) return;
      state.picked = k;
      optButtons.forEach(function (o) {
        var on = o.k === k;
        o.el.classList.toggle('on', on);
        o.el.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      btn.disabled = false;
      publish({ picked: k, correct: null });
    }

    function commit() {
      if (!state.picked || state.revealed) return;
      var key = answerOf(round);
      var right = state.picked === key;
      state.revealed = true;
      state.attempted += 1;
      state.brokeFrom = right ? 0 : state.streak;
      state.streak = right ? state.streak + 1 : 0;
      var justMastered = false;
      if (right && state.streak >= TARGET_RUN && !state.mastered) { state.mastered = true; justMastered = true; }

      optButtons.forEach(function (o) {
        o.el.disabled = true;
        if (o.k === key) o.el.classList.add('key');
      });

      var msg = feedback(round, pts, state.picked, right);
      if (justMastered) {
        msg += ' Three in a row — you have it: the trend is what is left once the season is ' +
          'averaged out.';
      }
      cap.textContent = msg;
      sr.textContent = msg;

      renderChart();
      runLine();

      btn.textContent = state.mastered ? 'Another anyway' : 'Next series';
      btn.disabled = false;
      btn.onclick = function () { state.i += 1; loadRound(true); };
      btn.focus();

      publish({ picked: state.picked, answer: key, correct: right });
    }

    loadRound(false);
  }

  window.SVWidget = {
    meta: {
      id: 'time-series-trend-vs-noise',
      title: 'Trend, season or noise?',
      teaches: 'Separating the underlying trend of a time series from repeating seasonal variation and irregular noise, and what a 4-point moving average is for.'
    },
    mount: mount
  };
})();
