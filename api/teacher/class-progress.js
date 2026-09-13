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
 *
 * The class-level blocks added on 29 Aug — attainment, lessonAttainment and
 * coverage — are all counts over the whole class. Coverage in particular is a
 * curriculum figure, not an effort one: it says WHICH LESSONS have been reached,
 * never on what day or for how long. A per-pupil day-by-day grid was drawn for
 * the old prototype dashboard and is deliberately not rebuilt here.
 */

/* Subject scoping and the ownership rule now live in _lib/scope.js, imported
   here and by the parents'-evening pack. A security filter with two copies
   eventually grows two behaviours. */
const { NEVER_SEND, baseSubject, inScope, pick, loadClassFor } = require('./_lib/scope');
const { loadCurriculum } = require('./_lib/curriculum');
const strength = require('./_lib/strength');
const { latestRead } = require('./_lib/weekly-read');

/* Evidence thresholds. Every one of these exists so the screen never prints a
   confident percentage over three answers. A thin number is worse than a blank
   one, because a teacher acts on it. */
const MIN_CLASS_ANSWERS   = 10;  // before a headline class accuracy is shown
const MIN_LESSON_ANSWERS  = 6;   // before one lesson gets an accuracy
const MIN_LESSON_STUDENTS = 2;   // one pupil's bad morning is not a class problem

function bucketLastActive(iso) {
  if (!iso) return 'never';
  const days = (Date.now() - new Date(iso).getTime()) / 86400000;
  if (days <= 7) return 'this week';
  if (days <= 14) return 'last week';
  if (days <= 28) return 'this month';
  return 'over a month';
}

/* The most recent day this pupil worked on THIS SUBJECT.
   The first version bucketed progress.updated_at — the whole account — under a
   heading that names the subject. A pupil who revised only French yesterday
   showed "this week" to their English teacher: pedagogically misleading, and
   it quietly reveals more than the subject-scoped view is meant to (that they
   were on the platform at all). Derived instead from the dates the blob
   already carries, all subject-scoped: kc entries (d), lesson completion dates
   (when), and warm-up days whose units are in scope. Dates only — never a
   time of day. */
