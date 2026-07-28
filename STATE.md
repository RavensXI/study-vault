# STATE — where everything is right now

_Last updated: 27 July 2026. One page. If this file and your memory disagree, trust this file, then update it._

## What's live

| Thing | Where |
|---|---|
| **Production** | `platform` branch → www.studyvault.co.uk — **untouched by any of this work** |
| **The preview** | `landing-wizard` branch → `study-vault-git-landing-wizard-…vercel.app` (Vercel builds every push; deployment-protected, so only Tom's logged-in browser sees it) |
| **Local dev** | `python design-lab/serve.py` → localhost:8901 (mimics the Vercel rewrites) |

On the preview branch only, `/` redirects to `/welcome`. Making that the real front door is a launch decision, not yet made.

## The flow (what a student experiences)

`/welcome` → picker (core four pre-ticked) → exam boards → topics (one question
at a time; History options, Lit set texts, RS religions, etc.) → **the real
dashboard** (`/classic`, day-one state, everything links to real lessons) →
sign-up is opt-in from the dashboard, never a gate. Sign-in restores the whole
setup from the account on any device.

## The five files that ARE the product flow

| File | Job |
|---|---|
| `design-lab/home-study.html` | Landing scene + wizard + real Supabase sign-up/sign-in |
| `design-lab/dash-data.js` | **The shared data layer** — wizard hand-off, subject catalog (NAMEC), slug + first-unit maps, completion rollup, unit scoping (`keepUnit`), the live Supabase units fetch. Both dashboards call `svDashInit()` |
| `design-lab/dash-classic.html` | The dashboard skin (planner modal, day-one UI, renderers) |
| `design-lab/dash-desk4.html` | The cosy-desk skin of the same dashboard (same `svDashInit` contract) |
| `css/reskin.css` | The lesson/browse/practice/guide look, incl. Young Serif masthead + dark mode |

Rule: anything both dashboards need lives in `dash-data.js`, never copy-pasted
into the pages. Staging hooks (`?picked` `?boards` `?tsel` `?done` `?snap`)
are parsed there too, so they behave identically on both views.

Supporting cast: `design-lab/warmup.js` (the Start-button warm-up quiz — 10
knowledge checks pulled from the student's own current units, once a day,
then into the lesson; shared by both dashboards), `design-lab/planner.js`
(the revision-plan engine + modal + day tooltip, shared — classic's exam
card and the desk's calendar postcard open the SAME planner),
`design-lab/skin-switcher.js` (applies the desk-world skin to real pages +
the reading tour; design-lab only), `design-lab/serve.py`, `vercel.json`
(rewrites), `js/main.js` (a11y toolbar — owns dark mode; stamps completion
dates).

## The data contract

- `localStorage["sv-welcome"]` = `{picked, boards, topics, meta}` — written by the
  wizard, read by both dashboards. `meta` carries resolved board labels + topic
  *names* so dashboards don't need the options dataset.
- Signed up/in: the same object lives in the account as `user_metadata.sv_welcome`.
  Sign-in restores it; while signed in, every wizard change syncs up (debounced).
  `localStorage["sv-user"]` = `{email}` marks the signed-in state for the prototypes.
- **Progress syncs to the account too** (`user_metadata.sv_progress`, via
  `design-lab/sync.js`): completions, dates, per-lesson task ticks, plan prefs,
  warm-up/flashcard stamps. Dashboards pull-merge on load and push after;
  lesson pages push after each completion (inline in `js/main.js`); sign-in
  restores it all onto a fresh device. Merges are ADDITIVE (union/OR) so no
  device can erase another's work. Sign-out pushes, then wipes the device —
  safe because the account now holds everything. Guests stay local-only.
- **Lesson completion is WEIGHTED** — `design-lab/LESSON_COMPLETION_SPEC.md`
  (agreed 27 Jun): exam question 40, flashcards 15, revision task 15,
  quiz/video/podcast 10 each, highlighter 0; done at ≥50% of available.
  Lesson pages write completions to `localStorage["sv-lessons-done"]`
  (`{"subject/unit":[numbers]}`) + completion dates to `sv-lessons-when`
  (powers the "this week" figures); dashboards read both.
- `localStorage["sv-warmup"]` = `{date,correct,total}` — today's warm-up
  result; Start skips the warm-up once it's done for the day.
- Exam countdowns on BOTH dashboards come from `EXAMS`/`svFirstLast()` in
  `dash-data.js` — never hardcode a day count in a view.
- Topic choices for History/Lit are literal Supabase **unit slugs** — "start
  lesson 1" links go straight into the chosen option/text.
- Real subject slugs + first units were **queried from Supabase**, not guessed
  (maps live once, in `design-lab/dash-data.js`: `SUBSLUG`, `FIRSTUNIT`).

## QA / staging hooks (all harmless in production)

`?snap` (kill animations for screenshots) · `?picked=&boards=&tsel=&tstep=`
(stage wizard state) · `?done=` (stage lesson completions) · `?probe` (page
reports control coordinates) · `?plan=YYYY-MM` (open planner at a month) ·
`?warmup=1` (auto-open the warm-up overlay) · `?psim=warm.lesson.cards`
(fake today's plan steps done) · `?fc=1|2` (open the flashcard modal,
2 = flipped) · `?user=email&menu=1` (fake signed-in avatar + open its menu) ·
`?forcecheck=1` (shorts feed: splice a recall card immediately) · `?dark=1` /
`?notour=1` / `?csprobe=1` (skin-switcher QA) · `?bench` (Tom's tuning bench).

## Generators (rerun any time; all in `scripts/`)

- `_designlab_wizard_demos.py` — the 3 demo loops + 42s full cut (probe-driven clicks, click-QA sheet)
- `_designlab_picker_demo.py` — original picker loop (superseded by the above)
- `_designlab_sketch_arrows.py`, `_designlab_shelf_lower.py`, `_designlab_shelf_bricabrac.py`, `_designlab_shelf_atmosphere*.py` — Gemini art props for the landing scene

## Teacher side (rudimentary, 14 Jul)

`design-lab/teach.html` (route `/teach`) — reader-skin teacher dashboard over a
SYNTHETIC 28-student class built on the real History AQA structure. The
aggregation code is the real thing: it consumes exactly the `sv_progress`
shape students sync. Surfaces: triage sentences (reteach candidate, gone
quiet, slipping, flying — all computed), topic recall grid, needs-first
roster with sparklines, student drill-in (warm-up trend, keeps-missing by
lesson, AI-marked practice transcripts). AI = ONE weekly brief per class
(`scripts/_teach_digest.py` → claude -p over aggregates → `teach-digest.js`)
+ the already-paid-for stored marking feedback. Capture feeding it (all in
sv_progress): warm-up misses + per-unit attempts, KC scores (`sv-kc-log`),
shorts check answers (`sv-shorts-checks`), flashcard self-marks
(`sv-flash-log`), practice answers + AI feedback (`sv-practice-log`).
Per-student pack: `?pack=N` — ONE A4 page (print-to-pdf verified), parent-
readable labels, AI draft via `scripts/_teach_pack.py`, teacher-triggered.

**Reframed into three tabs (28 Jul):** This week (triage + digest) · Topics
(recall grid with trend + Leitner mastery bars, shared-misconception panel,
most-missed lessons) · The class (roster + drill-in). New surfaces: fading
topics (fortnight-on-fortnight recall drop), "not sticking" flag (revising
most days, recall low+flat → technique conversation), misconception lines
("352 of 585 wrong answers chose X"). Powered by new student-side capture
(28 Jul, all account-synced): chosen distractor on every warm-up/quiz/shorts
miss, named misconception diagnoses from guided practice
(`sv-misconception-log`), Leitner boxes (`sv-flashcard-progress`) now in
sync.js. QA: `?tab=week|topics|class`.

**DECIDED (14 Jul, revised 27 Jul): the teacher dashboard is a PAID feature
and a headline reason schools pay. Free tier = student experience only.**
It ships on BOTH paid ramps (the Seneca land-and-expand shape):

- **Department tier (bottom-up):** a head of department signs up self-serve.
  The teacher creates a class and hands students a **join code**; students
  sign in like free users (email+password or "Continue with Google/Microsoft"
  — push the school email at signup). The code enrols the student into the
  class and grants the premium entitlement. No SSO, no DPO conversation,
  live in minutes. *(This revises 14 Jul's "no class codes" — that stays
  true for the school tier only.)*
- **School tier (top-down):** whole-school licence. Students/teachers sign
  in with school SSO and classes MIRROR the school's own directory (Teams /
  Classroom groups) — we never own or maintain rosters at this tier. Roster
  import later if a deal demands it: Teams/Graph first (UK is Microsoft),
  Wonde for MIS-level rostering.
- **Upgrade path (dept → school):** classes are ADOPTED into the school
  workspace, never duplicated; a student's evidence history must survive the
  transition (see identity schema below — this is why it exists).

Prerequisites for the real build: Entra admin consent (still pending),
Graph/Classroom group reads, capture moved to an events table + RLS, Stripe
for department self-serve.

## Identity schema (locked 27 Jul — bake into the launch schema)

**Person ≠ credential ≠ entitlement.** Three layers, so SSO arriving later
never forks accounts and the dept→school upgrade never orphans evidence:

- **Person** = one durable UUID (Supabase `auth.users`). ALL StudyVault data
  (progress, class membership, evidence) foreign-keys to this UUID — never
  to an email. Emails change and get recycled; the UUID does not.
- **Credential** = a sign-in method linked to the person (Supabase
  `auth.identities`): email+password (identifier = verified email), Google
  (identifier = `sub` claim, NOT the email), Microsoft (identifier =
  `oid`+`tid`, NOT the UPN). One person, many credentials.
- **Entitlement** = who pays, in our own table: department subscription
  scoped to school+subject; school licence scoped to school. A student's
  premium status = the union of their active entitlements. Class codes
  enrol + entitle; they never create identity.

Linking rules: **auto-link ONLY on a provider-verified matching email**
(unverified match = the classic account-takeover vector — never). Any other
merge is manual and proven by possession: sign into account A, then complete
a live sign-in with credential B inside that session, then merge —
ADDITIVELY (`svProgressMerge` semantics: a wrong merge can never destroy
data). Names/classes/year groups are hints for a teacher-flagged "same
student?" prompt, never linking evidence by themselves. Supabase implements
the person/credential layers natively (`linkIdentity()`, verified-email
auto-linking) — build only the entitlements table and the merge UX.

## Parked / open decisions

- **Paper→content mapping** for the planner taper (unit→paper per subject-board;
  "cumulative" flag for Maths/languages). Data task against the specs DB.
- **Supabase redirect allow-list** (Tom, dashboard): add
  `https://*-tom-shauns-projects.vercel.app/**` + `http://localhost:8901/**`
  so confirmation emails return to the preview instead of the live site.
- **Mobile layout** for the fixed-canvas landing — deliberately deferred.
- **Merging `landing-wizard` → `platform`** — nothing merges without Tom's word.
- Planner uses a **provisional summer-2027 timetable** (in dash-classic);
  real build reads `data/exam-dates-*.json`.

## Archive

`design-lab/archive/` = 39 retired prototypes (old homepages, dashboard
directions, concept pages, test harnesses). Reference only; nothing links to
them. Six older files remain in `design-lab/` because live rewrites or pages
still point at them (`bookbench`, `gold-lab`, `_shelf_compare`,
`dashboard-paths-v2`, `dashboard`, `hero-showcase`).
