/* Theatre spaces: where does the audience sit?
   One plan of a room. The student places the audience for a real production
   brief, commits, and the plan then draws the sightlines that brief creates.
   Marking and drawing both read the same facts (sides / arch / mobile), so a
   configuration can never be marked right and drawn wrong.
   Self-contained: no imports, no network, every selector scoped to .svw-thtr. */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';

  var CSS = [
'.svw-thtr{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.4;max-width:580px;margin:0 auto}',
'.svw-thtr *{box-sizing:border-box}',
'.svw-thtr p{margin:0}',
'.svw-thtr .t-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--t-acc);margin:0 0 .2rem}',
'.svw-thtr .t-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.18rem;font-weight:600;line-height:1.18;margin:0 0 .3rem}',
'.svw-thtr .t-frame{font-size:.82rem;line-height:1.45;color:#5b564e;margin:0 0 .45rem}',
'.svw-thtr .t-brief{font-size:.85rem;font-weight:600;line-height:1.38;margin:0 0 .45rem}',
'.svw-thtr .t-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;padding:.3rem;margin:0 auto .3rem;max-width:370px}',
'.svw-thtr .t-plan{display:block;width:100%;height:auto}',
'.svw-thtr .t-cap{font-size:.74rem;line-height:1.45;color:#5b564e;min-height:2.9em;margin:0 0 .5rem}',
'.svw-thtr .t-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.36rem}',
'.svw-thtr .t-chip{display:block;width:100%;font:inherit;text-align:center;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.34rem .22rem;cursor:pointer}',
'.svw-thtr .t-chip svg{display:block;width:100%;max-width:48px;height:auto;margin:0 auto .18rem}',
'.svw-thtr .t-chip span{display:block;font-size:.7rem;font-weight:600;line-height:1.2;min-height:2.4em}',
'.svw-thtr .t-chip[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
'.svw-thtr .t-chip .i-seat{fill:#e6e0d4;stroke:#c9c2b4;stroke-width:.8}',
'.svw-thtr .t-chip .i-act{fill:#fff;stroke:#2d2a26;stroke-width:1}',
'.svw-thtr .t-chip .i-ink{fill:#2d2a26}',
'.svw-thtr .t-chip .i-dash{fill:none;stroke:#8d8880;stroke-width:.8;stroke-dasharray:2.5 2}',
'.svw-thtr .t-chip[aria-pressed="true"] .i-seat{fill:#6e675d;stroke:#a49c90}',
'.svw-thtr .t-chip[aria-pressed="true"] .i-act{fill:#2d2a26;stroke:#fff}',
'.svw-thtr .t-chip[aria-pressed="true"] .i-ink{fill:#fff}',
'.svw-thtr .t-chip[aria-pressed="true"] .i-dash{stroke:#cfc8bd}',
'.svw-thtr .t-none{display:block;width:100%;margin-top:.36rem;font:inherit;font-size:.78rem;line-height:1.35;font-weight:500;text-align:left;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.42rem .6rem;cursor:pointer}',
'.svw-thtr .t-none[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}',
'.svw-thtr .t-opts.gone{display:none}',
'.svw-thtr .t-fb{display:none}',
'.svw-thtr .t-fb.on{display:block}',
'.svw-thtr .t-flag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin:0 0 .22rem}',
'.svw-thtr .t-flag.ok{color:#4f7d63}',
'.svw-thtr .t-flag.no{color:#5b564e}',
'.svw-thtr .t-say{font-size:.84rem;line-height:1.45;margin:0 0 .3rem}',
'.svw-thtr .t-note{font-size:.74rem;line-height:1.45;color:#8d8880;margin:0}',
'.svw-thtr .t-act{display:flex;align-items:center;justify-content:space-between;gap:.6rem;margin-top:.5rem}',
'.svw-thtr .t-run{font-size:.76rem;line-height:1.35;color:#5b564e;font-variant-numeric:tabular-nums}',
'.svw-thtr .t-go{flex:0 0 auto;font:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.5rem .95rem;cursor:pointer}',
'.svw-thtr .t-go[disabled]{background:#faf8f5;color:#a9a39a;border-color:#ddd7cd;cursor:default}',
'.svw-thtr .t-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
'.svw-thtr .t-seat{fill:#f2eee6;stroke:#ddd6c9;stroke-width:1}',
'.svw-thtr .t-seatrow{stroke:#c4bdae;stroke-width:1.5;stroke-linecap:round}',
'.svw-thtr .t-area{fill:#fff;stroke:#2d2a26;stroke-width:1.2}',
'.svw-thtr .t-house{fill:#fff;stroke:#2d2a26;stroke-width:1.1}',
'.svw-thtr .t-wing{fill:#e4ded1;stroke:none}',
'.svw-thtr .t-solid{fill:#2d2a26;stroke:none}',
'.svw-thtr .t-open{fill:none;stroke:#b8b1a5;stroke-width:1.1;stroke-dasharray:4 3}',
'.svw-thtr .t-aisle{fill:none;stroke:#8d8880;stroke-width:1;stroke-dasharray:3 2.5}',
'.svw-thtr .t-stand{fill:#a49e94}',
'.svw-thtr .t-ghost{fill:none;stroke:#8d8880;stroke-width:1.2;stroke-dasharray:3.5 2.5}',
'.svw-thtr .t-shade{fill:#2d2a26;fill-opacity:.14}',
'.svw-thtr .t-lit{fill:var(--t-acc);fill-opacity:.09}',
'.svw-thtr .t-ray{fill:none;stroke:var(--t-acc);stroke-width:1.3}',
'.svw-thtr .t-ray.no{stroke:#8d8880;stroke-dasharray:3 2.5}',
'.svw-thtr .t-stop{fill:#8d8880}',
'.svw-thtr .t-actor{fill:var(--t-acc)}',
'.svw-thtr .t-face{fill:none;stroke:var(--t-acc);stroke-width:1.6}',
'.svw-thtr .t-lab{font-family:Inter,system-ui,sans-serif;font-size:10px;fill:#5b564e}',
'.svw-thtr .t-tag{font-family:Inter,system-ui,sans-serif;font-size:10px;font-weight:600;fill:#2d2a26;paint-order:stroke;stroke:#faf8f5;stroke-width:2.8;stroke-linejoin:round}'
  ].join('\n');

  /* ---- the six configurations ------------------------------------------
     `sides`, `arch` and `mobile` are the whole model. The chip icon, the
     big plan and the marking predicate all read these same three facts. */
  var CFG = {
    pros: { id: 'pros', name: 'Proscenium arch', sides: ['S'], arch: true, mobile: false,
      cap: 'one side, through a frame. The wings stay hidden, so flats can look solid.' },
    endon: { id: 'endon', name: 'End-on', sides: ['S'], arch: false, mobile: false,
      cap: 'one side, no arch. Stage and seats share a room, and the seating can be re-set.' },
    thrust: { id: 'thrust', name: 'Thrust', sides: ['S', 'W', 'E'], arch: false, mobile: false,
      cap: 'three sides, close in. The fourth side stays a wall to build and enter through.' },
    round: { id: 'round', name: 'In the round', sides: ['N', 'S', 'W', 'E'], arch: false, mobile: false,
      cap: 'four sides, entering by the aisles. Nothing tall can stand, and somebody has the back.' },
    trav: { id: 'trav', name: 'Traverse', sides: ['W', 'E'], arch: false, mobile: false,
      cap: 'two banks facing down a corridor. Each half of the house watches the other half.' },
    prom: { id: 'prom', name: 'Promenade', sides: [], arch: false, mobile: true,
      cap: 'no fixed seats. The audience moves with the performers, so sightlines are not guaranteed.' }
  };

  /* ---- plan geometry (viewBox 320 x 118) -------------------------------- */
  var GEO = {
    pros: { act: { x: 118, y: 28, w: 84, h: 62 },
      house: { x: 92, y: 28, w: 136, h: 62 },
      wings: [{ x: 92, y: 28, w: 26, h: 62 }, { x: 202, y: 28, w: 26, h: 62 }],
      flats: [{ x: 92, y: 87, w: 26, h: 4 }, { x: 202, y: 87, w: 26, h: 4 }],
      blocks: { S: { x: 98, y: 96, w: 124, h: 20 } } },
    endon: { act: { x: 108, y: 28, w: 104, h: 62 }, openS: true,
      blocks: { S: { x: 98, y: 96, w: 124, h: 20 } } },
    thrust: { act: { x: 112, y: 24, w: 96, h: 70 }, wall: { x: 112, y: 24, w: 96, h: 5 },
      blocks: { S: { x: 96, y: 100, w: 128, h: 16 },
                W: { x: 16, y: 46, w: 88, h: 48 }, E: { x: 216, y: 46, w: 88, h: 48 } } },
    round: { act: { x: 118, y: 30, w: 84, h: 58 },
      blocks: { N: { x: 104, y: 4, w: 112, h: 18 }, S: { x: 104, y: 96, w: 112, h: 18 },
                W: { x: 24, y: 26, w: 84, h: 66 }, E: { x: 212, y: 26, w: 84, h: 66 } } },
    trav: { act: { x: 138, y: 10, w: 44, h: 98 },
      blocks: { W: { x: 18, y: 10, w: 112, h: 98 }, E: { x: 190, y: 10, w: 112, h: 98 } } },
    prom: { venue: { x: 14, y: 4, w: 292, h: 110 },
      walls: [[150, 4, 150, 40], [214, 70, 214, 114], [14, 74, 74, 74]],
      pillars: [{ x: 86, y: 52, w: 11, h: 11 }, { x: 168, y: 60, w: 11, h: 11 },
                { x: 238, y: 36, w: 11, h: 11 }],
      crowd: [[40, 22], [62, 34], [92, 20], [118, 30], [44, 60], [70, 68], [104, 74],
              [132, 60], [150, 86], [178, 96], [196, 40], [224, 20], [252, 62],
              [278, 40], [268, 96], [232, 100], [30, 96], [300, 74]] }
  };

  /* ---- geometry helpers ------------------------------------------------- */
  function mk(tag, a) {
    var e = document.createElementNS(NS, tag), k;
    for (k in a) { if (Object.prototype.hasOwnProperty.call(a, k)) e.setAttribute(k, a[k]); }
    return e;
  }
  function put(g, tag, a) { var e = mk(tag, a); g.appendChild(e); return e; }
  function tag(g, x, y, s, anchor, cls) {
    var e = mk('text', { x: x, y: y, 'text-anchor': anchor || 'middle', 'class': cls || 't-tag' });
    e.textContent = s; g.appendChild(e); return e;
  }
  function mid(r) { return { x: r.x + r.w / 2, y: r.y + r.h / 2 }; }
  function corners(r) {
    return [{ x: r.x, y: r.y }, { x: r.x + r.w, y: r.y },
            { x: r.x + r.w, y: r.y + r.h }, { x: r.x, y: r.y + r.h }];
  }
  function silhouette(vp, r) {
    var p = corners(r), base = Math.atan2(p[0].y - vp.y, p[0].x - vp.x);
    var lo = 0, hi = 0, loA = 0, hiA = 0, i, a;
    for (i = 1; i < 4; i++) {
      a = Math.atan2(p[i].y - vp.y, p[i].x - vp.x) - base;
      while (a > Math.PI) a -= 2 * Math.PI;
      while (a < -Math.PI) a += 2 * Math.PI;
      if (a < loA) { loA = a; lo = i; }
      if (a > hiA) { hiA = a; hi = i; }
    }
    return [p[lo], p[hi]];
  }
  function push(vp, p, len) {
    var dx = p.x - vp.x, dy = p.y - vp.y, m = Math.sqrt(dx * dx + dy * dy) || 1;
    return { x: p.x + dx / m * len, y: p.y + dy / m * len };
  }
  function shadow(g, vp, r) {
    var s = silhouette(vp, r), a = push(vp, s[0], 420), b = push(vp, s[1], 420);
    var pts = [s[0], a, b, s[1]].map(function (p) {
      return p.x.toFixed(1) + ',' + p.y.toFixed(1);
    }).join(' ');
    put(g, 'polygon', { points: pts, 'class': 't-shade' });
  }
  function segSeg(p1, p2, p3, p4) {
    var d = (p2.x - p1.x) * (p4.y - p3.y) - (p2.y - p1.y) * (p4.x - p3.x);
    if (Math.abs(d) < 1e-9) return null;
    var t = ((p3.x - p1.x) * (p4.y - p3.y) - (p3.y - p1.y) * (p4.x - p3.x)) / d;
    var u = ((p3.x - p1.x) * (p2.y - p1.y) - (p3.y - p1.y) * (p2.x - p1.x)) / d;
    if (t < 0 || t > 1 || u < 0 || u > 1) return null;
    return t;
  }
  function segRect(p, q, r) {
    var c = corners(r), best = null, i, t;
    for (i = 0; i < 4; i++) {
      t = segSeg(p, q, c[i], c[(i + 1) % 4]);
      if (t !== null && (best === null || t < best)) best = t;
    }
    return best;
  }
  /* One ray, stopped wherever the first blocker really is. */
  function ray(g, vp, target, blockers, dashWhenBlocked) {
    var t = 1, hit = false, i, s;
    for (i = 0; i < (blockers || []).length; i++) {
      s = segRect(vp, target, blockers[i]);
      if (s !== null && s < t) { t = s; hit = true; }
    }
    var ex = { x: vp.x + (target.x - vp.x) * t, y: vp.y + (target.y - vp.y) * t };
    put(g, 'line', { x1: vp.x.toFixed(1), y1: vp.y.toFixed(1),
      x2: ex.x.toFixed(1), y2: ex.y.toFixed(1),
      'class': 't-ray' + (hit && dashWhenBlocked !== false ? ' no' : '') });
    if (hit) put(g, 'circle', { cx: ex.x.toFixed(1), cy: ex.y.toFixed(1), r: 2.2, 'class': 't-stop' });
    return hit;
  }
  function actor(g, x, y, facing) {
    put(g, 'circle', { cx: x, cy: y, r: 3.6, 'class': 't-actor' });
    if (facing) {
      put(g, 'path', { d: 'M' + x + ',' + (y + 4) + ' L' + x + ',' + (y + 11), 'class': 't-face' });
      put(g, 'path', { d: 'M' + (x - 3) + ',' + (y + 8) + ' L' + x + ',' + (y + 12) +
        ' L' + (x + 3) + ',' + (y + 8), 'class': 't-face' });
    }
  }
  function seatRows(g, r, dir) {
    var i;
    if (dir === 'h') {
      for (i = r.y + 4; i <= r.y + r.h - 3; i += 5.5) {
        put(g, 'line', { x1: r.x + 4, y1: i.toFixed(1), x2: r.x + r.w - 4, y2: i.toFixed(1), 'class': 't-seatrow' });
      }
    } else {
      for (i = r.x + 4; i <= r.x + r.w - 3; i += 5.5) {
        put(g, 'line', { x1: i.toFixed(1), y1: r.y + 4, x2: i.toFixed(1), y2: r.y + r.h - 4, 'class': 't-seatrow' });
      }
    }
  }

  /* ---- the big plan ----------------------------------------------------- */
  function drawPlan(g, id) {
    while (g.firstChild) g.removeChild(g.firstChild);
    if (!id) {
      put(g, 'rect', { x: 14, y: 4, width: 292, height: 110, rx: 6, 'class': 't-open' });
      put(g, 'rect', { x: 118, y: 34, width: 84, height: 50, rx: 2, 'class': 't-area' });
      tag(g, 160, 62, 'acting area', 'middle', 't-lab');
      tag(g, 160, 14, 'an empty room', 'middle', 't-lab');
      return;
    }
    var geo = GEO[id], cfg = CFG[id], k, b;

    if (id === 'prom') {
      put(g, 'rect', { x: geo.venue.x, y: geo.venue.y, width: geo.venue.w, height: geo.venue.h,
        rx: 4, 'class': 't-open' });
      for (k = 0; k < geo.walls.length; k++) {
        put(g, 'line', { x1: geo.walls[k][0], y1: geo.walls[k][1],
          x2: geo.walls[k][2], y2: geo.walls[k][3], 'class': 't-open' });
      }
      for (k = 0; k < geo.pillars.length; k++) {
        b = geo.pillars[k];
        put(g, 'rect', { x: b.x, y: b.y, width: b.w, height: b.h, 'class': 't-solid' });
      }
      for (k = 0; k < geo.crowd.length; k++) {
        put(g, 'circle', { cx: geo.crowd[k][0], cy: geo.crowd[k][1], r: 2.1, 'class': 't-stand' });
      }
      tag(g, 20, 14, 'a working mill', 'start', 't-lab');
      return;
    }

    for (k in geo.blocks) {
      if (!Object.prototype.hasOwnProperty.call(geo.blocks, k)) continue;
      b = geo.blocks[k];
      put(g, 'rect', { x: b.x, y: b.y, width: b.w, height: b.h, rx: 3, 'class': 't-seat' });
      seatRows(g, b, (k === 'N' || k === 'S') ? 'h' : 'v');
    }

    if (id === 'pros') {
      put(g, 'rect', { x: geo.house.x, y: geo.house.y, width: geo.house.w, height: geo.house.h,
        rx: 2, 'class': 't-house' });
      for (k = 0; k < geo.wings.length; k++) {
        b = geo.wings[k];
        put(g, 'rect', { x: b.x, y: b.y, width: b.w, height: b.h, 'class': 't-wing' });
      }
      for (k = 0; k < geo.flats.length; k++) {
        b = geo.flats[k];
        put(g, 'rect', { x: b.x, y: b.y, width: b.w, height: b.h, 'class': 't-solid' });
      }
      tag(g, 105, 60, 'wings', 'middle', 't-lab');
      tag(g, 215, 60, 'wings', 'middle', 't-lab');
    } else if (id === 'endon') {
      put(g, 'path', { d: 'M108,90 L108,28 L212,28 L212,90', 'class': 't-area' });
      put(g, 'line', { x1: 108, y1: 90, x2: 212, y2: 90, 'class': 't-open' });
    } else {
      b = geo.act;
      put(g, 'rect', { x: b.x, y: b.y, width: b.w, height: b.h, rx: 2, 'class': 't-area' });
    }

    if (id === 'thrust') {
      b = geo.wall;
      put(g, 'rect', { x: b.x, y: b.y, width: b.w, height: b.h, 'class': 't-solid' });
      put(g, 'rect', { x: 148, y: b.y, width: 24, height: b.h, 'class': 't-seat' });
    }
    if (id === 'round') {
      put(g, 'path', { d: 'M108,24 L124,34 M212,24 L196,34 M108,94 L124,84 M212,94 L196,84',
        'class': 't-aisle' });
      tag(g, 160, 104 + 9, 'aisles', 'middle', 't-lab');
    }
    if (id === 'trav') tag(g, 160, 116, 'corridor', 'middle', 't-lab');
    if (cfg.sides.length === 1) tag(g, 26, 110, 'audience', 'start', 't-lab');
  }

  /* ---- reveal overlays: the consequence, drawn -------------------------
     Every shaded patch is a real shadow polygon cast by a real blocker from
     a real seat, clipped to the room it belongs to. */
  function ovPros(g, env) {
    var geo = GEO.pros, vp = mid(geo.blocks.S), cg = env.clipTo(geo.house), i;
    for (i = 0; i < geo.flats.length; i++) shadow(cg, vp, geo.flats[i]);
    actor(g, 160, 58, false);
    ray(g, vp, { x: 126, y: 34 }, geo.flats);
    ray(g, vp, { x: 160, y: 58 }, geo.flats);
    ray(g, vp, { x: 194, y: 34 }, geo.flats);
    tag(g, 160, 21, 'the wings stay out of sight');
  }
  function ovThrust(g, env) {
    var geo = GEO.thrust, p = { x: 160, y: 76 };
    shadow(env.clipTo({ x: 96, y: 0, w: 128, h: 24 }), mid(geo.blocks.S), geo.wall);
    actor(g, p.x, p.y, false);
    ray(g, mid(geo.blocks.S), p, []);
    ray(g, mid(geo.blocks.W), p, []);
    ray(g, mid(geo.blocks.E), p, []);
    tag(g, 160, 17, 'offstage, behind the wall');
    tag(g, 160, 92, 'three sides, all close');
  }
  function ovRound(g, env) {
    var geo = GEO.round, p = { x: 160, y: 56 };
    var tall = { x: 168, y: 32, w: 28, h: 8 };
    shadow(env.clipTo(geo.act), mid(geo.blocks.N), tall);
    put(g, 'rect', { x: tall.x, y: tall.y, width: tall.w, height: tall.h, 'class': 't-ghost' });
    actor(g, p.x, p.y, true);
    ray(g, mid(geo.blocks.S), p, []);
    ray(g, mid(geo.blocks.W), p, []);
    ray(g, mid(geo.blocks.E), p, []);
    ray(g, mid(geo.blocks.N), p, [], false);
    tag(g, 160, 15, 'this side has the back');
    tag(g, 186, 70, 'hidden by');
    tag(g, 186, 81, 'a tall piece');
  }
  function ovTrav(g) {
    var geo = GEO.trav, w = mid(geo.blocks.W), e = mid(geo.blocks.E);
    put(g, 'line', { x1: w.x, y1: 40, x2: e.x, y2: 78, 'class': 't-ray' });
    put(g, 'line', { x1: w.x, y1: 78, x2: e.x, y2: 40, 'class': 't-ray' });
    actor(g, 160, 59, false);
    tag(g, 160, 24, 'each bank sees the other');
    tag(g, 160, 100, 'the action in between');
  }
  function ovEndon(g) {
    var geo = GEO.endon, vp = mid(geo.blocks.S);
    put(g, 'polygon', { points: [vp.x + ',' + vp.y, '108,28', '212,28'].join(' '), 'class': 't-lit' });
    put(g, 'rect', { x: 92, y: 87, width: 26, height: 4, 'class': 't-ghost' });
    put(g, 'rect', { x: 202, y: 87, width: 26, height: 4, 'class': 't-ghost' });
    actor(g, 160, 58, false);
    ray(g, vp, { x: 114, y: 32 }, []);
    ray(g, vp, { x: 206, y: 32 }, []);
    tag(g, 62, 76, 'no arch');
    tag(g, 258, 76, 'no wings');
    tag(g, 160, 20, 'one continuous room');
  }
  function ovProm(g, env) {
    var geo = GEO.prom, p = { x: 206, y: 84 }, cg = env.clipTo(geo.venue), i;
    var eyes = [{ x: 270, y: 20 }, { x: 100, y: 26 }, { x: 60, y: 96 }, { x: 240, y: 100 }];
    shadow(cg, eyes[0], geo.pillars[2]);
    shadow(cg, eyes[1], geo.pillars[1]);
    for (i = 0; i < eyes.length; i++) ray(g, eyes[i], p, geo.pillars);
    actor(g, p.x, p.y, false);
    tag(g, 180, 22, 'no sightline');
    tag(g, 268, 78, 'no sightline');
    tag(g, 160, 110, 'the audience stands among it');
  }

  /* ---- chip icons: built from the same `sides` list -------------------- */
  function chipIcon(id) {
    var cfg = CFG[id];
    var svg = mk('svg', { viewBox: '0 0 44 30', 'aria-hidden': 'true', focusable: 'false' });
    var i, s;
    if (id === 'prom') {
      put(svg, 'rect', { x: 3, y: 3, width: 38, height: 24, rx: 2, 'class': 'i-dash' });
      var pts = [[10, 9], [19, 7], [28, 10], [36, 8], [8, 18], [17, 21], [26, 17],
                 [34, 20], [13, 25], [30, 25]];
      for (i = 0; i < pts.length; i++) {
        put(svg, 'circle', { cx: pts[i][0], cy: pts[i][1], r: 1.5, 'class': 'i-ink' });
      }
      return svg;
    }
    var act = (id === 'trav') ? { x: 18, y: 4, w: 8, h: 22 } : { x: 14, y: 9, w: 16, h: 12 };
    var bars = { N: { x: 12, y: 2, w: 20, h: 4 }, S: { x: 12, y: 24, w: 20, h: 4 },
                 W: { x: 3, y: 8, w: 7, h: 14 }, E: { x: 34, y: 8, w: 7, h: 14 } };
    if (id === 'trav') {
      bars.W = { x: 3, y: 4, w: 11, h: 22 };
      bars.E = { x: 30, y: 4, w: 11, h: 22 };
    }
    for (i = 0; i < cfg.sides.length; i++) {
      s = bars[cfg.sides[i]];
      put(svg, 'rect', { x: s.x, y: s.y, width: s.w, height: s.h, rx: 1, 'class': 'i-seat' });
    }
    put(svg, 'rect', { x: act.x, y: act.y, width: act.w, height: act.h, rx: 1, 'class': 'i-act' });
    if (cfg.arch) {
      put(svg, 'rect', { x: 8, y: 20, width: 7, height: 2, 'class': 'i-ink' });
      put(svg, 'rect', { x: 29, y: 20, width: 7, height: 2, 'class': 'i-ink' });
    }
    return svg;
  }

  /* ---- the briefs ------------------------------------------------------- */
  var ROUNDS = [
  { id: 'drawing-room',
    demand: 'A 1912 drawing room, played as if the audience were not there. Painted flats must look solid, and no actor may be seen waiting to enter.',
    offer: ['pros', 'endon', 'thrust', 'round'],
    test: function (c) { return c.sides.length === 1 && c.arch; },
    draw: ovPros,
    fb: {
      pros: 'the arch frames one face of the stage and masks the sides, so the wings stay out of sight and painted flats can pass for real walls. The fourth wall holds.',
      endon: 'you chose end-on. The audience does sit in front, so that half is right — but end-on has no arch and no masking, so they see straight into the sides. The illusion needs the frame.',
      thrust: 'you chose thrust. With the audience on three sides they look behind the flats and watch the actors waiting to come on. Painted scenery only reads from one face.',
      round: 'you chose in the round. Surrounded on four sides there is no back wall to paint and nowhere to hide an entrance. It is the opposite of a sealed drawing room.',
      none: 'you said the configuration makes no difference. It decides whether the wings can be hidden at all. Move this play into the round: the painted walls have no back, and every entrance happens in full view.'
    },
    note: 'End-on is not proscenium: the proscenium configuration specifically needs the framing arch.' },

  { id: 'globe',
    demand: 'Open-air Shakespeare for 700. The crowd must be close enough to read a face, wrapped round, with one solid wall behind for entrances.',
    offer: ['thrust', 'pros', 'round', 'trav'],
    test: function (c) { return c.sides.length === 3; },
    draw: ovThrust,
    fb: {
      thrust: 'three sides of audience close in, so proxemics do the work — a step towards one side is a step away from another. The fourth side stays a scenic wall, which is where the doors go.',
      pros: 'you chose proscenium arch. It gives you the wall, but it also puts the whole crowd out in front, one face and far back. The faces you wanted to read are lost at that distance.',
      round: 'you chose in the round. Four sides gets you close, but it takes the wall away: with audience behind, there is nowhere to build the doors.',
      trav: 'you chose traverse. Two facing banks are close, but they string the performers out along a corridor and leave you no scenic wall at all.',
      none: 'you said any configuration would do. The number of sides decides how far the back row sits and whether a wall can stand at all. On three sides the wall survives; on four it cannot.'
    },
    note: 'The Elizabethan Globe used a thrust, and Shakespeare’s plays were written for it.' },

  { id: 'interrogation',
    demand: 'A police interrogation in one room. The audience should feel implicated, with no hiding place and someone always seeing the suspect’s back.',
    offer: ['round', 'thrust', 'pros', 'endon'],
    test: function (c) { return c.sides.length === 4; },
    draw: ovRound,
    fb: {
      round: 'four sides means the performer is never fully front-on to anyone. Some of the audience always has the back, so the blocking has to keep turning to feed every side.',
      thrust: 'you chose thrust. Three sides is close, but the fourth is still a wall the performer can face and rest against. That upstage side is the hiding place the brief rules out.',
      pros: 'you chose proscenium arch. The arch puts the audience outside the room, looking in through a frame — the opposite of implicated. A turned back there reads as a mistake, not as exposure.',
      endon: 'you chose end-on. The audience is all in front, so the performer can simply play out to them and never turn away. Nobody ever gets the back.',
      none: 'you said the seats do not change the performance. Move this scene from end-on to the round and a turned back stops being a fault: it becomes routine, and the blocking has to be rewritten to feed every side.'
    },
    note: 'In the round, designers cannot use tall set pieces, and the rig has to light from all directions.' },

  { id: 'strike',
    demand: 'A town split by a strike. Each half of the audience must face the other half across the action, with the performers walking between them.',
    offer: ['trav', 'round', 'thrust', 'endon'],
    test: function (c) { return c.sides.length === 2; },
    draw: ovTrav,
    fb: {
      trav: 'two banks facing across a corridor, so each side of the house sees the other side’s faces over the top of the action. The geometry makes the argument: two sides, contested ground between them.',
      round: 'you chose in the round. Four sides surrounds the action, so the house reads as one ring rather than two camps. Traverse is the one that splits it in two.',
      thrust: 'you chose thrust. Three sides wraps the audience round a corner, and there is no facing bank opposite to stare back. This brief needs exactly two blocks.',
      endon: 'you chose end-on. One bank facing forward makes the audience a single body of observers. Nobody is looking at anybody.',
      none: 'you said it is only seating. Here the seating is the argument: two opposed banks turn the audience into the two sides of the strike. Play it end-on and that reading is simply gone.'
    },
    note: 'Traverse is also called corridor staging; it suits conflict, opposition and surveillance.' },

  { id: 'touring',
    demand: 'A touring two-hander in school halls: no arch, no wings, no fly tower. The seating is re-set each afternoon and shares the room with the stage.',
    offer: ['endon', 'pros', 'thrust', 'prom'],
    test: function (c) { return c.sides.length === 1 && !c.arch && !c.mobile; },
    draw: ovEndon,
    fb: {
      endon: 'the audience sits in front, as in a proscenium, but with no arch between them: stage and seats are one continuous space. That is why studio and black box rooms are set up end-on — the seats can be moved for the next show.',
      pros: 'you chose proscenium arch. A proscenium needs the built arch and the wings behind it. A school hall has neither, and an arch cannot be re-set in an afternoon.',
      thrust: 'you chose thrust. Wrapping the audience round three sides is possible in a hall, but the brief seats them in front of a stage that faces them. Thrust would mean re-blocking for three viewpoints.',
      prom: 'you chose promenade. That removes the seating altogether and walks the audience through the building. This brief keeps them seated, facing one way.',
      none: 'you said any of them. The room decides: no arch means no proscenium, whatever the seats do. End-on and proscenium look almost alike on a plan and are not the same configuration.'
    },
    note: 'Many studio and black box theatres are configured end-on because the seats can be repositioned.' },

  { id: 'mill',
    demand: 'A site-specific piece in a disused mill. The audience walks from room to room with the performers, and not every moment is visible to everyone.',
    offer: ['prom', 'round', 'trav', 'thrust'],
    test: function (c) { return !!c.mobile; },
    draw: ovProm,
    fb: {
      prom: 'no fixed seating at all: the audience becomes part of the world of the play and moves through it. That is why sightlines cannot be guaranteed — a pillar or a crowd can hide the action.',
      round: 'you chose in the round. It surrounds the action too, but the audience is seated and the action stays in one central space. Nobody walks to the next room.',
      trav: 'you chose traverse. Two seated banks with a corridor between them is a fixed room with fixed sightlines. This piece has neither.',
      thrust: 'you chose thrust. Three sides brings them close, but they are still seated in front of one playing area, and the director controls what every seat can see.',
      none: 'you said the choice does not matter. Promenade hands part of the control away: the audience’s distance is uncontrolled and their sightlines are not guaranteed. No seated configuration does that.'
    },
    note: 'Promenade needs careful stage management because sightlines cannot be guaranteed.' }
  ];

  var NONE_TEXT = 'Any of them — the configuration is only where the seats go, so the performance would be the same.';

  /* The answer is derived, never authored: exactly one offered configuration
     satisfies the brief's predicate over sides / arch / mobile. */
  (function deriveAnswers() {
    for (var i = 0; i < ROUNDS.length; i++) {
      var r = ROUNDS[i], win = [];
      for (var j = 0; j < r.offer.length; j++) {
        if (r.test(CFG[r.offer[j]])) win.push(r.offer[j]);
      }
      r.answer = win.length === 1 ? win[0] : null;
    }
  })();

  /* ---- mount ------------------------------------------------------------
     No transition, no animation, no timer anywhere, so ctx.reducedMotion
     needs no branch: nothing ever moves unasked. */
  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = ctx.accent ||
      (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';

    /* clip-path ids are document-wide, so two mounts on one page must not
       share them */
    var uid = 't' + Math.floor(Math.random() * 1e9).toString(36);

    var wrap = document.createElement('div');
    wrap.className = 'svw-thtr';
    wrap.style.setProperty('--t-acc', accent);

    var style = document.createElement('style');
    style.textContent = CSS;
    wrap.appendChild(style);

    wrap.insertAdjacentHTML('beforeend',
      '<p class="t-kick">Theatre spaces</p>' +
      '<p class="t-title">Where does the audience sit?</p>' +
      '<p class="t-frame">Before a set is built, the director fixes where the audience sits. ' +
      'Choose the configuration each brief demands.</p>' +
      '<p class="t-brief" id="tbrief"></p>' +
      '<div class="t-stage">' +
        '<svg class="t-plan" viewBox="0 0 320 118" role="img" id="tplan">' +
          '<defs>' +
            '<clipPath id="plan-' + uid + '"><rect x="0" y="0" width="320" height="118"/></clipPath>' +
            '<clipPath id="room-' + uid + '"><rect id="troom" x="0" y="0" width="320" height="118"/></clipPath>' +
          '</defs>' +
          '<g id="tbase"></g><g id="tov" clip-path="url(#plan-' + uid + ')"></g>' +
        '</svg>' +
      '</div>' +
      '<p class="t-cap" id="tcap"></p>' +
      '<div class="t-opts" id="topts">' +
        '<div class="t-grid" id="tgrid" role="group" aria-labelledby="tbrief"></div>' +
        '<button type="button" class="t-none" id="tnone" aria-pressed="false"></button>' +
      '</div>' +
      '<div class="t-fb" id="tfb">' +
        '<span class="t-flag" id="tflag"></span>' +
        '<p class="t-say" id="tsay"></p>' +
        '<p class="t-note" id="tnote"></p>' +
      '</div>' +
      '<div class="t-act"><p class="t-run" id="trun"></p>' +
        '<button type="button" class="t-go" id="tgo" disabled>Check</button></div>' +
      '<p class="t-sr" id="tsr" aria-live="polite"></p>');

    root.appendChild(wrap);

    var elBrief = wrap.querySelector('#tbrief');
    var elBase = wrap.querySelector('#tbase');
    var elOv = wrap.querySelector('#tov');
    var elPlan = wrap.querySelector('#tplan');
    var elCap = wrap.querySelector('#tcap');
    var elOpts = wrap.querySelector('#topts');
    var elGrid = wrap.querySelector('#tgrid');
    var elNone = wrap.querySelector('#tnone');
    var elFb = wrap.querySelector('#tfb');
    var elFlag = wrap.querySelector('#tflag');
    var elSay = wrap.querySelector('#tsay');
    var elNote = wrap.querySelector('#tnote');
    var elRun = wrap.querySelector('#trun');
    var elGo = wrap.querySelector('#tgo');
    var elSr = wrap.querySelector('#tsr');
    var elRoom = wrap.querySelector('#troom');

    /* shadows are clipped to the room that casts them, so a wedge never
       spills across the whole plan */
    var env = {
      clipTo: function (r) {
        elRoom.setAttribute('x', r.x); elRoom.setAttribute('y', r.y);
        elRoom.setAttribute('width', r.w); elRoom.setAttribute('height', r.h);
        return put(elOv, 'g', { 'clip-path': 'url(#room-' + uid + ')' });
      }
    };

    elNone.textContent = NONE_TEXT;

    /* the four configuration chips are built once and re-labelled per brief */
    var chips = [], i;
    for (i = 0; i < 4; i++) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 't-chip';
      b.setAttribute('aria-pressed', 'false');
      b.appendChild(document.createElementNS(NS, 'svg'));
      b.appendChild(document.createElement('span'));
      b.addEventListener('click', onPick);
      elGrid.appendChild(b);
      chips.push(b);
    }
    elNone.addEventListener('click', onPick);

    var state = { streak: 0, mastered: false, attempted: 0 };
    var order = [], cursor = 0, round = null, shown = [], picked = null, revealed = false;

    function shuffle(a) {
      for (var j = a.length - 1; j > 0; j--) {
        var k = Math.floor(Math.random() * (j + 1)), t = a[j]; a[j] = a[k]; a[k] = t;
      }
      return a;
    }

    function setPlan(id) {
      drawPlan(elBase, id);
      while (elOv.firstChild) elOv.removeChild(elOv.firstChild);
      elPlan.setAttribute('aria-label', id
        ? 'Plan: ' + CFG[id].name + ' — audience on ' + CFG[id].cap
        : 'Plan of an empty room, before the audience is placed.');
      elCap.textContent = id ? CFG[id].name + ' — audience on ' + CFG[id].cap
        : 'The room, before the seats are placed.';
      if (id === 'prom') {
        elCap.textContent = CFG.prom.name + ' — ' + CFG.prom.cap;
        elPlan.setAttribute('aria-label', 'Plan: promenade — ' + CFG.prom.cap);
      }
    }

    function nextRound() {
      if (cursor >= order.length) {
        var last = order.length ? order[order.length - 1] : -1;
        order = shuffle(ROUNDS.map(function (_, n) { return n; }));
        if (order[0] === last && order.length > 1) {
          var t = order[0]; order[0] = order[1]; order[1] = t;
        }
        cursor = 0;
      }
      round = ROUNDS[order[cursor++]];
      shown = shuffle(round.offer.slice());
      picked = null;
      revealed = false;

      elBrief.textContent = round.demand;
      for (var m = 0; m < chips.length; m++) {
        var icon = chipIcon(shown[m]);
        chips[m].replaceChild(icon, chips[m].firstChild);
        chips[m].lastChild.textContent = CFG[shown[m]].name;
        chips[m].setAttribute('aria-pressed', 'false');
        chips[m].setAttribute('aria-label', CFG[shown[m]].name +
          ': audience on ' + CFG[shown[m]].cap);
        chips[m].disabled = false;
      }
      elNone.setAttribute('aria-pressed', 'false');
      elNone.disabled = false;
      elOpts.classList.remove('gone');
      elFb.classList.remove('on');
      elGo.textContent = 'Check';
      elGo.disabled = true;
      setPlan(null);
      publish();
    }

    function onPick(ev) {
      if (revealed) return;
      var b = ev.currentTarget;
      var idx = chips.indexOf(b);
      picked = (idx >= 0) ? shown[idx] : 'none';
      for (var e = 0; e < chips.length; e++) {
        chips[e].setAttribute('aria-pressed', chips[e] === b ? 'true' : 'false');
      }
      elNone.setAttribute('aria-pressed', b === elNone ? 'true' : 'false');
      setPlan(idx >= 0 ? shown[idx] : null);
      if (idx < 0) {
        elCap.textContent = 'No configuration set — the seats stay where they were.';
      }
      elGo.disabled = false;
      publish();
    }

    function reveal() {
      revealed = true;
      state.attempted++;
      var right = (picked === round.answer);
      if (right) {
        state.streak++;
        if (state.streak >= 3) state.mastered = true;
      } else {
        state.streak = 0;
      }

      setPlan(round.answer);
      round.draw(elOv, env);

      elFlag.textContent = right ? 'Right' : 'Not quite';
      elFlag.className = 't-flag ' + (right ? 'ok' : 'no');
      elSay.textContent = '— ' + round.fb[picked] +
        (right && state.streak === 3
          ? ' That is three in a row: the configuration decides what the design and the blocking can even attempt.'
          : '');
      elNote.textContent = round.note;
      elOpts.classList.add('gone');
      elFb.classList.add('on');

      if (state.streak >= 3) {
        elRun.textContent = 'Three in a row — you have it.';
        elGo.textContent = 'Another anyway';
      } else if (right) {
        elRun.textContent = state.streak === 1
          ? '1 right in a row — two more.'
          : '2 right in a row — one more.';
        elGo.textContent = 'Next brief';
      } else {
        elRun.textContent = state.attempted > 1 ? 'Run back to nought.' : '';
        elGo.textContent = 'Next brief';
      }
      elSr.textContent = (right ? 'Right. ' : 'Not quite. ') + elSay.textContent +
        ' The plan now shows ' + CFG[round.answer].name + '.';
      publish();
    }

    elGo.addEventListener('click', function () {
      if (!revealed) {
        if (!picked) return;
        reveal();
      } else {
        nextRound();
      }
      elGo.focus();
    });

    wrap.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && !revealed && picked) {
        picked = null;
        for (var g = 0; g < chips.length; g++) chips[g].setAttribute('aria-pressed', 'false');
        elNone.setAttribute('aria-pressed', 'false');
        setPlan(null);
        elGo.disabled = true;
        publish();
      }
    });

    function publish() {
      root.dataset.svState = JSON.stringify({
        brief: round ? round.id : null,
        sidesOffered: round ? shown.map(function (id) { return CFG[id].sides.length; }) : [],
        picked: picked,
        answer: revealed && round ? round.answer : null,
        right: revealed ? (picked === round.answer) : null,
        revealed: revealed,
        streak: state.streak,
        mastered: state.mastered,
        attempted: state.attempted
      });
    }

    nextRound();
  }

  window.SVWidget = {
    meta: {
      id: 'theatre-configuration-impact',
      title: 'Theatre spaces: where does the audience sit?',
      teaches: 'Each staging configuration is a different performer-audience contract, not a seating variant: the number of sides decides what can be built, where an actor can stand, and who sees the back.'
    },
    mount: mount
  };
})();
