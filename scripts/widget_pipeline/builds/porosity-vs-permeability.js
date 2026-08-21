/* Porosity is not permeability - StudyVault lesson widget.
   The student reads a grain-scale sample, commits a porosity band AND a
   permeability band, then sends water in. Both the verdict and the water
   animation are derived from one model: a rasterised pore grid plus a
   flood fill, so the picture and the answer key cannot drift apart. */
(function () {
  'use strict';

  /* ---------- model space ---------- */
  var MW = 240, MH = 96;          /* drawing units; grid is 1 unit per cell */
  var GX = 240, GY = 96;
  var TOP = 10, BOT = 88;         /* the rock occupies rows TOP .. BOT-1 */
  var POR_HIGH = 25;              /* % pore space at or above this = high band */
  var THROAT_MIN = 0.01;          /* mm - below this, flow is negligible */
  var SPAN_MIN = 0.5;             /* share of pores joined top-to-bottom */
  var DUR = 2000;                 /* ms of water animation */
  var WIDE = 520;

  var C = {
    air: '#ffffff', pore: '#f4efe4', grain: '#c3b8a5', grain2: '#a3977f',
    matrix: '#ada191', hair: 'rgba(45,42,38,0.20)', water: '#4a7fa1'
  };

  function rnd(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      var t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function easeOut(p) { return 1 - Math.pow(1 - p, 2.2); }

  /* ---------- the samples ---------- */
  function genSandstone() {
    var r = rnd(1907), sh = [], row = 0, dx = 13.5, dy = 13.0, x, y;
    for (y = TOP - 8; y < BOT + 8; y += dy, row++) {
      for (x = -8; x < MW + 8; x += dx) {
        sh.push({ t: 'c', x: x + (row % 2 ? dx / 2 : 0) + (r() - 0.5) * 2.6,
                  y: y + (r() - 0.5) * 2.6, r: 6.15 + (r() - 0.5) * 1.2 });
      }
    }
    return sh;
  }
  function genClay() {
    var r = rnd(4231), sh = [], i;
    for (i = 0; i < 1250; i++) {
      sh.push({ t: 'r', x: r() * MW, y: TOP - 3 + r() * (BOT - TOP + 6),
                w: 5 + r() * 4.2, h: 1.3 + r() * 0.8, a: r() * Math.PI });
    }
    return sh;
  }
  function genBasalt() {
    var r = rnd(88117), sh = [], tries = 0, area = 0, i, ok, rad, x, y;
    var target = 0.335 * MW * (BOT - TOP);
    while (area < target && tries < 40000) {
      tries++;
      rad = 2.4 + r() * r() * 5.4;
      x = rad + r() * (MW - 2 * rad); y = TOP + rad + r() * (BOT - TOP - 2 * rad);
      ok = true;
      for (i = 0; i < sh.length; i++) {
        if (Math.hypot(sh[i].x - x, sh[i].y - y) < sh[i].r + rad + 1.5) { ok = false; break; }
      }
      if (ok) { sh.push({ t: 'c', x: x, y: y, r: rad }); area += Math.PI * rad * rad; }
    }
    return sh;
  }
  function genGranite() {
    var r = rnd(5501), sh = [], pts = [], x = MW * 0.44, y, i, k, bx, by, bp, m;
    for (y = TOP - 6; y <= BOT + 6; y += 7) {
      pts.push({ x: x, y: y });
      x += (r() - 0.5) * 17; x = Math.max(22, Math.min(MW - 22, x));
    }
    sh.push({ t: 'f', pts: pts, hw: 1.25 });
    m = pts[Math.floor(pts.length * 0.55)];
    bp = [{ x: m.x, y: m.y }]; bx = m.x; by = m.y;
    for (k = 0; k < 5; k++) { bx += 13 + r() * 9; by += (r() - 0.35) * 9; bp.push({ x: bx, y: by }); }
    sh.push({ t: 'f', pts: bp, hw: 0.85 });
    for (i = 0; i < 44; i++) {
      sh.push({ t: 'c', x: r() * MW, y: TOP + r() * (BOT - TOP), r: 0.5 + r() * 0.7 });
    }
    return sh;
  }
  function genPoorly() {
    var r = rnd(3313), sh = [], big = [], i, tries, rad, x, y, ok, inside, fines = 0;
    for (tries = 0; tries < 600 && big.length < 15; tries++) {
      rad = 8 + r() * 6; x = r() * MW; y = TOP + r() * (BOT - TOP); ok = true;
      for (i = 0; i < big.length; i++) {
        if (Math.hypot(big[i].x - x, big[i].y - y) < big[i].r + rad + 0.6) { ok = false; break; }
      }
      if (ok) big.push({ t: 'c', x: x, y: y, r: rad, tone: 1 });
    }
    sh = big.slice();
    for (tries = 0; tries < 2200; tries++) {
      rad = 2.6 + r() * 3.2; x = r() * MW; y = TOP + r() * (BOT - TOP); ok = true;
      for (i = 0; i < sh.length; i++) {
        if (Math.hypot(sh[i].x - x, sh[i].y - y) < sh[i].r + rad + 0.3) { ok = false; break; }
      }
      if (ok) sh.push({ t: 'c', x: x, y: y, r: rad, tone: 1 });
    }
    for (tries = 0; tries < 90000 && fines < 6000; tries++) {
      rad = 0.75 + r() * 1.05; x = r() * MW; y = TOP - 2 + r() * (BOT - TOP + 4); inside = false;
      for (i = 0; i < big.length; i++) {
        if (Math.hypot(big[i].x - x, big[i].y - y) < big[i].r * 0.86) { inside = true; break; }
      }
      if (inside) continue;
      sh.push({ t: 'c', x: x, y: y, r: rad, tone: 0 }); fines++;
    }
    return sh;
  }

  var ROCKS = [
    { id: 'sandstone', name: 'Well-sorted sandstone', mode: 'grains', gen: genSandstone,
      throatMm: 0.05, barUnits: 50, barLabel: '1 mm',
      mech: 'High porosity (about {P}%) and permeable: even-sized grains leave open, joined pores, so water streams through. Aquifer rock.' },
    { id: 'clay', name: 'Clay', mode: 'grains', gen: genClay,
      throatMm: 0.0006, barUnits: 33, barLabel: '0.01 mm',
      mech: 'High porosity (about {P}%), more than sandstone, yet impermeable: pores under 0.001 mm hold water fast. That is a caprock.' },
    { id: 'basalt', name: 'Vesicular basalt', mode: 'voids', gen: genBasalt,
      throatMm: 1.5, barUnits: 50, barLabel: '10 mm',
      mech: 'High porosity (about {P}%) but impermeable: the bubbles are sealed off from each other, so water soaks in at the top and stops.' },
    { id: 'granite', name: 'Fractured granite', mode: 'voids', gen: genGranite, crystals: true,
      throatMm: 2.5, barUnits: 50, barLabel: '50 mm',
      mech: 'Low porosity (about {P}%) yet permeable: the fracture runs top to bottom, so water streams along it. Cracks carry the flow.' },
    { id: 'poorly', name: 'Poorly sorted sandstone', mode: 'grains', gen: genPoorly,
      throatMm: 0.002, barUnits: 50, barLabel: '1 mm',
      mech: 'Low porosity (about {P}%) and impermeable: silt fills the gaps between the grains, pinching what is left too fine to pass water.' }
  ];

  /* ---------- rasterise + flood fill ---------- */
  function distSeg(px, py, a, b) {
    var vx = b.x - a.x, vy = b.y - a.y, wx = px - a.x, wy = py - a.y;
    var L = vx * vx + vy * vy, t = L ? (wx * vx + wy * vy) / L : 0;
    t = t < 0 ? 0 : t > 1 ? 1 : t;
    return Math.hypot(px - (a.x + t * vx), py - (a.y + t * vy));
  }
  function mark(g, s, val) {
    var x, y, x0, x1, y0, y1, dx, dy, ca, sa, ex, ey, lx, ly, k, a, b;
    if (s.t === 'c') {
      x0 = Math.floor(s.x - s.r); x1 = Math.ceil(s.x + s.r);
      y0 = Math.floor(s.y - s.r); y1 = Math.ceil(s.y + s.r);
      for (y = Math.max(TOP, y0); y <= Math.min(BOT - 1, y1); y++) {
        for (x = Math.max(0, x0); x <= Math.min(GX - 1, x1); x++) {
          dx = x + 0.5 - s.x; dy = y + 0.5 - s.y;
          if (dx * dx + dy * dy <= s.r * s.r) g[y * GX + x] = val;
        }
      }
    } else if (s.t === 'r') {
      ca = Math.cos(s.a); sa = Math.sin(s.a);
      ex = (Math.abs(s.w * ca) + Math.abs(s.h * sa)) / 2 + 1;
      ey = (Math.abs(s.w * sa) + Math.abs(s.h * ca)) / 2 + 1;
      for (y = Math.max(TOP, Math.floor(s.y - ey)); y <= Math.min(BOT - 1, Math.ceil(s.y + ey)); y++) {
        for (x = Math.max(0, Math.floor(s.x - ex)); x <= Math.min(GX - 1, Math.ceil(s.x + ex)); x++) {
          dx = x + 0.5 - s.x; dy = y + 0.5 - s.y;
          lx = dx * ca + dy * sa; ly = -dx * sa + dy * ca;
          if (Math.abs(lx) <= s.w / 2 && Math.abs(ly) <= s.h / 2) g[y * GX + x] = val;
        }
      }
    } else if (s.t === 'f') {
      for (k = 1; k < s.pts.length; k++) {
        a = s.pts[k - 1]; b = s.pts[k];
        y0 = Math.floor(Math.min(a.y, b.y) - s.hw - 1); y1 = Math.ceil(Math.max(a.y, b.y) + s.hw + 1);
        x0 = Math.floor(Math.min(a.x, b.x) - s.hw - 1); x1 = Math.ceil(Math.max(a.x, b.x) + s.hw + 1);
        for (y = Math.max(TOP, y0); y <= Math.min(BOT - 1, y1); y++) {
          for (x = Math.max(0, x0); x <= Math.min(GX - 1, x1); x++) {
            if (distSeg(x + 0.5, y + 0.5, a, b) <= s.hw) g[y * GX + x] = val;
          }
        }
      }
    }
  }
  function bfs(g, fromTop) {
    var depth = new Int32Array(GX * GY).fill(-1);
    var parent = new Int32Array(GX * GY).fill(-1);
    var q = new Int32Array(GX * GY), head = 0, tail = 0, x, i, c, cx, cy, d, k, nx, ny, n;
    var y0 = fromTop ? TOP : BOT - 1;
    for (x = 0; x < GX; x++) { i = y0 * GX + x; if (g[i] === 0) { depth[i] = 0; q[tail++] = i; } }
    while (head < tail) {
      c = q[head++]; cx = c % GX; cy = (c - cx) / GX; d = depth[c] + 1;
      for (k = 0; k < 4; k++) {
        nx = cx + (k === 0 ? 1 : k === 1 ? -1 : 0);
        ny = cy + (k === 2 ? 1 : k === 3 ? -1 : 0);
        if (nx < 0 || nx >= GX || ny < TOP || ny >= BOT) continue;
        n = ny * GX + nx;
        if (g[n] !== 0 || depth[n] >= 0) continue;
        depth[n] = d; parent[n] = c; q[tail++] = n;
      }
    }
    return { depth: depth, parent: parent };
  }
  function analyse(rock) {
    if (rock.model) return rock.model;
    var shapes = rock.gen();
    var g = new Uint8Array(GX * GY), x, y, i;
    for (y = 0; y < GY; y++) {
      for (x = 0; x < GX; x++) g[y * GX + x] = (y < TOP || y >= BOT) ? 2 : (rock.mode === 'grains' ? 0 : 1);
    }
    for (i = 0; i < shapes.length; i++) mark(g, shapes[i], rock.mode === 'grains' ? 1 : 0);

    var pore = 0, total = 0;
    for (y = TOP; y < BOT; y++) {
      for (x = 0; x < GX; x++) { total++; if (g[y * GX + x] === 0) pore++; }
    }
    var porosity = 100 * pore / total;
    var down = bfs(g, true), up = bfs(g, false), span = 0;
    for (i = 0; i < g.length; i++) if (g[i] === 0 && down.depth[i] >= 0 && up.depth[i] >= 0) span++;
    var spanFrac = pore ? span / pore : 0;
    var permeable = spanFrac >= SPAN_MIN && rock.throatMm >= THROAT_MIN;
    var capRow = (permeable || rock.throatMm >= THROAT_MIN) ? BOT
                 : TOP + Math.round(0.30 * (BOT - TOP));

    /* cells the water can wet, in the order it reaches them */
    var wet = [];
    for (i = 0; i < g.length; i++) {
      if (g[i] === 0 && down.depth[i] >= 0 && ((i - i % GX) / GX) <= capRow) wet.push(i);
    }
    wet.sort(function (a, b) { return down.depth[a] - down.depth[b]; });

    /* flow paths: shortest routes from the surface to the base */
    var exits = [], paths = [], p, clash, pts, cur, guard, ex;
    for (x = 0; x < GX; x++) {
      i = (BOT - 1) * GX + x;
      if (g[i] === 0 && down.depth[i] >= 0) exits.push(i);
    }
    exits.sort(function (a, b) { return down.depth[a] - down.depth[b]; });
    for (i = 0; i < exits.length && paths.length < 4; i++) {
      ex = exits[i] % GX; clash = false;
      for (p = 0; p < paths.length; p++) if (Math.abs(paths[p].exitX - ex) < 26) clash = true;
      if (clash) continue;
      pts = []; cur = exits[i]; guard = 0;
      while (cur >= 0 && guard++ < GX * GY) { pts.push(cur); cur = down.parent[cur]; }
      pts.reverse();
      paths.push({ exitX: ex, cells: pts });
    }

    rock.model = {
      shapes: shapes, porosity: porosity, spanFrac: spanFrac, permeable: permeable,
      porBand: porosity >= POR_HIGH ? 'high' : 'low', wet: wet, paths: paths
    };
    return rock.model;
  }

  /* ---------- styles (every selector scoped to .svw-pvp) ---------- */
  var CSS =
  '.svw-pvp{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2d2a26;line-height:1.45}' +
  '.svw-pvp *{box-sizing:border-box}' +
  '.svw-pvp-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}' +
  '.svw-pvp-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--pvp-a);margin:0 0 .15rem}' +
  '.svw-pvp-h{font-family:"Source Serif 4",Georgia,serif;font-size:1.22rem;font-weight:600;line-height:1.2;margin:0 0 .3rem}' +
  '.svw-pvp-frame{font-size:.82rem;color:#5b564e;margin:0 0 .65rem;max-width:64ch}' +
  '.svw-pvp-band{display:grid;gap:.65rem;align-items:start}' +
  '.svw-pvp.is-wide .svw-pvp-band{grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:1.1rem}' +
  '.svw-pvp-cvs{display:block;margin:0 auto;border-radius:10px;border:1px solid #e0d9cd}' +
  '.svw-pvp-note{font-size:.72rem;color:#8d8880;margin:.3rem 0 0;text-align:center;font-variant-numeric:tabular-nums}' +
  '.svw-pvp-step{margin:0 0 .45rem}' +
  '.svw-pvp-lab{display:flex;align-items:center;gap:.35rem;font-size:.7rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#8d8880;margin:0 0 .28rem}' +
  '.svw-pvp-n{display:inline-flex;align-items:center;justify-content:center;width:1.1rem;height:1.1rem;border-radius:50%;background:var(--pvp-s);color:var(--pvp-a);font-size:.66rem;font-weight:700;letter-spacing:0}' +
  '.svw-pvp-opts{display:grid;grid-template-columns:1fr 1fr;gap:.4rem}' +
  '.svw-pvp-opt{-webkit-appearance:none;appearance:none;display:block;width:100%;text-align:left;font-family:inherit;font-size:.82rem;font-weight:600;color:#2d2a26;background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.4rem .55rem;cursor:pointer}' +
  '.svw-pvp-opt .g{display:block;font-size:.7rem;font-weight:500;line-height:1.2;color:#8d8880;margin-top:.08rem}' +
  '.svw-pvp-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff}' +
  '.svw-pvp-opt[aria-pressed="true"] .g{color:#cfc8bd}' +
  '.svw-pvp-opt.is-key{border-color:#4f7d63;box-shadow:inset 0 0 0 1px #4f7d63}' +
  '.svw-pvp-opt[disabled]{cursor:default}' +
  '.svw-pvp-opt[disabled][aria-pressed="false"]{opacity:.55}' +
  '.svw-pvp-go{-webkit-appearance:none;appearance:none;font-family:inherit;font-size:.82rem;font-weight:600;color:#fff;background:#2d2a26;border:1px solid #2d2a26;border-radius:10px;padding:.5rem .95rem;cursor:pointer;margin-top:.15rem}' +
  '.svw-pvp-go[disabled]{opacity:.4;cursor:default}' +
  '.svw-pvp-run{font-size:.76rem;color:#8d8880;min-height:1.15rem;margin:.3rem 0 0}' +
  '.svw-pvp-cap{font-size:.84rem;line-height:1.5;margin:.6rem 0 0;padding-top:.55rem;border-top:1px solid #efe9e0;min-height:5rem}';

  /* ---------- mount ---------- */
  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = ctx.accent ||
      (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#8a6a4f';
    var reduced = !!ctx.reducedMotion;

    root.className = (root.className ? root.className + ' ' : '') + 'svw-pvp';
    root.style.setProperty('--pvp-a', accent);
    root.style.setProperty('--pvp-s', accent + '22');

    var st = document.createElement('style');
    st.textContent = CSS;
    root.appendChild(st);

    function el(tag, cls, txt) {
      var n = document.createElement(tag);
      if (cls) n.className = cls;
      if (txt != null) n.textContent = txt;
      return n;
    }

    root.appendChild(el('p', 'svw-pvp-kick', 'Groundwater'));
    root.appendChild(el('h3', 'svw-pvp-h', 'Will the water get through?'));
    root.appendChild(el('p', 'svw-pvp-frame',
      'A water company is drilling for groundwater. Predict this sample’s porosity, then its permeability.'));

    var band = el('div', 'svw-pvp-band');
    var stage = el('div', 'svw-pvp-stage');
    var cvs = document.createElement('canvas');
    cvs.className = 'svw-pvp-cvs';
    cvs.setAttribute('role', 'img');
    stage.appendChild(cvs);
    var note = el('p', 'svw-pvp-note', '');
    stage.appendChild(note);
    band.appendChild(stage);

    var panel = el('div', 'svw-pvp-panel');
    var opts = { por: {}, perm: {} };

    function stepRow(num, label, group, defs) {
      var wrap = el('div', 'svw-pvp-step');
      var lab = el('p', 'svw-pvp-lab');
      lab.appendChild(el('span', 'svw-pvp-n', num));
      lab.appendChild(el('span', null, label));
      wrap.appendChild(lab);
      var row = el('div', 'svw-pvp-opts');
      defs.forEach(function (d) {
        var b = el('button', 'svw-pvp-opt');
        b.type = 'button';
        b.setAttribute('aria-pressed', 'false');
        b.appendChild(el('span', null, d.head));
        b.appendChild(el('span', 'g', d.gloss));
        b.addEventListener('click', function () { pick(group, d.val); });
        opts[group][d.val] = b;
        row.appendChild(b);
      });
      wrap.appendChild(row);
      return wrap;
    }

    panel.appendChild(stepRow('1', 'Porosity', 'por', [
      { val: 'high', head: 'High', gloss: 'a quarter or more is pore space' },
      { val: 'low', head: 'Low', gloss: 'under a tenth is pore space' }
    ]));
    panel.appendChild(stepRow('2', 'Permeability', 'perm', [
      { val: 'permeable', head: 'Permeable', gloss: 'water flows through it' },
      { val: 'impermeable', head: 'Impermeable', gloss: 'water is held, not passed' }
    ]));

    var go = el('button', 'svw-pvp-go', 'Test it with water');
    go.type = 'button';
    go.disabled = true;
    panel.appendChild(go);
    var run = el('p', 'svw-pvp-run', '');
    panel.appendChild(run);
    band.appendChild(panel);
    root.appendChild(band);

    var cap = el('p', 'svw-pvp-cap', '');
    root.appendChild(cap);
    var sr = el('p', 'svw-pvp-sr', '');
    sr.setAttribute('aria-live', 'polite');
    root.appendChild(sr);

    /* ---------- state ---------- */
    var deck = [], roundNo = 0, rock = null, model = null;
    var picked = { por: null, perm: null };
    var committed = false, streak = 0, mastered = false, attempted = 0, lastRight = null;
    var x2 = cvs.getContext('2d'), baseCvs = null, wetCvs = null, wx = null, wetImg = null;
    var wetShown = 0, raf = 0, animStart = 0, scale = 1;

    function shuffleRest() {
      var rest = [1, 2, 3, 4], i, j, t;
      for (i = rest.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1)); t = rest[i]; rest[i] = rest[j]; rest[j] = t;
      }
      return rest;
    }
    function nextRock() {
      if (!deck.length) {
        deck = roundNo === 1 ? shuffleRest() : shuffleRest().concat([0]);
      }
      return ROCKS[deck.shift()];
    }

    function state() {
      root.dataset.svState = JSON.stringify({
        round: roundNo, sample: rock ? rock.id : null,
        porosityPct: model ? Math.round(model.porosity) : null,
        permeable: model ? model.permeable : null,
        picked: picked.por + '/' + picked.perm,
        committed: committed, correct: lastRight,
        streak: streak, mastered: mastered, attempted: attempted
      });
    }

    function layout() {
      var avail = root.clientWidth || 320;
      var wide = avail >= WIDE;
      if (wide) root.classList.add('is-wide'); else root.classList.remove('is-wide');
      var box = stage.clientWidth || (wide ? avail / 2 : avail);
      var maxH = wide ? 176 : 146;
      var cw = Math.max(180, Math.min(box, Math.round(maxH * MW / MH)));
      var ch = Math.round(cw * MH / MW);
      var dpr = Math.min(2, window.devicePixelRatio || 1);
      cvs.style.width = cw + 'px'; cvs.style.height = ch + 'px';
      cvs.width = Math.round(cw * dpr); cvs.height = Math.round(ch * dpr);
      scale = cvs.width / MW;
      drawBase();
      paint(committed ? 1 : 0);
    }

    /* ---------- drawing ---------- */
    function drawBase() {
      if (!rock || !cvs.width) return;
      baseCvs = document.createElement('canvas');
      baseCvs.width = cvs.width; baseCvs.height = cvs.height;
      var b = baseCvs.getContext('2d'), i, s, p, k = scale, r, cx, cy, a, L;
      b.fillStyle = C.air; b.fillRect(0, 0, baseCvs.width, baseCvs.height);
      b.save(); b.scale(k, k);
      b.beginPath(); b.rect(0, TOP, MW, BOT - TOP); b.clip();
      b.fillStyle = rock.mode === 'grains' ? C.pore : C.matrix;
      b.fillRect(0, TOP, MW, BOT - TOP);
      if (rock.crystals) {
        r = rnd(77);
        b.strokeStyle = 'rgba(45,42,38,0.11)'; b.lineWidth = 0.55;
        for (i = 0; i < 30; i++) {
          cx = r() * MW; cy = TOP + r() * (BOT - TOP); a = r() * Math.PI; L = 10 + r() * 28;
          b.beginPath();
          b.moveTo(cx - Math.cos(a) * L / 2, cy - Math.sin(a) * L / 2);
          b.lineTo(cx + Math.cos(a) * L / 2, cy + Math.sin(a) * L / 2);
          b.stroke();
        }
      }
      b.lineWidth = 0.32; b.strokeStyle = C.hair;
      for (i = 0; i < model.shapes.length; i++) {
        s = model.shapes[i];
        b.fillStyle = rock.mode === 'voids' ? C.pore : (s.tone === 1 ? C.grain2 : C.grain);
        if (s.t === 'c') {
          b.beginPath(); b.arc(s.x, s.y, s.r, 0, 6.2832); b.fill();
          if (s.r > 2.4) b.stroke();
        } else if (s.t === 'r') {
          b.save(); b.translate(s.x, s.y); b.rotate(s.a);
          b.fillRect(-s.w / 2, -s.h / 2, s.w, s.h); b.restore();
        } else if (s.t === 'f') {
          b.beginPath(); b.moveTo(s.pts[0].x, s.pts[0].y);
          for (p = 1; p < s.pts.length; p++) b.lineTo(s.pts[p].x, s.pts[p].y);
          b.lineWidth = s.hw * 2; b.lineJoin = 'round'; b.lineCap = 'round';
          b.strokeStyle = C.pore; b.stroke();
          b.lineWidth = 0.32; b.strokeStyle = C.hair;
        }
      }
      b.restore();
      /* scale bar on a plate, so it stays legible over pale samples too */
      b.save(); b.scale(k, k);
      var L2 = rock.barUnits, bx = MW - 9 - L2, by = BOT - 6.5;
      b.fillStyle = 'rgba(45,42,38,0.46)';
      b.fillRect(bx - 4, by - 4.6, L2 + 8, 9.2);
      b.lineCap = 'butt';
      b.strokeStyle = '#fff'; b.lineWidth = 1.3; barPath(b, bx, by, L2); b.stroke();
      b.restore();
      wetCvs = document.createElement('canvas'); wetCvs.width = GX; wetCvs.height = GY;
      wx = wetCvs.getContext('2d');
      wetImg = wx.createImageData(GX, GY);
      wetShown = 0;
    }
    function barPath(b, bx, by, L) {
      b.beginPath();
      b.moveTo(bx, by); b.lineTo(bx + L, by);
      b.moveTo(bx, by - 2.4); b.lineTo(bx, by + 2.4);
      b.moveTo(bx + L, by - 2.4); b.lineTo(bx + L, by + 2.4);
    }
    function setWet(i) {
      var o = i * 4, d = wetImg.data;
      d[o] = 74; d[o + 1] = 127; d[o + 2] = 161; d[o + 3] = 224;
    }
    function paint(p) {
      if (!baseCvs) return;
      var W = cvs.width, H = cvs.height, k = scale, i, cells, q, idx, c, cx, cy, fall, out, ex, pond, q2;
      x2.setTransform(1, 0, 0, 1, 0, 0);
      x2.imageSmoothingEnabled = true;
      x2.clearRect(0, 0, W, H);
      x2.drawImage(baseCvs, 0, 0);
      if (!committed || p <= 0) return;

      var soak = clamp((p - 0.16) / 0.84);
      var target = Math.floor(easeOut(soak) * model.wet.length);
      if (target < wetShown) { wetImg = wx.createImageData(GX, GY); wetShown = 0; }
      while (wetShown < target) { setWet(model.wet[wetShown]); wetShown++; }
      if (wetShown > 0) { wx.putImageData(wetImg, 0, 0); x2.drawImage(wetCvs, 0, 0, W, H); }

      x2.save(); x2.scale(k, k);
      x2.fillStyle = C.water;
      if (model.permeable) {
        for (i = 0; i < model.paths.length; i++) {
          cells = model.paths[i].cells; q = clamp(p * 1.25 - i * 0.13);
          if (q <= 0) continue;
          idx = Math.min(cells.length - 1, Math.floor(q * (cells.length - 1)));
          c = cells[idx]; cx = c % GX; cy = (c - cx) / GX;
          fall = p < 0.16 ? (0.16 - p) / 0.16 * (TOP + 6) : 0;
          x2.beginPath(); x2.arc(cx + 0.5, cy + 0.5 - fall, 2.3, 0, 6.2832); x2.fill();
        }
        out = clamp((p - 0.62) / 0.38);
        if (out > 0) {
          x2.globalAlpha = 0.85;
          for (i = 0; i < model.paths.length; i++) {
            ex = model.paths[i].exitX;
            x2.beginPath();
            x2.ellipse(ex + 0.5, BOT + 2.6, 3 + out * 7, 1.2 + out * 2.2, 0, 0, 6.2832);
            x2.fill();
          }
          x2.globalAlpha = 1;
        }
      } else {
        pond = clamp((p - 0.22) / 0.78) * (TOP - 1.5);
        for (i = 0; i < 5; i++) {
          q2 = clamp(p * 5 - i * 0.35);
          if (q2 <= 0 || q2 >= 1) continue;
          x2.beginPath();
          x2.arc(28 + i * 46, -4 + q2 * (TOP + 4), 2.3, 0, 6.2832); x2.fill();
        }
        if (pond > 0.3) {
          x2.globalAlpha = 0.8;
          x2.fillRect(0, TOP - pond, MW, pond);
          x2.globalAlpha = 1;
        }
      }
      x2.restore();
    }
    function animate(ts) {
      if (!root.isConnected) { raf = 0; return; }
      if (!animStart) animStart = ts;
      var p = clamp((ts - animStart) / DUR);
      paint(p);
      if (p < 1) raf = requestAnimationFrame(animate); else raf = 0;
    }

    /* ---------- rounds ---------- */
    function newRound() {
      if (raf) { cancelAnimationFrame(raf); raf = 0; }
      roundNo++;
      rock = roundNo === 1 ? ROCKS[0] : nextRock();
      model = analyse(rock);
      picked.por = null; picked.perm = null;
      committed = false; lastRight = null;
      ['por', 'perm'].forEach(function (grp) {
        Object.keys(opts[grp]).forEach(function (v) {
          var b = opts[grp][v];
          b.setAttribute('aria-pressed', 'false');
          b.classList.remove('is-key');
          b.disabled = false;
        });
      });
      go.textContent = 'Test it with water';
      go.disabled = true;
      note.textContent = 'Sample ' + roundNo + ' · white bar = ' + rock.barLabel;
      cap.textContent = 'Grains and crystals are dark, pore space is pale. The white bar sets the scale — the magnification changes between samples.';
      cvs.setAttribute('aria-label', 'A rock sample magnified until the grains and the spaces between them are visible.');
      sr.textContent = 'New sample. ' + cap.textContent;
      animStart = 0;
      layout();
      state();
    }

    function pick(grp, val) {
      if (committed) return;
      picked[grp] = val;
      Object.keys(opts[grp]).forEach(function (v) {
        opts[grp][v].setAttribute('aria-pressed', v === val ? 'true' : 'false');
      });
      go.disabled = !(picked.por && picked.perm);
      state();
    }

    function commit() {
      if (!picked.por || !picked.perm) return;
      committed = true;
      attempted++;
      var truePerm = model.permeable ? 'permeable' : 'impermeable';
      var ok = picked.por === model.porBand && picked.perm === truePerm;
      lastRight = ok;
      streak = ok ? streak + 1 : 0;
      if (streak >= 3) mastered = true;

      var mech = rock.mech.replace('{P}', String(Math.round(model.porosity)));
      var yours = picked.por + ' porosity, ' + picked.perm;
      cap.textContent = ok ? 'Right — ' + yours + '. ' + mech
                           : 'Not quite — you said ' + yours + '. ' + mech;

      opts.por[model.porBand].classList.add('is-key');
      opts.perm[truePerm].classList.add('is-key');
      ['por', 'perm'].forEach(function (grp) {
        Object.keys(opts[grp]).forEach(function (v) { opts[grp][v].disabled = true; });
      });

      run.textContent = streak >= 3 ? 'Three in a row — you have it: space is not flow.'
        : streak === 2 ? '2 right in a row — one more and you have it.'
        : streak === 1 ? '1 right in a row — two more to go.'
        : '';
      go.disabled = false;
      go.textContent = mastered ? 'Another anyway' : 'Next sample';

      sr.textContent = cap.textContent + ' ' + (model.permeable
        ? 'The water threads down through the connected pores and drips out of the base.'
        : 'The water soaks into the top of the sample, stops, and ponds on the surface.');

      state();
      animStart = 0;
      if (reduced) paint(1); else raf = requestAnimationFrame(animate);
    }

    go.addEventListener('click', function () {
      if (committed) newRound(); else commit();
    });
    root.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !committed && (picked.por || picked.perm)) {
        picked.por = null; picked.perm = null;
        ['por', 'perm'].forEach(function (grp) {
          Object.keys(opts[grp]).forEach(function (v) { opts[grp][v].setAttribute('aria-pressed', 'false'); });
        });
        go.disabled = true;
        state();
      }
    });

    if (window.ResizeObserver) {
      var ro = new ResizeObserver(function () { if (root.isConnected) layout(); });
      ro.observe(root);
    }

    newRound();
  }

  window.SVWidget = {
    meta: {
      id: 'porosity-vs-permeability',
      title: 'Will the water get through?',
      teaches: 'Porosity is how much pore space a rock holds; permeability is whether that space is connected and wide enough for water to flow. High porosity does not guarantee high permeability.'
    },
    mount: mount
  };
})();
