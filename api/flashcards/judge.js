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

function norm(s) {
  return String(s || '').toLowerCase().replace(/&[a-z]+;/g, ' ').replace(/[^a-z0-9 ]+/g, ' ').replace(/\b(the|a|an|of|in|on|at|to|and)\b/g, ' ').replace(/\s+/g, ' ').trim();
}
function plainMatch(kind, front, answer, typed) {
  const a = norm(answer), t = norm(typed);
  if (!t) return false;
  if (a === t) return true;
  const years = a.match(/\b(1[0-9]{3}|20[0-9]{2})\b/g) || [];
  if (years.length === 1) {
    const asksDay = /\b(month|day|date|exact|when exactly)\b/i.test(front);
    if (!asksDay && t === years[0]) return true;                                 // the year alone
    if (a.replace(/\b(1[0-9]{3}|20[0-9]{2})\b/g, ' ').replace(/\s+/g, ' ').trim() === t) return true;   // the answer without its year
  }
  const words = String(answer || '').trim().split(/\s+/);
  if (words.length >= 2 && words.length <= 4 && words.every(w => /^[A-Z][a-zA-Z'\-]+$/.test(w)) && t === norm(words[words.length - 1])) return true;   // surname alone
  return false;
}

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

  // Plain matches never need the judge: the same words, the year alone for a date the question
  // does not pin to a day or month, the surname alone for a person, the answer without its year.
  if (kind !== 'list' && plainMatch(kind, front, answer, typed)) {
    return res.status(200).json({ kind, p: 1, completeness: 2, verdict: 'right', plain: true });
  }
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
          ? 'The student\'s recall supplies the missing words of the sentence or an equivalent (a synonym, a different form of the number). When the missing words are a date, the correct year on its own is a full match; when they are a person, the surname on its own is a full match. A different fact does not count'
          : kind === 'explain'
            ? 'The student\'s explanation gives the same cause or mechanism as the model answer, in their own words; a shorter explanation that names the key link still counts, a description without the why or how does not'
            : 'The student\'s typed recall gives the same fact as the model answer; different wording, spelling mistakes and missing minor words are fine. For a date the correct year alone counts unless the question asks for the day or month; for a person the surname alone counts; a figure counts when it is the same to a sensible rounding, and so does a figure that follows from the model answer (the fall from 46% to 15% is a cut of about 30 percentage points). When the model answer gives several reasons or parts, most of them in the student\'s own words counts as the same fact';
    questions.correct = noul(rule);
    questions.completeness = score('How much of the model answer the student\'s recall covers', ['none of it', 'part of it', 'all of it']);
    questions.most_parts = noul('The model answer gives several reasons, parts or examples, and the student\'s recall gives at least half of them correctly in their own words');
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
      const p = a.correct ? a.correct.noul : 0, c = a.completeness ? a.completeness.score : 0, m = a.most_parts ? a.most_parts.noul : 0;
      // right when the judge is sure the key fact or link is there (a short answer in the
      // student's own words is still right), or fairly sure and the answer is complete, or the
      // answer has several parts and the student gave at least half of them
      const verdict = (p >= 0.75 || (p >= 0.6 && c >= 1.5) || (p >= 0.45 && m >= 0.7)) ? 'right' : ((p >= 0.45 || c >= 0.9) ? 'partly' : 'wrong');
      out = { kind, p: p, completeness: c, parts: m, verdict: verdict };
    }
    out.usage = r.usage ? r.usage.input_tokens : undefined;
    return res.status(200).json(out);
  } catch (e) {
    return res.status(502).json({ error: 'Could not judge that one', fallback: true, detail: String(e.message || e).slice(0, 200) });
  }
};
