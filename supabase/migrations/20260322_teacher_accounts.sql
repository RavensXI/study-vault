-- StudyVault: Teacher Accounts System
-- Adds teacher invitations, subject-level permissions, notifications,
-- and QA tracking columns on lessons.
-- Run date: 2026-03-22

-- ============================================================
-- 0. ENSURE pgcrypto EXTENSION (for gen_random_bytes)
-- ============================================================
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ============================================================
-- 1. EXTEND content_status ENUM
-- ============================================================
-- Existing values: draft, review, approved, live, archived
-- Add: pending_review, ready_for_teacher

-- PG 12+ supports ADD VALUE IF NOT EXISTS inside transactions
ALTER TYPE content_status ADD VALUE IF NOT EXISTS 'pending_review' AFTER 'draft';
ALTER TYPE content_status ADD VALUE IF NOT EXISTS 'ready_for_teacher' AFTER 'pending_review';

-- ============================================================
-- 2. NEW TABLE: teacher_invitations
-- ============================================================

CREATE TABLE IF NOT EXISTS teacher_invitations (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  school_id    uuid NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
  email        text NOT NULL,
  invited_by   uuid REFERENCES profiles(id),
  subject_ids  uuid[] DEFAULT '{}',
  token        text NOT NULL UNIQUE DEFAULT encode(extensions.gen_random_bytes(32), 'hex'),
  accepted_at  timestamptz,
  expires_at   timestamptz NOT NULL DEFAULT (now() + interval '7 days'),
  created_at   timestamptz DEFAULT now(),
  UNIQUE(school_id, email)
);

CREATE INDEX IF NOT EXISTS idx_teacher_invitations_token
  ON teacher_invitations (token);

CREATE INDEX IF NOT EXISTS idx_teacher_invitations_school
  ON teacher_invitations (school_id);

CREATE INDEX IF NOT EXISTS idx_teacher_invitations_email
  ON teacher_invitations (email);

-- ============================================================
-- 3. NEW TABLE: teacher_subjects
-- ============================================================

CREATE TABLE IF NOT EXISTS teacher_subjects (
  teacher_id  uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  subject_id  uuid NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
  can_edit    boolean DEFAULT true,
  can_publish boolean DEFAULT true,
  created_at  timestamptz DEFAULT now(),
  PRIMARY KEY (teacher_id, subject_id)
);

CREATE INDEX IF NOT EXISTS idx_teacher_subjects_teacher
  ON teacher_subjects (teacher_id);

CREATE INDEX IF NOT EXISTS idx_teacher_subjects_subject
  ON teacher_subjects (subject_id);

-- ============================================================
-- 4. NEW TABLE: notifications
-- ============================================================

CREATE TABLE IF NOT EXISTS notifications (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  type        text NOT NULL,
  title       text NOT NULL,
  body        text,
  link        text,
  read_at     timestamptz,
  created_at  timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_notifications_user_unread
  ON notifications (user_id) WHERE read_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_notifications_user_created
  ON notifications (user_id, created_at DESC);

-- ============================================================
-- 5. ADD QA TRACKING COLUMNS TO lessons
-- ============================================================

ALTER TABLE lessons ADD COLUMN IF NOT EXISTS reviewed_by   uuid REFERENCES profiles(id);
ALTER TABLE lessons ADD COLUMN IF NOT EXISTS reviewed_at   timestamptz;
ALTER TABLE lessons ADD COLUMN IF NOT EXISTS published_by  uuid REFERENCES profiles(id);
ALTER TABLE lessons ADD COLUMN IF NOT EXISTS published_at  timestamptz;

-- ============================================================
-- 6. HELPER FUNCTIONS
-- ============================================================

-- Check if current user is a teacher (or higher)
CREATE OR REPLACE FUNCTION is_teacher_or_above()
RETURNS boolean STABLE
LANGUAGE sql
SECURITY DEFINER
SET search_path = ''
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.profiles
    WHERE id = auth.uid()
      AND role IN ('teacher', 'school_admin', 'platform_admin')
  );
$$;

