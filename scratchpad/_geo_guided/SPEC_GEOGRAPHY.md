# Guided-Learning Fan-Out — Geography Skills (12 lessons)

You are converting one Geography Skills practice lesson to the guided-learning
format already shipped across all 192 maths lessons and 60 science calculation
lessons. Tom (the owner) approved that shape after doing the lessons himself.

**Your lesson row is shared by SIX subjects**: `geography-aqa`,
`geography-edexcel-a`, `geography-edexcel-b`, `geography-ocr`,
`geography-eduqas`, and Unity's `geography`. You edit ONE canonical row; a
propagation step copies it to the other five. So write board-neutral content:
never name an exam board, never cite a board-specific mark tariff.
Real GCSE students will do your steps.

## What makes Geography Skills different from maths

In maths the figure supports the question. **Here the map, chart or graph IS
the question.** The skill being taught is *reading a stimulus*, not arithmetic.
Everything below follows from that.

Three consequences you must honour:

1. **The stimulus is sacred.** If a problem carries an `image` or `chart`, it
   stays, byte-for-byte, unless it is factually wrong. Never drop one, never
   swap one, never invent a URL. There are 23 real OS map and thematic map
   images on R2 and 57 Chart.js configs; you may reuse an existing image URL
   from your own lesson, but you may not fabricate a new one.
