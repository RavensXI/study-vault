const { supabase } = require('../pipeline/_lib/supabase');

const ALLOWED_STATUS = ['open', 'fixed', 'wontfix', 'duplicate'];

function isAuthed(req) {
  const adminPw = req.headers['x-admin-password'];
  return adminPw && process.env.ADMIN_PASSWORD && adminPw === process.env.ADMIN_PASSWORD;
}

module.exports = async (req, res) => {
  if (!isAuthed(req)) return res.status(401).json({ error: 'Unauthorised' });

  // ---- POST: create a new flag ----
  if (req.method === 'POST') {
    const { lesson_id, problem_path, note } = req.body || {};
    if (!lesson_id || typeof lesson_id !== 'string') {
      return res.status(400).json({ error: 'lesson_id required' });
    }
    if (!problem_path || typeof problem_path !== 'string') {
      return res.status(400).json({ error: 'problem_path required' });
    }
    if (!note || typeof note !== 'string' || !note.trim()) {
      return res.status(400).json({ error: 'note required' });
    }
    const row = {
      lesson_id: lesson_id,
      problem_path: problem_path.slice(0, 200),
      note: note.slice(0, 2000),
    };
    const { data, error } = await supabase
      .from('practice_qa_flags')
      .insert(row)
      .select('id')
      .single();
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ ok: true, id: data.id });
  }

  // ---- GET: list flags (joined with lesson/unit/subject context) ----
  if (req.method === 'GET') {
    const status = req.query.status || '';
    const lessonId = req.query.lesson_id || '';
    const subjectSlug = req.query.subject_slug || '';

    let q = supabase
      .from('practice_qa_flags')
      .select(`
        id, lesson_id, problem_path, note, status, created_at, fixed_at,
        lessons:lesson_id (
          id, lesson_number, title, slug,
          units:unit_id (
            id, slug, name,
            subjects:subject_id ( id, slug, name, exam_board, school_id )
          )
        )
      `)
      .order('created_at', { ascending: false })
      .limit(1000);

    if (status && status !== 'all') {
      if (!ALLOWED_STATUS.includes(status)) {
        return res.status(400).json({ error: 'Invalid status' });
      }
      q = q.eq('status', status);
    }
    if (lessonId) q = q.eq('lesson_id', lessonId);

    const { data, error } = await q;
    if (error) return res.status(500).json({ error: error.message });

    let flags = data || [];

    // subject_slug filter is applied in JS because Supabase's filter on a
    // nested joined column is awkward — keeps the API call simple.
    if (subjectSlug) {
      flags = flags.filter(function (f) {
        const sub = f.lessons && f.lessons.units && f.lessons.units.subjects;
        return sub && sub.slug === subjectSlug;
      });
    }

    return res.json({ flags: flags });
  }

  // ---- PATCH: update a flag's status ----
  if (req.method === 'PATCH') {
    const { id, status, fixed_at } = req.body || {};
    if (!id) return res.status(400).json({ error: 'id required' });
    const update = {};
    if (status) {
      if (!ALLOWED_STATUS.includes(status)) {
        return res.status(400).json({ error: 'Invalid status' });
      }
      update.status = status;
      if (status === 'fixed' && fixed_at === undefined) {
        update.fixed_at = new Date().toISOString();
      }
    }
    if (fixed_at !== undefined) update.fixed_at = fixed_at;
    if (Object.keys(update).length === 0) {
      return res.status(400).json({ error: 'Nothing to update' });
    }
    const { error } = await supabase
      .from('practice_qa_flags')
      .update(update)
      .eq('id', id);
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ ok: true });
  }

  // ---- DELETE ----
  if (req.method === 'DELETE') {
    const { id } = req.body || {};
    if (!id) return res.status(400).json({ error: 'id required' });
    const { error } = await supabase
      .from('practice_qa_flags')
      .delete()
      .eq('id', id);
    if (error) return res.status(500).json({ error: error.message });
    return res.json({ ok: true });
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
