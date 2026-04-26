-- Bug reports from the public site
-- Run via Supabase SQL Editor (idempotent — safe to re-run)

CREATE TABLE IF NOT EXISTS bug_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  message TEXT NOT NULL,
  email TEXT,
  page_url TEXT,
  screenshot_url TEXT,
  viewport_size TEXT,
  user_agent TEXT,
  status TEXT NOT NULL DEFAULT 'open',  -- open | investigating | fixed | wontfix
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  notified_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS bug_reports_status_idx ON bug_reports(status);
CREATE INDEX IF NOT EXISTS bug_reports_created_at_idx ON bug_reports(created_at DESC);

-- Public POST goes through /api/bug-report (service-key insert).
-- No public read.
ALTER TABLE bug_reports ENABLE ROW LEVEL SECURITY;
