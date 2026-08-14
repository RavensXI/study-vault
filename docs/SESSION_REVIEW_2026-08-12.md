# Session Review Pack — 12–13 August 2026

**Purpose:** a complete, checkable record of one working session, written so an
independent reviewer (human or model) can verify the claims rather than take
them on trust.

**Branch:** `platform` · **Range:** `a043e5ed..00063651` (20 commits)
**Deployed:** yes, to https://www.studyvault.co.uk (Vercel, `lhr1`)
**Scope:** 27 files, +2,897 / −33 lines
**Author's note:** written by the assistant that did the work. Where something is
unverified, self-corrected, or was got wrong first time, it says so — those are
the places most worth a reviewer's attention.

---

## How to review this

The claims below are ordered by **risk**, not chronology. Sections 1–3 touch
children's data, data residency, and access control; they are where a review
should concentrate. Sections 4–6 are product work. Section 7 is a planning
document with no code. Section 8 lists what I know is still weak.

Everything ran against the **live production database**. There was no staging.

---

## 1. Access control — a real leak, found and closed

### 1.1 Review queue showed a teacher other subjects' content
`api/pipeline/review.js` · commit `da4afe79`

**Reported by Tom, not found by me.** Signed in as a history teacher at Unity, he
saw all 30 Music AQA lessons awaiting review.

**Cause:** the subjects *dropdown* was scoped by `teacher_subjects`; the lesson
*list* underneath it was not. It filtered by subject only when the client asked
it to, so with no filter selected any signed-in teacher received up to 200
lessons from any subject and any school. Worse, the scoping lived inside the
block that builds the dropdown, and the `lessons_only=1` fast path — the request
the page makes on every refresh — skipped that block entirely.

**Fix:** permitted-subject set computed once, before the fast path, applied to
both. A client-supplied `subject_id` is checked against it, or the filter becomes
the way around the boundary.

**Verified** against the live database as Tom's real teacher profile:

| Case | Before | After |
|---|---|---|
| No filter | Music AQA visible | 0 lessons |
| `lessons_only=1` | unscoped | scoped |
| `subject_id=music-aqa` directly | would work | 403 |
| platform_admin | everything | unchanged |

**Reviewer should check:** that writes were genuinely already safe. I claim
`publish` verifies `teacher_subjects.can_publish` per subject and
approve/reject/completion actions are admin-only — so this was read-only
exposure. Worth confirming independently.

**Deliberately not changed:** the no-assignment fallback excludes generic
content, despite a comment above it claiming "+ generic". I left the behaviour
and corrected nothing, on the grounds that widening access is not a thing to do
as a side effect of fixing a leak. A reviewer may disagree.

### 1.2 `/teach` was an ungated page that read live pupil data
`teach.html` · commit `3b55a1b9`

Linked publicly from the home page as "Try the teacher dashboard", carrying no
auth gate, and it switched from synthetic demo data to **real student
attainment** whenever a signed-in teacher happened to have classes. Its only
protection was row-level security being exactly right.

Now synthetic by default; `?live=1` opts in during development. Real data lives
at `/teacher/classes` behind the gate.

### 1.3 Subject scoping on the new endpoint
`api/teacher/_lib/scope.js`

First version of `class-progress` aggregated each child's **whole** progress
blob, so opening a maths class showed Macbeth misconceptions. Now scoped to the
class subject, matched on base slug so `maths-edexcel` classes still see
`maths-aqa` progress.

**A false pass worth knowing about:** after scoping, maths returned zeroes
everywhere. That was correct — maths is practice-format and has no knowledge
checks — but it is indistinguishable from a filter that has emptied everything.
Re-tested on English Literature to prove it narrows rather than wipes.

---

## 2. Data residency — closed two ways pupil work could leave the UK

`api/_lib/claude.js`, `api/ai-mark.js` · commit `4307ac6d`

**I overstated the problem first and corrected it.** I told Tom "the other AI
routes still fail open"; they do not. `callClaude` has always refused to fall
back once Bedrock is configured, and production has been on `bedrock:eu-west-2`
throughout — verified by calling `/api/ai-mark` and reading `servedBy`.

Two genuine holes existed:

1. **Bedrock not configured at all** fell straight through to
   `api.anthropic.com` silently. Not hypothetical — it is what my first test of
   the parents' evening summary hit, and the only reason it was noticed is that
   the route reports `servedBy`. A preview deploy or one deleted variable
   reproduces it with real pupil work in the request.
