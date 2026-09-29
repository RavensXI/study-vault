# Admin two-factor migration: local database test (29 Sep 2026)

Tests `supabase/migrations/20260929200000_admin_mfa.sql` and its rollback in **PGlite**
(Postgres compiled to WASM, in memory, inside node). Nothing touches production.
Never test DDL on the live database, not even inside BEGIN…ROLLBACK: a dry run there held locks
on classes/class_members and took production down for 25 minutes on 29 Sep 2026.

    cd <a scratch folder> && npm install @electric-sql/pglite
    node <repo>/scripts/tests/admin_mfa_db/run_pglite.mjs <repo root>

(run it from the scratch folder so node finds PGlite there)

- `00_supabase_stub.sql` stands in for Supabase's auth schema: auth.uid(), auth.jwt() from
  request.jwt.claims, and the roles.
- `01_schema_before.sql` holds the live definitions of the objects the migration changes,
  written by hand from pg_get_functiondef / pg_policies (29 Sep 2026) and supabase/migrations/.
- `02_seed.sql` is two schools, Tom, two teachers, two pupils, free and school content.

The matrix checks Tom at aal1 and aal2, both teachers and a pupil: before, after, after the
rollback, and after a second apply.

PGlite is single-connection, so it cannot show the lock_timeout behaviour (the migration gives up
after 3 s instead of queuing behind a reader). That was shown once on a local postgres:15
container before Docker was ruled out: it gave up after 3.0 s and left nothing half-applied.
The API side is tested by `scripts/tests/admin_mfa_api_test.js` (no network).
