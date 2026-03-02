const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');

/**
 * Approve a lesson plan and create pipeline_steps rows for each lesson.
 * Called after the teacher reviews and optionally edits the plan.
 */
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
  if (!finalPlan || !finalPlan.units) {
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
    for (const unit of finalPlan.units) {
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
      units: finalPlan.units.map(u => ({
        name: u.name,
        slug: u.slug,
        lesson_count: u.lessons.length,
      })),
    });
  } catch (err) {
    console.error('Approve plan error:', err);
    return res.status(500).json({ error: 'Failed to approve plan', detail: err.message });
  }
};
