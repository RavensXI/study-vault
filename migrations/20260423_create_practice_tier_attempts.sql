-- Practice tier attempts — per-student per-tier per-attempt record.
-- Source of truth for future teacher dashboards: "how many attempts did
-- students need at this lesson's silver tier?", "which tiers get retried
-- most often?", "what % of students reach gold on this subject?"
--
-- Client writes one row every time a student completes a tier (pass OR fail).
-- Client code in practice.html: recordTierAttempt()
--
-- Run this in the Supabase SQL editor to enable persistence. Until the table
-- exists, the client silently falls back to localStorage only — running this
-- migration later doesn't lose anything, it just starts collecting new data.

create table if not exists public.practice_tier_attempts (
  id             uuid primary key default gen_random_uuid(),
  user_id        text not null,                       -- Supabase user id for logged-in; 'anon-...' for free-tier
  lesson_id      uuid not null references public.lessons(id) on delete cascade,
  tier           text not null check (tier in ('bronze', 'silver', 'gold')),
  attempt_number integer not null check (attempt_number >= 1),
  correct        integer not null check (correct >= 0),
  attempted      integer not null check (attempted >= 0),
  tier_total     integer not null check (tier_total >= 0),
  passed         boolean not null,
  completed_at   timestamptz not null default now()
);

-- Indexes for the most likely dashboard queries
create index if not exists idx_pta_lesson_tier on public.practice_tier_attempts (lesson_id, tier);
create index if not exists idx_pta_user on public.practice_tier_attempts (user_id);
create index if not exists idx_pta_completed on public.practice_tier_attempts (completed_at desc);

-- RLS: anon can insert (so free-tier students contribute data); authenticated
-- users can read their own rows; teachers/admins can read their school's rows.
alter table public.practice_tier_attempts enable row level security;

-- Allow inserts from anyone (anon + authed). We trust the user_id string —
-- it's either a Supabase auth id or a localStorage-generated 'anon-...'
-- identifier. Abuse surface is bounded (a row per tier attempt).
create policy "Anyone can record a tier attempt"
  on public.practice_tier_attempts
  for insert
  with check (true);

-- Students can read their own attempts
create policy "Users read their own attempts"
  on public.practice_tier_attempts
  for select
  using (auth.uid()::text = user_id);

-- Admins read everything (service key bypasses RLS)
-- Teachers would get a separate policy once the teacher dashboard lands.
