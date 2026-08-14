const { supabase } = require('../../pipeline/_lib/supabase');

/**
 * Who may see which class, and which parts of a pupil's progress.
 *
 * This lives in one file because it is a security filter, and a security filter
 * with two copies eventually has two behaviours. Both class-progress.js and the
 * parents'-evening pack import from here.
 *
 * The rules are recorded in memory as feedback_teacher_data_boundary:
 *   SEND           attainment
 *   AGGREGATE ONLY when or how much a particular child worked
 *   NEVER          flashcard spacing, planner prefs, rest days, shorts
 * plus: a teacher sees THEIR SUBJECT and nothing else.
 */

/* keys on the progress blob that must never leave the server */
const NEVER_SEND = ['flashsr', 'flashday', 'flashlog', 'plan', 'shortschecks'];

/* Every key on the blob is "subject-slug/unit[/lesson]".
   Match the BASE subject, not the exact slug: a class is keyed to the board the
   school teaches (maths-edexcel) while a pupil's progress is logged under
   whichever board they picked (maths-aqa). Same maths either way. */
function baseSubject(slug) {
  return String(slug || '').toLowerCase()
    /* edexcel carries A/B variants exactly as ocr does (geography-edexcel-a,
       geography-edexcel-b) — without the group they fail to reduce and
       cross-board matching silently never applies to those subjects */
    .replace(/-(aqa|edexcel(-[ab])?|eduqas|wjec|ncfe|ocr(-[ab])?)$/, '');
}

function inScope(key, base) {
  if (!base) return true;                       // class has no subject: no filter
  return baseSubject(String(key).split('/')[0]) === base;
}

function pick(obj, base) {
  const out = {};
  Object.keys(obj || {}).forEach(function (k) { if (inScope(k, base)) out[k] = obj[k]; });
  return out;
}

function scrub(blob) {
  const b = Object.assign({}, blob || {});
  NEVER_SEND.forEach(function (k) { delete b[k]; });
  return b;
}

/**
 * Load a class and decide whether this person may see it.
 * Returns { ok:false, status, error } or { ok:true, cls, subject, base }.
 */
async function loadClassFor(auth, classId) {
  if (!classId) return { ok: false, status: 400, error: 'Missing class_id' };

  const { data: cls, error } = await supabase
    .from('classes')
    .select('id, name, school_id, subject_id, teacher_id, year_group')
    .eq('id', classId).single();
  if (error || !cls) return { ok: false, status: 404, error: 'Class not found' };

  /* You may see a class you teach. A school_admin may see any class in their
     own school. platform_admin sees anything. Nobody sees another school. */
  const role = auth.profile.role;
  const mine = cls.teacher_id && cls.teacher_id === auth.profile.id;
  const sameSchool = cls.school_id && cls.school_id === auth.profile.school_id;
  if (!(role === 'platform_admin' || mine || (role === 'school_admin' && sameSchool))) {
    return { ok: false, status: 403, error: 'That class is not yours.' };
  }

  let subject = null, base = '';
  if (cls.subject_id) {
    const { data: s } = await supabase
      .from('subjects').select('id, slug, name').eq('id', cls.subject_id).maybeSingle();
    if (s) { subject = s; base = baseSubject(s.slug); }
  }
  return { ok: true, cls, subject, base };
}

/* A student must actually be in the class before anyone reads their progress.
   Being allowed to open a class is not the same as being allowed to open any
   pupil the caller can name. */
async function isMember(classId, studentId) {
  if (!studentId) return false;
  const { data } = await supabase
    .from('class_members').select('class_id')
    .eq('class_id', classId).eq('student_id', studentId).maybeSingle();
  return !!data;
}

module.exports = { NEVER_SEND, baseSubject, inScope, pick, scrub, loadClassFor, isMember };
