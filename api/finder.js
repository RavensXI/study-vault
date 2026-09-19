const { ask, choice, configured } = require('./_lib/jev');

/**
 * Dashboard finder, the judged fallback: the student typed something the local index could
 * not match by words ("the bit where Scrooge sees his own grave"). Two quick decisions by
 * Jev, both bounded to the student's own subjects, never a generated answer:
 *   1. which unit (or none) the words belong to
 *   2. which lesson in that unit (or none)
 *
 * POST { q, units: [{ k, s, u, lessons: [{ n, t, g }] }] }
 *        k = "subject-slug/unit-slug", s = subject name, u = unit name,
 *        lessons: n number, t title, g a few glossary terms (string)
 *   ->   { unit: k | null, n: number | null, p: confidence }
 */
const RECENT = new Map(); const WINDOW_MS = 60 * 1000, MAX_PER_WINDOW = 30;
function limited(ip) {
  const now = Date.now(); const arr = (RECENT.get(ip) || []).filter(t => now - t < WINDOW_MS);
  arr.push(now); RECENT.set(ip, arr); if (RECENT.size > 5000) RECENT.clear();
  return arr.length > MAX_PER_WINDOW;
}
function clean(s, max) { return String(s == null ? '' : s).replace(/\s+/g, ' ').trim().slice(0, max); }

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  const origin = req.headers.origin || '';
  const okOrigin = /^https:\/\/(www\.)?studyvault\.co\.uk$/.test(origin) || /^https:\/\/[a-z0-9-]+\.vercel\.app$/.test(origin) || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin) || !origin;
  if (!okOrigin) return res.status(403).json({ error: 'Forbidden' });
  if (!configured()) return res.status(503).json({ error: 'Finder not configured', fallback: true });
  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || req.socket?.remoteAddress || '?';
  if (limited(ip)) return res.status(429).json({ error: 'Slow down a little', fallback: true });

  const b = req.body || {};
  const q = clean(b.q, 200);
  const units = (Array.isArray(b.units) ? b.units : []).slice(0, 60).map(u => ({
    k: clean(u.k, 120), s: clean(u.s, 60), u: clean(u.u, 80),
    lessons: (Array.isArray(u.lessons) ? u.lessons : []).slice(0, 40).map(l => ({ n: +l.n || 0, t: clean(l.t, 120), g: clean(l.g, 200) }))
  })).filter(u => u.k && u.lessons.length);
  if (!q || !units.length) return res.status(400).json({ error: 'q and units are required' });

  try {
    // 1. the unit
    const ucrit = { none: 'the words do not belong to any of these units' };
    units.forEach(u => { ucrit[u.k] = u.s + ' — ' + u.u + ': ' + u.lessons.map(l => l.t).join('; ').slice(0, 2000); });
    const r1 = await ask({ state: { student_typed: q, note: 'A GCSE student is looking for the lesson that covers what they typed. They may describe it loosely, misspell it, or use a nickname.' },
                          questions: { unit: choice('Which unit contains the lesson the student is looking for?', ucrit) } });
    const a1 = (r1.answers || {}).unit || {}; const probs = a1.probabilities || {};
    // the likeliest units (up to three) go forward together, so a near miss on the unit does not lose the lesson
    const cands = units.filter(u => (probs[u.k] || (a1.choice === u.k ? a1.confidence : 0) || 0) >= 0.12)
                       .sort((x, y) => (probs[y.k] || 0) - (probs[x.k] || 0)).slice(0, 3);
    if (!cands.length || (a1.choice === 'none' && (probs.none || 0) >= 0.6)) return res.status(200).json({ unit: null, n: null, p: probs.none || 0 });
    // 2. the lesson among those units' lessons
    const lcrit = { none: 'no lesson here covers it' };
    cands.forEach(u => u.lessons.forEach(l => { lcrit[u.k + '#' + l.n] = u.s + ' — ' + u.u + ' — ' + l.t + (l.g ? ' (covers: ' + l.g + ')' : ''); }));
    const r2 = await ask({ state: { student_typed: q, note: 'Pick the one lesson whose content answers or contains what the student typed.' },
                          questions: { lesson: choice('Which lesson covers what the student typed?', lcrit) } });
    const a2 = (r2.answers || {}).lesson || {}; const lk = a2.choice; const p2 = (a2.probabilities || {})[lk] || a2.confidence || 0;
    if (!lk || lk === 'none' || p2 < 0.3) return res.status(200).json({ unit: null, n: null, p: p2 });
    const hash = lk.lastIndexOf('#');
    return res.status(200).json({ unit: lk.slice(0, hash), n: +lk.slice(hash + 1), p: p2 });
  } catch (e) {
    return res.status(502).json({ error: 'Could not look that up', fallback: true, detail: String(e.message || e).slice(0, 200) });
  }
};
