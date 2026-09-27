/* score.cjs — the v2 test clip's music, synthesised from timeline.js (no samples, licence-clean).
   112.5 BPM (16 frames a beat at 30 fps), C major, C–Am–F–G. House-style pump: the music bus is
   side-chained to the kick; bass sits on the offbeats. Three buses (drums, music, effects) are mixed
   separately, then a gentle saturation and a peak normalise; render.cjs sets -14 LUFS.
   node score.cjs  ->  out/score.wav (48 kHz stereo float) */
const fs = require('fs'), path = require('path');
const TL = require('./timeline.js'), K = TL.K;
const SR = 48000, LEN = TL.FRAMES / TL.FPS, N = Math.ceil(LEN * SR);
const bus = () => [new Float32Array(N), new Float32Array(N)];
const DR = bus(), MU = bus(), FX = bus();
const at = f => Math.round(f / TL.FPS * SR);
const beatS = TL.BEAT / TL.FPS;
const mtof = m => 440 * Math.pow(2, (m - 69) / 12);
let seed = 2026; const rnd = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff) * 2 - 1;

function add(B, i0, buf, gain, pan = 0) {
  const gl = Math.cos((pan + 1) * Math.PI / 4) * gain, gr = Math.sin((pan + 1) * Math.PI / 4) * gain;
  for (let i = 0; i < buf.length; i++) { const j = i0 + i; if (j >= 0 && j < N) { B[0][j] += buf[i] * gl; B[1][j] += buf[i] * gr; } }
}
const place = (B, f, inst, pan = 0) => add(B, at(f), inst[0], inst[1], pan);
function lp(b, c) { const a = 1 - Math.exp(-2 * Math.PI * c / SR); let y = 0; for (let i = 0; i < b.length; i++) { y += a * (b[i] - y); b[i] = y; } return b; }
function hp(b, c) { const a = 1 - Math.exp(-2 * Math.PI * c / SR); let y = 0; for (let i = 0; i < b.length; i++) { y += a * (b[i] - y); b[i] -= y; } return b; }
function svf(b, fc, q, mode = 'band') { let low = 0, band = 0; for (let i = 0; i < b.length; i++) { const c = typeof fc === 'function' ? fc(i) : fc;
  const f = 2 * Math.sin(Math.PI * Math.min(c, SR / 6) / SR); const high = b[i] - low - band / q; band += f * high; low += f * band; b[i] = mode === 'low' ? low : band; } return b; }
const saw = p => 2 * (p - Math.floor(p + 0.5));

/* ---------- drums ---------- */
function kick(g = 1) { const n = Math.round(0.45 * SR), b = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) { const t = i / SR, f = 48 + 120 * Math.exp(-t * 30); ph += 2 * Math.PI * f / SR;
    b[i] = Math.tanh(Math.sin(ph) * 1.6) * Math.exp(-t * 6.5) + (i < 120 ? rnd() * 0.25 * (1 - i / 120) : 0); } return [b, 0.9 * g]; }
function clap(g = 1) { const n = Math.round(0.3 * SR), b = new Float32Array(n);
  for (let i = 0; i < n; i++) { const t = i / SR; let e = Math.exp(-t * 20); [0, 0.012, 0.024].forEach(o => { if (t >= o && t < o + 0.01) e = Math.max(e, 1 - (t - o) / 0.01); }); b[i] = rnd() * e; }
  svf(b, 1500, 1.3); return [b, 0.7 * g]; }
function hat(open, g = 1) { const n = Math.round((open ? 0.24 : 0.05) * SR), b = new Float32Array(n);
  for (let i = 0; i < n; i++) b[i] = rnd() * Math.exp(-i / SR * (open ? 12 : 65)); hp(b, 7500); hp(b, 7500); return [b, (open ? 0.22 : 0.13) * g]; }
function snare(g = 1) { const n = Math.round(0.15 * SR), b = new Float32Array(n);
  for (let i = 0; i < n; i++) { const t = i / SR; b[i] = rnd() * Math.exp(-t * 28) * 0.8 + Math.sin(2 * Math.PI * 200 * t) * Math.exp(-t * 32) * 0.5; } hp(b, 350); return [b, 0.45 * g]; }
function crash(g = 1) { const n = Math.round(1.6 * SR), b = new Float32Array(n);
  for (let i = 0; i < n; i++) b[i] = rnd() * Math.exp(-i / SR * 2.6); hp(b, 5000); svf(b, 9000, 0.7); return [b, 0.5 * g]; }

