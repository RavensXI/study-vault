/* limited-liability-protects-personal-assets-only
   A failing business, given as two columns of things worth money: what the
   business owns on one side, what the owner owns on the other, with a line
   between them. The student marks what the creditors can be paid from, then
   commits to what the owner loses.

   Every figure comes from one model — debt, the assets on each side, what the
   owner paid for shares, what is still unpaid on them. Reach and loss are
   derived from the legal form, never hand-authored, so the same collapse can
   be run as a sole trader and as a private limited company and the two answers
   cannot drift apart. */
(function () {
  'use strict';

  /* ------------------------------------------------------------- money --- */
  function group(n) {
    var s = String(n), out = '', c = 0, i;
    for (i = s.length - 1; i >= 0; i--) {
      out = s.charAt(i) + out; c++;
      if (c % 3 === 0 && i > 0) out = ',' + out;
    }
    return out;
  }
  function money(n) { return '£' + group(Math.abs(Math.round(n))); }

  /* -------------------------------------------------------------- data ---
     co  = things the business owns (always sold when it fails)
     own = things the owner owns; `unpaid:true` marks share money agreed but
           never paid, which is a debt the owner still owes.               */
  var BIZ = {
    cafe: {
      owner: 'Rita', pn: 'she', adj: 'her', poss: 'hers',
      noun: 'café', head: 'The café', debt: 96000, paidIn: 25000,
      co: [{ n: 'Coffee kit', v: 12000 }, { n: 'Stock', v: 3000 }, { n: 'Cash', v: 5000 }],
      own: [{ n: 'House', v: 140000, s: 'her house' }, { n: 'Car', v: 9000, s: 'her car' },
            { n: 'Savings', v: 7000, s: 'her savings' }]
    },
    build: {
      owner: 'Dev', pn: 'he', adj: 'his', poss: 'his',
      noun: 'firm', head: 'The firm', debt: 54000, paidIn: 0,
      co: [{ n: 'Van', v: 11000 }, { n: 'Tools', v: 4000 }, { n: 'Materials', v: 2000 }],
      own: [{ n: 'House', v: 120000, s: 'his house' }, { n: 'Car', v: 6000, s: 'his car' },
            { n: 'Savings', v: 3000, s: 'his savings' }]
    },
    salon: {
      owner: 'Priya', pn: 'she', adj: 'her', poss: 'hers',
      noun: 'salon', head: 'The salon', debt: 68000, paidIn: 30000,
      co: [{ n: 'Chairs', v: 9000 }, { n: 'Stock', v: 2000 }, { n: 'Cash', v: 4000 }],
      own: [{ n: 'House', v: 95000, s: 'her house' }, { n: 'Car', v: 8000, s: 'her car' },
            { n: 'Savings', v: 6000, s: 'her savings' }]
    },
    delivery: {
      owner: 'Marcus', pn: 'he', adj: 'his', poss: 'his',
      noun: 'firm', head: 'The firm', debt: 58000, paidIn: 12000, unpaid: 8000,
      co: [{ n: 'Two vans', v: 14000 }, { n: 'Kitchen kit', v: 6000 }, { n: 'Cash', v: 2000 }],
      own: [{ n: 'Unpaid shares', v: 8000, s: 'the unpaid share money', unpaid: true },
            { n: 'House', v: 110000, s: 'his house' }, { n: 'Savings', v: 5000, s: 'his savings' }]
    },
    print: {
      owner: 'Nadia', pn: 'she', adj: 'her', poss: 'hers',
      noun: 'shop', head: 'The shop', debt: 41000, paidIn: 18000,
      co: [{ n: 'Printers', v: 8000 }, { n: 'Paper stock', v: 2000 }, { n: 'Cash', v: 3000 }],
      own: [{ n: 'House', v: 130000, s: 'her house' }, { n: 'Car', v: 5000, s: 'her car' },
            { n: 'Savings', v: 9000, s: 'her savings' }]
    },
    stall: {
      owner: 'Tomas', pn: 'he', adj: 'his', poss: 'his',
      noun: 'stall', head: 'The stall', debt: 31000, paidIn: 0,
      co: [{ n: 'Stall + van', v: 7000 }, { n: 'Stock', v: 3000 }, { n: 'Cash', v: 1000 }],
      own: [{ n: 'House', v: 85000, s: 'his house' }, { n: 'Car', v: 4000, s: 'his car' },
            { n: 'Savings', v: 6000, s: 'his savings' }]
    }
  };

  /* Rounds 1-3 are pinned: the same collapse as a sole trader, then as a
     private limited company (the contrast is the teaching), then the unpaid
     share money. A student who masters in three has met all three forms. */
  var FIXED = [
    { k: 'cafe', form: 'sole',
      frame: 'Rita runs a café as a sole trader. It closes owing £96,000; selling everything it owns raises £20,000.' },
    { k: 'cafe', form: 'ltd',
      frame: 'Same café, same collapse — but Rita had set it up as a private limited company and paid £25,000 for her shares.' },
    { k: 'delivery', form: 'unpaid',
      frame: 'Marcus agreed to buy £20,000 of shares in his delivery firm and has paid £12,000. It folds owing £58,000; assets raise £22,000.' }
  ];
  var POOL = [
    { k: 'build', form: 'sole',
      frame: 'Dev runs a building firm as a sole trader. It collapses owing £54,000; its assets raise £17,000.' },
    { k: 'salon', form: 'ltd',
      frame: 'Priya’s salon is a private limited company. She paid £30,000 for her shares. It closes owing £68,000; assets raise £15,000.' },
    { k: 'print', form: 'ltd',
      frame: 'Nadia’s print shop is a private limited company. She paid £18,000 for her shares. It folds owing £41,000; assets raise £13,000.' },
    { k: 'stall', form: 'sole',
      frame: 'Tomas runs a market stall as a sole trader. It fails owing £31,000; its assets raise £11,000.' }
  ];

  function shuffle(a) {
    var out = a.slice(), i, j, t;
    for (i = out.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1)); t = out[i]; out[i] = out[j]; out[j] = t;
    }
    return out;
  }

  /* --------------------------------------------------------- the model --- */
  function solve(spec) {
    var b = BIZ[spec.k], i;
    var assets = 0, ownTot = 0;
    for (i = 0; i < b.co.length; i++) assets += b.co[i].v;
    for (i = 0; i < b.own.length; i++) if (!b.own[i].unpaid) ownTot += b.own[i].v;
    var unpaid = spec.form === 'unpaid' ? (b.unpaid || 0) : 0;
    var shortfall = b.debt - assets;

    /* which tiles the creditors can be paid from */
    var reach = {};
    for (i = 0; i < b.co.length; i++) reach['c' + i] = true;
    for (i = 0; i < b.own.length; i++) {
      if (spec.form === 'sole') reach['o' + i] = true;
      else if (spec.form === 'unpaid' && b.own[i].unpaid) reach['o' + i] = true;
    }

    var loss = spec.form === 'sole' ? b.debt : b.paidIn + unpaid;

    var opts;
    if (spec.form === 'sole') {
      opts = [
        { v: 0, g: 'nothing at all' },
        { v: assets, g: 'only what the business owned' },
        { v: shortfall, g: 'only the part left unpaid' },
        { v: b.debt, g: 'the whole debt, from ' + b.adj + ' own pocket' }
      ];
    } else if (spec.form === 'unpaid') {
      opts = [
        { v: 0, g: 'nothing at all' },
        { v: b.paidIn, g: 'only what ' + b.pn + ' has paid so far' },
        { v: b.paidIn + unpaid, g: b.adj + ' shares, paid and unpaid' },
        { v: b.paidIn + unpaid + ownTot, g: b.adj + ' shares, house and savings' }
      ];
    } else {
      opts = [
        { v: 0, g: 'nothing at all' },
        { v: b.paidIn, g: 'what ' + b.pn + ' paid for ' + b.adj + ' shares' },
        { v: shortfall, g: 'the debt the company cannot pay' },
        { v: b.paidIn + ownTot, g: b.adj + ' shares, house, car and savings' }
      ];
    }

    return {
      b: b, form: spec.form, frame: spec.frame, assets: assets, ownTot: ownTot,
      unpaid: unpaid, shortfall: shortfall, loss: loss, reach: reach,
      opts: shuffle(opts)
    };
  }

  /* ---------------------------------------------------------------- CSS --- */
  var CSS = [
    '.svw-lb{box-sizing:border-box;max-width:100%;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;font-size:16px;line-height:1.45;color:#2d2a26}',
    '.svw-lb *,.svw-lb *::before,.svw-lb *::after{box-sizing:border-box}',
    '.svw-lb p,.svw-lb h3{margin:0}',
    '.svw-lb .lb-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--lb-accent,#8a6a4f)}',
    '.svw-lb .lb-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.18;margin:.06rem 0 .22rem}',
    '.svw-lb .lb-frame{font-size:.84rem;line-height:1.42;color:#4a453e}',
    '.svw-lb .lb-step{display:flex;align-items:center;gap:.35rem;font-size:.74rem;font-weight:600;color:#5b564e;margin:.38rem 0 .16rem}',
    '.svw-lb .lb-num{flex:0 0 auto;width:1.02rem;height:1.02rem;border-radius:50%;background:var(--lb-accent,#8a6a4f);color:#fff;font-size:.62rem;font-weight:700;line-height:1;display:flex;align-items:center;justify-content:center}',
    '.svw-lb .lb-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.35rem .4rem .4rem}',
    '.svw-lb .lb-cols{display:grid;grid-template-columns:1fr 2px 1fr;gap:.4rem}',
    '.svw-lb .lb-wall{background:#dbd3c5;border-radius:2px}',
    '.svw-lb.is-held .lb-wall{background:#2d2a26}',
    '.svw-lb.is-breach .lb-wall{background:repeating-linear-gradient(#d3ccbf 0 3px,transparent 3px 7px)}',
    '.svw-lb .lb-head{font-size:.66rem;font-weight:700;letter-spacing:.03em;text-transform:uppercase;color:#8d8880;margin-bottom:.2rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.svw-lb .lb-tiles{display:flex;flex-direction:column;gap:.22rem}',
    '.svw-lb .lb-tile{display:block;width:100%;text-align:left;font:inherit;background:#fff;border:1px solid #e4ded4;border-radius:9px;padding:.2rem .4rem;cursor:pointer;color:#2d2a26}',
    '.svw-lb .lb-tile[aria-pressed="true"]{border-color:var(--lb-accent,#8a6a4f);box-shadow:inset 0 0 0 1px var(--lb-accent,#8a6a4f);background:var(--lb-tint,#f7f2eb)}',
    '.svw-lb .lb-tile[aria-disabled="true"]{cursor:default}',
    '.svw-lb .lb-n{display:block;font-size:.66rem;color:#8d8880;line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.svw-lb .lb-v{display:block;font-size:.83rem;font-weight:700;font-variant-numeric:tabular-nums;line-height:1.25;white-space:nowrap}',
    /* the business is sold outright, so its figures are struck; a house is
       only reached as far as the debt goes, so it greys but is not struck */
    '.svw-lb .lb-tile.is-gone .lb-v{color:#8d8880;text-decoration:line-through;text-decoration-color:#c3bcb0}',
    '.svw-lb .lb-tile.is-risk .lb-v{color:#8d8880}',
    '.svw-lb .lb-opts{display:grid;grid-template-columns:repeat(2,1fr);gap:.35rem}',
    '.svw-lb .lb-opt{font:inherit;text-align:left;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.3rem .5rem;cursor:pointer;color:#2d2a26}',
    '.svw-lb .lb-opt b{display:block;font-size:.86rem;font-weight:700;font-variant-numeric:tabular-nums;line-height:1.25}',
    '.svw-lb .lb-opt small{display:block;font-size:.68rem;color:#8d8880;line-height:1.25}',
    '.svw-lb .lb-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-lb .lb-opt[aria-pressed="true"] small{color:#ded7cb}',
    '.svw-lb .lb-opt[aria-disabled="true"]{cursor:default}',
    '.svw-lb .lb-act{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin-top:.45rem}',
    '.svw-lb .lb-go{font:inherit;font-size:.82rem;font-weight:600;padding:.48rem .95rem;border:1px solid #2d2a26;border-radius:10px;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-lb .lb-go[disabled]{opacity:.4;cursor:default}',
    '.svw-lb .lb-run{font-size:.75rem;color:#8d8880}',
    '.svw-lb .lb-cap{font-size:.8rem;line-height:1.5;margin-top:.4rem;color:#3c3833;min-height:4.5em}',
    '.svw-lb .lb-cap b{font-weight:700;color:#2d2a26}',
    '.svw-lb .lb-tile:focus-visible,.svw-lb .lb-opt:focus-visible,.svw-lb .lb-go:focus-visible{outline:2px solid var(--lb-accent,#8a6a4f);outline-offset:2px}',
    '.svw-lb .lb-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap}'
  ].join('\n');

  /* =============================================================== mount === */
  window.SVWidget = {
    meta: {
      id: 'limited-liability-protects-personal-assets-only',
      title: 'Where the loss stops',
      teaches: 'Limited liability draws a legal line around the owner’s own things: the company still owes every penny it owes, and the owner still loses what they put in — the loss is capped, not cancelled. A sole trader has no such line.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
        ctx.accent || '#8a6a4f';
      /* Nothing here animates, so ctx.reducedMotion needs no special case:
         the stage is redrawn only when the student acts. */

      root.className = (root.className ? root.className + ' ' : '') + 'svw-lb';
      root.style.setProperty('--lb-accent', accent);
      root.style.setProperty('--lb-tint', accent + '14');

      root.innerHTML =
        '<style>' + CSS + '</style>' +
        '<p class="lb-kick">Limited liability</p>' +
        '<h3 class="lb-title">Where the loss stops</h3>' +
        '<p class="lb-frame"></p>' +
        '<p class="lb-step"><span class="lb-num">1</span><span class="lb-s1"></span></p>' +
        '<div class="lb-stage">' +
          '<div class="lb-cols">' +
            '<div class="lb-col"><p class="lb-head lb-headco"></p><div class="lb-tiles lb-co"></div></div>' +
            '<div class="lb-wall" aria-hidden="true"></div>' +
            '<div class="lb-col"><p class="lb-head lb-headown"></p><div class="lb-tiles lb-own"></div></div>' +
          '</div>' +
        '</div>' +
        '<p class="lb-step"><span class="lb-num">2</span><span class="lb-s2"></span></p>' +
        '<div class="lb-opts" role="group"></div>' +
        '<div class="lb-act"><button type="button" class="lb-go" disabled>Check</button>' +
        '<span class="lb-run"></span></div>' +
        '<p class="lb-cap"></p>' +
        '<p class="lb-sr" role="status" aria-live="polite"></p>';

      var q = function (s) { return root.querySelector(s); };
      var elFrame = q('.lb-frame'), elS1 = q('.lb-s1'), elS2 = q('.lb-s2'),
          elHeadCo = q('.lb-headco'), elHeadOwn = q('.lb-headown'),
          elCo = q('.lb-co'), elOwn = q('.lb-own'), elOpts = q('.lb-opts'),
          elGo = q('.lb-go'), elRun = q('.lb-run'), elCap = q('.lb-cap'), elSr = q('.lb-sr');

      var st = { streak: 0, attempted: 0, mastered: false };
      var queue = FIXED.slice(), seeded = false;
      var r = null, marked = {}, choice = null, committed = false;
      var tiles = {}, optBtns = [];

      /* ----------------------------------------------------------- prose --- */
      function listOf(arr) {
        if (!arr.length) return '';
        if (arr.length === 1) return arr[0];
        return arr.slice(0, -1).join(', ') + ' and ' + arr[arr.length - 1];
      }

      function describeMarked() {
        var b = r.b, i, coOn = 0, ownOn = [];
        for (i = 0; i < b.co.length; i++) if (marked['c' + i]) coOn++;
        for (i = 0; i < b.own.length; i++) if (marked['o' + i]) ownOn.push(b.own[i].s);
        if (!coOn && !ownOn.length) return 'nothing at all';
        var coTxt = coOn === b.co.length ? 'the business’s assets'
          : (coOn ? 'part of the business’s assets' : '');
        var ownTxt = ownOn.length === b.own.length ? 'everything of ' + b.poss : listOf(ownOn);
        if (coTxt && !ownTxt) return coTxt + ' only';
        if (!coTxt) return 'only ' + ownTxt;
        return coTxt + ' and ' + ownTxt;
      }

      function truthReach() {
        var b = r.b;
        if (r.form === 'sole') {
          return 'everything: the ' + money(r.assets) + ' in the business, then ' +
            b.adj + ' house, car and savings';
        }
        if (r.form === 'unpaid') {
          return 'the ' + money(r.assets) + ' in the business and the ' + money(r.unpaid) +
            ' still unpaid on ' + b.adj + ' shares';
        }
        return 'the ' + b.noun + '’s ' + money(r.assets) + ' and nothing of ' + b.poss;
      }

      function lossGloss() {
        var b = r.b;
        if (r.form === 'sole') return 'the whole debt comes out of ' + b.adj + ' own pocket';
        if (r.form === 'unpaid') return 'what ' + b.pn + ' paid, plus the share money still owed';
        return 'what ' + b.pn + ' paid for ' + b.adj + ' shares';
      }

      function mechanism() {
        var b = r.b;
        if (r.form === 'sole') {
          if (choice === 0) {
            return 'Unlimited liability means the ' + money(r.shortfall) +
              ' the business cannot pay comes out of ' + b.adj + ' own things.';
          }
          if (choice === r.assets) {
            return 'The ' + money(r.assets) + ' is only the start; the other ' +
              money(r.shortfall) + ' comes from ' + b.pn + '.';
          }
          return 'A sole trader and the business are one legal person, so there is no line to stop at.';
        }
        if (r.form === 'unpaid') {
          if (choice === 0) {
            return 'Limited liability caps ' + b.adj + ' loss at what ' + b.pn +
              ' agreed to put in; it does not cancel it.';
          }
          if (choice === b.paidIn) {
            return 'The ' + money(r.unpaid) + ' ' + b.pn + ' agreed to pay and never did is still a debt ' + b.pn + ' owes.';
          }
          return 'Share money agreed but never paid is still owed; a liquidator can call it in.';
        }
        if (choice === 0) {
          return 'Limited liability caps ' + b.adj + ' loss; it does not cancel it.';
        }
        if (choice === r.shortfall) {
          return 'The ' + money(r.shortfall) + ' is the creditors’ loss — an unpaid company debt dies with the company.';
        }
        if (choice === b.paidIn + r.ownTot) {
          return b.adj.charAt(0).toUpperCase() + b.adj.slice(1) +
            ' own things sit outside the company; its creditors have no claim on them.';
        }
        return 'A company is a separate legal person: its debts are its own, not its owner’s.';
      }

      var MASTERY = 'Three in a row — you have it. A company’s debts stop at the company; a sole trader’s stop nowhere.';

      /* -------------------------------------------------------- feedback --- */
      function verdictText(reachOk, lossOk) {
        var b = r.b, ok = reachOk && lossOk;
        var justMastered = ok && st.streak + 1 >= 3 && !st.mastered;
        var tail = justMastered ? MASTERY : mechanism();

        if (ok) {
          return '<b>Right —</b> the creditors reach ' + truthReach() + '. ' + b.owner +
            ' loses ' + money(r.loss) + ': ' + lossGloss() + '. ' + tail;
        }
        var head = '<b>Not quite —</b> you marked ' + describeMarked() + ' and said ' + b.owner +
          ' loses ' + money(choice) + '. ';
        if (reachOk) {
          return head + 'The reach is right. But ' + b.owner + ' still loses ' +
            money(r.loss) + ': ' + lossGloss() + '. ' + tail;
        }
        if (lossOk) {
          return head + 'The loss is right. But the creditors reach ' + truthReach() + '. ' + tail;
        }
        return head + 'The creditors reach ' + truthReach() + '. ' + b.owner + ' loses ' +
          money(r.loss) + '. ' + tail;
      }

      function say(html) { elCap.innerHTML = html; elSr.textContent = elCap.textContent; }

      /* ----------------------------------------------------------- state --- */
      function publish(extra) {
        var s = {
          round: r.b.owner + '/' + r.form, form: r.form,
          marked: Object.keys(marked).sort(), choice: choice,
          phase: committed ? 'checked' : 'answering',
          streak: st.streak, mastered: st.mastered, attempted: st.attempted
        };
        if (extra) for (var k in extra) if (Object.prototype.hasOwnProperty.call(extra, k)) s[k] = extra[k];
        root.dataset.svState = JSON.stringify(s);
      }

      function reachIsRight() {
        var b = r.b, i, id;
        for (i = 0; i < b.co.length; i++) { id = 'c' + i; if (!!marked[id] !== !!r.reach[id]) return false; }
        for (i = 0; i < b.own.length; i++) { id = 'o' + i; if (!!marked[id] !== !!r.reach[id]) return false; }
        return true;
      }

      function syncGo() {
        var any = false, k;
        for (k in marked) if (marked[k]) { any = true; break; }
        elGo.disabled = !(any && choice !== null);
      }

      /* ------------------------------------------------------------ draw --- */
      function tileHTML(id, item) {
        return '<button type="button" class="lb-tile" data-id="' + id + '" aria-pressed="false">' +
          '<span class="lb-n">' + item.n + '</span><span class="lb-v">' + money(item.v) + '</span></button>';
      }

      function buildRound() {
        var b = r.b, i, h;
        elFrame.textContent = r.frame;
        elS1.textContent = 'Which of these can the creditors be paid from?';
        elS2.textContent = 'What does ' + b.owner + ' lose in total?';
        elHeadCo.textContent = b.head + ' · owes ' + money(b.debt);
        elHeadOwn.textContent = b.owner + ' herself';
        if (b.pn === 'he') elHeadOwn.textContent = b.owner + ' himself';

        h = ''; for (i = 0; i < b.co.length; i++) h += tileHTML('c' + i, b.co[i]);
        elCo.innerHTML = h;
        h = ''; for (i = 0; i < b.own.length; i++) h += tileHTML('o' + i, b.own[i]);
        elOwn.innerHTML = h;

        tiles = {};
        var all = root.querySelectorAll('.lb-tile');
        for (i = 0; i < all.length; i++) {
          tiles[all[i].dataset.id] = all[i];
          all[i].addEventListener('click', onTile);
        }

        h = '';
        for (i = 0; i < r.opts.length; i++) {
          h += '<button type="button" class="lb-opt" data-i="' + i + '" aria-pressed="false"><b>' +
            money(r.opts[i].v) + '</b><small>' + r.opts[i].g + '</small></button>';
        }
        elOpts.innerHTML = h;
        elOpts.setAttribute('aria-label', 'What ' + b.owner + ' loses in total');
        optBtns = [];
        var os = root.querySelectorAll('.lb-opt');
        for (i = 0; i < os.length; i++) { optBtns.push(os[i]); os[i].addEventListener('click', onOpt); }
      }

      function revealTiles() {
        var b = r.b, i, id, t, word;
        for (i = 0; i < b.co.length; i++) {
          id = 'c' + i; t = tiles[id];
          t.classList.add('is-gone');
          t.querySelector('.lb-n').textContent = b.co[i].n + ' · sold';
          t.setAttribute('aria-disabled', 'true');
        }
        for (i = 0; i < b.own.length; i++) {
          id = 'o' + i; t = tiles[id];
          word = r.reach[id] ? ' · at risk' : ' · safe';
          if (r.reach[id]) t.classList.add('is-risk');
          t.querySelector('.lb-n').textContent = b.own[i].n + word;
          t.setAttribute('aria-disabled', 'true');
        }
        var breached = false;
        for (i = 0; i < b.own.length; i++) if (r.reach['o' + i]) breached = true;
        root.classList.add(breached ? 'is-breach' : 'is-held');
        for (i = 0; i < optBtns.length; i++) optBtns[i].setAttribute('aria-disabled', 'true');
      }

      function showRun() {
        if (st.mastered) { elRun.textContent = 'You have it.'; return; }
        if (!st.streak) { elRun.textContent = ''; return; }
        elRun.textContent = st.streak + ' right in a row — ' +
          (st.streak === 2 ? 'one more' : (3 - st.streak) + ' more') + '.';
      }

      /* --------------------------------------------------------- handlers --- */
      function onTile(ev) {
        if (committed) return;
        var btn = ev.currentTarget, id = btn.dataset.id;
        marked[id] = !marked[id];
        if (!marked[id]) delete marked[id];
        btn.setAttribute('aria-pressed', marked[id] ? 'true' : 'false');
        var desc = describeMarked();
        say(desc === 'nothing at all'
          ? 'You are saying the creditors can be paid from nothing at all.'
          : 'You are saying the creditors can be paid from ' + desc + '.');
        syncGo();
        publish();
      }

      function onOpt(ev) {
        if (committed) return;
        var btn = ev.currentTarget, i = +btn.dataset.i, k;
        choice = r.opts[i].v;
        for (k = 0; k < optBtns.length; k++) {
          optBtns[k].setAttribute('aria-pressed', optBtns[k] === btn ? 'true' : 'false');
        }
        say('You are saying ' + r.b.owner + ' loses ' + money(choice) + ' in all — ' +
          r.opts[i].g + '.');
        syncGo();
        publish();
      }

      function commit() {
        var reachOk = reachIsRight(), lossOk = choice === r.loss, ok = reachOk && lossOk;
        st.attempted++;
        say(verdictText(reachOk, lossOk));
        st.streak = ok ? st.streak + 1 : 0;
        if (st.streak >= 3) st.mastered = true;
        committed = true;
        revealTiles();
        elGo.textContent = st.mastered ? 'Another anyway' : 'Next business';
        elGo.disabled = false;
        showRun();
        publish({ correct: ok, reachRight: reachOk, lossRight: lossOk, expectedLoss: r.loss });
      }

      function nextRound() {
        if (!queue.length) {
          if (!seeded) { queue = shuffle(POOL); seeded = true; }
          else { queue = shuffle(POOL.concat(FIXED)); }
        }
        r = solve(queue.shift());
        marked = {}; choice = null; committed = false;
        root.classList.remove('is-held'); root.classList.remove('is-breach');
        buildRound();
        elGo.textContent = 'Check';
        elGo.disabled = true;
        showRun();
        say('The business is <b>' + money(r.shortfall) +
          '</b> short of what it owes. That gap has to land on somebody.');
        publish();
      }

      elGo.addEventListener('click', function () {
        if (!committed) { commit(); return; }
        nextRound();
        var first = root.querySelector('.lb-tile');
        if (first) first.focus();
      });

      root.addEventListener('keydown', function (ev) {
        if (ev.key !== 'Escape' || committed) return;
        var any = false, k;
        for (k in marked) if (marked[k]) any = true;
        if (!any && choice === null) return;
        marked = {}; choice = null;
        for (k in tiles) tiles[k].setAttribute('aria-pressed', 'false');
        for (k = 0; k < optBtns.length; k++) optBtns[k].setAttribute('aria-pressed', 'false');
        say('Cleared — mark it again.');
        syncGo();
        publish();
      });

      nextRound();
    }
  };
})();
