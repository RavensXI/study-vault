const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const { job_id, latest, list } = req.query;

  // List all jobs (for job dashboard)
  if (list) {
    const { data: jobs } = await supabase
      .from('upload_jobs')
      .select('id, filename, status, current_phase, subject_slug, subject_config, lessons_created, created_at, updated_at, schools(name)')
      .order('created_at', { ascending: false })
      .limit(50);

    // Get step counts per job
    const jobIds = (jobs || []).map(j => j.id);
    const { data: stepCounts } = jobIds.length > 0
      ? await supabase
          .from('pipeline_steps')
          .select('job_id, content_done, diagrams_done, hero_done, narration_done, media_done')
          .in('job_id', jobIds)
      : { data: [] };

    // Aggregate counts per job
    const countsByJob = {};
    for (const s of (stepCounts || [])) {
      if (!countsByJob[s.job_id]) countsByJob[s.job_id] = { total: 0, content: 0, diagrams: 0, heroes: 0, narration: 0, media: 0 };
      const c = countsByJob[s.job_id];
      c.total++;
      if (s.content_done) c.content++;
      if (s.diagrams_done) c.diagrams++;
      if (s.hero_done) c.heroes++;
      if (s.narration_done) c.narration++;
      if (s.media_done) c.media++;
    }

    // Fetch schools list for the dropdown
    const { data: schools } = await supabase
      .from('schools')
      .select('id, name, slug')
      .order('name');

    const enriched = (jobs || []).map(j => ({
      ...j,
      subject_name: (j.subject_config || {}).subject_name || j.subject_slug || '—',
      school_name: j.schools?.name || '—',
      counts: countsByJob[j.id] || { total: 0, content: 0, diagrams: 0, heroes: 0, narration: 0, media: 0 },
    }));
    // Remove nested schools object from response
    enriched.forEach(j => delete j.schools);

    return res.status(200).json({ jobs: enriched, schools: schools || [] });
  }

  let job;

  if (latest) {
    // Find the most recent active job
    const { data: jobs } = await supabase
      .from('upload_jobs')
      .select('id, filename, status, current_phase, subject_slug, subject_config, lesson_plan, lessons_created, error_message, created_at, updated_at')
      .in('current_phase', ['uploaded', 'parsed', 'planned', 'generating'])
      .order('created_at', { ascending: false })
      .limit(1);

    job = jobs?.[0] || null;
    if (!job) {
      return res.status(200).json({ job: null, steps: [], summary: { total: 0 } });
    }
  } else {
    if (!job_id) {
      return res.status(400).json({ error: 'Missing job_id query parameter' });
    }
    const { data, error: jobError } = await supabase
      .from('upload_jobs')
      .select('id, filename, status, current_phase, subject_slug, subject_config, lesson_plan, lessons_created, error_message, extracted_text, created_at, updated_at')
      .eq('id', job_id)
      .single();

    if (jobError || !data) {
      return res.status(404).json({ error: 'Upload job not found' });
    }
    job = data;
  }

  // Fetch pipeline steps (use job.id — handles both job_id param and latest lookup)
  const { data: steps, error: stepsError } = await supabase
    .from('pipeline_steps')
    .select('id, lesson_id, unit_slug, lesson_number, lesson_title, content_done, questions_done, glossary_done, diagrams_done, narration_done, media_done, hero_done, last_error, retry_count')
    .eq('job_id', job.id)
    .order('unit_slug')
    .order('lesson_number');

  // Build summary
  const totalSteps = steps?.length || 0;
  const contentComplete = steps?.filter(s => s.content_done).length || 0;
  const questionsComplete = steps?.filter(s => s.questions_done).length || 0;
  const diagramsComplete = steps?.filter(s => s.diagrams_done).length || 0;
  const narrationComplete = steps?.filter(s => s.narration_done).length || 0;
  const heroComplete = steps?.filter(s => s.hero_done).length || 0;
  const mediaComplete = steps?.filter(s => s.media_done).length || 0;
  const errorCount = steps?.filter(s => s.last_error).length || 0;
  const allContentDone = totalSteps > 0 && contentComplete === totalSteps;

  // Send text length + preview, not the full extracted text
  const textLen = job.extracted_text ? job.extracted_text.length : 0;
  const textPreview = job.extracted_text ? job.extracted_text.substring(0, 600) : '';
  delete job.extracted_text;
  job.extracted_text_length = textLen;
  job.extracted_text_preview = textPreview;

  return res.status(200).json({
    job,
    steps: steps || [],
    summary: {
      total: totalSteps,
      content_complete: contentComplete,
      questions_complete: questionsComplete,
      diagrams_complete: diagramsComplete,
      narration_complete: narrationComplete,
      hero_complete: heroComplete,
      media_complete: mediaComplete,
      error_count: errorCount,
      all_content_done: allContentDone,
    },
  });
};
