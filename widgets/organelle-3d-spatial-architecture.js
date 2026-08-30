/* organelle-3d-spatial-architecture
   Predict where an organelle concentrates in a specialised cell, then watch the
   textbook-sparse diagram redraw itself as the crowded thing it really is. */
(function () {
  'use strict';

  var INK = '#2d2a26';
  var MUTED = '#5b564e';
  var FAINT = '#8d8880';
  var PAPER = '#faf8f5';
  var GREEN = '#4f7d63';

  /* ---------- deterministic scatter helpers ---------- */

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function box(r) {
    if (r.t === 'e') return [r.cx - r.rx, r.cy - r.ry, r.cx + r.rx, r.cy + r.ry];
    var xs = r.pts.map(function (p) { return p[0]; });
    var ys = r.pts.map(function (p) { return p[1]; });
    return [Math.min.apply(null, xs), Math.min.apply(null, ys),
            Math.max.apply(null, xs), Math.max.apply(null, ys)];
  }

  function inside(r, x, y) {
    if (r.t === 'e') {
      var dx = (x - r.cx) / r.rx, dy = (y - r.cy) / r.ry;
      return dx * dx + dy * dy <= 1;
    }
    var p = r.pts, hit = false;
    for (var i = 0, j = p.length - 1; i < p.length; j = i++) {
      var xi = p[i][0], yi = p[i][1], xj = p[j][0], yj = p[j][1];
      if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) hit = !hit;
    }
    return hit;
  }

  /* Rejection-sample n points inside any of `regions`, outside every hole. */
  function scatter(regions, holes, n, seed) {
    var rand = mulberry32(seed), out = [], guard = 0;
    var boxes = regions.map(box);
    var weights = boxes.map(function (b) { return (b[2] - b[0]) * (b[3] - b[1]); });
    var total = weights.reduce(function (a, b) { return a + b; }, 0);
    while (out.length < n && guard++ < n * 400) {
      var pick = rand() * total, k = 0;
      while (k < weights.length - 1 && pick > weights[k]) { pick -= weights[k]; k++; }
      var b = boxes[k];
      var x = b[0] + rand() * (b[2] - b[0]);
      var y = b[1] + rand() * (b[3] - b[1]);
      if (!inside(regions[k], x, y)) continue;
      var blocked = false;
      for (var h = 0; h < holes.length; h++) if (inside(holes[h], x, y)) { blocked = true; break; }
      if (!blocked) out.push([x, y]);
    }
    return out;
  }

  function shapeSvg(r, cls) {
    if (r.t === 'e') {
      return '<ellipse class="' + cls + '" cx="' + r.cx + '" cy="' + r.cy +
             '" rx="' + r.rx + '" ry="' + r.ry + '"/>';
    }
    return '<polygon class="' + cls + '" points="' +
           r.pts.map(function (p) { return p[0] + ',' + p[1]; }).join(' ') + '"/>';
  }

  function E(cx, cy, rx, ry) { return { t: 'e', cx: cx, cy: cy, rx: rx, ry: ry }; }
  function P() { return { t: 'p', pts: Array.prototype.slice.call(arguments) }; }

  /* ---------- shared strings ---------- */

  var EVEN_LABEL = 'Spread evenly — position does not matter';
  var EVEN_PICK = 'an even spread';
  var ENERGY_RULE = 'Energy is not piped around a cell. Whatever spends it has to sit beside whatever releases it.';

  /* ---------- the rounds ---------- */

  var ROUNDS = [
    {
      id: 'sperm',
      organelle: 'mitochondria',
      frame: 'A sperm cell swims to an egg, beating its tail the whole way. Predict where its mitochondria are.',
      rule: ENERGY_RULE,
      body: '<ellipse class="c-fill" cx="42" cy="46" rx="27" ry="17"/>' +
            '<rect class="c-fill" x="69" y="35" width="43" height="22" rx="5"/>',
      detail: '<ellipse class="c-org" cx="48" cy="46" rx="16" ry="10"/>' +
              '<path class="c-line" d="M42 29 A27 17 0 0 0 15 46 A27 17 0 0 0 42 63"/>' +
              '<path class="c-line" d="M112 46 C132 26 152 66 172 46 S212 26 236 46"/>',
      labels: [[42, 78, 'head', 'middle'], [91, 78, 'mid-piece', 'middle'], [190, 78, 'tail', 'middle']],
      sparse: [[30, 40], [52, 52], [86, 42], [100, 50], [38, 55]],
      sparseR: 2.4,
      cyto: { regions: [E(42, 46, 27, 17), P([69, 35], [112, 35], [112, 57], [69, 57])], holes: [E(48, 46, 16, 10)] },
      stipple: 80,
      zones: {
        mid: { label: 'Wrapped round the mid-piece, behind the head', pick: 'the mid-piece',
               regions: [P([70, 36], [111, 36], [111, 56], [70, 56])], holes: [] },
        head: { label: 'Packed into the head', pick: 'the head',
                regions: [E(42, 46, 26, 16)], holes: [],
                why: 'The head is filled by the nucleus and the enzyme cap that opens the egg.' }
      },
      answer: 'mid',
      order: ['head', 'mid', 'even', 'none'],
      evenWhy: 'Spread out, the far end of the tail waits on energy released back at the head.',
      noneWhy: 'A cell that swims for hours cannot do it without respiration.',
      dots: 70, dotR: 1.15, dotSeed: 11,
      tag: '≈ 70 mitochondria', tagAt: [91, 26],
      right: 'Right — the mid-piece. Roughly 70 mitochondria spiral round the base of the tail, so respiration releases the energy within micrometres of where it is spent.',
      fix: 'Roughly 70 spiral round the mid-piece, at the base of the tail that spends the energy.'
    },

    {
      id: 'roothair',
      organelle: 'mitochondria',
      frame: 'A root hair cell takes mineral ions from the soil by active transport. Predict where its mitochondria are.',
      rule: 'Active transport pushes ions against the gradient, and that costs energy. Energy is spent where it is released.',
      body: '<rect class="c-fill" x="74" y="14" width="140" height="72" rx="7"/>' +
            '<polygon class="c-fill" points="76,34 22,38 14,44 22,52 76,56"/>',
      detail: '<ellipse class="c-org" cx="186" cy="28" rx="15" ry="9"/>' +
              '<rect class="c-vac" x="96" y="46" width="102" height="34" rx="10"/>',
      labels: [[44, 70, 'hair', 'middle'], [181, 44, 'nucleus', 'middle'], [147, 67, 'vacuole', 'middle']],
      sparse: [[92, 26], [130, 26], [168, 62], [56, 45], [110, 84]],
      sparseR: 2.4,
      cyto: { regions: [P([76, 16], [212, 16], [212, 84], [76, 84]), P([76, 34], [22, 38], [14, 44], [22, 52], [76, 56])],
              holes: [E(186, 28, 15, 9), P([96, 46], [198, 46], [198, 80], [96, 80])] },
      stipple: 80,
      zones: {
        hair: { label: 'In the hair, close to the membrane', pick: 'the hair',
                regions: [P([80, 35], [24, 39], [17, 44], [24, 51], [80, 55])], holes: [] },
        middle: { label: 'In the middle, around the nucleus', pick: 'the middle of the cell',
                  regions: [E(160, 40, 44, 22)], holes: [],
                  why: 'The middle is taken up by the vacuole, and nothing there pumps ions.' }
      },
      answer: 'hair',
      order: ['even', 'hair', 'none', 'middle'],
      evenWhy: 'Spread evenly, most would sit far from the one surface where the pumping happens.',
      noneWhy: 'Active transport works against the gradient, so it cannot run without respiration.',
      dots: 46, dotR: 1.25, dotSeed: 23,
      tag: 'crammed into the hair', tagAt: [44, 11],
      right: 'Right — the hair. Active transport needs energy, so mitochondria crowd into the hair, pressed against the membrane where the carrier proteins pump the ions in.',
      fix: 'They crowd into the hair instead, against the membrane where the carriers pump.'
    },

    {
      id: 'palisade',
      organelle: 'chloroplasts',
      frame: 'A palisade cell lies just below the lit upper surface of a leaf. Predict where its chloroplasts are.',
      rule: 'Light is absorbed where it lands. What the top of a cell takes, the bottom never sees.',
      body: '<rect class="c-ghost" x="24" y="20" width="58" height="70" rx="6"/>' +
            '<rect class="c-ghost" x="158" y="20" width="58" height="70" rx="6"/>' +
            '<rect class="c-fill" x="91" y="20" width="58" height="70" rx="6"/>',
      detail: '<path class="c-line" d="M8 15 H232"/>' +
              '<path class="c-arrow" d="M70 2 V10 M66 7 L70 11 L74 7"/>' +
              '<path class="c-arrow" d="M120 2 V10 M116 7 L120 11 L124 7"/>' +
              '<path class="c-arrow" d="M170 2 V10 M166 7 L170 11 L174 7"/>' +
              '<ellipse class="c-org" cx="120" cy="80" rx="13" ry="7"/>',
      labels: [[30, 11, 'light', 'start'], [120, 84, 'nucleus', 'middle']],
      sparse: [[104, 34], [136, 44], [108, 58], [134, 68], [118, 48]],
      sparseR: 3,
      cyto: { regions: [P([93, 22], [147, 22], [147, 88], [93, 88])], holes: [E(120, 80, 13, 7)] },
      stipple: 70,
      zones: {
        upper: { label: 'Massed towards the top, nearest the light', pick: 'the top of the cell',
                 regions: [P([93, 22], [147, 22], [147, 54], [93, 54])], holes: [] },
        lower: { label: 'At the bottom, furthest from the light', pick: 'the bottom',
                 regions: [P([93, 60], [147, 60], [147, 88], [93, 88])], holes: [E(120, 80, 13, 7)],
                 why: 'Light is absorbed on the way down, so the bottom gets only what is left.' }
      },
      answer: 'upper',
      order: ['lower', 'none', 'upper', 'even'],
      evenWhy: 'Thinned at the top, some of the strongest light passes through unabsorbed.',
      noneWhy: 'The palisade layer is the main site of photosynthesis in the leaf.',
      dots: 46, dotR: 2.1, dotSeed: 37,
      tag: 'chloroplasts at the lit end', tagAt: [120, 98],
      right: 'Right — the top. As many as a hundred chloroplasts mass at the lit end of this mesophyll cell, and they shift as the light changes so the strongest light is caught first.',
      fix: 'They mass at the lit top of the cell instead, and shift as the light changes.'
    },

    {
      id: 'muscle',
      organelle: 'mitochondria',
      frame: 'A muscle fibre contracts by sliding protein filaments past one another. Predict where its mitochondria are.',
      rule: ENERGY_RULE,
      body: '<rect class="c-fill" x="10" y="18" width="220" height="58" rx="14"/>',
      detail: '<rect class="c-org" x="20" y="22" width="200" height="8" rx="4"/>' +
              '<rect class="c-org" x="20" y="36" width="200" height="8" rx="4"/>' +
              '<rect class="c-org" x="20" y="50" width="200" height="8" rx="4"/>' +
              '<rect class="c-org" x="20" y="64" width="200" height="8" rx="4"/>' +
              '<path class="c-tick" d="M50 22V30 M80 22V30 M110 22V30 M140 22V30 M170 22V30' +
              ' M50 36V44 M80 36V44 M110 36V44 M140 36V44 M170 36V44' +
              ' M50 50V58 M80 50V58 M110 50V58 M140 50V58 M170 50V58' +
              ' M50 64V72 M80 64V72 M110 64V72 M140 64V72 M170 64V72"/>',
      labels: [[120, 88, 'each band is a fibril', 'middle']],
      sparse: [[36, 33], [104, 33], [172, 47], [66, 61], [200, 61]],
      sparseR: 2.2,
      cyto: { regions: [P([12, 20], [228, 20], [228, 74], [12, 74])],
              holes: [P([20, 22], [220, 22], [220, 30], [20, 30]), P([20, 36], [220, 36], [220, 44], [20, 44]),
                      P([20, 50], [220, 50], [220, 58], [20, 58]), P([20, 64], [220, 64], [220, 72], [20, 72])] },
      stipple: 60,
      zones: {
        between: { label: 'In rows between the contracting fibrils', pick: 'between the fibrils',
                   regions: [P([20, 31], [220, 31], [220, 35], [20, 35]), P([20, 45], [220, 45], [220, 49], [20, 49]),
                             P([20, 59], [220, 59], [220, 63], [20, 63])], holes: [] },
        ends: { label: 'Bunched at the two ends of the fibre', pick: 'the two ends',
                regions: [P([12, 20], [34, 20], [34, 74], [12, 74]), P([206, 20], [228, 20], [228, 74], [206, 74])], holes: [],
                why: 'The filaments slide all the way along the fibre, not only at the ends.' }
      },
      answer: 'between',
      order: ['between', 'even', 'ends', 'none'],
      evenWhy: 'The fibrils are solid with filaments, so there is no room inside them.',
      noneWhy: 'A contracting fibre is one of the heaviest energy users in the body.',
      dots: 60, dotR: 1.1, dotSeed: 53,
      tag: 'rows in every gap', tagAt: [120, 12],
      right: 'Right — between the fibrils. The mitochondria sit in rows in the narrow gaps, so the energy respiration releases has almost no distance to travel to the filaments using it.',
      fix: 'They sit in rows in the narrow gaps between the fibrils, right beside the filaments.'
    },

    {
      id: 'redblood',
      organelle: 'mitochondria',
      frame: 'A red blood cell carries oxygen through the narrowest capillaries. Predict where its mitochondria are.',
      rule: ENERGY_RULE,
      body: '<circle class="c-fill" cx="66" cy="48" r="36"/>' +
            '<path class="c-fill" d="M136 48 C140 32 156 26 180 34 C204 26 220 32 224 48 C220 64 204 70 180 62 C156 70 140 64 136 48 Z"/>',
      detail: '<circle class="c-dip" cx="66" cy="48" r="17"/>',
      labels: [[66, 98, 'face on', 'middle'], [180, 98, 'from the side', 'middle'], [66, 51, 'dip', 'middle']],
      sparse: [[52, 32], [84, 42], [60, 68], [172, 44], [200, 52]],
      sparseR: 2.4,
      cyto: { regions: [E(66, 48, 35, 35), E(180, 48, 42, 15)], holes: [] },
      stipple: 200,
      zones: {
        dip: { label: 'In the dip at the centre', pick: 'the central dip',
               regions: [E(66, 48, 16, 16)], holes: [],
               why: 'The dip is the thinnest part of the cell, with the least room of anywhere in it.' },
        rim: { label: 'Around the thicker rim', pick: 'the rim',
               regions: [E(66, 48, 35, 35)], holes: [E(66, 48, 18, 18)],
               why: 'The rim is the thickest part, but it is filled with haemoglobin like the rest.' }
      },
      answer: 'none',
      order: ['rim', 'even', 'dip', 'none'],
      evenWhy: 'There is nothing to spread: this cell gave its organelles up before entering the blood.',
      dots: 0, dotR: 1, dotSeed: 71,
      tag: 'haemoglobin, no organelles', tagAt: [66, 8],
      right: 'Right — none at all. As it matures a red blood cell pushes out its nucleus and its mitochondria, so almost the whole cell is haemoglobin and it cannot use the oxygen it carries.',
      fix: 'It has none — it pushed them out as it matured, making room for haemoglobin.'
    },

    {
      id: 'secretory',
      organelle: 'ribosomes',
      frame: 'A pancreas cell makes digestive enzymes and exports them. Predict where most of its ribosomes are.',
      rule: 'A protein made in the wrong place still has to be carried to the right one.',
      body: '<ellipse class="c-fill" cx="118" cy="48" rx="78" ry="42"/>',
      detail: '<ellipse class="c-org" cx="118" cy="48" rx="25" ry="18"/>' +
              '<path class="c-line" d="M74 26 C104 12 140 14 166 30"/>' +
              '<path class="c-line" d="M68 38 C100 20 146 22 172 42"/>' +
              '<path class="c-line" d="M70 62 C102 80 144 78 170 58"/>' +
              '<path class="c-line" d="M78 72 C106 88 136 86 160 72"/>',
      labels: [[118, 51, 'nucleus', 'middle'], [118, 98, 'folded sheets: endoplasmic reticulum', 'middle']],
      sparse: [[92, 20], [150, 34], [88, 74], [156, 66], [118, 84]],
      sparseR: 2.2,
      cyto: { regions: [E(118, 48, 76, 40)], holes: [E(118, 48, 25, 18)] },
      stipple: 70,
      zones: {
        sheets: { label: 'Studded over the folded membrane sheets', pick: 'the membrane sheets',
                  regions: [E(118, 48, 60, 34)], holes: [E(118, 48, 29, 22)] },
        edge: { label: 'Lined up against the cell membrane', pick: 'the cell membrane',
                regions: [E(118, 48, 76, 40)], holes: [E(118, 48, 67, 33)],
                why: 'The membrane is the exit, not the workshop.' }
      },
      answer: 'sheets',
      order: ['none', 'sheets', 'edge', 'even'],
      evenWhy: 'Some do float free, but a loose protein still has to be caught and packed.',
      noneWhy: 'Ribosomes are where protein is made, and that is this cell’s whole job.',
      dots: 84, dotR: 1.05, dotSeed: 89,
      tag: 'ribosomes on the sheets', tagAt: [118, 12],
      right: 'Right — the membrane sheets. Most ribosomes are studded on the folded sheets around the nucleus, so a new enzyme is released straight into the channel that ships it out.',
      fix: 'Most are studded on the folded sheets round the nucleus, by the channel that exports it.'
    }
  ];

  var MASTERY = 'Right — three in a row, you have it. Position is part of the job: mitochondria where ' +
                'energy is spent, chloroplasts where light lands, and a red blood cell gives its ' +
                'organelles up for room.';

  function optionsFor(r) {
    return r.order.map(function (key) {
      if (key === 'even') return { key: 'even', label: EVEN_LABEL, pick: EVEN_PICK, why: r.evenWhy };
      if (key === 'none') return {
        key: 'none', label: 'None — this cell has no ' + r.organelle,
        pick: 'none at all', why: r.noneWhy
      };
      var z = r.zones[key];
      return { key: key, label: z.label, pick: z.pick, why: z.why };
    });
  }

  /* ---------- CSS ---------- */

  function css(ns, accent) {
    return [
      '.' + ns + '{background:#fff;border:1px solid #e8e3db;border-radius:16px;padding:1.3rem 1.25rem;',
      'font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:' + INK + ';',
      'container-type:inline-size;box-sizing:border-box;}',
      '.' + ns + ' *{box-sizing:border-box;}',
      '.' + ns + ' .k{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:' + accent + ';margin:0 0 .18rem;}',
      '.' + ns + ' h3{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.2;margin:0 0 .28rem;color:' + INK + ';}',
      '.' + ns + ' .frame{font-size:.84rem;line-height:1.45;color:' + MUTED + ';margin:0 0 .5rem;}',
      '.' + ns + ' .stage{background:' + PAPER + ';border:1px solid #efe9e0;border-radius:12px;padding:.3rem;margin:0 0 .5rem;}',
      '.' + ns + ' .stage svg{display:block;width:100%;height:auto;max-height:126px;margin:0 auto;}',
      '.' + ns + ' .c-fill{fill:#fff;stroke:#c9c0b2;stroke-width:1.3;}',
      '.' + ns + ' .c-ghost{fill:#fff;stroke:#e2dbcf;stroke-width:1.1;opacity:.7;}',
      '.' + ns + ' .c-org{fill:#e6dfd3;stroke:#c9c0b2;stroke-width:1;}',
      '.' + ns + ' .c-vac{fill:#f1ece2;stroke:#d8d0c2;stroke-width:1;}',
      '.' + ns + ' .c-dip{fill:#f2ece2;stroke:#d8d0c2;stroke-width:1;}',
      '.' + ns + ' .c-line{fill:none;stroke:#b8ae9e;stroke-width:1.6;stroke-linecap:round;}',
      '.' + ns + ' .c-arrow{fill:none;stroke:' + accent + ';stroke-width:1.4;stroke-linecap:round;stroke-linejoin:round;}',
      '.' + ns + ' .c-tick{fill:none;stroke:#ded6c8;stroke-width:.8;}',
      '.' + ns + ' .lab{font-size:10px;fill:' + MUTED + ';font-family:Inter,system-ui,sans-serif;}',
      '.' + ns + ' .tagline{font-size:10px;fill:' + FAINT + ';font-family:Inter,system-ui,sans-serif;}',
      '.' + ns + ' .cnt{font-size:10px;font-weight:600;fill:' + INK + ';font-family:Inter,system-ui,sans-serif;}',
      '.' + ns + ' .wash ellipse,.' + ns + ' .wash polygon{fill:' + accent + ';fill-opacity:.17;stroke:none;}',
      '.' + ns + ' .wash .cut{fill:#fff;fill-opacity:1;}',
      '.' + ns + ' .sparse ellipse{fill:#ddd4c4;stroke:#bdb3a1;stroke-width:.7;}',
      '.' + ns + ' .sparse{transition:opacity .18s ease;}',
      '.' + ns + ' .stip circle{fill:' + FAINT + ';fill-opacity:.55;}',
      '.' + ns + ' .real circle{fill:' + accent + ';fill-opacity:.92;}',
      '.' + ns + ' .fade{opacity:0;transition:opacity .3s ease;}',
      '.' + ns + ' .fade.on{opacity:1;}',
      '.' + ns + ' .opts{display:grid;grid-template-columns:1fr;gap:.34rem;margin:0 0 .5rem;}',
      '.' + ns + ' .opt{display:block;width:100%;text-align:left;font:inherit;font-size:.82rem;font-weight:600;',
      'line-height:1.35;padding:.44rem .78rem;border-radius:10px;border:1px solid #ddd7cd;background:' + PAPER + ';',
      'color:' + INK + ';cursor:pointer;}',
      '.' + ns + ' .opt:hover:not(:disabled){border-color:#c6bdaf;}',
      '.' + ns + ' .opt[aria-pressed="true"]{box-shadow:inset 0 0 0 2px ' + accent + ';border-color:' + accent + ';}',
      '.' + ns + ' .opt.key{background:' + INK + ';color:#fff;border-color:' + INK + ';box-shadow:none;}',
      '.' + ns + ' .opt:disabled{cursor:default;}',
      '.' + ns + ' .opt.dim{opacity:.45;}',
      '.' + ns + ' .dot{display:none;width:.42rem;height:.42rem;border-radius:50%;margin-right:.42rem;',
      'vertical-align:middle;background:' + GREEN + ';}',
      '.' + ns + ' .opt.key .dot{display:inline-block;}',
      '.' + ns + ' .row{display:flex;align-items:center;justify-content:space-between;gap:.6rem;margin:0 0 .45rem;}',
      '.' + ns + ' .run{font-size:.76rem;font-weight:600;color:' + MUTED + ';font-variant-numeric:tabular-nums;}',
      '.' + ns + ' .go{font:inherit;font-size:.82rem;font-weight:600;padding:.48rem 1.05rem;border-radius:10px;',
      'border:1px solid ' + INK + ';background:' + INK + ';color:#fff;cursor:pointer;flex:0 0 auto;}',
      '.' + ns + ' .go:disabled{background:' + PAPER + ';color:' + FAINT + ';border-color:#ddd7cd;cursor:default;}',
      '.' + ns + ' .cap{font-size:.86rem;line-height:1.5;color:' + INK + ';margin:0;min-height:4.5em;}',
      '.' + ns + ' .sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;',
      'clip:rect(0 0 0 0);white-space:nowrap;border:0;}',
      '@media (min-width:600px){.' + ns + ' .opts{grid-template-columns:1fr 1fr;}}',
      '@container (min-width:520px){.' + ns + ' .opts{grid-template-columns:1fr 1fr;}}',
      '.' + ns + '.rm .sparse,.' + ns + '.rm .fade{transition:none;}',
      '.' + ns + '.rm .fade{opacity:1;}'
    ].join('');
  }

  /* ---------- mount ---------- */

  window.SVWidget = {
    meta: {
      id: 'organelle-3d-spatial-architecture',
      title: 'Where the organelles actually sit',
      teaches: 'Organelles are packed into a crowded arrangement in which position serves the cell’s job, not scattered at random through empty cytoplasm.'
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var ns = 'svw-osa';
      var accent = (ctx.accent && /^#[0-9a-f]{6}$/i.test(ctx.accent)) ? ctx.accent
        : ((getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6f4e');
      var reduced = !!ctx.reducedMotion;

      var style = document.createElement('style');
      style.textContent = css(ns, accent);
      root.appendChild(style);

      var wrap = document.createElement('div');
      wrap.className = ns + (reduced ? ' rm' : '');
      wrap.innerHTML =
        '<p class="k">Cell structure</p>' +
        '<h3>Where the organelles actually sit</h3>' +
        '<p class="frame" data-frame></p>' +
        '<div class="stage" data-stage></div>' +
        '<div class="opts" data-opts></div>' +
        '<div class="row"><span class="run" data-run></span>' +
        '<button type="button" class="go" data-go disabled>Check</button></div>' +
        '<p class="cap" data-cap></p>' +
        '<p class="sr" aria-live="polite" data-sr></p>';
      root.appendChild(wrap);

      var elFrame = wrap.querySelector('[data-frame]');
      var elStage = wrap.querySelector('[data-stage]');
      var elOpts = wrap.querySelector('[data-opts]');
      var elRun = wrap.querySelector('[data-run]');
      var elGo = wrap.querySelector('[data-go]');
      var elCap = wrap.querySelector('[data-cap]');
      var elSr = wrap.querySelector('[data-sr]');

      var state = { streak: 0, mastered: false, attempted: 0, chosen: null, revealed: false };
      var queue = [], round = null, opts = [], buttons = [];

      function keyIndex(key) {
        for (var i = 0; i < opts.length; i++) if (opts[i].key === key) return i;
        return -1;
      }

      function shuffle(a) {
        for (var i = a.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
        }
        return a;
      }

      function nextRound() {
        if (!queue.length) {
          var pool = ROUNDS.filter(function (r) { return !round || r.id !== round.id; });
          queue = shuffle(pool);
        }
        return queue.shift();
      }

      function drawStage() {
        var r = round;
        var s = '<svg viewBox="0 0 240 112" role="img" aria-label="Diagram of a specialised cell">';
        s += '<g>' + r.body + '</g>';
        s += '<g class="wash" data-wash></g>';
        s += '<g>' + r.detail + '</g>';
        s += '<g class="sparse" data-sparse>' + r.sparse.map(function (p) {
          return '<ellipse cx="' + p[0] + '" cy="' + p[1] + '" rx="' + r.sparseR +
                 '" ry="' + (r.sparseR * 0.72) + '"/>';
        }).join('') + '</g>';
        s += '<g class="real fade" data-real></g>';
        s += '<g class="stip fade" data-stip></g>';
        s += '<g>' + r.labels.map(function (l) {
          return '<text class="lab" x="' + l[0] + '" y="' + l[1] + '" text-anchor="' + l[3] + '">' + l[2] + '</text>';
        }).join('') + '</g>';
        s += '<text class="cnt fade" data-cnt x="' + r.tagAt[0] + '" y="' + r.tagAt[1] + '" text-anchor="middle"></text>';
        s += '<text class="tagline" data-tag x="2" y="110">as textbooks draw it</text>';
        s += '</svg>';
        elStage.innerHTML = s;
      }

      function paintWash(key) {
        var g = elStage.querySelector('[data-wash]');
        var spark = elStage.querySelector('[data-sparse]');
        if (spark) spark.style.opacity = (key === 'none') ? '.14' : '1';
        if (!g) return;
        var out = '';
        if (key && key !== 'none') {
          var src = (key === 'even') ? round.cyto : round.zones[key];
          out = src.regions.map(function (z) { return shapeSvg(z, ''); }).join('') +
                (src.holes || []).map(function (z) { return shapeSvg(z, 'cut'); }).join('');
        }
        g.innerHTML = out;
      }

      function restate(o) {
        if (o.key === 'even') return 'An even spread: every part of the cytoplasm holding the same number.';
        if (o.key === 'none') return 'None: this cell doing its job without a single one.';
        return 'Your answer: ' + o.pick + '.';
      }

      function startRound() {
        round = nextRound();
        opts = optionsFor(round);
        state.chosen = null;
        state.revealed = false;
        elFrame.textContent = round.frame;
        drawStage();

        elOpts.innerHTML = '';
        buttons = opts.map(function (o) {
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'opt';
          b.setAttribute('aria-pressed', 'false');
          b.innerHTML = '<span class="dot"></span>' + o.label;
          b.addEventListener('click', function () { choose(o.key); });
          elOpts.appendChild(b);
          return b;
        });

        elGo.textContent = 'Check';
        elGo.disabled = true;
        elCap.textContent = round.rule;
        elRun.textContent = state.streak ? state.streak + ' in a row' : '';
        push();
      }

      function choose(key) {
        if (state.revealed) return;
        state.chosen = key;
        buttons.forEach(function (b, i) {
          b.setAttribute('aria-pressed', opts[i].key === key ? 'true' : 'false');
        });
        paintWash(key);
        elCap.textContent = restate(opts[keyIndex(key)]);
        elGo.disabled = false;
        push();
      }

      function reveal() {
        var r = round, correct = (state.chosen === r.answer);
        state.revealed = true;
        state.attempted += 1;
        state.streak = correct ? state.streak + 1 : 0;
        if (state.streak >= 3) state.mastered = true;

        var spark = elStage.querySelector('[data-sparse]');
        if (spark) spark.style.opacity = '0';

        var wash = elStage.querySelector('[data-wash]');
        if (wash) {
          wash.innerHTML = (r.answer === 'none') ? '' :
            r.zones[r.answer].regions.map(function (z) { return shapeSvg(z, ''); }).join('') +
            (r.zones[r.answer].holes || []).map(function (z) { return shapeSvg(z, 'cut'); }).join('');
        }

        elStage.querySelector('[data-stip]').innerHTML =
          scatter(r.cyto.regions, r.cyto.holes, r.stipple, r.dotSeed + 500).map(function (p) {
            return '<circle cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" r="0.8"/>';
          }).join('');

        var real = '';
        if (r.dots > 0) {
          var z = r.zones[r.answer];
          real = scatter(z.regions, z.holes || [], r.dots, r.dotSeed).map(function (p) {
            return '<circle cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" r="' + r.dotR + '"/>';
          }).join('');
        }
        elStage.querySelector('[data-real]').innerHTML = real;
        elStage.querySelector('[data-cnt]').textContent = r.tag;
        elStage.querySelector('[data-tag]').textContent = 'as it really is: nothing here is empty';
        ['[data-real]', '[data-stip]', '[data-cnt]'].forEach(function (sel) {
          elStage.querySelector(sel).classList.add('on');
        });

        buttons.forEach(function (b, i) {
          b.disabled = true;
          var isKey = opts[i].key === r.answer;
          var isMine = opts[i].key === state.chosen;
          if (isKey) b.classList.add('key');
          if (!isKey && !isMine) b.classList.add('dim');
        });

        var msg;
        if (correct) {
          msg = state.mastered ? MASTERY : r.right + (state.streak === 2 ? ' Two in a row — one more.' : '');
        } else {
          var mine = opts[keyIndex(state.chosen)];
          msg = 'Not quite — you chose ' + mine.pick + '. ' + (mine.why ? mine.why + ' ' : '') + r.fix;
        }
        elCap.textContent = msg;
        elSr.textContent = msg;
        elRun.textContent = state.streak ? state.streak + ' in a row' : '';
        elGo.textContent = state.mastered ? 'Another anyway' : 'Next cell';
        elGo.disabled = false;
        push();
      }

      function push() {
        root.dataset.svState = JSON.stringify({
          round: round ? round.id : null,
          chosen: state.chosen,
          correct: state.revealed ? (state.chosen === round.answer) : null,
          streak: state.streak,
          mastered: state.mastered,
          attempted: state.attempted
        });
      }

      elGo.addEventListener('click', function () {
        if (!state.revealed) { if (state.chosen) reveal(); return; }
        startRound();
        if (buttons[0]) buttons[0].focus();
      });

      /* open on the sperm cell: the most vivid case and a fair first read */
      queue = shuffle(ROUNDS.slice(1));
      queue.unshift(ROUNDS[0]);
      startRound();
    }
  };
})();
