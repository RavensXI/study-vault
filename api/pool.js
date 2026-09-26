/**
 * The anonymous answer pool (26 Sep 2026, approved by Tom).
 *
 * POST { rows: [ {k, a, v} | {k, got, of} ] }   (sent by js/answer-pool.js with sendBeacon)
 *   k    question key, five parts: subject/unit/lesson/<set>/<index>
 *        set = bronze|silver|gold (practice), kc (knowledge check), pq (end-of-lesson question, mark only),
 *              fcq / fcr (typed flashcard: question deck / recall card). Full list in js/answer-pool.js.
 *   a    the answer as given (short answers and chosen options only), v right|wrong|partly
 *   got/of  the mark an AI-marked written answer received (the writing itself never comes here)
 *
 * What is stored (table answer_pool, service key only): the question key, the tidied answer
 * or the mark, the verdict, a count, and the ISO week the row was first seen. Nothing about
 * who answered: no account, school, class, device, IP address or time of answering. Anything
 * that looks like personal data (an email address, phone number, postcode, @handle or link),
 * or is longer than 60 characters, is dropped before it is counted.
 */
const RECENT = new Map();            // ip -> [timestamps]; a soft per-IP cap. The IP is never stored.
const WINDOW_MS = 60 * 1000, MAX_PER_WINDOW = 30;
function limited(ip) {
  const now = Date.now(); const arr = (RECENT.get(ip) || []).filter(t => now - t < WINDOW_MS);
  arr.push(now); RECENT.set(ip, arr);
  if (RECENT.size > 5000) RECENT.clear();
  return arr.length > MAX_PER_WINDOW;
}

const KEY = /^[a-z0-9-]{1,80}\/[a-z0-9-]{1,80}\/\d{1,4}\/[a-z0-9_-]{1,40}\/\d{1,4}$/;
const PERSONAL = [
  /[^\s@]+@[^\s@]+\.[a-z]{2,}/i,                                // email address
  /(^|[^\w])@\w{2,}/,                                           // @handle
  /\b(https?:\/\/|www\.)|\b[a-z0-9-]+\.(com|co\.uk|uk|org|net|io|me|tv)\b/i,   // links
  /(\+44\s?|\b0)7\d{3}\s?\d{3}\s?\d{3}\b|\b0[1-9]\d{1,3}\s?\d{3,4}\s?\d{3,4}\b/,   // UK phone
  /\b[a-z]{1,2}\d[a-z\d]?\s*\d[a-z]{2}\b/i                      // UK postcode
];

function tidy(s) {
  return String(s == null ? '' : s).replace(/\s+/g, ' ').trim().toLowerCase();
}

function cleanRow(r) {
  if (!r || typeof r !== 'object') return null;
  const k = String(r.k || '');
  if (!KEY.test(k)) return null;
  if (r.of != null) {
    const of = parseInt(r.of, 10), got = parseInt(r.got, 10);
    if (!(of > 0 && of <= 40 && got >= 0 && got <= of)) return null;
    return { question_key: k, kind: 'mark', answer_norm: '', verdict: '', marks_of: of, got: got };
  }
  const v = String(r.v || '');
  if (!['right', 'wrong', 'partly'].includes(v)) return null;
  const a = tidy(r.a);
  if (!a || a.length > 60) return null;
  if (!/^[01\s]+$/.test(a) && PERSONAL.some(re => re.test(a))) return null;   // binary answers are not phone numbers
  return { question_key: k, kind: 'answer', answer_norm: a, verdict: v, marks_of: 0, got: 0 };
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || req.socket?.remoteAddress || '?';
  if (limited(ip)) return res.status(429).json({ error: 'Slow down a little' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = null; } }
  const rows = (body && Array.isArray(body.rows) ? body.rows : []).slice(0, 50).map(cleanRow).filter(Boolean);
  if (!rows.length) return res.status(204).end();

  try {
    const r = await fetch(process.env.SUPABASE_URL + '/rest/v1/rpc/pool_add', {
      method: 'POST',
      headers: { apikey: process.env.SUPABASE_SERVICE_KEY, Authorization: 'Bearer ' + process.env.SUPABASE_SERVICE_KEY,
                 'Content-Type': 'application/json' },
      body: JSON.stringify({ p_rows: rows })
    });
    if (!r.ok) return res.status(502).json({ error: 'pool unavailable' });
    return res.status(204).end();
  } catch (e) {
    return res.status(502).json({ error: 'pool unavailable' });
  }
};

module.exports.cleanRow = cleanRow;   // for tests
