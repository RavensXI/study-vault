/* Museum exhibit 3: class-progress shape, privacy, and the ownership rule.
   Aggregation VALUES vary with live data and stay unasserted — the contract
   is: platform_admin gets the full shape, private localStorage key names and
   raw timestamps never leak, the class's own teacher gets 200, a different
   teacher and another school's admin get 403. Read-only.

   Extended 29 Aug when the class screen stopped being a prototype: the
   attainment, lessonAttainment and coverage blocks are checked for INTERNAL
   CONSISTENCY rather than for values — a percentage is recomputed from the
   progress table independently, coverage may never exceed the course, and the
   evidence thresholds must hold. A wrong key on the blob returns nulls that
   look exactly like "this class has not started yet", so a shape test alone
   would have passed the bug it is meant to catch. */
const path = require('path');
const REPO = path.join(__dirname, '..', '..', '..');

let fails = 0;
function t(name, cond, detail) {
  if (!cond) fails++;
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (detail !== undefined ? ' — ' + detail : ''));
}

const authPath = require.resolve(path.join(REPO, 'api/pipeline/_lib/auth.js'));
let AUTH = null;
require.cache[authPath] = { id: authPath, filename: authPath, loaded: true,
  exports: { requireTeacher: async () => AUTH } };

const { createClient } = require(path.join(REPO, 'node_modules/@supabase/supabase-js'));
const handler = require(path.join(REPO, 'api/teacher/class-progress.js'));
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const res = () => { const r = { code: null, body: null };
  r.status = c => { r.code = c; return r; }; r.json = b => { r.body = b; return r; }; return r; };
const req = id => ({ method: 'GET', query: { class_id: id }, headers: {}, body: {} });

