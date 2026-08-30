/* bond-energy-not-sequential — breaking takes energy in, forming gives it out,
   and the balance of the two totals decides exothermic vs endothermic.
   Self-contained. No imports, no network, no storage. */
(function () {
  'use strict';

  /* Bond energies in kJ/mol, standard GCSE values. Every total below is summed
     from this data at run time — nothing is hand-authored. */
  var REACTIONS = [
    {
      eq: 'H₂ + Cl₂ → 2HCl',
      breakName: 'Bonds in H₂ and Cl₂ break',
      formName: 'Bonds in 2HCl form',
      broken: [{ n: 1, b: 'H–H', e: 436 }, { n: 1, b: 'Cl–Cl', e: 242 }],
      formed: [{ n: 2, b: 'H–Cl', e: 432 }]
    },
    {
      eq: '2HCl → H₂ + Cl₂',
      breakName: 'Bonds in 2HCl break',
      formName: 'Bonds in H₂ and Cl₂ form',
      broken: [{ n: 2, b: 'H–Cl', e: 432 }],
      formed: [{ n: 1, b: 'H–H', e: 436 }, { n: 1, b: 'Cl–Cl', e: 242 }]
    },
    {
      eq: 'N₂ + 3H₂ → 2NH₃',
      breakName: 'Bonds in N₂ and 3H₂ break',
      formName: 'Bonds in 2NH₃ form',
      broken: [{ n: 1, b: 'N≡N', e: 945 }, { n: 3, b: 'H–H', e: 436 }],
      formed: [{ n: 6, b: 'N–H', e: 391 }]
    },
    {
      eq: '2H₂O → 2H₂ + O₂',
      breakName: 'Bonds in 2H₂O break',
      formName: 'Bonds in 2H₂ and O₂ form',
      broken: [{ n: 4, b: 'O–H', e: 464 }],
      formed: [{ n: 2, b: 'H–H', e: 436 }, { n: 1, b: 'O=O', e: 498 }]
    },
    {
      eq: 'CH₄ + 2O₂ → CO₂ + 2H₂O',
      breakName: 'Bonds in CH₄ and 2O₂ break',
      formName: 'Bonds in CO₂ and 2H₂O form',
      broken: [{ n: 4, b: 'C–H', e: 413 }, { n: 2, b: 'O=O', e: 498 }],
      formed: [{ n: 2, b: 'C=O', e: 805 }, { n: 4, b: 'O–H', e: 464 }]
    },
    {
      eq: '2HBr → H₂ + Br₂',
      breakName: 'Bonds in 2HBr break',
      formName: 'Bonds in H₂ and Br₂ form',
      broken: [{ n: 2, b: 'H–Br', e: 366 }],
      formed: [{ n: 1, b: 'H–H', e: 436 }, { n: 1, b: 'Br–Br', e: 193 }]
    }
  ];

  var MINUS = '−';

  function total(list) {
    var s = 0;
    for (var i = 0; i < list.length; i++) s += list[i].n * list[i].e;
    return s;
  }
  function exprFull(list) {
    return list.map(function (x) {
      return (x.n > 1 ? x.n + ' × ' : '') + x.b + ' (' + x.e + ')';
    }).join(' + ');
  }
  function exprNum(list) {
    return list.map(function (x) {
      return x.n > 1 ? x.n + ' × ' + x.e : String(x.e);
    }).join(' + ');
  }
  function names(list) {
    return joinList(list.map(function (x) { return (x.n > 1 ? x.n + ' ' : '') + x.b; }));
  }
  function joinList(a) {
    return a.length > 1 ? a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1] : a[0];
  }
  function word(t) { return t === 'exo' ? 'exothermic' : 'endothermic'; }
  function signed(d) { return (d < 0 ? MINUS : '+') + Math.abs(d); }

  var CSS = [
    '.svw-bens{position:relative;box-sizing:border-box;max-width:100%;background:#fff;',
    'border:1px solid #e8e3db;border-radius:16px;padding:1.35rem;color:#2d2a26;',
    "font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;line-height:1.45;}",
    '.svw-bens *{box-sizing:border-box;}',
    '.svw-bens.bens-narrow{padding:.9rem;}',
    '.svw-bens .bens-kick{margin:0 0 .12rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;',
    'text-transform:uppercase;color:var(--bens-accent);}',
    ".svw-bens .bens-title{margin:0 0 .3rem;font-family:'Source Serif 4',Georgia,serif;",
    'font-size:1.22rem;font-weight:600;line-height:1.2;}',
    '.svw-bens .bens-frame{margin:0 0 .55rem;font-size:.84rem;color:#5b564e;}',
    '.svw-bens .bens-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;',
    'padding:.55rem .65rem;margin:0 0 .55rem;}',
    '.svw-bens .bens-eq{margin:0 0 .45rem;font-size:1rem;font-weight:600;letter-spacing:.01em;',
    'font-variant-numeric:tabular-nums;}',
    '.svw-bens .bens-ask{display:flex;flex-wrap:wrap;align-items:center;gap:.3rem .5rem;margin:0 0 .5rem;}',
    '.svw-bens .bens-step{display:inline-flex;align-items:center;justify-content:center;',
    'width:1.15rem;height:1.15rem;border-radius:50%;background:#2d2a26;color:#fff;',
    'font-size:.66rem;font-weight:700;flex:0 0 auto;}',
    '.svw-bens .bens-asklab{font-size:.78rem;font-weight:600;}',
    '.svw-bens .bens-opts{display:flex;flex-wrap:wrap;gap:.35rem;}',
    '.svw-bens .bens-btn{font:inherit;font-size:.78rem;font-weight:600;color:#2d2a26;',
    'padding:.36rem .6rem;border:1px solid #ddd7cd;border-radius:9px;background:#fff;cursor:pointer;}',
    '.svw-bens .bens-btn:hover:not(:disabled){border-color:#c9c1b4;}',
    '.svw-bens .bens-btn.is-sel{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
    '.svw-bens .bens-btn.is-truth{box-shadow:inset 0 0 0 2px #4f7d63;border-color:#4f7d63;}',
    '.svw-bens .bens-truthtag{font-size:.7rem;font-weight:600;color:#4f7d63;}',
    '.svw-bens .bens-truthtag:empty{display:none;}',
    '.svw-bens .bens-btn:disabled{cursor:default;opacity:1;}',
    '.svw-bens .bens-btn:focus-visible{outline:2px solid var(--bens-accent);outline-offset:2px;}',
    '.svw-bens .bens-cols{display:grid;grid-template-columns:1fr;gap:.5rem;}',
    '.svw-bens.bens-wide .bens-cols{grid-template-columns:1fr 1fr;gap:.7rem;}',
    '.svw-bens .bens-col{min-width:0;border-top:1px solid #efe9e0;padding-top:.4rem;}',
    '.svw-bens .bens-colhead{margin:0 0 .2rem;display:flex;flex-wrap:wrap;align-items:baseline;gap:.35rem;}',
    '.svw-bens .bens-colname{font-size:.76rem;font-weight:600;color:#5b564e;}',
    '.svw-bens .bens-badge{font-size:.64rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;',
    'padding:.08rem .3rem;border-radius:5px;background:var(--bens-tint);color:#2d2a26;}',
    '.svw-bens .bens-badge:empty{display:none;}',
    '.svw-bens .bens-sum{margin:0;font-size:.82rem;font-variant-numeric:tabular-nums;}',
    '.svw-bens .bens-in{width:4.6em;font:inherit;font-size:.82rem;font-variant-numeric:tabular-nums;',
    'padding:.16rem .3rem;border:1px solid #ddd7cd;border-radius:7px;background:#fff;color:#2d2a26;}',
    '.svw-bens .bens-in.is-filled{border-color:var(--bens-accent);}',
    '.svw-bens .bens-in:focus-visible{outline:2px solid var(--bens-accent);outline-offset:1px;}',
    '.svw-bens .bens-bars{margin:0;}',
    '.svw-bens .bens-bar{margin:0 0 .35rem;}',
    '.svw-bens .bens-barhead{display:flex;justify-content:space-between;gap:.5rem;margin:0 0 .16rem;',
    'font-size:.75rem;font-weight:600;font-variant-numeric:tabular-nums;}',
    '.svw-bens .bens-track{height:10px;border-radius:5px;background:#efe9e0;overflow:hidden;}',
    '.svw-bens .bens-fill{display:flex;justify-content:flex-end;height:100%;border-radius:5px;background:#cfc7ba;}',
    '.svw-bens .bens-exc{height:100%;background:var(--bens-accent);}',
    '.svw-bens .bens-diff{margin:.3rem 0 .18rem;font-size:.8rem;font-weight:600;font-variant-numeric:tabular-nums;}',
    '.svw-bens .bens-note{margin:0;font-size:.74rem;color:#8d8880;}',
    '.svw-bens .bens-controls{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem .6rem;margin:0 0 .5rem;}',
    '.svw-bens .bens-go{font:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;',
    'border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer;margin-left:auto;}',
    '.svw-bens .bens-go:focus-visible{outline:2px solid var(--bens-accent);outline-offset:2px;}',
    '.svw-bens .bens-cap{margin:0;font-size:.84rem;line-height:1.5;min-height:2rem;color:#2d2a26;}',
    '.svw-bens .bens-run{margin:.25rem 0 0;font-size:.76rem;color:#8d8880;}',
    '.svw-bens .bens-run:empty{margin:0;}',
    '.svw-bens .bens-run.is-done{color:#4f7d63;font-weight:600;}',
    '.svw-bens .is-hid{display:none;}',
    '.svw-bens .bens-sr{position:absolute;width:1px;height:1px;overflow:hidden;',
    'clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;}',
    '.svw-bens.bens-motion .bens-btn,.svw-bens.bens-motion .bens-in{transition:background-color .14s,border-color .14s,color .14s;}'
  ].join('');

  window.SVWidget = {
    meta: {
      id: 'bond-energy-not-sequential',
      title: 'Energy in, energy out',
      teaches: 'Breaking bonds takes energy in and forming bonds gives energy out; the balance of the two totals decides exothermic or endothermic, not which happens first.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var own = '';
      try { own = (getComputedStyle(root).getPropertyValue('--accent') || '').trim(); } catch (e) { own = ''; }
      var accent = ctx.accent || own || '#7a5c3e';
      var reduced = !!ctx.reducedMotion;

      root.className = (root.className ? root.className + ' ' : '') + 'svw-bens' + (reduced ? '' : ' bens-motion');
      root.style.setProperty('--bens-accent', accent);
      root.style.setProperty('--bens-tint', accent + '2e');

      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      root.insertAdjacentHTML('beforeend', [
        '<p class="bens-kick">Bond energies</p>',
        '<h3 class="bens-title">Energy in, energy out</h3>',
        '<p class="bens-frame">Bond energies are given in kJ/mol. Total the energy taken in and the energy given out, then decide: exothermic or endothermic?</p>',

        '<div class="bens-stage">',
        '  <p class="bens-eq" data-r="eq"></p>',
        '  <div class="bens-ask" data-r="ask">',
        '    <span class="bens-step">1</span>',
        '    <span class="bens-asklab">Energy is taken in by</span>',
        '    <span class="bens-opts">',
        '      <button type="button" class="bens-btn" data-dir="break">the bonds that break</button>',
        '      <button type="button" class="bens-btn" data-dir="form">the bonds that form</button>',
        '    </span>',
        '  </div>',
        '  <div class="bens-cols" data-r="cols">',
        '    <div class="bens-col">',
        '      <p class="bens-colhead"><span class="bens-colname" data-r="nameB"></span><span class="bens-badge" data-r="badgeB"></span></p>',
        '      <p class="bens-sum"><span class="bens-step">2</span> <span data-r="exprB"></span> = <input class="bens-in" type="number" inputmode="numeric" data-r="inB" aria-label="Total for the bonds that break, in kJ"> kJ</p>',
        '    </div>',
        '    <div class="bens-col">',
        '      <p class="bens-colhead"><span class="bens-colname" data-r="nameF"></span><span class="bens-badge" data-r="badgeF"></span></p>',
        '      <p class="bens-sum"><span class="bens-step">2</span> <span data-r="exprF"></span> = <input class="bens-in" type="number" inputmode="numeric" data-r="inF" aria-label="Total for the bonds that form, in kJ"> kJ</p>',
        '    </div>',
        '  </div>',
        '  <div class="bens-bars is-hid" data-r="bars">',
        '    <div class="bens-bar">',
        '      <p class="bens-barhead"><span data-r="labIn"></span><span data-r="valIn"></span></p>',
        '      <div class="bens-track"><div class="bens-fill" data-r="fillIn"><span class="bens-exc" data-r="excIn"></span></div></div>',
        '    </div>',
        '    <div class="bens-bar">',
        '      <p class="bens-barhead"><span data-r="labOut"></span><span data-r="valOut"></span></p>',
        '      <div class="bens-track"><div class="bens-fill" data-r="fillOut"><span class="bens-exc" data-r="excOut"></span></div></div>',
        '    </div>',
        '    <p class="bens-diff" data-r="diff"></p>',
        '    <p class="bens-note">Not two phases — breaking and forming overlap right through the reaction.</p>',
        '  </div>',
        '</div>',

        '<div class="bens-controls">',
        '  <span class="bens-step">3</span>',
        '  <span class="bens-asklab">Overall the reaction is</span>',
        '  <span class="bens-opts">',
        '    <button type="button" class="bens-btn" data-type="exo">exothermic</button>',
        '    <button type="button" class="bens-btn" data-type="endo">endothermic</button>',
        '    <span class="bens-truthtag" data-r="truthtag"></span>',
        '  </span>',
        '  <button type="button" class="bens-go" data-r="go">Check</button>',
        '</div>',

        '<p class="bens-cap" data-r="cap"></p>',
        '<p class="bens-run" data-r="run"></p>',
        '<p class="bens-sr" data-r="sr" aria-live="polite"></p>'
      ].join(''));

      var q = {};
      var nodes = root.querySelectorAll('[data-r]');
      for (var i = 0; i < nodes.length; i++) q[nodes[i].getAttribute('data-r')] = nodes[i];
      var dirBtns = root.querySelectorAll('[data-dir]');
      var typeBtns = root.querySelectorAll('[data-type]');

      /* ---- session state ---- */
      var order = REACTIONS.map(function (_, k) { return k; });
      var ptr = 0;
      var streak = 0, attempted = 0, mastered = false;
      var r = null, dir = null, type = null, committed = false;

      function shuffle(a) {
        for (var k = a.length - 1; k > 0; k--) {
          var j = Math.floor(Math.random() * (k + 1));
          var t = a[k]; a[k] = a[j]; a[j] = t;
        }
      }
      shuffle(order);

      function nextReaction() {
        if (ptr >= order.length) {
          var last = order[order.length - 1];
          do { shuffle(order); } while (order[0] === last);
          ptr = 0;
        }
        return REACTIONS[order[ptr++]];
      }

      function publish(extra) {
        var s = {
          reaction: r ? r.eq : null,
          inSide: dir,
          saidType: type,
          streak: streak,
          mastered: mastered,
          attempted: attempted,
          committed: committed
        };
        if (extra) for (var k in extra) if (Object.prototype.hasOwnProperty.call(extra, k)) s[k] = extra[k];
        root.dataset.svState = JSON.stringify(s);
      }

      function setSel(list, attr, val) {
        for (var k = 0; k < list.length; k++) {
          list[k].classList.toggle('is-sel', list[k].getAttribute(attr) === val);
          list[k].setAttribute('aria-pressed', list[k].getAttribute(attr) === val ? 'true' : 'false');
        }
      }

      function paintBadges() {
        q.badgeB.textContent = dir ? (dir === 'break' ? 'energy in' : 'energy out') : '';
        q.badgeF.textContent = dir ? (dir === 'break' ? 'energy out' : 'energy in') : '';
      }

      function lock(on) {
        for (var k = 0; k < dirBtns.length; k++) dirBtns[k].disabled = on;
        for (var m = 0; m < typeBtns.length; m++) typeBtns[m].disabled = on;
        q.inB.readOnly = on;
        q.inF.readOnly = on;
      }

      function newRound() {
        r = nextReaction();
        dir = null; type = null; committed = false;
        q.eq.textContent = r.eq;
        q.nameB.textContent = r.breakName;
        q.nameF.textContent = r.formName;
        q.exprB.textContent = exprFull(r.broken);
        q.exprF.textContent = exprFull(r.formed);
        q.inB.value = ''; q.inF.value = '';
        q.inB.classList.remove('is-filled'); q.inF.classList.remove('is-filled');
        setSel(dirBtns, 'data-dir', null);
        setSel(typeBtns, 'data-type', null);
        for (var t2 = 0; t2 < typeBtns.length; t2++) typeBtns[t2].classList.remove('is-truth');
        q.truthtag.textContent = '';
        paintBadges();
        q.bars.classList.add('is-hid');
        q.cols.classList.remove('is-hid');
        q.ask.classList.remove('is-hid');
        q.cap.textContent = '';
        q.go.textContent = 'Check';
        lock(false);
        publish();
      }

      function say(msg) {
        q.cap.textContent = msg;
        q.sr.textContent = msg;
      }

      function runLine() {
        if (mastered && streak >= 3) {
          q.run.classList.add('is-done');
          q.run.textContent = 'Three in a row — you have it. Breaking takes energy in, forming gives it out, and the bigger total decides — never the order.';
          return;
        }
        q.run.classList.remove('is-done');
        if (streak === 1) q.run.textContent = '1 right in a row — two more and you have it.';
        else if (streak === 2) q.run.textContent = '2 right in a row — one more and you have it.';
        else if (attempted > 0) q.run.textContent = 'Run reset — three in a row and you have it.';
        else q.run.textContent = '';
      }

      function drawBars(EIN, EOUT) {
        var max = Math.max(EIN, EOUT);
        q.labIn.textContent = 'Bonds broken — energy in';
        q.labOut.textContent = 'Bonds formed — energy out';
        q.valIn.textContent = EIN + ' kJ';
        q.valOut.textContent = EOUT + ' kJ';
        q.fillIn.style.width = (EIN / max * 100) + '%';
        q.fillOut.style.width = (EOUT / max * 100) + '%';
        var excPct = (max - Math.min(EIN, EOUT)) / max * 100;
        q.excIn.style.width = EIN > EOUT ? excPct + '%' : '0%';
        q.excOut.style.width = EOUT > EIN ? excPct + '%' : '0%';
        var d = EIN - EOUT;
        q.diff.textContent = EIN + ' ' + MINUS + ' ' + EOUT + ' = ' + signed(d) + ' kJ — ' +
          (d < 0 ? 'more out than in, so exothermic' : 'more in than out, so endothermic');
        q.bars.classList.remove('is-hid');
        q.cols.classList.add('is-hid');
        q.ask.classList.add('is-hid');
      }

      function commit() {
        var vB = parseInt(q.inB.value, 10);
        var vF = parseInt(q.inF.value, 10);
        var missing = [];
        if (!dir) missing.push('choose which side takes energy in');
        if (isNaN(vB)) missing.push('total the bonds that break');
        if (isNaN(vF)) missing.push('total the bonds that form');
        if (!type) missing.push('pick exothermic or endothermic');
        if (missing.length) {
          say('Still to do: ' + joinList(missing) + '.');
          publish({ incomplete: missing.length });
          return;
        }

        var EIN = total(r.broken), EOUT = total(r.formed);
        var d = EIN - EOUT;
        var truth = d < 0 ? 'exo' : 'endo';
        var sIn = dir === 'break' ? vB : vF;
        var sOut = dir === 'break' ? vF : vB;
        var dirOK = dir === 'break';
        var sumsOK = vB === EIN && vF === EOUT;
        var typeOK = type === truth;
        var right = dirOK && sumsOK && typeOK;

        attempted++;
        streak = right ? streak + 1 : 0;
        if (streak >= 3) mastered = true;
        committed = true;

        var msg;
        if (right) {
          msg = 'Right — ' + EIN + ' kJ in to break ' + names(r.broken) + ', ' + EOUT +
            ' kJ out as ' + names(r.formed) + ' form. ' + EIN + ' ' + MINUS + ' ' + EOUT + ' = ' +
            signed(d) + ' kJ: ' + word(truth) + '. The two totals decide it, not the order.';
        } else if (!dirOK) {
          msg = 'Not quite — you committed ' + sIn + ' kJ in, ' + sOut + ' kJ out and ' + word(type) +
            '. Breaking a bond needs energy pushed in to pull the atoms apart; forming one gives energy out. So it is ' +
            EIN + ' kJ in, ' + EOUT + ' kJ out: ' + EIN + ' ' + MINUS + ' ' + EOUT + ' = ' + signed(d) +
            ' kJ, ' + word(truth) + '.';
        } else if (!sumsOK) {
          msg = 'Not quite — you committed ' + sIn + ' kJ in, ' + sOut + ' kJ out and ' + word(type) +
            '. Broken: ' + exprNum(r.broken) + ' = ' + EIN + ' kJ. Formed: ' + exprNum(r.formed) + ' = ' +
            EOUT + ' kJ — every repeat counts. ' + EIN + ' ' + MINUS + ' ' + EOUT + ' = ' + signed(d) +
            ' kJ, ' + word(truth) + '.';
        } else {
          msg = 'Not quite — your totals were right, ' + EIN + ' kJ in and ' + EOUT + ' kJ out, but you said ' +
            word(type) + '. ' + EIN + ' ' + MINUS + ' ' + EOUT + ' = ' + signed(d) + ' kJ: ' +
            (d < 0 ? 'more comes out than goes in, so energy leaves the reaction'
                   : 'more goes in than comes out, so energy is drawn in') +
            ' — ' + word(truth) + '.';
        }

        drawBars(EIN, EOUT);
        for (var t = 0; t < typeBtns.length; t++) {
          var isTrue = typeBtns[t].getAttribute('data-type') === truth;
          typeBtns[t].classList.toggle('is-truth', isTrue);
          /* the tag must sit beside the option it points at, whichever that is */
          if (isTrue && !typeOK) typeBtns[t].insertAdjacentElement('afterend', q.truthtag);
        }
        q.truthtag.textContent = typeOK ? '' : '← this one';
        lock(true);
        say(msg);
        runLine();
        q.go.textContent = mastered ? 'Another anyway' : 'Next reaction';
        publish({
          energyIn: EIN, energyOut: EOUT, change: d, type: truth,
          saidIn: sIn, saidOut: sOut, saidType: type, correct: right
        });
      }

      /* ---- wiring (DOM built once, mutated thereafter) ---- */
      for (var a = 0; a < dirBtns.length; a++) {
        dirBtns[a].addEventListener('click', function () {
          if (committed) return;
          dir = this.getAttribute('data-dir');
          setSel(dirBtns, 'data-dir', dir);
          paintBadges();
          publish();
        });
      }
      for (var b = 0; b < typeBtns.length; b++) {
        typeBtns[b].addEventListener('click', function () {
          if (committed) return;
          type = this.getAttribute('data-type');
          setSel(typeBtns, 'data-type', type);
          publish();
        });
      }
      [q.inB, q.inF].forEach(function (el) {
        el.addEventListener('input', function () {
          el.classList.toggle('is-filled', el.value.trim() !== '');
        });
        el.addEventListener('keydown', function (ev) {
          if (ev.key === 'Enter') { ev.preventDefault(); q.go.click(); }
        });
      });
      q.go.addEventListener('click', function () {
        if (committed) newRound(); else commit();
      });

      function fitToOwnWidth() {
        var w = root.getBoundingClientRect().width;
        if (!w) return;
        root.classList.toggle('bens-wide', w >= 600);
        root.classList.toggle('bens-narrow', w <= 400);
      }
      if (typeof ResizeObserver === 'function') {
        new ResizeObserver(fitToOwnWidth).observe(root);
      } else if (window.addEventListener) {
        window.addEventListener('resize', fitToOwnWidth);
      }
      fitToOwnWidth();

      newRound();
      runLine();
    }
  };
})();
