-- StudyVault Pipeline: Upload-to-Lesson Generation Schema
-- Adds pipeline tracking tables and extends upload_jobs for the content generation pipeline.

-- ============================================================
-- EXTEND upload_jobs
-- ============================================================

ALTER TABLE upload_jobs
  ADD COLUMN IF NOT EXISTS subject_slug text,
  ADD COLUMN IF NOT EXISTS subject_config jsonb DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS ppt_storage_path text,
  ADD COLUMN IF NOT EXISTS extracted_text text,
  ADD COLUMN IF NOT EXISTS lesson_plan jsonb,
  ADD COLUMN IF NOT EXISTS current_phase text DEFAULT 'uploaded',
  ADD COLUMN IF NOT EXISTS updated_at timestamptz DEFAULT now();

-- Phase check constraint (separate statement for IF NOT EXISTS compatibility)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'upload_jobs_phase_check'
  ) THEN
    ALTER TABLE upload_jobs
      ADD CONSTRAINT upload_jobs_phase_check
      CHECK (current_phase IN ('uploaded','parsing','parsed','planning','planned','generating','complete','failed'));
  END IF;
END $$;

-- ============================================================
-- pipeline_steps — per-lesson progress tracking
-- ============================================================

CREATE TABLE IF NOT EXISTS pipeline_steps (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id          uuid NOT NULL REFERENCES upload_jobs(id) ON DELETE CASCADE,
  lesson_id       uuid REFERENCES lessons(id),
  unit_slug       text NOT NULL,
  lesson_number   smallint NOT NULL,
  lesson_title    text NOT NULL,

  -- Step completion flags
  content_done    boolean DEFAULT false,
  questions_done  boolean DEFAULT false,
  glossary_done   boolean DEFAULT false,
  diagrams_done   boolean DEFAULT false,
  narration_done  boolean DEFAULT false,
  media_done      boolean DEFAULT false,
  hero_done       boolean DEFAULT false,

  -- Error tracking
  last_error      text,
  retry_count     smallint DEFAULT 0,

  created_at      timestamptz DEFAULT now(),
  updated_at      timestamptz DEFAULT now(),

  UNIQUE(job_id, unit_slug, lesson_number)
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_pipeline_steps_job ON pipeline_steps (job_id);
CREATE INDEX IF NOT EXISTS idx_upload_jobs_phase ON upload_jobs (current_phase);

-- ============================================================
-- TRIGGERS
-- ============================================================

-- Auto-update updated_at on pipeline_steps
CREATE TRIGGER update_pipeline_steps_updated_at
  BEFORE UPDATE ON pipeline_steps
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Auto-update updated_at on upload_jobs (function already exists from 001)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger WHERE tgname = 'update_upload_jobs_updated_at'
  ) THEN
    CREATE TRIGGER update_upload_jobs_updated_at
      BEFORE UPDATE ON upload_jobs
      FOR EACH ROW EXECUTE FUNCTION update_updated_at();
  END IF;
END $$;

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE pipeline_steps ENABLE ROW LEVEL SECURITY;

-- Platform admin: full access
CREATE POLICY "Platform admin full access on pipeline_steps"
  ON pipeline_steps FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

-- Teachers can view their school's pipeline steps
CREATE POLICY "Teachers can view their school pipeline steps"
  ON pipeline_steps FOR SELECT
  USING (
    job_id IN (
      SELECT id FROM upload_jobs
      WHERE school_id = current_user_school_id()
    )
    AND current_user_role() IN ('teacher', 'school_admin')
  );

-- ============================================================
-- SUPABASE STORAGE BUCKET (run separately if needed)
-- ============================================================
-- Note: Supabase Storage buckets are created via the Dashboard or
-- the storage API, not via SQL migrations. Create the
-- 'pipeline-uploads' bucket manually in Dashboard > Storage.
