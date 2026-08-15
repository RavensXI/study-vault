/* my-classes: a teacher gets their own classes with join codes and sizes,
   plus the subjects they may create against. Read-only; picks any teacher
   who owns at least one class rather than a hardcoded id. */
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
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
const h = require(path.join(REPO, 'api/teacher/my-classes.js'));

const res = () => { const r = { code: null, body: null };
  r.status = c => { r.code = c; return r; }; r.json = b => { r.body = b; return r; }; return r; };

(async () => {
  const { data: cls } = await sb.from('classes')
    .select('teacher_id').not('name', 'like', '__E2E_TEST__%').limit(1).single();
  const { data: teacher } = await sb.from('profiles')
    .select('id, full_name, role, school_id').eq('id', cls.teacher_id).single();

  AUTH = { profile: teacher };
  const r = res();
  await h({ method: 'GET', headers: {}, query: {}, body: {} }, r);
  t('own classes -> 200', r.code === 200, r.code);
  const b = r.body || {};
  t('classes array returned', Array.isArray(b.classes) && b.classes.length >= 1,
    (b.classes || []).length);
  const c = (b.classes || [])[0] || {};
  t('class carries a join code', typeof c.joinCode === 'string' && c.joinCode.length === 6,
    c.joinCode);
  t('class carries a size', typeof c.size === 'number');
  t('subjects offered', Array.isArray(b.subjects) && b.subjects.length >= 1,
    (b.subjects || []).length);

  console.log('a05: ' + fails + ' failure(s)');
  process.exit(fails ? 1 : 0);
})().catch(e => { console.log('FAIL uncaught — ' + e.message); process.exit(1); });
