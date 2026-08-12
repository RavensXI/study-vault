const { requireTeacher } = require('../pipeline/_lib/auth');
const { supabase } = require('../pipeline/_lib/supabase');

/**
 * Class progress for a teacher.
 *
 * WHAT THIS RETURNS IS DELIBERATELY NARROW. The boundary was agreed with Tom on
 * 12 Aug 2026 and is recorded in memory as feedback_teacher_data_boundary:
 *
 *   SEND           attainment — misconceptions, quiz and practice outcomes,
 *                  completion against the weighted model
 *   AGGREGATE ONLY anything about WHEN or HOW MUCH a particular child worked.
 *                  "Twelve are under 20% of this unit" is fair. "Jamie revised
 *                  at 11:40pm on Sunday" is surveillance, and it is what makes a
 *                  parent complain and a school withdraw.
 *   NEVER          flashcard spacing state, planner preferences, rest days,
 *                  shorts watched. No teaching value, real privacy cost.
 *
 * This is children's data: UK GDPR and the Age Appropriate Design Code make
 * minimisation a legal requirement, not a courtesy. Every field below has to
 * answer a teaching question or it does not belong in the response.
 *
 * Last-active is therefore bucketed, never a timestamp — a teacher needs to know
 * who has stopped, not when someone was at their desk.
 */

/* Subject scoping and the ownership rule now live in _lib/scope.js, imported
   here and by the parents'-evening pack. A security filter with two copies
   eventually grows two behaviours. */
const { NEVER_SEND, baseSubject, inScope, pick } = require('./_lib/scope');

function bucketLastActive(iso) {
  if (!iso) return 'never';
  const days = (Date.now() - new Date(iso).getTime()) / 86400000;
  if (days <= 7) return 'this week';
  if (days <= 14) return 'last week';
  if (days <= 28) return 'this month';
  return 'over a month';
}

function countComplete(done) {
  if (!done || typeof done !== 'object') return 0;
  return Object.keys(done).reduce(function (n, k) {
    return n + ((done[k] || []).length || 0);
  }, 0);
}

/* Quiz accuracy from the kc log. Real shape, confirmed against live rows:
     kc = { "subject/unit/lesson": { d: "2026-07-14", s: 4, t: 4, miss: [...] } }
   s = score, t = total. I first assumed {correct,total} and every student came
   back with null accuracy — a dashboard full of blanks that looks like "no data"
   rather than "wrong key". */
function quizAccuracy(kc) {
  if (!kc || typeof kc !== 'object') return null;
  let right = 0, total = 0;
  Object.keys(kc).forEach(function (k) {
    const v = kc[k];
    if (v && typeof v.s === 'number' && typeof v.t === 'number') { right += v.s; total += v.t; }
  });
  return total ? Math.round((right / total) * 100) : null;
}

/* Warm-up accuracy per unit.
     warmlog = { "2026-06-16": { total: 10, units: { "subject/unit": {a, m} } } }
   a = attempts, m = misses. Attempts matter: computing accuracy from misses
   alone makes every unit look catastrophic. */
function warmupByUnit(warmlog, into, base) {
  if (!warmlog || typeof warmlog !== 'object') return;
  Object.keys(warmlog).forEach(function (day) {
    const units = (warmlog[day] || {}).units || {};
    Object.keys(units).forEach(function (u) {
      const x = units[u] || {};
      if (typeof x.a !== 'number') return;
      if (!inScope(u, base)) return;
      if (!into[u]) into[u] = { unit: u, attempts: 0, misses: 0, students: {} };
      into[u].attempts += x.a;
      into[u].misses += (x.m || 0);
    });
  });
}

/* The questions a class actually gets wrong, and WHICH WRONG ANSWER they picked.
   Real shape:
     miss: [{ q: "...", chose: "About a tenth", right: "About two-thirds" }]

   `chose` is the whole value here. "Fourteen got this wrong" tells a teacher to
   reteach something; "fourteen chose 'about a tenth' when the answer is
   'two-thirds'" tells them WHAT the class believes, which is a lesson starter.
   This is the misconception surfacing we scoped this morning — and it turns out
   it is already captured on every knowledge check site-wide, not only on the
   lessons with hand-authored misconception tags. No new capture needed. */
function missedQuestions(kc, into, studentId) {
  if (!kc || typeof kc !== 'object') return;
  Object.keys(kc).forEach(function (k) {
    (((kc[k] || {}).miss) || []).forEach(function (m) {
      if (!m || !m.q) return;
      const key = k + '|' + m.q;
      if (!into[key]) {
        into[key] = { where: k, question: String(m.q).slice(0, 200),
                      right: m.right ? String(m.right).slice(0, 120) : null,
                      misses: 0, students: {}, chose: {} };
      }
      const it = into[key];
      it.misses++;
      it.students[studentId] = 1;
      if (m.chose) {
        const c = String(m.chose).slice(0, 120);
        it.chose[c] = (it.chose[c] || 0) + 1;
      }
    });
  });
}

