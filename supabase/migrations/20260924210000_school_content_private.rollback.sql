-- Rollback for 20260924210000_school_content_private.sql: restores the 17 policies exactly
-- as saved in scripts/_backup_content_rls_2026-09-24.json (24 Sep 2026).
BEGIN;
DROP POLICY IF EXISTS "Anyone can read live free-tier subjects" ON public.subjects;
DROP POLICY IF EXISTS "School users can read their school's subjects" ON public.subjects;
DROP POLICY IF EXISTS "Anyone can read units of live free-tier subjects" ON public.units;
DROP POLICY IF EXISTS "School users can read their school's units" ON public.units;
DROP POLICY IF EXISTS "Anyone can read live free-tier lessons" ON public.lessons;
DROP POLICY IF EXISTS "School users can read their school's live lessons" ON public.lessons;
DROP POLICY IF EXISTS "Anyone can read guide pages of live free-tier subjects" ON public.guide_pages;
DROP POLICY IF EXISTS "School users can read their school's guide pages" ON public.guide_pages;
DROP POLICY IF EXISTS "School users can read their school's lesson overrides" ON public.lesson_overrides;
DROP POLICY IF EXISTS "Anyone can read guide pages of live subjects" ON public.guide_pages;
CREATE POLICY "Anyone can read guide pages of live subjects" ON public.guide_pages AS PERMISSIVE FOR SELECT TO public USING ((subject_id IN ( SELECT subjects.id
   FROM subjects
  WHERE (subjects.status = 'live'::content_status))));
DROP POLICY IF EXISTS "Platform admin full access on guide_pages" ON public.guide_pages;
CREATE POLICY "Platform admin full access on guide_pages" ON public.guide_pages AS PERMISSIVE FOR ALL TO public USING (is_platform_admin()) WITH CHECK (is_platform_admin());
DROP POLICY IF EXISTS "School users can read their guide pages" ON public.guide_pages;
CREATE POLICY "School users can read their guide pages" ON public.guide_pages AS PERMISSIVE FOR SELECT TO public USING ((subject_id IN ( SELECT subjects.id
   FROM subjects
  WHERE (subjects.school_id = current_user_school_id()))));
DROP POLICY IF EXISTS "Teachers can update guide pages for their subjects" ON public.guide_pages;
CREATE POLICY "Teachers can update guide pages for their subjects" ON public.guide_pages AS PERMISSIVE FOR UPDATE TO public USING (((current_user_role() = ANY (ARRAY['teacher'::user_role, 'school_admin'::user_role])) AND (subject_id IN ( SELECT s.id
   FROM subjects s
  WHERE ((s.school_id = current_user_school_id()) AND ((current_user_role() = 'school_admin'::user_role) OR (s.id IN ( SELECT teacher_subjects.subject_id
           FROM teacher_subjects
          WHERE ((teacher_subjects.teacher_id = auth.uid()) AND (teacher_subjects.can_edit = true)))))))))) WITH CHECK (((current_user_role() = ANY (ARRAY['teacher'::user_role, 'school_admin'::user_role])) AND (subject_id IN ( SELECT s.id
   FROM subjects s
  WHERE ((s.school_id = current_user_school_id()) AND ((current_user_role() = 'school_admin'::user_role) OR (s.id IN ( SELECT teacher_subjects.subject_id
           FROM teacher_subjects
          WHERE ((teacher_subjects.teacher_id = auth.uid()) AND (teacher_subjects.can_edit = true))))))))));
DROP POLICY IF EXISTS "lesson_overrides_read" ON public.lesson_overrides;
CREATE POLICY "lesson_overrides_read" ON public.lesson_overrides AS PERMISSIVE FOR SELECT TO public USING (true);
DROP POLICY IF EXISTS "Anyone can read live lessons" ON public.lessons;
CREATE POLICY "Anyone can read live lessons" ON public.lessons AS PERMISSIVE FOR SELECT TO public USING ((status = 'live'::content_status));
DROP POLICY IF EXISTS "Platform admin full access on lessons" ON public.lessons;
CREATE POLICY "Platform admin full access on lessons" ON public.lessons AS PERMISSIVE FOR ALL TO public USING (is_platform_admin()) WITH CHECK (is_platform_admin());
DROP POLICY IF EXISTS "Public read access on lessons" ON public.lessons;
CREATE POLICY "Public read access on lessons" ON public.lessons AS PERMISSIVE FOR SELECT TO public USING (true);
DROP POLICY IF EXISTS "Students can read live lessons from their school" ON public.lessons;
CREATE POLICY "Students can read live lessons from their school" ON public.lessons AS PERMISSIVE FOR SELECT TO public USING (((status = 'live'::content_status) AND (unit_id IN ( SELECT u.id
   FROM (units u
     JOIN subjects s ON ((u.subject_id = s.id)))
  WHERE (s.school_id = current_user_school_id())))));
