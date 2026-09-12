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
 *                  (Which CARDS a pupil keeps failing is attainment, and is
 *                  sent — see weakCards below. When they are next due is not.)
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

/* ---- Weak cards -------------------------------------------------------------
   The flashcard signal, per card. A pupil can hold a unit well and still fail
   ONE card in it every time — "the terms of the Treaty of Versailles" inside a
   Conflict and Tension deck that is otherwise in box 4. That is a thing a
   teacher can fix in five minutes on Monday, which is why it is worth sending.

   What leaves the server is attainment: which card, how weak, and the DATE it
   was last missed. The spacing state itself (nextReview, the streak, the
   timestamps in the log) stays on this side — flashsr and flashlog are on
   NEVER_SEND, and they are read here before the scrub and never copied out.

   Card keys are "<lesson uuid>:q<index>" into lessons.flashcard_questions; the
   mark log carries subject/unit/lesson-number and the question text. Both are
   joined to the course through the same byLessonId map lesson_visits uses, so a
   card from another subject is dropped on the way in. */
const WEAK_BOX          = 2;    // Leitner box 1–2 = not yet learned
const FINE_BOX          = 3;    // box 3+ = holding
const MIN_CARD_ATTEMPTS = 2;    // one wrong go at a new card is not a weak card
const WRONG_RUN         = 2;    // ...but two wrong marks in a row is
const PUPIL_WEAK_CARDS  = 5;
const CLASS_HOTSPOTS    = 10;
const MIN_HOTSPOT_PUPILS = 2;   // one pupil's blind spot is not a class teaching point
const UNIT_FINE_SHARE   = 0.7;
const UNIT_FINE_MIN_CARDS = 3;
const UNIT_FINE_KC_ACC  = 70;
const UNIT_FINE_KC_MIN  = 10;

function cardIdxOf(key) {
  const at = String(key).lastIndexOf(':');
  return at < 0 ? null : { lid: key.slice(0, at), idx: key.slice(at + 1) };
}

/* One pupil's card evidence, gathered before the blob is scrubbed.
   Returns the box-weak cards, the log-weak cards (a run of wrong marks), the
   last date each card text was missed, and per-unit "is the rest fine" data.
   Question TEXT is joined later, once we know which lessons need fetching. */
function collectCards(flashsr, flashlog, kcScoped, course, subjectSlug, idByKey) {
  const cards = (flashsr && flashsr.cards) || {};
  const byBox = [];            // { lid, idx, box, attempts }
  const unitCards = {};        // unit slug -> { fine: n, tried: n }
  const cardState = {};        // "lid:idx" -> { box, attempts }

  Object.keys(cards).forEach(function (k) {
    const at = cardIdxOf(k);
    if (!at) return;
    const where = course.byLessonId[at.lid];
    if (!where) return;                                  // not this subject: dropped
    const c = cards[k] || {};
    if (typeof c.box !== 'number') return;
    const attempts = typeof c.attempts === 'number' ? c.attempts : 0;
    cardState[at.lid + ':' + at.idx] = { box: c.box, attempts: attempts };
    const weak = c.box <= WEAK_BOX && attempts >= MIN_CARD_ATTEMPTS;
    if (weak) byBox.push({ lid: at.lid, idx: at.idx, box: c.box, attempts: attempts });
    if (!weak && attempts >= 1) {
      if (!unitCards[where.unit]) unitCards[where.unit] = { fine: 0, tried: 0 };
      unitCards[where.unit].tried++;
      if (c.box >= FINE_BOX) unitCards[where.unit].fine++;
    }
  });

  /* The mark log, newest first (it is written by unshift; sort anyway). Per
     card text: how many wrong marks sit at the top of its history, and the
     date of the most recent miss. Timestamps are read for order only. */
  const marks = {};            // "lid|text" -> { lid, q, run, open, lastWrong }
  const log = Array.isArray(flashlog) ? flashlog.slice() : [];
  log.sort(function (a, b) { return ((b && b.t) || 0) - ((a && a.t) || 0); });
  log.forEach(function (e) {
    if (!e || !e.q || !e.unit || !e.n) return;
    if (!subjectSlug || e.sub !== subjectSlug) return;   // exact slug: unit slugs repeat across boards
    const lid = idByKey[e.unit + '/' + e.n];
    if (!lid) return;
    const q = String(e.q).slice(0, 120);
    const key = lid + '|' + q;
    if (!marks[key]) marks[key] = { lid: lid, q: q, run: 0, open: true, lastWrong: null };
    const m = marks[key];
    if (e.ok) { m.open = false; return; }
    if (m.open) m.run++;
    const d = typeof e.d === 'string' ? e.d.slice(0, 10) : null;
    if (d && (!m.lastWrong || d > m.lastWrong)) m.lastWrong = d;
  });
  const byLog = Object.keys(marks).map(function (k) { return marks[k]; })
    .filter(function (m) { return m.run >= WRONG_RUN; });

  /* lesson-level evidence per unit, from the same kc rows the screen uses */
  const unitKc = {};
  Object.keys(kcScoped || {}).forEach(function (k) {
    const v = kcScoped[k] || {};
    if (typeof v.s !== 'number' || typeof v.t !== 'number') return;
    const unit = String(k).split('/')[1] || '';
    if (!unitKc[unit]) unitKc[unit] = { right: 0, total: 0 };
    unitKc[unit].right += v.s; unitKc[unit].total += v.t;
  });

  return { byBox: byBox, byLog: byLog, marks: marks, cardState: cardState,
           unitCards: unitCards, unitKc: unitKc };
}

