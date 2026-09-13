# Teacher dashboard — brief

Written 13 September 2026, the night before the teacher-dashboard session.
Nothing in the production tree was changed to write it. Mockups sit in
`design-lab/teacher-mockups/`.

The test this brief is written against: a teacher at 7:45am with a coffee opens
the page and gets the three most important facts in five seconds.

---

## (a) What the teacher screen shows today, and where every figure comes from

There is one teacher screen, `teacher/classes.html`, plus a printable
parents' evening pack that opens when a pupil's name is clicked. Sign-in and
sign-up are `teacher/login.html` and `teacher/signup.html`. All three wear
`css/teacher-shell.css` and `css/brand.css`, and never `css/reskin.css`.

The screen is, in page order:

| Block | What it says | Source |
|---|---|---|
| Class bar | class picker, roll size, join code | `/api/teacher/my-classes` — `classes`, `class_members`, `subjects` |
| Stats strip (3) | recall accuracy, pupils quizzed of roll, lessons reached | `/api/teacher/class-progress` → `attainment`, `coverage` |
| Last worked on … | five counts: this week / last week / this month / over a month / never | `activity`, bucketed from dates inside the progress blob |
| Where the class has got to | per unit: lessons reached, pupils started, typical lessons done | `coverage.units`, from `blob.done` plus the `lesson_visits` table |
| Questions the class gets wrong | question, the wrong answer most of them picked, the right answer, how many | `missedItems`, from `blob.kc[key].miss[]` |
| Misconceptions the class shares | named error pattern, where, pupils, times | `misconceptions`, from `blob.miscon` |
| Weakest lessons | lesson, accuracy, pupils, answers | `lessonAttainment`, from `blob.kc` tallied down the class |
| Weakest units | unit, accuracy, attempts | `weakestUnits`, from `blob.warmlog` |
| Students | name, lessons done, quiz accuracy, practice count, last active bucket | `students` |
| Build lessons from your own resources | a door to `/teacher/upload` | `canBuild` from `profiles.school_id` |
| Parents' evening pack | one printable page per pupil, plus an AI-drafted paragraph | `/api/teacher/student-pack`, `/api/teacher/pack-summary` (Bedrock eu-west-2, Haiku, fails closed) |

Everything on the class screen comes from one endpoint,
`api/teacher/class-progress.js`. That endpoint reads one `progress` row per
class member, deletes the never-send keys, filters every remaining key to the
class's base subject through `api/teacher/_lib/scope.js`, and aggregates. The
ownership rule and the subject filter live in `scope.js` so there is one copy
of the security filter. Evidence floors are enforced server-side: ten answers
before a class accuracy is printed, six answers and two pupils before one
lesson gets a percentage, twelve attempts before a unit does.

**The honest judgement.** The data on that page is good and the boundary work
is done properly. The problem is shape, not substance. It is eleven blocks of
roughly equal visual weight in one long scroll, ordered by how the data
happens to be structured rather than by what a teacher needs to decide. The
most actionable thing on the whole platform — the exact wrong answer fourteen
pupils picked — is the fifth block down, inside a table, below a coverage
table nobody checks on a Monday. Nothing on the page says what to do.

**Three things on it are quietly broken or wasted.**

1. `sv-misconception-log` is only ever written by `practice.html`. For an
   article subject — History, RS, Geography, Business — the "Misconceptions
   the class shares" table can never fill. Its empty state is written as if
   the class simply has not triggered one yet. For most teachers it is a
   permanently empty table.
2. `blob.practice` is the richest record on the platform: every AI-marked
   answer with the question, the marks available, the pupil's own words and
   the marker's feedback. The class screen uses `.length`. Everything else is
   discarded.
3. `js/strength.js` computes a real retrieval-strength model on the student
   side, and no teacher endpoint knows it exists.

---

## (b) What we can know per pupil and per class — and what we cannot

### Two sync paths, and only one reaches a teacher

This is the thing to know before designing anything.

- `js/main.js` (~line 2626) writes one **`progress`** row per pupil, keyed
  `person_id`, with a single `blob`. This is what every teacher endpoint
  reads.
- `js/account-sync.js` writes the whitelisted keys one row each into
  **`user_state`**. No teacher endpoint reads that table at all.

So a key can be fully account-synced and still invisible to a teacher.

### In `progress.blob` today — available, subject-scoped, usable now

