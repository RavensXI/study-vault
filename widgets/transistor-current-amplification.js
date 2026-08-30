/* StudyVault lesson widget - transistor-current-amplification
   A small base current controls a much larger collector current that is
   drawn FROM the supply. Below about 0.7 V the transistor is simply off.
   Every number here is computed from the round data; nothing is authored. */
(function () {
  'use strict';

  /* ---------- model ----------
     Currents are held in microamps as integers, so every comparison
     (saturated? off? equal to a distractor?) is exact. */

  var LOADS = {
    lamp: {
      name: 'lamp',
      off: 'the lamp stays dark',
      weak: 'the lamp glows but dim',
      full: 'the lamp at full brightness'
    },
    motor: {
      name: 'motor',
      off: 'the motor stays still',
      weak: 'the motor turns slowly',
      full: 'the motor at full speed'
    },
    relay: {
      name: 'relay',
      off: 'the relay does not click',
      weak: 'not enough to pull the relay in',
      full: 'the relay clicks in'
    }
  };

  /* mode: live | below (signal under the 0.7 V threshold) | nosupply
     ib is the base current the base resistor is sized for; in a below-threshold
     round the junction never conducts, so none of it actually flows. */
  var ROUNDS = [
    { load: 'lamp',  supply: 6,  full: 120000, gain: 200, ib: 400,  vsig: 5,   mode: 'live' },
    { load: 'motor', supply: 12, full: 250000, gain: 150, ib: 2000, vsig: 5,   mode: 'live' },
    { load: 'motor', supply: 12, full: 250000, gain: 200, ib: 500,  vsig: 5,   mode: 'nosupply' },
    { load: 'relay', supply: 9,  full: 60000,  gain: 120, ib: 600,  vsig: 0.4, mode: 'below' },
    { load: 'lamp',  supply: 9,  full: 150000, gain: 250, ib: 200,  vsig: 3.3, mode: 'live' },
    { load: 'relay', supply: 9,  full: 80000,  gain: 250, ib: 600,  vsig: 5,   mode: 'live' },
    { load: 'lamp',  supply: 6,  full: 100000, gain: 180, ib: 800,  vsig: 3.3, mode: 'live' },
    { load: 'motor', supply: 12, full: 200000, gain: 150, ib: 1500, vsig: 0.5, mode: 'below' }
  ];

  /* what the load does on a given collector current */
  function stateOf(ua, full) {
    if (ua <= 0) return 'off';
    if (ua >= full) return 'full';
    return (ua * 4 >= full) ? 'weak' : 'off';
  }

  function solve(r) {
    var demand = r.gain * r.ib;
    if (r.mode !== 'live') return { ic: 0, state: 'off', demand: demand };
    var ic = Math.min(demand, r.full);
    return { ic: ic, state: stateOf(ic, r.full), demand: demand };
  }

  function mAt(ua) {
    var v = ua / 1000;
    var r = Math.round(v);
    return ((Math.abs(v - r) < 1e-9) ? String(r) : v.toFixed(1)) + ' mA';
  }

  /* Correct answer plus the three wrong pictures this widget exists to
     falsify, all derived from the round's own figures. Duplicates collapse,
     which is why a round always shows four genuinely different currents. */
  function optionsFor(r) {
    var m = solve(r), out = [], seen = {};
    function add(ua, tag) {
      if (ua == null || ua < 0 || seen[ua]) return;
      seen[ua] = 1;
      out.push({ ua: ua, tag: tag });
    }
    add(m.ic, 'correct');
    add(r.gain * r.ib, 'multiply');   /* the gain multiplies whatever the circuit does */
    add(r.full, 'switch');            /* a transistor is just an on/off switch */
    add(r.ib, 'passthrough');         /* the signal itself travels on to the load */
    add(0, 'nothing');
    return out.slice(0, 4);
  }

  function frameFor(r, L) {
    if (r.mode === 'nosupply') {
      return 'The supply lead has come off; the signal still feeds ' + mAt(r.ib) +
             ' into the base. Predict the collector current.';
    }
    if (r.mode === 'below') {
      return 'The base resistor is sized for ' + mAt(r.ib) + ', but the signal is only ' + r.vsig +
             ' V — the junction needs 0.7 V. Predict the collector current.';
    }
    return 'A control signal feeds ' + mAt(r.ib) + ' into the base. Predict the collector current,' +
           ' and what the ' + L.name + ' does.';
  }

  function feedback(r, L, m, opt) {
    var V = r.supply + ' V';
    var ib = mAt(r.ib), ic = mAt(m.ic), full = mAt(r.full), dem = mAt(m.demand);
    var o = { right: opt.tag === 'correct', head: '', body: '' };

    if (o.right) {
      o.head = 'Right — ' + ic + ', ' + L[m.state] + '.';
      if (m.state === 'weak') {
        o.body = ' ' + ib + ' × gain ' + r.gain + ' = ' + dem + ', and the ' + L.name + ' can pass ' +
                 full + ', so it all flows — pushed by the ' + V + ' supply, not made by the transistor.';
      } else if (m.state === 'full') {
        o.body = ' The base would allow ' + dem + ', but the ' + V + ' supply and the ' + L.name +
                 ' can only pass ' + full + ', so it saturates there. Gain cannot invent current.';
      } else if (r.mode === 'below') {
        o.body = ' At ' + r.vsig + ' V the base-emitter junction is under the 0.7 V it needs, so no base' +
                 ' current flows at all — and gain ' + r.gain + ' × 0 is still 0.';
      } else {
        o.body = ' The base still takes ' + ib + ' and the gain is still ' + r.gain + ', but with the supply' +
                 ' lead off nothing is pushing current through the ' + L.name + '.';
      }
      return o;
    }

    o.head = 'Not quite — you said ' + mAt(opt.ua) + ', ' + L[stateOf(opt.ua, r.full)] + '.';

    if (opt.tag === 'multiply') {
      if (r.mode === 'nosupply') {
        o.body = ' That is what the transistor would let past, but the current has to come out of the ' + V +
                 ' supply — and the supply lead is off. Collector current: 0 mA.';
      } else if (r.mode === 'below') {
        o.body = ' The design aims for ' + ib + ' at the base, but at ' + r.vsig + ' V the junction is under' +
                 ' 0.7 V, so no base current flows — and ' + r.gain + ' × 0 is 0.';
      } else {
        o.body = ' ' + ib + ' × ' + r.gain + ' = ' + dem + ' is what the transistor would allow, but the ' +
                 V + ' supply and the ' + L.name + ' can only pass ' + full + '. It saturates there.';
      }
    } else if (opt.tag === 'switch') {
      if (r.mode === 'below') {
        o.body = ' A signal that is present is not the same as one that is big enough: at ' + r.vsig +
                 ' V the junction never turns on, so the ' + L.name + ' gets 0 mA.';
      } else if (r.mode === 'nosupply') {
        o.body = ' Nothing is pushing ' + full + ' through the ' + L.name + ': the supply lead is off. The' +
                 ' transistor opens the way for the supply’s current — it is not the source.';
      } else {
        var need = Math.ceil(r.full / r.gain);
        o.body = ' A transistor is not a plain on/off switch: ' + ib + ' × ' + r.gain + ' lets only ' + dem +
                 ' past, so ' + L[m.state] + '. It reaches full at ' + mAt(need) + ' into the base.';
      }
    } else if (opt.tag === 'passthrough') {
      if (m.ic > 0) {
        o.body = ' That is the base current, and it does not travel on into the ' + L.name + '. The two paths' +
                 ' meet at the emitter: ' + ib + ' in at the base, ' + ic + ' down from the supply.';
      } else {
        o.body = ' That is the base current, and it never travels on into the ' + L.name + '. The collector' +
                 ' current comes from the supply — and here it is 0 mA.';
      }
    } else {
      o.body = ' The signal is well above the 0.7 V the junction needs, so ' + ib + ' does flow in and the' +
               ' transistor turns on: ' + ib + ' × ' + r.gain + ' gives ' + ic + ' through the ' + L.name + '.';
    }
    return o;
  }

  /* ---------- style (every selector under .svw-tca) ---------- */
  var CSS = [
    '.svw-tca{--tca-a:#8a6a4f;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;',
    'color:#2d2a26;line-height:1.45}',
    '.svw-tca *{box-sizing:border-box}',
    '.svw-tca .tca-kick{margin:0 0 .15rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;',
    'text-transform:uppercase;color:var(--tca-a)}',
    '.svw-tca .tca-title{margin:0 0 .3rem;font-family:"Source Serif 4",Georgia,serif;font-size:1.15rem;',
    'font-weight:600;line-height:1.25}',
    '.svw-tca .tca-frame{margin:0 0 .6rem;font-size:.84rem;color:#5b564e;min-height:2.9em}',
    '.svw-tca .tca-body{display:flex;flex-wrap:wrap;gap:.65rem;align-items:flex-start}',
    '.svw-tca .tca-stage{flex:1 1 300px;background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;',
    'padding:.35rem .4rem}',
    '.svw-tca .tca-ctrl{flex:1 1 300px}',
    '.svw-tca .tca-svg{display:block;width:100%;max-width:400px;margin:0 auto}',
    '.svw-tca .tca-wire path,.svw-tca .tca-wire circle{fill:none;stroke:#b0a698;stroke-width:1.7;',
    'stroke-linecap:round;stroke-linejoin:round}',
    '.svw-tca .tca-wire circle{fill:#faf8f5}',
    '.svw-tca .tca-ink{fill:none;stroke:#2d2a26;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}',
    '.svw-tca .tca-bar{stroke-width:3}',
    '.svw-tca .tca-fill{fill:#2d2a26}',
    '.svw-tca .tca-acc{fill:var(--tca-a)}',
    '.svw-tca .tca-flow{fill:none;stroke:var(--tca-a);stroke-linecap:round;',
    'stroke-linejoin:round;opacity:.85}',
    '.svw-tca .tca-march{animation:tca-march 1.8s linear infinite}',
    '@keyframes tca-march{to{stroke-dashoffset:-18}}',
    '.svw-tca .tca-lab{fill:#5b564e;font-family:Inter,system-ui,sans-serif;font-size:12px}',
    '.svw-tca .tca-lab tspan{font-size:12px}',
    '.svw-tca .tca-sub{font-size:8.5px}',
    '.svw-tca .tca-glyph{fill:#2d2a26;font-family:Inter,system-ui,sans-serif;font-size:11px;font-weight:600;',
    'text-anchor:middle}',
    '.svw-tca .tca-sig{fill:#5b564e;font-family:Inter,system-ui,sans-serif;font-size:10px;text-anchor:middle}',
    '.svw-tca .tca-hide{display:none}',
    '.svw-tca .tca-opts{display:flex;flex-wrap:wrap;gap:.35rem;margin:0 0 .5rem}',
    '.svw-tca .tca-opt{flex:1 1 260px;display:flex;align-items:baseline;gap:.4rem;text-align:left;',
    'font-family:inherit;font-size:.82rem;font-weight:600;color:#2d2a26;background:#faf8f5;',
    'border:1px solid #ddd7cd;border-radius:10px;padding:.4rem .6rem;cursor:pointer}',
    '.svw-tca .tca-opt:hover:not(:disabled){border-color:#bdb4a5}',
    '.svw-tca .tca-opt .tca-out{font-weight:400;color:#5b564e}',
    '.svw-tca .tca-opt.is-sel{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-tca .tca-opt.is-sel .tca-out{color:#efeae2}',
    '.svw-tca .tca-opt.is-right{border-color:#4f7d63;background:#4f7d6314;color:#2d2a26}',
    '.svw-tca .tca-opt.is-right .tca-out{color:#4f7d63}',
    '.svw-tca .tca-opt.is-miss{border-color:#2d2a26;background:#faf8f5;color:#2d2a26}',
    '.svw-tca .tca-opt .tca-tick{margin-left:auto;color:#4f7d63;font-weight:700}',
    '.svw-tca .tca-opt:disabled{cursor:default}',
    '.svw-tca .tca-act{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap}',
    '.svw-tca .tca-go{font-family:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;',
    'border:1px solid #2d2a26;border-radius:10px;padding:.45rem .95rem;cursor:pointer}',
    '.svw-tca .tca-go:disabled{opacity:.35;cursor:default}',
    '.svw-tca .tca-streak{font-size:.75rem;color:#8d8880}',
    '.svw-tca .tca-cap{margin:.5rem 0 0;font-size:.84rem;line-height:1.5;color:#2d2a26;min-height:4.4em}',
    '.svw-tca .tca-cap .tca-v-right{color:#4f7d63}',
    '.svw-tca .tca-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;',
    'clip:rect(0 0 0 0);white-space:nowrap;border:0}'
  ].join('');

  var SVG = [
    '<svg class="tca-svg" viewBox="0 0 330 132" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">',
    '<path class="tca-flow tca-flow-c" d="M286 12 H188 V22 M188 46 V54 L170 64 M170 84 L188 94 V112 H286 V75 M286 48 V12"/>',
    '<path class="tca-flow tca-flow-b" d="M96 74 H170 M96 108 V112 H188"/>',
    '<g class="tca-wire">',
    '<path d="M286 12 H188 V22"/><path d="M188 46 V54 L170 64"/><path d="M170 84 L188 94 V112"/>',
    '<path d="M96 112 H286"/><path d="M286 112 V75"/>',
    '<path class="tca-sup-on" d="M286 48 V12"/>',
    '<g class="tca-sup-off tca-hide"><path d="M286 48 V40"/><path d="M286 24 V12"/>',
    '<circle cx="286" cy="36" r="3"/><circle cx="286" cy="28" r="3"/></g>',
    '<path d="M96 74 H170"/><path d="M96 74 V90"/><path d="M96 108 V112"/><path d="M140 112 V118"/>',
    '</g>',
    '<path class="tca-ink" d="M140 118 H154 M143 122 H151 M146 126 H148"/>',
    '<rect class="tca-ink" x="104" y="67" width="30" height="14" rx="2" fill="#faf8f5"/>',
    '<rect class="tca-ink" x="78" y="90" width="36" height="18" rx="4" fill="#faf8f5"/>',
    '<text class="tca-sig" x="96" y="102">signal</text>',
    '<path class="tca-ink tca-bar" d="M170 56 V92"/>',
    '<polygon class="tca-fill" points="0,0 -7,-2.7 -7,2.7" transform="translate(186,92.5) rotate(29)"/>',
    '<polygon class="tca-acc tca-ib-arrow" points="0,0 -6,-2.4 -6,2.4" transform="translate(160,74)"/>',
    '<polygon class="tca-acc tca-ic-arrow tca-hide" points="0,0 6,-2.6 6,2.6" transform="translate(232,12)"/>',
    '<g class="tca-batt"><path class="tca-ink" d="M274 50 H298"/><path class="tca-ink" d="M281 57 H291"/>',
    '<path class="tca-ink" d="M274 64 H298"/><path class="tca-ink" d="M281 71 H291"/></g>',
    '<circle class="tca-load-ring" cx="188" cy="34" r="12" fill="#fff" stroke="#2d2a26" stroke-width="1.6"/>',
    '<path class="tca-load-x tca-ink" d="M180.5 26.5 L195.5 41.5 M195.5 26.5 L180.5 41.5" stroke-width="1.4"/>',
    '<text class="tca-glyph tca-load-g tca-hide" x="188" y="38">M</text>',
    '<rect class="tca-load-rect tca-hide" x="176" y="22" width="24" height="24" rx="2" fill="#fff" stroke="#2d2a26" stroke-width="1.6"/>',
    '<path class="tca-load-h tca-ink tca-hide" d="M181 22 V46 M188 22 V46 M195 22 V46" stroke-width="1.2"/>',
    '<text class="tca-lab tca-l-load" x="172" y="29" text-anchor="end">lamp</text>',
    '<text class="tca-lab tca-l-rate" x="172" y="41" text-anchor="end">120 mA full</text>',
    '<text class="tca-lab" x="100" y="64">I<tspan class="tca-sub" dy="2">B</tspan>',
    '<tspan class="tca-l-ib" dy="-2"> = 0.4 mA</tspan></text>',
    '<text class="tca-lab" x="198" y="62">I<tspan class="tca-sub" dy="2">C</tspan>',
    '<tspan class="tca-l-ic" dy="-2"> = ?</tspan></text>',
    '<text class="tca-lab tca-l-gain" x="196" y="100">gain 200</text>',
    '<text class="tca-lab tca-l-v" x="276" y="90" text-anchor="end">9 V</text>',
    '<text class="tca-lab tca-l-sig" x="96" y="126" text-anchor="middle">5 V in</text>',
    '</svg>'
  ].join('');

  var HTML =
    '<style>' + CSS + '</style>' +
    '<p class="tca-kick">Transistor switching</p>' +
    '<h3 class="tca-title">Base current, collector current</h3>' +
    '<p class="tca-frame"></p>' +
    '<div class="tca-body">' +
      '<div class="tca-stage">' + SVG + '</div>' +
      '<div class="tca-ctrl">' +
        '<div class="tca-opts"></div>' +
        '<div class="tca-act"><button type="button" class="tca-go" disabled>Check</button>' +
        '<span class="tca-streak"></span></div>' +
        '<p class="tca-cap"></p>' +
      '</div>' +
    '</div>' +
    '<p class="tca-sr" aria-live="polite"></p>';

  window.SVWidget = {
    meta: {
      id: 'transistor-current-amplification',
      title: 'Base current, collector current',
      teaches: 'A small base current controls a much larger collector current that the supply provides; below about 0.7 V the transistor is off, and above saturation the load sets the ceiling.'
    },
    mount: function (root, ctx) {
      ctx = ctx || {};
      var reduced = !!ctx.reducedMotion;
      root.className = 'svw-tca';
      root.innerHTML = HTML;

      var accent = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
                   ctx.accent || '#8a6a4f';
      root.style.setProperty('--tca-a', accent);
      var hex6 = /^#[0-9a-f]{6}$/i.test(accent);

      var q = function (s) { return root.querySelector(s); };
      var elFrame = q('.tca-frame'), elOpts = q('.tca-opts'), elGo = q('.tca-go'),
          elStreak = q('.tca-streak'), elCap = q('.tca-cap'), elSr = q('.tca-sr');
      var flowC = q('.tca-flow-c'), flowB = q('.tca-flow-b'),
          icArrow = q('.tca-ic-arrow'), ring = q('.tca-load-ring'),
          lampX = q('.tca-load-x'), motorG = q('.tca-load-g'),
          coil = q('.tca-load-rect'), coilH = q('.tca-load-h'),
          supOn = q('.tca-sup-on'), supOff = q('.tca-sup-off'), batt = q('.tca-batt');
      var lIb = q('.tca-l-ib'), lIc = q('.tca-l-ic'), lGain = q('.tca-l-gain'),
          lLoad = q('.tca-l-load'), lRate = q('.tca-l-rate'), lV = q('.tca-l-v'),
          lSig = q('.tca-l-sig'), ibArrow = q('.tca-ib-arrow');

      /* first four rounds are a deliberate teaching arc: ordinary, ceiling,
         no supply, below threshold. The rest are shuffled. */
      var order = [0, 1, 2, 3], rest = [4, 5, 6, 7];
      for (var s = rest.length - 1; s > 0; s--) {
        var j = Math.floor(Math.random() * (s + 1)), t = rest[s];
        rest[s] = rest[j]; rest[j] = t;
      }
      order = order.concat(rest);

      var st = { n: 0, streak: 0, attempted: 0, mastered: false, picked: null, committed: false };
      var r, L, model, opts, btns = [];

      function tint(a) { return hex6 ? accent + a : '#faf8f5'; }

      function show(node, on) { node.classList.toggle('tca-hide', !on); }

      function publish(correct) {
        var d = {
          round: st.n + 1,
          picked: st.picked ? st.picked.ua / 1000 : null,
          committed: st.committed,
          streak: st.streak,
          attempted: st.attempted,
          mastered: st.mastered
        };
        if (st.committed) { d.ic = model.ic / 1000; d.correct = !!correct; }
        root.dataset.svState = JSON.stringify(d);
      }

      function drawFlow(ua, ghost) {
        var w = ua > 0 ? Math.round((2 + 5.5 * Math.min(1, ua / r.full)) * 10) / 10 : 0;
        flowC.style.strokeWidth = w + 'px';
        flowC.style.strokeDasharray = ghost ? '5 5' : (w ? '10 8' : 'none');
        flowC.style.opacity = ghost ? '0.4' : '0.85';
        flowC.classList.toggle('tca-march', !!(w && !ghost && !reduced));
        show(icArrow, !!w && !ghost);
      }

      function paintLoad(state) {
        var fill = state === 'full' ? tint('99') : (state === 'weak' ? tint('4d') : '#fff');
        ring.setAttribute('fill', fill);
        coil.setAttribute('fill', fill);
      }

      function setRound() {
        r = ROUNDS[order[st.n % order.length]];
        L = LOADS[r.load];
        model = solve(r);
        opts = optionsFor(r);
        for (var i = opts.length - 1; i > 0; i--) {
          var k = Math.floor(Math.random() * (i + 1)), tmp = opts[i];
          opts[i] = opts[k]; opts[k] = tmp;
        }
        st.picked = null;
        st.committed = false;

        elFrame.textContent = frameFor(r, L);

        /* diagram */
        var isLamp = r.load === 'lamp', isMotor = r.load === 'motor', isRelay = r.load === 'relay';
        show(ring, !isRelay); show(lampX, isLamp); show(motorG, isMotor);
        show(coil, isRelay); show(coilH, isRelay);
        show(supOn, r.mode !== 'nosupply'); show(supOff, r.mode === 'nosupply');
        batt.style.opacity = r.mode === 'nosupply' ? '0.35' : '1';
        lLoad.textContent = L.name;
        lRate.textContent = mAt(r.full) + ' full';
        lIb.textContent = ' = ' + (r.mode === 'below' ? '?' : mAt(r.ib));
        lIc.textContent = ' = ?';
        lGain.textContent = 'gain ' + r.gain;
        lV.textContent = r.supply + ' V';
        lSig.textContent = r.vsig + ' V in';
        flowB.style.strokeWidth = (r.mode === 'below' ? 0 : 2.4) + 'px';
        show(ibArrow, r.mode !== 'below');
        paintLoad('off');
        drawFlow(0, false);

        /* options: build once, then mutate */
        while (btns.length > opts.length) { elOpts.removeChild(btns.pop().b); }
        while (btns.length < opts.length) {
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'tca-opt';
          var num = document.createElement('span'); num.className = 'tca-num';
          var out = document.createElement('span'); out.className = 'tca-out';
          var tick = document.createElement('span'); tick.className = 'tca-tick';
          b.appendChild(num); b.appendChild(out); b.appendChild(tick);
          elOpts.appendChild(b);
          btns.push({ b: b, num: num, out: out, tick: tick });
          (function (idx) {
            b.addEventListener('click', function () { pick(idx); });
          })(btns.length - 1);
        }
        btns.forEach(function (o, i) {
          var op = opts[i];
          o.num.textContent = mAt(op.ua);
          o.out.textContent = L[stateOf(op.ua, r.full)];
          o.tick.textContent = '';
          o.b.disabled = false;
          o.b.className = 'tca-opt';
          o.b.setAttribute('aria-pressed', 'false');
        });

        elGo.textContent = 'Check';
        elGo.disabled = true;
        elCap.innerHTML = '<strong>Two currents</strong> meet at the emitter: the small one in at the base,' +
                          ' and whatever runs down through the ' + L.name + '.';
        say(L.name + ' circuit, ' + r.supply + ' volt supply' +
            (r.mode === 'nosupply' ? ', supply lead disconnected' : '') +
            (r.mode === 'below' ? ', signal ' + r.vsig + ' volts, below threshold' :
             ', base current ' + mAt(r.ib)) + ', gain ' + r.gain + '.');
        setStreakLine();
        publish(null);
      }

      function say(msg) { elSr.textContent = msg; }

      function setStreakLine() {
        if (st.mastered) { elStreak.textContent = 'Mastered — carry on if you like.'; return; }
        if (st.streak === 1) { elStreak.textContent = '1 in a row — two more to go.'; return; }
        if (st.streak === 2) { elStreak.textContent = '2 in a row — one more and you have it.'; return; }
        elStreak.textContent = '';
      }

      function pick(i) {
        if (st.committed) return;
        st.picked = opts[i];
        btns.forEach(function (o, k) {
          o.b.classList.toggle('is-sel', k === i);
          o.b.setAttribute('aria-pressed', k === i ? 'true' : 'false');
        });
        lIc.textContent = ' = ' + mAt(opts[i].ua) + '?';
        drawFlow(opts[i].ua, true);
        paintLoad('off');
        elGo.disabled = false;
        publish(null);
      }

      function commit() {
        if (!st.picked) return;
        st.committed = true;
        st.attempted++;
        var right = st.picked.tag === 'correct';
        if (right) { st.streak++; } else { st.streak = 0; }
        var justMastered = right && st.streak >= 3 && !st.mastered;
        if (right && st.streak >= 3) st.mastered = true;

        var fb = feedback(r, L, model, st.picked);
        var body = justMastered
          ? ' Three in a row — you have it: the base current decides how much of the supply’s' +
            ' current the transistor lets through.'
          : fb.body;
        elCap.innerHTML = '<strong class="' + (right ? 'tca-v-right' : '') + '">' +
                          fb.head.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</strong>' +
                          body.replace(/&/g, '&amp;').replace(/</g, '&lt;');

        lIc.textContent = ' = ' + mAt(model.ic);
        if (r.mode === 'below') lIb.textContent = ' = 0 mA';
        drawFlow(model.ic, false);
        paintLoad(model.state);

        btns.forEach(function (o, k) {
          o.b.disabled = true;
          o.b.classList.remove('is-sel');
          if (opts[k].tag === 'correct') { o.b.classList.add('is-right'); o.tick.textContent = '✓'; }
          else if (opts[k] === st.picked) { o.b.classList.add('is-miss'); }
        });

        elGo.textContent = st.mastered ? 'Another anyway' : 'Next';
        elGo.disabled = false;
        setStreakLine();
        say(fb.head + fb.body);
        publish(right);
      }

      elGo.addEventListener('click', function () {
        if (st.committed) { st.n++; setRound(); elGo.focus(); }
        else { commit(); }
      });

      setRound();
    }
  };
})();
