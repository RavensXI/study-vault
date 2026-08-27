/* ============================================================================
   Widget: witches-prophecies-ambiguous-loopholes
   Lesson: English Literature — Macbeth, "The Witches Return & Tyranny"

   The idea it makes concrete: the witches' statements are equivocations —
   every word is true, and every word is shaped so that Macbeth will hear the
   comfortable half. The student commits to what a prophecy actually
   guarantees (or where its wording leaves a way out, or whether an
   apparition's image warns or reassures) BEFORE any verdict appears, then
   sees the words' literal guarantee set beside Macbeth's inference.

   Misconceptions it must let the student commit and then refute:
     - "the witches lied"                      -> round 'palter'
     - "the witches made it happen / control him" -> rounds 'hereafter', 'bold'
     - "each prophecy is a plain statement with one meaning" -> 'born', 'birnam'
   ========================================================================== */
(function () {
  'use strict';

  var ID = 'witches-prophecies-ambiguous-loopholes';
  var NEEDED = 3;                 /* correct in a row to master (BUILD_GUIDE 0c) */
  var GLOSS = 'Equivocation — true to the letter, shaped to be misheard.';

  /* --------------------------------------------------------------------
     The bank. Nine rounds, three question shapes, so neither the ask nor
     the answer is predictable from the round before.
       shape 'guarantee' : what do these words actually promise?
       shape 'loophole'  : where does this wording leave a way out?
       shape 'image'     : do the words and the image warn, or reassure?
     Every quotation is short and functional; the play is public domain.
     -------------------------------------------------------------------- */
  var ROUNDS = [
    {
      id: 'hereafter',
      where: 'Act 1, Scene 3 — the witches greet Macbeth, then vanish.',
      quote: '“shalt be king hereafter”',
      ask: 'What do these words guarantee?',
      opts: [
        {
          t: 'He will be king — no method, no date, no length of reign.',
          ok: true,
          fb: 'you said the words promise only the crown. No method, no date, no reign length. Banquo hears the same voices and waits; Macbeth writes to his wife at once. The gap is his, not theirs.'
        },
        {
          t: 'That he must kill Duncan to take the throne.',
          ok: false,
          fb: 'you said the words tell him to kill Duncan. Duncan is never named. “Hereafter” stays open: succession, election, an old king dying in bed. Macbeth supplies the dagger; the words supply the crown.'
        },
        {
          t: 'That the witches have decided it and will make it happen.',
          ok: false,
          fb: 'you said the witches make it happen. They state; they never instruct, and they do not come near him again until he goes hunting for them. Banquo hears the identical words and acts on none of them.'
        }
      ],
      sa: 'The words guarantee',
      ta: 'He wears the crown at some point.',
      sb: 'Macbeth hears',
      tb: 'The throne is mine to take, now, by any means.'
    },
    {
      id: 'getkings',
      where: 'Act 1, Scene 3 — the witches turn from Macbeth to Banquo.',
      quote: '“Thou shalt get kings, though thou be none”',
      ask: 'What do these words guarantee about Banquo?',
      opts: [
        {
          t: 'His descendants will be kings; he never will.',
          ok: true,
          fb: 'you said the kings come from Banquo without Banquo ever being one. “Get” means father. Every word holds — Banquo dies uncrowned, Fleance escapes, and Act 4 shows Macbeth eight kings in a line.'
        },
        {
          t: 'Banquo will be crowned once Macbeth is gone.',
          ok: false,
          fb: 'you said Banquo takes the crown. “Though thou be none” rules that out in the same breath, like “Lesser than Macbeth, and greater”. Banquo is given the dynasty, never the throne.'
        },
        {
          t: 'Macbeth can end the line by killing Banquo.',
          ok: false,
          fb: 'you said killing Banquo ends the line. The promise is about descendants, so the death that mattered was Fleance’s — and Fleance escapes. Macbeth spends a murder on the wrong man.'
        }
      ],
      sa: 'The words guarantee',
      ta: 'Banquo fathers kings and wears no crown.',
      sb: 'Macbeth hears',
      tb: 'A barren sceptre — so the line can be cut.'
    },
    {
      id: 'born',
      where: 'Act 4, Scene 1 — a bloody child speaks the second prophecy.',
      quote: '“none of woman born / Shall harm Macbeth”',
      ask: 'Where does this wording leave a way out?',
      opts: [
        {
          t: 'Anyone not delivered in the ordinary way is not covered.',
          ok: true,
          fb: 'you said an unusual delivery slips the net. Macduff was “from his mother’s womb / Untimely ripp’d” — cut out, not born. Every word held, and the child saying it is bloody: the birth itself.'
        },
        {
          t: 'Only men are ruled out — a woman could still harm him.',
          ok: false,
          fb: 'you said it rules out men only. “None” rules out everyone; “of woman born” describes the delivery, not the killer. The give is in how Macduff arrived — cut from his mother, never born.'
        },
        {
          t: 'There is no way out — the words are plain and they held.',
          ok: false,
          fb: 'you said the words are plain. They are true, which is not the same. “Born” carries the exception on its own: Macduff was cut free, never born. Macbeth never tests that one word.'
        }
      ],
      sa: 'The words guarantee',
      ta: 'No one born in the ordinary way can harm him.',
      sb: 'Macbeth hears',
      tb: 'No man alive can touch me.'
    },
    {
      id: 'birnam',
      where: 'Act 5, Scene 3 — Macbeth repeats the third prophecy to himself.',
      quote: '“Till Birnam Wood remove to Dunsinane”',
      ask: 'Where does this wording leave a way out?',
      opts: [
        {
          t: 'A wood can be carried — the trees need not walk.',
          ok: true,
          fb: 'you said the wood can be carried. Malcolm orders every soldier to “hew him down a bough” and march behind it, so the wood does come. The words hold; only his picture of how breaks.'
        },
        {
          t: 'Dunsinane could be renamed, so nothing ever arrives.',
          ok: false,
          fb: 'you said the place name is the gap. The give is in “remove” — removing a wood takes hands, not roots. Malcolm’s soldiers cut boughs for cover and the wood arrives on their shoulders.'
        },
        {
          t: 'There is no way out — forests do not move, so he is safe.',
          ok: false,
          fb: 'you said forests do not move, so he is safe — which is Macbeth’s own reading, and the trap. He tests the picture, walking trees, and never the verb. “Remove” never promised the wood would move itself.'
        }
      ],
      sa: 'The words guarantee',
      ta: 'The wood reaches the hill — by any means.',
      sb: 'Macbeth hears',
      tb: 'An impossibility, so I cannot be beaten.'
    },
    {
      id: 'head',
      where: 'Act 4, Scene 1 — the first apparition: an armed head, helmeted.',
      quote: '“Beware Macduff”',
      ask: 'Do the words and the image warn, or reassure?',
      shape: 'image',
      correct: 0,
      fbs: [
        'you said both warn. The one plain warning he gets is the one he half-obeys: he sends killers to Fife, but Macduff is already in England. The helmeted head is commonly read as his own.',
        'you said the words reassure. “Beware Macduff” is a warning with a name in it, and the image agrees. It is the one prophecy with no loophole, and he answers it by killing the wrong household.',
        'you said both reassure. “Beware” is not comfort, and a severed head in a helmet is not comfort either. The comfort comes from the NEXT apparition, which he lets cancel this one: “then live, Macduff”.'
      ],
      sa: 'The words',
      ta: 'Name the danger: Macduff.',
      sb: 'The image',
      tb: 'A head in a helmet — commonly read as Macbeth’s own.'
    },
    {
      id: 'child',
      where: 'Act 4, Scene 1 — the second apparition: a child covered in blood.',
      quote: '“laugh to scorn / The power of man”',
      ask: 'Do the words and the image warn, or reassure?',
      shape: 'image',
      correct: 1,
      fbs: [
        'you said both warn. The words are pure comfort — laugh at the power of man. The warning is in the image alone: a child slick with blood is Macduff’s birth, the very thing that lets him through.',
        'you said the words reassure while the image warns. He is shown his killer as a newborn, bloody from the cutting that puts him outside “of woman born”, and he takes only the comfort.',
        'you said both reassure — Macbeth’s reading exactly. The words do. A child covered in blood does not: it shows the delivery the words quietly exclude. He hears only the promise.'
      ],
      sa: 'The words',
      ta: 'Fear no man; laugh at human power.',
      sb: 'The image',
      tb: 'A newborn bloody from being cut free — Macduff.'
    },
    {
      id: 'crown',
      where: 'Act 4, Scene 1 — the third apparition: a crowned child holding a tree.',
      quote: '“Macbeth shall never vanquish’d be”',
      ask: 'Do the words and the image warn, or reassure?',
      shape: 'image',
      correct: 1,
      fbs: [
        'you said both warn. “Never vanquish’d” is the most comforting thing he hears all night — he leaves saying he will “sleep in spite of thunder”. The warning sits in the picture, not in the words.',
        'you said the words reassure while the image warns. The picture hands him both halves of his defeat: the crowned child is the heir he cannot kill, the branch is the method. He asks about Banquo instead.',
        'you said both reassure. The words do. The picture does not — a crown on a child is the succession he murdered to prevent, and the tree in its hand is Birnam Wood already on its way.'
      ],
      sa: 'The words',
      ta: 'He cannot be beaten — until a wood moves.',
      sb: 'The image',
      tb: 'A crowned child with a branch — Malcolm, and the wood.'
    },
    {
      id: 'bold',
      where: 'Act 4, Scene 1 — the second apparition’s opening line.',
      quote: '“Be bloody, bold, and resolute”',
      ask: 'What does this actually tell Macbeth to do?',
      opts: [
        {
          t: 'It urges a manner — fearless, ruthless — and names no target.',
          ok: true,
          fb: 'you said it urges a manner and names nobody. No target is given. Macbeth picks one himself before the scene ends — “seize upon Fife” — and a wife and children die on his decision, not on an order.'
        },
        {
          t: 'It orders him to destroy Macduff’s household.',
          ok: false,
          fb: 'you said it orders the killing at Fife. This apparition never names Macduff. Macbeth settles on Fife after Lennox reports that Macduff has fled to England — he acts on news, then blames fate.'
        },
        {
          t: 'It shows the witches steering every move he makes.',
          ok: false,
          fb: 'you said the witches steer him. They urge an attitude and answer what he asks; they name no victim and set no date. The prophecies open a door — Macbeth walks through it and bars it behind him.'
        }
      ],
      sa: 'The words say',
      ta: 'Be fearless. No person, place or act is named.',
      sb: 'Macbeth hears',
      tb: 'A licence — strike first, strike anyone.'
    },
    {
      id: 'palter',
      where: 'Act 5, Scene 8 — cornered, Macbeth names what was done to him.',
      quote: '“palter with us in a double sense”',
      ask: 'Which of these is true of the prophecies?',
      opts: [
        {
          t: 'Every word came true; only his reading of them was false.',
          ok: true,
          fb: 'you said every word came true and only the reading failed. The wood came, carried; the man came, cut not born. “Palter” means to quibble — keep the promise to the ear, break it to the hope.'
        },
        {
          t: 'The witches lied about Birnam Wood — no trees ever moved.',
          ok: false,
          fb: 'you said the wood prophecy was a lie. It was kept: Malcolm’s soldiers cut boughs and carried them, and a messenger reports the wood beginning to move. “Remove” never promised roots and walking.'
        },
        {
          t: 'The witches lied about his death — a man did kill him.',
          ok: false,
          fb: 'you said the death prophecy was a lie. Macduff was cut from his mother, so he was never “of woman born” — the wording shut him out from the start. Exact, and built to be misheard.'
        }
      ],
      sa: 'What was said',
      ta: 'Every prophecy held, to the letter.',
      sb: 'What Macbeth heard',
      tb: 'Guarantees — so he calls it a lie.'
    }
  ];

  /* The three fixed answers for the apparition rounds. Which one is right
     changes between rounds (the armed head warns twice; the other two
     comfort in words and warn in the image), so it stays a real question. */
  var IMAGE_OPTS = [
    'Both warn — words and image point the same way.',
    'The words reassure, but the image warns.',
    'Both reassure — this is good news for Macbeth.'
  ];

  var MASTERY = 'Three in a row — you have it. Every word holds and none of it is an order: equivocation hands Macbeth true words and lets him supply the false reading.';

  function css(accent) {
    return '' +
'.svw-wpal{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45;}' +
'.svw-wpal *{box-sizing:border-box;}' +
'.svw-wpal .wpal-kicker{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + ';margin:0 0 .25rem;}' +
'.svw-wpal .wpal-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.18rem;line-height:1.2;margin:0 0 .35rem;}' +
'.svw-wpal .wpal-frame{font-size:.83rem;color:#5b564e;margin:0 0 .6rem;}' +
'.svw-wpal .wpal-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.6rem .75rem;margin:0 0 .6rem;}' +
'.svw-wpal .wpal-where{font-size:.72rem;color:#8d8880;margin:0 0 .25rem;}' +
'.svw-wpal .wpal-quote{font-family:"Source Serif 4",Georgia,serif;font-size:1.02rem;line-height:1.32;margin:0;}' +
'.svw-wpal .wpal-ask{font-size:.84rem;font-weight:600;margin:0 0 .4rem;}' +
'.svw-wpal .wpal-opts{display:grid;gap:.32rem;margin:0 0 .55rem;}' +
'.svw-wpal .wpal-opt{display:block;width:100%;text-align:left;font-family:inherit;font-size:.82rem;line-height:1.34;padding:.45rem .65rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;cursor:pointer;}' +
'.svw-wpal .wpal-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}' +
'.svw-wpal .wpal-fb{margin:0 0 .55rem;}' +
'.svw-wpal .wpal-verdict{font-size:.83rem;line-height:1.45;margin:0 0 .45rem;}' +
'.svw-wpal .wpal-mark{font-weight:700;}' +
'.svw-wpal .wpal-mark.is-right{color:#4f7d63;}' +
'.svw-wpal .wpal-split{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem .7rem;}' +
'.svw-wpal .wpal-gloss{font-size:.72rem;color:#8d8880;margin:0 0 .4rem;}' +
'.svw-wpal .wpal-row{margin:0 0 .35rem;}' +
'.svw-wpal .wpal-row:last-child{margin:0;}' +
'.svw-wpal .wpal-rlab{display:block;font-size:.68rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#8d8880;margin:0 0 .08rem;}' +
'.svw-wpal .wpal-rlab.is-a{color:' + accent + ';}' +
'.svw-wpal .wpal-rtxt{font-size:.8rem;line-height:1.38;margin:0;}' +
'.svw-wpal.is-wide .wpal-row{display:grid;grid-template-columns:126px 1fr;gap:.6rem;align-items:baseline;}' +
'.svw-wpal.is-wide .wpal-rlab{margin:0;}' +
'.svw-wpal .wpal-go{font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer;}' +
'.svw-wpal .wpal-go[disabled]{background:#faf8f5;color:#a9a29a;border-color:#ddd7cd;cursor:default;}' +
'.svw-wpal .wpal-run{font-size:.78rem;color:#8d8880;margin:.45rem 0 0;}' +
'.svw-wpal .wpal-run.is-done{color:#4f7d63;}' +
'.svw-wpal button:focus-visible{outline:2px solid ' + accent + ';outline-offset:2px;}' +
'.svw-wpal .wpal-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0;}';
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  window.SVWidget = {
    meta: {
      id: ID,
      title: 'What the witches actually said',
      teaches: 'The prophecies are equivocations — every word true, every word shaped so Macbeth hears a guarantee. The loopholes are in the wording, and the false reading is his.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = '';
      try {
        accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim();
      } catch (e) { accent = ''; }
      if (!/^#|^rgb/.test(accent)) accent = ctx.accent || '#8a6a4f';

      root.textContent = '';

      var wrap = el('div', 'svw-wpal');
      var style = document.createElement('style');
      style.textContent = css(accent);
      wrap.appendChild(style);

      /* ---- zone 1: header + task frame -------------------------------- */
      wrap.appendChild(el('p', 'wpal-kicker', 'Macbeth · the prophecies'));
      var h = el('h3', 'wpal-title', 'What the witches actually said');
      wrap.appendChild(h);
      wrap.appendChild(el('p', 'wpal-frame',
        'Macbeth takes comfort from a prophecy. Decide what its words really guarantee — and what they leave open.'));

      /* ---- zone 2: the stage (one prophecy) --------------------------- */
      var stage = el('div', 'wpal-stage');
      var where = el('p', 'wpal-where', '');
      var quote = el('blockquote', 'wpal-quote', '');
      stage.appendChild(where);
      stage.appendChild(quote);
      wrap.appendChild(stage);

      /* ---- zone 3: the ask + the answers ------------------------------ */
      var ask = el('p', 'wpal-ask', '');
      wrap.appendChild(ask);

      var opts = el('div', 'wpal-opts');
      opts.setAttribute('role', 'group');
      var btns = [];
      for (var i = 0; i < 3; i++) {
        var b = el('button', 'wpal-opt', '');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        (function (idx) {
          b.addEventListener('click', function () { pick(idx); });
        })(i);
        opts.appendChild(b);
        btns.push(b);
      }
      wrap.appendChild(opts);

      /* ---- zone 4: the caption (verdict + the split) ------------------- */
      var fb = el('div', 'wpal-fb');
      fb.style.display = 'none';
      var verdict = el('p', 'wpal-verdict');
      var mark = el('span', 'wpal-mark', '');
      var vtext = document.createTextNode('');
      verdict.appendChild(mark);
      verdict.appendChild(vtext);
      fb.appendChild(verdict);

      var split = el('div', 'wpal-split');
      split.appendChild(el('p', 'wpal-gloss', GLOSS));
      var rowA = el('div', 'wpal-row');
      var labA = el('span', 'wpal-rlab is-a', '');
      var txtA = el('p', 'wpal-rtxt', '');
      rowA.appendChild(labA); rowA.appendChild(txtA);
      var rowB = el('div', 'wpal-row');
      var labB = el('span', 'wpal-rlab', '');
      var txtB = el('p', 'wpal-rtxt', '');
      rowB.appendChild(labB); rowB.appendChild(txtB);
      split.appendChild(rowA);
      split.appendChild(rowB);
      fb.appendChild(split);
      wrap.appendChild(fb);

      var go = el('button', 'wpal-go', 'Check the wording');
      go.type = 'button';
      go.disabled = true;
      wrap.appendChild(go);

      var run = el('p', 'wpal-run', '');
      run.style.display = 'none';
      wrap.appendChild(run);

      var sr = el('p', 'wpal-sr', '');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      root.appendChild(wrap);

      /* wide enough for the split to sit side by side? measured, not
         media-queried: the widget's width is the modal's, not the page's. */
      function fit() {
        var w = wrap.getBoundingClientRect().width;
        if (w >= 460) wrap.classList.add('is-wide');
        else wrap.classList.remove('is-wide');
      }
      fit();
      if (typeof ResizeObserver === 'function') {
        try { new ResizeObserver(fit).observe(wrap); } catch (e) {}
      }

      /* ---- state ------------------------------------------------------ */
      var streak = 0, attempted = 0, mastered = false;
      var queue = [], current = null, choice = -1, locked = false;

      function shuffled(n) {
        var a = [], k, t;
        for (k = 0; k < n; k++) a.push(k);
        for (k = a.length - 1; k > 0; k--) {
          var j = Math.floor(Math.random() * (k + 1));
          t = a[k]; a[k] = a[j]; a[j] = t;
        }
        return a;
      }

      function nextRound() {
        if (!queue.length) {
          queue = shuffled(ROUNDS.length);
          if (current && queue[queue.length - 1] === current.index && queue.length > 1) {
            var s = queue[queue.length - 1];
            queue[queue.length - 1] = queue[0];
            queue[0] = s;
          }
        }
        var index = queue.pop();
        var r = ROUNDS[index];

        /* answers for this round, in a fresh order */
        var texts, correctIdx, fbs;
        if (r.shape === 'image') {
          texts = IMAGE_OPTS.slice();
          fbs = r.fbs.slice();
          correctIdx = r.correct;
        } else {
          texts = []; fbs = [];
          for (var q = 0; q < r.opts.length; q++) {
            texts.push(r.opts[q].t);
            fbs.push(r.opts[q].fb);
          }
          correctIdx = 0;
          for (var p = 0; p < r.opts.length; p++) if (r.opts[p].ok) correctIdx = p;
        }
        var order = shuffled(texts.length);
        var oTexts = [], oFbs = [], oCorrect = 0;
        for (var m = 0; m < order.length; m++) {
          oTexts.push(texts[order[m]]);
          oFbs.push(fbs[order[m]]);
          if (order[m] === correctIdx) oCorrect = m;
        }

        current = { index: index, r: r, texts: oTexts, fbs: oFbs, correct: oCorrect };
        choice = -1;
        locked = false;

        where.textContent = r.where;
        quote.textContent = r.quote;
        ask.textContent = r.ask;
        for (var z = 0; z < btns.length; z++) {
          btns[z].textContent = oTexts[z];
          btns[z].setAttribute('aria-pressed', 'false');
          btns[z].disabled = false;
        }
        opts.style.display = '';
        fb.style.display = 'none';
        go.textContent = 'Check the wording';
        go.disabled = true;
        publish();
      }

      function pick(idx) {
        if (locked) return;
        choice = idx;
        for (var z = 0; z < btns.length; z++) {
          btns[z].setAttribute('aria-pressed', z === idx ? 'true' : 'false');
        }
        go.disabled = false;
        publish();
      }

      function commit() {
        if (choice < 0) return;
        locked = true;
        attempted++;
        var right = (choice === current.correct);
        if (right) streak++; else streak = 0;
        var justMastered = false;
        if (right && streak >= NEEDED && !mastered) { mastered = true; justMastered = true; }

        mark.textContent = right ? 'Right — ' : 'Not quite — ';
        mark.className = 'wpal-mark' + (right ? ' is-right' : '');
        verdict.lastChild.nodeValue = current.fbs[choice];

        labA.textContent = current.r.sa;
        txtA.textContent = current.r.ta;
        labB.textContent = current.r.sb;
        txtB.textContent = current.r.tb;

        opts.style.display = 'none';
        for (var z = 0; z < btns.length; z++) btns[z].disabled = true;
        fb.style.display = '';

        go.textContent = mastered ? 'Another anyway' : 'Next prophecy';
        go.disabled = false;

        run.style.display = '';
        if (justMastered) {
          run.textContent = MASTERY;
          run.className = 'wpal-run is-done';
        } else if (!right) {
          run.textContent = 'Back to zero — three in a row finishes it.';
          run.className = 'wpal-run';
        } else if (streak === 1) {
          run.textContent = '1 right in a row — two more and you have it.';
          run.className = 'wpal-run';
        } else if (streak === 2) {
          run.textContent = '2 right in a row — one more and you have it.';
          run.className = 'wpal-run';
        } else {
          run.textContent = streak + ' right in a row.';
          run.className = 'wpal-run is-done';
        }

        sr.textContent = (right ? 'Right. ' : 'Not quite. ') + current.fbs[choice];
        publish();
      }

      go.addEventListener('click', function () {
        if (locked) nextRound(); else commit();
        go.focus();
      });

      function publish() {
        root.dataset.svState = JSON.stringify({
          round: current ? current.r.id : null,
          selected: choice,
          committed: locked,
          correct: locked ? (choice === current.correct) : null,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      nextRound();
    }
  };
})();
