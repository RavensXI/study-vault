/**
 * Monday morning: write each class's weekly read and email it to the teacher.
 *
 * Scheduled daily via vercel.json (Hobby-safe); it only runs the class loop on
 * Mondays (UTC) unless triggered by hand. Manual triggers, with the admin
 * password:
 *   GET /api/cron/weekly-reads                       every class, now
 *   GET /api/cron/weekly-reads?class_id=<id>         one class, now
 *   GET /api/cron/weekly-reads?class_id=<id>&dry=1   show the packet, call no model
 *   &force=1                                          ignore the 6-answer floor and rewrite this week's read
 *
 * Auth as weekly-digest.js: Vercel Cron sends Bearer CRON_SECRET; a person
 * sends X-Admin-Password. Fails closed without either.
 *
 * The read itself lives in api/teacher/_lib/weekly-read.js (packet, prompt,
 * cost cap, storage). This file only loops, emails and reports.
 */
const { supabase } = require('../pipeline/_lib/supabase');
const { runRead, mondayOf } = require('../teacher/_lib/weekly-read');
const { computeClassProgress, snapshotOf } = require('../teacher/class-progress');
const { baseSubject } = require('../teacher/_lib/scope');
const { sendEmail, escHtml } = require('../_lib/notify');

const BASE = 'https://www.studyvault.co.uk';

function authorize(req) {
  const secret = process.env.CRON_SECRET;
  const auth = req.headers['authorization'] || '';
  if (secret && auth === 'Bearer ' + secret) return { ok: true, manual: false };
  const pw = req.headers['x-admin-password'];
  if (pw && process.env.ADMIN_PASSWORD && pw === process.env.ADMIN_PASSWORD) return { ok: true, manual: true };
  return { ok: false };
}

/* Markdown-lite -> email HTML: **bold** headings, "- " bullets, paragraphs */
function mdToHtml(md) {
  const inline = function (s) { return escHtml(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\*(.+?)\*/g, '<em>$1</em>'); };
  let out = '', para = [], list = [];
  const flushP = function () { if (para.length) { out += '<p style="margin:0 0 1rem;line-height:1.55">' + inline(para.join(' ')) + '</p>'; para = []; } };
  const flushL = function () { if (list.length) { out += '<ul style="margin:0 0 1rem;padding-left:1.2rem">' + list.map(function (l) { return '<li style="margin:.2rem 0">' + inline(l) + '</li>'; }).join('') + '</ul>'; list = []; } };
  String(md || '').split('\n').forEach(function (line) {
    if (/^\s*[-•]\s+/.test(line)) { flushP(); list.push(line.replace(/^\s*[-•]\s+/, '')); }
    else if (!line.trim()) { flushP(); flushL(); }
    else { flushL(); para.push(line.trim()); }
  });
  flushP(); flushL();
  return out;
}

/* the Monday snapshot: what the class screen shows today, kept so next Monday can say what moved */
async function takeSnapshot(cls) {
  let subject = null, base = '';
  if (cls.subject_id) { const { data: s } = await supabase.from('subjects').select('id, slug, name').eq('id', cls.subject_id).maybeSingle(); if (s) { subject = s; base = baseSubject(s.slug); } }
  const d = await computeClassProgress(cls.id, cls, subject, base);
  const week = mondayOf(new Date());
  const { error } = await supabase.from('class_snapshots').upsert({ class_id: cls.id, week: week, data: snapshotOf(d) }, { onConflict: 'class_id,week' });
  return error ? { error: error.message } : { ok: true, week: week };
}

async function emailRead(cls, read) {
  if (!cls.teacher_id) return { skipped: 'no teacher' };
  const { data: t } = await supabase.from('profiles').select('email, full_name').eq('id', cls.teacher_id).maybeSingle();
  if (!t || !t.email) return { skipped: 'no email' };
  const link = BASE + '/teacher/classes';
  const subject = cls.name + ': this week’s summary';
  const html = '<div style="font-family:Georgia,serif;color:#26231e;max-width:640px;margin:0 auto;padding:8px 4px">' +
    '<p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#84806f;margin:0 0 .6rem">StudyVault &middot; ' + escHtml(cls.name) + (cls.subjectName ? ' &middot; ' + escHtml(cls.subjectName) : '') + '</p>' +
    '<h1 style="font-size:20px;margin:0 0 1rem">This week&rsquo;s summary</h1>' +
    mdToHtml(read.read_md) +
    '<p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#84806f;border-top:1px solid #e4dfd2;padding-top:.8rem;margin-top:1.2rem">Written by AI from ' + read.answers + ' marked answers by ' + read.pupils + ' pupils this week, and the quiz questions they got wrong. Check it before you act on it. Processed in the UK. ' +
    '<a href="' + link + '" style="color:#c06325">Open the class &rarr;</a></p></div>';
  const text = 'This week’s summary for ' + cls.name + '\n\n' + read.read_md + '\n\nWritten by AI from ' + read.answers + ' marked answers by ' + read.pupils + ' pupils. Check it before you act on it. ' + link;
  const r = await sendEmail({ to: t.email, subject: subject, html: html, text: text });
  if (r && r.ok) await supabase.from('class_reads').update({ emailed_at: new Date().toISOString() }).eq('id', read.id);
  return r;
}

module.exports = async function handler(req, res) {
  const a = authorize(req);
  if (!a.ok) return res.status(401).json({ error: 'Unauthorised' });
  const q = req.query || {};
  const isMonday = new Date().getUTCDay() === 1;
  if (!a.manual && !isMonday) return res.status(200).json({ ok: true, skipped: 'not Monday' });

  let classes;
  if (q.class_id) {
    const { data } = await supabase.from('classes').select('id, name, teacher_id, school_id, subject_id').eq('id', q.class_id);
    classes = data || [];
  } else {
    const { data } = await supabase.from('classes').select('id, name, teacher_id, school_id, subject_id');
    classes = data || [];
  }
  const subjNames = {};
  const sids = classes.map(function (c) { return c.subject_id; }).filter(Boolean);
  if (sids.length) { const { data: subs } = await supabase.from('subjects').select('id, name').in('id', sids); (subs || []).forEach(function (s) { subjNames[s.id] = s.name; }); }

  const out = [];
  for (const cls of classes) {
    try {
      const r = await runRead(cls.id, { force: q.force === '1', dry: q.dry === '1' });
      const item = { class: cls.name, id: cls.id };
      if (q.dry !== '1') item.snapshot = await takeSnapshot(cls);
      if (r.dry) { item.dry = true; item.answers = r.answers; item.pupils = r.pupils; item.packet = r.packet; }
      else if (r.skipped) item.skipped = r.reason;
      else if (r.error) item.error = r.error;
      else {
        item.answers = r.read.answers; item.pupils = r.read.pupils; item.model = r.read.model; item.existing = !!r.existing; item.cost_usd = r.read.cost_usd;
        if (!r.existing || q.force === '1') { cls.subjectName = subjNames[cls.subject_id]; item.email = await emailRead(cls, r.read); }
        if (q.class_id) item.read = r.read.read_md;
      }
      out.push(item);
    } catch (e) { out.push({ class: cls.name, id: cls.id, error: String(e && e.message || e) }); }
  }
  return res.status(200).json({ ok: true, monday: isMonday, manual: a.manual, classes: out.length, results: out });
};
