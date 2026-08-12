const { supabase } = require('./supabase');

/**
 * Forget a department's source material once their lessons are published.
 *
 * WHY THIS EXISTS. The upload pipeline already does the hard part: .pptx and
 * .pdf files are unpacked in the browser and never leave the school's machine —
 * only extracted text is posted. But that text was then kept for ever. Today
 * seventeen jobs still hold roughly 32 million characters of Unity's own
 * teaching resources, from builds that finished in March.
 *
 * The difference matters commercially. "Nobody at StudyVault reads your
 * resources" is a promise about our conduct. "The files never left your
 * building, and the text we extracted no longer exists" is a property of the
 * system, and it is the version that survives a DPO's questions.
 *
 * WHY PUBLISH AND NOT BUILD-COMPLETE. Tom's call, and the right one: between
 * building and publishing there is usually more work — a re-run, a fix, a
 * regenerated unit — and all of it needs the source. Deleting when the build
 * finishes would strip it at exactly the moment it is most likely to be needed
 * and force a department to upload everything again. Publishing is the point at
 * which they have accepted the output, so it is the point at which the raw
 * material has done its job.
 *
 * The job row itself is KEPT — filename, subject, counts, timestamps. Only the
 * text goes. That leaves an audit trail showing what was built from what,
 * without holding the content.
 */

/* Statuses that mean a lesson has NOT yet reached the department. While any
   lesson in the subject is still in one of these, the source is still in use. */
const UNFINISHED = ['pending_review', 'ready_for_teacher', 'publishing', 'awaiting_qa', 'draft'];

/**
 * Called after a publish succeeds. Non-fatal by design: forgetting the source
 * is important, but it must never turn a successful publish into an error the
 * teacher sees.
 *
 * @param {string[]} lessonIds lessons that were just published
 */
async function forgetSourceIfPublished(lessonIds) {
  try {
    if (!lessonIds || !lessonIds.length) return { cleared: 0 };

    /* Which subjects did those lessons belong to? */
    const { data: rows } = await supabase
      .from('lessons')
      .select('id, units!inner(subject_id, subjects!inner(id, slug, school_id))')
      .in('id', lessonIds);

    const subjects = {};
    (rows || []).forEach(function (r) {
      const s = r.units.subjects;
      subjects[s.id] = { id: s.id, slug: s.slug, school_id: s.school_id };
    });

    let cleared = 0;

    for (const key of Object.keys(subjects)) {
      const subj = subjects[key];

      /* Only when the WHOLE subject is through. Publishing one unit of a
         fourteen-unit build must not delete the source the other thirteen
         still need. */
      const { data: units } = await supabase
        .from('units').select('id').eq('subject_id', subj.id);
      const unitIds = (units || []).map(function (u) { return u.id; });
      if (!unitIds.length) continue;

      const { count: outstanding } = await supabase
        .from('lessons')
        .select('id', { count: 'exact', head: true })
        .in('unit_id', unitIds)
        .in('status', UNFINISHED);

      if (outstanding && outstanding > 0) continue;

      /* Match jobs by subject and school. The alternative link is
         lessons.source_ppt_hash against upload_jobs.file_hash, which is exact
         but only populated on some rows; subject + school is the pairing that
         actually holds across the whole table. */
      let q = supabase
        .from('upload_jobs')
        .update({ extracted_text: null })
        .eq('subject_slug', subj.slug)
        .not('extracted_text', 'is', null);

      q = subj.school_id ? q.eq('school_id', subj.school_id) : q.is('school_id', null);

      const { data: done } = await q.select('id');
      cleared += (done || []).length;
    }

    if (cleared) {
      console.log('[forget-source] published subject complete — cleared extracted text from',
        cleared, 'upload job(s)');
    }
    return { cleared: cleared };
  } catch (err) {
    /* Never fail a publish over this. Log it so it can be swept up instead. */
    console.error('[forget-source] could not clear source text:', err.message);
    return { cleared: 0, error: err.message };
  }
}

module.exports = { forgetSourceIfPublished, UNFINISHED };
