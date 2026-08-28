/* subduction-angle — StudyVault lesson widget
   Predict where a destructive margin's features sit from the angle of the
   descending slab. Every position is computed from the geometry
   (dip + a melting depth of about 100 km), so the reveal cannot contradict
   the marking. */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';
  var CLS = 'svw-subang';

  /* ------------------------------------------------------------------ model */

  var MELT = 100;                    /* km — depth at which melting starts */
  var DIPS = [20, 25, 30, 40, 45, 60];

  function rad(d) { return d * Math.PI / 180; }
  function snap5(v) { return Math.round(v / 5) * 5; }
  /* horizontal distance from the trench at which the slab is MELT km down */
  function arcDist(dip) { return snap5(MELT / Math.tan(rad(dip))); }
  /* depth of the slab a given distance inland */
  function slabDepth(dip, km) { return snap5(km * Math.tan(rad(dip))); }

  function asc(a, b) { return a - b; }

  /* pick one value below the target and one above it, else fill from nearest */
  function bracket(pool, target, blocked, want) {
    var out = [], used = blocked.slice(), i;
    var below = pool.filter(function (v) { return v < target && used.indexOf(v) < 0; }).sort(function (a, b) { return b - a; });
    var above = pool.filter(function (v) { return v > target && used.indexOf(v) < 0; }).sort(asc);
    if (below.length) { out.push(below[0]); used.push(below[0]); }
    if (above.length && out.length < want) { out.push(above[0]); used.push(above[0]); }
    var rest = pool.slice().sort(function (a, b) { return Math.abs(a - target) - Math.abs(b - target); });
    for (i = 0; i < rest.length && out.length < want; i++) {
      if (used.indexOf(rest[i]) < 0) { used.push(rest[i]); out.push(rest[i]); }
    }
    return out;
  }

  function arcRound(dip) {
    var ans = arcDist(dip);
    var pool = DIPS.map(arcDist);
    var opts = [0, ans].concat(bracket(pool, ans, [0, ans], 2)).sort(asc);
    return { type: 'arc', dip: dip, answer: ans, options: opts };
  }

  function depthRound(dip, site) {
    var ans = slabDepth(dip, site);
    var pool = [];
    DIPS.forEach(function (d) {
      if (d === dip) return;
      var v = slabDepth(d, site);
      if (v >= 20 && v <= 165) pool.push(v);
    });
    var opts = [10, ans].concat(bracket(pool, ans, [10, ans], 2)).sort(asc);
    return { type: 'depth', dip: dip, site: site, answer: ans, options: opts };
  }

  function changeRound(d1, d2) {
    var ans = arcDist(d2), old = arcDist(d1);
    var pool = DIPS.map(arcDist);
    var opts = [ans, old].concat(bracket(pool, ans, [ans, old], 2)).sort(asc);
    return { type: 'change', dip: d2, oldDip: d1, oldArc: old, answer: ans, options: opts };
  }

  function buildDeck() {
    var deck = [];
    DIPS.forEach(function (d) { deck.push(arcRound(d)); });
    [[20, 200], [25, 180], [30, 150], [40, 120], [45, 100]].forEach(function (p) {
      deck.push(depthRound(p[0], p[1]));
    });
    [[30, 45], [45, 25], [20, 40], [40, 20], [25, 60], [60, 30]].forEach(function (p) {
      deck.push(changeRound(p[0], p[1]));
    });
    /* shuffle */
    for (var i = deck.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = deck[i];
      deck[i] = deck[j]; deck[j] = t;
    }
    return deck;
  }

  /* ------------------------------------------------------------- geometry */

  var VBW = 300, VBH = 128;
  var K = 0.5;            /* px per km — equal on both axes, so drawn dip is true dip */
  var XT = 79;            /* x of the trench (0 km) */
  var SURF = 44;          /* y of the ground / sea floor */
  var PLOT_L = 24, PLOT_R = 299, PLOT_B = 124;
  var MAXD = (PLOT_B - SURF) / K;   /* 170 km of depth on the section */
  var MAXKM = (PLOT_R - XT) / K;    /* 440 km inland */

  function X(km) { return XT + km * K; }
  function Y(d) { return SURF + d * K; }

  function slabPath(dip) {
    var t = Math.tan(rad(dip));
    var endKm = Math.min(MAXKM, (MAXD - 2) / t);
    return 'M ' + PLOT_L + ' ' + (SURF + 2.2) + ' L ' + XT + ' ' + (SURF + 2.2) +
      ' L ' + X(endKm).toFixed(1) + ' ' + Y(endKm * t).toFixed(1);
  }

  /* ------------------------------------------------------------------ view */

  function el(name, attrs) {
    var e = document.createElementNS(NS, name), k;
    for (k in attrs) if (attrs.hasOwnProperty(k)) e.setAttribute(k, attrs[k]);
    return e;
  }
  function txt(x, y, s, size, fill, anchor) {
    var e = el('text', { x: x, y: y, 'font-size': size, fill: fill, 'text-anchor': anchor || 'middle' });
    e.textContent = s;
    return e;
  }

  function css(accent, reduced) {
    return '.' + CLS + '{background:#fff;border:1px solid #e8e3db;border-radius:16px;' +
      'padding:1rem;font-family:Inter,system-ui,-apple-system,sans-serif;color:#2d2a26;' +
      'box-sizing:border-box;max-width:100%;}' +
      '.' + CLS + ' *{box-sizing:border-box;}' +
      '.' + CLS + ' .k{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;' +
      'text-transform:uppercase;color:' + accent + ';}' +
      '.' + CLS + ' .t{margin:.2rem 0 .45rem;font-family:"Source Serif 4",Georgia,serif;' +
      'font-weight:600;font-size:1.2rem;line-height:1.2;}' +
      '.' + CLS + ' .frame{margin:0 0 .35rem;font-size:.84rem;line-height:1.45;color:#5b564e;}' +
      '.' + CLS + ' .ask{margin:0 0 .55rem;font-size:.88rem;line-height:1.4;font-weight:600;}' +
      '.' + CLS + ' .stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;' +
      'max-width:366px;margin:0 auto .55rem;overflow:hidden;}' +
      '.' + CLS + ' .stage svg{display:block;width:100%;height:auto;}' +
      '.' + CLS + ' .opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));' +
      'gap:.45rem;margin:0 0 .55rem;}' +
      '.' + CLS + ' .o{font:600 .82rem Inter,system-ui,sans-serif;color:#2d2a26;background:#faf8f5;' +
      'border:1px solid #ddd7cd;border-radius:10px;padding:.5rem .6rem;min-height:38px;cursor:pointer;' +
      'font-variant-numeric:tabular-nums;text-align:center;' + (reduced ? '' : 'transition:background .12s,border-color .12s;') + '}' +
      '.' + CLS + ' .o[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}' +
      '.' + CLS + ' .o.is-ans{border-color:' + accent + ';box-shadow:inset 0 0 0 1px ' + accent + ';}' +
      '.' + CLS + ' .o[disabled]{cursor:default;opacity:.92;}' +
      '.' + CLS + ' .act{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin:0 0 .5rem;}' +
      '.' + CLS + ' .go{font:600 .82rem Inter,system-ui,sans-serif;background:#2d2a26;color:#fff;' +
      'border:1px solid #2d2a26;border-radius:10px;padding:.5rem .95rem;cursor:pointer;}' +
      '.' + CLS + ' .run{font-size:.78rem;color:#8d8880;font-variant-numeric:tabular-nums;min-height:1em;}' +
      '.' + CLS + ' .cap{margin:0;font-size:.84rem;line-height:1.5;color:#2d2a26;min-height:68px;}' +
      '.' + CLS + ' .cap .v{font-weight:700;}' +
      '.' + CLS + ' .cap .rt{color:#4f7d63;}' +
      '.' + CLS + ' .cap.rest{color:#8d8880;}' +
      '.' + CLS + ' .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);' +
      'white-space:nowrap;margin:-1px;padding:0;border:0;}';
  }

  /* ------------------------------------------------------------------ mount */

  window.SVWidget = {
    meta: {
      id: 'subduction-angle',
      title: 'Follow the slab down',
      teaches: 'A subducting plate descends at a shallow angle and stays in contact, so the trench, the deepening earthquake foci and the volcanic arc all sit where the slab’s geometry puts them.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#a2563c';
      var reduced = !!ctx.reducedMotion;

      var wrap = document.createElement('div');
      wrap.className = CLS;
      var style = document.createElement('style');
      style.textContent = css(accent, reduced);
      wrap.appendChild(style);

      var kick = document.createElement('p'); kick.className = 'k'; kick.textContent = 'Destructive margin';
      var ttl = document.createElement('h3'); ttl.className = 't'; ttl.textContent = 'Follow the slab down';
      var frame = document.createElement('p'); frame.className = 'frame';
      var ask = document.createElement('p'); ask.className = 'ask';
      wrap.appendChild(kick); wrap.appendChild(ttl); wrap.appendChild(frame); wrap.appendChild(ask);

      /* ---- stage ---- */
      var stage = document.createElement('div'); stage.className = 'stage';
      var svg = el('svg', {
        viewBox: '0 0 ' + VBW + ' ' + VBH, role: 'img',
        'aria-label': 'Cross-section through a destructive plate margin'
      });
      stage.appendChild(svg); wrap.appendChild(stage);

      /* static furniture */
      svg.appendChild(el('rect', { x: PLOT_L, y: SURF, width: PLOT_R - PLOT_L, height: PLOT_B - SURF, fill: '#f1ebe1' }));

      [50, 100, 150].forEach(function (d) {
        svg.appendChild(el('line', {
          x1: PLOT_L, y1: Y(d), x2: PLOT_R, y2: Y(d),
          stroke: d === MELT ? '#cfc4b2' : '#e0d9cd', 'stroke-width': .7,
          'stroke-dasharray': d === MELT ? '4 3' : '2 4'
        }));
        svg.appendChild(txt(PLOT_L - 3, Y(d) + 3.4, String(d), 9.5, '#8d8880', 'end'));
      });
      [100, 200, 300, 400].forEach(function (km) {
        svg.appendChild(el('line', {
          x1: X(km), y1: SURF, x2: X(km), y2: PLOT_B,
          stroke: '#e0d9cd', 'stroke-width': .7, 'stroke-dasharray': '2 4'
        }));
      });
      svg.appendChild(txt(PLOT_R, Y(MELT) - 3.5, 'melting depth', 9, '#9a938a', 'end'));

      /* sea */
      svg.appendChild(el('rect', { x: PLOT_L, y: SURF - 10, width: XT - PLOT_L, height: 10, fill: '#dce6ea' }));
      svg.appendChild(el('path', {
        d: 'M ' + (PLOT_L + 10) + ' ' + (SURF - 4.5) + ' L ' + (PLOT_L + 30) + ' ' + (SURF - 4.5) +
          ' M ' + (PLOT_L + 26) + ' ' + (SURF - 7) + ' L ' + (PLOT_L + 31) + ' ' + (SURF - 4.5) +
          ' L ' + (PLOT_L + 26) + ' ' + (SURF - 2),
        stroke: '#7d8f97', 'stroke-width': 1.1, fill: 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round'
      }));

      /* slabs */
      var oldSlab = el('path', { d: '', stroke: '#b3aa9b', 'stroke-width': 3.4, fill: 'none', 'stroke-dasharray': '5 3', 'stroke-linecap': 'round' });
      var slab = el('path', { d: '', stroke: '#5f5a51', 'stroke-width': 4.4, fill: 'none', 'stroke-linejoin': 'round', 'stroke-linecap': 'round' });
      svg.appendChild(oldSlab); svg.appendChild(slab);

      /* continental plate over the top of the slab */
      svg.appendChild(el('path', {
        d: 'M ' + XT + ' ' + SURF + ' L ' + X(60) + ' ' + Y(15) + ' L ' + X(200) + ' ' + Y(32) +
          ' L ' + PLOT_R + ' ' + Y(35) + ' L ' + PLOT_R + ' ' + SURF + ' Z',
        fill: '#cfc6b5', stroke: '#b5aa96', 'stroke-width': .7
      }));
      svg.appendChild(el('line', { x1: PLOT_L, y1: SURF, x2: PLOT_R, y2: SURF, stroke: '#8d8880', 'stroke-width': .8 }));
      svg.appendChild(el('path', {
        d: 'M ' + X(-24) + ' ' + SURF + ' L ' + XT + ' ' + (SURF + 6) + ' L ' + X(10) + ' ' + SURF,
        fill: '#dce6ea', stroke: '#6e6960', 'stroke-width': .9, 'stroke-linejoin': 'round'
      }));
      svg.appendChild(txt(XT, SURF - 30, 'Trench', 10.5, '#2d2a26'));
      var contLbl = txt(X(250), Y(20), 'continental plate', 9.5, '#6b6459');
      svg.appendChild(contLbl);
      var oceanLbl = txt(PLOT_L, SURF - 14, 'oceanic plate (denser)', 9.5, '#6b6459', 'start');
      svg.appendChild(oceanLbl);

      /* candidate ticks */
      var ticks = el('g', {});
      svg.appendChild(ticks);

      /* the student's mark */
      var markG = el('g', { style: 'display:none' });
      var markLine = el('line', { stroke: '#2d2a26', 'stroke-width': 1, 'stroke-dasharray': '3 2' });
      var markShape = el('path', { d: '', fill: '#fff', stroke: '#2d2a26', 'stroke-width': 1.6, 'stroke-linejoin': 'round' });
      markG.appendChild(markLine); markG.appendChild(markShape);
      svg.appendChild(markG);

      /* the revealed truth */
      var revG = el('g', { style: 'display:none' });
      var revRise = el('line', { stroke: accent, 'stroke-width': 1.1, 'stroke-dasharray': '3 2' });
      var revDot = el('circle', { r: 2.6, fill: accent });
      var revShape = el('path', { d: '', fill: accent, stroke: accent, 'stroke-width': 1.2, 'stroke-linejoin': 'round' });
      var revQuakes = el('g', {});
      var revLbl = txt(0, 0, '', 9.5, accent);
      revG.appendChild(revRise); revG.appendChild(revQuakes); revG.appendChild(revDot);
      revG.appendChild(revShape); revG.appendChild(revLbl);
      svg.appendChild(revG);

      /* ---- controls ---- */
      var opts = document.createElement('div'); opts.className = 'opts';
      opts.setAttribute('role', 'group');
      opts.setAttribute('aria-label', 'Choose your answer');
      var btns = [];
      for (var i = 0; i < 4; i++) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'o'; b.setAttribute('aria-pressed', 'false');
        opts.appendChild(b); btns.push(b);
      }
      wrap.appendChild(opts);

      var act = document.createElement('div'); act.className = 'act';
      var go = document.createElement('button');
      go.type = 'button'; go.className = 'go'; go.textContent = 'Check';
      var run = document.createElement('span'); run.className = 'run';
      act.appendChild(go); act.appendChild(run); wrap.appendChild(act);

      var cap = document.createElement('p'); cap.className = 'cap rest';
      var sr = document.createElement('p'); sr.className = 'sr';
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(cap); wrap.appendChild(sr);
      root.appendChild(wrap);

      /* ---------------------------------------------------------- state */

      var deck = buildDeck(), deckAt = 0;
      var round = null, picked = null, locked = false;
      var streak = 0, attempted = 0, mastered = false;

      function pushState(extra) {
        var s = { streak: streak, mastered: mastered, attempted: attempted };
        if (round) { s.dip = round.dip; s.ask = round.type; s.answer = round.answer; }
        if (extra) for (var k in extra) if (extra.hasOwnProperty(k)) s[k] = extra[k];
        root.dataset.svState = JSON.stringify(s);
      }

      function volcano(x, y) {
        return 'M ' + (x - 6.5) + ' ' + y + ' L ' + x + ' ' + (y - 9) + ' L ' + (x + 6.5) + ' ' + y + ' Z';
      }
      function ring(x, y) {
        return 'M ' + (x - 3.4) + ' ' + y + ' a 3.4 3.4 0 1 0 6.8 0 a 3.4 3.4 0 1 0 -6.8 0';
      }

      function drawTicks() {
        while (ticks.firstChild) ticks.removeChild(ticks.firstChild);
        if (round.type === 'depth') {
          ticks.appendChild(el('line', {
            x1: X(round.site), y1: SURF - 5, x2: X(round.site), y2: Y(slabDepth(round.dip, round.site)),
            stroke: '#a49b8c', 'stroke-width': .9, 'stroke-dasharray': '3 3'
          }));
          ticks.appendChild(el('circle', { cx: X(round.site), cy: SURF, r: 2.2, fill: '#2d2a26' }));
          ticks.appendChild(txt(Math.min(X(round.site), PLOT_R - 26), SURF - 14, round.site + ' km', 9.5, '#6b6459'));
        } else {
          round.options.forEach(function (km) {
            ticks.appendChild(el('line', {
              x1: X(km), y1: SURF - 4.5, x2: X(km), y2: SURF, stroke: '#a49b8c', 'stroke-width': 1.1
            }));
          });
          if (round.type === 'change') {
            ticks.appendChild(el('path', {
              d: volcano(X(round.oldArc), SURF), fill: 'none', stroke: '#b3aa9b', 'stroke-width': 1.3, 'stroke-linejoin': 'round'
            }));
          }
        }
      }

      function drawMark() {
        if (picked === null) { markG.style.display = 'none'; return; }
        markG.style.display = '';
        if (round.type === 'depth') {
          var x = X(round.site), y = Y(picked);
          markLine.setAttribute('x1', x); markLine.setAttribute('y1', SURF);
          markLine.setAttribute('x2', x); markLine.setAttribute('y2', y);
          markLine.style.display = '';
          markShape.setAttribute('d', ring(x, y));
        } else {
          markLine.style.display = 'none';
          markShape.setAttribute('d', volcano(X(picked), SURF));
        }
      }

      function drawReveal() {
        var i;
        while (revQuakes.firstChild) revQuakes.removeChild(revQuakes.firstChild);
        oceanLbl.style.display = 'none';
        if (round.type === 'depth') {
          var xs = X(round.site), ys = Y(round.answer);
          revRise.setAttribute('x1', PLOT_L + 4); revRise.setAttribute('y1', ys);
          revRise.setAttribute('x2', xs); revRise.setAttribute('y2', ys);
          revDot.setAttribute('cx', xs); revDot.setAttribute('cy', ys);
          revShape.setAttribute('d', '');
          [0.3, 0.6, 1.35].forEach(function (f) {
            var km = round.site * f;
            var d = km * Math.tan(rad(round.dip));
            if (km > MAXKM || d > MAXD - 3) return;
            revQuakes.appendChild(el('circle', { cx: X(km), cy: Y(d), r: 1.7, fill: accent, opacity: .55 }));
          });
          revLbl.setAttribute('x', Math.min(Math.max(xs, PLOT_L + 26), PLOT_R - 4));
          revLbl.setAttribute('y', Math.min(ys + 12, PLOT_B - 3));
          revLbl.setAttribute('text-anchor', 'middle');
          revLbl.textContent = round.answer + ' km deep';
        } else {
          var xa = X(round.answer), ya = Y(slabDepth(round.dip, round.answer));
          revRise.setAttribute('x1', xa); revRise.setAttribute('y1', ya);
          revRise.setAttribute('x2', xa); revRise.setAttribute('y2', SURF);
          revDot.setAttribute('cx', xa); revDot.setAttribute('cy', ya);
          revShape.setAttribute('d', volcano(xa, SURF));
          revLbl.setAttribute('x', Math.min(Math.max(xa, PLOT_L + 22), PLOT_R - 22));
          revLbl.setAttribute('y', SURF - 14);
          revLbl.setAttribute('text-anchor', 'middle');
          revLbl.textContent = 'volcanoes';
        }
        revG.style.display = '';
      }

      /* ------------------------------------------------------- feedback */

      function verdict(ok, body) {
        cap.className = 'cap';
        cap.innerHTML = '';
        var v = document.createElement('span');
        v.className = 'v' + (ok ? ' rt' : '');
        v.textContent = ok ? 'Right — ' : 'Not quite — ';
        cap.appendChild(v);
        cap.appendChild(document.createTextNode(body));
        sr.textContent = (ok ? 'Right. ' : 'Not quite. ') + body;
      }

      function message(ok, pick) {
        var r = round, d;
        if (r.type === 'arc') {
          if (ok) {
            return r.answer + ' km from the trench. A ' + r.dip + '° slab only reaches 100 km down — where melting ' +
              'starts — that far inland, so the volcanic arc sits back from the trench, not on it.';
          }
          if (pick === 0) {
            return 'you put the volcanoes at the trench itself. There the slab has barely started down, ' +
              'far too shallow to melt anything. It gets to 100 km deep ' + r.answer + ' km inland, and that is where the volcanoes rise.';
          }
          d = slabDepth(r.dip, pick);
          if (pick < r.answer) {
            return 'you said ' + pick + ' km. Under there the ' + r.dip + '° slab is only ' + d +
              ' km down, short of the 100 km melting depth. It gets that deep ' + r.answer + ' km inland, so the volcanoes sit further back.';
          }
          return 'you said ' + pick + ' km. By there the slab is already ' + d +
            ' km down — it passed the 100 km melting depth back at ' + r.answer + ' km, so that is where the volcanoes are.';
        }
        if (r.type === 'depth') {
          if (ok) {
            return 'about ' + r.answer + ' km. ' + r.site + ' km inland the ' + r.dip + '° slab has already dived ' +
              r.answer + ' km, and the quakes happen along the slab. Go further inland and the foci get deeper still.';
          }
          if (pick === 10) {
            return 'you said about 10 km, which keeps every focus shallow. The foci follow the slab down: ' +
              r.site + ' km inland it is already ' + r.answer + ' km deep, so the quakes there are ' + r.answer + ' km deep too.';
          }
          return 'you said ' + pick + ' km. A ' + r.dip + '° slab drops about ' + snap5(100 * Math.tan(rad(r.dip))) +
            ' km for every 100 km inland, so at ' + r.site + ' km it is ' + r.answer + ' km down — and the foci sit on the slab.';
        }
        /* change */
        var closer = r.answer < r.oldArc;
        var delta = Math.abs(r.answer - r.oldArc);
        var dir = closer ? 'closer to the trench' : 'further inland';
        var than = (closer ? 'nearer the trench than' : 'further inland than') + ' the old ' + r.oldArc + ' km';
        if (ok) {
          return r.answer + ' km. The ' + (closer ? 'steeper' : 'shallower') + ' ' + r.dip + '° slab reaches 100 km depth ' +
            (closer ? 'sooner' : 'later') + ', so the volcanic arc moves ' + delta + ' km ' + dir + '.';
        }
        if (pick === r.oldArc) {
          return 'you left the volcanoes at ' + r.oldArc + ' km. The melting depth has not moved, but the route to it has: ' +
            'a ' + r.dip + '° slab is 100 km down after ' + r.answer + ' km, so they shift ' + delta + ' km ' + dir + '.';
        }
        return 'you said ' + pick + ' km. A ' + r.dip + '° slab is 100 km down after ' + r.answer +
          ' km, so that is where the volcanoes rise — ' + delta + ' km ' + than + '.';
      }

      /* ----------------------------------------------------------- rounds */

      function newRound() {
        if (deckAt >= deck.length) { deck = buildDeck(); deckAt = 0; }
        round = deck[deckAt++];
        picked = null; locked = false;

        if (round.type === 'arc') {
          frame.textContent = 'An oceanic plate is denser, so it dives under the continent — here at ' + round.dip +
            '°. Melting begins about 100 km down.';
          ask.textContent = 'How far from the trench do the volcanoes rise?';
        } else if (round.type === 'depth') {
          frame.textContent = 'An oceanic plate dives under the continent at ' + round.dip +
            '°. Earthquakes happen all along the top of the slab.';
          ask.textContent = 'How deep are the foci beneath a town ' + round.site + ' km inland from the trench?';
        } else {
          frame.textContent = 'The same margin, but the slab now dips at ' + round.dip + '° instead of ' +
            round.oldDip + '° (dashed). Melting still begins about 100 km down.';
          ask.textContent = 'The volcanoes used to rise ' + round.oldArc + ' km from the trench. Where do they rise now?';
        }

        slab.setAttribute('d', slabPath(round.dip));
        if (round.type === 'change') {
          oldSlab.setAttribute('d', slabPath(round.oldDip));
          oldSlab.style.display = '';
        } else {
          oldSlab.style.display = 'none';
        }
        oceanLbl.style.display = '';
        contLbl.style.display = '';
        revG.style.display = 'none';
        markG.style.display = 'none';
        drawTicks();

        btns.forEach(function (b, n) {
          var v = round.options[n];
          b.textContent = v + ' km';
          b.value = String(v);
          b.disabled = false;
          b.setAttribute('aria-pressed', 'false');
          b.classList.remove('is-ans');
          b.setAttribute('aria-label', round.type === 'depth' ? v + ' km deep' : v + ' km from the trench');
        });

        go.textContent = 'Check';
        cap.className = 'cap rest';
        cap.textContent = 'Everything at this margin follows the path of the slab.';
        pushState();
      }

      function commit() {
        if (picked === null) {
          cap.className = 'cap rest';
          cap.textContent = 'Nothing marked yet — choose where it goes on the section.';
          sr.textContent = 'Nothing marked yet.';
          return;
        }
        locked = true;
        attempted++;
        var ok = picked === round.answer;
        if (ok) { streak++; } else { streak = 0; }
        var justMastered = ok && streak >= 3 && !mastered;
        if (streak >= 3) mastered = true;

        drawReveal();
        var body = message(ok, picked);
        if (justMastered) {
          body = round.answer + ' km. Three in a row — you have it. The slab stays in contact as it slides down, so the ' +
            'trench sits at the margin, the foci deepen inland and the volcanoes stand back.';
        }
        verdict(ok, body);

        btns.forEach(function (b) {
          b.disabled = true;
          if (Number(b.value) === round.answer) b.classList.add('is-ans');
        });
        run.textContent = mastered
          ? (streak === 0 ? 'You have it — that one caught you out.' : 'You have it — keep going if you like.')
          : (streak === 0
            ? (attempted > 1 ? 'Run reset — three in a row to finish.' : '')
            : streak + ' right in a row — ' + (3 - streak) + ' more and you have it.');
        go.textContent = mastered ? 'Another anyway' : 'Next';
        pushState({ picked: picked, right: ok });
      }

      /* ------------------------------------------------------------ wiring */

      btns.forEach(function (b) {
        b.addEventListener('click', function () {
          if (locked) return;
          picked = Number(b.value);
          btns.forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
          drawMark();
          cap.className = 'cap rest';
          cap.textContent = round.type === 'depth'
            ? 'Marked: foci ' + picked + ' km down beneath the town.'
            : 'Marked: volcanoes ' + picked + ' km from the trench.';
          sr.textContent = cap.textContent;
          pushState({ picked: picked });
        });
      });

      go.addEventListener('click', function () {
        if (locked) { newRound(); btns[0].focus(); } else { commit(); }
      });

      newRound();
      pushState();
    }
  };
})();
