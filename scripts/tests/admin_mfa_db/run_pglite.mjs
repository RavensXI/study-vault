// LOCAL ONLY: PGlite (Postgres compiled to WASM, in this node process, in memory).
// Tests supabase/migrations/20260929200000_admin_mfa.sql and its rollback against the live
// definitions written by hand in 01_schema_before.sql. No network, no production.
import { PGlite } from '@electric-sql/pglite';
import fs from 'node:fs';
import path from 'node:path';

const HERE = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const REPO = process.argv[2];
const MIG = path.join(REPO, 'supabase/migrations/20260929200000_admin_mfa.sql');
const RB = path.join(REPO, 'supabase/migrations/20260929200000_admin_mfa.rollback.sql');
const read = (p) => fs.readFileSync(p, 'utf8');

// PGlite has no pgcrypto loaded here: the one use (a random invitation token default) gets a
// stand-in with the same signature. Everything else in the stub is as in 00_supabase_stub.sql.
const stub = read(path.join(HERE, '00_supabase_stub.sql')).replace(
  'CREATE EXTENSION pgcrypto WITH SCHEMA extensions;',
  () => "CREATE FUNCTION extensions.gen_random_bytes(n int) RETURNS bytea LANGUAGE sql AS $$ SELECT decode(md5(random()::text) || md5(random()::text), 'hex') $$;");   // a function: '$$' in a replacement string means '$'

const db = new PGlite();
await db.exec(stub);
await db.exec(read(path.join(HERE, '01_schema_before.sql')));
await db.exec(read(path.join(HERE, '02_seed.sql')));

const ids = (i) => `00000000-0000-0000-0000-00000000000${i}`;
const WHO = [['Tom (platform_admin) aal1', ids(1), 'aal1'], ['Tom (platform_admin) aal2', ids(1), 'aal2'],
  ['Teacher T1 school A aal1', ids(2), 'aal1'], ['Teacher T2 school B aal1', ids(3), 'aal1'], ['Pupil P1 aal1', ids(4), 'aal1']];

async function probe(uid, aal) {
  return db.transaction(async (tx) => {
    await tx.query('set local role authenticated');
    await tx.query("select set_config('request.jwt.claims', $1, true)", [JSON.stringify({ sub: uid, role: 'authenticated', aal })]);
    const r = (await tx.query(`select public.is_platform_admin() as admin,
      (select count(*) from public.classes)::int as classes, (select count(*) from public.class_members)::int as members,
      (select count(*) from public.lessons where status <> 'live')::int as unpublished,
      (select count(*) from public.subjects where school_id is not null)::int as school_subjects,
      (select count(*) from public.profiles)::int as profiles,
      public.teacher_manages_subject('5bbbbbbb-0000-0000-0000-000000000000') as manages_b`)).rows[0];
    const inv = (await tx.query(`select public.create_teacher_invitation('x-${aal}-${Math.random()}@test') as j`)).rows[0].j;
    r.invite = inv.success ? 'ok' : inv.error;
    await tx.rollback();
    return r;
  });
}

async function matrix(label) {
  console.log('\n== ' + label);
  const out = {};
  for (const [name, uid, aal] of WHO) {
    const p = await probe(uid, aal); out[name] = p;
    console.log('  ' + name.padEnd(28) + Object.entries(p).map(([k, v]) => `${k}=${v}`).join(' '));
  }
  return out;
}

const before = await matrix('BEFORE (as live today)');
let t = performance.now(); await db.exec(read(MIG)); const ms = performance.now() - t;
const after = await matrix(`AFTER migration (${ms.toFixed(1)} ms end to end)`);
t = performance.now(); await db.exec(read(RB)); const msRb = performance.now() - t;
const back = await matrix(`AFTER rollback (${msRb.toFixed(1)} ms)`);
await db.exec(read(MIG));
const fin = await matrix('AFTER migration applied again');

// the migration runs its timeouts (they must be set, and scoped to the transaction)
const lt = (await db.query("select current_setting('lock_timeout') as lt, current_setting('statement_timeout') as st")).rows[0];

const expect = {
  'Tom (platform_admin) aal1': { admin: false, classes: 1, members: 1, school_subjects: 1, profiles: 1, manages_b: false, invite: 'Sign in with your two-factor code first' },
  'Tom (platform_admin) aal2': { admin: true, classes: 2, members: 2, school_subjects: 2, profiles: 5, manages_b: true, invite: 'ok' },
  'Teacher T1 school A aal1': { admin: false, classes: 1, members: 1, manages_b: false },
  'Teacher T2 school B aal1': { admin: false, classes: 1, members: 1, manages_b: false },
  'Pupil P1 aal1': { admin: false, classes: 0, members: 1, unpublished: 0 },
};
const bad = [];
for (const [who, exp] of Object.entries(expect)) for (const [k, v] of Object.entries(exp)) if (fin[who][k] !== v) bad.push(`${who} ${k}: got ${fin[who][k]} want ${v}`);
for (const who of Object.keys(before)) {
  if (!who.startsWith('Tom') && JSON.stringify(before[who]) !== JSON.stringify(after[who])) bad.push('changed for ' + who);
  if (JSON.stringify(before[who]) !== JSON.stringify(back[who])) bad.push('rollback differs for ' + who);
}
if (lt.lt !== '0' || lt.st !== '0') bad.push(`timeouts leaked out of the transaction: ${JSON.stringify(lt)}`);
console.log(`\nsession timeouts after the migration committed: lock_timeout=${lt.lt} statement_timeout=${lt.st} (0 = the SET LOCALs ended with the transaction)`);
console.log('RESULT: ' + (bad.length ? 'FAIL' : 'PASS'));
bad.forEach((b) => console.log('  - ' + b));
await db.close();
process.exit(bad.length ? 1 : 0);
