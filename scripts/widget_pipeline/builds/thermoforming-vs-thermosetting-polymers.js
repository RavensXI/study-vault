/* thermoforming-vs-thermosetting-polymers — StudyVault lesson widget

   The two families are not the same plastic at different temperatures.
   One is separate tangled chains held by weak forces; the other is one
   cross-linked network of chains chemically bonded to each other.

   BOTH structures are drawn, labelled, from the first frame — the student
   never has to picture them from memory. Every answer option points at
   something already on screen.

   ONE model decides both the picture and the mark:

     heatResult(family, tempC)
       thermoforming : tempC >= softenC ? 'reform' : 'hold'
       thermosetting : tempC >= charC   ? 'char'   : 'hold'

   No input can ever return 'melt'. That outcome exists only as an option
   the student can commit — it is the misconception this widget falsifies.

   Every round clears its threshold by at least 20 degC, and every
   comparison is between integers, so nothing sits on a boundary.        */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';
  var CLS = 'svw-thermo';
  var UID = 0;

  /* ---------------------------------------------------------------- model */

  var CHAR_C = 210;         /* a cured thermoset chars above about this      */
  var SIL_CHAR_C = 300;     /* silicone takes far more before it breaks down */
  var GENERIC_SOFTEN = 100; /* the softening point of the left-hand block    */

  var P = {
    uf:   { id: 'uf',   name: 'urea formaldehyde',       fam: 'set',  charC: CHAR_C },
    mf:   { id: 'mf',   name: 'melamine formaldehyde',   fam: 'set',  charC: CHAR_C },
    pr:   { id: 'pr',   name: 'polyester resin',         fam: 'set',  charC: CHAR_C },
    er:   { id: 'er',   name: 'epoxy resin',             fam: 'set',  charC: CHAR_C },
    sil:  { id: 'sil',  name: 'silicone',                fam: 'set',  charC: SIL_CHAR_C },
    hips: { id: 'hips', name: 'high-impact polystyrene', fam: 'form', softenC: 100 },
    hdpe: { id: 'hdpe', name: 'high-density polythene',  fam: 'form', softenC: 130 },
    pp:   { id: 'pp',   name: 'polypropylene',           fam: 'form', softenC: 165 },
    acr:  { id: 'acr',  name: 'acrylic',                 fam: 'form', softenC: 100 }
  };

  /* structure -> behaviour. The only place an outcome is decided. */
  function heatResult(fam, tempC, softenC, charC) {
    if (fam === 'form') return tempC >= softenC ? 'reform' : 'hold';
    return tempC >= charC ? 'char' : 'hold';
  }
  function polyResult(p, tempC) {
    return heatResult(p.fam, tempC, p.softenC, p.charC);
  }
  /* what each block on the stage does at this temperature */
  function blockResult(fam, tempC) {
    return heatResult(fam, tempC, GENERIC_SOFTEN, CHAR_C);
  }

  var FAM = { set: 'thermosetting', form: 'thermoforming' };
  var BLOCK = { set: 'cross-linked', form: 'separate-chain' };

  /* ----------------------------------------------------------------- deck */

  /* SPECIFY: a product and its condition. Commit which structure the job
     needs, and what the job needs it to do.
     PREDICT: a named polymer meets a stated temperature. Commit which
     structure it has, and what the heat does to it.

     Round 1 is FIXED and states the rule, so a student who has read the
     lesson once can play it. Every later round is shuffled and unaided. */
  var FIRST = {
    dir: 'spec', p: 'uf', t: 120,
    frame: 'Separate chains slide when hot; cross-linked chains cannot — they char. A 13 A plug casing surrounds live pins, and a loose connection runs them to 120 °C.',
    hold: 'hold its shape while the pins run hot',
    reform: 'melt down and be moulded again',
    fails: 'A thermoplastic casing would soften at the pins.'
  };

  var DECK = [
    { dir: 'spec', p: 'mf', t: 180,
      frame: 'A kitchen worktop laminate takes pans straight off the hob, at about 180 °C.',
      hold: 'take a hot pan without softening',
      reform: 'be melted down and re-formed',
      fails: 'A thermoplastic worktop would soften there.' },
    { dir: 'spec', p: 'er', t: 180,
      frame: 'A carbon-fibre aircraft panel needs a resin matrix, cured once at 180 °C.',
      hold: 'set once and hold the fibres for good',
      reform: 'be re-melted to reshape the panel',
      fails: 'A thermoplastic matrix would soften when warm.' },
    { dir: 'spec', p: 'sil', t: 200,
      frame: 'A cake mould goes into a 200 °C oven every week and must come out the same shape.',
      hold: 'meet that oven again and again',
      reform: 'be melted down between bakes',
      fails: 'A thermoplastic mould would sag in that oven.' },
    { dir: 'spec', p: 'hips', t: 150,
      frame: 'A packaging tray is vacuum formed: the sheet is heated to 150 °C over a mould.',
      hold: 'stay rigid while it is heated',
      reform: 'soften enough to drape over the mould',
      fails: 'A thermoset cannot be softened at all.' },
    { dir: 'spec', p: 'hdpe', t: 180,
      frame: 'Milk bottles are collected, shredded and melted at 180 °C into new bottles.',
      hold: 'stay solid at 180 °C',
      reform: 'melt down and be moulded again',
      fails: 'A thermoset cannot be melted down or recycled.' },
    { dir: 'spec', p: 'pp', t: 200,
      frame: 'A flip-top cap is injection moulded at 200 °C, and its hinge flexes thousands of times.',
      hold: 'stay rigid in the injection moulder',
      reform: 'flow into the mould when hot',
      fails: 'A thermoset is cured in the mould, not injected.' },
    { dir: 'spec', p: 'acr', t: 230,
      frame: 'A vehicle rear light lens must be optically clear and injection moulded at 230 °C.',
      hold: 'stay solid at 230 °C',
      reform: 'melt and flow into the mould',
      fails: 'A thermoset never melts, so it cannot be injected.' },

    { dir: 'pred', p: 'uf', t: 250,
      frame: 'A urea formaldehyde plug casing is left in a 250 °C oven for ten minutes.',
      truth: 'At 250 °C the surface blisters and chars.' },
    { dir: 'pred', p: 'mf', t: 250,
      frame: 'An offcut of melamine formaldehyde worktop laminate is heated to 250 °C.',
      truth: 'At 250 °C it discolours and chars.' },
    { dir: 'pred', p: 'pr', t: 250,
      frame: 'A cured polyester resin offcut from a fibreglass hull is heated to 250 °C.',
      truth: 'At 250 °C the cured resin scorches.' },
    { dir: 'pred', p: 'er', t: 250,
      frame: 'A block of cured epoxy resin is heated to 250 °C.',
      truth: 'At 250 °C the cured block chars.' },
    { dir: 'pred', p: 'hips', t: 150,
      frame: 'A vacuum-formed HIPS tray goes back in the vacuum former at 150 °C.',
      truth: 'It goes rubbery and drapes over the mould.' },
    { dir: 'pred', p: 'acr', t: 160,
      frame: 'An acrylic strip is held over a line bender at 160 °C.',
      truth: 'It goes rubbery along the line and bends.' },
    { dir: 'pred', p: 'hdpe', t: 180,
      frame: 'Shredded HDPE milk bottles are heated to 180 °C in a moulding machine.',
      truth: 'It flows into the mould as a new bottle.' },
    { dir: 'pred', p: 'pp', t: 200,
      frame: 'Polypropylene granules are heated to 200 °C in an injection moulder.',
      truth: 'It flows into the mould as a new part.' }
  ];

  function buildDeck(first) {
    var d = DECK.slice(), i, j, t;
    for (i = d.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1)); t = d[i]; d[i] = d[j]; d[j] = t;
    }
    if (first) d.unshift(FIRST);
    return d;
  }

  /* -------------------------------------------------------------- options */

  /* Group 1 names the two blocks on screen, in the same words as their
     labels. Group 2 is always a behaviour: 'reform', 'hold' or 'melt' —
     and 'melt' is the misconception, committable in every single round. */
  var STRUCT_OPTS = [
    { v: 'form', label: 'separate chains — thermoforming' },
    { v: 'set', label: 'cross-linked — thermosetting' }
  ];
  var PRED_OPTS = [
    { v: 'reform', label: 'softens, then sets hard again' },
    { v: 'hold', label: 'stays solid — it only chars' },
    { v: 'melt', label: 'melts, and cannot set again' }
  ];
  var SPEC_MELT = 'melt only at a higher temperature';

  var MISC = {
    set: 'A thermoset has no melting point at all: it is one cross-linked network.',
    form: 'The difference is structure, not temperature: its chains are not bonded.'
  };
  var NEED = {
    set: 'This job needs cross-links.',
    form: 'This job needs sliding chains.'
  };
  var CLAIMPHR = {
    reform: 'softens and re-shapes',
    hold: 'holds its shape',
    melt: 'melts for good'
  };

  /* ------------------------------------------------------------- geometry */

  var VBW = 300, VBH = 62;
  var BY = 14, BH = 32, BB = BY + BH;      /* blocks sit on the plate at 46 */
  var BW = 116, LX = 26, RX = 158;
  var SLUMP = { hold: 0, char: 0, reform: 1, melt: 2.2 };
  var SLIDE = [8, -7, 10];
  var PHASE = [0.3, 2.1, 3.9];
  var NCH = 3;

  function f(n) { return Math.round(n * 10) / 10; }

  function shape(x0, s) {
    var drop = 6 * s, sag = 4.5 * s, spread = 4.5 * s;
    var top = BY + drop, l = x0 - spread, r = x0 + BW + spread;
    return {
      top: top, sag: sag, l: l, r: r,
      d: 'M ' + f(l) + ' ' + BB +
        ' L ' + f(l) + ' ' + f(top + 4) +
        ' Q ' + f(l) + ' ' + f(top) + ' ' + f(l + 6) + ' ' + f(top) +
        ' Q ' + f((l + r) / 2) + ' ' + f(top + sag * 2) + ' ' + f(r - 6) + ' ' + f(top) +
        ' Q ' + f(r) + ' ' + f(top) + ' ' + f(r) + ' ' + f(top + 4) +
        ' L ' + f(r) + ' ' + BB + ' Z'
    };
  }

  function chainY(sh, i) {
    var midTop = sh.top + sh.sag;
    return midTop + ((i + 0.7) / (NCH + 0.4)) * (BB - midTop);
  }

  var IN_A = [5, 17, 8], IN_B = [15, 6, 18];

  function chainD(sh, i, s) {
    var y = chainY(sh, i), slide = SLIDE[i] * s;
    var x0 = sh.l + IN_A[i] + slide, x1 = sh.r - IN_B[i] + slide, n = 16, d = '', k, x;
    for (k = 0; k <= n; k++) {
      x = x0 + (x1 - x0) * (k / n);
      d += (k ? ' L ' : 'M ') + f(x) + ' ' + f(y + 2.2 * Math.sin(k * 0.95 + PHASE[i]));
    }
    return d;
  }

  var LINK_X = [[0.24, 0.56, 0.84], [0.16, 0.46, 0.76]];

  function el(name, attrs) {
    var e = document.createElementNS(NS, name), k;
    for (k in attrs) if (attrs.hasOwnProperty(k)) e.setAttribute(k, attrs[k]);
    return e;
  }
  function txt(x, y, s, size, fill, anchor) {
    var e = el('text', { x: x, y: y, 'font-size': size, fill: fill, 'text-anchor': anchor || 'middle' });
    e.textContent = s;
    return e;
  }
  function clear(g) { while (g.firstChild) g.removeChild(g.firstChild); }

  /* ------------------------------------------------------------------ css */

  function css(accent, reduced) {
    var p = '.' + CLS + ' ';
    return '.' + CLS + '{background:#fff;border:1px solid #e8e3db;border-radius:16px;' +
      'padding:.95rem;font-family:Inter,system-ui,-apple-system,sans-serif;color:#2d2a26;' +
      'box-sizing:border-box;max-width:100%;}' +
      p + '*{box-sizing:border-box;}' +
      p + '.k{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;' +
      'text-transform:uppercase;color:' + accent + ';}' +
      p + '.t{margin:.16rem 0 .32rem;font-family:"Source Serif 4",Georgia,serif;' +
      'font-weight:600;font-size:1.18rem;line-height:1.16;}' +
      p + '.frame{margin:0 0 .22rem;font-size:.84rem;line-height:1.42;color:#5b564e;}' +
      p + '.ask{margin:0 0 .3rem;font-size:.88rem;line-height:1.3;font-weight:600;}' +
      p + '.stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;' +
      'max-width:340px;margin:0 auto .3rem;overflow:hidden;}' +
      p + '.stage svg{display:block;width:100%;height:auto;}' +
      p + '.sl{margin:0 0 .14rem;font-size:.68rem;font-weight:700;letter-spacing:.07em;' +
      'text-transform:uppercase;color:#8d8880;}' +
      p + '.sl b{color:' + accent + ';}' +
      p + '.grp{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));' +
      'gap:.3rem;margin:0 0 .34rem;}' +
      p + '.o{font:600 .82rem/1.28 Inter,system-ui,sans-serif;color:#2d2a26;background:#faf8f5;' +
      'border:1px solid #ddd7cd;border-radius:10px;padding:.28rem .55rem;min-height:28px;' +
      'cursor:pointer;text-align:left;' +
      (reduced ? '' : 'transition:background .12s,border-color .12s;') + '}' +
      p + '.o[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}' +
      p + '.o.is-ans{border-color:' + accent + ';box-shadow:inset 0 0 0 1px ' + accent + ';}' +
      p + '.o[disabled]{cursor:default;opacity:.94;}' +
      p + '.act{display:flex;align-items:center;gap:.55rem;flex-wrap:wrap;margin:0 0 .32rem;}' +
      p + '.go{font:600 .82rem Inter,system-ui,sans-serif;background:#2d2a26;color:#fff;' +
      'border:1px solid #2d2a26;border-radius:10px;padding:.42rem .95rem;cursor:pointer;}' +
      p + '.go[disabled]{background:#faf8f5;color:#a8a29a;border-color:#e0d9cd;cursor:default;}' +
      p + '.run{font-size:.78rem;color:#8d8880;font-variant-numeric:tabular-nums;}' +
      p + '.cap{margin:0;font-size:.82rem;line-height:1.42;color:#2d2a26;min-height:42px;}' +
      p + '.cap .v{font-weight:700;}' +
      p + '.cap .rt{color:#4f7d63;}' +
      p + '.cap.rest{color:#8d8880;}' +
      p + '.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);' +
      'white-space:nowrap;margin:-1px;padding:0;border:0;}';
  }

  /* ---------------------------------------------------------------- mount */

  window.SVWidget = {
    meta: {
      id: 'thermoforming-vs-thermosetting-polymers',
      title: 'Chains that slide, or a net that holds',
      teaches: 'A thermoforming polymer is separate tangled chains that slide when heated, so it softens and re-shapes again and again. A thermosetting polymer is one cross-linked network, so it never softens: heat only chars it.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent || (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
      var reduced = !!ctx.reducedMotion;
      var uid = 'thm' + (++UID) + '-' + Math.floor(Math.random() * 100000);

      var wrap = document.createElement('div');
      wrap.className = CLS;
      var style = document.createElement('style');
      style.textContent = css(accent, reduced);
      wrap.appendChild(style);

      var kick = document.createElement('p'); kick.className = 'k';
      kick.textContent = 'Polymer structure';
      var ttl = document.createElement('h3'); ttl.className = 't';
      ttl.textContent = 'Chains that slide, or a net that holds';
      var frameP = document.createElement('p'); frameP.className = 'frame';
      var askP = document.createElement('p'); askP.className = 'ask';
      wrap.appendChild(kick); wrap.appendChild(ttl);
      wrap.appendChild(frameP); wrap.appendChild(askP);

      /* -------------------------------------------------------------- stage */
      var stage = document.createElement('div'); stage.className = 'stage';
      var svg = el('svg', {
        viewBox: '0 0 ' + VBW + ' ' + VBH, role: 'img',
        'aria-label': 'Two blocks of polymer on one hot plate: separate tangled chains on the left, chains tied by cross-links on the right'
      });
      stage.appendChild(svg); wrap.appendChild(stage);

      var defs = el('defs', {});
      var clipL = el('clipPath', { id: uid + '-L' });
      var clipLP = el('path', { d: shape(LX, 0).d });
      clipL.appendChild(clipLP);
      var clipR = el('clipPath', { id: uid + '-R' });
      var clipRP = el('path', { d: shape(RX, 0).d });
      clipR.appendChild(clipRP);
      defs.appendChild(clipL); defs.appendChild(clipR);
      svg.appendChild(defs);

      /* the hot plate, drawn first so the blocks sit on it */
      svg.appendChild(el('rect', { x: 14, y: BB, width: 272, height: 3.4, rx: 1.7, fill: '#cfc4b2' }));
      [10, 291].forEach(function (x) {
        svg.appendChild(el('path', {
          d: 'M ' + x + ' ' + (BB - 2) + ' q 2.2 -1.4 0 -2.8 q -2.2 -1.4 0 -2.8 q 2.2 -1.4 0 -2.8',
          fill: 'none', stroke: '#c2b8a6', 'stroke-width': 1, 'stroke-linecap': 'round'
        }));
      });

      function makeBlock(x0, clipId) {
        var g = {};
        g.body = el('path', { d: shape(x0, 0).d, fill: '#ece5da', stroke: '#b8ae9e', 'stroke-width': 1 });
        svg.appendChild(g.body);
        g.inner = el('g', { 'clip-path': 'url(#' + clipId + ')' });
        g.chains = el('g', {});
        g.links = el('g', {});
        g.inner.appendChild(g.chains); g.inner.appendChild(g.links);
        svg.appendChild(g.inner);
        g.char = el('g', { opacity: 0 }); svg.appendChild(g.char);
        g.arrows = el('g', { opacity: 0 }); svg.appendChild(g.arrows);
        g.ring = el('path', { d: '', fill: 'none', stroke: accent, 'stroke-width': 2 });
        g.ring.style.display = 'none';
        svg.appendChild(g.ring);
        g.ghost = el('path', {
          d: '', fill: 'none', stroke: '#6f6a61', 'stroke-width': 1.1, 'stroke-dasharray': '4 3'
        });
        g.ghost.style.display = 'none';
        svg.appendChild(g.ghost);
        g.x0 = x0;
        return g;
      }
      var L = makeBlock(LX, uid + '-L');
      var R = makeBlock(RX, uid + '-R');
      L.clip = clipLP; R.clip = clipRP;

      /* labels: the naming a cold reader cannot be expected to supply */
      var topL = txt(LX + BW / 2, 9, 'separate chains', 8.6, '#8d8880');
      var topR = txt(RX + BW / 2, 9, 'cross-linked', 8.6, '#8d8880');
      var botL = txt(LX + BW / 2, 58, 'thermoforming', 8.6, '#8d8880');
      var botR = txt(RX + BW / 2, 58, 'thermosetting', 8.6, '#8d8880');
      [topL, topR, botL, botR].forEach(function (t) { svg.appendChild(t); });
      var tempT = txt(150, 58, '', 9.2, '#8d8880');
      tempT.setAttribute('font-weight', '600');
      svg.appendChild(tempT);

      /* ----------------------------------------------------------- controls */
      function group() {
        var lab = document.createElement('p'); lab.className = 'sl';
        var g = document.createElement('div'); g.className = 'grp';
        g.setAttribute('role', 'group');
        wrap.appendChild(lab); wrap.appendChild(g);
        var btns = [], i, b;
        for (i = 0; i < 3; i++) {
          b = document.createElement('button');
          b.type = 'button'; b.className = 'o';
          b.setAttribute('aria-pressed', 'false');
          g.appendChild(b); btns.push(b);
        }
        return { lab: lab, g: g, btns: btns };
      }
      var g1 = group(), g2 = group();

      var act = document.createElement('div'); act.className = 'act';
      var go = document.createElement('button');
      go.type = 'button'; go.className = 'go'; go.textContent = 'Check';
      go.disabled = true;
      var run = document.createElement('span'); run.className = 'run';
      act.appendChild(go); act.appendChild(run); wrap.appendChild(act);

      var cap = document.createElement('p'); cap.className = 'cap rest';
      var sr = document.createElement('p'); sr.className = 'sr';
      sr.setAttribute('aria-live', 'polite');
      wrap.appendChild(cap); wrap.appendChild(sr);
      root.appendChild(wrap);

      /* -------------------------------------------------------------- state */
      var deck = buildDeck(true), deckAt = 0;
      var round = null, spec = null, p1 = null, p2 = null, locked = false;
      var streak = 0, attempted = 0, mastered = false;
      var raf = 0;

      var view = { sL: 0, sR: 0, charR: 0, holdR: 0, arrowsL: 0, hot: false, ans: null };

      function pushState(extra) {
        var s = { streak: streak, mastered: mastered, attempted: attempted };
        if (round) {
          var trueOut = polyResult(spec, round.t);
          s.direction = round.dir === 'spec' ? 'specify' : 'predict';
          s.polymer = spec.id;
          s.family = FAM[spec.fam];
          s.tempC = round.t;
          s.answerStep1 = spec.fam;
          s.answerStep2 = trueOut === 'reform' ? 'reform' : 'hold';
          s.picked1 = p1; s.picked2 = p2;
        }
        if (extra) for (var k in extra) if (extra.hasOwnProperty(k)) s[k] = extra[k];
        root.dataset.svState = JSON.stringify(s);
      }

      /* ------------------------------------------------------------ drawing */

      function drawBlock(g, s, links, charOp, holdOp, arrowOp, ringOn, ghostOut) {
        var sh = shape(g.x0, s), i, j, x, y1, y2;
        g.body.setAttribute('d', sh.d);
        g.clip.setAttribute('d', sh.d);

        clear(g.chains); clear(g.links);
        for (i = 0; i < NCH; i++) {
          g.chains.appendChild(el('path', {
            d: chainD(sh, i, s), fill: 'none',
            stroke: '#8d857a', 'stroke-width': 1.4, 'stroke-linecap': 'round'
          }));
        }
        if (links) {
          for (i = 0; i < NCH - 1; i++) {
            y1 = chainY(sh, i); y2 = chainY(sh, i + 1);
            for (j = 0; j < 3; j++) {
              x = sh.l + LINK_X[i][j] * (sh.r - sh.l);
              g.links.appendChild(el('line', {
                x1: f(x), y1: f(y1), x2: f(x), y2: f(y2),
                stroke: holdOp > 0 ? accent : '#4f4a43',
                'stroke-width': f(1.9 + holdOp * 1.1), 'stroke-linecap': 'round'
              }));
              g.links.appendChild(el('circle', {
                cx: f(x), cy: f(y1), r: 1.5, fill: holdOp > 0 ? accent : '#4f4a43'
              }));
              g.links.appendChild(el('circle', {
                cx: f(x), cy: f(y2), r: 1.5, fill: holdOp > 0 ? accent : '#4f4a43'
              }));
            }
          }
        }

        g.char.setAttribute('opacity', f(charOp));
        clear(g.char);
        if (charOp > 0.01) {
          g.char.appendChild(el('path', {
            d: sh.d, fill: 'none', stroke: '#3f382f', 'stroke-width': 3,
            'stroke-linejoin': 'round'
          }));
          [0.3, 0.62].forEach(function (fr) {
            g.char.appendChild(el('ellipse', {
              cx: f(sh.l + fr * (sh.r - sh.l)), cy: BB - 3,
              rx: 9, ry: 2.4, fill: '#3a332c'
            }));
          });
        }

        g.arrows.setAttribute('opacity', f(arrowOp));
        clear(g.arrows);
        if (arrowOp > 0.01) {
          [0, 1].forEach(function (i) {
            var yy = chainY(sh, i), dir = SLIDE[i] > 0 ? 1 : -1;
            var cxx = (sh.l + sh.r) / 2 + dir * 17;
            g.arrows.appendChild(el('path', {
              d: 'M ' + f(cxx - dir * 8) + ' ' + f(yy) + ' L ' + f(cxx + dir * 8) + ' ' + f(yy) +
                ' M ' + f(cxx + dir * 3.5) + ' ' + f(yy - 2.8) + ' L ' + f(cxx + dir * 8) + ' ' + f(yy) +
                ' L ' + f(cxx + dir * 3.5) + ' ' + f(yy + 2.8),
              fill: 'none', stroke: accent, 'stroke-width': 1.4,
              'stroke-linecap': 'round', 'stroke-linejoin': 'round'
            }));
          });
        }

        if (ringOn) { g.ring.setAttribute('d', sh.d); g.ring.style.display = ''; }
        else { g.ring.style.display = 'none'; }

        if (ghostOut) {
          g.ghost.setAttribute('d', shape(g.x0, SLUMP[ghostOut]).d);
          g.ghost.style.display = '';
        } else {
          g.ghost.style.display = 'none';
        }
      }

      function render() {
        /* which block is ringed: the student's pick, or the answer once marked */
        var ringed = view.ans || p1;
        /* the claimed behaviour is drawn on the block claimed; before a block
           is chosen it is drawn on both, because it is a claim about "it" */
        var ghostL = null, ghostR = null;
        if (!locked && p2) {
          if (!p1 || p1 === 'form') ghostL = p2;
          if (!p1 || p1 === 'set') ghostR = p2;
        }
        drawBlock(L, view.sL, false, 0, 0, view.arrowsL, ringed === 'form', ghostL);
        drawBlock(R, view.sR, true, view.charR, view.holdR, 0, ringed === 'set', ghostR);

        topL.setAttribute('fill', ringed === 'form' ? '#2d2a26' : '#8d8880');
        botL.setAttribute('fill', ringed === 'form' ? '#2d2a26' : '#8d8880');
        topR.setAttribute('fill', ringed === 'set' ? '#2d2a26' : '#8d8880');
        botR.setAttribute('fill', ringed === 'set' ? '#2d2a26' : '#8d8880');
        tempT.setAttribute('fill', view.hot ? accent : '#8d8880');
      }

      function stopAnim() { if (raf) { cancelAnimationFrame(raf); raf = 0; } }

      /* the reveal: the left block's chains slide and it slumps, while the
         right block's network holds and its surface chars. Runs once. */
      function animate(tL, tCharR, tHoldR, tArrowsL) {
        stopAnim();
        if (reduced) {
          view.sL = tL; view.charR = tCharR; view.holdR = tHoldR; view.arrowsL = tArrowsL;
          render(); return;
        }
        var t0 = 0, DUR = 900;
        function step(now) {
          if (!t0) t0 = now;
          var t = Math.min(1, (now - t0) / DUR), e = 1 - Math.pow(1 - t, 3);
          view.sL = tL * e;
          view.charR = tCharR * Math.max(0, (e - 0.35) / 0.65);
          view.holdR = tHoldR * Math.min(1, e * 1.6);
          view.arrowsL = tArrowsL * Math.max(0, (e - 0.45) / 0.55);
          render();
          if (t < 1) { raf = requestAnimationFrame(step); } else { raf = 0; }
        }
        raf = requestAnimationFrame(step);
      }

      /* ----------------------------------------------------------- feedback */

      function g2Label(v) {
        if (round.dir === 'pred') {
          for (var i = 0; i < PRED_OPTS.length; i++) if (PRED_OPTS[i].v === v) return PRED_OPTS[i].label;
        }
        return v === 'melt' ? SPEC_MELT : round[v];
      }

      function specMsg(ok, ansBehav) {
        if (ok) {
          if (spec.fam === 'set') {
            return 'the cross-linked block. It must ' + round.hold +
              ', and cross-links stop any chain sliding. That is ' + spec.name + '.';
          }
          return 'the separate-chain block. It must ' + round.reform +
            ', and separate chains slide when hot. That is ' + spec.name + '.';
        }
        if (p1 === spec.fam) {
          if (p2 === 'melt') {
            return 'you picked the right block, but said it only melts at a higher temperature. ' +
              MISC[spec.fam];
          }
          return 'you picked the right block, but said the job needs it to ' + g2Label(p2) +
            '. It needs to ' + round[ansBehav] + '.';
        }
        return 'you picked the ' + BLOCK[p1] + ' block. ' + round.fails + ' ' + NEED[spec.fam];
      }

      function predMsg(ok) {
        var isSet = spec.fam === 'set';
        if (ok) {
          if (isSet) {
            return 'it stays solid. ' + round.truth +
              ' Cross-links bond chain to chain, so a thermoset has no melting point.';
          }
          return 'it softens, then sets hard again. ' + round.truth +
            ' Separate chains only need weak forces beaten.';
        }
        if (p1 === spec.fam) {
          if (isSet) {
            if (p2 === 'melt') {
              return 'you picked the right block, but said it melts once hot enough. Nothing melts: cross-links are chemical bonds, so it chars first.';
            }
            return 'you picked the right block, but said it softens. It cannot: those chains are bonded to each other. ' +
              round.truth;
          }
          if (p2 === 'melt') {
            return 'you picked the right block, but said it cannot set again. It can: the chains slide, you re-shape it, and it hardens on cooling.';
          }
          return 'you picked the right block, but said it stays solid. Its chains are separate, so they slide when hot. ' +
            round.truth;
        }
        return 'you picked the ' + BLOCK[p1] + ' block, but ' + spec.name + ' is ' +
          BLOCK[spec.fam] + '. ' + round.truth;
      }

      function verdict(ok, body) {
        cap.className = 'cap';
        cap.innerHTML = '';
        var v = document.createElement('span');
        v.className = 'v' + (ok ? ' rt' : '');
        v.textContent = ok ? 'Right — ' : 'Not quite — ';
        cap.appendChild(v);
        cap.appendChild(document.createTextNode(body));
        sr.textContent = (ok ? 'Right. ' : 'Not quite. ') + body;
      }

      /* ------------------------------------------------------------- rounds */

      function restCaption() {
        if (!p1 && !p2) {
          return 'Two blocks on one hot plate at ' + round.t +
            ' °C: separate chains on the left, chains tied together by cross-links on the right.';
        }
        var bits = [];
        if (p1) bits.push('Claimed: the ' + BLOCK[p1] + ' block.');
        if (p2) bits.push('It ' + CLAIMPHR[p2] + '.');
        return bits.join(' ');
      }
      function setRest() {
        cap.className = 'cap rest';
        cap.textContent = restCaption();
        sr.textContent = cap.textContent;
      }

      function setOpts(gr, list) {
        gr.btns.forEach(function (b, i) {
          if (i < list.length) {
            b.style.display = '';
            b.value = list[i].v;
            b.textContent = list[i].label;
            b.setAttribute('aria-label', list[i].label);
          } else {
            b.style.display = 'none';
            b.value = '';
          }
          b.disabled = false;
          b.setAttribute('aria-pressed', 'false');
          b.classList.remove('is-ans');
        });
      }

      function newRound() {
        stopAnim();
        if (deckAt >= deck.length) { deck = buildDeck(false); deckAt = 0; }
        round = deck[deckAt++];
        spec = P[round.p];
        p1 = null; p2 = null; locked = false;

        frameP.textContent = round.frame;
        askP.textContent = round.dir === 'spec'
          ? 'Which structure does this job need?'
          : 'Which structure is it, and what does the heat do?';
        tempT.textContent = round.t + ' °C';

        g1.lab.innerHTML = '';
        var b1 = document.createElement('b'); b1.textContent = '1 · ';
        g1.lab.appendChild(b1);
        g1.lab.appendChild(document.createTextNode('This polymer is'));
        g2.lab.innerHTML = '';
        var b2 = document.createElement('b'); b2.textContent = '2 · ';
        g2.lab.appendChild(b2);
        g2.lab.appendChild(document.createTextNode(round.dir === 'spec' ? 'This job needs it to' : 'In the heat it'));

        setOpts(g1, STRUCT_OPTS);
        setOpts(g2, round.dir === 'pred' ? PRED_OPTS : [
          { v: 'reform', label: round.reform },
          { v: 'hold', label: round.hold },
          { v: 'melt', label: SPEC_MELT }
        ]);

        view.sL = 0; view.sR = 0; view.charR = 0; view.holdR = 0;
        view.arrowsL = 0; view.hot = false; view.ans = null;
        render();

        go.textContent = 'Check';
        go.disabled = true;
        setRest();
        pushState();
      }

      function commit() {
        if (locked || !p1 || !p2) return;
        locked = true;
        attempted++;

        var trueOut = polyResult(spec, round.t);
        var ansBehav = trueOut === 'reform' ? 'reform' : 'hold';
        var ok = (p1 === spec.fam) && (p2 === ansBehav);

        streak = ok ? streak + 1 : 0;
        var justMastered = ok && streak >= 3 && !mastered;
        if (streak >= 3) mastered = true;

        /* both blocks meet the same heat, straight from the model */
        var outL = blockResult('form', round.t);
        var outR = blockResult('set', round.t);
        view.ans = spec.fam;
        view.hot = false;
        view.sL = 0; view.sR = 0; view.charR = 0; view.holdR = 0; view.arrowsL = 0;
        render();
        animate(SLUMP[outL], outR === 'char' ? 0.85 : 0, 1, outL === 'reform' ? 1 : 0);

        var body = round.dir === 'spec' ? specMsg(ok, ansBehav) : predMsg(ok);
        if (justMastered) {
          body = 'three in a row — you have it. Separate chains slide, so a thermoplastic re-shapes over and over. Cross-links hold a thermoset, so it only chars.';
        }
        verdict(ok, body);

        g1.btns.forEach(function (b) {
          b.disabled = true;
          if (b.value === spec.fam) b.classList.add('is-ans');
        });
        g2.btns.forEach(function (b) {
          b.disabled = true;
          if (b.value === ansBehav) b.classList.add('is-ans');
        });

        run.textContent = mastered
          ? 'You have it'
          : (streak === 0
            ? (attempted > 1 ? 'Run reset' : '')
            : streak + ' in a row — ' + (3 - streak) + ' to go');
        go.textContent = mastered ? 'Another anyway' : 'Next';
        go.disabled = false;
        pushState({ right: ok });
      }

      /* ------------------------------------------------------------- wiring */

      function pick(gr, which, b) {
        if (locked || !b.value) return;
        gr.btns.forEach(function (o) {
          o.setAttribute('aria-pressed', o === b ? 'true' : 'false');
        });
        if (which === 1) { p1 = b.value; } else { p2 = b.value; view.hot = p2 === 'melt'; }
        render();
        setRest();
        go.disabled = !(p1 && p2);
        pushState();
      }

      g1.btns.forEach(function (b) { b.addEventListener('click', function () { pick(g1, 1, b); }); });
      g2.btns.forEach(function (b) { b.addEventListener('click', function () { pick(g2, 2, b); }); });

      go.addEventListener('click', function () {
        if (locked) { newRound(); g1.btns[0].focus(); } else { commit(); }
      });

      wrap.addEventListener('keydown', function (e) {
        if (e.key !== 'Escape' || locked) return;
        if (!p1 && !p2) return;
        p1 = null; p2 = null; view.hot = false;
        g1.btns.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        g2.btns.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        render(); setRest();
        go.disabled = true;
        pushState();
      });

      newRound();
      pushState();
    }
  };
})();
