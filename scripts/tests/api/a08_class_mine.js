/* Museum exhibit 8: /api/class/mine lists the token's classes and nothing else.
   No token → 401; a bad token → 401; a student in no class → empty list; after
   joining a __E2E_TEST__ class the list carries its name, subject and teacher,
   and never the join code. Everything created is deleted at the end. */
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
const mine = require(path.join(REPO, 'api/class/mine.js'));
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
    .select('id, name').eq('slug', 'english-literature-aqa').single();
  /* a uuid that is nobody: no memberships, so the list must come back empty */
  const freshStudent = '00000000-0000-4000-8000-' + String(Date.now()).slice(-12).padStart(12, '0');
  /* a real student for the join leg (class_members needs a real person) */
  const { data: student } = await sb.from('progress').select('person_id').limit(1).single();
  const realStudent = student.person_id;

  let r = res();
  await mine({ method: 'GET', headers: {} }, r);
  t('no token -> 401', r.code === 401, r.code);

  r = res();
  await mine({ method: 'GET', headers: { authorization: 'Bearer not.a.real.jwt' } }, r);
  t('invalid token -> 401', r.code === 401, r.code);

  FAKE_USER = freshStudent;
  r = res();
  await mine({ method: 'GET', headers: { authorization: 'Bearer good-token' } }, r);
  t('no classes -> empty list', r.code === 200 && Array.isArray(r.body.classes) && r.body.classes.length === 0,
    r.code + ' ' + JSON.stringify(r.body));

  AUTH = { profile: teacher };
  r = res();
  await create({ method: 'POST', headers: {}, body:
    { name: '__E2E_TEST__', subject_id: subject.id, year_group: 11 } }, r);
  t('setup: class created', r.code === 200 && r.body && r.body.class, 'code ' + r.code);
  classId = r.body.class.id;
  const code = r.body.class.joinCode;

  FAKE_USER = realStudent;
  r = res();
  await join({ method: 'POST', headers: { authorization: 'Bearer good-token' }, body: { code: code } }, r);
  t('setup: joined', r.code === 200 && r.body.joined, r.code);

  r = res();
  await mine({ method: 'GET', headers: { authorization: 'Bearer good-token' } }, r);
  const c = r.body && r.body.classes && r.body.classes.find(x => x.id === classId);
  t('after joining -> the class is listed', r.code === 200 && !!c, r.code + ' ' + (r.body && r.body.classes && r.body.classes.length));
  t('carries the class name', c && c.name === '__E2E_TEST__', c && c.name);
  t('carries the subject name', c && c.subject === subject.name, c && c.subject);
  t('carries the teacher name', c && c.teacher === teacher.full_name, c && c.teacher);
  t('never the join code', !JSON.stringify(r.body).includes(code));

  await cleanup();
  console.log('a08: ' + fails + ' failure(s)');
  process.exit(fails ? 1 : 0);
})().catch(async e => { console.log('FAIL uncaught — ' + e.message); await cleanup(); process.exit(1); });
