/**
 * Retrieval strength, server-side (13 Sep 2026).
 *
 * A port of the student's own model (js/strength.js) so the teacher screen can
 * say "secure / developing / emerging" per pupil per unit in the same words the
 * pupil sees on their dashboard, and can tell a topic that was learned and has
 * since faded ("going cold") from one that was never learned.
 *
 * Evidence per lesson, all of it attainment and all of it already in the
 * progress blob the class screen reads:
 *   quiz    blob.kc["sub/unit/n"] = {s, t, d}        -> 25 + 75·(s/t), dated d
 *   read    blob.done["sub/unit"] ∋ n, blob.when[key] -> 45, dated when it was read
 *   answer  blob.practice[] = {k, m, r, d}           -> 25 + 75·(mark/marks), dated d
 * Each piece halves over a half-life that grows with the number of retrieval
 * events (7, 14, 28, 56, 112 days; doubled 14 Sep 2026, must match js/strength.js). Strength is the strongest piece after decay.
 *
 * Shorts checks (blob.shortschecks [{d,sub,unit,n,ok}]) are a NUDGE on top of the
 * real evidence, exactly as in js/strength.js: right +5, wrong -8, fading over 14
 * days, the sum kept within -15..+10, and the result kept inside the band the
 * real evidence earned. They never start a topic and never move it up a band.
 *
 * Flashcards are NOT an input here. Their spacing state is on the never-send
 * list (feedback_teacher_data_boundary), so a teacher's view of a pupil can be
 * a little lower than the pupil's own. That is the right way round.
 *
 * Bands match js/strength.js band(): secure 70+, developing 40–69, emerging
 * under 40. The revisit line (55) is where the student's plan brings a lesson
 * back; "dropped" = was secure on the undecayed evidence, now under that line.
 */
const HALF = [7, 14, 28, 56, 112];
const REVISIT_LINE = 55;

function daysSince(iso, now) {
  if (!iso || typeof iso !== 'string') return 999;
  const t = new Date(iso.slice(0, 10) + 'T00:00:00Z').getTime();
  if (isNaN(t)) return 999;
  return Math.max(0, ((now || Date.now()) - t) / 864e5);
}
function decay(v, d, reps) {
  const h = HALF[Math.min(HALF.length - 1, Math.max(0, reps - 1))];
  return v * Math.pow(0.5, d / h);
}
function band(s) { return s >= 70 ? 'g' : s >= 40 ? 'a' : 'r'; }
const SHORT_HALF = 14, SHORT_RIGHT = 5, SHORT_WRONG = -8, SHORT_MIN = -15, SHORT_MAX = 10;
function inBand(s, b) { const lo = b === 'g' ? 70 : b === 'a' ? 40 : 0, hi = b === 'g' ? 100 : b === 'a' ? 69 : 39; return Math.max(lo, Math.min(hi, s)); }
function shortsNudges(shorts, now) {
  const t = {};
  (Array.isArray(shorts) ? shorts : []).forEach(function (r) {
    if (!r || !r.unit || !r.n) return;
    const k = r.unit + '/' + r.n;
    t[k] = (t[k] || 0) + (r.ok ? SHORT_RIGHT : SHORT_WRONG) * Math.pow(0.5, daysSince(r.d, now) / SHORT_HALF);
  });
  Object.keys(t).forEach(function (k) { t[k] = Math.round(Math.max(SHORT_MIN, Math.min(SHORT_MAX, t[k]))); });
  return t;
}
function bandWord(b) { return b === 'g' ? 'secure' : b === 'a' ? 'developing' : b === 'r' ? 'emerging' : 'not yet'; }

/* "Mark: 3/8" or "3 out of 8" from the marker's text */
function markOf(entry) {
  const mm = String(entry && entry.r || '').match(/(\d+)\s*(?:\/|out of)\s*(\d+)/i);
  if (!mm || !+mm[2]) return null;
  return { got: +mm[1], of: +mm[2] };
}

/**
 * Every lesson this pupil has evidence for in the given (already subject-scoped)
 * kc / done / when / practice, as { "unit/n": {s, peak, reps, last, unit, n} }.
 */
function lessons(kc, done, when, practice, now, shorts) {
  const ev = {};   // "unit/n" -> [{v, d, quiz}]
  function add(unit, n, v, d, quiz) {
    if (!unit || !n) return;
    const k = unit + '/' + n;
    (ev[k] = ev[k] || []).push({ v: v, d: d, quiz: !!quiz });
  }
  Object.keys(kc || {}).forEach(function (k) {
    const e = kc[k] || {}; if (typeof e.s !== 'number' || !e.t) return;
    const p = k.split('/'); add(p[1], parseInt(p[2], 10), 25 + 75 * (e.s / e.t), daysSince(e.d, now), true);
  });
  Object.keys(done || {}).forEach(function (k) {
    const unit = k.split('/')[1];
    (done[k] || []).forEach(function (n) {
      const key = k + '/' + n, w = when && when[key];
      add(unit, parseInt(n, 10), 45, w ? daysSince(w, now) : 30);
    });
  });
  (Array.isArray(practice) ? practice : []).forEach(function (e) {
    const m = markOf(e); if (!m) return;
    const p = String(e.k || e.key || '').split('/');
    add(p[1], parseInt(p[2], 10), 25 + 75 * Math.min(1, m.got / m.of), daysSince(e.d, now), true);
  });
  const out = {}, nudges = shortsNudges(shorts, now);
  Object.keys(ev).forEach(function (k) {
    const list = ev[k], reps = list.length;
    let best = 0, peak = 0, last = 999, quiz = false;
    list.forEach(function (e) { best = Math.max(best, decay(e.v, e.d, reps)); peak = Math.max(peak, e.v); last = Math.min(last, e.d); if (e.quiz) quiz = true; });
    const p = k.split('/');
    const base = Math.round(best), nudge = nudges[k] || 0;
    const s = nudge ? inBand(base + nudge, band(base)) : base;
    out[k] = { s: s, peak: Math.round(peak), reps: reps, last: Math.round(last), unit: p[0], n: parseInt(p[1], 10), quiz: quiz };
  });
  return out;
}

/**
 * Per unit for one pupil: { unit: {s, peak, n, q, last, band, drop} }  (q = lessons with a quiz or marked answer; n - q were only read)
 * s = mean current strength over the lessons with evidence; peak = the same
 * mean with no decay (what they once knew); drop = was secure, now under the
 * revisit line — the "going cold" signal.
 */
function units(lessonMap) {
  const by = {};
  Object.keys(lessonMap).forEach(function (k) {
    const l = lessonMap[k];
    if (!by[l.unit]) by[l.unit] = { s: 0, peak: 0, n: 0, q: 0, last: 999 };
    by[l.unit].s += l.s; by[l.unit].peak += l.peak; by[l.unit].n++; if (l.quiz) by[l.unit].q++; by[l.unit].last = Math.min(by[l.unit].last, l.last);
  });
  Object.keys(by).forEach(function (u) {
    const x = by[u];
    x.s = Math.round(x.s / x.n); x.peak = Math.round(x.peak / x.n);
    x.band = band(x.s);
    x.drop = x.peak >= 70 && x.s < REVISIT_LINE;
  });
  return by;
}

module.exports = { lessons, units, band, bandWord, markOf, REVISIT_LINE, daysSince };
