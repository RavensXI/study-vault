/* Museum exhibits 1+3 end to end: create -> student joins with the code
   (token identity — this harness carries the auth monkeypatch the original
   predated) -> messy re-entry dedupes -> owning teacher sees the class ->
   a different teacher gets 403. Writes only __E2E_TEST__ rows; deletes them
   on exit, including on failure. */
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
const create = require(path.join(REPO, 'api/teacher/create-class.js'));
const join = require(path.join(REPO, 'api/class/join.js'));
const progress = require(path.join(REPO, 'api/teacher/class-progress.js'));

const res = () => { const r = { code: null, body: null };
  r.status = c => { r.code = c; return r; }; r.json = b => { r.body = b; return r; }; return r; };

let newClassId = null;
async function cleanup() {
  if (newClassId) {
    await sb.from('class_members').delete().eq('class_id', newClassId);
    await sb.from('classes').delete().eq('id', newClassId);
    const { data } = await sb.from('classes').select('id').eq('id', newClassId);
    t('cleanup: test class removed', (data || []).length === 0);
  }
}

(async () => {
  const { data: teacher } = await sb.from('profiles')
    .select('id, full_name, school_id, role').eq('role', 'teacher').limit(1).single();
  const { data: subject } = await sb.from('subjects')
    .select('id, name').eq('slug', 'english-literature-aqa').single();
  const { data: student } = await sb.from('progress').select('person_id').limit(1).single();
  const studentId = student.person_id;

  AUTH = { profile: teacher };
  let r = res();
  await create({ method: 'POST', headers: {}, body:
    { name: '__E2E_TEST__', subject_id: subject.id, year_group: 11 } }, r);
  t('create -> 200', r.code === 200, r.code + ' ' + JSON.stringify(r.body).slice(0, 60));
  if (r.code !== 200) throw new Error('create failed, aborting');
  newClassId = r.body.class.id;
  const code = r.body.class.joinCode;
  t('code is 6 chars, no ambiguous ILOU01',
    code.length === 6 && !/[ILOU01]/.test(code), code);

  FAKE_USER = studentId;
  const authed = { authorization: 'Bearer good-token' };
  r = res();
  await join({ method: 'POST', headers: authed, body: { code: code } }, r);
  t('student joins -> 200', r.code === 200, r.code);
  t('join names the class back', !!(r.body && r.body.class && r.body.class.name));

  const messy = (code.slice(0, 3) + ' ' + code.slice(3)).toLowerCase();
  r = res();
  await join({ method: 'POST', headers: authed, body: { code: messy } }, r);
  t('messy re-entry -> alreadyIn, no duplicate',
    r.code === 200 && r.body.alreadyIn === true, r.code + ' alreadyIn:' + (r.body || {}).alreadyIn);
  const { data: mems } = await sb.from('class_members').select('student_id').eq('class_id', newClassId);
  t('membership stays one row', (mems || []).length === 1, (mems || []).length);

  r = res();
  await progress({ method: 'GET', headers: {}, query: { class_id: newClassId }, body: {} }, r);
  t('owning teacher opens the class -> 200', r.code === 200, r.code);
  t('progress reports size 1', r.body && r.body.size === 1, (r.body || {}).size);
  t('progress is subject-scoped', !!(r.body && r.body.class && r.body.class.subject));

  const { data: other } = await sb.from('profiles')
    .select('id, role, school_id').eq('role', 'teacher').neq('id', teacher.id).limit(1).single();
  AUTH = { profile: other };
  r = res();
  await progress({ method: 'GET', headers: {}, query: { class_id: newClassId }, body: {} }, r);
  t('a different teacher -> 403', r.code === 403, r.code);
})().catch(e => { fails++; console.log('FAIL uncaught — ' + e.message); })
  .finally(async () => {
    await cleanup();
    console.log('a06: ' + fails + ' failure(s)');
    process.exit(fails ? 1 : 0);
  });
