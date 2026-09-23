-- The safeguarding route (23 Sep 2026): when a signed-in pupil at a school
-- writes something that may be a disclosure (an exam answer, a tutor message,
-- a flashcard answer, a search), the concern is kept here for that school's
-- safeguarding lead to review at /teacher/safeguarding. The email that tells
-- the lead carries no pupil name and no pupil words; they are only here.
--
-- Server-only table: RLS on, no policies. Only the service role reads or
-- writes it, through api/_lib/safeguard.js and api/teacher/safeguarding.js,
-- which checks that the reader is a named lead or deputy for the school.
-- Teachers never see these rows.
create table if not exists public.safeguarding_alerts (
  id            uuid primary key default gen_random_uuid(),
  school_id     uuid not null references public.schools(id) on delete cascade,
  student_id    uuid references auth.users(id) on delete set null,
  source        text not null check (source in ('exam_answer','tutor','flashcard','search')),
  page          text,                          -- where it was written, e.g. /lesson/history-aqa/...
  context       text,                          -- the question or task the pupil was answering
  body          text not null,                 -- the pupil's exact words
  decision      text not null,                 -- 'concern' or 'unsure' (the check's own word)
  category      text,
  reason        text,
  confidence    numeric(4,3),
  model         text,
  served_by     text,
  status        text not null default 'new' check (status in ('new','reviewed')),
  reviewed_by   uuid references public.profiles(id) on delete set null,
  reviewed_at   timestamptz,
  review_note   text,
  delete_after  timestamptz,                   -- reviewed_at + 90 days; unreviewed rows are never deleted
  notified_at   timestamptz,                   -- when the lead was emailed about this one (null = covered by an earlier email)
  created_at    timestamptz not null default now()
);
create index if not exists safeguarding_alerts_school_created on public.safeguarding_alerts (school_id, created_at desc);
create index if not exists safeguarding_alerts_delete_after on public.safeguarding_alerts (delete_after) where delete_after is not null;
alter table public.safeguarding_alerts enable row level security;
