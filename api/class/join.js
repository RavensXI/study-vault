const { supabase } = require('../pipeline/_lib/supabase');

/**
 * A student joins a class with a code.
 *
 * Deliberately runs server-side on the service key rather than letting the
 * browser query the classes table. A student needs to answer exactly one
 * question — "does this code match an open class" — and must not be able to
 * list classes, guess at them, or read the roll of a class they are not in.
 *
 * Joining a class is the moment a child's progress becomes visible to a member
 * of staff, so the response says plainly what they are agreeing to and names the
 * teacher. See memory feedback_teacher_data_boundary for what a teacher can then
 * see: attainment yes, study habits never.
 */

/* The generator never emits I, L, O, U, 0 or 1 precisely so they cannot be
   confused with 1, 0 and V. If one appears in what the student typed, it is a
   misread — and we say so rather than guessing. An earlier version folded these
   onto nearby characters, which can silently turn one valid code into a
   DIFFERENT valid code and put a child in the wrong class. A confusing error
   message is a support email; the wrong class is a data-protection incident. */
const AMBIGUOUS = /[ILOU01]/;

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const body = req.body || {};
  const code = String(body.code || '').toUpperCase().replace(/[\s\-_]/g, '');
  const studentId = body.student_id;

  if (!code) return res.status(400).json({ error: 'Enter the code your teacher gave you.' });
  if (!studentId) return res.status(401).json({ error: 'Sign in first, then join your class.' });

  if (AMBIGUOUS.test(code)) {
    return res.status(400).json({
      error: 'Class codes never use the letters I, L, O or U, or the digits 0 or 1. ' +
             'Have another look — it is probably a 1 for an I, or a 0 for an O.'
    });
  }
  if (code.length !== 6) {
    return res.status(400).json({ error: 'A class code is six characters. Check it with your teacher.' });
  }

  const { data: cls } = await supabase
    .from('classes')
    .select('id, name, year_group, join_open, teacher_id, subject_id')
    .eq('join_code', code)
    .maybeSingle();

  if (!cls) return res.status(404).json({ error: 'That code did not match a class. Check it with your teacher.' });
  if (cls.join_open === false) return res.status(403).json({ error: 'That class is not accepting new students.' });

  /* Already in it: say so plainly rather than erroring. A student who taps join
     twice has done nothing wrong. */
  const { data: existing } = await supabase
    .from('class_members')
    .select('class_id').eq('class_id', cls.id).eq('student_id', studentId).maybeSingle();

  if (!existing) {
    const { error } = await supabase
      .from('class_members').insert({ class_id: cls.id, student_id: studentId });
    if (error) {
      return res.status(500).json({ error: 'Could not join the class.', detail: error.message });
    }
  }

  const [{ data: teacher }, { data: subject }] = await Promise.all([
    supabase.from('profiles').select('full_name').eq('id', cls.teacher_id).maybeSingle(),
    supabase.from('subjects').select('name').eq('id', cls.subject_id).maybeSingle()
  ]);

  const who = (teacher && teacher.full_name) || 'Your teacher';
  const what = (subject && subject.name) || 'this subject';

  return res.status(200).json({
    joined: true,
    alreadyIn: !!existing,
    class: {
      id: cls.id,
      name: cls.name,
      subject: subject ? subject.name : null,
      teacher: teacher ? teacher.full_name : null
    },
    /* Shown to the student on the confirmation screen, not buried in a policy
       page. If we cannot state the trade plainly to a 15-year-old, we should not
       be making it on their behalf. */
    visibility: who + ' will be able to see how you get on in ' + what +
      ' — your scores, and which questions you find hard. They cannot see when ' +
      'you revise, your flashcard settings, or anything from your other subjects.'
  });
};
