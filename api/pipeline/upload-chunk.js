const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');

/**
 * Append a chunk of extracted text to an existing upload job.
 * Used when the total extracted text exceeds Vercel's 4.5 MB body limit.
 *
 * Uses Supabase RPC function append_extracted_text() to concatenate
 * directly in Postgres — the Vercel function never reads the full text.
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

  // Append chunk directly in Postgres (no read-modify-write cycle)
  const { error: rpcErr } = await supabase.rpc('append_extracted_text', {
    job_uuid: job_id,
    chunk_text: chunk,
  });

  if (rpcErr) {
    console.error('Failed to append chunk:', rpcErr);
    return res.status(500).json({ error: 'Failed to append chunk', detail: rpcErr.message });
  }

  // Mark as parsed when final chunk arrives
  if (is_last) {
    const { error: updateErr } = await supabase
      .from('upload_jobs')
      .update({ current_phase: 'parsed' })
      .eq('id', job_id);

    if (updateErr) {
      console.error('Failed to update phase:', updateErr);
      return res.status(500).json({ error: 'Failed to finalise job', detail: updateErr.message });
    }
  }

  return res.status(200).json({
    job_id,
    chunk_index,
    total_chunks: total_chunks || null,
    phase: is_last ? 'parsed' : 'uploaded',
  });
};
