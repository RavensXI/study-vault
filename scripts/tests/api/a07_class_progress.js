/* Museum exhibit 3: class-progress shape, privacy, and the ownership rule.
   Aggregation VALUES vary with live data and stay unasserted — the contract
   is: platform_admin gets the full shape, private localStorage key names and
   raw timestamps never leak, the class's own teacher gets 200, a different
   teacher and another school's admin get 403. Read-only. */
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

  console.log('a07: ' + fails + ' failure(s)');
  process.exit(fails ? 1 : 0);
})().catch(e => { console.log('FAIL uncaught — ' + e.message); process.exit(1); });
