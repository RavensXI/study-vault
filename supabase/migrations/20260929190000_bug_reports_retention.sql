-- Bug reports: retention (Tom, 29 Sep 2026). Closing a report (fixed / wontfix) deletes its
-- screenshot at once and sets delete_after to 30 days later; the daily housekeeping in
-- api/cron/weekly-digest.js then deletes the row. Open reports are never deleted.
alter table public.bug_reports add column if not exists delete_after timestamptz;
create index if not exists bug_reports_delete_after_idx on public.bug_reports (delete_after) where delete_after is not null;
