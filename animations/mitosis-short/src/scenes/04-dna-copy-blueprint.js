// 04 dna-copy-blueprint : The DNA is copied (schematic, T 7.0 to 9.5).
//
// The grown nucleus (G1: centre 540,900, radius 185) holds the four chromosomes as lattice worms.
// The camera pushes 6x into chromoA1 and turns it upright, where it resolves into a double helix:
// two strands with base-pair rungs. The helix unzips from the top, a new strand is built along each
// old strand (magenta while it draws, settling to lavender behind), rungs re-pair, and two identical
// double helices lie side by side, still joined at the centromere. The camera pulls back and each
// chromosome pops into an X on G2, one per 16th, while its tick under the nucleus splits into two.
//
// Layers, back to front (frame px at zoom 1):
//   0  plate        navy blueprint ground, screen-fixed and cached
//   1  grid         60 px world grid under the camera, two levels so it densifies on the push
//   2  guides       guide circles r 200 / 240 / 470 / 640, dial ticks, construction axes  (camera)
//   3  cell         grown cell outline r 440, 12 mitochondria, ribosome stipple           (camera, wide)
//   4  nucleus      lattice disc r 185, double rim, pores, nucleolus                      (camera)
//   5  chromatin    fibre loops; a near field of loose fibre only at high zoom            (camera)
//   6  chromosomes  four bodies: worm -> doubled worm -> X on G2                          (camera)
//   7  helix        chromoA1 at 6x: strands, rungs, the unzip and the new strands         (camera)
//   8  screen       reticle, push frame, brackets, base-pair rule, two insets,
//                   the node rail whose ticks go one -> two                               (screen-fixed)
//   9  glyph        FILM.lib.cycleGlyph at (900, 300), copy sector lighting               (screen-fixed)
//
// Nothing here is written: a schematic shot carries no text (art bible 5).
(function () {
  'use strict';

  const FILM = window.FILM;
  const L = FILM.lib;
  const P = L.pal;
  const E = L.ease;
  const TAU = Math.PI * 2;
  const DEG = Math.PI / 180;
  const FR = 1 / 24;
  const ID = 'dna-copy-blueprint';
  const REF = 'hero-cell'; // shapes that carry over from 01 / 03 seed from that shot
  const SEED = L.hash(ID);
  const sd = (...k) => L.hash(ID, ...k) & 0x7fffffff;

  const clamp = L.clamp;
  const lerp = L.lerp;
  const sstep = L.smoothstep;
  const boilNow = () => L.boil(L.T);

  // ---------------------------------------------------------------------------
  // Colours (hoisted once: pal is a read-only proxy)
  // ---------------------------------------------------------------------------
  const C = {
    navy: P.navy,
    navyDeep: P.navyDeep,
    navyLight: P.navyLight,
    grid: P.grid,
    lav: P.lavender,
    white: P.lineWhite,
    glow: P.glow,
    mag: P.magenta,
    blue: P.schemBlue, // pair A identity, thin lines only
    rust: P.schemRust, // pair B identity, thin lines only
  };

  // ---------------------------------------------------------------------------
  // Timing. t is shot-local seconds; the global time is t + 7.0.
  // ---------------------------------------------------------------------------
  const T_PUSH0 = 0.25; // T 7.250  push-in begins, 12 frames
  const T_PUSH1 = 0.75; // T 7.750  zoom 6 reached
  const T_UNZ0 = 0.75; // T 7.750  the rungs split, 8 frames
  const T_UNZ1 = 0.75 + 8 * FR; // T 8.083
  const T_NEW0 = 1.0; // T 8.000  new strands draw on, 12 frames
  const T_NEW1 = 1.5; // T 8.500  two double helices
  const T_PULL0 = 1.5; // T 8.500  pull back, 12 frames
  const T_PULL1 = 2.0; // T 9.000  zoom 1, screen-fixed from here
  const T_SWP0 = 1.0; // the other three chromosomes copy over the same window
  const T_SWP1 = 1.75;
  const POPS = [2.0, 2.125, 2.25, 2.375]; // A1, A2, B1, B2 on 16ths (T 9.0 .. 9.375)

  // drawings since a beat (12 fps), and a beat event that is visible ON its own frame
  const drawingAt = (t, a) => Math.floor((t - a) * 12 + 1e-6);
  const hit = (t, a, frames, e, lead) => {
    if (t < a) return 0;
    const u = clamp((t - a) / (frames * FR) + (lead == null ? 1 : lead) / frames);
    return (e || ((v) => v))(u);
  };

  // ---------------------------------------------------------------------------
  // Shared geometry (storyboard G1, G2, G5) — copied exactly
  // ---------------------------------------------------------------------------
  const NUC = { x: 540, y: 900, r: 185 }; // radius 185 after the growth of shot 03
  const CELL_R = 440; // the cell's mean radius at the end of 03
  const PHI = 11.15 * DEG; // chromatid splay: 2*75*sin(PHI) + 11 = 40 px, the X's width
  const BOW = 3; // outward bow of each arm, mid-arm

  const CHR = [
    { key: 'A1', cx: 470, cy: 850, len: 130, xh: 150, w: 16, rod: 11, sep: 13, amp: 9, lean: 20 * DEG, worm: 20 * DEG, tint: C.blue, tintW: 2.2, pop: POPS[0], node: 0, m: 420 },
    { key: 'A2', cx: 610, cy: 850, len: 130, xh: 150, w: 16, rod: 11, sep: 13, amp: 9, lean: -20 * DEG, worm: -20 * DEG, tint: C.blue, tintW: 2.2, pop: POPS[1], node: 3, m: 132 },
    { key: 'B1', cx: 480, cy: 955, len: 85, xh: 100, w: 13, rod: 9, sep: 10, amp: 6, lean: 20 * DEG, worm: 20 * DEG, tint: C.rust, tintW: 1.8, pop: POPS[2], node: 1, m: 108 },
    { key: 'B2', cx: 600, cy: 955, len: 85, xh: 100, w: 13, rod: 9, sep: 10, amp: 6, lean: -20 * DEG, worm: -20 * DEG, tint: C.rust, tintW: 1.8, pop: POPS[3], node: 2, m: 108 },
  ];

  // the nucleolus keeps its G1 place, drawn faint and dropped once the push passes it
  const NUCLEOLUS = { x: 500, y: 870, r: 20 };

  // mitochondria: the six of G1 plus the six that drew in through shot 03
  const MITO = [
    [300, 700], [760, 720], [280, 1060], [790, 1080], [420, 1190], [660, 640],
    [360, 560], [720, 1240], [240, 900], [840, 900], [500, 1240], [620, 560],
  ];

  // the node rail: one station per chromosome, ordered left to right by the chromosome's x
  const NODE_Y = 1420;
  const NODE_R = 50;
  const NODES = [
    { x: 240, y: NODE_Y, chr: 0 }, // A1
    { x: 440, y: NODE_Y, chr: 2 }, // B1
    { x: 640, y: NODE_Y, chr: 3 }, // B2
    { x: 840, y: NODE_Y, chr: 1 }, // A2
  ];

  // screen-fixed apparatus of the zoomed phase
  const INSET = { x: 320, y: 1340, r: 118 }; // base pairs, magnified again
  const SECT = { x: 790, y: 1160, r: 86 }; // the helix seen end-on: one becomes two
  const RULE_X = 120; // base-pair rule down the left edge
  const BRK_X = 900; // measurement bracket, as the storyboard places it

  // ---------------------------------------------------------------------------
  // Camera: push 6x into chromoA1 and turn its long axis upright, then pull back.
  // The G2 pose (t >= T_PULL1) is exactly the identity transform, so 05 match-cuts onto it.
  // ---------------------------------------------------------------------------
  const HOME = [540, 960];
  const TARGET = [CHR[0].cx, CHR[0].cy];
  const ZOOM = 6;
  const ROT = 70 * DEG; // 20 deg off horizontal + 70 = straight down the tall frame

  function camAt(t) {
    let e = 0;
    if (t > T_PUSH0 && t < T_PULL1) {
      if (t < T_PUSH1) e = E.inOutCubic((t - T_PUSH0) / (T_PUSH1 - T_PUSH0));
      else if (t < T_PULL0) e = 1;
      else e = 1 - E.inOutCubic((t - T_PULL0) / (T_PULL1 - T_PULL0));
    }
    if (e <= 0) return { x: HOME[0], y: HOME[1], zoom: 1, rot: 0, e: 0 };
    return {
      x: lerp(HOME[0], TARGET[0], e),
      y: lerp(HOME[1], TARGET[1], e),
      zoom: Math.pow(ZOOM, e),
      rot: ROT * e,
      e,
    };
  }

  function toScreen(cam, x, y) {
    const c = Math.cos(cam.rot), s = Math.sin(cam.rot);
    const dx = (x - cam.x) * cam.zoom, dy = (y - cam.y) * cam.zoom;
    return [540 + dx * c - dy * s, 960 + dx * s + dy * c];
  }

  function toWorld(cam, sx, sy) {
    const c = Math.cos(-cam.rot), s = Math.sin(-cam.rot);
    const dx = sx - 540, dy = sy - 960;
    return [cam.x + (dx * c - dy * s) / cam.zoom, cam.y + (dx * s + dy * c) / cam.zoom];
  }

  // world-space axis-aligned box the frame covers, for grid and culling
  function viewBox(cam) {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const [sx, sy] of [[0, 0], [1080, 0], [0, 1920], [1080, 1920]]) {
      const p = toWorld(cam, sx, sy);
      if (p[0] < x0) x0 = p[0];
      if (p[0] > x1) x1 = p[0];
      if (p[1] < y0) y0 = p[1];
      if (p[1] > y1) y1 = p[1];
    }
    return { x0, y0, x1, y1 };
  }

  // ---------------------------------------------------------------------------
  // Small drawing helpers
  // ---------------------------------------------------------------------------

  // a thin schematic polyline that boils on the 12 fps clock.
  // o.k scales width and wobble so a line drawn under the camera keeps its screen weight.
  function sline(ctx, pts, o) {
    if (!pts || pts.length < 2) return;
    o = o || {};
    const k = o.k || 1;
    const amp = (o.amp != null ? o.amp : 0.6) * k;
    const seed = (((o.seed | 0) + boilNow() * 131) | 0) & 0x7fffffff;
    ctx.save();
    ctx.globalAlpha *= o.alpha != null ? o.alpha : 1;
    ctx.strokeStyle = o.color || C.lav;
    ctx.lineWidth = (o.width || 1) * k;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    if (o.dash) ctx.setLineDash(o.dash.map((d) => d * k));
    ctx.beginPath();
    let s = 0;
    const n = pts.length;
    for (let i = 0; i < n; i++) {
      const p = pts[i];
      if (i > 0) s += Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]);
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      const dd = amp ? amp * L.noise1((s / k) * 0.02, seed) : 0;
      const x = p[0] - (ty / tl) * dd, y = p[1] + (tx / tl) * dd;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    if (o.closed) ctx.closePath();
    ctx.stroke();
    ctx.restore();
  }

  function dots(ctx, list, color, alpha) {
    if (!list.length) return;
    const p = new Path2D();
    for (const d of list) {
      p.moveTo(d[0] + d[2], d[1]);
      p.arc(d[0], d[1], d[2], 0, TAU);
    }
    ctx.save();
    ctx.globalAlpha *= alpha;
    ctx.fillStyle = color;
    ctx.fill(p);
    ctx.restore();
  }

  function arcPts(cx, cy, r, a0, a1, n) {
    const out = [];
    for (let i = 0; i <= n; i++) out.push([cx + Math.cos(lerp(a0, a1, i / n)) * r, cy + Math.sin(lerp(a0, a1, i / n)) * r]);
    return out;
  }

  function circlePts(cx, cy, r, n) {
    const out = [];
    for (let i = 0; i < n; i++) {
      const a = (i / n) * TAU;
      out.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
    }
    return out;
  }

  function cubicPts(p0, p1, p2, p3, n) {
    const out = [];
    for (let i = 0; i <= n; i++) {
      const u = i / n, v = 1 - u;
      out.push([
        v * v * v * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u * u * u * p3[0],
        v * v * v * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u * u * u * p3[1],
      ]);
    }
    return out;
  }

  // rotate a vector about the origin
  function rot2(x, y, a) {
    const c = Math.cos(a), s = Math.sin(a);
    return [x * c - y * s, x * s + y * c];
  }

  // interpolate two offsets from a common centre in polar form, so a shape turns instead of
  // collapsing through the middle when its pose rotates 70 degrees
  function polarLerp(cx, cy, a, b, e) {
    const ax = a[0] - cx, ay = a[1] - cy, bx = b[0] - cx, by = b[1] - cy;
    const r0 = Math.hypot(ax, ay), r1 = Math.hypot(bx, by);
    const t0 = Math.atan2(ay, ax);
    let dt = Math.atan2(by, bx) - t0;
    while (dt > Math.PI) dt -= TAU;
    while (dt < -Math.PI) dt += TAU;
    const ang = t0 + dt * e;
    const rad = r0 + (r1 - r0) * e;
    return [cx + Math.cos(ang) * rad, cy + Math.sin(ang) * rad];
  }

  // a rounded body around a centreline: the outline polygon of a rod with soft tips
  function bodyPoly(pts, half) {
    const n = pts.length;
    if (n < 2) return pts.slice();
    const A = [], B = [];
    for (let i = 0; i < n; i++) {
      const u = i / (n - 1);
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      const nx = -ty / tl, ny = tx / tl;
      const w = half * Math.sqrt(Math.max(0, 1 - Math.pow(Math.abs(2 * u - 1), 6)));
      A.push([pts[i][0] + nx * w, pts[i][1] + ny * w]);
      B.push([pts[i][0] - nx * w, pts[i][1] - ny * w]);
    }
    return A.concat(B.reverse());
  }

  // a coil running inside a body: the chromatin, wound up
  function coilPts(pts, half, turns, phase) {
    const n = pts.length;
    const out = [];
    for (let i = 0; i < n; i++) {
      const u = i / (n - 1);
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      const nx = -ty / tl, ny = tx / tl;
      const w = half * 0.55 * Math.sin(u * TAU * turns + phase) * Math.sqrt(Math.max(0, 1 - Math.pow(Math.abs(2 * u - 1), 6)));
      out.push([pts[i][0] + nx * w, pts[i][1] + ny * w]);
    }
    return out;
  }

  // ---------------------------------------------------------------------------
  // Memoized geometry. Everything below is a pure function of fixed seeds and never of t.
  // ---------------------------------------------------------------------------
  const GEO = {};

  // the cell and the nucleus keep the G1 construction (40-point near-circle, radius + 14*noise)
  // and seed from 01 so their wobble is the same shape the paper shots draw
  function cellPoly() {
    if (GEO.cell) return GEO.cell;
    const s = L.hash(REF, 'cell') & 0x7fffffff;
    const out = [];
    for (let i = 0; i < 40; i++) {
      const a = (i / 40) * TAU;
      const r = CELL_R + 14 * L.noise1(i * 0.31, s) + 5 * L.noise1(i * 0.77, s + 3);
      out.push([NUC.x + Math.cos(a) * r, NUC.y + Math.sin(a) * r]);
    }
    GEO.cell = L.smoothPts(out, true, 10);
    return GEO.cell;
  }

  function nucPoly() {
    if (GEO.nuc) return GEO.nuc;
    const s = L.hash(REF, 'nucleus') & 0x7fffffff;
    const out = [];
    for (let i = 0; i < 36; i++) {
      const a = (i / 36) * TAU;
      const r = NUC.r + 5 * L.noise1(i * 0.37, s) + 2.5 * L.noise1(i * 0.91, s + 5);
      out.push([NUC.x + Math.cos(a) * r, NUC.y + Math.sin(a) * r]);
    }
    GEO.nuc = L.smoothPts(out, true, 8);
    return GEO.nuc;
  }

  // the nuclear rim's inner line, 9 px in, as the art bible's double outline asks
  function nucInner() {
    if (GEO.nucIn) return GEO.nucIn;
    const src = nucPoly();
    GEO.nucIn = src.map((p) => {
      const dx = p[0] - NUC.x, dy = p[1] - NUC.y;
      const d = Math.hypot(dx, dy) || 1;
      return [NUC.x + (dx / d) * (d - 9), NUC.y + (dy / d) * (d - 9)];
    });
    return GEO.nucIn;
  }

  // mitochondria: beans, 60 by 28 px, each on a gently curved spine with folded inner ridges
  function mitoGeo() {
    if (GEO.mito) return GEO.mito;
    const out = [];
    const len = 60, wid = 28;
    for (let i = 0; i < MITO.length; i++) {
      const r = L.rng(sd('mito', i));
      const [x, y] = MITO[i];
      const a = Math.atan2(y - NUC.y, x - NUC.x) + r.range(-1.1, 1.1);
      const curve = r.range(-7, 7);
      const spine = [];
      for (let j = 0; j <= 14; j++) {
        const u = -1 + (2 * j) / 14;
        const p = rot2(u * (len / 2 - wid / 2 + 3), curve * (1 - u * u), a);
        spine.push([x + p[0], y + p[1]]);
      }
      const shell = bodyPoly(spine, wid / 2);
      const inner = bodyPoly(spine, wid / 2 - 4);
      // cristae: folded shelves reaching in from alternate walls
      const ridges = [];
      for (let j = 1; j <= 6; j++) {
        const u = j / 7;
        const k = Math.round(u * (spine.length - 1));
        const b0 = spine[Math.max(0, k - 1)], b1 = spine[Math.min(spine.length - 1, k + 1)];
        let tx = b1[0] - b0[0], ty = b1[1] - b0[1];
        const tl = Math.hypot(tx, ty) || 1;
        const nx = -ty / tl, ny = tx / tl;
        const side = j % 2 ? 1 : -1;
        const w0 = wid / 2 - 3, w1 = -wid / 2 + 9;
        ridges.push([
          [spine[k][0] + nx * side * w0, spine[k][1] + ny * side * w0],
          [spine[k][0] + nx * side * (w0 * 0.35) + (tx / tl) * 3, spine[k][1] + ny * side * (w0 * 0.35) + (ty / tl) * 3],
          [spine[k][0] + nx * side * w1, spine[k][1] + ny * side * w1],
        ]);
      }
      out.push({ x, y, a, shell, inner, ridges, seed: sd('mitoline', i) });
    }
    GEO.mito = out;
    return out;
  }

  // cytoskeleton: fine fibres spanning the cytoplasm from the nuclear rim to the membrane
  function cytoFibres() {
    if (GEO.cyto) return GEO.cyto;
    const r = L.rng(sd('cyto'));
    const out = [];
    for (let i = 0; i < 16; i++) {
      const a0 = (i / 16) * TAU + r.range(-0.12, 0.12);
      const a1 = a0 + r.range(-0.5, 0.5);
      const p0 = [NUC.x + Math.cos(a0) * (NUC.r + 8), NUC.y + Math.sin(a0) * (NUC.r + 8)];
      const p1 = [NUC.x + Math.cos(a1) * (CELL_R - 6), NUC.y + Math.sin(a1) * (CELL_R - 6)];
      const am = (a0 + a1) / 2 + r.range(-0.22, 0.22);
      const rm = lerp(NUC.r + 8, CELL_R - 6, 0.55);
      const pm = [NUC.x + Math.cos(am) * rm, NUC.y + Math.sin(am) * rm];
      out.push({ pts: L.smoothPts([p0, pm, p1], false, 12), seed: sd('cf', i), alpha: r.range(0.1, 0.2) });
    }
    GEO.cyto = out;
    return out;
  }

  // chromatin: loose fibre loops filling the nucleus behind the chromosomes
  function chromatin() {
    if (GEO.chromatin) return GEO.chromatin;
    const r = L.rng(sd('chromatin'));
    const out = [];
    for (let i = 0; i < 9; i++) {
      const a0 = r() * TAU;
      const rad = r.range(55, 150);
      const cx = NUC.x + Math.cos(a0) * r.range(10, 70);
      const cy = NUC.y + Math.sin(a0) * r.range(10, 70);
      const pts = [];
      const n = 26;
      for (let j = 0; j <= n; j++) {
        const a = a0 + (j / n) * TAU * r.range(0.55, 0.95);
        const rr = rad * (0.55 + 0.45 * L.noise1(j * 0.4 + i * 7, sd('cl', i)));
        const x = cx + Math.cos(a) * rr * 0.8;
        const y = cy + Math.sin(a) * rr;
        if (Math.hypot(x - NUC.x, y - NUC.y) > NUC.r - 12) continue;
        pts.push([x, y]);
      }
      if (pts.length > 6) out.push({ pts: L.smoothPts(pts, false, 8), seed: sd('clseed', i) });
    }
    GEO.chromatin = out;
    return out;
  }

  // the near field: loose fibre around chromoA1, authored so it reads at 6x
  function nearFibre() {
    if (GEO.near) return GEO.near;
    const r = L.rng(sd('near'));
    const out = [];
    for (let i = 0; i < 14; i++) {
      const cx = TARGET[0] + r.range(-70, 70);
      const cy = TARGET[1] + r.range(-120, 120);
      const pts = [];
      let x = cx, y = cy;
      let a = r() * TAU;
      for (let j = 0; j < 16; j++) {
        pts.push([x, y]);
        a += r.range(-0.7, 0.7);
        x += Math.cos(a) * 5.5;
        y += Math.sin(a) * 5.5;
      }
      out.push({ pts: L.smoothPts(pts, false, 3), seed: sd('nf', i), alpha: r.range(0.1, 0.26) });
    }
    GEO.near = out;
    return out;
  }

  // one chromosome's centreline, resampled to even arc length with normals
  function pathOf(ci) {
    const key = 'path' + ci;
    if (GEO[key]) return GEO[key];
    const ch = CHR[ci];
    const ca = Math.cos(ch.worm), sa = Math.sin(ch.worm);
    const s0 = sd('worm', ch.key);
    const raw = [];
    const n = 160;
    const vMid = ch.amp * (0.72 * L.noise1(0.5 * 2.7 + 1.3, s0) + 0.28 * L.noise1(0.5 * 6.4, s0 + 1));
    for (let i = 0; i <= n; i++) {
      const s = i / n;
      const u = (s - 0.5) * ch.len;
      const v = ch.amp * (0.72 * L.noise1(s * 2.7 + 1.3, s0) + 0.28 * L.noise1(s * 6.4, s0 + 1)) - vMid;
      raw.push([ch.cx + u * ca - v * sa, ch.cy + u * sa + v * ca]);
    }
    // resample by arc length so rungs and ticks sit evenly along the strand
    const acc = [0];
    for (let i = 1; i < raw.length; i++) acc.push(acc[i - 1] + Math.hypot(raw[i][0] - raw[i - 1][0], raw[i][1] - raw[i - 1][1]));
    const total = acc[acc.length - 1];
    const m = ch.m;
    const Pp = [], Nn = [];
    let j = 0;
    for (let i = 0; i <= m; i++) {
      const a = (i / m) * total;
      while (j < acc.length - 2 && acc[j + 1] < a) j++;
      const f = (a - acc[j]) / Math.max(1e-6, acc[j + 1] - acc[j]);
      Pp.push([lerp(raw[j][0], raw[j + 1][0], f), lerp(raw[j][1], raw[j + 1][1], f)]);
    }
    for (let i = 0; i <= m; i++) {
      const a = Pp[Math.max(0, i - 1)], b = Pp[Math.min(m, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      Nn.push([-ty / tl, tx / tl]);
    }
    GEO[key] = { P: Pp, N: Nn, total, m };
    return GEO[key];
  }

  // ---------------------------------------------------------------------------
  // The copy, as a state of each chromosome
  // ---------------------------------------------------------------------------

  // how far the fork has travelled down a chromosome, 0 at the top end, past 1 when it is through
  function forkAt(t, ci) {
    if (ci === 0) return clamp((t - T_UNZ0) / (T_UNZ1 - T_UNZ0), 0, 1) * 1.07;
    return clamp((t - T_SWP0) / (T_SWP1 - T_SWP0), 0, 1) * 1.07;
  }
  // how far the new strand has been built
  function buildAt(t) {
    return clamp((t - T_NEW0) / (T_NEW1 - T_NEW0), 0, 1) * 1.07;
  }
  // when the copy at s was made, so a just-made stretch can be magenta and settle behind
  function builtAtT(s) {
    return T_NEW0 + (s / 1.07) * (T_NEW1 - T_NEW0);
  }
  function sweptAtT(s) {
    return T_SWP0 + (s / 1.07) * (T_SWP1 - T_SWP0);
  }
  // magenta -> lavender over 8 frames, so no point on the strand holds magenta longer
  function freshColor(age) {
    const u = clamp((age - 3 * FR) / (5 * FR));
    if (u <= 0) return C.mag;
    if (u >= 1) return C.lav;
    return L.mix(C.mag, C.lav, u);
  }

  // separation of the two chromatids: it ramps in behind the fork and stays pinched at the
  // centromere, where sister chromatids hold together until they are pulled apart
  function sepAt(ch, s, fork) {
    const ramp = sstep(0, 0.07, fork - s);
    if (ramp <= 0) return 0;
    const pinch = 1 - 0.5 * Math.exp(-Math.pow((s - 0.5) / 0.045, 2));
    return ch.sep * ramp * pinch;
  }

  // the X pose: chromatid sigma as a rod through the centromere, tilted PHI off the X's axis
  function rodPoint(ch, sigma, s) {
    const u = 1 - 2 * s; // +1 at the top tip, -1 at the bottom
    const half = ch.xh / 2;
    const a = half * u * Math.cos(PHI);
    const p = sigma * (half * u * Math.sin(PHI) + BOW * Math.sin(Math.PI * Math.abs(u)));
    const ax = Math.sin(ch.lean), ay = -Math.cos(ch.lean);
    const px = Math.cos(ch.lean), py = Math.sin(ch.lean);
    return [ch.cx + ax * a + px * p, ch.cy + ay * a + py * p];
  }

  // a chromatid's centreline at time t: worm, doubled worm, or arm of the X
  function chromatidPts(ci, t, sigma, step) {
    const ch = CHR[ci];
    const G = pathOf(ci);
    const fork = forkAt(t, ci);
    const morph = hit(t, ch.pop, 3, E.outBack, 1);
    const out = [];
    for (let i = 0; i <= G.m; i += step) {
      const s = i / G.m;
      const off = sigma * sepAt(ch, s, fork);
      const w = [G.P[i][0] + G.N[i][0] * off, G.P[i][1] + G.N[i][1] * off];
      out.push(morph > 0 ? polarLerp(ch.cx, ch.cy, w, rodPoint(ch, sigma, s), morph) : w);
    }
    if (G.m % step !== 0) {
      const s = 1;
      const off = sigma * sepAt(ch, s, fork);
      const w = [G.P[G.m][0] + G.N[G.m][0] * off, G.P[G.m][1] + G.N[G.m][1] * off];
      out.push(morph > 0 ? polarLerp(ch.cx, ch.cy, w, rodPoint(ch, sigma, 1), morph) : w);
    }
    return out;
  }

  // ---------------------------------------------------------------------------
  // 0  Plate
  // ---------------------------------------------------------------------------
  function drawPlate(ctx) {
    // the grid is drawn separately, under the camera, so the cached plate carries none
    L.blueprint(ctx, { center: [NUC.x, NUC.y], seed: sd('plate'), grid: 0, circles: 3, diagonals: 5, noise: 1 });
  }

  // the plate's own furniture: a ruled band at the head of the sheet and a rule at its foot.
  // Both run full bleed outside the safe area, so they carry no meaning, only density.
  function drawSheet(ctx, t) {
    const drift = ((t * 8) % 24);
    // --- head band
    const y0 = 104, y1 = 196;
    ctx.save();
    ctx.beginPath();
    ctx.rect(0, y0, 1080, y1 - y0);
    ctx.clip();
    ctx.fillStyle = C.navyLight;
    ctx.globalAlpha = 0.4;
    ctx.fillRect(0, y0, 1080, y1 - y0);
    ctx.restore();
    L.hexLattice(ctx, [[0, y0], [1080, y0], [1080, y1], [0, y1]], { r: 11, alpha: 0.12, width: 1, seed: sd('headlat'), jitter: 1 });
    sline(ctx, [[-10, y0], [1090, y0]], { alpha: 0.45, width: 1.6, amp: 0.4, seed: sd('head0') });
    sline(ctx, [[-10, y1], [1090, y1]], { alpha: 0.45, width: 1.6, amp: 0.4, seed: sd('head1') });
    const hp = new Path2D(), hm = new Path2D();
    for (let i = 0; i < 90; i++) {
      const x = -20 + i * 12.6 + drift * 0.25;
      const major = i % 6 === 0;
      const p = major ? hm : hp;
      p.moveTo(x, y1);
      p.lineTo(x, y1 - (major ? 26 : 12));
      if (major) {
        p.moveTo(x, y0);
        p.lineTo(x, y0 + 14);
      }
    }
    ctx.save();
    ctx.strokeStyle = C.lav;
    ctx.lineCap = 'round';
    ctx.globalAlpha = 0.3;
    ctx.lineWidth = 1;
    ctx.stroke(hp);
    ctx.globalAlpha = 0.5;
    ctx.lineWidth = 1.4;
    ctx.stroke(hm);
    ctx.restore();
    // three index glyphs sitting on the band
    for (let i = 0; i < 3; i++) {
      const x = 120 + i * 108;
      sline(ctx, circlePts(x, 150, 22, 20), { closed: true, alpha: 0.5, width: 1.3, amp: 0.3, seed: sd('hg', i) });
      L.ticks(ctx, x, 150, { r: 14, n: 4 + i * 2, len: 8, color: C.white, alpha: 0.45, width: 1.2, rot: 0.4 * i });
    }
    // --- foot rule
    const fy = 1704;
    sline(ctx, [[-10, fy], [1090, fy]], { alpha: 0.35, width: 1.5, amp: 0.4, seed: sd('foot') });
    const fp = new Path2D(), fm = new Path2D();
    for (let i = 0; i < 61; i++) {
      const x = -10 + i * 18.4 - drift * 0.15;
      const major = i % 5 === 0;
      const p = major ? fm : fp;
      p.moveTo(x, fy);
      p.lineTo(x, fy + (major ? 30 : 14));
    }
    ctx.save();
    ctx.strokeStyle = C.lav;
    ctx.lineCap = 'round';
    ctx.globalAlpha = 0.26;
    ctx.lineWidth = 1;
    ctx.stroke(fp);
    ctx.globalAlpha = 0.42;
    ctx.lineWidth = 1.4;
    ctx.stroke(fm);
    ctx.restore();
    sline(ctx, [[-10, 1790], [1090, 1790]], { alpha: 0.2, width: 1.2, amp: 0.3, seed: sd('foot2') });
  }

  // ---------------------------------------------------------------------------
  // 1  Grid under the camera: two levels crossfaded, so the ruling densifies on the push
  // ---------------------------------------------------------------------------
  function drawGrid(ctx, cam) {
    const V = viewBox(cam);
    const k = 1 / cam.zoom;
    // pick the level whose screen pitch sits between 45 and 90 px
    const want = 60 * cam.zoom;
    const lvl = Math.max(0, Math.log2(want / 78));
    const n0 = Math.floor(lvl), n1 = n0 + 1;
    const f = lvl - n0;
    const levels = [[n0, 1 - f * 0.55], [n1, f * 0.9]];
    for (const [n, weight] of levels) {
      if (weight <= 0.02) continue;
      const pitch = 60 / Math.pow(2, n);
      if (pitch < 2) continue;
      const minor = new Path2D(), major = new Path2D();
      const i0 = Math.floor(V.x0 / pitch), i1 = Math.ceil(V.x1 / pitch);
      const j0 = Math.floor(V.y0 / pitch), j1 = Math.ceil(V.y1 / pitch);
      if ((i1 - i0) * (j1 - j0) > 4000) continue;
      for (let i = i0; i <= i1; i++) {
        const x = i * pitch;
        const p = i % 5 === 0 ? major : minor;
        p.moveTo(x, V.y0);
        p.lineTo(x, V.y1);
      }
      for (let j = j0; j <= j1; j++) {
        const y = j * pitch;
        const p = j % 5 === 0 ? major : minor;
        p.moveTo(V.x0, y);
        p.lineTo(V.x1, y);
      }
      ctx.save();
      ctx.strokeStyle = C.grid;
      ctx.lineWidth = k;
      ctx.globalAlpha = 0.3 * weight;
      ctx.stroke(minor);
      ctx.globalAlpha = 0.5 * weight;
      ctx.stroke(major);
      ctx.restore();
    }
  }

  // ---------------------------------------------------------------------------
  // 2  Guide geometry around the nucleus
  // ---------------------------------------------------------------------------
  function drawGuides(ctx, cam, t, wide) {
    const k = 1 / cam.zoom;
    const spin = ((6 * DEG) * (t / 2.5)) - Math.PI / 2;
    if (wide > 0.02) {
      ctx.save();
      ctx.globalAlpha = wide;
      L.guideCircle(ctx, NUC.x, NUC.y, 470, { alpha: 0.15, width: 1.5 * k });
      L.guideCircle(ctx, NUC.x, NUC.y, 640, { alpha: 0.09, width: 1 * k, dash: [3 * k, 9 * k] });
      L.ticks(ctx, NUC.x, NUC.y, { r: 470, n: 72, len: 10 * k, major: 12, majorLen: 22 * k, rot: spin, color: C.lav, alpha: 0.3, width: 1.3 * k, inward: true });
      // the four long construction lines of the plate, through the nucleus
      for (const a of [0, Math.PI / 4, Math.PI / 2, -Math.PI / 4]) {
        sline(ctx, [[NUC.x - Math.cos(a) * 700, NUC.y - Math.sin(a) * 700], [NUC.x + Math.cos(a) * 700, NUC.y + Math.sin(a) * 700]], {
          alpha: 0.09, width: 1, k, amp: 0, dash: [10, 9], seed: sd('diag', a),
        });
      }
      ctx.restore();
    }
    // the nucleus dial stays with the subject at every zoom
    ctx.save();
    ctx.globalAlpha = 0.9;
    L.guideCircle(ctx, NUC.x, NUC.y, 200, { alpha: 0.16, width: 1.5 * k });
    L.guideCircle(ctx, NUC.x, NUC.y, 240, { alpha: 0.1, width: 1 * k, dash: [2 * k, 8 * k] });
    L.ticks(ctx, NUC.x, NUC.y, { r: 200, n: 48, len: 9 * k, major: 12, majorLen: 20 * k, rot: spin, color: C.lav, alpha: 0.42, width: 1.3 * k, inward: true });
    L.ticks(ctx, NUC.x, NUC.y, { r: 200, n: 240, len: 4 * k, rot: spin, color: C.lav, alpha: 0.16, width: 1 * k });
    L.guideCircle(ctx, NUC.x, NUC.y, 7 * k, { alpha: 0.3, cross: 18 * k, width: 1 * k });
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // 3  The cell around the nucleus: it does not vanish because we are looking inside it
  // ---------------------------------------------------------------------------
  function drawCell(ctx, cam, wide) {
    if (wide <= 0.02) return;
    const k = 1 / cam.zoom;
    const cell = cellPoly();
    const nuc = nucPoly();
    ctx.save();
    ctx.globalAlpha = wide;
    // membrane, double line
    sline(ctx, cell, { closed: true, alpha: 0.6, width: 2.5, k, seed: sd('cellout'), amp: 0.7 });
    sline(ctx, cell.map((p) => {
      const dx = p[0] - NUC.x, dy = p[1] - NUC.y;
      const d = Math.hypot(dx, dy) || 1;
      return [NUC.x + (dx / d) * (d - 9), NUC.y + (dy / d) * (d - 9)];
    }), { closed: true, alpha: 0.3, width: 1.5, k, seed: sd('cellin'), amp: 0.6 });
    // cytoskeleton
    for (const f of cytoFibres()) sline(ctx, f.pts, { alpha: f.alpha, width: 1.1, k, seed: f.seed, amp: 0.5 });
    // ribosomes: the stipple that thickened through shot 03
    L.stipple(ctx, [cell, nuc], {
      spacing: 14, r: [0.9, 1.8], color: C.lav, alpha: 0.4 * wide, seed: sd('ribo'), boilAmp: 0.6,
      density: (x, y) => 0.6 + 0.3 * L.noise2(x * 0.006, y * 0.006, sd('ribod')),
    });
    // mitochondria
    for (const m of mitoGeo()) {
      ctx.save();
      ctx.beginPath();
      L.tracePath(ctx, m.shell, true);
      ctx.fillStyle = C.navy;
      ctx.globalAlpha *= 0.5;
      ctx.fill();
      ctx.restore();
      sline(ctx, m.shell, { closed: true, alpha: 0.5, width: 1.5, k, seed: m.seed, amp: 0.5 });
      sline(ctx, m.inner, { closed: true, alpha: 0.22, width: 1, k, seed: m.seed + 7, amp: 0.4 });
      for (let j = 0; j < m.ridges.length; j++) sline(ctx, m.ridges[j], { alpha: 0.32, width: 1.1, k, seed: m.seed + 1 + j, amp: 0.3 });
    }
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // 4  The nucleus
  // ---------------------------------------------------------------------------
  function drawNucleus(ctx, cam, t, wide) {
    const k = 1 / cam.zoom;
    const poly = nucPoly();
    const inner = nucInner();
    // tinted plate inside the rim
    ctx.save();
    ctx.beginPath();
    L.tracePath(ctx, poly, true);
    ctx.fillStyle = C.navyLight;
    ctx.globalAlpha = 0.34;
    ctx.fill();
    ctx.restore();
    // lattice: nucleoplasm, 18 px cells, dropped as the push passes the cell scale
    if (wide > 0.03) {
      ctx.save();
      ctx.globalAlpha = wide;
      L.hexLattice(ctx, poly, { r: 18, alpha: 0.2, width: 1 * k, seed: sd('nuclat'), jitter: 1.3, boilAmp: 0.35 });
      ctx.restore();
    }
    // chromatin loops behind the chromosomes
    ctx.save();
    ctx.globalAlpha = 0.8 * Math.max(wide, 0.25);
    for (const cl of chromatin()) sline(ctx, cl.pts, { alpha: 0.17, width: 1.2, k, seed: cl.seed, amp: 0.6 });
    ctx.restore();
    // nucleolus
    if (wide > 0.03) {
      ctx.save();
      ctx.globalAlpha = wide;
      const nl = circlePts(NUCLEOLUS.x, NUCLEOLUS.y, NUCLEOLUS.r, 26);
      L.stipple(ctx, nl, { spacing: 5, r: [0.9, 1.8], color: C.lav, alpha: 0.4, seed: sd('nucleolus'), boilAmp: 0.5 });
      sline(ctx, nl, { closed: true, alpha: 0.32, width: 1.1, k, seed: sd('nucleolusline'), amp: 0.4 });
      ctx.restore();
    }
    // rim: the art bible's double outline
    sline(ctx, poly, { closed: true, alpha: 0.85, width: 2.5, k, seed: sd('nucrim'), amp: 0.7 });
    sline(ctx, inner, { closed: true, alpha: 0.5, width: 1.5, k, seed: sd('nucrimin'), amp: 0.6 });
    // pores: short ticks straddling the rim
    const pores = new Path2D();
    for (let i = 0; i < 28; i++) {
      const a = (i / 28) * TAU + 0.11;
      const c = Math.cos(a), s = Math.sin(a);
      const rr = NUC.r + 4 * L.noise1(i * 0.7, sd('pore'));
      pores.moveTo(NUC.x + c * (rr - 7), NUC.y + s * (rr - 7));
      pores.lineTo(NUC.x + c * (rr + 7), NUC.y + s * (rr + 7));
    }
    ctx.save();
    ctx.strokeStyle = C.white;
    ctx.globalAlpha = 0.45;
    ctx.lineWidth = 1.5 * k;
    ctx.lineCap = 'round';
    ctx.stroke(pores);
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // 5  The near field, only once the push is deep enough to see fibre
  // ---------------------------------------------------------------------------
  function drawNearField(ctx, cam, near) {
    if (near <= 0.02) return;
    const k = 1 / cam.zoom;
    ctx.save();
    ctx.globalAlpha = near;
    for (const f of nearFibre()) sline(ctx, f.pts, { alpha: f.alpha, width: 1.3, k, seed: f.seed, amp: 0.8 });
    L.stipple(ctx, null, {
      bounds: [TARGET[0] - 110, TARGET[1] - 190, 220, 380], spacing: 11, r: [0.6, 1.1], color: C.lav,
      alpha: 0.15, seed: sd('nearstip'), boilAmp: 0.8, density: 0.45,
    });
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // 6  The chromosomes
  // ---------------------------------------------------------------------------
  function drawChromosomeBody(ctx, cam, t, ci, bodyAlpha) {
    if (bodyAlpha <= 0.02) return;
    const ch = CHR[ci];
    const k = 1 / cam.zoom;
    const fork = forkAt(t, ci);
    const morph = hit(t, ch.pop, 3, E.outBack, 1);
    const half = lerp(ch.w, ch.rod, clamp(morph)) / 2;
    const step = ci === 0 ? 10 : 3;
    const single = fork <= 0.001;
    const sigmas = single ? [0] : [-1, 1];
    ctx.save();
    ctx.globalAlpha *= bodyAlpha;
    for (const sigma of sigmas) {
      const mid = chromatidPts(ci, t, sigma, step);
      const poly = bodyPoly(mid, half);
      // body
      ctx.save();
      ctx.beginPath();
      L.tracePath(ctx, poly, true);
      ctx.fillStyle = C.navy;
      ctx.globalAlpha *= 0.6;
      ctx.fill();
      ctx.restore();
      // the coiled chromatin inside, and the bands it makes when it tightens
      sline(ctx, coilPts(mid, half, Math.max(4, Math.round(ch.len / 11)), ci * 1.1 + sigma), { alpha: 0.32, width: 1, k, seed: sd('coil', ci, sigma), amp: 0.3 });
      const bands = new Path2D();
      for (let b = 1; b <= 7; b++) {
        const u = b / 8;
        const i = Math.round(u * (mid.length - 1));
        const a = mid[Math.max(0, i - 1)], bb = mid[Math.min(mid.length - 1, i + 1)];
        let tx = bb[0] - a[0], ty = bb[1] - a[1];
        const tl = Math.hypot(tx, ty) || 1;
        const nx = -ty / tl, ny = tx / tl;
        const w = half * 0.88 * Math.sqrt(Math.max(0, 1 - Math.pow(Math.abs(2 * u - 1), 6)));
        bands.moveTo(mid[i][0] + nx * w, mid[i][1] + ny * w);
        bands.lineTo(mid[i][0] - nx * w, mid[i][1] - ny * w);
      }
      ctx.save();
      ctx.strokeStyle = C.lav;
      ctx.globalAlpha *= 0.34;
      ctx.lineWidth = 1.2 * k;
      ctx.lineCap = 'round';
      ctx.stroke(bands);
      ctx.restore();
      // identity line: pair A blue, pair B rust, thin, never a fill
      sline(ctx, mid, { color: ch.tint, alpha: 0.85, width: ch.tintW, k, seed: sd('tint', ci, sigma), amp: 0.25 });
      sline(ctx, poly, { closed: true, alpha: 0.9, width: 2, k, seed: sd('chrout', ci, sigma), amp: 0.5 });
      // the newly separated stretch glows while it is fresh
      if (!single && ci !== 0) {
        const G = pathOf(ci);
        const hotS = [];
        for (let i = 0; i <= G.m; i += step) {
          const s = i / G.m;
          if (s > fork) break;
          const age = t - sweptAtT(s);
          if (age >= 0 && age < 8 * FR) hotS.push(i);
        }
        if (hotS.length > 1) {
          const seg = [];
          for (const i of hotS) {
            const s = i / G.m;
            const off = sigma * sepAt(ch, s, fork);
            seg.push([G.P[i][0] + G.N[i][0] * off, G.P[i][1] + G.N[i][1] * off]);
          }
          const age0 = t - sweptAtT(hotS[Math.floor(hotS.length / 2)] / G.m);
          sline(ctx, seg, { color: freshColor(age0), alpha: 0.85, width: 2, k, seed: sd('hot', ci, sigma), amp: 0.4 });
        }
      }
    }
    ctx.restore();
  }

  // the centromere: a glow dot with radial ticks, where the two copies stay joined
  function drawCentromere(ctx, cam, t, ci) {
    const ch = CHR[ci];
    const k = 1 / cam.zoom;
    const morph = hit(t, ch.pop, 3, E.outBack, 1);
    const fork = forkAt(t, ci);
    const G = pathOf(ci);
    const mid = Math.round(G.m / 2);
    const base = morph > 0 ? [ch.cx, ch.cy] : [G.P[mid][0], G.P[mid][1]];
    const r = (fork > 0.5 ? 4.6 : 4) * (1 + 0.2 * morph);
    // a disc, not a star: the centromere is a joint, and a big glow would burn the X out
    sline(ctx, circlePts(base[0], base[1], 7 * k, 14), { closed: true, color: C.white, alpha: 0.75, width: 1.4, k, amp: 0.2, seed: sd('cenring', ci) });
    L.glowDot(ctx, base[0], base[1], r * k, { rays: 0, glow: 3.4, intensity: 0.55 + 0.2 * morph, seed: sd('cen', ci) });
    if (morph > 0.4) {
      L.ticks(ctx, base[0], base[1], { r: 13 * k, n: 8, len: 7 * k, color: C.white, alpha: 0.5 * morph, width: 1.2 * k, rot: ch.lean });
    }
  }

  // the pop ring: magenta marks the moment the copy shows as an X
  function drawPopRing(ctx, cam, t, ci) {
    const ch = CHR[ci];
    const d = t - ch.pop;
    if (d < 0 || d >= 6 * FR) return;
    const k = 1 / cam.zoom;
    const e = E.outExpo(clamp((d + FR) / (6 * FR)));
    const a = 1 - clamp((d + FR) / (6 * FR));
    ctx.save();
    ctx.strokeStyle = C.mag;
    ctx.globalAlpha = a;
    ctx.lineWidth = 3 * k;
    ctx.beginPath();
    ctx.arc(ch.cx, ch.cy, lerp(14, 74, e) * 1, 0, TAU);
    ctx.stroke();
    ctx.globalAlpha = a * 0.55;
    ctx.lineWidth = 1.5 * k;
    ctx.beginPath();
    ctx.arc(ch.cx, ch.cy, lerp(14, 104, e), 0, TAU);
    ctx.stroke();
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // 7  The double helix of chromoA1
  // ---------------------------------------------------------------------------
  const HR = 6; // helix radius: the two strands are 12 px apart on the chromosome
  const TURNS = 4.5; // over the 130 px chromosome, about 13 base pairs to a turn
  const RUNG_W = 14 / ZOOM; // rungs every 14 px on screen at zoom 6
  const PH0 = 0.4;

  function strandPhase(s, sigma, mirror) {
    return TAU * TURNS * s + PH0 + (sigma < 0 ? Math.PI : 0) + (mirror ? Math.PI : 0);
  }

  function strandXY(G, i, sigma, mirror, sep) {
    const s = i / G.m;
    const th = strandPhase(s, sigma, mirror);
    const off = sigma * sep + HR * Math.cos(th);
    return [G.P[i][0] + G.N[i][0] * off, G.P[i][1] + G.N[i][1] * off, Math.sin(th), Math.cos(th)];
  }

  // strand segments bucketed by depth, so the far side of the helix reads thinner and dimmer
  function strandInto(buckets, G, ch, sigma, mirror, fork, i0, i1, stride) {
    let prev = null, prevB = -1;
    for (let i = i0; i <= i1; i += stride) {
      const s = i / G.m;
      const sep = sepAt(ch, s, fork);
      const p = strandXY(G, i, sigma, mirror, sep);
      const b = p[2] < -0.34 ? 0 : p[2] < 0.34 ? 1 : 2;
      if (prev) {
        const path = buckets[Math.max(b, prevB)];
        path.moveTo(prev[0], prev[1]);
        path.lineTo(p[0], p[1]);
      }
      prev = p;
      prevB = b;
    }
  }

  function drawHelix(ctx, cam, t, near) {
    if (near <= 0.02) return;
    const ci = 0;
    const ch = CHR[ci];
    const G = pathOf(ci);
    const k = 1 / cam.zoom;
    const fork = forkAt(t, ci);
    const build = buildAt(t);
    const nRungs = Math.max(8, Math.round(G.total / RUNG_W));
    const stride = 2;

    ctx.save();
    ctx.globalAlpha *= near;

    // --- old strands: they run the whole length, wound about the axis, then about their own
    const back = [new Path2D(), new Path2D(), new Path2D()];
    strandInto(back, G, ch, 1, false, fork, 0, G.m, stride);
    strandInto(back, G, ch, -1, false, fork, 0, G.m, stride);
    ctx.save();
    ctx.lineCap = 'round';
    ctx.strokeStyle = C.lav;
    const wds = [1.7, 2.2, 2.7];
    const alf = [0.42, 0.68, 0.95];
    for (let b = 0; b < 3; b++) {
      ctx.globalAlpha = near * alf[b];
      ctx.lineWidth = wds[b] * k;
      ctx.stroke(back[b]);
    }
    ctx.restore();

    // --- new strands, built along each old strand, magenta while fresh
    if (build > 0) {
      const iBuild = Math.min(G.m, Math.round(build * G.m));
      const hotFrom = Math.max(0, Math.round((build - 0.26) * G.m));
      const buckets = [new Path2D(), new Path2D(), new Path2D()];
      for (const sigma of [1, -1]) strandInto(buckets, G, ch, sigma, true, fork, 0, iBuild, stride);
      ctx.save();
      ctx.lineCap = 'round';
      ctx.strokeStyle = C.lav;
      for (let b = 0; b < 3; b++) {
        ctx.globalAlpha = near * alf[b] * 0.95;
        ctx.lineWidth = wds[b] * 0.92 * k;
        ctx.stroke(buckets[b]);
      }
      ctx.restore();
      // the fresh stretch, drawn again in four bands so it reads as a gradient from the fork
      const BANDS = 4;
      for (let bd = 0; bd < BANDS; bd++) {
        const j0 = Math.round(lerp(hotFrom, iBuild, bd / BANDS));
        const j1 = Math.round(lerp(hotFrom, iBuild, (bd + 1) / BANDS));
        if (j1 - j0 < stride) continue;
        const hot = [new Path2D(), new Path2D(), new Path2D()];
        for (const sigma of [1, -1]) strandInto(hot, G, ch, sigma, true, fork, j0, j1, stride);
        const age = Math.max(0, t - builtAtT((((j0 + j1) / 2) / G.m) * 1.07));
        const col = freshColor(age);
        if (col === C.lav) continue;
        ctx.save();
        ctx.lineCap = 'round';
        ctx.strokeStyle = col;
        for (let b = 0; b < 3; b++) {
          ctx.globalAlpha = near * alf[b];
          ctx.lineWidth = wds[b] * k;
          ctx.stroke(hot[b]);
        }
        ctx.restore();
      }
    }

    // --- rungs
    const intact = new Path2D();
    const exposed = new Path2D();
    const stubs = [];
    const paired = new Path2D();
    const HOT_N = 4;
    const pairedHot = [];
    for (let b = 0; b < HOT_N; b++) pairedHot.push(new Path2D());
    for (let r = 0; r < nRungs; r++) {
      const s = (r + 0.5) / nRungs;
      const i = Math.min(G.m, Math.round(s * G.m));
      const sep = sepAt(ch, s, fork);
      if (s > fork) {
        // whole rung across the intact helix
        const a = strandXY(G, i, 1, false, sep);
        const b = strandXY(G, i, -1, false, sep);
        if (Math.abs(a[3]) > 0.06) {
          intact.moveTo(a[0], a[1]);
          intact.lineTo(b[0], b[1]);
        }
        continue;
      }
      if (s > build) {
        // unzipped and waiting: each old strand carries its half rung, bases exposed
        for (const sigma of [1, -1]) {
          const a = strandXY(G, i, sigma, false, sep);
          const axis = [G.P[i][0] + G.N[i][0] * sigma * sep, G.P[i][1] + G.N[i][1] * sigma * sep];
          const ex = lerp(a[0], axis[0], 0.52), ey = lerp(a[1], axis[1], 0.52);
          exposed.moveTo(a[0], a[1]);
          exposed.lineTo(ex, ey);
          stubs.push([ex, ey, 1.5 * k]);
        }
        continue;
      }
      // re-paired inside each new double helix
      const age = Math.max(0, t - builtAtT(s * 1.07));
      const fresh = age < 8 * FR;
      const band = fresh ? Math.min(HOT_N - 1, Math.floor((age / (8 * FR)) * HOT_N)) : -1;
      for (const sigma of [1, -1]) {
        const a = strandXY(G, i, sigma, false, sep);
        const b = strandXY(G, i, sigma, true, sep);
        if (Math.abs(a[3]) < 0.06) continue;
        const target = fresh ? pairedHot[band] : paired;
        target.moveTo(a[0], a[1]);
        target.lineTo(b[0], b[1]);
      }
    }
    ctx.save();
    ctx.lineCap = 'round';
    ctx.strokeStyle = C.white;
    ctx.globalAlpha = near * 0.5;
    ctx.lineWidth = 1.3 * k;
    ctx.stroke(intact);
    ctx.globalAlpha = near * 0.46;
    ctx.stroke(paired);
    ctx.globalAlpha = near * 0.62;
    ctx.lineWidth = 1.5 * k;
    ctx.stroke(exposed);
    for (let b = 0; b < HOT_N; b++) {
      ctx.strokeStyle = freshColor(((b + 0.5) / HOT_N) * 8 * FR);
      ctx.globalAlpha = near * 0.85;
      ctx.lineWidth = 1.6 * k;
      ctx.stroke(pairedHot[b]);
    }
    ctx.restore();
    dots(ctx, stubs, C.white, near * 0.7);

    // --- the fork itself
    if (fork > 0 && fork < 1.05) {
      const i = Math.min(G.m, Math.round(fork * G.m));
      const fx = G.P[i][0], fy = G.P[i][1];
      L.glowDot(ctx, fx, fy, 5 * k, { rays: 0, glow: 6, intensity: 0.8, color: C.white, seed: sd('fork') });
      const d = t - T_NEW0;
      if (d >= 0 && d < 6 * FR) {
        const e = E.outExpo(clamp((d + FR) / (6 * FR)));
        const a = 1 - clamp((d + FR) / (6 * FR));
        ctx.save();
        ctx.strokeStyle = C.mag;
        ctx.globalAlpha = near * a;
        ctx.lineWidth = 3 * k;
        ctx.beginPath();
        ctx.arc(fx, fy, lerp(16, 96, e) * k, 0, TAU);
        ctx.stroke();
        ctx.restore();
        L.glowDot(ctx, fx, fy, 7 * k, { rays: 12, rayLen: 3.2, glow: 5, color: C.mag, intensity: a * 1.1, seed: sd('forkflash') });
      }
    }
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // 8  Screen-fixed apparatus
  // ---------------------------------------------------------------------------

  // the reticle that finds chromoA1 before the push, and the frame that opens on it
  function drawReticle(ctx, cam, t) {
    const a = t < T_PUSH0 ? 1 : 1 - clamp((t - T_PUSH0) / (5 * FR));
    if (a <= 0.01) return;
    const p = toScreen(cam, TARGET[0], TARGET[1]);
    const e = E.outExpo(clamp(t / (6 * FR)));
    const r = lerp(150, 62, e);
    ctx.save();
    ctx.globalAlpha = a;
    sline(ctx, circlePts(p[0], p[1], r, 40), { closed: true, color: C.white, alpha: 0.55, width: 1.5, amp: 0.4, seed: sd('ret') });
    L.ticks(ctx, p[0], p[1], { r: r + 6, n: 24, len: 9, major: 6, majorLen: 18, color: C.white, alpha: 0.5, width: 1.4 });
    const cross = new Path2D();
    for (const s of [-1, 1]) {
      cross.moveTo(p[0] + s * (r - 26), p[1]);
      cross.lineTo(p[0] + s * (r + 26), p[1]);
      cross.moveTo(p[0], p[1] + s * (r - 26));
      cross.lineTo(p[0], p[1] + s * (r + 26));
    }
    ctx.strokeStyle = C.white;
    ctx.globalAlpha = a * 0.5;
    ctx.lineWidth = 1.4;
    ctx.stroke(cross);
    ctx.restore();
  }

  function drawPushFrame(ctx, cam, t) {
    if (t < T_PUSH0 || t > T_PULL1) return;
    const inPush = t <= T_PUSH1;
    const e = inPush ? E.inOutCubic((t - T_PUSH0) / (T_PUSH1 - T_PUSH0)) : cam.e;
    const a = inPush ? 0.55 * (1 - 0.3 * e) : 0.4 * e;
    const p = toScreen(cam, TARGET[0], TARGET[1]);
    const hw = lerp(120, 470, E.outCubic(e));
    const hh = lerp(180, 860, E.outCubic(e));
    const arm = 54;
    const path = new Path2D();
    for (const sx of [-1, 1]) {
      for (const sy of [-1, 1]) {
        const x = p[0] + sx * hw, y = p[1] + sy * hh;
        path.moveTo(x - sx * arm, y);
        path.lineTo(x, y);
        path.lineTo(x, y - sy * arm);
      }
    }
    ctx.save();
    ctx.strokeStyle = C.white;
    ctx.globalAlpha = a;
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.stroke(path);
    ctx.restore();
  }

  // the bracket the storyboard puts at x = 900: the nucleus when wide, the helix when close
  function drawBrackets(ctx, cam, t, wide, near) {
    if (wide > 0.02) {
      const p0 = toScreen(cam, NUC.x, NUC.y - NUC.r);
      const p1 = toScreen(cam, NUC.x, NUC.y + NUC.r);
      ctx.save();
      ctx.globalAlpha = wide;
      L.bracket(ctx, BRK_X, p0[1], BRK_X, p1[1], { cap: 18, color: C.lav, alpha: 0.6, width: 1.5 });
      L.ticks(ctx, BRK_X + 14, p0[1], { kind: 'linear', length: p1[1] - p0[1], angle: Math.PI / 2, n: 20, len: 8, major: 5, majorLen: 16, color: C.white, alpha: 0.4, width: 1.2, baseline: false });
      // an arc over the nucleus, the shot's other measure
      const c0 = toScreen(cam, NUC.x, NUC.y);
      const rr = NUC.r * cam.zoom + 44;
      L.arcAnnotation(ctx, c0[0], c0[1], rr, -Math.PI * 0.87, -Math.PI * 0.13, { color: C.lav, alpha: 0.5, width: 2, endTicks: 15 });
      L.arcAnnotation(ctx, c0[0], c0[1], rr + 9, -Math.PI * 0.78, -Math.PI * 0.22, { color: C.lav, alpha: 0.22, width: 1, endTicks: 0 });
      ctx.restore();
    }
    if (near > 0.02) {
      const G = pathOf(0);
      const a = toScreen(cam, G.P[0][0], G.P[0][1]);
      const b = toScreen(cam, G.P[G.m][0], G.P[G.m][1]);
      ctx.save();
      ctx.globalAlpha = near;
      L.bracket(ctx, BRK_X, a[1], BRK_X, b[1], { cap: 18, color: C.lav, alpha: 0.7, width: 1.5 });
      // the base-pair rule: one tick per rung, down the left edge
      const nR = Math.max(8, Math.round(G.total / RUNG_W));
      L.ticks(ctx, RULE_X, a[1], { kind: 'linear', length: b[1] - a[1], angle: Math.PI / 2, n: nR, len: 10, major: 10, majorLen: 24, color: C.white, alpha: 0.42, width: 1.2 });
      ctx.restore();
    }
  }

  // the base pairs, magnified again: the halves of each rung key into one another, which is why
  // the copy comes out the same. Drawn with no letters, as a schematic shot carries no text.
  function drawBasePairInset(ctx, t, near) {
    if (near <= 0.02) return;
    const { x: cx, y: cy, r: R } = INSET;
    const fork = forkAt(t, 0);
    const build = buildAt(t);
    ctx.save();
    ctx.globalAlpha = near;
    // plate
    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, TAU);
    ctx.fillStyle = C.navyLight;
    ctx.globalAlpha = near * 0.8;
    ctx.fill();
    ctx.restore();
    L.hexLattice(ctx, circlePts(cx, cy, R - 6, 44), { r: 10, alpha: 0.09, width: 1, seed: sd('inlat'), jitter: 0.9 });
    sline(ctx, circlePts(cx, cy, R, 60), { closed: true, alpha: 0.85, width: 2, seed: sd('inrim'), amp: 0.4 });
    sline(ctx, circlePts(cx, cy, R - 7, 60), { closed: true, alpha: 0.4, width: 1.1, seed: sd('inrim2'), amp: 0.35 });
    L.ticks(ctx, cx, cy, { r: R + 5, n: 48, len: 5, major: 12, majorLen: 12, color: C.lav, alpha: 0.4, width: 1 });

    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, R - 8, 0, TAU);
    ctx.clip();
    const H = 92; // half height of the strip
    const RI = 26; // helix radius here
    const SEPI = 40; // how far the two daughters part
    const turns = 1.3;
    const nR = 7;
    const at = (s, sigma, mirror, sep) => {
      const th = TAU * turns * s + 0.7 + (sigma < 0 ? Math.PI : 0) + (mirror ? Math.PI : 0);
      return [cx + sigma * sep + RI * Math.cos(th), cy - H + 2 * H * s, Math.sin(th), Math.cos(th)];
    };
    const sepI = (s) => (sstep(0, 0.1, fork - s) > 0 ? SEPI * sstep(0, 0.1, fork - s) : 0);
    // strands
    for (const sigma of [1, -1]) {
      const pts = [];
      for (let i = 0; i <= 80; i++) {
        const s = i / 80;
        pts.push(at(s, sigma, false, sepI(s)));
      }
      sline(ctx, pts, { alpha: 0.9, width: 2.4, seed: sd('instrand', sigma), amp: 0.4 });
      if (build > 0) {
        const npts = [];
        for (let i = 0; i <= 80; i++) {
          const s = i / 80;
          if (s > build) break;
          npts.push(at(s, sigma, true, sepI(s)));
        }
        if (npts.length > 1) {
          const age = Math.max(0, t - builtAtT(clamp(build - 0.1) * 1.07));
          sline(ctx, npts, { color: build < 1.0 ? freshColor(age) : C.lav, alpha: 0.9, width: 2.2, seed: sd('innew', sigma), amp: 0.4 });
        }
      }
    }
    // rungs, keyed: a knob on the old half, a notch on the half that meets it
    for (let r = 0; r < nR; r++) {
      const s = (r + 0.5) / nR;
      const sep = sepI(s);
      // the two bases of a pair are complementary, and the pattern changes down the strand
      const swap = r % 2 === 1;
      if (s > fork) {
        const a = at(s, 1, false, sep), b = at(s, -1, false, sep);
        drawKeyedRung(ctx, a, b, C.white, 0.75, swap);
        continue;
      }
      if (s > build) {
        // unzipped: each old strand carries its own half, and only its own partner will fit
        for (const sigma of [1, -1]) {
          const a = at(s, sigma, false, sep);
          const ax = cx + sigma * sep;
          drawHalfRung(ctx, a, [ax, a[1]], C.white, 0.7, (sigma > 0) === swap ? 'notch' : 'knob');
        }
        continue;
      }
      const age = Math.max(0, t - builtAtT(s * 1.07));
      const col = age < 8 * FR ? freshColor(age) : C.white;
      for (const sigma of [1, -1]) {
        const a = at(s, sigma, false, sep), b = at(s, sigma, true, sep);
        drawKeyedRung(ctx, a, b, col, age < 8 * FR ? 0.95 : 0.6, (sigma > 0) === swap);
      }
    }
    ctx.restore();
    ctx.restore();
  }

  function drawHalfRung(ctx, a, b, color, alpha, kind) {
    const w = Math.abs(a[3]);
    if (w < 0.1) return;
    ctx.save();
    ctx.globalAlpha *= alpha * (0.35 + 0.65 * w);
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(a[0], a[1]);
    ctx.lineTo(b[0], b[1]);
    ctx.stroke();
    if (kind === 'knob') {
      ctx.beginPath();
      ctx.arc(b[0], b[1], 3.6, 0, TAU);
      ctx.fill();
    } else {
      // a socket that the knob of the base opposite sits in
      const ang = Math.atan2(a[1] - b[1], a[0] - b[0]);
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      ctx.arc(b[0], b[1], 5.4, ang - 1.35, ang + 1.35);
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawKeyedRung(ctx, a, b, color, alpha, swap) {
    const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
    drawHalfRung(ctx, a, [mx, my], color, alpha, swap ? 'notch' : 'knob');
    drawHalfRung(ctx, b, [mx, my], color, alpha, swap ? 'knob' : 'notch');
  }

  // the helix seen end-on: one cross-section becomes two
  function drawSection(ctx, t, near) {
    if (near <= 0.02) return;
    const { x: cx, y: cy, r: R } = SECT;
    const fork = forkAt(t, 0);
    const build = buildAt(t);
    const split = sstep(0, 0.35, fork);
    ctx.save();
    ctx.globalAlpha = near;
    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, TAU);
    ctx.fillStyle = C.navyLight;
    ctx.globalAlpha = near * 0.75;
    ctx.fill();
    ctx.restore();
    sline(ctx, circlePts(cx, cy, R, 52), { closed: true, alpha: 0.8, width: 1.8, seed: sd('secrim'), amp: 0.35 });
    L.ticks(ctx, cx, cy, { r: R + 5, n: 36, len: 5, major: 9, majorLen: 12, color: C.lav, alpha: 0.35, width: 1 });
    // the cutting plane, edge on
    sline(ctx, [[cx - R + 10, cy], [cx + R - 10, cy]], { color: C.white, alpha: 0.22, width: 1.3, amp: 0, dash: [12, 4, 2, 4] });
    const th = TAU * 0.16 + fork * 3.1;
    const off = lerp(0, 36, split);
    const rr = lerp(30, 24, split);
    for (const sigma of [1, -1]) {
      const ox = cx + sigma * off;
      if (sigma < 0 && split < 0.02) continue;
      sline(ctx, circlePts(ox, cy, rr, 30), { closed: true, alpha: split > 0.02 ? 0.55 : 0.5, width: 1.2, seed: sd('seccirc', sigma), amp: 0.3 });
      const ax = ox + Math.cos(th) * rr, ay = cy + Math.sin(th) * rr;
      const bx = ox - Math.cos(th) * rr, by = cy - Math.sin(th) * rr;
      const hasNew = build > 0.02;
      ctx.save();
      ctx.strokeStyle = C.white;
      ctx.globalAlpha = near * 0.75;
      ctx.lineWidth = 1.6;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(bx, by);
      ctx.stroke();
      ctx.restore();
      dots(ctx, [[ax, ay, 5]], C.lav, 0.95);
      if (split < 0.02 || hasNew) {
        const age = Math.max(0, t - builtAtT(0.4));
        dots(ctx, [[bx, by, 5]], split < 0.02 ? C.lav : freshColor(age), 0.95);
      } else {
        sline(ctx, circlePts(bx, by, 5, 12), { closed: true, color: C.white, alpha: 0.55, width: 1.2, amp: 0 });
      }
    }
    ctx.restore();
  }

  // leaders from the helix out to the two insets
  function drawCallouts(ctx, cam, t, near) {
    if (near <= 0.02) return;
    const G = pathOf(0);
    const fork = clamp(forkAt(t, 0), 0.02, 1);
    const i = Math.min(G.m, Math.round(fork * G.m));
    const p = toScreen(cam, G.P[i][0], G.P[i][1]);
    ctx.save();
    ctx.globalAlpha = near;
    sline(ctx, circlePts(p[0], p[1], 26, 24), { closed: true, color: C.white, alpha: 0.6, width: 1.3, amp: 0.3, seed: sd('call') });
    const toInset = cubicPts([p[0] - 22, p[1] + 10], [p[0] - 150, p[1] + 90], [INSET.x + 60, INSET.y - 180], [INSET.x + 40, INSET.y - INSET.r + 6], 40);
    sline(ctx, toInset, { alpha: 0.4, width: 1.2, amp: 0, dash: [5, 6], seed: sd('lead1') });
    const toSect = cubicPts([p[0] + 22, p[1] - 8], [p[0] + 150, p[1] - 40], [SECT.x - 120, SECT.y - 120], [SECT.x - SECT.r + 8, SECT.y - 26], 40);
    sline(ctx, toSect, { alpha: 0.4, width: 1.2, amp: 0, dash: [5, 6], seed: sd('lead2') });
    ctx.restore();
  }

  // the count, told with ticks: under each chromosome one tick becomes two
  function drawNodes(ctx, t, wide) {
    if (wide <= 0.02) return;
    ctx.save();
    ctx.globalAlpha = wide;
    // rail
    sline(ctx, [[NODES[0].x - 120, NODE_Y], [NODES[3].x + 120, NODE_Y]], { alpha: 0.22, width: 1.3, amp: 0.3, seed: sd('rail') });
    L.ticks(ctx, NODES[0].x - 120, NODE_Y - 0, { kind: 'linear', length: NODES[3].x + 120 - (NODES[0].x - 120), angle: 0, n: 42, len: 7, major: 7, majorLen: 14, color: C.lav, alpha: 0.28, width: 1, baseline: false });
    for (const nd of NODES) {
      const ch = CHR[nd.chr];
      const G = pathOf(nd.chr);
      // leader from the chromosome down to its station
      const a = [G.P[Math.round(G.m * 0.5)][0], G.P[Math.round(G.m * 0.5)][1]];
      const leader = cubicPts(a, [a[0], a[1] + 200], [nd.x, nd.y - 220], [nd.x, nd.y - NODE_R - 4], 36);
      sline(ctx, leader, { alpha: 0.34, width: 1.2, amp: 0, dash: [4, 7], seed: sd('leader', nd.chr) });
      // plate
      ctx.save();
      ctx.beginPath();
      ctx.arc(nd.x, nd.y, NODE_R, 0, TAU);
      ctx.fillStyle = C.navyLight;
      ctx.globalAlpha = wide * 0.85;
      ctx.fill();
      ctx.restore();
      sline(ctx, circlePts(nd.x, nd.y, NODE_R, 36), { closed: true, alpha: 0.7, width: 1.6, amp: 0.35, seed: sd('node', nd.chr) });
      sline(ctx, circlePts(nd.x, nd.y, NODE_R - 7, 30), { closed: true, alpha: 0.3, width: 1, amp: 0.3, seed: sd('node2', nd.chr) });
      L.ticks(ctx, nd.x, nd.y, { r: NODE_R + 4, n: 16, len: 6, major: 4, majorLen: 12, color: C.lav, alpha: 0.4, width: 1.1 });
      // the tick, and its copy
      const e = hit(t, ch.pop, 3, E.outBack, 1);
      const dx = 15 * clamp(e);
      const tick = new Path2D();
      const half = 17;
      for (const sx of e > 0 ? [-1, 1] : [0]) {
        tick.moveTo(nd.x + sx * dx, nd.y - half);
        tick.lineTo(nd.x + sx * dx, nd.y + half);
      }
      ctx.save();
      ctx.strokeStyle = C.white;
      ctx.globalAlpha = wide * 0.95;
      ctx.lineWidth = 4;
      ctx.lineCap = 'round';
      ctx.stroke(tick);
      ctx.restore();
      // a magenta ring on the split
      const d = t - ch.pop;
      if (d >= 0 && d < 6 * FR) {
        const ee = E.outExpo(clamp((d + FR) / (6 * FR)));
        const aa = 1 - clamp((d + FR) / (6 * FR));
        ctx.save();
        ctx.strokeStyle = C.mag;
        ctx.globalAlpha = wide * aa;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(nd.x, nd.y, lerp(18, 56, ee), 0, TAU);
        ctx.stroke();
        ctx.restore();
      }
    }
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // Scene
  // ---------------------------------------------------------------------------
  FILM.scene({
    id: ID,
    draw(ctx, tIn, info) {
      const dur = info.dur;
      const t = clamp(tIn, 0, dur);
      const cam = camAt(t);
      // level of detail: wide is the cell scale, near is the helix scale
      const wide = 1 - sstep(1.7, 3.1, cam.zoom);
      const near = sstep(2.2, 3.6, cam.zoom);

      drawPlate(ctx);
      drawSheet(ctx, t);

      L.camera(ctx, cam, (c) => {
        drawGrid(c, cam);
        drawGuides(c, cam, t, wide);
        drawCell(c, cam, wide);
        drawNucleus(c, cam, t, wide);
        drawNearField(c, cam, near);
        // the three chromosomes we are not inside, then chromoA1 over them
        for (let ci = 1; ci < 4; ci++) {
          if (wide <= 0.02) break;
          drawChromosomeBody(c, cam, t, ci, wide);
          drawCentromere(c, cam, t, ci);
          drawPopRing(c, cam, t, ci);
        }
        drawChromosomeBody(c, cam, t, 0, 1 - near);
        drawHelix(c, cam, t, near);
        drawCentromere(c, cam, t, 0);
        drawPopRing(c, cam, t, 0);
      });

      drawBrackets(ctx, cam, t, wide, near);
      drawCallouts(ctx, cam, t, near);
      drawBasePairInset(ctx, t, near);
      drawSection(ctx, t, near);
      drawNodes(ctx, t, wide);
      drawPushFrame(ctx, cam, t);
      drawReticle(ctx, cam, t);

      L.cycleGlyph(ctx, info.T, 'schematic');
    },
  });
})();
