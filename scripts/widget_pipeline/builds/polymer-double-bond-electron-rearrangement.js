/* ------------------------------------------------------------------
   polymer-double-bond-electron-rearrangement

   Addition polymerisation: the C=C opens, one of its two bonds breaks,
   and those electrons become the single bonds that join monomer to
   monomer. Nothing is lost and nothing is added.

   Shape: the student commits a prediction (which drawing is the repeat
   unit?), then the reveal steps the mechanism on the anchor case,
   ethene, with the atom tally summed from the molecule model rather
   than asserted.
   ------------------------------------------------------------------ */
(function () {
  'use strict';

  var SVGNS = 'http://www.w3.org/2000/svg';

  /* ---------- the molecule model ------------------------------------ */

  /* Every atom count in the widget is summed from these lists. */
  var GROUP_ATOMS = {
    'H':   { C: 0, H: 1 },
    'Cl':  { Cl: 1 },
    'CH₃': { C: 1, H: 3 }
  };

  var MONOMERS = [
    { id: 'ethene', name: 'Ethene', formula: 'CH₂=CH₂',
      polymer: 'poly(ethene)', left: ['H', 'H'], right: ['H', 'H'] },
    { id: 'propene', name: 'Propene', formula: 'CH₂=CHCH₃',
      polymer: 'poly(propene)', left: ['H', 'H'], right: ['H', 'CH₃'] },
    { id: 'chloroethene', name: 'Chloroethene', formula: 'CH₂=CHCl',
      polymer: 'poly(chloroethene)', left: ['H', 'H'], right: ['H', 'Cl'] }
  ];

  var SUBS = '₀₁₂₃₄₅₆₇₈₉';
  var SUB_N = 'ₙ';
  var DASH = '–';

  function subDigits(n) {
    return String(n).split('').map(function (d) { return SUBS.charAt(+d); }).join('');
  }

  function addAtoms(total, group) {
    for (var k in group) { if (group[k]) total[k] = (total[k] || 0) + group[k]; }
    return total;
  }

  /* atoms in one unit built from a {left, right} substituent spec */
  function atomsOf(spec) {
    var total = { C: 2 };
    spec.left.concat(spec.right).forEach(function (s) {
      addAtoms(total, GROUP_ATOMS[s]);
    });
    return total;
  }

  function atomPhrase(total, suffix) {
    var parts = [];
    ['C', 'H', 'Cl'].forEach(function (k) {
      if (!total[k]) { return; }
      var n = (total[k] === 1 && suffix) ? suffix : total[k] + (suffix || '');
      parts.push(n + ' ' + k);
    });
    if (parts.length < 2) return parts[0] || 'no atoms';
    return parts.slice(0, -1).join(', ') + ' and ' + parts[parts.length - 1];
  }

  function atomDiff(full, reduced) {
    var missing = {};
    ['C', 'H', 'Cl'].forEach(function (k) {
      var d = (full[k] || 0) - (reduced[k] || 0);
      if (d > 0) missing[k] = d;
    });
    return missing;
  }

  /* condensed text for one carbon and its two substituents */
  function carbonText(subs) {
    var h = 0, others = [];
    subs.forEach(function (s) { if (s === 'H') { h++; } else { others.push(s); } });
    var t = 'C';
    if (h === 1) { t += 'H'; } else if (h > 1) { t += 'H' + subDigits(h); }
    others.forEach(function (o) { t += (o.length > 2 ? '(' + o + ')' : o); });
    return t;
  }

  /* the "atoms fall off" wrong picture: a side group is lost, or on
     ethene one H from each carbon */
  function loseSpec(m) {
    var hasGroup = m.right.some(function (s) { return s !== 'H'; });
    if (hasGroup) {
      return { left: m.left.slice(), right: m.right.filter(function (s) { return s === 'H'; }) };
    }
    return { left: ['H'], right: ['H'] };
  }

  /* ---------- the candidate repeat units ---------------------------- */

  function candidates(m) {
    var L = carbonText(m.left), R = carbonText(m.right);
    var lost = loseSpec(m);
    return {
      correct: {
        key: 'correct',
        text: DASH + '[' + DASH + L + DASH + R + DASH + ']' + DASH + SUB_N
      },
      keep: {
        key: 'keep',
        text: DASH + '[' + DASH + L + '=' + R + DASH + ']' + DASH + SUB_N
      },
      lose: {
        key: 'lose',
        text: DASH + '[' + DASH + carbonText(lost.left) + DASH +
              carbonText(lost.right) + DASH + ']' + DASH + SUB_N,
        missing: atomDiff(atomsOf(m), atomsOf(lost))
      },
      nobond: {
        key: 'nobond',
        text: '[' + L + DASH + R + ']' + SUB_N
      }
    };
  }

  /* which two wrong pictures each round offers, and where the right one sits */
  var WRONG_PAIRS = [['keep', 'lose'], ['lose', 'nobond'], ['nobond', 'keep']];
  var SLOT_ORDER = [[1, 0, 2], [2, 1, 0], [0, 2, 1], [1, 2, 0]];

  function speak(text) {
    return text
      .replace(/\[/g, ' open bracket ').replace(/\]/g, ' close bracket ')
      .replace(/=/g, ' double bond ')
      .replace(new RegExp(DASH, 'g'), ' bond ')
      .replace(new RegExp(SUB_N, 'g'), ' subscript n ')
      .replace(/₂/g, ' two ').replace(/₃/g, ' three ')
      .replace(/\s+/g, ' ').trim();
  }

  /* ---------- drawing ------------------------------------------------ */

  var VB_W = 274, VB_H = 112;
  var Y = 56, Y_TOP = 16, Y_BOT = 96;
  /* apart while they are still three molecules, evenly spaced once joined,
     so no C-C bond in the chain is drawn longer than any other */
  var SEP_X  = [24, 60, 116, 152, 208, 244];
  var JOIN_X = [32, 72, 112, 152, 192, 232];
  var BIG_X = [118, 158];

  function el(parent, name, attrs) {
    var n = document.createElementNS(SVGNS, name);
    for (var k in attrs) { if (attrs[k] !== null) n.setAttribute(k, attrs[k]); }
    parent.appendChild(n);
    return n;
  }

  function bond(g, x1, y1, x2, y2, dim) {
    el(g, 'line', { x1: x1, y1: y1, x2: x2, y2: y2, 'stroke-width': 1.7,
      stroke: '#2d2a26', 'stroke-linecap': 'round', opacity: dim ? 0.26 : 1 });
  }

  function text(g, x, y, s, size, dim) {
    var t = el(g, 'text', { x: x, y: y, 'text-anchor': 'middle',
      'dominant-baseline': 'central', 'font-size': size, fill: '#2d2a26',
      'font-family': 'Inter, system-ui, sans-serif', opacity: dim ? 0.26 : 1 });
    t.textContent = s;
    return t;
  }

  function dot(g, x, y, accent) {
    el(g, 'circle', { cx: x, cy: y, r: 3.4, fill: accent });
  }

  function carbon(g, x, subs, size, dim) {
    var gap = size * 0.62;
    text(g, x, Y, 'C', size, dim);
    if (subs[0]) {
      bond(g, x, Y - gap, x, Y_TOP + gap, dim);
      text(g, x, Y_TOP, subs[0], size, dim);
    }
    if (subs[1]) {
      bond(g, x, Y + gap, x, Y_BOT - gap, dim);
      text(g, x, Y_BOT, subs[1], size, dim);
    }
  }

  function link(g, x1, x2, size, double, dim) {
    var gap = size * 0.62;
    if (double) {
      bond(g, x1 + gap, Y - 4, x2 - gap, Y - 4, dim);
      bond(g, x1 + gap, Y + 4, x2 - gap, Y + 4, dim);
    } else {
      bond(g, x1 + gap, Y, x2 - gap, Y, dim);
    }
  }

  function bracket(g, x, dir) {
    var top = 10, bot = 102, arm = 8 * dir;
    el(g, 'path', { d: 'M' + (x + arm) + ',' + top + ' L' + x + ',' + top +
      ' L' + x + ',' + bot + ' L' + (x + arm) + ',' + bot,
      fill: 'none', stroke: '#2d2a26', 'stroke-width': 1.7,
      'stroke-linecap': 'round', 'stroke-linejoin': 'round' });
  }

  /* scene names: monomer | separate | opened | joined | bracketed | repeat */
  function drawScene(svg, scene, m, accent) {
    while (svg.firstChild) { svg.removeChild(svg.firstChild); }
    var g = el(svg, 'g', {});
    var size, i, x;

    if (scene === 'monomer' || scene === 'repeat') {
      size = 17;
      carbon(g, BIG_X[0], m.left, size, false);
      carbon(g, BIG_X[1], m.right, size, false);
      link(g, BIG_X[0], BIG_X[1], size, scene === 'monomer', false);
      if (scene === 'repeat') {
        /* the brackets clear the widest side group, so a CH3 never
           collides with the closing bracket */
        var widest = m.left.concat(m.right).reduce(function (a, t) {
          return Math.max(a, t.length);
        }, 1);
        var half = 40 + (widest > 2 ? 14 : (widest > 1 ? 6 : 0));
        var mid = (BIG_X[0] + BIG_X[1]) / 2;
        var bx1 = mid - half, bx2 = mid + half;
        bracket(g, bx1, 1);
        bracket(g, bx2, -1);
        bond(g, bx1 - 20, Y, BIG_X[0] - size * 0.62, Y, false);
        bond(g, BIG_X[1] + size * 0.62, Y, bx2 + 20, Y, false);
        dot(g, bx1 - 12, Y, accent);
        dot(g, bx2 + 12, Y, accent);
        text(g, bx2 + 10, Y_BOT + 6, SUB_N, 15, false);
      }
      return;
    }

    size = 14;
    var apart = (scene === 'separate' || scene === 'opened');
    var xs = apart ? SEP_X : JOIN_X;
    var subsFor = function (k) { return (k % 2 === 0) ? m.left : m.right; };

    for (i = 0; i < 6; i++) {
      var dim = (scene === 'bracketed') && (i < 2 || i > 3);
      carbon(g, xs[i], subsFor(i), size, dim);
    }
    /* the bond inside each monomer */
    for (i = 0; i < 3; i++) {
      var dim2 = (scene === 'bracketed') && (i !== 1);
      link(g, xs[2 * i], xs[2 * i + 1], size,
           scene === 'separate', dim2);
    }

    if (scene === 'opened') {
      for (i = 0; i < 6; i++) {
        x = xs[i] + (i % 2 === 0 ? -15 : 15);
        dot(g, x, Y, accent);
      }
    }

    if (scene === 'joined' || scene === 'bracketed') {
      /* the two new links: each made from one freed electron per carbon */
      [[1, 2], [3, 4]].forEach(function (pair) {
        var a = xs[pair[0]] + 8.7, b = xs[pair[1]] - 8.7;
        bond(g, a, Y, b, Y, false);
        dot(g, a + (b - a) * 0.34, Y, accent);
        dot(g, a + (b - a) * 0.66, Y, accent);
      });
      /* the chain carries on at both ends */
      var ends = (scene === 'bracketed');
      bond(g, xs[0] - 8.7, Y, xs[0] - 24, Y, ends);
      if (!ends) { dot(g, xs[0] - 20, Y, accent); }
      bond(g, xs[5] + 8.7, Y, xs[5] + 24, Y, ends);
      if (!ends) { dot(g, xs[5] + 20, Y, accent); }
    }

    if (scene === 'bracketed') {
      bracket(g, 92, 1);
      bracket(g, 172, -1);
      text(g, 182, Y_BOT + 5, SUB_N, 13, false);
    }
  }

  /* ---------- styles -------------------------------------------------- */

  function css(accent) {
    return [
      '.svw-poly{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;',
        'color:#2d2a26;line-height:1.45;-webkit-text-size-adjust:100%}',
      '.svw-poly *{box-sizing:border-box}',
      '.svw-poly .p-kicker{font-size:.66rem;font-weight:700;letter-spacing:.11em;',
        'text-transform:uppercase;color:' + accent + '}',
      '.svw-poly .p-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;',
        'font-size:1.18rem;margin:.15rem 0 .3rem;line-height:1.2}',
      '.svw-poly .p-frame{font-size:.86rem;margin:0 0 .55rem;color:#3f3a33}',
      '.svw-poly .p-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;',
        'padding:.25rem}',
      '.svw-poly .p-stage svg{display:block;width:100%;height:128px}',
      '.svw-poly .p-opts{display:grid;gap:.4rem;margin:.55rem 0 .35rem;',
        'grid-template-columns:repeat(auto-fit,minmax(238px,1fr))}',
      '.svw-poly .p-opt{display:flex;align-items:center;justify-content:space-between;',
        'flex-wrap:wrap;',
        'gap:.5rem;width:100%;text-align:left;font-family:inherit;color:#2d2a26;',
        'background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;',
        'padding:.42rem .6rem;cursor:pointer}',
      '.svw-poly .p-form{font-size:1rem;font-weight:600;letter-spacing:.01em;',
        'font-variant-numeric:tabular-nums;white-space:nowrap}',
      '.svw-poly .p-tag{font-size:.7rem;font-weight:600;color:#8d8880;white-space:nowrap}',
      '.svw-poly .p-opt[aria-pressed="true"]{background:' + accent + '1f;',
        'border-color:' + accent + '}',
      '.svw-poly .p-opt[data-mark="right"]{border-color:#4f7d63;background:#4f7d6314}',
      '.svw-poly .p-opt[data-mark="right"] .p-tag{color:#4f7d63}',
      '.svw-poly .p-opt[data-mark="yours"]{border-color:#2d2a26;background:#fff}',
      '.svw-poly .p-opt:disabled{cursor:default;opacity:1}',
      '.svw-poly .p-run{font-size:.78rem;color:#8d8880;margin:0;min-height:1.15rem}',
      '.svw-poly .p-actions{display:flex;gap:.5rem;align-items:center;margin:.15rem 0 .1rem}',
      '.svw-poly .p-go{font-family:inherit;font-size:.82rem;font-weight:600;',
        'padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;',
        'background:#2d2a26;color:#fff;cursor:pointer}',
      '.svw-poly .p-go:disabled{background:#faf8f5;color:#a49e95;border-color:#ddd7cd;',
        'cursor:default}',
      '.svw-poly .p-cap{font-size:.84rem;line-height:1.5;margin:.45rem 0 0;',
        'color:#3f3a33;min-height:6.2em}',
      '.svw-poly .p-sr{position:absolute;width:1px;height:1px;overflow:hidden;',
        'clip:rect(0 0 0 0);white-space:nowrap;margin:-1px;padding:0;border:0}'
    ].join('');
  }

  /* ---------- mount --------------------------------------------------- */

  function mount(root, ctx) {
    ctx = ctx || {};
    var own = (window.getComputedStyle(root).getPropertyValue('--accent') || '').trim();
    var accent = own || ctx.accent || '#8a6a4f';

    root.classList.add('svw-poly');
    root.innerHTML = '';

    var style = document.createElement('style');
    style.textContent = css(accent);
    root.appendChild(style);

    var head = document.createElement('div');
    head.innerHTML = '<div class="p-kicker">Addition polymerisation</div>' +
      '<h3 class="p-title">From monomer to repeat unit</h3>';
    var frame = document.createElement('p');
    frame.className = 'p-frame';
    head.appendChild(frame);
    root.appendChild(head);

    var stage = document.createElement('div');
    stage.className = 'p-stage';
    var svg = document.createElementNS(SVGNS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + VB_W + ' ' + VB_H);
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svg.setAttribute('role', 'img');
    stage.appendChild(svg);
    root.appendChild(stage);

    var opts = document.createElement('div');
    opts.className = 'p-opts';
    opts.setAttribute('role', 'group');
    opts.setAttribute('aria-label', 'Candidate repeat units');
    root.appendChild(opts);

    var run = document.createElement('p');
    run.className = 'p-run';
    root.appendChild(run);

    var actions = document.createElement('div');
    actions.className = 'p-actions';
    var go = document.createElement('button');
    go.type = 'button';
    go.className = 'p-go';
    go.textContent = 'Check';
    go.disabled = true;
    actions.appendChild(go);
    root.appendChild(actions);

    var cap = document.createElement('p');
    cap.className = 'p-cap';
    root.appendChild(cap);

    var sr = document.createElement('p');
    sr.className = 'p-sr';
    sr.setAttribute('aria-live', 'polite');
    root.appendChild(sr);

    /* three option buttons, built once and mutated thereafter */
    var buttons = [];
    for (var i = 0; i < 3; i++) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'p-opt';
      b.setAttribute('aria-pressed', 'false');
      b.innerHTML = '<span class="p-form"></span><span class="p-tag"></span>';
      opts.appendChild(b);
      buttons.push(b);
      b.addEventListener('click', (function (idx) {
        return function () { pick(idx); };
      })(i));
    }
    go.addEventListener('click', advance);

    /* ---------- state ------------------------------------------------- */

    var st = { round: 0, picked: null, committed: false, wasRight: null,
               streak: 0, attempted: 0, mastered: false, step: 0, brokeRun: false };
    var slots = [];   /* the three candidate objects in display order */
    var mono, cands;

    function publish() {
      root.dataset.svState = JSON.stringify({
        monomer: mono.id,
        picked: st.picked,
        committed: st.committed,
        correct: st.wasRight,
        step: st.step,
        streak: st.streak,
        attempted: st.attempted,
        mastered: st.mastered
      });
    }

    function say(msg) { sr.textContent = msg; }

    function newRound() {
      mono = MONOMERS[st.round % MONOMERS.length];
      cands = candidates(mono);
      var pair = WRONG_PAIRS[st.round % WRONG_PAIRS.length];
      var pool = [cands.correct, cands[pair[0]], cands[pair[1]]];
      var order = SLOT_ORDER[st.round % SLOT_ORDER.length];
      slots = order.map(function (k) { return pool[k]; });

      st.picked = null;
      st.committed = false;
      st.wasRight = null;
      st.step = 0;

      frame.textContent = 'n molecules of ' + mono.name.toLowerCase() + ' (' +
        mono.formula + ') polymerise. Choose the repeat unit of the ' +
        mono.polymer + ' formed.';

      buttons.forEach(function (btn, idx) {
        var c = slots[idx];
        btn.disabled = false;
        btn.removeAttribute('data-mark');
        btn.setAttribute('aria-pressed', 'false');
        btn.querySelector('.p-form').textContent = c.text;
        btn.querySelector('.p-tag').textContent = '';
        btn.setAttribute('aria-label', 'Option ' + (idx + 1) + ': ' + speak(c.text));
      });

      go.textContent = 'Check';
      go.disabled = true;
      drawScene(svg, 'monomer', mono, accent);
      svg.setAttribute('aria-label', mono.name + ', ' + mono.formula +
        ', drawn with its carbon to carbon double bond.');

      var one = atomsOf(mono);
      cap.textContent = 'One ' + mono.name.toLowerCase() + ' molecule holds ' +
        atomPhrase(one) + ', so n of them bring ' + atomPhrase(one, 'n') +
        ' into the reaction.';
      runLine();
      publish();
      say(mono.name + '. Three candidate repeat units offered.');
    }

    function runLine() {
      if (st.mastered) {
        run.textContent = 'You have it — carry on for another if you want.';
      } else if (st.streak === 0) {
        run.textContent = !st.attempted ? ''
          : (st.brokeRun ? 'That one reset the run — three in a row finishes it.'
                         : 'Three right in a row finishes it.');
      } else if (st.streak === 1) {
        run.textContent = '1 right in a row — two more and you have it.';
      } else {
        run.textContent = '2 right in a row — one more and you have it.';
      }
    }

    function pick(idx) {
      if (st.committed) { return; }
      st.picked = slots[idx].key;
      buttons.forEach(function (btn, j) {
        btn.setAttribute('aria-pressed', j === idx ? 'true' : 'false');
      });
      go.disabled = false;
      publish();
      say('Chosen: ' + speak(slots[idx].text));
    }

    /* ---------- the reveal -------------------------------------------- */

    function verdict() {
      var chosen = slots.filter(function (c) { return c.key === st.picked; })[0];
      var one = atomsOf(mono);
      if (st.picked === 'correct') {
        return 'Right — ' + chosen.text + '. The C=C opened: one of its two ' +
          'bonds broke, and those two electrons became the links to the units ' +
          'either side. All ' + atomPhrase(one, 'n') + ' are still there.';
      }
      if (st.picked === 'keep') {
        return 'Not quite — you chose ' + chosen.text + ', which keeps the ' +
          'C=C. Then nothing joins one unit to the next. One of the two bonds ' +
          'must break, and its electrons make the links.';
      }
      if (st.picked === 'lose') {
        return 'Not quite — you chose ' + chosen.text + ', which has lost ' +
          atomPhrase(chosen.missing) + '. Nothing leaves in addition ' +
          'polymerisation: the polymer is the only product, so everything ' +
          'attached to the carbons rides along unchanged.';
      }
      return 'Not quite — you chose ' + chosen.text + ', with no bonds ' +
        'through the brackets. Those bonds are what the C=C electrons made, and ' +
        'they show where the next unit joins.';
    }

    var STEPS = [
      { scene: 'separate', label: 'Open the bond' },
      { scene: 'opened', label: 'Join them up' },
      { scene: 'joined', label: 'Bracket one unit' },
      { scene: 'bracketed', label: 'Next monomer' }
    ];

    function stepCaption(n) {
      var three = {};
      var one = atomsOf(mono);
      ['C', 'H', 'Cl'].forEach(function (k) { if (one[k]) three[k] = one[k] * 3; });
      if (n === 1) {
        return 'One of the two bonds in each C=C has broken. Its two electrons ' +
          'are now one on each carbon — nothing has left the molecules: ' +
          'still ' + atomPhrase(three) + '.';
      }
      if (n === 2) {
        return 'Each pair of freed electrons has paired up into a new C–C ' +
          'single bond between neighbouring monomers. The electrons on the outer ' +
          'carbons are the open bonds where the chain carries on.';
      }
      return 'The bonds drawn through the brackets are the ones the opened C=C ' +
        'made, which is why the repeat unit shows them. n monomers give n repeat ' +
        'units: ' + atomPhrase(three) + ' in, ' + atomPhrase(three) + ' out.';
    }

    function commit() {
      st.committed = true;
      st.attempted++;
      st.wasRight = (st.picked === 'correct');
      st.brokeRun = (!st.wasRight && st.streak > 0);
      if (st.wasRight) {
        st.streak++;
        if (st.streak >= 3) { st.mastered = true; }
      } else {
        st.streak = 0;
      }

      buttons.forEach(function (btn, idx) {
        var c = slots[idx];
        btn.disabled = true;
        var tag = '';
        if (c.key === 'correct') { btn.setAttribute('data-mark', 'right'); tag = 'the repeat unit'; }
        if (c.key === st.picked) {
          tag = (c.key === 'correct') ? 'your answer · the repeat unit' : 'your answer';
          if (c.key !== 'correct') { btn.setAttribute('data-mark', 'yours'); }
        }
        btn.querySelector('.p-tag').textContent = tag;
      });

      var msg = verdict();
      if (st.mastered && st.streak === 3) {
        msg = 'Three in a row — you have it. Each C=C gives up one of its ' +
          'two bonds, and those electrons become the links along the chain. ' +
          'Every monomer atom is in the polymer.';
      }
      cap.textContent = msg;

      if (st.round === 0) {
        st.step = 0;
        drawScene(svg, STEPS[0].scene, mono, accent);
        svg.setAttribute('aria-label', 'Three ethene molecules, each with a ' +
          'carbon to carbon double bond.');
        go.textContent = STEPS[0].label;
      } else {
        drawScene(svg, 'repeat', mono, accent);
        svg.setAttribute('aria-label', 'The repeat unit of ' + mono.polymer +
          ', bracketed, with single bonds passing through the brackets.');
        go.textContent = st.mastered ? 'Another anyway' : 'Next monomer';
      }
      runLine();
      publish();
      say(msg);
    }

    function advance() {
      if (!st.committed) {
        if (!st.picked) { return; }
        commit();
        return;
      }
      if (st.round === 0 && st.step < 3) {
        st.step++;
        drawScene(svg, STEPS[st.step].scene, mono, accent);
        cap.textContent = stepCaption(st.step);
        go.textContent = STEPS[st.step].label;
        svg.setAttribute('aria-label', stepCaption(st.step));
        publish();
        say(cap.textContent);
        return;
      }
      st.round++;
      newRound();
    }

    newRound();
  }

  window.SVWidget = {
    meta: {
      id: 'polymer-double-bond-electron-rearrangement',
      title: 'From monomer to repeat unit',
      teaches: 'In addition polymerisation the C=C opens: one of its two bonds ' +
        'breaks and those electrons form the single bonds joining monomer to ' +
        'monomer, so no atoms are lost and nothing is added.'
    },
    mount: mount
  };
})();
