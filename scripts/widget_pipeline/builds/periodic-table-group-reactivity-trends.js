/* ============================================================
   Group 1 vs Group 7 reactivity trends
   One mechanism - the distance of the outer shell from the
   nucleus, plus shielding - drives BOTH trends, in opposite
   directions. Every verdict in here is derived from
   moreReactive(a, b, group); nothing is hand-authored.
   ============================================================ */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';

  /* ---------- the model -------------------------------------------------- */

  var G1 = [
    { id: 'li', sym: 'Li', name: 'lithium',   shells: 2, obs: 'fizzed steadily and slowly disappeared, never melting', sig: 'fizzes steadily without melting' },
    { id: 'na', sym: 'Na', name: 'sodium',    shells: 3, obs: 'melted into a ball and darted across the surface',      sig: 'melts into a ball and darts about' },
    { id: 'k',  sym: 'K',  name: 'potassium', shells: 4, obs: 'caught fire and burned with a lilac flame',             sig: 'catches fire with a lilac flame' },
    { id: 'rb', sym: 'Rb', name: 'rubidium',  shells: 5, obs: null, sig: null }
  ];

  var G7 = [
    { id: 'f',  sym: 'F',  name: 'fluorine', shells: 2, reagent: null,                halide: 'fluoride', colour: null },
    { id: 'cl', sym: 'Cl', name: 'chlorine', shells: 3, reagent: 'Chlorine water',    halide: 'chloride', colour: 'colourless' },
    { id: 'br', sym: 'Br', name: 'bromine',  shells: 4, reagent: 'Bromine water',     halide: 'bromide',  colour: 'orange' },
    { id: 'i',  sym: 'I',  name: 'iodine',   shells: 5, reagent: 'Iodine solution',   halide: 'iodide',   colour: 'brown' }
  ];

  /* Down a group each element has one more shell. The outer electron is
     therefore further from the nucleus and behind more shielding.
     Group 1 must LOSE that electron  -> looser hold = MORE reactive.
     Group 7 must GAIN one            -> weaker pull = LESS reactive. */
  function moreReactive(a, b, group) {
    if (group === 1) return a.shells > b.shells ? a : b;
    return a.shells < b.shells ? a : b;
  }
  function displaces(added, target) {
    return added !== target && moreReactive(added, target, 7) === added;
  }

  function byId(list, id) {
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /* ---------- round decks ------------------------------------------------ */

  function deckGroup1() {
    var out = [], i, j;
    for (i = 0; i < G1.length; i++) {
      for (j = i + 1; j < G1.length; j++) out.push({ kind: 'pair', group: 1, a: G1[i], b: G1[j] });
    }
    var seen = ['li', 'na', 'k'];
    for (i = 0; i < seen.length; i++) {
      for (j = 0; j < seen.length; j++) {
        if (i === j) continue;
        out.push({ kind: 'observe', group: 1, subject: byId(G1, seen[i]), other: byId(G1, seen[j]) });
      }
    }
    return shuffle(out);
  }

  function deckGroup7() {
    var out = [], i, j;
    for (i = 0; i < G7.length; i++) {
      for (j = i + 1; j < G7.length; j++) out.push({ kind: 'pair', group: 7, a: G7[i], b: G7[j] });
    }
    /* solution chemistry uses chlorine, bromine and iodine only */
    var sol = ['cl', 'br', 'i'];
    for (i = 0; i < sol.length; i++) {
      for (j = 0; j < sol.length; j++) {
        if (i === j) continue;
        out.push({ kind: 'displace', group: 7, added: byId(G7, sol[i]), target: byId(G7, sol[j]) });
      }
    }
    return shuffle(out);
  }

  /* ---------- geometry --------------------------------------------------- */

  var RAD = [12, 19, 26, 33, 40];
  var CY = 66, CXA = 86, CXB = 254;

  function unit(deg) {
    var r = deg * Math.PI / 180;
    return [Math.cos(r), Math.sin(r)];
  }
  function pts(list) {
    return list.map(function (p) { return (Math.round(p[0] * 10) / 10) + ',' + (Math.round(p[1] * 10) / 10); }).join(' ');
  }
  function head(tx, ty, ux, uy, size) {
    var bx = tx - ux * size, by = ty - uy * size, nx = -uy, ny = ux, h = size * 0.55;
    return pts([[tx, ty], [bx + nx * h, by + ny * h], [bx - nx * h, by - ny * h]]);
  }

  function el(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
    return n;
  }

  /* ---------- the widget ------------------------------------------------- */

  window.SVWidget = {
    meta: {
      id: 'periodic-table-group-reactivity-trends',
      title: 'Reactivity down a group',
      teaches: 'Reactivity rises down Group 1 and falls down Group 7, because the same growing atom makes an outer electron easier to lose and an incoming one harder to gain.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};

      /* accent: read from our own node first (two layers set --accent) */
      var acc = '';
      try { acc = (getComputedStyle(root).getPropertyValue('--accent') || '').trim(); } catch (e) { acc = ''; }
      if (!/^#[0-9a-f]{6}$/i.test(acc)) acc = /^#[0-9a-f]{6}$/i.test(ctx.accent || '') ? ctx.accent : '#8a6a4f';
      var still = !!ctx.reducedMotion;

      root.classList.add('svw-ptg');
      root.style.setProperty('--svwptg-acc', acc);

      var style = document.createElement('style');
      style.textContent = [
        '.svw-ptg{max-width:520px;margin:0 auto;color:#2d2a26;',
        'font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif}',
        '.svw-ptg *{box-sizing:border-box}',
        '.svw-ptg .k{margin:0 0 .16rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;',
        'text-transform:uppercase;color:' + acc + '}',
        '.svw-ptg .t{margin:0 0 .4rem;font-family:"Source Serif 4",Georgia,serif;font-weight:600;',
        'font-size:1.2rem;line-height:1.2}',
        '.svw-ptg .frame{margin:0 0 .55rem;font-size:.86rem;line-height:1.45;color:#3b3630}',
        '.svw-ptg .stage{display:block;width:100%;max-width:376px;height:auto;margin:0 auto .5rem}',
        '.svw-ptg .sh{fill:none;stroke:#ddd7cd;stroke-width:1.2}',
        '.svw-ptg .nuc{fill:#2d2a26}',
        '.svw-ptg .el{fill:' + acc + '}',
        '.svw-ptg .arr{stroke:#5b564e;stroke-width:1.6;stroke-linecap:round}',
        '.svw-ptg .arrh{fill:#5b564e}',
        '.svw-ptg .sym{font-family:Inter,system-ui,sans-serif;font-size:14px;font-weight:700;fill:#2d2a26}',
        '.svw-ptg .sub{font-family:Inter,system-ui,sans-serif;font-size:10.5px;fill:#8d8880}',
        '.svw-ptg .arc{fill:none;stroke:#8d8880;stroke-width:1.6;stroke-dasharray:4 3}',
        '.svw-ptg .arclbl{font-family:Inter,system-ui,sans-serif;font-size:11px;font-weight:600;fill:#5b564e}',
        '.svw-ptg .xline{stroke:#5b564e;stroke-width:1.8;stroke-linecap:round}',
        '.svw-ptg .win .sh{stroke:' + acc + ';stroke-width:1.9}',
        '.svw-ptg .win .sym{fill:' + acc + '}',
        '.svw-ptg .go .arc{stroke:' + acc + ';stroke-dasharray:none}',
        '.svw-ptg .go .arrh{fill:' + acc + '}',
        '.svw-ptg .opts{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;margin:0 0 .5rem}',
        '.svw-ptg .opt{font-family:inherit;font-size:.82rem;font-weight:600;line-height:1.25;',
        'padding:.5rem .55rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;',
        'color:#2d2a26;cursor:pointer;text-align:center' + (still ? '' : ';transition:background .12s,border-color .12s') + '}',
        '.svw-ptg .opt.you{background:#2d2a26;border-color:#2d2a26;color:#fff}',
        '.svw-ptg .opt.key{border-color:' + acc + ';border-width:2px;padding:calc(.5rem - 1px) calc(.55rem - 1px)}',
        '.svw-ptg .opt:disabled{cursor:default}',
        '.svw-ptg .row{display:flex;align-items:center;gap:.6rem;margin:0 0 .5rem;flex-wrap:wrap}',
        '.svw-ptg .prim{font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;',
        'border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
        '.svw-ptg .prim:disabled{background:#faf8f5;border-color:#ddd7cd;color:#a9a29a;cursor:default}',
        '.svw-ptg .run{font-size:.78rem;color:#8d8880;font-variant-numeric:tabular-nums}',
        '.svw-ptg .run.done{color:#4f7d63;font-weight:600}',
        '.svw-ptg .cap{margin:0;font-size:.84rem;line-height:1.5;color:#3b3630;background:#faf8f5;',
        'border:1px solid #efe9e0;border-radius:12px;padding:.6rem .7rem;min-height:4.8rem}',
        '.svw-ptg .cap strong{font-weight:700;color:#2d2a26}',
        '.svw-ptg .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);',
        'white-space:nowrap;border:0;padding:0;margin:-1px}'
      ].join('');
      root.appendChild(style);

      /* ---- static DOM, built once ---- */
      var kick = document.createElement('p'); kick.className = 'k'; kick.textContent = 'Groups 1 and 7';
      var title = document.createElement('h3'); title.className = 't'; title.textContent = 'Reactivity down a group';
      var frame = document.createElement('p'); frame.className = 'frame';

      var svg = el('svg', { 'class': 'stage', viewBox: '0 0 340 150', role: 'img' });
      var svgTitle = el('title', {}); svg.appendChild(svgTitle);

      function buildAtom(cx) {
        var g = el('g', {}), shells = [], i;
        for (i = 0; i < 5; i++) shells.push(g.appendChild(el('circle', { 'class': 'sh', cx: cx, cy: CY, r: RAD[i] })));
        var shaft = g.appendChild(el('line', { 'class': 'arr' }));
        var hd = g.appendChild(el('polygon', { 'class': 'arrh' }));
        g.appendChild(el('circle', { 'class': 'nuc', cx: cx, cy: CY, r: 6.5 }));
        var dot = g.appendChild(el('circle', { 'class': 'el', r: 4.2 }));
        var sym = g.appendChild(el('text', { 'class': 'sym', x: cx, y: CY + 62, 'text-anchor': 'middle' }));
        var sub = g.appendChild(el('text', { 'class': 'sub', x: cx, y: CY + 76, 'text-anchor': 'middle' }));
        return { g: g, cx: cx, shells: shells, shaft: shaft, hd: hd, dot: dot, sym: sym, sub: sub };
      }
      var atomL = buildAtom(CXA), atomR = buildAtom(CXB);
      svg.appendChild(atomL.g); svg.appendChild(atomR.g);

      var linkG = el('g', {});
      var arc = linkG.appendChild(el('path', { 'class': 'arc' }));
      var arcHd = linkG.appendChild(el('polygon', { 'class': 'arrh' }));
      var xa = linkG.appendChild(el('line', { 'class': 'xline' }));
      var xb = linkG.appendChild(el('line', { 'class': 'xline' }));
      var arcLbl = linkG.appendChild(el('text', { 'class': 'arclbl', 'text-anchor': 'middle' }));
      svg.appendChild(linkG);

      var opts = document.createElement('div'); opts.className = 'opts';
      var btn0 = document.createElement('button'); btn0.className = 'opt'; btn0.type = 'button';
      var btn1 = document.createElement('button'); btn1.className = 'opt'; btn1.type = 'button';
      opts.appendChild(btn0); opts.appendChild(btn1);

      var row = document.createElement('div'); row.className = 'row';
      var prim = document.createElement('button'); prim.className = 'prim'; prim.type = 'button'; prim.textContent = 'Check';
      var run = document.createElement('span'); run.className = 'run';
      row.appendChild(prim); row.appendChild(run);

      var capEl = document.createElement('p'); capEl.className = 'cap';
      var sr = document.createElement('p'); sr.className = 'sr'; sr.setAttribute('aria-live', 'polite');

      root.appendChild(kick); root.appendChild(title); root.appendChild(frame);
      root.appendChild(svg); root.appendChild(opts); root.appendChild(row);
      root.appendChild(capEl); root.appendChild(sr);

      /* ---- state ---- */
      var d1 = deckGroup1(), d7 = deckGroup7();
      var S = { n: 0, streak: 0, best: 0, attempted: 0, mastered: false, picked: -1, done: false, round: null };

      function nextRound() {
        var useG1 = (S.n % 2 === 0);
        if (useG1 && !d1.length) d1 = deckGroup1();
        if (!useG1 && !d7.length) d7 = deckGroup7();
        S.n++;
        return (useG1 ? d1 : d7).pop();
      }

      /* ---- painting ---- */

      function paintAtom(a, spec) {
        var R = RAD[spec.shells - 1], i;
        for (i = 0; i < 5; i++) a.shells[i].style.display = i < spec.shells ? '' : 'none';
        a.sym.textContent = spec.sym;
        a.sub.textContent = spec.sub;
        a.g.classList.remove('win');

        var u = unit(spec.ang === undefined ? -52 : spec.ang);
        if (spec.dot === 'none') { a.dot.style.display = 'none'; }
        else {
          a.dot.style.display = '';
          var dr = spec.dot === 'outside' ? R + 25 : R;
          a.dot.setAttribute('cx', Math.round((a.cx + u[0] * dr) * 10) / 10);
          a.dot.setAttribute('cy', Math.round((CY + u[1] * dr) * 10) / 10);
        }
        if (spec.arrow === 'none') {
          a.shaft.style.display = 'none'; a.hd.style.display = 'none';
        } else {
          a.shaft.style.display = ''; a.hd.style.display = '';
          var s1, s2, tip, dir;
          if (spec.arrow === 'out') { s1 = R + 8; s2 = R + 16; tip = R + 22; dir = 1; }
          else { s1 = R + 20; s2 = R + 13; tip = R + 6; dir = -1; }
          a.shaft.setAttribute('x1', a.cx + u[0] * s1); a.shaft.setAttribute('y1', CY + u[1] * s1);
          a.shaft.setAttribute('x2', a.cx + u[0] * s2); a.shaft.setAttribute('y2', CY + u[1] * s2);
          a.hd.setAttribute('points', head(a.cx + u[0] * tip, CY + u[1] * tip, u[0] * dir, u[1] * dir, 7));
        }
      }

      function hideLink() { linkG.style.display = 'none'; }

      function paintLink(addedShells, targetShells, phase) {
        linkG.style.display = '';
        var RA = RAD[addedShells - 1], RB = RAD[targetShells - 1];
        var uR = unit(-128), uL = unit(-52);
        var sx = CXB + uR[0] * (RB + 9), sy = CY + uR[1] * (RB + 9);
        var ex = CXA + uL[0] * (RA + 9), ey = CY + uL[1] * (RA + 9);
        var qx = (sx + ex) / 2, qy = Math.min(sy, ey) - 18;
        arc.setAttribute('d', 'M' + sx.toFixed(1) + ',' + sy.toFixed(1) + ' Q' + qx.toFixed(1) + ',' + qy.toFixed(1) + ' ' + ex.toFixed(1) + ',' + ey.toFixed(1));
        var tx = ex - qx, ty = ey - qy, m = Math.sqrt(tx * tx + ty * ty);
        arcHd.setAttribute('points', head(ex, ey, tx / m, ty / m, 7));
        var px = 0.25 * sx + 0.5 * qx + 0.25 * ex, py = 0.25 * sy + 0.5 * qy + 0.25 * ey;
        arcLbl.setAttribute('x', px.toFixed(1)); arcLbl.setAttribute('y', (py - 7).toFixed(1));

        var crossed = phase === 'no';
        arcHd.style.display = crossed ? 'none' : '';
        xa.style.display = xb.style.display = crossed ? '' : 'none';
        if (crossed) {
          /* sit the cross below the label so the two never touch */
          var cyx = py + 3.5, k = 5.5;
          xa.setAttribute('x1', px - k); xa.setAttribute('y1', cyx - k);
          xa.setAttribute('x2', px + k); xa.setAttribute('y2', cyx + k);
          xb.setAttribute('x1', px + k); xb.setAttribute('y1', cyx - k);
          xb.setAttribute('x2', px - k); xb.setAttribute('y2', cyx + k);
        }
        arcLbl.textContent = phase === 'ask' ? '?' : (phase === 'yes' ? 'moves' : 'stays');
        svg.classList.toggle('go', phase === 'yes');
      }

      /* ---- caption: plain text with **bold** spans, no innerHTML ---- */
      function say(node, text) {
        while (node.firstChild) node.removeChild(node.firstChild);
        var parts = String(text).split('**');
        for (var i = 0; i < parts.length; i++) {
          if (!parts[i]) continue;
          if (i % 2) {
            var b = document.createElement('strong'); b.textContent = parts[i]; node.appendChild(b);
          } else node.appendChild(document.createTextNode(parts[i]));
        }
      }
      function plain(text) { return String(text).replace(/\*\*/g, ''); }

      /* ---- round rendering ---- */

      function render() {
        var r = S.round;
        S.picked = -1; S.done = false;
        prim.textContent = 'Check';
        prim.disabled = true;
        btn0.disabled = btn1.disabled = false;
        btn0.className = btn1.className = 'opt';
        btn0.setAttribute('aria-pressed', 'false'); btn1.setAttribute('aria-pressed', 'false');
        svg.classList.remove('go');

        if (r.kind === 'displace') {
          frame.textContent = r.added.reagent + ' is added to potassium ' + r.target.halide +
            ' solution. Predict whether a displacement reaction happens.';
          paintAtom(atomL, { sym: r.added.sym, shells: r.added.shells, sub: r.added.shells + ' shells · added', dot: 'none', arrow: 'none' });
          paintAtom(atomR, { sym: r.target.sym + '⁻', shells: r.target.shells, sub: r.target.shells + ' shells · in solution', dot: 'shell', arrow: 'none', ang: -128 });
          paintLink(r.added.shells, r.target.shells, 'ask');
          btn0.textContent = 'Reaction happens'; btn1.textContent = 'No reaction';
          svgTitle.textContent = 'A ' + r.added.name + ' atom with ' + r.added.shells + ' shells beside a ' +
            r.target.halide + ' ion with ' + r.target.shells + ' shells, and a spare electron between them.';
          say(capEl, 'The ' + r.target.halide + ' ion is already holding the spare electron. It only moves across if the added halogen’s nucleus grips an **incoming** electron more tightly than ' + r.target.name + '’s does.');
        } else {
          var L = r.left, R2 = r.right, g = r.group;
          if (r.kind === 'observe') {
            frame.textContent = 'A piece of one of these two metals was dropped into water. It ' +
              r.subject.obs + '. Predict which metal it was.';
          } else if (g === 1) {
            frame.textContent = cap(L.name) + ' and ' + R2.name + ' are both in Group 1. Predict which one reacts more vigorously with water.';
          } else {
            frame.textContent = cap(L.name) + ' and ' + R2.name + ' are both in Group 7. Predict which one is the more reactive.';
          }
          var mode = g === 1 ? { dot: 'shell', arrow: 'out' } : { dot: 'outside', arrow: 'in' };
          paintAtom(atomL, { sym: L.sym, shells: L.shells, sub: L.shells + ' shells', dot: mode.dot, arrow: mode.arrow });
          paintAtom(atomR, { sym: R2.sym, shells: R2.shells, sub: R2.shells + ' shells', dot: mode.dot, arrow: mode.arrow });
          hideLink();
          btn0.textContent = cap(L.name); btn1.textContent = cap(R2.name);
          svgTitle.textContent = cap(L.name) + ' has ' + L.shells + ' electron shells, ' + R2.name + ' has ' +
            R2.shells + '. The arrow shows the electron ' + (g === 1 ? 'leaving each atom.' : 'arriving at each atom.');
          if (g === 1) {
            say(capEl, 'Each ring is an electron shell. A Group 1 atom reacts by **losing** its single outer electron — that is the arrow leaving. Add a shell and that electron sits further out, behind more shielding.');
          } else {
            say(capEl, 'Each ring is an electron shell. A Group 7 atom reacts by **gaining** one electron — that is the arrow coming in. Add a shell and the incoming electron lands further out, behind more shielding.');
          }
        }
        paintRun();
        stamp();
      }

      function paintRun() {
        if (S.mastered) { run.className = 'run done'; run.textContent = 'You have it.'; return; }
        run.className = 'run';
        if (!S.attempted) { run.textContent = ''; return; }
        if (S.streak === 0) run.textContent = 'Streak back to 0.';
        else if (S.streak === 1) run.textContent = '1 in a row — two more.';
        else run.textContent = '2 in a row — one more.';
      }

      function stamp() {
        root.dataset.svState = JSON.stringify({
          round: S.n,
          type: S.round ? S.round.kind : null,
          group: S.round ? S.round.group : null,
          picked: S.picked,
          committed: S.done,
          streak: S.streak,
          mastered: S.mastered,
          attempted: S.attempted
        });
      }

      /* ---- verdicts, all derived from the model ---- */

      function correctIndex(r) {
        if (r.kind === 'displace') return displaces(r.added, r.target) ? 0 : 1;
        var win = r.kind === 'observe' ? r.subject : moreReactive(r.left, r.right, r.group);
        return win === r.left ? 0 : 1;
      }

      function feedback(r, pickedIdx, ok) {
        var lead = ok ? 'Right — ' : 'Not quite — you ';

        if (r.kind === 'displace') {
          var yes = displaces(r.added, r.target);
          var A = r.added, T = r.target;
          var grip = A.shells < T.shells ? 'more' : 'less';
          var mech = cap(A.name) + ' has **' + A.shells + ' shells** to ' + T.name + '’s **' + T.shells +
            '**, so its nucleus grips an incoming electron ' + grip + ' tightly than ' + T.name + '’s does. ';
          var outcome = yes
            ? cap(A.name) + ' takes the electron from the ' + T.halide + ' ion and the solution turns **' + T.colour + '** as ' + T.name + ' is displaced.'
            : 'The ' + T.halide + ' ion keeps its electron, so the colour does not change.';
          if (ok) return lead + (yes ? 'a reaction happens. ' : 'no reaction. ') + mech + outcome;
          return lead + 'predicted ' + (pickedIdx === 0 ? 'a reaction' : 'no reaction') + '. ' + mech + outcome;
        }

        var L = r.left, R2 = r.right;
        var key = r.kind === 'observe' ? r.subject : moreReactive(L, R2, r.group);
        var other = key === L ? R2 : L;
        var picked = pickedIdx === 0 ? L : R2;

        if (r.kind === 'observe') {
          var harder = moreReactive(key, other, 1) === key;
          var contrast = harder
            ? cap(other.name) + ' holds its outer electron more tightly, so it only ' + other.sig + '.'
            : cap(other.name) + ' would have gone further still — it ' + other.sig + '.';
          var line = cap(key.name) + ' has **' + key.shells + ' shells** to ' + other.name + '’s **' + other.shells +
            '**, and more shells means the outer electron is further out and more shielded. ' + contrast;
          if (ok) return lead + key.name + '. ' + line;
          return lead + 'said ' + picked.name + '; it was **' + key.name + '**. ' + line;
        }

        if (r.group === 1) {
          var g1line = cap(key.name) + ' has **' + key.shells + ' shells** to ' + other.name + '’s **' + other.shells +
            '**, so its outer electron sits further from the nucleus and behind more shielding. That electron is **lost** more easily, so reactivity **rises** down Group 1.';
          if (ok) return lead + key.name + '. ' + g1line;
          return lead + 'said ' + picked.name + '; it is **' + key.name + '**. ' + g1line;
        }

        var g7line = cap(key.name) + ' has only **' + key.shells + ' shells** to ' + other.name + '’s **' + other.shells +
          '**, so an incoming electron lands closer to the nucleus and behind less shielding. It is **gained** more easily, so reactivity **falls** down Group 7.';
        if (ok) return lead + key.name + '. ' + g7line;
        return lead + 'said ' + picked.name + ', the lower one — but lower means **more** shells, not a stronger pull. ' + g7line;
      }

      var MASTERY = 'Three in a row — you have it. One atom change runs both trends: an extra shell puts the outer electron further out, behind more shielding. Group 1 **loses** it more easily, so reactivity rises; Group 7 **gains** one less easily, so reactivity falls.';

      /* ---- interaction ---- */

      function pick(i) {
        if (S.done) return;
        S.picked = i;
        btn0.className = 'opt' + (i === 0 ? ' you' : '');
        btn1.className = 'opt' + (i === 1 ? ' you' : '');
        btn0.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
        btn1.setAttribute('aria-pressed', i === 1 ? 'true' : 'false');
        prim.disabled = false;
        stamp();
      }

      function commit() {
        var r = S.round, key = correctIndex(r), ok = S.picked === key;
        S.done = true;
        S.attempted++;
        S.streak = ok ? S.streak + 1 : 0;
        if (S.streak > S.best) S.best = S.streak;
        var justMastered = false;
        if (S.streak >= 3 && !S.mastered) { S.mastered = true; justMastered = true; }

        btn0.disabled = btn1.disabled = true;
        (key === 0 ? btn0 : btn1).classList.add('key');

        if (r.kind === 'displace') paintLink(r.added.shells, r.target.shells, displaces(r.added, r.target) ? 'yes' : 'no');
        else (key === 0 ? atomL : atomR).g.classList.add('win');

        var msg = (justMastered || (S.mastered && ok)) && ok
          ? feedback(r, S.picked, ok).split('. ')[0] + '. ' + MASTERY
          : feedback(r, S.picked, ok);
        say(capEl, msg);
        sr.textContent = plain(msg);

        prim.textContent = S.mastered ? 'Another anyway' : 'Next round';
        prim.disabled = false;
        paintRun();
        stamp();
      }

      btn0.addEventListener('click', function () { pick(0); });
      btn1.addEventListener('click', function () { pick(1); });
      prim.addEventListener('click', function () {
        if (!S.done) { if (S.picked >= 0) commit(); return; }
        S.round = prepare(nextRound());
        render();
      });

      /* randomise which candidate is drawn on the left */
      function prepare(r) {
        if (r.kind === 'pair') {
          var flip = Math.random() < 0.5;
          r.left = flip ? r.b : r.a; r.right = flip ? r.a : r.b;
        } else if (r.kind === 'observe') {
          var f2 = Math.random() < 0.5;
          r.left = f2 ? r.other : r.subject; r.right = f2 ? r.subject : r.other;
        }
        return r;
      }

      S.round = prepare(nextRound());
      render();
    }
  };
})();