2. **`ai-mark.js`'s Groq path never touches `_lib/claude.js`**, so no UK guard
   applied to it. `GROQ_API_KEY` is unset in production (verified: quick tier
   reports `bedrock:eu-west-2`), but setting it would silently route marking to a
   US provider.

Both now governed by the existing `ALLOW_US_FALLBACK` switch — one thing to
reason about rather than three. With it set, requests work, log loudly, and say
so in `servedBy`.

**Verified after deploying**, because a fail-closed change can take a feature
down:

| Route | Result |
|---|---|
| ai-mark quick tier | `bedrock:eu-west-2` Haiku, marked 2/2 |
| ai-mark exam tier | `bedrock:eu-west-2` Sonnet |
| /api/simplify | 200 |
| /api/tutor | alive (400 = my malformed test payload) |

**Reviewer should check:** whether `ALLOW_US_FALLBACK` governing both the
unconfigured case and the mid-call fallback is the right coupling, or whether
they warrant separate switches.

---

## 3. Children's data — what a teacher can see

`api/teacher/class-progress.js`, `_lib/pack.js`, `pack-summary.js`

Boundary agreed with Tom and recorded in memory: send attainment; aggregate
anything about *when or how much* a child worked; never send flashcard spacing,
planner preferences, rest days or shorts watched. Last-active is bucketed
(`this week` / `last week` / …), never timestamped.

**One deliberate exception, flagged to Tom before building it.** The parents'
evening pack shows **days revised** and a run of **daily warm-up scores** — per-child
effort data, which the rule makes aggregate-only. Justification: the pack is
printed for that child's own parent, where effort is ordinary report content.
Fenced by: capped at 10 sessions, dates never times, and it appears nowhere on
the class screen. The reasoning is written into `api/teacher/_lib/pack.js` so
whoever changes it next sees the trade.

**`pack-summary.js` fails closed on region** and refuses to return a draft whose
`servedBy` is not Bedrock. It rebuilds the evidence server-side from class id +
student id rather than accepting it from the client, so a page cannot put its own
text in front of the model. The model receives a first name only — no surname, no
identifiers, no session dates.

**Membership is checked, not just class access:** being allowed to open a class
is not being allowed to open any pupil id the caller can name. Verified — a
non-member returns 404, with the same message as "no such pupil" so the endpoint
cannot be used to probe for who exists.

**Reviewer should check:** whether the effort-data exception is defensible, and
whether bucketing is coarse enough. This is the judgement call I am least certain
about.

---

## 4. Teacher platform — new, and the reason for most of the above

### 4.1 What was built
| File | What |
|---|---|
| `api/teacher/class-progress.js` | class aggregation: activity buckets, weakest units, **most-missed questions with the wrong answer students actually chose**, student table |
| `api/teacher/my-classes.js` | a teacher's classes + join codes + roll sizes; `canBuild` capability |
| `api/teacher/create-class.js` | create a class, allocate a join code |
| `api/class/join.js` | student joins by code |
| `api/teacher/student-pack.js` | one pupil's parents' evening pack |
| `api/teacher/pack-summary.js` | AI-drafted teacher paragraph, UK-only |
| `teacher/classes.html` | the consolidated teacher screen (700 lines) |
| `scripts/_create_class_join_codes.sql` | migration — **Tom ran this manually** |

### 4.2 The finding that mattered most
The knowledge-check log already stores **which wrong answer each student
picked** (`miss: [{q, chose, right}]`), retrospectively, for every quiz ever
taken. Class-level item analysis therefore needs no authoring at all — which
contradicts the cost estimate I gave Tom that morning about surfacing
misconceptions. Written up in memory.

It also catches our own bad questions. The first run flagged students repeatedly
picking "The Prince of Cats" for Tybalt and being marked wrong. **They were
right** — Mercutio uses "more than prince of cats" (2.4) and "good king of cats"
(3.1). The multiple choice offered both and failed the more famous one. Fixed in
place; checked all four English Literature boards, only that one was defective.

### 4.3 Join codes
Alphabet excludes I, L, O, U, 0, 1 so codes survive being read off a whiteboard.
The join endpoint **refuses** a code containing any of them rather than folding
it onto a near neighbour — folding can silently turn one valid code into a
different valid code, putting a child in the wrong class. I wrote the folding
version first and removed it.

