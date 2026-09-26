-- Anonymous answer pool (26 Sep 2026, approved by Tom).
--
-- One row per question + tidied answer (or, for AI-marked writing, per question + mark),
-- with a count. No person, account, school, class, device, IP or per-answer time: the
-- only date is the ISO week the row was first seen. Written by /api/pool with the
-- service key; nobody else can read or write it (RLS on, no policies).
--
-- kind 'answer': answer_norm + verdict (right | wrong | partly); marks_of/got are 0.
-- kind 'mark'  : marks_of + got (the mark the AI marker gave); answer_norm '' , verdict ''.

create table if not exists public.answer_pool (
  question_key text not null,
  kind         text not null check (kind in ('answer', 'mark')),
  answer_norm  text not null default '' check (char_length(answer_norm) <= 60),
  verdict      text not null default '' check (verdict in ('', 'right', 'wrong', 'partly')),
  marks_of     smallint not null default 0,
  got          smallint not null default 0,
  n            integer not null default 0,
  first_week   text not null,
  primary key (question_key, kind, answer_norm, verdict, marks_of, got)
);

alter table public.answer_pool enable row level security;
revoke all on public.answer_pool from anon, authenticated;

create or replace function public.pool_add(p_rows jsonb)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
  r jsonb;
  added integer := 0;
  wk text := to_char(now() at time zone 'Europe/London', 'IYYY-"W"IW');
begin
  if jsonb_typeof(p_rows) <> 'array' or jsonb_array_length(p_rows) > 50 then
    return 0;
  end if;
  for r in select * from jsonb_array_elements(p_rows) loop
    insert into public.answer_pool (question_key, kind, answer_norm, verdict, marks_of, got, n, first_week)
    values (left(r->>'question_key', 160), r->>'kind', coalesce(r->>'answer_norm', ''), coalesce(r->>'verdict', ''),
            coalesce((r->>'marks_of')::smallint, 0), coalesce((r->>'got')::smallint, 0), 1, wk)
    on conflict (question_key, kind, answer_norm, verdict, marks_of, got)
    do update set n = public.answer_pool.n + 1;
    added := added + 1;
  end loop;
  return added;
end;
$$;

revoke all on function public.pool_add(jsonb) from public, anon, authenticated;
grant execute on function public.pool_add(jsonb) to service_role;
