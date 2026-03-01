-- StudyVault Dynamic Architecture: Full Schema Migration
-- Run this in the Supabase SQL Editor (Dashboard → SQL → New Query)

-- ============================================================
-- CUSTOM TYPES
-- ============================================================

CREATE TYPE user_role AS ENUM ('platform_admin', 'school_admin', 'teacher', 'student');
CREATE TYPE content_status AS ENUM ('draft', 'review', 'approved', 'live', 'archived');

-- ============================================================
-- CORE TABLES
-- ============================================================

-- Schools: top-level tenant
CREATE TABLE schools (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name       text NOT NULL,
  slug       text NOT NULL UNIQUE,
  domain     text,
  logo_url   text,
  settings   jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Profiles: extends auth.users
CREATE TABLE profiles (
  id         uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  school_id  uuid REFERENCES schools(id),
  role       user_role NOT NULL DEFAULT 'student',
  full_name  text,
  email      text,
  exam_date  date,
  settings   jsonb DEFAULT '{}',
  is_demo    boolean NOT NULL DEFAULT false,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Subjects: one per GCSE subject per school
CREATE TABLE subjects (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  school_id  uuid NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
  slug       text NOT NULL,
  name       text NOT NULL,
  exam_board text NOT NULL,
  spec_code  text,
  color      text,
  image_url  text,
  detail     text,
  status     content_status NOT NULL DEFAULT 'draft',
  is_active  boolean DEFAULT false,
  sort_order smallint DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  UNIQUE(school_id, slug)
);

-- Units: unit/theme/paper within a subject
CREATE TABLE units (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id   uuid NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
  slug         text NOT NULL,
  name         text NOT NULL,
  subtitle     text,
  body_class   text NOT NULL,
  accent       text NOT NULL,
  accent_light text NOT NULL,
  accent_badge text NOT NULL,
  image_url    text,
  lesson_count smallint NOT NULL DEFAULT 0,
  sort_order   smallint DEFAULT 0,
  created_at   timestamptz DEFAULT now(),
  UNIQUE(subject_id, slug)
);

-- Lessons: the central content table
CREATE TABLE lessons (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  unit_id             uuid NOT NULL REFERENCES units(id) ON DELETE CASCADE,
  lesson_number       smallint NOT NULL,
  slug                text NOT NULL,
  title               text NOT NULL,

  -- Content HTML
  content_html        text,
  exam_tip_html       text,
  conclusion_html     text,

  -- Hero image
  hero_image_url      text,
  hero_image_alt      text,
  hero_image_position text DEFAULT 'center 50%',
  hero_image_caption  text,

  -- JSONB data (maps to existing window.* globals)
  narration_manifest  jsonb DEFAULT '[]',
  practice_questions  jsonb DEFAULT '[]',
  knowledge_checks    jsonb DEFAULT '[]',
  glossary_terms      jsonb DEFAULT '[]',
  diagrams            jsonb DEFAULT '[]',
  related_media       jsonb DEFAULT '[]',

  -- YouTube
  youtube_video_id    text,

  -- Content pipeline
  status              content_status NOT NULL DEFAULT 'draft',
  status_changed_by   uuid REFERENCES profiles(id),
  approved_at         timestamptz,
  source_ppt_hash     text,

  created_at          timestamptz DEFAULT now(),
  updated_at          timestamptz DEFAULT now(),
  UNIQUE(unit_id, lesson_number)
);

-- ============================================================
-- USER PROGRESS TABLES
-- ============================================================

-- Replaces studyvault-subjects-{userId} localStorage
CREATE TABLE user_selected_subjects (
  user_id    uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  subject_id uuid NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, subject_id)
);

-- Replaces studyvault-visited localStorage
CREATE TABLE lesson_visits (
  user_id     uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  lesson_id   uuid NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  first_visit timestamptz DEFAULT now(),
  last_visit  timestamptz DEFAULT now(),
  visit_count integer DEFAULT 1,
  PRIMARY KEY (user_id, lesson_id)
);

-- Replaces studyvault-kc-{unit}/{lesson} localStorage
CREATE TABLE knowledge_check_scores (
  user_id      uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  lesson_id    uuid NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  best_score   smallint NOT NULL,
  total        smallint NOT NULL,
  attempts     integer DEFAULT 1,
  last_attempt timestamptz DEFAULT now(),
  PRIMARY KEY (user_id, lesson_id)
);

-- ============================================================
-- GUIDE PAGES & PIPELINE TRACKING
-- ============================================================

-- Exam technique + revision technique guide pages
CREATE TABLE guide_pages (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id   uuid NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
  guide_type   text NOT NULL CHECK (guide_type IN ('exam-technique', 'revision-technique')),
  slug         text NOT NULL,
  title        text NOT NULL,
  content_html text NOT NULL,
  sort_order   smallint DEFAULT 0,
  UNIQUE(subject_id, guide_type, slug)
);

-- Content pipeline audit log
CREATE TABLE content_pipeline_logs (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id   uuid REFERENCES lessons(id),
  from_status content_status,
  to_status   content_status NOT NULL,
  changed_by  uuid REFERENCES profiles(id),
  notes       text,
  created_at  timestamptz DEFAULT now()
);

-- PPT upload tracking (future use)
CREATE TABLE upload_jobs (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  school_id       uuid NOT NULL REFERENCES schools(id),
  uploaded_by     uuid NOT NULL REFERENCES profiles(id),
  filename        text NOT NULL,
  file_hash       text,
  status          text DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
  lessons_created integer DEFAULT 0,
  error_message   text,
  created_at      timestamptz DEFAULT now()
);

-- ============================================================
-- CLASSES (teacher analytics)
-- ============================================================

CREATE TABLE classes (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  school_id  uuid NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
  teacher_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  name       text NOT NULL,
  subject_id uuid REFERENCES subjects(id),
  year_group smallint
);

CREATE TABLE class_members (
  class_id   uuid NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  student_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  PRIMARY KEY (class_id, student_id)
);

-- ============================================================
-- HELPER FUNCTIONS
-- ============================================================

CREATE OR REPLACE FUNCTION current_user_school_id()
RETURNS uuid STABLE
LANGUAGE sql
SECURITY DEFINER
SET search_path = ''
AS $$
  SELECT school_id FROM public.profiles WHERE id = auth.uid();
$$;

CREATE OR REPLACE FUNCTION is_platform_admin()
RETURNS boolean STABLE
LANGUAGE sql
SECURITY DEFINER
SET search_path = ''
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'platform_admin'
  );
