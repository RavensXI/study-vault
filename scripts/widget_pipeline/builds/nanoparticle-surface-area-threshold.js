/* =====================================================================
   Same substance, smaller pieces
   ---------------------------------------------------------------------
   Cut a solid up and you add no material - but every cut turns inside
   into surface. The widget makes the student PREDICT the total surface
   area (or the SA:V ratio, or which of two same-mass samples acts
   faster) before it shows anything, then derives every figure from the
   geometry: total surface = pieces x surface of one piece.

   All areas, volumes, counts and factors are computed here from the
   cube dimensions. Nothing is asserted.
   ===================================================================== */
(function () {
  'use strict';

  var SVGNS = 'http://www.w3.org/2000/svg';

  /* ---------------------------------------------------------------
     numbers
     --------------------------------------------------------------- */
  var SUPS = { '0': '⁰', '1': '¹', '2': '²', '3': '³',
    '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷',
    '8': '⁸', '9': '⁹', '-': '⁻' };
  var NNBSP = ' ';               /* narrow no-break space: 6 000 */

  function sup(n) {
    return String(n).split('').map(function (c) { return SUPS[c] || c; }).join('');
  }
  function sig(v) { return Number(Number(v).toPrecision(3)); }
  function group(v) {
    return String(v).replace(/\B(?=(\d{3})+(?!\d))/g, NNBSP);
  }
  /* below 10^8, spell it out; above, a clean power of ten */
  function num(v) {
    v = Number(v);
    if (v < 1e8) return group(v >= 100 ? Math.round(v) : sig(v));
    var e = Math.floor(Math.log10(v) + 1e-9);
    var m = sig(v / Math.pow(10, e));
    return (m === 1 ? '' : group(m) + ' × ') + '10' + sup(e);
  }
  /* an area given in mm2, shown in whichever unit keeps it readable */
  function area(mm2) {
    var v = Number(mm2);
    if (v >= 1e6) return num(sig(v / 1e6)) + ' m²';
    if (v >= 1e-2) return num(sig(v)) + ' mm²';
    if (v >= 1e-8) return num(sig(v * 1e6)) + ' µm²';
    return num(sig(v * 1e12)) + ' nm²';
  }
  function times(f) { return num(sig(f)) + ' ×'; }
  /* a closing application sentence, only when the round carries one */
  function tail(t) { return t ? ' ' + t : ''; }

  /* ---------------------------------------------------------------
     rounds - every figure derived from the cube dimensions
     --------------------------------------------------------------- */

  /* cut a block of side S (mm) into cubes, each edge divided n ways */
  function cutRound(c) {
    var S = c.S, n = c.n;
    var blockSA = 6 * S * S;                 /* mm2 */
    var blockV = S * S * S;                  /* mm3 */
    var pieces = Math.pow(n, 3);
    var pSide = S / n;
    var pSA = 6 * pSide * pSide;
    var total = blockSA * n;                 /* = pieces x pSA */
    var onFace = n * n;
    var pV = pSide * pSide * pSide;
    var savLine = ' SA : V goes from ' + num(sig(blockSA / blockV)) + ' : 1 to ' +
      num(sig(pSA / pV)) + ' : 1, measured in mm.';
    var r = {
      id: c.id,
      frame: c.frame,
      premise: c.premise,
      arrow: c.arrow,
      schematic: c.drawn < n ? 'drawn ' + c.drawn + ' × ' + c.drawn +
        ', not ' + num(n) + ' × ' + num(n) : '',
      gridL: 1, gridR: c.drawn,
      leftTitle: 'Before', rightTitle: 'After the cut',
      leftLines: ['one cube, ' + c.sideText, 'surface ' + area(blockSA)],
      rightLines: [num(pieces) + ' cubes, ' + c.pieceText, 'each ' + area(pSA)],
      askLabel: 'total surface',
      answerText: area(total),
      options: [
        { label: area(blockSA) + ' — unchanged', note: '' },
        { label: area(total), note: '' },
        { label: area(blockSA * onFace), note: '' },
        { label: area(blockSA * pieces), note: '' }
      ],
      correct: 1,
      state: { cut: n, pieces: pieces, totalMm2: sig(total) }
    };
    r.fb = [
      'Not quite — you said ' + area(blockSA) + ', unchanged. Cutting adds no ' +
      c.mat + ', but every cut opens two fresh faces: ' + num(pieces) + ' cubes × ' +
      area(pSA) + ' = ' + area(total) + ' from the same ' + num(blockV) + ' mm³.',

      'Right — ' + area(total) + '. ' + num(pieces) + ' cubes, each ' + area(pSA) +
      ', from the same ' + num(blockV) + ' mm³ of ' + c.mat + '. Divide every edge by ' +
      num(n) + ' and the surface rises ' + times(n) + '.' +
      (c.appl ? tail(c.appl) : savLine),

      'Not quite — you said ' + area(blockSA * onFace) + '. That is ' + area(blockSA) +
      ' × ' + num(onFace) + ', the cubes on one face. What counts is ' + num(pieces) +
      ' cubes at ' + area(pSA) + ' each: ' + area(total) + '.',

      'Not quite — you said ' + area(blockSA * pieces) + '. That hands every one of the ' +
      num(pieces) + ' cubes the whole block’s ' + area(blockSA) + '. Each carries only ' +
      area(pSA) + ': ' + area(total) + '.'
    ];
    return r;
  }

  /* the same cut, but the question is the FACTOR the surface grows by */
  function factorRound(c) {
    var S = c.S, n = c.n;
    var blockSA = 6 * S * S;
    var pieces = Math.pow(n, 3);
    var pSide = S / n;
    var pSA = 6 * pSide * pSide;
    var total = blockSA * n;
    var shrink = n * n;                      /* how much smaller one face is */
    var r = {
      id: c.id,
      frame: c.frame,
      premise: c.premise,
      arrow: c.arrow,
      schematic: 'drawn ' + c.drawn + ' × ' + c.drawn + ', not ' + num(n) +
        ' × ' + num(n),
      gridL: 1, gridR: c.drawn,
      leftTitle: 'Before', rightTitle: 'After the cut',
      leftLines: ['one cube, ' + c.sideText, 'surface ' + area(blockSA)],
      rightLines: [num(pieces) + ' cubes, ' + c.pieceText, 'each ' + area(pSA)],
      askLabel: 'total surface',
      answerText: area(total),
      options: [
        { label: 'No change — ' + times(1), note: '' },
        { label: times(n), note: '' },
        { label: times(shrink), note: '' },
        { label: times(pieces), note: '' }
      ],
      correct: 1,
      state: { cut: n, pieces: pieces, factor: n }
    };
    r.fb = [
      'Not quite — you said no change. No ' + c.mat + ' is added, yet ' + num(pieces) +
      ' cubes of ' + area(pSA) + ' each come to ' + area(total) + ', against ' +
      area(blockSA) + ' before. The cuts turn inside into surface.',

      'Right — ' + times(n) + '. ' + area(blockSA) + ' becomes ' + area(total) +
      ', more than two tennis courts, from one cube ' + c.sideText +
      ' across.' + tail(c.appl),

      'Not quite — you said ' + times(shrink) + '. That is how much smaller each cube’s ' +
      'surface is (' + area(pSA) + ' against ' + area(blockSA) + '). There are ' +
      num(pieces) + ' of them: ' + num(pieces) + ' ÷ ' + num(shrink) + ' = ' + times(n) + '.',

      'Not quite — you said ' + times(pieces) + '. That is the number of cubes, not the ' +
      'surface factor. Each has ' + num(shrink) + ' times less surface: ' + num(pieces) +
      ' ÷ ' + num(shrink) + ' = ' + times(n) + '.'
    ];
    return r;
  }

  /* one cube of side S cut in half each way: what happens to SA : V? */
  function ratioRound(c) {
    var S = c.S, s = S / 2;
    var bigSA = 6 * S * S, bigV = S * S * S;
    var smSA = 6 * s * s, smV = s * s * s;
    var rBig = bigSA / bigV, rSm = smSA / smV;
    var aFac = (S / s) * (S / s), vFac = (S / s) * (S / s) * (S / s);
    function rat(v) { return num(sig(v)) + ' : 1'; }
    var r = {
      id: c.id,
      frame: c.frame,
      premise: c.premise,
      arrow: c.arrow,
      schematic: '',
      gridL: 1, gridR: 2, highlight: true,
      leftTitle: 'The whole cube', rightTitle: 'One small cube',
      leftLines: [num(S) + ' mm across', area(bigSA) + ', ' + num(bigV) + ' mm³',
        'SA : V = ' + rat(rBig)],
      rightLines: [num(s) + ' mm across', area(smSA) + ', ' + num(smV) + ' mm³'],
      askLabel: 'SA : V',
      answerText: rat(rSm),
      options: [
        { label: rat(rBig) + ' — unchanged', note: '' },
        { label: rat(rSm), note: '' },
        { label: rat(rBig * aFac), note: '' },
        { label: rat(rBig * vFac), note: '' }
      ],
      correct: 1,
      state: { ratioBefore: sig(rBig), ratioAfter: sig(rSm) }
    };
    r.fb = [
      'Not quite — you said ' + rat(rBig) + ', unchanged. Both fell, but not equally: ' +
      'surface to a quarter, volume to an eighth. ' + area(smSA) + ' ÷ ' + num(smV) +
      ' mm³ = ' + rat(rSm) + '.',

      'Right — ' + rat(rSm) + '. Surface fell to a quarter (' + area(bigSA) + ' → ' +
      area(smSA) + '), volume to an eighth (' + num(bigV) + ' → ' + num(smV) +
      ' mm³). A quarter against an eighth doubles the ratio.' + tail(c.appl),

      'Not quite — you said ' + rat(rBig * aFac) + '. ' + num(aFac) +
      ' is how far the surface fell, not the ratio. Divide the new surface by the new volume: ' +
      area(smSA) + ' ÷ ' + num(smV) + ' mm³ = ' + rat(rSm) + '.',

      'Not quite — you said ' + rat(rBig * vFac) + '. ' + num(vFac) +
      ' is how far the volume fell. The ratio is new surface over new volume: ' +
      area(smSA) + ' ÷ ' + num(smV) + ' mm³ = ' + rat(rSm) + ', double the old ' +
      rat(rBig) + '.'
    ];
    return r;
  }

  /* two samples, same mass, different piece size: which acts faster? */
  function compareRound(c) {
    var V = c.V;                              /* mm3 in each sample */
    var a = c.aSide, b = c.bSide;             /* piece sides in mm */
    var aN = V / (a * a * a), bN = V / (b * b * b);
    var aSA = 6 * a * a, bSA = 6 * b * b;
    var aTot = aN * aSA, bTot = bN * bSA;
    var factor = sig(a / b);                  /* = bTot / aTot */
    var shrink = sig((a / b) * (a / b));      /* one grain vs one particle */
    var split = sig(Math.pow(a / b, 3));      /* particles per grain */
    var r = {
      id: c.id,
      frame: c.frame,
      premise: c.premise,
      arrow: c.arrow,
      schematic: 'both drawn coarser than life',
      gridL: 2, gridR: c.drawn,
      leftTitle: 'A · ' + c.aText, rightTitle: 'B · ' + c.bText,
      leftLines: [num(aN) + ' grains, ' + c.aSize, 'total surface ' + area(aTot)],
      rightLines: [num(bN) + ' particles, ' + c.bSize, 'each ' + area(bSA)],
      askLabel: 'total surface',
      answerText: area(bTot),
      options: [
        { label: 'Both the same', note: 'same mass of ' + c.mat },
        { label: 'A is faster', note: 'its grains are bigger' },
        { label: 'B is faster', note: times(factor) + ' more surface' },
        { label: 'B is faster', note: times(split) + ' more surface' }
      ],
      correct: 2,
      state: { factor: factor, particles: sig(bN) }
    };
    r.fb = [
      'Not quite — you said both the same. The mass is the same; the exposed surface is not. ' +
      'B spreads it over ' + area(bTot) + ' against A’s ' + area(aTot) + ' — ' +
      times(factor) + ' more for the reaction to work on.',

      'Not quite — you said A. One grain does beat one particle, by ' + num(shrink) +
      ' times, but ' + num(split) + ' particles replace each grain: ' + num(split) + ' ÷ ' +
      num(shrink) + ' = ' + times(factor) + ' more surface for B.',

      'Right — B, with ' + times(factor) + ' the surface. One particle has ' +
      num(shrink) + ' times less surface than a grain, but ' + num(split) +
      ' replace it: ' + num(split) + ' ÷ ' + num(shrink) + ' = ' + times(factor) +
      '.' + tail(c.appl),

      'Not quite — you said ' + times(split) + '. That is how many particles replace one grain, ' +
      'not the surface factor. Each has ' + num(shrink) + ' times less surface: ' + num(split) +
      ' ÷ ' + num(shrink) + ' = ' + times(factor) + '.'
    ];
    return r;
  }

  function buildRounds() {
    return [
      cutRound({
        id: 'cut-mm', S: 10, n: 10, drawn: 10, mat: 'silver',
        sideText: '1 cm', pieceText: '1 mm',
        frame: 'A 1 cm cube of silver is cut into cubes 1 mm across, and none is lost. ' +
          'Predict the total surface area of the pieces.',
        premise: 'Nothing is added and nothing is lost — the same silver, in more pieces.',
        arrow: ['cut each edge', 'into 10'],
        appl: ''
      }),
      ratioRound({
        id: 'halve', S: 2, mat: 'zinc oxide',
        frame: 'A 2 mm cube of zinc oxide is cut into cubes 1 mm across. Predict the ' +
          'surface-area-to-volume ratio of one small cube.',
        premise: 'Halving the side cuts the surface and the volume — but by different amounts.',
        arrow: ['halve', 'every edge'],
        appl: 'Keep halving and the ratio keeps doubling.'
      }),
      cutRound({
        id: 'cut-um', S: 1, n: 1000, drawn: 10, mat: 'titanium dioxide',
        sideText: '1 mm', pieceText: '1 µm',
        frame: 'A 1 mm cube of titanium dioxide is ground into cubes 1 µm across ' +
          '(1 µm = 1000 nm). Predict the total surface area of the powder.',
        premise: 'The powder holds exactly the titanium dioxide the cube held.',
        arrow: ['cut each edge', 'into 1000'],
        appl: 'Milled this fine, it blocks UV in sunscreen without looking white.'
      }),
      compareRound({
        id: 'silver', V: 8, aSide: 1, bSide: 1e-5, drawn: 10, mat: 'silver',
        aText: '1 mm grains', bText: '10 nm particles',
        aSize: '1 mm', bSize: '10 nm',
        frame: 'Two dressings hold the same mass of silver: A as 1 mm grains, B as 10 nm ' +
          'particles. Silver ions come off the surface. Predict which acts faster.',
        premise: 'Same mass of silver in each dressing — 8 mm³.',
        arrow: ['same silver,', 'finer pieces'],
        appl: 'A wound dressing needs only a trace of silver.'
      }),
      factorRound({
        id: 'cut-nano', S: 10, n: 1e6, drawn: 10, mat: 'silver',
        sideText: '1 cm', pieceText: '10 nm',
        frame: 'A 1 cm cube of silver is cut into cubes 10 nm across — nanoparticle size. ' +
          'Predict how many times more surface the pieces have in total.',
        premise: 'Nanoparticles measure 1–100 nm, so 10 nm cubes are well inside the range.',
        arrow: ['cut each edge', 'into a million'],
        appl: 'At 10 nm about one atom in six sits on the surface; in the whole cube, ' +
          'fewer than one in a million.'
      }),
      compareRound({
        id: 'gold', V: 1, aSide: 1e-3, bSide: 5e-6, drawn: 10, mat: 'gold',
        aText: '1 µm grains', bText: '5 nm particles',
        aSize: '1 µm', bSize: '5 nm',
        frame: 'Two catalysts hold the same mass of gold: A as 1 µm grains, B as 5 nm ' +
          'particles. The reaction happens on the surface. Predict which works faster.',
        premise: 'Same mass of gold in each catalyst — 1 mm³.',
        arrow: ['same gold,', 'finer pieces'],
        appl: 'That is why catalysts are used as fine particles.'
      })
    ];
  }

  var MASTERY = 'Three in a row — you have it. Cutting adds no material; it turns inside ' +
    'into surface, so SA : V climbs as the pieces shrink. Below 100 nm so much of a substance ' +
    'is surface that it behaves unlike the bulk — which is also why the possible risks of ' +
    'engineered nanoparticles are still being researched.';

  /* ---------------------------------------------------------------
     style - every selector scoped to .svw-nano
     --------------------------------------------------------------- */
  var CSS = [
    '.svw-nano{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;max-width:720px;margin:0 auto}',
    '.svw-nano *{box-sizing:border-box}',
    '.svw-nano-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:@A}',
    '.svw-nano-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;font-weight:600;line-height:1.2;margin:.12rem 0 .3rem}',
    '.svw-nano-frame{font-size:.85rem;line-height:1.42;margin:0 0 .55rem;color:#3b3730}',
    '.svw-nano-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem .55rem .45rem}',
    '.svw-nano-svg{display:block;width:100%;max-width:460px;height:92px;margin:0 auto}',
    '.svw-nano-stats{display:grid;grid-template-columns:1fr 1fr;gap:.35rem .5rem;max-width:460px;margin:.25rem auto 0}',
    '.svw-nano-side{min-width:0}',
    '.svw-nano-st{font-size:.68rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#8d8880;margin-bottom:.1rem}',
    '.svw-nano-l{font-size:.75rem;line-height:1.36;color:#3b3730;font-variant-numeric:tabular-nums}',
    '.svw-nano-ask{font-weight:700;color:#2d2a26}',
    '.svw-nano-run{min-height:1rem;font-size:.72rem;line-height:1;color:#8d8880;margin:.45rem 0 .3rem}',
    '.svw-nano-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.4rem}',
    '.svw-nano-opt{display:block;width:100%;text-align:left;font-family:inherit;font-size:.82rem;font-weight:600;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.4rem .58rem;cursor:pointer;font-variant-numeric:tabular-nums}',
    '.svw-nano-opt b{font-weight:600}',
    '.svw-nano-opt i{display:block;font-style:normal;font-weight:500;font-size:.7rem;color:#8d8880;line-height:1.25}',
    '.svw-nano-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-nano-opt[aria-pressed="true"] i{color:#e8e2d9}',
    '.svw-nano-opt:disabled{cursor:default}',
    '.svw-nano-opt.is-key{border-color:#4f7d63;box-shadow:inset 0 0 0 1px #4f7d63}',
    '.svw-nano-act{display:flex;align-items:center;gap:.5rem;margin:.45rem 0 .4rem}',
    '.svw-nano-go{font-family:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.5rem .95rem;cursor:pointer}',
    '.svw-nano-go:disabled{opacity:.38;cursor:default}',
    '.svw-nano-cap{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem .65rem;font-size:.84rem;line-height:1.45;color:#3b3730;min-height:3.4rem}',
    '.svw-nano-cap b{color:#2d2a26}',
    '.svw-nano-cap b.ok{color:#4f7d63}',
    '.svw-nano-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}',
    '.svw-nano-hide{display:none}'
  ].join('\n');

  var CSS_MOTION = '.svw-nano-opt,.svw-nano-go{transition:background-color .12s ease,border-color .12s ease}';

  /* ---------------------------------------------------------------
     mount
     --------------------------------------------------------------- */
  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = (ctx.accent || '').trim();
    if (!accent) {
      try {
        accent = getComputedStyle(root).getPropertyValue('--accent').trim();
      } catch (e) { accent = ''; }
    }
    if (!/^#[0-9a-f]{6}$/i.test(accent)) accent = '#8a6a4f';
    var reduced = !!ctx.reducedMotion;

    root.classList.add('svw-nano');
    while (root.firstChild) root.removeChild(root.firstChild);

    var style = document.createElement('style');
    style.textContent = CSS.replace(/@A/g, accent) + (reduced ? '' : '\n' + CSS_MOTION);
    root.appendChild(style);

    function el(tag, cls, text) {
      var n = document.createElement(tag);
      if (cls) n.className = cls;
      if (text != null) n.textContent = text;
      return n;
    }

    /* --- header ------------------------------------------------- */
    root.appendChild(el('div', 'svw-nano-kick', 'Surface area : volume'));
    root.appendChild(el('div', 'svw-nano-title', 'Same substance, smaller pieces'));
    var frame = el('p', 'svw-nano-frame', '');
    root.appendChild(frame);

    /* --- stage -------------------------------------------------- */
    var stage = el('div', 'svw-nano-stage');
    var svg = document.createElementNS(SVGNS, 'svg');
    svg.setAttribute('viewBox', '0 0 320 82');
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svg.setAttribute('class', 'svw-nano-svg');
    svg.setAttribute('role', 'img');
    stage.appendChild(svg);

    var stats = el('div', 'svw-nano-stats');
    var sides = [];
    for (var si = 0; si < 2; si++) {
      var side = el('div', 'svw-nano-side');
      var st = el('div', 'svw-nano-st', '');
      side.appendChild(st);
      var lines = [];
      for (var li = 0; li < 3; li++) {
        var ln = el('div', 'svw-nano-l', '');
        side.appendChild(ln);
        lines.push(ln);
      }
      stats.appendChild(side);
      sides.push({ title: st, lines: lines });
    }
    stage.appendChild(stats);
    root.appendChild(stage);

    /* --- run counter -------------------------------------------- */
    var run = el('div', 'svw-nano-run', '');
    root.appendChild(run);

    /* --- options ------------------------------------------------ */
    var opts = el('div', 'svw-nano-opts');
    opts.setAttribute('role', 'group');
    opts.setAttribute('aria-label', 'Your prediction');
    var optBtns = [];
    for (var oi = 0; oi < 4; oi++) {
      var b = el('button', 'svw-nano-opt');
      b.type = 'button';
      b.setAttribute('aria-pressed', 'false');
      b.appendChild(el('b', null, ''));
      b.appendChild(el('i', null, ''));
      (function (idx, btn) {
        btn.addEventListener('click', function () { choose(idx); });
      })(oi, b);
      opts.appendChild(b);
      optBtns.push(b);
    }
    root.appendChild(opts);

    /* --- commit ------------------------------------------------- */
    var act = el('div', 'svw-nano-act');
    var go = el('button', 'svw-nano-go', 'Check');
    go.type = 'button';
    go.disabled = true;
    go.addEventListener('click', function () { primary(); });
    act.appendChild(go);
    root.appendChild(act);

    /* --- caption ------------------------------------------------ */
    var cap = el('div', 'svw-nano-cap');
    root.appendChild(cap);
    var sr = el('p', 'svw-nano-sr', '');
    sr.setAttribute('aria-live', 'polite');
    root.appendChild(sr);

    /* --- state -------------------------------------------------- */
    var pool = buildRounds();
    var queue = [];
    var round = null;
    var picked = -1;
    var revealed = false;
    var streak = 0, attempted = 0, mastered = false;

    function refill() {
      var rest = pool.slice(1);
      for (var i = rest.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var t = rest[i]; rest[i] = rest[j]; rest[j] = t;
      }
      queue = queue.concat(rest);
    }
    queue.push(pool[0]);
    refill();

    /* --- drawing ------------------------------------------------ */
    function cube(x, y, s, dz, divs, tint, markOne) {
      var g = document.createElementNS(SVGNS, 'g');
      var front = tint ? accent + '1f' : '#f1ece3';
      var top = tint ? accent + '12' : '#f8f5ef';
      var right = tint ? accent + '33' : '#e6dfd3';
      var edge = tint ? accent + '99' : '#c3baaa';
      var grid = tint ? accent + '5c' : '#c3baaa';

      function poly(pts, fill) {
        var p = document.createElementNS(SVGNS, 'polygon');
        p.setAttribute('points', pts);
        p.setAttribute('fill', fill);
        p.setAttribute('stroke', edge);
        p.setAttribute('stroke-width', '1');
        g.appendChild(p);
      }
      function line(x1, y1, x2, y2, w, col) {
        var l = document.createElementNS(SVGNS, 'line');
        l.setAttribute('x1', x1); l.setAttribute('y1', y1);
        l.setAttribute('x2', x2); l.setAttribute('y2', y2);
        l.setAttribute('stroke', col); l.setAttribute('stroke-width', w);
        g.appendChild(l);
      }
      var ty = y, fy = y + dz;
      poly((x) + ',' + fy + ' ' + (x + dz) + ',' + ty + ' ' + (x + dz + s) + ',' + ty +
        ' ' + (x + s) + ',' + fy, top);
      poly((x + s) + ',' + fy + ' ' + (x + dz + s) + ',' + ty + ' ' + (x + dz + s) + ',' +
        (ty + s) + ' ' + (x + s) + ',' + (fy + s), right);
      poly((x) + ',' + fy + ' ' + (x + s) + ',' + fy + ' ' + (x + s) + ',' + (fy + s) +
        ' ' + (x) + ',' + (fy + s), front);

      if (markOne) {
        var c = s / divs;
        var m = document.createElementNS(SVGNS, 'rect');
        m.setAttribute('x', x); m.setAttribute('y', fy);
        m.setAttribute('width', c); m.setAttribute('height', c);
        m.setAttribute('fill', accent + '7a');
        g.appendChild(m);
      }
      for (var i = 1; i < divs; i++) {
        var o = (s / divs) * i;
        line(x + o, fy, x + o, fy + s, .6, grid);
        line(x, fy + o, x + s, fy + o, .6, grid);
      }
      var depth = Math.min(divs, 4);
      for (var k = 1; k < depth; k++) {
        var d = (s / depth) * k;
        line(x + d, fy, x + d + dz, ty, .5, grid);          /* top face */
        line(x + s, fy + d, x + s + dz, ty + d, .5, grid);   /* right face */
      }
      return g;
    }

    function text(x, y, str, size, fill, anchor, weight) {
      var t = document.createElementNS(SVGNS, 'text');
      t.setAttribute('x', x); t.setAttribute('y', y);
      t.setAttribute('font-size', size);
      t.setAttribute('fill', fill);
      t.setAttribute('text-anchor', anchor || 'middle');
      t.setAttribute('font-family', 'Inter,system-ui,sans-serif');
      if (weight) t.setAttribute('font-weight', weight);
      t.textContent = str;
      return t;
    }

    function drawStage(r) {
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      var s = 58, dz = 14, y = 4;
      svg.appendChild(cube(14, y, s, dz, r.gridL, false, false));
      svg.appendChild(cube(218, y, s, dz, r.gridR, true, !!r.highlight));
      /* arrow */
      var mid = 160, ay = y + dz + s / 2;
      var ln = document.createElementNS(SVGNS, 'line');
      ln.setAttribute('x1', 100); ln.setAttribute('y1', ay);
      ln.setAttribute('x2', 208); ln.setAttribute('y2', ay);
      ln.setAttribute('stroke', '#c3baaa'); ln.setAttribute('stroke-width', '1');
      svg.appendChild(ln);
      var hd = document.createElementNS(SVGNS, 'polygon');
      hd.setAttribute('points', '214,' + ay + ' 205,' + (ay - 3.6) + ' 205,' + (ay + 3.6));
      hd.setAttribute('fill', '#c3baaa');
      svg.appendChild(hd);
      svg.appendChild(text(mid, ay - 16, r.arrow[0], 10, '#5b564e'));
      svg.appendChild(text(mid, ay - 5, r.arrow[1], 10, '#5b564e'));
      if (r.schematic) svg.appendChild(text(mid, ay + 17, r.schematic, 8.5, '#8d8880'));
      svg.setAttribute('aria-label', r.leftTitle + ': ' + r.leftLines.join(', ') +
        '. ' + r.rightTitle + ': ' + r.rightLines.join(', ') + '.');
    }

    /* --- rendering ---------------------------------------------- */
    function fillSide(side, title, lines, askLabel, askValue) {
      side.title.textContent = title;
      for (var i = 0; i < 3; i++) {
        var node = side.lines[i];
        while (node.firstChild) node.removeChild(node.firstChild);
        if (i < lines.length) {
          node.appendChild(document.createTextNode(lines[i]));
        } else if (askLabel && i === lines.length) {
          node.appendChild(document.createTextNode(askLabel + ' '));
          var strong = document.createElement('span');
          strong.className = 'svw-nano-ask';
          strong.textContent = askValue;
          node.appendChild(strong);
        }
      }
    }

    function render() {
      var r = round;
      frame.textContent = r.frame;
      drawStage(r);
      fillSide(sides[0], r.leftTitle, r.leftLines, '', '');
      fillSide(sides[1], r.rightTitle, r.rightLines, r.askLabel,
        revealed ? r.answerText : '?');
      for (var i = 0; i < 4; i++) {
        var o = r.options[i];
        optBtns[i].firstChild.textContent = o.label;
        optBtns[i].lastChild.textContent = o.note;
        optBtns[i].setAttribute('aria-pressed', picked === i ? 'true' : 'false');
        optBtns[i].disabled = revealed;
        optBtns[i].classList.toggle('is-key', revealed && i === r.correct);
      }
      go.disabled = !revealed && picked < 0;
      go.textContent = revealed ? (mastered ? 'Another anyway' : 'Next one') : 'Check';
      opts.classList.toggle('svw-nano-hide', revealed && mastered);
      run.textContent = runText();
      publish();
    }

    function runText() {
      if (!attempted) return '';
      if (mastered) return 'Three in a row — carry on if you want to.';
      if (streak === 0) return 'Back to none in a row.';
      if (streak === 1) return '1 right in a row.';
      return '2 right in a row — one more and you have it.';
    }

    function publish() {
      var d = {
        round: round.id,
        attempted: attempted,
        streak: streak,
        mastered: mastered,
        picked: picked,
        phase: revealed ? 'revealed' : (picked < 0 ? 'choosing' : 'ready')
      };
      if (revealed) {
        d.correct = picked === round.correct;
        d.answer = round.answerText;
      }
      for (var k in round.state) if (round.state.hasOwnProperty(k)) d[k] = round.state[k];
      root.dataset.svState = JSON.stringify(d);
    }

    function say(html, plain) {
      cap.innerHTML = '';
      cap.appendChild(html);
      sr.textContent = plain;
    }

    function caption(msg, right) {
      var frag = document.createDocumentFragment();
      var head = msg.slice(0, msg.indexOf('—') + 1);
      var b = document.createElement('b');
      if (right) b.className = 'ok';
      b.textContent = head;
      frag.appendChild(b);
      frag.appendChild(document.createTextNode(msg.slice(head.length)));
      say(frag, msg);
    }

    /* --- interaction -------------------------------------------- */
    function choose(i) {
      if (revealed) return;
      picked = i;
      render();
    }

    function primary() {
      if (!revealed) {
        if (picked < 0) return;
        revealed = true;
        attempted++;
        var right = picked === round.correct;
        if (right) {
          streak++;
          if (streak >= 3) mastered = true;
        } else {
          streak = 0;
        }
        render();
        if (right && mastered && streak === 3) {
          var f = document.createDocumentFragment();
          var b = document.createElement('b');
          b.className = 'ok';
          b.textContent = MASTERY.slice(0, MASTERY.indexOf('—') + 1);
          f.appendChild(b);
          f.appendChild(document.createTextNode(MASTERY.slice(b.textContent.length)));
          say(f, MASTERY);
        } else {
          caption(round.fb[picked], right);
        }
      } else {
        next();
      }
    }

    function next() {
      if (!queue.length) refill();
      var nxt = queue.shift();
      if (nxt === round && queue.length) { queue.push(nxt); nxt = queue.shift(); }
      round = nxt;
      picked = -1;
      revealed = false;
      render();
      cap.textContent = round.premise;
      sr.textContent = round.premise;
      optBtns[0].focus();
    }

    /* Escape clears a prediction that has not been committed */
    root.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && !revealed && picked >= 0) {
        picked = -1;
        render();
        ev.stopPropagation();
      }
    });

    /* --- first paint -------------------------------------------- */
    round = queue.shift();
    render();
    cap.textContent = round.premise;
  }

  window.SVWidget = {
    meta: {
      id: 'nanoparticle-surface-area-threshold',
      title: 'Same substance, smaller pieces',
      teaches: 'Cutting a solid adds no material but converts inside into surface: total ' +
        'surface area rises by the number of divisions per edge, so surface-area-to-volume ' +
        'ratio climbs as pieces shrink. In the 1-100 nm range so much of the substance is ' +
        'surface that it behaves unlike the bulk.'
    },
    mount: mount
  };
})();
