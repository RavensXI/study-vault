/* comp.js — draws frame f of the launch video onto a canvas, for any of three shapes.
   Every change of picture and every word is keyed to a grid frame from timeline.js, so the edit
   is the music. URL params: ?ar=16x9|1x1|9x16  &debug=1 (beat overlay)  &f=N (preview one frame). */
(function () {
  const TL = window.TL, F = TL.F, E = TL.EIGHTH;
  const q = new URLSearchParams(location.search);
  const AR = q.get('ar') || '16x9', DEBUG = q.get('debug') === '1';
  const SIZE = { '16x9': [1920, 1080], '1x1': [1080, 1080], '9x16': [1080, 1920] }[AR];
  const [W, H] = SIZE;
  const cv = document.getElementById('c'); cv.width = W; cv.height = H;
  const g = cv.getContext('2d');
  const PAPER = '#faf8f5', INK = '#2d2a26', RUST = '#c06325', MUTED = '#6f675e', GREEN = '#2f7d4f';

  /* ---------- assets ---------- */
  const C = 'captures/final/';
  const IMG = {};
  const list = ['home-d', 'home-p', 'subjects-d-full', 'lesson-d-mid', 'lesson-d-podcast', 'lesson-p-top',
    'fc-after-00', 'fc-after-02', 'maths-s0-t0', 'maths-s0-t1', 'maths-s0-a1', 'maths-s1-t0', 'maths-s1-t1', 'maths-s1-a2',
    'es-0', 'en-0', 'en-after-3', 'ai-wait-00', 'ai-result', 'wd-open', 'wd-a1', 'wd-a2', 'wd-result', 'teach-questions'];
  for (let i = 0; i <= 10; i++) list.push('fc-type-' + String(i).padStart(2, '0'));
  for (let i = 0; i < 7; i++) list.push('es-p' + i + '-ok');
  for (let i = 0; i < 6; i++) list.push('en-r' + i);
  for (let i = 1; i <= 12; i++) list.push('ai-type-' + String(i).padStart(2, '0'));
  const MONT = ['science-aqa', 'geography-aqa', 'english-literature-aqa', 'religious-studies-aqa', 'business-aqa', 'psychology-aqa',
    'computer-science-aqa', 'drama-aqa', 'astronomy-edexcel', 'sociology-aqa', 'economics-aqa', 'physical-education-aqa',
    'geology-eduqas', 'film-studies-eduqas', 'history-edexcel', 'classical-civilisation-ocr'];
  MONT.forEach(m => list.push('mont-' + m));
  let pending = list.length;
  window.READY = false;
  list.forEach(n => { const im = new Image(); im.onload = im.onerror = () => { if (--pending === 0) boot(); }; im.src = C + n + '.png'; IMG[n] = im; });
  function boot() {
    Promise.all(['800 80px Inter', '600 40px Inter', '500 40px Inter', 'italic 500 40px "Source Serif 4"', '600 40px "Source Serif 4"', '80px "Young Serif"']
      .map(s => document.fonts.load(s))).then(() => document.fonts.ready).then(() => { window.READY = true; if (q.get('f')) draw(+q.get('f')); });
  }

  /* ---------- crops (capture pixels) ---------- */
  const CROP = {
    read: [52, 590, 1320, 660], hear: [0, 0, 1170, 2532], watch: [1922, 922, 893, 511],
    cards: [38, 595, 1094, 1342], maths: [1180, 330, 1240, 1270], es: [960, 300, 1340, 1480], en: [620, 420, 1780, 1380],
    ai: [720, 108, 1440, 1584], wd: [490, 380, 1900, 1040], wdR: [490, 455, 1900, 865], teach: [376, 619, 2128, 907], mont: [0, 187, 1170, 1521],
    home: [0, 0, 2880, 1800], homeP: [0, 0, 1170, 2532],
  };
  const FILL = { '16x9': null, '1x1': 1008 / 740, '9x16': 1020 / 900 }[AR];
  const ROW_BOTTOMS = [770, 936, 1104, 1270, 1394, 1516];   // teacher table: header, rows 1..5 (capture px)

  /* ---------- layout per shape ---------- */
  const LAY = {
    '16x9': { text: { x: 96, y: 0, w: 610, h: H }, media: { x: 740, y: 70, w: 1120, h: 940 }, head: 76, sub: 40, label: 26, align: 'left', vcenter: true },
    '1x1': { text: { x: 70, y: 60, w: 940, h: 250 }, media: { x: 36, y: 330, w: 1008, h: 710 }, head: 72, sub: 34, label: 24, align: 'left', vcenter: false },
    '9x16': { text: { x: 70, y: 170, w: 940, h: 520 }, media: { x: 30, y: 700, w: 1020, h: 1120 }, head: 96, sub: 42, label: 28, align: 'left', vcenter: false },
  }[AR];

  /* ---------- helpers ---------- */
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const ease = t => 1 - Math.pow(1 - clamp(t), 4);                  // soft close
  const easeBack = t => { t = clamp(t); const c = 1.9; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };
  let GRAIN = null;
  function paper() {
    g.fillStyle = PAPER; g.fillRect(0, 0, W, H);
    if (!GRAIN) { GRAIN = document.createElement('canvas'); GRAIN.width = 256; GRAIN.height = 256; const gc = GRAIN.getContext('2d'); const d = gc.createImageData(256, 256);
      let s = 7; for (let i = 0; i < d.data.length; i += 4) { s = (s * 16807) % 2147483647; const v = s % 20; d.data[i] = d.data[i + 1] = d.data[i + 2] = 120 + v; d.data[i + 3] = 10; } gc.putImageData(d, 0, 0); }
    g.fillStyle = g.createPattern(GRAIN, 'repeat'); g.fillRect(0, 0, W, H);
    const rg = g.createRadialGradient(W * 0.5, H * 0.45, Math.min(W, H) * 0.3, W * 0.5, H * 0.5, Math.max(W, H) * 0.8);
    rg.addColorStop(0, 'rgba(255,255,255,0)'); rg.addColorStop(1, 'rgba(120,95,70,0.08)'); g.fillStyle = rg; g.fillRect(0, 0, W, H);
  }
  function rr(x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
  function fitRect(cw, ch, box) { const s = Math.min(box.w / cw, box.h / ch); const w = cw * s, h = ch * s; return { x: box.x + (box.w - w) / 2, y: box.y + (box.h - h) / 2, w, h }; }
  function coverRect(cw, ch, box) { const s = Math.max(box.w / cw, box.h / ch); const w = cw * s, h = ch * s; return { x: box.x + (box.w - w) / 2, y: box.y + (box.h - h) / 2, w, h }; }
  /* a screen: image crop fitted into box, framed (card or phone), with scale about its centre */
  function screen(name, crop, box, o = {}) {
    const im = IMG[name]; if (!im || !im.width) return;
    let [cx, cy, cw, ch] = crop;
    const fillA = o.phone ? null : (o.fill || FILL);
    if (fillA && cw / ch > fillA) { const nw = ch * fillA; cx = cx + (cw - nw) * (o.fx == null ? 0.5 : o.fx); cw = nw; }
    let r = fitRect(cw, ch, box);
    const s = o.scale || 1, a = o.alpha == null ? 1 : o.alpha, dy = o.dy || 0;
    g.save(); g.globalAlpha = a;
    g.translate(r.x + r.w / 2, r.y + r.h / 2 + dy); g.scale(s, s); g.translate(-(r.x + r.w / 2), -(r.y + r.h / 2));
    const rad = o.phone ? Math.min(r.w, r.h) * 0.075 : 18;
    if (o.phone) { // bezel
      g.save(); g.shadowColor = 'rgba(45,42,38,0.28)'; g.shadowBlur = 50; g.shadowOffsetY = 22;
      rr(r.x - 14, r.y - 14, r.w + 28, r.h + 28, rad + 12); g.fillStyle = '#1f1d1b'; g.fill(); g.restore();
    } else {
      g.save(); g.shadowColor = 'rgba(45,42,38,0.22)'; g.shadowBlur = 44; g.shadowOffsetY = 18; rr(r.x, r.y, r.w, r.h, rad); g.fillStyle = '#fff'; g.fill(); g.restore();
    }
    g.save(); rr(r.x, r.y, r.w, r.h, rad); g.clip();
    const clipH = o.clipH == null ? ch : o.clipH;
    g.drawImage(im, cx, cy, cw, clipH, r.x, r.y, r.w, r.h * clipH / ch);
    if (clipH < ch) { g.fillStyle = '#fbfaf7'; g.fillRect(r.x, r.y + r.h * clipH / ch, r.w, r.h * (1 - clipH / ch)); }
    g.restore();
    if (!o.phone) { g.strokeStyle = 'rgba(45,42,38,0.10)'; g.lineWidth = 1.5; rr(r.x, r.y, r.w, r.h, rad); g.stroke(); }
    g.restore();
    return r;
  }
  /* the push every picture change gets: lands with a small overshoot on the cut frame */
  const push = (f, f0) => 1.045 - 0.045 * easeBack((f - f0) / 8);
  const pulse = f => { const b = f % TL.BEAT; return 1 + 0.010 * Math.exp(-b / 2.5); };

  /* words: each pops on its own grid frame */
  function word(txt, x, y, size, f, f0, o = {}) {
    if (f < f0) return 0;
    const p = (f - f0) / 7;
    const s = o.noPop ? 1 : 1 + 0.22 * (1 - easeBack(p));
    const a = clamp((f - f0) / 3);
    g.save(); g.globalAlpha = a * (o.alpha == null ? 1 : o.alpha);
    g.font = o.font || `800 ${size}px Inter`; g.fillStyle = o.color || INK; g.textBaseline = 'alphabetic';
    const w = g.measureText(txt).width; const ax = o.align === 'center' ? x - w / 2 : x;
    g.translate(ax + w / 2, y - size * 0.35); g.scale(s, s); g.translate(-(ax + w / 2), -(y - size * 0.35));
    if (o.letter) { g.letterSpacing = o.letter + 'px'; }
    g.fillText(txt, ax, y); g.restore();
    return w;
  }
  function wrapLines(txt, size, maxW, font) { g.font = font || `800 ${size}px Inter`; const words = txt.split(' '); const out = []; let line = '';
    words.forEach(w => { const t = line ? line + ' ' + w : w; if (g.measureText(t).width > maxW && line) { out.push(line); line = w; } else line = t; }); if (line) out.push(line); return out; }
  /* a stack of headline lines + optional label/sub, each item: {t, f, kind:'head'|'sub'|'label'} */
  function textBlock(f, items, box) {
    box = box || LAY.text;
    const rows = [];
    items.forEach(it => {
      const size = it.kind === 'sub' ? LAY.sub : it.kind === 'label' ? LAY.label : (it.size || LAY.head);
      const font = it.kind === 'sub' ? `italic 500 ${size}px "Source Serif 4"` : it.kind === 'label' ? `600 ${size}px Inter` : `800 ${size}px Inter`;
      const lines = it.kind === 'label' ? [it.t.toUpperCase()] : wrapLines(it.t, size, box.w, font);
      lines.forEach((ln, i) => rows.push({ ln, size, font, f: it.f + (it.stagger ? i * it.stagger : 0), kind: it.kind || 'head', color: it.color, gap: it.kind === 'label' ? size * 1.9 : it.kind === 'sub' ? size * 1.45 : size * 1.08, swash: it.swash && i === lines.length - 1 }));
    });
    const total = rows.reduce((a, r) => a + r.gap, 0);
    let y = LAY.vcenter ? box.y + (box.h - total) / 2 : box.y;
    rows.forEach(r => {
      y += r.gap;
      const color = r.color || (r.kind === 'label' ? RUST : r.kind === 'sub' ? MUTED : INK);
      const w = word(r.ln, box.x, y - (r.kind === 'head' ? r.size * 0.2 : 0), r.size, f, r.f, { font: r.font, color, letter: r.kind === 'label' ? 3 : 0, noPop: r.kind === 'sub' });
      if (r.swash && f >= r.f) swash(box.x, y + r.size * 0.02, Math.min(w, box.w), f, r.f + 3);
      if (r.kind === 'label') y += 4;
    });
  }
  /* the site's hand-drawn underline, drawn on over 8 frames */
  function swash(x, y, w, f, f0) {
    const p = ease((f - f0) / 8); if (p <= 0) return;
    g.save(); g.strokeStyle = RUST; g.lineWidth = Math.max(4, LAY.head * 0.06); g.lineCap = 'round';
    g.beginPath(); const n = 30; for (let i = 0; i <= n * p; i++) { const t = i / n; const xx = x + t * w; const yy = y + Math.sin(t * Math.PI) * -6 + Math.sin(t * 9) * 1.5; i ? g.lineTo(xx, yy) : g.moveTo(xx, yy); } g.stroke(); g.restore();
  }
  function stamp(txt, cx, cy, size, f, f0, color) {
    if (f < f0) return; const p = (f - f0) / 8; const s = 1 + 0.9 * (1 - easeBack(p)); const a = clamp((f - f0) / 2);
    g.save(); g.globalAlpha = a; g.translate(cx, cy); g.scale(s, s); g.rotate(-0.06);
    g.font = `800 ${size}px Inter`; const w = g.measureText(txt).width;
    g.shadowColor = 'rgba(45,42,38,0.25)'; g.shadowBlur = 30; g.shadowOffsetY = 10;
    g.fillStyle = color || GREEN; rr(-w / 2 - size * 0.35, -size * 0.8, w + size * 0.7, size * 1.15, 14); g.fill();
    g.shadowColor = 'transparent'; g.fillStyle = '#fff'; g.fillText(txt, -w / 2, size * 0.18); g.restore();
  }
  function wordmark(cx, cy, size, f, f0, o = {}) {
    if (f < f0) return;
    const p = (f - f0) / 10; const s = o.noPop ? 1 : 1 + 0.55 * (1 - easeBack(p));
    const shake = o.noPop ? 0 : Math.max(0, 1 - (f - f0) / 8) * 10;
    g.save(); g.font = `${size}px "Young Serif"`; const w = g.measureText('StudyVault').width; const lockW = size * 0.24;
    const total = w + lockW + size * 0.06;
    g.translate(cx + Math.sin(f * 2.3) * shake, cy + Math.cos(f * 1.7) * shake); g.scale(s, s);
    g.fillStyle = INK; g.fillText('StudyVault', -total / 2, size * 0.32);
    // padlock full stop (brand viewBox 512 384 1023 1280 on a 2048 path)
    const lock = new Path2D(window.LOCK_D); const lh = size * 0.3, lw = lh * 1023 / 1280;
    const lx = -total / 2 + w + size * 0.06, ly = size * 0.32 - lh;
    const drop = o.noPop ? 0 : (1 - easeBack(clamp((f - f0 - 3) / 8))) * -size * 0.8;
    g.save(); g.translate(lx, ly + drop); g.scale(lw / 1023, lh / 1280); g.translate(-512, -384); g.fillStyle = RUST; g.fill(lock); g.restore();
    g.restore();
  }
  function flash(f, f0, len = 5) { const a = 1 - (f - f0) / len; if (a > 0 && f >= f0) { g.save(); g.globalAlpha = a * 0.55; g.fillStyle = '#fff'; g.fillRect(0, 0, W, H); g.restore(); } }
  const pick = (f, seq) => { let cur = seq[0]; for (const s of seq) if (f >= s.f) cur = s; return cur; };

  /* ---------- scenes ---------- */
  function sIntro(f) {
    const s0 = F(0);
    const cover = AR === '9x16' ? ['home-p', CROP.homeP] : ['home-d', CROP.home];
    const im = IMG[cover[0]], [cx, cy, cw, ch] = cover[1];
    // slow push, then a punch-in on beat 2 toward the wordmark
    const z = 1.02 + 0.05 * (f - s0) / TL.BAR + (f >= F(0, 2) ? 0.10 * easeBack((f - F(0, 2)) / 8) : 0);
    const r = coverRect(cw, ch, { x: 0, y: 0, w: W, h: H });
    const fx = AR === '9x16' ? 0.5 : 0.5, fy = AR === '9x16' ? 0.33 : 0.52;
    g.save(); g.translate(W * fx, H * fy); g.scale(z * pulse(f), z * pulse(f)); g.translate(-W * fx, -H * fy);
    g.drawImage(im, cx, cy, cw, ch, r.x, r.y, r.w, r.h); g.restore();
    const a = 1 - clamp((f - s0) / 6); if (a > 0) { g.fillStyle = `rgba(250,248,245,${a})`; g.fillRect(0, 0, W, H); }
  }
  function sBoards(f) {
    paper();
    // the subject list races by underneath
    const im = IMG['subjects-d-full'];
    if (im && im.width) { const sc = W / 1400; const scroll = (f - F(1)) * 38; g.save(); g.globalAlpha = 0.09;
      g.drawImage(im, 700, 300 + scroll % (im.height - 2400), 1500, 2400, W * 0.5 - 1500 * sc / 2, 0, 1500 * sc, 2400 * sc); g.restore(); }
    const big = AR === '16x9' ? 150 : AR === '1x1' ? 130 : 150;
    const cy = AR === '9x16' ? H * 0.38 : H * 0.42;
    const shake = f >= F(1, 3) ? (f - F(1, 3)) * 0.35 : 0;
    g.save(); g.translate(Math.sin(f * 3.1) * shake, Math.cos(f * 2.7) * shake);
    word('98 courses.', W / 2, cy, big, f, F(1, 0), { align: 'center' });
    const boards = [['AQA', F(1, 1, 0)], ['Edexcel', F(1, 1, 1)], ['OCR', F(1, 2, 0)], ['Eduqas', F(1, 2, 1)]];
    const bs = AR === '16x9' ? 64 : AR === '1x1' ? 56 : 62;
    if (AR === '9x16') {
      boards.forEach(([b, t], i) => word(b, W / 2, cy + 150 + i * bs * 1.35, bs, f, t, { align: 'center', color: RUST, font: `800 ${bs}px Inter` }));
      word('Every major exam board.', W / 2, cy + 150 + 4 * bs * 1.35 + 30, 40, f, F(1, 3), { align: 'center', font: 'italic 500 40px "Source Serif 4"', color: MUTED, noPop: true });
    } else {
      g.font = `800 ${bs}px Inter`; const gap = bs * 0.9; const widths = boards.map(([b]) => g.measureText(b).width); const tw = widths.reduce((a, b) => a + b, 0) + gap * 3;
      let x = W / 2 - tw / 2; boards.forEach(([b, t], i) => { word(b, x, cy + bs * 2, bs, f, t, { color: RUST, font: `800 ${bs}px Inter` }); x += widths[i] + gap; });
      word('Every major exam board.', W / 2, cy + bs * 2 + 90, AR === '1x1' ? 36 : 42, f, F(1, 3), { align: 'center', font: `italic 500 ${AR === '1x1' ? 36 : 42}px "Source Serif 4"`, color: MUTED, noPop: true });
    }
    g.restore();
  }
  function sDrop(f) {
    paper();
    const i = Math.floor((f - F(2)) / E);                      // 0..15, one swap per eighth
    const n = AR === '16x9' ? 5 : AR === '1x1' ? 3 : 2;
    const rows = AR === '9x16' ? 2 : 1;
    const area = AR === '16x9' ? { x: 60, y: 330, w: W - 120, h: 700 } : AR === '1x1' ? { x: 50, y: 330, w: W - 100, h: 680 } : { x: 60, y: 640, w: W - 120, h: 1220 };
    const cols = n, tileW = (area.w - (cols - 1) * 30) / cols, tileH = (area.h - (rows - 1) * 30) / rows;
    const slots = cols * rows; let k = 0;
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++, k++) {
      // eighth j swaps slot j % slots to subject (slots + j) % 16: one tile changes on every eighth
      let j = -1; for (let t = i; t >= 0; t--) if (t % slots === k) { j = t; break; }
      const idx = j < 0 ? k : (slots + j) % MONT.length;
      const box = { x: area.x + c * (tileW + 30), y: area.y + r * (tileH + 30), w: tileW, h: tileH };
      const sc = j >= 0 ? push(f, F(2) + j * E) : 1;
      screen('mont-' + MONT[idx], CROP.mont, box, { phone: true, scale: sc * pulse(f) });
    }
    // headline band
    const big = AR === '16x9' ? 110 : AR === '1x1' ? 96 : 118;
    const ty = AR === '16x9' ? 200 : AR === '1x1' ? 200 : 380;
    if (f < F(3)) word('4,490 lessons.', AR === '9x16' ? W / 2 : W / 2, ty, big, f, F(2), { align: 'center' });
    else {
      g.font = `800 ${big}px Inter`; const w1 = g.measureText('Free.').width, w2 = g.measureText(' No ads.').width;
      if (AR === '9x16') { word('Free.', W / 2, ty - 70, big, f, F(3), { align: 'center', color: RUST }); word('No ads.', W / 2, ty + 70, big, f, F(3, 1), { align: 'center' }); }
      else { const x0 = W / 2 - (w1 + w2) / 2; word('Free.', x0, ty, big, f, F(3), { color: RUST }); word('No ads.', x0 + w1 + big * 0.3, ty, big, f, F(3, 1)); }
    }
    if (f >= F(2) && f < F(2) + 5) flash(f, F(2), 5);
  }
  /* a zoom that keeps the frame's shape: k times closer, centred on (cx, cy) in capture px, clamped inside the crop */
  function zoomCrop(full, cx, cy, k) { const [x, y, w, h] = full; const zw = w / k, zh = h / k;
    const zx = clamp(cx - zw / 2, x, x + w - zw), zy = clamp(cy - zh / 2, y, y + h - zh); return [zx, zy, zw, zh]; }
  const lerpCrop = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
  function mediaSeq(f, seq, opts = {}) {
    const cur = pick(f, seq);
    const sc = push(f, cur.cut != null ? cur.cut : cur.f) * pulse(f);
    let crop = cur.crop;
    const z = opts.zoom; if (z && f >= z.f0) crop = lerpCrop(crop, zoomCrop(crop, z.cx, z.cy, z.k), ease((f - z.f0) / 9));
    const first = seq[0].f, lift = f - first < 10 ? (1 - easeBack((f - first) / 9)) * 70 : 0;
    return screen(cur.img, crop, opts.box || LAY.media, Object.assign({ scale: sc, dy: lift }, opts, cur.o || {}));
  }
  function sLesson(f) {
    paper();
    mediaSeq(f, [{ f: F(4, 0), img: 'lesson-d-mid', crop: CROP.read, o: { fx: 0 } }, { f: F(4, 2), img: 'lesson-p-top', crop: CROP.hear, o: { phone: true } }, { f: F(5, 0), img: 'lesson-d-mid', crop: CROP.watch }]);
    textBlock(f, [{ t: 'Read it.', f: F(4, 0) }, { t: 'Hear it.', f: F(4, 2) }, { t: 'Watch it.', f: F(5, 0), swash: true }, { t: 'Narration, podcasts and video.', f: F(5, 2), kind: 'sub' }]);
  }
  function sCards(f) {
    paper();
    const seq = [];
    for (let k = 0; k < 8; k++) seq.push({ f: F(6) + k * E, img: 'fc-type-' + String(Math.round(k * 10 / 7)).padStart(2, '0'), crop: CROP.cards, cut: F(6) });
    seq.push({ f: F(7, 0), img: 'fc-after-00', crop: CROP.cards, cut: F(6) });
    seq.push({ f: F(7, 1), img: 'fc-after-02', crop: CROP.cards });
    const box = AR === '16x9' ? { x: 880, y: 70, w: 900, h: 940 } : LAY.media;
    mediaSeq(f, seq, { box });
    textBlock(f, [{ t: 'Flashcards', f: F(6, 0), kind: 'label' }, { t: 'Type what you remember.', f: F(6, 0) }, { t: 'Checked in a second.', f: F(7, 1), color: GREEN, swash: true }]);
  }
  function sPractice(f) {
    paper();
    const seq = [
      { f: F(8, 0, 0), img: 'maths-s0-t0', crop: CROP.maths, cut: F(8) }, { f: F(8, 0, 1), img: 'maths-s0-t1', crop: CROP.maths, cut: F(8) },
      { f: F(8, 1), img: 'maths-s0-a1', crop: CROP.maths, cut: F(8) }, { f: F(8, 2, 0), img: 'maths-s1-t0', crop: CROP.maths, cut: F(8) },
      { f: F(8, 2, 1), img: 'maths-s1-t1', crop: CROP.maths, cut: F(8) }, { f: F(8, 3), img: 'maths-s1-a2', crop: CROP.maths, cut: F(8) },
      { f: F(9), img: 'es-0', crop: CROP.es },
    ];
    for (let i = 0; i < 7; i++) seq.push({ f: F(9) + (i + 1) * E, img: 'es-p' + i + '-ok', crop: CROP.es, cut: F(9) });
    seq.push({ f: F(10), img: 'en-0', crop: CROP.en });
    for (let i = 0; i < 6; i++) seq.push({ f: F(10) + (i + 1) * E, img: 'en-r' + i, crop: CROP.en, cut: F(10) });
    seq.push({ f: F(10, 3, 1), img: 'en-after-3', crop: CROP.en, cut: F(10) });
    mediaSeq(f, seq);
    const label = f < F(9) ? ['Maths', F(8)] : f < F(10) ? ['Spanish', F(9)] : ['English Language', F(10)];
    textBlock(f, [{ t: label[0], f: label[1], kind: 'label' }, { t: 'Practice that marks as you go.', f: F(8), swash: true }]);
  }
  function sAI(f) {
    paper();
    const seq = [];
    for (let k = 0; k < 8; k++) seq.push({ f: F(11) + k * E, img: 'ai-type-' + String(Math.max(1, Math.round((k + 1) * 12 / 8))).padStart(2, '0'), crop: CROP.ai, cut: F(11) });
    seq.push({ f: F(12, 0), img: 'ai-wait-00', crop: CROP.ai, cut: F(11) });
    seq.push({ f: F(12, 1), img: 'ai-result', crop: CROP.ai });
    const r = mediaSeq(f, seq, { zoom: { f0: F(12, 3), cx: 1150, cy: 520, k: 1.45 } });
    if (r) stamp('4 / 4', r.x + r.w * 0.72, r.y + r.h * 0.2, AR === '16x9' ? 84 : 76, f, F(12, 1));
    textBlock(f, [{ t: 'Exam answers', f: F(11, 0) }, { t: 'marked.', f: F(11, 1), swash: true }, { t: 'Feedback in seconds. Hosted in London.', f: F(12, 2), kind: 'sub' }]);
  }
  function sWidget(f) {
    paper();
    mediaSeq(f, [{ f: F(13, 0), img: 'wd-open', crop: CROP.wd, o: { fx: 0 } }, { f: F(13, 2), img: 'wd-a1', crop: CROP.wd, cut: F(13) }, { f: F(13, 3), img: 'wd-a2', crop: CROP.wd, cut: F(13) }, { f: F(14, 0), img: 'wd-result', crop: CROP.wdR }], { zoom: { f0: F(14, 1), cx: 1150, cy: 1130, k: 1.5 }, fx: 0 });
    textBlock(f, [{ t: 'Interactive', f: F(13, 0), kind: 'label' }, { t: 'Built around the mistakes pupils make.', f: F(13, 0), stagger: E, swash: true }, { t: 'Three right in a row to master it.', f: F(14, 2), kind: 'sub' }]);
  }
  function sTeacher(f) {
    paper();
    const reveal = [F(15, 0), F(15, 1), F(15, 2), F(15, 3), F(15, 3, 1)];
    let rows = 0; reveal.forEach(t => { if (f >= t) rows++; });
    const clipH = ROW_BOTTOMS[rows] - CROP.teach[1];
    // zoom onto the first row's wrong answer on bar 16 beat 2 (same frame shape, 2x closer)
    const zf = F(16, 2), zp = ease((f - zf) / 9);
    const full = CROP.teach;
    const crop = zp > 0 ? lerpCrop(full, zoomCrop(full, 1100, 853, 1.6), zp) : full;
    screen('teach-questions', crop, LAY.media, { scale: push(f, f >= zf ? zf : F(15)) * pulse(f), clipH: zp > 0 ? crop[3] : clipH, fx: 0,
      dy: f - F(15) < 10 ? (1 - easeBack((f - F(15)) / 9)) * 70 : 0 });
    textBlock(f, [{ t: 'For teachers', f: F(15, 0), kind: 'label' }, { t: 'See what the class gets wrong.', f: F(15, 0), stagger: E, swash: true }, { t: 'Down to the wrong answer they chose.', f: F(16, 0), kind: 'sub' }]);
  }
  function sRecap(f) {
    const b = Math.min(3, Math.floor((f - F(17)) / TL.BEAT));
    const shots = [['fc-after-02', CROP.cards, true], ['maths-s1-a2', CROP.maths], ['es-p6-ok', CROP.es], ['wd-result', CROP.wdR]];
    paper();
    const [img, crop, phone] = shots[b];
    const box = { x: W * 0.08, y: H * 0.08, w: W * 0.84, h: H * 0.84 };
    screen(img, crop, box, { scale: push(f, F(17, b)) * (1 + 0.04 * (f - F(17, b)) / TL.BEAT), phone: !!phone });
    flash(f, F(17, b), 4);
  }
  function sStop(f) {
    paper();
    const big = AR === '16x9' ? 96 : AR === '1x1' ? 80 : 88;
    if (f < F(18, 2)) {
      word('Everything you’re studying.', W / 2, H / 2 - big * 0.55, big, f, F(18, 0), { align: 'center', font: `600 ${big}px "Source Serif 4"` });
      word('Nothing you’re not.', W / 2, H / 2 + big * 0.75, big, f, F(18, 1), { align: 'center', font: `600 ${big}px "Source Serif 4"`, color: RUST });
    } else endCard(f);
  }
  function endCard(f) {
    paper();
    const size = AR === '16x9' ? 190 : AR === '1x1' ? 160 : 170;
    const cy = AR === '9x16' ? H * 0.44 : H * 0.44;
    wordmark(W / 2, cy, size, f, F(18, 2));
    flash(f, F(18, 2), 7);
    word('www.studyvault.co.uk', W / 2, cy + size * 0.95, AR === '16x9' ? 54 : 46, f, F(19, 0), { align: 'center', font: `600 ${AR === '16x9' ? 54 : 46}px Inter`, color: INK });
    const sub = AR === '16x9' ? 'Free GCSE revision. Every major exam board. No ads.' : 'Free GCSE revision. No ads.';
    word(sub, W / 2, cy + size * 0.95 + 80, AR === '16x9' ? 40 : 38, f, F(19, 2), { align: 'center', font: `italic 500 ${AR === '16x9' ? 40 : 38}px "Source Serif 4"`, color: MUTED, noPop: true });
  }

  function draw(f) {
    g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, W, H);
    const s = TL.SECTIONS.find(s => f >= s.f0 && f < s.f1) || TL.SECTIONS[TL.SECTIONS.length - 1];
    ({ intro: sIntro, boards: sBoards, drop: sDrop, lesson: sLesson, cards: sCards, maths: sPractice, spanish: sPractice, english: sPractice,
      ai: sAI, widget: sWidget, teacher: sTeacher, recap: sRecap, stop: sStop, end: endCard })[s.id](f);
    if (DEBUG) debug(f, s);
  }
  function debug(f, s) {
    const bar = Math.floor(f / TL.BAR), beat = Math.floor((f % TL.BAR) / TL.BEAT), sub = (f % TL.BEAT) / TL.BEAT;
    g.save(); g.fillStyle = 'rgba(0,0,0,0.75)'; g.fillRect(0, H - 90, W, 90);
    g.font = '600 34px Inter'; g.fillStyle = '#fff';
    g.fillText(`f ${f}   bar ${bar} beat ${beat}   ${s.id}   t ${(f / TL.FPS).toFixed(2)}s`, 30, H - 35);
    for (let b = 0; b < 4; b++) { g.fillStyle = b === beat ? (f % TL.BEAT === 0 ? '#ff3b30' : RUST) : '#555'; g.fillRect(W - 300 + b * 70, H - 70, 56, 50); }
    const cues = TL.CUES.filter(c => c.f === f).map(c => c.type); if (cues.length) { g.fillStyle = '#7CFC00'; g.fillText('CUE ' + cues.join(' '), W / 2, H - 35); }
    if (f % TL.BEAT === 0) { g.strokeStyle = '#ff3b30'; g.lineWidth = 12; g.strokeRect(6, 6, W - 12, H - 12); }
    g.restore();
  }
  window.renderFrame = f => { draw(f); };
})();
