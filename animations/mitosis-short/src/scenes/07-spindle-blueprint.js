// 07 spindle-blueprint : "Fibres line the chromosomes up" (schematic, global T 13.5 to 16.0)
//
// The mitotic spindle drawn as a blueprint plate on the storyboard's G3 geometry. Layers, back to front:
//   1 blueprint plate: navy base, 60 px grid, guide circles r 380 / 520 / 566 centred (540, 900), two long
//     diagonals, the pole-to-pole axis, side rulers, a bottom tick ruler and registration crosses
//   2 the elongating cell: an ellipse half-width 380 and half-height 520 at (540, 900) as a double lavender
//     outline, a cortex hex lattice band inside the membrane, cytoplasm stipple and 72 rim ticks
//   3 the metaphase plate: the construction line y = 900, its tick scale from x 340 to 740, the two dashed
//     spindle-envelope arcs, and the width bracket that draws on at t 2.0
//   4 the two poles (centrosomes) at (540, 430) and (540, 1370): a 22 px disc with 12 radial ticks, a crossed
//     centriole pair, three rings, a short astral fan and a glow core
//   5 the four X chromosomes on the plate at x 400 (A1), 495 (B1), 585 (B2), 680 (A2): two pinched chromatids
//     each, a 6 px hex lattice, banding ticks, a thin identity line (schemBlue for pair A, schemRust for pair
//     B) and a glow-dot centromere
//   6 the spindle itself: four kinetochore fibres from each pole, three filaments apiece, converging on the
//     centromere and on nothing else, plus ten free fibres per pole fanning past the equator; solid outside
//     the chromosomes and dashed hidden lines under them
//   7 measurement and callouts: the attachment gauge at the top left, an arc annotation over each pole's fan,
//     and two node glyphs (a kinetochore close-up, a fibre bundle end-on) wired back to their sources
//   8 the cycle glyph at (900, 300), drawn by FILM.lib.cycleGlyph so it never drifts from the other shots
//
// Beats (local t, global T = 13.5 + t):
//   0.000  frame 0 is 06's last frame on G3: the ellipse, both poles bright, the four X shapes already on the
//          plate but scattered +-40 px in y and still tilted 20 degrees
//   0.500  fibres shoot from the top pole to each centromere, one per 32nd, 6 frames of outExpo, with a
//          magenta tick at each touch; the kinetochore node wakes on the first touch
//   1.000  the same from the bottom pole, right to left; the cross-section node wakes
//   1.500  the chromosomes snap onto y = 900 and stand upright (outBack over 3 drawings) and the free fibres
//          draw in, one pair per frame
//   2.000  the width bracket draws along the plate and every fibre trembles 2 px on the 12 fps boil
//   2.500  the exact G3 metaphase pose, screen-fixed, held for the hard cut into 08
//
// Nothing here rides a camera transform: the shot is locked at zoom 1 so 08 lands on these pixels.
// No text: schematic shots carry none (art bible 5).
(function () {
  'use strict';

  const FILM = window.FILM;
  const L = FILM.lib;
  const P = L.pal;
  const E = L.ease;
  const TAU = Math.PI * 2;
  const DEG = Math.PI / 180;
  const FR = 1 / 24;

  const ID = 'spindle-blueprint';
  const REF = 'membrane-breaks'; // the shot this one cuts from; its pose is frame 0 here
  const SEED = L.hash(ID) % 100000;
  const sd = (...k) => L.hash(ID, ...k) & 0x7fffffff;

  // Colours. pal is a read-only proxy, so every name is hoisted out of the loops.
  const LAV = P.lavender;
  const WHITE = P.lineWhite;
  const GLOW = P.glow;
  const MAG = P.magenta;
  const NAVY = P.navy;
  const NAVY_L = P.navyLight;
  const TINT_A = P.schemBlue; // pair A identity, thin lines only
  const TINT_B = P.schemRust; // pair B identity, thin lines only

  const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
  const lerp = (a, b, u) => a + (b - a) * u;
  const sstep = (a, b, x) => {
    const u = clamp((x - a) / (b - a));
    return u * u * (3 - 2 * u);
  };

  // ---------------------------------------------------------------------------
  // Shared geometry (docs/storyboard.md, G3 and G5). Copy these numbers exactly.
  // ---------------------------------------------------------------------------

  const CELL = { x: 540, y: 900, rx: 380, ry: 520 };
  const PLATE_Y = 900;
  const PLATE_X0 = 340;
  const PLATE_X1 = 740;
  const POLE_R = 22;
  const POLES = [
    { x: 540, y: 430, dir: 1 }, // top pole; dir is the way its fibres travel
    { x: 540, y: 1370, dir: -1 },
  ];

  // The four X chromosomes: two pairs, A long and blue, B short and rust, as in every other shot.
  // dy0 and tilt0 are the scatter 06 leaves on its last frame (+-40 px in y, 20 degrees alternately);
  // shot 06 copies these four numbers so the cut does not jump.
  const CH = [
    { x: 400, pair: 'A', h: 75, spread: 20, wmax: 9.5, dy0: 31, tilt0: -20 * DEG },
    { x: 495, pair: 'B', h: 50, spread: 16, wmax: 8, dy0: -24, tilt0: 20 * DEG },
    { x: 585, pair: 'B', h: 50, spread: 16, wmax: 8, dy0: 17, tilt0: -20 * DEG },
    { x: 680, pair: 'A', h: 75, spread: 20, wmax: 9.5, dy0: -35, tilt0: 20 * DEG },
  ];
  for (const c of CH) {
    c.w0 = c.wmax * 0.62; // half-width at the waist
    c.waist = c.w0 + 0.35; // centreline offset: the sisters leave a 0.7 px gap at the centromere
    c.tint = c.pair === 'A' ? TINT_A : TINT_B;
  }

  // Beats, local seconds.
  const B_TOP = 0.5; // T 14.0  fibres from the top pole
  const B_BOT = 1.0; // T 14.5  fibres from the bottom pole
  const B_SNAP = 1.5; // T 15.0  the chromosomes snap onto the plate
  const B_TREM = 2.0; // T 15.5  the bracket draws, the fibres tremble
  const S32 = 1.5 * FR; // a 32nd note at 120 bpm
  const FIB_DRAW = 6 * FR; // a fibre draws on over 6 frames
  const TOP_ORDER = [0, 1, 2, 3]; // left to right, the pizzicato rising
  const BOT_ORDER = [3, 2, 1, 0]; // right to left, falling

  const startOf = (i, s) => (s === 0 ? B_TOP + TOP_ORDER.indexOf(i) * S32 : B_BOT + BOT_ORDER.indexOf(i) * S32);
  const landOf = (i, s) => startOf(i, s) + FIB_DRAW;

  // ---------------------------------------------------------------------------
  // Timing helpers (scene anatomy 7)
  // ---------------------------------------------------------------------------

  // drawings since beat a, on the 12 fps twos clock
  const drawing = (t, a) => Math.floor((t - a) * 12 + 1e-6);
  // 0..1 progress, already moving on the beat frame itself
  const hitU = (t, a, frames, lead = 1) => (t < a ? 0 : clamp((t - a) / (frames * FR) + lead / frames));
  // full on the beat frame, fading to nothing over the given frames
  const decay = (t, a, frames) => {
    const u = (t - a + 1e-4) / (frames * FR);
    return u < 0 || u > 1 ? 0 : (1 - u) * (1 - u);
  };
  // the frame index since a beat, for events that must last an exact number of frames
  const framesSince = (t, a) => Math.floor((t - a) * 24 + 1e-4);

  // ---------------------------------------------------------------------------
  // Small geometry helpers
  // ---------------------------------------------------------------------------

  function arcPts(cx, cy, r, a0, a1, step = 5, ry = r) {
    const n = Math.max(2, Math.ceil((Math.abs(a1 - a0) * Math.max(r, ry)) / step));
    const out = [];
    for (let i = 0; i <= n; i++) {
      const a = lerp(a0, a1, i / n);
      out.push([cx + Math.cos(a) * r, cy + Math.sin(a) * ry]);
    }
    return out;
  }

  function quadPts(x0, y0, cx, cy, x1, y1, n = 36) {
    const out = [];
    for (let i = 0; i <= n; i++) {
      const u = i / n, v = 1 - u;
      out.push([v * v * x0 + 2 * u * v * cx + u * u * x1, v * v * y0 + 2 * u * v * cy + u * u * y1]);
    }
    return out;
  }

  function lengthOf(pts) {
    let s = 0;
    for (let i = 1; i < pts.length; i++) s += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    return s;
  }

  // the first fraction u of a polyline, measured by arc length
  function cut(pts, u) {
    if (u >= 1) return pts;
    if (u <= 0 || pts.length < 2) return [];
    const target = lengthOf(pts) * u;
    const out = [pts[0]];
    let acc = 0;
    for (let i = 1; i < pts.length; i++) {
      const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
      if (acc + d >= target) {
        const f = d ? (target - acc) / d : 0;
        out.push([lerp(pts[i - 1][0], pts[i][0], f), lerp(pts[i - 1][1], pts[i][1], f)]);
        break;
      }
      out.push(pts[i]);
      acc += d;
    }
    return out;
  }

  // how far along a ray from (px, py) the cell membrane sits, with a margin
  function rayInsideCell(px, py, ux, uy, margin) {
    const rx = CELL.rx - margin, ry = CELL.ry - margin;
    const dx = (px - CELL.x) / rx, dy = (py - CELL.y) / ry;
    const ex = ux / rx, ey = uy / ry;
    const a = ex * ex + ey * ey;
    const b = 2 * (dx * ex + dy * ey);
    const c = dx * dx + dy * dy - 1;
    const disc = b * b - 4 * a * c;
    if (disc <= 0 || a <= 0) return 0;
    return (-b + Math.sqrt(disc)) / (2 * a);
  }

  // boil jitter for hand-built Path2D geometry
  const jit = (i, k, bi, amp = 0.45) => (L.h3(i, k * 31 + 7, bi * 13 + SEED) - 0.5) * 2 * amp;

  // ---------------------------------------------------------------------------
  // Drawing helpers
  // ---------------------------------------------------------------------------

  function strokeP(ctx, p, color, alpha, width, dash) {
    ctx.save();
    ctx.strokeStyle = color;
    ctx.globalAlpha *= alpha;
    ctx.lineWidth = width;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    if (dash) ctx.setLineDash(dash);
    ctx.stroke(p);
    ctx.restore();
  }

  function fillP(ctx, p, color, alpha) {
    ctx.save();
    ctx.fillStyle = color;
    ctx.globalAlpha *= alpha;
    ctx.fill(p);
    ctx.restore();
  }

  // a hand-inked schematic line: for the hero outlines only, it resamples and costs
  function sl(ctx, pts, o) {
    if (!pts || pts.length < 2) return;
    L.inkPath(
      ctx,
      pts,
      Object.assign(
        {
          width: 1.5, color: LAV, alpha: 0.6, wobble: 0.7, tremble: 0.12, boilAmp: 0.55,
          taper: [3, 3], minWidth: 0.55, widthJitter: 0.1, swell: 0, rough: 0.1, step: 3,
        },
        o
      )
    );
  }

  // a cheap boiling polyline: everything that is not a hero outline
  function pl(ctx, pts, o = {}) {
    if (!pts || pts.length < 2) return;
    const amp = o.amp != null ? o.amp : 0.5;
    const seed = (o.seed | 0) + (o.bi | 0) * 131;
    const p = new Path2D();
    let s = 0;
    const n = pts.length;
    for (let i = 0; i < n; i++) {
      const q = pts[i];
      if (i > 0) s += Math.hypot(q[0] - pts[i - 1][0], q[1] - pts[i - 1][1]);
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
      const tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = Math.hypot(tx, ty) || 1;
      const d = amp ? amp * L.noise1(s * 0.02, seed) : 0;
      const x = q[0] - (ty / tl) * d, y = q[1] + (tx / tl) * d;
      if (i === 0) p.moveTo(x, y);
      else p.lineTo(x, y);
    }
    if (o.closed) p.closePath();
    strokeP(ctx, p, o.color || LAV, o.alpha != null ? o.alpha : 0.6, o.width || 1, o.dash);
  }

  // closed outline with draw-on progress u
  function outline(ctx, pts, u, o) {
    if (u <= 0) return;
    if (u >= 0.999) sl(ctx, pts, Object.assign({ closed: true, overlap: 6 }, o));
    else sl(ctx, cut(pts.concat([pts[0]]), u), o);
  }

  // art bible 3.2 primary double outline: outer 2.5 px at 85 percent, inner 1.5 px at 50 percent
  function doubleOutline(ctx, outer, inner, u, seed, o = {}) {
    const a = o.alpha != null ? o.alpha : 1;
    const col = o.color || LAV;
    outline(ctx, outer, u, { width: o.width || 2.5, alpha: 0.85 * a, seed, color: col });
    outline(ctx, inner, u, { width: o.innerWidth || 1.5, alpha: 0.5 * a, seed: seed + 1, color: col });
  }

  // soft additive halo under a primary outline so the silhouette reads at phone size
  function halo(ctx, pts, closed, alpha, width = 10, color = LAV) {
    if (!pts || pts.length < 2) return;
    const p = new Path2D();
    L.tracePath(p, pts, closed);
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    strokeP(ctx, p, color, alpha, width);
    strokeP(ctx, p, color, alpha * 0.8, width * 0.45);
    ctx.restore();
  }

  // radial ticks along an arc, boiling; dir +1 outward, -1 inward
  function tickArc(ctx, cx, cy, r, o) {
    const n = o.n;
    const a0 = o.a0 != null ? o.a0 : 0;
    const span = o.span != null ? o.span : TAU;
    const full = Math.abs(span - TAU) < 1e-6;
    const dir = o.dir || 1;
    const bi = o.bi || 0;
    const prog = o.p != null ? clamp(o.p) : 1;
    const minor = new Path2D();
    const major = new Path2D();
    const count = full ? n : n + 1;
    const shown = Math.round(count * prog);
    for (let i = 0; i < shown; i++) {
      if (o.skip && o.skip(i)) continue;
      const a = a0 + (i / n) * span + jit(i, 1, bi, 0.002);
      const isMajor = o.major && i % o.major === 0;
      const len = (isMajor ? o.majorLen : o.len) * dir;
      const c = Math.cos(a), s = Math.sin(a);
      const r0 = r + jit(i, 2, bi, 0.4), r1 = r + len + jit(i, 3, bi, 0.5);
      const tgt = isMajor ? major : minor;
      tgt.moveTo(cx + c * r0, cy + s * r0);
      tgt.lineTo(cx + c * r1, cy + s * r1);
    }
    strokeP(ctx, minor, o.color || LAV, o.alpha != null ? o.alpha : 0.5, o.width || 1.2, o.dash);
    if (o.major) {
      strokeP(ctx, major, o.majorColor || o.color || WHITE, o.majorAlpha != null ? o.majorAlpha : 0.6, o.majorWidth || 1.5, o.dash);
    }
  }

  // ---------------------------------------------------------------------------
  // Chromosome geometry
  // ---------------------------------------------------------------------------

  // half-width of a chromatid at u = |distance from the centromere| / arm length
  function halfW(u, c) {
    return c.w0 + (c.wmax - c.w0) * sstep(0.02, 0.32, u) - c.wmax * 0.42 * sstep(0.74, 1, u);
  }

  // one chromatid in the chromosome's own coordinates: a rod that runs from the top arm tip, pinches at
  // the centromere and opens out again to the bottom tip, so the pair reads as an X
  const CHROMATID = (function () {
    const out = [];
    for (let i = 0; i < CH.length; i++) {
      const c = CH[i];
      const tipHW = halfW(1, c);
      const hEff = c.h - tipHW; // the cap tips then land exactly on +-c.h
      const per = [];
      for (let side = -1; side <= 1; side += 2) {
        const n = 30;
        const mid = [];
        const hws = [];
        for (let k = 0; k <= n; k++) {
          const v = -1 + (2 * k) / n;
          const u = Math.abs(v);
          mid.push([side * (c.waist + (c.spread - c.waist) * (0.78 * u + 0.22 * u * u)), v * hEff]);
          hws.push(halfW(u, c));
        }
        per.push({ side, mid, hws, poly: rodOutline(mid, hws) });
      }
      out.push(per);
    }
    return out;
  })();

  // closed outline around a centreline with a per-point half-width and round caps
  function rodOutline(mid, hws, capSteps = 7) {
    const n = mid.length;
    const nx = [], ny = [], tx = [], ty = [];
    for (let i = 0; i < n; i++) {
      const a = mid[Math.max(0, i - 1)], b = mid[Math.min(n - 1, i + 1)];
      let ex = b[0] - a[0], ey = b[1] - a[1];
      const el = Math.hypot(ex, ey) || 1;
      ex /= el;
      ey /= el;
      tx.push(ex);
      ty.push(ey);
      nx.push(-ey);
      ny.push(ex);
    }
    const right = [], left = [];
    for (let i = 0; i < n; i++) {
      right.push([mid[i][0] + nx[i] * hws[i], mid[i][1] + ny[i] * hws[i]]);
      left.push([mid[i][0] - nx[i] * hws[i], mid[i][1] - ny[i] * hws[i]]);
    }
    const cap = (i, sgn) => {
      const out = [];
      const w = hws[i];
      for (let k = 1; k < capSteps; k++) {
        const th = (k / capSteps) * Math.PI;
        const cs = Math.cos(th) * sgn, sn = Math.sin(th) * sgn;
        out.push([mid[i][0] + nx[i] * w * cs + tx[i] * w * sn, mid[i][1] + ny[i] * w * cs + ty[i] * w * sn]);
      }
      return out;
    };
    return right.concat(cap(n - 1, 1), left.slice().reverse(), cap(0, -1));
  }

  // how far a chromosome has settled onto the plate: 0 where 06 left it, 1 on the exact G3 pose
  const SNAP3 = [0.46, 1.12, 1]; // outBack over 3 drawings
  function settle(i, tw) {
    const a1 = landOf(i, 0), a2 = landOf(i, 1);
    let s = 0;
    if (tw >= a1 - 1e-6) s = 0.4 * E.outCubic(clamp((tw - a1) / (4 * FR)));
    if (tw >= a2 - 1e-6) s = 0.4 + 0.32 * E.outCubic(clamp((tw - a2) / (4 * FR)));
    if (tw >= B_SNAP - 1e-6) s = 0.72 + 0.28 * SNAP3[Math.min(2, drawing(tw, B_SNAP))];
    return s;
  }

  // the pose of one chromosome on the twos clock
  function poseOf(i, tw) {
    const c = CH[i];
    const s = settle(i, tw);
    const k = 1 - s; // goes slightly negative on the overshoot drawing
    const d = Math.floor(tw * 12 + 1e-6);
    const jg = (L.h3(i, d, SEED + 41) - 0.5) * 2 * 3.2 * Math.max(0, k);
    const rot = c.tilt0 * k;
    const ca = Math.cos(rot), sa = Math.sin(rot);
    const x = c.x, y = PLATE_Y + c.dy0 * k + jg;
    const world = (q) => [x + q[0] * ca - q[1] * sa, y + q[0] * sa + q[1] * ca];
    return { i, c, x, y, rot, s, ca, sa, world };
  }

  // the two chromatid silhouettes of one chromosome, in screen coordinates
  function chromatidPolys(p) {
    return CHROMATID[p.i].map((cd) => cd.poly.map(p.world));
  }

  // ---------------------------------------------------------------------------
  // Free fibres: ten from each pole, fanning past the equator to the far side
  // ---------------------------------------------------------------------------

  const FREE = (function () {
    const out = [];
    for (let s = 0; s < 2; s++) {
      const pole = POLES[s];
      const r = L.rng(L.hash(ID, 'free', s));
      for (let k = 0; k < 10; k++) {
        const m = -1 + (2 * (k + 0.5)) / 10; // -0.9 .. 0.9 across the fan
        const a = m * 26 * DEG + r.range(-2, 2) * DEG;
        const ux = Math.sin(a), uy = pole.dir * Math.cos(a);
        const reach = rayInsideCell(pole.x, pole.y, ux, uy, 34);
        const len = Math.min(reach, 700 + 150 * (1 - Math.abs(m)) + r.range(-40, 40));
        out.push({
          s, k, pole,
          ex: pole.x + ux * len,
          ey: pole.y + uy * len,
          bow: m * 20 + r.range(-9, 9),
          seed: sd('free', s, k),
          alpha: 0.2 + 0.12 * (1 - Math.abs(m)),
        });
      }
    }
    return out;
  })();

  // ---------------------------------------------------------------------------
  // 1 Blueprint plate and guides
  // ---------------------------------------------------------------------------

  function drawPlate(ctx, t, bi) {
    L.blueprint(ctx, { center: [540, 900], circles: 0, diagonals: 0, seed: 713 });

    // two long diagonals crossing on the plate centre
    const diag = new Path2D();
    diag.moveTo(-60, 240);
    diag.lineTo(1140, 1560);
    diag.moveTo(1140, 240);
    diag.lineTo(-60, 1560);
    strokeP(ctx, diag, LAV, 0.12, 1);

    // the guide circles: r 380 is the cell's half-width, r 520 its half-height, r 566 the outer scale
    L.guideCircle(ctx, CELL.x, CELL.y, 380, { alpha: 0.1, width: 1, dash: [2, 8] });
    L.guideCircle(ctx, CELL.x, CELL.y, 520, { alpha: 0.11, width: 1.4 });
    L.guideCircle(ctx, CELL.x, CELL.y, 566, { alpha: 0.08, width: 1, dash: [2, 9] });
    tickArc(ctx, CELL.x, CELL.y, 566, {
      n: 120, len: 7, major: 10, majorLen: 15, color: LAV, alpha: 0.2,
      majorColor: WHITE, majorAlpha: 0.3, width: 1, majorWidth: 1.2, bi,
    });
    tickArc(ctx, CELL.x, CELL.y, 520, { n: 240, len: 3, dir: -1, color: LAV, alpha: 0.12, width: 1, bi });

    // the pole-to-pole axis and the frame centre line
    const axis = new Path2D();
    axis.moveTo(540, 150);
    axis.lineTo(540, 1740);
    strokeP(ctx, axis, LAV, 0.11, 1, [10, 8]);
    const axisLive = new Path2D();
    axisLive.moveTo(540, POLES[0].y);
    axisLive.lineTo(540, POLES[1].y);
    strokeP(ctx, axisLive, LAV, 0.2, 1, [3, 6]);

    // construction lines through the poles and the plate
    const cons = new Path2D();
    for (const y of [POLES[0].y, PLATE_Y, POLES[1].y]) {
      cons.moveTo(72, y);
      cons.lineTo(1008, y);
    }
    strokeP(ctx, cons, LAV, 0.1, 1, [2, 7]);

    // cross-section ellipses: the cell read as a body of revolution
    for (const y of [600, 760, 1040, 1200]) {
      const k = Math.sqrt(Math.max(0, 1 - Math.pow((y - CELL.y) / CELL.ry, 2)));
      const w = CELL.rx * k;
      if (w < 30) continue;
      pl(ctx, L.ellipsePts(CELL.x, y, w, w * 0.15, 52), { closed: true, alpha: 0.11, width: 1, dash: [3, 6], amp: 0.3, seed: sd('sect', y), bi });
    }

    // left ruler down the full height of the cell
    const rule = new Path2D();
    const ruleMaj = new Path2D();
    rule.moveTo(60, 372);
    rule.lineTo(60, 1428);
    for (let y = 380, i = 0; y <= 1420; y += 20, i++) {
      const tgt = i % 5 === 0 ? ruleMaj : rule;
      tgt.moveTo(60, y + jit(i, 5, bi, 0.3));
      tgt.lineTo(60 + (i % 5 === 0 ? 20 : 9), y + jit(i, 6, bi, 0.3));
    }
    strokeP(ctx, rule, LAV, 0.28, 1);
    strokeP(ctx, ruleMaj, LAV, 0.42, 1.3);

    // right scale, outside the safe area: decoration only
    const rr = new Path2D();
    for (let y = 420, i = 0; y <= 1400; y += 28, i++) {
      rr.moveTo(1004, y);
      rr.lineTo(1004 + (i % 4 === 0 ? 16 : 7), y + jit(i, 7, bi, 0.3));
    }
    rr.moveTo(1004, 420);
    rr.lineTo(1004, 1400);
    strokeP(ctx, rr, LAV, 0.22, 1);

    // bottom tick ruler and its registration crosses
    const RY = 1660, RX0 = 100, RX1 = 980;
    const rl = new Path2D();
    const rlMaj = new Path2D();
    rl.moveTo(RX0, RY);
    rl.lineTo(RX1, RY);
    for (let x = RX0, i = 0; x <= RX1 + 0.1; x += 30, i++) {
      const maj = i % 5 === 0;
      const tgt = maj ? rlMaj : rl;
      tgt.moveTo(x + jit(i, 61, bi, 0.3), RY);
      tgt.lineTo(x + jit(i, 62, bi, 0.3), RY + (maj ? 24 : 12));
    }
    strokeP(ctx, rl, LAV, 0.3, 1.4);
    strokeP(ctx, rlMaj, LAV, 0.34, 1.5);
    const rf = new Path2D();
    for (let x = RX0 + 15, i = 0; x <= RX1; x += 30, i++) {
      rf.moveTo(x, RY);
      rf.lineTo(x, RY + 5 + jit(i, 63, bi, 0.4));
    }
    strokeP(ctx, rf, LAV, 0.18, 1);
    const reg = new Path2D();
    for (const x of [RX0, RX1]) {
      const y = 1760;
      reg.moveTo(x - 18, y);
      reg.lineTo(x + 18, y);
      reg.moveTo(x, y - 18);
      reg.lineTo(x, y + 18);
      reg.moveTo(x + 9, y);
      reg.arc(x, y, 9, 0, TAU);
      reg.moveTo(x, RY + 30);
      reg.lineTo(x, 1742);
    }
    strokeP(ctx, reg, LAV, 0.32, 1.2);

    // the blueprint drop: a short glow wash along the plate on the cut frame
    const drop = decay(t, 0, 4);
    if (drop > 0) {
      ctx.save();
      ctx.globalCompositeOperation = 'lighter';
      const g = ctx.createLinearGradient(0, PLATE_Y - 260, 0, PLATE_Y + 260);
      g.addColorStop(0, L.rgba(GLOW, 0));
      g.addColorStop(0.5, L.rgba(GLOW, 0.07 * drop));
      g.addColorStop(1, L.rgba(GLOW, 0));
      ctx.fillStyle = g;
      ctx.fillRect(0, PLATE_Y - 260, 1080, 520);
      ctx.restore();
    }
  }

  // ---------------------------------------------------------------------------
  // 2 The elongating cell on G3
  // ---------------------------------------------------------------------------

  const CELL_OUT = L.ellipsePts(CELL.x, CELL.y, CELL.rx, CELL.ry, 150);
  const CELL_IN = L.ellipsePts(CELL.x, CELL.y, CELL.rx - 9, CELL.ry - 9, 150);
  const CELL_CORTEX = L.ellipsePts(CELL.x, CELL.y, CELL.rx - 54, CELL.ry - 62, 120);

  function drawCell(ctx, t, bi) {
    // the cortex band: tissue lattice between the membrane and the cytoplasm proper
    L.hexLattice(ctx, [CELL_IN, CELL_CORTEX], {
      r: 17, width: 1, alpha: 0.17, color: LAV, seed: sd('cortex'), jitter: 1.2,
    });

    // cytoplasm stipple, thinner through the middle where the spindle works
    L.stipple(ctx, CELL_IN, {
      spacing: 11, r: [0.7, 1.5], color: LAV, alpha: 0.32, seed: sd('cyto'), boilAmp: 0.6,
      density: (x, y) => {
        const dx = (x - CELL.x) / CELL.rx, dy = (y - CELL.y) / CELL.ry;
        const d = Math.hypot(dx, dy);
        const spindle = 1 - 0.75 * Math.exp(-Math.pow((x - CELL.x) / 300, 2) - Math.pow((y - CELL.y) / 420, 2));
        return clamp(0.22 + 0.7 * sstep(0.35, 1, d)) * spindle;
      },
    });

    // the membrane: a soft halo, then the art bible's double outline
    halo(ctx, CELL_OUT, true, 0.05, 14);
    doubleOutline(ctx, CELL_OUT, CELL_IN, 1, sd('membrane'));

    // rim ticks all the way round, longer every ninth
    const rim = new Path2D();
    const rimMaj = new Path2D();
    for (let i = 0; i < 72; i++) {
      const a = (i / 72) * TAU;
      const cx = Math.cos(a), sy = Math.sin(a);
      const x = CELL.x + cx * CELL.rx, y = CELL.y + sy * CELL.ry;
      // outward normal of the ellipse
      let nx = cx / CELL.rx, ny = sy / CELL.ry;
      const nl = Math.hypot(nx, ny) || 1;
      nx /= nl;
      ny /= nl;
      const maj = i % 9 === 0;
      const len = maj ? 17 : 8;
      const tgt = maj ? rimMaj : rim;
      tgt.moveTo(x + nx * (2 + jit(i, 8, bi, 0.4)), y + ny * 2);
      tgt.lineTo(x + nx * len, y + ny * (len + jit(i, 9, bi, 0.5)));
    }
    strokeP(ctx, rim, LAV, 0.32, 1);
    strokeP(ctx, rimMaj, WHITE, 0.4, 1.4);
  }

  // ---------------------------------------------------------------------------
  // 3 The metaphase plate
  // ---------------------------------------------------------------------------

  function drawPlateLine(ctx, t, bi) {
    const landed = clamp((t - B_SNAP) / (6 * FR));

    // the equator as a construction line right across the frame, brighter inside the cell
    const wide = new Path2D();
    wide.moveTo(40, PLATE_Y);
    wide.lineTo(1040, PLATE_Y);
    strokeP(ctx, wide, LAV, 0.14, 1, [10, 9]);
    const inside = new Path2D();
    inside.moveTo(CELL.x - CELL.rx + 14, PLATE_Y);
    inside.lineTo(CELL.x + CELL.rx - 14, PLATE_Y);
    strokeP(ctx, inside, LAV, 0.22 + 0.2 * landed, 1.2, [4, 7]);

    // the plate's tick scale from x 340 to 740, majors every 100 px
    const minor = new Path2D();
    const major = new Path2D();
    for (let x = PLATE_X0; x <= PLATE_X1 + 0.1; x += 20) {
      const maj = Math.round(x - PLATE_X0) % 100 === 0;
      const tgt = maj ? major : minor;
      const j = jit(x, 11, bi, 0.35);
      tgt.moveTo(x + j, PLATE_Y - (maj ? 9 : 4));
      tgt.lineTo(x + j, PLATE_Y + (maj ? 18 : 8));
    }
    strokeP(ctx, minor, WHITE, 0.32 + 0.2 * landed, 1.2);
    strokeP(ctx, major, WHITE, 0.45 + 0.25 * landed, 1.5);

    // the spindle envelope: two dashed arcs from pole to pole through the ends of the plate
    for (const s of [-1, 1]) {
      const ctrlX = CELL.x + s * 400;
      pl(ctx, quadPts(POLES[0].x, POLES[0].y, ctrlX, PLATE_Y, POLES[1].x, POLES[1].y, 40), {
        alpha: 0.16, width: 1, dash: [4, 9], amp: 0.4, seed: sd('envelope', s), bi,
      });
    }
  }

  // ---------------------------------------------------------------------------
  // 4 The poles
  // ---------------------------------------------------------------------------

  function drawPole(ctx, s, t, bi) {
    const pole = POLES[s];
    const { x, y } = pole;
    const pulse = Math.max(decay(t, s === 0 ? B_TOP : B_BOT, 10), decay(t, 0, 8) * 0.6);

    // a navy knock-out so nothing behind the centrosome muddles it
    const ko = new Path2D();
    ko.arc(x, y, POLE_R + 6, 0, TAU);
    fillP(ctx, ko, NAVY, 0.82);

    // the astral fan: short rays out toward the membrane, away from the spindle
    const ast = new Path2D();
    for (let i = 0; i < 22; i++) {
      const a = (-Math.PI / 2) * pole.dir + (-1 + (2 * (i + 0.5)) / 22) * 104 * DEG;
      const ux = Math.cos(a), uy = Math.sin(a);
      const reach = rayInsideCell(x, y, ux, uy, 26);
      const len = Math.min(reach, 92 + 54 * L.h3(i, 3, SEED + 12));
      ast.moveTo(x + ux * (POLE_R + 6), y + uy * (POLE_R + 6));
      ast.lineTo(x + ux * len + jit(i, 12, bi, 0.6), y + uy * len + jit(i, 13, bi, 0.6));
    }
    strokeP(ctx, ast, LAV, 0.3, 1);

    // three rings and the 22 px disc of G3
    L.guideCircle(ctx, x, y, POLE_R + 26, { alpha: 0.2, width: 1, dash: [3, 6] });
    L.guideCircle(ctx, x, y, POLE_R + 14, { alpha: 0.14, width: 1 });
    pl(ctx, L.ellipsePts(x, y, POLE_R, POLE_R, 40), { closed: true, color: LAV, alpha: 0.9, width: 2.5, amp: 0.4, seed: sd('pole', s), bi });
    pl(ctx, L.ellipsePts(x, y, POLE_R - 7, POLE_R - 7, 32), { closed: true, color: LAV, alpha: 0.5, width: 1.5, amp: 0.3, seed: sd('pole-in', s), bi });

    // the twelve radial ticks of G3
    tickArc(ctx, x, y, POLE_R + 3, {
      n: 12, a0: -Math.PI / 2, len: 14, major: 3, majorLen: 22, color: WHITE, alpha: 0.72,
      majorColor: WHITE, majorAlpha: 0.85, width: 1.5, majorWidth: 1.7, bi,
    });

    // a crossed centriole pair inside the disc
    const cen = new Path2D();
    for (const [ang, off] of [[0.35, -5], [0.35 + Math.PI / 2, 5]]) {
      const cx2 = x + Math.cos(ang + Math.PI / 2) * off, cy2 = y + Math.sin(ang + Math.PI / 2) * off;
      cen.moveTo(cx2 - Math.cos(ang) * 9, cy2 - Math.sin(ang) * 9);
      cen.lineTo(cx2 + Math.cos(ang) * 9, cy2 + Math.sin(ang) * 9);
    }
    strokeP(ctx, cen, WHITE, 0.85, 3);

    // the glow core: art bible 5, radius 9 with a 40 px halo
    L.glowDot(ctx, x, y, 9, {
      rays: 12, rayLen: 1.9, rayWidth: 0.18, glow: 4.4, intensity: 0.72 + 0.45 * pulse,
      seed: sd('poleglow', s), rot: 0.13 + bi * 0.01,
    });
    if (pulse > 0) {
      const pr = new Path2D();
      pr.arc(x, y, lerp(96, POLE_R + 10, pulse), 0, TAU);
      strokeP(ctx, pr, LAV, 0.45 * pulse, 1.4);
    }
  }

  // ---------------------------------------------------------------------------
  // 5 The four X chromosomes
  // ---------------------------------------------------------------------------

  function drawChromosome(ctx, p, polys, bi) {
    const c = p.c;
    const i = p.i;

    // knock-out: the fibres behind stop at the chromosome and carry on as hidden lines
    const ko = new Path2D();
    for (const poly of polys) L.tracePath(ko, poly, true);
    fillP(ctx, ko, NAVY, 0.88);

    // a faint halo so the four shapes read against the fibre field
    for (const poly of polys) halo(ctx, poly, true, 0.04, 9);

    // the lattice inside each chromatid, at 6 px
    ctx.save();
    L.hexLattice(ctx, polys, {
      r: 6, width: 0.9, alpha: 0.34, color: LAV, seed: sd('lat', i), jitter: 0.5, clip: true,
    });
    ctx.restore();

    // banding: short cross ticks along each chromatid, and the identity line down its middle
    for (let k = 0; k < 2; k++) {
      const cd = CHROMATID[i][k];
      const mid = cd.mid.map(p.world);
      const band = new Path2D();
      const n = cd.mid.length;
      for (let j = 3; j < n - 3; j += 3) {
        const a = mid[j - 1], b = mid[j + 1];
        let tx = b[0] - a[0], ty = b[1] - a[1];
        const tl = Math.hypot(tx, ty) || 1;
        tx /= tl;
        ty /= tl;
        const w = cd.hws[j] - 1.6;
        if (w < 1.5) continue;
        band.moveTo(mid[j][0] + ty * w, mid[j][1] - tx * w);
        band.lineTo(mid[j][0] - ty * w, mid[j][1] + tx * w);
      }
      strokeP(ctx, band, LAV, 0.34, 1);
      // the identity line: the one place pair A and pair B are told apart in blueprint
      pl(ctx, mid.slice(2, mid.length - 2), { color: c.tint, alpha: 0.66, width: 1.2, amp: 0.3, seed: sd('tint', i, k), bi });
      // the chromatid outline
      pl(ctx, cd.poly.map(p.world), { closed: true, color: LAV, alpha: 0.9, width: 2.3, amp: 0.45, seed: sd('chr', i, k), bi });
    }

    // the constriction marks either side of the centromere
    const waist = new Path2D();
    for (const s of [-1, 1]) {
      const a = p.world([s * (c.waist + c.wmax * 0.9), -7]);
      const b = p.world([s * (c.waist + c.wmax * 0.9), 7]);
      waist.moveTo(a[0], a[1]);
      waist.lineTo(b[0], b[1]);
    }
    strokeP(ctx, waist, LAV, 0.4, 1.2);
  }

  function drawCentromere(ctx, p, t, bi) {
    const attached = (t >= landOf(p.i, 0) - 1e-6 ? 1 : 0) + (t >= landOf(p.i, 1) - 1e-6 ? 1 : 0);
    const k = 0.48 + 0.13 * attached;
    L.glowDot(ctx, p.x, p.y, 7, {
      rays: 10, rayLen: 1.8, rayWidth: 0.2, glow: 4.4, intensity: k, seed: sd('cen', p.i), rot: p.rot + bi * 0.02,
    });
    const ring = new Path2D();
    ring.arc(p.x, p.y, 12.5, 0, TAU);
    strokeP(ctx, ring, WHITE, 0.6, 1.3);
  }

  // the kinetochore: the plate a fibre grips, drawn on the centromere facing its own pole
  function drawKinetochore(ctx, p, s, t) {
    const land = landOf(p.i, s);
    if (t < land - 1e-6) return;
    const pole = POLES[s];
    let ux = pole.x - p.x, uy = pole.y - p.y;
    const ul = Math.hypot(ux, uy) || 1;
    ux /= ul;
    uy /= ul;
    const px = -uy, py = ux;
    const bx = p.x + ux * 11, by = p.y + uy * 11;
    const grip = new Path2D();
    grip.moveTo(bx + px * 9, by + py * 9);
    grip.lineTo(bx - px * 9, by - py * 9);
    grip.moveTo(bx + px * 9 + ux * 5, by + py * 9 + uy * 5);
    grip.lineTo(bx + px * 9, by + py * 9);
    grip.moveTo(bx - px * 9 + ux * 5, by - py * 9 + uy * 5);
    grip.lineTo(bx - px * 9, by - py * 9);
    strokeP(ctx, grip, WHITE, 0.9, 2);
  }

  // ---------------------------------------------------------------------------
  // 6 The spindle fibres
  // ---------------------------------------------------------------------------

  // 2 px of tremble on the boil clock once the plate is measured
  function trembleAt(t, idx, bi) {
    const amt = 2 * clamp((t - B_TREM) / (4 * FR));
    if (amt <= 0) return 0;
    return (L.h3(idx, bi, SEED + 77) - 0.5) * 2 * amt;
  }

  // every fibre on the frame, as plain polylines: the caller renders them twice, solid outside the
  // chromosomes and as dashed hidden lines under them
  function buildFibres(t, bi, poses) {
    const out = [];
    // kinetochore fibres: three filaments each, splayed at the pole and meeting on the centromere
    for (let s = 0; s < 2; s++) {
      const pole = POLES[s];
      for (let i = 0; i < 4; i++) {
        const st = startOf(i, s);
        const prog = E.outExpo(hitU(t, st, 6));
        if (prog <= 0) continue;
        const p = poses[i];
        let ux = p.x - pole.x, uy = p.y - pole.y;
        const ul = Math.hypot(ux, uy) || 1;
        ux /= ul;
        uy /= ul;
        const px = -uy, py = ux;
        const sx = pole.x + ux * (POLE_R + 4), sy = pole.y + uy * (POLE_R + 4);
        for (let f = -1; f <= 1; f++) {
          const idx = (s * 4 + i) * 3 + (f + 1);
          const tr = trembleAt(t, idx, bi);
          const spread = f * 7;
          const bow = f * 13 + tr + (L.h3(idx, 5, SEED + 3) - 0.5) * 6;
          const mx = (sx + p.x) / 2 + px * bow, my = (sy + p.y) / 2 + py * bow;
          const pts = quadPts(sx + px * spread, sy + py * spread, mx, my, p.x, p.y, 30);
          out.push({
            pts: cut(pts, prog),
            width: f === 0 ? 2 : 1.3,
            alpha: f === 0 ? 0.5 : 0.34,
            seed: sd('kfib', s, i, f),
            k: true,
          });
        }
      }
    }
    // free fibres: they fan past the equator and interdigitate with the other pole's
    for (let n = 0; n < FREE.length; n++) {
      const f = FREE[n];
      const prog = E.outExpo(hitU(t, B_SNAP + f.k * FR, 6));
      if (prog <= 0) continue;
      const tr = trembleAt(t, 200 + n, bi);
      let px = -(f.ey - f.pole.y), py = f.ex - f.pole.x;
      const pln = Math.hypot(px, py) || 1;
      px /= pln;
      py /= pln;
      const mx = (f.pole.x + f.ex) / 2 + px * (f.bow + tr);
      const my = (f.pole.y + f.ey) / 2 + py * (f.bow + tr);
      let ux = f.ex - f.pole.x, uy = f.ey - f.pole.y;
      const ul = Math.hypot(ux, uy) || 1;
      ux /= ul;
      uy /= ul;
      const pts = quadPts(f.pole.x + ux * (POLE_R + 4), f.pole.y + uy * (POLE_R + 4), mx, my, f.ex, f.ey, 28);
      out.push({ pts: cut(pts, prog), width: 1.4, alpha: f.alpha, seed: f.seed, k: false });
    }
    return out;
  }

  function renderFibres(ctx, fibres, bi, hidden) {
    for (const f of fibres) {
      if (f.pts.length < 2) continue;
      pl(ctx, f.pts, {
        color: WHITE,
        alpha: hidden ? f.alpha * 0.5 : f.alpha,
        width: hidden ? Math.max(1, f.width - 0.5) : f.width,
        amp: 0.6,
        seed: f.seed,
        bi,
        dash: hidden ? [4, 5] : null,
      });
    }
  }

  function clipOutsideChromosomes(ctx, polys) {
    ctx.beginPath();
    ctx.rect(-60, -60, 1200, 2040);
    for (const poly of polys) L.tracePath(ctx, poly, true);
    ctx.clip('evenodd');
  }

  function clipInsideChromosomes(ctx, polys) {
    ctx.beginPath();
    for (const poly of polys) L.tracePath(ctx, poly, true);
    ctx.clip('evenodd');
  }

  // ---------------------------------------------------------------------------
  // 7 Magenta: each touch, and the snap onto the plate
  // ---------------------------------------------------------------------------

  function drawMagenta(ctx, t, poses) {
    // a ring and a cross tick at each centromere as its fibre lands, 6 frames
    for (let s = 0; s < 2; s++) {
      const pole = POLES[s];
      for (let i = 0; i < 4; i++) {
        const land = landOf(i, s);
        const fr = framesSince(t, land);
        if (fr < 0 || fr >= 6) continue;
        const p = poses[i];
        const a = 1 - fr / 6;
        const ring = new Path2D();
        ring.arc(p.x, p.y, lerp(10, 46, E.outExpo(fr / 5)), 0, TAU);
        strokeP(ctx, ring, MAG, a, 3);
        let ux = pole.x - p.x, uy = pole.y - p.y;
        const ul = Math.hypot(ux, uy) || 1;
        ux /= ul;
        uy /= ul;
        const tick = new Path2D();
        tick.moveTo(p.x + ux * 18 - uy * 13, p.y + uy * 18 + ux * 13);
        tick.lineTo(p.x + ux * 18 + uy * 13, p.y + uy * 18 - ux * 13);
        strokeP(ctx, tick, MAG, a, 3);
      }
    }
    // the alignment itself: the plate flashes for 4 frames on T 15.0
    const fr = framesSince(t, B_SNAP);
    if (fr >= 0 && fr < 4) {
      const a = 1 - fr / 4;
      const line = new Path2D();
      line.moveTo(PLATE_X0 - 16, PLATE_Y);
      line.lineTo(PLATE_X1 + 16, PLATE_Y);
      strokeP(ctx, line, MAG, a, 3);
      const caps = new Path2D();
      for (const x of [PLATE_X0 - 16, PLATE_X1 + 16]) {
        caps.moveTo(x, PLATE_Y - 16);
        caps.lineTo(x, PLATE_Y + 16);
      }
      strokeP(ctx, caps, MAG, a, 3);
    }
  }

  // ---------------------------------------------------------------------------
  // 8 Measurement
  // ---------------------------------------------------------------------------

  function drawMeasures(ctx, t, bi, poses) {
    // pole-to-pole height on the left, present from frame 0
    const ext = new Path2D();
    for (const pole of POLES) {
      ext.moveTo(118 - 6, pole.y);
      ext.lineTo(pole.x - POLE_R - 14, pole.y);
    }
    strokeP(ctx, ext, LAV, 0.16, 1, [2, 6]);
    L.bracket(ctx, 118, POLES[0].y, 118, POLES[1].y, { alpha: 0.5, cap: 16, color: LAV, width: 1.5 });

    // the width bracket along the plate, drawing on from T 15.5
    const bp = E.outExpo(hitU(t, B_TREM, 6));
    if (bp > 0) {
      const dropLines = new Path2D();
      for (const x of [PLATE_X0, PLATE_X1]) {
        dropLines.moveTo(x, PLATE_Y + 20);
        dropLines.lineTo(x, PLATE_Y + 124);
      }
      strokeP(ctx, dropLines, LAV, 0.3 * bp, 1, [3, 5]);
      L.bracket(ctx, PLATE_X0, PLATE_Y + 130, PLATE_X1, PLATE_Y + 130, { p: bp, alpha: 0.65, cap: 16, color: LAV, width: 1.5 });
      L.ticks(ctx, PLATE_X0, PLATE_Y + 142, {
        kind: 'linear', length: PLATE_X1 - PLATE_X0, angle: 0, n: 20, len: 5, major: 5, majorLen: 11,
        side: 1, color: LAV, alpha: 0.4 * bp, width: 1, baseline: false,
      });
    }

    // an arc annotation over each pole's fan, once that pole's fibres have all landed
    for (let s = 0; s < 2; s++) {
      const pole = POLES[s];
      const done = landOf(s === 0 ? 3 : 0, s);
      const ap = E.outExpo(hitU(t, done, 6));
      if (ap <= 0) continue;
      const angles = poses.map((p) => Math.atan2(p.y - pole.y, p.x - pole.x));
      let a0 = Math.min.apply(null, angles), a1 = Math.max.apply(null, angles);
      if (s === 1) {
        // the bottom pole looks up: keep the arc the short way round
        const t0 = a0;
        a0 = a1;
        a1 = t0;
      }
      L.arcAnnotation(ctx, pole.x, pole.y, 168, a0, a1, { color: LAV, alpha: 0.55, width: 1.4, p: ap, endTicks: 10 });
      const spokes = new Path2D();
      for (const a of [a0, a1]) {
        spokes.moveTo(pole.x + Math.cos(a) * 150, pole.y + Math.sin(a) * 150);
        spokes.lineTo(pole.x + Math.cos(a) * 186, pole.y + Math.sin(a) * 186);
      }
      strokeP(ctx, spokes, LAV, 0.4 * ap, 1.1);
    }
  }

  // ---------------------------------------------------------------------------
  // 9 Attachment gauge, top left: eight cells, one per fibre that has taken hold
  // ---------------------------------------------------------------------------

  function drawGauge(ctx, t, bi) {
    const x0 = 130, yTop = 250, cw = 34, gap = 10, chh = 28;
    const frame = new Path2D();
    const w = 4 * cw + 3 * gap;
    const arm = 11;
    for (const [x, y, sx, sy] of [
      [x0 - 12, yTop - 12, 1, 1],
      [x0 + w + 12, yTop - 12, -1, 1],
      [x0 - 12, yTop + 2 * chh + 6 + 12, 1, -1],
      [x0 + w + 12, yTop + 2 * chh + 6 + 12, -1, -1],
    ]) {
      frame.moveTo(x + sx * arm, y);
      frame.lineTo(x, y);
      frame.lineTo(x, y + sy * arm);
    }
    strokeP(ctx, frame, LAV, 0.5, 1.3);

    for (let i = 0; i < 4; i++) {
      const x = x0 + i * (cw + gap);
      for (let s = 0; s < 2; s++) {
        const y = yTop + s * (chh + 6);
        const box = new Path2D();
        box.rect(x + jit(i, 30 + s, bi, 0.3), y, cw, chh);
        strokeP(ctx, box, LAV, 0.34, 1);
        const land = landOf(i, s);
        const d = drawing(t, land);
        if (d < 0) continue;
        const k = [0.68, 1.1, 1][Math.min(2, d)];
        const f = new Path2D();
        f.rect(x + cw / 2 - (cw * k) / 2, y + chh / 2 - (chh * k) / 2, cw * k, chh * k);
        fillP(ctx, f, WHITE, 0.82);
        // the pair tint as a short upright bar inside the lit cell
        const tint = new Path2D();
        tint.moveTo(x + cw / 2, y + 6);
        tint.lineTo(x + cw / 2, y + chh - 6);
        strokeP(ctx, tint, CH[i].tint, 0.85, 2);
      }
    }
    // a tick scale under the gauge
    const tk = new Path2D();
    const yb = yTop + 2 * chh + 6 + 10;
    tk.moveTo(x0 - 4, yb);
    tk.lineTo(x0 + w + 4, yb);
    for (let i = 0; i <= 8; i++) {
      const x = x0 - 4 + (i * (w + 8)) / 8;
      tk.moveTo(x, yb);
      tk.lineTo(x, yb + (i % 2 === 0 ? 12 : 7));
    }
    strokeP(ctx, tk, LAV, 0.42, 1);
  }

  // ---------------------------------------------------------------------------
  // 10 Node glyphs: a kinetochore close-up and a fibre bundle end-on
  // ---------------------------------------------------------------------------

  const NODE_A = { x: 180, y: 1470, r: 50, wake: landOf(0, 0) };
  const NODE_B = { x: 880, y: 1470, r: 50, wake: landOf(3, 1) };

  function nodeFrame(ctx, N, p, bi, seed) {
    const disc = new Path2D();
    disc.arc(N.x, N.y, (N.r - 1) * (0.7 + 0.3 * p), 0, TAU);
    fillP(ctx, disc, NAVY_L, 0.82 * p);
    pl(ctx, L.ellipsePts(N.x, N.y, N.r, N.r, 64), { closed: true, color: LAV, alpha: 0.85, width: 2, amp: 0.4, seed, bi });
    pl(ctx, L.ellipsePts(N.x, N.y, N.r - 8, N.r - 8, 56), { closed: true, color: LAV, alpha: 0.45, width: 1.2, amp: 0.3, seed: seed + 1, bi });
    tickArc(ctx, N.x, N.y, N.r + 4, {
      n: 32, len: 4, major: 8, majorLen: 9, color: LAV, alpha: 0.4 * p,
      majorColor: WHITE, majorAlpha: 0.5 * p, width: 1, majorWidth: 1.3, bi,
    });
  }

  function drawNodes(ctx, t, bi, poses) {
    // node A: the kinetochore, wired back to the first chromosome to be caught
    const src = poses[0];
    const routeA = quadPts(src.x - 26, src.y + 12, 250, 1200, NODE_A.x + 12, NODE_A.y - NODE_A.r - 6, 40);
    pl(ctx, routeA, { alpha: 0.3, width: 1.2, dash: [2, 7], amp: 0, seed: sd('routeA'), bi });
    const pA = E.outExpo(hitU(t, NODE_A.wake, 8));
    if (pA > 0) {
      pl(ctx, cut(routeA, pA), { alpha: 0.6, width: 1.5, amp: 0.5, seed: sd('wireA'), bi });
      const dot = new Path2D();
      dot.arc(src.x - 26, src.y + 12, 4, 0, TAU);
      strokeP(ctx, dot, WHITE, 0.7 * pA, 1.3);
    }
    nodeFrame(ctx, NODE_A, Math.max(0.35, pA), bi, sd('nodeA'));
    if (pA > 0) drawNodeKinetochore(ctx, NODE_A, pA, bi, t);

    // node B: a fibre bundle seen end-on, wired back to the bottom pole
    const routeB = quadPts(POLES[1].x + 20, POLES[1].y + 18, 770, 1430, NODE_B.x - 14, NODE_B.y - NODE_B.r - 6, 40);
    pl(ctx, routeB, { alpha: 0.3, width: 1.2, dash: [2, 7], amp: 0, seed: sd('routeB'), bi });
    const pB = E.outExpo(hitU(t, NODE_B.wake, 8));
    if (pB > 0) {
      pl(ctx, cut(routeB, pB), { alpha: 0.6, width: 1.5, amp: 0.5, seed: sd('wireB'), bi });
    }
    nodeFrame(ctx, NODE_B, Math.max(0.35, pB), bi, sd('nodeB'));
    if (pB > 0) drawNodeBundle(ctx, NODE_B, pB, bi);
  }

  // inside node A: two chromatid stubs, the centromere and three filaments gripping it
  function drawNodeKinetochore(ctx, N, p, bi, t) {
    ctx.save();
    ctx.beginPath();
    ctx.arc(N.x, N.y, N.r - 6, 0, TAU);
    ctx.clip();
    ctx.globalAlpha *= p;
    for (const s of [-1, 1]) {
      const mid = [];
      const hws = [];
      for (let k = 0; k <= 12; k++) {
        const v = -1 + (2 * k) / 12;
        const u = Math.abs(v);
        mid.push([N.x + s * (7 + 16 * Math.pow(u, 0.8)), N.y + v * 34]);
        hws.push(6 + 4 * sstep(0.02, 0.36, u) - 3 * sstep(0.8, 1, u));
      }
      const poly = rodOutline(mid, hws);
      fillP(ctx, (function () { const q = new Path2D(); L.tracePath(q, poly, true); return q; })(), NAVY, 0.7);
      L.hexLattice(ctx, [poly], { r: 5, width: 0.8, alpha: 0.3, color: LAV, seed: sd('nodelat', s), jitter: 0.4 });
      pl(ctx, poly, { closed: true, color: LAV, alpha: 0.85, width: 1.6, amp: 0.3, seed: sd('noderod', s), bi });
      pl(ctx, mid, { color: TINT_A, alpha: 0.55, width: 1.1, amp: 0.2, seed: sd('nodetint', s), bi });
    }
    // three filaments coming down onto the plate over the centromere
    const fil = new Path2D();
    for (let f = -1; f <= 1; f++) {
      fil.moveTo(N.x + f * 9 + jit(f, 44, bi, 0.5), N.y - 46);
      fil.lineTo(N.x + f * 3, N.y - 14);
    }
    strokeP(ctx, fil, WHITE, 0.75, 1.6);
    const plate = new Path2D();
    plate.moveTo(N.x - 11, N.y - 12);
    plate.lineTo(N.x + 11, N.y - 12);
    plate.moveTo(N.x - 11, N.y - 12);
    plate.lineTo(N.x - 11, N.y - 6);
    plate.moveTo(N.x + 11, N.y - 12);
    plate.lineTo(N.x + 11, N.y - 6);
    strokeP(ctx, plate, WHITE, 0.95, 2);
    L.glowDot(ctx, N.x, N.y, 5, { rays: 8, rayLen: 2, glow: 4.2, intensity: 0.9, seed: sd('nodeglow') });
    ctx.restore();
  }

  // inside node B: a fibre in cross-section, thirteen protofilaments to a tube
  function drawNodeBundle(ctx, N, p, bi) {
    ctx.save();
    ctx.beginPath();
    ctx.arc(N.x, N.y, N.r - 6, 0, TAU);
    ctx.clip();
    ctx.globalAlpha *= p;
    const tubes = [[0, 0, 16], [-27, -9, 10], [27, -9, 10], [-17, 21, 10], [17, 21, 10], [0, -28, 10]];
    for (let i = 0; i < tubes.length; i++) {
      const [dx, dy, r] = tubes[i];
      const cx = N.x + dx, cy = N.y + dy;
      const ring = new Path2D();
      ring.arc(cx, cy, r, 0, TAU);
      strokeP(ctx, ring, i === 0 ? WHITE : LAV, i === 0 ? 0.8 : 0.5, i === 0 ? 1.6 : 1.2);
      const dots = new Path2D();
      const rr = i === 0 ? 2.2 : 1.3;
      for (let k = 0; k < 13; k++) {
        const a = (k / 13) * TAU + jit(i, k, bi, 0.01);
        dots.moveTo(cx + Math.cos(a) * r + rr, cy + Math.sin(a) * r);
        dots.arc(cx + Math.cos(a) * r, cy + Math.sin(a) * r, rr, 0, TAU);
      }
      fillP(ctx, dots, i === 0 ? WHITE : LAV, i === 0 ? 0.9 : 0.6);
    }
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // Scene
  // ---------------------------------------------------------------------------

  FILM.scene({
    id: ID,
    draw(ctx, tRaw, info) {
      const t = clamp(tRaw, 0, info.dur);
      const tw = L.onTwos(t);
      const bi = L.boil(info.T);

      const poses = [0, 1, 2, 3].map((i) => poseOf(i, tw));
      const shapes = poses.map(chromatidPolys);
      const polys = [];
      for (const pair of shapes) for (const poly of pair) polys.push(poly);
      const fibres = buildFibres(t, bi, poses);

      // 1 plate and guides
      drawPlate(ctx, t, bi);
      // 2 the cell
      drawCell(ctx, t, bi);
      // 3 the metaphase plate
      drawPlateLine(ctx, t, bi);
      // 4 the poles
      drawPole(ctx, 0, t, bi);
      drawPole(ctx, 1, t, bi);
      // 5 the chromosomes
      for (let i = 0; i < 4; i++) drawChromosome(ctx, poses[i], shapes[i], bi);
      // 6 the fibres: solid in the open, hidden lines under the chromosomes
      ctx.save();
      clipOutsideChromosomes(ctx, polys);
      renderFibres(ctx, fibres, bi, false);
      ctx.restore();
      ctx.save();
      clipInsideChromosomes(ctx, polys);
      renderFibres(ctx, fibres, bi, true);
      ctx.restore();
      // the grip, then the centromere on top of it
      for (const p of poses) {
        drawKinetochore(ctx, p, 0, t);
        drawKinetochore(ctx, p, 1, t);
      }
      for (const p of poses) drawCentromere(ctx, p, t, bi);
      // 7 magenta events
      drawMagenta(ctx, t, poses);
      // 8 measurement, 9 gauge, 10 nodes
      drawMeasures(ctx, t, bi, poses);
      drawGauge(ctx, t, bi);
      drawNodes(ctx, t, bi, poses);
      // 11 the cycle glyph, last and never re-implemented
      L.cycleGlyph(ctx, info.T, 'schematic');
    },
  });
})();
