/* state-change-energy-plateau — self-contained lesson widget.
   No imports, no network, no storage. Everything scoped to .svw-scep. */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';
  var RC = 'svw-scep';
  var SECS = 120; // every round looks two minutes ahead

  /* ---------------------------------------------------------------- data */
  /* changing: false | 'melt' | 'freeze' | 'boil' | 'condense'
     The answer is DERIVED from these fields, never written down:
       flat  <=> changing !== false  (two states present at a transition temp)
       energy: potential store if flat, kinetic store otherwise            */
  var ROUNDS = [
    { sub: 'Water', mp: 0, bp: 100, now: -15, dir: 'heat', changing: false, pow: 50,
      ctx: '−15 °C — all ice, well below 0 °C', span: [-30, 25], mode: 's' },
    { sub: 'Water', mp: 0, bp: 100, now: -5, dir: 'heat', changing: false, pow: 50,
      ctx: '−5 °C — ice, not yet at its melting point', span: [-20, 25], mode: 's' },
    { sub: 'Water', mp: 0, bp: 100, now: 0, dir: 'heat', changing: 'melt', pow: 50,
      ctx: '0 °C — ice and water together', span: [-20, 25], mode: 'sl', f0: 0.67, f1: 0.33 },
    { sub: 'Water', mp: 0, bp: 100, now: 0, dir: 'heat', changing: false, pow: 50,
      ctx: '0 °C — the last of the ice has just melted', span: [-15, 30], mode: 'l' },
    { sub: 'Water', mp: 0, bp: 100, now: 45, dir: 'heat', changing: false, pow: 50,
      ctx: '45 °C — all liquid', span: [20, 110], mode: 'l' },
    { sub: 'Water', mp: 0, bp: 100, now: 100, dir: 'heat', changing: 'boil', pow: 50,
      ctx: '100 °C — bubbling, liquid turning to steam', span: [75, 130], mode: 'lg', f0: 0.67, f1: 0.33 },
    { sub: 'Water', mp: 0, bp: 100, now: 100, dir: 'heat', changing: false, pow: 50,
      ctx: '100 °C — all steam now, in a sealed tube', span: [80, 145], mode: 'g' },
    { sub: 'Water', mp: 0, bp: 100, now: 0, dir: 'cool', changing: 'freeze', pow: 20,
      ctx: '0 °C — ice and water together, in a freezer', span: [-20, 25], mode: 'sl', f0: 0.33, f1: 0.67 },
    { sub: 'Water', mp: 0, bp: 100, now: 100, dir: 'cool', changing: 'condense', pow: 20,
      ctx: '100 °C — steam condensing on a cold plate', span: [75, 130], mode: 'lg', f0: 0.33, f1: 0.67 },
    { sub: 'Water', mp: 0, bp: 100, now: 70, dir: 'cool', changing: false, pow: 20,
      ctx: '70 °C — all liquid, in a cold room', span: [10, 95], mode: 'l' },
    { sub: 'Water', mp: 0, bp: 100, now: 5, dir: 'cool', changing: false, pow: 20,
      ctx: '5 °C — liquid water, not yet at 0 °C', span: [-15, 35], mode: 'l' },
    { sub: 'Stearic acid', mp: 69, bp: 361, now: 69, dir: 'cool', changing: 'freeze', pow: 15,
      ctx: '69 °C — molten, first crystals appearing', span: [40, 100], mode: 'sl', f0: 0.25, f1: 0.58 },
    { sub: 'Stearic acid', mp: 69, bp: 361, now: 40, dir: 'cool', changing: false, pow: 15,
      ctx: '40 °C — a solid block, cooling in air', span: [10, 85], mode: 's' },
    { sub: 'Stearic acid', mp: 69, bp: 361, now: 90, dir: 'heat', changing: false, pow: 30,
      ctx: '90 °C — molten, being heated further', span: [55, 125], mode: 'l' },
    { sub: 'Lead', mp: 327, bp: 1749, now: 327, dir: 'heat', changing: 'melt', pow: 400,
      ctx: '327 °C — about half of it is still solid', span: [270, 390], mode: 'sl', f0: 0.5, f1: 0.25 },
    { sub: 'Lead', mp: 327, bp: 1749, now: 150, dir: 'heat', changing: false, pow: 400,
      ctx: '150 °C — a solid block in a furnace', span: [80, 370], mode: 's' },
    { sub: 'Lead', mp: 327, bp: 1749, now: 500, dir: 'cool', changing: false, pow: 200,
      ctx: '500 °C — molten, cooling in air', span: [300, 570], mode: 'l' }
  ];

  /* keep only rounds whose data is internally consistent */
  ROUNDS = ROUNDS.filter(function (r) {
    if (!r.changing) return true;
    if (r.changing === 'melt' || r.changing === 'freeze') return r.now === r.mp;
    return r.now === r.bp;
  });

  function truthOf(r) {
    var flat = !!r.changing;
    return { t: flat ? 'flat' : (r.dir === 'heat' ? 'rise' : 'fall'), e: flat ? 'pot' : 'kin' };
  }

  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }
  function degC(n) { return (n < 0 ? '−' + Math.abs(n) : String(n)) + ' °C'; }

  /* ------------------------------------------------------------ feedback */
  function feedback(r, pt, pe) {
    var tr = truthOf(r), J = fmt(r.pow * SECS), heat = r.dir === 'heat';
    if (pt === tr.t && pe === tr.e) {
      if (tr.t === 'flat') {
        return { ok: true,
          v: heat ? 'Flat — and ' + J + ' J still went in.'
                  : 'Flat — and ' + J + ' J still came out.',
          b: r.changing === 'boil'
              ? 'It went to the potential store, pulling the molecules apart — they are not broken up themselves. Average kinetic energy is unchanged.'
              : r.changing === 'condense'
              ? 'It came from the potential store as the molecules pulled together — they were never broken up. Average kinetic energy is unchanged.'
              : heat
              ? 'It went to the potential store, pulling particles apart against the forces holding them. Average kinetic energy is unchanged: latent heat.'
              : 'It came from the potential store as particles pulled together and the forces re-formed. Average kinetic energy is unchanged: latent heat.' };
      }
      if (tr.t === 'rise') {
        return { ok: true, v: 'Rising — nothing is changing state.',
          b: 'So all of the energy goes to the kinetic store. The particles speed up, and that is what the thermometer reads.' };
      }
      return { ok: true, v: 'Falling — nothing is changing state.',
        b: 'So the energy leaving comes out of the kinetic store. The particles slow down, and the thermometer follows.' };
    }

    if (pe === 'none') {
      return { ok: false,
        v: heat ? 'The heater has not stopped.' : 'It has not stopped losing energy.',
        b: heat
            ? 'The energy is not lost: ' + J + ' J still arrived, and it is now held in the pulled-apart arrangement of the particles.'
            : 'About ' + J + ' J still left, and it came out of the store held in the arrangement of the particles as they pulled together.' };
    }

    if (pt !== tr.t) {
      if (tr.t === 'flat') {
        return { ok: false, v: 'Not quite — the line stays flat.',
          b: (heat ? J + ' J still arrived. ' : 'About ' + J + ' J still left. ') +
             'While two states sit together at ' + degC(r.now) + ', every joule goes to the forces between particles, not to speed.' };
      }
      if (tr.t === 'rise') {
        return { ok: false, v: 'Not quite — the line rises.',
          b: 'Nothing is changing state, so there are no forces to overcome. All of the energy goes to the kinetic store and particles speed up.' };
      }
      return { ok: false, v: 'Not quite — the line falls.',
        b: 'Nothing is changing state, so the energy leaving comes straight out of the kinetic store. The particles slow down.' };
    }

    if (tr.e === 'pot') {
      return { ok: false, v: 'The flat line was right.',
        b: 'If the energy were changing how fast the particles move, the thermometer would move too. A flat line means the potential store.' };
    }
    return { ok: false, v: 'The direction was right.',
      b: 'Nothing is changing state, so no forces are being overcome and none are re-forming. Every joule goes to the kinetic store.' };
  }

  /* --------------------------------------------------------- particle art */
  var SLOT_S = [], SLOT_L = [], SLOT_G = [], PHASE = [];
  (function () {
    var i, c, rw;
    for (i = 0; i < 12; i++) {
      c = i % 4; rw = Math.floor(i / 4);
      SLOT_S.push({ x: 0.045 + c * 0.072, y: 0.20 + rw * 0.30 });
    }
    var lx = [0.05, 0.14, 0.235, 0.10, 0.20, 0.29, 0.06, 0.16, 0.26, 0.12, 0.22, 0.31];
    var ly = [0.30, 0.22, 0.33, 0.55, 0.48, 0.60, 0.80, 0.74, 0.84, 0.98, 0.92, 0.99];
    for (i = 0; i < 12; i++) SLOT_L.push({ x: lx[i], y: Math.min(0.92, ly[i] * 0.9) });
    var gx = [0.04, 0.17, 0.30, 0.43, 0.56, 0.69, 0.82, 0.95, 0.11, 0.37, 0.63, 0.89];
    var gy = [0.55, 0.15, 0.78, 0.32, 0.90, 0.20, 0.62, 0.40, 0.95, 0.06, 0.48, 0.85];
    for (i = 0; i < 12; i++) SLOT_G.push({ x: gx[i], y: gy[i] });
    for (i = 0; i < 12; i++) PHASE.push((i * 2.399963) % 6.2831853);
  })();

  function slotFor(mode, i, frac) {
    var n, s;
    if (mode === 's') return SLOT_S[i];
    if (mode === 'l') return SLOT_L[i];
    if (mode === 'g') return SLOT_G[i];
    n = Math.round(12 * frac);
    if (mode === 'sl') {
      if (i < n) return SLOT_S[i];
      s = SLOT_L[i]; return { x: s.x + 0.60, y: s.y };
    }
    if (i < n) { s = SLOT_L[i]; return { x: s.x + 0.02, y: 0.45 + s.y * 0.5 }; }
    return SLOT_G[i];
  }

  function lerp(a, b, t) { return a + (b - a) * t; }

  /* ----------------------------------------------------------------- css */
  var CSS = [
    '.' + RC + '{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
    '.' + RC + ' *{box-sizing:border-box}',
    '.' + RC + ' .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--svw-a);margin:0 0 2px}',
    '.' + RC + ' .t{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.2;margin:0 0 8px}',
    '.' + RC + ' .frame{margin:0 0 10px}',
    '.' + RC + ' .sample{font-size:.82rem;font-weight:600;color:#2d2a26;margin:0 0 3px;font-variant-numeric:tabular-nums}',
    '.' + RC + ' .ask{font-size:.82rem;line-height:1.45;color:#5b564e;margin:0}',
    '.' + RC + ' .step{display:inline-block;min-width:17px;height:17px;line-height:17px;text-align:center;border-radius:5px;background:#efe9e0;color:#8d8880;font-size:.68rem;font-weight:700;margin-right:7px;vertical-align:1px}',
    '.' + RC + ' .step.now{background:#2d2a26;color:#fff}',
    '.' + RC + ' .step.done{background:var(--svw-a-soft);color:#2d2a26}',
    '.' + RC + ' .wrap{display:grid;gap:12px;align-items:start}',
    '.' + RC + ' .wrap>*{min-width:0}',
    '.' + RC + '.is-wide .wrap{grid-template-columns:1.08fr 1fr;gap:18px}',
    '.' + RC + ' .stage{min-width:0;background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;padding:8px 11px 6px}',
    '.' + RC + ' .plot{position:relative;width:100%;min-width:0;overflow:hidden}',
    '.' + RC + ' .plot svg{position:absolute;left:0;top:0;width:100%;height:100%;display:block}',
    '.' + RC + ' svg text{font-family:Inter,system-ui,sans-serif}',
    '.' + RC + ' .lab{font-size:.74rem;font-weight:600;color:#8d8880;margin:0 0 4px}',
    '.' + RC + ' .row3{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}',
    '.' + RC + ' .row3 .b{min-width:0;overflow:hidden;text-overflow:ellipsis}',
    '.' + RC + ' .col{display:grid;gap:5px;margin:0 0 7px}',
    '.' + RC + ' .b{font-family:inherit;font-size:.8rem;font-weight:600;line-height:1.25;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.44rem .55rem;cursor:pointer;text-align:left;-webkit-appearance:none;appearance:none}',
    '.' + RC + ' .row3 .b{text-align:center;padding:.48rem .25rem;font-size:.78rem}',
    '.' + RC + ' .b:hover{border-color:#c9c1b4}',
    '.' + RC + ' .b.on{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.' + RC + ' .b:disabled{cursor:default;color:#a49d92}',
    '.' + RC + ' .b.true{background:var(--svw-a-soft);border-color:var(--svw-a);color:#2d2a26;box-shadow:inset 0 0 0 1px var(--svw-a)}',
    '.' + RC + ' .b.miss{background:#fff;border:1px dashed #c9c1b4;color:#8d8880;box-shadow:none}',
    '.' + RC + ' .picked{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px;font-size:.79rem;color:#5b564e;margin:0 0 6px}',
    '.' + RC + ' .picked b{color:#2d2a26;font-weight:600}',
    '.' + RC + ' .lk{font-family:inherit;font-size:.75rem;font-weight:600;color:#5b564e;background:none;border:0;border-bottom:1px solid #c9c1b4;padding:0;cursor:pointer}',
    '.' + RC + ' .act{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:2px 0 0}',
    '.' + RC + ' .go{font-family:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.5rem 1.05rem;cursor:pointer}',
    '.' + RC + ' .streak{font-size:.75rem;color:#8d8880;flex:1 1 8ch;min-width:0}',
    '.' + RC + ' .streak.m{color:#4f7d63;font-weight:600}',
    '.' + RC + ' .cap{font-size:.84rem;line-height:1.45;color:#5b564e;margin:6px 0 0;min-height:44px}',
    '.' + RC + ' .cap b{display:block;color:#2d2a26;font-weight:600;margin:0 0 2px}',
    '.' + RC + ' .cap b.g{color:#4f7d63}',
    '.' + RC + ' .sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.' + RC + ' .hide{display:none}'
  ].join('');

  /* --------------------------------------------------------------- mount */
  window.SVWidget = {
    meta: {
      id: 'state-change-energy-plateau',
      title: 'Where does the energy go?',
      teaches: 'While a substance is changing state the supplied energy goes to the potential store, overcoming the forces between particles, so the average kinetic energy — and the temperature — holds steady.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = (ctx.accent || '').trim() ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6f4a';
      var soft = /^#[0-9a-fA-F]{6}$/.test(accent) ? accent + '2e' : accent;
      var reduced = !!ctx.reducedMotion;

      root.classList.add(RC);
      root.style.setProperty('--svw-a', accent);
      root.style.setProperty('--svw-a-soft', soft);

      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      /* ---- markup, built once ---- */
      function mk(tag, cls, txt) {
        var e = document.createElement(tag);
        if (cls) e.className = cls;
        if (txt != null) e.textContent = txt;
        return e;
      }
      function sv(tag, attrs) {
        var e = document.createElementNS(NS, tag), k;
        for (k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) e.setAttribute(k, attrs[k]);
        return e;
      }

      root.appendChild(mk('p', 'k', 'Heating and cooling curves'));
      root.appendChild(mk('h3', 't', 'Where does the energy go?'));

      var frame = mk('div', 'frame');
      var sampleEl = mk('p', 'sample', '');
      var askEl = mk('p', 'ask', '');
      frame.appendChild(sampleEl);
      frame.appendChild(askEl);
      root.appendChild(frame);

      var wrap = mk('div', 'wrap');
      root.appendChild(wrap);

      var stage = mk('div', 'stage');

      var plotWrap = mk('div', 'plot');
      var svg = sv('svg', { xmlns: NS, role: 'img', preserveAspectRatio: 'none' });
      var svgTitle = sv('title', {});
      svgTitle.textContent = 'Temperature against time, with the next two minutes to predict.';
      svg.appendChild(svgTitle);
      plotWrap.appendChild(svg);
      stage.appendChild(plotWrap);
      wrap.appendChild(stage);

      var side = mk('div', 'side');
      wrap.appendChild(side);

      /* question 1 */
      var q1 = mk('div', 'q1');
      var q1lab = mk('p', 'lab');
      var step1 = mk('span', 'step', '1');
      q1lab.appendChild(step1);
      q1lab.appendChild(document.createTextNode('What does the thermometer do next?'));
      q1.appendChild(q1lab);
      var q1row = mk('div', 'row3');
      var TOPTS = [
        { k: 'rise', s: '↗ Rises' },
        { k: 'flat', s: '→ Stays flat' },
        { k: 'fall', s: '↘ Falls' }
      ];
      var tBtns = TOPTS.map(function (o) {
        var b = mk('button', 'b', o.s);
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', function () { pickTemp(o.k); });
        q1row.appendChild(b);
        return b;
      });
      q1.appendChild(q1row);
      side.appendChild(q1);

      /* collapsed summary of question 1 */
      var picked = mk('div', 'picked hide');
      var step1b = mk('span', 'step done', '1');
      picked.appendChild(step1b);
      picked.appendChild(mk('span', null, 'Thermometer:'));
      var pickedVal = mk('b', null, '');
      picked.appendChild(pickedVal);
      var changeBtn = mk('button', 'lk', 'change');
      changeBtn.type = 'button';
      changeBtn.addEventListener('click', function () { reopen(); });
      picked.appendChild(changeBtn);
      side.appendChild(picked);

      /* question 2 */
      var q2 = mk('div', 'q2 hide');
      var q2lab = mk('p', 'lab');
      var step2 = mk('span', 'step', '2');
      var q2labText = document.createTextNode('');
      q2lab.appendChild(step2);
      q2lab.appendChild(q2labText);
      q2.appendChild(q2lab);
      var q2col = mk('div', 'col');
      var eKeys = ['kin', 'pot', 'none'];
      var eBtns = eKeys.map(function (k) {
        var b = mk('button', 'b', '');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', function () { pickEnergy(k); });
        q2col.appendChild(b);
        return b;
      });
      q2.appendChild(q2col);
      side.appendChild(q2);

      /* action row */
      var act = mk('div', 'act');
      var go = mk('button', 'go', 'Check');
      go.type = 'button';
      go.addEventListener('click', function () { onGo(); });
      act.appendChild(go);
      var streakEl = mk('span', 'streak', '');
      act.appendChild(streakEl);
      side.appendChild(act);

      /* caption */
      var cap = mk('p', 'cap');
      var capV = mk('b', null, '');
      var capB = document.createTextNode('');
      cap.appendChild(capV);
      cap.appendChild(capB);
      side.appendChild(cap);

      var sr = mk('p', 'sr');
      sr.setAttribute('aria-live', 'polite');
      side.appendChild(sr);

      /* ---- svg scaffolding, built once ---- */
      var PH = 102, GAPY = 12, BH = 32, SVGH = PH + GAPY + BH;
      var padL = 36, padR = 12, padT = 18, padB = 16;

      var gBg = sv('rect', { fill: '#fff', stroke: '#efe9e0', rx: 8, x: 0, y: 0, width: 10, height: PH });
      svg.appendChild(gBg);
      var band = sv('rect', { fill: soft, x: 0, y: 0, width: 0, height: 0, rx: 3 });
      svg.appendChild(band);
      var guides = [0, 1].map(function () {
        var g = sv('g', {});
        var ln = sv('line', { stroke: '#c9c1b4', 'stroke-width': 1, 'stroke-dasharray': '3 4' });
        var tx = sv('text', { 'font-size': 11, fill: '#8d8880', stroke: '#faf8f5', 'stroke-width': 3,
          'paint-order': 'stroke', 'stroke-linejoin': 'round' });
        g.appendChild(ln); g.appendChild(tx); svg.appendChild(g);
        return { g: g, ln: ln, tx: tx };
      });
      var axisY = sv('line', { stroke: '#ddd7cd', 'stroke-width': 1 });
      var axisX = sv('line', { stroke: '#ddd7cd', 'stroke-width': 1 });
      svg.appendChild(axisY); svg.appendChild(axisX);
      var yLabs = [0, 1, 2].map(function () {
        var t = sv('text', { 'font-size': 11, fill: '#8d8880', 'text-anchor': 'end' });
        svg.appendChild(t); return t;
      });
      var axLab = sv('text', { 'font-size': 11, fill: '#8d8880', x: 1, y: 9 });
      axLab.textContent = 'T/°C';
      svg.appendChild(axLab);
      var bandLab = sv('text', { 'font-size': 11, fill: '#8d8880', 'text-anchor': 'middle' });
      bandLab.textContent = 'the next 2 minutes';
      svg.appendChild(bandLab);

      var ghost = sv('line', { stroke: '#8d8880', 'stroke-width': 2, 'stroke-dasharray': '5 4', 'stroke-linecap': 'round', visibility: 'hidden' });
      svg.appendChild(ghost);
      var real = sv('line', { stroke: accent, 'stroke-width': 2.6, 'stroke-linecap': 'round', visibility: 'hidden' });
      svg.appendChild(real);
      var ghostTag = sv('text', { 'font-size': 11, fill: '#8d8880', 'text-anchor': 'end', visibility: 'hidden' });
      ghostTag.textContent = 'you said';
      svg.appendChild(ghostTag);
      var marker = sv('circle', { r: 4.2, fill: accent, stroke: '#fff', 'stroke-width': 1.5 });
      svg.appendChild(marker);

      var legend = sv('text', { 'font-size': 11, fill: '#a49d92' });
      legend.textContent = 'the marks show speed';
      svg.appendChild(legend);
      var speedTag = sv('text', { 'font-size': 11, fill: accent, 'text-anchor': 'end', 'font-weight': 600 });
      svg.appendChild(speedTag);

      var parts = [];
      for (var pi = 0; pi < 12; pi++) {
        var ln2 = sv('line', { stroke: '#c9c1b4', 'stroke-width': 2, 'stroke-linecap': 'round' });
        var c2 = sv('circle', { r: 4, fill: '#8d8880' });
        svg.appendChild(ln2); svg.appendChild(c2);
        parts.push({ l: ln2, c: c2 });
      }

      /* ---- state ---- */
      var deck = [], round = null, pickT = null, pickE = null, revealed = false;
      var streak = 0, attempted = 0, mastered = false;
      var W = 320, geo = null, raf = 0, animT = 1;

      function shuffle(a) {
        for (var i = a.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
        }
        return a;
      }
      function nextRound() {
        if (!deck.length) {
          deck = shuffle(ROUNDS.slice());
          if (round && deck[deck.length - 1] === round && deck.length > 1) {
            var t = deck[0]; deck[0] = deck[deck.length - 1]; deck[deck.length - 1] = t;
          }
        }
        return deck.pop();
      }

      function state() {
        var tr = round ? truthOf(round) : { t: null, e: null };
        root.dataset.svState = JSON.stringify({
          id: 'state-change-energy-plateau',
          step: revealed ? 'revealed' : (q1.classList.contains('hide') ? 'energy' : 'temperature'),
          substance: round ? round.sub : null,
          at: round ? round.now : null,
          changingState: round ? (round.changing || false) : null,
          answer: revealed ? tr : null,
          picked: { temperature: pickT, energy: pickE },
          correct: revealed ? (pickT === tr.t && pickE === tr.e) : null,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      /* ---- geometry ---- */
      function measure() {
        var w = Math.round(root.clientWidth || 320);
        root.classList.toggle('is-wide', w >= 640);
        plotWrap.style.height = SVGH + 'px';
        W = Math.max(200, Math.round(plotWrap.clientWidth) || 200);
        svg.setAttribute('viewBox', '0 0 ' + W + ' ' + SVGH);
        var pl = padL, pr = W - padR, pt = padT, pb = PH - padB;
        geo = {
          pl: pl, pr: pr, pt: pt, pb: pb,
          x0: pl + (pr - pl) * 0.24,
          x1: pl + (pr - pl) * 0.88,
          bt: PH + GAPY, bh: BH
        };
      }

      function yOf(T) {
        var lo = round.span[0], hi = round.span[1];
        return geo.pb - (T - lo) / (hi - lo) * (geo.pb - geo.pt);
      }

      function drawFrame() {
        var g = geo, i;
        gBg.setAttribute('width', W);
        gBg.setAttribute('height', PH);
        band.setAttribute('x', g.x0); band.setAttribute('y', g.pt);
        band.setAttribute('width', g.x1 - g.x0); band.setAttribute('height', g.pb - g.pt);
        axisY.setAttribute('x1', g.pl); axisY.setAttribute('x2', g.pl);
        axisY.setAttribute('y1', g.pt); axisY.setAttribute('y2', g.pb);
        axisX.setAttribute('x1', g.pl); axisX.setAttribute('x2', g.pr);
        axisX.setAttribute('y1', g.pb); axisX.setAttribute('y2', g.pb);
        bandLab.setAttribute('x', (g.x0 + g.x1) / 2);
        bandLab.setAttribute('y', g.pb + 13);

        var lo = round.span[0], hi = round.span[1];
        var stp = (hi - lo) > 200 ? 50 : (hi - lo) > 60 ? 10 : 5;
        var vals = [lo, Math.round((lo + hi) / 2 / stp) * stp, hi];
        for (i = 0; i < 3; i++) {
          yLabs[i].setAttribute('x', g.pl - 5);
          yLabs[i].setAttribute('y', yOf(vals[i]) + 3.5);
          yLabs[i].textContent = (vals[i] < 0 ? '−' + Math.abs(vals[i]) : vals[i]);
        }

        var tps = [];
        if (round.mp > lo && round.mp < hi) tps.push({ T: round.mp, s: 'melts / freezes at ' + degC(round.mp) });
        if (round.bp > lo && round.bp < hi) tps.push({ T: round.bp, s: 'boils / condenses at ' + degC(round.bp) });
        for (i = 0; i < 2; i++) {
          if (i < tps.length) {
            var y = yOf(tps[i].T);
            guides[i].g.setAttribute('visibility', 'visible');
            guides[i].ln.setAttribute('x1', g.pl); guides[i].ln.setAttribute('x2', g.pr);
            guides[i].ln.setAttribute('y1', y); guides[i].ln.setAttribute('y2', y);
            guides[i].tx.setAttribute('x', g.x0 + 9);
            guides[i].tx.setAttribute('y', y - 8 < g.pt + 10 ? y + 15 : y - 8);
            guides[i].tx.textContent = tps[i].s;
          } else {
            guides[i].g.setAttribute('visibility', 'hidden');
          }
        }

        marker.setAttribute('cx', g.x0);
        marker.setAttribute('cy', yOf(round.now));

        legend.setAttribute('visibility', revealed ? 'hidden' : 'visible');
        legend.setAttribute('x', g.pl);
        legend.setAttribute('y', PH + 12);
        speedTag.setAttribute('x', g.pr);
        speedTag.setAttribute('y', PH + 12);
      }

      function endY(kind) {
        var g = geo, y0 = yOf(round.now);
        var span = (g.pb - g.pt) * 0.30;
        if (kind === 'rise') return Math.max(g.pt + 5, y0 - Math.min(span, y0 - g.pt - 5));
        if (kind === 'fall') return Math.min(g.pb - 5, y0 + Math.min(span, g.pb - y0 - 5));
        return y0;
      }

      function drawLines() {
        var g = geo, y0 = yOf(round.now);
        if (pickT) {
          ghost.setAttribute('visibility', 'visible');
          ghost.setAttribute('x1', g.x0); ghost.setAttribute('y1', y0);
          ghost.setAttribute('x2', g.x1); ghost.setAttribute('y2', endY(pickT));
        } else {
          ghost.setAttribute('visibility', 'hidden');
        }
        if (revealed) {
          var tr = truthOf(round), ye = endY(tr.t);
          var f = animT;
          real.setAttribute('visibility', 'visible');
          real.setAttribute('x1', g.x0); real.setAttribute('y1', y0);
          real.setAttribute('x2', g.x0 + (g.x1 - g.x0) * f);
          real.setAttribute('y2', y0 + (ye - y0) * f);
          var differ = pickT !== tr.t;
          ghostTag.setAttribute('visibility', differ ? 'visible' : 'hidden');
          if (differ) {
            ghostTag.setAttribute('x', g.x1);
            ghostTag.setAttribute('y', endY(pickT) + (endY(pickT) > ye ? 13 : -6));
          }
        } else {
          real.setAttribute('visibility', 'hidden');
          ghostTag.setAttribute('visibility', 'hidden');
        }
      }

      function speedAt(t) {
        var tr = truthOf(round);
        if (tr.t === 'flat') return 1;
        return tr.t === 'rise' ? 1 + 0.62 * t : 1 - 0.45 * t;
      }

      function drawParticles(t, jig) {
        var g = geo, bw = Math.min(g.pr - g.pl, 340), bx = g.pl, by = g.bt, bh = g.bh;
        var s = revealed ? speedAt(t) : 1;
        var frac = null;
        if (round.mode === 'sl' || round.mode === 'lg') {
          frac = revealed ? lerp(round.f0, round.f1, t) : round.f0;
        }
        var L = 2 + 12 * s;
        for (var i = 0; i < 12; i++) {
          var p = slotFor(round.mode, i, frac);
          var cx = bx + Math.min(0.985, Math.max(0.015, p.x)) * bw;
          var cy = by + 5 + Math.min(1, Math.max(0, p.y)) * (bh - 10);
          if (jig) {
            cx += 1.9 * s * Math.sin(PHASE[i] + jig * 0.013);
            cy += 1.6 * s * Math.cos(PHASE[i] * 1.7 + jig * 0.017);
          }
          parts[i].c.setAttribute('cx', cx);
          parts[i].c.setAttribute('cy', cy);
          parts[i].l.setAttribute('x1', cx - L / 2);
          parts[i].l.setAttribute('x2', cx + L / 2);
          parts[i].l.setAttribute('y1', cy);
          parts[i].l.setAttribute('y2', cy);
        }
      }

      function speedWord() {
        var tr = truthOf(round);
        if (tr.t === 'flat') return 'same average speed';
        return tr.t === 'rise' ? 'faster on average' : 'slower on average';
      }

      /* ---- interaction ---- */
      function pickTemp(k) {
        if (revealed) return;
        pickT = k;
        tBtns.forEach(function (b, i) {
          var on = TOPTS[i].k === k;
          b.classList.toggle('on', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        pickedVal.textContent = TOPTS.filter(function (o) { return o.k === k; })[0].s.slice(2);
        picked.classList.remove('hide');
        q1.classList.add('hide');
        q2.classList.remove('hide');
        step1.className = 'step done';
        step2.className = 'step now';
        drawLines();
        state();
        say('Prediction sketched on the graph: ' + pickedVal.textContent + '. Now choose where the energy goes.');
        if (!pickE) eBtns[0].focus();
      }

      function reopen() {
        if (revealed) return;
        q1.classList.remove('hide');
        picked.classList.add('hide');
        step1.className = 'step now';
        state();
        tBtns[0].focus();
      }

      function pickEnergy(k) {
        if (revealed) return;
        pickE = k;
        eBtns.forEach(function (b, i) {
          var on = eKeys[i] === k;
          b.classList.toggle('on', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        state();
        say('Energy destination chosen. Press Check.');
      }

      function setCap(v, b, good) {
        capV.textContent = v;
        capV.className = good ? 'g' : '';
        capB.nodeValue = b;
      }
      function say(s) { sr.textContent = s; }

      function openingCap() { setCap('', '', false); }

      function onGo() {
        if (!revealed) {
          if (!pickT) {
            setCap('Start with the thermometer.', ' Say what the line does over the next two minutes, then where the energy goes.', false);
            q1.classList.remove('hide'); picked.classList.add('hide');
            tBtns[0].focus();
            return;
          }
          if (!pickE) {
            setCap('One more to go.', ' Choose where that energy is going before you check.', false);
            eBtns[0].focus();
            return;
          }
          commit();
        } else {
          load(nextRound());
        }
      }

      function commit() {
        revealed = true;
        attempted++;
        var tr = truthOf(round);
        var fb = feedback(round, pickT, pickE);
        if (fb.ok) {
          streak++;
          if (streak >= 3) mastered = true;
        } else {
          streak = 0;
        }

        tBtns.forEach(function (b, i) {
          b.disabled = true;
          b.classList.remove('on');
          b.classList.toggle('true', TOPTS[i].k === tr.t);
          b.classList.toggle('miss', TOPTS[i].k === pickT && pickT !== tr.t);
        });
        eBtns.forEach(function (b, i) {
          b.disabled = true;
          b.classList.remove('on');
          b.classList.toggle('true', eKeys[i] === tr.e);
          b.classList.toggle('miss', eKeys[i] === pickE && pickE !== tr.e);
        });
        changeBtn.disabled = true;
        step2.className = 'step done';
        q1.classList.add('hide');
        picked.classList.remove('hide');
        q2.classList.remove('hide');

        if (fb.ok && streak === 3) {
          setCap('Three in a row — you have it.',
            ' During a change of state the energy still flows — into the potential store, not the kinetic one. The temperature holds flat: latent heat.', true);
        } else {
          setCap(fb.v, ' ' + fb.b, fb.ok);
        }

        speedTag.textContent = speedWord();
        legend.setAttribute('visibility', 'hidden');
        go.textContent = mastered ? 'Another anyway' : 'Next';
        updateStreak();
        say(fb.v + ' ' + fb.b);
        state();
        playReveal();
      }

      function updateStreak() {
        if (mastered) {
          streakEl.textContent = 'Three in a row.';
          streakEl.className = 'streak m';
          return;
        }
        streakEl.className = 'streak';
        if (streak === 0) streakEl.textContent = revealed ? 'Back to zero — you need three.' : '';
        else if (streak === 1) streakEl.textContent = '1 in a row — two more.';
        else streakEl.textContent = '2 in a row — one more.';
      }

      function playReveal() {
        if (raf) { cancelAnimationFrame(raf); raf = 0; }
        if (reduced) {
          animT = 1; drawLines(); drawParticles(1, 0);
          return;
        }
        var t0 = 0;
        function step(ts) {
          if (!t0) t0 = ts;
          var e = Math.min(1, (ts - t0) / 1100);
          animT = e < 1 ? 1 - Math.pow(1 - e, 3) : 1;
          drawLines();
          drawParticles(animT, ts);
          if (e < 1) { raf = requestAnimationFrame(step); }
          else { raf = 0; drawParticles(1, 0); }
        }
        raf = requestAnimationFrame(step);
      }

      function load(r) {
        if (raf) { cancelAnimationFrame(raf); raf = 0; }
        round = r; pickT = null; pickE = null; revealed = false; animT = 0;

        sampleEl.textContent = r.sub + ' at ' + r.ctx;
        askEl.textContent = (r.dir === 'heat'
          ? 'A heater puts ' + fmt(r.pow) + ' J into it every second for two minutes. Predict what the thermometer does — and where that energy goes.'
          : 'It gives out about ' + fmt(r.pow) + ' J every second for two minutes. Predict what the thermometer does — and where it comes from.');

        q1.classList.remove('hide');
        picked.classList.add('hide');
        q2.classList.add('hide');
        changeBtn.disabled = false;
        tBtns.forEach(function (b) { b.disabled = false; b.classList.remove('on', 'true', 'miss'); b.setAttribute('aria-pressed', 'false'); });
        eBtns.forEach(function (b) { b.disabled = false; b.classList.remove('on', 'true', 'miss'); b.setAttribute('aria-pressed', 'false'); });

        var heat = r.dir === 'heat';
        q2labText.nodeValue = heat ? 'Where does that energy go?' : 'Where does that energy come from?';
        eBtns[0].textContent = heat ? 'Kinetic store — particles speed up' : 'Kinetic store — particles slow down';
        eBtns[1].textContent = heat ? 'Potential store — pulling particles apart' : 'Potential store — forces re-forming';
        eBtns[2].textContent = heat ? 'Nowhere — the heater has stopped' : 'Nowhere — it has stopped losing energy';

        step1.className = 'step now';
        step2.className = 'step';
        go.textContent = 'Check';
        speedTag.textContent = '';
        legend.setAttribute('visibility', 'visible');
        openingCap();
        updateStreak();

        measure(); drawFrame(); drawLines(); drawParticles(0, 0);
        state();
        say(r.sub + ' at ' + r.ctx + '. Predict what the thermometer does next.');
      }

      root.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !revealed && (pickT || pickE)) {
          pickT = null; pickE = null;
          tBtns.forEach(function (b) { b.classList.remove('on'); b.setAttribute('aria-pressed', 'false'); });
          eBtns.forEach(function (b) { b.classList.remove('on'); b.setAttribute('aria-pressed', 'false'); });
          q1.classList.remove('hide'); picked.classList.add('hide'); q2.classList.add('hide');
          step1.className = 'step now'; step2.className = 'step';
          drawLines();
          openingCap();
          say('Prediction cleared.');
          tBtns[0].focus();
          e.stopPropagation();
        }
      });

      function relayout() {
        if (!round) return;
        measure(); drawFrame(); drawLines(); drawParticles(revealed ? 1 : 0, 0);
      }
      if (typeof ResizeObserver === 'function') {
        var ro = new ResizeObserver(function () {
          if (Math.round(plotWrap.clientWidth) === W && root.classList.contains('is-wide') === (root.clientWidth >= 640)) return;
          relayout();
        });
        ro.observe(root);
      } else {
        window.addEventListener('resize', relayout);
      }

      deck = shuffle(ROUNDS.slice());
      load(nextRound());
      relayout();
    }
  };
})();
