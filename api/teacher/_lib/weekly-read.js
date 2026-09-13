const { supabase } = require('../../pipeline/_lib/supabase');
const { callClaude } = require('../../_lib/claude');
const { NEVER_SEND, inScope, pick, loadClassFor } = require('./scope');
const { loadCurriculum } = require('./curriculum');
const strength = require('./strength');

/**
 * The weekly read (13 Sep 2026).
 *
 * Once a week, per class, a model reads that week's marked answers (the
 * question, the pupil's own words, the marker's feedback) and the quiz questions
 * the class got wrong, and writes four short paragraphs for the teacher: the
 * pattern across answers, one thing to model, up to three pupils worth a word,
 * and what the quizzes suggest. It is stored in class_reads and shown on the
 * class screen; the cron emails it on Monday morning.
 *
 * Boundary: it reads attainment only — answers, marks, feedback, wrong quiz
 * answers — through the same subject scope as the class screen. Nothing about
 * when or how long anyone worked goes in the packet. Pupil work stays in the
 * UK: the call goes through api/_lib/claude.js, which runs on Bedrock London
 * and fails closed when that is not configured.
 *
 * Cost (Tom, 13 Sep 2026): Sonnet, thinking off, at most 30 answers a read,
 * only when a class has 6+ new marked answers, and a hard cap per school per
 * academic year after which reads drop to Haiku rather than stop. The bake-off
 * that chose Sonnet is in StudyVault Business/weekly-read-bakeoff-2026-09-13.md.
 */
const MIN_ANSWERS = 6;
const MAX_ANSWERS = 30;
const DAYS = 7;
const MODEL = 'claude-sonnet-5';
const FALLBACK = 'claude-haiku-4-5-20251001';
const SCHOOL_CAP_USD = 62;                 // ≈ £50 a year, per school, then Haiku
const PRICE = { 'claude-sonnet-5': [3, 15], 'claude-haiku-4-5-20251001': [1, 5] };   // $/M in, out (on-demand)

function iso(d) { return d.toISOString().slice(0, 10); }
function mondayOf(d) { const x = new Date(d); const day = (x.getUTCDay() + 6) % 7; x.setUTCDate(x.getUTCDate() - day); return iso(x); }
function academicYearStart(d) { const y = d.getUTCFullYear(); return new Date(Date.UTC(d.getUTCMonth() >= 8 ? y : y - 1, 8, 1)); }

/**
 * Everything the model may see for one class this week. Returns null with a
 * reason when there is not enough to read.
 */
async function buildPacket(classId, opts) {
  opts = opts || {};
  const { data: cls } = await supabase.from('classes').select('id, name, school_id, subject_id, teacher_id').eq('id', classId).single();
  if (!cls) return { error: 'Class not found' };
  let subject = null, base = '';
  if (cls.subject_id) {
    const { data: s } = await supabase.from('subjects').select('id, slug, name').eq('id', cls.subject_id).maybeSingle();
    if (s) { subject = s; base = require('./scope').baseSubject(s.slug); }
  }
  const { data: members } = await supabase.from('class_members').select('student_id').eq('class_id', classId);
  const ids = (members || []).map(function (m) { return m.student_id; });
  if (!ids.length) return { cls: cls, skip: 'no pupils' };
  const [{ data: rows }, { data: people }, course] = await Promise.all([
    supabase.from('progress').select('person_id, blob').in('person_id', ids),
    supabase.from('profiles').select('id, full_name').in('id', ids),
    loadCurriculum(subject ? subject.id : null)
  ]);
  const nameOf = {}; (people || []).forEach(function (p) { nameOf[p.id] = p.full_name || 'Pupil'; });
  const since = iso(new Date(Date.now() - DAYS * 864e5));
  const unitName = function (slug) { return course.unitName[slug] || String(slug || '').replace(/-/g, ' '); };

  let answers = [];
  const missTally = {};
  ids.forEach(function (id) {
    const row = (rows || []).find(function (r) { return r.person_id === id; });
    const blob = (row && row.blob) || {};
    NEVER_SEND.forEach(function (k) { delete blob[k]; });
    (Array.isArray(blob.practice) ? blob.practice : []).forEach(function (e) {
      if (!e || !inScope(e.k || e.key || '', base)) return;
      if (!e.d || e.d < since) return;
      const mk = strength.markOf(e); if (!mk) return;
      const p = String(e.k || e.key || '').split('/');
      answers.push({ pupil: nameOf[id], unit: unitName(p[1]), lesson: parseInt(p[2], 10) || null, question_type: e.t || (mk.of + ' marks'),
                     question: String(e.q || '').slice(0, 300), answer: String(e.a || '').slice(0, 1500), mark: mk.got + ' of ' + mk.of,
                     marker_feedback: String(e.r || '').slice(0, 1200), _id: id });
    });
    const kc = pick(blob.kc, base);
    Object.keys(kc).forEach(function (k) {
      const v = kc[k] || {}; if (!v.d || v.d < since) return;
      (v.miss || []).forEach(function (m) {
        if (!m || !m.q) return;
        const key = k + '|' + m.q;
        const it = missTally[key] || (missTally[key] = { unit: unitName(k.split('/')[1]), question: String(m.q).slice(0, 200), right: m.right ? String(m.right).slice(0, 120) : null, chose: {}, pupils: {} });
        it.pupils[id] = 1; if (m.chose) { const c = String(m.chose).slice(0, 120); it.chose[c] = (it.chose[c] || 0) + 1; }
      });
    });
  });
  const pupilsWithAnswers = Object.keys(answers.reduce(function (o, a) { o[a._id] = 1; return o; }, {})).length;
  if (answers.length < MIN_ANSWERS && !opts.force) return { cls: cls, subject: subject, skip: 'only ' + answers.length + ' marked answers this week (needs ' + MIN_ANSWERS + ')' };
  /* cap the read: keep a spread across pupils rather than one prolific pupil's whole week */
  if (answers.length > MAX_ANSWERS) {
    const byPupil = {}; answers.forEach(function (a) { (byPupil[a._id] = byPupil[a._id] || []).push(a); });
    const out = []; let round = 0;
    while (out.length < MAX_ANSWERS) { let added = false; Object.keys(byPupil).forEach(function (id) { if (out.length < MAX_ANSWERS && byPupil[id][round]) { out.push(byPupil[id][round]); added = true; } }); if (!added) break; round++; }
    answers = out;
  }
  const missed = Object.keys(missTally).map(function (k) {
    const it = missTally[k], top = Object.keys(it.chose).sort(function (a, b) { return it.chose[b] - it.chose[a]; })[0] || null;
    return { unit: it.unit, question: it.question, right_answer: it.right, most_common_wrong_answer: top, pupils_wrong: Object.keys(it.pupils).length };
  }).filter(function (m) { return m.pupils_wrong >= 2; }).sort(function (a, b) { return b.pupils_wrong - a.pupils_wrong; }).slice(0, 6);

  return {
    cls: cls, subject: subject, answersCount: answers.length, pupils: pupilsWithAnswers,
    packet: {
      class: cls.name + (subject ? ' · ' + subject.name : ''), week_ending: iso(new Date()), pupils_in_class: ids.length,
      marked_answers_this_week: answers.map(function (a) { const b = Object.assign({}, a); delete b._id; return b; }),
      quiz_questions_most_missed_this_week: missed
    }
  };
}

