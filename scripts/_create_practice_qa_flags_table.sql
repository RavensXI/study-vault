-- Migration: create practice_qa_flags table
-- Run once via psql or Supabase SQL editor.

CREATE TABLE IF NOT EXISTS practice_qa_flags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  problem_path TEXT NOT NULL,
  note TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','fixed','wontfix','duplicate')),
  created_at TIMESTAMPTZ DEFAULT now(),
  fixed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS practice_qa_flags_status_idx ON practice_qa_flags (status, created_at DESC);
CREATE INDEX IF NOT EXISTS practice_qa_flags_lesson_idx ON practice_qa_flags (lesson_id);
