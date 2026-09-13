const { requireTeacher } = require('../pipeline/_lib/auth');
const { supabase } = require('../pipeline/_lib/supabase');
const { loadClassFor } = require('./_lib/scope');

/**
 * Small edits to a class the teacher owns. Today: the register size (`roll`),
 * so the class screen can say "24 of 28 have joined" and the teacher knows how
 * many to chase from their own register. A number only — never pupil names,
 * which would be pupil data held before a pupil has joined (Tom, 13 Sep 2026).
 *
 * POST { class_id, roll }   roll: integer 1..60, or null to clear
 */
module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  const auth = await requireTeacher(req, res);
  if (!auth) return;
  const body = req.body || {};
  const scope = await loadClassFor(auth, body.class_id);
  if (!scope.ok) return res.status(scope.status || 400).json({ error: scope.error });

  const patch = {};
  if ('roll' in body) {
    if (body.roll === null || body.roll === '') patch.roll = null;
    else {
      const n = parseInt(body.roll, 10);
      if (isNaN(n) || n < 1 || n > 60) return res.status(400).json({ error: 'Register size must be a whole number between 1 and 60.' });
      patch.roll = n;
    }
  }
  if (!Object.keys(patch).length) return res.status(400).json({ error: 'Nothing to change.' });

  const { data, error } = await supabase.from('classes').update(patch).eq('id', scope.cls.id).select('id, roll').single();
  if (error) return res.status(500).json({ error: 'Could not save that.', detail: error.message });
  return res.status(200).json({ ok: true, class: data });
};
