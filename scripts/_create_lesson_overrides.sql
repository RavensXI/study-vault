-- ===========================================================================
--  lesson_overrides — school edits to shared free-tier lessons
--  Run this in the Supabase SQL editor. There is no SQL RPC on this project,
--  so schema changes cannot be applied from a script.
-- ===========================================================================
--
-- WHY A SEPARATE TABLE, NOT A FORKED ROW IN `lessons`
--
-- About forty places read `lessons`, and nine of them serve the public:
-- browse, lesson, practice, home counts, /exams, revise, the podcast RSS feed.
-- A forked row sitting in `lessons` under the same unit would be returned by
-- every one of those queries unless each was taught to filter it out. One
-- missed filter puts a school's private content on the public site.
--
-- An override table inverts that. Every existing query keeps returning the
-- generic lesson untouched, and only the loaders that SHOULD show school
-- content do a second lookup. Safe by default rather than safe if we
-- remembered.
--
-- It also gives inheritance at FIELD level. A school that rewrites the
-- knowledge checks stores only knowledge_checks; the article body stays NULL
-- and keeps receiving our fact-check corrections and spec updates. Lesson-level
-- forking would freeze the whole lesson the moment anyone touched a comma.
--
-- The editable set below is exactly what api/pipeline/update-lesson.js and
-- update-hero.js can write — no more. Note `title` is NOT editable, which is
-- why browse listings and lesson counts need no changes at all.
-- ===========================================================================

create table if not exists public.lesson_overrides (
  id                  uuid primary key default gen_random_uuid(),
  lesson_id           uuid not null references public.lessons(id) on delete cascade,
  school_id           uuid not null references public.schools(id) on delete cascade,

  -- NULL means "inherit from the base lesson". Only fields the school actually
  -- changed are ever written.
  content_html        text,
  exam_tip_html       text,
  conclusion_html     text,
  practice_questions  jsonb,
  knowledge_checks    jsonb,
  flashcard_questions jsonb,
  glossary_terms      jsonb,
  hero_image_url      text,
  hero_image_alt      text,
  hero_image_caption  text,
  hero_image_position text,

  -- Fingerprint of the base lesson's editable fields at the moment the school
  -- first edited it. Compare against the live base to answer "has StudyVault
  -- changed the original since we took our copy?" — which is what lets us show
  -- a school what moved instead of silently replacing their work.
  forked_from_version text not null,

  created_by          text,
  updated_by          text,
  created_at          timestamptz not null default now(),
  updated_at          timestamptz not null default now(),

  -- one override per lesson per school
  unique (lesson_id, school_id)
);

create index if not exists lesson_overrides_school_idx
  on public.lesson_overrides (school_id, lesson_id);

alter table public.lesson_overrides enable row level security;

-- Reads match the posture of `lessons` today: the browser reads with the anon
-- key, so select is open. (Bespoke content being anon-readable is a known open
-- item from the June security review and is not made worse here.)
drop policy if exists lesson_overrides_read on public.lesson_overrides;
create policy lesson_overrides_read
  on public.lesson_overrides for select
  using (true);

-- No insert/update/delete policy is defined on purpose. Writes are only
-- possible with the service key, which means only through the API — where
-- api/pipeline/_lib/scope.js has already checked the caller owns the school.

comment on table public.lesson_overrides is
  'School-specific edits layered over shared free-tier lessons. NULL column = inherit from lessons. Written only by the pipeline API under scope.js ownership checks.';
