/* StudyVault launch video v2 — the picture. Every frame is a pure function of the frame number
   (window.renderFrame(f)), drawn on one canvas, so a render is frame-exact and repeatable.

   House rules (Tom): one idea per scene; interface rebuilt as animatable parts in the site's own
   look, never cropped screenshots; transitions are objects doing something (the rust padlock dot,
   masks, a zoom-through), never a plain cut; text holds long enough to read; no pill shapes, no
   coloured left-border stripes, no hint captions.

   URL: comp.html?ar=16x9|9x16|1x1 [&debug=1] [&still=practice|end] */
(function () {
  const Q = new URLSearchParams(location.search);
  const AR = Q.get('ar') || '16x9', DEBUG = Q.get('debug') === '1', STILL = Q.get('still');
  const [W, H] = { '16x9': [1920, 1080], '9x16': [1080, 1920], '1x1': [1080, 1080] }[AR];
  const P = H > W;                                   // portrait: its own layout, not a crop
  const u = P ? W / 1080 : H / 1080;
  const cv = document.getElementById('c'); cv.width = W; cv.height = H;
  const ctx = cv.getContext('2d');
  const { FPS, F, K } = window.TL;

  const PAPER = '#faf8f5', INK = '#2d2a26', RUST = '#c06325', GREEN = '#2f7d4f', MUTED = '#8a8580',
    LINE = '#e6e0d6', CARD = '#ffffff', GREEN_TINT = '#eef6f0';
  const SERIF = '"Source Serif 4", Georgia, serif', SANS = 'Inter, "Segoe UI", sans-serif', MARK = '"Young Serif", Georgia, serif';

  /* ---------- easing ---------- */
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const prog = (f, s, d) => clamp((f - s) / d);
  function bezier(x1, y1, x2, y2) {                  // CSS cubic-bezier, solved by Newton then bisection
    const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx, cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
    const sx = t => ((ax * t + bx) * t + cx) * t, sy = t => ((ay * t + by) * t + cy) * t, dx = t => (3 * ax * t + 2 * bx) * t + cx;
    return x => { if (x <= 0) return 0; if (x >= 1) return 1; let t = x;
      for (let i = 0; i < 8; i++) { const e = sx(t) - x; if (Math.abs(e) < 1e-6) return sy(t); const d = dx(t); if (Math.abs(d) < 1e-6) break; t -= e / d; }
      let lo = 0, hi = 1; t = x; for (let i = 0; i < 30; i++) { const v = sx(t); if (Math.abs(v - x) < 1e-6) break; if (v < x) lo = t; else hi = t; t = (lo + hi) / 2; } return sy(t); };
  }
  const SOFT = bezier(0.16, 1, 0.3, 1);              // the site's soft-close
  const SNAP = bezier(0.8, 0, 0, 1);                 // wipes: fast, then a hard stop
  const IN_EXPO = t => t <= 0 ? 0 : t >= 1 ? 1 : Math.pow(2, 10 * t - 10);
  const INOUT_EXPO = t => t <= 0 ? 0 : t >= 1 ? 1 : t < 0.5 ? Math.pow(2, 20 * t - 10) / 2 : (2 - Math.pow(2, -20 * t + 10)) / 2;
  const INOUT_CUBIC = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  const IN_CUBIC = t => t * t * t;
  function spring(ts, k = 380, c = 20) {             // mass 1, released at 0, settles at 1
    if (ts <= 0) return 0; const w0 = Math.sqrt(k), z = c / (2 * w0);
    if (z >= 1) return 1 - Math.exp(-w0 * ts) * (1 + w0 * ts);
    const wd = w0 * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w0 * ts) * (Math.cos(wd * ts) + (z * w0 / wd) * Math.sin(wd * ts));
  }
  const sp = (f, s, k, c) => f < s ? 0 : spring((f - s) / FPS, k, c);
  const mixHex = (a, b, t) => { const pa = [1, 3, 5].map(i => parseInt(a.substr(i, 2), 16)), pb = [1, 3, 5].map(i => parseInt(b.substr(i, 2), 16));
    return 'rgb(' + pa.map((v, i) => Math.round(lerp(v, pb[i], t))).join(',') + ')'; };

  /* ---------- paper grain (deterministic) ---------- */
  const grain = document.createElement('canvas'); grain.width = grain.height = 256;
  { const g = grain.getContext('2d'), im = g.createImageData(256, 256); let s = 7;
    for (let i = 0; i < im.data.length; i += 4) { s = (s * 1103515245 + 12345) & 0x7fffffff; const v = s % 255;
      im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; } g.putImageData(im, 0, 0); }
  let grainPat = null;
  function paper(alpha = 1) {
    ctx.globalAlpha = alpha; ctx.fillStyle = PAPER; ctx.fillRect(0, 0, W, H);
    if (!grainPat) grainPat = ctx.createPattern(grain, 'repeat');
    ctx.globalAlpha = 0.028 * alpha; ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = grainPat; ctx.fillRect(0, 0, W, H);
    ctx.globalCompositeOperation = 'source-over';
    const v = ctx.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.3, W / 2, H / 2, Math.max(W, H) * 0.75);
    v.addColorStop(0, 'rgba(45,42,38,0)'); v.addColorStop(1, 'rgba(45,42,38,0.06)');
    ctx.globalAlpha = alpha; ctx.fillStyle = v; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1;
  }
  function inkBg() {
    ctx.fillStyle = INK; ctx.fillRect(0, 0, W, H);
    const v = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, Math.max(W, H) * 0.7);
    v.addColorStop(0, 'rgba(255,245,230,0.05)'); v.addColorStop(1, 'rgba(0,0,0,0.25)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
  }

  /* ---------- primitives ---------- */
  function rr(x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }
  function dot(x, y, r, col = RUST) { if (r <= 0) return; ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); }
  const LOCK = new Path2D(window.LOCK_D);
  /* the padlock full stop (brand viewBox 512 384 1023 1280): the body stays, the shackle lifts */
  function lock(cx, cy, h, lift, col = RUST) {
    const s = h / 1280; if (s <= 0) return;
    ctx.save(); ctx.translate(cx - 1023 / 2 * s, cy - 1280 / 2 * s); ctx.scale(s, s); ctx.translate(-512, -384); ctx.fillStyle = col;
    ctx.save(); ctx.beginPath(); ctx.rect(400, 836, 1300, 900); ctx.clip(); ctx.fill(LOCK); ctx.restore();
    ctx.save(); ctx.translate(0, -lift); ctx.beginPath(); ctx.rect(400, 200, 1300, 636); ctx.clip(); ctx.fill(LOCK); ctx.restore();
    ctx.restore();
  }
  function font(fam, px, wt = 600, ital = false) { return `${ital ? 'italic ' : ''}${wt} ${px}px ${fam}`; }
  /* a word rising out of an invisible slot on its own baseline (the reference's baseline mask) */
  function maskWord(txt, x, y, fnt, col, p, lineH, dir = 1) {
    ctx.font = fnt; const w = ctx.measureText(txt).width;
    ctx.save(); ctx.beginPath(); ctx.rect(x - 4 * u, y - lineH * 0.86, w + 8 * u, lineH * 1.12); ctx.clip();
    ctx.fillStyle = col; ctx.fillText(txt, x, y + (1 - p) * lineH * dir); ctx.restore(); return w;
  }
  function wrap(txt, fnt, maxW) { ctx.font = fnt; const out = []; let line = '';
    txt.split(' ').forEach(wd => { const t = line ? line + ' ' + wd : wd; if (ctx.measureText(t).width > maxW && line) { out.push(line); line = wd; } else line = t; });
    if (line) out.push(line); return out; }
  function shadowOn(blur, dy, a) { ctx.shadowColor = `rgba(45,42,38,${a})`; ctx.shadowBlur = blur; ctx.shadowOffsetY = dy; }
  function shadowOff() { ctx.shadowColor = 'transparent'; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0; }
  function tickMark(cx, cy, r, drawP, col = '#fff', wid) {   // a check drawn as a stroke
    if (drawP <= 0) return; const pts = [[-0.42, 0.02], [-0.12, 0.32], [0.45, -0.3]];
    const seg1 = Math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]), seg2 = Math.hypot(pts[2][0] - pts[1][0], pts[2][1] - pts[1][1]);
    const L = (seg1 + seg2) * drawP; ctx.strokeStyle = col; ctx.lineWidth = wid || r * 0.22; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.moveTo(cx + pts[0][0] * r, cy + pts[0][1] * r);
    if (L <= seg1) { const t = L / seg1; ctx.lineTo(cx + lerp(pts[0][0], pts[1][0], t) * r, cy + lerp(pts[0][1], pts[1][1], t) * r); }
    else { ctx.lineTo(cx + pts[1][0] * r, cy + pts[1][1] * r); const t = (L - seg1) / seg2; ctx.lineTo(cx + lerp(pts[1][0], pts[2][0], t) * r, cy + lerp(pts[1][1], pts[2][1], t) * r); }
    ctx.stroke();
  }

  /* ---------- layout ---------- */
  const HEAD = { size: P ? 124 * u : 176 * u };
  const CARD_W = 840 * u, CARD_H = 460 * u, CARD_SCALE = P ? 1.14 : 1;   // a tall screen shows the same card, bigger
  const CARD_C = P ? [W / 2, H * 0.58] : [W * 0.655, H * 0.5];
  const TITLE = P ? { x: 80 * u, y: H * 0.235, size: 92 * u } : { x: 130 * u, y: H * 0.41, size: 70 * u };
  const ANSWER = "the League's report on Manchuria";
  const BACK_TXT = "The League of Nations' 1932 report on Manchuria. It found that Japan's invasion was not self-defence.";

  /* "Every GCSE subject." with the rust dot as its full stop */
  function headlineLayout() {
    const fnt = font(SERIF, HEAD.size, 600); ctx.font = fnt; ctx.letterSpacing = `${-0.02 * HEAD.size}px`;
    const words = ['Every', 'GCSE', 'subject'], gap = HEAD.size * 0.26, dotR = HEAD.size * 0.085;
    const ws = words.map(w => ctx.measureText(w).width);
    if (P) {                                          // two lines on a tall screen
      const l1 = ws[0] + gap + ws[1], l2 = ws[2] + dotR * 3; const lh = HEAD.size * 1.08, y1 = H * 0.44, y2 = y1 + lh;
      const pos = [[W / 2 - l1 / 2, y1], [W / 2 - l1 / 2 + ws[0] + gap, y1], [W / 2 - l2 / 2, y2]];
      return { fnt, words, ws, pos, dot: [pos[2][0] + ws[2] + dotR * 1.6, y2 - dotR], dotR, lh: HEAD.size * 1.2, boardsY: y2 + 110 * u };
    }
    const total = ws[0] + ws[1] + ws[2] + gap * 2 + dotR * 3; let x = W / 2 - total / 2; const y = H * 0.5 + HEAD.size * 0.3;
    const pos = ws.map((w, i) => { const p = [x, y]; x += w + gap; return p; });
    return { fnt, words, ws, pos, dot: [pos[2][0] + ws[2] + dotR * 1.6, y - dotR], dotR, lh: HEAD.size * 1.2, boardsY: y + 110 * u };
  }

  /* ---------- the flashcard, drawn in card space (origin = card centre) ---------- */
  function flashcard(f, face, appear) {
    const w = CARD_W, h = CARD_H, L = -w / 2, T = -h / 2, pad = 44 * u;
    const inA = i => SOFT(prog(f, K.cardIn + 5 + i * 2, 14));          // staggered build of the contents
    const item = (i, draw) => { const a = appear ? inA(i) : 1; if (a <= 0) return; ctx.save(); ctx.globalAlpha *= a; ctx.translate(0, (1 - a) * 14 * u); draw(); ctx.restore(); };
    const right = f >= K.tick, tickS = sp(f, K.tick, 420, 15);
    // header
    item(0, () => {
      ctx.fillStyle = INK; ctx.font = font(SANS, 22 * u, 600); ctx.textAlign = 'left'; ctx.fillText('Flashcard revision', L + pad, T + 50 * u);
      ctx.textAlign = 'right'; ctx.font = font(SANS, 20 * u, 500); ctx.fillStyle = MUTED;
      if (!right) ctx.fillText('Card 4 of 14', -L - pad, T + 50 * u);
      else { const p = SOFT(prog(f, K.tick + 2, 14)); ctx.fillStyle = GREEN; ctx.font = font(SANS, 22 * u, 700);
        ctx.save(); ctx.beginPath(); ctx.rect(0, T + 20 * u, -L - pad + 4 * u, 42 * u); ctx.clip(); ctx.fillText('Right', -L - pad, T + 50 * u + (1 - p) * 34 * u); ctx.restore(); }
      ctx.textAlign = 'left'; ctx.fillStyle = LINE; ctx.fillRect(L, T + 80 * u, w, 2 * u);
    });
    if (face === 'front') {
      item(1, () => { ctx.fillStyle = MUTED; ctx.font = font(SANS, 16 * u, 700); ctx.letterSpacing = `${0.16 * 16 * u}px`; ctx.fillText('WHO OR WHAT?', L + pad, T + 136 * u); ctx.letterSpacing = '0px'; });
      item(2, () => { ctx.fillStyle = INK; ctx.font = font(SERIF, 48 * u, 600); ctx.fillText('The Lytton Report', L + pad, T + 198 * u); });
      // the answer box
      item(3, () => {
        const bx = L + pad, by = T + 238 * u, bw = w - pad * 2, bh = 80 * u;
        const typing = f >= K.typeFrom && !right, gp = SOFT(prog(f, K.tick, 10));
        rr(bx, by, bw, bh, 12 * u); ctx.fillStyle = right ? mixHex('#fdfcfa', GREEN_TINT, gp) : '#fdfcfa'; ctx.fill();
        ctx.lineWidth = (typing ? 2.5 : 2) * u; ctx.strokeStyle = right ? mixHex(INK, GREEN, gp) : typing ? INK : LINE; ctx.stroke();
        const n = f < K.typeFrom ? 0 : Math.min(ANSWER.length, Math.floor((f - K.typeFrom) / 1.5) + 1);
        const txt = ANSWER.slice(0, n); ctx.font = font(SANS, 27 * u, 500); ctx.fillStyle = INK; ctx.fillText(txt, bx + 26 * u, by + 50 * u);
        if (!txt) { ctx.fillStyle = '#b9b2a8'; ctx.fillText('Type what you remember', bx + 26 * u, by + 50 * u); }
        if (typing && Math.floor(f / 8) % 2 === 0) { const cw = ctx.measureText(txt).width; ctx.fillStyle = INK; ctx.fillRect(bx + 28 * u + cw, by + 24 * u, 2.5 * u, 34 * u); }
        if (right) { const cx = bx + bw - 44 * u, cy = by + bh / 2, r = 24 * u * tickS;
          const rp = prog(f, K.tick, 18); if (rp < 1) { ctx.strokeStyle = `rgba(47,125,79,${0.5 * (1 - rp)})`; ctx.lineWidth = 3 * u; ctx.beginPath(); ctx.arc(cx, cy, lerp(24, 90, SOFT(rp)) * u, 0, Math.PI * 2); ctx.stroke(); }
          dot(cx, cy, r, GREEN); tickMark(cx, cy, 24 * u * Math.max(0.01, tickS), prog(f, K.tick + 2, 7), '#fff', 4.5 * u); }
      });
      // Check button
      item(4, () => {
        const bx = L + pad, by = T + 350 * u, bw = 160 * u, bh = 62 * u;
        const press = f >= K.check ? 1 - 0.07 * Math.max(0, 1 - sp(f, K.check, 520, 26)) * (f - K.check < 3 ? (f - K.check + 1) / 3 : 1) : 1;
        const sc = f >= K.check && f < K.check + 3 ? 1 - 0.07 * (f - K.check + 1) / 3 : f >= K.check ? lerp(0.93, 1, sp(f, K.check + 3, 500, 22)) : 1;
        ctx.save(); ctx.translate(bx + bw / 2, by + bh / 2); ctx.scale(sc, sc);
        rr(-bw / 2, -bh / 2, bw, bh, 12 * u); ctx.fillStyle = right ? mixHex(INK, GREEN, SOFT(prog(f, K.tick, 10))) : INK; ctx.fill();
        ctx.fillStyle = '#fff'; ctx.font = font(SANS, 23 * u, 600); ctx.textAlign = 'center'; ctx.fillText(right ? 'Checked' : 'Check', 0, 8 * u); ctx.textAlign = 'left';
        ctx.restore(); void press;
      });
    } else {
      // the back: model answer, and what the pupil wrote
      ctx.fillStyle = MUTED; ctx.font = font(SANS, 16 * u, 700); ctx.letterSpacing = `${0.16 * 16 * u}px`; ctx.fillText('MODEL ANSWER', L + pad, T + 136 * u); ctx.letterSpacing = '0px';
      const fnt = font(SERIF, 36 * u, 600), lines = wrap(BACK_TXT, fnt, w - pad * 2); ctx.font = fnt; ctx.fillStyle = INK;
      lines.forEach((ln, i) => ctx.fillText(ln, L + pad, T + 196 * u + i * 48 * u));
      const yy = T + 196 * u + lines.length * 48 * u + 28 * u;
      ctx.fillStyle = LINE; ctx.fillRect(L + pad, yy - 22 * u, w - pad * 2, 2 * u);
      ctx.font = font(SANS, 22 * u, 500); ctx.fillStyle = MUTED; ctx.fillText('You wrote', L + pad, yy + 14 * u);
      ctx.fillStyle = INK; ctx.font = font(SANS, 24 * u, 500); ctx.fillText(ANSWER, L + pad, yy + 50 * u);
      const cx = -L - pad - 24 * u, cy = yy + 32 * u; dot(cx, cy, 24 * u, GREEN); tickMark(cx, cy, 24 * u, 1, '#fff', 4.5 * u);
    }
  }
  /* where the back face's tick sits, in canvas space (the zoom-through aims at it) */
  function backTickPos() {
    ctx.font = font(SERIF, 36 * u, 600); const lines = wrap(BACK_TXT, font(SERIF, 36 * u, 600), CARD_W - 88 * u);
    const T = -CARD_H / 2, yy = T + 196 * u + lines.length * 48 * u + 28 * u;
    const x = CARD_C[0] + (CARD_W / 2 - 44 * u - 24 * u) * CARD_SCALE, y = CARD_C[1] + (yy + 32 * u) * CARD_SCALE, d = 1.035;   // the card scene's drift at its end
    return [W / 2 + (x - W / 2) * d, H / 2 + (y - H / 2) * d];
  }

  function drift(f, s, e, amt) { const d = 1 + amt * INOUT_CUBIC(prog(f, s, e - s)); ctx.translate(W / 2, H / 2); ctx.scale(d, d); ctx.translate(-W / 2, -H / 2); }
  function cardScene(f) {
    paper(); ctx.save(); drift(f, K.cardIn, K.zoom, 0.035);
    const s = sp(f, K.cardIn, 300, 21);
    // headline beside (or above) the card
    const t = TITLE, lh = t.size * 1.12, fnt = font(SANS, t.size, 800);
    ctx.letterSpacing = `${-0.03 * t.size}px`;
    const l1 = P ? ['Type what you', 'remember.'] : ['Type what', 'you remember.'];
    l1.forEach((ln, i) => { let x = P ? W / 2 - (ctx.font = fnt, ctx.measureText(ln).width) / 2 : t.x;
      maskWord(ln, x, t.y + i * lh, fnt, INK, SOFT(prog(f, K.cardIn + 4 + i * 4, 18)), lh); });
    const l2 = 'Checked instantly.';
    { ctx.font = fnt; const x = P ? W / 2 - ctx.measureText(l2).width / 2 : t.x; maskWord(l2, x, t.y + 2 * lh + (P ? 0 : 18 * u), fnt, GREEN, SOFT(prog(f, K.tick + 2, 18)), lh); }
    ctx.letterSpacing = '0px';
    // the card: out of the dot, then the flip
    if (s <= 0) { ctx.restore(); return; }
    const flipP = INOUT_CUBIC(prog(f, K.flip, 14)), th = flipP * Math.PI, face = th < Math.PI / 2 ? 'front' : 'back';
    const sx = Math.max(0.002, Math.abs(Math.cos(th))), lift = Math.sin(th) * 0.04;
    const sc = lerp(0.06, 1, s) * (1 + lift) * CARD_SCALE;
    ctx.save(); ctx.translate(CARD_C[0], CARD_C[1]); ctx.scale(sc * sx, sc);
    shadowOn(lerp(10, 60, s) * u, lerp(4, 22, s) * u, 0.13 + lift); rr(-CARD_W / 2, -CARD_H / 2, CARD_W, CARD_H, 18 * u);
    const bodyT = clamp((f - K.cardIn) / 6); ctx.fillStyle = mixHex(RUST, CARD, bodyT); ctx.fill(); shadowOff();
    if (bodyT >= 1) flashcard(f, face, true);
    if (flipP > 0 && flipP < 1) { ctx.fillStyle = `rgba(45,42,38,${0.18 * Math.sin(th)})`; rr(-CARD_W / 2, -CARD_H / 2, CARD_W, CARD_H, 18 * u); ctx.fill(); }
    ctx.restore(); ctx.restore();
  }

  /* ---------- the test clip, frame by frame ---------- */
  function frame(f) {
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left'; ctx.letterSpacing = '0px';
    const C = [W / 2, H / 2], r0 = 15 * u;
    if (f < K.wipe + 10) {                                   // A: the padlock dot on ink
      inkBg();
      const dotS = sp(f, K.dotIn, 420, 17), grow = sp(f, K.lockIn, 300, 19), lift = sp(f, K.unlock, 360, 15) * 190;
      const out = IN_CUBIC(prog(f, K.lockOut, 8));
      if (f < K.lockOut + 8) {
        const lh = lerp(r0 * 2.2, 200 * u, grow) * (1 - out);
        const gl = ctx.createRadialGradient(C[0], C[1], 0, C[0], C[1], 420 * u); gl.addColorStop(0, `rgba(192,99,37,${0.2 * grow * (1 - out)})`); gl.addColorStop(1, 'rgba(192,99,37,0)');
        ctx.fillStyle = gl; ctx.fillRect(0, 0, W, H);
        const rp = prog(f, K.unlock, 22); if (rp > 0 && rp < 1) { ctx.strokeStyle = `rgba(192,99,37,${0.55 * (1 - rp)})`; ctx.lineWidth = 3 * u; ctx.beginPath(); ctx.arc(C[0], C[1], lerp(120, 520, SOFT(rp)) * u, 0, Math.PI * 2); ctx.stroke(); }
        if (grow < 0.2) dot(C[0], C[1], r0 * dotS * (1 - grow * 5), RUST);
        if (grow > 0) lock(C[0], C[1], lh, lift * (1 - out), RUST);
        if (out > 0.7) dot(C[0], C[1], r0 * (out - 0.7) / 0.3, RUST);
      } else if (f < K.wipe) {                               // the dot stretches into a line, rust to paper
        const s = INOUT_EXPO(prog(f, K.lockOut + 8, K.wipe - K.lockOut - 8));
        const hw = lerp(r0, W * 0.56, s), th = lerp(r0 * 2, 5 * u, s);
        rr(C[0] - hw, C[1] - th / 2, hw * 2, th, th / 2); ctx.fillStyle = mixHex(RUST, PAPER, s); ctx.fill();
      } else {                                               // the line opens into paper
        const s = SNAP(prog(f, K.wipe, 10)), hh = lerp(5 * u, H * 1.02, s);
        ctx.save(); ctx.beginPath(); ctx.rect(0, C[1] - hh / 2, W, hh); ctx.clip(); paper(); headline(f); ctx.restore();
      }
    } else if (f < K.cardIn) {                               // B: the headline, then the dot travels
      paper(); ctx.save(); drift(f, K.wipe, K.dotMove, 0.03); headline(f); ctx.restore();
    } else if (f < K.zoom) {                                 // C: the flashcard
      cardScene(f);
    } else if (f < K.collapse) {                             // D: zoom-through into the tick
      const [tx, ty] = backTickPos(), e = IN_EXPO(prog(f, K.zoom, 16)), z = Math.exp(Math.log(90) * e), m = SOFT(prog(f, K.zoom, 12));
      ctx.save(); ctx.translate(lerp(tx, C[0], m), lerp(ty, C[1], m)); ctx.scale(z, z); ctx.translate(-tx, -ty); cardScene(f); ctx.restore();
      const cover = clamp((z - 30) / 40); if (cover > 0) { ctx.globalAlpha = cover; ctx.fillStyle = GREEN; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1; }
    } else {                                                 // E: the green collapses into a dot on paper; the next scene begins
      paper();
      const s = INOUT_EXPO(prog(f, K.collapse, 16)), R = Math.hypot(W, H) / 2 + 10;
      const r = lerp(R, r0, s);
      if (f < K.next) { ctx.fillStyle = mixHex(GREEN, RUST, clamp((s - 0.55) / 0.45)); ctx.beginPath(); ctx.arc(C[0], C[1], r, 0, Math.PI * 2); ctx.fill(); }
      else nextTitle(f);
    }
    if (DEBUG) debugOverlay(f);
  }

  function headline(f) {
    const Lh = headlineLayout(); ctx.letterSpacing = `${-0.02 * HEAD.size}px`;
    const starts = [K.w1, K.w2, K.w3];
    Lh.words.forEach((w, i) => {
      const pin = SOFT(prog(f, starts[i], 18)), pout = IN_CUBIC(prog(f, K.textOut + i * 3, 10));
      if (pout >= 1) return;
      ctx.save(); ctx.font = Lh.fnt; const x = Lh.pos[i][0], y = Lh.pos[i][1];
      ctx.beginPath(); ctx.rect(x - 6 * u, y - Lh.lh * 0.86, Lh.ws[i] + 12 * u, Lh.lh * 1.14); ctx.clip();
      ctx.fillStyle = INK; ctx.fillText(w, x, y + (1 - pin) * Lh.lh - pout * Lh.lh); ctx.restore();
    });
    ctx.letterSpacing = '0px';
    // the full stop: the rust dot, which then travels to the card
    const ds = sp(f, K.w3 + 6, 420, 15);
    let [dx, dy] = Lh.dot, dr = Lh.dotR * ds;
    if (f >= K.dotMove) { const m = SOFT(prog(f, K.dotMove, 16)); dx = lerp(Lh.dot[0], CARD_C[0], m); dy = lerp(Lh.dot[1], CARD_C[1], m); dr = lerp(Lh.dotR, 26 * u, m); }
    dot(dx, dy, dr, RUST);
    // the boards, each rising on a sixteenth
    const boards = ['AQA', 'Edexcel', 'OCR', 'Eduqas'], bf = font(SANS, (P ? 34 : 36) * u, 600); ctx.font = bf; ctx.letterSpacing = `${0.02 * 36 * u}px`;
    const gap = 54 * u, bw = boards.map(b => ctx.measureText(b).width), tot = bw.reduce((a, b) => a + b, 0) + gap * 3; let x = W / 2 - tot / 2;
    boards.forEach((b, i) => { const pin = SOFT(prog(f, K.boards + i * 4, 16)), pout = IN_CUBIC(prog(f, K.textOut + 4 + i * 2, 10));
      if (pout < 1) maskWord(b, x, Lh.boardsY, bf, mixHex(MUTED, INK, 0.25), pin - pout * 1.0, 50 * u);
      if (i < 3) { ctx.fillStyle = LINE; const cxp = x + bw[i] + gap / 2; if (pin > 0.5 && pout < 0.5) dot(cxp, Lh.boardsY - 12 * u, 3.5 * u, '#cfc7bb'); }
      x += bw[i] + gap; });
    ctx.letterSpacing = '0px';
  }

  function nextTitle(f) {
    const words = ['Practice', 'that', 'marks', 'as', 'you', 'go'], size = P ? 96 * u : 120 * u, fnt = font(SERIF, size, 600);
    ctx.font = fnt; ctx.letterSpacing = `${-0.02 * size}px`; const gap = size * 0.26, dotR = size * 0.085;
    const ws = words.map(w => ctx.measureText(w).width);
    let lines = P ? [[0, 1, 2], [3, 4, 5]] : [[0, 1, 2, 3, 4, 5]];
    const lh = size * 1.1, y0 = H / 2 + size * 0.3 - (lines.length - 1) * lh / 2; let endX = 0, endY = 0;
    lines.forEach((ln, li) => { const tot = ln.reduce((a, i) => a + ws[i], 0) + gap * (ln.length - 1) + (li === lines.length - 1 ? dotR * 3 : 0);
      let x = W / 2 - tot / 2; const y = y0 + li * lh;
      ln.forEach(i => { maskWord(words[i], x, y, fnt, INK, SOFT(prog(f, K.next + 2 + i * 2, 16)), size * 1.2); x += ws[i] + gap; });
      endX = x - gap + dotR * 1.6; endY = y - dotR; });
    ctx.letterSpacing = '0px';
    const m = SOFT(prog(f, K.next, 14)); dot(lerp(W / 2, endX, m), lerp(H / 2, endY, m), lerp(15 * u, dotR, m), RUST);
  }

  /* ---------- style-frame scenes (stage 1 stills) ---------- */
  function practiceStill() {
    paper(); ctx.letterSpacing = '0px';
    const t = P ? { x: 80 * u, y: 250 * u } : { x: 150 * u, y: H * 0.4 }, size = P ? 84 * u : 76 * u, fnt = font(SANS, size, 800);
    ctx.letterSpacing = `${-0.03 * size}px`; ctx.font = fnt; ctx.fillStyle = INK;
    const lines = P ? ['Practice that marks', 'as you go'] : ['Practice that', 'marks as you go'];
    lines.forEach((ln, i) => { const x = P ? W / 2 - ctx.measureText(ln).width / 2 : t.x; ctx.fillText(ln, x, t.y + i * size * 1.12);
      if (i === lines.length - 1) dot(x + ctx.measureText(ln).width + size * 0.14, t.y + i * size * 1.12 - size * 0.085, size * 0.085, RUST); });
    ctx.letterSpacing = '0px';
    // the question card
    const cw = P ? 920 * u : 840 * u, ch = P ? 820 * u : 700 * u, cx = P ? W / 2 : W * 0.64, cy = P ? H * 0.6 : H * 0.5, L = cx - cw / 2, T = cy - ch / 2, pad = 44 * u;
    shadowOn(60 * u, 22 * u, 0.13); rr(L, T, cw, ch, 18 * u); ctx.fillStyle = CARD; ctx.fill(); shadowOff();
    ctx.font = font(SANS, 22 * u, 600); ctx.fillStyle = INK; ctx.fillText('Percentages', L + pad, T + 50 * u);
    ctx.textAlign = 'right'; ctx.font = font(SANS, 20 * u, 500); ctx.fillStyle = MUTED; ctx.fillText('Silver · question 3 of 7', L + cw - pad, T + 50 * u); ctx.textAlign = 'left';
    ctx.fillStyle = LINE; ctx.fillRect(L, T + 80 * u, cw, 2 * u);
    const q = wrap('A jacket costs £40. A sign says 25% off. How much do you pay?', font(SERIF, 36 * u, 600), cw - pad * 2);
    ctx.font = font(SERIF, 36 * u, 600); ctx.fillStyle = INK; q.forEach((ln, i) => ctx.fillText(ln, L + pad, T + 146 * u + i * 48 * u));
    // bar model: four £10 blocks, the last one taken off
    const by = T + 146 * u + q.length * 48 * u + 40 * u, bw = (cw - pad * 2) / 4, bh = 76 * u;
    for (let i = 0; i < 4; i++) { const x = L + pad + i * bw; rr(x + 4 * u, by, bw - 8 * u, bh, 12 * u);
      ctx.fillStyle = i === 3 ? '#f6e3d5' : '#f3f0ea'; ctx.fill(); ctx.lineWidth = 2 * u; ctx.strokeStyle = i === 3 ? RUST : LINE; ctx.stroke();
      ctx.font = font(SANS, 26 * u, 600); ctx.fillStyle = i === 3 ? RUST : INK; ctx.textAlign = 'center'; ctx.fillText('£10', x + bw / 2, by + 48 * u); ctx.textAlign = 'left'; }
    ctx.font = font(SANS, 20 * u, 600); ctx.fillStyle = RUST; ctx.textAlign = 'center'; ctx.fillText('25% off', L + pad + 3.5 * bw, by - 14 * u); ctx.textAlign = 'left';
    // answer row, marked right
    const ay = by + bh + 44 * u; ctx.font = font(SANS, 24 * u, 600); ctx.fillStyle = INK; ctx.fillText('Answer', L + pad, ay + 46 * u);
    const ax = L + pad + 120 * u; rr(ax, ay, 220 * u, 72 * u, 12 * u); ctx.fillStyle = GREEN_TINT; ctx.fill(); ctx.lineWidth = 2.5 * u; ctx.strokeStyle = GREEN; ctx.stroke();
    ctx.font = font(SANS, 30 * u, 600); ctx.fillStyle = INK; ctx.fillText('£30', ax + 22 * u, ay + 48 * u);
    dot(ax + 220 * u - 38 * u, ay + 36 * u, 22 * u, GREEN); tickMark(ax + 220 * u - 38 * u, ay + 36 * u, 22 * u, 1, '#fff', 4 * u);
    // feedback: a whole tinted panel, not a stripe
    const fy = ay + 100 * u; rr(L + pad, fy, cw - pad * 2, 96 * u, 12 * u); ctx.fillStyle = GREEN_TINT; ctx.fill();
    ctx.font = font(SANS, 24 * u, 700); ctx.fillStyle = GREEN; ctx.fillText('Right.', L + pad + 24 * u, fy + 42 * u);
    ctx.font = font(SANS, 22 * u, 500); ctx.fillStyle = INK; ctx.fillText('25% of £40 is £10, so you pay £40 − £10 = £30.', L + pad + 24 * u, fy + 74 * u);
    // three in a row: circles, not a pill
    const sy = T + ch - 46 * u; ctx.font = font(SANS, 20 * u, 600); ctx.fillStyle = MUTED; ctx.fillText('3 in a row', L + pad, sy + 7 * u);
    for (let i = 0; i < 4; i++) dot(L + pad + 130 * u + i * 30 * u, sy, 9 * u, i < 3 ? GREEN : '#e6e0d6');
  }
  function endStill() {
    paper(); const size = P ? 150 * u : 190 * u; ctx.font = font(MARK, size, 400); ctx.fillStyle = INK;
    const word = 'StudyVault', ww = ctx.measureText(word).width, lh = size * 0.34, total = ww + size * 0.06 + lh * 1023 / 1280;
    const x = W / 2 - total / 2, y = H / 2 + size * 0.05; ctx.fillText(word, x, y);
    lock(x + ww + size * 0.06 + lh * 1023 / 1280 / 2, y - lh / 2, lh, 0, RUST);
    ctx.textAlign = 'center'; ctx.font = font(SANS, (P ? 34 : 36) * u, 500); ctx.fillStyle = MUTED;
    if (P) { ctx.fillText('Free GCSE revision.', W / 2, y + 130 * u); ctx.fillText('Every major exam board. No ads.', W / 2, y + 180 * u); }
    else ctx.fillText('Free GCSE revision. Every major exam board. No ads.', W / 2, y + 120 * u);
    ctx.font = font(SANS, (P ? 38 : 40) * u, 600); ctx.fillStyle = INK; ctx.fillText('www.studyvault.co.uk', W / 2, y + (P ? 270 : 210) * u); ctx.textAlign = 'left';
  }

  function debugOverlay(f) {
    const bar = Math.floor(f / 64), beat = Math.floor(f % 64 / 16), six = Math.floor(f % 16 / 4);
    ctx.fillStyle = 'rgba(0,0,0,0.6)'; ctx.fillRect(0, 0, 330, 60); ctx.fillStyle = f % 16 === 0 ? '#ff4d4d' : '#fff';
    ctx.font = '600 28px monospace'; ctx.fillText(`f${f} ${bar}.${beat}.${six}`, 16, 40);
    if (f % 16 < 3) { ctx.fillStyle = '#ff4d4d'; ctx.fillRect(W - 60, 10, 40, 40); }
  }

  window.renderFrame = f => { if (STILL === 'practice') practiceStill(); else if (STILL === 'end') endStill(); else frame(f); };
  Promise.all([
    document.fonts.load(font(SERIF, 40, 600)), document.fonts.load(font(SANS, 40, 800)), document.fonts.load(font(SANS, 40, 700)),
    document.fonts.load(font(SANS, 40, 600)), document.fonts.load(font(SANS, 40, 500)), document.fonts.load(font(MARK, 40, 400)),
  ]).then(() => document.fonts.ready).then(() => { window.renderFrame(0); window.READY = true; });
})();