/* ---------- music ---------- */
function supersaw(notes, dur, cut, g = 1) { const n = Math.round(dur * SR), b = new Float32Array(n); const osc = [];
  notes.forEach(m => [-0.14, -0.05, 0.05, 0.14].forEach(d => osc.push({ f: mtof(m + d), p: (rnd() + 1) / 2 })));
  for (let i = 0; i < n; i++) { const t = i / SR, env = Math.min(1, t / 0.01) * Math.min(1, (dur - t) / 0.03); let s = 0;
    for (const o of osc) { o.p += o.f / SR; s += saw(o.p); } b[i] = s / osc.length * env; }
  svf(b, typeof cut === 'function' ? cut : () => cut, 0.8, 'low'); return [b, 0.5 * g]; }
function bass(m, dur, g = 1) { const n = Math.round(dur * SR), b = new Float32Array(n), f = mtof(m); let p = 0;
  for (let i = 0; i < n; i++) { const t = i / SR; p += f / SR; const env = Math.min(1, t / 0.004) * Math.exp(-t * 7) * Math.min(1, (dur - t) / 0.01);
    b[i] = (Math.sin(2 * Math.PI * p) * 0.9 + saw(p) * 0.35) * env; } lp(b, 700); return [b, 0.62 * g]; }
function pluck(m, g = 1, dec = 14) { const n = Math.round(0.3 * SR), b = new Float32Array(n), f = mtof(m); let p = 0;
  for (let i = 0; i < n; i++) { const t = i / SR; p += f / SR; b[i] = (((p % 1) < 0.5 ? 1 : -1) * 0.35 + Math.sin(2 * Math.PI * p) * 0.65) * Math.exp(-t * dec); }
  lp(b, 4200); return [b, 0.22 * g]; }
function pad(notes, dur, c0, c1, g = 1) { const n = Math.round(dur * SR), b = new Float32Array(n), osc = [];
  notes.forEach(m => [-0.08, 0.08].forEach(d => osc.push({ f: mtof(m + d), p: (rnd() + 1) / 2 })));
  for (let i = 0; i < n; i++) { const t = i / SR, env = Math.min(1, t / 0.3) * Math.min(1, (dur - t) / 0.08); let s = 0;
    for (const o of osc) { o.p += o.f / SR; s += saw(o.p); } b[i] = s / osc.length * Math.max(0, env); }
  svf(b, i => c0 * Math.pow(c1 / c0, i / n), 0.9, 'low'); return [b, 0.5 * g]; }

/* ---------- effects ---------- */
function tone(f1, f2, dur, dec, g) { const n = Math.round(dur * SR), b = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) { const t = i / SR; ph += 2 * Math.PI * (f1 + (f2 - f1) * t / dur) / SR; b[i] = Math.sin(ph) * Math.exp(-t * dec) * Math.min(1, t / 0.002); } return [b, g]; }
function chime() { const a = tone(1318.5, 1318.5, 0.25, 10, 1)[0], c = tone(1975.5, 1975.5, 0.5, 6, 1)[0], d = tone(2637, 2637, 0.4, 9, 1)[0];
  const o1 = Math.round(0.06 * SR), b = new Float32Array(o1 + c.length); a.forEach((v, i) => b[i] += v * 0.8); c.forEach((v, i) => { b[i + o1] += v; if (i < d.length) b[i + o1] += d[i] * 0.3; }); return [b, 0.3]; }
function click(g = 1) { const n = Math.round(0.03 * SR), b = new Float32Array(n); for (let i = 0; i < n; i++) b[i] = rnd() * Math.exp(-i / SR * 300); svf(b, 3200, 3); return [b, 0.5 * g]; }
function unlockClick() { const a = click(1.3)[0], c = click(1)[0], off = Math.round(0.055 * SR), b = new Float32Array(off + c.length);
  a.forEach((v, i) => b[i] += v); c.forEach((v, i) => b[i + off] += v); const t = tone(900, 700, 0.12, 30, 1)[0]; t.forEach((v, i) => b[i] += v * 0.3); return [b, 0.55]; }
function whoosh(len, peak) { const n = Math.round(len * SR), b = new Float32Array(n), pk = peak * SR;
  for (let i = 0; i < n; i++) b[i] = rnd() * (i < pk ? Math.pow(i / pk, 2.2) : Math.exp(-(i - pk) / SR * 12)); svf(b, i => 400 + 5200 * Math.min(1, i / pk), 1.4); return [b, 0.34]; }
