-- Add Foundation/Higher tier column to lessons
-- Values: 'both' (default), 'foundation', 'higher'
-- Used by tiered subjects: Maths, Science, Separate Sciences, Languages

ALTER TABLE lessons
ADD COLUMN IF NOT EXISTS tier text NOT NULL DEFAULT 'both'
CHECK (tier IN ('foundation', 'higher', 'both'));

-- Index for efficient tier filtering on browse pages
CREATE INDEX IF NOT EXISTS idx_lessons_tier ON lessons (tier) WHERE tier != 'both';

COMMENT ON COLUMN lessons.tier IS 'Foundation/Higher tier: both (default), foundation, or higher. Foundation students see both+foundation, Higher students see all.';