DROP POLICY IF EXISTS "Teachers can read all lessons from their school" ON public.lessons;
CREATE POLICY "Teachers can read all lessons from their school" ON public.lessons AS PERMISSIVE FOR SELECT TO public USING (((current_user_role() = ANY (ARRAY['teacher'::user_role, 'school_admin'::user_role])) AND (unit_id IN ( SELECT u.id
   FROM (units u
     JOIN subjects s ON ((u.subject_id = s.id)))
  WHERE (s.school_id = current_user_school_id())))));
DROP POLICY IF EXISTS "Teachers can update lessons for their subjects" ON public.lessons;
CREATE POLICY "Teachers can update lessons for their subjects" ON public.lessons AS PERMISSIVE FOR UPDATE TO public USING (((current_user_role() = ANY (ARRAY['teacher'::user_role, 'school_admin'::user_role])) AND (unit_id IN ( SELECT u.id
   FROM (units u
     JOIN subjects s ON ((u.subject_id = s.id)))
  WHERE ((s.school_id = current_user_school_id()) AND ((current_user_role() = 'school_admin'::user_role) OR (s.id IN ( SELECT teacher_subjects.subject_id
           FROM teacher_subjects
          WHERE ((teacher_subjects.teacher_id = auth.uid()) AND (teacher_subjects.can_edit = true)))))))))) WITH CHECK (((current_user_role() = ANY (ARRAY['teacher'::user_role, 'school_admin'::user_role])) AND (unit_id IN ( SELECT u.id
   FROM (units u
     JOIN subjects s ON ((u.subject_id = s.id)))
  WHERE ((s.school_id = current_user_school_id()) AND ((current_user_role() = 'school_admin'::user_role) OR (s.id IN ( SELECT teacher_subjects.subject_id
           FROM teacher_subjects
          WHERE ((teacher_subjects.teacher_id = auth.uid()) AND (teacher_subjects.can_edit = true))))))))));
DROP POLICY IF EXISTS "Anyone can read live subjects" ON public.subjects;
CREATE POLICY "Anyone can read live subjects" ON public.subjects AS PERMISSIVE FOR SELECT TO public USING ((status = 'live'::content_status));
DROP POLICY IF EXISTS "Platform admin full access on subjects" ON public.subjects;
CREATE POLICY "Platform admin full access on subjects" ON public.subjects AS PERMISSIVE FOR ALL TO public USING (is_platform_admin()) WITH CHECK (is_platform_admin());
DROP POLICY IF EXISTS "School users can read their subjects" ON public.subjects;
CREATE POLICY "School users can read their subjects" ON public.subjects AS PERMISSIVE FOR SELECT TO public USING ((school_id = current_user_school_id()));
DROP POLICY IF EXISTS "Anyone can read units of live subjects" ON public.units;
CREATE POLICY "Anyone can read units of live subjects" ON public.units AS PERMISSIVE FOR SELECT TO public USING ((subject_id IN ( SELECT subjects.id
   FROM subjects
  WHERE (subjects.status = 'live'::content_status))));
DROP POLICY IF EXISTS "Platform admin full access on units" ON public.units;
CREATE POLICY "Platform admin full access on units" ON public.units AS PERMISSIVE FOR ALL TO public USING (is_platform_admin()) WITH CHECK (is_platform_admin());
DROP POLICY IF EXISTS "School users can read their units" ON public.units;
CREATE POLICY "School users can read their units" ON public.units AS PERMISSIVE FOR SELECT TO public USING ((subject_id IN ( SELECT subjects.id
   FROM subjects
  WHERE (subjects.school_id = current_user_school_id()))));
DROP FUNCTION IF EXISTS public.get_invitation_subjects(text);
-- user_school_ids() is left in place: nothing else depends on it and it is harmless.
COMMIT;