function riser(len, g = 1) { const n = Math.round(len * SR), b = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) { const x = i / n; ph += 2 * Math.PI * (200 + 1600 * x * x) / SR; b[i] = rnd() * 0.7 + Math.sin(ph) * 0.2; }
  svf(b, i => 300 + 7500 * Math.pow(i / n, 2), 2.5); for (let i = 0; i < n; i++) b[i] *= Math.pow(i / n, 2); return [b, 0.5 * g]; }
function impact(small) { const n = Math.round((small ? 0.8 : 1.6) * SR), b = new Float32Array(n), c = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) { const t = i / SR; ph += 2 * Math.PI * (34 + 70 * Math.exp(-t * 10)) / SR; b[i] = Math.sin(ph) * Math.exp(-t * (small ? 5 : 2.6)); c[i] = rnd() * Math.exp(-t * (small ? 8 : 4)); }
  hp(c, 1500); for (let i = 0; i < n; i++) b[i] = b[i] * 0.9 + c[i] * 0.25; return [b, small ? 0.45 : 0.75]; }
function suck(len) { const n = Math.round(len * SR), b = new Float32Array(n); for (let i = 0; i < n; i++) b[i] = rnd() * Math.pow(1 - i / n, 1.5) * Math.min(1, i / (0.02 * SR));
  svf(b, i => 6000 * Math.pow(1 - i / n, 2) + 200, 2); return [b, 0.35]; }

/* ---------- arrangement ---------- */
const CH = { C: [60, 64, 67, 72], Am: [57, 60, 64, 69], F: [53, 57, 60, 65], G: [55, 59, 62, 67] };
const ROOT = { C: 36, Am: 33, F: 29, G: 31 };
const BARS = ['G', 'C', 'Am', 'F', 'G', 'Am'];                    // bar 0 is the intro (dominant into the wipe)
const kicks = [];
for (let bar = 1; bar < 6; bar++) {
  const c = BARS[bar], f0 = TL.F(bar);
  const build = bar === 5;
  for (let bt = 0; bt < 4; bt++) {
    const fb = TL.F(bar, bt);
    if (!(build && bt >= 2)) { place(DR, fb, kick()); kicks.push(fb); }          // the kick drops out for the zoom
    if (bt === 1 || bt === 3) if (!(build && bt === 3)) place(DR, fb, clap());
    place(DR, fb + 8, hat(true), 0.25);
    for (let s = 0; s < 4; s++) if (s !== 2) place(DR, fb + s * 4, hat(false, s === 0 ? 0.8 : 0.55), -0.25);
    // offbeat bass (between the kicks), octave jump on the last offbeat
    if (!(build && bt >= 2)) place(MU, fb + 8, bass(ROOT[c] + (bt === 3 ? 12 : 0), beatS / 2 * 0.95));
  }
  // chords: one bar of supersaw, pumped by the side-chain; the build opens the filter
  place(MU, f0, supersaw(CH[c], build ? beatS * 2 : beatS * 4, build ? 2600 : 2200, 0.9), 0);
  // arp from the card scene on
  if (bar >= 3) { const a = [CH[c][0] + 12, CH[c][2] + 12, CH[c][1] + 12, CH[c][3] + 12];
    for (let s = 0; s < 16; s++) { if (build && s >= 8) break; place(MU, f0 + s * 4, pluck(a[s % 4] + (s % 8 >= 4 ? 0 : 12), 0.8), s % 2 ? 0.45 : -0.45); } }
}
// intro: a pad that opens up, and the first sounds of the dot and the padlock
place(MU, 0, pad(CH.G.map(m => m - 12), TL.SEC(K.wipe) + 0.02, 260, 2400, 1.1), 0);
place(FX, K.dotIn, pluck(84, 1.1, 9), 0);                         // the dot
place(FX, K.lockIn, impact(true), 0);                             // the padlock grows
place(FX, K.unlock, unlockClick(), 0.1);                          // the shackle lifts
place(FX, K.lockOut, riser(TL.SEC(K.wipe - K.lockOut), 0.9), 0);  // one beat of riser into the wipe
// the wipe: the downbeat
place(FX, K.wipe, impact(false), 0); place(DR, K.wipe, crash(1), 0);
// the words, the boards
[[K.w1, 76], [K.w2, 79], [K.w3, 84]].forEach(([f, m]) => place(FX, f, pluck(m, 1.2, 10), 0));
[0, 1, 2, 3].forEach(i => place(FX, K.boards + i * 4, tone(1568 + i * 196, 1568 + i * 196, 0.08, 40, 0.14), i % 2 ? 0.3 : -0.3));
place(FX, K.textOut, whoosh(0.3, 0.12), 0);
place(FX, K.dotMove, tone(520, 880, 0.18, 12, 0.28), 0);
// the card
place(FX, K.cardIn, impact(true), 0); place(FX, K.cardIn, tone(660, 990, 0.1, 30, 0.2), 0);
for (let f = K.typeFrom; f < K.check; f += 4) place(FX, f, click(0.55), 0.15);
place(FX, K.check, click(1.3), 0);
place(FX, K.tick, chime(), 0.05); place(DR, K.tick, crash(0.35), 0.2);
place(FX, K.flip - 7, whoosh(0.4, 7 / TL.FPS), 0);
// the zoom: a snare roll and a riser, then the suck into the dot, then the hit
for (let s = 0; s < 8; s++) place(DR, K.zoom + s * 4, snare(0.4 + 0.08 * s), 0.1);
place(FX, K.zoom, riser(TL.SEC(K.collapse - K.zoom) + 0.05, 1.1), 0);
place(FX, K.collapse, suck(TL.SEC(K.next - K.collapse)), 0);
place(DR, K.next, kick(1.2)); kicks.push(K.next); place(DR, K.next, crash(1.1), 0); place(FX, K.next, impact(false), 0);
place(MU, K.next, supersaw(CH.C, 0.7, 3200, 1.1), 0); place(MU, K.next, bass(36, 0.6, 1.2));

