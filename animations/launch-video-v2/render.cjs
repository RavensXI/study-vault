/* render.cjs — frame-exact render of comp.html (NODE_PATH = global npm root).
   node render.cjs students|teachers 16x9|9x16|1x1 [--debug] [--from N --to M]  -> out/<video>-<ar>.mp4 --dept=<dept> (with out/score-<dept>-<video>.wav)
   node render.cjs students 16x9 --still <frame> --png out.png                   -> one PNG
   Frames come from canvas.toDataURL (PNG for stills, JPEG q .96 for video) piped into ffmpeg; the score is
   levelled to about -14 LUFS with one measured gain; limiting at 4x oversampling keeps the true peak under -1 dBFS after AAC. */
const http = require('http'), fs = require('fs'), path = require('path'), { spawn, execSync } = require('child_process');
const { chromium } = require('playwright');
const TL = require('./timeline.js');
const video = process.argv[2] || 'students', ar = process.argv[3] || '16x9', debug = process.argv.includes('--debug');
const dept = (process.argv.find(a => a.startsWith('--dept=')) || '--dept=general').slice(7);
const FR = TL.VIDEOS[video].frames;
const argv = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const still = argv('--still'), png = argv('--png');
const from = +(argv('--from') || 0), to = argv('--to') != null ? +argv('--to') : FR - 1;
const SIZE = { '16x9': [1920, 1080], '1x1': [1080, 1080], '9x16': [1080, 1920] }[ar];
const ROOT = __dirname, PORT = 8960 + ['16x9', '1x1', '9x16'].indexOf(ar) * 2 + (video === 'teachers' ? 1 : 0) + (still ? 10 : 0) + (process.pid % 20) * 20;
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.json': 'application/json' };
const srv = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, d) => { if (e) { r.statusCode = 404; return r.end(); } r.setHeader('Content-Type', TYPES[path.extname(p)] || 'application/octet-stream'); r.end(d); }); });
(async () => {
  await new Promise(res => srv.listen(PORT, '127.0.0.1', res));
  fs.mkdirSync(path.join(ROOT, 'out'), { recursive: true });
  const b = await chromium.launch({ channel: 'chrome', args: ['--disable-gpu'] });
  const p = await b.newPage({ viewport: { width: SIZE[0], height: SIZE[1] } });
  p.on('pageerror', e => console.log('pageerror', String(e)));
  const scene = `&video=${video}&dept=${dept}`;
  await p.goto(`http://127.0.0.1:${PORT}/comp.html?ar=${ar}${debug ? '&debug=1' : ''}${scene}`);
  await p.waitForFunction(() => window.READY === true, null, { timeout: 120000 });
  if (still) {
    const f = +still;
    const data = await p.evaluate(f => { window.renderFrame(f); return document.getElementById('c').toDataURL('image/png'); }, f);
    fs.writeFileSync(png || path.join(ROOT, 'out', `still-${dept}-${video}-${ar}-${still}.png`), Buffer.from(data.split(',')[1], 'base64'));
    console.log('wrote', png); await b.close(); srv.close(); return;
  }
  const wav = path.join(ROOT, 'out', `score-${dept}-${video}.wav`);
  const meas = execSync(`ffmpeg -hide_banner -nostats -i "${wav}" -af ebur128 -f null - 2>&1`).toString();
  const I = +meas.match(/I:\s+(-?[\d.]+) LUFS/g).pop().match(/-?[\d.]+/)[0];
  const gain = (-12.2 - I).toFixed(2);   // the limiter takes back ~1.7 dB, landing near -14 LUFS
  const name = `${dept}-${video}-${ar}${debug ? '-debug' : ''}${from || to !== FR - 1 ? `-${from}-${to}` : ''}.mp4`;
  const out = path.join(ROOT, 'out', name);
  const ss = (from / TL.FPS).toFixed(4), dur = ((to - from + 1) / TL.FPS).toFixed(4);
  const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(TL.FPS), '-c:v', 'mjpeg', '-i', '-',
    '-ss', ss, '-t', dur, '-i', wav, '-af', `volume=${gain}dB,alimiter=limit=0.8:attack=1:release=50:level=disabled,aresample=192000,alimiter=limit=0.81:attack=0.5:release=40:level=disabled,aresample=48000`,
    '-c:v', 'libx264', '-preset', debug ? 'veryfast' : 'slow', '-crf', debug ? '24' : '16', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', String(TL.FPS),
    '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', '-shortest', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = from; f <= to; f++) {
    const data = await p.evaluate(f => { window.renderFrame(f); return document.getElementById('c').toDataURL('image/jpeg', 0.96); }, f);
    const buf = Buffer.from(data.slice(data.indexOf(',') + 1), 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 100 === 0) console.log(`${ar} frame ${f}/${to} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  await b.close(); srv.close();
  console.log(`wrote ${out} (${(fs.statSync(out).size / 1e6).toFixed(1)} MB, gain ${gain} dB from I=${I})`);
})();
