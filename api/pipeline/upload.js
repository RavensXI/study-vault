const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');
const crypto = require('crypto');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const { subject_name, exam_board, spec_code, storage_path, filename, file_hash } = req.body;

  if (!subject_name || !exam_board || !storage_path || !filename) {
    return res.status(400).json({ error: 'Missing required fields: subject_name, exam_board, storage_path, filename' });
  }

  // Generate a slug from the subject name
  const subject_slug = subject_name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

  // Create the upload_job record
  const { data: job, error } = await supabase
    .from('upload_jobs')
    .insert({
      school_id: auth.profile.school_id,
      uploaded_by: auth.profile.id,
      filename,
      file_hash: file_hash || null,
      status: 'pending',
      subject_slug,
      subject_config: { subject_name, exam_board, spec_code },
      ppt_storage_path: storage_path,
      current_phase: 'uploaded',
    })
    .select('id, status, current_phase')
    .single();

  if (error) {
    console.error('Failed to create upload_job:', error);
    return res.status(500).json({ error: 'Failed to create upload job', detail: error.message });
  }

  return res.status(201).json({
    job_id: job.id,
    status: job.status,
    current_phase: job.current_phase,
  });
};
