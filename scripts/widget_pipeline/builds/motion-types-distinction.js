/* ============================================================
   motion-types-distinction

   Ten machine parts and mechanisms. The student watches one marked
   point move, commits to a name, and only then sees the path it
   traced. A straight trace against an arc trace is what settles
   reciprocating against oscillating.

   The answer key is not written down anywhere. Each round supplies a
   parametric path for the marked point; analyse() samples it and
   decides two things - is the path straight, and does it turn back -
   and those two answers name the motion. The same path draws the
   trace, so the reveal cannot drift from the marking.
   ============================================================ */
(function () {
  'use strict';

  var TAU = Math.PI * 2;
  var D = 180 / Math.PI;

  var TYPES = [
    { k: 'rotary', label: 'Rotary' },
    { k: 'linear', label: 'Linear' },
    { k: 'reciprocating', label: 'Reciprocating' },
    { k: 'oscillating', label: 'Oscillating' }
  ];
  var LABEL = {};
  TYPES.forEach(function (t) { LABEL[t.k] = t.label; });

  /* ---------- shared drawing constants ---------- */
  var BODY = 'fill:#efe9e0;stroke:#c3bbac;stroke-width:1.4';
  var HAIR = 'fill:none;stroke:#c3bbac;stroke-width:1.6';
  var THIN = 'fill:none;stroke:#ded6c8;stroke-width:1.4';
  var PART = 'fill:#ffffff;stroke:#2d2a26;stroke-width:1.6';
  var INK = 'fill:#2d2a26';
  var BAR = 'fill:none;stroke:#2d2a26;stroke-width:2.4';
  var LBL = 'font:600 9px Inter,system-ui,sans-serif;fill:#a09a90;letter-spacing:.08em';

  function n(v) { return Math.round(v * 100) / 100; }

  function marker(x, y, A) {
    return '<g data-m="mk" transform="translate(' + n(x) + ',' + n(y) + ')">' +
      '<circle r="8.5" style="fill:#fff;fill-opacity:.92;stroke:' + A + ';stroke-width:2"/>' +
      '<text data-m="q" y="3.5" text-anchor="middle" style="font:700 10px Inter,system-ui,sans-serif;fill:' + A + '">?</text>' +
      '<circle data-m="dot" r="3.6" style="fill:' + A + ';display:none"/></g>';
  }

  /* ---------- the cam profile, and the follower it lifts ----------
     One function. The polygon outline and the follower height are both
     read from it, so the drawing and the motion cannot disagree.      */
  var CAM_BASE = 18, CAM_LIFT = 30;
  function camR(u) {
    u = u - Math.floor(u);
    var h = CAM_LIFT;
    if (u < 0.30) return CAM_BASE + h * (1 - Math.cos(Math.PI * u / 0.30)) / 2;
    if (u < 0.45) return CAM_BASE + h;
    if (u < 0.75) return CAM_BASE + h * (1 + Math.cos(Math.PI * (u - 0.45) / 0.30)) / 2;
    return CAM_BASE;
  }
  function camOutline(cx, cy) {
    var pts = [], i, u, r;
    for (i = 0; i < 96; i++) {
      u = i / 96; r = camR(u);
      pts.push(n(cx + r * Math.sin(TAU * u)) + ',' + n(cy - r * Math.cos(TAU * u)));
    }
    return pts.join(' ');
  }

  /* crank and slider: real geometry, one crank centre, one rod length */
  var CK = { cx: 70, cy: 104, r: 30, rod: 104 };
  function pin(t) {
    return { x: CK.cx + CK.r * Math.cos(TAU * t), y: CK.cy + CK.r * Math.sin(TAU * t) };
  }
  function slider(t) {
    var s = CK.r * Math.sin(TAU * t);
    return CK.cx + CK.r * Math.cos(TAU * t) + Math.sqrt(CK.rod * CK.rod - s * s);
  }
  function crankScene(A, cylinder, markOnPin) {
    return (cylinder
      ? '<path d="M 126 80 L 254 80 A 4 4 0 0 1 258 84 L 258 124 A 4 4 0 0 1 254 128 L 126 128" style="' + HAIR + '"/>'
      : '<line x1="120" y1="86" x2="252" y2="86" style="' + HAIR + '"/>' +
        '<line x1="120" y1="122" x2="252" y2="122" style="' + HAIR + '"/>') +
      '<circle cx="70" cy="104" r="30" style="' + BODY + '"/>' +
      '<line data-m="rod" x1="100" y1="104" x2="174" y2="104" style="' + BAR + '"/>' +
      '<g data-m="sl" transform="translate(174,104)">' +
        '<rect x="-19" y="' + (cylinder ? -21 : -15) + '" width="38" height="' + (cylinder ? 42 : 30) + '" rx="3" style="' + PART + '"/>' +
        (markOnPin ? '' : marker(0, 0, A)) +
      '</g>' +
      '<g data-m="cr" transform="rotate(0,70,104)">' +
        '<line x1="70" y1="104" x2="100" y2="104" style="' + BAR + '"/>' +
        '<circle cx="100" cy="104" r="4.5" style="' + INK + '"/>' +
        (markOnPin ? marker(100, 104, A) : '') +
      '</g>' +
      '<circle cx="70" cy="104" r="3.5" style="' + INK + '"/>' +
      '<text x="' + (markOnPin ? 186 : 44) + '" y="152" style="' + LBL + '">INPUT</text>';
  }

  /* ============================================================
     THE ROUNDS
     point(t) is the marked point. Nothing here states an answer.
     ============================================================ */
  var ROUNDS = [
    {
      key: 'needle',
      ms: 2400,
      ask: 'A sewing machine needle is driven by the motor above. Name the type of motion of the needle.',
      note: 'Inside the machine head, a crank and slider converts the motor’s rotary motion into this.',
      point: function (t) { return { x: 170, y: 88 + 24 * (1 - Math.cos(TAU * t)) }; },
      scene: function (A) {
        return '<rect x="30" y="132" width="260" height="22" rx="4" style="' + BODY + '"/>' +
          '<rect x="152" y="118" width="36" height="9" rx="2" style="' + PART + '"/>' +
          '<g data-m="nd" transform="translate(0,0)">' +
            '<rect x="163" y="6" width="14" height="68" rx="3" style="' + PART + '"/>' +
            '<line x1="170" y1="70" x2="170" y2="88" style="stroke:#2d2a26;stroke-width:2.6"/>' +
            marker(170, 88, A) +
          '</g>' +
          '<rect x="118" y="12" width="92" height="48" rx="9" style="' + BODY + '"/>' +
          '<rect x="196" y="12" width="94" height="122" rx="9" style="' + BODY + '"/>' +
          '<text x="36" y="126" style="' + LBL + '">FABRIC</text>';
      },
      pose: function (t, m) {
        m.nd.setAttribute('transform', 'translate(0,' + n(24 * (1 - Math.cos(TAU * t))) + ')');
      }
    },
    {
      key: 'pendulum',
      ms: 2600,
      ask: 'A clock pendulum hangs from a fixed pivot at the top. Name the type of motion of the bob.',
      note: 'The bob is fixed to a pivot, so every point on the rod is stuck on a curve.',
      point: function (t) {
        var a = 0.5 * Math.cos(TAU * t);
        return { x: 160 - 112 * Math.sin(a), y: 20 + 112 * Math.cos(a) };
      },
      scene: function (A) {
        return '<rect x="86" y="4" width="148" height="160" rx="8" style="' + THIN + '"/>' +
          '<rect x="118" y="8" width="84" height="14" rx="3" style="' + BODY + '"/>' +
          '<g data-m="rd" transform="rotate(0,160,20)">' +
            '<line x1="160" y1="20" x2="160" y2="126" style="stroke:#2d2a26;stroke-width:2.4"/>' +
            '<circle cx="160" cy="132" r="13" style="' + PART + '"/>' +
            marker(160, 132, A) +
          '</g>' +
          '<circle cx="160" cy="20" r="3.5" style="' + INK + '"/>';
      },
      pose: function (t, m) {
        var a = 0.5 * Math.cos(TAU * t) * D;
        m.rd.setAttribute('transform', 'rotate(' + n(a) + ',160,20)');
      }
    },
    {
      key: 'lathe',
      ms: 2200,
      ask: 'On a lathe the work is gripped in the chuck and the tool is held still. Name the chuck’s motion.',
      note: 'A milling machine is the other way round: the cutter turns and the table carries the work past it in a straight line.',
      point: function (t) {
        return { x: 176 + 34 * Math.cos(TAU * t), y: 84 + 34 * Math.sin(TAU * t) };
      },
      scene: function (A) {
        var jaws = '', i;
        for (i = 0; i < 3; i++) {
          jaws += '<rect x="168" y="34" width="16" height="20" rx="2" style="' + PART +
            '" transform="rotate(' + (i * 120) + ',176,84)"/>';
        }
        return '<rect x="10" y="44" width="48" height="80" rx="6" style="' + BODY + '"/>' +
          '<rect x="58" y="78" width="70" height="12" rx="2" style="' + BODY + '"/>' +
          '<g data-m="ck" transform="rotate(0,176,84)">' +
            '<circle cx="176" cy="84" r="48" style="' + BODY + '"/>' +
            '<circle cx="176" cy="84" r="22" style="' + PART + '"/>' + jaws +
            marker(210, 84, A) +
          '</g>' +
          '<polygon points="268,84 248,76 248,92" style="' + INK + '"/>' +
          '<rect x="268" y="68" width="24" height="32" rx="3" style="' + BODY + '"/>' +
          '<text x="246" y="120" style="' + LBL + '">TOOL</text>' +
          '<text x="14" y="138" style="' + LBL + '">HEADSTOCK</text>';
      },
      pose: function (t, m) {
        m.ck.setAttribute('transform', 'rotate(' + n(360 * t) + ',176,84)');
      }
    },
    {
      key: 'conveyor',
      ms: 3400,
      wrap: false,
      ask: 'A box sits on a running conveyor belt. Name the type of motion of the box.',
      note: 'The pulleys have the rotary motion; the box on top of the belt only ever travels one way.',
      point: function (t) { return { x: 8 + 304 * t, y: 76 }; },
      scene: function (A) {
        return '<line x1="0" y1="92" x2="320" y2="92" style="stroke:#c3bbac;stroke-width:2.6"/>' +
          '<line x1="0" y1="134" x2="320" y2="134" style="stroke:#c3bbac;stroke-width:2.6"/>' +
          '<g data-m="p1" transform="rotate(0,40,113)"><circle cx="40" cy="113" r="21" style="' + BODY + '"/>' +
            '<line x1="40" y1="92" x2="40" y2="134" style="stroke:#c3bbac;stroke-width:1.4"/></g>' +
          '<g data-m="p2" transform="rotate(0,280,113)"><circle cx="280" cy="113" r="21" style="' + BODY + '"/>' +
            '<line x1="280" y1="92" x2="280" y2="134" style="stroke:#c3bbac;stroke-width:1.4"/></g>' +
          '<g data-m="bx" transform="translate(8,0)">' +
            '<rect x="-23" y="60" width="46" height="32" rx="3" style="' + PART + '"/>' +
            '<line x1="-23" y1="72" x2="23" y2="72" style="stroke:#c3bbac;stroke-width:1.2"/>' +
            marker(0, 76, A) +
          '</g>' +
          '<text x="8" y="160" style="' + LBL + '">BELT</text>';
      },
      pose: function (t, m) {
        m.bx.setAttribute('transform', 'translate(' + n(8 + 304 * t) + ',0)');
        var a = n(828 * t);
        m.p1.setAttribute('transform', 'rotate(' + a + ',40,113)');
        m.p2.setAttribute('transform', 'rotate(' + a + ',280,113)');
      }
    },
    {
      key: 'wiper',
      ms: 2800,
      ask: 'A wiper blade is driven from a pivot at the base of the screen. Name the blade’s motion.',
      note: 'A linkage converts the wiper motor’s rotary motion into this. The blade never goes right round.',
      point: function (t) {
        var a = 0.62 * Math.cos(TAU * t);
        return { x: 160 + 112 * Math.sin(a), y: 150 - 112 * Math.cos(a) };
      },
      scene: function (A) {
        return '<path d="M 26 18 L 294 18 L 272 148 L 48 148 Z" style="fill:#fff;stroke:#ded6c8;stroke-width:1.5"/>' +
          '<g data-m="wp" transform="rotate(0,160,150)">' +
            '<line x1="160" y1="150" x2="160" y2="46" style="stroke:#2d2a26;stroke-width:2.4"/>' +
            '<line x1="160" y1="92" x2="160" y2="40" style="stroke:#2d2a26;stroke-width:5.5;stroke-linecap:round"/>' +
            marker(160, 38, A) +
          '</g>' +
          '<circle cx="160" cy="150" r="4.5" style="' + INK + '"/>' +
          '<text x="30" y="162" style="' + LBL + '">WINDSCREEN</text>';
      },
      pose: function (t, m) {
        m.wp.setAttribute('transform', 'rotate(' + n(0.62 * Math.cos(TAU * t) * D) + ',160,150)');
      }
    },
    {
      key: 'lift',
      ms: 3400,
      wrap: false,
      ask: 'A lift car is being raised up its shaft. Name the type of motion of the car.',
      note: 'The winding drum turns, but the car itself runs one way along a straight guide.',
      point: function (t) { return { x: 160, y: 150 - 172 * t }; },
      scene: function (A) {
        var ticks = '', i, y;
        for (i = 0; i < 3; i++) {
          y = 34 + i * 52;
          ticks += '<line x1="78" y1="' + y + '" x2="96" y2="' + y + '" style="' + HAIR + '"/>' +
            '<line x1="224" y1="' + y + '" x2="242" y2="' + y + '" style="' + HAIR + '"/>';
        }
        return '<line x1="96" y1="0" x2="96" y2="168" style="' + THIN + '"/>' +
          '<line x1="224" y1="0" x2="224" y2="168" style="' + THIN + '"/>' + ticks +
          '<line data-m="cb" x1="160" y1="0" x2="160" y2="122" style="stroke:#c3bbac;stroke-width:1.8"/>' +
          '<g data-m="car" transform="translate(160,150)">' +
            '<rect x="-52" y="-28" width="104" height="56" rx="4" style="' + PART + '"/>' +
            '<line x1="0" y1="-28" x2="0" y2="28" style="stroke:#c3bbac;stroke-width:1.2"/>' +
            marker(0, 0, A) +
          '</g>' +
          '<text x="248" y="38" style="' + LBL + '">FLOOR 3</text>';
      },
      pose: function (t, m) {
        var y = 150 - 172 * t;
        m.car.setAttribute('transform', 'translate(160,' + n(y) + ')');
        m.cb.setAttribute('y2', n(y - 28));
      }
    },
    {
      key: 'cam',
      ms: 2800,
      ask: 'A motor turns the cam at a steady speed. Name the type of motion of the follower resting on it.',
      note: 'That is the cam’s job — rotary input, reciprocating output. The shape of the cam sets the size of the stroke.',
      point: function (t) { return { x: 152, y: 116 - camR(t) - 52 }; },
      scene: function (A) {
        return '<polygon data-m="cam" points="' + camOutline(152, 116) + '" style="fill:#efe9e0;stroke:#a09a90;stroke-width:1.5"/>' +
          '<g data-m="fol" transform="translate(152,94)">' +
            '<polygon points="0,0 -6,-11 6,-11" style="' + PART + '"/>' +
            '<rect x="-5" y="-56" width="10" height="45" rx="2" style="' + PART + '"/>' +
            marker(0, -52, A) +
          '</g>' +
          '<rect x="136" y="48" width="32" height="11" rx="2" style="' + BODY + '"/>' +
          '<circle cx="152" cy="116" r="4" style="' + INK + '"/>' +
          '<text x="208" y="120" style="' + LBL + '">INPUT</text>' +
          '<text x="208" y="134" style="' + LBL + '">CAM</text>';
      },
      pose: function (t, m) {
        m.cam.setAttribute('transform', 'rotate(' + n(-360 * t) + ',152,116)');
        m.fol.setAttribute('transform', 'translate(152,' + n(116 - camR(t)) + ')');
      }
    },
    {
      key: 'crank',
      ms: 2600,
      ask: 'A motor drives the crank of a crank and slider round. Name the type of motion of the slider.',
      note: 'A crank and slider converts rotary input into reciprocating output. The stroke is twice the crank radius.',
      point: function (t) { return { x: slider(t), y: 104 }; },
      scene: function (A) { return crankScene(A, false, false); },
      pose: function (t, m) {
        var p = pin(t), s = slider(t);
        m.cr.setAttribute('transform', 'rotate(' + n(360 * t) + ',70,104)');
        m.sl.setAttribute('transform', 'translate(' + n(s) + ',104)');
        m.rod.setAttribute('x1', n(p.x)); m.rod.setAttribute('y1', n(p.y));
        m.rod.setAttribute('x2', n(s)); m.rod.setAttribute('y2', 104);
      }
    },
    {
      key: 'pegslot',
      ms: 2800,
      ask: 'A peg on a turning disc runs in the lever’s slot. Name the type of motion at the top of the lever.',
      note: 'A peg and slot converts rotary input into oscillating output. The lever is pivoted, so its tip is stuck on an arc.',
      point: function (t) {
        var px = 160 + 30 * Math.sin(TAU * t), py = 78 - 30 * Math.cos(TAU * t);
        var f = Math.atan2(px - 160, 148 - py);
        return { x: 160 + 112 * Math.sin(f), y: 148 - 112 * Math.cos(f) };
      },
      scene: function (A) {
        return '<circle cx="160" cy="78" r="38" style="' + BODY + '"/>' +
          '<g data-m="dc" transform="rotate(0,160,78)">' +
            '<line x1="160" y1="78" x2="160" y2="48" style="stroke:#c3bbac;stroke-width:2"/>' +
          '</g>' +
          '<g data-m="lv" transform="translate(160,148) rotate(0)">' +
            '<rect x="-7" y="-118" width="14" height="126" rx="7" style="' + PART + '"/>' +
            '<rect x="-3.5" y="-104" width="7" height="80" rx="3.5" style="fill:#faf8f5;stroke:#c3bbac;stroke-width:1"/>' +
            marker(0, -112, A) +
          '</g>' +
          '<g data-m="pg" transform="rotate(0,160,78)">' +
            '<circle cx="160" cy="48" r="6" style="' + INK + '"/></g>' +
          '<circle cx="160" cy="148" r="4.5" style="' + INK + '"/>' +
          '<text x="210" y="82" style="' + LBL + '">INPUT</text>' +
          '<text x="210" y="96" style="' + LBL + '">DISC</text>';
      },
      pose: function (t, m) {
        var px = 160 + 30 * Math.sin(TAU * t), py = 78 - 30 * Math.cos(TAU * t);
        var f = Math.atan2(px - 160, 148 - py) * D;
        m.dc.setAttribute('transform', 'rotate(' + n(360 * t) + ',160,78)');
        m.pg.setAttribute('transform', 'rotate(' + n(360 * t) + ',160,78)');
        m.lv.setAttribute('transform', 'translate(160,148) rotate(' + n(f) + ')');
      }
    },
    {
      key: 'engine',
      ms: 2600,
      ask: 'A piston is pushed back and forth in its cylinder. A rod joins it to the crank. Name the crank’s motion.',
      note: 'The same crank and slider, worked the other way: reciprocating input at the piston, rotary output at the crank.',
      point: function (t) { return pin(t); },
      scene: function (A) { return crankScene(A, true, true); },
      pose: function (t, m) {
        var p = pin(t), s = slider(t);
        m.cr.setAttribute('transform', 'rotate(' + n(360 * t) + ',70,104)');
        m.sl.setAttribute('transform', 'translate(' + n(s) + ',104)');
        m.rod.setAttribute('x1', n(p.x)); m.rod.setAttribute('y1', n(p.y));
        m.rod.setAttribute('x2', n(s)); m.rod.setAttribute('y2', 104);
      }
    }
  ];

  /* ============================================================
     THE MODEL THAT MARKS THE ANSWER
     Two measurements on the sampled path, nothing else:
       straight?  max deviation from the principal chord / its span.
                  Measured over all ten rounds: every straight path gives
                  0.000; the three arcs give 0.128, 0.160 and 0.225; a
                  circle gives 0.500. The cut at 0.04 is clear of both.
       turns back? a velocity reversal of more than 120 degrees.
                  Zero-length steps (a cam dwell) are skipped.
     ============================================================ */
  function analyse(fn, wrap) {
    var N = 144, p = [], i;
    for (i = 0; i < N; i++) p.push(fn(i / N));

    var far = 0, best = -1, d;
    for (i = 1; i < N; i++) {
      d = (p[i].x - p[0].x) * (p[i].x - p[0].x) + (p[i].y - p[0].y) * (p[i].y - p[0].y);
      if (d > best) { best = d; far = i; }
    }
    var ux = p[far].x - p[0].x, uy = p[far].y - p[0].y;
    var len = Math.sqrt(ux * ux + uy * uy) || 1;
    ux /= len; uy /= len;

    var dev = 0, lo = 0, hi = 0, along, perp, dx, dy;
    for (i = 0; i < N; i++) {
      dx = p[i].x - p[0].x; dy = p[i].y - p[0].y;
      along = dx * ux + dy * uy;
      perp = Math.abs(dx * uy - dy * ux);
      if (perp > dev) dev = perp;
      if (along < lo) lo = along;
      if (along > hi) hi = along;
    }
    var span = (hi - lo) || 1;

    var loIdx = 0, hiIdx = 0, loV = Infinity, hiV = -Infinity;
    for (i = 0; i < N; i++) {
      along = (p[i].x - p[0].x) * ux + (p[i].y - p[0].y) * uy;
      if (along < loV) { loV = along; loIdx = i; }
      if (along > hiV) { hiV = along; hiIdx = i; }
    }

    var cyclic = wrap !== false;
    var segs = cyclic ? N : N - 1;
    var V = [], vx, vy, mag, c;
    for (i = 0; i < segs; i++) {
      vx = p[(i + 1) % N].x - p[i].x; vy = p[(i + 1) % N].y - p[i].y;
      mag = Math.sqrt(vx * vx + vy * vy);
      if (mag < span * 1e-6) continue;          /* a dwell holds still: no direction */
      V.push({ x: vx / mag, y: vy / mag });
    }
    /* a closed path is compared right round, or a turning point sitting on
       t = 0 would never be seen at all */
    var pairs = cyclic ? V.length : V.length - 1;
    var rev = 0, turn = 0, a1, b1;
    for (i = 0; i < pairs; i++) {
      a1 = V[i]; b1 = V[(i + 1) % V.length];
      c = a1.x * b1.x + a1.y * b1.y;
      if (c < -0.5) rev++;
      turn += Math.atan2(a1.x * b1.y - a1.y * b1.x, c);
    }
    return {
      points: p, straight: (dev / span) < 0.04, reverses: rev >= 2,
      turn: Math.abs(turn), ratio: dev / span, loIdx: loIdx, hiIdx: hiIdx
    };
  }

  function classify(a) {
    if (a.reverses) return a.straight ? 'reciprocating' : 'oscillating';
    return a.straight ? 'linear' : 'rotary';
  }

  function fact(a) {
    if (a.reverses) {
      return a.straight
        ? 'The traced path is a straight line, and it turns back at each end.'
        : 'The traced path is an arc, and it turns back at each end.';
    }
    return a.straight
      ? 'The traced path is a straight line, and it keeps going the same way.'
      : 'The traced path is a full circle about a fixed axis.';
  }

  var DIAG = {
    'oscillating>reciprocating': 'Oscillating goes back and forth too, but along an arc — a pendulum, a wiper blade.',
    'reciprocating>oscillating': 'Reciprocating goes back and forth too, but in a straight line — a piston, a needle.',
    'rotary>reciprocating': 'Rotary motion goes right round a fixed axis, the same way every turn. Repeating is not rotary.',
    'rotary>oscillating': 'Rotary motion goes right round a fixed axis. This one turns back long before it gets there.',
    'rotary>linear': 'Rotary motion goes round a fixed axis. Nothing here turns about a centre.',
    'linear>reciprocating': 'Linear motion is straight and one way only — a lift rising, a box on a belt. This comes straight back.',
    'linear>oscillating': 'Linear motion is straight and one way only. This path curves, and it returns.',
    'linear>rotary': 'Linear motion is a straight line. This point never leaves its circle.',
    'reciprocating>rotary': 'Reciprocating is straight and back and forth. This keeps going the same way about a fixed axis.',
    'reciprocating>linear': 'Reciprocating comes back on itself. This one keeps going and never returns.',
    'oscillating>rotary': 'Oscillating swings along an arc and turns back. This goes right round, the same way every turn.',
    'oscillating>linear': 'Oscillating swings along an arc and turns back. This path is straight and never returns.'
  };

  var CUE = 'Two things decide it: the shape of the path, and whether the part comes back.';
  var MASTER = 'Three in a row — you have it. Two questions name any motion: is the path a line or an arc, ' +
    'and does the part come back or keep going? Converting one into another is a mechanism’s job — a cam ' +
    'or a crank and slider gives reciprocating, a peg and slot gives oscillating.';

  /* Reduced motion steps by equal DISTANCE along the path, never equal
     time: a sinusoid crawls at its turning points, so equal-time steps
     shift the marker about 2px and the button looks broken. */
  function stepTimes(a, wrap, count) {
    var p = a.points, N = p.length, cyclic = wrap !== false;
    var cum = [0], i, b, d = 0, segs = cyclic ? N : N - 1;
    for (i = 0; i < segs; i++) {
      b = p[(i + 1) % N];
      d += Math.sqrt((b.x - p[i].x) * (b.x - p[i].x) + (b.y - p[i].y) * (b.y - p[i].y));
      cum.push(d);
    }
    var out = [], k, target, j = 0;
    for (k = 0; k < count; k++) {
      target = d * k / count;
      while (j < cum.length - 1 && cum[j + 1] < target) j++;
      out.push(j / N);
    }
    return out;
  }

  /* ---------- the trace, drawn from the same samples the model marked ---------- */
  function traceMarkup(a, A) {
    var pts = a.points.map(function (q) { return n(q.x) + ',' + n(q.y); });
    var closed = !a.reverses && !a.straight;
    var d = '<polyline points="' + pts.join(' ') + (closed ? ' ' + pts[0] : '') +
      '" style="fill:none;stroke:' + A + ';stroke-width:2.2;stroke-dasharray:5 4;stroke-linecap:round"/>';
    function head(i) {
      var p = a.points[i], q = a.points[(i - 2 + a.points.length) % a.points.length];
      var vx = p.x - q.x, vy = p.y - q.y, m = Math.sqrt(vx * vx + vy * vy) || 1;
      vx /= m; vy /= m;
      var s = 6.5;
      return '<polygon points="' + n(p.x + vx * s) + ',' + n(p.y + vy * s) + ' ' +
        n(p.x - vx * s + vy * s * 0.62) + ',' + n(p.y - vy * s - vx * s * 0.62) + ' ' +
        n(p.x - vx * s - vy * s * 0.62) + ',' + n(p.y - vy * s + vx * s * 0.62) +
        '" style="fill:' + A + '"/>';
    }
    if (a.reverses) d += head(a.hiIdx) + head(a.loIdx);
    else d += head(Math.round(a.points.length * 0.72));
    return '<g data-m="tr" style="display:none">' + d + '</g>';
  }

  /* ============================================================ */
  var CSS =
    '.svw-mo{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;' +
      'line-height:1.45;max-width:600px;margin:0 auto}' +
    '.svw-mo *{box-sizing:border-box}' +
    '.svw-mo-kick{margin:0;font-size:.66rem;font-weight:700;letter-spacing:.11em;' +
      'text-transform:uppercase;color:var(--svmo-a)}' +
    '.svw-mo-title{margin:.1rem 0 .3rem;font-family:"Source Serif 4",Georgia,serif;' +
      'font-weight:600;font-size:1.2rem;line-height:1.2}' +
    '.svw-mo-ask{margin:0 0 .5rem;font-size:.86rem;line-height:1.35;min-height:4em;color:#3c3831}' +
    '.svw-mo-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.25rem}' +
    '.svw-mo-stage svg{display:block;width:100%;height:168px}' +
    '.svw-mo-opts{display:grid;grid-template-columns:1fr 1fr;gap:.4rem;margin:.5rem 0}' +
    '.svw-mo-opt{font:600 .82rem/1.2 inherit;padding:.5rem .5rem;border-radius:10px;' +
      'border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;text-align:center}' +
    '.svw-mo-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}' +
    '.svw-mo-opt[disabled]{cursor:default;opacity:.55}' +
    '.svw-mo-opt[disabled][aria-pressed="true"]{opacity:1}' +
    '.svw-mo-row{display:flex;gap:.4rem;align-items:center}' +
    '.svw-mo-go{font:600 .82rem/1.2 inherit;padding:.55rem 1.1rem;border-radius:10px;' +
      'border:1px solid #2d2a26;background:#2d2a26;color:#fff;cursor:pointer}' +
    '.svw-mo-go[disabled]{opacity:.35;cursor:default}' +
    '.svw-mo-step{font:600 .78rem/1.2 inherit;padding:.5rem .8rem;border-radius:10px;' +
      'border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer}' +
    '.svw-mo-cap{margin:.55rem 0 0;font-size:.84rem;line-height:1.5;min-height:3.6em;color:#3c3831}' +
    '.svw-mo-cap b{font-weight:700}' +
    '.svw-mo-run{margin:.2rem 0 0;font-size:.78rem;color:#8d8880;min-height:1.3em}' +
    '.svw-mo-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);' +
      'clip-path:inset(50%);white-space:nowrap}';

  function mount(root, ctx) {
    ctx = ctx || {};
    var reduced = !!ctx.reducedMotion;

    var wrap = document.createElement('div');
    wrap.className = 'svw-mo';
    var style = document.createElement('style');
    style.textContent = CSS;
    wrap.appendChild(style);
    root.appendChild(wrap);

    var A = (getComputedStyle(root).getPropertyValue('--accent') || '').trim() ||
      ctx.accent || '#8a6a4f';
    wrap.style.setProperty('--svmo-a', A);

    var head = document.createElement('div');
    head.innerHTML = '<p class="svw-mo-kick">Motion</p>' +
      '<h3 class="svw-mo-title">Four kinds of movement</h3>' +
      '<p class="svw-mo-ask"></p>';
    wrap.appendChild(head);
    var askEl = head.querySelector('.svw-mo-ask');

    var stageEl = document.createElement('div');
    stageEl.className = 'svw-mo-stage';
    wrap.appendChild(stageEl);

    var optsEl = document.createElement('div');
    optsEl.className = 'svw-mo-opts';
    var optBtns = TYPES.map(function (T) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'svw-mo-opt';
      b.textContent = T.label;
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () { choose(T.k); });
      optsEl.appendChild(b);
      return b;
    });
    wrap.appendChild(optsEl);

    var row = document.createElement('div');
    row.className = 'svw-mo-row';
    var go = document.createElement('button');
    go.type = 'button';
    go.className = 'svw-mo-go';
    go.textContent = 'Check';
    go.disabled = true;
    row.appendChild(go);
    var stepBtn = null;
    if (reduced) {
      stepBtn = document.createElement('button');
      stepBtn.type = 'button';
      stepBtn.className = 'svw-mo-step';
      stepBtn.textContent = 'Step on';
      row.appendChild(stepBtn);
    }
    wrap.appendChild(row);

    var capEl = document.createElement('p');
    capEl.className = 'svw-mo-cap';
    wrap.appendChild(capEl);
    var runEl = document.createElement('p');
    runEl.className = 'svw-mo-run';
    wrap.appendChild(runEl);
    var srEl = document.createElement('p');
    srEl.className = 'svw-mo-sr';
    srEl.setAttribute('aria-live', 'polite');
    wrap.appendChild(srEl);

    /* ---------- state ---------- */
    var order = shuffle(), oi = -1;
    var round = null, ana = null, answer = null, els = null;
    var chosen = null, revealed = false;
    var streak = 0, mastered = false, attempted = 0;
    var t = 0, raf = null, lastTs = 0, steps = null, si = 0;

    function shuffle() {
      var a = ROUNDS.slice(), i, j, tmp, tries;
      for (tries = 0; tries < 40; tries++) {
        for (i = a.length - 1; i > 0; i--) {
          j = Math.floor(Math.random() * (i + 1));
          tmp = a[i]; a[i] = a[j]; a[j] = tmp;
        }
        if (ok(a)) break;
      }
      return a;
      /* no two neighbours share an answer, so the same word twice never
         builds a run and a one-word guesser cannot reach mastery */
      function ok(list) {
        for (var k = 1; k < list.length; k++) {
          if (keyOf(list[k]) === keyOf(list[k - 1])) return false;
        }
        return true;
      }
    }
    function keyOf(r) {
      if (!r._k) r._k = classify(analyse(r.point, r.wrap));
      return r._k;
    }

    function setState() {
      root.dataset.svState = JSON.stringify({
        round: round ? round.key : null,
        chosen: chosen,
        correct: revealed ? (chosen === answer) : null,
        streak: streak, mastered: mastered, attempted: attempted
      });
    }

    function setRound() {
      oi = (oi + 1) % order.length;
      round = order[oi];
      ana = analyse(round.point, round.wrap);
      answer = classify(ana);
      chosen = null; revealed = false;

      askEl.textContent = round.ask;
      stageEl.innerHTML = '<svg viewBox="0 0 320 168" preserveAspectRatio="xMidYMid meet" ' +
        'focusable="false" aria-hidden="true">' + round.scene(A) + traceMarkup(ana, A) + '</svg>';
      els = {};
      var all = stageEl.querySelectorAll('[data-m]');
      for (var i = 0; i < all.length; i++) {
        var k = all[i].getAttribute('data-m');
        if (!(k in els)) els[k] = all[i];
      }

      optBtns.forEach(function (b) { b.disabled = false; b.setAttribute('aria-pressed', 'false'); });
      go.disabled = true;
      go.textContent = 'Check';
      capEl.textContent = CUE;
      runEl.textContent = runLine();
      srEl.textContent = round.ask;

      t = 0;
      steps = stepTimes(ana, round.wrap, 12);
      si = 0;
      if (reduced) {
        els.tr.style.display = '';           /* no motion: the whole path, drawn still */
        round.pose(0, els);
      } else {
        start();
      }
      setState();
    }

    function runLine() {
      if (mastered) return 'You have it — keep going for as long as you like.';
      if (streak === 2) return 'Two right in a row — one more and you have it.';
      if (streak === 1) return 'One right in a row — two more and you have it.';
      return '';
    }

    function choose(k) {
      if (revealed) return;
      chosen = k;
      optBtns.forEach(function (b, i) {
        b.setAttribute('aria-pressed', TYPES[i].k === k ? 'true' : 'false');
      });
      go.disabled = false;
      setState();
    }

    function commit() {
      revealed = true;
      attempted++;
      var right = chosen === answer;
      if (right) { streak++; if (streak >= 3) mastered = true; } else { streak = 0; }

      stop();
      t = steps[Math.round(steps.length / 4)];
      round.pose(t, els);
      els.tr.style.display = '';
      if (els.q) els.q.style.display = 'none';
      if (els.dot) els.dot.style.display = '';
      optBtns.forEach(function (b) { b.disabled = true; });

      var msg;
      if (right) {
        msg = '<b>Right — ' + LABEL[answer] + '.</b> ' + fact(ana) + ' ' + round.note;
      } else {
        msg = '<b>Not quite — you said ' + LABEL[chosen] + '.</b> ' + fact(ana) +
          ' That makes it <b>' + LABEL[answer] + '</b>. ' + DIAG[chosen + '>' + answer];
      }
      if (right && mastered && streak === 3) msg = MASTER;
      capEl.innerHTML = msg;
      runEl.textContent = runLine();
      srEl.textContent = capEl.textContent;
      go.textContent = mastered ? 'Another anyway' : 'Next';
      setState();
    }

    go.addEventListener('click', function () {
      if (!revealed) { if (chosen) commit(); }
      else setRound();
    });
    if (stepBtn) {
      stepBtn.addEventListener('click', function () {
        si = (si + 1) % steps.length;
        t = steps[si];
        round.pose(t, els);
        srEl.textContent = 'Step ' + (si + 1) + ' of ' + steps.length + '.';
      });
    }

    /* ---------- motion: runs only while a round is on screen ---------- */
    function frame(ts) {
      if (!root.isConnected || revealed || reduced) { raf = null; return; }
      if (lastTs) t = (t + (ts - lastTs) / round.ms) % 1;
      lastTs = ts;
      round.pose(t, els);
      raf = requestAnimationFrame(frame);
    }
    function start() {
      if (raf || reduced) return;
      lastTs = 0;
      raf = requestAnimationFrame(frame);
    }
    function stop() {
      if (raf) { cancelAnimationFrame(raf); raf = null; }
    }

    setRound();
  }

  window.SVWidget = {
    meta: {
      id: 'motion-types-distinction',
      title: 'Four kinds of movement',
      teaches: 'Rotary, linear, reciprocating and oscillating motion told apart by the path a point traces, and the mechanisms that convert one into another'
    },
    mount: mount
  };
})();
