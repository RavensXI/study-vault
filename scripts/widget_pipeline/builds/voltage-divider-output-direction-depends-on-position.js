/* ============================================================
   Sensing voltage divider - which way does V_out move?

   The idea it makes concrete: V_out is R2's share of V_in, so the SAME
   sensor drives the output in opposite directions depending on whether
   it sits above the tap (R1) or below it (R2).

   Every verdict is derived from V_out = V_in x R2 / (R1 + R2) on the
   round's own figures. Nothing is hand-authored.
   ============================================================ */
window.SVWidget = {
  meta: {
    id: 'voltage-divider-output-direction-depends-on-position',
    title: 'Sensor position in a voltage divider',
    teaches: 'Whether V_out rises or falls as a sensed quantity changes depends on whether the sensor is R1 (above the tap) or R2 (below it).'
  },

  mount: function (root, ctx) {
    var A = (ctx && ctx.accent) ||
            (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
    var REDUCE = !!(ctx && ctx.reducedMotion);

    var OHM = 'Ω', TIMES = '×', ARR = '→', RSQ = '’', DASH = '—';

    /* ---------- model -------------------------------------------------- */

    function kohm(v) { return v + ' k' + OHM; }
    function volts(v) { return v.toFixed(1) + ' V'; }
    /* V_out = V_in x R2 / (R1 + R2) */
    function vout(vin, r1, r2) { return vin * r2 / (r1 + r2); }

    var RULE = {
      LDR: 'an LDR' + RSQ + 's resistance **falls as the light rises**',
      Thermistor: 'a thermistor' + RSQ + 's resistance **falls as it gets warmer**'
    };
    /* how each sensor is named in running prose */
    var WORD = { LDR: 'LDR', Thermistor: 'thermistor' };
    function cap1(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

    /* sensor of resistance r sitting at round.pos -> {r1, r2} */
    function pair(round, r) {
      return round.pos === 'R1' ? { r1: r, r2: round.fixed } : { r1: round.fixed, r2: r };
    }

    var PREDICT = [
      { vin: 9, sensor: 'LDR', fixed: 2, pos: 'R1', rFrom: 16, rTo: 1, change: 'The room gets brighter.' },
      { vin: 9, sensor: 'LDR', fixed: 2, pos: 'R2', rFrom: 16, rTo: 1, change: 'The room gets brighter.' },
      { vin: 5, sensor: 'Thermistor', fixed: 1, pos: 'R1', rFrom: 9, rTo: 1, change: 'The room warms up.' },
      { vin: 5, sensor: 'Thermistor', fixed: 1, pos: 'R2', rFrom: 1, rTo: 9, change: 'The room cools down.' },
      { vin: 9, sensor: 'LDR', fixed: 1, pos: 'R1', rFrom: 2, rTo: 8, change: 'Dusk falls and it gets darker.' },
      { vin: 9, sensor: 'Thermistor', fixed: 3, pos: 'R2', rFrom: 15, rTo: 3, change: 'The room warms up.' }
    ];

    var DESIGN = [
      { vin: 9, sensor: 'LDR', fixed: 2, rTrig: 16, rOther: 1,
        cond: 'in the dark', other: 'in bright light', device: 'lamp',
        frame: 'A lamp must switch on in darkness. Its driver only fires when V_out is high. Decide where the LDR belongs.' },
      { vin: 9, sensor: 'Thermistor', fixed: 2, rTrig: 1, rOther: 16,
        cond: 'when it is hot', other: 'when it is cool', device: 'fan',
        frame: 'A fan must switch on when the room gets hot. Its driver only fires when V_out is high. Decide where the thermistor belongs.' },
      { vin: 5, sensor: 'Thermistor', fixed: 1, rTrig: 9, rOther: 1,
        cond: 'in the cold', other: 'in the warm', device: 'alarm',
        frame: 'A frost alarm must sound when it gets cold. Its driver only fires when V_out is high. Decide where the thermistor belongs.' }
    ];

    function shuffle(a) {
      a = a.slice();
      for (var i = a.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
      }
      return a;
    }

    /* predict and design rounds interleaved, so a run of three correct
       answers always covers both kinds */
    function buildOrder() {
      var p = shuffle(PREDICT), d = shuffle(DESIGN), out = [], pat = 'ppdppdpdp', pi = 0, di = 0;
      for (var i = 0; i < pat.length; i++) {
        if (pat.charAt(i) === 'p' && pi < p.length) out.push(prepPredict(p[pi++]));
        else if (di < d.length) out.push(prepDesign(d[di++]));
      }
      return out;
    }

    function prepPredict(r) {
      var a = pair(r, r.rFrom), b = pair(r, r.rTo);
      var o = {
        kind: 'predict', data: r,
        before: a, after: b,
        vBefore: vout(r.vin, a.r1, a.r2), vAfter: vout(r.vin, b.r1, b.r2),
        frame: 'The ' + WORD[r.sensor] + ' is ' + r.pos +
               (r.pos === 'R1' ? ' (above the tap)' : ' (below the tap)') +
               ' and a ' + kohm(r.fixed) + ' resistor is ' + (r.pos === 'R1' ? 'R2' : 'R1') +
               '. ' + r.change + ' Predict what V_out does.',
        q1: 'The ' + WORD[r.sensor] + RSQ + 's resistance then:',
        o1: [['up', 'Goes up'], ['down', 'Goes down']],
        q2: 'And V_out then:',
        o2: [['rises', 'Rises'], ['falls', 'Falls']],
        opening: 'A sensor only changes its **resistance**. The divider is the part that turns that into a changing **voltage**.'
      };
      o.a1 = r.rTo > r.rFrom ? 'up' : 'down';
      o.a2 = o.vAfter > o.vBefore ? 'rises' : 'falls';
      return o;
    }

    function prepDesign(r) {
      var o = {
        kind: 'design', data: r,
        vTrigTop: vout(r.vin, r.rTrig, r.fixed),   /* sensor as R1 */
        vTrigBot: vout(r.vin, r.fixed, r.rTrig),   /* sensor as R2 */
        vOtherTop: vout(r.vin, r.rOther, r.fixed),
        vOtherBot: vout(r.vin, r.fixed, r.rOther),
        frame: r.frame,
        q1: 'Its resistance ' + r.cond + ' is:',
        o1: [['up', 'Higher'], ['down', 'Lower']],
        q2: 'So the ' + WORD[r.sensor] + ' belongs at:',
        o2: [['R1', 'R1 (top)'], ['R2', 'R2 (bottom)']],
        opening: 'The driver never sees the sensor ' + DASH +
                 ' all it reads is **V_out**. Your wiring decides which way that moves.'
      };
      o.a1 = r.rTrig > r.rOther ? 'up' : 'down';
      o.a2 = o.vTrigBot > o.vTrigTop ? 'R2' : 'R1';
      return o;
    }

    /* ---------- shell -------------------------------------------------- */

    var NS = 'svw-vdp';
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

    root.textContent = '';
    var wrap = el('div', NS);
    root.appendChild(wrap);

    var css = el('style');
    css.textContent = [
      '.' + NS + '{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45}',
      '.' + NS + ' *{box-sizing:border-box}',
      '.' + NS + ' .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .15rem;color:' + A + '}',
      '.' + NS + ' .hdr{display:flex;align-items:baseline;gap:.55rem}',
      '.' + NS + ' .ttl{font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;font-weight:600;margin:0;flex:1;line-height:1.2}',
      '.' + NS + ' .run{font-size:.72rem;color:#8d8880;white-space:nowrap;font-variant-numeric:tabular-nums}',
      '.' + NS + ' .frame{font-size:.85rem;margin:.35rem 0 .6rem;color:#3c382f}',
      '.' + NS + ' .work{display:flex;flex-wrap:wrap;gap:.8rem}',
      '.' + NS + ' .stage{flex:1 1 285px;background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.4rem .5rem .3rem}',
      '.' + NS + ' .stage svg{display:block;width:100%;height:128px}',
      '.' + NS + ' .stage svg text{font-family:Inter,system-ui,sans-serif}',
      '.' + NS + ' .eq{font-size:.74rem;color:#8d8880;text-align:center;margin:.15rem 0 0;font-variant-numeric:tabular-nums}',
      '.' + NS + ' .ctrl{flex:1 1 285px;display:flex;flex-direction:column;justify-content:center}',
      '.' + NS + ' .grp{margin-bottom:.3rem}',
      '.' + NS + ' .grp[data-live="no"]{opacity:.4}',
      '.' + NS + ' .step{display:flex;align-items:center;gap:.35rem;margin:0 0 .25rem}',
      '.' + NS + ' .chip{width:16px;height:16px;flex:none;border-radius:50%;background:#efe9e0;color:#5b564e;font-size:.62rem;font-weight:700;display:flex;align-items:center;justify-content:center}',
      '.' + NS + ' .q{font-size:.78rem;font-weight:600}',
      '.' + NS + ' .opts{display:flex;gap:.35rem}',
      '.' + NS + ' .opt{flex:1 1 0;font-family:inherit;font-size:.82rem;font-weight:600;padding:.45rem .3rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;cursor:pointer}',
      '.' + NS + ' .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
      '.' + NS + ' .opt:disabled{cursor:default}',
      '.' + NS + ' .go{margin-top:.45rem;width:100%;font-family:inherit;font-size:.84rem;font-weight:600;padding:.5rem 1rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
      '.' + NS + ' .go:disabled{opacity:.35;cursor:default}',
      '.' + NS + ' .cap{font-size:.84rem;line-height:1.5;margin:.55rem 0 0;min-height:4em;color:#3c382f}',
      '.' + NS + ' .cap strong{font-weight:600}',
      '.' + NS + ' .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}',
      REDUCE ? '' : '.' + NS + ' .opt,.' + NS + ' .go{transition:background .14s ease,color .14s ease}'
    ].join('\n');
    wrap.appendChild(css);

    wrap.appendChild(el('p', 'k', 'Sensing dividers'));
    var hdr = el('div', 'hdr');
    hdr.appendChild(el('h3', 'ttl', 'Top or bottom?'));
    var run = el('span', 'run', '');
    hdr.appendChild(run);
    wrap.appendChild(hdr);

    var frame = el('p', 'frame', '');
    wrap.appendChild(frame);

    var work = el('div', 'work');
    wrap.appendChild(work);

    /* --- stage: the divider itself -------------------------------------- */
    var stage = el('div', 'stage');
    var svg = sv('svg', { viewBox: '0 0 288 120', 'aria-hidden': 'true', focusable: 'false' });
    var WIRE = 122, RAIL = 12, TAP = 60, GND = 108;

    function line(x1, y1, x2, y2, w, col) {
      return sv('line', { x1: x1, y1: y1, x2: x2, y2: y2, stroke: col || '#8d8880',
                          'stroke-width': w || 1.4, 'stroke-linecap': 'round' });
    }
    function txt(x, y, s, size, weight, fill, anchor) {
      var t = sv('text', { x: x, y: y, 'font-size': size, 'font-weight': weight || 400,
                           fill: fill || '#2d2a26', 'text-anchor': anchor || 'start' });
      t.textContent = s;
      return t;
    }

    svg.appendChild(line(102, RAIL, 142, RAIL));
    svg.appendChild(line(WIRE, RAIL, WIRE, 22));
    svg.appendChild(line(WIRE, 48, WIRE, 72));
    svg.appendChild(line(WIRE, 98, WIRE, GND));
    svg.appendChild(line(108, GND, 136, GND));
    svg.appendChild(line(113, GND + 4, 131, GND + 4));
    svg.appendChild(line(118, GND + 8, 126, GND + 8));
    var vinLabel = txt(96, RAIL + 4, '', 11.5, 600, '#5b564e', 'end');
    svg.appendChild(vinLabel);
    svg.appendChild(txt(145, GND + 4, '0 V', 11.5, 400, '#8d8880'));

    var box1 = sv('rect', { x: 105, y: 22, width: 34, height: 26, rx: 3, fill: '#fff',
                            stroke: '#5b564e', 'stroke-width': 1.4 });
    var box2 = sv('rect', { x: 105, y: 72, width: 34, height: 26, rx: 3, fill: '#fff',
                            stroke: '#5b564e', 'stroke-width': 1.4 });
    svg.appendChild(box1); svg.appendChild(box2);

    /* the variable-resistance arrow that marks a component as the sensor */
    function sensorMark(y) {
      var g = sv('g', { opacity: '0' });
      g.appendChild(sv('line', { x1: 104, y1: y + 27, x2: 140, y2: y - 1,
                                 stroke: '#2d2a26', 'stroke-width': 1.3 }));
      g.appendChild(sv('polygon', { points: '143,' + (y - 4) + ' 135,' + (y - 2) + ' 139,' + (y + 4),
                                    fill: '#2d2a26' }));
      return g;
    }
    var mark1 = sensorMark(22), mark2 = sensorMark(72);
    svg.appendChild(mark1); svg.appendChild(mark2);

    svg.appendChild(txt(150, 30, 'R1', 10.5, 600, '#8d8880'));
    svg.appendChild(txt(150, 80, 'R2', 10.5, 600, '#8d8880'));
    var n1 = txt(96, 33, '', 11.5, 600, '#2d2a26', 'end');
    var v1 = txt(96, 46, '', 11.5, 400, '#5b564e', 'end');
    var n2 = txt(96, 83, '', 11.5, 600, '#2d2a26', 'end');
    var v2 = txt(96, 96, '', 11.5, 400, '#5b564e', 'end');
    svg.appendChild(n1); svg.appendChild(v1); svg.appendChild(n2); svg.appendChild(v2);

    svg.appendChild(line(WIRE, TAP, 194, TAP));
    svg.appendChild(sv('circle', { cx: WIRE, cy: TAP, r: 3, fill: '#5b564e' }));
    svg.appendChild(sv('circle', { cx: 197, cy: TAP, r: 3.2, fill: '#fff',
                                   stroke: '#8d8880', 'stroke-width': 1.4 }));
    svg.appendChild(txt(205, TAP - 5, 'V out', 11, 600, '#5b564e'));
    var vTxt = txt(205, TAP + 12, '', 14.5, 700, A);
    var vWas = txt(205, TAP + 26, '', 10.5, 400, '#8d8880');
    svg.appendChild(vTxt); svg.appendChild(vWas);
    var tri = sv('polygon', { points: '0,0 0,0 0,0', fill: '#2d2a26', opacity: '0' });
    svg.appendChild(tri);

    stage.appendChild(svg);
    var eq = el('p', 'eq', '');
    stage.appendChild(eq);
    work.appendChild(stage);

    /* --- controls -------------------------------------------------------- */
    var ctrl = el('div', 'ctrl');
    function group(n) {
      var g = el('div', 'grp');
      var s = el('div', 'step');
      s.appendChild(el('span', 'chip', String(n)));
      var q = el('span', 'q', '');
      s.appendChild(q);
      g.appendChild(s);
      var o = el('div', 'opts');
      var b = [el('button', 'opt'), el('button', 'opt')];
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

    /* ---------- state ---------------------------------------------------- */

    var order = buildOrder();
    var idx = 0, s1 = null, s2 = null, done = false;
    var streak = 0, attempted = 0, mastered = false, lastCorrect = null;

    function R() { return order[idx % order.length]; }

    function say(str) {
      cap.textContent = '';
      str.split('**').forEach(function (part, i) {
        if (!part) return;
        cap.appendChild(i % 2 ? el('strong', null, part) : document.createTextNode(part));
      });
      sr.textContent = str.replace(/\*\*/g, '');
    }

    function pushState(extra) {
      var r = R(), st = {
        round: idx + 1, kind: r.kind, picked: (s1 || '-') + '|' + (s2 || '-'),
        committed: done, correct: lastCorrect,
        streak: streak, mastered: mastered, attempted: attempted
      };
      if (extra) for (var k in extra) if (extra.hasOwnProperty(k)) st[k] = extra[k];
      root.dataset.svState = JSON.stringify(st);
    }

    function setTri(dir) {
      if (!dir) { tri.setAttribute('opacity', '0'); return; }
      var x = 262, y = TAP + 8;
      tri.setAttribute('points', dir === 'up'
        ? (x + ',' + (y - 9) + ' ' + (x - 5) + ',' + y + ' ' + (x + 5) + ',' + y)
        : (x + ',' + y + ' ' + (x - 5) + ',' + (y - 9) + ' ' + (x + 5) + ',' + (y - 9)));
      tri.setAttribute('opacity', '1');
    }

    function dash(on) {
      [box1, box2].forEach(function (b) {
        if (on) { b.setAttribute('stroke-dasharray', '4 3'); b.setAttribute('stroke', '#b9b2a6'); }
        else { b.removeAttribute('stroke-dasharray'); b.setAttribute('stroke', '#5b564e'); }
      });
    }

    /* draw the circuit as it currently stands */
    function drawStage() {
      var r = R(), d = r.data;
      vinLabel.textContent = 'V in = ' + d.vin + ' V';
      setTri(null);
      vWas.textContent = '';
      mark1.setAttribute('opacity', '0');
      mark2.setAttribute('opacity', '0');
      var formula = 'V out = V in ' + TIMES + ' R2/(R1 + R2)';

      if (r.kind === 'predict') {
        dash(false);
        var st = done ? r.after : r.before;
        var top = d.pos === 'R1';
        (top ? mark1 : mark2).setAttribute('opacity', '1');
        n1.textContent = top ? d.sensor : 'Fixed';
        n2.textContent = top ? 'Fixed' : d.sensor;
        v1.textContent = kohm(st.r1);
        v2.textContent = kohm(st.r2);
        var v = done ? r.vAfter : r.vBefore;
        vTxt.textContent = volts(v);
        if (done) {
          vWas.textContent = 'was ' + volts(r.vBefore);
          setTri(r.vAfter > r.vBefore ? 'up' : 'down');
          eq.textContent = d.vin + ' ' + TIMES + ' ' + st.r2 + '/(' + st.r1 + ' + ' + st.r2 + ') = ' + volts(v);
        } else {
          eq.textContent = formula;
        }
        return;
      }

      /* design round */
      if (!s2) {
        dash(true);
        n1.textContent = '?'; v1.textContent = '';
        n2.textContent = '?'; v2.textContent = '';
        vTxt.textContent = '?';
        eq.textContent = formula;
        return;
      }
      dash(false);
      var chosenTop = s2 === 'R1';
      (chosenTop ? mark1 : mark2).setAttribute('opacity', '1');
      n1.textContent = chosenTop ? d.sensor : 'Fixed';
      n2.textContent = chosenTop ? 'Fixed' : d.sensor;
      if (!done) {
        v1.textContent = chosenTop ? '' : kohm(d.fixed);
        v2.textContent = chosenTop ? kohm(d.fixed) : '';
        vTxt.textContent = '?';
        eq.textContent = formula;
        return;
      }
      var r1 = chosenTop ? d.rTrig : d.fixed, r2 = chosenTop ? d.fixed : d.rTrig;
      v1.textContent = kohm(r1);
      v2.textContent = kohm(r2);
      var vt = vout(d.vin, r1, r2), vo = chosenTop ? r.vOtherTop : r.vOtherBot;
      vTxt.textContent = volts(vt);
      vWas.textContent = d.cond;
      setTri(vt > vo ? 'up' : 'down');
      eq.textContent = d.vin + ' ' + TIMES + ' ' + r2 + '/(' + r1 + ' + ' + r2 + ') = ' + volts(vt);
    }

    function paintOpts() {
      var r = R();
      g1.btns.forEach(function (b, i) {
        b.textContent = r.o1[i][1];
        b.setAttribute('aria-pressed', s1 === r.o1[i][0] ? 'true' : 'false');
        b.disabled = done;
      });
      g2.btns.forEach(function (b, i) {
        b.textContent = r.o2[i][1];
        b.setAttribute('aria-pressed', s2 === r.o2[i][0] ? 'true' : 'false');
        b.disabled = done || !s1;
      });
      g2.node.setAttribute('data-live', s1 ? 'yes' : 'no');
      go.disabled = !done && !(s1 && s2);
    }

    function runLabel() {
      if (mastered) run.textContent = 'Mastered';
      else if (streak === 2) run.textContent = '2 in a row ' + DASH + ' 1 more';
      else if (streak === 1) run.textContent = '1 in a row';
      else run.textContent = '';
    }

    function showRound() {
      var r = R();
      s1 = null; s2 = null; done = false; lastCorrect = null;
      frame.textContent = r.frame;
      g1.q.textContent = r.q1;
      g2.q.textContent = r.q2;
      go.textContent = 'Check';
      paintOpts();
      drawStage();
      say(r.opening);
      runLabel();
      pushState();
    }

    /* ---------- the verdict, derived from the divider -------------------- */

    function judgePredict(r) {
      var d = r.data, W = WORD[d.sensor], correct = (s1 === r.a1) && (s2 === r.a2);
      var s1w = s1 === 'up' ? 'goes up' : 'goes down';
      var s2w = s2 === 'rises' ? 'rises' : 'falls';
      var grew = d.rTo > d.rFrom;
      /* which way the share moves - read straight off the two resistances */
      var reason = d.pos === 'R1'
        ? 'a ' + (grew ? 'bigger' : 'smaller') + ' R1 leaves R2 the ' + (grew ? 'smaller' : 'bigger') + ' share'
        : 'a ' + (grew ? 'bigger' : 'smaller') + ' R2 takes a ' + (grew ? 'bigger' : 'smaller') + ' share';
      var move = 'V_out ' + r.a2 + ', ' + volts(r.vBefore) + ' ' + ARR + ' ' + volts(r.vAfter) + '.';
      /* name the direction of the resistance change, so the rule and the
         round cannot appear to contradict each other when the quantity falls */
      var went = grew ? 'climbs to ' : 'drops to ';
      var head = (correct ? 'Right ' : 'Not quite ') + DASH + ' you said the resistance ' + s1w +
                 ' and V_out ' + s2w + '. ';
      var body;
      if (correct) {
        body = 'The ' + W + ' ' + went + '**' + kohm(d.rTo) + '**, and V_out is **R2' + RSQ +
               's share** of the ' + d.vin + ' V: ' + reason + ', so ' + move;
      } else if (s1 === r.a1) {
        body = 'The resistance is right: it ' + went + kohm(d.rTo) + '. But V_out is **R2' + RSQ +
               's share** of the ' + d.vin + ' V, and the ' + W + ' is ' + d.pos + ' ' + DASH + ' ' + reason +
               ', so ' + move;
      } else if (s2 === r.a2) {
        body = 'V_out does ' + (r.a2 === 'rises' ? 'rise' : 'fall') + ', but not for that reason: ' +
               RULE[d.sensor] + ', so here it ' + went + kohm(d.rTo) + ' and ' + reason + '. V_out: ' +
               volts(r.vBefore) + ' ' + ARR + ' ' + volts(r.vAfter) + '.';
      } else {
        body = cap1(RULE[d.sensor]) + ', so here it ' + went + kohm(d.rTo) + '. V_out is **R2' + RSQ +
               's share**: ' + reason + ', so ' + move;
      }
      return { correct: correct, msg: head + body, mastery: 'Right ' + DASH + ' ' + move + ' ' };
    }

    function judgeDesign(r) {
      var d = r.data, W = WORD[d.sensor], correct = (s1 === r.a1) && (s2 === r.a2);
      var s1w = s1 === 'up' ? 'higher' : 'lower';
      var chosenTop = s2 === 'R1';
      var vChosen = chosenTop ? r.vTrigTop : r.vTrigBot;
      var vChosenOther = chosenTop ? r.vOtherTop : r.vOtherBot;
      var vRight = r.a2 === 'R1' ? r.vTrigTop : r.vTrigBot;
      var head = correct
        ? 'Right ' + DASH + ' you chose ' + s2 + ', with the resistance ' + s1w + ' ' + d.cond + '. '
        : (s2 === r.a2
            ? 'Not quite ' + DASH + ' ' + s2 + ' is the right home, but you called the resistance ' +
              s1w + ' ' + d.cond + '. '
            : 'Not quite ' + DASH + ' you chose ' + s2 + ', with the resistance ' + s1w + ' ' +
              d.cond + '. ');
      var body = '', stated = false;
      if (s1 !== r.a1) {
        body += cap1(RULE[d.sensor]) + ', so ' + d.cond + ' it is **' + kohm(d.rTrig) + '**. ';
        stated = true;
      }
      /* the sensor against the fixed resistor in the trigger condition */
      var bigger = d.rTrig > d.fixed;
      var subject = stated
        ? 'that ' + (bigger ? 'big' : 'small') + ' resistance '
        : 'the ' + W + ' is ' + kohm(d.rTrig) + ' ' + d.cond + ' and ';
      var verb = chosenTop
        ? (bigger ? 'takes most of the ' + d.vin + ' V itself'
                  : 'hands R2 (' + kohm(d.fixed) + ') the bigger share')
        : (bigger ? 'takes most of the ' + d.vin + ' V'
                  : 'leaves R1 (' + kohm(d.fixed) + ') the bigger share');
      body += 'At ' + s2 + ' ' + subject + verb + ': V_out ';
      if (correct || s2 === r.a2) {
        body += volts(vChosen) + ', against ' + volts(vChosenOther) + ' ' + d.other + ' ' + DASH +
                ' the ' + d.device + ' fires.';
      } else {
        body += 'only ' + volts(vChosen) + ' ' + DASH + ' the ' + d.device + ' stays off. At **' +
                r.a2 + '** it reaches ' + volts(vRight) + '.';
      }
      return { correct: correct, msg: head + body,
               mastery: 'Right ' + DASH + ' the ' + W + ' belongs at ' + r.a2 + '. ' };
    }

    var MASTERY = '**Three in a row ' + DASH + ' you have it.** V_out is always R2' + RSQ +
                  's share of V_in, so the same sensor swings the output the opposite way when it sits at R1.';

    function commit() {
      var r = R();
      var v = r.kind === 'predict' ? judgePredict(r) : judgeDesign(r);
      var hadRun = streak;
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
      pushState({ vout: vTxt.textContent });
    }

    /* ---------- wiring ---------------------------------------------------- */

    g1.btns.forEach(function (b, i) {
      b.addEventListener('click', function () {
        if (done) return;
        s1 = R().o1[i][0];
        paintOpts(); pushState();
      });
    });
    g2.btns.forEach(function (b, i) {
      b.addEventListener('click', function () {
        if (done || !s1) return;
        s2 = R().o2[i][0];
        paintOpts(); drawStage(); pushState();
      });
    });
    go.addEventListener('click', function () {
      if (done) { idx++; showRound(); return; }
      if (s1 && s2) commit();
    });
    wrap.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !done && (s1 || s2)) {
        s1 = null; s2 = null;
        paintOpts(); drawStage(); pushState();
      }
    });

    showRound();
  }
};
