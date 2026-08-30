/* biomass-transfer-respiration
 * Allocate an animal's food intake across new biomass, respiration, egestion
 * and excretion. The account must balance, then the student commits.
 *
 * MARKING: the verdict is structural, not point-accurate. A student can infer
 * the SHAPE of the account from the lesson (about a tenth passes on; the
 * losses are respiration, egestion, excretion) plus the round's own cues
 * (fibrous food, warm-blooded flier). No lesson teaches per-animal splits, so
 * those are revealed as teaching, never marked. See verdict() below.
 *
 * Self-contained: no imports, no network, no storage outside root.
 */
(function () {
  'use strict';

  var UNITS = 20;              /* every intake is split into 20 equal units of 5% */

  /* Criterion (c): the taught figure is "about a tenth". This band is 5-15%,
     the range a student can defend from the lesson alone. Every animal's real
     passed-on value below lies inside it, so the reveal never contradicts it. */
  var PASS_MIN = 1;            /* 5%  */
  var PASS_MAX = 3;            /* 15% */

  /* Criterion (d): egestion large-vs-small must match the round's cue. Wide
     enough (15 percentage points) that only an ordinal error fails. */
  var EGES_TOL = 3;

  /* Only used to decide whether to also praise the arithmetic. Never to fail. */
  var CLOSE_TOL = 1;
  var STREAK_TARGET = 3;

  var BIN_KEYS = ['biomass', 'resp', 'eges', 'excr'];
  var BIN_WORDS = {
    biomass: 'new biomass',
    resp: 'respiration',
    eges: 'faeces',
    excr: 'urine'
  };

  /* Allocations are held in whole units, so the books balance in integers and
     the kJ figures are derived (units * step). No floats anywhere. */
  var ANIMALS = [
    {
      id: 'cow',
      step: 200,
      alloc: { biomass: 2, resp: 11, eges: 6, excr: 1 },
      scene: 'A dairy cow takes in 4000 kJ of grass — tough, fibrous, and much of it cellulose she cannot digest.',
      labels: {
        biomass: 'Passed on — growth and milk',
        resp: 'Respiration — leaves as heat',
        eges: 'Egested — faeces (undigested)',
        excr: 'Excreted — urine (urea)'
      },
      egesWhy: 'grass is full of cellulose she cannot digest, so a big share leaves undigested',
      typical: 'In a real dairy cow cellulose sends {eges} kJ out as faeces, but holding a big body at 39 °C respires away {resp} kJ — more still — and only {biomass} kJ, {bpct}%, is passed on.'
    },
    {
      id: 'owl',
      step: 50,
      alloc: { biomass: 1, resp: 16, eges: 2, excr: 1 },
      scene: 'A barn owl takes in 1000 kJ of voles, swallowed whole and almost fully digested; it hunts on the wing for hours and holds its body at 40 °C.',
      labels: {
        biomass: 'Passed on — growth',
        resp: 'Respiration — leaves as heat',
        eges: 'Egested — pellet and faeces',
        excr: 'Excreted — nitrogen waste'
      },
      egesWhy: 'vole flesh is almost fully digested — only fur and bone come back up',
      typical: 'A real barn owl loses only {eges} kJ as pellet and faeces, while flying and holding 40 °C respire away {resp} kJ; just {biomass} kJ, {bpct}%, is passed on.'
    },
    {
      id: 'hen',
      step: 100,
      alloc: { biomass: 3, resp: 13, eges: 3, excr: 1 },
      scene: 'A laying hen takes in 2000 kJ of grain — starchy and easily digested — and she is penned, so she moves very little.',
      labels: {
        biomass: 'Passed on — growth and eggs',
        resp: 'Respiration — leaves as heat',
        eges: 'Egested — faeces (undigested)',
        excr: 'Excreted — nitrogen waste'
      },
      egesWhy: 'grain is starchy and digests easily',
      typical: 'A real laying hen egests only {eges} kJ because grain digests easily and she barely moves, yet holding 41 °C still respires away {resp} kJ; {biomass} kJ, {bpct}%, is passed on.'
    },
    {
      id: 'mouse',
      step: 20,
      alloc: { biomass: 1, resp: 17, eges: 1, excr: 1 },
      scene: 'A wood mouse takes in 400 kJ of seeds and nuts — energy-dense and almost fully digested — but its body is tiny, so it loses heat fast at 37 °C.',
      labels: {
        biomass: 'Passed on — growth',
        resp: 'Respiration — leaves as heat',
        eges: 'Egested — faeces (undigested)',
        excr: 'Excreted — urine (urea)'
      },
      egesWhy: 'seeds are energy-dense and digest almost fully',
      typical: 'A real wood mouse egests just {eges} kJ, but a tiny body loses heat so fast that {resp} kJ is respired away; only {biomass} kJ, {bpct}%, is passed on.'
    },
    {
      id: 'fox',
      step: 100,
      alloc: { biomass: 2, resp: 13, eges: 3, excr: 2 },
      scene: 'A red fox takes in 2000 kJ of meat — digestible, but protein-rich, so plenty of nitrogen waste leaves in its urine; it ranges for miles each night.',
      labels: {
        biomass: 'Passed on — growth',
        resp: 'Respiration — leaves as heat',
        eges: 'Egested — faeces (undigested)',
        excr: 'Excreted — urine (urea)'
      },
      egesWhy: 'meat digests well',
      typical: 'A real red fox egests only {eges} kJ, though protein leaves {excr} kJ of nitrogen waste in urine, while ranging and holding 38 °C respire away {resp} kJ; {biomass} kJ, {bpct}%, is passed on.'
    }
  ];

  var CSS = [
    '.svw-btr{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45;-webkit-text-size-adjust:100%;}',
    '.svw-btr *{box-sizing:border-box;}',
    '.svw-btr .btr-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--btr-accent);margin:0 0 .2rem;}',
    '.svw-btr .btr-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.2;margin:0 0 .4rem;}',
    '.svw-btr .btr-frame{font-size:.86rem;line-height:1.5;color:#3a352e;margin:0 0 .7rem;}',
    '.svw-btr .btr-ask{font-weight:600;color:#2d2a26;}',
    '.svw-btr .btr-meter{display:flex;justify-content:space-between;align-items:baseline;gap:.7rem;font-size:.72rem;font-weight:600;color:#5b564e;font-variant-numeric:tabular-nums;margin:0 0 .4rem;}',
    '.svw-btr .btr-left{color:#2d2a26;}',
    '.svw-btr .btr-key{text-align:right;white-space:nowrap;}',
    '.svw-btr:not(.is-done) .btr-key{padding-right:32px;}',
    '.svw-btr .btr-rows{display:flex;flex-direction:column;gap:.5rem;margin:0 0 .7rem;}',
    '.svw-btr .btr-head{display:flex;align-items:center;gap:.4rem;}',
    '.svw-btr .btr-lab{flex:1 1 auto;font-size:.76rem;font-weight:600;min-width:0;}',
    '.svw-btr .btr-step{flex:0 0 auto;display:flex;align-items:center;gap:.18rem;}',
    '.svw-btr .btr-pm{width:28px;height:28px;padding:0;border:1px solid #ddd7cd;background:#faf8f5;border-radius:8px;color:#2d2a26;font:600 1rem/1 Inter,system-ui,sans-serif;cursor:pointer;}',
    '.svw-btr .btr-pm:hover{background:#f2ece2;}',
    '.svw-btr .btr-pm[disabled]{opacity:.38;cursor:default;}',
    '.svw-btr .btr-val{min-width:44px;text-align:right;font-size:.82rem;font-weight:700;font-variant-numeric:tabular-nums;}',
    '.svw-btr .btr-res{display:none;font-size:.76rem;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;color:#5b564e;}',
    '.svw-btr .btr-res b{font-weight:700;color:#2d2a26;}',
    '.svw-btr.is-done .btr-step{display:none;}',
    '.svw-btr.is-done .btr-res{display:block;}',
    '.svw-btr .btr-track{position:relative;height:11px;margin-top:.3rem;background:#f2ece3;border:1px solid #e8e2d9;border-radius:6px;overflow:hidden;}',
    '.svw-btr .btr-fill{position:absolute;top:0;bottom:0;left:0;width:0;background:var(--btr-accent);opacity:.5;}',
    '.svw-btr .btr-mark{position:absolute;top:0;bottom:0;width:2px;background:#2d2a26;left:0;display:none;box-shadow:0 0 0 1px rgba(255,255,255,.85);}',
    '.svw-btr.is-done .btr-mark{display:block;}',
    '.svw-btr .btr-act{display:flex;align-items:center;gap:.7rem;margin:0 0 .6rem;}',
    '.svw-btr .btr-run{flex:1 1 auto;font-size:.74rem;line-height:1.35;color:#5b564e;min-width:0;}',
    '.svw-btr .btr-go{flex:0 0 auto;padding:.5rem .95rem;border:1px solid #2d2a26;border-radius:10px;background:#2d2a26;color:#fff;font:600 .82rem/1.2 Inter,system-ui,sans-serif;cursor:pointer;}',
    '.svw-btr .btr-go.is-quiet{background:#faf8f5;color:#2d2a26;border-color:#ddd7cd;}',
    '.svw-btr .btr-cap{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.6rem .7rem;font-size:.84rem;line-height:1.5;min-height:4.2rem;}',
    '.svw-btr .btr-v-ok{font-weight:700;color:#4f7d63;}',
    '.svw-btr .btr-v-no{font-weight:700;color:#2d2a26;}',
    '.svw-btr .btr-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0;}',
    '.svw-btr button:focus-visible{outline:2px solid var(--btr-accent);outline-offset:2px;}'
  ].join('');

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  window.SVWidget = {
    meta: {
      id: 'biomass-transfer-respiration',
      title: 'Where the food goes',
      teaches: 'Respiration, not undigested material, is the biggest loss of biomass between trophic levels; only about a tenth is passed on.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || '#7a6a52';
      try {
        var cs = getComputedStyle(root).getPropertyValue('--accent');
        if (cs && cs.trim()) accent = cs.trim();
      } catch (e) { /* ignore */ }
      var reduced = !!ctx.reducedMotion;

      var style = document.createElement('style');
      style.textContent = CSS + (reduced ? '' : '.svw-btr .btr-fill{transition:width .18s ease;}');
      root.appendChild(style);

      var wrap = el('div', 'svw-btr');
      wrap.style.setProperty('--btr-accent', accent);
      root.appendChild(wrap);

      wrap.appendChild(el('p', 'btr-kick', 'Biomass transfer'));
      wrap.appendChild(el('h3', 'btr-title', 'Where the food goes'));
      var frameEl = el('p', 'btr-frame');
      var sceneEl = el('span');
      var askEl = el('span', 'btr-ask', ' Which loss is biggest, and roughly how much is passed on?');
      frameEl.appendChild(sceneEl);
      frameEl.appendChild(askEl);
      wrap.appendChild(frameEl);

      var meter = el('div', 'btr-meter');
      var leftEl = el('span', 'btr-left', '');
      var keyEl = el('span', 'btr-key', '');
      meter.appendChild(leftEl);
      meter.appendChild(keyEl);
      wrap.appendChild(meter);

      var rowsEl = el('div', 'btr-rows');
      wrap.appendChild(rowsEl);

      var rows = {};
      BIN_KEYS.forEach(function (key) {
        var row = el('div', 'btr-row');
        var head = el('div', 'btr-head');
        var lab = el('span', 'btr-lab', '');
        var step = el('span', 'btr-step');
        var minus = el('button', 'btr-pm', '−');
        var val = el('span', 'btr-val', '0');
        var plus = el('button', 'btr-pm', '+');
        var res = el('span', 'btr-res', '');
        minus.type = 'button';
        plus.type = 'button';
        step.appendChild(minus);
        step.appendChild(val);
        step.appendChild(plus);
        head.appendChild(lab);
        head.appendChild(step);
        head.appendChild(res);
        var track = el('div', 'btr-track');
        var fillBar = el('div', 'btr-fill');
        var mark = el('div', 'btr-mark');
        track.appendChild(fillBar);
        track.appendChild(mark);
        row.appendChild(head);
        row.appendChild(track);
        rowsEl.appendChild(row);
        rows[key] = { lab: lab, val: val, res: res, fill: fillBar, mark: mark, minus: minus, plus: plus };
        minus.addEventListener('click', function () { nudgeBin(key, -1); });
        plus.addEventListener('click', function () { nudgeBin(key, 1); });
      });

      var act = el('div', 'btr-act');
      var runEl = el('p', 'btr-run', '');
      var goBtn = el('button', 'btr-go', 'Check the account');
      goBtn.type = 'button';
      act.appendChild(runEl);
      act.appendChild(goBtn);
      wrap.appendChild(act);

      var capEl = el('div', 'btr-cap');
      wrap.appendChild(capEl);

      var srEl = el('p', 'btr-sr');
      srEl.setAttribute('aria-live', 'polite');
      wrap.appendChild(srEl);

      /* ---------- state ---------- */
      var order = ANIMALS.slice();
      for (var i = order.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = order[i]; order[i] = order[j]; order[j] = tmp;
      }
      var idx = 0;
      var animal = order[0];
      var given = { biomass: 0, resp: 0, eges: 0, excr: 0 };
      var committed = false;
      var streak = 0, attempted = 0, mastered = false;

      function intake() { return animal.step * UNITS; }
      function kj(u) { return u * animal.step; }
      function pct(u) { return Math.round(u * 100 / UNITS); }
      function placed() {
        return given.biomass + given.resp + given.eges + given.excr;
      }
      function fill(str) {
        var a = animal.alloc;
        return str
          .replace('{biomass}', String(kj(a.biomass)))
          .replace('{resp}', String(kj(a.resp)))
          .replace('{eges}', String(kj(a.eges)))
          .replace('{excr}', String(kj(a.excr)))
          .replace('{bpct}', String(pct(a.biomass)));
      }

      /* The bin that is really the largest, read off the round's own data —
         never assumed to be respiration. */
      function trueLargest() {
        var best = BIN_KEYS[0];
        BIN_KEYS.forEach(function (k) {
          if (animal.alloc[k] > animal.alloc[best]) best = k;
        });
        return best;
      }

      /* Structural marking. Criterion (a), the balance, is enforced before
         commit, so it is always true here. */
      function verdict() {
        var big = trueLargest();
        var largestOk = BIN_KEYS.every(function (k) {
          return k === big || given[big] > given[k];
        });
        var passedOnOk = given.biomass >= PASS_MIN && given.biomass <= PASS_MAX;
        var egestionOk = Math.abs(given.eges - animal.alloc.eges) <= EGES_TOL;
        var close = BIN_KEYS.every(function (k) {
          return Math.abs(given[k] - animal.alloc[k]) <= CLOSE_TOL;
        });
        return {
          big: big,
          largestOk: largestOk,
          passedOnOk: passedOnOk,
          egestionOk: egestionOk,
          close: close,
          right: largestOk && passedOnOk && egestionOk
        };
      }

      function pushState() {
        var v = committed ? verdict() : null;
        root.dataset.svState = JSON.stringify({
          streak: streak,
          mastered: mastered,
          attempted: attempted,
          animal: animal.id,
          placed: placed(),
          balanced: placed() === UNITS,
          committed: committed,
          correct: v ? v.right : null,
          shape: v ? { largestOk: v.largestOk, passedOnOk: v.passedOnOk, egestionOk: v.egestionOk } : null
        });
      }

      function nudgeBin(key, dir) {
        if (committed) return;
        var next = given[key] + dir;
        if (next < 0) next = 0;
        if (next > UNITS - (placed() - given[key])) next = UNITS - (placed() - given[key]);
        if (next === given[key]) return;
        given[key] = next;
        paint();
        srEl.textContent = animal.labels[key] + ': ' + kj(given[key]) + ' kilojoules. ' +
          (UNITS - placed()) * animal.step + ' kilojoules still to place.';
      }

      function paint() {
        var left = (UNITS - placed()) * animal.step;
        leftEl.textContent = committed
          ? 'Intake ' + intake() + ' kJ'
          : (left === 0
            ? 'Balanced — all ' + intake() + ' kJ placed'
            : 'Still to place: ' + left + ' kJ');
        keyEl.textContent = committed ? 'yours → typical (kJ)' : 'kJ';
        BIN_KEYS.forEach(function (k) {
          var r = rows[k];
          r.lab.textContent = animal.labels[k];
          r.val.textContent = String(kj(given[k]));
          r.fill.style.width = (given[k] * 100 / UNITS) + '%';
          r.minus.disabled = committed || given[k] === 0;
          r.plus.disabled = committed || placed() === UNITS;
          r.minus.setAttribute('aria-label', 'Less ' + BIN_WORDS[k]);
          r.plus.setAttribute('aria-label', 'More ' + BIN_WORDS[k]);
          if (committed) {
            r.res.innerHTML = '';
            r.res.appendChild(document.createTextNode(kj(given[k]) + ' → '));
            var b = document.createElement('b');
            b.textContent = String(kj(animal.alloc[k]));
            r.res.appendChild(b);
            r.mark.style.left = 'calc(' + (animal.alloc[k] * 100 / UNITS) + '% - 1px)';
          }
        });
        pushState();
      }

      function runLine() {
        if (mastered) {
          runEl.textContent = 'You have it — keep going if you like.';
        } else if (streak === 0) {
          runEl.textContent = '';
        } else if (streak === STREAK_TARGET - 1) {
          runEl.textContent = streak + ' right in a row — one more and you have it.';
        } else {
          runEl.textContent = streak + ' right — two more in a row and you have it.';
        }
      }

      /* Wrong-answer diagnosis, keyed to the criterion that failed. */
      function diagnose(v) {
        var a = animal.alloc;
        if (!v.largestOk && given.eges >= given[v.big]) {
          return 'you made ' + (animal.id === 'owl' ? 'the pellet and faeces' : 'faeces') +
            ' the biggest loss (' + kj(given.eges) + ' kJ), with respiration at ' + kj(given.resp) +
            ' kJ. It is the other way round. Faeces are food that was eaten but never digested; ' +
            'respiration is food burnt to move, digest and stay warm, and it leaves the body as heat for good.';
        }
        if (!v.largestOk) {
          return 'your biggest figure is ' + BIN_WORDS[largestGiven()] + ' at ' + kj(given[largestGiven()]) +
            ' kJ. ' + BIN_WORDS[v.big].charAt(0).toUpperCase() + BIN_WORDS[v.big].slice(1) +
            ' should be the biggest here: an animal burns food all day to move, digest and stay warm, and all of that leaves as heat.';
        }
        if (!v.passedOnOk && given.biomass > PASS_MAX) {
          return 'you passed on ' + kj(given.biomass) + ' kJ, ' + pct(given.biomass) +
            '% of the intake. Only about a tenth of what an animal eats becomes new biomass — that is why a food chain runs out of energy after four or five levels.';
        }
        if (!v.passedOnOk) {
          return 'you passed on only ' + kj(given.biomass) + ' kJ, ' + pct(given.biomass) +
            '%. About a tenth does get through, and that tenth is the whole reason the next trophic level can exist.';
        }
        if (given.eges > a.eges) {
          return 'you sent ' + kj(given.eges) + ' kJ, ' + pct(given.eges) +
            '%, out as faeces — too much here, because ' + animal.egesWhy +
            '. Respiration, not undigested food, is where most of it goes.';
        }
        return 'you sent only ' + kj(given.eges) + ' kJ, ' + pct(given.eges) +
          '%, out as faeces — too little here, because ' + animal.egesWhy +
          '. Egestion is a real loss, just never the biggest one.';
      }

      function largestGiven() {
        var best = BIN_KEYS[0];
        BIN_KEYS.forEach(function (k) { if (given[k] > given[best]) best = k; });
        return best;
      }

      function say(html) { capEl.innerHTML = html; }

      function commit() {
        if (committed) { nextRound(); return; }
        if (placed() !== UNITS) {
          say('You have <b>' + (UNITS - placed()) * animal.step +
            ' kJ</b> still to place. Every kilojoule taken in has to end up somewhere, so the account must balance before it can be checked.');
          srEl.textContent = capEl.textContent;
          return;
        }
        committed = true;
        attempted += 1;
        var v = verdict();
        if (v.right) {
          streak += 1;
          if (streak >= STREAK_TARGET) mastered = true;
        } else {
          streak = 0;
        }
        paint();

        var text;
        if (v.right && mastered && streak === STREAK_TARGET) {
          text = '<span class="btr-v-ok">Right — three in a row, and you have it.</span> ' +
            BIN_WORDS[v.big].charAt(0).toUpperCase() + BIN_WORDS[v.big].slice(1) +
            ' is the biggest loss at every level: food burnt to move, digest and stay warm, leaving as heat. ' +
            'Egestion and excretion take less, and only about a tenth is passed on.';
        } else if (v.right && v.close) {
          text = '<span class="btr-v-ok">Right —</span> ' + BIN_WORDS[v.big] + ' biggest at ' +
            kj(given[v.big]) + ' kJ, and ' + kj(given.biomass) + ' kJ passed on — ' + pct(given.biomass) +
            '%, about a tenth. Your figures are close to the measured ones too. ' + fill(animal.typical);
        } else if (v.right) {
          text = '<span class="btr-v-ok">Right — you had the shape of it:</span> ' + BIN_WORDS[v.big] +
            ' biggest at ' + kj(given[v.big]) + ' kJ, and ' + kj(given.biomass) + ' kJ passed on — ' +
            pct(given.biomass) + '%, about a tenth. ' + fill(animal.typical);
        } else {
          text = '<span class="btr-v-no">Not quite —</span> ' + diagnose(v);
        }
        say(text);
        srEl.textContent = capEl.textContent;
        goBtn.textContent = mastered ? 'Another anyway' : 'Next animal';
        goBtn.classList.add('is-quiet');
        wrap.classList.add('is-done');
        runLine();
        pushState();
      }

      function nextRound() {
        idx = (idx + 1) % order.length;
        animal = order[idx];
        given = { biomass: 0, resp: 0, eges: 0, excr: 0 };
        committed = false;
        wrap.classList.remove('is-done');
        goBtn.textContent = 'Check the account';
        goBtn.classList.remove('is-quiet');
        sceneEl.textContent = animal.scene;
        say('Nothing vanishes: every one of those ' + intake() +
          ' kJ is built into new biomass, burnt in respiration, egested or excreted.');
        runLine();
        paint();
        srEl.textContent = animal.scene + askEl.textContent;
      }

      goBtn.addEventListener('click', commit);

      sceneEl.textContent = animal.scene;
      say('Nothing vanishes: every one of those ' + intake() +
        ' kJ is built into new biomass, burnt in respiration, egested or excreted.');
      runLine();
      paint();
    }
  };
})();
