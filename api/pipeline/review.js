const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');

module.exports = async function handler(req, res) {
  const auth = await requireTeacher(req, res);
  if (!auth) return;

  // GET — fetch review queue and counts
  if (req.method === 'GET') {
    const { filter } = req.query;

    // Fetch counts by status
    const statuses = ['draft', 'review', 'approved', 'live'];
    const counts = {};
    for (const s of statuses) {
      const { count } = await supabase
        .from('lessons')
        .select('id', { count: 'exact', head: true })
        .eq('status', s);
      counts[s] = count || 0;
    }

    // Fetch lessons for the requested filter
    let query = supabase
      .from('lessons')
      .select('id, lesson_number, slug, title, status, updated_at, unit_id, units!inner(name, slug, subject_id, subjects!inner(name, slug))')
      .order('updated_at', { ascending: false });

    if (filter && filter !== 'all') {
      query = query.eq('status', filter);
    }

    const { data: lessons, error } = await query;
    if (error) {
      return res.status(500).json({ error: 'Failed to fetch lessons', detail: error.message });
    }

    return res.status(200).json({ lessons: lessons || [], counts });
  }

  // POST — approve or reject a lesson
  if (req.method === 'POST') {
    const { lesson_id, action, notes } = req.body;

    if (!lesson_id || !action) {
      return res.status(400).json({ error: 'Missing lesson_id or action' });
    }

    if (action === 'approve') {
      const { error } = await supabase
        .from('lessons')
        .update({ status: 'live', approved_at: new Date().toISOString() })
        .eq('id', lesson_id);

      if (error) {
        return res.status(500).json({ error: 'Failed to approve', detail: error.message });
      }

      // Log
      await supabase.from('content_pipeline_logs').insert({
        lesson_id,
        from_status: 'review',
        to_status: 'live',
        changed_by: auth.profile.id || auth.user.id,
        notes: notes || 'Approved via review UI',
      });

      return res.status(200).json({ ok: true });

    } else if (action === 'reject') {
      const { error } = await supabase
        .from('lessons')
        .update({ status: 'draft' })
        .eq('id', lesson_id);

      if (error) {
        return res.status(500).json({ error: 'Failed to reject', detail: error.message });
      }

      await supabase.from('content_pipeline_logs').insert({
        lesson_id,
        from_status: 'review',
        to_status: 'draft',
        changed_by: auth.profile.id || auth.user.id,
        notes: notes || 'Rejected via review UI',
      });

      return res.status(200).json({ ok: true });

    } else if (action === 'approve_all') {
      // Bulk approve all lessons in review status — single update, no loop
      const { error, count } = await supabase
        .from('lessons')
        .update({ status: 'live', approved_at: new Date().toISOString() })
        .eq('status', 'review');

      if (error) {
        return res.status(500).json({ error: 'Failed to bulk approve', detail: error.message });
      }

      return res.status(200).json({ ok: true, approved: count || 0 });
    }

    return res.status(400).json({ error: 'Unknown action: ' + action });
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