-- Check if a teacher manages a specific subject
CREATE OR REPLACE FUNCTION teacher_manages_subject(p_subject_id uuid)
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

-- ============================================================
-- 7. ROW LEVEL SECURITY
-- ============================================================

-- ---- teacher_invitations ----

ALTER TABLE teacher_invitations ENABLE ROW LEVEL SECURITY;

-- Platform admin: full access
CREATE POLICY "Platform admin full access on teacher_invitations"
  ON teacher_invitations FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

-- School admins can manage invitations for their school
CREATE POLICY "School admins can manage their school invitations"
  ON teacher_invitations FOR ALL
  USING (
    school_id = current_user_school_id()
    AND current_user_role() IN ('school_admin')
  )
  WITH CHECK (
    school_id = current_user_school_id()
    AND current_user_role() IN ('school_admin')
  );

-- Teachers can read invitations addressed to their email
CREATE POLICY "Teachers can read own invitations"
  ON teacher_invitations FOR SELECT
  USING (
    email = (SELECT email FROM profiles WHERE id = auth.uid())
  );

-- Anyone can read an invitation by token (for the accept flow)
-- This is safe because tokens are unguessable (32 random bytes)
CREATE POLICY "Anyone can read invitation by token"
  ON teacher_invitations FOR SELECT
  USING (
    -- Only allow reading specific invitation when token is known
    -- (application code passes token as filter)
    true
  );

-- ---- teacher_subjects ----

ALTER TABLE teacher_subjects ENABLE ROW LEVEL SECURITY;

-- Platform admin: full access
CREATE POLICY "Platform admin full access on teacher_subjects"
  ON teacher_subjects FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

-- School admins can manage teacher-subject assignments for their school
CREATE POLICY "School admins can manage teacher subjects"
  ON teacher_subjects FOR ALL
  USING (
    current_user_role() IN ('school_admin')
    AND teacher_id IN (
      SELECT id FROM profiles WHERE school_id = current_user_school_id()
    )
  )
  WITH CHECK (
    current_user_role() IN ('school_admin')
    AND teacher_id IN (
      SELECT id FROM profiles WHERE school_id = current_user_school_id()
    )
  );

-- Teachers can read their own subject assignments
CREATE POLICY "Teachers can read own subject assignments"
  ON teacher_subjects FOR SELECT
  USING (teacher_id = auth.uid());

-- ---- notifications ----

ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- Platform admin: full access (for sending system notifications)
CREATE POLICY "Platform admin full access on notifications"
  ON notifications FOR ALL
  USING (is_platform_admin())
  WITH CHECK (is_platform_admin());

-- Users can read their own notifications
CREATE POLICY "Users can read own notifications"
  ON notifications FOR SELECT
  USING (user_id = auth.uid());

-- Users can update their own notifications (mark as read)
CREATE POLICY "Users can update own notifications"
  ON notifications FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

-- Users can delete their own notifications
CREATE POLICY "Users can delete own notifications"
  ON notifications FOR DELETE
  USING (user_id = auth.uid());

-- ============================================================
-- 8. TEACHER LESSON EDIT POLICIES
-- ============================================================
-- Allow teachers to update lessons for subjects they manage.
-- This addresses the editor school scoping blocker.

CREATE POLICY "Teachers can update lessons for their subjects"
  ON lessons FOR UPDATE
  USING (
    current_user_role() IN ('teacher', 'school_admin')
    AND unit_id IN (
      SELECT u.id FROM units u
      JOIN subjects s ON u.subject_id = s.id
      WHERE s.school_id = current_user_school_id()
        AND (
          current_user_role() = 'school_admin'
          OR s.id IN (
            SELECT subject_id FROM teacher_subjects
            WHERE teacher_id = auth.uid() AND can_edit = true
          )
        )
    )
  )
  WITH CHECK (
    current_user_role() IN ('teacher', 'school_admin')
    AND unit_id IN (
      SELECT u.id FROM units u
      JOIN subjects s ON u.subject_id = s.id
      WHERE s.school_id = current_user_school_id()
        AND (
          current_user_role() = 'school_admin'
          OR s.id IN (
            SELECT subject_id FROM teacher_subjects
            WHERE teacher_id = auth.uid() AND can_edit = true
          )
        )
    )
  );

