const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const { job_id } = req.query;
  if (!job_id) {
    return res.status(400).json({ error: 'Missing job_id query parameter' });
  }

  // Fetch the upload job
  const { data: job, error: jobError } = await supabase
    .from('upload_jobs')
    .select('id, filename, status, current_phase, subject_slug, subject_config, lesson_plan, lessons_created, error_message, created_at, updated_at')
    .eq('id', job_id)
    .single();

  if (jobError || !job) {
    return res.status(404).json({ error: 'Upload job not found' });
  }

  // Fetch pipeline steps
  const { data: steps, error: stepsError } = await supabase
    .from('pipeline_steps')
    .select('id, lesson_id, unit_slug, lesson_number, lesson_title, content_done, questions_done, glossary_done, diagrams_done, narration_done, media_done, hero_done, last_error, retry_count')
    .eq('job_id', job_id)
    .order('unit_slug')
    .order('lesson_number');

  // Build summary
  const totalSteps = steps?.length || 0;
  const contentComplete = steps?.filter(s => s.content_done).length || 0;
  const questionsComplete = steps?.filter(s => s.questions_done).length || 0;
  const diagramsComplete = steps?.filter(s => s.diagrams_done).length || 0;
  const narrationComplete = steps?.filter(s => s.narration_done).length || 0;
  const allContentDone = totalSteps > 0 && contentComplete === totalSteps;

  return res.status(200).json({
    job,
    steps: steps || [],
    summary: {
      total: totalSteps,
      content_complete: contentComplete,
      questions_complete: questionsComplete,
      diagrams_complete: diagramsComplete,
      narration_complete: narrationComplete,
      all_content_done: allContentDone,
    },
  });
};
