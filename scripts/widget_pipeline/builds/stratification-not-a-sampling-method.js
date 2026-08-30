/* ============================================================
   stratification-not-a-sampling-method — "Two decisions, not one"

   A stratified sample is planned in two moves. First the strata fix
   HOW MANY come from each group, in proportion to group size. Then a
   random method still has to choose WHICH individuals — inside every
   group. Students who think stratification IS the sampling method
   stop after move one.

   So the student commits to both: an allocation across the drawn
   population, and a selection method. The misconception — "sorting
   into the groups is the sampling" — is an option in every round,
   as is "everyone in the groups" for the allocation.

   Everything (allocation, distractors, the drawn sample, the
   feedback arithmetic) is computed from the population model, so the
   picture cannot contradict the marking.
   ============================================================ */
(function () {
  'use strict';

  /* ---------- the populations ----------------------------------------
     Every stratum is a multiple of 5 so it draws as clean rows of five,
     and every share n_i = N_i x n / N is a whole number.                */

  var ROUNDS = [
    { place: 'Fairfield High', unit: 'students', prep: 'in',
      gw: 'year group', gwp: 'year groups', list: 'register',
      chooser: 'the head of year', sample: 15,
      groups: [{ name: 'Year 9', n: 30 }, { name: 'Year 10', n: 25 }, { name: 'Year 11', n: 20 }] },

    { place: 'Riverside Gym', unit: 'members', prep: 'in',
      gw: 'age band', gwp: 'age bands', list: 'membership list',
      chooser: 'the manager', sample: 16,
      groups: [{ name: '16–29', n: 20 }, { name: '30–49', n: 30 }, { name: '50–69', n: 20 }, { name: '70+', n: 10 }] },

    { place: 'Hillcrest Hospital', unit: 'staff', prep: 'in',
      gw: 'job group', gwp: 'job groups', list: 'staff list',
      chooser: 'the ward manager', sample: 8,
      groups: [{ name: 'Nurses', n: 30 }, { name: 'Doctors', n: 10 }, { name: 'Admin', n: 20 }, { name: 'Porters', n: 20 }] },

    { place: 'Beechwood College', unit: 'students', prep: 'on',
      gw: 'course', gwp: 'courses', list: 'register',
      chooser: 'the course leader', sample: 20,
      groups: [{ name: 'Art', n: 25 }, { name: 'Science', n: 30 }, { name: 'Health', n: 15 }, { name: 'Sport', n: 30 }] },

    { place: 'Marsden Rowing Club', unit: 'members', prep: 'in',
      gw: 'membership group', gwp: 'membership groups', list: 'membership list',
      chooser: 'the club captain', sample: 15,
      groups: [{ name: 'Junior', n: 20 }, { name: 'Adult', n: 30 }, { name: 'Senior', n: 25 }] }
  ];

  /* ---------- the model ---------------------------------------------- */

  function popOf(r) {
    var s = 0, i;
    for (i = 0; i < r.groups.length; i++) s += r.groups[i].n;
    return s;
  }
  function allocOf(r) {                    /* proportional share, exact */
    var N = popOf(r), out = [], i;
    for (i = 0; i < r.groups.length; i++) out.push(r.groups[i].n * r.sample / N);
    return out;
  }
  function equalOf(r) {
    var k = r.groups.length, out = [], i;
    for (i = 0; i < k; i++) out.push(r.sample / k);
    return out;
  }
  function reverseOf(a) { return a.slice().reverse(); }
  function sizesOf(r) {
    var out = [], i;
    for (i = 0; i < r.groups.length; i++) out.push(r.groups[i].n);
    return out;
  }
  function join(a) { return a.join(' · '); }

  /* four distinct allocations, the right one first */
  function allocOptions(r) {
    var right = allocOf(r);
    var cands = [
      { key: 'right', v: right },
      { key: 'equal', v: equalOf(r) },
      { key: 'inverse', v: reverseOf(right) },
      { key: 'whole', v: sizesOf(r) }
    ];
    var seen = {}, out = [], i, lab;
    for (i = 0; i < cands.length; i++) {
      lab = join(cands[i].v);
      if (seen[lab]) continue;
      seen[lab] = 1;
      cands[i].label = lab;
      out.push(cands[i]);
    }
    var bump = 1;
    while (out.length < 4) {               /* insurance only; never runs on this data */
      var v = right.slice();
      v[0] = v[0] + bump;
      lab = join(v);
      if (!seen[lab]) { seen[lab] = 1; out.push({ key: 'slip', v: v, label: lab }); }
      bump++;
    }
    return out;
  }

  function methodOptions(r) {
    return [
      { key: 'random', label: 'Random numbers pick inside each group',
        echo: 'drawn with random numbers inside each group',
        chip: 'random numbers inside each group' },
      { key: 'strataOnly', label: 'Sorting into groups is the sampling',
        echo: 'and that sorting into the ' + r.gwp + ' is the sampling',
        chip: 'the groups are the sample' },
      { key: 'first', label: 'Take the first names on each list',
        echo: 'taking the first names on the ' + r.list,
        chip: 'the first names on each list' },
      { key: 'chooser', label: cap(r.chooser) + ' chooses the sample',
        echo: 'with ' + r.chooser + ' choosing',
        chip: r.chooser + ' chooses' }
    ];
  }

  /* deterministic 32-bit shuffle: the drawn sample scatters through a
     stratum instead of sitting at the top, and the option order moves */
  function rng(seed) {
    var s = (seed | 0) || 2463534242;
    return function () {
      s ^= s << 13; s |= 0;
      s ^= s >>> 17;
      s ^= s << 5; s |= 0;
      return (s >>> 0) / 4294967296;
    };
  }
  function shuffle(arr, seed) {
    var a = arr.slice(), rnd = rng(seed * 2654435761 + 17), i, j, t;
    for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(rnd() * (i + 1));
      t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function drawFrom(size, take, seed) {    /* which dots the random draw lands on */
    var idx = [], i;
    for (i = 0; i < size; i++) idx.push(i);
    return shuffle(idx, seed).slice(0, take);
  }

  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  var WORD = { 2: 'two', 3: 'three', 4: 'four', 5: 'five', 8: 'eight', 10: 'ten' };
  function word(n) { return WORD[n] || String(n); }
  function listOut(a) {                    /* 6, 5 and 4 */
    if (a.length === 1) return String(a[0]);
    return a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
  }
  function firstDiff(a, b) {
    for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return i;
    return 0;
  }
  /* "The Year 9 group is 30 of the 75, so it gives 30/75 × 15 = 6" */
  function shareLine(r, i) {
    var N = popOf(r), A = allocOf(r);
    return 'The ' + r.groups[i].name + ' group is ' + r.groups[i].n + ' of the ' + N +
      ', so it gives ' + r.groups[i].n + '/' + N + ' × ' + r.sample + ' = ' + A[i];
  }

  function allocWhy(r, opt) {
    var A = allocOf(r), N = popOf(r), i;
    if (opt.key === 'equal') {
      i = firstDiff(A, opt.v);
      return 'The same number from every group ignores that the ' + r.gwp +
        ' are different sizes. ' + shareLine(r, i) + ', not ' + opt.v[i] + '.';
    }
    if (opt.key === 'inverse') {
      i = firstDiff(A, opt.v);
      return 'Those are the right numbers on the wrong groups — they run in reverse. ' +
        shareLine(r, i) + ', not ' + opt.v[i] + '.';
    }
    if (opt.key === 'whole') {
      return 'That is all ' + N + ' of them, not a sample of ' + r.sample +
        '. The ' + r.gwp + ' organise the sample frame — the sample is drawn from them.';
    }
    i = firstDiff(A, opt.v);
    return shareLine(r, i) + ', not ' + opt.v[i] + '.';
  }

  function methodWhy(r, opt) {
    var A = allocOf(r), N = popOf(r);
    if (opt.key === 'strataOnly') {
      return 'Sorting is only the first move: it fixes how many come from each ' + r.gw +
        ', not which ' + r.unit + '. Nothing has been picked yet — you would still be holding all ' +
        N + '. Number each ' + r.gw + ' on the ' + r.list + ' and draw ' + listOut(A) +
        ' with random numbers.';
    }
    if (opt.key === 'first') {
      return 'The top of a ' + r.list + ' is not a random choice. A ' + r.list +
        ' has an order — alphabetical, or who joined first — so the same ' + r.unit +
        ' come up every time and everyone lower down never appears. Draw the names with random numbers instead.';
    }
    if (opt.key === 'chooser') {
      return 'A person choosing is not random either: ' + r.chooser +
        ' picks the ones expected to answer well, and that bias goes straight into the results. Number the ' +
        r.list + ' and let random numbers choose.';
    }
    return '';
  }

  /* ---------- widget -------------------------------------------------- */

  window.SVWidget = {
    meta: {
      id: 'stratification-not-a-sampling-method',
      title: 'Choosing a stratified sample',
      teaches: 'Stratification only divides the population into groups and fixes each group’s share of the sample; a random method must still choose the individuals inside every group.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var nodeAccent = '';
      try { nodeAccent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim(); } catch (e) {}
      var accent = ctx.accent || nodeAccent || '#4f7d63';
      var still = !!ctx.reducedMotion;

      root.className = (root.className ? root.className + ' ' : '') + 'svw-strat';
      if (still) root.className += ' svw-strat--still';
      root.style.setProperty('--svw-a', accent);

      root.innerHTML = [
        '<p class="svw-strat__kicker">Sampling</p>',
        '<h3 class="svw-strat__title">Choosing a stratified sample</h3>',
        '<p class="svw-strat__frame" data-r="frame"></p>',
        '<div class="svw-strat__stage">',
        '  <div class="svw-strat__strata" data-r="strata" role="img"></div>',
        '  <p class="svw-strat__note" data-r="note"></p>',
        '</div>',
        '<div class="svw-strat__step" data-r="step1">',
        '  <p class="svw-strat__lab"><span class="svw-strat__num">1</span> <span data-r="lab1"></span></p>',
        '  <div class="svw-strat__opts svw-strat__opts--num" data-r="opts1" role="group"></div>',
        '  <button type="button" class="svw-strat__chip" data-r="chip1" disabled hidden></button>',
        '</div>',
        '<div class="svw-strat__step" data-r="step2" hidden>',
        '  <p class="svw-strat__lab"><span class="svw-strat__num">2</span> <span data-r="lab2"></span></p>',
        '  <div class="svw-strat__opts svw-strat__opts--txt" data-r="opts2" role="group"></div>',
        '  <button type="button" class="svw-strat__chip" data-r="chip2" disabled hidden></button>',
        '</div>',
        '<div class="svw-strat__actions">',
        '  <button type="button" class="svw-strat__primary" data-r="check" disabled>Check</button>',
        '  <button type="button" class="svw-strat__ghost" data-r="next" hidden>Next sample</button>',
        '  <span class="svw-strat__run" data-r="run"></span>',
        '</div>',
        '<p class="svw-strat__caption" data-r="caption"></p>',
        '<p class="svw-strat__sr" data-r="sr" aria-live="polite"></p>'
      ].join('');

      var style = document.createElement('style');
      style.textContent = CSS;
      root.insertBefore(style, root.firstChild);

      var el = {}, nodes = root.querySelectorAll('[data-r]'), i;
      for (i = 0; i < nodes.length; i++) el[nodes[i].getAttribute('data-r')] = nodes[i];

      /* option buttons are built once and relabelled each round */
      var btn1 = [], btn2 = [], k;
      for (k = 0; k < 4; k++) {
        btn1.push(mkOpt(el.opts1, 1, k));
        btn2.push(mkOpt(el.opts2, 2, k));
      }
      function mkOpt(host, which, idx) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'svw-strat__opt';
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', function () { pick(which, idx); });
        host.appendChild(b);
        return b;
      }

      var S = { round: 0, streak: 0, attempted: 0, mastered: false,
                pick1: -1, pick2: -1, revealed: false, o1: [], o2: [] };
      var dots = [];

      el.check.addEventListener('click', commit);
      el.next.addEventListener('click', function () {
        S.round = (S.round + 1) % ROUNDS.length; newRound();
      });
      el.chip1.addEventListener('click', function () { if (!S.revealed) reopen(1); });
      el.chip2.addEventListener('click', function () { if (!S.revealed) reopen(2); });

      /* ---- the stage: one dot per person, five to a row, groups bottom-aligned ---- */

      function buildStage() {
        var r = ROUNDS[S.round], g, j, col, wrap, d, lab, sz, arr;
        el.strata.innerHTML = '';
        dots = [];
        for (g = 0; g < r.groups.length; g++) {
          col = document.createElement('div');
          col.className = 'svw-strat__stratum';
          wrap = document.createElement('div');
          wrap.className = 'svw-strat__dots';
          wrap.setAttribute('aria-hidden', 'true');
          arr = [];
          for (j = 0; j < r.groups[g].n; j++) {
            d = document.createElement('span');
            d.className = 'svw-strat__dot';
            wrap.appendChild(d);
            arr.push(d);
          }
          dots.push(arr);
          lab = document.createElement('p');
          lab.className = 'svw-strat__glab';
          lab.textContent = r.groups[g].name;
          sz = document.createElement('p');
          sz.className = 'svw-strat__gsize';
          sz.textContent = String(r.groups[g].n);
          col.appendChild(wrap); col.appendChild(lab); col.appendChild(sz);
          el.strata.appendChild(col);
        }
        paint();
      }

      function paint() {
        var r = ROUNDS[S.round], A = allocOf(r), g, j, take, on;
        for (g = 0; g < dots.length; g++) {
          on = {};
          if (S.revealed) {
            take = drawFrom(r.groups[g].n, A[g], S.round * 31 + g * 7 + 3);
            for (j = 0; j < take.length; j++) on[take[j]] = 1;
          }
          for (j = 0; j < dots[g].length; j++) {
            dots[g][j].className = 'svw-strat__dot' +
              (S.revealed ? (on[j] ? ' is-in' : ' is-out') : '');
          }
        }
        el.strata.setAttribute('aria-label', S.revealed
          ? 'The population, with ' + listOut(A) + ' scattered picks marked across the ' + r.gwp + '.'
          : popOf(r) + ' ' + r.unit + ' shown as dots, stacked into ' + word(r.groups.length) +
            ' ' + r.gwp + ' of different sizes.');
      }

      /* ---- rounds ---- */

      function newRound() {
        var r = ROUNDS[S.round], N = popOf(r);
        S.pick1 = -1; S.pick2 = -1; S.revealed = false;
        S.o1 = shuffle(allocOptions(r), S.round + 5);
        S.o2 = shuffle(methodOptions(r), S.round + 11);

        el.frame.textContent = r.place + ' has ' + N + ' ' + r.unit + ' ' + r.prep + ' ' +
          word(r.groups.length) + ' ' + r.gwp + '. A stratified sample of ' + r.sample +
          ' is to be taken.';
        el.lab1.textContent = 'How many come from each group';
        el.lab2.textContent = 'How those ' + r.sample + ' are chosen';

        for (k = 0; k < 4; k++) {
          btn1[k].textContent = S.o1[k].label;
          btn2[k].textContent = S.o2[k].label;
          btn1[k].setAttribute('aria-pressed', 'false');
          btn2[k].setAttribute('aria-pressed', 'false');
          btn1[k].disabled = false;
          btn2[k].disabled = false;
        }
        el.opts1.setAttribute('aria-label', 'How many come from each group');
        el.opts2.setAttribute('aria-label', 'How the sample is chosen');

        show(el.step1, true); show(el.opts1, true); show(el.chip1, false); el.chip1.disabled = true;
        show(el.step2, false); show(el.opts2, true); show(el.chip2, false); el.chip2.disabled = true;
        show(el.check, true); el.check.disabled = true;
        show(el.next, false);

        el.note.textContent = 'One dot = one person. The answers below run left to right.';
        el.caption.textContent = 'A stratum is one group within the sample frame. The dots show how big each one is.';
        buildStage();
        runLine();
        state();
      }

      function pick(which, idx) {
        if (S.revealed) return;
        if (which === 1) {
          S.pick1 = idx;
          for (k = 0; k < 4; k++) btn1[k].setAttribute('aria-pressed', k === idx ? 'true' : 'false');
          collapse(1);
          show(el.step2, true);
          if (S.pick2 < 0) btn2[0].focus();
        } else {
          S.pick2 = idx;
          for (k = 0; k < 4; k++) btn2[k].setAttribute('aria-pressed', k === idx ? 'true' : 'false');
          collapse(2);
          el.check.focus();
        }
        el.check.disabled = (S.pick1 < 0 || S.pick2 < 0);
        state();
      }

      function collapse(which) {
        var b = which === 1 ? el.chip1 : el.chip2;
        var opts = which === 1 ? el.opts1 : el.opts2;
        var txt = which === 1 ? S.o1[S.pick1].label : S.o2[S.pick2].chip;
        var lead = which === 1 ? 'Numbers' : 'Method';
        b.textContent = lead + ': ' + txt + '  ·  change';
        b.setAttribute('aria-label', lead + ' — you chose ' + txt + '. Change it.');
        b.disabled = false;
        show(b, true); show(opts, false);
        for (k = 0; k < 4; k++) (which === 1 ? btn1 : btn2)[k].disabled = true;
      }

      function reopen(which) {
        var b = which === 1 ? el.chip1 : el.chip2;
        var opts = which === 1 ? el.opts1 : el.opts2;
        show(b, false); b.disabled = true; show(opts, true);
        for (k = 0; k < 4; k++) (which === 1 ? btn1 : btn2)[k].disabled = false;
        (which === 1 ? btn1 : btn2)[0].focus();
        state();
      }

      /* ---- commit ---- */

      function commit() {
        if (S.revealed || S.pick1 < 0 || S.pick2 < 0) return;
        var r = ROUNDS[S.round], A = allocOf(r), N = popOf(r);
        var a = S.o1[S.pick1], m = S.o2[S.pick2];
        var okA = a.key === 'right', okM = m.key === 'random', ok = okA && okM;

        S.revealed = true;
        S.attempted++;
        S.streak = ok ? S.streak + 1 : 0;
        if (S.streak >= 3) S.mastered = true;

        show(el.step1, false); show(el.step2, false);
        show(el.check, false);
        show(el.next, true);
        el.next.textContent = S.mastered ? 'Another anyway' : 'Next sample';

        var said = 'you said ' + a.label + ', ' + m.echo;
        var msg;

        if (ok) {
          msg = 'Right — ' + a.label + ', drawn with random numbers inside each group. ' +
            'Each group gives the sample the same share it holds of the population. ' +
            shareLine(r, biggest(r)) + '. Splitting ' + r.place + ' into ' + r.gwp +
            ' only organises the sample frame — the ' + r.sample + ' ' + r.unit +
            ' still have to be drawn at random, group by group.';
          if (S.mastered) {
            msg = 'Three in a row — you have it. Stratification is the preparation, not the selection. ' +
              'It divides the population into groups and gives each group the share of the sample it holds of the population. ' +
              'A random method then still has to pick the individuals inside every group. Stop after the first step and nothing has been sampled at all.';
          }
        } else if (okA) {
          msg = 'Not quite — ' + said + '. The numbers are right. ' + methodWhy(r, m);
        } else if (okM) {
          msg = 'Not quite — ' + said + '. The method is right. ' + allocWhy(r, a) +
            ' The split is ' + join(A) + '.';
        } else {
          msg = 'Not quite — ' + said + '. ' + allocWhy(r, a) + ' The split is ' + join(A) +
            '. ' + methodWhy(r, m);
        }

        el.caption.textContent = msg;
        el.note.textContent = 'Sample taken: ' + join(A) + ' — one in ' + word(N / r.sample) +
          ' of every group, drawn at random.';
        paint();
        runLine();
        state();
        el.next.focus();
      }

      function biggest(r) {
        var b = 0, i2;
        for (i2 = 1; i2 < r.groups.length; i2++) if (r.groups[i2].n > r.groups[b].n) b = i2;
        return b;
      }

      function runLine() {
        if (S.mastered) { el.run.textContent = 'You have it'; return; }
        el.run.textContent = S.streak === 0 ? '' :
          S.streak === 1 ? '1 right in a row' : '2 right in a row — one more and you have it';
      }

      function show(node, on) {
        if (on) node.removeAttribute('hidden'); else node.setAttribute('hidden', '');
      }

      function state() {
        var r = ROUNDS[S.round], A = allocOf(r);
        el.sr.textContent = el.caption.textContent + ' ' + (el.strata.getAttribute('aria-label') || '');
        root.dataset.svState = JSON.stringify({
          streak: S.streak, mastered: S.mastered, attempted: S.attempted,
          round: S.round, place: r.place, population: popOf(r), sample: r.sample,
          strata: sizesOf(r), correctSplit: A,
          pickedSplit: S.pick1 < 0 ? null : S.o1[S.pick1].v,
          pickedMethod: S.pick2 < 0 ? null : S.o2[S.pick2].key,
          answered: (S.pick1 >= 0 ? 1 : 0) + (S.pick2 >= 0 ? 1 : 0),
          revealed: S.revealed,
          correct: S.revealed ? (S.o1[S.pick1].key === 'right' && S.o2[S.pick2].key === 'random') : null
        });
      }

      /* layout follows the container, not the viewport */
      var wide = null;
      function layout() {
        var w = root.getBoundingClientRect().width;
        var next = w >= 470;
        if (next !== wide) { wide = next; root.classList.toggle('svw-strat--wide', next); }
      }

      var ro = null;
      if (window.ResizeObserver) {
        ro = new ResizeObserver(function () { layout(); });
        ro.observe(root);
      } else {
        window.addEventListener('resize', layout);
      }

      layout();
      newRound();
      return function () { if (ro) ro.disconnect(); else window.removeEventListener('resize', layout); };
    }
  };

  /* ---------- scoped styles ------------------------------------------ */

  var CSS = [
    '.svw-strat{box-sizing:border-box;background:#fff;border:1px solid #e8e3db;border-radius:16px;',
    'padding:1rem 1rem .85rem;color:#2d2a26;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;',
    'font-size:16px;line-height:1.4;max-width:100%;--dz:7px;--dg:2px;}',
    '.svw-strat *{box-sizing:border-box;}',
    '.svw-strat__kicker{margin:0 0 .15rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;',
    'text-transform:uppercase;color:var(--svw-a);}',
    '.svw-strat__title{margin:0 0 .3rem;font-family:"Source Serif 4",Georgia,serif;font-size:1.22rem;',
    'font-weight:600;line-height:1.18;}',
    '.svw-strat__frame{margin:0 0 .5rem;font-size:.84rem;line-height:1.45;color:#3c3833;}',
    '.svw-strat__stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;',
    'padding:.5rem .5rem .4rem;margin:0 0 .5rem;}',
    '.svw-strat__strata{display:flex;align-items:flex-end;justify-content:center;gap:.75rem;}',
    '.svw-strat__stratum{display:flex;flex-direction:column;align-items:center;}',
    '.svw-strat__dots{display:grid;grid-template-columns:repeat(5,var(--dz));gap:var(--dg);',
    'margin:0 0 .28rem;}',
    '.svw-strat__dot{display:block;width:var(--dz);height:var(--dz);border-radius:50%;',
    'background:#cbc3b6;}',
    '.svw-strat:not(.svw-strat--still) .svw-strat__dot{transition:background-color .18s ease;}',
    '.svw-strat__dot.is-in{background:var(--svw-a);box-shadow:0 0 0 1px #fff;}',
    '.svw-strat__dot.is-out{background:#e6e0d6;}',
    '.svw-strat__glab{margin:0;font-size:.68rem;font-weight:600;line-height:1.2;color:#2d2a26;',
    'white-space:nowrap;}',
    '.svw-strat__gsize{margin:0;font-size:.66rem;line-height:1.25;color:#8d8880;',
    'font-variant-numeric:tabular-nums;}',
    '.svw-strat__note{margin:.35rem 0 0;font-size:.72rem;line-height:1.35;color:#8d8880;',
    'text-align:center;font-variant-numeric:tabular-nums;}',
    '.svw-strat__step{margin:0 0 .32rem;}',
    '.svw-strat__step[hidden]{display:none;}',
    '.svw-strat__lab{margin:0 0 .24rem;font-size:.78rem;font-weight:600;color:#2d2a26;}',
    '.svw-strat__num{display:inline-block;min-width:1.15em;margin-right:.25rem;padding:0 .3em;',
    'border-radius:5px;background:var(--svw-a);color:#fff;font-size:.68rem;text-align:center;}',
    '.svw-strat__opts{display:grid;gap:.3rem;}',
    '.svw-strat__opts[hidden]{display:none;}',
    '.svw-strat__opts--num{grid-template-columns:1fr 1fr;}',
    '.svw-strat__opts--txt{grid-template-columns:1fr;}',
    '.svw-strat__opt,.svw-strat__chip,.svw-strat__primary,.svw-strat__ghost{font-family:inherit;cursor:pointer;}',
    '.svw-strat__opt{padding:.36rem .5rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;',
    'color:#2d2a26;font-size:.8rem;font-weight:600;line-height:1.3;text-align:left;',
    'font-variant-numeric:tabular-nums;}',
    '.svw-strat__opts--num .svw-strat__opt{text-align:center;letter-spacing:.02em;}',
    '.svw-strat__opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
    '.svw-strat__opt:disabled{cursor:default;opacity:1;}',
    '.svw-strat__chip{display:inline-block;max-width:100%;text-align:left;padding:.32rem .55rem;',
    'border:1px dashed #ddd7cd;border-radius:10px;background:#fff;color:#5b564e;font-size:.76rem;',
    'font-weight:600;line-height:1.3;}',
    '.svw-strat__chip:disabled{cursor:default;}',
    '.svw-strat__chip[hidden]{display:none;}',
    '.svw-strat__actions{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;margin:.1rem 0 .4rem;}',
    '.svw-strat__primary{padding:.45rem .95rem;border:1px solid #2d2a26;border-radius:10px;',
    'background:#2d2a26;color:#fff;font-size:.82rem;font-weight:600;}',
    '.svw-strat__primary:disabled{background:#f2eee7;border-color:#e0d9cd;color:#a49d92;cursor:default;}',
    '.svw-strat__primary[hidden],.svw-strat__ghost[hidden]{display:none;}',
    '.svw-strat__ghost{padding:.45rem .95rem;border:1px solid #ddd7cd;border-radius:10px;',
    'background:#faf8f5;color:#2d2a26;font-size:.82rem;font-weight:600;}',
    '.svw-strat__run{font-size:.74rem;color:#8d8880;}',
    '.svw-strat__caption{margin:0;font-size:.84rem;line-height:1.5;color:#3c3833;min-height:3em;}',
    '.svw-strat__sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;',
    'clip:rect(0 0 0 0);white-space:nowrap;border:0;}',
    '.svw-strat__opt:focus-visible,.svw-strat__chip:focus-visible,.svw-strat__primary:focus-visible,',
    '.svw-strat__ghost:focus-visible{outline:2px solid var(--svw-a);outline-offset:2px;}',
    '.svw-strat--wide{padding:1.35rem 1.35rem 1.1rem;--dz:9px;--dg:3px;}',
    '.svw-strat--wide .svw-strat__strata{gap:1.4rem;}',
    '.svw-strat--wide .svw-strat__opts--num{grid-template-columns:repeat(4,1fr);}',
    '.svw-strat--wide .svw-strat__opts--txt{grid-template-columns:1fr 1fr;}',
    '.svw-strat--wide .svw-strat__caption{min-height:2.6em;}'
  ].join('');
})();
