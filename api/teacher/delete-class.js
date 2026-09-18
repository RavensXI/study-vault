const { requireTeacher } = require('../pipeline/_lib/auth');
const { supabase } = require('../pipeline/_lib/supabase');
const { loadClassFor } = require('./_lib/scope');

/**
 * Delete a class the teacher owns (or, for a school_admin, any class at their
 * school). The memberships go with it; the students keep every bit of their
 * revision, because nothing of theirs lives on the class. The caller must send
 * the word "delete" typed out, so a stray tap cannot do it (Tom, 19 Sep 2026).
 *
 * POST { class_id, confirm: "delete" }
 */
module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  const auth = await requireTeacher(req, res);
  if (!auth) return;
  const body = req.body || {};
  if (String(body.confirm || '').trim().toLowerCase() !== 'delete') {
    return res.status(400).json({ error: 'Type the word delete to confirm.' });
  }
  const scope = await loadClassFor(auth, body.class_id);
  if (!scope.ok) return res.status(scope.status || 400).json({ error: scope.error });

  const { error: mErr } = await supabase.from('class_members').delete().eq('class_id', scope.cls.id);
  if (mErr) return res.status(500).json({ error: 'Could not remove the class members.', detail: mErr.message });
  const { error } = await supabase.from('classes').delete().eq('id', scope.cls.id);
  if (error) return res.status(500).json({ error: 'Could not delete the class.', detail: error.message });
  return res.status(200).json({ ok: true, deleted: scope.cls.id, name: scope.cls.name });
};
