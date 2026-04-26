const { supabase } = require('../pipeline/_lib/supabase');

const ALLOWED_STATUS = ['pending', 'building', 'live', 'rejected'];

function isAuthed(req) {
  const adminPw = req.headers['x-admin-password'];
  return adminPw && process.env.ADMIN_PASSWORD && adminPw === process.env.ADMIN_PASSWORD;
}

module.exports = async (req, res) => {
  if (!isAuthed(req)) return res.status(401).json({ error: 'Unauthorised' });

  if (req.method === 'GET') {
    const status = req.query.status || '';
    let q = supabase
      .from('subject_requests')
      .select('id, subject_name, topic, exam_board, email, notes, status, user_agent, created_at, notified_at')
      .order('created_at', { ascending: false })
      .limit(500);
    if (status && ALLOWED_STATUS.includes(status)) q = q.eq('status', status);
    const { data, error } = await q;
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ requests: data || [] });
  }

  if (req.method === 'PATCH') {
    const { id, status, notes, notified_at } = req.body || {};
    if (!id) return res.status(400).json({ error: 'id required' });
    const update = {};
    if (status) {
      if (!ALLOWED_STATUS.includes(status)) {
        return res.status(400).json({ error: 'Invalid status' });
      }
      update.status = status;
    }
    if (typeof notes === 'string') update.notes = notes.slice(0, 500);
    if (notified_at !== undefined) update.notified_at = notified_at;
    if (Object.keys(update).length === 0) {
      return res.status(400).json({ error: 'Nothing to update' });
    }
    const { error } = await supabase.from('subject_requests').update(update).eq('id', id);
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ ok: true });
  }

  if (req.method === 'DELETE') {
    const { id } = req.body || {};
    if (!id) return res.status(400).json({ error: 'id required' });
    const { error } = await supabase.from('subject_requests').delete().eq('id', id);
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ ok: true });
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
