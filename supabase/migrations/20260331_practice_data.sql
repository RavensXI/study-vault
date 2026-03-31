-- Add practice_data JSONB column for practice-first lesson format
-- Used by maths (and potentially science) for method cards, worked examples, and problem banks
ALTER TABLE lessons ADD COLUMN IF NOT EXISTS practice_data jsonb DEFAULT '{}';
