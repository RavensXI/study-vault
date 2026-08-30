/* ============================================================
   StudyVault lesson widget - zener-regulator-active-clamping
   Electronics (Eduqas), "Diodes, Half-Wave Rectification and Zener
   Voltage Regulation".

   The idea it makes concrete: a zener regulator is ACTIVE. It holds
   V_out at V_Z by conducting whatever current that takes, so a rising
   supply changes the ZENER CURRENT, not the output voltage. A resistor
   would keep a fixed share of V_in; a zener does not share, it clamps.

   Scope is the lesson's own circuit: unregulated supply -> series
   resistor Rs -> zener (cathode up, anode to 0 V), output across the
   zener. No load branch, because the lesson has none. The one boundary
   round comes from the lesson's own sentence - the diode clamps "when
   the reverse voltage REACHES the breakdown voltage" - so a supply that
   sags below V_Z leaves the zener out of breakdown entirely.

   Every figure is derived from two lines of the lesson's own model:
       V_out = V_Z while V_in > V_Z, else V_out = V_in
       I     = (V_in - V_Z) / Rs   (Ohm's law on the series resistor)
   Voltages are held as integer millivolts and resistances as integer
   ohms, chosen so every current is a whole number of milliamps. The
   pool is filtered at load time against those identities, so a bad
   entry cannot reach a student.
   ============================================================ */
