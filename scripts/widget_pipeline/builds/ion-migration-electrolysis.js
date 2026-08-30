/* ============================================================
   ion-migration-electrolysis

   Makes concrete: in electrolysis the IONS THEMSELVES travel.
   Positive ions (cations) are attracted across the liquid to the
   negative electrode (cathode) and GAIN electrons; negative ions
   (anions) travel to the positive electrode (anode) and LOSE them.

   Misconceptions it must let a student commit to, every round:
     - "the current just passes through, nothing moves"  -> "Stays put"
     - "ions go to the electrode with their own charge"   -> wrong rod
     - "anode/cathode are the other way round"            -> step 2

   Molten electrolytes only: the metal forms at the cathode and the
   non-metal at the anode, with no aqueous discharge rules to muddy
   the one idea being taught.
   ============================================================ */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';

  /* Ion counts follow the formula unit, so the picture never implies a
     ratio the chemistry does not have (PbBr2 is 1 : 2, not 1 : 1). */
  var ROUNDS = [
    { id: 'pbbr2', name: 'Molten lead(II) bromide',
      cat: { sym: 'Pb²⁺', n: 1 }, an: { sym: 'Br⁻', n: 2 },
      metal: 'lead', nonmetal: 'bromine' },
    { id: 'zncl2', name: 'Molten zinc chloride',
      cat: { sym: 'Zn²⁺', n: 1 }, an: { sym: 'Cl⁻', n: 2 },
      metal: 'zinc', nonmetal: 'chlorine' },
    { id: 'nacl', name: 'Molten sodium chloride',
      cat: { sym: 'Na⁺', n: 2 }, an: { sym: 'Cl⁻', n: 2 },
      metal: 'sodium', nonmetal: 'chlorine' },
    { id: 'mgcl2', name: 'Molten magnesium chloride',
      cat: { sym: 'Mg²⁺', n: 1 }, an: { sym: 'Cl⁻', n: 2 },
      metal: 'magnesium', nonmetal: 'chlorine' },
    { id: 'kbr', name: 'Molten potassium bromide',
      cat: { sym: 'K⁺', n: 2 }, an: { sym: 'Br⁻', n: 2 },
      metal: 'potassium', nonmetal: 'bromine' }
  ];

  var MDASH = '—';
  var DOT = '·';

  var CSS = [
    '.svw-ionmig{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;position:relative}',
    '.svw-ionmig *{box-sizing:border-box}',
    '.svw-ionmig .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--ia)}',
    '.svw-ionmig .ttl{font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;font-weight:600;margin:.1rem 0 .28rem;line-height:1.2}',
    '.svw-ionmig .frame{font-size:.85rem;line-height:1.45;margin:0 0 .55rem;color:#3c3833}',
    '.svw-ionmig .cell{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.35rem;margin-bottom:.45rem}',
    '.svw-ionmig svg{display:block;width:100%;height:128px}',
    '.svw-ionmig .lbl{font-size:.7rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#8d8880;margin:0 0 .3rem}',
    '.svw-ionmig .row{display:grid;grid-template-columns:3.3rem 1fr 1fr 1fr;gap:.3rem;align-items:center;margin-bottom:.3rem}',
    '.svw-ionmig .ion{font-size:.86rem;font-weight:700;font-variant-numeric:tabular-nums}',
    '.svw-ionmig .b{font-size:.76rem;font-weight:600;line-height:1.15;padding:.4rem .3rem;border-radius:9px;',
    'border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;font-family:inherit;text-align:center}',
    '.svw-ionmig .b[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-ionmig .b:disabled{cursor:default}',
    '.svw-ionmig .step2{margin-top:.5rem}',
    '.svw-ionmig .asleep{opacity:.4}',
    '.svw-ionmig .cta{display:flex;align-items:center;gap:.6rem;margin-top:.45rem}',
    '.svw-ionmig .go{font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;',
    'background:#2d2a26;color:#fff;cursor:pointer;font-family:inherit;flex:0 0 auto}',
    '.svw-ionmig .go:disabled{background:#efe9e0;border-color:#e4ddd2;color:#a39d94;cursor:default}',
    '.svw-ionmig .run{flex:1 1 auto;font-size:.76rem;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svw-ionmig .cap{font-size:.84rem;line-height:1.5;color:#3c3833;margin:.6rem 0 0;min-height:3.6rem}',
    '.svw-ionmig .cap strong{font-weight:700;color:#2d2a26}',
    '.svw-ionmig .sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;',
    'clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}'
  ].join('');

  /* Geometry, in viewBox units. The viewBox is deliberately short and wide:
     with a fixed CSS height the scale is set by whichever axis binds first,
     and a tall viewBox drove the ion labels down to about 8px on a phone.
     This shape keeps every label at .66rem or above, down to 360px. */
  var LEFT_X = 58, RIGHT_X = 222;
  var HOME_Y = { cat: 64, an: 85 };
  var DOCK = { left: 83, right: 197 };
  var CAP_W = 30, CAP_H = 17;

  function el(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) { if (attrs.hasOwnProperty(k)) n.setAttribute(k, attrs[k]); }
    return n;
  }

  function mount(root, ctx) {
    var accent = (ctx && ctx.accent) ||
      (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
    var reduced = !!(ctx && ctx.reducedMotion);

    var wrap = document.createElement('div');
    wrap.className = 'svw-ionmig';
    wrap.style.setProperty('--ia', accent);
    var style = document.createElement('style');
    style.textContent = CSS;
    wrap.appendChild(style);

    var st = {
      i: Math.floor(Math.random() * ROUNDS.length),
      R: null, negSide: 'left', asked: 'anode',
      pick: { cat: null, an: null, prod: null },
      revealed: false, correct: null,
      streak: 0, mastered: false, attempted: 0
    };

    /* ---------- shell ---------- */
    var head = document.createElement('div');
    head.innerHTML = '<div class="k">Electrolysis</div><div class="ttl">Where do the ions go?</div>';
    var frame = document.createElement('p');
    frame.className = 'frame';
    head.appendChild(frame);
    wrap.appendChild(head);

    var cellBox = document.createElement('div');
    cellBox.className = 'cell';
    var svg = el('svg', { viewBox: '0 0 280 112', 'aria-hidden': 'true',
      preserveAspectRatio: 'xMidYMid meet' });
    cellBox.appendChild(svg);
    wrap.appendChild(cellBox);

    /* beaker + liquid */
    svg.appendChild(el('path', { d: 'M24,55 L256,55 L256,87 Q256,95 248,95 L32,95 Q24,95 24,87 Z',
      fill: accent + '1c' }));
    svg.appendChild(el('path', { d: 'M22,46 L22,88 Q22,96 31,96 L249,96 Q258,96 258,88 L258,46',
      fill: 'none', stroke: '#cfc7ba', 'stroke-width': '1.6', 'stroke-linecap': 'round' }));
    svg.appendChild(el('line', { x1: 24, y1: 55, x2: 256, y2: 55,
      stroke: accent + '55', 'stroke-width': '1.2' }));

    /* d.c. supply + wires */
    svg.appendChild(el('rect', { x: 106, y: 0, width: 68, height: 16, rx: 4.5,
      fill: '#fff', stroke: '#d8d1c5', 'stroke-width': '1.2' }));
    var supplyTxt = el('text', { x: 140, y: 11.4, 'text-anchor': 'middle',
      'font-size': '9.5', fill: '#8d8880', 'font-family': 'Inter,sans-serif' });
    supplyTxt.textContent = 'd.c. supply';
    svg.appendChild(supplyTxt);
    svg.appendChild(el('polyline', { points: '106,8 58,8 58,15', fill: 'none',
      stroke: '#c3bbae', 'stroke-width': '1.8' }));
    svg.appendChild(el('polyline', { points: '174,8 222,8 222,15', fill: 'none',
      stroke: '#c3bbae', 'stroke-width': '1.8' }));

    /* rods */
    svg.appendChild(el('rect', { x: 52, y: 32, width: 12, height: 51, rx: 2,
      fill: '#d5cec2', stroke: '#b6ada0', 'stroke-width': '1' }));
    svg.appendChild(el('rect', { x: 216, y: 32, width: 12, height: 51, rx: 2,
      fill: '#d5cec2', stroke: '#b6ada0', 'stroke-width': '1' }));

    /* terminal sign badges */
    function badge(cx) {
      var g = el('g', {});
      g.appendChild(el('circle', { cx: cx, cy: 23.5, r: 8.6, fill: '#fff',
        stroke: '#b6ada0', 'stroke-width': '1.2' }));
      var t = el('text', { x: cx, y: 23.5, 'text-anchor': 'middle', dy: '.36em',
        'font-size': '14', 'font-weight': '700', fill: '#2d2a26',
        'font-family': 'Inter,sans-serif' });
      g.appendChild(t);
      svg.appendChild(g);
      return t;
    }
    var signL = badge(LEFT_X), signR = badge(RIGHT_X);

    /* names + products, filled in only after the reveal */
    function label(x, y, anchor, size, weight, fill) {
      var t = el('text', { x: x, y: y, 'text-anchor': anchor, 'font-size': size,
        'font-weight': weight, fill: fill, 'font-family': 'Inter,sans-serif' });
      svg.appendChild(t);
      return t;
    }
    var nameL = label(70, 45, 'start', '9.6', '600', '#8d8880');
    var nameR = label(210, 45, 'end', '9.6', '600', '#8d8880');
    var prodL = label(LEFT_X, 108, 'middle', '10.4', '700', '#2d2a26');
    var prodR = label(RIGHT_X, 108, 'middle', '10.4', '700', '#2d2a26');

    var ionLayer = el('g', {});
    svg.appendChild(ionLayer);

    /* ---------- controls ---------- */
    var ctl = document.createElement('div');
    var lbl1 = document.createElement('div');
    lbl1.className = 'lbl';
    lbl1.textContent = '1 ' + DOT + ' Where does each ion end up?';
    ctl.appendChild(lbl1);

    var DESTS = [{ v: 'left', t: 'Left rod' }, { v: 'right', t: 'Right rod' },
                 { v: 'none', t: 'Stays put' }];
    var ionBtn = { cat: [], an: [] };
    var ionName = {};

    ['cat', 'an'].forEach(function (which) {
      var row = document.createElement('div');
      row.className = 'row';
      var nm = document.createElement('span');
      nm.className = 'ion';
      row.appendChild(nm);
      ionName[which] = nm;
      DESTS.forEach(function (d) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'b';
        b.textContent = d.t;
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', function () { choose(which, d.v, b); });
        row.appendChild(b);
        ionBtn[which].push({ b: b, v: d.v });
      });
      ctl.appendChild(row);
    });

    var step2 = document.createElement('div');
    step2.className = 'step2 asleep';
    var lbl2 = document.createElement('div');
    lbl2.className = 'lbl';
    step2.appendChild(lbl2);
    var prodRow = document.createElement('div');
    prodRow.className = 'row';
    prodRow.style.gridTemplateColumns = '1fr 1fr 1fr';
    var prodBtn = [];
    for (var p = 0; p < 3; p++) {
      var pb = document.createElement('button');
      pb.type = 'button';
      pb.className = 'b';
      pb.disabled = true;
      pb.setAttribute('aria-pressed', 'false');
      (function (btn) {
        btn.addEventListener('click', function () { choose('prod', btn.dataset.v, btn); });
      })(pb);
      prodRow.appendChild(pb);
      prodBtn.push(pb);
    }
    step2.appendChild(prodRow);
    ctl.appendChild(step2);

    var cta = document.createElement('div');
    cta.className = 'cta';
    var go = document.createElement('button');
    go.type = 'button';
    go.className = 'go';
    go.textContent = 'Check';
    go.disabled = true;
    var run = document.createElement('span');
    run.className = 'run';
    cta.appendChild(go);
    cta.appendChild(run);
    ctl.appendChild(cta);
    wrap.appendChild(ctl);

    var cap = document.createElement('p');
    cap.className = 'cap';
    wrap.appendChild(cap);

    var sr = document.createElement('p');
    sr.className = 'sr';
    sr.setAttribute('aria-live', 'polite');
    wrap.appendChild(sr);

    root.appendChild(wrap);

    /* ---------- model ---------- */
    function trueSide(which) {
      var other = st.negSide === 'left' ? 'right' : 'left';
      return which === 'cat' ? st.negSide : other;
    }
    function rodWord(side) { return side === 'left' ? 'the left rod' : 'the right rod'; }
    function signWord(side) { return side === st.negSide ? 'negative' : 'positive'; }
    function sideOfName(name) {
      var other = st.negSide === 'left' ? 'right' : 'left';
      return name === 'cathode' ? st.negSide : other;
    }
    function trueProdKey() { return st.asked === 'anode' ? 'nonmetal' : 'metal'; }
    function prodWord(key) {
      if (key === 'metal') return st.R.metal;
      if (key === 'nonmetal') return st.R.nonmetal;
      return 'nothing';
    }

    function pushState() {
      root.dataset.svState = JSON.stringify({
        electrolyte: st.R.id, negSide: st.negSide, asked: st.asked,
        cation: st.pick.cat, anion: st.pick.an, product: st.pick.prod,
        correct: st.correct, streak: st.streak,
        mastered: st.mastered, attempted: st.attempted
      });
    }

    /* ---------- drawing ---------- */
    function dockXY(which, index, side) {
      if (side === 'none') return homeXY(which, index);
      var base = DOCK[side];
      var step = side === 'left' ? 32 : -32;
      return { x: base + index * step, y: HOME_Y[which] };
    }
    function homeXY(which, index) {
      var n = st.R[which].n;
      var startX = 140 - (n - 1) * 17;
      return { x: startX + index * 34, y: HOME_Y[which] };
    }

    var ionNodes = { cat: [], an: [] };

    function buildIons() {
      while (ionLayer.firstChild) ionLayer.removeChild(ionLayer.firstChild);
      ionNodes = { cat: [], an: [] };
      ['cat', 'an'].forEach(function (which) {
        var spec = st.R[which];
        for (var i = 0; i < spec.n; i++) {
          var g = el('g', {});
          var c = el('rect', { x: -CAP_W / 2, y: -CAP_H / 2, width: CAP_W, height: CAP_H,
            rx: CAP_H / 2,
            fill: which === 'cat' ? accent + '2b' : '#ece7de',
            stroke: which === 'cat' ? accent : '#b0a89a', 'stroke-width': '1.2' });
          var t = el('text', { x: 0, y: 0, dy: '.34em', 'text-anchor': 'middle',
            'font-size': '9.6', 'font-weight': '700', fill: '#2d2a26',
            'font-family': 'Inter,sans-serif' });
          t.textContent = spec.sym;
          g.appendChild(c);
          g.appendChild(t);
          g.style.transition = reduced ? 'none' : 'transform .6s cubic-bezier(.16,1,.3,1)';
          var pos = homeXY(which, i);
          g.style.transform = 'translate(' + pos.x + 'px,' + pos.y + 'px)';
          ionLayer.appendChild(g);
          ionNodes[which].push(g);
        }
      });
    }

    function moveIons(which, side) {
      ionNodes[which].forEach(function (g, i) {
        var pos = dockXY(which, i, side);
        g.style.transform = 'translate(' + pos.x + 'px,' + pos.y + 'px)';
      });
    }

    /* ---------- interaction ---------- */
    function choose(which, value, btn) {
      if (st.revealed) return;
      st.pick[which] = value;
      var list = which === 'prod' ? prodBtn : ionBtn[which].map(function (o) { return o.b; });
      list.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
      if (which !== 'prod') moveIons(which, value);

      var placed = st.pick.cat && st.pick.an;
      if (placed) {
        step2.classList.remove('asleep');
        prodBtn.forEach(function (b) { b.disabled = false; });
      }
      go.disabled = !(placed && st.pick.prod);
      pushState();
    }

    function commit() {
      if (st.revealed) { nextRound(); return; }
      if (go.disabled) return;

      var catTrue = trueSide('cat'), anTrue = trueSide('an');
      var ok = st.pick.cat === catTrue && st.pick.an === anTrue &&
               st.pick.prod === trueProdKey();

      st.revealed = true;
      st.attempted++;
      st.correct = ok;
      st.streak = ok ? st.streak + 1 : 0;
      if (ok && st.streak >= 3) st.mastered = true;

      /* the real cell, derived from the charges - never hand-placed */
      moveIons('cat', catTrue);
      moveIons('an', anTrue);
      nameL.textContent = st.negSide === 'left' ? 'cathode' : 'anode';
      nameR.textContent = st.negSide === 'left' ? 'anode' : 'cathode';
      prodL.textContent = st.negSide === 'left' ? st.R.metal : st.R.nonmetal;
      prodR.textContent = st.negSide === 'left' ? st.R.nonmetal : st.R.metal;

      ionBtn.cat.concat(ionBtn.an).forEach(function (o) { o.b.disabled = true; });
      prodBtn.forEach(function (b) { b.disabled = true; });
      go.textContent = st.mastered ? 'Another anyway' : 'Next question';
      go.disabled = false;
      run.textContent = st.mastered ? 'Mastered.'
        : (st.streak === 0 ? '' : st.streak + ' right in a row ' + MDASH +
           ' ' + (3 - st.streak) + ' to go.');

      cap.innerHTML = verdict(ok, catTrue, anTrue);
      sr.textContent = cap.textContent;
      pushState();
    }

    function verdict(ok, catTrue, anTrue) {
      var R = st.R, C = R.cat.sym, A = R.an.sym;
      var lead = ok ? '<strong>Right ' + MDASH + '</strong> ' : '<strong>Not quite ' + MDASH + '</strong> ';

      if (ok) {
        var echo = C + ' to ' + rodWord(catTrue) + ' (' + signWord(catTrue) + '), ' +
          A + ' to the ' + (anTrue === 'left' ? 'left' : 'right') + ' (' +
          signWord(anTrue) + '), ' + prodWord(trueProdKey()) + ' at the ' + st.asked + '. ';
        if (st.mastered) {
          return lead + C + ' to the ' + signWord(catTrue) + ' rod, ' + A + ' to the ' +
            signWord(anTrue) + ', ' + prodWord(trueProdKey()) + ' at the ' + st.asked +
            '. Three in a row ' + MDASH + ' you have it: the ions migrate, positives to ' +
            'the negative cathode to gain electrons (reduction), negatives to the ' +
            'positive anode to lose them (oxidation).';
        }
        return lead + echo + 'The ions themselves cross the liquid: ' + C +
          ' gains electrons at the cathode (a gain is reduction), ' + A +
          ' loses them at the anode.';
      }

      /* stationary ions: the "current just passes through" picture */
      if (st.pick.cat === 'none' || st.pick.an === 'none') {
        var who = (st.pick.cat === 'none' && st.pick.an === 'none') ? 'both ions stay'
          : (st.pick.cat === 'none' ? C + ' stays' : A + ' stays');
        return lead + 'you said ' + who + ' put. Then nothing reaches a rod and no ' +
          'product forms ' + MDASH + ' which is why a solid ionic compound cannot be ' +
          'electrolysed. Molten, the ions travel: ' + C + ' to the ' +
          signWord(catTrue) + ' rod, ' + A + ' to the ' + signWord(anTrue) + ' one.';
      }

      /* positive ion sent to the positive rod */
      if (st.pick.cat !== catTrue) {
        return lead + 'you sent ' + C + ' to ' + rodWord(st.pick.cat) + ', which is the ' +
          signWord(st.pick.cat) + ' one. Like charges repel: a positive ion is pulled the ' +
          'other way, to ' + rodWord(catTrue) + ' ' + MDASH + ' the cathode ' + MDASH +
          ' where it gains electrons and ' + R.metal + ' forms.';
      }

      /* negative ion sent to the negative rod */
      if (st.pick.an !== anTrue) {
        return lead + C + ' was right, but you sent ' + A + ' to ' + rodWord(st.pick.an) +
          ', the ' + signWord(st.pick.an) + ' one. A negative ion is repelled there and ' +
          'attracted to ' + rodWord(anTrue) + ' ' + MDASH + ' the anode ' + MDASH +
          ' where it loses electrons and ' + R.nonmetal + ' forms.';
      }

      /* migration right, electrode naming wrong */
      var said = st.pick.prod === 'none' ? 'nothing forms' : prodWord(st.pick.prod) + ' forms';
      var arriving = st.asked === 'anode' ? A : C;
      var verb = st.asked === 'anode' ? 'loses' : 'gains';
      return lead + 'both ions went the right way, but you said ' + said + ' at the ' +
        st.asked + '. The ' + st.asked + ' is ' + rodWord(sideOfName(st.asked)) + ', the ' +
        signWord(sideOfName(st.asked)) + ' one, so ' + arriving + ' arrives there, ' + verb +
        ' electrons, and ' + prodWord(trueProdKey()) + ' forms.';
    }

    /* ---------- rounds ---------- */
    function nextRound() {
      var prev = st.R;
      st.R = ROUNDS[st.i % ROUNDS.length];
      st.i++;
      st.negSide = Math.random() < 0.5 ? 'left' : 'right';
      st.asked = Math.random() < 0.5 ? 'anode' : 'cathode';
      st.pick = { cat: null, an: null, prod: null };
      st.revealed = false;
      st.correct = null;

      frame.textContent = st.R.name + ' is electrolysed. Its ' + st.R.cat.sym +
        ' and ' + st.R.an.sym + ' ions are free to move. Where does each ion end up, ' +
        'and what forms at the ' + st.asked + '?';

      signL.textContent = st.negSide === 'left' ? '−' : '+';
      signR.textContent = st.negSide === 'left' ? '+' : '−';
      nameL.textContent = '';
      nameR.textContent = '';
      prodL.textContent = '';
      prodR.textContent = '';

      ionName.cat.textContent = st.R.cat.sym;
      ionName.an.textContent = st.R.an.sym;
      ionBtn.cat.concat(ionBtn.an).forEach(function (o) {
        o.b.disabled = false;
        o.b.setAttribute('aria-pressed', 'false');
      });

      lbl2.textContent = '2 ' + DOT + ' What forms at the ' + st.asked + '?';
      var opts = [{ v: 'metal', t: cap1(st.R.metal) }, { v: 'nonmetal', t: cap1(st.R.nonmetal) },
                  { v: 'none', t: 'Nothing forms' }];
      shuffle(opts);
      prodBtn.forEach(function (b, i) {
        b.textContent = opts[i].t;
        b.dataset.v = opts[i].v;
        b.disabled = true;
        b.setAttribute('aria-pressed', 'false');
      });
      step2.classList.add('asleep');

      go.textContent = 'Check';
      go.disabled = true;

      buildIons();
      if (prev) {
        cap.textContent = 'A fresh cell, and the terminals may have swapped over ' +
          MDASH + ' the signs on the rods are the ones that count.';
      } else {
        cap.textContent = 'A solid ionic compound will not conduct: its ions are locked ' +
          'in the lattice. Melting frees them to move.';
      }
      sr.textContent = 'New cell. ' + st.R.name + '. The left rod is the ' +
        (st.negSide === 'left' ? 'negative' : 'positive') + ' terminal, the right rod is the ' +
        (st.negSide === 'left' ? 'positive' : 'negative') + ' terminal.';
      pushState();
    }

    function cap1(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
    function shuffle(a) {
      for (var i = a.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var t = a[i]; a[i] = a[j]; a[j] = t;
      }
      return a;
    }

    go.addEventListener('click', commit);
    nextRound();
  }

  window.SVWidget = {
    meta: {
      id: 'ion-migration-electrolysis',
      title: 'Where do the ions go?',
      teaches: 'In electrolysis the ions themselves migrate: positive ions to the ' +
        'negative cathode where they gain electrons, negative ions to the positive ' +
        'anode where they lose them.'
    },
    mount: mount
  };
})();
