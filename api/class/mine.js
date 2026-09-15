const { supabase } = require('../pipeline/_lib/supabase');

/**
 * The classes the signed-in student is in, for the dashboard avatar menu.
 *
 * Runs server-side on the service key for the same reason join.js does: a
 * student may read their own memberships under RLS, but not the teacher's
 * profile row, and the menu line is "In 10X with Mr Shaun" — the name is the
 * point. Identity comes from the bearer token only; nothing in the query
 * string or body chooses whose classes come back.
 *
 * Returns { classes: [{ id, name, subject, teacher, year_group }] } — the same
 * shape join.js confirms with, so the menu and the confirmation card agree.
 */
module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const authHeader = req.headers.authorization || '';
  if (!authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Sign in first.' });
  }
  const { data: userData, error: authError } =
    await supabase.auth.getUser(authHeader.slice(7));
  if (authError || !userData || !userData.user) {
    return res.status(401).json({ error: 'Your sign-in has expired.' });
  }
  const studentId = userData.user.id;

  const { data: rows, error } = await supabase
    .from('class_members').select('class_id').eq('student_id', studentId);
  if (error) return res.status(500).json({ error: 'Could not read your classes.' });
  const ids = (rows || []).map(function (r) { return r.class_id; });
  if (!ids.length) return res.status(200).json({ classes: [] });

  const { data: classes } = await supabase
    .from('classes').select('id, name, year_group, teacher_id, subject_id').in('id', ids);
  const list = classes || [];

  const teacherIds = Array.from(new Set(list.map(function (c) { return c.teacher_id; }).filter(Boolean)));
  const subjectIds = Array.from(new Set(list.map(function (c) { return c.subject_id; }).filter(Boolean)));
  const [{ data: teachers }, { data: subjects }] = await Promise.all([
    teacherIds.length ? supabase.from('profiles').select('id, full_name').in('id', teacherIds) : Promise.resolve({ data: [] }),
    subjectIds.length ? supabase.from('subjects').select('id, name').in('id', subjectIds) : Promise.resolve({ data: [] })
  ]);
  const tName = {}; (teachers || []).forEach(function (t) { tName[t.id] = t.full_name; });
  const sName = {}; (subjects || []).forEach(function (s) { sName[s.id] = s.name; });

  /* Only the fields the menu prints. The join code, the roll and the other
     students never leave the server. */
  return res.status(200).json({
    classes: list.map(function (c) {
      return {
        id: c.id,
        name: c.name,
        subject: sName[c.subject_id] || null,
        teacher: tName[c.teacher_id] || null,
        year_group: c.year_group || null
      };
    })
  });
};
