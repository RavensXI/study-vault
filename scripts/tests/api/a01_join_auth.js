/* Museum exhibit 1: the join endpoint takes identity from the TOKEN only.
   No token → 401; a token Supabase rejects → 401; a valid session joins the
   token's user even when the body smuggles a different student_id.
   Everything created is named __E2E_TEST__ and deleted at the end. */
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

const supaMod = require(path.join(REPO, 'api/pipeline/_lib/supabase.js'));
const realGetUser = supaMod.supabase.auth.getUser.bind(supaMod.supabase.auth);
let FAKE_USER = null;
supaMod.supabase.auth.getUser = async function (tok) {
  if (FAKE_USER && tok === 'good-token') {
    return { data: { user: { id: FAKE_USER } }, error: null };
  }
  return realGetUser(tok);
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
  t('setup: class created', r.code === 200 && r.body && r.body.class, 'code ' + r.code);
  classId = r.body.class.id;
  const code = r.body.class.joinCode;

  r = res();
  await join({ method: 'POST', headers: {}, body: { code: code } }, r);
  t('no token -> 401', r.code === 401, r.code + ' ' + (r.body && r.body.error));

  r = res();
  await join({ method: 'POST', headers: { authorization: 'Bearer not.a.real.jwt' },
               body: { code: code } }, r);
  t('invalid token -> 401', r.code === 401, r.code + ' ' + (r.body && r.body.error));

  FAKE_USER = realStudent;
  r = res();
  await join({ method: 'POST', headers: { authorization: 'Bearer good-token' },
               body: { code: code, student_id: '99999999-9999-9999-9999-999999999999' } }, r);
  t('valid session joins', r.code === 200 && !!(r.body && r.body.joined),
    r.code + ' joined:' + (r.body && r.body.joined));

  const { data: mems } = await sb.from('class_members').select('student_id').eq('class_id', classId);
  const ids = (mems || []).map(m => m.student_id);
  t('exactly one membership row', ids.length === 1, ids.length);
  t('member is the TOKEN user', ids[0] === realStudent);
  t('smuggled student_id ignored',
    ids.indexOf('99999999-9999-9999-9999-999999999999') === -1);
})().catch(e => { fails++; console.log('FAIL uncaught — ' + e.message); })
  .finally(async () => {
    await cleanup();
    console.log('a01: ' + fails + ' failure(s)');
    process.exit(fails ? 1 : 0);
  });