End-to-end verified against live data, then the test rows deleted: create →
code `QENSA9` → student joins → typing `"qen sa9"` recognised with **no duplicate
membership row** → teacher sees real aggregation → a different teacher gets 403.

---

## 5. Teacher auth — three faults, all pre-existing

Found by walking the journey rather than reading code.

1. **"Forgot password" had never worked for anyone.** `teacher/login.html` had no
   recovery handling of any kind — no hash parsing, no `PASSWORD_RECOVERY`
   listener, no form. It sent a real email whose link could not work. (`235ee2ad`)
2. **The reset form signed you out of itself.** A recovery token establishes a
   real session, and the page redirected anyone signed in — so the form appeared
   for ~4 seconds and vanished. (`e029bda5`)
3. **No sign-out existed anywhere in the teacher area.** `auth-gate.js` only
   injects it into `.header-nav` or `.admin-nav`; neither the old dashboard nor
   the new page had one. Added `/teacher/login?signout=1` as a route that works
   regardless of what any page renders. (`fb1336c6`)

**Tom also had to change two Supabase settings** I could not: the redirect
allow-list, and the Site URL, which pointed at `study-vault-alpha.vercel.app`.
That second one matters beyond cosmetics — sessions are per-origin, so a reset
completed on the Vercel domain leaves you logged out on the real one.

---

## 6. Consolidation, and the privacy story for uploads

- **One teacher screen** (`3b55a1b9`): class dropdown, roll, join code and create
  flow in a single bar; picking a class drives everything below. Restyled onto
  the tokens `welcome.html` actually ships. `/teacher/dashboard` now serves it.
- **Teacher shell** (`de0d50b9`, `827a36eb`): `js/teacher-shell.js` +
  `css/teacher-shell.css` make the shared admin pages wear the teacher platform's
  clothes when the signed-in person is a teacher. Deliberately **not**
  `reskin.css`, which breaks these table layouts. `.admin-nav` is reused rather
  than replaced because `auth-gate` injects Sign out into that class name.
  Verified in both roles — admin console unchanged.
- **Source material is forgotten on publish** (`48e4cd0d`): uploaded resources
  were already parsed in the *browser* (files never leave the school's machine,
  only text is posted) but that text was kept for ever.
  `api/pipeline/_lib/forget-source.js` clears it when the whole subject goes
  live — publish rather than build-complete, because the gap between those is
  where re-runs happen. **Backlog cleared with Tom's explicit approval: 32,332,632
  characters across 36 jobs**, job rows kept so the audit trail survives.
  Independently re-read afterwards: 0 jobs holding text, 4,914 lessons untouched.

---

## 7. `docs/PRACTICE_BUILD_MASTER_PLAN.md` — planning only, no code

Tom asked what it would take to make the build pipeline produce practice-format
lessons. **I wrote it too fast the first time and he called it** — I had proposed
modifying a 1,285-line driver I had only grepped, and asserted the renderer
"handles every type" without opening the file. Rewritten after actually reading
`driver.py`, `practice.html`, the schema docs and the QA record.

Findings a reviewer can check:

- `driver.py` is 18 stages on the Batch API, one request per lesson, resumable,
  with agents barred from touching Supabase. It is **article-only by design** —
  hardcodes `"practice_units": []` and treats a practice unit as drift.
- **Both artefacts the pipeline doc calls canonical have never existed in git:**
  `scripts/factory/` and `scripts/_qa_practice_data.py`. `git log --all` returns
  nothing for either path.
- `_validate_content_json.py` is article-only, yet the driver gates every lesson
  through it.
- Verified: all 22 live input types **are** handled in `practice.html`.
  `ENGLISH_INPUT_TYPES` also contains the MFL types — it is really
  "non-quantitative", mislabelled.
- **977 practice lessons, 19,215 problems, 6 lessons ever reviewed (0.6%), 18
  flags on those 6.**
- Cost basis $0.48/lesson article, from the Console; the driver's own meter reads
  ~2× high (open bug). Memory and code disagree about the 1h cache pre-warm.

**Conclusion, which changed between drafts:** build the missing *validator*
first, not the generator. It is pure Python, pays back across 19,215 existing
problems, and is the acceptance test for anything generated later.

---

## 8. Known weaknesses — where I would look hardest

1. **No staging environment.** Every change was verified against production.
   Several were bulk writes.
