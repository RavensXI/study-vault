-- Pipeline Asset Metadata: columns for subject-agnostic asset scripts
-- Adds per-lesson metadata to pipeline_steps so narration, diagram, and hero
-- scripts can operate without hardcoded subject data.

-- ============================================================
-- NEW COLUMNS on pipeline_steps
-- ============================================================

ALTER TABLE pipeline_steps
  ADD COLUMN IF NOT EXISTS diagram_prompt  text,
  ADD COLUMN IF NOT EXISTS hero_keywords   text[],
  ADD COLUMN IF NOT EXISTS subject_slug    text,
  ADD COLUMN IF NOT EXISTS diagram_style   text DEFAULT 'gemini_only';

-- Constraint: diagram_style must be a known value
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'pipeline_steps_diagram_style_check'
  ) THEN
    ALTER TABLE pipeline_steps
      ADD CONSTRAINT pipeline_steps_diagram_style_check
      CHECK (diagram_style IN ('gemini_only', 'matplotlib_gemini'));
  END IF;
END $$;

-- ============================================================
-- PARTIAL INDEXES for efficient script queries
-- ============================================================

-- Narration script: find lessons needing narration for a given job
CREATE INDEX IF NOT EXISTS idx_pipeline_steps_narration_pending
  ON pipeline_steps (job_id)
  WHERE narration_done = false AND content_done = true;

-- Diagram script: find lessons needing diagrams for a given job
CREATE INDEX IF NOT EXISTS idx_pipeline_steps_diagrams_pending
  ON pipeline_steps (job_id)
  WHERE diagrams_done = false AND content_done = true;

-- Hero script: find lessons needing hero images for a given job
CREATE INDEX IF NOT EXISTS idx_pipeline_steps_hero_pending
  ON pipeline_steps (job_id)
  WHERE hero_done = false AND content_done = true;

-- Media curation: find lessons needing related media
CREATE INDEX IF NOT EXISTS idx_pipeline_steps_media_pending
  ON pipeline_steps (job_id)
  WHERE media_done = false AND content_done = true;
