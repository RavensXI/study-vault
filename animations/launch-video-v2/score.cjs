/* score.cjs — the launch videos' music, synthesised from timeline.js (no samples, licence-clean).
   112.5 BPM (16 frames a beat at 30 fps), C major, C–Am–F–G one chord a bar. House-style pump: the music
   bus is side-chained to the kick; bass on the offbeats. Each bar's arrangement comes from its kind in the
   timeline (intro, drop, groove, build, break, stop, end); every sound effect comes from a scene cue, so it
   lands on the frame of the thing it belongs to.   node score.cjs students|teachers -> out/score-<video>.wav */
const fs = require('fs'), path = require('path');
const TL = require('./timeline.js');
const VIDEO = process.argv[2] || 'students', V = TL.VIDEOS[VIDEO];
const SR = 48000, LEN = V.frames / TL.FPS, N = Math.ceil(LEN * SR);
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
const PROG = ['C', 'Am', 'F', 'G'];
const B = TL.BEAT, BAR = TL.BAR;
const kicks = [];
const bars = [];
V.scenes.forEach(s => s.kinds.forEach((k, i) => bars.push({ kind: k, scene: s, i })));
bars.forEach((bb, bar) => {
  const f0 = bar * BAR, kind = bb.kind, c = kind === 'intro' ? 'G' : PROG[(bar + 399) % 4];
  if (kind === 'intro') { place(MU, f0, pad(CH.G.map(m => m - 12), BAR / TL.FPS + 0.02, 260, 2400, 1.1)); return; }
  if (kind === 'stop') {                                      // one beat of nothing, then the hit on beat 1
    const h = f0 + B; place(DR, h, kick(1.25)); kicks.push(h); place(DR, h, crash(1.1)); place(DR, h, clap(1.0));
    place(MU, h, supersaw(CH.C, 1.1, 3000, 1.1)); place(MU, h, bass(36, 0.9, 1.2)); place(MU, h, pad(CH.C, 3 * beatS + 0.05, 2400, 900, 0.9));
    return;
  }
  if (kind === 'end') {                                       // ring out
    place(MU, f0, pad(CH.F, 4 * beatS, 1600, 700, 0.8)); place(MU, f0, bass(29, 1.4, 0.7));
    [0, 2, 4, 6].forEach((e, j) => place(MU, f0 + e * 8, pluck(CH.F[j % 4] + 12, 0.55, 8), j % 2 ? 0.35 : -0.35));
    place(DR, f0, kick(0.6)); kicks.push(f0);
    return;
  }
  const full = kind !== 'break', drop = kind === 'drop', build = kind === 'build';
  for (let bt = 0; bt < 4; bt++) {
    const fb = f0 + bt * B;
    const kickOn = kind === 'break' ? bt === 0 : !(build && bt >= 2);
    if (kickOn) { place(DR, fb, kick(kind === 'break' ? 0.8 : 1)); kicks.push(fb); }
    if (full && (bt === 1 || bt === 3) && !(build && bt === 3)) place(DR, fb, clap(drop ? 1.05 : 1));
    place(DR, fb + 8, hat(full, full ? 1 : 0.7), 0.25);
    if (full) for (let s = 0; s < 4; s++) if (s !== 2) place(DR, fb + s * 4, hat(false, s === 0 ? 0.8 : 0.55), -0.25);
    if (!(build && bt >= 2)) place(MU, fb + 8, bass(ROOT[c] + (bt === 3 ? 12 : 0), beatS / 2 * 0.95, kind === 'break' ? 0.7 : 1));
  }
  if (drop) place(DR, f0, crash(0.9), 0.1);
  place(MU, f0, supersaw(CH[c], build ? beatS * 2 : beatS * 4, drop ? 2800 : kind === 'break' ? 1300 : 2200, kind === 'break' ? 0.7 : 0.9));
  if (kind !== 'groove' || bb.i % 2 === 1) {
    const a = [CH[c][0] + 12, CH[c][2] + 12, CH[c][1] + 12, CH[c][3] + 12];
    for (let s = 0; s < 16; s++) { if (build && s >= 8) break; place(MU, f0 + s * 4, pluck(a[s % 4] + (s % 8 >= 4 ? 0 : 12), drop ? 0.9 : 0.7), s % 2 ? 0.45 : -0.45); }
  }
  if (build) { for (let s = 0; s < 8; s++) place(DR, f0 + 2 * B + s * 4, snare(0.4 + 0.08 * s), 0.1); place(FX, f0 + 2 * B, riser(2 * beatS + 0.03, 0.9)); }
});

