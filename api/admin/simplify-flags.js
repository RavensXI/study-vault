/**
 * Admin — Simplify QA queue
 *
 * Surfaces simplify_cache rows that failed the async Sonnet QA twice
 * (qa_status='pending_review'). The original (already fact-checked) paragraph
 * is served to students until an admin resolves the row here.
 *
 * Actions:
 *   PATCH  { id, status?, simplified_text? }  — approve (status='pass'),
 *                                               or save a hand-edited rewrite
 *   DELETE { id }                             — purge; regenerates fresh on
 *                                               the next student view
 *
 * Auth: X-Admin-Password header === ADMIN_PASSWORD (mirrors bug-reports.js).
 */

const { supabase } = require('../pipeline/_lib/supabase');

const ALLOWED_STATUS = ['pass', 'pending_review'];

function isAuthed(req) {
  const adminPw = req.headers['x-admin-password'];
  return adminPw && process.env.ADMIN_PASSWORD && adminPw === process.env.ADMIN_PASSWORD;
}

module.exports = async (req, res) => {
  if (!isAuthed(req)) return res.status(401).json({ error: 'Unauthorised' });

  if (req.method === 'GET') {
    const status = req.query.status || 'pending_review';
    let q = supabase
      .from('simplify_cache')
      .select('id, lesson_id, target_level, paragraph_index, subject_slug, original_text, simplified_text, qa_status, qa_notes, regen_count, created_at, updated_at, lessons(title)')
      .order('updated_at', { ascending: false })
      .limit(500);
    if (status && status !== 'all') q = q.eq('qa_status', status);
    const { data, error } = await q;
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ entries: data || [] });
  }

  if (req.method === 'PATCH') {
    const { id, status, simplified_text } = req.body || {};
    if (!id) return res.status(400).json({ error: 'id required' });
    const update = {};
    if (status) {
      if (!ALLOWED_STATUS.includes(status)) return res.status(400).json({ error: 'Invalid status' });
      update.qa_status = status;
    }
    if (typeof simplified_text === 'string') {
      if (!simplified_text.trim()) return res.status(400).json({ error: 'simplified_text empty' });
      update.simplified_text = simplified_text.slice(0, 8000);
    }
    if (Object.keys(update).length === 0) return res.status(400).json({ error: 'Nothing to update' });
    const { error } = await supabase.from('simplify_cache').update(update).eq('id', id);
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ ok: true });
  }

  if (req.method === 'DELETE') {
    const { id } = req.body || {};
    if (!id) return res.status(400).json({ error: 'id required' });
    const { error } = await supabase.from('simplify_cache').delete().eq('id', id);
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ ok: true });
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
