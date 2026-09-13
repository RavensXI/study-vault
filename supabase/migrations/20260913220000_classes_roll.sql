-- Register size (13 Sep 2026): how many pupils the teacher has on their own
-- register, so the class screen can say "24 of 28 have joined". A number only.
alter table public.classes add column if not exists roll int check (roll is null or (roll between 1 and 60));
