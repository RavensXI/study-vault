-- ============================================================
-- Account sync — per-key store of a student's device state
--
-- One row per (user, localStorage key). js/account-sync.js merges this
-- with the device on sign-in and writes through on every change, so
-- progress (KC scores, practice logs, streaks, picks, prefs) belongs to
-- the ACCOUNT, not the browser. Before this, only lesson_visits synced:
-- a cleared browser or new phone silently lost everything (found 19 Aug).
--
-- value is always {"raw": "<verbatim localStorage string>"} — the client
-- re-serialises nothing, so what comes back is byte-identical to what
-- the page wrote. updated_at powers newer-wins merging for scalars.
--
-- Applied 2026-08-19 via SUPABASE_DB_URL (scripts/_apply_user_state.py).
-- ============================================================

create table if not exists user_state (
  user_id    uuid not null references auth.users(id) on delete cascade,
  key        text not null check (char_length(key) <= 64),
  value      jsonb not null,
  updated_at timestamptz not null default now(),
  primary key (user_id, key)
);

alter table user_state enable row level security;

drop policy if exists user_state_own on user_state;
create policy user_state_own on user_state
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

grant select, insert, update, delete on user_state to authenticated;
