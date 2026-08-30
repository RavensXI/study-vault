/* ============================================================
   One beat, two loops — the heart as a double pump.

   Everything the widget says or marks is derived from ROUTE, the single
   circulation model below: vena cava -> right atrium -> right ventricle
   -> pulmonary artery -> lungs -> pulmonary vein -> left atrium ->
   left ventricle -> aorta -> body -> (back to the vena cava).

   The tracked cell always carries a partner cell exactly five stations
   ahead, i.e. half a lap. That single invariant is what makes the
   simultaneity visible: whenever the tracked cell leaves one ventricle,
   the partner leaves the other, on the same squeeze.
   ============================================================ */
(function () {
  'use strict';

  var ID = 'heart-simultaneous-double-circulation';
  var CLS = 'svw-heartdc';

  /* ---------------------------------------------------------- model */

  var ROUTE = [
    { id: 'vena-cava',        name: 'the vena cava',        chamber: false, at: [30, 105] },
    { id: 'right-atrium',     name: 'the right atrium',     chamber: true,  at: [89, 58] },
    { id: 'right-ventricle',  name: 'the right ventricle',  chamber: true,  at: [89, 99] },
    { id: 'pulmonary-artery', name: 'the pulmonary artery', chamber: false, at: [52, 78] },
    { id: 'lungs',            name: 'the lungs',            chamber: false, at: [124, 11] },
    { id: 'pulmonary-vein',   name: 'the pulmonary vein',   chamber: false, at: [248, 26] },
    { id: 'left-atrium',      name: 'the left atrium',      chamber: true,  at: [211, 58] },
    { id: 'left-ventricle',   name: 'the left ventricle',   chamber: true,  at: [211, 99] },
    { id: 'aorta',            name: 'the aorta',            chamber: false, at: [272, 118] },
    { id: 'body',             name: 'the body',             chamber: false, at: [124, 144] }
  ];
  var N = ROUTE.length;
  var HALF = 5;                     /* half a lap: the partner cell's offset */

  /* waypoints for the hop from station i to station i+1 (end point last) */
  var LEGS = [
    [[30, 58], [89, 58]],
    [[89, 99]],
    [[52, 99], [52, 78]],
    [[52, 11], [124, 11]],
    [[248, 11], [248, 26]],
    [[248, 58], [211, 58]],
    [[211, 99]],
    [[272, 99], [272, 118]],
    [[272, 144], [124, 144]],
    [[30, 144], [30, 105]]
  ];

  function idx(id) {
    for (var i = 0; i < N; i++) { if (ROUTE[i].id === id) return i; }
    return -1;
  }
  function stepsTo(from, to) { return (to - from + N) % N; }
  function oxygenated(i) { return i >= 4 && i <= 8; }
  function Cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  /* ------------------------------------------------------- questions */
  /* Route questions name four stations; which one is reached first is
     computed from ROUTE, never authored, so the reveal cannot contradict
     the marking. */

  var ROUTE_Q = [
    {
      start: 'right-ventricle',
      pool: ['lungs', 'aorta', 'left-ventricle', 'body'],
      mech: 'It leaves through the pulmonary artery. On that same squeeze the left ventricle sent blood to the body.',
      diag: {
        'aorta': 'The aorta leaves the left ventricle; blood from the right side must go through the lungs first.',
        'left-ventricle': 'Blood never crosses the septum. It reaches the left side only after the lungs.',
        'body': 'The body is fed by the left side. This cell still has to collect its oxygen.'
      }
    },
    {
      start: 'left-ventricle',
      pool: ['lungs', 'body', 'right-atrium', 'pulmonary-vein'],
      mech: 'It leaves through the aorta. On that same squeeze the right ventricle sent blood to the lungs.',
      diag: {
        'lungs': 'The lungs are fed by the right ventricle. This blood is already oxygenated.',
        'right-atrium': 'It gets there, but only after the body — blood passes the heart twice a lap.',
        'pulmonary-vein': 'The pulmonary vein brings blood from the lungs into the left atrium. This cell has just left the heart.'
      }
    },
    {
      start: 'lungs',
      pool: ['left-atrium', 'right-atrium', 'aorta', 'body'],
      mech: 'It returns through the pulmonary vein. Out on the right, back in on the left — that is the loop.',
      diag: {
        'right-atrium': 'Blood does not return to the side it left from. The right atrium takes blood from the body.',
        'aorta': 'Two steps further on: left atrium, then left ventricle, then the aorta.',
        'body': 'It must be pumped again first. Blood from the lungs goes back into the heart before the body.'
      }
    },
    {
      start: 'body',
      pool: ['right-atrium', 'left-atrium', 'lungs', 'aorta'],
      mech: 'It returns through the vena cava. Deoxygenated blood always comes back to the right side.',
      diag: {
        'left-atrium': 'The left atrium takes blood from the lungs. Blood from the body arrives on the right.',
        'lungs': 'Not straight there. The right side of the heart has to pump it to the lungs.',
        'aorta': 'The aorta carries blood away from the heart, never back into it.'
      }
    },
    {
      start: 'vena-cava',
      pool: ['right-ventricle', 'right-atrium', 'lungs', 'left-atrium'],
      mech: 'The vena cava empties into the right atrium; the valve below it stops blood running back from the ventricle.',
      diag: {
        'right-ventricle': 'One step too far. The atrium fills first, then pushes blood down into the ventricle.',
        'lungs': 'The lungs come later. The right side of the heart has to pump it there.',
        'left-atrium': 'The left atrium receives blood from the lungs, not from the vena cava.'
      }
    },
    {
      start: 'pulmonary-artery',
      pool: ['lungs', 'body', 'left-ventricle', 'right-atrium'],
      mech: 'An artery carries blood away from the heart — this is the one artery carrying deoxygenated blood.',
      diag: {
        'body': 'That is the aorta. The pulmonary artery only ever goes to the lungs.',
        'left-ventricle': 'The left ventricle comes later, after the lungs and the left atrium.',
        'right-atrium': 'That is behind it. This blood has already been pumped out of the heart.'
      }
    }
  ];

  var MEANWHILE_Q = [
    {
      at: 'left-ventricle',
      ask: 'The left ventricle squeezes blood into the aorta. At that same instant the right ventricle is…',
      right: 'the right ventricle is squeezing too, into the pulmonary artery. One beat, both pumps: lungs and body are fed at the same instant.',
      opts: [
        { t: 'Squeezing too, into the pulmonary artery', ok: true },
        { t: 'Resting — the sides take it in turns', d: 'Both ventricles are one muscle: they never take turns.' },
        { t: 'Filling — it squeezes on the next beat', d: 'It filled before this beat. Both ventricles fill and empty together.' },
        { t: 'Empty — it squeezed a moment earlier', d: 'No delay between the sides: right and left squeeze on the same beat.' }
      ],
      truth: 'It is squeezing too, into the pulmonary artery.'
    },
    {
      at: 'right-atrium',
      ask: 'Blood from the vena cava is filling the right atrium. At that instant the left atrium is…',
      right: 'the left atrium is filling too, from the pulmonary vein. Both atria fill together, then both ventricles empty together.',
      opts: [
        { t: 'Filling too, from the pulmonary vein', ok: true },
        { t: 'Empty — waiting for the right side', d: 'Nothing waits its turn: both atria fill at once, from different veins.' },
        { t: 'Squeezing into the left ventricle', d: 'The two atria act together, so they contract together as well.' },
        { t: 'Taking that blood through the septum', d: 'The septum is a solid wall — blood never crosses it inside the heart.' }
      ],
      truth: 'It is filling too, from the pulmonary vein.'
    },
    {
      at: 'right-ventricle',
      ask: 'Both ventricles are squeezing at once. At that same instant the two atria are…',
      right: 'the atria are relaxed and refilling. Left and right act together; it is upper and lower that take turns.',
      opts: [
        { t: 'Relaxed, filling for the next beat', ok: true },
        { t: 'Squeezing as well — all four at once', d: 'Atria and ventricles alternate, so all four never squeeze together.' },
        { t: 'Squeezing one after the other', d: 'Left and right never alternate: both atria act as one.' },
        { t: 'Sealed shut until the next beat', d: 'They are filling, not sealed — blood is arriving from both veins.' }
      ],
      truth: 'They are relaxed and refilling.'
    },
    {
      at: 'left-ventricle',
      ask: 'One heartbeat pushes blood out of the heart. In that single beat, blood leaves…',
      right: 'both ventricles empty on the same beat — right to the lungs, left to the body. That is what a double circulation means.',
      opts: [
        { t: 'Both ventricles — to lungs and body', ok: true },
        { t: 'The right ventricle, then the left', d: 'Not one then the other. Both empty on the same beat, to different places.' },
        { t: 'The left ventricle only', d: 'The right ventricle is emptying too, into the pulmonary artery.' },
        { t: 'All four chambers at once', d: 'Not all four. The atria are relaxed and filling while the ventricles squeeze.' }
      ],
      truth: 'Both ventricles empty on that one beat.'
    }
  ];

  /* build the pool: every route answer computed from ROUTE */
  function buildPool() {
    var pool = [], i, j;
    for (i = 0; i < ROUTE_Q.length; i++) {
      var q = ROUTE_Q[i], s = idx(q.start), best = -1, bestD = 99;
      for (j = 0; j < q.pool.length; j++) {
        var d = stepsTo(s, idx(q.pool[j]));
        if (d > 0 && d < bestD) { bestD = d; best = j; }
      }
      var opts = [];
      for (j = 0; j < q.pool.length; j++) {
        opts.push({
          t: Cap(ROUTE[idx(q.pool[j])].name),
          ok: j === best,
          d: q.diag[q.pool[j]] || ''
        });
      }
      pool.push({
        kind: 'route', id: 'r' + i, at: q.start, hops: bestD,
        ask: 'The tracked cell is in ' + ROUTE[s].name + ' now. Which of these does it reach <strong>first</strong>?',
        right: 'from ' + ROUTE[s].name + ' the cell reaches ' + ROUTE[idx(q.pool[best])].name + ' first. ' + q.mech,
        truth: 'It reaches ' + ROUTE[idx(q.pool[best])].name + ' first.',
        opts: opts
      });
    }
    for (i = 0; i < MEANWHILE_Q.length; i++) {
      var m = MEANWHILE_Q[i];
      pool.push({
        kind: 'meanwhile', id: 'm' + i, at: m.at, hops: 1,
        ask: m.ask, right: m.right, truth: m.truth, opts: m.opts.slice()
      });
    }
    return pool;
  }

  /* ------------------------------------------------------------- css */

  function css(accent, reduced) {
    var a = accent;
    return [
      '.' + CLS + '{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4}',
      '.' + CLS + ' *{box-sizing:border-box}',
      '.' + CLS + ' .kick{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + a + '}',
      '.' + CLS + ' .ttl{margin:.12rem 0 .18rem;font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.15}',
      '.' + CLS + ' .scn{margin:0;font-size:.8rem;color:#8d8880}',
      '.' + CLS + ' .ask{margin:.3rem 0 0;font-size:.84rem;line-height:1.42}',
      '.' + CLS + ' .ask strong{font-weight:700}',
      '.' + CLS + ' .main{display:grid;grid-template-columns:1fr;gap:.5rem;margin-top:.5rem}',
      '.' + CLS + '.wide .main{grid-template-columns:minmax(300px,1.05fr) minmax(230px,1fr);gap:.9rem;align-items:center}',
      '.' + CLS + ' .stagewrap{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.2rem;max-width:330px;width:100%;margin:0 auto}',
      '.' + CLS + '.wide .stagewrap{max-width:360px}',
      '.' + CLS + ' svg{display:block;width:100%;height:auto}',
      '.' + CLS + ' .opts{display:grid;grid-template-columns:1fr;gap:.3rem}',
      '.' + CLS + ' .opt{font:inherit;font-size:.8rem;font-weight:600;text-align:left;padding:.34rem .6rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;cursor:pointer;display:flex;gap:.4rem;align-items:baseline}',
      '.' + CLS + ' .opt .mk{font-size:.78rem;font-weight:700;width:.7rem;flex:none;color:#8d8880}',
      '.' + CLS + ' .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
      '.' + CLS + ' .opt[aria-pressed="true"] .mk{color:#fff}',
      '.' + CLS + ' .opt.ok{background:#fff;border-color:#4f7d63;color:#33553f}',
      '.' + CLS + ' .opt.ok .mk{color:#4f7d63}',
      '.' + CLS + ' .opt.no{background:#fff;border-color:#ddd7cd;color:#8d8880}',
      '.' + CLS + ' .act{display:flex;align-items:center;justify-content:space-between;gap:.5rem;margin-top:.4rem}',
      '.' + CLS + ' .go{font:inherit;font-size:.82rem;font-weight:600;padding:.42rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
      '.' + CLS + ' .go[disabled]{background:#faf8f5;border-color:#ddd7cd;color:#a8a29a;cursor:default}',
      '.' + CLS + ' .run{font-size:.75rem;color:#8d8880;font-variant-numeric:tabular-nums;text-align:right}',
      '.' + CLS + ' .cap{margin:.5rem 0 0;font-size:.82rem;line-height:1.45;color:#2d2a26;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.45rem .6rem;min-height:5.8rem}',
      '.' + CLS + '.mid .cap,.' + CLS + '.wide .cap{min-height:4.6rem}',
      '.' + CLS + ' .cap strong{font-weight:700}',
      '.' + CLS + ' .sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
      /* diagram */
      '.' + CLS + ' .organ{fill:#fff;stroke:#d9d2c7;stroke-width:1.4}',
      '.' + CLS + ' .organ-t{font-size:11px;font-weight:600;fill:#5b564e;text-anchor:middle;font-family:Inter,system-ui,sans-serif}',
      '.' + CLS + ' .ch-t{font-size:10px;font-weight:600;fill:#5b564e;text-anchor:middle;font-family:Inter,system-ui,sans-serif}',
      '.' + CLS + ' .ves-t{font-size:10px;font-weight:600;fill:#8d8880;text-anchor:middle;font-family:Inter,system-ui,sans-serif}',
      '.' + CLS + ' .ves{fill:none;stroke-width:5;stroke-linecap:round;stroke-linejoin:round}',
      '.' + CLS + ' .halo{fill:none;stroke:#faf8f5;stroke-width:11;stroke-linecap:round;stroke-linejoin:round}',
      '.' + CLS + ' .deox{stroke:#4a6fa5}',
      '.' + CLS + ' .ox{stroke:#b0453a}',
      '.' + CLS + ' .arrow{fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}',
      '.' + CLS + ' .valve{fill:none;stroke:#b3aca0;stroke-width:1.6;stroke-linecap:round}',
      '.' + CLS + ' .chamber{stroke-width:1.8;transform-box:fill-box;transform-origin:center}',
      '.' + CLS + ' .chamber.thick{stroke-width:4.5}',
      '.' + CLS + ' .r-side{fill:#eef3f9;stroke:#4a6fa5}',
      '.' + CLS + ' .l-side{fill:#fbeeec;stroke:#b0453a}',
      '.' + CLS + ' .chamber.squeeze{transform:scale(.9)}',
      '.' + CLS + ' .cell circle{stroke-width:0}',
      '.' + CLS + ' .cell:not(.mark) circle{opacity:.4}',
      '.' + CLS + ' .cell.mark circle{stroke:' + a + ';stroke-width:2.8}',
      '.' + CLS + ' .cell.mark .halo-c{stroke:#faf8f5;stroke-width:2;fill:none}',
      reduced ? '' :
        '.' + CLS + ' .chamber{transition:transform .18s ease}' +
        '.' + CLS + ' .cell{transition:transform .2s linear}'
    ].join('\n');
  }

  /* ------------------------------------------------------------ svg */

  function svgMarkup() {
    var s = '';
    s += '<svg viewBox="0 0 300 154" role="img" aria-label="Diagram of the double circulation">';
    /* organs */
    s += '<rect class="organ" x="110" y="1" width="80" height="20" rx="8"/>';
    s += '<text class="organ-t" x="150" y="15">Lungs</text>';
    s += '<rect class="organ" x="110" y="134" width="80" height="20" rx="8"/>';
    s += '<text class="organ-t" x="150" y="148">Body</text>';
    /* vessels: vena cava first, pulmonary artery drawn over it with a
       halo — the pulmonary trunk really does pass in front */
    s += '<path class="ves deox" d="M110,144 H30 V58 H76"/>';
    s += '<path class="halo" d="M76,99 H52 V11 H110"/>';
    s += '<path class="ves deox" d="M76,99 H52 V11 H110"/>';
    s += '<path class="ves ox" d="M190,11 H248 V58 H224"/>';
    s += '<path class="ves ox" d="M224,99 H272 V144 H190"/>';
    /* direction */
    s += '<path class="arrow deox" d="M26,92 L30,84 L34,92"/>';
    s += '<path class="arrow deox" d="M48,34 L52,26 L56,34"/>';
    s += '<path class="arrow ox" d="M244,40 L248,48 L252,40"/>';
    s += '<path class="arrow ox" d="M268,132 L272,140 L276,132"/>';
    /* heart */
    s += '<rect class="organ" x="76" y="45" width="148" height="74" rx="10"/>';
    s += '<line x1="150" y1="45" x2="150" y2="119" stroke="#d9d2c7" stroke-width="2"/>';
    s += '<rect id="ra" class="chamber r-side" x="80" y="49" width="68" height="31" rx="6"/>';
    s += '<rect id="rv" class="chamber r-side" x="80" y="84" width="68" height="31" rx="6"/>';
    s += '<rect id="la" class="chamber l-side" x="152" y="49" width="68" height="31" rx="6"/>';
    s += '<rect id="lv" class="chamber l-side thick" x="152" y="84" width="68" height="31" rx="6"/>';
    s += '<path class="valve" d="M106,80 L114,84 M132,84 L140,80"/>';
    s += '<path class="valve" d="M178,80 L186,84 M204,84 L212,80"/>';
    s += '<text class="ch-t" x="121" y="61">Right</text><text class="ch-t" x="121" y="73">atrium</text>';
    s += '<text class="ch-t" x="121" y="96">Right</text><text class="ch-t" x="121" y="108">ventricle</text>';
    s += '<text class="ch-t" x="183" y="61">Left</text><text class="ch-t" x="183" y="73">atrium</text>';
    s += '<text class="ch-t" x="183" y="96">Left</text><text class="ch-t" x="183" y="108">ventricle</text>';
    /* vessel names */
    s += '<text class="ves-t" x="98" y="31">Pulmonary</text><text class="ves-t" x="98" y="42">artery</text>';
    s += '<text class="ves-t" x="202" y="31">Pulmonary</text><text class="ves-t" x="202" y="42">vein</text>';
    s += '<text class="ves-t" x="58" y="131">Vena cava</text>';
    s += '<text class="ves-t" x="250" y="131">Aorta</text>';
    /* cells */
    s += '<g id="partner" class="cell"><circle r="5"/></g>';
    s += '<g id="tracked" class="cell mark"><circle r="6"/><circle class="halo-c" r="8.2"/></g>';
    s += '</svg>';
    return s;
  }

  /* ----------------------------------------------------------- mount */

  window.SVWidget = {
    meta: {
      id: ID,
      title: 'One beat, two loops',
      teaches: 'Both sides of the heart contract on the same beat, driving two circuits at once, so blood passes through the heart twice on each lap of the body.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || getComputedStyle(root).getPropertyValue('--accent').trim() || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;

      var pool = buildPool();
      var order = [], queued = 0;
      var q = null, picked = -1, committed = false, lastCorrect = null;
      var streak = 0, attempted = 0, mastered = false;
      var trackedIdx = 0, timers = [];

      /* ---- DOM, built once ---- */
      var box = document.createElement('div');
      box.className = CLS;
      var style = document.createElement('style');
      style.textContent = css(accent, reduced);
      box.appendChild(style);

      var head = document.createElement('div');
      head.innerHTML =
        '<p class="kick">Circulatory system</p>' +
        '<h3 class="ttl">One beat, two loops</h3>' +
        '<p class="scn">Track one red blood cell round the circuit.</p>' +
        '<p class="ask"></p>';
      box.appendChild(head);
      var askEl = head.querySelector('.ask');

      var main = document.createElement('div');
      main.className = 'main';
      var stage = document.createElement('div');
      stage.className = 'stagewrap';
      stage.innerHTML = svgMarkup();
      var panel = document.createElement('div');
      var optsEl = document.createElement('div');
      optsEl.className = 'opts';
      var act = document.createElement('div');
      act.className = 'act';
      var goBtn = document.createElement('button');
      goBtn.type = 'button';
      goBtn.className = 'go';
      goBtn.textContent = 'Check';
      var runEl = document.createElement('span');
      runEl.className = 'run';
      act.appendChild(goBtn);
      act.appendChild(runEl);
      panel.appendChild(optsEl);
      panel.appendChild(act);
      main.appendChild(stage);
      main.appendChild(panel);
      box.appendChild(main);

      var capEl = document.createElement('p');
      capEl.className = 'cap';
      box.appendChild(capEl);
      var srEl = document.createElement('p');
      srEl.className = 'sr';
      srEl.setAttribute('aria-live', 'polite');
      box.appendChild(srEl);

      var optBtns = [];
      for (var i = 0; i < 4; i++) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'opt';
        b.setAttribute('aria-pressed', 'false');
        b.innerHTML = '<span class="mk" aria-hidden="true"></span><span class="tx"></span>';
        optsEl.appendChild(b);
        optBtns.push(b);
        (function (n) {
          b.addEventListener('click', function () { pick(n); });
        })(i);
      }
      root.appendChild(box);

      var svg = stage.querySelector('svg');
      var gTracked = svg.querySelector('#tracked');
      var gPartner = svg.querySelector('#partner');
      var chambers = {
        1: svg.querySelector('#ra'), 2: svg.querySelector('#rv'),
        6: svg.querySelector('#la'), 7: svg.querySelector('#lv')
      };

      /* ---- width class, resolved synchronously then watched ---- */
      function fit() {
        var w = root.clientWidth || box.clientWidth || 0;
        box.classList.toggle('wide', w >= 620);
        box.classList.toggle('mid', w >= 470);
      }
      fit();
      if (window.ResizeObserver) {
        var ro = new ResizeObserver(fit);
        ro.observe(root);
      }

      /* ---- cell placement ---- */
      function paint(i) {
        var col = oxygenated(i) ? '#b0453a' : '#4a6fa5';
        gTracked.firstChild.setAttribute('fill', col);
        var p = (i + HALF) % N;
        gPartner.firstChild.setAttribute('fill', oxygenated(p) ? '#b0453a' : '#4a6fa5');
      }
      function place(i, animate) {
        var p = (i + HALF) % N;
        if (!animate) {
          gTracked.style.transition = 'none';
          gPartner.style.transition = 'none';
        }
        gTracked.setAttribute('transform', 'translate(' + ROUTE[i].at[0] + ',' + ROUTE[i].at[1] + ')');
        gPartner.setAttribute('transform', 'translate(' + ROUTE[p].at[0] + ',' + ROUTE[p].at[1] + ')');
        paint(i);
      }
      function clearTimers() {
        for (var t = 0; t < timers.length; t++) { clearTimeout(timers[t]); }
        timers = [];
      }
      function later(fn, ms) { timers.push(setTimeout(fn, ms)); }

      /* Walk both cells forward `hops` stations. Every hop out of a
         chamber squeezes BOTH chambers of that pair at once — the
         partner is half a lap away, so it is always the mirror one. */
      function advance(hops, done) {
        if (reduced) {
          trackedIdx = (trackedIdx + hops) % N;
          place(trackedIdx, false);
          if (done) done();
          return;
        }
        var D = 520;
        function hop(k) {
          if (!root.isConnected) return;
          if (k >= hops) { if (done) done(); return; }
          var from = trackedIdx;
          if (ROUTE[from].chamber) {
            var pair = (from === 1 || from === 6) ? [1, 6] : [2, 7];
            chambers[pair[0]].classList.add('squeeze');
            chambers[pair[1]].classList.add('squeeze');
            later(function () {
              chambers[pair[0]].classList.remove('squeeze');
              chambers[pair[1]].classList.remove('squeeze');
            }, D * 0.55);
          }
          runLegs(gTracked, from, D);
          runLegs(gPartner, (from + HALF) % N, D);
          trackedIdx = (from + 1) % N;
          later(function () { paint(trackedIdx); hop(k + 1); }, D);
        }
        hop(0);
      }
      function runLegs(g, from, D) {
        var legs = LEGS[from], per = D / legs.length;
        g.style.transition = 'transform ' + per + 'ms linear';
        legs.forEach(function (pt, n) {
          later(function () {
            if (!root.isConnected) return;
            g.setAttribute('transform', 'translate(' + pt[0] + ',' + pt[1] + ')');
          }, n * per);
        });
      }

      /* ---- state ---- */
      function publish() {
        root.dataset.svState = JSON.stringify({
          question: q ? q.id : null,
          picked: picked,
          committed: committed,
          correct: lastCorrect,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        });
      }

      function nextQuestion() {
        clearTimers();
        if (!order.length) {
          order = pool.slice();
          for (var k = order.length - 1; k > 0; k--) {
            var j = Math.floor(Math.random() * (k + 1)), tmp = order[k];
            order[k] = order[j]; order[j] = tmp;
          }
          /* never repeat the question just answered */
          if (q && order[0] === q && order.length > 1) {
            order.push(order.shift());
          }
        }
        q = order.shift();
        queued++;
        picked = -1;
        committed = false;
        lastCorrect = null;
        askEl.innerHTML = q.ask;
        var shuffled = q.opts.slice();
        for (var m = shuffled.length - 1; m > 0; m--) {
          var r = Math.floor(Math.random() * (m + 1)), s = shuffled[m];
          shuffled[m] = shuffled[r]; shuffled[r] = s;
        }
        q.shown = shuffled;
        for (var o = 0; o < optBtns.length; o++) {
          var btn = optBtns[o];
          btn.className = 'opt';
          btn.setAttribute('aria-pressed', 'false');
          btn.querySelector('.tx').textContent = shuffled[o].t;
          btn.querySelector('.mk').textContent = '';
          btn.disabled = false;
        }
        goBtn.textContent = 'Check';
        goBtn.disabled = true;
        trackedIdx = idx(q.at);
        place(trackedIdx, false);
        capEl.innerHTML = attempted === 0
          ? 'Drawn as the patient faces you, so the heart’s <strong>right side is on the left</strong> of the picture. Blue is deoxygenated, red is oxygenated. The pale cell is a second cell, half a lap ahead.'
          : 'The tracked cell is in <strong>' + ROUTE[trackedIdx].name.replace('the ', '') + '</strong>. The pale cell shows where blood on the other side is at the same instant.';
        publish();
      }

      function pick(n) {
        if (committed) return;
        picked = n;
        for (var o = 0; o < optBtns.length; o++) {
          optBtns[o].setAttribute('aria-pressed', o === n ? 'true' : 'false');
        }
        goBtn.disabled = false;
        publish();
      }

      function commit() {
        if (picked < 0) return;
        committed = true;
        attempted++;
        var chosen = q.shown[picked];
        var right = !!chosen.ok;
        lastCorrect = right;
        streak = right ? streak + 1 : 0;
        var justMastered = false;
        if (streak >= 3 && !mastered) { mastered = true; justMastered = true; }

        for (var o = 0; o < optBtns.length; o++) {
          var btn = optBtns[o], op = q.shown[o];
          btn.setAttribute('aria-pressed', 'false');
          btn.className = 'opt' + (op.ok ? ' ok' : (o === picked ? ' no' : ''));
          btn.querySelector('.mk').textContent = op.ok ? '✓' : (o === picked ? '✕' : '');
          btn.disabled = true;
        }

        var msg;
        if (right) {
          msg = '<strong>Right —</strong> ' + q.right;
        } else {
          msg = '<strong>Not quite —</strong> you said “' + chosen.t + '”. ' +
                q.truth + ' ' + (chosen.d || '');
        }
        if (justMastered) {
          msg = '<strong>Three in a row — you have it.</strong> The heart is one muscle with two pumps: every beat sends blood to the lungs and to the body at once, so blood passes through the heart twice on one lap.';
        }
        capEl.innerHTML = msg;
        srEl.textContent = (right ? 'Correct. ' : 'Not correct. ') + capEl.textContent;

        runEl.textContent = mastered
          ? 'You have it'
          : (streak === 0
              ? 'Back to 0 — three in a row'
              : streak + ' right in a row' + (streak === 2 ? ' — one more' : ''));

        goBtn.disabled = true;
        advance(q.hops, function () {
          if (!root.isConnected) return;
          goBtn.disabled = false;
        });
        if (reduced) { goBtn.disabled = false; }
        goBtn.textContent = mastered ? 'Another anyway' : 'Next question';
        publish();
      }

      goBtn.addEventListener('click', function () {
        if (committed) { nextQuestion(); goBtn.focus(); }
        else { commit(); }
      });

      nextQuestion();
    }
  };
})();
