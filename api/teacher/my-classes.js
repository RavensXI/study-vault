const { requireTeacher } = require('../pipeline/_lib/auth');
const { supabase } = require('../pipeline/_lib/supabase');

/**
 * The classes this teacher owns, with their join codes and roll sizes.
 *
 * Runs server-side rather than letting the page query the classes table, for
 * one reason that matters: the shared TEACHER_PASSWORD login has no auth.uid(),
 * so row-level security returns it nothing. A page built on a direct query would
 * work for individually-signed-in teachers and silently show an empty list to
 * everyone on the shared password.
 *
 * Roll size only — no student names and no attainment. Those come from
 * class-progress.js, which enforces the data boundary.
 */
module.exports = async function handler(req, res) {
  if (req.method !== 'GET' && req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const role = auth.profile.role;

  let q = supabase
    .from('classes')
    .select('id, name, year_group, subject_id, join_code, join_open, teacher_id, school_id')
    .order('name');

  /* A teacher sees their own. A school admin sees their school's. Only
     platform_admin sees everything, and that is Tom looking at his own data. */
  if (role === 'teacher') {
    q = q.eq('teacher_id', auth.profile.id);
  } else if (role === 'school_admin') {
    q = q.eq('school_id', auth.profile.school_id);
  }

  const { data: classes, error } = await q;
  if (error) return res.status(500).json({ error: 'Could not load your classes.', detail: error.message });
  if (!classes || !classes.length) {
    return res.status(200).json({ classes: [], canBuild: !!auth.profile.school_id,
                                  subjects: await subjectList(auth) });
  }

  const ids = classes.map(function (c) { return c.id; });
  const subjectIds = [...new Set(classes.map(function (c) { return c.subject_id; }).filter(Boolean))];

  const [{ data: members }, { data: subjects }] = await Promise.all([
    supabase.from('class_members').select('class_id').in('class_id', ids),
    subjectIds.length
      ? supabase.from('subjects').select('id, name').in('id', subjectIds)
      : Promise.resolve({ data: [] })
  ]);

  const size = {};
  (members || []).forEach(function (m) { size[m.class_id] = (size[m.class_id] || 0) + 1; });
  const subjectName = {};
  (subjects || []).forEach(function (s) { subjectName[s.id] = s.name; });

  return res.status(200).json({
    /* Whether this person's school may build its own content. A capability of
       the SCHOOL, never a link handed to a person: a link lives in one
       teacher's inbox and is lost the moment they leave, which is the failure
       we designed the class-derived access to avoid. */
    canBuild: !!auth.profile.school_id,
    classes: classes.map(function (c) {
      return {
        id: c.id,
        name: c.name,
        yearGroup: c.year_group,
        subject: subjectName[c.subject_id] || null,
        joinCode: c.join_code,
        joinOpen: c.join_open !== false,
        size: size[c.id] || 0
      };
    }),
    subjects: await subjectList(auth)
  });
};

/* What this teacher may create a class for.
   Their school's own bespoke subjects first, then the generic ones every
   student can already reach. CLAUDE.md documents a school_subscriptions table
   for this; it does not exist in the database, and subjects.school_id is what
   actually carries the relationship. */
async function subjectList(auth) {
  const schoolId = auth.profile.school_id;

  const { data: generic } = await supabase
    .from('subjects').select('id, name, school_id')
    .is('school_id', null).eq('status', 'live').order('name').limit(400);

  let bespoke = [];
  if (schoolId) {
    const { data } = await supabase
      .from('subjects').select('id, name, school_id')
      .eq('school_id', schoolId).eq('status', 'live').order('name');
    bespoke = data || [];
  }

  /* Bespoke first: if a school has built its own Geography, that is the one
     their teacher means, and it should not be below 70 generic entries. */
  return bespoke
    .map(function (s) { return { id: s.id, name: s.name, own: true }; })
    .concat((generic || []).map(function (s) { return { id: s.id, name: s.name, own: false }; }));
}
