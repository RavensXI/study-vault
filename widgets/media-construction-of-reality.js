/* Selection, combination and the construction of reality.
   Self-contained. No network, no storage, no eval, no timers.

   One neutral fictional event - a protest outside a town library that is
   closing - and one pool of raw material, every item of it true. Each round
   shows two bulletins built from that pool and asks the single question the
   misconception cannot survive: what makes their versions differ? "One of
   them has the facts wrong" is on the board every round, and every round it
   is false, because both bulletins are accurate.

   No brand names, real or invented: outlets are "Bulletin A" and
   "Bulletin B", people are roles. Nothing has to be memorised - the pool
   items are on screen whenever they are needed.

   The answer is derived from the round data by categorise(), never
   hand-authored, so the drawing and the marking cannot drift apart. */
(function () {
  'use strict';

  var EM = '—', LQ = '“', RQ = '”';

  /* The afternoon's raw material. Every item happened. */
  var POOL = {
    p1: 'the crowd of about 200 at the doors',
    p2: 'a pensioner who reads there every day',
    p3: 'the council says the roof is unsafe',
    p4: 'two protesters shouting at a steward',
    p5: 'children in the story corner',
    p6: 'loans down a third in five years'
  };
  var POOL_ORDER = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6'];

  var OPTS = {
    selection: {
      label: 'Different material ' + EM + ' each used something the other left out.',
      pick: 'each used different material',
      is: 'the two bulletins hold different material'
    },
    order: {
      label: 'The same material, in a different order.',
      pick: 'the same material in a different order',
      is: 'the same material sits in a different order'
    },
    wording: {
      label: 'The same material, in different words or shots.',
      pick: 'the same material in different words or shots',
      is: 'the same material is described in different words or shots'
    },
    facts: {
      label: 'Nothing was chosen ' + EM + ' one of them has the facts wrong.',
      pick: 'one of them has the facts wrong',
      is: null
    }
  };
  var OPT_KEYS = ['selection', 'order', 'wording', 'facts'];

  /* What separates the answer the student picked from the one that is right. */
  var APART = {
    'order>selection': 'The order is not what separates them ' + EM + ' the two bulletins do not hold the same items.',
    'wording>selection': 'The wording matches wherever the items match. It is the items themselves that differ.',
    'selection>order': 'Both bulletins hold the same items ' + EM + ' nothing was added or cut. Only their positions moved.',
    'wording>order': 'The words are identical in both. It is where they sit that changed.',
    'selection>wording': 'Both bulletins hold the same items, in the same order. Look again at how one of them is described.',
    'order>wording': 'The order matches in both. What differs is the description attached to one item.'
  };

  var ROUNDS = [
    {
      a: [{ id: 'p1' }, { id: 'p2' }, { id: 'p5' }],
      b: [{ id: 'p1' }, { id: 'p3' }, { id: 'p6' }],
      why: 'Both opened on the same crowd, and every item is true. A then stayed with the readers, B with the case for closing. Neither showed the two shouting, so no audience saw it.'
    },
    {
      a: [{ id: 'p1' }, { id: 'p3' }, { id: 'p2' }],
      b: [{ id: 'p3' }, { id: 'p1' }, { id: 'p2' }],
      why: 'Same three items, same words, different order. Open on the crowd and the council is answering a protest; open on the unsafe roof and the crowd is objecting to a safety decision.'
    },
    {
      a: [{ id: 'p1', w: 'filmed tight from the front' }, { id: 'p2' }, { id: 'p3' }],
      b: [{ id: 'p1', w: 'filmed wide from the rooftop' }, { id: 'p2' }, { id: 'p3' }],
      why: 'One crowd, one number, two camera positions. From the front the 200 fill the frame; from the rooftop they sit in a half-empty square. Neither shot is faked.'
    },
    {
      a: [{ id: 'p5' }, { id: 'p2' }],
      b: [{ id: 'p6' }, { id: 'p3' }],
      why: 'Two halves of one afternoon: A took the readers, B took the roof and the numbers. Neither showed the 200 at the doors, so no audience saw a protest.'
    },
    {
      a: [{ id: 'p1' }, { id: 'p3' }, { id: 'p6', w: 'read as ' + LQ + 'a third fewer loans' + RQ }],
      b: [{ id: 'p1' }, { id: 'p3' }, { id: 'p6', w: 'read as ' + LQ + 'two thirds of the loans remain' + RQ }],
      why: 'One figure, two true readings: a third fewer loans and two thirds remaining are the same number from opposite ends. The words did the work, not the material.'
    },
    {
      a: [{ id: 'p4' }, { id: 'p1' }, { id: 'p2' }],
      b: [{ id: 'p1' }, { id: 'p2' }, { id: 'p4' }],
      why: 'Same three items, same words. Lead on the shouting and the afternoon is a row; put it last and it is a footnote to 200 quiet people. Position tells the audience what counts.'
    },
    {
      a: [{ id: 'p1' }, { id: 'p4' }],
      b: [{ id: 'p1' }, { id: 'p2' }],
      why: 'Both opened on the same crowd, and both are true. A followed it with the two shouting, B with the pensioner who reads there. One second item, a disturbance or a loss.'
    }
  ];

  /* Derive the answer from the data: different items, or the same items in a
     different order, or the same items in the same order described
     differently. Exactly one must apply, or the round is not used. */
  function categorise(r) {
    var idsA = r.a.map(function (x) { return x.id; });
    var idsB = r.b.map(function (x) { return x.id; });
    if (idsA.slice().sort().join(',') !== idsB.slice().sort().join(',')) return 'selection';
    if (idsA.join(',') !== idsB.join(',')) return 'order';
    for (var i = 0; i < r.a.length; i++) {
      if ((r.a[i].w || '') !== (r.b[i].w || '')) return 'wording';
    }
    return null;
  }

  var LIVE = ROUNDS.filter(function (r) {
    r.answer = categorise(r);
    r.unused = POOL_ORDER.filter(function (id) {
      var used = false;
      r.a.concat(r.b).forEach(function (x) { if (x.id === id) used = true; });
      return !used;
    });
    return !!r.answer;
  });

  var CSS = [
    '.svw-mcr{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45;-webkit-text-size-adjust:100%}',
    '.svw-mcr *{box-sizing:border-box}',
    '.svw-mcr [hidden]{display:none !important}',
    '.svw-mcr p{margin:0}',
    '.svw-mcr .mcr-kicker{font-size:.66rem;line-height:1.2;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--mcr-a)}',
    '.svw-mcr .mcr-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;margin:.1rem 0 .18rem;line-height:1.2}',
    '.svw-mcr .mcr-frame{font-size:.82rem;line-height:1.4;color:#5b564e}',
    '.svw-mcr .mcr-stage{margin-top:.5rem;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem .6rem}',
    '.svw-mcr .mcr-cut{border:0;border-top:1px solid #e8e2d9;margin:.38rem 0}',
    '.svw-mcr .mcr-who{font-size:.68rem;line-height:1.35;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#8d8880;margin-bottom:.15rem}',
    '.svw-mcr .mcr-ord{font-weight:500;color:#a49e95}',
    '.svw-mcr .mcr-item{display:flex;align-items:flex-start;gap:.38rem;padding:.07rem 0}',
    '.svw-mcr .mcr-n{flex:0 0 auto;min-width:1.05rem;height:1.05rem;line-height:1.05rem;text-align:center;border-radius:50%;background:var(--mcr-tint);color:var(--mcr-a);font-size:.66rem;font-weight:700;font-variant-numeric:tabular-nums;margin-top:.1rem}',
    '.svw-mcr .mcr-txt{font-size:.78rem;line-height:1.35}',
    '.svw-mcr .mcr-var{color:#5b564e}',
    '.svw-mcr .mcr-ask{font-size:.74rem;line-height:1.35;font-weight:600;color:#5b564e;margin:.55rem 0 .22rem}',
    '.svw-mcr .mcr-opts{display:flex;flex-direction:column;gap:.24rem}',
    '.svw-mcr .mcr-btn{display:block;width:100%;font:inherit;font-size:.8rem;line-height:1.3;font-weight:600;text-align:left;padding:.34rem .65rem;border-radius:9px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer}',
    '.svw-mcr .mcr-btn.is-on{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-mcr .mcr-actions{display:flex;align-items:center;gap:.5rem;margin-top:.5rem}',
    '.svw-mcr .mcr-go{font:inherit;font-size:.82rem;line-height:1.3;font-weight:600;padding:.45rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
    '.svw-mcr .mcr-go[disabled]{background:#faf8f5;border-color:#ddd7cd;color:#8d8880;cursor:default}',
    '.svw-mcr .mcr-next{font:inherit;font-size:.82rem;line-height:1.3;font-weight:600;padding:.45rem .95rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer}',
    '.svw-mcr .mcr-left{margin-top:.45rem;font-size:.72rem;line-height:1.4;color:#8d8880}',
    '.svw-mcr .mcr-leftlab{font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#8d8880}',
    '.svw-mcr .mcr-cap{font-size:.84rem;line-height:1.45;margin-top:.4rem;min-height:1.45em}',
    '.svw-mcr .mcr-run{color:#8d8880}',
    '.svw-mcr .mcr-mast{color:#4f7d63;font-weight:600}',
    '.svw-mcr .mcr-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
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

  function shuffle(list) {
    for (var i = list.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = list[i]; list[i] = list[j]; list[j] = t;
    }
    return list;
  }

  window.SVWidget = {
    meta: {
      id: 'media-construction-of-reality',
      title: 'Same afternoon, two bulletins',
      teaches: 'Two accurate bulletins can leave audiences with different versions of one event, because each is built by selection, order and wording rather than simply shown.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';

      var wrap = el('div', 'svw-mcr');
      wrap.style.setProperty('--mcr-a', accent);
      wrap.style.setProperty('--mcr-tint', rgba(accent, 0.14));
      var style = document.createElement('style');
      style.textContent = CSS;
      wrap.appendChild(style);

      wrap.appendChild(el('p', 'mcr-kicker', 'Media language'));
      wrap.appendChild(el('h3', 'mcr-title', 'Same afternoon, two bulletins'));
      wrap.appendChild(el('p', 'mcr-frame',
        'A town library is closing. Two bulletins cover the protest outside it. ' +
        'Say what makes them differ.'));

      /* ---- stage: the two bulletins, item by item, in the order broadcast ---- */
      var stage = el('div', 'mcr-stage');
      var slots = { a: [], b: [] };
      ['a', 'b'].forEach(function (side, k) {
        if (k === 1) stage.appendChild(el('hr', 'mcr-cut'));
        var who = el('p', 'mcr-who', 'Bulletin ' + side.toUpperCase());
        who.appendChild(el('span', 'mcr-ord', ' · running order'));
        stage.appendChild(who);
        for (var i = 0; i < 3; i++) {
          var row = el('div', 'mcr-item');
          var n = el('span', 'mcr-n', String(i + 1));
          var txt = el('p', 'mcr-txt');
          var stem = document.createTextNode('');
          var vr = el('span', 'mcr-var');
          txt.appendChild(stem);
          txt.appendChild(vr);
          row.appendChild(n);
          row.appendChild(txt);
          row.hidden = true;
          slots[side].push({ row: row, stem: stem, vr: vr });
          stage.appendChild(row);
        }
      });
      wrap.appendChild(stage);

      /* ---- controls ---- */
      var ask = el('p', 'mcr-ask', 'What makes the two versions differ?');
      wrap.appendChild(ask);
      var optWrap = el('div', 'mcr-opts');
      var optBtns = [];
      for (var q = 0; q < OPT_KEYS.length; q++) {
        (function () {
          var b = el('button', 'mcr-btn', '');
          b.type = 'button';
          b.setAttribute('aria-pressed', 'false');
          b.addEventListener('click', function () { pick(b.dataset.key); });
          optBtns.push(b);
          optWrap.appendChild(b);
        })();
      }
      wrap.appendChild(optWrap);

      var actions = el('div', 'mcr-actions');
      var go = el('button', 'mcr-go', 'Check it');
      go.type = 'button';
      go.disabled = true;
      go.addEventListener('click', commit);
      actions.appendChild(go);
      wrap.appendChild(actions);

      /* ---- the rest of the pool: what neither audience ever saw ---- */
      var left = el('p', 'mcr-left');
      left.appendChild(el('span', 'mcr-leftlab', 'Neither bulletin used'));
      var leftText = document.createTextNode('');
      left.appendChild(leftText);
      left.hidden = true;
      wrap.appendChild(left);

      var cap = el('p', 'mcr-cap');
      wrap.appendChild(cap);

      var onward = el('div', 'mcr-actions');
      var next = el('button', 'mcr-next', 'Next pair');
      next.type = 'button';
      next.addEventListener('click', function () { st.idx++; newRound(); });
      onward.appendChild(next);
      onward.hidden = true;
      wrap.appendChild(onward);

      var sr = el('p', 'mcr-sr');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      root.appendChild(wrap);

      /* ---- state ---- */
      var order = shuffle(LIVE.map(function (_, i) { return i; }));
      var st = { idx: 0, picked: null, committed: false, correct: null,
                 streak: 0, attempted: 0, mastered: false };

      function round() { return LIVE[order[st.idx % order.length]]; }

      function publish() {
        var r = round();
        root.dataset.svState = JSON.stringify({
          streak: st.streak, mastered: st.mastered, attempted: st.attempted,
          picked: st.picked, answer: r.answer, correct: st.correct,
          committed: st.committed, unused: r.unused.length
        });
      }

      function runLine() {
        if (st.streak === 1) return 'One right ' + EM + ' two more and you have it.';
        if (st.streak === 2) return 'Two in a row ' + EM + ' one more and you have it.';
        return st.streak + ' in a row.';
      }

      function pick(k) {
        if (st.committed || !k) return;
        st.picked = k;
        optBtns.forEach(function (b) {
          var on = b.dataset.key === k;
          b.classList.toggle('is-on', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        go.disabled = false;
        publish();
      }

      function drawSide(side, items) {
        slots[side].forEach(function (s, i) {
          var it = items[i];
          if (!it) { s.row.hidden = true; return; }
          s.stem.nodeValue = POOL[it.id];
          s.vr.textContent = it.w ? ' ' + EM + ' ' + it.w : '';
          s.row.hidden = false;
        });
      }

      function newRound() {
        var r = round();
        st.picked = null; st.committed = false; st.correct = null;

        drawSide('a', r.a);
        drawSide('b', r.b);

        shuffle(OPT_KEYS.slice()).forEach(function (k, i) {
          optBtns[i].dataset.key = k;
          optBtns[i].textContent = OPTS[k].label;
          optBtns[i].classList.remove('is-on');
          optBtns[i].setAttribute('aria-pressed', 'false');
        });

        leftText.nodeValue = ': ' +
          r.unused.map(function (id) { return POOL[id]; }).join('; ') + '.';

        ask.hidden = false;
        optWrap.hidden = false;
        actions.hidden = false;
        go.disabled = true;
        left.hidden = true;
        onward.hidden = true;

        cap.innerHTML = '';
        if (st.mastered) {
          cap.innerHTML = '<span class="mcr-mast">You have it.</span> ' +
            '<span class="mcr-run">Keep going for as long as you like.</span>';
        } else if (st.streak > 0) {
          cap.innerHTML = '<span class="mcr-run">' + runLine() + '</span>';
        }
        publish();
      }

      function commit() {
        if (st.committed || !st.picked) return;
        var r = round();
        st.committed = true;
        st.attempted++;
        st.correct = st.picked === r.answer;
        if (st.correct) {
          st.streak++;
          if (st.streak >= 3) st.mastered = true;
        } else {
          st.streak = 0;
        }

        var msg;
        if (st.correct) {
          msg = '<strong>Right ' + EM + ' ' + OPTS[r.answer].is + '.</strong> ';
        } else if (st.picked === 'facts') {
          msg = '<strong>Not quite ' + EM + ' you said one of them has the facts wrong.</strong> ' +
                'Both are accurate: every item in both happened that afternoon. ' +
                'In fact ' + OPTS[r.answer].is + '. ';
        } else {
          msg = '<strong>Not quite ' + EM + ' you said ' + OPTS[st.picked].pick + '.</strong> ' +
                'In fact ' + OPTS[r.answer].is + '. ';
        }
        msg += r.why;
        if (st.picked === 'facts') {
          msg += ' Two true accounts can still leave you with different afternoons.';
        } else if (!st.correct && APART[st.picked + '>' + r.answer]) {
          msg += ' ' + APART[st.picked + '>' + r.answer];
        }
        if (st.correct && st.streak === 3) {
          msg += ' <span class="mcr-mast">Three in a row ' + EM + ' you have it: nothing was invented, ' +
                 'so the version an audience gets is built from what is selected, left out, ' +
                 'ordered and worded.</span>';
        } else if (st.correct) {
          msg += ' <span class="mcr-run">' + runLine() + '</span>';
        }
        cap.innerHTML = msg;
        sr.textContent = cap.textContent;

        ask.hidden = true;
        optWrap.hidden = true;
        actions.hidden = true;
        left.hidden = r.unused.length === 0;
        onward.hidden = false;
        next.textContent = st.mastered ? 'Another anyway' : 'Next pair';
        publish();
      }

      newRound();
    }
  };
})();
