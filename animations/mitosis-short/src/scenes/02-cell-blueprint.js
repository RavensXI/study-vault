// 02 cell-blueprint : "Inside — nucleus, 23 pairs, the cycle" (schematic, global T 2.0 to 4.5)
//
// The match cut from 01 lands on G1, so the cell outline, the nucleus, the four chromosomes, the
// six mitochondria and the neighbours are the storyboard's Shared geometry numbers, built with the
// wobble helpers 01-hero-cell.js publishes for its siblings (lumpy / lumpyRing / wormCentre, seeded
// LIB.hash('hero-cell', ...)), so the blueprint lands on the paper drawing's exact pixels.
// Camera locked at zoom 1; no text anywhere (art bible section 5).
//
// Layers, back to front:
//   1  near-black navyDeep, the dust the spark lights, then the blueprint plate fading in from T 2.25
//   2  guide geometry: circles r 470 and 640 at (540, 900) turning 6 degrees across the shot,
//      corner diagonals, construction axes, registration crosses, concentric cytoplasm arcs
//   3  measurement: height bracket x 900 (y 520 to 1280), width bracket y 1345 (x 160 to 920),
//      left tick scale x 60, an arc annotation on the nuclear rim — each popping on its own 16th
//   4  top specimen strip y 118 to 212: a row of cells in section, three of them mid-division
//   5  neighbour cells on G1, cut by the frame edges, lattice fragments below the safe area
//   6  the G1 cell: navy fill, ribosome stipple sweeping out, six mitochondria with cristae,
//      the double lavender outline drawing round from 12 o'clock
//   7  the nucleus: hex lattice at 18 px sweeping out from the centre, envelope with pore ticks,
//      the nucleolus, and the four lattice worm chromosomes (A long, B short) with glow-dot centres
//   8  the tally: 46 lineWhite ticks in 23 pairs along the r 300 arc, one magenta ring per pair
//   9  node glyphs: the nuclear envelope in section (left), one uncopied chromosome thread (right)
//  10  the opening spark, then the cycle glyph G5 (FILM.lib.cycleGlyph, the canonical helper)
//      arriving on T 4.0 behind a magenta ring
(function () {
  'use strict';

  const ID = 'cell-blueprint';
  const REF = 'hero-cell'; // G1 seeds come from shot 01, so the outline boils the same across the cut
  const TAU = Math.PI * 2;
  const DEG = Math.PI / 180;
  const FR = 1 / 24;

  const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
  const lerp = (a, b, u) => a + (b - a) * u;
  const sstep = (a, b, x) => {
    const u = clamp((x - a) / (b - a));
    return u * u * (3 - 2 * u);
  };

  // ---------------------------------------------------------------------------
  // Shared geometry G1 (docs/storyboard.md) — copied exactly
  // ---------------------------------------------------------------------------

  const CX = 540, CY = 900;
  const R_CELL = 380;  // mean radius, 40-point polyline with r = 380 + 14 * noise
  const R_NUC = 170;   // nucleus mean radius, same centre

  // Four chromosomes, two pairs: A long (130 px), B short (85 px); both members of a pair identical.
  // 20 degrees off horizontal, alternating left and right, so each pair mirrors about x = 540.
  const CHROMO = [
    { key: 'A1', x: 470, y: 850, len: 130, hw: 10.0, tilt: -20, pair: 0 },
    { key: 'A2', x: 610, y: 850, len: 130, hw: 10.0, tilt: 20, pair: 0 },
    { key: 'B1', x: 480, y: 955, len: 85, hw: 8.5, tilt: -20, pair: 1 },
    { key: 'B2', x: 600, y: 955, len: 85, hw: 8.5, tilt: 20, pair: 1 },
  ];

  // Six mitochondria, 60 by 28 px beans
  const MITO = [[300, 700], [760, 720], [280, 1060], [790, 1080], [420, 1190], [660, 640]];
  const MITO_W = 60, MITO_H = 28;

  // Nucleolus: the denser disc 01 draws at (500, 870), radius 27
  const NUCLEOLUS = [500, 870, 27];

  // Neighbour cells: partial circles cut by the frame edge, radius 300 to 360.
  // Centres, radii and the seed index k are 01's, so the field does not shift at the cut.
  const NEIGH = [
    [60, 380, 318, 1], [1020, 420, 330, 2], [40, 1420, 326, 3], [1040, 1400, 336, 4], [540, 1690, 344, 5],
  ];

  // The tally: 46 ticks in 23 pairs on an arc of radius 300 around the nucleus,
  // from 8 o'clock clockwise (over the top) to 4 o'clock — a 240 degree sweep.
  const TAL = { r: 300, a0: 150 * DEG, span: 240 * DEG, n: 23, gap: 3.5 * DEG, len: 21 };

  // Network node glyphs, 116 px across, inside the safe area
  const NODE_L = { cx: 182, cy: 1452, r: 58, sr: 36 };
  const NODE_R = { cx: 878, cy: 1452, r: 58, sr: 40 };

  // ---------------------------------------------------------------------------
  // Geometry, built once: a pure function of the constants above
  // ---------------------------------------------------------------------------

  function cumLen(pts) {
    const c = new Float64Array(pts.length);
    for (let i = 1; i < pts.length; i++) c[i] = c[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    return c;
  }

  function slicePts(pts, cum, frac) {
    if (frac >= 1) return pts;
    if (frac <= 0) return [];
    const target = cum[cum.length - 1] * clamp(frac);
    const out = [];
    for (let i = 0; i < pts.length; i++) {
      if (cum[i] <= target) out.push(pts[i]);
      else {
        const a = pts[i - 1];
        const u = (target - cum[i - 1]) / (cum[i] - cum[i - 1] || 1);
        out.push([lerp(a[0], pts[i][0], u), lerp(a[1], pts[i][1], u)]);
        break;
      }
    }
    return out;
  }

  // The G1 outline. 01-hero-cell.js publishes the convention every sibling must seed the same way
  // (its header: LIB.hash('hero-cell', 'membrane') and 'nucleus'), so lumpy and lumpyRing are copied
  // from it verbatim and the blueprint outline lands on the paper outline's exact pixels.
  function lumpy(L, seed) {
    const r = L.rng(seed);
    const p1 = r.range(0, TAU), p2 = r.range(0, TAU), p3 = r.range(0, TAU), p4 = r.range(0, TAU);
    const w1 = r.range(0.52, 0.66), w2 = r.range(0.3, 0.42), w3 = r.range(0.14, 0.22), w4 = r.range(0.07, 0.12);
    const norm = w1 + w2 + w3 + w4;
    return (a) =>
      (w1 * Math.sin(2 * a + p1) + w2 * Math.sin(3 * a + p2) + w3 * Math.sin(5 * a + p3) + w4 * Math.sin(8 * a + p4)) / norm;
  }

  // start turns the list so the pen begins at 12 o'clock; the radius depends only on the absolute
  // angle, so the curve itself is identical to 01's whatever point the list starts from.
  function lumpyRing(cx, cy, R, amp, n, shape, start) {
    const out = [];
    const s = start || 0;
    for (let i = 0; i < n; i++) {
      const a = s + (i / n) * TAU;
      const rr = R + amp * shape(a);
      out.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]);
    }
    return out;
  }

  // a closed point ring resampled fine, with the first point repeated so it can be drawn on
  function openLoop(L, pts, step) {
    const s = L.smoothPts(pts, true, step || 4);
    s.push(s[0]);
    return s;
  }

  // One worm chromosome, uncondensed: a slack thread that drifts off its own axis. Copied from
  // 01-hero-cell.js (wormCentre) with 01's seeds, so the same four threads carry across the cut.
  // `k` is the drawing index on twos, so the thread trembles twelve times a second and holds between.
  function wormCentre(L, c, len, deg, seed, k, trem) {
    const a = deg * DEG;
    const ca = Math.cos(a), sa = Math.sin(a);
    const N = 20;
    const raw = [];
    const off = (u) => len * 0.16 * L.noise1(u * 2.6 + 1.7, seed) + len * 0.07 * L.noise1(u * 6.1 + 0.3, seed + 3);
    const v0 = off(0);
    for (let i = 0; i <= N; i++) {
      const u = i / N - 0.5;
      const s = u * len;
      // the ends are free to swing, the middle barely moves: a thread, not a rigid bar
      const swing = trem * (0.35 + 1.5 * u * u);
      const v = off(u) - v0 + (L.h3(i * 7 + 1, k, seed) - 0.5) * 2 * swing;
      raw.push([c[0] + s * ca - v * sa, c[1] + s * sa + v * ca]);
    }
    return L.smoothPts(raw, false, 3);
  }

  function normalsOf(spine) {
    const n = spine.length;
    const out = [];
    for (let i = 0; i < n; i++) {
      const a = spine[Math.max(0, i - 1)], b = spine[Math.min(n - 1, i + 1)];
      const tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      out.push([-ty / tl, tx / tl, tx / tl, ty / tl]);
    }
    return out;
  }

  // closed band round a spine with round caps
  function bandPoly(spine, nrm, wAt) {
    const n = spine.length;
    const inner = [], outer = [];
    for (let i = 0; i < n; i++) {
      const w = wAt(i / (n - 1));
      inner.push([spine[i][0] + nrm[i][0] * w, spine[i][1] + nrm[i][1] * w]);
      outer.push([spine[i][0] - nrm[i][0] * w, spine[i][1] - nrm[i][1] * w]);
    }
    const capEnd = [], capStart = [];
    const pe = spine[n - 1], ne = nrm[n - 1], we = wAt(1);
    for (let j = 1; j < 9; j++) {
      const a = (j / 9) * Math.PI;
      capEnd.push([pe[0] + ne[0] * we * Math.cos(a) + ne[2] * we * Math.sin(a), pe[1] + ne[1] * we * Math.cos(a) + ne[3] * we * Math.sin(a)]);
    }
    const ps = spine[0], ns = nrm[0], ws = wAt(0);
    for (let j = 1; j < 9; j++) {
      const a = (j / 9) * Math.PI;
      capStart.push([ps[0] - ns[0] * ws * Math.cos(a) - ns[2] * ws * Math.sin(a), ps[1] - ns[1] * ws * Math.cos(a) - ns[3] * ws * Math.sin(a)]);
    }
    return inner.concat(capEnd, outer.slice().reverse(), capStart);
  }

  // Everything drawn for one worm chromosome at drawing index k: the thread, the band round it,
  // the lattice rungs across the band and the dotted fibre down the middle. Pure in (ch, k).
  function wormParts(L, ch, k, S0) {
    const c = ch.c;
    const spine = wormCentre(L, [c.x, c.y], c.len, c.tilt, ch.wseed, k, 2.6);
    const nrm = normalsOf(spine);
    const poly = bandPoly(spine, nrm, ch.wAt);
    const cum = cumLen(spine);
    const total = cum[cum.length - 1] || 1;
    const at = (s) => {
      let i = 0;
      while (i < spine.length - 2 && cum[i + 1] < s) i++;
      const u = clamp((s - cum[i]) / (cum[i + 1] - cum[i] || 1));
      return {
        p: [lerp(spine[i][0], spine[i + 1][0], u), lerp(spine[i][1], spine[i + 1][1], u)],
        n: nrm[i],
        u: (cum[i] + (cum[i + 1] - cum[i]) * u) / total,
      };
    };
    const rungs = [];
    for (let s = 7, j = 0; s < total - 6; s += 11, j++) {
      const q = at(s);
      const w = ch.wAt(q.u) * 0.8;
      const bow = (L.h3(j, ch.seed, S0 + 41) - 0.5) * 2.2;
      rungs.push({
        p0: [q.p[0] + q.n[0] * w, q.p[1] + q.n[1] * w],
        cm: [q.p[0] + q.n[2] * bow, q.p[1] + q.n[3] * bow],
        p1: [q.p[0] - q.n[0] * w, q.p[1] - q.n[1] * w],
      });
    }
    const thread = [];
    for (let s = 4; s < total - 3; s += 6) {
      const q = at(s);
      const off = Math.sin(s * 0.28 + ch.seed) * ch.wAt(q.u) * 0.32;
      thread.push([q.p[0] + q.n[0] * off, q.p[1] + q.n[1] * off]);
    }
    return { spine, poly, rungs, thread };
  }

  // a mitochondrion: an ellipse bent into a bean, plus cristae across its short axis
  function beanPts(cx, cy, w, h, rot, bend, n) {
    const out = [];
    const cr = Math.cos(rot), sr = Math.sin(rot);
    for (let i = 0; i < n; i++) {
      const a = (i / n) * TAU;
      const x = Math.cos(a) * (w / 2);
      let y = Math.sin(a) * (h / 2);
      y += bend * (Math.pow(x / (w / 2), 2) - 0.45);
      out.push([cx + x * cr - y * sr, cy + x * sr + y * cr]);
    }
    return out;
  }

  let GEO = null;
  function geo(L) {
    if (GEO) return GEO;
    const g = {};
    const S0 = L.hash(ID) & 0xffff;

    // ---- the cell outline: G1, with 01's membrane shape ---------------------
    const TOP = -Math.PI / 2;
    const MEM = lumpy(L, L.hash(REF, 'membrane') & 0x7fffffff);
    const NUC = lumpy(L, L.hash(REF, 'nucleus') & 0x7fffffff);
    g.mem = MEM;
    g.cell40 = lumpyRing(CX, CY, R_CELL, 14, 40, MEM, TOP);
    g.out = openLoop(L, g.cell40, 4);
    g.cumOut = cumLen(g.out);
    g.in = openLoop(L, lumpyRing(CX, CY, R_CELL - 9, 14, 40, MEM, TOP), 4);
    g.cumIn = cumLen(g.in);
    g.poly = L.smoothPts(g.cell40, true, 12);           // coarse, for clips and containment
    g.polyIn = L.smoothPts(lumpyRing(CX, CY, R_CELL - 13, 14, 40, MEM, TOP), true, 12);

    // ---- the nucleus (01 draws it at amplitude 8 over 32 points) -------------
    g.nuc32 = lumpyRing(CX, CY, R_NUC, 8, 32, NUC, TOP);
    g.nucOut = openLoop(L, g.nuc32, 3);
    g.cumNuc = cumLen(g.nucOut);
    g.nucIn = openLoop(L, lumpyRing(CX, CY, R_NUC - 9, 8, 32, NUC, TOP), 3);
    g.nucPoly = L.smoothPts(g.nuc32, true, 9);
    g.nucPolyIn = L.smoothPts(lumpyRing(CX, CY, R_NUC - 12, 8, 32, NUC, TOP), true, 9);

    // nuclear pores: 26 rim marks, each a gap between two short posts
    g.pores = [];
    for (let i = 0; i < 26; i++) {
      const a = TOP + (i / 26) * TAU + (L.h3(i, 5, S0) - 0.5) * 0.06;
      g.pores.push({ a, r: R_NUC + 8 * NUC(a), big: i % 3 === 0 });
    }

    // ---- the four chromosomes ----------------------------------------------
    // The thread itself is rebuilt per drawing (it trembles on twos with 01's seeds); everything
    // that does not move lives here.
    g.chromo = CHROMO.map((c) => ({
      c,
      wAt: (u) => c.hw * (0.80 + 0.20 * Math.sin(Math.PI * u)),
      wseed: L.hash(REF, 'chromo', c.key) & 0x7fffffff,
      seed: L.hash(ID, 'chromo', c.key) & 0xffff,
    }));

    // ---- mitochondria ------------------------------------------------------
    g.mito = MITO.map((m, i) => {
      const rot = Math.atan2(m[1] - CY, m[0] - CX) + Math.PI / 2 + (L.h3(i, 3, S0 + 11) - 0.5) * 0.9;
      const bend = 5 + 3 * L.h3(i, 7, S0 + 12);
      const pts = beanPts(m[0], m[1], MITO_W, MITO_H, rot, bend, 44);
      // cristae: short folds across the short axis, alternating from each wall
      const cr = [];
      const ct = Math.cos(rot), st = Math.sin(rot);
      const nC = 6;
      for (let j = 0; j < nC; j++) {
        const u = (j + 0.5) / nC;
        const x = (u - 0.5) * MITO_W * 0.76;
        const yb = bend * (Math.pow(x / (MITO_W / 2), 2) - 0.45);
        const side = j % 2 ? 1 : -1;
        const h = MITO_H * (0.30 + 0.16 * L.h3(i, j, S0 + 13));
        const p0 = [x, yb + side * MITO_H * 0.40];
        const p1 = [x + (L.h3(j, i, S0 + 14) - 0.5) * 5, yb + side * (MITO_H * 0.40 - h)];
        const to = (p) => [m[0] + p[0] * ct - p[1] * st, m[1] + p[0] * st + p[1] * ct];
        cr.push([to(p0), to(p1)]);
      }
      return { pts, cr, x: m[0], y: m[1], seed: S0 + 60 + i * 13 };
    });

    // ---- neighbour cells: 01's table, shapes and seeds ----------------------
    g.neigh = NEIGH.map((nb) => {
      const s = L.hash(REF, 'neigh', nb[3]) & 0x7fffffff;
      const shape = lumpy(L, s);
      // each neighbour's nucleus leans toward the hero cell, as 01 places them
      let dx = CX - nb[0], dy = CY - nb[1];
      const dl = Math.hypot(dx, dy) || 1;
      dx /= dl;
      dy /= dl;
      const nx = nb[0] + dx * nb[2] * 0.32, ny = nb[1] + dy * nb[2] * 0.32;
      return {
        x: nb[0], y: nb[1], r: nb[2], nx, ny, nr: nb[2] * 0.28,
        poly: L.smoothPts(lumpyRing(nb[0], nb[1], nb[2], 15, 36, shape), true, 10),
        nuc: L.smoothPts(lumpyRing(nx, ny, nb[2] * 0.28, 9, 26, lumpy(L, s + 11)), true, 8),
        low: nb[1] > 1200,
        seed: (s & 0xffff) + 5,
      };
    });

    // ---- membrane detail: short rungs just inside the outline, and radial spokes ----
    g.memTicks = [];
    for (let i = 0; i < 76; i++) {
      const a = TOP + (i / 76) * TAU;
      // tone per rung, rounded so the whole ring strokes in a handful of passes
      const al = Math.round((0.17 + 0.2 * L.h3(i, 11, S0 + 72)) * 20) / 20;
      g.memTicks.push({ a, r: R_CELL + 14 * MEM(a), len: 7 + 6 * L.h3(i, 3, S0 + 71), u: i / 76, big: i % 6 === 0, al });
    }
    g.spokes = [];
    for (let i = 0; i < 24; i++) {
      const a = TOP + (i / 24) * TAU + 0.0654;
      g.spokes.push({ a, r0: 196 + 10 * L.h3(i, 9, S0 + 73), r1: R_CELL - 34 + 14 * MEM(a) });
    }

    // ---- the tally: 23 pairs on the r 300 arc ------------------------------
    g.tally = [];
    for (let i = 0; i < TAL.n; i++) {
      const am = TAL.a0 + ((i + 0.5) / TAL.n) * TAL.span;
      g.tally.push({
        am,
        a: [am - TAL.gap / 2, am + TAL.gap / 2],
        mx: CX + Math.cos(am) * (TAL.r + TAL.len / 2),
        my: CY + Math.sin(am) * (TAL.r + TAL.len / 2),
      });
    }

    // ---- top specimen strip: cells in section, three of them dividing ------
    g.strip = [];
    {
      const r = L.rng(L.hash(ID, 'strip'));
      let x = -16, i = 0;
      while (x < 1110) {
        const rr = r.range(11, 25);
        const y = r.range(148, 180);
        const div = i % 6 === 2 ? r.range(0.42, 0.95) : 0;
        g.strip.push({ x: x + rr, y, r: rr, div, seed: (L.hash(ID, 'strip', i) & 0xffff) });
        x += rr * 2 + r.range(8, 26);
        i++;
      }
    }

    // ---- the dust the spark lights before the plate comes up ----------------
    // Each speck is its own fill so it can carry its own tone and twinkle; the field also keeps the
    // opening frame a real drawing rather than a bare fill.
    g.dust = [];
    {
      const r = L.rng(L.hash(ID, 'dust'));
      for (let i = 0; i < 280; i++) {
        const x = r.range(-20, 1100), y = r.range(-20, 1940);
        const d = Math.hypot(x - CX, y - CY);
        const lit = 1 - sstep(120, 880, d);
        g.dust.push({
          x, y,
          r: 0.7 + 1.5 * r() * (0.5 + 0.5 * lit),
          a: (0.08 + 0.34 * lit) * r.range(0.6, 1.2),
          hot: r() < 0.3,
          ang: Math.atan2(y - CY, x - CX),
        });
      }
    }

    // ---- lead-line sources for the two node glyphs -------------------------
    // left: a point on the nuclear envelope, lower left; right: chromosome A2
    const aL = 137 * DEG;
    g.srcL = [CX + Math.cos(aL) * R_NUC, CY + Math.sin(aL) * R_NUC];
    g.srcR = [CHROMO[1].x, CHROMO[1].y];

    GEO = g;
    return g;
  }

  // ---------------------------------------------------------------------------
  // Line helpers
  // ---------------------------------------------------------------------------

  // polyline displaced along its normal by a low-frequency noise that changes with the boil
  function wobPts(L, pts, seed, amp, bi) {
    const n = pts.length;
    const out = new Array(n);
    let s = 0;
    const sd = (seed + bi * 7919) | 0;
    for (let i = 0; i < n; i++) {
      const p = pts[i];
      if (i > 0) s += Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]);
      const a = pts[i > 0 ? i - 1 : 0], b = pts[i < n - 1 ? i + 1 : n - 1];
      const tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      const d = amp * L.noise1(s * 0.018, sd);
      out[i] = [p[0] - (ty / tl) * d, p[1] + (tx / tl) * d];
    }
    return out;
  }

  function addPoly(path, pts, closed, dx, dy) {
    if (!pts || pts.length < 2) return;
    const ox = dx || 0, oy = dy || 0;
    path.moveTo(pts[0][0] + ox, pts[0][1] + oy);
    for (let i = 1; i < pts.length; i++) path.lineTo(pts[i][0] + ox, pts[i][1] + oy);
    if (closed) path.closePath();
  }

  function wob(L, path, pts, seed, amp, bi, closed) {
    if (!pts || pts.length < 2) return;
    addPoly(path, wobPts(L, pts, seed, amp, bi), closed);
  }

  function stroke(ctx, path, color, alpha, width, dash) {
    if (alpha <= 0.004) return;
    ctx.save();
    ctx.strokeStyle = color;
    ctx.globalAlpha *= alpha;
    ctx.lineWidth = width;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    if (dash) ctx.setLineDash(dash);
    ctx.stroke(path);
    ctx.restore();
  }

  function fill(ctx, path, color, alpha) {
    if (alpha <= 0.004) return;
    ctx.save();
    ctx.fillStyle = color;
    ctx.globalAlpha *= alpha;
    ctx.fill(path);
    ctx.restore();
  }

  // paths grouped by alpha so each tone is one stroke call
  function bucket(map, a) {
    let p = map.get(a);
    if (!p) {
      p = new Path2D();
      map.set(a, p);
    }
    return p;
  }
  function strokeBuckets(ctx, map, color, width, mul) {
    const m = mul == null ? 1 : mul;
    for (const [a, p] of map) if (a * m > 0.004) stroke(ctx, p, color, a * m, width);
  }

  function arcPath(path, cx, cy, r, a0, a1, step) {
    const n = Math.max(2, Math.ceil(Math.abs(a1 - a0) / (step || 0.05)));
    for (let i = 0; i <= n; i++) {
      const a = a0 + ((a1 - a0) * i) / n;
      const x = cx + Math.cos(a) * r, y = cy + Math.sin(a) * r;
      if (i === 0) path.moveTo(x, y);
      else path.lineTo(x, y);
    }
  }

  function seg(t, a, frames, e) {
    const u = clamp((t - a) / (frames * FR));
    if (u <= 1e-5) return 0; // outBack returns about 1e-16 at 0, which would draw a speck
    return e ? e(u) : u;
  }

  // ---------------------------------------------------------------------------
  // The top specimen strip (decorative, above the safe area)
  // ---------------------------------------------------------------------------

  function drawStrip(ctx, L, P, g, bi, k) {
    if (k <= 0) return;
    const lav = P.lavender, white = P.lineWhite;
    const xr = -20 + 1120 * clamp(k * 1.15);
    ctx.save();
    ctx.beginPath();
    ctx.rect(0, 108, xr, 118);
    ctx.clip();

    // the band ground, a shade lighter than the plate
    ctx.fillStyle = P.navyLight;
    ctx.globalAlpha = 0.30;
    ctx.fillRect(-10, 118, 1100, 94);
    ctx.globalAlpha = 1;

    // rules top and bottom
    const rules = new Path2D();
    wob(L, rules, [[-10, 119], [360, 119], [720, 119], [1090, 119]], 1201, 0.5, bi, false);
    stroke(ctx, rules, lav, 0.34, 1.2);
    const rule2 = new Path2D();
    wob(L, rule2, [[-10, 211], [360, 211], [720, 211], [1090, 211]], 1202, 0.5, bi, false);
    stroke(ctx, rule2, lav, 0.55, 1.8);
    L.ticks(ctx, -10, 211, { length: 1100, angle: 0, n: 55, len: 6, major: 5, majorLen: 12, side: -1, baseline: false, color: white, alpha: 0.32, width: 1 });

    // cells in section, a few of them pinched in two
    const cells = new Path2D();
    const nucs = new Path2D();
    for (const s of g.strip) {
      const jb = (L.h3(s.seed, bi, 3) - 0.5) * 0.7;
      if (s.div > 0) {
        const rr = s.r * 0.86;
        const dx = s.r * s.div;
        cells.moveTo(s.x - dx + rr, s.y + jb);
        cells.arc(s.x - dx, s.y + jb, rr, 0, TAU);
        cells.moveTo(s.x + dx + rr, s.y + jb);
        cells.arc(s.x + dx, s.y + jb, rr, 0, TAU);
        nucs.moveTo(s.x - dx + rr * 0.34, s.y + jb);
        nucs.arc(s.x - dx, s.y + jb, rr * 0.34, 0, TAU);
        nucs.moveTo(s.x + dx + rr * 0.34, s.y + jb);
        nucs.arc(s.x + dx, s.y + jb, rr * 0.34, 0, TAU);
      } else {
        cells.moveTo(s.x + s.r, s.y + jb);
        cells.ellipse(s.x, s.y + jb, s.r, s.r * 0.88, 0, 0, TAU);
        nucs.moveTo(s.x + s.r * 0.32, s.y + jb);
        nucs.arc(s.x, s.y + jb, s.r * 0.32, 0, TAU);
      }
    }
    stroke(ctx, cells, lav, 0.34, 1);
    fill(ctx, nucs, lav, 0.30);

    // a sparse tissue stipple between them
    L.stipple(ctx, null, {
      bounds: [-10, 122, 1100, 86],
      spacing: 13,
      r: [1.0, 1.7],
      color: lav,
      alpha: 0.22,
      density: 0.5,
      seed: 1207,
    });

    // registration lozenges at both ends of the band
    const lz = new Path2D();
    for (const sgn of [1, -1]) {
      const x0 = sgn > 0 ? 16 : 1064;
      lz.moveTo(x0, 155);
      lz.lineTo(x0 + sgn * 17, 165);
      lz.lineTo(x0, 175);
      lz.closePath();
    }
    fill(ctx, lz, lav, 0.45);
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // Neighbour cells (G1 positions), cut by the frame edges
  // ---------------------------------------------------------------------------

  function drawNeighbours(ctx, L, P, g, bi, k) {
    if (k <= 0) return;
    const lav = P.lavender, white = P.lineWhite;
    for (const nb of g.neigh) {
      const p = new Path2D();
      wob(L, p, nb.poly, nb.seed, 0.8, bi, true);
      const pn = new Path2D();
      wob(L, pn, nb.nuc, nb.seed + 7, 0.6, bi, true);
      ctx.save();
      ctx.globalAlpha = k;
      fill(ctx, p, P.navy, 0.4);
      // their own cytoplasm grain, thin enough to stay behind the hero cell
      L.stipple(ctx, nb.poly, { spacing: 15, r: [1.0, 1.8], color: lav, alpha: 0.13, density: 0.5, seed: nb.seed + 41 });
      stroke(ctx, p, lav, 0.32, 1.6);
      fill(ctx, pn, P.navyLight, 0.3);
      stroke(ctx, pn, lav, 0.26, 1.2);
      // a pair of chromosome marks in each neighbour nucleus: every cell carries the same set
      const cm = new Path2D();
      const rr = nb.r * 0.42;
      for (let j = 0; j < 4; j++) {
        const a = (j / 4) * TAU + nb.seed * 0.001;
        const cx = nb.x + Math.cos(a) * rr * 0.45;
        const cy = nb.y - nb.r * 0.08 + Math.sin(a) * rr * 0.45;
        const th = a + Math.PI / 2;
        cm.moveTo(cx - Math.cos(th) * 13, cy - Math.sin(th) * 13);
        cm.quadraticCurveTo(cx + Math.sin(th) * 5, cy - Math.cos(th) * 5, cx + Math.cos(th) * 13, cy + Math.sin(th) * 13);
      }
      stroke(ctx, cm, white, 0.18, 1.4);
      if (nb.low) {
        // below the safe area the neighbours show their lattice, so the field reads as tissue
        L.hexLattice(ctx, nb.poly, { r: 15, alpha: 0.075, width: 1, color: lav, seed: nb.seed + 21, jitter: 1.2 });
      }
      ctx.restore();
    }
  }

  // ---------------------------------------------------------------------------
  // A network node glyph: a lead line from a source region out to a small round plate
  // ---------------------------------------------------------------------------

  function nodeGlyph(ctx, L, P, o, content) {
    const k = clamp(o.k);
    if (k <= 0) return;
    const lav = P.lavender;
    const dx = o.cx - o.sx, dy = o.cy - o.sy;
    const dl = Math.hypot(dx, dy) || 1;
    const ux = dx / dl, uy = dy / dl;
    const ax = o.sx + ux * o.sr, ay = o.sy + uy * o.sr;
    const bx = o.cx - ux * (o.r + 6), by = o.cy - uy * (o.r + 6);
    const mx = (ax + bx) / 2 + uy * o.bow, my = (ay + by) / 2 - ux * o.bow;
    const lead = [];
    for (let i = 0; i <= 26; i++) {
      const u = (i / 26) * k, v = 1 - u;
      lead.push([v * v * ax + 2 * v * u * mx + u * u * bx, v * v * ay + 2 * v * u * my + u * u * by]);
    }
    const lp = new Path2D();
    wob(L, lp, lead, o.seed, 0.5, o.bi, false);
    stroke(ctx, lp, lav, 0.42, 1.2);

    // the dashed ring round the region being magnified
    const sp = new Path2D();
    sp.arc(o.sx, o.sy, o.sr * Math.min(1, k * 1.3), 0, TAU);
    stroke(ctx, sp, lav, 0.45, 1.2, [4, 5]);

    ctx.save();
    ctx.translate(o.cx, o.cy);
    ctx.scale(k, k);
    ctx.beginPath();
    ctx.arc(0, 0, o.r, 0, TAU);
    ctx.fillStyle = P.navy;
    ctx.globalAlpha = 0.95;
    ctx.fill();
    ctx.fillStyle = P.navyLight;
    ctx.globalAlpha = 0.5;
    ctx.fill();
    ctx.globalAlpha = 1;
    const rim = new Path2D();
    wob(L, rim, L.ellipsePts(0, 0, o.r, o.r, 64), o.seed + 1, 0.4, o.bi, true);
    stroke(ctx, rim, lav, 0.85, 2);
    const rim2 = new Path2D();
    rim2.arc(0, 0, o.r - 7, 0, TAU);
    stroke(ctx, rim2, lav, 0.3, 1);
    L.ticks(ctx, 0, 0, { r: o.r + 3, n: 36, len: 5, major: 9, majorLen: 10, color: lav, alpha: 0.35, width: 1, rot: o.rot });
    ctx.beginPath();
    ctx.arc(0, 0, o.r - 8, 0, TAU);
    ctx.clip();
    content(ctx);
    ctx.restore();
  }

  // left node: the nuclear envelope in section — two membranes with pores between them
  function nodeEnvelope(ctx, L, P, bi, tk) {
    const lav = P.lavender, white = P.lineWhite;
    const wave = (y, amp, ph) => {
      const pts = [];
      for (let x = -62; x <= 62; x += 4) pts.push([x, y + amp * Math.sin(x * 0.055 + ph)]);
      return pts;
    };
    // cytoplasm grain above the envelope, nucleoplasm lattice below it
    L.stipple(ctx, null, { bounds: [-60, -60, 120, 44], spacing: 8, r: [1.0, 1.7], color: lav, alpha: 0.34, density: 0.6, seed: 2101 });
    L.hexLattice(ctx, (c) => c.rect(-60, 14, 120, 52), { bounds: [-60, 14, 120, 52], r: 10, alpha: 0.42, width: 1, color: lav, seed: 2102 });

    const PORE = [-34, 4, 40];
    const outerP = new Path2D(), innerP = new Path2D();
    const gap = 11;
    const pieces = (y, amp, ph, path) => {
      const pts = wave(y, amp, ph);
      let run = [];
      for (const p of pts) {
        const near = PORE.some((px) => Math.abs(p[0] - px) < gap);
        if (near) {
          if (run.length > 1) addPoly(path, wobPts(L, run, 2103 + y, 0.4, bi), false);
          run = [];
        } else run.push(p);
      }
      if (run.length > 1) addPoly(path, wobPts(L, run, 2104 + y, 0.4, bi), false);
    };
    pieces(-11, 2.6, 0.6, outerP);
    pieces(11, 2.6, 0.2, innerP);
    stroke(ctx, outerP, white, 0.9, 2.4);
    stroke(ctx, innerP, white, 0.8, 2.4);

    // each pore: the two membranes joining, with the pore ring seen edge-on
    const pr = new Path2D();
    const rings = new Path2D();
    for (const px of PORE) {
      pr.moveTo(px - gap, -11 + 2.6 * Math.sin((px - gap) * 0.055 + 0.6));
      pr.quadraticCurveTo(px - gap + 3, 0, px - gap, 11 + 2.6 * Math.sin((px - gap) * 0.055 + 0.2));
      pr.moveTo(px + gap, -11 + 2.6 * Math.sin((px + gap) * 0.055 + 0.6));
      pr.quadraticCurveTo(px + gap - 3, 0, px + gap, 11 + 2.6 * Math.sin((px + gap) * 0.055 + 0.2));
      // the pore ring seen edge-on: a short post each side of the channel
      rings.moveTo(px - gap, -17);
      rings.lineTo(px - gap, -12);
      rings.moveTo(px + gap, -17);
      rings.lineTo(px + gap, -12);
      rings.moveTo(px - gap, 17);
      rings.lineTo(px - gap, 12);
      rings.moveTo(px + gap, 17);
      rings.lineTo(px + gap, 12);
    }
    stroke(ctx, pr, lav, 0.85, 1.8);
    stroke(ctx, rings, lav, 0.6, 1.8);

    // a bracket across the two membranes
    L.bracket(ctx, 52, -11, 52, 11, { offset: 0, cap: 10, width: 1.2, alpha: 0.6, color: lav });
    // three particles drifting through the middle pore, stepping on the boil
    const dots = new Path2D();
    for (let i = 0; i < 3; i++) {
      const u = ((bi + i * 4) % 12) / 12;
      const y = lerp(-28, 28, u);
      dots.moveTo(PORE[1] + 2.6, y);
      dots.arc(PORE[1], y, 2.6, 0, TAU);
    }
    fill(ctx, dots, P.glow, 0.6 * tk);
  }

  // right node: one chromosome before the copy — a single coiled thread, not yet two
  function nodeThread(ctx, L, P, bi, tint) {
    const lav = P.lavender, white = P.lineWhite;
    L.hexLattice(ctx, (c) => c.arc(0, 0, 54, 0, TAU), { bounds: [-54, -54, 108, 108], r: 11, alpha: 0.14, width: 1, color: lav, seed: 2201 });
    // the coil: one fibre wound round a shallow axis running lower-left to upper-right
    const th = -20 * DEG, ct = Math.cos(th), st = Math.sin(th);
    // the turns nearest the viewer are drawn solid, the far half faint, so it reads as a coil
    // wound round its axis rather than as a flat wave
    const coil = [];
    for (let i = 0; i <= 180; i++) {
      const u = i / 180;
      const s = lerp(-44, 44, u);
      const ph = u * TAU * 3.2 + (bi % 12) * 0.02;
      const env = 17 * Math.sin(Math.PI * clamp(u * 1.08 - 0.04));
      const off = env * Math.sin(ph);
      coil.push([s * ct - off * st, s * st + off * ct, Math.cos(ph)]);
    }
    const front = new Path2D(), back = new Path2D();
    let run = [], side = coil[0][2] > 0;
    for (const p of coil) {
      const sNow = p[2] > 0;
      if (sNow !== side) {
        addPoly(side ? front : back, run, false);
        run = [run[run.length - 1]].filter(Boolean);
        side = sNow;
      }
      run.push([p[0], p[1]]);
    }
    addPoly(side ? front : back, run, false);
    const halo = new Path2D();
    addPoly(halo, coil.map((p) => [p[0], p[1]]), false);
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    stroke(ctx, halo, tint, 0.13, 11);
    ctx.restore();
    stroke(ctx, back, tint, 0.38, 2);
    stroke(ctx, front, tint, 0.95, 3);
    // the axis it is wound on, and end ticks
    const ax = new Path2D();
    ax.moveTo(-46 * ct, -46 * st);
    ax.lineTo(46 * ct, 46 * st);
    stroke(ctx, ax, lav, 0.3, 1, [5, 6]);
    const et = new Path2D();
    for (const sgn of [-1, 1]) {
      const x = 46 * sgn * ct, y = 46 * sgn * st;
      et.moveTo(x + st * 9, y - ct * 9);
      et.lineTo(x - st * 9, y + ct * 9);
    }
    stroke(ctx, et, white, 0.55, 1.4);
    // one thread, so one centre mark
    L.glowDot(ctx, 0, 0, 4.5, { rays: 0, glow: 4, intensity: 0.8, seed: 2203 });
  }

  // ---------------------------------------------------------------------------
  // Scene
  // ---------------------------------------------------------------------------

  FILM.scene({
    id: ID,
    draw(ctx, tIn, info) {
      const L = info.lib, P = L.pal, E = L.ease;
      const dur = info.dur;
      // snap near-frame times onto the frame grid (plus a hair) so beat tests never miss by one ulp
      let t = clamp(tIn, 0, dur);
      const tFrame = Math.round(t * 24) / 24;
      if (Math.abs(t - tFrame) < 1e-4) t = tFrame + 1e-7;
      const bi = L.boil(info.T);
      const g = geo(L);
      const SEED = L.hash(ID) & 0xffff;

      const lav = P.lavender, white = P.lineWhite, mag = P.magenta, glow = P.glow;
      const tintA = P.schemBlue, tintB = P.schemRust;

      // ---- beats (shot-local seconds; global T in the comments) -------------
      const B_SPARK = 0;      // T 2.000  near-black, one white spark at the nucleus centre
      const B_BUILD = 0.25;   // T 2.250  plate, guides and the cell outline
      const B_NUC = 0.5;      // T 2.500  the nucleus lattice sweeps out
      const B_CH = [0.5, 0.625, 0.75, 0.875]; // T 2.500 to 2.875, one chromosome per 16th
      const B_MEAS = 0.75;    // T 2.750  height bracket
      const B_MEAS2 = 0.875;  // T 2.875  width bracket
      const B_NODE = 1.0;     // T 3.000  node glyphs open
      const B_TALLY = 1.0;    // T 3.000  the 23 pairs start
      const TALLY_END = 1.75; // T 3.750  and finish
      const B_GLYPH = 2.0;    // T 4.000  the cycle glyph arrives

      const PAIR_DT = (TALLY_END - B_TALLY) / TAL.n;

      // progress that is already visible on the beat frame itself
      const hit = (a, frames, e, lead) => {
        if (t < a) return 0;
        const u = clamp((t - a) / (frames * FR) + (lead == null ? 1 : lead) / frames);
        return e ? e(u) : u;
      };
      const pop = (a) => hit(a, 3, E.outBack);

      // ---- 1 base ------------------------------------------------------------
      ctx.fillStyle = P.navyDeep;
      ctx.fillRect(0, 0, 1080, 1920);
      // the spark lights the plate before the plate exists
      const preSpark = 1 - sstep(B_BUILD, B_BUILD + 5 * FR, t);
      if (preSpark > 0) {
        ctx.save();
        ctx.globalCompositeOperation = 'lighter';
        const gl = ctx.createRadialGradient(CX, CY, 0, CX, CY, 620);
        gl.addColorStop(0, L.rgba(lav, 0.16 * preSpark));
        gl.addColorStop(0.45, L.rgba(lav, 0.05 * preSpark));
        gl.addColorStop(1, L.rgba(lav, 0));
        ctx.fillStyle = gl;
        ctx.fillRect(0, 280, 1080, 1240);
        ctx.restore();

        // the dust the spark picks out, drifting a little away from it on the boil
        ctx.save();
        for (let i = 0; i < g.dust.length; i++) {
          const d = g.dust[i];
          const tw = 0.7 + 0.6 * L.h3(i, bi, SEED + 80);
          const push = 3 * L.h3(i, 7, SEED + 81) * (1 - preSpark);
          ctx.globalAlpha = Math.min(1, d.a * tw * preSpark);
          ctx.fillStyle = d.hot ? white : lav;
          ctx.beginPath();
          ctx.arc(d.x + Math.cos(d.ang) * push, d.y + Math.sin(d.ang) * push, d.r, 0, TAU);
          ctx.fill();
        }
        ctx.restore();
      }

      const aBg = hit(B_BUILD, 6);
      if (aBg > 0) {
        ctx.save();
        ctx.globalAlpha = aBg;
        L.blueprint(ctx, { center: [CX, CY], circles: 0, diagonals: 0, seed: 207 });
        ctx.restore();
      }

      // ---- 2 guide geometry --------------------------------------------------
      if (aBg > 0) {
        ctx.save();
        ctx.globalAlpha = aBg;
        const rot = 6 * DEG * (t / dur);
        ctx.save();
        ctx.translate(CX, CY);
        ctx.rotate(rot);
        L.guideCircle(ctx, 0, 0, 470, { alpha: 0.15, width: 1.5 });
        L.ticks(ctx, 0, 0, { r: 470, n: 120, len: 6, major: 10, majorLen: 15, inward: true, color: lav, alpha: 0.2, width: 1 });
        L.guideCircle(ctx, 0, 0, 640, { alpha: 0.12, width: 1.5 });
        L.guideCircle(ctx, 0, 0, 652, { alpha: 0.09, width: 1, dash: [2, 9] });
        for (let k = 0; k < 4; k++) {
          const a = k * 90 * DEG + 22 * DEG;
          L.arcAnnotation(ctx, 0, 0, 486, a, a + 30 * DEG, { color: lav, alpha: 0.18, width: 1.2, endTicks: 10 });
        }
        // six radial spokes out to the big circle
        const spokes = new Path2D();
        for (let k = 0; k < 6; k++) {
          const a = k * 60 * DEG + 12 * DEG;
          spokes.moveTo(Math.cos(a) * 486, Math.sin(a) * 486);
          spokes.lineTo(Math.cos(a) * 638, Math.sin(a) * 638);
        }
        stroke(ctx, spokes, lav, 0.1, 1, [7, 9]);
        ctx.restore();

        // corner diagonals, full bleed
        const diag = new Path2D();
        diag.moveTo(0, 0);
        diag.lineTo(1080, 1920);
        diag.moveTo(1080, 0);
        diag.lineTo(0, 1920);
        stroke(ctx, diag, lav, 0.12, 1);

        // construction axes through the cell centre
        const axes = new Path2D();
        axes.moveTo(CX, 300);
        axes.lineTo(CX, 1620);
        axes.moveTo(80, CY);
        axes.lineTo(1000, CY);
        stroke(ctx, axes, lav, 0.14, 1, [10, 9]);

        // registration crosses where the r 380 circle meets the axes
        const reg = new Path2D();
        for (const [x, y] of [[CX, 520], [CX, 1280], [160, CY], [920, CY]]) {
          reg.moveTo(x - 9, y);
          reg.lineTo(x + 9, y);
          reg.moveTo(x, y - 9);
          reg.lineTo(x, y + 9);
        }
        stroke(ctx, reg, lav, 0.4, 1.2);

        // concentric construction arcs through the cytoplasm
        const conc = new Path2D();
        arcPath(conc, CX, CY, 220, -150 * DEG, -20 * DEG);
        arcPath(conc, CX, CY, 340, 30 * DEG, 160 * DEG);
        stroke(ctx, conc, lav, 0.12, 1, [4, 7]);

        // the arc the tally will be struck on, set out before it fills
        const pre = new Path2D();
        arcPath(pre, CX, CY, TAL.r, TAL.a0, TAL.a0 + TAL.span, 0.04);
        stroke(ctx, pre, lav, 0.15, 1, [3, 9]);

        // the outer boundary measured in the upper left, where the plate is emptiest
        L.arcAnnotation(ctx, CX, CY, 408, 196 * DEG, 262 * DEG, { color: lav, alpha: 0.3, width: 1.4, endTicks: 14 });
        L.ticks(ctx, CX, CY, { r: 414, n: 30, len: 7, major: 5, majorLen: 14, start: 196 * DEG, span: 66 * DEG, color: white, alpha: 0.3, width: 1 });

        // section arrows on the equator at both frame edges
        const sec = new Path2D();
        for (const sgn of [1, -1]) {
          const x0 = sgn > 0 ? 12 : 1068;
          sec.moveTo(x0, CY - 9);
          sec.lineTo(x0 + sgn * 18, CY);
          sec.lineTo(x0, CY + 9);
          sec.closePath();
        }
        fill(ctx, sec, lav, 0.5);
        ctx.restore();
      }

      // ---- 3 measurement (pops on 16ths) --------------------------------------
      const kH = pop(B_MEAS), kW = pop(B_MEAS2), kS = pop(B_MEAS - 0.125), kN = pop(B_MEAS2 + 0.125);
      if (kS > 0) {
        // the long tick scale down the left edge
        L.ticks(ctx, 60, 130, { length: 1660, angle: Math.PI / 2, n: 42, len: 10 * kS, major: 5, majorLen: 22 * kS, side: -1, alpha: 0.45, width: 1.5, color: lav, p: clamp(kS * 1.2) });
      }
      if (kH > 0) {
        // the cell's diameter, measured down the right side
        L.bracket(ctx, 900, 520, 900, 1280, { p: clamp(kH), alpha: 0.6, cap: 16, color: lav });
        L.ticks(ctx, 900, 520, { length: 760, angle: Math.PI / 2, n: 8, len: 12 * kH, side: 1, baseline: false, alpha: 0.55, width: 1.5, color: white });
        const ext = new Path2D();
        ext.moveTo(CX + 40, 520);
        ext.lineTo(896, 520);
        ext.moveTo(CX + 40, 1280);
        ext.lineTo(896, 1280);
        stroke(ctx, ext, lav, 0.22 * clamp(kH), 1, [4, 7]);
      }
      if (kW > 0) {
        // the cell's width, measured under it
        L.bracket(ctx, 160, 1345, 920, 1345, { p: clamp(kW), alpha: 0.6, cap: 16, color: lav });
        L.ticks(ctx, 160, 1345, { length: 760, angle: 0, n: 8, len: 10 * kW, side: -1, baseline: false, alpha: 0.5, width: 1.5, color: white });
        const ext = new Path2D();
        ext.moveTo(160, CY + 60);
        ext.lineTo(160, 1341);
        ext.moveTo(920, CY + 60);
        ext.lineTo(920, 1341);
        stroke(ctx, ext, lav, 0.22 * clamp(kW), 1, [4, 7]);
      }

      // ---- 4 top specimen strip ------------------------------------------------
      drawStrip(ctx, L, P, g, bi, hit(B_BUILD, 8, E.outExpo, 0.5));

      // ---- 5 neighbour cells ---------------------------------------------------
      drawNeighbours(ctx, L, P, g, bi, aBg * 0.9);

      // ---- 6 the cell ----------------------------------------------------------
      const kOut = hit(B_BUILD, 8, E.outExpo, 0.5);   // the outline draws round from 12 o'clock
      const kIn = seg(t, B_BUILD + 2 * FR, 8, E.outExpo);
      const kFill = seg(t, B_BUILD + 2 * FR, 6, E.inOutSine);

      if (kFill > 0) {
        ctx.save();
        ctx.beginPath();
        L.tracePath(ctx, g.poly, true);
        ctx.fillStyle = P.navy;
        ctx.globalAlpha = 0.55 * kFill;
        ctx.fill();
        // a soft lift round the nucleus, falling off toward the membrane
        ctx.clip();
        ctx.globalCompositeOperation = 'lighter';
        const gl = ctx.createRadialGradient(CX - 30, CY - 40, 20, CX, CY, 430);
        gl.addColorStop(0, L.rgba(lav, 0.12));
        gl.addColorStop(0.5, L.rgba(lav, 0.045));
        gl.addColorStop(1, L.rgba(lav, 0));
        ctx.globalAlpha = kFill;
        ctx.fillStyle = gl;
        ctx.fillRect(CX - 400, CY - 400, 800, 800);
        ctx.restore();
      }

      // ribosome stipple: G1 density 0.35, sweeping out from the centre with the build,
      // in two grains so the cytoplasm has fine dust and larger granules
      const kCyto = hit(B_BUILD + 2 * FR, 8, E.outExpo, 0.5);
      if (kCyto > 0) {
        const front = 40 + 420 * kCyto;
        const inFront = (x, y) => (Math.hypot(x - CX, y - CY) < front ? 0.35 : 0);
        L.stipple(ctx, [g.polyIn, g.nucPoly], {
          spacing: 11, r: [1.0, 1.9], color: lav, alpha: 0.34, seed: SEED + 21, density: inFront,
        });
        L.stipple(ctx, [g.polyIn, g.nucPoly], {
          spacing: 26, r: [1.5, 2.2], color: white, alpha: 0.4, seed: SEED + 22,
          density: (x, y) => inFront(x, y) * 1.6,
        });

        // radial construction spokes from the nuclear rim out to the membrane
        const sp = new Path2D();
        const junction = new Path2D();
        for (let i = 0; i < g.spokes.length; i++) {
          const q = g.spokes[i];
          const c = Math.cos(q.a), s = Math.sin(q.a);
          const r1 = Math.min(q.r1, front);
          if (r1 <= q.r0) continue;
          sp.moveTo(CX + c * q.r0, CY + s * q.r0);
          sp.lineTo(CX + c * r1, CY + s * r1);
          if (r1 > 232) {
            junction.moveTo(CX + c * 224 + 1.6, CY + s * 224);
            junction.arc(CX + c * 224, CY + s * 224, 1.6, 0, TAU);
          }
        }
        stroke(ctx, sp, lav, 0.13, 1, [5, 11]);
        fill(ctx, junction, lav, 0.3);
      }

      // mitochondria: six beans with cristae, drawing in one per 32nd from the build beat
      for (let i = 0; i < g.mito.length; i++) {
        const m = g.mito[i];
        const k = hit(B_BUILD + 2 * FR + i * 0.0625, 3, E.outBack);
        if (k <= 0) continue;
        const kk = Math.min(1.08, k);
        ctx.save();
        ctx.translate(m.x, m.y);
        ctx.scale(kk, kk);
        ctx.translate(-m.x, -m.y);
        const p = new Path2D();
        wob(L, p, m.pts, m.seed, 0.6, bi, true);
        fill(ctx, p, P.navyLight, 0.5);
        stroke(ctx, p, lav, 0.72, 1.6);
        const cr = new Path2D();
        for (const c of m.cr) {
          cr.moveTo(c[0][0], c[0][1]);
          cr.quadraticCurveTo((c[0][0] + c[1][0]) / 2 + 2, (c[0][1] + c[1][1]) / 2, c[1][0], c[1][1]);
        }
        stroke(ctx, cr, white, 0.42, 1);
        ctx.restore();
      }

      // membrane rungs: short ticks just inside the outline, drawing round with it
      if (kOut > 0) {
        const mt = new Map();
        const mtBig = new Path2D();
        for (let i = 0; i < g.memTicks.length; i++) {
          const q = g.memTicks[i];
          if (q.u > kOut) continue;
          const c = Math.cos(q.a), s = Math.sin(q.a);
          const jb = (L.h3(i, bi, SEED + 77) - 0.5) * 0.8;
          const r0 = q.r - 8 + jb;
          const tgt = q.big ? mtBig : bucket(mt, q.al);
          tgt.moveTo(CX + c * r0, CY + s * r0);
          tgt.lineTo(CX + c * (r0 - q.len), CY + s * (r0 - q.len));
        }
        strokeBuckets(ctx, mt, lav, 1.2);
        stroke(ctx, mtBig, white, 0.42, 1.5);
      }

      // the double outline: outer 2.5 px at 85 percent, inner 1.5 px at 50, nine px apart
      if (kOut > 0) {
        const po = new Path2D();
        wob(L, po, slicePts(g.out, g.cumOut, kOut), SEED + 1, 0.6, bi, false);
        ctx.save();
        ctx.globalCompositeOperation = 'lighter';
        stroke(ctx, po, lav, 0.05, 17);
        stroke(ctx, po, lav, 0.07, 7);
        ctx.restore();
        stroke(ctx, po, lav, 0.85, 2.5);
        // the pen head while the outline runs round
        if (kOut < 1) {
          const sl = slicePts(g.out, g.cumOut, kOut);
          const e = sl[sl.length - 1];
          if (e) L.glowDot(ctx, e[0], e[1], 7, { rays: 0, glow: 4, intensity: 0.9, seed: SEED + 2 });
        }
      }
      if (kIn > 0) {
        const pi = new Path2D();
        wob(L, pi, slicePts(g.in, g.cumIn, kIn), SEED + 3, 0.5, bi, false);
        stroke(ctx, pi, lav, 0.5, 1.5);
      }

      // ---- 7 the nucleus -------------------------------------------------------
      const kNuc = hit(B_NUC, 6, E.outExpo, 0.5);
      if (kNuc > 0) {
        const front = 18 + (R_NUC + 16) * kNuc;
        // the lattice sweeps out from the centre, cell by cell
        L.hexLattice(ctx, g.nucPolyIn, {
          r: 18,
          alpha: 0.34,
          width: 1,
          color: lav,
          seed: SEED + 40,
          jitter: 1.1,
          cellFn: (cx, cy) => Math.hypot(cx - CX, cy - CY) < front,
        });
        // the sweep front while it runs
        if (kNuc < 1) {
          const fr = new Path2D();
          fr.arc(CX, CY, front, 0, TAU);
          stroke(ctx, fr, white, 0.4 * (1 - kNuc), 1.5);
        }
        // the nucleolus: a denser disc, drawn under the chromosomes
        const kNo = hit(B_NUC + 2 * FR, 3, E.outBack);
        if (kNo > 0) {
          const nr = NUCLEOLUS[2] * Math.min(1.08, kNo);
          const np = new Path2D();
          wob(L, np, L.ellipsePts(NUCLEOLUS[0], NUCLEOLUS[1], nr, nr * 0.94, 26), SEED + 45, 0.5, bi, true);
          fill(ctx, np, P.navyLight, 0.5);
          stroke(ctx, np, lav, 0.5, 1.2);
          L.stipple(ctx, (c) => c.arc(NUCLEOLUS[0], NUCLEOLUS[1], nr - 1, 0, TAU), {
            bounds: [NUCLEOLUS[0] - nr, NUCLEOLUS[1] - nr, nr * 2, nr * 2],
            spacing: 4.6, r: [1.0, 1.5], color: lav, alpha: 0.5, density: 0.8, seed: SEED + 46,
          });
        }

        // the envelope: a double line drawing round from 12 o'clock, then pore marks
        const kRim = hit(B_NUC, 8, E.outExpo, 0.5);
        const pr = new Path2D();
        wob(L, pr, slicePts(g.nucOut, g.cumNuc, kRim), SEED + 41, 0.5, bi, false);
        stroke(ctx, pr, lav, 0.8, 2);
        const pr2 = new Path2D();
        wob(L, pr2, slicePts(g.nucIn, g.cumNuc, Math.max(0, kRim - 0.08)), SEED + 42, 0.4, bi, false);
        stroke(ctx, pr2, lav, 0.45, 1.2);
        const pore = new Path2D();
        const poreBig = new Path2D();
        for (let i = 0; i < g.pores.length; i++) {
          const q = g.pores[i];
          const u = ((q.a + Math.PI / 2 + TAU) % TAU) / TAU;
          if (u > kRim) continue;
          const c = Math.cos(q.a), s = Math.sin(q.a);
          const tgt = q.big ? poreBig : pore;
          tgt.moveTo(CX + c * (q.r - 6), CY + s * (q.r - 6));
          tgt.lineTo(CX + c * (q.r + 6), CY + s * (q.r + 6));
        }
        stroke(ctx, pore, white, 0.4, 1.2);
        stroke(ctx, poreBig, white, 0.6, 1.5);
        // an arc annotation on the rim, the nucleus called out as a boundary
        if (kN > 0) {
          L.arcAnnotation(ctx, CX, CY, R_NUC + 26, 22 * DEG, 74 * DEG, {
            color: lav, alpha: 0.55 * clamp(kN), width: 1.5, endTicks: 12, p: clamp(kN),
          });
        }
      }

      // ---- the four chromosomes: lattice worms with glow-dot centres ------------
      for (let k = 0; k < g.chromo.length; k++) {
        const ch = g.chromo[k];
        const kc = hit(B_CH[k], 3, E.outBack);
        if (kc <= 0) continue;
        const tint = ch.c.pair === 0 ? tintA : tintB;
        const s = Math.min(1.08, kc);
        // the glow dot sits under the worm, so the centre back-lights it instead of burning it out
        L.glowDot(ctx, ch.c.x, ch.c.y, 10 * s, { rays: 0, glow: 4.4, intensity: 0.85, twinkle: 0.14, seed: ch.seed + 3 });
        ctx.save();
        ctx.translate(ch.c.x, ch.c.y);
        ctx.scale(s, s);
        ctx.translate(-ch.c.x, -ch.c.y);
        // the thread and its band, rebuilt on this drawing so it trembles with 01's
        const w = wormParts(L, ch, bi, SEED);
        const bp = new Path2D();
        wob(L, bp, w.poly, ch.seed, 0.55, bi, true);
        fill(ctx, bp, P.navy, 0.72);
        ctx.save();
        ctx.globalCompositeOperation = 'lighter';
        const hp = new Path2D();
        wob(L, hp, w.spine, ch.seed + 5, 0.4, bi, false);
        stroke(ctx, hp, tint, 0.13, 22);
        ctx.restore();
        // the lattice: rungs across the band, then the outline over them
        const rg = new Path2D();
        for (let i = 0; i < w.rungs.length; i++) {
          const r = w.rungs[i];
          const jx = (L.h3(i, bi, ch.seed + 9) - 0.5) * 0.7;
          rg.moveTo(r.p0[0], r.p0[1]);
          rg.quadraticCurveTo(r.cm[0] + jx, r.cm[1], r.p1[0], r.p1[1]);
        }
        stroke(ctx, rg, tint, 0.45, 1);
        // the coiled thread down the middle: one fibre, not yet copied
        const th = new Path2D();
        wob(L, th, w.thread, ch.seed + 11, 0.4, bi, false);
        stroke(ctx, th, white, 0.4, 1.2, [5, 5]);
        stroke(ctx, bp, tint, 0.95, 2.2);
        ctx.restore();

        // the centre: a hot core and 12 radial ticks (art bible section 5)
        const core = new Path2D();
        core.arc(ch.c.x, ch.c.y, 5 * s, 0, TAU);
        fill(ctx, core, glow, 0.95);
        L.ticks(ctx, ch.c.x, ch.c.y, {
          r: 21 * s, n: 12, len: 15 * s, major: 3, majorLen: 20 * s,
          rot: (bi % 4) * 7.5 * DEG, color: white, alpha: 0.62, width: 1.5,
        });
      }

      // both members of a pair are the same length: one measure under each, struck on the
      // 16th that completes the pair, so the two long and the two short read as two pairs
      for (let k = 0; k < g.chromo.length; k++) {
        const ch = g.chromo[k];
        const kb = hit(B_CH[ch.c.pair === 0 ? 1 : 3] + 2 * FR, 4, E.outExpo, 0.5);
        if (kb <= 0) continue;
        const th = ch.c.tilt * DEG;
        const dx = Math.cos(th) * ch.c.len * 0.5, dy = Math.sin(th) * ch.c.len * 0.5;
        L.bracket(ctx, ch.c.x - dx, ch.c.y - dy, ch.c.x + dx, ch.c.y + dy, {
          offset: 26, cap: 9, width: 1.2, alpha: 0.42 * clamp(kb), color: white, p: clamp(kb),
        });
      }

      // ---- 8 the tally: 46 ticks in 23 pairs ------------------------------------
      if (t >= B_TALLY - FR) {
        const done = clamp((t - B_TALLY) / (TALLY_END - B_TALLY));
        const aEnd = TAL.a0 + TAL.span * done;
        // a calm band behind the arc, so 46 fine ticks read against the cytoplasm grain
        const band = new Path2D();
        arcPath(band, CX, CY, TAL.r + TAL.len / 2 - 4, TAL.a0, aEnd, 0.03);
        stroke(ctx, band, P.navy, 0.62, 40);
        const spine = new Path2D();
        arcPath(spine, CX, CY, TAL.r - 6, TAL.a0, aEnd, 0.03);
        stroke(ctx, spine, white, 0.3, 1.3);
        const guide = new Path2D();
        arcPath(guide, CX, CY, TAL.r + TAL.len + 10, TAL.a0, aEnd, 0.03);
        stroke(ctx, guide, lav, 0.18, 1, [3, 8]);

        const ticks = new Path2D();
        const bridges = new Path2D();
        for (let i = 0; i < g.tally.length; i++) {
          const q = g.tally[i];
          const ta = B_TALLY + i * PAIR_DT;
          const kt = hit(ta, 2, E.outBack);
          if (kt <= 0) continue;
          const len = TAL.len * Math.min(1.1, kt);
          for (const a of q.a) {
            const c = Math.cos(a), s = Math.sin(a);
            ticks.moveTo(CX + c * (TAL.r - 1), CY + s * (TAL.r - 1));
            ticks.lineTo(CX + c * (TAL.r + len), CY + s * (TAL.r + len));
          }
          // the little bridge that makes each pair read as a pair, not as a scale
          if (kt > 0.4) arcPath(bridges, CX, CY, TAL.r - 6, q.a[0], q.a[1], 0.02);
        }
        stroke(ctx, ticks, white, 0.75, 1.6);
        stroke(ctx, bridges, white, 0.6, 1.6);

        // a magenta ring pulses once per pair, so the count travels round the arc
        for (let i = 0; i < g.tally.length; i++) {
          const ta = B_TALLY + i * PAIR_DT;
          if (t < ta || t >= ta + 3 * FR) continue;
          const u = (t - ta) / (3 * FR);
          const q = g.tally[i];
          ctx.save();
          ctx.beginPath();
          ctx.arc(q.mx, q.my, lerp(5, 19, E.outExpo(u + 0.2)), 0, TAU);
          ctx.strokeStyle = mag;
          ctx.globalAlpha = (1 - u * u) * 0.88;
          ctx.lineWidth = 3;
          ctx.stroke();
          ctx.restore();
        }

        // the end brackets of the completed sweep
        if (done >= 1) {
          const ends = new Path2D();
          for (const a of [TAL.a0, TAL.a0 + TAL.span]) {
            const c = Math.cos(a), s = Math.sin(a);
            ends.moveTo(CX + c * (TAL.r - 14), CY + s * (TAL.r - 14));
            ends.lineTo(CX + c * (TAL.r + TAL.len + 14), CY + s * (TAL.r + TAL.len + 14));
          }
          stroke(ctx, ends, white, 0.55, 1.8);
        }
      }

      // ---- 9 node glyphs -------------------------------------------------------
      const kNodeL = hit(B_NODE, 4, E.outBack, 0.6);
      const kNodeR = hit(B_NODE + 0.125, 4, E.outBack, 0.6);
      nodeGlyph(ctx, L, P, {
        cx: NODE_L.cx, cy: NODE_L.cy, r: NODE_L.r, k: kNodeL,
        sx: g.srcL[0], sy: g.srcL[1], sr: NODE_L.sr, bow: 70, seed: SEED + 90, bi, rot: t * 0.3,
      }, () => nodeEnvelope(ctx, L, P, bi, clamp(kNodeL)));
      nodeGlyph(ctx, L, P, {
        cx: NODE_R.cx, cy: NODE_R.cy, r: NODE_R.r, k: kNodeR,
        sx: g.srcR[0], sy: g.srcR[1], sr: NODE_R.sr, bow: -80, seed: SEED + 95, bi, rot: -t * 0.3,
      }, () => nodeThread(ctx, L, P, bi, tintA));

      // ---- 10 the spark --------------------------------------------------------
      // T 2.000: one white spark at (540, 900) on near-black, with two glassy rings on the cut
      if (t < B_BUILD + 8 * FR) {
        const lf = Math.floor(t * 24 + 1e-6);
        const flare = [0.42, 0.86, 1.14][lf] != null ? [0.42, 0.86, 1.14][lf] : 1;
        const fade = 1 - seg(t, B_BUILD, 8);
        const r = 13 * flare * (bi % 2 ? 0.92 : 1.06);
        if (t < B_BUILD) {
          for (let k = 0; k < 2; k++) {
            const u = clamp((t - k * 3 * FR) / 0.42);
            if (u <= 0) continue;
            ctx.save();
            ctx.beginPath();
            ctx.arc(CX, CY, 18 + (k ? 190 : 330) * E.outExpo(u), 0, TAU);
            ctx.strokeStyle = lav;
            ctx.globalAlpha = (k ? 0.16 : 0.26) * (1 - u) * (1 - u);
            ctx.lineWidth = 1.5;
            ctx.stroke();
            ctx.restore();
          }
        }
        L.glowDot(ctx, CX, CY, r, {
          rays: 8, rayLen: 3.6, rot: (bi % 2) * 22.5 * DEG, seed: SEED + 70, glow: 5.2,
          intensity: 0.35 + 0.65 * fade,
        });
      }

      // ---- 11 the cycle glyph G5 (the canonical helper), arriving on T 4.0 -------
      const kGlyph = hit(B_GLYPH, 6, E.outCubic, 0.5);
      if (kGlyph > 0) {
        // a plate so the guide geometry never shows through the arcs
        ctx.save();
        ctx.globalAlpha = kGlyph;
        const plate = new Path2D();
        plate.arc(900, 300, 70, 0, TAU);
        fill(ctx, plate, P.navy, 0.94);
        fill(ctx, plate, P.navyLight, 0.4);
        stroke(ctx, plate, lav, 0.28, 1);
        // the ticks sit inside the ring, so the glyph keeps its footprint in the safe area
        L.ticks(ctx, 900, 300, { r: 44, n: 48, len: 4, major: 12, majorLen: 9, color: lav, alpha: 0.3, width: 1, inward: true });
        ctx.restore();
        L.cycleGlyph(ctx, info.T, 'schematic', kGlyph);
      }
      // the magenta flash on the beat: a ring through the glyph, 20 to 80 over 4 frames
      if (t >= B_GLYPH && t < B_GLYPH + 4 * FR) {
        const u = (t - B_GLYPH) / (4 * FR);
        ctx.save();
        ctx.beginPath();
        ctx.arc(900, 300, lerp(20, 80, E.outExpo(u + 0.25)), 0, TAU);
        ctx.strokeStyle = mag;
        ctx.globalAlpha = 1 - u * u;
        ctx.lineWidth = 3;
        ctx.stroke();
        ctx.restore();
      }
    },
  });
})();
