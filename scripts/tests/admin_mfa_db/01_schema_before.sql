-- The objects the admin-MFA migration changes or depends on, as they are LIVE today (definitions
-- read from pg_get_functiondef / pg_policies on 29 Sep 2026 and supabase/migrations/), plus the
-- tables they read. Written by hand; nothing dumped from production.
CREATE TYPE public.user_role AS ENUM ('platform_admin', 'school_admin', 'teacher', 'student');

CREATE TABLE public.schools (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text);
CREATE TABLE public.profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  school_id uuid REFERENCES public.schools(id),
  role public.user_role NOT NULL DEFAULT 'student',
  full_name text
);
CREATE TABLE public.subjects (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), school_id uuid REFERENCES public.schools(id), name text);
CREATE TABLE public.units (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), subject_id uuid REFERENCES public.subjects(id));
CREATE TABLE public.lessons (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), unit_id uuid REFERENCES public.units(id), status text NOT NULL DEFAULT 'live');
CREATE TABLE public.classes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  school_id uuid NOT NULL REFERENCES public.schools(id) ON DELETE CASCADE,
  teacher_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  name text NOT NULL, subject_id uuid REFERENCES public.subjects(id)
);
CREATE TABLE public.class_members (
  class_id uuid NOT NULL REFERENCES public.classes(id) ON DELETE CASCADE,
  student_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  PRIMARY KEY (class_id, student_id)
);
CREATE TABLE public.teacher_subjects (
  teacher_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  subject_id uuid NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
  PRIMARY KEY (teacher_id, subject_id)
);
CREATE TABLE public.teacher_invitations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  school_id uuid REFERENCES public.schools(id) ON DELETE CASCADE,
  email text NOT NULL,
  invited_by uuid REFERENCES public.profiles(id),
  subject_ids uuid[] DEFAULT '{}',
  token text NOT NULL UNIQUE DEFAULT encode(extensions.gen_random_bytes(32), 'hex'),
  UNIQUE (school_id, email)
);

-- live definitions (29 Sep 2026)
CREATE OR REPLACE FUNCTION public.is_platform_admin()
 RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO ''
AS $$ SELECT EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'platform_admin'); $$;

CREATE OR REPLACE FUNCTION public.is_teacher_or_above()
 RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO ''
AS $$ SELECT EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('teacher', 'school_admin', 'platform_admin')); $$;

CREATE OR REPLACE FUNCTION public.teacher_manages_subject(p_subject_id uuid)
 RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO ''
AS $$
  SELECT EXISTS (SELECT 1 FROM public.teacher_subjects WHERE teacher_id = auth.uid() AND subject_id = p_subject_id)
  OR EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('school_admin', 'platform_admin'));
$$;

CREATE OR REPLACE FUNCTION public.user_school_ids()
 RETURNS SETOF uuid LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO ''
AS $$
  SELECT school_id FROM public.profiles WHERE id = auth.uid() AND school_id IS NOT NULL
  UNION SELECT c.school_id FROM public.class_members m JOIN public.classes c ON c.id = m.class_id WHERE m.student_id = auth.uid();
$$;

CREATE OR REPLACE FUNCTION public.create_teacher_invitation(p_email text, p_subject_ids uuid[] DEFAULT '{}'::uuid[])
 RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path TO ''
AS $function$
DECLARE v_user_id uuid; v_school_id uuid; v_role public.user_role; v_invitation_id uuid; v_token text;
BEGIN
  v_user_id := auth.uid();
  SELECT role, school_id INTO v_role, v_school_id FROM public.profiles WHERE id = v_user_id;
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
EXCEPTION WHEN unique_violation THEN
  RETURN jsonb_build_object('error', 'An invitation already exists for this email at this school');
END;
$function$;

-- RLS as live: the "Platform admin full access" family, the two class rules, and the content
-- rules (school content private; unpublished lessons staff-only)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.schools ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.units ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lessons ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.class_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.teacher_subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.teacher_invitations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Platform admin full access on profiles" ON public.profiles FOR ALL USING (public.is_platform_admin()) WITH CHECK (public.is_platform_admin());
CREATE POLICY own_profile ON public.profiles FOR SELECT USING (id = auth.uid());
CREATE POLICY "Platform admin full access on schools" ON public.schools FOR ALL USING (public.is_platform_admin()) WITH CHECK (public.is_platform_admin());
CREATE POLICY "Platform admin full access on subjects" ON public.subjects FOR ALL USING (public.is_platform_admin()) WITH CHECK (public.is_platform_admin());
CREATE POLICY content_subjects ON public.subjects FOR SELECT USING (school_id IS NULL OR school_id IN (SELECT public.user_school_ids()));
CREATE POLICY "Platform admin full access on units" ON public.units FOR ALL USING (public.is_platform_admin()) WITH CHECK (public.is_platform_admin());
CREATE POLICY content_units ON public.units FOR SELECT USING (EXISTS (SELECT 1 FROM public.subjects s WHERE s.id = units.subject_id));
CREATE POLICY "Platform admin full access on lessons" ON public.lessons FOR ALL USING (public.is_platform_admin()) WITH CHECK (public.is_platform_admin());
CREATE POLICY content_lessons ON public.lessons FOR SELECT USING (
  (status = 'live' OR public.is_teacher_or_above()) AND EXISTS (SELECT 1 FROM public.units u WHERE u.id = lessons.unit_id));
CREATE POLICY "Platform admin full access on classes" ON public.classes FOR ALL USING (public.is_platform_admin()) WITH CHECK (public.is_platform_admin());
CREATE POLICY "Platform admin full access on class_members" ON public.class_members FOR ALL USING (public.is_platform_admin()) WITH CHECK (public.is_platform_admin());
CREATE POLICY "Platform admin full access on teacher_subjects" ON public.teacher_subjects FOR ALL USING (public.is_platform_admin()) WITH CHECK (public.is_platform_admin());
CREATE POLICY "Platform admin full access on teacher_invitations" ON public.teacher_invitations FOR ALL USING (public.is_platform_admin()) WITH CHECK (public.is_platform_admin());

-- the two class rules exactly as live
CREATE POLICY classes_teacher_own ON public.classes FOR SELECT TO authenticated USING (
  (teacher_id = auth.uid()) OR (EXISTS ( SELECT 1 FROM public.profiles p
    WHERE ((p.id = auth.uid()) AND (p.role = ANY (ARRAY['school_admin'::public.user_role, 'platform_admin'::public.user_role]))
      AND ((p.role = 'platform_admin'::public.user_role) OR (p.school_id = classes.school_id)))))
);
CREATE POLICY class_members_own ON public.class_members FOR SELECT TO authenticated USING (
  (student_id = auth.uid()) OR (EXISTS ( SELECT 1 FROM public.classes c
    WHERE ((c.id = class_members.class_id) AND ((c.teacher_id = auth.uid()) OR (EXISTS ( SELECT 1 FROM public.profiles p
      WHERE ((p.id = auth.uid()) AND (p.role = ANY (ARRAY['school_admin'::public.user_role, 'platform_admin'::public.user_role]))
        AND ((p.role = 'platform_admin'::public.user_role) OR (p.school_id = c.school_id)))))))))
);

GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO authenticated, service_role;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated, service_role;
