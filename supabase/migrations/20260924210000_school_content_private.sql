-- School content is private to its school (24 Sep 2026).
--
-- Before this, "Public read access on lessons" (USING true) let anyone holding the public key
-- read every lesson, including school-only lessons and unpublished drafts, and the "anyone can
-- read live ..." rules on subjects, units and guide pages did not check school_id. The site
-- only hid school content by not asking for it. Tom's rule: anonymous users must never be able
-- to see a school's content.
--
-- After this:
--   * anyone:        live free-tier content only (school_id IS NULL, subject live, lesson live)
--   * school users:  their school's content, where "their school" is the school on their
--                    profile OR the school of any class they belong to (joining a class does
--                    not set profiles.school_id, so membership must count)
--   * teachers:      unchanged (their school's lessons at any status)
--   * platform admin: unchanged (full access); the password-gated admin pages read through
--                    /api/staff/rest, which uses the service key
--
-- Rollback: supabase/migrations/20260924210000_school_content_private.rollback.sql
-- (restores the 17 policies saved in scripts/_backup_content_rls_2026-09-24.json).

BEGIN;

-- Which schools the signed-in user belongs to. Empty for anonymous visitors.
CREATE OR REPLACE FUNCTION public.user_school_ids()
RETURNS SETOF uuid
LANGUAGE sql
STABLE SECURITY DEFINER
SET search_path TO ''
AS $$
  SELECT p.school_id FROM public.profiles p
   WHERE p.id = auth.uid() AND p.school_id IS NOT NULL
  UNION
  SELECT c.school_id FROM public.class_members cm
    JOIN public.classes c ON c.id = cm.class_id
   WHERE cm.student_id = auth.uid() AND c.school_id IS NOT NULL
$$;
REVOKE ALL ON FUNCTION public.user_school_ids() FROM public;
GRANT EXECUTE ON FUNCTION public.user_school_ids() TO anon, authenticated;

-- subjects ---------------------------------------------------------------------------------
DROP POLICY IF EXISTS "Anyone can read live subjects" ON public.subjects;
DROP POLICY IF EXISTS "School users can read their subjects" ON public.subjects;
CREATE POLICY "Anyone can read live free-tier subjects" ON public.subjects
  FOR SELECT USING (status = 'live' AND school_id IS NULL);
CREATE POLICY "School users can read their school's subjects" ON public.subjects
  FOR SELECT USING (school_id IN (SELECT public.user_school_ids()));

-- units ------------------------------------------------------------------------------------
DROP POLICY IF EXISTS "Anyone can read units of live subjects" ON public.units;
DROP POLICY IF EXISTS "School users can read their units" ON public.units;
CREATE POLICY "Anyone can read units of live free-tier subjects" ON public.units
  FOR SELECT USING (subject_id IN (
    SELECT s.id FROM public.subjects s WHERE s.status = 'live' AND s.school_id IS NULL));
CREATE POLICY "School users can read their school's units" ON public.units
  FOR SELECT USING (subject_id IN (
    SELECT s.id FROM public.subjects s WHERE s.school_id IN (SELECT public.user_school_ids())));

-- lessons ----------------------------------------------------------------------------------
DROP POLICY IF EXISTS "Public read access on lessons" ON public.lessons;
DROP POLICY IF EXISTS "Anyone can read live lessons" ON public.lessons;
DROP POLICY IF EXISTS "Students can read live lessons from their school" ON public.lessons;
CREATE POLICY "Anyone can read live free-tier lessons" ON public.lessons
  FOR SELECT USING (status = 'live' AND unit_id IN (
    SELECT u.id FROM public.units u JOIN public.subjects s ON s.id = u.subject_id
     WHERE s.status = 'live' AND s.school_id IS NULL));
CREATE POLICY "School users can read their school's live lessons" ON public.lessons
  FOR SELECT USING (status = 'live' AND unit_id IN (
    SELECT u.id FROM public.units u JOIN public.subjects s ON s.id = u.subject_id
     WHERE s.school_id IN (SELECT public.user_school_ids())));
-- kept as they were: "Teachers can read all lessons from their school",
-- "Teachers can update lessons for their subjects", "Platform admin full access on lessons"

-- guide pages ------------------------------------------------------------------------------
DROP POLICY IF EXISTS "Anyone can read guide pages of live subjects" ON public.guide_pages;
DROP POLICY IF EXISTS "School users can read their guide pages" ON public.guide_pages;
CREATE POLICY "Anyone can read guide pages of live free-tier subjects" ON public.guide_pages
  FOR SELECT USING (subject_id IN (
    SELECT s.id FROM public.subjects s WHERE s.status = 'live' AND s.school_id IS NULL));
CREATE POLICY "School users can read their school's guide pages" ON public.guide_pages
  FOR SELECT USING (subject_id IN (
    SELECT s.id FROM public.subjects s WHERE s.school_id IN (SELECT public.user_school_ids())));

-- a school's own edits to free-tier lessons ------------------------------------------------
DROP POLICY IF EXISTS "lesson_overrides_read" ON public.lesson_overrides;
CREATE POLICY "School users can read their school's lesson overrides" ON public.lesson_overrides
  FOR SELECT USING (school_id IN (SELECT public.user_school_ids()) OR public.is_platform_admin());

-- Teacher sign-up lists the inviting school's subjects before the teacher has an account.
-- A valid, unused, unexpired invitation token is the only thing that unlocks them.
CREATE OR REPLACE FUNCTION public.get_invitation_subjects(p_token text)
RETURNS TABLE(id uuid, name text, slug text, school_id uuid, exam_board text)
LANGUAGE sql
STABLE SECURITY DEFINER
SET search_path TO 'public'
AS $$
  SELECT s.id, s.name::text, s.slug::text, s.school_id, s.exam_board::text
    FROM subjects s
   WHERE s.status = 'live'
     AND (s.school_id IS NULL
          OR s.school_id = (SELECT ti.school_id FROM teacher_invitations ti
                             WHERE ti.token = p_token AND ti.accepted_at IS NULL
                               AND ti.expires_at > now()))
   ORDER BY s.name
$$;
REVOKE ALL ON FUNCTION public.get_invitation_subjects(text) FROM public;
GRANT EXECUTE ON FUNCTION public.get_invitation_subjects(text) TO anon, authenticated;

COMMIT;
