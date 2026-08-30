/* Vertical vs horizontal integration - where a takeover sits on the chain.
   Self-contained. No network, no storage, no eval.

   Firms are named by what they DO ("the studio", "a cinema chain"), never by
   invented brand, so nothing has to be memorised before the idea can be met.
   Round one asks one question; the second part arrives once the footing is there. */
(function () {
  'use strict';

  var EM = '—', LQ = '“', RQ = '”';

  /* Drawn top to bottom, so "along the chain" really is vertical on screen
     and "the same stage" really is horizontal. */
  var CHAIN = [
    { id: 'prod',  n: '1', label: 'Production',   gloss: 'films get made' },
    { id: 'dist',  n: '2', label: 'Distribution', gloss: 'films get sold on' },
    { id: 'exhib', n: '3', label: 'Exhibition',   gloss: 'audiences watch' }
  ];

  var POWER_MISS = {
    down:  'Control of where films get shown comes from owning the stage that puts them in front of an audience.',
    up:    'A supply of films comes from owning the stage that makes them, when you are the one doing the showing.',
    share: 'A bigger share of one stage comes from buying a firm that does the same job as you.'
  };

  var ROUNDS = [
    {
      deal: 'A film studio wants to buy a cinema chain.',
      buyer: { role: 'the studio', stage: 'prod' },
      target: { role: 'a cinema chain', stage: 'exhib' },
      kind: 'vertical', power: 'down',
      opts: {
        down:  'Control of where its films get shown',
        up:    'A supply of films to show',
        share: 'A bigger share of film-making'
      },
      why: 'The studio makes films at stage 1; the cinema chain shows them at stage 3. Buying at a different stage of the same chain is <strong>vertical integration</strong>, and it gives the studio control of where its own films get shown.'
    },
    {
      deal: 'A film studio wants to buy a rival film studio.',
      buyer: { role: 'the studio', stage: 'prod' },
      target: { role: 'a rival studio', stage: 'prod' },
      kind: 'horizontal', power: 'share',
      opts: {
        share: 'A bigger share of film-making',
        down:  'Control of where its films get shown',
        up:    'A supply of films to show'
      },
      why: 'Both firms make films at stage 1. Buying at the same stage is <strong>horizontal integration</strong>: it adds the rival' + '’' + 's output to the studio' + '’' + 's own and removes a competitor for the same scripts, stars and audiences.'
    },
    {
      deal: 'A film studio wants to buy the distributor that sells its films to cinemas.',
      buyer: { role: 'the studio', stage: 'prod' },
      target: { role: 'the distributor', stage: 'dist' },
      kind: 'vertical', power: 'down',
      opts: {
        down:  'Control of how its films reach cinemas',
        share: 'A bigger share of film-making',
        up:    'A supply of films to show'
      },
      why: 'The studio makes films at stage 1; the distributor sells them on at stage 2. Buying along the chain is <strong>vertical integration</strong>, and the studio stops paying another firm to get its films into cinemas. Owning stage after stage this way is how a <strong>conglomerate</strong> comes to control the whole route from camera to screen.'
    },
    {
      deal: 'A streaming service wants to buy a film studio.',
      buyer: { role: 'the service', stage: 'exhib' },
      target: { role: 'a film studio', stage: 'prod' },
      kind: 'vertical', power: 'up',
      opts: {
        up:    'Its own supply of films to stream',
        down:  'Control of where its films get shown',
        share: 'A bigger share of streaming'
      },
      why: 'The service shows films at stage 3; the studio makes them at stage 1. Buying back up the chain is <strong>vertical integration</strong>, and it gives the service films of its own that no rival can outbid it for.'
    },
    {
      deal: 'A huge film studio wants to buy a tiny two-person studio.',
      buyer: { role: 'the huge studio', stage: 'prod' },
      target: { role: 'the tiny studio', stage: 'prod' },
      kind: 'horizontal', power: 'share',
      opts: {
        share: 'A bigger share of film-making',
        down:  'Control of where its films get shown',
        up:    'A supply of films to show'
      },
      why: 'Size is not the test: both firms make films at stage 1. The same stage makes this <strong>horizontal integration</strong>, and it adds the small studio' + '’' + 's films to the big one' + '’' + 's share of film-making.'
    },
    {
      deal: 'A small film studio wants to buy a 200-screen cinema chain.',
      buyer: { role: 'the small studio', stage: 'prod' },
      target: { role: 'the cinema chain', stage: 'exhib' },
      kind: 'vertical', power: 'down',
      opts: {
        down:  'Guaranteed screens for its own films',
        share: 'A bigger share of film-making',
        up:    'A supply of films to show'
      },
      why: 'Size is not the test: the studio makes films at stage 1, the chain shows them at stage 3. Different stages make this <strong>vertical integration</strong>, and it guarantees the studio' + '’' + 's films the screens they need.'
    },
    {
      deal: 'A streaming service wants to buy a rival streaming service.',
      buyer: { role: 'the service', stage: 'exhib' },
      target: { role: 'a rival service', stage: 'exhib' },
      kind: 'horizontal', power: 'share',
      opts: {
        share: 'A bigger share of streaming',
        up:    'Its own supply of films to stream',
        down:  'Control of where its films get shown'
      },
      why: 'Both firms show films to audiences at stage 3, so this is <strong>horizontal integration</strong>. The rival' + '’' + 's subscribers transfer across, growing the service' + '’' + 's share of streaming and removing somewhere else for viewers to go.'
    }
  ];

  var CSS = [
    '.svw-vhi{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45;-webkit-text-size-adjust:100%}',
    '.svw-vhi *{box-sizing:border-box}',
    '.svw-vhi [hidden]{display:none !important}',
    '.svw-vhi p{margin:0}',
    '.svw-vhi .vhi-kicker{font-size:.66rem;line-height:1.2;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--vhi-a)}',
    '.svw-vhi .vhi-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;margin:.1rem 0 .18rem;line-height:1.2}',
    '.svw-vhi .vhi-frame{font-size:.82rem;line-height:1.4;color:#5b564e}',
    '.svw-vhi .vhi-stage{margin-top:.5rem;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.55rem .6rem}',
    '.svw-vhi .vhi-deal{font-size:.92rem;line-height:1.35;font-weight:600;margin-bottom:.45rem}',
    '.svw-vhi .vhi-row{display:flex;flex-wrap:wrap;align-items:center;gap:.16rem .5rem;border-radius:9px;padding:.2rem .3rem;margin:0 -.3rem}',
    '.svw-vhi .vhi-row + .vhi-row{margin-top:.2rem}',
    '.svw-vhi .vhi-row.is-live{background:var(--vhi-band)}',
    '.svw-vhi .vhi-rowlab{flex:0 0 auto;font-size:.68rem;line-height:1.35;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#8d8880}',
    '.svw-vhi .vhi-rowlab .vhi-gloss{font-weight:500;letter-spacing:0;text-transform:none}',
    '.svw-vhi .vhi-blocks{flex:1 1 17rem;display:flex;flex-wrap:wrap;align-items:center;gap:.26rem}',
    '.svw-vhi .vhi-firm{font-size:.74rem;line-height:1.35;padding:.18rem .45rem;border-radius:8px;border:1px solid #e0d9cd;background:#fff;color:#2d2a26;white-space:nowrap;font-weight:600}',
    '.svw-vhi .vhi-firm.is-buyer{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-vhi .vhi-firm.is-target{border:1px dashed var(--vhi-a);background:var(--vhi-tint)}',
    '.svw-vhi .vhi-other{width:26px;height:15px;border-radius:5px;background:#ece7de;border:1px solid #e4ded4}',
    '.svw-vhi .vhi-steps{margin-top:.5rem}',
    '.svw-vhi .vhi-step + .vhi-step{margin-top:.4rem}',
    '.svw-vhi .vhi-steplab{font-size:.74rem;line-height:1.35;font-weight:600;color:#5b564e;margin-bottom:.2rem}',
    '.svw-vhi .vhi-num{display:inline-block;min-width:1.05rem;height:1.05rem;line-height:1.05rem;text-align:center;border-radius:50%;background:var(--vhi-tint);color:var(--vhi-a);font-size:.66rem;font-weight:700;margin-right:.25rem}',
    '.svw-vhi .vhi-kinds{display:flex;flex-wrap:wrap;gap:.3rem}',
    '.svw-vhi .vhi-opts{display:flex;flex-direction:column;gap:.24rem}',
    '.svw-vhi .vhi-btn{font:inherit;font-size:.8rem;line-height:1.3;font-weight:600;text-align:left;padding:.34rem .65rem;border-radius:9px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer}',
    '.svw-vhi .vhi-btn.is-on{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-vhi .vhi-actions{display:flex;align-items:center;gap:.5rem;margin-top:.5rem}',
    '.svw-vhi .vhi-onward{margin-top:.55rem}',
    '.svw-vhi .vhi-go{font:inherit;font-size:.82rem;line-height:1.3;font-weight:600;padding:.45rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-vhi .vhi-go[disabled]{background:#faf8f5;border-color:#ddd7cd;color:#8d8880;cursor:default}',
    '.svw-vhi .vhi-next{font:inherit;font-size:.82rem;line-height:1.3;font-weight:600;padding:.45rem .95rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer}',
    '.svw-vhi .vhi-cap{font-size:.84rem;line-height:1.5;margin-top:.45rem;min-height:1.5em;color:#2d2a26}',
    '.svw-vhi .vhi-cap .vhi-run{color:#8d8880}',
    '.svw-vhi .vhi-cap .vhi-mast{color:#4f7d63;font-weight:600}',
    '.svw-vhi .vhi-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
  ].join('');

  function rgba(hex, a) {
    var h = String(hex || '').trim().replace('#', '');
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    if (!/^[0-9a-fA-F]{6}$/.test(h)) return 'rgba(138,106,79,' + a + ')';
    return 'rgba(' + parseInt(h.slice(0, 2), 16) + ',' + parseInt(h.slice(2, 4), 16) + ',' +
           parseInt(h.slice(4, 6), 16) + ',' + a + ')';
  }

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }

  function stageName(id) {
    for (var i = 0; i < CHAIN.length; i++) if (CHAIN[i].id === id) return CHAIN[i].label.toLowerCase();
    return id;
  }

  window.SVWidget = {
    meta: {
      id: 'vertical-vs-horizontal-integration',
      title: 'Which kind of integration?',
      teaches: 'Vertical integration buys a firm at a different stage of the supply chain; horizontal integration buys one at the same stage, and each buys a different power.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';

      var wrap = el('div', 'svw-vhi');
      wrap.style.setProperty('--vhi-a', accent);
      wrap.style.setProperty('--vhi-tint', rgba(accent, 0.13));
      wrap.style.setProperty('--vhi-band', rgba(accent, 0.09));
      var style = document.createElement('style');
      style.textContent = CSS;
      wrap.appendChild(style);

      wrap.appendChild(el('p', 'vhi-kicker', 'Media industries'));
      wrap.appendChild(el('h3', 'vhi-title', 'Which kind of integration?'));
      wrap.appendChild(el('p', 'vhi-frame',
        'Films are made, then sold on, then shown to audiences.'));

      /* ---- stage: the chain, drawn top to bottom ---- */
      var stage = el('div', 'vhi-stage');
      var deal = el('p', 'vhi-deal');
      stage.appendChild(deal);
      var rowEls = {}, blockEls = {};
      CHAIN.forEach(function (row) {
        var r = el('div', 'vhi-row');
        var lab = el('p', 'vhi-rowlab');
        lab.appendChild(el('span', 'vhi-num', row.n));
        lab.appendChild(document.createTextNode(row.label + ' '));
        lab.appendChild(el('span', 'vhi-gloss', '· ' + row.gloss));
        r.appendChild(lab);
        var blocks = el('div', 'vhi-blocks');
        /* two named slots per stage, then the other firms as unlabelled blocks */
        var slots = [el('span', 'vhi-firm'), el('span', 'vhi-firm')];
        slots.forEach(function (s) { s.hidden = true; blocks.appendChild(s); });
        for (var o = 0; o < 2; o++) {
          var other = el('div', 'vhi-other');
          other.setAttribute('aria-hidden', 'true');
          blocks.appendChild(other);
        }
        blockEls[row.id] = slots;
        r.appendChild(blocks);
        rowEls[row.id] = r;
        stage.appendChild(r);
      });
      wrap.appendChild(stage);

      /* ---- controls ---- */
      var steps = el('div', 'vhi-steps');

      var step1 = el('div', 'vhi-step');
      var lab1 = el('p', 'vhi-steplab');
      lab1.hidden = true;
      lab1.appendChild(el('span', 'vhi-num', '1'));
      var lab1Text = document.createTextNode('Vertical or horizontal?');
      lab1.appendChild(lab1Text);
      step1.appendChild(lab1);
      var kindWrap = el('div', 'vhi-kinds');
      var kindBtns = {};
      ['vertical', 'horizontal'].forEach(function (k) {
        var b = el('button', 'vhi-btn', k.charAt(0).toUpperCase() + k.slice(1));
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', function () { pickKind(k); });
        kindBtns[k] = b;
        kindWrap.appendChild(b);
      });
      step1.appendChild(kindWrap);
      steps.appendChild(step1);

      var step2 = el('div', 'vhi-step');
      var lab2 = el('p', 'vhi-steplab');
      lab2.appendChild(el('span', 'vhi-num', '2'));
      var lab2Text = document.createTextNode('And what does it buy the studio?');
      lab2.appendChild(lab2Text);
      step2.appendChild(lab2);
      var optWrap = el('div', 'vhi-opts');
      var optBtns = [];
      for (var i = 0; i < 3; i++) {
        (function () {
          var b = el('button', 'vhi-btn', '');
          b.type = 'button';
          b.setAttribute('aria-pressed', 'false');
          b.addEventListener('click', function () { pickPower(b.dataset.power); });
          optBtns.push(b);
          optWrap.appendChild(b);
        })();
      }
      step2.appendChild(optWrap);
      step2.hidden = true;
      steps.appendChild(step2);
      wrap.appendChild(steps);

      var actions = el('div', 'vhi-actions');
      var go = el('button', 'vhi-go', 'Check it');
      go.type = 'button';
      go.disabled = true;
      go.addEventListener('click', commit);
      actions.appendChild(go);
      wrap.appendChild(actions);

      var cap = el('p', 'vhi-cap');
      wrap.appendChild(cap);

      var onward = el('div', 'vhi-actions vhi-onward');
      var next = el('button', 'vhi-next', 'Next takeover');
      next.type = 'button';
      next.addEventListener('click', function () { st.idx++; newRound(); });
      onward.appendChild(next);
      onward.hidden = true;
      wrap.appendChild(onward);

      var sr = el('p', 'vhi-sr');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      root.appendChild(wrap);

      /* ---- state ---- */
      var order = ROUNDS.map(function (_, i2) { return i2; });
      for (var s = order.length - 1; s > 0; s--) {
        var j = Math.floor(Math.random() * (s + 1));
        var t = order[s]; order[s] = order[j]; order[j] = t;
      }
      var st = { idx: 0, kind: null, power: null, committed: false, askPower: false,
                 streak: 0, attempted: 0, mastered: false, correct: null };

      function round() { return ROUNDS[order[st.idx % order.length]]; }

      function publish() {
        root.dataset.svState = JSON.stringify({
          streak: st.streak, mastered: st.mastered, attempted: st.attempted,
          kind: st.kind, power: st.askPower ? st.power : null, correct: st.correct
        });
      }

      function ready() { return st.askPower ? !!(st.kind && st.power) : !!st.kind; }

      function pickKind(k) {
        if (st.committed) return;
        st.kind = k;
        for (var key in kindBtns) {
          var on = key === k;
          kindBtns[key].classList.toggle('is-on', on);
          kindBtns[key].setAttribute('aria-pressed', on ? 'true' : 'false');
        }
        go.disabled = !ready();
        publish();
      }

      function pickPower(p) {
        if (st.committed || !p || !st.askPower) return;
        st.power = p;
        optBtns.forEach(function (b) {
          var on = b.dataset.power === p;
          b.classList.toggle('is-on', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        go.disabled = !ready();
        publish();
      }

      function newRound() {
        var r = round();
        st.kind = null; st.power = null; st.committed = false; st.correct = null;
        /* the second question arrives once the classification has footing */
        st.askPower = st.attempted >= 1;

        deal.textContent = r.deal;
        CHAIN.forEach(function (row) {
          rowEls[row.id].classList.remove('is-live');
          blockEls[row.id].forEach(function (slot) {
            slot.hidden = true;
            slot.classList.remove('is-buyer', 'is-target');
          });
        });
        function place(actor, cls) {
          var slots = blockEls[actor.stage];
          var slot = slots[0].hidden ? slots[0] : slots[1];
          slot.textContent = actor.role;
          slot.classList.add(cls);
          slot.hidden = false;
          rowEls[actor.stage].classList.add('is-live');
        }
        place(r.buyer, 'is-buyer');
        place(r.target, 'is-target');

        var keys = ['up', 'down', 'share'];
        for (var q = keys.length - 1; q > 0; q--) {
          var m = Math.floor(Math.random() * (q + 1));
          var tmp = keys[q]; keys[q] = keys[m]; keys[m] = tmp;
        }
        optBtns.forEach(function (b, k2) {
          b.dataset.power = keys[k2];
          b.textContent = r.opts[keys[k2]];
          b.classList.remove('is-on');
          b.setAttribute('aria-pressed', 'false');
        });
        for (var key2 in kindBtns) {
          kindBtns[key2].classList.remove('is-on');
          kindBtns[key2].setAttribute('aria-pressed', 'false');
        }
        lab2Text.nodeValue = 'And what does it buy ' + r.buyer.role + '?';
        lab1.hidden = !st.askPower;
        step2.hidden = !st.askPower;

        steps.hidden = false;
        actions.hidden = false;
        go.disabled = true;
        onward.hidden = true;
        cap.innerHTML = '';
        if (st.mastered) {
          cap.innerHTML = '<span class="vhi-mast">You have it.</span> ' +
            '<span class="vhi-run">Keep going for as long as you like.</span>';
        } else if (st.streak > 0) {
          cap.innerHTML = '<span class="vhi-run">' + st.streak + ' right in a row ' + EM + ' ' +
            (st.streak === 2 ? 'one more and you have it.' : 'two more and you have it.') + '</span>';
        }
        publish();
      }

      function commit() {
        if (st.committed || !ready()) return;
        var r = round();
        var kindOK = st.kind === r.kind;
        var powerOK = !st.askPower || st.power === r.power;
        st.committed = true;
        st.attempted++;
        st.correct = kindOK && powerOK;
        if (st.correct) {
          st.streak++;
          if (st.streak >= 3) st.mastered = true;
        } else {
          st.streak = 0;
        }

        var right = r.opts[r.power];
        var msg;
        if (st.correct && st.askPower) {
          msg = '<strong>Right ' + EM + ' ' + r.kind + ' integration, and ' + LQ + right + RQ + '.</strong> ';
        } else if (st.correct) {
          msg = '<strong>Right ' + EM + ' ' + r.kind + ' integration.</strong> ';
        } else if (!kindOK && !st.askPower) {
          msg = '<strong>Not quite ' + EM + ' you said ' + st.kind + ' integration. This is <span>' +
                r.kind + '</span> integration.</strong> ';
        } else if (!kindOK && powerOK) {
          msg = '<strong>Not quite ' + EM + ' you said ' + st.kind + ' integration.</strong> What it buys was right ' +
                EM + ' ' + LQ + right + RQ + ' ' + EM + ' but that comes from <strong>' + r.kind +
                ' integration</strong>. ';
        } else if (!kindOK) {
          msg = '<strong>Not quite ' + EM + ' you said ' + st.kind + ' integration and ' + LQ +
                r.opts[st.power] + RQ + '.</strong> This is <strong>' + r.kind +
                ' integration</strong>, and it buys ' + LQ + right + RQ + '. ';
        } else {
          msg = '<strong>Not quite ' + EM + ' ' + r.kind + ' integration was right, but you picked ' + LQ +
                r.opts[st.power] + RQ + '.</strong> It buys ' + LQ + right + RQ + '. ';
        }
        msg += r.why;
        if (!kindOK) {
          msg += ' ' + (st.kind === 'horizontal'
            ? 'Horizontal would mean both firms did the same job, but one works at ' +
              stageName(r.buyer.stage) + ' and the other at ' + stageName(r.target.stage) + '.'
            : 'Vertical would mean the two sat at different stages, but both work at ' +
              stageName(r.buyer.stage) + '.');
        } else if (!powerOK) {
          msg += ' ' + POWER_MISS[st.power];
        }
        if (st.mastered && st.correct) {
          msg += ' <span class="vhi-mast">Three in a row ' + EM + ' you have it: a different stage of the chain is vertical, ' +
                 'the same stage is horizontal.</span>';
        } else if (st.correct) {
          msg += ' <span class="vhi-run">' + st.streak + ' right in a row.</span>';
        }
        cap.innerHTML = msg;
        sr.textContent = cap.textContent;

        steps.hidden = true;
        actions.hidden = true;
        onward.hidden = false;
        next.textContent = st.mastered ? 'Another anyway' : 'Next takeover';
        publish();
      }

      newRound();
    }
  };
})();
