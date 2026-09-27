/* StudyVault launch videos v2 — the picture. Every frame is a pure function of the frame number
   (window.renderFrame(f)), drawn on one canvas, so a render is frame-exact and repeatable.

   House rules (Tom, 27 Sep 2026): one idea per scene; the interface rebuilt as animatable parts in the
   site's own look, never cropped screenshots; transitions are objects doing something (the padlock,
   colour fields, masks, a zoom-through), never a plain cut; every line holds long enough to read
   (words x 0.3 s + 1 s); no pill shapes, no coloured left-border stripes, no hint captions.
   Fictional or free-tier content only.

   URL: comp.html?video=students|teachers&ar=16x9|1x1|9x16 [&debug=1] */
(function () {
  const Q = new URLSearchParams(location.search);
  const VIDEO = Q.get('video') || 'students', AR = Q.get('ar') || '16x9', DEBUG = Q.get('debug') === '1';
  const [W, H] = { '16x9': [1920, 1080], '9x16': [1080, 1920], '1x1': [1080, 1080] }[AR];
  const MODE = AR === '16x9' ? 'L' : AR === '1x1' ? 'S' : 'P';
  const u = MODE === 'L' ? H / 1080 : W / 1080;
  const cv = document.getElementById('c'); cv.width = W; cv.height = H;
  const ctx = cv.getContext('2d');
  const TL = window.TL, { FPS, BEAT } = TL, V = TL.VIDEOS[VIDEO];

  const PAPER = '#faf8f5', INK = '#2d2a26', RUST = '#c06325', GREEN = '#2f7d4f', MUTED = '#8a8580', AMBER = '#c9922e',
    LINE = '#e6e0d6', CARD = '#ffffff', GREEN_TINT = '#eaf4ed', RUST_TINT = '#f8e7dc', AMBER_TINT = '#f7ecd6', SOFTBG = '#f6f3ee';
  const SERIF = '"Source Serif 4", Georgia, serif', SANS = 'Inter, "Segoe UI", sans-serif', MARK = '"Young Serif", Georgia, serif';

  /* ---------- easing ---------- */
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const prog = (f, s, d) => clamp((f - s) / d);
  function bezier(x1, y1, x2, y2) {
    const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx, cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
    const sx = t => ((ax * t + bx) * t + cx) * t, sy = t => ((ay * t + by) * t + cy) * t;
    return x => { if (x <= 0) return 0; if (x >= 1) return 1; let lo = 0, hi = 1, t = x;
      for (let i = 0; i < 40; i++) { const v = sx(t); if (Math.abs(v - x) < 1e-6) break; if (v < x) lo = t; else hi = t; t = (lo + hi) / 2; } return sy(t); };
  }
  const SOFT = bezier(0.16, 1, 0.3, 1), SNAP = bezier(0.8, 0, 0, 1);
  const IN_EXPO = t => t <= 0 ? 0 : t >= 1 ? 1 : Math.pow(2, 10 * t - 10);
  const INOUT_EXPO = t => t <= 0 ? 0 : t >= 1 ? 1 : t < 0.5 ? Math.pow(2, 20 * t - 10) / 2 : (2 - Math.pow(2, -20 * t + 10)) / 2;
  const INOUT_CUBIC = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  const IN_CUBIC = t => t * t * t;
  function spring(ts, k = 380, c = 20) {
    if (ts <= 0) return 0; const w0 = Math.sqrt(k), z = c / (2 * w0);
    if (z >= 1) return 1 - Math.exp(-w0 * ts) * (1 + w0 * ts);
    const wd = w0 * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w0 * ts) * (Math.cos(wd * ts) + (z * w0 / wd) * Math.sin(wd * ts));
  }
  const sp = (f, s, k, c) => f < s ? 0 : spring((f - s) / FPS, k, c);
  const hex = h => [1, 3, 5].map(i => parseInt(h.substr(i, 2), 16));
  const mix = (a, b, t) => { const pa = hex(a), pb = hex(b); return 'rgb(' + pa.map((v, i) => Math.round(lerp(v, pb[i], clamp(t)))).join(',') + ')'; };

  /* ---------- grounds ---------- */
  const grain = document.createElement('canvas'); grain.width = grain.height = 256;
  { const g = grain.getContext('2d'), im = g.createImageData(256, 256); let s = 7;
    for (let i = 0; i < im.data.length; i += 4) { s = (s * 1103515245 + 12345) & 0x7fffffff; const v = s % 255;
      im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; } g.putImageData(im, 0, 0); }
  let grainPat = null;
  function ground(col = PAPER, dark = false) {
    ctx.fillStyle = col; ctx.fillRect(0, 0, W, H);
    if (!grainPat) grainPat = ctx.createPattern(grain, 'repeat');
    ctx.globalAlpha = dark ? 0.05 : 0.028; ctx.globalCompositeOperation = dark ? 'overlay' : 'multiply'; ctx.fillStyle = grainPat; ctx.fillRect(0, 0, W, H);
    ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
    const v = ctx.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.3, W / 2, H / 2, Math.max(W, H) * 0.75);
    v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, dark ? 'rgba(0,0,0,0.28)' : 'rgba(45,42,38,0.06)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
  }

  /* ---------- primitives ---------- */
  function rr(x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }
  function dot(x, y, r, col = RUST) { if (r <= 0) return; ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); }
  function font(fam, px, wt = 600) { return `${wt} ${px}px ${fam}`; }
  function shadowOn(blur, dy, a) { ctx.shadowColor = `rgba(45,42,38,${a})`; ctx.shadowBlur = blur; ctx.shadowOffsetY = dy; }
  function shadowOff() { ctx.shadowColor = 'transparent'; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0; }
  function text(s, x, y, fnt, col, align = 'left') { ctx.font = fnt; ctx.fillStyle = col; ctx.textAlign = align; ctx.fillText(s, x, y); ctx.textAlign = 'left'; }
  function wrap(s, fnt, maxW) { ctx.font = fnt; const out = []; let line = '';
    s.split(' ').forEach(wd => { const t = line ? line + ' ' + wd : wd; if (ctx.measureText(t).width > maxW && line) { out.push(line); line = wd; } else line = t; });
    if (line) out.push(line); return out; }
  /* the same number of lines as a greedy wrap, but as even as possible (no one-word last line) */
  function wrapBal(s, fnt, maxW) { const n = wrap(s, fnt, maxW).length; if (n < 2) return [s]; let lo = maxW * 0.4, hi = maxW;
    for (let i = 0; i < 18; i++) { const m = (lo + hi) / 2; if (wrap(s, fnt, m).length > n) lo = m; else hi = m; } return wrap(s, fnt, hi + 1); }
  /* a line rising out of an invisible slot on its own baseline */
  function maskLine(s, x, y, fnt, col, p, lh, align = 'left') {
    if (p <= 0) return; ctx.font = fnt; const w = ctx.measureText(s).width, x0 = align === 'center' ? x - w / 2 : x;
    ctx.save(); ctx.beginPath(); ctx.rect(x0 - 8 * u, y - lh * 0.9, w + 16 * u, lh * 1.18); ctx.clip();
    ctx.fillStyle = col; ctx.textAlign = 'left'; ctx.fillText(s, x0, y + (1 - p) * lh); ctx.restore(); return w;
  }
  function tickMark(cx, cy, r, drawP, col = '#fff', wid) {
    if (drawP <= 0) return; const pts = [[-0.42, 0.02], [-0.12, 0.32], [0.45, -0.3]];
    const s1 = Math.hypot(0.3, 0.3), s2 = Math.hypot(0.57, 0.62), L = (s1 + s2) * clamp(drawP);
    ctx.strokeStyle = col; ctx.lineWidth = wid || r * 0.2; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.beginPath(); ctx.moveTo(cx + pts[0][0] * r, cy + pts[0][1] * r);
    if (L <= s1) { const t = L / s1; ctx.lineTo(cx + lerp(pts[0][0], pts[1][0], t) * r, cy + lerp(pts[0][1], pts[1][1], t) * r); }
    else { ctx.lineTo(cx + pts[1][0] * r, cy + pts[1][1] * r); const t = (L - s1) / s2; ctx.lineTo(cx + lerp(pts[1][0], pts[2][0], t) * r, cy + lerp(pts[1][1], pts[2][1], t) * r); }
    ctx.stroke();
  }
  function crossMark(cx, cy, r, col = '#fff') { ctx.strokeStyle = col; ctx.lineWidth = r * 0.2; ctx.lineCap = 'round'; ctx.beginPath();
    ctx.moveTo(cx - r * 0.32, cy - r * 0.32); ctx.lineTo(cx + r * 0.32, cy + r * 0.32); ctx.moveTo(cx + r * 0.32, cy - r * 0.32); ctx.lineTo(cx - r * 0.32, cy + r * 0.32); ctx.stroke(); }
  function badge(cx, cy, r, ok, t0, f) { const s = sp(f, t0, 420, 15); if (s <= 0) return;
    const rp = prog(f, t0, 18); if (rp < 1) { ctx.strokeStyle = ok ? `rgba(47,125,79,${0.5 * (1 - rp)})` : `rgba(192,99,37,${0.5 * (1 - rp)})`; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(cx, cy, lerp(r, r * 3.4, SOFT(rp)), 0, 7); ctx.stroke(); }
    dot(cx, cy, r * s, ok ? GREEN : RUST); if (ok) tickMark(cx, cy, r * Math.max(0.01, s), prog(f, t0 + 2, 7), '#fff', r * 0.19); else if (s > 0.6) crossMark(cx, cy, r * s); }
  function button(x, y, w, h, label, f, pressAt, col = INK, doneLabel, doneAt, doneCol = GREEN) {
    let sc = 1; if (f >= pressAt && f < pressAt + 3) sc = 1 - 0.08 * (f - pressAt + 1) / 3; else if (f >= pressAt + 3) sc = lerp(0.92, 1, sp(f, pressAt + 3, 500, 22));
    const done = doneAt != null && f >= doneAt; ctx.save(); ctx.translate(x + w / 2, y + h / 2); ctx.scale(sc, sc);
    rr(-w / 2, -h / 2, w, h, 12); ctx.fillStyle = done ? mix(col, doneCol, prog(f, doneAt, 8)) : col; ctx.fill();
    text(done && doneLabel ? doneLabel : label, 0, 8, font(SANS, 22, 600), '#fff', 'center'); ctx.restore();
  }
  const LOCK = new Path2D(window.LOCK_D), KEYHOLE = new Path2D(window.KEYHOLE_D);
  /* The StudyVault padlock (the wordmark's own path, keyhole included). A real padlock opens this way:
     the shackle lifts, its short (left) leg comes out of the body, and it swings round the long (right)
     leg, which stays seated. lift is in lock units (the lock is 1280 tall); swing 0 = shut, 1 = turned
     half a turn. hole = the colour showing through the keyhole. */
  const PIVOT = 1369.3;
  function lock(cx, cy, h, lift = 0, swing = 0, col = RUST, hole = PAPER) {
    const s = h / 1280; if (s <= 0) return;
    ctx.save(); ctx.translate(cx - 1023 / 2 * s, cy - 1280 / 2 * s); ctx.scale(s, s); ctx.translate(-512, -384); ctx.fillStyle = col;
    ctx.save(); ctx.translate(0, -lift); ctx.translate(PIVOT, 0); ctx.scale(Math.cos(swing * Math.PI), 1); ctx.translate(-PIVOT, 0);
    ctx.beginPath(); ctx.rect(300, 200, 2200, 646); ctx.clip(); ctx.fill(LOCK); ctx.restore();
    if (lift > 0) { const w = Math.abs(Math.cos(swing * Math.PI)); ctx.fillRect(PIVOT - 37.8 * Math.max(0.35, w), 845 - lift, 75.6 * Math.max(0.35, w), lift + 30); }
    ctx.save(); ctx.beginPath(); ctx.rect(300, 845, 2200, 900); ctx.clip(); ctx.fill(LOCK); ctx.restore();
    ctx.fillStyle = hole; ctx.fill(KEYHOLE);
    ctx.restore();
  }

  /* ---------- layout ---------- */
  const TITLE = MODE === 'L' ? { x: 110 * u, w: 560 * u, size: 76 * u, align: 'left' }
    : MODE === 'S' ? { x: W / 2, w: 940 * u, size: 62 * u, align: 'center', top: 96 * u }
    : { x: W / 2, w: 960 * u, size: 84 * u, align: 'center', top: 300 * u };
  function panelBox(pw, ph) {
    if (MODE === 'L') { const s = Math.min(1.42, 1130 * u / pw, 860 * u / ph); return { cx: 1300 * u, cy: 545 * u, s }; }
    if (MODE === 'S') { const s = Math.min(1.14, 1000 * u / pw, 700 * u / ph); return { cx: W / 2, cy: 625 * u, s }; }
    const s = Math.min(1.22, 1010 * u / pw, 1180 * u / ph); return { cx: W / 2, cy: 1110 * u, s };
  }
  /* title: segments [{t, at (frame), col}] laid out once so nothing jumps */
  function title(segs, f, size) {
    const sz = size || TITLE.size, fnt = font(SANS, sz, 800), lh = sz * 1.1;
    ctx.letterSpacing = `${-0.03 * sz}px`;
    const lines = []; segs.forEach(sg => wrapBal(sg.t, fnt, TITLE.w).forEach((ln, i) => lines.push({ ln, at: sg.at + i * 4, col: sg.col || INK, gap: i === 0 && lines.length ? sz * 0.14 : 0 })));
    const total = lines.reduce((a, l) => a + lh + l.gap, 0);
    let y = MODE === 'L' ? H / 2 - total / 2 + sz * 0.82 : TITLE.top + sz * 0.82;
    lines.forEach(l => { y += l.gap; maskLine(l.ln, TITLE.x, y, fnt, l.col, SOFT(prog(f, l.at, 18)), lh, TITLE.align); y += lh; });
    ctx.letterSpacing = '0px';
  }
  /* a card: springs out of its anchor dot, then drifts very slightly */
  function card(pw, ph, f, inAt, draw, opts = {}) {
    const b = panelBox(pw, ph), s = sp(f, inAt, 300, 21); if (s <= 0 && !opts.always) return b;
    const k = opts.always ? 1 : s, dx = opts.dx || 0;
    ctx.save(); ctx.translate(b.cx + dx, b.cy + (opts.dy || 0)); ctx.scale(b.s * lerp(0.05, 1, k) * (opts.sc || 1), b.s * lerp(0.05, 1, k) * (opts.sc || 1));
    if (opts.rot) ctx.rotate(opts.rot);
    shadowOn(lerp(8, 60, k), lerp(4, 22, k), 0.13); rr(-pw / 2, -ph / 2, pw, ph, 18); ctx.fillStyle = mix(RUST, CARD, clamp((f - inAt) / 6)); ctx.fill(); shadowOff();
    if (f - inAt >= 6 || opts.always) { ctx.save(); ctx.translate(-pw / 2, -ph / 2); draw(); ctx.restore(); }
    ctx.restore(); return b;
  }
  const inA = (f, at) => SOFT(prog(f, at, 14));
  function item(f, at, fn) { const a = inA(f, at); if (a <= 0) return; ctx.save(); ctx.globalAlpha *= a; ctx.translate(0, (1 - a) * 14); fn(); ctx.restore(); }
  function header(pw, left, right, rightCol = MUTED) {
    text(left, 40, 50, font(SANS, 22, 600), INK); if (right) text(right, pw - 40, 50, font(SANS, 20, 500), rightCol, 'right');
    ctx.fillStyle = LINE; ctx.fillRect(0, 78, pw, 2);
  }
  function eyebrow(s, x, y, col = MUTED) { ctx.font = font(SANS, 15, 700); ctx.letterSpacing = '2.4px'; ctx.fillStyle = col; ctx.fillText(s.toUpperCase(), x, y); ctx.letterSpacing = '0px'; }

  /* ===================== panels (card space, top-left origin) ===================== */
  const FC = { w: 820, h: 460, ans: "the League's report on Manchuria",
    back: "The League of Nations' 1932 report on Manchuria. It found Japan's invasion was not self-defence." };
  function flashFront(f, k) {
    const right = f >= k.tick, pw = FC.w;
    item(f, k.in + 6, () => { header(pw, 'Flashcard revision', right ? null : 'Card 4 of 14');
      if (right) { const p = SOFT(prog(f, k.tick + 2, 14)); ctx.save(); ctx.beginPath(); ctx.rect(pw / 2, 20, pw / 2 - 36, 44); ctx.clip(); text('Right', pw - 40, 50 + (1 - p) * 34, font(SANS, 22, 700), GREEN, 'right'); ctx.restore(); } });
    item(f, k.in + 8, () => eyebrow('Who or what?', 40, 132));
    item(f, k.in + 10, () => text('The Lytton Report', 40, 192, font(SERIF, 48, 600), INK));
    item(f, k.in + 12, () => {
      const bx = 40, by = 230, bw = pw - 80, bh = 82, typing = f >= k.type && !right, gp = prog(f, k.tick, 10);
      rr(bx, by, bw, bh, 12); ctx.fillStyle = right ? mix('#fdfcfa', GREEN_TINT, gp) : '#fdfcfa'; ctx.fill();
      ctx.lineWidth = typing ? 2.5 : 2; ctx.strokeStyle = right ? mix(INK, GREEN, gp) : typing ? INK : LINE; ctx.stroke();
      const n = f < k.type ? 0 : Math.min(FC.ans.length, Math.floor((f - k.type) / (k.rate || 1.5)) + 1), s = FC.ans.slice(0, n);
      text(s || 'Type what you remember', bx + 26, by + 52, font(SANS, 28, 500), s ? INK : '#b9b2a8');
      if (typing && Math.floor(f / 8) % 2 === 0) { ctx.font = font(SANS, 28, 500); ctx.fillStyle = INK; ctx.fillRect(bx + 28 + (s ? ctx.measureText(s).width : 0), by + 24, 2.5, 36); }
      if (right) badge(bx + bw - 44, by + bh / 2, 25, true, k.tick, f);
    });
    item(f, k.in + 14, () => button(40, 346, 170, 64, 'Check', f, k.check, INK, 'Checked', k.tick));
  }
  function flashBack(f) {
    const pw = FC.w; header(pw, 'Flashcard revision', 'Right', GREEN);
    eyebrow('Model answer', 40, 132);
    const fnt = font(SERIF, 36, 600), lines = wrap(FC.back, fnt, pw - 80); lines.forEach((ln, i) => text(ln, 40, 190 + i * 48, fnt, INK));
    const yy = 190 + lines.length * 48 + 16; ctx.fillStyle = LINE; ctx.fillRect(40, yy - 16, pw - 80, 2);
    text('You wrote', 40, yy + 26, font(SANS, 22, 500), MUTED); text(FC.ans, 40, yy + 62, font(SANS, 25, 500), INK);
    badge(pw - 64, yy + 44, 25, true, -99, f);
  }
  function flashTickPos() { const lines = (ctx.font = font(SERIF, 36, 600), wrap(FC.back, font(SERIF, 36, 600), FC.w - 80)); return [FC.w - 64, 190 + lines.length * 48 + 16 + 44]; }

  const MA = { w: 820, h: 640 };
  function mathsPanel(f, k) {
    const pw = MA.w;
    item(f, k.in + 6, () => header(pw, 'Percentages', 'Silver · question 3 of 7'));
    item(f, k.in + 9, () => { const q = wrap('A jacket costs £40. A sign says 25% off. How much do you pay?', font(SERIF, 36, 600), pw - 80); q.forEach((ln, i) => text(ln, 40, 150 + i * 48, font(SERIF, 36, 600), INK)); });
    const by = 300, bw = (pw - 80) / 4, bh = 80;
    for (let i = 0; i < 4; i++) { const a = sp(f, k.blocks + i * (k.step || 8), 420, 17); if (a <= 0) continue;
      const off = i === 3 && f >= k.off, op = prog(f, k.off, 8), x = 40 + i * bw;
      ctx.save(); ctx.translate(x + bw / 2, by + bh / 2); ctx.scale(a, a); rr(-bw / 2 + 5, -bh / 2, bw - 10, bh, 12);
      ctx.fillStyle = off ? mix(SOFTBG, RUST_TINT, op) : SOFTBG; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = off ? mix(LINE, RUST, op) : LINE; ctx.stroke();
      text('£10', 0, 10, font(SANS, 28, 600), off ? mix(INK, RUST, op) : INK, 'center'); ctx.restore(); }
    if (f >= k.off) { ctx.font = font(SANS, 21, 700); maskLine('25% off', 40 + 3.5 * bw - ctx.measureText('25% off').width / 2, by - 16, font(SANS, 21, 700), RUST, SOFT(prog(f, k.off, 12)), 30); }
    const ay = 424; item(f, k.blocks + 12, () => { text('Answer', 40, ay + 48, font(SANS, 25, 600), INK);
      const ax = 170, right = f >= k.tick, gp = prog(f, k.tick, 10); rr(ax, ay, 240, 76, 12); ctx.fillStyle = right ? mix('#fdfcfa', GREEN_TINT, gp) : '#fdfcfa'; ctx.fill();
      ctx.lineWidth = 2.5; ctx.strokeStyle = right ? mix(INK, GREEN, gp) : f >= k.typeA ? INK : LINE; ctx.stroke();
      const n = f < k.typeA ? 0 : Math.min(3, Math.floor((f - k.typeA) / (k.rate || 4)) + 1); text('£30'.slice(0, n), ax + 22, ay + 50, font(SANS, 32, 600), INK);
      if (right) badge(ax + 240 - 40, ay + 38, 23, true, k.tick, f); });
    if (f >= k.fb) item(f, k.fb, () => { rr(430, ay, pw - 470, 76, 12); ctx.fillStyle = GREEN_TINT; ctx.fill();
      text('Right.', 452, ay + 32, font(SANS, 21, 700), GREEN); text('25% of £40 is £10, so £40 − £10.', 452, ay + 60, font(SANS, 19, 500), INK); });
    item(f, k.blocks + 14, () => { text('3 in a row to move up', 40, 582, font(SANS, 20, 600), MUTED);
      for (let i = 0; i < 3; i++) { const on = f >= k.streak + i * (k.step || 8), a = sp(f, k.streak + i * (k.step || 8), 450, 14);
        dot(290 + i * 34, 575, 10, '#e6e0d6'); if (on) dot(290 + i * 34, 575, 10 * a, GREEN); } });
  }
  const SB = { w: 820, h: 560, tiles: ['Me', 'gusta', 'jugar', 'al', 'fútbol.'], bank: ['jugar', 'fútbol.', 'Me', 'juega', 'al', 'gusta'] };
  function spanishPanel(f, k) {
    const pw = SB.w; header(pw, 'Spanish · build the sentence', 'Silver · question 2 of 7');
    text('English:', 40, 138, font(SANS, 22, 600), MUTED); text('I like playing football.', 140, 138, font(SERIF, 32, 600), INK);
    const right = f >= k.tick2, gp = prog(f, k.tick2, 10);
    rr(40, 176, pw - 80, 104, 14); ctx.fillStyle = right ? mix(SOFTBG, GREEN_TINT, gp) : SOFTBG; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = right ? mix(LINE, GREEN, gp) : LINE; ctx.setLineDash(right ? [] : [8, 8]); ctx.stroke(); ctx.setLineDash([]);
    ctx.font = font(SANS, 30, 600); const tw = s => ctx.measureText(s).width + 44;
    const bankPos = {}; { let x = 40; const y = 330; SB.bank.forEach(s => { bankPos[s] = [x, y]; x += tw(s) + 14; }); }
    const zonePos = {}; { let x = 60; SB.tiles.forEach(s => { zonePos[s] = [x, 200]; x += tw(s) + 12; }); }
    SB.bank.forEach(s => { const [bx, by] = bankPos[s]; ctx.fillStyle = '#efebe4'; rr(bx, by, tw(s), 60, 12); ctx.fill(); });
    SB.bank.forEach(s => {
      const i = SB.tiles.indexOf(s), t0 = i < 0 ? Infinity : k.tiles + i * (k.step || 8), m = f < t0 ? 0 : SOFT(prog(f, t0, 10));
      const [bx, by] = bankPos[s], [zx, zy] = i < 0 ? [bx, by] : zonePos[s], x = lerp(bx, zx, m), y = lerp(by, zy, m) - Math.sin(m * Math.PI) * 50;
      shadowOn(m > 0 && m < 1 ? 20 : 8, m > 0 && m < 1 ? 10 : 3, 0.12); rr(x, y, tw(s), 60, 12); ctx.fillStyle = i < 0 && f >= k.tick2 ? '#f3f0ea' : CARD; ctx.fill(); shadowOff();
      ctx.lineWidth = 2; ctx.strokeStyle = right && i >= 0 ? GREEN : LINE; ctx.stroke();
      text(s, x + 22, y + 40, font(SANS, 30, 600), i < 0 && f >= k.tick2 ? '#b9b2a8' : INK);
    });
    button(40, 440, 170, 64, 'Check', f, k.check2, INK, 'Checked', k.tick2);
    if (right) { badge(pw - 70, 228, 25, true, k.tick2, f); item(f, k.tick2 + 3, () => text('Right. “Me gusta” + the infinitive.', 236, 482, font(SANS, 22, 600), GREEN)); }
  }

  const EX = { w: 840, h: 700, q: 'Explain why the League of Nations failed to stop Japan in Manchuria.',
    ans: 'Britain and France did not want a war so far away, and without the USA the League had no army and no way to make sanctions hurt Japan, so it could only write a report.' };
  function examPanel(f, k) {
    const pw = EX.w;
    item(f, k.in + 6, () => header(pw, 'History · exam question', '4 marks'));
    item(f, k.in + 9, () => wrap(EX.q, font(SERIF, 32, 600), pw - 80).forEach((ln, i) => text(ln, 40, 142 + i * 44, font(SERIF, 32, 600), INK)));
    item(f, k.in + 12, () => { rr(40, 222, pw - 80, 190, 12); ctx.fillStyle = '#fdfcfa'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = LINE; ctx.stroke();
      const n = f < k.lines ? 0 : Math.floor((f - k.lines) * (k.cps || 3.2)), shown = EX.ans.slice(0, n);
      wrap(shown || ' ', font(SANS, 24, 500), pw - 130).slice(0, 5).forEach((ln, i) => text(ln, 64, 262 + i * 36, font(SANS, 24, 500), INK)); });
    item(f, k.in + 14, () => button(40, 434, 250, 64, 'Mark my answer', f, k.submit, INK, 'Marked', k.mark));
    if (f >= k.marking && f < k.mark) { for (let i = 0; i < 3; i++) { const a = 0.35 + 0.65 * Math.max(0, Math.sin((f - k.marking) / 4 - i * 0.9)); dot(320 + i * 22, 466, 6, `rgba(45,42,38,${a})`); } }
    if (f >= k.mark) {
      const g = sp(f, k.mark, 260, 13), gx = pw - 110, gy = 466;
      ctx.lineWidth = 12; ctx.strokeStyle = LINE; ctx.beginPath(); ctx.arc(gx, gy, 52, 0, 7); ctx.stroke();
      ctx.strokeStyle = GREEN; ctx.lineCap = 'round'; ctx.beginPath(); ctx.arc(gx, gy, 52, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * Math.min(1.04, g)); ctx.stroke();
      const n = Math.min(4, Math.round(4 * clamp(g))); text(`${n}/4`, gx, gy + 12, font(SANS, 34, 800), INK, 'center');
      const rp = prog(f, k.mark, 20); if (rp < 1) { ctx.strokeStyle = `rgba(47,125,79,${0.45 * (1 - rp)})`; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(gx, gy, lerp(60, 170, SOFT(rp)), 0, 7); ctx.stroke(); }
    }
    if (f >= k.fb1) item(f, k.fb1, () => { rr(40, 526, pw - 80, 66, 12); ctx.fillStyle = GREEN_TINT; ctx.fill(); text('What went well', 62, 566, font(SANS, 21, 700), GREEN); text('Two clear reasons, each explained.', 250, 566, font(SANS, 21, 500), INK); });
    if (f >= k.fb2) item(f, k.fb2, () => { rr(40, 604, pw - 80, 66, 12); ctx.fillStyle = SOFTBG; ctx.fill(); text('To push on', 62, 644, font(SANS, 21, 700), INK); text('Back each reason with a date or a fact.', 250, 644, font(SANS, 21, 500), INK); });
  }

  const LE = { w: 860, h: 640 };
  function lessonPanel(f, k) {
    const pw = LE.w;
    item(f, k.in + 6, () => eyebrow('History · Conflict and tension · lesson 7', 44, 64));
    item(f, k.in + 8, () => text('The Manchurian Crisis', 44, 124, font(SERIF, 50, 600), INK));
    item(f, k.in + 10, () => { ctx.fillStyle = LINE; ctx.fillRect(44, 150, pw - 88, 2);
      const body = 'In September 1931 a bomb damaged the South Manchurian Railway near Mukden. Japan blamed Chinese soldiers and used the explosion as an excuse to invade Manchuria. China asked the League of Nations for help.';
      wrap(body, font(SERIF, 27, 500), pw - 88).forEach((ln, i) => text(ln, 44, 204 + i * 42, font(SERIF, 27, 500), INK)); });
    // narration player: slides up at "Hear it"
    if (f >= k.hear) { const a = sp(f, k.hear, 320, 22), y = lerp(pw, 480, a); ctx.save(); ctx.beginPath(); rr(0, 0, pw, LE.h, 18); ctx.clip();
      rr(28, y, pw - 56, 122, 14); ctx.fillStyle = SOFTBG; ctx.fill();
      dot(90, y + 61, 32, INK); ctx.fillStyle = '#fff'; ctx.fillRect(80, y + 47, 7, 28); ctx.fillRect(94, y + 47, 7, 28);
      text('Narration', 144, y + 50, font(SANS, 22, 700), INK); text('Listen while you read', 144, y + 82, font(SANS, 19, 500), MUTED);
      const n = 34, wx = 400, ww = pw - 56 - 400 - 16, playP = clamp((f - k.hear) / (8 * BEAT));
      for (let i = 0; i < n; i++) { const hh = 14 + 36 * Math.abs(Math.sin(i * 1.7) * Math.cos(i * 0.6 + 0.4)) * (0.7 + 0.3 * Math.sin((f - k.hear) / 3 + i));
        ctx.fillStyle = i / n < playP ? RUST : '#d8d1c6'; rr(wx + i * (ww / n), y + 61 - hh / 2, ww / n - 4, hh, 2); ctx.fill(); }
      ctx.restore(); }
  }
  function videoTile(f, k, b) {           // the "Watch it" tile, in screen space, overlapping the lesson card's corner
    if (f < k.watch) return; const a = sp(f, k.watch, 300, 17), vw = 400, vh = 236;
    const cx = b.cx + LE.w * b.s / 2 - vw * b.s / 2 + 26 * u, cy = b.cy - LE.h * b.s / 2 + vh * b.s * (MODE === 'L' ? 0.28 : -0.1);
    ctx.save(); ctx.translate(cx, cy); ctx.scale(b.s * a, b.s * a); ctx.rotate(0.03 * (1 - a) + 0.015);
    shadowOn(50, 20, 0.22); rr(-vw / 2, -vh / 2, vw, vh, 16); const g = ctx.createLinearGradient(-vw / 2, -vh / 2, vw / 2, vh / 2); g.addColorStop(0, '#3a4a5c'); g.addColorStop(1, '#1d2430'); ctx.fillStyle = g; ctx.fill(); shadowOff();
    ctx.save(); rr(-vw / 2, -vh / 2, vw, vh, 16); ctx.clip();
    for (let i = 0; i < 5; i++) { ctx.fillStyle = `rgba(255,255,255,${0.04 + 0.02 * i})`; ctx.fillRect(-vw / 2 + i * 90 - ((f - k.watch) * 0.6 % 90), -vh / 2 + 120 - i * 14, 70, 200); }
    ctx.fillStyle = 'rgba(0,0,0,0.35)'; ctx.fillRect(-vw / 2, vh / 2 - 54, vw, 54); ctx.restore();
    dot(0, -18, 34, 'rgba(255,255,255,0.92)'); ctx.fillStyle = INK; ctx.beginPath(); ctx.moveTo(-9, -34); ctx.lineTo(17, -18); ctx.lineTo(-9, -2); ctx.fill();
    text('Video', -vw / 2 + 20, vh / 2 - 20, font(SANS, 20, 700), '#fff'); text('7:50', vw / 2 - 20, vh / 2 - 20, font(SANS, 18, 500), 'rgba(255,255,255,0.8)', 'right');
    ctx.restore();
  }

  const WG = { w: 820, h: 580 };
  function widgetPanel(f, k) {
    const pw = WG.w, second = f >= k.next, sw = SOFT(prog(f, k.next, 12));
    header(pw, 'Quick check · decimals', second ? 'Question 2' : 'Question 1');
    const q = (opts, pickAt, pickIdx, good, x0, alpha) => { ctx.save(); ctx.globalAlpha *= alpha; ctx.translate(x0, 0);
      text('Which is bigger?', 40, 150, font(SERIF, 42, 600), INK);
      opts.forEach((o, i) => { const x = 40 + i * 380, y = 188, w = 360, h = 150, picked = f >= pickAt && i === pickIdx;
        let sc = 1; if (picked && f < pickAt + 3) sc = 0.95; else if (picked) sc = lerp(0.95, 1, sp(f, pickAt + 3, 500, 20));
        ctx.save(); ctx.translate(x + w / 2, y + h / 2); ctx.scale(sc, sc); rr(-w / 2, -h / 2, w, h, 16);
        const judged = picked && f >= pickAt + (good ? 4 : k.why - pickAt);
        ctx.fillStyle = !picked ? SOFTBG : judged ? (good ? GREEN_TINT : RUST_TINT) : '#efe9df'; ctx.fill(); ctx.lineWidth = picked ? 3 : 2; ctx.strokeStyle = !picked ? LINE : judged ? (good ? GREEN : RUST) : INK; ctx.stroke();
        text(o, 0, 22, font(SANS, 64, 700), INK, 'center'); if (judged) badge(w / 2 - 36, -h / 2 + 34, 20, good, good ? pickAt + 4 : k.why, f); ctx.restore(); });
      ctx.restore(); };
    if (!second || sw < 1) q(['0.25', '0.3'], k.pickWrong, 0, false, -sw * 60, 1 - sw);
    if (second) q(['0.7', '0.65'], k.pickRight, 0, true, (1 - sw) * 60, sw);
    if (f >= k.why && !second) item(f, k.why, () => { rr(40, 364, pw - 80, 150, 14); ctx.fillStyle = RUST_TINT; ctx.fill();
      text('Not quite. Longer isn’t bigger.', 64, 408, font(SANS, 25, 700), RUST);
      text('0.3 is the same as 0.30. Compare the tenths first:', 64, 448, font(SANS, 22, 500), INK); text('3 tenths is more than 2 tenths.', 64, 482, font(SANS, 22, 500), INK); });
    if (second) item(f, k.pickRight + 4, () => { rr(40, 364, pw - 80, 150, 14); ctx.fillStyle = GREEN_TINT; ctx.fill();
      text('Right. 7 tenths is more than 6 tenths.', 64, 420, font(SANS, 25, 700), GREEN);
      text('3 in a row and it’s mastered', 64, 470, font(SANS, 21, 600), MUTED);
      for (let i = 0; i < 3; i++) { dot(400 + i * 34, 463, 10, '#dcd5ca'); const on = i === 0 ? k.pickRight + 4 : k.streak + (i - 1) * 8; if (i < 2 && f >= on) dot(400 + i * 34, 463, 10 * sp(f, on, 450, 14), GREEN); } });
  }

  /* ---------- teacher panels ---------- */
  const TC = { w: 900, h: 660 };
  function tabs(pw, active) {
    text('10M2 · History', 40, 50, font(SANS, 22, 700), INK);
    ['This week', 'Markbook'].forEach((t, i) => { const x = pw - 330 + i * 160; text(t, x, 50, font(SANS, 20, active === i ? 700 : 500), active === i ? INK : MUTED);
      if (active === i) { ctx.font = font(SANS, 20, 700); ctx.fillStyle = RUST; ctx.fillRect(x, 64, ctx.measureText(t).width, 3); } });
    ctx.fillStyle = LINE; ctx.fillRect(0, 78, pw, 2);
  }
  function classesPanel(f, k) {
    const pw = TC.w; item(f, k.in + 6, () => tabs(pw, 0));
    item(f, k.brief, () => { eyebrow('This week', 40, 126);
      text('Go over the Lytton Report again.', 40, 172, font(SANS, 27, 700), INK);
      text('14 of the 22 who answered chose “Japan acted in self-defence”.', 40, 210, font(SANS, 22, 500), INK); });
    item(f, k.brief + 12, () => { text('Weimar Germany is being forgotten.', 40, 258, font(SANS, 22, 600), RUST); ctx.font = font(SANS, 22, 600);
      text('6 pupils need to revise it again.', 40 + ctx.measureText('Weimar Germany is being forgotten. ').width, 258, font(SANS, 22, 500), INK); });
    const figs = [[71, '%', 'of quiz answers right'], [2, '', 'topics being forgotten'], [22, ' of 26', 'have done a quiz']];
    figs.forEach(([n, suf, lab], i) => item(f, k.figs + i * 4, () => { const x = 40 + i * 280, y = 290; rr(x, y, 260, 120, 14); ctx.fillStyle = SOFTBG; ctx.fill();
      const c = Math.round(n * SOFT(prog(f, k.figs + i * 4, 24))); text(c + suf, x + 22, y + 62, font(SANS, 44, 800), INK); text(lab, x + 22, y + 98, font(SANS, 19, 500), MUTED); }));
    const panels = [['Go over these again', ['The Lytton Report', 'Article 231']], ['Being forgotten', ['Weimar Germany · 6 pupils']], ['Pupils to talk to', ['Jamal R.', 'Ellie T.']]];
    panels.forEach(([h, rows], i) => item(f, [k.p1, k.p2, k.p3][i], () => { const x = 40 + i * 280, y = 432; rr(x, y, 260, 190, 14); ctx.lineWidth = 2; ctx.strokeStyle = LINE; ctx.stroke();
      text(h, x + 20, y + 40, font(SANS, 19, 700), INK); rows.forEach((r, j) => text(r, x + 20, y + 84 + j * 36, font(SANS, 19, 500), INK)); }));
  }
  const MB = { w: 900, h: 620, topics: ['Conflict', 'Germany', 'Health', 'Elizabeth', 'Cold War'],
    pupils: ['Amira K.', 'Ben O.', 'Chloe W.', 'Dev S.', 'Ellie T.', 'Finn H.', 'Jamal R.', 'Maya L.'] };
  function markbookPanel(f, k) {
    const pw = MB.w; tabs(pw, 1);
    const x0 = 190, y0 = 128, cw = (pw - x0 - 30) / 5, ch = 50;
    MB.topics.forEach((t, j) => text(t, x0 + j * cw + cw / 2, y0, font(SANS, 18, 600), MUTED, 'center'));
    MB.pupils.forEach((p, i) => { text(p, 40, y0 + 46 + i * ch, font(SANS, 20, 600), INK);
      MB.topics.forEach((t, j) => { const v = (i * 7 + j * 11 + (i * j) % 5) % 10, band = v < 5 ? 0 : v < 8 ? 1 : 2, at = k.cells + (i + j) * 2.4;
        const a = sp(f, at, 420, 17); if (a <= 0) return; const cx = x0 + j * cw + cw / 2, cy = y0 + 38 + i * ch;
        ctx.save(); ctx.translate(cx, cy); ctx.scale(a, a); rr(-cw / 2 + 6, -ch / 2 + 5, cw - 12, ch - 10, 10); ctx.fillStyle = [GREEN_TINT, AMBER_TINT, RUST_TINT][band]; ctx.fill();
        text(['secure', 'developing', 'emerging'][band], 0, 7, font(SANS, 16, 600), [GREEN, '#9a6b1c', RUST][band], 'center'); ctx.restore(); }); });
    item(f, k.legend, () => { const y = y0 + 38 + 8 * ch + 16; [['knows it well', GREEN_TINT, GREEN], ['getting there', AMBER_TINT, '#9a6b1c'], ['needs work', RUST_TINT, RUST]].forEach(([l, bg, c], i) => {
      const x = 190 + i * 230; rr(x, y - 22, 26, 26, 6); ctx.fillStyle = bg; ctx.fill(); text(l, x + 38, y - 2, font(SANS, 19, 600), c); }); });
  }
  const WR = { w: 900, h: 600, rows: [['What did the Lytton Report find?', 'Japan acted in self-defence', 14], ['What was Article 231?', 'Reparations', 9],
    ['What did sanctions on Italy leave out?', 'Weapons', 8], ['Why did the USA not join the League?', 'It was not invited', 6]] };
  function wrongPanel(f, k) {
    const pw = WR.w; item(f, k.in + 6, () => header(pw, 'Questions the class gets wrong', '10M2 · History'));
    item(f, k.in + 8, () => { text('Question', 40, 124, font(SANS, 17, 700), MUTED); text('Most chose', 470, 124, font(SANS, 17, 700), MUTED); text('Pupils', pw - 40, 124, font(SANS, 17, 700), MUTED, 'right'); });
    WR.rows.forEach(([q, a, n], i) => { const at = k.rows + i * BEAT; if (f < at) return; const y = 144 + i * 86, lit = i === 0 && f >= k.light, lp = prog(f, k.light, 10);
      item(f, at, () => { if (lit) { const s = 1 + 0.02 * Math.sin(Math.PI * clamp((f - k.light) / 12)); ctx.save(); ctx.translate(pw / 2, y + 38); ctx.scale(s, s); ctx.translate(-pw / 2, -(y + 38)); rr(24, y + 2, pw - 48, 72, 12); ctx.fillStyle = mix(CARD, RUST_TINT, lp); ctx.fill(); }
        text(q, 40, y + 46, font(SANS, 21, 600), INK); text('“' + a + '”', 470, y + 46, font(SANS, 21, 600), lit ? RUST : INK); text(String(n), pw - 40, y + 46, font(SANS, 24, 800), INK, 'right');
        if (lit) ctx.restore(); if (i < 3) { ctx.fillStyle = LINE; ctx.fillRect(40, y + 80, pw - 80, 1.5); } }); });
    item(f, k.light + 8, () => button(40, pw === 900 ? 506 : 506, 330, 64, '▶  Show these on the board', f, k.board, INK));
  }
  const SU = { w: 880, h: 660 };
  function summaryPanel(f, k) {
    const pw = SU.w;
    item(f, k.in + 6, () => { dot(62, 56, 24, RUST); text('S', 62, 64, font(MARK, 24, 400), '#fff', 'center');
      text('StudyVault', 100, 48, font(SANS, 21, 700), INK); text('to Ms Patel · Monday morning', 100, 76, font(SANS, 18, 500), MUTED);
      ctx.fillStyle = LINE; ctx.fillRect(0, 104, pw, 2); text('10M2 History: this week’s summary', 40, 156, font(SERIF, 34, 600), INK); });
    const sec = (at, y, h, lines) => item(f, at, () => { text(h, 40, y, font(SANS, 21, 700), INK); lines.forEach((l, i) => text(l, 40, y + 36 + i * 32, font(SANS, 21, 500), INK)); });
    sec(k.h1, 222, 'What keeps coming up', ['Many pupils mix up Article 231 (war guilt)', 'with reparations.']);
    sec(k.h2, 348, 'One thing to show them next lesson', ['Articles 231 and 232 side by side.']);
    sec(k.h3, 442, 'Pupils to talk to', ['Jamal R. has got the last five Germany questions wrong.']);
    item(f, k.h3 + 8, () => { ctx.fillStyle = LINE; ctx.fillRect(40, 540, pw - 80, 1.5); text('Written by AI from 23 marked answers. Check it before you act on it.', 40, 584, font(SANS, 18, 500), MUTED); });
  }
  const PK = { w: 640, h: 820 };
  function packPanel(f, k) {
    const pw = PK.w;
    item(f, k.in + 6, () => { eyebrow('Parents’ evening · History', 44, 64); text('Amira K.', 44, 124, font(SERIF, 50, 600), INK); text('Year 10 · lessons finished: 34', 44, 164, font(SANS, 20, 500), MUTED); ctx.fillStyle = LINE; ctx.fillRect(44, 190, pw - 88, 2); });
    item(f, k.in + 10, () => text('Topics, against the class average', 44, 236, font(SANS, 19, 700), INK));
    [['Conflict and tension', 0.82, 0.64], ['Germany 1890–1945', 0.46, 0.58], ['Health and the people', 0.71, 0.6], ['Elizabethan England', 0.63, 0.55]].forEach(([t, v, avg], i) => {
      const y = 272 + i * 70; item(f, k.in + 12, () => text(t, 44, y, font(SANS, 18, 500), INK));
      const bw = pw - 88, g = SOFT(prog(f, k.bars + i * 8, 20)); rr(44, y + 14, bw, 20, 6); ctx.fillStyle = SOFTBG; ctx.fill();
      if (g > 0) { rr(44, y + 14, bw * v * g, 20, 6); ctx.fillStyle = v >= avg ? GREEN : AMBER; ctx.fill(); ctx.fillStyle = INK; ctx.fillRect(44 + bw * avg - 1.5, y + 8, 3, 32); } });
    item(f, k.wrongs, () => { text('Wrong answers that keep coming back', 44, 574, font(SANS, 19, 700), INK); text('Said Article 231 was about reparations (twice)', 44, 608, font(SANS, 18, 500), RUST); });
    item(f, k.para, () => { text('From the teacher', 44, 668, font(SANS, 19, 700), INK);
      const n = Math.floor((f - k.para) * 3.4), s = 'Amira is strongest on Conflict and tension. Before the mock, she should revise Weimar Germany.'.slice(0, Math.max(0, n));
      wrap(s || ' ', font(SERIF, 21, 500), pw - 88).forEach((ln, i) => text(ln, 44, 704 + i * 30, font(SERIF, 21, 500), INK));
      text('Written by AI · check before printing', 44, 790, font(SANS, 15, 500), MUTED); });
  }
  const SA = { w: 820, h: 560 };
  function safePanel(f, k) {
    const pw = SA.w;
    item(f, k.in + 6, () => { dot(62, 56, 24, TL.C.navy); ctx.strokeStyle = '#fff'; ctx.lineWidth = 3.5; ctx.beginPath(); ctx.moveTo(62, 42); ctx.lineTo(62, 60); ctx.stroke(); dot(62, 69, 2.6, '#fff');
      text('Safeguarding · StudyVault', 100, 48, font(SANS, 21, 700), INK); text('to the safeguarding lead', 100, 76, font(SANS, 18, 500), MUTED); ctx.fillStyle = LINE; ctx.fillRect(0, 104, pw, 2); });
    item(f, k.body, () => { text('A concern needs your review', 40, 162, font(SERIF, 36, 600), INK);
      ['An answer written by a pupil in 10M2 was flagged by', 'the safeguarding check. Open StudyVault to review it.'].forEach((l, i) => text(l, 40, 214 + i * 34, font(SANS, 22, 500), INK)); });
    item(f, k.note, () => { rr(40, 296, pw - 80, 80, 12); ctx.fillStyle = SOFTBG; ctx.fill(); text('This email has no names and no words from the pupil.', 64, 344, font(SANS, 21, 600), INK); });
    item(f, k.note + 8, () => button(40, 408, 300, 66, 'Review the concern', f, k.review, TL.C.navy));
  }
  const PV = { w: 820, h: 560 };
  function privatePanel(f, k) {
    const pw = PV.w;
    item(f, k.in + 6, () => header(pw, 'Demo High School · your own topics', null));
    ['Medicine through time: our fieldwork', 'The Norman conquest: local sites', 'Year 10 mock: the questions we set', 'Source packs from our archive'].forEach((r, i) => item(f, k.rows + i * 8, () => {
      const y = 116 + i * 78; rr(40, y, pw - 80, 62, 12); ctx.fillStyle = SOFTBG; ctx.fill(); text(r, 64, y + 40, font(SANS, 22, 600), INK); }));
    item(f, k.close + 6, () => text('Only your pupils and staff can see it.', 40, 470 + 40, font(SANS, 22, 600), GREEN));
  }

  /* ===================== scenes ===================== */
  const kf = (S, name) => S.keys[name] * BEAT;
  function sceneKeys(S) { const o = {}; for (const n in S.keys) o[n] = kf(S, n); return o; }
  const OPEN_C = () => [W / 2, H / 2];

  const SCENES = {
    open(t, S) {
      const k = sceneKeys(S), [cx, cy] = OPEN_C(), r0 = 15 * u; ground(INK, true);
      const dotS = sp(t, k.dot, 420, 17), grow = sp(t, k.lock, 300, 19);
      const lift = 150 * sp(t, k.unlock, 380, 16), swing = sp(t, k.swing, 170, 11);
      const out = IN_CUBIC(prog(t, k.collapse, 8));
      if (t < k.collapse + 8) {
        const lh = lerp(r0 * 2.2, 230 * u, grow) * (1 - out);
        const gl = ctx.createRadialGradient(cx, cy, 0, cx, cy, 460 * u); gl.addColorStop(0, `rgba(192,99,37,${0.2 * grow * (1 - out)})`); gl.addColorStop(1, 'rgba(192,99,37,0)'); ctx.fillStyle = gl; ctx.fillRect(0, 0, W, H);
        const rp = prog(t, k.unlock, 22); if (rp > 0 && rp < 1) { ctx.strokeStyle = `rgba(192,99,37,${0.55 * (1 - rp)})`; ctx.lineWidth = 3 * u; ctx.beginPath(); ctx.arc(cx, cy, lerp(130, 560, SOFT(rp)) * u, 0, 7); ctx.stroke(); }
        if (grow < 0.25) dot(cx, cy, r0 * dotS * (1 - grow * 4));
        if (grow > 0) lock(cx - (swing * 60 * u * (1 - out)), cy, lh, lift * (1 - out), clamp(swing), RUST, INK);
        if (out > 0.7) dot(cx, cy, r0 * (out - 0.7) / 0.3);
      } else {
        const s = INOUT_EXPO(prog(t, k.collapse + 8, S.bars * 64 - k.collapse - 8)), hw = lerp(r0, W * 0.56, s), th = lerp(r0 * 2, 5 * u, s);
        rr(cx - hw, cy - th / 2, hw * 2, th, th / 2); ctx.fillStyle = mix(RUST, PAPER, s); ctx.fill();
      }
    },
    head(t, S) {
      const k = sceneKeys(S); ground();
      const words = ['Every', 'major', 'GCSE', 'subject'], at = [k.w0, k.w1, k.w2, k.w3];
      const size = (MODE === 'L' ? 132 : MODE === 'S' ? 112 : 128) * u, fnt = font(SERIF, size, 600), lh = size * 1.14, gap = size * 0.26, dr = size * 0.085;
      ctx.letterSpacing = `${-0.02 * size}px`; ctx.font = fnt; const ws = words.map(w => ctx.measureText(w).width);
      const rows = MODE === 'L' ? [[0, 1, 2, 3]] : [[0, 1], [2, 3]], pos = [];
      const y0 = H / 2 + size * 0.3 - (rows.length - 1) * lh / 2 - 30 * u;
      rows.forEach((r, ri) => { const tot = r.reduce((a, i) => a + ws[i], 0) + gap * (r.length - 1) + (ri === rows.length - 1 ? dr * 3 : 0); let x = W / 2 - tot / 2;
        r.forEach(i => { pos[i] = [x, y0 + ri * lh]; x += ws[i] + gap; }); });
      words.forEach((w, i) => maskLine(w, pos[i][0], pos[i][1], fnt, INK, SOFT(prog(t, at[i], 18)), lh));
      ctx.letterSpacing = '0px';
      const dx = pos[3][0] + ws[3] + dr * 1.6, dy = pos[3][1] - dr; dot(dx, dy, dr * sp(t, k.stop, 420, 15));
      S.exit = [dx, dy];
      const boards = ['AQA', 'Edexcel', 'OCR', 'Eduqas'], bf = font(SANS, (MODE === 'L' ? 40 : 38) * u, 600); ctx.font = bf;
      const bg = 56 * u, bw = boards.map(b => ctx.measureText(b).width), tot = bw.reduce((a, b) => a + b, 0) + bg * 3; let x = W / 2 - tot / 2; const by = pos[3][1] + (MODE === 'L' ? 120 : 130) * u;
      boards.forEach((b, i) => { maskLine(b, x, by, bf, mix(MUTED, INK, 0.3), SOFT(prog(t, k.boards + i * 4, 16)), 54 * u);
        if (i < 3 && t >= k.boards + i * 4 + 6) dot(x + bw[i] + bg / 2, by - 13 * u, 4 * u * sp(t, k.boards + i * 4 + 6, 400, 15), '#cfc7bb'); x += bw[i] + bg; });
      if (t < 12) { const s = SNAP(prog(t, 0, 11)), hh = lerp(5 * u, H * 1.02, s); ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, H / 2 - hh / 2); ctx.rect(0, H / 2 + hh / 2, W, H); ctx.fillStyle = INK; ctx.fill(); ctx.restore(); }
    },
    lesson(t, S) {
      const k = sceneKeys(S); ground(); k.in = 4;
      title([{ t: 'Read it.', at: k.read }, { t: 'Hear it.', at: k.hear, col: RUST }, { t: 'Watch it.', at: k.watch }], t);
      const b = card(LE.w, LE.h, t, k.in, () => lessonPanel(t, k)); videoTile(t, k, b); S.exit = [b.cx, b.cy];
    },
    flash(t, S) {
      const k = sceneKeys(S); k.in = 4; k.type = k.typeFrom; ground();
      const draw = () => {
        title([{ t: 'Type what you remember.', at: k.in + 4 }, { t: 'Checked instantly.', at: k.tick + 2, col: GREEN }], t);
        const flipP = INOUT_CUBIC(prog(t, k.flip, 14)), th = flipP * Math.PI, face = th < Math.PI / 2 ? 'front' : 'back', sx = Math.max(0.002, Math.abs(Math.cos(th)));
        const b = panelBox(FC.w, FC.h + 60), s = sp(t, k.in, 300, 21); if (s <= 0) return b;
        ctx.save(); ctx.translate(b.cx, b.cy); ctx.scale(b.s * lerp(0.05, 1, s) * sx * (1 + Math.sin(th) * 0.04), b.s * lerp(0.05, 1, s) * (1 + Math.sin(th) * 0.04));
        shadowOn(lerp(8, 60, s), lerp(4, 22, s), 0.13); rr(-FC.w / 2, -FC.h / 2, FC.w, FC.h, 18); ctx.fillStyle = mix(RUST, CARD, clamp((t - k.in) / 6)); ctx.fill(); shadowOff();
        if (t - k.in >= 6) { ctx.save(); ctx.translate(-FC.w / 2, -FC.h / 2); face === 'front' ? flashFront(t, k) : flashBack(t); ctx.restore(); }
        if (flipP > 0 && flipP < 1) { ctx.fillStyle = `rgba(45,42,38,${0.18 * Math.sin(th)})`; rr(-FC.w / 2, -FC.h / 2, FC.w, FC.h, 18); ctx.fill(); }
        ctx.restore(); return b;
      };
      if (t < k.zoom) { draw(); return; }
      const b = panelBox(FC.w, FC.h + 60), [px, py] = flashTickPos(), tx = b.cx + (px - FC.w / 2) * b.s, ty = b.cy + (py - FC.h / 2) * b.s;
      const e = IN_EXPO(prog(t, k.zoom, S.bars * 64 - k.zoom)), z = Math.exp(Math.log(80) * e), m = SOFT(prog(t, k.zoom, 12));
      ctx.save(); ctx.translate(lerp(tx, W / 2, m), lerp(ty, H / 2, m)); ctx.scale(z, z); ctx.translate(-tx, -ty); draw(); ctx.restore();
      const cover = clamp((z - 28) / 30); if (cover > 0) { ctx.globalAlpha = cover; ctx.fillStyle = GREEN; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1; }
    },
    practice(t, S) {
      const k = sceneKeys(S); k.in = 4; ground();
      title([{ t: 'Practice that marks as you go.', at: k.in + 4 }], t);
      const sw = SOFT(prog(t, k.swap, 14)), off = (MODE === 'L' ? 1300 : 1000) * u;
      if (sw < 1) card(MA.w, MA.h, t, k.in, () => mathsPanel(t, k), { dx: -sw * off, rot: -sw * 0.05 });
      if (t >= k.swap) card(SB.w, SB.h, t, k.swap, () => spanishPanel(t, k), { dx: (1 - sw) * off * 0.4, always: true, rot: (1 - sw) * 0.05 });
      const b = panelBox(SB.w, SB.h); S.exit = t >= k.swap ? [b.cx + (SB.w / 2 - 70) * b.s, b.cy + (228 - SB.h / 2) * b.s] : [b.cx, b.cy];
    },
    exam(t, S) {
      const k = sceneKeys(S); k.in = 4; ground();
      title([{ t: 'Exam answers, marked.', at: k.in + 4 }, { t: 'Feedback in seconds.', at: k.mark + 4, col: GREEN }], t);
      const b = card(EX.w, EX.h, t, k.in, () => examPanel(t, k)); S.exit = [b.cx + (EX.w / 2 - 110) * b.s, b.cy + (466 - EX.h / 2) * b.s];
    },
    widget(t, S) {
      const k = sceneKeys(S); k.in = 4; ground();
      title([{ t: 'Learn from your mistakes.', at: k.in + 4 }], t);
      const b = card(WG.w, WG.h, t, k.in, () => widgetPanel(t, k)); S.exit = [b.cx, b.cy];
    },
    free(t, S) {
      const k = sceneKeys(S); ground(RUST, true);
      const size = (MODE === 'L' ? 190 : 170) * u, fnt = font(SERIF, size, 600), lh = size * 1.1;
      ctx.letterSpacing = `${-0.02 * size}px`;
      if (MODE === 'L') { ctx.font = fnt; const a = ctx.measureText('Free.').width, b2 = ctx.measureText('No ads.').width, g = 70 * u, x = W / 2 - (a + g + b2) / 2, y = H / 2 + size * 0.32;
        maskLine('Free.', x, y, fnt, '#fff', SOFT(prog(t, k.free, 18)), lh); maskLine('No ads.', x + a + g, y, fnt, '#fff', SOFT(prog(t, k.ads, 18)), lh); }
      else { maskLine('Free.', W / 2, H / 2 - lh * 0.2, fnt, '#fff', SOFT(prog(t, k.free, 18)), lh, 'center'); maskLine('No ads.', W / 2, H / 2 + lh * 0.9, fnt, '#fff', SOFT(prog(t, k.ads, 18)), lh, 'center'); }
      ctx.letterSpacing = '0px'; S.exit = [W / 2, H / 2];
    },
    end(t, S) {
      const k = sceneKeys(S); ground();
      const size = (MODE === 'L' ? 210 : MODE === 'S' ? 158 : 168) * u; ctx.font = font(MARK, size, 400);
      const word = 'StudyVault', ww = ctx.measureText(word).width, lh = size * 0.34, lw = lh * 1023 / 1280, gap = size * 0.06, total = ww + gap + lw;
      const x0 = W / 2 - total / 2, base = H / 2 + size * 0.12 - (MODE === 'L' ? 20 : 60) * u;
      let x = x0; for (let i = 0; i < word.length; i++) { const ch = word[i], cw = ctx.measureText(word.slice(0, i + 1)).width - ctx.measureText(word.slice(0, i)).width;
        maskLine(ch, x, base, font(MARK, size, 400), INK, SOFT(prog(t, k.letters + i * 1.5, 16)), size * 1.2); x += cw; }
      const lx = x0 + ww + gap + lw / 2, ly = base - lh / 2;
      const fly = SOFT(prog(t, k.hit, k.lock - k.hit)), cx = lerp(W / 2, lx, fly), cy = lerp(H / 2, ly, fly);
      if (t < k.lock) { const pulse = t < k.hit ? 1 + 0.12 * Math.sin(t / 3) : 1; dot(cx, cy, 15 * u * pulse * lerp(1, 0.7, fly)); }
      else { const g = sp(t, k.lock, 380, 19), cl = sp(t, k.close, 420, 17);
        const swing = 1 - clamp(cl * 1.4), lift = 150 * (t < k.close ? 1 : 1 - clamp(sp(t, k.close + 5, 520, 20)));
        lock(lx, ly, lh * lerp(0.4, 1, g), lift, clamp(swing), RUST, PAPER); }
      const tf = font(SANS, (MODE === 'L' ? 38 : 34) * u, 500), uf = font(SANS, (MODE === 'L' ? 44 : 40) * u, 700);
      const tagLines = MODE === 'L' ? [S.tag] : wrap(S.tag, tf, W - 140 * u);
      tagLines.forEach((l, i) => maskLine(l, W / 2, base + (MODE === 'L' ? 130 : 150) * u + i * 50 * u, tf, MUTED, SOFT(prog(t, k.tag + i * 4, 18)), 50 * u, 'center'));
      maskLine('www.studyvault.co.uk', W / 2, base + (MODE === 'L' ? 230 : 190 + tagLines.length * 50) * u, uf, INK, SOFT(prog(t, k.url, 18)), 60 * u, 'center');
      if (t < 14) { const s = INOUT_EXPO(prog(t, 0, 12)), R = Math.hypot(W, H) / 2 + 10; ctx.fillStyle = S.enter.color; ctx.beginPath(); ctx.arc(W / 2, H / 2, lerp(R, 15 * u, s), 0, 7); ctx.fill(); }
    },
    /* ---- teachers ---- */
    montage(t, S) {
      const k = sceneKeys(S); ground();
      title([{ t: 'What your pupils get.', at: 8 }], t);
      const slot = t < k.f2 ? 0 : t < k.f3 ? 1 : 2, off = (MODE === 'L' ? 1300 : 1000) * u;
      const out = (at) => SOFT(prog(t, at, 12)), cardsAt = [k.f1, k.f2, k.f3];
      const fk = { in: k.f1, type: k.f1 + 6, rate: 0.6, check: k.f1tick - 8, tick: k.f1tick };
      const mk = { in: k.f2, blocks: k.f2 + 6, step: 4, off: k.f2 + 22, typeA: k.f2 + 26, rate: 3, tick: k.f2tick, fb: k.f2tick + 4, streak: k.f2tick + 6 };
      const ek = { in: k.f3, lines: k.f3 + 6, cps: 7, submit: k.f3 + 28, marking: k.f3 + 31, mark: k.f3mark, fb1: k.f3mark + 10, fb2: k.f3mark + 18 };
      if (slot === 0 || t < k.f2 + 12) card(FC.w, FC.h + 60, t, k.f1, () => flashFront(t, fk), { dx: -out(k.f2) * off });
      if (t >= k.f2 && (slot === 1 || t < k.f3 + 12)) card(MA.w, MA.h, t, k.f2, () => mathsPanel(t, mk), { dx: (1 - out(k.f2)) * off * 0.4 - out(k.f3) * off, always: true });
      if (t >= k.f3) card(EX.w, EX.h, t, k.f3, () => examPanel(t, ek), { dx: (1 - out(k.f3)) * off * 0.4, always: true });
      const b = panelBox(EX.w, EX.h); S.exit = [b.cx, b.cy]; void cardsAt;
    },
    classes(t, S) { const k = sceneKeys(S); k.in = 4; ground(); title([{ t: 'Your class, at a glance.', at: 8 }], t); const b = card(TC.w, TC.h, t, k.in, () => classesPanel(t, k)); S.exit = [b.cx, b.cy]; },
    markbook(t, S) { const k = sceneKeys(S); k.in = 4; ground(); title([{ t: 'A markbook that fills itself.', at: 8 }], t); const b = card(MB.w, MB.h, t, k.in, () => markbookPanel(t, k)); S.exit = [b.cx, b.cy]; },
    wrong(t, S) { const k = sceneKeys(S); k.in = 4; ground(); title([{ t: 'See what the class gets wrong.', at: 8 }], t); const b = card(WR.w, WR.h, t, k.in, () => wrongPanel(t, k)); S.exit = [b.cx, b.cy - (WR.h / 2 - 182) * b.s]; },
    summary(t, S) { const k = sceneKeys(S); k.in = 4; ground(); title([{ t: 'This week’s summary, every Monday.', at: 8 }], t); const b = card(SU.w, SU.h, t, k.in, () => summaryPanel(t, k)); S.exit = [b.cx, b.cy]; },
    pack(t, S) { const k = sceneKeys(S); k.in = 4; ground(); title([{ t: 'Parents’ evening, ready to print.', at: 8 }], t); const b = card(PK.w, PK.h, t, k.in, () => packPanel(t, k), { rot: -0.012 }); S.exit = [b.cx, b.cy]; },
    safe(t, S) { const k = sceneKeys(S); k.in = 4; ground(); title([{ t: 'Concerns go straight to your safeguarding lead.', at: 8 }], t); const b = card(SA.w, SA.h, t, k.in, () => safePanel(t, k)); S.exit = [b.cx, b.cy]; },
    private(t, S) {
      const k = sceneKeys(S); k.in = 4; ground(); title([{ t: 'Your school’s own content stays private.', at: 8 }], t);
      const b = card(PV.w, PV.h, t, k.in, () => privatePanel(t, k));
      if (t >= k.lock) { const lx = b.cx + (PV.w / 2 - 70) * b.s, ly = b.cy - (PV.h / 2 - 20) * b.s, g = sp(t, k.lock, 300, 17), drop = lerp(-120 * u, 0, SOFT(prog(t, k.lock, 12)));
        const cl = sp(t, k.close, 420, 17), swing = 1 - clamp(cl * 1.4), lift = 150 * (t < k.close ? 1 : 1 - clamp(sp(t, k.close + 5, 520, 20)));
        shadowOn(30, 12, 0.18); lock(lx, ly + drop, 120 * u * b.s * g, lift, clamp(swing), RUST, CARD); shadowOff(); S.exit = [lx, ly]; }
      else S.exit = [b.cx, b.cy];
    },
  };

  /* ===================== transitions ===================== */
  const TIN = 8, TOUT = 12;
  function growOver(p, tr, from) {                 // the colour field covering the outgoing scene
    if (p <= 0) return; const col = tr.color || RUST;
    if (tr.type === 'bars') { const n = 6, bw = W / n; for (let i = 0; i < n; i++) { const q = SNAP(clamp(p * 1.6 - i * 0.12)); ctx.fillStyle = col; ctx.fillRect(i * bw - 1, H * (1 - q), bw + 2, H * q + 1); } return; }
    const [x, y] = from || [W / 2, H / 2], R = Math.hypot(Math.max(x, W - x), Math.max(y, H - y)) + 4;
    ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, R * IN_CUBIC(p) + 12 * u, 0, 7); ctx.fill();
  }
  function revealOver(p, tr, to) {                 // the field leaving, to show the incoming scene
    if (p >= 1) return; const col = tr.color || RUST;
    if (tr.type === 'bars') { const n = 6, bw = W / n; for (let i = 0; i < n; i++) { const q = SNAP(clamp(p * 1.6 - i * 0.12)); ctx.fillStyle = col; ctx.fillRect(i * bw - 1, 0, bw + 2, H * (1 - q) + 1); } return; }
    const [x, y] = to || [W / 2, H / 2], R = Math.hypot(Math.max(x, W - x), Math.max(y, H - y)) + 4;
    ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, lerp(R, 12 * u, INOUT_EXPO(p)), 0, 7); ctx.fill();
  }
  function anchorOf(S) { const pb = { lesson: [LE.w, LE.h], flash: [FC.w, FC.h + 60], practice: [MA.w, MA.h], exam: [EX.w, EX.h], widget: [WG.w, WG.h], montage: [FC.w, FC.h + 60],
    classes: [TC.w, TC.h], markbook: [MB.w, MB.h], wrong: [WR.w, WR.h], summary: [SU.w, SU.h], pack: [PK.w, PK.h], safe: [SA.w, SA.h], private: [PV.w, PV.h] }[S.id];
    if (!pb) return [W / 2, H / 2]; const b = panelBox(pb[0], pb[1]); return [b.cx, b.cy]; }

  function frame(f) {
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left'; ctx.letterSpacing = '0px';
    const i = V.scenes.findIndex(s => f >= s.f0 && f < s.f1), S = V.scenes[Math.max(0, i)], t = f - S.f0, next = V.scenes[i + 1];
    SCENES[S.id](t, S);
    if (next && next.enter && ['circle', 'bars', 'field'].includes(next.enter.type) && t >= S.bars * 64 - TIN) growOver((t - (S.bars * 64 - TIN) + 1) / TIN, next.enter, S.exit);
    if (S.enter && ['circle', 'bars', 'zoom'].includes(S.enter.type) && S.id !== 'end' && t < TOUT) revealOver(t / TOUT, S.enter.type === 'zoom' ? { type: 'circle', color: S.enter.color } : S.enter, anchorOf(S));
    if (DEBUG) { const bar = Math.floor(f / 64), beat = Math.floor(f % 64 / 16); ctx.fillStyle = 'rgba(0,0,0,0.6)'; ctx.fillRect(0, 0, 360, 56); ctx.fillStyle = f % 16 === 0 ? '#ff4d4d' : '#fff'; ctx.font = '600 26px monospace'; ctx.fillText(`f${f} ${bar}.${beat} ${S.id}`, 14, 38); }
  }

  window.renderFrame = frame;
  window.FRAMES = V.frames;
  Promise.all([font(SERIF, 40, 600), font(SERIF, 40, 500), font(SANS, 40, 800), font(SANS, 40, 700), font(SANS, 40, 600), font(SANS, 40, 500), font(MARK, 40, 400)].map(x => document.fonts.load(x)))
    .then(() => document.fonts.ready).then(() => { frame(0); window.READY = true; });
})();
