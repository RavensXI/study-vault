// Shot 06 membrane-breaks : "Mitosis begins — the nuclear membrane goes".
// Illustrated (paper plate), global T 11.5 to 13.5 (2.0 s). Enters on core's cream flash
// (transitionIn flash 0.125 s), so frames 0-2 are washed by core; frame 0 is nevertheless the
// full 05 pose underneath: the grown cell (mean radius 440) on G1, nucleus 185, the four X
// chromosomes on G2.
//
// The hinge is T 12.0 (local t 0.5): the nuclear membrane bursts into its 24 dashes, which drift
// out and fade; the nucleus and its nucleolus dissolve. T 12.5: the chromosomes condense (tighter,
// thicker, darker) and the two centrosome poles show at the G3 positions while the membrane tents
// out to meet them. T 13.0: the chromosomes drift to the plate and the cell elongates.
//
// Both ends of this shot are handovers, so both are copied from the finished neighbours rather than
// from the storyboard: frame 0 is 05's last pose (its condensed chromosome table), and from
// T 13.4167 every frame is 07's frame 0 — the four chromosomes gathered at the plate but NOT yet on
// the line (x 400, 495, 585, 680, dy +31, -24, +17, -35 about y 900, tilts -20, +20, -20, +20, and
// 07's chromatid sizes), the poles on G3 and the outline on the G3 ellipse (380 by 520). 07 does the
// snap onto y = 900 itself, on its own beat at T 15.0.
//
// Layers, back to front:
//   1. paper, stripes (stripeCream / stripeApricot), stripe rule lines, corner dust
//   2. construction: guide circles and ticks, the 470 square (its edges carry the poles), the 45
//      degree diameters, the growth dimension bars
//   3. cytoplasm: fill, cytoHatch band near the membrane, ribosome stipple, twelve mitochondria
//   4. nucleus: mauve fill, cross-hatch shadow, nucleolus (dissolving to stipple)
//   5. the four X chromosomes on G2, condensing and drifting to the plate
//   6. the nuclear envelope: 24 inkSoft dashes, intact then bursting
//   7. the cell membrane (6 px ink, doubled), then the two poles with their radial ticks
//   8. overlays: annYellow bracket 'nucleus' (the one label), annBlue dotted circle where the
//      nucleus was, hinge rings (annMagenta + annYellow), plate marks and drift trails (annBlue),
//      pole rings (annYellow)
//   9. the cycle glyph (lib.cycleGlyph, verbatim from lib — 02 owns it)
(function () {
  'use strict';

  const FILM = window.FILM;
  const L = FILM.lib;
  const P = L.pal;
  const E = L.ease;
  const TAU = Math.PI * 2;
  const DEG = Math.PI / 180;
  const FR = 1 / 24;
  const TW = 1 / 12;
  const EPS = 1e-6;

  const ID = 'membrane-breaks';
  const REF01 = 'hero-cell'; // G1 owns the cell and nucleus outlines
  const REF05 = 'copies-joined'; // G2 hands the four X chromosomes over

  const sd = (...k) => L.hash(ID, ...k) & 0x7fffffff;
  const sd01 = (...k) => L.hash(REF01, ...k) & 0x7fffffff;
  const sd05 = (...k) => L.hash(REF05, ...k) & 0x7fffffff;

  const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
  const lerp = (a, b, u) => a + (b - a) * u;
  const sstep = (a, b, x) => {
    const u = clamp((x - a) / (b - a || 1));
    return u * u * (3 - 2 * u);
  };

  // ---------------------------------------------------------------------------
  // Shared geometry (docs/storyboard.md, "Shared geometry")
  // ---------------------------------------------------------------------------

  const CX = 540, CY = 900;
  const R_CELL = 440; // G1 grown to 440 by the end of 03
  const RX_G3 = 380, RY_G3 = 520; // the G3 ellipse at T 13.5
  const R_NUC = 185; // nucleus radius after growth
  const PLATE_Y = 900;
  const POLE_TOP = [540, 430];
  const POLE_BOT = [540, 1370];
  const SQ = 470; // the construction square: its horizontal edges pass through both poles

  // local beats (global T = 11.5 + t)
  const B_HINGE = 0.5; // T 12.0 : the envelope bursts
  const B_COND = 1.0; // T 12.5 : the chromosomes condense, the poles show
  const B_DRIFT = 1.5; // T 13.0 : the drift to the plate, the cell elongates
  const T_ELONG = 1.25; // the outline starts to stretch a quarter-beat early so it meets the poles
  const T_LAND = 1.5 + 0.5 - TW; // the last drawing, where every ramp is finished and held

  // G2: four X chromosomes, each two identical copies joined at the centromere.
  // This shot is the handover between two finished neighbours, so both ends are copied exactly.
  //
  //   start  = 05's last frame. Its table is { h, w, rod, cen } with the condense applied
  //            (s 0.94 on h and w, s 0.94 * thick 1.08 on rod and cen), tilts -20 / +20 / -20 / +20.
  //            Htot0 = h + rod, because 05 caps its centreline at +-h.
  //   end    = 07's frame 0, which opens on the plate scattered, not aligned: centres x 400, 495,
  //            585, 680 with dy [+31, -24, +17, -35] about y 900 and tilts [-20, +20, -20, +20],
  //            half-height h, tip offset `spread`, chromatid half-width `wmax`. 07 snaps them onto
  //            the line itself at T 15.0, so 06 hands over the scatter, not the G3 metaphase row.
  // The order below is 07's index order, so `i` is the same chromosome in both files.
  const C05 = (h, w, rod) => ({ Htot0: h * 0.94 + rod * 0.94 * 1.08, wTip0: w * 0.94, wmax0: rod * 0.94 * 1.08 });
  const CHROMO = [
    Object.assign({ id: 'A1', pair: 0, x0: 470, y0: 850, tilt0: -20 * DEG, cen0: 7.5 * 0.94 * 1.08,
      x1: 400, dy1: 31, tilt1: -20 * DEG, Htot1: 75, wTip1: 20, wmax1: 9.5 }, C05(75, 20, 7.5)),
    Object.assign({ id: 'B1', pair: 1, x0: 480, y0: 955, tilt0: -20 * DEG, cen0: 6.6 * 0.94 * 1.08,
      x1: 495, dy1: -24, tilt1: 20 * DEG, Htot1: 50, wTip1: 16, wmax1: 8 }, C05(50, 13.5, 6.4)),
    Object.assign({ id: 'B2', pair: 1, x0: 600, y0: 955, tilt0: 20 * DEG, cen0: 6.6 * 0.94 * 1.08,
      x1: 585, dy1: 17, tilt1: -20 * DEG, Htot1: 50, wTip1: 16, wmax1: 8 }, C05(50, 13.5, 6.4)),
    Object.assign({ id: 'A2', pair: 0, x0: 610, y0: 850, tilt0: 20 * DEG, cen0: 7.5 * 0.94 * 1.08,
      x1: 680, dy1: -35, tilt1: 20 * DEG, Htot1: 75, wTip1: 20, wmax1: 9.5 }, C05(75, 20, 7.5)),
  ];
  // 07 adds its own per-drawing jitter to that scatter; on its frame 0 the drawing index is 0, so
  // the offset is this constant. Mirrored here (same hash, same seed) so the cut lands to the pixel.
  const SEED07 = L.hash('spindle-blueprint') % 100000;
  const JIT07 = CHROMO.map((c, i) => (L.h3(i, 0, SEED07 + 41) - 0.5) * 2 * 3.2);
  const PAIR = [
    { base: P.chromoA, deep: P.chromoADeep, light: P.chromoALight },
    { base: P.chromoB, deep: P.chromoBDeep, light: P.chromoBLight },
  ];

  // G1's six mitochondria plus the six 03 draws in as the cell grows: [x, y, rotation]
  const MITO = [
    [300, 700, -0.34], [760, 720, 0.44], [280, 1060, 0.26], [790, 1080, -0.52],
    [420, 1190, 0.14], [660, 640, -0.22], [360, 560, 0.58], [720, 1240, -0.64],
    [240, 900, 1.22], [840, 900, -1.16], [500, 1240, 0.06], [620, 560, 0.36],
  ];

  // ---------------------------------------------------------------------------
  // Seeded outlines: three harmonics so the wobble closes on itself exactly
  // ---------------------------------------------------------------------------

  // The outline wobble: three harmonics, so it closes on itself exactly and never drifts off into
  // an egg. The low harmonic stays small on purpose — the cell is an irregular near-circle, not a pear.
  function harmonics(seed, amp) {
    const r = L.rng(seed);
    const ph = [r() * TAU, r() * TAU, r() * TAU];
    return (a) => amp * (0.3 * Math.sin(3 * a + ph[0]) + 0.42 * Math.sin(5 * a + ph[1]) + 0.28 * Math.sin(8 * a + ph[2]));
  }
  const CELL_WOB = harmonics(sd01('cell-outline'), 14); // G1: radius + 14 * noise
  const NUC_WOB = harmonics(sd01('nucleus-outline'), 7);

  const angTo = (a, b) => {
    let d = Math.abs(a - b) % TAU;
    if (d > Math.PI) d = TAU - d;
    return d;
  };

  // The cell outline: an ellipse (rx, ry) carrying G1's wobble, with a soft tent toward each pole
  // while the centrosomes arrive. The tent decays to zero as the ellipse reaches G3, so the last
  // frame is exactly the G3 ellipse plus the wobble.
  function cellR(a, rx, ry, tent) {
    const ca = Math.cos(a), sa = Math.sin(a);
    const er = (rx * ry) / Math.hypot(ry * ca, rx * sa);
    let tp = 0;
    if (tent > 0.01) {
      // a broad, gentle swell toward each pole — never a point
      const du = angTo(a, -Math.PI / 2) / 0.95;
      const dd = angTo(a, Math.PI / 2) / 0.95;
      tp = tent * (Math.exp(-du * du) + Math.exp(-dd * dd));
    }
    return er + CELL_WOB(a) + tp;
  }
  function cellPts(rx, ry, tent, n) {
    const out = [];
    const N = n || 40; // G1: a 40-point polyline
    for (let i = 0; i < N; i++) {
      const a = (i / N) * TAU;
      const r = cellR(a, rx, ry, tent);
      out.push([CX + Math.cos(a) * r, CY + Math.sin(a) * r]);
    }
    return out;
  }
  const nucR = (a) => R_NUC + NUC_WOB(a);
  const NUC_PTS = (() => {
    const out = [];
    for (let i = 0; i < 32; i++) {
      const a = (i / 32) * TAU;
      out.push([CX + Math.cos(a) * nucR(a), CY + Math.sin(a) * nucR(a)]);
    }
    return out;
  })();
  const NUC_SMOOTH = L.smoothPts(NUC_PTS, true, 9);

  // ---------------------------------------------------------------------------
  // The 24 envelope dashes: contiguous arcs of the nuclear membrane (30 to 60 px each)
  // ---------------------------------------------------------------------------

  const DASHES = (() => {
    const r = L.rng(sd05('envelope'));
    const step = TAU / 24;
    const edge = [];
    for (let i = 0; i < 24; i++) edge.push(i * step + r.range(-0.15, 0.15) * step);
    const out = [];
    for (let i = 0; i < 24; i++) {
      const a0 = edge[i];
      const a1 = (i === 23 ? edge[0] + TAU : edge[i + 1]);
      const am = (a0 + a1) / 2;
      out.push({
        a0, a1, am,
        pts: (() => {
          const q = [];
          const n = Math.max(3, Math.round(((a1 - a0) * R_NUC) / 9));
          for (let k = 0; k <= n; k++) {
            const a = lerp(a0, a1, k / n);
            q.push([Math.cos(a) * nucR(a), Math.sin(a) * nucR(a)]);
          }
          return q;
        })(),
        spin: r.range(-0.55, 0.55),
        side: r.range(-0.22, 0.22), // a little sideways slip as it lets go
        rate: r.range(0.82, 1.2),
        lag: (r.int(0, 2) * 0.5) / 24, // a couple of dashes let go a frame late
        seed: sd('dash', i),
      });
    }
    return out;
  })();

  // The nucleolus, a denser disc inside the nucleus (01: 40 px at (500, 870)), and the stipple
  // it dissolves into once the envelope goes.
  const NLO = [500, 870, 38];
  const NLO_DOTS = (() => {
    const r = L.rng(sd('nucleolus'));
    const out = [];
    for (let i = 0; i < 96; i++) {
      const a = r() * TAU;
      const rr = NLO[2] * Math.sqrt(r());
      out.push({
        x: NLO[0] + Math.cos(a) * rr,
        y: NLO[1] + Math.sin(a) * rr,
        dir: a + r.range(-0.55, 0.55),
        sp: r.range(70, 190),
        r: r.range(1.1, 2.4),
        d: r.range(0, 0.22),
      });
    }
    return out;
  })();

  // ---------------------------------------------------------------------------
  // Small draw helpers
  // ---------------------------------------------------------------------------

  function trace(ctx, pts, closed) {
    for (let i = 0; i < pts.length; i++) {
      if (i === 0) ctx.moveTo(pts[i][0], pts[i][1]);
      else ctx.lineTo(pts[i][0], pts[i][1]);
    }
    if (closed !== false) ctx.closePath();
  }
  function fillPoly(ctx, pts, color, alpha) {
    ctx.save();
    ctx.globalAlpha *= alpha == null ? 1 : alpha;
    ctx.fillStyle = color;
    ctx.beginPath();
    trace(ctx, pts, true);
    ctx.fill();
    ctx.restore();
  }
  function clipPoly(ctx, pts) {
    ctx.beginPath();
    trace(ctx, pts, true);
    ctx.clip();
  }
  function strokePts(ctx, pts, color, width, alpha, dash) {
    if (pts.length < 2 || alpha <= 0) return;
    ctx.save();
    ctx.globalAlpha *= clamp(alpha);
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    if (dash) ctx.setLineDash(dash);
    ctx.beginPath();
    trace(ctx, pts, false);
    ctx.stroke();
    ctx.restore();
  }
  function ring(ctx, x, y, r, color, width, alpha, dash) {
    if (alpha <= 0 || r <= 0) return;
    ctx.save();
    ctx.globalAlpha *= clamp(alpha);
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.lineCap = 'round';
    if (dash) ctx.setLineDash(dash);
    ctx.beginPath();
    ctx.arc(x, y, r, 0, TAU);
    ctx.stroke();
    ctx.restore();
  }
  function dot(ctx, x, y, r, color, alpha) {
    ctx.save();
    ctx.globalAlpha *= alpha == null ? 1 : alpha;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, TAU);
    ctx.fill();
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // 1. Background: paper, stripes, ruled stripe edges, corner dust
  // ---------------------------------------------------------------------------

  const DUST_TOP = [[0, 0], [1080, 0], [1080, 230], [0, 230]];
  const DUST_BOT = [[0, 1580], [1080, 1580], [1080, 1920], [0, 1920]];

  function drawBackground(ctx, Tg) {
    // the default paper and stripe seeds, so the sheet and the bands are the same ones either side
    // of the cut from 05
    L.paper(ctx);
    const off = (Tg / 0.5) * 6; // stripes drift 6 px along their normal per beat
    L.stripes(ctx, { colors: [P.stripeCream, P.stripeApricot], width: 140, angle: -0.52, offset: off });
    // a pencilled rule on every band edge, like a laid-out plate
    ctx.save();
    ctx.globalAlpha = 0.1;
    ctx.strokeStyle = P.inkSoft;
    ctx.lineWidth = 1;
    const a = -0.52, nx = -Math.sin(a), ny = Math.cos(a);
    const o = ((off % 280) + 280) % 280;
    ctx.beginPath();
    for (let k = -12; k <= 12; k++) {
      const v = k * 140 + o;
      const bx = 540 + nx * v, by = 960 + ny * v;
      ctx.moveTo(bx - Math.cos(a) * 1400, by - Math.sin(a) * 1400);
      ctx.lineTo(bx + Math.cos(a) * 1400, by + Math.sin(a) * 1400);
    }
    ctx.stroke();
    ctx.restore();
    L.stipple(ctx, DUST_TOP, { spacing: 11, r: [0.8, 1.5], color: P.inkFaint, alpha: 0.5, density: 0.3, seed: sd('dust', 0) });
    L.stipple(ctx, DUST_BOT, { spacing: 11, r: [0.8, 1.5], color: P.inkFaint, alpha: 0.5, density: 0.3, seed: sd('dust', 1) });
  }

  // ---------------------------------------------------------------------------
  // 2. Construction: the draughtsman's marks the cell is built on
  // ---------------------------------------------------------------------------

  function drawConstruction(ctx, t, elong, ry) {
    // guide circles and a fine graticule round the cell
    L.guideCircle(ctx, CX, CY, SQ, { color: P.inkFaint, alpha: 0.3, width: 1.5 });
    L.guideCircle(ctx, CX, CY, SQ + 90, { color: P.inkFaint, alpha: 0.22, width: 1.2, dash: [7, 9] });
    L.ticks(ctx, CX, CY, { r: SQ + 90, n: 72, len: 10, major: 6, majorLen: 22, color: P.inkFaint, alpha: 0.34, width: 1.4, inward: true });
    // corner registration marks, as on a printer's plate
    ctx.save();
    ctx.strokeStyle = P.inkFaint;
    ctx.globalAlpha = 0.34;
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    for (const [mx, my, sx2, sy2] of [[54, 54, 1, 1], [1026, 54, -1, 1], [54, 1866, 1, -1], [1026, 1866, -1, -1]]) {
      ctx.moveTo(mx, my + sy2 * 26);
      ctx.lineTo(mx, my);
      ctx.lineTo(mx + sx2 * 26, my);
    }
    ctx.stroke();
    ctx.restore();
    // the equator the chromosomes are heading for, ruled right across the plate
    const eq = sstep(B_DRIFT - 2 * FR, B_DRIFT + 4 * FR, t);
    if (eq > 0.01) {
      L.inkPath(ctx, [[540 - 520 * eq, PLATE_Y], [540 + 520 * eq, PLATE_Y]], {
        width: 1.5, color: P.inkFaint, alpha: 0.4 * eq, smooth: false, taper: 0, wobble: 0.9, seed: sd('equator'),
      });
      for (let i = -5; i <= 5; i++) {
        if (!i) continue;
        const x = CX + i * 96;
        if (Math.abs(i * 96) > 520 * eq) continue;
        strokePts(ctx, [[x, PLATE_Y - 9], [x, PLATE_Y + 9]], P.inkFaint, 1.3, 0.4 * eq);
      }
    }
    // the square around it: its horizontal edges pass through both poles (y 430 and 1370)
    const sq = [[CX - SQ, CY - SQ], [CX + SQ, CY - SQ], [CX + SQ, CY + SQ], [CX - SQ, CY + SQ]];
    for (let i = 0; i < 4; i++) {
      const a = sq[i], b = sq[(i + 1) % 4];
      L.inkPath(ctx, [a, b], { width: 1.5, color: P.inkFaint, alpha: 0.32, smooth: false, taper: 0, wobble: 0.9, seed: sd('square', i) });
    }
    // the 45 degree diameters, run well past the cell
    const D = 1180;
    for (const s of [-1, 1]) {
      L.inkPath(ctx, [[CX - D * 0.7071, CY - s * D * 0.7071], [CX + D * 0.7071, CY + s * D * 0.7071]], {
        width: 1.4, color: P.inkFaint, alpha: 0.3, smooth: false, taper: 0, wobble: 1, seed: sd('diag', s),
      });
    }
    // the long axis the poles will sit on, faint outside the cell
    L.inkPath(ctx, [[CX, 120], [CX, 1860]], { width: 1.4, color: P.inkFaint, alpha: 0.26, smooth: false, taper: 0, wobble: 0.8, seed: sd('axis') });
    // growth dimension: a static bar at the old radius, a moving bar on the stretching outline
    if (elong > 0.002) {
      const al = clamp(elong * 2.4) * 0.6;
      for (const s of [-1, 1]) {
        const y0 = CY + s * (R_CELL + 26);
        strokePts(ctx, [[CX - 30, y0], [CX + 30, y0]], P.inkFaint, 1.4, al * 0.8);
        const y1 = CY + s * (ry + 30);
        strokePts(ctx, [[CX - 44, y1], [CX + 44, y1]], P.inkFaint, 2, al);
        strokePts(ctx, [[CX, y0], [CX, y1]], P.inkFaint, 1.3, al * 0.7, [5, 7]);
        strokePts(ctx, [[CX - 9, y1 + s * 11], [CX, y1], [CX + 9, y1 + s * 11]], P.inkFaint, 1.6, al);
      }
    }
  }

  // ---------------------------------------------------------------------------
  // 3. Cytoplasm, mitochondria, ribosomes
  // ---------------------------------------------------------------------------

  function drawMito(ctx, m, sx, sy, k) {
    const x = CX + (m[0] - CX) * sx;
    const y = CY + (m[1] - CY) * sy;
    const rot = m[2];
    const g = 1 + 0.12 * L.noise1(k * 1.7 + 0.3, sd('mitoSize')); // no two beans the same size
    const hl = 30 * g, hw = 14 * g;
    const body = L.capsulePts(x, y, hl * 2, hw, rot, 44);
    L.inkPath(ctx, body, { closed: true, width: 2.6, color: P.ink, fill: P.mito, seed: sd('mito', k), wobble: 1.1, step: 3 });
    const cs = Math.cos(rot), sn = Math.sin(rot);
    const to = (lx, ly) => [x + lx * cs - ly * sn, y + lx * sn + ly * cs];
    // folded inner ridges: cristae reaching in from alternate walls
    const nCr = 6;
    for (let i = 0; i < nCr; i++) {
      const u = -0.74 + (i / (nCr - 1)) * 1.48;
      const side = i % 2 ? 1 : -1;
      const lx = u * hl;
      const reach = hw * (0.5 + 0.34 * L.noise1(i * 2.1 + k, sd('crista', k)));
      L.inkPath(ctx, [to(lx, side * hw * 0.92), to(lx + side * 2.5, side * (hw * 0.92 - reach)), to(lx - 3, -side * (hw * 0.2))], {
        width: 1.8, color: P.mitoDeep, alpha: 0.9, seed: sd('cr', k, i), taper: [3, 6], wobble: 0.4,
      });
    }
    L.inkPath(ctx, [to(-hl * 0.86, 0), to(0, hw * 0.12), to(hl * 0.86, 0)], {
      width: 1.5, color: P.mitoDeep, alpha: 0.5, seed: sd('mitoAxis', k), taper: [8, 8], wobble: 0.4,
    });
    L.hatch(ctx, body, {
      angle: rot + Math.PI / 2, spacing: 5.5, width: 1.2, color: P.mitoDeep, alpha: 0.65, length: [6, 16], gap: [2, 5], inset: 2,
      seed: sd('mitoHatch', k),
      density: (px, py) => sstep(-0.25, 0.7, ((px - x) + (py - y)) / 34),
    });
  }

  function drawCytoplasm(ctx, cellSmooth, sx, sy, nucMask) {
    fillPoly(ctx, cellSmooth, P.cytoplasm);
    // directional hatching near the membrane, heaviest on the lower right (light from the upper left)
    const rxIn = R_CELL * sx, ryIn = R_CELL * sy;
    const band = (px, py) => {
      const dx = (px - CX) / rxIn, dy = (py - CY) / ryIn;
      const rn = Math.hypot(dx, dy);
      const side = sstep(-0.75, 0.9, (dx + dy) * 0.7071);
      return sstep(0.56, 0.97, rn) * (0.34 + 0.66 * side);
    };
    L.hatch(ctx, cellSmooth, {
      angle: -Math.PI / 4, spacing: 8, width: 1.6, color: P.cytoHatch, alpha: 0.95, length: [18, 56], gap: [3, 9],
      inset: 5, seed: sd('cytoHatch'), density: band,
    });
    L.hatch(ctx, cellSmooth, {
      angle: -Math.PI / 4 - Math.PI / 3, spacing: 11, width: 1.4, color: P.cytoHatch, alpha: 0.7, length: [14, 40], gap: [4, 10],
      inset: 6, seed: sd('cytoCross'),
      density: (px, py) => {
        const dx = (px - CX) / rxIn, dy = (py - CY) / ryIn;
        return sstep(0.7, 1, Math.hypot(dx, dy)) * sstep(0.05, 0.95, (dx + dy) * 0.7071);
      },
    });
    // a few soft light strokes round the lit shoulder, so the flat fill has a form
    L.hatch(ctx, cellSmooth, {
      angle: -Math.PI / 4, spacing: 14, width: 1.3, color: P.paperShade, alpha: 0.5, length: [20, 60], gap: [6, 16],
      inset: 10, seed: sd('cytoLit'),
      density: (px, py) => {
        const dx = (px - CX) / rxIn, dy = (py - CY) / ryIn;
        return sstep(0.62, 0.95, Math.hypot(dx, dy)) * sstep(0.1, -0.85, (dx + dy) * 0.7071);
      },
    });
    // ribosomes: 03 lifts the stipple to 0.6; the nucleus keeps them out until it breaks down.
    // A slow noise field clumps them, so the cytoplasm reads as drawn texture, not sand.
    L.stipple(ctx, cellSmooth, {
      spacing: 7.6, r: [1, 2.1], color: P.ribosome, alpha: 0.85, jitter: 0.52, seed: sd('ribo'), boilAmp: 0.4,
      density: (px, py) => {
        const inNuc = 1 - sstep(0.82, 1.06, Math.hypot(px - CX, py - CY) / R_NUC);
        const clump = 0.62 + 0.5 * L.fbm2(px * 0.007, py * 0.007, sd('riboField'), 3);
        return clamp(0.6 * clump) * (1 - inNuc * nucMask);
      },
    });
    for (let k = 0; k < MITO.length; k++) drawMito(ctx, MITO[k], sx, sy, k);
  }

  // ---------------------------------------------------------------------------
  // 4. The nucleus: fill, shadow, nucleolus; then the dissolve
  // ---------------------------------------------------------------------------

  function drawNucleus(ctx, t, tw, alpha, flash) {
    if (alpha <= 0.008) return;
    ctx.save();
    ctx.globalAlpha *= alpha;
    fillPoly(ctx, NUC_SMOOTH, P.nucleus);
    L.crossHatch(ctx, NUC_SMOOTH, {
      angle: -Math.PI / 4, spacing: 9, crossSpacing: 12, width: 1.4, color: P.nucleusDeep, alpha: 0.5, tone: 0.62,
      length: [14, 40], gap: [3, 9], inset: 6, seed: sd('nucHatch'),
      density: (px, py) => sstep(-0.1, 0.9, ((px - CX) + (py - CY)) / (R_NUC * 1.3)),
    });
    L.stipple(ctx, NUC_SMOOTH, {
      spacing: 9, r: [0.9, 1.7], color: P.nucleusDeep, alpha: 0.45, density: 0.4, seed: sd('nucGrain'),
    });
    if (flash > 0.01) fillPoly(ctx, NUC_SMOOTH, P.white, flash);
    ctx.restore();
  }

  function drawNucleolus(ctx, t, tw, alpha) {
    const u = t < B_HINGE ? 0 : clamp((tw - B_HINGE) / (12 * FR));
    if (u < 1) {
      // the solid disc, shrinking as it lets go
      const k = 1 - 0.55 * u;
      ctx.save();
      ctx.globalAlpha *= alpha * (1 - u);
      L.inkCircle(ctx, NLO[0], NLO[1], NLO[2] * k, {
        width: 2, color: P.nucleusDeep, fill: P.nucleusDeep, fillAlpha: 0.85, seed: sd('nlo'), wobble: 1.4,
      });
      L.stipple(ctx, L.ellipsePts(NLO[0], NLO[1], NLO[2] * k, NLO[2] * k, 28), {
        spacing: 6, r: [1, 2], color: P.nucleusRim, alpha: 0.5, density: 0.5, seed: sd('nloGrain'),
      });
      ctx.restore();
    }
    if (u > 0) {
      // ...dissolving as stipple that drifts out and fades
      ctx.save();
      ctx.fillStyle = P.nucleusDeep;
      for (let i = 0; i < NLO_DOTS.length; i++) {
        const d = NLO_DOTS[i];
        const uu = clamp((u - d.d) / (1 - d.d));
        if (uu <= 0) continue;
        const e = E.outCubic(uu);
        const rr = d.sp * e;
        ctx.globalAlpha = 0.85 * (1 - uu) * alpha;
        ctx.beginPath();
        ctx.arc(d.x + Math.cos(d.dir) * rr, d.y + Math.sin(d.dir) * rr, d.r * (1 - 0.35 * uu), 0, TAU);
        ctx.fill();
      }
      ctx.restore();
    }
  }

  // ---------------------------------------------------------------------------
  // 5. The four X chromosomes
  // ---------------------------------------------------------------------------

  // A closed outline round a centreline with a per-point half-width and round caps. Copied from 07
  // so the two shots build the identical silhouette from the identical numbers.
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

  // One copy (chromatid): a rod that leaves the centromere, swells through the arm and rounds off at
  // the tip, so the two of them read as an X. `m` is how far the condense has gone: at 0 the pair
  // touches at the waist and the rod is an even thickness (05's shape), at 1 the waist gap, the
  // profile and every number are 07's frame 0 exactly.
  function chromatid(ps, side) {
    const wmax = ps.wmax;
    const w0 = wmax * lerp(1, 0.62, ps.m);
    const waist = w0 + 0.35 * ps.m;
    const hwAt = (u) => w0 + (wmax - w0) * sstep(0.02, 0.32, u) - wmax * 0.42 * sstep(0.74, 1, u) * ps.m;
    const hEff = ps.Htot - hwAt(1);
    const n = 30;
    const mid = [], hws = [];
    for (let k = 0; k <= n; k++) {
      const v = -1 + (2 * k) / n;
      const u = Math.abs(v);
      mid.push([side * (waist + (ps.wTip - waist) * (0.78 * u + 0.22 * u * u)), v * hEff]);
      hws.push(hwAt(u));
    }
    return { mid, hws, poly: rodOutline(mid, hws) };
  }

  function chromoPose(i, t, tw, drift) {
    const c = CHROMO[i];
    // condense on T 12.5: the copies tighten, thicken and darken (art bible 10.2), over 3 drawings
    const dcond = t < B_COND - EPS ? -1 : Math.floor((tw - B_COND) * 12 + EPS);
    const cond = dcond < 0 ? 0 : [0.62, 1.06, 1][Math.min(2, dcond)];
    const m = clamp(cond); // the shape morph never overshoots, only the size and the tone do
    // released into the cytoplasm once the envelope goes: a small float, gone by the time it lands
    const fl = sstep(B_HINGE, B_COND, tw) * (1 - drift);
    const wob = 0.035 * L.noise1(tw * 2.3 + i * 4.1, sd('wobble', i)) * (1 - drift);
    return {
      i,
      x: lerp(c.x0, c.x1, drift) + 11 * L.noise1(tw * 1.7 + i * 5.3, sd('float', i)) * fl,
      y: lerp(c.y0, PLATE_Y + c.dy1 + JIT07[i], drift) + 9 * L.noise1(tw * 1.45 + i * 7.9, sd('float', i, 2)) * fl,
      rot: lerp(c.tilt0, c.tilt1, drift) + wob,
      Htot: lerp(c.Htot0, c.Htot1, cond),
      wTip: lerp(c.wTip0, c.wTip1, cond),
      wmax: lerp(c.wmax0, c.wmax1, cond),
      cen: lerp(c.cen0, 9.5, cond),
      m,
      dark: cond,
    };
  }

  function drawChromosome(ctx, i, ps) {
    const c = CHROMO[i];
    const col = PAIR[c.pair];
    const cs = Math.cos(ps.rot), sn = Math.sin(ps.rot);
    const to = (q) => [ps.x + q[0] * cs - q[1] * sn, ps.y + q[0] * sn + q[1] * cs];
    const fill = L.mix(col.base, col.deep, 0.08 + 0.26 * ps.dark);
    const lit = L.mix(col.base, P.white, 0.45);
    for (let side = -1; side <= 1; side += 2) {
      const cd = chromatid(ps, side);
      const poly = cd.poly.map(to);
      const mid = cd.mid.map(to);
      L.inkPath(ctx, poly, { closed: true, width: 2.6, color: col.deep, fill, seed: sd('rodInk', c.id, side), wobble: 0.8, step: 3, overlap: 8 });
      L.hatch(ctx, poly, {
        angle: -30 * DEG, spacing: lerp(6, 4.6, ps.dark), width: 1.2, color: col.deep, alpha: 0.75,
        length: [8, 26], gap: [3, 7], inset: 2, seed: sd('rodHatch', c.id, side),
        density: (px, py) => sstep(-0.4, 0.8, ((px - ps.x) + (py - ps.y)) / (ps.Htot * 1.1)),
      });
      // banding: short cross ticks along the copy (07 draws the same ones in lattice weight)
      ctx.save();
      clipPoly(ctx, poly);
      for (let j = 4; j < mid.length - 4; j += 4) {
        const a = mid[j - 1], b = mid[j + 1];
        let dx = b[0] - a[0], dy = b[1] - a[1];
        const dl = Math.hypot(dx, dy) || 1;
        dx /= dl;
        dy /= dl;
        const w = cd.hws[j] + 1.4;
        L.inkPath(ctx, [[mid[j][0] + dy * w, mid[j][1] - dx * w], [mid[j][0] - dy * w, mid[j][1] + dx * w]], {
          width: 2.2, color: col.deep, alpha: 0.3 + 0.22 * ps.dark, smooth: false, taper: [2, 2], wobble: 0.5,
          seed: sd('band', c.id, side, j),
        });
      }
      ctx.restore();
      // the identity line down the middle, and a lit edge on the side the light comes from
      L.inkPath(ctx, mid.slice(3, mid.length - 3), {
        width: 1.2, color: P.inkFaint, alpha: 0.42, seed: sd('rodMid', c.id, side), taper: [10, 10], wobble: 0.5,
      });
      const litPts = [];
      for (let j = 3; j < mid.length - 3; j++) {
        const a = mid[Math.max(0, j - 1)], b = mid[Math.min(mid.length - 1, j + 1)];
        let dx = b[0] - a[0], dy = b[1] - a[1];
        const dl = Math.hypot(dx, dy) || 1;
        dx /= dl;
        dy /= dl;
        const s2 = -dy - dx < 0 ? 1 : -1; // the upper-left flank of this rod
        const w = cd.hws[j] * 0.62;
        litPts.push([mid[j][0] + s2 * dy * w, mid[j][1] - s2 * dx * w]);
      }
      L.inkPath(ctx, litPts.slice(0, Math.ceil(litPts.length * 0.55)), {
        width: 1.8, color: lit, alpha: 0.5, seed: sd('rodLit', c.id, side), taper: [8, 14],
      });
    }
    // the centromere: the disc the two identical copies are joined at
    L.inkCircle(ctx, ps.x, ps.y, ps.cen, { width: 1.8, color: P.ink, fill: P.centromere, seed: sd('cen', c.id), wobble: 0.5 });
  }

  // ---------------------------------------------------------------------------
  // 6. The nuclear envelope, intact and then in 24 pieces
  // ---------------------------------------------------------------------------

  function drawEnvelope(ctx, t, tw) {
    if (t < B_HINGE - EPS) {
      // one continuous membrane: the same 24 arcs, laid end to end
      for (let i = 0; i < DASHES.length; i++) {
        const d = DASHES[i];
        const pts = d.pts.map((p) => [CX + p[0], CY + p[1]]);
        L.inkPath(ctx, pts, { width: 4, color: P.nucleusRim, seed: d.seed, taper: [2, 2], minWidth: 0.85, wobble: 0.9, swell: 0.05 });
      }
      return;
    }
    // the burst: out 40 px over 6 frames with outExpo, a slower slide after, fading over 12 frames
    for (let i = 0; i < DASHES.length; i++) {
      const d = DASHES[i];
      const tt = tw - B_HINGE - d.lag;
      const a = 1 - clamp(tt / (12 * FR) + 1 / 12);
      if (a <= 0.01) continue;
      const u = clamp(tt / (6 * FR) + 1 / 6);
      const out = 40 * E.outExpo(u) * d.rate + 58 * E.outCubic(clamp((tt - 4 * FR) / (11 * FR)));
      const sp = d.spin * E.outCubic(clamp(tt / (9 * FR)));
      const slip = d.side * out;
      const ca = Math.cos(d.am), sa = Math.sin(d.am);
      const cs = Math.cos(sp), sn = Math.sin(sp);
      // the piece keeps its own shape: rotate about its middle, then push along the normal
      const mx = Math.cos(d.am) * nucR(d.am), my = Math.sin(d.am) * nucR(d.am);
      const pts = d.pts.map((p) => {
        const lx = p[0] - mx, ly = p[1] - my;
        return [
          CX + mx + lx * cs - ly * sn + ca * out - sa * slip,
          CY + my + lx * sn + ly * cs + sa * out + ca * slip,
        ];
      });
      L.inkPath(ctx, pts, {
        width: lerp(3.4, 5, a), color: P.membraneDash, alpha: a, seed: d.seed,
        taper: [4, 4], minWidth: 0.6, wobble: 1.2,
      });
    }
  }

  // ---------------------------------------------------------------------------
  // 7. The poles (centrosomes) at the G3 positions
  // ---------------------------------------------------------------------------

  function drawPole(ctx, px, py, k, appear) {
    if (appear <= 0.01) return;
    ctx.save();
    ctx.globalAlpha *= 0.2 + 0.8 * appear;
    const r = 22 * (0.55 + 0.45 * appear);
    L.guideCircle(ctx, px, py, 52 * appear, { color: P.inkFaint, alpha: 0.45, width: 1.3, dash: [6, 8] });
    L.ticks(ctx, px, py, { r: r + 7, n: 12, len: 17, color: P.inkSoft, alpha: 0.8, width: 2, p: appear });
    L.inkCircle(ctx, px, py, r, { width: 2.6, color: P.inkSoft, fill: P.pole, seed: sd('pole', k), wobble: 0.8 });
    L.hatch(ctx, L.ellipsePts(px, py, r, r, 24), {
      angle: -Math.PI / 4, spacing: 5, width: 1.2, color: P.mitoDeep, alpha: 0.7, length: [5, 13], gap: [2, 5], inset: 2,
      seed: sd('poleHatch', k),
      density: (x, y) => sstep(-0.2, 0.8, ((x - px) + (y - py)) / (r * 1.4)),
    });
    dot(ctx, px - r * 0.34, py - r * 0.34, r * 0.2, P.white, 0.4);
    ctx.restore();
  }

  // ---------------------------------------------------------------------------
  // 8. Overlays
  // ---------------------------------------------------------------------------

  function drawOverlays(ctx, t, tw, drift, appear, poses) {
    // the one label: a bracket round the nucleus, fading once the nucleus has gone
    const labAlpha = 1 - sstep(0.9, 1.4, t);
    if (labAlpha > 0.01) {
      ctx.save();
      ctx.globalAlpha *= labAlpha;
      L.bracket(ctx, CX - R_NUC, 690, CX + R_NUC, 690, {
        cap: 26, color: P.annYellow, alpha: 1, width: 3, label: 'nucleus', labelSize: 34,
      });
      ctx.restore();
    }
    // where the nucleus was: a dotted ring that fades with it
    if (t >= B_HINGE - EPS) {
      const u = clamp((t - B_HINGE) / (16 * FR));
      ring(ctx, CX, CY, R_NUC * (1 + 0.07 * u), P.annBlue, 2.5, 0.95 * (1 - u), [3, 13]);
    }
    // the hinge: a change ring and an attention ring off the breaking envelope
    if (t >= B_HINGE - EPS) {
      const um = clamp((t - B_HINGE) / (8 * FR) + 1 / 8);
      if (um < 1) ring(ctx, CX, CY, R_NUC * 0.85 + 400 * E.outExpo(um), P.annMagenta, 3, 1 - Math.pow(um, 0.75));
      const uy = clamp((t - B_HINGE - FR) / (10 * FR) + 0.1);
      if (uy > 0 && uy < 1) ring(ctx, CX, CY, 110 + 430 * E.outExpo(uy), P.annYellow, 3, 1 - uy);
    }
    // the poles arriving
    if (appear > 0) {
      const u = clamp((t - B_COND) / (6 * FR) + 1 / 6);
      if (u < 1) {
        for (const p of [POLE_TOP, POLE_BOT]) ring(ctx, p[0], p[1], 20 + 62 * E.outExpo(u), P.annYellow, 3, 1 - u);
      }
    }
    // the metaphase plate and the drift to it
    if (t >= B_DRIFT - EPS) {
      const u = E.outExpo(clamp((t - B_DRIFT) / (6 * FR) + 1 / 6));
      const seg = 140 * u;
      strokePts(ctx, [[390 - seg, PLATE_Y], [390, PLATE_Y]], P.annBlue, 2.5, 0.9, [14, 10]);
      strokePts(ctx, [[690, PLATE_Y], [690 + seg, PLATE_Y]], P.annBlue, 2.5, 0.9, [14, 10]);
      for (let i = 0; i < CHROMO.length; i++) {
        const c = CHROMO[i], ps = poses[i];
        // a trajectory drawn on behind each chromosome, and the mark on the plate it is heading for
        if (drift > 0.02 && drift < 0.999) strokePts(ctx, [[c.x0, c.y0], [ps.x, ps.y]], P.annBlue, 2.5, 0.85, [12, 9]);
        strokePts(ctx, [[c.x1, PLATE_Y - 16 * u], [c.x1, PLATE_Y + 16 * u]], P.annBlue, 2, 0.75);
        // it gathers near the line but has not reached it: a short leader closes the last of the gap
        if (drift > 0.995) {
          ring(ctx, ps.x, ps.y, 12.5, P.annBlue, 2, 0.9);
          strokePts(ctx, [[ps.x, ps.y + Math.sign(PLATE_Y - ps.y) * (ps.cen + 6)], [ps.x, PLATE_Y]], P.annBlue, 2, 0.7, [5, 6]);
        }
      }
    }
  }

  // ---------------------------------------------------------------------------
  // The shot
  // ---------------------------------------------------------------------------

  FILM.scene({
    id: ID,
    draw(ctx, tIn, info) {
      const t = clamp(tIn, 0, info.dur); // a transition may ask past the end: hold the last pose
      const Tg = info.shot.start + t;
      const tw = L.onTwos(t);

      // --- timing -----------------------------------------------------------
      // the drift and the stretch both finish on the last drawing, so the final frames hold the
      // exact G3 pose 07 cuts onto
      const drift = E.inOutCubic(clamp((tw - B_DRIFT + TW) / 0.5));
      const elong = E.inOutCubic(clamp((t - T_ELONG) / (T_LAND - T_ELONG)));
      const appear = t < B_COND - EPS ? 0 : E.outExpo(clamp((t - B_COND) / (8 * FR) + 1 / 8));
      const tent = 56 * appear * (1 - elong);
      const rx = lerp(R_CELL, RX_G3, elong);
      const ry = lerp(R_CELL, RY_G3, elong);
      const nucAlpha = 1 - clamp((t - B_HINGE) / (10 * FR));
      const nucFlash = t < B_HINGE - EPS ? 0 : [0.55, 0.22, 0][Math.min(2, Math.floor((tw - B_HINGE) * 12 + EPS))];

      const cell = cellPts(rx, ry, tent);
      const cellSmooth = L.smoothPts(cell, true, 10);
      const poses = [];
      for (let i = 0; i < CHROMO.length; i++) poses.push(chromoPose(i, t, tw, drift));

      // --- 1. plate ---------------------------------------------------------
      drawBackground(ctx, Tg);

      // --- 2. construction --------------------------------------------------
      drawConstruction(ctx, t, elong, ry);

      // --- 3. the cell's contents ------------------------------------------
      ctx.save();
      clipPoly(ctx, cellSmooth);
      drawCytoplasm(ctx, cellSmooth, rx / R_CELL, ry / R_CELL, nucAlpha);

      // --- 4. the nucleus ---------------------------------------------------
      drawNucleus(ctx, t, tw, nucAlpha, nucFlash);
      drawNucleolus(ctx, t, tw, Math.max(nucAlpha, t >= B_HINGE ? 1 - clamp((tw - B_HINGE) / (12 * FR)) : 0));

      // --- 5. the chromosomes ----------------------------------------------
      for (let i = 0; i < CHROMO.length; i++) drawChromosome(ctx, i, poses[i]);

      // --- 6. the nuclear envelope -----------------------------------------
      drawEnvelope(ctx, t, tw);
      ctx.restore();

      // --- 7. the membrane, then the poles ---------------------------------
      L.inkPath(ctx, cell, {
        closed: true, width: 6, color: P.membrane, seed: sd01('membrane'), step: 4, wobble: 1.6, overlap: 26,
        double: { offset: -9, width: 0.25, alpha: 0.4, from: 0.08, to: 0.62 },
      });
      drawPole(ctx, POLE_TOP[0], POLE_TOP[1], 0, appear);
      drawPole(ctx, POLE_BOT[0], POLE_BOT[1], 1, appear);

      // --- 8. overlays ------------------------------------------------------
      drawOverlays(ctx, t, tw, drift, appear, poses);

      // --- 9. the cycle glyph (G5), always last ----------------------------
      L.cycleGlyph(ctx, info.T, 'illustrated');
    },
  });
})();
