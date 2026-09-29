-- Rollback of 20260929200000_admin_mfa.sql: platform_admin powers without the two-factor step
-- (the definitions as they were live on 29 Sep 2026).
BEGIN;

CREATE OR REPLACE FUNCTION public.is_platform_admin()
RETURNS boolean STABLE
LANGUAGE sql
SECURITY DEFINER
SET search_path = ''
AS $$
  SELECT EXISTS (
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
      AND role IN ('school_admin', 'platform_admin')
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
  SELECT role, school_id INTO v_role, v_school_id
  FROM public.profiles WHERE id = v_user_id;
  IF v_role NOT IN ('school_admin', 'platform_admin') THEN
    RETURN jsonb_build_object('error', 'Only school admins can invite teachers');
  END IF;
  IF v_school_id IS NULL AND v_role != 'platform_admin' THEN
    RETURN jsonb_build_object('error', 'No school associated with your account');
  END IF;
  INSERT INTO public.teacher_invitations (school_id, email, invited_by, subject_ids)
  VALUES (v_school_id, lower(trim(p_email)), v_user_id, p_subject_ids)
  RETURNING id, token INTO v_invitation_id, v_token;
  RETURN jsonb_build_object('success', true, 'invitation_id', v_invitation_id, 'token', v_token);
EXCEPTION
  WHEN unique_violation THEN
    RETURN jsonb_build_object('error', 'An invitation already exists for this email at this school');
END;
$function$;

DROP POLICY IF EXISTS classes_teacher_own ON public.classes;
CREATE POLICY classes_teacher_own ON public.classes FOR SELECT TO authenticated USING (
  (teacher_id = auth.uid()) OR (EXISTS ( SELECT 1 FROM public.profiles p
    WHERE ((p.id = auth.uid()) AND (p.role = ANY (ARRAY['school_admin'::public.user_role, 'platform_admin'::public.user_role]))
      AND ((p.role = 'platform_admin'::public.user_role) OR (p.school_id = classes.school_id)))))
);

DROP POLICY IF EXISTS class_members_own ON public.class_members;
CREATE POLICY class_members_own ON public.class_members FOR SELECT TO authenticated USING (
  (student_id = auth.uid()) OR (EXISTS ( SELECT 1 FROM public.classes c
    WHERE ((c.id = class_members.class_id) AND ((c.teacher_id = auth.uid()) OR (EXISTS ( SELECT 1 FROM public.profiles p
      WHERE ((p.id = auth.uid()) AND (p.role = ANY (ARRAY['school_admin'::public.user_role, 'platform_admin'::public.user_role]))
        AND ((p.role = 'platform_admin'::public.user_role) OR (p.school_id = c.school_id))))))))))
);

DROP FUNCTION IF EXISTS public.session_is_aal2();

COMMIT;
