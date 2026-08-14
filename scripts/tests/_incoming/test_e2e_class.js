/* End to end: teacher creates a class -> student joins with the code ->
   the class appears on the teacher's progress endpoint.

   This WRITES to the live database, so everything it creates is named
   __E2E_TEST__ and is deleted at the end, including on failure. It touches no
   existing class and no existing membership. */
const path = require('path');
const REPO = 'C:/Users/tshau/Documents/Study Vault';

const authPath = require.resolve(path.join(REPO, 'api/pipeline/_lib/auth.js'));
let AUTH = null;
require.cache[authPath] = { id: authPath, filename: authPath, loaded: true,
  exports: { requireTeacher: async () => AUTH } };

const { createClient } = require(path.join(REPO, 'node_modules/@supabase/supabase-js'));
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const create = require(path.join(REPO, 'api/teacher/create-class.js'));
const join = require(path.join(REPO, 'api/class/join.js'));
const progress = require(path.join(REPO, 'api/teacher/class-progress.js'));

const res = () => { const r = { code: null, body: null };
  r.status = c => { r.code = c; return r; }; r.json = b => { r.body = b; return r; }; return r; };

let newClassId = null, studentId = null;

async function cleanup() {
  if (newClassId) {
    await sb.from('class_members').delete().eq('class_id', newClassId);
    await sb.from('classes').delete().eq('id', newClassId);
    const { data } = await sb.from('classes').select('id').eq('id', newClassId);
    console.log('\ncleanup: test class removed ->', (data || []).length === 0 ? 'yes' : 'STILL THERE');
  }
}

(async () => {
  /* a real teacher and a real subject, so the row is valid */
  const { data: teacher } = await sb.from('profiles')
    .select('id, full_name, school_id, role').eq('role', 'teacher').limit(1).single();
  const { data: subject } = await sb.from('subjects')
    .select('id, name').eq('slug', 'english-literature-aqa').single();
  const { data: student } = await sb.from('progress')
    .select('person_id').limit(1).single();
  studentId = student.person_id;

  console.log('teacher :', teacher.full_name);
  console.log('subject :', subject.name);

  AUTH = { profile: teacher };

  /* 1 — create */
  let r = res();
  await create({ method: 'POST', headers: {}, body:
    { name: '__E2E_TEST__', subject_id: subject.id, year_group: 11 } }, r);
  console.log('\n1. create class ->', r.code);
  if (r.code !== 200) { console.log('   ', JSON.stringify(r.body)); return; }
  newClassId = r.body.class.id;
  const code = r.body.class.joinCode;
  console.log('   code:', code, '| reads out as:', r.body.instructions);
  console.log('   6 chars, no ambiguous:', code.length === 6 && !/[ILOU01]/.test(code));

  /* 2 — a student joins with it */
  r = res();
  await join({ method: 'POST', headers: {}, body: { code: code, student_id: studentId } }, r);
  console.log('\n2. student joins ->', r.code, '| alreadyIn:', r.body.alreadyIn);
  console.log('   class :', r.body.class.name, '·', r.body.class.subject, '· teacher', r.body.class.teacher);
  console.log('   told  :', r.body.visibility);

  /* 3 — lower case, spaces, typed off a whiteboard */
  r = res();
  const messy = (code.slice(0, 3) + ' ' + code.slice(3)).toLowerCase();
  await join({ method: 'POST', headers: {}, body: { code: messy, student_id: studentId } }, r);
  console.log('\n3. same code typed "' + messy + '" ->', r.code, '| alreadyIn:', r.body.alreadyIn,
              '(must be true — no duplicate row)');

  const { data: mems } = await sb.from('class_members').select('student_id').eq('class_id', newClassId);
  console.log('   membership rows:', mems.length, mems.length === 1 ? '(correct)' : '(DUPLICATE!)');

  /* 4 — the teacher now sees them on the progress endpoint */
  r = res();
  await progress({ method: 'GET', headers: {}, query: { class_id: newClassId }, body: {} }, r);
  console.log('\n4. teacher opens the class ->', r.code);
  console.log('   subject scope:', r.body.class.subject);
  console.log('   size:', r.body.size, '| students:', JSON.stringify(r.body.students[0]));
  console.log('   missed items:', r.body.missedItems.length, '| weak units:', r.body.weakestUnits.length);

  /* 5 — a different teacher must not see it */
  const { data: other } = await sb.from('profiles')
    .select('id, role, school_id').eq('role', 'teacher').neq('id', teacher.id).limit(1).single();
  AUTH = { profile: other };
  r = res();
  await progress({ method: 'GET', headers: {}, query: { class_id: newClassId }, body: {} }, r);
  console.log('\n5. a different teacher ->', r.code, JSON.stringify(r.body));
})().catch(e => console.log('\nFAILED:', e.message)).finally(cleanup);
