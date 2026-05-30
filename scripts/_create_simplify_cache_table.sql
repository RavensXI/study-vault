-- ============================================================
-- Simplify Language — persistent cache of on-demand simplifications
--
-- One row per (original paragraph text, target level). The first viewer of a
-- paragraph generates it (Haiku, ~1s); everyone after reads the cache for free.
-- An async Sonnet QA pass blesses or rejects each row off the student's
-- critical path. Failed rows surface in /admin/simplify-review; the original
-- (already fact-checked) paragraph is served until an admin resolves them.
--
-- This table is NEVER read by the anon browser client — only by the API
-- routes (service key) and the admin review page (service key via API).
-- Keep it locked down so already-simplified content can't be scraped.
--
-- Run in the Supabase SQL editor.
-- ============================================================

create table if not exists simplify_cache (
  id              uuid primary key default gen_random_uuid(),
  original_hash   text not null,                       -- sha256(normalised original text)
  target_level    text not null default 'simple',      -- 'simple' for v1; keyed for future levels
  lesson_id       uuid references lessons(id) on delete cascade,
  paragraph_index text,                                -- data-narration-id (admin context only)
  subject_slug    text,
  original_text   text not null,
  simplified_text text not null,
  qa_status       text not null default 'pending',     -- pending | pass | fail | pending_review
  qa_notes        text,
  qa_model        text,
  gen_model       text,
  regen_count     int  not null default 0,
  created_at      timestamptz default now(),
  updated_at      timestamptz default now(),
  unique (original_hash, target_level)
);

create index if not exists simplify_cache_qa_status_idx on simplify_cache (qa_status);
create index if not exists simplify_cache_lesson_idx     on simplify_cache (lesson_id);

-- Keep updated_at fresh on any change.
create or replace function simplify_cache_touch_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists simplify_cache_touch_trg on simplify_cache;
create trigger simplify_cache_touch_trg
  before update on simplify_cache
  for each row execute function simplify_cache_touch_updated_at();

-- Lock down: only the service role (API routes) may touch this table.
alter table simplify_cache enable row level security;
-- No policies for anon/authenticated => browser clients get zero rows.
-- The service key bypasses RLS, so the API routes still have full access.