/* "Otherwise fine": the unit's other cards are mostly holding, or the quiz
   evidence for the unit is good. The weak card is then an exception, which is
   the most actionable kind, so those sort first. */
function unitIsFine(ev, unit) {
  const uc = ev.unitCards[unit];
  if (uc && uc.tried >= UNIT_FINE_MIN_CARDS && uc.fine / uc.tried >= UNIT_FINE_SHARE) return true;
  const kc = ev.unitKc[unit];
  if (kc && kc.total >= UNIT_FINE_KC_MIN && (kc.right / kc.total) * 100 >= UNIT_FINE_KC_ACC) return true;
  return false;
}

/* Join one pupil's evidence to question text. Returns the FULL weak list,
   ranked; the caller caps it for the response and uses the whole of it for
   the class roll-up. */
function weakCardsFor(ev, textOf, course, subjectSlug, unitLabel) {
  const out = {};
  function place(key, lid, idx, question, box, attempts, lastWrong) {
    const where = course.byLessonId[lid];
    if (!where || !question) return;
    if (!out[key]) {
      out[key] = { key: key, subject: subjectSlug, unitSlug: where.unit, unitName: unitLabel(where.unit),
                   lessonNumber: where.lesson,
                   lessonTitle: course.lessonTitle[where.unit + '/' + where.lesson] || null,
                   question: String(question).slice(0, 200),
                   box: box, attempts: attempts, lastWrong: lastWrong || null,
                   unitFine: unitIsFine(ev, where.unit) };
      return;
    }
    const it = out[key];
    if (it.box == null && box != null) { it.box = box; it.attempts = attempts; }
    if (lastWrong && (!it.lastWrong || lastWrong > it.lastWrong)) it.lastWrong = lastWrong;
  }

  ev.byBox.forEach(function (c) {
    const qs = textOf[c.lid];
    const i = parseInt(String(c.idx).replace(/^q/, ''), 10);
    const q = qs && qs[i];
    if (!q) return;                                      // deck regenerated: index no longer names a card
    const m = ev.marks[c.lid + '|' + q.slice(0, 120)];
    place(c.lid + ':' + c.idx, c.lid, c.idx, q, c.box, c.attempts, m ? m.lastWrong : null);
  });

  ev.byLog.forEach(function (m) {
    const qs = textOf[m.lid] || [];
    let i = -1;
    for (let j = 0; j < qs.length; j++) { if (qs[j].slice(0, 120) === m.q) { i = j; break; } }
    if (i >= 0) {
      const st = ev.cardState[m.lid + ':q' + i] || {};
      place(m.lid + ':q' + i, m.lid, 'q' + i, qs[i],
            typeof st.box === 'number' ? st.box : null,
            typeof st.attempts === 'number' ? st.attempts : null, m.lastWrong);
    } else {
      /* the text the pupil actually saw, even if the deck has since changed */
      place(m.lid + ':t:' + m.q, m.lid, null, m.q, null, null, m.lastWrong);
    }
  });

  return Object.keys(out).map(function (k) { return out[k]; })
    .sort(function (a, b) {
      if (a.unitFine !== b.unitFine) return a.unitFine ? -1 : 1;
      const ab = a.box == null ? 99 : a.box, bb = b.box == null ? 99 : b.box;
      if (ab !== bb) return ab - bb;
      return (b.attempts || 0) - (a.attempts || 0);
    });
}

