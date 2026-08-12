# Practice Build — Master Plan

**Status:** proposal. Nothing here has been built.
**Written:** 12–13 August 2026.
**Question asked:** the build pipeline predates practice-format lessons. What would
it take to make it build them?

**Short answer:** less than expected, and in a different order than expected. The
schema, the renderer and the reference lessons are all in good shape. What is
missing is not generation — it is *verification*, and that changes what to build
first.

---

## 1. The three findings that shape everything below

**1. There is no practice pipeline, and the two artefacts the documentation
calls canonical have never existed in git.**
`docs/PRACTICE_PIPELINE.md` names `scripts/factory/` as the home of the stage
orchestration and prompt templates, and `scripts/_qa_practice_data.py` as the
validation gate. Neither is in the repository and neither is in history —
`git log --all` returns nothing for either path. `scripts/factory/` on disk holds
only `_passage_audio/` and `voice_samples/`. So the factory that produced 608
English Language problems, and the QA script that was supposed to gate every
practice lesson, are both unrecoverable. Every other family survived properly
(music-practice 40/40 `.py` tracked, language-practice 3/3, science-practice 2/2).

**2. The newest build machinery refuses practice by design.**
`scripts/api_build/driver.py` (1,285 lines, 18 stages, Anthropic Batch API) is
the driver behind D&T Edexcel and both Psychology arms. It hardcodes
`"practice_units": []`, iterates `plan["article_units"]` only, and its plan
checker treats a practice unit as drift: `"unexpected practice_units for an
article subject"`.

**3. The corpus is large and almost entirely unverified.**

| | |
|---|---|
| Practice lessons live | **977** |
| Problems authored | **19,215** |
| Lessons ever QA-reviewed | **6** (0.6%) |
| Flags raised on those 6 | **18 — 3.0 per lesson** |

The generator is gone, the gate was never built, and 99.4% of the corpus has
never been looked at. Building more practice content before building the gate
multiplies an unverified corpus using a process nobody can inspect.

*Honest caveat:* those 6 lessons were almost certainly chosen because they looked
suspect, so 3.0 defects/lesson is not a clean population estimate. It is,
however, the only evidence that exists, and it points one way.

---

## 2. What is actually in good shape

This is not a rescue job. Four things are solid and should not be touched.

### 2.1 The schema generalises

Every practice lesson stores one `practice_data` envelope. Blocks observed
across seven families:

| Block | Maths | EngLang | MFL | Science | Geog | Music | Stats |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `method_card` | ● | ● | ● | ● | ● | ● | ● |
| `problem_bank` | ● | ● | ● | ● | ● | ● | ● |
| `worked_examples` | ● | ● | ● | ● | ● | ● | ● |
| `topic_links` | ● | ● | — | ● | ● | — | ● |
| `exam_context` | — | ● | ● | ● | — | ● | ● |
| `tier_guides` | ● | — | — | ● | ● | — | ● |
| `guided` | ● | — | — | ● | ● | — | ● |
| `passages` | — | ● | — | — | — | ● | — |
| `ai_marking_prompts` | — | ● | ● | — | — | — | — |
| `related_videos` | ● | — | — | ● | ● | — | — |

`problem_bank` is keyed `bronze` / `silver` / `gold` (+ `*_description`) in
**every** family without exception.

### 2.2 Music proved the envelope stretches without changing

Music score-reading and listening — built 10–11 August, the most exotic subject
on the platform — use `passages` `{id, text, label}` with problems carrying
`passage_id`, the same mechanism English Language uses for reading extracts.
Inline SVG notation and audio players live inside the passage `text`. **No new
schema. No new input types.** A subject nobody designed for fitted the format
unmodified. That is the strongest evidence that this is a build problem, not a
design problem.

### 2.3 The renderer already handles everything (verified, not assumed)

Rendering lives in `practice.html` (not `practice-loader.js`), dispatching on
`input_type`. I cross-checked all 22 types present in live data against the
branches in that file: **every live type is handled, with none orphaned.**

One wart worth knowing before touching it: the array named
`ENGLISH_INPUT_TYPES` also contains all the MFL types — `translate`,
`dictation`, `vocab_match`, `role_play`, `sentence_builder`, `spot_correct`. It
is really "non-quantitative types", mislabelled. Adding a family's types means
editing that array *and* writing a handler; new input types are not free.

