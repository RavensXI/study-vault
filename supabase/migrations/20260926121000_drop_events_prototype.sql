-- 26 Sep 2026 (Tom approved): the old teacher-prototype table `events` is dropped.
-- It held 236,399 synthetic answer rows for the 300 Demo High School pupils (Apr-Jul 2026);
-- only teach.html (the retired /teach prototype, now a redirect to /teacher/classes) read it.
-- No foreign keys, views, functions or triggers depended on it.
-- Backup: scripts/_backup_events_table_2026-09-26.json.gz (every row, verified 236,399).
drop table if exists public.events;
