/* Fractional distillation — where does it leave the column?
 * Self-contained lesson widget. No imports, no network, no storage.
 *
 * ONE RULE drives everything on screen, marking and reveal alike:
 *   a hydrocarbon condenses at the first level (scanning upwards from the
 *   400 degC base) whose temperature is BELOW its boiling point.
 *   - nothing cool enough anywhere  -> it never condenses, leaves the top as gas
 *   - even the 400 degC base is cooler than its boiling point -> it never
 *     vaporised at all, and drains off as bitumen.
 */
(function () {
  'use strict';

  var DEG = '°C';
  var MID = '·';
  var DASH = '—';

  /* Levels, BOTTOM first. Temperature t is the temperature of that level;
     a level collects every hydrocarbon whose boiling point lies between its
     own temperature and the temperature of the level beneath it. */
  var LEVELS = [
    { key: 'bitumen', t: 400, chip: '400' + DEG, name: 'Bitumen',
      sub: 'never boils ' + MID + ' drains at the base', frac: 'bitumen',
      aria: 'Never boils. Bitumen drains from the base at 400 degrees Celsius.' },
    { key: 'fuel-oil', t: 350, chip: '350' + DEG, name: 'Fuel oil', sub: '', frac: 'fuel oil',
      aria: 'Tray at 350 degrees Celsius. Fuel oil.' },
    { key: 'diesel', t: 250, chip: '250' + DEG, name: 'Diesel', sub: '', frac: 'diesel',
      aria: 'Tray at 250 degrees Celsius. Diesel.' },
    { key: 'kerosene', t: 150, chip: '150' + DEG, name: 'Kerosene', sub: '', frac: 'kerosene',
      aria: 'Tray at 150 degrees Celsius. Kerosene.' },
    { key: 'petrol', t: 25, chip: '25' + DEG, name: 'Petrol', sub: '', frac: 'petrol',
      aria: 'Tray at 25 degrees Celsius. Petrol.' },
    { key: 'gases', t: null, chip: 'gas out', name: 'Refinery gases',
      sub: 'leaves the top still a gas', frac: 'refinery gases',
      aria: 'Leaves the top of the column still a gas. Refinery gases.' }
  ];
  var BOTTOM = 0;
  var TOP = LEVELS.length - 1;

  /* Real alkanes, real boiling points, each at least 16 degC clear of a
     level temperature so no round sits on a boundary. */
  var POOL = [
    { n: 'Propane', c: 3, bp: -42, bpText: '−' + '42' + DEG },
    { n: 'Butane', c: 4, bp: -1, bpText: '−' + '1' + DEG },
    { n: 'Hexane', c: 6, bp: 69, bpText: '69' + DEG },
    { n: 'Heptane', c: 7, bp: 98, bpText: '98' + DEG },
    { n: 'Octane', c: 8, bp: 126, bpText: '126' + DEG },
    { n: 'Undecane', c: 11, bp: 196, bpText: '196' + DEG },
    { n: 'Dodecane', c: 12, bp: 216, bpText: '216' + DEG },
    { n: 'Tridecane', c: 13, bp: 234, bpText: '234' + DEG },
    { n: 'Pentadecane', c: 15, bp: 270, bpText: '270' + DEG },
    { n: 'Hexadecane', c: 16, bp: 287, bpText: '287' + DEG },
    { n: 'Octadecane', c: 18, bp: 317, bpText: '317' + DEG },
    { n: 'Docosane', c: 22, bp: 369, bpText: '369' + DEG },
    { n: 'Tricosane', c: 23, bp: 380, bpText: '380' + DEG },
    { n: 'Pentacontane', c: 50, bp: 520, bpText: 'over 500' + DEG },
    { n: 'Hexacontane', c: 60, bp: 620, bpText: 'over 600' + DEG }
  ];

  /* The single rule. Integers only, so no epsilon is needed. */
  function levelFor(bp) {
    for (var i = 0; i < LEVELS.length; i++) {
      if (LEVELS[i].t === null) return i;
      if (LEVELS[i].t < bp) return i;
    }
    return TOP;
  }

  function echoOf(i) {
    if (i === TOP) return 'it leaves the top as a gas';
    if (i === BOTTOM) return 'it never boils';
    return 'the ' + LEVELS[i].t + DEG + ' tray';
  }

  function rightText(item, i) {
    if (i === TOP) {
      return 'Right ' + DASH + ' out of the top as a gas. Even the coolest tray, 25' + DEG +
        ', is warmer than its boiling point of ' + item.bpText +
        ', so it never condenses: it leaves as refinery gases.';
    }
    if (i === BOTTOM) {
      return 'Right ' + DASH + ' it never boils. The base is only 400' + DEG +
        ', cooler than its boiling point of ' + item.bpText +
        ', so it stays liquid the whole way and drains off as bitumen.';
    }
    var below = LEVELS[i - 1].t;
    return 'Right ' + DASH + ' the ' + LEVELS[i].t + DEG + ' tray. It is still a gas at ' + below + DEG +
      '; ' + LEVELS[i].t + DEG + ' is the first level cooler than its boiling point of ' + item.bpText +
      ', so it condenses there as ' + LEVELS[i].frac + '.';
  }

  function wrongText(item, chosen, truth) {
    var head = 'Not quite ' + DASH + ' you said ' + echoOf(chosen) + '. ';
    if (truth === TOP) {
      return head + 'Every tray is warmer than its boiling point of ' + item.bpText +
        ', so it never condenses at all and leaves the top as refinery gases.';
    }
    if (truth === BOTTOM) {
      return head + 'It never boils in the first place: the base is 400' + DEG +
        ' and its boiling point of ' + item.bpText +
        ' is higher, so it cannot vaporise. It drains off as bitumen.';
    }
    var tt = LEVELS[truth].t, frac = LEVELS[truth].frac;
    if (chosen === TOP) {
      return head + 'Long chains do not rise highest. With a boiling point of ' + item.bpText +
        ' it condenses at the first level cooler than that ' + DASH + ' the ' + tt + DEG +
        ' tray, as ' + frac + '.';
    }
    if (chosen === BOTTOM) {
      return head + 'It does boil: the base is 400' + DEG + ', hotter than ' + item.bpText +
        ', so it vaporises and rises. It condenses at the ' + tt + DEG + ' tray, as ' + frac + '.';
    }
    if (chosen < truth) {
      return head + 'At ' + LEVELS[chosen].t + DEG + ' the column is still hotter than ' + item.bpText +
        ', so it is still a gas and keeps rising. It condenses higher, at the ' + tt + DEG +
        ' tray, as ' + frac + '.';
    }
    return head + 'It has already condensed by then: ' + tt + DEG +
      ' is the first level cooler than its boiling point of ' + item.bpText +
      ', so it never reaches ' + LEVELS[chosen].t + DEG + '. That tray collects ' + frac + '.';
  }

  var MASTERY = 'Three in a row ' + DASH + ' you have it. Nothing is burned and no bonds are broken: ' +
    'each hydrocarbon condenses at the first level cooler than its own boiling point, so long chains ' +
    'collect low and short chains stay gas to the top.';

  var OPENING = 'It all enters the base as one hot vapour ' + DASH + ' nothing is separated yet.';

  var CSS = [
    '.svw-fdbp{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;max-width:620px;margin:0 auto;line-height:1.4}',
    '.svw-fdbp *{box-sizing:border-box}',
    '.svw-fdbp .fd-kicker{margin:0 0 .15rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--fd-a)}',
    '.svw-fdbp .fd-title{margin:0 0 .3rem;font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.18}',
    '.svw-fdbp .fd-frame{margin:0 0 .55rem;font-size:.84rem;line-height:1.42;color:#5b564e}',
    '.svw-fdbp .fd-prompt{display:flex;flex-wrap:wrap;align-items:baseline;gap:.1rem .45rem;margin:0 0 .5rem;padding:.4rem .6rem;background:var(--fd-tint);border:1px solid var(--fd-line);border-radius:12px}',
    '.svw-fdbp .fd-mol{font-size:.92rem;font-weight:700}',
    '.svw-fdbp .fd-molsub{font-size:.78rem;color:#5b564e;font-variant-numeric:tabular-nums}',
    '.svw-fdbp .fd-stage{display:flex;gap:.45rem;padding:.45rem;background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px}',
    '.svw-fdbp .fd-bar{flex:0 0 6px;border-radius:3px;background:linear-gradient(to bottom,#e9eef1,#f4e4d2)}',
    '.svw-fdbp .fd-rows{flex:1;min-width:0;display:flex;flex-direction:column;gap:.25rem}',
    '.svw-fdbp .fd-row{display:grid;grid-template-columns:52px minmax(0,1fr) auto;align-items:center;gap:.45rem;width:100%;min-height:34px;margin:0;padding:.3rem .45rem;text-align:left;font:inherit;font-size:.84rem;color:#2d2a26;background:#fff;border:1px solid #e8e2d9;border-radius:9px;cursor:pointer}',
    '.svw-fdbp .fd-row:focus-visible{outline:2px solid var(--fd-a);outline-offset:2px}',
    '.svw-fdbp .fd-row[aria-pressed="true"]{background:var(--fd-tint);border-color:var(--fd-a);box-shadow:inset 0 0 0 1px var(--fd-a)}',
    '.svw-fdbp .fd-row.is-true{border-color:#4f7d63;box-shadow:inset 0 0 0 1px #4f7d63}',
    '.svw-fdbp .fd-row[disabled]{cursor:default;opacity:1}',
    '.svw-fdbp .fd-chip{font-size:.72rem;font-weight:700;font-variant-numeric:tabular-nums;color:#5b564e;background:#faf8f5;border:1px solid #eee7dc;border-radius:7px;padding:.1rem .18rem;text-align:center}',
    '.svw-fdbp .fd-label{min-width:0}',
    '.svw-fdbp .fd-name{font-weight:600;display:block}',
    '.svw-fdbp .fd-sub{display:block;font-size:.68rem;color:#8d8880;line-height:1.25}',
    '.svw-fdbp .fd-right{display:flex;align-items:center;gap:.35rem}',
    '.svw-fdbp .fd-mark{font-size:.64rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#5b564e;white-space:nowrap}',
    '.svw-fdbp .fd-mark.is-true{color:#4f7d63}',
    '.svw-fdbp .fd-dots{display:flex;gap:2px}',
    '.svw-fdbp .fd-dots i{width:5px;height:5px;border-radius:50%;background:var(--fd-a);display:block}',
    '.svw-fdbp .fd-commit{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem .7rem;margin:.5rem 0 .35rem}',
    '.svw-fdbp .fd-check{font:inherit;font-size:.84rem;font-weight:700;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.45rem 1rem;cursor:pointer}',
    '.svw-fdbp .fd-check:focus-visible{outline:2px solid var(--fd-a);outline-offset:2px}',
    '.svw-fdbp .fd-streak{margin:0;min-height:1.05rem;font-size:.74rem;font-weight:600;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svw-fdbp .fd-caption{margin:0;min-height:2.9rem;font-size:.84rem;line-height:1.45;color:#2d2a26}',
    '.svw-fdbp .fd-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svw-fdbp.fd-nomotion *{transition:none!important;animation:none!important}'
  ].join('\n');

  function hex(v) {
    v = (v || '').trim();
    return /^#[0-9a-fA-F]{6}$/.test(v) ? v : null;
  }

  window.SVWidget = {
    meta: {
      id: 'fractional-distillation-boiling-point',
      title: 'Up the fractionating column',
      teaches: 'Each hydrocarbon in crude oil condenses at the height where the column temperature first falls below its own boiling point, so high boiling points collect low down.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = hex(ctx.accent) || hex(getComputedStyle(root).getPropertyValue('--accent')) || '#9c5c33';

      root.className = (root.className ? root.className + ' ' : '') + 'svw-fdbp' + (ctx.reducedMotion ? ' fd-nomotion' : '');
      root.style.setProperty('--fd-a', accent);
      root.style.setProperty('--fd-tint', accent + '14');
      root.style.setProperty('--fd-line', accent + '3a');

      var style = document.createElement('style');
      style.textContent = CSS;
      root.appendChild(style);

      /* ---- markup, built once ---- */
      var head = document.createElement('div');
      head.innerHTML =
        '<p class="fd-kicker">Crude oil</p>' +
        '<h3 class="fd-title">Up the fractionating column</h3>' +
        '<p class="fd-frame">Crude oil vapour enters at 400' + DEG + ' and cools as it rises to 25' + DEG +
        ' at the top. Where does each hydrocarbon leave the column?</p>';
      root.appendChild(head);

      var prompt = document.createElement('p');
      prompt.className = 'fd-prompt';
      var molEl = document.createElement('span');
      molEl.className = 'fd-mol';
      var subEl = document.createElement('span');
      subEl.className = 'fd-molsub';
      prompt.appendChild(molEl);
      prompt.appendChild(subEl);
      root.appendChild(prompt);

      var stage = document.createElement('div');
      stage.className = 'fd-stage';
      var bar = document.createElement('div');
      bar.className = 'fd-bar';
      bar.setAttribute('aria-hidden', 'true');
      var rowsWrap = document.createElement('div');
      rowsWrap.className = 'fd-rows';
      stage.appendChild(bar);
      stage.appendChild(rowsWrap);
      root.appendChild(stage);

      var rows = [];
      for (var k = LEVELS.length - 1; k >= 0; k--) {
        (function (idx) {
          var lv = LEVELS[idx];
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'fd-row';
          b.setAttribute('aria-pressed', 'false');
          b.setAttribute('aria-label', lv.aria);
          b.dataset.lvl = String(idx);
          b.innerHTML =
            '<span class="fd-chip">' + lv.chip + '</span>' +
            '<span class="fd-label"><span class="fd-name">' + lv.name + '</span>' +
            (lv.sub ? '<span class="fd-sub">' + lv.sub + '</span>' : '') + '</span>' +
            '<span class="fd-right"><span class="fd-mark"></span><span class="fd-dots" aria-hidden="true"></span></span>';
          b.addEventListener('click', function () { pick(idx); });
          rowsWrap.appendChild(b);
          rows[idx] = b;
        })(k);
      }

      var commit = document.createElement('div');
      commit.className = 'fd-commit';
      var checkBtn = document.createElement('button');
      checkBtn.type = 'button';
      checkBtn.className = 'fd-check';
      checkBtn.textContent = 'Check';
      var streakEl = document.createElement('p');
      streakEl.className = 'fd-streak';
      commit.appendChild(checkBtn);
      commit.appendChild(streakEl);
      root.appendChild(commit);

      var caption = document.createElement('p');
      caption.className = 'fd-caption';
      caption.textContent = OPENING;
      root.appendChild(caption);

      var sr = document.createElement('p');
      sr.className = 'fd-sr';
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* ---- state ---- */
      var order = [], cursor = 0, item = null, truth = 0;
      var chosen = null, phase = 'ask';
      var streak = 0, attempted = 0, mastered = false;
      var collected = [];
      for (var c = 0; c < LEVELS.length; c++) collected[c] = 0;

      function shuffle() {
        order = POOL.slice();
        for (var i = order.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1));
          var t = order[i]; order[i] = order[j]; order[j] = t;
        }
        cursor = 0;
      }

      function sync() {
        root.dataset.svState = JSON.stringify({
          streak: streak,
          mastered: mastered,
          attempted: attempted,
          molecule: item ? item.n : null,
          boilingPoint: item ? item.bp : null,
          answer: LEVELS[truth].key,
          chosen: chosen === null ? null : LEVELS[chosen].key,
          correct: phase === 'done' ? (chosen === truth) : null
        });
      }

      function paintDots(i) {
        var box = rows[i].querySelector('.fd-dots');
        var want = Math.min(collected[i], 6);
        while (box.childElementCount > want) box.removeChild(box.lastChild);
        while (box.childElementCount < want) box.appendChild(document.createElement('i'));
      }

      function clearMarks() {
        for (var i = 0; i < rows.length; i++) {
          rows[i].classList.remove('is-true');
          rows[i].setAttribute('aria-pressed', 'false');
          rows[i].disabled = false;
          var m = rows[i].querySelector('.fd-mark');
          m.textContent = '';
          m.classList.remove('is-true');
        }
      }

      function nextRound() {
        if (!order.length || cursor >= order.length) shuffle();
        var candidate = order[cursor++];
        if (item && candidate.n === item.n && cursor < order.length) candidate = order[cursor++];
        item = candidate;
        truth = levelFor(item.bp);
        chosen = null;
        phase = 'ask';
        clearMarks();
        molEl.textContent = item.n;
        subEl.textContent = item.c + ' carbons ' + MID + ' boils at ' + item.bpText;
        caption.textContent = OPENING;
        checkBtn.textContent = 'Check';
        sr.textContent = 'New hydrocarbon: ' + item.n + ', ' + item.c + ' carbon atoms, boils at ' + item.bpText + '.';
        sync();
      }

      function pick(i) {
        if (phase !== 'ask') return;
        chosen = i;
        for (var r = 0; r < rows.length; r++) rows[r].setAttribute('aria-pressed', r === i ? 'true' : 'false');
        var where = (i === TOP) ? 'leaves the top as a gas'
          : (i === BOTTOM) ? 'never boils, and drains off as bitumen'
          : 'condenses at the ' + LEVELS[i].t + DEG + ' tray, as ' + LEVELS[i].frac;
        caption.textContent = 'Your prediction: ' + item.n + ' ' + where + '.';
        sr.textContent = 'Chosen: ' + echoOf(i) + '.';
        sync();
      }

      function check() {
        if (chosen === null) {
          caption.textContent = 'Pick the level where ' + item.n + ' leaves ' + DASH +
            ' the column gets cooler as you go up.';
          rows[3].focus();
          sr.textContent = caption.textContent;
          return;
        }
        phase = 'done';
        attempted++;
        var correct = chosen === truth;
        var hadRun = streak > 0;
        streak = correct ? streak + 1 : 0;
        var justMastered = false;
        if (correct && streak >= 3 && !mastered) { mastered = true; justMastered = true; }

        collected[truth]++;
        paintDots(truth);

        rows[truth].classList.add('is-true');
        var trueMark = rows[truth].querySelector('.fd-mark');
        trueMark.textContent = truth === TOP ? 'leaves here' : truth === BOTTOM ? 'stays here' : 'condenses';
        trueMark.classList.add('is-true');
        if (!correct) rows[chosen].querySelector('.fd-mark').textContent = 'your pick';
        for (var r = 0; r < rows.length; r++) rows[r].disabled = true;

        var msg = correct ? rightText(item, truth) : wrongText(item, chosen, truth);
        if (justMastered) msg = msg.split('.')[0] + '. ' + MASTERY;
        caption.textContent = msg;

        streakEl.textContent = !correct ? (hadRun ? 'Run back to zero ' + DASH + ' three in a row to finish.' : '')
          : streak === 1 ? '1 right in a row.'
          : streak === 2 ? '2 right in a row ' + DASH + ' one more and you have it.'
          : streak + ' right in a row.';

        checkBtn.textContent = mastered ? 'Another anyway' : 'Next hydrocarbon';
        sr.textContent = msg;
        sync();
      }

      checkBtn.addEventListener('click', function () {
        if (phase === 'done') nextRound(); else check();
      });

      shuffle();
      nextRound();
    }
  };
})();
