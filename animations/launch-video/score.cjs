/* score.cjs — the launch video's music, synthesised from timeline.js (no samples, licence-clean).
   A minor, Am–F–C–G one chord a bar, 128.571 BPM (14 frames a beat at 30 fps).
   Every drum hit, stab, riser and sound effect is placed on a grid frame, so it lands on the same
   frame as the cut or the pop it belongs to.   node score.cjs  ->  out/score.wav (48 kHz stereo, float) */
const fs = require('fs'), path = require('path');
const TL = require('./timeline.js');
const SR = 48000, LEN = TL.FRAMES / TL.FPS;
const N = Math.ceil(LEN * SR);
const L = new Float32Array(N), R = new Float32Array(N);
const at = f => Math.round(f / TL.FPS * SR);             // frame -> sample
const beatS = TL.BEAT / TL.FPS;                            // seconds per beat
const mtof = m => 440 * Math.pow(2, (m - 69) / 12);
let seed = 12345; const rnd = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff) * 2 - 1;

function add(i0, buf, gain, pan) {                          // mix a mono buffer in, equal-power pan
  const gl = Math.cos((pan + 1) * Math.PI / 4) * gain, gr = Math.sin((pan + 1) * Math.PI / 4) * gain;
  for (let i = 0; i < buf.length; i++) { const j = i0 + i; if (j >= 0 && j < N) { L[j] += buf[i] * gl; R[j] += buf[i] * gr; } }
}
function lp(buf, cut) { const a = 1 - Math.exp(-2 * Math.PI * cut / SR); let y = 0; for (let i = 0; i < buf.length; i++) { y += a * (buf[i] - y); buf[i] = y; } return buf; }
function hp(buf, cut) { const a = 1 - Math.exp(-2 * Math.PI * cut / SR); let y = 0; for (let i = 0; i < buf.length; i++) { y += a * (buf[i] - y); buf[i] = buf[i] - y; } return buf; }
function bp(buf, fc, q) {                                   // state-variable bandpass, fc may be a function of i
  let low = 0, band = 0; for (let i = 0; i < buf.length; i++) { const c = typeof fc === 'function' ? fc(i) : fc;
    const f = 2 * Math.sin(Math.PI * Math.min(c, SR / 6) / SR); const high = buf[i] - low - band / q; band += f * high; low += f * band; buf[i] = band; } return buf; }

/* ---------- instruments ---------- */
function kick(g = 1) { const n = Math.round(0.42 * SR), b = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) { const t = i / SR; const f = 45 + 110 * Math.exp(-t * 32); ph += 2 * Math.PI * f / SR;
    b[i] = Math.sin(ph) * Math.exp(-t * 7.5) + (i < 90 ? rnd() * 0.35 * (1 - i / 90) : 0); } return [b, 0.95 * g]; }
function clap(g = 1) { const n = Math.round(0.28 * SR), b = new Float32Array(n);
  for (let i = 0; i < n; i++) { const t = i / SR; let e = Math.exp(-t * 22); [0, 0.011, 0.022].forEach(o => { if (t >= o && t < o + 0.01) e = Math.max(e, 1 - (t - o) / 0.01); }); b[i] = rnd() * e; }
  bp(b, 1400, 1.2); return [b, 0.62 * g]; }
function snare(g = 1) { const n = Math.round(0.16 * SR), b = new Float32Array(n);
  for (let i = 0; i < n; i++) { const t = i / SR; b[i] = rnd() * Math.exp(-t * 26) * 0.8 + Math.sin(2 * Math.PI * 190 * t) * Math.exp(-t * 30) * 0.5; }
  hp(b, 300); return [b, 0.5 * g]; }
function hat(open, g = 1) { const n = Math.round((open ? 0.2 : 0.045) * SR), b = new Float32Array(n);
  for (let i = 0; i < n; i++) b[i] = rnd() * Math.exp(-i / SR * (open ? 14 : 70)); hp(b, 7000); hp(b, 7000); return [b, (open ? 0.2 : 0.16) * g]; }
