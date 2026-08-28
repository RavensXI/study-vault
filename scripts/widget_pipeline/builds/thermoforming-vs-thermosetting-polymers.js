/* thermoforming-vs-thermosetting-polymers — StudyVault lesson widget

   The two families are not the same plastic at different temperatures.
   One is separate tangled chains held by weak forces; the other is one
   cross-linked network of chains chemically bonded to each other.

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

  var CHAR_C = 210;        /* a cured thermoset chars above about this      */
  var SIL_CHAR_C = 300;    /* silicone takes far more before it breaks down */
  var GENERIC_SOFTEN = 100;/* the softening point of the ghost thermoplastic */

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
  /* what a generic member of that family would do, for the claim ghost */
  function ghostResult(fam, tempC) {
    return heatResult(fam, tempC, GENERIC_SOFTEN, CHAR_C);
  }

  var STRUCT_OF = { set: 'links', form: 'chains' };
  var FAM = { set: 'thermosetting', form: 'thermoforming' };

  /* ----------------------------------------------------------------- deck */

  /* SPECIFY: a product and its service or process condition. Commit the
     family AND the structural reason.
     PREDICT: a formed part meets a stated temperature. Commit what the
     heat does AND the structural reason. */
  var DECK = [
    { dir: 'spec', p: 'uf', t: 120, tag: 'plug casing',
      frame: 'A 13 A plug casing surrounds live pins. A loose connection can run them to 120 °C.',
      needs: 'the casing must not soften around hot pins.',
      fails: 'A thermoplastic casing would soften at the pins.' },
    { dir: 'spec', p: 'mf', t: 180, tag: 'worktop laminate',
      frame: 'A kitchen worktop laminate takes pans straight off the hob, at about 180 °C.',
      needs: 'the surface must take a hot pan without softening.',
      fails: 'A thermoplastic worktop would soften there.' },
    { dir: 'spec', p: 'er', t: 180, tag: 'panel matrix',
      frame: 'A carbon-fibre aircraft panel needs a resin matrix, cured once at 180 °C.',
      needs: 'the matrix must set once and hold the fibres for good.',
      fails: 'A thermoplastic matrix would soften when warm.' },
    { dir: 'spec', p: 'sil', t: 200, tag: 'cake mould',
      frame: 'A cake mould goes into a 200 °C oven every week and must come out the same shape.',
      needs: 'the mould must meet that oven again and again.',
      fails: 'A thermoplastic mould would sag in that oven.' },
    { dir: 'spec', p: 'hips', t: 150, tag: 'packaging tray',
      frame: 'A packaging tray is vacuum formed: the sheet is heated to 150 °C over a mould.',
      needs: 'the sheet must soften to drape over the mould.',
      fails: 'A thermoset cannot be softened at all.' },
    { dir: 'spec', p: 'hdpe', t: 180, tag: 'milk bottle',
      frame: 'Milk bottles are collected, shredded and melted at 180 °C into new bottles.',
      needs: 'the bottles must melt down and be moulded again.',
      fails: 'A thermoset cannot be melted down or recycled.' },
    { dir: 'spec', p: 'pp', t: 200, tag: 'flip-top cap',
      frame: 'A flip-top cap is injection moulded at 200 °C, and its hinge flexes thousands of times.',
      needs: 'injection moulding needs a material that flows.',
      fails: 'A thermoset is cured in the mould, not injected.' },
    { dir: 'spec', p: 'acr', t: 230, tag: 'light lens',
      frame: 'A vehicle rear light lens must be optically clear and injection moulded at 230 °C.',
      needs: 'the lens is injection moulded, so it must flow.',
      fails: 'A thermoset never melts, so it cannot be injected.' },

    { dir: 'pred', p: 'uf', t: 250, tag: 'urea formaldehyde',
      frame: 'A urea formaldehyde plug casing is left in a 250 °C oven for ten minutes.',
      truth: 'At 250 °C the surface blisters and chars.' },
    { dir: 'pred', p: 'mf', t: 250, tag: 'melamine formaldehyde',
      frame: 'An offcut of melamine formaldehyde worktop laminate is heated to 250 °C.',
      truth: 'At 250 °C it discolours and chars.' },
    { dir: 'pred', p: 'pr', t: 250, tag: 'polyester resin',
      frame: 'A cured polyester resin offcut from a fibreglass hull is heated to 250 °C.',
      truth: 'At 250 °C the cured resin scorches.' },
    { dir: 'pred', p: 'er', t: 250, tag: 'epoxy resin',
      frame: 'A block of cured epoxy resin is heated to 250 °C.',
      truth: 'At 250 °C the cured block chars.' },
    { dir: 'pred', p: 'hips', t: 150, tag: 'high-impact polystyrene',
      frame: 'A vacuum-formed HIPS tray goes back in the vacuum former at 150 °C.',
      truth: 'It goes rubbery and drapes over the mould.' },
    { dir: 'pred', p: 'acr', t: 160, tag: 'acrylic',
      frame: 'An acrylic strip is held over a line bender at 160 °C.',
      truth: 'It goes rubbery along the line and bends.' },
    { dir: 'pred', p: 'hdpe', t: 180, tag: 'high-density polythene',
      frame: 'Shredded HDPE milk bottles are heated to 180 °C in a moulding machine.',
      truth: 'It flows into the mould as a new bottle.' },
    { dir: 'pred', p: 'pp', t: 200, tag: 'polypropylene',
      frame: 'Polypropylene granules are heated to 200 °C in an injection moulder.',
      truth: 'It flows into the mould as a new part.' }
  ];

  function buildDeck() {
    var d = DECK.slice(), i, j, t;
    for (i = d.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1)); t = d[i]; d[i] = d[j]; d[j] = t;
    }
    return d;
  }

  /* -------------------------------------------------------------- options */

  var FAM_OPTS = [
    { v: 'form', label: 'Thermoforming' },
    { v: 'set', label: 'Thermosetting' }
  ];
  var OUT_OPTS = [
    { v: 'reform', label: 'Softens, then sets hard again' },
    { v: 'rigid', label: 'Stays solid — it only chars' },
    { v: 'melt', label: 'Melts, and cannot set again' }
  ];
  var WHY_OPTS = [
    { v: 'chains', label: 'Separate chains that can slide' },
    { v: 'links', label: 'Cross-linked into one network' },
    { v: 'same', label: 'Same chains, only a higher heat' }
  ];

  var ECHO = {
    chains: 'the chains slide',
    links: 'cross-links hold it',
    same: 'they differ only in heat'
  };
  var STRUCT_TXT = {
    set: 'A thermoset is one cross-linked network: no chain can slide.',
    form: 'A thermoplastic is separate chains, so heat lets them slide.'
  };
  /* what to say to a student who has just said the two differ only by degree */
  var MISC = {
    set: 'A thermoset has no melting point at all: it is one cross-linked network.',
    form: 'The difference is structure, not temperature: its chains are not bonded.'
  };
  var NEED_LINE = {
    set: 'This needs cross-links.',
    form: 'This needs sliding chains.'
  };
  var DRAWN = {
    chains: 'separate tangled chains',
    links: 'a cross-linked network',
    same: 'the same chains, only hotter'
  };
  var CLAIM = {
    reform: 'it softens and re-shapes',
    rigid: 'it never softens',
    melt: 'it melts for good',
    form: 'thermoforming',
    set: 'thermosetting'
  };

  /* ------------------------------------------------------------- geometry */

  var VBW = 300, VBH = 70;
  var BX = 60, BY = 14, BW = 180, BH = 40, BB = BY + BH;
  var SLUMP = { hold: 0, char: 0, reform: 1, melt: 2 };
  var SLIDE = [11, -8, 14, -12];
  var PHASE = [0.2, 1.9, 3.4, 5.1];

  function f(n) { return Math.round(n * 10) / 10; }

  function shape(s) {
    var drop = 9 * s, sag = 7 * s, spread = 12 * s;
    var top = BY + drop, l = BX - spread, r = BX + BW + spread;
    return {
      top: top, sag: sag, l: l, r: r,
      d: 'M ' + f(l) + ' ' + BB +
        ' L ' + f(l) + ' ' + f(top + 5) +
        ' Q ' + f(l) + ' ' + f(top) + ' ' + f(l + 7) + ' ' + f(top) +
        ' Q ' + f((l + r) / 2) + ' ' + f(top + sag * 2) + ' ' + f(r - 7) + ' ' + f(top) +
        ' Q ' + f(r) + ' ' + f(top) + ' ' + f(r) + ' ' + f(top + 5) +
        ' L ' + f(r) + ' ' + BB + ' Z'
    };
  }

  function chainY(sh, i) {
    var midTop = sh.top + sh.sag;
    return midTop + ((i + 0.8) / 4.6) * (BB - midTop);
  }

  function chainD(sh, i, s) {
    var y = chainY(sh, i), slide = SLIDE[i] * s;
    var x0 = sh.l - 10 + slide, x1 = sh.r + 10 + slide, n = 22;
    var d = '', k, x;
    for (k = 0; k <= n; k++) {
      x = x0 + (x1 - x0) * (k / n);
      d += (k ? ' L ' : 'M ') + f(x) + ' ' + f(y + 2.6 * Math.sin(k * 0.78 + PHASE[i]));
    }
    return d;
  }

  var LINK_X = [[0.24, 0.58, 0.84], [0.16, 0.5, 0.78], [0.3, 0.62, 0.9]];

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
      p + '.o.hid{display:none;}' +
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
        'aria-label': 'A block of the polymer, magnified, on a heater'
      });
      stage.appendChild(svg); wrap.appendChild(stage);

      var defs = el('defs', {});
      var clip = el('clipPath', { id: uid + '-c' });
      var clipPathEl = el('path', { d: shape(0).d });
      clip.appendChild(clipPathEl);
      defs.appendChild(clip);
      svg.appendChild(defs);

      var tagT = txt(150, 10, '', 8.6, '#8d8880');
      svg.appendChild(tagT);

      var block = el('path', { d: shape(0).d, fill: '#ece5da', stroke: '#b8ae9e', 'stroke-width': 1 });
      svg.appendChild(block);

      var inner = el('g', { 'clip-path': 'url(#' + uid + '-c)' });
      var chainsG = el('g', {});
      var linksG = el('g', {});
      inner.appendChild(chainsG); inner.appendChild(linksG);
      svg.appendChild(inner);

      var charG = el('g', { opacity: 0 });
      svg.appendChild(charG);
      var arrowsG = el('g', { opacity: 0 });
      svg.appendChild(arrowsG);

      var ghost = el('path', {
        d: '', fill: 'none', stroke: accent, 'stroke-width': 1.2,
        'stroke-dasharray': '4 3'
      });
      ghost.style.display = 'none';
      svg.appendChild(ghost);

      /* heater */
      svg.appendChild(el('rect', { x: 30, y: BB, width: 240, height: 3.6, rx: 1.8, fill: '#cfc4b2' }));
      [16, 27, 273, 284].forEach(function (x) {
        svg.appendChild(el('path', {
          d: 'M ' + x + ' ' + (BB - 2) + ' q 2.4 -1.5 0 -3 q -2.4 -1.5 0 -3 q 2.4 -1.5 0 -3',
          fill: 'none', stroke: '#c2b8a6', 'stroke-width': 1, 'stroke-linecap': 'round'
        }));
      });
      var tempT = txt(150, 66, '', 9.4, '#8d8880');
      tempT.setAttribute('font-weight', '600');
      svg.appendChild(tempT);

      /* ----------------------------------------------------------- controls */
      function group(labelText) {
        var lab = document.createElement('p'); lab.className = 'sl';
        var g = document.createElement('div'); g.className = 'grp';
        g.setAttribute('role', 'group');
        wrap.appendChild(lab); wrap.appendChild(g);
        return { lab: lab, g: g, btns: [] };
      }
      function fillGroup(gr, n) {
        var i, b;
        for (i = 0; i < n; i++) {
          b = document.createElement('button');
          b.type = 'button'; b.className = 'o';
          b.setAttribute('aria-pressed', 'false');
          gr.g.appendChild(b); gr.btns.push(b);
        }
      }
      var g1 = group(); fillGroup(g1, 3);
      var g2 = group(); fillGroup(g2, 3);

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
      var deck = buildDeck(), deckAt = 0;
      var round = null, spec = null, p1 = null, p2 = null, locked = false;
      var streak = 0, attempted = 0, mastered = false;
      var raf = 0;

      var view = { s: 0, struct: null, ghostOut: null, char: 0, hold: 0, arrows: 0, hot: false };

      function pushState(extra) {
        var s = { streak: streak, mastered: mastered, attempted: attempted };
        if (round) {
          s.direction = round.dir === 'spec' ? 'specify' : 'predict';
          s.polymer = spec.id;
          s.family = FAM[spec.fam];
          s.tempC = round.t;
          s.answerStep1 = round.dir === 'spec' ? spec.fam
            : (polyResult(spec, round.t) === 'reform' ? 'reform' : 'rigid');
          s.answerStep2 = STRUCT_OF[spec.fam];
          s.picked1 = p1; s.picked2 = p2;
        }
        if (extra) for (var k in extra) if (extra.hasOwnProperty(k)) s[k] = extra[k];
        root.dataset.svState = JSON.stringify(s);
      }

      /* ------------------------------------------------------------ drawing */

      function render() {
        var sh = shape(view.s), i, j, k, x, y1, y2, ln;
        block.setAttribute('d', sh.d);
        clipPathEl.setAttribute('d', sh.d);

        clear(chainsG); clear(linksG);
        if (view.struct) {
          for (i = 0; i < 4; i++) {
            chainsG.appendChild(el('path', {
              d: chainD(sh, i, view.s), fill: 'none',
              stroke: '#7d766c', 'stroke-width': 1.5, 'stroke-linecap': 'round'
            }));
          }
          if (view.struct === 'links') {
            for (i = 0; i < 3; i++) {
              y1 = chainY(sh, i); y2 = chainY(sh, i + 1);
              for (j = 0; j < 3; j++) {
                x = sh.l + LINK_X[i][j] * (sh.r - sh.l);
                ln = el('line', {
                  x1: f(x), y1: f(y1), x2: f(x), y2: f(y2),
                  stroke: view.hold > 0 ? accent : '#8d8880',
                  'stroke-width': f(1.5 + view.hold * 1.1), 'stroke-linecap': 'round'
                });
                linksG.appendChild(ln);
              }
            }
          }
        }

        /* the scorched surface: the network is still there underneath */
        charG.setAttribute('opacity', f(view.char));
        clear(charG);
        if (view.char > 0.01) {
          charG.appendChild(el('path', {
            d: sh.d, fill: 'none', stroke: '#3f382f', 'stroke-width': 3.4,
            'stroke-linejoin': 'round'
          }));
          [0.26, 0.55, 0.8].forEach(function (fr) {
            charG.appendChild(el('ellipse', {
              cx: f(sh.l + fr * (sh.r - sh.l)), cy: BB - 3.5,
              rx: 10, ry: 2.8, fill: '#3a332c'
            }));
          });
        }

        /* slide arrows: what the chains just did */
        arrowsG.setAttribute('opacity', f(view.arrows));
        clear(arrowsG);
        if (view.arrows > 0.01) {
          [0, 3].forEach(function (i) {
            var yy = chainY(sh, i), dir = SLIDE[i] > 0 ? 1 : -1;
            var cxx = (sh.l + sh.r) / 2 + dir * 22;
            arrowsG.appendChild(el('path', {
              d: 'M ' + f(cxx - dir * 9) + ' ' + f(yy) + ' L ' + f(cxx + dir * 9) + ' ' + f(yy) +
                ' M ' + f(cxx + dir * 4) + ' ' + f(yy - 3.2) + ' L ' + f(cxx + dir * 9) + ' ' + f(yy) +
                ' L ' + f(cxx + dir * 4) + ' ' + f(yy + 3.2),
              fill: 'none', stroke: accent, 'stroke-width': 1.5,
              'stroke-linecap': 'round', 'stroke-linejoin': 'round'
            }));
          });
        }

        if (view.ghostOut) {
          ghost.setAttribute('d', shape(SLUMP[view.ghostOut]).d);
          ghost.style.display = '';
        } else {
          ghost.style.display = 'none';
        }
        tempT.setAttribute('fill', view.hot ? accent : '#8d8880');
      }

      function stopAnim() { if (raf) { cancelAnimationFrame(raf); raf = 0; } }

      /* the reveal: chains slide the block into a slump, or the network
         holds and the surface chars. Runs once, then stops. */
      function animate(targetS, targetChar, targetHold, targetArrows) {
        stopAnim();
        if (reduced) {
          view.s = targetS; view.char = targetChar;
          view.hold = targetHold; view.arrows = targetArrows;
          render(); return;
        }
        var t0 = 0, DUR = 900;
        function step(now) {
          if (!t0) t0 = now;
          var t = Math.min(1, (now - t0) / DUR);
          var e = 1 - Math.pow(1 - t, 3);
          view.s = targetS * e;
          view.char = targetChar * Math.max(0, (e - 0.35) / 0.65);
          view.hold = targetHold * Math.min(1, e * 1.6);
          view.arrows = targetArrows * Math.max(0, (e - 0.45) / 0.55);
          render();
          if (t < 1) { raf = requestAnimationFrame(step); } else { raf = 0; }
        }
        raf = requestAnimationFrame(step);
      }

      /* ----------------------------------------------------------- feedback */

      function specMsg(ok, ansFam) {
        if (ok) {
          if (ansFam === 'set') {
            return 'thermosetting — ' + round.needs +
              ' Cross-links stop any chain sliding. That is ' + spec.name + '.';
          }
          return 'thermoforming — ' + round.needs +
            ' Separate chains slide when hot. That is ' + spec.name + '.';
        }
        if (p1 === ansFam) {
          if (p2 === 'same') {
            return 'you said ' + FAM[ansFam] + ' — right, but not because it melts hotter. ' +
              MISC[ansFam];
          }
          return 'you said ' + FAM[ansFam] + ' — right, but that is the other family’s structure. ' +
            STRUCT_TXT[ansFam];
        }
        return 'you chose ' + FAM[p1] + ', because ' + ECHO[p2] + '. ' +
          round.fails + ' ' + NEED_LINE[ansFam];
      }

      function predMsg(ok, ansOut) {
        var isSet = spec.fam === 'set';
        if (ok) {
          if (isSet) {
            return 'it never softens. ' + round.truth +
              ' Cross-links bond chain to chain, so a thermoset has no melting point.';
          }
          return 'it softens, then sets hard again on cooling. ' + round.truth +
            ' Its chains are separate — heat beats only weak forces.';
        }
        if (p1 === ansOut) {
          if (p2 === 'same') {
            return 'the outcome is right — but not because one just needs more heat. ' + MISC[spec.fam];
          }
          return 'the outcome is right — but that is the other family’s structure. ' + STRUCT_TXT[spec.fam];
        }
        if (isSet) {
          if (p1 === 'melt') {
            if (p2 === 'same') {
              return 'you said it melts once hot enough, and that these are the same chains. Cross-links are chemical bonds between them, so it chars first.';
            }
            return 'you said it melts once it is hot enough. Nothing melts: cross-links are chemical bonds, so it chars before it ever softens.';
          }
          return 'you said it softens and re-shapes. It cannot: the chains are bonded to each other. ' +
            round.truth;
        }
        if (p1 === 'melt') {
          return 'you said it melts and cannot set again. It does soften — but that is not the end of it: it sets hard again on cooling.';
        }
        return 'you said it never softens. It does: its chains are separate, not bonded, so they slide when hot. ' +
          round.truth;
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
        var bits = [];
        if (view.struct) bits.push('Drawn: ' + DRAWN[p2] + '.');
        if (p1) bits.push('Predicted: ' + CLAIM[p1] + '.');
        if (!bits.length) {
          return round.dir === 'spec'
            ? 'The block is the material for that job, magnified. The heater under it is at ' + round.t + ' °C.'
            : 'The block is the ' + round.tag + ', magnified. The heater under it is at ' + round.t + ' °C.';
        }
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
            b.classList.remove('hid');
            b.value = list[i].v;
            b.textContent = list[i].label;
            b.setAttribute('aria-label', list[i].label);
          } else {
            b.classList.add('hid');
            b.value = '';
          }
          b.disabled = false;
          b.setAttribute('aria-pressed', 'false');
          b.classList.remove('is-ans');
        });
      }

      function newRound() {
        stopAnim();
        if (deckAt >= deck.length) { deck = buildDeck(); deckAt = 0; }
        round = deck[deckAt++];
        spec = P[round.p];
        p1 = null; p2 = null; locked = false;

        frameP.textContent = round.frame;
        askP.textContent = round.dir === 'spec' ? 'Which family, and why?' : 'What does the heat do, and why?';
        tagT.textContent = round.dir === 'spec' ? 'inside the ' + round.tag : round.tag + ', magnified';
        tempT.textContent = round.t + ' °C';

        g1.lab.innerHTML = '';
        var b1 = document.createElement('b'); b1.textContent = '1 · ';
        g1.lab.appendChild(b1);
        g1.lab.appendChild(document.createTextNode(round.dir === 'spec' ? 'Family' : 'In the heat'));
        g2.lab.innerHTML = '';
        var b2 = document.createElement('b'); b2.textContent = '2 · ';
        g2.lab.appendChild(b2);
        g2.lab.appendChild(document.createTextNode('Because'));

        setOpts(g1, round.dir === 'spec' ? FAM_OPTS : OUT_OPTS);
        setOpts(g2, WHY_OPTS);

        view.s = 0; view.struct = null; view.ghostOut = null;
        view.char = 0; view.hold = 0; view.arrows = 0; view.hot = false;
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

        var ansFam = spec.fam;
        var trueOut = polyResult(spec, round.t);
        var ansOut = trueOut === 'reform' ? 'reform' : 'rigid';
        var ansStep1 = round.dir === 'spec' ? ansFam : ansOut;
        var ansWhy = STRUCT_OF[ansFam];
        var ok = (p1 === ansStep1) && (p2 === ansWhy);

        streak = ok ? streak + 1 : 0;
        var justMastered = ok && streak >= 3 && !mastered;
        if (streak >= 3) mastered = true;

        /* the truth is drawn from the model, never hand-set */
        view.struct = ansWhy;
        view.hot = false;
        /* the claim outline only earns its place when it differs from the truth */
        if (view.ghostOut && SLUMP[view.ghostOut] === SLUMP[trueOut]) view.ghostOut = null;
        view.s = 0; view.char = 0; view.hold = 0; view.arrows = 0;
        render();
        animate(SLUMP[trueOut], trueOut === 'char' ? 0.85 : 0,
          ansFam === 'set' ? 1 : 0, trueOut === 'reform' ? 1 : 0);

        var body = round.dir === 'spec' ? specMsg(ok, ansFam) : predMsg(ok, ansOut);
        if (justMastered) {
          body = 'three in a row — you have it. Separate chains slide, so a thermoplastic re-shapes over and over. Cross-links hold a thermoset, so it only chars.';
        }
        verdict(ok, body);

        g1.btns.forEach(function (b) {
          b.disabled = true;
          if (b.value === ansStep1) b.classList.add('is-ans');
        });
        g2.btns.forEach(function (b) {
          b.disabled = true;
          if (b.value === ansWhy) b.classList.add('is-ans');
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
        if (which === 1) {
          p1 = b.value;
          view.ghostOut = round.dir === 'spec' ? ghostResult(p1, round.t) : p1;
        } else {
          p2 = b.value;
          view.struct = p2 === 'links' ? 'links' : 'chains';
          view.hot = p2 === 'same';
          view.hold = 0;
        }
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
        p1 = null; p2 = null;
        g1.btns.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        g2.btns.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        view.struct = null; view.ghostOut = null; view.hot = false;
        render(); setRest();
        go.disabled = true;
        pushState();
      });

      newRound();
      pushState();
    }
  };
})();
