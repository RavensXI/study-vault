/* Vertical vs horizontal integration - media conglomerate supply chain.
   Self-contained. No network, no storage, no eval. */
(function () {
  'use strict';

  var EM = '—', RSQ = '’', LQ = '“', RQ = '”';

  /* The chain is drawn top-to-bottom, so "along the chain" really is
     vertical on screen and "same stage" really is horizontal. */
  var CHAIN = [
    { id: 'prod', n: '1', label: 'Production', gloss: 'films get made', firms: [
      { id: 'halcyon',   name: 'Halcyon Pictures', own: true },
      { id: 'northgate', name: 'Northgate Films' },
      { id: 'foxglove',  name: 'Foxglove Films' }
    ] },
    { id: 'dist', n: '2', label: 'Distribution', gloss: 'films get sold on', firms: [
      { id: 'meridian',  name: 'Meridian Sales' },
      { id: 'crosswind', name: 'Crosswind Media' }
    ] },
    { id: 'exhib', n: '3', label: 'Exhibition', gloss: 'audiences watch', firms: [
      { id: 'riverline', name: 'Riverline', own: true },
      { id: 'vantage',   name: 'Vantage Cinemas' },
      { id: 'larkfield', name: 'Larkfield Play' }
    ] }
  ];

  var STAGE_OF = {};
  var FIRM = {};
  CHAIN.forEach(function (row) {
    row.firms.forEach(function (f) { STAGE_OF[f.id] = row; FIRM[f.id] = f; });
  });

  var ROUNDS = [
    {
      buyer: 'halcyon', target: 'northgate', kind: 'horizontal', power: 'share',
      deal: 'Halcyon Pictures, Kestrel' + RSQ + 's film studio, wants to buy rival studio Northgate Films.',
      opts: {
        share: 'A bigger share of film production',
        down:  'Control of how its films reach viewers',
        up:    'A guaranteed supply of films to show'
      },
      why: 'Halcyon and Northgate both sit at stage 1, so this is <strong>horizontal integration</strong> ' + EM +
           ' buying at the same stage. The effect is a bigger share of production, and one rival fewer bidding for the same scripts, stars and audiences.'
    },
    {
      buyer: 'halcyon', target: 'meridian', kind: 'vertical', power: 'down',
      deal: 'Halcyon Pictures wants to buy Meridian Sales, which sells finished films to cinemas.',
      opts: {
        down:  'Control of how its films reach cinemas',
        share: 'A bigger share of film production',
        up:    'A guaranteed supply of films to show'
      },
      why: 'Halcyon makes films at stage 1; Meridian sells them on at stage 2. Buying along the chain is <strong>vertical integration</strong>, ' +
           'and it gives Kestrel control of how its own films reach cinemas instead of paying a rival firm to carry them.'
    },
    {
      buyer: 'riverline', target: 'foxglove', kind: 'vertical', power: 'up',
      deal: 'Riverline, Kestrel' + RSQ + 's streaming service, wants to buy Foxglove Films, a small studio.',
      opts: {
        up:    'A guaranteed supply of films to stream',
        down:  'Control of the screens its films play on',
        share: 'A bigger share of the streaming market'
      },
      why: 'Riverline shows films at stage 3; Foxglove makes them at stage 1. Buying back up the chain is <strong>vertical integration</strong>, ' +
           'and it guarantees Riverline films of its own that no rival service can outbid it for.'
    },
    {
      buyer: 'halcyon', target: 'vantage', kind: 'vertical', power: 'down',
      deal: 'Halcyon Pictures wants to buy Vantage Cinemas, a chain far bigger than the studio.',
      opts: {
        down:  'Guaranteed screens for its own films',
        share: 'A bigger share of film production',
        up:    'A guaranteed supply of films to show'
      },
      why: 'Vantage is much the bigger firm, but size is not the test: Vantage sits at stage 3 and Halcyon at stage 1. ' +
           'Different stages make this <strong>vertical integration</strong>, and it guarantees Kestrel' + RSQ + 's films the screens they need.'
    },
    {
      buyer: 'halcyon', target: 'foxglove', kind: 'horizontal', power: 'share',
      deal: 'Halcyon Pictures wants to buy Foxglove Films, a two-person studio with three films.',
      opts: {
        share: 'A bigger share of film production',
        down:  'Control of how its films reach viewers',
        up:    'A guaranteed supply of films to show'
      },
      why: 'Foxglove is tiny, but size is not the test: both firms make films at stage 1. The same stage makes this <strong>horizontal integration</strong>, ' +
           'and it adds Foxglove' + RSQ + 's output and back catalogue to Kestrel' + RSQ + 's share of production.'
    },
    {
      buyer: 'riverline', target: 'larkfield', kind: 'horizontal', power: 'share',
      deal: 'Riverline wants to buy Larkfield Play, a rival service with two million members.',
      opts: {
        share: 'A bigger share of the streaming market',
        up:    'A guaranteed supply of new films to stream',
        down:  'Control of the screens its films play on'
      },
      why: 'Riverline and Larkfield both reach audiences at stage 3, so this is <strong>horizontal integration</strong>. ' +
           'Two million members transfer to Kestrel, growing its share of the streaming market and removing a service viewers might have chosen instead.'
    }
  ];

  var POWER_MISS = {
    down:  'Control of the route to viewers comes from owning the stage that carries a film to them.',
    up:    'A guaranteed supply comes from owning the stage that makes the films, when you are the one showing them.',
    share: 'A bigger share of one stage comes from buying a firm doing the same job as you.'
  };

  var CSS = [
    '.svw-vhi{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45;-webkit-text-size-adjust:100%}',
    '.svw-vhi *{box-sizing:border-box}',
    '.svw-vhi [hidden]{display:none !important}',
    '.svw-vhi p{margin:0}',
    '.svw-vhi .vhi-kicker{font-size:.66rem;line-height:1.2;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--vhi-a)}',
    '.svw-vhi .vhi-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;margin:.1rem 0 .22rem;line-height:1.2}',
    '.svw-vhi .vhi-frame{font-size:.84rem;color:#5b564e}',
    '.svw-vhi .vhi-stage{margin-top:.5rem;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem .6rem}',
    '.svw-vhi .vhi-deal{font-size:.84rem;font-weight:600;margin-bottom:.4rem}',
    '.svw-vhi .vhi-row{display:flex;flex-wrap:wrap;align-items:center;gap:.16rem .5rem;border-radius:9px;padding:.18rem .3rem;margin:0 -.3rem}',
    '.svw-vhi .vhi-row + .vhi-row{margin-top:.2rem}',
    '.svw-vhi .vhi-row.is-live{background:var(--vhi-band)}',
    '.svw-vhi .vhi-rowlab{flex:0 0 auto;font-size:.68rem;line-height:1.35;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#8d8880}',
    '.svw-vhi .vhi-rowlab .vhi-gloss{font-weight:500;letter-spacing:0;text-transform:none}',
    '.svw-vhi .vhi-chips{flex:1 1 19rem;display:flex;flex-wrap:wrap;gap:.26rem}',
    '.svw-vhi .vhi-chip{font-size:.72rem;line-height:1.35;padding:.18rem .42rem;border-radius:8px;border:1px solid #e0d9cd;background:#fff;color:#5b564e;white-space:nowrap}',
    '.svw-vhi .vhi-chip.is-own{background:var(--vhi-tint);border-color:var(--vhi-edge);color:#2d2a26}',
    '.svw-vhi .vhi-chip.is-buyer{background:#2d2a26;border-color:#2d2a26;color:#fff;font-weight:600}',
    '.svw-vhi .vhi-chip.is-target{border:1px dashed var(--vhi-a);background:var(--vhi-tint);color:#2d2a26;font-weight:600}',
    '.svw-vhi .vhi-steps{margin-top:.5rem}',
    '.svw-vhi .vhi-step + .vhi-step{margin-top:.35rem}',
    '.svw-vhi .vhi-kindline{display:flex;align-items:center;flex-wrap:wrap;gap:.35rem}',
    '.svw-vhi .vhi-steplab{font-size:.74rem;line-height:1.35;font-weight:600;color:#5b564e}',
    '.svw-vhi .vhi-num{display:inline-block;min-width:1.05rem;height:1.05rem;line-height:1.05rem;text-align:center;border-radius:50%;background:var(--vhi-tint);color:var(--vhi-a);font-size:.66rem;font-weight:700;margin-right:.25rem}',
    '.svw-vhi .vhi-opts{display:flex;flex-direction:column;gap:.24rem;margin-top:.22rem}',
    '.svw-vhi .vhi-btn{font:inherit;font-size:.78rem;line-height:1.3;font-weight:600;text-align:left;padding:.3rem .6rem;border-radius:9px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer}',
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

  window.SVWidget = {
    meta: {
      id: 'vertical-vs-horizontal-integration',
      title: 'Growing a media conglomerate',
      teaches: 'Vertical integration buys a firm at a different stage of the supply chain; horizontal integration buys one at the same stage, and each buys a different power.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';

      var wrap = el('div', 'svw-vhi');
      wrap.style.setProperty('--vhi-a', accent);
      wrap.style.setProperty('--vhi-tint', rgba(accent, 0.13));
      wrap.style.setProperty('--vhi-edge', rgba(accent, 0.4));
      wrap.style.setProperty('--vhi-band', rgba(accent, 0.09));
      var style = document.createElement('style');
      style.textContent = CSS;
      wrap.appendChild(style);

      wrap.appendChild(el('p', 'vhi-kicker', 'Media industries'));
      wrap.appendChild(el('h3', 'vhi-title', 'Growing a media conglomerate'));
      wrap.appendChild(el('p', 'vhi-frame',
        'Kestrel Media owns two firms in this chain. Judge each takeover it proposes.'));

      /* ---- stage: the supply chain, drawn top to bottom ---- */
      var stage = el('div', 'vhi-stage');
      var deal = el('p', 'vhi-deal');
      stage.appendChild(deal);
      var rowEls = {}, chipEls = {};
      CHAIN.forEach(function (row) {
        var r = el('div', 'vhi-row');
        var lab = el('p', 'vhi-rowlab');
        lab.appendChild(el('span', 'vhi-num', row.n));
        lab.appendChild(document.createTextNode(row.label + ' '));
        lab.appendChild(el('span', 'vhi-gloss', '· ' + row.gloss));
        r.appendChild(lab);
        var chips = el('div', 'vhi-chips');
        row.firms.forEach(function (f) {
          var c = el('span', 'vhi-chip' + (f.own ? ' is-own' : ''), f.name);
          chipEls[f.id] = c;
          chips.appendChild(c);
        });
        r.appendChild(chips);
        rowEls[row.id] = r;
        stage.appendChild(r);
      });
      wrap.appendChild(stage);

      /* ---- controls ---- */
      var steps = el('div', 'vhi-steps');

      var step1 = el('div', 'vhi-step');
      var kindLine = el('div', 'vhi-kindline');
      var lab1 = el('p', 'vhi-steplab');
      lab1.appendChild(el('span', 'vhi-num', '1'));
      lab1.appendChild(document.createTextNode('Which kind?'));
      kindLine.appendChild(lab1);
      var kindBtns = {};
      ['vertical', 'horizontal'].forEach(function (k) {
        var b = el('button', 'vhi-btn', k.charAt(0).toUpperCase() + k.slice(1));
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', function () { pickKind(k); });
        kindBtns[k] = b;
        kindLine.appendChild(b);
      });
      step1.appendChild(kindLine);
      steps.appendChild(step1);

      var step2 = el('div', 'vhi-step');
      var lab2 = el('p', 'vhi-steplab');
      lab2.appendChild(el('span', 'vhi-num', '2'));
      lab2.appendChild(document.createTextNode('What power does it buy Kestrel?'));
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
      steps.appendChild(step2);
      wrap.appendChild(steps);

      var actions = el('div', 'vhi-actions');
      var go = el('button', 'vhi-go', 'Check the takeover');
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
      var st = { idx: 0, kind: null, power: null, committed: false,
                 streak: 0, attempted: 0, mastered: false, correct: null };

      function round() { return ROUNDS[order[st.idx % order.length]]; }

      function publish() {
        root.dataset.svState = JSON.stringify({
          streak: st.streak, mastered: st.mastered, attempted: st.attempted,
          kind: st.kind, power: st.power, correct: st.correct
        });
      }

      function pickKind(k) {
        if (st.committed) return;
        st.kind = k;
        for (var key in kindBtns) {
          var on = key === k;
          kindBtns[key].classList.toggle('is-on', on);
          kindBtns[key].setAttribute('aria-pressed', on ? 'true' : 'false');
        }
        go.disabled = !(st.kind && st.power);
        publish();
      }

      function pickPower(p) {
        if (st.committed || !p) return;
        st.power = p;
        optBtns.forEach(function (b) {
          var on = b.dataset.power === p;
          b.classList.toggle('is-on', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        go.disabled = !(st.kind && st.power);
        publish();
      }

      function newRound() {
        var r = round();
        st.kind = null; st.power = null; st.committed = false; st.correct = null;
        deal.textContent = r.deal;
        for (var id in chipEls) {
          chipEls[id].classList.remove('is-buyer', 'is-target');
        }
        for (var rid in rowEls) rowEls[rid].classList.remove('is-live');
        chipEls[r.buyer].classList.add('is-buyer');
        chipEls[r.target].classList.add('is-target');
        rowEls[STAGE_OF[r.buyer].id].classList.add('is-live');
        rowEls[STAGE_OF[r.target].id].classList.add('is-live');

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
        if (st.committed || !st.kind || !st.power) return;
        var r = round();
        var kindOK = st.kind === r.kind;
        var powerOK = st.power === r.power;
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
        if (st.correct) {
          msg = '<strong>Right ' + EM + ' ' + r.kind + ' integration, and ' + LQ + right + RQ + '.</strong> ';
        } else if (!kindOK && powerOK) {
          msg = '<strong>Not quite ' + EM + ' you said ' + st.kind + ' integration.</strong> The power you picked was right ' +
                EM + ' ' + LQ + right + RQ + ' ' + EM + ' but that is bought by <strong>' + r.kind +
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
          var bs = STAGE_OF[r.buyer], ts = STAGE_OF[r.target];
          msg += ' ' + (st.kind === 'horizontal'
            ? 'Horizontal would mean both firms do the same job: ' + FIRM[r.buyer].name + ' works at ' +
              bs.label.toLowerCase() + ', ' + FIRM[r.target].name + ' at ' + ts.label.toLowerCase() + '.'
            : 'Vertical would mean the two sit at different stages, but both work at ' +
              bs.label.toLowerCase() + '.');
        } else if (!powerOK) {
          msg += ' ' + POWER_MISS[st.power];
        }
        if (st.mastered && st.correct) {
          msg += ' <span class="vhi-mast">Three in a row ' + EM + ' you have it: along the chain is vertical, ' +
                 'across one stage is horizontal.</span>';
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