| Blob key | localStorage key | Shape | What it can answer |
|---|---|---|---|
| `kc` | `sv-kc-log` | `{"sub/unit/n": {d, s, t, miss:[{q, chose, right}]}}` | Recall accuracy by pupil, lesson, unit. **And the exact distractor chosen.** Dated. |
| `done` | `sv-lessons-done` | `{"sub/unit": [n, …]}` | Lessons completed against the weighted model |
| `when` | `sv-lessons-when` | `{"sub/unit/n": "YYYY-MM-DD"}` | Date a lesson was finished — the decay clock |
| `practice` | `sv-practice-log` | `[{d, k, q, m, a, r}]`, last 40 | AI-marked exam answers: question, marks available, the answer, the marker's feedback |
| `warmlog` | `sv-warmup-log` | `{"YYYY-MM-DD": {total, units: {"sub/unit": {a, m}}}}` | Warm-up accuracy per unit. Use attempts, never misses alone |
| `miscon` | `sv-misconception-log` | `[{d, sub, unit, n, tag}]`, last 200 | Named, evidenced error patterns — **practice-format subjects only** |
| `tasks` | `sv_progress_*` | per-lesson task state | Which components of a lesson were done |

Plus tables: `class_members` (the only door to a pupil), `profiles`,
`lesson_visits` (opened but not finished), `units`, `lessons`,
`knowledge_check_scores`.

### Computable server-side but not computed today

**Retrieval strength, per lesson, 0–100.** `js/strength.js` takes four kinds
of evidence and decays each one by half over a half-life that lengthens with
repetition (3, 6, 12, 24, 48 days), then takes the strongest surviving piece.
Three of its four inputs are already in the blob:

- quiz — `kc` → `25 + 75·(s/t)`, dated `d`
- read — `done` + `when` → `45`
- marked answer — `practice` → `25 + 75·(mark/marks)`, dated `d`
- cards — `flashsr` → **on the never-send list, so excluded**

Bands are the school's words, from `js/progress.js`: **emerging** under 40,
**developing** 40–69, **secure** 70 and over. The revisit line is 55. A
lesson with real evidence that has decayed under 55 is "due a revisit".

This is the single biggest unused asset. It gives a class its topic bands,
and — projected three days forward, exactly as the student planner does — it
gives **what the class is currently forgetting**. No competitor has it
because no competitor has the decay model.

**Exam-technique gaps.** `blob.practice[].r` is the marker's own feedback
text, and `m` is the marks available. `strength.js` already parses `n/m` out
of `r`. Averaged across a class by unit, that is "they are scoring 40% of the
marks on eight-mark questions in Germany". That is a teaching fact.

### What we cannot know yet — say this plainly

- **Per-pupil identity at scale.** Microsoft SSO is waiting on Entra admin
  consent. Until that lands, a pupil reaches a class only by typing a join
  code into a StudyVault account they made themselves. Every class roll is
  opt-in and partial. Any screen must read correctly when half the class is
  missing, and must never imply an absent pupil has done nothing.
- **Free-tier pupils are invisible, permanently.** They have no school, so
  nothing leaves their account. This is a rule, not a gap.
- **Card-level weak spots.** `flashsr` is on `NEVER_SEND` in `scope.js`. The
  `weakCards` / `cardHotspots` work parked on the `retrieval-strength` branch
  needs that rule changed first. See the open questions.
- **Revisit outcomes, widget mastery, exit tickets.** `sv-revisit`,
  `sv-widget-done` and `sv-exit-log` sync to `user_state` only. They are
  captured and unreachable. Either `main.js` adds them to the blob, or a
  teacher endpoint learns to read `user_state`.
- **Named misconceptions for article subjects.** Nothing outside
  `practice.html` writes `sv-misconception-log`.
- **Anything about when or how much one named child worked.** Aggregate only,
  by the 12 August rule. The parents' evening pack is the one agreed
  exception, and it stays an exception.

---

## (c) What is maximally useful to a classroom teacher, ranked

1. **The three wrong answers to reteach, with the exact words the class
   chose.** "Fourteen chose 'about a tenth' when the answer is 'two-thirds'"
   is a starter slide; "fourteen got this wrong" is a number. It is already
   captured on every knowledge check ever taken, so it costs nothing.
2. **What the class is forgetting.** Topics they learned, scored well on, and
   have now decayed under the revisit line. This is the one thing a revision
   platform can say that a markbook cannot, and it is the honest answer to
   "what should my do-now be".
3. **Five names to have a word with, each with one reason.** Teachers act on
   names, not on distributions. Capped at five so it stays a to-do rather
   than a roll call, and worded as attainment.
4. **Exam-technique gaps from the marked answers.** "They lose the marks on
   the 8-markers in Germany" changes next lesson's teaching; a recall
   percentage does not. The evidence is sitting unused in `blob.practice`.
5. **Who has not started at all.** Already computed as buckets. Buckets get
   read and forgotten; names get chased. Show the names.
6. **Weakest lessons and units.** Real and useful, but they answer a
   planning question rather than a Monday question. They belong below the
   fold.
7. **The parents' evening one-pager.** Already built and genuinely good. It
   should open from a pupil's name anywhere on the screen, not only from the
   bottom table.
8. **Curriculum coverage.** A once-a-half-term check. Keep it; demote it.

Two things deliberately **not** on this list: anything resembling work-setting
or due dates, which is outside the vision; and any per-pupil timeline, which
is what gets a school to withdraw.

