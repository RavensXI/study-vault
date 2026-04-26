-- Subject requests from the public homepage
-- Run via Supabase SQL Editor (idempotent — safe to re-run)

CREATE TABLE IF NOT EXISTS subject_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_name TEXT NOT NULL,
  topic TEXT,
  exam_board TEXT,
  email TEXT,
  notes TEXT,
  status TEXT NOT NULL DEFAULT 'pending',  -- pending | building | live | rejected
  user_agent TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  notified_at TIMESTAMPTZ
);

-- Add topic column for tables created before that field existed
ALTER TABLE subject_requests ADD COLUMN IF NOT EXISTS topic TEXT;

CREATE INDEX IF NOT EXISTS subject_requests_status_idx ON subject_requests(status);
CREATE INDEX IF NOT EXISTS subject_requests_created_at_idx ON subject_requests(created_at DESC);

-- Public can insert (writes go through /api/subject-request, so RLS just needs to allow service-role bypass).
-- No public read — only admin.
ALTER TABLE subject_requests ENABLE ROW LEVEL SECURITY;
