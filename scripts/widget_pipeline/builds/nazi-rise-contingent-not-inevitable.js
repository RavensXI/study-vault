/* Widget: nazi-rise-contingent-not-inevitable
   One stage (a bar chart of real election results), four prediction rounds.
   The student commits to a prediction, then the evidence reveals. */
(function () {
  'use strict';

  var ID = 'nazi-rise-contingent-not-inevitable';
  var C = 'svw-nrc';

  /* chart geometry, in px --------------------------------------------- */
  var PLOT = 112;   /* height of the plotting box            */
  var AREA = 88;    /* height available to a full-scale bar  */
  var DOMAIN = 55;  /* per cent at the top of the scale      */

  function px(v) { return Math.max(3, Math.round(v / DOMAIN * AREA)); }
  var MAJ = Math.round(50 / DOMAIN * AREA);

  /* rounds ------------------------------------------------------------- */
  var ROUNDS = [
    {
      id: 'nov-1932-direction',
      task: 'Each bar is the Nazi share of the Reichstag vote. In July 1932 it stood at 37.3%. Predict what the November 1932 election did to it.',
      note: 'The dashed line marks 50% — the share a party needs for a majority in the Reichstag.',
      cols: [
        { k: '1928', v: 2.6 },
        { k: '1930', v: 18.3 },
        { k: 'Jul 1932', v: 37.3 },
        { k: 'Nov 1932', v: 33.1, hidden: true, focus: true }
      ],
      right: 'Right — you said it fell back below 35%. It fell to 33.1%, down 4.2 points from July, and 34 seats went with it. Hitler was appointed eight weeks later with his vote in decline.',
      shortRight: 'the vote fell to 33.1%',
      options: [
        { label: 'Rose again, above 40%', ok: false, fb: 'Not quite — you said the vote rose above 40%. It fell to 33.1%: 34 seats lost and the party close to bankruptcy. The last free election before Hitler took office was a Nazi setback, not a surge.' },
        { label: 'Held steady, near 37%', ok: false, fb: 'Not quite — you said it held steady near 37%. It dropped to 33.1% and 34 seats went. Support was not a rising line that carried him into office — it was falling when he was appointed.' },
        { label: 'Fell back, below 35%', ok: true }
      ]
    },
    {
      id: 'presidency-1932',
      task: 'In April 1932 Hitler challenged President Hindenburg for the presidency. Predict the result of that run-off vote.',
      note: 'A presidential candidate needs more than half the run-off vote to win outright.',
      majRight: true,
      cols: [
        { k: 'Hindenburg', v: 53.0, hidden: true, focus: true },
        { k: 'Hitler', v: 36.8, hidden: true }
      ],
      right: 'Right — you said Hindenburg won it. He took 53.0% to Hitler’s 36.8% in the April run-off. Hitler polled 13 million votes and still lost by 16 points — national office never came to him by election.',
      shortRight: 'Hindenburg won, 53.0% to 36.8%',
      options: [
        { label: 'Hitler won it', ok: false, fb: 'Not quite — you said Hitler won it. Hindenburg took 53.0% to Hitler’s 36.8%. Thirteen million votes and still beaten by 16 points: Hitler never won a national office at the ballot box.' },
        { label: 'A dead heat, too close to call', ok: false, fb: 'Not quite — you said it was too close to call. Hindenburg won it clearly, 53.0% to 36.8%. Hitler’s 13 million votes alarmed the elite, but he lost the presidency by 16 points.' },
        { label: 'Hindenburg won it', ok: true }
      ]
    },
    {
      id: 'how-he-took-office',
      task: 'Hitler became Chancellor on 30 January 1933, eight weeks after the November result. Predict how he got the job.',
      note: 'These are every free Reichstag election the party fought before he took office.',
      mark: '30 Jan 1933 · Chancellor',
      cols: [
        { k: '1928', v: 2.6 },
        { k: '1930', v: 18.3 },
        { k: 'Jul 1932', v: 37.3 },
        { k: 'Nov 1932', v: 33.1, focus: true }
      ],
      right: 'Right — you said the President appointed him. Hindenburg signed him in on 30 January 1933 after private talks with Papen, who thought the conservatives could box Hitler in. No vote put him there.',
      shortRight: 'the President appointed him',
      options: [
        { label: 'He won the November election', ok: false, fb: 'Not quite — you said he won the November election. The Nazis came first on 33.1%, which is not a majority, and no election makes anyone Chancellor. Hindenburg appointed him on 30 January 1933.' },
        { label: 'He seized power by force', ok: false, fb: 'Not quite — you said he seized power by force. Force was tried in Munich in 1923 and failed. In 1933 the office was handed over: Hindenburg appointed him after Papen brokered a deal.' },
        { label: 'The President appointed him', ok: true }
      ]
    },
    {
      id: 'best-free-share',
      task: 'The Nazis fought four free Reichstag elections. Predict the highest share they ever won in one of them.',
      note: 'The dashed line marks 50% — the share a party needs for a majority in the Reichstag.',
      cols: [
        { k: '1928', v: 2.6, hidden: true },
        { k: '1930', v: 18.3, hidden: true },
        { k: 'Jul 1932', v: 37.3, hidden: true, focus: true },
        { k: 'Nov 1932', v: 33.1, hidden: true },
        { k: 'Mar 1933', v: 43.9, dim: true, note: 'not free', late: true }
      ],
      right: 'Right — you said about 37%. July 1932 was the ceiling: 37.3%. March 1933 reached 43.9%, but only after the Reichstag fire decree jailed opponents — and even that was short of a majority.',
      shortRight: 'the peak was 37.3%, in July 1932',
      options: [
        { label: 'Over 50% — a majority', ok: false, fb: 'Not quite — you said over 50%. The best free result was 37.3% in July 1932. Even the 43.9% of March 1933, with opponents jailed and the SA on the streets, fell short of a majority.' },
        { label: 'About 44%', ok: false, fb: 'Not quite — you said about 44%. That is March 1933 — 43.9% — polled after the Reichstag fire decree with opponents jailed, so not a free election. The best free result was 37.3%, in July 1932.' },
        { label: 'About 37%', ok: true }
      ]
    }
  ];

  var CSS =
    '.' + C + '{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}' +
    '.' + C + ' *{box-sizing:border-box}' +
    '.' + C + ' .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .18rem}' +
    '.' + C + ' .t{font-family:"Source Serif 4",Georgia,serif;font-size:1.15rem;font-weight:600;line-height:1.2;margin:0 0 .3rem}' +
    '.' + C + ' .task{font-size:.84rem;line-height:1.45;color:#4a453d;margin:0 0 .55rem}' +
    '.' + C + ' .stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem .6rem .3rem;margin:0 0 .6rem}' +
    '.' + C + ' .plot{position:relative;display:flex;align-items:flex-end;gap:.4rem;height:' + PLOT + 'px}' +
    '.' + C + ' .col{flex:1 1 0;min-width:0;display:flex;flex-direction:column;justify-content:flex-end}' +
    '.' + C + ' .val{font-size:.7rem;font-weight:600;text-align:center;line-height:1.15;margin-bottom:2px;font-variant-numeric:tabular-nums;color:#5b564e}' +
    '.' + C + ' .bar{background:#d9d2c6;border-radius:3px 3px 0 0}' +
    '.' + C + ' .bar.hid{background:transparent;border:1px dashed #cfc7ba;border-bottom:0}' +
    '.' + C + ' .bar.dim{background:#ece6db;border:1px dashed #cfc7ba;border-bottom:0}' +
    '.' + C + ' .maj{position:absolute;left:0;right:0;bottom:' + MAJ + 'px;border-top:1px dashed #c9c1b4}' +
    '.' + C + ' .majl{position:absolute;left:0;bottom:' + (MAJ + 2) + 'px;font-size:.66rem;color:#8d8880;background:#faf8f5;padding:0 3px}' +
    '.' + C + ' .majl.r{left:auto;right:0}' +
    '.' + C + ' .mark{position:absolute;right:0;top:0;display:flex;align-items:center;gap:5px;font-size:.66rem;font-weight:600}' +
    '.' + C + ' .mark i{width:7px;height:7px;border-radius:50%;display:block}' +
    '.' + C + ' .conn{position:absolute;width:0;border-left:1px dashed #b8ae9e}' +
    '.' + C + ' .xrow{display:flex;gap:.4rem;height:30px;margin-top:5px}' +
    '.' + C + ' .x{flex:1 1 0;min-width:0;text-align:center;font-size:.66rem;color:#8d8880;line-height:1.25}' +
    '.' + C + ' .x b{font-weight:600;color:#5b564e}' +
    '.' + C + ' .x span{display:block;color:#a8a29a}' +
    '.' + C + ' .opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(178px,1fr));gap:.4rem;margin:0 0 .5rem}' +
    '.' + C + ' .o{font-family:inherit;font-size:.82rem;font-weight:600;line-height:1.25;text-align:left;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.45rem .6rem;cursor:pointer}' +
    '.' + C + ' .o[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}' +
    '.' + C + ' .o.ok{background:#4f7d6318;border-color:#4f7d63;color:#2d2a26}' +
    '.' + C + ' .o[disabled]{cursor:default}' +
    '.' + C + ' .act{display:flex;align-items:center;gap:.55rem;margin:0 0 .5rem}' +
    '.' + C + ' .go{font-family:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.5rem .95rem;cursor:pointer}' +
    '.' + C + ' .go[disabled]{opacity:.4;cursor:default}' +
    '.' + C + ' .run{font-size:.74rem;color:#8d8880;font-variant-numeric:tabular-nums}' +
    '.' + C + ' .cap{font-size:.84rem;line-height:1.5;margin:0;border-top:1px solid #efe9e0;padding-top:.5rem;min-height:58px}' +
    '.' + C + ' .sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}' +
    '.' + C + '.mo .bar{transition:height .45s cubic-bezier(.16,1,.3,1)}';

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  window.SVWidget = {
    meta: {
      id: ID,
      title: 'The road to 30 January 1933',
      teaches: 'The Nazi rise was contingent: the vote was falling before Hitler was appointed, and no free election gave the party a majority.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = (ctx.accent || '').trim();
      try {
        var v = getComputedStyle(root).getPropertyValue('--accent').trim();
        if (v) accent = v;
      } catch (e) { /* keep ctx.accent */ }
      if (!/^#[0-9a-f]{6}$/i.test(accent)) accent = '#8a6a4f';
      var motion = !ctx.reducedMotion;

      root.classList.add(C);
      if (motion) root.classList.add('mo');
      var style = el('style');
      style.textContent = CSS;
      root.appendChild(style);

      var kick = el('p', 'k', 'Germany 1928–1933');
      kick.style.color = accent;
      root.appendChild(kick);
      root.appendChild(el('h3', 't', 'The road to 30 January 1933'));

      var task = el('p', 'task');
      root.appendChild(task);

      /* --- one stage: the chart ---------------------------------------- */
      var stage = el('div', 'stage');
      var plot = el('div', 'plot');
      var maj = el('div', 'maj');
      var majl = el('div', 'majl', '50% = majority');
      var conn = el('div', 'conn');
      var mark = el('div', 'mark');
      var markT = el('span');
      var markD = el('i');
      markD.style.background = accent;
      mark.appendChild(markT);
      mark.appendChild(markD);
      mark.style.color = accent;

      var cols = [], i;
      for (i = 0; i < 5; i++) {
        var col = el('div', 'col');
        var val = el('div', 'val');
        var bar = el('div', 'bar');
        col.appendChild(val);
        col.appendChild(bar);
        plot.appendChild(col);
        cols.push({ col: col, val: val, bar: bar });
      }
      plot.appendChild(maj);
      plot.appendChild(majl);
      plot.appendChild(conn);
      plot.appendChild(mark);
      stage.appendChild(plot);

      var xrow = el('div', 'xrow');
      var xs = [];
      for (i = 0; i < 5; i++) {
        var x = el('div', 'x');
        var xb = el('b');
        var xn = el('span');
        x.appendChild(xb);
        x.appendChild(xn);
        xrow.appendChild(x);
        xs.push({ x: x, b: xb, n: xn });
      }
      stage.appendChild(xrow);
      root.appendChild(stage);

      /* --- controls ---------------------------------------------------- */
      var opts = el('div', 'opts');
      var obtn = [];
      for (i = 0; i < 3; i++) {
        var b = el('button', 'o');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        opts.appendChild(b);
        obtn.push(b);
      }
      root.appendChild(opts);

      var act = el('div', 'act');
      var go = el('button', 'go', 'Check the result');
      go.type = 'button';
      go.disabled = true;
      var run = el('span', 'run', '');
      act.appendChild(go);
      act.appendChild(run);
      root.appendChild(act);

      var cap = el('p', 'cap');
      root.appendChild(cap);
      var sr = el('p', 'sr');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* --- state ------------------------------------------------------- */
      var order = shuffle([0, 1, 2, 3]);
      var seat = 0;
      var round = null, shown = null, picked = -1, committed = false;
      var streak = 0, mastered = false, attempted = 0;

      function shuffle(a) {
        for (var j = a.length - 1; j > 0; j--) {
          var k = Math.floor(Math.random() * (j + 1));
          var t = a[j]; a[j] = a[k]; a[k] = t;
        }
        return a;
      }

      function state(correct) {
        root.dataset.svState = JSON.stringify({
          round: round.id,
          picked: picked < 0 ? null : shown[picked].label,
          committed: committed,
          correct: correct == null ? null : correct,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      function drawCols(reveal) {
        var list = round.cols.filter(function (c) { return !c.late || reveal; });
        for (var j = 0; j < 5; j++) {
          var c = list[j];
          if (!c) {
            cols[j].col.style.display = 'none';
            xs[j].x.style.display = 'none';
            continue;
          }
          cols[j].col.style.display = '';
          xs[j].x.style.display = '';
          var hide = c.hidden && !reveal;
          cols[j].val.textContent = hide ? '?' : c.v.toFixed(1) + '%';
          cols[j].bar.className = 'bar' + (hide ? ' hid' : (c.dim ? ' dim' : ''));
          cols[j].bar.style.height = (hide ? 22 : px(c.v)) + 'px';
          cols[j].bar.style.background = (!hide && c.focus) ? accent : '';
          xs[j].b.textContent = c.k;
          xs[j].n.textContent = (reveal && c.note) ? c.note : '';
        }
        /* the appointment marker, and its line down to the bar it sits over */
        var wantMark = !!round.mark && reveal;
        mark.style.display = wantMark ? 'flex' : 'none';
        conn.style.display = wantMark ? 'block' : 'none';
        if (wantMark) {
          markT.textContent = round.mark;
          var fi = 0;
          for (var m = 0; m < list.length; m++) if (list[m].focus) fi = m;
          var node = cols[fi].col;
          var mid = node.offsetLeft + node.offsetWidth / 2;
          conn.style.left = (mid > 0 ? mid : 0) + 'px';
          conn.style.top = '14px';
          conn.style.height = Math.max(0, PLOT - 14 - px(list[fi].v) - 16) + 'px';
        }
      }

      function render() {
        round = ROUNDS[order[seat % 4]];
        shown = shuffle(round.options.slice());
        picked = -1;
        committed = false;
        task.textContent = round.task;
        for (var j = 0; j < 3; j++) {
          obtn[j].textContent = shown[j].label;
          obtn[j].setAttribute('aria-pressed', 'false');
          obtn[j].className = 'o';
          obtn[j].disabled = false;
        }
        go.textContent = 'Check the result';
        go.disabled = true;
        drawCols(false);
        majl.className = 'majl' + (round.majRight ? ' r' : '');
        cap.textContent = round.note;
        run.textContent = streak > 0 ? streak + ' in a row' : '';
        state(null);
      }

      function pick(j) {
        if (committed) return;
        picked = j;
        for (var k = 0; k < 3; k++) obtn[k].setAttribute('aria-pressed', k === j ? 'true' : 'false');
        go.disabled = false;
        sr.textContent = 'Prediction chosen: ' + shown[j].label;
        state(null);
      }

      function commit() {
        if (picked < 0) return;
        if (committed) { seat++; render(); return; }
        committed = true;
        attempted++;
        var opt = shown[picked];
        var correct = !!opt.ok;
        var had = streak;
        streak = correct ? streak + 1 : 0;
        if (streak >= 3) mastered = true;

        drawCols(true);
        for (var j = 0; j < 3; j++) {
          obtn[j].disabled = true;
          if (shown[j].ok) obtn[j].className = 'o ok';
        }

        var text;
        if (correct && streak === 3) {
          text = 'Right — ' + round.shortRight + '. Three in a row: you have it. From 2.6% to a 37.3% peak, then down to 33.1% before he was appointed — and never a free majority. Historians read that as contingency, and the figures behind it are exact.';
        } else if (correct) {
          text = round.right + (streak === 1
            ? ' One in a row — two more and you have it.'
            : ' Two in a row — one more and you have it.');
        } else {
          text = opt.fb + (had > 0 ? ' That run resets — three in a row finishes it.' : '');
        }
        cap.textContent = text;
        sr.textContent = text;
        run.textContent = streak > 0 ? streak + ' in a row' : '';
        go.textContent = mastered ? 'Another anyway' : 'Next question';
        state(correct);
      }

      obtn.forEach(function (b, j) {
        b.addEventListener('click', function () { pick(j); });
      });
      go.addEventListener('click', commit);

      render();
    }
  };
})();
