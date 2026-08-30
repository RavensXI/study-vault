/* Which starch reaction? — gelatinisation vs dextrinisation.
   Self-contained lesson widget. No imports, no network, no storage. */
(function () {
  'use strict';

  var GEL = 'gel', DEX = 'dex', NONE = 'none', BOTH = 'both', CARAM = 'caram';

  var NAME = {
    gel: 'gelatinisation',
    dex: 'dextrinisation',
    none: 'no reaction yet',
    both: 'both reactions',
    caram: 'caramelisation'
  };

  /* Every round: a real kitchen scenario, one defensible answer, and a
     diagnosis for each wrong route that says what separates it from the
     right one. Answers vary round to round (gel, dex, dex, gel, none,
     gel, both) so nothing can be re-typed from memory. */
  var ROUNDS = [
    {
      id: 'white-sauce',
      material: 'flour',
      scenario: 'Plain flour is whisked into cold milk. The pan goes on the hob and is stirred up to the boil.',
      answer: GEL,
      right: 'The granules soak up milk, swell from about 60 °C and burst near 80 °C, releasing amylose that traps the liquid. Fully thick by 93–100 °C.',
      options: [
        { kind: GEL, label: 'Gelatinisation — the sauce thickens' },
        { kind: DEX, label: 'Dextrinisation — the flour browns',
          why: 'Dextrinisation needs dry heat. Here every grain is wrapped in milk, so the granules drink it in and swell — the sauce thickens and nothing browns.' },
        { kind: NONE, label: 'Nothing yet — it thickens as it cools',
          why: 'Thickening happens on the way up, not down: granules swell from about 60 °C and burst near 80 °C. Cooling only sets a sauce that is already thick.' },
        { kind: BOTH, label: 'Both — it browns while it thickens',
          why: 'Nothing browns while it is wet. In liquid the surface is held at 100 °C, and splitting starch into dextrins takes roughly 150 °C of dry heat.' }
      ]
    },
    {
      id: 'toast',
      material: 'bread',
      scenario: 'A slice of bread sits under a hot, dry grill. The surface turns golden, then darker.',
      answer: DEX,
      right: 'Dry heat above about 150 °C breaks the surface starch into dextrins — golden, crisp and slightly sweet. No water, so nothing thickens.',
      options: [
        { kind: DEX, label: 'Dextrinisation — the surface browns' },
        { kind: GEL, label: 'Gelatinisation — the starch swells',
          why: 'Swelling needs liquid for the granules to absorb. Under a dry grill there is none, so the heat splits the surface starch instead of softening it.' },
        { kind: CARAM, label: 'Caramelisation — the sugars brown',
          why: 'Caramelisation is a sugar reaction: sugar has to melt at about 160 °C. The surface of bread is mostly starch, and dry heat breaks it down into dextrins.' },
        { kind: NONE, label: 'Nothing — the bread is only drying out',
          why: 'Drying alone leaves bread pale and hard. The gold is new chemistry — starch broken into dextrins, which is also why toast tastes slightly sweet.' }
      ]
    },
    {
      id: 'roux',
      material: 'flour',
      scenario: 'Flour is cooked in melted butter for two minutes until it is sandy and smells nutty. No liquid has gone in yet.',
      answer: DEX,
      right: 'Hot fat carries heat but gives the granules nothing to absorb, so the starch browns instead. The thickening waits for the milk.',
      options: [
        { kind: DEX, label: 'Dextrinisation — the flour browns' },
        { kind: GEL, label: 'Gelatinisation — the butter thickens it',
          why: 'Fat is not water. Granules can only swell by taking up liquid, and butter offers none, so nothing thickens until the milk goes in.' },
        { kind: BOTH, label: 'Both — it browns and thickens together',
          why: 'There is no liquid in the pan to thicken. In a roux the two run in order: browning dry first, thickening once the milk arrives.' },
        { kind: NONE, label: 'Nothing — fat cannot change starch',
          why: 'Something has changed — you can smell it. Dry heat is breaking the starch into dextrins, which is what gives a brown roux its nutty taste.' }
      ]
    },
    {
      id: 'custard',
      material: 'cornflour',
      scenario: 'Cornflour is blended with cold milk, stirred into a pan of hot milk and held just below boiling for a minute.',
      answer: GEL,
      right: 'The granules swell from about 60 °C and burst, and the amylose released tangles into a mesh. The custard is fully thick at 93–100 °C.',
      options: [
        { kind: GEL, label: 'Gelatinisation — it thickens to custard' },
        { kind: DEX, label: 'Dextrinisation — the cornflour browns',
          why: 'The cornflour is suspended in milk, not exposed to dry heat, so it cannot brown. Liquid plus heat is the recipe for swelling and bursting.' },
        { kind: NONE, label: 'Nothing — starch needs 160 °C to work',
          why: 'Starch starts swelling at about 60 °C and is fully thick near boiling. 160 °C is where sugar caramelises, not where starch thickens.' },
        { kind: BOTH, label: 'Both — the top browns as it thickens',
          why: 'A wet surface is pinned at boiling point, far below browning heat. Skin on custard is protein and evaporation, not dextrinisation.' }
      ]
    },
    {
      id: 'cold-slurry',
      material: 'cornflour',
      scenario: 'Cornflour is stirred into a jug of cold water and left standing on the worktop for ten minutes.',
      answer: NONE,
      right: 'Gelatinisation needs water AND heat. Cold water alone leaves the granules packed and insoluble, so they simply sink to the bottom of the jug.',
      options: [
        { kind: NONE, label: 'Nothing yet — it stays thin and settles' },
        { kind: GEL, label: 'Gelatinisation — water is present',
          why: 'Water is only half the condition. Below about 60 °C the granules stay packed and insoluble — they sink rather than swell. Heat is what opens them.' },
        { kind: GEL, label: 'Gelatinisation — slowly, given time',
          why: 'Time does not stand in for temperature. The granules need about 60 °C before they take up water; on a cold worktop they will still be settling tomorrow.' },
        { kind: DEX, label: 'Dextrinisation — the starch dries out',
          why: 'Dextrinisation needs dry heat of roughly 150 °C. This jug is wet and cold, so there is no route to browning at all.' }
      ]
    },
    {
      id: 'lumpy',
      material: 'flour',
      scenario: 'Flour is tipped straight into a pan of hot milk. The sauce goes lumpy.',
      answer: GEL,
      right: 'It happened, but too fast: the outside of each clump gelatinised instantly and sealed dry flour inside. That is why flour is blended with cold liquid first.',
      options: [
        { kind: GEL, label: 'Gelatinisation — but only on the lumps' },
        { kind: NONE, label: 'Nothing — the sauce failed, so no reaction',
          why: 'A failure is still chemistry. The starch on the outside of each clump gelatinised at once, which is exactly what sealed the dry flour inside.' },
        { kind: DEX, label: 'Dextrinisation — dry flour browned',
          why: 'The flour met hot milk, not dry heat, and the sauce never browned. The lumps are starch that gelatinised on the outside and stayed dry within.' },
        { kind: BOTH, label: 'Both — browned lumps in a thick sauce',
          why: 'Nothing browned: the pan is wet throughout and capped at 100 °C. The lumps are pale — gelatinised skin over dry flour.' }
      ]
    },
    {
      id: 'pie',
      material: 'pie',
      scenario: 'A fruit pie thickened with cornflour bakes in a hot oven. The filling bubbles and the pastry lid turns golden.',
      answer: BOTH,
      right: 'One oven, two conditions: the wet filling gelatinises and thickens, while the dry pastry surface dextrinises and browns.',
      options: [
        { kind: BOTH, label: 'Both — filling thickens, crust browns' },
        { kind: GEL, label: 'Gelatinisation — one oven, one reaction',
          why: 'The reaction follows the conditions, not the appliance. The filling is wet so it thickens; the pastry surface is dry, so it browns instead.' },
        { kind: DEX, label: 'Dextrinisation — the oven is dry heat',
          why: 'The oven is dry, but the filling is not: sealed under a lid it is wet and capped near 100 °C, so it gelatinises while the crust browns.' },
        { kind: NONE, label: 'Nothing — baking is too dry to thicken',
          why: 'The filling carries its own liquid, and that is all the granules need. Dry oven air only reaches the crust.' }
      ]
    }
  ];

  var STAGE_LABEL = {
    gel: 'Water in — granules swell, burst, trap the liquid.',
    dex: 'No water — dry heat splits surface starch into dextrins.',
    none: 'Water, no heat — granules stay packed and sink.',
    both: 'Wet filling gelatinises; dry crust dextrinises.'
  };

  var RULE = 'Ask “is there water?” first — water plus heat swells and bursts the granules and thickens; dry heat splits surface starch into dextrins and browns it.';

  var CSS = [
    '.svw-gvd{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45}',
    '.svw-gvd *{box-sizing:border-box}',
    '.svw-gvd .gvd-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .15rem}',
    '.svw-gvd .gvd-title{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.2;margin:0 0 .5rem}',
    '.svw-gvd .gvd-frame{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.5rem .65rem;margin:0 0 .45rem}',
    '.svw-gvd .gvd-scen{font-size:.88rem;font-weight:600;margin:0}',
    '.svw-gvd .gvd-ask{font-size:.79rem;color:#8d8880;margin:.25rem 0 0}',
    '.svw-gvd .gvd-svg{display:block;width:100%;height:84px}',
    '.svw-gvd .gvd-slab{font-size:.78rem;color:#5b564e;margin:.15rem 0 .5rem;min-height:1.15rem}',
    '.svw-gvd .gvd-opts{display:grid;gap:.3rem;margin:0 0 .5rem}',
    '.svw-gvd .gvd-opt{width:100%;text-align:left;font-family:inherit;font-size:.82rem;font-weight:600;line-height:1.25;padding:.45rem .65rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;cursor:pointer}',
    '.svw-gvd .gvd-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-gvd .gvd-opt.gvd-true{border-color:#4f7d63;color:#4f7d63;background:#fff}',
    '.svw-gvd .gvd-opt.gvd-true[aria-pressed="true"]{background:#4f7d63;border-color:#4f7d63;color:#fff}',
    '.svw-gvd .gvd-opt:disabled{cursor:default;opacity:1}',
    '.svw-gvd .gvd-row{display:flex;align-items:center;justify-content:space-between;gap:.6rem}',
    '.svw-gvd .gvd-run{font-size:.78rem;color:#8d8880;margin:0}',
    '.svw-gvd .gvd-go{font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer;white-space:nowrap}',
    '.svw-gvd .gvd-go:disabled{background:#faf8f5;color:#b3ada3;border-color:#e0d9cd;cursor:default}',
    '.svw-gvd .gvd-cap{font-size:.84rem;line-height:1.48;margin:.5rem 0 0;min-height:4.5em}',
    '.svw-gvd .gvd-yes{color:#4f7d63;font-weight:700}',
    '.svw-gvd .gvd-no{color:#2d2a26;font-weight:700}',
    '.svw-gvd .gvd-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}'
  ].join('');

  var SVG = [
    '<svg class="gvd-svg" viewBox="0 0 320 92" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">',
    '<rect x="8" y="14" width="304" height="64" rx="12" fill="#ffffff" stroke="#e0d9cd"/>',

    /* idle: packed, unchanged granules */
    '<g class="gvd-g" data-g="idle">',
    '<circle cx="115" cy="46" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="133" cy="46" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="151" cy="46" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="169" cy="46" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="187" cy="46" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="205" cy="46" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '</g>',

    /* gelatinisation: liquid, swollen granules, one burst releasing amylose */
    '<g class="gvd-g" data-g="gel">',
    '<rect class="gvd-liq" x="9" y="15" width="302" height="62" rx="11"/>',
    '<circle cx="42" cy="46" r="8.5" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="59" cy="46" r="8.5" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="76" cy="46" r="8.5" fill="#ece6dc" stroke="#d5cec2"/>',
    '<path class="gvd-step" d="M100 39l8 7-8 7" fill="none"/>',
    '<circle class="gvd-swell" cx="141" cy="46" r="15"/>',
    '<circle class="gvd-swell" cx="175" cy="46" r="15"/>',
    '<path class="gvd-step" d="M205 39l8 7-8 7" fill="none"/>',
    '<circle class="gvd-burst" cx="260" cy="46" r="17" fill="none" stroke-dasharray="5 4"/>',
    '<path class="gvd-amyl" d="M234 33q13-8 26-1t26-5" fill="none"/>',
    '<path class="gvd-amyl" d="M232 59q14 9 28 1t26 5" fill="none"/>',
    '<circle class="gvd-drop" cx="112" cy="24" r="2.4"/>',
    '<circle class="gvd-drop" cx="198" cy="69" r="2.4"/>',
    '<circle class="gvd-drop" cx="296" cy="26" r="2.4"/>',
    '</g>',

    /* dextrinisation: dry heat on top, browned surface, chains breaking off */
    '<g class="gvd-g" data-g="dex">',
    '<path d="M104 2l6 7 6-7" fill="none" stroke="#b07a3f" stroke-width="1.6"/>',
    '<path d="M154 2l6 7 6-7" fill="none" stroke="#b07a3f" stroke-width="1.6"/>',
    '<path d="M204 2l6 7 6-7" fill="none" stroke="#b07a3f" stroke-width="1.6"/>',
    '<rect x="9" y="15" width="302" height="18" rx="10" fill="#b07a3f" fill-opacity=".45"/>',
    '<rect x="9" y="26" width="302" height="7" fill="#b07a3f" fill-opacity=".45"/>',
    '<path d="M112 21l9-5M142 22l9-5M172 21l9-5M202 22l9-5" stroke="#8a5f2f" stroke-width="1.6"/>',
    '<path d="M128 41l7-4M158 42l7-4M188 41l7-4" stroke="#b07a3f" stroke-width="1.6"/>',
    '<circle cx="115" cy="56" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="133" cy="56" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="151" cy="56" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="169" cy="56" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="187" cy="56" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="205" cy="56" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '</g>',

    /* no reaction: cold liquid, granules packed and settled on the bottom */
    '<g class="gvd-g" data-g="none">',
    '<rect class="gvd-liq" x="9" y="15" width="302" height="62" rx="11"/>',
    '<circle cx="115" cy="66" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="133" cy="66" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="151" cy="66" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="169" cy="66" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="187" cy="66" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="205" cy="66" r="9" fill="#ece6dc" stroke="#d5cec2"/>',
    '</g>',

    /* both: one dish, two conditions */
    '<g class="gvd-g" data-g="both">',
    '<rect class="gvd-liq" x="10" y="16" width="146" height="60" rx="10"/>',
    '<circle class="gvd-swell" cx="58" cy="48" r="14"/>',
    '<circle class="gvd-swell" cx="110" cy="48" r="14"/>',
    '<rect x="164" y="16" width="148" height="18" rx="9" fill="#b07a3f" fill-opacity=".45"/>',
    '<rect x="164" y="27" width="148" height="7" fill="#b07a3f" fill-opacity=".45"/>',
    '<circle cx="196" cy="58" r="8" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="212" cy="58" r="8" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="228" cy="58" r="8" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="244" cy="58" r="8" fill="#ece6dc" stroke="#d5cec2"/>',
    '<circle cx="260" cy="58" r="8" fill="#ece6dc" stroke="#d5cec2"/>',
    '<path d="M160 14v64" stroke="#e0d9cd" stroke-dasharray="3 4"/>',
    '<text x="83" y="88" font-size="11" text-anchor="middle" fill="#8d8880" font-family="Inter,system-ui,sans-serif">filling</text>',
    '<text x="238" y="88" font-size="11" text-anchor="middle" fill="#8d8880" font-family="Inter,system-ui,sans-serif">crust</text>',
    '</g>',
    '</svg>'
  ].join('');

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i];
      a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  window.SVWidget = {
    meta: {
      id: 'gelatinisation-vs-dextrinisation',
      title: 'Which starch reaction?',
      teaches: 'Gelatinisation needs water and heat and thickens a liquid; dextrinisation is dry heat and browns a surface.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
                   ctx.accent || '#8a6a4f';

      root.classList.add('svw-gvd');
      root.innerHTML =
        '<style>' + CSS + '</style>' +
        '<p class="gvd-kick">Food science</p>' +
        '<h3 class="gvd-title">Which starch reaction?</h3>' +
        '<div class="gvd-frame">' +
          '<p class="gvd-scen"></p>' +
          '<p class="gvd-ask">Predict which starch reaction takes place, and what you would see.</p>' +
        '</div>' +
        SVG +
        '<p class="gvd-slab"></p>' +
        '<div class="gvd-opts" role="group" aria-label="Your prediction"></div>' +
        '<div class="gvd-row"><p class="gvd-run"></p>' +
          '<button type="button" class="gvd-go">Check</button></div>' +
        '<p class="gvd-cap"></p>' +
        '<p class="gvd-sr" aria-live="polite"></p>';

      var q = function (s) { return root.querySelector(s); };
      var scenEl = q('.gvd-scen'), slabEl = q('.gvd-slab'), optsEl = q('.gvd-opts'),
          runEl = q('.gvd-run'), goEl = q('.gvd-go'), capEl = q('.gvd-cap'), srEl = q('.gvd-sr');

      /* accent-tinted parts of the diagram, set once */
      var i, els;
      els = root.querySelectorAll('.gvd-liq');
      for (i = 0; i < els.length; i++) els[i].setAttribute('fill', accent + '29');
      els = root.querySelectorAll('.gvd-swell');
      for (i = 0; i < els.length; i++) {
        els[i].setAttribute('fill', accent + '33');
        els[i].setAttribute('stroke', accent + '99');
      }
      els = root.querySelectorAll('.gvd-burst');
      for (i = 0; i < els.length; i++) {
        els[i].setAttribute('stroke', accent);
        els[i].setAttribute('stroke-width', '1.9');
      }
      els = root.querySelectorAll('.gvd-amyl');
      for (i = 0; i < els.length; i++) {
        els[i].setAttribute('stroke', accent);
        els[i].setAttribute('stroke-width', '1.7');
      }
      els = root.querySelectorAll('.gvd-step');
      for (i = 0; i < els.length; i++) {
        els[i].setAttribute('stroke', accent + '99');
        els[i].setAttribute('stroke-width', '1.8');
      }
      els = root.querySelectorAll('.gvd-drop');
      for (i = 0; i < els.length; i++) els[i].setAttribute('fill', accent + '66');
      q('.gvd-kick').style.color = accent;

      var groups = {};
      els = root.querySelectorAll('.gvd-g');
      for (i = 0; i < els.length; i++) groups[els[i].getAttribute('data-g')] = els[i];

      /* four option buttons, built once and re-labelled each round */
      var optBtns = [];
      for (i = 0; i < 4; i++) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'gvd-opt';
        b.setAttribute('aria-pressed', 'false');
        b.dataset.slot = String(i);
        b.addEventListener('click', onPick);
        optsEl.appendChild(b);
        optBtns.push(b);
      }
      goEl.addEventListener('click', onGo);

      var order = [0].concat(shuffle(ROUNDS.slice(1).map(function (r, k) { return k + 1; })));
      var pos = 0, round = null, layout = [], picked = -1, committed = false,
          streak = 0, attempted = 0, mastered = false, lastCorrect = null;

      function showStage(key) {
        for (var k in groups) if (groups.hasOwnProperty(k)) {
          groups[k].style.display = (k === key) ? '' : 'none';
        }
      }

      function state() {
        root.dataset.svState = JSON.stringify({
          round: round.id,
          picked: picked < 0 ? null : layout[picked].kind,
          correct: lastCorrect,
          streak: streak,
          attempted: attempted,
          mastered: mastered
        });
      }

      function runLine() {
        if (committed || streak === 0) { runEl.textContent = streak >= 3 ? '3 in a row — you have it.' : ''; return; }
        runEl.textContent = streak === 1
          ? '1 in a row — two more and you have it.'
          : '2 in a row — one more and you have it.';
      }

      function newRound() {
        round = ROUNDS[order[pos % order.length]];
        pos++;
        layout = shuffle(round.options.slice());
        for (var k = 0; k < optBtns.length; k++) {
          optBtns[k].textContent = layout[k].label;
          optBtns[k].setAttribute('aria-pressed', 'false');
          optBtns[k].classList.remove('gvd-true');
          optBtns[k].disabled = false;
        }
        scenEl.textContent = round.scenario;
        slabEl.textContent = 'Starch granules in the ' + round.material + '.';
        showStage('idle');
        capEl.textContent = '';
        picked = -1;
        committed = false;
        lastCorrect = null;
        goEl.textContent = 'Check';
        goEl.disabled = true;
        runLine();
        state();
      }

      function onPick(ev) {
        if (committed) return;
        var slot = Number(ev.currentTarget.dataset.slot);
        picked = slot;
        for (var k = 0; k < optBtns.length; k++) {
          optBtns[k].setAttribute('aria-pressed', k === slot ? 'true' : 'false');
        }
        goEl.disabled = false;
        state();
      }

      function onGo() {
        if (!committed) { commit(); } else { newRound(); }
      }

      function commit() {
        if (picked < 0) return;
        var chosen = layout[picked];
        var ok = chosen.kind === round.answer;
        committed = true;
        attempted++;
        lastCorrect = ok;
        streak = ok ? streak + 1 : 0;
        if (streak >= 3) mastered = true;

        for (var k = 0; k < optBtns.length; k++) {
          optBtns[k].disabled = true;
          if (layout[k].kind === round.answer) optBtns[k].classList.add('gvd-true');
        }
        showStage(round.answer);
        slabEl.textContent = STAGE_LABEL[round.answer];

        var text;
        if (ok && streak === 3) {
          text = 'Right — ' + NAME[round.answer] + '. Three in a row, so you have it. ' + RULE;
        } else if (ok) {
          text = 'Right — ' + NAME[round.answer] + '. ' + round.right;
        } else {
          text = 'Not quite — you chose “' + chosen.label + '”. ' + chosen.why;
        }
        capEl.innerHTML = '<span class="' + (ok ? 'gvd-yes' : 'gvd-no') + '">' +
          (ok ? 'Right —' : 'Not quite —') + '</span>' + esc(text.replace(/^(Right —|Not quite —)/, ''));
        srEl.textContent = text;

        goEl.textContent = mastered ? 'Another anyway' : 'Next scenario';
        goEl.disabled = false;
        runLine();
        state();
      }

      newRound();
    }
  };
})();
