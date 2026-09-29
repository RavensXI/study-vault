-- Admin powers need the two-factor step (Tom, 29 Sep 2026).
--
-- The shared admin password is retired: admin is Tom's own account plus a code from Microsoft
-- Authenticator. A session that has passed that step carries aal = 'aal2' in its token. Every
-- rule that gave platform_admin extra reach now also asks for aal2, so a stolen password alone
-- reaches no more than a teacher's own school. Teachers and pupils are unaffected.
--
-- Apply together with the admin-mfa code (api/_lib/admin-auth.js). Rollback:
-- 20260929200000_admin_mfa.rollback.sql.

BEGIN;
-- Give up rather than queue: if a lock is not free within 3 s (a long query is reading classes
-- or class_members), abort, and run it again later. Queuing behind a reader would block every
-- later query on those tables until the reader finished, which is how a lock stalls a live
-- database. The statements themselves take milliseconds. Run it on its own: nothing else in
-- the transaction, never a test query inside it.
SET LOCAL lock_timeout = '3s';
SET LOCAL statement_timeout = '15s';

CREATE OR REPLACE FUNCTION public.session_is_aal2()
RETURNS boolean STABLE
LANGUAGE sql
SET search_path = ''
AS $$
  SELECT coalesce(auth.jwt() ->> 'aal', '') = 'aal2';
$$;

CREATE OR REPLACE FUNCTION public.is_platform_admin()
RETURNS boolean STABLE
LANGUAGE sql
SECURITY DEFINER
SET search_path = ''
AS $$
  SELECT public.session_is_aal2() AND EXISTS (
    SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'platform_admin'
  );
$$;

CREATE OR REPLACE FUNCTION public.teacher_manages_subject(p_subject_id uuid)
RETURNS boolean STABLE
LANGUAGE sql
SECURITY DEFINER
SET search_path = ''
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.teacher_subjects
    WHERE teacher_id = auth.uid()
      AND subject_id = p_subject_id
  )
  OR EXISTS (
    SELECT 1 FROM public.profiles
    WHERE id = auth.uid()
      AND (role = 'school_admin' OR (role = 'platform_admin' AND public.session_is_aal2()))
  );
$$;

CREATE OR REPLACE FUNCTION public.create_teacher_invitation(p_email text, p_subject_ids uuid[] DEFAULT '{}'::uuid[])
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $function$
DECLARE
  v_user_id uuid;
  v_school_id uuid;
  v_role public.user_role;
  v_invitation_id uuid;
  v_token text;
BEGIN
  v_user_id := auth.uid();

  -- Check permissions
  SELECT role, school_id INTO v_role, v_school_id
  FROM public.profiles WHERE id = v_user_id;

  IF v_role NOT IN ('school_admin', 'platform_admin') THEN
    RETURN jsonb_build_object('error', 'Only school admins can invite teachers');
  END IF;

  IF v_role = 'platform_admin' AND NOT public.session_is_aal2() THEN
    RETURN jsonb_build_object('error', 'Sign in with your two-factor code first');
  END IF;

  IF v_school_id IS NULL AND v_role != 'platform_admin' THEN
    RETURN jsonb_build_object('error', 'No school associated with your account');
  END IF;

  -- Create the invitation
  INSERT INTO public.teacher_invitations (school_id, email, invited_by, subject_ids)
  VALUES (v_school_id, lower(trim(p_email)), v_user_id, p_subject_ids)
  RETURNING id, token INTO v_invitation_id, v_token;

  RETURN jsonb_build_object(
    'success', true,
    'invitation_id', v_invitation_id,
    'token', v_token
  );

EXCEPTION
  WHEN unique_violation THEN
    RETURN jsonb_build_object('error', 'An invitation already exists for this email at this school');
END;
$function$;

-- The two class rules named platform_admin directly: every school's classes and members.
DROP POLICY IF EXISTS classes_teacher_own ON public.classes;
CREATE POLICY classes_teacher_own ON public.classes FOR SELECT TO authenticated USING (
  (teacher_id = auth.uid()) OR (EXISTS (
    SELECT 1 FROM public.profiles p
    WHERE p.id = auth.uid()
      AND ((p.role = 'school_admin' AND p.school_id = classes.school_id)
        OR (p.role = 'platform_admin' AND (public.session_is_aal2() OR p.school_id = classes.school_id)))
  ))
);

DROP POLICY IF EXISTS class_members_own ON public.class_members;
CREATE POLICY class_members_own ON public.class_members FOR SELECT TO authenticated USING (
  (student_id = auth.uid()) OR (EXISTS (
    SELECT 1 FROM public.classes c
    WHERE c.id = class_members.class_id
      AND ((c.teacher_id = auth.uid()) OR (EXISTS (
        SELECT 1 FROM public.profiles p
        WHERE p.id = auth.uid()
          AND ((p.role = 'school_admin' AND p.school_id = c.school_id)
            OR (p.role = 'platform_admin' AND (public.session_is_aal2() OR p.school_id = c.school_id)))
      )))
  ))
);

COMMIT;