---

## (d) A recommended direction, and two alternatives

### Recommended — the Monday briefing

The page opens with a dated line of prose that says what happened and what to
do about it, then three action panels in a fixed order: **Reteach this**,
**Going cold**, and **Have a word**. Each panel holds at most three items,
and each item is a complete teaching thought — the question, the exact wrong
answer, the count. Under those sits a quiet divider and everything the
current screen already shows, unchanged in substance and reordered by
usefulness.

It wins because it is the only shape that passes the five-second test while
throwing nothing away. A teacher who wants the tables still has them; a
teacher with a coffee never scrolls. It is also the cheapest to build: two of
the three panels are re-renders of data `class-progress.js` already returns,
and the third needs the strength model ported server-side, which is about
sixty lines of arithmetic that already exist in `js/strength.js`. It carries
one honest risk, which is that a briefing sentence assembled from thin
evidence reads as confident nonsense — handled the way the endpoint already
handles it, by refusing to speak below the evidence floors and saying so.

I would put a **Project this** button on the reteach panel, which opens the
third direction below as a full-screen starter. That combination is my actual
recommendation: a briefing you read, with a one-click route to the artefact
you teach from.

### Alternative one — the markbook

A class-by-topic grid: units across the top, pupils down the side, one
strength band per cell in the school's own words. Teachers read grids without
being taught how, it prints for a department meeting, and it answers "which
topic" and "which pupil" in a single object rather than two panels.

It fails the five-second test. A grid tells you everything and therefore
recommends nothing — the teacher still has to do the reading. It also invites
a use it should not have: a grid of coloured cells per child looks like a
grading instrument, and the moment a head of department exports it to a
spreadsheet, an attainment tool becomes a monitoring one. Worth building
later as a tab, not as the front door.

### Alternative two — the lesson starter

The dashboard stops being a report and becomes teaching material. One
projectable page: the three questions this class got most wrong, in display
type, with the distractor concealed until the teacher taps it, and the class's
own tally revealed after. It is the most distinctive thing we could ship and
it targets a teacher's real bottleneck, which is making the do-now, not
reading the report.

On its own it is too narrow. It answers "what do I teach first thing" and
nothing else — not who to chase, not what is fading, not what parents will
ask on Thursday. It earns its place as a button on the briefing, not as the
screen.

### On the visual language

**Move the teacher pages onto the student dashboard's paper-and-ink look.**
This is a small change dressed as a big one: `css/teacher-shell.css` and
`classic.html` already declare the *same* `--paper:#f6f1e7`,
`--card:#fffdf8`, `--ink:#26231e`, `--line:#e4dfd2`. What differs is
geometry and accent — the teacher pages use 16px radii with soft shadows and
a brown `--anchor` for every action, while the student page uses 4px radii, a
hairline border, and the brand rust `#c06325` for the one thing you press.

Three reasons to move. The 16px-and-soft-shadow card is exactly the generic
SaaS look that keeps getting rejected elsewhere on this project, and it is
the only place left carrying it. Rust is the brand's accent and the teacher
pages currently do not use it at all, so a teacher and a pupil in the same
school see two products. And a school evaluating us will see both screens in
the same meeting.

Keep `--anchor` brown for text links, secondary buttons and table chrome, so
rust stays scarce enough to mean *act here*. Keep Caveat for one thing only —
the date stamp beside the wordmark — or it turns twee. Tables keep their
current geometry; only their borders and radii change.

---

## (e) Open questions for Tom

1. **Are flashcard boxes attainment or study habits?** `flashsr` is on the
   never-send list, so the card-level weak spots parked on the
   `retrieval-strength` branch cannot ship as built. My view: *which cards a
   pupil keeps getting wrong* is attainment and belongs to the teacher, while
   *when they reviewed them and how often* is habit and does not. Splitting it
   that way unblocks the work. Your call, because it changes a written rule.
2. **Do we fix the misconception table, or retire it?** For History it can
   never fill. Either article lessons start writing tags on a wrong knowledge
   check, which is a content job across the fleet, or the table merges into
   "questions the class gets wrong" and the distinction disappears from the
   teacher's view.
3. **Five names, or the whole class?** I have capped "have a word" at five,
   which makes it a to-do list. A head of department may want the full roll.
   A cap is a design position, not a technical limit.
4. **Should the AI write the briefing sentence?** The parents' evening pack
   already drafts a paragraph on Bedrock London for about a penny. The same
   route could write the Monday line. Cheaper and safer is to assemble it
   from templates and never let a model near it. My preference is templates,
   because a teacher reads that line in five seconds and will not check it.
5. **Does the class screen wait for SSO, or ship on join codes?** Everything
   here works today for a class that typed a code in. If the answer is wait,
   the September build is the redesign only; if ship, the empty and partial
   states need as much care as the full ones.
