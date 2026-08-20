/* em-spectrum-continuous — one continuous EM spectrum, seven human labels.
   Self-contained. No imports, no network, no storage outside root. */
(function () {
  'use strict';

  var C = 3e8;                 /* speed of all EM waves in a vacuum, GCSE value */
  var LMAX = 3, LMIN = -13, SPAN = LMAX - LMIN;   /* log10(wavelength / m) */
  var LV_HI = Math.log10(7e-7);
  var LV_LO = Math.log10(4e-7);

  var BANDS = [
    /* reg = singular form for "is in the ___ region"; name = prose form.
       Boundaries are the conventional GCSE values and are approximate. */
    { key: 'radio', reg: 'radio',         name: 'radio waves',   btn: 'Radio',       lo: -1,    hi: LMAX,  rng: '10⁻¹ m and longer' },
    { key: 'micro', reg: 'microwave',     name: 'microwaves',    btn: 'Microwaves',  lo: -3,    hi: -1,    rng: 'about 10⁻³ to 10⁻¹ m' },
    { key: 'ir',    reg: 'infrared',      name: 'infrared',      btn: 'Infrared',    lo: LV_HI, hi: -3,    rng: 'about 7 × 10⁻⁷ to 10⁻³ m' },
    { key: 'vis',   reg: 'visible light', name: 'visible light', btn: 'Visible',     lo: LV_LO, hi: LV_HI, rng: 'about 4 × 10⁻⁷ to 7 × 10⁻⁷ m' },
    { key: 'uv',    reg: 'ultraviolet',   name: 'ultraviolet',   btn: 'Ultraviolet', lo: -8,    hi: LV_LO, rng: 'about 10⁻⁸ to 4 × 10⁻⁷ m' },
    { key: 'xray',  reg: 'X-ray',         name: 'X-rays',        btn: 'X-rays',      lo: -11,   hi: -8,    rng: 'about 10⁻¹¹ to 10⁻⁸ m' },
    { key: 'gamma', reg: 'gamma ray',     name: 'gamma rays',    btn: 'Gamma',       lo: LMIN,  hi: -11,   rng: 'shorter than about 10⁻¹¹ m' }
  ];

  var SUPCH = { '-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³',
                '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹' };

  function sup(n) {
    var s = String(n), o = '', i;
    for (i = 0; i < s.length; i++) o += (SUPCH[s.charAt(i)] || s.charAt(i));
    return o;
  }

  function sci(x, dp) {
    if (dp == null) dp = 1;
    var e = Math.floor(Math.log10(Math.abs(x)));
    var m = x / Math.pow(10, e);
    m = Number(m.toFixed(dp));
    if (Math.abs(m) >= 10) { m = Number((m / 10).toFixed(dp)); e += 1; }
    /* 10⁰ = 1: write "3.0", never the odd-looking "3.0 × 10⁰" */
    if (e === 0) return m.toFixed(dp);
    return m.toFixed(dp) + ' × 10' + sup(e);
  }

  function bandOf(L) {
    for (var i = 0; i < BANDS.length; i++) if (L >= BANDS[i].lo) return BANDS[i];
    return BANDS[BANDS.length - 1];
  }
  function bandByKey(k) {
    for (var i = 0; i < BANDS.length; i++) if (BANDS[i].key === k) return BANDS[i];
    return null;
  }
  function idxOf(b) {
    for (var i = 0; i < BANDS.length; i++) if (BANDS[i].key === b.key) return i;
    return -1;
  }
  function xOf(L) {
    var t = (LMAX - L) / SPAN;
    return t < 0 ? 0 : (t > 1 ? 1 : t);
  }
  function mid(b) { return (Math.max(b.lo, LMIN) + Math.min(b.hi, LMAX)) / 2; }

  /* how band a compares with band b, in orders of magnitude of wavelength */
  function relTo(a, b) {
    var d = Math.round(mid(a) - mid(b));
    if (d === 0) return null;
    return 'about 10' + sup(Math.abs(d)) + ' times ' + (d > 0 ? 'longer' : 'shorter');
  }

  /* ---------- round banks ---------- */

  var BANK_A = [
    { lam: 1500,    key: 'radio' }, { lam: 3,       key: 'radio' }, { lam: 0.25,   key: 'radio' },
    { lam: 3e-2,    key: 'micro' }, { lam: 1.2e-2,  key: 'micro' }, { lam: 5e-3,   key: 'micro' },
    { lam: 2e-4,    key: 'ir'    }, { lam: 1e-5,    key: 'ir'    }, { lam: 3e-6,   key: 'ir'    },
    { lam: 6.5e-7,  key: 'vis'   }, { lam: 5e-7,    key: 'vis'   }, { lam: 4.5e-7, key: 'vis'   },
    { lam: 3e-7,    key: 'uv'    }, { lam: 1e-7,    key: 'uv'    }, { lam: 3e-8,   key: 'uv'    },
    { lam: 1e-9,    key: 'xray'  }, { lam: 4e-10,   key: 'xray'  }, { lam: 6e-11,  key: 'xray'  },
    { lam: 5e-12,   key: 'gamma' }, { lam: 1e-12,   key: 'gamma' }, { lam: 3e-13,  key: 'gamma' }
  ];

  var ROW2 = {
    speed: {
      label: 'Speed in a vacuum',
      ask: 'the speed',
      opts: ['Still 3 × 10⁸ m/s', 'Faster', 'Slower'],
      right: function () { return 0; },
      fix: function () {
        return 'Speed never shifts: every EM wave crosses a vacuum at 3.0 × 10⁸ m/s.';
      }
    },
    kind: {
      label: 'Type of wave',
      ask: 'the type of wave',
      opts: ['Still transverse', 'Now longitudinal', 'No longer a wave'],
      right: function () { return 0; },
      fix: function () {
        return 'It stays transverse — changing λ slides it along the ribbon, it does not make it ' +
          'another kind of thing.';
      }
    },
    medium: {
      label: 'Need for a medium',
      ask: 'the need for a medium',
      opts: ['No — still crosses a vacuum', 'Yes — it needs matter now'],
      right: function () { return 0; },
      fix: function () {
        return 'No EM wave needs a medium: that is how sunlight crosses empty space.';
      }
    },
    energy: {
      label: 'Energy the radiation transfers',
      ask: 'the energy',
      opts: ['Higher', 'Lower', 'Unchanged'],
      right: function (r) { return r.shorter ? 0 : 1; },
      fix: function (r) {
        return 'Energy follows frequency, so a ' + (r.shorter ? 'shorter' : 'longer') +
          ' λ carries ' + (r.shorter ? 'more' : 'less') + ' — the short end is the dangerous end.';
      }
    }
  };

  var BANK_B = [
    { lam: 3e-2,   f: 1000,  shorter: true,  row2: 'speed'  },
    { lam: 6e-7,   f: 100,   shorter: true,  row2: 'kind'   },
    { lam: 2e-10,  f: 10000, shorter: false, row2: 'medium' },
    { lam: 5e-7,   f: 50,    shorter: true,  row2: 'energy' },
    { lam: 4e-9,   f: 25,    shorter: false, row2: 'kind'   },
    { lam: 2e-2,   f: 200,   shorter: false, row2: 'energy' }
  ];

  /* visible is a 1.5% sliver — never a fair slider target */
  var BANK_C = [
    { key: 'radio', scene: 'A long-wave transmitter is being tuned.' },
    { key: 'micro', scene: 'A satellite link is being tested.' },
    { key: 'ir',    scene: 'A thermal camera is being calibrated.' },
    { key: 'uv',    scene: 'A sunbed is being safety-checked.' },
    { key: 'xray',  scene: 'A hospital scanner is being serviced.' },
    { key: 'gamma', scene: 'A sealed radioactive source is being surveyed.' }
  ];

  window.SVWidget = {
    meta: {
      id: 'em-spectrum-continuous',
      title: 'Across the spectrum',
      teaches: 'The seven named regions are labels on one continuous slide of wavelength and frequency; in a vacuum every EM wave is transverse and travels at 3 × 10⁸ m/s.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#a8642e';
      var still = !!ctx.reducedMotion;

      root.classList.add('svw-emsc');

      var css = '' +
      /* the host modal is already the white card (STYLE_DIGEST): paint no page
         background, no second border, no second ring of padding. */
      '.svw-emsc{box-sizing:border-box;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;' +
        'color:#2d2a26;max-width:100%;-webkit-text-size-adjust:100%;}' +
      '.svw-emsc *,.svw-emsc *::before,.svw-emsc *::after{box-sizing:border-box;}' +
      '.svw-emsc .e-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + ';}' +
      '.svw-emsc .e-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;' +
        'margin:.12rem 0 .3rem;line-height:1.15;}' +
      '.svw-emsc .e-frame{margin:0 0 .6rem;font-size:.84rem;line-height:1.45;color:#3c3831;}' +
      '.svw-emsc .e-frame b{font-weight:600;}' +
      '.svw-emsc .e-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.6rem .65rem .55rem;}' +
      '.svw-emsc .e-ticks{position:relative;height:13px;}' +
      '.svw-emsc .e-tick{position:absolute;top:0;font-size:.62rem;color:#8d8880;white-space:nowrap;' +
        'transform:translateX(-50%);font-variant-numeric:tabular-nums;}' +
      '.svw-emsc .e-tick.e-t0{transform:none;left:0;}' +
      '.svw-emsc .e-tick.e-t9{transform:translateX(-100%);}' +
      '.svw-emsc .e-ribbon{position:relative;height:34px;border-radius:5px;overflow:hidden;' +
        'background:linear-gradient(to right,#efe6d6 0%,#e3d3b4 16%,#cbb488 30%,#a89c7e 44%,' +
        '#7f8894 58%,#5b6675 70%,#3c414e 84%,#26262e 100%);}' +
      '.svw-emsc .e-vis{position:absolute;top:0;bottom:0;min-width:4px;' +
        'background:linear-gradient(to right,#c0352c,#d97a2b,#d8c341,#3f9f6a,#3f5fd0,#7b3fa0);}' +
      '.svw-emsc .e-marker{position:absolute;top:0;bottom:0;width:2px;margin-left:-1px;' +
        'background:' + accent + ';box-shadow:0 0 0 1px #fff;}' +
      '.svw-emsc .e-marker::after{content:"";position:absolute;top:2px;left:-3px;width:8px;height:8px;' +
        'border-radius:50%;background:' + accent + ';box-shadow:0 0 0 1.5px #fff;}' +
      '.svw-emsc .e-pin{position:absolute;top:0;bottom:0;width:2px;margin-left:-1px;background:#2d2a26;opacity:.85;}' +
      '.svw-emsc .e-brk{position:relative;height:26px;margin-top:3px;}' +
      '.svw-emsc .e-bar{position:absolute;height:4px;border-radius:2px;}' +
      '.svw-emsc .e-blab{position:absolute;font-size:.66rem;font-weight:600;white-space:nowrap;' +
        'transform:translateX(-50%);}' +
      '.svw-emsc .e-r0 .e-bar{top:0;background:' + accent + ';}' +
      '.svw-emsc .e-r0 .e-blab{top:5px;color:' + accent + ';}' +
      '.svw-emsc .e-r1 .e-bar{top:17px;background:#b3aca1;}' +
      '.svw-emsc .e-r1 .e-blab{top:21px;color:#7d776e;}' +
      '.svw-emsc .e-sl{margin:.5rem 0 .1rem;}' +
      '.svw-emsc input[type=range].e-range{-webkit-appearance:none;appearance:none;width:100%;height:18px;' +
        'background:transparent;display:block;margin:0;cursor:pointer;}' +
      '.svw-emsc input[type=range].e-range:focus{outline:none;}' +
      '.svw-emsc input[type=range].e-range::-webkit-slider-runnable-track{height:5px;border-radius:3px;background:#ddd7cd;}' +
      '.svw-emsc input[type=range].e-range::-moz-range-track{height:5px;border-radius:3px;background:#ddd7cd;}' +
      '.svw-emsc input[type=range].e-range::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;' +
        'width:17px;height:17px;border-radius:50%;background:#fff;border:2px solid ' + accent + ';margin-top:-6px;}' +
      '.svw-emsc input[type=range].e-range::-moz-range-thumb{width:15px;height:15px;border-radius:50%;' +
        'background:#fff;border:2px solid ' + accent + ';}' +
      '.svw-emsc input[type=range].e-range:focus-visible::-webkit-slider-thumb{box-shadow:0 0 0 3px ' + accent + '44;}' +
      '.svw-emsc .e-ends{display:flex;justify-content:space-between;font-size:.66rem;color:#8d8880;}' +
      '.svw-emsc .e-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(92px,1fr));gap:.3rem .5rem;' +
        'margin-top:.45rem;padding-top:.45rem;border-top:1px solid #efe9e0;}' +
      '.svw-emsc .e-sl2{display:block;font-size:.66rem;font-weight:600;color:#8d8880;letter-spacing:.01em;}' +
      '.svw-emsc .e-sv{display:block;font-size:.79rem;font-weight:600;font-variant-numeric:tabular-nums;}' +
      '.svw-emsc .e-q{margin-top:.6rem;}' +
      '.svw-emsc .e-row+.e-row{margin-top:.4rem;}' +
      '.svw-emsc .e-rl{display:block;font-size:.7rem;font-weight:700;color:#5b564e;margin-bottom:.22rem;}' +
      '.svw-emsc .e-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(92px,1fr));gap:.35rem;}' +
      '.svw-emsc .e-opt{font:inherit;font-size:.76rem;font-weight:600;line-height:1.2;padding:.42rem .4rem;' +
        'border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;text-align:center;}' +
      '.svw-emsc .e-opt[aria-pressed=true]{background:#2d2a26;border-color:#2d2a26;color:#fff;}' +
      '.svw-emsc .e-opt.e-key{border-color:' + accent + ';box-shadow:inset 0 0 0 1px ' + accent + ';}' +
      '.svw-emsc .e-opt:disabled{cursor:default;opacity:.75;}' +
      '.svw-emsc .e-act{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin-top:.6rem;}' +
      '.svw-emsc .e-go{font:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;' +
        'border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer;}' +
      '.svw-emsc .e-go:disabled{background:#faf8f5;color:#a29b91;border-color:#ddd7cd;cursor:default;}' +
      '.svw-emsc .e-run{font-size:.74rem;color:#8d8880;}' +
      '.svw-emsc .e-cap{margin:.6rem 0 0;padding-top:.55rem;border-top:1px solid #efe9e0;font-size:.82rem;' +
        'line-height:1.5;color:#3c3831;min-height:3.6em;}' +
      '.svw-emsc .e-cap strong{font-weight:600;color:#2d2a26;}' +
      '.svw-emsc .e-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);' +
        'clip-path:inset(50%);white-space:nowrap;}' +
      (still ? '.svw-emsc *{transition:none !important;animation:none !important;}' : '');

      var st = document.createElement('style');
      st.textContent = css;
      root.appendChild(st);

      /* ---------- build DOM once ---------- */
      function el(tag, cls, txt) {
        var n = document.createElement(tag);
        if (cls) n.className = cls;
        if (txt != null) n.textContent = txt;
        return n;
      }

      var kick = el('div', 'e-kick', 'Electromagnetic waves');
      var title = el('h3', 'e-title', 'Across the spectrum');
      var frame = el('p', 'e-frame');
      root.appendChild(kick); root.appendChild(title); root.appendChild(frame);

      var stage = el('div', 'e-stage');
      var ticks = el('div', 'e-ticks');
      [[3, '1 km'], [0, '1 m'], [-3, '1 mm'], [-6, '1 µm'], [-9, '1 nm'], [-12, '1 pm']]
        .forEach(function (t, i, arr) {
          var s = el('span', 'e-tick' + (i === 0 ? ' e-t0' : (i === arr.length - 1 ? ' e-t9' : '')), t[1]);
          s.style.left = (xOf(t[0]) * 100).toFixed(2) + '%';
          ticks.appendChild(s);
        });
      var ribbon = el('div', 'e-ribbon');
      var visStrip = el('span', 'e-vis');
      visStrip.style.left = (xOf(LV_HI) * 100).toFixed(2) + '%';
      visStrip.style.width = ((xOf(LV_LO) - xOf(LV_HI)) * 100).toFixed(2) + '%';
      var marker = el('span', 'e-marker');
      ribbon.appendChild(visStrip); ribbon.appendChild(marker);
      var brk = el('div', 'e-brk');
      stage.appendChild(ticks); stage.appendChild(ribbon); stage.appendChild(brk);

      var slWrap = el('div', 'e-sl');
      var range = document.createElement('input');
      range.type = 'range';
      range.className = 'e-range';
      range.min = '0'; range.max = String(SPAN * 100); range.step = '1';
      range.setAttribute('aria-label', 'Detector wavelength');
      slWrap.appendChild(range);
      var ends = el('div', 'e-ends');
      ends.appendChild(el('span', null, '← longer waves'));
      ends.appendChild(el('span', null, 'shorter waves →'));
      slWrap.appendChild(ends);
      stage.appendChild(slWrap);

      var stats = el('div', 'e-stats');
      function stat(lab) {
        var w = el('div');
        w.appendChild(el('span', 'e-sl2', lab));
        var v = el('span', 'e-sv', '—');
        w.appendChild(v); stats.appendChild(w);
        return v;
      }
      var vLam = stat('Wavelength λ');
      var vFrq = stat('Frequency f');
      var vSpd = stat('Speed v = fλ');
      stage.appendChild(stats);
      root.appendChild(stage);

      var qBox = el('div', 'e-q');
      root.appendChild(qBox);

      var act = el('div', 'e-act');
      var go = el('button', 'e-go', 'Check');
      go.type = 'button';
      var run = el('span', 'e-run', '');
      act.appendChild(go); act.appendChild(run);
      root.appendChild(act);

      var cap = el('p', 'e-cap');
      root.appendChild(cap);
      var sr = el('p', 'e-sr');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      function setRich(node, str) {
        node.textContent = '';
        var parts = String(str).split('**');
        for (var i = 0; i < parts.length; i++) {
          if (!parts[i]) continue;
          if (i % 2 === 1) { var b = document.createElement('strong'); b.textContent = parts[i]; node.appendChild(b); }
          else node.appendChild(document.createTextNode(parts[i]));
        }
      }

      /* ---------- state ---------- */
      var S = {
        lam: 1e-5,
        round: null,
        type: 0,
        pick: [null, null],
        locked: false,
        streak: 0,
        attempted: 0,
        mastered: false,
        lastCorrect: null,
        poolA: [], poolB: [], poolC: []
      };

      function draw(pool, bank) {
        if (!pool.length) {
          var i;
          for (i = 0; i < bank.length; i++) pool.push(i);
          for (i = pool.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1)), t = pool[i]; pool[i] = pool[j]; pool[j] = t;
          }
        }
        return bank[pool.pop()];
      }

      function setLambda(lam) {
        S.lam = lam;
        var L = Math.log10(lam);
        range.value = String(Math.round((LMAX - L) * 100));
        paint();
      }

      function paint() {
        var L = Math.log10(S.lam);
        var f = C / S.lam;
        marker.style.left = (xOf(L) * 100).toFixed(3) + '%';
        vLam.textContent = sci(S.lam) + ' m';
        vFrq.textContent = sci(f) + ' Hz';
        vSpd.textContent = sci(f * S.lam) + ' m/s';
        if (!S.locked) {
          var live = 'At λ = ' + sci(S.lam) + ' m the frequency is ' + sci(f) +
            ' Hz, so v = fλ = ' + sci(f * S.lam) + ' m/s.';
          setRich(cap, live);
          sr.textContent = live;
        }
        pushState();
      }

      function pushState() {
        root.dataset.svState = JSON.stringify({
          streak: S.streak,
          mastered: S.mastered,
          attempted: S.attempted,
          correct: S.lastCorrect,
          task: S.round ? S.round.type : null,
          picked: S.pick[1] == null ? S.pick[0] : (S.pick[0] + ',' + S.pick[1]),
          wavelength: Number(S.lam.toPrecision(3)),
          frequency: Number((C / S.lam).toPrecision(3)),
          region: bandOf(Math.log10(S.lam)).key
        });
      }

      /* ---------- reveal marks under the ribbon ---------- */
      var pins = [];
      function clearReveal() {
        brk.textContent = '';
        while (pins.length) { ribbon.removeChild(pins.pop()); }
      }
      function addPin(L) {
        var p = el('span', 'e-pin');
        p.style.left = (xOf(L) * 100).toFixed(3) + '%';
        ribbon.appendChild(p);
        pins.push(p);
      }
      function addBar(rowCls, b, text) {
        var g = el('div', rowCls);
        var bar = el('span', 'e-bar');
        var x0 = xOf(Math.min(b.hi, LMAX)), x1 = xOf(Math.max(b.lo, LMIN));
        bar.style.left = (x0 * 100).toFixed(2) + '%';
        bar.style.width = Math.max(0.9, (x1 - x0) * 100).toFixed(2) + '%';
        g.appendChild(bar);
        var lab = el('span', 'e-blab', text);
        var cx = (x0 + x1) / 2;
        lab.style.left = (Math.min(0.86, Math.max(0.14, cx)) * 100).toFixed(2) + '%';
        g.appendChild(lab);
        brk.appendChild(g);
      }

      /* ---------- question rendering ---------- */
      var optBtns = [];

      function optionRow(rowIdx, label, opts) {
        var row = el('div', 'e-row');
        if (label) row.appendChild(el('span', 'e-rl', label));
        var grid = el('div', 'e-opts');
        opts.forEach(function (txt, i) {
          var b = el('button', 'e-opt', txt);
          b.type = 'button';
          b.setAttribute('aria-pressed', 'false');
          b.addEventListener('click', function () {
            if (S.locked) return;
            S.pick[rowIdx] = i;
            optBtns.forEach(function (o) {
              if (o.row === rowIdx) o.node.setAttribute('aria-pressed', o.i === i ? 'true' : 'false');
            });
            syncGo();
            pushState();
          });
          optBtns.push({ node: b, row: rowIdx, i: i });
          grid.appendChild(b);
        });
        row.appendChild(grid);
        qBox.appendChild(row);
      }

      function syncGo() {
        if (S.locked) { go.disabled = false; return; }
        var r = S.round;
        if (r.type === 'C') { go.disabled = false; return; }
        var need = (r.type === 'B') ? 2 : 1;
        var have = 0;
        for (var i = 0; i < need; i++) if (S.pick[i] != null) have++;
        go.disabled = have < need;
      }

      function newRound() {
        S.type = (S.type % 3) + 1;
        S.pick = [null, null];
        S.locked = false;
        optBtns = [];
        qBox.textContent = '';
        clearReveal();
        go.textContent = 'Check';

        var r;
        if (S.type === 1) {
          var a = draw(S.poolA, BANK_A);
          r = { type: 'A', lam: a.lam, band: bandByKey(a.key) };
          setLambda(a.lam);
          setRich(frame, 'A detector in a vacuum picks up an electromagnetic wave of wavelength **' +
            sci(a.lam) + ' m**. Name the region of the spectrum it belongs to.');
          optionRow(0, null, BANDS.map(function (b) { return b.btn; }));
        } else if (S.type === 2) {
          var b2 = draw(S.poolB, BANK_B);
          var lam1 = b2.shorter ? b2.lam / b2.f : b2.lam * b2.f;
          var fs = b2.f >= 10000 ? '10 000' : String(b2.f);
          r = {
            type: 'B', lam: b2.lam, lam1: lam1, factor: b2.f, fs: fs, shorter: b2.shorter,
            row2: ROW2[b2.row2],
            right: [b2.shorter ? 0 : 1, ROW2[b2.row2].right(b2)]
          };
          setLambda(b2.lam);
          setRich(frame, 'A source in a vacuum emits an electromagnetic wave of wavelength **' +
            sci(b2.lam) + ' m**. It is swapped for a source whose wavelength is **' + fs +
            '× ' + (b2.shorter ? 'shorter' : 'longer') + '**. Predict what happens to each property.');
          optionRow(0, 'Frequency', [fs + '× higher', fs + '× lower', 'Unchanged']);
          optionRow(1, r.row2.label, r.row2.opts);
        } else {
          var c = draw(S.poolC, BANK_C);
          var target = bandByKey(c.key), ti = idxOf(target), si;
          do { si = Math.floor(Math.random() * BANDS.length); } while (Math.abs(si - ti) < 2);
          r = { type: 'C', band: target };
          setLambda(Math.pow(10, mid(BANDS[si])));
          setRich(frame, c.scene + ' Set the detector to a wavelength that lies in the **' +
            target.name + '** region.');
        }
        S.round = r;
        S.lastCorrect = null;
        syncGo();
        paint();
        pushState();
      }

      /* ---------- feedback ---------- */
      function judge() {
        var r = S.round, ok, msg;
        S.attempted++;

        if (r.type === 'A') {
          var chose = BANDS[S.pick[0]];
          ok = chose.key === r.band.key;
          var f = C / r.lam;
          addPin(Math.log10(r.lam));
          addBar('e-r0', r.band, r.band.btn);
          if (ok) {
            msg = 'Right — ' + sci(r.lam) + ' m is in the **' + r.band.reg + '** region (' + r.band.rng +
              '), f = ' + sci(f) + ' Hz. Here fλ = ' + sci(f * r.lam) +
              ' m/s, and it is that at every other point on the ribbon too.';
          } else {
            addBar('e-r1', chose, 'you said ' + chose.btn);
            var adj = Math.abs(idxOf(chose) - idxOf(r.band)) === 1;
            var gap = relTo(chose, r.band);
            msg = 'Not quite — you said **' + chose.name + '**. ' + sci(r.lam) + ' m is in the **' +
              r.band.reg + '** region (' + r.band.rng + '); ' +
              (adj || !gap
                ? 'that region sits right next door, and the dividing line is a naming convention, not a wall.'
                : 'that region is ' + gap + '.') +
              ' Same family, same 3.0 × 10⁸ m/s in a vacuum — only λ and f differ.';
          }
        } else if (r.type === 'B') {
          ok = (S.pick[0] === r.right[0]) && (S.pick[1] === r.right[1]);
          var f0 = C / r.lam, f1 = C / r.lam1;
          var b0 = bandOf(Math.log10(r.lam)), b1 = bandOf(Math.log10(r.lam1));
          addPin(Math.log10(r.lam)); addPin(Math.log10(r.lam1));
          addBar('e-r0', b0, 'before: ' + b0.btn);
          addBar('e-r1', b1, 'after: ' + b1.btn);
          if (ok) {
            msg = 'Right — λ ' + r.fs + '× ' + (r.shorter ? 'shorter' : 'longer') + ' makes f ' +
              r.fs + '× ' + (r.shorter ? 'higher' : 'lower') + ': ' + sci(f0) + ' → ' + sci(f1) +
              ' Hz, with **v fixed at 3.0 × 10⁸ m/s**. The label slid from ' + b0.name +
              ' to ' + b1.name + '; the wave itself did not change kind.';
          } else {
            var said0 = [r.fs + '× higher', r.fs + '× lower', 'unchanged'][S.pick[0]];
            var said1 = r.row2.opts[S.pick[1]].toLowerCase();
            var badF = S.pick[0] !== r.right[0], badR = S.pick[1] !== r.right[1];
            var echo = [];
            if (badF) echo.push('Frequency: **' + said0 + '**');
            if (badR) echo.push(r.row2.label + ': **' + said1 + '**');
            var why = [];
            if (badF) {
              why.push('v is fixed at 3.0 × 10⁸ m/s, so v = fλ forces f ' +
                (r.shorter ? 'up' : 'down') + ': ' + sci(f0) + ' → ' + sci(f1) + ' Hz.');
            }
            if (badR) why.push(r.row2.fix(r));
            /* both rows wrong is already a long message — drop the tail then */
            if (!(badF && badR)) {
              why.push('Same wave, new label (' + b0.name + ' → ' + b1.name + ').');
            }
            msg = 'Not quite — you said ' + echo.join('; ') + '. ' + why.join(' ');
          }
        } else {
          var got = bandOf(Math.log10(S.lam));
          ok = got.key === r.band.key;
          var fc = C / S.lam;
          addPin(Math.log10(S.lam));
          addBar('e-r0', r.band, r.band.btn);
          if (ok) {
            msg = 'Right — ' + sci(S.lam) + ' m lies in the **' + r.band.reg + '** region (' + r.band.rng +
              '), f = ' + sci(fc) + ' Hz. Move either way and the name changes while v holds at ' +
              sci(fc * S.lam) + ' m/s: the regions are labels, not separate things.';
          } else {
            addBar('e-r1', got, 'you set ' + got.btn);
            var adj2 = Math.abs(idxOf(got) - idxOf(r.band)) === 1;
            var gap2 = relTo(r.band, got);   /* target relative to where they stopped */
            msg = 'Not quite — ' + sci(S.lam) + ' m is in the **' + got.reg + '** region. ' +
              'The **' + r.band.reg + '** region is ' + r.band.rng +
              (adj2 || !gap2
                ? ', so you stopped just the wrong side of the mark — and that mark is where we change the name, not where the wave changes.'
                : ' — ' + gap2 + ' than where you stopped. Same family either way: still transverse, still 3.0 × 10⁸ m/s.');
          }
        }

        S.lastCorrect = ok;
        var prevStreak = S.streak;
        if (ok) S.streak++; else S.streak = 0;
        var justMastered = false;
        if (ok && S.streak >= 3 && !S.mastered) { S.mastered = true; justMastered = true; }

        if (justMastered) {
          msg = 'Right — three in a row, and you have it: one continuous ribbon, ' +
            '**3.0 × 10⁸ m/s in a vacuum for every part of it**, all transverse. ' +
            'Shorten λ and f rises to match; the seven names are only labels on the slide.';
        }

        S.locked = true;
        optBtns.forEach(function (o) {
          o.node.disabled = true;
          var key = (r.type === 'A') ? (BANDS[o.i].key === r.band.key)
                                     : (o.i === r.right[o.row]);
          if (key) o.node.classList.add('e-key');
        });

        setRich(cap, msg);
        sr.textContent = msg;
        go.textContent = S.mastered ? 'Another anyway' : 'Next wave';
        go.disabled = false;
        run.textContent = S.mastered ? ''
          : (S.streak === 0 ? (prevStreak > 0 ? 'Run reset — back to nought.' : '')
            : S.streak === 1 ? '1 right in a row — two more.'
            : '2 right in a row — one more and you have it.');
        pushState();
      }

      /* ---------- wiring ---------- */
      range.addEventListener('input', function () {
        var L = LMAX - (Number(range.value) / 100);
        S.lam = Math.pow(10, L);
        paint();
      });

      go.addEventListener('click', function () {
        if (S.locked) { newRound(); return; }
        judge();
      });

      newRound();
      pushState();
    }
  };
})();