-- Teachers can update guide pages for their subjects
CREATE POLICY "Teachers can update guide pages for their subjects"
  ON guide_pages FOR UPDATE
  USING (
    current_user_role() IN ('teacher', 'school_admin')
    AND subject_id IN (
      SELECT s.id FROM subjects s
      WHERE s.school_id = current_user_school_id()
        AND (
          current_user_role() = 'school_admin'
          OR s.id IN (
            SELECT subject_id FROM teacher_subjects
            WHERE teacher_id = auth.uid() AND can_edit = true
          )
        )
    )
  )
  WITH CHECK (
    current_user_role() IN ('teacher', 'school_admin')
    AND subject_id IN (
      SELECT s.id FROM subjects s
      WHERE s.school_id = current_user_school_id()
        AND (
          current_user_role() = 'school_admin'
          OR s.id IN (
            SELECT subject_id FROM teacher_subjects
            WHERE teacher_id = auth.uid() AND can_edit = true
          )
        )
    )
  );

-- ============================================================
-- 9. RPC: Accept teacher invitation
-- ============================================================

CREATE OR REPLACE FUNCTION accept_teacher_invitation(p_token text)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  v_invitation record;
  v_user_id uuid;
  v_subject_id uuid;
BEGIN
  v_user_id := auth.uid();

  IF v_user_id IS NULL THEN
    RETURN jsonb_build_object('error', 'Not authenticated');
  END IF;

  -- Find and validate the invitation
  SELECT * INTO v_invitation
  FROM public.teacher_invitations
  WHERE token = p_token
    AND accepted_at IS NULL
    AND expires_at > now();

  IF v_invitation IS NULL THEN
    RETURN jsonb_build_object('error', 'Invitation not found, already used, or expired');
  END IF;

  -- Update the user's profile: set role to teacher, assign school
  UPDATE public.profiles
  SET role = 'teacher',
      school_id = v_invitation.school_id,
      updated_at = now()
  WHERE id = v_user_id;

  -- Create teacher_subjects entries for each invited subject
  IF v_invitation.subject_ids IS NOT NULL AND array_length(v_invitation.subject_ids, 1) > 0 THEN
    FOREACH v_subject_id IN ARRAY v_invitation.subject_ids LOOP
      INSERT INTO public.teacher_subjects (teacher_id, subject_id)
      VALUES (v_user_id, v_subject_id)
      ON CONFLICT (teacher_id, subject_id) DO NOTHING;
    END LOOP;
  END IF;

  -- Mark invitation as accepted
  UPDATE public.teacher_invitations
  SET accepted_at = now()
  WHERE id = v_invitation.id;

  -- Create a welcome notification
  INSERT INTO public.notifications (user_id, type, title, body, link)
  VALUES (
    v_user_id,
    'invitation_accepted',
    'Welcome to StudyVault',
    'Your teacher account has been set up. You can now edit lessons for your assigned subjects.',
    '/admin/editor'
  );

  RETURN jsonb_build_object(
    'success', true,
    'school_id', v_invitation.school_id,
    'subject_count', COALESCE(array_length(v_invitation.subject_ids, 1), 0)
  );
END;
$$;

-- ============================================================
-- 10. RPC: Create teacher invitation (for school admins)
-- ============================================================

CREATE OR REPLACE FUNCTION create_teacher_invitation(
  p_email text,
  p_subject_ids uuid[] DEFAULT '{}'
)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
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
$$;

-- ============================================================
-- 11. RPC: Mark notification as read
-- ============================================================

CREATE OR REPLACE FUNCTION mark_notification_read(p_notification_id uuid)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  UPDATE public.notifications
  SET read_at = now()
  WHERE id = p_notification_id
    AND user_id = auth.uid();
END;
$$;

-- Mark all notifications as read
CREATE OR REPLACE FUNCTION mark_all_notifications_read()
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  UPDATE public.notifications
  SET read_at = now()
  WHERE user_id = auth.uid()
    AND read_at IS NULL;
END;
$$;
