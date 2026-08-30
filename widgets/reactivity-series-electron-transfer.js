/* ==========================================================================
   Reactivity series as electron transfer.

   A metal's place in the series IS how readily it lets go of its outer
   electrons. The student is given a strip of one metal in a solution of
   another metal's compound and must commit to two things before anything
   is revealed: does a reaction happen, and which metal ends up as the
   positive ions. The stage draws the series as an axis of electron-losing
   tendency, and on commit puts the two half-equations at the positions of
   the metals they describe, with the electron arrow running between them.

   Every non-ASCII character is written as an escape so the file is safe
   whatever charset it is served under.
   ========================================================================== */
(function () {
  'use strict';

  var ARROW = '\u2192';   /* right arrow */
  var MINUS = '\u2212';   /* minus sign, for the electron charge */
  var DASH  = '\u2014';   /* em dash */
  var RSQ   = '\u2019';   /* right single quote */

  /* Standard GCSE series, most reactive first. Charges are the ions these
     metals actually form in the salts used below. */
  var METALS = [
    { sym: 'K',  name: 'potassium', ion: '+'  },
    { sym: 'Na', name: 'sodium',    ion: '+'  },
    { sym: 'Ca', name: 'calcium',   ion: '2+' },
    { sym: 'Mg', name: 'magnesium', ion: '2+' },
    { sym: 'Al', name: 'aluminium', ion: '3+' },
    { sym: 'Zn', name: 'zinc',      ion: '2+' },
    { sym: 'Fe', name: 'iron',      ion: '2+' },
    { sym: 'Cu', name: 'copper',    ion: '2+' }
  ];

  /* m = metal strip added, s = metal already present as ions in the
     solution. A reaction happens exactly when m sits above s (m < s).
     Only reactions a school lab really shows: no group 1 or 2 metals in
     water, and aluminium is used with a chloride, which is what gets past
     its oxide layer. */
  var ROUNDS = [
    { m: 5, s: 7, salt: 'copper(II) sulfate',  col: 'blue ',
      obs: 'the blue fades and pink-brown copper coats the zinc' },
    { m: 3, s: 6, salt: 'iron(II) sulfate',    col: 'pale green ',
      obs: 'the pale green fades and grey iron coats the magnesium' },
    { m: 6, s: 7, salt: 'copper(II) sulfate',  col: 'blue ',
      obs: 'the blue fades and copper coats the iron nail' },
    { m: 4, s: 7, salt: 'copper(II) chloride', col: 'blue-green ',
      obs: 'the blue-green fades and copper coats the aluminium' },
    { m: 5, s: 6, salt: 'iron(II) sulfate',    col: 'pale green ',
      obs: 'the pale green fades and grey iron collects on the zinc' },
    { m: 3, s: 7, salt: 'copper(II) sulfate',  col: 'blue ',
      obs: 'the blue fades quickly and copper coats the magnesium' },
    { m: 7, s: 3, salt: 'magnesium sulfate',   col: 'colourless ',
      obs: 'the copper stays shiny and the solution stays colourless' },
    { m: 7, s: 5, salt: 'zinc sulfate',        col: 'colourless ',
      obs: 'the copper stays shiny and the solution stays colourless' },
    { m: 6, s: 3, salt: 'magnesium chloride',  col: 'colourless ',
      obs: 'the iron stays as it was and the solution stays colourless' },
    { m: 7, s: 4, salt: 'aluminium sulfate',   col: 'colourless ',
      obs: 'the copper stays shiny and the solution stays colourless' }
  ];

  /* Six reactions, four non-reactions, dealt so that no more than two of a
     kind arrive in a row. Guessing "it always reacts" cannot survive. */
  var PATTERN = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0];

  var NS = 'http://www.w3.org/2000/svg';
  var VBW = 320, VBH = 107;
  var XL = 18, XR = 302;
  var Y_AX = 12, Y_AXS = 26, Y_SYM = 44, Y_LINE = 52,
      Y_ARL = 67, Y_ARR = 74, Y_ROWA = 90, Y_ROWB = 104;

  function chargeN(ion) { return ion === '+' ? 1 : parseInt(ion, 10); }
  function cap1(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function mx(i) { return XL + (XR - XL) * i / (METALS.length - 1); }

  function el(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt != null) e.textContent = txt;
    return e;
  }
  function sv(tag, attrs) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) if (attrs.hasOwnProperty(k)) e.setAttribute(k, attrs[k]);
    return e;
  }

  /* A five-part text run so a superscript can be mutated without rebuilding
     the node: plain, super, plain, super, plain. dy shifts cancel out. */
  function runText(cls, y) {
    var t = sv('text', { class: cls, y: y, x: XL, 'text-anchor': 'start' });
    var parts = [];
    for (var i = 0; i < 5; i++) {
      var a = { };
      if (i === 1 || i === 3) { a.dy = '-3.6'; a['font-size'] = '7.6'; }
      if (i === 2 || i === 4) { a.dy = '3.6'; }
      var sp = sv('tspan', a);
      t.appendChild(sp);
      parts.push(sp);
    }
    t.parts = parts;
    return t;
  }
  function setRun(t, segs) {
    for (var i = 0; i < 5; i++) t.parts[i].textContent = segs[i] || '';
  }
  function placeRun(t, x, key) {
    var ax, at;
    if (x < 78) { ax = 16; at = 'start'; }
    else if (x > 242) { ax = 304; at = 'end'; }
    else { ax = x; at = 'middle'; }
    t.setAttribute('x', ax);
    t.setAttribute('text-anchor', at);
    if (!key) return;
    var w = 0;
    try { w = t.getComputedTextLength(); } catch (e) { w = 0; }
    var left = at === 'start' ? ax : (at === 'end' ? ax - w : ax - w / 2);
    key.setAttribute('cx', Math.max(4, left - 6));
  }

  function halfMetal(i) {
    var M = METALS[i], n = chargeN(M.ion);
    return [M.sym + ' ' + ARROW + ' ' + M.sym, M.ion,
            ' + ' + (n > 1 ? n : '') + 'e', MINUS, ''];
  }
  function halfIon(i) {
    var M = METALS[i], n = chargeN(M.ion);
    return [M.sym, M.ion, ' + ' + (n > 1 ? n : '') + 'e', MINUS,
            ' ' + ARROW + ' ' + M.sym];
  }

  var CSS = [
    '.svw-rset{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26}',
    '.svw-rset *{box-sizing:border-box}',
    '.svw-rset .k{margin:0 0 .15rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase}',
    '.svw-rset .t{margin:0 0 .4rem;font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.18}',
    '.svw-rset .frame{margin:0 0 .6rem;font-size:.86rem;line-height:1.45;color:#3d3a34}',
    '.svw-rset .frame strong{font-weight:600}',
    '.svw-rset .stage{margin:0 auto .55rem;max-width:400px}',
    '.svw-rset .stage svg{display:block;width:100%;height:auto}',
    '.svw-rset .ax{font-size:11px;font-weight:700;letter-spacing:.05em;fill:#8d8880}',
    '.svw-rset .axs{font-size:11px;fill:#8d8880}',
    '.svw-rset .sym{font-size:13px;font-weight:700;fill:#b0a99e}',
    '.svw-rset .sym.on{fill:#2d2a26}',
    '.svw-rset .rowl{font-size:11px;fill:#3d3a34}',
    '.svw-rset .arl{font-size:11px;font-weight:600;fill:#8d8880}',
    '.svw-rset .step{margin:0 0 .45rem}',
    '.svw-rset .step.off{opacity:.4}',
    '.svw-rset .lab{margin:0 0 .28rem;font-size:.78rem;font-weight:600;color:#5b564e;display:flex;align-items:center;gap:.38rem}',
    '.svw-rset .chip{display:inline-flex;align-items:center;justify-content:center;width:1.02rem;height:1.02rem;border-radius:50%;background:#efe9e0;color:#5b564e;font-size:.66rem;font-weight:700;flex:0 0 auto}',
    '.svw-rset .opts{display:flex;flex-wrap:wrap;gap:.4rem}',
    '.svw-rset .opt{flex:1 1 8rem;min-width:0;font-family:inherit;font-size:.82rem;font-weight:600;line-height:1.2;padding:.5rem .55rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;text-align:center;transition:background .12s ease,color .12s ease}',
    '.svw-rset.rm .opt{transition:none}',
    '.svw-rset .opt .f{font-weight:400;color:#8d8880}',
    '.svw-rset .opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
    '.svw-rset .opt[aria-pressed="true"] .f{color:#d8d2c8}',
    '.svw-rset .opt[disabled]{cursor:default}',
    '.svw-rset .commit{display:flex;align-items:center;gap:.65rem;margin:.5rem 0 .55rem}',
    '.svw-rset .go{font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem 1.05rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer;flex:0 0 auto}',
    '.svw-rset .go[disabled]{opacity:.32;cursor:default}',
    '.svw-rset .run{font-size:.76rem;color:#8d8880;font-variant-numeric:tabular-nums}',
    '.svw-rset .cap{margin:0;padding-top:.5rem;border-top:1px solid #efe9e0;font-size:.86rem;line-height:1.5;color:#3d3a34;min-height:4.6em}',
    '.svw-rset .cap strong{font-weight:600;color:#2d2a26}',
    '.svw-rset .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
  ].join('');

  window.SVWidget = {
    meta: {
      id: 'reactivity-series-electron-transfer',
      title: 'Which way do the electrons go?',
      teaches: 'A metal' + RSQ + 's place in the reactivity series is how readily it loses ' +
               'electrons, which is why a more reactive metal displaces a less reactive ' +
               'one from its compound.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;
      var uid = 'svwrs' + Math.floor(Math.random() * 1e9).toString(36);

      /* ---------------------------------------------------------- shell */
      var wrap = el('div', 'svw-rset' + (reduced ? ' rm' : ''));
      var style = document.createElement('style');
      style.textContent = CSS;
      wrap.appendChild(style);

      var kick = el('p', 'k', 'Reactivity series');
      kick.style.color = accent;
      wrap.appendChild(kick);
      wrap.appendChild(el('h3', 't', 'Which way do the electrons go?'));

      var frame = el('p', 'frame');
      frame.appendChild(document.createTextNode('A strip of '));
      var fMetal = el('strong');
      frame.appendChild(fMetal);
      frame.appendChild(document.createTextNode(' is placed in '));
      var fCol = el('span');
      frame.appendChild(fCol);
      var fSalt = el('strong');
      frame.appendChild(fSalt);
      frame.appendChild(document.createTextNode(
        ' solution. Predict what happens, and where any electrons go.'));
      wrap.appendChild(frame);

      /* ---------------------------------------------------------- stage */
      var stage = el('div', 'stage');
      var svg = sv('svg', {
        viewBox: '0 0 ' + VBW + ' ' + VBH,
        preserveAspectRatio: 'xMidYMid meet',
        role: 'img'
      });
      var svgTitle = sv('title', {});
      svg.appendChild(svgTitle);

      var defs = sv('defs', {});
      [['a', accent], ['b', '#b3aca1']].forEach(function (p) {
        var mk = sv('marker', {
          id: uid + '-' + p[0], viewBox: '0 0 8 8', refX: '7.4', refY: '4',
          markerWidth: '4.6', markerHeight: '4.6', orient: 'auto'
        });
        mk.appendChild(sv('path', { d: 'M0 0 L8 4 L0 8 Z', fill: p[1] }));
        defs.appendChild(mk);
      });
      svg.appendChild(defs);

      var axL = sv('text', { class: 'ax', x: 16, y: Y_AX, 'text-anchor': 'start' });
      axL.textContent = 'MORE REACTIVE';
      var axR = sv('text', { class: 'ax', x: 304, y: Y_AX, 'text-anchor': 'end' });
      axR.textContent = 'LESS REACTIVE';
      var axLs = sv('text', { class: 'axs', x: 16, y: Y_AXS, 'text-anchor': 'start' });
      axLs.textContent = 'loses electrons readily';
      var axRs = sv('text', { class: 'axs', x: 304, y: Y_AXS, 'text-anchor': 'end' });
      axRs.textContent = 'holds them tightly';
      svg.appendChild(axL); svg.appendChild(axR);
      svg.appendChild(axLs); svg.appendChild(axRs);

      svg.appendChild(sv('line', {
        x1: 16, y1: Y_LINE, x2: 304, y2: Y_LINE, stroke: '#ddd7cd', 'stroke-width': '1.2'
      }));

      var symNodes = [];
      METALS.forEach(function (M, i) {
        var x = mx(i);
        svg.appendChild(sv('line', {
          x1: x, y1: Y_LINE - 3.5, x2: x, y2: Y_LINE + 3.5,
          stroke: '#ddd7cd', 'stroke-width': '1.2'
        }));
        var s = sv('text', { class: 'sym', x: x, y: Y_SYM, 'text-anchor': 'middle' });
        s.textContent = M.sym;
        svg.appendChild(s);
        symNodes.push(s);
      });

      var dotM = sv('circle', { r: '3.4', cy: Y_LINE, cx: -20, fill: accent });
      var dotS = sv('circle', {
        r: '3.4', cy: Y_LINE, cx: -20, fill: '#fff',
        stroke: accent, 'stroke-width': '1.6'
      });
      svg.appendChild(dotM); svg.appendChild(dotS);

      var arrow = sv('line', {
        x1: 0, y1: Y_ARR, x2: 0, y2: Y_ARR, stroke: accent,
        'stroke-width': '1.6', opacity: '0'
      });
      var cross1 = sv('line', {
        x1: 0, y1: 0, x2: 0, y2: 0, stroke: '#b3aca1', 'stroke-width': '1.6', opacity: '0'
      });
      var cross2 = sv('line', {
        x1: 0, y1: 0, x2: 0, y2: 0, stroke: '#b3aca1', 'stroke-width': '1.6', opacity: '0'
      });
      svg.appendChild(arrow); svg.appendChild(cross1); svg.appendChild(cross2);

      var keyA = sv('circle', { r: '2.6', cy: Y_ROWA - 3.4, cx: -20, fill: accent });
      var keyB = sv('circle', { r: '2.6', cy: Y_ROWB - 3.4, cx: -20, fill: '#fff',
                                stroke: accent, 'stroke-width': '1.4' });
      svg.appendChild(keyA); svg.appendChild(keyB);

      var arLab = runText('arl', Y_ARL);
      var rowA = runText('rowl', Y_ROWA);
      var rowB = runText('rowl', Y_ROWB);
      svg.appendChild(arLab); svg.appendChild(rowA); svg.appendChild(rowB);

      stage.appendChild(svg);
      wrap.appendChild(stage);

      /* -------------------------------------------------------- controls */
      function stepBlock(n, question) {
        var box = el('div', 'step');
        var lab = el('p', 'lab');
        lab.appendChild(el('span', 'chip', String(n)));
        lab.appendChild(el('span', null, question));
        box.appendChild(lab);
        var opts = el('div', 'opts');
        box.appendChild(opts);
        var a = el('button', 'opt'), b = el('button', 'opt');
        a.type = 'button'; b.type = 'button';
        a.setAttribute('aria-pressed', 'false');
        b.setAttribute('aria-pressed', 'false');
        opts.appendChild(a); opts.appendChild(b);
        return { box: box, btns: [a, b] };
      }

      var step1 = stepBlock(1, 'Does a reaction happen?');
      step1.btns[0].textContent = 'A reaction happens';
      step1.btns[1].textContent = 'Nothing happens';
      wrap.appendChild(step1.box);

      var step2 = stepBlock(2, 'Which metal ends up as ions in the solution?');
      var ionSpans = step2.btns.map(function (b) {
        var n = el('span', 'n');
        var f = el('span', 'f');
        b.appendChild(n);
        b.appendChild(document.createTextNode(' '));
        b.appendChild(f);
        var f0 = document.createTextNode('(');
        var fs = el('span');
        var sup = document.createElement('sup');
        var f1 = document.createTextNode(')');
        f.appendChild(f0); f.appendChild(fs); f.appendChild(sup); f.appendChild(f1);
        return { name: n, sym: fs, sup: sup };
      });
      wrap.appendChild(step2.box);

      var commit = el('div', 'commit');
      var go = el('button', 'go', 'Check');
      go.type = 'button';
      var runLine = el('span', 'run', '');
      commit.appendChild(go);
      commit.appendChild(runLine);
      wrap.appendChild(commit);

      var cap = el('p', 'cap');
      cap.setAttribute('aria-live', 'polite');
      wrap.appendChild(cap);

      var sr = el('p', 'sr');
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(sr);

      root.appendChild(wrap);

      /* ----------------------------------------------------------- state */
      var queue = [], qi = 0, first = true;
      var round = null, pickR = null, pickI = null;
      var committed = false, streak = 0, attempted = 0, mastered = false, lastOk = null;

      function shuffle(a) {
        for (var i = a.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1));
          var t = a[i]; a[i] = a[j]; a[j] = t;
        }
        return a;
      }
      function buildQueue() {
        var R = [], N = [], i;
        for (i = 0; i < ROUNDS.length; i++) {
          (ROUNDS[i].m < ROUNDS[i].s ? R : N).push(ROUNDS[i]);
        }
        shuffle(R); shuffle(N);
        if (first) {
          /* open on the canonical demonstration: zinc in copper(II) sulfate */
          for (i = 0; i < R.length; i++) {
            if (R[i].m === 5 && R[i].s === 7) { var t = R[0]; R[0] = R[i]; R[i] = t; break; }
          }
          first = false;
        }
        var q = [], ri = 0, ni = 0;
        for (i = 0; i < PATTERN.length; i++) {
          q.push(PATTERN[i] ? R[ri++] : N[ni++]);
        }
        queue = q; qi = 0;
      }

      function state(extra) {
        var o = {
          metal: METALS[round.m].name,
          solution: round.salt,
          reacts: round.m < round.s,
          picked: pickR === null ? null : (pickR ? 'reaction' : 'no-reaction'),
          pickedIon: pickI === null ? null : METALS[pickI].name,
          committed: committed,
          correct: lastOk,
          streak: streak,
          mastered: mastered,
          attempted: attempted
        };
        for (var k in extra) if (extra.hasOwnProperty(k)) o[k] = extra[k];
        root.dataset.svState = JSON.stringify(o);
      }

      function press(btns, idx) {
        for (var i = 0; i < btns.length; i++) {
          btns[i].setAttribute('aria-pressed', i === idx ? 'true' : 'false');
        }
      }
      function setStep2Live(on) {
        step2.box.className = 'step' + (on ? '' : ' off');
        step2.btns[0].disabled = !on;
        step2.btns[1].disabled = !on;
      }
      function refreshGo() {
        go.disabled = !committed && (pickR === null || pickI === null);
      }

      function hideTransfer() {
        arrow.setAttribute('opacity', '0');
        cross1.setAttribute('opacity', '0');
        cross2.setAttribute('opacity', '0');
        setRun(arLab, ['', '', '', '', '']);
      }

      function newRound() {
        if (qi >= queue.length) buildQueue();
        round = queue[qi++];
        pickR = null; pickI = null; committed = false; lastOk = null;

        var M = METALS[round.m], S = METALS[round.s];
        fMetal.textContent = M.name;
        fCol.textContent = round.col;
        fSalt.textContent = round.salt;

        press(step1.btns, -1);
        press(step2.btns, -1);
        /* option order follows the scenario: the strip, then the solution */
        [round.m, round.s].forEach(function (idx, k) {
          ionSpans[k].name.textContent = cap1(METALS[idx].name);
          ionSpans[k].sym.textContent = METALS[idx].sym;
          ionSpans[k].sup.textContent = METALS[idx].ion;
        });
        setStep2Live(false);
        go.textContent = 'Check';
        refreshGo();

        svgTitle.textContent = 'Reactivity series from potassium to copper. ' +
          cap1(M.name) + ' and ' + S.name + ' are marked.';
        symNodes.forEach(function (n, i) {
          n.setAttribute('class', 'sym' + (i === round.m || i === round.s ? ' on' : ''));
        });
        dotM.setAttribute('cx', mx(round.m));
        dotS.setAttribute('cx', mx(round.s));
        hideTransfer();
        setRun(rowA, [M.name + ' strip', '', '', '', '']);
        placeRun(rowA, mx(round.m), keyA);
        setRun(rowB, [S.sym, S.ion, ' ions in solution', '', '']);
        placeRun(rowB, mx(round.s), keyB);

        cap.textContent = 'The solution already contains ' + S.name +
          ' ions; the strip is neutral ' + M.name + ' atoms.';
        sr.textContent = 'New question. ' + frame.textContent;
        state();
      }

      function drawTransfer(reacts) {
        var xa = mx(round.m), xb = mx(round.s);
        arrow.setAttribute('x1', xa);
        arrow.setAttribute('x2', xb);
        arrow.setAttribute('stroke', reacts ? accent : '#b3aca1');
        arrow.setAttribute('stroke-dasharray', reacts ? 'none' : '3 3');
        arrow.setAttribute('marker-end', 'url(#' + uid + (reacts ? '-a' : '-b') + ')');
        arrow.setAttribute('opacity', '1');
        var mid = Math.max(60, Math.min(260, (xa + xb) / 2));
        arLab.setAttribute('x', mid);
        arLab.setAttribute('text-anchor', 'middle');
        arLab.style.fill = reacts ? accent : '#8d8880';
        setRun(arLab, reacts ? ['electrons', '', '', '', ''] : ['no transfer', '', '', '', '']);
        if (!reacts) {
          cross1.setAttribute('x1', mid - 4); cross1.setAttribute('y1', Y_ARR - 4);
          cross1.setAttribute('x2', mid + 4); cross1.setAttribute('y2', Y_ARR + 4);
          cross2.setAttribute('x1', mid + 4); cross2.setAttribute('y1', Y_ARR - 4);
          cross2.setAttribute('x2', mid - 4); cross2.setAttribute('y2', Y_ARR + 4);
          cross1.setAttribute('opacity', '1');
          cross2.setAttribute('opacity', '1');
        }
      }

      function verdictText(reacts, ok) {
        var M = METALS[round.m], S = METALS[round.s];
        var nM = chargeN(M.ion), nS = chargeN(S.ion);
        var said = pickR ? 'a reaction happens' : 'nothing happens';
        var saidIon = METALS[pickI].name;

        if (ok && reacts) {
          return 'Right ' + DASH + ' a reaction, with ' + M.name + ' ending up as the ions. ' +
            cap1(M.name) + ' is higher in the series, so it gives up electrons more readily: ' +
            'each ' + M.name + ' atom loses ' + num(nM) + ', and each ' + S.name +
            ' ion takes ' + num(nS) + ' and becomes a ' + S.name + ' atom. So ' +
            round.obs + '.';
        }
        if (ok && !reacts) {
          return 'Right ' + DASH + ' nothing happens, and the ' + S.name +
            ' stays as the ions. ' + cap1(M.name) + ' is lower in the series than ' +
            S.name + ', so it holds its outer electrons more tightly and has none to ' +
            'hand over. ' + cap1(round.obs) + '.';
        }
        if (reacts && !pickR) {
          return 'Not quite ' + DASH + ' you said ' + said + ', with ' + saidIon +
            ' as the ions. A reaction does happen: ' + M.name + ' is higher in the series, ' +
            'so it lets go of electrons more readily than ' + S.name + ' does. The ' +
            S.name + ' ions take them and turn into metal, while the ' + M.name +
            ' goes into solution as ions.';
        }
        if (!reacts && pickR) {
          return 'Not quite ' + DASH + ' you said ' + said + ', with ' + saidIon +
            ' as the ions. ' + cap1(M.name) + ' sits below ' + S.name +
            ' in the series: it holds its outer electrons more tightly, so it has none ' +
            'to give the ' + S.name + ' ions. Electrons never travel up the series.';
        }
        if (reacts) {
          return 'Not quite ' + DASH + ' a reaction does happen, but you said ' + saidIon +
            ' ends up as the ions. It is the metal that loses electrons that becomes the ion: ' +
            M.name + ' loses ' + num(nM) + (nM === 1 ? ' electron' : ' electrons') +
            ' per atom and goes into solution, while the ' +
            S.name + ' ions gain electrons and become ' + S.name + ' metal.';
        }
        return 'Not quite ' + DASH + ' no reaction is right, but you said ' + saidIon +
          ' ends up as the ions. Nothing was transferred, so nothing changed: the ' +
          S.name + ' ions were already in solution and are still there.';
      }

      function num(n) {
        return n === 1 ? 'one' : (n === 2 ? 'two' : 'three');
      }

      function doCheck() {
        var reacts = round.m < round.s;
        var rightIon = reacts ? round.m : round.s;
        var ok = (pickR === reacts) && (pickI === rightIon);
        committed = true;
        attempted++;
        lastOk = ok;
        streak = ok ? streak + 1 : 0;
        var justMastered = ok && streak === 3 && !mastered;
        if (streak >= 3) mastered = true;

        var M = METALS[round.m], S = METALS[round.s];
        drawTransfer(reacts);
        if (reacts) {
          setRun(rowA, halfMetal(round.m));
          setRun(rowB, halfIon(round.s));
        } else {
          setRun(rowA, [M.name + ' strip unchanged', '', '', '', '']);
          setRun(rowB, [S.sym, S.ion, ' still in solution', '', '']);
        }
        placeRun(rowA, mx(round.m), keyA);
        placeRun(rowB, mx(round.s), keyB);

        cap.textContent = '';
        if (justMastered) {
          cap.appendChild(document.createTextNode(
            'Right ' + DASH + ' ' + (reacts
              ? 'a reaction, with ' + M.name + ' ending up as the ions. '
              : 'nothing happens, and the ' + S.name + ' stays as the ions. ')));
          var strong = el('strong', null,
            'Three in a row ' + DASH + ' you have it. A metal' + RSQ + 's place in the ' +
            'series is how readily it lets go of its outer electrons: the higher one ' +
            'loses them and becomes the ion, and the lower one' + RSQ + 's ions collect ' +
            'them and turn back into metal.');
          cap.appendChild(strong);
        } else {
          cap.textContent = verdictText(reacts, ok);
        }
        sr.textContent = cap.textContent;

        runLine.textContent = mastered
          ? 'Mastered ' + DASH + ' keep going if you want.'
          : (streak === 0
              ? 'Run back to zero ' + DASH + ' three in a row ends it.'
              : (streak === 1
                  ? '1 right in a row.'
                  : '2 right in a row ' + DASH + ' one more and you have it.'));

        go.textContent = mastered ? 'Another anyway' : 'Next round';
        go.disabled = false;
        state();
      }

      /* ---------------------------------------------------------- wiring */
      step1.btns[0].addEventListener('click', function () {
        if (committed) return;
        pickR = true; press(step1.btns, 0); setStep2Live(true); refreshGo(); state();
      });
      step1.btns[1].addEventListener('click', function () {
        if (committed) return;
        pickR = false; press(step1.btns, 1); setStep2Live(true); refreshGo(); state();
      });
      step2.btns[0].addEventListener('click', function () {
        if (committed) return;
        pickI = round.m; press(step2.btns, 0); refreshGo(); state();
      });
      step2.btns[1].addEventListener('click', function () {
        if (committed) return;
        pickI = round.s; press(step2.btns, 1); refreshGo(); state();
      });
      go.addEventListener('click', function () {
        if (committed) {
          newRound();
          step1.btns[0].focus();
        } else if (pickR !== null && pickI !== null) {
          doCheck();
        }
      });

      buildQueue();
      newRound();
    }
  };
})();
