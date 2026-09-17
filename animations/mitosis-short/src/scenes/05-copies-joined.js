// 05 copies-joined: Two identical copies, joined. Illustrated, global T 9.5 to 11.5 (2.0 s at 120 bpm).
//
// The match cut from 04 lands here: the four X chromosomes of G2 are on exactly the same pixels,
// now inked on paper inside the grown cell (membrane mean radius 440, nucleus mean radius 185).
// The camera is locked at zoom 1, so every number below is a frame pixel and nothing rides lib.camera.
//
// Layer plan (back to front):
//   1  paper plate, stripeCream / stripeApricot stripes (140 px, 30 deg, 6 px drift per beat),
//      a paperDeep 45 deg hatch vignette below the safe area (y 1540-1920)
//   2  neighbour cells on the G1 positions, cut by the frame edges, at 70 percent
//   3  construction in inkFaint: the frame axes, the cell's 45 degree diameters, a square round the
//      cell, guide circles r 440 and r 505, a 48-tick ring round the nucleus at r 205, level leaders
//      on the two chromosome rows (y 850 and y 955) with registration crosses
//   4  the cell's cast shadow: its outline offset +36, +28 and hatched at 45 degrees (light upper left)
//   5  cytoplasm fill, cytoHatch directional hatching near the membrane, ribosome stipple at 0.6
//   6  twelve mitochondria (the six of G1 plus the six that drew in during 03), beans with cristae
//   7  nucleus: fill, nucleusDeep cross-hatch on the lower right, nucleolus, nuclear membrane 4 px
//   8  the four X chromosomes on G2: two identical crossing rods, hatched at 30 degrees, an inkSoft
//      centromere disc at the crossing, a faint inkFaint centre line down each arm
//   9  the cell membrane, 6 px ink with a doubled stroke
//  10  overlays, screen-fixed: annMagenta centromere rings, the annYellow 'chromosome' bracket with
//      its two leaders onto chromoA1, the annBlue 'identical' arc joining A1's two arms,
//      annYellow tightening rings on the condense
//  11  the cycle glyph (lib.cycleGlyph), never re-implemented
//
// Timing, t is shot-local seconds (T = 9.5 + t), d = onTwos(t) * 12 is the drawing index:
//   t 0.000  T  9.500  the G2 pose exactly, screen-fixed; frame 0 is fully drawn
//   t 0.500  T 10.000  the four centromere rings pulse 14 -> 60 px over 4 frames, staggered 2 frames
//                      apart in the order A1, A2, B1, B2; the 'chromosome' bracket draws in over 4
//   t 1.000  T 10.500  the 'identical' arc draws from A1's left arm to its right arm over 6 frames;
//                      both of A1's arms glow chromoALight for 3 drawings
//   t 1.500  T 11.000  all four chromosomes condense: 6 percent shorter over 3 drawings with an
//                      overshoot, 8 percent thicker, hatching darker; four yellow rings tighten
//   t 1.708 on         held to the cut, so the hinge flash into 06 lands on a clean pose
//   throughout         the chromosomes wobble on twos (zero on drawing 0 so frame 0 is exact),
//                      the stripes drift, every ink line boils at 12 fps
(function () {
  'use strict';

  const ID = 'copies-joined';
  const LIB = FILM.lib;
  const TAU = Math.PI * 2;
  const DEG = Math.PI / 180;
  const FR = 1 / 24;

  // Shapes that survive a cut seed from the shot that owns them, so their wobble matches across it.
  const REF_CELL = 'hero-cell';           // G1: the cell, nucleus, mitochondria, neighbours
  const REF_G2 = 'dna-copy-blueprint';    // G2: the four X chromosomes

  const sd = (...k) => LIB.hash(ID, ...k) & 0x7fffffff;
  const sdCell = (...k) => LIB.hash(REF_CELL, ...k) & 0x7fffffff;
  const sdG2 = (...k) => LIB.hash(REF_G2, ...k) & 0x7fffffff;

  const lerp = (a, b, u) => a + (b - a) * u;
  const clamp = (v, lo = 0, hi = 1) => (v < lo ? lo : v > hi ? hi : v);
  const sstep = (a, b, x) => {
    const u = clamp((x - a) / (b - a));
    return u * u * (3 - 2 * u);
  };

  // ===========================================================================================
  // Shared geometry (docs/storyboard.md, "Shared geometry")
  // ===========================================================================================

  // G1, grown: the cell is an irregular near-circle centred (540, 900); 03 took the mean radius from
  // 380 to 440 and the nucleus from 170 to 185. The 40-point polyline and the 14 px wobble stay.
  // The amplitudes are the G1 wobble carried up with the growth and then pushed until the eye can
  // see it: a body cell is never a perfect circle (art bible 10.7).
  const CX = 540, CY = 900;
  const CELL_R = 440, CELL_AMP = 30, CELL_N = 40;
  const NUC_R = 185, NUC_AMP = 14, NUC_N = 36;

  // the nucleolus: a dense disc inside the nucleus, clear of all four chromosomes
  const NUCLEOLUS = [556, 1042, 21];

  // G2: each chromosome is two identical copies joined at the centromere, drawn as an X.
  // chromoA is 150 px tall with arms 40 px wide, chromoB 100 px tall; centres as in G1,
  // tilted 20 degrees alternately (the left member of each pair leans left, the right one right).
  //   h    half height          w    half width at the tips
  //   rod  half thickness       cen  centromere disc radius
  //   wf / wg: the two wobble frequencies, both giving zero on drawing 0 so frame 0 sits on G2
  const CHROMOS = [
    { key: 'A1', cx: 470, cy: 850, h: 75, w: 20, rod: 7.5, cen: 7.5, tilt: -20 * DEG, pair: 'A', wf: 0.55, wg: 0.37 },
    { key: 'A2', cx: 610, cy: 850, h: 75, w: 20, rod: 7.5, cen: 7.5, tilt: 20 * DEG, pair: 'A', wf: 0.47, wg: 0.29 },
    { key: 'B1', cx: 480, cy: 955, h: 50, w: 13.5, rod: 6.4, cen: 6.6, tilt: -20 * DEG, pair: 'B', wf: 0.63, wg: 0.44 },
    { key: 'B2', cx: 600, cy: 955, h: 50, w: 13.5, rod: 6.4, cen: 6.6, tilt: 20 * DEG, pair: 'B', wf: 0.41, wg: 0.52 },
  ];

  // G1 mitochondria, 60 by 28 px, plus the six that drew in across 03 (5.0, 5.5 and 6.0)
  const MITO = [
    [300, 700], [760, 720], [280, 1060], [790, 1080], [420, 1190], [660, 640],
    [360, 560], [720, 1240], [240, 900], [840, 900], [500, 1240], [620, 560],
  ];

  // G1 neighbours: partial circles cut by the frame edge, drawn in the same style at 70 percent
  const NEIGHBOURS = [
    [60, 380, 320], [1020, 420, 340], [40, 1420, 300], [1040, 1400, 360], [540, 1690, 330],
  ];

  // the annYellow bracket that carries the word 'chromosome', under chromoA1
  const BRK_Y = 1132, BRK_X0 = 296, BRK_X1 = 644;

  // beats, as shot-local seconds with the global time beside them
  const B_RING = 0.5;   // T 10.0  centromere rings pulse, the bracket draws in
  const B_ARC = 1.0;    // T 10.5  the 'identical' arc draws, A1's arms glow
  const B_COND = 1.5;   // T 11.0  the four chromosomes condense

  // ===========================================================================================
  // Geometry helpers
  // ===========================================================================================

  // A closed irregular near-circle: a periodic sum of four harmonics with seeded phases, weighted
  // toward the low orders so the outline swells in broad lobes rather than rippling. Periodic, so
  // the loop never shows a seam, and identical every time it is asked for.
  const BLOB_W = [1, 0.85, 0.6, 0.35];
  const BLOB_SUM = 2.8;
  function blobPts(cx, cy, r, amp, seed, n) {
    const pts = [];
    const ph = [];
    for (let k = 2; k <= 5; k++) ph.push(LIB.h3(k, 7, seed) * TAU);
    for (let i = 0; i < n; i++) {
      const a = (i / n) * TAU;
      let v = 0;
      for (let k = 2; k <= 5; k++) v += BLOB_W[k - 2] * Math.sin(k * a + ph[k - 2]);
      const rr = r + (amp * v) / BLOB_SUM;
      pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]);
    }
    return pts;
  }

  // the local radius of such a blob in a given direction, for the tone functions
  function blobRadius(a, r, amp, seed) {
    let v = 0;
    for (let k = 2; k <= 5; k++) v += BLOB_W[k - 2] * Math.sin(k * a + LIB.h3(k, 7, seed) * TAU);
    return r + (amp * v) / BLOB_SUM;
  }

  // unit normals along a polyline (open)
  function normals(cl) {
    const n = cl.length;
    const nx = new Float64Array(n), ny = new Float64Array(n);
    for (let i = 0; i < n; i++) {
      const a = Math.max(0, i - 1), b = Math.min(n - 1, i + 1);
      let tx = cl[b][0] - cl[a][0], ty = cl[b][1] - cl[a][1];
      const l = Math.hypot(tx, ty) || 1;
      tx /= l;
      ty /= l;
      nx[i] = -ty;
      ny[i] = tx;
    }
    return { nx, ny };
  }

  // A closed capsule round an open centreline: both offsets plus a semicircular cap at each end.
  function capsule(cl, hw, capN) {
    const { nx, ny } = normals(cl);
    const n = cl.length;
    const left = [], right = [];
    for (let i = 0; i < n; i++) {
      left.push([cl[i][0] + nx[i] * hw, cl[i][1] + ny[i] * hw]);
      right.push([cl[i][0] - nx[i] * hw, cl[i][1] - ny[i] * hw]);
    }
    const cap = (i, a0) => {
      const out = [];
      for (let k = 1; k < capN; k++) {
        const a = a0 - (k / capN) * Math.PI;
        out.push([cl[i][0] + Math.cos(a) * hw, cl[i][1] + Math.sin(a) * hw]);
      }
      return out;
    };
    const aEnd = Math.atan2(ny[n - 1], nx[n - 1]);
    const aStart = Math.atan2(ny[0], nx[0]) + Math.PI;
    return left.concat(cap(n - 1, aEnd), right.reverse(), cap(0, aStart));
  }

  // A mitochondrion: a bent bean, length by width, with rounded ends.
  function beanPts(len, wid, bend, n) {
    const top = [], bot = [];
    for (let i = 0; i <= n; i++) {
      const u = i / n;
      const x = lerp(-len / 2, len / 2, u);
      const y = -bend * Math.sin(Math.PI * u);
      const hw = (wid / 2) * Math.pow(Math.sin(Math.PI * u), 0.55);
      // the centreline's own tilt, so the caps sit square to it
      const dy = (-bend * Math.PI * Math.cos(Math.PI * u)) / (len / 2) / 2;
      const l = Math.hypot(1, dy) || 1;
      const nx = -dy / l, ny = 1 / l;
      top.push([x + nx * hw, y + ny * hw]);
      bot.push([x - nx * hw, y - ny * hw]);
    }
    return top.concat(bot.reverse());
  }

  // ===========================================================================================
  // Memoized, strictly time-independent geometry
  // ===========================================================================================

  let GEO = null;
  function geo() {
    if (GEO) return GEO;
    const cell = blobPts(CX, CY, CELL_R, CELL_AMP, sdCell('cell'), CELL_N);
    const cellSmooth = LIB.smoothPts(cell, true, 8);
    const nuc = blobPts(CX, CY, NUC_R, NUC_AMP, sdCell('nucleus'), NUC_N);
    const nucSmooth = LIB.smoothPts(nuc, true, 6);

    // the cast shadow: the membrane offset down-right, the outer rim only
    const shadow = cellSmooth.map(([x, y]) => [x + 36, y + 28]);

    // mitochondria: a seeded angle and a seeded bend each, all inside the grown cell
    const mitos = MITO.map(([x, y], i) => {
      const r = LIB.rng(sdCell('mito', i));
      const rot = r.range(-1.25, 1.25);
      const len = r.range(56, 64);
      const wid = r.range(25, 31);
      const bend = r.range(4, 9) * (r() < 0.5 ? -1 : 1);
      const pts = beanPts(len, wid, bend, 26);
      // cristae: shelves folding in from alternating sides
      const nC = 4 + Math.floor(r() * 3);
      const cristae = [];
      for (let k = 0; k < nC; k++) {
        const u = 0.16 + (0.68 * (k + 0.5)) / nC + r.range(-0.03, 0.03);
        const side = k % 2 ? 1 : -1;
        const xx = lerp(-len / 2, len / 2, u);
        const yy = -bend * Math.sin(Math.PI * u);
        const hw = (wid / 2) * Math.pow(Math.sin(Math.PI * u), 0.55);
        const reach = hw * r.range(1.25, 1.65);
        cristae.push([
          [xx, yy + side * hw * 0.94],
          [xx + r.range(-3, 3), yy + side * hw * 0.5],
          [xx + r.range(-5, 5), yy - side * (reach - hw)],
        ]);
      }
      return { x, y, rot, len, wid, pts, cristae, seed: sdCell('mitoDraw', i) };
    });

    // neighbours: the same cell, drawn as a ghost so the stripes keep running behind the field and
    // the hero stays the only solid form. Partial, cut by the frame edges.
    const nbrs = NEIGHBOURS.map(([x, y, r], i) => {
      const body = LIB.smoothPts(blobPts(x, y, r, 22, sdCell('nbr', i), 34), true, 10);
      const nr = r * 0.4;
      const nuc2 = LIB.smoothPts(blobPts(x + r * 0.08, y - r * 0.05, nr, 11, sdCell('nbrn', i), 26), true, 8);
      // a handful of the neighbour's own chromosomes, so no cell in the field looks empty
      const rr = LIB.rng(sdCell('nbrChr', i));
      const worms = [];
      for (let k = 0; k < 4; k++) {
        const a = rr() * TAU;
        const rad = Math.sqrt(rr()) * nr * 0.55;
        const cxk = x + r * 0.08 + Math.cos(a) * rad;
        const cyk = y - r * 0.05 + Math.sin(a) * rad;
        const len = nr * (k < 2 ? 0.55 : 0.36);
        const ang = 20 * DEG * (k % 2 ? 1 : -1);
        const co = Math.cos(ang), si = Math.sin(ang);
        const w = [];
        for (let q = 0; q <= 5; q++) {
          const u = q / 5 - 0.5;
          const lx = u * len;
          const ly = Math.sin(u * Math.PI * 1.6) * len * 0.12;
          w.push([cxk + lx * co - ly * si, cyk + lx * si + ly * co]);
        }
        worms.push({ pts: w, pair: k < 2 ? 'A' : 'B' });
      }
      return { x, y, r, body, nuc: nuc2, worms, seed: sdCell('nbrDraw', i) };
    });

    // a nucleolus outline, drawn once
    const nucleolus = LIB.smoothPts(blobPts(NUCLEOLUS[0], NUCLEOLUS[1], NUCLEOLUS[2], 3, sdCell('nucleolus'), 20), true, 4);

    const sCell = sdCell('cell'), sNuc = sdCell('nucleus');
    GEO = {
      cell, cellSmooth, nuc, nucSmooth, shadow, mitos, nbrs, nucleolus,
      cellBounds: LIB.bounds(cellSmooth),
      nucBounds: LIB.bounds(nucSmooth),
      arms: new Map(),
      // 0 at the centre, 1 on the membrane, following the real irregular outline
      rCell: (x, y) => {
        const dx = x - CX, dy = y - CY;
        return Math.hypot(dx, dy) / blobRadius(Math.atan2(dy, dx), CELL_R, CELL_AMP, sCell);
      },
      rNuc: (x, y) => {
        const dx = x - CX, dy = y - CY;
        return Math.hypot(dx, dy) / blobRadius(Math.atan2(dy, dx), NUC_R, NUC_AMP, sNuc);
      },
    };
    return GEO;
  }

  // how far a point lies toward the shadow, -1 fully lit (upper left) to 1 fully shadowed
  const litness = (x, y, cx, cy, r) => ((x - cx) * 0.7071 + (y - cy) * 0.7071) / r;

  // ---------------------------------------------------------------------------
  // One arm (one chromatid) of an X, in the chromosome's own local frame.
  // Arm 1 runs from the upper left tip through the centromere to the lower right tip; arm 2 is its
  // mirror. The pair is built from one centreline so the two are the same length, the same
  // thickness and the same shape: the copies are identical (art bible 10.2).
  // ---------------------------------------------------------------------------

  function armGeom(h, w, rod) {
    const key = `${Math.round(h * 100)}|${Math.round(w * 100)}|${Math.round(rod * 100)}`;
    const G = geo();
    let A = G.arms.get(key);
    if (A) return A;
    const N = 26;
    const cl = [];
    for (let i = 0; i <= N; i++) {
      const v = (i / N) * 2 - 1;              // -1 at the top tip, +1 at the bottom tip
      const s = v < 0 ? -1 : 1;
      // the arms pinch at the centromere and flare toward the tips
      const x = w * s * Math.pow(Math.abs(v), 1.15);
      cl.push([x, h * v]);
    }
    const poly = capsule(cl, rod, 9);
    // the arm's straight axis through the origin, for the shadow-side density
    const ax = cl[N][0] - cl[0][0], ay = cl[N][1] - cl[0][1];
    const al = Math.hypot(ax, ay) || 1;
    A = { cl, poly, ux: ax / al, uy: ay / al, mx: -ay / al, my: ax / al, rod, h, w };
    G.arms.set(key, A);
    return A;
  }

  const mirrorX = (pts) => pts.map(([x, y]) => [-x, y]);

  // ===========================================================================================
  // Background
  // ===========================================================================================

  function drawBackground(ctx, L, P, T) {
    L.paper(ctx, { seed: 5 });
    ctx.save();
    ctx.globalAlpha = 0.87;
    L.stripes(ctx, {
      colors: [P.stripeCream, P.stripeApricot],
      width: 140,
      angle: -0.52,
      offset: 12 * T,     // 6 px per beat at 120 bpm
      seed: 505,
    });
    ctx.restore();
    // below the safe area the plate darkens, so the cell sits on the page rather than floating
    L.hatch(ctx, [[-40, 1520], [1120, 1520], [1120, 1960], [-40, 1960]], {
      angle: -Math.PI / 4,
      spacing: 8,
      width: 1.7,
      color: P.paperDeep,
      alpha: 0.24,
      length: [18, 62],
      gap: [3, 10],
      seed: sd('vignette'),
      density: (x, y) => sstep(1545, 1870, y),
    });
    // and a narrow band of the same at the very top, above the safe area
    L.hatch(ctx, [[-40, -40], [1120, -40], [1120, 230], [-40, 230]], {
      angle: -Math.PI / 4,
      spacing: 9,
      width: 1.6,
      color: P.paperDeep,
      alpha: 0.18,
      length: [14, 48],
      gap: [3, 10],
      seed: sd('vignetteTop'),
      density: (x, y) => 1 - sstep(60, 214, y),
    });
  }

  // ===========================================================================================
  // Neighbour cells: the tissue the hero cell sits in, cut by the frame edges
  // ===========================================================================================

  function drawNeighbours(ctx, L, P) {
    const G = geo();
    ctx.save();
    ctx.globalAlpha = 0.7;
    for (const nb of G.nbrs) {
      // no flat fill: the stripes must keep running behind the whole field, so a neighbour is a
      // thin membrane, a pale nucleus and a whisper of tone near its shaded edge
      ctx.save();
      ctx.globalAlpha = 0.34;
      ctx.beginPath();
      L.tracePath(ctx, nb.body, true);
      ctx.fillStyle = P.neighbour;
      ctx.fill();
      ctx.restore();
      L.hatch(ctx, nb.body, {
        angle: -Math.PI / 4,
        spacing: 13,
        width: 1.3,
        color: P.cytoHatch,
        alpha: 0.42,
        length: [16, 52],
        gap: [4, 12],
        seed: nb.seed + 1,
        density: (x, y) => sstep(0.25, 1.0, litness(x, y, nb.x, nb.y, nb.r)),
      });
      // the neighbour's own nucleus, and four chromosomes inside it so no cell reads as empty
      ctx.save();
      ctx.globalAlpha = 0.5;
      L.inkPath(ctx, nb.nuc, {
        closed: true,
        width: 2.2,
        color: P.inkSoft,
        alpha: 0.75,
        fill: P.neighbourNucleus,
        seed: nb.seed + 2,
        wobble: 1.1,
      });
      for (let k = 0; k < nb.worms.length; k++) {
        const w = nb.worms[k];
        L.inkPath(ctx, w.pts, {
          width: nb.r * (w.pair === 'A' ? 0.05 : 0.043),
          color: w.pair === 'A' ? P.chromoA : P.chromoB,
          alpha: 0.7,
          seed: nb.seed + 20 + k,
          taper: [6, 8],
          wobble: 0.8,
          swell: 0,
        });
      }
      ctx.restore();
      L.inkPath(ctx, nb.body, {
        closed: true,
        width: 3.2,
        color: P.inkSoft,
        alpha: 0.72,
        seed: nb.seed + 3,
        wobble: 1.5,
      });
    }
    ctx.restore();
  }

  // ===========================================================================================
  // Construction: the technical-drawing scaffold in inkFaint, behind the cell
  // ===========================================================================================

  function line(p, x0, y0, x1, y1) {
    p.moveTo(x0, y0);
    p.lineTo(x1, y1);
  }

  function drawConstruction(ctx, L, P) {
    const faint = new Path2D();    // 30 percent
    const mid = new Path2D();      // 45 percent, the pieces that must read

    // the frame's axes through the cell's centre, running past the edges
    line(faint, CX, -40, CX, 1960);
    line(faint, -40, CY, 1120, CY);
    // the 45 degree diameters, out past the membrane
    for (const s of [-1, 1]) {
      const c = Math.SQRT1_2;
      line(faint, CX - c * 560, CY - s * c * 560, CX + c * 560, CY + s * c * 560);
    }
    // a faint square round the cell, its corners on the 45 degree rays
    const q = CELL_R + 12;
    faint.moveTo(CX - q, CY - q);
    faint.lineTo(CX + q, CY - q);
    faint.lineTo(CX + q, CY + q);
    faint.lineTo(CX - q, CY + q);
    faint.closePath();
    // corner ticks on the square
    for (const sx of [-1, 1]) {
      for (const sy of [-1, 1]) {
        line(mid, CX + sx * q, CY + sy * (q - 22), CX + sx * q, CY + sy * (q + 22));
        line(mid, CX + sx * (q - 22), CY + sy * q, CX + sx * (q + 22), CY + sy * q);
      }
    }
    ctx.save();
    ctx.strokeStyle = P.inkFaint;
    ctx.lineCap = 'round';
    ctx.lineWidth = 1.5;
    ctx.globalAlpha = 0.3;
    ctx.stroke(faint);
    ctx.globalAlpha = 0.45;
    ctx.stroke(mid);
    ctx.restore();

    // guide circles on the mean membrane and just outside it
    L.guideCircle(ctx, CX, CY, CELL_R, { color: P.inkFaint, alpha: 0.3, width: 1.5, dash: [3, 8] });
    L.guideCircle(ctx, CX, CY, CELL_R + 65, { color: P.inkFaint, alpha: 0.22, width: 1.5 });
    L.guideCircle(ctx, CX, CY, NUC_R + 20, { color: P.inkFaint, alpha: 0.3, width: 1.5, dash: [2, 8] });

    // a 48-tick ring round the nucleus, every eighth long
    L.ticks(ctx, CX, CY, {
      r: NUC_R + 20,
      n: 48,
      len: 8,
      major: 8,
      majorLen: 17,
      color: P.inkFaint,
      alpha: 0.42,
      width: 1.5,
    });
    // and a coarser one on the membrane circle, over the top half only
    L.ticks(ctx, CX, CY, {
      r: CELL_R,
      n: 36,
      len: 9,
      major: 3,
      majorLen: 18,
      start: Math.PI,
      span: Math.PI,
      color: P.inkFaint,
      alpha: 0.35,
      width: 1.5,
    });

    // level leaders on the two chromosome rows, broken where the nucleus stands
    const rows = new Path2D();
    for (const y of [850, 955]) {
      const half = Math.sqrt(Math.max(0, (CELL_R - 10) * (CELL_R - 10) - (y - CY) * (y - CY)));
      const gap = Math.sqrt(Math.max(0, (NUC_R + 32) * (NUC_R + 32) - (y - CY) * (y - CY)));
      line(rows, CX - half, y, CX - gap, y);
      line(rows, CX + gap, y, CX + half, y);
      for (const s of [-1, 1]) {
        line(rows, CX + s * half, y - 9, CX + s * half, y + 9);
        for (let k = 1; k < 5; k++) {
          const x = CX + s * lerp(gap, half, k / 5);
          line(rows, x, y - 5, x, y + 5);
        }
      }
    }
    // registration crosses on the four G2 centres, so the geometry shows even under the ink
    for (const c of CHROMOS) {
      line(rows, c.cx - 11, c.cy, c.cx + 11, c.cy);
      line(rows, c.cx, c.cy - 11, c.cx, c.cy + 11);
    }
    ctx.save();
    ctx.strokeStyle = P.inkFaint;
    ctx.lineCap = 'round';
    ctx.lineWidth = 1.5;
    ctx.globalAlpha = 0.45;
    ctx.stroke(rows);
    ctx.restore();
  }

  // ===========================================================================================
  // The cell: shadow, cytoplasm, mitochondria, nucleus, membrane
  // ===========================================================================================

  function drawCellShadow(ctx, L, P) {
    const G = geo();
    L.hatch(ctx, G.shadow, {
      angle: -Math.PI / 4,
      spacing: 6,
      width: 1.5,
      color: P.inkFaint,
      alpha: 0.45,
      length: [14, 46],
      gap: [2, 7],
      seed: sd('cellShadow'),
      density: (x, y) => {
        const r = G.rCell(x - 36, y - 28);
        return (1 - sstep(0.9, 1.03, r)) * sstep(-0.1, 0.25, litness(x - 36, y - 28, CX, CY, CELL_R));
      },
    });
  }

  function drawCytoplasm(ctx, L, P) {
    const G = geo();
    // flat fill inside the membrane
    ctx.save();
    ctx.beginPath();
    L.tracePath(ctx, G.cellSmooth, true);
    ctx.fillStyle = P.cytoplasm;
    ctx.fill();
    ctx.restore();

    // Directional hatching in the cytoplasm near the membrane. The light is upper left, so the
    // upper-left third of the cytoplasm is left flat and the tone builds round to the lower right.
    const ring = [G.cellSmooth, G.nucSmooth];
    L.hatch(ctx, ring, {
      angle: -Math.PI / 4,
      spacing: 9,
      width: 1.6,
      color: P.cytoHatch,
      alpha: 0.95,
      length: [18, 62],
      gap: [3, 10],
      inset: 5,
      overshoot: 2,
      seed: sd('cytoA'),
      density: (x, y) => {
        const r = G.rCell(x, y);
        const lit = sstep(-0.32, 0.7, litness(x, y, CX, CY, CELL_R));
        return sstep(0.46, 0.98, r) * lit;
      },
    });
    // a second layer at 105 degrees where the plate is furthest from the light
    L.hatch(ctx, ring, {
      angle: -105 * DEG,
      spacing: 11,
      width: 1.4,
      color: P.cytoHatch,
      alpha: 0.8,
      length: [16, 48],
      gap: [4, 12],
      inset: 5,
      seed: sd('cytoB'),
      density: (x, y) => {
        const r = G.rCell(x, y);
        return sstep(0.55, 1.0, r) * sstep(0.3, 0.92, litness(x, y, CX, CY, CELL_R));
      },
    });
    // and a short third layer right against the shaded membrane, the deepest tone in the cell
    L.hatch(ctx, ring, {
      angle: -Math.PI / 4,
      spacing: 6,
      width: 1.3,
      color: P.inkFaint,
      alpha: 0.4,
      length: [10, 30],
      gap: [3, 9],
      inset: 3,
      seed: sd('cytoC'),
      density: (x, y) => {
        const r = G.rCell(x, y);
        return sstep(0.83, 1.0, r) * sstep(0.45, 0.95, litness(x, y, CX, CY, CELL_R));
      },
    });

    // ribosomes: fine stipple through the cytoplasm, density 0.6 after the growth of 03, a little
    // thicker out toward the membrane where the rough endoplasmic reticulum sits
    L.stipple(ctx, ring, {
      spacing: 8.5,
      r: [0.9, 1.9],
      color: P.ribosome,
      alpha: 0.6,
      seed: sd('ribosome'),
      density: (x, y) => {
        const r = G.rCell(x, y);
        // drifting clumps rather than an even sand, so the cytoplasm reads as tissue
        const n = L.fbm2(x * 0.0075, y * 0.0075, sd('ribNoise'), 3);
        return clamp(0.38 + 0.3 * sstep(0.3, 1, r) + 0.34 * n);
      },
    });
  }

  function drawMitochondria(ctx, L, P) {
    const G = geo();
    for (let i = 0; i < G.mitos.length; i++) {
      const m = G.mitos[i];
      ctx.save();
      ctx.translate(m.x, m.y);
      ctx.rotate(m.rot);
      // body
      L.inkPath(ctx, m.pts, {
        closed: true,
        width: 3,
        color: P.ink,
        fill: P.mito,
        seed: m.seed,
        wobble: 0.9,
      });
      // cristae, folding in from alternating sides
      for (let k = 0; k < m.cristae.length; k++) {
        L.inkPath(ctx, m.cristae[k], {
          width: 2,
          color: P.mitoDeep,
          alpha: 0.95,
          seed: m.seed + 10 + k,
          taper: [3, 9],
          wobble: 0.5,
          swell: 0,
        });
      }
      // tone on the side away from the light; the light stays upper-left in frame space,
      // so it turns with the bean
      const lx = Math.cos(-m.rot) - Math.sin(-m.rot);
      const ly = -Math.sin(-m.rot) + Math.cos(-m.rot);
      const ll = Math.hypot(lx, ly) || 1;
      L.hatch(ctx, m.pts, {
        angle: -Math.PI / 4 - m.rot,
        spacing: 5,
        width: 1.2,
        color: P.mitoDeep,
        alpha: 0.75,
        length: [6, 18],
        gap: [2, 5],
        inset: 1,
        overshoot: 1,
        clip: true,
        seed: m.seed + 40,
        density: (x, y) => clamp(((x * lx) / ll + (y * ly) / ll) / (m.wid * 0.5) + 0.12),
      });
      // a white catchlight along the lit edge
      const hi = [];
      for (let k = 0; k <= 6; k++) {
        const u = 0.2 + 0.6 * (k / 6);
        const xx = lerp(-m.len / 2, m.len / 2, u);
        const hw = (m.wid / 2) * Math.pow(Math.sin(Math.PI * u), 0.55);
        hi.push([xx - (lx / ll) * hw * 0.55, -0 - (ly / ll) * hw * 0.55]);
      }
      L.inkPath(ctx, hi, {
        width: 1.8,
        color: P.white,
        alpha: 0.5,
        seed: m.seed + 70,
        taper: [8, 12],
        wobble: 0.4,
        swell: 0,
      });
      ctx.restore();
    }
  }

  function drawNucleus(ctx, L, P) {
    const G = geo();
    // the nucleus casts its own shadow into the cytoplasm, down and right of it, so it sits in the
    // cell rather than on top of it
    const cast = G.nucSmooth.map(([x, y]) => [x + 17, y + 13]);
    L.hatch(ctx, cast, {
      angle: -Math.PI / 4,
      spacing: 5.5,
      width: 1.3,
      color: P.inkFaint,
      alpha: 0.42,
      length: [8, 26],
      gap: [2, 6],
      seed: sd('nucCast'),
      density: (x, y) => {
        const r = G.rNuc(x - 17, y - 13);
        return (1 - sstep(0.88, 1.03, r)) * sstep(0.1, 0.55, litness(x - 17, y - 13, CX, CY, NUC_R));
      },
    });
    // fill
    ctx.save();
    ctx.beginPath();
    L.tracePath(ctx, G.nucSmooth, true);
    ctx.fillStyle = P.nucleus;
    ctx.fill();
    ctx.restore();

    // cross-hatch shadow: light from the upper left, so the tone falls to the lower right
    L.crossHatch(ctx, G.nucSmooth, {
      angle: -Math.PI / 4,
      spacing: 9,
      crossSpacing: 13,
      layers: 2,
      width: 1.3,
      color: P.nucleusDeep,
      alpha: 0.52,
      length: [12, 40],
      gap: [3, 8],
      inset: 4,
      overshoot: 2,
      seed: sd('nucTone'),
      density: (x, y) => {
        const d = litness(x, y, CX, CY, NUC_R);
        const r = G.rNuc(x, y);
        return sstep(-0.05, 0.9, d) * (0.45 + 0.55 * sstep(0.3, 1, r));
      },
    });

    // the nucleolus: a denser disc, stippled, with its own soft tone
    L.inkPath(ctx, G.nucleolus, {
      closed: true,
      width: 2.2,
      color: P.nucleusRim,
      alpha: 0.85,
      fill: P.nucleusDeep,
      seed: sdCell('nucleolusInk'),
      wobble: 0.7,
    });
    L.stipple(ctx, G.nucleolus, {
      spacing: 5,
      r: [0.9, 1.6],
      color: P.nucleusRim,
      alpha: 0.45,
      density: 0.55,
      seed: sd('nucleolusDots'),
    });

    // the nuclear membrane, 4 px inkSoft with a quiet second pen line
    L.inkPath(ctx, G.nucSmooth, {
      closed: true,
      width: 4,
      color: P.nucleusRim,
      seed: sdCell('nucRim'),
      wobble: 1.2,
      double: { offset: 3.5, alpha: 0.32, width: 0.34, from: 0.12, to: 0.55 },
    });
  }

  function drawMembrane(ctx, L, P) {
    const G = geo();
    L.inkPath(ctx, G.cellSmooth, {
      closed: true,
      width: 6,
      color: P.membrane,
      seed: sdCell('membrane'),
      wobble: 1.7,
      double: { offset: 4.5, alpha: 0.38, width: 0.28, from: 0.1, to: 0.48 },
    });
  }

  // ===========================================================================================
  // The chromosomes
  // ===========================================================================================

  // The live pose of one chromosome: its centre, its rotation, how far it has condensed.
  function poseOf(c, d, cond) {
    // the wobble is a sine of the drawing index, so it is exactly zero on drawing 0 and the
    // frame that 04 cuts onto sits on the G2 numbers to the pixel
    const rot = c.tilt + 1.7 * DEG * Math.sin(d * c.wf);
    const dx = 1.5 * Math.sin(d * c.wg);
    const dy = 1.3 * Math.sin(d * c.wf * 0.83);
    return {
      cx: c.cx + dx,
      cy: c.cy + dy,
      rot,
      // condensing: 6 percent shorter, 8 percent thicker, darker
      h: c.h * cond.s,
      w: c.w * cond.s,
      rod: c.rod * cond.s * cond.thick,
      cen: c.cen * cond.s * cond.thick,
      tone: cond.tone,
    };
  }

  // the four tips of an X in frame coordinates: [topLeft, topRight, bottomLeft, bottomRight]
  function tipsOf(p) {
    const co = Math.cos(p.rot), si = Math.sin(p.rot);
    const at = (x, y) => [p.cx + x * co - y * si, p.cy + x * si + y * co];
    return [at(-p.w, -p.h), at(p.w, -p.h), at(-p.w, p.h), at(p.w, p.h)];
  }

  function drawChromosome(ctx, L, P, c, p, glow) {
    const A = armGeom(p.h, p.w, p.rod);
    const base = c.pair === 'A' ? P.chromoA : P.chromoB;
    const deep = c.pair === 'A' ? P.chromoADeep : P.chromoBDeep;
    const light = c.pair === 'A' ? P.chromoALight : P.chromoBLight;
    const fill = glow ? light : base;
    const seed = sdG2('chromo', c.key);

    // the light direction in the chromosome's own frame
    const lx = Math.cos(-p.rot) - Math.sin(-p.rot);
    const ly = -Math.sin(-p.rot) + Math.cos(-p.rot);
    const ll = Math.hypot(lx, ly) || 1;

    ctx.save();
    ctx.translate(p.cx, p.cy);
    ctx.rotate(p.rot);

    // Both arms come from one centreline, so they are the same length and the same thickness.
    // Arm 2 is arm 1 mirrored in x: the two copies of the chromosome, identical.
    const arms = [
      { poly: A.poly, cl: A.cl, mx: A.mx, my: A.my, s: 1 },
      { poly: mirrorX(A.poly), cl: mirrorX(A.cl), mx: -A.mx, my: A.my, s: -1 },
    ];

    // A clear margin of nucleoplasm round the whole X, so each chromosome reads as its own body
    // where chromoA1 and chromoB1 all but touch. The tone of the nucleus stops at the form,
    // which is what a hand would do.
    ctx.save();
    ctx.strokeStyle = P.nucleus;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.lineWidth = 9.5;
    for (const poly of [A.poly, mirrorX(A.poly)]) {
      ctx.beginPath();
      L.tracePath(ctx, poly, true);
      ctx.stroke();
    }
    ctx.fillStyle = P.nucleus;
    ctx.beginPath();
    ctx.arc(0, 0, p.cen + 5, 0, TAU);
    ctx.fill();
    ctx.restore();

    // order: the arm that leans away from the light goes down first, so the crossing reads
    const order = lx >= 0 ? [1, 0] : [0, 1];
    for (const ai of order) {
      const arm = arms[ai];
      // which side of this arm is in shadow
      const sgn = arm.mx * (lx / ll) + arm.my * (ly / ll) >= 0 ? 1 : -1;

      L.inkPath(ctx, arm.poly, {
        closed: true,
        width: 3,
        color: P.ink,
        fill,
        seed: seed + 11,
        wobble: 0.85,
        step: 3,
      });
      // hatching at 30 degrees, on the shadow side of the rod only
      L.hatch(ctx, arm.poly, {
        angle: -Math.PI / 6 - p.rot,
        spacing: p.tone > 0.5 ? 4.6 : 5.6,
        width: 1.25,
        color: deep,
        alpha: 0.82,
        length: [6, 20],
        gap: [2, 5],
        inset: 1,
        overshoot: 1,
        clip: true,
        seed: seed + 21 + ai,
        density: (x, y) => clamp(((x * arm.mx + y * arm.my) * sgn) / p.rod + 0.05),
      });
      // a 105 degree cross layer once the chromosome has condensed
      if (p.tone > 0.5) {
        L.hatch(ctx, arm.poly, {
          angle: -105 * DEG - p.rot,
          spacing: 6.5,
          width: 1.15,
          color: deep,
          alpha: 0.6,
          length: [5, 16],
          gap: [2, 5],
          inset: 1,
          clip: true,
          seed: seed + 41 + ai,
          density: (x, y) => clamp(((x * arm.mx + y * arm.my) * sgn) / p.rod - 0.35),
        });
      }
      // the faint centre line down the arm
      L.inkPath(ctx, arm.cl, {
        width: 1.4,
        color: P.inkFaint,
        alpha: 0.42,
        seed: seed + 61 + ai,
        taper: [10, 14],
        wobble: 0.5,
        swell: 0,
      });
      // and a white catchlight just inside the lit edge
      const hi = [];
      for (let k = 2; k < arm.cl.length - 2; k++) {
        hi.push([
          arm.cl[k][0] - arm.mx * sgn * p.rod * 0.52,
          arm.cl[k][1] - arm.my * sgn * p.rod * 0.52,
        ]);
      }
      L.inkPath(ctx, hi, {
        width: 1.5,
        color: P.white,
        alpha: 0.4,
        seed: seed + 81 + ai,
        taper: [14, 18],
        wobble: 0.4,
        swell: 0,
      });
    }

    // the centromere: an inkSoft disc where the two arms cross
    L.inkPath(ctx, L.ellipsePts(0, 0, p.cen, p.cen, 20), {
      closed: true,
      width: 2.2,
      color: P.ink,
      fill: P.centromere,
      seed: seed + 101,
      wobble: 0.35,
    });
    ctx.save();
    ctx.fillStyle = P.white;
    ctx.globalAlpha = 0.5;
    ctx.beginPath();
    ctx.arc(-p.cen * 0.32, -p.cen * 0.34, p.cen * 0.26, 0, TAU);
    ctx.fill();
    ctx.restore();

    ctx.restore();
  }

  // the chromosomes' own cast shadow on the nucleoplasm, one hatch pass for all eight arms
  function drawChromoShadow(ctx, L, P, poses) {
    const path = new Path2D();
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (let i = 0; i < CHROMOS.length; i++) {
      const p = poses[i];
      const A = armGeom(p.h, p.w, p.rod);
      const co = Math.cos(p.rot), si = Math.sin(p.rot);
      for (const poly of [A.poly, mirrorX(A.poly)]) {
        poly.forEach(([x, y], k) => {
          const X = p.cx + x * co - y * si + 11;
          const Y = p.cy + x * si + y * co + 9;
          if (k === 0) path.moveTo(X, Y);
          else path.lineTo(X, Y);
          if (X < x0) x0 = X;
          if (X > x1) x1 = X;
          if (Y < y0) y0 = Y;
          if (Y > y1) y1 = Y;
        });
        path.closePath();
      }
    }
    const G = geo();
    ctx.save();
    ctx.beginPath();
    L.tracePath(ctx, G.nucSmooth, true);
    ctx.clip();
    L.hatch(ctx, path, {
      angle: -Math.PI / 4,
      spacing: 5.5,
      width: 1.3,
      color: P.nucleusDeep,
      alpha: 0.62,
      length: [8, 26],
      gap: [2, 6],
      seed: sd('chromoShadow'),
      bounds: { x: x0 - 8, y: y0 - 8, w: x1 - x0 + 16, h: y1 - y0 + 16 },
    });
    ctx.restore();
  }

  // ===========================================================================================
  // Overlays: screen-fixed, full opacity, never hatched or grained (art bible 6)
  // ===========================================================================================

  // annMagenta rings bursting from each centromere on the beat, staggered 2 frames apart
  function drawCentromereRings(ctx, L, P, t, poses) {
    const E = L.ease;
    ctx.save();
    ctx.strokeStyle = P.annMagenta;
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    for (let i = 0; i < CHROMOS.length; i++) {
      const start = B_RING + (i * 2) / 24;
      if (t < start - 1e-9) continue;
      const age = (t - start) * 24;
      if (age >= 9) continue;
      const p = poses[i];
      const r = lerp(14, 60, E.outExpo((age + 1) / 4));
      const a = 1 - Math.pow(clamp(age / 9), 1.5);
      if (a <= 0) continue;
      ctx.globalAlpha = a;
      ctx.beginPath();
      ctx.arc(p.cx, p.cy, r, 0, TAU);
      ctx.stroke();
      // a second, tighter ring snapping in behind it, for the first three frames
      if (age < 3) {
        ctx.globalAlpha = a * 0.8;
        ctx.beginPath();
        ctx.arc(p.cx, p.cy, lerp(46, 20, E.outExpo((age + 1) / 3)), 0, TAU);
        ctx.stroke();
      }
    }
    ctx.restore();
  }

  // The annYellow bracket that names the chromosome: a square bracket opening upward, sitting under
  // chromoA1's column. One dashed leader climbs to A1's centromere. It runs up at x 425, which is
  // the lane between the nucleus wall and chromoB1's left tip, then turns in over the last 70 px,
  // so it reaches A1 without ever lying across another chromosome.
  const LEAD_X = 425, LEAD_TURN = 905, LEAD_STOP = 17;

  function drawBracket(ctx, L, P, pOn, poses) {
    if (pOn <= 0) return;
    const p = poses[0];                              // chromoA1
    L.bracket(ctx, BRK_X0, BRK_Y, BRK_X1, BRK_Y, {
      color: P.annYellow,
      alpha: 1,
      width: 2.5,
      cap: 20,
      style: 'square',
      label: 'chromosome',
      labelSize: 34,
      p: pOn,
    });
    const grow = clamp((pOn - 0.25) / 0.75);
    if (grow <= 0) return;

    const y0 = BRK_Y - 14;
    const turn = Math.min(LEAD_TURN, p.cy + 55);
    let dx = p.cx - LEAD_X, dy = p.cy - turn;
    const dl = Math.hypot(dx, dy) || 1;
    dx /= dl;
    dy /= dl;
    const tip = [p.cx - dx * LEAD_STOP, p.cy - dy * LEAD_STOP];
    const legA = y0 - turn;                          // the straight climb
    const legB = dl - LEAD_STOP;                     // the turn in
    const run = (legA + legB) * grow;

    ctx.save();
    ctx.strokeStyle = P.annYellow;
    ctx.fillStyle = P.annYellow;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = 2.2;
    ctx.setLineDash([11, 9]);
    ctx.beginPath();
    ctx.moveTo(LEAD_X, y0);
    if (run <= legA) {
      ctx.lineTo(LEAD_X, y0 - run);
    } else {
      ctx.lineTo(LEAD_X, turn);
      const u = (run - legA) / legB;
      ctx.lineTo(lerp(LEAD_X, tip[0], u), lerp(turn, tip[1], u));
    }
    ctx.stroke();
    ctx.setLineDash([]);
    if (grow >= 1) {
      // an arrowhead along the leader, stopping short of the centromere
      const nx = -dy, ny = dx;
      ctx.beginPath();
      ctx.moveTo(tip[0], tip[1]);
      ctx.lineTo(tip[0] - dx * 17 + nx * 7, tip[1] - dy * 17 + ny * 7);
      ctx.lineTo(tip[0] - dx * 17 - nx * 7, tip[1] - dy * 17 - ny * 7);
      ctx.closePath();
      ctx.fill();
    }
    ctx.restore();
  }

  // an annBlue ruler down the right of the cell, measuring the nucleus: the one overlay that is
  // already there on frame 0, so the match cut from 04 lands on a fully drawn plate
  function drawNucleusRuler(ctx, L, P) {
    const X = 930;
    const top = CY - NUC_R, bot = CY + NUC_R;
    const p = new Path2D();
    p.moveTo(X, top);
    p.lineTo(X, bot);
    for (let y = top; y <= bot + 0.01; y += 18.5) {
      const k = Math.round((y - top) / 18.5);
      const len = k % 5 === 0 ? 28 : 12;
      p.moveTo(X, y);
      p.lineTo(X - len, y);
    }
    // two short witness dashes, no further: a leader run back to the nucleus would box the cell in
    p.moveTo(X - 40, top);
    p.lineTo(X - 96, top);
    p.moveTo(X - 40, bot);
    p.lineTo(X - 96, bot);
    ctx.save();
    ctx.strokeStyle = P.annBlue;
    ctx.lineCap = 'round';
    ctx.lineWidth = 2;
    ctx.globalAlpha = 0.9;
    ctx.stroke(p);
    ctx.fillStyle = P.annBlue;
    for (const y of [top, bot]) {
      ctx.beginPath();
      ctx.arc(X, y, 4.5, 0, TAU);
      ctx.fill();
    }
    ctx.restore();
  }

  // the annBlue arc joining chromoA1's two arms, and the word that names what they are
  function drawIdenticalArc(ctx, L, P, pOn, poses) {
    if (pOn <= 0) return;
    const p = poses[0];
    const tips = tipsOf(p);
    const tl = tips[0], tr = tips[1];
    const aL = Math.atan2(tl[1] - p.cy, tl[0] - p.cx);
    const aR = Math.atan2(tr[1] - p.cy, tr[0] - p.cx);
    const rTip = Math.hypot(tl[0] - p.cx, tl[1] - p.cy);
    const R = rTip + 56;
    L.arcAnnotation(ctx, p.cx, p.cy, R, aL - 20 * DEG, aR + 20 * DEG, {
      color: P.annBlue,
      width: 2,
      alpha: 1,
      endTicks: 10,
      dot: 4,
      label: 'identical',
      labelSize: 34,
      labelOffset: 34,
      p: pOn,
    });
    // radial ties from each arm's tip out to the arc, so the arc visibly joins the two arms
    ctx.save();
    ctx.strokeStyle = P.annBlue;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.beginPath();
    for (const a of [aL, aR]) {
      const r0 = rTip + 7;
      const r1 = lerp(r0, R, clamp(pOn * 1.4));
      ctx.moveTo(p.cx + Math.cos(a) * r0, p.cy + Math.sin(a) * r0);
      ctx.lineTo(p.cx + Math.cos(a) * r1, p.cy + Math.sin(a) * r1);
      // a small perpendicular tick where the tie meets the arm
      const c = Math.cos(a), s = Math.sin(a);
      ctx.moveTo(p.cx + c * r0 + s * 7, p.cy + s * r0 - c * 7);
      ctx.lineTo(p.cx + c * r0 - s * 7, p.cy + s * r0 + c * 7);
    }
    ctx.stroke();
    ctx.restore();
  }

  // annYellow rings closing in on each chromosome as it condenses
  function drawTightenRings(ctx, L, P, t, poses) {
    if (t < B_COND - 1e-9) return;
    const age = (t - B_COND) * 24;
    if (age >= 6) return;
    const E = L.ease;
    ctx.save();
    ctx.strokeStyle = P.annYellow;
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.globalAlpha = 1 - clamp((age - 2) / 4);
    for (let i = 0; i < CHROMOS.length; i++) {
      const p = poses[i];
      const r0 = Math.hypot(p.w, p.h) + 22;
      const r = lerp(r0, r0 - 20, E.outExpo((age + 1) / 4));
      ctx.beginPath();
      ctx.arc(p.cx, p.cy, r, 0, TAU);
      ctx.stroke();
      if (age < 3) {
        ctx.beginPath();
        for (let k = 0; k < 4; k++) {
          const a = Math.PI / 4 + (k * Math.PI) / 2;
          ctx.moveTo(p.cx + Math.cos(a) * (r + 7), p.cy + Math.sin(a) * (r + 7));
          ctx.lineTo(p.cx + Math.cos(a) * (r + 17), p.cy + Math.sin(a) * (r + 17));
        }
        ctx.stroke();
      }
    }
    ctx.restore();
  }

  // ===========================================================================================
  // Scene
  // ===========================================================================================

  // the condense: three drawings from T 11.0, an overshoot past the final 94 percent
  const COND_S = [0.975, 0.928, 0.94];
  const COND_T = [0.35, 0.85, 1];

  FILM.scene({
    id: ID,
    draw(ctx, tIn, info) {
      const L = info.lib;
      const P = L.pal;
      const E = L.ease;
      const t = clamp(tIn, 0, info.dur);
      const d = Math.round(L.onTwos(t) * 12);          // drawing index, 12 a second
      const T = info.T;

      // beat helpers: `lead` makes an event visible ON its beat frame, not one frame after it
      const drawing = (a) => Math.floor((t - a) * 12 + 1e-6);
      const hit = (a, frames, e, lead = 1) => {
        if (t < a - 1e-9) return 0;
        const u = clamp((t - a) / (frames * FR) + lead / frames);
        return e ? e(u) : u;
      };

      // --- the condense state, shared by every chromosome ---
      let cond = { s: 1, thick: 1, tone: 0 };
      if (t >= B_COND - 1e-9) {
        const k = Math.min(2, drawing(B_COND));
        cond = { s: COND_S[k], thick: lerp(1, 1.08, COND_T[k]), tone: COND_T[k] };
      }
      const poses = CHROMOS.map((c) => poseOf(c, d, cond));
      const glowA1 = t >= B_ARC - 1e-9 && drawing(B_ARC) < 3;

      // 1. background -------------------------------------------------------------------------
      drawBackground(ctx, L, P, T);

      // 2. the tissue round the hero cell ------------------------------------------------------
      drawNeighbours(ctx, L, P);

      // 3. construction -----------------------------------------------------------------------
      drawConstruction(ctx, L, P);

      // 4. the cell's cast shadow --------------------------------------------------------------
      drawCellShadow(ctx, L, P);

      // 5. cytoplasm, 6. mitochondria ----------------------------------------------------------
      drawCytoplasm(ctx, L, P);
      drawMitochondria(ctx, L, P);

      // 7. nucleus -----------------------------------------------------------------------------
      drawNucleus(ctx, L, P);

      // 8. the four X chromosomes on G2 ---------------------------------------------------------
      drawChromoShadow(ctx, L, P, poses);
      // the upper pair first, the lower pair over it, so the frame reads back to front
      for (const i of [0, 1, 2, 3]) {
        drawChromosome(ctx, L, P, CHROMOS[i], poses[i], glowA1 && CHROMOS[i].key === 'A1');
      }

      // 9. the membrane, last of the drawing ----------------------------------------------------
      drawMembrane(ctx, L, P);

      // 10. overlays ----------------------------------------------------------------------------
      drawNucleusRuler(ctx, L, P);
      drawCentromereRings(ctx, L, P, t, poses);
      drawBracket(ctx, L, P, hit(B_RING, 4, E.outExpo), poses);
      drawIdenticalArc(ctx, L, P, hit(B_ARC, 6, E.outExpo), poses);
      drawTightenRings(ctx, L, P, t, poses);

      // 11. the film's time device, drawn last and never re-implemented --------------------------
      L.cycleGlyph(ctx, T, 'illustrated');
    },
  });
})();