/* ---------- cues: scene key moments -> sounds ---------- */
const SFX = {
  dot: () => pluck(84, 1.1, 9), word: () => pluck(79, 1.0, 11), thud: () => impact(true), unlock: () => unlockClick(),
  swish: () => whoosh(0.3, 0.1), suck: () => suck(0.3), riser1: () => riser(beatS + 0.02, 0.9), hit: () => impact(false),
  pop: () => tone(1046.5, 1568, 0.08, 30, 0.2), click: () => click(1.3), chime: () => chime(), flip: () => whoosh(0.38, 0.2),
  impact: () => impact(false), impact_s: () => impact(true), buzz: () => tone(330, 260, 0.18, 14, 0.22), mail: () => tone(880, 1320, 0.14, 18, 0.22),
  lockclick: () => unlockClick(), count: () => tone(1318.5, 1760, 0.12, 20, 0.16),
};
const MULTI = { board4: [4, 4, 'tick'], blocks4: [4, 8, 'pop'], tiles5: [5, 8, 'pop'], streak3: [3, 8, 'tick'], rows4: [4, 16, 'pop'], typing: [16, 2, 'key'], typing3: [3, 4, 'key'], cells: [14, 3, 'tick'] };
V.scenes.forEach(s => (s.cues || []).forEach(([key, name]) => {
  const f = s.f0 + (typeof key === 'number' ? key : s.keys[key]) * B;
  if (MULTI[name]) { const [n, step, what] = MULTI[name]; for (let i = 0; i < n; i++) {
    const g = what === 'key' ? click(0.5) : what === 'tick' ? tone(1568 + i * 98, 1568 + i * 98, 0.07, 40, 0.13) : tone(1046.5 + i * 60, 1568, 0.07, 30, 0.18);
    place(FX, f + i * step, g, i % 2 ? 0.3 : -0.3); } return; }
  place(FX, f, SFX[name](), 0);
}));
/* a whoosh that peaks on every colour-field transition */
V.scenes.forEach(s => { if (s.enter && ['circle', 'bars', 'field', 'zoom'].includes(s.enter.type) && s.id !== 'end') place(FX, s.f0 - 8, whoosh(0.4, 8 / TL.FPS), 0); });
/* the stop: hard silence for the first beat of the stop bar (4 ms fade), then a soft suck as the field collapses */
V.scenes.forEach(s => s.kinds.forEach((k, i) => { if (k !== 'stop') return; const f = s.f0 + i * BAR, a = at(f), b2 = at(f + B), fade = Math.round(0.004 * SR);
  [DR, MU, FX].forEach(Bu => { for (let j = a - fade; j < b2; j++) { const g = j < a ? (a - j) / fade : 0; Bu[0][j] *= g; Bu[1][j] *= g; } });
  place(FX, f, suck(0.35), 0); }));

/* side-chain pump */
{ const env = new Float32Array(N).fill(1);
  kicks.forEach(f => { const s0 = at(f), rel = Math.round(0.26 * SR); for (let i = 0; i < rel && s0 + i < N; i++) { const x = i / rel; env[s0 + i] = Math.min(env[s0 + i], 0.3 + 0.7 * (1 - Math.pow(1 - x, 2.4))); } });
  for (let i = 0; i < N; i++) { MU[0][i] *= env[i]; MU[1][i] *= env[i]; } }
const L = new Float32Array(N), R = new Float32Array(N), G = { dr: 0.95, mu: 0.6, fx: 0.72 };
for (let i = 0; i < N; i++) { L[i] = DR[0][i] * G.dr + MU[0][i] * G.mu + FX[0][i] * G.fx; R[i] = DR[1][i] * G.dr + MU[1][i] * G.mu + FX[1][i] * G.fx; }
{ const n = Math.round(1.2 * SR); for (let i = N - n; i < N; i++) { const g = Math.pow((N - i) / n, 1.5); L[i] *= g; R[i] *= g; } }
let peak = 0; for (let i = 0; i < N; i++) { L[i] = Math.tanh(L[i] * 1.2); R[i] = Math.tanh(R[i] * 1.2); peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i])); }
const norm = Math.pow(10, -3 / 20) / peak, out = Buffer.alloc(44 + N * 8);
out.write('RIFF', 0); out.writeUInt32LE(36 + N * 8, 4); out.write('WAVE', 8); out.write('fmt ', 12); out.writeUInt32LE(16, 16);
out.writeUInt16LE(3, 20); out.writeUInt16LE(2, 22); out.writeUInt32LE(SR, 24); out.writeUInt32LE(SR * 8, 28); out.writeUInt16LE(8, 32); out.writeUInt16LE(32, 34);
out.write('data', 36); out.writeUInt32LE(N * 8, 40);
for (let i = 0; i < N; i++) { out.writeFloatLE(L[i] * norm, 44 + i * 8); out.writeFloatLE(R[i] * norm, 48 + i * 8); }
fs.mkdirSync(path.join(__dirname, 'out'), { recursive: true });
fs.writeFileSync(path.join(__dirname, 'out', `score-${VIDEO}.wav`), out);
console.log(`score ${VIDEO}: ${LEN.toFixed(2)} s, ${bars.length} bars at ${TL.BPM} BPM, ${kicks.length} kicks`);
