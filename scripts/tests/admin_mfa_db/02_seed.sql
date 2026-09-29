-- Two schools; Tom (platform_admin, school A); teacher T1 (school A) and T2 (school B) with a
-- class each; one pupil in each class; free-tier and school content; one unpublished lesson.
INSERT INTO public.schools (id, name) VALUES
  ('aaaaaaaa-0000-0000-0000-00000000000a', 'School A'),
  ('bbbbbbbb-0000-0000-0000-00000000000b', 'School B');
INSERT INTO auth.users (id, email) VALUES
  ('00000000-0000-0000-0000-000000000001', 'tom@test'),
  ('00000000-0000-0000-0000-000000000002', 't1@test'),
  ('00000000-0000-0000-0000-000000000003', 't2@test'),
  ('00000000-0000-0000-0000-000000000004', 'p1@test'),
  ('00000000-0000-0000-0000-000000000005', 'p2@test');
INSERT INTO public.profiles (id, school_id, role, full_name) VALUES
  ('00000000-0000-0000-0000-000000000001', 'aaaaaaaa-0000-0000-0000-00000000000a', 'platform_admin', 'Tom'),
  ('00000000-0000-0000-0000-000000000002', 'aaaaaaaa-0000-0000-0000-00000000000a', 'teacher', 'T1'),
  ('00000000-0000-0000-0000-000000000003', 'bbbbbbbb-0000-0000-0000-00000000000b', 'teacher', 'T2'),
  ('00000000-0000-0000-0000-000000000004', NULL, 'student', 'P1'),
  ('00000000-0000-0000-0000-000000000005', NULL, 'student', 'P2');
INSERT INTO public.subjects (id, school_id, name) VALUES
  ('50000000-0000-0000-0000-000000000000', NULL, 'Free History'),
  ('5aaaaaaa-0000-0000-0000-000000000000', 'aaaaaaaa-0000-0000-0000-00000000000a', 'A History'),
  ('5bbbbbbb-0000-0000-0000-000000000000', 'bbbbbbbb-0000-0000-0000-00000000000b', 'B History');
INSERT INTO public.units (id, subject_id) VALUES
  ('60000000-0000-0000-0000-000000000000', '50000000-0000-0000-0000-000000000000'),
  ('6aaaaaaa-0000-0000-0000-000000000000', '5aaaaaaa-0000-0000-0000-000000000000'),
  ('6bbbbbbb-0000-0000-0000-000000000000', '5bbbbbbb-0000-0000-0000-000000000000');
INSERT INTO public.lessons (unit_id, status) VALUES
  ('60000000-0000-0000-0000-000000000000', 'live'),
  ('60000000-0000-0000-0000-000000000000', 'pending_review'),
  ('6aaaaaaa-0000-0000-0000-000000000000', 'live'),
  ('6bbbbbbb-0000-0000-0000-000000000000', 'live');
INSERT INTO public.classes (id, school_id, teacher_id, name) VALUES
  ('c000000a-0000-0000-0000-000000000000', 'aaaaaaaa-0000-0000-0000-00000000000a', '00000000-0000-0000-0000-000000000002', 'A 10X'),
  ('c000000b-0000-0000-0000-000000000000', 'bbbbbbbb-0000-0000-0000-00000000000b', '00000000-0000-0000-0000-000000000003', 'B 10Y');
INSERT INTO public.class_members (class_id, student_id) VALUES
  ('c000000a-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000004'),
  ('c000000b-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000005');
INSERT INTO public.teacher_subjects (teacher_id, subject_id) VALUES
  ('00000000-0000-0000-0000-000000000002', '5aaaaaaa-0000-0000-0000-000000000000');