function lastSubjectActivity(blob, base) {
  let latest = null;
  const later = function (d) {
    if (d && typeof d === 'string' && (!latest || d > latest)) latest = d;
  };
  const kc = pick(blob.kc, base);
  Object.keys(kc).forEach(function (k) { later((kc[k] || {}).d); });
  const when = pick(blob.when, base);
  Object.keys(when).forEach(function (k) { later(when[k]); });
  Object.keys(blob.warmlog || {}).forEach(function (day) {
    const units = (blob.warmlog[day] || {}).units || {};
    if (Object.keys(units).some(function (u) { return inScope(u, base); })) later(day);
  });
  return latest;
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

/* Class attainment, lesson by lesson.
   The same kc rows the per-pupil column is built from, tallied the other way up:
   down the class instead of across one child. This is the honest version of the
   heatmap the old prototype drew from a sine wave. */
function tallyLessonKc(kc, into, studentId) {
  Object.keys(kc || {}).forEach(function (k) {
    const v = kc[k] || {};
    if (typeof v.s !== 'number' || typeof v.t !== 'number' || !v.t) return;
    const parts = String(k).split('/');
    const unit = parts[1] || '';
    const lesson = parseInt(parts[2], 10);
    if (!unit || !lesson) return;
    const id = unit + '/' + lesson;
    if (!into[id]) into[id] = { unit: unit, lesson: lesson, right: 0, total: 0, students: {} };
    into[id].right += v.s;
    into[id].total += v.t;
    into[id].students[studentId] = 1;
  });
}

/* Which lessons the class has reached.
   Completions come from blob.done — "subject/unit": [lesson numbers]. Opens come
   from the lesson_visits table, which is the only record of a lesson a pupil
   read but never finished. A lesson counts as touched either way; a teacher
   planning the next fortnight needs "has anyone been here", not "did they tick
   it off". */
function tallyCoverage(done, into, studentId) {
  Object.keys(done || {}).forEach(function (k) {
    const unit = String(k).split('/')[1] || '';
    if (!unit) return;
    const list = done[k] || [];
    if (!list.length) return;
    if (!into[unit]) into[unit] = { unit: unit, lessons: {}, students: {}, completions: 0 };
    list.forEach(function (n) {
      const num = parseInt(n, 10);
      if (!num) return;
      into[unit].lessons[num] = true;
      into[unit].completions++;
    });
    into[unit].students[studentId] = 1;
  });
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

/* The most recent Monday snapshot before today, for "since last Monday" on the screen */
async function lastSnapshot(classId) {
  const today = new Date().toISOString().slice(0, 10);
  const { data } = await supabase.from('class_snapshots').select('week, data').eq('class_id', classId).lt('week', today).order('week', { ascending: false }).limit(1).maybeSingle();
  return data ? Object.assign({ week: data.week }, data.data) : null;
}

/* What a Monday snapshot keeps: class-level counts only */
function snapshotOf(d) {
  const units = {};
  (d.unitBands || []).forEach(function (u) { units[u.slug] = { score: u.score, secure: u.secure, developing: u.developing, emerging: u.emerging, notYet: u.notYet, under: u.under }; });
  return { recall: d.attainment ? d.attainment.accuracy : null, answered: d.attainment ? d.attainment.answered : 0, withEvidence: d.attainment ? d.attainment.studentsWithEvidence : 0,
           marked: (d.markbook && d.markbook.rows || []).reduce(function (n, r) { return n + (r.marks ? r.marks.answers : 0); }, 0), units: units };
}

/**
 * The whole class picture as one object. The HTTP handler below authorises and
 * then calls this; the Monday cron calls it directly to take the week's snapshot.
 */
async function computeClassProgress(classId, cls, classSubject, base) {
  /* The class is the only door to a pupil. Everything below reads from this
     list, so a free-tier user — who is in no class_members row — cannot appear
     in a teacher view by any path. */
  const { data: members } = await supabase
    .from('class_members').select('student_id').eq('class_id', classId);
  const ids = (members || []).map(function (m) { return m.student_id; });

  const shell = {
    class: { id: cls.id, name: cls.name, year_group: cls.year_group,
             subject: classSubject ? classSubject.name : null,
             subjectSlug: classSubject ? classSubject.slug : null }
  };

  if (!ids.length) {
    return Object.assign({}, shell, {
      size: 0, students: [], misconceptions: [], weakestUnits: [], missedItems: [],
      attainment: null, lessonAttainment: [], coverage: null, activity: {},
      markbook: { units: [], questionTypes: [], rows: [] }, unitBands: [], goingCold: [], haveAWord: [], marks: [], lastWeek: null
    });
  }

  const [{ data: rows }, { data: people }, course, weeklyRead, lastWeek] = await Promise.all([
    supabase.from('progress').select('person_id, blob, updated_at').in('person_id', ids),
    supabase.from('profiles').select('id, full_name').in('id', ids),
    loadCurriculum(classSubject ? classSubject.id : null),
    latestRead(classId).catch(function () { return null; }),
    lastSnapshot(classId).catch(function () { return null; })
  ]);
  const nameOf = {};
  (people || []).forEach(function (p) { nameOf[p.id] = p.full_name || 'Student'; });

  const students = [];
  const misTally = {};
  const unitTally = {};      // warm-up accuracy per unit
  const questionTally = {};  // the individual questions this class gets wrong
  const lessonKc = {};       // class attainment, lesson by lesson
  const coverTally = {};     // which lessons of the course have been reached
  const activity = { 'this week': 0, 'last week': 0, 'this month': 0, 'over a month': 0, never: 0 };
  let classRight = 0, classAnswered = 0, withEvidence = 0;
  /* 13 Sep 2026 — the Monday-briefing screen: per pupil per unit strength in the
     pupil's own words (secure / developing / emerging), what each pupil keeps
     getting wrong, and their marked answers. All attainment; nothing about when
     or how long. Assembled here so the markbook, "going cold" and "have a word"
     all read from one pass over the class. */
  const pupilUnits = {};     // id -> { unitSlug: {s, peak, n, band, drop} }
  const pupilLessons = {};   // id -> { "unit/n": {s, band, quiz} }  (the markbook's lessons-in-one-unit view)
  const pupilTypes = {};     // id -> { type: {got, of, answers} }   (the markbook's question-type view)
  const typeSeen = {};       // type -> answers across the class
  const pupilMisses = {};    // id -> [{unit, lesson, q, chose, right, times}]
  const pupilAnswers = {};   // id -> [{unit, lesson, marks, got, note}]
  const marksTally = {};     // marks available -> {answers, got, of, units:{}}
  const doneOf = {};         // id -> subject-scoped done map (for "opened N units")
  const NOW = Date.now();

  ids.forEach(function (id) {
    const row = (rows || []).find(function (r) { return r.person_id === id; });
    const blob = (row && row.blob) || {};
    NEVER_SEND.forEach(function (k) { delete blob[k]; });   // belt and braces

    const bucket = bucketLastActive(lastSubjectActivity(blob, base));
    activity[bucket] = (activity[bucket] || 0) + 1;

    const kcScoped = pick(blob.kc, base);
    const doneScoped = pick(blob.done, base);
    doneOf[id] = doneScoped;

    const mine = quizAccuracy(kcScoped);
    Object.keys(kcScoped).forEach(function (k) {
      const v = kcScoped[k] || {};
      if (typeof v.s === 'number' && typeof v.t === 'number') { classRight += v.s; classAnswered += v.t; }
    });
    if (mine != null) withEvidence++;

    students.push({
      id: id,
      name: nameOf[id] || 'Student',
      lessonsComplete: countComplete(doneScoped),
      quizAccuracy: mine,
      kcAnswered: Object.keys(kcScoped).reduce(function (n, k) { return n + (((kcScoped[k] || {}).t) || 0); }, 0),
      practiceAnswered: Array.isArray(blob.practice)
        ? blob.practice.filter(function (x) { return inScope((x && (x.k || x.key)) || '', base); }).length
        : 0,
      lastActive: bucket            // bucketed on purpose — never a timestamp
    });

    warmupByUnit(blob.warmlog, unitTally, base);
    missedQuestions(kcScoped, questionTally, id);

    const practiceScoped = Array.isArray(blob.practice)
      ? blob.practice.filter(function (x) { return x && inScope(x.k || x.key || '', base); }) : [];
    const lessonMap = strength.lessons(kcScoped, doneScoped, pick(blob.when, base), practiceScoped, NOW);
    pupilUnits[id] = strength.units(lessonMap);
    pupilLessons[id] = {};
    Object.keys(lessonMap).forEach(function (k) { const l = lessonMap[k]; pupilLessons[id][k] = { s: l.s, band: strength.band(l.s), quiz: l.quiz }; });
    /* the questions this pupil keeps getting wrong, folded by question */
    const mm = {};
    Object.keys(kcScoped).forEach(function (k) {
      const parts = k.split('/');
      (((kcScoped[k] || {}).miss) || []).forEach(function (m) {
        if (!m || !m.q) return;
        const key = parts[1] + '|' + m.q;
        if (!mm[key]) mm[key] = { unit: parts[1], lesson: parseInt(parts[2], 10), q: String(m.q).slice(0, 160), chose: m.chose ? String(m.chose).slice(0, 100) : null, right: m.right ? String(m.right).slice(0, 100) : null, times: 0 };
        mm[key].times++;
      });
    });
    pupilMisses[id] = Object.keys(mm).map(function (k) { return mm[k]; }).sort(function (a, b) { return b.times - a.times; }).slice(0, 12);
    /* marked answers: the mark, the marks available, and the marker's first note */
    pupilAnswers[id] = practiceScoped.map(function (e) {
      const mk = strength.markOf(e); if (!mk) return null;
      const parts = String(e.k || e.key || '').split('/');
      const note = String(e.r || '').replace(/^[^\n]*\b(mark|score)[^\n]*\n?/i, '').replace(/\s+/g, ' ').trim().slice(0, 140);
      const row = { unit: parts[1] || '', lesson: parseInt(parts[2], 10) || null, marks: mk.of, got: mk.got, note: note || null };
      /* question type, as the question carries it ("8 marks · Explain Significance"); older entries only know the marks */
      const ty = (e.t && String(e.t).replace(/^\d+\s*marks?\s*[·\-–—:]\s*/i, '').trim()) || (mk.of + '-mark');
      const pt = pupilTypes[id] || (pupilTypes[id] = {});
      const tt = pt[ty] || (pt[ty] = { got: 0, of: 0, answers: 0 });
      tt.got += mk.got; tt.of += mk.of; tt.answers++;
      typeSeen[ty] = (typeSeen[ty] || 0) + 1;
      const mt = marksTally[mk.of] || (marksTally[mk.of] = { marks: mk.of, answers: 0, got: 0, of: 0, units: {} });
      mt.answers++; mt.got += mk.got; mt.of += mk.of; mt.units[row.unit] = (mt.units[row.unit] || 0) + 1;
      return row;
    }).filter(Boolean).slice(0, 8);
    tallyLessonKc(kcScoped, lessonKc, id);
    tallyCoverage(doneScoped, coverTally, id);

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

  /* Lessons opened but never finished. Bounded twice: by class membership on the
     query, and by this subject's own lesson ids on the way in — a pupil who also
     studies Geography does not leak a single Geography row to their English
     teacher. */
  const { data: visits } = await supabase
    .from('lesson_visits').select('user_id, lesson_id').in('user_id', ids).limit(20000);
  (visits || []).forEach(function (v) {
    const at = course.byLessonId[v.lesson_id];
    if (!at) return;                                   // not this subject: dropped
    if (!coverTally[at.unit]) {
      coverTally[at.unit] = { unit: at.unit, lessons: {}, students: {}, completions: 0 };
    }
    coverTally[at.unit].lessons[at.lesson] = true;
    coverTally[at.unit].students[v.user_id] = 1;
  });

  students.sort(function (a, b) { return a.name.localeCompare(b.name); });

  function unitLabel(slug) {
    return course.unitName[slug] || String(slug || '').replace(/-/g, ' ');
  }

  const misconceptions = Object.keys(misTally)
    .map(function (k) {
      const m = misTally[k];
      delete m._seen;
      m.unitName = unitLabel(m.unit);   // "Macbeth", not "macbeth"
      return m;
    })
    .sort(function (a, b) { return b.students - a.students || b.count - a.count; })
    .slice(0, 25);

  /* Weakest units first — accuracy, with attempts shown so a teacher can see
     how much evidence sits behind each number. Anything under 12 attempts is
     too thin to act on and is dropped rather than shown as a scary percentage. */
  const weakestUnits = Object.keys(unitTally).map(function (k) {
    const u = unitTally[k];
    const slug = String(u.unit).split('/')[1] || '';
    return { unit: unitLabel(slug), slug: slug, attempts: u.attempts,
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
    const wp = String(q.where).split('/');
    const met = lessonKc[wp[1] + '/' + wp[2]];
    return { where: q.where, unit: unitLabel(wp[1]), lesson: parseInt(wp[2], 10) || null,
             met: met ? Object.keys(met.students).length : null,
             question: q.question, right: q.right,
             misses: q.misses, students: Object.keys(q.students).length,
             commonWrongAnswer: top, commonWrongCount: top ? q.chose[top] : 0 };
  }).filter(function (q) { return q.students >= 2; })
    .sort(function (a, b) { return b.students - a.students || b.misses - a.misses; })
    .slice(0, 20);

  /* Class attainment lesson by lesson, weakest first. Only lessons more than one
     pupil has been quizzed on, and only where enough questions were answered to
     mean anything. Everything thinner is reported as a count, not hidden — a
     teacher should be able to tell "nobody has done this yet" apart from "this
     screen has decided not to tell me". */
  const lessonRows = Object.keys(lessonKc).map(function (k) { return lessonKc[k]; });
  const lessonAttainment = lessonRows.map(function (r) {
    return {
      unit: unitLabel(r.unit),
      unitSlug: r.unit,
      lesson: r.lesson,
      title: course.lessonTitle[r.unit + '/' + r.lesson] || null,
      answered: r.total,
      accuracy: Math.round((r.right / r.total) * 100),
      students: Object.keys(r.students).length
    };
  }).filter(function (r) {
    return r.students >= MIN_LESSON_STUDENTS && r.answered >= MIN_LESSON_ANSWERS;
  }).sort(function (a, b) { return a.accuracy - b.accuracy || b.students - a.students; })
    .slice(0, 20);

  const attainment = {
    answered: classAnswered,
    accuracy: classAnswered >= MIN_CLASS_ANSWERS
      ? Math.round((classRight / classAnswered) * 100) : null,
    studentsWithEvidence: withEvidence,
    size: ids.length,
    lessonsWithEvidence: lessonRows.length,
    lessonsShown: lessonAttainment.length
  };

  /* Coverage. Units the class has actually worked in, best-covered last so the
     gaps read first. Untouched units are counted, not listed: a set-text subject
     carries twenty-nine units and a class studies four, so printing the other
     twenty-five as 0% would bury the real news. */
  const coverUnits = Object.keys(coverTally).map(function (slug) {
    const c = coverTally[slug];
    const touched = Object.keys(c.lessons).length;
    const total = course.liveCount[slug] || 0;
    const started = Object.keys(c.students).length;
    return {
      unit: unitLabel(slug),
      slug: slug,
      practice: !!course.practiceUnit[slug],
      lessons: total,
      touched: touched,
      percent: total ? Math.round((touched / total) * 100) : null,
      studentsStarted: started,
      /* averaged over the pupils who have STARTED the unit, not the whole roll.
         Dividing by the roll turned "one pupil has done a lesson of A Christmas
         Carol" into an average of 0, which reads as nobody having touched it. */
      avgDone: started ? Math.round((c.completions / started) * 10) / 10 : 0
    };
  }).sort(function (a, b) {
    if (a.percent == null) return 1;
    if (b.percent == null) return -1;
    return a.percent - b.percent;
  });

  const touchedSlugs = {};
  coverUnits.forEach(function (u) { touchedSlugs[u.slug] = 1; });
  const untouched = course.units.filter(function (u) { return !touchedSlugs[u.slug]; });

  const coverage = course.units.length ? {
    courseUnits: course.units.length,
    courseLessons: course.totalLessons,
    unitsStarted: coverUnits.length,
    lessonsTouched: coverUnits.reduce(function (n, u) { return n + u.touched; }, 0),
    /* The denominator that means something. English Literature carries 222
       lessons because it covers every set text on the spec; a class studies
       three of them. "21 of 222" reads as a class in crisis when they are
       actually 21 of 28 through the texts they take, so the headline counts
       only the units they have started. courseLessons stays available for
       anything that genuinely wants the whole course. */
    lessonsInStartedUnits: coverUnits.reduce(function (n, u) { return n + u.lessons; }, 0),
    unitsUntouched: untouched.length,
    units: coverUnits
  } : null;

  /* ---- the briefing's panels and the markbook (13 Sep 2026) ---- */
  const unitsTouched = {};
  ids.forEach(function (id) { Object.keys(pupilUnits[id] || {}).forEach(function (u) { unitsTouched[u] = 1; }); });
  const markUnits = course.units.filter(function (u) { return unitsTouched[u.slug]; }).map(function (u) {
    return { slug: u.slug, name: u.name, lessons: course.liveCount[u.slug] || 0, practice: !!course.practiceUnit[u.slug] };
  });
  const unitBands = markUnits.map(function (u) {
    const c = { g: 0, a: 0, r: 0, n: 0 }; let tot = 0, cnt = 0, under = 0, dropped = 0, last = 999;
    ids.forEach(function (id) {
      const x = (pupilUnits[id] || {})[u.slug];
      if (!x) { c.n++; return; }
      c[x.band]++; tot += x.s; cnt++; if (x.s < strength.REVISIT_LINE) under++; if (x.drop) dropped++; last = Math.min(last, x.last);
    });
    const score = cnt ? Math.round(tot / cnt) : null;
    return { unit: u.name, slug: u.slug, lessons: u.lessons, secure: c.g, developing: c.a, emerging: c.r, notYet: c.n,
             pupils: cnt, score: score, band: score == null ? null : strength.band(score),
             word: score == null ? 'not started' : strength.bandWord(strength.band(score)),
             under: under, dropped: dropped, lastDays: cnt ? last : null };
  });
  /* going cold: learned, then faded. Needs a few pupils and more than one slip. */
  const goingCold = unitBands.filter(function (u) { return u.pupils >= 3 && u.dropped >= 2; })
    .sort(function (a, b) { return b.dropped - a.dropped || b.under - a.under; }).slice(0, 4);

  /* have a word: a short list, one reason each, worst reasons first */
  const words = [];
  students.forEach(function (st) {
    const id = st.id, pu = pupilUnits[id] || {}, slugs = Object.keys(pu);
    const drops = slugs.filter(function (u) { return pu[u].drop; });
    const ans = pupilAnswers[id] || [];
    const got = ans.reduce(function (n, a) { return n + a.got; }, 0), of = ans.reduce(function (n, a) { return n + a.marks; }, 0);
    const dn = doneOf[id] || {};
    const doneUnits = Object.keys(dn).filter(function (k) { return (dn[k] || []).length; });
    const maxLesson = doneUnits.reduce(function (m, k) { return Math.max(m, Math.max.apply(null, dn[k].map(Number))); }, 0);
    /* plain words (Tom, 13 Sep 2026): say what happened, not the model's name for it */
    if (drops.length) words.push({ id: id, name: st.name, rank: 0, why: 'Knew ' + unitLabel(drops[0]) + ' well, now needs to revise it again' + (drops.length > 1 ? ' (and ' + (drops.length - 1) + ' more ' + (drops.length > 2 ? 'topics' : 'topic') + ')' : '') + '.' });
    else if (st.quizAccuracy != null && st.quizAccuracy < 45 && st.kcAnswered >= 10) words.push({ id: id, name: st.name, rank: 1, why: 'Got ' + st.quizAccuracy + '% of ' + st.kcAnswered + ' quiz answers right, the lowest in the class.' });
    else if (ans.length >= 3 && of && got / of < 0.4) words.push({ id: id, name: st.name, rank: 2, why: 'Scores about ' + Math.round(got / ans.length * 10) / 10 + ' out of ' + Math.round(of / ans.length) + ' on marked answers, over ' + ans.length + ' of them.' });
    else if (doneUnits.length >= 3 && maxLesson <= 2) words.push({ id: id, name: st.name, rank: 3, why: 'Has started ' + doneUnits.length + ' topics and not got past lesson 2 in any of them.' });
    else if (!slugs.length) words.push({ id: id, name: st.name, rank: 4, why: 'Has not done a lesson or quiz in ' + (classSubject ? classSubject.name : 'this subject') + ' yet.' });
  });
  const haveAWord = words.sort(function (a, b) { return a.rank - b.rank || a.name.localeCompare(b.name); }).slice(0, 5);

  /* where the marks are going: by the marks a question carries */
  const marks = Object.keys(marksTally).map(function (k) {
    const m = marksTally[k];
    const topUnit = Object.keys(m.units).sort(function (a, b) { return m.units[b] - m.units[a]; })[0];
    return { marks: m.marks, answers: m.answers, average: Math.round(m.got / m.answers * 10) / 10, percent: Math.round(m.got / m.of * 100), unit: unitLabel(topUnit) };
  }).filter(function (m) { return m.answers >= 3; }).sort(function (a, b) { return a.marks - b.marks; });

  /* the markbook: one row per pupil, one cell per unit the class has touched;
     plus the two other views — lessons within a unit, and marks by question type */
  const questionTypes = Object.keys(typeSeen).sort(function (a, b) { return typeSeen[b] - typeSeen[a]; }).slice(0, 8);
  const markbook = {
    units: markUnits,
    questionTypes: questionTypes,
    rows: students.map(function (st) {
      const pu = pupilUnits[st.id] || {}, cells = {};
      markUnits.forEach(function (u) { const x = pu[u.slug]; if (x) cells[u.slug] = { band: x.band, score: x.s, n: x.n, q: x.q, drop: x.drop }; });
      const ans = pupilAnswers[st.id] || [];
      const got = ans.reduce(function (n, a) { return n + a.got; }, 0), of = ans.reduce(function (n, a) { return n + a.marks; }, 0);
      let weakest = null;
      Object.keys(pu).forEach(function (u) { if (!weakest || pu[u].s < pu[weakest].s) weakest = u; });
      const types = {};
      questionTypes.forEach(function (t) { const x = (pupilTypes[st.id] || {})[t]; if (x) types[t] = { percent: Math.round(x.got / x.of * 100), answers: x.answers }; });
      return { id: st.id, name: st.name, cells: cells, marks: of ? { percent: Math.round(got / of * 100), answers: ans.length } : null,
               recall: st.quizAccuracy, weakest: weakest ? unitLabel(weakest) : null,
               lessons: pupilLessons[st.id] || {}, types: types,
               misses: pupilMisses[st.id] || [], answers: ans };
    })
  };

  return Object.assign({}, shell, {
    size: ids.length,
    students: students,
    markbook: markbook,
    weeklyRead: weeklyRead,
    unitBands: unitBands,
    goingCold: goingCold,
    haveAWord: haveAWord,
    marks: marks,
    attainment: attainment,
    lessonAttainment: lessonAttainment,
    coverage: coverage,
    misconceptions: misconceptions,
    weakestUnits: weakestUnits,
    missedItems: missedItems,
    activity: activity,
    lastWeek: lastWeek
  });
}

module.exports = async function handler(req, res) {
  if (req.method !== 'GET' && req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const classId = (req.query && req.query.class_id) || (req.body && req.body.class_id);

  /* Ownership, school and subject scoping in one place, shared with the pack.
     You may see a class you teach; a school_admin may see any class in their own
     school; platform_admin sees anything; nobody sees another school. */
  const scope = await loadClassFor(auth, classId);
  if (!scope.ok) return res.status(scope.status || 400).json({ error: scope.error });

  const out = await computeClassProgress(classId, scope.cls, scope.subject, scope.base);
  return res.status(200).json(out);
};
module.exports.computeClassProgress = computeClassProgress;
module.exports.snapshotOf = snapshotOf;
