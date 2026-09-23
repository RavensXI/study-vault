const { supabase } = require('../pipeline/_lib/supabase');

/**
 * The safeguarding lead's view of the concerns the safeguarding check kept
 * (api/_lib/safeguard.js, table safeguarding_alerts).
 *
 * WHO MAY READ. A signed-in member of staff whose account email is the school's
 * lead_email or one of its deputy_emails in schools.settings.safeguarding.
 * Nobody else: not the pupil's teacher, not a school admin, not the admin
 * password. Identity comes from the bearer token only.
 *
 *   GET                         -> { schools: [{ id, name }], alerts: [...] }
 *   POST { id, note }           -> marks one alert reviewed; it is deleted 90 days later
 */
const KEEP_DAYS = 90;

async function leadSchools(req) {
  const h = req.headers.authorization || '';
  if (!h.startsWith('Bearer ')) return null;
  const { data, error } = await supabase.auth.getUser(h.slice(7));
  if (error || !data || !data.user) return null;
  const email = String(data.user.email || '').trim().toLowerCase();
  if (!email) return { userId: data.user.id, schools: [] };
  const { data: schools } = await supabase.from('schools').select('id, name, settings');
  const mine = (schools || []).filter(s => {
    const sg = (s.settings && s.settings.safeguarding) || {};
    return [sg.lead_email].concat(sg.deputy_emails || []).some(e => String(e || '').trim().toLowerCase() === email);
  });
  return { userId: data.user.id, schools: mine.map(s => ({ id: s.id, name: s.name })) };
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  const who = await leadSchools(req);
  if (!who) return res.status(401).json({ error: 'Sign in first.' });
  if (!who.schools.length) return res.status(403).json({ error: 'This page is for a school’s safeguarding lead and deputies.' });
  const ids = who.schools.map(s => s.id);

  if (req.method === 'POST') {
    const b = req.body || {};
    const id = String(b.id || '');
    const note = String(b.note || '').slice(0, 1000).trim() || null;
    const { data: row } = await supabase.from('safeguarding_alerts').select('id, school_id, status').eq('id', id).maybeSingle();
    if (!row || ids.indexOf(row.school_id) < 0) return res.status(404).json({ error: 'That concern is not one of yours.' });
    const now = new Date();
    const { error } = await supabase.from('safeguarding_alerts').update({
      status: 'reviewed', reviewed_by: who.userId, reviewed_at: now.toISOString(), review_note: note,
      delete_after: new Date(now.getTime() + KEEP_DAYS * 86400000).toISOString()
    }).eq('id', id);
    if (error) return res.status(500).json({ error: 'Could not save that.' });
    return res.status(200).json({ ok: true });
  }
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const { data: alerts, error } = await supabase.from('safeguarding_alerts')
    .select('id, school_id, student_id, source, page, context, body, decision, category, reason, status, reviewed_at, review_note, reviewed_by, created_at')
    .in('school_id', ids).order('created_at', { ascending: false }).limit(200);
  if (error) return res.status(500).json({ error: 'Could not read the concerns.' });
  const list = alerts || [];

  // the pupil's name and their classes at that school, and who reviewed each one
  const people = Array.from(new Set(list.map(a => a.student_id).concat(list.map(a => a.reviewed_by)).filter(Boolean)));
  const pupils = Array.from(new Set(list.map(a => a.student_id).filter(Boolean)));
  const [{ data: profs }, { data: mem }] = await Promise.all([
    people.length ? supabase.from('profiles').select('id, full_name, email').in('id', people) : Promise.resolve({ data: [] }),
    pupils.length ? supabase.from('class_members').select('student_id, classes(name, school_id)').in('student_id', pupils) : Promise.resolve({ data: [] })
  ]);
  const name = {}; (profs || []).forEach(p => { name[p.id] = p.full_name || p.email || 'A pupil'; });
  const classesOf = {};
  (mem || []).forEach(m => { if (m.classes) (classesOf[m.student_id + '|' + m.classes.school_id] = classesOf[m.student_id + '|' + m.classes.school_id] || []).push(m.classes.name); });

  return res.status(200).json({
    schools: who.schools,
    alerts: list.map(a => ({
      id: a.id, school_id: a.school_id, created_at: a.created_at, source: a.source, page: a.page,
      pupil: a.student_id ? (name[a.student_id] || 'A pupil') : 'A pupil whose account has been deleted',
      classes: (classesOf[a.student_id + '|' + a.school_id] || []).sort(),
      context: a.context, body: a.body, decision: a.decision, category: a.category, reason: a.reason,
      status: a.status, reviewed_at: a.reviewed_at, review_note: a.review_note,
      reviewed_by: a.reviewed_by ? (name[a.reviewed_by] || null) : null
    }))
  });
};
