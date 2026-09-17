// 03 growth : "The cell grows". Global T 4.5 to 7.0 (shot-local 0 to 2.5), illustrated paper plate.
//
// The cell starts exactly on G1 (01's cell: centre (540,900), mean radius 380, nucleus 170) and
// inflates on the four beats to radius 440, making more mitochondria and more ribosomes as it goes.
// The chromosome count never changes: two chromoA (long, blue) and two chromoB (short, rust) are
// drawn in every frame, in the G1 arrangement, so the viewer can count them before and after.
//
// Layers, back to front:
//   stripes (screen space: stripeCream and stripeSage, drifting 6 px per beat)
//   > under the camera (push 1.00 -> 1.03 on inOutSine, world (540,900) pinned to screen (540,900)):
//       five neighbour cells cut by the frame edge (G1 positions, 72 percent)
//       > hero cytoplasm, its membrane-band hatch in cytoHatch and the shaded lower-right
//       > construction lines: the 45 degree diameters, the blocking square, and a dotted ghost
//         circle left behind on every radius the membrane has already passed
//       > ribosome stipple in inkFaint, density stepping 0.35 -> 0.60 on the beats
//       > twelve mitochondria: G1's six, plus six that draw in two to a beat with folded cristae
//       > nucleus, nucleolus, nuclear pores, and the four chromosomes as loose worm shapes
//       > the membrane itself, 6 px ink with a doubled retrace
//   > overlays (screen space, never hatched, full opacity): the annBlue ruler at x 960 and the
//     growth bracket that stretches past its ends, a chevron on the ruler for each radius reached,
//     the annYellow mitochondrion tally ring at (180,300) with a bean glyph inside, a pop ring per
//     new mitochondrion, and the nucleus pulse on the last beat
//   > the cycle glyph (FILM.lib.cycleGlyph, the canonical helper), always last.
//
// Chromosomes, mitochondria and the membrane pose move on twos; the push, the ruler, the bracket
// and every ring run at a full 24 fps; ink lines boil at 12 fps.
(function () {
  'use strict';

  const FILM = window.FILM;
  const LIB = FILM.lib;
  const P = LIB.pal;
  const E = LIB.ease;

  const ID = 'growth';
  // G1 belongs to the cold open: its outline noise, its nucleus and its organelle placement are
  // seeded from that shot's id so the silhouette is the same cell in 01, 02 and here.
  const REF = 'hero-cell';

  const DUR = 2.5;
  const LAST_F = 59; // 60 frames at 24 fps; the last one holds
  const FR = 1 / 24;
  const TAU = Math.PI * 2;

  const clamp = LIB.clamp;
  const lerp = LIB.lerp;
  const sstep = (a, b, x) => {
    const u = clamp((x - a) / (b - a));
    return u * u * (3 - 2 * u);
  };
  const sd = (...k) => LIB.hash(ID, ...k) & 0x7fffffff;
  const gsd = (...k) => LIB.hash(REF, ...k) & 0x7fffffff;

  // ===========================================================================
  // Numbers from the storyboard: G1, and 03's beat sheet
  // ===========================================================================

  const CX = 540, CY = 900;

  // beats, shot-local: T 5.0, 5.5, 6.0, 6.5
  const BEAT = [0.5, 1.0, 1.5, 2.0];
  const BEAT_F = [12, 24, 36, 48];

  // mean membrane radius before the first beat, then after each beat
  const RAD = [380, 398, 414, 428, 440];
  // the nucleus only grows on the third beat (T 6.0)
  const NUCR = [170, 170, 170, 185, 185];
  // ribosome stipple density rises across the shot
  const STIP = [0.35, 0.41, 0.47, 0.54, 0.6];

  // a three-drawing pop with a 7 percent overshoot (art bible 7.2)
  const POP3 = [0.52, 1.07, 1];

  // nucleolus: a 40 px disc at (500,870) in the G1 nucleus, carried out as the nucleus grows
  const NUCLEOLUS = { dx: -40, dy: -30, r: 20 };

  // ---------------------------------------------------------------------------
  // The four chromosomes (G1). Two pairs, four in total, and this shot never changes that.
  // Both members of a pair are the same length; the pairs differ. 20 degrees off horizontal,
  // tilted alternately left and right.
  // ---------------------------------------------------------------------------

  const CHROMO = [
    { key: 'A1', x: 470, y: 850, len: 130, tilt: -20, hw: 7.5, fill: 'chromoA', deep: 'chromoADeep' },
    { key: 'A2', x: 610, y: 850, len: 130, tilt: 20, hw: 7.5, fill: 'chromoA', deep: 'chromoADeep' },
    { key: 'B1', x: 480, y: 955, len: 85, tilt: -20, hw: 7.5, fill: 'chromoB', deep: 'chromoBDeep' },
    { key: 'B2', x: 600, y: 955, len: 85, tilt: 20, hw: 7.5, fill: 'chromoB', deep: 'chromoBDeep' },
  ];

  // ---------------------------------------------------------------------------
  // Mitochondria. The first six are G1's; the last six draw in two to a beat at the storyboard's
  // positions. `f` is the frame the draw-on starts, `tick` the slot it fills on the tally ring.
  // ---------------------------------------------------------------------------

  const MITO = [
    { x: 300, y: 700, f: -1 },
    { x: 760, y: 720, f: -1 },
    { x: 280, y: 1060, f: -1 },
    { x: 790, y: 1080, f: -1 },
    { x: 420, y: 1190, f: -1 },
    { x: 660, y: 640, f: -1 },
    { x: 360, y: 560, f: 12, beat: 0, tick: 0 }, // T 5.0
    { x: 720, y: 1240, f: 15, beat: 0, tick: 1 },
    { x: 240, y: 900, f: 24, beat: 1, tick: 2 }, // T 5.5
    { x: 840, y: 900, f: 27, beat: 1, tick: 3 },
    { x: 500, y: 1240, f: 36, beat: 2, tick: 4 }, // T 6.0
    { x: 620, y: 560, f: 39, beat: 2, tick: 5 },
  ];

  const MITO_LEN = 60, MITO_WID = 28; // 60 by 28 px beans

  // ---------------------------------------------------------------------------
  // Neighbour cells: partial circles cut by the frame edge (G1), radius 300 to 360, 72 percent.
  // ---------------------------------------------------------------------------

  const NEIGH = [
    { x: 60, y: 380, r: 320 },
    { x: 1020, y: 420, r: 340 },
    { x: 40, y: 1420, r: 300 },
    { x: 1040, y: 1400, r: 360 },
    { x: 540, y: 1690, r: 330 },
  ];

  // ---------------------------------------------------------------------------
  // Overlay geometry
  // ---------------------------------------------------------------------------

  const RULER_X = 960, RULER_Y0 = 520, RULER_Y1 = 1280; // exactly the G1 cell's diameter
  const BRACKET_X = 918;
  const TALLY = { x: 180, y: 300, r: 46 };

  // ===========================================================================
  // Small geometry helpers
  // ===========================================================================

  // periodic wobble round a circle: noise sampled on the circle itself, so the closed outline
  // has no seam where the polyline meets its start
  function nAt(a, seed, k) {
    return LIB.noise2(Math.cos(a) * k, Math.sin(a) * k, seed);
  }

  // Enough lobes that the silhouette reads as a living cell rather than a compass circle, at the
  // amplitude the shared geometry fixes. Both octaves are kept under half the sample count: a
  // finer one would alias into a faceted rounded polygon, which is exactly what a hand-inked
  // membrane must not look like.
  function ringNoise(n, seed) {
    const out = new Float64Array(n);
    const k1 = n / 22, k2 = n / 13;
    for (let i = 0; i < n; i++) {
      const a = -Math.PI / 2 + (i / n) * TAU;
      out[i] = clamp(0.74 * nAt(a, seed, k1) + 0.32 * nAt(a, seed + 7, k2), -1, 1);
    }
    return out;
  }

  // G1: "an irregular near-circle ... a 40-point polyline with radius 380 + 14 * noise"
  const CELL_N = ringNoise(40, gsd('cell'));
  const NUC_N = ringNoise(32, gsd('nucleus'));

  function ringPts(cx, cy, r, amp, table) {
    const n = table.length;
    const out = new Array(n);
    for (let i = 0; i < n; i++) {
      const a = -Math.PI / 2 + (i / n) * TAU;
      const rr = r + amp * table[i];
      out[i] = [cx + Math.cos(a) * rr, cy + Math.sin(a) * rr];
    }
    return out;
  }

  const cellPts = (r) => ringPts(CX, CY, r, 14, CELL_N);
  const nucPts = (r) => ringPts(CX, CY, r, 8, NUC_N);

  const scaleAbout = (pts, cx, cy, s) => pts.map((p) => [cx + (p[0] - cx) * s, cy + (p[1] - cy) * s]);

  // A rod: offset a centreline by a width profile that is flat through the middle and rounds off
  // at both ends. `endPow` sets how square the ends are, `fullPow` how full the middle is.
  function rodOutline(pts, hw, endPow, fullPow) {
    const n = pts.length;
    const left = [], right = [];
    for (let i = 0; i < n; i++) {
      const a = pts[i > 0 ? i - 1 : 0], b = pts[i < n - 1 ? i + 1 : n - 1];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      tx /= tl;
      ty /= tl;
      const u = i / (n - 1);
      const w = hw * Math.pow(Math.max(0, 1 - Math.pow(Math.abs(2 * u - 1), endPow)), fullPow);
      left.push([pts[i][0] - ty * w, pts[i][1] + tx * w]);
      right.push([pts[i][0] + ty * w, pts[i][1] - tx * w]);
    }
    right.reverse();
    return left.concat(right);
  }

  // a gently bowed spine of `len` px through (cx, cy) at `tilt` radians, bowed `bow` px sideways
  function bowedSpine(cx, cy, len, tilt, bow, n) {
    const ca = Math.cos(tilt), sa = Math.sin(tilt);
    const out = [];
    for (let i = 0; i < n; i++) {
      const u = i / (n - 1);
      const s = (u - 0.5) * len;
      const v = bow * Math.sin(Math.PI * u);
      out.push([cx + s * ca - v * sa, cy + s * sa + v * ca]);
    }
    return out;
  }

  // ===========================================================================
  // Chromosomes: loose worm shapes, drawn (never hidden) so the four can be counted
  // ===========================================================================

  // The spine is a lazy S whose swing tapers to nothing at the tips. `k` is the on-twos drawing
  // index: the whole worm drifts a couple of pixels per drawing so it lives without moving house.
  function wormSpine(ch, k) {
    const seed = gsd('worm', ch.key);
    const tilt = (ch.tilt * Math.PI) / 180;
    const ca = Math.cos(tilt), sa = Math.sin(tilt);
    const ph = LIB.h3(seed, 3, 11) * TAU;
    const n = 13;
    const pts = [];
    for (let i = 0; i < n; i++) {
      const u = i / (n - 1);
      const s = (u - 0.5) * ch.len;
      const env = Math.pow(Math.sin(Math.PI * u), 0.55);
      let v = ch.len * 0.135 * Math.sin(u * Math.PI * 1.75 + ph) * env;
      v += ch.len * 0.055 * LIB.noise1(u * 3.4 + 4.1, seed + 5) * env;
      // the worm breathes on twos: a slow travelling ripple, 2.5 px at most
      v += 2.5 * env * LIB.noise1(u * 2.1 + k * 0.62, seed + 9);
      const dx = 1.6 * LIB.noise1(k * 0.51 + 2.3, seed + 13);
      const dy = 1.6 * LIB.noise1(k * 0.47 + 8.7, seed + 17);
      pts.push([ch.x + s * ca - v * sa + dx, ch.y + s * sa + v * ca + dy]);
    }
    return LIB.smoothPts(pts, false, 5);
  }

  function drawChromosome(ctx, ch, k) {
    const spine = wormSpine(ch, k);
    const shape = rodOutline(spine, ch.hw, 6, 0.42);
    const fill = P[ch.fill], deep = P[ch.deep];
    const seed = sd('chromo', ch.key);

    // body: flat colour with an ink outline (art bible 3.1, secondary form)
    LIB.inkPath(ctx, shape, {
      closed: true,
      width: 2.6,
      color: P.ink,
      fill,
      seed,
      wobble: 0.7,
      tremble: 0.25,
      taper: [8, 14],
      step: 3,
    });
    // shadow on the lower right only; the lit upper left stays flat colour
    LIB.hatch(ctx, shape, {
      angle: -Math.PI / 4,
      spacing: 5,
      width: 1.2,
      color: deep,
      alpha: 0.85,
      length: [5, 15],
      gap: [2, 4],
      inset: 1.5,
      overshoot: 0.5,
      clip: true,
      seed: seed + 3,
      density: (x, y) => sstep(-0.1, 0.85, ((x - ch.x) * 0.707 + (y - ch.y) * 0.707) / (ch.len * 0.34) + 0.25),
    });
    // a darker thread along the shadow flank, so the worm reads as round, not flat
    const flank = [];
    for (let i = 1; i < spine.length - 1; i += 2) {
      const a = spine[i - 1], b = spine[i + 1];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      const u = i / (spine.length - 1);
      const w = ch.hw * 0.52 * Math.pow(Math.max(0, 1 - Math.pow(Math.abs(2 * u - 1), 6)), 0.42);
      flank.push([spine[i][0] + (ty / tl) * w, spine[i][1] - (tx / tl) * w]);
    }
    if (flank.length > 2) {
      LIB.inkPath(ctx, flank, { width: 1.5, color: deep, alpha: 0.7, seed: seed + 5, taper: [6, 10], wobble: 0.5 });
    }
  }

  // ===========================================================================
  // Mitochondria: beans with folded inner ridges
  // ===========================================================================

  // Positions come straight from the storyboard, except that a bean placed outside the membrane
  // it belongs to would be a drawing error: any centre further out than the radius that beat
  // reaches is pulled back along its own radius, and every bean lies across the radius (a bean
  // hugging the flow of the cytoplasm), so none of them spears the membrane.
  const MITOS = MITO.map((m, i) => {
    const seed = gsd('mito', i);
    let dx = m.x - CX, dy = m.y - CY;
    const d = Math.hypot(dx, dy) || 1;
    const rAtBeat = m.f < 0 ? RAD[0] : RAD[m.beat + 1];
    // no two organelles are stamped from one die: each bean is a shade longer or shorter
    const size = lerp(0.86, 1.14, LIB.h3(seed, 11, 4));
    const len = MITO_LEN * size, wid = MITO_WID * lerp(0.92, 1.08, LIB.h3(seed, 13, 6)) / size * 0.98;
    const dMax = rAtBeat - (len * 0.5 + 16);
    const s = d > dMax ? dMax / d : 1;
    const x = CX + dx * s, y = CY + dy * s;
    const radial = Math.atan2(dy, dx);
    const rot = radial + Math.PI / 2 + (LIB.h3(seed, 5, 2) - 0.5) * 1.5;
    const bow = (LIB.h3(seed, 7, 3) - 0.5) * 2 * 8;
    const spine = bowedSpine(x, y, len, rot, bow, 17);
    const shape = rodOutline(spine, wid / 2, 2.4, 0.42);
    const MITO_WID_L = wid;
    // cristae: folds crossing the bean from alternate sides
    const cr = [];
    const nCr = 7;
    for (let c = 0; c < nCr; c++) {
      const u = (c + 0.85) / (nCr + 0.7);
      const idx = clamp(u, 0, 1) * (spine.length - 1);
      const i0 = Math.floor(idx);
      const i1 = Math.min(spine.length - 1, i0 + 1);
      const fr = idx - i0;
      const px = lerp(spine[i0][0], spine[i1][0], fr);
      const py = lerp(spine[i0][1], spine[i1][1], fr);
      const a = spine[Math.max(0, i0 - 1)], b = spine[Math.min(spine.length - 1, i1 + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      tx /= tl;
      ty /= tl;
      const nx = -ty, ny = tx;
      const sgn = c % 2 ? 1 : -1;
      const hw = (MITO_WID_L / 2) * Math.pow(Math.max(0, 1 - Math.pow(Math.abs(2 * u - 1), 2.4)), 0.42);
      // a fold reaches most of the way across the bean, hooking back a little at its tip
      const reach = hw * lerp(1.55, 1.95, LIB.h3(seed, c, 9));
      const lean = tx * (LIB.h3(seed, c, 11) - 0.5) * 7;
      const leanY = ty * (LIB.h3(seed, c, 11) - 0.5) * 7;
      cr.push([
        [px + nx * (hw - 1) * sgn, py + ny * (hw - 1) * sgn],
        [px + nx * (hw - reach * 0.5) * sgn + lean * 0.5, py + ny * (hw - reach * 0.5) * sgn + leanY * 0.5],
        [px + nx * (hw - reach) * sgn + lean, py + ny * (hw - reach) * sgn + leanY],
      ]);
    }
    return { i, x, y, rot, spine, shape, cr, seed, hw: MITO_WID_L / 2, f: m.f, tick: m.tick, beat: m.beat };
  });

  // prog 0..1 draws the bean on: the outline travels round, then the fill, then the cristae
  function drawMito(ctx, m, prog) {
    if (prog <= 0.001) return;
    const seed = sd('bean', m.i);
    if (prog >= 0.999) {
      LIB.inkPath(ctx, m.shape, {
        closed: true,
        width: 3,
        color: P.ink,
        fill: P.mito,
        seed,
        wobble: 0.8,
        tremble: 0.3,
        taper: [10, 18],
        step: 3,
      });
    } else {
      // partial: the pen runs round the bean and the colour floods in behind it
      const n = m.shape.length;
      const cut = Math.max(3, Math.round(n * clamp(prog / 0.55)));
      const part = m.shape.slice(0, cut);
      if (prog > 0.4) {
        ctx.save();
        ctx.globalAlpha *= sstep(0.4, 0.85, prog);
        ctx.fillStyle = P.mito;
        ctx.beginPath();
        LIB.tracePath(ctx, m.shape, true);
        ctx.fill();
        ctx.restore();
      }
      LIB.inkPath(ctx, part, { width: 3, color: P.ink, seed, wobble: 0.8, tremble: 0.3, taper: [8, 4], step: 3 });
    }

    // inner membrane, a hair inside the outline
    if (prog > 0.6) {
      const inner = m.shape.map((p) => [m.x + (p[0] - m.x) * 0.78, m.y + (p[1] - m.y) * 0.78]);
      ctx.save();
      ctx.globalAlpha *= sstep(0.6, 0.9, prog);
      LIB.inkPath(ctx, inner, { closed: true, width: 1.3, color: P.mitoDeep, alpha: 0.5, seed: seed + 1, wobble: 0.5, taper: [6, 10], step: 4 });
      ctx.restore();
    }

    // cristae, one per 1/6 of the draw-on tail
    for (let c = 0; c < m.cr.length; c++) {
      const th = 0.62 + (c / m.cr.length) * 0.36;
      if (prog < th) continue;
      ctx.save();
      ctx.globalAlpha *= clamp((prog - th) / 0.08 + 0.35);
      LIB.inkPath(ctx, m.cr[c], { width: 2.4, color: P.mitoDeep, alpha: 1, seed: seed + 20 + c, taper: [2, 5], wobble: 0.4, tremble: 0.2 });
      ctx.restore();
    }

    // shadow on the lower right of the bean
    if (prog > 0.75) {
      ctx.save();
      ctx.globalAlpha *= sstep(0.75, 1, prog);
      LIB.hatch(ctx, m.shape, {
        angle: -Math.PI / 4,
        spacing: 5,
        width: 1.3,
        color: P.mitoDeep,
        alpha: 0.8,
        length: [5, 14],
        gap: [2, 5],
        inset: 2,
        overshoot: 0,
        clip: true,
        seed: seed + 40,
        density: (x, y) => sstep(-0.2, 0.9, ((x - m.x) * 0.707 + (y - m.y) * 0.707) / (m.hw * 1.25)),
      });
      ctx.restore();
    }
  }

  // ===========================================================================
  // Neighbour cells
  // ===========================================================================

  const NEIGHS = NEIGH.map((nb, i) => {
    const seed = gsd('nb', i);
    const table = ringNoise(28, seed);
    const outline = ringPts(nb.x, nb.y, nb.r, nb.r * 0.036, table);
    const nr = nb.r * 0.36;
    const nTable = ringNoise(22, seed + 3);
    const ang = LIB.h3(seed, 2, 5) * TAU;
    const off = nb.r * 0.12;
    const ncx = nb.x + Math.cos(ang) * off, ncy = nb.y + Math.sin(ang) * off;
    const nucleus = ringPts(ncx, ncy, nr, nr * 0.05, nTable);
    // two organelles apiece, kept well inside
    const beans = [];
    for (let b = 0; b < 2; b++) {
      const a = LIB.h3(seed, b, 7) * TAU;
      const d = nb.r * lerp(0.55, 0.74, LIB.h3(seed, b, 8));
      const bx = nb.x + Math.cos(a) * d, by = nb.y + Math.sin(a) * d;
      const sp = bowedSpine(bx, by, MITO_LEN * 0.92, a + Math.PI / 2, 5, 13);
      beans.push({ pts: rodOutline(sp, MITO_WID * 0.45, 2.4, 0.42), x: bx, y: by });
    }
    return { i, cx: nb.x, cy: nb.y, r: nb.r, outline, nucleus, ncx, ncy, nr, beans, seed };
  });

  // The neighbours are the tissue the hero sits in, not rivals for it: one hero cell has to hold
  // the frame, so they are drawn in the same hand at about half weight and never carry ink as
  // black as the hero's membrane.
  function drawNeighbour(ctx, nb) {
    ctx.save();
    ctx.globalAlpha *= 0.52;
    // cytoplasm
    LIB.inkPath(ctx, nb.outline, {
      closed: true,
      width: 2.8,
      color: P.inkSoft,
      alpha: 0.85,
      fill: P.neighbour,
      seed: sd('nbout', nb.i),
      wobble: 1.6,
      tremble: 0.4,
      taper: [14, 24],
      step: 5,
    });
    // tone on the lower right
    LIB.hatch(ctx, nb.outline, {
      angle: -Math.PI / 4,
      spacing: 13,
      width: 1.3,
      color: P.cytoHatch,
      alpha: 0.75,
      length: [14, 44],
      inset: 8,
      clip: true,
      seed: sd('nbhatch', nb.i),
      density: (x, y) => sstep(0.15, 1, ((x - nb.cx) * 0.707 + (y - nb.cy) * 0.707) / nb.r),
    });
    for (const b of nb.beans) {
      LIB.inkPath(ctx, b.pts, { closed: true, width: 2, color: P.inkSoft, alpha: 0.7, fill: P.mito, seed: sd('nbbean', nb.i, b.x | 0), wobble: 0.6, taper: [8, 14], step: 5 });
    }
    // nucleus
    LIB.inkPath(ctx, nb.nucleus, {
      closed: true,
      width: 2.2,
      color: P.inkSoft,
      alpha: 0.8,
      fill: P.neighbourNucleus,
      fillAlpha: 0.85,
      seed: sd('nbnuc', nb.i),
      wobble: 1,
      taper: [10, 18],
      step: 5,
    });
    LIB.hatch(ctx, nb.nucleus, {
      angle: -Math.PI / 4,
      spacing: 10,
      width: 1.1,
      color: P.nucleusDeep,
      alpha: 0.45,
      length: [8, 24],
      inset: 4,
      clip: true,
      seed: sd('nbnh', nb.i),
      density: (x, y) => sstep(0.2, 1, ((x - nb.ncx) * 0.707 + (y - nb.ncy) * 0.707) / nb.nr),
    });
    ctx.restore();
  }

  // ===========================================================================
  // Layers under the camera
  // ===========================================================================

  function drawCytoplasm(ctx, cell, R) {
    // flat fill through the wobbled outline
    LIB.inkPath(ctx, cell, {
      closed: true,
      width: 0.6,
      color: P.cytoplasm,
      alpha: 0.9,
      fill: P.cytoplasm,
      seed: sd('cytofill'),
      wobble: 1.4,
      tremble: 0.3,
      taper: [0, 0],
      step: 4,
    });

    // directional hatching in the band inside the membrane, heaviest on the lower right
    const inner = scaleAbout(cell, CX, CY, (R - 150) / R);
    LIB.hatch(ctx, [cell, inner], {
      angle: -Math.PI / 4,
      spacing: 8,
      width: 1.6,
      color: P.cytoHatch,
      alpha: 1,
      length: [16, 52],
      gap: [3, 8],
      inset: 7,
      overshoot: 2,
      bend: 1.2,
      seed: sd('cytohatch'),
      density: (x, y) => 0.2 + 0.95 * sstep(-0.45, 0.85, ((x - CX) * 0.707 + (y - CY) * 0.707) / R),
    });
    // a second, tighter layer where the shade is deepest (art bible 4.1: cross layer at 105 degrees)
    const inner2 = scaleAbout(cell, CX, CY, (R - 96) / R);
    LIB.hatch(ctx, [cell, inner2], {
      angle: -Math.PI / 4 - Math.PI / 3,
      spacing: 7,
      width: 1.4,
      color: P.cytoHatch,
      alpha: 0.9,
      length: [10, 30],
      gap: [3, 7],
      inset: 5,
      seed: sd('cytocross'),
      density: (x, y) => sstep(0.2, 1, ((x - CX) * 0.707 + (y - CY) * 0.707) / R),
    });
    // the darkest wedge, hard against the membrane on the shadow side
    const inner3 = scaleAbout(cell, CX, CY, (R - 44) / R);
    LIB.hatch(ctx, [cell, inner3], {
      angle: -Math.PI / 4,
      spacing: 5,
      width: 1.3,
      color: P.cytoHatch,
      alpha: 0.9,
      length: [8, 22],
      gap: [2, 6],
      inset: 3,
      seed: sd('cytodeep'),
      density: (x, y) => sstep(0.55, 1.1, ((x - CX) * 0.707 + (y - CY) * 0.707) / R),
    });
  }

  // 45 degree diameters, the blocking square, and one dotted ghost circle per radius already left
  // behind: the pencil under-drawing the inked cell grew out of.
  function drawConstruction(ctx, t, f) {
    const cons = { width: 1.5, color: P.inkFaint, alpha: 0.3, taper: [0, 0], wobble: 2, tremble: 0.3, step: 6 };
    const d = 560;
    const k = Math.SQRT1_2 * d;
    LIB.inkPath(ctx, [[CX - k, CY - k], [CX + k, CY + k]], Object.assign({ seed: sd('diag', 0) }, cons));
    LIB.inkPath(ctx, [[CX - k, CY + k], [CX + k, CY - k]], Object.assign({ seed: sd('diag', 1) }, cons));

    // blocking square, half 460, with a small cross at each corner
    const s = 460;
    const sq = [[CX - s, CY - s], [CX + s, CY - s], [CX + s, CY + s], [CX - s, CY + s]];
    LIB.inkPath(ctx, sq, Object.assign({ closed: true, smooth: false }, cons, { alpha: 0.26, seed: sd('square') }));
    ctx.save();
    ctx.strokeStyle = P.inkFaint;
    ctx.globalAlpha *= 0.4;
    ctx.lineWidth = 1.3;
    ctx.lineCap = 'round';
    ctx.beginPath();
    for (const [qx, qy] of sq) {
      ctx.moveTo(qx - 13, qy);
      ctx.lineTo(qx + 13, qy);
      ctx.moveTo(qx, qy - 13);
      ctx.lineTo(qx, qy + 13);
    }
    // quadrant ticks on the square's edges
    for (const [ax, ay, bx, by] of [[CX, CY - s, 0, 1], [CX, CY + s, 0, -1], [CX - s, CY, 1, 0], [CX + s, CY, -1, 0]]) {
      ctx.moveTo(ax, ay);
      ctx.lineTo(ax + bx * 22, ay + by * 22);
    }
    ctx.stroke();
    ctx.restore();

    // ghost circles: after each beat the radius the membrane has just left stays as a dotted
    // trace, so the frame carries the whole history of the growth, not just its latest state
    ctx.save();
    ctx.strokeStyle = P.inkFaint;
    ctx.lineWidth = 1.6;
    ctx.lineCap = 'round';
    ctx.setLineDash([4, 9]);
    // RAD[0] is the overlay's job (the blue dotted outline), so the pencil starts at the next one
    for (let b = 1; b < BEAT.length; b++) {
      if (t < BEAT[b] - 1e-6) break;
      const fade = clamp((f - BEAT_F[b] + 1) / 3);
      ctx.globalAlpha = 0.46 * fade;
      const g = cellPts(RAD[b]);
      ctx.beginPath();
      LIB.tracePath(ctx, LIB.smoothPts(g, true, 10), true);
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawRibosomes(ctx, cell, nucleus, density) {
    // Ribosome stipple fills the cytoplasm; the nucleus is a hole in the even-odd clip. The
    // density drifts a little across the cell so the fill reads as living texture and not sand.
    const seed = sd('ribodrift');
    LIB.stipple(ctx, [cell, nucleus], {
      spacing: 7.5,
      r: [1, 2.2],
      density: (x, y) => density * (0.82 + 0.34 * (0.5 + 0.5 * LIB.noise2(x / 190, y / 190, seed))),
      color: P.ribosome,
      alpha: 0.68,
      jitter: 0.45,
      seed: sd('ribosome'),
    });
  }

  function drawNucleus(ctx, nuc, RN, k) {
    // fill and rim
    LIB.inkPath(ctx, nuc, {
      closed: true,
      width: 4,
      color: P.nucleusRim,
      fill: P.nucleus,
      seed: sd('nucrim'),
      wobble: 1.1,
      tremble: 0.3,
      taper: [12, 22],
      step: 3,
      double: { offset: 5, width: 0.3, alpha: 0.3, from: 0.12, to: 0.62 },
    });
    // cross-hatched shadow, kept to the outer lower right so the nucleus stays clean where the
    // chromosomes have to be counted
    LIB.crossHatch(ctx, nuc, {
      angle: -Math.PI / 4,
      spacing: 9,
      crossSpacing: 13,
      width: 1.2,
      color: P.nucleusDeep,
      alpha: 0.55,
      layers: 2,
      length: [10, 34],
      gap: [3, 8],
      inset: 6,
      clip: true,
      seed: sd('nuchatch'),
      density: (x, y) => sstep(0.3, 1.05, ((x - CX) * 0.707 + (y - CY) * 0.707) / RN),
    });
    // nuclear pores: short dashes straddling the membrane
    ctx.save();
    ctx.strokeStyle = P.nucleusRim;
    ctx.lineCap = 'round';
    ctx.lineWidth = 2.2;
    ctx.globalAlpha *= 0.75;
    ctx.beginPath();
    for (let i = 0; i < 26; i++) {
      const a = -Math.PI / 2 + (i / 26) * TAU + 0.06 * LIB.noise1(i * 0.8, sd('pore'));
      const rr = RN + 8 * NUC_N[Math.round((i / 26) * NUC_N.length) % NUC_N.length];
      const j = (LIB.h3(i, 3, sd('pore')) - 0.5) * 3;
      ctx.moveTo(CX + Math.cos(a) * (rr - 4 + j), CY + Math.sin(a) * (rr - 4 + j));
      ctx.lineTo(CX + Math.cos(a) * (rr + 4 + j), CY + Math.sin(a) * (rr + 4 + j));
    }
    ctx.stroke();
    ctx.restore();

    // nucleolus: a denser disc, carried outward as the nucleus grows
    const s = RN / NUCR[0];
    const ox = CX + NUCLEOLUS.dx * s, oy = CY + NUCLEOLUS.dy * s;
    const orad = NUCLEOLUS.r * s;
    const oPts = LIB.ellipsePts(ox, oy, orad * 1.06, orad * 0.94, 26, 0.3);
    LIB.inkPath(ctx, oPts, { closed: true, width: 2, color: P.nucleusRim, alpha: 0.85, fill: P.nucleusDeep, seed: sd('nucleolus'), wobble: 0.6, taper: [6, 12], step: 3 });
    LIB.stipple(ctx, LIB.ellipsePts(ox, oy, orad * 1.5, orad * 1.5, 24), {
      spacing: 6,
      r: [0.8, 1.5],
      density: (x, y) => 0.55 * (1 - sstep(orad * 0.85, orad * 1.5, Math.hypot(x - ox, y - oy))),
      color: P.nucleusDeep,
      alpha: 0.6,
      seed: sd('nucleolusstip'),
    });

    // the four chromosomes, on twos, never more and never fewer
    for (const ch of CHROMO) drawChromosome(ctx, ch, k);
  }

  function drawMembrane(ctx, cell) {
    LIB.inkPath(ctx, cell, {
      closed: true,
      width: 6,
      color: P.membrane,
      seed: sd('membrane'),
      wobble: 1.8,
      tremble: 0.4,
      taper: [16, 30],
      step: 3,
      double: { offset: 5, width: 0.26, alpha: 0.4, from: 0.14, to: 0.78 },
    });
    // a scatter of fine ticks along the membrane, the ink hand's tooth
    ctx.save();
    ctx.strokeStyle = P.inkSoft;
    ctx.globalAlpha *= 0.45;
    ctx.lineWidth = 1.4;
    ctx.lineCap = 'round';
    ctx.beginPath();
    for (let i = 0; i < 44; i++) {
      const u = i / 44;
      const idx = u * (cell.length - 1);
      const i0 = Math.floor(idx), i1 = (i0 + 1) % cell.length;
      const fr = idx - i0;
      const px = lerp(cell[i0][0], cell[i1][0], fr), py = lerp(cell[i0][1], cell[i1][1], fr);
      const a = Math.atan2(py - CY, px - CX);
      if (LIB.h3(i, 5, sd('tick')) < 0.45) continue;
      const l = 5 + 5 * LIB.h3(i, 7, sd('tick'));
      ctx.moveTo(px - Math.cos(a) * l, py - Math.sin(a) * l);
      ctx.lineTo(px + Math.cos(a) * l * 0.25, py + Math.sin(a) * l * 0.25);
    }
    ctx.stroke();
    ctx.restore();
  }

  // ===========================================================================
  // Overlays: screen space, full opacity, never hatched (art bible 6)
  // ===========================================================================

  function drawRuler(ctx) {
    ctx.save();
    ctx.strokeStyle = P.annBlue;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(RULER_X, RULER_Y0);
    ctx.lineTo(RULER_X, RULER_Y1);
    // ticks face out into the clean margin so the tick field never lands on the cell
    let i = 0;
    for (let y = RULER_Y0; y <= RULER_Y1 + 1e-6; y += 20, i++) {
      const long = i % 5 === 0;
      ctx.moveTo(RULER_X, y);
      ctx.lineTo(RULER_X + (long ? 28 : 12), y);
    }
    ctx.stroke();
    // end bars: the height the cell had when the shot opened
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(RULER_X - 12, RULER_Y0);
    ctx.lineTo(RULER_X + 30, RULER_Y0);
    ctx.moveTo(RULER_X - 12, RULER_Y1);
    ctx.lineTo(RULER_X + 30, RULER_Y1);
    ctx.stroke();
    ctx.restore();
  }

  // The membrane the shot opened on, kept as a dotted blue outline in screen space: the one mark
  // that makes the growth unarguable, because the ink membrane walks away from it beat by beat.
  const START_OUTLINE = LIB.smoothPts(cellPts(RAD[0]), true, 9);

  function drawStartOutline(ctx) {
    ctx.save();
    ctx.strokeStyle = P.annBlue;
    ctx.globalAlpha = 0.8;
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.setLineDash([9, 11]);
    ctx.beginPath();
    LIB.tracePath(ctx, START_OUTLINE, true);
    ctx.stroke();
    ctx.setLineDash([]);
    // four quadrant pips so the outline reads as a measurement, not a second membrane
    ctx.globalAlpha = 1;
    ctx.lineWidth = 3;
    ctx.beginPath();
    for (let q = 0; q < 4; q++) {
      const a = -Math.PI / 2 + (q * Math.PI) / 2;
      const c = Math.cos(a), s = Math.sin(a);
      ctx.moveTo(CX + c * (RAD[0] - 11), CY + s * (RAD[0] - 11));
      ctx.lineTo(CX + c * (RAD[0] + 11), CY + s * (RAD[0] + 11));
    }
    ctx.stroke();
    ctx.restore();
  }

  // a bar across the ruler for each radius the membrane has reached, pinned to the zoom it was
  // marked at so a mark never creeps once it is made, and a heavier run of ruler between the
  // current pair
  function drawRulerMarks(ctx, t, f, zAt) {
    ctx.save();
    ctx.strokeStyle = P.annBlue;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    for (let b = 0; b < BEAT.length; b++) {
      if (t < BEAT[b] - 1e-6) break;
      const pr = E.outExpo(clamp((f - BEAT_F[b] + 1) / 4));
      const zb = zAt(BEAT[b]);
      ctx.globalAlpha = 0.95 * pr;
      ctx.lineWidth = 3.5;
      for (const sgn of [-1, 1]) {
        const y = CY + sgn * RAD[b + 1] * zb;
        const w = 40 * pr;
        ctx.beginPath();
        ctx.moveTo(RULER_X - 6, y);
        ctx.lineTo(RULER_X + w, y);
        ctx.stroke();
      }
    }
    ctx.restore();
  }

  function drawBracket(ctx, R, z, f) {
    const y0 = CY - R * z, y1 = CY + R * z;
    ctx.save();
    ctx.strokeStyle = P.annBlue;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    // the height the cell started at, kept as a dotted pair so the stretch is legible
    ctx.globalAlpha = 0.45;
    ctx.lineWidth = 2;
    ctx.setLineDash([2, 7]);
    ctx.beginPath();
    ctx.moveTo(BRACKET_X - 18, RULER_Y0);
    ctx.lineTo(RULER_X, RULER_Y0);
    ctx.moveTo(BRACKET_X - 18, RULER_Y1);
    ctx.lineTo(RULER_X, RULER_Y1);
    ctx.stroke();
    ctx.setLineDash([]);
    // the bracket itself
    ctx.globalAlpha = 1;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(BRACKET_X - 16, y0);
    ctx.lineTo(BRACKET_X, y0);
    ctx.lineTo(BRACKET_X, y1);
    ctx.lineTo(BRACKET_X - 16, y1);
    ctx.moveTo(BRACKET_X, (y0 + y1) / 2);
    ctx.lineTo(BRACKET_X + 12, (y0 + y1) / 2);
    ctx.stroke();
    // arrow ticks at both ends, pointing out of the span
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (const [y, sgn] of [[y0, 1], [y1, -1]]) {
      ctx.moveTo(BRACKET_X - 7, y + sgn * 11);
      ctx.lineTo(BRACKET_X, y);
      ctx.lineTo(BRACKET_X + 7, y + sgn * 11);
    }
    ctx.stroke();
    // a hairline leader from each bracket end in toward the membrane it measures, stopping short
    // of the cell so it never lies across the drawing
    ctx.globalAlpha = 0.6;
    ctx.lineWidth = 1.5;
    ctx.setLineDash([2, 6]);
    ctx.beginPath();
    for (const y of [y0, y1]) {
      ctx.moveTo(BRACKET_X - 22, y);
      ctx.lineTo(CX + 40, y);
    }
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.restore();
    void f;
  }

  // the tally ring: one tick per new mitochondrion, with a bean glyph inside so the count needs
  // no words
  function drawTally(ctx, f) {
    const { x, y, r } = TALLY;
    ctx.save();
    ctx.strokeStyle = P.annYellow;
    ctx.fillStyle = P.annYellow;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, TAU);
    ctx.stroke();
    // six slots round the ring, clockwise from 12 o'clock
    for (const m of MITOS) {
      if (m.f < 0) continue;
      if (f < m.f) continue;
      const pr = E.outBack(clamp((f - m.f + 1) / 3));
      const a = -Math.PI / 2 + (m.tick / 6) * TAU;
      const l = 26 * pr;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(x + Math.cos(a) * (r + 6), y + Math.sin(a) * (r + 6));
      ctx.lineTo(x + Math.cos(a) * (r + 6 + l), y + Math.sin(a) * (r + 6 + l));
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(x + Math.cos(a) * (r + 6 + l), y + Math.sin(a) * (r + 6 + l), 2.6 * pr, 0, TAU);
      ctx.fill();
    }
    ctx.restore();

    // the thing being counted, drawn small at the ring's centre: no words needed
    const sp = bowedSpine(x, y, 46, -0.5, 5, 13);
    const shape = rodOutline(sp, 10, 2.4, 0.42);
    LIB.inkPath(ctx, shape, { closed: true, width: 2.6, color: P.ink, fill: P.mito, seed: sd('tallybean'), wobble: 0.4, taper: [6, 10], step: 3 });
    ctx.save();
    ctx.strokeStyle = P.mitoDeep;
    ctx.lineCap = 'round';
    ctx.lineWidth = 2.2;
    ctx.beginPath();
    for (let c = 0; c < 5; c++) {
      const u = (c + 1) / 6;
      const idx = u * (sp.length - 1);
      const i0 = Math.floor(idx), i1 = Math.min(sp.length - 1, i0 + 1);
      const fr = idx - i0;
      const px = lerp(sp[i0][0], sp[i1][0], fr), py = lerp(sp[i0][1], sp[i1][1], fr);
      const sgn = c % 2 ? 1 : -1;
      const hw = 10 * Math.pow(Math.max(0, 1 - Math.pow(Math.abs(2 * u - 1), 2.4)), 0.42);
      ctx.moveTo(px + Math.sin(-0.5) * (hw - 1) * sgn, py - Math.cos(-0.5) * (hw - 1) * sgn);
      ctx.lineTo(px - Math.sin(-0.5) * hw * 0.7 * sgn, py + Math.cos(-0.5) * hw * 0.7 * sgn);
    }
    ctx.stroke();
    ctx.restore();
  }

  // a small attention ring where each new mitochondrion lands
  function drawPops(ctx, f, z, toS) {
    ctx.save();
    ctx.strokeStyle = P.annYellow;
    ctx.lineCap = 'round';
    for (const m of MITOS) {
      if (m.f < 0) continue;
      const start = m.f + 4;
      const k = f - start;
      if (k < 0 || k > 9) continue;
      const pr = clamp((k + 1) / 7);
      const s = toS(m.x, m.y);
      const rr = (22 + 54 * E.outExpo(pr)) * z;
      ctx.globalAlpha = 1 - sstep(0.25, 1, pr);
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(s[0], s[1], rr, 0, TAU);
      ctx.stroke();
      if (k <= 1) {
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {
          const a = (i / 6) * TAU + 0.4;
          ctx.moveTo(s[0] + Math.cos(a) * (rr + 6), s[1] + Math.sin(a) * (rr + 6));
          ctx.lineTo(s[0] + Math.cos(a) * (rr + 16), s[1] + Math.sin(a) * (rr + 16));
        }
        ctx.stroke();
      }
    }
    ctx.restore();
  }

  // T 6.500: a yellow ring pulses out of the nucleus
  function drawPulse(ctx, f, z, RN, toS) {
    const start = BEAT_F[3];
    const k = f - start;
    if (k < 0) return;
    const c = toS(CX, CY);
    ctx.save();
    ctx.strokeStyle = P.annYellow;
    ctx.lineCap = 'round';
    for (const [delay, w] of [[0, 3.5], [5, 2]]) {
      const kk = k - delay;
      if (kk < 0 || kk > 15) continue;
      const pr = clamp((kk + 1) / 7);
      const rr = lerp(RN, 520, E.outExpo(pr)) * z;
      ctx.globalAlpha = (1 - sstep(0.35, 1.05, (kk + 1) / 15)) * (delay ? 0.6 : 1);
      ctx.lineWidth = w;
      ctx.beginPath();
      ctx.arc(c[0], c[1], rr, 0, TAU);
      ctx.stroke();
    }
    if (k <= 2) {
      ctx.globalAlpha = 1 - k / 3;
      ctx.lineWidth = 3;
      ctx.beginPath();
      for (let i = 0; i < 10; i++) {
        const a = (i / 10) * TAU + 0.21;
        const r0 = (RN + 26 + k * 34) * z, r1 = r0 + 26 * z;
        ctx.moveTo(c[0] + Math.cos(a) * r0, c[1] + Math.sin(a) * r0);
        ctx.lineTo(c[0] + Math.cos(a) * r1, c[1] + Math.sin(a) * r1);
      }
      ctx.stroke();
    }
    ctx.restore();
  }

  // ===========================================================================
  // Beat ramps
  // ===========================================================================

  // table[0] holds before the first beat; each beat moves to the next value over three drawings
  // with an outBack overshoot, so the change is visible ON the beat frame
  function steppedPop(t, table) {
    let v = table[0];
    for (let b = 0; b < BEAT.length; b++) {
      if (t < BEAT[b] - 1e-6) break;
      const d = Math.floor((t - BEAT[b]) * 12 + 1e-6);
      v = lerp(v, table[b + 1], d >= 2 ? 1 : POP3[d]);
    }
    return v;
  }

  // the same shape without the overshoot, for quantities that only ever rise
  function steppedRamp(t, table) {
    let v = table[0];
    for (let b = 0; b < BEAT.length; b++) {
      if (t < BEAT[b] - 1e-6) break;
      const d = Math.floor((t - BEAT[b]) * 12 + 1e-6);
      v = lerp(v, table[b + 1], clamp((d + 1) / 2));
    }
    return v;
  }

  // ===========================================================================
  // Scene
  // ===========================================================================

  FILM.scene({
    id: ID,
    draw(ctx, tIn, info) {
      const L = info.lib;
      const t = clamp(tIn, 0, DUR);
      const f = Math.min(LAST_F, Math.floor(t * 24 + 1e-6));
      const k = Math.floor(t * 12 + 1e-6); // drawing index: characters and organelles move on twos
      const tw = k / 12;

      // camera: a slow push that keeps world (540,900) on screen (540,900), so frame 0 lands
      // exactly on G1 and the match back out of the shot is clean
      const zAt = (tt) => 1 + 0.03 * E.inOutSine(clamp(tt / DUR));
      const z = zAt(t);
      const camY = CY + 60 / z;
      const toS = (x, y) => [540 + (x - 540) * z, CY + (y - CY) * z];

      // the pose for this frame: the membrane and the nucleus step on the beats, on twos
      const R = steppedPop(tw, RAD);
      const RN = steppedPop(tw, NUCR);
      const dens = steppedRamp(tw, STIP);

      const cellRaw = cellPts(R);
      const cell = L.smoothPts(cellRaw, true, 9);
      const nucRaw = nucPts(RN);
      const nuc = L.smoothPts(nucRaw, true, 8);

      // ------------------------------------------------------------ 1. stripes (screen)
      L.stripes(ctx, {
        colors: [P.stripeCream, P.stripeSage],
        width: 140,
        angle: -0.52,
        offset: 12 * info.T, // 6 px per beat along the normal
        seed: sd('stripes'),
      });

      // ------------------------------------------------------------ 2. the world
      L.camera(ctx, { x: 540, y: camY, zoom: z }, (c) => {
        // 2a. the tissue the cell sits in
        for (const nb of NEIGHS) drawNeighbour(c, nb);

        // 2b. the cell body and its tone
        drawCytoplasm(c, cell, R);

        // 2c. pencil under-drawing, showing through the cytoplasm
        drawConstruction(c, tw, f);

        // 2d. ribosomes: more of them every beat
        drawRibosomes(c, cell, nuc, dens);

        // 2e. mitochondria: six from G1, six drawing in two to a beat
        for (const m of MITOS) {
          const prog = m.f < 0 ? 1 : clamp((f - m.f + 1) / 4);
          drawMito(c, m, prog);
        }

        // 2f. nucleus, nucleolus, pores and the four chromosomes
        drawNucleus(c, nuc, RN, k);

        // 2g. the membrane last, over everything inside it
        drawMembrane(c, cell);
      });

      // ------------------------------------------------------------ 3. overlays (screen space)
      drawStartOutline(ctx);
      drawRuler(ctx);
      drawRulerMarks(ctx, tw, f, zAt);
      drawBracket(ctx, R, z, f);
      drawTally(ctx, f);
      drawPops(ctx, f, z, toS);
      drawPulse(ctx, f, z, RN, toS);

      // ------------------------------------------------------------ 4. the film's clock, always last
      L.cycleGlyph(ctx, info.T, 'illustrated');
    },
  });
})();
