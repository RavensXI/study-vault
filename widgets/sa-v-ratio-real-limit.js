/* Surface area to volume ratio as a real physical limit on diffusion.
   Self-contained: no imports, no network, no storage, all CSS scoped. */
(function () {
  'use strict';

  /* Model rule, stated to the student: a block can supply itself by
     diffusion alone when it has at least BAR cm2 of surface for every
     cm3 of tissue. Tested on integers (sa >= BAR * v) so no pair ever
     sits on a floating-point knife edge. Tightest margin in the pool is
     +2 cm2 (34 vs 32); the closest failure is -4 (28 vs 32). */
  var BAR = 4;

  /* Every figure is derived from w/d/h at run time. The payoff sentence
     is the only authored prose per pair; each was checked against the
     computed numbers. */
  var PAIRS = [
    { a: { w: 1, d: 1, h: 1 }, b: { w: 2, d: 2, h: 2 },
      payoff: '' },
    { a: { w: 3, d: 3, h: 3 }, b: { w: 2, d: 2, h: 2 },
      payoff: 'Both are chunky, and chunky loses: tissue in the middle sits a long way from any surface.' },
    { a: { w: 6, d: 1, h: 1 }, b: { w: 2, d: 2, h: 2 },
      payoff: 'A is the longer block and still wins — being thin beats being small.' },
    { a: { w: 2, d: 2, h: 2 }, b: { w: 8, d: 1, h: 1 },
      payoff: 'Shape alone decides it here.' },
    { a: { w: 1, d: 1, h: 1 }, b: { w: 4, d: 1, h: 1 },
      payoff: 'B holds four times the tissue and still copes, because it never gets thick.' },
    { a: { w: 4, d: 4, h: 4 }, b: { w: 3, d: 1, h: 1 },
      payoff: 'The big cube has far more surface in total — and nothing like enough of it per cm³.' },
    { a: { w: 2, d: 1, h: 1 }, b: { w: 3, d: 3, h: 3 },
      payoff: 'Over five times A’s surface, but over thirteen times A’s tissue — that is the squeeze.' },
    { a: { w: 4, d: 2, h: 1 }, b: { w: 8, d: 1, h: 1 },
      payoff: 'Narrow in two directions beats narrow in one — that is the shape of a villus.' },
    { a: { w: 5, d: 1, h: 1 }, b: { w: 3, d: 3, h: 1 },
      payoff: 'B is thin too, but wide with it — thinness helps only if surface keeps pace with tissue.' },
    { a: { w: 2, d: 2, h: 2 }, b: { w: 3, d: 3, h: 1 },
      payoff: 'Flattening B does lift its ratio above A’s, but not far enough to clear the bar.' },
    { a: { w: 2, d: 1, h: 1 }, b: { w: 5, d: 1, h: 1 },
      payoff: 'B holds two and a half times A’s tissue and still manages — thin wins again.' }
  ];

  var OPTS = [['a', 'A only'], ['b', 'B only'], ['both', 'Both'], ['neither', 'Neither']];
  var PHRASE = { a: 'A only', b: 'B only', both: 'both of them', neither: 'neither of them' };

  var OPENING = 'SA:V is a supply figure: how many cm² of surface each cm³ of tissue has to draw on.';

  var MASTERY = 'Three in a row — you have it: volume outgrows surface, so SA:V always falls as size rises, ' +
    'and only narrow shapes keep it up — hence finger-shaped villi and thread-like root hairs.';

  var CSS =
    '.svw-sav{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45}' +
    '.svw-sav *{box-sizing:border-box}' +
    '.svw-sav p,.svw-sav h3{margin:0}' +
    '.svw-sav .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin-bottom:.15rem}' +
    '.svw-sav .t{font-family:"Source Serif 4",Georgia,serif;font-size:1.12rem;font-weight:600;line-height:1.2;margin-bottom:.28rem}' +
    '.svw-sav .frame{font-size:.82rem;color:#5b564e;margin-bottom:.5rem}' +
    '.svw-sav .stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem;display:grid;grid-template-columns:1fr 1fr;gap:.5rem}' +
    '.svw-sav .col{min-width:0;text-align:center}' +
    '.svw-sav .cl{font-size:.72rem;color:#8d8880;font-variant-numeric:tabular-nums}' +
    '.svw-sav .cl b{color:#2d2a26;font-weight:700}' +
    '.svw-sav .draw svg{display:block;width:100%;height:96px}' +
    '.svw-sav .fig{display:none}' +
    '.svw-sav .col.rev .fig{display:block}' +
    '.svw-sav .fig p{font-size:.72rem;color:#5b564e;font-variant-numeric:tabular-nums;line-height:1.3}' +
    '.svw-sav .fig .r{font-size:.8rem;font-weight:700}' +
    '.svw-sav .fig .tag{font-size:.7rem;font-weight:600;line-height:1.25;margin-top:.05rem}' +
    '.svw-sav .col.pass .tag{color:#4f7d63}' +
    '.svw-sav .col.fail .tag{color:#8d8880}' +
    '.svw-sav .q{font-size:.78rem;font-weight:600;margin:.5rem 0 .28rem}' +
    /* fixed 2x2 at every width: single-block answers on the top row, joint answers below */
    '.svw-sav .opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.35rem;max-width:480px}' +
    '.svw-sav .b{font-family:inherit;font-size:.82rem;font-weight:600;padding:.4rem .55rem;border-radius:10px;' +
      'border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;text-align:center}' +
    '.svw-sav:not(.rm) .b{transition:background-color .12s ease,border-color .12s ease}' +
    '.svw-sav .b[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}' +
    '.svw-sav .row{display:flex;align-items:center;gap:.6rem;margin-top:.45rem}' +
    '.svw-sav .go{font-family:inherit;font-size:.82rem;font-weight:600;padding:.45rem 1rem;border-radius:10px;' +
      'border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer;flex:none}' +
    '.svw-sav .go[disabled]{background:#faf8f5;color:#a9a299;border-color:#e0d9cd;cursor:default}' +
    '.svw-sav .run{font-size:.74rem;color:#8d8880;min-height:1em}' +
    '.svw-sav .cap{font-size:.84rem;margin-top:.45rem;min-height:5.4em}' +
    '.svw-sav .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}';

  function met(b) { return { sa: 2 * (b.w * b.d + b.w * b.h + b.d * b.h), v: b.w * b.d * b.h }; }
  function passes(m) { return m.sa >= BAR * m.v; }
  function num(x) { return String(Math.round(x * 100) / 100); }
  function dimStr(b) { return b.w + '×' + b.d + '×' + b.h + ' cm'; }

  /* n such that y is a uniform n-times enlargement of x, else 0 */
  function scaleN(x, y) {
    var n = y.w / x.w;
    if (n >= 2 && Math.abs(n - Math.round(n)) < 1e-9 && y.d === x.d * n && y.h === x.h * n) return Math.round(n);
    return 0;
  }

  function draw(b, ex, ey, accent, verdict) {
    var K = 0.45, w = b.w, d = b.d, h = b.h;
    var bw = w + K * d, bh = h + K * d;
    var ox = (ex - bw) / 2, oy = (ey - bh) / 2, fy = oy + K * d;
    var edge = verdict === null ? '#b0a798' : (verdict ? '#4f7d63' : '#9a938a');
    var grid = verdict === null ? '#d3cbbd' : (verdict ? '#a9c3b3' : '#cac3ba');
    var s = [], i;
    function n(x) { return Math.round(x * 1000) / 1000; }
    function poly(pts, fill) {
      var p = pts.map(function (q) { return n(q[0]) + ',' + n(q[1]); }).join(' ');
      s.push('<polygon points="' + p + '" fill="' + fill + '" stroke="' + edge +
        '" stroke-width="1.2" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>');
    }
    function line(x1, y1, x2, y2) {
      s.push('<line x1="' + n(x1) + '" y1="' + n(y1) + '" x2="' + n(x2) + '" y2="' + n(y2) +
        '" stroke="' + grid + '" stroke-width=".7" vector-effect="non-scaling-stroke"/>');
    }
    poly([[ox, fy], [ox + K * d, oy], [ox + w + K * d, oy], [ox + w, fy]], accent + '33');
    poly([[ox + w, fy], [ox + w + K * d, oy], [ox + w + K * d, oy + h], [ox + w, fy + h]], accent + '1a');
    s.push('<rect x="' + n(ox) + '" y="' + n(fy) + '" width="' + n(w) + '" height="' + n(h) +
      '" fill="#ffffff" stroke="' + edge + '" stroke-width="1.2" vector-effect="non-scaling-stroke"/>');
    for (i = 1; i < w; i++) { line(ox + i, fy, ox + i, fy + h); line(ox + i, fy, ox + i + K * d, oy); }
    for (i = 1; i < h; i++) { line(ox, fy + i, ox + w, fy + i); line(ox + w, fy + i, ox + w + K * d, oy + i); }
    for (i = 1; i < d; i++) {
      line(ox + i * K, fy - i * K, ox + w + i * K, fy - i * K);
      line(ox + w + i * K, fy - i * K, ox + w + i * K, fy - i * K + h);
    }
    return '<svg viewBox="0 0 ' + n(ex) + ' ' + n(ey) + '" preserveAspectRatio="xMidYMid meet" ' +
      'aria-hidden="true" focusable="false">' + s.join('') + '</svg>';
  }

  window.SVWidget = {
    meta: {
      id: 'sa-v-ratio-real-limit',
      title: 'Can it live on its surface alone?',
      teaches: 'Volume outgrows surface area, so SA:V falls as size rises — the physical reason large organisms need exchange surfaces.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = String(ctx.accent || '').trim();
      if (!/^#[0-9a-fA-F]{6}$/.test(accent)) {
        accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim();
      }
      if (!/^#[0-9a-fA-F]{6}$/.test(accent)) accent = '#8a6a4f';

      /* pair 0 first (the canonical cube doubling), then a shuffled tail */
      var order = [0], rest = [], i, j, t;
      for (i = 1; i < PAIRS.length; i++) rest.push(i);
      for (i = rest.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1)); t = rest[i]; rest[i] = rest[j]; rest[j] = t;
      }
      order = order.concat(rest);

      var pos = 0, sel = null, done = false, streak = 0, attempted = 0, mastered = false;
      var P, A, B, mA, mB, rA, rB, passA, passB, key;

      function colHTML(kk) {
        return '<div class="col" data-c="' + kk + '">' +
          '<p class="cl"><b>Block ' + kk.toUpperCase() + '</b> <span class="dm"></span></p>' +
          '<div class="draw"></div>' +
          '<div class="fig"><p class="fsa"></p><p class="fv"></p><p class="r"></p><p class="tag"></p></div>' +
          '</div>';
      }

      var wrap = document.createElement('div');
      wrap.className = 'svw-sav' + (ctx.reducedMotion ? ' rm' : '');
      var st = document.createElement('style');
      st.textContent = CSS;
      wrap.appendChild(st);

      wrap.insertAdjacentHTML('beforeend',
        '<p class="k">Surface area : volume</p>' +
        '<h3 class="t">Two blocks, two ratios</h3>' +
        '<p class="frame">Each block is solid living tissue, taking in oxygen only by diffusion through its ' +
        'outer surface. In this model a block needs an SA:V of at least 4:1 to supply every cell.</p>' +
        '<div class="stage">' + colHTML('a') + colHTML('b') + '</div>' +
        '<p class="q" id="svsav-q">Which can manage on its surface alone?</p>' +
        '<div class="opts" role="group" aria-labelledby="svsav-q"></div>' +
        '<div class="row"><button type="button" class="go"></button><p class="run"></p></div>' +
        '<p class="cap"></p>' +
        '<p class="sr" aria-live="polite"></p>');

      var cols = { a: wrap.querySelector('[data-c="a"]'), b: wrap.querySelector('[data-c="b"]') };
      var optWrap = wrap.querySelector('.opts');
      var go = wrap.querySelector('.go');
      var run = wrap.querySelector('.run');
      var cap = wrap.querySelector('.cap');
      var sr = wrap.querySelector('.sr');
      var btns = {};

      OPTS.forEach(function (o) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'b';
        b.textContent = o[1];
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', function () { pick(o[0]); });
        optWrap.appendChild(b);
        btns[o[0]] = b;
      });

      go.addEventListener('click', function () { if (done) { next(); } else { commit(); } });

      wrap.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && sel && !done) pick(sel);
      });

      function pick(k) {
        if (done) return;
        sel = (sel === k) ? null : k;
        OPTS.forEach(function (o) { btns[o[0]].setAttribute('aria-pressed', String(sel === o[0])); });
        go.disabled = !sel;
        push();
      }

      function frame() {
        var eA = { x: A.w + 0.45 * A.d, y: A.h + 0.45 * A.d };
        var eB = { x: B.w + 0.45 * B.d, y: B.h + 0.45 * B.d };
        return { ex: Math.max(eA.x, eB.x) + 0.7, ey: Math.max(eA.y, eB.y) + 0.7 };
      }

      function load() {
        P = PAIRS[order[pos % order.length]];
        A = P.a; B = P.b;
        mA = met(A); mB = met(B);
        rA = mA.sa / mA.v; rB = mB.sa / mB.v;
        passA = passes(mA); passB = passes(mB);
        key = (passA && passB) ? 'both' : passA ? 'a' : passB ? 'b' : 'neither';
        var f = frame();
        [['a', A], ['b', B]].forEach(function (row) {
          var c = cols[row[0]];
          c.className = 'col';
          c.querySelector('.dm').textContent = dimStr(row[1]);
          c.querySelector('.draw').innerHTML = draw(row[1], f.ex, f.ey, accent, null);
        });
      }

      function reveal() {
        var f = frame();
        [['a', A, mA, passA], ['b', B, mB, passB]].forEach(function (row) {
          var c = cols[row[0]], m = row[2], ok = row[3];
          c.className = 'col rev ' + (ok ? 'pass' : 'fail');
          c.querySelector('.draw').innerHTML = draw(row[1], f.ex, f.ey, accent, ok);
          c.querySelector('.fsa').textContent = 'Surface ' + m.sa + ' cm²';
          c.querySelector('.fv').textContent = 'Volume ' + m.v + ' cm³';
          var r = c.querySelector('.r');
          r.textContent = 'SA:V ' + num(m.sa / m.v) + ':1';
          r.style.color = accent;
          c.querySelector('.tag').textContent = ok ? 'surface alone is enough' : 'needs an exchange system';
        });
      }

      function mechanism() {
        var n = scaleN(A, B), big = 'B', small = 'A';
        if (!n) { n = scaleN(B, A); if (n) { big = 'A'; small = 'B'; } }
        if (n) {
          var rBig = big === 'A' ? rA : rB, rSmall = small === 'A' ? rA : rB;
          return big + ' is ' + n + '× the width of ' + small + ': ' + (n * n) + '× the surface but ' +
            (n * n * n) + '× the tissue. Each cm³ of ' + small + ' has ' + num(rSmall) +
            ' cm² of surface working for it; each cm³ of ' + big + ' only ' + num(rBig) + '.';
        }
        var hi = rA > rB ? 'A' : 'B', lo = hi === 'A' ? 'B' : 'A';
        var mHi = hi === 'A' ? mA : mB, mLo = hi === 'A' ? mB : mA;
        if (mA.v === mB.v) {
          return 'Both hold ' + mA.v + ' cm³, yet ' + hi + ' exposes ' + mHi.sa + ' cm² against ' +
            mLo.sa + ' — stretching the same tissue out puts more of it at the surface.';
        }
        return 'Every cm³ of ' + hi + ' has ' + num(mHi.sa / mHi.v) +
          ' cm² of surface working for it; every cm³ of ' + lo + ' has only ' + num(mLo.sa / mLo.v) + '.';
      }

      function diagnosis() {
        var claim = { a: sel === 'a' || sel === 'both', b: sel === 'b' || sel === 'both' };
        var truth = { a: passA, b: passB }, out = [];
        ['a', 'b'].forEach(function (kk) {
          if (claim[kk] === truth[kk]) return;
          var m = kk === 'a' ? mA : mB;
          out.push(kk.toUpperCase() + ': ' + m.sa + ' cm² over ' + m.v + ' cm³ — ' +
            num(m.sa / m.v) + ' cm² per cm³, ' + (truth[kk] ? 'clear of the bar.' : 'under the bar.'));
        });
        var big = mA.v > mB.v ? 'a' : (mB.v > mA.v ? 'b' : null);
        if (big && claim[big] && !truth[big]) out.push('More surface in total is not more surface per cm³.');
        return out.join(' ');
      }

      function commit() {
        if (!sel || done) return;
        done = true;
        attempted++;
        var right = sel === key;
        streak = right ? streak + 1 : 0;
        var justMastered = right && streak >= 3 && !mastered;
        if (justMastered) mastered = true;
        reveal();

        var text;
        if (right) {
          /* on the mastery round the generalisation replaces the per-round
             mechanism - both blocks' figures are on the stage above it */
          text = 'Right — ' + PHRASE[key] + '. ' +
            (justMastered ? MASTERY : mechanism() + (P.payoff ? ' ' + P.payoff : ''));
        } else {
          text = 'Not quite — you said ' + PHRASE[sel] + '; the geometry gives ' + PHRASE[key] + '. ' + diagnosis();
        }
        cap.textContent = text;
        run.textContent = mastered
          ? (justMastered ? 'Three in a row — mastered.' : 'Mastered — keep going if you like.')
          : (right
              ? (streak === 1 ? '1 right in a row — two more and you have it.'
                              : '2 right in a row — one more and you have it.')
              : 'Back to zero — three in a row ends it.');
        go.textContent = mastered ? 'Another anyway' : 'Next pair';
        go.disabled = false;
        sr.textContent = 'Block A: surface ' + mA.sa + ' square centimetres, volume ' + mA.v +
          ' cubic centimetres, ratio ' + num(rA) + ' to 1. Block B: surface ' + mB.sa + ', volume ' +
          mB.v + ', ratio ' + num(rB) + ' to 1. ' + text;
        push();
      }

      function next() {
        pos++;
        done = false;
        sel = null;
        OPTS.forEach(function (o) { btns[o[0]].setAttribute('aria-pressed', 'false'); });
        load();
        cap.textContent = OPENING;
        run.textContent = mastered ? 'Mastered — keep going if you like.' : '';
        go.textContent = 'Check';
        go.disabled = true;
        sr.textContent = 'New pair. Block A ' + dimStr(A) + ', Block B ' + dimStr(B) + '.';
        if (document.activeElement === go) btns.a.focus();
        push();
      }

      function push() {
        root.dataset.svState = JSON.stringify({
          sel: sel, answer: key, correct: done ? (sel === key) : null,
          streak: streak, mastered: mastered, attempted: attempted,
          saA: mA.sa, vA: mA.v, ratioA: Math.round(rA * 100) / 100,
          saB: mB.sa, vB: mB.v, ratioB: Math.round(rB * 100) / 100
        });
      }

      root.appendChild(wrap);
      load();
      cap.textContent = OPENING;
      go.textContent = 'Check';
      go.disabled = true;
      push();
    }
  };
})();
