/* Adds a test deputy lead to the test school (sg-test-lead@demo.studyvault.co.uk) so the
   review page can be checked in a browser without Tom's own password. Idempotent. */
const crypto = require('crypto'); const fs = require('fs');
const { supabase } = require('../../api/pipeline/_lib/supabase');
(async () => {
  const fx = require('./fixtures.json');
  const email = 'sg-test-lead@demo.studyvault.co.uk', password = 'Sg-' + crypto.randomBytes(6).toString('hex') + '!';
  const { data: list } = await supabase.auth.admin.listUsers({ page: 1, perPage: 1000 });
  let u = (list.users || []).find(x => String(x.email).toLowerCase() === email);
  if (u) await supabase.auth.admin.updateUserById(u.id, { password });
  else u = (await supabase.auth.admin.createUser({ email, password, email_confirm: true, user_metadata: { full_name: 'Test Lead' } })).data.user;
  await supabase.from('profiles').upsert({ id: u.id, email, full_name: 'Test Lead', role: 'teacher', school_id: fx.school_id, is_demo: true }, { onConflict: 'id' });
  const { data: s } = await supabase.from('schools').select('settings').eq('id', fx.school_id).single();
  const sg = Object.assign({}, s.settings.safeguarding); sg.deputy_emails = [email];
  await supabase.from('schools').update({ settings: Object.assign({}, s.settings, { safeguarding: sg }) }).eq('id', fx.school_id);
  fx.lead = { id: u.id, email, password }; fs.writeFileSync(__dirname + '/fixtures.json', JSON.stringify(fx, null, 1));
  console.log('test deputy lead ready');
})().catch(e => { console.error(e); process.exit(1); });
