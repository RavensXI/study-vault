/* Follow the energy — conservation-of-energy-dispersal
   The student allocates a device's whole energy input across the stores it
   really ends up in. Nothing is destroyed, nothing is used up, and the total
   must balance exactly. Commit with Check, then the reveal teaches. */
(function () {
  'use strict';

  var ROUNDS = [
    {
      id: 'kettle',
      device: 'Electric kettle',
      scenario: 'An electric kettle takes in |{input} J| of energy by electrical working.',
      evidence: 'The water reaches 100 °C. The kettle body is hot to touch, and steam leaves the spout.',
      input: 2000,
      step: 100,
      rows: [
        { label: 'Thermal store of the water — by heating', fixed: 1700, kind: 'useful' },
        { label: 'Thermal store of the kettle body and stand', kind: 'waste' },
        { label: 'Thermal store of the kitchen air and steam', kind: 'waste' },
        { label: 'Destroyed — these joules stop existing', kind: 'trap',
          msg: 'Nothing was destroyed. Those {n} J are in the thermal store of the kettle body, the steam and the kitchen air — you can feel them.' }
      ],
      win: 'Balanced: {input} J in, {input} J still here. {useful} J sits in the water’s thermal store — {eff}% efficient. Heating spread the other {waste} J through the body, the steam and the air: dispersed, not destroyed.'
    },
    {
      id: 'hoist',
      device: 'Electric hoist',
      scenario: 'An electric hoist lifts a crate, taking in |{input} J| by electrical working.',
      evidence: 'A 50 kg crate rises 8 m, so m g h = 4000 J. The motor casing and the gearbox are warm afterwards, and the hoist whines.',
      input: 5000,
      step: 200,
      rows: [
        { label: 'Gravitational potential store of the crate', fixed: 4000, kind: 'useful' },
        { label: 'Thermal store of the motor and gears', kind: 'waste' },
        { label: 'Thermal store of the air around the hoist', kind: 'waste' },
        { label: 'Used up — spent doing the lifting', kind: 'trap',
          msg: 'Energy is never used up. Lifting is a transfer, not a cost: those {n} J are heating the motor, the gears and the air.' }
      ],
      win: 'Balanced: {input} J in, {input} J still here. Mechanical working put {useful} J into the crate’s gravitational potential store — {eff}% efficient. Friction heated the other {waste} J into the surroundings.'
    },
    {
      id: 'rabbit',
      device: 'Rabbit eating grass',
      scenario: 'A rabbit eats grass holding |{input} J| in its chemical store.',
      evidence: 'The rabbit breathes hard, hops about all day and leaves droppings behind. It puts on very little weight.',
      input: 8000,
      step: 800,
      rows: [
        { label: 'Chemical store of the rabbit’s new tissue', fixed: 800, kind: 'useful' },
        { label: 'Chemical store of the droppings and urine', fixed: 3200, kind: 'waste' },
        { label: 'Thermal store of the surroundings', kind: 'waste' },
        { label: 'Destroyed — used up staying alive', kind: 'trap',
          msg: 'Nothing is used up. Those {n} J left the rabbit by heating: respiration and hopping warmed the air, the burrow and the ground.' }
      ],
      win: 'Balanced: {input} J eaten, {input} J still here. Just {useful} J becomes new tissue — about {eff}% passed on. Respiration and hopping heated {r2} J into the surroundings; {r1} J stays in the droppings.'
    },
    {
      id: 'lamp',
      device: 'Filament lamp',
      scenario: 'A filament lamp takes in |{input} J| of energy by electrical working.',
      evidence: 'The bulb glows. After a minute the glass is too hot to touch, and so is the shade above it.',
      input: 1000,
      step: 10,
      rows: [
        { label: 'Thermal store of the filament, glass and air', fixed: 950, kind: 'waste' },
        { label: 'Radiated as light — the walls absorb it', kind: 'useful' },
        { label: 'Destroyed — these joules stop existing', kind: 'trap',
          msg: 'Nothing is destroyed. Those {n} J heated the filament, the glass and the air around the lamp, and they are still there.' },
        { label: 'Used up — spent making the bulb glow', kind: 'trap',
          msg: 'Glowing is a transfer, not a cost. Those {n} J left the lamp by radiation or by heating, and both routes end in the room.' }
      ],
      win: 'Balanced: {input} J in, {input} J still here. Only {useful} J is radiated as light — {eff}% efficient. The walls absorb that light too, so all {input} J ends in the room’s thermal store.'
    },
    {
      id: 'brakes',
      device: 'Bicycle braking',
      scenario: 'A cyclist brakes to a stop from |{input} J| in the kinetic store of bike and rider.',
      evidence: '80 kg travelling at 5 m/s, so the kinetic store holds 1000 J. The blocks smell hot, the rims are warm and the brakes squeal.',
      input: 1000,
      step: 20,
      rows: [
        { label: 'Thermal store of the brake blocks and rims', fixed: 900, kind: 'waste' },
        { label: 'Thermal store of the air and surroundings', kind: 'waste' },
        { label: 'Kinetic store of the bike — some is kept', kind: 'trap',
          msg: 'The bike has stopped, so v = 0 and its kinetic store is empty. Those {n} J are in the blocks, the rims and the air.' },
        { label: 'Destroyed — stopping wipes it out', kind: 'trap',
          msg: 'Stopping destroys nothing. Those {n} J are in the thermal store of the blocks, the rims and the air — hot enough to burn a finger.' }
      ],
      win: 'Balanced: {input} J of kinetic store, {input} J still here. Braking dissipates on purpose: friction heated all {waste} J into the blocks, the rims and the air — none of it gone.'
    }
  ];

  var CSS = [
    '.svw-coe{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
    '.svw-coe *{box-sizing:border-box}',
    '.svw-coe .coe-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--coe-accent);margin:0 0 .15rem}',
    '.svw-coe .coe-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.2;margin:0 0 .55rem}',
    '.svw-coe .coe-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.55rem .65rem}',
    '.svw-coe .coe-frame{font-size:.84rem;line-height:1.5;margin:0 0 .5rem;color:#2d2a26}',
    '.svw-coe .coe-frame b{font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap}',
    '.svw-coe .coe-bar{display:flex;height:24px;border-radius:8px;overflow:hidden;background:#fff;border:1px solid #e0d9cd}',
    '.svw-coe .coe-bar.is-over{border-color:#2d2a26;border-style:dashed}',
    '.svw-coe .coe-seg{height:100%;min-width:0;background:var(--coe-soft);border-right:1px solid #fff;transition:width .18s ease}',
    '.svw-coe.is-still .coe-seg{transition:none}',
    '.svw-coe .coe-seg.k-useful{background:var(--coe-accent)}',
    '.svw-coe .coe-seg.k-waste{background:#c9c0b2}',
    '.svw-coe .coe-seg.k-trap{background:repeating-linear-gradient(45deg,#e6ded2 0 5px,#f7f3ed 5px 10px)}',
    '.svw-coe .coe-tail{flex:1 1 auto;min-width:0}',
    '.svw-coe .coe-left{display:flex;align-items:baseline;gap:.4rem;margin:0 0 .45rem;color:#5b564e}',
    '.svw-coe .coe-big{font-size:1.3rem;font-weight:600;line-height:1.1;color:#2d2a26;font-variant-numeric:tabular-nums}',
    '.svw-coe .coe-leadlab{font-size:.78rem;font-weight:600}',
    '.svw-coe .coe-rows{margin:.15rem 0 0}',
    '.svw-coe .coe-row{display:flex;align-items:center;gap:.5rem;padding:.42rem 0;border-bottom:1px solid #efe9e0}',
    '.svw-coe .coe-lab{flex:1 1 auto;font-size:.82rem;min-width:0}',
    '.svw-coe .coe-row.is-given .coe-lab{font-size:.78rem;color:#8d8880}',
    '.svw-coe .coe-ctl{display:flex;align-items:center;gap:.3rem;flex:0 0 auto}',
    '.svw-coe .coe-tag{font-size:.66rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#8d8880;margin-right:.35rem;white-space:nowrap}',
    '.svw-coe .coe-tag.t-useful{color:var(--coe-accent)}',
    '.svw-coe .coe-val{font-size:.82rem;font-weight:600;font-variant-numeric:tabular-nums;text-align:center;min-width:3.4rem}',
    '.svw-coe .coe-val.is-fixed{text-align:right;min-width:4.4rem}',
    '.svw-coe .coe-val.is-fixed{color:#5b564e}',
    '.svw-coe button.coe-step{width:30px;height:30px;padding:0;border:1px solid #ddd7cd;background:#faf8f5;border-radius:8px;font:inherit;font-size:1rem;line-height:1;color:#2d2a26;cursor:pointer}',
    '.svw-coe button.coe-step:hover:not(:disabled){border-color:#c8bfb1}',
    '.svw-coe button.coe-step:disabled{opacity:.35;cursor:default}',
    '.svw-coe .coe-act{display:flex;align-items:center;gap:.7rem;flex-wrap:wrap;margin:.5rem 0 0}',
    '.svw-coe button.coe-go{background:#2d2a26;color:#fff;border:1px solid #2d2a26;border-radius:10px;padding:.5rem 1.05rem;font:inherit;font-size:.82rem;font-weight:600;cursor:pointer}',
    '.svw-coe button.coe-go:hover{background:#413c36}',
    '.svw-coe .coe-streak{font-size:.78rem;color:#4f7d63;font-weight:600;flex:1 1 11rem;min-width:0;margin:0}',
    '.svw-coe .coe-cap{font-size:.84rem;line-height:1.5;color:#5b564e;margin:.5rem 0 0;min-height:2.8em}',
    '.svw-coe .coe-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svw-coe.is-narrow .coe-row{display:block;padding:.25rem 0 .3rem}',
    '.svw-coe.is-narrow .coe-ctl{margin-top:.15rem;justify-content:flex-end}',
    '.svw-coe.is-narrow .coe-tag{margin-right:auto}'
  ].join('\n');

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  var ASK = ' Measurements already account for |{measured} J|. Place the remaining |{rem} J| where they really end up, so the books balance.';

  function fill(tpl, map) {
    return tpl.replace(/\{(\w+)\}/g, function (m, k) {
      return (map[k] === undefined || map[k] === null) ? m : String(map[k]);
    });
  }

  window.SVWidget = {
    meta: {
      id: 'conservation-of-energy-dispersal',
      title: 'Follow the energy',
      teaches: 'Wasted energy is transferred to the thermal store of the surroundings and dispersed, never destroyed or used up; the total always balances, and efficiency is the useful share of it.'
    },
    mount: function (root, ctx) {
      var accent = (ctx && ctx.accent) ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!(ctx && ctx.reducedMotion);

      root.innerHTML = '';
      root.classList.add('svw-coe');
      if (reduced) root.classList.add('is-still');
      root.style.setProperty('--coe-accent', accent);
      root.style.setProperty('--coe-soft', /^#[0-9a-f]{6}$/i.test(accent) ? accent + '3d' : '#d9d2c6');

      var style = el('style');
      style.textContent = CSS;
      root.appendChild(style);

      /* ---- shell: header, stage, ledger + action, caption ---- */
      root.appendChild(el('p', 'coe-kick', 'Energy audit'));
      root.appendChild(el('h3', 'coe-title', 'Follow the energy'));

      var frame = el('p', 'coe-frame');
      root.appendChild(frame);

      var stage = el('div', 'coe-stage');
      var left = el('p', 'coe-left');
      var big = el('span', 'coe-big');
      var leadLab = el('span', 'coe-leadlab');
      left.appendChild(big);
      left.appendChild(leadLab);
      stage.appendChild(left);
      var bar = el('div', 'coe-bar');
      stage.appendChild(bar);
      root.appendChild(stage);

      var rowsWrap = el('div', 'coe-rows');
      root.appendChild(rowsWrap);

      var act = el('div', 'coe-act');
      var go = el('button', 'coe-go', 'Check');
      go.type = 'button';
      var streakLine = el('p', 'coe-streak');
      act.appendChild(go);
      act.appendChild(streakLine);
      root.appendChild(act);

      var cap = el('p', 'coe-cap');
      cap.setAttribute('aria-live', 'polite');
      root.appendChild(cap);

      var sr = el('p', 'coe-sr');
      sr.setAttribute('aria-live', 'polite');
      root.appendChild(sr);

      /* ---- state ---- */
      var idx = 0, streak = 0, attempted = 0, mastered = false;
      var round = null, vals = [], phase = 'placing', blown = false;
      var rowEls = [], tail = null;

      function setFrame(text) {
        frame.textContent = '';
        text.split('|').forEach(function (part, i) {
          if (!part) return;
          frame.appendChild(i % 2 ? el('b', null, part) : document.createTextNode(part));
        });
      }

      function layout() {
        var w = root.clientWidth || root.getBoundingClientRect().width || 0;
        root.classList.toggle('is-narrow', w > 0 && w < 480);
      }

      function total() {
        var t = 0;
        for (var i = 0; i < vals.length; i++) t += vals[i];
        return t;
      }

      function sumKind(kind) {
        var t = 0;
        for (var i = 0; i < vals.length; i++) {
          if (round.rows[i].kind === kind) t += vals[i];
        }
        return t;
      }

      function firstBadTrap() {
        for (var i = 0; i < vals.length; i++) {
          if (round.rows[i].kind === 'trap' && vals[i] > 0) return i;
        }
        return -1;
      }

      function buildRound() {
        round = ROUNDS[idx];
        vals = round.rows.map(function (r) { return r.fixed || 0; });
        phase = 'placing';
        blown = false;
        rowEls = [];

        var measured = round.rows.reduce(function (t, r) { return t + (r.fixed || 0); }, 0);
        setFrame(fill(round.scenario + ASK, {
          input: round.input, measured: measured, rem: round.input - measured
        }));

        bar.innerHTML = '';
        rowsWrap.innerHTML = '';

        round.rows.forEach(function (r, i) {
          var seg = el('div', 'coe-seg');
          bar.appendChild(seg);

          var row = el('div', 'coe-row' + (r.fixed ? ' is-given' : ''));
          row.appendChild(el('div', 'coe-lab', r.label));
          var ctl = el('div', 'coe-ctl');
          var tag = el('span', 'coe-tag', r.fixed ? 'measured' : '');
          ctl.appendChild(tag);
          var minus = null, plus = null;
          var val = el('span', 'coe-val' + (r.fixed ? ' is-fixed' : ''));
          if (r.fixed) {
            ctl.appendChild(val);
          } else {
            minus = el('button', 'coe-step', '−');
            minus.type = 'button';
            minus.setAttribute('aria-label', 'Take ' + round.step + ' joules out of: ' + r.label);
            plus = el('button', 'coe-step', '+');
            plus.type = 'button';
            plus.setAttribute('aria-label', 'Put ' + round.step + ' joules into: ' + r.label);
            minus.addEventListener('click', function () { nudge(i, -1); });
            plus.addEventListener('click', function () { nudge(i, 1); });
            ctl.appendChild(minus);
            ctl.appendChild(val);
            ctl.appendChild(plus);
          }
          row.appendChild(ctl);
          rowsWrap.appendChild(row);
          rowEls.push({ tag: tag, val: val, minus: minus, plus: plus, seg: seg });
        });

        tail = el('div', 'coe-tail');
        bar.appendChild(tail);

        cap.textContent = round.evidence;
        go.textContent = 'Check';
        render();
      }

      function nudge(i, dir) {
        if (phase !== 'placing') return;
        var next = vals[i] + dir * round.step;
        if (next < 0) next = 0;
        if (next > round.input) next = round.input;
        if (next === vals[i]) return;
        vals[i] = next;
        render();
      }

      function commit() {
        attempted++;
        var placed = total();
        var bad = firstBadTrap();
        var ok = (bad === -1) && (placed === round.input);
        var useful = sumKind('useful');
        var map = {
          input: round.input,
          useful: useful,
          waste: sumKind('waste'),
          placed: placed,
          diff: Math.abs(round.input - placed),
          eff: Math.round(useful * 100 / round.input),
          n: bad === -1 ? 0 : vals[bad]
        };
        /* row values are quotable in the prose, so a caption can never
           drift from what the student actually placed */
        for (var i = 0; i < vals.length; i++) map['r' + i] = vals[i];

        if (ok) {
          phase = 'done';
          if (!blown) {
            streak++;
            if (streak >= 3) mastered = true;
          }
          cap.textContent = fill(round.win, map);
          go.textContent = mastered ? 'Another anyway' : 'Next device';
        } else {
          blown = true;
          streak = 0;
          if (bad !== -1) {
            cap.textContent = fill(round.rows[bad].msg, map);
          } else if (placed < round.input) {
            cap.textContent = fill('Only {placed} J of the {input} J is accounted for. The missing {diff} J cannot leak out of the universe — every joule ends up in some store.', map);
          } else {
            cap.textContent = fill('You have placed {placed} J, but only {input} J went in. Energy cannot be created either — the books have to balance exactly.', map);
          }
        }
        render();
      }

      function nextRound() {
        idx = (idx + 1) % ROUNDS.length;
        buildRound();
      }

      function render() {
        var placed = total();
        var span = Math.max(placed, round.input);
        var done = phase === 'done';

        round.rows.forEach(function (r, i) {
          var re = rowEls[i];
          re.val.textContent = vals[i] + ' J';
          re.seg.style.width = (vals[i] * 100 / span) + '%';
          re.seg.className = 'coe-seg' + (done ? ' k-' + r.kind : '');
          if (re.minus) re.minus.disabled = done || vals[i] === 0;
          if (re.plus) re.plus.disabled = done || placed >= round.input + round.step;
          re.tag.textContent = done
            ? (r.kind === 'useful' ? 'useful' : r.kind === 'waste' ? 'wasted' : '')
            : (r.fixed ? 'measured' : '');
          re.tag.className = 'coe-tag' + (done && r.kind === 'useful' ? ' t-useful' : '');
        });

        tail.style.width = (Math.max(0, round.input - placed) * 100 / span) + '%';
        bar.classList.toggle('is-over', placed > round.input);

        var leftJ = round.input - placed;
        big.textContent = (leftJ < 0 ? '+' + (-leftJ) : leftJ) + ' J';
        leadLab.textContent = leftJ > 0 ? 'left to place'
          : leftJ < 0 ? 'more than went in'
            : done ? 'left — the books balance' : 'left — ready to check';
        var msg = big.textContent + ' ' + leadLab.textContent;

        streakLine.textContent = (mastered && done)
          ? 'Three in a row — nothing is ever destroyed.'
          : streak === 1 ? '1 right in a row.'
            : streak === 2 ? '2 right in a row — one more and you have it.'
              : '';

        sr.textContent = round.device + '. ' + msg + '. ' + cap.textContent;

        root.dataset.svState = JSON.stringify({
          device: round.id,
          input: round.input,
          placed: placed,
          remaining: leftJ,
          committed: done || blown,
          correct: done,
          efficiency: done ? Math.round(sumKind('useful') * 100 / round.input) : null,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      go.addEventListener('click', function () {
        if (phase === 'done') nextRound(); else commit();
      });

      layout();
      buildRound();
      if (typeof ResizeObserver === 'function') {
        new ResizeObserver(layout).observe(root);
      }
    }
  };
})();