function saw(ph) { return 2 * (ph - Math.floor(ph + 0.5)); }
function bassNote(m, dur, g = 1) { const n = Math.round(dur * SR), b = new Float32Array(n); const f = mtof(m); let p1 = 0, p2 = 0;
  for (let i = 0; i < n; i++) { const t = i / SR; p1 += f / SR; p2 += f * 1.004 / SR;
    const env = Math.min(1, t / 0.004) * Math.exp(-t * 5.5); b[i] = (saw(p1) * 0.6 + saw(p2) * 0.4 + Math.sin(2 * Math.PI * p1) * 0.7) * env; }
  lp(b, 520); lp(b, 900); return [b, 0.42 * g]; }
function chord(notes, dur, cut, g = 1, attack = 0.005, rel = 6) { const n = Math.round(dur * SR), b = new Float32Array(n);
  const ph = []; notes.forEach(m => [-0.11, 0, 0.09].forEach(d => ph.push({ f: mtof(m + d), p: (rnd() + 1) / 2 })));
  for (let i = 0; i < n; i++) { const t = i / SR; const env = Math.min(1, t / attack) * Math.exp(-t * rel); let s = 0;
    ph.forEach(o => { o.p += o.f / SR; s += saw(o.p); }); b[i] = s / ph.length * env; }
  lp(b, typeof cut === 'number' ? cut : 2400); lp(b, 3800); return [b, 0.55 * g]; }
function pad(notes, dur, cutFrom, cutTo, g = 1) { const n = Math.round(dur * SR), b = new Float32Array(n);
  const ph = []; notes.forEach(m => [-0.08, 0.07].forEach(d => ph.push({ f: mtof(m + d), p: (rnd() + 1) / 2 })));
  for (let i = 0; i < n; i++) { const t = i / SR; const env = Math.min(1, t / 0.25) * Math.min(1, (dur - t) / 0.35); let s = 0;
    ph.forEach(o => { o.p += o.f / SR; s += saw(o.p); }); b[i] = s / ph.length * Math.max(0, env); }
  // swept lowpass
  let y = 0; for (let i = 0; i < n; i++) { const c = cutFrom + (cutTo - cutFrom) * i / n; const a = 1 - Math.exp(-2 * Math.PI * c / SR); y += a * (b[i] - y); b[i] = y; }
  return [b, 0.45 * g]; }
function pluck(m, g = 1) { const n = Math.round(0.22 * SR), b = new Float32Array(n); const f = mtof(m); let p = 0;
  for (let i = 0; i < n; i++) { const t = i / SR; p += f / SR; const sq = (p % 1) < 0.5 ? 1 : -1; b[i] = (sq * 0.5 + Math.sin(2 * Math.PI * p) * 0.5) * Math.exp(-t * 16); }
  lp(b, 3200); return [b, 0.2 * g]; }
function riser(len) { const n = Math.round(len * SR), b = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) { const x = i / n; ph += 2 * Math.PI * (180 + 1800 * x * x) / SR; b[i] = rnd() * 0.7 + Math.sin(ph) * 0.25; }
  bp(b, i => 300 + 7000 * Math.pow(i / n, 2), 3); for (let i = 0; i < n; i++) b[i] *= Math.pow(i / n, 2.2); return [b, 0.55]; }
function impact(small) { const n = Math.round((small ? 0.9 : 1.8) * SR), b = new Float32Array(n), c = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) { const t = i / SR; ph += 2 * Math.PI * (32 + 60 * Math.exp(-t * 9)) / SR; b[i] = Math.sin(ph) * Math.exp(-t * (small ? 4.5 : 2.4)); c[i] = rnd() * Math.exp(-t * (small ? 6 : 3)); }
  lp(c, 5000); hp(c, 900); for (let i = 0; i < n; i++) b[i] = b[i] * 0.9 + c[i] * 0.35; return [b, small ? 0.55 : 0.8]; }
function whoosh() { const n = Math.round(0.34 * SR), b = new Float32Array(n); const peak = 5 / TL.FPS;
  for (let i = 0; i < n; i++) { const t = i / SR; b[i] = rnd() * (t < peak ? Math.pow(t / peak, 2) : Math.exp(-(t - peak) * 14)); }
  bp(b, i => 500 + 5000 * Math.min(1, i / (peak * SR)), 1.6); return [b, 0.32]; }
