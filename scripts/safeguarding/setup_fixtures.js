/* Safeguarding route set-up (23 Sep 2026). Idempotent: safe to run again.
     node scripts/safeguarding/setup_fixtures.js
   1. Unity College: safeguarding contacts (lead Bev Worthington). Merged into
      schools.settings; no other key is touched.
   2. "Safeguarding Test School" whose lead is Tom (t.shaun@unity.lancs.sch.uk),
      a test teacher who is NOT a lead, a test class, and a test pupil in it.
   Logins are written to scripts/safeguarding/fixtures.json (git-ignored values are
   test-only accounts on a test school with no real pupils). */
const crypto = require('crypto');
const fs = require('fs');
const { supabase } = require('../../api/pipeline/_lib/supabase');

async function one(q) { const { data, error } = await q; if (error) throw new Error(error.message); return data; }

async function user(email, fullName, role, schoolId) {
  const { data: list } = await supabase.auth.admin.listUsers({ page: 1, perPage: 1000 });
  let u = (list && list.users || []).find(x => String(x.email).toLowerCase() === email);
  const password = 'Sg-' + crypto.randomBytes(6).toString('hex') + '!';
  if (u) await supabase.auth.admin.updateUserById(u.id, { password });
  else {
    const { data, error } = await supabase.auth.admin.createUser({ email, password, email_confirm: true, user_metadata: { full_name: fullName } });
    if (error) throw new Error(error.message); u = data.user;
  }
  await one(supabase.from('profiles').upsert({ id: u.id, email, full_name: fullName, role, school_id: schoolId, is_demo: true }, { onConflict: 'id' }));
  return { id: u.id, email, password };
}

(async () => {
  // 1. Unity
  const unity = (await one(supabase.from('schools').select('id, settings').eq('slug', 'unity-college')))[0];
  const us = Object.assign({}, unity.settings || {}, { safeguarding: { lead_name: 'Bev Worthington', lead_email: 'b.worthington@unity.lancs.sch.uk', deputy_emails: [] } });
  await one(supabase.from('schools').update({ settings: us }).eq('id', unity.id));
  console.log('Unity safeguarding contacts set');

  // 2. the test school
  let school = (await one(supabase.from('schools').select('id').eq('slug', 'safeguarding-test')))[0];
  const settings = { safeguarding: { lead_name: 'Tom Shaun (test)', lead_email: 't.shaun@unity.lancs.sch.uk', deputy_emails: [] } };
  if (!school) school = (await one(supabase.from('schools').insert({ name: 'Safeguarding Test School', slug: 'safeguarding-test', settings }).select('id')))[0];
  else await one(supabase.from('schools').update({ settings }).eq('id', school.id));
  const teacher = await user('sg-test-teacher@demo.studyvault.co.uk', 'Test Teacher', 'teacher', school.id);
  const pupil = await user('sg-test-pupil@demo.studyvault.co.uk', 'Test Pupil', 'student', null);
  let cls = (await one(supabase.from('classes').select('id').eq('school_id', school.id).eq('name', 'Test 11A')))[0];
  if (!cls) cls = (await one(supabase.from('classes').insert({ school_id: school.id, teacher_id: teacher.id, name: 'Test 11A', year_group: 11, join_open: false }).select('id')))[0];
  await one(supabase.from('class_members').upsert({ class_id: cls.id, student_id: pupil.id }, { onConflict: 'class_id,student_id' }));
  const out = { school_id: school.id, class_id: cls.id, lead_email: 't.shaun@unity.lancs.sch.uk (your own login)', teacher, pupil };
  fs.writeFileSync(__dirname + '/fixtures.json', JSON.stringify(out, null, 1));
  console.log('test school, teacher, class and pupil ready; logins in scripts/safeguarding/fixtures.json');
})().catch(e => { console.error(e); process.exit(1); });
