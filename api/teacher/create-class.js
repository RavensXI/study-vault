const { requireTeacher } = require('../pipeline/_lib/auth');
const { supabase } = require('../pipeline/_lib/supabase');

/**
 * Create a class and return its join code.
 *
 * This is the department tier: a head of department makes a class, reads the
 * code out, and their students are in. No SSO, no IT department, no school
 * agreement needed first — which is the whole point of it commercially.
 *
 * Requires scripts/_create_class_join_codes.sql to have been run.
 */

/* Same alphabet as the SQL generator: no I, L, O, U, 0 or 1, because this gets
   read aloud and copied off a whiteboard. Generated here as well as in Postgres
   so the API does not depend on the function existing. */
const ALPHABET = 'ABCDEFGHJKMNPQRSTVWXYZ23456789';

function makeCode() {
  let out = '';
  for (let i = 0; i < 6; i++) {
    out += ALPHABET[Math.floor(Math.random() * ALPHABET.length)];
  }
  return out;
}

async function uniqueCode() {
  for (let attempt = 0; attempt < 8; attempt++) {
    const code = makeCode();
    const { data } = await supabase
      .from('classes').select('id').eq('join_code', code).maybeSingle();
    if (!data) return code;
  }
  /* Eight collisions against a 1.07bn space means something is wrong with the
     random source, not that we were unlucky. Fail loudly. */
  throw new Error('Could not allocate a unique join code');
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const body = req.body || {};
  const name = String(body.name || '').trim();
  const subjectId = body.subject_id || null;
  const yearGroup = body.year_group ? parseInt(body.year_group, 10) : null;

  if (!name) return res.status(400).json({ error: 'Give the class a name.' });
  if (name.length > 40) return res.status(400).json({ error: 'That name is too long.' });
  if (!subjectId) return res.status(400).json({ error: 'Choose a subject for the class.' });

  /* The subject must exist. A class pointing at nothing would aggregate to an
     empty dashboard with no explanation of why. */
  const { data: subject } = await supabase
    .from('subjects').select('id, name, slug').eq('id', subjectId).maybeSingle();
  if (!subject) return res.status(400).json({ error: 'That subject does not exist.' });

  /* A teacher creates classes in their own school, never anywhere else. The
     school is taken from their profile, never from the request body — otherwise
     anyone with a teacher account could plant a class in another school. */
  const schoolId = auth.profile.school_id || null;

  /* The uniqueness check and the insert are two round trips, so two teachers
     creating classes at the same moment can pass the check with the same code
     and race to the unique index. The index wins — but the loser used to get a
     bare 500. Retry with a fresh code instead; only a non-collision error is
     surfaced. */
  let created = null, error = null;
  for (let attempt = 0; attempt < 3; attempt++) {
    const code = await uniqueCode();
    ({ data: created, error } = await supabase
      .from('classes')
      .insert({
        name: name,
        subject_id: subject.id,
        year_group: isNaN(yearGroup) ? null : yearGroup,
        teacher_id: auth.profile.id,
        school_id: schoolId,
        join_code: code
      })
      .select('id, name, year_group, join_code')
      .single());
    if (!error) break;
    if (!/duplicate|unique|23505/i.test(error.message || '')) break;
  }

  if (error) {
    return res.status(500).json({ error: 'Could not create the class.', detail: error.message });
  }

  return res.status(200).json({
    class: {
      id: created.id,
      name: created.name,
      yearGroup: created.year_group,
      subject: subject.name,
      joinCode: created.join_code
    },
    /* what the teacher actually reads out */
    instructions: 'Students go to studyvault.co.uk/join and enter ' + created.join_code
  });
};