/* side-chain: the music bus ducks under every kick and swells back (the pump) */
{ const env = new Float32Array(N).fill(1);
  kicks.forEach(f => { const s0 = at(f), rel = Math.round(0.26 * SR);
    for (let i = 0; i < rel && s0 + i < N; i++) { const x = i / rel; env[s0 + i] = Math.min(env[s0 + i], 0.28 + 0.72 * (1 - Math.pow(1 - x, 2.4) * (1 - x > 0 ? 1 : 0))); } });
  for (let i = 0; i < N; i++) { MU[0][i] *= env[i]; MU[1][i] *= env[i]; } }

/* mix: drums, music, effects; a gentle glue saturation; a short fade at the very end */
const L = new Float32Array(N), R = new Float32Array(N);
const G = { dr: 0.95, mu: 0.62, fx: 0.7 };
for (let i = 0; i < N; i++) { L[i] = DR[0][i] * G.dr + MU[0][i] * G.mu + FX[0][i] * G.fx; R[i] = DR[1][i] * G.dr + MU[1][i] * G.mu + FX[1][i] * G.fx; }
{ const n = Math.round(0.25 * SR); for (let i = N - n; i < N; i++) { const g = (N - i) / n; L[i] *= g; R[i] *= g; } }
let peak = 0; for (let i = 0; i < N; i++) { L[i] = Math.tanh(L[i] * 1.2) / 1.2 * 1.2; R[i] = Math.tanh(R[i] * 1.2) / 1.2 * 1.2; peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i])); }
const norm = Math.pow(10, -3 / 20) / peak;
const out = Buffer.alloc(44 + N * 8);
out.write('RIFF', 0); out.writeUInt32LE(36 + N * 8, 4); out.write('WAVE', 8); out.write('fmt ', 12); out.writeUInt32LE(16, 16);
out.writeUInt16LE(3, 20); out.writeUInt16LE(2, 22); out.writeUInt32LE(SR, 24); out.writeUInt32LE(SR * 8, 28); out.writeUInt16LE(8, 32); out.writeUInt16LE(32, 34);
out.write('data', 36); out.writeUInt32LE(N * 8, 40);
for (let i = 0; i < N; i++) { out.writeFloatLE(L[i] * norm, 44 + i * 8); out.writeFloatLE(R[i] * norm, 48 + i * 8); }
fs.mkdirSync(path.join(__dirname, 'out'), { recursive: true });
fs.writeFileSync(path.join(__dirname, 'out', 'score.wav'), out);
console.log(`score: ${LEN.toFixed(2)} s at ${TL.BPM} BPM, ${kicks.length} kicks, peak ${peak.toFixed(3)}`);