### 2.4 The three pinned reference lessons are alive and correct

All three are `live` with exactly 20 problems each:

| Reference | ID | Covers |
|---|---|---|
| EngLang AQA P1 Reading L1 | `83ab6156…` | passage-based, AI-marked prose |
| Spanish AQA Popular Culture L1 | `934d507a…` | MFL, 10 types incl. dictation |
| Maths AQA Graphs L3 | `c8bc060f…` | deterministic calculation shape |

**This is the recovery path.** The factory code is gone, but the specification
survives as three known-good lessons plus the staging rationale in the doc. The
factory can be rebuilt from its output.

---

## 3. Input types, by family and volume

| Type | Families | Notes |
|---|---|---|
| `multiple_choice` | all seven | the universal type |
| `single_value` | Maths, Science, Sep Sci, Geography, Statistics | 65–89% of those families |
| `ai_mark` | English Language, MFL | routes to `/api/ai-mark` |
| `translate`, `gap_fill`, `dictation`, `sentence_builder`, `vocab_match`, `spot_correct`, `role_play` | MFL | `dictation` needs Azure audio |
| `highlight_evidence`, `traffic_light`, `connotation_picker`, `evidence_match`, `misleading_summary`, `improve_sentence`, `spot_error` | English Language | the diverse family |
| `fraction`, `two_solutions` | Maths, Statistics | |
| `standard_form` | Maths, Science, Sep Sci | |
| `xy_pair` | Maths only | |
| `reorder` | English Language, MFL, Music | |

Volumes: Maths 953, English Language 608, MFL 520 each, Separate Sciences 420,
Statistics 370, Science 300, Geography 280, Music 228.

Statistics is confirmed as Maths with a different mix (`single_value` 207,
`multiple_choice` 127, `fraction` 25, `two_solutions` 11) — no unique types, so
it comes nearly free once Maths is done. The so-called "Maths types" are really
*quantitative* types and the registry should say so.

---

## 4. How `driver.py` actually works

Necessary detail, because the recommendation is to extend it rather than replace
it. I had not read this properly when I first drafted this plan, and it changes
the shape of the work.

**18 stages, resumable, on the Batch API:**

```
plan → plancheck → activate → prep → submit → poll → fix → pollfix
     → factcheck → pollfactcheck → applyfixes → pollapplyfixes
     → media → pollmedia → insertmedia → guides → pollguides → insert
```

Key mechanics:

- **One batch request per lesson.** `custom_id` = `unit_slug` + lesson number.
  `max_tokens: 32000` — a comment records that 16,000 truncated 23 of 31
  lessons, because Sonnet 5's adaptive thinking bills against `max_tokens`
  (~10–14k/lesson observed on top of a 4–8k lesson JSON).
- **Structured outputs** via `LESSON_SCHEMA`, plus the external validator, gate
  every lesson.
- **Resumable** per stage via `state.json`; batch collection is idempotent after
  a double-ledger bug.
- **The driver holds all Supabase keys; agents are single-shot and never touch
  the database.** A safety rule adopted after the mojibake incident. Any practice
  path must keep it.

**A cost discrepancy worth resolving before spending anything.**
`memory/project_api_build_calibration.md` says the 1-hour cache pre-warm before
each batch "earns its keep; keep it". The code comment in `stage_prep` says the
opposite and strips cache markers from batched requests, because batch requests
run in parallel so hits land ~5% in practice (measured on the D&T arm: 1 read
per 22 requests), and below ~53% a 1h marker *loses* money — about $1.93, +48%
on that stage. The code is newer than the memory. Practice will have a much
larger shared prefix per unit (method card, passages, tier definitions), so this
is worth re-measuring rather than inheriting either answer.

**Cost basis for estimating practice:** article content settled at **$0.48 per
lesson** (Psychology, 69 lessons across two boards, $32.99 on the Console;
~£11–12 for a clean 30-lesson subject). Note the driver's internal meter reads
about 2× high — an open formula bug — so **quote from the Console, not from
`driver.py costs`.**

---

