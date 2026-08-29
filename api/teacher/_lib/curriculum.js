const { supabase } = require('../../pipeline/_lib/supabase');

/**
 * The shape of a subject's course: its units, and the live lessons inside them.
 *
 * Two jobs, both of which the class screen needs and neither of which the
 * progress blob can answer on its own:
 *
 *   NAMES      a progress key is "english-literature-aqa/romeo-and-juliet/4".
 *              A teacher reads "Romeo and Juliet — L4 The Fight Scene". Every
 *              figure we show has to be pinned to something they recognise or
 *              they cannot act on it.
 *   DENOMINATORS coverage is meaningless without them. "Nine lessons done" is
 *              a number; "nine of ten" is a decision about what to teach next.
 *
 * Only `live` lessons count. A lesson still at pending_review is not visible to
 * a pupil, so including it would report a class as behind on work it has never
 * been able to see.
 *
 * lesson_visits is keyed by lesson UUID, so the id map is built here too — it is
 * the only way to turn a visit row into a place in the course.
 */
async function loadCurriculum(subjectId) {
  const empty = {
    units: [],
    unitName: {},
    practiceUnit: {},
    liveCount: {},
    lessonTitle: {},
    byLessonId: {},
    totalLessons: 0
  };
  if (!subjectId) return empty;

  const { data: subject } = await supabase
    .from('subjects').select('id, settings').eq('id', subjectId).maybeSingle();

  const { data: units } = await supabase
    .from('units').select('id, slug, name, sort_order')
    .eq('subject_id', subjectId).order('sort_order');
  if (!units || !units.length) return empty;

  const slugOf = {};
  const out = Object.assign({}, empty, { units: [] });

  /* Practice units carry no knowledge check, so a class working through them
     shows blank attainment for ever. Flagging them lets the screen say "no quiz
     on practice units" instead of leaving a teacher to wonder what is broken. */
  const practice = ((subject && subject.settings && subject.settings.practice_units) || []);

  units.forEach(function (u) {
    slugOf[u.id] = u.slug;
    out.unitName[u.slug] = u.name;
    out.practiceUnit[u.slug] = practice.indexOf(u.slug) >= 0;
    out.liveCount[u.slug] = 0;
    out.units.push({ slug: u.slug, name: u.name });
  });

  const { data: lessons } = await supabase
    .from('lessons').select('id, unit_id, lesson_number, title, status')
    .in('unit_id', units.map(function (u) { return u.id; }));

  (lessons || []).forEach(function (l) {
    const slug = slugOf[l.unit_id];
    if (!slug) return;
    const key = slug + '/' + l.lesson_number;
    out.lessonTitle[key] = l.title;
    out.byLessonId[l.id] = { unit: slug, lesson: l.lesson_number };
    if (l.status === 'live') {
      out.liveCount[slug] = (out.liveCount[slug] || 0) + 1;
      out.totalLessons++;
    }
  });

  return out;
}

module.exports = { loadCurriculum };
