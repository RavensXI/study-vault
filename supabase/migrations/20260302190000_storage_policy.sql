-- Allow uploads to the pipeline-uploads bucket.
-- This is permissive because demo users lack Supabase auth sessions.
-- Once SSO is active, tighten to require auth.role() = 'authenticated'.

CREATE POLICY "Allow pipeline uploads"
  ON storage.objects FOR INSERT
  WITH CHECK (bucket_id = 'pipeline-uploads');

CREATE POLICY "Allow pipeline reads"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'pipeline-uploads');

CREATE POLICY "Allow pipeline deletes"
  ON storage.objects FOR DELETE
  USING (bucket_id = 'pipeline-uploads');
