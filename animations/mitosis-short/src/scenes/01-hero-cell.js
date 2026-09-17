// 01 hero-cell : Cold open, one body cell among many.
//
// T 0.0 to 2.0, illustrated (paper plate). Enters on the film start and on the loop replay from 11.
// One generic animal body cell sits on the storyboard's G1 geometry, huge in a tall frame, with
// neighbour cells cut by the four edges so the field reads as living tissue. Inside the membrane:
// cytoplasm with directional hatching near the rim, ribosome stipple, six bean mitochondria, and one
// nucleus holding four loose worm chromosomes (two pairs: chromoA long blue, chromoB short rust).
//
// Frame 0 is the full pose. The cell breathes on the 0.5 s beat (membrane 380 to 392 and back over
// three drawings) while a magenta and a yellow ring burst from the nucleus; smaller breaths land on
// T 1.0 and T 1.5. The camera pushes in from zoom 1.00 to 1.04 with inOutSine.
//
// Layers, back to front:
//   0  the paper plate
//   1  stripes (screen-fixed, full bleed, drifting 1 px per frame)
//   2  neighbour cells, quiet, cut by the frame edges
//   3  the hero's contact shade on the tissue, lower right only
//   4  construction geometry: guide circles, the 45 degree diameters, the square, registration marks
//   5  the hero cell: cytoplasm, hatching, ribosomes, mitochondria, nucleus, nucleolus, chromosomes,
//      then the doubled ink membrane on top
//   6  overlays: the annBlue ring band (r 400 to 440), the annYellow 90 degree ruler arc over the
//      top, and the burst rings on the beats
//   7  the shared cycle glyph, screen-fixed, always last
//
// Match cut: 02 cuts onto this outline, so every number in the G1 block below is copied verbatim
// from docs/storyboard.md "Shared geometry / G1". A sibling shot that needs the same wobbled
// outline must seed it the same way: LIB.hash('hero-cell', 'membrane') and 'nucleus'.
//
// Biology held to (art bible 10.1, 10.2, 10.7): an irregular near-circle, no cell wall, no
// chloroplasts, no vacuole; exactly four chromosomes in two equal-length pairs, drawn (never hidden)
// as long thin threads because the DNA has not been copied yet; mitochondria with folded inner
// ridges; ribosomes as stipple; a nucleolus inside the nuclear membrane.
(function () {
  'use strict';

  const ID = 'hero-cell';
  const LIB = FILM.lib;
  const TAU = Math.PI * 2;
  const DEG = Math.PI / 180;

  // ---------------------------------------------------------------------------
  // small maths
  // ---------------------------------------------------------------------------

  const lerp = (a, b, t) => a + (b - a) * t;
  const clamp = (v, lo = 0, hi = 1) => (v < lo ? lo : v > hi ? hi : v);
  const sstep = (a, b, x) => {
    const t = clamp((x - a) / (b - a || 1e-6));
    return t * t * (3 - 2 * t);
  };
  // every seed in this file derives from the shot id, so the drawing is identical on every render
  const sd = (...k) => LIB.hash(ID, ...k) & 0x7fffffff;

  function trace(ctx, pts, closed = true) {
    for (let i = 0; i < pts.length; i++) {
      if (i === 0) ctx.moveTo(pts[i][0], pts[i][1]);
      else ctx.lineTo(pts[i][0], pts[i][1]);
    }
    if (closed) ctx.closePath();
  }

  function fillPoly(ctx, pts, color, alpha = 1) {
    ctx.save();
    ctx.globalAlpha *= alpha;
    ctx.fillStyle = color;
    ctx.beginPath();
    trace(ctx, pts, true);
    ctx.fill();
    ctx.restore();
  }

  // A closed rod around a centreline: both flanks offset by halfW, with true half-disc ends, so a
  // chromosome thread or a mitochondrion reads as a tube and not as a lens.
  function rodPoly(line, halfW) {
    const n = line.length;
    if (n < 2) return line.slice();
    let total = 0;
    for (let i = 1; i < n; i++) total += Math.hypot(line[i][0] - line[i - 1][0], line[i][1] - line[i - 1][1]);
    const capF = clamp(halfW / Math.max(1e-3, total), 0.02, 0.45);
    const left = [], right = [];
    for (let i = 0; i < n; i++) {
      const a = line[Math.max(0, i - 1)], b = line[Math.min(n - 1, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const l = Math.hypot(tx, ty) || 1;
      tx /= l;
      ty /= l;
      const u = i / (n - 1);
      const e = Math.min(u, 1 - u);
      const kk = e >= capF ? 1 : Math.sqrt(Math.max(0, 1 - Math.pow(1 - e / capF, 2)));
      const w = halfW * kk;
      left.push([line[i][0] - ty * w, line[i][1] + tx * w]);
      right.push([line[i][0] + ty * w, line[i][1] - tx * w]);
    }
    return left.concat(right.reverse());
  }

  // A closed, seeded, organic near-circle. Four harmonics, so the loop joins itself exactly and the
  // shape reads as a living cell rather than a compass circle. The low harmonics carry most of the
  // amplitude, which flattens one flank and bulges another, the way a cell pressed by its neighbours
  // actually sits.
  function lumpy(seed) {
    const r = LIB.rng(seed);
    const p1 = r.range(0, TAU), p2 = r.range(0, TAU), p3 = r.range(0, TAU), p4 = r.range(0, TAU);
    const w1 = r.range(0.52, 0.66), w2 = r.range(0.3, 0.42), w3 = r.range(0.14, 0.22), w4 = r.range(0.07, 0.12);
    const norm = w1 + w2 + w3 + w4;
    return (a) =>
      (w1 * Math.sin(2 * a + p1) + w2 * Math.sin(3 * a + p2) + w3 * Math.sin(5 * a + p3) + w4 * Math.sin(8 * a + p4)) / norm;
  }

  function lumpyRing(cx, cy, R, amp, n, shape) {
    const out = [];
    for (let i = 0; i < n; i++) {
      const a = (i / n) * TAU;
      const rr = R + amp * shape(a);
      out.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]);
    }
    return out;
  }

  // ---------------------------------------------------------------------------
  // G1: the hero cell (docs/storyboard.md, Shared geometry). 02, 03 and 11 land on these numbers.
  // ---------------------------------------------------------------------------

  const CX = 540;          // cell centre x
  const CY = 900;          // cell centre y
  const R0 = 380;          // mean membrane radius at rest
  const NR0 = 170;         // mean nuclear radius

  const MEM_SHAPE = lumpy(sd('membrane'));
  const NUC_SHAPE = lumpy(sd('nucleus'));

  // 40-point polyline, radius R + 14 * noise (storyboard G1). The wobble shape is fixed; only R breathes.
  const membranePts = (R) => lumpyRing(CX, CY, R, 14, 40, MEM_SHAPE);
  // the nucleus is a near-circle too, a little quieter than the membrane
  const nucleusPts = (R) => lumpyRing(CX, CY, R, 8, 32, NUC_SHAPE);

  // Four chromosomes, two pairs. Both members of a pair are the same length, width and colour; the
  // two pairs differ. Tilted 20 degrees, alternately left and right (storyboard G1). They are long
  // and thin here because the DNA has not been copied yet (art bible 10.2).
  const CHROMO = [
    { key: 'A1', c: [470, 850], len: 130, deg: -20, half: 10, fill: 'chromoA', deep: 'chromoADeep' },
    { key: 'A2', c: [610, 850], len: 130, deg: 20, half: 10, fill: 'chromoA', deep: 'chromoADeep' },
    { key: 'B1', c: [480, 955], len: 85, deg: -20, half: 8.5, fill: 'chromoB', deep: 'chromoBDeep' },
    { key: 'B2', c: [600, 955], len: 85, deg: 20, half: 8.5, fill: 'chromoB', deep: 'chromoBDeep' },
  ];

  // The nucleolus: a denser disc inside the nucleus (general cell biology), drawn under the
  // chromosomes so nothing in the count of four is hidden by it.
  const NUCLEOLUS = { x: 500, y: 870, r: 27 };

  // Six mitochondria, 60 by 28 px, at the storyboard's G1 positions. Rotations and sizes are
  // hand-set so no two lie parallel and none crowds the nucleus.
  const MITO = [
    { x: 300, y: 700, rot: 0.55, s: 1.0 },
    { x: 760, y: 720, rot: -0.5, s: 0.94 },
    { x: 280, y: 1060, rot: -0.35, s: 1.06 },
    { x: 790, y: 1080, rot: 0.62, s: 0.97 },
    { x: 420, y: 1190, rot: 0.15, s: 1.03 },
    { x: 660, y: 640, rot: -0.8, s: 0.92 },
  ];

  // Neighbour cells: partial circles cut by the frame edge, radius 300 to 360 (storyboard G1), drawn
  // in the same style but quiet, so the hero keeps the frame. They carry no chromosomes: the film
  // asks the viewer to count four, and four is all that may be countable.
  const NEIGH = [
    { x: 60, y: 380, r: 318, k: 1 },
    { x: 1020, y: 420, r: 330, k: 2 },
    { x: 40, y: 1420, r: 326, k: 3 },
    { x: 1040, y: 1400, r: 336, k: 4 },
    { x: 540, y: 1690, r: 344, k: 5 },
  ];

  // ---------------------------------------------------------------------------
  // Static geometry, built once. Everything here is strictly t-independent.
  // ---------------------------------------------------------------------------

  // A mitochondrion in its own coordinates: a 56 px rod bent 6 px so it reads as a bean, with the
  // convex side up (toward the light) and cristae folding in from alternate flanks.
  const MITO_GEO = (() => {
    const line = [];
    const N = 24;
    for (let i = 0; i <= N; i++) {
      const u = i / N - 0.5;
      line.push([u * 56, -6 * (1 - 4 * u * u) + 3]);
    }
    const centre = LIB.smoothPts(line, false, 2.5);
    const outline = rodPoly(centre, 12.5);
    // cristae: seven folds of the inner membrane, alternating sides, each crossing about 70 per cent
    const cristae = [];
    for (let j = 0; j < 7; j++) {
      const u = -0.33 + j * 0.11;
      const i = Math.round((u + 0.5) * (centre.length - 1));
      const p = centre[Math.min(centre.length - 1, Math.max(0, i))];
      const a = centre[Math.max(0, i - 2)], b = centre[Math.min(centre.length - 1, i + 2)];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const l = Math.hypot(tx, ty) || 1;
      tx /= l;
      ty /= l;
      const nx = -ty, ny = tx;
      const s = j % 2 ? 1 : -1;
      const w = 11.2;
      const o0 = [p[0] + nx * w * s, p[1] + ny * w * s];
      const o1 = [p[0] - nx * w * 0.36 * s + tx * 3.4 * s, p[1] - ny * w * 0.36 * s + ty * 3.4 * s];
      const mid = [(o0[0] + o1[0]) / 2 + tx * 2.8 * s, (o0[1] + o1[1]) / 2 + ty * 2.8 * s];
      cristae.push([o0, mid, o1]);
    }
    // the inner membrane runs just inside the outer one, so the folds have something to leave from
    const inner = rodPoly(centre, 9.6);
    return { centre, outline, inner, cristae };
  })();

  // Each neighbour cell: its wobbled membrane, a nucleus leaning toward the frame centre, a
  // nucleolus and two mitochondria, all fixed for the life of the film.
  const NEIGH_GEO = NEIGH.map((N) => {
    const seed = sd('neigh', N.k);
    const pts = lumpyRing(N.x, N.y, N.r, 15, 36, lumpy(seed));
    let dx = CX - N.x, dy = CY - N.y;
    const dl = Math.hypot(dx, dy) || 1;
    dx /= dl;
    dy /= dl;
    const nx = N.x + dx * N.r * 0.32;
    const ny = N.y + dy * N.r * 0.32;
    const nr = N.r * 0.28;
    const npts = lumpyRing(nx, ny, nr, 9, 26, lumpy(seed + 11));
    // the clip the interior work uses: pulled in so no stroke lands outside the wandering pen line
    const ptsIn = lumpyRing(N.x, N.y, N.r - 6, 15, 36, lumpy(seed));
    const r = LIB.rng(seed + 31);
    const mitos = [];
    // four mitochondria each, kept clear of the nucleus, so a neighbour reads as a working cell
    for (let j = 0; j < 4; j++) {
      let a = 0, rad = 0, px = 0, py = 0, tries = 0;
      do {
        a = r.range(0, TAU);
        rad = N.r * r.range(0.42, 0.72);
        px = N.x + Math.cos(a) * rad;
        py = N.y + Math.sin(a) * rad;
        tries++;
      } while (Math.hypot(px - nx, py - ny) < nr + 34 && tries < 8);
      mitos.push({ x: px, y: py, rot: r.range(-1.2, 1.2), s: 0.8 });
    }
    const nucleolus = { x: nx - nr * 0.26, y: ny - nr * 0.2, r: nr * 0.3 };
    return { N, pts, ptsIn, nx, ny, nr, npts, nucleolus, mitos };
  });

  // Registration crosses on the G1 points a later shot has to hit.
  const MARKS = (() => {
    const out = [[CX, CY], [NUCLEOLUS.x, NUCLEOLUS.y]];
    for (const c of CHROMO) out.push(c.c);
    for (const m of MITO) out.push([m.x, m.y]);
    out.push([CX - R0, CY], [CX + R0, CY], [CX, CY - R0], [CX, CY + R0]);
    return out;
  })();

  // Nuclear pores: short paired ticks straddling the nuclear membrane. Fixed angles, so they sit on
  // the rim wherever the rim's own wobble puts it.
  const PORE_A = (() => {
    const out = [];
    const r = LIB.rng(sd('pores'));
    for (let i = 0; i < 20; i++) out.push((i / 20) * TAU + r.range(-0.045, 0.045));
    return out;
  })();

  // ---------------------------------------------------------------------------
  // Chromosome threads
  // ---------------------------------------------------------------------------

  // A loose, uncondensed chromosome: a slack thread that drifts off its own axis. `k` is the drawing
  // index on twos, so the thread trembles twelve times a second and holds between.
  function wormCentre(c, len, deg, seed, k, trem) {
    const a = deg * DEG;
    const ca = Math.cos(a), sa = Math.sin(a);
    const N = 20;
    const raw = [];
    const off = (u) => len * 0.16 * LIB.noise1(u * 2.6 + 1.7, seed) + len * 0.07 * LIB.noise1(u * 6.1 + 0.3, seed + 3);
    const v0 = off(0);
    for (let i = 0; i <= N; i++) {
      const u = i / N - 0.5;
      const s = u * len;
      // the ends are free to swing, the middle barely moves: a thread, not a rigid bar
      const swing = trem * (0.35 + 1.5 * u * u);
      const v = off(u) - v0 + (LIB.h3(i * 7 + 1, k, seed) - 0.5) * 2 * swing;
      raw.push([c[0] + s * ca - v * sa, c[1] + s * sa + v * ca]);
    }
    return LIB.smoothPts(raw, false, 3);
  }

  function drawWorm(ctx, L, P, spec, seed, k, opts) {
    const o = opts || {};
    const alpha = o.alpha != null ? o.alpha : 1;
    const line = wormCentre(spec.c, spec.len, spec.deg, seed, k, o.trem != null ? o.trem : 2.6);
    const halfW = spec.half;
    const poly = rodPoly(line, halfW);
    const fill = P[spec.fill];
    const deep = P[spec.deep];
    ctx.save();
    ctx.globalAlpha *= alpha;
    // 1. the body, filled and outlined in one hand-inked pass
    L.inkPath(ctx, poly, {
      closed: true,
      width: o.line != null ? o.line : 2.4,
      color: P.ink,
      fill,
      seed: seed + 1,
      wobble: 0.9,
      tremble: 0.35,
      taper: [6, 10],
    });
    // 2. contour hatching across the tube, on the shadow flank only (art bible 4.1: cylinders)
    if (o.hatch !== false) {
      const a = spec.deg * DEG;
      const nx = -Math.sin(a), ny = Math.cos(a);
      const s = nx * 0.7071 + ny * 0.7071 >= 0 ? 1 : -1;
      const cx = spec.c[0], cy = spec.c[1];
      L.hatch(ctx, poly, {
        angle: a + Math.PI / 2,
        spacing: 6,
        width: 1.3,
        color: deep,
        alpha: 0.9,
        length: [5, 17],
        gap: [1.2, 3],
        inset: 1.2,
        overshoot: 1,
        bend: 1.4,
        seed: seed + 2,
        density: (x, y) => sstep(-0.2, 0.75, (s * ((x - cx) * nx + (y - cy) * ny)) / halfW),
      });
    }
    // 3. a chromatin line down the middle so the thread reads as coiled, not solid
    if (o.core !== false) {
      L.inkPath(ctx, line, {
        width: 1.5,
        color: deep,
        alpha: 0.5,
        seed: seed + 4,
        taper: [halfW * 1.8, halfW * 2.4],
        wobble: 0.6,
        swell: 0,
      });
    }
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // Mitochondria
  // ---------------------------------------------------------------------------

  // `plain` drops the cristae and the tone: the neighbours' mitochondria are only a hint of one.
  function drawMito(ctx, L, P, x, y, rot, seed, scale, plain) {
    const s = scale || 1;
    const ca = Math.cos(rot), sa = Math.sin(rot);
    const M = (p) => [x + (p[0] * ca - p[1] * sa) * s, y + (p[0] * sa + p[1] * ca) * s];
    const outline = MITO_GEO.outline.map(M);
    L.inkPath(ctx, outline, {
      closed: true,
      width: 2.8 * s,
      color: P.ink,
      fill: P.mito,
      seed: seed + 1,
      wobble: 0.9,
      tremble: 0.3,
      taper: [6, 10],
    });
    if (plain) {
      // one folded ridge, so even the small ones read as mitochondria and not as beans of jelly
      L.inkPath(ctx, MITO_GEO.cristae[3].map(M), {
        width: 1.8 * s,
        color: P.mitoDeep,
        alpha: 0.9,
        seed: seed + 9,
        taper: [2, 4],
        wobble: 0.4,
        step: 2,
      });
      return;
    }
    // the inner membrane, running just inside the outer one
    L.inkPath(ctx, MITO_GEO.inner.map(M), {
      closed: true,
      width: 1.5 * s,
      color: P.mitoDeep,
      alpha: 0.65,
      seed: seed + 2,
      wobble: 0.5,
      taper: [8, 14],
    });
    // cristae: the folded inner membrane, drawn as separate short strokes
    for (let j = 0; j < MITO_GEO.cristae.length; j++) {
      const c = MITO_GEO.cristae[j].map(M);
      L.inkPath(ctx, c, {
        width: 2.1 * s,
        color: P.mitoDeep,
        alpha: 1,
        seed: seed + 10 + j,
        taper: [2, 4],
        wobble: 0.4,
        swell: 0.12,
        step: 2,
      });
    }
    // tone: the lower-right half of the bean turns from the light
    L.hatch(ctx, outline, {
      angle: -Math.PI / 4,
      spacing: 4.4 * s,
      width: 1.2,
      color: P.mitoDeep,
      alpha: 0.85,
      length: [5, 15],
      gap: [1.5, 4],
      inset: 1.2,
      overshoot: 1,
      seed: seed + 3,
      density: (px, py) => sstep(-0.1, 0.9, ((px - x) * 0.7071 + (py - y) * 0.7071) / (14 * s)),
    });
  }

  // ---------------------------------------------------------------------------
  // Neighbour cells: the tissue the hero sits in
  // ---------------------------------------------------------------------------

  // one pen setting for every neighbour membrane, so the fill pass and the line pass coincide
  const NEIGH_PEN = { closed: true, width: 4.2, wobble: 3, wobbleFreq: 1 / 190, tremble: 0.5 };

  function drawNeighbour(ctx, L, P, G) {
    const seed = sd('neighdraw', G.N.k);
    const N = G.N;
    // 1. cytoplasm, filled along this cell's own inked outline
    L.inkPath(ctx, G.pts, Object.assign({ fill: P.neighbour, alpha: 0.001 }, NEIGH_PEN, { seed: seed + 6 }));
    // 2. a single band of tone near the rim, heavier on the lower right
    L.hatch(ctx, [G.ptsIn, G.npts], {
      angle: -Math.PI / 4,
      spacing: 12,
      width: 1.3,
      color: P.cytoHatch,
      alpha: 0.6,
      length: [14, 38],
      inset: 5,
      overshoot: 2,
      seed: seed + 1,
      density: (x, y) => {
        const d = Math.hypot(x - N.x, y - N.y) / N.r;
        const lit = ((x - N.x) + (y - N.y)) / (N.r * 1.414);
        return sstep(0.5, 0.99, d) * lerp(0.25, 1, sstep(-0.8, 0.8, lit));
      },
    });
    // 3. ribosomes, sparser than the hero's so the eye stays on the middle of the frame
    L.stipple(ctx, [G.ptsIn, G.npts], {
      spacing: 13,
      density: 0.2,
      r: [1.0, 1.9],
      color: P.ribosome,
      alpha: 0.6,
      seed: seed + 2,
    });
    // 4. two mitochondria, drawn plain
    for (let j = 0; j < G.mitos.length; j++) {
      const m = G.mitos[j];
      drawMito(ctx, L, P, m.x, m.y, m.rot, seed + 20 + j * 13, m.s, true);
    }
    // 5. nucleus: a soft disc with its own rim, chromatin texture, shading and an off-centre nucleolus
    L.inkPath(ctx, G.npts, {
      closed: true,
      width: 3.2,
      color: P.nucleusRim,
      alpha: 0.9,
      fill: P.neighbourNucleus,
      seed: seed + 3,
      wobble: 1.4,
    });
    L.stipple(ctx, G.npts, {
      spacing: 9,
      density: 0.26,
      r: [0.8, 1.4],
      color: P.nucleusDeep,
      alpha: 0.45,
      seed: seed + 7,
    });
    L.hatch(ctx, G.npts, {
      angle: -Math.PI / 4,
      spacing: 7.5,
      width: 1.25,
      color: P.nucleusDeep,
      alpha: 0.55,
      length: [8, 24],
      inset: 3,
      seed: seed + 4,
      density: (x, y) => sstep(-0.4, 0.95, ((x - G.nx) + (y - G.ny)) / (G.nr * 1.414)),
    });
    L.inkCircle(ctx, G.nucleolus.x, G.nucleolus.y, G.nucleolus.r, {
      width: 1.8,
      color: P.nucleusRim,
      alpha: 0.8,
      fill: P.nucleusDeep,
      fillAlpha: 0.85,
      seed: seed + 5,
      wobble: 0.8,
      ry: G.nucleolus.r * 0.9,
    });
    // 6. the membrane last, so it stays crisp over everything inside
    L.inkPath(ctx, G.pts, Object.assign({ color: P.ink, alpha: 0.82, double: { width: 0.3, offset: 3, alpha: 0.25 } }, NEIGH_PEN, { seed: seed + 6 }));
  }

  // ---------------------------------------------------------------------------
  // Construction geometry, in inkFaint, behind the hero cell
  // ---------------------------------------------------------------------------

  function drawConstruction(ctx, L, P) {
    const faint = { width: 1.5, color: P.inkFaint, alpha: 0.3, taper: [0, 0], wobble: 1.5, smooth: false, step: 9 };
    ctx.save();
    // the two 45 degree diameters, running well past the cell
    for (const a of [-Math.PI / 4, Math.PI / 4]) {
      const c = Math.cos(a), s = Math.sin(a);
      L.inkPath(ctx, [[CX - c * 640, CY - s * 640], [CX + c * 640, CY + s * 640]], Object.assign({ seed: sd('diag', a > 0 ? 1 : 0) }, faint));
    }
    // the upright and level axes, quieter still
    L.inkPath(ctx, [[CX, CY - 700], [CX, CY + 760]], Object.assign({}, faint, { seed: sd('axisV'), alpha: 0.2 }));
    L.inkPath(ctx, [[CX - 620, CY], [CX + 620, CY]], Object.assign({}, faint, { seed: sd('axisH'), alpha: 0.2 }));
    // a faint square around the cell, drawn as four separate pen strokes so the corners stay open
    const x0 = CX - R0, x1 = CX + R0, y0 = CY - R0, y1 = CY + R0;
    const sq = [
      [[x0, y0], [x1, y0]],
      [[x1, y0], [x1, y1]],
      [[x1, y1], [x0, y1]],
      [[x0, y1], [x0, y0]],
    ];
    for (let i = 0; i < 4; i++) L.inkPath(ctx, sq[i], Object.assign({ seed: sd('square', i) }, faint));
    // guide circles: the nucleus, and one wide circle the overlay ring sits inside
    L.guideCircle(ctx, CX, CY, NR0, { color: P.inkFaint, alpha: 0.3, width: 1.5, dash: [3, 8] });
    L.guideCircle(ctx, CX, CY, 600, { color: P.inkFaint, alpha: 0.2, width: 1.5 });
    // a degree scale over the top of the cell, as in the reference's cold open
    {
      const minor = new Path2D(), major = new Path2D();
      for (let a = -175; a <= -5; a += 5) {
        const c = Math.cos(a * DEG), s = Math.sin(a * DEG);
        const p = a % 15 === 0 ? major : minor;
        const len = a % 15 === 0 ? 18 : 9;
        p.moveTo(CX + c * R0, CY + s * R0);
        p.lineTo(CX + c * (R0 + len), CY + s * (R0 + len));
      }
      ctx.save();
      ctx.strokeStyle = P.inkFaint;
      ctx.lineCap = 'round';
      ctx.lineWidth = 1.5;
      ctx.globalAlpha = 0.34;
      ctx.stroke(minor);
      ctx.globalAlpha = 0.5;
      ctx.stroke(major);
      ctx.restore();
    }
    // registration crosses on the points a later shot must hit
    {
      const marks = new Path2D();
      for (const [x, y] of MARKS) {
        marks.moveTo(x - 9, y);
        marks.lineTo(x + 9, y);
        marks.moveTo(x, y - 9);
        marks.lineTo(x, y + 9);
      }
      ctx.save();
      ctx.strokeStyle = P.inkFaint;
      ctx.globalAlpha = 0.5;
      ctx.lineWidth = 1.5;
      ctx.stroke(marks);
      ctx.restore();
    }
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // Timing
  // ---------------------------------------------------------------------------

  const B_BREATH1 = 0.5;   // T 0.5, the beat: the big breath and the ring burst
  const B_BREATH2 = 1.0;   // T 1.0
  const B_BREATH3 = 1.5;   // T 1.5

  // A breath is a three-drawing pop with a small overshoot, then a two-drawing settle.
  const BREATH_PROFILE = [0.5, 1.0, 0.62, 0.24, 0.07];
  const BREATHS = [[B_BREATH1, 12], [B_BREATH2, 7], [B_BREATH3, 5]];

  function breathAt(t) {
    let v = 0;
    for (let i = 0; i < BREATHS.length; i++) {
      const a = BREATHS[i][0], amp = BREATHS[i][1];
      if (t < a - 1e-6) continue;
      const d = Math.floor((t - a) * 12 + 1e-6);
      if (d >= 0 && d < BREATH_PROFILE.length) v += amp * BREATH_PROFILE[d];
    }
    return v;
  }

  // ---------------------------------------------------------------------------
  // Overlays
  // ---------------------------------------------------------------------------

  // A ring leaving the nucleus. `delay` is in frames after the beat; the ring is drawn on the beat
  // frame itself, starting exactly on the nuclear rim.
  function burstRing(ctx, P, E, t, beat, color, delay, r0, r1, frames, fade, ticks, width) {
    const f = (t - beat) * 24 - delay;
    if (f < -1e-6 || f > fade + 2) return;
    const r = lerp(r0, r1, E.outExpo(clamp(f / frames)));
    const alpha = 1 - clamp((f - 2) / fade);
    if (alpha <= 0) return;
    const p = new Path2D();
    p.moveTo(CX + r, CY);
    p.arc(CX, CY, r, 0, TAU);
    if (ticks) {
      for (let q = 0; q < 4; q++) {
        const a = Math.PI / 4 + (q * Math.PI) / 2;
        p.moveTo(CX + Math.cos(a) * (r - 10), CY + Math.sin(a) * (r - 10));
        p.lineTo(CX + Math.cos(a) * (r + 10), CY + Math.sin(a) * (r + 10));
      }
    }
    ctx.save();
    ctx.lineCap = 'round';
    // an ink underlay so the ring still reads where it crosses the yellow stripes
    ctx.strokeStyle = P.ink;
    ctx.lineWidth = width + 3;
    ctx.globalAlpha = alpha * 0.22;
    ctx.stroke(p);
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.globalAlpha = alpha;
    ctx.stroke(p);
    ctx.restore();
  }

  function drawOverlays(ctx, L, P, E, t, R) {
    // 1. the annBlue ring band, radius 400 to 440, with four radial ties on the diagonals
    ctx.save();
    ctx.lineCap = 'round';
    ctx.strokeStyle = P.annBlue;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(CX, CY, 400, 0, TAU);
    ctx.stroke();
    ctx.globalAlpha = 0.55;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(CX, CY, 440, 0, TAU);
    ctx.stroke();
    const ties = new Path2D();
    for (let q = 0; q < 4; q++) {
      const a = Math.PI / 4 + (q * Math.PI) / 2;
      ties.moveTo(CX + Math.cos(a) * 400, CY + Math.sin(a) * 400);
      ties.lineTo(CX + Math.cos(a) * 440, CY + Math.sin(a) * 440);
    }
    ctx.globalAlpha = 0.8;
    ctx.lineWidth = 2;
    ctx.stroke(ties);
    // the origin mark where the band crosses the upright axis
    ctx.globalAlpha = 1;
    ctx.fillStyle = P.annBlue;
    ctx.beginPath();
    ctx.arc(CX, CY + 440, 4, 0, TAU);
    ctx.fill();
    ctx.restore();

    // 2. the annYellow 90 degree arc with its ruler, over the top of the cell
    const a0 = -135 * DEG, a1 = -45 * DEG;
    L.ticks(ctx, CX, CY, {
      r: 470,
      n: 19,
      start: a0,
      span: a1 - a0,
      len: 13,
      major: 3,
      majorLen: 30,
      color: P.annYellow,
      alpha: 1,
      width: 2.2,
    });
    L.arcAnnotation(ctx, CX, CY, 470, a0, a1, {
      color: P.annYellow,
      width: 2.5,
      endTicks: 12,
      alpha: 1,
    });
    // a dotted leader from the crown of the arc down to the crown of the membrane, so the ruler
    // reads as measuring this cell and not as decoration
    ctx.save();
    ctx.fillStyle = P.annYellow;
    ctx.beginPath();
    ctx.arc(CX, CY - 470, 5, 0, TAU);
    ctx.fill();
    const dots = new Path2D();
    for (let y = CY - 452; y < CY - R0 - 14; y += 15) {
      dots.moveTo(CX + 2.6, y);
      dots.arc(CX, y, 2.6, 0, TAU);
    }
    ctx.globalAlpha = 0.85;
    ctx.fill(dots);
    ctx.restore();

    // 3. the burst on the beat: magenta leads, yellow follows two frames later
    burstRing(ctx, P, E, t, B_BREATH1, P.annMagenta, 0, NR0, 520, 6, 12, false, 3);
    burstRing(ctx, P, E, t, B_BREATH1, P.annYellow, 2, NR0, 520, 6, 12, true, 3);
    // the smaller breaths carry a single quiet yellow echo each
    burstRing(ctx, P, E, t, B_BREATH2, P.annYellow, 0, NR0, 330, 5, 8, false, 2);
    burstRing(ctx, P, E, t, B_BREATH3, P.annYellow, 0, NR0, 320, 5, 8, false, 2);
  }

  // ---------------------------------------------------------------------------
  // The hero cell
  // ---------------------------------------------------------------------------

  // A band of tone in the intercellular space on the lower right of the hero, so the cell lifts off
  // the tissue behind it. Light comes from the upper left.
  function drawContactShade(ctx, L, P, R) {
    const inner = membranePts(R + 3);
    const outer = membranePts(R + 62);
    L.hatch(ctx, [outer, inner], {
      angle: -Math.PI / 4,
      spacing: 5,
      width: 1.4,
      color: P.paperDeep,
      alpha: 0.75,
      length: [8, 26],
      inset: 2,
      overshoot: 2,
      seed: sd('contact'),
      density: (x, y) => sstep(0.05, 0.85, ((x - CX) + (y - CY)) / (R * 1.414)),
    });
  }

  // The membrane is inked twice with the same seed, so both passes land on the same wandering line:
  // once under everything to lay the cytoplasm down inside the drawn outline, once on top.
  const MEM_PEN = {
    closed: true,
    width: 6,
    seed: sd('mem'),
    wobble: 4,
    wobbleFreq: 1 / 210,
    tremble: 0.7,
  };

  function drawHeroCell(ctx, L, P, R, k) {
    const mem = membranePts(R);
    // everything inside clips to a slightly tighter ring, so no hatch stroke can land outside the
    // wandering pen line
    const memIn = membranePts(R - 5);
    const nuc = nucleusPts(NR0);

    // 1. cytoplasm, filled along the membrane's own inked outline
    L.inkPath(ctx, mem, Object.assign({ color: P.membrane, fill: P.cytoplasm, alpha: 0.001 }, MEM_PEN));

    // 2. a very light overall tone across the whole cytoplasm, so the fill is never a flat plane
    L.hatch(ctx, [memIn, nuc], {
      angle: -Math.PI / 4,
      spacing: 16,
      width: 1.2,
      color: P.cytoHatch,
      alpha: 0.42,
      length: [20, 60],
      gap: [6, 18],
      inset: 8,
      seed: sd('cytoflat'),
      density: 0.55,
    });

    // 3. directional hatching near the membrane. Light falls from the upper left, so the band
    //    thickens around the lower right. The nucleus is a hole in the clip.
    L.hatch(ctx, [memIn, nuc], {
      angle: -Math.PI / 4,
      spacing: 7,
      width: 1.6,
      color: P.cytoHatch,
      alpha: 1,
      length: [14, 44],
      gap: [2, 7],
      inset: 5,
      overshoot: 2,
      seed: sd('cyto'),
      density: (x, y) => {
        const d = Math.hypot(x - CX, y - CY) / R;
        const lit = ((x - CX) + (y - CY)) / (R * 1.414);
        return sstep(0.32, 0.97, d) * lerp(0.3, 1, sstep(-0.85, 0.75, lit));
      },
    });
    // the cross layer, only in the deepest corner of the shadow
    L.hatch(ctx, [memIn, nuc], {
      angle: -Math.PI / 4 - Math.PI / 3,
      spacing: 7.5,
      width: 1.4,
      color: P.cytoHatch,
      alpha: 0.85,
      length: [10, 32],
      inset: 5,
      overshoot: 1,
      seed: sd('cyto2'),
      density: (x, y) => {
        const d = Math.hypot(x - CX, y - CY) / R;
        const lit = ((x - CX) + (y - CY)) / (R * 1.414);
        return sstep(0.44, 0.99, d) * sstep(0.1, 0.9, lit);
      },
    });
    // 4. ribosomes: fine stipple across the cytoplasm at the storyboard's density, boiling
    L.stipple(ctx, [memIn, nuc], {
      spacing: 6.8,
      density: 0.35,
      r: [0.8, 2.1],
      color: P.ribosome,
      alpha: 0.85,
      seed: sd('ribo'),
    });

    // 5. mitochondria, drifting a little with the breath so the inside of the cell feels alive
    const push = (R - R0) * 0.22;
    for (let i = 0; i < MITO.length; i++) {
      const m = MITO[i];
      const dx = m.x - CX, dy = m.y - CY;
      const dl = Math.hypot(dx, dy) || 1;
      const f = push * (dl / R0);
      drawMito(ctx, L, P, m.x + (dx / dl) * f, m.y + (dy / dl) * f, m.rot, sd('mito', i), m.s, false);
    }

    // 6. the nucleus: fill, chromatin stipple, shading that wraps the lower half
    fillPoly(ctx, nuc, P.nucleus);
    L.stipple(ctx, nuc, {
      spacing: 8,
      density: 0.3,
      r: [0.8, 1.5],
      color: P.nucleusDeep,
      alpha: 0.5,
      seed: sd('chromatin'),
    });
    L.crossHatch(ctx, nuc, {
      spacing: 6.5,
      crossSpacing: 8.5,
      width: 1.35,
      color: P.nucleusDeep,
      alpha: 0.66,
      layers: 2,
      length: [10, 30],
      gap: [2, 6],
      inset: 4,
      seed: sd('nucx'),
      density: (x, y) => sstep(-0.55, 0.95, ((x - CX) + (y - CY)) / (NR0 * 1.414)),
    });

    // 7. the nucleolus, a denser disc, drawn under the chromosomes so the count of four stays clear
    {
      const np = L.ellipsePts(NUCLEOLUS.x, NUCLEOLUS.y, NUCLEOLUS.r, NUCLEOLUS.r * 0.93, 28, 0.4);
      L.inkPath(ctx, np, {
        closed: true,
        width: 2.8,
        color: P.nucleusRim,
        alpha: 1,
        fill: P.nucleusDeep,
        seed: sd('nucleolus'),
        wobble: 1,
      });
      L.stipple(ctx, np, {
        spacing: 4.6,
        density: 0.55,
        r: [0.9, 1.6],
        color: P.nucleusRim,
        alpha: 0.5,
        seed: sd('nucleolusDots'),
      });
      // a single highlight crescent on the lit side
      ctx.save();
      ctx.beginPath();
      ctx.arc(NUCLEOLUS.x - 2, NUCLEOLUS.y - 2, NUCLEOLUS.r - 7, Math.PI * 1.05, Math.PI * 1.55);
      ctx.strokeStyle = P.nucleus;
      ctx.globalAlpha = 0.5;
      ctx.lineWidth = 3;
      ctx.lineCap = 'round';
      ctx.stroke();
      ctx.restore();
    }

    // 8. the four chromosomes: two pairs, drawn every frame so the count can always be followed
    for (let i = 0; i < CHROMO.length; i++) {
      drawWorm(ctx, L, P, CHROMO[i], sd('chromo', CHROMO[i].key), k, {});
    }

    // 9. the nuclear membrane, over the chromosomes, 4 px inkSoft, with its pores
    L.inkPath(ctx, nuc, {
      closed: true,
      width: 4,
      color: P.nucleusRim,
      seed: sd('nucrim'),
      wobble: 1.3,
      double: { width: 0.34, offset: 3, alpha: 0.3 },
    });
    {
      const pores = new Path2D();
      for (let i = 0; i < PORE_A.length; i++) {
        const a = PORE_A[i];
        const rr = NR0 + 8 * NUC_SHAPE(a);
        const c = Math.cos(a), s = Math.sin(a);
        // a short bar across the rim at each pore, tangent to it
        pores.moveTo(CX + c * rr - s * 6, CY + s * rr + c * 6);
        pores.lineTo(CX + c * rr + s * 6, CY + s * rr - c * 6);
      }
      ctx.save();
      ctx.strokeStyle = P.nucleus;
      ctx.globalAlpha = 0.85;
      ctx.lineWidth = 3.6;
      ctx.lineCap = 'butt';
      ctx.stroke(pores);
      ctx.restore();
    }

    // 10. the cell membrane last: 6 px ink, one continuous line, with an occasional doubled retrace.
    //     The pen wanders 4 px either way over long arcs, so the boundary is drawn, never compassed.
    L.inkPath(ctx, mem, Object.assign({ color: P.membrane, double: { width: 0.25, offset: 3.5, alpha: 0.4 } }, MEM_PEN));
  }

  // ---------------------------------------------------------------------------
  // Scene
  // ---------------------------------------------------------------------------

  FILM.scene({
    id: ID,
    draw(ctx, tIn, info) {
      const L = info.lib;
      const P = L.pal;
      const E = L.ease;
      // a transition can ask for t past the end: hold the final pose
      const t = clamp(tIn, 0, info.dur);
      const k = Math.floor(t * 12 + 1e-6); // the drawing index: characters move on twos

      // --- 0. the cream paper plate. The stripes cover every pixel of it, so it is drawn through a
      //        one-pixel clip: what matters is that lib's cached paper canvas exists before any of
      //        this shot's line work. That cached plate is the page's first offscreen canvas, and
      //        Chromium rasterises the main canvas differently before and after one exists, so
      //        without this the shot drew one way cold and another way after the rest of the film.
      ctx.save();
      ctx.beginPath();
      ctx.rect(0, 0, 1, 1);
      ctx.clip();
      L.paper(ctx);
      ctx.restore();

      // --- 1. stripes, full bleed and screen-fixed, drifting 1 px per frame ---
      L.stripes(ctx, {
        colors: [P.stripeCream, P.stripeYellow],
        width: 140,
        angle: -0.52,
        offset: 24 * info.T,
        seed: sd('stripes'),
      });

      // --- camera: a locked push-in from zoom 1.00 to 1.04 that keeps the cell centre on (540, 900) ---
      const zoom = 1 + 0.04 * E.inOutSine(info.dur > 0 ? t / info.dur : 0);
      const cam = { x: CX, y: CY + 60 / zoom, zoom };

      // --- the breathing radius (frame 0 sits exactly on G1) ---
      const R = R0 + breathAt(t);

      L.camera(ctx, cam, (ctx) => {
        // --- 2. neighbour cells, behind everything, quiet ---
        ctx.save();
        ctx.globalAlpha = 0.62;
        for (let i = 0; i < NEIGH_GEO.length; i++) drawNeighbour(ctx, L, P, NEIGH_GEO[i]);
        ctx.restore();

        // --- 3. the hero's contact shade on the tissue ---
        drawContactShade(ctx, L, P, R);

        // --- 4. construction geometry, over the tissue and under the hero ---
        drawConstruction(ctx, L, P);

        // --- 5. the hero cell ---
        drawHeroCell(ctx, L, P, R, k);

        // --- 6. overlays ---
        drawOverlays(ctx, L, P, E, t, R);
      });

      // --- 7. the shared cycle glyph: screen-fixed, always the last thing drawn ---
      L.cycleGlyph(ctx, info.T, 'illustrated');
    },
  });
})();
