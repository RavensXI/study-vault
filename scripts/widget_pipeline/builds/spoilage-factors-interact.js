/* spoilage-factors-interact
   Microbial growth needs every condition at once. A storage method closes
   some conditions and leaves others wide open, so the student commits to
   what happens AND to which condition is taken away. Both verdicts come
   from one factor model, so no two rounds can contradict each other.

   The model: five conditions, each at level 3 (open), 1 (held down) or
   0 (shut off). Growth runs at the LOWEST of them -- that is the whole
   idea. Nutrients are never removable; a food is made of them. */
(function () {
  'use strict';

  var ID = 'spoilage-factors-interact';

  /* Source stays ASCII; typography is applied on the way to the DOM so no
     tool in the chain can mangle a degree sign or a minus sign. */
  function ty(s) {
    return String(s)
      .replace(/--/g, '—')
      .replace(/MINUS/g, '−')
      .replace(/degC/g, '°C')
      .replace(/'/g, '’');
  }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  /* ---- the factor model ------------------------------------------------ */

  var FACTORS = [
    { k: 'nutrients', label: 'Nutrients', fixed: true },
    { k: 'moisture', label: 'Moisture' },
    { k: 'warmth', label: 'Warmth' },
    { k: 'oxygen', label: 'Oxygen' },
    { k: 'ph', label: 'Suitable pH' }
  ];
  var IDX = {};
  for (var fi = 0; fi < FACTORS.length; fi++) IDX[FACTORS[fi].k] = fi;

  var LOWER = {
    nutrients: 'nutrients', moisture: 'moisture', warmth: 'warmth',
    oxygen: 'oxygen', ph: 'suitable pH'
  };
  var TAGWORD = { 3: 'open', 1: 'held down', 0: 'shut off' };

  /* Levels are listed in FACTORS order: nutrients, moisture, warmth,
     oxygen, suitable pH. Everything a verdict needs is derived from them. */
  function derive(L) {
    var min = L[0], i;
    for (i = 1; i < L.length; i++) if (L[i] < min) min = L[i];
    var held = [];
    for (i = 0; i < L.length; i++) if (L[i] <= 1) held.push(FACTORS[i].k);
    return {
      min: min,
      outcome: min === 0 ? 'stopped' : (min === 1 ? 'slowed' : 'spoils'),
      answer: held.length === 0 ? 'none' : (held.length === 1 ? held[0] : 'more'),
      held: held
    };
  }

  var OUTSAID = { stopped: 'growth stops', slowed: 'slowed only', spoils: 'spoils anyway' };
  var OUTTRUE = {
    stopped: 'growth stops',
    slowed: 'growth is only slowed',
    spoils: 'it spoils anyway'
  };
  var ANSSAID = {
    moisture: 'moisture', warmth: 'warmth', oxygen: 'oxygen', ph: 'suitable pH',
    more: 'more than one', none: 'none of them'
  };

  var OUTOPT = [
    { k: 'stopped', strong: 'Growth stops', sub: 'keeps for months' },
    { k: 'slowed', strong: 'Slowed only', sub: 'days, not months' },
    { k: 'spoils', strong: 'Spoils anyway', sub: 'nothing is holding it' }
  ];
  var ANSOPT = [
    { k: 'moisture', label: 'Moisture' },
    { k: 'warmth', label: 'Warmth' },
    { k: 'oxygen', label: 'Oxygen' },
    { k: 'ph', label: 'Suitable pH' },
    { k: 'more', label: 'More than one' },
    { k: 'none', label: 'None of them' }
  ];

  /* ---- the rounds -------------------------------------------------------
     Every food and method here is one the two lessons teach: fridge at
     0-5 degC, freezer at MINUS18 degC, jam at 60-65% sugar, pickling at
     pH 2-3, vacuum packing, pasteurised milk, dried goods, yoghurt.      */

  var ROUNDS = [
    {
      id: 'fridge-chicken',
      scen: 'Yesterday\'s roast chicken, covered, on the top shelf of a fridge running at 4 degC.',
      L: [3, 3, 1, 3, 3],
      keeps: 'two or three days',
      right: 'Below 5 degC bacteria divide far more slowly, so the fridge buys two or three days. ' +
        'It buys nothing more: the meat is still moist, still full of protein, still in air and ' +
        'still at a neutral pH, so the count keeps creeping up.',
      dOut: {
        stopped: 'Chilling holds warmth down; it does not shut it off. 4 degC is still inside the ' +
          'range where bacteria manage, slowly, and the other four conditions are untouched. ' +
          'That is why a fridge buys days and a use-by date, not months.',
        spoils: 'The cold is doing real work. This same plate on a warm worktop would be unsafe by ' +
          'morning; at 4 degC it is good for two or three days.'
      }
    },
    {
      id: 'freezer-peas',
      scen: 'A bag of peas, blanched before packing, in a chest freezer at MINUS18 degC.',
      L: [3, 1, 0, 3, 3],
      keeps: 'months',
      right: 'MINUS18 degC is far below anything that can reproduce, and the water is locked up as ' +
        'ice, so two conditions go at once -- that is why a freezer stops growth where a fridge ' +
        'only slows it. Nothing is killed, though: thaw the peas and both conditions open together.',
      dOut: {
        slowed: 'A fridge slows, a freezer stops. At MINUS18 degC microorganisms cannot reproduce ' +
          'at all, and the water they would drink is ice. They survive, but they do not multiply.',
        spoils: 'Frozen peas keep for months. Growth needs liquid water and a workable temperature, ' +
          'and MINUS18 degC takes both away at the same time.'
      }
    },
    {
      id: 'jam-sealed',
      scen: 'Strawberry jam boiled to about 65% sugar and sealed hot into a sterilised jar, kept in a cupboard.',
      L: [3, 0, 3, 3, 3],
      keeps: 'up to two years unopened',
      right: 'Sugar does not poison anything -- it locks up the water. At 60 to 65% sugar the water ' +
        'activity is too low for bacteria or yeasts to take any up. The cupboard is warm and the jam ' +
        'is nothing but nutrients, and neither matters while the water is out of reach.',
      dOut: {
        slowed: 'This is a shut door, not a slow one. With no water available nothing grows at all, ' +
          'which is why an unopened jar keeps for up to two years in a warm cupboard.',
        spoils: 'Warmth, air and sugar are all there, and still nothing grows. Growth needs every ' +
          'condition together, and the water is gone.'
      }
    },
    {
      id: 'jam-opened',
      scen: 'The same jar, opened a month ago. A wet spoon has been dipped in, and it stands in a warm kitchen.',
      L: [3, 3, 3, 3, 3],
      keeps: 'a fuzzy patch on the surface within a week or two',
      right: 'Water from the spoon sits on top of the jam, where the sugar no longer holds it down. ' +
        'That thin film has moisture, warmth, air and sugar all at once -- which is why mould grows ' +
        'on the surface of a jar and not through the middle.',
      dOut: {
        stopped: 'The sugar was doing all of the work, and only while the water stayed locked up. A ' +
          'wet spoon puts free water back on the surface, and up there every condition is met at once.',
        slowed: 'Nothing is holding that surface film back. It is wet, warm, in air and made of sugar, ' +
          'so mould grows on it at normal speed -- a week or two and it is fuzzy.'
      }
    },
    {
      id: 'pickled-onions',
      scen: 'Onions packed in malt vinegar at about pH 2.5, sealed in a jar in the larder.',
      L: [3, 3, 3, 3, 0],
      keeps: 'a year or more',
      right: 'Nearly every bacterium, mould and yeast needs a pH near neutral, and pH 2.5 is far ' +
        'outside it. It makes no difference that the onions are wet, warm and full of nutrients: ' +
        'one condition, fully shut, is enough on its own.',
      dOut: {
        slowed: 'Acid this strong is a shut door rather than a slow one. At pH 2.5 the microorganisms ' +
          'that spoil food cannot work at all, so a sealed jar keeps for a year or more in a warm larder.',
        spoils: 'Everything else here suits them perfectly -- wet, warm, in air, full of nutrients. ' +
          'The acid alone is enough, because growth needs all five conditions together.'
      }
    },
    {
      id: 'bacon-warm',
      scen: 'Vacuum-packed bacon with the air drawn out, left on a warm worktop for two days.',
      L: [3, 3, 3, 1, 3],
      keeps: 'a couple of days, and it is not safe by then',
      right: 'Drawing the air out stops moulds and the bacteria that need oxygen, so it will not go ' +
        'furry. But some bacteria grow with no oxygen at all, Clostridium botulinum among them, and ' +
        'warmth, moisture and nutrients are all still there for those. That is why the pack says ' +
        'keep refrigerated.',
      dOut: {
        stopped: 'Taking oxygen away is never a full shutdown. Moulds and aerobic bacteria are gone, ' +
          'but anaerobic bacteria need no oxygen at all, so warmth and moisture keep working on the ' +
          'meat -- and this pack is dangerous long before it looks spoiled.',
        spoils: 'The vacuum is doing something real: with no oxygen, moulds and aerobic bacteria ' +
          'cannot grow, so it will not go furry. Anaerobic bacteria still can, and that is the danger.'
      }
    },
    {
      id: 'dried-pasta',
      scen: 'Dried pasta in a sealed jar in a warm cupboard.',
      L: [3, 0, 3, 3, 3],
      keeps: 'months, even years',
      right: 'Drying takes the water activity down so far that nothing can grow, and that on its own ' +
        'is enough. The pasta is warm, in air and made of starch -- every other condition is wide ' +
        'open, and none of them counts for anything without water.',
      dOut: {
        slowed: 'With no available water nothing grows at all, so this is a stop rather than a ' +
          'slowdown. Dried pasta keeps for months in a warm cupboard.',
        spoils: 'Warmth, air and starch are all there for them, and still nothing happens. Every ' +
          'condition has to be met together, and the water is missing.'
      }
    },
    {
      id: 'damp-pasta',
      scen: 'The same pasta, tipped into a paper bag with the lid left off, in a steamy kitchen. It has gone soft.',
      L: [3, 3, 3, 3, 3],
      keeps: 'mould within days',
      right: 'Drying was the only thing keeping this pasta, and damp air has undone it. The starch, ' +
        'the water, the warmth, the air and a neutral pH are all there together now, which is ' +
        'exactly the state the pasta was dried to avoid. Dried food keeps for as long as it stays dry.',
      dOut: {
        stopped: 'Drying only works while the food stays dry. Damp air has put the water back, and ' +
          'with all five conditions met at once this pasta is no better protected than fresh food.',
        slowed: 'Nothing is being held down any more. Once the water is back the pasta has the full ' +
          'set -- nutrients, moisture, warmth, air and a neutral pH -- so it moulds at normal speed.'
      }
    },
    {
      id: 'yoghurt-warm',
      scen: 'A pot of plain yoghurt left open on the worktop. Its lactic acid has taken the pH down to about 4.4.',
      L: [3, 3, 3, 3, 1],
      keeps: 'a day or two, souring as it goes',
      right: 'Lactic acid holds most harmful bacteria back, which is why yoghurt keeps better than ' +
        'the milk it was made from. But pH 4.4 is nowhere near vinegar\'s 2.5, so moulds and yeasts ' +
        'tolerate it, and warmth, moisture and nutrients are all still open.',
      dOut: {
        stopped: 'Held down is not shut off. pH 4.4 stops most bacteria but not moulds or yeasts, ' +
          'and nothing else has been taken away, so an open pot in a warm kitchen sours within a ' +
          'day or two.',
        spoils: 'The acid is buying real time. Plain milk left in the same warm kitchen would be off ' +
          'far faster; yoghurt makes its own preservative as it ferments.'
      }
    },
    {
      id: 'yoghurt-fridge',
      scen: 'The same yoghurt, lid on, in the fridge at 4 degC.',
      L: [3, 3, 1, 3, 1],
      keeps: 'a fortnight or more',
      right: 'Two conditions are held down at once now, and they cover each other: the acid stops ' +
        'most bacteria, and the cold slows what the acid does not touch, the moulds and yeasts. ' +
        'Neither is a full stop on its own, which is why the pot still carries a use-by date.',
      dOut: {
        stopped: 'Neither condition is fully shut. pH 4.4 is not vinegar and 4 degC is not a freezer, ' +
          'so growth is very slow rather than stopped -- a fortnight, and then it goes.',
        spoils: 'Two conditions held down together beat either one alone. That is why yoghurt ' +
          'outlasts milk on the same fridge shelf by more than a week.'
      }
    },
    {
      id: 'bacon-fridge',
      scen: 'The same vacuum pack of bacon, unopened, in the fridge at 4 degC.',
      L: [3, 3, 1, 1, 3],
      keeps: 'several weeks unopened',
      right: 'The vacuum removes the moulds and the bacteria that need oxygen; the cold slows the ' +
        'anaerobic ones the vacuum cannot touch. Neither is a full stop alone, but together they ' +
        'cover each other\'s gaps -- weeks here, days on a warm worktop.',
      dOut: {
        stopped: 'Neither condition is fully shut, so the pack still carries a use-by date. ' +
          'Anaerobic bacteria grow without oxygen, and 4 degC only slows them.',
        spoils: 'Two partial controls together are much stronger than one. The vacuum takes out the ' +
          'aerobes and the cold holds back the rest, so this keeps for weeks.'
      }
    },
    {
      id: 'milk-fridge',
      scen: 'An opened carton of pasteurised milk, back in the fridge at 4 degC.',
      L: [3, 3, 1, 3, 3],
      keeps: 'three or four days once opened',
      right: 'Pasteurising killed the bacteria that were in the milk, but it changed no condition at ' +
        'all. Once the carton is opened and new bacteria get in, only the cold is holding them, and ' +
        'the milk is still moist, still full of nutrients and still at a neutral pH.',
      dOut: {
        stopped: 'Heating the milk removed the microorganisms, not the conditions. New ones get in ' +
          'the moment the carton is opened, and 4 degC only slows them -- which is why an opened ' +
          'carton is good for three or four days, not months.',
        spoils: 'The cold is doing real work. The same open carton in a warm kitchen would be sour ' +
          'within a day; in the fridge it lasts three or four days.'
      }
    }
  ];

  /* generic diagnoses, derived, for outcome misses not authored above */
  function genericOut(said, real, r) {
    if (said === 'stopped' && real === 'slowed') {
      return 'Held down is not shut off: the lowest condition here is still just workable, so ' +
        'growth carries on slowly. That buys ' + r.keeps + ', and no more.';
    }
    if (said === 'stopped' && real === 'spoils') {
      return 'Nothing here is being held down at all, so there is nothing to stop growth.';
    }
    if (said === 'slowed' && real === 'stopped') {
      return 'This is a full stop rather than a slowdown: one condition is shut off completely, ' +
        'and growth needs all of them together.';
    }
    if (said === 'slowed' && real === 'spoils') {
      return 'Nothing is being held down here, so nothing is slowing it either.';
    }
    if (said === 'spoils' && real === 'stopped') {
      return 'One condition is shut off completely, and growth needs every condition at once, so ' +
        'it does not spoil at all while that stays shut.';
    }
    return 'Something real is being held down here, and that buys ' + r.keeps + '.';
  }

  function heldPhrase(d) {
    var parts = [], i;
    for (i = 0; i < d.held.length; i++) parts.push(LOWER[d.held[i]]);
    if (parts.length === 2) return parts[0] + ' and ' + parts[1];
    return parts.slice(0, -1).join(', ') + ' and ' + parts[parts.length - 1];
  }

  function trueClause(d) {
    if (d.answer === 'none') return 'Nothing at all is taken away here.';
    if (d.answer === 'more') {
      return 'Two conditions are taken away here, not one: ' + heldPhrase(d) + '.';
    }
    return 'It is ' + LOWER[d.answer] + ' that this storage takes away.';
  }

  /* ---- styles ----------------------------------------------------------- */

  var CSS = [
    '.svw-spf{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45;display:flex;flex-direction:column}',
    '.svw-spf *{box-sizing:border-box}',
    /* fixed reading order; on commit the action bar drops below the verdict
       without ever moving in the DOM, so keyboard focus stays put */
    '.svw-spf .spf-kick{order:1}.svw-spf .spf-title{order:2}.svw-spf .spf-frame{order:3}',
    '.svw-spf .spf-stage{order:4}.svw-spf .spf-grp1{order:5}.svw-spf .spf-grp2{order:6}',
    '.svw-spf .spf-bar{order:7}.svw-spf .spf-fb{order:8}.svw-spf .spf-sr{order:10}',
    '.svw-spf .spf-bar.is-after{order:9;margin-top:.45rem}',
    '.svw-spf .spf-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .18rem}',
    '.svw-spf .spf-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.16rem;font-weight:600;line-height:1.2;margin:0 0 .28rem}',
    '.svw-spf .spf-frame{font-size:.81rem;line-height:1.45;color:#5b564e;margin:0 0 .55rem}',
    '.svw-spf .spf-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.6rem .7rem;margin:0 0 .55rem}',
    '.svw-spf .spf-scen{font-size:.85rem;font-weight:600;line-height:1.4;margin:0 0 .45rem}',
    '.svw-spf .spf-shead{font-size:.67rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:#8d8880;margin:0 0 .3rem}',
    '.svw-spf .spf-row{display:grid;grid-template-columns:5.1rem 1fr 4.9rem;align-items:center;gap:.35rem;padding:.12rem .28rem;border:1px solid transparent;border-radius:7px}',
    '.svw-spf .spf-name{font-size:.72rem;font-weight:600;line-height:1.2}',
    '.svw-spf .spf-track{height:9px;border-radius:5px;background:#ece6dc;overflow:hidden}',
    '.svw-spf .spf-fill{display:block;height:100%;border-radius:5px;width:100%}',
    '.svw-spf .spf-tag{font-size:.67rem;font-weight:600;line-height:1.2;color:#8d8880;text-align:right}',
    '.svw-spf .spf-row.is-key .spf-tag{font-weight:700}',
    '.svw-spf .spf-row.is-miss{border-color:#ddd7cd;border-style:dashed}',
    '.svw-spf .spf-grp{margin:0 0 .45rem}',
    '.svw-spf .spf-grp.is-locked{opacity:.42}',
    '.svw-spf .spf-step{display:flex;align-items:center;gap:.38rem;font-size:.75rem;font-weight:700;margin:0 0 .3rem}',
    '.svw-spf .spf-num{display:inline-flex;align-items:center;justify-content:center;width:1.02rem;height:1.02rem;border-radius:5px;font-size:.64rem;font-weight:700;color:#fff}',
    '.svw-spf .spf-opts{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.32rem}',
    '.svw-spf .spf-opt{font-family:inherit;text-align:left;padding:.36rem .4rem;border:1px solid #ddd7cd;border-radius:10px;background:#fff;color:#2d2a26;cursor:pointer}',
    '.svw-spf .spf-opt b{display:block;font-size:.75rem;font-weight:700;line-height:1.2}',
    '.svw-spf .spf-opt i{display:block;font-style:normal;font-size:.67rem;font-weight:500;line-height:1.2;color:#8d8880;margin-top:.1rem}',
    '.svw-spf .spf-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-spf .spf-opt[aria-pressed="true"] i{color:#d8d2c8}',
    '.svw-spf .spf-opt:disabled{cursor:default}',
    '.svw-spf .spf-opt--plain{font-size:.75rem;font-weight:600;line-height:1.2;text-align:center;padding:.42rem .3rem}',
    '.svw-spf .spf-bar{display:flex;align-items:center;justify-content:space-between;gap:.6rem;margin:.1rem 0 0}',
    '.svw-spf .spf-run{font-size:.74rem;color:#8d8880;margin:0}',
    '.svw-spf .spf-go{font-family:inherit;font-size:.83rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer;white-space:nowrap}',
    '.svw-spf .spf-go:disabled{background:#f2ede5;border-color:#e9e3d9;color:#a8a29a;cursor:default}',
    '.svw-spf .spf-fb{font-size:.83rem;line-height:1.46;margin:.5rem 0 0}',
    '.svw-spf .spf-vd{font-weight:700}',
    '.svw-spf .spf-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
    '.svw-spf .spf-fill{transition:width .34s cubic-bezier(0.16,1,0.3,1),background-color .34s ease}',
    '.svw-spf--still .spf-fill{transition:none}'
  ].join('');

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = ty(txt);
    return n;
  }

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i];
      a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /* ---- mount ------------------------------------------------------------ */

  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
      (ctx.accent || '').trim() || '#8a6a4f';
    var OPEN_FILL = accent + '73';
    var HELD_FILL = '#c4bdb1';

    var S = {
      round: null, d: null, pickOut: null, pickAns: null, committed: false,
      streak: 0, attempted: 0, mastered: false, lastCorrect: null
    };

    var wrap = el('div', 'svw-spf' + (ctx.reducedMotion ? ' svw-spf--still' : ''));
    var style = document.createElement('style');
    style.textContent = CSS;
    wrap.appendChild(style);

    var kick = el('p', 'spf-kick', 'Food safety');
    kick.style.color = accent;
    wrap.appendChild(kick);
    wrap.appendChild(el('h3', 'spf-title', 'What does this storage actually stop?'));
    wrap.appendChild(el('p', 'spf-frame',
      'Out on the worktop a food meets every condition microorganisms need, all at once. ' +
      'Predict what this storage takes away -- and whether that is enough.'));

    /* stage: the scenario, then the five conditions as bars */
    var stage = el('div', 'spf-stage');
    var scen = el('p', 'spf-scen');
    var shead = el('p', 'spf-shead');
    stage.appendChild(scen);
    stage.appendChild(shead);
    var rows = {};
    FACTORS.forEach(function (f) {
      var row = el('div', 'spf-row');
      row.appendChild(el('span', 'spf-name', f.label));
      var track = el('span', 'spf-track');
      var fill = el('span', 'spf-fill');
      track.appendChild(fill);
      row.appendChild(track);
      var tag = el('span', 'spf-tag');
      row.appendChild(tag);
      rows[f.k] = { row: row, fill: fill, tag: tag };
      stage.appendChild(row);
    });
    wrap.appendChild(stage);

    function stepLabel(n, text) {
      var lab = el('p', 'spf-step');
      var num = el('span', 'spf-num', String(n));
      num.style.background = accent;
      lab.appendChild(num);
      lab.appendChild(document.createTextNode(ty(text)));
      return lab;
    }

    /* step 1 -- what happens */
    var g1 = el('div', 'spf-grp spf-grp1');
    g1.appendChild(stepLabel(1, 'What happens to it?'));
    var r1 = el('div', 'spf-opts');
    var outBtns = {};
    OUTOPT.forEach(function (o) {
      var b = el('button', 'spf-opt');
      b.type = 'button';
      b.setAttribute('aria-pressed', 'false');
      b.appendChild(el('b', null, o.strong));
      b.appendChild(el('i', null, o.sub));
      b.addEventListener('click', function () { pick('out', o.k); });
      outBtns[o.k] = b;
      r1.appendChild(b);
    });
    g1.appendChild(r1);
    wrap.appendChild(g1);

    /* step 2 -- which condition it takes away */
    var g2 = el('div', 'spf-grp spf-grp2 is-locked');
    g2.appendChild(stepLabel(2, 'Which condition does it take away?'));
    var r2 = el('div', 'spf-opts');
    var ansBtns = {};
    ANSOPT.forEach(function (o) {
      var b = el('button', 'spf-opt spf-opt--plain', o.label);
      b.type = 'button';
      b.disabled = true;
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () { pick('ans', o.k); });
      ansBtns[o.k] = b;
      r2.appendChild(b);
    });
    g2.appendChild(r2);
    wrap.appendChild(g2);

    var bar = el('div', 'spf-bar');
    var run = el('p', 'spf-run');
    var go = el('button', 'spf-go', 'Check');
    go.type = 'button';
    go.disabled = true;
    go.addEventListener('click', function () {
      if (S.committed) { nextRound(); } else { commit(); }
    });
    bar.appendChild(run);
    bar.appendChild(go);
    wrap.appendChild(bar);

    var fb = el('p', 'spf-fb');
    fb.style.display = 'none';
    wrap.appendChild(fb);

    var sr = el('p', 'spf-sr');
    sr.setAttribute('aria-live', 'polite');
    wrap.appendChild(sr);

    root.appendChild(wrap);

    /* ---- behaviour ---- */

    function publish() {
      root.dataset.svState = JSON.stringify({
        streak: S.streak, mastered: S.mastered, attempted: S.attempted,
        correct: S.lastCorrect,
        round: S.round ? S.round.id : null,
        /* the truth is published only once the student has committed, so
           dataset.svState can never be read as an answer key */
        outcome: S.committed ? S.d.outcome : null,
        answer: S.committed ? S.d.answer : null,
        picked: { outcome: S.pickOut, condition: S.pickAns }
      });
    }

    function paint(levels) {
      FACTORS.forEach(function (f, i) {
        var lev = levels[i];
        var o = rows[f.k];
        o.fill.style.width = lev === 3 ? '100%' : (lev === 1 ? '32%' : '5%');
        o.fill.style.backgroundColor = lev === 3 ? OPEN_FILL : HELD_FILL;
        o.tag.textContent = ty(f.fixed ? 'always open' : TAGWORD[lev]);
        o.tag.style.color = '#8d8880';
        o.row.className = 'spf-row';
        o.row.style.background = '';
        o.row.style.borderColor = 'transparent';
      });
    }

    function markReveal() {
      var d = S.d;
      d.held.forEach(function (k) {
        var o = rows[k];
        o.row.classList.add('is-key');
        o.row.style.background = accent + '18';
        o.row.style.borderColor = accent;
        o.tag.style.color = accent;
      });
      if (S.pickAns && rows[S.pickAns] && d.held.indexOf(S.pickAns) === -1) {
        rows[S.pickAns].row.classList.add('is-miss');
      }
    }

    function pick(kind, key) {
      if (S.committed) return;
      if (kind === 'out') {
        S.pickOut = key;
        OUTOPT.forEach(function (o) {
          outBtns[o.k].setAttribute('aria-pressed', o.k === key ? 'true' : 'false');
        });
        g2.classList.remove('is-locked');
        ANSOPT.forEach(function (o) { ansBtns[o.k].disabled = false; });
      } else {
        S.pickAns = key;
        ANSOPT.forEach(function (o) {
          ansBtns[o.k].setAttribute('aria-pressed', o.k === key ? 'true' : 'false');
        });
      }
      go.disabled = !(S.pickOut && S.pickAns);
      sr.textContent = ty('Chosen: ' + (S.pickOut ? OUTSAID[S.pickOut] : 'outcome not set') +
        ', ' + (S.pickAns ? ANSSAID[S.pickAns] : 'condition not set') + '.');
      publish();
    }

    function clearPicks() {
      if (S.committed) return;
      S.pickOut = null; S.pickAns = null;
      OUTOPT.forEach(function (o) { outBtns[o.k].setAttribute('aria-pressed', 'false'); });
      ANSOPT.forEach(function (o) {
        ansBtns[o.k].setAttribute('aria-pressed', 'false');
        ansBtns[o.k].disabled = true;
      });
      g2.classList.add('is-locked');
      go.disabled = true;
      publish();
    }

    wrap.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !S.committed && (S.pickOut || S.pickAns)) {
        clearPicks();
        e.stopPropagation();
      }
    });

    function factorDiag() {
      var r = S.round, d = S.d, picked = S.pickAns;
      if (picked === 'none') {
        return 'You said nothing was taken away, but ' + heldPhrase(d) + ' ' +
          (d.held.length > 1 ? 'are' : 'is') + ' -- and that is what buys the time.';
      }
      if (picked === 'more') {
        if (d.answer === 'none') {
          return 'Nothing at all is taken away here: all five conditions are met together.';
        }
        return 'Only one condition is taken away here, not two: ' + LOWER[d.answer] +
          '. The other four are wide open.';
      }
      var lev = r.L[IDX[picked]];
      if (lev === 3) {
        return 'The ' + LOWER[picked] + ' bar is wide open here -- this storage does nothing to it. ' +
          trueClause(d);
      }
      return 'The ' + LOWER[picked] + ' is taken away, but not on its own. ' + trueClause(d);
    }

    /* Each named condition carries its OWN level word, so the sentence can
       never say "held down" about a bar the reveal draws as "shut off". */
    function ansTrue() {
      var d = S.d, L = S.round.L;
      if (d.answer === 'none') return 'nothing taken away at all';
      if (d.answer === 'more') {
        return d.held.map(function (k) {
          return LOWER[k] + ' ' + TAGWORD[L[IDX[k]]];
        }).join(' and ');
      }
      return LOWER[d.answer] + ' ' + TAGWORD[L[IDX[d.answer]]];
    }

    function verdict() {
      var r = S.round, d = S.d;
      var okOut = S.pickOut === d.outcome, okAns = S.pickAns === d.answer;
      if (okOut && okAns) {
        return { ok: true, head: 'Right -- ',
          tail: OUTTRUE[d.outcome] + ', with ' + ansTrue() + '. ' + r.right };
      }
      var tail = 'you said ' + OUTSAID[S.pickOut] + ', ' + ANSSAID[S.pickAns] + '. ' +
        'What happens: ' + OUTTRUE[d.outcome] + ', with ' + ansTrue() + ' -- ' + r.keeps + '. ';
      tail += okOut ? factorDiag()
                    : ((r.dOut && r.dOut[S.pickOut]) || genericOut(S.pickOut, d.outcome, r));
      return { ok: false, head: 'Not quite -- ', tail: tail };
    }

    function runLine() {
      var t;
      if (S.mastered && S.committed && S.lastCorrect) t = 'Three in a row -- you have it.';
      else if (S.streak === 2) t = '2 in a row -- one more and you have it.';
      else if (S.streak === 1) t = '1 in a row -- two more and you have it.';
      else if (S.attempted === 0) t = 'Three in a row finishes it.';
      else t = 'Run reset -- three in a row finishes it.';
      run.textContent = ty(t);
    }

    function commit() {
      var v = verdict();
      S.attempted += 1;
      S.lastCorrect = v.ok;
      S.streak = v.ok ? S.streak + 1 : 0;
      var justMastered = false;
      if (S.streak >= 3 && !S.mastered) { S.mastered = true; justMastered = true; }
      S.committed = true;

      paint(S.round.L);
      markReveal();

      var text = v.tail;
      if (justMastered) {
        /* the run line already says three in a row, so this says what the
           student now KNOWS rather than repeating the count */
        text += ' Growth needs every condition at once, so a store stops spoilage only by shutting ' +
          'one of them off completely. Hold a condition down and you only buy time.';
      }
      fb.textContent = '';
      var vd = el('span', 'spf-vd', v.head);
      if (v.ok) vd.style.color = '#4f7d63';
      fb.appendChild(vd);
      fb.appendChild(document.createTextNode(ty(text)));
      fb.style.display = '';

      g1.style.display = 'none';
      g2.style.display = 'none';
      bar.classList.add('is-after');
      shead.textContent = ty('What this storage leaves');
      go.textContent = ty(S.mastered ? 'Another anyway' : 'Next scenario');
      go.disabled = false;
      runLine();
      sr.textContent = ty(v.head + text);
      publish();
    }

    var order = shuffle(ROUNDS.map(function (r, i) { return i; }));
    var pos = 0;

    function nextRound() {
      if (pos >= order.length) { order = shuffle(order); pos = 0; }
      var r = ROUNDS[order[pos]];
      pos += 1;

      S.round = r;
      S.d = derive(r.L);
      S.pickOut = null; S.pickAns = null; S.committed = false;

      scen.textContent = ty(r.scen);
      shead.textContent = ty('What growth needs -- all five at once');
      paint([3, 3, 3, 3, 3]);

      OUTOPT.forEach(function (o) { outBtns[o.k].setAttribute('aria-pressed', 'false'); });
      ANSOPT.forEach(function (o) {
        ansBtns[o.k].setAttribute('aria-pressed', 'false');
        ansBtns[o.k].disabled = true;
      });
      g2.classList.add('is-locked');
      g1.style.display = ''; g2.style.display = '';
      bar.classList.remove('is-after');
      fb.style.display = 'none';
      go.textContent = ty('Check');
      go.disabled = true;
      runLine();
      publish();
    }

    nextRound();
  }

  window.SVWidget = {
    meta: {
      id: ID,
      title: 'What does this storage actually stop?',
      teaches: 'Microorganisms need nutrients, moisture, warmth, oxygen and a suitable pH together, ' +
        'so a storage method stops spoilage only where it shuts a condition off completely; a ' +
        'condition merely held down buys time and nothing more.'
    },
    mount: mount
  };
})();
