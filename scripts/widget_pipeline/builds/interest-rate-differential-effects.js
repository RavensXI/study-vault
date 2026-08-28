/* interest-rate-differential-effects
   One base-rate move, six very different people. The student predicts which
   way it moves a named household or firm, and when they feel it. Every
   verdict is derived from the one transmission model below, so no two rounds
   can contradict each other. */
(function () {
  'use strict';

  var ID = 'interest-rate-differential-effects';

  /* Source stays ASCII; typography is applied on the way to the DOM so no
     tool in the chain can mangle a pound sign or an em dash. */
  function ty(s) {
    return String(s)
      .replace(/--/g, '—')
      .replace(/\|>/g, '→')
      .replace(/GBP/g, '£')
      .replace(/'/g, '’');
  }
  function money(n) {
    n = Math.round(n);
    var s = String(n);
    if (s.length > 3) s = s.slice(0, s.length - 3) + ',' + s.slice(-3);
    return '£' + s;
  }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  /* ---- the transmission model -------------------------------------------
     when:    'weeks'   reached directly, at the next bill or statement
              'dealend' locked by a fixed term, reached only when it ends
              'months'  reached second-hand, through decisions or other people
     riseDir: which way a RISE moves them. A cut is the mirror image.        */

  var CHARS = [
    {
      id: 'tracker', name: 'The Hartleys', plural: true,
      sit: 'GBP148,000 left on a tracker mortgage -- the rate moves with the base rate.',
      when: 'weeks', riseDir: 'worse',
      mech: function (rise, d) {
        return 'A tracker follows the base rate, so the payment ' +
          (rise ? 'climbs' : 'falls') + ' by about ' + money(148000 * d / 1200) +
          ' a month from the next payment date. Borrowers on variable deals feel a move first.';
      },
      sepWhen: 'Nothing has to end or be renewed first -- the change is already in their next bill.',
      sepDir: 'They are borrowing, so a higher base rate costs them more and a lower one less.'
    },
    {
      id: 'fixed', name: 'Nadia', plural: false,
      sit: 'Her mortgage is fixed at 2.4% until 2029, with GBP162,000 left.',
      when: 'dealend', riseDir: 'worse',
      mech: function (rise, d) {
        return 'Her rate is locked until 2029, so her payment does not move at all now. If rates are still ' +
          d.toFixed(2) + ' points ' + (rise ? 'higher' : 'lower') + ' when the fix ends, the move ' +
          (rise ? 'adds about ' : 'takes about ') + money(162000 * d / 1200) + ' a month ' +
          (rise ? 'to' : 'off') + ' her repayment.';
      },
      sepWhen: 'A fix delays a rate change; it does not cancel it.',
      sepDir: 'When the fix runs out she takes whatever rate is going then, so it reaches her in the end.'
    },
    {
      id: 'saver', name: 'Joan', plural: false,
      sit: 'Retired, with GBP26,000 in an instant-access savings account that follows the base rate.',
      when: 'weeks', riseDir: 'better',
      mech: function (rise, d) {
        return 'A saver is on the other side of the deal: the bank ' + (rise ? 'pays her more' : 'pays her less') +
          ', about ' + money(26000 * d / 100) + ' a year, within weeks of the move.';
      },
      sepWhen: 'Her money is not tied up, so the bank can change the rate it pays her straight away.',
      sepDir: 'A rise is not bad news for everybody -- money lent to a bank earns more.'
    },
    {
      id: 'firm', name: 'Marsh Lane Bakery', plural: false,
      sit: 'Planning a GBP70,000 loan for a new oven. The owners review the plan each quarter.',
      when: 'months', riseDir: 'worse',
      mech: function (rise, d) {
        return 'They have not borrowed yet. The loan would now cost ' + money(70000 * d / 100) +
          ' a year ' + (rise ? 'more' : 'less') + ' in interest, so the oven is ' +
          (rise ? 'likely to be put off' : 'more likely to be ordered') +
          ' -- investment turns slowly.';
      },
      sepWhen: 'The decision comes at the next quarterly review, not this month.',
      sepDir: 'Dearer borrowing holds investment back; cheaper borrowing brings it forward.'
    },
    {
      id: 'renter', name: 'Marcus', plural: false,
      sit: 'Rents a flat -- no mortgage, no savings. His landlord has a tracker on it; the rent is set each spring.',
      when: 'months', riseDir: 'worse',
      mech: function (rise, d) {
        return 'Nothing lands on him this month. His landlord pays about ' + money(130000 * d / 1200) +
          ' a month ' + (rise ? 'more' : 'less') + ', and the rent follows at the spring renewal.';
      },
      sepWhen: 'He is reached second-hand, through his landlord, so it waits for the renewal.',
      sepDir: 'His landlord costs move with the base rate, and rents follow those costs.'
    },
    {
      id: 'bond', name: 'Owen', plural: false,
      sit: 'GBP8,000 locked in a two-year fixed savings bond that matures in 2027.',
      when: 'dealend', riseDir: 'better',
      mech: function (rise, d) {
        return 'His bond is fixed, so he earns exactly the same until 2027 -- the move passes him by. He ' +
          (rise ? 'gains' : 'loses') + ' only when he reinvests, about ' + money(8000 * d / 100) +
          ' a year ' + (rise ? 'more' : 'less') + ' if rates hold.';
      },
      sepWhen: 'Fixing works the same way for a saver as for a borrower: it waits for the term to end.',
      sepDir: 'He is lending to the bank, so higher rates eventually pay him more and lower ones less.'
    }
  ];

  var RISES = [
    { from: '4.00', to: '5.25', d: 1.25 },
    { from: '3.00', to: '4.00', d: 1.00 },
    { from: '2.50', to: '3.25', d: 0.75 }
  ];
  var CUTS = [
    { from: '5.25', to: '4.50', d: 0.75 },
    { from: '4.75', to: '4.25', d: 0.50 },
    { from: '5.00', to: '4.00', d: 1.00 }
  ];

  var DIRLAB = { better: 'better off', worse: 'worse off' };
  var WHENLAB = { weeks: 'within weeks', dealend: 'when the deal ends', months: 'gradually over months' };
  var WHENBTN = { weeks: 'Within weeks', dealend: 'When the deal ends', months: 'Gradually, over months' };
  /* the three timings, soonest first, so the row reads as a time line */
  var WHENORDER = ['weeks', 'months', 'dealend'];
  var WHENCELL = { weeks: 'Within weeks', dealend: 'At the deal end', months: 'Over months' };

  function trueDir(ch, rise) {
    if (rise) return ch.riseDir;
    return ch.riseDir === 'worse' ? 'better' : 'worse';
  }

  var CSS =
  '.svw-ird{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4;' +
    'display:flex;flex-direction:column}' +
  '.svw-ird__kicker{order:1}.svw-ird__title{order:2}.svw-ird__frame{order:3}.svw-ird__stage{order:4}' +
  '.svw-ird__group{order:5}.svw-ird__go{order:6}.svw-ird__land{order:7}.svw-ird__cap{order:8}' +
  '.svw-ird__sr{order:10}' +
  '.svw-ird *{box-sizing:border-box}' +
  '.svw-ird__sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}' +
  '.svw-ird__kicker{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .25rem}' +
  '.svw-ird__title{font-family:"Source Serif 4",Georgia,serif;font-size:1.16rem;font-weight:600;line-height:1.2;margin:0 0 .3rem}' +
  '.svw-ird__frame{font-size:.82rem;line-height:1.45;color:#5b564e;margin:0 0 .7rem}' +
  '.svw-ird__stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.65rem .75rem;margin:0 0 .7rem}' +
  '.svw-ird__rate{display:flex;align-items:baseline;gap:.45rem;flex-wrap:wrap}' +
  '.svw-ird__rateval{font-size:1rem;font-weight:700;font-variant-numeric:tabular-nums}' +
  '.svw-ird__ratetag{font-size:.72rem;font-weight:600;font-variant-numeric:tabular-nums}' +
  '.svw-ird__gloss{font-size:.72rem;line-height:1.4;color:#8d8880;margin:.25rem 0 0}' +
  '.svw-ird__rule{height:1px;background:#e8e2d9;margin:.55rem 0 .5rem}' +
  '.svw-ird__who{font-size:.86rem;font-weight:700;margin:0 0 .15rem}' +
  '.svw-ird__sit{font-size:.82rem;line-height:1.45;color:#5b564e;margin:0}' +
  '.svw-ird__group{margin:0 0 .55rem}' +
  '.svw-ird__group.is-locked{opacity:.4}' +
  '.svw-ird__steplab{display:flex;align-items:center;gap:.38rem;font-size:.75rem;font-weight:700;margin:0 0 .32rem}' +
  '.svw-ird__num{display:inline-flex;align-items:center;justify-content:center;width:1.02rem;height:1.02rem;' +
    'border-radius:5px;font-size:.64rem;font-weight:700;color:#fff}' +
  '.svw-ird__row{display:grid;gap:.4rem}' +
  '.svw-ird__row--2{grid-template-columns:1fr 1fr}' +
  '.svw-ird__row--3{grid-template-columns:1fr 1fr 1fr}' +
  '.svw-ird__opt{font-family:inherit;font-size:.78rem;font-weight:600;line-height:1.25;padding:.42rem .3rem;' +
    'border:1px solid #ddd7cd;border-radius:10px;background:#fff;color:#2d2a26;cursor:pointer}' +
  '.svw-ird__opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}' +
  '.svw-ird__opt:disabled{cursor:default}' +
  '.svw-ird__go{width:100%;font-family:inherit;font-size:.85rem;font-weight:600;padding:.55rem .9rem;' +
    'border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}' +
  '.svw-ird__go:disabled{background:#f2ede5;border-color:#e9e3d9;color:#a8a29a;cursor:default}' +
  '.svw-ird__land{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.35rem;margin:.2rem 0 0}' +
  '.svw-ird__landlab{font-size:.7rem;font-weight:700;line-height:1.2;color:#8d8880;margin:.5rem 0 0;order:7}' +
  '.svw-ird__cell{font-size:.7rem;font-weight:600;line-height:1.2;text-align:center;padding:.32rem .2rem;' +
    'border:1px solid #e8e2d9;border-radius:8px;color:#8d8880;background:#faf8f5}' +
  '.svw-ird__cell.is-true{color:#2d2a26;font-weight:700}' +
  '.svw-ird__cell.is-miss{border-style:dashed;color:#5b564e}' +
  '.svw-ird__cap{min-height:2.4rem;margin:.55rem 0 0}' +
  '.svw-ird__fb{font-size:.84rem;line-height:1.46;margin:0}' +
  '.svw-ird__verdict{font-weight:700}' +
  '.svw-ird__streak{font-size:.74rem;color:#8d8880;margin:.4rem 0 0}' +
  '.svw-ird--still .svw-ird__opt,.svw-ird--still .svw-ird__go{transition:none}';

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = ty(txt);
    return n;
  }

  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = (ctx.accent || '').trim() ||
      (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';

    var S = {
      round: null, pickDir: null, pickWhen: null, committed: false,
      streak: 0, attempted: 0, mastered: false, lastCorrect: null
    };

    var wrap = el('div', 'svw-ird' + (ctx.reducedMotion ? ' svw-ird--still' : ''));
    var style = document.createElement('style');
    style.textContent = CSS;
    wrap.appendChild(style);

    var kicker = el('p', 'svw-ird__kicker', 'Interest rates');
    kicker.style.color = accent;
    wrap.appendChild(kicker);
    wrap.appendChild(el('h3', 'svw-ird__title', 'Who feels a rate change, and when'));
    wrap.appendChild(el('p', 'svw-ird__frame',
      'The Bank of England has changed the base rate. Predict how it lands on the ' +
      'household or firm below -- which way, and how soon.'));

    /* stage */
    var stage = el('div', 'svw-ird__stage');
    var rateRow = el('div', 'svw-ird__rate');
    var rateVal = el('span', 'svw-ird__rateval');
    var rateTag = el('span', 'svw-ird__ratetag');
    rateTag.style.color = accent;
    rateRow.appendChild(rateVal); rateRow.appendChild(rateTag);
    stage.appendChild(rateRow);
    stage.appendChild(el('p', 'svw-ird__gloss',
      'The base rate is what the Bank of England charges banks to borrow; they pass changes on.'));
    stage.appendChild(el('div', 'svw-ird__rule'));
    var who = el('p', 'svw-ird__who');
    var sit = el('p', 'svw-ird__sit');
    stage.appendChild(who); stage.appendChild(sit);
    wrap.appendChild(stage);

    /* controls */
    function stepLabel(n, text) {
      var lab = el('p', 'svw-ird__steplab');
      var num = el('span', 'svw-ird__num', String(n));
      num.style.background = accent;
      lab.appendChild(num);
      lab.appendChild(document.createTextNode(ty(text)));
      return lab;
    }

    var g1 = el('div', 'svw-ird__group');
    g1.appendChild(stepLabel(1, 'Which way for them?'));
    var row1 = el('div', 'svw-ird__row svw-ird__row--2');
    var dirBtns = {};
    ['worse', 'better'].forEach(function (k) {
      var b = el('button', 'svw-ird__opt', cap(DIRLAB[k]));
      b.type = 'button';
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () { pick('dir', k); });
      dirBtns[k] = b; row1.appendChild(b);
    });
    g1.appendChild(row1);
    wrap.appendChild(g1);

    var g2 = el('div', 'svw-ird__group is-locked');
    g2.appendChild(stepLabel(2, 'When do they feel it?'));
    var row2 = el('div', 'svw-ird__row svw-ird__row--3');
    var whenBtns = {};
    WHENORDER.forEach(function (k) {
      var b = el('button', 'svw-ird__opt', WHENBTN[k]);
      b.type = 'button';
      b.disabled = true;
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () { pick('when', k); });
      whenBtns[k] = b; row2.appendChild(b);
    });
    g2.appendChild(row2);
    wrap.appendChild(g2);

    var go = el('button', 'svw-ird__go', 'Check');
    go.type = 'button';
    go.disabled = true;
    go.addEventListener('click', function () {
      if (S.committed) { nextRound(); } else { commit(); }
    });
    wrap.appendChild(go);

    /* where it lands: only drawn once an answer is committed */
    var landLab = el('p', 'svw-ird__landlab', 'When it reaches them');
    landLab.style.display = 'none';
    wrap.appendChild(landLab);
    var land = el('div', 'svw-ird__land');
    land.style.display = 'none';
    var cells = {};
    WHENORDER.forEach(function (k) {
      var c = el('div', 'svw-ird__cell', WHENCELL[k]);
      cells[k] = c; land.appendChild(c);
    });
    wrap.appendChild(land);

    var capBox = el('div', 'svw-ird__cap');
    var fb = el('p', 'svw-ird__fb');
    fb.style.display = 'none';
    var streak = el('p', 'svw-ird__streak');
    capBox.appendChild(fb); capBox.appendChild(streak);
    wrap.appendChild(capBox);

    var sr = el('p', 'svw-ird__sr');
    sr.setAttribute('aria-live', 'polite');
    wrap.appendChild(sr);

    root.appendChild(wrap);

    /* ---- behaviour ---- */

    function publish() {
      root.dataset.svState = JSON.stringify({
        streak: S.streak, mastered: S.mastered, attempted: S.attempted,
        correct: S.lastCorrect,
        character: S.round ? S.round.ch.id : null,
        change: S.round ? (S.round.rise ? 'rise' : 'cut') : null,
        picked: { dir: S.pickDir, when: S.pickWhen }
      });
    }

    function pick(kind, key) {
      if (S.committed) return;
      if (kind === 'dir') {
        S.pickDir = key;
        Object.keys(dirBtns).forEach(function (k) {
          dirBtns[k].setAttribute('aria-pressed', k === key ? 'true' : 'false');
        });
        g2.classList.remove('is-locked');
        Object.keys(whenBtns).forEach(function (k) { whenBtns[k].disabled = false; });
      } else {
        S.pickWhen = key;
        Object.keys(whenBtns).forEach(function (k) {
          whenBtns[k].setAttribute('aria-pressed', k === key ? 'true' : 'false');
        });
      }
      go.disabled = !(S.pickDir && S.pickWhen);
      sr.textContent = ty('Chosen: ' + (S.pickDir ? DIRLAB[S.pickDir] : 'not set') + ', ' +
        (S.pickWhen ? WHENLAB[S.pickWhen] : 'timing not set') + '.');
      publish();
    }

    function clearPicks() {
      if (S.committed) return;
      S.pickDir = null; S.pickWhen = null;
      Object.keys(dirBtns).forEach(function (k) { dirBtns[k].setAttribute('aria-pressed', 'false'); });
      Object.keys(whenBtns).forEach(function (k) {
        whenBtns[k].setAttribute('aria-pressed', 'false'); whenBtns[k].disabled = true;
      });
      g2.classList.add('is-locked');
      go.disabled = true;
      publish();
    }

    wrap.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !S.committed && (S.pickDir || S.pickWhen)) {
        clearPicks();
        e.stopPropagation();
      }
    });

    function verdictText() {
      var r = S.round, ch = r.ch;
      var td = trueDir(ch, r.rise), tw = ch.when;
      var ok = (S.pickDir === td && S.pickWhen === tw);
      var mech = ch.mech(r.rise, r.d);
      var tail;
      if (ok) {
        tail = ' -- ' + DIRLAB[td] + ', ' + WHENLAB[tw] + '. ' + mech;
      } else {
        tail = ' -- you said ' + DIRLAB[S.pickDir] + ', ' + WHENLAB[S.pickWhen] + '. ' +
          ch.name + ' ' + (ch.plural ? 'are' : 'is') + ' ' + DIRLAB[td] + ', ' + WHENLAB[tw] + '. ' + mech;
        /* one diagnostic clause: the timing miss if there is one, since that is
           the idea this widget exists to fix; otherwise the direction miss. */
        tail += ' ' + (S.pickWhen !== tw ? ch.sepWhen : ch.sepDir);
      }
      return { ok: ok, head: ok ? 'Right' : 'Not quite', tail: tail, tw: tw };
    }

    function commit() {
      var v = verdictText();

      S.attempted += 1;
      S.lastCorrect = v.ok;
      S.streak = v.ok ? S.streak + 1 : 0;
      if (S.streak >= 3) S.mastered = true;
      S.committed = true;

      fb.textContent = '';
      var head = el('span', 'svw-ird__verdict', v.head);
      if (v.ok) head.style.color = '#4f7d63';
      fb.appendChild(head);
      fb.appendChild(document.createTextNode(ty(v.tail)));
      fb.style.display = '';

      Object.keys(cells).forEach(function (k) {
        var c = cells[k];
        c.className = 'svw-ird__cell';
        c.style.background = '#faf8f5';
        c.style.borderColor = '#e8e2d9';
        if (k === v.tw) {
          c.classList.add('is-true');
          c.style.background = accent + '22';
          c.style.borderColor = accent;
        } else if (k === S.pickWhen) {
          c.classList.add('is-miss');
        }
      });
      land.style.display = '';
      landLab.style.display = '';

      g1.style.display = 'none';
      g2.style.display = 'none';
      go.style.order = '9';          /* drops below the reveal without moving in the DOM */
      go.textContent = ty(S.mastered ? 'Another anyway' : 'Next one');
      go.disabled = false;
      setStreakLine();
      sr.textContent = ty(v.head + v.tail);
      publish();
    }

    function setStreakLine() {
      var t;
      if (S.mastered && S.committed && S.lastCorrect) {
        t = 'Three in a row -- you have it. The same move reaches a tracker in weeks, a fixed deal ' +
            'only when it ends, and a firm or a renter gradually over months.';
      } else if (S.streak === 2) {
        t = '2 right in a row -- one more and you have it.';
      } else if (S.streak === 1) {
        t = '1 right in a row -- two more and you have it.';
      } else if (S.attempted === 0) {
        t = 'Three in a row finishes it.';
      } else {
        t = 'Run reset -- three in a row finishes it.';
      }
      streak.textContent = ty(t);
    }

    function nextRound() {
      var prev = S.round;
      var pool = CHARS.filter(function (c) { return !prev || c.id !== prev.ch.id; });
      var ch = pool[Math.floor(Math.random() * pool.length)];
      var rise = prev ? !prev.rise : (Math.random() < 0.5);
      var list = rise ? RISES : CUTS;
      var rc = list[Math.floor(Math.random() * list.length)];

      S.round = { ch: ch, rise: rise, d: rc.d, from: rc.from, to: rc.to };
      S.pickDir = null; S.pickWhen = null; S.committed = false;

      rateVal.textContent = ty('Base rate ' + rc.from + '% |> ' + rc.to + '%');
      rateTag.textContent = ty((rise ? 'a rise of ' : 'a cut of ') + rc.d.toFixed(2) + ' points');
      who.textContent = ty(ch.name);
      sit.textContent = ty(ch.sit);

      Object.keys(dirBtns).forEach(function (k) { dirBtns[k].setAttribute('aria-pressed', 'false'); });
      Object.keys(whenBtns).forEach(function (k) {
        whenBtns[k].setAttribute('aria-pressed', 'false'); whenBtns[k].disabled = true;
      });
      g2.classList.add('is-locked');
      g1.style.display = ''; g2.style.display = '';
      land.style.display = 'none';
      landLab.style.display = 'none';
      fb.style.display = 'none';
      go.style.order = '';
      go.textContent = ty('Check');
      go.disabled = true;
      setStreakLine();
      publish();
    }

    nextRound();
  }

  window.SVWidget = {
    meta: {
      id: ID,
      title: 'Who feels a rate change, and when',
      teaches: 'A base rate change reaches households and firms unevenly and with different lags: variable borrowers and savers within weeks, fixed deals only when the term ends, firms and renters gradually over months.'
    },
    mount: mount
  };
})();
