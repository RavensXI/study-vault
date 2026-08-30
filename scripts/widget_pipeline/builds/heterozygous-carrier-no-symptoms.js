/* ================================================================
   heterozygous-carrier-no-symptoms

   One dominant (working) allele is enough. A heterozygous carrier of a
   recessive disorder has no symptoms at all - yet can still pass the
   faulty allele on, which is how two healthy parents have an affected
   child.

   Three rotating question shapes, every answer derived from the model:
     phenotype  genotype -> health + carrier status (misconception
                "mild symptoms" is committable)
     chance     two parents' genotypes -> chance for each child
     pedigree   a family tree -> a hidden genotype, found by enumerating
                every assignment consistent with the drawn phenotypes
   ================================================================ */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';

  /* ---------------------------------------------------------------
     1. The genetics. Nothing below this block hard-codes an answer.
     --------------------------------------------------------------- */

  var DISORDERS = [
    { id: 'cf',   name: 'cystic fibrosis', abbr: 'CF',
      rule: 'Cystic fibrosis (CF) is recessive: f is the faulty allele, F the working one.',
      mode: 'recessive', dom: 'F', rec: 'f' },
    { id: 'alb',  name: 'albinism', abbr: 'albinism',
      rule: 'Albinism is recessive: a is the faulty allele, A the working one.',
      mode: 'recessive', dom: 'A', rec: 'a' },
    { id: 'poly', name: 'polydactyly', abbr: 'polydactyly',
      rule: 'Polydactyly is dominant: D is the polydactyly allele, d the working one.',
      mode: 'dominant', dom: 'D', rec: 'd' }
  ];

  function GG(d) { return [d.dom + d.dom, d.dom + d.rec, d.rec + d.rec]; }
  function badAllele(d) { return d.mode === 'recessive' ? d.rec : d.dom; }

  function affected(g, d) {
    return d.mode === 'recessive'
      ? g === d.rec + d.rec
      : g.indexOf(d.dom) >= 0;
  }
  function carrier(g, d) {
    return d.mode === 'recessive' && !affected(g, d) && g.indexOf(d.rec) >= 0;
  }
  function norm(a, b, d) {
    if (a === d.dom && b === d.dom) return d.dom + d.dom;
    if (a === d.rec && b === d.rec) return d.rec + d.rec;
    return d.dom + d.rec;
  }
  /* the four gamete combinations, in Punnett order */
  function cross(g1, g2, d) {
    return [norm(g1[0], g2[0], d), norm(g1[0], g2[1], d),
            norm(g1[1], g2[0], d), norm(g1[1], g2[1], d)];
  }
  function countAffected(g1, g2, d) {
    var k = cross(g1, g2, d), n = 0;
    for (var i = 0; i < 4; i++) if (affected(k[i], d)) n++;
    return n;
  }
  function countCarriers(g1, g2, d) {
    var k = cross(g1, g2, d), n = 0;
    for (var i = 0; i < 4; i++) if (carrier(k[i], d)) n++;
    return n;
  }

  /* Every genotype assignment consistent with a drawn family: the
     phenotypes on the diagram, any genotype printed on it, and
     Mendelian transmission. The answer key falls out of this. */
  function consistentSets(fam, d) {
    var all = GG(d);
    var kids = fam.kids;
    var out = { mother: {}, father: {} };
    for (var q = 0; q < kids.length; q++) out['kid' + q] = {};
    function ok(mem, g) {
      if (affected(g, d) !== mem.affected) return false;
      if (mem.shown && g !== mem.shown) return false;
      return true;
    }
    for (var i = 0; i < all.length; i++) {
      if (!ok(fam.mother, all[i])) continue;
      for (var j = 0; j < all.length; j++) {
        if (!ok(fam.father, all[j])) continue;
        var pool = cross(all[i], all[j], d);
        var kidOptions = [];
        var viable = true;
        for (var k = 0; k < kids.length; k++) {
          var opts = [];
          for (var p = 0; p < pool.length; p++) {
            if (opts.indexOf(pool[p]) < 0 && ok(kids[k], pool[p])) opts.push(pool[p]);
          }
          if (!opts.length) { viable = false; break; }
          kidOptions.push(opts);
        }
        if (!viable) continue;
        out.mother[all[i]] = 1;
        out.father[all[j]] = 1;
        for (var k2 = 0; k2 < kids.length; k2++) {
          for (var o = 0; o < kidOptions[k2].length; o++) out['kid' + k2][kidOptions[k2][o]] = 1;
        }
      }
    }
    var sets = {};
    for (var key in out) {
      var list = [];
      for (var n = 0; n < all.length; n++) if (out[key][all[n]]) list.push(all[n]);
      sets[key] = list;
    }
    return sets;
  }

  /* ---------------------------------------------------------------
     2. People and rounds
     --------------------------------------------------------------- */

  var FEM = ['Maya', 'Priya', 'Aisha', 'Erin', 'Leah', 'Nadia', 'Grace', 'Zara'];
  var MAL = ['Daniel', 'Sam', 'Owen', 'Jonah', 'Marcus', 'Callum', 'Ethan', 'Rhys'];

  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function pickFew(a, n) {
    var c = a.slice(), out = [];
    while (out.length < n && c.length) out.push(c.splice(Math.floor(Math.random() * c.length), 1)[0]);
    return out;
  }
  function she(s) { return s === 'f' ? 'she' : 'he'; }
  function her(s) { return s === 'f' ? 'her' : 'his'; }
  function child(s) { return s === 'f' ? 'daughter' : 'son'; }

  var CHANCE_LABELS = ['No chance', '1 in 4', '1 in 2', '3 in 4', 'Every child'];

  /* ---- shape 1: genotype -> health ---- */
  function roundPhenotype() {
    var d = pick(DISORDERS);
    var gs = GG(d);
    var r = Math.random();
    var g = r < 0.55 ? gs[1] : (r < 0.8 ? gs[2] : gs[0]);
    var sex = Math.random() < 0.5 ? 'f' : 'm';
    var name = pick(sex === 'f' ? FEM : MAL);

    var opts = [
      { key: 'clear',    label: 'No symptoms — not a carrier' },
      { key: 'carrier',  label: 'No symptoms — a carrier' },
      { key: 'mild',     label: 'Mild symptoms' },
      { key: 'affected', label: 'Has ' + d.name }
    ];
    var answerKey = affected(g, d) ? 'affected' : (carrier(g, d) ? 'carrier' : 'clear');

    var truth;
    if (d.mode === 'dominant') {
      if (affected(g, d)) {
        truth = name + ' is ' + g + '. ' + d.dom + ' is dominant, so one copy is enough to show '
          + d.name + '. A dominant condition has no carriers: have the allele, show it.';
      } else {
        truth = name + ' is ' + g + ' — no ' + d.dom + ' allele at all, so no ' + d.name
          + ' and nothing faulty to pass on. Only recessive disorders have carriers.';
      }
    } else if (carrier(g, d)) {
      truth = name + ' is *' + g + '*: the working ' + d.dom + ' allele still makes working protein, so '
        + she(sex) + ' has *no symptoms at all* — but ' + she(sex) + ' carries ' + d.rec
        + ' and can pass it to a child.';
    } else if (affected(g, d)) {
      truth = name + ' is *' + g + '*: two faulty alleles and no working one, so no working protein is made and '
        + she(sex) + ' has ' + d.name + '. A carrier is ' + d.dom + d.rec + '.';
    } else {
      truth = name + ' is *' + g + '*: two working alleles. There is no faulty allele there at all — nothing to show, and nothing to pass on.';
    }

    var diag = {};
    diag.mild = 'Alleles do not blend or dilute each other. ';
    diag.clear = !affected(g, d) ? 'The health half is right. '
      : (d.mode === 'dominant' ? 'One copy of ' + d.dom + ' is enough to show it. '
                               : 'Two faulty alleles always show. ');
    diag.carrier = (d.mode === 'dominant')
      ? 'Carriers exist only for recessive disorders. '
      : (affected(g, d) ? 'A carrier keeps one working allele to hide the faulty one. ' : 'A carrier needs a faulty allele to carry. ');
    diag.affected = (d.mode === 'recessive')
      ? 'That takes two faulty alleles (' + d.rec + d.rec + '). '
      : 'Only ' + d.dom + ' causes it, and there is none here. ';

    return {
      shape: 'phenotype',
      d: d, optMin: '196px',
      key: g + '/' + d.id,
      rule: d.rule,
      ask: 'The two alleles ' + name + ' inherited for the ' + d.name
         + ' gene are shown. Predict ' + her(sex) + ' health.',
      opts: opts,
      answerKey: answerKey,
      head: function (k) {
        return k === answerKey
          ? 'Right — ' + (answerKey === 'clear' ? 'no symptoms, and not a carrier.'
              : answerKey === 'carrier' ? 'no symptoms, and a carrier.'
              : name + ' has ' + d.name + '.')
          : 'Not quite — you said ' + optLabel(opts, k).toLowerCase().replace(' — ', ', ') + '.';
      },
      body: function (k) { return (k === answerKey ? '' : diag[k] || '') + truth; },
      draw: function (svg, revealed) { drawGene(svg, name, g, d, revealed, sex); }
    };
  }

  /* ---- shape 2: two parents -> chance for each child ---- */
  function roundChance() {
    var d = pick(DISORDERS.slice(0, 2));   /* carriers, so recessive only */
    var D = d.dom, R = d.rec;
    var pairs = [[D + R, D + R], [D + R, D + D], [R + R, D + D], [D + R, R + R]];
    var pr = pick(pairs);
    if (Math.random() < 0.5) pr = [pr[1], pr[0]];
    var names = pickFew(FEM, 1).concat(pickFew(MAL, 1));
    var mum = { name: names[0], sex: 'f', geno: pr[0] };
    var dad = { name: names[1], sex: 'm', geno: pr[1] };

    var nAff = countAffected(mum.geno, dad.geno, d);
    var nCar = countCarriers(mum.geno, dad.geno, d);
    var combos = cross(mum.geno, dad.geno, d);
    var answerKey = CHANCE_LABELS[nAff];
    var opts = CHANCE_LABELS.map(function (l) { return { key: l, label: l }; });

    var truth = mum.geno + ' and ' + dad.geno + ' combine to give *' + combos.join(', ')
      + '*. ' + (nAff ? nAff + ' of the 4 is ' + R + R + ', so the chance is *' + answerKey.toLowerCase()
                      + '* for each child, every time.'
                     : 'None is ' + R + R + ', so no child can have ' + d.abbr + '.')
      + (nCar ? ' ' + nCar + ' of the 4 ' + (nCar === 1 ? 'is a carrier' : 'are carriers')
                + ' with no symptoms.' : '');

    function diag(k) {
      var pickedN = CHANCE_LABELS.indexOf(k);
      if (pickedN === 3) return 'That counts every child carrying an ' + R + ' — carrying is not having. ';
      if (pickedN === 0) return 'A carrier has no symptoms but can still pass ' + R + ' on. ';
      if (pickedN === 2) return 'That is the chance of getting ' + R + ' from one parent; the disorder needs one from each. ';
      if (pickedN === 4) return 'Each parent passes on only one of their two alleles. ';
      if (nAff === 0) return 'Both parents must be able to pass ' + R + '; one of them cannot. ';
      return '';
    }

    return {
      shape: 'chance',
      d: d, optMin: '104px',
      key: mum.geno + 'x' + dad.geno + '/' + d.id,
      rule: d.rule,
      ask: mum.name + ' and ' + dad.name + ' have the genotypes shown. Predict the chance that each child has '
         + d.abbr + '.',
      opts: opts,
      answerKey: answerKey,
      head: function (k) {
        return k === answerKey ? 'Right — ' + answerKey.toLowerCase() + '.'
                               : 'Not quite — you said ' + k.toLowerCase() + '.';
      },
      body: function (k) { return (k === answerKey ? '' : diag(k)) + truth; },
      draw: function (svg, revealed) { drawCross(svg, mum, dad, d, revealed); }
    };
  }

  /* ---- shape 3: family tree -> a hidden genotype ---- */
  function roundPedigree() {
    var d = pick(DISORDERS.slice(0, 2));
    var D = d.dom, R = d.rec;
    var fn = pickFew(FEM, 2), mn = pickFew(MAL, 2);
    var scen = pick(['S1', 'S1', 'S1', 'S2', 'S2', 'S3', 'S4', 'S4', 'S5', 'S5', 'S6', 'S6']);
    var fam, targetKey, ask, truth;

    if (scen === 'S1' || scen === 'S2' || scen === 'S3') {
      var kidSex = Math.random() < 0.5 ? ['m', 'f'] : ['f', 'm'];
      var k1 = { name: kidSex[0] === 'f' ? fn[1] : mn[1], sex: kidSex[0], affected: true, shown: null };
      var k2 = { name: kidSex[1] === 'f' ? fn[1] : mn[1], sex: kidSex[1], affected: false, shown: null };
      fam = {
        mother: { name: fn[0], sex: 'f', affected: false, shown: null },
        father: { name: mn[0], sex: 'm', affected: false, shown: null },
        kids: [k1, k2]
      };
      if (scen === 'S1') {
        targetKey = Math.random() < 0.5 ? 'mother' : 'father';
        var t = fam[targetKey];
        ask = 'Neither ' + fam.mother.name + ' nor ' + fam.father.name + ' has ' + d.abbr
            + ', but their ' + child(k1.sex) + ' ' + k1.name + ' does. Predict ' + t.name + '’s genotype.';
        truth = k1.name + ' is ' + R + R + ', so ' + she(k1.sex) + ' got one ' + R + ' from each parent. '
              + t.name + ' has no symptoms, so ' + she(t.sex) + ' is not ' + R + R + ' — ' + she(t.sex)
              + ' must be *' + D + R + '*, a carrier.';
      } else if (scen === 'S2') {
        targetKey = 'kid1';
        ask = 'Neither parent has ' + d.abbr + '. Their ' + child(k1.sex) + ' ' + k1.name + ' has it; their '
            + child(k2.sex) + ' ' + k2.name + ' does not. Predict ' + k2.name + '’s genotype.';
        truth = 'Both parents must be ' + D + R + ', giving ' + D + D + ', ' + D + R + ', ' + D + R + ', ' + R + R
              + '. ' + k2.name + ' has no symptoms, so not ' + R + R + ' — *'
              + D + D + ' or ' + D + R + '*, and the two look identical.';
      } else {
        targetKey = 'kid0';
        ask = 'Neither parent has ' + d.abbr + ', but their ' + child(k1.sex) + ' ' + k1.name
            + ' does. Predict ' + k1.name + '’s genotype.';
        truth = d.name.charAt(0).toUpperCase() + d.name.slice(1) + ' is recessive, so it only shows with two faulty alleles: '
              + k1.name + ' must be *' + R + R + '*, one ' + R + ' from each parent.';
      }
    } else {
      var affMum = Math.random() < 0.5;
      var kSex = Math.random() < 0.5 ? 'f' : 'm';
      var kName = kSex === 'f' ? fn[1] : mn[1];
      var clearGeno = scen === 'S5' ? D + D : (scen === 'S4' ? D + D : D + R);
      var otherGeno = scen === 'S5' ? D + R : R + R;
      var mumGeno = affMum ? otherGeno : clearGeno;
      var dadGeno = affMum ? clearGeno : otherGeno;
      fam = {
        mother: { name: fn[0], sex: 'f', affected: affected(mumGeno, d), shown: mumGeno },
        father: { name: mn[0], sex: 'm', affected: affected(dadGeno, d), shown: dadGeno },
        kids: [{ name: kName, sex: kSex, affected: false, shown: null }]
      };
      targetKey = 'kid0';
      var aff = affMum ? fam.mother : fam.father;
      var cle = affMum ? fam.father : fam.mother;
      if (scen === 'S5') {
        ask = 'Neither parent has ' + d.abbr + ' and their genotypes are shown. Predict the genotype of their '
            + child(kSex) + ' ' + kName + ', who has no symptoms.';
        truth = fam.mother.shown + ' and ' + fam.father.shown + ' give ' + cross(fam.mother.shown, fam.father.shown, d).join(', ')
              + '. No child can be ' + R + R + ', so ' + kName + ' is *' + D + D + ' or ' + D + R
              + '* — you cannot tell by looking.';
      } else if (scen === 'S4') {
        ask = aff.name + ' has ' + d.abbr + '; ' + cle.name + '’s genotype is shown. Predict the genotype of their '
            + child(kSex) + ' ' + kName + ', who has no symptoms.';
        truth = aff.name + ' is ' + R + R + ', so every gamete carries ' + R + '. ' + cle.name + ' is ' + D + D
              + ', so every gamete carries ' + D + '. Every child is *' + D + R + '* — a carrier, no symptoms.';
      } else {
        ask = cle.name + '’s genotype is shown; ' + aff.name + ' has ' + d.abbr + '. Predict the genotype of their '
            + child(kSex) + ' ' + kName + ', who has no symptoms.';
        truth = D + R + ' and ' + R + R + ' give ' + cross(D + R, R + R, d).join(', ') + '. ' + kName
              + ' has no symptoms, so ' + she(kSex) + ' is not ' + R + R + ' — ' + she(kSex) + ' must be *' + D + R + '*.';
      }
    }

    var sets = consistentSets(fam, d);
    var answer = sets[targetKey];
    var answerKey = answer.length === 1 ? answer[0]
                  : (answer.length === 2 && answer[0] === D + D && answer[1] === D + R) ? D + D + ' or ' + D + R
                  : null;
    if (!answerKey) return null;               /* never ship an unmappable round */

    var opts = [
      { key: D + D, label: D + D + ' — two working' },
      { key: D + R, label: D + R + ' — one of each' },
      { key: R + R, label: R + R + ' — two faulty' },
      { key: D + D + ' or ' + D + R, label: D + D + ' or ' + D + R + ' — cannot tell' }
    ];
    var target = targetKey === 'mother' ? fam.mother
               : targetKey === 'father' ? fam.father
               : fam.kids[+targetKey.slice(3)];

    function diag(k) {
      if (k === R + R) return target.name + ' has no symptoms, so ' + she(target.sex) + ' cannot be ' + R + R + '. ';
      if (k === D + D && answerKey === D + R) return D + D + ' has no ' + R + ' to inherit or to pass on. ';
      if (answerKey.length > 2 && k.length === 2) {
        var other = answerKey.split(' or ').filter(function (x) { return x !== k; })[0];
        return k + ' is possible — but so is ' + other + '. ';
      }
      if (k.length > 2) return 'This family does fix it. ';
      return '';
    }

    return {
      shape: 'pedigree',
      d: d, optMin: '184px',
      key: scen + '/' + d.id + '/' + targetKey,
      rule: d.rule,
      ask: ask,
      opts: opts,
      answerKey: answerKey,
      head: function (k) {
        return k === answerKey ? 'Right — ' + answerKey + '.'
                               : 'Not quite — you said ' + k + '.';
      },
      body: function (k) { return (k === answerKey ? '' : diag(k)) + truth; },
      draw: function (svg, revealed) { drawFamily(svg, fam, d, sets, revealed); }
    };
  }

  function optLabel(opts, key) {
    for (var i = 0; i < opts.length; i++) if (opts[i].key === key) return opts[i].label;
    return key;
  }

  var ORDER = ['phenotype', 'chance', 'pedigree'];
  function nextRound(state) {
    var guard = 0;
    while (guard++ < 40) {
      var shape = ORDER[state.turn % 3];
      state.turn++;
      var r = shape === 'phenotype' ? roundPhenotype()
            : shape === 'chance' ? roundChance() : roundPedigree();
      if (r && r.key !== state.lastKey) { state.lastKey = r.key; return r; }
    }
    return roundPhenotype();
  }

  /* ---------------------------------------------------------------
     3. Drawing. One stage, fixed height, so nothing jumps on commit.
     --------------------------------------------------------------- */

  function el(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }
  function tx(x, y, s, cls, anchor) {
    var t = el('text', { x: x, y: y, 'text-anchor': anchor || 'middle', 'class': cls });
    t.textContent = s;
    return t;
  }
  function clear(svg) { while (svg.firstChild) svg.removeChild(svg.firstChild); }

  function tilePair(g, cx, top, geno, d) {
    var W = 17, H = 19, GAP = 3, x0 = cx - (2 * W + GAP) / 2;
    for (var i = 0; i < 2; i++) {
      var isBad = geno[i] === badAllele(d);
      g.appendChild(el('rect', { x: x0 + i * (W + GAP), y: top, width: W, height: H, rx: 4,
        'class': 'svw-hc-tile' + (isBad ? ' svw-hc-bad' : '') }));
      g.appendChild(tx(x0 + i * (W + GAP) + W / 2, top + 14, geno[i], 'svw-hc-al'));
    }
  }
  function unknownPair(g, cx, top) {
    g.appendChild(el('rect', { x: cx - 18.5, y: top, width: 37, height: 19, rx: 4, 'class': 'svw-hc-unk' }));
    g.appendChild(tx(cx, top + 14, '?', 'svw-hc-al'));
  }
  function person(g, cx, cy, sex, isAff, r) {
    var n = sex === 'f'
      ? el('circle', { cx: cx, cy: cy, r: r || 11 })
      : el('rect', { x: cx - (r || 11), y: cy - (r || 11), width: 2 * (r || 11), height: 2 * (r || 11), rx: 2 });
    n.setAttribute('class', 'svw-hc-p' + (isAff ? ' svw-hc-aff' : ''));
    g.appendChild(n);
  }

  /* shape 1 stage: the two chromosome copies carrying the gene */
  function drawGene(svg, name, geno, d, revealed, sex) {
    clear(svg);
    svg.setAttribute('viewBox', '0 0 270 124');
    var g = el('g', {});
    svg.appendChild(g);
    g.appendChild(tx(96, 56, 'the gene for', 'svw-hc-sm', 'end'));
    g.appendChild(tx(96, 70, d.name, 'svw-hc-sm', 'end'));
    var xs = [150, 232];
    var lab = ['from mother', 'from father'];
    for (var i = 0; i < 2; i++) {
      g.appendChild(tx(xs[i], 16, lab[i], 'svw-hc-nm'));
      g.appendChild(el('rect', { x: xs[i] - 9, y: 22, width: 18, height: 78, rx: 9, 'class': 'svw-hc-chr' }));
      var isBad = geno[i] === badAllele(d);
      g.appendChild(el('rect', { x: xs[i] - 13, y: 49, width: 26, height: 24, rx: 5,
        'class': 'svw-hc-tile' + (isBad ? ' svw-hc-bad' : '') }));
      g.appendChild(tx(xs[i], 67, geno[i], 'svw-hc-alb'));
    }
    if (revealed) {
      var tag = affected(geno, d) ? name + ' has ' + d.name
        : carrier(geno, d) ? name + ': no symptoms, a carrier'
        : name + ': no symptoms, not a carrier';
      g.appendChild(tx(135, 117, tag, 'svw-hc-tag'));
    }
  }

  /* shape 2 stage: parents, then the four combinations after commit */
  function drawCross(svg, mum, dad, d, revealed) {
    clear(svg);
    svg.setAttribute('viewBox', '0 0 320 124');
    var g = el('g', {});
    svg.appendChild(g);
    var P = [{ p: mum, cx: 100, side: 'end' }, { p: dad, cx: 220, side: 'start' }];
    for (var i = 0; i < 2; i++) {
      var m = P[i].p, cx = P[i].cx, tX = P[i].side === 'end' ? cx - 16 : cx + 16;
      var isAff = affected(m.geno, d);
      person(g, cx, 24, m.sex, isAff);
      g.appendChild(tx(tX, 20, m.name, 'svw-hc-nm', P[i].side));
      g.appendChild(tx(tX, 33, isAff ? 'has ' + d.abbr : 'no symptoms', 'svw-hc-sm', P[i].side));
      tilePair(g, cx, 40, m.geno, d);
    }
    g.appendChild(el('path', { d: 'M111 24 H209', 'class': 'svw-hc-line' }));
    if (!revealed) {
      g.appendChild(el('path', { d: 'M160 24 V78', 'class': 'svw-hc-line' }));
      g.appendChild(el('circle', { cx: 160, cy: 89, r: 10, 'class': 'svw-hc-ghost' }));
      g.appendChild(tx(160, 93, '?', 'svw-hc-al'));
      g.appendChild(tx(160, 118, 'each child', 'svw-hc-sm'));
    } else {
      var combos = cross(mum.geno, dad.geno, d);
      var nAff = countAffected(mum.geno, dad.geno, d);
      g.appendChild(el('path', { d: 'M160 24 V62', 'class': 'svw-hc-line' }));
      g.appendChild(tx(160, 76, 'each child — one of these four:', 'svw-hc-sm'));
      for (var c = 0; c < 4; c++) {
        var x = 52 + c * 72;
        if (affected(combos[c], d)) {
          g.appendChild(el('rect', { x: x - 23, y: 79, width: 46, height: 25, rx: 7, 'class': 'svw-hc-ring' }));
        }
        tilePair(g, x, 82, combos[c], d);
      }
      g.appendChild(tx(160, 118, nAff === 0
        ? 'no combination is ' + d.rec + d.rec + ' — no child can have ' + d.abbr
        : 'the ringed combination' + (nAff > 1 ? 's have ' : ' has ') + d.abbr,
        nAff === 0 ? 'svw-hc-sm' : 'svw-hc-tag'));
    }
  }

  /* shape 3 stage: the family tree */
  function drawFamily(svg, fam, d, sets, revealed) {
    clear(svg);
    svg.setAttribute('viewBox', '0 0 320 124');
    var g = el('g', {});
    svg.appendChild(g);
    var rows = [
      { m: fam.mother, key: 'mother', cx: 100, side: 'end', cy: 24 },
      { m: fam.father, key: 'father', cx: 220, side: 'start', cy: 24 }
    ];
    var kidX = fam.kids.length === 1 ? [160] : [100, 220];
    for (var k = 0; k < fam.kids.length; k++) {
      rows.push({ m: fam.kids[k], key: 'kid' + k, cx: kidX[k], cy: 86,
        side: fam.kids.length === 1 ? 'start' : (k === 0 ? 'end' : 'start') });
    }
    g.appendChild(el('path', { d: 'M111 24 H209 M160 24 V66', 'class': 'svw-hc-line' }));
    if (fam.kids.length === 1) {
      g.appendChild(el('path', { d: 'M160 66 V75', 'class': 'svw-hc-line' }));
    } else {
      g.appendChild(el('path', { d: 'M100 66 H220 M100 66 V75 M220 66 V75', 'class': 'svw-hc-line' }));
    }
    for (var i = 0; i < rows.length; i++) {
      var r = rows[i], m = r.m, tX = r.side === 'end' ? r.cx - 16 : r.cx + 16;
      person(g, r.cx, r.cy, m.sex, m.affected);
      g.appendChild(tx(tX, r.cy - 4, m.name, 'svw-hc-nm', r.side));
      g.appendChild(tx(tX, r.cy + 9, m.affected ? 'has ' + d.abbr : 'no symptoms', 'svw-hc-sm', r.side));
      var top = r.cy + 16;
      if (m.shown) tilePair(g, r.cx, top, m.shown, d);
      else if (!revealed) unknownPair(g, r.cx, top);
      else {
        var s = sets[r.key];
        if (s.length === 1) tilePair(g, r.cx, top, s[0], d);
        else g.appendChild(tx(r.cx, top + 14, s.join(' or '), 'svw-hc-tag'));
      }
    }
  }

  /* ---------------------------------------------------------------
     4. Style
     --------------------------------------------------------------- */

  var CSS = [
'.svw-hc{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;display:flex;flex-direction:column;gap:.5rem}',
'.svw-hc *{box-sizing:border-box}',
'.svw-hc .svw-hc-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--hc-a)}',
'.svw-hc .svw-hc-h{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.2rem;line-height:1.15;margin:.1rem 0 0}',
'.svw-hc .svw-hc-rule{font-size:.76rem;line-height:1.4;color:#5b564e;margin:.3rem 0 0}',
'.svw-hc .svw-hc-ask{font-size:.88rem;line-height:1.4;font-weight:500;margin:.24rem 0 0}',
'.svw-hc .svw-hc-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.35rem}',
'.svw-hc .svw-hc-svg{display:block;width:100%;height:118px}',
'.svw-hc .svw-hc-opts{display:grid;gap:6px;grid-template-columns:repeat(auto-fit,minmax(var(--hc-min,190px),1fr))}',
'.svw-hc .svw-hc-opt{font-family:inherit;font-size:.82rem;font-weight:600;line-height:1.2;text-align:left;padding:.46rem .7rem;border:1px solid #ddd7cd;border-radius:10px;background:#faf8f5;color:#2d2a26;cursor:pointer}',
'.svw-hc .svw-hc-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
'.svw-hc .svw-hc-opt[disabled]{cursor:default}',
'.svw-hc .svw-hc-opt[disabled]:not([aria-pressed="true"]):not(.svw-hc-right){opacity:.48}',
'.svw-hc .svw-hc-right{border-color:#4f7d63;box-shadow:inset 0 0 0 1px #4f7d63}',
'.svw-hc .svw-hc-row{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap}',
'.svw-hc .svw-hc-go{font-family:inherit;font-size:.82rem;font-weight:600;padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}',
'.svw-hc .svw-hc-go[disabled]{background:#faf8f5;color:#a09a91;border-color:#e0d9cd;cursor:default}',
'.svw-hc .svw-hc-run{font-size:.78rem;color:#5b564e;flex:1 1 120px;min-width:0;font-variant-numeric:tabular-nums}',
'.svw-hc .svw-hc-cap{font-size:.86rem;line-height:1.5;margin:0;min-height:3.9em}',
'.svw-hc .svw-hc-cap b{font-weight:600}',
'.svw-hc .svw-hc-v{font-weight:600}',
'.svw-hc .svw-hc-v-ok{color:#4f7d63}',
'.svw-hc .svw-hc-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
'.svw-hc .svw-hc-p{fill:#fff;stroke:#2d2a26;stroke-width:1.6}',
'.svw-hc .svw-hc-aff{fill:#2d2a26}',
'.svw-hc .svw-hc-ghost{fill:none;stroke:#c6bfb2;stroke-width:1.4;stroke-dasharray:3 2.6}',
'.svw-hc .svw-hc-line{stroke:#bdb5a8;stroke-width:1.4;fill:none}',
'.svw-hc .svw-hc-chr{fill:#f2ece3;stroke:#ddd7cd;stroke-width:1.4}',
'.svw-hc .svw-hc-tile{fill:#fff;stroke:#ddd7cd;stroke-width:1.2}',
'.svw-hc .svw-hc-bad{fill:var(--hc-t);stroke:var(--hc-a)}',
'.svw-hc .svw-hc-ring{fill:none;stroke:var(--hc-a);stroke-width:1.5}',
'.svw-hc .svw-hc-unk{fill:#fff;stroke:#c6bfb2;stroke-width:1.2;stroke-dasharray:3 2.6}',
'.svw-hc .svw-hc-al{font-family:Inter,system-ui,sans-serif;font-size:12.5px;font-weight:700;fill:#2d2a26}',
'.svw-hc .svw-hc-alb{font-family:Inter,system-ui,sans-serif;font-size:15px;font-weight:700;fill:#2d2a26}',
'.svw-hc .svw-hc-nm{font-family:Inter,system-ui,sans-serif;font-size:11.5px;font-weight:600;fill:#2d2a26}',
'.svw-hc .svw-hc-sm{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:#8d8880}',
'.svw-hc .svw-hc-tag{font-family:Inter,system-ui,sans-serif;font-size:11.5px;font-weight:600;fill:#4f7d63}',
'.svw-hc-motion .svw-hc-opt{transition:background .12s ease,color .12s ease}'
  ].join('');

  /* ---------------------------------------------------------------
     5. Mount
     --------------------------------------------------------------- */

  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = ctx.accent
      || (getComputedStyle(root).getPropertyValue('--accent') || '').trim()
      || '#8a6a4f';

    root.className = 'svw-hc' + (ctx.reducedMotion ? '' : ' svw-hc-motion');
    root.style.setProperty('--hc-a', accent);
    root.style.setProperty('--hc-t', accent + '2e');

    var style = document.createElement('style');
    style.textContent = CSS;
    root.appendChild(style);

    var head = document.createElement('div');
    var kick = document.createElement('div');
    kick.className = 'svw-hc-kick';
    kick.textContent = 'Genotype and phenotype';
    var h = document.createElement('div');
    h.className = 'svw-hc-h';
    h.textContent = 'Carrier or affected?';
    var rule = document.createElement('p');
    rule.className = 'svw-hc-rule';
    var ask = document.createElement('p');
    ask.className = 'svw-hc-ask';
    head.appendChild(kick); head.appendChild(h); head.appendChild(rule); head.appendChild(ask);

    var stage = document.createElement('div');
    stage.className = 'svw-hc-stage';
    var svg = el('svg', { viewBox: '0 0 320 124', preserveAspectRatio: 'xMidYMid meet',
      'class': 'svw-hc-svg', role: 'img' });
    stage.appendChild(svg);

    var optsEl = document.createElement('div');
    optsEl.className = 'svw-hc-opts';

    var row = document.createElement('div');
    row.className = 'svw-hc-row';
    var go = document.createElement('button');
    go.type = 'button';
    go.className = 'svw-hc-go';
    go.textContent = 'Check';
    go.disabled = true;
    var run = document.createElement('div');
    run.className = 'svw-hc-run';
    row.appendChild(go); row.appendChild(run);

    var cap = document.createElement('p');
    cap.className = 'svw-hc-cap';
    var sr = document.createElement('p');
    sr.className = 'svw-hc-sr';
    sr.setAttribute('aria-live', 'polite');

    root.appendChild(head);
    root.appendChild(stage);
    root.appendChild(optsEl);
    root.appendChild(row);
    root.appendChild(cap);
    root.appendChild(sr);

    var S = { turn: Math.floor(Math.random() * 3), lastKey: null,
              streak: 0, attempted: 0, mastered: false };
    var round = null, picked = null, done = false;

    function writeCap(text, verdict, isRight) {
      while (cap.firstChild) cap.removeChild(cap.firstChild);
      if (verdict) {
        var v = document.createElement('span');
        v.className = 'svw-hc-v' + (isRight ? ' svw-hc-v-ok' : '');
        v.textContent = verdict + ' ';
        cap.appendChild(v);
      }
      var parts = String(text).split('*');
      for (var i = 0; i < parts.length; i++) {
        if (!parts[i]) continue;
        if (i % 2) {
          var b = document.createElement('b');
          b.textContent = parts[i];
          cap.appendChild(b);
        } else {
          cap.appendChild(document.createTextNode(parts[i]));
        }
      }
    }

    function pushState() {
      root.dataset.svState = JSON.stringify({
        shape: round ? round.shape : null,
        question: round ? round.key : null,
        picked: picked,
        correct: done ? (picked === round.answerKey) : null,
        streak: S.streak,
        mastered: S.mastered,
        attempted: S.attempted
      });
    }

    function runLine() {
      if (S.mastered) { run.textContent = 'You have it — keep going if you like.'; return; }
      if (!S.attempted) { run.textContent = ''; return; }
      if (S.streak === 0) { run.textContent = 'Run reset — start again.'; return; }
      run.textContent = S.streak + ' right in a row — '
        + (S.streak === 2 ? 'one more' : (3 - S.streak) + ' more') + ' and you have it.';
    }

    function choose(key, btn) {
      if (done) return;
      picked = key;
      var bs = optsEl.querySelectorAll('button');
      for (var i = 0; i < bs.length; i++) bs[i].setAttribute('aria-pressed', bs[i] === btn ? 'true' : 'false');
      go.disabled = false;
      pushState();
    }

    function newRound() {
      round = nextRound(S);
      picked = null; done = false;
      rule.textContent = round.rule;
      ask.textContent = round.ask;
      optsEl.style.setProperty('--hc-min', round.optMin);
      while (optsEl.firstChild) optsEl.removeChild(optsEl.firstChild);
      round.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'svw-hc-opt';
        b.setAttribute('aria-pressed', 'false');
        b.textContent = o.label;
        b.addEventListener('click', function () { choose(o.key, b); });
        optsEl.appendChild(b);
      });
      round.draw(svg, false);
      svg.setAttribute('aria-label', round.ask);
      go.textContent = 'Check';
      go.disabled = true;
      writeCap(round.shape === 'pedigree'
        ? 'In a family tree, a filled shape means that person has the disorder. The alleles behind it are not on show.'
        : round.shape === 'chance'
        ? 'Each child is a fresh combination — the parents’ alleles are shuffled again every time.'
        : 'Genotype is the pair of alleles a person carries. Phenotype is what you can actually see.');
      sr.textContent = round.ask;
      pushState();
    }

    function commit() {
      if (done) { newRound(); return; }
      if (!picked) return;
      done = true;
      S.attempted++;
      var right = picked === round.answerKey;
      if (right) {
        S.streak++;
        if (S.streak >= 3) S.mastered = true;
      } else {
        S.streak = 0;
      }
      var bs = optsEl.querySelectorAll('button');
      for (var i = 0; i < bs.length; i++) {
        bs[i].disabled = true;
        if (round.opts[i].key === round.answerKey) bs[i].className = 'svw-hc-opt svw-hc-right';
      }
      round.draw(svg, true);
      var text = round.body(picked);
      if (right && S.mastered && S.streak === 3) {
        text += ' Three in a row — you have it: one working allele is enough, so a carrier shows nothing yet still passes the faulty allele on.';
      }
      var h = round.head(picked);
      var cut = h.indexOf('—');
      writeCap(h.slice(cut + 1).trim() + ' ' + text, h.slice(0, cut + 1).trim(), right);
      go.textContent = S.mastered ? 'Another anyway' : 'Next question';
      go.disabled = false;
      sr.textContent = round.head(picked) + ' ' + text.replace(/\*/g, '');
      runLine();
      pushState();
    }

    go.addEventListener('click', commit);
    newRound();
    runLine();
  }

  window.SVWidget = {
    meta: {
      id: 'heterozygous-carrier-no-symptoms',
      title: 'Carrier or affected?',
      teaches: 'One working allele is enough: a heterozygous carrier of a recessive disorder has no symptoms at all, yet can still pass the faulty allele on.'
    },
    mount: mount
  };
})();
