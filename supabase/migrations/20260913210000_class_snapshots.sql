-- Weekly class snapshots (13 Sep 2026): what the class screen showed on a Monday,
-- so next Monday can say what moved ("4 more secure than last week"). Class-level
-- counts only — per unit: score, secure/developing/emerging/nothing-yet counts,
-- how many need to revise it again; plus quiz answers right, pupils with a quiz,
-- marked answers. Never per pupil (feedback_teacher_data_boundary). Written by
-- api/cron/weekly-reads.js. RLS on, no policies: service role only.
create table if not exists public.class_snapshots (
  id         uuid primary key default gen_random_uuid(),
  class_id   uuid not null references public.classes(id) on delete cascade,
  week       date not null,
  data       jsonb not null,
  created_at timestamptz not null default now(),
  unique (class_id, week)
);
alter table public.class_snapshots enable row level security;