(function () {
  'use strict';

  var NS = 'svw-zen';
  var OHM = 'Ω', MINUS = '−', ARR = '→', DASH = '—', RSQ = '’';

  /* ---------- the pool -----------------------------------------------
     t = round type:
       rise  supply climbs, Rs unchanged           -> V_out holds, I rises
       fall  supply drops but stays above V_Z      -> V_out holds, I falls
       comp  supply AND Rs change together         -> V_out holds, I holds
       sag   supply drops BELOW V_Z                -> V_out follows, I = 0
     Everything else is computed. ------------------------------------- */
  var RAW = [
    { t: 'rise', vz: 5100,  vin: 9000,  vin2: 12000, rs: 300, rs2: 300 },
    { t: 'rise', vz: 6200,  vin: 8000,  vin2: 12000, rs: 200, rs2: 200 },
    { t: 'rise', vz: 12000, vin: 15000, vin2: 20000, rs: 200, rs2: 200 },
    { t: 'rise', vz: 5600,  vin: 10000, vin2: 15000, rs: 200, rs2: 200 },

    { t: 'fall', vz: 15000, vin: 20000, vin2: 18000, rs: 200, rs2: 200 },
    { t: 'fall', vz: 5600,  vin: 12000, vin2: 9000,  rs: 200, rs2: 200 },
    { t: 'fall', vz: 3300,  vin: 9000,  vin2: 6000,  rs: 300, rs2: 300 },

    { t: 'comp', vz: 12000, vin: 15000, vin2: 18000, rs: 150, rs2: 300 },
    { t: 'comp', vz: 15000, vin: 18000, vin2: 21000, rs: 100, rs2: 200 },
    { t: 'comp', vz: 12000, vin: 18000, vin2: 15000, rs: 300, rs2: 150 },

    { t: 'sag',  vz: 5100,  vin: 9000,  vin2: 3000,  rs: 300, rs2: 300 },
    { t: 'sag',  vz: 12000, vin: 15000, vin2: 5000,  rs: 150, rs2: 150 }
  ];

  function volts(mv) {
    var a = Math.abs(mv), s = (a % 1000 === 0) ? String(a / 1000) : (a / 1000).toFixed(1);
    return (mv < 0 ? MINUS : '') + s + ' V';
  }
  function ohms(r) { return r + ' ' + OHM; }
  function mA(i) { return i + ' mA'; }

  /* Derive a round, and refuse anything that is not integer-clean. */
  function prep(r) {
    var regBefore = r.vin > r.vz;
    var regAfter = r.vin2 > r.vz;
    if (!regBefore) return null;
    if (r.vin2 === r.vin || r.vin2 === r.vz) return null;
    if ((r.vin - r.vz) % r.rs !== 0) return null;
    if (regAfter && (r.vin2 - r.vz) % r.rs2 !== 0) return null;

    /* what the output WOULD be if the zener behaved like a resistor,
       i.e. kept a fixed share of the supply. This is the misconception,
       priced out of the round's own figures. */
    if ((r.vz * r.vin2) % r.vin !== 0) return null;
    var prop = r.vz * r.vin2 / r.vin;
    if (prop % 100 !== 0) return null;
    if (prop === r.vz || prop === r.vin2 || r.vz === r.vin2) return null;

    var iB = (r.vin - r.vz) / r.rs;
    var iA = regAfter ? (r.vin2 - r.vz) / r.rs2 : 0;
    if (iB <= 0 || iA < 0) return null;

    var opts = [r.vz, prop, r.vin2].sort(function (a, b) { return a - b; });
    var ansV = regAfter ? r.vz : r.vin2;
    var ansI = iA > iB ? 'up' : (iA < iB ? 'down' : 'same');

    return {
      r: r, prop: prop, iB: iB, iA: iA, regAfter: regAfter,
      vout2: regAfter ? r.vz : r.vin2,
      opts: opts, ansV: ansV, ansI: ansI
    };
  }

  var POOL = [];
  for (var pi = 0; pi < RAW.length; pi++) {
    var pr = prep(RAW[pi]);
    if (pr) POOL.push(pr);
  }

  window.SVWidget = {
    meta: {
      id: 'zener-regulator-active-clamping',
      title: 'Zener regulator: move the supply',
      teaches: 'A zener regulator holds V_out at V_Z by changing its own current; the supply and the series resistor set that current, not the output voltage.'
    },

    mount: function (root, ctx) {
      var A = (ctx && ctx.accent) ||
              (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var REDUCE = !!(ctx && ctx.reducedMotion);

      /* ---------- tiny DOM helpers ---------------------------------- */
      function el(tag, cls, txt) {
        var n = document.createElement(tag);
        if (cls) n.className = cls;
        if (txt != null) n.textContent = txt;
        return n;
      }
      function sv(tag, attrs) {
        var n = document.createElementNS('http://www.w3.org/2000/svg', tag);
        for (var k in attrs) if (attrs.hasOwnProperty(k)) n.setAttribute(k, attrs[k]);
        return n;
      }
      function line(x1, y1, x2, y2, w, col) {
        return sv('line', { x1: x1, y1: y1, x2: x2, y2: y2, stroke: col || '#8d8880',
                            'stroke-width': w || 1.4, 'stroke-linecap': 'round' });
      }
      function txt(x, y, s, size, weight, fill, anchor) {
        var t = sv('text', { x: x, y: y, 'font-size': size, 'font-weight': weight || 400,
                             fill: fill || '#2d2a26', 'text-anchor': anchor || 'start' });
        t.textContent = s || '';
        return t;
      }

      root.textContent = '';
      var wrap = el('div', NS);
      root.appendChild(wrap);

      /* ---------- scoped style -------------------------------------- */
      var css = el('style');
      css.textContent = [
        '.' + NS + '{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45}',
        '.' + NS + ' *{box-sizing:border-box}',
        '.' + NS + ' .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .15rem;color:' + A + '}',
        '.' + NS + ' .hdr{display:flex;align-items:baseline;gap:.55rem}',
        '.' + NS + ' .ttl{font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;font-weight:600;margin:0;flex:1;line-height:1.2}',
        '.' + NS + ' .run{font-size:.72rem;color:#8d8880;white-space:nowrap;font-variant-numeric:tabular-nums}',
        '.' + NS + ' .frame{font-size:.85rem;margin:.3rem 0 .45rem;color:#3c382f}',
        '.' + NS + ' .work{display:flex;flex-wrap:wrap;gap:.6rem}',
        '.' + NS + ' .stage{flex:1 1 290px;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.3rem .4rem .2rem}',
        '.' + NS + ' .stage svg{display:block;width:100%;max-width:330px;height:auto;margin:0 auto}',
        '.' + NS + ' .stage svg text{font-family:Inter,system-ui,sans-serif;font-variant-numeric:tabular-nums}',
        '.' + NS + ' .eq{font-size:.72rem;line-height:1.3;color:#8d8880;text-align:center;margin:.1rem 0 0;font-variant-numeric:tabular-nums}',
        '.' + NS + ' .ctrl{flex:1 1 250px;display:flex;flex-direction:column;justify-content:center}',
        '.' + NS + ' .grp{margin-bottom:.3rem}',
        '.' + NS + ' .grp[data-live="no"]{opacity:.4}',
        '.' + NS + ' .step{display:flex;align-items:center;gap:.35rem;margin:0 0 .25rem}',
        '.' + NS + ' .chip{width:16px;height:16px;flex:none;border-radius:50%;background:#efe9e0;color:#5b564e;font-size:.62rem;font-weight:700;display:flex;align-items:center;justify-content:center}',
        '.' + NS + ' .q{font-size:.78rem;font-weight:600}',
        '.' + NS + ' .opts{display:flex;gap:.3rem}',
        '.' + NS + ' .opt{flex:1 1 0;min-width:0;font-family:inherit;font-size:.8rem;font-weight:600;padding:.4rem .2rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;cursor:pointer;font-variant-numeric:tabular-nums}',
        '.' + NS + ' .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
        '.' + NS + ' .opt:disabled{cursor:default}',
        '.' + NS + ' .go{margin-top:.4rem;width:100%;font-family:inherit;font-size:.84rem;font-weight:600;padding:.5rem 1rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
        '.' + NS + ' .go:disabled{opacity:.35;cursor:default}',
        '.' + NS + ' .cap{font-size:.84rem;line-height:1.5;margin:.5rem 0 0;min-height:3.8em;color:#3c382f}',
        '.' + NS + ' .cap strong{font-weight:600}',
        '.' + NS + ' .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}',
        REDUCE ? '' : '.' + NS + ' .opt,.' + NS + ' .go{transition:background .14s ease,color .14s ease}'
      ].join('\n');
      wrap.appendChild(css);

      /* ---------- header + task frame -------------------------------- */
      wrap.appendChild(el('p', 'k', 'Zener regulation'));
      var hdr = el('div', 'hdr');
      hdr.appendChild(el('h3', 'ttl', 'Move the supply'));
      var run = el('span', 'run', '');
      hdr.appendChild(run);
      wrap.appendChild(hdr);

      var frame = el('p', 'frame', '');
      wrap.appendChild(frame);

      var work = el('div', 'work');
      wrap.appendChild(work);

      /* ---------- stage: the regulator circuit ----------------------- */
      var stage = el('div', 'stage');
      var svg = sv('svg', { viewBox: '0 -2 320 119', 'aria-hidden': 'true', focusable: 'false' });
      var WX = 122, RAIL = 12, RSY = 24, RSH = 26, TAP = 62, ZBAR = 78, ZFOOT = 96, GND = 108;

      /* wires */
      svg.appendChild(line(102, RAIL, 142, RAIL));
      svg.appendChild(line(WX, RAIL, WX, RSY));
      svg.appendChild(line(WX, RSY + RSH, WX, ZBAR));
      svg.appendChild(line(WX, ZFOOT, WX, GND));
      svg.appendChild(line(WX - 14, GND, WX + 14, GND));
      svg.appendChild(line(WX - 9, GND + 4, WX + 9, GND + 4));
      svg.appendChild(line(WX - 4, GND + 8, WX + 4, GND + 8));

      /* series resistor */
      svg.appendChild(sv('rect', { x: WX - 17, y: RSY, width: 34, height: RSH, rx: 3,
                                   fill: '#fff', stroke: '#5b564e', 'stroke-width': 1.4 }));
      svg.appendChild(txt(WX + 21, RSY + 12, 'Rs', 10.5, 600, '#8d8880'));

      /* zener: cathode bar at the top (reverse biased), anode to 0 V */
      var zTri = sv('polygon', { points: (WX - 10) + ',' + ZFOOT + ' ' + (WX + 10) + ',' + ZFOOT +
                                          ' ' + WX + ',' + (ZBAR + 2),
                                 fill: '#fff', stroke: '#2d2a26', 'stroke-width': 1.4 });
      svg.appendChild(zTri);
      svg.appendChild(line(WX - 12, ZBAR, WX + 12, ZBAR, 1.9, '#2d2a26'));
      svg.appendChild(line(WX - 12, ZBAR, WX - 16, ZBAR + 5, 1.6, '#2d2a26'));
      svg.appendChild(line(WX + 12, ZBAR, WX + 16, ZBAR - 5, 1.6, '#2d2a26'));

      /* left-hand read-outs */
      var vinTxt = txt(98, RAIL + 4, '', 11.5, 600, '#2d2a26', 'end');
      var rsTxt = txt(98, RSY + 20, '', 11.5, 400, '#5b564e', 'end');
      var zTxt = txt(98, ZBAR + 14, '', 11, 600, '#2d2a26', 'end');
      svg.appendChild(vinTxt); svg.appendChild(rsTxt); svg.appendChild(zTxt);
      svg.appendChild(txt(WX + 20, GND + 4, '0 V', 11, 400, '#8d8880'));

      /* current through Rs and the zener */
      var iArrow = sv('g', {});
      var iLine = line(146, ZBAR - 4, 146, ZFOOT - 6, 1.6, '#2d2a26');
      var iHead = sv('polygon', { points: '146,' + (ZFOOT - 1) + ' 141,' + (ZFOOT - 9) +
                                          ' 151,' + (ZFOOT - 9), fill: '#2d2a26' });
      iArrow.appendChild(iLine); iArrow.appendChild(iHead);
      svg.appendChild(iArrow);
      svg.appendChild(txt(156, ZBAR + 2, 'I', 10.5, 600, '#8d8880'));
      var iTxt = txt(164, ZBAR + 2, '', 12, 700, '#2d2a26');
      var iWas = txt(156, ZBAR + 16, '', 9.5, 400, '#8d8880');
      svg.appendChild(iTxt); svg.appendChild(iWas);

      /* output tap */
      svg.appendChild(line(WX, TAP, 222, TAP));
      svg.appendChild(sv('circle', { cx: WX, cy: TAP, r: 3, fill: '#5b564e' }));
      svg.appendChild(sv('circle', { cx: 226, cy: TAP, r: 3.2, fill: '#fff',
                                     stroke: '#8d8880', 'stroke-width': 1.4 }));
      svg.appendChild(txt(234, TAP - 6, 'V out', 11, 600, '#5b564e'));
      var vTxt = txt(234, TAP + 12, '', 14.5, 700, A);
      var vWas = txt(234, TAP + 26, '', 9.5, 400, '#8d8880');
      svg.appendChild(vTxt); svg.appendChild(vWas);

      stage.appendChild(svg);
      var eq = el('p', 'eq', '');
      stage.appendChild(eq);
      work.appendChild(stage);

      /* ---------- controls ------------------------------------------- */
      var ctrl = el('div', 'ctrl');
      function group(n) {
        var g = el('div', 'grp');
        var s = el('div', 'step');
        s.appendChild(el('span', 'chip', String(n)));
        var q = el('span', 'q', '');
        s.appendChild(q);
        g.appendChild(s);
        var o = el('div', 'opts');
        var b = [el('button', 'opt'), el('button', 'opt'), el('button', 'opt')];
        b.forEach(function (x) { x.type = 'button'; x.setAttribute('aria-pressed', 'false'); o.appendChild(x); });
        g.appendChild(o);
        return { node: g, q: q, btns: b };
      }
      var g1 = group(1), g2 = group(2);
      ctrl.appendChild(g1.node); ctrl.appendChild(g2.node);
      var go = el('button', 'go', 'Check');
      go.type = 'button';
      ctrl.appendChild(go);
      work.appendChild(ctrl);

      var cap = el('p', 'cap', '');
      wrap.appendChild(cap);
      var sr = el('p', 'sr');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      /* ---------- state ---------------------------------------------- */
      var IWORD = { up: 'rises', same: 'stays the same', down: 'falls' };
      var ILABEL = [['up', 'Rises'], ['same', 'No change'], ['down', 'Falls']];

      function shuffle(a) {
        a = a.slice();
        for (var i = a.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
        }
        return a;
      }
      /* interleave the four kinds, so any run of three spans more than one */
      function buildOrder() {
        var by = { rise: [], fall: [], comp: [], sag: [] }, ptr = { rise: 0, fall: 0, comp: 0, sag: 0 };
        POOL.forEach(function (o) { by[o.r.t].push(o); });
        ['rise', 'fall', 'comp', 'sag'].forEach(function (k) { by[k] = shuffle(by[k]); });
        var map = { r: 'rise', f: 'fall', c: 'comp', s: 'sag' }, out = [];
        'rfcrsfrcfrcs'.split('').forEach(function (ch) {
          var t = map[ch];
          if (ptr[t] < by[t].length) out.push(by[t][ptr[t]++]);
        });
        ['rise', 'fall', 'comp', 'sag'].forEach(function (t) {
          while (ptr[t] < by[t].length) out.push(by[t][ptr[t]++]);
        });
        return out;
      }

      var order = buildOrder();
      var idx = 0, s1 = null, s2 = null, done = false;
      var streak = 0, attempted = 0, mastered = false, lastCorrect = null;

      function O() { return order[idx % order.length]; }

      function say(str) {
        cap.textContent = '';
        str.split('**').forEach(function (part, i) {
          if (!part) return;
          cap.appendChild(i % 2 ? el('strong', null, part) : document.createTextNode(part));
        });
        sr.textContent = str.replace(/\*\*/g, '');
      }

      function pushState() {
        var o = O(), r = o.r;
        root.dataset.svState = JSON.stringify({
          round: idx + 1, kind: r.t,
          picked: (s1 == null ? '-' : s1) + '|' + (s2 || '-'),
          committed: done, correct: lastCorrect,
          streak: streak, mastered: mastered, attempted: attempted,
          vz: r.vz / 1000, vinBefore: r.vin / 1000, vinAfter: r.vin2 / 1000,
          rs: done ? r.rs2 : r.rs,
          vout: (done ? o.vout2 : r.vz) / 1000,
          iz: done ? o.iA : o.iB
        });
      }

      /* ---------- the picture, drawn from the model ------------------- */
      function drawStage() {
        var o = O(), r = o.r;
        var vin = done ? r.vin2 : r.vin;
        var rs = done ? r.rs2 : r.rs;
        var vout = done ? o.vout2 : r.vz;
        var cur = done ? o.iA : o.iB;
        var conducting = done ? o.regAfter : true;

        vinTxt.textContent = 'V in = ' + volts(vin);
        rsTxt.textContent = ohms(rs);
        zTxt.textContent = volts(r.vz) + ' zener';
        vTxt.textContent = volts(vout);
        vWas.textContent = !done ? '' : (vout === r.vz ? 'unchanged' : 'was ' + volts(r.vz));

        zTri.setAttribute('fill', conducting ? A + '33' : '#fff');
        if (cur > 0) {
          iArrow.setAttribute('opacity', '1');
          iLine.setAttribute('stroke-width', String(1.2 + Math.min(cur, 60) / 22));
          iTxt.textContent = mA(cur);
          iTxt.setAttribute('fill', '#2d2a26');
        } else {
          iArrow.setAttribute('opacity', '0');
          iTxt.textContent = '0 mA';
          iTxt.setAttribute('fill', '#8d8880');
        }
        iWas.textContent = !done ? '' : (cur === o.iB ? 'unchanged' : 'was ' + mA(o.iB));

        if (!done) {
          eq.textContent = 'I = (V in ' + MINUS + ' V Z) / Rs';
        } else if (o.regAfter) {
          eq.textContent = '(' + (r.vin2 / 1000) + ' ' + MINUS + ' ' + (r.vz / 1000) + ') / ' +
                           r.rs2 + ' = ' + mA(o.iA);
        } else {
          eq.textContent = 'V in below V Z ' + DASH + ' no breakdown, I = 0 mA';
        }
      }

      function paintOpts() {
        var o = O();
        g1.btns.forEach(function (b, i) {
          b.textContent = volts(o.opts[i]);
          b.setAttribute('aria-pressed', s1 === o.opts[i] ? 'true' : 'false');
          b.disabled = done;
        });
        g2.btns.forEach(function (b, i) {
          b.textContent = ILABEL[i][1];
          b.setAttribute('aria-pressed', s2 === ILABEL[i][0] ? 'true' : 'false');
          b.disabled = done || s1 == null;
        });
        g2.node.setAttribute('data-live', s1 == null ? 'no' : 'yes');
        go.disabled = !done && !(s1 != null && s2);
      }

      function runLabel() {
        if (mastered) run.textContent = 'Mastered';
        else if (streak === 2) run.textContent = '2 in a row ' + DASH + ' 1 more';
        else if (streak === 1) run.textContent = '1 in a row';
        else run.textContent = '';
      }

      function frameText(o) {
        var r = o.r;
        var s = 'A ' + volts(r.vz) + ' zener regulates a ' + volts(r.vin) +
                ' supply through a ' + ohms(r.rs) + ' series resistor. ';
        if (r.t === 'comp') {
          s += 'The supply is changed to ' + volts(r.vin2) + ' and the series resistor to ' +
               ohms(r.rs2) + '. ';
        } else {
          s += 'The supply now ' + (r.vin2 > r.vin ? 'rises' : 'falls') + ' to ' +
               volts(r.vin2) + '. ';
        }
        return s + 'Predict V_out and the zener current.';
      }

      var OPENING = 'Rs and the zener sit in series across the supply: **one current runs ' +
                    'through both**, and their two voltages must add up to V_in.';

      function showRound() {
        var o = O();
        s1 = null; s2 = null; done = false; lastCorrect = null;
        frame.textContent = frameText(o);
        g1.q.textContent = 'V_out then becomes:';
        g2.q.textContent = 'The zener current then:';
        go.textContent = 'Check';
        paintOpts();
        drawStage();
        say(OPENING);
        runLabel();
        pushState();
      }

      /* ---------- the verdict, read off the model --------------------- */
      function judge(o) {
        var r = o.r;
        var correct = (s1 === o.ansV) && (s2 === o.ansI);
        var head = (correct ? 'Right ' : 'Not quite ') + DASH + ' you said V_out becomes ' +
                   volts(s1) + ' and the current ' + IWORD[s2] + '. ';
        var body, closer;

        if (o.regAfter) {
          body = 'In breakdown the zener holds V_out at ' + volts(r.vz) +
                 ', so Rs takes the rest: ' + volts(r.vin - r.vz) + ' ' + ARR + ' ' +
                 volts(r.vin2 - r.vz) + '. ';
          if (r.t === 'comp') {
            body += 'Rs changes too (' + ohms(r.rs) + ' ' + ARR + ' ' + ohms(r.rs2) +
                    '), so the current holds at ' + mA(o.iA) + '.';
          } else {
            body += 'The current through both goes ' + mA(o.iB) + ' ' + ARR + ' ' + mA(o.iA) + '.';
          }
          if (s1 === o.prop) {
            closer = ' A resistor would keep a fixed share of V_in ' + DASH + ' that is where ' +
                     volts(o.prop) + ' comes from. A zener does not share; it clamps.';
          } else if (s1 === r.vin2) {
            closer = ' V_out = V_in would mean the zener was doing nothing. In breakdown it ' +
                     'conducts hard and holds the rail down.';
          } else if (!correct) {
            closer = ' Its current is not fixed either: it is whatever Rs lets through, ' +
                     '(V_in ' + MINUS + ' V_Z) / Rs.';
          } else if (o.ansI === 'up') {
            closer = ' The zener holds the rail by conducting more, not by resisting more.';
          } else if (o.ansI === 'down') {
            closer = ' It still holds the rail while passing less ' + DASH +
                     ' the voltage it holds never moves.';
          } else {
            closer = ' The zener sets the voltage; the supply and Rs set the current.';
          }
        } else {
          body = volts(r.vin2) + ' is below the zener' + RSQ + 's ' + volts(r.vz) +
                 ' breakdown voltage, so it never conducts: ' + mA(o.iB) + ' ' + ARR + ' 0 mA. ' +
                 'With no current, Rs drops nothing, so V_out follows the supply to ' +
                 volts(r.vin2) + '.';
          if (s1 === r.vz) {
            closer = ' A zener holds a **ceiling**. It cannot lift a supply that is already ' +
                     'below V_Z.';
          } else if (s1 === o.prop) {
            closer = ' Nothing is being shared here ' + DASH + ' with no current, Rs drops 0 V.';
          } else {
            closer = ' A zener holds a **ceiling**, so clamping stops the moment the supply ' +
                     'drops below V_Z.';
          }
        }

        var mastery = o.regAfter
          ? 'Right ' + DASH + ' V_out held at ' + volts(r.vz) + ' and the current ' +
            (o.iA === o.iB ? 'held at ' + mA(o.iA)
                           : 'went ' + mA(o.iB) + ' ' + ARR + ' ' + mA(o.iA)) + '. '
          : 'Right ' + DASH + ' the supply fell below V_Z, the zener stopped conducting and ' +
            'V_out followed it to ' + volts(r.vin2) + '. ';

        return { correct: correct, msg: head + body + closer, mastery: mastery };
      }

      var MASTERY = '**Three in a row ' + DASH + ' you have it.** The zener fixes V_out at V_Z ' +
                    'by conducting whatever current that takes. The supply and Rs fix that ' +
                    'current: I = (V_in ' + MINUS + ' V_Z) / Rs.';

      function commit() {
        var o = O(), v = judge(o), hadRun = streak;
        done = true;
        attempted++;
        lastCorrect = v.correct;
        streak = v.correct ? streak + 1 : 0;
        var firstMastery = false;
        if (v.correct && streak >= 3 && !mastered) { mastered = true; firstMastery = true; }
        var msg = v.msg;
        if (firstMastery) msg = v.mastery + MASTERY;
        else if (!v.correct && hadRun > 0) msg += ' Your run resets to zero.';
        say(msg);
        drawStage();
        paintOpts();
        go.textContent = mastered ? 'Another anyway' : 'Next';
        runLabel();
        pushState();
      }

      /* ---------- wiring ---------------------------------------------- */
      g1.btns.forEach(function (b, i) {
        b.addEventListener('click', function () {
          if (done) return;
          s1 = O().opts[i];
          paintOpts(); pushState();
        });
      });
      g2.btns.forEach(function (b, i) {
        b.addEventListener('click', function () {
          if (done || s1 == null) return;
          s2 = ILABEL[i][0];
          paintOpts(); pushState();
        });
      });
      go.addEventListener('click', function () {
        if (done) { idx++; showRound(); return; }
        if (s1 != null && s2) commit();
      });
      wrap.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !done && (s1 != null || s2)) {
          s1 = null; s2 = null;
          paintOpts(); pushState();
        }
      });

      showRound();
    }
  };
})();
