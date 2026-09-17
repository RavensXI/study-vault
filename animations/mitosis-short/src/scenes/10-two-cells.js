// 10 two-cells : Two cells, then a pull-back to the tissue.
// T 21.5 to 25.5 (4.0 s, 96 frames), illustrated paper plate, enters on a flash (core draws it).
//
// Frame 0 is the G4 pose drawn screen-fixed: two near-circles on (540, 560) and (540, 1240),
// radius 300, still joined by a 60 px neck at y 900. The neck closes over three drawings on the
// beat, each membrane seals with a small yellow ring, an annBlue arc labelled 'identical' joins
// the two nuclei and the tally ring flips one tick to two. From T 22.5 the camera pulls back to
// zoom 0.45 about (540, 900) while two dozen neighbour cells pop in on 16ths, outward from the
// centre; four of them are mid-division at four different stages. The last frame is held clean.
//
// Layers, back to front:
//   1  stripes (stripeCream / stripeYellow), screen-fixed, drifting 6 px a beat
//   2  construction lines on the G4 pose (inkFaint), under the camera
//   3  tissue: 24 neighbour cells, farthest first
//   4  the two daughter cells in full detail
//   5  overlays, screen-fixed: seal rings, the 'identical' arc, the tally ring, the target frame
//   6  the cycle glyph (FILM.lib.cycleGlyph, never re-implemented)
//
// ===========================================================================================
// HANDOVER TO SHOT 11 — everything shot 11 needs to open on this shot's last frame
// ===========================================================================================
// Camera at T 25.5 : lib.camera(ctx, { x: 540, y: 900 + 60 / 0.45, zoom: 0.45 }, ...)
//   so world (540, 900) is pinned at screen (540, 900) and screen = 540 + (x - 540) * z,
//   900 + (y - 900) * z. The visible world rectangle is x -660..1740, y -1100..3167.
// Background : lib.stripes, colors [stripeCream, stripeYellow], width 140, angle -0.52,
//   offset 12 * T, seed lib.hash('two-cells', 'stripes'), screen-fixed (it does not ride the camera).
// The pair    : upper daughter centre (540, 560) r 300, lower daughter centre (540, 1240) r 300,
//   each with a nucleus r 135 holding four single-copy chromosomes (two chromoA, two chromoB)
//   in the G1 arrangement scaled 0.8, and four mitochondria. 11 pushes into the LOWER daughter.
// Tissue      : the TISSUE table below — 24 rows of [x, y, r, stage]. Copy it verbatim, with the
//   pressing rule: a tissue cell is DRAWN at r + 40 (r + 8 if it is dividing) and then cut back
//   where it meets another cell, on the radical plane between the two drawn radii less 7 px, and
//   round each daughter at its 300 px radius plus 13 px. That is what gives the field its flat
//   contact faces; see pressedBlobPts. Cell i's own wobble seed is lib.hash('two-cells','tissue',i).
// Overlays at the last frame : the annYellow tally ring at (180, 300) showing two ticks, the
//   annBlue target frame around the pair (screen 405..675 x 612..1188), the cycle glyph at
//   (900, 300) fully lit. The 'identical' arc and the seal rings have gone by T 23.75.
// ===========================================================================================
(function () {
  'use strict';

  const ID = 'two-cells';
  const LIB = FILM.lib;
  const PAL = LIB.pal;
  const TAU = Math.PI * 2;
  const DEG = Math.PI / 180;
  const FR = 1 / 24;

  // ---------------------------------------------------------------------------
  // small maths
  // ---------------------------------------------------------------------------

  const lerp = (a, b, t) => a + (b - a) * t;
  const clamp = (v, lo = 0, hi = 1) => (v < lo ? lo : v > hi ? hi : v);
  const sstep = (a, b, x) => {
    const t = clamp((x - a) / (b - a));
    return t * t * (3 - 2 * t);
  };
  const sd = (...k) => LIB.hash(ID, ...k) & 0x7fffffff;
  const outExpo = (p) => (p >= 1 ? 1 : 1 - Math.pow(2, -10 * clamp(p)));
  const outBack = (p) => {
    p = clamp(p);
    return 1 + 2.70158 * Math.pow(p - 1, 3) + 1.70158 * Math.pow(p - 1, 2);
  };
  const inOutCubic = (p) => ((p = clamp(p)), p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2);
  // Math.hypot is not bit-stable across V8's optimisation tiers: the same call can differ by one
  // last-place bit once a long render has tiered up, which moves a pixel and fails the frame hash.
  const hyp = (x, y) => Math.sqrt(x * x + y * y);
  // and anything that feeds a whole frame's geometry is quantised, so a last-place bit cannot ripple
  const q6 = (v) => Math.round(v * 1e6) / 1e6;

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

  function strokePoly(ctx, pts, color, width, alpha = 1, closed = true) {
    ctx.save();
    ctx.globalAlpha *= alpha;
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.beginPath();
    trace(ctx, pts, closed);
    ctx.stroke();
    ctx.restore();
  }

  // ===========================================================================================
  // 1. SHARED GEOMETRY
  // ===========================================================================================

  // G4 (storyboard): the pinched cell at T 21.5 and the two daughters it becomes.
  const CX = 540;              // the frame's centre line, the pair's axis
  const G4 = {
    upperY: 560,               // upper daughter centre
    lowerY: 1240,              // lower daughter centre
    midY: 900,                 // the furrow, and the point the pull-back is centred on
    r: 300,                    // each daughter's mean radius
    neckHalf: 30,              // half the 60 px neck at T 21.5
    nucR: 135,                 // each daughter's nucleus radius
  };

  // G1's four chromosomes, written as fractions of the nucleus radius so the same table serves
  // the daughters (nucleus 135) and every neighbour nucleus. Two pairs: A long blue, B short rust.
  // G1: A1 (470, 850) and A2 (610, 850) 130 px long; B1 (480, 955) and B2 (600, 955) 85 px long,
  // all at 20 degrees off horizontal, alternately left and right, about the nucleus centre (540, 900).
  const CHROMO = [
    { key: 'A1', gx: -70 / 170, gy: -50 / 170, gl: 130 / 170, ang: 20 * DEG, pair: 'A' },
    { key: 'A2', gx: 70 / 170, gy: -50 / 170, gl: 130 / 170, ang: -20 * DEG, pair: 'A' },
    { key: 'B1', gx: -60 / 170, gy: 55 / 170, gl: 85 / 170, ang: 20 * DEG, pair: 'B' },
    { key: 'B2', gx: 60 / 170, gy: 55 / 170, gl: 85 / 170, ang: -20 * DEG, pair: 'B' },
  ];
  const NUCLEOLUS = { gx: -40 / 170, gy: -30 / 170, gr: 40 / 170 };

  // Mitochondria shared out between the daughters: four each, offsets from the cell centre.
  // They are not genetic, so the two daughters may hold different ones; the nuclei are identical.
  const MITO_UPPER = [
    [-175, -110, 0.45], [160, -140, -0.75], [-120, 165, -0.3], [185, 95, 1.15],
  ];
  const MITO_LOWER = [
    [-190, 85, 0.2], [150, -155, 0.9], [-105, -175, -0.55], [165, 150, -1.0],
  ];
  const MITO_LEN = 48, MITO_W = 22;

  // ---------------------------------------------------------------------------
  // THE TISSUE TABLE — 24 neighbour cells in world coordinates.
  // Copy this table verbatim into shot 11: it is the field 11 opens on.
  //   [ x, y, radius, stage ]   stage: null = interphase (a nucleus with four loose chromosomes)
  //                             'spindle'    = metaphase, chromosomes on a plate between two poles
  //                             'pinchEarly' = a shallow furrow, two nuclei
  //                             'pinchMid'   = a deeper furrow
  //                             'pinchLate'  = a thread of a neck, about to part
  // Rows are in pop-in order: nearest the centre (540, 900) first. Minimum clearance between any
  // two cells, and between a cell and a daughter, is 1.6 px; nothing overlaps.
  // ---------------------------------------------------------------------------
  const TISSUE = [
    [-117, 894, 402, null],          //  0   d 657
    [1211, 590, 356, 'spindle'],     //  1   d 739
    [1247, 1250, 302, null],         //  2   d 789
    [14, 163, 339, 'pinchMid'],      //  3   d 905
    [647, -48, 301, null],           //  4   d 954
    [826, 1844, 352, 'pinchEarly'],  //  5   d 986
    [-59, 1785, 454, 'pinchLate'],   //  6   d 1069
    [1245, -35, 267, null],          //  7   d 1171
    [1830, 963, 341, null],          //  8   d 1292
    [-750, 1253, 323, null],         //  9   d 1337
    [-750, 463, 361, null],          // 10   d 1362
    [1830, 309, 309, null],          // 11   d 1419
    [83, -539, 358, null],           // 12   d 1510
    [974, -559, 302, null],          // 13   d 1522
    [1830, 1794, 488, null],         // 14   d 1570
    [-762, 1980, 250, null],         // 15   d 1692
    [-750, -449, 477, null],         // 16   d 1867
    [1830, -490, 472, null],         // 17   d 1896
    [505, 2720, 372, null],          // 18   d 1820
    [1265, 2700, 360, null],         // 19   d 1941
    [-235, 2700, 322, null],         // 20   d 1960
    [456, -1190, 389, null],         // 21   d 2092
    [1097, -1190, 248, null],        // 22   d 2163
    [-750, -1190, 262, null],        // 23   d 2456
  ];

  // the division axis of each dividing neighbour, so the field never looks regimented
  const DIV_AXIS = { 1: 0.38, 3: -0.52, 5: 1.22, 6: 2.42 };

  // pressing: how large each tissue cell is actually drawn, and who it presses against.
  // A dividing cell is barely inflated — it has rounded up for mitosis and keeps its own shape,
  // so its neighbours flatten against it rather than the other way round.
  const PRESS_PAD = 40;
  const PRESS_R = TISSUE.map((row) => row[2] + (row[3] ? 8 : PRESS_PAD));
  const HARD_CELLS = [[CX, G4.upperY, G4.r], [CX, G4.lowerY, G4.r]];
  const SOFT_CELLS = TISSUE.map((row, i) => {
    const out = [];
    for (let j = 0; j < TISSUE.length; j++) {
      if (j === i) continue;
      const d = hyp(TISSUE[j][0] - row[0], TISSUE[j][1] - row[1]);
      if (d < PRESS_R[i] + PRESS_R[j]) out.push([TISSUE[j][0], TISSUE[j][1], PRESS_R[j]]);
    }
    return out;
  });

  // pinch shapes as fractions of the packing radius: [ neckHalf, lobeR, lobeOffset ]
  // every one fits inside its packing circle (lobeOffset + lobeR <= 1)
  const PINCH = {
    pinchEarly: [0.55, 0.60, 0.38],
    pinchMid: [0.34, 0.52, 0.46],
    pinchLate: [0.12, 0.46, 0.52],
  };

  // ===========================================================================================
  // 2. PERIODIC RADIAL WOBBLE
  // A cell is an irregular near-circle, never a perfect circle. The wobble is periodic in the
  // angle so a closed outline has no seam, and it is time-independent: the line boil on top of it
  // comes from lib.inkPath.
  // ===========================================================================================

  const wobCache = new Map();
  function wobbler(seed) {
    const key = seed >>> 0;
    let f = wobCache.get(key);
    if (f) return f;
    const r = LIB.rng(seed);
    const H = [];
    let norm = 0;
    for (const n of [2, 3, 5, 7, 11]) {
      const a = r.range(0.25, 1) / Math.sqrt(n);
      H.push([n, a, r() * TAU]);
      norm += a;
    }
    f = (ang) => {
      let s = 0;
      for (let i = 0; i < H.length; i++) s += H[i][1] * Math.sin(H[i][0] * ang + H[i][2]);
      return s / norm;
    };
    wobCache.set(key, f);
    return f;
  }

  // ===========================================================================================
  // 3. SHAPE BUILDERS
  // ===========================================================================================

  /** An irregular near-circle: radius r with a seeded periodic wobble of amp px. */
  function blobPts(cx, cy, r, amp, seed, n) {
    const w = wobbler(seed);
    const N = n || Math.max(32, Math.round(r * 0.22));
    const out = new Array(N);
    for (let i = 0; i < N; i++) {
      const a = (i / N) * TAU;
      const rr = r + amp * w(a);
      out[i] = [cx + Math.cos(a) * rr, cy + Math.sin(a) * rr];
    }
    return out;
  }

  /**
   * A tissue cell pressed against its neighbours.
   * Every neighbour is drawn PRESS px larger than its packing radius, then cut back where it meets
   * another cell, so the membranes flatten against each other and only a thin line of paper stays
   * between them: body cells sit among many others, they do not float in gaps.
   *
   *   soft : [x, y, pressRadius] of another pressed cell. Both cells are cut on the same radical
   *          plane — the plane where the two inflated radii balance — so the two flats agree and
   *          the pair keeps an even HALF_GAP either side of it.
   *   hard : [x, y, radius] of a cell that is NOT inflated (a daughter). The point is pulled back
   *          along its own ray until it clears that circle, so the tissue curves round the pair.
   */
  const HALF_GAP = 7;      // paper left between two pressed membranes, each side of the plane
  const HARD_GAP = 13;     // paper left between a tissue cell and a daughter

  function pressedBlobPts(cx, cy, r, amp, seed, n, soft, hard) {
    const w = wobbler(seed);
    const N = n || Math.max(32, Math.round(r * 0.16));
    const out = new Array(N);
    for (let i = 0; i < N; i++) {
      const a = (i / N) * TAU;
      const ux = Math.cos(a), uy = Math.sin(a);
      let rr = r + amp * w(a);
      const floor = r * 0.5;
      for (let k = 0; k < soft.length; k++) {
        const vx = soft[k][0] - cx, vy = soft[k][1] - cy;
        const dist = hyp(vx, vy);
        if (dist < 1 || dist > r + soft[k][2]) continue;      // not touching: nothing to cut
        const cosang = (ux * vx + uy * vy) / dist;
        if (cosang <= 0.12) continue;                          // the far side of the cell
        const plane = (dist * dist + r * r - soft[k][2] * soft[k][2]) / (2 * dist) - HALF_GAP;
        const lim = plane / cosang;
        if (lim > floor && lim < rr) rr = lim;
      }
      for (let k = 0; k < hard.length; k++) {
        const vx = hard[k][0] - cx, vy = hard[k][1] - cy;
        const R = hard[k][2] + HARD_GAP;
        const vv = vx * vx + vy * vy;
        if (vv > (rr + R) * (rr + R)) continue;
        const uv = ux * vx + uy * vy;
        const disc = uv * uv - (vv - R * R);
        if (disc <= 0) continue;                               // the ray misses that circle
        const lim = uv - Math.sqrt(disc);
        if (lim > floor && lim < rr) rr = lim;
      }
      out[i] = [cx + ux * rr, cy + uy * rr];
    }
    return out;
  }

  /**
   * A pinched cell: two lobes of radius R whose centres sit h either side of the middle along the
   * division axis, bridged by two opposing furrow arcs that leave a neck 2*hw wide. This is the
   * G4 shape and every pinching neighbour, so the furrow always reads the same way.
   * Needs h >= sqrt(R*R - hw*hw); every caller in this file satisfies it.
   */
  function peanutPts(cx, cy, axis, h, R, hw, amp, seed) {
    const Rf = (h * h + hw * hw - R * R) / (2 * (R - hw));
    const xf = hw + Rf;
    const tA = Math.atan2(h, xf);
    const w = wobbler(seed);
    const ca = Math.cos(axis - Math.PI / 2), sa = Math.sin(axis - Math.PI / 2);
    const out = [];
    const put = (lx, ly) => out.push([cx + lx * ca - ly * sa, cy + lx * sa + ly * ca]);

    const lobeArc = (ly, a0, a1) => {
      const span = a1 - a0;
      const n = Math.max(10, Math.round((Math.abs(span) * R) / 9));
      for (let i = 0; i <= n; i++) {
        const a = a0 + (span * i) / n;
        const rr = R + amp * w(a);
        put(Math.cos(a) * rr, ly + Math.sin(a) * rr);
      }
    };
    const furrowArc = (lx, a0, a1) => {
      const span = a1 - a0;
      const n = Math.max(6, Math.round((Math.abs(span) * Rf) / 7));
      for (let i = 0; i <= n; i++) {
        const a = a0 + (span * i) / n;
        put(lx + Math.cos(a) * Rf, Math.sin(a) * Rf);
      }
    };

    // upper lobe, right furrow, lower lobe, left furrow — one closed loop
    lobeArc(-h, Math.PI - tA, TAU + tA);
    furrowArc(xf, tA - Math.PI, -tA - Math.PI);
    lobeArc(h, -tA, Math.PI + tA);
    furrowArc(-xf, tA, -tA);
    return out;
  }

  /**
   * A daughter cell just after it sealed: the near-circle of radius R with a shallow flat where it
   * parted from its sister, healing over two drawings. `face` is +1 when the sister was below.
   */
  function sealedPts(cx, cy, R, face, flat, amp, seed) {
    const w = wobbler(seed);
    const N = Math.max(40, Math.round(R * 0.24));
    const out = new Array(N);
    const faceAng = face > 0 ? Math.PI / 2 : -Math.PI / 2;
    for (let i = 0; i < N; i++) {
      const a = (i / N) * TAU;
      let d = a - faceAng;
      while (d > Math.PI) d -= TAU;
      while (d < -Math.PI) d += TAU;
      const notch = 1 - 0.055 * flat * Math.exp(-(d * d) / 0.18);
      const rr = (R + amp * w(a)) * notch;
      out[i] = [cx + Math.cos(a) * rr, cy + Math.sin(a) * rr];
    }
    return out;
  }

  /** A loose worm chromosome's centreline: a gently waving rod. */
  function wormSpine(cx, cy, len, ang, bend, seed) {
    const r = LIB.rng(seed);
    const k = r.range(1.0, 1.8);
    const ph = r() * TAU;
    const ca = Math.cos(ang), sa = Math.sin(ang);
    const N = 10;
    const pts = new Array(N + 1);
    for (let i = 0; i <= N; i++) {
      const u = i / N - 0.5;
      const s = u * len;
      const v = bend * Math.sin(u * TAU * k + ph);
      pts[i] = [cx + ca * s - sa * v, cy + sa * s + ca * v];
    }
    return LIB.smoothPts(pts, false, 4);
  }

  /** Wrap a centreline in a constant-width ribbon with rounded ends. */
  function ribbonOutline(pts, halfW) {
    const n = pts.length;
    const up = new Array(n), dn = new Array(n);
    for (let i = 0; i < n; i++) {
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const l = hyp(tx, ty) || 1;
      tx /= l;
      ty /= l;
      const u = i / (n - 1);
      const taper = Math.sqrt(Math.max(1e-4, 1 - Math.pow(Math.abs(u - 0.5) * 2, 6)));
      const wv = halfW * taper;
      up[i] = [pts[i][0] - ty * wv, pts[i][1] + tx * wv];
      dn[i] = [pts[i][0] + ty * wv, pts[i][1] - tx * wv];
    }
    return up.concat(dn.reverse());
  }

  /** A mitochondrion: a bean, slightly bowed, with folded inner ridges. */
  function beanOutline(cx, cy, len, w, ang, seed) {
    const r = LIB.rng(seed);
    const bow = w * r.range(0.22, 0.42) * r.sign();
    const ca = Math.cos(ang), sa = Math.sin(ang);
    const N = 14;
    const spine = [];
    for (let i = 0; i <= N; i++) {
      const u = i / N - 0.5;
      const s = u * (len - w);
      const v = bow * Math.cos(u * Math.PI);
      spine.push([cx + ca * s - sa * v, cy + sa * s + ca * v]);
    }
    const sm = LIB.smoothPts(spine, false, 4);
    return { outline: ribbonOutline(sm, w / 2), spine: sm };
  }

  /** An X chromosome: two equal rods crossing at the centromere. Used by the spindle neighbour. */
  function xChromoRods(cx, cy, h, armW, ang) {
    const rods = [];
    for (const tilt of [-0.52, 0.52]) {
      const a = ang + tilt;
      const ca = Math.cos(a), sa = Math.sin(a);
      rods.push(ribbonOutline([
        [cx - ca * h * 0.5, cy - sa * h * 0.5],
        [cx, cy],
        [cx + ca * h * 0.5, cy + sa * h * 0.5],
      ], armW / 2));
    }
    return rods;
  }

  /**
   * The lit-side crescent of a blob: the band just inside the membrane on the shadow side.
   * Hatching this instead of hatching the whole cell with a density function is both the right
   * drawing (only shadow sides get hatched) and far cheaper per frame.
   */
  function crescent(poly, cx, cy, depth, lightX, lightY) {
    const n = poly.length;
    const lit = new Array(n);
    for (let i = 0; i < n; i++) {
      const dx = poly[i][0] - cx, dy = poly[i][1] - cy;
      const l = hyp(dx, dy) || 1;
      lit[i] = (dx / l) * lightX + (dy / l) * lightY;
    }
    // the contiguous run facing the shadow
    let start = -1;
    for (let i = 0; i < n; i++) {
      if (lit[i] > -0.12 && lit[(i - 1 + n) % n] <= -0.12) {
        start = i;
        break;
      }
    }
    if (start < 0) return null;
    const run = [];
    for (let k = 0; k < n; k++) {
      const i = (start + k) % n;
      if (lit[i] <= -0.12) break;
      run.push(i);
    }
    if (run.length < 6) return null;
    const outer = [], inner = [];
    for (let k = 0; k < run.length; k++) {
      const p = poly[run[k]];
      const u = k / (run.length - 1);
      const d = depth * Math.sin(Math.PI * u);
      const dx = p[0] - cx, dy = p[1] - cy;
      const l = hyp(dx, dy) || 1;
      outer.push(p);
      inner.push([p[0] - (dx / l) * d, p[1] - (dy / l) * d]);
    }
    return outer.concat(inner.reverse());
  }

  // ===========================================================================================
  // 4. SCALE-AWARE DRAWING
  // V.ws keeps pens near their nominal screen width as the camera pulls back: at zoom 1 it is 1,
  // at zoom 0.45 it is 1.82, so a 6 px membrane lands at about 4.9 px on screen instead of 2.7.
  // ===========================================================================================

  function makeView(zoom, camX, camY) {
    const hw = 540 / zoom, hh = 960 / zoom;
    return {
      zoom,
      ws: q6(Math.pow(zoom, -0.75)),
      x0: camX - hw - 40,
      x1: camX + hw + 40,
      y0: camY - hh - 40,
      y1: camY + hh + 40,
    };
  }
  const onScreen = (V, x, y, r) => !(x + r < V.x0 || x - r > V.x1 || y + r < V.y0 || y - r > V.y1);

  function inkV(ctx, V, pts, o) {
    const ws = V.ws;
    const width = (o.width != null ? o.width : 3) * ws;
    const tp = o.taper != null ? o.taper : o.closed ? [10, 22] : [18, 34];
    const q = {
      closed: !!o.closed,
      width,
      color: o.color || PAL.ink,
      alpha: o.alpha != null ? o.alpha : 1,
      seed: o.seed,
      fill: o.fill || null,
      fillAlpha: o.fillAlpha,
      wobble: (o.wobble != null ? o.wobble : 2) * ws,
      tremble: (o.tremble != null ? o.tremble : 0.4) * ws,
      boilAmp: (o.boilAmp != null ? o.boilAmp : 0.7) * ws,
      rough: (o.rough != null ? o.rough : 0.22 + 0.07 * (o.width != null ? o.width : 3)) * ws,
      step: (o.step || 2.5) * Math.max(1, ws * 0.85),
      taper: Array.isArray(tp) ? [tp[0] * ws, tp[1] * ws] : tp * ws,
      smooth: o.smooth,
      widthJitter: o.widthJitter,
      minWidth: o.minWidth,
      swell: o.swell,
      pressure: o.pressure,
    };
    if (o.double) {
      const d = o.double === true ? {} : Object.assign({}, o.double);
      if (d.offset == null) d.offset = (width / 2 + 3 * ws) * (sd('dbl', o.seed) & 1 ? 1 : -1);
      else d.offset *= ws;
      q.double = d;
    }
    LIB.inkPath(ctx, pts, q);
  }

  function hatchV(ctx, V, clip, o) {
    const ws = V.ws;
    LIB.hatch(ctx, clip, Object.assign({}, o, {
      spacing: (o.spacing || 8) * ws,
      width: (o.width != null ? o.width : 1.4) * ws,
      length: (o.length || [16, 64]).map((v) => v * ws),
      gap: (o.gap || [2, 7]).map((v) => v * ws),
      bow: (o.bow != null ? o.bow : 0.7) * ws,
      bend: (o.bend || 0) * ws,
      inset: (o.inset != null ? o.inset : 6) * ws,
      overshoot: (o.overshoot != null ? o.overshoot : 3) * ws,
      boilAmp: (o.boilAmp != null ? o.boilAmp : 0.45) * ws,
    }));
  }

  function crossHatchV(ctx, V, clip, o) {
    const ws = V.ws;
    LIB.crossHatch(ctx, clip, Object.assign({}, o, {
      spacing: (o.spacing || 8) * ws,
      crossSpacing: (o.crossSpacing || (o.spacing || 8) * 1.4) * ws,
      width: (o.width != null ? o.width : 1.4) * ws,
      length: (o.length || [16, 64]).map((v) => v * ws),
      inset: (o.inset != null ? o.inset : 6) * ws,
      overshoot: (o.overshoot != null ? o.overshoot : 3) * ws,
      boilAmp: (o.boilAmp != null ? o.boilAmp : 0.45) * ws,
    }));
  }

  function stippleV(ctx, V, bounds, o) {
    const ws = V.ws;
    const rr = o.r || [1.0, 2.2];
    LIB.stipple(ctx, null, Object.assign({}, o, {
      bounds,
      spacing: (o.spacing || 7.5) * ws,
      r: [rr[0] * ws, rr[1] * ws],
      boilAmp: (o.boilAmp != null ? o.boilAmp : 0.35) * ws,
    }));
  }

  function plainStroke(ctx, V, path, color, width, alpha, dash) {
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = width * V.ws;
    ctx.globalAlpha *= alpha == null ? 1 : alpha;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    if (dash) ctx.setLineDash(dash.map((d) => d * V.ws));
    ctx.stroke(path);
    ctx.restore();
  }

  // ===========================================================================================
  // 5. CELL PARTS
  // ===========================================================================================

  /** Cytoplasm: flat fill, a hatched crescent inside the shadow rim, ribosome stipple. */
  function paintCytoplasm(ctx, V, poly, cx, cy, r, o) {
    fillPoly(ctx, poly, o.fill);
    const cres = crescent(poly, cx, cy, r * (o.depth || 0.30), 0.707, 0.707);
    if (cres) {
      hatchV(ctx, V, cres, {
        angle: -Math.PI / 4,
        spacing: o.spacing || 9,
        width: 1.4,
        color: o.hatch,
        alpha: o.hatchAlpha != null ? o.hatchAlpha : 0.75,
        length: [14, 46],
        seed: o.seed + 11,
        inset: 4,
        overshoot: 4,
      });
    }
    if (o.stipple > 0) {
      const R = r * 0.93;
      const opts = {
        spacing: o.stippleSpacing || 9,
        r: [1.0, 2.0],
        color: PAL.ribosome,
        alpha: o.stippleAlpha != null ? o.stippleAlpha : 0.7,
        seed: o.seed + 23,
      };
      if (o.clipToPoly) {
        // a pressed cell has flat faces, so the dots have to respect the real outline.
        // Every other point is enough for a point-in-polygon test and halves its cost.
        const ws = V.ws;
        const lite = [];
        for (let k = 0; k < poly.length; k += 2) lite.push(poly[k]);
        LIB.stipple(ctx, lite, Object.assign({}, opts, {
          spacing: opts.spacing * ws,
          r: [opts.r[0] * ws, opts.r[1] * ws],
          boilAmp: 0.35 * ws,
          density: o.stipple,
          pad: -6,
        }));
      } else {
        stippleV(ctx, V, { x: cx - R, y: cy - R, w: R * 2, h: R * 2 }, Object.assign({}, opts, {
          density: (x, y) => (hyp(x - cx, y - cy) < R ? o.stipple : 0),
        }));
      }
    }
  }

  /** The nucleus: mauve near-circle, inkSoft rim, cross-hatched shadow, a nucleolus disc. */
  function paintNucleus(ctx, V, cx, cy, r, o) {
    const poly = blobPts(cx, cy, r, r * 0.035, o.seed, Math.max(26, Math.round(r * 0.3)));
    fillPoly(ctx, poly, o.fill || PAL.nucleus);
    const cres = crescent(poly, cx, cy, r * 0.5, 0.707, 0.707);
    if (cres) {
      crossHatchV(ctx, V, cres, {
        angle: -Math.PI / 4,
        spacing: o.spacing || 7,
        width: 1.2,
        color: PAL.nucleusDeep,
        alpha: o.hatchAlpha != null ? o.hatchAlpha : 0.55,
        layers: 2,
        length: [10, 30],
        seed: o.seed + 31,
        inset: 3,
        overshoot: 3,
      });
    }
    if (o.nucleolus !== false) {
      const nx = cx + r * NUCLEOLUS.gx, ny = cy + r * NUCLEOLUS.gy;
      const nr = r * NUCLEOLUS.gr;
      const np = blobPts(nx, ny, nr, nr * 0.1, o.seed + 41, 20);
      fillPoly(ctx, np, PAL.nucleusDeep, 0.85);
      if (o.ink) inkV(ctx, V, np, { closed: true, width: 1.6, color: PAL.nucleusRim, alpha: 0.5, seed: o.seed + 43 });
    }
    if (o.ink) {
      inkV(ctx, V, poly, { closed: true, width: o.rimWidth || 4, color: PAL.nucleusRim, alpha: o.rimAlpha != null ? o.rimAlpha : 0.95, seed: o.seed + 47, wobble: 1.6 });
    } else {
      const p = new Path2D();
      trace(p, poly, true);
      plainStroke(ctx, V, p, PAL.nucleusRim, o.rimWidth || 3, o.rimAlpha != null ? o.rimAlpha : 0.8);
    }
    return poly;
  }

  /**
   * The four chromosomes inside a nucleus, in the G1 arrangement: two long chromoA and two short
   * chromoB, single copies, drawn as loose worms so the count can be followed in every shot.
   */
  function paintChromosomes(ctx, V, cx, cy, nucR, o) {
    const ink = !!o.ink;
    const bright = !!o.bright;
    const seed = o.seed;
    const rot = o.rot || 0;
    const cr = Math.cos(rot), sr = Math.sin(rot);
    for (let i = 0; i < CHROMO.length; i++) {
      const c = CHROMO[i];
      const ox = nucR * c.gx, oy = nucR * c.gy;
      const px = cx + ox * cr - oy * sr;
      const py = cy + ox * sr + oy * cr;
      const len = nucR * c.gl;
      const halfW = nucR * 0.053;
      const spine = wormSpine(px, py, len, c.ang + rot, nucR * 0.055, seed + i * 17);
      const poly = ribbonOutline(spine, halfW);
      const base = c.pair === 'A' ? (bright ? PAL.chromoALight : PAL.chromoA) : (bright ? PAL.chromoBLight : PAL.chromoB);
      const deep = c.pair === 'A' ? PAL.chromoADeep : PAL.chromoBDeep;
      fillPoly(ctx, poly, base, o.alpha != null ? o.alpha : 1);
      if (o.hatch) {
        hatchV(ctx, V, poly, {
          angle: 30 * DEG,
          spacing: 5,
          width: 1.1,
          color: deep,
          alpha: 0.7 * (o.alpha != null ? o.alpha : 1),
          length: [6, 18],
          seed: seed + 100 + i,
          inset: 1.5,
          overshoot: 1.5,
          density: 0.75,
        });
        // a faint centre line down the worm, the reference's engraved look
        const cp = new Path2D();
        trace(cp, spine, false);
        plainStroke(ctx, V, cp, deep, 0.9, 0.35 * (o.alpha != null ? o.alpha : 1));
      }
      if (ink) {
        inkV(ctx, V, poly, { closed: true, width: 2.2, color: PAL.ink, alpha: 0.9 * (o.alpha != null ? o.alpha : 1), seed: seed + 200 + i, wobble: 1, taper: [4, 8] });
      } else {
        const p = new Path2D();
        trace(p, poly, true);
        plainStroke(ctx, V, p, PAL.ink, 1.6, 0.75 * (o.alpha != null ? o.alpha : 1));
      }
    }
  }

  /** Mitochondria: sage beans with folded inner ridges. */
  function paintMito(ctx, V, cx, cy, len, w, ang, seed, o) {
    const b = beanOutline(cx, cy, len, w, ang, seed);
    fillPoly(ctx, b.outline, PAL.mito, o && o.alpha != null ? o.alpha : 1);
    const ridges = new Path2D();
    const n = b.spine.length;
    for (let k = 1; k <= 4; k++) {
      const i = Math.round(((k / 5) * (n - 1)));
      const a = b.spine[Math.max(0, i - 1)], c = b.spine[Math.min(n - 1, i + 1)];
      let tx = c[0] - a[0], ty = c[1] - a[1];
      const l = hyp(tx, ty) || 1;
      tx /= l;
      ty /= l;
      const p = b.spine[i];
      const hwv = w * 0.36;
      ridges.moveTo(p[0] + ty * hwv, p[1] - tx * hwv);
      ridges.quadraticCurveTo(p[0] + tx * w * 0.2, p[1] + ty * w * 0.2, p[0] - ty * hwv, p[1] + tx * hwv);
    }
    plainStroke(ctx, V, ridges, PAL.mitoDeep, 1.8, 0.95);
    if (o && o.ink) {
      inkV(ctx, V, b.outline, { closed: true, width: 2.8, color: PAL.ink, alpha: 1, seed: seed + 7, wobble: 1 });
    } else {
      const p = new Path2D();
      trace(p, b.outline, true);
      plainStroke(ctx, V, p, PAL.ink, 2, 0.8);
    }
  }

  /** A centrosome at a spindle pole: a small disc with radial ticks. */
  function paintPole(ctx, V, x, y, r, seed) {
    const poly = blobPts(x, y, r, r * 0.12, seed, 18);
    fillPoly(ctx, poly, PAL.pole, 0.95);
    const p = new Path2D();
    trace(p, poly, true);
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * TAU + 0.2;
      p.moveTo(x + Math.cos(a) * r * 1.05, y + Math.sin(a) * r * 1.05);
      p.lineTo(x + Math.cos(a) * r * 1.85, y + Math.sin(a) * r * 1.85);
    }
    plainStroke(ctx, V, p, PAL.inkSoft, 1.6, 0.85);
  }

  // ===========================================================================================
  // 6. THE TWO DAUGHTERS
  // Both are the same size and hold the same four chromosomes, drawn from the same table with the
  // same seed, so a viewer comparing the two nuclei sees the same four shapes in the same places.
  // The cell outlines mirror about y 900 (they parted there) and the mitochondria differ, because
  // organelles are shared out while the chromosomes are copied exactly.
  // ===========================================================================================

  /** The shadow the nucleus casts down and right across the cytoplasm. */
  function paintNucleusShadow(ctx, V, cx, cy, nucR, seed) {
    const off = nucR * 0.26;
    const shade = LIB.ellipsePts(cx + off, cy + off * 1.05, nucR * 1.04, nucR * 0.98, 30, -0.4);
    hatchV(ctx, V, shade, {
      angle: -Math.PI / 4 + 1.05,
      spacing: 7,
      width: 1.2,
      color: PAL.ink,
      alpha: 0.19,
      length: [10, 28],
      seed: seed + 17,
      inset: 6,
      overshoot: 1,
      density: 0.72,
    });
  }

  /**
   * Everything inside a daughter's membrane. Both daughters take the same seeds, so the two nuclei
   * hold the same four chromosomes drawn exactly the same way: that is what the 'identical' arc is
   * pointing at. Only the mitochondria differ, because organelles are shared out, not copied.
   */
  function daughterContents(ctx, V, cy, o) {
    const nucR = G4.nucR;
    paintNucleusShadow(ctx, V, CX, cy, nucR, sd('nucshadow'));
    paintNucleus(ctx, V, CX, cy, nucR, { seed: sd('nuc'), ink: true, rimWidth: 4, spacing: 7 });
    paintChromosomes(ctx, V, CX, cy, nucR, { seed: sd('chromo'), ink: true, hatch: true, bright: o.bright });
  }

  function drawDaughterBody(ctx, V, poly, cy, o) {
    paintCytoplasm(ctx, V, poly, CX, cy, G4.r, {
      fill: PAL.cytoplasm,
      hatch: PAL.cytoHatch,
      hatchAlpha: 0.8,
      spacing: 8,
      depth: 0.30,
      stipple: o.stipple,
      stippleSpacing: 8.5,
      stippleAlpha: 0.65,
      seed: o.seed,
    });
    const mito = cy === G4.upperY ? MITO_UPPER : MITO_LOWER;
    for (let i = 0; i < mito.length; i++) {
      paintMito(ctx, V, CX + mito[i][0], cy + mito[i][1], MITO_LEN, MITO_W, mito[i][2], sd('mito', cy) + i * 13, { ink: true });
    }
    daughterContents(ctx, V, cy, o);
  }

  /** The hero membrane: 6 px ink with an occasional doubled retrace, the same seed for both cells. */
  function paintHeroMembrane(ctx, V, poly) {
    inkV(ctx, V, poly, {
      closed: true,
      width: 5.6,
      color: PAL.membrane,
      seed: sd('membrane'),
      wobble: 2.6,
      double: { width: 0.26, alpha: 0.36, offset: 4 },
    });
  }

  // ===========================================================================================
  // 7. NEIGHBOUR CELLS
  // Drawn in the same style at 70 to 80 percent: the neighbour cytoplasm and nucleus tints, ink at
  // 80 percent, and plain strokes rather than inked ones inside the cell, where the hand-drawn
  // edge is under a pixel wide once the camera has pulled back.
  // ===========================================================================================

  function neighbourSeed(i) {
    return sd('tissue', i);
  }

  function drawInterphaseNeighbour(ctx, V, i, x, y, r, seed, detail) {
    const poly = pressedBlobPts(x, y, r, r * 0.045, seed, Math.max(34, Math.round(r * 0.15)), SOFT_CELLS[i], HARD_CELLS);
    paintCytoplasm(ctx, V, poly, x, y, r, {
      fill: PAL.neighbour,
      hatch: PAL.cytoHatch,
      hatchAlpha: 0.55,
      spacing: 11,
      depth: 0.24,
      stipple: detail >= 2 ? 0.30 : 0,
      stippleSpacing: 11,
      stippleAlpha: 0.5,
      clipToPoly: true,
      seed: seed + 3,
    });
    if (detail >= 1) {
      const rr = LIB.rng(seed + 5);
      const off = r * 0.1;
      const oa = rr() * TAU;
      const nx = x + Math.cos(oa) * off, ny = y + Math.sin(oa) * off;
      const nucR = r * rr.range(0.38, 0.44);
      paintNucleus(ctx, V, nx, ny, nucR, {
        seed: seed + 61,
        fill: PAL.neighbourNucleus,
        ink: false,
        rimWidth: 3,
        rimAlpha: 0.7,
        hatchAlpha: 0.42,
        spacing: 8,
      });
      paintChromosomes(ctx, V, nx, ny, nucR, { seed: seed + 71, ink: false, hatch: false, alpha: 0.72, rot: rr.range(-0.7, 0.7) });
      const nm = 2 + (rr() < 0.5 ? 1 : 0);
      for (let i = 0; i < nm; i++) {
        const a = rr() * TAU;
        const d = r * rr.range(0.50, 0.72);
        paintMito(ctx, V, x + Math.cos(a) * d, y + Math.sin(a) * d, r * 0.17, r * 0.078, rr() * TAU, seed + 91 + i * 7, null);
      }
    }
    inkV(ctx, V, poly, { closed: true, width: 3.6, color: PAL.ink, alpha: 0.78, seed: seed + 101, wobble: 2.4 });
  }

  function drawPinchNeighbour(ctx, V, x, y, r, seed, stage, axis, detail) {
    const [hwF, lobeF, offF] = PINCH[stage];
    const a = axis;
    const ca = Math.cos(a), sa = Math.sin(a);
    const poly = peanutPts(x, y, a, r * offF, r * lobeF, r * hwF, r * 0.04, seed);
    paintCytoplasm(ctx, V, poly, x, y, r * 0.92, {
      fill: PAL.neighbour,
      hatch: PAL.cytoHatch,
      hatchAlpha: 0.55,
      spacing: 11,
      depth: 0.3,
      stipple: detail >= 2 ? 0.28 : 0,
      stippleSpacing: 11,
      stippleAlpha: 0.5,
      clipToPoly: true,
      seed: seed + 3,
    });
    if (detail >= 1) {
      const nucR = r * lobeF * 0.45;
      const rr = LIB.rng(seed + 5);
      for (const s of [-1, 1]) {
        const nx = x + ca * s * r * offF, ny = y + sa * s * r * offF;
        paintNucleus(ctx, V, nx, ny, nucR, {
          seed: seed + 61,
          fill: PAL.neighbourNucleus,
          ink: false,
          rimWidth: 3,
          rimAlpha: 0.7,
          hatchAlpha: 0.42,
          spacing: 8,
        });
        paintChromosomes(ctx, V, nx, ny, nucR, { seed: seed + 71, ink: false, hatch: false, alpha: 0.72, rot: a });
      }
      for (let i = 0; i < 2; i++) {
        const ang = rr() * TAU;
        const d = r * rr.range(0.3, 0.5);
        paintMito(ctx, V, x + Math.cos(ang) * d, y + Math.sin(ang) * d, r * 0.16, r * 0.072, rr() * TAU, seed + 91 + i * 7, null);
      }
    }
    inkV(ctx, V, poly, { closed: true, width: 3.6, color: PAL.ink, alpha: 0.78, seed: seed + 101, wobble: 2.4 });
    // the contractile furrow reads as two short inkSoft creases either side of the neck
    const creases = new Path2D();
    for (const s of [-1, 1]) {
      const hx = x - sa * s * r * hwF, hy = y + ca * s * r * hwF;
      creases.moveTo(hx - ca * r * 0.1, hy - sa * r * 0.1);
      creases.quadraticCurveTo(hx - sa * s * r * 0.05, hy + ca * s * r * 0.05, hx + ca * r * 0.1, hy + sa * r * 0.1);
    }
    plainStroke(ctx, V, creases, PAL.inkSoft, 2, 0.55);
  }

  function drawSpindleNeighbour(ctx, V, x, y, r, seed, axis, detail) {
    const a = axis;
    const ca = Math.cos(a), sa = Math.sin(a);
    // an elongated cell: the mitotic cell stretches along the spindle axis
    const w = wobbler(seed);
    const N = Math.max(36, Math.round(r * 0.16));
    const poly = new Array(N);
    for (let i = 0; i < N; i++) {
      const ang = (i / N) * TAU;
      const k = 1 + 0.035 * w(ang);
      const lx = Math.cos(ang) * r * 0.78 * k, ly = Math.sin(ang) * r * 0.99 * k;
      poly[i] = [x + lx * Math.cos(a - Math.PI / 2) - ly * Math.sin(a - Math.PI / 2), y + lx * Math.sin(a - Math.PI / 2) + ly * Math.cos(a - Math.PI / 2)];
    }
    paintCytoplasm(ctx, V, poly, x, y, r * 0.88, {
      fill: PAL.neighbour,
      hatch: PAL.cytoHatch,
      hatchAlpha: 0.55,
      spacing: 11,
      depth: 0.26,
      stipple: detail >= 2 ? 0.26 : 0,
      stippleSpacing: 11,
      stippleAlpha: 0.5,
      clipToPoly: true,
      seed: seed + 3,
    });

    const poleD = r * 0.84;
    const P1 = [x - ca * poleD, y - sa * poleD];
    const P2 = [x + ca * poleD, y + sa * poleD];
    // the metaphase plate: four X chromosomes across the middle, mirroring G3's spacing
    const plate = [-0.37, -0.12, 0.12, 0.37].map((u) => [x - sa * u * r, y + ca * u * r]);
    const kinds = ['A', 'B', 'B', 'A'];

    if (detail >= 1) {
      const fib = new Path2D();
      for (const P of [P1, P2]) {
        for (const q of plate) {
          const mx = (P[0] + q[0]) / 2 - sa * (q[0] - x) * 0.08;
          const my = (P[1] + q[1]) / 2 + ca * (q[1] - y) * 0.08;
          fib.moveTo(P[0], P[1]);
          fib.quadraticCurveTo(mx, my, q[0], q[1]);
        }
        // free fibres fanning past the plate
        for (let i = -3; i <= 3; i++) {
          if (!i) continue;
          const u = i * 0.13;
          fib.moveTo(P[0], P[1]);
          fib.lineTo(x - sa * u * r * 2.4 + (P[0] - x) * -0.22, y + ca * u * r * 2.4 + (P[1] - y) * -0.22);
        }
      }
      plainStroke(ctx, V, fib, PAL.fibre, 1.8, 0.7);
    }

    // four X chromosomes on the plate: two chromoA (long) outside, two chromoB (short) inside,
    // each an X of two identical copies joined at a centromere disc
    for (let i = 0; i < plate.length; i++) {
      const long = kinds[i] === 'A';
      const rods = xChromoRods(plate[i][0], plate[i][1], r * (long ? 0.27 : 0.20), r * 0.062, a + Math.PI / 2);
      const col = long ? PAL.chromoA : PAL.chromoB;
      const deep = long ? PAL.chromoADeep : PAL.chromoBDeep;
      for (const rod of rods) {
        fillPoly(ctx, rod, col, 0.96);
        const p = new Path2D();
        trace(p, rod, true);
        plainStroke(ctx, V, p, deep, 1.8, 0.85);
      }
      ctx.save();
      ctx.fillStyle = PAL.centromere;
      ctx.beginPath();
      ctx.arc(plate[i][0], plate[i][1], r * 0.034, 0, TAU);
      ctx.fill();
      ctx.restore();
    }

    paintPole(ctx, V, P1[0], P1[1], r * 0.062, seed + 201);
    paintPole(ctx, V, P2[0], P2[1], r * 0.062, seed + 203);
    inkV(ctx, V, poly, { closed: true, width: 3.6, color: PAL.ink, alpha: 0.78, seed: seed + 101, wobble: 2.4 });
  }

  /**
   * One tissue cell. The pop is a transform about the cell's own centre, so the pressed outline
   * and everything inside it stay exactly as they will be once the cell has settled.
   */
  function drawNeighbour(ctx, V, i, scale, alpha) {
    const row = TISSUE[i];
    const x = row[0], y = row[1];
    const r = PRESS_R[i];
    const stage = row[3];
    if (!onScreen(V, x, y, r * Math.max(1, scale))) return;
    const px = r * V.zoom * scale;
    const detail = px >= 118 ? 2 : px >= 52 ? 1 : 0;
    const seed = neighbourSeed(i);
    const axis = DIV_AXIS[i] != null ? DIV_AXIS[i] : 0;
    ctx.save();
    ctx.globalAlpha *= alpha;
    if (scale !== 1) {
      ctx.translate(x, y);
      ctx.scale(scale, scale);
      ctx.translate(-x, -y);
    }
    if (stage === 'spindle') drawSpindleNeighbour(ctx, V, x, y, r, seed, axis, detail);
    else if (stage) drawPinchNeighbour(ctx, V, x, y, r, seed, stage, axis, detail);
    else drawInterphaseNeighbour(ctx, V, i, x, y, r, seed, detail);
    ctx.restore();
  }

  // ===========================================================================================
  // 8. THE PLATE'S CONSTRUCTION GEOMETRY
  // The scaffold the drawing was set out on, in inkFaint, under the camera and behind the cells,
  // so only the parts outside a membrane show: the axis through the pair, the furrow line, the
  // corner diagonals, a square and a degree-ruled circle around the pair, rays through the G4 key
  // points, and a registration cross on each of them. It carries the empty paper above and below
  // the pair while the camera is still locked, and it thins out once the tissue arrives.
  // ===========================================================================================

  const CONS_R = 720;                 // the degree-ruled circle around the pair
  const CONS_SQUARE = [140, 180, 800, 1440];   // x, y, w, h of the faint square around the pair

  function drawConstruction(ctx, V, alpha) {
    if (alpha <= 0.01) return;
    ctx.save();
    ctx.globalAlpha *= alpha;
    const cons = { width: 1.5, color: PAL.inkFaint, alpha: 0.32, taper: [0, 0], wobble: 1.6, smooth: false, step: 10 };

    // the pair's axis and the line the furrow closed on
    inkV(ctx, V, [[CX, -300], [CX, 2100]], Object.assign({ seed: sd('axis') }, cons));
    inkV(ctx, V, [[-180, G4.midY], [1260, G4.midY]], Object.assign({ seed: sd('mid') }, cons));
    // the two diameters at 45 degrees, running past the cells
    for (const s of [-1, 1]) {
      inkV(ctx, V, [[CX - s * 820, G4.midY - 820], [CX + s * 820, G4.midY + 820]], Object.assign({ seed: sd('diag', s) }, cons));
    }
    // the horizontals the pair's extremes sit on
    for (const hy of [G4.upperY - G4.r, G4.lowerY + G4.r]) {
      inkV(ctx, V, [[CONS_SQUARE[0] - 60, hy], [CONS_SQUARE[0] + CONS_SQUARE[2] + 60, hy]], Object.assign({ seed: sd('hline', hy) }, cons, { alpha: 0.22 }));
    }
    // a faint square around the pair
    const sq = LIB.rectPts(CONS_SQUARE[0], CONS_SQUARE[1], CONS_SQUARE[2], CONS_SQUARE[3], 40);
    inkV(ctx, V, sq, { closed: true, width: 1.5, color: PAL.inkFaint, alpha: 0.24, seed: sd('square'), taper: [0, 0], wobble: 2.2 });

    // construction circles: one just outside each daughter, and the ruled circle around the pair
    LIB.guideCircle(ctx, CX, G4.upperY, G4.r + 44, { color: PAL.inkFaint, alpha: 0.24, width: 1.5 * V.ws });
    LIB.guideCircle(ctx, CX, G4.lowerY, G4.r + 44, { color: PAL.inkFaint, alpha: 0.24, width: 1.5 * V.ws });
    LIB.guideCircle(ctx, CX, G4.upperY, G4.nucR + 30, { color: PAL.inkFaint, alpha: 0.20, width: 1.5 * V.ws, dash: [3, 8] });
    LIB.guideCircle(ctx, CX, G4.lowerY, G4.nucR + 30, { color: PAL.inkFaint, alpha: 0.20, width: 1.5 * V.ws, dash: [3, 8] });
    LIB.guideCircle(ctx, CX, G4.midY, CONS_R, { color: PAL.inkFaint, alpha: 0.26, width: 1.5 * V.ws });

    // a degree scale on that circle: a 10 px tick every 5 degrees, a 22 px tick every 15
    {
      const deg = new Path2D();
      for (let a = -180; a < 180; a += 5) {
        const c = Math.cos(a * DEG), s = Math.sin(a * DEG);
        const len = a % 15 === 0 ? 22 : 10;
        deg.moveTo(CX + c * CONS_R, G4.midY + s * CONS_R);
        deg.lineTo(CX + c * (CONS_R + len), G4.midY + s * (CONS_R + len));
      }
      plainStroke(ctx, V, deg, PAL.inkFaint, 1.5, 0.4);
    }

    // rays from the furrow out through each of the G4 key points to the ruled circle
    {
      const rays = new Path2D();
      for (const [px, py] of [
        [CX - G4.r, G4.upperY], [CX + G4.r, G4.upperY], [CX - G4.r, G4.lowerY], [CX + G4.r, G4.lowerY],
        [CX - G4.nucR, G4.upperY], [CX + G4.nucR, G4.upperY], [CX - G4.nucR, G4.lowerY], [CX + G4.nucR, G4.lowerY],
      ]) {
        const a = Math.atan2(py - G4.midY, px - CX);
        const r0 = hyp(px - CX, py - G4.midY) + 16;
        if (r0 > CONS_R - 20) continue;
        rays.moveTo(CX + Math.cos(a) * r0, G4.midY + Math.sin(a) * r0);
        rays.lineTo(CX + Math.cos(a) * CONS_R, G4.midY + Math.sin(a) * CONS_R);
      }
      plainStroke(ctx, V, rays, PAL.inkFaint, 1.5, 0.26);
    }

    // registration crosses on the G4 key points
    const marks = new Path2D();
    const K = 12 * V.ws;
    for (const [mx, my] of [
      [CX, G4.upperY - G4.r], [CX, G4.upperY + G4.r], [CX, G4.lowerY - G4.r], [CX, G4.lowerY + G4.r],
      [CX - G4.r, G4.upperY], [CX + G4.r, G4.upperY], [CX - G4.r, G4.lowerY], [CX + G4.r, G4.lowerY],
      [CX, G4.upperY], [CX, G4.lowerY],
      [CONS_SQUARE[0], CONS_SQUARE[1]], [CONS_SQUARE[0] + CONS_SQUARE[2], CONS_SQUARE[1]],
      [CONS_SQUARE[0], CONS_SQUARE[1] + CONS_SQUARE[3]], [CONS_SQUARE[0] + CONS_SQUARE[2], CONS_SQUARE[1] + CONS_SQUARE[3]],
    ]) {
      marks.moveTo(mx - K, my);
      marks.lineTo(mx + K, my);
      marks.moveTo(mx, my - K);
      marks.lineTo(mx, my + K);
    }
    plainStroke(ctx, V, marks, PAL.inkFaint, 1.5, 0.5);
    ctx.restore();
  }

  // ===========================================================================================
  // 9. OVERLAYS — screen-fixed, drawn after the camera closes
  // ===========================================================================================

  /** The tally ring at (180, 300): ticks only, one before the division lands, two after. */
  function drawTally(ctx, two, popScale, pulse) {
    const cx = 180, cy = 300, r = 46;
    const body = new Path2D();
    body.moveTo(cx + r, cy);
    body.arc(cx, cy, r, 0, TAU);
    const tick = (a, s) => {
      const c = Math.cos(a), sn = Math.sin(a);
      body.moveTo(cx + c * (r - 7 * s), cy + sn * (r - 7 * s));
      body.lineTo(cx + c * (r + 19 * s), cy + sn * (r + 19 * s));
    };
    if (!two) {
      tick(-Math.PI / 2, 1);
    } else {
      tick(-Math.PI / 2 - 15 * DEG, 1);
      tick(-Math.PI / 2 + 15 * DEG, popScale);
    }
    ctx.save();
    ctx.lineCap = 'round';
    // an ink underlay so the tally still reads once the tissue has filled the frame
    ctx.strokeStyle = PAL.ink;
    ctx.globalAlpha = 0.22;
    ctx.lineWidth = 6.5;
    ctx.stroke(body);
    ctx.globalAlpha = 1;
    ctx.strokeStyle = PAL.annYellow;
    ctx.lineWidth = 3;
    ctx.stroke(body);
    if (pulse > 0) {
      ctx.globalAlpha = pulse;
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.arc(cx, cy, r + 26 * (1 - pulse), 0, TAU);
      ctx.stroke();
    }
    ctx.restore();
  }

  /** A yellow ring, with an ink underlay so it reads over the stripes. */
  function ring(ctx, x, y, r, color, alpha, ticks) {
    const p = new Path2D();
    p.moveTo(x + r, y);
    p.arc(x, y, r, 0, TAU);
    if (ticks) {
      for (let q = 0; q < 4; q++) {
        const a = Math.PI / 4 + (q * Math.PI) / 2;
        p.moveTo(x + Math.cos(a) * (r - 8), y + Math.sin(a) * (r - 8));
        p.lineTo(x + Math.cos(a) * (r + 8), y + Math.sin(a) * (r + 8));
      }
    }
    ctx.save();
    ctx.lineCap = 'round';
    ctx.strokeStyle = PAL.ink;
    ctx.globalAlpha = alpha * 0.22;
    ctx.lineWidth = 6;
    ctx.stroke(p);
    ctx.strokeStyle = color;
    ctx.globalAlpha = alpha;
    ctx.lineWidth = 3;
    ctx.stroke(p);
    ctx.restore();
  }

  /** Corner brackets framing the daughter pair inside the tissue: shot 11 pushes in on this. */
  function drawTargetFrame(ctx, sc, p) {
    if (p <= 0) return;
    const a = sc(CX - G4.r - 30, G4.upperY - G4.r - 40);
    const b = sc(CX + G4.r + 30, G4.lowerY + G4.r + 40);
    const arm = 38 * p;
    ctx.save();
    ctx.globalAlpha *= Math.min(1, p * 1.6);
    ctx.strokeStyle = PAL.annBlue;
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    const corner = (x, y, sx, sy) => {
      ctx.beginPath();
      ctx.moveTo(x, y + sy * arm);
      ctx.lineTo(x, y);
      ctx.lineTo(x + sx * arm, y);
      ctx.stroke();
    };
    corner(a[0], a[1], 1, 1);
    corner(b[0], a[1], -1, 1);
    corner(a[0], b[1], 1, -1);
    corner(b[0], b[1], -1, -1);
    // a short dashed leader down the axis between the two corners, so the pair is unmistakable
    ctx.setLineDash([9, 8]);
    ctx.lineWidth = 2;
    ctx.globalAlpha *= 0.7;
    ctx.beginPath();
    ctx.moveTo((a[0] + b[0]) / 2, a[1] + arm * 0.4);
    ctx.lineTo((a[0] + b[0]) / 2, a[1] + arm * 0.4 + 30 * p);
    ctx.moveTo((a[0] + b[0]) / 2, b[1] - arm * 0.4);
    ctx.lineTo((a[0] + b[0]) / 2, b[1] - arm * 0.4 - 30 * p);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.restore();
  }

  // ===========================================================================================
  // 10. BEATS (shot-local seconds; global T = 21.5 + t)
  // ===========================================================================================

  const B_SEAL = 0;        // T 21.5  the neck closes over three drawings, membranes seal
  const B_ARC = 0.5;       // T 22.0  the 'identical' arc draws, the tally flips 1 to 2
  const B_PULL = 1.0;      // T 22.5  the pull-back starts, 36 frames to zoom 0.45
  const B_TISSUE = 1.5;    // T 23.0  neighbours start popping in on 16ths, outward
  const B_FULL = 3.5;      // T 25.0  the field is full, the two daughters glow for three drawings
  const PULL_DUR = 1.5;    // 36 frames
  const ARC_OUT = 1.5;     // the arc starts fading here and is gone by 1.75

  const popAt = (i) => B_TISSUE + Math.floor((i * 2) / 3) * 0.125;

  // ===========================================================================================
  // 11. SCENE
  // ===========================================================================================

  FILM.scene({
    id: ID,
    draw(ctx, tIn, info) {
      const L = info.lib;
      const P = L.pal;
      const t = clamp(tIn, 0, info.dur);
      const d = Math.floor(t * 12 + 1e-6);          // drawing index, twelve a second
      const fr = t * 24;                            // frames since the shot started

      const drawingSince = (a) => Math.floor((t - a) * 12 + 1e-6);
      const hit = (a, frames, e, lead = 1) => (t < a ? 0 : (e || ((u) => u))(clamp((t - a) / (frames * FR) + lead / frames)));
      const popTwos = (a) => (t < a ? 0 : [0.72, 1.08, 1][Math.min(2, drawingSince(a))]);

      // --- 1. stripes, screen-fixed, with a jolt on the division hit ------------------------
      const jolt = fr < 4 ? 10 * (1 - fr / 4) : 0;
      L.stripes(ctx, {
        colors: [P.stripeCream, P.stripeYellow],
        width: 140,
        angle: -0.52,
        offset: 12 * info.T + jolt,
        seed: sd('stripes'),
      });

      // --- camera: locked to T 22.5, then the pull-back to 0.45 about (540, 900) ------------
      const zoom = t <= B_PULL ? 1 : q6(lerp(1, 0.45, inOutCubic((t - B_PULL) / PULL_DUR)));
      const camX = CX;
      const camY = G4.midY + 60 / zoom;
      const cam = { x: camX, y: camY, zoom };
      const V = makeView(zoom, camX, camY);
      // world to screen, for the overlays
      const sc = (x, y) => [540 + (x - camX) * zoom, 960 + (y - camY) * zoom];

      // the pair's state: joined for two drawings, then two sealed cells
      // the neck closes over three drawings on the beat: 60 px wide (G4), a thread, then apart
      const joined = d < 2;
      const neckHalf = d === 0 ? G4.neckHalf : 7;
      const flat = clamp(1 - Math.max(0, d - 2) / 2);
      const bright = t >= B_FULL && t < B_FULL + 0.25;

      L.camera(ctx, cam, (ctx) => {
        // --- 2. construction lines ---------------------------------------------------------
        drawConstruction(ctx, V, lerp(1, 0.42, sstep(1.0, 2.0, t)));

        // --- 3. the tissue, farthest first so nearer cells sit on top ----------------------
        if (t >= B_TISSUE - 1e-6) {
          for (let i = TISSUE.length - 1; i >= 0; i--) {
            const a = popAt(i);
            if (t < a - 1e-6) continue;
            const k = drawingSince(a);
            const scale = k <= 0 ? 0.62 : k === 1 ? 1.07 : 1;
            const alpha = k <= 0 ? 0.8 : 1;
            drawNeighbour(ctx, V, i, scale, alpha);
          }
        }

        // --- 4. the two daughters ----------------------------------------------------------
        if (joined) {
          // still one body: the G4 peanut under a single continuous membrane.
          // The cytoplasm fills the whole outline, including the neck, and each lobe carries its
          // own tone, so the two ends already read as two cells waiting to be cut apart.
          const poly = peanutPts(CX, G4.midY, Math.PI / 2, (G4.lowerY - G4.upperY) / 2, G4.r, neckHalf, G4.r * 0.045, sd('lobe'));
          fillPoly(ctx, poly, P.cytoplasm);
          for (const cy of [G4.upperY, G4.lowerY]) {
            const lobe = blobPts(CX, cy, G4.r, G4.r * 0.045, sd('lobe'), 44);
            const cres = crescent(lobe, CX, cy, G4.r * 0.30, 0.707, 0.707);
            if (cres) {
              hatchV(ctx, V, cres, {
                angle: -Math.PI / 4, spacing: 8, width: 1.4, color: P.cytoHatch, alpha: 0.8,
                length: [14, 46], seed: sd('cell', cy) + 11, inset: 4, overshoot: 4,
              });
            }
            const R = G4.r * 0.93;
            stippleV(ctx, V, { x: CX - R, y: cy - R, w: R * 2, h: R * 2 }, {
              spacing: 8.5,
              density: (x, y) => (hyp(x - CX, y - cy) < R ? 0.42 : 0),
              r: [1.0, 2.0], color: P.ribosome, alpha: 0.65, seed: sd('cell', cy) + 23,
            });
            const mito = cy === G4.upperY ? MITO_UPPER : MITO_LOWER;
            for (let i = 0; i < mito.length; i++) {
              paintMito(ctx, V, CX + mito[i][0], cy + mito[i][1], MITO_LEN, MITO_W, mito[i][2], sd('mito', cy) + i * 13, { ink: true });
            }
            daughterContents(ctx, V, cy, { bright: false });
          }
          paintHeroMembrane(ctx, V, poly);
          // the contractile ring: two short inkSoft creases either side of the closing neck
          const creases = new Path2D();
          for (const s of [-1, 1]) {
            creases.moveTo(CX + s * (neckHalf + 5), G4.midY - 36);
            creases.quadraticCurveTo(CX + s * (neckHalf - 11), G4.midY, CX + s * (neckHalf + 5), G4.midY + 36);
          }
          plainStroke(ctx, V, creases, P.inkSoft, 2.2, 0.6);
        } else {
          // two cells: the same outline drawn twice, each with a shallow flat where it parted,
          // healing over two drawings. Same size, same four chromosomes, identical to each other.
          for (const cy of [G4.upperY, G4.lowerY]) {
            const face = cy === G4.upperY ? 1 : -1;
            const poly = sealedPts(CX, cy, G4.r, face, flat, G4.r * 0.045, sd('lobe'));
            drawDaughterBody(ctx, V, poly, cy, { seed: sd('cell', cy), stipple: 0.42, bright });
            paintHeroMembrane(ctx, V, poly);
          }
        }
      });

      // --- 5. overlays, screen-fixed -------------------------------------------------------

      // the membranes seal: a small yellow ring at each new pole, on the drawing the neck closes
      if (d >= 2) {
        const p = hit(2 / 12, 5, outExpo);
        const fade = 1 - clamp((t - 2 / 12 - 4 * FR) / (6 * FR));
        if (fade > 0) {
          for (const [cy, sign] of [[G4.upperY, 1], [G4.lowerY, -1]]) {
            const w = sc(CX, cy + sign * (G4.r - 10));
            ring(ctx, w[0], w[1], (12 + 42 * p) * zoom, P.annYellow, fade, false);
          }
        }
      }

      // a yellow ring around each daughter on the beat the pair is named identical:
      // it expands with outExpo over six frames and is gone ten frames after the beat
      {
        const p = hit(B_ARC, 6, outExpo);
        const fade = 1 - clamp((t - B_ARC - 2 * FR) / (8 * FR));
        if (p > 0 && fade > 0) {
          for (const cy of [G4.upperY, G4.lowerY]) {
            const w = sc(CX, cy);
            ring(ctx, w[0], w[1], (G4.r + 8 + 92 * p) * zoom, P.annYellow, fade * 0.8, true);
          }
        }
      }

      // exactly one arcAnnotation: the two nuclei joined, labelled 'identical'.
      // The ends stop on the nucleus rims rather than their centres, and the arc rides the camera
      // so it stays on the nuclei while the pull-back starts, then fades over six frames.
      {
        const drawOn = hit(B_ARC, 6, outExpo);
        const fade = 1 - clamp((t - ARC_OUT) / (6 * FR));
        if (drawOn > 0 && fade > 0) {
          const c = sc(CX, G4.midY);
          const r = ((G4.lowerY - G4.upperY) / 2) * zoom;
          const inset = 22 * DEG;
          ctx.save();
          ctx.globalAlpha *= fade;
          L.arcAnnotation(ctx, c[0], c[1], r, -Math.PI / 2 - inset, -Math.PI * 1.5 + inset, {
            color: P.annBlue,
            width: 2.5,
            p: drawOn,
            endTicks: 12,
            dot: 5,
            label: 'identical',
            labelSize: 28,
            labelOffset: 44,
          });
          ctx.restore();
        }
      }

      // the tally ring: one tick, then two on the beat the arc draws
      {
        const two = t >= B_ARC - 1e-6;
        const pulse = two ? 1 - clamp((t - B_ARC) / (7 * FR)) : 0;
        drawTally(ctx, two, two ? popTwos(B_ARC) : 1, pulse);
      }

      // the target frame around the pair, drawn on once the field is nearly full
      drawTargetFrame(ctx, sc, hit(3.0, 6, outExpo));

      // the two daughters glow for three drawings when the field fills
      if (bright) {
        const g = 1 - drawingSince(B_FULL) / 3;
        for (const cy of [G4.upperY, G4.lowerY]) {
          const w = sc(CX, cy);
          ctx.save();
          ctx.globalAlpha = 0.85 * g;
          ctx.strokeStyle = P.chromoALight;
          ctx.lineWidth = 4;
          ctx.beginPath();
          ctx.arc(w[0], w[1], (G4.r + 16) * zoom, 0, TAU);
          ctx.stroke();
          ctx.restore();
        }
      }

      // --- 6. the cycle glyph, always last, never re-implemented ----------------------------
      L.cycleGlyph(ctx, info.T, 'illustrated');
    },
  });
})();