$$;

CREATE OR REPLACE FUNCTION current_user_role()
RETURNS user_role STABLE
LANGUAGE sql
SECURITY DEFINER
SET search_path = ''
AS $$
  SELECT role FROM public.profiles WHERE id = auth.uid();
$$;

-- ============================================================
-- TRIGGERS
-- ============================================================

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, email)
  VALUES (
    new.id,
    COALESCE(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name', ''),
    new.email
  );
  RETURN new;
END;
$$;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Auto-assign school by email domain
CREATE OR REPLACE FUNCTION auto_assign_school()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  domain_part text;
  school_uuid uuid;
BEGIN
  IF new.email IS NOT NULL THEN
    domain_part := split_part(new.email, '@', 2);
    SELECT id INTO school_uuid FROM public.schools WHERE domain = domain_part LIMIT 1;
    IF school_uuid IS NOT NULL THEN
      UPDATE public.profiles SET school_id = school_uuid WHERE id = new.id AND school_id IS NULL;
    END IF;
  END IF;
  RETURN new;
END;
$$;

CREATE TRIGGER on_profile_assign_school
  AFTER INSERT ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION auto_assign_school();

-- Auto-update updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  new.updated_at = now();
  RETURN new;
END;
$$;

CREATE TRIGGER update_schools_updated_at
  BEFORE UPDATE ON schools
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_lessons_updated_at
  BEFORE UPDATE ON lessons
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- RPC: increment visit count (called from lesson-loader.js)
CREATE OR REPLACE FUNCTION increment_visit_count(p_user_id uuid, p_lesson_id uuid)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  UPDATE public.lesson_visits
  SET visit_count = visit_count + 1,
      last_visit = now()
  WHERE user_id = p_user_id AND lesson_id = p_lesson_id;
END;
$$;

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_subjects_school ON subjects (school_id);
CREATE INDEX idx_units_subject ON units (subject_id);
CREATE INDEX idx_lessons_unit_order ON lessons (unit_id, lesson_number);
CREATE INDEX idx_lessons_status ON lessons (status);
CREATE INDEX idx_lesson_visits_user ON lesson_visits (user_id);
CREATE INDEX idx_kc_scores_user ON knowledge_check_scores (user_id);
CREATE INDEX idx_profiles_school ON profiles (school_id);
CREATE INDEX idx_schools_domain ON schools (domain);

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE schools ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE units ENABLE ROW LEVEL SECURITY;
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_selected_subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE lesson_visits ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_check_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE guide_pages ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_pipeline_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE upload_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE class_members ENABLE ROW LEVEL SECURITY;

-- ---- schools ----

CREATE POLICY "Platform admin full access on schools"
  ON schools FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

CREATE POLICY "Users can read their own school"
  ON schools FOR SELECT
  USING (id = current_user_school_id());

-- ---- profiles ----

CREATE POLICY "Platform admin full access on profiles"
  ON profiles FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

CREATE POLICY "Users can read own profile"
  ON profiles FOR SELECT
  USING (id = auth.uid());

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (id = auth.uid())
  WITH CHECK (id = auth.uid());

CREATE POLICY "Teachers can read school profiles"
  ON profiles FOR SELECT
  USING (
    school_id = current_user_school_id()
    AND current_user_role() IN ('teacher', 'school_admin')
  );

-- ---- subjects ----

CREATE POLICY "Platform admin full access on subjects"
  ON subjects FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

CREATE POLICY "School users can read their subjects"
  ON subjects FOR SELECT
  USING (school_id = current_user_school_id());

-- ---- units ----

CREATE POLICY "Platform admin full access on units"
  ON units FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

CREATE POLICY "School users can read their units"
  ON units FOR SELECT
  USING (
    subject_id IN (SELECT id FROM subjects WHERE school_id = current_user_school_id())
  );

-- ---- lessons ----

CREATE POLICY "Platform admin full access on lessons"
  ON lessons FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

CREATE POLICY "Students can read live lessons from their school"
  ON lessons FOR SELECT
  USING (
    status = 'live'
    AND unit_id IN (
      SELECT u.id FROM units u
      JOIN subjects s ON u.subject_id = s.id
      WHERE s.school_id = current_user_school_id()
    )
  );

CREATE POLICY "Teachers can read all lessons from their school"
  ON lessons FOR SELECT
  USING (
    current_user_role() IN ('teacher', 'school_admin')
    AND unit_id IN (
      SELECT u.id FROM units u
      JOIN subjects s ON u.subject_id = s.id
      WHERE s.school_id = current_user_school_id()
    )
  );

-- ---- user_selected_subjects ----

CREATE POLICY "Users manage own subject selections"
  ON user_selected_subjects FOR ALL
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Platform admin full access on user_selected_subjects"
  ON user_selected_subjects FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

-- ---- lesson_visits ----

CREATE POLICY "Users manage own visits"
  ON lesson_visits FOR ALL
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Teachers can read school student visits"
  ON lesson_visits FOR SELECT
  USING (
    current_user_role() IN ('teacher', 'school_admin')
    AND user_id IN (
      SELECT id FROM profiles WHERE school_id = current_user_school_id()
    )
  );

CREATE POLICY "Platform admin full access on lesson_visits"
  ON lesson_visits FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

-- ---- knowledge_check_scores ----

CREATE POLICY "Users manage own KC scores"
  ON knowledge_check_scores FOR ALL
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Teachers can read school student KC scores"
  ON knowledge_check_scores FOR SELECT
  USING (
    current_user_role() IN ('teacher', 'school_admin')
    AND user_id IN (
      SELECT id FROM profiles WHERE school_id = current_user_school_id()
    )
  );

CREATE POLICY "Platform admin full access on knowledge_check_scores"
  ON knowledge_check_scores FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

-- ---- guide_pages ----

CREATE POLICY "Platform admin full access on guide_pages"
  ON guide_pages FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

CREATE POLICY "School users can read their guide pages"
  ON guide_pages FOR SELECT
  USING (
    subject_id IN (SELECT id FROM subjects WHERE school_id = current_user_school_id())
  );

-- ---- content_pipeline_logs ----

CREATE POLICY "Platform admin full access on content_pipeline_logs"
  ON content_pipeline_logs FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

CREATE POLICY "Teachers can read their school pipeline logs"
  ON content_pipeline_logs FOR SELECT
  USING (
    current_user_role() IN ('teacher', 'school_admin')
    AND lesson_id IN (
      SELECT l.id FROM lessons l
      JOIN units u ON l.unit_id = u.id
      JOIN subjects s ON u.subject_id = s.id
      WHERE s.school_id = current_user_school_id()
    )
  );

-- ---- upload_jobs ----

CREATE POLICY "Platform admin full access on upload_jobs"
  ON upload_jobs FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

CREATE POLICY "School admins can manage their upload jobs"
  ON upload_jobs FOR ALL
  USING (
    school_id = current_user_school_id()
    AND current_user_role() IN ('teacher', 'school_admin')
  )
  WITH CHECK (
    school_id = current_user_school_id()
    AND current_user_role() IN ('teacher', 'school_admin')
  );

-- ---- classes ----

CREATE POLICY "Platform admin full access on classes"
  ON classes FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

CREATE POLICY "School staff can manage classes"
  ON classes FOR ALL
  USING (
    school_id = current_user_school_id()
    AND current_user_role() IN ('teacher', 'school_admin')
  )
  WITH CHECK (
    school_id = current_user_school_id()
    AND current_user_role() IN ('teacher', 'school_admin')
  );

CREATE POLICY "Students can read their classes"
  ON classes FOR SELECT
  USING (
    id IN (SELECT class_id FROM class_members WHERE student_id = auth.uid())
  );

-- ---- class_members ----

CREATE POLICY "Platform admin full access on class_members"
  ON class_members FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

CREATE POLICY "Teachers can manage class members"
  ON class_members FOR ALL
  USING (
    class_id IN (
      SELECT id FROM classes
      WHERE school_id = current_user_school_id()
      AND current_user_role() IN ('teacher', 'school_admin')
    )
  )
  WITH CHECK (
    class_id IN (
      SELECT id FROM classes
      WHERE school_id = current_user_school_id()
      AND current_user_role() IN ('teacher', 'school_admin')
    )
  );

CREATE POLICY "Students can read own class memberships"
  ON class_members FOR SELECT
  USING (student_id = auth.uid());
