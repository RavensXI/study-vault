/* plot-vs-story — story (chronological) vs plot (what reaches the screen, in
   screen order). Original mini-narratives; no real film is used. */
(function () {
  'use strict';

  var NARR = {
    salt: [
      'Nadia learns to read a ledger',
      'Ruben burns the harbour office',
      'The insurance money is paid out',
      'Nadia finds the burnt ledger',
      'Ruben is arrested on the quay'
    ],
    shed: [
      'Dele hides the letter in a shed',
      'The family hunts for the letter',
      'His brother misses the deadline',
      'Dele owns up to his brother',
      'The brothers repaint the shed'
    ],
    kiln: [
      'Her gran fires a blue glaze',
      'The kiln is bricked up for years',
      'Mira inherits a cracked bowl',
      'Mira’s first pot comes out grey',
      'Mira finds the glaze recipe'
    ]
  };

  var OPTS = [
    { key: 'mystery',  label: 'Mystery — we work out how we got here' },
    { key: 'suspense', label: 'Suspense — we know what they do not' },
    { key: 'same',     label: 'No difference — the same events happen' }
  ];

  var ROUNDS = [
    {
      nar: 'salt', order: [4, 1, 5], q: 'first', answer: 4,
      frame: 'A film opens on a woman prising up a lighthouse floorboard. She lifts out a ledger with its edges burnt black.',
      ask: 'Which of the five story events is the audience meeting first?',
      rightTail: 'The plot starts there. The story starts years earlier, at event 1, and the film reaches it afterwards as a flashback.',
      diag: {
        1: 'That is where the story begins, but a plot need not begin where the story begins. This one opens on event 4 and reaches event 1 later, as a flashback.',
        2: 'The burnt edges point to the fire, but the camera never shows it: a story event can reach the plot as a trace only. The audience meets event 4, the discovery.',
        3: 'The payout is in the story, and nothing on screen shows it. The audience meets event 4, the discovery.',
        5: 'The arrest is the last scene, not the first. The audience meets event 4, the discovery.'
      }
    },
    {
      nar: 'shed', order: [4, 1, 2], q: 'unshown', answer: [3, 5],
      frame: 'A film cuts between a boy owning up to his brother, the same boy earlier pushing an envelope behind a paint tin in the shed, and a family pulling the house apart.',
      ask: 'Select every story event this film never puts on screen.',
      rightTail: 'The plot picks three scenes and jumps the rest. Story time skipped like that is an ellipsis.',
      wrongTail: 'The missed deadline and the repainted shed happen in the story and stay off screen. The plot selects; it does not show everything. Story time it skips is an ellipsis.'
    },
    {
      nar: 'kiln', order: [1, 4, 5], q: 'effect', answer: 'suspense',
      frame: 'Mira was born after the pottery shut; she never saw her grandmother work. This cut keeps event 1 and drops events 2 and 3.',
      ask: 'What does keeping event 1 on screen give the audience?',
      right: 'The plot hands us the blue firing that Mira never saw, so we watch her fail while already holding the answer. Knowing more than the character is dramatic irony, and it is what makes the scene tense.',
      diag: {
        mystery: 'Mystery needs the cause withheld. Here the plot shows the cause first, so nothing is hidden from us — only from Mira. We are ahead of her, not behind her.',
        same: 'Cut event 1 out and we would be as lost as Mira is. Choosing to put it on screen is the whole difference: selection is a plot choice, not a neutral one.'
      }
    },
    {
      nar: 'shed', order: [2, 1, 4], q: 'first', answer: 2,
      frame: 'A different cut of the same story opens on a family pulling out drawers and shaking books, hunting for a letter that is not in the house.',
      ask: 'Which of the five story events is the audience meeting first?',
      rightTail: 'The plot opens in the middle of the story, then flashes back to event 1 to show where the letter went.',
      diag: {
        1: 'That is where the story begins, and the film does show it — second, as a flashback. What the audience meets first is event 2, the search.',
        3: 'The missed deadline never reaches the screen at all. The audience meets event 2, the search.',
        4: 'Owning up is the last scene, not the first. The audience meets event 2, the search.',
        5: 'The repainting never reaches the screen. The audience meets event 2, the search.'
      }
    },
    {
      nar: 'salt', order: [2, 4, 5], q: 'unshown', answer: [1, 3],
      frame: 'A film cuts between a man striking a match in the harbour office, a woman lifting a burnt ledger from under a floorboard, and an arrest on the quay at dawn.',
      ask: 'Select every story event this film never puts on screen.',
      rightTail: 'One of them is the motive: the money never reaches the screen at all. Story time the plot skips is an ellipsis.',
      wrongTail: 'The reading lesson and the insurance payout happen in the story and stay off screen. The plot selects; it does not show everything. Story time it skips is an ellipsis.'
    },
    {
      nar: 'kiln', order: [4, 3, 5], q: 'effect', answer: 'mystery',
      frame: 'A second cut of the same story opens on the failed grey pot, and the grandmother’s firing is left out of the film entirely.',
      ask: 'What does this arrangement create?',
      right: 'Opening on the grey pot puts the result before its cause, and the firing that explains it never appears, so we work backwards alongside Mira instead of ahead of her.',
      diag: {
        suspense: 'Suspense needs us to hold something the character does not. This cut drops the firing, so we know less than Mira, not more. We are the ones in the dark.',
        same: 'These are the same five story events as the other cut. That one kept the firing and built suspense; this one drops it and builds mystery. The arrangement is the choice.'
      }
    }
  ];

  var ORD = ['1st', '2nd', '3rd'];

  function listEvents(a) {
    if (!a.length) return 'nothing';
    if (a.length === 1) return 'event ' + a[0];
    return 'events ' + a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
  }
  function same(a, b) {
    if (a.length !== b.length) return false;
    for (var i = 0; i < a.length; i++) { if (a[i] !== b[i]) return false; }
    return true;
  }

  window.SVWidget = {
    meta: {
      id: 'plot-vs-story',
      title: 'Story order, screen order',
      teaches: 'Story is every event in the film world in chronological order; plot is what the film selects and the order it shows it in.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;

      var roundIdx = 0, streak = 0, attempted = 0, mastered = false;
      var picked = [], choice = null, committed = false, wasRight = false;

      root.classList.add('svw-pvs');
      root.innerHTML =
        '<style>' + css(accent) + '</style>' +
        '<div class="pvs-kick">Narrative structure</div>' +
        '<h3 class="pvs-title">Story order, screen order</h3>' +
        '<p class="pvs-frame"></p>' +
        '<p class="pvs-ask"></p>' +
        '<div class="pvs-stage">' +
          '<div class="pvs-heads"><span>Story &middot; in the order it happens</span>' +
          '<span>Plot &middot; on screen</span></div>' +
          '<div class="pvs-tracks">' +
            '<div class="pvs-rows"></div>' +
            '<div class="pvs-chips"></div>' +
            '<svg class="pvs-threads" aria-hidden="true"></svg>' +
          '</div>' +
        '</div>' +
        '<div class="pvs-opts"></div>' +
        '<div class="pvs-foot"><button type="button" class="pvs-go">Check</button>' +
        '<span class="pvs-streak"></span></div>' +
        '<p class="pvs-cap"></p>' +
        '<p class="pvs-sr" aria-live="polite"></p>';

      var elRows = root.querySelector('.pvs-rows');
      var elChips = root.querySelector('.pvs-chips');
      var elTracks = root.querySelector('.pvs-tracks');
      var elSvg = root.querySelector('.pvs-threads');
      var elOpts = root.querySelector('.pvs-opts');
      var elGo = root.querySelector('.pvs-go');
      var elCap = root.querySelector('.pvs-cap');
      var elFrame = root.querySelector('.pvs-frame');
      var elAsk = root.querySelector('.pvs-ask');
      var elStreak = root.querySelector('.pvs-streak');
      var elSr = root.querySelector('.pvs-sr');

      var rows = [], chips = [], opts = [];
      var i, b, c, o;
      for (i = 0; i < 5; i++) {
        b = document.createElement('button');
        b.type = 'button';
        b.className = 'pvs-row';
        b.setAttribute('aria-pressed', 'false');
        b.innerHTML = '<span class="pvs-num">' + (i + 1) + '</span><span class="pvs-txt"></span>';
        b.addEventListener('click', onRow(i + 1));
        elRows.appendChild(b);
        rows.push(b);
      }
      for (i = 0; i < 3; i++) {
        c = document.createElement('div');
        c.className = 'pvs-chip';
        c.textContent = ORD[i];
        elChips.appendChild(c);
        chips.push(c);
      }
      for (i = 0; i < OPTS.length; i++) {
        o = document.createElement('button');
        o.type = 'button';
        o.className = 'pvs-opt';
        o.textContent = OPTS[i].label;
        o.setAttribute('aria-pressed', 'false');
        o.addEventListener('click', onOpt(OPTS[i].key));
        elOpts.appendChild(o);
        opts.push(o);
      }

      elGo.addEventListener('click', function () {
        if (committed) { roundIdx = (roundIdx + 1) % ROUNDS.length; loadRound(); }
        else { commit(); }
      });

      if (typeof ResizeObserver === 'function') {
        try {
          new ResizeObserver(function () { draw(); }).observe(elTracks);
        } catch (e) { /* threads simply do not re-fit; layout is unaffected */ }
      }

      loadRound();
      return;

      /* ---------- round lifecycle ---------- */

      function R() { return ROUNDS[roundIdx]; }

      function loadRound() {
        var r = R(), ev = NARR[r.nar], k;
        picked = []; choice = null; committed = false; wasRight = false;

        elFrame.textContent = r.frame;
        elAsk.textContent = r.ask;

        for (k = 0; k < 5; k++) {
          rows[k].querySelector('.pvs-txt').textContent = ev[k];
          rows[k].className = 'pvs-row';
          rows[k].setAttribute('aria-pressed', 'false');
          rows[k].disabled = (r.q === 'effect');
        }
        for (k = 0; k < 3; k++) {
          opts[k].className = 'pvs-opt';
          opts[k].setAttribute('aria-pressed', 'false');
          chips[k].classList.remove('is-on');
        }
        elOpts.style.display = (r.q === 'effect') ? '' : 'none';

        /* An effect question is about an arrangement you can see, so that
           round draws its threads from the start. The other two withhold
           them: the mapping is what the student commits to. */
        if (r.q === 'effect') markPlot();

        elGo.textContent = 'Check';
        elGo.disabled = (r.q !== 'unshown');
        elCap.innerHTML = '';
        setStreak();
        push();
        draw();
      }

      function markPlot() {
        var r = R(), k;
        for (k = 0; k < 3; k++) { chips[k].classList.add('is-on'); }
        for (k = 1; k <= 5; k++) {
          rows[k - 1].classList.add(r.order.indexOf(k) >= 0 ? 'is-shown' : 'is-cut');
        }
        draw();
      }

      /* ---------- controls ---------- */

      function onRow(n) {
        return function () {
          var r = R(), k, at, on;
          if (committed || r.q === 'effect') return;
          if (r.q === 'first') { picked = (picked[0] === n) ? [] : [n]; }
          else {
            at = picked.indexOf(n);
            if (at >= 0) { picked.splice(at, 1); } else { picked.push(n); }
            picked.sort();
          }
          for (k = 1; k <= 5; k++) {
            on = picked.indexOf(k) >= 0;
            rows[k - 1].classList.toggle('is-sel', on);
            rows[k - 1].setAttribute('aria-pressed', on ? 'true' : 'false');
          }
          elGo.disabled = (r.q === 'first' && !picked.length);
          push();
        };
      }

      function onOpt(key) {
        return function () {
          var k, on;
          if (committed || R().q !== 'effect') return;
          choice = key;
          for (k = 0; k < OPTS.length; k++) {
            on = OPTS[k].key === key;
            opts[k].classList.toggle('is-sel', on);
            opts[k].setAttribute('aria-pressed', on ? 'true' : 'false');
          }
          elGo.disabled = false;
          push();
        };
      }

      /* ---------- commit ---------- */

      function commit() {
        var r = R(), ev = NARR[r.nar], msg, k;
        committed = true;

        if (r.q === 'effect') {
          wasRight = (choice === r.answer);
          msg = wasRight
            ? yes() + 'you chose ' + labelOf(r.answer) + '. ' + r.right
            : no() + 'you chose ' + labelOf(choice) + '. ' + r.diag[choice];
          elOpts.style.display = 'none';
        } else if (r.q === 'first') {
          wasRight = (picked[0] === r.answer);
          msg = wasRight
            ? yes() + 'you chose event ' + r.answer + ': ' + ev[r.answer - 1] + '. That is what the audience meets first. ' + r.rightTail
            : no() + 'you chose event ' + picked[0] + ': ' + ev[picked[0] - 1] + '. ' + r.diag[picked[0]];
          markPlot();
        } else {
          wasRight = same(picked, r.answer);
          if (wasRight) {
            msg = yes() + 'you marked ' + listEvents(picked) + ', and neither reaches the screen. ' + r.rightTail;
          } else if (!picked.length) {
            msg = no() + 'you marked nothing, so you said all five events reach the screen. Three do. ' + r.wrongTail;
          } else {
            var extra = picked.filter(function (n) { return r.answer.indexOf(n) < 0; });
            var missed = r.answer.filter(function (n) { return picked.indexOf(n) < 0; });
            msg = extra.length
              ? no() + 'you marked ' + listEvents(picked) + '. ' + up(listEvents(extra)) +
                (extra.length > 1 ? ' are on screen, so they belong' : ' is on screen, so it belongs') +
                ' to the plot as well as to the story. The film never shows ' +
                listEvents(r.answer) + '. ' + r.wrongTail
              : no() + 'you marked ' + listEvents(picked) + ', which is right as far as it goes. The film also never shows ' +
                listEvents(missed) + '. ' + r.wrongTail;
          }
          markPlot();
        }

        for (k = 0; k < 5; k++) { rows[k].classList.remove('is-sel'); rows[k].disabled = true; }
        for (k = 0; k < picked.length; k++) { rows[picked[k] - 1].classList.add('is-pick'); }

        attempted++;
        streak = wasRight ? streak + 1 : 0;
        if (streak >= 3 && !mastered) {
          mastered = true;
          msg += ' <strong class="pvs-yes">Three in a row — you have it.</strong> Story is everything that happens in the world of the film, in order; plot is what reaches the screen, and when. Theorists call them fabula and syuzhet.';
        }

        elCap.innerHTML = msg;
        elSr.textContent = elCap.textContent;
        elGo.textContent = mastered ? 'Another anyway' : 'Next cut';
        elGo.disabled = false;
        setStreak();
        push();
      }

      function labelOf(key) {
        for (var k = 0; k < OPTS.length; k++) {
          if (OPTS[k].key === key) {
            return '“' + OPTS[k].label.split(' — ')[0].toLowerCase() + '”';
          }
        }
        return key;
      }
      function up(t) { return t.charAt(0).toUpperCase() + t.slice(1); }
      function yes() { return '<strong class="pvs-yes">Right —</strong> '; }
      function no() { return '<strong class="pvs-no">Not quite —</strong> '; }

      function setStreak() {
        if (mastered) { elStreak.textContent = 'Mastered — three in a row.'; }
        else if (!attempted) { elStreak.textContent = ''; }
        else if (streak === 0) { elStreak.textContent = 'Back to zero — three in a row to finish.'; }
        else if (streak === 1) { elStreak.textContent = '1 right in a row.'; }
        else { elStreak.textContent = '2 in a row — one more and you have it.'; }
      }

      function push() {
        root.dataset.svState = JSON.stringify({
          streak: streak, mastered: mastered, attempted: attempted,
          round: roundIdx, question: R().q,
          answer: (R().q === 'effect') ? choice : picked.slice(),
          committed: committed, correct: committed ? wasRight : null
        });
      }

      /* ---------- threads ---------- */

      function draw() {
        var r = R(), w, h, k, row, chip, x1, y1, x2, y2, d, p, len;
        while (elSvg.firstChild) { elSvg.removeChild(elSvg.firstChild); }
        if (!chips[0].classList.contains('is-on')) return;
        w = elTracks.clientWidth; h = elTracks.clientHeight;
        if (!w || !h) return;
        elSvg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
        for (k = 0; k < r.order.length; k++) {
          row = rows[r.order[k] - 1]; chip = chips[k];
          x1 = row.offsetLeft + row.offsetWidth;
          y1 = row.offsetTop + row.offsetHeight / 2;
          x2 = chip.offsetLeft;
          y2 = chip.offsetTop + chip.offsetHeight / 2;
          d = Math.max(14, (x2 - x1) * 0.55);
          p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          p.setAttribute('d', 'M' + x1 + ' ' + y1 + ' C' + (x1 + d) + ' ' + y1 + ',' +
                              (x2 - d) + ' ' + y2 + ',' + x2 + ' ' + y2);
          p.setAttribute('fill', 'none');
          p.setAttribute('stroke', accent);
          p.setAttribute('stroke-width', '1.6');
          p.setAttribute('stroke-linecap', 'round');
          elSvg.appendChild(p);
          if (!reduced && p.getTotalLength) {
            len = p.getTotalLength();
            p.style.strokeDasharray = len;
            p.style.strokeDashoffset = len;
            p.getBoundingClientRect();
            p.style.transition = 'stroke-dashoffset .5s ease-out ' + (k * 0.09) + 's';
            p.style.strokeDashoffset = '0';
          }
        }
      }
    }
  };

  function css(a) {
    var tint = a + '18', line = a + '66';
    return [
      '.svw-pvs{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;max-width:560px}',
      '.svw-pvs *{box-sizing:border-box}',
      '.svw-pvs .pvs-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + a + ';margin:0 0 .15rem}',
      '.svw-pvs .pvs-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;font-weight:600;line-height:1.2;margin:0 0 .35rem}',
      '.svw-pvs .pvs-frame{font-size:.82rem;line-height:1.45;color:#5b564e;margin:0 0 .25rem}',
      '.svw-pvs .pvs-ask{font-size:.84rem;line-height:1.4;font-weight:600;margin:0 0 .5rem}',
      '.svw-pvs .pvs-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem .55rem;margin:0 0 .5rem}',
      '.svw-pvs .pvs-heads{max-width:380px;display:flex;justify-content:space-between;gap:.4rem;font-size:.66rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:#8d8880;margin:0 0 .3rem}',
      '.svw-pvs .pvs-tracks{position:relative;max-width:380px;display:grid;grid-template-columns:minmax(0,1fr) 38px;align-items:stretch}',
      '.svw-pvs .pvs-rows{max-width:240px;display:flex;flex-direction:column;gap:.25rem}',
      '.svw-pvs .pvs-row{display:flex;align-items:center;gap:.35rem;width:100%;text-align:left;font-family:inherit;font-size:.76rem;line-height:1.25;color:#2d2a26;background:#fff;border:1px solid #e8e2d9;border-radius:9px;padding:.32rem .38rem;cursor:pointer}',
      '.svw-pvs .pvs-row:disabled{cursor:default}',
      '.svw-pvs .pvs-num{flex:0 0 auto;width:17px;height:17px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.68rem;font-weight:700;background:#efe9e0;color:#5b564e;font-variant-numeric:tabular-nums}',
      '.svw-pvs .pvs-row.is-sel{background:#2d2a26;border-color:#2d2a26;color:#fff}',
      '.svw-pvs .pvs-row.is-sel .pvs-num{background:#fff;color:#2d2a26}',
      '.svw-pvs .pvs-row.is-shown{background:' + tint + ';border-color:' + line + '}',
      '.svw-pvs .pvs-row.is-cut{background:transparent;border-style:dashed;border-color:#ddd7cd;color:#8d8880}',
      '.svw-pvs .pvs-row.is-cut .pvs-num{background:#f2ede5;color:#a9a49b}',
      '.svw-pvs .pvs-row.is-pick{box-shadow:inset 0 0 0 2px #2d2a26}',
      '.svw-pvs .pvs-chips{grid-column:2;display:flex;flex-direction:column;justify-content:space-around;align-items:stretch}',
      '.svw-pvs .pvs-chip{visibility:hidden;font-size:.68rem;font-weight:700;text-align:center;color:' + a + ';background:' + tint + ';border:1px solid ' + line + ';border-radius:8px;padding:.22rem 0}',
      '.svw-pvs .pvs-chip.is-on{visibility:visible}',
      '.svw-pvs .pvs-threads{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}',
      '.svw-pvs .pvs-opts{display:flex;flex-direction:column;gap:.28rem;margin:0 0 .5rem}',
      '.svw-pvs .pvs-opt{font-family:inherit;font-size:.78rem;font-weight:600;text-align:left;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.42rem .6rem;cursor:pointer}',
      '.svw-pvs .pvs-opt.is-sel{background:#2d2a26;border-color:#2d2a26;color:#fff}',
      '.svw-pvs .pvs-foot{display:flex;align-items:center;justify-content:space-between;gap:.6rem;margin:0 0 .45rem}',
      '.svw-pvs .pvs-go{font-family:inherit;font-size:.82rem;font-weight:600;padding:.45rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
      '.svw-pvs .pvs-go:disabled{background:#faf8f5;border-color:#e0d9cd;color:#a9a49b;cursor:default}',
      '.svw-pvs .pvs-streak{font-size:.72rem;color:#8d8880;text-align:right;font-variant-numeric:tabular-nums}',
      '.svw-pvs .pvs-cap{font-size:.82rem;line-height:1.5;margin:0;min-height:3em}',
      '.svw-pvs .pvs-yes{color:#4f7d63}',
      '.svw-pvs .pvs-no{color:#2d2a26}',
      '.svw-pvs .pvs-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;border:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
    ].join('');
  }
})();
