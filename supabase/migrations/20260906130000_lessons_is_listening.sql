-- 6 Sep 2026: third lesson format. A listening lesson is an article row whose
-- body carries the Music set-work stage (class "sv-listening"). Derived from
-- the content so it can never drift from what the page actually renders;
-- stored + indexed so /admin/build-status can filter on it without scanning
-- ~50 MB of content_html (which hit the statement timeout).
ALTER TABLE public.lessons
  ADD COLUMN IF NOT EXISTS is_listening boolean
  GENERATED ALWAYS AS (COALESCE(content_html, '') LIKE '%sv-listening%') STORED;
CREATE INDEX IF NOT EXISTS idx_lessons_is_listening ON public.lessons (is_listening) WHERE is_listening;
