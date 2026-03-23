-- Pipeline Phase Split: add publishing + awaiting_qa statuses and enrichment tracking columns

-- Add new enum values to content_status
ALTER TYPE content_status ADD VALUE IF NOT EXISTS 'publishing';
ALTER TYPE content_status ADD VALUE IF NOT EXISTS 'awaiting_qa';

-- Add enrichment tracking columns to lessons
ALTER TABLE lessons ADD COLUMN IF NOT EXISTS enrichment_started_at timestamptz;
ALTER TABLE lessons ADD COLUMN IF NOT EXISTS enrichment_completed_at timestamptz;
ALTER TABLE lessons ADD COLUMN IF NOT EXISTS enrichment_error text;

-- Partial indexes for efficient polling of the new statuses
CREATE INDEX IF NOT EXISTS idx_lessons_publishing ON lessons (status) WHERE status = 'publishing';
CREATE INDEX IF NOT EXISTS idx_lessons_awaiting_qa ON lessons (status) WHERE status = 'awaiting_qa';