module.exports = async function handler(req, res) {
  if (req.method !== 'GET' && req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const classId = (req.query && req.query.class_id) || (req.body && req.body.class_id);
  if (!classId) return res.status(400).json({ error: 'Missing class_id' });

  const { data: cls, error: clsErr } = await supabase
    .from('classes')
    .select('id, name, school_id, subject_id, teacher_id, year_group')
    .eq('id', classId)
    .single();
  if (clsErr || !cls) return res.status(404).json({ error: 'Class not found' });

  /* You may see a class you teach. A school_admin may see any class in their
     own school. platform_admin sees anything. Nobody sees another school. */
  const role = auth.profile.role;
  const mine = cls.teacher_id && cls.teacher_id === auth.profile.id;
  const sameSchool = cls.school_id && cls.school_id === auth.profile.school_id;
  const allowed = role === 'platform_admin' || mine || (role === 'school_admin' && sameSchool);
  if (!allowed) return res.status(403).json({ error: 'That class is not yours.' });

  /* the subject this class is for — everything below is scoped to it */
  let classSubject = null, base = '';
  if (cls.subject_id) {
    const { data: subj } = await supabase
      .from('subjects').select('slug, name').eq('id', cls.subject_id).single();
    if (subj) { classSubject = subj; base = baseSubject(subj.slug); }
  }

  const { data: members } = await supabase
    .from('class_members').select('student_id').eq('class_id', classId);
  const ids = (members || []).map(function (m) { return m.student_id; });
  if (!ids.length) return res.status(200).json({ class: cls, size: 0, students: [], misconceptions: [], activity: {} });

  const [{ data: rows }, { data: people }] = await Promise.all([
    supabase.from('progress').select('person_id, blob, updated_at').in('person_id', ids),
    supabase.from('profiles').select('id, full_name').in('id', ids)
  ]);
  const nameOf = {};
  (people || []).forEach(function (p) { nameOf[p.id] = p.full_name || 'Student'; });

  const students = [];
  const misTally = {};
  const unitTally = {};      // warm-up accuracy per unit
  const questionTally = {};  // the individual questions this class gets wrong
  const activity = { 'this week': 0, 'last week': 0, 'this month': 0, 'over a month': 0, never: 0 };

  ids.forEach(function (id) {
    const row = (rows || []).find(function (r) { return r.person_id === id; });
    const blob = (row && row.blob) || {};
    NEVER_SEND.forEach(function (k) { delete blob[k]; });   // belt and braces

    const bucket = bucketLastActive(row && row.updated_at);
    activity[bucket] = (activity[bucket] || 0) + 1;

    const kcScoped = pick(blob.kc, base);

    students.push({
      id: id,
      name: nameOf[id] || 'Student',
      lessonsComplete: countComplete(pick(blob.done, base)),
      quizAccuracy: quizAccuracy(kcScoped),
      practiceAnswered: Array.isArray(blob.practice)
        ? blob.practice.filter(function (x) { return inScope((x && (x.k || x.key)) || '', base); }).length
        : 0,
      lastActive: bucket            // bucketed on purpose — never a timestamp
    });

    warmupByUnit(blob.warmlog, unitTally, base);
    missedQuestions(kcScoped, questionTally, id);

    /* misconceptions are the point of the whole thing: each entry was written
       only when a wrong answer MATCHED a known error, never on a guess */
    (blob.miscon || []).forEach(function (m) {
      if (!m || !m.tag) return;
      if (base && baseSubject(m.sub) !== base) return;   // not this teacher's subject
      const key = [m.sub || '', m.unit || '', m.n || 0, m.tag].join('|');
      if (!misTally[key]) {
        misTally[key] = { subject: m.sub, unit: m.unit, lesson: m.n, tag: m.tag, count: 0, students: 0, _seen: {} };
      }
      misTally[key].count++;
      if (!misTally[key]._seen[id]) { misTally[key]._seen[id] = 1; misTally[key].students++; }
    });
  });

  const misconceptions = Object.keys(misTally)
    .map(function (k) { const m = misTally[k]; delete m._seen; return m; })
    .sort(function (a, b) { return b.students - a.students || b.count - a.count; })
    .slice(0, 25);

  students.sort(function (a, b) { return a.name.localeCompare(b.name); });

  /* Weakest units first — accuracy, with attempts shown so a teacher can see
     how much evidence sits behind each number. Anything under 12 attempts is
     too thin to act on and is dropped rather than shown as a scary percentage. */
  const weakestUnits = Object.keys(unitTally).map(function (k) {
    const u = unitTally[k];
    return { unit: u.unit, attempts: u.attempts,
             accuracy: u.attempts ? Math.round(((u.attempts - u.misses) / u.attempts) * 100) : null };
  }).filter(function (u) { return u.attempts >= 12; })
    .sort(function (a, b) { return a.accuracy - b.accuracy; }).slice(0, 12);

  /* The item analysis: which questions the class actually got wrong, and how
     many of them. Needs at least two students, or it is one pupil's slip. */
  const missedItems = Object.keys(questionTally).map(function (k) {
    const q = questionTally[k];
    /* the most popular wrong answer, with how many picked it — a shared wrong
       answer is a misconception; scattered wrong answers are just difficulty */
    const top = Object.keys(q.chose)
      .sort(function (a, b) { return q.chose[b] - q.chose[a]; })[0] || null;
    return { where: q.where, question: q.question, right: q.right,
             misses: q.misses, students: Object.keys(q.students).length,
             commonWrongAnswer: top, commonWrongCount: top ? q.chose[top] : 0 };
  }).filter(function (q) { return q.students >= 2; })
    .sort(function (a, b) { return b.students - a.students || b.misses - a.misses; })
    .slice(0, 20);

  return res.status(200).json({
    class: { id: cls.id, name: cls.name, year_group: cls.year_group,
             subject: classSubject ? classSubject.name : null,
             subjectSlug: classSubject ? classSubject.slug : null },
    size: ids.length,
    students: students,
    misconceptions: misconceptions,
    weakestUnits: weakestUnits,
    missedItems: missedItems,
    activity: activity
  });
};