function blip(f1, f2, dur, g) { const n = Math.round(dur * SR), b = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) { const t = i / SR; ph += 2 * Math.PI * (f1 + (f2 - f1) * t / dur) / SR; b[i] = Math.sin(ph) * Math.exp(-t * 28) * Math.min(1, t / 0.002); } return [b, g]; }
function tickSfx() { const a = blip(1318.5, 1318.5, 0.12, 0.2)[0], c = blip(1975.5, 1975.5, 0.2, 0.2)[0]; const off = Math.round(0.055 * SR);
  const b = new Float32Array(off + c.length); a.forEach((v, i) => b[i] += v); c.forEach((v, i) => b[i + off] += v); return [b, 0.36]; }
function keySfx() { const n = Math.round(0.025 * SR), b = new Float32Array(n); for (let i = 0; i < n; i++) b[i] = rnd() * Math.exp(-i / SR * 260); bp(b, 3500, 2); return [b, 0.3]; }

/* ---------- arrangement ---------- */
const PROG = [[57, 60, 64], [53, 57, 60], [55, 60, 64], [55, 59, 62]];   // Am F C G
const ROOT = [45, 41, 48, 43];
const place = (f, inst, pan = 0) => add(at(f), inst[0], inst[1], pan);
const secOf = bar => TL.SECTIONS.find(s => bar >= s.bar && bar < s.bar + s.bars).id;

for (let bar = 0; bar < TL.BARS; bar++) {
  const id = secOf(bar), c = PROG[bar % 4], root = ROOT[bar % 4], f0 = TL.F(bar);
  const full = !['intro', 'boards', 'stop', 'end'].includes(id);
  const drop = id === 'drop' || id === 'recap';
  if (id === 'stop') {                                                  // two beats of nothing, then the hit
    place(TL.F(bar, 2), kick(1.2)); place(TL.F(bar, 2), clap(1.1));
    place(TL.F(bar, 2), pad([45, 57, 60, 64, 69], 2 * beatS + 0.2, 1800, 900, 1.1));
    place(TL.F(bar, 2), chord([57, 60, 64, 69], 1.2, 3000, 1.1, 0.003, 2.2), 0);
    place(TL.F(bar, 2), bassNote(33, 1.4, 1.3)); place(TL.F(bar, 2), hat(true, 1.4), 0.3);
    continue;
  }
  if (id === 'end') {                                                   // ring out: soft pad, a slow pluck, a last kick
    const endC = bar === 19 ? [53, 57, 60, 65] : [55, 60, 64, 67];
    place(f0, pad(endC, 4 * beatS + 0.1, 1400, 700, 0.8));
    place(f0, bassNote(bar === 19 ? 41 : 48, 1.6, 0.7));
    for (let e = 0; e < 8; e += 2) place(f0 + e * TL.EIGHTH, pluck(endC[(e / 2) % 4] + 12, 0.6), e % 4 ? 0.35 : -0.35);
    if (bar === 19) place(f0, kick(0.7));
    continue;
  }
  // drums
  for (let b = 0; b < 4; b++) {
    const fb = TL.F(bar, b);
    const kickOn = id === 'intro' ? true : id === 'boards' ? b < 3 : id === 'recap' ? b < 4 : true;
    if (kickOn) place(fb, kick(id === 'intro' ? 0.8 : 1));
    if (full && (b === 1 || b === 3)) place(fb, clap(drop ? 1.1 : 1));
    place(fb + TL.EIGHTH, hat(full, full ? 1 : 0.8), 0.25);           // offbeat hat (open in the groove)
    if (full) { place(fb, hat(false, 0.7), -0.2); place(fb + 3.5, hat(false, 0.5), -0.2); place(fb + 10.5, hat(false, 0.5), -0.2); }
  }
  // snare roll into the drop / into the stop
  if (id === 'boards' || id === 'recap') {
    for (let s = 0; s < 16; s++) { if (s < 8 && s % 2) continue; const fr = f0 + s * 3.5; place(fr, snare(0.35 + 0.65 * s / 15), 0.1); }
  }
  // bass: pumping eighths from the build on
  if (id !== 'intro') for (let e = 0; e < 8; e++) {
    const m = root + (e % 2 ? 12 : 0); place(f0 + e * TL.EIGHTH, bassNote(m - 12, TL.EIGHTH / TL.FPS * 0.95, e % 2 ? 0.8 : 1));
  }
  // harmony
  if (id === 'intro') place(f0, pad(c, 4 * beatS + 0.05, 350, 1600, 0.9));
  else if (id === 'boards') place(f0, pad(c, 4 * beatS + 0.05, 900, 4200, 0.8));
  else for (let b = 0; b < 4; b++) place(TL.F(bar, b) + TL.EIGHTH, chord(c.map(m => m + 12), 0.2, drop ? 3600 : 2600, drop ? 1 : 0.8), b % 2 ? 0.3 : -0.3);
  // lead arp (sixteenths) in the drop, the practice run and the recap
  if (drop || ['maths', 'spanish', 'english', 'widget'].includes(id)) {
    const arp = [c[0] + 12, c[1] + 12, c[2] + 12, c[1] + 24];
    for (let s = 0; s < 16; s++) place(f0 + s * 3.5, pluck(arp[s % 4] + (s % 8 >= 4 ? 12 : 0), drop ? 1 : 0.7), (s % 2 ? 0.4 : -0.4));
  }
}
// sidechain: duck everything but the kick under each kick (approximate: gain envelope on the mix before kicks are added is complex; duck the mix after the fact, lightly)
// sound effects from the cue sheet
TL.CUES.forEach(c => {
  if (c.type === 'riser') place(c.f, riser(c.len / TL.FPS));
  if (c.type === 'impact') place(c.f, impact(c.small));
  if (c.type === 'whoosh') place(c.f, whoosh(), 0);
  if (c.type === 'tick') place(c.f, tickSfx(), 0.1);
  if (c.type === 'pop') place(c.f, blip(1046.5, 1568, 0.07, 0.24), -0.1);
  if (c.type === 'click') place(c.f, blip(2600, 2200, 0.03, 0.14), 0);
  if (c.type === 'key') place(c.f, keySfx(), 0.15);
  if (c.type === 'hit') place(c.f, impact(false));
});
// the stop: hard silence from bar 18 beat 0 to beat 2 (tails cut with a 3 ms fade)
{ const a = at(TL.F(18, 0)), b = at(TL.F(18, 2)), fade = Math.round(0.003 * SR);
  for (let i = a - fade; i < b; i++) { const g = i < a ? (a - i) / fade : 0; L[i] *= g; R[i] *= g; } }
