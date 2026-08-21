/* holderness-hard-defences
   Hard defences hold the stretch they stand on, but they trap or cut off the
   sediment travelling along the coast. A sediment budget runs down six
   stretches of the Holderness coast; beach width is the buffer, and cliff
   retreat is derived from it. The student predicts what a proposed scheme
   does to a named stretch, commits, and then watches the whole coast redraw.
   Every number in the feedback comes out of the model. */
(function () {
  'use strict';

  /* ---------- the coast, north (top) to south (bottom) ---------- */
  var PLACES = ['Skipsea', 'Atwick', 'Mappleton', 'Great Cowden', 'Aldbrough', 'Tunstall'];

  /* ---------- the sediment budget ----------
     Each stretch receives sediment from the one updrift, its boulder-clay
     cliff adds more as it crumbles, and about half of what arrives is lost
     offshore. Undefended, that settles at a steady throughput: a 25 m beach
     and 1.8 m of cliff retreat a year, the Holderness average.
     Beach width is the buffer, so retreat rises as the beach thins.        */
  var IN0 = 100;        /* sediment arriving from the north (index units)   */
  var CLIFF = 50;       /* added by an undefended boulder-clay cliff        */
  var ONWARD = 0.5;     /* fraction of arriving sediment that travels on    */
  var BEACH_K = 0.2;    /* index units -> metres of beach                   */
  var BASE = 1.8;       /* m of cliff retreat a year on the natural coast   */
  var REF = 25;         /* the natural beach width, in metres              */
  var HELD = 0.1;       /* retreat behind a structure that is holding       */

  var SCHEMES = {
    groynes: {
      noun: 'Rock groynes',
      frame: 'Two rock groynes — barriers built out into the sea — are proposed at',
      cliff: 0, hold: 45, imported: 0, scour: 1, holds: true
    },
    wall: {
      noun: 'A sea wall',
      frame: 'A curved concrete sea wall is proposed at',
      cliff: 0, hold: 0, imported: 0, scour: 0.72, holds: true
    },
    armour: {
      noun: 'Rock armour',
      frame: 'Rock armour along the cliff foot is proposed at',
      cliff: 0, hold: 0, imported: 0, scour: 1, holds: true
    },
    nourish: {
      noun: 'Beach nourishment',
      frame: 'Beach nourishment — imported sand piled on the beach — is proposed at',
      cliff: 20, hold: 0, imported: 110, scour: 1, holds: false
    }
  };

  /* Run the budget down the coast. scheme = {type, at} or null for natural. */
  function simulate(scheme) {
    var rows = [], arrive = IN0, i;
    for (i = 0; i < PLACES.length; i++) {
      var s = (scheme && scheme.at === i) ? SCHEMES[scheme.type] : null;
      var cliff = s ? s.cliff : CLIFF;
      var hold = s ? s.hold : 0;
      var imported = s ? s.imported : 0;
      var scour = s ? s.scour : 1;
      var beachIdx = (arrive + 0.5 * cliff + hold + imported) * scour;
      var width = beachIdx * BEACH_K;
      var retreat = (s && s.holds) ? HELD
        : Math.min(4, Math.max(0.3, BASE * Math.sqrt(REF / width)));
      rows.push({ width: width, retreat: retreat, scheme: s ? scheme.type : null });
      arrive = Math.max(0, ONWARD * arrive + cliff + imported - hold);
    }
    return rows;
  }

  var NATURAL = simulate(null);

  function m(x) { return Math.round(x); }              /* metres of beach   */
  function t(x) { return Math.round(x * 10); }         /* tenths of a metre */
  function rate(x) { return (t(x) / 10).toFixed(1); }  /* what is displayed */

  /* Decided on the displayed tenths, never on a bare float: faster is a
     rise of 12% or more, slower is a fall of 10% or more. Every round in
     the pool sits at least two tenths clear of both boundaries.           */
  function verdict(before, after) {
    var b = t(before), a = t(after);
    if (a * 100 >= b * 112) return 'speeds';
    if (a * 100 <= b * 90) return 'slows';
    return 'same';
  }

  /* ---------- the rounds ---------- */
  var ROUNDS = [
    { d: 'groynes', at: 2, ask: 3 },
    { d: 'nourish', at: 1, ask: 2 },
    { d: 'groynes', at: 3, ask: 1 },
    { d: 'wall', at: 4, ask: 5 },
    { d: 'armour', at: 0, ask: 1 },
    { d: 'wall', at: 2, ask: 2 },
    { d: 'groynes', at: 1, ask: 3 },
    { d: 'nourish', at: 2, ask: 3 },
    { d: 'armour', at: 4, ask: 2 }
  ];
  ROUNDS.forEach(function (r) {
    r.after = simulate({ type: r.d, at: r.at });
    r.truth = verdict(NATURAL[r.ask].retreat, r.after[r.ask].retreat);
  });

  var VERB = { speeds: 'speeds up', same: 'stays about the same', slows: 'slows down' };
  var OPTION = [
    { k: 'speeds', label: 'Speeds up' },
    { k: 'same', label: 'Stays about the same' },
    { k: 'slows', label: 'Slows down' }
  ];

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), s = a[i]; a[i] = a[j]; a[j] = s;
    }
    return a;
  }

  /* Open on the Mappleton case, then guarantee two different answers in the
     next two rounds, so nobody masters this by pressing one button. */
  function buildOrder() {
    var first = ROUNDS[0];
    var rest = ROUNDS.slice(1);
    var slow = shuffle(rest.filter(function (r) { return r.truth === 'slows'; }));
    var same = shuffle(rest.filter(function (r) { return r.truth === 'same'; }));
    var pair = shuffle([slow.shift(), same.shift()]);
    var tail = shuffle(rest.filter(function (r) {
      return r !== pair[0] && r !== pair[1];
    }));
    return [first, pair[0], pair[1]].concat(tail);
  }

  /* ---------- little DOM helpers ---------- */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function frag(parent, parts) {
    parent.textContent = '';
    parts.forEach(function (p) {
      if (typeof p === 'string') parent.appendChild(document.createTextNode(p));
      else parent.appendChild(p);
    });
  }

  function css(accent, tint) {
    return [
      '.svw-hd{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;',
      'color:#2d2a26;line-height:1.45;}',
      '.svw-hd *{box-sizing:border-box;}',
      '.svw-hd-kicker{font-size:.66rem;font-weight:700;letter-spacing:.11em;',
      'text-transform:uppercase;color:', accent, ';margin:0 0 .18rem;}',
      '.svw-hd-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;',
      'font-weight:600;margin:0 0 .35rem;line-height:1.2;}',
      '.svw-hd-frame{font-size:.88rem;margin:0 0 .5rem;max-width:66ch;}',
      '.svw-hd-frame b{font-weight:700;}',
      '.svw-hd-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;',
      'padding:.55rem .7rem .45rem;}',
      '.svw-hd-strip{display:grid;grid-template-columns:15px minmax(0,1fr) 97px;',
      'column-gap:.5rem;row-gap:.3rem;align-items:center;}',
      '.svw-hd-rail{grid-column:1;grid-row:1 / span 6;display:flex;flex-direction:column;',
      'align-items:center;justify-content:space-between;height:100%;',
      'font-size:.66rem;color:#8d8880;letter-spacing:.04em;}',
      '.svw-hd-railline{flex:1;width:0;border-left:1px dashed #cfc7ba;margin:2px 0;}',
      '.svw-hd-arrow{width:0;height:0;border-left:3.5px solid transparent;',
      'border-right:3.5px solid transparent;border-top:5px solid #b7ae9f;margin-bottom:2px;}',
      '.svw-hd-track{grid-column:2;position:relative;height:14px;background:#e4eaec;',
      'border-right:2px solid #2d2a26;border-radius:3px 0 0 3px;}',
      '.svw-hd-track--ask{outline:1.5px solid ', accent, ';outline-offset:1.5px;}',
      '.svw-hd-beach{position:absolute;right:0;top:0;bottom:0;background:#e6d6b2;',
      'border-radius:2px 0 0 2px;transition:width .55s cubic-bezier(.16,1,.3,1);}',
      '.svw-hd--still .svw-hd-beach{transition:none;}',
      '.svw-hd-def{position:absolute;right:0;top:-2px;bottom:-2px;}',
      '.svw-hd-strip[data-built="0"] .svw-hd-def{opacity:.4;}',
      '.svw-hd-def--wall{width:5px;background:#2d2a26;border-radius:1px;}',
      '.svw-hd-def--groynes{width:22px;background:repeating-linear-gradient(180deg,',
      'transparent 0 3px,#2d2a26 3px 5px,transparent 5px 9px);}',
      '.svw-hd-def--armour{width:8px;background:repeating-linear-gradient(45deg,',
      '#2d2a26 0 2px,transparent 2px 4px);}',
      '.svw-hd-def--nourish{width:30px;background:repeating-linear-gradient(90deg,',
      'rgba(45,42,38,.3) 0 2px,transparent 2px 6px);}',
      '.svw-hd-name{grid-column:3;font-size:.72rem;color:#5b564e;line-height:1.2;}',
      '.svw-hd-name--site{color:#2d2a26;font-weight:700;}',
      '.svw-hd-name--ask{color:#2d2a26;font-weight:700;}',
      '.svw-hd-name--ask::before{content:"";display:inline-block;width:6px;height:6px;',
      'border-radius:50%;background:', accent, ';margin-right:5px;vertical-align:middle;}',
      '.svw-hd-readout{font-size:.8rem;color:#5b564e;margin:.45rem 0 0;',
      'font-variant-numeric:tabular-nums;}',
      '.svw-hd-answers{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));',
      'gap:.4rem;margin:.5rem 0 0;}',
      '.svw-hd-opt{font-family:inherit;font-size:.78rem;font-weight:600;color:#2d2a26;',
      'background:#fff;border:1px solid #ddd7cd;border-radius:10px;padding:.5rem .3rem;',
      'min-height:42px;text-align:center;cursor:pointer;line-height:1.25;}',
      '.svw-hd-opt:hover:not(:disabled){border-color:#b9b1a4;}',
      '.svw-hd-opt--truth{border-color:#4f7d63;color:#4f7d63;}',
      '.svw-hd-opt[aria-pressed="true"]{background:#2d2a26;color:#fff;border-color:#2d2a26;}',
      '.svw-hd-opt:disabled{cursor:default;}',
      '.svw-hd-actions{display:flex;align-items:center;justify-content:space-between;',
      'gap:.6rem;margin-top:.4rem;min-height:36px;}',
      '.svw-hd-streak{font-size:.76rem;color:#5b564e;flex:1 1 auto;min-width:0;}',
      '.svw-hd-go{font-family:inherit;font-size:.82rem;font-weight:600;color:#fff;',
      'background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;',
      'padding:.5rem .95rem;cursor:pointer;margin-left:auto;flex:0 0 auto;white-space:nowrap;}',
      '.svw-hd-go--wait{visibility:hidden;}',
      '.svw-hd-cap{font-size:.86rem;line-height:1.48;margin:.45rem 0 0;min-height:4.6em;',
      'max-width:66ch;}',
      '.svw-hd-mark{font-weight:700;}',
      '.svw-hd-done{color:#4f7d63;font-weight:700;}',
      '.svw-hd-sr{position:absolute;width:1px;height:1px;overflow:hidden;',
      'clip:rect(0 0 0 0);white-space:nowrap;}',
      '.svw-hd-tint{background:', tint, ';}'
    ].join('');
  }

  function mount(root, ctx) {
    ctx = ctx || {};
    var probe = (window.getComputedStyle(root).getPropertyValue('--accent') || '').trim();
    var accent = probe || ctx.accent || '#8a6a4f';
    var tint = /^#[0-9a-f]{6}$/i.test(accent) ? accent + '1f' : accent;
    var reduced = !!ctx.reducedMotion;

    root.textContent = '';
    var wrap = el('div', 'svw-hd' + (reduced ? ' svw-hd--still' : ''));
    var style = document.createElement('style');
    style.textContent = css(accent, tint);
    wrap.appendChild(style);

    wrap.appendChild(el('p', 'svw-hd-kicker', 'Coastal management'));
    wrap.appendChild(el('h3', 'svw-hd-title', 'Defending the Holderness coast'));
    var frame = el('p', 'svw-hd-frame');
    wrap.appendChild(frame);

    /* ---- stage: one strip of coast, sea on the left, land on the right ---- */
    var stage = el('div', 'svw-hd-stage');
    var strip = el('div', 'svw-hd-strip');
    strip.setAttribute('data-built', '0');
    var rail = el('div', 'svw-hd-rail');
    rail.appendChild(el('span', null, 'N'));
    rail.appendChild(el('span', 'svw-hd-railline'));
    rail.appendChild(el('span', 'svw-hd-arrow'));
    rail.appendChild(el('span', null, 'S'));
    strip.appendChild(rail);

    var tracks = [], beaches = [], marks = [], names = [];
    PLACES.forEach(function (name, i) {
      var track = el('div', 'svw-hd-track');
      var beach = el('span', 'svw-hd-beach');
      var mark = el('span', 'svw-hd-def');
      mark.style.display = 'none';
      track.appendChild(beach);
      track.appendChild(mark);
      var label = el('div', 'svw-hd-name', name);
      strip.appendChild(track);
      strip.appendChild(label);
      tracks.push(track); beaches.push(beach); marks.push(mark); names.push(label);
    });
    stage.appendChild(strip);
    var readout = el('p', 'svw-hd-readout');
    stage.appendChild(readout);
    wrap.appendChild(stage);

    /* ---- controls ---- */
    var answers = el('div', 'svw-hd-answers');
    var opts = OPTION.map(function (o) {
      var b = el('button', 'svw-hd-opt', o.label);
      b.type = 'button';
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () { pick(o.k); });
      answers.appendChild(b);
      return b;
    });
    wrap.appendChild(answers);

    var actions = el('div', 'svw-hd-actions');
    var streakLine = el('span', 'svw-hd-streak', '');
    var go = el('button', 'svw-hd-go svw-hd-go--wait', 'See what happens');
    go.type = 'button';
    go.addEventListener('click', onGo);
    actions.appendChild(streakLine);
    actions.appendChild(go);
    wrap.appendChild(actions);

    var cap = el('p', 'svw-hd-cap');
    wrap.appendChild(cap);
    var sr = el('p', 'svw-hd-sr');
    sr.setAttribute('aria-live', 'polite');
    wrap.appendChild(sr);

    root.appendChild(wrap);

    /* ---- state ---- */
    var order = buildOrder(), at = 0, round = null;
    var picked = null, committed = false;
    var streak = 0, attempted = 0, mastered = false;

    function scale(width) {
      var pct = Math.max(2, Math.min(100, (width / 50) * 100));
      return pct.toFixed(1) + '%';
    }

    function paint(rows) {
      rows.forEach(function (r, i) { beaches[i].style.width = scale(r.width); });
    }

    function setState() {
      root.dataset.svState = JSON.stringify({
        scheme: round.d, site: PLACES[round.at], ask: PLACES[round.ask],
        answer: picked, expected: round.truth,
        correct: committed ? picked === round.truth : null,
        beachAfter: m(round.after[round.ask].width),
        retreatAfter: Number(rate(round.after[round.ask].retreat)),
        streak: streak, mastered: mastered, attempted: attempted
      });
    }

    function newRound() {
      round = order[at % order.length];
      at++;
      picked = null; committed = false;
      var site = PLACES[round.at], ask = PLACES[round.ask];
      var rel = round.ask === round.at ? ' itself'
        : round.ask === round.at + 1 ? ', just south'
          : round.ask > round.at ? ', two stretches south'
            : ', to the north';

      frag(frame, [
        SCHEMES[round.d].frame + ' ',
        el('b', 'svw-hd-site', site),
        '. Predict what happens to cliff retreat at ',
        el('b', 'svw-hd-site', ask),
        rel + '.'
      ]);

      strip.setAttribute('data-built', '0');
      marks.forEach(function (mk, i) {
        mk.style.display = i === round.at ? 'block' : 'none';
        mk.className = 'svw-hd-def svw-hd-def--' + round.d;
      });
      names.forEach(function (n, i) {
        n.className = 'svw-hd-name' +
          (i === round.at ? ' svw-hd-name--site' : '') +
          (i === round.ask ? ' svw-hd-name--ask' : '');
      });
      tracks.forEach(function (tr, i) {
        tr.className = 'svw-hd-track' + (i === round.ask ? ' svw-hd-track--ask' : '');
      });
      paint(NATURAL);
      readout.textContent = ask + ' now — beach ' + m(NATURAL[round.ask].width) +
        ' m · cliff retreat ' + rate(NATURAL[round.ask].retreat) + ' m a year';

      opts.forEach(function (b) {
        b.disabled = false;
        b.setAttribute('aria-pressed', 'false');
        b.className = 'svw-hd-opt';
      });
      go.textContent = 'See what happens';
      go.className = 'svw-hd-go svw-hd-go--wait';

      frag(cap, [
        'No defences on this stretch yet: a ', String(m(NATURAL[0].width)),
        ' m beach the whole way down, and the boulder-clay cliffs losing ',
        rate(NATURAL[0].retreat),
        ' m a year. The beach is the buffer — it soaks up the wave energy ',
        'before it reaches the cliff foot.'
      ]);
      showStreak();
      setState();
    }

    function pick(k) {
      if (committed) return;
      picked = k;
      opts.forEach(function (b, i) {
        b.setAttribute('aria-pressed', OPTION[i].k === k ? 'true' : 'false');
      });
      go.className = 'svw-hd-go';
      setState();
    }

    function showStreak() {
      if (mastered) {
        streakLine.textContent = streak + ' right in a row.';
      } else if (streak === 1) {
        streakLine.textContent = '1 right — two more and you have it.';
      } else if (streak === 2) {
        streakLine.textContent = '2 right — one more and you have it.';
      } else {
        streakLine.textContent = '';
      }
    }

    function onGo() {
      if (committed) { newRound(); return; }
      if (!picked) return;
      commit();
    }

    function commit() {
      committed = true;
      attempted++;
      var right = picked === round.truth;
      streak = right ? streak + 1 : 0;
      var justMastered = false;
      if (right && streak >= 3 && !mastered) { mastered = true; justMastered = true; }

      strip.setAttribute('data-built', '1');
      paint(round.after);

      var site = PLACES[round.at], ask = PLACES[round.ask];
      var b0 = m(NATURAL[round.ask].width), b1 = m(round.after[round.ask].width);
      var e0 = rate(NATURAL[round.ask].retreat), e1 = rate(round.after[round.ask].retreat);
      readout.textContent = ask + ' — beach ' + b0 + ' → ' + b1 +
        ' m · cliff retreat ' + e0 + ' → ' + e1 + ' m a year';

      opts.forEach(function (b, i) {
        b.disabled = true;
        if (!right && OPTION[i].k === round.truth) b.className = 'svw-hd-opt svw-hd-opt--truth';
      });

      var opener = right
        ? 'Right — you said retreat at ' + ask + ' ' + VERB[picked] + '. '
        : 'Not quite — you said retreat at ' + ask + ' ' + VERB[picked] +
          '; it ' + VERB[round.truth] + '. ';

      var body = mastered && right && justMastered
        ? masteryText()
        : explain(site, ask, b0, b1, e0, e1);

      frag(cap, [
        el('span', 'svw-hd-mark' + (justMastered ? ' svw-hd-done' : ''), opener),
        body
      ]);
      sr.textContent = opener + body + ' Beach widths, north to south: ' +
        round.after.map(function (r, i) { return PLACES[i] + ' ' + m(r.width) + ' m'; }).join(', ') + '.';

      go.textContent = mastered ? 'Another anyway' : 'Next scheme';
      go.className = 'svw-hd-go';
      showStreak();
      setState();
    }

    function masteryText() {
      return 'Three in a row — you have it. The coast is one sediment system: ' +
        'trap the drift, or armour the cliffs that feed it, and every beach ' +
        'downdrift goes hungry while its cliff takes the wave energy. Mappleton ' +
        'got rock groynes in 1991; the cliffs at Great Cowden, just south, then ' +
        'lost ground much faster.';
    }

    function explain(site, ask, b0, b1, e0, e1) {
      var d = round.d;
      var bSite = m(round.after[round.at].width);
      if (round.ask < round.at) {
        return ask + ' sits updrift of ' + site + ': its sediment arrives from ' +
          'further north, and nothing built to the south can change that. Beach ' +
          'stays ' + b0 + ' m, retreat stays ' + e0 + ' m a year. A defence pushes ' +
          'its problem downdrift, never back up the coast — look at the ' +
          'stretches below ' + site + '.';
      }
      if (round.ask === round.at) {
        if (d === 'nourish') {
          return 'The imported sand gives ' + site + ' a ' + b1 + ' m beach that ' +
            'soaks up wave energy before it reaches the cliff: retreat eases ' +
            e0 + ' → ' + e1 + ' m a year. It is the one scheme that adds sediment ' +
            'rather than removing it — but the drift carries it away, so it has ' +
            'to be replaced.';
        }
        var own = d === 'wall'
          ? 'Reflected waves scour its own beach, ' + b0 + ' → ' + b1 + ' m. '
          : d === 'groynes'
            ? 'The trapped sand widens its own beach to ' + b1 + ' m. '
            : 'Its own beach thins to ' + b1 + ' m without the cliff’s sand. ';
        return 'The structure holds the cliff line at ' + site + ' itself: retreat ' +
          'drops ' + e0 + ' → ' + e1 + ' m a year while it stands. ' + own +
          'But the sediment that cliff used to shed is now missing from every ' +
          'beach south of it.';
      }
      if (d === 'groynes') {
        return 'The groynes hold the drifting sediment on their updrift side, so ' +
          site + '’s beach widens to ' + bSite + ' m and little gets past. ' + ask +
          ' loses the beach that absorbed the wave energy: ' + b0 + ' → ' + b1 +
          ' m, retreat ' + e0 + ' → ' + e1 + ' m a year. Protecting ' + site +
          ' moves the loss downdrift.';
      }
      if (d === 'wall') {
        return 'The wall stops the boulder-clay cliff at ' + site + ' crumbling — ' +
          'and that cliff was the supply feeding sediment south. ' + ask +
          ' receives less: beach ' + b0 + ' → ' + b1 + ' m, retreat ' + e0 + ' → ' +
          e1 + ' m a year. The wall holds ' + site + '; the sea takes it out on ' +
          ask + ' instead.';
      }
      if (d === 'armour') {
        return 'Rock armour shields the cliff foot at ' + site + ', so that cliff ' +
          'stops crumbling into the drift — and those cliffs are the sediment ' +
          'supply. ' + ask + '’s beach thins ' + b0 + ' → ' + b1 + ' m and retreat ' +
          'rises ' + e0 + ' → ' + e1 + ' m a year. Stopping erosion here stops the ' +
          'sand arriving there.';
      }
      return 'Nourishment adds sand to the system instead of trapping what is ' +
        'already moving through it. The drift carries the surplus south, so ' + ask +
        '’s beach widens ' + b0 + ' → ' + b1 + ' m and retreat eases ' + e0 + ' → ' +
        e1 + ' m a year. The sand has to be replaced as the drift moves it on.';
    }

    newRound();
  }

  window.SVWidget = {
    meta: {
      id: 'holderness-hard-defences',
      title: 'Defending the Holderness coast',
      teaches: 'Hard defences hold the stretch they stand on, but by trapping the ' +
        'drift or cutting off the cliffs that feed it they starve the beaches ' +
        'downdrift, where erosion then speeds up.'
    },
    mount: mount
  };
})();
