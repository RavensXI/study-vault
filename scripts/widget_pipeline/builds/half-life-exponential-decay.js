/* Half-life and exponential decay -------------------------------------
   Makes concrete: each half-life halves what is LEFT, so the fall gets
   smaller every time and the sample never reaches zero. The linear
   picture ("all gone after two half-lives") is always on the answer
   list, so the misconception can be committed and then falsified.
   Self-contained: no imports, no network, no storage. -------------- */
(function () {
  'use strict';

  var ID = 'half-life-exponential-decay';
  var COLS = 5;            /* 0..4 half-lives on the chart */
  var TARGET_RUN = 3;      /* mastery exit */

  /* Every start is divisible by 2^(k+1) so every figure on screen is a
     whole number of nuclei. Counts are abstract on purpose: a real
     activity in Bq for 800 nuclei would not be defensible. */
  var ROUNDS = [
    { S: 800,  T: 3,  k: 2, u: 'days',    su: 'd'   },
    { S: 2400, T: 5,  k: 3, u: 'hours',   su: 'h'   },
    { S: 640,  T: 20, k: 4, u: 'minutes', su: 'min' },
    { S: 960,  T: 2,  k: 3, u: 'years',   su: 'yr'  },
    { S: 1600, T: 6,  k: 4, u: 'hours',   su: 'h'   },
    { S: 1200, T: 8,  k: 2, u: 'days',    su: 'd'   }
  ];

  var ARROW = ' → ';
  var DASH = ' — ';

  function pow2(n) { return Math.pow(2, n); }
  function left(S, i) { return S / pow2(i); }

  /* Options always contain the exponential answer and the linear one
     (0 = "it has all gone"), plus real, diagnosable confusions. */
  function optionsFor(S, k) {
    var correct = left(S, k);
    var want = [0, correct];
    var extra = [S / 2, left(S, k - 1), S - correct, left(S, k + 1)];
    for (var i = 0; i < extra.length && want.length < 5; i++) {
      var v = extra[i];
      if (v >= 0 && v === Math.round(v) && want.indexOf(v) === -1) want.push(v);
    }
    return want.sort(function (a, b) { return a - b; });
  }

  function chainText(S, k) {
    var parts = [];
    for (var i = 0; i <= k; i++) parts.push(left(S, i));
    return parts.join(ARROW);
  }

  function shuffled(n) {
    var a = [], i, j, t;
    for (i = 0; i < n; i++) a.push(i);
    for (i = n - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1));
      t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  var CSS = [
    '.svw-hlx{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45}',
    '.svw-hlx *{box-sizing:border-box}',
    '.svw-hlx-kicker{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .1rem}',
    '.svw-hlx-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.15rem;margin:0 0 .35rem;letter-spacing:-.01em}',
    '.svw-hlx-frame{font-size:.86rem;margin:0 0 .7rem;color:#3c382f}',
    '.svw-hlx-frame b{font-weight:600;font-variant-numeric:tabular-nums}',
    '.svw-hlx-chart{display:flex;gap:6px;height:112px;align-items:flex-end}',
    '.svw-hlx-col{flex:1 1 0;position:relative;height:100%;background:#faf8f5;border:1px solid #e8e2d9;border-radius:6px}',
    '.svw-hlx-col.is-ask{border-color:#b9b0a2;background:#f6f2eb}',
    '.svw-hlx-fill{position:absolute;left:0;right:0;bottom:0;height:0;min-height:0;border-radius:5px;transition:height .45s cubic-bezier(.16,1,.3,1)}',
    '.svw-hlx-still .svw-hlx-fill{transition:none}',
    '.svw-hlx-mark{position:absolute;left:0;right:0;bottom:0;border-top:2px dashed #6f6a62;display:none}',
    '.svw-hlx-mark span{position:absolute;right:2px;font-size:.68rem;font-weight:600;color:#3c382f;background:#fff;border:1px solid #ddd7cd;border-radius:4px;padding:0 3px;white-space:nowrap;font-variant-numeric:tabular-nums}',
    '.svw-hlx-mark.is-low span{bottom:3px}',
    '.svw-hlx-mark.is-high span{top:3px}',
    '.svw-hlx-axis{display:flex;gap:6px;margin:.3rem 0 .8rem}',
    '.svw-hlx-cell{flex:1 1 0;text-align:center;overflow:hidden}',
    '.svw-hlx-cell .t{display:block;font-size:.68rem;color:#8d8880;white-space:nowrap;font-variant-numeric:tabular-nums}',
    '.svw-hlx-cell .n{display:block;font-size:.74rem;font-weight:600;min-height:1.05rem;white-space:nowrap;font-variant-numeric:tabular-nums}',
    '.svw-hlx-cell.is-ask .t{color:#3c382f;font-weight:600}',
    '.svw-hlx-opts{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px}',
    '.svw-hlx-opt{font:600 .84rem Inter,system-ui,sans-serif;font-variant-numeric:tabular-nums;padding:.5rem .3rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;text-align:center}',
    '.svw-hlx-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-hlx-opt[disabled]{cursor:default;opacity:.5}',
    '.svw-hlx-opt.is-key[disabled]{opacity:1;border-color:#4f7d63;color:#3f6b53;background:#fff}',
    '.svw-hlx-row{display:flex;align-items:center;gap:.6rem;margin:.7rem 0 0}',
    '.svw-hlx-go{font:600 .84rem Inter,system-ui,sans-serif;padding:.52rem 1rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-hlx-go[disabled]{opacity:.4;cursor:default}',
    '.svw-hlx-run{margin-left:auto;text-align:right;font-size:.74rem;color:#8d8880}',
    '.svw-hlx-cap{font-size:.84rem;line-height:1.5;color:#3c382f;margin:.65rem 0 0;min-height:92px}',
    '.svw-hlx-cap b{font-weight:600;font-variant-numeric:tabular-nums}',
    '.svw-hlx-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;margin:-1px;padding:0;border:0}'
  ].join('\n');

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  window.SVWidget = {
    meta: {
      id: ID,
      title: 'Half-life: how much is left?',
      teaches: 'Each half-life halves the remaining nuclei, so decay is exponential and never reaches zero.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
                   ctx.accent || '#8a6a4f';
      var still = !!ctx.reducedMotion;

      root.textContent = '';
      var wrap = el('div', 'svw-hlx' + (still ? ' svw-hlx-still' : ''));
      var style = el('style');
      style.textContent = CSS;
      wrap.appendChild(style);

      var kicker = el('p', 'svw-hlx-kicker', 'Radioactive decay');
      kicker.style.color = accent;
      wrap.appendChild(kicker);
      wrap.appendChild(el('h3', 'svw-hlx-title', 'Half-life'));

      var frame = el('p', 'svw-hlx-frame');
      wrap.appendChild(frame);

      /* stage: one chart, five columns, one shared time axis */
      var chart = el('div', 'svw-hlx-chart');
      var axis = el('div', 'svw-hlx-axis');
      var cols = [], fills = [], cells = [], times = [], counts = [], i;
      for (i = 0; i < COLS; i++) {
        var col = el('div', 'svw-hlx-col');
        var fill = el('div', 'svw-hlx-fill');
        fill.style.background = accent;
        col.appendChild(fill);
        chart.appendChild(col);
        cols.push(col); fills.push(fill);

        var cell = el('div', 'svw-hlx-cell');
        var t = el('span', 't');
        var n = el('span', 'n');
        cell.appendChild(t); cell.appendChild(n);
        axis.appendChild(cell);
        cells.push(cell); times.push(t); counts.push(n);
      }
      var mark = el('div', 'svw-hlx-mark');
      var markLabel = el('span');
      mark.appendChild(markLabel);
      wrap.appendChild(chart);
      wrap.appendChild(axis);

      var opts = el('div', 'svw-hlx-opts');
      var btns = [];
      for (i = 0; i < 5; i++) {
        var b = el('button', 'svw-hlx-opt');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        opts.appendChild(b);
        btns.push(b);
      }
      wrap.appendChild(opts);

      var row = el('div', 'svw-hlx-row');
      var go = el('button', 'svw-hlx-go', 'Check');
      go.type = 'button';
      var run = el('p', 'svw-hlx-run', '');
      row.appendChild(go);
      row.appendChild(run);
      wrap.appendChild(row);

      var cap = el('p', 'svw-hlx-cap');
      wrap.appendChild(cap);
      var sr = el('p', 'svw-hlx-sr');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      root.appendChild(wrap);

      /* ---- state ---- */
      var order = shuffled(ROUNDS.length);
      var ptr = 0;
      var R = null, values = [], picked = null, committed = false;
      var streak = 0, mastered = false, attempted = 0, roundNo = 0, wasRight = null;

      var OPENING = 'Which nucleus decays next is random' + DASH +
        'half-life describes the whole sample, not any single nucleus.';

      function pushState() {
        root.dataset.svState = JSON.stringify({
          id: ID,
          round: roundNo,
          start: R.S,
          halfLife: R.T,
          unit: R.u,
          halfLivesAsked: R.k,
          remaining: left(R.S, R.k),
          picked: picked,
          committed: committed,
          right: wasRight,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      function setRun() {
        if (!attempted) { run.textContent = ''; return; }
        if (streak >= TARGET_RUN) run.textContent = 'You have it';
        else if (streak === 2) run.textContent = '2 in a row' + DASH + 'one more';
        else if (streak === 1) run.textContent = '1 in a row';
        else run.textContent = 'Run back to zero';
      }

      function newRound() {
        R = ROUNDS[order[ptr % order.length]];
        ptr++;
        roundNo++;
        picked = null;
        committed = false;
        wasRight = null;
        values = optionsFor(R.S, R.k);

        frame.innerHTML = 'A sample contains <b>' + R.S +
          '</b> undecayed nuclei of an isotope with a half-life of <b>' +
          R.T + ' ' + R.u + '</b>. How many undecayed nuclei remain after <b>' +
          (R.T * R.k) + ' ' + R.u + '</b>?';

        for (var i = 0; i < COLS; i++) {
          times[i].textContent = i === 0 ? '0' : (R.T * i) + ' ' + R.su;
          counts[i].textContent = i === 0 ? String(R.S) : '';
          fills[i].style.height = i === 0 ? '100%' : '0%';
          fills[i].style.minHeight = i === 0 ? '3px' : '0';
          fills[i].style.transitionDelay = '0ms';
          if (i === R.k) { cols[i].className = 'svw-hlx-col is-ask'; cells[i].className = 'svw-hlx-cell is-ask'; }
          else { cols[i].className = 'svw-hlx-col'; cells[i].className = 'svw-hlx-cell'; }
        }
        if (mark.parentNode) mark.parentNode.removeChild(mark);
        mark.style.display = 'none';

        for (var j = 0; j < btns.length; j++) {
          var b = btns[j];
          if (j < values.length) {
            b.textContent = String(values[j]);
            b.style.display = '';
            b.disabled = false;
            b.className = 'svw-hlx-opt';
            b.setAttribute('aria-pressed', 'false');
          } else {
            b.style.display = 'none';
            b.disabled = true;
          }
        }

        go.textContent = 'Check';
        go.disabled = true;
        cap.textContent = OPENING;
        setRun();
        pushState();
      }

      function pick(v, b) {
        if (committed) return;
        picked = v;
        for (var j = 0; j < btns.length; j++) {
          btns[j].setAttribute('aria-pressed', btns[j] === b ? 'true' : 'false');
        }
        go.disabled = false;
        pushState();
      }

      function verdictHtml(a) {
        var S = R.S, k = R.k, T = R.T, u = R.u;
        var correct = left(S, k);
        var time = '<b>' + (T * k) + ' ' + u + '</b>';
        var ch = '<b>' + chainText(S, k) + '</b>';

        if (a === correct) {
          if (mastered && streak >= TARGET_RUN) {
            return 'Right' + DASH + '<b>' + correct + '</b> left, and three in a row: you have it. ' +
              'Each half-life halves <b>what remains</b>' + DASH + '<b>' + chainText(S, 4) + '</b>' + DASH +
              'so the drop gets smaller every time and the sample never reaches zero.';
          }
          return 'Right' + DASH + '<b>' + correct + '</b> undecayed nuclei left. ' +
            time + ' is ' + k + ' half-lives, so ' + ch +
            '. Each half-life halves what is left, not the starting amount, and the activity halves with it.';
        }

        var head = 'Not quite' + DASH + 'you said <b>' + a + '</b> undecayed nuclei. ';
        if (a === 0) {
          return head + 'After ' + time + ' (' + k + ' half-lives) <b>' + correct +
            '</b> are left: ' + ch + '. Halving applies to <b>what remains</b>, so the number lost shrinks each time and the sample never reaches zero.';
        }
        if (a === S - correct) {
          return head + 'That is how many have <b>decayed</b>. The question asks how many are still undecayed after ' +
            time + ': ' + ch + ', so <b>' + correct + '</b> are left.';
        }
        if (a === S / 2) {
          return head + 'That is the count after <b>one</b> half-life (' + T + ' ' + u + '). ' +
            time + ' is ' + k + ' half-lives, so keep halving what is left: ' + ch + '.';
        }
        if (a === left(S, k - 1)) {
          return head + 'That is where the sample is after <b>' + (k - 1) +
            '</b> half-lives. ' + time + ' gives ' + k + ', so halve the remainder once more: <b>' +
            a + ARROW + correct + '</b>.';
        }
        if (a === left(S, k + 1)) {
          return head + 'That is one half-life too far. ' + time + ' is ' + k + ' half-lives, not ' +
            (k + 1) + ': ' + ch + ' leaves <b>' + correct + '</b>.';
        }
        return head + 'After ' + time + ' (' + k + ' half-lives) <b>' + correct +
          '</b> are left: ' + ch + '. Each half-life halves what remains.';
      }

      function commit() {
        if (committed) { newRound(); return; }
        if (picked === null) return;

        committed = true;
        attempted++;
        var correct = left(R.S, R.k);
        wasRight = picked === correct;
        if (wasRight) {
          streak++;
          if (streak >= TARGET_RUN) mastered = true;
        } else {
          streak = 0;
        }

        /* reveal the whole decay, derived from the model, not authored */
        for (var i = 1; i < COLS; i++) {
          var v = left(R.S, i);
          counts[i].textContent = String(v);
          fills[i].style.minHeight = '3px';
          fills[i].style.transitionDelay = still ? '0ms' : (i * 70) + 'ms';
          fills[i].style.height = (v / R.S * 100) + '%';
        }

        /* the student's own committed number, on the column that was asked */
        var pct = Math.max(0, Math.min(100, picked / R.S * 100));
        mark.style.bottom = pct <= 0 ? '2px' : pct + '%';
        mark.className = 'svw-hlx-mark ' + (pct > 70 ? 'is-high' : 'is-low');
        markLabel.textContent = 'you ' + picked;
        mark.style.display = 'block';
        cols[R.k].appendChild(mark);

        for (var j = 0; j < values.length; j++) {
          btns[j].disabled = true;
          btns[j].className = 'svw-hlx-opt' + (values[j] === correct ? ' is-key' : '');
        }

        cap.innerHTML = verdictHtml(picked);
        sr.textContent = (wasRight ? 'Right. ' : 'Not quite. ') + 'You said ' + picked +
          '. ' + correct + ' undecayed nuclei remain after ' + (R.T * R.k) + ' ' + R.u + '.';
        go.textContent = mastered ? 'Another anyway' : 'Next question';
        go.disabled = false;
        setRun();
        pushState();
      }

      for (i = 0; i < btns.length; i++) {
        (function (b) {
          b.addEventListener('click', function () { pick(Number(b.textContent), b); });
        })(btns[i]);
      }

      go.addEventListener('click', function () {
        var advancing = committed;
        commit();
        if (advancing) {
          for (var j = 0; j < btns.length; j++) {
            if (!btns[j].disabled) { btns[j].focus(); break; }
          }
        }
      });

      newRound();
    }
  };
})();