/* flashcard_questions rows are [{q|question, a|answer}] — normalise to text */
function questionTexts(list) {
  return (Array.isArray(list) ? list : []).map(function (it) {
    return String((it && (it.q || it.question)) || '');
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

  const cls = scope.cls;
  const classSubject = scope.subject;
  const base = scope.base;

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
    return res.status(200).json(Object.assign({}, shell, {
      size: 0, students: [], misconceptions: [], weakestUnits: [], missedItems: [],
      attainment: null, lessonAttainment: [], coverage: null, activity: {}, cardHotspots: []
    }));
  }

  const [{ data: rows }, { data: people }, course] = await Promise.all([
    supabase.from('progress').select('person_id, blob, updated_at').in('person_id', ids),
    supabase.from('profiles').select('id, full_name').in('id', ids),
    loadCurriculum(classSubject ? classSubject.id : null)
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

  /* "unit-slug/lesson-number" -> lesson id, the reverse of byLessonId, so a
     mark-log entry (which carries slugs) meets a card key (which carries ids) */
  const idByKey = {};
  Object.keys(course.byLessonId).forEach(function (lid) {
    const at = course.byLessonId[lid];
    idByKey[at.unit + '/' + at.lesson] = lid;
  });
  const subjectSlug = classSubject ? classSubject.slug : null;
  const cardEvidence = {};   // pupil id -> collectCards() output, joined to text below

  ids.forEach(function (id) {
    const row = (rows || []).find(function (r) { return r.person_id === id; });
    const blob = (row && row.blob) || {};
    /* card evidence is read BEFORE the scrub and reduced to attainment; the
       raw spacing state and the timestamped log go no further than this */
    cardEvidence[id] = collectCards(blob.flashsr, blob.flashlog, pick(blob.kc, base),
                                    course, subjectSlug, idByKey);
    NEVER_SEND.forEach(function (k) { delete blob[k]; });   // belt and braces

    const bucket = bucketLastActive(lastSubjectActivity(blob, base));
    activity[bucket] = (activity[bucket] || 0) + 1;

    const kcScoped = pick(blob.kc, base);
    const doneScoped = pick(blob.done, base);

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
      practiceAnswered: Array.isArray(blob.practice)
        ? blob.practice.filter(function (x) { return inScope((x && (x.k || x.key)) || '', base); }).length
        : 0,
      lastActive: bucket            // bucketed on purpose — never a timestamp
    });

    warmupByUnit(blob.warmlog, unitTally, base);
    missedQuestions(kcScoped, questionTally, id);
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

  /* Question text for the weak cards only — one fetch for the lessons any
     pupil's evidence points at, never the whole course's decks. */
  const needText = {};
  Object.keys(cardEvidence).forEach(function (id) {
    const ev = cardEvidence[id];
    ev.byBox.forEach(function (c) { needText[c.lid] = 1; });
    ev.byLog.forEach(function (m) { needText[m.lid] = 1; });
  });
  const textOf = {};
  const needIds = Object.keys(needText);
  for (let i = 0; i < needIds.length; i += 100) {
    const { data: deck } = await supabase
      .from('lessons').select('id, flashcard_questions').in('id', needIds.slice(i, i + 100));
    (deck || []).forEach(function (l) { textOf[l.id] = questionTexts(l.flashcard_questions); });
  }

  const hotTally = {};   // card key -> { card, pupils: {} }
  students.forEach(function (s) {
    const all = weakCardsFor(cardEvidence[s.id], textOf, course, subjectSlug, unitLabel);
    all.forEach(function (c) {
      if (!hotTally[c.key]) hotTally[c.key] = { card: c, pupils: {} };
      hotTally[c.key].pupils[s.id] = 1;
    });
    s.weakCards = all.slice(0, PUPIL_WEAK_CARDS).map(function (c) {
      return { subject: c.subject, unitSlug: c.unitSlug, unitName: c.unitName,
               lessonNumber: c.lessonNumber, lessonTitle: c.lessonTitle,
               question: c.question, box: c.box, attempts: c.attempts,
               lastWrong: c.lastWrong, unitFine: c.unitFine };
    });
  });

  /* The class roll-up: a card weak for several pupils is a teaching point,
     not five separate conversations. Needs two pupils, like missedItems. */
  const cardHotspots = Object.keys(hotTally).map(function (k) {
    const h = hotTally[k], c = h.card;
    return { subject: c.subject, unitSlug: c.unitSlug, unitName: c.unitName,
             lessonNumber: c.lessonNumber, lessonTitle: c.lessonTitle,
             question: c.question, pupils: Object.keys(h.pupils).length };
  }).filter(function (h) { return h.pupils >= MIN_HOTSPOT_PUPILS; })
    .sort(function (a, b) { return b.pupils - a.pupils || a.question.localeCompare(b.question); })
    .slice(0, CLASS_HOTSPOTS);

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
    return { where: q.where, question: q.question, right: q.right,
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

  return res.status(200).json(Object.assign({}, shell, {
    size: ids.length,
    students: students,
    attainment: attainment,
    lessonAttainment: lessonAttainment,
    coverage: coverage,
    misconceptions: misconceptions,
    weakestUnits: weakestUnits,
    missedItems: missedItems,
    activity: activity,
    cardHotspots: cardHotspots
  }));
};
