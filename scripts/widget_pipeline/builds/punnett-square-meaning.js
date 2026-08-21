/* StudyVault lesson widget — punnett-square-meaning
   Each cell of a Punnett square is one equally likely fertilisation outcome.
   Self-contained: no imports, no network, no storage, no eval. */
(function () {
  'use strict';

  /* ---------------------------------------------------------------- data */

  var CROSSES = [
    { scen: 'Two tall pea plants, both Tt, are crossed.',
      key: 'T (tall) is dominant to t (dwarf).',
      p1: 'Tt', p2: 'Tt', dom: 'T', rec: 't',
      domPhen: 'tall', recPhen: 'dwarf',
      domAsk: 'is tall', recAsk: 'is dwarf',
      one: 'seedling', many: 'seedlings' },

    { scen: 'A tall pea plant (Tt) is crossed with a dwarf pea plant (tt).',
      key: 'T (tall) is dominant to t (dwarf).',
      p1: 'Tt', p2: 'tt', dom: 'T', rec: 't',
      domPhen: 'tall', recPhen: 'dwarf',
      domAsk: 'is tall', recAsk: 'is dwarf',
      one: 'seedling', many: 'seedlings' },

    { scen: 'Two black mice, both Bb, are bred together.',
      key: 'B (black fur) is dominant to b (white fur).',
      p1: 'Bb', p2: 'Bb', dom: 'B', rec: 'b',
      domPhen: 'black', recPhen: 'white',
      domAsk: 'has black fur', recAsk: 'has white fur',
      one: 'pup', many: 'pups' },

    { scen: 'A black mouse (Bb) is bred with a white mouse (bb).',
      key: 'B (black fur) is dominant to b (white fur).',
      p1: 'Bb', p2: 'bb', dom: 'B', rec: 'b',
      domPhen: 'black', recPhen: 'white',
      domAsk: 'has black fur', recAsk: 'has white fur',
      one: 'pup', many: 'pups' },

    { scen: 'Two parents are each carriers of cystic fibrosis (Ff).',
      key: 'F is dominant; two f alleles cause cystic fibrosis.',
      p1: 'Ff', p2: 'Ff', dom: 'F', rec: 'f',
      domPhen: 'unaffected', recPhen: 'affected',
      domAsk: 'is unaffected', recAsk: 'has cystic fibrosis',
      domTag: 'no CF', recTag: 'has CF',
      one: 'child', many: 'children' },

    { scen: 'Two round-seeded pea plants, both Rr, are crossed.',
      key: 'R (round seed) is dominant to r (wrinkled seed).',
      p1: 'Rr', p2: 'Rr', dom: 'R', rec: 'r',
      domPhen: 'round', recPhen: 'wrinkled',
      domAsk: 'is round', recAsk: 'is wrinkled',
      one: 'seed', many: 'seeds' },

    { scen: 'A black mouse (BB) is bred with a black mouse (Bb).',
      key: 'B (black fur) is dominant to b (white fur).',
      p1: 'BB', p2: 'Bb', dom: 'B', rec: 'b',
      domPhen: 'black', recPhen: 'white',
      domAsk: 'has black fur', recAsk: 'has white fur',
      one: 'pup', many: 'pups' },

    { scen: 'A tall pea plant (TT) is crossed with a dwarf pea plant (tt).',
      key: 'T (tall) is dominant to t (dwarf).',
      p1: 'TT', p2: 'tt', dom: 'T', rec: 't',
      domPhen: 'tall', recPhen: 'dwarf',
      domAsk: 'is tall', recAsk: 'is dwarf',
      one: 'seedling', many: 'seedlings' }
  ];

  var FRACS = ['0', '1/4', '1/2', '3/4', '1'];
  var TYPES = ['fill', 'prob', 'litter'];
  var TRIALS = 200;

  /* ------------------------------------------------------------- helpers */

  function gam(g) { return [g.charAt(0), g.charAt(1)]; }

  function pair(a, b, dom) { return (a === dom) ? a + b : b + a; }

  function isDom(g, dom) { return g.indexOf(dom) >= 0; }

  function shuffle(a) {
    var i, j, t;
    for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1));
      t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function strip(s) { return s.replace(/\.\s*$/, ''); }

  function hex(c) {
    if (typeof c !== 'string') return '';
    c = c.trim();
    if (/^#[0-9a-f]{3}$/i.test(c)) {
      return '#' + c.charAt(1) + c.charAt(1) + c.charAt(2) + c.charAt(2) +
             c.charAt(3) + c.charAt(3);
    }
    return /^#[0-9a-f]{6}$/i.test(c) ? c : '';
  }

  /* --------------------------------------------------------------- mount */

  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = hex(ctx.accent) ||
                 hex(getComputedStyle(root).getPropertyValue('--accent')) ||
                 '#6b7f5e';
    var still = !!ctx.reducedMotion;

    /* ---- styles (every selector scoped to .svw-pun) ---- */
    var css = [
      '.svw-pun{background:#fff;border:1px solid #e8e3db;border-radius:16px;',
      'padding:1.2rem 1.15rem;color:#2d2a26;font-family:Inter,system-ui,',
      '-apple-system,"Segoe UI",sans-serif;font-size:16px;line-height:1.5}',
      '.svw-pun *{box-sizing:border-box;margin:0}',
      '.svw-pun{box-sizing:border-box}',
      '.svw-pun .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;',
      'text-transform:uppercase;color:' + accent + '}',
      '.svw-pun .t{font-family:"Source Serif 4",Georgia,serif;font-weight:600;',
      'font-size:1.22rem;line-height:1.25;margin:.05rem 0 .3rem}',
      '.svw-pun .frame{font-size:.84rem;line-height:1.45;color:#3f3a34;',
      'margin-bottom:.55rem}',
      '.svw-pun .frame b{font-weight:600;color:#2d2a26}',
      '.svw-pun .stage{background:#faf8f5;border:1px solid #efe9e0;',
      'border-radius:12px;padding:.45rem .45rem}',
      '.svw-pun .grid{display:grid;grid-template-columns:.58fr 1fr 1fr;',
      'gap:4px;max-width:282px;margin:0 auto}',
      '.svw-pun .bx{display:flex;align-items:center;justify-content:center;',
      'min-height:36px;border-radius:8px;font-variant-numeric:tabular-nums}',
      '.svw-pun .cor{color:#a8a096;font-size:.95rem}',
      '.svw-pun .gm{background:' + accent + '1f;border:1px solid ' + accent +
      '55;font-weight:700;font-size:1rem}',
      '.svw-pun .cl{background:#fff;border:1px solid #e0d9cd;font-weight:600;',
      'font-size:.98rem}',
      '.svw-pun .cl.tg{border-color:' + accent + ';box-shadow:inset 0 0 0 1px ' +
      accent + '}',
      '.svw-pun .cl.pv{color:#8d8880}',
      '.svw-pun .cl.qm{color:#bcb4a8;font-weight:700}',
      '.svw-pun .cl.ok{border-color:#4f7d63;color:#33604a}',
      '.svw-pun .lit{display:flex;gap:5px;margin-top:.4rem;justify-content:center}',
      '.svw-pun .lit .ch{flex:1 1 0;max-width:70px;background:#fff;',
      'border:1px solid #e0d9cd;border-radius:8px;padding:.15rem .1rem;',
      'text-align:center;font-size:.68rem;line-height:1.25}',
      '.svw-pun .lit .ch b{font-size:.8rem;font-weight:700}',
      '.svw-pun .lit .ch span{color:#5b564e}',
      '.svw-pun .ask{font-size:.86rem;font-weight:600;margin:.4rem 0 .3rem;',
      'line-height:1.35}',
      '.svw-pun .opts{display:flex;flex-wrap:wrap;gap:.35rem}',
      '.svw-pun .opts.col{flex-direction:column}',
      '.svw-pun .o{font:600 .82rem Inter,system-ui,sans-serif;color:#2d2a26;',
      'background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;',
      'padding:.45rem .9rem;cursor:pointer;text-align:left;line-height:1.35}',
      '.svw-pun .opts.col .o{width:100%}',
      '.svw-pun .o:focus-visible{outline:2px solid ' + accent + ';outline-offset:2px}',
      '.svw-pun .o.sel{background:#2d2a26;border-color:#2d2a26;color:#fff}',
      '.svw-pun .o.right{border-color:#4f7d63;color:#33604a}',
      '.svw-pun .o.sel.right{background:#4f7d63;border-color:#4f7d63;color:#fff}',
      '.svw-pun .o[disabled]{cursor:default;opacity:1}',
      '.svw-pun .bar{display:flex;align-items:center;gap:.6rem;margin-top:.5rem}',
      '.svw-pun .go{font:600 .82rem Inter,system-ui,sans-serif;background:#2d2a26;',
      'color:#fff;border:1px solid #2d2a26;border-radius:10px;',
      'padding:.45rem 1.05rem;cursor:pointer}',
      '.svw-pun .go:focus-visible{outline:2px solid ' + accent + ';outline-offset:2px}',
      '.svw-pun .run{font-size:.76rem;color:#8d8880;font-variant-numeric:tabular-nums}',
      '.svw-pun .cap{font-size:.82rem;line-height:1.5;color:#3f3a34;',
      'margin-top:.5rem}',
      '.svw-pun .cap.live{min-height:4.6em}',
      '.svw-pun .cap b{font-weight:600;color:#2d2a26}',
      '.svw-pun .sr{position:absolute;width:1px;height:1px;overflow:hidden;',
      'clip:rect(0 0 0 0);white-space:nowrap}'
    ].join('');
    if (still) {
      css += '.svw-pun *{transition:none!important;animation:none!important}';
    }

    root.className = (root.className ? root.className + ' ' : '') + 'svw-pun';

    var st = document.createElement('style');
    st.textContent = css;
    root.appendChild(st);

    /* ---- skeleton, built once ---- */
    function el(tag, cls, txt) {
      var n = document.createElement(tag);
      if (cls) n.className = cls;
      if (txt != null) n.textContent = txt;
      return n;
    }

    root.appendChild(el('div', 'k', 'Genetic crosses'));
    root.appendChild(el('h3', 't', 'Reading a Punnett square'));

    var frame = el('p', 'frame');
    root.appendChild(frame);

    var stage = el('div', 'stage');
    var grid = el('div', 'grid');
    var boxes = {};
    boxes.corner = el('div', 'bx cor', '×');
    grid.appendChild(boxes.corner);
    boxes.top = [el('div', 'bx gm'), el('div', 'bx gm')];
    grid.appendChild(boxes.top[0]);
    grid.appendChild(boxes.top[1]);
    boxes.side = [el('div', 'bx gm'), el('div', 'bx gm')];
    boxes.cell = [[el('div', 'bx cl'), el('div', 'bx cl')],
                  [el('div', 'bx cl'), el('div', 'bx cl')]];
    grid.appendChild(boxes.side[0]);
    grid.appendChild(boxes.cell[0][0]);
    grid.appendChild(boxes.cell[0][1]);
    grid.appendChild(boxes.side[1]);
    grid.appendChild(boxes.cell[1][0]);
    grid.appendChild(boxes.cell[1][1]);
    stage.appendChild(grid);

    var litter = el('div', 'lit');
    litter.style.display = 'none';
    var chips = [];
    for (var ci = 0; ci < 4; ci++) {
      var ch = el('div', 'ch');
      ch.appendChild(el('b'));
      ch.appendChild(el('span'));
      chips.push(ch);
      litter.appendChild(ch);
    }
    stage.appendChild(litter);
    root.appendChild(stage);

    var ask = el('p', 'ask');
    root.appendChild(ask);

    var opts = el('div', 'opts');
    var optBtns = [];
    for (var oi = 0; oi < 5; oi++) {
      var b = el('button', 'o');
      b.type = 'button';
      b.style.display = 'none';
      (function (idx) {
        b.addEventListener('click', function () { choose(idx); });
      })(oi);
      optBtns.push(b);
      opts.appendChild(b);
    }
    root.appendChild(opts);

    var bar = el('div', 'bar');
    var go = el('button', 'go', 'Check');
    go.type = 'button';
    var run = el('span', 'run', '');
    bar.appendChild(go);
    bar.appendChild(run);
    root.appendChild(bar);

    var cap = el('p', 'cap');
    root.appendChild(cap);

    var sr = el('p', 'sr');
    sr.setAttribute('aria-live', 'polite');
    root.appendChild(sr);

    /* ---- state ---- */
    var S = { streak: 0, mastered: false, attempted: 0, round: 0,
              picked: -1, phase: 'ask' };
    var deck = [];
    var q = null;

    function drawCross(needSplit) {
      var i, tries;
      for (tries = 0; tries < 3; tries++) {
        for (i = 0; i < deck.length; i++) {
          if (!needSplit || deck[i].mixed) return deck.splice(i, 1)[0];
        }
        deck = shuffle(CROSSES.map(function (c) {
          var m = model(c);
          return { c: c, m: m, mixed: m.domCount > 0 && m.domCount < 4 };
        }));
      }
      return deck.splice(0, 1)[0];
    }

    function model(c) {
      var top = gam(c.p1), side = gam(c.p2), cells = [], r, cc, n = 0;
      for (r = 0; r < 2; r++) {
        cells.push([]);
        for (cc = 0; cc < 2; cc++) {
          var g = pair(top[cc], side[r], c.dom);
          cells[r].push(g);
          if (isDom(g, c.dom)) n++;
        }
      }
      return { top: top, side: side, cells: cells, domCount: n };
    }

    /* ---- question builders ---- */

    function buildFill(c, m) {
      var r = Math.floor(Math.random() * 2), cc = Math.floor(Math.random() * 2);
      var right = m.cells[r][cc];
      var labels = shuffle([c.dom + c.dom, c.dom + c.rec, c.rec + c.rec]);
      return {
        type: 'fill', c: c, m: m, r: r, cc: cc,
        ask: 'Which pair of alleles belongs in the highlighted cell?',
        labels: labels, correct: labels.indexOf(right), right: right,
        column: false
      };
    }

    function buildProb(c, m) {
      var v = Math.floor(Math.random() * 5);
      var het = c.dom + c.rec, hd = c.dom + c.dom, hr = c.rec + c.rec;
      var n = 0, text = '', desc = '', geno = null, r, cc;
      function count(fn) {
        var k = 0;
        for (r = 0; r < 2; r++) for (cc = 0; cc < 2; cc++) if (fn(m.cells[r][cc])) k++;
        return k;
      }
      if (v === 0) {
        n = m.domCount;
        text = 'What is the probability that any one ' + c.one + ' ' + c.domAsk + '?';
        desc = 'carry at least one ' + c.dom;
      } else if (v === 1) {
        n = 4 - m.domCount;
        text = 'What is the probability that any one ' + c.one + ' ' + c.recAsk + '?';
        desc = 'are ' + hr;
      } else if (v === 2) {
        geno = het; n = count(function (g) { return g === het; });
        text = 'What is the probability that any one ' + c.one +
               ' is heterozygous (' + het + ')?';
        desc = 'are ' + het;
      } else if (v === 3) {
        geno = hr; n = count(function (g) { return g === hr; });
        text = 'What is the probability that any one ' + c.one +
               ' has the genotype ' + hr + '?';
        desc = 'are ' + hr;
      } else {
        geno = hd; n = count(function (g) { return g === hd; });
        text = 'What is the probability that any one ' + c.one +
               ' has the genotype ' + hd + '?';
        desc = 'are ' + hd;
      }
      return {
        type: 'prob', c: c, m: m, ask: text, labels: FRACS.slice(),
        correct: n, n: n, desc: desc, geno: geno, column: false
      };
    }

    function buildLitter(c, m) {
      var e = m.domCount, o = 4 - e;
      var right = 'Any split from 0 to 4 ' + c.domPhen + '; ' + e +
                  ' is likeliest.';
      var labels = shuffle([
        'Exactly ' + e + ' ' + c.domPhen + ', ' + o + ' ' + c.recPhen +
          ' — guaranteed.',
        right,
        'Once ' + e + ' are ' + c.domPhen + ', the rest must be ' + c.recPhen + '.'
      ]);
      return {
        type: 'litter', c: c, m: m, e: e,
        ask: 'Four ' + c.many + ' grow from this cross. Which is true?',
        labels: labels, correct: labels.indexOf(right), column: true
      };
    }

    /* ---- rendering ---- */

    function newRound() {
      var type = TYPES[S.round % 3];
      var d = drawCross(type === 'litter');
      var c = d.c, m = d.m;
      q = type === 'fill' ? buildFill(c, m)
        : type === 'prob' ? buildProb(c, m)
        : buildLitter(c, m);
      S.picked = -1;
      S.phase = 'ask';
      paintFrame();
      paintGrid();
      litter.style.display = 'none';
      ask.textContent = q.ask;
      paintOpts();
      go.textContent = 'Check';
      cap.textContent = '';
      writeState();
    }

    function paintFrame() {
      var c = q.c;
      frame.innerHTML = '';
      var b = document.createElement('b');
      b.textContent = c.scen + ' ';
      frame.appendChild(b);
      frame.appendChild(document.createTextNode(
        c.key + ' Gametes head the top row and the left column.'));
    }

    function paintGrid() {
      var m = q.m, r, cc;
      boxes.top[0].textContent = m.top[0];
      boxes.top[1].textContent = m.top[1];
      boxes.side[0].textContent = m.side[0];
      boxes.side[1].textContent = m.side[1];
      for (r = 0; r < 2; r++) {
        for (cc = 0; cc < 2; cc++) {
          var box = boxes.cell[r][cc];
          box.className = 'bx cl';
          if (q.type === 'fill' && r === q.r && cc === q.cc) {
            box.className = 'bx cl tg qm';
            box.textContent = '?';
          } else {
            box.textContent = m.cells[r][cc];
          }
        }
      }
    }

    function paintOpts() {
      var i;
      opts.className = q.column ? 'opts col' : 'opts';
      for (i = 0; i < optBtns.length; i++) {
        if (i < q.labels.length) {
          optBtns[i].textContent = q.labels[i];
          optBtns[i].style.display = '';
          optBtns[i].disabled = false;
          optBtns[i].className = 'o';
          optBtns[i].setAttribute('aria-pressed', 'false');
        } else {
          optBtns[i].style.display = 'none';
          optBtns[i].disabled = true;
        }
      }
    }

    function choose(i) {
      if (S.phase !== 'ask' || i >= q.labels.length) return;
      S.picked = i;
      for (var k = 0; k < q.labels.length; k++) {
        optBtns[k].className = (k === i) ? 'o sel' : 'o';
        optBtns[k].setAttribute('aria-pressed', k === i ? 'true' : 'false');
      }
      if (q.type === 'fill') {
        var box = boxes.cell[q.r][q.cc];
        box.className = 'bx cl tg pv';
        box.textContent = q.labels[i];
      }
      say('Selected ' + q.labels[i] + '. Press Check.');
      writeState();
    }

    function say(msg) { sr.textContent = msg; }

    function setCap(html) {
      cap.innerHTML = html;
      say(cap.textContent);
    }

    /* ---- simulation (real random draws) ---- */

    function sampleOne(c, m) {
      var a = m.top[Math.floor(Math.random() * 2)];
      var b = m.side[Math.floor(Math.random() * 2)];
      return pair(a, b, c.dom);
    }

    function sampleFour(c, m) {
      var out = [], i;
      for (i = 0; i < 4; i++) out.push(sampleOne(c, m));
      return out;
    }

    function matchRate(c, m, e) {
      var hits = 0, t, i, d;
      for (t = 0; t < TRIALS; t++) {
        d = 0;
        for (i = 0; i < 4; i++) if (isDom(sampleOne(c, m), c.dom)) d++;
        if (d === e) hits++;
      }
      return hits;
    }

    /* ---- commit ---- */

    go.addEventListener('click', function () {
      if (S.phase === 'done') { S.round++; newRound(); go.focus(); return; }
      if (S.picked < 0) {
        setCap('Choose one of the answers above, then press <b>Check</b>.');
        return;
      }
      commit();
    });

    function commit() {
      var right = (S.picked === q.correct);
      S.attempted++;
      S.streak = right ? S.streak + 1 : 0;
      var justMastered = false;
      if (right && S.streak >= 3 && !S.mastered) { S.mastered = true; justMastered = true; }
      S.phase = 'done';

      var i;
      for (i = 0; i < q.labels.length; i++) {
        optBtns[i].disabled = true;
        optBtns[i].className = 'o' + (i === S.picked ? ' sel' : '') +
                               (i === q.correct ? ' right' : '');
      }
      if (q.type === 'fill') {
        var box = boxes.cell[q.r][q.cc];
        box.className = 'bx cl tg' + (right ? ' ok' : '');
        box.textContent = q.right;
      }

      cap.className = 'cap live';
      setCap(feedback(right, justMastered));
      run.textContent = S.streak > 0 ? S.streak + ' in a row' : '';
      go.textContent = S.mastered ? 'Another anyway' : 'Next cross';
      writeState();
    }

    /* ---- feedback ---- */

    function verdict(ok) { return ok ? '<b>Right — </b>' : '<b>Not quite — </b>'; }

    function masteryLine() {
      return ' <b>Three in a row — you have it:</b> the ratio is the chance at ' +
             'every fertilisation, not a quota.';
    }

    function feedback(ok, mastered) {
      var c = q.c, m = q.m, s = '', close = '';
      if (q.type === 'fill') {
        var mine = q.labels[S.picked];
        var top = m.top[q.cc], side = m.side[q.r];
        if (ok) {
          s = verdict(true) + mine + '. The top gamete <b>' + top +
              '</b> meets the side gamete <b>' + side + '</b>.';
          close = ' That cell is one fertilisation: one allele from each parent.';
        } else {
          var why;
          if (top !== side && mine === pair(top, top, c.dom)) {
            why = 'that uses the top gamete ' + top + ' twice and ignores the side parent. ';
          } else if (top !== side && mine === pair(side, side, c.dom)) {
            why = 'that uses the side gamete ' + side + ' twice and ignores the top parent. ';
          } else {
            var have = [top, side], miss = '', z, w;
            for (z = 0; z < 2; z++) {
              w = have.indexOf(mine.charAt(z));
              if (w >= 0) have.splice(w, 1); else miss = mine.charAt(z);
            }
            why = 'that needs a ' + miss + ', but this cell is fed by ' + top +
                  ' and ' + side + '. ';
          }
          s = verdict(false) + 'you said <b>' + mine + '</b> — ' + why +
              'The top gamete ' + top + ' meets the side gamete ' + side +
              ', so the cell is <b>' + q.right + '</b>.';
        }
      } else if (q.type === 'prob') {
        var mineF = q.labels[S.picked], rightF = FRACS[q.n];
        if (q.n === 0) {
          close = ' No cell can give it, so it never happens from this cross.';
        } else if (q.n === 4) {
          close = ' Every cell gives it, so it happens at every fertilisation.';
        } else if (q.geno) {
          close = ' Count genotypes here, not appearance: cells that look ' +
                  c.domPhen + ' are not all ' + q.geno + '.';
        } else {
          close = ' Each ' + c.one + ' has that chance every time — earlier ' +
                  c.many + ' change nothing.';
        }
        if (ok) {
          s = verdict(true) + mineF + '. ' + q.n + ' of the 4 cells ' + q.desc +
              ', and the four cells are equally likely, so the chance is ' +
              rightF + '.';
        } else {
          s = verdict(false) + 'you said <b>' + mineF + '</b>. Count the cells: ' +
              q.n + ' of the 4 ' + q.desc + ', so the probability is <b>' + rightF +
              '</b>.';
        }
      } else {
        var four = sampleFour(c, m), d = 0, i;
        for (i = 0; i < 4; i++) if (isDom(four[i], c.dom)) d++;
        showLitter(four);
        var hits = matchRate(c, m, q.e);
        var pct = Math.round(hits / TRIALS * 100);
        var real = d + ' ' + c.domPhen + ', ' + (4 - d) + ' ' + c.recPhen;
        var sim = 'In ' + TRIALS + ' sets of four, exactly ' + q.e + ':' +
                  (4 - q.e) + ' came up ' + hits + ' times (' + pct + '%).';
        var matched = (d === q.e);
        if (ok) {
          s = verdict(true) + 'any split can happen. ' + (matched
            ? 'These four did come out <b>' + real + '</b> — the likeliest ' +
              'single result, but only ' + hits + ' sets in ' + TRIALS + ' did that.'
            : 'These four: <b>' + real + '</b>. ' + sim);
          close = ' The ratio is the chance each time, not a quota.';
        } else {
          s = verdict(false) + 'you said ‘' + strip(q.labels[S.picked]) + '’. ' +
              (matched
                ? 'These four did come out <b>' + real + '</b> — but that is luck, ' +
                  'not a rule: only ' + hits + ' of ' + TRIALS + ' sets of four did.'
                : 'These four: <b>' + real + '</b>. ' + sim);
          close = ' Each fertilisation is a fresh ' + q.e + ' in 4 chance.';
        }
      }
      if (mastered) return s + masteryLine();
      s += close;
      if (ok && S.streak === 2) {
        s += ' <b>2 in a row</b> — one more and you have it.';
      }
      return s;
    }

    function showLitter(four) {
      var c = q.c, i;
      for (i = 0; i < 4; i++) {
        chips[i].firstChild.textContent = four[i];
        chips[i].lastChild.textContent = ' ' + (isDom(four[i], c.dom) ?
          (c.domTag || c.domPhen) : (c.recTag || c.recPhen));
      }
      litter.style.display = '';
    }

    /* ---- state out ---- */

    function writeState() {
      root.dataset.svState = JSON.stringify({
        streak: S.streak,
        mastered: S.mastered,
        attempted: S.attempted,
        round: S.round,
        type: q ? q.type : null,
        selected: S.picked >= 0 && q ? q.labels[S.picked] : null,
        phase: S.phase
      });
    }

    deck = [];
    newRound();
  }

  window.SVWidget = {
    meta: {
      id: 'punnett-square-meaning',
      title: 'Reading a Punnett square',
      teaches: 'Each cell is one equally likely pairing of one gamete from each parent, so the ratio is a probability at every fertilisation, not a prediction of four actual offspring.'
    },
    mount: mount
  };
})();
