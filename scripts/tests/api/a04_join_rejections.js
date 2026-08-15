/* Join + create-class rejection paths. Every case returns before any insert
   — this writes nothing. The contract: student mistakes get a 4xx and an
   error message; never a 200, never a 500. */
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

const join = require(path.join(REPO, 'api/class/join.js'));
const create = require(path.join(REPO, 'api/teacher/create-class.js'));

const res = () => { const r = { code: null, body: null };
  r.status = c => { r.code = c; return r; }; r.json = b => { r.body = b; return r; }; return r; };

(async () => {
  const joinCases = [
    ['empty code', { code: '' }],
    ['O typed for Q', { code: 'ABCO34' }],
    ['zero typed', { code: 'ABC034' }],
    ['1 typed for J', { code: 'ABC134' }],
    ['too short', { code: 'ABC2' }],
    ['spaces and hyphen', { code: 'ab c-234' }],
    ['well formed, no match', { code: 'ZZZZZZ' }],
  ];
  for (const [label, body] of joinCases) {
    const r = res();
    await join({ method: 'POST', body: body, headers: {} }, r);
    t('join: ' + label + ' -> 4xx + error',
      r.code >= 400 && r.code < 500 && !!(r.body && r.body.error),
      r.code + ' ' + String((r.body || {}).error).slice(0, 50));
  }

  AUTH = { profile: { id: 'teach-1', role: 'teacher', school_id: null } };
  const createCases = [
    ['no name', { name: '', subject_id: 'x' }],
    ['no subject', { name: '10 Set 1', subject_id: '' }],
    ['name too long', { name: 'x'.repeat(41), subject_id: 'x' }],
    ['unknown subject', { name: '10 Set 1', subject_id: '00000000-0000-0000-0000-000000000000' }],
  ];
  for (const [label, body] of createCases) {
    const r = res();
    await create({ method: 'POST', body: body, headers: {} }, r);
    t('create: ' + label + ' -> 4xx + error',
      r.code >= 400 && r.code < 500 && !!(r.body && r.body.error),
      r.code + ' ' + String((r.body || {}).error).slice(0, 50));
  }

  const r = res();
  await create({ method: 'GET', body: {}, headers: {} }, r);
  t('create: GET -> 405', r.code === 405, r.code);

  console.log('a04: ' + fails + ' failure(s)');
  process.exit(fails ? 1 : 0);
})().catch(e => { console.log('FAIL uncaught — ' + e.message); process.exit(1); });
