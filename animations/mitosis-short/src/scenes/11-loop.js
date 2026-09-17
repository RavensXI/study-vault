// 11 loop : "One daughter becomes the hero — the cycle loops" (illustrated, global T 25.5 to 30.0)
//
// Frame 0 IS 10's last frame: its 24-cell tissue, pressed flat against itself, the two G4 daughters,
// its tally and its corner frame. The camera then pushes into the LOWER daughter over 72 frames from
// T 26.0 so that by T 29.0 it sits exactly on G1 at zoom 1 with 01's composition, held screen-fixed
// for the last 12 frames. The film loops out of this frame into 01's frame 0.
//
// World model (the one idea the whole file rests on):
//   The world IS 01's frame. The hero cell sits on G1 at (540, 900) with mean radius 380, and the
//   camera lands at { x: 540, y: 960, zoom: 1 }, which lib.camera renders as the identity, so world
//   pixels are frame pixels and every G1 number lands exactly where 01 draws it. 10's world is this
//   one shifted 340 px, and its camera pins world (540, 560) here at screen (540, 900) — which is
//   where this shot's camera starts, so the daughters open on screen 747 and 1053, 10's own pixels.
//   The daughter grows back from WIDE = 300/380 to 1 in five beat steps, and the whole field
//   expands about it by k = scale / WIDE, so k is 1 on frame 0 (10's field at 10's size) and 1.267
//   at the end. That expansion alone carries 18 of the 24 cells off the frame.
//
// Layers, back to front (frame px):
//   1 stripes, screen-fixed: stripeCream and stripeYellow, 140 px bands at -0.52. The drift runs
//     306 to 280, so the bands leave 10 unbroken and land on 01's phase at the loop.
//   2 the tissue: 10's 24 cells with 10's wobble seeds, stages, division axes and interiors, drawn
//     with its pressing rule (a cell inflated by 40 px, cut back on the radical plane between
//     neighbours) which relaxes back to round between T 26.0 and T 28.0 as the frame tightens
//   3 the fates inside that field: five of 10's cells become 01's five neighbours at (60,380)
//     (1020,420) (40,1420) (1040,1400) (540,1690) — cell 0 drifts in, cells 1, 5 and 6 finish the
//     division they were already in and their daughters take four of the places
//   4 the hero's construction lines: the 45 degree diameters, the square and the centre cross
//   5 the sibling daughter, drawn by the same painter as the hero (same size, same four
//     chromosomes), leaving the frame over the top from T 27.0
//   6 the hero cell: cytoplasm with cytoHatch rim hatching, ribosome stipple 0.42 to 0.35, six
//     mitochondria (the four 10 shared out migrate to their G1 places, two draw in on the beats),
//     the nucleus with its cross-hatch, nucleolus and four chromosomes relaxing into the G1 worms,
//     and the 6 px doubled ink membrane
//   7 overlays, screen-fixed: 10's tally and corner frame lifting over the first beat, the annBlue
//     reticle (r 400 and 440) and the annYellow 90 degree arc locking onto the hero, a beat ring on
//     each growth step, and the yellow burst from the nucleus on T 29.5
//   8 the wordmark 'studyvault' from T 28.5 (art bible section 9), then lib.cycleGlyph, last
//
// Line weights follow 10's rule, width * k^-0.75, so they read as 10's do while the camera is wide
// and land on the art bible's weights (membrane 6, nuclear rim 4) once the push-in is home.
(function () {
  'use strict';

  const ID = 'loop';
  const REF = 'hero-cell'; // 01 owns the G1 plate: its id seeds every G1 shape here
  const REF10 = 'two-cells'; // 10 owns the wide tissue this shot opens on
  const LIB = FILM.lib;
  const TAU = Math.PI * 2;
  const DEG = Math.PI / 180;
  const FR = 1 / 24;

  const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
  const lerp = (a, b, u) => a + (b - a) * u;
  const sstep = (a, b, x) => {
    const u = clamp((x - a) / (b - a));
    return u * u * (3 - 2 * u);
  };

  // every seed in the file derives from a shot id
  // Math.hypot is not bit-stable across V8's optimisation tiers: the same call can differ by one
  // last-place bit once a long render has tiered up, which moves a pixel and fails the frame hash.
  const hyp = (x, y) => Math.sqrt(x * x + y * y);

  const sd = (...k) => LIB.hash(ID, ...k) & 0x7fffffff;
  const sdG1 = (...k) => LIB.hash(REF, ...k) & 0x7fffffff; // shapes that must land on 01's plate
  const sdT = (...k) => LIB.hash(REF10, ...k) & 0x7fffffff; // the field 10 pulled back to

  // ---------------------------------------------------------------------------
  // Shared geometry (docs/storyboard.md, "Shared geometry" G1 and G4)
  // ---------------------------------------------------------------------------

  const CX = 540, CY = 900; // the hero cell's centre in frame pixels
  const R_CELL = 380; // G1 mean membrane radius
  const R_NUC = 170; // G1 mean nuclear radius
  const WIDE = 300 / 380; // G4: the daughter is the G1 cell at this scale (135/170 agrees)
  const SIB_GAP = 680; // G4: 1240 - 560, the gap between the daughters at the cut

  // Camera. 10 ends on lib.camera({ x: 540, y: 900 + 60 / 0.45, zoom: 0.45 }) in ITS world, which
  // is this one shifted 340 px down, so world (540, 560) here sits at screen (540, 900) on frame 0
  // and the daughters land on screen 747 and 1053, exactly where 10 leaves them. The push-in ends
  // on the identity, where world (540, 900) is screen (540, 900): G1.
  const CAM_Y0 = CY - SIB_GAP / 2 + 60 / 0.45; // 693.33
  const CAM_Y1 = 960; // world pixels are frame pixels
  const Z0 = 0.45, Z1 = 1;

  // the sibling's place in the expanding field, and how far it leaves over the top
  const SIB_F = [CX, CY - SIB_GAP / WIDE]; // (540, 38.7)
  const SIB_EXIT = -520;

  // G1 mitochondria: 6 beans, 60 by 28
  const MITO = [[300, 700], [760, 720], [280, 1060], [790, 1080], [420, 1190], [660, 640]];
  // 10 shares four out to each daughter, at its own offsets and angles (48 by 22 at the daughter's
  // scale, which is this table at the G1 scale). Each one migrates to the G1 place nearest it as
  // the cell grows, and the two the daughter is missing draw in on the growth beats.
  //   G1 index -> [offset x, offset y, angle] in G1 units about the cell centre
  const MITO_HERO = { 2: [-241, 108, 0.2], 1: [190, -196, 0.9], 0: [-133, -222, -0.55], 3: [209, 190, -1.0] };
  const MITO_SIB = { 0: [-222, -139, 0.45], 1: [203, -177, -0.75], 4: [-152, 209, -0.3], 3: [234, 120, 1.15] };
  const MITO_AT = [-1, -1, -1, -1, 2.0, 2.5]; // shot-local beat, -1 = there from frame 0

  // G1 chromosomes: two pairs, chromoA long (130 px), chromoB short (85 px), 20 degrees off
  // horizontal alternately left and right, drawn as loose worms so the four can be followed
  const CHR = [
    { cx: 470, cy: 850, len: 130, w: 15, kind: 'A', dir: 1, ph: 0.0 },
    { cx: 610, cy: 850, len: 130, w: 15, kind: 'A', dir: -1, ph: 1.9 },
    { cx: 480, cy: 955, len: 85, w: 13, kind: 'B', dir: 1, ph: 3.4 },
    { cx: 600, cy: 955, len: 85, w: 13, kind: 'B', dir: -1, ph: 5.1 },
  ];
  for (const c of CHR) c.ang = c.dir * 20 * DEG;

  // G1 neighbours: partial circles cut by the frame edge, radius 300 to 360
  const NEIGH = [
    { x: 60, y: 380, r: 330 },
    { x: 1020, y: 420, r: 340 },
    { x: 40, y: 1420, r: 320 },
    { x: 1040, y: 1400, r: 350 },
    { x: 540, y: 1690, r: 360 },
  ];

  // ---------------------------------------------------------------------------
  // The field this shot opens on — 10's tissue, copied verbatim from its handover block
  // (docs: src/scenes/10-two-cells.js, "HANDOVER TO SHOT 11"). 10's rows are in its own world;
  // y is shifted by -340 here so the lower daughter, the cell this shot pushes into, is the G1
  // hero at (540, 900). Cell i keeps 10's wobble seed, hash('two-cells', 'tissue', i).
  //   [ x, y, r, stage ]  stage null = interphase, else 'spindle' | 'pinchEarly|Mid|Late'
  // ---------------------------------------------------------------------------

  const T10_DY = -340;
  const TISSUE = [
    [-117, 894, 402, null], [1211, 590, 356, 'spindle'], [1247, 1250, 302, null],
    [14, 163, 339, 'pinchMid'], [647, -48, 301, null], [826, 1844, 352, 'pinchEarly'],
    [-59, 1785, 454, 'pinchLate'], [1245, -35, 267, null], [1830, 963, 341, null],
    [-750, 1253, 323, null], [-750, 463, 361, null], [1830, 309, 309, null],
    [83, -539, 358, null], [974, -559, 302, null], [1830, 1794, 488, null],
    [-762, 1980, 250, null], [-750, -449, 477, null], [1830, -490, 472, null],
    [505, 2720, 372, null], [1265, 2700, 360, null], [-235, 2700, 322, null],
    [456, -1190, 389, null], [1097, -1190, 248, null], [-750, -1190, 262, null],
  ];
  // 10's division axes, so a dividing cell parts the way it was already parting
  const DIV_AXIS = { 1: 0.38, 3: -0.52, 5: 1.22, 6: 2.42 };
  // 10's pressing rule: a cell is DRAWN at r + 40 (r + 8 if it is dividing) and cut back where it
  // meets another cell, on the radical plane between the two drawn radii less HALF_GAP, and round
  // each daughter at its 300 px radius plus HARD_GAP. That is what flattens the contact faces.
  const PRESS_PAD = 40, HALF_GAP = 7, HARD_GAP = 13;
  // pinch shapes as fractions of the packing radius: [ neckHalf, lobeR, lobeOffset ]
  const PINCH = {
    pinchEarly: [0.55, 0.60, 0.38],
    pinchMid: [0.34, 0.52, 0.46],
    pinchLate: [0.12, 0.46, 0.52],
  };

  // Where 10's field goes. Everything expands about the hero as the daughter grows back (the
  // factor k below), which carries all but six cells off the frame by T 28.5. Those six land 01's
  // five neighbours: cell 0 drifts in, cell 1 finishes its mitosis and one daughter takes the
  // upper-right place, cell 5 parts into the two lower ones, cell 6 gives the lower-left one.
  // slot = index into NEIGH; lobe = which side of the division axis takes it (+1 or -1).
  const FATE = {
    0: { slot: 0 },
    1: { split: 2.0, from: 'pinchEarly', at: 0.75, lobe: -1, slot: 1 },
    2: { push: [170, 0] },
    3: { push: [0, -80] },
    5: { split: 1.5, from: 'pinchEarly', at: 0.25, lobe: -1, slot: 3, lobe2: 1, slot2: 4 },
    6: { split: 0.5, from: 'pinchLate', at: 0, lobe: -1, slot: 2 },
  };

  // beats, shot-local seconds (T = 25.5 + t)
  const B_PUSH = 0.5; // T 26.0 the push-in begins, 72 frames
  const B_G1 = 1.0; // T 26.5 first growth step; the nearest neighbour's furrow closes
  const B_G2 = 1.5; // T 27.0 the chromosomes start to relax; the sibling leaves; lines fade in
  const B_G3 = 2.0; // T 27.5
  const B_G4 = 2.5; // T 28.0
  const B_G5 = 3.0; // T 28.5 growth complete; the wordmark fades in
  const B_LAND = 3.5; // T 29.0 the push-in lands on G1
  const B_RING = 4.0; // T 29.5 the yellow ring pulses from the nucleus
  const GBEATS = [B_G1, B_G2, B_G3, B_G4, B_G5];

  // ---------------------------------------------------------------------------
  // Line helpers
  // ---------------------------------------------------------------------------

  function addPoly(path, pts, closed, dx = 0, dy = 0) {
    if (!pts || pts.length < 2) return;
    path.moveTo(pts[0][0] + dx, pts[0][1] + dy);
    for (let i = 1; i < pts.length; i++) path.lineTo(pts[i][0] + dx, pts[i][1] + dy);
    if (closed) path.closePath();
  }

  // polyline displaced along its own normal by a boiling noise: the cheap version of an ink line
  function wobPts(L, pts, seed, amp, bi) {
    const n = pts.length;
    const out = new Array(n);
    let s = 0;
    const sdd = (seed + bi * 7919) | 0;
    for (let i = 0; i < n; i++) {
      const p = pts[i];
      if (i > 0) s += hyp(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]);
      const a = pts[i > 0 ? i - 1 : 0], b = pts[i < n - 1 ? i + 1 : n - 1];
      const tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = hyp(tx, ty) || 1;
      const d = amp * L.noise1(s * 0.02, sdd);
      out[i] = [p[0] - (ty / tl) * d, p[1] + (tx / tl) * d];
    }
    return out;
  }

  function wob(L, path, pts, seed, amp, bi, closed) {
    if (!pts || pts.length < 2) return;
    addPoly(path, wobPts(L, pts, seed, amp, bi), closed);
  }

  function stroke(ctx, path, color, alpha, width, dash) {
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

  function fillPath(ctx, path, color, alpha) {
    ctx.save();
    ctx.fillStyle = color;
    ctx.globalAlpha *= alpha == null ? 1 : alpha;
    ctx.fill(path);
    ctx.restore();
  }

  // a closed near-circle: the film never draws a cell as a perfect circle
  function blobPts(cx, cy, R, amp, n, seed) {
    const out = [];
    const k = R / 380;
    for (let i = 0; i < n; i++) {
      const a = (i / n) * TAU;
      const c = Math.cos(a), s = Math.sin(a);
      const w =
        0.72 * LIB.noise2(c * 1.7, s * 1.7, seed) +
        0.28 * LIB.noise2(c * 4.3, s * 4.3, seed + 1);
      out.push([cx + c * (R + amp * k * w), cy + s * (R + amp * k * w)]);
    }
    return out;
  }

  // a flat-ended ribbon around a centreline, rounded at the tips (chromosomes, mitochondria)
  function ribbonPts(pts, w, round) {
    const n = pts.length;
    const A = [], B = [];
    const rp = round == null ? 0.28 : round;
    for (let i = 0; i < n; i++) {
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = hyp(tx, ty) || 1;
      tx /= tl;
      ty /= tl;
      const u = n > 1 ? i / (n - 1) : 0.5;
      const e = Math.max(0, 1 - (2 * u - 1) * (2 * u - 1));
      const hw = (w / 2) * Math.pow(e, rp);
      A.push([pts[i][0] - ty * hw, pts[i][1] + tx * hw]);
      B.push([pts[i][0] + ty * hw, pts[i][1] - tx * hw]);
    }
    B.reverse();
    return A.concat(B);
  }

  // one chromosome centreline. rel 0 is the freshly decondensed copy the daughter starts with,
  // rel 1 is the loose G1 worm; the four are drawn in every frame, never hidden.
  function wormPts(c, rel, seed, n) {
    const m = n || 13;
    const len = c.len * lerp(0.9, 1, rel);
    const bow = c.len * lerp(0.05, 0.155, rel);
    const jit = lerp(1.4, 4.2, rel);
    const ca = Math.cos(c.ang), sa = Math.sin(c.ang);
    const out = [];
    for (let i = 0; i < m; i++) {
      const u = i / (m - 1) - 0.5;
      // one dominant lobe with a small kink on it: enough curve to read as a loose worm, never so
      // much that the two members of a pair run into each other and read as one chromosome
      const lat =
        bow * (Math.sin(u * TAU * 0.92 + c.ph) + 0.22 * Math.sin(u * TAU * 1.9 + c.ph * 2.3)) +
        jit * LIB.noise1(u * 7.3 + 2.1, seed);
      const ax = u * len + jit * 0.5 * LIB.noise1(u * 5.1 + 7.7, seed + 3);
      out.push([c.cx + ax * ca - lat * sa, c.cy + ax * sa + lat * ca]);
    }
    return out;
  }

  // a cheap shadow crescent inside a circle: 45 degree strokes, denser toward the lower right
  function crescent(path, R, spacing, seed, bi, frac) {
    const dx = Math.cos(-Math.PI / 4), dy = Math.sin(-Math.PI / 4);
    const nx = -dy, ny = dx; // points down-right, the shadow side
    const r = R * 0.94;
    let row = 0;
    for (let v = r * 0.06; v < r * 0.97; v += spacing, row++) {
      const h = Math.sqrt(Math.max(0, r * r - v * v));
      const dens = sstep(0.02, 0.5, v / r) * (frac == null ? 1 : frac);
      if (LIB.h3(row, 11, seed) > dens) continue;
      const jb = (LIB.h3(row, bi, seed + 5) - 0.5) * 1.6;
      const u0 = -h * (0.34 + 0.5 * LIB.h3(row, 3, seed));
      const u1 = h * (0.5 + 0.44 * LIB.h3(row, 7, seed));
      path.moveTo(u0 * dx + (v + jb) * nx, u0 * dy + (v + jb) * ny);
      path.lineTo(u1 * dx + (v + jb) * nx, u1 * dy + (v + jb) * ny);
    }
  }

  // ---------------------------------------------------------------------------
  // 10's shape builders, ported so this shot opens on its exact field
  // (src/scenes/10-two-cells.js sections 2 and 3; the seeds come from 10's id)
  // ---------------------------------------------------------------------------

  // A periodic radial wobble: five harmonics normalised, so a closed outline has no seam and the
  // shape is time-independent. The line boil on top of it comes from lib.inkPath.
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

  // An irregular near-circle with 10's wobble: the round state this field relaxes into.
  function wobBlob(cx, cy, r, amp, seed, n) {
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
   * A tissue cell pressed against its neighbours (10's rule, verbatim), blended with the same cell
   * left round. `press` 1 is 10's pressed field on frame 0; 0 is the round cell this shot ends on,
   * so the contact faces relax as the camera tightens on the hero.
   *   soft : [x, y, pressRadius] of another inflated cell — both are cut on the radical plane
   *   hard : [x, y, radius] of a daughter, which is not inflated: the tissue curves round it
   */
  function pressedBlobPts(cx, cy, r, amp, seed, n, soft, hard, press) {
    const w = wobbler(seed);
    const N = n || Math.max(32, Math.round(r * 0.16));
    const out = new Array(N);
    const floor = r * 0.5;
    for (let i = 0; i < N; i++) {
      const a = (i / N) * TAU;
      const ux = Math.cos(a), uy = Math.sin(a);
      const base = r + amp * w(a);
      let rr = base;
      if (press > 0.002) {
        for (let k = 0; k < soft.length; k++) {
          const vx = soft[k][0] - cx, vy = soft[k][1] - cy;
          const dist = Math.sqrt(vx * vx + vy * vy);
          if (dist < 1 || dist > r + soft[k][2]) continue;
          const cosang = (ux * vx + uy * vy) / dist;
          if (cosang <= 0.12) continue;
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
          if (disc <= 0) continue;
          const lim = uv - Math.sqrt(disc);
          if (lim > floor && lim < rr) rr = lim;
        }
        rr = base + (rr - base) * press;
      }
      out[i] = [cx + ux * rr, cy + uy * rr];
    }
    return out;
  }

  /**
   * A pinched cell (10's peanut): two lobes of radius R whose centres sit h either side of the
   * middle along the division axis, bridged by two opposing furrow arcs leaving a 2*hw neck.
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
    lobeArc(-h, Math.PI - tA, TAU + tA);
    furrowArc(xf, tA - Math.PI, -tA - Math.PI);
    lobeArc(h, -tA, Math.PI + tA);
    furrowArc(-xf, tA, -tA);
    return out;
  }

  /** 10's constant-width ribbon with rounded ends, for the X chromosomes on a spindle. */
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

  /** An X chromosome: two equal rods crossing at the centromere (the spindle neighbour). */
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

  // ---------------------------------------------------------------------------
  // Geometry, built once: a pure function of the constants above
  // ---------------------------------------------------------------------------

  let GEO = null;
  function geo(L) {
    if (GEO) return GEO;
    const g = {};

    // ---- the hero's G1 shapes (seeded from 01's id so this plate matches the plate 01 draws) ----
    g.hero = {
      outline: blobPts(CX, CY, R_CELL, 14, 40, sdG1('outline')),
      nucleus: blobPts(CX, CY, R_NUC, 7, 30, sdG1('nucleus')),
      nucleolus: blobPts(500, 870, 40, 3.2, 18, sdG1('nucleolus')),
      mito: MITO.map((m, i) => {
        const a = Math.atan2(m[1] - CY, m[0] - CX) + Math.PI / 2;
        return { x: m[0], y: m[1], a: a + (L.h3(i, 3, sdG1('mito')) - 0.5) * 0.8, seed: sdG1('mito', i) };
      }),
    };
    // the cytoplasm ring the stipple and the rim hatching live in
    g.hero.ring = [g.hero.outline, g.hero.nucleus.slice().reverse()];

    // ---- the wide tissue field: 10's 24 cells, in this shot's world ---------------------------
    // A cell sits at  hero + k * (p0 - hero) + drift, with k = scale / WIDE, so on frame 0 (k = 1)
    // the field IS 10's last frame and it spreads as the daughter grows back. Six cells are given
    // a fate (FATE above): five of 01's neighbours come out of them, three by finishing a division.
    const cells = [];
    for (let i = 0; i < TISSUE.length; i++) {
      const row = TISSUE[i];
      const stage = row[3];
      const f = FATE[i] || null;
      const c = {
        i,
        x0: row[0],
        y0: row[1] + T10_DY,
        rPack: row[2],
        R: row[2] + (stage ? 8 : PRESS_PAD), // 10 draws a dividing cell barely inflated
        stage0: stage,
        axis: DIV_AXIS[i] != null ? DIV_AXIS[i] : 0,
        seed: sdT('tissue', i), // 10's own wobble seed for this cell
        fate: f,
        push: (f && f.push) || null,
        slot: f && f.slot != null ? NEIGH[f.slot] : null,
        slot2: f && f.slot2 != null ? NEIGH[f.slot2] : null,
      };
      // 10's interior rules, drawn from the same rng in the same order, so the nuclei, chromosome
      // turns and mitochondria sit exactly where 10 put them
      const rr = L.rng(c.seed + 5);
      c.nucA = rr() * TAU;
      c.nucF = rr.range(0.38, 0.44);
      c.chrRot = rr.range(-0.7, 0.7);
      c.mitoN = 2 + (rr() < 0.5 ? 1 : 0);
      c.mito = [];
      for (let k = 0; k < c.mitoN; k++) c.mito.push([rr() * TAU, rr.range(0.5, 0.72), rr() * TAU]);
      c.mitoPinch = [[rr() * TAU, rr.range(0.3, 0.5), rr() * TAU], [rr() * TAU, rr.range(0.3, 0.5), rr() * TAU]];
      cells.push(c);
    }
    // 10's pressing partners: the cells whose inflated discs overlap this one on frame 0
    for (const c of cells) {
      c.soft = [];
      for (const o of cells) {
        if (o === c) continue;
        if (hyp(o.x0 - c.x0, o.y0 - c.y0) < c.R + o.R) c.soft.push(o);
      }
    }
    // farthest from the hero first, so nearer cells sit on top, as 10 draws them
    cells.sort((a, b) => hyp(b.x0 - CX, b.y0 - CY) - hyp(a.x0 - CX, a.y0 - CY));
    g.cells = cells;

    // ---- the hero's construction lines: 45 degree diameters and the faint square (01) ----------
    // both run past the membrane, as a drawing's construction does
    const D = 372; // 526 along each diagonal, 146 px clear of the 380 membrane
    g.cons = {
      diag: [
        [[CX - D, CY - D], [CX + D, CY + D]],
        [[CX + D, CY - D], [CX - D, CY + D]],
      ],
      // the square that circumscribes the G1 circle, and the centre cross carried out to the frame
      square: [[CX - 380, CY - 380], [CX + 380, CY - 380], [CX + 380, CY + 380], [CX - 380, CY + 380]],
      axis: [[[CX - 640, CY], [CX + 640, CY]], [[CX, CY - 760], [CX, CY + 900]]],
      marks: [[CX, CY - 380], [CX, CY + 380], [CX - 380, CY], [CX + 380, CY]],
    };

    GEO = g;
    return g;
  }

  // ---------------------------------------------------------------------------
  // Painters
  // ---------------------------------------------------------------------------

  // One mitochondrion: a bean 60 by 28 with folded inner ridges (art bible 10.1).
  // `simple` is the cheap version for cells that are small on screen.
  function drawMito(ctx, L, P, m, prog, px, bi, alpha, simple) {
    if (prog <= 0.02) return;
    const len = 60 * prog, w = 28 * prog;
    const ca = Math.cos(m.a), sa = Math.sin(m.a);
    const mid = [];
    for (let i = 0; i <= 8; i++) {
      const u = i / 8 - 0.5;
      const bow = 7 * (1 - 4 * u * u);
      mid.push([m.x + u * len * ca - bow * sa, m.y + u * len * sa + bow * ca]);
    }
    const out = ribbonPts(mid, w, 0.42);
    const body = new Path2D();
    wob(L, body, out, m.seed, 0.9, bi, true);
    fillPath(ctx, body, P.mito, alpha);
    if (simple) {
      const r2 = new Path2D();
      for (let i = 0; i < 3; i++) {
        const u = -0.25 + i * 0.25;
        const bow = 7 * (1 - 4 * u * u);
        const cxp = m.x + u * len * ca - bow * sa, cyp = m.y + u * len * sa + bow * ca;
        const h = (w / 2) * 0.72 * prog;
        r2.moveTo(cxp - sa * h, cyp + ca * h);
        r2.lineTo(cxp + sa * h, cyp - ca * h);
      }
      stroke(ctx, r2, P.mitoDeep, 0.8 * alpha, px(1.5));
      stroke(ctx, body, P.ink, 0.9 * alpha, px(2));
      return;
    }
    // inner ridges: short folds crossing the short axis
    const ridge = new Path2D();
    const nR = 4;
    for (let i = 0; i < nR; i++) {
      const u = -0.3 + (0.6 * i) / (nR - 1);
      const bow = 7 * (1 - 4 * u * u);
      const cxp = m.x + u * len * ca - bow * sa, cyp = m.y + u * len * sa + bow * ca;
      const h = (w / 2) * 0.78 * prog;
      const j = (L.h3(i, bi, m.seed) - 0.5) * 2.2;
      ridge.moveTo(cxp - sa * h + ca * j, cyp + ca * h + sa * j);
      ridge.quadraticCurveTo(cxp + ca * (j + 4), cyp + sa * (j + 4), cxp + sa * h + ca * j, cyp - ca * h + sa * j);
    }
    stroke(ctx, ridge, P.mitoDeep, 0.85 * alpha, px(1.8));
    // shadow side
    const sh = new Path2D();
    for (let i = 0; i < 5; i++) {
      const u = -0.34 + i * 0.17;
      const bow = 7 * (1 - 4 * u * u);
      const cxp = m.x + u * len * ca - bow * sa, cyp = m.y + u * len * sa + bow * ca;
      const h = (w / 2) * 0.86 * prog;
      sh.moveTo(cxp + sa * h * 0.15, cyp - ca * h * 0.15);
      sh.lineTo(cxp + sa * h, cyp - ca * h);
    }
    ctx.save();
    ctx.clip(body);
    stroke(ctx, sh, P.mitoDeep, 0.5 * alpha, px(1.4));
    ctx.restore();
    L.inkPath(ctx, out, { closed: true, width: px(2.2), color: P.ink, alpha: 0.92 * alpha, seed: m.seed + 3, wobble: 0.8, step: 3 });
  }

  // One chromosome as a loose worm: fill, ink outline, faint centre line, shadow hatching.
  function drawWorm(ctx, L, P, c, rel, seed, px, bi, alpha, lod) {
    const mid = wormPts(c, rel, seed, lod >= 2 ? 15 : 9);
    const w = c.w * lerp(1.22, 1, rel);
    const out = ribbonPts(mid, w, 0.3);
    const base = c.kind === 'A' ? P.chromoA : P.chromoB;
    const deep = c.kind === 'A' ? P.chromoADeep : P.chromoBDeep;
    const body = new Path2D();
    wob(L, body, out, seed + 1, 0.7, bi, true);
    fillPath(ctx, body, L.mix(base, deep, 0.42 * (1 - rel)), alpha);
    if (lod >= 2) {
      const hatch = new Path2D();
      for (let i = 1; i < mid.length - 1; i += 2) {
        const p = mid[i];
        const a = mid[i - 1], b = mid[i + 1];
        let tx = b[0] - a[0], ty = b[1] - a[1];
        const tl = hyp(tx, ty) || 1;
        tx /= tl;
        ty /= tl;
        const h = (w / 2) * 0.9;
        const j = (L.h3(i, bi, seed) - 0.5) * 1.4;
        hatch.moveTo(p[0] - ty * h * 0.05 + tx * j, p[1] + tx * h * 0.05 + ty * j);
        hatch.lineTo(p[0] - ty * h + tx * j, p[1] + tx * h + ty * j);
      }
      stroke(ctx, hatch, deep, 0.5 * alpha, px(1.3));
      const spine = new Path2D();
      wob(L, spine, mid, seed + 7, 0.5, bi, false);
      stroke(ctx, spine, P.inkFaint, 0.45 * alpha, px(1.1));
    }
    L.inkPath(ctx, out, { closed: true, width: px(2), color: P.ink, alpha: 0.9 * alpha, seed: seed + 11, wobble: 0.7, step: 3 });
  }

  // The hero cell (and its identical sibling) in G1 coordinates: the caller has put the context in
  // hero space, so every number below is a G1 number and lands where 01 draws it.
  function drawHeroCell(ctx, L, P, g, o) {
    // 10's line rule: a width reads at w * k^0.25 screen px while the camera is wide and lands on
    // exactly w, the art bible's weight, once the push-in is home
    const px = (w) => w * Math.pow(o.k, -0.75);
    const bi = o.bi, A = o.alpha, so = o.seedOff | 0;
    const H = g.hero;
    const lod = o.lod;

    // construction lines, behind the cell: the diameters at 45 degrees and the faint square
    if (o.cons > 0) {
      const a = 0.46 * o.cons * A;
      for (let i = 0; i < 2; i++) {
        L.inkPath(ctx, g.cons.diag[i], {
          width: px(1.5), color: P.inkFaint, alpha: a, seed: sdG1('diag', i) + so,
          smooth: false, step: 10, taper: [0, 0], wobble: 1.6,
        });
      }
      const sq = new Path2D();
      wob(L, sq, L.smoothPts(g.cons.square, true, 40), sdG1('square') + so, 1.6, bi, true);
      stroke(ctx, sq, P.inkFaint, a * 0.8, px(1.5));
      for (let i = 0; i < g.cons.axis.length; i++) {
        L.inkPath(ctx, g.cons.axis[i], {
          width: px(1.5), color: P.inkFaint, alpha: a * 0.5, seed: sdG1('axis', i) + so,
          smooth: false, step: 12, taper: [0, 0], wobble: 1.8,
        });
      }
      const mk = new Path2D();
      for (const p of g.cons.marks) {
        mk.moveTo(p[0] - 11, p[1]);
        mk.lineTo(p[0] + 11, p[1]);
        mk.moveTo(p[0], p[1] - 11);
        mk.lineTo(p[0], p[1] + 11);
      }
      stroke(ctx, mk, P.inkFaint, a * 1.5, px(1.5));
    }

    // 1 cytoplasm
    const cyto = new Path2D();
    wob(L, cyto, H.outline, sdG1('outline') + so, 2.4, bi, true);
    fillPath(ctx, cyto, P.cytoplasm, A);

    // 2 directional hatching in cytoHatch near the membrane, heavier on the lower right
    L.hatch(ctx, H.outline, {
      angle: -Math.PI / 4,
      spacing: px(9),
      width: px(1.5),
      color: P.cytoHatch,
      alpha: 0.9 * A,
      length: [px(16), px(52)],
      gap: [px(3), px(9)],
      inset: px(5),
      overshoot: px(2),
      clip: true,
      seed: sd('cyto', so),
      density: (x, y) => {
        const d = hyp(x - CX, y - CY) / R_CELL;
        const lit = (x - CX + (y - CY)) / (R_CELL * 1.414);
        return (0.34 + 0.66 * sstep(0.34, 0.95, d)) * lerp(0.34, 1, sstep(-0.8, 0.7, lit));
      },
    });

    // 2b deep shade: a second layer at 105 degrees in the lower-right corner of the cytoplasm,
    // where the form turns away from the light
    if (lod >= 2) {
      L.hatch(ctx, H.outline, {
        angle: -Math.PI / 4 - Math.PI / 3,
        spacing: px(12),
        width: px(1.3),
        color: P.cytoHatch,
        alpha: 0.65 * A,
        length: [px(14), px(40)],
        gap: [px(4), px(10)],
        inset: px(6),
        clip: true,
        seed: sd('cyto2', so),
        density: (x, y) => {
          const d = hyp(x - CX, y - CY) / R_CELL;
          const lit = (x - CX + (y - CY)) / (R_CELL * 1.414);
          return sstep(0.6, 0.95, d) * sstep(0.1, 0.75, lit);
        },
      });
    }

    // 3 ribosomes: fine stipple through the cytoplasm, thickening as the cell grows
    L.stipple(ctx, H.ring, {
      spacing: px(7.6),
      r: [px(1.0), px(2.1)],
      color: P.ribosome,
      alpha: 0.55 * A,
      seed: sd('ribo', so),
      density: o.stip,
    });

    // 4 mitochondria: the four 10 shared out to this daughter migrate to their G1 places as the
    // cell grows, and the two it is missing draw in on the growth beats
    for (let i = 0; i < H.mito.length; i++) {
      const m = H.mito[i];
      const from = o.mitoFrom && o.mitoFrom[i];
      const mm = from
        ? {
            x: lerp(CX + from[0], m.x, o.mig),
            y: lerp(CY + from[1], m.y, o.mig),
            a: lerp(from[2], m.a, o.mig),
            seed: m.seed,
          }
        : m;
      drawMito(ctx, L, P, mm, o.mito[i], px, bi, A);
    }

    // 5 the nucleus: fill, cross-hatch shadow along its lower left (01), nucleolus, chromosomes
    const nuc = new Path2D();
    wob(L, nuc, H.nucleus, sdG1('nucleus') + so, 1.8, bi, true);
    fillPath(ctx, nuc, P.nucleus, A);
    L.crossHatch(ctx, H.nucleus, {
      angle: -Math.PI / 4,
      spacing: px(7.5),
      crossSpacing: px(10),
      width: px(1.4),
      color: P.nucleusDeep,
      alpha: 0.72 * A,
      layers: 2,
      length: [px(12), px(34)],
      gap: [px(3), px(8)],
      inset: px(4),
      clip: true,
      seed: sd('nuchatch', so),
      density: (x, y) => sstep(0.1, 1.05, (CX - x + (y - CY)) / (R_NUC * 1.414)),
    });
    if (o.nucleolus > 0.01) {
      const nl = new Path2D();
      wob(L, nl, H.nucleolus, sdG1('nucleolus') + so, 1.4, bi, true);
      fillPath(ctx, nl, P.nucleusDeep, 0.92 * A * o.nucleolus);
      if (lod >= 2) {
        L.stipple(ctx, H.nucleolus, {
          spacing: px(5),
          r: [px(0.9), px(1.7)],
          color: P.ink,
          alpha: 0.28 * A * o.nucleolus,
          seed: sd('nucleolus', so),
          density: 0.8,
        });
        stroke(ctx, nl, P.nucleusRim, 0.38 * A * o.nucleolus, px(1.8));
      }
    }
    for (let i = 0; i < CHR.length; i++) {
      drawWorm(ctx, L, P, CHR[i], o.rel, sdG1('chr', i) + so, px, bi, A, lod);
    }
    L.inkPath(ctx, H.nucleus, {
      closed: true, width: px(4), color: P.nucleusRim, alpha: 0.95 * A,
      seed: sdG1('nucrim') + so, wobble: 1.5, step: 3.2,
    });

    // 6 the membrane: one continuous doubled ink line
    L.inkPath(ctx, H.outline, {
      closed: true, width: px(6), color: P.membrane, alpha: A,
      seed: sdG1('membrane') + so, wobble: 1.8, step: 3.2,
      double: { width: 0.25, offset: px(3.2), alpha: 0.4 },
    });
  }

  // Four chromosomes inside a neighbour's nucleus: two pairs, never a different count.
  // The whole set is turned (and sometimes mirrored) per cell, so a field of nuclei does not read
  // as a field of identical faces.
  function neighbourChromo(ctx, L, P, R, px, bi, seed, lod, alpha, rot, flip) {
    const k = R / R_NUC;
    const ca = Math.cos(rot || 0), sa = Math.sin(rot || 0);
    const fl = flip || 1;
    for (let i = 0; i < CHR.length; i++) {
      const c = CHR[i];
      const lx = (c.cx - CX) * k * fl, ly = (c.cy - CY) * k;
      const nc = {
        cx: lx * ca - ly * sa,
        cy: lx * sa + ly * ca,
        len: c.len * k,
        w: c.w * k,
        kind: c.kind,
        dir: c.dir * fl,
        ph: c.ph,
        ang: c.ang * fl + (rot || 0),
      };
      if (lod >= 2) {
        drawWorm(ctx, L, P, nc, 1, seed + i * 31, px, bi, alpha, 1);
      } else {
        const mid = wormPts(nc, 1, seed + i * 31, 8);
        const p = new Path2D();
        addPoly(p, wobPts(L, mid, seed + i, 0.6, bi), false);
        stroke(ctx, p, c.kind === 'A' ? P.chromoA : P.chromoB, 0.88 * alpha, Math.max(px(1.8), nc.w * 0.64));
      }
    }
  }

  // ---------------------------------------------------------------------------
  // Tissue cells, in world coordinates, drawn 10's way: pressed contact faces on frame 0 that
  // relax back to round as the camera tightens, the same nuclei, chromosome turns, mitochondria
  // and mid-division stages. `st` carries this frame's state for one cell.
  // ---------------------------------------------------------------------------

  // the cytoplasm of a neighbour: flat fill, a hatched crescent in the shadow rim, ribosome stipple
  function paintNeighbourCyto(ctx, L, P, poly, cx, cy, R, seed, bi, px, lod) {
    const body = new Path2D();
    addPoly(body, poly, true);
    fillPath(ctx, body, P.neighbour, 1.22);
    const sh = new Path2D();
    crescent(sh, R * 0.94, px(11), seed + 11, bi, lod >= 2 ? 1 : 0.8);
    ctx.save();
    ctx.clip(body);
    ctx.translate(cx, cy);
    stroke(ctx, sh, P.cytoHatch, 0.62, px(1.4));
    ctx.restore();
    if (lod >= 2) {
      const lite = [];
      for (let k = 0; k < poly.length; k += 2) lite.push(poly[k]);
      L.stipple(ctx, lite, {
        spacing: px(11), r: [px(1.0), px(2.0)], color: P.ribosome, alpha: 0.5,
        seed: seed + 23, density: 0.3, pad: -6,
      });
    }
    return body;
  }

  // a neighbour's nucleus: mauve near-circle, shaded crescent, nucleolus, inkSoft rim
  function paintNeighbourNucleus(ctx, L, P, nx, ny, nr, seed, bi, px, lod) {
    const poly = wobBlob(nx, ny, nr, nr * 0.035, seed, Math.max(20, Math.round(nr * 0.3)));
    const np = new Path2D();
    addPoly(np, poly, true);
    fillPath(ctx, np, P.neighbourNucleus, 1);
    const sh = new Path2D();
    crescent(sh, nr * 0.95, px(7), seed + 31, bi, 0.95);
    ctx.save();
    ctx.clip(np);
    ctx.translate(nx, ny);
    ctx.rotate(Math.PI / 2); // the nucleus takes its shade on the lower left, as 01 draws it
    stroke(ctx, sh, P.nucleusDeep, 0.5, px(1.2));
    ctx.restore();
    const ol = new Path2D();
    ol.arc(nx - nr * (40 / 170), ny - nr * (30 / 170), nr * (40 / 170), 0, TAU);
    fillPath(ctx, ol, P.nucleusDeep, 0.85);
    stroke(ctx, np, P.nucleusRim, 0.7, px(3));
    return poly;
  }

  // 10's mitochondria inside a neighbour: R * 0.17 long, a third as wide
  function paintNeighbourMito(ctx, L, P, cx, cy, R, list, seed, bi, px, lod, scaleF) {
    for (let i = 0; i < list.length; i++) {
      const a = list[i][0], dF = list[i][1], ang = list[i][2];
      const len = R * (scaleF || 0.17);
      const sc = len / 60;
      ctx.save();
      ctx.translate(cx + Math.cos(a) * R * dF, cy + Math.sin(a) * R * dF);
      ctx.scale(sc, sc);
      drawMito(ctx, L, P, { x: 0, y: 0, a: ang, seed: seed + 91 + i * 7 }, 1, (w) => px(w) / sc, bi, 1, lod < 2);
      ctx.restore();
    }
  }

  /** An interphase tissue cell, or one lobe of a cell that has just parted. */
  function paintInterphaseCell(ctx, L, P, st) {
    const cx = st.cx, cy = st.cy, R = st.R, bi = st.bi, lod = st.lod, px = st.px, seed = st.seed;
    const poly = st.press > 0.002
      ? pressedBlobPts(cx, cy, R, R * 0.045, seed, Math.max(30, Math.round(R * 0.15)), st.soft, st.hard, st.press)
      : wobBlob(cx, cy, R, R * 0.045, seed, Math.max(30, Math.round(R * 0.15)));
    paintNeighbourCyto(ctx, L, P, poly, cx, cy, R, seed + 3, bi, px, lod);
    if (lod >= 1) {
      const off = R * 0.1;
      const nx = cx + Math.cos(st.nucA) * off, ny = cy + Math.sin(st.nucA) * off;
      const nucR = R * st.nucF;
      paintNeighbourNucleus(ctx, L, P, nx, ny, nucR, seed + 61, bi, px, lod);
      if (st.chrA > 0.02) {
        ctx.save();
        ctx.translate(nx, ny);
        neighbourChromo(ctx, L, P, nucR, px, bi, seed + 71, lod, 0.72 * st.chrA, st.chrRot, 1);
        ctx.restore();
      }
      paintNeighbourMito(ctx, L, P, cx, cy, R, st.mito, seed, bi, px, lod, 0.17);
    }
    if (lod >= 2) {
      L.inkPath(ctx, poly, { closed: true, width: px(3.6), color: P.ink, alpha: 0.78, seed: seed + 101, wobble: 2.4, step: 3.4 });
    } else {
      const ink = new Path2D();
      addPoly(ink, poly, true);
      stroke(ctx, ink, P.ink, 0.78, px(3.6));
    }
  }

  /** A pinching tissue cell: 10's peanut, a nucleus in each lobe, two furrow creases. */
  function paintPinchCell(ctx, L, P, st) {
    const cx = st.cx, cy = st.cy, R = st.R, bi = st.bi, lod = st.lod, px = st.px, seed = st.seed;
    const axis = st.axis;
    const hwF = st.pinchF[0], lobeF = st.pinchF[1], offF = st.pinchF[2];
    const ca = Math.cos(axis), sa = Math.sin(axis);
    const poly = peanutPts(cx, cy, axis, R * offF, R * lobeF, R * hwF, R * 0.04, seed);
    paintNeighbourCyto(ctx, L, P, poly, cx, cy, R * 0.92, seed + 3, bi, px, lod);
    if (lod >= 1) {
      const nucR = R * lobeF * 0.45;
      for (const sg of [-1, 1]) {
        const nx = cx + ca * sg * R * offF, ny = cy + sa * sg * R * offF;
        paintNeighbourNucleus(ctx, L, P, nx, ny, nucR, seed + 61, bi, px, lod);
        if (st.chrA > 0.02) {
          ctx.save();
          ctx.translate(nx, ny);
          neighbourChromo(ctx, L, P, nucR, px, bi, seed + 71, lod, 0.72 * st.chrA, axis, 1);
          ctx.restore();
        }
      }
      paintNeighbourMito(ctx, L, P, cx, cy, R, st.mitoPinch, seed, bi, px, lod, 0.16);
    }
    if (lod >= 2) {
      L.inkPath(ctx, poly, { closed: true, width: px(3.6), color: P.ink, alpha: 0.78, seed: seed + 101, wobble: 2.4, step: 3.4 });
    } else {
      const ink = new Path2D();
      addPoly(ink, poly, true);
      stroke(ctx, ink, P.ink, 0.78, px(3.6));
    }
    const creases = new Path2D();
    for (const sg of [-1, 1]) {
      const hx = cx - sa * sg * R * hwF, hy = cy + ca * sg * R * hwF;
      creases.moveTo(hx - ca * R * 0.1, hy - sa * R * 0.1);
      creases.quadraticCurveTo(hx - sa * sg * R * 0.05, hy + ca * sg * R * 0.05, hx + ca * R * 0.1, hy + sa * R * 0.1);
    }
    stroke(ctx, creases, P.inkSoft, 0.55, px(2));
  }

  /** The metaphase neighbour: an elongated cell, two poles, four X chromosomes on the plate. */
  function paintSpindleCell(ctx, L, P, st) {
    const cx = st.cx, cy = st.cy, R = st.R, bi = st.bi, lod = st.lod, px = st.px, seed = st.seed;
    const axis = st.axis;
    const ca = Math.cos(axis), sa = Math.sin(axis);
    const w = wobbler(seed);
    const N = Math.max(34, Math.round(R * 0.16));
    const poly = new Array(N);
    const cr = Math.cos(axis - Math.PI / 2), sr = Math.sin(axis - Math.PI / 2);
    for (let i = 0; i < N; i++) {
      const ang = (i / N) * TAU;
      const k = 1 + 0.035 * w(ang);
      const lx = Math.cos(ang) * R * 0.78 * k, ly = Math.sin(ang) * R * 0.99 * k;
      poly[i] = [cx + lx * cr - ly * sr, cy + lx * sr + ly * cr];
    }
    paintNeighbourCyto(ctx, L, P, poly, cx, cy, R * 0.88, seed + 3, bi, px, lod);
    const poleD = R * 0.84;
    const Q1 = [cx - ca * poleD, cy - sa * poleD];
    const Q2 = [cx + ca * poleD, cy + sa * poleD];
    const plate = [-0.37, -0.12, 0.12, 0.37].map((u) => [cx - sa * u * R, cy + ca * u * R]);
    const kinds = ['A', 'B', 'B', 'A'];
    if (lod >= 1) {
      const fib = new Path2D();
      for (const Q of [Q1, Q2]) {
        for (const q of plate) {
          const mx = (Q[0] + q[0]) / 2 - sa * (q[0] - cx) * 0.08;
          const my = (Q[1] + q[1]) / 2 + ca * (q[1] - cy) * 0.08;
          fib.moveTo(Q[0], Q[1]);
          fib.quadraticCurveTo(mx, my, q[0], q[1]);
        }
        for (let i = -3; i <= 3; i++) {
          if (!i) continue;
          const u = i * 0.13;
          fib.moveTo(Q[0], Q[1]);
          fib.lineTo(cx - sa * u * R * 2.4 + (Q[0] - cx) * -0.22, cy + ca * u * R * 2.4 + (Q[1] - cy) * -0.22);
        }
      }
      stroke(ctx, fib, P.fibre, 0.7, px(1.8));
    }
    for (let i = 0; i < plate.length; i++) {
      const long = kinds[i] === 'A';
      const rods = xChromoRods(plate[i][0], plate[i][1], R * (long ? 0.27 : 0.2), R * 0.062, axis + Math.PI / 2);
      const col = long ? P.chromoA : P.chromoB;
      const deep = long ? P.chromoADeep : P.chromoBDeep;
      for (const rod of rods) {
        const rp = new Path2D();
        addPoly(rp, rod, true);
        fillPath(ctx, rp, col, 0.96);
        stroke(ctx, rp, deep, 0.85, px(1.8));
      }
      const dot = new Path2D();
      dot.arc(plate[i][0], plate[i][1], R * 0.034, 0, TAU);
      fillPath(ctx, dot, P.centromere, 1);
    }
    for (const pole of [[Q1, 201], [Q2, 203]]) {
      const Q = pole[0], pr = R * 0.062;
      const pp = new Path2D();
      addPoly(pp, wobBlob(Q[0], Q[1], pr, pr * 0.12, seed + pole[1], 18), true);
      fillPath(ctx, pp, P.pole, 0.95);
      const ticks = new Path2D();
      for (let i = 0; i < 12; i++) {
        const a = (i / 12) * TAU + 0.2;
        ticks.moveTo(Q[0] + Math.cos(a) * pr * 1.05, Q[1] + Math.sin(a) * pr * 1.05);
        ticks.lineTo(Q[0] + Math.cos(a) * pr * 1.85, Q[1] + Math.sin(a) * pr * 1.85);
      }
      stroke(ctx, ticks, P.inkSoft, 0.85, px(1.6));
      stroke(ctx, pp, P.inkSoft, 0.85, px(1.6));
    }
    if (lod >= 2) {
      L.inkPath(ctx, poly, { closed: true, width: px(3.6), color: P.ink, alpha: 0.78, seed: seed + 101, wobble: 2.4, step: 3.4 });
    } else {
      const ink = new Path2D();
      addPoly(ink, poly, true);
      stroke(ctx, ink, P.ink, 0.78, px(3.6));
    }
  }

  // ---------------------------------------------------------------------------
  // Overlays (screen-fixed, drawn over the illustration at full opacity)
  // ---------------------------------------------------------------------------

  function ringPath(x, y, r, ticks, tick) {
    const p = new Path2D();
    p.moveTo(x + r, y);
    p.arc(x, y, r, 0, TAU);
    if (ticks) {
      for (let i = 0; i < ticks; i++) {
        const a = (i / ticks) * TAU + Math.PI / ticks;
        p.moveTo(x + Math.cos(a) * r, y + Math.sin(a) * r);
        p.lineTo(x + Math.cos(a) * (r + tick), y + Math.sin(a) * (r + tick));
      }
    }
    return p;
  }

  // ---------------------------------------------------------------------------
  // Scene
  // ---------------------------------------------------------------------------

  FILM.scene({
    id: ID,
    draw(ctx, tIn, info) {
      const L = info.lib, P = L.pal, E = L.ease;
      const dur = info.dur;
      // snap near-frame times onto the frame grid so beat comparisons never miss by one ulp
      let t = clamp(tIn, 0, dur);
      const tFrame = Math.round(t * 24) / 24;
      if (Math.abs(t - tFrame) < 1e-4) t = tFrame + 1e-7;
      const tw = L.onTwos(t); // objects move on twos
      const bi = L.boil(info.T); // every ink line boils at 12 fps
      const g = geo(L);

      // drawings since beat a (0 on the beat frame and the frame after)
      const drawing = (a) => Math.floor((t - a) * 12 + 1e-6);
      // progress already visible on the beat frame itself
      const hit = (a, frames, e, lead = 1) => {
        if (t < a) return 0;
        const u = clamp((t - a) / (frames * FR) + lead / frames);
        return e ? e(u) : u;
      };
      const popTwos = (a) => (t < a ? 0 : [0.72, 1.08, 1][Math.min(2, drawing(a))]);

      // ---- 1 stripes, screen-fixed ------------------------------------------------------
      // Both seams have to hold: 10 leaves the bands at 12 * 25.5 = 306, and 01 opens on 0, which is
      // the same phase as 280 (two 140 px bands). So the drift runs 306 to 280 across the shot: the
      // bands keep moving, the cut from 10 does not jump, and the loop back into 01 lands on its
      // exact phase. The edge wobble is seeded from 01's id, so the band edges match at the loop.
      L.stripes(ctx, {
        colors: [P.stripeCream, P.stripeYellow],
        width: 140,
        angle: -0.52,
        offset: 306 - (26 * (info.T - 25.5)) / 4.5,
        seed: sdG1('stripes'),
      });

      // ---- 2 camera and the growth clock -------------------------------------------------
      // the push-in: zoom 0.45 to 1.00 over 72 frames from T 26.0, inOutSine, landing on G1
      const pu = E.inOutSine(clamp((t - B_PUSH) / (B_LAND - B_PUSH)));
      const zoom = lerp(Z0, Z1, pu);
      const camY = lerp(CAM_Y0, CAM_Y1, pu);

      // the daughter grows back to G1 size in five beat steps, each a 3-drawing pop
      let grow = 0;
      for (let i = 0; i < GBEATS.length; i++) {
        if (tw < GBEATS[i]) break;
        grow = (i + popTwos(GBEATS[i])) / GBEATS.length;
      }
      const s = WIDE + (1 - WIDE) * grow; // hero (and field) scale: WIDE at the cut, 1 on G1
      const kH = s * zoom; // hero local units to screen pixels
      const hsx = 540, hsy = 960 + (CY - camY) * zoom; // the hero's screen centre

      // the chromosomes relax from single copies into the G1 worms over T 27.0 to 28.5
      const rel = E.inOutSine(clamp((tw - B_G2) / (B_G5 - B_G2)));
      // 10 leaves the daughters with a dense cytoplasm and a nucleolus already reformed; both
      // settle onto 01's values as the cell grows
      const stip = lerp(0.42, 0.35, grow);
      const nucleolus = 1;
      // three mitochondria are there from the cut, three draw in on the beats
      const mitoProg = MITO_AT.map((a, i) =>
        a < 0 ? 1 : tw < a ? 0 : E.outBack(clamp((tw - a) / (4 * FR) + 0.25)) * (0.55 + 0.45 * clamp((tw - a) / (4 * FR) + 0.25))
      );
      // construction lines fade in behind the hero
      const cons = sstep(B_G2, B_G4, t);
      // the shared-out mitochondria migrate from 10's places to the G1 six
      const mig = E.inOutSine(clamp((tw - B_PUSH) / (B_G4 - B_PUSH)));

      // the sibling daughter: the same cell, leaving over the top of the frame from T 27.0
      const sibLeave = E.inOutCubic(clamp((t - B_G2) / (B_G5 - B_G2)));
      const sibX = CX + s * (SIB_F[0] - CX);
      const sibY = CY + s * (SIB_F[1] - CY) + SIB_EXIT * sibLeave;

      // 01's neighbours hold a plain nucleus with its nucleolus, so the field's chromosomes ease
      // away as the hero takes the frame and the loop hands over cleanly
      const nChr = 1 - sstep(2.2, 3.2, t);
      // the field expands about the hero at the same rate the daughter grows back, so frame 0 is
      // 10's field at its own scale (k = 1) and by T 28.5 the six cells with a fate have landed
      const k = s / WIDE;
      const fate = E.inOutCubic(clamp((t - B_PUSH) / (B_G5 - B_PUSH))); // T 26.0 to 28.5
      // 10's pressed contact faces relax back to round as the frame tightens on the hero
      const press = 1 - sstep(B_PUSH, B_G4, t);

      const onScreen = (wx, wy, wr) => {
        const x = 540 + (wx - 540) * zoom, y = 960 + (wy - camY) * zoom, r = wr * zoom;
        return x + r > -30 && x - r < 1110 && y + r > -30 && y - r < 1950;
      };
      const lodOf = (sr) => (sr < 55 ? 0 : sr < 130 ? 1 : sr < 240 ? 2 : 3);
      // 10's line weights: ws = zoom^-0.75, so a width reads at w * k^0.25 screen px while the
      // camera is wide and lands on exactly w — the art bible's weight — once the push-in is home
      const pxOf = (kk) => (w) => w * Math.pow(kk, -0.75);
      const px = pxOf(kH);

      // where a tissue cell sits now: 10's place carried out by the expansion, plus its fate
      const cellPos = (c) => {
        let x = CX + k * (c.x0 - CX), y = CY + k * (c.y0 - CY);
        if (c.push) {
          x += c.push[0] * fate;
          y += c.push[1] * fate;
        }
        return [x, y, c.R * k];
      };

      // ---- 3 the world under the camera --------------------------------------------------
      L.camera(ctx, { x: 540, y: camY, zoom }, (ctx) => {
        // the tissue: 10's 24 cells, farthest from the hero first, as 10 draws them
        const hard = [[CX, CY, R_CELL * s], [sibX, sibY, R_CELL * s]];
        for (const c of g.cells) {
          const pos = cellPos(c);
          const f = c.fate;
          const split = f && f.split != null && t >= f.split - 1e-6;
          if (!split) {
            if (!onScreen(pos[0], pos[1], pos[2] * 1.2)) continue;
            const sr = pos[2] * zoom;
            const lod = lodOf(sr);
            // a dividing cell that will part deepens its furrow first
            let stage = c.stage0, pinchF = c.stage0 && PINCH[c.stage0] ? PINCH[c.stage0] : null;
            if (f && f.split != null) {
              const u = clamp((t - f.at) / (f.split - f.at));
              const a0 = PINCH[f.from], a1 = PINCH.pinchLate;
              stage = t >= f.at ? 'pinch' : c.stage0;
              if (t >= f.at) pinchF = [lerp(a0[0], a1[0], u), lerp(a0[1], a1[1], u), lerp(a0[2], a1[2], u)];
            }
            const st = {
              cx: pos[0], cy: pos[1], R: pos[2], bi, lod, px, seed: c.seed,
              nucA: c.nucA, nucF: c.nucF, chrRot: c.chrRot, chrA: nChr,
              mito: c.mito, mitoPinch: c.mitoPinch, axis: c.axis, pinchF,
              press,
              soft: c.soft.map((o) => {
                const q = cellPos(o);
                return [q[0], q[1], q[2]];
              }),
              hard,
            };
            ctx.save();
            ctx.globalAlpha *= 0.72; // neighbours sit at 70 percent (G1)
            if (stage === 'spindle') paintSpindleCell(ctx, L, P, st);
            else if (stage === 'pinch' || stage === 'pinchEarly' || stage === 'pinchMid' || stage === 'pinchLate') {
              st.pinchF = pinchF || PINCH.pinchMid;
              paintPinchCell(ctx, L, P, st);
            } else paintInterphaseCell(ctx, L, P, st);
            ctx.restore();
            continue;
          }
          // the cell has parted: its two daughters, each on its own way. The one that takes a
          // place in 01's plate drifts onto it and grows to its radius; the other keeps spreading.
          const lp = PINCH.pinchLate;
          const ca = Math.cos(c.axis), sa = Math.sin(c.axis);
          const partU = E.outBack(clamp((t - f.split) / (10 * FR)));
          const off = pos[2] * lp[2] + 0.55 * pos[2] * partU; // the pair pushes apart as it seals
          const lobeR = pos[2] * lp[1];
          const drift = E.inOutCubic(clamp((t - f.split) / (B_G5 - f.split)));
          for (const sg of [-1, 1]) {
            let lx = pos[0] + ca * sg * off, ly = pos[1] + sa * sg * off, lr = lobeR;
            const slot = sg === f.lobe ? c.slot : sg === f.lobe2 ? c.slot2 : null;
            if (slot) {
              lx = lerp(lx, slot.x, drift);
              ly = lerp(ly, slot.y, drift);
              lr = lerp(lr, slot.r, drift);
            }
            if (!onScreen(lx, ly, lr * 1.2)) continue;
            const lod = lodOf(lr * zoom);
            ctx.save();
            ctx.globalAlpha *= 0.72;
            paintInterphaseCell(ctx, L, P, {
              cx: lx, cy: ly, R: lr, bi, lod, px, seed: c.seed + (sg > 0 ? 311 : 617),
              nucA: c.nucA + (sg > 0 ? 0.9 : -0.9), nucF: c.nucF, chrRot: c.chrRot + sg * 1.1,
              chrA: nChr, mito: c.mito, press: 0, soft: [], hard,
            });
            ctx.restore();
          }
        }

        // the sibling daughter: identical to the hero, same size and the same four chromosomes
        if (onScreen(sibX, sibY, R_CELL * s * 1.1)) {
          ctx.save();
          ctx.translate(sibX, sibY);
          ctx.scale(s, s);
          ctx.translate(-CX, -CY);
          drawHeroCell(ctx, L, P, g, {
            k: kH, bi, alpha: 1, seedOff: 977, rel, stip, nucleolus, mito: mitoProg, cons: 0,
            lod: lodOf(R_CELL * s * zoom), mig, mitoFrom: MITO_SIB,
          });
          ctx.restore();
        }

        // the hero: the lower daughter, which lands exactly on G1
        ctx.save();
        ctx.translate(CX, CY);
        ctx.scale(s, s);
        ctx.translate(-CX, -CY);
        drawHeroCell(ctx, L, P, g, {
          k: kH, bi, alpha: 1, seedOff: 0, rel, stip, nucleolus, mito: mitoProg, cons,
          lod: lodOf(R_CELL * s * zoom), mig, mitoFrom: MITO_HERO,
        });
        ctx.restore();
      });

      // ---- 4 overlays, screen-fixed ------------------------------------------------------
      // 10's two remaining overlays, carried across the cut and lifted over the first beat: the
      // tally ring showing two, and the annBlue corner frame round the pair
      const outg = 1 - clamp((t - B_PUSH) / (8 * FR));
      if (outg > 0.01) {
        ctx.save();
        ctx.globalAlpha = outg;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        // the tally: a ring at (180, 300) with two ticks, over an ink underlay so it reads on tissue
        const tally = new Path2D();
        tally.moveTo(180 + 46, 300);
        tally.arc(180, 300, 46, 0, TAU);
        for (const dd of [-15 * DEG, 15 * DEG]) {
          const a = -Math.PI / 2 + dd;
          const c = Math.cos(a), sn = Math.sin(a);
          tally.moveTo(180 + c * (46 - 7), 300 + sn * (46 - 7));
          tally.lineTo(180 + c * (46 + 19), 300 + sn * (46 + 19));
        }
        ctx.strokeStyle = P.ink;
        ctx.globalAlpha = outg * 0.22;
        ctx.lineWidth = 6.5;
        ctx.stroke(tally);
        ctx.strokeStyle = P.annYellow;
        ctx.globalAlpha = outg;
        ctx.lineWidth = 2.6;
        ctx.stroke(tally);
        // the corner frame: 10's box round the pair, on the same world points
        const sc = (x, y) => [540 + (x - 540) * zoom, 960 + (y - camY) * zoom];
        const A = sc(CX - R_CELL * s - 30, sibY - R_CELL * s - 40);
        const B = sc(CX + R_CELL * s + 30, CY + R_CELL * s + 40);
        const arm = 38;
        ctx.strokeStyle = P.annBlue;
        ctx.lineWidth = 2.5;
        const corner = (x, y, sx, sy) => {
          ctx.beginPath();
          ctx.moveTo(x, y + sy * arm);
          ctx.lineTo(x, y);
          ctx.lineTo(x + sx * arm, y);
          ctx.stroke();
        };
        corner(A[0], A[1], 1, 1);
        corner(B[0], A[1], -1, 1);
        corner(A[0], B[1], 1, -1);
        corner(B[0], B[1], -1, -1);
        ctx.setLineDash([9, 8]);
        ctx.lineWidth = 2;
        ctx.globalAlpha = outg * 0.7;
        ctx.beginPath();
        ctx.moveTo((A[0] + B[0]) / 2, A[1] + arm * 0.4);
        ctx.lineTo((A[0] + B[0]) / 2, A[1] + arm * 0.4 + 30);
        ctx.moveTo((A[0] + B[0]) / 2, B[1] - arm * 0.4);
        ctx.lineTo((A[0] + B[0]) / 2, B[1] - arm * 0.4 - 30);
        ctx.stroke();
        ctx.restore();
      }

      // the reticle: the annBlue pair of rings drops onto the hero over the push-in and lands on
      // 01's radius 400 and 440, with the origin dot at the foot of the outer ring
      const ret = sstep(0.9, 1.15, t);
      if (ret > 0.01) {
        const conv = E.inOutCubic(clamp((t - 0.9) / 1.35));
        const f = lerp(1.95, 1, conv);
        const r400 = 400 * kH * f, r440 = 440 * kH * f;
        ctx.save();
        ctx.globalAlpha = ret;
        ctx.lineCap = 'round';
        ctx.strokeStyle = P.annBlue;
        ctx.fillStyle = P.annBlue;
        ctx.lineWidth = 2.2;
        ctx.stroke(ringPath(hsx, hsy, r400, 0, 0));
        ctx.globalAlpha = ret * 0.72;
        ctx.lineWidth = 1.6;
        ctx.stroke(ringPath(hsx, hsy, r440, 0, 0));
        ctx.globalAlpha = ret;
        ctx.beginPath();
        ctx.arc(hsx, hsy + r440, 4.5, 0, TAU);
        ctx.fill();
        ctx.restore();
      }

      // the 90 degree annYellow arc with its tick scale over the top of the cell (01)
      const arc = sstep(B_G4, B_G4 + 0.25, t);
      if (arc > 0.01) {
        const R = 470 * kH;
        ctx.save();
        ctx.globalAlpha = arc;
        ctx.strokeStyle = P.annYellow;
        ctx.fillStyle = P.annYellow;
        ctx.lineWidth = 2.5;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.arc(hsx, hsy, R, -135 * DEG, -45 * DEG);
        ctx.stroke();
        const tk = new Path2D();
        for (let i = 0; i <= 16; i++) {
          const a = (-135 + (90 * i) / 16) * DEG;
          const len = i % 4 === 0 ? 18 : 10;
          tk.moveTo(hsx + Math.cos(a) * R, hsy + Math.sin(a) * R);
          tk.lineTo(hsx + Math.cos(a) * (R + len), hsy + Math.sin(a) * (R + len));
        }
        ctx.lineWidth = 2;
        ctx.stroke(tk);
        ctx.beginPath();
        ctx.arc(hsx, hsy - R, 4.5, 0, TAU);
        ctx.fill();
        ctx.restore();
      }

      // a beat ring on each growth step: the heartbeat under the push-in
      for (const b of GBEATS) {
        if (t < b || t > b + 5 * FR) continue;
        const u = hit(b, 4, E.outExpo);
        const a = 0.42 * (1 - clamp((t - b) / (5 * FR)));
        if (a <= 0.01) continue;
        ctx.save();
        ctx.globalAlpha = a;
        ctx.strokeStyle = P.annYellow;
        ctx.lineWidth = 2;
        ctx.lineCap = 'round';
        ctx.stroke(ringPath(hsx, hsy, (R_CELL * 1.03 + 90 * u) * kH, 0, 0));
        ctx.restore();
      }

      // T 29.5: the yellow ring pulses out of the nucleus, the burst 01 answers on its own beat
      if (t >= B_RING && t < B_RING + 8 * FR) {
        const u = hit(B_RING, 6, E.outExpo, 0); // starts on the nuclear membrane, on the beat frame
        const a = 1 - clamp((t - B_RING) / (8 * FR));
        const r = lerp(R_NUC, 520, u) * kH;
        ctx.save();
        ctx.lineCap = 'round';
        ctx.strokeStyle = P.ink;
        ctx.globalAlpha = a * 0.25;
        ctx.lineWidth = 6;
        ctx.stroke(ringPath(hsx, hsy, r, 0, 0));
        ctx.strokeStyle = P.annYellow;
        ctx.globalAlpha = a;
        ctx.lineWidth = 3;
        ctx.stroke(ringPath(hsx, hsy, r, 4, 18));
        ctx.restore();
      }

      // ---- 5 the wordmark, once in the film (art bible section 9) -------------------------
      const wm = clamp((t - B_G5) / (8 * FR));
      if (wm > 0.01) {
        L.text(ctx, 'studyvault', 540, 1470, {
          size: 44, weight: 300, color: P.inkSoft, alpha: 0.85 * wm,
          align: 'center', baseline: 'alphabetic', tracking: '0.12em',
        });
      }

      // ---- 6 the cycle glyph, last and never re-implemented -------------------------------
      L.cycleGlyph(ctx, info.T, 'illustrated');
    },
  });
})();
