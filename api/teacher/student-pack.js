const { requireTeacher } = require('../pipeline/_lib/auth');
const { buildPack } = require('./_lib/pack');

/**
 * One pupil's parents' evening pack.
 *
 * Ownership and subject scoping are enforced in _lib/scope.js, and the pupil
 * must actually be a member of the class — being allowed to open a class is not
 * the same as being allowed to open any pupil id the caller can name.
 */
module.exports = async function handler(req, res) {
  if (req.method !== 'GET' && req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const q = req.query || {}, b = req.body || {};
  const classId = q.class_id || b.class_id;
  const studentId = q.student_id || b.student_id;

  const out = await buildPack(auth, classId, studentId);
  if (!out.ok) return res.status(out.status || 400).json({ error: out.error });
  return res.status(200).json(out.pack);
};