// fade the last 0.6 s
{ const n = Math.round(0.6 * SR); for (let i = N - n; i < N; i++) { const g = (N - i) / n; L[i] *= g; R[i] *= g; } }
// master: soft clip, normalise to -1 dBFS peak (loudness is set by ffmpeg loudnorm at mux)
let peak = 0; for (let i = 0; i < N; i++) { L[i] = Math.tanh(L[i] * 1.1); R[i] = Math.tanh(R[i] * 1.1); peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i])); }
const norm = Math.pow(10, -1 / 20) / peak;
const out = Buffer.alloc(44 + N * 8);
out.write('RIFF', 0); out.writeUInt32LE(36 + N * 8, 4); out.write('WAVE', 8); out.write('fmt ', 12); out.writeUInt32LE(16, 16);
out.writeUInt16LE(3, 20); out.writeUInt16LE(2, 22); out.writeUInt32LE(SR, 24); out.writeUInt32LE(SR * 8, 28); out.writeUInt16LE(8, 32); out.writeUInt16LE(32, 34);
out.write('data', 36); out.writeUInt32LE(N * 8, 40);
for (let i = 0; i < N; i++) { out.writeFloatLE(L[i] * norm, 44 + i * 8); out.writeFloatLE(R[i] * norm, 48 + i * 8); }
fs.mkdirSync(path.join(__dirname, 'out'), { recursive: true });
fs.writeFileSync(path.join(__dirname, 'out', 'score.wav'), out);
console.log(`score: ${LEN.toFixed(2)} s, ${TL.BPM.toFixed(3)} BPM, peak before norm ${peak.toFixed(3)}, cues ${TL.CUES.length}`);
