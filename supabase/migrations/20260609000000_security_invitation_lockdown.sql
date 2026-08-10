-- ============================================================
-- Security hardening (9 Jun 2026): teacher_invitations was world-readable
-- ============================================================
--
-- The "Anyone can read invitation by token" policy was USING (true). The
-- inline comment claimed the application's `.eq('token', ...)` filter made it
-- safe, but RLS cannot see client filters: USING (true) made EVERY row —
-- token and teacher email included — readable by the anon role. A live token
-- could be harvested and used at /teacher/signup to claim a teacher account
-- (which carries lesson/guide edit rights for that school).
--
-- Replacement: drop the open SELECT policy entirely and provide a
-- SECURITY DEFINER lookup that takes the token as an argument and returns
-- only the non-secret fields the signup page needs, for an exact match only.
-- The token itself is never returned. The admin / school-admin / own-email
-- policies on the table are unchanged.

DROP POLICY IF EXISTS "Anyone can read invitation by token" ON teacher_invitations;

CREATE OR REPLACE FUNCTION public.get_invitation_by_token(p_token text)
RETURNS TABLE (email text, accepted_at timestamptz, expires_at timestamptz, school_name text)
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT ti.email, ti.accepted_at, ti.expires_at, s.name AS school_name
  FROM teacher_invitations ti
  LEFT JOIN schools s ON s.id = ti.school_id
  WHERE ti.token = p_token;
$$;

REVOKE ALL ON FUNCTION public.get_invitation_by_token(text) FROM public;
GRANT EXECUTE ON FUNCTION public.get_invitation_by_token(text) TO anon, authenticated;
