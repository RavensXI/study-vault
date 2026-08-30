/* Across the core - transformer voltage/current trade-off.
   One self-contained lesson widget. No imports, no network, no storage. */
(function () {
  'use strict';

  /* Every round is chosen so the turns ratio divides the supply exactly:
     no awkward decimals in any option the student can pick. */
  var ROUNDS = [
    { np: 100,  ns: 400,  vp: 12,   ip: 8,   grid: null },
    { np: 250,  ns: 1250, vp: 4000, ip: 250, grid: 'up' },
    { np: 800,  ns: 200,  vp: 1200, ip: 8,   grid: null },
    { np: 200,  ns: 600,  vp: 240,  ip: 9,   grid: null },
    { np: 1200, ns: 200,  vp: 6000, ip: 6,   grid: 'down' },
    { np: 150,  ns: 750,  vp: 60,   ip: 10,  grid: null }
  ];

  var CSS = [
    '.svw-tvc{font-family:Inter,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;color:#2d2a26;line-height:1.4}',
    '.svw-tvc *{box-sizing:border-box}',
    '.svw-tvc .kick{margin:0 0 .15rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--tvc-accent)}',
    '.svw-tvc .ttl{margin:0 0 .3rem;font-family:"Source Serif 4",Georgia,serif;font-size:1.18rem;font-weight:600;line-height:1.18}',
    '.svw-tvc .frame{margin:0 0 .55rem;font-size:.84rem;line-height:1.45;color:#5b564e}',
    '.svw-tvc .stage{margin:0 0 .55rem;padding:.35rem .5rem;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px}',
    '.svw-tvc .stage svg{display:block;width:100%;max-width:344px;height:auto;margin:0 auto}',
    '.svw-tvc .grp{margin:0 0 .42rem}',
    '.svw-tvc .grp.sleep{opacity:.55}',
    '.svw-tvc .lab{display:flex;align-items:center;gap:.4rem;margin:0 0 .26rem;font-size:.72rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#5b564e}',
    '.svw-tvc .num{display:inline-flex;align-items:center;justify-content:center;width:17px;height:17px;border-radius:50%;background:#2d2a26;color:#fff;font-size:.66rem;font-weight:700;line-height:1;flex:none}',
    '.svw-tvc .opts{display:grid;grid-template-columns:repeat(3,1fr);gap:.35rem}',
    '.svw-tvc .opt{min-width:0;padding:.5rem .25rem;font-family:inherit;font-size:.82rem;font-weight:600;font-variant-numeric:tabular-nums;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;cursor:pointer;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;transition:background .12s ease,color .12s ease}',
    '.svw-tvc .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-tvc .opt[disabled]{cursor:default}',
    '.svw-tvc .commit{display:flex;align-items:center;gap:.55rem;flex-wrap:wrap;margin:.1rem 0 .5rem}',
    '.svw-tvc .go{margin:0;flex:none;padding:.56rem 1.05rem;font-family:inherit;font-size:.84rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;cursor:pointer}',
    '.svw-tvc .go[disabled]{color:#a29c93;background:#faf8f5;border-color:#e4ded4;cursor:default}',
    '.svw-tvc .run{margin:0;min-height:1.1em;font-size:.76rem;color:#8d8880}',
    '.svw-tvc .cap{margin:0;padding:.58rem .7rem;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;font-size:.84rem;line-height:1.45;min-height:4.2em}',
    '.svw-tvc .cap p{margin:0}',
    '.svw-tvc .cap p + p{margin-top:.3rem}',
    '.svw-tvc button:focus-visible{outline:2px solid var(--tvc-accent);outline-offset:2px}',
    '.svw-tvc.nomo .opt{transition:none}'
  ].join('\n');

  var HTML =
    '<p class="kick">Transformers</p>' +
    '<h3 class="ttl">Across the core</h3>' +
    '<p class="frame">This transformer is supplied on its primary side. Predict what the secondary coil delivers.</p>' +
    '<div class="stage">' +
      '<svg viewBox="0 0 280 104" role="img" aria-label="transformer">' +
        '<text class="t-plab" x="0" y="9" font-size="9" fill="#8d8880"></text>' +
        '<text class="t-slab" x="280" y="9" font-size="9" fill="#8d8880" text-anchor="end"></text>' +
        '<rect x="112" y="14" width="56" height="70" rx="3" fill="#e6e0d5" stroke="#d5cdbf"></rect>' +
        '<rect x="124" y="26" width="32" height="46" fill="#faf8f5" stroke="#d5cdbf"></rect>' +
        '<path class="t-pcoil" fill="none" stroke="#5b564e" stroke-width="2.4" stroke-linecap="round"></path>' +
        '<path class="t-scoil" fill="none" stroke="#5b564e" stroke-width="2.4" stroke-linecap="round"></path>' +
        '<text class="t-core" x="140" y="97" font-size="9" fill="#8d8880" text-anchor="middle">soft iron core</text>' +
        '<text class="t-pval" x="0" y="98" font-size="11.5" font-weight="600" fill="#2d2a26"></text>' +
        '<text class="t-sval" x="280" y="98" font-size="11.5" font-weight="600" fill="#2d2a26" text-anchor="end"></text>' +
      '</svg>' +
    '</div>' +
    '<div class="grp g-v"><span class="lab"><span class="num">1</span>Secondary voltage Vₛ</span>' +
      '<div class="opts o-v"></div></div>' +
    '<div class="grp g-i sleep"><span class="lab"><span class="num">2</span>Secondary current Iₛ</span>' +
      '<div class="opts o-i"></div></div>' +
    '<div class="commit"><button type="button" class="go" disabled>Check</button>' +
      '<div class="run" aria-live="polite"></div></div>' +
    '<div class="cap" aria-live="polite"></div>';

  /* ---- number formatting: British spacing, no stray decimals ---- */
  function grp(n) {
    var s = String(n);
    return s.length > 3 ? s.replace(/\B(?=(\d{3})+(?!\d))/g, ' ') : s;
  }
  function fv(n) { return grp(n) + ' V'; }
  function fa(n) { return grp(n) + ' A'; }
  function fw(w) {
    if (w >= 1000000 && w % 1000000 === 0) return grp(w / 1000000) + ' MW';
    if (w >= 10000 && w % 1000 === 0) return grp(w / 1000) + ' kW';
    return grp(w) + ' W';
  }
  function gcd(a, b) { while (b) { var t = b; b = a % b; a = t; } return a; }

  function derive(d) {
    var g = gcd(d.np, d.ns);
    var up = d.ns > d.np;
    return {
      np: d.np, ns: d.ns, vp: d.vp, ip: d.ip, grid: d.grid, up: up,
      vs: d.vp * d.ns / d.np,          /* the honest answer */
      is: d.ip * d.np / d.ns,          /* current moves the other way */
      vinv: d.vp * d.np / d.ns,        /* ratio applied upside down */
      iflat: d.ip,                     /* "the current just carries on" */
      iup: d.ip * d.ns / d.np,         /* "both rise together" */
      p: d.vp * d.ip,
      ra: d.np / g, rb: d.ns / g,
      f: up ? (d.ns / d.np) : (d.np / d.ns)
    };
  }

  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i];
      a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  window.SVWidget = {
    meta: {
      id: 'transformer-voltage-current-tradeoff',
      title: 'Across the core',
      teaches: 'A transformer that steps voltage up forces the current down by the same factor, because the power delivered can never exceed the power supplied.'
    },

    mount: function (root, ctx) {
      var accent = (ctx && ctx.accent) ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!(ctx && ctx.reducedMotion);

      root.innerHTML = '';
      root.className = 'svw-tvc' + (reduced ? ' nomo' : '');
      root.style.setProperty('--tvc-accent', accent);
      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);
      root.insertAdjacentHTML('beforeend', HTML);

      var q = function (s) { return root.querySelector(s); };
      var picture = q('.stage svg');
      var svg = { plab: q('.t-plab'), slab: q('.t-slab'), pval: q('.t-pval'),
                  sval: q('.t-sval'), pcoil: q('.t-pcoil'), scoil: q('.t-scoil') };
      var boxV = q('.o-v'), boxI = q('.o-i'), grpI = q('.g-i');
      var go = q('.go'), run = q('.run'), cap = q('.cap');

      var idx = 0, r = derive(ROUNDS[0]);
      var pv = null, pi = null, done = false;
      var streak = 0, attempted = 0, mastered = false;

      /* --- build the six option buttons once, then relabel them --- */
      function makeOpts(box, kind) {
        var list = [];
        for (var i = 0; i < 3; i++) {
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'opt';
          b.setAttribute('aria-pressed', 'false');
          box.appendChild(b);
          list.push(b);
          (function (btn) {
            btn.addEventListener('click', function () { pick(kind, btn); });
          })(b);
        }
        return list;
      }
      var vBtns = makeOpts(boxV, 'v'), iBtns = makeOpts(boxI, 'i');

      /* Windings drawn as turns wrapped round a limb, with two leads out to
         the supply or the load - not lines through the core. */
      function coil(path, n, primary) {
        var x = primary ? 112 : 168;          /* the wire runs on the outer face */
        var dir = primary ? -1 : 1;           /* turns bulge away from the core  */
        var sweep = primary ? 0 : 1;
        var top = 26, h = 46 / n;
        var d = 'M' + (x + dir * 16) + ' ' + top + 'H' + x;
        for (var i = 0; i < n; i++) d += 'a6 ' + (h / 2) + ' 0 0 ' + sweep + ' 0 ' + h;
        d += 'H' + (x + dir * 16);
        path.setAttribute('d', d);
      }

      function state() {
        root.dataset.svState = JSON.stringify({
          round: idx + 1, attempted: attempted, streak: streak,
          mastered: mastered, committed: done,
          correct: done ? (pv === r.vs && pi === r.is) : null,
          pickedVs: pv, pickedIs: pi, answerVs: r.vs, answerIs: r.is
        });
      }

      function paintSecondary(answer) {
        svg.sval.textContent = answer
          ? (fv(r.vs) + '  ·  ' + fa(r.is))
          : ((pv === null ? '? V' : fv(pv)) + '  ·  ' + (pi === null ? '? A' : fa(pi)));
        svg.sval.setAttribute('fill', answer ? accent : '#2d2a26');
      }

      function pick(kind, btn) {
        if (done) return;
        var val = Number(btn.dataset.val);
        var list = (kind === 'v') ? vBtns : iBtns;
        for (var i = 0; i < list.length; i++) {
          list[i].setAttribute('aria-pressed', list[i] === btn ? 'true' : 'false');
        }
        if (kind === 'v') { pv = val; } else { pi = val; }
        grpI.classList.remove('sleep');
        paintSecondary(false);
        go.disabled = !(pv !== null && pi !== null);
        state();
      }

      function newRound() {
        r = derive(ROUNDS[idx]);
        pv = null; pi = null; done = false;
        var vs = shuffle([r.vs, r.vinv, r.vp]);
        var is = shuffle([r.is, r.iflat, r.iup]);
        for (var i = 0; i < 3; i++) {
          vBtns[i].textContent = fv(vs[i]); vBtns[i].dataset.val = vs[i];
          vBtns[i].disabled = false; vBtns[i].setAttribute('aria-pressed', 'false');
          iBtns[i].textContent = fa(is[i]); iBtns[i].dataset.val = is[i];
          iBtns[i].disabled = false; iBtns[i].setAttribute('aria-pressed', 'false');
        }
        grpI.classList.add('sleep');
        svg.plab.textContent = 'Primary · Nₚ = ' + grp(r.np) + ' turns';
        svg.slab.textContent = 'Secondary · Nₛ = ' + grp(r.ns) + ' turns';
        svg.pval.textContent = fv(r.vp) + '  ·  ' + fa(r.ip);
        coil(svg.pcoil, r.up ? 3 : 5, true);
        coil(svg.scoil, r.up ? 5 : 3, false);
        paintSecondary(false);
        picture.setAttribute('aria-label',
          'Transformer: primary coil ' + grp(r.np) + ' turns, supplied at ' + fv(r.vp) + ' and ' + fa(r.ip) +
          '; secondary coil ' + grp(r.ns) + ' turns, values not chosen yet.');
        go.textContent = 'Check';
        go.disabled = true;
        runLine();
        say('<p>The two coils never touch. The changing magnetic field in the iron core is the only thing that links them.</p>');
        state();
      }

      function runLine() {
        if (mastered) { run.textContent = 'You have it. Keep going if you like.'; return; }
        if (streak === 1) { run.textContent = '1 right in a row — two more and you have it.'; return; }
        if (streak === 2) { run.textContent = '2 right in a row — one more and you have it.'; return; }
        run.textContent = '';
      }

      function say(html) { cap.innerHTML = html; }

      function dirWords() {
        return r.up
          ? { v: r.f + '× bigger', i: r.f + '× smaller' }
          : { v: r.f + '× smaller', i: r.f + '× bigger' };
      }

      function rightMsg() {
        if (mastered && streak === 3) {
          return '<p>Right — ' + fv(r.vs) + ' and ' + fa(r.is) +
            '. Three in a row — you have it: the turns ratio sets the voltage, the current moves the opposite way by the same factor, and the power out never exceeds the power in.</p>';
        }
        var d = dirWords();
        var one = 'Right — ' + fv(r.vs) + ' and ' + fa(r.is) + '. Turns ratio ' + r.ra + ':' + r.rb +
          ', so the voltage is ' + d.v + ' and the current ' + d.i + ': ' +
          fv(r.vp) + ' × ' + fa(r.ip) + ' = ' + fw(r.p) + ' in, ' +
          fv(r.vs) + ' × ' + fa(r.is) + ' = ' + fw(r.p) + ' out.';
        var two = '';
        if (r.grid === 'up') {
          two = '<p>That is why the grid steps up: ' + fa(r.is) + ' in the cables, not ' +
            fa(r.ip) + ', and heating loss goes with the current squared.</p>';
        } else if (r.grid === 'down') {
          two = '<p>A substation steps down for local use and the current climbs back: ' +
            fa(r.is) + ' locally, where the line carried ' + fa(r.ip) + '.</p>';
        }
        return '<p>' + one + '</p>' + two;
      }

      function wrongMsg() {
        var impl = pv * pi;
        var d = dirWords();
        var s = 'Not quite — you committed ' + fv(pv) + ' and ' + fa(pi) + '. ';
        if (pv === r.vp && pi === r.ip) {
          s += 'That is the primary side unchanged. With ' + grp(r.ns) + ' turns against ' + grp(r.np) +
            ', the voltage is ' + d.v + ' and the current must go the other way. ';
        } else if (impl === r.p) {
          s += 'That is the right power, but the wrong pair: the coil with more turns carries the higher voltage. ';
        } else {
          s += 'That is ' + fw(impl) + ' out of a ' + fw(r.p) + ' supply. ';
          if (pi === r.iflat) {
            s += 'The current cannot carry on unchanged while the voltage changes — power in = power out. ';
          } else if (pi === r.iup) {
            s += 'Voltage and current do not rise together: ' + d.v + ' on the voltage means ' + d.i + ' on the current. ';
          } else {
            s += 'The coil with more turns carries the higher voltage. ';
          }
        }
        s += 'The secondary delivers ' + fv(r.vs) + ' and ' + fa(r.is) + '.';
        return '<p>' + s + '</p>';
      }

      function commit() {
        var ok = (pv === r.vs && pi === r.is);
        var had = streak;
        done = true;
        attempted++;
        streak = ok ? streak + 1 : 0;
        if (streak >= 3) mastered = true;
        for (var i = 0; i < 3; i++) { vBtns[i].disabled = true; iBtns[i].disabled = true; }
        paintSecondary(true);
        picture.setAttribute('aria-label',
          'Transformer: primary ' + fv(r.vp) + ' and ' + fa(r.ip) +
          '; secondary ' + fv(r.vs) + ' and ' + fa(r.is) + '.');
        say(ok ? rightMsg() : wrongMsg());
        runLine();
        if (!ok && had > 0 && !mastered) run.textContent = 'Back to zero — three in a row to finish.';
        go.textContent = mastered ? 'Another anyway' : 'Next transformer';
        go.disabled = false;
        state();
      }

      go.addEventListener('click', function () {
        if (done) {
          var n = idx;
          while (n === idx && ROUNDS.length > 1) n = Math.floor(Math.random() * ROUNDS.length);
          idx = n;
          newRound();
        } else if (pv !== null && pi !== null) {
          commit();
        }
      });

      newRound();
    }
  };
})();
