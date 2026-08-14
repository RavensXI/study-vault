/* Stub the auth layer so this tests the AGGREGATION and the ownership rule,
   not the password. Auth itself is covered by requireTeacher's own callers. */
const path = require('path');
const REPO = 'C:/Users/tshau/Documents/Study Vault';
const authPath = require.resolve(path.join(REPO, 'api/pipeline/_lib/auth.js'));
let AUTH = null;
require.cache[authPath] = { id: authPath, filename: authPath, loaded: true,
  exports: { requireTeacher: async () => AUTH } };

const { createClient } = require(path.join(REPO, 'node_modules/@supabase/supabase-js'));
const handler = require(path.join(REPO, 'api/teacher/class-progress.js'));
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const res = () => { const r = { code:null, body:null };
  r.status = c => { r.code = c; return r; }; r.json = b => { r.body = b; return r; }; return r; };
const req = id => ({ method:'GET', query:{ class_id:id }, headers:{}, body:{} });

/* Which class to walk. Default is the first (maths, practice-format, so it has
   no knowledge checks by design). Pass a class id to test an article subject —
   the point being that "all zeroes" must be proved to be the SUBJECT, not the
   scoping filter quietly emptying everything. */
const TARGET = process.argv[2];

(async () => {
  const q = sb.from('classes').select('id,name,teacher_id,school_id');
  const cls = TARGET ? (await q.eq('id', TARGET).single()).data : (await q.limit(1)).data[0];
  console.log('class under test:', cls.name);

  AUTH = { profile: { id: 'x', role: 'platform_admin', school_id: null } };
  let r = res(); await handler(req(cls.id), r);
  console.log('\nplatform_admin ->', r.code);
  const b = r.body;
  console.log('  subject scope:', b.class.subject, '(' + b.class.subjectSlug + ')');
  console.log('  size:', b.size, '| students:', b.students.length);
  console.log('  activity:', JSON.stringify(b.activity));
  console.log('  sample:', JSON.stringify(b.students[0]));
  console.log('  misconceptions:', b.misconceptions.length);
  b.misconceptions.slice(0,3).forEach(m => console.log('     ' + m.students + ' students · ' + String(m.tag).slice(0,58)));
  console.log('');
  console.log('  WEAKEST UNITS (warm-up accuracy, >=12 attempts):', b.weakestUnits.length);
  b.weakestUnits.slice(0,6).forEach(u =>
    console.log('     ' + String(u.accuracy).padStart(3) + '%  (' + u.attempts + ' attempts)  ' + u.unit));

  console.log('');
  console.log('  MOST-MISSED QUESTIONS (>=2 students):', b.missedItems.length);
  b.missedItems.slice(0,6).forEach(q => {
    console.log('     ' + q.students + ' students · ' + q.where);
    console.log('        Q: ' + q.question.slice(0,92));
    console.log('        they chose: "' + q.commonWrongAnswer + '" (x' + q.commonWrongCount + ')   answer: "' + q.right + '"');
  });

  const s = JSON.stringify(b);
  console.log('  PRIVATE keys leaked:', (s.match(/flashsr|flashday|flashlog|shortschecks/g) || ['none']).join(','));
  console.log('  raw timestamps leaked:', (s.match(/\d{4}-\d{2}-\d{2}T/g) || []).length);

  AUTH = { profile: { id: cls.teacher_id, role: 'teacher', school_id: cls.school_id } };
  r = res(); await handler(req(cls.id), r);
  console.log('\nthe class\'s OWN teacher ->', r.code);

  AUTH = { profile: { id: 'someone-else', role: 'teacher', school_id: cls.school_id } };
  r = res(); await handler(req(cls.id), r);
  console.log('a DIFFERENT teacher, same school ->', r.code, JSON.stringify(r.body).slice(0,50));

  AUTH = { profile: { id: 'other', role: 'school_admin', school_id: '00000000-0000-0000-0000-000000000000' } };
  r = res(); await handler(req(cls.id), r);
  console.log('school_admin of ANOTHER school ->', r.code);
})();