## 5. Where the gap is, precisely

| Layer | State |
|---|---|
| `practice.html` renderer | **Fine.** All 22 live types handled. Verified. |
| `practice_data` schema | **Fine.** Proven across seven families incl. Music. |
| Pinned reference lessons | **Fine.** All three live, 20 problems each. |
| `api/pipeline/approve-plan.js` | **Fixed 12 Aug** — reads `article_units` + `practice_units`, returns `practice_units` for `subjects.settings`. |
| `scripts/api_build/driver.py` | Article-only by design. Rejects practice plans. |
| Generation stages | **Never existed in git.** `scripts/factory/` unrecoverable. |
| Validation gate | **Never existed in git.** `scripts/_qa_practice_data.py` unrecoverable. |
| `_validate_content_json.py` | **Article-only.** Knows `practice_questions`, `knowledge_checks`, `flashcard_questions`. No concept of `problem_bank`, `input_type` or `solutions` — yet the driver gates every lesson through it. |
| Practice QA | **Human only.** `/admin/practice-qa` writing to `practice_qa_flags`. 0.6% coverage. |
| Web pipeline generation | Does not exist. upload → parse → plan → approve, then nothing. |
| `docs/PRACTICE_PIPELINE.md` | Stale (15 May). Points at both missing artefacts. Music absent from the registry. |

---

## 6. What the human QA actually caught

The 18 flags are the best available specification for an automated gate, because
they are real defects a teacher found in shipped content:

| Defect | Example | Catchable by schema check? |
|---|---|---|
| Problem with no question | *"No question prompt — display only says 'The dual bar chart shows sales for two shops'"* | **Yes** |
| Question/display mismatch | *"the question says find the missing frequency f, but there is no mention of f in the table"* | Partly |
| Serialisation bug in the answer | *"it claims the expected answer is: [object Object]"* | **Yes** |
| **Wrong answer key** | *"Is the median not between 23 and 27? So the answer should be 25?"* | **No — needs independent computation** |
| Visual failure | *"the circles get huge and overlap"* | No — needs rendering |

Roughly half are structural and catchable for free in Python. The wrong answer
key is the one that matters most pedagogically — it tells a correct student they
are wrong — and it needs a different technique entirely.

---

## 7. Recommendation

### Phase 0 — Build the missing validator FIRST *(new; this is the change of order)*

Write `scripts/_qa_practice_data.py` as documented but never built. Pure Python,
no model calls, runs over all 977 existing lessons in minutes:

- 20 problems per lesson, tier distribution 7–8 / 6 / 5–6
- every problem has the fields its `input_type` requires
- `solutions` is the right *type* (numeric vs array-of-indices) and is not an
  object stringified into `[object Object]`
- non-empty `question` on every problem
- `bronze_description` / `silver_description` / `gold_description` present
- no exam-board level descriptors, no spec codes
- `ai_marking_prompts` reference `/api/ai-mark` tier routing correctly
- options not prefixed `"A. "` (the renderer adds letter badges; prefixing
  double-renders)

**Why first:** it is the cheapest thing on this list, it pays back immediately
across 19,215 existing problems, and it is the acceptance test for anything
generated later. Building the generator first means having no way to tell whether
its output is good.

### Phase 1 — Independent answer verification for deterministic types

`single_value`, `fraction`, `two_solutions`, `standard_form` and `xy_pair` are
89% of quantitative problems and are *machine-checkable*. Re-derive the answer
with sympy from the problem statement and compare with the stored key; disagreement
is a flag, not a failure. This is the only thing that catches "the answer should
be 25", and it is exactly the class of error most damaging to a student's trust.

Non-deterministic types (`ai_mark`, prose) cannot be checked this way and should
be sampled by a model against the mark scheme instead.

### Phase 2 — Teach `driver.py` about formats

Make units format-aware through `stage_plan`, `stage_plancheck` and
`stage_activate`; stop treating `practice_units` as drift; write
`settings.practice_units` on activation. No generation yet — just let an honest
practice plan survive the pipeline. Extend `_validate_content_json.py` or branch
to the new practice validator depending on unit format.

### Phase 3 — Generation, staged, Science first

