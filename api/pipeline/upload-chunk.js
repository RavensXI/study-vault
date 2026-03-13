const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');

/**
 * Append a chunk of extracted text to an existing upload job.
 * Used when the total extracted text exceeds Vercel's 4.5 MB body limit.
 *
 * POST { job_id, chunk, chunk_index, total_chunks, is_last }
 */
module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const { job_id, chunk, chunk_index, total_chunks, is_last } = req.body;

  if (!job_id || chunk === undefined || chunk_index === undefined) {
    return res.status(400).json({ error: 'Missing required fields: job_id, chunk, chunk_index' });
  }

  // Fetch current extracted_text
  const { data: job, error: fetchErr } = await supabase
    .from('upload_jobs')
    .select('id, extracted_text, current_phase')
    .eq('id', job_id)
    .single();

  if (fetchErr || !job) {
    return res.status(404).json({ error: 'Job not found' });
  }

  // Append chunk to existing text
  const currentText = job.extracted_text || '';
  const updatedText = currentText + chunk;

  const update = { extracted_text: updatedText };

  // Mark as parsed when final chunk arrives
  if (is_last) {
    update.current_phase = 'parsed';
  }

  const { error: updateErr } = await supabase
    .from('upload_jobs')
    .update(update)
    .eq('id', job_id);

  if (updateErr) {
    console.error('Failed to append chunk:', updateErr);
    return res.status(500).json({ error: 'Failed to append chunk', detail: updateErr.message });
  }

  return res.status(200).json({
    job_id,
    chunk_index,
    total_chunks: total_chunks || null,
    text_length: updatedText.length,
    phase: update.current_phase || job.current_phase,
  });
};
