/* redshift-stretching-mechanism — self-contained lesson widget.
   Predict where a galaxy's hydrogen absorption lines land in the spectrum
   that reaches Earth, then read distance from the size of the redshift. */
(function () {
  'use strict';

  var SVGNS = 'http://www.w3.org/2000/svg';

  /* ---- physics model ------------------------------------------------- */
  var REST = [434, 486, 656];      // nm, hydrogen absorption lines
  var HEAD = 656;                  // the line quoted in prose
  var LAM0 = 400, LAM1 = 720;      // wavelength span drawn on the strip
  var X0 = 8, X1 = 292;            // user units for that span
  var C_KMS = 300000;              // speed of light, km/s

  // shifts are held as integers in parts per thousand, so every comparison
  // and every size band is decided on integers, never on a float.
  function xOf(nm) { return X0 + (nm - LAM0) * (X1 - X0) / (LAM1 - LAM0); }
  function obsNm(nm, pm) { return Math.round(nm * (1000 + pm) / 1000); }
  function speedKms(pm) { return Math.abs(pm) * (C_KMS / 1000); }
  function group(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function pctTxt(pm) {
    var t = Math.abs(pm) / 10;
    return (Math.abs(pm) % 10 === 0 ? t.toFixed(0) : t.toFixed(1)) + '%';
  }

  // size bands: small <= 30 pm (3%), big >= 45 pm (4.5%). No round sits
  // between the two, so the intended answer is always clear of the edge.
  var SMALL_MAX = 30, BIG_MIN = 45;

  /* ---- round banks ---------------------------------------------------- */
  // pm = the true shift. small/big/blue = the magnitudes offered as options,
  // one of which is the truth. Every option value is computed, not typed.
  var SHIFTS = [
    { pm:  60, small: 20, big: 60, blue: 40 },
    { pm:  20, small: 20, big: 60, blue: 40 },
    { pm: -40, small: 20, big: 60, blue: 40 },
    { pm:   0, small: 20, big: 60, blue: 40 },
    { pm:  50, small: 20, big: 50, blue: 40 },
    { pm:  25, small: 25, big: 60, blue: 40 },
    { pm: -20, small: 25, big: 60, blue: 20 },
    { pm:   0, small: 25, big: 50, blue: 20 }
  ];
  var PAIRS = [
    { a: 20, b: 60 }, { a: 60, b: 20 }, { a: 30, b: 30 },
    { a: 25, b: 50 }, { a: 50, b: 25 }, { a: 60, b: 60 }
  ];

  function bandOf(pm) {
    if (pm === 0) return 'none';
    if (pm < 0) return 'blue';
    return pm <= SMALL_MAX ? 'redsmall' : 'redbig';
  }
  function pairAnswer(p) { return p.a > p.b ? 'A' : (p.b > p.a ? 'B' : 'same'); }

  // Keep only rounds whose true shift is unambiguously small or big, and whose
  // offered option carries exactly the true arrival wavelength.
  SHIFTS = SHIFTS.filter(function (r) {
    var b = bandOf(r.pm);
    if (r.pm > SMALL_MAX && r.pm < BIG_MIN) return false;
    if (b === 'redsmall') return r.small === r.pm;
    if (b === 'redbig') return r.big === r.pm;
    if (b === 'blue') return r.blue === -r.pm;
    return true;
  });

  /* ---- small helpers -------------------------------------------------- */
  function svg(tag, attrs) {
    var n = document.createElementNS(SVGNS, tag), k;
    for (k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
    return n;
  }
  function h(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }
  function shuffled(arr) {
    var a = arr.slice(), i, j, t;
    for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1)); t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  var CSS = [
    '.svw-rs{background:#fff;border:1px solid #e8e3db;border-radius:16px;padding:1rem 1.1rem 1.05rem;',
    'font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4;}',
    '.svw-rs *{box-sizing:border-box;}',
    '.svw-rs .rs-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .15rem;}',
    '.svw-rs .rs-ttl{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.2;margin:0 0 .28rem;}',
    '.svw-rs .rs-frame{font-size:.86rem;line-height:1.4;margin:0 0 .45rem;color:#4a453e;}',
    '.svw-rs .rs-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.35rem .3rem;margin:0 0 .45rem;}',
    '.svw-rs .rs-svg{display:block;width:100%;height:auto;max-width:470px;margin:0 auto;}',
    '.svw-rs .rs-opts{display:grid;gap:.3rem;grid-template-columns:repeat(auto-fit,minmax(238px,1fr));margin:0 0 .45rem;}',
    '.svw-rs .rs-opt{display:flex;align-items:baseline;justify-content:space-between;gap:.45rem;width:100%;text-align:left;',
    'font-family:inherit;font-size:.8rem;font-weight:600;line-height:1.25;color:#2d2a26;background:#faf8f5;',
    'border:1px solid #ddd7cd;border-radius:10px;padding:.3rem .6rem;cursor:pointer;font-variant-numeric:tabular-nums;}',
    '.svw-rs .rs-opt:hover:not(:disabled){border-color:#c3bbac;}',
    '.svw-rs .rs-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
    '.svw-rs .rs-opt:disabled{cursor:default;opacity:.45;}',
    '.svw-rs .rs-opt.is-key{opacity:1;border-color:#4f7d63;box-shadow:inset 0 0 0 1px #4f7d63;}',
    '.svw-rs .rs-opt.is-yours{opacity:1;}',
    '.svw-rs .rs-tag{font-size:.68rem;font-weight:600;letter-spacing:.04em;white-space:nowrap;color:#8d8880;}',
    '.svw-rs .rs-opt.is-key .rs-tag{color:#4f7d63;}',
    '.svw-rs .rs-opt[aria-pressed="true"] .rs-tag{color:#e8e3db;}',
    '.svw-rs .rs-row{display:flex;align-items:center;justify-content:space-between;gap:.6rem;margin:0 0 .45rem;}',
    '.svw-rs .rs-run{font-size:.76rem;color:#8d8880;min-height:1rem;}',
    '.svw-rs .rs-go{font-family:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;',
    'border-radius:10px;padding:.45rem .95rem;cursor:pointer;white-space:nowrap;}',
    '.svw-rs .rs-go:disabled{opacity:.4;cursor:default;}',
    '.svw-rs .rs-cap{font-size:.84rem;line-height:1.45;margin:0;min-height:4.8em;color:#3c3831;}',
    '.svw-rs .rs-cap b{font-weight:700;}',
    '.svw-rs .rs-cap b.ok{color:#4f7d63;}',
    '.svw-rs .rs-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;',
    'clip:rect(0 0 0 0);white-space:nowrap;border:0;}',
    '.svw-rs .rs-line{transform:translateX(0px);}',
    '.svw-rs.rs-anim .rs-line{transition:transform .55s cubic-bezier(0.16,1,0.3,1);}'
  ].join('');

  window.SVWidget = {
    meta: {
      id: 'redshift-stretching-mechanism',
      title: 'Where do the lines land?',
      teaches: 'Redshift is the arriving wavelength being stretched because the source recedes: faster recession gives a bigger shift, and the biggest shifts belong to the most distant galaxies.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#9a6b4f';
      var reduce = !!ctx.reducedMotion;
      var uid = 'rs' + Math.floor(Math.random() * 1e9);

      root.classList.add('svw-rs');
      if (!reduce) root.classList.add('rs-anim');
      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      /* ---------- header ---------- */
      var kick = h('p', 'rs-kick', 'Light from galaxies');
      kick.style.color = accent;
      root.appendChild(kick);
      root.appendChild(h('h3', 'rs-ttl', 'Where do the lines land?'));
      var frame = h('p', 'rs-frame', '');
      root.appendChild(frame);

      /* ---------- stage ---------- */
      var stage = h('div', 'rs-stage');
      var s = svg('svg', {
        'class': 'rs-svg', viewBox: '0 0 300 90',
        preserveAspectRatio: 'xMidYMid meet', role: 'img'
      });
      var sTitle = svg('title', {}); sTitle.textContent = 'Spectra';
      s.appendChild(sTitle);

      var defs = svg('defs', {});
      var grad = svg('linearGradient', { id: uid + '-g', x1: '0', x2: '1', y1: '0', y2: '0' });
      [[400, '#4a2a86'], [440, '#2f3cbd'], [480, '#1a7fb6'], [505, '#169a84'],
       [530, '#3aa53c'], [560, '#9db32c'], [580, '#d6c223'], [605, '#df911f'],
       [632, '#d0511e'], [660, '#b8271c'], [700, '#7c1512'], [720, '#5a0f0d']
      ].forEach(function (st) {
        grad.appendChild(svg('stop', {
          offset: ((st[0] - LAM0) / (LAM1 - LAM0) * 100).toFixed(2) + '%', 'stop-color': st[1]
        }));
      });
      defs.appendChild(grad);
      s.appendChild(defs);

      function makeStrip(label) {
        var g = svg('g', {});
        var lab = svg('text', {
          x: X0, y: 8, 'font-size': 11, 'font-weight': 600, fill: '#5b564e',
          'font-family': 'Inter, system-ui, sans-serif'
        });
        lab.textContent = label;
        g.appendChild(lab);
        g.appendChild(svg('rect', {
          x: X0, y: 12, width: X1 - X0, height: 18, rx: 2,
          fill: 'url(#' + uid + '-g)', stroke: '#cfc6b7', 'stroke-width': .8
        }));
        var ghosts = [], links = [];
        REST.forEach(function (nm) {
          var lk = svg('line', {
            x1: xOf(nm).toFixed(2), y1: 21, x2: xOf(nm).toFixed(2), y2: 21,
            stroke: '#fff', 'stroke-width': 1.3, 'stroke-linecap': 'round', 'stroke-opacity': .92
          });
          lk.style.display = 'none'; g.appendChild(lk); links.push(lk);
          var gh = svg('line', {
            x1: xOf(nm).toFixed(2), y1: 12, x2: xOf(nm).toFixed(2), y2: 30,
            stroke: '#fff', 'stroke-width': 1.3, 'stroke-dasharray': '2.4 2.4', 'stroke-opacity': .85
          });
          gh.style.display = 'none'; g.appendChild(gh); ghosts.push(gh);
        });
        var lines = [], nums = [];
        REST.forEach(function (nm) {
          var r = svg('rect', {
            'class': 'rs-line', x: (xOf(nm) - 1.6).toFixed(2), y: 12,
            width: 3.2, height: 18, fill: '#17161a',
            stroke: '#f7f3ec', 'stroke-width': .7, 'stroke-opacity': .75
          });
          g.appendChild(r); lines.push(r);
          var t = svg('text', {
            x: xOf(nm).toFixed(2), y: 39, 'font-size': 11, 'text-anchor': 'middle',
            fill: '#5b564e', 'font-family': 'Inter, system-ui, sans-serif'
          });
          t.textContent = nm;
          g.appendChild(t); nums.push(t);
        });
        s.appendChild(g);
        return { g: g, lab: lab, lines: lines, nums: nums, ghosts: ghosts, links: links };
      }

      var strip = [makeStrip('Measured in the lab'), makeStrip('Arriving from galaxy A'), makeStrip('Arriving from the galaxy')];
      stage.appendChild(s);
      root.appendChild(stage);

      /* ---------- controls ---------- */
      var KEYS = ['redsmall', 'redbig', 'blue', 'none', 'looksred', 'slower'];
      var opts = h('div', 'rs-opts');
      opts.setAttribute('role', 'group');
      var btn = KEYS.map(function (k) {
        var b = h('button', 'rs-opt');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        b.dataset.key = k;
        b.appendChild(h('span', 'rs-lbl', ''));
        b.appendChild(h('span', 'rs-tag', ''));
        b.addEventListener('click', function () { pick(k); });
        opts.appendChild(b);
        return b;
      });
      root.appendChild(opts);

      var row = h('div', 'rs-row');
      var run = h('p', 'rs-run', '');
      var go = h('button', 'rs-go', 'Check');
      go.type = 'button';
      go.disabled = true;
      go.addEventListener('click', onGo);
      row.appendChild(run); row.appendChild(go);
      root.appendChild(row);

      var cap = h('p', 'rs-cap', '');
      root.appendChild(cap);
      var sr = h('p', 'rs-sr', '');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* ---------- state ---------- */
      var st = {
        i: 0, round: null, choice: null, done: false,
        streak: 0, attempted: 0, mastered: false
      };
      var poolS = shuffled(SHIFTS), poolD = shuffled(PAIRS), pS = 0, pD = 0;

      function nextRound() {
        var wantDist = st.i >= 2 && st.i % 2 === 0;
        st.i++;
        if (wantDist) {
          if (pD >= poolD.length) { poolD = shuffled(PAIRS); pD = 0; }
          var p = poolD[pD++];
          return { kind: 'dist', a: p.a, b: p.b, ans: pairAnswer(p) };
        }
        if (pS >= poolS.length) { poolS = shuffled(SHIFTS); pS = 0; }
        var r = poolS[pS++];
        return {
          kind: 'shift', pm: r.pm, truth: bandOf(r.pm),
          small: r.small, big: r.big, blue: r.blue
        };
      }

      function setLines(sp, pm, show) {
        REST.forEach(function (nm, k) {
          var dx = xOf(nm * (1000 + pm) / 1000) - xOf(nm);
          sp.lines[k].style.transform = 'translateX(' + dx.toFixed(2) + 'px)';
          sp.lines[k].style.display = show ? '' : 'none';
          sp.nums[k].textContent = obsNm(nm, pm);
          sp.nums[k].setAttribute('x', xOf(obsNm(nm, pm)).toFixed(2));
          sp.nums[k].style.display = show ? '' : 'none';
        });
      }
      function resetLines(sp) {
        REST.forEach(function (nm, k) {
          sp.lines[k].style.transition = 'none';
          sp.lines[k].style.transform = 'translateX(0px)';
          sp.nums[k].textContent = nm;
          sp.nums[k].setAttribute('x', xOf(nm).toFixed(2));
        });
        /* force reflow so the next transform animates from zero */
        void s.getBoundingClientRect();
        REST.forEach(function (nm, k) { sp.lines[k].style.transition = ''; });
      }

      function layout(kind) {
        if (kind === 'shift') {
          strip[0].g.setAttribute('transform', 'translate(0,0)');
          strip[1].g.style.display = 'none';
          strip[2].g.setAttribute('transform', 'translate(0,47)');
          strip[2].lab.textContent = 'Arriving from the galaxy';
        } else {
          strip[0].g.setAttribute('transform', 'translate(0,0)');
          strip[1].g.style.display = '';
          strip[1].g.setAttribute('transform', 'translate(0,30)');
          strip[2].g.setAttribute('transform', 'translate(0,60)');
          strip[1].lab.textContent = 'Arriving from galaxy A';
          strip[2].lab.textContent = 'Arriving from galaxy B';
        }
        strip[2].g.style.display = '';
      }

      function label(i, text, tag) {
        btn[i].firstChild.textContent = text;
        btn[i].lastChild.textContent = tag || '';
      }

      function startRound() {
        var r = st.round = nextRound();
        st.choice = null; st.done = false;
        strip.forEach(function (sp) {
          sp.ghosts.forEach(function (n) { n.style.display = 'none'; });
          sp.links.forEach(function (n) { n.style.display = 'none'; });
        });
        go.textContent = 'Check';
        go.disabled = true;

        btn.forEach(function (b) {
          b.disabled = false;
          b.setAttribute('aria-pressed', 'false');
          b.classList.remove('is-key', 'is-yours');
          b.lastChild.textContent = '';
          b.style.display = '';
        });

        layout(r.kind);
        resetLines(strip[2]);

        if (r.kind === 'shift') {
          strip[0].nums.forEach(function (t) { t.style.display = ''; });
          setLines(strip[2], 0, false);
          strip[2].g.style.opacity = '.5';
          frame.textContent = frameShift(r);
          label(0, 'Small move towards red — ' + obsNm(HEAD, r.small) + ' nm');
          label(1, 'Big move towards red — ' + obsNm(HEAD, r.big) + ' nm');
          label(2, 'Move towards blue — ' + obsNm(HEAD, -r.blue) + ' nm');
          label(3, 'No move — lines stay at ' + HEAD + ' nm');
          label(4, 'The galaxy itself turns red');
          label(5, 'The light arrives more slowly');
          cap.innerHTML = 'The lab lines sit at 434 nm, 486 nm and ' + HEAD +
            ' nm. Light travels at 300,000 km/s.';
        } else {
          strip[0].nums.forEach(function (t) { t.style.display = 'none'; });
          strip[1].g.style.opacity = '1';
          strip[2].g.style.opacity = '1';
          setLines(strip[1], r.a, true);
          setLines(strip[2], r.b, true);
          strip[1].nums.forEach(function (t) { t.style.display = 'none'; });
          strip[2].nums.forEach(function (t) { t.style.display = 'none'; });
          strip[1].lab.textContent = 'Galaxy A';
          strip[2].lab.textContent = 'Galaxy B';
          frame.textContent = 'Hydrogen leaves the same dark lines wherever it is, so each galaxy’s ' +
            'light can be compared with the lab. Which of these two galaxies is farther away?';
          label(0, 'Galaxy A is farther');
          label(1, 'Galaxy B is farther');
          label(2, 'Both are the same distance');
          label(3, 'You cannot tell from the shift');
          btn[4].style.display = 'none';
          btn[5].style.display = 'none';
          cap.innerHTML = 'Both galaxies contain hydrogen, so the light left each of them with its ' +
            'lines at 434 nm, 486 nm and ' + HEAD + ' nm.';
        }
        showRun();
        sr.textContent = frame.textContent;
        publish();
      }

      var PREMISE = 'Hydrogen leaves the same dark lines wherever it is, so a shift against the ' +
        'lab reveals how a galaxy moves. ';

      function frameShift(r) {
        if (r.truth === 'none') {
          return PREMISE + 'This one neither approaches nor recedes — where do its lines land?';
        }
        if (r.truth === 'blue') {
          return PREMISE + 'This one approaches us at ' + group(speedKms(r.pm)) +
            ' km/s — where do its lines land?';
        }
        return PREMISE + 'This one recedes ' + (r.truth === 'redbig' ? 'fast' : 'slowly') + ', at ' +
          group(speedKms(r.pm)) + ' km/s — where do its lines land?';
      }

      function pick(k) {
        if (st.done) return;
        st.choice = k;
        btn.forEach(function (b) {
          b.setAttribute('aria-pressed', b.dataset.key === k ? 'true' : 'false');
        });
        go.disabled = false;
        sr.textContent = 'Selected: ' + btn.filter(function (b) { return b.dataset.key === k; })[0].firstChild.textContent;
        publish();
      }

      function keyOf(r) {
        if (r.kind === 'shift') return r.truth;
        return r.ans === 'A' ? 'redsmall' : (r.ans === 'B' ? 'redbig' : 'blue');
      }

      function onGo() {
        if (st.done) { startRound(); return; }
        if (!st.choice) return;
        var r = st.round, ok;
        if (r.kind === 'shift') {
          ok = st.choice === r.truth;
        } else {
          ok = st.choice === keyOf(r);
        }
        st.done = true;
        st.attempted++;
        st.streak = ok ? st.streak + 1 : 0;
        var justMastered = false;
        if (ok && st.streak >= 3 && !st.mastered) { st.mastered = true; justMastered = true; }

        btn.forEach(function (b) {
          b.disabled = true;
          if (b.dataset.key === keyOf(r)) { b.classList.add('is-key'); b.lastChild.textContent = 'right'; }
          if (b.dataset.key === st.choice) {
            b.classList.add('is-yours');
            if (!ok) b.lastChild.textContent = 'yours';
          }
        });

        if (r.kind === 'shift') {
          strip[2].g.style.opacity = '1';
          setLines(strip[2], r.pm, true);
          if (r.pm !== 0) {
            REST.forEach(function (nm, k) {
              strip[2].links[k].setAttribute('x2', xOf(nm * (1000 + r.pm) / 1000).toFixed(2));
              strip[2].links[k].style.display = '';
              strip[2].ghosts[k].style.display = '';
            });
          }
        } else {
          strip[1].lab.textContent = 'Galaxy A arrives at ' + obsNm(HEAD, r.a) + ' nm' +
            (r.ans === 'A' ? ' (the farther one)' : (r.ans === 'same' ? ' (same shift)' : ''));
          strip[2].lab.textContent = 'Galaxy B arrives at ' + obsNm(HEAD, r.b) + ' nm' +
            (r.ans === 'B' ? ' (the farther one)' : (r.ans === 'same' ? ' (same shift)' : ''));
        }

        var msg = justMastered ? masteryText(r) : (r.kind === 'shift' ? shiftText(r, ok) : distText(r, ok));
        cap.innerHTML = msg;
        sr.textContent = cap.textContent;
        go.textContent = st.mastered ? 'Another anyway' : 'Next galaxy';
        showRun();
        publish();
      }

      function showRun() {
        if (st.mastered) { run.textContent = 'Three in a row — you have it.'; return; }
        if (st.streak === 0) { run.textContent = st.attempted ? 'Run reset — three in a row to go.' : ''; return; }
        if (st.streak === 1) { run.textContent = '1 right in a row.'; return; }
        run.textContent = st.streak + ' right in a row — one more and you have it.';
      }

      /* ---------- feedback ---------- */
      function ok(t) { return '<b class="ok">Right —</b> ' + t; }
      function no(t) { return '<b>Not quite —</b> ' + t; }

      function shiftText(r, correct) {
        var o = obsNm(HEAD, r.pm), v = group(speedKms(r.pm)), f = pctTxt(r.pm), c = st.choice;
        if (correct) {
          if (r.truth === 'redbig') {
            return ok('a big shift towards the red end. Receding at ' + v + ' km/s stretches every ' +
              'wavelength by ' + f + ', so ' + HEAD + ' nm arrives as ' + o + ' nm. The light still travels at 3.0 × 10⁸ m/s.');
          }
          if (r.truth === 'redsmall') {
            return ok('a small shift towards the red end. ' + v + ' km/s is only ' + f + ' of the speed ' +
              'of light, so ' + HEAD + ' nm arrives as ' + o + ' nm. Slower recession, smaller stretch.');
          }
          if (r.truth === 'blue') {
            return ok('a shift towards the blue end. Approaching at ' + v + ' km/s squeezes each ' +
              'wavelength by ' + f + ', so ' + HEAD + ' nm arrives as ' + o + ' nm — shorter wavelength, higher frequency.');
          }
          return ok('the lines stay put. With no motion towards or away, each crest sets off from ' +
            'the same distance, so ' + HEAD + ' nm arrives as ' + HEAD + ' nm. No stretch, no squeeze.');
        }
        if (c === 'slower') {
          return no('you said the light arrives more slowly. It does not — light from every galaxy ' +
            'arrives at 3.0 × 10⁸ m/s. ' + (r.pm === 0
              ? 'Here nothing changed at all: ' + HEAD + ' nm left and ' + HEAD + ' nm arrived.'
              : 'The wavelength changed, not the speed: ' + HEAD + ' nm left, ' + o + ' nm arrived.'));
        }
        if (c === 'looksred') {
          return no('you said the galaxy itself turns red. Nothing is dyed red. ' + (r.pm > 0
            ? 'The dark lines slide towards the red end — ' + HEAD + ' nm arriving as ' + o +
              ' nm. The pattern moves, the colour of the galaxy does not.'
            : (r.pm < 0
              ? 'These lines slide the other way, towards blue: ' + HEAD + ' nm arrives as ' + o + ' nm.'
              : 'These lines do not move at all: ' + HEAD + ' nm arrives as ' + HEAD + ' nm.')));
        }
        if ((c === 'redsmall' || c === 'redbig') && (r.truth === 'redsmall' || r.truth === 'redbig')) {
          return no('you said a ' + (c === 'redbig' ? 'big' : 'small') + ' shift towards red. Direction ' +
            'right, size wrong: ' + v + ' km/s is ' + f + ' of the speed of light, so ' + HEAD +
            ' nm arrives as ' + o + ' nm. Faster recession, bigger stretch.');
        }
        if (c === 'redsmall' || c === 'redbig') {
          return no('you said the lines shift towards red. Red means a longer wavelength, which ' +
            'happens when the source recedes. ' + (r.pm === 0
              ? 'This galaxy does neither, so ' + HEAD + ' nm arrives as ' + HEAD + ' nm.'
              : 'This one approaches at ' + v + ' km/s, so ' + HEAD + ' nm arrives as ' + o + ' nm.'));
        }
        if (c === 'blue') {
          return no('you said the lines shift towards blue. Blue means a shorter wavelength, which ' +
            'happens when a source approaches. ' + (r.pm === 0
              ? 'This galaxy is doing neither, so ' + HEAD + ' nm arrives as ' + HEAD + ' nm.'
              : 'This one recedes at ' + v + ' km/s, so ' + HEAD + ' nm arrives as ' + o + ' nm.'));
        }
        return no('you said the lines stay put. They only stay put when a galaxy is neither ' +
          'approaching nor receding. This one moves at ' + v + ' km/s, so ' + HEAD + ' nm arrives as ' + o + ' nm.');
      }

      function distText(r, correct) {
        var oa = obsNm(HEAD, r.a), ob = obsNm(HEAD, r.b);
        var fa = pctTxt(r.a), fb = pctTxt(r.b);
        var far = r.ans, big = far === 'A' ? 'A' : 'B', small = far === 'A' ? 'B' : 'A';
        var c = st.choice;
        if (correct) {
          if (far === 'same') {
            return ok('the same distance. Both sets of lines are shifted by ' + fa + ' — ' + HEAD +
              ' nm arriving as ' + oa + ' nm for each. Equal redshift, equal recession speed, equal distance.');
          }
          return ok('Galaxy ' + big + ' is farther. Its lines shift ' + (far === 'A' ? fa : fb) +
            ' against ' + (far === 'A' ? fb : fa) + ', so it recedes faster — and the faster a galaxy ' +
            'recedes, the farther away it is. That link is the evidence the universe is expanding.');
        }
        if (c === 'blue') {
          return no('you said the same distance. The shifts differ — ' + fa + ' for A against ' + fb +
            ' for B — so they are not receding at the same speed. Galaxy ' + big +
            ' has the bigger redshift, so Galaxy ' + big + ' is farther.');
        }
        if (c === 'none') {
          return no('you said you cannot tell from the shift. For distant galaxies it can: a bigger redshift ' +
            'means faster recession, and faster recession means greater distance. ' + (far === 'same'
              ? 'Here both shift by ' + fa + ', so both are the same distance.'
              : 'Here Galaxy ' + big + ' shifts more, so Galaxy ' + big + ' is farther.'));
        }
        var said = c === 'redsmall' ? 'A' : 'B';
        if (far === 'same') {
          return no('you said Galaxy ' + said + '. Both sets of lines are shifted by the same ' + fa +
            ', so both galaxies recede at ' + group(speedKms(r.a)) + ' km/s — same speed, same distance.');
        }
        return no('you said Galaxy ' + said + '. Galaxy A shifts ' + fa + ' and Galaxy B shifts ' + fb +
          ': the bigger redshift belongs to Galaxy ' + big + ', so Galaxy ' + big + ' recedes faster and is the farther one.');
      }

      function masteryText(r) {
        var tail = r.kind === 'shift' && r.pm !== 0
          ? HEAD + ' nm arrived here as ' + obsNm(HEAD, r.pm) + ' nm. '
          : '';
        return ok('three in a row, you have it. A receding source stretches the wavelength that ' +
          'arrives — ' + tail + 'the lines slide towards the red end while the light keeps its ' +
          'speed. Bigger shift, faster recession, and for distant galaxies, greater distance.');
      }

      /* ---------- test surface ---------- */
      function publish() {
        var r = st.round;
        root.dataset.svState = JSON.stringify({
          kind: r ? r.kind : null,
          shiftPm: r ? (r.kind === 'shift' ? r.pm : [r.a, r.b]) : null,
          answer: r ? keyOf(r) : null,
          choice: st.choice,
          correct: st.done ? st.choice === keyOf(r) : null,
          streak: st.streak,
          mastered: st.mastered,
          attempted: st.attempted
        });
      }

      root.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !st.done && st.choice) {
          st.choice = null;
          btn.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
          go.disabled = true;
          publish();
        }
      });

      startRound();
    }
  };
})();
