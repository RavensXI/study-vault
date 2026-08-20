/* ============================================================
   current-not-used-up

   Series current is the same at every point. Charge travels a
   closed loop; energy is transferred at components, charge is not
   consumed. The student predicts every ammeter reading, commits,
   and only then sees the meters agree.
   ============================================================ */
(function () {
  'use strict';

  var OHM = 'Ω';

  /* ---- the circuits -------------------------------------------------
     Currents are held in milliamps so every comparison is an integer.
     given: index of the meter whose reading is printed for them, or
     null - those rounds hand over only the cell p.d. and the two
     resistances, so copying a number across is not available.        */
  var ROUNDS = [
    { cell: 6.0, c1: { name: 'Lamp P', r: 12 }, c2: { name: 'Lamp Q', r: 8 },
      given: 0, bank: [100, 150, 200, 300, 500] },
    { cell: 12.0, c1: { name: 'Resistor', r: 30 }, c2: { name: 'Lamp', r: 20 },
      given: null, bank: [120, 200, 240, 400, 600] },
    { cell: 9.0, c1: { name: 'Buzzer', r: 15 }, c2: { name: 'Resistor', r: 30 },
      given: 2, bank: [100, 200, 300, 450, 600] },
    { cell: 4.5, c1: { name: 'Lamp', r: 6 }, c2: { name: 'Motor', r: 3 },
      given: null, bank: [250, 300, 500, 750, 1500] },
    { cell: 6.0, c1: { name: 'Resistor', r: 10 }, c2: { name: 'Lamp', r: 5 },
      given: 1, bank: [200, 400, 600, 800, 1200] },
    { cell: 3.0, c1: { name: 'Lamp', r: 4 }, c2: { name: 'Resistor', r: 8 },
      given: null, bank: [150, 250, 300, 500, 750] }
  ];

  var GOAL = 3;                 /* three in a row and you are released */

  /* ---- geometry of the loop ---------------------------------------- */
  var VB_W = 340, VB_H = 176;
  var LX = 36, RX = 304, TY = 30, BY = 138;
  var PLATE_L = 162, PLATE_R = 178;

  /* conventional current: out of the long plate, left along the bottom,
     up the left side, across the top, down the right side, back in. */
  var SEG = [
    { x: PLATE_L, y: BY, dx: -1, dy: 0, l: PLATE_L - LX },
    { x: LX, y: BY, dx: 0, dy: -1, l: BY - TY },
    { x: LX, y: TY, dx: 1, dy: 0, l: RX - LX },
    { x: RX, y: TY, dx: 0, dy: 1, l: BY - TY },
    { x: RX, y: BY, dx: -1, dy: 0, l: RX - PLATE_R }
  ];
  var PERIM = 0;
  for (var si = 0; si < SEG.length; si++) PERIM += SEG[si].l;
  var NDOTS = 14, DOT_SPEED = 120, FLOW_MS = 6000;

  var METERS = [
    { cx: LX, cy: 84, tx: LX + 19, ty: 88, anchor: 'start', gy: 100 },
    { cx: 170, cy: TY, tx: 170, ty: 57, anchor: 'middle', gy: 69 },
    { cx: RX, cy: 84, tx: RX - 19, ty: 88, anchor: 'end', gy: 100 }
  ];

  function posAt(s) {
    s = ((s % PERIM) + PERIM) % PERIM;
    for (var i = 0; i < SEG.length; i++) {
      var g = SEG[i];
      if (s <= g.l) return [g.x + g.dx * s, g.y + g.dy * s];
      s -= g.l;
    }
    return [SEG[0].x, SEG[0].y];
  }

  function amps(ma) { return (ma / 1000).toFixed(2) + ' A'; }
  /* a teacher writes 6 V and 4.5 V, not 6.0 V - keep the decimal only
     where the value actually has one */
  function volts(v) {
    var x = Math.round(v * 10) / 10;
    return (x === Math.round(x) ? String(Math.round(x)) : x.toFixed(1)) + ' V';
  }

  function shuffled(n) {
    var a = [], i, j, t;
    for (i = 0; i < n; i++) a.push(i);
    for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1)); t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function shape(p) {
    var down = false, up = false, i;
    for (i = 1; i < p.length; i++) {
      if (p[i] < p[i - 1]) down = true;
      if (p[i] > p[i - 1]) up = true;
    }
    if (!down && !up) return 'flat';
    if (down && !up) return 'falling';
    if (up && !down) return 'rising';
    return 'mixed';
  }

  var CSS = [
    '.svw-cnu{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;',
    'color:#2d2a26;line-height:1.45}',
    '.svw-cnu *{box-sizing:border-box}',
    '.svw-cnu .cnu-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;',
    'text-transform:uppercase;color:var(--cnu-accent);margin:0 0 .16rem}',
    '.svw-cnu .cnu-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;',
    'font-size:1.22rem;line-height:1.2;margin:0}',
    /* the task frame: scenario + ask, in the header, above the stage */
    '.svw-cnu .cnu-frame{font-size:.84rem;line-height:1.45;color:#5b564e;margin:.3rem 0 0}',
    '.svw-cnu .cnu-frame b{font-weight:600;color:#2d2a26}',
    '.svw-cnu .cnu-steprow{display:flex;align-items:center;gap:.5rem}',
    '.svw-cnu .cnu-num{flex:0 0 auto;width:20px;height:20px;border-radius:50%;',
    'display:inline-flex;align-items:center;justify-content:center;font-size:.7rem;',
    'font-weight:700;border:1px solid #ddd7cd;background:#fff;color:#8d8880}',
    '.svw-cnu .cnu-num.is-now{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-cnu .cnu-num.is-done{background:#4f7d63;border-color:#4f7d63;color:#fff}',
    '.svw-cnu .cnu-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;',
    'padding:.45rem .4rem;margin:.65rem 0 .6rem}',
    '.svw-cnu .cnu-svg{display:block;width:100%;max-width:440px;height:auto;margin:0 auto;',
    'aspect-ratio:' + VB_W + '/' + VB_H + '}',
    '.svw-cnu .cnu-bank{display:flex;flex-wrap:wrap;gap:.4rem;flex:1 1 auto}',
    '.svw-cnu .cnu-chip{font-family:inherit;font-size:.82rem;font-weight:600;line-height:1;',
    'font-variant-numeric:tabular-nums;padding:.52rem .68rem;border:1px solid #ddd7cd;',
    'background:#faf8f5;color:#2d2a26;border-radius:10px;cursor:pointer}',
    '.svw-cnu .cnu-chip[aria-pressed="true"]{background:#2d2a26;color:#fff;border-color:#2d2a26}',
    '.svw-cnu .cnu-chip:disabled{opacity:.4;cursor:default}',
    '.svw-cnu .cnu-act{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin-top:.55rem}',
    '.svw-cnu .cnu-go{font-family:inherit;font-size:.82rem;font-weight:600;line-height:1;',
    'padding:.58rem 1rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;',
    'color:#fff;cursor:pointer}',
    '.svw-cnu .cnu-go:disabled{background:#faf8f5;color:#a49e94;border-color:#ddd7cd;cursor:default}',
    '.svw-cnu .cnu-streak{font-size:.76rem;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svw-cnu .cnu-cap{font-size:.86rem;line-height:1.5;color:#3a352e;margin:.55rem 0 0;',
    'min-height:2.4rem}',
    '.svw-cnu .cnu-cap b{font-weight:600}',
    '.svw-cnu .cnu-cap b.ok{color:#4f7d63}',
    '.svw-cnu .cnu-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;',
    'overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svw-cnu .cnu-wire{fill:none;stroke:#b3aa9d;stroke-width:2.2;stroke-linecap:round}',
    '.svw-cnu .cnu-arrow{fill:#b3aa9d}',
    '.svw-cnu .cnu-box{fill:#fff;stroke:#2d2a26;stroke-width:1.4}',
    '.svw-cnu .cnu-name{font-family:inherit;font-size:10.5px;font-weight:500;fill:#6f6a62}',
    '.svw-cnu .cnu-ohm{font-family:inherit;font-size:11px;font-weight:600;fill:#2d2a26}',
    '.svw-cnu .cnu-cellv{font-family:inherit;font-size:11px;font-weight:600;fill:#2d2a26}',
    '.svw-cnu .cnu-read{font-family:inherit;font-size:12px;font-weight:600;fill:#a49e94;',
    'font-variant-numeric:tabular-nums}',
    '.svw-cnu .cnu-read.is-set{fill:#2d2a26}',
    '.svw-cnu .cnu-read.is-true{fill:var(--cnu-accent)}',
    '.svw-cnu .cnu-tag{font-family:inherit;font-size:9.5px;font-weight:500;fill:#8d8880}',
    '.svw-cnu .cnu-pd{font-family:inherit;font-size:10.5px;font-weight:600;',
    'fill:var(--cnu-accent);visibility:hidden}',
    '.svw-cnu .cnu-pd.is-on{visibility:visible}',
    '.svw-cnu .cnu-face{fill:#fff;stroke:#2d2a26;stroke-width:1.4}',
    '.svw-cnu .cnu-sym{font-family:inherit;font-size:10px;font-weight:700;fill:#2d2a26}',
    '.svw-cnu .cnu-meter{cursor:pointer;outline:none}',
    '.svw-cnu .cnu-ring{fill:none;stroke:var(--cnu-accent);stroke-width:2;',
    'stroke-dasharray:3.2 3.2;opacity:0}',
    '.svw-cnu .cnu-meter.is-active .cnu-ring{opacity:1}',
    '.svw-cnu .cnu-meter:focus .cnu-ring{opacity:1;stroke-dasharray:none}',
    '.svw-cnu .cnu-meter:focus-visible .cnu-ring{opacity:1;stroke-dasharray:none}',
    '.svw-cnu .cnu-dot{fill:var(--cnu-accent)}',
    '.svw-cnu .cnu-flow{visibility:hidden}',
    '.svw-cnu .cnu-flow.is-on{visibility:visible}'
  ].join('');

  function svgMarkup() {
    var s = [];
    s.push('<svg class="cnu-svg" viewBox="0 0 ' + VB_W + ' ' + VB_H + '" role="img" ');
    s.push('aria-label="A series circuit: a cell, two components and three ammeters in one loop.">');

    /* wire: the whole rectangle, minus the gap where the cell sits */
    s.push('<path class="cnu-wire" d="M' + PLATE_L + ' ' + BY + ' H' + LX + ' V' + TY +
           ' H' + RX + ' V' + BY + ' H' + PLATE_R + '"/>');

    /* direction arrows on the wire */
    var arrows = [[100, BY, 180], [LX, 112, -90], [66, TY, 0], [RX, 112, 90]];
    for (var a = 0; a < arrows.length; a++) {
      s.push('<polygon class="cnu-arrow" points="0,0 -6,-3.6 -6,3.6" transform="translate(' +
             arrows[a][0] + ',' + arrows[a][1] + ') rotate(' + arrows[a][2] + ')"/>');
    }

    /* cell */
    s.push('<line class="cnu-wire" x1="' + PLATE_L + '" y1="' + (BY - 15) + '" x2="' +
           PLATE_L + '" y2="' + (BY + 15) + '" stroke-width="2"/>');
    s.push('<line class="cnu-wire" x1="' + PLATE_R + '" y1="' + (BY - 8) + '" x2="' +
           PLATE_R + '" y2="' + (BY + 8) + '" stroke-width="3.4"/>');
    s.push('<text class="cnu-cellv" data-k="cell" x="170" y="164" text-anchor="middle">6.0 V</text>');

    /* the two components */
    var cx = [110, 230];
    for (var c = 0; c < 2; c++) {
      s.push('<text class="cnu-name" data-k="name' + c + '" x="' + cx[c] +
             '" y="13" text-anchor="middle">Lamp</text>');
      s.push('<rect class="cnu-box" x="' + (cx[c] - 30) + '" y="' + (TY - 11) +
             '" width="60" height="22" rx="3"/>');
      /* the resistance sits BELOW the box: the box interior is left clear
         so the moving charge is seen passing straight through it. */
      s.push('<text class="cnu-ohm" data-k="ohm' + c + '" x="' + cx[c] +
             '" y="53" text-anchor="middle">12 ' + OHM + '</text>');
      s.push('<text class="cnu-pd" data-k="pd' + c + '" x="' + cx[c] +
             '" y="67" text-anchor="middle">0.0 V</text>');
    }

    /* ammeters */
    for (var m = 0; m < 3; m++) {
      var M = METERS[m];
      s.push('<g class="cnu-meter" data-meter="' + m + '" tabindex="0" role="button" ' +
             'aria-label="Ammeter A' + (m + 1) + '">');
      s.push('<circle class="cnu-ring" cx="' + M.cx + '" cy="' + M.cy + '" r="17"/>');
      s.push('<circle class="cnu-face" cx="' + M.cx + '" cy="' + M.cy + '" r="12.5"/>');
      s.push('<text class="cnu-sym" x="' + M.cx + '" y="' + (M.cy + 3.5) +
             '" text-anchor="middle">A' + (m + 1) + '</text>');
      s.push('</g>');
      s.push('<text class="cnu-read" data-k="read' + m + '" x="' + M.tx + '" y="' + M.ty +
             '" text-anchor="' + M.anchor + '">?</text>');
      s.push('<text class="cnu-tag" data-k="tag' + m + '" x="' + M.tx + '" y="' + M.gy +
             '" text-anchor="' + M.anchor + '"></text>');
    }

    /* moving charge, drawn last so it passes over the components */
    s.push('<g class="cnu-flow" data-k="flow">');
    for (var d = 0; d < NDOTS; d++) s.push('<circle class="cnu-dot" r="3" cx="-20" cy="-20"/>');
    s.push('</g>');

    s.push('</svg>');
    return s.join('');
  }

  window.SVWidget = {
    meta: {
      id: 'current-not-used-up',
      title: 'Where does the current go?',
      teaches: 'Current is the same at every point in a series circuit: charge flows in a closed loop and is not used up. Components differ because they take different shares of the potential difference.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
                   ctx.accent || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;

      var wrap = document.createElement('div');
      wrap.className = 'svw-cnu';
      wrap.style.setProperty('--cnu-accent', accent);
      wrap.innerHTML =
        '<style>' + CSS + '</style>' +
        '<div class="cnu-kick">Series circuits</div>' +
        '<h3 class="cnu-title">Where does the current go?</h3>' +
        '<p class="cnu-frame" data-k="frame"></p>' +
        '<div class="cnu-stage">' + svgMarkup() + '</div>' +
        '<div class="cnu-controls">' +
          '<div class="cnu-steprow">' +
            '<span class="cnu-num" data-k="n1" aria-hidden="true">1</span>' +
            '<div class="cnu-bank" role="group" aria-label="Step 1: readings to place">' +
              '<button type="button" class="cnu-chip"></button>' +
              '<button type="button" class="cnu-chip"></button>' +
              '<button type="button" class="cnu-chip"></button>' +
              '<button type="button" class="cnu-chip"></button>' +
              '<button type="button" class="cnu-chip"></button>' +
            '</div>' +
          '</div>' +
          '<div class="cnu-act">' +
            '<span class="cnu-num" data-k="n2" aria-hidden="true">2</span>' +
            '<button type="button" class="cnu-go">Check the readings</button>' +
            '<span class="cnu-streak"></span>' +
          '</div>' +
        '</div>' +
        '<p class="cnu-cap"></p>' +
        '<p class="cnu-sr" aria-live="polite"></p>';
      root.appendChild(wrap);

      var el = {};
      var keyed = wrap.querySelectorAll('[data-k]');
      for (var i = 0; i < keyed.length; i++) el[keyed[i].getAttribute('data-k')] = keyed[i];
      var chips = wrap.querySelectorAll('.cnu-chip');
      var meters = wrap.querySelectorAll('.cnu-meter');
      var reads = [el.read0, el.read1, el.read2];
      var tags = [el.tag0, el.tag1, el.tag2];
      var dots = el.flow.querySelectorAll('.cnu-dot');
      var go = wrap.querySelector('.cnu-go');
      var cap = wrap.querySelector('.cnu-cap');
      var streakEl = wrap.querySelector('.cnu-streak');
      var live = wrap.querySelector('.cnu-sr');

      /* round 1 always opens: it is the one with a reading already on the
         dial, so the first move needs no explaining. */
      var order = shuffled(ROUNDS.length);
      order.splice(order.indexOf(0), 1);
      order.unshift(0);
      var pos = 0;
      var streak = 0, attempted = 0, mastered = false;
      var R, I, picks, active, revealed, wasRight;
      var raf = 0;

      /* ---- charge flow ------------------------------------------- */
      function placeDots(s0) {
        var gap = PERIM / NDOTS;
        for (var d = 0; d < NDOTS; d++) {
          var p = posAt(s0 + d * gap);
          dots[d].setAttribute('cx', p[0].toFixed(1));
          dots[d].setAttribute('cy', p[1].toFixed(1));
        }
      }
      function stopFlow() {
        if (raf) { cancelAnimationFrame(raf); raf = 0; }
        el.flow.classList.remove('is-on');
      }
      function startFlow() {
        stopFlow();
        el.flow.classList.add('is-on');
        placeDots(0);
        if (reduced) return;                  /* static, evenly spaced */
        var t0 = (window.performance && performance.now) ? performance.now() : Date.now();
        var step = function (t) {
          if (!wrap.isConnected) { raf = 0; return; }
          var dt = t - t0;
          placeDots(dt / 1000 * DOT_SPEED);
          raf = dt < FLOW_MS ? requestAnimationFrame(step) : 0;
        };
        raf = requestAnimationFrame(step);
      }

      /* ---- state ------------------------------------------------- */
      function publish() {
        root.dataset.svState = JSON.stringify({
          circuit: ROUNDS.indexOf(R) + 1,
          givenMeter: R.given === null ? null : R.given + 1,
          picks_mA: picks.slice(),
          trueCurrent_mA: I,
          checked: revealed,
          correct: revealed ? wasRight : null,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      function filled() {
        return picks[0] !== null && picks[1] !== null && picks[2] !== null;
      }

      function drawMeters() {
        var m, c;
        for (m = 0; m < 3; m++) {
          /* picks stays the student's answer all the way through, so the
             diagnosis reads what they actually did; the dials show the
             true reading once it is revealed. */
          var v = revealed ? I : picks[m];
          reads[m].textContent = v === null ? '?' : amps(v);
          reads[m].classList.toggle('is-set', v !== null);
          reads[m].classList.toggle('is-true', revealed);
          tags[m].textContent = (!revealed && R.given === m) ? 'given' : '';
          meters[m].classList.toggle('is-active', !revealed && m === active);
        }
        for (c = 0; c < 5; c++) {
          var on = !revealed && active !== null && picks[active] === R.bank[c];
          chips[c].setAttribute('aria-pressed', on ? 'true' : 'false');
        }
        setSteps();
      }

      /* The two control groups are numbered, and the number shows where the
         student is: step 1 is live until every dial is set, then it goes
         green and step 2 lights up with the button it belongs to. */
      function setSteps() {
        var done = filled();
        el.n1.classList.toggle('is-now', !revealed && !done);
        el.n1.classList.toggle('is-done', done);
        el.n2.classList.toggle('is-now', !revealed && done);
        el.n2.classList.toggle('is-done', revealed);
      }

      function setStreakLine() {
        var t = '';
        if (mastered) t = 'Mastered.';
        else if (streak === 1) t = '1 in a row — 2 more.';
        else if (streak === 2) t = '2 in a row — 1 more to go.';
        else if (attempted > 0) t = 'Back to zero — 3 in a row finishes.';
        streakEl.textContent = t;
      }

      /* The task frame: the situation, then the ask - the way a question
         paper states it. It never says what the readings will do. */
      function pairPhrase() {
        if (R.c1.name.indexOf('Lamp') === 0 && R.c2.name.indexOf('Lamp') === 0) return 'two lamps';
        return 'a ' + R.c1.name.toLowerCase() + ' and a ' + R.c2.name.toLowerCase();
      }
      function taskFrame() {
        var scene = 'A ' + volts(R.cell) + ' cell, ' + pairPhrase() + ', one loop. ';
        if (R.given === null) {
          return scene + 'No ammeter is reading yet. Predict the readings at A1, A2 and A3.';
        }
        var others = [];
        for (var m = 0; m < 3; m++) if (m !== R.given) others.push('A' + (m + 1));
        return scene + 'Ammeter A' + (R.given + 1) + ' reads <b>' + amps(I) +
               '</b>. Predict the readings at ' + others[0] + ' and ' + others[1] + '.';
      }

      function note() {
        var big = R.c1.r >= R.c2.r ? R.c1 : R.c2;
        var small = R.c1.r >= R.c2.r ? R.c2 : R.c1;
        var bigV = volts(I * big.r / 1000), smallV = volts(I * small.r / 1000);
        if (R.c1.name.indexOf('Lamp') === 0 && R.c2.name.indexOf('Lamp') === 0) {
          return big.name + ' has the larger resistance, so it takes ' + bigV + ' of the ' +
                 volts(R.cell) + ' while ' + small.name + ' takes ' + smallV +
                 ' — same current, different brightness.';
        }
        return 'The ' + big.name.toLowerCase() + ' takes ' + bigV + ' of the ' + volts(R.cell) +
               ' and the ' + small.name.toLowerCase() + ' takes ' + smallV +
               '. Energy is shared out along the loop; charge is not.';
      }

      function feedback() {
        var s = shape(picks), same = amps(I);
        var theirs = amps(picks[0]) + ', ' + amps(picks[1]) + ', ' + amps(picks[2]);
        var sum = R.c1.r + R.c2.r;
        if (wasRight) {
          if (mastered) {
            return '<b class="ok">Three in a row — you have it.</b> ' + same +
                   ' at every meter. In series the current is the same at every point: charge ' +
                   'travels a loop and none of it is used up. What gets shared out is the ' +
                   'potential difference — the bigger resistance takes the bigger share.';
          }
          return '<b>Right — ' + same + ' at every meter.</b> One loop, one path: every ' +
                 'coulomb that leaves the cell passes A1, both components and A3, then goes ' +
                 'back in. ' + note();
        }
        if (s === 'falling') {
          return '<b>Not quite.</b> You had the readings falling round the loop: ' + theirs +
                 '. Charge cannot leak out of the wire or pile up inside a component, so every ' +
                 'meter reads <b>' + same + '</b>. A component takes energy from the charge, ' +
                 'not the charge itself.';
        }
        if (s === 'rising') {
          return '<b>Not quite.</b> You had the current growing round the loop: ' + theirs +
                 '. The cell does not make new charge — it pushes the charge already in the ' +
                 'wires. Every meter reads <b>' + same + '</b>.';
        }
        if (s === 'mixed') {
          return '<b>Not quite.</b> Your readings disagree: ' + theirs + '. There is no junction ' +
                 'in this circuit where charge could leave or gather, so all three meters must ' +
                 'read the same: <b>' + same + '</b>.';
        }
        /* flat, but the wrong value */
        var only = null;
        if (picks[0] === Math.round(R.cell * 1000 / R.c1.r)) only = R.c1;
        else if (picks[0] === Math.round(R.cell * 1000 / R.c2.r)) only = R.c2;
        var lead = '<b>Close.</b> The same reading everywhere is right' +
                   (only ? ' — but you used only the ' + only.r + ' ' + OHM + ' ' +
                    only.name.toLowerCase() + '. ' : ' — but not that value. ');
        return lead + 'In series the resistances add: ' + R.c1.r + ' ' + OHM + ' + ' + R.c2.r +
               ' ' + OHM + ' = ' + sum + ' ' + OHM + ', so I = V ÷ R = ' + volts(R.cell) + ' ÷ ' +
               sum + ' ' + OHM + ' = <b>' + same + '</b> at all three meters.';
      }

      function say(html) {
        cap.innerHTML = html;
        live.textContent = cap.textContent;
      }

      /* ---- rounds ------------------------------------------------ */
      function loadRound() {
        var c;
        R = ROUNDS[order[pos]];
        I = Math.round(R.cell * 1000 / (R.c1.r + R.c2.r));
        picks = [null, null, null];
        if (R.given !== null) picks[R.given] = I;
        active = picks[0] === null ? 0 : (picks[1] === null ? 1 : 2);
        revealed = false;
        wasRight = false;

        el.cell.textContent = volts(R.cell);
        el.name0.textContent = R.c1.name;
        el.name1.textContent = R.c2.name;
        el.ohm0.textContent = R.c1.r + ' ' + OHM;
        el.ohm1.textContent = R.c2.r + ' ' + OHM;
        el.pd0.textContent = volts(I * R.c1.r / 1000);
        el.pd1.textContent = volts(I * R.c2.r / 1000);
        el.pd0.classList.remove('is-on');
        el.pd1.classList.remove('is-on');

        for (c = 0; c < 5; c++) {
          chips[c].textContent = amps(R.bank[c]);
          chips[c].disabled = false;
        }
        go.textContent = 'Check the readings';
        go.disabled = !filled();
        stopFlow();
        el.frame.innerHTML = taskFrame();
        drawMeters();
        setStreakLine();
        /* the caption is feedback only: before a commit there is nothing
           honest to put in it that is not the ask or the answer */
        cap.textContent = '';
        live.textContent = el.frame.textContent;
        publish();
      }

      function assign(ma) {
        if (revealed || active === null) return;
        picks[active] = ma;
        var placed = active, nxt = -1, m;
        for (m = 0; m < 3; m++) {
          if (picks[m] === null) { nxt = m; break; }
        }
        if (nxt !== -1) active = nxt;
        go.disabled = !filled();
        drawMeters();
        live.textContent = 'A' + (placed + 1) + ' set to ' + amps(ma) +
          (filled() ? '. All three meters are set.' : '.');
        publish();
      }

      function commit() {
        if (!filled()) return;
        revealed = true;
        attempted++;
        wasRight = picks[0] === I && picks[1] === I && picks[2] === I;
        streak = wasRight ? streak + 1 : 0;
        if (wasRight && streak >= GOAL) mastered = true;
        active = null;
        el.pd0.classList.add('is-on');
        el.pd1.classList.add('is-on');
        for (var c = 0; c < 5; c++) chips[c].disabled = true;
        go.textContent = mastered ? 'Another anyway' : 'Next circuit';
        go.disabled = false;
        drawMeters();
        setStreakLine();
        say(feedback());
        startFlow();
        publish();
      }

      function next() {
        pos++;
        if (pos >= order.length) { order = shuffled(ROUNDS.length); pos = 0; }
        loadRound();
      }

      /* ---- wiring ------------------------------------------------ */
      for (var ci = 0; ci < chips.length; ci++) {
        (function (k) {
          chips[k].addEventListener('click', function () { assign(R.bank[k]); });
        }(ci));
      }
      for (var mi = 0; mi < meters.length; mi++) {
        (function (k) {
          var pick = function () {
            if (revealed) return;
            active = k;
            drawMeters();
            live.textContent = 'Meter A' + (k + 1) + ' selected.';
          };
          meters[k].addEventListener('click', pick);
          meters[k].addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
              e.preventDefault();
              pick();
            }
          });
        }(mi));
      }
      go.addEventListener('click', function () {
        if (revealed) { next(); } else { commit(); }
      });

      loadRound();
    }
  };
}());
