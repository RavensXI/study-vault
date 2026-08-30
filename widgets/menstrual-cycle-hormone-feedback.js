/* ============================================================
   menstrual-cycle-hormone-feedback

   The idea: the cycle is four OVERLAPPING hormone curves driving each
   other by feedback, not four events in a list. Part one walks the
   cycle on a live graph, drawing each causal link as it fires. Part two
   commits to cause-and-effect questions on the same graph.

   Every curve is sampled from a model (asymmetric gaussians), so the
   shape a student reasons about and the shape the questions describe
   cannot drift apart.
   ============================================================ */
(function () {
  'use strict';

  var SVGNS = 'http://www.w3.org/2000/svg';
  var D0 = 1, D1 = 28;              /* day domain */
  var YMAX = 1.06;                  /* relative level ceiling */

  var COL = { fsh: '#2d2a26', oes: '#b06a2c', lh: '#4f7d63', prg: '#5b6b91' };
  var NAME = { fsh: 'FSH', oes: 'Oestrogen', lh: 'LH', prg: 'Progesterone' };
  var ORDER = ['fsh', 'oes', 'lh', 'prg'];

  /* ---------- the model ---------------------------------- */

  function ag(d, mu, sl, sr) {          /* asymmetric gaussian */
    var s = d < mu ? sl : sr, z = (d - mu) / s;
    return Math.exp(-0.5 * z * z);
  }
  var MODEL = {
    /* FSH: pituitary. Rises while progesterone is low, pushed down by
       oestrogen, rising again at the very end as progesterone falls. */
    fsh: function (d) { return 0.12 + 0.46 * ag(d, 4.5, 2.6, 3.0) + 0.46 * ag(d, 32.5, 2.6, 3.0); },
    /* Oestrogen: follicle, then a smaller corpus-luteum rise. */
    oes: function (d) { return 0.08 + 0.86 * ag(d, 12.3, 3.6, 1.7) + 0.34 * ag(d, 20.5, 3.4, 3.0); },
    /* LH: flat, then the mid-cycle surge. */
    lh: function (d) { return 0.10 + 0.90 * ag(d, 13.2, 1.05, 1.15) + 0.05 * ag(d, 20.5, 3.4, 3.0); },
    /* Progesterone: corpus luteum only. Second term is the previous
       cycle's tail, so day 1 and day 28 join up. */
    prg: function (d) { return 0.06 + 0.88 * ag(d, 21.5, 3.4, 2.4) + 0.88 * ag(d, -6.5, 3.4, 2.4); }
  };

  /* Uterus lining thickness, 0-1, smoothed between keyframes. */
  var LK = [[1, 0.34], [5, 0.06], [9, 0.34], [14, 0.72], [19, 0.94], [24, 0.99], [26, 0.84], [28, 0.44]];
  function lining(d) {
    if (d <= LK[0][0]) return LK[0][1];
    for (var i = 1; i < LK.length; i++) {
      if (d <= LK[i][0]) {
        var a = LK[i - 1], b = LK[i], t = (d - a[0]) / (b[0] - a[0]);
        t = 0.5 - 0.5 * Math.cos(Math.PI * t);
        return a[1] + (b[1] - a[1]) * t;
      }
    }
    return LK[LK.length - 1][1];
  }

  var BANDS = {                       /* lining phases, for the track */
    shed: [1, 5, 'sheds'],
    rebuild: [6, 13, 'rebuilds'],
    maintain: [15, 25, 'maintained']
  };

  /* ---------- the walk ------------------------------------ */

  var STEPS = [
    { day: 1, reveal: 3.2, hi: ['prg'], band: 'shed',
      tag: { h: 'prg', d: 1.6, label: 'progesterone has fallen' },
      text: 'Day 1: the lining breaks down and bleeding starts. It breaks down because progesterone, which was holding it, has fallen away — the last event of the cycle before.' },
    { day: 4, reveal: 6.2, hi: ['fsh'], band: 'shed',
      tag: { h: 'fsh', d: 4.5, label: 'matures a follicle' },
      text: 'Progesterone is low, so the pituitary is free to release FSH. FSH travels in the blood to the ovary and makes one follicle, holding an egg, start to mature.' },
    { day: 8, reveal: 10, hi: ['oes'], band: 'rebuild',
      tag: { h: 'oes', d: 8, label: 'from the follicle' },
      text: 'The growing follicle releases oestrogen. Oestrogen rebuilds the lining that was just shed — repair starts long before the egg is ready.' },
    { day: 10, reveal: 11.2, hi: ['oes', 'fsh'], band: 'rebuild',
      link: { from: ['oes', 9.6], to: ['fsh', 9.6], kind: 'stop', label: 'inhibits FSH' },
      text: 'Oestrogen also acts back on the pituitary and inhibits FSH. Watch the curves cross: FSH is falling while oestrogen is still climbing. That is negative feedback.' },
    { day: 12.3, reveal: 13.6, hi: ['oes', 'lh'], band: 'rebuild',
      link: { from: ['oes', 11.4], to: ['lh', 13.2], kind: 'go', label: 'stimulates LH' },
      text: 'Around day 12 oestrogen peaks, and at that level its effect on the pituitary flips from inhibiting to stimulating: LH surges.' },
    { day: 14, reveal: 16, hi: ['lh'], band: 'rebuild', ovulation: true,
      tag: { h: 'lh', d: 14.2, label: 'ovulation' },
      text: 'Day 14. The LH surge makes the mature follicle burst and release its egg. Ovulation is caused by a hormone peak, not by the date.' },
    { day: 20, reveal: 24, hi: ['prg'], band: 'maintain', ovulation: true,
      link: { from: ['prg', 20], to: ['fsh', 20], kind: 'stop', label: 'inhibits FSH and LH' },
      text: 'The empty follicle becomes the corpus luteum and releases progesterone. It keeps the lining thick, and inhibits FSH and LH so no second follicle matures.' },
    { day: 27, reveal: 28, hi: ['prg'], band: null, ovulation: true, loop: 'and it starts again',
      tag: { h: 'prg', d: 26.4, label: 'progesterone falls' },
      text: 'No fertilisation, so the corpus luteum breaks down. Progesterone falls, nothing is holding the lining, and it sheds — which is day 1 of the next cycle.' }
  ];

  /* ---------- the question pool --------------------------- */

  var QS = [
    { id: 'q1', band: [9, 15], hi: [],
      stem: 'It is day 12. Which statement describes the hormone levels on that single day?',
      opts: ['Oestrogen high, LH starting to surge, FSH low but still present.',
             'Only oestrogen — each hormone acts alone in its own phase.',
             'Progesterone high, holding the lining ready for the egg.'],
      right: 0,
      fb: ['Right — oestrogen high, LH surging, FSH low. All four hormones are in the blood at once; what changes is how much. On day 12 three curves are doing three different things.',
           'Not quite — you said only oestrogen is present. All four are in the blood all month. On day 12 oestrogen is near its peak, LH is starting to surge, and FSH is low precisely because oestrogen has inhibited it.',
           'Not quite — you said progesterone is high on day 12. Progesterone only rises after ovulation, when the empty follicle becomes the corpus luteum. On day 12 the follicle is still intact and oestrogen is peaking.'] },

    { id: 'q2', band: [5, 13], hi: ['oes', 'fsh'],
      stem: 'Oestrogen is climbing steeply on day 10. What happens to FSH, and why?',
      opts: ['FSH falls — rising oestrogen inhibits FSH release from the pituitary.',
             'FSH rises — oestrogen makes the pituitary release more FSH.',
             'FSH is unchanged — oestrogen acts only on the uterus lining.'],
      right: 0,
      fb: ['Right — FSH falls because oestrogen inhibits it. Negative feedback: the follicle’s own oestrogen switches off the FSH that grew it, so usually only one follicle finishes maturing.',
           'Not quite — you said FSH rises. Oestrogen does stimulate the pituitary, but only at its peak and only for LH. Its effect on FSH is the opposite: the FSH curve falls while oestrogen is still climbing.',
           'Not quite — you said FSH is unchanged. Oestrogen has three jobs, not one: it thickens the lining, it inhibits FSH at the pituitary, and at its peak it triggers the LH surge. Look at days 6 to 13.'] },

    { id: 'q3', band: [10, 16], hi: ['lh'],
      stem: 'The LH surge happens at about day 13. What causes it?',
      opts: ['Oestrogen reaching its peak stimulates the pituitary.',
             'FSH falling frees the pituitary to make LH instead.',
             'Progesterone from the corpus luteum triggers it.'],
      right: 0,
      fb: ['Right — the oestrogen peak stimulates the pituitary. That is the flip: low oestrogen inhibits, peak oestrogen stimulates, so the follicle triggers its own release.',
           'Not quite — you said falling FSH causes the surge. FSH falls and LH surges at about the same time, but neither causes the other: high oestrogen does both, inhibiting FSH and stimulating LH.',
           'Not quite — you said progesterone triggers it. Progesterone comes afterwards: the corpus luteum only forms once the egg has gone. The LH surge is triggered by oestrogen reaching its peak.'] },

    { id: 'q4', band: [11, 17], hi: [],
      stem: 'An egg is released from the ovary at about day 14. What triggers that release?',
      opts: ['The surge of LH from the pituitary gland.',
             'The uterus lining reaching its full thickness.',
             'The rise in progesterone after day 14.'],
      right: 0,
      fb: ['Right — the LH surge. LH from the pituitary makes the mature follicle burst and release the egg. Note the order on the graph: the LH peak comes first, ovulation follows it.',
           'Not quite — you said the lining triggers it. The lining is an effect, not a cause: oestrogen thickens it over the same days, but nothing signals from the uterus to the ovary. The trigger is the LH surge.',
           'Not quite — you said the progesterone rise. Progesterone rises after ovulation, because the empty follicle becomes the corpus luteum. The trigger just before ovulation is the LH surge.'] },

    { id: 'q5', band: [15, 26], hi: [],
      stem: 'After ovulation the lining is kept thick. Which hormone does that, and where is it made?',
      opts: ['Progesterone, from the corpus luteum in the ovary.',
             'Progesterone, released by the pituitary gland.',
             'LH, released by the ovary once the egg has gone.'],
      right: 0,
      fb: ['Right — progesterone from the corpus luteum. The empty follicle does not just vanish: it becomes a gland in the ovary that holds the lining ready for an embryo.',
           'Not quite — you named progesterone but put it in the pituitary. The pituitary makes FSH and LH; the ovary makes oestrogen and progesterone. Progesterone comes from the corpus luteum, the follicle left behind.',
           'Not quite — you said LH from the ovary. LH is made in the pituitary and its surge is over by day 16. The lining is held by progesterone from the corpus luteum in the ovary.'] },

    { id: 'q6', band: [15, 26], hi: ['fsh', 'lh'],
      stem: 'Between days 15 and 26 both FSH and LH stay low. What is holding them down?',
      opts: ['Progesterone from the corpus luteum inhibits both.',
             'The pituitary has used up its FSH and LH earlier.',
             'It is not their turn — each hormone acts in its own phase.'],
      right: 0,
      fb: ['Right — progesterone inhibits both. That is why no new follicle matures while the lining is being held ready, and it is exactly how the combined contraceptive pill works.',
           'Not quite — you said the pituitary has run out. Glands are not stores that empty; the pituitary is being actively inhibited. High progesterone suppresses FSH and LH until progesterone itself falls.',
           'Not quite — you said it is not their turn. Nothing takes turns. Progesterone from the corpus luteum is actively inhibiting the pituitary, and FSH only rises again once progesterone has fallen.'] },

    { id: 'q7', band: [22, 28], hi: ['prg'],
      stem: 'The egg is not fertilised, the corpus luteum breaks down and progesterone falls. What happens next?',
      opts: ['The lining breaks down and bleeding starts — day 1.',
             'The lining keeps thickening, ready for next month.',
             'Nothing, until day 28, when the cycle runs out of days.'],
      right: 0,
      fb: ['Right — the lining breaks down and that is day 1. Progesterone was the only thing holding it. With progesterone low, FSH is no longer inhibited, so FSH rises and the next follicle starts to mature.',
           'Not quite — you said the lining keeps thickening. The lining is not self-supporting: progesterone maintains it. Once the corpus luteum breaks down, progesterone falls and the lining is shed.',
           'Not quite — you said nothing happens until the days run out. The calendar is not the cause, the hormone is. Day 1 is the day bleeding starts, and it starts because progesterone has fallen.'] },

    { id: 'q8', band: null, hi: ['oes', 'prg'],
      stem: 'A combined contraceptive pill keeps oestrogen and progesterone high every day. Why does that stop ovulation?',
      opts: ['They inhibit FSH and LH, so no follicle matures and no surge fires.',
             'They thicken the lining so much that the egg cannot get out.',
             'They stop the ovary from making any hormones at all.'],
      right: 0,
      fb: ['Right — FSH and LH are inhibited. Held high, oestrogen and progesterone keep the pituitary switched off, so no follicle matures and the LH surge that would release an egg never happens.',
           'Not quite — you said the thick lining traps the egg. The egg leaves the ovary, not the uterus, so lining thickness cannot block it. The pill acts higher up: it inhibits FSH and LH at the pituitary.',
           'Not quite — you said the ovary stops making hormones. The pill supplies oestrogen and progesterone rather than silencing the ovary. Because those stay high, FSH and LH are inhibited and no follicle matures.'] }
  ];

  var MASTERED_TEXT = 'Three in a row — you have it. Every event in the cycle is caused by a hormone changing level, and each hormone acts back on the gland that started it. Nothing waits its turn.';

  /* ---------- helpers ------------------------------------- */

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }
  function sv(tag, attrs) {
    var n = document.createElementNS(SVGNS, tag);
    if (attrs) for (var k in attrs) if (attrs.hasOwnProperty(k)) n.setAttribute(k, attrs[k]);
    return n;
  }
  function textWidth(node, fallbackChars, fontSize) {
    try {
      var w = node.getComputedTextLength();
      if (w > 0) return w;
    } catch (e) { /* fall through */ }
    return fallbackChars * fontSize * 0.55;
  }

  /* ---------- mount --------------------------------------- */

  function mount(root, ctx) {
    ctx = ctx || {};
    var reduced = !!ctx.reducedMotion;
    var uid = 'svmcf' + Math.floor(Math.random() * 1e9).toString(36);

    var accent = ctx.accent || '#8a6a4f';
    try {
      var own = getComputedStyle(root).getPropertyValue('--accent');
      if (own && own.trim()) accent = own.trim();
    } catch (e) { /* keep ctx.accent */ }

    /* ---- state ---- */
    var S = {
      phase: 'walk',
      step: 0,
      day: STEPS[0].day,
      completed: false,
      question: null,
      selected: null,
      slot: null,
      committed: false,
      correct: null,
      streak: 0,
      attempted: 0,
      mastered: false
    };
    var queue = [], qIndex = -1, cur = null, slots = [0, 1, 2];

    /* ---- shell ---- */
    root.className = (root.className ? root.className + ' ' : '') + 'svw-mcf';
    root.innerHTML = '';
    var style = document.createElement('style');
    style.textContent = css(accent, reduced);
    root.appendChild(style);

    var wrap = el('div', 'svw-mcf__wrap');
    root.appendChild(wrap);

    wrap.appendChild(el('p', 'svw-mcf__kicker', 'The menstrual cycle'));
    wrap.appendChild(el('h3', 'svw-mcf__title', 'Four hormones, one loop'));
    var frame = el('p', 'svw-mcf__frame',
      'Four hormones control the 28-day cycle: FSH, LH, oestrogen and progesterone. ' +
      'Step through one cycle and trace what each one causes.');
    wrap.appendChild(frame);

    var legend = el('div', 'svw-mcf__legend');
    var keyNodes = {};
    ORDER.forEach(function (h) {
      var k = el('span', 'svw-mcf__key');
      var i = el('i');
      i.style.background = COL[h];
      k.appendChild(i);
      k.appendChild(document.createTextNode(NAME[h]));
      legend.appendChild(k);
      keyNodes[h] = k;
    });
    wrap.appendChild(legend);

    var stage = el('div', 'svw-mcf__stage');
    wrap.appendChild(stage);

    /* question block is built once, on first entry to the quiz */
    var qBlock = null, stemNode = null, optNodes = [], echo = null, echoText = null;

    var bar = el('div', 'svw-mcf__bar');
    var btnBack = el('button', 'svw-mcf__btn', 'Back');
    btnBack.type = 'button';
    var btnGo = el('button', 'svw-mcf__btn svw-mcf__btn--go', 'See what happens next');
    btnGo.type = 'button';
    var meter = el('span', 'svw-mcf__meter', '');
    bar.appendChild(btnBack);
    bar.appendChild(btnGo);
    bar.appendChild(meter);
    wrap.appendChild(bar);

    var cap = el('p', 'svw-mcf__cap', '');
    wrap.appendChild(cap);

    var ruler = el('div', 'svw-mcf__cap svw-mcf__ruler', '');
    wrap.appendChild(ruler);

    var sr = el('p', 'svw-mcf__sr', '');
    sr.setAttribute('aria-live', 'polite');
    wrap.appendChild(sr);

    /* ---- svg skeleton, built once ---- */
    var G = {};
    var svgEl = sv('svg', { xmlns: SVGNS, 'aria-hidden': 'true', focusable: 'false' });
    stage.appendChild(svgEl);

    var defs = sv('defs');
    var clip = sv('clipPath', { id: uid + '-clip' });
    var clipRect = sv('rect', { x: 0, y: 0, width: 0, height: 0 });
    clip.appendChild(clipRect);
    defs.appendChild(clip);
    svgEl.appendChild(defs);

    G.qBand = sv('rect', { class: 'svw-mcf__qband' });
    svgEl.appendChild(G.qBand);
    G.bandHi = sv('rect', { class: 'svw-mcf__bandhi' });
    svgEl.appendChild(G.bandHi);

    var gGhost = sv('g', { class: 'svw-mcf__ghost' });
    G.ghostLining = sv('path', { class: 'svw-mcf__ghostfill' });
    gGhost.appendChild(G.ghostLining);
    G.ghosts = {};
    ORDER.forEach(function (h) {
      var p = sv('path', { fill: 'none', stroke: COL[h], 'stroke-width': 1.5 });
      gGhost.appendChild(p);
      G.ghosts[h] = p;
    });
    svgEl.appendChild(gGhost);

    var gClip = sv('g', { 'clip-path': 'url(#' + uid + '-clip)' });
    G.liningPath = sv('path', { class: 'svw-mcf__lining' });
    gClip.appendChild(G.liningPath);
    G.curves = {};
    ORDER.forEach(function (h) {
      var p = sv('path', { class: 'svw-mcf__curve', fill: 'none', stroke: COL[h],
        'stroke-width': 2.4, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' });
      gClip.appendChild(p);
      G.curves[h] = p;
    });
    svgEl.appendChild(gClip);

    G.axis = sv('path', { class: 'svw-mcf__axis' });
    svgEl.appendChild(G.axis);
    G.yLabel = sv('text', { class: 'svw-mcf__axlab' });
    G.yLabel.textContent = 'Hormone level (relative)';
    svgEl.appendChild(G.yLabel);

    G.ticks = [1, 7, 14, 21, 28].map(function (d) {
      var t = sv('text', { class: 'svw-mcf__tick' });
      t.textContent = String(d);
      svgEl.appendChild(t);
      return { day: d, node: t };
    });

    G.ovMark = sv('path', { class: 'svw-mcf__ovmark' });
    svgEl.appendChild(G.ovMark);

    G.marker = sv('path', { class: 'svw-mcf__marker' });
    svgEl.appendChild(G.marker);
    G.chip = sv('rect', { class: 'svw-mcf__chip', rx: 5 });
    svgEl.appendChild(G.chip);
    G.chipText = sv('text', { class: 'svw-mcf__chiptext' });
    svgEl.appendChild(G.chipText);

    G.trackLabel = sv('text', { class: 'svw-mcf__tracklab' });
    G.trackLabel.textContent = 'Uterus lining';
    svgEl.appendChild(G.trackLabel);
    G.bandFrame = sv('rect', { class: 'svw-mcf__bandframe', rx: 4 });
    svgEl.appendChild(G.bandFrame);
    G.bandLabels = {};
    Object.keys(BANDS).forEach(function (k) {
      var t = sv('text', { class: 'svw-mcf__bandlab' });
      t.textContent = BANDS[k][2];
      svgEl.appendChild(t);
      G.bandLabels[k] = t;
    });

    G.loop = sv('path', { class: 'svw-mcf__loop' });
    svgEl.appendChild(G.loop);
    G.loopHead = sv('path', { class: 'svw-mcf__loophead' });
    svgEl.appendChild(G.loopHead);
    G.loopText = sv('text', { class: 'svw-mcf__looplab' });
    svgEl.appendChild(G.loopText);
    G.ovText = sv('text', { class: 'svw-mcf__looplab' });
    G.ovText.textContent = 'ovulation';
    svgEl.appendChild(G.ovText);

    G.ann = sv('g', { class: 'svw-mcf__ann' });
    G.annLine = sv('path', { fill: 'none' });
    G.annCap = sv('path', {});
    G.annDot = sv('circle', { r: 2.6 });
    G.annText = sv('text', {});
    G.ann.appendChild(G.annLine);
    G.ann.appendChild(G.annCap);
    G.ann.appendChild(G.annDot);
    G.ann.appendChild(G.annText);
    svgEl.appendChild(G.ann);

    /* ---- geometry ---- */
    var geo = { w: 320, h: 208, padL: 8, padR: 8, top: 8, bot: 128, arc: true };
    var revealDay = STEPS[0].reveal, revealTarget = revealDay, raf = 0;

    function X(d) { return geo.padL + (d - D0) / (D1 - D0) * (geo.w - geo.padL - geo.padR); }
    function Y(v) { return geo.top + (1 - v / YMAX) * (geo.bot - geo.top); }

    function pathFor(fn) {
      var s = '', d;
      for (d = D0; d <= D1 + 0.001; d += 0.25) {
        s += (s ? 'L' : 'M') + X(d).toFixed(1) + ' ' + Y(fn(d)).toFixed(1);
      }
      return s;
    }
    function liningPathStr() {
      var top = geo.bandTop, h = geo.bandH, s = '', d;
      for (d = D0; d <= D1 + 0.001; d += 0.25) {
        s += (s ? 'L' : 'M') + X(d).toFixed(1) + ' ' + (top + h - lining(d) * h).toFixed(1);
      }
      return s + 'L' + X(D1).toFixed(1) + ' ' + (top + h) + 'L' + X(D0).toFixed(1) + ' ' + (top + h) + 'Z';
    }

    function layout() {
      var w = stage.clientWidth - 10;          /* stage padding */
      if (!(w > 60)) w = 300;
      geo.w = Math.round(w);
      geo.arc = (S.phase === 'walk');
      geo.bandTop = 166;
      geo.bandH = 17;
      geo.h = geo.arc ? 216 : 188;

      svgEl.setAttribute('viewBox', '0 0 ' + geo.w + ' ' + geo.h);
      svgEl.setAttribute('height', geo.h);
      svgEl.style.height = geo.h + 'px';

      clipRect.setAttribute('y', 0);
      clipRect.setAttribute('height', geo.h);
      clipRect.setAttribute('x', geo.padL - 3);

      ORDER.forEach(function (h) {
        var d = pathFor(MODEL[h]);
        G.curves[h].setAttribute('d', d);
        G.ghosts[h].setAttribute('d', d);
      });
      var lp = liningPathStr();
      G.liningPath.setAttribute('d', lp);
      G.ghostLining.setAttribute('d', lp);
      G.axis.setAttribute('d', 'M' + X(D0) + ' ' + geo.bot + 'H' + X(D1));
      G.yLabel.setAttribute('x', X(D0) + 2);
      G.yLabel.setAttribute('y', geo.top + 10);

      G.trackLabel.setAttribute('x', X(D0));
      G.trackLabel.setAttribute('y', geo.bandTop - 4);
      G.bandFrame.setAttribute('x', X(D0));
      G.bandFrame.setAttribute('y', geo.bandTop);
      G.bandFrame.setAttribute('width', X(D1) - X(D0));
      G.bandFrame.setAttribute('height', geo.bandH);
      Object.keys(BANDS).forEach(function (k) {
        var b = BANDS[k], t = G.bandLabels[k];
        t.setAttribute('x', (X(b[0]) + X(b[1])) / 2);
        t.setAttribute('y', geo.bandTop + geo.bandH - 5);
        var fits = (X(b[1]) - X(b[0])) > textWidth(t, b[2].length, 11) + 6;
        t.style.display = fits ? '' : 'none';
      });

      var ly = geo.h - 18, lb = geo.h - 4;
      G.loop.setAttribute('d', 'M' + X(D1) + ' ' + (geo.bandTop + geo.bandH + 3) +
        'V' + ly + 'H' + X(D0) + 'V' + (geo.bandTop + geo.bandH + 3));
      G.loopHead.setAttribute('d', 'M' + (X(D0) - 3.5) + ' ' + (geo.bandTop + geo.bandH + 7) +
        'L' + X(D0) + ' ' + (geo.bandTop + geo.bandH + 2) + 'L' + (X(D0) + 3.5) + ' ' + (geo.bandTop + geo.bandH + 7) + 'Z');
      G.loopText.setAttribute('x', X(D0));
      G.loopText.setAttribute('y', lb);
      G.loopText.setAttribute('text-anchor', 'start');
      G.ovText.setAttribute('x', X(14));
      G.ovText.setAttribute('y', geo.bandTop - 4);
      G.ovText.setAttribute('text-anchor', 'middle');

      G.ovMark.setAttribute('d', 'M' + X(14) + ' ' + (geo.bot - 4) + 'v8');
      sizeCaption();
      paint();
    }

    /* Reserve exactly the tallest step text, so the caption never jumps and
       never leaves a hole either. */
    function sizeCaption() {
      var w = cap.clientWidth;
      if (!(w > 40)) return;
      ruler.style.width = w + 'px';
      var tallest = 0;
      for (var i = 0; i < STEPS.length; i++) {
        ruler.textContent = STEPS[i].text;
        if (ruler.offsetHeight > tallest) tallest = ruler.offsetHeight;
      }
      ruler.textContent = '';
      cap.style.minHeight = tallest + 'px';
    }

    /* ---- painting ---- */
    function paint() {
      var st = (S.phase === 'walk') ? STEPS[S.step] : null;
      var hi = st ? st.hi : (cur ? cur.hi : []);
      var dim = hi && hi.length;

      var faint = (S.phase === 'walk') ? 0.25 : 0.4;   /* ghosts sit under the walk */
      ORDER.forEach(function (h) {
        var on = !dim || hi.indexOf(h) >= 0;
        G.curves[h].style.opacity = on ? 1 : faint;
        G.curves[h].setAttribute('stroke-width', (dim && on) ? 3.2 : 2.4);
        keyNodes[h].className = 'svw-mcf__key' + (dim && !on ? ' svw-mcf__key--off' : '');
      });

      gGhost.style.display = (S.phase === 'walk') ? '' : 'none';

      /* reveal window */
      var xr = X(S.phase === 'walk' ? revealDay : D1) + 3;
      clipRect.setAttribute('width', Math.max(0, xr - (geo.padL - 3)));

      /* lining phase highlight */
      var b = st && st.band ? BANDS[st.band] : null;
      if (b) {
        G.bandHi.style.display = '';
        G.bandHi.setAttribute('x', X(b[0]));
        G.bandHi.setAttribute('y', geo.bandTop);
        G.bandHi.setAttribute('width', X(b[1]) - X(b[0]));
        G.bandHi.setAttribute('height', geo.bandH);
      } else {
        G.bandHi.style.display = 'none';
      }
      Object.keys(BANDS).forEach(function (k) {
        G.bandLabels[k].style.fontWeight = (st && st.band === k) ? 700 : 400;
        G.bandLabels[k].style.opacity = (st && st.band === k) ? 1 : 0.55;
      });

      /* question day band */
      var qb = (S.phase === 'quiz' && cur && cur.band) ? cur.band : null;
      if (qb) {
        G.qBand.style.display = '';
        G.qBand.setAttribute('x', X(qb[0]));
        G.qBand.setAttribute('y', geo.top);
        G.qBand.setAttribute('width', X(qb[1]) - X(qb[0]));
        G.qBand.setAttribute('height', geo.bot - geo.top);
      } else {
        G.qBand.style.display = 'none';
      }

      /* day marker + chip: walk only */
      if (S.phase === 'walk') {
        var mx = X(S.day);
        G.marker.style.display = '';
        G.marker.setAttribute('d', 'M' + mx.toFixed(1) + ' ' + geo.top + 'V' + geo.bot);
        var label = 'Day ' + Math.round(S.day);
        G.chipText.textContent = label;
        var cw = Math.max(34, textWidth(G.chipText, label.length, 11) + 12);
        var cx = Math.min(Math.max(mx - cw / 2, X(D0) - 2), X(D1) + 2 - cw);
        G.chip.style.display = '';
        G.chip.setAttribute('x', cx);
        G.chip.setAttribute('y', geo.bot + 3);
        G.chip.setAttribute('width', cw);
        G.chip.setAttribute('height', 15);
        G.chipText.setAttribute('x', cx + cw / 2);
        G.chipText.setAttribute('y', geo.bot + 14);
        G.chipText.setAttribute('text-anchor', 'middle');
        G.chipText.style.display = '';
        G.ticks.forEach(function (t) {
          var tx = X(t.day);
          t.node.style.display = (tx > cx - 9 && tx < cx + cw + 9) ? 'none' : '';
          t.node.setAttribute('x', tx);
          t.node.setAttribute('y', geo.bot + 14);
          t.node.setAttribute('text-anchor', t.day === 1 ? 'start' : (t.day === 28 ? 'end' : 'middle'));
        });
      } else {
        G.marker.style.display = 'none';
        G.chip.style.display = 'none';
        G.chipText.style.display = 'none';
        G.ticks.forEach(function (t) {
          t.node.style.display = '';
          t.node.setAttribute('x', X(t.day));
          t.node.setAttribute('y', geo.bot + 14);
          t.node.setAttribute('text-anchor', t.day === 1 ? 'start' : (t.day === 28 ? 'end' : 'middle'));
        });
      }

      /* ovulation mark */
      var ovOn = (S.phase === 'quiz') || (st && st.ovulation);
      G.ovMark.style.display = ovOn ? '' : 'none';
      G.ovText.style.display = ovOn ? '' : 'none';

      /* loop back to day 1 */
      var loopOn = geo.arc;
      G.loop.style.display = loopOn ? '' : 'none';
      G.loopHead.style.display = loopOn ? '' : 'none';
      if (loopOn && st && st.loop) {
        G.loopText.textContent = st.loop;
        G.loopText.style.display = '';
        G.loop.classList.add('is-on');
        G.loopHead.classList.add('is-on');
      } else {
        G.loopText.style.display = 'none';
        G.loop.classList.remove('is-on');
        G.loopHead.classList.remove('is-on');
      }

      drawAnnotation(st);
    }

    /* The axis caption sits in the top-left. If a step's annotation lands on
       top of it (only happens on the narrowest phones), drop the caption for
       that step rather than printing two labels over each other. */
    function guardAxisLabel() {
      G.yLabel.style.display = '';
      if (G.annText.style.display === 'none' || G.ann.style.display === 'none') return;
      try {
        var a = G.yLabel.getBBox(), b = G.annText.getBBox();
        if (a.x < b.x + b.width && b.x < a.x + a.width &&
            a.y < b.y + b.height && b.y < a.y + a.height) G.yLabel.style.display = 'none';
      } catch (e) { /* no layout yet */ }
    }

    function drawAnnotation(st) {
      var a = st && (st.link || st.tag);
      if (!a || S.phase !== 'walk') { G.ann.style.display = 'none'; G.yLabel.style.display = ''; return; }
      G.ann.style.display = '';
      var right = X(D1), left = X(D0);

      if (st.link) {
        var x1 = X(st.link.from[1]), y1 = Y(MODEL[st.link.from[0]](st.link.from[1]));
        var x2 = X(st.link.to[1]), y2 = Y(MODEL[st.link.to[0]](st.link.to[1]));
        var dx = x2 - x1, dy = y2 - y1, len = Math.sqrt(dx * dx + dy * dy) || 1;
        var ux = dx / len, uy = dy / len;
        var sx = x1 + ux * 5, sy = y1 + uy * 5, ex = x2 - ux * 7, ey = y2 - uy * 7;
        G.annLine.setAttribute('d', 'M' + sx.toFixed(1) + ' ' + sy.toFixed(1) + 'L' + ex.toFixed(1) + ' ' + ey.toFixed(1));
        G.annLine.style.display = '';
        if (st.link.kind === 'stop') {
          G.annCap.setAttribute('d', 'M' + (ex - uy * 5).toFixed(1) + ' ' + (ey + ux * 5).toFixed(1) +
            'L' + (ex + uy * 5).toFixed(1) + ' ' + (ey - ux * 5).toFixed(1));
          G.annCap.setAttribute('fill', 'none');
          G.annCap.setAttribute('stroke-width', 2.2);
        } else {
          G.annCap.setAttribute('d', 'M' + (ex + ux * 7).toFixed(1) + ' ' + (ey + uy * 7).toFixed(1) +
            'L' + (ex - uy * 4).toFixed(1) + ' ' + (ey + ux * 4).toFixed(1) +
            'L' + (ex + uy * 4).toFixed(1) + ' ' + (ey - ux * 4).toFixed(1) + 'Z');
          G.annCap.setAttribute('fill', '#2d2a26');
          G.annCap.setAttribute('stroke-width', 0);
        }
        G.annCap.style.display = '';
        G.annDot.style.display = 'none';
        placeText(G.annText, st.link.label, ex, (sy + ey) / 2, left, right);
        guardAxisLabel();
      } else {
        var tx = X(st.tag.d), ty = Y(MODEL[st.tag.h](st.tag.d));
        G.annLine.style.display = 'none';
        G.annCap.style.display = 'none';
        G.annDot.style.display = '';
        G.annDot.setAttribute('cx', tx.toFixed(1));
        G.annDot.setAttribute('cy', ty.toFixed(1));
        placeText(G.annText, st.tag.label, tx, ty - 11, left, right);
        guardAxisLabel();
      }
    }

    function placeText(node, label, x, y, left, right) {
      node.textContent = label;
      var w = textWidth(node, label.length, 11.5);
      var toRight = (x + 7 + w) <= right;
      node.setAttribute('text-anchor', toRight ? 'start' : 'end');
      node.setAttribute('x', (toRight ? x + 7 : Math.max(x - 7, left + w)).toFixed(1));
      node.setAttribute('y', Math.max(geo.top + 10, Math.min(y, geo.bot - 3)).toFixed(1));
      node.style.display = '';
    }

    /* ---- reveal tween ---- */
    function animateTo(target) {
      revealTarget = target;
      if (reduced) { revealDay = target; paint(); return; }
      if (raf) { cancelAnimationFrame(raf); raf = 0; }
      var from = revealDay, t0 = 0;
      function frame(ts) {
        if (!t0) t0 = ts;
        var k = Math.min(1, (ts - t0) / 420);
        revealDay = from + (target - from) * (1 - Math.pow(1 - k, 3));
        paint();
        if (k < 1) { raf = requestAnimationFrame(frame); } else { raf = 0; }
      }
      raf = requestAnimationFrame(frame);
    }

    /* ---- state out ---- */
    function publish() {
      root.dataset.svState = JSON.stringify({
        phase: S.phase,
        step: S.step + 1,
        steps: STEPS.length,
        day: Math.round(S.day),
        completed: S.completed,
        question: S.question,
        selected: S.selected,
        slot: S.slot,
        committed: S.committed,
        correct: S.correct,
        streak: S.streak,
        attempted: S.attempted,
        mastered: S.mastered
      });
    }

    /* ---- walk ---- */
    function showStep(i) {
      S.phase = 'walk';
      S.step = Math.max(0, Math.min(STEPS.length - 1, i));
      var st = STEPS[S.step];
      S.day = st.day;
      S.completed = S.completed || (S.step === STEPS.length - 1);
      cap.textContent = st.text;
      sr.textContent = st.text;
      btnBack.style.display = S.step > 0 ? '' : 'none';
      btnGo.textContent = (S.step === STEPS.length - 1) ? 'Go to the questions' : 'See what happens next';
      meter.textContent = 'Step ' + (S.step + 1) + ' of ' + STEPS.length;
      if (qBlock) qBlock.style.display = 'none';
      frame.style.display = '';
      cap.classList.remove('svw-mcf__cap--free');
      layout();
      animateTo(st.reveal);
      publish();
    }

    /* ---- quiz ---- */
    function buildQuiz() {
      qBlock = el('div', 'svw-mcf__q');
      stemNode = el('p', 'svw-mcf__stem', '');
      qBlock.appendChild(stemNode);
      var list = el('div', 'svw-mcf__opts');
      for (var i = 0; i < 3; i++) {
        (function (idx) {
          var b = el('button', 'svw-mcf__opt', '');
          b.type = 'button';
          b.setAttribute('aria-pressed', 'false');
          b.addEventListener('click', function () { choose(idx); });
          list.appendChild(b);
          optNodes.push(b);
        })(i);
      }
      qBlock.appendChild(list);
      echo = el('div', 'svw-mcf__echo');
      echo.appendChild(document.createTextNode('Your answer: '));
      echoText = el('b', null, '');
      echo.appendChild(echoText);
      echo.style.display = 'none';
      qBlock.appendChild(echo);
      wrap.insertBefore(qBlock, bar);
    }

    function shuffle(a) {
      for (var i = a.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
      }
      return a;
    }
    function refill() {
      queue = shuffle(QS.slice());
      qIndex = -1;
    }

    function nextQuestion() {
      if (!qBlock) buildQuiz();
      S.phase = 'quiz';
      S.completed = true;
      frame.style.display = 'none';
      qBlock.style.display = '';
      qIndex++;
      if (qIndex >= queue.length) { refill(); qIndex = 0; }
      cur = queue[qIndex];
      slots = shuffle([0, 1, 2]);      /* the right answer must not always sit first */
      S.question = cur.id;
      S.selected = null;
      S.slot = null;
      S.committed = false;
      S.correct = null;
      stemNode.textContent = cur.stem;
      optNodes.forEach(function (b, i) {
        b.textContent = cur.opts[slots[i]];
        b.setAttribute('aria-pressed', 'false');
        b.disabled = false;
        b.style.display = '';
      });
      echo.style.display = 'none';
      cap.textContent = '';
      cap.classList.add('svw-mcf__cap--free');
      btnBack.style.display = 'none';
      btnGo.textContent = 'Check';
      btnGo.disabled = true;
      updateMeter();
      layout();
      publish();
    }

    function choose(i) {
      if (S.phase !== 'quiz' || S.committed) return;
      S.slot = i;
      S.selected = slots[i];
      optNodes.forEach(function (b, k) { b.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
      btnGo.disabled = false;
      publish();
    }

    function commit() {
      if (S.phase !== 'quiz' || S.committed || S.selected == null) return;
      S.committed = true;
      S.attempted++;
      S.correct = (S.selected === cur.right);
      if (S.correct) {
        S.streak++;
        if (S.streak >= 3) S.mastered = true;
      } else {
        S.streak = 0;
        queue.push(cur);          /* wrong questions come back */
      }
      optNodes.forEach(function (b) { b.style.display = 'none'; b.disabled = true; });
      echoText.textContent = cur.opts[S.selected];
      echo.className = 'svw-mcf__echo' + (S.correct ? ' svw-mcf__echo--ok' : '');
      echo.style.display = '';
      var msg = cur.fb[S.selected];
      if (S.correct && S.mastered && S.streak === 3) msg = msg + ' ' + MASTERED_TEXT;
      cap.textContent = msg;
      sr.textContent = msg;
      btnGo.textContent = S.mastered ? 'Another anyway' : 'Next question';
      btnGo.disabled = false;
      btnBack.style.display = S.mastered ? '' : 'none';
      btnBack.textContent = 'Walk the cycle again';
      updateMeter();
      layout();
      publish();
    }

    function updateMeter() {
      if (S.mastered) meter.textContent = 'You have it.';
      else if (S.streak === 1) meter.textContent = '1 right in a row — two more.';
      else if (S.streak === 2) meter.textContent = '2 right in a row — one more and you have it.';
      else meter.textContent = 'Three in a row finishes it.';
    }

    /* ---- controls ---- */
    btnGo.addEventListener('click', function () {
      if (S.phase === 'walk') {
        if (S.step === STEPS.length - 1) { refill(); nextQuestion(); }
        else showStep(S.step + 1);
      } else {
        if (!S.committed) commit();
        else nextQuestion();
      }
    });
    btnBack.addEventListener('click', function () {
      if (S.phase === 'walk') {
        if (S.step > 0) { revealDay = STEPS[S.step - 1].reveal; showStep(S.step - 1); }
      } else if (S.mastered) {
        btnBack.textContent = 'Back';
        revealDay = STEPS[0].reveal;
        showStep(0);
      }
    });

    /* ---- go ---- */
    showStep(0);
    if (typeof ResizeObserver === 'function') {
      var ro = new ResizeObserver(function () { layout(); });
      ro.observe(stage);
    }
  }

  /* ---------- styles (every selector scoped) --------------- */

  function css(accent, reduced) {
    return [
      '.svw-mcf{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
      '.svw-mcf .svw-mcf__wrap{max-width:660px;margin:0 auto}',
      '.svw-mcf .svw-mcf__wrap *{box-sizing:border-box}',
      '.svw-mcf .svw-mcf__kicker{margin:0 0 .16rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + '}',
      '.svw-mcf .svw-mcf__title{margin:0 0 .34rem;font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;font-weight:600;line-height:1.2}',
      '.svw-mcf .svw-mcf__frame{margin:0 0 .5rem;font-size:.86rem;line-height:1.45;color:#5b564e}',
      '.svw-mcf .svw-mcf__legend{display:flex;flex-wrap:wrap;gap:.25rem .85rem;margin:0 0 .38rem}',
      '.svw-mcf .svw-mcf__key{display:inline-flex;align-items:center;gap:.32rem;font-size:.74rem;font-weight:600;color:#5b564e}',
      '.svw-mcf .svw-mcf__key--off{opacity:.4}',
      '.svw-mcf .svw-mcf__key i{display:block;width:14px;height:3px;border-radius:2px}',
      '.svw-mcf .svw-mcf__stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.3rem .3rem .15rem;margin:0 0 .5rem}',
      '.svw-mcf .svw-mcf__stage svg{display:block;width:100%}',
      '.svw-mcf .svw-mcf__axis{stroke:#d9d2c6;stroke-width:1;fill:none}',
      '.svw-mcf .svw-mcf__axlab{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:#8d8880}',
      '.svw-mcf .svw-mcf__tick{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:#8d8880;font-variant-numeric:tabular-nums}',
      '.svw-mcf .svw-mcf__lining{fill:#2d2a26;opacity:.16}',
      '.svw-mcf .svw-mcf__bandframe{fill:none;stroke:#e0d9cd;stroke-width:1}',
      '.svw-mcf .svw-mcf__bandhi{fill:' + accent + ';opacity:.16}',
      '.svw-mcf .svw-mcf__qband{fill:' + accent + ';opacity:.10}',
      '.svw-mcf .svw-mcf__bandlab{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:#5b564e;text-anchor:middle}',
      '.svw-mcf .svw-mcf__tracklab{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:#8d8880}',
      '.svw-mcf .svw-mcf__marker{stroke:' + accent + ';stroke-width:1;stroke-dasharray:2 3;fill:none}',
      '.svw-mcf .svw-mcf__chip{fill:' + accent + '}',
      '.svw-mcf .svw-mcf__chiptext{font-family:Inter,system-ui,sans-serif;font-size:11px;font-weight:700;fill:#fff;font-variant-numeric:tabular-nums}',
      '.svw-mcf .svw-mcf__ovmark{stroke:#2d2a26;stroke-width:1.4;fill:none}',
      '.svw-mcf .svw-mcf__loop{fill:none;stroke:#b3aa9c;stroke-width:1.2;stroke-dasharray:4 3}',
      '.svw-mcf .svw-mcf__loop.is-on{stroke:#2d2a26;stroke-width:1.6;stroke-dasharray:none}',
      '.svw-mcf .svw-mcf__loophead{fill:#b3aa9c}',
      '.svw-mcf .svw-mcf__loophead.is-on{fill:#2d2a26}',
      '.svw-mcf .svw-mcf__looplab{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:#5b564e}',
      '.svw-mcf .svw-mcf__ann text{font-family:Inter,system-ui,sans-serif;font-size:11.5px;font-weight:600;fill:#2d2a26;paint-order:stroke fill;stroke:#faf8f5;stroke-width:3.4;stroke-linejoin:round}',
      '.svw-mcf .svw-mcf__ann path{stroke:#2d2a26}',
      '.svw-mcf .svw-mcf__ann circle{fill:#2d2a26}',
      '.svw-mcf .svw-mcf__q{margin:0 0 .1rem}',
      '.svw-mcf .svw-mcf__stem{margin:0 0 .45rem;font-size:.86rem;line-height:1.45;font-weight:600}',
      '.svw-mcf .svw-mcf__opts{margin:0}',
      '.svw-mcf .svw-mcf__opt{display:block;width:100%;text-align:left;margin:0 0 .32rem;padding:.42rem .6rem;font-family:inherit;font-size:.82rem;line-height:1.38;font-weight:400;color:#2d2a26;background:#fff;border:1px solid #ddd7cd;border-radius:10px;cursor:pointer}',
      '.svw-mcf .svw-mcf__opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;font-weight:600}',
      '.svw-mcf .svw-mcf__echo{font-size:.8rem;line-height:1.4;color:#5b564e;margin:0 0 .1rem}',
      '.svw-mcf .svw-mcf__echo b{font-weight:600;color:#2d2a26}',
      '.svw-mcf .svw-mcf__echo--ok b{color:#4f7d63}',
      '.svw-mcf .svw-mcf__bar{display:flex;align-items:center;flex-wrap:wrap;gap:.45rem .6rem;margin:.15rem 0 0}',
      '.svw-mcf .svw-mcf__btn{font-family:inherit;font-size:.82rem;font-weight:600;line-height:1;padding:.5rem .95rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;cursor:pointer}',
      '.svw-mcf .svw-mcf__btn--go{background:#2d2a26;border-color:#2d2a26;color:#fff}',
      '.svw-mcf .svw-mcf__btn[disabled]{opacity:.45;cursor:default}',
      '.svw-mcf .svw-mcf__btn:focus-visible{outline:2px solid ' + accent + ';outline-offset:2px}',
      '.svw-mcf .svw-mcf__opt:focus-visible{outline:2px solid ' + accent + ';outline-offset:2px}',
      '.svw-mcf .svw-mcf__meter{margin-left:auto;font-size:.76rem;font-weight:600;color:#8d8880;font-variant-numeric:tabular-nums}',
      '.svw-mcf .svw-mcf__cap{margin:.5rem 0 0;font-size:.82rem;line-height:1.48;color:#2d2a26;min-height:96px}',
      '.svw-mcf .svw-mcf__cap--free{min-height:0 !important}',
      '.svw-mcf .svw-mcf__ghost{opacity:.17}',
      '.svw-mcf .svw-mcf__ghostfill{fill:#2d2a26;opacity:.5}',
      '.svw-mcf .svw-mcf__ruler{position:absolute;visibility:hidden;pointer-events:none;left:-9999px;top:0;min-height:0}',
      '.svw-mcf .svw-mcf__sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}'
    ].join('\n');
  }

  window.SVWidget = {
    meta: {
      id: 'menstrual-cycle-hormone-feedback',
      title: 'Four hormones, one loop',
      teaches: 'The menstrual cycle as overlapping hormone curves driving each other by feedback, not four separate stages in a list.'
    },
    mount: mount
  };
})();