(async () => {
  const { data: cls } = await sb.from('classes')
    .select('id,name,teacher_id,school_id')
    .not('name', 'like', '__E2E_TEST__%').limit(1).single();

  AUTH = { profile: { id: 'x', role: 'platform_admin', school_id: null } };
  let r = res();
  await handler(req(cls.id), r);
  t('platform_admin -> 200', r.code === 200, r.code);
  const b = r.body || {};
  t('subject scope present', !!(b.class && b.class.subject && b.class.subjectSlug));
  t('students array', Array.isArray(b.students));
  t('activity object', b.activity && typeof b.activity === 'object');
  t('misconceptions array', Array.isArray(b.misconceptions));
  t('weakest-units array', Array.isArray(b.weakestUnits));
  t('missed-items array', Array.isArray(b.missedItems));

  const s = JSON.stringify(b);
  t('no private localStorage keys leak',
    !/flashsr|flashday|flashlog|shortschecks/.test(s));
  t('no raw timestamps leak', !/\d{4}-\d{2}-\d{2}T/.test(s),
    ((s.match(/\d{4}-\d{2}-\d{2}T/g) || []).length) + ' found');

  AUTH = { profile: { id: cls.teacher_id, role: 'teacher', school_id: cls.school_id } };
  r = res(); await handler(req(cls.id), r);
  t("the class's own teacher -> 200", r.code === 200, r.code);

  AUTH = { profile: { id: 'someone-else', role: 'teacher', school_id: cls.school_id } };
  r = res(); await handler(req(cls.id), r);
  t('a different teacher, same school -> 403', r.code === 403, r.code);

  AUTH = { profile: { id: 'other', role: 'school_admin',
                      school_id: '00000000-0000-0000-0000-000000000000' } };
  r = res(); await handler(req(cls.id), r);
  t("another school's admin -> 403", r.code === 403, r.code);

  AUTH = { profile: { id: 'x', role: 'platform_admin', school_id: null } };
  r = res(); await handler({ method: 'GET', query: {}, headers: {}, body: {} }, r);
  t('no class_id -> 400', r.code === 400, r.code);

  /* ---- the class-level blocks ------------------------------------------
     Run against a class that actually has knowledge-check evidence, so the
     assertions below are about real arithmetic rather than about empty
     arrays agreeing with each other. */
  const withKc = await findClassWithEvidence(sb);
  t('a class with quiz evidence exists to test against', !!withKc,
    withKc ? withKc.name : 'none found — the blocks below are unproven');

  if (withKc) {
    r = res(); await handler(req(withKc.id), r);
    const d = r.body;
    const a = d.attainment;
    t('attainment block present', !!a && typeof a.answered === 'number', JSON.stringify(a));
    t('attainment accuracy is a real percentage',
      a.accuracy === null || (a.accuracy >= 0 && a.accuracy <= 100), a.accuracy);
    t('pupils with evidence cannot exceed the roll',
      a.studentsWithEvidence <= a.size, a.studentsWithEvidence + '/' + a.size);

    /* recomputed straight from the progress table, not from the response */
    const { data: mem } = await sb.from('class_members')
      .select('student_id').eq('class_id', withKc.id);
    const ids = mem.map(m => m.student_id);
    const { data: prog } = await sb.from('progress').select('blob').in('person_id', ids);
    let right = 0, total = 0;
    prog.forEach(p => Object.keys((p.blob || {}).kc || {}).forEach(k => {
      if (baseOf(k.split('/')[0]) !== withKc.base) return;
      const v = p.blob.kc[k];
      if (typeof v.s === 'number' && typeof v.t === 'number') { right += v.s; total += v.t; }
    }));
    t('class accuracy matches an independent recount',
      a.answered === total &&
      a.accuracy === (total >= 10 ? Math.round(right / total * 100) : null),
      a.answered + '/' + total + ' ' + a.accuracy + '%');

    t('lessonAttainment respects its evidence thresholds',
      d.lessonAttainment.every(l => l.students >= 2 && l.answered >= 6 &&
                                    l.accuracy >= 0 && l.accuracy <= 100),
      JSON.stringify(d.lessonAttainment[0]));
    t('lesson rows are named for a human, not slugged',
      d.lessonAttainment.every(l => l.unit && !/\//.test(l.unit)),
      JSON.stringify((d.lessonAttainment[0] || {}).unit));
    t('weakest units are named too',
      d.weakestUnits.every(u => !/\//.test(u.unit)),
      JSON.stringify((d.weakestUnits[0] || {}).unit));

    const cov = d.coverage;
    t('coverage block present', !!cov && Array.isArray(cov.units));
    t('no unit reports more lessons reached than it holds',
      cov.units.every(u => !u.lessons || u.touched <= u.lessons),
      JSON.stringify(cov.units.filter(u => u.lessons && u.touched > u.lessons)));
    t('started + untouched accounts for every unit on the course',
      cov.unitsStarted + cov.unitsUntouched === cov.courseUnits,
      cov.unitsStarted + '+' + cov.unitsUntouched + ' vs ' + cov.courseUnits);
    t('the headline denominator is the started units, not the whole course',
      cov.lessonsInStartedUnits <= cov.courseLessons &&
      cov.lessonsTouched <= cov.lessonsInStartedUnits,
      cov.lessonsTouched + '/' + cov.lessonsInStartedUnits + ' of ' + cov.courseLessons);
    t('no study-habit figure is computed anywhere in the response',
      !/"(timeMinutes|streak|minutes|sessions|warmlog|plan|flash)/.test(JSON.stringify(d)));
  }

  /* ---- a class nobody has joined ---------------------------------------
     Every class in the live database has a roll, so the branch is exercised by
     making class_members answer empty rather than by writing a throwaway class
     into production. An empty class must return an honest empty body — not
     zeroes dressed up as measurements. */
  const realFrom = sb.from.bind(sb);
  const supaMod = require(path.join(REPO, 'api/pipeline/_lib/supabase.js'));
  const handlerFrom = supaMod.supabase.from.bind(supaMod.supabase);
  supaMod.supabase.from = table => table === 'class_members'
    ? { select: () => ({ eq: () => Promise.resolve({ data: [] }) }) }
    : handlerFrom(table);
  r = res(); await handler(req(cls.id), r);
  supaMod.supabase.from = handlerFrom;
  t('a class with no members returns an honest empty body',
    r.code === 200 && r.body.size === 0 && r.body.students.length === 0 &&
    r.body.attainment === null && r.body.coverage === null,
    JSON.stringify(r.body).slice(0, 140));
  t('the empty body still leaks no school or teacher id',
    !('school_id' in r.body.class) && !('teacher_id' in r.body.class));
  void realFrom;

  console.log('a07: ' + fails + ' failure(s)');
  process.exit(fails ? 1 : 0);
})().catch(e => { console.log('FAIL uncaught — ' + e.message); process.exit(1); });

function baseOf(slug) {
  return String(slug || '').toLowerCase()
    .replace(/-(aqa|edexcel(-[ab])?|eduqas|wjec|ncfe|ocr(-[ab])?)$/, '');
}

/* The first class whose members have knowledge-check answers in the class's own
   subject. Picking class[0] blindly landed on a practice-first maths set, where
   every attainment assertion passes vacuously against nulls. */
async function findClassWithEvidence(sb) {
  const { data: classes } = await sb.from('classes')
    .select('id, name, subject_id').not('name', 'like', '__E2E_TEST__%').limit(60);
  const { data: subjects } = await sb.from('subjects').select('id, slug');
  const slugOf = {};
  subjects.forEach(s => { slugOf[s.id] = s.slug; });

  for (const c of classes) {
    if (!c.subject_id || !slugOf[c.subject_id]) continue;
    const base = baseOf(slugOf[c.subject_id]);
    const { data: mem } = await sb.from('class_members')
      .select('student_id').eq('class_id', c.id).limit(40);
    if (!mem || !mem.length) continue;
    const { data: prog } = await sb.from('progress')
      .select('blob').in('person_id', mem.map(m => m.student_id));
    let answered = 0;
    (prog || []).forEach(p => Object.keys((p.blob || {}).kc || {}).forEach(k => {
      if (baseOf(k.split('/')[0]) !== base) return;
      const v = p.blob.kc[k];
      if (typeof v.t === 'number') answered += v.t;
    }));
    if (answered >= 40) return { id: c.id, name: c.name, base: base };
  }
  return null;
}
