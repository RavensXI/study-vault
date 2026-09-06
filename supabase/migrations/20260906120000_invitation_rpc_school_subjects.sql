-- 6 Sep 2026: the teacher sign-up page now lets a teacher pick the subjects
-- they teach. To list the right subjects it needs the invitation's school id
-- (for that school's bespoke subjects) and the subject ids the admin already
-- assigned (pre-ticked, not un-tickable). Neither is secret: the school name
-- was already returned, and a subject id identifies public content. The
-- token itself is still never returned.
CREATE OR REPLACE FUNCTION public.get_invitation_by_token(p_token text)
RETURNS TABLE (email text, accepted_at timestamptz, expires_at timestamptz,
               school_name text, school_id uuid, subject_ids uuid[])
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT ti.email, ti.accepted_at, ti.expires_at, s.name AS school_name,
         ti.school_id, ti.subject_ids
  FROM teacher_invitations ti
  LEFT JOIN schools s ON s.id = ti.school_id
  WHERE ti.token = p_token;
$$;

REVOKE ALL ON FUNCTION public.get_invitation_by_token(text) FROM public;
GRANT EXECUTE ON FUNCTION public.get_invitation_by_token(text) TO anon, authenticated;
