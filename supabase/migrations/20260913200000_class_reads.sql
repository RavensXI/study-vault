-- The weekly read (13 Sep 2026): one AI-drafted paragraph set per class per week,
-- written from that week's marked answers and missed quiz questions, shown on
-- the teacher's class screen and emailed on Monday morning. Server-only table:
-- RLS on, no policies, so only the service role (the cron and the teacher API,
-- which both enforce class ownership) can read or write it.
create table if not exists public.class_reads (
  id          uuid primary key default gen_random_uuid(),
  class_id    uuid not null references public.classes(id) on delete cascade,
  school_id   uuid references public.schools(id) on delete set null,
  week        date not null,                 -- the Monday the read is for
  model       text not null,                 -- 'claude-sonnet-5' or the Haiku fallback once a school hits its cap
  served_by   text,                          -- transport that answered (bedrock:eu-west-2:... expected)
  read_md     text not null,
  answers     int  not null default 0,       -- marked answers read
  pupils      int  not null default 0,       -- distinct pupils among them
  cost_usd    numeric(8,5) not null default 0,
  emailed_at  timestamptz,
  created_at  timestamptz not null default now(),
  unique (class_id, week)
);
create index if not exists class_reads_school_created on public.class_reads (school_id, created_at desc);
alter table public.class_reads enable row level security;
