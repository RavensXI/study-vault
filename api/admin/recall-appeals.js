const { supabase } = require('../pipeline/_lib/supabase');

/**
 * Typed-recall appeals: when a student presses "I think I was right?" on a card the
 * judge marked wrong, the case (card, what they typed, verdict) is saved to their
 * account under sv-recall-appeals. This lists those cases grouped by card, most
 * appealed first, so the judge's rules can be fixed where they trip. Read-only, and
 * nothing about who appealed leaves the server.
 *
 * GET ?kind=all|recall|term|definition|cloze&limit=100
 */
function isAuthed(req) {
  const adminPw = req.headers['x-admin-password'];
  return adminPw && process.env.ADMIN_PASSWORD && adminPw === process.env.ADMIN_PASSWORD;
}

module.exports = async (req, res) => {
  if (!isAuthed(req)) return res.status(401).json({ error: 'Unauthorised' });
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });
  const kind = String(req.query.kind || 'all');
  const limit = Math.min(parseInt(req.query.limit, 10) || 100, 500);

  const { data, error } = await supabase.from('user_state').select('value, updated_at').eq('key', 'sv-recall-appeals');
  if (error) return res.status(500).json({ error: error.message });

  const groups = new Map(); let total = 0;
  (data || []).forEach(row => {
    let arr = [];
    try { arr = JSON.parse((row.value && row.value.raw) || '[]'); } catch (e) { return; }
    if (!Array.isArray(arr)) return;
    arr.forEach(a => {
      if (!a || !a.front) return;
      if (kind !== 'all' && (a.kind || 'recall') !== kind) return;
      total++;
      const key = (a.kind || 'recall') + '|' + a.front;
      const g = groups.get(key) || { kind: a.kind || 'recall', front: a.front, answer: a.answer || '', n: 0, verdicts: {}, typed: [], last: 0 };
      g.n++;
      g.verdicts[a.verdict || '?'] = (g.verdicts[a.verdict || '?'] || 0) + 1;
      if (a.typed && g.typed.length < 6 && !g.typed.includes(a.typed)) g.typed.push(a.typed);
      if (a.t && a.t > g.last) g.last = a.t;
      groups.set(key, g);
    });
  });
  const list = Array.from(groups.values()).sort((x, y) => y.n - x.n || y.last - x.last).slice(0, limit);
  return res.json({ total: total, cards: list.length, students_with_appeals: (data || []).length, groups: list });
};
