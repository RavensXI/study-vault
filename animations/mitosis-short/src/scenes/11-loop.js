// 11 loop : "One daughter becomes the hero — the cycle loops" (illustrated, global T 25.5 to 30.0)
//
// Opens on 10's last frame: the wide tissue at zoom 0.45, the two G4 daughters among a field of
// neighbours. The camera pushes into the LOWER daughter over 72 frames from T 26.0 so that by
// T 29.0 it sits exactly on G1 at zoom 1 with 01's composition, held screen-fixed for the last
// 12 frames. The film loops out of this frame into 01's frame 0.
//
// World model (the one idea the whole file rests on):
//   The world IS 01's frame. The hero cell sits on G1 at (540, 900) with mean radius 380, and the
//   camera lands at { x: 540, y: 960, zoom: 1 }, which lib.camera renders as the identity, so world
//   pixels are frame pixels and every G1 number lands exactly where 01 draws it.
//   Every other cell is placed at  hero + scale(t) * (final - hero), with scale running from
//   WIDE = 300/380 (the G4 daughter: radius 300, nucleus 135) to 1 (G1: radius 380, nucleus 170) in
//   five beat steps. So the whole tissue expands about the hero as the daughter grows back, and the
//   opening frame is 10's pose: daughters 680 px apart (screen 807 and 1113), radius 135 on screen.
//   The sibling daughter is the one cell that also drifts: it accelerates off the top of the frame
//   from T 27.0, because 01's plate has five neighbours and no cell at top centre.
//
// Layers, back to front (frame px):
//   1 stripes, screen-fixed: stripeCream and stripeYellow, 140 px bands at -0.52, 12 px per second,
//     landing on offset 0 at T 30.0 so the loop seam does not jump
//   2 the tissue field under the camera: a seeded lattice of neighbour cells (cytoplasm neighbour,
//     nuclei neighbourNucleus, 72 percent), three of them mid-division and one running a miniature
//     spindle; the nearest furrow closes on T 26.5
//   3 the five G1 neighbours at (60,380) (1020,420) (40,1420) (1040,1400) (540,1690); the upper two
//     start a little further out and settle onto 01's exact positions by T 28.5
//   4 the hero's construction lines: the 45 degree diameters and the faint square, fading in T 27.0
//   5 the sibling daughter, drawn by the same painter as the hero (same size, same four chromosomes),
//     leaving the frame over the top
//   6 the hero cell: cytoplasm with cytoHatch rim hatching, ribosome stipple 0.20 to 0.35, six
//     mitochondria (three drawn in on the beats), the nucleus with its cross-hatch, nucleolus and
//     four chromosomes relaxing into the G1 worms, and the 6 px doubled ink membrane
//   7 overlays, screen-fixed: 10's nucleus arc and tally fading out on the first beat, the annBlue
//     reticle (r 400 with ticks to 440) and the annYellow 90 degree arc locking onto the hero, a beat
//     ring on each growth step, and the yellow burst from the nucleus on T 29.5
//   8 the wordmark 'studyvault' from T 28.5 (art bible section 9), then lib.cycleGlyph, last
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

  // camera: 10's last frame, then the identity
  const CAM_Y0 = CY - SIB_GAP / 2; // 560: the frame centre sits midway between the daughters
  const CAM_Y1 = 960; // world pixels are frame pixels
  const Z0 = 0.45, Z1 = 1;

  // the sibling's place in the expanding field, and how far it leaves over the top
  const SIB_F = [CX, CY - SIB_GAP / WIDE]; // (540, 38.7)
  const SIB_EXIT = -520;

  // G1 mitochondria: 6 beans, 60 by 28
  const MITO = [[300, 700], [760, 720], [280, 1060], [790, 1080], [420, 1190], [660, 640]];
  // the daughter keeps three at the cut; the other three draw in on the growth beats
  const MITO_AT = [-1, 1.5, 2.5, -1, -1, 2.0]; // shot-local beat, -1 = present from frame 0

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
    { x: 60, y: 380, r: 330, settle: [-86, 61] }, // settles in from up-left of the sibling
    { x: 1020, y: 420, r: 340, settle: [82, 65] },
    { x: 40, y: 1420, r: 320, settle: [0, 0] },
    { x: 1040, y: 1400, r: 350, settle: [0, 0] },
    { x: 540, y: 1690, r: 360, settle: [0, 0] },
  ];

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
      if (i > 0) s += Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]);
      const a = pts[i > 0 ? i - 1 : 0], b = pts[i < n - 1 ? i + 1 : n - 1];
      const tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
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
      const tl = Math.hypot(tx, ty) || 1;
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

  // the outline of a cell part way through cytokinesis: two lobes joined by a concave neck
  function pinchPts(R, neck, n, seed) {
    const rl = R * 0.63, d = R * 0.54;
    const nw = Math.max(0.5, R * neck);
    const H = d + rl;
    const right = [];
    for (let i = 0; i <= n; i++) {
      const y = -H + (2 * H * i) / n;
      const ay = Math.abs(y);
      let hw;
      if (ay >= d) hw = Math.sqrt(Math.max(0, rl * rl - (ay - d) * (ay - d)));
      else hw = nw + (rl - nw) * Math.pow(ay / d, 1.7);
      const w = 1 + 0.035 * LIB.noise1(y * 0.012, seed);
      right.push([hw * w, y]);
    }
    const left = [];
    for (let i = right.length - 1; i >= 0; i--) left.push([-right[i][0], right[i][1]]);
    return right.concat(left);
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

    // ---- the wide tissue field --------------------------------------------------------------
    // Cells are authored in final (frame) coordinates. At time t a cell sits at
    // hero + scale * (final - hero), so the field expands about the hero as the daughter grows.
    const cells = [];
    NEIGH.forEach((nb, i) => {
      cells.push({
        fx: nb.x, fy: nb.y, R: nb.r, seed: sdG1('neighbour', i), slot: true,
        dx0: nb.settle[0], dy0: nb.settle[1], stage: 'normal',
      });
    });

    const fixed = [[CX, CY, R_CELL], [SIB_F[0], SIB_F[1], R_CELL]];
    for (const nb of NEIGH) fixed.push([nb.x, nb.y, nb.r]);

    const inFinalFrame = (x, y, R) => x > -R - 30 && x < 1080 + R + 30 && y > -R - 30 && y < 1920 + R + 30;

    const SP = 985, ROW = SP * 0.866;
    const rr = L.rng(L.hash(REF10, 'tissue'));
    const lat = [];
    for (let j = -5; j <= 4; j++) {
      for (let i = -2; i <= 2; i++) {
        const fx = CX + i * SP + (j & 1 ? SP / 2 : 0) + rr.range(-125, 125);
        const fy = CY + j * ROW + rr.range(-110, 110);
        const R = rr.range(295, 445);
        if (inFinalFrame(fx, fy, R)) continue; // 01's frame holds the hero and its five neighbours only
        if (Math.hypot(fx - SIB_F[0], fy - SIB_F[1]) < R_CELL + R + 20) continue; // the sibling's place
        lat.push({ fx, fy, R });
      }
    }

    // relax: neighbours in tissue press against each other, they do not overlap
    for (let pass = 0; pass < 4; pass++) {
      for (const a of lat) {
        for (const f of fixed) {
          const dx = a.fx - f[0], dy = a.fy - f[1];
          const d = Math.hypot(dx, dy) || 1;
          const m = (a.R + f[2]) * 0.99;
          if (d < m) {
            a.fx += (dx / d) * (m - d);
            a.fy += (dy / d) * (m - d);
          }
        }
        for (const b of lat) {
          if (b === a) continue;
          const dx = a.fx - b.fx, dy = a.fy - b.fy;
          const d = Math.hypot(dx, dy) || 1;
          const m = (a.R + b.R) * 0.99; // packed like an epithelium, barely any paper between cells
          if (d < m) {
            const p = (m - d) * 0.5;
            a.fx += (dx / d) * p;
            a.fy += (dy / d) * p;
            b.fx -= (dx / d) * p;
            b.fy -= (dy / d) * p;
          }
        }
      }
    }

    // fill the holes the relaxation opened, so the wide frame reads as packed tissue
    const all = lat.slice();
    const clear = (x, y) => {
      let m = Infinity;
      for (const c of all) m = Math.min(m, Math.hypot(x - c.fx, y - c.fy) - c.R);
      for (const f of fixed) m = Math.min(m, Math.hypot(x - f[0], y - f[1]) - f[2]);
      return m;
    };
    const fr = L.rng(L.hash(REF10, 'fill'));
    for (let gy = CY - 3250; gy <= CY + 2400 && all.length < 46; gy += 300) {
      for (let gx = CX - 1620; gx <= CX + 1620 && all.length < 46; gx += 300) {
        const x = gx + fr.range(-80, 80), y = gy + fr.range(-80, 80);
        const room = clear(x, y);
        if (room < 265) continue;
        const R = clamp(room - 25, 290, 430);
        if (inFinalFrame(x, y, R)) continue;
        if (Math.hypot(x - SIB_F[0], y - SIB_F[1]) < R_CELL + R + 20) continue;
        all.push({ fx: x, fy: y, R });
      }
    }

    // drop anything the relaxation pushed back into 01's frame, then keep a stable order
    const keep = all.filter((c) => !inFinalFrame(c.fx, c.fy, c.R * 0.72));
    keep.sort((a, b) => a.fy - b.fy || a.fx - b.fx);
    keep.forEach((c, i) => {
      c.seed = sdT('cell', i);
      c.stage = 'normal';
      c.dx0 = 0;
      c.dy0 = 0;
      c.slot = false;
      cells.push(c);
    });

    // several neighbours are mid-division at different stages (art bible 10.6), chosen by how near
    // they sit to the centre of the opening frame so the viewer actually sees them
    const screen0 = (c) => {
      const wx = CX + WIDE * (c.fx - CX), wy = CY + WIDE * (c.fy - CY);
      return [540 + (wx - 540) * Z0, 960 + (wy - CAM_Y0) * Z0, c.R * WIDE * Z0];
    };
    const cand = keep
      .map((c) => {
        const s = screen0(c);
        return {
          c,
          d: Math.hypot(s[0] - 540, s[1] - 960),
          on: s[0] > -s[2] && s[0] < 1080 + s[2] && s[1] > -s[2] && s[1] < 1920 + s[2],
          // a cell wholly inside the opening frame shows its whole stage, so it is picked first
          full: s[0] - s[2] > 20 && s[0] + s[2] < 1060 && s[1] - s[2] > 40 && s[1] + s[2] < 1880,
        };
      })
      .filter((o) => o.on)
      .sort((a, b) => (a.full === b.full ? a.d - b.d : a.full ? -1 : 1));
    const tag = (rank, stage) => {
      if (cand[rank]) cand[rank].c.stage = stage;
    };
    tag(0, 'pinch-close'); // this one's furrow closes on the beat at T 26.5
    tag(1, 'spindle');
    tag(3, 'pinch');
    tag(6, 'pinch');
    for (const c of cells) {
      const h = c.seed & 0xffff;
      c.tilt = (L.h3(h, 5, 31) - 0.5) * TAU;
      c.nucF = 0.34 + 0.15 * L.h3(h, 9, 17);
      c.nucOff = [(L.h3(h, 11, 23) - 0.5) * 0.24, (L.h3(h, 13, 29) - 0.5) * 0.24];
      c.mitoN = 3 + Math.floor(L.h3(h, 17, 37) * 4);
      // every nucleus turns its own way, or a field of cells reads as a field of faces
      c.chrRot = L.h3(h, 19, 41) * TAU;
      c.chrFlip = L.h3(h, 23, 43) < 0.5 ? -1 : 1;
      // cells pressed together are not round: a seeded squash along the cell's own axis
      c.squash = 1 + 0.16 * (L.h3(h, 29, 47) - 0.5);
    }
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
        const tl = Math.hypot(tx, ty) || 1;
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
    const px = (w) => w / o.k; // a width that renders at w screen pixels
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
        const d = Math.hypot(x - CX, y - CY) / R_CELL;
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
          const d = Math.hypot(x - CX, y - CY) / R_CELL;
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

    // 4 mitochondria, three of them drawing in on the growth beats
    for (let i = 0; i < H.mito.length; i++) drawMito(ctx, L, P, H.mito[i], o.mito[i], px, bi, A);

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

  // One neighbour cell, drawn in its own final-size local coordinates about (0, 0).
  function drawTissueCell(ctx, L, P, c, o) {
    const px = (w) => w / o.k;
    const bi = o.bi, lod = o.lod, R = c.R;
    const A = 1; // the caller has already set the neighbour's 72 percent

    if (c.stage === 'split') {
      // the furrow closed on the beat: two fresh cells, still touching, each with its own nucleus
      const lr = R * 0.63;
      for (const sgn of [-1, 1]) {
        const d = (R * 0.54 + o.gap) * sgn;
        const dx = -Math.sin(c.tilt) * d, dy = Math.cos(c.tilt) * d;
        const pts = blobPts(0, 0, lr, 12, 26, c.seed + (sgn > 0 ? 7 : 3));
        ctx.save();
        ctx.translate(dx, dy);
        const body = new Path2D();
        wob(L, body, pts, c.seed + sgn + 2, 2, bi, true);
        fillPath(ctx, body, P.neighbour, 1.22);
        if (lod >= 1) {
          const sh = new Path2D();
          crescent(sh, lr, px(9), c.seed + 13, bi, 0.85);
          ctx.save();
          ctx.clip(body);
          stroke(ctx, sh, P.cytoHatch, 0.75, px(1.5));
          ctx.restore();
        }
        const nr = lr * 0.44;
        const np = blobPts(0, 0, nr, 5, 18, c.seed + 21 + sgn);
        const nucP = new Path2D();
        wob(L, nucP, np, c.seed + 5 + sgn, 1.2, bi, true);
        fillPath(ctx, nucP, P.neighbourNucleus, A);
        if (lod >= 1 && o.chrA > 0.02) neighbourChromo(ctx, L, P, nr, px, bi, c.seed + 41 + sgn, lod, 0.9 * o.chrA, c.chrRot + sgn * 1.1, c.chrFlip);
        stroke(ctx, nucP, P.nucleusRim, 0.8, px(2.2));
        stroke(ctx, body, P.ink, 0.95, px(3));
        ctx.restore();
      }
      return;
    }

    // ---- outline -------------------------------------------------------------------------
    let pts;
    if (c.stage === 'pinch' || c.stage === 'pinch-close') {
      pts = pinchPts(R, o.neck, 34, c.seed);
      const ca = Math.cos(c.tilt), sa = Math.sin(c.tilt);
      pts = pts.map((p) => [p[0] * ca - p[1] * sa, p[0] * sa + p[1] * ca]);
    } else {
      // cells packed in tissue are not round: each takes a seeded squash along its own axis
      const ca = Math.cos(c.tilt), sa = Math.sin(c.tilt);
      const sx = c.stage === 'spindle' ? 0.84 : c.squash;
      const sy = c.stage === 'spindle' ? 1.2 : 2 - c.squash;
      pts = blobPts(0, 0, R, 24, 26, c.seed).map((p) => {
        const x = p[0] * sx, y = p[1] * sy;
        return [x * ca - y * sa, x * sa + y * ca];
      });
    }
    const body = new Path2D();
    wob(L, body, pts, c.seed + 1, 2.2, bi, true);
    // the cytoplasm is the one part drawn nearer to solid (0.88), so cells overlapping in the field
    // do not read as ghost rings through each other; every line and detail keeps the 72 percent
    fillPath(ctx, body, P.neighbour, 1.22);

    // ---- tone ----------------------------------------------------------------------------
    if (lod >= 1) {
      const sh = new Path2D();
      crescent(sh, R, px(9.5), c.seed + 13, bi, lod >= 2 ? 1 : 0.8);
      ctx.save();
      ctx.clip(body);
      stroke(ctx, sh, P.cytoHatch, 0.8, px(1.5));
      if (lod >= 2) {
        // deep shade takes a second layer at 105 degrees (art bible 4.1)
        const cross = new Path2D();
        crescent(cross, R * 0.99, px(13), c.seed + 17, bi, 0.55);
        ctx.save();
        ctx.rotate(-Math.PI / 3);
        stroke(ctx, cross, P.cytoHatch, 0.6, px(1.3));
        ctx.restore();
      }
      ctx.restore();
    }
    if (lod >= 3) {
      L.stipple(ctx, pts, {
        spacing: px(11),
        r: [px(1.0), px(1.9)],
        color: P.ribosome,
        alpha: 0.45,
        seed: c.seed + 61,
        density: 0.55,
      });
    }

    // ---- inside --------------------------------------------------------------------------
    if (c.stage === 'spindle') {
      // a miniature metaphase: two poles, four X chromosomes on the plate, fibres between
      const ca = Math.cos(c.tilt), sa = Math.sin(c.tilt);
      const rot = (x, y) => [x * ca - y * sa, x * sa + y * ca];
      const poles = [rot(0, -R * 0.95), rot(0, R * 0.95)];
      const fib = new Path2D();
      const xs = [-0.42, -0.15, 0.15, 0.42];
      const cent = xs.map((u) => rot(u * R * 0.8, 0));
      for (const p of poles) {
        for (const q of cent) {
          fib.moveTo(p[0], p[1]);
          fib.quadraticCurveTo((p[0] + q[0]) / 2 + (L.h3(q[0] | 0, bi, c.seed) - 0.5) * 12, (p[1] + q[1]) / 2, q[0], q[1]);
        }
        for (let i = 0; i < 4; i++) {
          const a = (i / 3 - 0.5) * 1.1;
          const e = rot(Math.sin(a) * R * 0.75, (p === poles[0] ? 1 : -1) * R * 0.2);
          fib.moveTo(p[0], p[1]);
          fib.lineTo(e[0], e[1]);
        }
      }
      stroke(ctx, fib, P.fibre, 0.75, px(1.6));
      for (const p of poles) {
        const d = new Path2D();
        d.arc(p[0], p[1], R * 0.07, 0, TAU);
        fillPath(ctx, d, P.pole, 0.95);
        stroke(ctx, d, P.ink, 0.8, px(1.6));
      }
      // the plate itself, a faint line the four sit on
      const plate = new Path2D();
      const pa = rot(-R * 0.62, 0), pb = rot(R * 0.62, 0);
      plate.moveTo(pa[0], pa[1]);
      plate.lineTo(pb[0], pb[1]);
      stroke(ctx, plate, P.inkFaint, 0.4, px(1.2), [px(7), px(7)]);
      // two pairs: the long blue pair outside, the short rust pair inside, each an X of two copies
      const kinds = ['A', 'B', 'B', 'A'];
      for (let i = 0; i < 4; i++) {
        const q = cent[i];
        const h = (kinds[i] === 'A' ? 0.115 : 0.082) * R;
        const xp = new Path2D();
        for (const s2 of [-1, 1]) {
          const a1 = rot(xs[i] * R * 0.8 - s2 * h * 0.42, -h), a2 = rot(xs[i] * R * 0.8 + s2 * h * 0.42, h);
          xp.moveTo(a1[0], a1[1]);
          xp.lineTo(a2[0], a2[1]);
        }
        stroke(ctx, xp, kinds[i] === 'A' ? P.chromoA : P.chromoB, 0.95, Math.max(px(2.6), R * 0.034));
        const dot = new Path2D();
        dot.arc(q[0], q[1], Math.max(px(2.6), R * 0.022), 0, TAU);
        fillPath(ctx, dot, P.centromere, 0.9);
      }
    } else if (c.stage === 'pinch' || c.stage === 'pinch-close') {
      const ca = Math.cos(c.tilt), sa = Math.sin(c.tilt);
      for (const sgn of [-1, 1]) {
        const d = R * 0.54 * sgn;
        const dx = -sa * d, dy = ca * d;
        const nr = R * 0.63 * 0.44;
        const np = blobPts(dx, dy, nr, 5, 18, c.seed + 21 + sgn);
        const nucP = new Path2D();
        wob(L, nucP, np, c.seed + 5 + sgn, 1.2, bi, true);
        fillPath(ctx, nucP, P.neighbourNucleus, A);
        if (lod >= 1 && o.chrA > 0.02) {
          ctx.save();
          ctx.translate(dx, dy);
          neighbourChromo(ctx, L, P, nr, px, bi, c.seed + 41 + sgn, lod, 0.9 * o.chrA, c.chrRot + sgn * 1.1, c.chrFlip);
          ctx.restore();
        }
        stroke(ctx, nucP, P.nucleusRim, 0.8, px(2.2));
      }
      // the furrow: a pair of arcs pulling the outline in
      const fur = new Path2D();
      for (const s2 of [-1, 1]) {
        const w = Math.max(1, R * o.neck);
        const a0 = [(-sa * 0) + ca * w * s2, (ca * 0) + sa * w * s2];
        fur.moveTo(a0[0] - (-sa) * R * 0.2, a0[1] - ca * R * 0.2);
        fur.quadraticCurveTo(a0[0] + ca * 6 * s2, a0[1] + sa * 6 * s2, a0[0] + (-sa) * R * 0.2, a0[1] + ca * R * 0.2);
      }
      stroke(ctx, fur, P.inkSoft, 0.5, px(1.6));
    } else {
      const nr = R * c.nucF;
      const nx = c.nucOff[0] * R, ny = c.nucOff[1] * R;
      const np = blobPts(nx, ny, nr, 8, 20, c.seed + 21);
      const nucP = new Path2D();
      wob(L, nucP, np, c.seed + 5, 1.4, bi, true);
      fillPath(ctx, nucP, P.neighbourNucleus, A);
      if (lod >= 2) {
        L.crossHatch(ctx, np, {
          angle: -Math.PI / 4, spacing: px(9), width: px(1.2), color: P.nucleusDeep,
          alpha: 0.5, layers: 2, length: [px(10), px(26)], gap: [px(3), px(7)], inset: px(3),
          clip: true, seed: c.seed + 71,
          density: (x, y) => sstep(0.1, 1.1, (nx - x + (y - ny)) / (nr * 1.414)),
        });
      } else if (lod >= 1) {
        // the cheap version of the same shadow: a crescent along the nucleus's lower left
        const sh = new Path2D();
        crescent(sh, nr, px(7), c.seed + 71, bi, 0.9);
        ctx.save();
        ctx.translate(nx, ny);
        ctx.rotate(Math.PI / 2);
        ctx.save();
        ctx.beginPath();
        ctx.arc(0, 0, nr * 0.94, 0, TAU);
        ctx.clip();
        stroke(ctx, sh, P.nucleusDeep, 0.5, px(1.2));
        ctx.restore();
        ctx.restore();
      }
      if (lod >= 1 && o.chrA > 0.02) {
        ctx.save();
        ctx.translate(nx, ny);
        neighbourChromo(ctx, L, P, nr, px, bi, c.seed + 41, lod, 0.92 * o.chrA, c.chrRot, c.chrFlip);
        ctx.restore();
      }
      stroke(ctx, nucP, P.nucleusRim, 0.85, px(2.4));
      // a nucleolus: the denser disc every nucleus holds
      if (lod >= 1) {
        const ol = new Path2D();
        const ox = nx - nr * 0.3, oy = ny - nr * 0.18;
        ol.arc(ox, oy, nr * 0.22, 0, TAU);
        fillPath(ctx, ol, P.nucleusDeep, 0.6);
      }
    }

    // ---- mitochondria --------------------------------------------------------------------
    if (lod >= 1 && c.stage !== 'spindle') {
      const n = lod >= 2 ? c.mitoN : Math.min(3, c.mitoN);
      for (let i = 0; i < n; i++) {
        const a = (i / n) * TAU + c.tilt * 1.7;
        const rr = R * (0.66 + 0.14 * L.h3(i, 3, c.seed));
        const m = { x: Math.cos(a) * rr, y: Math.sin(a) * rr, a: a + Math.PI / 2, seed: c.seed + 101 + i };
        const sc = (R / R_CELL) * 0.9;
        ctx.save();
        ctx.translate(m.x, m.y);
        ctx.scale(sc, sc);
        drawMito(ctx, L, P, { x: 0, y: 0, a: m.a, seed: m.seed }, lod >= 2 ? 1 : 0.9, (w) => w / (o.k * sc), bi, 1, lod < 2);
        ctx.restore();
      }
    }

    // ---- membrane ------------------------------------------------------------------------
    if (lod >= 2) {
      L.inkPath(ctx, pts, {
        closed: true, width: px(3.2), color: P.ink, alpha: 0.95,
        seed: c.seed + 7, wobble: 1.6, step: 3.4,
      });
    } else {
      stroke(ctx, body, P.ink, 0.95, px(3));
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
      // ribosomes thicken as the cell grows; the nucleolus reforms
      const stip = lerp(0.2, 0.35, grow);
      const nucleolus = sstep(B_G3, B_G5 - 0.25, tw);
      // three mitochondria are there from the cut, three draw in on the beats
      const mitoProg = MITO_AT.map((a, i) =>
        a < 0 ? 1 : tw < a ? 0 : E.outBack(clamp((tw - a) / (4 * FR) + 0.25)) * (0.55 + 0.45 * clamp((tw - a) / (4 * FR) + 0.25))
      );
      // construction lines fade in behind the hero
      const cons = sstep(B_G2, B_G4, t);

      // the sibling daughter: the same cell, leaving over the top of the frame from T 27.0
      const sibLeave = E.inOutCubic(clamp((t - B_G2) / (B_G5 - B_G2)));
      const sibX = CX + s * (SIB_F[0] - CX);
      const sibY = CY + s * (SIB_F[1] - CY) + SIB_EXIT * sibLeave;

      // the two upper neighbours settle the last 100 px onto 01's exact positions
      const settle = 1 - E.inOutCubic(clamp((t - B_G1) / (B_G5 - B_G1)));
      // 01's neighbours hold a plain nucleus with its nucleolus, so the field's chromosomes ease
      // away as the hero takes the frame and the loop hands over cleanly
      const nChr = 1 - sstep(2.2, 3.2, t);

      const onScreen = (wx, wy, wr) => {
        const x = 540 + (wx - 540) * zoom, y = 960 + (wy - camY) * zoom, r = wr * zoom;
        return x + r > -30 && x - r < 1110 && y + r > -30 && y - r < 1950;
      };
      const lodOf = (sr) => (sr < 55 ? 0 : sr < 130 ? 1 : sr < 240 ? 2 : 3);

      // ---- 3 the world under the camera --------------------------------------------------
      L.camera(ctx, { x: 540, y: camY, zoom }, (ctx) => {
        // the tissue field, top to bottom so lower cells overlap the ones behind them
        for (const c of g.cells) {
          const fx = c.fx + c.dx0 * settle, fy = c.fy + c.dy0 * settle;
          const wx = CX + s * (fx - CX), wy = CY + s * (fy - CY);
          const wr = c.R * s;
          if (!onScreen(wx, wy, wr * 1.25)) continue;
          const sr = wr * zoom;
          // the nearest furrow closes on the beat at T 26.5 and the two cells part
          let stage = c.stage, neck = 0.34, gap = 0;
          if (stage === 'pinch-close') {
            if (tw < B_G1) {
              neck = lerp(0.3, 0.06, clamp((tw - 0.25) / (B_G1 - 0.25)));
              stage = 'pinch';
            } else {
              stage = 'split';
              gap = 10 * popTwos(B_G1);
            }
          } else if (stage === 'pinch') {
            neck = 0.2 + 0.16 * L.h3(c.seed & 0xffff, 3, 7);
          }
          ctx.save();
          ctx.globalAlpha *= 0.72; // neighbours sit at 70 percent (G1)
          ctx.translate(wx, wy);
          ctx.scale(s, s);
          drawTissueCell(ctx, L, P, Object.assign({}, c, { stage }), {
            k: kH, bi, lod: lodOf(sr), neck, gap, chrA: nChr,
          });
          ctx.restore();
        }

        // the sibling daughter: identical to the hero, same size and the same four chromosomes
        if (onScreen(sibX, sibY, R_CELL * s * 1.1)) {
          ctx.save();
          ctx.translate(sibX, sibY);
          ctx.scale(s, s);
          ctx.translate(-CX, -CY);
          drawHeroCell(ctx, L, P, g, {
            k: kH, bi, alpha: 1, seedOff: 977, rel, stip, nucleolus, mito: mitoProg, cons: 0,
            lod: lodOf(R_CELL * s * zoom),
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
          lod: lodOf(R_CELL * s * zoom),
        });
        ctx.restore();
      });

      // ---- 4 overlays, screen-fixed ------------------------------------------------------
      // 10's pair overlays, held for one beat then lifted over 6 frames
      const outg = 1 - clamp((t - B_PUSH) / (6 * FR));
      if (outg > 0.01) {
        const sy2 = 960 + (sibY - camY) * zoom;
        ctx.save();
        ctx.globalAlpha = outg;
        ctx.strokeStyle = P.annBlue;
        ctx.fillStyle = P.annBlue;
        ctx.lineWidth = 2.5;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(hsx, hsy);
        ctx.quadraticCurveTo(hsx + 170 * zoom * 2, (hsy + sy2) / 2, hsx, sy2);
        ctx.stroke();
        for (const yy of [hsy, sy2]) {
          ctx.beginPath();
          ctx.arc(hsx, yy, 5, 0, TAU);
          ctx.fill();
        }
        // the tally that flipped 1 to 2 in shot 10
        ctx.strokeStyle = P.annYellow;
        ctx.fillStyle = P.annYellow;
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.arc(180, 300, 44, 0, TAU);
        ctx.stroke();
        ctx.beginPath();
        for (const dx of [-12, 12]) {
          ctx.moveTo(180 + dx, 282);
          ctx.lineTo(180 + dx, 318);
        }
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
