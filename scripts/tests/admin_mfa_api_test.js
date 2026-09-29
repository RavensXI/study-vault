/**
 * Admin two-factor sign-in: API tests with NO network (29 Sep 2026).
 *
 * Runs the real route handlers in node with the Supabase client and fetch stubbed. A "token" is
 * a real-shaped JWT whose payload carries sub + aal; the stub's auth.getUser() accepts any token
 * it issued. So this proves each route's decision: aal1 admin -> refused, aal2 admin -> allowed,
 * the old X-Admin-Password -> refused, teachers unaffected.
 *
 *   node scripts/tests/admin_mfa_api_test.js
 */
const path = require('path');
const Module = require('module');
const ROOT = path.join(__dirname, '..', '..');

process.env.SUPABASE_URL = 'https://stub.invalid';
process.env.SUPABASE_SERVICE_KEY = 'stub-service-key';
process.env.ADMIN_PASSWORD = 'the-old-shared-password';
process.env.CRON_SECRET = 'cron-secret';

// ---- people ----
const TOM = '00000000-0000-0000-0000-000000000001', TEACHER = '00000000-0000-0000-0000-000000000002';
const PROFILES = {
  [TOM]: { id: TOM, role: 'platform_admin', school_id: 'school-a', full_name: 'Tom' },
  [TEACHER]: { id: TEACHER, role: 'teacher', school_id: 'school-a', full_name: 'Teacher' },
};
const b64 = (o) => Buffer.from(JSON.stringify(o)).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const token = (sub, aal) => b64({ alg: 'HS256' }) + '.' + b64({ sub, aal, role: 'authenticated' }) + '.sig';

// ---- a Supabase client stub: any query chain resolves to empty rows; profiles by id ----
function chain(table) {
  const st = { table, filters: {} };
  const result = () => {
    if (table === 'profiles' && st.filters.id) return { data: PROFILES[st.filters.id] || null, error: null };
    if (table === 'schools') return { data: { id: 'school-a' }, error: null };
    return { data: [], error: null, count: 0 };
  };
  const p = new Proxy(function () {}, {
    get(_, k) {
      if (k === 'then') { const r = result(); const v = st.single ? r : (Array.isArray(r.data) || r.data === null ? r : { data: [r.data], error: null }); return (res) => res(v); }
      if (k === 'single' || k === 'maybeSingle') return () => { st.single = true; return p; };
      if (k === 'eq') return (col, val) => { st.filters[col] = val; return p; };
      return () => p;
    },
  });
  return p;
}
const stubClient = {
  from: (t) => chain(t),
  rpc: () => Promise.resolve({ data: null, error: null }),
  auth: {
    getUser: async (tok) => {
      try {
        const c = JSON.parse(Buffer.from(String(tok).split('.')[1], 'base64').toString());
        if (PROFILES[c.sub]) return { data: { user: { id: c.sub, email: c.sub + '@test' } }, error: null };
      } catch (e) {}
      return { data: { user: null }, error: { message: 'invalid' } };
    },
  },
  storage: { from: () => ({ upload: async () => ({}), getPublicUrl: () => ({ data: {} }) }) },
};
const origLoad = Module._load;
Module._load = function (req, parent, isMain) {
  if (/pipeline[\\/]_lib[\\/]supabase$|[\\/]_lib[\\/]supabase$/.test(req) || req.endsWith('/supabase') && req.startsWith('.')) return { supabase: stubClient };
  if (req === '@supabase/supabase-js') return { createClient: () => stubClient };
  return origLoad.apply(this, arguments);
};
global.fetch = async () => ({ ok: true, status: 200, headers: new Map([['content-type', 'application/json']]), text: async () => '[]', json: async () => [] });

// ---- a tiny req/res ----
async function call(file, { method = 'GET', headers = {}, query = {}, body } = {}) {
  const h = require(path.join(ROOT, file));
  let status = 200;
  const res = {
    statusCode: 200, headers: {},
    setHeader(k, v) { this.headers[k] = v; }, getHeader(k) { return this.headers[k]; },
    status(c) { status = c; this.statusCode = c; return this; },
    json() { return this; }, send() { return this; }, end() { return this; },
  };
  const lower = {}; Object.keys(headers).forEach((k) => (lower[k.toLowerCase()] = headers[k]));
  await h({ method, headers: lower, query, body: body || {}, url: '/' }, res);
  return status;
}

const A1 = { authorization: 'Bearer ' + token(TOM, 'aal1') };
const A2 = { authorization: 'Bearer ' + token(TOM, 'aal2') };
const T1 = { authorization: 'Bearer ' + token(TEACHER, 'aal1') };
const PW = { 'x-admin-password': process.env.ADMIN_PASSWORD };
const ADMIN_ROUTES = ['api/admin/bug-reports.js', 'api/admin/practice-qa-flags.js', 'api/admin/recall-appeals.js',
  'api/admin/school-submissions.js', 'api/admin/simplify-flags.js', 'api/admin/subject-requests.js'];