2. **The 3.0 defects/lesson figure is not a clean estimate.** Those 6 lessons
   were almost certainly chosen because they looked suspect. I say so in the plan
   but the number is quotable and could mislead.
3. **`teacher/classes.html` is 700 lines of inline script.** It works and is
   render-tested, but it is not modular and has no automated tests.
4. **I broke that page during the session** — a script inserted JS referencing an
   element whose markup had silently failed to insert, and reported success
   because I had dropped the assertion I used on every other edit. Caught by a
   render, not by a check.
5. **The teacher shell restyles admin pages by CSS override.** Scoped to
   `body[data-staff="teacher"]`, but it is a reskin over markup it does not own,
   and future admin changes can slip out from under it.
6. **`/teacher/upload` re-shelled but not walked as a teacher.** I do not know
   whether its flow offers things only Tom should see.
7. **The editor was given the shell but its editing experience is unwalked** —
   block types may exist that make no sense for a teacher.
8. **Music practice content is Tom's to verify by ear** and was excluded from all
   automated checking.
9. **Several fixes were verified by DOM inspection where a screenshot would have
   been better** — this page freezes Chrome's screenshot under CDP, so I used
   Playwright, but coverage is not uniform.

---

## 9. Things I got wrong during the session, and corrected

Listed because a reviewer should weight my other claims accordingly.

| Claim | Reality |
|---|---|
| "The other AI routes fail open" | They do not once Bedrock is configured. Production was always London. |
| "17 jobs holding retained text" | 17 rows matched `not null`; several held an empty string. The 32.3M character total was right, the row count overstated. |
| `quizAccuracy` assumed `{correct, total}` | Real shape `{d, s, t, miss[]}`. Every student returned null. |
| Assumed Tom's EngLit assignment was stale | It is correct — both his subjects are Unity bespoke. |
| First plan draft | Written without reading the driver it proposed to modify. |
| A char-folding routine in `join.js` | Could map one valid code to a different valid code. Removed before shipping. |
| Told Tom a file path that did not exist on his branch | The SQL was committed to `platform`; I had restored him to another branch. |

---

## 10. Commit list

```
00063651  Rewrite the practice plan after actually reading the code
aa67c14d  Plan: what it would take to make the pipeline build practice lessons
827a36eb  Build flow: re-shelled, and the plan can finally say "practice"
de0d50b9  Teacher shell: the shared admin pages, wearing the teacher platform's clothes
48e4cd0d  Forget a department's source material once their lessons go live
da4afe79  Review queue: scope the LESSONS, not just the dropdown
4307ac6d  Close the last two ways pupil work could leave the UK unannounced
2283265c  Parents' evening packs and the AI summary, on real data
3b55a1b9  Consolidate the teacher area into one screen, in the site's own design
fb1336c6  Give teachers a way out: sign-out, and a sign-in page you can reach
e029bda5  Password reset: stop the page signing you out of its own reset form
235ee2ad  Password reset: build the half of the flow that never existed
c8a02944  Classes page: stop rendering a signed-in page that can fetch nothing
3074a5f3  Merge branch 'score-reading-rebuild' into platform
7c36ad0d  Teacher classes screen: make a class, read the code out, see the misconceptions
e0118b1a  Class join codes: the department tier, without waiting for IT
326dfc97  Teacher class progress: attainment, scoped to the subject they teach
72374f50  CLAUDE.md: school codes are retired, say so where I keep reading it
3eb9a4b3  Catalogue: planner solved — two slug faults, one hidden behind the other
a2fc67b9  Catalogue: planner still empty after the cohort and slug fixes (F5)
```

## 11. Manual actions Tom performed

- Ran `scripts/_create_class_join_codes.sql` in the Supabase SQL editor
  (result: 103 classes, 103 codes, 103 distinct — verified independently).
- Changed the Supabase Auth **Site URL** and **redirect allow-list**.
- Approved the 32.3M-character source-text deletion.
- Approved pushing to `origin/platform`.

## 12. Non-code changes

Memory files written or updated: `feedback_teacher_data_boundary`,
`feedback_scope_the_data_not_the_control` (new),
`project_item_analysis_already_captured` (new),
`project_parents_evening_pack` (new), plus `MEMORY.md` index lines.

Content change to live Supabase: one English Literature AQA knowledge-check and
flashcard (Romeo and Juliet L8, Tybalt).
