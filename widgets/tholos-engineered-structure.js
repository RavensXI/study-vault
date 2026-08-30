/* tholos-engineered-structure
   The Treasury of Atreus in section. A tholos is not a hole in a hillside and
   not a heap of stone: it is 33 dressed rings, each oversailing the one below,
   closed by a capstone, with the mound loading every block from above.

   ONE geometric model drives both the drawing and the marking. The profile
   r(y) = R(1-(y/H)^2)^0.75 fixes every ring's radius, so the step-in, the
   bearing left on each block, the closing span at the apex and the numbers
   quoted in the feedback all come from the same three lines of arithmetic.
   Change the profile and the picture and the prose move together.

   Self-contained: no imports, no network, every selector scoped to .svw-thol. */
(function () {
  'use strict';

  /* ---- the model ------------------------------------------------------ */
  /* Lesson figures: chamber about 14 m across and 13 m high, dromos about
     36 m long, inner lintel block over 100 tonnes, built about 1250 BC. */
  var R = 7, H = 13, N = 33, DEPTH = 1.2, PACK = 2.0, POW = 0.75;
  var CH = H / N;                      /* height of one ring, 0.394 m       */

  function rad(y) {                    /* inner radius of the dome at height y */
    var t = y / H;
    if (t <= 0) return R;
    if (t >= 1) return 0;
    return R * Math.pow(1 - t * t, POW);
  }
  function innerR(j) { return rad((j - 1) * CH); }        /* ring j, 1..N   */
  function stepIn(j) { return innerR(j - 1) - innerR(j); } /* oversail      */
  function bearing(j) { return DEPTH - stepIn(j); }        /* still bearing */

  var RING = 26;
  var TOPR = innerR(N);
  var CAPSPAN = 2 * TOPR;
  function d2(x) { return x.toFixed(2); }
  function d1(x) { return x.toFixed(1); }

  var S26 = d2(stepIn(RING)), B26 = d2(bearing(RING));     /* 0.29 / 0.91   */
  var S33 = d2(stepIn(N));                                 /* 0.56          */
  var CAPM = d1(CAPSPAN);                                  /* 1.7           */

  /* packing and mound: the same family of curve, one size up, so the fill
     wraps the dome with clearance everywhere */
  var RP = R + DEPTH + PACK, HP = H + PACK;
  function radP(y) {
    var t = y / HP;
    if (t >= 1) return 0;
    return RP * Math.pow(1 - t * t, POW);
  }

  var FIXED = (2 * R) + ' m across · ' + H + ' m high · ' + N + ' rings';

  /* ---- the rounds ----------------------------------------------------- */
  var ROUNDS = [
    {
      id: 'oversail', hi: 'ring', ov: 'ov-ring',
      fact: 'blocks ' + DEPTH + ' m deep · ring ' + RING + ' steps in ' + S26 + ' m',
      q: 'You are setting ring ' + RING + ' of the ' + N + ', its blocks ' + S26 +
         ' m further in than the ring below, out over the chamber. What stops it tipping in?',
      opts: [
        { ok: true,
          t: 'Most of each block still rests on the ring below, and the weight above pins its back.',
          fb: 'Right — you said the block is still bearing, and weighted from above. Ring ' + RING +
              ' creeps in only ' + S26 + ' m, so ' + B26 + ' m of each ' + DEPTH +
              ' m block still sits on the ring below, and every ring above presses on its back.' },
        { t: 'Nothing has to — the rings are heaped stone, held up by the hill packed round them.',
          fb: 'Not quite — you said a heap held by the hill. These are dressed blocks in level courses, each set a measured ' +
              S26 + ' m in from the one below. A heap has no courses and cannot leave a ' + (2 * R) + ' m room inside it.' },
        { t: 'Mortar and metal cramps fix every block to the ring underneath.',
          fb: 'Not quite — you said mortar and cramps. The blocks are laid dry, stone on stone. What holds ring ' +
              RING + ' is geometry and weight: ' + B26 + ' m of each block still bears on the ring below, and the rings above press on its back.' }
      ],
      note: 'Corbelling: the technique the lesson also meets in the galleries at Tiryns.'
    },
    {
      id: 'lintel', hi: 'door', ov: 'ov-door',
      fact: 'inner lintel block over 100 tonnes',
      q: 'A lintel of over a hundred tonnes spans the door, and a triangular gap is left open above it. Where does the mound’s weight travel?',
      opts: [
        { ok: true,
          t: 'Round the gap — the courses above lean in from both sides, into the jambs.',
          fb: 'Right — you said the load goes round the gap. The triangle is a hole left on purpose: the courses either side oversail until they meet above it, so the mound runs down into the jambs. The lintel carries little else.' },
        { t: 'Straight down onto the lintel — that is why the block weighs over a hundred tonnes.',
          fb: 'Not quite — you said the mound presses straight onto the lintel. Then no single stone could hold a hillside, whatever it weighed. The gap above it is left open on purpose, so the courses either side carry the load into the jambs.' },
        { t: 'There is nothing to carry — the chamber is a natural hollow in the hillside.',
          fb: 'Not quite — you said the chamber is a natural hollow. It is a stone dome, built up in an open pit and then buried, so earth sits on masonry the whole way up. That is why a gap was left above the lintel.' }
      ],
      note: 'Archaeologists call this a relieving triangle; the Lion Gate has one too.'
    },
    {
      id: 'mound', hi: 'pack', ov: 'ov-pack',
      fact: 'ring ' + N + ' steps in ' + S33 + ' m, the biggest step',
      q: 'Strip the mound and the packing off the finished dome, down to bare stone. What happens?',
      opts: [
        { ok: true,
          t: 'The upper rings lose the load pinning their backs, and are likeliest to fall in.',
          fb: 'Right — you said the top loses its hold. Ring ' + N + ' steps in ' + S33 +
              ' m, the biggest step in the dome, and has least stone above it. Take the mound and packing away and the crown goes first. The earth is structure, not cover.' },
        { t: 'Nothing — it is a cairn of piled stone, so taking the earth off just uncovers it.',
          fb: 'Not quite — you said a piled cairn. A cairn cannot leave a room ' + (2 * R) + ' m across and ' + H +
              ' m high inside it. This is ' + N + ' shaped rings, and archaeologists usually credit its survival to the fill packed round it.' },
        { t: 'Nothing — the rings meet in closed circles, so the dome locks itself.',
          fb: 'Not quite — you said it locks itself. There is no wedge and no keystone here: each ring simply oversails the one below, and the further in it steps the more it leans on weight from above.' }
      ],
      note: 'The tomb was built in a pit cut into the hillside, then buried.'
    },
    {
      id: 'apex', hi: 'cap', ov: 'ov-cap',
      fact: 'each ring ' + d2(CH) + ' m high',
      q: 'The rings climb ' + H + ' m, closing in as they rise. What finishes the very top of the dome?',
      opts: [
        { ok: true,
          t: 'One capstone, laid last over the hole that is left.',
          fb: 'Right — you said a single capstone. Run the rings up and the opening shrinks until only ' + CAPM +
              ' m of sky is left after ' + N + ' of them; one slab covers that. Nothing is wedged — the dome is finished, not keyed.' },
        { t: 'A wedge-shaped keystone, dropped in to lock the last ring.',
          fb: 'Not quite — you said a keystone. Keystones belong to true arches, where wedges press sideways on each other. Here every block lies flat and oversails the one below, and the last hole, ' +
              CAPM + ' m across, is simply covered.' },
        { t: 'Nothing — the stones run out and the earth heaped on top fills the last of it.',
          fb: 'Not quite — you said the earth fills it. Loose earth cannot bridge a hole; it would pour into the chamber. The rings close the span themselves until ' +
              CAPM + ' m is left, and one slab covers that.' }
      ],
      note: 'From inside, the closing rings give the tomb its beehive shape.'
    },
    {
      id: 'span', hi: 'void', ov: 'ov-span',
      fact: 'dromos 36 m to the door',
      q: 'The chamber floor is ' + (2 * R) + ' m across, and roofing it is the whole problem. How is that span covered in stone?',
      opts: [
        { ok: true,
          t: 'Each ring steps in, so the span shrinks course by course until one slab covers it.',
          fb: 'Right — you said the span is closed a ring at a time. No stone here bridges ' + (2 * R) +
              ' m: the widest gap any single block covers is the ' + CAPM + ' m left after ' + N +
              ' rings have crept inwards. One hard span becomes ' + N + ' easy ones.' },
        { t: 'Beams laid flat across the top, like the lintel — they had hundred-tonne blocks.',
          fb: 'Not quite — you said flat beams. The lintel is enormous, but it spans a doorway; stone laid flat snaps under its own weight long before ' +
              (2 * R) + ' m. Corbelling avoids the span: ' + N + ' rings close it to ' + CAPM + ' m.' },
        { t: 'It is not covered — the chamber is a cave, so the hill itself is the roof.',
          fb: 'Not quite — you said the hill is the roof. The tomb was dug as an open pit, built up in ' + N +
              ' stone rings and then buried. What you stand under is masonry, ' + H + ' m of it, not rock left in place.' }
      ],
      note: 'Work on this scale means rulers able to command labour for years.'
    }
  ];

  var MASTERY = ' That is three in a row — a tholos is built, not dug.';

  /* ---- drawing geometry ----------------------------------------------- */
  var SVGNS = 'http://www.w3.org/2000/svg';
  var VW = 300, VH = 136;
  var S = 7;                 /* px per metre                              */
  var FLOOR = 124, CX = 210;
  var FACE = CX - R * S - 35;      /* front of the mound, x = 126          */
  var MOUTH = 6;                   /* dromos mouth at the left            */
  var DOORH = 5.4;                 /* doorway height in metres            */

  function Y(h) { return FLOOR - h * S; }
  function X(sign, r) { return CX + sign * r * S; }

  function innerPts(sign) {
    var pts = [], j;
    for (j = 1; j <= N; j++) {
      pts.push([X(sign, innerR(j)), Y((j - 1) * CH)]);
      pts.push([X(sign, innerR(j)), Y(j * CH)]);
    }
    return pts;
  }
  function outerPts(sign) {
    var pts = [], j;
    for (j = 1; j <= N; j++) pts.push([X(sign, innerR(j) + DEPTH), Y((j - 1) * CH)]);
    pts.push([X(sign, innerR(N) + DEPTH), Y(N * CH)]);
    return pts;
  }
  function poly(pts) {
    var d = '', i;
    for (i = 0; i < pts.length; i++) {
      d += (i ? 'L' : 'M') + r1(pts[i][0]) + ',' + r1(pts[i][1]) + ' ';
    }
    return d;
  }
  function r1(v) { return Math.round(v * 10) / 10; }

  function bandPath(sign) {
    var out = outerPts(sign), inn = innerPts(sign).slice().reverse();
    return poly(out) + poly(inn).replace('M', 'L') + 'Z';
  }
  function voidPath() {
    var l = innerPts(-1), rr = innerPts(1).slice().reverse();
    return poly(l) + poly(rr).replace('M', 'L') + 'Z';
  }
  function packPath() {
    var pts = [], y, k;
    for (k = 0; k <= 30; k++) {
      y = (k / 30) * HP;
      pts.push([X(-1, radP(y)), Y(y)]);
    }
    for (k = 30; k >= 0; k--) {
      y = (k / 30) * HP;
      pts.push([X(1, radP(y)), Y(y)]);
    }
    return poly(pts) + 'Z';
  }
  function jointPath() {
    var d = '', j, sign, s;
    for (s = 0; s < 2; s++) {
      sign = s ? 1 : -1;
      for (j = 2; j <= N; j++) {
        d += 'M' + r1(X(sign, innerR(j))) + ',' + r1(Y((j - 1) * CH)) +
             'L' + r1(X(sign, innerR(j - 1) + DEPTH)) + ',' + r1(Y((j - 1) * CH)) + ' ';
      }
    }
    return d;
  }

  /* ---- widget --------------------------------------------------------- */
  window.SVWidget = {
    meta: {
      id: 'tholos-engineered-structure',
      title: 'How the tholos stands up',
      teaches: 'A Mycenaean tholos tomb is an engineered corbelled structure, not a cave or a heap: each ring oversails the last, a capstone closes the span, and the mound loads the dome into stability.'
    },
    /* ctx.reducedMotion needs no branch: this widget has no transition, no
       animation and no timer, so nothing ever moves unasked. */
    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';

      var wrap = document.createElement('div');
      wrap.className = 'svw-thol';
      wrap.style.setProperty('--t-acc', accent);

      var style = document.createElement('style');
      style.textContent = css();
      wrap.appendChild(style);

      wrap.insertAdjacentHTML('beforeend',
        '<p class="t-kick">Mycenaean architecture</p>' +
        '<p class="t-title">How the tholos stands up</p>' +
        '<p class="t-frame">Mycenae, about 1250 BC. The Treasury of Atreus, cut through the middle. ' +
        'Work out how the dome stands up instead of falling in.</p>' +
        '<div class="t-stage"></div>' +
        '<p class="t-fact" id="tfact"></p>' +
        '<div class="t-slot">' +
          '<p class="t-q" id="tq"></p>' +
          '<div class="t-opts" id="topts" role="group" aria-labelledby="tq"></div>' +
          '<div class="t-fb" id="tfb">' +
            '<span class="t-flag" id="tflag"></span>' +
            '<p class="t-say" id="tsay"></p>' +
            '<p class="t-note" id="tnote"></p>' +
          '</div>' +
        '</div>' +
        '<div class="t-act"><p class="t-run" id="trun"></p>' +
          '<button type="button" class="t-go" id="tgo" disabled>Check</button></div>' +
        '<p class="t-sr" id="tsr" aria-live="polite"></p>');

      root.appendChild(wrap);

      var svg = buildSvg();
      wrap.querySelector('.t-stage').appendChild(svg);

      var elFact = wrap.querySelector('#tfact');
      var elQ    = wrap.querySelector('#tq');
      var elOpts = wrap.querySelector('#topts');
      var elFb   = wrap.querySelector('#tfb');
      var elFlag = wrap.querySelector('#tflag');
      var elSay  = wrap.querySelector('#tsay');
      var elNote = wrap.querySelector('#tnote');
      var elRun  = wrap.querySelector('#trun');
      var elGo   = wrap.querySelector('#tgo');
      var elSr   = wrap.querySelector('#tsr');

      var btns = [], i;
      for (i = 0; i < 3; i++) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 't-opt';
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', onPick);
        elOpts.appendChild(b);
        btns.push(b);
      }

      var streak = 0, mastered = false, attempted = 0;
      var order = [], cursor = 0, round = null, shown = null, picked = -1, committed = false;

      function shuffle(a) {
        for (var j = a.length - 1; j > 0; j--) {
          var k = Math.floor(Math.random() * (j + 1)), t = a[j]; a[j] = a[k]; a[k] = t;
        }
        return a;
      }

      function clearMarks() {
        var m = svg.querySelectorAll('.t-mark');
        for (var a = 0; a < m.length; a++) m[a].classList.remove('t-mark');
        var o = svg.querySelectorAll('.t-ov.on');
        for (var c = 0; c < o.length; c++) o[c].classList.remove('on');
      }
      function markGroup(key) {
        var m = svg.querySelectorAll('[data-hi="' + key + '"]');
        for (var a = 0; a < m.length; a++) m[a].classList.add('t-mark');
      }

      function nextRound() {
        if (cursor >= order.length) {
          var last = order.length ? order[order.length - 1] : -1;
          order = shuffle(ROUNDS.map(function (_, k) { return k; }));
          if (order[0] === last && order.length > 1) {
            var t = order[0]; order[0] = order[1]; order[1] = t;
          }
          cursor = 0;
        }
        round = ROUNDS[order[cursor++]];
        shown = shuffle(round.opts.slice());
        picked = -1;
        committed = false;

        elFact.textContent = FIXED + ' · ' + round.fact;
        elQ.textContent = round.q;
        for (var m = 0; m < btns.length; m++) {
          btns[m].textContent = shown[m].t;
          btns[m].setAttribute('aria-pressed', 'false');
          btns[m].disabled = false;
        }
        elOpts.style.display = '';
        elFb.classList.remove('on');
        elGo.textContent = 'Check';
        elGo.disabled = true;
        clearMarks();
        markGroup(round.hi);
        paintRun();
        publish();
      }

      function onPick(ev) {
        if (committed) return;
        var b = ev.currentTarget;
        picked = btns.indexOf(b);
        for (var e = 0; e < btns.length; e++) {
          btns[e].setAttribute('aria-pressed', btns[e] === b ? 'true' : 'false');
        }
        elGo.disabled = false;
        publish();
      }

      function reveal() {
        committed = true;
        attempted++;
        var right = !!shown[picked].ok;
        if (right) { streak++; if (streak >= 3) mastered = true; } else { streak = 0; }

        elFlag.textContent = right ? 'Right' : 'Not quite';
        elFlag.className = 't-flag ' + (right ? 'ok' : 'no');
        elSay.textContent = shown[picked].fb + (right && streak === 3 ? MASTERY : '');
        elNote.textContent = round.note;
        elOpts.style.display = 'none';
        elFb.classList.add('on');

        var ov = svg.querySelector('#' + round.ov);
        if (ov) ov.classList.add('on');

        elGo.textContent = mastered ? 'Another anyway' : 'Next question';
        paintRun();
        elSr.textContent = elFlag.textContent + '. ' + elSay.textContent;
        publish();
      }

      function paintRun() {
        if (mastered) { elRun.textContent = 'Three in a row — you have it.'; return; }
        if (streak > 0) {
          elRun.textContent = streak + ' right in a row — ' + (3 - streak) + ' more.';
        } else {
          elRun.textContent = attempted > 1 && committed ? 'Run back to nought.' : '';
        }
      }

      elGo.addEventListener('click', function () {
        if (!committed) {
          if (picked < 0) return;
          reveal();
        } else {
          nextRound();
        }
        elGo.focus();
      });

      wrap.addEventListener('keydown', function (ev) {
        if (ev.key === 'Escape' && !committed && picked >= 0) {
          picked = -1;
          for (var g = 0; g < btns.length; g++) btns[g].setAttribute('aria-pressed', 'false');
          elGo.disabled = true;
          publish();
        }
      });

      function publish() {
        root.dataset.svState = JSON.stringify({
          round: round ? round.id : null,
          picked: picked,
          committed: committed,
          correct: committed ? !!shown[picked].ok : null,
          streak: streak,
          mastered: mastered,
          attempted: attempted,
          facts: {
            courses: N, span: 2 * R, height: H, blockDepth: DEPTH,
            ring: RING, stepIn: +S26, bearing: +B26, capSpan: +CAPM
          }
        });
      }

      nextRound();
    }
  };

  /* ---- the section ---------------------------------------------------- */
  function buildSvg() {
    var svg = document.createElementNS(SVGNS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + VW + ' ' + VH);
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svg.setAttribute('class', 't-svg');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label',
      'Section through the Treasury of Atreus: a long dromos leading to a doorway ' +
      'under a massive lintel with a triangular gap above it, opening into a dome ' +
      'of ' + N + ' corbelled rings closed by a capstone, all buried under a mound.');

    function n(tag, attrs, parent) {
      var e = document.createElementNS(SVGNS, tag), k;
      for (k in attrs) { if (attrs.hasOwnProperty(k)) e.setAttribute(k, attrs[k]); }
      (parent || svg).appendChild(e);
      return e;
    }
    function label(x, y, s, cls, anchor, parent) {
      var e = n('text', { x: x, y: y, class: cls || 't-lab', 'text-anchor': anchor || 'middle' }, parent);
      e.textContent = s;
      return e;
    }

    var HILL = 'C160,20 186,12 215,12 L300,15';
    function cutY(x) { return FLOOR - ((x - MOUTH) / (FACE - MOUTH)) * (FLOOR - 44); }

    /* earth mass, with the dromos cutting notched out of it */
    n('path', {
      class: 't-earth',
      d: 'M0,' + VH + ' L0,132 L' + MOUTH + ',' + FLOOR + ' L' + FACE + ',' + FLOOR +
         ' L' + FACE + ',44 ' + HILL + ' L300,' + VH + ' Z'
    });
    n('path', { class: 't-ground', d: 'M' + FACE + ',44 ' + HILL });

    /* the dromos: cut down into the slope, its far wall lined in stone */
    n('path', { class: 't-line', d: 'M' + MOUTH + ',' + FLOOR + ' L' + FACE + ',44 L' + FACE + ',' + FLOOR + ' Z' });
    var dj = '', dx;
    for (dx = 20; dx < FACE - 4; dx += 13) {
      dj += 'M' + dx + ',' + FLOOR + ' L' + dx + ',' + r1(cutY(dx) + 1) + ' ';
    }
    n('path', { class: 't-joint', d: dj });
    n('path', { class: 't-floor', d: 'M' + MOUTH + ',' + FLOOR + ' L' + FACE + ',' + FLOOR });
    /* break: the drawing omits most of the 36 m */
    n('rect', { class: 't-void', x: 46, y: 92, width: 11, height: 34 });
    n('path', { class: 't-brk', d: 'M46,125 L50,113 L46,101 L50,93 M57,125 L61,113 L57,101 L61,93' });
    n('path', { class: 't-dim', d: 'M10,118 L122,118 M10,115 L10,121 M122,115 L122,121' });

    n('path', { class: 't-pack', d: packPath(), 'data-hi': 'pack' });
    n('path', { class: 't-band', d: bandPath(-1) });
    n('path', { class: 't-band', d: bandPath(1) });
    n('path', { class: 't-joint', d: jointPath() });
    n('path', { class: 't-void', d: voidPath(), 'data-hi': 'void' });

    /* capstone over the hole the rings leave */
    n('rect', {
      class: 't-stone', 'data-hi': 'cap',
      x: r1(X(-1, TOPR + DEPTH)), y: r1(Y(H) - 6.3),
      width: r1(2 * (TOPR + DEPTH) * S), height: 6.3
    });

    /* ring 26, invisible until the round that asks about it */
    var ry = r1(Y(RING * CH)), rh = r1(CH * S);
    n('rect', { class: 't-ghost', 'data-hi': 'ring', x: r1(X(-1, innerR(RING) + DEPTH)),
                y: ry, width: r1(DEPTH * S), height: rh });
    n('rect', { class: 't-ghost', 'data-hi': 'ring', x: r1(X(1, innerR(RING))),
                y: ry, width: r1(DEPTH * S), height: rh });

    /* doorway, lintel and the triangular gap */
    n('rect', { class: 't-void', x: FACE, y: r1(Y(DOORH)), width: 170 - FACE, height: r1(FLOOR - Y(DOORH)) });
    n('path', { class: 't-face', d: 'M' + FACE + ',44 L' + FACE + ',' + r1(Y(DOORH)) });
    n('rect', { class: 't-stone', 'data-hi': 'door', x: 122, y: 78, width: 22, height: 8.2 });
    n('rect', { class: 't-stone', 'data-hi': 'door', x: 144, y: 78, width: 22, height: 8.2 });
    n('path', { class: 't-tri', 'data-hi': 'door', d: 'M128,78 L164,78 L146,57 Z' });
    n('path', { class: 't-joint', d: 'M124,74 L133,74 M124,69 L137,69 M124,64 L141,64 M124,59 L145,59' +
                                    ' M168,74 L159,74 M168,69 L155,69 M168,64 L151,64 M168,59 L147,59' });

    /* chamber width, measured on the model */
    n('path', { class: 't-dim', d: 'M' + r1(X(-1, R)) + ',117 L' + r1(X(1, R)) + ',117 M' +
                                   r1(X(-1, R)) + ',114 L' + r1(X(-1, R)) + ',120 M' +
                                   r1(X(1, R)) + ',114 L' + r1(X(1, R)) + ',120' });
    label(CX, 113, (2 * R) + ' m');

    /* ---- the detail: three rings at four times the size ---- */
    var IS = 4 * S, IX = 24, IY = 49;
    var bh = CH * IS, bd = DEPTH * IS, st = stepIn(RING) * IS, t;
    n('rect', { class: 't-detail', x: 8, y: 6, width: 90, height: 46, rx: 3 });
    n('rect', { class: 't-stone', x: r1(IX - st), y: r1(IY), width: r1(bd), height: r1(51 - IY) });
    for (t = 0; t < 3; t++) {
      n('rect', {
        class: 't-stone', 'data-hi': 'ring',
        x: r1(IX + t * st), y: r1(IY - (t + 1) * bh), width: r1(bd), height: r1(bh)
      });
    }
    var inA = r1(IX + st + bd), inB = r1(IX + 2 * st + bd);
    n('path', { class: 't-dim', d: 'M' + inA + ',24 L' + inA + ',14 M' + inB + ',15 L' + inB + ',14 M' +
                                   inA + ',14 L' + inB + ',14' });
    label(r1((inA + inB) / 2 + 9), 12, S26 + ' m');
    label(53, 59, 'detail: three rings, 4×');
    n('path', { class: 't-lead', d: 'M99,40 L166,70' });

    label(66, 113, 'dromos — 36 m');
    label(116, 92, 'lintel', 't-lab', 'end');
    n('path', { class: 't-lead', d: 'M118,91 L140,85' });
    label(292, 22, 'mound', 't-lab', 'end');
    label(292, 54, 'packing', 't-lab', 'end');
    n('path', { class: 't-lead', d: 'M288,58 L272,88' });
    label(232, 102, N + ' stone rings', 't-lab', 'end');
    n('path', { class: 't-lead', d: 'M234,100 L254,100' });

    /* ---- overlays: shown only after the student commits ---- */
    var g;

    g = n('g', { class: 't-ov', id: 'ov-ring' });
    n('rect', { class: 't-hl', x: r1(X(-1, innerR(RING) + DEPTH)), y: ry,
                width: r1(DEPTH * S), height: rh }, g);
    n('rect', { class: 't-hl', x: r1(X(1, innerR(RING))), y: ry,
                width: r1(DEPTH * S), height: rh }, g);
    n('rect', { class: 't-hl', x: r1(IX + 2 * st), y: r1(IY - 3 * bh), width: r1(bd), height: r1(bh) }, g);
    n('path', { class: 't-arw', d: 'M50,8 L50,14 M47,11 L50,15 L53,11' }, g);
    n('path', { class: 't-dim2', d: 'M' + r1(IX + 2 * st) + ',' + r1(IY - 2 * bh) +
                                    ' L' + r1(IX + st + bd) + ',' + r1(IY - 2 * bh) }, g);
    label(10, 72, B26 + ' m still bearing', 't-tag', 'start', g);
    n('path', { class: 't-lead2', d: 'M96,70 L' + r1(X(-1, innerR(RING))) + ',' + r1(+ry + 1) }, g);

    g = n('g', { class: 't-ov', id: 'ov-door' });
    n('path', { class: 't-arw2', d: 'M146,52 C130,60 126,70 126,78' }, g);
    n('path', { class: 't-arw2', d: 'M146,52 C162,60 166,70 166,78' }, g);
    n('path', { class: 't-arw', d: 'M123,73 L126,79 L129,73 M163,73 L166,79 L169,73' }, g);
    label(10, 72, 'load runs round the gap', 't-tag', 'start', g);
    n('path', { class: 't-lead2', d: 'M110,70 L134,62' }, g);

    g = n('g', { class: 't-ov', id: 'ov-pack' });
    n('path', { class: 't-hl2', d: packPath() }, g);
    n('path', { class: 't-arw', d: 'M168,50 L172,58 M169,55 L172,59 L175,54 M252,50 L248,58 M245,54 L248,59 L251,55' +
                                   ' M196,30 L198,40 M195,36 L198,41 L201,35 M224,30 L222,40 M219,36 L222,41 L225,35' }, g);
    label(258, 22, 'the mound loads every block', 't-tag', 'end', g);

    g = n('g', { class: 't-ov', id: 'ov-cap' });
    n('rect', { class: 't-hl', x: r1(X(-1, TOPR + DEPTH)), y: r1(Y(H) - 6.3),
                width: r1(2 * (TOPR + DEPTH) * S), height: 6.3 }, g);
    n('path', { class: 't-dim2', d: 'M' + r1(X(-1, TOPR)) + ',40 L' + r1(X(1, TOPR)) + ',40' }, g);
    label(210, 22, 'one slab over ' + CAPM + ' m', 't-tag', 'middle', g);
    n('path', { class: 't-lead2', d: 'M210,26 L210,40' }, g);

    g = n('g', { class: 't-ov', id: 'ov-span' });
    n('path', { class: 't-hl3', d: poly(innerPts(-1)) }, g);
    n('path', { class: 't-hl3', d: poly(innerPts(1)) }, g);
    label(10, 72, N + ' rings close it to ' + CAPM + ' m', 't-tag', 'start', g);
    n('path', { class: 't-lead2', d: 'M120,70 L170,62' }, g);

    return svg;
  }

  function css() {
    return [
'.svw-thol{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
'.svw-thol *{box-sizing:border-box}',
'.svw-thol p{margin:0}',
'.svw-thol .t-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--t-acc);margin:0 0 .2rem}',
'.svw-thol .t-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.18rem;font-weight:600;line-height:1.18;margin:0 0 .3rem}',
'.svw-thol .t-frame{font-size:.82rem;line-height:1.42;color:#5b564e;margin:0 0 .45rem}',
'.svw-thol .t-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;padding:.2rem;margin:0 auto .35rem;max-width:340px}',
'.svw-thol .t-svg{display:block;width:100%;height:auto}',
'.svw-thol .t-fact{font-size:.72rem;line-height:1.35;color:#8d8880;font-variant-numeric:tabular-nums;margin:0 0 .4rem}',
'.svw-thol .t-slot{min-height:168px}',
'.svw-thol .t-q{font-size:.85rem;font-weight:600;line-height:1.36;margin:0 0 .42rem}',
'.svw-thol .t-opts{display:flex;flex-direction:column;gap:.32rem}',
'.svw-thol .t-opt{display:block;width:100%;text-align:left;font:inherit;font-size:.82rem;line-height:1.34;font-weight:500;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.4rem .6rem;cursor:pointer}',
'.svw-thol .t-opt:hover:not(:disabled){border-color:#c6bdaf}',
'.svw-thol .t-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
'.svw-thol .t-opt:disabled{cursor:default;opacity:.55}',
'.svw-thol .t-fb{display:none}',
'.svw-thol .t-fb.on{display:block}',
'.svw-thol .t-flag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin:0 0 .22rem}',
'.svw-thol .t-flag.ok{color:#4f7d63}',
'.svw-thol .t-flag.no{color:#5b564e}',
'.svw-thol .t-say{font-size:.84rem;line-height:1.45;margin:0 0 .3rem}',
'.svw-thol .t-note{font-size:.75rem;line-height:1.42;color:#8d8880;margin:0}',
'.svw-thol .t-act{display:flex;align-items:center;justify-content:space-between;gap:.6rem;margin-top:.5rem}',
'.svw-thol .t-run{font-size:.76rem;line-height:1.3;color:#5b564e;font-variant-numeric:tabular-nums}',
'.svw-thol .t-go{flex:0 0 auto;font:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.5rem .95rem;cursor:pointer}',
'.svw-thol .t-go:disabled{background:#faf8f5;color:#a9a39a;border-color:#ddd7cd;cursor:default}',
'.svw-thol .t-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
/* the section */
'.svw-thol .t-earth{fill:#e7dfd1;stroke:none}',
'.svw-thol .t-pack{fill:#dbd0b9;stroke:none}',
'.svw-thol .t-band{fill:#f2ece0;stroke:#a99a7d;stroke-width:.7}',
'.svw-thol .t-void{fill:#faf8f5;stroke:none}',
'.svw-thol .t-stone{fill:#f2ece0;stroke:#8d8880;stroke-width:.7}',
'.svw-thol .t-tri{fill:#faf8f5;stroke:#8d8880;stroke-width:.7}',
'.svw-thol .t-joint{fill:none;stroke:#bcae8f;stroke-width:.45}',
'.svw-thol .t-line{fill:#f0eade;stroke:#b8ab93;stroke-width:.6}',
'.svw-thol .t-ground{fill:none;stroke:#b8ab93;stroke-width:.8}',
'.svw-thol .t-detail{fill:none;stroke:#e0d9cd;stroke-width:.8;rx:3}',
'.svw-thol .t-ghost{fill:none;stroke:none}',
'.svw-thol .t-brk{fill:none;stroke:#b8ab93;stroke-width:.8}',
'.svw-thol .t-floor{fill:none;stroke:#8d8880;stroke-width:1}',
'.svw-thol .t-face{fill:none;stroke:#8d8880;stroke-width:1}',
'.svw-thol .t-dim{fill:none;stroke:#8d8880;stroke-width:.7}',
'.svw-thol .t-lead{fill:none;stroke:#a09a90;stroke-width:.6}',
'.svw-thol .t-lab{font-family:Inter,system-ui,sans-serif;font-size:9px;fill:#5b564e;paint-order:stroke;stroke:#faf8f5;stroke-width:2.4;stroke-linejoin:round}',
'.svw-thol .t-mark{stroke:var(--t-acc);stroke-width:1.6}',
'.svw-thol .t-ov{display:none}',
'.svw-thol .t-ov.on{display:block}',
'.svw-thol .t-hl{fill:var(--t-acc);fill-opacity:.35;stroke:var(--t-acc);stroke-width:1}',
'.svw-thol .t-hl2{fill:var(--t-acc);fill-opacity:.16;stroke:var(--t-acc);stroke-width:1}',
'.svw-thol .t-hl3{fill:none;stroke:var(--t-acc);stroke-width:1.4}',
'.svw-thol .t-arw{fill:none;stroke:var(--t-acc);stroke-width:1.2;stroke-linecap:round}',
'.svw-thol .t-arw2{fill:none;stroke:var(--t-acc);stroke-width:1.4;stroke-linecap:round}',
'.svw-thol .t-dim2{fill:none;stroke:var(--t-acc);stroke-width:1.2}',
'.svw-thol .t-lead2{fill:none;stroke:var(--t-acc);stroke-width:.7}',
'.svw-thol .t-tag{font-family:Inter,system-ui,sans-serif;font-size:9px;font-weight:600;fill:#2d2a26;paint-order:stroke;stroke:#faf8f5;stroke-width:2.8;stroke-linejoin:round}'
    ].join('');
  }
})();
