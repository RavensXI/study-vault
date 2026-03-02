-- Make upload_jobs work with demo users (no profile/school records).
-- Revert to NOT NULL once SSO is active and demo accounts are removed.

ALTER TABLE upload_jobs ALTER COLUMN school_id DROP NOT NULL;
ALTER TABLE upload_jobs ALTER COLUMN uploaded_by DROP NOT NULL;
