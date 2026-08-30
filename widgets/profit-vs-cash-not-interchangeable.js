/* profit-vs-cash-not-interchangeable
   One month of a small business, given as a ledger of events.
   The student predicts PROFIT for the month and CASH at month end.
   Every figure is derived from the ledger: profit sums the revenue earned and
   the costs incurred; cash sums the opening balance and the money that
   actually moved. Nothing is asserted, and the two can never drift apart. */
(function () {
  'use strict';

  /* ---------- money ---------- */
  function group(n) {
    var s = String(n), out = '', c = 0, i;
    for (i = s.length - 1; i >= 0; i--) {
      out = s.charAt(i) + out; c++;
      if (c % 3 === 0 && i > 0) out = ',' + out;
    }
    return out;
  }
  function money(n) {
    n = Math.round(n);
    return (n < 0 ? '−£' : '£') + group(Math.abs(n));
  }
  function moneyAbs(n) { return money(Math.abs(n)); }

  /* ---------- the ledgers ----------
     rev / cash are multipliers on amt: +1 in, -1 out, 0 not this month.
     Each label carries the same amt, so the words and the arithmetic
     cannot drift apart. */
  var ROUNDS = [
    {
      who: 'a joinery workshop',
      open: 1200,
      events: [
        { amt: 6000, text: 'sold on 60-day trade credit', rev: 1, cash: 0 },
        { amt: 1400, text: 'sold at the counter, paid now', rev: 1, cash: 1 },
        { amt: 3000, text: 'timber used, paid on delivery', rev: -1, cash: -1 },
        { amt: 2200, text: 'wages, paid this month', rev: -1, cash: -1 },
        { amt: 800, text: 'rent and bills, paid now', rev: -1, cash: -1 }
      ],
      gap: 'The {a0} sale is revenue now, money in 60 days — the bills were paid now.',
      soWhat: 'A profitable month that still leaves the workshop {Kabs} overdrawn.'
    },
    {
      who: 'a print shop',
      open: 900,
      events: [
        { amt: 5000, text: "last month's credit sale lands", rev: 0, cash: 1 },
        { amt: 2100, text: 'printing sold, paid at once', rev: 1, cash: 1 },
        { amt: 1600, text: 'paper and ink used, paid now', rev: -1, cash: -1 },
        { amt: 1900, text: 'wages, paid this month', rev: -1, cash: -1 },
        { amt: 1100, text: 'rent and bills, paid now', rev: -1, cash: -1 }
      ],
      gap: "The {a0} that landed was last month's credit sale; this month's own sales did not cover the bills.",
      soWhat: 'Healthy-looking cash with a {Pabs} loss underneath it.'
    },
    {
      who: 'a sandwich shop',
      open: 700,
      events: [
        { amt: 5400, text: 'sold at the till, paid at once', rev: 1, cash: 1 },
        { amt: 2300, text: 'ingredients used, pay next month', rev: -1, cash: 0 },
        { amt: 1500, text: 'wages, paid this month', rev: -1, cash: -1 },
        { amt: 1000, text: 'rent and bills, paid now', rev: -1, cash: -1 }
      ],
      gap: 'The {a1} of ingredients is a cost the moment they are used, but the supplier is paid next month.',
      soWhat: 'Cash looks strong only because a {a1} bill has not landed yet.'
    },
    {
      who: 'a landscaping firm',
      open: 1800,
      events: [
        { amt: 3600, text: 'jobs done, paid on the day', rev: 1, cash: 1 },
        { amt: 2400, text: 'council job, 30-day trade credit', rev: 1, cash: 0 },
        { amt: 2900, text: 'plants used, paid next month', rev: -1, cash: 0 },
        { amt: 2700, text: 'wages, paid this month', rev: -1, cash: -1 },
        { amt: 800, text: 'fuel, rent and bills, paid now', rev: -1, cash: -1 }
      ],
      gap: 'Trade credit runs both ways: {a1} of sales is unpaid to the firm, {a2} of materials unpaid by it.',
      soWhat: 'A {Pabs} loss, and the bank balance still rose {dAbs}.'
    },
    {
      who: 'a phone repair shop',
      open: 1100,
      events: [
        { amt: 4300, text: 'repairs sold, paid on the spot', rev: 1, cash: 1 },
        { amt: 1500, text: 'parts used, paid on delivery', rev: -1, cash: -1 },
        { amt: 1400, text: 'wages, paid this month', rev: -1, cash: -1 },
        { amt: 600, text: 'rent and bills, paid now', rev: -1, cash: -1 }
      ],
      gap: 'Nothing here is on trade credit, so every pound earned or spent moved in the same month.',
      soWhat: 'Cash rose by exactly the profit; the closing {K} includes the {O} it opened with.'
    }
  ];

  /* every figure derived from the ledger, never asserted */
  function solve(r) {
    var profit = 0, moved = 0, i;
    for (i = 0; i < r.events.length; i++) {
      profit += r.events[i].rev * r.events[i].amt;
      moved += r.events[i].cash * r.events[i].amt;
    }
    return { profit: profit, moved: moved, cash: r.open + moved };
  }

  function fill(str, r) {
    var s = solve(r);
    return str
      .replace(/\{a(\d)\}/g, function (_, d) { return money(r.events[+d].amt); })
      .replace(/\{P\}/g, money(s.profit))
      .replace(/\{Pabs\}/g, moneyAbs(s.profit))
      .replace(/\{K\}/g, money(s.cash))
      .replace(/\{Kabs\}/g, moneyAbs(s.cash))
      .replace(/\{O\}/g, money(r.open))
      .replace(/\{dAbs\}/g, moneyAbs(s.moved));
  }

  var CSS = [
    '.svw-pvc{box-sizing:border-box;max-width:100%;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;font-size:16px;line-height:1.45;color:#2d2a26}',
    '.svw-pvc *,.svw-pvc *::before,.svw-pvc *::after{box-sizing:border-box}',
    '.svw-pvc p,.svw-pvc h3{margin:0}',
    '.svw-pvc .pvc-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--pvc-accent,#8a6a4f)}',
    '.svw-pvc .pvc-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.2;margin:.1rem 0 .26rem}',
    '.svw-pvc .pvc-task{font-size:.85rem;color:#4a453e;margin-bottom:.55rem}',
    '.svw-pvc .pvc-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.3rem .6rem .4rem;margin-bottom:.55rem}',
    '.svw-pvc .pvc-row{display:flex;align-items:center;gap:.5rem;padding:.26rem 0;border-top:1px solid #efe9e0;font-size:.8rem}',
    '.svw-pvc .pvc-row:first-child{border-top:0}',
    '.svw-pvc .pvc-open{color:#5b564e}',
    '.svw-pvc .pvc-txt{flex:1 1 auto;min-width:0}',
    '.svw-pvc .pvc-txt b{font-weight:600;font-variant-numeric:tabular-nums}',
    '.svw-pvc .pvc-badges{display:none;flex:0 0 auto;gap:.4rem}',
    '.svw-pvc.is-open .pvc-badges{display:flex}',
    '.svw-pvc .pvc-b{flex:0 0 auto;width:1rem;height:1rem;border-radius:50%;font-size:.62rem;font-weight:700;line-height:1;display:flex;align-items:center;justify-content:center;border:1px solid #ddd7cd;color:#a09a90;background:#fff}',
    '.svw-pvc .pvc-b.on{background:var(--pvc-accent,#8a6a4f);border-color:var(--pvc-accent,#8a6a4f);color:#fff}',
    '.svw-pvc .pvc-tot{display:none}',
    '.svw-pvc.is-open .pvc-tot{display:block;border-top:1px solid #e0d9cd;margin-top:.28rem;padding-top:.22rem}',
    '.svw-pvc .pvc-totrow{display:flex;align-items:center;justify-content:space-between;gap:.5rem;padding:.1rem 0}',
    '.svw-pvc .pvc-totlab{display:flex;align-items:center;gap:.4rem;font-size:.72rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#8d8880}',
    '.svw-pvc .pvc-totrow b{font-size:.98rem;font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}',
    '.svw-pvc .pvc-ctrls{display:flex;flex-wrap:wrap;gap:.5rem;align-items:flex-end}',
    '.svw-pvc .pvc-field{flex:1 1 138px;min-width:128px}',
    '.svw-pvc .pvc-lab{display:block;font-size:.7rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#8d8880;margin-bottom:.18rem}',
    '.svw-pvc .pvc-inwrap{display:flex;gap:.3rem}',
    '.svw-pvc .pvc-sign{flex:0 0 auto;width:2rem;height:2.1rem;border:1px solid #ddd7cd;background:#faf8f5;border-radius:9px;font:inherit;font-size:.95rem;font-weight:700;color:#2d2a26;cursor:pointer;padding:0}',
    '.svw-pvc .pvc-sign.neg{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-pvc .pvc-in{flex:1 1 auto;min-width:0;width:100%;height:2.1rem;border:1px solid #ddd7cd;background:#fff;border-radius:9px;padding:0 .5rem;font:inherit;font-size:.9rem;font-weight:600;font-variant-numeric:tabular-nums;color:#2d2a26}',
    '.svw-pvc .pvc-in:focus,.svw-pvc .pvc-sign:focus,.svw-pvc .pvc-go:focus{outline:2px solid var(--pvc-accent,#8a6a4f);outline-offset:1px}',
    '.svw-pvc .pvc-in[disabled],.svw-pvc .pvc-sign[disabled]{opacity:.8;cursor:default}',
    '.svw-pvc .pvc-go{flex:1 1 148px;max-width:100%;height:2.1rem;border:1px solid #2d2a26;background:#2d2a26;color:#fff;border-radius:10px;font:inherit;font-size:.82rem;font-weight:600;cursor:pointer;padding:0 .9rem}',
    '.svw-pvc .pvc-streak{font-size:.76rem;color:#8d8880;margin-top:.4rem;min-height:1rem}',
    '.svw-pvc .pvc-cap{font-size:.84rem;line-height:1.5;margin-top:.2rem;min-height:3.6em}',
    '.svw-pvc .pvc-cap b{font-weight:600}',
    '.svw-pvc .pvc-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
  ].join('\n');

  window.SVWidget = {
    meta: {
      id: 'profit-vs-cash-not-interchangeable',
      title: 'Two numbers, one month',
      teaches: 'Profit and cash are different measures on different clocks: trade credit separates the sale from the money, so a profitable month can end overdrawn.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var uid = 'pvc' + Math.random().toString(36).slice(2, 8);

      root.className = (root.className ? root.className + ' ' : '') + 'svw-pvc';
      root.style.setProperty('--pvc-accent', accent);

      root.innerHTML =
        '<style>' + CSS + '</style>' +
        '<p class="pvc-kick">Cash flow</p>' +
        '<h3 class="pvc-title">Two numbers, one month</h3>' +
        '<p class="pvc-task"></p>' +
        '<div class="pvc-stage">' +
          '<div class="pvc-rows"></div>' +
          '<div class="pvc-tot">' +
            '<div class="pvc-totrow"><span class="pvc-totlab"><span class="pvc-b on">P</span>Profit for the month</span><b class="pvc-tp"></b></div>' +
            '<div class="pvc-totrow"><span class="pvc-totlab"><span class="pvc-b on">C</span>Cash at month end</span><b class="pvc-tk"></b></div>' +
          '</div>' +
        '</div>' +
        '<div class="pvc-ctrls">' +
          '<div class="pvc-field">' +
            '<label class="pvc-lab" for="' + uid + 'p">Profit for the month (£)</label>' +
            '<div class="pvc-inwrap">' +
              '<button type="button" class="pvc-sign" data-for="p" aria-label="Profit sign, currently positive">+</button>' +
              '<input class="pvc-in" id="' + uid + 'p" type="text" inputmode="numeric" autocomplete="off">' +
            '</div>' +
          '</div>' +
          '<div class="pvc-field">' +
            '<label class="pvc-lab" for="' + uid + 'c">Cash at month end (£)</label>' +
            '<div class="pvc-inwrap">' +
              '<button type="button" class="pvc-sign" data-for="c" aria-label="Cash sign, currently positive">+</button>' +
              '<input class="pvc-in" id="' + uid + 'c" type="text" inputmode="numeric" autocomplete="off">' +
            '</div>' +
          '</div>' +
          '<button type="button" class="pvc-go">Check the month</button>' +
        '</div>' +
        '<p class="pvc-streak"></p>' +
        '<p class="pvc-cap"></p>' +
        '<p class="pvc-sr" role="status" aria-live="polite"></p>';

      var q = function (s) { return root.querySelector(s); };
      var elTask = q('.pvc-task'), elRows = q('.pvc-rows'), elTP = q('.pvc-tp'), elTK = q('.pvc-tk'),
          elGo = q('.pvc-go'), elStreak = q('.pvc-streak'), elCap = q('.pvc-cap'), elSr = q('.pvc-sr'),
          inP = q('#' + uid + 'p'), inC = q('#' + uid + 'c'),
          sgnP = root.querySelector('.pvc-sign[data-for="p"]'),
          sgnC = root.querySelector('.pvc-sign[data-for="c"]');

      var GLOSS = '<b>Trade credit</b> means the goods go out now and the money arrives later — 30 or 60 days later.';

      var st = { streak: 0, attempted: 0, mastered: false, revealed: false, sign: { p: 1, c: 1 } };
      var queue = [], round = null, sol = null, first = true;

      function nextRound() {
        if (first) { queue = [ROUNDS[0]]; first = false; }
        if (!queue.length) {
          var pool = ROUNDS.slice(), i, j, t;
          for (i = pool.length - 1; i > 0; i--) {
            j = Math.floor(Math.random() * (i + 1)); t = pool[i]; pool[i] = pool[j]; pool[j] = t;
          }
          if (round && pool[0] === round && pool.length > 1) { t = pool[0]; pool[0] = pool[1]; pool[1] = t; }
          queue = pool;
        }
        round = queue.shift();
        sol = solve(round);
      }

      function drawRound() {
        var html = '<div class="pvc-row pvc-open"><span class="pvc-txt"><b>' + money(round.open) +
          '</b> in the bank on the 1st</span><span class="pvc-badges">' +
          '<span class="pvc-b">P</span><span class="pvc-b on">C</span></span></div>';
        for (var i = 0; i < round.events.length; i++) {
          var e = round.events[i];
          html += '<div class="pvc-row"><span class="pvc-txt"><b>' + money(e.amt) + '</b> ' + e.text +
            '</span><span class="pvc-badges">' +
            '<span class="pvc-b' + (e.rev ? ' on' : '') + '">P</span>' +
            '<span class="pvc-b' + (e.cash ? ' on' : '') + '">C</span></span></div>';
        }
        elRows.innerHTML = html;
        elTask.innerHTML = 'One month at <b>' + round.who +
          '</b>. Predict its profit, and its cash in the bank at month end.';
        elTP.textContent = money(sol.profit);
        elTK.textContent = money(sol.cash);
      }

      function setSign(key, v) {
        st.sign[key] = v;
        var b = key === 'p' ? sgnP : sgnC;
        b.textContent = v < 0 ? '−' : '+';
        b.className = 'pvc-sign' + (v < 0 ? ' neg' : '');
        b.setAttribute('aria-label', (key === 'p' ? 'Profit' : 'Cash') +
          ' sign, currently ' + (v < 0 ? 'negative' : 'positive'));
      }

      /* accept a typed minus or accounting brackets as well as the sign
         button, and make the button agree with what was typed */
      function readVal(input, key) {
        var raw = String(input.value).replace(/[,\s£]/g, ''), neg = false;
        if (/^\(.+\)$/.test(raw)) { neg = true; raw = raw.slice(1, -1); }
        if (/^[-−–]/.test(raw)) { neg = true; raw = raw.replace(/^[-−–]+/, ''); }
        if (!/^\d+$/.test(raw)) return null;
        if (neg && st.sign[key] > 0) setSign(key, -1);
        return st.sign[key] * parseInt(raw, 10);
      }

      function publish(extra) {
        var s = {
          round: round.who, streak: st.streak, mastered: st.mastered,
          attempted: st.attempted, signs: (st.sign.p < 0 ? '-' : '+') + (st.sign.c < 0 ? '-' : '+')
        };
        if (extra) for (var k in extra) if (Object.prototype.hasOwnProperty.call(extra, k)) s[k] = extra[k];
        root.dataset.svState = JSON.stringify(s);
      }

      function say(html) { elCap.innerHTML = html; elSr.textContent = elCap.textContent; }

      function startRound() {
        nextRound();
        st.revealed = false;
        root.classList.remove('is-open');
        inP.value = ''; inC.value = '';
        inP.disabled = false; inC.disabled = false;
        sgnP.disabled = false; sgnC.disabled = false;
        setSign('p', 1); setSign('c', 1);
        drawRound();
        elGo.textContent = 'Check the month';
        say(GLOSS);
        publish({ awaiting: true });
      }

      /* ---------- feedback: verdict first, then the student's own answer ---------- */
      function verdict(gp, gc) {
        var P = sol.profit, K = sol.cash, moved = sol.moved;
        var gapLine = fill(round.gap, round);

        if (gp === P && gc === K) {
          if (st.streak + 1 >= 3 && !st.mastered) {
            return 'Right — profit ' + money(P) + ' and cash ' + money(K) +
              '. Three in a row: you have it. Profit counts a sale when it is made and a cost when it is used up; cash counts either only when the money moves, and trade credit is the gap between them.';
          }
          return 'Right — profit <b>' + money(P) + '</b> and cash <b>' + money(K) +
            '</b>, both true of one month. ' + gapLine + ' ' + fill(round.soWhat, round);
        }

        var head = 'Not quite — you said profit <b>' + money(gp) + '</b> and cash <b>' + money(gc) +
          '</b>. Profit was <b>' + money(P) + '</b>; the bank ended at <b>' + money(K) + '</b>. ';

        if (gp === gc) {
          return head + gapLine + ' Profit is not money in the till.';
        }
        if (gp === P && gc === round.open + P) {
          return head + 'You added the profit to the opening balance, as if every pound earned were already banked.';
        }
        if (gc === K && gp === moved) {
          return head + 'You measured profit by the money that moved. Profit counts what was earned and what was used up, whenever the cash lands.';
        }
        if (gp === P) {
          return head + 'The profit is right; cash is the timing. ' + gapLine;
        }
        if (gc === K) {
          return head + 'The cash is right; profit ignores when money moves, counting sales when made and costs when incurred.';
        }
        return head + gapLine;
      }

      function commit() {
        if (st.revealed) { startRound(); inP.focus(); return; }
        var gp = readVal(inP, 'p'), gc = readVal(inC, 'c');
        if (gp === null || gc === null) {
          say('Put a figure in both boxes — one for the profit the month earned, one for the cash left in the bank.');
          publish({ awaiting: true, blank: true });
          (gp === null ? inP : inC).focus();
          return;
        }
        inP.value = String(Math.abs(gp)); inC.value = String(Math.abs(gc));
        var right = (gp === sol.profit && gc === sol.cash);
        var hadRun = st.streak;
        st.attempted++;
        say(verdict(gp, gc));
        st.streak = right ? st.streak + 1 : 0;
        if (st.streak >= 3) st.mastered = true;
        st.revealed = true;
        root.classList.add('is-open');
        inP.disabled = true; inC.disabled = true;
        sgnP.disabled = true; sgnC.disabled = true;
        elGo.textContent = st.mastered ? 'Another anyway' : 'Next month';
        elStreak.textContent = st.mastered
          ? 'Three in a row — you can stop here.'
          : (st.streak === 1 ? '1 right in a row — two more and you have it.'
            : st.streak === 2 ? '2 right in a row — one more and you have it.'
              : hadRun ? 'Run back to zero — that is what a guess costs.'
                : 'Three in a row and you have it.');
        publish({ correct: right, saidProfit: gp, saidCash: gc, profit: sol.profit, cash: sol.cash });
      }

      sgnP.addEventListener('click', function () { setSign('p', -st.sign.p); publish({ awaiting: !st.revealed }); });
      sgnC.addEventListener('click', function () { setSign('c', -st.sign.c); publish({ awaiting: !st.revealed }); });
      elGo.addEventListener('click', commit);
      root.addEventListener('keydown', function (ev) {
        if (ev.key === 'Enter' && (ev.target === inP || ev.target === inC)) { ev.preventDefault(); commit(); }
      });

      startRound();
    }
  };
})();
