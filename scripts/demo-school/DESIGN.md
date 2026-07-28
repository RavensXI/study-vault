# Demo High School — the seeded cohort on the real pipe

**Goal.** Build the launch plumbing (events table + RLS + real classes) and
prove it with a full synthetic school: every dashboard — student and teacher —
running on the same code path real schools will use. The only fictional thing
is the people.

## Tenant

- School: **Demo High School**, slug `demo-high`, `settings.demo = true`.
- Every seeded profile carries `is_demo = true` (column already existed).
- Wipe = delete by school_id (accounts via admin API, rows cascade).

## Cohort

- **Year 10 + Year 11**, default 150 students each (`--year-size`).
- Accounts: `firstnamelastname@demo.studyvault.co.uk`, one shared password
  (set at seed time via `--password`, never committed).
- Each student: global ability + per-subject wobble, an engagement archetype
  (steady / crammer / quiet / struggling / grafter / flying), an activity
  history over the past ~12 weeks. Year 11 are further through every course
  and revise harder (exams nearer).

## Departments (board + topics chosen ONCE, like a real school)

| Subject | Board pick (slug) | Taken by |
|---|---|---|
| Maths | maths-edexcel | all |
| English Language | english-language-aqa | all |
| English Literature | english-literature-aqa | all |
| Combined Science | science-aqa | ~75% |
| Separate Sciences | separate-sciences | top ~25% |
| History | history-aqa | option ~55% take Hist or Geog |
| Geography | geography-aqa | option |
| French | french-aqa | option ~40% take a language |
| Spanish | spanish-aqa | option |
| Business | business-edexcel | option |
| Computer Science | computer-science (OCR) | option |
| PE | physical-education-aqa | option |
| Psychology | psychology-aqa | option |
| Drama | drama-aqa | option |
| Religious Studies | religious-studies-aqa | option |

Every student: core (Maths, Eng Lang, Eng Lit, a science) + 4 options.
Departmental unit choices (e.g. History's four studied options) are fixed in
`seed.py` config, queried from the real generic subjects so every link a demo
student clicks lands on a real lesson.

## Classes & teachers

- Per subject per year: students split into classes of ≤28, named
  `10H1`, `11G2` (year + subject letter + index).
- Teacher accounts (same email domain + password, `role = 'teacher'`),
  one per ~2 classes, wired via `classes.teacher_id`.

## The events table (the new launch plumbing)

`scripts/_create_events_table.sql` — one row per piece of retrieval evidence:
warm-up answer, quiz miss (with chosen distractor), shorts check, flashcard
box move, named misconception, lesson completion. RLS:

- students insert/select their own rows only;
- teachers select rows for students in classes they own;
- service key seeds/wipes.

Client capture keeps writing localStorage + user_metadata (offline-first,
existing behaviour) and gains a queued double-write to `events` when signed
in. The teacher dashboard reads ONLY `events` + classes.

## Two sinks, one generator

The activity generator writes each student's history twice:
1. `user_metadata.sv_progress` — so signing in as the student restores their
   dashboards exactly as the sync layer expects;
2. `events` rows — so the teacher pipeline aggregates the same truth.

## Order of work

1. ✅ events table + RLS applied
2. seed.py phase A: roster, accounts, classes, memberships
3. seed.py phase B: activity generator (port of the teach.html synthetic
   generator, against real unit structures) → both sinks
4. teach.html: swap inline generator for the events API (class picker becomes
   real); keep the synthetic mode behind `?synthetic=1` for public demos
5. student-side capture: double-write to events when signed in