const rows = [];
async function expect(label, file, opts, want) {
  let got;
  try { got = await call(file, opts); } catch (e) { got = 'threw: ' + e.message.split('\n')[0]; }
  const ok = Array.isArray(want) ? want.includes(got) : got === want;
  rows.push({ ok, label, file, got, want });
}

(async () => {
  for (const f of ADMIN_ROUTES) {
    await expect('admin aal1', f, { headers: A1 }, 401);
    await expect('admin aal2', f, { headers: A2 }, 200);
    await expect('old X-Admin-Password', f, { headers: PW }, 401);
    await expect('teacher', f, { headers: T1 }, 401);
    await expect('no sign-in', f, {}, 401);
  }
  const STAFF = { query: { p: 'subjects?select=id&limit=1' } };
  await expect('admin aal1', 'api/staff/rest.js', { ...STAFF, headers: A1 }, 403);
  await expect('admin aal2', 'api/staff/rest.js', { ...STAFF, headers: A2 }, 200);
  await expect('old X-Admin-Password', 'api/staff/rest.js', { ...STAFF, headers: PW }, 401);
  await expect('teacher', 'api/staff/rest.js', { ...STAFF, headers: T1 }, 403);
  await expect('password login', 'api/auth/login.js', { method: 'POST', body: { password: process.env.ADMIN_PASSWORD } }, 410);
  await expect('school code login', 'api/auth/login.js', { method: 'POST', body: { code: 'x' } }, 410);
  await expect('admin aal1', 'api/auth/invite-teacher.js', { method: 'POST', headers: A1, body: { email: 'x@test' } }, 401);
  await expect('old X-Admin-Password', 'api/auth/invite-teacher.js', { method: 'POST', headers: PW, body: { email: 'x@test' } }, 401);
  await expect('admin aal2 (passes auth; stub then fails the school lookup)', 'api/auth/invite-teacher.js', { method: 'POST', headers: A2, body: { email: 'x@test' } }, [200, 400, 404, 500]);
  for (const f of ['api/cron/weekly-digest.js', 'api/cron/weekly-reads.js']) {
    await expect('admin aal1 manual run', f, { headers: A1 }, 401);
    await expect('old X-Admin-Password', f, { headers: PW }, 401);
    await expect('Vercel cron secret', f, { headers: { authorization: 'Bearer cron-secret' } }, 200);
  }
  // requireTeacher: the teacher routes keep working at aal1, for teachers and for Tom (as a teacher)
  const { requireTeacher } = require(path.join(ROOT, 'api/pipeline/_lib/auth.js'));
  const fakeRes = { status() { return this; }, json() { return this; } };
  const r1 = await requireTeacher({ headers: A1 }, fakeRes), r2 = await requireTeacher({ headers: A2 }, fakeRes);
  const rt = await requireTeacher({ headers: T1 }, fakeRes), rp = await requireTeacher({ headers: PW }, fakeRes);
  rows.push({ ok: r1 && r1.profile.role === 'teacher', label: 'requireTeacher: Tom aal1 is treated as a teacher', file: 'api/pipeline/_lib/auth.js', got: r1 && r1.profile.role, want: 'teacher' });
  rows.push({ ok: r2 && r2.profile.role === 'platform_admin', label: 'requireTeacher: Tom aal2 is admin', file: 'api/pipeline/_lib/auth.js', got: r2 && r2.profile.role, want: 'platform_admin' });
  rows.push({ ok: rt && rt.profile.role === 'teacher', label: 'requireTeacher: teacher aal1 unaffected', file: 'api/pipeline/_lib/auth.js', got: rt && rt.profile.role, want: 'teacher' });
  rows.push({ ok: rp === null, label: 'requireTeacher: old password refused', file: 'api/pipeline/_lib/auth.js', got: rp === null ? 'refused' : 'accepted', want: 'refused' });
  const { isPlatformAdmin: isAdmin } = require(path.join(ROOT, 'api/pipeline/_lib/scope.js'));
  if (typeof isAdmin === 'function') {
    rows.push({ ok: isAdmin(r1) === false, label: 'scope.isPlatformAdmin: Tom aal1', file: 'api/pipeline/_lib/scope.js', got: isAdmin(r1), want: false });
    rows.push({ ok: isAdmin(r2) === true, label: 'scope.isPlatformAdmin: Tom aal2', file: 'api/pipeline/_lib/scope.js', got: isAdmin(r2), want: true });
  }

  let fail = 0;
  for (const r of rows) { if (!r.ok) fail++; console.log((r.ok ? 'PASS ' : 'FAIL ') + r.label.padEnd(58) + ' ' + r.file.padEnd(36) + ' got ' + r.got + (r.ok ? '' : ' want ' + r.want)); }
  console.log(`\n${rows.length} checks, ${fail} failed`);
  process.exit(fail ? 1 : 0);
})();
