// 09 two-nuclei-blueprint : "Two new nuclei, the cell pinches" (schematic, global T 19.0 to 21.5)
//
// Frame 0 is 08's last frame on G3: the elongated cell (half-width 380, half-height 560 after 08's
// T 18.0 beat), poles at (540, 400) and (540, 1400), the spindle still strung, and the two arrived
// sets of four single-copy chromosomes centred on y 560 and y 1240. From T 21.375 the frame is
// exactly G4 (two near-circles r 300 at (540, 560) and (540, 1240), a 60 px neck at y 900, each
// nucleus r 135 holding the four chromosomes in the G1 arrangement scaled 0.8), screen-fixed, so
// 10 flashes onto the same pixels. Nothing here rides a camera.
//
// Layers, back to front:
//   1  blueprint plate: navy, 60 px grid, corner marks
//   2  guide geometry: circles r 470 / 640 at (540, 900) turning 6 degrees, corner diagonals,
//      the equator construction line with its tick scale, the long axis, registration crosses
//   3  target construction: the two G4 lobe circles r 300, the nucleus circles r 135, the two
//      furrow circles r 49 struck from (540 +/- 79, 900), and the furrow pull arrows
//   4  cytoplasm: navy calming fill inside the outline, a soft inner light, ribosome stipple,
//      six lattice mitochondria sharing themselves out between the two lobes as the cell pinches
//   5  spindle: the two poles (22 px discs, 12 radial ticks) with 08's arrival rings fading,
//      8 centromere fibres and 20 free fibres, dissolving into stipple on T 20.0
//   6  the two new nuclei: interior fill, hex lattice nucleoplasm, then the chromosomes
//   7  chromosomes: four per nucleus, each a ribbon that morphs from the condensed V of anaphase
//      into a loose G1 worm, with a thin identity line (schemBlue pair A, schemRust pair B)
//   8  nuclear envelopes: double lavender rim with a lineWhite pore ladder, drawn round from
//      12 o'clock on T 19.5 and T 19.75, then nucleoli as glow dots
//   9  the cell outline: double outline with its membrane ladder, pinching to G4
//  10  measurement: the height bracket and left ruler, the neck bracket at the equator, a
//      bracket per nucleus with its extension lines and rim ticks
//  11  magenta: the two membrane-closed rings and the two furrow rings (each under 12 frames)
//  12  network: the furrow inset (left) and the envelope-assembly inset (right) on lead lines
//  13  the cycle glyph at (900, 300) through FILM.lib.cycleGlyph, drawn last
(function () {
  'use strict';

  const ID = 'two-nuclei-blueprint';
  const LIB = FILM.lib;
  const P = LIB.pal;
  const E = LIB.ease;
  const TAU = Math.PI * 2;
  const DEG = Math.PI / 180;
  const FR = 1 / 24;

  // hoisted colours (pal is a read-only proxy)
  const LAV = P.lavender, WHITE = P.lineWhite, MAG = P.magenta, GLOW = P.glow;
  const NAVY = P.navy, NAVYD = P.navyDeep, NAVYL = P.navyLight;
  const TINT_A = P.schemBlue, TINT_B = P.schemRust;

  const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
  const lerp = (a, b, u) => a + (b - a) * u;
  const sstep = (a, b, x) => {
    const u = clamp((x - a) / (b - a));
    return u * u * (3 - 2 * u);
  };
  // every seed in this file comes from the shot id
  const sd = (...k) => LIB.hash(ID, ...k) & 0x7fffffff;

  // ---------------------------------------------------------------------------
  // Shared geometry (docs/storyboard.md: G3 at the cut, G4 at the end)
  // ---------------------------------------------------------------------------

  const CX = 540;          // the frame axis
  const EQ = 900;          // metaphase plate, then the furrow line
  const A_ELL = 380;       // G3 half-width
  const B_ELL = 560;       // 08's half-height at its last beat
  const R_LOBE = 300;      // G4 daughter radius
  const CY_U = 560;        // G4 upper daughter centre
  const CY_L = 1240;       // G4 lower daughter centre
  const NECK_HW = 30;      // half of the 60 px neck
  const B_G4 = EQ - (CY_U - R_LOBE);   // 640: half-height of the pinched pair
  const D_LOBE = EQ - CY_U;            // 340
  const R_NUC = 135;       // G4 nucleus radius
  const POLE_U = 400, POLE_L = 1400;   // 08's poles at its last beat

  // The furrow is struck as a circle tangent to both lobes: (NECK_HW + Rf)^2 + D^2 = (R_LOBE + Rf)^2
  const R_FUR = (R_LOBE * R_LOBE - NECK_HW * NECK_HW - D_LOBE * D_LOBE) / (2 * (NECK_HW - R_LOBE));
  const D_FUR = NECK_HW + R_FUR;                       // furrow centre offset from the axis
  const DY_T = (R_FUR * D_LOBE) / (R_LOBE + R_FUR);    // where furrow meets lobe, above/below y 900

  // the G4 silhouette: half-width at a height y
  function xFinal(y) {
    const d = y - EQ;
    if (Math.abs(d) <= DY_T) return D_FUR - Math.sqrt(Math.max(0, R_FUR * R_FUR - d * d));
    const cy = d < 0 ? CY_U : CY_L;
    const q = R_LOBE * R_LOBE - (y - cy) * (y - cy);
    return q > 0 ? Math.sqrt(q) : 0;
  }
  // the G3 ellipse: half-width at a height y
  function xEllipse(y) {
    const s = (y - EQ) / B_ELL;
    return s * s >= 1 ? 0 : A_ELL * Math.sqrt(1 - s * s);
  }

  const S_SHAPE = sd('shape');
  // a body cell is never a perfect circle: a fixed low-frequency irregularity on the silhouette
  function bump(s) {
    return 1 + 0.030 * LIB.noise1(s * 2.4 + 3.1, S_SHAPE) + 0.016 * LIB.noise1(s * 5.7 - 1.4, S_SHAPE + 7);
  }
  const halfHeight = (k) => lerp(B_ELL, B_G4, k);
  // s runs -1 (top pole) to +1 (bottom pole); k is the pinch, 0 at the cut and 1 on G4
  function halfWidth(s, k) {
    const e = xEllipse(EQ + s * B_ELL);
    const f = xFinal(EQ + s * B_G4);
    return lerp(e, f, k) * bump(s);
  }

  // sample list: clustered at the poles (fast curvature) and again across the furrow
  const SLIST = (() => {
    const out = [];
    const n = 116;
    for (let i = 0; i <= n; i++) out.push(-Math.cos((i / n) * Math.PI));
    for (let s = -0.235; s <= 0.235; s += 0.0075) out.push(s);
    out.sort((a, b) => a - b);
    const cleaned = [];
    for (const s of out) {
      const v = clamp(s, -1, 1);
      if (!cleaned.length || v - cleaned[cleaned.length - 1] > 1e-4) cleaned.push(v);
    }
    if (cleaned[cleaned.length - 1] < 1) cleaned.push(1);
    return cleaned;
  })();

  // the outline as a closed polygon: right side top to bottom, then left side back up
  function outlinePts(k, step) {
    const HH = halfHeight(k);
    const st = step || 1;
    const right = [], left = [];
    for (let i = 0; i < SLIST.length; i += st) {
      const s = SLIST[i];
      const y = EQ + s * HH;
      const w = halfWidth(s, k);
      right.push([CX + w, y]);
      left.push([CX - w, y]);
    }
    const last = SLIST[SLIST.length - 1];
    if (right[right.length - 1][1] < EQ + last * HH) {
      right.push([CX, EQ + last * HH]);
      left.push([CX, EQ + last * HH]);
    }
    return right.concat(left.reverse());
  }

  // the inner line of the double outline, 9 px in (built from the profile so the poles stay clean)
  function innerPts(k, step) {
    const HH = halfHeight(k) - 9;
    const st = step || 2;
    const right = [], left = [];
    for (let i = 0; i < SLIST.length; i += st) {
      const s = SLIST[i];
      const y = EQ + s * HH;
      const w = Math.max(0, halfWidth(s, k) - 9);
      right.push([CX + w, y]);
      left.push([CX - w, y]);
    }
    return right.concat(left.reverse());
  }

  // ---------------------------------------------------------------------------
  // Chromosomes
  //
  // Four per set, the same four in both, so the daughters are identical. Pair A is long
  // (schemBlue), pair B short (schemRust). Arrival x values are G3's: A 470 / 610, B 480 / 600,
  // staggered +/- 24 px in y about the set centre so the four can be counted in the huddle.
  // The relaxed pose is G1's arrangement scaled 0.8 about the nucleus centre.
  // ---------------------------------------------------------------------------

  const NPTS = 25;         // spine samples per chromosome
  const MID = (NPTS - 1) / 2;

  const SET = [
    // kind 0 = pair A (long), 1 = pair B (short)
    { kind: 0, ax: 470, ady: -36, dx: -56, dy: -40, tilt: 20 },   // A1
    { kind: 1, ax: 480, ady: 34, dx: -48, dy: 44, tilt: -20 },    // B1
    { kind: 1, ax: 600, ady: 34, dx: 48, dy: 44, tilt: 20 },      // B2
    { kind: 0, ax: 610, ady: -36, dx: 56, dy: -40, tilt: -20 },   // A2
  ];
  // condensed V (a chromatid bent at the centromere) and relaxed worm, per pair
  const KIND = [
    { vw: 40, vh: 42, len: 104, bow: 12, hw0: 12.0, hw1: 7.2, tint: TINT_A },
    { vw: 26, vh: 28, len: 68, bow: 8, hw0: 10.0, hw1: 6.2, tint: TINT_B },
  ];

  function cumLen(pts) {
    const c = new Float64Array(pts.length);
    for (let i = 1; i < pts.length; i++) c[i] = c[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    return c;
  }

  function resample(pts, n) {
    const c = cumLen(pts);
    const total = c[c.length - 1] || 1;
    const out = [];
    let j = 0;
    for (let i = 0; i < n; i++) {
      const target = (total * i) / (n - 1);
      while (j < pts.length - 2 && c[j + 1] < target) j++;
      const u = (target - c[j]) / (c[j + 1] - c[j] || 1);
      out.push([lerp(pts[j][0], pts[j + 1][0], u), lerp(pts[j][1], pts[j + 1][1], u)]);
    }
    return out;
  }

  // the anaphase pose: apex (the centromere) leads toward the pole, the two arms trail
  function veePts(cx, cy, vw, vh, ap) {
    const apex = [cx, cy - ap * vh];
    const tipL = [cx - vw, cy + ap * vh];
    const tipR = [cx + vw, cy + ap * vh];
    return resample(LIB.smoothPts([tipL, apex, tipR], false, 4), NPTS);
  }

  // the interphase pose: a loose worm lying at 20 degrees off horizontal
  function wormPts(cx, cy, len, tilt, bow, seed) {
    const ca = Math.cos(tilt), sa = Math.sin(tilt);
    const ph = LIB.h3(seed, 3, 101) * TAU;
    const out = [];
    for (let i = 0; i < NPTS; i++) {
      const u = i / (NPTS - 1) - 0.5;
      const s = u * len;
      const off = bow * Math.sin((u + 0.5) * Math.PI * 1.7 + ph) + bow * 0.4 * LIB.noise1(u * 5 + 2, seed);
      out.push([cx + ca * s - sa * off, cy + sa * s + ca * off]);
    }
    return out;
  }

  // half-width along a chromosome: near constant, softened at the two ends
  function widthsFor(hw) {
    const out = [];
    for (let i = 0; i < NPTS; i++) out.push(hw * (1 - 0.32 * Math.pow(Math.abs(i - MID) / MID, 2.4)));
    return out;
  }

  function normalsOf(pts) {
    const n = pts.length;
    const out = [];
    for (let i = 0; i < n; i++) {
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
      const tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      out.push([-ty / tl, tx / tl, tx / tl, ty / tl]);
    }
    return out;
  }

  // closed ribbon around a spine, with round caps at both ends
  function ribbonPoly(pts, hws, nrm) {
    const n = pts.length;
    const left = [], right = [];
    for (let i = 0; i < n; i++) {
      const p = pts[i], q = nrm[i], w = hws[i];
      left.push([p[0] + q[0] * w, p[1] + q[1] * w]);
      right.push([p[0] - q[0] * w, p[1] - q[1] * w]);
    }
    const cap = (i, dir) => {
      const p = pts[i], q = nrm[i], w = hws[i];
      const out = [];
      for (let j = 1; j < 7; j++) {
        const a = (j / 7) * Math.PI;
        const c = Math.cos(a), s = Math.sin(a) * dir;
        out.push([p[0] + q[0] * w * c + q[2] * w * s, p[1] + q[1] * w * c + q[3] * w * s]);
      }
      return out;
    };
    return left.concat(cap(n - 1, 1), right.reverse(), cap(0, -1));
  }

  // ---------------------------------------------------------------------------
  // Mitochondria: six lattice beans, three ending in each daughter (the cytoplasm shares out)
  // ---------------------------------------------------------------------------

  const MITO = [
    { x0: 330, y0: 640, r0: -24, x1: 332, y1: 470, r1: -14 },
    { x0: 735, y0: 690, r0: 34, x1: 716, y1: 618, r1: 22 },
    { x0: 306, y0: 872, r0: 8, x1: 452, y1: 776, r1: -38 },
    { x0: 762, y0: 1058, r0: -30, x1: 728, y1: 1178, r1: -16 },
    { x0: 332, y0: 1180, r0: 22, x1: 356, y1: 1318, r1: 40 },
    { x0: 622, y0: 1312, r0: -12, x1: 600, y1: 1438, r1: -4 },
  ];

  // ---------------------------------------------------------------------------
  // Geometry built once (a pure function of the constants above)
  // ---------------------------------------------------------------------------

  let GEO = null;
  function geo(L) {
    if (GEO) return GEO;
    const g = {};

    // free fibres: ten per pole, fanning past the equator, plus their dissolution drift
    g.free = [];
    for (const [py, sign, tag] of [[POLE_U, 1, 'up'], [POLE_L, -1, 'dn']]) {
      const r = L.rng(L.hash(ID, 'free', tag));
      for (let i = 0; i < 10; i++) {
        const a = lerp(-62, 62, i / 9) * DEG + r.range(-3.5, 3.5) * DEG;
        const len = r.range(430, 620);
        const ex = CX + Math.sin(a) * len;
        const ey = py + sign * Math.cos(a) * len;
        g.free.push({
          x0: CX + Math.sin(a) * 26, y0: py + sign * Math.cos(a) * 26,
          x1: ex, y1: ey,
          bow: r.range(-16, 16), seed: (L.hash(ID, 'free', tag, i) & 0xffff), alpha: r.range(0.26, 0.46),
        });
      }
    }

    // ribosome stipple keeps clear of the two nuclei once they exist
    g.stippleSeed = sd('ribo');

    // the two inset node glyphs
    g.node = {
      furrow: { x: 182, y: 1428, r: 54, seed: sd('node-furrow') },
      envelope: { x: 880, y: 1428, r: 54, seed: sd('node-env') },
    };

    // pole tick rotation offsets, fixed per pole
    g.poleSeed = [sd('pole', 0), sd('pole', 1)];

    // chromosome seeds: one per set and slot, so the worm bow is stable
    g.chrSeed = [[], []];
    for (let s = 0; s < 2; s++) for (let i = 0; i < 4; i++) g.chrSeed[s].push(sd('chr', s, i));

    // nucleolus offsets: G1's nucleolus at (500, 870) against a (540, 900) nucleus, scaled 0.8
    g.nucleolus = [-32, -24];

    GEO = g;
    return g;
  }

  // ---------------------------------------------------------------------------
  // Line helpers
  // ---------------------------------------------------------------------------

  function wobPts(L, pts, seed, amp, bi) {
    const n = pts.length;
    const out = new Array(n);
    let s = 0;
    const sdd = (seed + bi * 7919) | 0;
    for (let i = 0; i < n; i++) {
      const p = pts[i];
      if (i > 0) s += Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]);
      const a = pts[i > 0 ? i - 1 : 0], b = pts[i < n - 1 ? i + 1 : n - 1];
      const tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      const d = amp * L.noise1(s * 0.02, sdd);
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

  function seg(t, a, frames, e) {
    const u = clamp((t - a) / (frames * FR));
    if (u <= 1e-5) return 0;   // outBack returns about 1e-16 at 0, which would draw a speck
    return e ? e(u) : u;
  }

  function arcPts(cx, cy, r, a0, a1, n) {
    const out = [];
    const m = n || Math.max(8, Math.round((Math.abs(a1 - a0) * r) / 9));
    for (let i = 0; i <= m; i++) {
      const a = a0 + ((a1 - a0) * i) / m;
      out.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
    }
    return out;
  }

  // ---------------------------------------------------------------------------
  // One chromosome: the ribbon, its bands, its identity line and its centromere
  // ---------------------------------------------------------------------------

  function drawChromosome(ctx, L, spec, cx0, cy0, cx1, cy1, ap, relax, seed, bi, alpha) {
    const K = KIND[spec.kind];
    const vee = veePts(cx0, cy0, K.vw, K.vh, ap);
    const worm = wormPts(cx1, cy1, K.len, spec.tilt * DEG, K.bow, seed);
    const pts = [];
    for (let i = 0; i < NPTS; i++) {
      pts.push([lerp(vee[i][0], worm[i][0], relax), lerp(vee[i][1], worm[i][1], relax)]);
    }
    const hw = lerp(K.hw0, K.hw1, relax);
    const hws = widthsFor(hw);
    const nrm = normalsOf(pts);
    const body = ribbonPoly(pts, hws, nrm);

    // the form, solid over the grid so the count reads
    const bp = new Path2D();
    wob(L, bp, body, seed + 11, 0.5, bi, true);
    fill(ctx, bp, NAVY, 0.86 * alpha);
    fill(ctx, bp, NAVYL, 0.34 * alpha);

    // chromatin bands across the ribbon, and the thin identity line down the spine
    const bands = new Path2D();
    for (let i = 3; i < NPTS - 3; i += 3) {
      const p = pts[i], q = nrm[i], w = hws[i] * 0.78;
      const j = (L.h3(i, bi, seed + 3) - 0.5) * 1.1;
      bands.moveTo(p[0] + q[0] * w + j, p[1] + q[1] * w);
      bands.lineTo(p[0] - q[0] * w + j, p[1] - q[1] * w);
    }
    stroke(ctx, bands, LAV, 0.24 * alpha, 1);

    const spine = new Path2D();
    wob(L, spine, pts, seed + 5, 0.4, bi, false);
    stroke(ctx, spine, K.tint, 0.62 * alpha, 1.4);

    // double outline: 1.8 px primary, a 1 px inner line held 3 px inside
    const inner = new Path2D();
    const hIn = [];
    for (let i = 0; i < NPTS; i++) hIn.push(Math.max(1, hws[i] - 3));
    wob(L, inner, ribbonPoly(pts, hIn, nrm), seed + 13, 0.4, bi, true);
    stroke(ctx, inner, LAV, 0.26 * alpha, 1);
    stroke(ctx, bp, LAV, 0.88 * alpha, 1.8);

    // centromere: a disc at the middle, a glow while the chromosome is still condensed
    const cm = pts[MID | 0];
    const hot = (1 - relax) * alpha;
    const disc = new Path2D();
    disc.moveTo(cm[0] + hw * 0.66, cm[1]);
    disc.arc(cm[0], cm[1], hw * 0.66, 0, TAU);
    fill(ctx, disc, NAVY, 0.9 * alpha);
    stroke(ctx, disc, WHITE, (0.45 + 0.4 * (1 - relax)) * alpha, 1.3);
    if (hot > 0.02) {
      L.glowDot(ctx, cm[0], cm[1], 5.5, {
        rays: 8, rayLen: 2.4, rot: (bi % 2) * 22.5 * DEG, glow: 3.6,
        intensity: hot, seed: seed + 21, twinkle: 0.14,
      });
    }
    return cm;
  }

  // ---------------------------------------------------------------------------
  // One new nucleus
  // ---------------------------------------------------------------------------

  // the interior: a calming navy fill and the nucleoplasm lattice, clipped to the swept wedge
  function drawNucleusFill(ctx, L, cx, cy, prog, seed, bi) {
    if (prog <= 0) return;
    const a0 = -Math.PI / 2, a1 = a0 + TAU * clamp(prog);
    ctx.save();
    ctx.beginPath();
    if (prog >= 1) ctx.arc(cx, cy, R_NUC - 9, 0, TAU);
    else {
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, R_NUC - 9, a0, a1);
      ctx.closePath();
    }
    ctx.clip();
    ctx.fillStyle = NAVY;
    ctx.globalAlpha = 0.55;
    ctx.fillRect(cx - R_NUC, cy - R_NUC, R_NUC * 2, R_NUC * 2);
    ctx.globalAlpha = 1;
    L.hexLattice(ctx, (c) => c.arc(cx, cy, R_NUC - 12, 0, TAU), {
      bounds: [cx - R_NUC, cy - R_NUC, R_NUC * 2, R_NUC * 2],
      r: 17, alpha: 0.24, width: 1, seed: seed + 1, color: LAV,
    });
    // a soft lift from the upper left, the schematic's only glow inside the nucleus
    ctx.globalCompositeOperation = 'lighter';
    const gl = ctx.createRadialGradient(cx - 40, cy - 46, 10, cx, cy, R_NUC);
    gl.addColorStop(0, L.rgba(LAV, 0.1));
    gl.addColorStop(0.6, L.rgba(LAV, 0.035));
    gl.addColorStop(1, L.rgba(LAV, 0));
    ctx.fillStyle = gl;
    ctx.fillRect(cx - R_NUC, cy - R_NUC, R_NUC * 2, R_NUC * 2);
    ctx.restore();
  }

  // the envelope: a double rim with a pore ladder, drawn round from 12 o'clock
  function drawNucleusRim(ctx, L, cx, cy, prog, seed, bi) {
    if (prog <= 0) return;
    const k = clamp(prog);
    const a0 = -Math.PI / 2, a1 = a0 + TAU * k;
    const outer = new Path2D();
    wob(L, outer, arcPts(cx, cy, R_NUC, a0, a1), seed + 31, 0.7, bi, false);
    const inner = new Path2D();
    wob(L, inner, arcPts(cx, cy, R_NUC - 9, a0, a1), seed + 32, 0.6, bi, false);

    // the ladder of membrane cells between the two lines
    const rungs = new Path2D();
    const nR = Math.max(1, Math.round((TAU * R_NUC * k) / 11));
    for (let i = 0; i <= nR; i++) {
      const a = a0 + (a1 - a0) * (i / Math.max(1, nR));
      const c = Math.cos(a), s = Math.sin(a);
      const j = (L.h3(i, bi, seed + 33) - 0.5) * 0.8;
      rungs.moveTo(cx + c * (R_NUC - 9 + j), cy + s * (R_NUC - 9 + j));
      rungs.lineTo(cx + c * (R_NUC + j), cy + s * (R_NUC + j));
    }
    stroke(ctx, rungs, LAV, 0.32, 1);
    stroke(ctx, inner, LAV, 0.5, 1.5);
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    stroke(ctx, outer, LAV, 0.05, 13);
    ctx.restore();
    stroke(ctx, outer, LAV, 0.85, 2.5);

    // eight nuclear pores: a lineWhite bar bridging the two lines
    const pores = new Path2D();
    for (let i = 0; i < 8; i++) {
      const a = a0 + (i + 0.5) * (TAU / 8);
      if (a > a1) continue;
      const c = Math.cos(a), s = Math.sin(a);
      pores.moveTo(cx + c * (R_NUC - 12) - s * 6, cy + s * (R_NUC - 12) + c * 6);
      pores.lineTo(cx + c * (R_NUC + 3) - s * 6, cy + s * (R_NUC + 3) + c * 6);
      pores.moveTo(cx + c * (R_NUC - 12) + s * 6, cy + s * (R_NUC - 12) - c * 6);
      pores.lineTo(cx + c * (R_NUC + 3) + s * 6, cy + s * (R_NUC + 3) - c * 6);
    }
    stroke(ctx, pores, WHITE, 0.6, 1.4);

    // the drawing head: a bright tick where the envelope is still being laid down
    if (k < 1) {
      const c = Math.cos(a1), s = Math.sin(a1);
      const head = new Path2D();
      head.moveTo(cx + c * (R_NUC - 20), cy + s * (R_NUC - 20));
      head.lineTo(cx + c * (R_NUC + 16), cy + s * (R_NUC + 16));
      stroke(ctx, head, WHITE, 0.8, 2);
    }
  }

  // ---------------------------------------------------------------------------
  // Mitochondrion: a lattice bean with folded inner ridges
  // ---------------------------------------------------------------------------

  function drawMito(ctx, L, x, y, rot, seed, bi, alpha) {
    if (alpha <= 0.01) return;
    const RX = 30, RY = 14;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    const body = L.ellipsePts(0, 0, RX, RY, 44);
    const bp = new Path2D();
    wob(L, bp, body, seed, 0.5, bi, true);
    fill(ctx, bp, NAVY, 0.7 * alpha);
    fill(ctx, bp, NAVYL, 0.3 * alpha);
    // cristae: a folded ridge running the length of the bean
    const cr = new Path2D();
    for (let i = -3; i <= 3; i++) {
      const px = i * 7.4 + (L.h3(i + 4, bi, seed + 2) - 0.5) * 0.8;
      const h = RY * 0.72 * (1 - 0.5 * Math.pow(Math.abs(px) / RX, 2));
      cr.moveTo(px, -h);
      cr.quadraticCurveTo(px + 3.4, 0, px, h);
    }
    stroke(ctx, cr, LAV, 0.34 * alpha, 1);
    const spine = new Path2D();
    spine.moveTo(-RX + 5, 0);
    spine.lineTo(RX - 5, 0);
    stroke(ctx, spine, LAV, 0.2 * alpha, 1, [4, 6]);
    stroke(ctx, bp, LAV, 0.62 * alpha, 1.5);
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // Network node glyph: a lead line from a point on the cell out to a small round inset
  // ---------------------------------------------------------------------------

  function nodeGlyph(ctx, L, node, k, sx, sy, sr, bi, tRot, content) {
    if (k <= 0) return;
    const kk = clamp(k);
    const cx = node.x, cy = node.y, seed = node.seed;
    const dx = cx - sx, dy = cy - sy;
    const dl = Math.hypot(dx, dy) || 1;
    const ux = dx / dl, uy = dy / dl;
    const ax = sx + ux * sr, ay = sy + uy * sr;
    const bx = cx - ux * (node.r + 8), by = cy - uy * (node.r + 8);
    const mx = (ax + bx) / 2 + uy * 54, my = (ay + by) / 2 - ux * 54;
    const lead = [];
    for (let i = 0; i <= 22; i++) {
      const u = (i / 22) * kk, v = 1 - u;
      lead.push([v * v * ax + 2 * v * u * mx + u * u * bx, v * v * ay + 2 * v * u * my + u * u * by]);
    }
    const lp = new Path2D();
    wob(L, lp, lead, seed + 2, 0.5, bi, false);
    stroke(ctx, lp, LAV, 0.45, 1.2);
    // the ring round the magnified place
    const src = new Path2D();
    src.arc(sx, sy, sr * kk, 0, TAU);
    stroke(ctx, src, LAV, 0.45, 1.2, [4, 5]);

    ctx.save();
    ctx.translate(cx, cy);
    ctx.scale(kk, kk);
    const plate = new Path2D();
    plate.arc(0, 0, node.r, 0, TAU);
    fill(ctx, plate, NAVYD, 0.92);
    fill(ctx, plate, NAVYL, 0.42);
    const rim = new Path2D();
    wob(L, rim, L.ellipsePts(0, 0, node.r, node.r, 56), seed + 3, 0.4, bi, true);
    stroke(ctx, rim, LAV, 0.85, 2);
    const rim2 = new Path2D();
    rim2.arc(0, 0, node.r - 7, 0, TAU);
    stroke(ctx, rim2, LAV, 0.3, 1);
    L.ticks(ctx, 0, 0, { r: node.r + 5, n: 32, len: 4, major: 8, majorLen: 9, color: LAV, alpha: 0.35, width: 1, rot: tRot });
    ctx.save();
    ctx.beginPath();
    ctx.arc(0, 0, node.r - 9, 0, TAU);
    ctx.clip();
    content(ctx);
    ctx.restore();
    ctx.restore();
  }

  // inset 1: the furrow in section, the contractile ring drawing the membrane in
  function furrowInset(ctx, L, k, bi, seed) {
    const R = 49;                     // the inset's own furrow radius
    const tip = lerp(-40, 12, k);     // the notch tip travelling in as the neck closes
    const cxf = tip + R;
    for (const off of [0, 7]) {
      const p = new Path2D();
      wob(L, p, arcPts(cxf + off, 0, R, Math.PI * 0.58, Math.PI * 1.42, 22), seed + off, 0.5, bi, false);
      stroke(ctx, p, LAV, off ? 0.4 : 0.85, off ? 1 : 2.2);
    }
    // the filament band lying along the inner face of the furrow
    const band = new Path2D();
    for (let i = 0; i <= 16; i++) {
      const a = Math.PI * 0.6 + (Math.PI * 0.8 * i) / 16;
      const c = Math.cos(a), s = Math.sin(a);
      const j = (L.h3(i, bi, seed + 5) - 0.5) * 1.2;
      band.moveTo(cxf + c * (R + 9 + j), s * (R + 9 + j));
      band.lineTo(cxf + c * (R + 17 + j), s * (R + 17 + j));
    }
    stroke(ctx, band, WHITE, 0.45 + 0.25 * k, 1.2);
    // three arrows showing the pull
    const ar = new Path2D();
    for (const yy of [-26, 0, 26]) {
      const x0 = -46, x1 = tip - 16 - 10 * (1 - k);
      if (x1 - x0 < 8) continue;
      ar.moveTo(x0, yy);
      ar.lineTo(x1, yy);
      ar.moveTo(x1 - 7, yy - 5);
      ar.lineTo(x1, yy);
      ar.lineTo(x1 - 7, yy + 5);
    }
    stroke(ctx, ar, LAV, 0.55, 1.4);
    // cytoplasm stipple behind the furrow
    L.stipple(ctx, null, {
      bounds: [-46, -46, 92, 92], spacing: 8, r: [1, 1.7], color: LAV, alpha: 0.26,
      seed: seed + 9, density: (x) => sstep(tip + 26, tip - 30, x) * 0.8,
    });
  }

  // inset 2: vesicles gathering along the chromatin edge into a double envelope with pores
  function envelopeInset(ctx, L, k, bi, seed) {
    // the chromatin the envelope is laid against
    L.stipple(ctx, null, {
      bounds: [-46, 4, 92, 46], spacing: 6.5, r: [1, 1.9], color: LAV, alpha: 0.35,
      seed: seed + 11, density: (x, y) => sstep(6, 30, y) * 0.9,
    });
    const nV = 7;
    const merged = clamp((k - 0.45) / 0.55);
    for (let i = 0; i < nV; i++) {
      const cx = -42 + (84 * i) / (nV - 1);
      const grow = clamp((k - 0.08 * i) * 1.5);
      if (grow <= 0) continue;
      const w = lerp(7, 84 / (nV - 1) / 2 + 1.5, merged) * grow;
      const h = lerp(6.5, 3.4, merged);
      const yy = lerp(-14 - 5 * L.h3(i, 1, seed), -4, merged);
      const v = new Path2D();
      v.ellipse(cx, yy, w, h, 0, 0, TAU);
      fill(ctx, v, NAVY, 0.6);
      stroke(ctx, v, LAV, 0.75, 1.4);
    }
    if (merged > 0.2) {
      const a = (merged - 0.2) / 0.8;
      const l1 = new Path2D();
      wob(L, l1, [[-46, -8], [-14, -8.6], [16, -7.6], [46, -8]], seed + 21, 0.5, bi, false);
      const l2 = new Path2D();
      wob(L, l2, [[-46, 0], [-14, -0.6], [16, 0.4], [46, 0]], seed + 22, 0.5, bi, false);
      stroke(ctx, l1, LAV, 0.85 * a, 2);
      stroke(ctx, l2, LAV, 0.6 * a, 1.6);
      const pores = new Path2D();
      for (const px of [-28, 2, 30]) {
        pores.moveTo(px - 5, -9.5);
        pores.lineTo(px - 5, 1.5);
        pores.moveTo(px + 5, -9.5);
        pores.lineTo(px + 5, 1.5);
      }
      stroke(ctx, pores, WHITE, 0.7 * a, 1.3);
    }
  }

  // ---------------------------------------------------------------------------
  // Section band below the safe area: the furrow seen in section across the membrane,
  // its notch deepening with the pinch. Construction, so it runs full bleed.
  // ---------------------------------------------------------------------------

  const SEC_Y = 1706;

  function sectionProfile(x, depth) {
    const u = (x - CX) / 210;
    return SEC_Y + depth * Math.exp(-u * u * 1.35);
  }

  function drawFurrowSection(ctx, L, k, bi, seed) {
    const depth = lerp(14, 148, k);
    const outer = [], inner = [];
    for (let x = -20; x <= 1100; x += 8) {
      const y = sectionProfile(x, depth);
      outer.push([x, y]);
      inner.push([x, sectionProfile(x, depth * 0.94) + 11]);
    }
    // the two leaves of the membrane
    const op = new Path2D();
    wob(L, op, outer, seed + 1, 0.5, bi, false);
    const ip = new Path2D();
    wob(L, ip, inner, seed + 2, 0.4, bi, false);
    // the ladder between them
    const rung = new Path2D();
    for (let i = 1; i < outer.length - 1; i += 2) {
      const j = (L.h3(i, bi, seed + 3) - 0.5) * 0.9;
      rung.moveTo(outer[i][0] + j, outer[i][1]);
      rung.lineTo(inner[i][0] + j, inner[i][1]);
    }
    stroke(ctx, rung, LAV, 0.2, 1);
    stroke(ctx, ip, LAV, 0.3, 1.1);
    stroke(ctx, op, LAV, 0.5, 2);

    // the contractile filament band lying under the notch, tightening as the furrow deepens
    const fil = new Path2D();
    for (let i = 0; i < outer.length; i++) {
      const x = outer[i][0];
      const w = Math.exp(-(((x - CX) / 210) ** 2) * 1.35);
      if (w < 0.22) continue;
      const y = sectionProfile(x, depth * 0.94) + 13;
      const l = 6 + 10 * w * k;
      const j = (L.h3(i, bi, seed + 4) - 0.5) * 1.2;
      fil.moveTo(x + j, y);
      fil.lineTo(x + j, y + l);
    }
    stroke(ctx, fil, WHITE, 0.32 + 0.22 * k, 1.2);

    // cytoplasm under the membrane
    L.stipple(ctx, (c) => {
      c.moveTo(-20, 1920);
      for (const p of inner) c.lineTo(p[0], p[1] + 26);
      c.lineTo(1100, 1920);
      c.closePath();
    }, {
      bounds: [0, SEC_Y, 1080, 1920 - SEC_Y], spacing: 8, r: [1, 1.7],
      color: LAV, alpha: 0.24, seed: seed + 5,
      density: (x, y) => 0.75 * sstep(1920, SEC_Y + 20, y),
    });

    // depth bracket at the left, and a tick scale along the band
    L.bracket(ctx, 168, SEC_Y, 168, SEC_Y + depth, { cap: 12, alpha: 0.4, color: LAV, width: 1.2 });
    const ext = new Path2D();
    ext.moveTo(176, SEC_Y);
    ext.lineTo(330, SEC_Y);
    ext.moveTo(176, SEC_Y + depth);
    ext.lineTo(CX - 120, SEC_Y + depth);
    stroke(ctx, ext, LAV, 0.18, 1, [5, 7]);
    L.ticks(ctx, 60, SEC_Y - 46, { kind: 'linear', length: 960, angle: 0, n: 32, len: 6, major: 8, majorLen: 13, side: 1, baseline: false, color: LAV, alpha: 0.22, width: 1 });
  }

  // ---------------------------------------------------------------------------
  // Tally plate: four marks per daughter, lighting on the bell arpeggio as each
  // envelope closes — two long (pair A) and two short (pair B), so the set reads as
  // two pairs. The film's other counters (02, 03, 10) use the same language.
  // ---------------------------------------------------------------------------

  function drawTally(ctx, L, lit, bi, seed) {
    const x0 = 96, y0 = 236, w = 132, h = 138;
    const plate = new Path2D();
    plate.moveTo(x0 + 9, y0);
    plate.arcTo(x0 + w, y0, x0 + w, y0 + 9, 9);
    plate.arcTo(x0 + w, y0 + h, x0 + w - 9, y0 + h, 9);
    plate.arcTo(x0, y0 + h, x0, y0 + h - 9, 9);
    plate.arcTo(x0, y0, x0 + 9, y0, 9);
    plate.closePath();
    fill(ctx, plate, NAVYD, 0.86);
    fill(ctx, plate, NAVYL, 0.4);
    stroke(ctx, plate, LAV, 0.25, 1);
    // the divider: one column per daughter
    const div = new Path2D();
    div.moveTo(x0 + w / 2, y0 + 12);
    div.lineTo(x0 + w / 2, y0 + h - 12);
    stroke(ctx, div, LAV, 0.22, 1, [4, 6]);

    for (let col = 0; col < 2; col++) {
      for (let j = 0; j < 4; j++) {
        const cx = x0 + 34 + col * 64;
        const cy = y0 + 28 + j * 28;
        const long = j < 2;                   // two long (pair A), two short (pair B)
        const half = long ? 19 : 12;
        const k = lit[col][j];
        const slot = new Path2D();
        slot.moveTo(cx - half, cy);
        slot.lineTo(cx + half, cy);
        stroke(ctx, slot, LAV, 0.22, 1);
        if (k <= 0) continue;
        const kk = Math.min(1.15, k);
        const mark = new Path2D();
        const bow = (long ? 5 : 3.4) * (L.h3(col, j, seed) > 0.5 ? 1 : -1);
        mark.moveTo(cx - half * kk, cy + bow * 0.4);
        mark.quadraticCurveTo(cx, cy - bow, cx + half * kk, cy + bow * 0.4);
        stroke(ctx, mark, WHITE, 0.92, long ? 3.4 : 3);
        const dot = new Path2D();
        dot.moveTo(cx + 2.4, cy);
        dot.arc(cx, cy, 2.4, 0, TAU);
        fill(ctx, dot, NAVYD, 0.9);
      }
    }
  }

  // ---------------------------------------------------------------------------
  // Scene
  // ---------------------------------------------------------------------------

  FILM.scene({
    id: ID,
    draw(ctx, tIn, info) {
      const L = info.lib;
      const dur = info.dur;
      // snap near-frame times onto the frame grid so beat tests never miss by one ulp
      let t = clamp(tIn, 0, dur);
      const tF = Math.round(t * 24) / 24;
      if (Math.abs(t - tF) < 1e-4) t = tF + 1e-7;
      const tw = L.onTwos(t);
      const bi = L.boil(info.T);
      const g = geo(L);
      const SEED = L.hash(ID) & 0xffff;

      // beats, shot-local (global T in the comments)
      const B_MEM_U = 0.5;     // T 19.50  upper envelope draws round
      const B_MEM_L = 0.75;    // T 19.75  lower envelope
      const B_DISS = 1.0;      // T 20.00  fibres dissolve, chromosomes relax
      const B_PINCH = 1.5;     // T 20.50  the furrow starts, first magenta ring
      const B_FUR2 = 2.0;      // T 21.00  second furrow ring
      const T_G4 = 2.375;      // T 21.375 the G4 pose, held to the cut

      const drawingOf = (a) => Math.floor((t - a) * 12 + 1e-6);
      const hit = (a, frames, e, lead) => {
        if (t < a) return 0;
        const u = clamp((t - a) / (frames * FR) + (lead == null ? 1 : lead) / frames);
        return e ? e(u) : u;
      };

      const kMemU = hit(B_MEM_U, 8, E.outExpo);
      const kMemL = hit(B_MEM_L, 8, E.outExpo);
      const kDiss = seg(t, B_DISS, 6);
      const kDust = seg(t, B_DISS, 11);
      const kRelax = E.inOutSine(clamp((tw - B_DISS) / (12 * FR)));
      const kPinch = E.inOutCubic(clamp((tw - B_PINCH) / (T_G4 - B_PINCH)));
      const kPole = 1 - seg(t, B_DISS, 8);
      const kNucleolus = hit(2.0, 4, E.outBack);

      const HH = halfHeight(kPinch);
      const yTop = EQ - HH, yBot = EQ + HH;
      const neckHW = halfWidth(0, kPinch);

      // ---- 1 plate -----------------------------------------------------------
      L.blueprint(ctx, { center: [CX, EQ], circles: 0, diagonals: 0, seed: 309, noise: 0.9 });

      // ---- 2 guide geometry ---------------------------------------------------
      ctx.save();
      ctx.translate(CX, EQ);
      ctx.rotate(6 * DEG * (t / dur));
      L.guideCircle(ctx, 0, 0, 470, { alpha: 0.13, width: 1.5 });
      L.ticks(ctx, 0, 0, { r: 470, n: 120, len: 6, major: 10, majorLen: 15, inward: true, color: LAV, alpha: 0.18, width: 1 });
      L.guideCircle(ctx, 0, 0, 640, { alpha: 0.08, width: 1.5 });
      L.guideCircle(ctx, 0, 0, 652, { alpha: 0.09, width: 1, dash: [2, 9] });
      for (let q = 0; q < 4; q++) {
        const a = q * 90 * DEG + 24 * DEG;
        L.arcAnnotation(ctx, 0, 0, 488, a, a + 30 * DEG, { color: LAV, alpha: 0.16, width: 1.2, endTicks: 10 });
      }
      ctx.restore();

      const diag = new Path2D();
      diag.moveTo(0, 0);
      diag.lineTo(1080, 1920);
      diag.moveTo(1080, 0);
      diag.lineTo(0, 1920);
      stroke(ctx, diag, LAV, 0.12, 1);

      // the long axis and the equator: construction lines that stop at the outline
      const axis = new Path2D();
      axis.moveTo(CX, 180);
      axis.lineTo(CX, 1640);
      stroke(ctx, axis, LAV, 0.14, 1, [10, 9]);

      const eqLine = new Path2D();
      eqLine.moveTo(56, EQ);
      eqLine.lineTo(CX - neckHW - 22, EQ);
      eqLine.moveTo(CX + neckHW + 22, EQ);
      eqLine.lineTo(1024, EQ);
      stroke(ctx, eqLine, LAV, 0.3, 1.2, [12, 9]);
      L.ticks(ctx, 96, EQ, { kind: 'linear', length: 888, angle: 0, n: 24, len: 7, major: 6, majorLen: 14, side: -1, baseline: false, color: LAV, alpha: 0.22, width: 1 });

      // registration crosses on the axis and at the plate ends
      const reg = new Path2D();
      for (const [x, y] of [[CX, 260], [CX, 1540], [76, EQ], [1004, EQ]]) {
        reg.moveTo(x - 10, y);
        reg.lineTo(x + 10, y);
        reg.moveTo(x, y - 10);
        reg.lineTo(x, y + 10);
      }
      stroke(ctx, reg, LAV, 0.38, 1.2);

      // the top scale strip, with a section arrow at each end pointing at the plate below
      L.ticks(ctx, 60, 186, { kind: 'linear', length: 960, angle: 0, n: 40, len: 7, major: 5, majorLen: 15, side: 1, color: LAV, alpha: 0.26, width: 1 });
      const sec = new Path2D();
      for (const sg of [1, -1]) {
        const x = sg > 0 ? 24 : 1056;
        sec.moveTo(x, 178);
        sec.lineTo(x + sg * 18, 186);
        sec.lineTo(x, 194);
        sec.closePath();
      }
      fill(ctx, sec, LAV, 0.45);

      // ---- 2b the furrow in section, below the safe area -----------------------
      drawFurrowSection(ctx, L, kPinch, bi, SEED + 500);

      // ---- 3 target construction ----------------------------------------------
      // the two lobe circles the outline is travelling toward, struck once the envelopes exist
      const kTarget = hit(B_MEM_U, 8, E.outCubic);
      if (kTarget > 0) {
        for (const cy of [CY_U, CY_L]) {
          L.guideCircle(ctx, CX, cy, R_LOBE, { alpha: 0.16 * kTarget, width: 1.2, dash: [7, 9], p: kTarget });
          L.guideCircle(ctx, CX, cy, R_NUC, { alpha: 0.2 * kTarget, width: 1, dash: [3, 6], p: kTarget, cross: 14 });
        }
      }
      // the furrow circles: the arcs the membrane is being pulled onto
      const kFur = hit(B_PINCH - 0.25, 6, E.outCubic);
      if (kFur > 0) {
        for (const sg of [-1, 1]) {
          L.guideCircle(ctx, CX + sg * D_FUR, EQ, R_FUR, { alpha: 0.26 * kFur, width: 1.2, dash: [5, 6], p: kFur });
        }
        const pull = new Path2D();
        for (const sg of [-1, 1]) {
          const x0 = CX + sg * (neckHW + 150), x1 = CX + sg * (neckHW + 30);
          pull.moveTo(x0, EQ);
          pull.lineTo(x1, EQ);
          pull.moveTo(x1 + sg * 10, EQ - 7);
          pull.lineTo(x1, EQ);
          pull.lineTo(x1 + sg * 10, EQ + 7);
        }
        stroke(ctx, pull, LAV, 0.4 * kFur, 1.4);
      }

      // ---- 4 cytoplasm ---------------------------------------------------------
      const out = outlinePts(kPinch, 1);
      const outCoarse = outlinePts(kPinch, 4);
      const traceOut = (c) => L.tracePath(c, outCoarse, true);

      ctx.save();
      ctx.beginPath();
      traceOut(ctx);
      ctx.clip();
      ctx.fillStyle = NAVY;
      ctx.globalAlpha = 0.5;
      ctx.fillRect(120, yTop - 10, 840, yBot - yTop + 20);
      // an inner light in each half, so the two daughters read as separate bodies
      ctx.globalCompositeOperation = 'lighter';
      for (const cy of [CY_U, CY_L]) {
        const gl = ctx.createRadialGradient(CX - 60, cy - 60, 20, CX, cy, 380);
        gl.addColorStop(0, L.rgba(LAV, 0.085));
        gl.addColorStop(0.55, L.rgba(LAV, 0.03));
        gl.addColorStop(1, L.rgba(LAV, 0));
        ctx.fillStyle = gl;
        ctx.fillRect(CX - 400, cy - 400, 800, 800);
      }
      ctx.restore();

      // ribosome stipple, clear of the two nuclei
      const nucGuard = (x, y) => {
        const du = Math.hypot(x - CX, y - CY_U), dl = Math.hypot(x - CX, y - CY_L);
        const ku = kMemU > 0 ? sstep(R_NUC - 6, R_NUC + 22, du) : 1;
        const kl = kMemL > 0 ? sstep(R_NUC - 6, R_NUC + 22, dl) : 1;
        return Math.min(ku, kl);
      };
      L.stipple(ctx, traceOut, {
        bounds: [CX - 400, yTop, 800, yBot - yTop],
        spacing: 8.5, r: [1.0, 2.0], color: LAV, alpha: 0.3, seed: g.stippleSeed,
        density: (x, y) => 0.42 * nucGuard(x, y) * (0.72 + 0.28 * sstep(0, 260, Math.hypot(x - CX, (y - EQ) * 0.6))),
      });

      // six mitochondria drifting into their own daughter as the cell pinches
      const kMito = E.inOutCubic(clamp((tw - B_PINCH + 0.25) / (T_G4 - B_PINCH + 0.25)));
      for (let i = 0; i < MITO.length; i++) {
        const m = MITO[i];
        const mx = lerp(m.x0, m.x1, kMito);
        const my = lerp(m.y0, m.y1, kMito);
        drawMito(ctx, L, mx, my, lerp(m.r0, m.r1, kMito) * DEG, SEED + 140 + i * 17, bi, 1);
      }

      // ---- 5 spindle -----------------------------------------------------------
      // chromosome poses first: the fibres end on the centromeres
      const sets = [];
      for (let s = 0; s < 2; s++) {
        const cyArr = s === 0 ? CY_U : CY_L;
        const ap = s === 0 ? 1 : -1;     // the apex leads toward this set's pole
        const list = [];
        for (let i = 0; i < 4; i++) {
          const spec = SET[i];
          list.push({
            spec,
            cx0: spec.ax, cy0: cyArr + spec.ady,
            cx1: CX + spec.dx, cy1: cyArr + spec.dy,
            ap, seed: g.chrSeed[s][i],
          });
        }
        sets.push({ list, cy: cyArr, pole: s === 0 ? POLE_U : POLE_L });
      }
      // the centromere of each chromosome at this frame (fibre attachment, art bible 10.5)
      const cmOf = (c) => {
        const K = KIND[c.spec.kind];
        const vApex = [c.cx0, c.cy0 - c.ap * K.vh];
        const wMid = [c.cx1, c.cy1];
        return [lerp(vApex[0], wMid[0], kRelax), lerp(vApex[1], wMid[1], kRelax)];
      };

      if (kPole > 0.01) {
        // free fibres and centromere fibres, trembling on the boil, then dissolving into stipple
        const fib = new Path2D();
        const dust = new Path2D();
        const lineA = clamp(1 - kDiss * 1.7);
        const dustA = kDust > 0 && kDust < 1 ? 0.5 * (1 - kDust) : 0;

        const addFibre = (x0, y0, x1, y1, bow, seed) => {
          const dx = x1 - x0, dy = y1 - y0;
          const dl = Math.hypot(dx, dy) || 1;
          const nx = -dy / dl, ny = dx / dl;
          const tremble = bow + (L.h3(seed, bi, 91) - 0.5) * 4;
          const pts = [];
          const n = 18;
          for (let i = 0; i <= n; i++) {
            const u = i / n;
            const b = Math.sin(u * Math.PI) * tremble;
            pts.push([x0 + dx * u + nx * b, y0 + dy * u + ny * b]);
          }
          if (lineA > 0.01) addPoly(fib, pts, false);
          if (dustA > 0) {
            for (let i = 1; i < n; i += 2) {
              const p = pts[i];
              const a = L.h3(seed, i, 77) * TAU;
              const d = 34 * kDust * (0.4 + 0.6 * L.h3(i, seed, 78));
              dust.moveTo(p[0] + Math.cos(a) * d + 1.3, p[1] + Math.sin(a) * d);
              dust.arc(p[0] + Math.cos(a) * d, p[1] + Math.sin(a) * d, 1.3, 0, TAU);
            }
          }
        };

        for (const f of g.free) addFibre(f.x0, f.y0, f.x1, f.y1, f.bow, f.seed);
        for (const st of sets) {
          for (const c of st.list) {
            const cm = cmOf(c);
            addFibre(CX, st.pole, cm[0], cm[1], (c.spec.ax - CX) * 0.04, c.seed + 41);
          }
        }
        // the spindle lives inside the cell: everything is clipped to the membrane
        ctx.save();
        ctx.beginPath();
        traceOut(ctx);
        ctx.clip();
        stroke(ctx, fib, WHITE, 0.45 * lineA * kPole, 2);
        if (dustA > 0) fill(ctx, dust, LAV, dustA);
        ctx.restore();

        // the two poles: a 22 px disc with 12 radial ticks, and 08's arrival ring still fading
        for (let s = 0; s < 2; s++) {
          const py = s === 0 ? POLE_U : POLE_L;
          const ring = seg(t, 0, 8);
          if (ring < 1) {
            const rp = new Path2D();
            rp.arc(CX, py, lerp(58, 156, E.outExpo(ring)), 0, TAU);
            stroke(ctx, rp, WHITE, 0.4 * (1 - ring) * (1 - ring), 2.5);
          }
          const disc = new Path2D();
          wob(L, disc, L.ellipsePts(CX, py, 22, 22, 36), g.poleSeed[s], 0.6, bi, true);
          fill(ctx, disc, NAVYD, 0.7 * kPole);
          stroke(ctx, disc, LAV, 0.8 * kPole, 1.8);
          L.ticks(ctx, CX, py, {
            r: 26, n: 12, len: 14, major: 3, majorLen: 22,
            rot: (bi % 4) * 7.5 * DEG, color: WHITE, alpha: 0.6 * kPole, width: 1.5,
          });
          L.glowDot(ctx, CX, py, 8, { rays: 0, glow: 3.4, color: GLOW, intensity: 0.7 * kPole, seed: g.poleSeed[s] + 3, twinkle: 0.12 });
        }
      }

      // ---- 6 nucleus interiors -------------------------------------------------
      drawNucleusFill(ctx, L, CX, CY_U, kMemU, SEED + 200, bi);
      drawNucleusFill(ctx, L, CX, CY_L, kMemL, SEED + 300, bi);

      // ---- 7 chromosomes -------------------------------------------------------
      for (let s = 0; s < 2; s++) {
        for (const c of sets[s].list) {
          drawChromosome(ctx, L, c.spec, c.cx0, c.cy0, c.cx1, c.cy1, c.ap, kRelax, c.seed, bi, 1);
        }
      }

      // ---- 8 nuclear envelopes, then the nucleoli ------------------------------
      drawNucleusRim(ctx, L, CX, CY_U, kMemU, SEED + 200, bi);
      drawNucleusRim(ctx, L, CX, CY_L, kMemL, SEED + 300, bi);
      if (kNucleolus > 0) {
        for (const cy of [CY_U, CY_L]) {
          const nx = CX + g.nucleolus[0], ny = cy + g.nucleolus[1];
          const k = Math.min(1.12, kNucleolus);
          L.stipple(ctx, (c) => c.arc(nx, ny, 16 * k, 0, TAU), {
            bounds: [nx - 20, ny - 20, 40, 40], spacing: 4.4, r: [1, 1.6], color: LAV, alpha: 0.5, seed: SEED + 411,
          });
          const ring = new Path2D();
          ring.arc(nx, ny, 16 * k, 0, TAU);
          stroke(ctx, ring, LAV, 0.5, 1.2);
          L.glowDot(ctx, nx, ny, 8 * k, { rays: 0, glow: 3.2, color: GLOW, intensity: 0.85, seed: SEED + 412, twinkle: 0.1 });
          L.ticks(ctx, nx, ny, { r: 24 * k, n: 12, len: 6, color: WHITE, alpha: 0.4, width: 1, rot: (bi % 4) * 7.5 * DEG });
        }
      }

      // ---- 9 the cell outline --------------------------------------------------
      const inn = innerPts(kPinch, 2);
      const outerP = new Path2D();
      wob(L, outerP, out, SEED + 1, 0.7, bi, true);
      const innerP = new Path2D();
      wob(L, innerP, inn, SEED + 2, 0.5, bi, true);
      // the membrane ladder between the two lines
      const rung = new Path2D();
      const half = out.length / 2;
      for (let i = 4; i < half - 4; i += 6) {
        const o1 = out[i], o2 = out[out.length - 1 - i];
        const i1 = inn[Math.min(inn.length - 1, Math.round((i * inn.length) / out.length))];
        const i2 = inn[inn.length - 1 - Math.min(inn.length - 1, Math.round((i * inn.length) / out.length))];
        rung.moveTo(o1[0], o1[1]);
        rung.lineTo(i1[0], i1[1]);
        rung.moveTo(o2[0], o2[1]);
        rung.lineTo(i2[0], i2[1]);
      }
      stroke(ctx, rung, LAV, 0.22, 1);
      stroke(ctx, innerP, LAV, 0.5, 1.5);
      ctx.save();
      ctx.globalCompositeOperation = 'lighter';
      stroke(ctx, outerP, LAV, 0.05, 15);
      stroke(ctx, outerP, LAV, 0.07, 7);
      ctx.restore();
      stroke(ctx, outerP, LAV, 0.85, 2.5);

      // ---- 10 measurement ------------------------------------------------------
      // the left ruler and the whole-cell height bracket, tracking the poles
      L.ticks(ctx, 60, 250, { kind: 'linear', length: 1300, angle: Math.PI / 2, n: 32, len: 9, major: 4, majorLen: 20, side: -1, color: LAV, alpha: 0.35, width: 1.2 });
      L.bracket(ctx, 142, yTop, 142, yBot, { cap: 16, alpha: 0.5, color: LAV, width: 1.4 });
      const ext = new Path2D();
      ext.moveTo(150, yTop);
      ext.lineTo(CX - 14, yTop);
      ext.moveTo(150, yBot);
      ext.lineTo(CX - 14, yBot);
      stroke(ctx, ext, LAV, 0.2, 1, [5, 7]);

      // the neck: the measurement that carries the shot
      L.bracket(ctx, CX - neckHW, EQ, CX + neckHW, EQ, { cap: 15, alpha: 0.75, color: LAV, width: 1.5 });
      const neckExt = new Path2D();
      for (const sg of [-1, 1]) {
        neckExt.moveTo(CX + sg * neckHW, EQ - 9);
        neckExt.lineTo(CX + sg * neckHW, EQ - 26);
        neckExt.moveTo(CX + sg * neckHW, EQ + 9);
        neckExt.lineTo(CX + sg * neckHW, EQ + 26);
      }
      stroke(ctx, neckExt, WHITE, 0.45, 1.2);

      // one bracket per new nucleus, with its extension lines and rim ticks
      for (let s = 0; s < 2; s++) {
        const cy = s === 0 ? CY_U : CY_L;
        const k = s === 0 ? kMemU : kMemL;
        if (k <= 0) continue;
        const kk = clamp(k);
        L.bracket(ctx, 900, cy - R_NUC, 900, cy + R_NUC, { cap: 15, alpha: 0.55, color: LAV, width: 1.4, p: kk });
        const e2 = new Path2D();
        for (const sg of [-1, 1]) {
          e2.moveTo(CX + 30, cy + sg * R_NUC);
          e2.lineTo(884, cy + sg * R_NUC);
        }
        stroke(ctx, e2, LAV, 0.2 * kk, 1, [5, 7]);
        L.ticks(ctx, CX, cy, { r: R_NUC + 12, n: 36, len: 6, major: 9, majorLen: 13, color: LAV, alpha: 0.3 * kk, width: 1, p: kk });
      }

      // ---- 11 magenta: the moments of change ----------------------------------
      const ring = (x, y, a, frames, r0, r1, w, alpha) => {
        if (t < a || t >= a + frames * FR) return;
        const u = (t - a) / (frames * FR);
        ctx.save();
        ctx.beginPath();
        ctx.arc(x, y, lerp(r0, r1, E.outExpo(u + 0.5 / frames)), 0, TAU);
        ctx.strokeStyle = MAG;
        ctx.globalAlpha = (alpha == null ? 1 : alpha) * (1 - u * u);
        ctx.lineWidth = w;
        ctx.stroke();
        ctx.restore();
      };
      // each envelope closing: the nucleus has divided
      ring(CX, CY_U, B_MEM_U + 8 * FR, 6, R_NUC - 10, R_NUC + 70, 3);
      ring(CX, CY_L, B_MEM_L + 8 * FR, 6, R_NUC - 10, R_NUC + 70, 3);
      // the furrow, on both pinch beats
      for (const a of [B_PINCH, B_FUR2]) {
        ring(CX, EQ, a, 8, 40, 260, 3, 0.9);
        if (t >= a && t < a + 8 * FR) {
          const u = (t - a) / (8 * FR);
          const arc = new Path2D();
          for (const sg of [-1, 1]) {
            const r = lerp(70, 150, E.outExpo(u + 0.06));
            arc.moveTo(CX + sg * (neckHW + 6), EQ - r * 0.5);
            arc.quadraticCurveTo(CX + sg * (neckHW - 14), EQ, CX + sg * (neckHW + 6), EQ + r * 0.5);
          }
          stroke(ctx, arc, MAG, 1 - u * u, 3);
        }
      }

      // ---- 12 network insets ---------------------------------------------------
      const kNodeF = hit(B_PINCH - 0.125, 4, E.outBack);
      nodeGlyph(ctx, L, g.node.furrow, kNodeF, CX - neckHW - 6, EQ, 34, bi, t * 0.35, (c) => furrowInset(c, L, kPinch, bi, g.node.furrow.seed));
      const kNodeE = hit(B_MEM_L, 4, E.outBack);
      nodeGlyph(ctx, L, g.node.envelope, kNodeE, CX + 96, CY_L + 96, 30, bi, -t * 0.3, (c) => envelopeInset(c, L, kMemL, bi, g.node.envelope.seed));

      // ---- 12b the tally: four chromosomes now sit in each new nucleus ---------
      const litMarks = [[], []];
      for (let col = 0; col < 2; col++) {
        const a0 = (col === 0 ? B_MEM_U : B_MEM_L) + 6 * FR;
        for (let j = 0; j < 4; j++) litMarks[col].push(hit(a0 + j * 0.0625, 3, E.outBack));
      }
      drawTally(ctx, L, litMarks, bi, SEED + 600);

      // ---- 13 the cycle glyph (the film's time device; the helper is never re-implemented) ----
      const plate = new Path2D();
      plate.arc(900, 300, 76, 0, TAU);
      fill(ctx, plate, NAVYD, 0.9);
      fill(ctx, plate, NAVYL, 0.38);
      stroke(ctx, plate, LAV, 0.25, 1);
      L.ticks(ctx, 900, 300, { r: 76, n: 48, len: 4, major: 12, majorLen: 9, color: LAV, alpha: 0.3, width: 1 });
      L.cycleGlyph(ctx, info.T, 'schematic');
    },
  });
})();
