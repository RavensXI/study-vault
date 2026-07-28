-- Fix: infinite recursion between classes <-> class_members RLS policies
-- (surfaced 2026-07-28 when the teacher dashboard first exercised them).
-- Cross-table checks move into SECURITY DEFINER helpers, which read with
-- owner rights and so never re-enter the policy chain.

create or replace function public.member_class_ids(uid uuid)
returns setof uuid
language sql security definer set search_path = public stable as
$$ select class_id from public.class_members where student_id = uid $$;

create or replace function public.staff_class_ids(uid uuid)
returns setof uuid
language sql security definer set search_path = public stable as
$$ select c.id from public.classes c
   join public.profiles p on p.id = uid
   where p.role in ('teacher', 'school_admin') and c.school_id = p.school_id $$;

create or replace function public.taught_student_ids(uid uuid)
returns setof uuid
language sql security definer set search_path = public stable as
$$ select cm.student_id from public.class_members cm
   join public.classes c on c.id = cm.class_id
   where c.teacher_id = uid $$;

drop policy if exists "Students can read their classes" on public.classes;
create policy "Students can read their classes" on public.classes
  for select using (id in (select public.member_class_ids(auth.uid())));

drop policy if exists "Teachers can manage class members" on public.class_members;
create policy "Teachers can manage class members" on public.class_members
  for all using (class_id in (select public.staff_class_ids(auth.uid())));

drop policy if exists events_teacher_select on public.events;
create policy events_teacher_select on public.events
  for select using (person_id in (select public.taught_student_ids(auth.uid())));
