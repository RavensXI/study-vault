/* The join endpoint after the auth fix.
   Everything created is named __E2E_TEST__ and deleted at the end.

   The Supabase client's auth.getUser is monkeypatched so the test can mint a
   "session" for a chosen user id — the point under test is the HANDLER's
   behaviour: no token → 401, bad token → 401, and the body student_id being
   ignored in favour of the token's identity. */
const path = require('path');
const REPO = 'C:/Users/tshau/Documents/Study Vault';

const authPath = require.resolve(path.join(REPO, 'api/pipeline/_lib/auth.js'));
let AUTH = null;
require.cache[authPath] = { id: authPath, filename: authPath, loaded: true,
  exports: { requireTeacher: async () => AUTH } };

const supaMod = require(path.join(REPO, 'api/pipeline/_lib/supabase.js'));
const realGetUser = supaMod.supabase.auth.getUser.bind(supaMod.supabase.auth);
let FAKE_USER = null;    // when set, tokens equal to 'good-token' resolve to this id
supaMod.supabase.auth.getUser = async function (tok) {
  if (FAKE_USER && tok === 'good-token') {
    return { data: { user: { id: FAKE_USER } }, error: null };
  }
  return realGetUser(tok);   // real verification for everything else
};

const { createClient } = require(path.join(REPO, 'node_modules/@supabase/supabase-js'));
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
const join = require(path.join(REPO, 'api/class/join.js'));
const create = require(path.join(REPO, 'api/teacher/create-class.js'));

const res = () => { const r = { code: null, body: null };
  r.status = c => { r.code = c; return r; }; r.json = b => { r.body = b; return r; }; return r; };

let classId = null;
async function cleanup() {
  if (classId) {
    await sb.from('class_members').delete().eq('class_id', classId);
    await sb.from('classes').delete().eq('id', classId);
    console.log('\ncleanup: test class removed');
  }
}

(async () => {
  const { data: teacher } = await sb.from('profiles')
    .select('id, full_name, school_id, role').eq('role', 'teacher').limit(1).single();
  const { data: subject } = await sb.from('subjects')
    .select('id').eq('slug', 'english-literature-aqa').single();
  const { data: student } = await sb.from('progress').select('person_id').limit(1).single();
  const realStudent = student.person_id;

  AUTH = { profile: teacher };
  let r = res();
  await create({ method: 'POST', headers: {}, body:
    { name: '__E2E_TEST__', subject_id: subject.id, year_group: 11 } }, r);
  classId = r.body.class.id;
  const code = r.body.class.joinCode;
  console.log('class created, code', code, '| instructions:', r.body.instructions);

  // 1. no token at all
  r = res();
  await join({ method: 'POST', headers: {}, body: { code: code } }, r);
  console.log('1. no token          ->', r.code, r.body.error);

  // 2. a token Supabase rejects (real verification path)
  r = res();
  await join({ method: 'POST', headers: { authorization: 'Bearer not.a.real.jwt' },
               body: { code: code } }, r);
  console.log('2. invalid token     ->', r.code, r.body.error);

  // 3. valid session; body also smuggles a DIFFERENT student_id — must be ignored
  FAKE_USER = realStudent;
  r = res();
  await join({ method: 'POST', headers: { authorization: 'Bearer good-token' },
               body: { code: code, student_id: '99999999-9999-9999-9999-999999999999' } }, r);
  console.log('3. valid session     ->', r.code, '| joined:', r.body.joined);

  const { data: mems } = await sb.from('class_members').select('student_id').eq('class_id', classId);
  const ids = (mems || []).map(m => m.student_id);
  console.log('   membership rows   :', ids.length);
  console.log('   is the TOKEN user :', ids[0] === realStudent, '(must be true)');
  console.log('   smuggled id used  :', ids.indexOf('99999999-9999-9999-9999-999999999999') !== -1, '(must be false)');
})().catch(e => console.log('FAILED:', e.message)).finally(cleanup);
