// 08 pull-apart : The copies are pulled apart. Illustrated (paper plate).
// Global T 16.0 to 19.0 — 3.0 s, 72 frames at 24 fps, 120 bpm (a beat is 12 frames).
//
// The whole shot is SCREEN-FIXED: 07 (blueprint) cuts onto frame 0 and 09 (blueprint) cuts onto
// the last frame, so every match-cut number below is a frame pixel and no part of the subject
// rides lib.camera. The storyboard's slow pull (zoom 1.00 to 0.97) is carried by the background
// plate alone — the stripes and the outer construction geometry open out by 3 percent across the
// shot — so the G3 geometry lands exactly on the contract pixels at both ends of the shot and
// neither cut jumps.
//
// Layer plan (frame px, back to front):
//   1  paper plate, stripeCream / stripeSky stripes (140 px band, 30 deg, 6 px drift per beat),
//      a paperDeep 45 deg hatch vignette in the top and bottom bands
//   2  construction in inkFaint: the spindle axis x 540, the circle the cell grew out of, a
//      guide ellipse 40 px outside the membrane, the 45 degree diameters, corner brackets, a
//      tick ruler down the right margin, the metaphase-plate leaders on y 900 (fading once the
//      copies leave) and the arrival leaders on y 560 / 1240
//   3  the cell: cytoplasm inside the G3 ellipse (half-width 380, half-height 520 -> 560), rim
//      hatching in cytoHatch, a second layer at 105 deg in the deep shadow, ribosome stipple in
//      inkFaint, the 6 px doubled ink membrane
//   4  the spindle: 10 free fibres fanning to the far side with cross-links where they overlap
//      at the equator, 12 mitochondria, the two poles (22 px hatched pole discs, 12 radial
//      ticks), 8 kinetochore fibres running pole -> centromere and nowhere else
//   5  the chromosomes: four upright X shapes on the plate that split into eight single-arm V
//      copies, two chromoA and two chromoB arriving at each pole (art bible 10.7)
//   6  overlays: annBlue dashed trajectories with a leading arrowhead, annYellow split rings and
//      pole rings, and the annYellow 'spindle' bracket — the shot's one label
//   7  the cycle glyph, lib.cycleGlyph(ctx, info.T, 'illustrated'), copied verbatim
//
// Shared geometry (docs/storyboard.md, G3), all screen-fixed:
//   poles (540, 430) and (540, 1370), moving to (540, 400) and (540, 1400) from T 18.0
//   plate y 900; metaphase centres x 400 (A1), 495 (B1), 585 (B2), 680 (A2), arms vertical
//   arrival (copied from 09's frame-0 SET table, not derived): each copy is a single-arm V with
//            its centromere at the apex — pair A at x 470 and 610 with the centromere on y 482
//            (upper set) and y 1246 (lower), pair B at x 480 and 600 on y 566 and y 1302, arms
//            running (40, 84) for A and (26, 56) for B from the centromere to each tip, rods 24
//            and 20 px thick. The sets stay centred on y 560 and y 1240.
//   the cell outline elongates from half-height 520 to 560; the half-width stays 380
//
// Timing, by drawing index d = onTwos(t) * 12 (everything drawn as an object moves on twos;
// overlays, ring expansion and draw-on progress run at the full 24 fps):
//   d 0      T 16.000  G3 metaphase pose, fully drawn: four X chromosomes upright on the plate,
//                      both poles, 18 fibres bowed by 13 px of slack, the bracket fading in
//   d 6      T 16.500  the fibres tighten to 2 px of slack over 3 drawings and each centromere
//                      splits into two inkSoft discs 10 px apart, with an annYellow ring each
//   d 12     T 17.000  the copies separate: every X becomes two single-arm chromosomes that
//                      travel to opposite poles centromere first, the arms swinging back into a
//                      trailing V; annBlue trajectories draw on behind them
//   d 24     T 18.000  the cell elongates further (545 -> 560) and the poles move out to
//                      (540, 400) and (540, 1400)
//   d 30     T 18.500  the sets land on the G3 end positions; two annYellow rings pulse at the
//                      poles and the trajectories fade out
//   d 30-35  T 18.5 to 19.0  held, so 09 cuts onto a still frame
(function () {
  'use strict';

  const ID = 'pull-apart';
  // the spindle geometry is handed over from 07, so its wobble seeds come from that shot's id
  const REF = 'spindle-blueprint';
  const LIB = FILM.lib;
  const E = LIB.ease;
  const TAU = Math.PI * 2;
  const DEG = Math.PI / 180;
  const FR = 1 / 24;

  // local copy of the palette: reading through the frozen proxy in a hot loop costs
  const P = {};
  for (const k of Object.keys(LIB.pal)) P[k] = LIB.pal[k];

  const lerp = (a, b, u) => a + (b - a) * u;
  const clamp = (v, lo = 0, hi = 1) => (v < lo ? lo : v > hi ? hi : v);
  const sstep = (a, b, x) => {
    const u = clamp((x - a) / (b - a));
    return u * u * (3 - 2 * u);
  };
  const hyp = Math.hypot;

  // every seed in the file derives from the shot id; shared geometry from the handover shot's id
  const sd = (...k) => LIB.hash(ID, ...k) & 0x7fffffff;
  const rd = (...k) => LIB.hash(REF, ...k) & 0x7fffffff;

  // =====================================================================================
  // Shared geometry constants (docs/storyboard.md, "Shared geometry", G1, G3 and G5)
  // =====================================================================================

  const CX = 540;          // the spindle axis
  const CY = 900;          // the metaphase plate and the cell's centre
  const HW = 380;          // cell half-width, constant through 07 and 08
  const HH_0 = 520;        // cell half-height at T 16.0 (the pose 07 hands over)
  const HH_1 = 560;        // cell half-height from T 18.5 (the pose 09 takes)
  const POLE_A = 430;      // top pole at T 16.0 (the bottom pole mirrors about CY)
  const POLE_B = 400;      // top pole from T 18.5

  // beats, in local seconds (the global T is in the comment)
  const B_TIGHT = 0.5;     // T 16.5  fibres tighten, centromeres split
  const B_SPLIT = 1.0;     // T 17.0  the copies separate and start travelling
  const B_ELONG = 2.0;     // T 18.0  the cell elongates further, the poles move out
  const B_LAND = 2.5;      // T 18.5  the sets arrive, the pole rings pulse
  const TRAVEL = B_LAND - B_SPLIT; // 1.5 s = 18 drawings

  // The four chromosomes. x is the metaphase centre on the plate; ex is the arrival x (G3: A at
  // 470 and 610, B at 480 and 600). eyU and eyL are where the CENTROMERE of the copy at the top
  // and the bottom pole comes to rest, read straight off 09's frame-0 table (its SET rows staggered
  // -36 / +34 about the set centres y 560 and y 1240, with the apex vh px ahead of each row's
  // centre): A leads its set, B follows it, and the lower set is 09's table with its apex flipped,
  // not a mirror of the upper one. 09 cuts onto these pixels, so they are copied, not derived.
  const CHROMO = [
    { kind: 'A', x: 400, ex: 470, eyU: 482, eyL: 1246 },
    { kind: 'B', x: 495, ex: 480, eyU: 566, eyL: 1302 },
    { kind: 'B', x: 585, ex: 600, eyU: 566, eyL: 1302 },
    { kind: 'A', x: 680, ex: 610, eyU: 482, eyL: 1246 },
  ];

  // Chromosome sizes. At metaphase (G2) chromoA is 150 px tall and chromoB 100 px, each an X of
  // two identical copies joined at the centromere; tip is the sideways reach of an arm tip and w
  // the rod thickness, so an A reads 150 x 76 and a B 100 x 64 — a clear gap between neighbours
  // on the plate. On arrival each single-arm copy takes 09's V exactly: half-width vw and apex
  // vh ahead of its row centre, so an arm runs (vw, 2 vh) from the centromere to each tip. The
  // arms lengthen a little as the copy pulls free of its sister, which is what lets both ends of
  // the shot sit on their contract pixels.
  const DIM = {
    A: { h: 150, tip: 26, w: 24, vw: 40, vh: 42, col: 'chromoA', deep: 'chromoADeep' },
    B: { h: 100, tip: 22, w: 20, vw: 26, vh: 28, col: 'chromoB', deep: 'chromoBDeep' },
  };
  for (const k of Object.keys(DIM)) {
    const d = DIM[k];
    d.La0 = hyp(d.h / 2, d.tip);             // arm length at metaphase, centromere to tip
    d.th0 = Math.atan2(d.h / 2, d.tip);      // half-angle at metaphase: the arms stand near vertical
    d.La1 = hyp(d.vw, 2 * d.vh);             // arm length on arrival (09's V)
    d.th1 = Math.atan2(d.vw, 2 * d.vh);      // half-angle of the trailing V on arrival
  }

  // Mitochondria (art bible 10.1: beans with folded inner ridges), authored on the FINAL cell
  // (half-height 560) and carried inward in y while the cell is shorter, so nothing drifts into
  // an arriving chromosome. They keep out of the travel corridor and off the bracket's lane.
  const MITO = [
    [255, 665, -0.5], [215, 850, 0.12], [225, 1060, -0.38], [330, 1270, 0.46],
    [360, 480, 0.28], [270, 1200, 0.62], [790, 690, -0.62], [850, 900, 0.18],
    [805, 1085, -0.5], [715, 1300, 0.34], [730, 520, -0.26], [420, 1345, 0.7],
  ];

  // The 10 free fibres: five from each pole, fanning past the plate to the far side of the cell
  // (G3). Each entry is the lateral offset of the far end from the axis and the fraction of the
  // half-height it reaches, so they stretch as the cell elongates.
  const FREE_A = [[-236, 0.78], [-128, 0.84], [-18, 0.86], [126, 0.83], [240, 0.76]];
  const FREE_B = [[-218, 0.77], [-112, 0.85], [22, 0.86], [134, 0.82], [228, 0.75]];

  // the bracket lane: the one label lives here, clear of the membrane, the fibres and the beans
  const BR_X = 300, BR_Y0 = 1160, BR_Y1 = 620;

  // =====================================================================================
  // Memoized geometry (t-independent and seeded, built once)
  // =====================================================================================

  let GEO = null;
  function geo() {
    if (GEO) return GEO;
    // The membrane's hand-drawn irregularity: the G1 rule (radius + 14 * noise) carried onto the
    // elongated ellipse and seeded from 07, so the shape the blueprint left is the shape the ink
    // finds. The wobble is stored once; the half-height is applied at draw time.
    const N = 44;
    const wob = new Float64Array(N);
    const s0 = rd('outline'), s1 = rd('outline', 2);
    for (let i = 0; i < N; i++) {
      const a = (i / N) * TAU;
      wob[i] = 14 * (0.68 * LIB.noise1(Math.cos(a) * 2.1 + Math.sin(a) * 1.3 + 3.7, s0)
        + 0.32 * LIB.noise1(i * 0.91, s1));
    }
    GEO = { N, wob };
    return GEO;
  }

  /** The cell outline for a given half-height: 44 seeded points ready for smoothing or inking. */
  function cellPts(hh) {
    const g = geo();
    const out = [];
    for (let i = 0; i < g.N; i++) {
      const a = (i / g.N) * TAU;
      const w = g.wob[i];
      out.push([CX + (HW + w) * Math.cos(a), CY + (hh + w * 1.15) * Math.sin(a)]);
    }
    return out;
  }

  /** Normalised radius inside the cell: 0 at the centre, 1 on the membrane. */
  const cellQ = (x, y, hh) => hyp((x - CX) / HW, (y - CY) / hh);

  // =====================================================================================
  // Small drawing helpers
  // =====================================================================================

  /** A plain stroked path in one colour: construction lines, ticks and rulers. */
  function stroke(ctx, fn, color, alpha, width, dash) {
    if (alpha <= 0.004) return;
    ctx.save();
    ctx.strokeStyle = color;
    ctx.globalAlpha *= alpha;
    ctx.lineWidth = width;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    if (dash) ctx.setLineDash(dash);
    ctx.beginPath();
    fn(ctx);
    ctx.stroke();
    ctx.restore();
  }

  /** Half a circle of points from angle a0 sweeping -PI: the rounded cap on a rod end. */
  function capArc(px, py, a0, r, n) {
    const out = [];
    for (let k = 1; k < n; k++) {
      const a = a0 - (k / n) * Math.PI;
      out.push([px + Math.cos(a) * r, py + Math.sin(a) * r]);
    }
    return out;
  }

  /**
   * A rounded rod around a centreline: offsets the line by hwAt(u) on both sides and closes it
   * with a semicircular cap at each end. Returns a closed polygon ready for fill, hatch and ink.
   */
  function ribbonPoly(pts, hwAt) {
    const n = pts.length;
    const nx = new Float64Array(n), ny = new Float64Array(n), hw = new Float64Array(n);
    for (let i = 0; i < n; i++) {
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1];
      const tl = hyp(tx, ty) || 1;
      tx /= tl;
      ty /= tl;
      nx[i] = -ty;
      ny[i] = tx;
      hw[i] = hwAt(n === 1 ? 0 : i / (n - 1));
    }
    const left = [], right = [];
    for (let i = 0; i < n; i++) {
      left.push([pts[i][0] + nx[i] * hw[i], pts[i][1] + ny[i] * hw[i]]);
      right.push([pts[i][0] - nx[i] * hw[i], pts[i][1] - ny[i] * hw[i]]);
    }
    const e = n - 1;
    const endCap = capArc(pts[e][0], pts[e][1], Math.atan2(ny[e], nx[e]), hw[e], 7);
    const startCap = capArc(pts[0][0], pts[0][1], Math.atan2(ny[0], nx[0]) + Math.PI, hw[0], 7);
    return left.concat(endCap, right.reverse(), startCap);
  }

  /**
   * One spindle fibre: a slightly wavy line from (x0, y0) to (x1, y1), bowed sideways by `slack`
   * and given a seeded shiver so the fibres never read as ruled lines.
   */
  function fibrePts(x0, y0, x1, y1, slack, side, seed, bi) {
    const dx = x1 - x0, dy = y1 - y0;
    const L = hyp(dx, dy) || 1;
    const px = -dy / L, py = dx / L;
    const n = 11;
    const out = [];
    for (let i = 0; i <= n; i++) {
      const u = i / n;
      const env = Math.sin(Math.PI * u);
      const b = side * slack * env
        + 1.9 * env * LIB.noise1(u * 3.4 + 1.7, seed)
        + 0.8 * env * LIB.noise1(u * 8.1, seed + bi * 13 + 5);
      out.push([x0 + dx * u + px * b, y0 + dy * u + py * b]);
    }
    return out;
  }

  // =====================================================================================
  // The chromatid: a V of two arms meeting at the centromere
  // =====================================================================================
  //
  // At metaphase the half-angle is about 71 degrees for chromoA, so the two arms stand almost
  // vertical and the chromatid reads as the left (or right) half of an upright X. As the copy is
  // pulled to its pole the axis swings 90 degrees and the half-angle closes to 26 degrees, so the
  // centromere leads and the two arms trail behind it in a V (storyboard 08, T 17.0).

  /** Geometry of one chromatid from its state: centreline, outline polygon and arm directions. */
  function chromatidGeo(st) {
    const a1 = st.axis - st.theta, a2 = st.axis + st.theta;
    const bx = Math.cos(st.axis) * st.bow, by = Math.sin(st.axis) * st.bow;
    const tip1 = [st.x + Math.cos(a1) * st.La, st.y + Math.sin(a1) * st.La];
    const tip2 = [st.x + Math.cos(a2) * st.La, st.y + Math.sin(a2) * st.La];
    const m1 = [st.x + Math.cos(a1) * st.La * 0.56 + bx, st.y + Math.sin(a1) * st.La * 0.56 + by];
    const m2 = [st.x + Math.cos(a2) * st.La * 0.56 + bx, st.y + Math.sin(a2) * st.La * 0.56 + by];
    const line = LIB.smoothPts([tip1, m1, [st.x, st.y], m2, tip2], false, 4);
    const half = st.w / 2;
    // A waist at the centromere while the two sisters are still joined there, opening out to a
    // full-width centromere once the copy is free — which is the silhouette 09 takes over.
    const waist = st.waist;
    const hwAt = (u) => {
      const d = Math.abs(u - 0.5) * 2;
      return half * (waist + (1 - waist) * sstep(0, 0.44, d)) * (1 - 0.24 * sstep(0.78, 1, d));
    };
    return { line, poly: ribbonPoly(line, hwAt), tip1, tip2, a1, a2 };
  }

  /**
   * The state of one chromatid at drawing time tw.
   *   i   which chromosome (0..3)
   *   s   0 = the copy that leaves for the TOP pole, 1 = the copy for the BOTTOM pole
   *   hs  half the separation of the two centromere discs (2 before T 16.5, 5 after)
   */
  function chromatidState(i, s, tw, hs) {
    const C = CHROMO[i];
    const D = DIM[C.kind];
    const sgn = s ? 1 : -1;
    const sx = C.x + sgn * hs;
    const sy = CY;
    const ex = C.ex;
    const ey = s ? C.eyL : C.eyU;
    const uu = clamp((tw - B_SPLIT) / TRAVEL);
    // the split cracks open on the beat, then the copy glides the rest of the way with inOutCubic
    const u = 0.24 * E.outCubic(uu * 3.4) + 0.76 * E.inOutCubic(uu);
    // The re-orientation waits one drawing: the X first cracks cleanly into its two halves, still
    // in the metaphase pose, and only then do the arms swing back. Swinging them while the halves
    // still overlap reads as two interlocked zigzags, not as a chromosome being pulled.
    const ua = E.outCubic(clamp((uu - 0.055) * 4.4));
    // the arms sweep hardest early, when the copy is being yanked clear of its sister, and settle
    // back onto 09's half-angle exactly at the end
    let theta = lerp(D.th0, D.th1, ua) - 14 * DEG * Math.sin(Math.PI * Math.pow(clamp(uu), 0.6));
    if (theta < 11 * DEG) theta = 11 * DEG;
    return {
      kind: C.kind,
      i, s,
      x: lerp(sx, ex, u),
      y: lerp(sy, ey, u),
      sx, sy, ex, ey,
      // s = 0: PI -> PI/2, arms trailing below a copy climbing to the top pole
      // s = 1: 0  -> -PI/2, arms trailing above a copy falling to the bottom pole
      axis: (s ? 0 : Math.PI) - (Math.PI / 2) * ua,
      theta,
      La: lerp(D.La0, D.La1, E.inOutSine(uu)),
      w: D.w,
      waist: lerp(0.58, 0.92, ua),
      bow: 11 * Math.sin(Math.PI * clamp(uu * 1.1)),
      u: uu,
      moving: uu > 0 && uu < 1,
      dir: s ? 1 : -1,
    };
  }

  // =====================================================================================
  // Background
  // =====================================================================================

  function drawBackground(ctx, T, pull) {
    LIB.paper(ctx, { seed: sd('paper') % 9973 });
    ctx.save();
    ctx.globalAlpha = 0.88;
    // stripes drift 6 px along their normal per beat and open out with the background pull
    LIB.stripes(ctx, {
      colors: [P.stripeCream, P.stripeSky],
      width: 140 * pull,
      angle: -0.52,
      offset: 12 * T,
      wobble: 1.6,
      seed: sd('stripes') % 9973,
    });
    ctx.restore();
    // the bottom band sits under the Shorts title row: a paperDeep hatch vignette fading upward
    LIB.hatch(ctx, null, {
      bounds: { x: -30, y: 1540, w: 1140, h: 410 },
      angle: -Math.PI / 4,
      spacing: 8,
      width: 1.7,
      color: P.paperDeep,
      alpha: 0.26,
      length: [18, 60],
      gap: [3, 9],
      seed: sd('vign', 1),
      density: (x, y) => sstep(1560, 1880, y),
    });
    // a lighter one under the top bar
    LIB.hatch(ctx, null, {
      bounds: { x: -30, y: -20, w: 1140, h: 250 },
      angle: -Math.PI / 4,
      spacing: 10,
      width: 1.5,
      color: P.paperDeep,
      alpha: 0.2,
      length: [14, 46],
      gap: [4, 12],
      seed: sd('vign', 2),
      density: (x, y) => 1 - sstep(10, 215, y),
    });
  }

  // =====================================================================================
  // Construction geometry (inkFaint, about 1.5 px at 20 to 50 percent — art bible 3.1)
  // =====================================================================================

  function drawConstruction(ctx, t, hh, pyT, pyB, pull) {
    const k = pull; // the construction plate opens out with the background pull
    const SX = (x) => CX + (x - CX) * k;
    const SY = (y) => CY + (y - CY) * k;

    // the spindle axis, broken where the poles and the plate sit
    stroke(ctx, (c) => {
      const gaps = [[pyT - 48, pyT + 48], [pyB - 48, pyB + 48], [CY - 120, CY + 120]];
      let y = 300;
      for (const [a, b] of gaps) {
        c.moveTo(SX(CX), SY(y));
        c.lineTo(SX(CX), SY(a));
        y = b;
      }
      c.moveTo(SX(CX), SY(y));
      c.lineTo(SX(CX), SY(1520));
    }, P.inkFaint, 0.32, 1.5);

    // the 45 degree diameters through the cell's centre, run well past the membrane
    stroke(ctx, (c) => {
      for (const sgn of [-1, 1]) {
        c.moveTo(SX(CX - 680), SY(CY - sgn * 680));
        c.lineTo(SX(CX + 680), SY(CY + sgn * 680));
      }
    }, P.inkFaint, 0.22, 1.5);

    // the circle the cell grew out of, and the guide ellipse 40 px outside the membrane
    LIB.guideCircle(ctx, SX(CX), SY(CY), (HW + 40) * k, { color: P.inkFaint, alpha: 0.2, width: 1.5 });
    ctx.save();
    ctx.translate(CX, CY);
    ctx.scale(1, (hh + 40) / (HW + 40));
    ctx.translate(-CX, -CY);
    LIB.guideCircle(ctx, CX, CY, (HW + 40) * k, { color: P.inkFaint, alpha: 0.3, width: 2.4 });
    ctx.restore();

    // corner brackets round the cell's bounding box
    stroke(ctx, (c) => {
      const x0 = SX(CX - HW - 40), x1 = SX(CX + HW + 40);
      const y0 = SY(CY - hh - 40), y1 = SY(CY + hh + 40);
      const m = 66;
      for (const [ax, ay, dx, dy] of [[x0, y0, 1, 1], [x1, y0, -1, 1], [x0, y1, 1, -1], [x1, y1, -1, -1]]) {
        c.moveTo(ax, ay + dy * m);
        c.lineTo(ax, ay);
        c.lineTo(ax + dx * m, ay);
      }
    }, P.inkFaint, 0.34, 1.5);

    // a tick ruler down the right margin, clear of the cycle glyph, growing with the cell
    stroke(ctx, (c) => {
      const x = SX(975);
      const y0 = SY(CY - hh), y1 = SY(CY + hh);
      c.moveTo(x, y0);
      c.lineTo(x, y1);
      for (let y = Math.ceil(y0 / 40) * 40; y <= y1; y += 40) {
        const major = Math.round(y) % 200 === 0;
        c.moveTo(x, y);
        c.lineTo(x - (major ? 26 : 12), y);
      }
      for (const y of [y0, y1]) {
        c.moveTo(x - 18, y);
        c.lineTo(x + 18, y);
      }
    }, P.inkFaint, 0.42, 1.6);

    // the metaphase plate: leaders on y 900 with 60 px ticks, left open on the subject axis,
    // fading out once the copies are clear of it
    const plate = 1 - sstep(1.15, 1.65, t);
    if (plate > 0.01) {
      stroke(ctx, (c) => {
        for (const [a, b] of [[60, 300], [780, 1020]]) {
          c.moveTo(SX(a), SY(CY));
          c.lineTo(SX(b), SY(CY));
          for (let x = a; x <= b + 0.1; x += 60) {
            c.moveTo(SX(x), SY(CY - 7));
            c.lineTo(SX(x), SY(CY + 7));
          }
        }
        for (const x of [60, 1020]) {
          c.moveTo(SX(x), SY(CY - 16));
          c.lineTo(SX(x), SY(CY + 16));
        }
      }, P.inkFaint, 0.5 * plate, 1.8);
    }

    // the arrival rows: leaders on y 560 and y 1240 drawing in as the sets approach
    const land = sstep(1.7, 2.1, t);
    if (land > 0.01) {
      stroke(ctx, (c) => {
        for (const y of [560, 1240]) {
          for (const [a, b] of [[60, 60 + 170 * land], [1020 - 170 * land, 1020]]) {
            c.moveTo(SX(a), SY(y));
            c.lineTo(SX(b), SY(y));
          }
          c.moveTo(SX(60), SY(y - 13));
          c.lineTo(SX(60), SY(y + 13));
          c.moveTo(SX(1020), SY(y - 13));
          c.lineTo(SX(1020), SY(y + 13));
        }
      }, P.inkFaint, 0.5 * land, 1.8);
    }

    // a dotted ghost of the outline the cell started from, so the elongation reads
    if (hh > HH_0 + 2) {
      const g = geo();
      const ghost = [];
      for (let i = 0; i < g.N; i++) {
        const a = (i / g.N) * TAU;
        const w = g.wob[i];
        ghost.push([SX(CX + (HW + w) * Math.cos(a)), SY(CY + (HH_0 + w * 1.15) * Math.sin(a))]);
      }
      const gp = LIB.smoothPts(ghost, true, 10);
      stroke(ctx, (c) => LIB.tracePath(c, gp, true),
        P.inkFaint, 0.36 * sstep(HH_0 + 2, HH_0 + 16, hh), 1.8, [1.5, 8]);
    }

    // pole construction: a faint ring and a crosshair at each centrosome
    for (const py of [pyT, pyB]) {
      stroke(ctx, (c) => {
        c.moveTo(SX(CX) + 40 * k, SY(py));
        c.arc(SX(CX), SY(py), 40 * k, 0, TAU);
        c.moveTo(SX(CX) - 58 * k, SY(py));
        c.lineTo(SX(CX) - 46 * k, SY(py));
        c.moveTo(SX(CX) + 46 * k, SY(py));
        c.lineTo(SX(CX) + 58 * k, SY(py));
      }, P.inkFaint, 0.34, 1.5);
    }
  }

  // =====================================================================================
  // The cell
  // =====================================================================================

  function drawCell(ctx, hh) {
    const raw = cellPts(hh);
    const poly = LIB.smoothPts(raw, true, 9);

    // 1 cytoplasm, flat colour
    ctx.save();
    ctx.fillStyle = P.cytoplasm;
    ctx.beginPath();
    LIB.tracePath(ctx, poly, true);
    ctx.fill();
    ctx.restore();

    // 2 directional hatching near the membrane, heavier on the lower right (light from the upper
    // left, art bible 4.1). The analytic radius keeps it off the per-point polygon test.
    const bnd = { x: CX - HW - 6, y: CY - hh - 6, w: HW * 2 + 12, h: hh * 2 + 12 };
    LIB.hatch(ctx, null, {
      bounds: bnd,
      angle: -Math.PI / 4,
      spacing: 10,
      width: 1.5,
      color: P.cytoHatch,
      alpha: 0.8,
      length: [14, 46],
      gap: [3, 9],
      seed: sd('cyto', 1),
      density: (x, y) => {
        const q = cellQ(x, y, hh);
        if (q > 0.995) return 0;
        const dir = ((x - CX) / HW + (y - CY) / hh) * 0.707;
        return sstep(0.5, 0.96, q) * (0.42 + 0.58 * sstep(-0.4, 0.75, dir));
      },
    });
    // a second pass at 105 degrees in the deep shadow only: tone without a gradient
    LIB.hatch(ctx, null, {
      bounds: bnd,
      angle: -Math.PI / 4 - Math.PI / 3,
      spacing: 13,
      width: 1.3,
      color: P.cytoHatch,
      alpha: 0.62,
      length: [10, 34],
      gap: [4, 11],
      seed: sd('cyto', 2),
      density: (x, y) => {
        const q = cellQ(x, y, hh);
        if (q > 0.99) return 0;
        const dir = ((x - CX) / HW + (y - CY) / hh) * 0.707;
        return sstep(0.64, 0.99, q) * sstep(0.18, 0.9, dir);
      },
    });

    // 3 ribosomes: fine stipple through the cytoplasm, thinner over the spindle so the fibres read
    LIB.stipple(ctx, null, {
      bounds: bnd,
      spacing: 8.4,
      r: [1.0, 2.1],
      color: P.ribosome,
      alpha: 0.55,
      seed: sd('ribo'),
      boilAmp: 0.4,
      density: (x, y) => {
        const q = cellQ(x, y, hh);
        if (q > 0.965) return 0;
        return (0.34 + 0.3 * sstep(0.2, 0.95, q)) * (1 - 0.4 * sstep(0.1, 0.9, 1 - Math.abs(x - CX) / 300));
      },
    });

    return { raw, poly };
  }

  /** The membrane: a 6 px ink line with an occasional doubled retrace (art bible 3.1). */
  function drawMembrane(ctx, raw) {
    LIB.inkPath(ctx, raw, {
      closed: true,
      width: 6,
      color: P.membrane,
      seed: rd('membrane'),
      wobble: 1.8,
      tremble: 0.45,
      boilAmp: 0.6,
      double: { offset: 6, width: 0.26, alpha: 0.4 },
    });
  }

  // =====================================================================================
  // Mitochondria (art bible 10.1: beans with folded inner ridges)
  // =====================================================================================

  function beanPts(len, wid, bend, n) {
    const base = LIB.ellipsePts(0, 0, len / 2, wid / 2, n);
    const out = [];
    for (const [x, y] of base) {
      const u = x / (len / 2);
      out.push([x, y + bend * (1 - u * u)]);
    }
    return out;
  }

  function drawMito(ctx, x, y, rot, idx) {
    const len = 60, wid = 28;
    const r = LIB.rng(sd('mito', idx));
    const bend = r.range(-6, 6);
    const local = beanPts(len, wid, bend, 34);
    const cs = Math.cos(rot), sn = Math.sin(rot);
    const pts = local.map(([px, py]) => [x + px * cs - py * sn, y + px * sn + py * cs]);

    ctx.save();
    ctx.fillStyle = P.mito;
    ctx.beginPath();
    LIB.tracePath(ctx, pts, true);
    ctx.fill();
    ctx.restore();

    // cristae: folded ridges across the short axis, drawn from the upper edge inward
    ctx.save();
    ctx.beginPath();
    LIB.tracePath(ctx, pts, true);
    ctx.clip();
    const rp = new Path2D();
    for (let i = 0; i < 5; i++) {
      const u = -0.62 + (i / 4) * 1.24;
      const px = (u * len) / 2;
      const py0 = -wid / 2 + bend * (1 - u * u) + 1;
      const py1 = wid / 2 + bend * (1 - u * u) - 1;
      const sw = r.range(-5, 5);
      const a = [x + px * cs - py0 * sn, y + px * sn + py0 * cs];
      const b = [x + (px + sw) * cs - py1 * 0.55 * sn, y + (px + sw) * sn + py1 * 0.55 * cs];
      const m = [x + (px + sw * 1.7) * cs, y + (px + sw * 1.7) * sn];
      rp.moveTo(a[0], a[1]);
      rp.quadraticCurveTo(m[0], m[1], b[0], b[1]);
    }
    ctx.strokeStyle = P.mitoDeep;
    ctx.globalAlpha = 0.85;
    ctx.lineWidth = 1.8;
    ctx.lineCap = 'round';
    ctx.stroke(rp);
    ctx.restore();

    // the shadow side
    LIB.hatch(ctx, pts, {
      angle: -Math.PI / 4,
      spacing: 5,
      width: 1.2,
      color: P.mitoDeep,
      alpha: 0.7,
      length: [5, 16],
      gap: [2, 5],
      inset: 2,
      overshoot: 2,
      seed: sd('mitohatch', idx),
      density: (px, py) => clamp(((px - x) + (py - y)) / 34 + 0.35),
    });
    LIB.inkPath(ctx, pts, {
      closed: true,
      width: 2.4,
      color: P.ink,
      seed: sd('mitoink', idx),
      wobble: 0.7,
      tremble: 0.25,
    });
  }

  // =====================================================================================
  // Poles (centrosomes): a 22 px hatched disc with 12 radial ticks (G3)
  // =====================================================================================

  function drawPole(ctx, x, y, idx) {
    const disc = LIB.ellipsePts(x, y, 11, 11, 26);
    stroke(ctx, (c) => {
      for (let i = 0; i < 12; i++) {
        const a = (i / 12) * TAU + (idx ? Math.PI / 12 : 0);
        const l = i % 3 === 0 ? 22 : 15;
        c.moveTo(x + Math.cos(a) * 14, y + Math.sin(a) * 14);
        c.lineTo(x + Math.cos(a) * (14 + l), y + Math.sin(a) * (14 + l));
      }
    }, P.inkSoft, 0.85, 1.9);
    ctx.save();
    ctx.fillStyle = P.pole;
    ctx.beginPath();
    LIB.tracePath(ctx, disc, true);
    ctx.fill();
    ctx.restore();
    LIB.hatch(ctx, disc, {
      angle: -Math.PI / 4,
      spacing: 4,
      width: 1.1,
      color: P.ink,
      alpha: 0.5,
      length: [4, 12],
      gap: [1, 3],
      inset: 1,
      overshoot: 1,
      seed: sd('polehatch', idx),
      density: (px, py) => clamp(((px - x) + (py - y)) / 18 + 0.3),
    });
    // the pair of centrioles inside the centrosome, two short crossed bars
    stroke(ctx, (c) => {
      const a = idx ? 0.5 : -0.7;
      c.moveTo(x + Math.cos(a) * 5, y + Math.sin(a) * 5);
      c.lineTo(x - Math.cos(a) * 5, y - Math.sin(a) * 5);
      const b = a + Math.PI / 2;
      c.moveTo(x + Math.cos(b) * 4 + 2, y + Math.sin(b) * 4);
      c.lineTo(x - Math.cos(b) * 4 + 2, y - Math.sin(b) * 4);
    }, P.inkSoft, 0.8, 2);
    LIB.inkPath(ctx, disc, {
      closed: true,
      width: 2.6,
      color: P.ink,
      seed: sd('poleink', idx),
      wobble: 0.5,
      tremble: 0.2,
    });
  }

  // =====================================================================================
  // Chromosomes
  // =====================================================================================

  function drawChromatid(ctx, st, key) {
    const D = DIM[st.kind];
    const G = chromatidGeo(st);
    const col = P[D.col], deep = P[D.deep];

    // flat colour first: tone comes from hatching, never a gradient
    ctx.save();
    ctx.fillStyle = col;
    ctx.beginPath();
    LIB.tracePath(ctx, G.poly, true);
    ctx.fill();
    ctx.restore();

    // hatching at 30 degrees on the shadow side (as 05)
    LIB.hatch(ctx, G.poly, {
      angle: -30 * DEG,
      spacing: 5.5,
      width: 1.3,
      color: deep,
      alpha: 0.82,
      length: [5, 17],
      gap: [2, 5],
      inset: 2,
      overshoot: 2,
      seed: sd('chhatch', key),
      density: (x, y) => clamp(((x - st.x) + (y - st.y)) / 62 + 0.42),
    });
    // a tighter second layer along the trailing edge while a copy is being pulled
    if (st.moving) {
      const bx = Math.cos(st.axis), by = Math.sin(st.axis);
      LIB.hatch(ctx, G.poly, {
        angle: -30 * DEG - Math.PI / 3,
        spacing: 7,
        width: 1.1,
        color: deep,
        alpha: 0.5,
        length: [4, 12],
        gap: [2, 4],
        inset: 2,
        overshoot: 1,
        seed: sd('chhatch2', key),
        density: (x, y) => clamp((((x - st.x) * bx + (y - st.y) * by) / 55) * 1.2),
      });
    }

    // banding and a faint centre line down each arm
    ctx.save();
    ctx.beginPath();
    LIB.tracePath(ctx, G.poly, true);
    ctx.clip();
    const band = new Path2D();
    for (const a of [G.a1, G.a2]) {
      const ux = Math.cos(a), uy = Math.sin(a);
      const nx = -uy, ny = ux;
      for (const f of [0.34, 0.56, 0.78]) {
        const px = st.x + ux * st.La * f + Math.cos(st.axis) * st.bow * (1 - f);
        const py = st.y + uy * st.La * f + Math.sin(st.axis) * st.bow * (1 - f);
        const h = st.w * 0.46;
        band.moveTo(px - nx * h, py - ny * h);
        band.lineTo(px + nx * h, py + ny * h);
      }
    }
    ctx.strokeStyle = deep;
    ctx.globalAlpha = 0.5;
    ctx.lineWidth = 2.2;
    ctx.lineCap = 'round';
    ctx.stroke(band);
    ctx.restore();

    const n = G.line.length;
    const mid = (n - 1) / 2;
    const spans = [
      [Math.round(mid * 0.14), Math.round(mid * 0.82)],
      [Math.round(mid + (n - 1 - mid) * 0.18), Math.round(mid + (n - 1 - mid) * 0.86)],
    ];
    for (const [a, b] of spans) {
      const seg = G.line.slice(Math.min(a, b), Math.max(a, b) + 1);
      if (seg.length > 2) {
        LIB.inkPath(ctx, seg, {
          width: 1.3,
          color: P.inkFaint,
          alpha: 0.45,
          seed: sd('chline', key, a),
          taper: [5, 9],
          wobble: 0.5,
          swell: 0,
        });
      }
    }

    // the outline
    LIB.inkPath(ctx, G.poly, {
      closed: true,
      width: 3.3,
      color: P.ink,
      seed: sd('chink', key),
      wobble: 0.7,
      tremble: 0.3,
      boilAmp: 0.6,
    });
    return G;
  }

  /** The centromere: an inkSoft disc at the vertex with a thin ink ring (G2). */
  function drawCentromere(ctx, st, key, r) {
    const disc = LIB.ellipsePts(st.x, st.y, r, r, 18);
    ctx.save();
    ctx.fillStyle = P.centromere;
    ctx.beginPath();
    LIB.tracePath(ctx, disc, true);
    ctx.fill();
    ctx.restore();
    LIB.inkPath(ctx, disc, {
      closed: true,
      width: 1.6,
      color: P.ink,
      alpha: 0.85,
      seed: sd('cenink', key),
      wobble: 0.4,
      tremble: 0.15,
    });
  }

  // =====================================================================================
  // Scene
  // =====================================================================================

  FILM.scene({
    id: ID,
    draw(ctx, tIn, info) {
      const L = info.lib;
      const dur = info.dur || 3;
      const t = clamp(tIn, 0, dur);
      const tw = L.onTwos(t);              // characters and objects move on twos
      const T = info.T;
      const bi = L.boil(T);

      // --- timing helpers (docs/reference/scene-anatomy.md) ---
      const drawing = (a) => Math.floor((t - a) * 12 + 1e-6);
      const hit = (a, frames, e, lead = 1) =>
        (t < a - 1e-6 ? 0 : (e || ((u) => u))(clamp((t - a) / (frames * FR) + lead / frames)));
      const popTwos = (a) => (t < a - 1e-6 ? 0 : [0.72, 1.08, 1][Math.min(2, Math.max(0, drawing(a)))]);

      // --- the shot's slow pull, carried by the background plate only ---
      const pull = 1 + 0.03 * E.inOutSine(clamp(t / dur));

      // --- the cell elongates as the fibres pull (art bible 10.5) ---
      const hh = tw < B_SPLIT
        ? HH_0
        : tw < B_ELONG
          ? lerp(HH_0, 545, E.inOutSine(clamp((tw - B_SPLIT) / (B_ELONG - B_SPLIT))))
          : lerp(545, HH_1, E.inOutCubic(clamp((tw - B_ELONG) / (B_LAND - B_ELONG))));

      // --- the poles move out from the T 18.0 beat ---
      const pmove = E.inOutCubic(clamp((tw - B_ELONG) / (B_LAND - B_ELONG)));
      const pyT = lerp(POLE_A, POLE_B, pmove);
      const pyB = 2 * CY - pyT;

      // --- fibre slack: 13 px at the cut, tightening to 2 px over 3 drawings from T 16.5 ---
      const slack = lerp(13, 2, t < B_TIGHT - 1e-6 ? 0 : clamp((drawing(B_TIGHT) + 1) / 3));

      // --- the centromere splits into two discs 10 px apart on the T 16.5 beat ---
      const hs = 2 + 3 * popTwos(B_TIGHT);

      // --- the eight chromatids, far-travelled ones drawn last so they read as nearest ---
      const CH = [];
      for (let i = 0; i < 4; i++) {
        for (let s = 0; s < 2; s++) CH.push(chromatidState(i, s, tw, hs));
      }
      const order = CH.map((st, k) => ({ st, k })).sort((a, b) => Math.abs(a.st.y - CY) - Math.abs(b.st.y - CY));

      // =================================================================================
      // 1 background
      // =================================================================================
      drawBackground(ctx, T, pull);

      // =================================================================================
      // 2 construction
      // =================================================================================
      drawConstruction(ctx, t, hh, pyT, pyB, pull);

      // =================================================================================
      // 3 the cell
      // =================================================================================
      const cell = drawCell(ctx, hh);
      drawMembrane(ctx, cell.raw);

      // =================================================================================
      // 4 the spindle: free fibres, mitochondria, poles, kinetochore fibres
      // =================================================================================

      // free fibres fan from each pole past the plate to the far side (G3)
      const freeEnd = (ox, fy) => [CX + ox, CY + fy * hh];
      const freeFibre = (x0, y0, ox, fy, idx) => {
        const [x1, y1] = freeEnd(ox, fy);
        const pts = fibrePts(x0, y0, x1, y1, slack * 0.75, idx % 2 ? 1 : -1, sd('free', idx), bi);
        LIB.inkPath(ctx, pts, {
          width: 1.7,
          color: P.fibre,
          alpha: 0.48,
          seed: sd('freeink', idx),
          taper: [10, 26],
          wobble: 1.1,
          tremble: 0.35,
          swell: 0,
        });
      };
      FREE_A.forEach(([ox, f], i) => freeFibre(CX, pyT, ox, f, i));
      FREE_B.forEach(([ox, f], i) => freeFibre(CX, pyB, ox, -f, 10 + i));

      // where the two fans overlap at the equator the fibres are cross-linked: short ticks that
      // mark the band the cell will pinch along in 09
      stroke(ctx, (c) => {
        for (let i = 0; i < FREE_A.length; i++) {
          const [ox, f] = FREE_A[i];
          const [x1, y1] = freeEnd(ox, f);
          for (let j = 0; j < 2; j++) {
            const y = CY - 34 + (i * 2 + j) * 13;
            const u = (y - pyT) / (y1 - pyT || 1);
            if (u < 0 || u > 1) continue;
            const x = CX + (x1 - CX) * u;
            const dx = x1 - CX, dy = y1 - pyT;
            const dl = hyp(dx, dy) || 1;
            c.moveTo(x + (dy / dl) * 8, y - (dx / dl) * 8);
            c.lineTo(x - (dy / dl) * 8, y + (dx / dl) * 8);
          }
        }
      }, P.fibre, 0.55, 2);

      // mitochondria, carried with the stretching cytoplasm and drifting on twos
      MITO.forEach(([mx, my0, rot], i) => {
        const my = CY + ((my0 - CY) / HH_1) * hh;
        const j = L.h3(sd('mitodrift', i), Math.round(tw * 12), 3);
        const j2 = L.h3(sd('mitodrift', i), Math.round(tw * 12), 11);
        drawMito(ctx, mx + (j - 0.5) * 3.4, my + (j2 - 0.5) * 3.4, rot + (j - 0.5) * 0.05, i);
      });

      drawPole(ctx, CX, pyT, 0);
      drawPole(ctx, CX, pyB, 1);

      // kinetochore fibres: one from each pole to each centromere and nowhere else
      // (art bible 10.7). Each shortens as its copy climbs toward the pole.
      CH.forEach((st, k) => {
        const py = st.s ? pyB : pyT;
        const pts = fibrePts(CX, py, st.x, st.y, slack * (st.u > 0 ? 0.35 : 1), k % 2 ? 1 : -1, sd('kfib', k), bi);
        LIB.inkPath(ctx, pts, {
          width: 2.1,
          color: P.fibre,
          alpha: 0.95,
          seed: sd('kfibink', k),
          taper: [12, 6],
          wobble: 1,
          tremble: 0.3,
          swell: 0,
        });
      });

      // =================================================================================
      // 5 the chromosomes
      // =================================================================================
      for (const { st, k } of order) drawChromatid(ctx, st, k);
      for (const { st, k } of order) drawCentromere(ctx, st, k, hs > 3 ? 6.5 : 7);

      // =================================================================================
      // 6 overlays (screen-fixed, above the illustration, never hatched or grained)
      // =================================================================================

      // 6a annBlue trajectories: a dashed tail drawing on behind each travelling copy with an
      // arrowhead leading it toward its pole (art bible 3.3: 2.5 px, 14 on and 10 off)
      const trajFade = (1 - sstep(2.58, 2.83, t)) * sstep(B_SPLIT - 0.02, B_SPLIT + 0.09, t);
      if (trajFade > 0.01) {
        ctx.save();
        ctx.globalAlpha = trajFade;
        ctx.strokeStyle = P.annBlue;
        ctx.fillStyle = P.annBlue;
        ctx.lineCap = 'round';
        ctx.lineWidth = 2.5;
        ctx.setLineDash([14, 10]);
        // the tail runs from the plate to the trailing arm tips, so it is never hidden under the
        // chromosome it belongs to
        ctx.beginPath();
        for (const st of CH) {
          const tail = st.La * 0.62 + 24;
          if (Math.abs(st.y - st.sy) < tail + 16) continue;
          ctx.moveTo(st.sx, st.sy + st.dir * 10);
          ctx.lineTo(st.x, st.y - st.dir * tail);
        }
        ctx.stroke();
        ctx.setLineDash([]);
        // the arrowhead leads the copy, on clean cytoplasm, pointing at its pole
        ctx.beginPath();
        for (const st of CH) {
          const tail = st.La * 0.62 + 24;
          if (Math.abs(st.y - st.sy) < tail + 16) continue;
          const dir = st.dir;
          const hx = st.x, hy = st.y + dir * 32;
          ctx.moveTo(hx, hy + dir * 16);
          ctx.lineTo(hx - 9, hy - dir * 3);
          ctx.lineTo(hx, hy + dir * 1);
          ctx.lineTo(hx + 9, hy - dir * 3);
          ctx.closePath();
        }
        ctx.fill();
        ctx.restore();
      }

      // 6b annYellow rings on each centromere as it splits (T 16.5)
      if (t >= B_TIGHT - 1e-6 && t < B_TIGHT + 0.3) {
        const fr = Math.round((t - B_TIGHT) * 24);
        const a = 1 - Math.pow(clamp(fr / 6), 1.6);
        if (a > 0.01) {
          ctx.save();
          ctx.strokeStyle = P.annYellow;
          ctx.lineWidth = 3;
          ctx.globalAlpha = a;
          ctx.beginPath();
          for (let i = 0; i < 4; i++) {
            const r = 14 + 46 * E.outExpo((fr + 1) / 6);
            ctx.moveTo(CHROMO[i].x + r, CY);
            ctx.arc(CHROMO[i].x, CY, r, 0, TAU);
          }
          ctx.stroke();
          ctx.restore();
        }
      }

      // 6c annYellow rings pulsing at each pole as its set arrives (T 18.5)
      if (t >= B_LAND - 1e-6 && t < B_LAND + 0.44) {
        ctx.save();
        ctx.strokeStyle = P.annYellow;
        ctx.lineCap = 'round';
        for (const [py, off] of [[pyT, 0], [pyB, 2 / 24]]) {
          for (const [delay, w] of [[0, 3], [3 / 24, 2]]) {
            const f = (t - B_LAND - off - delay) * 24;
            if (f < -1e-6) continue;
            const a = 1 - Math.pow(clamp(f / 8), 1.5);
            if (a <= 0.01) continue;
            ctx.globalAlpha = a;
            ctx.lineWidth = w;
            ctx.beginPath();
            ctx.arc(CX, py, 34 + 116 * E.outExpo((f + 1) / 8), 0, TAU);
            ctx.stroke();
          }
          // four short spokes on the first frames, the reference's arrival geometry
          const f0 = (t - B_LAND - off) * 24;
          if (f0 >= -1e-6 && f0 < 5) {
            ctx.globalAlpha = 1 - clamp(f0 / 5);
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            for (let i = 0; i < 4; i++) {
              const a = Math.PI / 4 + (i * Math.PI) / 2;
              const r0 = 54 + 40 * E.outExpo((f0 + 1) / 6);
              ctx.moveTo(CX + Math.cos(a) * r0, py + Math.sin(a) * r0);
              ctx.lineTo(CX + Math.cos(a) * (r0 + 22), py + Math.sin(a) * (r0 + 22));
            }
            ctx.stroke();
          }
        }
        ctx.restore();
      }

      // 6d the shot's one label: an annYellow bracket beside the fibres, reading bottom to top
      ctx.save();
      ctx.globalAlpha = hit(0, 3, E.outExpo, 1);
      L.bracket(ctx, BR_X, BR_Y0, BR_X, BR_Y1, {
        style: 'dim',
        color: P.annYellow,
        alpha: 1,
        width: 2.5,
        cap: 20,
        label: 'spindle',
        labelSize: 32,
        p: 1,
      });
      ctx.restore();

      // =================================================================================
      // 7 the cycle glyph (G5) — the film's time device, drawn last and never re-implemented
      // =================================================================================
      FILM.lib.cycleGlyph(ctx, info.T, 'illustrated');
    },
  });
})();