const SYSTEM = 'You write a short weekly read for a busy secondary teacher about one class, from the evidence in the packet and nothing else. ' +
  'Plain British English, short sentences, no jargon, no praise of the tool. Never invent a fact, a pupil, a quote or a number; every claim must be traceable to the packet. ' +
  'When you quote, quote the PUPIL\'S OWN WORDS from their answer, in quotation marks, never the marker\'s feedback. If the evidence is thin, say so rather than stretch it. ' +
  'Name pupils only where the evidence about them is specific and fixable. This is for the teacher only.';
function userPrompt(packet) {
  return 'Write the weekly read for this class in exactly this shape, in Markdown:\n\n' +
    '**The pattern this week** — 2 to 4 sentences: the habits that recur ACROSS several marked answers (not one pupil), with counts. Quote one or two short phrases from pupils\' answers as evidence.\n\n' +
    '**One thing to model next lesson** — 2 to 3 sentences: the single most useful thing to demonstrate, tied to the question types they attempted.\n\n' +
    '**Worth a word** — up to three pupils, one line each: name, the specific fixable habit, the evidence (which question, and what they wrote).\n\n' +
    '**From the quizzes** — 1 to 2 sentences on the most-missed quiz questions and what the wrong answers suggest the class believes. If there are none, say so in one line.\n\n' +
    'Under 260 words in total. Do not add a title or a word count.\n\nPACKET:\n' + JSON.stringify(packet, null, 1);
}

async function schoolSpendUsd(schoolId) {
  if (!schoolId) return 0;
  const { data } = await supabase.from('class_reads').select('cost_usd').eq('school_id', schoolId).gte('created_at', academicYearStart(new Date()).toISOString());
  return (data || []).reduce(function (n, r) { return n + Number(r.cost_usd || 0); }, 0);
}

/**
 * Write (or return) this week's read for a class. { read, skipped, reason }
 */
async function runRead(classId, opts) {
  opts = opts || {};
  const week = mondayOf(new Date());
  if (!opts.force) {
    const { data: have } = await supabase.from('class_reads').select('*').eq('class_id', classId).eq('week', week).maybeSingle();
    if (have) return { read: have, existing: true };
  }
  const p = await buildPacket(classId, opts);
  if (p.error) return { error: p.error };
  if (p.skip) return { skipped: true, reason: p.skip, cls: p.cls };
  if (opts.dry) return { dry: true, packet: p.packet, answers: p.answersCount, pupils: p.pupils };

  const spent = await schoolSpendUsd(p.cls.school_id);
  const model = spent >= SCHOOL_CAP_USD ? FALLBACK : MODEL;
  const data = await callClaude({ model: model, max_tokens: 1200, thinking: { type: 'disabled' }, system: SYSTEM, messages: [{ role: 'user', content: userPrompt(p.packet) }] });
  const text = (data.content || []).map(function (b) { return b.text || ''; }).join('').trim();
  if (!text) return { error: 'empty read' };
  const u = data.usage || {}, pr = PRICE[model] || [3, 15];
  const cost = ((u.input_tokens || 0) * pr[0] + (u.output_tokens || 0) * pr[1]) / 1e6;
  const row = { class_id: classId, school_id: p.cls.school_id || null, week: week, model: model, served_by: data._servedBy || null,
                read_md: text, answers: p.answersCount, pupils: p.pupils, cost_usd: Math.round(cost * 1e5) / 1e5 };
  const { data: saved, error } = await supabase.from('class_reads').upsert(row, { onConflict: 'class_id,week' }).select().single();
  if (error) return { error: error.message };
  return { read: saved, existing: false, capped: model !== MODEL };
}

/** the latest read for a class, for the class screen */
async function latestRead(classId) {
  const { data } = await supabase.from('class_reads').select('week, model, read_md, answers, pupils, served_by, created_at').eq('class_id', classId).order('week', { ascending: false }).limit(1).maybeSingle();
  return data || null;
}

module.exports = { buildPacket, runRead, latestRead, mondayOf, MIN_ANSWERS, MAX_ANSWERS, SCHOOL_CAP_USD };
