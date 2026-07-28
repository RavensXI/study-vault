-- The real fix for the JWT-bloat finding (28 Jul): progress lives in a
-- TABLE, not in user_metadata (Supabase embeds metadata in every access
-- token; a term of history overflowed Cloudflare's header limits and
-- 520'd all of a student's content requests). One row per person, the
-- whole sv_progress object as jsonb, own-row RLS. Teachers never read
-- this - class evidence comes from public.events.

create table if not exists public.progress (
  person_id  uuid primary key references auth.users (id) on delete cascade,
  school_id  uuid references public.schools (id) on delete set null,
  blob       jsonb not null,
  updated_at timestamptz not null default now()
);

alter table public.progress enable row level security;

drop policy if exists progress_self_all on public.progress;
create policy progress_self_all on public.progress
  for all using (auth.uid() = person_id) with check (auth.uid() = person_id);
