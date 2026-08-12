const { supabase } = require('../../pipeline/_lib/supabase');
const { pick, scrub, loadClassFor, isMember } = require('./scope');

/**
 * The parents' evening pack for one pupil.
 *
 * A NOTE ON THE BOUNDARY, because this is the one place we cross it on purpose.
 *
 * feedback_teacher_data_boundary says anything about WHEN or HOW MUCH a
 * particular child worked is aggregate-only — "Jamie revised at 11:40pm on
 * Sunday" is surveillance. This pack reports days revised and a run of daily
 * warm-up scores, which is per-child effort data.
 *
 * That is deliberate and it is a different context: the pack is printed for
 * that child's own parent, and effort is ordinary report content that every
 * school already sends home. What it must NOT become is a timeline. So:
 *
 *   - days are COUNTED and shown as dates, never as times of day
 *   - the run is capped at the last 10 sessions, not the full history
 *   - nothing here is exposed on the class screen, only on a pack a teacher
 *     deliberately opens for one pupil
 *
 * If that trade ever looks wrong, this is the file to change.
 */

const WARMUP_DAYS = 10;      // a run long enough to show a trend, short enough not to be a log
const RECENT_DAYS = 28;      // "days revised" window — a half term

function ymd(d) { return d.toISOString().slice(0, 10); }

function daysAgo(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d;
}

/* accuracy over the knowledge-check log, and the questions this pupil keeps
   getting wrong — the two things a parent actually asks about */
function fromKc(kc) {
  let right = 0, total = 0;
  const byUnit = {};
  const missTally = {};

  Object.keys(kc || {}).forEach(function (key) {
    const v = kc[key] || {};
    if (typeof v.s !== 'number' || typeof v.t !== 'number') return;
    right += v.s; total += v.t;

    const parts = key.split('/');
    const unit = parts[0] + '/' + (parts[1] || '');
    if (!byUnit[unit]) byUnit[unit] = { unit: unit, right: 0, total: 0 };
    byUnit[unit].right += v.s;
    byUnit[unit].total += v.t;

    (v.miss || []).forEach(function (m) {
      if (!m || !m.q) return;
      const k = unit + '|' + m.q;
      if (!missTally[k]) {
        missTally[k] = { unit: unit, question: String(m.q).slice(0, 180),
                         right: m.right ? String(m.right).slice(0, 120) : null, times: 0 };
      }
      missTally[k].times++;
    });
  });

  return {
    accuracy: total ? Math.round((right / total) * 100) : null,
    answered: total,
    byUnit: byUnit,
    misses: Object.keys(missTally).map(function (k) { return missTally[k]; })
                  .sort(function (a, b) { return b.times - a.times; })
  };
}

/* daily warm-up: score out of the questions attempted that day, in this subject
   only. warmlog[day] = { total, units: { "subject/unit": {a, m} } } — there is
   no top-level `correct`, so it is derived from attempts minus misses. */
function fromWarmlog(warmlog, base) {
  const days = Object.keys(warmlog || {}).sort();
  const out = [];
  days.forEach(function (d) {
    const units = pick((warmlog[d] || {}).units || {}, base);
    let a = 0, m = 0;
    Object.keys(units).forEach(function (u) { a += (units[u].a || 0); m += (units[u].m || 0); });
    if (a > 0) out.push({ date: d, right: a - m, total: a });
  });
  return out;
}

async function buildPack(auth, classId, studentId) {
  const scope = await loadClassFor(auth, classId);
  if (!scope.ok) return scope;

  if (!(await isMember(classId, studentId))) {
    /* Deliberately the same message either way. "Not in this class" and "no
       such pupil" would let a caller probe for who exists. */
    return { ok: false, status: 404, error: 'That student is not in this class.' };
  }

  const [{ data: person }, { data: row }] = await Promise.all([
    supabase.from('profiles').select('id, full_name').eq('id', studentId).maybeSingle(),
    supabase.from('progress').select('blob, updated_at').eq('person_id', studentId).maybeSingle()
  ]);

  const blob = scrub(row && row.blob);
  const base = scope.base;

  const kc = fromKc(pick(blob.kc, base));
  const done = pick(blob.done, base);
  const lessons = Object.keys(done).reduce(function (n, k) {
    return n + ((done[k] || []).length || 0);
  }, 0);

  const warm = fromWarmlog(blob.warmlog, base);
  const since = ymd(daysAgo(RECENT_DAYS));
  const daysRevised = warm.filter(function (w) { return w.date >= since; }).length;
  const lastDate = warm.length ? warm[warm.length - 1].date : null;

  /* unit names, so the pack reads "Macbeth" not "english-literature-aqa/macbeth" */
  const unitNames = {};
  if (scope.subject) {
    const { data: units } = await supabase
      .from('units').select('slug, name, sort_order')
      .eq('subject_id', scope.subject.id).order('sort_order');
    (units || []).forEach(function (u) { unitNames[u.slug] = u.name; });
  }

  function prettyUnit(key) {
    const slug = String(key).split('/')[1] || '';
    return unitNames[slug] || slug.replace(/-/g, ' ');
  }

  /* the class average per unit, so a parent can see "against the class" —
     aggregate over everyone else, never naming another child */
  const { data: members } = await supabase
    .from('class_members').select('student_id').eq('class_id', classId);
  const ids = (members || []).map(function (m) { return m.student_id; });
  const { data: allRows } = await supabase
    .from('progress').select('person_id, blob').in('person_id', ids);

  const classUnit = {};
  (allRows || []).forEach(function (r) {
    const k = fromKc(pick((r.blob || {}).kc, base));
    Object.keys(k.byUnit).forEach(function (u) {
      if (!classUnit[u]) classUnit[u] = { right: 0, total: 0 };
      classUnit[u].right += k.byUnit[u].right;
      classUnit[u].total += k.byUnit[u].total;
    });
  });

  const units = Object.keys(kc.byUnit).map(function (u) {
    const mine = kc.byUnit[u];
    const cls = classUnit[u];
    return {
      unit: prettyUnit(u),
      accuracy: mine.total >= 5 ? Math.round((mine.right / mine.total) * 100) : null,
      answered: mine.total,
      classAccuracy: cls && cls.total >= 10 ? Math.round((cls.right / cls.total) * 100) : null,
      lessonsDone: (done[u] || []).length
    };
  }).sort(function (a, b) {
    if (a.accuracy == null) return 1;
    if (b.accuracy == null) return -1;
    return a.accuracy - b.accuracy;
  });

  return {
    ok: true,
    status: 200,
    pack: {
      student: { id: studentId, name: (person && person.full_name) || 'Student' },
      class: { id: scope.cls.id, name: scope.cls.name, yearGroup: scope.cls.year_group,
               subject: scope.subject ? scope.subject.name : null },
      headline: {
        lessonsFinished: lessons,
        questionsAnswered: kc.answered,
        recallAccuracy: kc.accuracy,
        daysRevised: daysRevised,          // counted, never timestamped — see the note above
        lastRevised: lastDate
      },
      units: units,
      strongest: units.filter(function (u) { return u.accuracy != null && u.accuracy >= 75; })
                      .sort(function (a, b) { return b.accuracy - a.accuracy; }).slice(0, 4),
      keepsMissing: kc.misses.filter(function (m) { return m.times >= 2; }).slice(0, 4)
                             .map(function (m) {
                               return { unit: prettyUnit(m.unit), question: m.question,
                                        right: m.right, times: m.times };
                             }),
      warmups: warm.slice(-WARMUP_DAYS)
    }
  };
}

module.exports = { buildPack };
