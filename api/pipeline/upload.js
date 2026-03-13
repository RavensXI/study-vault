const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');
const crypto = require('crypto');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const { subject_name, exam_board, spec_code, storage_path, filename, file_hash, school_id: body_school_id, extracted_text } = req.body;

  if (!subject_name || !exam_board || !filename) {
    return res.status(400).json({ error: 'Missing required fields: subject_name, exam_board, filename' });
  }

  // Client-side parsing: extracted_text provided → skip straight to 'parsed'
  // Legacy server-side parsing: storage_path provided → start at 'uploaded'
  // Chunked upload: chunked=true → create job with no text, chunks sent via upload-chunk.js
  const chunked = req.body.chunked;
  if (!extracted_text && !storage_path && !chunked) {
    return res.status(400).json({ error: 'Either extracted_text, storage_path, or chunked flag is required' });
  }

  // Generate a slug from the subject name
  const subject_slug = subject_name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

  // Build the record — school_id and uploaded_by may be null for demo users
  const record = {
    filename,
    file_hash: file_hash || null,
    status: 'pending',
    subject_slug,
    subject_config: { subject_name, exam_board, spec_code },
    ppt_storage_path: storage_path || null,
    current_phase: extracted_text ? 'parsed' : 'uploaded',
  };

  // If text was parsed client-side, store it directly
  // For chunked uploads, initialise as empty string (chunks appended via upload-chunk.js)
  if (extracted_text) {
    record.extracted_text = extracted_text;
  } else if (chunked) {
    record.extracted_text = '';
  }
  // School from form dropdown (preferred), falling back to auth profile
  record.school_id = body_school_id || auth.profile.school_id || null;
  // Only set uploaded_by if it's a valid UUID (not a demo username)
  if (auth.profile.id && auth.profile.id.length > 10) record.uploaded_by = auth.profile.id;

  const { data: job, error } = await supabase
    .from('upload_jobs')
    .insert(record)
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
