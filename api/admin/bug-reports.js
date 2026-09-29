const { supabase } = require('../pipeline/_lib/supabase');
const { deleteScreenshot, deleteAfter } = require('../_lib/bug-screenshot');

const ALLOWED_STATUS = ['open', 'investigating', 'fixed', 'wontfix'];

function isAuthed(req) {
  const adminPw = req.headers['x-admin-password'];
  return adminPw && process.env.ADMIN_PASSWORD && adminPw === process.env.ADMIN_PASSWORD;
}

module.exports = async (req, res) => {
  if (!isAuthed(req)) return res.status(401).json({ error: 'Unauthorised' });

  if (req.method === 'GET') {
    const status = req.query.status || '';
    let q = supabase
      .from('bug_reports')
      .select('id, message, email, page_url, screenshot_url, viewport_size, user_agent, status, notes, created_at, notified_at')
      .order('created_at', { ascending: false })
      .limit(500);
    if (status && ALLOWED_STATUS.includes(status)) q = q.eq('status', status);
    const { data, error } = await q;
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ reports: data || [] });
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
    if (typeof notes === 'string') update.notes = notes.slice(0, 2000);
    if (notified_at !== undefined) update.notified_at = notified_at;
    if (Object.keys(update).length === 0) {
      return res.status(400).json({ error: 'Nothing to update' });
    }
    // Closing a report deletes its screenshot now and the report 30 days later; reopening keeps it.
    if (status === 'fixed' || status === 'wontfix') {
      const { data: row } = await supabase.from('bug_reports').select('screenshot_url').eq('id', id).maybeSingle();
      if (row && row.screenshot_url && await deleteScreenshot(row.screenshot_url)) update.screenshot_url = null;
      update.delete_after = deleteAfter();
    } else if (status) update.delete_after = null;
    const { error } = await supabase.from('bug_reports').update(update).eq('id', id);
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ ok: true });
  }

  if (req.method === 'DELETE') {
    const { id } = req.body || {};
    if (!id) return res.status(400).json({ error: 'id required' });
    const { data: row } = await supabase.from('bug_reports').select('screenshot_url').eq('id', id).maybeSingle();
    if (row && row.screenshot_url) await deleteScreenshot(row.screenshot_url);
    const { error } = await supabase.from('bug_reports').delete().eq('id', id);
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ ok: true });
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