Adopt the eight stages from `PRACTICE_PIPELINE.md`. The rationale is sound and
worth quoting verbatim:

> one agent producing a whole lesson's 20 problems thins toward the end (silver
> and gold are worse than bronze)

Two amendments from the data:

- **`guided` needs its own stage.** Maths and Science carry step scaffolds
  (`guided_steps: [{say, pre, hint, answer}]`) inside problems. They are the
  most valuable and most error-prone part; folding them into the bronze stage is
  precisely the thinning the staging exists to prevent.
- **Tier descriptions are part of the bank**, produced with it, not after.

On the Batch API this means ~8 batches per unit rather than 1 per subject. Each
stage is a submit/poll pair, so the existing `stage_submit` / `collect_batch`
machinery is reusable but the stage list roughly doubles.

**Family order — by difficulty, not demand, because each earns the next:**

1. **Science calculation units** — 3 types, 89% one type, existing schema doc,
   deterministic answers fully covered by Phase 1. The canary.
2. **Maths / Statistics** — 6 types, adds `guided_steps`, KaTeX, Chart.js.
3. **Geography Skills** — 2 types but custom panels (charts, OS maps, ruler).
4. **MFL** — 10 types, AI marking, plus Azure dictation audio (already automated:
   `generate_dictation_audio.py` → Azure → R2 → `audio_url`).
5. **English Language** — 11 types, narrated passages, AI marking and AI writing.
   Last: both the most complex *and* the only family with no surviving
   implementation to copy.

**Music stays artisanal, deliberately.** Its value is curated public-domain audio
and hand-checked notation. A generic factory would produce worse music lessons
than Tom does by hand. Recording that as a decision beats rediscovering it.

### Canary before fleet

Build **one Science calculation unit for one board**, read the Console delta for
that single stage — which also closes the open ledger-vs-Console formula bug —
and only then decide the rest. Practice is ~8 model calls per lesson against
article's 1; assume nothing about the multiple until it is measured.

---

## 8. What this does NOT need

- **No renderer changes** for existing types. Verified.
- **No schema migration.** The envelope is right.
- **No new database columns.** `practice_data` and `settings.practice_units` suffice.
- **No rebuild of existing content** — though Phase 0 will tell us, for the first
  time, whether that is true.

---

## 9. Decisions only Tom can make

1. **Do departments get practice builds at all?** Article is one model call per
   lesson; practice is roughly eight across 20 problems and three tiers. At
   $0.48/lesson for article, a 48-lesson practice subject is a materially
   different number from a 40-lesson article one. It may be right to offer
   departments article builds and keep practice in-house.

2. **What does Phase 0 do if it finds a lot?** If the validator flags a
   meaningful share of 977 lessons, that is a remediation programme competing
   with new subjects for the same time. Worth deciding the appetite *before*
   running it, so the result informs rather than ambushes.

3. **Does `PRACTICE_PIPELINE.md` become the spec or get rewritten?** It is three
   months old and points at two files that never existed. Recommend keeping the
   staging rationale and reference-lesson mapping — both still correct — and
   rewriting the runbook sections around what actually shipped, including Music.

---

## 10. Suggested first three days

| Day | Work |
|---|---|
| 1 | Write `scripts/_qa_practice_data.py` (Phase 0). Run it over all 977 lessons. Read the result before planning anything else — it may reorder this list. |
| 2 | Refresh `PRACTICE_PIPELINE.md` against reality: add Music, add `guided`/`tier_guides`, fix the two dead references, document the tiered bank properly, note the `ENGLISH_INPUT_TYPES` misnomer. |
| 3 | `driver.py` format awareness through plan → plancheck → activate, and branch the validator by unit format. Still no generation. |

Phase 1 (sympy answer-checking) slots in as soon as Phase 0's output shows which
types are worst affected.

---

## 11. Loose ends I could not close

- **Why was `scripts/factory/` never committed?** Something kept it out. Worth a
  `.gitignore` check before recreating anything there, or the same thing happens
  again.
- **The cache pre-warm question** (§4) needs one measured answer, not two
  contradictory ones.
- **The ledger's 2× overread** is still open. The canary run is the natural place
  to close it: one stage, Console before and after, reconcile that delta.
