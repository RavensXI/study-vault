const { ask, noul, score, configured } = require('../_lib/jev');

/**
 * Typed-recall flashcards: the student types what they remember and Jev judges it
 * against the card's own answer. Nothing is generated; the model answer on the card
 * is the only thing shown back. Card kinds and what "right" means for each:
 *
 *   recall     the card's question; right = same fact as the answer, any wording
 *   term       a term shown, the student types its meaning; right = the meaning
 *   definition a meaning shown, the student names the term; right = the term (or its
 *              exact synonym); spelling is forgiven
 *   cloze      a lesson sentence with a gap; right = the missing words or an equivalent
 *   list       "name the four ..."; each item judged on its own, so the card can say
 *              which ones were hit
 *
 * POST { kind, front, answer, typed, items? }   ->  { verdict, p, completeness, items? }
 *   verdict: right | partly | wrong    (right when p >= 0.85, or p >= 0.7 and completeness >= 1.5;
 *            partly when p >= 0.45 or completeness >= 0.9; else wrong)
 */
const RECENT = new Map();            // ip -> [timestamps] ; a soft per-IP cap, like ai-mark
const WINDOW_MS = 60 * 1000, MAX_PER_WINDOW = 60;
function limited(ip) {
  const now = Date.now(); const arr = (RECENT.get(ip) || []).filter(t => now - t < WINDOW_MS);
  arr.push(now); RECENT.set(ip, arr);
  if (RECENT.size > 5000) RECENT.clear();
  return arr.length > MAX_PER_WINDOW;
}
function clean(s, max) { return String(s == null ? '' : s).replace(/\s+/g, ' ').trim().slice(0, max); }

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  const origin = req.headers.origin || '';
  const okOrigin = /^https:\/\/(www\.)?studyvault\.co\.uk$/.test(origin) || /^https:\/\/[a-z0-9-]+\.vercel\.app$/.test(origin) || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin) || !origin;
  if (!okOrigin) return res.status(403).json({ error: 'Forbidden' });
  if (!configured()) return res.status(503).json({ error: 'Judge not configured', fallback: true });
  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || req.socket?.remoteAddress || '?';
  if (limited(ip)) return res.status(429).json({ error: 'Slow down a little', fallback: true });

  const b = req.body || {};
  const kind = ['recall', 'term', 'definition', 'cloze', 'list', 'explain'].includes(b.kind) ? b.kind : 'recall';
  const front = clean(b.front, 600), answer = clean(b.answer, 800), typed = clean(b.typed, 600);
  const items = Array.isArray(b.items) ? b.items.map(x => clean(x, 160)).filter(Boolean).slice(0, 10) : [];
  if (!front || !answer || !typed) return res.status(400).json({ error: 'front, answer and typed are required' });

  const state = { flashcard_kind: kind, flashcard_front: front, model_answer: answer, student_typed_recall: typed };
  const questions = {};
  if (kind === 'list' && items.length) {
    items.forEach((it, i) => { questions['item' + i] = noul('The student\'s recall includes this item (its own words, misspellings and a partial name are fine): ' + it); });
    questions.extra_wrong = noul('The student\'s recall includes something that is not on the list and is wrong');
  } else {
    const rule = kind === 'definition'
      ? 'The student has named the term the meaning describes, or an exact synonym of it; misspellings are fine, a different term is not'
      : kind === 'term'
        ? 'The student\'s recall gives the meaning of the term as the model answer does, in any wording; a vaguer but correct meaning still counts'
        : kind === 'cloze'
          ? 'The student\'s recall supplies the missing words of the sentence or an equivalent (a synonym, a different form of the number); a different fact does not'
          : kind === 'explain'
            ? 'The student\'s explanation gives the same cause or mechanism as the model answer, in their own words; a shorter explanation that names the key link still counts, a description without the why or how does not'
            : 'The student\'s typed recall gives the same fact as the model answer; different wording, spelling mistakes and missing minor words are fine';
    questions.correct = noul(rule);
    questions.completeness = score('How much of the model answer the student\'s recall covers', ['none of it', 'part of it', 'all of it']);
  }

  try {
    const r = await ask({ state, questions });
    const a = r.answers || {};
    let out;
    if (kind === 'list' && items.length) {
      const hit = items.map((it, i) => ({ item: it, p: a['item' + i] ? a['item' + i].noul : 0 }));
      const n = hit.filter(h => h.p >= 0.6).length;
      const extra = a.extra_wrong ? a.extra_wrong.noul : 0;
      out = { kind, items: hit, hits: n, of: items.length, extra_wrong: extra,
              completeness: items.length ? 2 * n / items.length : 0,
              verdict: n === items.length ? 'right' : (n > 0 ? 'partly' : 'wrong') };
    } else {
      const p = a.correct ? a.correct.noul : 0, c = a.completeness ? a.completeness.score : 0;
      // right when the judge is sure the key fact or link is there (a short answer in the
      // student's own words is still right), or fairly sure and the answer is complete
      const verdict = (p >= 0.85 || (p >= 0.7 && c >= 1.5)) ? 'right' : ((p >= 0.45 || c >= 0.9) ? 'partly' : 'wrong');
      out = { kind, p: p, completeness: c, verdict: verdict };
    }
    out.usage = r.usage ? r.usage.input_tokens : undefined;
    return res.status(200).json(out);
  } catch (e) {
    return res.status(502).json({ error: 'Could not judge that one', fallback: true, detail: String(e.message || e).slice(0, 200) });
  }
};
