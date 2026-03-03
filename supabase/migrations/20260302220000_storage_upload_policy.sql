-- Allow all operations on pipeline-uploads bucket (replaces restrictive policies).
-- The bucket is used for both PPT uploads and hero image uploads from the admin UI.
-- Demo users have no auth.uid() so policies must be permissive.

DROP POLICY IF EXISTS "Allow pipeline uploads" ON storage.objects;
DROP POLICY IF EXISTS "Allow pipeline reads" ON storage.objects;
DROP POLICY IF EXISTS "Allow pipeline deletes" ON storage.objects;

-- Permissive: anyone can upload, read, update, and delete in this bucket
CREATE POLICY "pipeline-uploads full access"
  ON storage.objects FOR ALL
  USING (bucket_id = 'pipeline-uploads')
  WITH CHECK (bucket_id = 'pipeline-uploads');
