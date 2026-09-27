/* render.cjs — frame-exact render of comp.html to MP4 with the synthesised score.
   node render.cjs 16x9 [--debug] [--from N --to M] [--sheet]   (NODE_PATH = global npm root)
   Frames come from canvas.toDataURL (JPEG q .95) piped straight into ffmpeg; the score is levelled to about -14 LUFS. */
const http = require('http'), fs = require('fs'), path = require('path'), { spawn, execSync } = require('child_process');
const { chromium } = require('playwright');
const TL = require('./timeline.js');
const ar = process.argv[2] || '16x9', debug = process.argv.includes('--debug');
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? +process.argv[i + 1] : null; };
const from = arg('--from') || 0, to = arg('--to') != null ? arg('--to') : TL.FRAMES - 1;
const SIZE = { '16x9': [1920, 1080], '1x1': [1080, 1080], '9x16': [1080, 1920] }[ar];
const ROOT = __dirname, PORT = 8932 + ['16x9', '1x1', '9x16'].indexOf(ar);
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.json': 'application/json' };
const srv = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, d) => { if (e) { r.statusCode = 404; return r.end(); } r.setHeader('Content-Type', TYPES[path.extname(p)] || 'application/octet-stream'); r.end(d); }); });
(async () => {
  await new Promise(res => srv.listen(PORT, '127.0.0.1', res));
  fs.mkdirSync(path.join(ROOT, 'out'), { recursive: true });
  // loudness: one linear gain to ~-14 LUFS integrated (measured, not dynamic)
  const wav = path.join(ROOT, 'out', 'score.wav');
  const meas = execSync(`ffmpeg -hide_banner -nostats -i "${wav}" -af ebur128 -f null - 2>&1`).toString();
  const I = +meas.match(/I:\s+(-?[\d.]+) LUFS/g).pop().match(/-?[\d.]+/)[0];
  const gain = (-14 - I).toFixed(2);
  const name = `launch-${ar}${debug ? '-debug' : ''}${from || to !== TL.FRAMES - 1 ? `-${from}-${to}` : ''}.mp4`;
  const out = path.join(ROOT, 'out', name);
  const b = await chromium.launch({ channel: 'chrome', args: ['--disable-gpu'] });
  const p = await b.newPage({ viewport: { width: SIZE[0], height: SIZE[1] } });
  p.on('pageerror', e => console.log('pageerror', String(e)));
  await p.goto(`http://127.0.0.1:${PORT}/comp.html?ar=${ar}${debug ? '&debug=1' : ''}`);
  await p.waitForFunction(() => window.READY === true, null, { timeout: 120000 });
  const ss = (from / TL.FPS).toFixed(4), dur = ((to - from + 1) / TL.FPS).toFixed(4);
  const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(TL.FPS), '-c:v', 'mjpeg', '-i', '-',
    '-ss', ss, '-t', dur, '-i', wav, '-af', `volume=${gain}dB,alimiter=limit=0.89:attack=1:release=50`,
    '-c:v', 'libx264', '-preset', debug ? 'veryfast' : 'slow', '-crf', debug ? '24' : '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', String(TL.FPS),
    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = from; f <= to; f++) {
    const data = await p.evaluate(f => { window.renderFrame(f); return document.getElementById('c').toDataURL('image/jpeg', 0.95); }, f);
    const buf = Buffer.from(data.slice(data.indexOf(',') + 1), 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 120 === 0) console.log(`${ar} frame ${f}/${to} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  await b.close(); srv.close();
  console.log(`wrote ${out} (${(fs.statSync(out).size / 1e6).toFixed(1)} MB, gain ${gain} dB from I=${I})`);
})();
