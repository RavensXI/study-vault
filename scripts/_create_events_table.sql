-- The evidence store: one row per piece of retrieval-practice evidence.
-- This is LAUNCH schema, not demo kit — the teacher dashboard reads only
-- this table; students keep localStorage + user_metadata as offline cache.
-- Applied 2026-07-28 (demo-school build). Additive: creates only.

create table if not exists public.events (
  id         bigint generated always as identity primary key,
  person_id  uuid not null references auth.users (id) on delete cascade,
  school_id  uuid references public.schools (id) on delete set null,
  subject    text not null,           -- subject slug (subjects.slug)
  unit       text,                    -- unit slug
  lesson     smallint,                -- lesson number within the unit
  kind       text not null check (kind in
               ('warmup','quiz','shorts','flash','practice','miscon','lesson_done')),
  ok         boolean,                 -- right/wrong where applicable
  q          text,                    -- the question (wrong answers carry it)
  chose      text,                    -- the chosen distractor (misses only)
  answer     text,                    -- the right answer (misses only)
  tag        text,                    -- named misconception / shorts topic
  box        smallint,                -- flashcard box after the move
  meta       jsonb,
  at         timestamptz not null default now()
);

create index if not exists events_person_at
  on public.events (person_id, at desc);
create index if not exists events_school_subject_at
  on public.events (school_id, subject, at desc);

alter table public.events enable row level security;

-- students: their own rows only
drop policy if exists events_self_insert on public.events;
create policy events_self_insert on public.events
  for insert with check (auth.uid() = person_id);
drop policy if exists events_self_select on public.events;
create policy events_self_select on public.events
  for select using (auth.uid() = person_id);

-- teachers: rows of students in classes they own
drop policy if exists events_teacher_select on public.events;
create policy events_teacher_select on public.events
  for select using (
    exists (
      select 1
      from public.class_members cm
      join public.classes c on c.id = cm.class_id
      where cm.student_id = events.person_id
        and c.teacher_id = auth.uid()
    )
  );