2. **Every walk begins by LOCATING, not reading.** The first box of a
   map/chart walk orients the student on the stimulus ("How many squares
   across from the left edge is the church?"), and only then reads a value.
   A walk that jumps straight to arithmetic teaches arithmetic, not geography.
   This is the single most important instruction in this document.
3. **Never claim a figure you do not carry.** If the display says "the map
   shows" / "from the graph", the problem must have `image` or `chart`. Three
   problems site-wide currently overstate this (L02 gold[4], L03 gold[3],
   L06 gold[3]) — they describe their data in words, which is fine; just make
   sure the wording does not promise a picture.

## The pedagogical model (why each piece exists)

Skills are learned by DOING tiny steps with instant feedback, not by reading
prose. The flow is a ladder that removes one layer of help at a time:

1. **Opener** (`guided.opener`): a concrete puzzle the student solves by
   common sense BEFORE any formal method. The reveal then names what they just
   did as the technique. Geography has excellent hooks; see section 5.
2. **Teach walks** (`guided.teach.{bronze,silver,gold}`): one worked problem
   per tier, done as micro-steps the student types. Each tier's walk shows the
   ONE new move that tier adds.
3. **Completion problem**: the player deals each tier's first bank question
   half-worked (everything before the first `phase:"substitute"` step arrives
   pre-filled and ticked; the student finishes). You set the boundary.
4. **Bare questions with a lifeline**: every bank problem's `guided_steps`
   power a "Stuck? Do this one with me" walk, before AND after a wrong answer.
5. **Honest diagnosis**: a misconception message only ever shows when the
   student's answer equals that error's `expect`. Never guess.

## Reference materials

- **Exemplar shape (copy this structure):**
  `scratchpad\_maths_audit\_l09_rebuilt_practice_data.json`
- **Its walks in readable form:** `scratchpad\_maths_audit\_l09_guided_transcripts.txt`
- **Pre-run state of all 72 geography rows (diff + rollback):**
  `scratchpad\_geo_audit\_pre_dump_all.json`
- **Your work-list entry (lesson id, key, title):**
  `scratchpad\_geo_guided\_worklist.json`

## Data access

Supabase REST, service key in env `SUPABASE_SERVICE_KEY`:
- GET  `https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.<ID>&select=practice_data`
- PATCH same URL, body `{"practice_data": <full object>}`, headers `apikey`,
  `Authorization: Bearer`, `Content-Type: application/json`,
  `Prefer: return=minimal`.

Fetch FRESH before you start (the pre-dump is for diffing only).
**PATCH only the `practice_data` column, only your ONE assigned row id. Never
another row, never another column. Do not git commit anything.**

Write Python scripts to files and run them. Never pass content with
backslashes through a bash heredoc; it corrupts escapes.

## Per-lesson procedure

### 1. Verify and repair the bank (correctness first)

- Answer EVERY problem yourself from its display and its stimulus. Compare
  with stored `solutions`.
- For problems with an `image`: you cannot see the map. Do **not** guess and
  do **not** "correct" a stored answer you cannot independently verify.
  Instead: trust the stored answer, and if the question is ambiguous or the
  stored answer looks impossible (e.g. a 4-figure grid reference with 5
  digits, a bearing over 360, a negative distance), record it in your changes
  file under `flagged_unverifiable` and leave the value alone. Never invent
  map facts.
- For problems whose data is fully in the display text (L01–L07, L10) or in a
  `chart` config: fresh-solve exactly. Fix wrong stored answers with the
  MINIMAL edit that yields a clean answer. Re-solve after every edit.
- Keep tier sizes (bronze 8, silver 7, gold 5) and input types unless a
  problem is genuinely mis-posed.

### 2. Misconceptions (honest diagnosis) — the biggest single repair

The current bank has **292 catch-all misconceptions** with `check: "wrong"`,
which fire on ANY wrong answer. That is exactly the bug Tom hit in maths:
students get told they made a mistake they did not make. Worse, many messages
**state the correct answer outright** (L11 bronze[0] says "They are both in
grid square 8332" — that is the answer).

Rules:
- Every misconception gets `pattern`, `message`, `expect`, optional `note`.
- **Delete `check: "wrong"` entirely.** It is replaced by `expect` matching.
- `expect` = the exact wrong answer that error produces for THIS problem,
  derived by actually committing the error. If the error has no single
  determinate wrong answer, set `expect: null` (it simply never fires).
- **A message must never state the correct answer**, in any form. Name the
  error, point at the method move, and stop. The validator fails any message
  containing the solution.
- 0–3 per problem, only real derivable ones. Do not force them.

Geography gives you unusually clean determinate errors — use them:
| Error | Determinate wrong answer |
|---|---|
| Northing before easting in a grid reference | the digit pairs swapped |
| 4-figure answer given where 6-figure asked (or vice versa) | truncated/padded reference |
| Reading the wrong axis on a bar/line graph | the other axis's value |
| Frequency instead of frequency density (histogram) | the raw frequency |
| Percentage change over the NEW value not the original | the recomputed percentage |
| Counting grid squares instead of measuring along the line | the square count |
| Bearing measured anticlockwise, or from the wrong north | 360 − answer |
| Median taken without sorting first | the middle of the unsorted list |
| Using range where IQR asked | max − min |

For `input_type: multiple_choice`, `expect` is the **index** of the distractor
that error leads to.

### 3. Hints and tier descriptions

- `hint` per problem: ONE plain-text sentence pointing at the method move
  ("Read the easting off the bottom edge first, then the northing up the
  side."). Plain text only: no LaTeX, no HTML.
- **`problem_bank.{tier}_description` does not currently exist in geography —
  you must add all three.** One plain line defining what that rung demands in
  this topic. These show on every question card.

### 4. tier_guides (the current rung's reference card)

For each tier: `{title, steps, example}`.
- `title`: "Bronze: <what this rung is>" (colon, never a dash).
- `steps`: 2–4 strings, total ≤ 115 words, GCSE-plain language,
  `<strong>` allowed.
- `example`: `{question, steps:[{label, content}]}` — one stepped example at
  that tier's difficulty, ending with an answer step (`isAnswer: true,
  is_answer: true`) and a check step before it.

### 5. guided.opener (the concrete hook) — the creative heart

Quality bar: a student who has NEVER met the topic can answer the first box by
pure common sense, and the reveal honestly names what they just did as the
technique. It must be concrete, not "a simpler version of the same question".
2–3 boxes max, then a say-only reveal step.

Suggested hooks (improve on these if you can):

| Lesson | Hook |
|---|---|
| L01 Bar & line graphs | two bars side by side, which is taller and by how much |
| L02 Pie charts & histograms | a pizza cut into quarters; half the class had chips |
| L03 Scatter & correlation | taller people have bigger feet, spot the odd one out |
| L04 Population pyramids | two shapes: which country has more children |
| L05 Mean, median, mode | pocket money where one friend gets £100 |
| L06 Quartiles & IQR | splitting a queue of 8 people into four equal groups |
| L07 Percentage change | a £20 hoodie now costs £25 |
| L08 Choropleth & isoline | darker shading means more, like a heat map on a phone |
| L09 Proportional symbols & flow lines | bigger circle = bigger city; thicker arrow = more people |
| L10 Fieldwork & sampling | picking 10 people to represent the whole school fairly |
| L11 Grid references | telling a friend where you parked: row then number |
| L12 Distance & direction | 2 cm on the map is 1 km, so 6 cm is how far |

**Show what you say (Tom's rule).** If any student-facing text claims a figure
("here are two bars", "look at this shape"), the display MUST contain it:
inline SVG is allowed and encouraged (self-contained, < 2 KB, `role="img"` +
`aria-label`, soft fills, no external references), or unicode art for simple
grids. If you cannot draw it, reword to pure imagination ("Picture a pizza cut
into quarters") so nothing is claimed that is not shown.

### 6. guided.teach walks (one per tier)

- A problem NOT in the bank, at that tier's difficulty, in micro-steps.
- Demonstrates that tier's ONE new move explicitly.
- ≥ 4 boxes each; every box numeric; `done` notes where they teach.
- If the teach walk needs a stimulus, either reuse an existing `image` URL
  from this lesson (correctly described) or draw an inline SVG. Do not
  invent URLs.

### 7. guided_steps on every bank problem

- Micro-steps for the FULL solve of that exact problem. Shapes:
  - say-only step: `{say}`
  - box step: `{pre, post?, answer, hint, done?, say?, phase?}`
- **First box locates on the stimulus** (see "What makes Geography different").
- `answer` MUST be a plain number. Design boxes so the typed thing is always
  numeric: counts, readings, values, totals, grid digits, bearings.
- `pre`/`post` are PLAIN TEXT. `say` may use `<strong>`.
- Wrong answers: first wrong shows your `hint`, second reveals and moves on.
  Write hints that unstick, not scold.
- **Completion boundary**: tag the step where the finishing phase begins with
  `"phase": "substitute"` (fixed tag name; means "second half starts here").
  Rule of thumb: locating and set-up are pre-worked; the student does the
  reading-through, the calculation and the check. ≥ 1 step before the
  boundary, ≥ 2 live boxes at/after it.
- End every walk with a CHECK step that verifies the answer against the
  original question, with a `done` note saying why it must be right.
- **Multiple choice**: 98 of 240 problems are MC. Where the correct option is
  reachable by a procedure (reading a value, a calculation, a comparison), MC
  problems **do** get `guided_steps` — the boxes work the numbers and the
  final say-step names the option. Only genuinely evaluative MC ("explain why
  random sampling might be impractical") may omit them, and then you must set
  `guided_skip_reason`.
- VERIFY every box value by computing it independently after writing the walk.
  Final boxes must land exactly on the stored `solutions`.

### 8. method_card (slim reference only)

Trim to: title, ≤ 4 short steps, content ≤ 140 words, one compact example.
The teaching now lives in the walks; this is the Learn-view reference.

### 9. Keep everything else

`related_videos`, `topic_links`, `worked_examples`, `image`, `chart`, `ruler`,
`options`, and anything else in practice_data: preserve byte-for-byte unless
this spec names it. You are ADDING `tier_guides` / `guided` / `guided_steps` /
`hint` / `{tier}_description` / `expect` and repairing content, not rebuilding
the object.

## Style rules (hard)

- **NO EM DASHES anywhere student-facing.** Use commas, colons, brackets or
  full stops. (Internal `note` / `guided_skip_reason` exempt.) The existing
  MC `options` contain several; rewrite them. The validator enforces this.
- Plain unicode (×, ÷, −, £, →, °) not HTML entities.
- GCSE reading age (15–16), warm but not chatty. Every box earns its place.
- British English. Money in £. Distances in km/m. Bearings in degrees, three
  figures (e.g. 045°).
- Board-neutral: never name an exam board or a mark tariff.

## Ship gate (in this order)

1. Write the finished practice_data to
   `scratchpad\_geo_guided\lesson_<KEY>.json`
2. Run the validator until it passes:
   `python scratchpad\_geo_guided\_validate_geo.py <that file>`
3. PATCH the live canonical row with the file's contents.
4. Write `scratchpad\_geo_guided\changes_<KEY>.json`:
   `{"key", "problems_fixed":[{tier,index,what,old,new}], "misconceptions_rewritten": n,
     "flagged_unverifiable":[...], "opener_concept":"...", "notes":"..."}`

---

# CHECKER BRIEF (independent verification agent)

You are checking a lesson someone else converted. Be adversarial: on the maths
fan-out the verification layer wrongly cleared 2 real errors, and checkers
caught 14 defective lessons across the boards. Do not rubber-stamp. Fetch the
LIVE row (GET above). Then:

1. **Answers**: fresh-solve every problem whose data is in the display or
   chart. Stored solutions must match exactly. For image-based problems you
   cannot verify the map: check only internal consistency (a 4-figure
   reference has 4 digits, a bearing is 0–360, a distance is positive) and
   confirm the author did not silently change a stored answer they could not
   verify. Silently changed image-based answers are a FAIL.
2. **Every box**: recompute every `guided_steps` / `teach` / `opener` box
   value independently. The walk must be continuous (each step follows from
   the last) and land on the stored solutions.
3. **Locating step**: does each map/chart walk's FIRST box orient the student
   on the stimulus rather than jumping to arithmetic? Flag every walk that
   does not.
4. **Expects**: commit each misconception's described error yourself; your
   wrong answer must equal `expect` (or expect must be null). Any surviving
   `check: "wrong"` is a FAIL.
5. **No answer leakage**: no misconception message, hint, or tier description
   may state the correct answer.
6. **Completion boundary**: the pre-worked half must genuinely be locating and
   set-up; the live half must be a meaningful finish (≥ 2 boxes).
7. **Opener**: could a student who has never met this topic answer box 1 by
   common sense? Does the reveal honestly name the technique? If it claims a
   figure, is the figure actually there?
8. **Stimulus preservation**: compare against the pre-dump entry for this
   lesson. Every `image`, `chart` and `ruler` present before must be present
   now and unchanged. Any invented image URL is an immediate FAIL.
9. **Preservation**: `related_videos`, `topic_links`, `worked_examples` and
   other untouched fields unchanged (except a legitimately slimmed
   `method_card`).
10. **Style**: no em dashes student-facing (including inside `options`); hints
    plain text; numeric-only boxes; tier guides within budget; board-neutral.
11. Run the validator yourself on the live data.

Report every defect with its exact path (e.g. `silver[3].guided_steps[4]`).
FAIL on: any wrong answer, any box that does not compute, any expect that does
not reproduce, any dropped or invented stimulus, any answer leakage, any
surviving `check:"wrong"`. Style nits alone with correct content: pass=true
but list them in findings.
