# Guided-Learning Fan-Out — Maths Edexcel (47 lessons)

You are converting one maths practice lesson to the guided-learning format
piloted on algebra L09 (Simultaneous Equations). Tom (the owner) approved that
pilot's exact shape after testing it himself. Your job is to reproduce the
shape for your assigned lesson with the same care. **Both the free tier and
paying schools serve these exact rows.** Real GCSE students will do your steps.

## The pedagogical model (why each piece exists)

Maths is learned by DOING tiny steps with instant feedback, not by reading
prose. The lesson flow is a ladder that removes one layer of help at a time:

1. **Opener** (`guided.opener`): a concrete puzzle the student can solve by
   common sense IN THEIR HEAD before any formal method. The reveal then names
   what they just did as the method. (L09: "2 coffees + 1 muffin = £7; 1 coffee
   + 1 muffin = £4. A coffee costs £__?" Answering it IS elimination.) Then the
   player offers two doors: walk me through one / jump straight in.
2. **Teach walks** (`guided.teach.{bronze,silver,gold}`): one worked problem
   per tier done as micro-steps the student types. Each tier's walk shows the
   ONE new move that tier adds.
3. **Completion problem**: the player automatically deals each tier's first
   bank question half-worked (everything before the first `phase:"substitute"`
   step arrives pre-filled and ticked; the student finishes). You control the
   boundary via the phase tag.
4. **Bare questions with a lifeline**: every bank problem's `guided_steps`
   power a "Stuck? Do this one with me" walk, available before AND after a
   wrong answer.
5. **Honest diagnosis**: a misconception message only ever shows when the
   student's answer equals that error's `expect` value. Never guess.

## Reference materials (read these)

- Exemplar (THE shape to copy): `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_audit\_l09_rebuilt_practice_data.json`
- Its walks in human-readable form: `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_audit\_l09_guided_transcripts.txt`
- Audit findings for YOUR lesson (fix all of yours): `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_audit\_audit_result.json`
  (`issues[]` entries and `unconfirmed[]` entries matching your lesson key)
- Pre-run state of all 48 lessons (for diffing and rollback):
  `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_pre_fanout_dump.json`
- Work-list with your lesson id: `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_worklist.json`

## Data access

Supabase REST, service key in env `SUPABASE_SERVICE_KEY`:
- GET  `https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.<ID>&select=practice_data`
- PATCH same URL with body `{"practice_data": <full object>}`, headers
  `apikey`, `Authorization: Bearer`, `Content-Type: application/json`,
  `Prefer: return=minimal`.
Fetch FRESH before you start (the pre-dump is for diffing only).
**PATCH only the `practice_data` column. Never any other column, never any
other row. Do not git commit anything.**

Write Python scripts to files and run them (never pass content with
backslashes through bash heredocs; it corrupts LaTeX).

## Per-lesson procedure

### 1. Verify and repair the bank (correctness first)
- Fresh-solve EVERY problem from its display text yourself, exactly. Compare
  with stored `solutions`.
- Wrong stored answer, impossible/degenerate problem, non-calculator problem
  with messy decimals, duplicate answers within a tier, or a filed audit issue
  for your lesson: fix with the MINIMAL edit that yields a clean answer
  (integers preferred on `calculator:false`). Re-solve after every edit.
- Keep the existing tier sizes and input types unless a filed issue says the
  problem is mis-posed. Keep displays in LaTeX `\(...\)`.
- If your lesson appears in `unconfirmed[]`, treat those problems as SUSPECT:
  the overnight verifiers wrongly cleared at least two real errors elsewhere.
  Re-solve with extra care.

### 2. Misconceptions (honest diagnosis)
- Every misconception keeps/gets: `pattern`, `message`, `expect`, optional
  internal `note`.
- `expect` = the exact wrong answer that error produces for THIS problem,
  derived by actually committing the error. If the error has no single
  determinate wrong answer, set `expect: null` (it will simply never fire).
- Never force misconceptions: 0-3 per problem, only real, derivable ones.
- Rewrite any message containing an em dash (see style rules).
- If you changed a problem's numbers, recompute every expect.

### 3. Hints and tier descriptions
- `hint` per problem: ONE plain-text sentence pointing at the method move
  ("Multiply the second equation by 2, then subtract."). Renders as plain
  text: no LaTeX, no HTML.
- `problem_bank.{tier}_description`: one plain line defining what that rung
  demands IN THIS TOPIC. These show on every question card.

### 4. tier_guides (the current rung's reference card)
For each tier: `{title, steps, example}`.
- `title`: "Bronze: <what this rung is>" (colon, never a dash).
- `steps`: 2-4 strings, total <= 115 words, GCSE-plain language, HTML
  `<strong>` allowed, LaTeX allowed.
- `example`: `{question, steps:[{label, content}]}` one stepped example
  matched to that tier's difficulty, ending with an answer step
  (`isAnswer: true, is_answer: true`) and a check step before it.

### 5. guided.opener (the concrete hook) — the creative heart
Quality bar: a student who has NEVER met the topic can answer the first box
by pure common sense, and the reveal honestly names what they just did as the
method. It must be concrete (money, sweets, journeys, recipes...), not "a
simpler equation". 2-3 boxes max, then a say-only reveal step linking to the
algebra/notation. If your topic truly has no such hook (rare), the opener may
instead be the simplest possible instance of the skill posed as a puzzle, but
try hard first: percentages -> sale prices; ratio -> sharing sweets fairly;
probability -> picking from a visible bag; graphs -> reading a real journey;
area -> tiles/paint; sequences -> spotting the next number pattern children
already do; standard form -> writing the distance to the Moon without zeros.
`display` supports HTML (`<br>`) and plain text; keep it visual.

### 6. guided.teach walks (one per tier)
- A problem NOT in the bank, at that tier's difficulty, walked in micro-steps.
- The walk demonstrates the tier's ONE new move explicitly.
- >= 4 boxes each; every box numeric; `done` notes where they teach ("Gone.
  That was the whole point.").

### 7. guided_steps on every bank problem
- Micro-steps for the FULL solve of that exact problem. Shapes:
  - say-only step: `{say}` (statements flow past without input)
  - box step: `{pre, post?, answer, hint, done?, say?, phase?}`
- `answer` MUST be a plain number (int/float). Design boxes so the thing
  typed is always a number: coefficients ("...= __x" via `post`), values,
  totals. Never ask for expressions or words.
- `pre`/`post` are PLAIN TEXT (no LaTeX; the em dash rule applies). `say`
  fields may use LaTeX `\(...\)` and `<strong>`.
- Wrong answers in the player: first wrong shows your `hint`, second reveals
  and moves on. Write hints that unstick, not scold.
- **Completion boundary**: tag the step where the finishing phase begins with
  `"phase": "substitute"` (the tag name is fixed; semantically it means "the
  second half starts here"). Everything before it gets pre-worked in the
  completion problem. Rule of thumb: the main method move (set-up, transform,
  eliminate, rearrange) is pre-worked; the student does the solve-through,
  back-substitution/interpretation, and check. At least 1 step before the
  boundary and at least 2 live boxes at/after it.
- End every walk with a CHECK step that verifies the answer in the original
  question, with a `done` note confirming why it must be right.
- `input_type: multiple_choice` problems may omit guided_steps. Any other
  omission needs a `guided_skip_reason` field explaining why (rare).
- VERIFY every box value by computing it independently after writing the walk.
  The final boxes must land exactly on the stored `solutions`.

### 8. method_card (slim reference only)
Trim to: title, <= 4 short steps, content <= 140 words, one compact example.
The teaching now lives in the walks; this is the Learn-view reference.

### 9. Keep everything else
`related_videos`, `topic_links`, `worked_examples`, `passages`, exam fields,
anything else in practice_data: preserve byte-for-byte unless a filed issue
names it. You are ADDING `tier_guides`/`guided`/`guided_steps`/`hint`/`phase`
and repairing content, not rebuilding the object.

## Style rules (hard)

- **NO EM DASHES anywhere student-facing.** In maths, a dash reads as a minus
  sign. Use commas, colons, brackets, or full stops. (Internal `note` fields
  exempt.) The validator enforces this.
- Plain unicode (×, ÷, −, £, →) not HTML entities. LaTeX only inside `\(...\)`.
- GCSE reading age (15-16), warm but not chatty. Match the L09 transcripts'
  voice. Every box earns its place; no filler steps.
- British English. Money in £.

## Special case: algebra L10 (Simultaneous Equations, Quadratic)

Its answers are two (x, y) PAIRS, which no input type can represent. Convert
each problem: display ends with "Give the two x-values." and `solutions` =
the two x values, `input_type: "two_solutions"` (unordered pair input:
correct here since both are x). The guided walk still finds both full pairs
and says so; the typed answer is just the x-values. Verify both pairs satisfy
BOTH equations. Linear-pair problems in other lessons (if any) use
`input_type: "xy_pair"` (ordered x-then-y input) like L09.

## Ship gate (in this order)

1. Write the finished practice_data to
   `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\lesson_<KEY>.json`
2. Run the validator until it passes:
   `python "C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_validate_guided.py" <that file>`
3. PATCH the live row with the file's contents.
4. Write `C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\changes_<KEY>.json`:
   `{"key", "problems_fixed": [{tier, index, what, old, new}], "issues_resolved": n, "opener_concept": "...", "notes": "..."}`

---

# CHECKER BRIEF (independent verification agent)

You are checking a lesson someone else converted. Be adversarial: the
overnight audit's verification layer wrongly cleared 2 real errors; do not
rubber-stamp. Fetch the LIVE row (GET above). Then:

1. **Maths**: fresh-solve every problem from its display. Stored solutions
   must match exactly. Non-calculator problems must have clean answers.
2. **Every box**: recompute every `guided_steps`/`teach`/`opener` box value
   independently. The walk must be mathematically continuous (each step
   follows from the previous) and land on the stored solutions.
3. **Expects**: commit each misconception's described error yourself; your
   wrong answer must equal `expect` (or expect must be null).
4. **Completion boundary**: the pre-worked half must genuinely be the set-up
   phase; the live half must be a meaningful finish (>= 2 boxes).
5. **Opener**: could a student who never met this topic answer box 1 by
   common sense? Does the reveal honestly name the method?
6. **Preservation**: compare against the pre-dump entry for this lesson:
   `related_videos`, `topic_links`, `worked_examples` (unless legitimately
   trimmed by spec section 8), and other untouched fields must be unchanged.
7. **Style**: no em dashes in student-facing strings; hints plain text;
   numeric-only boxes; tier guides within budget.
8. Run the validator yourself on the live data.

Report every defect with its exact path (e.g. `silver[3].guided_steps[4]`).
Judge pass/fail: FAIL on any maths error, any box that doesn't compute, any
expect that doesn't reproduce, or lost preserved fields. Style nits alone
with correct maths: pass=true but list them in findings.
