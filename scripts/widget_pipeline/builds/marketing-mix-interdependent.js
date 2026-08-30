/* marketing-mix-interdependent
   The four Ps are one decision, not four. A business changes one element of
   its mix; the student predicts which OTHER P is now under the most strain,
   and why — or commits that the mix still holds. Commit before check,
   verdict-first feedback, mastery at three in a row. */
(function () {
  'use strict';

  var P_ORDER = ['product', 'price', 'place', 'promotion'];
  var P_LABEL = {
    product: 'Product', price: 'Price', place: 'Place',
    promotion: 'Promotion', none: 'the mix still holds'
  };

  /* Each round states a forcing fact inside the mix itself (a cost, a cut, a
     customer who cannot travel), so exactly one other P is genuinely trapped. */
  var ROUNDS = [
    {
      id: 'jewellery',
      market: 'Buyers of 25–40 who want a piece nobody else owns, and will pay for the maker’s time.',
      mix: {
        product: 'One at a time · 3 hrs · £22 silver',
        price: '£95 a piece',
        place: 'Craft fairs and its own website',
        promotion: 'Instagram films from the workshop'
      },
      changed: { price: '£29 a piece' },
      frame: 'Loom & Lark has cut its price from £95 to £29 to chase fashion buyers. Which other P is now under strain — or does the mix hold?',
      answer: 'product',
      reasons: [
        { t: '£29 cannot pay for 3 hrs and £22 of silver.', ok: true },
        { t: 'A lower price always widens the market.',
          no: 'Cheaper does widen a market — but only if the thing sold can still be made for the money. At £29 it cannot, so the pieces must be batch-cast.' },
        { t: 'The stall will need more room for stock.',
          no: 'Stand size is a detail. The sum that has broken is £22 of silver plus three hours of work against £29, which forces the product to change.' }
      ],
      right: 'The strain lands on Product: at £29 the pieces have to be cast in batches, and a batch-cast piece is no longer the one-off this buyer paid £95 for. Price never moves on its own — it drags the product behind it.',
      fb: {
        price: '',
        place: 'Craft fairs and a website will sell £29 jewellery quite happily — nothing about the new price shuts a stall. What £29 cannot pay for is £22 of silver plus three hours at the bench, so Product gives first.',
        promotion: 'The workshop films are still honest today. They only become a lie once the pieces are batch-cast — and that is the real pressure: Product has to change before Promotion does.',
        none: '£29 does not cover £22 of silver plus three hours of work, so something must give: the pieces become batch-cast and the one-off that justified £95 disappears. A price cut is never free — one of the other three Ps pays for it.'
      }
    },
    {
      id: 'desks',
      market: 'Students and first-flat renters furnishing a whole room for under £100.',
      mix: {
        product: 'Plain flat-pack desk · £38 to make',
        price: '£59 delivered · £9 to send',
        place: 'Its own website only',
        promotion: 'TikTok clips of the 20-minute build'
      },
      changed: { place: 'Store concession · cheapest desk £400' },
      frame: 'Foldwork now sells through a store that keeps 40p in every £1. Which other P is now under strain — or does the mix hold?',
      answer: 'price',
      reasons: [
        { t: '£35.40 kept, against £47 of cost.', ok: true },
        { t: 'Store shoppers buy on impulse anyway.',
          no: 'Stopping the clips is a choice, not a pressure. The thing that has broken is arithmetic: £35.40 kept out of £59, against £47 of cost.' },
        { t: 'A flat-pack desk does not need a shop.',
          no: 'The concession is already signed and it takes 40p in every £1. That is the change, and Price is the P that has to answer it.' }
      ],
      right: 'Place drags Price behind it: £59 leaves Foldwork £35.40 once the store takes its cut, against £47 to make and deliver. Lift the price to cover that and the desk climbs away from the under-£100 renter it was built for — and beside £400 desks it already looks like the cheap one. Place is never just a shelf.',
      fb: {
        place: '',
        product: 'The desk itself still suits the buyer — the timber and the 20-minute build have not moved. What has moved is that 40p in every £1 now leaves the till, so £59 no longer covers the £47 it costs to make and send.',
        promotion: 'The TikTok clips still reach the same renter, and the store does not stop them. The break is arithmetic: £35.40 kept against £47 of cost, so Price is the P under strain.',
        none: '40p in every £1 out of £59 leaves £35.40 against £47 of cost — a loss on every desk. Place has pulled Price out of line, so the mix cannot stand still.'
      }
    },
    {
      id: 'icecream',
      market: 'Farm-shop and deli shoppers who buy a treat and read the label.',
      mix: {
        product: 'Farmhouse ice cream, plain tub',
        price: '£4.50 a tub',
        place: 'Twelve farm shops and delis',
        promotion: 'Tasting stands and a recipe card'
      },
      changed: { price: '£6.00 a tub', product: 'Named herd, printed lidded tub' },
      frame: 'Two Fields has gone from £4.50 to £6.00, in a printed tub naming the herd. Which other P is now under strain — or does the mix hold?',
      answer: 'none',
      reasons: [
        { t: 'A better product now justifies the price.', ok: true },
        { t: 'Farm shops never argue about a price rise.',
          no: 'Shops do argue, and a rise is not automatically safe. What makes this one safe is that the shopper is handed more in return for the extra £1.50.' },
        { t: 'A tasting stand makes any price look fair.',
          no: 'A stand helps, but it cannot rescue a price the product has not earned. Here the product has earned it, which is why nothing else is trapped.' }
      ],
      right: 'Both moves point at the same shopper: the person who reads the label is asked for £1.50 more and handed a named herd to read about. A deli is still where she stands, and a tasting stand is still how she decides. A mix only breaks when one P is pulled away from the customer the other three were chosen for.',
      fb: {
        place: 'Place is worth testing, and it holds: a deli is exactly where a label-reader stands, and £6.00 is an ordinary deli price. Nothing here has been pulled away from that shopper — the mix still holds.',
        promotion: 'A tasting stand works better at £6.00 than at £4.50: the taste is the argument for the extra £1.50. Nothing has been pulled away from the label-reading shopper — the mix still holds.'
      }
    },
    {
      id: 'bikes',
      market: 'Commuters who need the bike back the same day and cannot take it anywhere.',
      mix: {
        product: 'Van comes to you · 40-minute service',
        price: '£35 at the kerb',
        place: 'Your street, within four miles',
        promotion: 'Cards through doors on the four-mile ring'
      },
      changed: { place: 'A unit on an estate, six miles out' },
      frame: 'Kerbside has parked the van and moved into a unit six miles out. Which other P is now under strain — or does the mix hold?',
      answer: 'product',
      reasons: [
        { t: 'This customer cannot bring the bike anywhere.', ok: true },
        { t: 'A unit has room for more bikes a day.',
          no: 'True, and beside the point for this customer: she still cannot get the bike to the unit, so what is being sold has to change.' },
        { t: 'Door cards are cheap, so they can stay.',
          no: 'The cards can carry on — but they would advertise a doorstep service Kerbside no longer performs. The product has to change before the cards do.' }
      ],
      right: 'Place was not a detail here — it WAS the product. “We come to you, back on the road in 40 minutes” dies the moment the customer has to ride six miles and leave the bike overnight. What is left is an ordinary repair shop, and £35 has to be re-argued against every other shop in town.',
      fb: {
        place: '',
        price: 'Price does come under pressure, but only because the thing being priced has changed. The first casualty is Product: “we come to you” cannot survive a unit six miles from a commuter who cannot travel.',
        promotion: 'The door cards are cheap and still reach the same streets — but they would now advertise a service Kerbside cannot give. Product changes first; Promotion only has to follow it.',
        none: 'This customer was chosen because she cannot take the bike anywhere. Move the work six miles out and the doorstep service — the product itself — is gone. Place and Product were the same decision all along.'
      }
    },
    {
      id: 'skincare',
      market: 'Shoppers who buy one good bottle a year and want to be told what is in it.',
      mix: {
        product: 'One 50ml serum, six ingredients',
        price: '£48 a bottle',
        place: 'Own site and nine independent chemists',
        promotion: 'A pharmacist’s write-up of each ingredient'
      },
      changed: { promotion: '48-hour “3 for 2” countdown ads' },
      frame: 'Halcyon Skin has swapped its write-ups for a “3 for 2” countdown. Which other P is now under strain — or does the mix hold?',
      answer: 'price',
      reasons: [
        { t: 'Three for two makes the real price £32.', ok: true },
        { t: 'Urgency sells more, and volume fixes margin.',
          no: 'More bottles at £32 is not the same as more money, and the shopper who paid £48 last month has just been taught to wait for the next countdown.' },
        { t: 'Chemists cannot run social media offers.',
          no: 'They can run them, and some will. The damage is to the £48 itself: three for two makes the real price £32.' }
      ],
      right: 'A countdown deal is a price cut wearing Promotion’s clothes: three for two makes the real price £32, and once a shopper has seen one, £48 is simply a number to wait out. The write-ups were what justified £48 in the first place, so the brand has traded its reason for its price.',
      fb: {
        promotion: '',
        product: 'The six ingredients are unchanged — nothing inside the bottle has moved. What has moved is the price a shopper actually pays: three for two makes it £32, so Price is where the strain lands.',
        place: 'The nine chemists will not enjoy being undercut, but they can still stock it. The number that has stopped being true is £48 — three for two makes the real price £32.',
        none: 'Three for two is a price cut wearing Promotion’s clothes. The real price is now £32, and a shopper who has seen one countdown will wait for the next, so £48 cannot stand as it was.'
      }
    },
    {
      id: 'granola',
      market: 'Trolley shoppers who want breakfast for the week for under £3.',
      mix: {
        product: '500g plain oat granola · 95p to make',
        price: '£2.60 shelf · £1.55 to the maker',
        place: 'Two supermarket chains, cereal aisle',
        promotion: 'Shelf-edge offers, 3 bags for £7'
      },
      changed: { product: 'Raspberry and honey · £1.90 to make' },
      frame: 'Brackenfield’s new recipe costs £1.90 a bag to make, not 95p. Which other P is now under strain — or does the mix hold?',
      answer: 'price',
      reasons: [
        { t: '£1.90 of cost against £1.55 of income.', ok: true },
        { t: 'Better ingredients sell themselves.',
          no: 'They may well sell — at a loss of 35p a bag. Every bag sold now costs more to make than it earns, so the shelf price cannot stay put.' },
        { t: 'Trolley shoppers never read the shelf edge.',
          no: 'Shelf-edge offers work either way, and 3 for £7 makes the loss bigger. What has broken is £1.90 of cost against £1.55 of income.' }
      ],
      right: 'Product pushes Price: the maker now spends £1.90 to earn £1.55, so the shelf price has to climb towards £4.50. And there is the second lesson — at £4.50 this is no longer breakfast for under £3, so the customer in the middle changes too. Push one P far enough and you change who you are selling to.',
      fb: {
        product: '',
        place: 'Both chains will keep the listing; nothing about the recipe loses it. What cannot survive is £1.90 of cost against £1.55 of income, so Price is the P under strain.',
        promotion: 'The shelf-edge offers still reach the same trolley — and 3 bags for £7 makes the loss bigger, not smaller. The break is £1.90 of cost against £1.55 of income.',
        none: '£1.90 of cost against £1.55 of income is a loss on every bag, so Price cannot stand still. A better product is not free: it is paid for out of Price, and often out of the customer you had.'
      }
    }
  ];

  var CSS = [
    '.svw-mmi{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;font-size:16px;line-height:1.5}',
    '.svw-mmi *{box-sizing:border-box}',
    '.svw-mmi .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .18rem}',
    '.svw-mmi h3{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;margin:0;line-height:1.2}',
    '.svw-mmi .frame{font-size:.84rem;line-height:1.45;margin:.3rem 0 .55rem;color:#3d3934}',
    '.svw-mmi .board{position:relative;background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;padding:.5rem;display:grid;grid-template-columns:1fr 1fr;gap:.7rem}',
    '.svw-mmi .ov{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0}',
    '.svw-mmi .p{position:relative;z-index:1;text-align:left;background:#fff;border:1px solid #e0d9cd;border-radius:10px;padding:.34rem .45rem;font:inherit;cursor:pointer;color:#2d2a26}',
    '.svw-mmi .p .n{display:block;font-size:.66rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8d8880}',
    '.svw-mmi .p .v{display:block;font-size:.78rem;line-height:1.26;margin-top:.08rem}',
    '.svw-mmi .p[data-sel="1"]{border-color:#2d2a26;box-shadow:inset 0 0 0 1px #2d2a26}',
    '.svw-mmi .p[data-chg="1"]{border-style:dashed;cursor:default}',
    '.svw-mmi .p[data-chg="1"] .n:after{content:" · changed";letter-spacing:.04em;color:var(--mmi-a)}',
    '.svw-mmi .p[data-strain="1"]{border-color:var(--mmi-a);box-shadow:inset 0 0 0 1px var(--mmi-a)}',
    '.svw-mmi .p[data-miss="1"]{border-style:dotted;border-color:#8d8880}',
    '.svw-mmi .mkt{position:relative;z-index:1;grid-column:1/-1;background:#fff;border:1px solid #e0d9cd;border-radius:10px;padding:.4rem .55rem}',
    '.svw-mmi .mkt[data-fit="1"]{border-color:#4f7d63;box-shadow:inset 0 0 0 1px #4f7d63}',
    '.svw-mmi .mkt[data-test="1"]{border-color:var(--mmi-a);box-shadow:inset 0 0 0 1px var(--mmi-a)}',
    '.svw-mmi .mkt .n{display:block;font-size:.66rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}',
    '.svw-mmi .mkt .v{display:block;font-size:.78rem;line-height:1.35;margin-top:.1rem}',
    '.svw-mmi .none{display:block;width:100%;margin-top:.45rem;text-align:left}',
    '.svw-mmi .btn{font:inherit;font-size:.82rem;font-weight:600;padding:.42rem .8rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;line-height:1.3}',
    '.svw-mmi .btn[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-mmi .btn:disabled{opacity:.5;cursor:default}',
    '.svw-mmi .why{margin-top:.5rem}',
    '.svw-mmi .why .lab{font-size:.7rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#8d8880;margin:0 0 .25rem}',
    '.svw-mmi .why .btn{display:block;width:100%;text-align:left;margin-bottom:.26rem;font-weight:500;padding:.3rem .55rem}',
    '.svw-mmi .why .btn[aria-pressed="true"]{font-weight:600}',
    '.svw-mmi .go{display:flex;align-items:center;gap:.6rem;margin-top:.5rem;flex-wrap:wrap}',
    '.svw-mmi .go .run{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-mmi .streak{font-size:.76rem;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svw-mmi .cap{font-size:.84rem;line-height:1.45;margin:.5rem 0 0;min-height:1.6rem;color:#2d2a26}',
    '.svw-mmi .cap b{font-weight:700}',
    '.svw-mmi .hide{display:none}',
    '.svw-mmi .sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svw-mmi.mo .p,.svw-mmi.mo .btn,.svw-mmi.mo .mkt{transition:border-color .16s ease,box-shadow .16s ease,background .16s ease}'
  ].join('\n');

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }

  window.SVWidget = {
    meta: {
      id: 'marketing-mix-interdependent',
      title: 'Change one P, test the mix',
      teaches: 'The four Ps are one joined-up decision: change one and the others come under pressure, and the test of a mix is whether all four still point at the same target market.'
    },
    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || '#8a6a4f';
      try {
        var got = getComputedStyle(root).getPropertyValue('--accent');
        if (got && got.trim()) accent = got.trim();
      } catch (e) {}

      var wrap = el('div', 'svw-mmi' + (ctx.reducedMotion ? '' : ' mo'));
      wrap.style.setProperty('--mmi-a', accent);
      var style = document.createElement('style');
      style.textContent = CSS;
      wrap.appendChild(style);

      /* ---- header ---- */
      var kick = el('p', 'k', 'Marketing mix');
      kick.style.color = accent;
      wrap.appendChild(kick);
      wrap.appendChild(el('h3', null, 'Change one P, test the mix'));
      var frame = el('p', 'frame');
      wrap.appendChild(frame);

      /* ---- stage: the mix board ---- */
      var board = el('div', 'board');
      var ov = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      ov.setAttribute('class', 'ov');
      ov.setAttribute('preserveAspectRatio', 'none');
      var links = [];
      for (var s = 0; s < 4; s++) {
        var ln = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        ln.setAttribute('stroke-width', '2.5');
        ln.setAttribute('stroke-linecap', 'round');
        ln.setAttribute('opacity', '0');
        ov.appendChild(ln); links.push(ln);
      }
      var head = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
      head.setAttribute('opacity', '0');
      ov.appendChild(head);
      board.appendChild(ov);

      var cards = {};
      function addCard(key) {
        var b = el('button', 'p');
        b.type = 'button';
        b.appendChild(el('span', 'n', P_LABEL[key]));
        var v = el('span', 'v');
        b.appendChild(v);
        b.addEventListener('click', function () { pick(key); });
        cards[key] = { btn: b, v: v };
        board.appendChild(b);
      }
      addCard('product'); addCard('price');
      var mkt = el('div', 'mkt');
      var mktN = el('span', 'n', 'Target market');
      mktN.style.color = accent;
      var mktV = el('span', 'v');
      mkt.appendChild(mktN); mkt.appendChild(mktV);
      board.appendChild(mkt);
      addCard('place'); addCard('promotion');
      wrap.appendChild(board);

      /* ---- controls ---- */
      var noneBtn = el('button', 'btn none', 'The mix still holds — nothing else changes');
      noneBtn.type = 'button';
      noneBtn.setAttribute('aria-pressed', 'false');
      noneBtn.addEventListener('click', function () { pick('none'); });
      wrap.appendChild(noneBtn);

      var why = el('div', 'why hide');
      why.appendChild(el('p', 'lab', 'Because'));
      var rBtns = [];
      for (var r = 0; r < 3; r++) {
        (function (i) {
          var b = el('button', 'btn');
          b.type = 'button';
          b.setAttribute('aria-pressed', 'false');
          b.addEventListener('click', function () { pickReason(i); });
          why.appendChild(b); rBtns.push(b);
        })(r);
      }
      wrap.appendChild(why);

      var go = el('div', 'go');
      var runBtn = el('button', 'btn run', 'Check the mix');
      runBtn.type = 'button';
      runBtn.disabled = true;
      runBtn.addEventListener('click', commit);
      var nextBtn = el('button', 'btn hide', 'Next scenario');
      nextBtn.type = 'button';
      nextBtn.addEventListener('click', function () { nextRound(); });
      var streakEl = el('span', 'streak', '');
      go.appendChild(runBtn); go.appendChild(nextBtn); go.appendChild(streakEl);
      wrap.appendChild(go);

      var cap = el('p', 'cap');
      wrap.appendChild(cap);
      var sr = el('div', 'sr');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      root.appendChild(wrap);

      /* ---- state ---- */
      var order = ROUNDS.slice();
      for (var i = order.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var t = order[i]; order[i] = order[j]; order[j] = t;
      }
      var idx = 0, round = null, picked = null, reason = null;
      var committed = false, lastCorrect = null;
      var streak = 0, attempted = 0, mastered = false;

      function state() {
        root.dataset.svState = JSON.stringify({
          round: round ? round.id : null,
          picked: picked, reason: reason,
          committed: committed, correct: lastCorrect,
          streak: streak, mastered: mastered, attempted: attempted
        });
      }

      function isChanged(key) { return round && Object.prototype.hasOwnProperty.call(round.changed, key); }

      function loadRound() {
        round = order[idx % order.length];
        picked = null; reason = null; committed = false; lastCorrect = null;
        frame.textContent = round.frame;
        mktV.textContent = round.market;
        mkt.removeAttribute('data-fit');
        mkt.removeAttribute('data-test');
        P_ORDER.forEach(function (key) {
          var c = cards[key];
          if (isChanged(key)) {
            c.v.textContent = round.changed[key];
            c.btn.setAttribute('data-chg', '1');
            c.btn.disabled = true;
          } else {
            c.v.textContent = round.mix[key];
            c.btn.removeAttribute('data-chg');
            c.btn.disabled = false;
          }
          c.btn.removeAttribute('data-sel');
          c.btn.removeAttribute('data-strain');
          c.btn.removeAttribute('data-miss');
          c.btn.setAttribute('aria-pressed', 'false');
        });
        noneBtn.classList.remove('hide');
        noneBtn.disabled = false;
        noneBtn.setAttribute('aria-pressed', 'false');
        for (var k = 0; k < 3; k++) {
          rBtns[k].textContent = round.reasons[k].t;
          rBtns[k].setAttribute('aria-pressed', 'false');
          rBtns[k].disabled = false;
        }
        why.classList.add('hide');
        runBtn.classList.remove('hide');
        runBtn.disabled = true;
        nextBtn.classList.add('hide');
        links.forEach(function (l) { l.setAttribute('opacity', '0'); });
        head.setAttribute('opacity', '0');
        mkt.removeAttribute('data-test');
        cap.textContent = 'Each P here was chosen for one customer.';
        updateStreak();
        state();
      }

      function pick(key) {
        if (committed || isChanged(key)) return;
        picked = key;
        P_ORDER.forEach(function (k) {
          var on = (k === key);
          if (on) cards[k].btn.setAttribute('data-sel', '1');
          else cards[k].btn.removeAttribute('data-sel');
          cards[k].btn.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        noneBtn.setAttribute('aria-pressed', key === 'none' ? 'true' : 'false');
        if (key === 'none') noneBtn.setAttribute('data-sel', '1');
        why.classList.remove('hide');
        runBtn.disabled = (reason === null);
        cap.textContent = 'Under strain: ' + P_LABEL[key] + '.';
        sr.textContent = P_LABEL[key] + ' chosen as the P under strain.';
        state();
      }

      function pickReason(i) {
        if (committed) return;
        reason = i;
        for (var k = 0; k < 3; k++) rBtns[k].setAttribute('aria-pressed', k === i ? 'true' : 'false');
        runBtn.disabled = (picked === null);
        state();
      }

      function updateStreak() {
        if (mastered) streakEl.textContent = streak + ' in a row.';
        else if (streak === 1) streakEl.textContent = '1 right in a row.';
        else if (streak === 2) streakEl.textContent = '2 right in a row — one more and you have it.';
        else streakEl.textContent = '';
      }

      function box(n) {
        return { l: n.offsetLeft, t: n.offsetTop, r: n.offsetLeft + n.offsetWidth,
                 b: n.offsetTop + n.offsetHeight,
                 cx: n.offsetLeft + n.offsetWidth / 2, cy: n.offsetTop + n.offsetHeight / 2 };
      }
      /* how far along the ray it leaves the rectangle it started in */
      function exitT(r, x, y, dx, dy) {
        var tx = dx > 0 ? (r.r - x) / dx : (dx < 0 ? (r.l - x) / dx : Infinity);
        var ty = dy > 0 ? (r.b - y) / dy : (dy < 0 ? (r.t - y) / dy : Infinity);
        return Math.min(tx, ty);
      }
      /* draw connector i in the visible gap between boxes A and B */
      function link(i, A, B, colour, dashed, arrow) {
        var a = box(A), b = box(B);
        var dx = b.cx - a.cx, dy = b.cy - a.cy;
        var len = Math.sqrt(dx * dx + dy * dy) || 1;
        var ux = dx / len, uy = dy / len;
        var t1 = exitT(a, a.cx, a.cy, dx, dy);
        var t2 = exitT(b, b.cx, b.cy, -dx, -dy);
        var x1 = a.cx + dx * t1 + ux * 2, y1 = a.cy + dy * t1 + uy * 2;
        var x2 = b.cx - dx * t2 - ux * 2, y2 = b.cy - dy * t2 - uy * 2;
        var ln = links[i];
        ln.setAttribute('x1', x1); ln.setAttribute('y1', y1);
        ln.setAttribute('x2', x2); ln.setAttribute('y2', y2);
        ln.setAttribute('stroke', colour);
        if (dashed) ln.setAttribute('stroke-dasharray', '3 3');
        else ln.removeAttribute('stroke-dasharray');
        ln.setAttribute('opacity', '.95');
        if (arrow) {
          var px = -uy, py = ux;
          head.setAttribute('points',
            (x2 + ux * 1) + ',' + (y2 + uy * 1) + ' ' +
            (x2 - ux * 7 + px * 4.5) + ',' + (y2 - uy * 7 + py * 4.5) + ' ' +
            (x2 - ux * 7 - px * 4.5) + ',' + (y2 - uy * 7 - py * 4.5));
          head.setAttribute('fill', colour);
          head.setAttribute('opacity', '.95');
        }
      }

      function draw() {
        if (!committed || !round) return;
        var w = board.clientWidth, h = board.clientHeight;
        if (!w || !h) return;
        ov.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
        links.forEach(function (l) { l.setAttribute('opacity', '0'); });
        head.setAttribute('opacity', '0');
        if (round.answer === 'none') {
          P_ORDER.forEach(function (key, n) { link(n, cards[key].btn, mkt, '#4f7d63', true, false); });
          mkt.setAttribute('data-fit', '1');
        } else {
          var n = 0;
          for (var key in round.changed) { link(n++, cards[key].btn, mkt, accent, false, false); }
          link(n, mkt, cards[round.answer].btn, accent, false, true);
          mkt.setAttribute('data-test', '1');
        }
      }

      function commit() {
        if (committed || picked === null || reason === null) return;
        committed = true;
        attempted++;
        var rightP = (picked === round.answer);
        var rightR = !!round.reasons[reason].ok;
        lastCorrect = rightP && rightR;
        var quoted = '“' + round.reasons[reason].t.replace(/\.$/, '') + '”';
        var said = (picked === 'none') ? 'you said the mix still holds'
                                       : 'you picked ' + P_LABEL[picked];
        var msg;
        if (lastCorrect) {
          msg = 'Right — ' + said + ', because ' + quoted + '. ' + round.right;
          streak++;
          if (streak >= 3 && !mastered) {
            mastered = true;
            msg += ' Three in a row — you have it: the four Ps are one decision, and the test is whether all four still point at the same customer.';
          }
        } else if (rightP) {
          msg = 'Not quite — ' + (picked === 'none' ? 'the mix does hold'
                : P_LABEL[picked] + ' is right') + ', but not for the reason you gave: ' +
                quoted + '. ' + round.reasons[reason].no;
          streak = 0;
        } else {
          msg = 'Not quite — ' + said + ', because ' + quoted + '. ' + round.fb[picked];
          streak = 0;
        }
        cap.textContent = msg;
        sr.textContent = msg;

        P_ORDER.forEach(function (k) { cards[k].btn.disabled = true; });
        if (picked !== 'none' && !rightP) cards[picked].btn.setAttribute('data-miss', '1');
        if (round.answer !== 'none') {
          cards[round.answer].btn.setAttribute('data-strain', '1');
          for (var key in round.changed) cards[key].btn.setAttribute('data-strain', '1');
        }
        noneBtn.disabled = true;
        for (var k2 = 0; k2 < 3; k2++) rBtns[k2].disabled = true;
        why.classList.add('hide');
        noneBtn.classList.add('hide');
        runBtn.classList.add('hide');
        nextBtn.textContent = mastered ? 'Another anyway' : 'Next scenario';
        nextBtn.classList.remove('hide');
        updateStreak();
        draw();
        state();
        try { nextBtn.focus({ preventScroll: true }); } catch (e) {}
      }

      function nextRound() {
        idx++;
        loadRound();
        try { cards[P_ORDER[0]].btn.focus({ preventScroll: true }); } catch (e) {}
      }

      wrap.addEventListener('keydown', function (ev) {
        if (ev.key === 'Escape' && !committed && picked !== null) {
          picked = null; reason = null;
          P_ORDER.forEach(function (k) {
            cards[k].btn.removeAttribute('data-sel');
            cards[k].btn.setAttribute('aria-pressed', 'false');
          });
          noneBtn.removeAttribute('data-sel');
          noneBtn.setAttribute('aria-pressed', 'false');
          for (var k = 0; k < 3; k++) rBtns[k].setAttribute('aria-pressed', 'false');
          why.classList.add('hide');
          runBtn.disabled = true;
          cap.textContent = 'Each P here was chosen for one customer.';
          state();
        }
      });

      window.addEventListener('resize', draw);
      loadRound();
    }
  };
})();
