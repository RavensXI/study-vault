/* Exercises the REJECTION paths only. Every case below returns before any
   insert, so this writes nothing to the live database. The happy path cannot be
   tested until scripts/_create_class_join_codes.sql has been run — the
   join_code column does not exist yet. */
const path = require('path');
const REPO = 'C:/Users/tshau/Documents/Study Vault';

const authPath = require.resolve(path.join(REPO, 'api/pipeline/_lib/auth.js'));
let AUTH = null;
require.cache[authPath] = { id: authPath, filename: authPath, loaded: true,
  exports: { requireTeacher: async () => AUTH } };

const join = require(path.join(REPO, 'api/class/join.js'));
const create = require(path.join(REPO, 'api/teacher/create-class.js'));

const res = () => { const r = { code: null, body: null };
  r.status = c => { r.code = c; return r; }; r.json = b => { r.body = b; return r; }; return r; };

(async () => {
  console.log('=== JOIN: what a student can get wrong ===');
  const cases = [
    ['no code at all',        { code: '',        student_id: 'stu' }],
    ['not signed in',         { code: 'ABC234',  student_id: null  }],
    ['typed O for Q',         { code: 'ABCO34',  student_id: 'stu' }],
    ['typed 0 (zero)',        { code: 'ABC034',  student_id: 'stu' }],
    ['typed 1 for J',         { code: 'ABC134',  student_id: 'stu' }],
    ['too short',             { code: 'ABC2',    student_id: 'stu' }],
    ['spaces and a hyphen',   { code: 'ab c-234',student_id: 'stu' }],
    ['well formed, no match', { code: 'ZZZZZZ',  student_id: 'stu' }]
  ];
  for (const [label, body] of cases) {
    const r = res();
    await join({ method: 'POST', body: body, headers: {} }, r);
    console.log('  ' + label.padEnd(24) + r.code + '  ' + String((r.body || {}).error || 'OK').slice(0, 74));
  }

  console.log('');
  console.log('=== CREATE CLASS: teacher input ===');
  AUTH = { profile: { id: 'teach-1', role: 'teacher', school_id: null } };
  const cc = [
    ['no name',        { name: '',        subject_id: 'x' }],
    ['no subject',     { name: '10 Set 1', subject_id: '' }],
    ['name too long',  { name: 'x'.repeat(41), subject_id: 'x' }],
    ['unknown subject',{ name: '10 Set 1', subject_id: '00000000-0000-0000-0000-000000000000' }]
  ];
  for (const [label, body] of cc) {
    const r = res();
    await create({ method: 'POST', body: body, headers: {} }, r);
    console.log('  ' + label.padEnd(24) + r.code + '  ' + String((r.body || {}).error || 'OK').slice(0, 74));
  }

  const r = res();
  await create({ method: 'GET', body: {}, headers: {} }, r);
  console.log('  ' + 'GET not allowed'.padEnd(24) + r.code);
})();
