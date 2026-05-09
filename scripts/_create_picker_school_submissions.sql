-- Picker school submissions: free-tier students optionally tell us
-- which school they're at on the last step of the wizard. Used for
-- school-level interest signal (sales targeting), no per-student PII.
--
-- Run via Supabase SQL Editor (idempotent — safe to re-run).

CREATE TABLE IF NOT EXISTS picker_school_submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  school_name TEXT NOT NULL,
  -- TRUE if the student picked from the schools-data directory, FALSE if
  -- they typed in a name the directory didn't recognise.
  is_directory_match BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS picker_school_submissions_lower_name_idx
  ON picker_school_submissions(LOWER(school_name));
CREATE INDEX IF NOT EXISTS picker_school_submissions_created_idx
  ON picker_school_submissions(created_at DESC);

-- All writes go through /api/school-submission (service role bypasses RLS).
-- No public read — only admin via /api/admin/school-submissions.
ALTER TABLE picker_school_submissions ENABLE ROW LEVEL SECURITY;
