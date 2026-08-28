/* The two scoreboards: battlefield success against war aims.
   One episode's fighting is laid out as scoreboard 1. The student commits a
   two-part answer — where it leaves the named side, and which fact decides
   that — before scoreboard 2 (the war aim and the clock) is revealed.
   Self-contained: no imports, no network, every selector scoped to .svw-tsv. */
(function () {
  'use strict';

  var CSS = [
'.svw-tsv{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
'.svw-tsv *{box-sizing:border-box}',
'.svw-tsv p{margin:0}',
'.svw-tsv .t-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--t-acc);margin:0 0 .2rem}',
'.svw-tsv .t-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.18rem;font-weight:600;line-height:1.18;margin:0 0 .3rem}',
'.svw-tsv .t-frame{font-size:.82rem;line-height:1.44;color:#5b564e;margin:0 0 .5rem}',
'.svw-tsv .t-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;padding:.5rem .6rem;margin:0 0 .5rem}',
'.svw-tsv .t-board{font-size:.66rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#8d8880;margin:0 0 .16rem}',
'.svw-tsv .t-ep{font-size:.8rem;font-weight:600;line-height:1.32;margin:0 0 .3rem}',
'.svw-tsv .t-when{color:var(--t-acc)}',
'.svw-tsv .t-row{display:grid;grid-template-columns:7.4rem 1fr;gap:.35rem;font-size:.78rem;line-height:1.32;padding:.16rem 0;border-top:1px solid #efe9e0}',
'.svw-tsv .t-k{color:#8d8880}',
'.svw-tsv .t-v{font-weight:600;font-variant-numeric:tabular-nums}',
'.svw-tsv .t-two{display:none;margin-top:.42rem;padding-top:.4rem;border-top:1px solid #e0d9cd}',
'.svw-tsv .t-two.on{display:block}',
'.svw-tsv .t-2h{font-size:.66rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--t-acc);margin:0 0 .22rem}',
'.svw-tsv .t-2grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:.28rem .9rem}',
'.svw-tsv .t-2k{display:block;font-size:.68rem;font-weight:600;color:#8d8880}',
'.svw-tsv .t-2v{font-size:.78rem;line-height:1.34}',
'.svw-tsv .t-2m{font-size:.78rem;font-weight:600;line-height:1.34;margin:.28rem 0 0;padding-top:.26rem;border-top:1px solid #efe9e0}',
'.svw-tsv .t-ask{display:block}',
'.svw-tsv .t-ask.off{display:none}',
'.svw-tsv .t-gh{display:flex;align-items:center;gap:.4rem;font-size:.78rem;font-weight:600;line-height:1.3;margin:0 0 .28rem}',
'.svw-tsv .t-chip{flex:0 0 auto;width:1.12rem;height:1.12rem;border-radius:50%;background:var(--t-acc);color:#fff;font-size:.66rem;font-weight:700;display:flex;align-items:center;justify-content:center}',
'.svw-tsv .t-gh.sleep{color:#a9a39a}',
'.svw-tsv .t-gh.sleep .t-chip{background:#ddd7cd;color:#fff}',
'.svw-tsv .t-scale{display:grid;grid-template-columns:repeat(3,1fr);gap:.28rem;margin:0 0 .4rem}',
'.svw-tsv .t-opts{display:flex;flex-direction:column;gap:.26rem;margin:0 0 .38rem}',
'.svw-tsv .t-opt{display:block;width:100%;font:inherit;font-size:.81rem;line-height:1.32;font-weight:500;color:#2d2a26;background:#fff;border:1px solid #ddd7cd;border-radius:10px;padding:.34rem .58rem;cursor:pointer}',
'.svw-tsv .t-scale .t-opt{text-align:center;padding:.34rem .3rem}',
'.svw-tsv .t-opts .t-opt{text-align:left}',
'.svw-tsv .t-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
'.svw-tsv .t-opt[disabled]{cursor:default;color:#a9a39a;background:#faf8f5}',
'.svw-tsv .t-fb{display:none}',
'.svw-tsv .t-fb.on{display:block}',
'.svw-tsv .t-flag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin:0 0 .18rem}',
'.svw-tsv .t-flag.ok{color:#4f7d63}',
'.svw-tsv .t-flag.no{color:#5b564e}',
'.svw-tsv .t-say{font-size:.82rem;line-height:1.46;margin:0}',
'.svw-tsv .t-act{display:flex;align-items:center;justify-content:space-between;gap:.6rem;margin-top:.46rem}',
'.svw-tsv .t-run{font-size:.75rem;line-height:1.35;color:#5b564e;font-variant-numeric:tabular-nums}',
'.svw-tsv .t-go{flex:0 0 auto;font:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.46rem .95rem;cursor:pointer}',
'.svw-tsv .t-go[disabled]{background:#faf8f5;color:#a9a39a;border-color:#ddd7cd;cursor:default}',
'.svw-tsv .t-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}'
  ].join('\n');

  /* The three verdicts on scoreboard 2. Left to right they are a scale, so
     they keep their order every round. Reading the fighting straight off
     scoreboard 1 — the misconception — always reaches one of them. */
  var VERDICTS = [
    { id: 'win',   label: 'Closer to winning', echo: 'closer to winning' },
    { id: 'level', label: 'No closer either way', echo: 'no closer either way' },
    { id: 'lose',  label: 'Closer to losing', echo: 'closer to losing' }
  ];

  /* Each round: one real episode, its fighting as figures, the side being
     judged, the correct verdict, and three candidate deciders. Exactly one
     decider in every round is the tactical count itself (mis: true). */
  var ROUNDS = [
  {
    id: 'michael', side: 'Germany', verb: 'was',
    when: '21 March 1918',
    ep: 'Operation Michael: the German spring offensive opens on the Somme.',
    led: [
      ['Ground taken', '65 km — most since 1914'],
      ['Opening barrage', 'over a million shells'],
      ['German losses', 'about 240,000 men'],
      ['Americans', '250,000 a month by July']
    ],
    v: 'lose',
    vfb: {
      win: 'The biggest gain in four years bought nothing that mattered: no rail junction, no wedge between the British and French armies, no decision.',
      level: 'It was worse than level. The ground cost about 240,000 trained men Germany could not replace, and left a longer, unfortified line to hold.',
      lose: 'The gain was real and it left Germany weaker: irreplaceable troops spent, more line to hold, and still no decision before the Americans.'
    },
    rs: [
      { ok: true, echo: 'the clock on the Americans',
        t: 'Germany had to force a decision before American numbers told.' },
      { mis: true, echo: 'the ground taken',
        t: 'The ground: 65 km in a week, the biggest advance since 1914.',
        fb: 'Ground only counts if something you need sits on it. Ludendorff took open country and ended further from the one result he had to have.' },
      { echo: 'a shortage of guns and shells',
        t: 'Germany had run out of guns and shells, so the attack stopped.',
        fb: 'Germany fired a million shells in five hours on the first morning. The attack outran its own supplies and its objective — it was not disarmed.' }
    ],
    had: 'Win before American numbers tell.',
    clock: 'By July, 250,000 Americans a month.',
    move: 'The 65 km touched neither.'
  },
  {
    id: 'hundred', side: 'the Allies', verb: 'were',
    when: '8 August 1918',
    ep: 'The Hundred Days: the Allies attack at Amiens and keep attacking.',
    led: [
      ['8 August', 'Ludendorff’s “black day”'],
      ['German prisoners', 'about 385,000'],
      ['Hindenburg Line', 'broken, 29 September'],
      ['German allies', 'three quit by 3 November']
    ],
    v: 'win',
    vfb: {
      win: 'Here the two scoreboards agree — not because ground was taken, but because every attack cost Germany men and allies it could not replace.',
      level: 'These gains did count. Germany lost about 385,000 prisoners and three allies inside six weeks, then asked for an armistice.',
      lose: 'The Allies were not sliding backwards. They broke the Hindenburg Line on 29 September and Germany sought terms in November.'
    },
    rs: [
      { ok: true, echo: 'losses Germany could not replace',
        t: 'Germany was losing men and allies it had no way of replacing.' },
      { mis: true, echo: 'the ground taken',
        t: 'The ground: the side taking ground is the side winning the war.',
        fb: 'Right verdict, wrong reason: Germany took more ground in March and came out weaker. What counts here is that its losses cannot be replaced.' },
      { echo: 'a German mutiny',
        t: 'The German army mutinied, so the Allies walked into empty ground.',
        fb: 'German units fought hard all autumn and the Allies paid for every mile. The mutiny at Kiel came in November, after the army was already beaten.' }
    ],
    had: 'Wear the German army past holding a line.',
    clock: 'It ran their way: German reserves shrank.',
    move: 'This time both scoreboards moved together.'
  },
  {
    id: 'sweep', side: 'the United States', verb: 'was',
    when: '1966–67',
    ep: 'Search and destroy: US units sweep the countryside for NLF fighters.',
    led: [
      ['US troops', 'about 485,000 by 1967'],
      ['Enemy dead reported', 'far above US losses'],
      ['US dead by 1968', 'more than 15,000'],
      ['After each sweep', 'the unit went back']
    ],
    v: 'level',
    vfb: {
      win: 'The count rose and the map did not change: the unit went back to base and the NLF walked into the same villages that night.',
      level: 'Four years of escalation and the position was the same: the counting measured American effort, not Vietnamese ground made safe.',
      lose: 'The United States was not being beaten in the field. Its units won nearly every engagement; what they could not do was make a village stay safe.'
    },
    rs: [
      { ok: true, echo: 'the ground nobody held',
        t: 'A sweep that ends back at base leaves the villages as they were.' },
      { mis: true, echo: 'the body count',
        t: 'The body count: they were killing far more than they were losing.',
        fb: 'A body count only wins a war if the enemy runs out of bodies. The NLF replaced its losses down the Trail and chose when to fight again.' },
      { echo: 'losing the fights',
        t: 'American troops were being beaten in the fighting itself.',
        fb: 'American units won almost every engagement they fought — that is exactly the problem. The defeat was never on the battlefield.' }
    ],
    had: 'Make South Vietnam safe enough to stand alone.',
    clock: 'US patience: half now called it a mistake.',
    move: 'The body count touched neither.'
  },
  {
    id: 'tet', side: 'the NLF', verb: 'was',
    when: '30 January 1968',
    ep: 'The Tet Offensive: the NLF and North Vietnamese army attack across the South.',
    led: [
      ['Towns attacked', 'more than 100'],
      ['Fighters sent in', 'about 80,000'],
      ['Positions kept', 'none — all retaken'],
      ['NLF losses', 'tens of thousands']
    ],
    v: 'win',
    vfb: {
      win: 'Beaten on every street, ahead on the scoreboard they cared about: inside two months Johnson halted most bombing, quit the race and agreed to talks.',
      level: 'It moved them a long way. Inside two months Johnson halted most of the bombing, gave up his re-election bid and agreed to talks in Paris.',
      lose: 'On the ground, yes: they lost tens of thousands, kept nothing, and the rising in the South never came. But holding ground was never the aim.'
    },
    rs: [
      { ok: true, echo: 'American patience',
        t: 'They only had to survive until America stopped paying the price.' },
      { mis: true, echo: 'the losses they took',
        t: 'The losses: tens of thousands dead and every position retaken.',
        fb: 'They spent those fighters knowingly. Tet was measured by what Americans watching at home concluded, not by what its units kept.' },
      { echo: 'the cities they held',
        t: 'They captured Saigon and Hue and held on to them.',
        fb: 'They held nothing: every position was retaken, Hue by late February. Tet worked through what it showed, not through what it captured.' }
    ],
    had: 'Avoid defeat until America gives up.',
    clock: 'It ran their way: Johnson quit the race.',
    move: 'Losing the streets touched neither.'
  },
  {
    id: 'thunder', side: 'the United States', verb: 'was',
    when: '2 March 1965',
    ep: 'Rolling Thunder: sustained US bombing of North Vietnam and the supply routes.',
    led: [
      ['Ran for', 'three and a half years'],
      ['Bombs dropped', 'over 600,000 tons'],
      ['US aircraft lost', 'around 900'],
      ['Ho Chi Minh Trail', 'repaired, still working']
    ],
    v: 'level',
    vfb: {
      win: 'Three and a half years of bombing and the supplies still went south: the Trail was mended by hand and rerouted faster than it could be cut.',
      level: 'The tonnage was enormous and the position did not move: North Vietnam had few factories to lose, and the Trail was mended as fast as it was cut.',
      lose: 'The bombing did not lose America the war either. Around 900 aircraft and their crews were a heavy price, but the position did not move.'
    },
    rs: [
      { ok: true, echo: 'what the bombs could not reach',
        t: 'Bombs could not reach what kept the war in the South going.' },
      { mis: true, echo: 'the tonnage dropped',
        t: 'The tonnage: over 600,000 tons must have brought Hanoi near breaking.',
        fb: 'Tonnage assumes the enemy has something worth bombing. North Vietnam was mostly farmland, and the war in the South ran on rice and bicycles.' },
      { echo: 'stopping too soon',
        t: 'The bombing was called off too early for it to work.',
        fb: 'It ran from March 1965 to late 1968, the longest sustained bombing campaign in American history. Time was not the missing ingredient.' }
    ],
    had: 'Break Hanoi’s will; cut the supply route.',
    clock: 'US patience, and 900 aircrew lost or held.',
    move: 'The tonnage touched neither.'
  },
  {
    id: 'uboat', side: 'Germany', verb: 'was',
    when: '1 February 1917',
    ep: 'Unrestricted submarine warfare: U-boats sink any ship supplying Britain.',
    led: [
      ['Sunk in April 1917', 'about 870,000 tons'],
      ['British wheat', 'a few weeks’ supply'],
      ['United States', 'declared war, 6 April'],
      ['From May 1917', 'convoys cut the losses']
    ],
    v: 'lose',
    vfb: {
      win: 'The tonnage was real and it came at the worst possible price: sinking neutral shipping is what brought the United States in on 6 April 1917.',
      level: 'It was worse than level. The sinkings peaked in April and fell away under convoy, while the war gained an enemy Germany could not out-produce.',
      lose: 'The campaign had to starve Britain out before it brought America in. It did the second, not the first, and convoys then closed the window.'
    },
    rs: [
      { ok: true, echo: 'what the sinkings brought in',
        t: 'It had to force Britain out before it brought America in.' },
      { mis: true, echo: 'the tonnage sunk',
        t: 'The tonnage: about 870,000 tons sunk in April 1917 alone.',
        fb: 'Sinking ships was the method, not the aim. The aim was to force Britain out before America arrived — and the sinkings did the opposite.' },
      { echo: 'too few U-boats',
        t: 'Germany had too few U-boats to keep the sinkings up.',
        fb: 'The U-boats went on sinking ships into 1918. What beat them was the convoy system from May 1917, and by then Germany had made its worst enemy.' }
    ],
    had: 'Force Britain out before America arrives.',
    clock: 'Nine weeks: the USA declared war, 6 April.',
    move: 'The 870,000 tons started that clock.'
  }
  ];

  /* ---- mount ----------------------------------------------------------- */
  /* ctx.reducedMotion needs no branch: nothing here transitions, animates or
     runs on a timer, so nothing moves unasked. */
  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = ctx.accent ||
      (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';

    var wrap = document.createElement('div');
    wrap.className = 'svw-tsv';
    wrap.style.setProperty('--t-acc', accent);

    var style = document.createElement('style');
    style.textContent = CSS;
    wrap.appendChild(style);

    wrap.insertAdjacentHTML('beforeend',
      '<p class="t-kick">Tactics and strategy</p>' +
      '<p class="t-title">The two scoreboards</p>' +
      '<p class="t-frame">A war runs two scoreboards: the fighting, and how close a side is ' +
      'to its war aim. Judge the second from the first.</p>' +
      '<div class="t-stage">' +
        '<p class="t-board">Scoreboard 1 — the fighting</p>' +
        '<p class="t-ep"><span class="t-when" id="twhen"></span> <span id="tep"></span></p>' +
        '<div id="tled"></div>' +
        '<div class="t-two" id="ttwo">' +
          '<p class="t-2h">Scoreboard 2 — the war</p>' +
          '<div class="t-2grid">' +
            '<p class="t-2v"><span class="t-2k" id="thadk"></span><span id="thad"></span></p>' +
            '<p class="t-2v"><span class="t-2k">The clock</span><span id="tclock"></span></p>' +
          '</div>' +
          '<p class="t-2m" id="tmove"></p>' +
        '</div>' +
      '</div>' +
      '<div class="t-ask" id="task">' +
        '<p class="t-gh" id="tgh1"><span class="t-chip">1</span><span id="tq1"></span></p>' +
        '<div class="t-scale" id="tv" role="group" aria-labelledby="tq1"></div>' +
        '<p class="t-gh sleep" id="tgh2"><span class="t-chip">2</span><span>What decides it?</span></p>' +
        '<div class="t-opts" id="tr" role="group" aria-labelledby="tgh2"></div>' +
      '</div>' +
      '<div class="t-fb" id="tfb">' +
        '<span class="t-flag" id="tflag"></span>' +
        '<p class="t-say" id="tsay"></p>' +
      '</div>' +
      '<div class="t-act"><p class="t-run" id="trun"></p>' +
        '<button type="button" class="t-go" id="tgo" disabled>Check</button></div>' +
      '<p class="t-sr" id="tsr" aria-live="polite"></p>');

    root.appendChild(wrap);

    var elWhen  = wrap.querySelector('#twhen');
    var elEp    = wrap.querySelector('#tep');
    var elLed   = wrap.querySelector('#tled');
    var elTwo   = wrap.querySelector('#ttwo');
    var elHadK  = wrap.querySelector('#thadk');
    var elHad   = wrap.querySelector('#thad');
    var elClock = wrap.querySelector('#tclock');
    var elMove  = wrap.querySelector('#tmove');
    var elAsk   = wrap.querySelector('#task');
    var elQ1    = wrap.querySelector('#tq1');
    var elGh2   = wrap.querySelector('#tgh2');
    var elFb    = wrap.querySelector('#tfb');
    var elFlag  = wrap.querySelector('#tflag');
    var elSay   = wrap.querySelector('#tsay');
    var elRun   = wrap.querySelector('#trun');
    var elGo    = wrap.querySelector('#tgo');
    var elSr    = wrap.querySelector('#tsr');

    /* four ledger rows, built once and refilled each round */
    var kCells = [], vCells = [], i, r, sp;
    for (i = 0; i < 4; i++) {
      r = document.createElement('div');
      r.className = 't-row';
      sp = document.createElement('span'); sp.className = 't-k'; r.appendChild(sp); kCells.push(sp);
      sp = document.createElement('span'); sp.className = 't-v'; r.appendChild(sp); vCells.push(sp);
      elLed.appendChild(r);
    }

    function makeRow(host, fn) {
      var out = [], b, n;
      for (n = 0; n < 3; n++) {
        b = document.createElement('button');
        b.type = 'button';
        b.className = 't-opt';
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', fn);
        host.appendChild(b);
        out.push(b);
      }
      return out;
    }

    var vBtns = makeRow(wrap.querySelector('#tv'), onVerdict);
    var rBtns = makeRow(wrap.querySelector('#tr'), onReason);
    for (i = 0; i < 3; i++) vBtns[i].textContent = VERDICTS[i].label;

    var state = { streak: 0, mastered: false, attempted: 0 };
    var order = [], cursor = 0, round = null;
    var rShown = [], vPick = -1, rPick = -1, revealed = false;

    function shuffle(a) {
      for (var j = a.length - 1; j > 0; j--) {
        var k = Math.floor(Math.random() * (j + 1)), t = a[j]; a[j] = a[k]; a[k] = t;
      }
      return a;
    }

    function nextRound() {
      if (cursor >= order.length) {
        var last = order.length ? order[order.length - 1] : -1;
        order = shuffle(ROUNDS.map(function (_, n) { return n; }));
        if (order[0] === last && order.length > 1) {
          var sw = order[0]; order[0] = order[1]; order[1] = sw;
        }
        cursor = 0;
      }
      round = ROUNDS[order[cursor++]];
      rShown = shuffle(round.rs.slice());
      vPick = -1; rPick = -1; revealed = false;

      elWhen.textContent = round.when;
      elEp.textContent = round.ep;
      for (var n = 0; n < 4; n++) {
        kCells[n].textContent = round.led[n][0];
        vCells[n].textContent = round.led[n][1];
      }
      elQ1.textContent = 'Where does this leave ' + round.side + '?';
      for (n = 0; n < 3; n++) {
        vBtns[n].setAttribute('aria-pressed', 'false');
        rBtns[n].textContent = rShown[n].t;
        rBtns[n].setAttribute('aria-pressed', 'false');
        rBtns[n].disabled = true;
      }
      elGh2.className = 't-gh sleep';
      elTwo.classList.remove('on');
      elAsk.classList.remove('off');
      elFb.classList.remove('on');
      elGo.textContent = 'Check';
      elGo.disabled = true;
      publish();
    }

    function onVerdict(ev) {
      if (revealed) return;
      var b = ev.currentTarget;
      vPick = vBtns.indexOf(b);
      for (var n = 0; n < 3; n++) {
        vBtns[n].setAttribute('aria-pressed', vBtns[n] === b ? 'true' : 'false');
        rBtns[n].disabled = false;
      }
      elGh2.className = 't-gh';
      elGo.disabled = (rPick < 0);
      publish();
    }

    function onReason(ev) {
      if (revealed) return;
      var b = ev.currentTarget;
      rPick = rBtns.indexOf(b);
      for (var n = 0; n < 3; n++) {
        rBtns[n].setAttribute('aria-pressed', rBtns[n] === b ? 'true' : 'false');
      }
      elGo.disabled = (vPick < 0);
      publish();
    }

    function clearPicks() {
      vPick = -1; rPick = -1;
      for (var n = 0; n < 3; n++) {
        vBtns[n].setAttribute('aria-pressed', 'false');
        rBtns[n].setAttribute('aria-pressed', 'false');
        rBtns[n].disabled = true;
      }
      elGh2.className = 't-gh sleep';
      elGo.disabled = true;
      publish();
    }

    function reveal() {
      revealed = true;
      state.attempted++;
      var vSel = VERDICTS[vPick], rSel = rShown[rPick];
      var vOk = vSel.id === round.v, rOk = !!rSel.ok;
      var right = vOk && rOk;

      if (right) {
        state.streak++;
        if (state.streak >= 3) state.mastered = true;
      } else {
        state.streak = 0;
      }

      /* One clause, chosen by the bigger error: a wrong verdict is corrected
         first, and only a right verdict lets the decider be the lesson. */
      var body = right ? round.vfb[round.v]
               : (vOk ? rSel.fb : round.vfb[vSel.id]);

      elFlag.textContent = right ? 'Right' : 'Not quite';
      elFlag.className = 't-flag ' + (right ? 'ok' : 'no');
      elSay.textContent = '— you said ' + round.side + ' ' + round.verb + ' ' +
        vSel.echo + ', decided by ' + rSel.echo + '. ' + body +
        (right && state.streak === 3 ? ' You read the aim and the clock, not the count.' : '');

      elHadK.textContent = 'What ' + round.side + ' had to do';
      elHad.textContent = round.had;
      elClock.textContent = round.clock;
      elMove.textContent = round.move;
      elTwo.classList.add('on');
      elAsk.classList.add('off');
      elFb.classList.add('on');

      if (state.streak >= 3) {
        elRun.textContent = 'Three in a row — you have it.';
        elGo.textContent = 'Another anyway';
      } else if (right) {
        elRun.textContent = state.streak === 1
          ? '1 right in a row — two more.'
          : '2 right in a row — one more.';
        elGo.textContent = 'Next episode';
      } else {
        elRun.textContent = state.attempted > 1 ? 'Run back to nought.' : '';
        elGo.textContent = 'Next episode';
      }
      elSr.textContent = (right ? 'Right. ' : 'Not quite. ') + elSay.textContent;
      publish();
    }

    elGo.addEventListener('click', function () {
      if (!revealed) {
        if (vPick < 0 || rPick < 0) return;
        reveal();
      } else {
        nextRound();
      }
      elGo.focus();
    });

    wrap.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && !revealed && (vPick >= 0 || rPick >= 0)) clearPicks();
    });

    function publish() {
      root.dataset.svState = JSON.stringify({
        episode: round ? round.id : null,
        side: round ? round.side : null,
        answer: round ? round.v : null,
        verdict: vPick >= 0 ? VERDICTS[vPick].id : null,
        decider: rPick < 0 ? null
               : (rShown[rPick].ok ? 'aim' : (rShown[rPick].mis ? 'count' : 'other')),
        revealed: revealed,
        streak: state.streak,
        mastered: state.mastered,
        attempted: state.attempted
      });
    }

    nextRound();
  }

  window.SVWidget = {
    meta: {
      id: 'tactical-vs-strategic-victory',
      title: 'The two scoreboards',
      teaches: 'Battlefield success and strategic victory are separate scoreboards: each side has its own war aim and its own clock, so the tactical count can climb while the strategic position gets worse.'
    },
    mount: mount
  };
})();
