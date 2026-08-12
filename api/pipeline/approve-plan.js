const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');

/**
 * Approve a lesson plan and create pipeline_steps rows for each lesson.
 * Called after the teacher reviews and optionally edits the plan.
 */
/**
 * Every unit in the plan, each tagged with its format.
 *
 * Accepts the current planner's split arrays AND the flat `units` array older
 * jobs were stored with. An older plan has no format field at all, and article
 * is the right assumption there: practice-format subjects did not exist when
 * those plans were written, so nothing in them can be practice.
 */
function collectUnits(plan) {
  if (!plan) return [];
  const out = [];
  (plan.article_units || []).forEach(function (u) {
    out.push(Object.assign({}, u, { format: 'article' }));
  });
  (plan.practice_units || []).forEach(function (u) {
    out.push(Object.assign({}, u, { format: 'practice' }));
  });
  if (!out.length && Array.isArray(plan.units)) {
    plan.units.forEach(function (u) {
      out.push(Object.assign({}, u, { format: u.format || 'article' }));
    });
  }
  /* sort_order is in the current schema and absent from the old one; fall back
     to the order they arrived in rather than shuffling legacy plans. */
  return out.map(function (u, i) {
    return Object.assign({}, u, { sort_order: u.sort_order != null ? u.sort_order : i + 1 });
  }).sort(function (a, b) { return a.sort_order - b.sort_order; });
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const { job_id, plan, colors, action } = req.body;
  if (!job_id) {
    return res.status(400).json({ error: 'Missing job_id' });
  }

  // Handle "send to review" action
  if (action === 'send_to_review') {
    const { data: steps } = await supabase
      .from('pipeline_steps')
      .select('lesson_id, content_done')
      .eq('job_id', job_id);

    let count = 0;
    for (const s of (steps || [])) {
      if (s.content_done && s.lesson_id) {
        await supabase.from('lessons').update({ status: 'review' }).eq('id', s.lesson_id);
        count++;
      }
    }
    await supabase.from('upload_jobs').update({ current_phase: 'complete' }).eq('id', job_id);
    return res.status(200).json({ status: 'sent_to_review', lessons_count: count });
  }

  // Fetch the upload job
  const { data: job, error: jobError } = await supabase
    .from('upload_jobs')
    .select('*')
    .eq('id', job_id)
    .single();

  if (jobError || !job) {
    return res.status(404).json({ error: 'Upload job not found' });
  }

  // Use the provided (possibly edited) plan, or fall back to the stored plan
  const finalPlan = plan || job.lesson_plan;

  /* FORMAT-AWARE PLANS.
   *
   * This endpoint predates practice-format lessons. It read finalPlan.units and
   * nothing else, so a plan produced by the current planner — which emits
   * article_units and practice_units as separate arrays, exactly as
   * docs/PLANNING_PROMPT.md specifies — would have had every practice unit
   * silently dropped. No error, just a subject that quietly came out
   * article-only.
   *
   * Both shapes are accepted: the legacy flat `units`, and the split arrays.
   * Each unit carries its format forward so the rest of the build, and
   * subjects.settings.practice_units, can route it to /practice/ rather than
   * /lesson/.
   */
  const planUnits = collectUnits(finalPlan);
  if (!finalPlan || !planUnits.length) {
    return res.status(400).json({ error: 'No plan available. Run /api/pipeline/plan first.' });
  }

  try {
    // Update the plan (teacher may have edited lesson titles or removed lessons)
    const updatedConfig = {
      ...job.subject_config,
      colors: colors || job.subject_config?.colors || {},
    };

    await supabase.from('upload_jobs').update({
      lesson_plan: finalPlan,
      subject_config: updatedConfig,
      current_phase: 'planned',
    }).eq('id', job_id);

    // Create pipeline_steps for each lesson
    const steps = [];
    for (const unit of planUnits) {
      for (const lesson of unit.lessons) {
        steps.push({
          job_id,
          unit_slug: unit.slug,
          lesson_number: lesson.number,
          lesson_title: lesson.title,
        });
      }
    }

    // Upsert steps (idempotent — won't overwrite existing progress)
    const { error: stepsError } = await supabase
      .from('pipeline_steps')
      .upsert(steps, { onConflict: 'job_id,unit_slug,lesson_number', ignoreDuplicates: true });

    if (stepsError) {
      throw new Error(`Failed to create pipeline steps: ${stepsError.message}`);
    }

    const totalLessons = steps.length;

    return res.status(200).json({
      job_id,
      status: 'planned',
      total_lessons: totalLessons,
      units: planUnits.map(u => ({
        name: u.name,
        slug: u.slug,
        format: u.format,
        lesson_count: (u.lessons || []).length,
      })),
      /* what browse-loader needs in subjects.settings to send these units to
         /practice/ instead of /lesson/ */
      practice_units: planUnits.filter(u => u.format === 'practice').map(u => u.slug),
    });
  } catch (err) {
    console.error('Approve plan error:', err);
    return res.status(500).json({ error: 'Failed to approve plan', detail: err.message });
  }
};
